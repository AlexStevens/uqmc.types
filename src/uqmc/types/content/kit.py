from five import grok
from zope.component import getUtility
from Products.CMFPlone.interfaces import IPloneSiteRoot
from plone.dexterity.content import Container
from plone.directives.dexterity import AddForm, EditForm

from uqmc.types.interfaces.content import IUQMCKit


class UQMCKit(Container):
    def count_left(self):
        total_left = 1

        catalog = getUtility(IPloneSiteRoot).portal_catalog
        gear_path = '/'.join(self.getPhysicalPath())
        results = catalog(
                path={'query': gear_path, 'depth': 1},
                portal_type='uqmc.types.loan',
            )

        for loan in results:
            loan = loan.getObject()
            total_left -= loan.quantity

        return total_left


class UQMCKitAddForm(AddForm):
    grok.name('uqmc.types.kit')


class UQMCKitEditForm(EditForm):
    grok.context(IUQMCKit)
