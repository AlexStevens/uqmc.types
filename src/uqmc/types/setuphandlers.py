from zope.component import getUtility
from Products.TinyMCE.interfaces.utility import ITinyMCE

def install(context):
    if context.readDataFile('uqmc.types.marker.txt') is None:
        return

    cts = ['uqmc.types.gear']
    tinymce = getUtility(ITinyMCE)

    linkable = tinymce.linkable.split('\n')
    linkable += [ct for ct in cts if ct not in linkable]

    tinymce.linkable = '\n'.join( linkable )
