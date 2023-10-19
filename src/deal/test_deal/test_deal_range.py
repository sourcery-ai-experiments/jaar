from src.deal.idea import IdeaKid
from src.deal.deal import dealunit_shop


def test_dealAddingIdeaWithAddinCorrectlyTransformsRangeScenario1():
    # Given
    healer_text = "Mia"
    x_deal = dealunit_shop(_healer=healer_text, _weight=10)

    l1 = "level1"
    idea_kid_l1 = IdeaKid(_weight=30, _label=l1)
    x_deal.add_idea(pad=x_deal._project_handle, idea_kid=idea_kid_l1)
    l1_road = f"{x_deal._project_handle},{l1}"

    rx1 = "range_root_example"
    idea_kid_rx1 = IdeaKid(_weight=30, _label=rx1)
    x_deal.add_idea(pad=l1_road, idea_kid=idea_kid_rx1)
    rx1_road = f"{l1_road},{rx1}"
    x_deal.edit_idea_attr(road=rx1_road, begin=10, close=25)

    y_idea = x_deal.get_idea_kid(road=rx1_road)
    print(f"Add example child idea to road='{rx1_road}'")

    rcA = "range_child_example"
    idea_kid_rcA = IdeaKid(_weight=30, _begin=10, _close=25, _label=rcA)
    x_deal.add_idea(pad=rx1_road, idea_kid=idea_kid_rcA)

    rcA_road = f"{rx1_road},{rcA}"
    x_idea = x_deal.get_idea_kid(road=rcA_road)

    assert x_idea._begin == 10
    assert x_idea._close == 25

    # When
    x_deal.edit_idea_attr(road=rcA_road, addin=7)

    # Then
    assert x_idea._begin == 17
    assert x_idea._close == 32


def test_dealAddingIdeaWithAddinCorrectlyTransformsRangeScenario2():
    # Given
    healer_text = "Bob"
    x_deal = dealunit_shop(_healer=healer_text, _weight=10)

    l1 = "level1"
    idea_kid_l1 = IdeaKid(_weight=30, _label=l1)
    x_deal.add_idea(pad=x_deal._project_handle, idea_kid=idea_kid_l1)
    l1_road = f"{x_deal._project_handle},{l1}"

    rx1 = "range_root_example"
    idea_kid_rx1 = IdeaKid(_weight=30, _label=rx1)
    x_deal.add_idea(pad=l1_road, idea_kid=idea_kid_rx1)
    rx1_road = f"{l1_road},{rx1}"
    x_deal.edit_idea_attr(road=rx1_road, begin=10, close=25)

    y_idea = x_deal.get_idea_kid(road=rx1_road)
    print(f"Add example child idea to road='{rx1_road}'")

    rcA = "range_child_example"
    idea_kid_rcA = IdeaKid(_weight=30, _begin=10, _close=25, _label=rcA)
    x_deal.add_idea(pad=rx1_road, idea_kid=idea_kid_rcA)

    rcA_road = f"{rx1_road},{rcA}"
    x_idea = x_deal.get_idea_kid(road=rcA_road)

    assert x_idea._begin == 10
    assert x_idea._close == 25
    assert x_idea._addin is None

    # When
    x_deal.edit_idea_attr(road=rcA_road, addin=15, denom=5)

    # Then
    assert x_idea._begin == 5
    assert x_idea._close == 8
    assert x_idea._addin == 15
    assert x_idea._denom == 5


def test_get_idea_ranged_kids_CorrectlyReturnsAllChildren():
    # GIVEN
    healer_text = "Noa"
    x_deal = dealunit_shop(_healer=healer_text)
    x_deal.set_time_hreg_ideas(c400_count=7)

    # WHEN
    weekunit_road = f"{x_deal._project_handle},time,tech,week"
    ranged_ideas = x_deal.get_idea_ranged_kids(idea_road=weekunit_road)

    # # THEN
    assert len(ranged_ideas) == 7


def test_get_idea_ranged_kids_CorrectlyReturnsSomeChildrenScen1():
    # GIVEN
    healer_text = "Noa"
    x_deal = dealunit_shop(_healer=healer_text)
    x_deal.set_time_hreg_ideas(c400_count=7)

    # WHEN
    weekunit_road = f"{x_deal._project_handle},time,tech,week"
    begin_x = 1440
    close_x = 4 * 1440
    ranged_ideas = x_deal.get_idea_ranged_kids(
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
    healer_text = "Noa"
    x_deal = dealunit_shop(_healer=healer_text)
    x_deal.set_time_hreg_ideas(c400_count=7)

    # WHEN THEN
    week_road = f"{x_deal._project_handle},time,tech,week"
    assert (
        len(x_deal.get_idea_ranged_kids(idea_road=week_road, begin=0, close=1440)) == 1
    )
    assert (
        len(x_deal.get_idea_ranged_kids(idea_road=week_road, begin=0, close=2000)) == 2
    )
    assert (
        len(x_deal.get_idea_ranged_kids(idea_road=week_road, begin=0, close=3000)) == 3
    )


def test_get_idea_ranged_kids_CorrectlyReturnsSomeChildrenScen3():
    # GIVEN
    healer_text = "Noa"
    x_deal = dealunit_shop(_healer=healer_text)
    x_deal.set_time_hreg_ideas(c400_count=7)

    # WHEN THEN
    week_road = f"{x_deal._project_handle},time,tech,week"
    assert len(x_deal.get_idea_ranged_kids(idea_road=week_road, begin=0)) == 1
    assert len(x_deal.get_idea_ranged_kids(idea_road=week_road, begin=1440)) == 1
