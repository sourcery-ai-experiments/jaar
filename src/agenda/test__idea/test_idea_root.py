from src.agenda.idea import IdeaRoot, idearoot_shop
from src.agenda.road import get_default_economy_root_label as root_label
from pytest import raises as pytest_raises


def test_IdeaRoot_exists():
    # GIVEN / WHEN
    x_idearoot = IdeaRoot()

    # THEN
    assert x_idearoot
    assert x_idearoot._label is None
    assert x_idearoot._kids is None


def test_idearoot_shop_ReturnsCorrectObj():
    # GIVEN / WHEN
    x_idearoot = idearoot_shop()

    # THEN
    assert x_idearoot
    assert x_idearoot._label == root_label()
    assert x_idearoot._kids == {}


def test_IdeaRoot_set_idea_label_get_default_economy_root_label_DoesNotRaisesError():
    # GIVEN
    x_idearoot = idearoot_shop()

    # WHEN

    x_idearoot.set_idea_label(_label=root_label())

    # THEN
    assert x_idearoot._label == root_label()


def test_IdeaRoot_set_idea_label_CorrectlyDoesNotRaisesError():
    # GIVEN
    x_idearoot = idearoot_shop()
    el_paso_text = "El Paso"

    # WHEN
    x_idearoot.set_idea_label(_label=el_paso_text, agenda_economy_id=el_paso_text)

    # THEN
    assert x_idearoot._label == el_paso_text


def test_IdeaRoot_set_idea_label_InCorrectlyDoesRaisesError():
    # GIVEN
    x_idearoot = idearoot_shop()
    el_paso_text = "El Paso"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        x_idearoot.set_idea_label(_label=casa_text, agenda_economy_id=el_paso_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{el_paso_text}'"
    )


def test_IdeaRoot_set_idea_label_RaisesErrorWhen_agenda_economy_id_IsNone():
    # GIVEN
    x_idearoot = idearoot_shop()

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        x_idearoot.set_idea_label(_label=casa_text, agenda_economy_id=None)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{root_label()}'"
    )


def test_IdeaRoot_set_idea_label_agenda_economy_id_EqualRootLabelDoesNotRaisesError():
    # GIVEN
    x_idearoot = idearoot_shop()

    # WHEN
    x_idearoot.set_idea_label(_label=root_label(), agenda_economy_id=root_label())

    # THEN
    assert x_idearoot._label == root_label()
