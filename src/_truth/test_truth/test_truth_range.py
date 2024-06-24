from src._truth.idea import ideaunit_shop
from src._truth.truth import truthunit_shop


def test_truthAddingIdeaWithAddinCorrectlyTransformsRangeScenario1():
    # GIVEN
    mia_truth = truthunit_shop("Mia", _weight=10)

    l1 = "level1"
    mia_truth.add_l1_idea(ideaunit_shop(l1, _weight=30))
    l1_road = mia_truth.make_l1_road(l1)

    rx1 = "range_root_example"
    mia_truth.add_idea(ideaunit_shop(rx1, _weight=30), parent_road=l1_road)
    rx1_road = mia_truth.make_road(l1_road, rx1)
    mia_truth.edit_idea_attr(road=rx1_road, begin=10, close=25)

    y_idea = mia_truth.get_idea_obj(rx1_road)
    print(f"Add example child idea to road='{rx1_road}'")

    rcA = "range_child_example"
    mia_truth.add_idea(ideaunit_shop(rcA, _weight=30, _begin=10, _close=25), rx1_road)

    rcA_road = mia_truth.make_road(rx1_road, rcA)
    x_idea = mia_truth.get_idea_obj(rcA_road)

    assert x_idea._begin == 10
    assert x_idea._close == 25

    # WHEN
    mia_truth.edit_idea_attr(road=rcA_road, addin=7)

    # THEN
    assert x_idea._begin == 17
    assert x_idea._close == 32


def test_truthAddingIdeaWithAddinCorrectlyTransformsRangeScenario2():
    # GIVEN
    bob_truth = truthunit_shop(_owner_id="Bob", _weight=10)

    l1 = "level1"
    bob_truth.add_l1_idea(ideaunit_shop(l1, _weight=30))
    l1_road = bob_truth.make_l1_road(l1)

    rx1 = "range_root_example"
    bob_truth.add_idea(ideaunit_shop(rx1, _weight=30), parent_road=l1_road)
    rx1_road = bob_truth.make_road(l1_road, rx1)
    bob_truth.edit_idea_attr(road=rx1_road, begin=10, close=25)

    y_idea = bob_truth.get_idea_obj(rx1_road)
    print(f"Add example child idea to road='{rx1_road}'")

    rcA = "range_child_example"
    bob_truth.add_idea(ideaunit_shop(rcA, _weight=30, _begin=10, _close=25), rx1_road)

    rcA_road = bob_truth.make_road(rx1_road, rcA)
    x_idea = bob_truth.get_idea_obj(rcA_road)

    assert x_idea._begin == 10
    assert x_idea._close == 25
    assert x_idea._addin is None

    # WHEN
    bob_truth.edit_idea_attr(road=rcA_road, addin=15, denom=5)

    # THEN
    assert x_idea._begin == 5
    assert x_idea._close == 8
    assert x_idea._addin == 15
    assert x_idea._denom == 5


def test_get_idea_ranged_kids_ReturnsAllChildren():
    # GIVEN
    noa_truth = truthunit_shop("Noa")
    noa_truth.set_time_hreg_ideas(c400_count=7)

    # WHEN
    time_road = noa_truth.make_l1_road("time")
    tech_road = noa_truth.make_road(time_road, "tech")
    week_road = noa_truth.make_road(tech_road, "week")
    ranged_ideas = noa_truth.get_idea_ranged_kids(idea_road=week_road)

    # # THEN
    assert len(ranged_ideas) == 7


def test_get_idea_ranged_kids_ReturnsSomeChildrenScen1():
    # GIVEN
    noa_truth = truthunit_shop("Noa")
    noa_truth.set_time_hreg_ideas(c400_count=7)

    # WHEN
    time_road = noa_truth.make_l1_road("time")
    tech_road = noa_truth.make_road(time_road, "tech")
    week_road = noa_truth.make_road(tech_road, "week")
    begin_x = 1440
    close_x = 4 * 1440
    ranged_ideas = noa_truth.get_idea_ranged_kids(week_road, begin_x, close_x)

    # THEN
    # for idea_x in ranged_ideas.values():
    #     print(
    #         f"{begin_x=} {close_x=} {idea_x._label=} {idea_x._begin=} {idea_x._close=} "
    #     )
    assert len(ranged_ideas) == 3


def test_get_idea_ranged_kids_ReturnsSomeChildrenScen2():
    # GIVEN
    noa_truth = truthunit_shop("Noa")
    noa_truth.set_time_hreg_ideas(c400_count=7)

    # WHEN THEN
    time_road = noa_truth.make_l1_road("time")
    tech_road = noa_truth.make_road(time_road, "tech")
    week_road = noa_truth.make_road(tech_road, "week")
    assert len(noa_truth.get_idea_ranged_kids(week_road, begin=0, close=1440)) == 1
    assert len(noa_truth.get_idea_ranged_kids(week_road, begin=0, close=2000)) == 2
    assert len(noa_truth.get_idea_ranged_kids(week_road, begin=0, close=3000)) == 3


def test_get_idea_ranged_kids_ReturnsSomeChildrenScen3():
    # GIVEN
    noa_truth = truthunit_shop("Noa")
    noa_truth.set_time_hreg_ideas(c400_count=7)

    # WHEN THEN
    time_road = noa_truth.make_l1_road("time")
    tech_road = noa_truth.make_road(time_road, "tech")
    week_road = noa_truth.make_road(tech_road, "week")
    assert len(noa_truth.get_idea_ranged_kids(idea_road=week_road, begin=0)) == 1
    assert len(noa_truth.get_idea_ranged_kids(idea_road=week_road, begin=1440)) == 1
