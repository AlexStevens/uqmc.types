from zope import schema
from plone.directives import form
from Products.Archetypes.Field import LinesField
from Products.Archetypes.Widget import LinesWidget


class IUQMCConfiguration(form.Schema):
    """ Interface for UQMC Configuration Panel
    """

    gear_types = schema.List(
            title=u'Gear Types',
            description=u'Separate types by new lines',
            value_type=schema.TextLine(),
            default=[u'Quickdraw', u'Rope', u'Alloy Carabiner',
                    u'Steel Carabiner', u'Belay Device', u'Sling', u'Bandage'
                ],
        )

    kit_types = schema.List(
            title=u'Kit Types',
            description=u'Separate types by new lines',
            value_type=schema.TextLine(),
            default=[u'Top Rope', u'Lead', u'Trad Rack', u'Hiking',
                    u'First Aid'
                ],
        )
