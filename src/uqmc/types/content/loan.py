from five import grok
from zope.interface import implements
from zope.component import getUtility
from plone.dexterity.content import Item
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.content.interfaces import INameFromTitle


class INameFromPersonName(INameFromTitle):
    """ Marker interface for new 'title' naming scheme
    """


class NameFromPersonName(object):
    """ Override the default 'title' naming scheme. Will also pass this title
        to the 'id' setting functions.
    """

    implements(INameFromPersonName)

    def __init__(self, context):
        self.context = context

    @property
    def title(self):
        member = getUtility(IPloneSiteRoot).portal_membership.getMemberById(
                self.context.member_id
            )
        if member:
            return member.getProperty('fullname') or self.context.member_id
        else:
            return self.context.member_id


class UQMCLoan(Item):
    def Title(self):
        member = getUtility(IPloneSiteRoot).portal_membership.getMemberById(
                self.member_id
            )
        name = member.getProperty('fullname') or str(self.member_id)
        return "Loan by " + name
