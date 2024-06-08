from src.change.change import changeunit_shop, ChangeUnit
from src.change.examples.example_atoms import (
    get_atom_example_beliefunit_knee,
    get_atom_example_ideaunit_ball,
    get_atom_example_ideaunit_knee,
    get_atom_example_ideaunit_sports,
)


def yao_sue_changeunit() -> ChangeUnit:
    return changeunit_shop(_giver="Yao", _change_id=37, _faces=set("Sue"))


def get_sue_changeunit() -> ChangeUnit:
    return changeunit_shop(_giver="Sue", _change_id=37, _faces=set("Yao"))


def sue_1atomunits_changeunit() -> ChangeUnit:
    x_changeunit = changeunit_shop(_giver="Sue", _change_id=53, _faces=set("Yao"))
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
    return x_changeunit


def sue_2atomunits_changeunit() -> ChangeUnit:
    x_changeunit = changeunit_shop(_giver="Sue", _change_id=53, _faces=set("Yao"))
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
    return x_changeunit


def sue_3atomunits_changeunit() -> ChangeUnit:
    x_changeunit = changeunit_shop(_giver="Sue", _change_id=37, _faces=set("Yao"))
    x_changeunit._bookunit.set_agendaatom(get_atom_example_beliefunit_knee())
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_ball())
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    return x_changeunit


def sue_4atomunits_changeunit() -> ChangeUnit:
    x_changeunit = changeunit_shop(_giver="Sue", _change_id=47, _faces=set("Yao"))
    x_changeunit._bookunit.set_agendaatom(get_atom_example_beliefunit_knee())
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_ball())
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_knee())
    x_changeunit._bookunit.set_agendaatom(get_atom_example_ideaunit_sports())
    return x_changeunit
