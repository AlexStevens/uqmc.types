from five import grok
from plone.dexterity.content import Container
from plone.directives.dexterity import AddForm, EditForm

from uqmc.types.interfaces.content import IUQMCGear


class UQMCGear(Container):
    pass


class UQMCGearAddForm(AddForm):
    grok.name('uqmc.types.gear')


class UQMCGearEditForm(EditForm):
    grok.context(IUQMCGear)
