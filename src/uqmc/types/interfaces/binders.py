from five import grok
from zope.interface import implements
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary
from z3c.formwidget.query.interfaces import IQuerySource
from Products.PlonePAS.plugins.ufactory import PloneUser
from zope.schema.interfaces import IContextSourceBinder, IVocabularyTokenized

from uqmc.types.interfaces.browser import IUQMCConfiguration

@grok.provider(IContextSourceBinder)
def member_source_binder(context):
    return MemberSourceBinder(context)


@grok.provider(IContextSourceBinder)
def geartypes_source_binder(context):
    return type_vocabulary(type_name = 'gear_types')


@grok.provider(IContextSourceBinder)
def kittypes_source_binder(context):
    return type_vocabulary(type_name = 'kit_types')


def type_vocabulary(type_name = 'gear_types'):
    terms = []

    registry = queryUtility(IRegistry)
    settings = registry.forInterface(IUQMCConfiguration)

    for uqmc_type in getattr(settings, type_name, None):
        term = SimpleVocabulary.createTerm(
                uqmc_type,
                str(uqmc_type),
                uqmc_type
            )
        terms.append(term)

    return SimpleVocabulary(terms)


class GroupQuerySourceBase(object):
    implements(IQuerySource, IVocabularyTokenized)

    def __init__(self, context):
        self.context = context
        self.terms = None
        self.by_id = None

    def __contains__(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        if self.terms is None:
            self._create_terms()

        try:
            return value in self.by_id
        except TypeError:
            # sometimes values are not hashable
            return False

    def getTerm(self, value):
        """See zope.schema.interfaces.IBaseVocabulary"""
        if self.terms is None:
            self._create_terms()

        try:
            return self.by_id[value]
        except KeyError:
            raise LookupError(value)

    def getTermByToken(self, token):
        """See zope.schema.interfaces.IVocabularyTokenized"""
        return self.getTerm( token )

    def __iter__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        if self.terms is None:
            self._create_terms()

        return iter(self.terms)

    def __len__(self):
        """See zope.schema.interfaces.IIterableVocabulary"""
        if self.terms is None:
            self._create_terms()

        return len(self.terms)


    def search(self, query_string):
        """See z3c.formwidget.query.interfaces.IQuerySource"""
        self._create_terms(query_string)

        return self.terms


class MemberSourceBinder(GroupQuerySourceBase):
    """ Context source binder to provide vocabulary of all site users.
    """

    def _create_terms(self, name_filter = None):
        self.terms = []
        self.by_id = {}
        members = None

        membership = getToolByName(self.context, 'portal_membership')
        if not name_filter:
            members = membership.listMembers()
        else:
            keys = {}
            names = membership.searchForMembers({'name': name_filter})
            emails = membership.searchForMembers({'email': name_filter})
            for name in names:
                keys[name.getId()] = name
            for email in emails:
                keys[email.getId()] = email
            members = keys.values()

        for member in members:
            member_id = member.getProperty('id')
            if isinstance(member, PloneUser):
                member_id = member.getId()
            member_name = member.getProperty('fullname') or member_id
            term = SimpleVocabulary.createTerm(
                    member_id,
                    str(member_id),
                    member_name
                )
            self.terms.append(term)
            self.by_id[member_id] = term

        return self.terms
