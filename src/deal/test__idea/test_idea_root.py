from src.deal.idea import IdeaRoot
from src.deal.road import get_default_fix_root_label as root_label
from pytest import raises as pytest_raises


def test_IdeaRoot_exists():
    # GIVEN / WHEN
    new_obj = IdeaRoot()

    # THEN
    assert new_obj

    assert new_obj._label == root_label()
    assert new_obj._kids is None


def test_IdeaRoot_set_idea_label_get_default_fix_root_label_DoesNotRaisesError():
    # GIVEN
    new_obj = IdeaRoot()

    # WHEN

    new_obj.set_idea_label(_label=root_label())

    # THEN
    assert new_obj._label == root_label()


def test_IdeaRoot_set_idea_label_CorrectlyDoesNotRaisesError():
    # GIVEN
    new_obj = IdeaRoot()
    fix_handle = "El Paso"

    # WHEN

    new_obj.set_idea_label(_label=fix_handle, deal_fix_handle=fix_handle)

    # THEN
    assert new_obj._label == fix_handle


def test_IdeaRoot_set_idea_label_InCorrectlyDoesRaisesError():
    # GIVEN
    new_obj = IdeaRoot()
    fix_handle = "El Paso"

    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        new_obj.set_idea_label(_label=casa_text, deal_fix_handle=fix_handle)
    assert (
        str(excinfo.value) == f"Cannot set idearoot to string other than '{fix_handle}'"
    )


def test_IdeaRoot_set_idea_label_RaisesErrorWhen_deal_fix_handle_IsNone():
    # GIVEN
    new_obj = IdeaRoot()

    # WHEN/THEN

    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        new_obj.set_idea_label(_label=casa_text, deal_fix_handle=None)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{root_label()}'"
    )


def test_IdeaRoot_set_idea_label_deal_fix_handle_EqualRootLabelDoesNotRaisesError():
    # GIVEN
    new_obj = IdeaRoot()

    # WHEN

    new_obj.set_idea_label(_label=root_label(), deal_fix_handle=root_label())

    # THEN
    assert new_obj._label == root_label()
