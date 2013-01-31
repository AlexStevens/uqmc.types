from zope import schema
from plone.directives import form
from plone.formwidget.autocomplete import AutocompleteFieldWidget

from uqmc.types.interfaces.binders import member_source_binder, \
                                            geartypes_source_binder, \
                                            kittypes_source_binder


class IUQMCGear(form.Schema):
    """ Content type for all UQMC Gear
    """

    type = schema.Choice(
            title=u'Gear Type',
            description=u'Choose a type out of the following (add more via the UQMC Configuration)',
            source=geartypes_source_binder,
        )

    total = schema.Int(
            title=u'Number of Pieces',
            description=u'The total gear count for this purchase',
        )

    form.widget(on_loan=AutocompleteFieldWidget)
    on_loan = schema.Choice(
            title=u'Currently on loan to',
            source=member_source_binder,
            required=False,
        )


class IUQMCKit(form.Schema):
    """ Content type for all UQMC Kits that hold gear
    """

    type = schema.Choice(
            title=u'Gear Type',
            description=u'Choose a type out of the following (add more via the UQMC Configuration)',
            source=kittypes_source_binder,
        )

    form.widget(on_loan=AutocompleteFieldWidget)
    on_loan = schema.Choice(
            title=u'Currently on loan to',
            source=member_source_binder,
            required=False,
        )