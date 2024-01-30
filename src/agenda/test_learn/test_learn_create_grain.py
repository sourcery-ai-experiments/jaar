from src._prime.road import get_single_roadnode
from src._prime.meld import get_meld_default
from src.agenda.group import balancelink_shop
from src.agenda.party import partylink_shop
from src.agenda.reason_idea import beliefunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.group import groupunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.learn import (
    create_learnunit,
    grain_insert,
    grain_update,
    grain_delete,
    learnunit_shop,
    grainunit_shop,
)
from src.agenda.examples.example_learns import (
    get_sue_personroad,
    get_sue_learnunit_example1,
    get_yao_example_roadunit as yao_roadunit,
)
from src.agenda.examples.example_agendas import get_agenda_with_4_levels
from src.tools.python import get_nested_value
from copy import deepcopy as copy_deepcopy


def test_create_learnunit_ReturnsCorrectObj_EmptyLearnUnit():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_agenda = get_agenda_with_4_levels()

    # WHEN
    sue_learnunit = create_learnunit(sue_agenda, sue_agenda, sue_road)

    # THEN
    assert sue_learnunit.grainunits == {}
    assert sue_learnunit.agenda_road == sue_road


def test_create_learnunit_ReturnsCorrectObjWith_GrainUnit_partyunit_insert():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
    before_sue_agenda = agendaunit_shop(sue_text)
    after_sue_agenda = copy_deepcopy(before_sue_agenda)
    rico_text = "Rico"
    rico_creditor_weight = 33
    rico_debtor_weight = 44
    rico_depotlink_type = "assignment"
    after_sue_agenda.add_partyunit(
        rico_text,
        creditor_weight=rico_creditor_weight,
        debtor_weight=rico_debtor_weight,
        depotlink_type=rico_depotlink_type,
    )

    # WHEN
    sue_learnunit = create_learnunit(before_sue_agenda, after_sue_agenda, sue_road)

    # THEN
    assert len(sue_learnunit.grainunits.get(grain_insert())) == 1
    sue_insert_dict = sue_learnunit.grainunits.get(grain_insert())
    sue_partyunit_dict = sue_insert_dict.get("partyunit")
    rico_grainunit = sue_partyunit_dict.get(rico_text)
    assert rico_grainunit.get_value("party_id") == rico_text
    assert rico_grainunit.get_value("creditor_weight") == rico_creditor_weight
    assert rico_grainunit.get_value("debtor_weight") == rico_debtor_weight
    assert rico_grainunit.get_value("depotlink_type") == rico_depotlink_type


def test_create_learnunit_ReturnsCorrectObjWith_GrainUnit_partyunit_delete():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
    before_sue_agenda = agendaunit_shop(sue_text)
    after_sue_agenda = copy_deepcopy(before_sue_agenda)

    rico_text = "Rico"
    before_sue_agenda.add_partyunit(rico_text)

    # WHEN
    sue_learnunit = create_learnunit(before_sue_agenda, after_sue_agenda, sue_road)

    # THEN
    rico_grainunit = get_nested_value(
        sue_learnunit.grainunits, [grain_delete(), "partyunit", rico_text]
    )
    assert rico_grainunit.get_value("party_id") == rico_text


def test_create_learnunit_ReturnsCorrectObjWith_GrainUnit_partyunit_update():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
    before_sue_agenda = agendaunit_shop(sue_text)
    after_sue_agenda = copy_deepcopy(before_sue_agenda)
    rico_text = "Rico"
    before_sue_agenda.add_partyunit(rico_text)
    rico_creditor_weight = 33
    rico_debtor_weight = 44
    rico_depotlink_type = "assignment"
    after_sue_agenda.add_partyunit(
        rico_text,
        creditor_weight=rico_creditor_weight,
        debtor_weight=rico_debtor_weight,
        depotlink_type=rico_depotlink_type,
    )

    # WHEN
    sue_learnunit = create_learnunit(before_sue_agenda, after_sue_agenda, sue_road)

    # THEN
    x_keylist = [grain_update(), "partyunit", rico_text]
    rico_grainunit = get_nested_value(sue_learnunit.grainunits, x_keylist)
    assert rico_grainunit.get_value("party_id") == rico_text
    assert rico_grainunit.get_value("creditor_weight") == rico_creditor_weight
    assert rico_grainunit.get_value("debtor_weight") == rico_debtor_weight
    assert rico_grainunit.get_value("depotlink_type") == rico_depotlink_type


def test_create_learnunit_ReturnsCorrectObjWith_GrainUnit_AgendaUnit_weight_update():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
    before_sue_agenda = agendaunit_shop(sue_text)
    after_sue_agenda = copy_deepcopy(before_sue_agenda)
    x_agendaUnit_weight = 55
    x_max_tree_traverse = 66
    x_party_creditor_pool = 77
    x_party_debtor_pool = 88
    x_auto_output_to_forum = True
    x_meld_strategy = "override"
    after_sue_agenda._weight = x_agendaUnit_weight
    after_sue_agenda.set_max_tree_traverse(x_max_tree_traverse)
    after_sue_agenda.set_party_creditor_pool(x_party_creditor_pool)
    after_sue_agenda.set_party_debtor_pool(x_party_debtor_pool)
    after_sue_agenda._set_auto_output_to_forum(x_auto_output_to_forum)
    after_sue_agenda.set_meld_strategy(x_meld_strategy)

    # WHEN
    sue_learnunit = create_learnunit(before_sue_agenda, after_sue_agenda, sue_road)

    # THEN
    sue_grainunits = sue_learnunit.grainunits
    x_keylist = [grain_update(), "AgendaUnit_weight"]
    rico_grainunit = get_nested_value(sue_grainunits, x_keylist)
    assert rico_grainunit.get_value("AgendaUnit_weight") == x_agendaUnit_weight

    x_keylist = [grain_update(), "_max_tree_traverse"]
    rico_grainunit = get_nested_value(sue_learnunit.grainunits, x_keylist)
    assert rico_grainunit.get_value("_max_tree_traverse") == x_max_tree_traverse

    x_keylist = [grain_update(), "_party_creditor_pool"]
    rico_grainunit = get_nested_value(sue_learnunit.grainunits, x_keylist)
    assert rico_grainunit.get_value("_party_creditor_pool") == x_party_creditor_pool

    x_keylist = [grain_update(), "_party_debtor_pool"]
    rico_grainunit = get_nested_value(sue_learnunit.grainunits, x_keylist)
    assert rico_grainunit.get_value("_party_debtor_pool") == x_party_debtor_pool

    x_keylist = [grain_update(), "_auto_output_to_forum"]
    rico_grainunit = get_nested_value(sue_learnunit.grainunits, x_keylist)
    assert rico_grainunit.get_value("_auto_output_to_forum") == x_auto_output_to_forum

    x_keylist = [grain_update(), "_meld_strategy"]
    rico_grainunit = get_nested_value(sue_learnunit.grainunits, x_keylist)
    assert rico_grainunit.get_value("_meld_strategy") == x_meld_strategy


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_groupunit_partylink():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_agendaunit = agendaunit_shop(sue_text)
#     rico_text = "Rico"
#     carm_text = "Carmen"
#     dizz_text = "Dizzy"
#     before_sue_agendaunit.add_partyunit(rico_text)
#     before_sue_agendaunit.add_partyunit(carm_text)
#     before_sue_agendaunit.add_partyunit(dizz_text)
#     run_text = ",runners"
#     run_groupunit = groupunit_shop(run_text)
#     run_groupunit.set_partylink(partylink_shop(rico_text))
#     run_groupunit.set_partylink(partylink_shop(carm_text))
#     fly_text = ",flyers"
#     fly_groupunit = groupunit_shop(fly_text)
#     fly_groupunit.set_partylink(partylink_shop(rico_text))
#     fly_groupunit.set_partylink(partylink_shop(carm_text))
#     fly_groupunit.set_partylink(partylink_shop(dizz_text))
#     before_sue_agendaunit.set_groupunit(run_groupunit)
#     before_sue_agendaunit.set_groupunit(fly_groupunit)
#     assert len(before_sue_agendaunit.get_groupunit(run_text)._partys) == 2
#     assert len(before_sue_agendaunit.get_groupunit(fly_text)._partys) == 3

#     # WHEN
#     rico_grainunit = grainunit_shop("groupunit_partylink", grain_delete())
#     rico_grainunit.set_locator("group_id", run_text)
#     rico_grainunit.set_locator("party_id", rico_text)
#     rico_grainunit.set_required_arg("group_id", run_text)
#     rico_grainunit.set_required_arg("party_id", rico_text)
#     # print(f"{rico_grainunit=}")
#     carm_grainunit = grainunit_shop("groupunit_partylink", grain_delete())
#     carm_grainunit.set_locator("group_id", fly_text)
#     carm_grainunit.set_locator("party_id", carm_text)
#     carm_grainunit.set_required_arg("group_id", fly_text)
#     carm_grainunit.set_required_arg("party_id", carm_text)
#     # print(f"{carm_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(rico_grainunit)
#     sue_learnunit.set_grainunit(carm_grainunit)
#     after_sue_agendaunit = sue_learnunit.get_after_agenda(before_sue_agendaunit)

#     # THEN
#     assert len(after_sue_agendaunit.get_groupunit(fly_text)._partys) == 2
#     assert len(after_sue_agendaunit.get_groupunit(run_text)._partys) == 1


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_groupunit_partylink():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_agendaunit = agendaunit_shop(sue_text)
#     rico_text = "Rico"
#     carm_text = "Carmen"
#     dizz_text = "Dizzy"
#     before_sue_agendaunit.add_partyunit(rico_text)
#     before_sue_agendaunit.add_partyunit(carm_text)
#     before_sue_agendaunit.add_partyunit(dizz_text)
#     run_text = ",runners"
#     run_groupunit = groupunit_shop(run_text)
#     run_groupunit.set_partylink(partylink_shop(carm_text))
#     before_sue_agendaunit.set_groupunit(run_groupunit)
#     assert len(before_sue_agendaunit.get_groupunit(run_text)._partys) == 1

#     # WHEN
#     rico_grainunit = grainunit_shop("groupunit_partylink", grain_insert())
#     rico_grainunit.set_locator("group_id", run_text)
#     rico_grainunit.set_locator("party_id", rico_text)
#     rico_grainunit.set_required_arg("group_id", run_text)
#     rico_grainunit.set_required_arg("party_id", rico_text)
#     rico_run_creditor_weight = 17
#     rico_grainunit.set_optional_arg("creditor_weight", rico_run_creditor_weight)
#     print(f"{rico_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(rico_grainunit)
#     after_sue_agendaunit = sue_learnunit.get_after_agenda(before_sue_agendaunit)

#     # THEN
#     assert len(after_sue_agendaunit.get_groupunit(run_text)._partys) == 2
#     after_run_groupunit = after_sue_agendaunit.get_groupunit(run_text)
#     after_run_rico_partylink = after_run_groupunit.get_partylink(rico_text)
#     assert after_run_rico_partylink != None
#     assert after_run_rico_partylink.creditor_weight == rico_run_creditor_weight


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_groupunit_partylink():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_agendaunit = agendaunit_shop(sue_text)
#     rico_text = "Rico"
#     before_sue_agendaunit.add_partyunit(rico_text)
#     run_text = ",runners"
#     run_groupunit = groupunit_shop(run_text)
#     old_rico_run_creditor_weight = 3
#     run_groupunit.set_partylink(partylink_shop(rico_text, old_rico_run_creditor_weight))
#     before_sue_agendaunit.set_groupunit(run_groupunit)
#     before_run_groupunit = before_sue_agendaunit.get_groupunit(run_text)
#     before_run_rico_partylink = before_run_groupunit.get_partylink(rico_text)
#     assert before_run_rico_partylink.creditor_weight == old_rico_run_creditor_weight
#     assert before_run_rico_partylink.debtor_weight == 1

#     # WHEN
#     rico_grainunit = grainunit_shop("groupunit_partylink", grain_update())
#     rico_grainunit.set_locator("group_id", run_text)
#     rico_grainunit.set_locator("party_id", rico_text)
#     rico_grainunit.set_required_arg("group_id", run_text)
#     rico_grainunit.set_required_arg("party_id", rico_text)
#     new_rico_run_creditor_weight = 7
#     new_rico_run_debtor_weight = 11
#     rico_grainunit.set_optional_arg("creditor_weight", new_rico_run_creditor_weight)
#     rico_grainunit.set_optional_arg("debtor_weight", new_rico_run_debtor_weight)
#     print(f"{rico_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(rico_grainunit)
#     after_sue_agendaunit = sue_learnunit.get_after_agenda(before_sue_agendaunit)

#     # THEN
#     after_run_groupunit = after_sue_agendaunit.get_groupunit(run_text)
#     after_run_rico_partylink = after_run_groupunit.get_partylink(rico_text)
#     assert after_run_rico_partylink.creditor_weight == new_rico_run_creditor_weight
#     assert after_run_rico_partylink.debtor_weight == new_rico_run_debtor_weight


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_groupunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_agendaunit = agendaunit_shop(sue_text)
#     run_text = ",runners"
#     fly_text = ",flyers"
#     before_sue_agendaunit.set_groupunit(groupunit_shop(fly_text))
#     before_sue_agendaunit.set_groupunit(groupunit_shop(run_text))
#     assert before_sue_agendaunit.get_groupunit(run_text) != None
#     assert before_sue_agendaunit.get_groupunit(fly_text) != None

#     # WHEN
#     x_grainunit = grainunit_shop("groupunit", grain_delete())
#     print(f"{x_grainunit=}")
#     x_grainunit.set_locator("group_id", run_text)
#     x_grainunit.set_required_arg("group_id", run_text)
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(x_grainunit)
#     after_sue_agendaunit = sue_learnunit.get_after_agenda(before_sue_agendaunit)

#     # THEN
#     assert after_sue_agendaunit.get_groupunit(run_text) is None
#     assert after_sue_agendaunit.get_groupunit(fly_text) != None


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_groupunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_agendaunit = agendaunit_shop(sue_text)
#     run_text = ",runners"
#     before_sue_agendaunit.set_groupunit(groupunit_shop(run_text))
#     fly_text = ",flyers"
#     assert before_sue_agendaunit.get_groupunit(run_text) != None
#     assert before_sue_agendaunit.get_groupunit(fly_text) is None

#     # WHEN
#     x_grainunit = grainunit_shop("groupunit", grain_insert())
#     x_grainunit.set_locator("group_id", fly_text)
#     x_grainunit.set_required_arg("group_id", fly_text)
#     x_grainunit.set_optional_arg("_partylinks_set_by_economy_road", yao_roadunit())
#     print(f"{x_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(x_grainunit)
#     after_sue_agendaunit = sue_learnunit.get_after_agenda(before_sue_agendaunit)

#     # THEN
#     assert after_sue_agendaunit.get_groupunit(run_text) != None
#     assert after_sue_agendaunit.get_groupunit(fly_text) != None


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_groupunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_agendaunit = agendaunit_shop(sue_text)
#     run_text = ",runners"
#     before_sue_agendaunit.set_groupunit(groupunit_shop(run_text))
#     assert (
#         before_sue_agendaunit.get_groupunit(run_text)._partylinks_set_by_economy_road
#         is None
#     )

#     # WHEN
#     x_grainunit = grainunit_shop("groupunit", grain_update())
#     x_grainunit.set_locator("group_id", run_text)
#     x_grainunit.set_required_arg("group_id", run_text)
#     x_grainunit.set_optional_arg("_partylinks_set_by_economy_road", yao_roadunit())
#     print(f"{x_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(x_grainunit)
#     after_sue_agendaunit = sue_learnunit.get_after_agenda(before_sue_agendaunit)

#     # THEN
#     assert (
#         after_sue_agendaunit.get_groupunit(run_text)._partylinks_set_by_economy_road
#         == yao_roadunit()
#     )


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_groupunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_agendaunit = agendaunit_shop(sue_text)
#     run_text = ",runners"
#     fly_text = ",flyers"
#     before_sue_agendaunit.set_groupunit(groupunit_shop(fly_text))
#     before_sue_agendaunit.set_groupunit(groupunit_shop(run_text))
#     assert before_sue_agendaunit.get_groupunit(run_text) != None
#     assert before_sue_agendaunit.get_groupunit(fly_text) != None

#     # WHEN
#     x_grainunit = grainunit_shop("groupunit", grain_delete())
#     print(f"{x_grainunit=}")
#     x_grainunit.set_locator("group_id", run_text)
#     x_grainunit.set_required_arg("group_id", run_text)
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(x_grainunit)
#     after_sue_agendaunit = sue_learnunit.get_after_agenda(before_sue_agendaunit)

#     # THEN
#     assert after_sue_agendaunit.get_groupunit(run_text) is None
#     assert after_sue_agendaunit.get_groupunit(fly_text) != None


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_ideaunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_agendaunit = agendaunit_shop(sue_text)
#     sports_text = "sports"
#     sports_road = before_sue_agendaunit.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
#     disc_text = "Ultimate Disc"
#     disc_road = before_sue_agendaunit.make_road(sports_road, disc_text)
#     before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
#     before_sue_agendaunit.add_idea(ideaunit_shop(disc_text), sports_road)
#     assert before_sue_agendaunit.idea_exists(ball_road)
#     assert before_sue_agendaunit.idea_exists(disc_road)

#     # WHEN
#     delete_disc_grainunit = grainunit_shop("idea", grain_delete())
#     delete_disc_grainunit.set_locator("road", disc_road)
#     delete_disc_grainunit.set_required_arg("road", disc_road)
#     print(f"{delete_disc_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(delete_disc_grainunit)
#     after_sue_agendaunit = sue_learnunit.get_after_agenda(before_sue_agendaunit)

#     # THEN
#     assert after_sue_agendaunit.idea_exists(ball_road)
#     assert after_sue_agendaunit.idea_exists(disc_road) == False


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_ideaunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_agendaunit = agendaunit_shop(sue_text)
#     sports_text = "sports"
#     sports_road = before_sue_agendaunit.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
#     disc_text = "Ultimate Disc"
#     disc_road = before_sue_agendaunit.make_road(sports_road, disc_text)
#     before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
#     assert before_sue_agendaunit.idea_exists(ball_road)
#     assert before_sue_agendaunit.idea_exists(disc_road) == False

#     # WHEN
#     # x_addin = 140
#     # x_begin = 1000
#     # x_close = 1700
#     # x_denom = 17
#     x_meld_strategy = "override"
#     x_numeric_road = None
#     # x_numor = 10
#     x_promise = True
#     insert_disc_grainunit = grainunit_shop("idea", grain_insert())
#     insert_disc_grainunit.set_locator("road", disc_road)
#     insert_disc_grainunit.set_required_arg("label", disc_text)
#     insert_disc_grainunit.set_required_arg("parent_road", sports_road)
#     # insert_disc_grainunit.set_optional_arg("_addin", x_addin)
#     # insert_disc_grainunit.set_optional_arg("_begin", x_begin)
#     # insert_disc_grainunit.set_optional_arg("_close", x_close)
#     # insert_disc_grainunit.set_optional_arg("_denom", x_denom)
#     insert_disc_grainunit.set_optional_arg("_meld_strategy", x_meld_strategy)
#     insert_disc_grainunit.set_optional_arg("_numeric_road", x_numeric_road)
#     # insert_disc_grainunit.set_optional_arg("_numor", x_numor)
#     insert_disc_grainunit.set_optional_arg("promise", x_promise)

#     print(f"{insert_disc_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(insert_disc_grainunit)
#     after_sue_agendaunit = sue_learnunit.get_after_agenda(before_sue_agendaunit)

#     # THEN
#     assert after_sue_agendaunit.idea_exists(ball_road)
#     assert after_sue_agendaunit.idea_exists(disc_road)


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_ideaunit_SimpleAttributes():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_agendaunit = agendaunit_shop(sue_text)
#     sports_text = "sports"
#     sports_road = before_sue_agendaunit.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
#     before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
#     assert before_sue_agendaunit.get_idea_obj(ball_road)._begin is None
#     assert before_sue_agendaunit.get_idea_obj(ball_road)._close is None
#     assert before_sue_agendaunit.get_idea_obj(ball_road)._meld_strategy == "default"
#     assert before_sue_agendaunit.get_idea_obj(ball_road).promise == False

#     # WHEN
#     # x_addin = 140
#     x_begin = 1000
#     x_close = 1700
#     # x_denom = 17
#     x_meld_strategy = "override"
#     # x_numor = 10
#     x_promise = True
#     insert_disc_grainunit = grainunit_shop("idea", grain_update())
#     insert_disc_grainunit.set_locator("road", ball_road)
#     insert_disc_grainunit.set_required_arg("road", ball_road)
#     # insert_disc_grainunit.set_optional_arg("_addin", x_addin)
#     insert_disc_grainunit.set_optional_arg("_begin", x_begin)
#     insert_disc_grainunit.set_optional_arg("_close", x_close)
#     # insert_disc_grainunit.set_optional_arg("_denom", x_denom)
#     insert_disc_grainunit.set_optional_arg("_meld_strategy", x_meld_strategy)
#     # insert_disc_grainunit.set_optional_arg("_numor", x_numor)
#     insert_disc_grainunit.set_optional_arg("promise", x_promise)

#     print(f"{insert_disc_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(insert_disc_grainunit)
#     after_sue_agendaunit = sue_learnunit.get_after_agenda(before_sue_agendaunit)

#     # THEN
#     assert after_sue_agendaunit.get_idea_obj(ball_road)._begin == x_begin
#     assert after_sue_agendaunit.get_idea_obj(ball_road)._close == x_close
#     assert (
#         after_sue_agendaunit.get_idea_obj(ball_road)._meld_strategy == x_meld_strategy
#     )
#     assert after_sue_agendaunit.get_idea_obj(ball_road).promise


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_idea_balancelink():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     rico_text = "Rico"
#     carm_text = "Carmen"
#     dizz_text = "Dizzy"
#     before_sue_au.add_partyunit(rico_text)
#     before_sue_au.add_partyunit(carm_text)
#     before_sue_au.add_partyunit(dizz_text)
#     run_text = ",runners"
#     run_groupunit = groupunit_shop(run_text)
#     run_groupunit.set_partylink(partylink_shop(rico_text))
#     run_groupunit.set_partylink(partylink_shop(carm_text))
#     fly_text = ",flyers"
#     fly_groupunit = groupunit_shop(fly_text)
#     fly_groupunit.set_partylink(partylink_shop(rico_text))
#     fly_groupunit.set_partylink(partylink_shop(carm_text))
#     fly_groupunit.set_partylink(partylink_shop(dizz_text))
#     before_sue_au.set_groupunit(run_groupunit)
#     before_sue_au.set_groupunit(fly_groupunit)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     disc_text = "Ultimate Disc"
#     disc_road = before_sue_au.make_road(sports_road, disc_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     before_sue_au.add_idea(ideaunit_shop(disc_text), sports_road)
#     before_sue_au.edit_idea_attr(ball_road, balancelink=balancelink_shop(run_text))
#     before_sue_au.edit_idea_attr(ball_road, balancelink=balancelink_shop(fly_text))
#     before_sue_au.edit_idea_attr(disc_road, balancelink=balancelink_shop(run_text))
#     before_sue_au.edit_idea_attr(disc_road, balancelink=balancelink_shop(fly_text))
#     assert len(before_sue_au.get_idea_obj(ball_road)._balancelinks) == 2
#     assert len(before_sue_au.get_idea_obj(disc_road)._balancelinks) == 2

#     # WHEN
#     delete_disc_grainunit = grainunit_shop("idea_balancelink", grain_delete())
#     delete_disc_grainunit.set_locator("road", disc_road)
#     delete_disc_grainunit.set_locator("group_id", fly_text)
#     delete_disc_grainunit.set_required_arg("road", disc_road)
#     delete_disc_grainunit.set_required_arg("group_id", fly_text)
#     print(f"{delete_disc_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(delete_disc_grainunit)
#     after_sue_agendaunit = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     assert len(after_sue_agendaunit.get_idea_obj(ball_road)._balancelinks) == 2
#     assert len(after_sue_agendaunit.get_idea_obj(disc_road)._balancelinks) == 1


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_idea_balancelink():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     rico_text = "Rico"
#     carm_text = "Carmen"
#     before_sue_au.add_partyunit(rico_text)
#     before_sue_au.add_partyunit(carm_text)
#     run_text = ",runners"
#     run_groupunit = groupunit_shop(run_text)
#     run_groupunit.set_partylink(partylink_shop(rico_text))
#     before_sue_au.set_groupunit(run_groupunit)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     before_sue_au.edit_idea_attr(ball_road, balancelink=balancelink_shop(run_text))
#     run_balancelink = before_sue_au.get_idea_obj(ball_road)._balancelinks.get(run_text)
#     assert run_balancelink.creditor_weight == 1
#     assert run_balancelink.debtor_weight == 1

#     # WHEN
#     x_creditor_weight = 55
#     x_debtor_weight = 66
#     update_disc_grainunit = grainunit_shop("idea_balancelink", grain_update())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("group_id", run_text)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("group_id", run_text)
#     update_disc_grainunit.set_optional_arg("creditor_weight", x_creditor_weight)
#     update_disc_grainunit.set_optional_arg("debtor_weight", x_debtor_weight)
#     # print(f"{update_disc_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(update_disc_grainunit)
#     after_sue_au = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     run_balancelink = after_sue_au.get_idea_obj(ball_road)._balancelinks.get(run_text)
#     print(f"{run_balancelink.creditor_weight=}")
#     assert run_balancelink.creditor_weight == x_creditor_weight
#     assert run_balancelink.debtor_weight == x_debtor_weight


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_idea_balancelink():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     rico_text = "Rico"
#     carm_text = "Carmen"
#     before_sue_au.add_partyunit(rico_text)
#     before_sue_au.add_partyunit(carm_text)
#     run_text = ",runners"
#     run_groupunit = groupunit_shop(run_text)
#     run_groupunit.set_partylink(partylink_shop(rico_text))
#     before_sue_au.set_groupunit(run_groupunit)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     before_ball_idea = before_sue_au.get_idea_obj(ball_road)
#     assert before_ball_idea._balancelinks.get(run_text) is None

#     # WHEN
#     x_creditor_weight = 55
#     x_debtor_weight = 66
#     update_disc_grainunit = grainunit_shop("idea_balancelink", grain_insert())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("group_id", run_text)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("group_id", run_text)
#     update_disc_grainunit.set_optional_arg("creditor_weight", x_creditor_weight)
#     update_disc_grainunit.set_optional_arg("debtor_weight", x_debtor_weight)
#     # print(f"{update_disc_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(update_disc_grainunit)
#     after_sue_au = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     after_ball_idea = after_sue_au.get_idea_obj(ball_road)
#     assert after_ball_idea._balancelinks.get(run_text) != None


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_idea_beliefunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     knee_text = "knee"
#     knee_road = before_sue_au.make_l1_road(knee_text)
#     broken_text = "broke cartilage"
#     broken_road = before_sue_au.make_road(knee_road, broken_text)
#     before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
#     before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
#     before_ball_idea = before_sue_au.get_idea_obj(ball_road)
#     assert before_ball_idea._beliefunits == {}

#     # WHEN
#     broken_open = 55
#     broken_nigh = 66
#     update_disc_grainunit = grainunit_shop("idea_beliefunit", grain_insert())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)
#     update_disc_grainunit.set_required_arg("pick", broken_road)
#     update_disc_grainunit.set_optional_arg("open", broken_open)
#     update_disc_grainunit.set_optional_arg("nigh", broken_nigh)
#     # print(f"{update_disc_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(update_disc_grainunit)
#     after_sue_au = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     after_ball_idea = after_sue_au.get_idea_obj(ball_road)
#     assert after_ball_idea._beliefunits != {}
#     assert after_ball_idea._beliefunits.get(knee_road) != None
#     assert after_ball_idea._beliefunits.get(knee_road).base == knee_road
#     assert after_ball_idea._beliefunits.get(knee_road).pick == broken_road
#     assert after_ball_idea._beliefunits.get(knee_road).open == broken_open
#     assert after_ball_idea._beliefunits.get(knee_road).nigh == broken_nigh


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_idea_beliefunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     knee_text = "knee"
#     knee_road = before_sue_au.make_l1_road(knee_text)
#     broken_text = "broke cartilage"
#     broken_road = before_sue_au.make_road(knee_road, broken_text)
#     before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
#     before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
#     before_sue_au.edit_idea_attr(
#         road=ball_road, beliefunit=beliefunit_shop(base=knee_road, pick=broken_road)
#     )
#     before_ball_idea = before_sue_au.get_idea_obj(ball_road)
#     assert before_ball_idea._beliefunits != {}
#     assert before_ball_idea._beliefunits.get(knee_road) != None

#     # WHEN
#     update_disc_grainunit = grainunit_shop("idea_beliefunit", grain_delete())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)
#     # print(f"{update_disc_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(update_disc_grainunit)
#     after_sue_au = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     after_ball_idea = after_sue_au.get_idea_obj(ball_road)
#     assert after_ball_idea._beliefunits == {}


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_idea_beliefunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     knee_text = "knee"
#     knee_road = before_sue_au.make_l1_road(knee_text)
#     broken_text = "broke cartilage"
#     broken_road = before_sue_au.make_road(knee_road, broken_text)
#     medical_text = "get medical attention"
#     medical_road = before_sue_au.make_road(knee_road, medical_text)
#     before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
#     before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
#     before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
#     before_knee_beliefunit = beliefunit_shop(knee_road, broken_road)
#     before_sue_au.edit_idea_attr(ball_road, beliefunit=before_knee_beliefunit)
#     before_ball_idea = before_sue_au.get_idea_obj(ball_road)
#     assert before_ball_idea._beliefunits != {}
#     assert before_ball_idea._beliefunits.get(knee_road) != None
#     assert before_ball_idea._beliefunits.get(knee_road).pick == broken_road
#     assert before_ball_idea._beliefunits.get(knee_road).open is None
#     assert before_ball_idea._beliefunits.get(knee_road).nigh is None

#     # WHEN
#     medical_open = 45
#     medical_nigh = 77
#     update_disc_grainunit = grainunit_shop("idea_beliefunit", grain_update())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)
#     update_disc_grainunit.set_optional_arg("pick", medical_road)
#     update_disc_grainunit.set_optional_arg("open", medical_open)
#     update_disc_grainunit.set_optional_arg("nigh", medical_nigh)
#     # print(f"{update_disc_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(update_disc_grainunit)
#     after_sue_au = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     after_ball_idea = after_sue_au.get_idea_obj(ball_road)
#     assert after_ball_idea._beliefunits != {}
#     assert after_ball_idea._beliefunits.get(knee_road) != None
#     assert after_ball_idea._beliefunits.get(knee_road).pick == medical_road
#     assert after_ball_idea._beliefunits.get(knee_road).open == medical_open
#     assert after_ball_idea._beliefunits.get(knee_road).nigh == medical_nigh


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_idea_reasonunit_premiseunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     knee_text = "knee"
#     knee_road = before_sue_au.make_l1_road(knee_text)
#     broken_text = "broke cartilage"
#     broken_road = before_sue_au.make_road(knee_road, broken_text)
#     before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
#     before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
#     before_sue_au.edit_idea_attr(
#         ball_road, reason_base=knee_road, reason_premise=broken_road
#     )
#     before_ball_idea = before_sue_au.get_idea_obj(ball_road)
#     assert before_ball_idea._reasonunits != {}
#     before_knee_reasonunit = before_ball_idea.get_reasonunit(knee_road)
#     assert before_knee_reasonunit != None
#     broken_premiseunit = before_knee_reasonunit.get_premise(broken_road)
#     assert broken_premiseunit.need == broken_road
#     assert broken_premiseunit.open is None
#     assert broken_premiseunit.nigh is None
#     assert broken_premiseunit.divisor is None

#     # WHEN
#     broken_open = 45
#     broken_nigh = 77
#     broken_divisor = 3
#     update_disc_grainunit = grainunit_shop(
#         "idea_reasonunit_premiseunit", grain_update()
#     )
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_locator("need", broken_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)
#     update_disc_grainunit.set_required_arg("need", broken_road)
#     update_disc_grainunit.set_optional_arg("open", broken_open)
#     update_disc_grainunit.set_optional_arg("nigh", broken_nigh)
#     update_disc_grainunit.set_optional_arg("divisor", broken_divisor)
#     # print(f"{update_disc_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(update_disc_grainunit)
#     after_sue_au = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     after_ball_idea = after_sue_au.get_idea_obj(ball_road)
#     after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
#     assert after_knee_reasonunit != None
#     after_broken_premiseunit = after_knee_reasonunit.get_premise(broken_road)
#     assert after_broken_premiseunit.need == broken_road
#     assert after_broken_premiseunit.open == broken_open
#     assert after_broken_premiseunit.nigh == broken_nigh
#     assert after_broken_premiseunit.divisor == broken_divisor


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_idea_reasonunit_premiseunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     knee_text = "knee"
#     knee_road = before_sue_au.make_l1_road(knee_text)
#     broken_text = "broke cartilage"
#     broken_road = before_sue_au.make_road(knee_road, broken_text)
#     medical_text = "get medical attention"
#     medical_road = before_sue_au.make_road(knee_road, medical_text)
#     before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
#     before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
#     before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
#     before_sue_au.edit_idea_attr(
#         ball_road, reason_base=knee_road, reason_premise=broken_road
#     )
#     before_ball_idea = before_sue_au.get_idea_obj(ball_road)
#     before_knee_reasonunit = before_ball_idea.get_reasonunit(knee_road)
#     assert before_knee_reasonunit.get_premise(broken_road) != None
#     assert before_knee_reasonunit.get_premise(medical_road) is None

#     # WHEN
#     medical_open = 45
#     medical_nigh = 77
#     medical_divisor = 3
#     update_disc_grainunit = grainunit_shop(
#         "idea_reasonunit_premiseunit", grain_insert()
#     )
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_locator("need", medical_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)
#     update_disc_grainunit.set_required_arg("need", medical_road)
#     update_disc_grainunit.set_optional_arg("open", medical_open)
#     update_disc_grainunit.set_optional_arg("nigh", medical_nigh)
#     update_disc_grainunit.set_optional_arg("divisor", medical_divisor)
#     # print(f"{update_disc_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(update_disc_grainunit)
#     after_sue_au = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     after_ball_idea = after_sue_au.get_idea_obj(ball_road)
#     after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
#     after_medical_premiseunit = after_knee_reasonunit.get_premise(medical_road)
#     assert after_medical_premiseunit != None
#     assert after_medical_premiseunit.need == medical_road
#     assert after_medical_premiseunit.open == medical_open
#     assert after_medical_premiseunit.nigh == medical_nigh
#     assert after_medical_premiseunit.divisor == medical_divisor


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_idea_reasonunit_premiseunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     knee_text = "knee"
#     knee_road = before_sue_au.make_l1_road(knee_text)
#     broken_text = "broke cartilage"
#     broken_road = before_sue_au.make_road(knee_road, broken_text)
#     medical_text = "get medical attention"
#     medical_road = before_sue_au.make_road(knee_road, medical_text)
#     before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
#     before_sue_au.add_idea(ideaunit_shop(broken_text), knee_road)
#     before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
#     before_sue_au.edit_idea_attr(
#         ball_road, reason_base=knee_road, reason_premise=broken_road
#     )
#     before_sue_au.edit_idea_attr(
#         ball_road, reason_base=knee_road, reason_premise=medical_road
#     )
#     before_ball_idea = before_sue_au.get_idea_obj(ball_road)
#     before_knee_reasonunit = before_ball_idea.get_reasonunit(knee_road)
#     assert before_knee_reasonunit.get_premise(broken_road) != None
#     assert before_knee_reasonunit.get_premise(medical_road) != None

#     # WHEN
#     update_disc_grainunit = grainunit_shop(
#         "idea_reasonunit_premiseunit", grain_delete()
#     )
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_locator("need", medical_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)
#     update_disc_grainunit.set_required_arg("need", medical_road)
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(update_disc_grainunit)
#     after_sue_au = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     after_ball_idea = after_sue_au.get_idea_obj(ball_road)
#     after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
#     assert after_knee_reasonunit.get_premise(broken_road) != None
#     assert after_knee_reasonunit.get_premise(medical_road) is None


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_idea_reasonunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     knee_text = "knee"
#     knee_road = before_sue_au.make_l1_road(knee_text)
#     medical_text = "get medical attention"
#     medical_road = before_sue_au.make_road(knee_road, medical_text)
#     before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
#     before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
#     before_ball_idea = before_sue_au.get_idea_obj(ball_road)
#     assert before_ball_idea.get_reasonunit(knee_road) is None

#     # WHEN
#     medical_suff_idea_active = True
#     update_disc_grainunit = grainunit_shop("idea_reasonunit", grain_insert())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)
#     update_disc_grainunit.set_optional_arg("suff_idea_active", medical_suff_idea_active)
#     # print(f"{update_disc_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(update_disc_grainunit)
#     after_sue_au = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     after_ball_idea = after_sue_au.get_idea_obj(ball_road)
#     after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
#     assert after_knee_reasonunit != None
#     assert after_knee_reasonunit.get_premise(medical_road) is None
#     assert after_knee_reasonunit.suff_idea_active == medical_suff_idea_active


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_update_idea_reasonunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     knee_text = "knee"
#     knee_road = before_sue_au.make_l1_road(knee_text)
#     medical_text = "get medical attention"
#     medical_road = before_sue_au.make_road(knee_road, medical_text)
#     before_medical_suff_idea_active = False
#     before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
#     before_sue_au.add_idea(ideaunit_shop(medical_text), knee_road)
#     before_sue_au.edit_idea_attr(
#         road=ball_road,
#         reason_base=knee_road,
#         reason_suff_idea_active=before_medical_suff_idea_active,
#     )
#     before_ball_idea = before_sue_au.get_idea_obj(ball_road)
#     before_ball_reasonunit = before_ball_idea.get_reasonunit(knee_road)
#     assert before_ball_reasonunit != None
#     assert before_ball_reasonunit.suff_idea_active == before_medical_suff_idea_active

#     # WHEN
#     after_medical_suff_idea_active = True
#     update_disc_grainunit = grainunit_shop("idea_reasonunit", grain_update())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)
#     update_disc_grainunit.set_optional_arg(
#         "suff_idea_active", after_medical_suff_idea_active
#     )
#     # print(f"{update_disc_grainunit=}")
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(update_disc_grainunit)
#     after_sue_au = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     after_ball_idea = after_sue_au.get_idea_obj(ball_road)
#     after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
#     assert after_knee_reasonunit != None
#     assert after_knee_reasonunit.get_premise(medical_road) is None
#     assert after_knee_reasonunit.suff_idea_active == after_medical_suff_idea_active


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_idea_reasonunit():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     knee_text = "knee"
#     knee_road = before_sue_au.make_l1_road(knee_text)
#     medical_suff_idea_active = False
#     before_sue_au.add_l1_idea(ideaunit_shop(knee_text))
#     before_sue_au.edit_idea_attr(
#         road=ball_road,
#         reason_base=knee_road,
#         reason_suff_idea_active=medical_suff_idea_active,
#     )
#     before_ball_idea = before_sue_au.get_idea_obj(ball_road)
#     assert before_ball_idea.get_reasonunit(knee_road) != None

#     # WHEN
#     update_disc_grainunit = grainunit_shop("idea_reasonunit", grain_delete())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(update_disc_grainunit)
#     after_sue_au = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     after_ball_idea = after_sue_au.get_idea_obj(ball_road)
#     assert after_ball_idea.get_reasonunit(knee_road) is None


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_insert_idea_suffgroup():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     rico_text = "Rico"
#     before_sue_au.add_partyunit(rico_text)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     before_ball_ideaunit = before_sue_au.get_idea_obj(ball_road)
#     assert before_ball_ideaunit._assignedunit._suffgroups == {}

#     # WHEN
#     update_disc_grainunit = grainunit_shop("idea_suffgroup", grain_insert())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("group_id", rico_text)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("group_id", rico_text)
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(update_disc_grainunit)
#     after_sue_au = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     after_ball_ideaunit = after_sue_au.get_idea_obj(ball_road)
#     assert after_ball_ideaunit._assignedunit._suffgroups != {}
#     assert after_ball_ideaunit._assignedunit.get_suffgroup(rico_text) != None


# def test_LearnUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_delete_idea_suffgroup():
#     # GIVEN
#     sue_road = get_sue_personroad()
#     sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
#     before_sue_au = agendaunit_shop(sue_text)
#     rico_text = "Rico"
#     before_sue_au.add_partyunit(rico_text)
#     sports_text = "sports"
#     sports_road = before_sue_au.make_l1_road(sports_text)
#     ball_text = "basketball"
#     ball_road = before_sue_au.make_road(sports_road, ball_text)
#     before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
#     before_ball_ideaunit = before_sue_au.get_idea_obj(ball_road)
#     before_ball_ideaunit._assignedunit.set_suffgroup(rico_text)
#     assert before_ball_ideaunit._assignedunit._suffgroups != {}
#     assert before_ball_ideaunit._assignedunit.get_suffgroup(rico_text) != None

#     # WHEN
#     update_disc_grainunit = grainunit_shop("idea_suffgroup", grain_delete())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("group_id", rico_text)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("group_id", rico_text)
#     sue_learnunit = learnunit_shop(sue_road)
#     sue_learnunit.set_grainunit(update_disc_grainunit)
#     print(f"{before_sue_au.get_idea_obj(ball_road)._assignedunit=}")
#     after_sue_au = sue_learnunit.get_after_agenda(before_sue_au)

#     # THEN
#     after_ball_ideaunit = after_sue_au.get_idea_obj(ball_road)
#     assert after_ball_ideaunit._assignedunit._suffgroups == {}
