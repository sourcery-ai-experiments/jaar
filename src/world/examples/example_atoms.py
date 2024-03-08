from src._road.road import create_road
from src.agenda.atom import agendaatom_shop, atom_insert, AgendaAtom


def get_beliefunit_atom_example_01() -> AgendaAtom:
    # WHEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    knee_open = 7

    # WHEN
    x_category = "agenda_idea_beliefunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    insert_beliefunit_agendaatom = agendaatom_shop(x_category, atom_insert())
    insert_beliefunit_agendaatom.set_required_arg(road_text, ball_road)
    insert_beliefunit_agendaatom.set_required_arg(base_text, knee_road)
    insert_beliefunit_agendaatom.set_optional_arg(open_text, knee_open)

    return insert_beliefunit_agendaatom
