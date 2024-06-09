from src._road.road import create_road
from src.change.atom import (
    agendaatom_shop,
    atom_insert,
    get_from_json as agendaatom_get_from_json,
)
from src._instrument.python import x_is_json


def test_AgendaAtom_get_dict_ReturnsCorrectObj():
    # GIVEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    x_category = "agenda_idea_beliefunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    nigh_text = "nigh"
    knee_open = 7
    knee_nigh = 13
    insert_beliefunit_agendaatom = agendaatom_shop(x_category, atom_insert())
    insert_beliefunit_agendaatom.set_required_arg(road_text, ball_road)
    insert_beliefunit_agendaatom.set_required_arg(base_text, knee_road)
    insert_beliefunit_agendaatom.set_optional_arg(open_text, knee_open)
    insert_beliefunit_agendaatom.set_optional_arg(nigh_text, knee_nigh)

    # WHEN
    atom_dict = insert_beliefunit_agendaatom.get_dict()

    # THEN
    assert atom_dict == {
        "category": x_category,
        "crud_text": atom_insert(),
        "required_args": {road_text: ball_road, base_text: knee_road},
        "optional_args": {open_text: knee_open, nigh_text: knee_nigh},
    }


def test_AgendaAtom_get_json_ReturnsCorrectObj():
    # GIVEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    x_category = "agenda_idea_beliefunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    nigh_text = "nigh"
    knee_open = 7
    knee_nigh = 13
    insert_beliefunit_agendaatom = agendaatom_shop(x_category, atom_insert())
    insert_beliefunit_agendaatom.set_required_arg(road_text, ball_road)
    insert_beliefunit_agendaatom.set_required_arg(base_text, knee_road)
    insert_beliefunit_agendaatom.set_optional_arg(open_text, knee_open)
    insert_beliefunit_agendaatom.set_optional_arg(nigh_text, knee_nigh)

    # WHEN
    atom_json = insert_beliefunit_agendaatom.get_json()

    # THEN
    assert x_is_json(atom_json)


def test_agendaatom_get_from_json_ReturnsCorrectObj():
    # GIVEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    x_category = "agenda_idea_beliefunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    nigh_text = "nigh"
    knee_open = 7
    knee_nigh = 13
    gen_agendaatom = agendaatom_shop(x_category, atom_insert())
    gen_agendaatom.set_required_arg(road_text, ball_road)
    gen_agendaatom.set_required_arg(base_text, knee_road)
    gen_agendaatom.set_optional_arg(open_text, knee_open)
    gen_agendaatom.set_optional_arg(nigh_text, knee_nigh)
    atom_json = gen_agendaatom.get_json()

    # WHEN
    json_agendaatom = agendaatom_get_from_json(atom_json)

    # THEN
    assert json_agendaatom.category == gen_agendaatom.category
    assert json_agendaatom.crud_text == gen_agendaatom.crud_text
    assert json_agendaatom.required_args == gen_agendaatom.required_args
    assert json_agendaatom.optional_args == gen_agendaatom.optional_args
    assert json_agendaatom == gen_agendaatom
