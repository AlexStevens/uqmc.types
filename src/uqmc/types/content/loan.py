from five import grok
from z3c.form import button
from zope.event import notify
from zope.component import getUtility
from plone.dexterity.content import Item
from zope.interface import implements, Invalid
from plone.dexterity.events import AddCancelledEvent
from plone.dexterity.events import EditCancelledEvent
from plone.dexterity.events import EditFinishedEvent
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.app.content.interfaces import INameFromTitle
from plone.directives.dexterity import AddForm, EditForm
from z3c.form.interfaces import WidgetActionExecutionError
from Products.statusmessages.interfaces import IStatusMessage

from uqmc.types.interfaces.content import IUQMCLoan


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


class UQMCLoanForm(object):
    def get_container_and_count(self):
        self.container = None
        self.count_left = 0

        if hasattr(self.context, 'get_gear'):
            self.container = self.context.get_gear()
            self.count_left = self.container.count_left()
            if hasattr(self.container, 'get_kit') and \
                    self.container.get_kit().count_left() <= 0:
                self.count_left = 0
                self.container = self.container.get_kit()
        elif hasattr(self.context, 'get_kit'):
            self.container = self.context.get_kit()
            self.count_left = self.container.count_left()


class UQMCLoanAddForm(UQMCLoanForm, AddForm):
    grok.name('uqmc.types.loan')

    def updateWidgets(self):
        super(UQMCLoanAddForm, self).updateWidgets()
        self.get_container_and_count()
        self.widgets['quantity'].value = self.count_left

    @button.buttonAndHandler(u'Save', name='save')
    def handleAdd(self, action):
        data, errors = self.extractData()

        if not self.container:
            IStatusMessage(self.request).addStatusMessage(
                    'The loan must be placed within a Kit or Gear type!',
                    'error'
                )
            return

        if 'quantity' in data and int(data['quantity']) > self.count_left:
            raise WidgetActionExecutionError(
                    'quantity',
                    Invalid('There are only %s item(s) left to loan' % \
                            self.count_left
                        )
                )

        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True
            IStatusMessage(self.request).addStatusMessage(u"Item created", "info")

    @button.buttonAndHandler(u'Cancel', name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(u"Add New Item operation cancelled", "info")
        self.request.response.redirect(self.nextURL())
        notify(AddCancelledEvent(self.context))


class UQMCLoanEditForm(UQMCLoanForm, EditForm):
    grok.context(IUQMCLoan)

    def updateWidgets(self):
        super(UQMCLoanEditForm, self).updateWidgets()
        self.get_container_and_count()

    @button.buttonAndHandler(u'Save', name='save')
    def handleApply(self, action):
        data, errors = self.extractData()

        if not self.container:
            IStatusMessage(self.request).addStatusMessage(
                    'The loan must be placed within a Kit or Gear type!',
                    'error'
                )
            return

        loanable = self.count_left + self.context.quantity
        if 'quantity' in data and int(data['quantity']) > loanable:
            raise WidgetActionExecutionError(
                    'quantity',
                    Invalid('There are only %s item(s) left to loan' % loanable)
                )

        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(u"Changes saved", "info")
        self.request.response.redirect(self.nextURL())
        notify(EditFinishedEvent(self.context))

    @button.buttonAndHandler(u'Cancel', name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(u"Edit cancelled", "info")
        self.request.response.redirect(self.nextURL())
        notify(EditCancelledEvent(self.context))
