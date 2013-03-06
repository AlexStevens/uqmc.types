import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from plone import api
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from uqmc.types.testing import UQMC_TYPES_INTEGRATION_TESTING
from uqmc.types.interfaces.browser import IUQMCConfiguration

from DateTime import DateTime

class TestConfigletUnit(unittest.TestCase):

    layer = UQMC_TYPES_INTEGRATION_TESTING

    def setUp(self):
        # Main Layer
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']

        # Test Variables
        users = [
                'malcolm.reynolds@serenity.org',
                'zoe.washburne@serenity.org',
                'hoban.washburne@serenity.org',
                'inara.serra@serenity.org',
                'jayne.cobb@serenity.org',
                'kaylee.frye@serenity.org',
                'simon.tam@serenity.org',
                'river.tam@serenity.org',
                'derrial.book@serenity.org',
            ]

        executives = [
                unicode(users[0]+' | '+str(DateTime().year())+' | Captain'),
                unicode(users[1]+' | '+str(DateTime().year())+' | 2IC'),
                unicode(users[2]+' | '+str(DateTime().year())+' | Pilot'),
            ]

        gear_types = [
                u'Quickdraw',
                u'Rope',
                u'Alloy Carabiner',
                u'Steel Carabiner',
                u'Belay Device',
                u'Sling',
                u'Bandage',
                u'Syringe',
            ]

        kit_types = [
                u'Top Rope',
                u'Lead',
                u'Trad Rack',
                u'Hiking',
                u'First Aid',
                u'Portaledge Kit',
            ]

        self.test_data = {
                'executives': executives,
                'gear_types': gear_types,
                'kit_types': kit_types,
            }

        # Create Users, etc
        for user in users:
            api.user.create(email=user, username=user)

    def test_exec_role_creation(self):
        view = getMultiAdapter(
                (self.portal, self.request),
                name='uqmc-configuration'
            )

        view.applyChanges(self.test_data)

        for user in self.test_data.get('executives', None):
            user = user.split(' | ')
            group_id = user[1] + '-' + user[2]
            self.assertTrue(api.group.get(groupname=group_id))

    def test_gear_type_addition(self):
        settings = queryUtility(IRegistry).forInterface(IUQMCConfiguration)
        view = getMultiAdapter(
                (self.portal, self.request),
                name='uqmc-configuration'
            )

        view.applyChanges(self.test_data)

        for gear_type in self.test_data.get('gear_types', None):
            self.assertTrue(gear_type in settings.gear_types)

    def test_kit_type_addition(self):
        settings = queryUtility(IRegistry).forInterface(IUQMCConfiguration)
        view = getMultiAdapter(
                (self.portal, self.request),
                name='uqmc-configuration'
            )

        view.applyChanges(self.test_data)

        for kit_type in self.test_data.get('kit_types', None):
            self.assertTrue(kit_type in settings.kit_types)
