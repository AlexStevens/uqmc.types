from zope import schema
from plone.directives import form, dexterity
from zope.interface import Invalid
from plone.formwidget.autocomplete import AutocompleteFieldWidget

from uqmc.types.interfaces.binders import member_source_binder, \
                                            geartypes_source_binder, \
                                            kittypes_source_binder


def greater_than_zero(value):
    """ Check to see if greater than zero
    """
    if int(value) > 0:
        return True
    else:
        raise Invalid(u'Please enter a value greater than zero!')


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
            constraint=greater_than_zero,
        )

    form.mode(on_loan='display')
    on_loan = schema.Int(
            title=u'On Loan',
            required=False,
            default=0,
        )


class IUQMCKit(form.Schema):
    """ Content type for all UQMC Kits that hold gear
    """

    type = schema.Choice(
            title=u'Gear Type',
            description=u'Choose a type out of the following (add more via the UQMC Configuration)',
            source=kittypes_source_binder,
        )

    form.mode(on_loan='display')
    on_loan = schema.Int(
            title=u'On Loan',
            required=False,
            default=0,
        )


class IUQMCLoan(form.Schema):
    """ Content type for all UQMC Loans of Kits/Gear
    """

    form.widget(member_id=AutocompleteFieldWidget)
    member_id = schema.Choice(
            title=u'Member',
            description=u'Type any few letters of a members name',
            source=member_source_binder,
        )

    quantity = schema.Int(
            title=u'Number of Pieces Borrowing',
            default=1,
            constraint=greater_than_zero,
        )
