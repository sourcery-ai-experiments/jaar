from src._truth.idea import ideaunit_shop
from src._truth.truth import truthunit_shop
from src._truth.belief import beliefunit_shop
from src._truth.other import otherunit_shop, otherlink_shop
from src._truth.origin import originunit_shop
from pytest import raises as pytest_raises
from src._truth.examples.example_truths import truth_v001


def test_TruthUnit_meld_BaseScenario():
    # GIVEN
    bob_text = "Bob"
    bob1_truth = truthunit_shop(bob_text)
    bob2_truth = truthunit_shop(bob_text)
    assert bob1_truth
    assert bob1_truth._owner_id == bob_text

    # WHEN
    bob1_truth.meld(exterior_truth=bob2_truth)

    # THEN
    assert bob1_truth
    assert bob1_truth._owner_id == bob_text


def test_TruthUnit_meld_WeightDoesNotCombine():
    # GIVEN
    bob_text = "Bob"
    bob1_truth = truthunit_shop(bob_text)
    bob1_truth._weight = 3
    bob2_truth = truthunit_shop(bob_text)
    bob2_truth._weight = 5
    assert bob1_truth._weight == 3

    # WHEN
    bob1_truth.meld(exterior_truth=bob2_truth)

    # THEN
    assert bob1_truth._weight == 3


def test_TruthUnit_meld_OtherUnits():
    # GIVEN
    yao_text = "Yao"
    yao_otherunit = otherunit_shop(other_id=yao_text)

    bob_text = "Bob"
    bob1_truth = truthunit_shop(bob_text)
    bob1_truth.set_otherunit(yao_otherunit)

    bob2_truth = truthunit_shop(bob_text)
    bob2_truth.set_otherunit(yao_otherunit)
    zia_text = "Zia"
    zia_otherunit = otherunit_shop(other_id=zia_text)
    bob2_truth.set_otherunit(zia_otherunit)
    assert len(bob1_truth._others) == 1
    assert bob1_truth.other_exists(yao_text)
    assert bob1_truth.other_exists(zia_text) is False

    # WHEN
    bob1_truth.meld(exterior_truth=bob2_truth)

    # THEN
    assert len(bob1_truth._others) == 2
    assert bob1_truth.other_exists(yao_text)
    assert bob1_truth.other_exists(zia_text)


def test_TruthUnit_meld_OtherUnits_ignore_otherunits_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_otherunit = otherunit_shop(other_id=yao_text)

    bob_text = "Bob"
    bob1_truth = truthunit_shop(bob_text)
    bob1_truth.set_otherunit(yao_otherunit)

    bob2_truth = truthunit_shop(bob_text)
    bob2_truth.set_otherunit(yao_otherunit)
    zia_text = "Zia"
    zia_otherunit = otherunit_shop(other_id=zia_text)
    bob2_truth.set_otherunit(zia_otherunit)
    assert len(bob1_truth._others) == 1
    assert bob1_truth.other_exists(yao_text)
    assert bob1_truth.other_exists(zia_text) is False

    # WHEN
    bob1_truth.meld(exterior_truth=bob2_truth, ignore_otherunits=True)

    # THEN
    assert len(bob1_truth._others) == 1
    assert bob1_truth.other_exists(yao_text)
    assert bob1_truth.other_exists(zia_text) is False


def test_TruthUnit_meld_BeliefUnits_WhereBeliefUnitIsMissing():
    # GIVEN
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(belief_id=run_text)

    bob_text = "Bob"
    bob1_truth = truthunit_shop(bob_text)
    bob1_truth.set_beliefunit(run_beliefunit)

    bob2_truth = truthunit_shop(bob_text)
    bob2_truth.set_beliefunit(run_beliefunit)
    swim_text = ",swimmers"
    swim_beliefunit = beliefunit_shop(belief_id=swim_text)
    bob2_truth.set_beliefunit(swim_beliefunit)
    assert len(bob1_truth._beliefs) == 1
    assert bob1_truth.get_beliefunit(run_text) != None
    assert bob1_truth.get_beliefunit(swim_text) is None

    # WHEN
    bob1_truth.meld(exterior_truth=bob2_truth)

    # THEN
    # for x_belief_id in bob1_truth._beliefs.values():
    #     print(f"bob1_truth {x_belief_id.other_id=}")

    assert len(bob1_truth._beliefs) == 2
    assert bob1_truth.get_beliefunit(run_text) != None
    assert bob1_truth.get_beliefunit(swim_text) != None


def test_TruthUnit_meld_BeliefUnits_WhereBeliefUnitMembershipIsDifferent():
    # GIVEN

    bob_text = "Bob"
    bob1_truth = truthunit_shop(bob_text)
    sue_text = "Sue"
    bob1_truth.set_otherunit(otherunit_shop(sue_text))

    run_text = ",runners"
    bob1_truth.set_beliefunit(beliefunit_shop(run_text))
    bob1_truth.get_beliefunit(run_text).set_otherlink(otherlink_shop(sue_text))

    bob2_truth = truthunit_shop(bob_text)
    yao_text = "Yao"
    bob2_truth.set_otherunit(otherunit_shop(yao_text))
    bob2_truth.set_otherunit(otherunit_shop(sue_text))
    bob2_truth.set_beliefunit(beliefunit_shop(run_text))
    bob2_truth.get_beliefunit(run_text).set_otherlink(otherlink_shop(yao_text))
    bob2_truth.get_beliefunit(run_text).set_otherlink(otherlink_shop(sue_text))
    assert len(bob1_truth._beliefs) == 2
    assert len(bob1_truth.get_beliefunit(run_text)._others) == 1

    # WHEN
    bob1_truth.meld(exterior_truth=bob2_truth)

    # THEN
    assert len(bob1_truth._beliefs) == 3
    assert len(bob1_truth.get_beliefunit(run_text)._others) == 2


def test_TruthUnit_idearoot_meld_idearoot_AttrCorrectlyMelded():
    # GIVEN
    bob_text = "Bob"
    bob1_truth = truthunit_shop(bob_text)
    bob2_truth = truthunit_shop(bob_text)
    bob2_truth._idearoot._uid = 4
    assert bob1_truth._idearoot._uid == 1
    assert bob2_truth._idearoot._uid == 4

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        bob1_truth.meld(bob2_truth)
    assert (
        str(excinfo.value)
        == f"Meld fail idea={bob1_truth._real_id} _uid:1 with {bob2_truth._real_id} _uid:4"
    )


def test_TruthUnit_idearoot_meld_Add4IdeasScenario():
    # GIVEN
    bob_text = "Bob"
    bob1_truth = truthunit_shop(bob_text)

    tech_text = "tech"
    tech_road = bob1_truth.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = bob1_truth.make_road(tech_road, bowl_text)
    swim_text = "swim"
    swim_road = bob1_truth.make_l1_road(swim_text)
    free_text = "freestyle"
    free_road = bob1_truth.make_road(swim_road, free_text)

    bob2_truth = truthunit_shop(bob_text)
    bob2_truth.add_l1_idea(ideaunit_shop(tech_text))
    bob2_truth.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob2_truth.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    assert len(bob1_truth.get_idea_dict()) == 1
    assert bob1_truth.idea_exists(tech_road) is False
    assert bob1_truth.idea_exists(bowl_road) is False
    assert bob1_truth.idea_exists(swim_road) is False
    assert bob1_truth.idea_exists(free_road) is False

    # WHEN
    bob1_truth.meld(bob2_truth)

    # THEN
    assert len(bob1_truth.get_idea_dict()) == 5
    assert bob1_truth.idea_exists(tech_road)
    assert bob1_truth.idea_exists(bowl_road)
    assert bob1_truth.idea_exists(swim_road)
    assert bob1_truth.idea_exists(free_road)
    assert bob1_truth.get_idea_obj(tech_road)._label == tech_text
    assert bob1_truth.get_idea_obj(bowl_road)._label == bowl_text
    assert bob1_truth.get_idea_obj(swim_road)._label == swim_text
    assert bob1_truth.get_idea_obj(free_road)._label == free_text


def test_TruthUnit_idearoot_meld_2EqualIdeasScenario():
    # GIVEN
    yao_text = "Yao"
    yao1_truth = truthunit_shop(yao_text)
    tech_text = "tech"
    tech_road = yao1_truth.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = yao1_truth.make_road(tech_road, bowl_text)

    yao1_truth.add_l1_idea(ideaunit_shop(tech_text))
    yao1_truth.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)

    yao2_truth = truthunit_shop(yao_text)
    yao2_truth.add_l1_idea(ideaunit_shop(tech_text))
    yao2_truth.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    assert yao1_truth.get_idea_obj(bowl_road)._weight == 1
    assert len(yao1_truth.get_idea_dict()) == 3

    # WHEN
    yao1_truth.meld(yao2_truth)

    # THEN
    assert yao1_truth.get_idea_obj(bowl_road)._weight == 1
    assert len(yao1_truth.get_idea_dict()) == 3


def test_TruthUnit_factunits_meld_ReturnsCorrectObj_BaseScenario():
    # GIVEN
    bob_text = "Bob"
    bob1_truth = truthunit_shop(bob_text)
    tech_text = "tech"
    tech_road = bob1_truth.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = bob1_truth.make_road(tech_road, bowl_text)

    bob1_truth.add_l1_idea(ideaunit_shop(tech_text))
    bob1_truth.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob1_truth.set_fact(base=tech_road, pick=bowl_road)

    bob2_truth = truthunit_shop(bob_text)
    bob2_truth.add_l1_idea(ideaunit_shop(tech_text))
    bob2_truth.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob2_truth.set_fact(base=tech_road, pick=bowl_road)
    bob1_idearoot = bob1_truth._idearoot
    bob2_idearoot = bob2_truth._idearoot
    assert len(bob1_idearoot._factunits) == 1
    assert len(bob1_idearoot._factunits) == len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits == bob2_idearoot._factunits

    # WHEN
    bob1_truth.meld(bob2_truth)

    # THEN
    assert len(bob1_idearoot._factunits) == 1
    assert len(bob1_idearoot._factunits) == len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits == bob2_idearoot._factunits


def test_TruthUnit_factunits_meld_ReturnsCorrectObj_2FactUnits():
    # GIVEN
    bob_text = "Bob"
    bob1_truth = truthunit_shop(bob_text)
    tech_text = "tech"
    tech_road = bob1_truth.make_l1_road(tech_text)
    bowl_text = "bowl"
    bowl_road = bob1_truth.make_road(tech_road, bowl_text)
    swim_text = "swim"
    swim_road = bob1_truth.make_l1_road(swim_text)
    free_text = "freestyle"

    bob1_truth.add_l1_idea(ideaunit_shop(tech_text))
    bob1_truth.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob1_truth.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    bob1_truth.set_fact(base=tech_road, pick=bowl_road)

    bob2_truth = truthunit_shop(bob_text)
    bob2_truth.add_l1_idea(ideaunit_shop(tech_text))
    bob2_truth.add_idea(ideaunit_shop(bowl_text), parent_road=tech_road)
    bob2_truth.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    bob2_truth.set_fact(base=tech_road, pick=bowl_road)
    bob2_truth.set_fact(base=swim_road, pick=swim_road)
    bob1_idearoot = bob1_truth._idearoot
    bob2_idearoot = bob2_truth._idearoot
    assert len(bob1_idearoot._factunits) == 1
    assert len(bob1_idearoot._factunits) != len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits != bob2_idearoot._factunits

    # WHEN
    bob1_truth.meld(bob2_truth)

    # THEN
    assert len(bob1_idearoot._factunits) == 2
    assert len(bob1_idearoot._factunits) == len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits == bob2_idearoot._factunits


def test_TruthUnit_factunits_meld_IdeasMeldedBeforeFacts():
    # GIVEN
    bob_text = "Bob"
    bob1_truth = truthunit_shop(bob_text)

    swim_text = "swim"
    swim_road = bob1_truth.make_l1_road(swim_text)
    free_text = "freestyle"

    bob2_truth = truthunit_shop(bob_text)
    bob2_truth.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    bob2_truth.set_fact(base=swim_road, pick=swim_road)
    bob1_idearoot = bob1_truth._idearoot
    bob2_idearoot = bob2_truth._idearoot
    assert len(bob1_idearoot._factunits) == 0
    assert bob1_truth.idea_exists(swim_road) is False
    assert len(bob1_idearoot._factunits) != len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits != bob2_truth._idearoot._factunits

    # WHEN
    bob1_truth.meld(bob2_truth)

    # THEN
    assert len(bob1_idearoot._factunits) == 1
    assert bob1_truth.get_idea_obj(swim_road)._label == swim_text
    assert len(bob1_idearoot._factunits) == len(bob2_idearoot._factunits)
    assert bob1_idearoot._factunits == bob2_truth._idearoot._factunits


def test_TruthUnit_meld_BeliefsMeldedBefore_Others():
    # GIVEN
    yao_text = "Yao"
    yao1_truth = truthunit_shop(yao_text)
    yao2_truth = truthunit_shop(yao_text)
    bob_text = "Bob"
    yao2_truth.set_otherunit(otherunit_shop(bob_text))
    assert yao2_truth.get_beliefunit(bob_text) != None
    yao2_truth.set_beliefunit(beliefunit_shop(bob_text, _other_mirror=True))

    # WHEN/THEN
    assert yao1_truth.meld(yao2_truth) is None  # No error raised


def test_TruthUnit_factunits_meld_FactsAttributeCorrectlySet():
    # GIVEN
    bob_text = "Bob"
    bob1_truth = truthunit_shop(bob_text)

    swim_text = "swim"
    swim_road = bob1_truth.make_l1_road(swim_text)
    free_text = "freestyle"
    free_road = bob1_truth.make_l1_road(free_text)
    bob1_truth.add_idea(ideaunit_shop(free_text), parent_road=swim_road)

    bob2_truth = truthunit_shop(bob_text)
    bob2_truth.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    bob2_truth.set_fact(base=swim_road, pick=free_road, open=23, nigh=27)
    bob1_idearoot = bob1_truth._idearoot
    assert len(bob1_idearoot._factunits) == 0

    # WHEN
    bob1_truth.meld(bob2_truth)

    # THEN
    assert len(bob1_idearoot._factunits) == 1
    assert bob1_idearoot._factunits[swim_road].base == swim_road
    assert bob1_idearoot._factunits[swim_road].pick == free_road
    assert bob1_idearoot._factunits[swim_road].open == 23
    assert bob1_idearoot._factunits[swim_road].nigh == 27


def test_TruthUnit_meld_ReturnsCorrectObj_LargeExample():
    # GIVEN
    bob_text = "Bob"
    bob_truth = truthunit_shop(bob_text, "music")
    bob_idearoot = bob_truth._idearoot
    bob_idearoot._uid = 1
    yao_truth = truth_v001()

    yao_idearoot = yao_truth._idearoot
    yao_truthr_bl = yao_idearoot._balancelines
    family_text = ",Family"
    yao_family_bl = yao_truthr_bl.get(family_text)

    print(f"Before {yao_family_bl._truth_cred=} {yao_idearoot._kids_total_weight=}")
    print(f"Before   {yao_family_bl._truth_debt=} {yao_idearoot._kids_total_weight=}")

    # WHEN
    bob_truth.meld(yao_truth)
    bob_truth.get_tree_metrics()

    # THEN
    print(f"After  {yao_family_bl._truth_cred=} {yao_idearoot._kids_total_weight=}")
    print(f"After    {yao_family_bl._truth_debt=} {yao_idearoot._kids_total_weight=}")
    assert bob_truth._weight == yao_truth._weight
    assert bob_idearoot._kids == yao_idearoot._kids
    assert bob_idearoot._uid == yao_idearoot._uid
    assert bob_idearoot._factunits == yao_idearoot._factunits
    assert bob_truth._beliefs == yao_truth._beliefs
    assert bob_truth._others == yao_truth._others

    assert len(bob_idearoot._factunits) == 2
    assert len(bob_idearoot._factunits) == len(yao_idearoot._factunits)
    assert bob_truth._owner_id != yao_truth._owner_id
    print(f"{len(bob_truth._beliefs.items())=}")
    # for bob_truth_belief_key, bob_truth_belief_obj in bob_truth._beliefs.items():
    #     print(f"{bob_truth_belief_key=}")
    #     assert bob_truth_belief_obj.uid == yao_truth._beliefs[bob_truth_belief_key].uid
    #     assert bob_truth_belief_obj == yao_truth._beliefs[bob_truth_belief_key]
    assert bob_truth._beliefs == yao_truth._beliefs
    assert len(bob_truth.get_idea_dict()) == len(yao_truth.get_idea_dict())

    bob_truthr_bl = bob_idearoot._balancelines
    bob_family_bl = bob_truthr_bl.get(family_text)
    print("Melded")

    assert bob_family_bl != None
    # assert bob_family_bl == yao_family_bl
    # assert bob_family_bl.truth_cred == yao_family_bl .truth_cred
    print(f"{bob_family_bl._truth_cred=} {bob_idearoot._kids_total_weight=}")
    print(f"{yao_family_bl._truth_cred=} {bob_idearoot._kids_total_weight=}")
    print(f"  {bob_family_bl._truth_debt=} {bob_idearoot._kids_total_weight=}")
    print(f"  {yao_family_bl._truth_debt=} {bob_idearoot._kids_total_weight=}")
    assert abs(bob_family_bl._truth_cred - yao_family_bl._truth_cred) < 0.0001
    assert abs(bob_family_bl._truth_debt - yao_family_bl._truth_debt) < 0.0001

    # for balanceline in bob_truthr_bl.values():
    #     if balanceline.other_id != fam_text:
    #         assert balanceline == yao_truthr_bl.get(balanceline.other_id)
    assert bob_truthr_bl == yao_truthr_bl
    # assert x_truth1._idearoot._balancelines == bob2_truth._idearoot._balancelines
    # assert x_truth1._idearoot == bob2_truth._idearoot


def test_TruthUnit__meld_originlinks_CorrectlySetsOriginLinks():
    # GIVEN
    bob_text = "Bob"
    sue_text = "Sue"
    sue_weight = 4
    bob_truth = truthunit_shop(bob_text)
    assert len(bob_truth._originunit._links) == 0

    # WHEN
    bob_truth._meld_originlinks(other_id=sue_text, other_weight=sue_weight)

    # THEN
    assert len(bob_truth._originunit._links) == 1
    bob_sue_originunit = originunit_shop()
    bob_sue_originunit.set_originlink(other_id=sue_text, weight=sue_weight)
    assert bob_truth._originunit == bob_sue_originunit


def test_TruthUnit_meld_OriginUnitsCorrectlySet():
    # GIVEN
    bob_text = "Bob"
    bob_truth = truthunit_shop(bob_text)

    swim_text = "swim"
    swim_road = bob_truth.make_l1_road(swim_text)
    free_text = "freestyle"
    free_road = bob_truth.make_road(swim_road, free_text)
    back_text = "backstroke"
    back_road = bob_truth.make_road(swim_road, back_text)
    bob_truth.add_idea(ideaunit_shop(free_text), parent_road=swim_road)

    sue_text = "Sue"
    sue_weight = 4
    sue_x_truth = truthunit_shop(sue_text)
    sue_x_truth.add_idea(ideaunit_shop(free_text), parent_road=swim_road)
    sue_x_truth.set_fact(base=swim_road, pick=free_road, open=23, nigh=27)
    sue_x_truth.add_idea(ideaunit_shop(back_text), parent_road=swim_road)
    assert len(bob_truth._originunit._links) == 0

    # WHEN
    bob_truth.meld(sue_x_truth, other_weight=sue_weight)

    # THEN
    sue_originunit = originunit_shop()
    sue_originunit.set_originlink(other_id=sue_text, weight=sue_weight)
    assert len(bob_truth._originunit._links) == 1
    assert bob_truth._originunit == sue_originunit
    bob_free_idea = bob_truth.get_idea_obj(free_road)
    bob_back_idea = bob_truth.get_idea_obj(back_road)
    print(f"{bob_free_idea._originunit=}")
    print(f"{bob_back_idea._originunit=}")
    assert bob_free_idea._originunit != None
    assert bob_free_idea._originunit != originunit_shop()
    assert bob_free_idea._originunit == sue_originunit
    assert bob_back_idea._originunit != None
    assert bob_back_idea._originunit != originunit_shop()
    assert bob_back_idea._originunit == sue_originunit
