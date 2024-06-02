from src._road.road import create_road, RealID
from src.change.atom import (
    agendaatom_shop,
    atom_delete,
    atom_insert,
    atom_update,
    AgendaAtom,
)
from src.change.book import bookunit_shop, BookUnit
from src.real.examples.real_env_kit import get_test_real_id


def get_atom_example_ideaunit_sports(real_id: RealID = None) -> AgendaAtom:
    if real_id is None:
        real_id = get_test_real_id()
    sports_text = "sports"
    x_category = "agenda_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    insert_ideaunit_agendaatom = agendaatom_shop(x_category, atom_insert())
    insert_ideaunit_agendaatom.set_required_arg(label_text, sports_text)
    insert_ideaunit_agendaatom.set_required_arg(parent_road_text, real_id)
    return insert_ideaunit_agendaatom


def get_atom_example_ideaunit_ball(real_id: RealID = None) -> AgendaAtom:
    if real_id is None:
        real_id = get_test_real_id()
    sports_text = "sports"
    sports_road = create_road(real_id, sports_text)
    ball_text = "basketball"
    x_category = "agenda_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    insert_ideaunit_agendaatom = agendaatom_shop(x_category, atom_insert())
    insert_ideaunit_agendaatom.set_required_arg(label_text, ball_text)
    insert_ideaunit_agendaatom.set_required_arg(parent_road_text, sports_road)
    return insert_ideaunit_agendaatom


def get_atom_example_ideaunit_knee(real_id: RealID = None) -> AgendaAtom:
    if real_id is None:
        real_id = get_test_real_id()
    sports_text = "sports"
    sports_road = create_road(real_id, sports_text)
    knee_text = "knee"
    knee_begin = 1
    knee_close = 71
    x_category = "agenda_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    begin_text = "_begin"
    close_text = "_close"
    insert_ideaunit_agendaatom = agendaatom_shop(x_category, atom_insert())
    insert_ideaunit_agendaatom.set_required_arg(label_text, knee_text)
    insert_ideaunit_agendaatom.set_required_arg(parent_road_text, sports_road)
    insert_ideaunit_agendaatom.set_optional_arg(begin_text, knee_begin)
    insert_ideaunit_agendaatom.set_optional_arg(close_text, knee_close)
    return insert_ideaunit_agendaatom


def get_atom_example_beliefunit_knee(real_id: RealID = None) -> AgendaAtom:
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
    x_category = "agenda_idea_beliefunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    nigh_text = "nigh"
    insert_beliefunit_agendaatom = agendaatom_shop(x_category, atom_insert())
    insert_beliefunit_agendaatom.set_required_arg(road_text, ball_road)
    insert_beliefunit_agendaatom.set_required_arg(base_text, knee_road)
    insert_beliefunit_agendaatom.set_optional_arg(open_text, knee_open)
    insert_beliefunit_agendaatom.set_optional_arg(nigh_text, knee_nigh)
    return insert_beliefunit_agendaatom


def get_bookunit_carm_example() -> BookUnit:
    sue_bookunit = bookunit_shop()

    agendaunit_text = "agendaunit"
    pool_agendaatom = agendaatom_shop(agendaunit_text, atom_update())
    pool_attribute = "_party_creditor_pool"
    pool_agendaatom.set_optional_arg(pool_attribute, 77)
    sue_bookunit.set_agendaatom(pool_agendaatom)

    category = "agenda_partyunit"
    carm_text = "Carmen"
    carm_agendaatom = agendaatom_shop(category, atom_delete())
    carm_agendaatom.set_required_arg("party_id", carm_text)
    sue_bookunit.set_agendaatom(carm_agendaatom)
    return sue_bookunit
