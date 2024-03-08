from src._road.road import create_road
from src.agenda.party import partyunit_shop
from src.agenda.atom import (
    AgendaAtom,
    agendaatom_shop,
    atom_insert,
    atom_delete,
    atom_update,
    category_ref,
    is_category_ref,
    get_atom_config_dict,
    get_mog,
    set_mog,
    get_atom_columns_build,
)


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
