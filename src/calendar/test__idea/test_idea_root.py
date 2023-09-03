from src.calendar.idea import IdeaRoot
from src.calendar.road import get_global_root_desc as root_desc
from pytest import raises as pytest_raises


def test_IdeaRoot_exists():
    # GIVEN / WHEN
    new_obj = IdeaRoot()

    # THEN
    assert new_obj

    assert new_obj._desc == root_desc()
    assert new_obj._kids is None


def test_IdeaRoot_set_idea_desc_DoesNotRaisesError():
    # GIVEN
    new_obj = IdeaRoot()

    # WHEN

    new_obj.set_idea_desc(desc=root_desc())

    # THEN
    assert new_obj._desc == root_desc()


def test_IdeaRoot_set_idea_desc_RaisesError():
    # GIVEN
    new_obj = IdeaRoot()

    # WHEN/THEN

    with pytest_raises(Exception) as excinfo:
        src_text = "src"
        new_obj.set_idea_desc(desc=src_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{root_desc()}'"
    )
