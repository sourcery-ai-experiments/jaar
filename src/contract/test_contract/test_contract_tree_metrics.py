from src.contract.examples.example_contracts import (
    contract_v001,
    get_contract_with_4_levels,
)
from src.contract.contract import ContractUnit
from src.contract.tree_metrics import TreeMetrics
from src.contract.idea import IdeaKid


def test_contract_get_tree_metrics_exists():
    # GIVEN
    tree_metrics = TreeMetrics()
    assert tree_metrics != None

    # WHEN
    cx = ContractUnit(_healer="Zia")
    cx_tree_metrics = cx.get_tree_metrics()

    # THEN
    assert cx_tree_metrics.node_count != None
    assert cx_tree_metrics.required_bases != None
    assert cx_tree_metrics.level_count != None
    assert cx_tree_metrics.balancelinks_metrics != None


def test_contract_get_tree_metrics_get_idea_uid_max_correctlyGetsMaxIdeaUID():
    # GIVEN
    cx = contract_v001()

    # WHEN
    tree_metrics_x = cx.get_tree_metrics()

    # THEN
    assert tree_metrics_x.uid_max == 279
    assert cx.get_idea_uid_max() == 279


def test_contract_get_tree_metrics_all_idea_uids_are_unique_IsCorrectBoolean():
    # GIVEN
    cx = contract_v001()

    # WHEN
    tree_metrics_x = cx.get_tree_metrics()

    # THEN
    assert tree_metrics_x.all_idea_uids_are_unique == False
    assert len(tree_metrics_x.uid_dict) == 219


def test_contract_get_tree_set_all_idea_uids_unique():
    # GIVEN
    cx = contract_v001()
    tree_metrics_before = cx.get_tree_metrics()
    assert len(tree_metrics_before.uid_dict) == 219

    # WHEN
    cx.set_all_idea_uids_unique()

    # THEN
    tree_metrics_after = cx.get_tree_metrics()
    # for uid, uid_count in tree_metrics_after.uid_dict.items():
    #     # print(f"{uid=} {uid_count=} {len(cx.get_idea_list())=}")
    #     print(f"{uid=} {uid_count=} ")
    assert len(tree_metrics_after.uid_dict) == 253
    assert tree_metrics_after.all_idea_uids_are_unique == True


def test_contract_contract_get_tree_metrics_sets_uids_correctly():
    # GIVEN
    healer_text = "Zia"
    cx = ContractUnit(_healer=healer_text)
    swim_text = "swim"
    walk_text = "walk"
    cx.add_idea(idea_kid=IdeaKid(_label=swim_text, _uid=None), walk=cx._healing_kind)
    cx.add_idea(idea_kid=IdeaKid(_label=walk_text, _uid=2), walk=cx._healing_kind)
    assert cx.get_idea_kid(road=f"{cx._healing_kind},{swim_text}")._uid is None

    cx.set_all_idea_uids_unique()

    # THEN
    assert cx.get_idea_kid(road=f"{cx._healing_kind},{swim_text}")._uid != None


def test_contract_get_tree_metrics_ReturnsAccurateActionIdeaCount():
    # GIVEN
    cx = contract_v001()
    tree_metrics_before = cx.get_tree_metrics()
    assert tree_metrics_before.bond_promise_count == 69

    # WHEN
    cx.add_idea(idea_kid=IdeaKid(_label="clean", promise=True), walk=f"{cx._healer}")

    # THEN
    tree_metrics_after = cx.get_tree_metrics()
    assert tree_metrics_after.bond_promise_count == 70


def test_contract_get_tree_metrics_ReturnsANoneActionIdeaRoad():
    # GIVEN
    healer_text = "Nia"
    cx = ContractUnit(_healer=healer_text, _weight=10)
    weekdays = "weekdays"
    idea_kid_weekdays = IdeaKid(_weight=40, _label=weekdays)
    cx.add_idea(idea_kid=idea_kid_weekdays, walk=f"{cx._healing_kind}")
    tree_metrics_before = cx.get_tree_metrics()
    # WHEN/THEN
    assert tree_metrics_before.an_promise_idea_road is None


def test_contract_get_tree_metrics_ReturnsAnActionIdeaRoad():
    # GIVEN
    cx = contract_v001()
    tree_metrics_before = cx.get_tree_metrics()
    # WHEN/THEN
    assert (
        tree_metrics_before.an_promise_idea_road
        == f"{cx._healing_kind},ACME,ACME Employee Responsiblities,Know Abuse Prevention and Reporting guildlines,Take Fall 2021 training"
    )
