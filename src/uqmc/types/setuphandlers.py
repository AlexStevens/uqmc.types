from plone import api
from DateTime import DateTime


def new_executives_year_group():
    current_year = DateTime().year()
    current_executives = 'UQMC Executives %s' % str(current_year)
    if not api.group.get(groupname=current_executives):
        api.group.create(
                groupname=current_executives,
                title=current_executives,
                description='UQMC Executives for the year %s' % current_year
            )
        api.group.grant_roles(groupname=current_executives, roles=['Manager'])

        for group in api.group.get_groups():
            if 'UQMC Executives' in group.id and \
                    int(group.id.split(' ')[2]) < (current_year - 1):
                api.group.revoke_roles(group=group, roles=['Manager'])
                api.group.grant_roles(group=group, roles=['Reader'])


def install(context):
    if context.readDataFile('uqmc.types.marker.txt') is None:
        return

    # Assign UQMC Specific Groups, remove Reviewers and Administrators
    for group in api.group.get_groups():
        if group.id in ['Reviewers', 'Administrators']:
            api.group.delete(groupname=group.id)

    new_executives_year_group()
