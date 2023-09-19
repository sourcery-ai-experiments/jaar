from src.contract.idea import IdeaKid
from src.contract.contract import ContractUnit
from src.contract.group import groupunit_shop
from src.contract.member import memberunit_shop
from src.contract.road import get_global_root_label as root_label
from src.contract.origin import originunit_shop
from pytest import raises as pytest_raises
from src.contract.examples.example_contracts import contract_v001
from src.contract.x_func import get_on_meld_weight_actions


def test_contract_meld_BaseScenario():
    # GIVEN
    contract_text = "x_contract"
    cx1 = ContractUnit(_owner=contract_text)
    cx2 = ContractUnit(_owner=contract_text)

    # WHEN
    cx1.meld(other_contract=cx2)

    # THEN
    assert cx1
    assert cx1._owner == contract_text


def test_contract_meld_WeightDoesNotCombine():
    # GIVEN
    contract_text = "x_contract"
    cx1 = ContractUnit(_owner=contract_text)
    cx1._weight = 3
    cx2 = ContractUnit(_owner=contract_text)
    cx2._weight = 5

    # WHEN
    cx1.meld(other_contract=cx2)

    # THEN
    assert cx1._weight == 3


def test_contract_meld_MemberUnits():
    # GIVEN
    x1_name = "x1_member"
    x1_member = memberunit_shop(name=x1_name)

    contract_text = "x_contract"
    cx1 = ContractUnit(_owner=contract_text)
    cx1.set_memberunit(memberunit=x1_member)

    cx2 = ContractUnit(_owner=contract_text)
    cx2.set_memberunit(memberunit=x1_member)
    x2_name = "x2_member"
    x2_member = memberunit_shop(name=x2_name)
    cx2.set_memberunit(memberunit=x2_member)
    assert len(cx1._members) == 1

    # WHEN
    cx1.meld(other_contract=cx2)

    # THEN
    assert len(cx1._members) == 2
    assert cx1._members.get(x1_name) != None
    assert cx1._members.get(x2_name) != None


def test_contract_meld_GroupUnits():
    # GIVEN
    x1_name = "x1_group"
    x1_group = groupunit_shop(name=x1_name)

    contract_text = "x_contract"
    cx1 = ContractUnit(_owner=contract_text)
    cx1.set_groupunit(groupunit=x1_group)

    cx2 = ContractUnit(_owner=contract_text)
    cx2.set_groupunit(groupunit=x1_group)
    x2_name = "x2_group"
    x2_group = groupunit_shop(name=x2_name, uid=5)
    cx2.set_groupunit(groupunit=x2_group)
    assert len(cx1._groups) == 1

    # WHEN
    cx1.meld(other_contract=cx2)

    # THEN
    # for group_name in cx1._groups.values():
    #     print(f"cx1 {group_name.name=}")

    assert len(cx1._groups) == 2
    assert cx1._groups.get(x1_name) != None
    assert cx1._groups.get(x2_name) != None
    # assert cx1._groups.get(x2_name).uid == 5


def test_contract_idearoot_meld_IdeaRootAttrCorrectlyMelded():
    # GIVEN
    cx1 = ContractUnit(_owner="spirit")
    cx2 = ContractUnit(_owner="spirit")
    cx2._idearoot._uid = 4
    assert cx1._idearoot._uid == 1
    assert cx2._idearoot._uid == 4

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        cx1.meld(cx2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea=None,{root_label()} _uid:1 with None,{root_label()} _uid:4"
    )


def test_contract_idearoot_meld_Add4IdeasScenario():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"
    swim_text = "swim"
    swim_road = f"{root_label()},{swim_text}"
    free_text = "freestyle"
    free_road = f"{root_label()},{swim_text},{free_text}"

    cx1 = ContractUnit(_owner="spirit")

    cx2 = ContractUnit(_owner="spirit")
    cx2.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    cx2.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    cx2.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))

    # WHEN
    cx1.meld(cx2)

    # THEN
    assert len(cx1.get_idea_list()) == 5
    assert cx1.get_idea_kid(road=tech_road)._label == tech_text
    assert cx1.get_idea_kid(road=bowl_road)._label == bowl_text
    assert cx1.get_idea_kid(road=swim_road)._label == swim_text
    assert cx1.get_idea_kid(road=free_road)._label == free_text


def test_contract_idearoot_meld_2SameIdeasScenario():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"

    owner_text = "Yoa"
    cx1 = ContractUnit(_owner=owner_text)
    cx1.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    cx1.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))

    cx2 = ContractUnit(_owner=owner_text)
    cx2.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    cx2.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))

    assert cx1.get_idea_kid(road=bowl_road)._weight == 1
    # WHEN
    cx1.meld(cx2)

    # THEN
    assert cx1.get_idea_kid(road=bowl_road)._weight == 1
    assert len(cx1.get_idea_list()) == 3


def test_contract_acptfactunits_meld_BaseScenarioWorks():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"

    cx1 = ContractUnit(_owner="test7")
    cx1.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    cx1.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    cx1.set_acptfact(base=tech_road, pick=bowl_road)

    cx2 = ContractUnit(_owner="test7")
    cx2.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    cx2.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    cx2.set_acptfact(base=tech_road, pick=bowl_road)

    # WHEN
    cx1.meld(cx2)

    # THEN
    assert len(cx1._idearoot._acptfactunits) == 1
    assert len(cx1._idearoot._acptfactunits) == len(cx2._idearoot._acptfactunits)
    assert cx1._idearoot._acptfactunits == cx2._idearoot._acptfactunits


def test_contract_acptfactunits_meld_2AcptFactUnitsWorks():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"
    swim_text = "swim"
    swim_road = f"{root_label()},{swim_text}"
    free_text = "freestyle"

    cx1 = ContractUnit(_owner="test7")
    cx1.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    cx1.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    cx1.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))
    cx1.set_acptfact(base=tech_road, pick=bowl_road)

    cx2 = ContractUnit(_owner="test7")
    cx2.add_idea(walk=root_label(), idea_kid=IdeaKid(_label=tech_text))
    cx2.add_idea(walk=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    cx2.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))
    cx2.set_acptfact(base=tech_road, pick=bowl_road)
    cx2.set_acptfact(base=swim_road, pick=swim_road)

    # WHEN
    cx1.meld(cx2)

    # THEN
    assert len(cx1._idearoot._acptfactunits) == 2
    assert len(cx1._idearoot._acptfactunits) == len(cx2._idearoot._acptfactunits)
    assert cx1._idearoot._acptfactunits == cx2._idearoot._acptfactunits


def test_contract_acptfactunits_meld_IdeasMeldedBeforeAcptFacts():
    # GIVEN
    swim_text = "swim"
    swim_road = f"{root_label()},{swim_text}"
    free_text = "freestyle"

    cx1 = ContractUnit(_owner="test7")

    cx2 = ContractUnit(_owner="test7")
    cx2.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))
    cx2.set_acptfact(base=swim_road, pick=swim_road)

    # WHEN
    cx1.meld(cx2)

    # THEN
    print()
    assert len(cx1._idearoot._acptfactunits) == 1
    assert cx1.get_idea_kid(swim_road)._label == swim_text
    assert cx1._idearoot._kids[swim_text]._label == swim_text
    assert len(cx1._idearoot._acptfactunits) == len(cx2._idearoot._acptfactunits)
    assert cx1._idearoot._acptfactunits == cx2._idearoot._acptfactunits


def test_contract_acptfactunits_meld_GroupsMeldedBefore_Members():
    # GIVEN
    owner_text = "Yoa"
    cx1 = ContractUnit(_owner=owner_text)
    cx2 = ContractUnit(_owner=owner_text)
    bob = "bob"
    cx2.set_memberunit(memberunit_shop(name=bob))
    assert cx2._groups.get(bob) != None
    assert cx2._groups.get(bob).uid is None
    cx2.set_groupunit(groupunit_shop(name=bob, uid=13))
    assert cx2._groups.get(bob).uid == 13

    # WHEN/THEN
    assert cx1.meld(cx2) is None  # No error raised
    # with pytest_raises(Exception) as excinfo:
    #     cx1.meld(cx2)
    # assert (
    #     str(excinfo.value)
    #     == f"Meld fail GroupUnit bob .uid='None' not the same as .uid='13"
    # )


def test_contract_acptfactunits_meld_AcptFactsAttributeCorrectlySet():
    # GIVEN
    swim_text = "swim"
    swim_road = f"{root_label()},{swim_text}"
    free_text = "freestyle"
    free_road = f"{root_label()},{free_text}"

    cx1 = ContractUnit(_owner="test7")
    cx1.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))

    cx2 = ContractUnit(_owner="test7")
    cx2.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))
    cx2.set_acptfact(base=swim_road, pick=free_road, open=23, nigh=27)

    # WHEN
    cx1.meld(cx2)

    # THEN
    print()
    assert len(cx1._idearoot._acptfactunits) == 1
    assert cx1._idearoot._acptfactunits[swim_road].base == swim_road
    assert cx1._idearoot._acptfactunits[swim_road].pick == free_road
    assert cx1._idearoot._acptfactunits[swim_road].open == 23
    assert cx1._idearoot._acptfactunits[swim_road].nigh == 27


def test_contract_meld_worksCorrectlyForLargeExample():
    # GIVEN
    owner_text = "TlME"
    cx1 = ContractUnit(_owner=owner_text)
    cx1._idearoot._uid = 1
    cx2 = contract_v001()

    cx2r_bl = cx2._idearoot._grouplines
    fam_text = "Family"

    print(
        f"Before {cx2r_bl.get(fam_text)._contract_credit=} {cx2._idearoot._kids_total_weight=}"
    )

    # WHEN
    cx1.meld(cx2)
    cx1.get_tree_metrics()

    # THEN
    print(
        f"After    {cx2r_bl.get(fam_text)._contract_debt=} {cx2._idearoot._kids_total_weight=}"
    )
    assert cx1._weight == cx2._weight
    assert cx1._idearoot._kids == cx2._idearoot._kids
    assert cx1._idearoot._uid == cx2._idearoot._uid
    assert cx1._idearoot._acptfactunits == cx2._idearoot._acptfactunits
    assert cx1._groups == cx2._groups
    assert cx1._members == cx2._members

    assert len(cx1._idearoot._acptfactunits) == 2
    assert len(cx1._idearoot._acptfactunits) == len(cx2._idearoot._acptfactunits)
    assert cx1._owner == cx2._owner
    print(f"{len(cx1._groups.items())=}")
    # for cx1_group_key, cx1_group_obj in cx1._groups.items():
    #     print(f"{cx1_group_key=}")
    #     assert cx1_group_obj.uid == cx2._groups[cx1_group_key].uid
    #     assert cx1_group_obj == cx2._groups[cx1_group_key]
    assert cx1._groups == cx2._groups
    assert len(cx1.get_idea_list()) == len(cx2.get_idea_list())

    cx1r_bl = cx1._idearoot._grouplines
    print(
        f"Melded   {cx1r_bl.get(fam_text)._contract_debt=} {cx1._idearoot._kids_total_weight=}"
    )

    assert cx1r_bl.get(fam_text) != None
    # assert cx1r_bl.get(fam_text) == cx2r_bl.get(fam_text)
    # assert cx1r_bl.get(fam_text).contract_credit == cx2r_bl.get(fam_text).contract_credit
    print(
        f"{cx1r_bl.get(fam_text)._contract_credit=} {cx1._idearoot._kids_total_weight=}"
    )
    print(
        f"{cx2r_bl.get(fam_text)._contract_credit=} {cx1._idearoot._kids_total_weight=}"
    )
    print(
        f"  {cx1r_bl.get(fam_text)._contract_debt=} {cx1._idearoot._kids_total_weight=}"
    )
    print(
        f"  {cx2r_bl.get(fam_text)._contract_debt=} {cx1._idearoot._kids_total_weight=}"
    )
    assert (
        abs(
            cx1r_bl.get(fam_text)._contract_credit
            - cx2r_bl.get(fam_text)._contract_credit
        )
        < 0.0001
    )
    assert (
        abs(cx1r_bl.get(fam_text)._contract_debt - cx2r_bl.get(fam_text)._contract_debt)
        < 0.0001
    )

    # for groupline in cx1r_bl.values():
    #     if groupline.name != fam_text:
    #         assert groupline == cx2r_bl.get(groupline.name)
    assert cx1r_bl == cx2r_bl
    # assert cx1._idearoot._grouplines == cx2._idearoot._grouplines
    # assert cx1._idearoot == cx2._idearoot


def test_get_on_meld_weight_actions_HasCorrectItems():
    assert len(get_on_meld_weight_actions()) == 5
    assert get_on_meld_weight_actions() == {
        "accept": None,
        "default": None,
        "match": None,
        "override": None,
        "sum": None,
    }


def test_contract__meld_originlinks_CorrectlySetsOriginLinks():
    # GIVEN
    bob_text = "Bob"
    sue_text = "Sue"
    sue_weight = 4
    bob_cx = ContractUnit(_owner=bob_text)
    assert len(bob_cx._originunit._links) == 0

    # WHEN
    bob_cx._meld_originlinks(member_name=sue_text, member_weight=sue_weight)

    # THEN
    assert len(bob_cx._originunit._links) == 1
    bob_sue_originunit = originunit_shop()
    bob_sue_originunit.set_originlink(name=sue_text, weight=sue_weight)
    assert bob_cx._originunit == bob_sue_originunit


def test_contract_meld_OriginUnitsCorrectlySet():
    # GIVEN
    swim_text = "swim"
    swim_road = f"{root_label()},{swim_text}"
    free_text = "freestyle"
    free_road = f"{swim_road},{free_text}"
    back_text = "backstroke"
    back_road = f"{swim_road},{back_text}"

    bob_text = "Bob"
    bob_cx = ContractUnit(_owner=bob_text)
    bob_cx.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))

    sue_text = "Sue"
    sue_weight = 4
    sue_cx = ContractUnit(_owner=sue_text)
    sue_cx.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=free_text))
    sue_cx.set_acptfact(base=swim_road, pick=free_road, open=23, nigh=27)
    sue_cx.add_idea(walk=swim_road, idea_kid=IdeaKid(_label=back_text))
    assert len(bob_cx._originunit._links) == 0

    # WHEN
    bob_cx.meld(sue_cx, member_weight=sue_weight)

    # THEN
    sue_originunit = originunit_shop()
    sue_originunit.set_originlink(name=sue_text, weight=sue_weight)
    assert len(bob_cx._originunit._links) == 1
    assert bob_cx._originunit == sue_originunit
    bob_free_idea = bob_cx.get_idea_kid(road=free_road)
    bob_back_idea = bob_cx.get_idea_kid(road=back_road)
    print(f"{bob_free_idea._originunit=}")
    print(f"{bob_back_idea._originunit=}")
    assert bob_free_idea._originunit != None
    assert bob_free_idea._originunit != originunit_shop()
    assert bob_free_idea._originunit == sue_originunit
    assert bob_back_idea._originunit != None
    assert bob_back_idea._originunit != originunit_shop()
    assert bob_back_idea._originunit == sue_originunit
