from lib.agent.idea import IdeaKid
from lib.agent.agent import AgentUnit
from lib.agent.brand import brandunit_shop
from lib.agent.ally import allyunit_shop
from pytest import raises as pytest_raises
from lib.agent.examples.example_agents import agent_v001
from lib.agent.x_func import get_on_meld_weight_actions


def test_agent_meld_BaseScenario():
    # GIVEN
    agent_text = "x_agent"
    ax1 = AgentUnit(_desc=agent_text)
    ax2 = AgentUnit(_desc=agent_text)

    # WHEN
    ax1.meld(other_agent=ax2)

    # THEN
    assert ax1
    assert ax1._desc == agent_text


def test_agent_meld_WeightDoesNotCombine():
    # GIVEN
    agent_text = "x_agent"
    ax1 = AgentUnit(_desc=agent_text)
    ax1._weight = 3
    ax2 = AgentUnit(_desc=agent_text)
    ax2._weight = 5

    # WHEN
    ax1.meld(other_agent=ax2)

    # THEN
    assert ax1._weight == 3


def test_agent_meld_AllyUnits():
    # GIVEN
    x1_name = "x1_ally"
    x1_ally = allyunit_shop(name=x1_name)

    agent_text = "x_agent"
    ax1 = AgentUnit(_desc=agent_text)
    ax1.set_allyunit(allyunit=x1_ally)

    ax2 = AgentUnit(_desc=agent_text)
    ax2.set_allyunit(allyunit=x1_ally)
    x2_name = "x2_ally"
    x2_ally = allyunit_shop(name=x2_name)
    ax2.set_allyunit(allyunit=x2_ally)
    assert len(ax1._allys) == 1

    # WHEN
    ax1.meld(other_agent=ax2)

    # THEN
    assert len(ax1._allys) == 2
    assert ax1._allys.get(x1_name) != None
    assert ax1._allys.get(x2_name) != None


def test_agent_meld_BrandUnits():
    # GIVEN
    x1_name = "x1_brand"
    x1_brand = brandunit_shop(name=x1_name)

    agent_text = "x_agent"
    ax1 = AgentUnit(_desc=agent_text)
    ax1.set_brandunit(brandunit=x1_brand)

    ax2 = AgentUnit(_desc=agent_text)
    ax2.set_brandunit(brandunit=x1_brand)
    x2_name = "x2_brand"
    x2_brand = brandunit_shop(name=x2_name, uid=5)
    ax2.set_brandunit(brandunit=x2_brand)
    assert len(ax1._brands) == 1

    # WHEN
    ax1.meld(other_agent=ax2)

    # THEN
    for brand_name in ax1._brands.values():
        print(f"ax1 {brand_name.name=}")

    assert len(ax1._brands) == 2
    assert ax1._brands.get(x1_name) != None
    assert ax1._brands.get(x2_name) != None
    # assert ax1._brands.get(x2_name).uid == 5


def test_agent_idearoot_meld_IdeaRootAttrCorrectlyMelded():
    # GIVEN
    src = "casa"
    ax1 = AgentUnit(_desc="spirit")
    ax2 = AgentUnit(_desc="spirit")
    ax2._idearoot._uid = 4
    assert ax1._idearoot._uid == 1
    assert ax2._idearoot._uid == 4

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        ax1.meld(ax2)
    assert (
        str(excinfo.value)
        == f"Meld fail idea=None,spirit _uid:1 with None,spirit _uid:4"
    )


def test_agent_idearoot_meld_Add4IdeasScenario():
    # GIVEN
    src = "casa"
    tech_text = "tech"
    tech_road = f"{src},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{src},{tech_text},{bowl_text}"
    swim_text = "swim"
    swim_road = f"{src},{swim_text}"
    free_text = "freestyle"
    free_road = f"{src},{swim_text},{free_text}"

    ax1 = AgentUnit(_desc="spirit")

    ax2 = AgentUnit(_desc="spirit")
    ax2.add_idea(walk=src, idea_kid=IdeaKid(_desc=tech_text))
    ax2.add_idea(walk=tech_road, idea_kid=IdeaKid(_desc=bowl_text))
    ax2.add_idea(walk=swim_road, idea_kid=IdeaKid(_desc=free_text))

    # WHEN
    ax1.meld(ax2)

    # THEN
    assert len(ax1.get_idea_list()) == 5
    assert ax1.get_idea_kid(road=tech_road)._desc == tech_text
    assert ax1.get_idea_kid(road=bowl_road)._desc == bowl_text
    assert ax1.get_idea_kid(road=swim_road)._desc == swim_text
    assert ax1.get_idea_kid(road=free_road)._desc == free_text


def test_agent_idearoot_meld_2SameIdeasScenario():
    # GIVEN
    src = "casa"
    tech_text = "tech"
    tech_road = f"{src},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{src},{tech_text},{bowl_text}"

    ax1 = AgentUnit(_desc=src)
    ax1.add_idea(walk=src, idea_kid=IdeaKid(_desc=tech_text))
    ax1.add_idea(walk=tech_road, idea_kid=IdeaKid(_desc=bowl_text))

    ax2 = AgentUnit(_desc=src)
    ax2.add_idea(walk=src, idea_kid=IdeaKid(_desc=tech_text))
    ax2.add_idea(walk=tech_road, idea_kid=IdeaKid(_desc=bowl_text))

    assert ax1.get_idea_kid(road=bowl_road)._weight == 1
    # WHEN
    ax1.meld(ax2)

    # THEN
    assert ax1.get_idea_kid(road=bowl_road)._weight == 1
    assert len(ax1.get_idea_list()) == 3


def test_agent_acptfactunits_meld_BaseScenarioWorks():
    # GIVEN
    src = "casa"
    tech_text = "tech"
    tech_road = f"{src},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{src},{tech_text},{bowl_text}"

    ax1 = AgentUnit(_desc="test7")
    ax1.add_idea(walk=src, idea_kid=IdeaKid(_desc=tech_text))
    ax1.add_idea(walk=tech_road, idea_kid=IdeaKid(_desc=bowl_text))
    ax1.set_acptfact(base=tech_road, pick=bowl_road)

    ax2 = AgentUnit(_desc="test7")
    ax2.add_idea(walk=src, idea_kid=IdeaKid(_desc=tech_text))
    ax2.add_idea(walk=tech_road, idea_kid=IdeaKid(_desc=bowl_text))
    ax2.set_acptfact(base=tech_road, pick=bowl_road)

    # WHEN
    ax1.meld(ax2)

    # THEN
    assert len(ax1._idearoot._acptfactunits) == 1
    assert len(ax1._idearoot._acptfactunits) == len(ax2._idearoot._acptfactunits)
    assert ax1._idearoot._acptfactunits == ax2._idearoot._acptfactunits


def test_agent_acptfactunits_meld_2AcptFactUnitsWorks():
    # GIVEN
    src = "casa"
    tech_text = "tech"
    tech_road = f"{src},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{src},{tech_text},{bowl_text}"
    swim_text = "swim"
    swim_road = f"{src},{swim_text}"
    free_text = "freestyle"

    ax1 = AgentUnit(_desc="test7")
    ax1.add_idea(walk=src, idea_kid=IdeaKid(_desc=tech_text))
    ax1.add_idea(walk=tech_road, idea_kid=IdeaKid(_desc=bowl_text))
    ax1.add_idea(walk=swim_road, idea_kid=IdeaKid(_desc=free_text))
    ax1.set_acptfact(base=tech_road, pick=bowl_road)

    ax2 = AgentUnit(_desc="test7")
    ax2.add_idea(walk=src, idea_kid=IdeaKid(_desc=tech_text))
    ax2.add_idea(walk=tech_road, idea_kid=IdeaKid(_desc=bowl_text))
    ax2.add_idea(walk=swim_road, idea_kid=IdeaKid(_desc=free_text))
    ax2.set_acptfact(base=tech_road, pick=bowl_road)
    ax2.set_acptfact(base=swim_road, pick=swim_road)

    # WHEN
    ax1.meld(ax2)

    # THEN
    assert len(ax1._idearoot._acptfactunits) == 2
    assert len(ax1._idearoot._acptfactunits) == len(ax2._idearoot._acptfactunits)
    assert ax1._idearoot._acptfactunits == ax2._idearoot._acptfactunits


def test_agent_acptfactunits_meld_IdeasMeldedBeforeAcptFacts():
    # GIVEN
    src = "casa"
    swim_text = "swim"
    swim_road = f"{src},{swim_text}"
    free_text = "freestyle"

    ax1 = AgentUnit(_desc="test7")

    ax2 = AgentUnit(_desc="test7")
    ax2.add_idea(walk=swim_road, idea_kid=IdeaKid(_desc=free_text))
    ax2.set_acptfact(base=swim_road, pick=swim_road)

    # WHEN
    ax1.meld(ax2)

    # THEN
    print()
    assert len(ax1._idearoot._acptfactunits) == 1
    assert ax1.get_idea_kid(swim_road)._desc == swim_text
    assert ax1._idearoot._kids[swim_text]._desc == swim_text
    assert len(ax1._idearoot._acptfactunits) == len(ax2._idearoot._acptfactunits)
    assert ax1._idearoot._acptfactunits == ax2._idearoot._acptfactunits


def test_agent_acptfactunits_meld_BrandsMeldedBefore_Allys():
    # GIVEN
    src = "casa"
    ax1 = AgentUnit(_desc=src)
    ax2 = AgentUnit(_desc=src)
    bob = "bob"
    ax2.set_allyunit(allyunit_shop(name=bob))
    assert ax2._brands.get(bob) != None
    assert ax2._brands.get(bob).uid is None
    ax2.set_brandunit(brandunit_shop(name=bob, uid=13))
    assert ax2._brands.get(bob).uid == 13

    # WHEN/THEN
    assert ax1.meld(ax2) is None  # No error raised
    # with pytest_raises(Exception) as excinfo:
    #     ax1.meld(ax2)
    # assert (
    #     str(excinfo.value)
    #     == f"Meld fail BrandUnit bob .uid='None' not the same as .uid='13"
    # )


def test_agent_acptfactunits_meld_AcptFactsAttributeCorrectlySet():
    # GIVEN
    src = "casa"
    swim_text = "swim"
    swim_road = f"{src},{swim_text}"
    free_text = "freestyle"
    free_road = f"{src},{free_text}"

    ax1 = AgentUnit(_desc="test7")
    ax1.add_idea(walk=swim_road, idea_kid=IdeaKid(_desc=free_text))

    ax2 = AgentUnit(_desc="test7")
    ax2.add_idea(walk=swim_road, idea_kid=IdeaKid(_desc=free_text))
    ax2.set_acptfact(base=swim_road, pick=free_road, open=23, nigh=27)

    # WHEN
    ax1.meld(ax2)

    # THEN
    print()
    assert len(ax1._idearoot._acptfactunits) == 1
    assert ax1._idearoot._acptfactunits[swim_road].base == swim_road
    assert ax1._idearoot._acptfactunits[swim_road].pick == free_road
    assert ax1._idearoot._acptfactunits[swim_road].open == 23
    assert ax1._idearoot._acptfactunits[swim_road].nigh == 27


def test_agent_meld_worksCorrectlyForLargeExample():
    # GIVEN
    src = "TlME"
    ax1 = AgentUnit(_desc=src)
    ax1._idearoot._uid = 1
    ax2 = agent_v001()

    ax2r_bl = ax2._idearoot._brandlines
    fam_text = "Family"

    print(
        f"Before {ax2r_bl.get(fam_text)._agent_credit=} {ax2._idearoot._kids_total_weight=}"
    )

    # WHEN
    ax1.meld(ax2)
    ax1.get_tree_metrics()

    # THEN
    print(
        f"After    {ax2r_bl.get(fam_text)._agent_debt=} {ax2._idearoot._kids_total_weight=}"
    )
    assert ax1._weight == ax2._weight
    assert ax1._idearoot._kids == ax2._idearoot._kids
    assert ax1._idearoot._uid == ax2._idearoot._uid
    assert ax1._idearoot._acptfactunits == ax2._idearoot._acptfactunits
    assert ax1._brands == ax2._brands
    assert ax1._allys == ax2._allys

    assert len(ax1._idearoot._acptfactunits) == 2
    assert len(ax1._idearoot._acptfactunits) == len(ax2._idearoot._acptfactunits)
    assert ax1._desc == ax2._desc
    for ax1_brand_key, ax1_brand_obj in ax1._brands.items():
        assert ax1_brand_obj.uid == ax2._brands[ax1_brand_key].uid
        assert ax1_brand_obj == ax2._brands[ax1_brand_key]
    assert ax1._brands == ax2._brands
    assert len(ax1.get_idea_list()) == len(ax2.get_idea_list())

    ax1r_bl = ax1._idearoot._brandlines
    print(
        f"Melded   {ax1r_bl.get(fam_text)._agent_debt=} {ax1._idearoot._kids_total_weight=}"
    )

    assert ax1r_bl.get(fam_text) != None
    # assert ax1r_bl.get(fam_text) == ax2r_bl.get(fam_text)
    # assert ax1r_bl.get(fam_text).agent_credit == ax2r_bl.get(fam_text).agent_credit
    print(f"{ax1r_bl.get(fam_text)._agent_credit=} {ax1._idearoot._kids_total_weight=}")
    print(f"{ax2r_bl.get(fam_text)._agent_credit=} {ax1._idearoot._kids_total_weight=}")
    print(f"  {ax1r_bl.get(fam_text)._agent_debt=} {ax1._idearoot._kids_total_weight=}")
    print(f"  {ax2r_bl.get(fam_text)._agent_debt=} {ax1._idearoot._kids_total_weight=}")
    assert (
        abs(ax1r_bl.get(fam_text)._agent_credit - ax2r_bl.get(fam_text)._agent_credit)
        < 0.0001
    )
    assert (
        abs(ax1r_bl.get(fam_text)._agent_debt - ax2r_bl.get(fam_text)._agent_debt)
        < 0.0001
    )
    for brandline in ax1r_bl.values():
        if brandline.name != fam_text:
            assert brandline == ax2r_bl.get(brandline.name)
    # assert ax1._idearoot._brandlines == ax2._idearoot._brandlines
    # assert ax1._idearoot == ax2._idearoot


def test_agent_meld_make_meldable():
    # GIVEN
    src = "Yahoo"
    ax1 = AgentUnit(_desc=src)
    ax1._idearoot._uid = 1

    ax2 = agent_v001()
    assert ax2._idearoot._desc != ax1._idearoot._desc
    with pytest_raises(Exception) as excinfo:
        assert ax2.meld(other_agent=ax1)
    assert (
        str(excinfo.value)
        == f"Meld fail idearoot _desc '{ax2._desc}' not the same as '{ax1._desc}'"
    )

    # WHEN
    assert ax2._weight == 1
    ax1.make_meldable(starting_digest_agent=ax2)
    assert ax2._idearoot._desc == ax1._idearoot._desc

    # THEN
    assert ax2._weight == 1
    ax2.meld(other_agent=ax1)
    assert ax2._weight == 1


def test_get_on_meld_weight_actions_HasCorrectItems():
    assert len(get_on_meld_weight_actions()) == 5
    assert get_on_meld_weight_actions() == {
        "accept": None,
        "default": None,
        "match": None,
        "override": None,
        "sum": None,
    }
