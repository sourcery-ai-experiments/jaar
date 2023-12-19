from src.agenda.idea import IdeaRoot, idearoot_shop
from src.agenda.road import get_default_economy_root_label as root_label
from pytest import raises as pytest_raises


def test_IdeaRoot_exists():
    # GIVEN / WHEN
    new_obj = IdeaRoot()

    # THEN
    assert new_obj
    assert new_obj._label is None
    assert new_obj._kids is None


def test_idearoot_shop_ReturnsCorrectObj():
    # GIVEN / WHEN
    new_obj = idearoot_shop()

    # THEN
    assert new_obj
    assert new_obj._label == root_label()
    assert new_obj._kids is None


def test_IdeaRoot_set_idea_label_get_default_economy_root_label_DoesNotRaisesError():
    # GIVEN
    new_obj = idearoot_shop()

    # WHEN

    new_obj.set_idea_label(_label=root_label())

    # THEN
    assert new_obj._label == root_label()


def test_IdeaRoot_set_idea_label_CorrectlyDoesNotRaisesError():
    # GIVEN
    new_obj = idearoot_shop()
    economy_id = "El Paso"

    # WHEN
    new_obj.set_idea_label(_label=economy_id, agenda_economy_id=economy_id)

    # THEN
    assert new_obj._label == economy_id


def test_IdeaRoot_set_idea_label_InCorrectlyDoesRaisesError():
    # GIVEN
    new_obj = idearoot_shop()
    economy_id = "El Paso"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        new_obj.set_idea_label(_label=casa_text, agenda_economy_id=economy_id)
    assert (
        str(excinfo.value) == f"Cannot set idearoot to string other than '{economy_id}'"
    )


def test_IdeaRoot_set_idea_label_RaisesErrorWhen_agenda_economy_id_IsNone():
    # GIVEN
    new_obj = idearoot_shop()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        new_obj.set_idea_label(_label=casa_text, agenda_economy_id=None)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{root_label()}'"
    )


def test_IdeaRoot_set_idea_label_agenda_economy_id_EqualRootLabelDoesNotRaisesError():
    # GIVEN
    new_obj = idearoot_shop()

    # WHEN
    new_obj.set_idea_label(_label=root_label(), agenda_economy_id=root_label())

    # THEN
    assert new_obj._label == root_label()
