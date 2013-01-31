from five import grok
from plone.dexterity.content import Container
from plone.directives.dexterity import AddForm, EditForm

from uqmc.types.interfaces.content import IUQMCKit


class UQMCKit(Container):
    pass


class UQMCKitAddForm(AddForm):
    grok.name('uqmc.types.kit')


class UQMCKitEditForm(EditForm):
    grok.context(IUQMCKit)
