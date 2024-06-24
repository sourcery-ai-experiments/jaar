from src._road.road import get_terminus_node, get_parent_road
from src._truth.belief import balancelink_shop
from src._truth.other import otherlink_shop
from src._truth.reason_idea import factunit_shop
from src._truth.idea import ideaunit_shop
from src._truth.belief import beliefunit_shop
from src._truth.truth import truthunit_shop
from src.atom.quark import (
    quark_update,
    quark_delete,
    quark_insert,
    quarkunit_shop,
)
from src.atom.nuc import nucunit_shop
from src.atom.examples.example_nucs import get_nucunit_example1


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_SimplestScenario():
    # GIVEN
    ex1_nucunit = nucunit_shop()

    # WHEN
    sue_text = "Sue"
    sue_weight = 55
    before_sue_truthunit = truthunit_shop(sue_text, _weight=sue_weight)
    after_sue_truthunit = ex1_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    assert after_sue_truthunit._weight == sue_weight
    assert after_sue_truthunit == before_sue_truthunit


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnitSimpleAttrs():
    # GIVEN
    sue_nucunit = nucunit_shop()
    sue_text = "Sue"

    sue_weight = 44
    before_sue_truthunit = truthunit_shop(sue_text, _weight=sue_weight)

    category = "truthunit"
    x_quarkunit = quarkunit_shop(category, quark_update())
    new1_value = 55
    new1_arg = "_weight"
    x_quarkunit.set_optional_arg(new1_arg, new1_value)
    new2_value = 66
    new2_arg = "_max_tree_traverse"
    x_quarkunit.set_optional_arg(new2_arg, new2_value)
    new3_value = 77
    new3_arg = "_other_credor_pool"
    x_quarkunit.set_optional_arg(new3_arg, new3_value)
    new4_value = 88
    new4_arg = "_other_debtor_pool"
    x_quarkunit.set_optional_arg(new4_arg, new4_value)
    new5_value = "override"
    new5_arg = "_meld_strategy"
    x_quarkunit.set_optional_arg(new5_arg, new5_value)
    new6_value = 0.5
    new6_arg = "_pixel"
    x_quarkunit.set_optional_arg(new6_arg, new6_value)
    sue_nucunit.set_quarkunit(x_quarkunit)
    new7_value = 0.025
    new7_arg = "_penny"
    x_quarkunit.set_optional_arg(new7_arg, new7_value)
    sue_nucunit.set_quarkunit(x_quarkunit)

    # WHEN
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    print(f"{sue_nucunit.quarkunits.keys()=}")
    assert after_sue_truthunit._max_tree_traverse == new2_value
    assert after_sue_truthunit._other_credor_pool == new3_value
    assert after_sue_truthunit._other_debtor_pool == new4_value
    assert after_sue_truthunit._meld_strategy == new5_value
    assert after_sue_truthunit._weight == new1_value
    assert after_sue_truthunit._weight != before_sue_truthunit._weight
    assert after_sue_truthunit._pixel == new6_value
    assert after_sue_truthunit._pixel != before_sue_truthunit._pixel
    assert after_sue_truthunit._penny == new7_value
    assert after_sue_truthunit._penny != before_sue_truthunit._penny


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_delete_other():
    # GIVEN
    sue_nucunit = nucunit_shop()
    sue_text = "Sue"

    before_sue_truthunit = truthunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_truthunit.add_otherunit(rico_text)
    before_sue_truthunit.add_otherunit(carm_text)

    category = "truth_otherunit"
    x_quarkunit = quarkunit_shop(category, quark_delete())
    x_quarkunit.set_required_arg("other_id", carm_text)
    sue_nucunit.set_quarkunit(x_quarkunit)

    # WHEN
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    print(f"{sue_nucunit.quarkunits=}")
    assert after_sue_truthunit != before_sue_truthunit
    assert after_sue_truthunit.other_exists(rico_text)
    assert after_sue_truthunit.other_exists(carm_text) is False


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_insert_other():
    # GIVEN
    sue_nucunit = nucunit_shop()
    sue_text = "Sue"

    before_sue_truthunit = truthunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_truthunit.add_otherunit(rico_text)
    assert before_sue_truthunit.other_exists(rico_text)
    assert before_sue_truthunit.other_exists(carm_text) is False

    # WHEN
    category = "truth_otherunit"
    x_quarkunit = quarkunit_shop(category, quark_insert())
    x_quarkunit.set_required_arg("other_id", carm_text)
    x_credor_weight = 55
    x_debtor_weight = 66
    x_quarkunit.set_optional_arg("credor_weight", x_credor_weight)
    x_quarkunit.set_optional_arg("debtor_weight", x_debtor_weight)
    sue_nucunit.set_quarkunit(x_quarkunit)
    print(f"{sue_nucunit.quarkunits.keys()=}")
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    rico_otherunit = after_sue_truthunit.get_other(rico_text)
    carm_otherunit = after_sue_truthunit.get_other(carm_text)
    assert rico_otherunit != None
    assert carm_otherunit != None
    assert carm_otherunit.credor_weight == x_credor_weight
    assert carm_otherunit.debtor_weight == x_debtor_weight


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_update_other():
    # GIVEN
    sue_nucunit = nucunit_shop()
    sue_text = "Sue"

    before_sue_truthunit = truthunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_truthunit.add_otherunit(rico_text)
    assert before_sue_truthunit.get_other(rico_text).credor_weight == 1

    # WHEN
    category = "truth_otherunit"
    x_quarkunit = quarkunit_shop(category, quark_update())
    x_quarkunit.set_required_arg("other_id", rico_text)
    rico_credor_weight = 55
    x_quarkunit.set_optional_arg("credor_weight", rico_credor_weight)
    sue_nucunit.set_quarkunit(x_quarkunit)
    print(f"{sue_nucunit.quarkunits.keys()=}")
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    rico_other = after_sue_truthunit.get_other(rico_text)
    assert rico_other.credor_weight == rico_credor_weight


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_delete_otherlink():
    # GIVEN
    sue_text = "Sue"
    before_sue_truthunit = truthunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_truthunit.add_otherunit(rico_text)
    before_sue_truthunit.add_otherunit(carm_text)
    before_sue_truthunit.add_otherunit(dizz_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_otherlink(otherlink_shop(rico_text))
    run_beliefunit.set_otherlink(otherlink_shop(carm_text))
    fly_text = ",flyers"
    fly_beliefunit = beliefunit_shop(fly_text)
    fly_beliefunit.set_otherlink(otherlink_shop(rico_text))
    fly_beliefunit.set_otherlink(otherlink_shop(carm_text))
    fly_beliefunit.set_otherlink(otherlink_shop(dizz_text))
    before_sue_truthunit.set_beliefunit(run_beliefunit)
    before_sue_truthunit.set_beliefunit(fly_beliefunit)
    assert len(before_sue_truthunit.get_beliefunit(run_text)._others) == 2
    assert len(before_sue_truthunit.get_beliefunit(fly_text)._others) == 3

    # WHEN
    rico_quarkunit = quarkunit_shop("truth_belief_otherlink", quark_delete())
    rico_quarkunit.set_required_arg("belief_id", run_text)
    rico_quarkunit.set_required_arg("other_id", rico_text)
    # print(f"{rico_quarkunit=}")
    carm_quarkunit = quarkunit_shop("truth_belief_otherlink", quark_delete())
    carm_quarkunit.set_required_arg("belief_id", fly_text)
    carm_quarkunit.set_required_arg("other_id", carm_text)
    # print(f"{carm_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(rico_quarkunit)
    sue_nucunit.set_quarkunit(carm_quarkunit)
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    assert len(after_sue_truthunit.get_beliefunit(fly_text)._others) == 2
    assert len(after_sue_truthunit.get_beliefunit(run_text)._others) == 1


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_insert_otherlink():
    # GIVEN
    sue_text = "Sue"
    before_sue_truthunit = truthunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_truthunit.add_otherunit(rico_text)
    before_sue_truthunit.add_otherunit(carm_text)
    before_sue_truthunit.add_otherunit(dizz_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_otherlink(otherlink_shop(carm_text))
    before_sue_truthunit.set_beliefunit(run_beliefunit)
    assert len(before_sue_truthunit.get_beliefunit(run_text)._others) == 1

    # WHEN
    rico_quarkunit = quarkunit_shop("truth_belief_otherlink", quark_insert())
    rico_quarkunit.set_required_arg("belief_id", run_text)
    rico_quarkunit.set_required_arg("other_id", rico_text)
    rico_run_credor_weight = 17
    rico_quarkunit.set_optional_arg("credor_weight", rico_run_credor_weight)
    print(f"{rico_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(rico_quarkunit)
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    assert len(after_sue_truthunit.get_beliefunit(run_text)._others) == 2
    after_run_beliefunit = after_sue_truthunit.get_beliefunit(run_text)
    after_run_rico_otherlink = after_run_beliefunit.get_otherlink(rico_text)
    assert after_run_rico_otherlink != None
    assert after_run_rico_otherlink.credor_weight == rico_run_credor_weight


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_update_otherlink():
    # GIVEN
    sue_text = "Sue"
    before_sue_truthunit = truthunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_truthunit.add_otherunit(rico_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    old_rico_run_credor_weight = 3
    run_beliefunit.set_otherlink(otherlink_shop(rico_text, old_rico_run_credor_weight))
    before_sue_truthunit.set_beliefunit(run_beliefunit)
    before_run_beliefunit = before_sue_truthunit.get_beliefunit(run_text)
    before_run_rico_otherlink = before_run_beliefunit.get_otherlink(rico_text)
    assert before_run_rico_otherlink.credor_weight == old_rico_run_credor_weight
    assert before_run_rico_otherlink.debtor_weight == 1

    # WHEN
    rico_quarkunit = quarkunit_shop("truth_belief_otherlink", quark_update())
    rico_quarkunit.set_required_arg("belief_id", run_text)
    rico_quarkunit.set_required_arg("other_id", rico_text)
    new_rico_run_credor_weight = 7
    new_rico_run_debtor_weight = 11
    rico_quarkunit.set_optional_arg("credor_weight", new_rico_run_credor_weight)
    rico_quarkunit.set_optional_arg("debtor_weight", new_rico_run_debtor_weight)
    print(f"{rico_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(rico_quarkunit)
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    after_run_beliefunit = after_sue_truthunit.get_beliefunit(run_text)
    after_run_rico_otherlink = after_run_beliefunit.get_otherlink(rico_text)
    assert after_run_rico_otherlink.credor_weight == new_rico_run_credor_weight
    assert after_run_rico_otherlink.debtor_weight == new_rico_run_debtor_weight


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_delete_beliefunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_truthunit = truthunit_shop(sue_text)
    run_text = ",runners"
    fly_text = ",flyers"
    before_sue_truthunit.set_beliefunit(beliefunit_shop(fly_text))
    before_sue_truthunit.set_beliefunit(beliefunit_shop(run_text))
    assert before_sue_truthunit.get_beliefunit(run_text) != None
    assert before_sue_truthunit.get_beliefunit(fly_text) != None

    # WHEN
    x_quarkunit = quarkunit_shop("truth_beliefunit", quark_delete())
    print(f"{x_quarkunit=}")
    x_quarkunit.set_required_arg("belief_id", run_text)
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(x_quarkunit)
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    assert after_sue_truthunit.get_beliefunit(run_text) is None
    assert after_sue_truthunit.get_beliefunit(fly_text) != None


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_insert_beliefunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_truthunit = truthunit_shop(sue_text)
    run_text = ",runners"
    before_sue_truthunit.set_beliefunit(beliefunit_shop(run_text))
    fly_text = ",flyers"
    assert before_sue_truthunit.get_beliefunit(run_text) != None
    assert before_sue_truthunit.get_beliefunit(fly_text) is None

    # WHEN
    x_quarkunit = quarkunit_shop("truth_beliefunit", quark_insert())
    x_quarkunit.set_required_arg("belief_id", fly_text)
    print(f"{x_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(x_quarkunit)
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    assert after_sue_truthunit.get_beliefunit(run_text) != None
    assert after_sue_truthunit.get_beliefunit(fly_text) != None


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_update_beliefunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_truthunit = truthunit_shop(sue_text)
    run_text = ",runners"
    before_sue_truthunit.set_beliefunit(beliefunit_shop(run_text))

    # WHEN
    yao_text = "Yao"
    x_quarkunit = quarkunit_shop("truth_beliefunit", quark_update())
    x_quarkunit.set_required_arg("belief_id", run_text)
    print(f"{x_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(x_quarkunit)
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN # keep as proof functions do not fail with arguments above
    assert after_sue_truthunit != None


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_delete_beliefunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_truthunit = truthunit_shop(sue_text)
    run_text = ",runners"
    fly_text = ",flyers"
    before_sue_truthunit.set_beliefunit(beliefunit_shop(fly_text))
    before_sue_truthunit.set_beliefunit(beliefunit_shop(run_text))
    assert before_sue_truthunit.get_beliefunit(run_text) != None
    assert before_sue_truthunit.get_beliefunit(fly_text) != None

    # WHEN
    x_quarkunit = quarkunit_shop("truth_beliefunit", quark_delete())
    print(f"{x_quarkunit=}")
    x_quarkunit.set_required_arg("belief_id", run_text)
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(x_quarkunit)
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    assert after_sue_truthunit.get_beliefunit(run_text) is None
    assert after_sue_truthunit.get_beliefunit(fly_text) != None


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_delete_ideaunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_truthunit = truthunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_truthunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_truthunit.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_truthunit.make_road(sports_road, disc_text)
    before_sue_truthunit.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_truthunit.add_idea(ideaunit_shop(disc_text), sports_road)
    assert before_sue_truthunit.idea_exists(ball_road)
    assert before_sue_truthunit.idea_exists(disc_road)

    # WHEN
    delete_disc_quarkunit = quarkunit_shop("truth_ideaunit", quark_delete())
    delete_disc_quarkunit.set_required_arg(
        "label", get_terminus_node(disc_road, before_sue_truthunit._road_delimiter)
    )
    print(f"{disc_road=}")
    delete_disc_quarkunit.set_required_arg(
        "parent_road",
        get_parent_road(disc_road, before_sue_truthunit._road_delimiter),
    )
    print(f"{delete_disc_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(delete_disc_quarkunit)
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    assert after_sue_truthunit.idea_exists(ball_road)
    assert after_sue_truthunit.idea_exists(disc_road) is False


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_insert_ideaunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_truthunit = truthunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_truthunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_truthunit.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_truthunit.make_road(sports_road, disc_text)
    before_sue_truthunit.add_idea(ideaunit_shop(ball_text), sports_road)
    assert before_sue_truthunit.idea_exists(ball_road)
    assert before_sue_truthunit.idea_exists(disc_road) is False

    # WHEN
    # x_addin = 140
    # x_begin = 1000
    # x_close = 1700
    # x_denom = 17
    x_meld_strategy = "override"
    x_numeric_road = None
    # x_numor = 10
    x_pledge = True
    insert_disc_quarkunit = quarkunit_shop("truth_ideaunit", quark_insert())
    insert_disc_quarkunit.set_required_arg("label", disc_text)
    insert_disc_quarkunit.set_required_arg("parent_road", sports_road)
    # insert_disc_quarkunit.set_optional_arg("_addin", x_addin)
    # insert_disc_quarkunit.set_optional_arg("_begin", x_begin)
    # insert_disc_quarkunit.set_optional_arg("_close", x_close)
    # insert_disc_quarkunit.set_optional_arg("_denom", x_denom)
    insert_disc_quarkunit.set_optional_arg("_meld_strategy", x_meld_strategy)
    insert_disc_quarkunit.set_optional_arg("_numeric_road", x_numeric_road)
    # insert_disc_quarkunit.set_optional_arg("_numor", x_numor)
    insert_disc_quarkunit.set_optional_arg("pledge", x_pledge)

    print(f"{insert_disc_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(insert_disc_quarkunit)
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    assert after_sue_truthunit.idea_exists(ball_road)
    assert after_sue_truthunit.idea_exists(disc_road)


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_update_ideaunit_SimpleAttributes():
    # GIVEN
    sue_text = "Sue"
    before_sue_truthunit = truthunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_truthunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_truthunit.make_road(sports_road, ball_text)
    before_sue_truthunit.add_idea(ideaunit_shop(ball_text), sports_road)
    assert before_sue_truthunit.get_idea_obj(ball_road)._begin is None
    assert before_sue_truthunit.get_idea_obj(ball_road)._close is None
    assert before_sue_truthunit.get_idea_obj(ball_road)._meld_strategy == "default"
    assert before_sue_truthunit.get_idea_obj(ball_road).pledge is False

    # WHEN
    # x_addin = 140
    x_begin = 1000
    x_close = 1700
    # x_denom = 17
    x_meld_strategy = "override"
    # x_numor = 10
    x_pledge = True
    insert_disc_quarkunit = quarkunit_shop("truth_ideaunit", quark_update())
    insert_disc_quarkunit.set_required_arg("label", ball_text)
    insert_disc_quarkunit.set_required_arg("parent_road", sports_road)
    # insert_disc_quarkunit.set_optional_arg("_addin", x_addin)
    insert_disc_quarkunit.set_optional_arg("_begin", x_begin)
    insert_disc_quarkunit.set_optional_arg("_close", x_close)
    # insert_disc_quarkunit.set_optional_arg("_denom", x_denom)
    insert_disc_quarkunit.set_optional_arg("_meld_strategy", x_meld_strategy)
    # insert_disc_quarkunit.set_optional_arg("_numor", x_numor)
    insert_disc_quarkunit.set_optional_arg("pledge", x_pledge)

    print(f"{insert_disc_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(insert_disc_quarkunit)
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    assert after_sue_truthunit.get_idea_obj(ball_road)._begin == x_begin
    assert after_sue_truthunit.get_idea_obj(ball_road)._close == x_close
    assert after_sue_truthunit.get_idea_obj(ball_road)._meld_strategy == x_meld_strategy
    assert after_sue_truthunit.get_idea_obj(ball_road).pledge


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_delete_idea_balancelink():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_au.add_otherunit(rico_text)
    before_sue_au.add_otherunit(carm_text)
    before_sue_au.add_otherunit(dizz_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_otherlink(otherlink_shop(rico_text))
    run_beliefunit.set_otherlink(otherlink_shop(carm_text))
    fly_text = ",flyers"
    fly_beliefunit = beliefunit_shop(fly_text)
    fly_beliefunit.set_otherlink(otherlink_shop(rico_text))
    fly_beliefunit.set_otherlink(otherlink_shop(carm_text))
    fly_beliefunit.set_otherlink(otherlink_shop(dizz_text))
    before_sue_au.set_beliefunit(run_beliefunit)
    before_sue_au.set_beliefunit(fly_beliefunit)
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
    delete_disc_quarkunit = quarkunit_shop("truth_idea_balancelink", quark_delete())
    delete_disc_quarkunit.set_required_arg("road", disc_road)
    delete_disc_quarkunit.set_required_arg("belief_id", fly_text)
    print(f"{delete_disc_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(delete_disc_quarkunit)
    after_sue_truthunit = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    assert len(after_sue_truthunit.get_idea_obj(ball_road)._balancelinks) == 2
    assert len(after_sue_truthunit.get_idea_obj(disc_road)._balancelinks) == 1


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_update_idea_balancelink():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_au.add_otherunit(rico_text)
    before_sue_au.add_otherunit(carm_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_otherlink(otherlink_shop(rico_text))
    before_sue_au.set_beliefunit(run_beliefunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_au.edit_idea_attr(ball_road, balancelink=balancelink_shop(run_text))
    run_balancelink = before_sue_au.get_idea_obj(ball_road)._balancelinks.get(run_text)
    assert run_balancelink.credor_weight == 1
    assert run_balancelink.debtor_weight == 1

    # WHEN
    x_credor_weight = 55
    x_debtor_weight = 66
    update_disc_quarkunit = quarkunit_shop("truth_idea_balancelink", quark_update())
    update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("belief_id", run_text)
    update_disc_quarkunit.set_optional_arg("credor_weight", x_credor_weight)
    update_disc_quarkunit.set_optional_arg("debtor_weight", x_debtor_weight)
    # print(f"{update_disc_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(update_disc_quarkunit)
    after_sue_au = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    run_balancelink = after_sue_au.get_idea_obj(ball_road)._balancelinks.get(run_text)
    print(f"{run_balancelink.credor_weight=}")
    assert run_balancelink.credor_weight == x_credor_weight
    assert run_balancelink.debtor_weight == x_debtor_weight


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_insert_idea_balancelink():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_au.add_otherunit(rico_text)
    before_sue_au.add_otherunit(carm_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_otherlink(otherlink_shop(rico_text))
    before_sue_au.set_beliefunit(run_beliefunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea._balancelinks.get(run_text) is None

    # WHEN
    x_credor_weight = 55
    x_debtor_weight = 66
    update_disc_quarkunit = quarkunit_shop("truth_idea_balancelink", quark_insert())
    update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("belief_id", run_text)
    update_disc_quarkunit.set_optional_arg("credor_weight", x_credor_weight)
    update_disc_quarkunit.set_optional_arg("debtor_weight", x_debtor_weight)
    # print(f"{update_disc_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(update_disc_quarkunit)
    after_sue_au = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._balancelinks.get(run_text) != None


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_insert_idea_factunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
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
    assert before_ball_idea._factunits == {}

    # WHEN
    broken_open = 55
    broken_nigh = 66
    update_disc_quarkunit = quarkunit_shop("truth_idea_factunit", quark_insert())
    update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("base", knee_road)
    update_disc_quarkunit.set_optional_arg("pick", broken_road)
    update_disc_quarkunit.set_optional_arg("open", broken_open)
    update_disc_quarkunit.set_optional_arg("nigh", broken_nigh)
    # print(f"{update_disc_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(update_disc_quarkunit)
    after_sue_au = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._factunits != {}
    assert after_ball_idea._factunits.get(knee_road) != None
    assert after_ball_idea._factunits.get(knee_road).base == knee_road
    assert after_ball_idea._factunits.get(knee_road).pick == broken_road
    assert after_ball_idea._factunits.get(knee_road).open == broken_open
    assert after_ball_idea._factunits.get(knee_road).nigh == broken_nigh


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_delete_idea_factunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
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
        road=ball_road, factunit=factunit_shop(base=knee_road, pick=broken_road)
    )
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea._factunits != {}
    assert before_ball_idea._factunits.get(knee_road) != None

    # WHEN
    update_disc_quarkunit = quarkunit_shop("truth_idea_factunit", quark_delete())
    update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("base", knee_road)
    # print(f"{update_disc_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(update_disc_quarkunit)
    after_sue_au = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._factunits == {}


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_update_idea_factunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
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
    before_knee_factunit = factunit_shop(knee_road, broken_road)
    before_sue_au.edit_idea_attr(ball_road, factunit=before_knee_factunit)
    before_ball_idea = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_idea._factunits != {}
    assert before_ball_idea._factunits.get(knee_road) != None
    assert before_ball_idea._factunits.get(knee_road).pick == broken_road
    assert before_ball_idea._factunits.get(knee_road).open is None
    assert before_ball_idea._factunits.get(knee_road).nigh is None

    # WHEN
    medical_open = 45
    medical_nigh = 77
    update_disc_quarkunit = quarkunit_shop("truth_idea_factunit", quark_update())
    update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("base", knee_road)
    update_disc_quarkunit.set_optional_arg("pick", medical_road)
    update_disc_quarkunit.set_optional_arg("open", medical_open)
    update_disc_quarkunit.set_optional_arg("nigh", medical_nigh)
    # print(f"{update_disc_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(update_disc_quarkunit)
    after_sue_au = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea._factunits != {}
    assert after_ball_idea._factunits.get(knee_road) != None
    assert after_ball_idea._factunits.get(knee_road).pick == medical_road
    assert after_ball_idea._factunits.get(knee_road).open == medical_open
    assert after_ball_idea._factunits.get(knee_road).nigh == medical_nigh


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_update_idea_reason_premiseunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
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
    update_disc_quarkunit = quarkunit_shop(
        "truth_idea_reason_premiseunit", quark_update()
    )
    update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("base", knee_road)
    update_disc_quarkunit.set_required_arg("need", broken_road)
    update_disc_quarkunit.set_optional_arg("open", broken_open)
    update_disc_quarkunit.set_optional_arg("nigh", broken_nigh)
    update_disc_quarkunit.set_optional_arg("divisor", broken_divisor)
    # print(f"{update_disc_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(update_disc_quarkunit)
    after_sue_au = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit != None
    after_broken_premiseunit = after_knee_reasonunit.get_premise(broken_road)
    assert after_broken_premiseunit.need == broken_road
    assert after_broken_premiseunit.open == broken_open
    assert after_broken_premiseunit.nigh == broken_nigh
    assert after_broken_premiseunit.divisor == broken_divisor


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_insert_idea_reason_premiseunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
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
    update_disc_quarkunit = quarkunit_shop(
        "truth_idea_reason_premiseunit", quark_insert()
    )
    update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("base", knee_road)
    update_disc_quarkunit.set_required_arg("need", medical_road)
    update_disc_quarkunit.set_optional_arg("open", medical_open)
    update_disc_quarkunit.set_optional_arg("nigh", medical_nigh)
    update_disc_quarkunit.set_optional_arg("divisor", medical_divisor)
    # print(f"{update_disc_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(update_disc_quarkunit)
    after_sue_au = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    after_medical_premiseunit = after_knee_reasonunit.get_premise(medical_road)
    assert after_medical_premiseunit != None
    assert after_medical_premiseunit.need == medical_road
    assert after_medical_premiseunit.open == medical_open
    assert after_medical_premiseunit.nigh == medical_nigh
    assert after_medical_premiseunit.divisor == medical_divisor


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_delete_idea_reason_premiseunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
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
    update_disc_quarkunit = quarkunit_shop(
        "truth_idea_reason_premiseunit", quark_delete()
    )
    update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("base", knee_road)
    update_disc_quarkunit.set_required_arg("need", medical_road)
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(update_disc_quarkunit)
    after_sue_au = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit.get_premise(broken_road) != None
    assert after_knee_reasonunit.get_premise(medical_road) is None


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_insert_idea_reasonunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
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
    update_disc_quarkunit = quarkunit_shop("truth_idea_reasonunit", quark_insert())
    update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("base", knee_road)
    update_disc_quarkunit.set_optional_arg("suff_idea_active", medical_suff_idea_active)
    # print(f"{update_disc_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(update_disc_quarkunit)
    after_sue_au = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit != None
    assert after_knee_reasonunit.get_premise(medical_road) is None
    assert after_knee_reasonunit.suff_idea_active == medical_suff_idea_active


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_update_idea_reasonunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
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
    update_disc_quarkunit = quarkunit_shop("truth_idea_reasonunit", quark_update())
    update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("base", knee_road)
    update_disc_quarkunit.set_optional_arg(
        "suff_idea_active", after_medical_suff_idea_active
    )
    # print(f"{update_disc_quarkunit=}")
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(update_disc_quarkunit)
    after_sue_au = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    after_knee_reasonunit = after_ball_idea.get_reasonunit(knee_road)
    assert after_knee_reasonunit != None
    assert after_knee_reasonunit.get_premise(medical_road) is None
    assert after_knee_reasonunit.suff_idea_active == after_medical_suff_idea_active


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_delete_idea_reasonunit():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
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
    update_disc_quarkunit = quarkunit_shop("truth_idea_reasonunit", quark_delete())
    update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("base", knee_road)
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(update_disc_quarkunit)
    after_sue_au = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    after_ball_idea = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_idea.get_reasonunit(knee_road) is None


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_insert_idea_suffbelief():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_au.add_otherunit(rico_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_ideaunit = before_sue_au.get_idea_obj(ball_road)
    assert before_ball_ideaunit._assignedunit._suffbeliefs == {}

    # WHEN
    update_disc_quarkunit = quarkunit_shop("truth_idea_suffbelief", quark_insert())
    update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("belief_id", rico_text)
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(update_disc_quarkunit)
    after_sue_au = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    after_ball_ideaunit = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_ideaunit._assignedunit._suffbeliefs != {}
    assert after_ball_ideaunit._assignedunit.get_suffbelief(rico_text) != None


def test_NucUnit_get_edited_truth_ReturnsCorrectObj_TruthUnit_delete_idea_suffbelief():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = truthunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_au.add_otherunit(rico_text)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_ideaunit = before_sue_au.get_idea_obj(ball_road)
    before_ball_ideaunit._assignedunit.set_suffbelief(rico_text)
    assert before_ball_ideaunit._assignedunit._suffbeliefs != {}
    assert before_ball_ideaunit._assignedunit.get_suffbelief(rico_text) != None

    # WHEN
    update_disc_quarkunit = quarkunit_shop("truth_idea_suffbelief", quark_delete())
    update_disc_quarkunit.set_required_arg("road", ball_road)
    update_disc_quarkunit.set_required_arg("belief_id", rico_text)
    sue_nucunit = nucunit_shop()
    sue_nucunit.set_quarkunit(update_disc_quarkunit)
    print(f"{before_sue_au.get_idea_obj(ball_road)._assignedunit=}")
    after_sue_au = sue_nucunit.get_edited_truth(before_sue_au)

    # THEN
    after_ball_ideaunit = after_sue_au.get_idea_obj(ball_road)
    assert after_ball_ideaunit._assignedunit._suffbeliefs == {}


def test_NucUnit_get_nucunit_example1_ContainsQuarkUnits():
    # GIVEN
    sue_text = "Sue"
    before_sue_truthunit = truthunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_truthunit.add_otherunit(rico_text)
    before_sue_truthunit.add_otherunit(carm_text)
    before_sue_truthunit.add_otherunit(dizz_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_otherlink(otherlink_shop(rico_text))
    run_beliefunit.set_otherlink(otherlink_shop(carm_text))
    fly_text = ",flyers"
    fly_beliefunit = beliefunit_shop(fly_text)
    fly_beliefunit.set_otherlink(otherlink_shop(rico_text))
    fly_beliefunit.set_otherlink(otherlink_shop(dizz_text))
    before_sue_truthunit.set_beliefunit(run_beliefunit)
    before_sue_truthunit.set_beliefunit(fly_beliefunit)
    assert before_sue_truthunit._weight != 55
    assert before_sue_truthunit._max_tree_traverse != 66
    assert before_sue_truthunit._other_credor_pool != 77
    assert before_sue_truthunit._other_debtor_pool != 88
    assert before_sue_truthunit._meld_strategy != "override"
    assert before_sue_truthunit.other_exists(rico_text)
    assert before_sue_truthunit.other_exists(carm_text)
    assert before_sue_truthunit.get_beliefunit(run_text) != None
    assert before_sue_truthunit.get_beliefunit(fly_text) != None

    # WHEN
    ex1_nucunit = get_nucunit_example1()
    after_sue_truthunit = ex1_nucunit.get_edited_truth(before_sue_truthunit)

    # THEN
    assert after_sue_truthunit._weight == 55
    assert after_sue_truthunit._max_tree_traverse == 66
    assert after_sue_truthunit._other_credor_pool == 77
    assert after_sue_truthunit._other_debtor_pool == 88
    assert after_sue_truthunit._meld_strategy == "override"
    assert after_sue_truthunit.other_exists(rico_text)
    assert after_sue_truthunit.other_exists(carm_text) is False
