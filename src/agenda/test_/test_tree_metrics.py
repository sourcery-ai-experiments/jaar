from src.agenda.examples.example_agendas import agenda_v001, get_agenda_with_4_levels
from src.agenda.agenda import agendaunit_shop
from src.agenda.tree_metrics import TreeMetrics, treemetrics_shop
from src.agenda.idea import ideaunit_shop
from src._prime.road import create_road_from_nodes


def test_TreeMetrics_Exists():
    # GIVEN / WHEN
    x_tree_metrics = TreeMetrics()

    # THEN
    assert x_tree_metrics != None
    assert x_tree_metrics.node_count is None
    assert x_tree_metrics.level_count is None
    assert x_tree_metrics.reason_bases is None
    assert x_tree_metrics.balancelinks_metrics is None
    assert x_tree_metrics.uid_max is None
    assert x_tree_metrics.uid_dict is None
    assert x_tree_metrics.all_idea_uids_are_unique is None


def test_treemetrics_shop_ReturnsCorrectObj():
    # GIVEN / WHEN
    x_tree_metrics = treemetrics_shop()

    # THEN
    assert x_tree_metrics != None
    assert x_tree_metrics.node_count == 0
    assert x_tree_metrics.level_count == {}
    assert x_tree_metrics.reason_bases == {}
    assert x_tree_metrics.balancelinks_metrics == {}
    assert x_tree_metrics.uid_max == 0
    assert x_tree_metrics.uid_dict == {}
    assert x_tree_metrics.all_idea_uids_are_unique
