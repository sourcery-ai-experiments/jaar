from src._road.road import create_road
from src.atom.quark import (
    quarkunit_shop,
    quark_insert,
    get_from_json as quarkunit_get_from_json,
)
from src._instrument.python import x_is_json


def test_QuarkUnit_get_dict_ReturnsCorrectObj():
    # GIVEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    x_category = "world_idea_factunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    nigh_text = "nigh"
    knee_open = 7
    knee_nigh = 13
    insert_factunit_quarkunit = quarkunit_shop(x_category, quark_insert())
    insert_factunit_quarkunit.set_required_arg(road_text, ball_road)
    insert_factunit_quarkunit.set_required_arg(base_text, knee_road)
    insert_factunit_quarkunit.set_optional_arg(open_text, knee_open)
    insert_factunit_quarkunit.set_optional_arg(nigh_text, knee_nigh)

    # WHEN
    quark_dict = insert_factunit_quarkunit.get_dict()

    # THEN
    assert quark_dict == {
        "category": x_category,
        "crud_text": quark_insert(),
        "required_args": {road_text: ball_road, base_text: knee_road},
        "optional_args": {open_text: knee_open, nigh_text: knee_nigh},
    }


def test_QuarkUnit_get_json_ReturnsCorrectObj():
    # GIVEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    x_category = "world_idea_factunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    nigh_text = "nigh"
    knee_open = 7
    knee_nigh = 13
    insert_factunit_quarkunit = quarkunit_shop(x_category, quark_insert())
    insert_factunit_quarkunit.set_required_arg(road_text, ball_road)
    insert_factunit_quarkunit.set_required_arg(base_text, knee_road)
    insert_factunit_quarkunit.set_optional_arg(open_text, knee_open)
    insert_factunit_quarkunit.set_optional_arg(nigh_text, knee_nigh)

    # WHEN
    quark_json = insert_factunit_quarkunit.get_json()

    # THEN
    assert x_is_json(quark_json)


def test_quarkunit_get_from_json_ReturnsCorrectObj():
    # GIVEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    x_category = "world_idea_factunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    nigh_text = "nigh"
    knee_open = 7
    knee_nigh = 13
    gen_quarkunit = quarkunit_shop(x_category, quark_insert())
    gen_quarkunit.set_required_arg(road_text, ball_road)
    gen_quarkunit.set_required_arg(base_text, knee_road)
    gen_quarkunit.set_optional_arg(open_text, knee_open)
    gen_quarkunit.set_optional_arg(nigh_text, knee_nigh)
    quark_json = gen_quarkunit.get_json()

    # WHEN
    json_quarkunit = quarkunit_get_from_json(quark_json)

    # THEN
    assert json_quarkunit.category == gen_quarkunit.category
    assert json_quarkunit.crud_text == gen_quarkunit.crud_text
    assert json_quarkunit.required_args == gen_quarkunit.required_args
    assert json_quarkunit.optional_args == gen_quarkunit.optional_args
    assert json_quarkunit == gen_quarkunit
