from src._road.road import create_road
from src.agenda.party import partylink_shop
from src.agenda.reason_idea import beliefunit_shop
from src.agenda.group import groupunit_shop
from src.agenda.atom import (
    atom_update,
    atom_delete,
    atom_insert,
    agendaatom_shop,
    atom_mstr_table_name,
    atom_hx_table_name,
    get_agendaatom_from_rowdata,
)
from src.instrument.sqlite import get_rowdata
from pytest import raises as pytest_raises
from sqlite3 import connect as sqlite3_connect


def test_AgendaAtom_get_description_ReturnsCorrectObj_AgendaUnitSimpleAttrs():
    # WHEN
    new2_value = 66
    category = "agendaunit"
    opt_arg2 = "_max_tree_traverse"
    x_agendaatom = agendaatom_shop(category, atom_update())
    x_agendaatom.set_optional_arg(opt_arg2, new2_value)
    # THEN
    assert (
        x_agendaatom.get_description()
        == f"Agenda's maximum number of Agenda output evaluations changed to {new2_value}."
    )

    # WHEN
    new5_value = "override"
    opt_arg5 = "_meld_strategy"
    x_agendaatom = agendaatom_shop(category, atom_update())
    x_agendaatom.set_optional_arg(opt_arg5, new5_value)
    # THEN
    assert (
        x_agendaatom.get_description()
        == f"Agenda's Meld Strategy changed to {new5_value}."
    )

    # WHEN
    new3_value = 77
    opt_arg3 = "_party_creditor_pool"
    x_agendaatom = agendaatom_shop(category, atom_update())
    x_agendaatom.set_optional_arg(opt_arg3, new3_value)
    # THEN
    assert (
        x_agendaatom.get_description()
        == f"Agenda's creditor pool limit changed to {new3_value}."
    )

    # WHEN
    new4_value = 88
    opt_arg4 = "_party_debtor_pool"
    x_agendaatom = agendaatom_shop(category, atom_update())
    x_agendaatom.set_optional_arg(opt_arg4, new4_value)
    # THEN
    assert (
        x_agendaatom.get_description()
        == f"Agenda's debtor pool limit changed to {new4_value}."
    )

    # GIVEN
    new1_value = 55
    opt_arg1 = "_weight"
    # WHEN
    x_agendaatom = agendaatom_shop(category, atom_update())
    x_agendaatom.set_optional_arg(opt_arg1, new1_value)
    # THEN
    assert x_agendaatom.get_description() == f"Agenda's weight changed to {new1_value}."


def test_AgendaAtom_get_insert_sqlstr_RaisesErrorWhen_is_valid_False():
    # WHEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)

    # WHEN
    x_category = "agenda_idea_beliefunit"
    update_disc_agendaatom = agendaatom_shop(x_category, atom_update())
    # update_disc_agendaatom.set_required_arg("road", ball_road)
    update_disc_agendaatom.set_required_arg("base", knee_road)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        update_disc_agendaatom.get_insert_sqlstr()
    assert (
        str(excinfo.value)
        == f"Cannot get_insert_sqlstr '{x_category}' with is_valid=False."
    )


def test_AgendaAtom_get_insert_sqlstr_ReturnsCorrectObj_AgendaUnitSimpleAttrs():
    # WHEN
    new2_value = 66
    category = "agendaunit"
    opt_arg2 = "_max_tree_traverse"
    x_agendaatom = agendaatom_shop(category, atom_update())
    x_agendaatom.set_optional_arg(opt_arg2, new2_value)
    # THEN
    x_table = "atom_hx"
    example_sqlstr = f"""INSERT INTO {x_table} (
  {category}_{atom_update()}_{opt_arg2}
)
VALUES (
  {new2_value}
)
;"""
    assert x_agendaatom.get_insert_sqlstr() == example_sqlstr


def test_AgendaAtom_get_insert_sqlstr_ReturnsCorrectObj_idea_beliefunit():
    # GIVEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    knee_open = 7
    x_category = "agenda_idea_beliefunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    update_disc_agendaatom = agendaatom_shop(x_category, atom_insert())
    update_disc_agendaatom.set_required_arg(road_text, ball_road)
    update_disc_agendaatom.set_required_arg(base_text, knee_road)
    update_disc_agendaatom.set_optional_arg(open_text, knee_open)

    # WHEN
    gen_sqlstr = update_disc_agendaatom.get_insert_sqlstr()

    # THEN
    example_sqlstr = f"""INSERT INTO {atom_hx_table_name()} (
  {x_category}_{atom_insert()}_{road_text}
, {x_category}_{atom_insert()}_{base_text}
, {x_category}_{atom_insert()}_{open_text}
)
VALUES (
  '{ball_road}'
, '{knee_road}'
, {knee_open}
)
;"""
    assert gen_sqlstr == example_sqlstr


def test_get_agendaatom_from_rowdata_ReturnsCorrectObj_idea_beliefunit():
    # GIVEN
    sports_text = "sports"
    sports_road = create_road("a", sports_text)
    ball_text = "basketball"
    ball_road = create_road(sports_road, ball_text)
    knee_text = "knee"
    knee_road = create_road("a", knee_text)
    knee_open = 7
    x_category = "agenda_idea_beliefunit"
    road_text = "road"
    base_text = "base"
    open_text = "open"
    x_sqlstr = f"""SELECT
  '{ball_road}' as {x_category}_{atom_insert()}_{road_text}
, '{knee_road}' as {x_category}_{atom_insert()}_{base_text}
, {knee_open} as {x_category}_{atom_insert()}_{open_text}
"""
    x_conn = sqlite3_connect(":memory:")
    x_rowdata = get_rowdata(atom_hx_table_name(), x_conn, x_sqlstr)

    # WHEN
    x_agendaatom = get_agendaatom_from_rowdata(x_rowdata)

    # THEN
    update_disc_agendaatom = agendaatom_shop(x_category, atom_insert())
    update_disc_agendaatom.set_required_arg(road_text, ball_road)
    update_disc_agendaatom.set_required_arg(base_text, knee_road)
    update_disc_agendaatom.set_optional_arg(open_text, knee_open)
    assert update_disc_agendaatom.category == x_agendaatom.category
    assert update_disc_agendaatom.crud_text == x_agendaatom.crud_text
    assert update_disc_agendaatom.required_args == x_agendaatom.required_args
    assert update_disc_agendaatom.optional_args == x_agendaatom.optional_args
