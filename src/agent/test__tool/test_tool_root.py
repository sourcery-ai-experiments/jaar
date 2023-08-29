from src.agent.tool import ToolRoot


def test_tool_core_exists():
    new_obj = ToolRoot()
    assert new_obj
    assert new_obj._kids is None
