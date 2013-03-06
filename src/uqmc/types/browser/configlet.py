from five import grok
from plone import api
from DateTime import DateTime
from plone.directives import form
from zope.interface import Interface
from zope.component import queryUtility
from plone.registry.interfaces import IRegistry

from uqmc.types.interfaces.browser import IUQMCConfiguration


def create_year_exec_group(executive):
    login_id = executive[0].strip()
    new_group_id = executive[1].strip() + '-' + \
            executive[2].strip().replace(' ', '_')
    new_group_title = executive[1].strip() + '-' + executive[2].strip()

    try:
        users = api.user.get_users(groupname=new_group_id)
        for user in users:
            if user.id != login_id:
                """ Remove this user from group """
                # TODO
            else:
                break
    except api.exc.GroupNotFoundError, e:
        api.group.create(
                groupname=new_group_id,
                title=new_group_title,
                description='%s for the year %s' % (
                        executive[2].strip(),
                        executive[1].strip()
                    )
            )
        api.group.grant_roles(groupname=new_group_id, roles=['Manager'])
        if not api.user.get(username=login_id):
            raise Exception
        api.group.add_user(groupname=new_group_id, username=login_id)


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
        current_year = DateTime().year()
        registry = queryUtility(IRegistry)
        settings = registry.forInterface(IUQMCConfiguration)

        new_exec = data.get('executives', None)
        if settings.executives != new_exec:
            settings.executives = new_exec
            for new in new_exec:
                executive = new.split('|')
                if len(executive) != 3:
                    raise Exception
                else:
                    create_year_exec_group(executive)

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
