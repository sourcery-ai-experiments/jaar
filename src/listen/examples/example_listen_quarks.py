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


def get_quark_example_ideaunit_sports(real_id: RealID = None) -> QuarkUnit:
    if real_id is None:
        real_id = get_test_real_id()
    sports_text = "sports"
    x_category = "truth_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    insert_ideaunit_quarkunit = quarkunit_shop(x_category, quark_insert())
    insert_ideaunit_quarkunit.set_required_arg(label_text, sports_text)
    insert_ideaunit_quarkunit.set_required_arg(parent_road_text, real_id)
    return insert_ideaunit_quarkunit


def get_quark_example_ideaunit_ball(real_id: RealID = None) -> QuarkUnit:
    if real_id is None:
        real_id = get_test_real_id()
    sports_text = "sports"
    sports_road = create_road(real_id, sports_text)
    ball_text = "basketball"
    x_category = "truth_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    insert_ideaunit_quarkunit = quarkunit_shop(x_category, quark_insert())
    insert_ideaunit_quarkunit.set_required_arg(label_text, ball_text)
    insert_ideaunit_quarkunit.set_required_arg(parent_road_text, sports_road)
    return insert_ideaunit_quarkunit


def get_quark_example_ideaunit_knee(real_id: RealID = None) -> QuarkUnit:
    if real_id is None:
        real_id = get_test_real_id()
    sports_text = "sports"
    sports_road = create_road(real_id, sports_text)
    knee_text = "knee"
    knee_begin = 1
    knee_close = 71
    x_category = "truth_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    begin_text = "_begin"
    close_text = "_close"
    insert_ideaunit_quarkunit = quarkunit_shop(x_category, quark_insert())
    insert_ideaunit_quarkunit.set_required_arg(label_text, knee_text)
    insert_ideaunit_quarkunit.set_required_arg(parent_road_text, sports_road)
    insert_ideaunit_quarkunit.set_optional_arg(begin_text, knee_begin)
    insert_ideaunit_quarkunit.set_optional_arg(close_text, knee_close)
    return insert_ideaunit_quarkunit


def get_quark_example_factunit_knee(real_id: RealID = None) -> QuarkUnit:
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
    x_category = "truth_idea_factunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    nigh_text = "nigh"
    insert_factunit_quarkunit = quarkunit_shop(x_category, quark_insert())
    insert_factunit_quarkunit.set_required_arg(road_text, ball_road)
    insert_factunit_quarkunit.set_required_arg(base_text, knee_road)
    insert_factunit_quarkunit.set_optional_arg(open_text, knee_open)
    insert_factunit_quarkunit.set_optional_arg(nigh_text, knee_nigh)
    return insert_factunit_quarkunit


def get_nucunit_carm_example() -> NucUnit:
    sue_nucunit = nucunit_shop()

    truthunit_text = "truthunit"
    pool_quarkunit = quarkunit_shop(truthunit_text, quark_update())
    pool_attribute = "_other_credor_pool"
    pool_quarkunit.set_optional_arg(pool_attribute, 77)
    sue_nucunit.set_quarkunit(pool_quarkunit)

    category = "truth_otherunit"
    carm_text = "Carmen"
    carm_quarkunit = quarkunit_shop(category, quark_delete())
    carm_quarkunit.set_required_arg("other_id", carm_text)
    sue_nucunit.set_quarkunit(carm_quarkunit)
    return sue_nucunit
