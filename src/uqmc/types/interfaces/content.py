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


class IUQMCKit(form.Schema):
    """ Content type for all UQMC Kits that hold gear
    """

    type = schema.Choice(
            title=u'Gear Type',
            description=u'Choose a type out of the following (add more via the UQMC Configuration)',
            source=kittypes_source_binder,
        )


class IUQMCLoan(form.Schema):
    """ Content type for all UQMC Loans of Kits/Gear
    """

    form.widget(member=AutocompleteFieldWidget)
    member = schema.Choice(
            title=u'Member',
            description=u'Type any few letters of a members name',
            source=member_source_binder,
        )

    quantity = schema.Int(
            title=u'Number of Pieces Borrowing',
            default=1,
        )
