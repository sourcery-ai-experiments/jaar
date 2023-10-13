from src.contract.idea import IdeaKid
from src.contract.contract import ContractUnit


def test_contractAddingIdeaWithAddinCorrectlyTransformsRangeScenario1():
    # Given
    owner_text = "Mia"
    cx = ContractUnit(_owner=owner_text, _weight=10)

    l1 = "level1"
    idea_kid_l1 = IdeaKid(_weight=30, _label=l1)
    cx.add_idea(walk=cx._heal_kind, idea_kid=idea_kid_l1)
    l1_road = f"{cx._heal_kind},{l1}"

    rx1 = "range_root_example"
    idea_kid_rx1 = IdeaKid(_weight=30, _label=rx1)
    cx.add_idea(walk=l1_road, idea_kid=idea_kid_rx1)
    rx1_road = f"{l1_road},{rx1}"
    cx.edit_idea_attr(road=rx1_road, begin=10, close=25)

    y_idea = cx.get_idea_kid(road=rx1_road)
    print(f"Add example child idea to road='{rx1_road}'")

    rcA = "range_child_example"
    idea_kid_rcA = IdeaKid(_weight=30, _begin=10, _close=25, _label=rcA)
    cx.add_idea(walk=rx1_road, idea_kid=idea_kid_rcA)

    rcA_road = f"{rx1_road},{rcA}"
    x_idea = cx.get_idea_kid(road=rcA_road)

    assert x_idea._begin == 10
    assert x_idea._close == 25

    # When
    cx.edit_idea_attr(road=rcA_road, addin=7)

    # Then
    assert x_idea._begin == 17
    assert x_idea._close == 32


def test_contractAddingIdeaWithAddinCorrectlyTransformsRangeScenario2():
    # Given
    owner_text = "Bob"
    cx = ContractUnit(_owner=owner_text, _weight=10)

    l1 = "level1"
    idea_kid_l1 = IdeaKid(_weight=30, _label=l1)
    cx.add_idea(walk=cx._heal_kind, idea_kid=idea_kid_l1)
    l1_road = f"{cx._heal_kind},{l1}"

    rx1 = "range_root_example"
    idea_kid_rx1 = IdeaKid(_weight=30, _label=rx1)
    cx.add_idea(walk=l1_road, idea_kid=idea_kid_rx1)
    rx1_road = f"{l1_road},{rx1}"
    cx.edit_idea_attr(road=rx1_road, begin=10, close=25)

    y_idea = cx.get_idea_kid(road=rx1_road)
    print(f"Add example child idea to road='{rx1_road}'")

    rcA = "range_child_example"
    idea_kid_rcA = IdeaKid(_weight=30, _begin=10, _close=25, _label=rcA)
    cx.add_idea(walk=rx1_road, idea_kid=idea_kid_rcA)

    rcA_road = f"{rx1_road},{rcA}"
    x_idea = cx.get_idea_kid(road=rcA_road)

    assert x_idea._begin == 10
    assert x_idea._close == 25
    assert x_idea._addin is None

    # When
    cx.edit_idea_attr(road=rcA_road, addin=15, denom=5)

    # Then
    assert x_idea._begin == 5
    assert x_idea._close == 8
    assert x_idea._addin == 15
    assert x_idea._denom == 5


def test_get_idea_ranged_kids_CorrectlyReturnsAllChildren():
    # GIVEN
    owner_text = "Noa"
    cx = ContractUnit(_owner=owner_text)
    cx.set_time_hreg_ideas(c400_count=7)

    # WHEN
    weekunit_road = f"{cx._heal_kind},time,tech,week"
    ranged_ideas = cx.get_idea_ranged_kids(idea_road=weekunit_road)

    # # THEN
    assert len(ranged_ideas) == 7


def test_get_idea_ranged_kids_CorrectlyReturnsSomeChildrenScen1():
    # GIVEN
    owner_text = "Noa"
    cx = ContractUnit(_owner=owner_text)
    cx.set_time_hreg_ideas(c400_count=7)

    # WHEN
    weekunit_road = f"{cx._heal_kind},time,tech,week"
    begin_x = 1440
    close_x = 4 * 1440
    ranged_ideas = cx.get_idea_ranged_kids(
        idea_road=weekunit_road, begin=begin_x, close=close_x
    )

    # THEN
    # for idea_x in ranged_ideas.values():
    #     print(
    #         f"{begin_x=} {close_x=} {idea_x._label=} {idea_x._begin=} {idea_x._close=} "
    #     )
    assert len(ranged_ideas) == 3


def test_get_idea_ranged_kids_CorrectlyReturnsSomeChildrenScen2():
    # GIVEN
    owner_text = "Noa"
    cx = ContractUnit(_owner=owner_text)
    cx.set_time_hreg_ideas(c400_count=7)

    # WHEN THEN
    week_road = f"{cx._heal_kind},time,tech,week"
    assert len(cx.get_idea_ranged_kids(idea_road=week_road, begin=0, close=1440)) == 1
    assert len(cx.get_idea_ranged_kids(idea_road=week_road, begin=0, close=2000)) == 2
    assert len(cx.get_idea_ranged_kids(idea_road=week_road, begin=0, close=3000)) == 3


def test_get_idea_ranged_kids_CorrectlyReturnsSomeChildrenScen3():
    # GIVEN
    owner_text = "Noa"
    cx = ContractUnit(_owner=owner_text)
    cx.set_time_hreg_ideas(c400_count=7)

    # WHEN THEN
    week_road = f"{cx._heal_kind},time,tech,week"
    assert len(cx.get_idea_ranged_kids(idea_road=week_road, begin=0)) == 1
    assert len(cx.get_idea_ranged_kids(idea_road=week_road, begin=1440)) == 1
