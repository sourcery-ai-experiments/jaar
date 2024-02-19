from src.agenda.meld import get_meld_default
from src.agenda.group import balancelink_shop
from src.agenda.party import partylink_shop
from src.agenda.reason_idea import beliefunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.group import groupunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.understand import (
    understandunit_shop,
    learn_update,
    learn_delete,
    learn_insert,
    learnunit_shop,
)
from src.agenda.examples.example_understands import (
    get_sue_understandunit_example1,
    get_yao_example_roadunit as yao_roadunit,
)


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_SimplestScenario():
    # GIVEN
    sue_understandunit = understandunit_shop()

    # WHEN
    sue_text = "Sue"
    sue_weight = 55
    before_sue_agendaunit = agendaunit_shop(sue_text, _weight=sue_weight)
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit._weight == sue_weight
    assert after_sue_agendaunit == before_sue_agendaunit


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnitSimpleAttrs():
    # GIVEN
    sue_understandunit = understandunit_shop()
    sue_text = "Sue"

    sue_weight = 44
    before_sue_agendaunit = agendaunit_shop(sue_text, _weight=sue_weight)

    category = "agendaunit"
    x_learnunit = learnunit_shop(category, learn_update())
    new1_value = 55
    new1_arg = "_weight"
    x_learnunit.set_optional_arg(new1_arg, new1_value)
    new2_value = 66
    new2_arg = "_max_tree_traverse"
    x_learnunit.set_optional_arg(new2_arg, new2_value)
    new3_value = 77
    new3_arg = "_party_creditor_pool"
    x_learnunit.set_optional_arg(new3_arg, new3_value)
    new4_value = 88
    new4_arg = "_party_debtor_pool"
    x_learnunit.set_optional_arg(new4_arg, new4_value)
    new5_value = "override"
    new5_arg = "_meld_strategy"
    x_learnunit.set_optional_arg(new5_arg, new5_value)
    sue_understandunit.set_learnunit(x_learnunit)

    # WHEN
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    print(f"{sue_understandunit.learnunits.keys()=}")
    assert after_sue_agendaunit._max_tree_traverse == new2_value
    assert after_sue_agendaunit._party_creditor_pool == new3_value
    assert after_sue_agendaunit._party_debtor_pool == new4_value
    assert after_sue_agendaunit._meld_strategy == new5_value
    assert after_sue_agendaunit._weight == new1_value
    assert after_sue_agendaunit._weight != before_sue_agendaunit._weight


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_party():
    # GIVEN
    sue_understandunit = understandunit_shop()
    sue_text = "Sue"

    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_agendaunit.add_partyunit(rico_text)
    before_sue_agendaunit.add_partyunit(carm_text)

    category = "partyunit"
    x_learnunit = learnunit_shop(category, learn_delete())
    x_learnunit.set_locator("party_id", carm_text)
    x_learnunit.set_required_arg("party_id", carm_text)
    sue_understandunit.set_learnunit(x_learnunit)

    # WHEN
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    print(f"{sue_understandunit.learnunits=}")
    assert after_sue_agendaunit != before_sue_agendaunit
    assert after_sue_agendaunit.get_party(rico_text) != None
    assert after_sue_agendaunit.get_party(carm_text) is None


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_party():
    # GIVEN
    sue_understandunit = understandunit_shop()
    sue_text = "Sue"

    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_agendaunit.add_partyunit(rico_text)
    assert before_sue_agendaunit.get_party(rico_text) != None
    assert before_sue_agendaunit.get_party(carm_text) is None

    # WHEN
    category = "partyunit"
    x_learnunit = learnunit_shop(category, learn_insert())
    x_learnunit.set_locator("party_id", carm_text)
    x_learnunit.set_required_arg("party_id", carm_text)
    x_creditor_weight = 55
    x_debtor_weight = 66
    x_learnunit.set_optional_arg("creditor_weight", x_creditor_weight)
    x_learnunit.set_optional_arg("debtor_weight", x_debtor_weight)
    sue_understandunit.set_learnunit(x_learnunit)
    print(f"{sue_understandunit.learnunits.keys()=}")
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    rico_partyunit = after_sue_agendaunit.get_party(rico_text)
    carm_partyunit = after_sue_agendaunit.get_party(carm_text)
    assert rico_partyunit != None
    assert carm_partyunit != None
    assert carm_partyunit.creditor_weight == x_creditor_weight
    assert carm_partyunit.debtor_weight == x_debtor_weight


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_party():
    # GIVEN
    sue_understandunit = understandunit_shop()
    sue_text = "Sue"

    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_agendaunit.add_partyunit(rico_text)
    assert before_sue_agendaunit.get_party(rico_text).creditor_weight == 1

    # WHEN
    category = "partyunit"
    x_learnunit = learnunit_shop(category, learn_update())
    x_learnunit.set_locator("party_id", rico_text)
    x_learnunit.set_required_arg("party_id", rico_text)
    rico_creditor_weight = 55
    x_learnunit.set_optional_arg("creditor_weight", rico_creditor_weight)
    sue_understandunit.set_learnunit(x_learnunit)
    print(f"{sue_understandunit.learnunits.keys()=}")
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    rico_party = after_sue_agendaunit.get_party(rico_text)
    assert rico_party.creditor_weight == rico_creditor_weight


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_partylink():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_agendaunit.add_partyunit(rico_text)
    before_sue_agendaunit.add_partyunit(carm_text)
    before_sue_agendaunit.add_partyunit(dizz_text)
    run_text = ",runners"
    run_groupunit = groupunit_shop(run_text)
    run_groupunit.set_partylink(partylink_shop(rico_text))
    run_groupunit.set_partylink(partylink_shop(carm_text))
    fly_text = ",flyers"
    fly_groupunit = groupunit_shop(fly_text)
    fly_groupunit.set_partylink(partylink_shop(rico_text))
    fly_groupunit.set_partylink(partylink_shop(carm_text))
    fly_groupunit.set_partylink(partylink_shop(dizz_text))
    before_sue_agendaunit.set_groupunit(run_groupunit)
    before_sue_agendaunit.set_groupunit(fly_groupunit)
    assert len(before_sue_agendaunit.get_groupunit(run_text)._partys) == 2
    assert len(before_sue_agendaunit.get_groupunit(fly_text)._partys) == 3

    # WHEN
    rico_learnunit = learnunit_shop("partylink", learn_delete())
    rico_learnunit.set_locator("group_id", run_text)
    rico_learnunit.set_locator("party_id", rico_text)
    rico_learnunit.set_required_arg("group_id", run_text)
    rico_learnunit.set_required_arg("party_id", rico_text)
    # print(f"{rico_learnunit=}")
    carm_learnunit = learnunit_shop("partylink", learn_delete())
    carm_learnunit.set_locator("group_id", fly_text)
    carm_learnunit.set_locator("party_id", carm_text)
    carm_learnunit.set_required_arg("group_id", fly_text)
    carm_learnunit.set_required_arg("party_id", carm_text)
    # print(f"{carm_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(rico_learnunit)
    sue_understandunit.set_learnunit(carm_learnunit)
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert len(after_sue_agendaunit.get_groupunit(fly_text)._partys) == 2
    assert len(after_sue_agendaunit.get_groupunit(run_text)._partys) == 1


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_partylink():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_agendaunit.add_partyunit(rico_text)
    before_sue_agendaunit.add_partyunit(carm_text)
    before_sue_agendaunit.add_partyunit(dizz_text)
    run_text = ",runners"
    run_groupunit = groupunit_shop(run_text)
    run_groupunit.set_partylink(partylink_shop(carm_text))
    before_sue_agendaunit.set_groupunit(run_groupunit)
    assert len(before_sue_agendaunit.get_groupunit(run_text)._partys) == 1

    # WHEN
    rico_learnunit = learnunit_shop("partylink", learn_insert())
    rico_learnunit.set_locator("group_id", run_text)
    rico_learnunit.set_locator("party_id", rico_text)
    rico_learnunit.set_required_arg("group_id", run_text)
    rico_learnunit.set_required_arg("party_id", rico_text)
    rico_run_creditor_weight = 17
    rico_learnunit.set_optional_arg("creditor_weight", rico_run_creditor_weight)
    print(f"{rico_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(rico_learnunit)
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert len(after_sue_agendaunit.get_groupunit(run_text)._partys) == 2
    after_run_groupunit = after_sue_agendaunit.get_groupunit(run_text)
    after_run_rico_partylink = after_run_groupunit.get_partylink(rico_text)
    assert after_run_rico_partylink != None
    assert after_run_rico_partylink.creditor_weight == rico_run_creditor_weight


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_partylink():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_agendaunit.add_partyunit(rico_text)
    run_text = ",runners"
    run_groupunit = groupunit_shop(run_text)
    old_rico_run_creditor_weight = 3
    run_groupunit.set_partylink(partylink_shop(rico_text, old_rico_run_creditor_weight))
    before_sue_agendaunit.set_groupunit(run_groupunit)
    before_run_groupunit = before_sue_agendaunit.get_groupunit(run_text)
    before_run_rico_partylink = before_run_groupunit.get_partylink(rico_text)
    assert before_run_rico_partylink.creditor_weight == old_rico_run_creditor_weight
    assert before_run_rico_partylink.debtor_weight == 1

    # WHEN
    rico_learnunit = learnunit_shop("partylink", learn_update())
    rico_learnunit.set_locator("group_id", run_text)
    rico_learnunit.set_locator("party_id", rico_text)
    rico_learnunit.set_required_arg("group_id", run_text)
    rico_learnunit.set_required_arg("party_id", rico_text)
    new_rico_run_creditor_weight = 7
    new_rico_run_debtor_weight = 11
    rico_learnunit.set_optional_arg("creditor_weight", new_rico_run_creditor_weight)
    rico_learnunit.set_optional_arg("debtor_weight", new_rico_run_debtor_weight)
    print(f"{rico_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(rico_learnunit)
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    after_run_groupunit = after_sue_agendaunit.get_groupunit(run_text)
    after_run_rico_partylink = after_run_groupunit.get_partylink(rico_text)
    assert after_run_rico_partylink.creditor_weight == new_rico_run_creditor_weight
    assert after_run_rico_partylink.debtor_weight == new_rico_run_debtor_weight


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_groupunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    run_text = ",runners"
    fly_text = ",flyers"
    before_sue_agendaunit.set_groupunit(groupunit_shop(fly_text))
    before_sue_agendaunit.set_groupunit(groupunit_shop(run_text))
    assert before_sue_agendaunit.get_groupunit(run_text) != None
    assert before_sue_agendaunit.get_groupunit(fly_text) != None

    # WHEN
    x_learnunit = learnunit_shop("groupunit", learn_delete())
    print(f"{x_learnunit=}")
    x_learnunit.set_locator("group_id", run_text)
    x_learnunit.set_required_arg("group_id", run_text)
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(x_learnunit)
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit.get_groupunit(run_text) is None
    assert after_sue_agendaunit.get_groupunit(fly_text) != None


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_groupunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    run_text = ",runners"
    before_sue_agendaunit.set_groupunit(groupunit_shop(run_text))
    fly_text = ",flyers"
    assert before_sue_agendaunit.get_groupunit(run_text) != None
    assert before_sue_agendaunit.get_groupunit(fly_text) is None

    # WHEN
    x_learnunit = learnunit_shop("groupunit", learn_insert())
    x_learnunit.set_locator("group_id", fly_text)
    x_learnunit.set_required_arg("group_id", fly_text)
    x_learnunit.set_optional_arg("_treasury_partylinks", yao_roadunit())
    print(f"{x_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(x_learnunit)
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit.get_groupunit(run_text) != None
    assert after_sue_agendaunit.get_groupunit(fly_text) != None


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_groupunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    run_text = ",runners"
    before_sue_agendaunit.set_groupunit(groupunit_shop(run_text))
    assert before_sue_agendaunit.get_groupunit(run_text)._treasury_partylinks is None

    # WHEN
    x_learnunit = learnunit_shop("groupunit", learn_update())
    x_learnunit.set_locator("group_id", run_text)
    x_learnunit.set_required_arg("group_id", run_text)
    x_learnunit.set_optional_arg("_treasury_partylinks", yao_roadunit())
    print(f"{x_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(x_learnunit)
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert (
        after_sue_agendaunit.get_groupunit(run_text)._treasury_partylinks
        == yao_roadunit()
    )


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_groupunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    run_text = ",runners"
    fly_text = ",flyers"
    before_sue_agendaunit.set_groupunit(groupunit_shop(fly_text))
    before_sue_agendaunit.set_groupunit(groupunit_shop(run_text))
    assert before_sue_agendaunit.get_groupunit(run_text) != None
    assert before_sue_agendaunit.get_groupunit(fly_text) != None

    # WHEN
    x_learnunit = learnunit_shop("groupunit", learn_delete())
    print(f"{x_learnunit=}")
    x_learnunit.set_locator("group_id", run_text)
    x_learnunit.set_required_arg("group_id", run_text)
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(x_learnunit)
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit.get_groupunit(run_text) is None
    assert after_sue_agendaunit.get_groupunit(fly_text) != None


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_ideaunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_agendaunit.make_road(sports_road, disc_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_agendaunit.add_idea(ideaunit_shop(disc_text), sports_road)
    assert before_sue_agendaunit.idea_exists(ball_road)
    assert before_sue_agendaunit.idea_exists(disc_road)

    # WHEN
    delete_disc_learnunit = learnunit_shop("ideaunit", learn_delete())
    delete_disc_learnunit.set_locator("road", disc_road)
    delete_disc_learnunit.set_required_arg("road", disc_road)
    print(f"{delete_disc_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(delete_disc_learnunit)
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit.idea_exists(ball_road)
    assert after_sue_agendaunit.idea_exists(disc_road) == False


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_ideaunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_agendaunit.make_road(sports_road, disc_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    assert before_sue_agendaunit.idea_exists(ball_road)
    assert before_sue_agendaunit.idea_exists(disc_road) == False

    # WHEN
    # x_addin = 140
    # x_begin = 1000
    # x_close = 1700
    # x_denom = 17
    x_meld_strategy = "override"
    x_numeric_road = None
    # x_numor = 10
    x_promise = True
    insert_disc_learnunit = learnunit_shop("ideaunit", learn_insert())
    insert_disc_learnunit.set_locator("road", disc_road)
    insert_disc_learnunit.set_required_arg("label", disc_text)
    insert_disc_learnunit.set_required_arg("parent_road", sports_road)
    # insert_disc_learnunit.set_optional_arg("_addin", x_addin)
    # insert_disc_learnunit.set_optional_arg("_begin", x_begin)
    # insert_disc_learnunit.set_optional_arg("_close", x_close)
    # insert_disc_learnunit.set_optional_arg("_denom", x_denom)
    insert_disc_learnunit.set_optional_arg("_meld_strategy", x_meld_strategy)
    insert_disc_learnunit.set_optional_arg("_numeric_road", x_numeric_road)
    # insert_disc_learnunit.set_optional_arg("_numor", x_numor)
    insert_disc_learnunit.set_optional_arg("promise", x_promise)

    print(f"{insert_disc_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(insert_disc_learnunit)
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit.idea_exists(ball_road)
    assert after_sue_agendaunit.idea_exists(disc_road)


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_ideaunit_SimpleAttributes():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    assert before_sue_agendaunit.get_idea_obj(ball_road)._begin is None
    assert before_sue_agendaunit.get_idea_obj(ball_road)._close is None
    assert before_sue_agendaunit.get_idea_obj(ball_road)._meld_strategy == "default"
    assert before_sue_agendaunit.get_idea_obj(ball_road).promise == False

    # WHEN
    # x_addin = 140
    x_begin = 1000
    x_close = 1700
    # x_denom = 17
    x_meld_strategy = "override"
    # x_numor = 10
    x_promise = True
    insert_disc_learnunit = learnunit_shop("ideaunit", learn_update())
    insert_disc_learnunit.set_locator("road", ball_road)
    insert_disc_learnunit.set_required_arg("road", ball_road)
    # insert_disc_learnunit.set_optional_arg("_addin", x_addin)
    insert_disc_learnunit.set_optional_arg("_begin", x_begin)
    insert_disc_learnunit.set_optional_arg("_close", x_close)
    # insert_disc_learnunit.set_optional_arg("_denom", x_denom)
    insert_disc_learnunit.set_optional_arg("_meld_strategy", x_meld_strategy)
    # insert_disc_learnunit.set_optional_arg("_numor", x_numor)
    insert_disc_learnunit.set_optional_arg("promise", x_promise)

    print(f"{insert_disc_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(insert_disc_learnunit)
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit.get_idea_obj(ball_road)._begin == x_begin
    assert after_sue_agendaunit.get_idea_obj(ball_road)._close == x_close
    assert (
        after_sue_agendaunit.get_idea_obj(ball_road)._meld_strategy == x_meld_strategy
    )
    assert after_sue_agendaunit.get_idea_obj(ball_road).promise


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_idea_balancelink():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_au.add_partyunit(rico_text)
    before_sue_au.add_partyunit(carm_text)
    before_sue_au.add_partyunit(dizz_text)
    run_text = ",runners"
    run_groupunit = groupunit_shop(run_text)
    run_groupunit.set_partylink(partylink_shop(rico_text))
    run_groupunit.set_partylink(partylink_shop(carm_text))
    fly_text = ",flyers"
    fly_groupunit = groupunit_shop(fly_text)
    fly_groupunit.set_partylink(partylink_shop(rico_text))
    fly_groupunit.set_partylink(partylink_shop(carm_text))
    fly_groupunit.set_partylink(partylink_shop(dizz_text))
    before_sue_au.set_groupunit(run_groupunit)
    before_sue_au.set_groupunit(fly_groupunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_au.make_road(sports_road, disc_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_au.add_idea(ideaunit_shop(disc_text), sports_road)
    before_sue_au.edit_idea_attr(ball_road, balancelink=balancelink_shop(run_text))
    before_sue_au.edit_idea_attr(ball_road, balancelink=balancelink_shop(fly_text))
    before_sue_au.edit_idea_attr(disc_road, balancelink=balancelink_shop(run_text))
    before_sue_au.edit_idea_attr(disc_road, balancelink=balancelink_shop(fly_text))
    assert len(before_sue_au.get_idea_obj(ball_road)._balancelinks) == 2
    assert len(before_sue_au.get_idea_obj(disc_road)._balancelinks) == 2

    # WHEN
    delete_disc_learnunit = learnunit_shop("idea_balancelink", learn_delete())
    delete_disc_learnunit.set_locator("road", disc_road)
    delete_disc_learnunit.set_locator("group_id", fly_text)
    delete_disc_learnunit.set_required_arg("road", disc_road)
    delete_disc_learnunit.set_required_arg("group_id", fly_text)
    print(f"{delete_disc_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(delete_disc_learnunit)
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    assert len(after_sue_agendaunit.get_idea_obj(ball_road)._balancelinks) == 2
    assert len(after_sue_agendaunit.get_idea_obj(disc_road)._balancelinks) == 1


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_idea_balancelink():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_au.add_partyunit(rico_text)
    before_sue_au.add_partyunit(carm_text)
    run_text = ",runners"
    run_groupunit = groupunit_shop(run_text)
    run_groupunit.set_partylink(partylink_shop(rico_text))
    before_sue_au.set_groupunit(run_groupunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_au.edit_idea_attr(ball_road, balancelink=balancelink_shop(run_text))
    run_balancelink = before_sue_au.get_idea_obj(ball_road)._balancelinks.get(run_text)
    assert run_balancelink.creditor_weight == 1
    assert run_balancelink.debtor_weight == 1

    # WHEN
    x_creditor_weight = 55
    x_debtor_weight = 66
    update_disc_learnunit = learnunit_shop("idea_balancelink", learn_update())
    update_disc_learnunit.set_locator("road", ball_road)
    update_disc_learnunit.set_locator("group_id", run_text)
    update_disc_learnunit.set_required_arg("road", ball_road)
    update_disc_learnunit.set_required_arg("group_id", run_text)
    update_disc_learnunit.set_optional_arg("creditor_weight", x_creditor_weight)
    update_disc_learnunit.set_optional_arg("debtor_weight", x_debtor_weight)
    # print(f"{update_disc_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(update_disc_learnunit)
    after_sue_au = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    run_balancelink = after_sue_au.get_idea_obj(ball_road)._balancelinks.get(run_text)
    print(f"{run_balancelink.creditor_weight=}")
    assert run_balancelink.creditor_weight == x_creditor_weight
    assert run_balancelink.debtor_weight == x_debtor_weight


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_idea_balancelink():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_au.add_partyunit(rico_text)
    before_sue_au.add_partyunit(carm_text)
    run_text = ",runners"
    run_groupunit = groupunit_shop(run_text)
    run_groupunit.set_partylink(partylink_shop(rico_text))
    before_sue_au.set_groupunit(run_groupunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea._balancelinks.get(run_text) is None

    # WHEN
    x_creditor_weight = 55
    x_debtor_weight = 66
    update_disc_learnunit = learnunit_shop("idea_balancelink", learn_insert())
    update_disc_learnunit.set_locator("road", ball_road)
    update_disc_learnunit.set_locator("group_id", run_text)
    update_disc_learnunit.set_required_arg("road", ball_road)
    update_disc_learnunit.set_required_arg("group_id", run_text)
    update_disc_learnunit.set_optional_arg("creditor_weight", x_creditor_weight)
    update_disc_learnunit.set_optional_arg("debtor_weight", x_debtor_weight)
    # print(f"{update_disc_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(update_disc_learnunit)
    after_sue_au = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._balancelinks.get(run_text) != None


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_idea_beliefunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea._beliefunits == {}

    # WHEN
    broken_open = 55
    broken_nigh = 66
    update_disc_learnunit = learnunit_shop("idea_beliefunit", learn_insert())
    update_disc_learnunit.set_locator("road", ball_road)
    update_disc_learnunit.set_locator("base", knee_road)
    update_disc_learnunit.set_required_arg("road", ball_road)
    update_disc_learnunit.set_required_arg("base", knee_road)
    update_disc_learnunit.set_optional_arg("pick", broken_road)
    update_disc_learnunit.set_optional_arg("open", broken_open)
    update_disc_learnunit.set_optional_arg("nigh", broken_nigh)
    # print(f"{update_disc_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(update_disc_learnunit)
    after_sue_au = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._beliefunits != {}
    assert after_ball_idea._beliefunits.get(knee_road) != None
    assert after_ball_idea._beliefunits.get(knee_road).base == knee_road
    assert after_ball_idea._beliefunits.get(knee_road).pick == broken_road
    assert after_ball_idea._beliefunits.get(knee_road).open == broken_open
    assert after_ball_idea._beliefunits.get(knee_road).nigh == broken_nigh


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_idea_beliefunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
    before_sue_au.edit_idea_attr(
        road=ball_road, beliefunit=beliefunit_shop(base=knee_road, pick=broken_road)
    )
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea._beliefunits != {}
    assert before_ball_idea._beliefunits.get(knee_road) != None

    # WHEN
    update_disc_learnunit = learnunit_shop("idea_beliefunit", learn_delete())
    update_disc_learnunit.set_locator("road", ball_road)
    update_disc_learnunit.set_locator("base", knee_road)
    update_disc_learnunit.set_required_arg("road", ball_road)
    update_disc_learnunit.set_required_arg("base", knee_road)
    # print(f"{update_disc_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(update_disc_learnunit)
    after_sue_au = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._beliefunits == {}


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_idea_beliefunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_text)
    medical_text = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
    before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
    before_knee_beliefunit = beliefunit_shop(knee_road, broken_road)
    before_sue_au.edit_idea_attr(ball_road, beliefunit=before_knee_beliefunit)
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea._beliefunits != {}
    assert before_ball_idea._beliefunits.get(knee_road) != None
    assert before_ball_idea._beliefunits.get(knee_road).pick == broken_road
    assert before_ball_idea._beliefunits.get(knee_road).open is None
    assert before_ball_idea._beliefunits.get(knee_road).nigh is None

    # WHEN
    medical_open = 45
    medical_nigh = 77
    update_disc_learnunit = learnunit_shop("idea_beliefunit", learn_update())
    update_disc_learnunit.set_locator("road", ball_road)
    update_disc_learnunit.set_locator("base", knee_road)
    update_disc_learnunit.set_required_arg("road", ball_road)
    update_disc_learnunit.set_required_arg("base", knee_road)
    update_disc_learnunit.set_optional_arg("pick", medical_road)
    update_disc_learnunit.set_optional_arg("open", medical_open)
    update_disc_learnunit.set_optional_arg("nigh", medical_nigh)
    # print(f"{update_disc_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(update_disc_learnunit)
    after_sue_au = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._beliefunits != {}
    assert after_ball_idea._beliefunits.get(knee_road) != None
    assert after_ball_idea._beliefunits.get(knee_road).pick == medical_road
    assert after_ball_idea._beliefunits.get(knee_road).open == medical_open
    assert after_ball_idea._beliefunits.get(knee_road).nigh == medical_nigh


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_idea_reason_premiseunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
    before_sue_au.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=broken_road
    )
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea._reasonunits != {}
    before_knee_reasonunit = before_ball_idea.get_reasonunit(knee_road)
    assert before_knee_reasonunit != None
    broken_premiseunit = before_knee_reasonunit.get_premise(broken_road)
    assert broken_premiseunit.need == broken_road
    assert broken_premiseunit.open is None
    assert broken_premiseunit.nigh is None
    assert broken_premiseunit.divisor is None

    # WHEN
    broken_open = 45
    broken_nigh = 77
    broken_divisor = 3
    update_disc_learnunit = learnunit_shop("idea_reason_premiseunit", learn_update())
    update_disc_learnunit.set_locator("road", ball_road)
    update_disc_learnunit.set_locator("base", knee_road)
    update_disc_learnunit.set_locator("need", broken_road)
    update_disc_learnunit.set_required_arg("road", ball_road)
    update_disc_learnunit.set_required_arg("base", knee_road)
    update_disc_learnunit.set_required_arg("need", broken_road)
    update_disc_learnunit.set_optional_arg("open", broken_open)
    update_disc_learnunit.set_optional_arg("nigh", broken_nigh)
    update_disc_learnunit.set_optional_arg("divisor", broken_divisor)
    # print(f"{update_disc_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(update_disc_learnunit)
    after_sue_au = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit != None
    after_broken_premiseunit = after_knee_reasonunit.get_premise(broken_road)
    assert after_broken_premiseunit.need == broken_road
    assert after_broken_premiseunit.open == broken_open
    assert after_broken_premiseunit.nigh == broken_nigh
    assert after_broken_premiseunit.divisor == broken_divisor


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_idea_reason_premiseunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_text)
    medical_text = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
    before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
    before_sue_au.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=broken_road
    )
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    before_knee_reasonunit = before_ball_idea.get_reasonunit(knee_road)
    assert before_knee_reasonunit.get_premise(broken_road) != None
    assert before_knee_reasonunit.get_premise(medical_road) is None

    # WHEN
    medical_open = 45
    medical_nigh = 77
    medical_divisor = 3
    update_disc_learnunit = learnunit_shop("idea_reason_premiseunit", learn_insert())
    update_disc_learnunit.set_locator("road", ball_road)
    update_disc_learnunit.set_locator("base", knee_road)
    update_disc_learnunit.set_locator("need", medical_road)
    update_disc_learnunit.set_required_arg("road", ball_road)
    update_disc_learnunit.set_required_arg("base", knee_road)
    update_disc_learnunit.set_required_arg("need", medical_road)
    update_disc_learnunit.set_optional_arg("open", medical_open)
    update_disc_learnunit.set_optional_arg("nigh", medical_nigh)
    update_disc_learnunit.set_optional_arg("divisor", medical_divisor)
    # print(f"{update_disc_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(update_disc_learnunit)
    after_sue_au = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    after_medical_premiseunit = after_knee_reasonunit.get_premise(medical_road)
    assert after_medical_premiseunit != None
    assert after_medical_premiseunit.need == medical_road
    assert after_medical_premiseunit.open == medical_open
    assert after_medical_premiseunit.nigh == medical_nigh
    assert after_medical_premiseunit.divisor == medical_divisor


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_idea_reason_premiseunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_au.make_road(knee_road, broken_text)
    medical_text = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
    before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
    before_sue_au.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=broken_road
    )
    before_sue_au.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=medical_road
    )
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    before_knee_reasonunit = before_ball_idea.get_reasonunit(knee_road)
    assert before_knee_reasonunit.get_premise(broken_road) != None
    assert before_knee_reasonunit.get_premise(medical_road) != None

    # WHEN
    update_disc_learnunit = learnunit_shop("idea_reason_premiseunit", learn_delete())
    update_disc_learnunit.set_locator("road", ball_road)
    update_disc_learnunit.set_locator("base", knee_road)
    update_disc_learnunit.set_locator("need", medical_road)
    update_disc_learnunit.set_required_arg("road", ball_road)
    update_disc_learnunit.set_required_arg("base", knee_road)
    update_disc_learnunit.set_required_arg("need", medical_road)
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(update_disc_learnunit)
    after_sue_au = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit.get_premise(broken_road) != None
    assert after_knee_reasonunit.get_premise(medical_road) is None


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_idea_reasonunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_text)
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea.get_reasonunit(knee_road) is None

    # WHEN
    medical_suff_idea_active = True
    update_disc_learnunit = learnunit_shop("idea_reasonunit", learn_insert())
    update_disc_learnunit.set_locator("road", ball_road)
    update_disc_learnunit.set_locator("base", knee_road)
    update_disc_learnunit.set_required_arg("road", ball_road)
    update_disc_learnunit.set_required_arg("base", knee_road)
    update_disc_learnunit.set_optional_arg("suff_idea_active", medical_suff_idea_active)
    # print(f"{update_disc_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(update_disc_learnunit)
    after_sue_au = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit != None
    assert after_knee_reasonunit.get_premise(medical_road) is None
    assert after_knee_reasonunit.suff_idea_active == medical_suff_idea_active


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_idea_reasonunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_au.make_road(knee_road, medical_text)
    before_medical_suff_idea_active = False
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
    before_sue_au.edit_idea_attr(
        road=ball_road,
        reason_base=knee_road,
        reason_suff_idea_active=before_medical_suff_idea_active,
    )
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    before_ball_reasonunit = before_ball_idea.get_reasonunit(knee_road)
    assert before_ball_reasonunit != None
    assert before_ball_reasonunit.suff_idea_active == before_medical_suff_idea_active

    # WHEN
    after_medical_suff_idea_active = True
    update_disc_learnunit = learnunit_shop("idea_reasonunit", learn_update())
    update_disc_learnunit.set_locator("road", ball_road)
    update_disc_learnunit.set_locator("base", knee_road)
    update_disc_learnunit.set_required_arg("road", ball_road)
    update_disc_learnunit.set_required_arg("base", knee_road)
    update_disc_learnunit.set_optional_arg(
        "suff_idea_active", after_medical_suff_idea_active
    )
    # print(f"{update_disc_learnunit=}")
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(update_disc_learnunit)
    after_sue_au = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit != None
    assert after_knee_reasonunit.get_premise(medical_road) is None
    assert after_knee_reasonunit.suff_idea_active == after_medical_suff_idea_active


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_idea_reasonunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_au.make_l1_road(knee_text)
    medical_suff_idea_active = False
    before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_au.edit_idea_attr(
        road=ball_road,
        reason_base=knee_road,
        reason_suff_idea_active=medical_suff_idea_active,
    )
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea.get_reasonunit(knee_road) != None

    # WHEN
    update_disc_learnunit = learnunit_shop("idea_reasonunit", learn_delete())
    update_disc_learnunit.set_locator("road", ball_road)
    update_disc_learnunit.set_locator("base", knee_road)
    update_disc_learnunit.set_required_arg("road", ball_road)
    update_disc_learnunit.set_required_arg("base", knee_road)
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(update_disc_learnunit)
    after_sue_au = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea.get_reasonunit(knee_road) is None


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_idea_suffgroup():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_au.add_partyunit(rico_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_ideaunit = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_ideaunit._assignedunit._suffgroups == {}

    # WHEN
    update_disc_learnunit = learnunit_shop("idea_suffgroup", learn_insert())
    update_disc_learnunit.set_locator("road", ball_road)
    update_disc_learnunit.set_locator("group_id", rico_text)
    update_disc_learnunit.set_required_arg("road", ball_road)
    update_disc_learnunit.set_required_arg("group_id", rico_text)
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(update_disc_learnunit)
    after_sue_au = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    after_ball_ideaunit = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_ideaunit._assignedunit._suffgroups != {}
    assert after_ball_ideaunit._assignedunit.get_suffgroup(rico_text) != None


def test_UnderstandUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_idea_suffgroup():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_au.add_partyunit(rico_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_ideaunit = before_sue_au.get_idea_obj(ball_road)
    before_ball_ideaunit._assignedunit.set_suffgroup(rico_text)
    assert before_ball_ideaunit._assignedunit._suffgroups != {}
    assert before_ball_ideaunit._assignedunit.get_suffgroup(rico_text) != None

    # WHEN
    update_disc_learnunit = learnunit_shop("idea_suffgroup", learn_delete())
    update_disc_learnunit.set_locator("road", ball_road)
    update_disc_learnunit.set_locator("group_id", rico_text)
    update_disc_learnunit.set_required_arg("road", ball_road)
    update_disc_learnunit.set_required_arg("group_id", rico_text)
    sue_understandunit = understandunit_shop()
    sue_understandunit.set_learnunit(update_disc_learnunit)
    print(f"{before_sue_au.get_idea_obj(ball_road)._assignedunit=}")
    after_sue_au = sue_understandunit.get_after_agenda(before_sue_au)

    # THEN
    after_ball_ideaunit = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_ideaunit._assignedunit._suffgroups == {}


def test_UnderstandUnit_get_sue_understandunit_example1_ContainsLearnUnits():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_agendaunit.add_partyunit(rico_text)
    before_sue_agendaunit.add_partyunit(carm_text)
    before_sue_agendaunit.add_partyunit(dizz_text)
    run_text = ",runners"
    run_groupunit = groupunit_shop(run_text)
    run_groupunit.set_partylink(partylink_shop(rico_text))
    run_groupunit.set_partylink(partylink_shop(carm_text))
    fly_text = ",flyers"
    fly_groupunit = groupunit_shop(fly_text)
    fly_groupunit.set_partylink(partylink_shop(rico_text))
    fly_groupunit.set_partylink(partylink_shop(dizz_text))
    before_sue_agendaunit.set_groupunit(run_groupunit)
    before_sue_agendaunit.set_groupunit(fly_groupunit)
    assert before_sue_agendaunit._weight != 55
    assert before_sue_agendaunit._max_tree_traverse != 66
    assert before_sue_agendaunit._party_creditor_pool != 77
    assert before_sue_agendaunit._party_debtor_pool != 88
    assert before_sue_agendaunit._meld_strategy != "override"
    assert before_sue_agendaunit.get_party(rico_text) != None
    assert before_sue_agendaunit.get_party(carm_text) != None
    assert before_sue_agendaunit.get_groupunit(run_text) != None
    assert before_sue_agendaunit.get_groupunit(fly_text) != None

    # WHEN
    sue_understandunit = get_sue_understandunit_example1()
    after_sue_agendaunit = sue_understandunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit._weight == 55
    assert after_sue_agendaunit._max_tree_traverse == 66
    assert after_sue_agendaunit._party_creditor_pool == 77
    assert after_sue_agendaunit._party_debtor_pool == 88
    assert after_sue_agendaunit._meld_strategy == "override"
    assert after_sue_agendaunit.get_party(rico_text) != None
    assert after_sue_agendaunit.get_party(carm_text) is None
