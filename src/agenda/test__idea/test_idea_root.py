from src.agenda.idea import IdeaRoot
from src.agenda.road import get_default_culture_root_label as root_label
from pytest import raises as pytest_raises


def test_IdeaRoot_exists():
    # GIVEN / WHEN
    new_obj = IdeaRoot()

    # THEN
    assert new_obj

    assert new_obj._label == root_label()
    assert new_obj._kids is None


def test_IdeaRoot_set_idea_label_get_default_culture_root_label_DoesNotRaisesError():
    # GIVEN
    new_obj = IdeaRoot()

    # WHEN

    new_obj.set_idea_label(_label=root_label())

    # THEN
    assert new_obj._label == root_label()


def test_IdeaRoot_set_idea_label_CorrectlyDoesNotRaisesError():
    # GIVEN
    new_obj = IdeaRoot()
    culture_handle = "El Paso"

    # WHEN

    new_obj.set_idea_label(_label=culture_handle, agenda_culture_handle=culture_handle)

    # THEN
    assert new_obj._label == culture_handle


def test_IdeaRoot_set_idea_label_InCorrectlyDoesRaisesError():
    # GIVEN
    new_obj = IdeaRoot()
    culture_handle = "El Paso"

    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        new_obj.set_idea_label(_label=casa_text, agenda_culture_handle=culture_handle)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{culture_handle}'"
    )


def test_IdeaRoot_set_idea_label_RaisesErrorWhen_agenda_culture_handle_IsNone():
    # GIVEN
    new_obj = IdeaRoot()

    # WHEN/THEN

    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        new_obj.set_idea_label(_label=casa_text, agenda_culture_handle=None)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{root_label()}'"
    )


def test_IdeaRoot_set_idea_label_agenda_culture_handle_EqualRootLabelDoesNotRaisesError():
    # GIVEN
    new_obj = IdeaRoot()

    # WHEN

    new_obj.set_idea_label(_label=root_label(), agenda_culture_handle=root_label())

    # THEN
    assert new_obj._label == root_label()
