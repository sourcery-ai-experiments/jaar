from src._prime.road import get_single_roadnode
from src._prime.meld import get_meld_default
from src.agenda.party import partylink_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.group import groupunit_shop
from src.agenda.agenda import agendaunit_shop
from src.world.move import (
    MoveUnit,
    moveunit_shop,
    stir_update,
    stir_delete,
    stir_insert,
    stirunit_shop,
)
from src.world.examples.example_deals import (
    get_sue_personroad,
    get_sue_moveunit_example1,
)


def test_MoveUnit_get_after_agenda_ReturnsCorrectObj_SimplestScenario():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)

    # WHEN
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
    sue_weight = 55
    before_sue_agendaunit = agendaunit_shop(sue_text, _weight=sue_weight)
    after_sue_agendaunit = sue_moveunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit._weight == sue_weight
    assert after_sue_agendaunit == before_sue_agendaunit


def test_MoveUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnitSimpleAttrs():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")

    sue_weight = 44
    before_sue_agendaunit = agendaunit_shop(sue_text, _weight=sue_weight)

    new1_value = 55
    category = "AgendaUnit_weight"
    x_stirunit = stirunit_shop(category, stir_update())
    x_stirunit.set_required_arg(category, new1_value)
    sue_moveunit.set_stirunit(x_stirunit)

    new2_value = 66
    category = "_max_tree_traverse"
    x_stirunit = stirunit_shop(category, stir_update())
    x_stirunit.set_required_arg(category, new2_value)
    sue_moveunit.set_stirunit(x_stirunit)

    new3_value = 77
    category = "_party_creditor_pool"
    x_stirunit = stirunit_shop(category, stir_update())
    x_stirunit.set_required_arg(category, new3_value)
    sue_moveunit.set_stirunit(x_stirunit)

    new4_value = 88
    category = "_party_debtor_pool"
    x_stirunit = stirunit_shop(category, stir_update())
    x_stirunit.set_required_arg(category, new4_value)
    sue_moveunit.set_stirunit(x_stirunit)

    new5_value = "override"
    category = "_meld_strategy"
    x_stirunit = stirunit_shop(category, stir_update())
    x_stirunit.set_required_arg(category, new5_value)
    sue_moveunit.set_stirunit(x_stirunit)

    # WHEN
    after_sue_agendaunit = sue_moveunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    print(f"{sue_moveunit.update_stirs=}")
    assert after_sue_agendaunit._weight == new1_value
    assert after_sue_agendaunit._weight != before_sue_agendaunit._weight
    assert after_sue_agendaunit._max_tree_traverse == new2_value
    assert after_sue_agendaunit._party_creditor_pool == new3_value
    assert after_sue_agendaunit._party_debtor_pool == new4_value
    assert after_sue_agendaunit._meld_strategy == new5_value


def test_MoveUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_party():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")

    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_agendaunit.add_partyunit(rico_text)
    before_sue_agendaunit.add_partyunit(carm_text)

    category = "partyunit"
    x_stirunit = stirunit_shop(category, stir_delete())
    x_stirunit.set_locator("party_id", carm_text)
    sue_moveunit.set_stirunit(x_stirunit)

    # WHEN
    after_sue_agendaunit = sue_moveunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    print(f"{sue_moveunit.update_stirs=}")
    assert after_sue_agendaunit != before_sue_agendaunit
    assert after_sue_agendaunit.get_party(rico_text) != None
    assert after_sue_agendaunit.get_party(carm_text) is None


def test_MoveUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_groupunit_partylink():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
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
    rico_stirunit = stirunit_shop("groupunit_partylink", stir_delete())
    rico_stirunit.set_locator("group_id", run_text)
    rico_stirunit.set_locator("party_id", rico_text)
    rico_stirunit.set_required_arg("group_id", run_text)
    rico_stirunit.set_required_arg("party_id", rico_text)
    # print(f"{rico_stirunit=}")
    carm_stirunit = stirunit_shop("groupunit_partylink", stir_delete())
    carm_stirunit.set_locator("group_id", fly_text)
    carm_stirunit.set_locator("party_id", carm_text)
    carm_stirunit.set_required_arg("group_id", fly_text)
    carm_stirunit.set_required_arg("party_id", carm_text)
    # print(f"{carm_stirunit=}")
    sue_moveunit = moveunit_shop(sue_road)
    sue_moveunit.set_stirunit(rico_stirunit)
    sue_moveunit.set_stirunit(carm_stirunit)
    after_sue_agendaunit = sue_moveunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert len(after_sue_agendaunit.get_groupunit(fly_text)._partys) == 2
    assert len(after_sue_agendaunit.get_groupunit(run_text)._partys) == 1


def test_MoveUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_groupunit():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
    before_sue_agendaunit = agendaunit_shop(sue_text)
    run_text = ",runners"
    fly_text = ",flyers"
    before_sue_agendaunit.set_groupunit(groupunit_shop(fly_text))
    before_sue_agendaunit.set_groupunit(groupunit_shop(run_text))
    assert before_sue_agendaunit.get_groupunit(run_text) != None
    assert before_sue_agendaunit.get_groupunit(fly_text) != None

    # WHEN
    x_stirunit = stirunit_shop("groupunit", stir_delete())
    print(f"{x_stirunit=}")
    x_stirunit.set_locator("group_id", run_text)
    x_stirunit.set_required_arg("group_id", run_text)
    sue_moveunit = moveunit_shop(sue_road)
    sue_moveunit.set_stirunit(x_stirunit)
    after_sue_agendaunit = sue_moveunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit.get_groupunit(run_text) is None
    assert after_sue_agendaunit.get_groupunit(fly_text) != None


def test_MoveUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_ideaunit():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
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
    delete_disc_stirunit = stirunit_shop("idea", stir_delete())
    delete_disc_stirunit.set_locator("road", disc_road)
    delete_disc_stirunit.set_required_arg("road", disc_road)
    print(f"{delete_disc_stirunit=}")
    sue_moveunit = moveunit_shop(sue_road)
    sue_moveunit.set_stirunit(delete_disc_stirunit)
    after_sue_agendaunit = sue_moveunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit.idea_exists(ball_road)
    assert after_sue_agendaunit.idea_exists(disc_road) == False


def test_MoveUnit_get_sue_moveunit_example1_ContainsStirUnits():
    # GIVEN
    sue_text = get_single_roadnode("PersonRoad", get_sue_personroad(), "PersonID")
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
    sue_moveunit = get_sue_moveunit_example1()
    after_sue_agendaunit = sue_moveunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit._weight == 55
    assert after_sue_agendaunit._max_tree_traverse == 66
    assert after_sue_agendaunit._party_creditor_pool == 77
    assert after_sue_agendaunit._party_debtor_pool == 88
    assert after_sue_agendaunit._meld_strategy == "override"
    assert after_sue_agendaunit.get_party(rico_text) != None
    assert after_sue_agendaunit.get_party(carm_text) is None
