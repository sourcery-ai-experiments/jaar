from src.agent.idea import IdeaRoot


def test_idea_core_exists():
    new_obj = IdeaRoot()
    assert new_obj
    assert new_obj._kids is None
