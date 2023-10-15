from src.contract.idea import IdeaRoot
from src.contract.road import get_default_cure_root_label as root_label
from pytest import raises as pytest_raises


def test_IdeaRoot_exists():
    # GIVEN / WHEN
    new_obj = IdeaRoot()

    # THEN
    assert new_obj

    assert new_obj._label == root_label()
    assert new_obj._kids is None


def test_IdeaRoot_set_idea_label_get_default_cure_root_label_DoesNotRaisesError():
    # GIVEN
    new_obj = IdeaRoot()

    # WHEN

    new_obj.set_idea_label(_label=root_label())

    # THEN
    assert new_obj._label == root_label()


def test_IdeaRoot_set_idea_label_CorrectlyDoesNotRaisesError():
    # GIVEN
    new_obj = IdeaRoot()
    cure_handle = "El Paso"

    # WHEN

    new_obj.set_idea_label(_label=cure_handle, contract_cure_handle=cure_handle)

    # THEN
    assert new_obj._label == cure_handle


def test_IdeaRoot_set_idea_label_InCorrectlyDoesRaisesError():
    # GIVEN
    new_obj = IdeaRoot()
    cure_handle = "El Paso"

    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        new_obj.set_idea_label(_label=casa_text, contract_cure_handle=cure_handle)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{cure_handle}'"
    )


def test_IdeaRoot_set_idea_label_RaisesErrorWhen_contract_cure_handle_IsNone():
    # GIVEN
    new_obj = IdeaRoot()

    # WHEN/THEN

    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        new_obj.set_idea_label(_label=casa_text, contract_cure_handle=None)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{root_label()}'"
    )


def test_IdeaRoot_set_idea_label_contract_cure_handle_EqualRootLabelDoesNotRaisesError():
    # GIVEN
    new_obj = IdeaRoot()

    # WHEN

    new_obj.set_idea_label(_label=root_label(), contract_cure_handle=root_label())

    # THEN
    assert new_obj._label == root_label()
