from plone import api
from DateTime import DateTime


def install(context):
    if context.readDataFile('uqmc.types.marker.txt') is None:
        return

    # Assign UQMC Specific Groups, remove Reviewers and Administrators
    for group in api.group.get_groups():
        if group.id in ['Reviewers', 'Administrators']:
            api.group.delete(groupname=group.id)
