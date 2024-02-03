from src._prime.road import get_single_roadnode, create_road
from src.agenda.party import partylink_shop
from src.agenda.reason_idea import beliefunit_shop
from src.agenda.group import groupunit_shop
from src.agenda.learn import (
    grain_update,
    grain_delete,
    grain_insert,
    grainunit_shop,
)
from src.agenda.examples.example_learns import (
    get_sue_proad,
    get_yao_example_roadunit as yao_roadunit,
)


def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnitSimpleAttrs():
    # WHEN
    new2_value = 66
    category = "agendaunit"
    opt_arg2 = "_max_tree_traverse"
    x_grainunit = grainunit_shop(category, grain_update())
    x_grainunit.set_optional_arg(opt_arg2, new2_value)
    # THEN
    assert (
        x_grainunit.get_description()
        == f"Agenda's maximum number of Agenda output evaluations changed to {new2_value}."
    )

    # WHEN
    new5_value = "override"
    opt_arg5 = "_meld_strategy"
    x_grainunit = grainunit_shop(category, grain_update())
    x_grainunit.set_optional_arg(opt_arg5, new5_value)
    # THEN
    assert (
        x_grainunit.get_description()
        == f"Agenda's Meld Strategy changed to {new5_value}."
    )

    # WHEN
    new3_value = 77
    opt_arg3 = "_party_creditor_pool"
    x_grainunit = grainunit_shop(category, grain_update())
    x_grainunit.set_optional_arg(opt_arg3, new3_value)
    # THEN
    assert (
        x_grainunit.get_description()
        == f"Agenda's creditor pool limit changed to {new3_value}."
    )

    # WHEN
    new4_value = 88
    opt_arg4 = "_party_debtor_pool"
    x_grainunit = grainunit_shop(category, grain_update())
    x_grainunit.set_optional_arg(opt_arg4, new4_value)
    # THEN
    assert (
        x_grainunit.get_description()
        == f"Agenda's debtor pool limit changed to {new4_value}."
    )

    # GIVEN
    new1_value = 55
    opt_arg1 = "_weight"
    # WHEN
    x_grainunit = grainunit_shop(category, grain_update())
    x_grainunit.set_optional_arg(opt_arg1, new1_value)
    # THEN
    assert x_grainunit.get_description() == f"Agenda's weight changed to {new1_value}."


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_delete_party():
#     # GIVEN

#     rico_text = "Rico"
#     carm_text = "Carmen"

#     category = "partyunit"
#     x_grainunit = grainunit_shop(category, grain_delete())
#     x_grainunit.set_locator("party_id", carm_text)
#     x_grainunit.set_required_arg("party_id", carm_text)


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_insert_party():
#     # GIVEN

#     rico_text = "Rico"
#     carm_text = "Carmen"

#     # WHEN
#     category = "partyunit"
#     x_grainunit = grainunit_shop(category, grain_insert())
#     x_grainunit.set_locator("party_id", carm_text)
#     x_grainunit.set_required_arg("party_id", carm_text)
#     x_creditor_weight = 55
#     x_debtor_weight = 66
#     x_grainunit.set_optional_arg("creditor_weight", x_creditor_weight)
#     x_grainunit.set_optional_arg("debtor_weight", x_debtor_weight)


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_update_party():
#     # GIVEN

#     rico_text = "Rico"

#     # WHEN
#     category = "partyunit"
#     x_grainunit = grainunit_shop(category, grain_update())
#     x_grainunit.set_locator("party_id", rico_text)
#     x_grainunit.set_required_arg("party_id", rico_text)
#     rico_creditor_weight = 55
#     x_grainunit.set_optional_arg("creditor_weight", rico_creditor_weight)

#     # THEN


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_delete_partylink():
#     # GIVEN

#     rico_text = "Rico"
#     carm_text = "Carmen"
#     dizz_text = "Dizzy"

#     run_text = ",runners"
#     run_groupunit = groupunit_shop(run_text)
#     run_groupunit.set_partylink(partylink_shop(rico_text))
#     run_groupunit.set_partylink(partylink_shop(carm_text))
#     fly_text = ",flyers"
#     fly_groupunit = groupunit_shop(fly_text)
#     fly_groupunit.set_partylink(partylink_shop(rico_text))
#     fly_groupunit.set_partylink(partylink_shop(carm_text))
#     fly_groupunit.set_partylink(partylink_shop(dizz_text))

#     # WHEN
#     rico_grainunit = grainunit_shop("partylink", grain_delete())
#     rico_grainunit.set_locator("group_id", run_text)
#     rico_grainunit.set_locator("party_id", rico_text)
#     rico_grainunit.set_required_arg("group_id", run_text)
#     rico_grainunit.set_required_arg("party_id", rico_text)
#     # print(f"{rico_grainunit=}")
#     carm_grainunit = grainunit_shop("partylink", grain_delete())
#     carm_grainunit.set_locator("group_id", fly_text)
#     carm_grainunit.set_locator("party_id", carm_text)
#     carm_grainunit.set_required_arg("group_id", fly_text)
#     carm_grainunit.set_required_arg("party_id", carm_text)
#     # print(f"{carm_grainunit=}")


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_insert_partylink():
#     # GIVEN

#     rico_text = "Rico"
#     carm_text = "Carmen"
#     dizz_text = "Dizzy"

#     run_text = ",runners"
#     run_groupunit = groupunit_shop(run_text)
#     run_groupunit.set_partylink(partylink_shop(carm_text))

#     # WHEN
#     rico_grainunit = grainunit_shop("partylink", grain_insert())
#     rico_grainunit.set_locator("group_id", run_text)
#     rico_grainunit.set_locator("party_id", rico_text)
#     rico_grainunit.set_required_arg("group_id", run_text)
#     rico_grainunit.set_required_arg("party_id", rico_text)
#     rico_run_creditor_weight = 17
#     rico_grainunit.set_optional_arg("creditor_weight", rico_run_creditor_weight)
#     print(f"{rico_grainunit=}")


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_update_partylink():
#     # GIVEN

#     rico_text = "Rico"

#     run_text = ",runners"
#     run_groupunit = groupunit_shop(run_text)
#     old_rico_run_creditor_weight = 3
#     run_groupunit.set_partylink(partylink_shop(rico_text, old_rico_run_creditor_weight))

#     # WHEN
#     rico_grainunit = grainunit_shop("partylink", grain_update())
#     rico_grainunit.set_locator("group_id", run_text)
#     rico_grainunit.set_locator("party_id", rico_text)
#     rico_grainunit.set_required_arg("group_id", run_text)
#     rico_grainunit.set_required_arg("party_id", rico_text)
#     new_rico_run_creditor_weight = 7
#     new_rico_run_debtor_weight = 11
#     rico_grainunit.set_optional_arg("creditor_weight", new_rico_run_creditor_weight)
#     rico_grainunit.set_optional_arg("debtor_weight", new_rico_run_debtor_weight)
#     print(f"{rico_grainunit=}")


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_delete_groupunit():
#     # GIVEN

#     run_text = ",runners"
#     fly_text = ",flyers"

#     # WHEN
#     x_grainunit = grainunit_shop("groupunit", grain_delete())
#     print(f"{x_grainunit=}")
#     x_grainunit.set_locator("group_id", run_text)
#     x_grainunit.set_required_arg("group_id", run_text)


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_insert_groupunit():
#     # GIVEN

#     run_text = ",runners"
#     fly_text = ",flyers"

#     # WHEN
#     x_grainunit = grainunit_shop("groupunit", grain_insert())
#     x_grainunit.set_locator("group_id", fly_text)
#     x_grainunit.set_required_arg("group_id", fly_text)
#     x_grainunit.set_optional_arg("_treasury_partylinks", yao_roadunit())
#     print(f"{x_grainunit=}")


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_update_groupunit():
#     # GIVEN

#     run_text = ",runners"

#     # WHEN
#     x_grainunit = grainunit_shop("groupunit", grain_update())
#     x_grainunit.set_locator("group_id", run_text)
#     x_grainunit.set_required_arg("group_id", run_text)
#     x_grainunit.set_optional_arg("_treasury_partylinks", yao_roadunit())
#     print(f"{x_grainunit=}")


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_delete_groupunit():
#     # GIVEN

#     run_text = ",runners"
#     fly_text = ",flyers"

#     # WHEN
#     x_grainunit = grainunit_shop("groupunit", grain_delete())
#     print(f"{x_grainunit=}")
#     x_grainunit.set_locator("group_id", run_text)
#     x_grainunit.set_required_arg("group_id", run_text)


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_delete_ideaunit():
#     # GIVEN

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)
#     disc_text = "Ultimate Disc"
#     disc_road = create_road(sports_road, disc_text)

#     # WHEN
#     delete_disc_grainunit = grainunit_shop("ideaunit", grain_delete())
#     delete_disc_grainunit.set_locator("road", disc_road)
#     delete_disc_grainunit.set_required_arg("road", disc_road)
#     print(f"{delete_disc_grainunit=}")


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_insert_ideaunit():
#     # GIVEN

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)
#     disc_text = "Ultimate Disc"
#     disc_road = create_road(sports_road, disc_text)

#     # WHEN
#     # x_addin = 140
#     # x_begin = 1000
#     # x_close = 1700
#     # x_denom = 17
#     x_meld_strategy = "override"
#     x_numeric_road = None
#     # x_numor = 10
#     x_promise = True
#     insert_disc_grainunit = grainunit_shop("ideaunit", grain_insert())
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


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_update_ideaunit_SimpleAttributes():
#     # GIVEN

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)

#     # WHEN
#     # x_addin = 140
#     x_begin = 1000
#     x_close = 1700
#     # x_denom = 17
#     x_meld_strategy = "override"
#     # x_numor = 10
#     x_promise = True
#     insert_disc_grainunit = grainunit_shop("ideaunit", grain_update())
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


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_delete_idea_balancelink():
#     # GIVEN

#     rico_text = "Rico"
#     carm_text = "Carmen"
#     dizz_text = "Dizzy"

#     run_text = ",runners"
#     run_groupunit = groupunit_shop(run_text)
#     run_groupunit.set_partylink(partylink_shop(rico_text))
#     run_groupunit.set_partylink(partylink_shop(carm_text))
#     fly_text = ",flyers"
#     fly_groupunit = groupunit_shop(fly_text)
#     fly_groupunit.set_partylink(partylink_shop(rico_text))
#     fly_groupunit.set_partylink(partylink_shop(carm_text))
#     fly_groupunit.set_partylink(partylink_shop(dizz_text))
#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)
#     disc_text = "Ultimate Disc"
#     disc_road = create_road(sports_road, disc_text)

#     # WHEN
#     delete_disc_grainunit = grainunit_shop("idea_balancelink", grain_delete())
#     delete_disc_grainunit.set_locator("road", disc_road)
#     delete_disc_grainunit.set_locator("group_id", fly_text)
#     delete_disc_grainunit.set_required_arg("road", disc_road)
#     delete_disc_grainunit.set_required_arg("group_id", fly_text)
#     print(f"{delete_disc_grainunit=}")


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_update_idea_balancelink():
#     # GIVEN

#     rico_text = "Rico"
#     carm_text = "Carmen"

#     run_text = ",runners"
#     run_groupunit = groupunit_shop(run_text)
#     run_groupunit.set_partylink(partylink_shop(rico_text))
#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)

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


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_insert_idea_balancelink():
#     # GIVEN

#     rico_text = "Rico"
#     carm_text = "Carmen"

#     run_text = ",runners"
#     run_groupunit = groupunit_shop(run_text)
#     run_groupunit.set_partylink(partylink_shop(rico_text))
#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)

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


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_insert_idea_beliefunit():
#     # GIVEN

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)
#     knee_text = "knee"
#     knee_road = create_road("a", knee_text)
#     broken_text = "broke cartilage"
#     broken_road = create_road(knee_road, broken_text)

#     # WHEN
#     broken_open = 55
#     broken_nigh = 66
#     update_disc_grainunit = grainunit_shop("idea_beliefunit", grain_insert())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)
#     update_disc_grainunit.set_optional_arg("pick", broken_road)
#     update_disc_grainunit.set_optional_arg("open", broken_open)
#     update_disc_grainunit.set_optional_arg("nigh", broken_nigh)
#     # print(f"{update_disc_grainunit=}")


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_delete_idea_beliefunit():
#     # GIVEN

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)
#     knee_text = "knee"
#     knee_road = create_road("a", knee_text)
#     broken_text = "broke cartilage"
#     broken_road = create_road(knee_road, broken_text)

#     # WHEN
#     update_disc_grainunit = grainunit_shop("idea_beliefunit", grain_delete())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)
#     # print(f"{update_disc_grainunit=}")


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_update_idea_beliefunit():
#     # GIVEN

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)
#     knee_text = "knee"
#     knee_road = create_road("a", knee_text)
#     broken_text = "broke cartilage"
#     broken_road = create_road(knee_road, broken_text)
#     medical_text = "get medical attention"
#     medical_road = create_road(knee_road, medical_text)
#     before_knee_beliefunit = beliefunit_shop(knee_road, broken_road)

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


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_update_idea_reason_premiseunit():
#     # GIVEN

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)
#     knee_text = "knee"
#     knee_road = create_road("a", knee_text)
#     broken_text = "broke cartilage"
#     broken_road = create_road(knee_road, broken_text)

#     # WHEN
#     broken_open = 45
#     broken_nigh = 77
#     broken_divisor = 3
#     update_disc_grainunit = grainunit_shop(
#         "idea_reason_premiseunit", grain_update()
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


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_insert_idea_reason_premiseunit():
#     # GIVEN

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)
#     knee_text = "knee"
#     knee_road = create_road("a", knee_text)
#     broken_text = "broke cartilage"
#     broken_road = create_road(knee_road, broken_text)
#     medical_text = "get medical attention"
#     medical_road = create_road(knee_road, medical_text)

#     # WHEN
#     medical_open = 45
#     medical_nigh = 77
#     medical_divisor = 3
#     update_disc_grainunit = grainunit_shop(
#         "idea_reason_premiseunit", grain_insert()
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


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_delete_idea_reason_premiseunit():
#     # GIVEN

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)
#     knee_text = "knee"
#     knee_road = create_road("a", knee_text)
#     broken_text = "broke cartilage"
#     broken_road = create_road(knee_road, broken_text)
#     medical_text = "get medical attention"
#     medical_road = create_road(knee_road, medical_text)
#     # WHEN
#     update_disc_grainunit = grainunit_shop(
#         "idea_reason_premiseunit", grain_delete()
#     )
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_locator("need", medical_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)
#     update_disc_grainunit.set_required_arg("need", medical_road)


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_insert_idea_reasonunit():
#     # GIVEN

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)
#     knee_text = "knee"
#     knee_road = create_road("a", knee_text)
#     medical_text = "get medical attention"
#     medical_road = create_road(knee_road, medical_text)

#     # WHEN
#     medical_suff_idea_active = True
#     update_disc_grainunit = grainunit_shop("idea_reasonunit", grain_insert())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)
#     update_disc_grainunit.set_optional_arg("suff_idea_active", medical_suff_idea_active)
#     # print(f"{update_disc_grainunit=}")


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_update_idea_reasonunit():
#     # GIVEN

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)
#     knee_text = "knee"
#     knee_road = create_road("a", knee_text)
#     medical_text = "get medical attention"
#     medical_road = create_road(knee_road, medical_text)
#     before_medical_suff_idea_active = False
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


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_delete_idea_reasonunit():
#     # GIVEN

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)
#     knee_text = "knee"
#     knee_road = create_road("a", knee_text)
#     medical_suff_idea_active = False

#     # WHEN
#     update_disc_grainunit = grainunit_shop("idea_reasonunit", grain_delete())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("base", knee_road)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("base", knee_road)


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_insert_idea_suffgroup():
#     # GIVEN

#     rico_text = "Rico"

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)

#     # WHEN
#     update_disc_grainunit = grainunit_shop("idea_suffgroup", grain_insert())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("group_id", rico_text)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("group_id", rico_text)


# def test_GrainUnit_get_description_ReturnsCorrectObj_AgendaUnit_delete_idea_suffgroup():
#     # GIVEN

#     rico_text = "Rico"

#     sports_text = "sports"
#     sports_road = create_road("a", sports_text)
#     ball_text = "basketball"
#     ball_road = create_road(sports_road, ball_text)

#     # WHEN
#     update_disc_grainunit = grainunit_shop("idea_suffgroup", grain_delete())
#     update_disc_grainunit.set_locator("road", ball_road)
#     update_disc_grainunit.set_locator("group_id", rico_text)
#     update_disc_grainunit.set_required_arg("road", ball_road)
#     update_disc_grainunit.set_required_arg("group_id", rico_text)


# def test_LearnUnit_get_sue_learnunit_example1_ContainsGrainUnits():
#     # GIVEN
#     sue_text = get_single_roadnode("PersonRoad", get_sue_proad(), "PersonID")

#     rico_text = "Rico"
#     carm_text = "Carmen"
#     dizz_text = "Dizzy"

#     run_text = ",runners"
#     run_groupunit = groupunit_shop(run_text)
#     run_groupunit.set_partylink(partylink_shop(rico_text))
#     run_groupunit.set_partylink(partylink_shop(carm_text))
#     fly_text = ",flyers"
#     fly_groupunit = groupunit_shop(fly_text)
#     fly_groupunit.set_partylink(partylink_shop(rico_text))
#     fly_groupunit.set_partylink(partylink_shop(dizz_text))
