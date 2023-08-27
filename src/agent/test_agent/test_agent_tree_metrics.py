from src.agent.examples.example_agents import agent_v001, get_agent_with_4_levels
from src.agent.agent import AgentUnit
from src.agent.tree_metrics import TreeMetrics
from src.agent.idea import IdeaKid


def test_agent_get_tree_metrics_exists():
    # GIVEN
    tree_metrics = TreeMetrics()
    assert tree_metrics != None

    # WHEN
    sx = AgentUnit(_desc="testing_lw")
    sx_tree_metrics = sx.get_tree_metrics()

    # THEN
    assert sx_tree_metrics.nodeCount != None
    assert sx_tree_metrics.required_bases != None
    assert sx_tree_metrics.levelCount != None
    assert sx_tree_metrics.grouplinks_metrics != None


def test_agent_get_tree_metrics_get_idea_uid_max_correctlyGetsMaxIdeaUID():
    # GIVEN
    sx = agent_v001()

    # WHEN
    tree_metrics_x = sx.get_tree_metrics()

    # THEN
    assert tree_metrics_x.uid_max == 279
    assert sx.get_idea_uid_max() == 279


def test_agent_get_tree_metrics_all_idea_uids_are_unique_IsCorrectBoolean():
    # GIVEN
    sx = agent_v001()

    # WHEN
    tree_metrics_x = sx.get_tree_metrics()

    # THEN
    assert tree_metrics_x.all_idea_uids_are_unique == False
    assert len(tree_metrics_x.uid_dict) == 219


def test_agent_get_tree_set_all_idea_uids_unique():
    # GIVEN
    sx = agent_v001()
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


def test_agent_agent_get_tree_metrics_assigns_uids_correctly():
    # GIVEN
    src_text = "testing_lw"
    src_road = src_text
    sx = AgentUnit(_desc=src_text)
    swim_text = "swim"
    walk_text = "walk"
    sx.add_idea(idea_kid=IdeaKid(_desc=swim_text, _uid=None), walk=src_road)
    sx.add_idea(idea_kid=IdeaKid(_desc=walk_text, _uid=2), walk=src_road)
    assert sx.get_idea_kid(road=f"{src_road},{swim_text}")._uid is None

    sx.set_all_idea_uids_unique()

    # THEN
    assert sx.get_idea_kid(road=f"{src_road},{swim_text}")._uid != None


def test_agent_get_tree_metrics_ReturnsAccurateActionIdeaCount():
    # GIVEN
    cx = agent_v001()
    tree_metrics_before = cx.get_tree_metrics()
    assert tree_metrics_before.bond_promise_count == 69

    # WHEN
    cx.add_idea(idea_kid=IdeaKid(_desc="clean", promise=True), walk=f"{cx._desc}")

    # THEN
    tree_metrics_after = cx.get_tree_metrics()
    assert tree_metrics_after.bond_promise_count == 70


def test_agent_get_tree_metrics_ReturnsANoneActionIdeaRoad():
    # GIVEN
    src = "src"
    cx = AgentUnit(_weight=10, _desc=src)
    weekdays = "weekdays"
    idea_kid_weekdays = IdeaKid(_weight=40, _desc=weekdays)
    cx.add_idea(idea_kid=idea_kid_weekdays, walk=f"{src}")
    tree_metrics_before = cx.get_tree_metrics()
    # WHEN/THEN
    assert tree_metrics_before.an_promise_idea_road is None


def test_agent_get_tree_metrics_ReturnsAnActionIdeaRoad():
    # GIVEN
    cx = agent_v001()
    tree_metrics_before = cx.get_tree_metrics()
    # WHEN/THEN
    assert (
        tree_metrics_before.an_promise_idea_road
        == "TlME,ACME,ACME Employee Responsiblities,Know Abuse Prevention and Reporting guildlines,Take Fall 2021 training"
    )
