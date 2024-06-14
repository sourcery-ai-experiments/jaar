from src._road.jaar_config import get_test_real_id
from src._road.road import create_road, RealID
from src.atom.quark import quarkunit_shop, quark_insert, QuarkUnit


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
