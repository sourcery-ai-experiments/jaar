from src.world.z_gift import giftunit_shop, GiftUnit
from src.world.examples.example_atoms import (
    get_atom_example_beliefunit_knee,
    get_atom_example_ideaunit_ball,
    get_atom_example_ideaunit_knee,
    get_atom_example_ideaunit_sports,
)


def yao_sue_giftunit() -> GiftUnit:
    return giftunit_shop(_giver="Yao", _gift_id=37, _takers=set("Sue"))


def get_sue_giftunit() -> GiftUnit:
    return giftunit_shop(_giver="Sue", _gift_id=37, _takers=set("Yao"))


def sue_1atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(_giver="Sue", _gift_id=53, _takers=set("Yao"))
    x_giftunit._bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
    return x_giftunit


def sue_2atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(_giver="Sue", _gift_id=53, _takers=set("Yao"))
    x_giftunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    x_giftunit._bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
    return x_giftunit


def sue_3atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(_giver="Sue", _gift_id=37, _takers=set("Yao"))
    x_giftunit._bookunit.set_agendaatom(get_atom_example_beliefunit_knee())
    x_giftunit._bookunit.set_agendaatom(get_atom_example_ideaunit_ball())
    x_giftunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    return x_giftunit


def sue_4atomunits_giftunit() -> GiftUnit:
    x_giftunit = giftunit_shop(_giver="Sue", _gift_id=47, _takers=set("Yao"))
    x_giftunit._bookunit.set_agendaatom(get_atom_example_beliefunit_knee())
    x_giftunit._bookunit.set_agendaatom(get_atom_example_ideaunit_ball())
    x_giftunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    x_giftunit._bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
    return x_giftunit
