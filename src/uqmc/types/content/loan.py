from five import grok
from plone.dexterity.content import Item
from plone.directives.dexterity import AddForm, EditForm

from uqmc.types.interfaces.content import IUQMCLoan


class UQMCLoan(Item):
    pass


class UQMCLoanAddForm(AddForm):
    grok.name('uqmc.types.loan')


class UQMCLoanEditForm(EditForm):
    grok.context(IUQMCLoan)
