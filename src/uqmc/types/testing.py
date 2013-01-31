from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting

from plone.testing import z2

from zope.configuration import xmlconfig


class UqmctypesLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import uqmc.types
        xmlconfig.file(
            'configure.zcml',
            uqmc.types,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'uqmc.types:default')

UQMC_TYPES_FIXTURE = UqmctypesLayer()
UQMC_TYPES_INTEGRATION_TESTING = IntegrationTesting(
    bases=(UQMC_TYPES_FIXTURE,),
    name="UqmctypesLayer:Integration"
)
