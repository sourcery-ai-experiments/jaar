from src.agent.examples.example_agents import (
    get_agent_1Task_1CE0MinutesRequired_1AcptFact,
)
from src.agent.agent import AgentUnit
from pytest import raises as pytest_raises


def test_agent_exists():
    new_obj = AgentUnit()
    assert new_obj
    assert new_obj._weight == 1
    assert new_obj._max_tree_traverse == 3
    assert new_obj._tree_traverse_count is None
    assert new_obj._rational == False
    assert str(type(new_obj._toolroot)).find(".tool.ToolRoot'>")


def test_agent_IsAbleToSetTaskAsComplete():
    agent_x = get_agent_1Task_1CE0MinutesRequired_1AcptFact()

    assert agent_x != None
    assert len(agent_x._toolroot._kids["obtain mail"]._requiredunits) == 1
    tool_list = agent_x.get_tool_list()
    # for tool in tool_list:
    #     print(tool._desc)
    mail_tool = tool_list[1]
    assert mail_tool.promise == True
    assert mail_tool._task == True

    ced_min_desc = "CE0_minutes"
    ced_road = f"test45,{ced_min_desc}"
    agent_x.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    tool_list = agent_x.get_tool_list()
    assert mail_tool.promise == True
    assert mail_tool._task == False


def test_agent_IsAbleToEditAcptFactUnitAnyAncestor_Tool_1():
    agent_x = get_agent_1Task_1CE0MinutesRequired_1AcptFact()
    ced_min_desc = "CE0_minutes"
    ced_road = f"test45,{ced_min_desc}"
    agent_x.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=85)
    tool_list = agent_x.get_tool_list()
    mail_tool = tool_list[1]
    assert mail_tool.promise == True
    assert mail_tool._task == False

    agent_x.set_acptfact(base=ced_road, pick=ced_road, open=82, nigh=95)
    tool_list = agent_x.get_tool_list()
    mail_tool = tool_list[1]
    assert mail_tool.promise == True
    assert mail_tool._task == True


def test_agent_tooloot_uid_isAlwaysEqualTo1():
    # GIVEN
    src_text = "testing_lw"
    src_road = src_text

    # WHEN
    sx = AgentUnit(_desc=src_text)

    # THEN
    assert sx._toolroot._uid == 1


def test_agent_set_max_tree_traverse_CorrectlySetsInt():
    # GIVEN
    src_text = "testing_lw"
    sx = AgentUnit(_desc=src_text)
    assert sx._max_tree_traverse == 3

    # WHEN
    sx.set_max_tree_traverse(int_x=11)

    # THEN
    assert sx._max_tree_traverse == 11


def test_agent_set_max_tree_traverse_CorrectlyRaisesError():
    # GIVEN
    src_text = "testing_lw"
    sx = AgentUnit(_desc=src_text)
    assert sx._max_tree_traverse == 3

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        sx.set_max_tree_traverse(int_x=1)
    assert (
        str(excinfo.value)
        == "set_max_tree_traverse: input '1' must be number that is 2 or greater"
    )
