from src._truth.reason_assign import assigned_heir_shop, assignedunit_shop
from src._truth.truth import truthunit_shop
from src._truth.idea import ideaunit_shop
from src._truth.belief import beliefunit_shop


def test_truth_edit_idea_attr_CorrectlySetsAssignedUnit():
    # GIVEN
    xio_truth = truthunit_shop("Xio")
    run_text = "run"
    run_road = xio_truth.make_l1_road(run_text)
    xio_truth.add_l1_idea(ideaunit_shop(run_text))
    run_idea = xio_truth.get_idea_obj(run_road)
    assert run_idea._assignedunit == assignedunit_shop()

    # WHEN
    assignedunit_x = assignedunit_shop()
    xio_truth.edit_idea_attr(assignedunit=assignedunit_x, road=run_road)

    # THEN
    assert run_idea._assignedunit == assignedunit_x


def test_truth_idearoot_assignedunit_CorrectlySets_idea_assignedheir():
    # GIVEN
    assignedunit_x = assignedunit_shop()

    tim_truth = truthunit_shop("Tim")
    tim_truth.edit_idea_attr(assignedunit=assignedunit_x, road=tim_truth._real_id)
    assert tim_truth._idearoot._assignedunit == assignedunit_x
    assert tim_truth._idearoot._assignedheir is None

    # WHEN
    tim_truth.calc_truth_metrics()

    # THEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffbeliefs(
        parent_assignheir=None, assignunit=assignedunit_x, truth_beliefs=None
    )
    assert tim_truth._idearoot._assignedheir != None
    assert tim_truth._idearoot._assignedheir == assigned_heir_x


def test_truth_ideakid_assignedunit_EmptyCorrectlySets_idea_assignedheir():
    # GIVEN
    bob_text = "Bob"
    assignedunit_x = assignedunit_shop()

    bob_truth = truthunit_shop(bob_text)
    run_text = "run"
    run_road = bob_truth.make_road(bob_text, run_text)
    bob_truth.add_otherunit(other_id=bob_text)
    bob_truth.add_l1_idea(ideaunit_shop(run_text))
    bob_truth.edit_idea_attr(road=run_road, assignedunit=assignedunit_x)
    run_idea = bob_truth.get_idea_obj(run_road)
    assert run_idea._assignedunit == assignedunit_x
    assert run_idea._assignedheir is None

    # WHEN
    bob_truth.calc_truth_metrics()

    # THEN
    assert run_idea._assignedheir != None
    assert run_idea._assignedheir._owner_id_assigned is False

    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffbeliefs(
        parent_assignheir=None,
        assignunit=assignedunit_x,
        truth_beliefs=bob_truth._beliefs,
    )
    print(f"{assigned_heir_x._owner_id_assigned=}")
    assert (
        run_idea._assignedheir._owner_id_assigned == assigned_heir_x._owner_id_assigned
    )
    assert run_idea._assignedheir == assigned_heir_x


def test_truth_ideakid_assignedunit_CorrectlySets_grandchild_idea_assignedheir():
    # GIVEN
    noa_truth = truthunit_shop("Noa")
    swim_text = "swimming"
    swim_road = noa_truth.make_l1_road(swim_text)
    morn_text = "morning"
    morn_road = noa_truth.make_road(swim_road, morn_text)
    four_text = "fourth"
    four_road = noa_truth.make_road(morn_road, four_text)
    assignedunit_x = assignedunit_shop()
    swimmers_text = ",swimmers"
    assignedunit_x.set_suffbelief(belief_id=swimmers_text)

    noa_truth.set_beliefunit(y_beliefunit=beliefunit_shop(belief_id=swimmers_text))
    noa_truth.add_l1_idea(ideaunit_shop(swim_text))
    noa_truth.add_idea(ideaunit_shop(morn_text), parent_road=swim_road)
    noa_truth.add_idea(ideaunit_shop(four_text), parent_road=morn_road)
    noa_truth.edit_idea_attr(road=swim_road, assignedunit=assignedunit_x)
    # print(noa_truth.make_road(four_road=}\n{morn_road=))
    four_idea = noa_truth.get_idea_obj(four_road)
    assert four_idea._assignedunit == assignedunit_shop()
    assert four_idea._assignedheir is None

    # WHEN
    noa_truth.calc_truth_metrics()

    # THEN
    assigned_heir_x = assigned_heir_shop()
    assigned_heir_x.set_suffbeliefs(
        parent_assignheir=None,
        assignunit=assignedunit_x,
        truth_beliefs=noa_truth._beliefs,
    )
    assert four_idea._assignedheir != None
    assert four_idea._assignedheir == assigned_heir_x


def test_TruthUnit__get_filtered_balancelinks_idea_CorrectlyFiltersIdea_AssignUnit():
    # GIVEN
    noa_text = "Noa"
    noa1_truth = truthunit_shop(noa_text)
    xia_text = "Xia"
    zoa_text = "Zoa"
    noa1_truth.add_otherunit(other_id=xia_text)
    noa1_truth.add_otherunit(other_id=zoa_text)

    casa_text = "casa"
    casa_road = noa1_truth.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = noa1_truth.make_l1_road(swim_text)
    noa1_truth.add_idea(ideaunit_shop(casa_text), parent_road=noa1_truth._real_id)
    noa1_truth.add_idea(ideaunit_shop(swim_text), parent_road=noa1_truth._real_id)
    swim_assignedunit = assignedunit_shop()
    swim_assignedunit.set_suffbelief(belief_id=xia_text)
    swim_assignedunit.set_suffbelief(belief_id=zoa_text)
    noa1_truth.edit_idea_attr(road=swim_road, assignedunit=swim_assignedunit)
    noa1_truth_swim_idea = noa1_truth.get_idea_obj(swim_road)
    noa1_truth_swim_suffbeliefs = noa1_truth_swim_idea._assignedunit._suffbeliefs
    assert len(noa1_truth_swim_suffbeliefs) == 2

    # WHEN
    noa2_truth = truthunit_shop(noa_text)
    noa2_truth.add_otherunit(other_id=xia_text)
    filtered_idea = noa2_truth._get_filtered_balancelinks_idea(noa1_truth_swim_idea)

    # THEN
    filtered_swim_suffbeliefs = filtered_idea._assignedunit._suffbeliefs
    assert len(filtered_swim_suffbeliefs) == 1
    assert list(filtered_swim_suffbeliefs) == [xia_text]


def test_TruthUnit_add_idea_CorrectlyFiltersIdea_balancelinks():
    # GIVEN
    noa1_truth = truthunit_shop("Noa")
    xia_text = "Xia"
    zoa_text = "Zoa"
    noa1_truth.add_otherunit(other_id=xia_text)
    noa1_truth.add_otherunit(other_id=zoa_text)

    casa_text = "casa"
    casa_road = noa1_truth.make_l1_road(casa_text)
    swim_text = "swim"
    swim_road = noa1_truth.make_l1_road(swim_text)
    noa1_truth.add_idea(ideaunit_shop(casa_text), parent_road=noa1_truth._real_id)
    noa1_truth.add_idea(ideaunit_shop(swim_text), parent_road=noa1_truth._real_id)
    swim_assignedunit = assignedunit_shop()
    swim_assignedunit.set_suffbelief(belief_id=xia_text)
    swim_assignedunit.set_suffbelief(belief_id=zoa_text)
    noa1_truth.edit_idea_attr(road=swim_road, assignedunit=swim_assignedunit)
    noa1_truth_swim_idea = noa1_truth.get_idea_obj(swim_road)
    noa1_truth_swim_suffbeliefs = noa1_truth_swim_idea._assignedunit._suffbeliefs
    assert len(noa1_truth_swim_suffbeliefs) == 2

    # WHEN
    noa2_truth = truthunit_shop("Noa")
    noa2_truth.add_otherunit(other_id=xia_text)
    noa2_truth.add_l1_idea(noa1_truth_swim_idea, create_missing_beliefs=False)

    # THEN
    noa2_truth_swim_idea = noa2_truth.get_idea_obj(swim_road)
    noa2_truth_swim_suffbeliefs = noa2_truth_swim_idea._assignedunit._suffbeliefs
    assert len(noa2_truth_swim_suffbeliefs) == 1
    assert list(noa2_truth_swim_suffbeliefs) == [xia_text]
