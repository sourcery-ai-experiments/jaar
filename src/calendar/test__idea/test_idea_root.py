from src.calendar.idea import IdeaRoot
from pytest import raises as pytest_raises


def test_IdeaRoot_exists():
    # GIVEN / WHEN
    new_obj = IdeaRoot()

    # THEN
    assert new_obj
    flount_text = "flount"
    assert new_obj._desc == flount_text
    assert new_obj._kids is None


def test_IdeaRoot_set_idea_desc_DoesNotRaisesError():
    # GIVEN
    new_obj = IdeaRoot()

    # WHEN
    flount_text = "flount"
    new_obj.set_idea_desc(desc=flount_text)

    # THEN
    assert new_obj._desc == flount_text


def test_IdeaRoot_set_idea_desc_RaisesError():
    # GIVEN
    new_obj = IdeaRoot()

    # WHEN/THEN
    flount_text = "flount"
    with pytest_raises(Exception) as excinfo:
        src_text = "src"
        new_obj.set_idea_desc(desc=src_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{flount_text}'"
    )
