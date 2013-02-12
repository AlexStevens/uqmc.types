from five import grok
from zope.component import getUtility
from plone.dexterity.content import Container
from Products.CMFPlone.interfaces import IPloneSiteRoot


class UQMCContainer(Container):
    def count_left(self):
        total_left = self.count

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


class UQMCKit(UQMCContainer):
    def get_kit(self):
        return self

    @property
    def count(self):
        return 1
