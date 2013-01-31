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
            default=[u'quickdraw', u'rope', u'alloy carabiner',
                    u'steel carabiner', u'belay device', u'sling', u'bandage'
                ],
        )

    kit_types = schema.List(
            title=u'Kit Types',
            description=u'Separate types by new lines',
            value_type=schema.TextLine(),
            default=[u'top rope', u'lead', u'trad rack', u'hiking',
                    u'first aid'
                ],
        )
