from src.atom.atom import atomunit_shop, AtomUnit
from src.listen.examples.example_listen_quarks import (
    get_quark_example_beliefunit_knee,
    get_quark_example_factunit_ball,
    get_quark_example_factunit_knee,
    get_quark_example_factunit_sports,
)


def yao_sue_atomunit() -> AtomUnit:
    return atomunit_shop(person_id="Yao", _atom_id=37, _faces={"Sue"})


def get_sue_atomunit() -> AtomUnit:
    return atomunit_shop(person_id="Sue", _atom_id=37, _faces={"Yao"})


def sue_1quarkunits_atomunit() -> AtomUnit:
    x_atomunit = atomunit_shop(person_id="Sue", _atom_id=53, _faces={"Yao"})
    x_atomunit._nucunit.set_quarkunit(get_quark_example_factunit_sports())
    return x_atomunit


def sue_2quarkunits_atomunit() -> AtomUnit:
    x_atomunit = atomunit_shop(person_id="Sue", _atom_id=53, _faces={"Yao"})
    x_atomunit._nucunit.set_quarkunit(get_quark_example_factunit_knee())
    x_atomunit._nucunit.set_quarkunit(get_quark_example_factunit_sports())
    return x_atomunit


def sue_3quarkunits_atomunit() -> AtomUnit:
    x_atomunit = atomunit_shop(person_id="Sue", _atom_id=37, _faces={"Yao"})
    x_atomunit._nucunit.set_quarkunit(get_quark_example_beliefunit_knee())
    x_atomunit._nucunit.set_quarkunit(get_quark_example_factunit_ball())
    x_atomunit._nucunit.set_quarkunit(get_quark_example_factunit_knee())
    return x_atomunit


def sue_4quarkunits_atomunit() -> AtomUnit:
    x_atomunit = atomunit_shop(person_id="Sue", _atom_id=47, _faces={"Yao"})
    x_atomunit._nucunit.set_quarkunit(get_quark_example_beliefunit_knee())
    x_atomunit._nucunit.set_quarkunit(get_quark_example_factunit_ball())
    x_atomunit._nucunit.set_quarkunit(get_quark_example_factunit_knee())
    x_atomunit._nucunit.set_quarkunit(get_quark_example_factunit_sports())
    return x_atomunit
