from five import grok
from zope.interface import implements
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry
from Products.CMFCore.utils import getToolByName
from zope.schema.vocabulary import SimpleVocabulary
from z3c.formwidget.query.interfaces import IQuerySource
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

        portal_url = self.context.portal_url()
        userprefs_url = '/'+portal_url.split('/')[-1]+'/@@usergroup-userprefs'
        user_prefs = self.context.unrestrictedTraverse(userprefs_url)
        members = user_prefs.membershipSearch(
                searchString=name_filter,
                searchGroups=False,
            )

        for member in members:
            member_id = member.getProperty('id')
            member_name = member.getProperty('fullname')
            term = SimpleVocabulary.createTerm(
                    member_id,
                    str(member_id),
                    member_name
                )
            self.terms.append(term)
            self.by_id[member_id] = term

        return self.terms
