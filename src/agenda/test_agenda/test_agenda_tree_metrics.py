from src.agenda.examples.example_agendas import (
    agenda_v001,
    get_agenda_with_4_levels,
)
from src.agenda.agenda import agendaunit_shop
from src.agenda.tree_metrics import TreeMetrics
from src.agenda.idea import ideacore_shop


def test_agenda_get_tree_metrics_exists():
    # GIVEN
    tree_metrics = TreeMetrics()
    assert tree_metrics != None

    # WHEN
    x_agenda = agendaunit_shop(_healer="Zia")
    x_agenda_tree_metrics = x_agenda.get_tree_metrics()

    # THEN
    assert x_agenda_tree_metrics.node_count != None
    assert x_agenda_tree_metrics.required_bases != None
    assert x_agenda_tree_metrics.level_count != None
    assert x_agenda_tree_metrics.balancelinks_metrics != None


def test_agenda_get_tree_metrics_get_idea_uid_max_correctlyGetsMaxIdeaUID():
    # GIVEN
    x_agenda = agenda_v001()

    # WHEN
    tree_metrics_x = x_agenda.get_tree_metrics()

    # THEN
    assert tree_metrics_x.uid_max == 279
    assert x_agenda.get_idea_uid_max() == 279


def test_agenda_get_tree_metrics_all_idea_uids_are_unique_IsCorrectBoolean():
    # GIVEN
    x_agenda = agenda_v001()

    # WHEN
    tree_metrics_x = x_agenda.get_tree_metrics()

    # THEN
    assert tree_metrics_x.all_idea_uids_are_unique == False
    assert len(tree_metrics_x.uid_dict) == 219


def test_agenda_get_tree_set_all_idea_uids_unique():
    # GIVEN
    x_agenda = agenda_v001()
    tree_metrics_before = x_agenda.get_tree_metrics()
    assert len(tree_metrics_before.uid_dict) == 219

    # WHEN
    x_agenda.set_all_idea_uids_unique()

    # THEN
    tree_metrics_after = x_agenda.get_tree_metrics()
    # for uid, uid_count in tree_metrics_after.uid_dict.items():
    #     # print(f"{uid=} {uid_count=} {len(x_agenda.get_idea_list())=}")
    #     print(f"{uid=} {uid_count=} ")
    assert len(tree_metrics_after.uid_dict) == 253
    assert tree_metrics_after.all_idea_uids_are_unique == True


def test_agenda_agenda_get_tree_metrics_sets_uids_correctly():
    # GIVEN
    healer_text = "Zia"
    x_agenda = agendaunit_shop(_healer=healer_text)
    swim_text = "swim"
    pad_text = "pad"
    x_agenda.add_idea(ideacore_shop(swim_text, _uid=None), x_agenda._economy_id)
    x_agenda.add_idea(ideacore_shop(pad_text, _uid=2), x_agenda._economy_id)
    swim_road = x_agenda.make_l1_road(swim_text)
    assert x_agenda.get_idea_kid(swim_road)._uid is None

    x_agenda.set_all_idea_uids_unique()

    # THEN
    assert x_agenda.get_idea_kid(swim_road)._uid != None


def test_agenda_get_tree_metrics_ReturnsANoneActionIdeaRoadUnit():
    # GIVEN
    healer_text = "Nia"
    x_agenda = agendaunit_shop(healer_text, _weight=10)
    weekdays = "weekdays"
    x_agenda.add_idea(ideacore_shop(weekdays, _weight=40), x_agenda._economy_id)
    tree_metrics_before = x_agenda.get_tree_metrics()

    # WHEN/THEN
    assert tree_metrics_before.an_promise_idea_road is None


def test_agenda_get_tree_metrics_ReturnsAnActionIdeaRoadUnit():
    # GIVEN
    x_agenda = agenda_v001()
    tree_metrics_before = x_agenda.get_tree_metrics()

    # WHEN/THEN
    train_road = x_agenda.make_road(
        road_nodes=[
            x_agenda._economy_id,
            "ACME",
            "ACME Employee Responsiblities",
            "Know Abuse Prevention and Reporting guildlines",
            "Take Fall 2021 training",
        ]
    )
    assert tree_metrics_before.an_promise_idea_road == train_road
