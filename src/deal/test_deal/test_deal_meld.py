from src.deal.idea import IdeaKid
from src.deal.deal import DealUnit
from src.deal.group import groupunit_shop
from src.deal.party import partyunit_shop
from src.deal.origin import originunit_shop
from pytest import raises as pytest_raises
from src.deal.examples.example_deals import deal_v001
from src.deal.x_func import get_on_meld_weight_actions


def test_deal_meld_BaseScenario():
    # GIVEN
    deal_text = "x_deal"
    x_deal1 = DealUnit(_healer=deal_text)
    x_deal2 = DealUnit(_healer=deal_text)

    # WHEN
    x_deal1.meld(other_deal=x_deal2)

    # THEN
    assert x_deal1
    assert x_deal1._healer == deal_text


def test_deal_meld_WeightDoesNotCombine():
    # GIVEN
    deal_text = "x_deal"
    x_deal1 = DealUnit(_healer=deal_text)
    x_deal1._weight = 3
    x_deal2 = DealUnit(_healer=deal_text)
    x_deal2._weight = 5

    # WHEN
    x_deal1.meld(other_deal=x_deal2)

    # THEN
    assert x_deal1._weight == 3


def test_deal_meld_PartyUnits():
    # GIVEN
    x1_title = "x1_party"
    x1_party = partyunit_shop(title=x1_title)

    deal_text = "x_deal"
    x_deal1 = DealUnit(_healer=deal_text)
    x_deal1.set_partyunit(partyunit=x1_party)

    x_deal2 = DealUnit(_healer=deal_text)
    x_deal2.set_partyunit(partyunit=x1_party)
    x2_title = "x2_party"
    x2_party = partyunit_shop(title=x2_title)
    x_deal2.set_partyunit(partyunit=x2_party)
    assert len(x_deal1._partys) == 1

    # WHEN
    x_deal1.meld(other_deal=x_deal2)

    # THEN
    assert len(x_deal1._partys) == 2
    assert x_deal1._partys.get(x1_title) != None
    assert x_deal1._partys.get(x2_title) != None


def test_deal_meld_GroupUnits():
    # GIVEN
    x1_title = "x1_group"
    x1_group = groupunit_shop(brand=x1_title)

    deal_text = "x_deal"
    x_deal1 = DealUnit(_healer=deal_text)
    x_deal1.set_groupunit(groupunit=x1_group)

    x_deal2 = DealUnit(_healer=deal_text)
    x_deal2.set_groupunit(groupunit=x1_group)
    x2_title = "x2_group"
    x2_group = groupunit_shop(brand=x2_title, uid=5)
    x_deal2.set_groupunit(groupunit=x2_group)
    assert len(x_deal1._groups) == 1

    # WHEN
    x_deal1.meld(other_deal=x_deal2)

    # THEN
    # for group_title in x_deal1._groups.values():
    #     print(f"x_deal1 {group_title.title=}")

    assert len(x_deal1._groups) == 2
    assert x_deal1._groups.get(x1_title) != None
    assert x_deal1._groups.get(x2_title) != None
    # assert x_deal1._groups.get(x2_title).uid == 5


def test_deal_idearoot_meld_IdeaRootAttrCorrectlyMelded():
    # GIVEN
    x_deal1 = DealUnit(_healer="spirit")
    x_deal2 = DealUnit(_healer="spirit")
    x_deal2._idearoot._uid = 4
    assert x_deal1._idearoot._uid == 1
    assert x_deal2._idearoot._uid == 4

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_deal1.meld(x_deal2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea=None,{x_deal1._fix_handle} _uid:1 with None,{x_deal2._fix_handle} _uid:4"
    )


def test_deal_idearoot_meld_Add4IdeasScenario():
    # GIVEN
    spirit_text = "spirit"
    x_deal1 = DealUnit(_healer=spirit_text)

    tech_text = "tech"
    tech_road = f"{x_deal1._fix_handle},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{x_deal1._fix_handle},{tech_text},{bowl_text}"
    swim_text = "swim"
    swim_road = f"{x_deal1._fix_handle},{swim_text}"
    free_text = "freestyle"
    free_road = f"{x_deal1._fix_handle},{swim_text},{free_text}"

    x_deal2 = DealUnit(_healer=spirit_text)
    x_deal2.add_idea(pad=x_deal2._fix_handle, idea_kid=IdeaKid(_label=tech_text))
    x_deal2.add_idea(pad=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    x_deal2.add_idea(pad=swim_road, idea_kid=IdeaKid(_label=free_text))

    # WHEN
    x_deal1.meld(x_deal2)

    # THEN
    assert len(x_deal1.get_idea_list()) == 5
    assert x_deal1.get_idea_kid(road=tech_road)._label == tech_text
    assert x_deal1.get_idea_kid(road=bowl_road)._label == bowl_text
    assert x_deal1.get_idea_kid(road=swim_road)._label == swim_text
    assert x_deal1.get_idea_kid(road=free_road)._label == free_text


def test_deal_idearoot_meld_2SameIdeasScenario():
    # GIVEN
    healer_text = "Yoa"
    x_deal1 = DealUnit(_healer=healer_text)
    tech_text = "tech"
    tech_road = f"{x_deal1._fix_handle},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{x_deal1._fix_handle},{tech_text},{bowl_text}"

    x_deal1.add_idea(pad=x_deal1._fix_handle, idea_kid=IdeaKid(_label=tech_text))
    x_deal1.add_idea(pad=tech_road, idea_kid=IdeaKid(_label=bowl_text))

    x_deal2 = DealUnit(_healer=healer_text)
    x_deal2.add_idea(pad=x_deal2._fix_handle, idea_kid=IdeaKid(_label=tech_text))
    x_deal2.add_idea(pad=tech_road, idea_kid=IdeaKid(_label=bowl_text))

    assert x_deal1.get_idea_kid(road=bowl_road)._weight == 1
    # WHEN
    x_deal1.meld(x_deal2)

    # THEN
    assert x_deal1.get_idea_kid(road=bowl_road)._weight == 1
    assert len(x_deal1.get_idea_list()) == 3


def test_deal_acptfactunits_meld_BaseScenarioWorks():
    # GIVEN
    x_deal1 = DealUnit(_healer="test7")
    tech_text = "tech"
    tech_road = f"{x_deal1._fix_handle},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{x_deal1._fix_handle},{tech_text},{bowl_text}"

    x_deal1.add_idea(pad=x_deal1._fix_handle, idea_kid=IdeaKid(_label=tech_text))
    x_deal1.add_idea(pad=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    x_deal1.set_acptfact(base=tech_road, pick=bowl_road)

    x_deal2 = DealUnit(_healer="test7")
    x_deal2.add_idea(pad=x_deal2._fix_handle, idea_kid=IdeaKid(_label=tech_text))
    x_deal2.add_idea(pad=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    x_deal2.set_acptfact(base=tech_road, pick=bowl_road)

    # WHEN
    x_deal1.meld(x_deal2)

    # THEN
    assert len(x_deal1._idearoot._acptfactunits) == 1
    assert len(x_deal1._idearoot._acptfactunits) == len(
        x_deal2._idearoot._acptfactunits
    )
    assert x_deal1._idearoot._acptfactunits == x_deal2._idearoot._acptfactunits


def test_deal_acptfactunits_meld_2AcptFactUnitsWorks():
    # GIVEN
    x_deal1 = DealUnit(_healer="test7")
    tech_text = "tech"
    tech_road = f"{x_deal1._fix_handle},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{x_deal1._fix_handle},{tech_text},{bowl_text}"
    swim_text = "swim"
    swim_road = f"{x_deal1._fix_handle},{swim_text}"
    free_text = "freestyle"

    x_deal1.add_idea(pad=x_deal1._fix_handle, idea_kid=IdeaKid(_label=tech_text))
    x_deal1.add_idea(pad=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    x_deal1.add_idea(pad=swim_road, idea_kid=IdeaKid(_label=free_text))
    x_deal1.set_acptfact(base=tech_road, pick=bowl_road)

    x_deal2 = DealUnit(_healer="test7")
    x_deal2.add_idea(pad=x_deal2._fix_handle, idea_kid=IdeaKid(_label=tech_text))
    x_deal2.add_idea(pad=tech_road, idea_kid=IdeaKid(_label=bowl_text))
    x_deal2.add_idea(pad=swim_road, idea_kid=IdeaKid(_label=free_text))
    x_deal2.set_acptfact(base=tech_road, pick=bowl_road)
    x_deal2.set_acptfact(base=swim_road, pick=swim_road)

    # WHEN
    x_deal1.meld(x_deal2)

    # THEN
    assert len(x_deal1._idearoot._acptfactunits) == 2
    assert len(x_deal1._idearoot._acptfactunits) == len(
        x_deal2._idearoot._acptfactunits
    )
    assert x_deal1._idearoot._acptfactunits == x_deal2._idearoot._acptfactunits


def test_deal_acptfactunits_meld_IdeasMeldedBeforeAcptFacts():
    # GIVEN
    x_deal1 = DealUnit(_healer="test7")

    swim_text = "swim"
    swim_road = f"{x_deal1._fix_handle},{swim_text}"
    free_text = "freestyle"

    x_deal2 = DealUnit(_healer="test7")
    x_deal2.add_idea(pad=swim_road, idea_kid=IdeaKid(_label=free_text))
    x_deal2.set_acptfact(base=swim_road, pick=swim_road)

    # WHEN
    x_deal1.meld(x_deal2)

    # THEN
    print()
    assert len(x_deal1._idearoot._acptfactunits) == 1
    assert x_deal1.get_idea_kid(swim_road)._label == swim_text
    assert x_deal1._idearoot._kids[swim_text]._label == swim_text
    assert len(x_deal1._idearoot._acptfactunits) == len(
        x_deal2._idearoot._acptfactunits
    )
    assert x_deal1._idearoot._acptfactunits == x_deal2._idearoot._acptfactunits


def test_deal_acptfactunits_meld_GroupsMeldedBefore_Partys():
    # GIVEN
    healer_text = "Yoa"
    x_deal1 = DealUnit(_healer=healer_text)
    x_deal2 = DealUnit(_healer=healer_text)
    bob = "bob"
    x_deal2.set_partyunit(partyunit_shop(title=bob))
    assert x_deal2._groups.get(bob) != None
    assert x_deal2._groups.get(bob).uid is None
    x_deal2.set_groupunit(groupunit_shop(brand=bob, uid=13))
    assert x_deal2._groups.get(bob).uid == 13

    # WHEN/THEN
    assert x_deal1.meld(x_deal2) is None  # No error raised
    # with pytest_raises(Exception) as excinfo:
    #     x_deal1.meld(x_deal2)
    # assert (
    #     str(excinfo.value)
    #     == f"Meld fail GroupUnit bob .uid='None' not the same as .uid='13"
    # )


def test_deal_acptfactunits_meld_AcptFactsAttributeCorrectlySet():
    # GIVEN
    x_deal1 = DealUnit(_healer="test7")

    swim_text = "swim"
    swim_road = f"{x_deal1._fix_handle},{swim_text}"
    free_text = "freestyle"
    free_road = f"{x_deal1._fix_handle},{free_text}"
    x_deal1.add_idea(pad=swim_road, idea_kid=IdeaKid(_label=free_text))

    x_deal2 = DealUnit(_healer="test7")
    x_deal2.add_idea(pad=swim_road, idea_kid=IdeaKid(_label=free_text))
    x_deal2.set_acptfact(base=swim_road, pick=free_road, open=23, nigh=27)

    # WHEN
    x_deal1.meld(x_deal2)

    # THEN
    print()
    assert len(x_deal1._idearoot._acptfactunits) == 1
    assert x_deal1._idearoot._acptfactunits[swim_road].base == swim_road
    assert x_deal1._idearoot._acptfactunits[swim_road].pick == free_road
    assert x_deal1._idearoot._acptfactunits[swim_road].open == 23
    assert x_deal1._idearoot._acptfactunits[swim_road].nigh == 27


def test_deal_meld_worksCorrectlyForLargeExample():
    # GIVEN
    healer_text = "TlME"
    x_deal1 = DealUnit(_healer=healer_text)
    x_deal1._idearoot._uid = 1
    x_deal2 = deal_v001()

    x_deal2r_bl = x_deal2._idearoot._balancelines
    fam_text = "Family"

    print(
        f"Before {x_deal2r_bl.get(fam_text)._deal_credit=} {x_deal2._idearoot._kids_total_weight=}"
    )

    # WHEN
    x_deal1.meld(x_deal2)
    x_deal1.get_tree_metrics()

    # THEN
    print(
        f"After    {x_deal2r_bl.get(fam_text)._deal_debt=} {x_deal2._idearoot._kids_total_weight=}"
    )
    assert x_deal1._weight == x_deal2._weight
    assert x_deal1._idearoot._kids == x_deal2._idearoot._kids
    assert x_deal1._idearoot._uid == x_deal2._idearoot._uid
    assert x_deal1._idearoot._acptfactunits == x_deal2._idearoot._acptfactunits
    assert x_deal1._groups == x_deal2._groups
    assert x_deal1._partys == x_deal2._partys

    assert len(x_deal1._idearoot._acptfactunits) == 2
    assert len(x_deal1._idearoot._acptfactunits) == len(
        x_deal2._idearoot._acptfactunits
    )
    assert x_deal1._healer == x_deal2._healer
    print(f"{len(x_deal1._groups.items())=}")
    # for x_deal1_group_key, x_deal1_group_obj in x_deal1._groups.items():
    #     print(f"{x_deal1_group_key=}")
    #     assert x_deal1_group_obj.uid == x_deal2._groups[x_deal1_group_key].uid
    #     assert x_deal1_group_obj == x_deal2._groups[x_deal1_group_key]
    assert x_deal1._groups == x_deal2._groups
    assert len(x_deal1.get_idea_list()) == len(x_deal2.get_idea_list())

    x_deal1r_bl = x_deal1._idearoot._balancelines
    print(
        f"Melded   {x_deal1r_bl.get(fam_text)._deal_debt=} {x_deal1._idearoot._kids_total_weight=}"
    )

    assert x_deal1r_bl.get(fam_text) != None
    # assert x_deal1r_bl.get(fam_text) == x_deal2r_bl.get(fam_text)
    # assert x_deal1r_bl.get(fam_text).deal_credit == x_deal2r_bl.get(fam_text).deal_credit
    print(
        f"{x_deal1r_bl.get(fam_text)._deal_credit=} {x_deal1._idearoot._kids_total_weight=}"
    )
    print(
        f"{x_deal2r_bl.get(fam_text)._deal_credit=} {x_deal1._idearoot._kids_total_weight=}"
    )
    print(
        f"  {x_deal1r_bl.get(fam_text)._deal_debt=} {x_deal1._idearoot._kids_total_weight=}"
    )
    print(
        f"  {x_deal2r_bl.get(fam_text)._deal_debt=} {x_deal1._idearoot._kids_total_weight=}"
    )
    assert (
        abs(
            x_deal1r_bl.get(fam_text)._deal_credit
            - x_deal2r_bl.get(fam_text)._deal_credit
        )
        < 0.0001
    )
    assert (
        abs(x_deal1r_bl.get(fam_text)._deal_debt - x_deal2r_bl.get(fam_text)._deal_debt)
        < 0.0001
    )

    # for balanceline in x_deal1r_bl.values():
    #     if balanceline.title != fam_text:
    #         assert balanceline == x_deal2r_bl.get(balanceline.title)
    assert x_deal1r_bl == x_deal2r_bl
    # assert x_deal1._idearoot._balancelines == x_deal2._idearoot._balancelines
    # assert x_deal1._idearoot == x_deal2._idearoot


def test_get_on_meld_weight_actions_HasCorrectItems():
    assert len(get_on_meld_weight_actions()) == 5
    assert get_on_meld_weight_actions() == {
        "accept": None,
        "default": None,
        "match": None,
        "override": None,
        "sum": None,
    }


def test_deal__meld_originlinks_CorrectlySetsOriginLinks():
    # GIVEN
    bob_text = "Bob"
    sue_text = "Sue"
    sue_weight = 4
    bob_x_deal = DealUnit(_healer=bob_text)
    assert len(bob_x_deal._originunit._links) == 0

    # WHEN
    bob_x_deal._meld_originlinks(party_title=sue_text, party_weight=sue_weight)

    # THEN
    assert len(bob_x_deal._originunit._links) == 1
    bob_sue_originunit = originunit_shop()
    bob_sue_originunit.set_originlink(title=sue_text, weight=sue_weight)
    assert bob_x_deal._originunit == bob_sue_originunit


def test_deal_meld_OriginUnitsCorrectlySet():
    # GIVEN
    bob_text = "Bob"
    bob_x_deal = DealUnit(_healer=bob_text)

    swim_text = "swim"
    swim_road = f"{bob_x_deal._fix_handle},{swim_text}"
    free_text = "freestyle"
    free_road = f"{swim_road},{free_text}"
    back_text = "backstroke"
    back_road = f"{swim_road},{back_text}"
    bob_x_deal.add_idea(pad=swim_road, idea_kid=IdeaKid(_label=free_text))

    sue_text = "Sue"
    sue_weight = 4
    sue_x_deal = DealUnit(_healer=sue_text)
    sue_x_deal.add_idea(pad=swim_road, idea_kid=IdeaKid(_label=free_text))
    sue_x_deal.set_acptfact(base=swim_road, pick=free_road, open=23, nigh=27)
    sue_x_deal.add_idea(pad=swim_road, idea_kid=IdeaKid(_label=back_text))
    assert len(bob_x_deal._originunit._links) == 0

    # WHEN
    bob_x_deal.meld(sue_x_deal, party_weight=sue_weight)

    # THEN
    sue_originunit = originunit_shop()
    sue_originunit.set_originlink(title=sue_text, weight=sue_weight)
    assert len(bob_x_deal._originunit._links) == 1
    assert bob_x_deal._originunit == sue_originunit
    bob_free_idea = bob_x_deal.get_idea_kid(road=free_road)
    bob_back_idea = bob_x_deal.get_idea_kid(road=back_road)
    print(f"{bob_free_idea._originunit=}")
    print(f"{bob_back_idea._originunit=}")
    assert bob_free_idea._originunit != None
    assert bob_free_idea._originunit != originunit_shop()
    assert bob_free_idea._originunit == sue_originunit
    assert bob_back_idea._originunit != None
    assert bob_back_idea._originunit != originunit_shop()
    assert bob_back_idea._originunit == sue_originunit
