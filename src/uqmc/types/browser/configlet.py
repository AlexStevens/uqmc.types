from five import grok
from plone.directives import form
from zope.interface import Interface
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from uqmc.types.interfaces.browser import IUQMCConfiguration


class UQMCConfiguration(form.SchemaEditForm):
    """ Configuration panel for UQ Mountain Club
    """

    grok.name('uqmc-configuration')
    grok.context(Interface)
    grok.require('cmf.ManagePortal')

    schema = IUQMCConfiguration

    label = "UQ Mountain Club Configuration"
    description = """Configure the various properties of the UQMC Website"""

    def getContent(self):
        registry = queryUtility(IRegistry)
        return registry.forInterface(IUQMCConfiguration)

    def applyChanges(self, data):
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IUQMCConfiguration)

        settings.gear_types = data.get('gear_types', None)
        settings.kit_types = data.get('kit_types', None)

    def updateWidgets(self):
        super(UQMCConfiguration, self).updateWidgets()
        self.widgets['gear_types'].rows = 5
        self.widgets['kit_types'].rows = 5

    def update(self):
        self.request.set('disable_border', True)
        self.request.set('disable_plone.leftcolumn', True)
        self.request.set('disable_plone.rightcolumn', True)
        super(UQMCConfiguration, self).update()
