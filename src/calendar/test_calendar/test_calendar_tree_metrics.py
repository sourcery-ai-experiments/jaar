from src.calendar.examples.example_calendars import (
    calendar_v001,
    get_calendar_with_4_levels,
)
from src.calendar.calendar import CalendarUnit
from src.calendar.tree_metrics import TreeMetrics
from src.calendar.idea import IdeaKid
from src.calendar.road import get_global_root_label as root_label


def test_calendar_get_tree_metrics_exists():
    # GIVEN
    tree_metrics = TreeMetrics()
    assert tree_metrics != None

    # WHEN
    sx = CalendarUnit(_owner="Zia")
    sx_tree_metrics = sx.get_tree_metrics()

    # THEN
    assert sx_tree_metrics.nodeCount != None
    assert sx_tree_metrics.required_bases != None
    assert sx_tree_metrics.levelCount != None
    assert sx_tree_metrics.grouplinks_metrics != None


def test_calendar_get_tree_metrics_get_idea_uid_max_correctlyGetsMaxIdeaUID():
    # GIVEN
    sx = calendar_v001()

    # WHEN
    tree_metrics_x = sx.get_tree_metrics()

    # THEN
    assert tree_metrics_x.uid_max == 279
    assert sx.get_idea_uid_max() == 279


def test_calendar_get_tree_metrics_all_idea_uids_are_unique_IsCorrectBoolean():
    # GIVEN
    sx = calendar_v001()

    # WHEN
    tree_metrics_x = sx.get_tree_metrics()

    # THEN
    assert tree_metrics_x.all_idea_uids_are_unique == False
    assert len(tree_metrics_x.uid_dict) == 219


def test_calendar_get_tree_set_all_idea_uids_unique():
    # GIVEN
    sx = calendar_v001()
    tree_metrics_before = sx.get_tree_metrics()
    assert len(tree_metrics_before.uid_dict) == 219

    # WHEN
    sx.set_all_idea_uids_unique()

    # THEN
    tree_metrics_after = sx.get_tree_metrics()
    # for uid, uid_count in tree_metrics_after.uid_dict.items():
    #     # print(f"{uid=} {uid_count=} {len(sx.get_idea_list())=}")
    #     print(f"{uid=} {uid_count=} ")
    assert len(tree_metrics_after.uid_dict) == 253
    assert tree_metrics_after.all_idea_uids_are_unique == True


def test_calendar_calendar_get_tree_metrics_sets_uids_correctly():
    # GIVEN
    owner_text = "Zia"
    sx = CalendarUnit(_owner=owner_text)
    swim_text = "swim"
    walk_text = "walk"
    sx.add_idea(idea_kid=IdeaKid(_label=swim_text, _uid=None), walk=root_label())
    sx.add_idea(idea_kid=IdeaKid(_label=walk_text, _uid=2), walk=root_label())
    assert sx.get_idea_kid(road=f"{root_label()},{swim_text}")._uid is None

    sx.set_all_idea_uids_unique()

    # THEN
    assert sx.get_idea_kid(road=f"{root_label()},{swim_text}")._uid != None


def test_calendar_get_tree_metrics_ReturnsAccurateActionIdeaCount():
    # GIVEN
    cx = calendar_v001()
    tree_metrics_before = cx.get_tree_metrics()
    assert tree_metrics_before.bond_promise_count == 69

    # WHEN
    cx.add_idea(idea_kid=IdeaKid(_label="clean", promise=True), walk=f"{cx._owner}")

    # THEN
    tree_metrics_after = cx.get_tree_metrics()
    assert tree_metrics_after.bond_promise_count == 70


def test_calendar_get_tree_metrics_ReturnsANoneActionIdeaRoad():
    # GIVEN
    owner_text = "Nia"
    cx = CalendarUnit(_owner=owner_text, _weight=10)
    weekdays = "weekdays"
    idea_kid_weekdays = IdeaKid(_weight=40, _label=weekdays)
    cx.add_idea(idea_kid=idea_kid_weekdays, walk=f"{root_label()}")
    tree_metrics_before = cx.get_tree_metrics()
    # WHEN/THEN
    assert tree_metrics_before.an_promise_idea_road is None


def test_calendar_get_tree_metrics_ReturnsAnActionIdeaRoad():
    # GIVEN
    cx = calendar_v001()
    tree_metrics_before = cx.get_tree_metrics()
    # WHEN/THEN
    assert (
        tree_metrics_before.an_promise_idea_road
        == f"{root_label()},ACME,ACME Employee Responsiblities,Know Abuse Prevention and Reporting guildlines,Take Fall 2021 training"
    )
