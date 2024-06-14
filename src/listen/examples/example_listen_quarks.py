from src._road.jaar_config import get_test_real_id
from src._road.road import create_road, RealID
from src.atom.quark import (
    quarkunit_shop,
    quark_delete,
    quark_insert,
    quark_update,
    QuarkUnit,
)
from src.atom.nuc import nucunit_shop, NucUnit


def get_quark_example_oathunit_sports(real_id: RealID = None) -> QuarkUnit:
    if real_id is None:
        real_id = get_test_real_id()
    sports_text = "sports"
    x_category = "agenda_oathunit"
    label_text = "label"
    parent_road_text = "parent_road"
    insert_oathunit_quarkunit = quarkunit_shop(x_category, quark_insert())
    insert_oathunit_quarkunit.set_required_arg(label_text, sports_text)
    insert_oathunit_quarkunit.set_required_arg(parent_road_text, real_id)
    return insert_oathunit_quarkunit


def get_quark_example_oathunit_ball(real_id: RealID = None) -> QuarkUnit:
    if real_id is None:
        real_id = get_test_real_id()
    sports_text = "sports"
    sports_road = create_road(real_id, sports_text)
    ball_text = "basketball"
    x_category = "agenda_oathunit"
    label_text = "label"
    parent_road_text = "parent_road"
    insert_oathunit_quarkunit = quarkunit_shop(x_category, quark_insert())
    insert_oathunit_quarkunit.set_required_arg(label_text, ball_text)
    insert_oathunit_quarkunit.set_required_arg(parent_road_text, sports_road)
    return insert_oathunit_quarkunit


def get_quark_example_oathunit_knee(real_id: RealID = None) -> QuarkUnit:
    if real_id is None:
        real_id = get_test_real_id()
    sports_text = "sports"
    sports_road = create_road(real_id, sports_text)
    knee_text = "knee"
    knee_begin = 1
    knee_close = 71
    x_category = "agenda_oathunit"
    label_text = "label"
    parent_road_text = "parent_road"
    begin_text = "_begin"
    close_text = "_close"
    insert_oathunit_quarkunit = quarkunit_shop(x_category, quark_insert())
    insert_oathunit_quarkunit.set_required_arg(label_text, knee_text)
    insert_oathunit_quarkunit.set_required_arg(parent_road_text, sports_road)
    insert_oathunit_quarkunit.set_optional_arg(begin_text, knee_begin)
    insert_oathunit_quarkunit.set_optional_arg(close_text, knee_close)
    return insert_oathunit_quarkunit


def get_quark_example_beliefunit_knee(real_id: RealID = None) -> QuarkUnit:
    if real_id is None:
        real_id = get_test_real_id()
    sports_text = "sports"
    sports_road = create_road(real_id, sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road(real_id, knee_text)
    knee_open = 7
    knee_nigh = 23
    x_category = "agenda_oath_beliefunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    nigh_text = "nigh"
    insert_beliefunit_quarkunit = quarkunit_shop(x_category, quark_insert())
    insert_beliefunit_quarkunit.set_required_arg(road_text, ball_road)
    insert_beliefunit_quarkunit.set_required_arg(base_text, knee_road)
    insert_beliefunit_quarkunit.set_optional_arg(open_text, knee_open)
    insert_beliefunit_quarkunit.set_optional_arg(nigh_text, knee_nigh)
    return insert_beliefunit_quarkunit


def get_nucunit_carm_example() -> NucUnit:
    sue_nucunit = nucunit_shop()

    agendaunit_text = "agendaunit"
    pool_quarkunit = quarkunit_shop(agendaunit_text, quark_update())
    pool_attribute = "_party_credor_pool"
    pool_quarkunit.set_optional_arg(pool_attribute, 77)
    sue_nucunit.set_quarkunit(pool_quarkunit)

    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_quarkunit = quarkunit_shop(category, quark_delete())
    carm_quarkunit.set_required_arg("party_id", carm_text)
    sue_nucunit.set_quarkunit(carm_quarkunit)
    return sue_nucunit
