from src.agenda.idea import idea_kid_shop
from src.agenda.road import get_default_economy_root_roadnode as root_label
from pytest import raises as pytest_raises


def test_idea_kid_shop_With_root_ReturnsCorrectObj():
    # GIVEN / WHEN
    x_idearoot = idea_kid_shop(_root=True)

    # THEN
    assert x_idearoot
    assert x_idearoot._root
    assert x_idearoot._label == root_label()
    assert x_idearoot._kids == {}
    assert x_idearoot._root == True


def test_IdeaUnit_set_idea_label_get_default_economy_root_roadnode_DoesNotRaisesError():
    # GIVEN
    x_idearoot = idea_kid_shop(_root=True)

    # WHEN

    x_idearoot.set_idea_label(_label=root_label())

    # THEN
    assert x_idearoot._label == root_label()


def test_IdeaUnit_set_idea_label_CorrectlyDoesNotRaisesError():
    # GIVEN
    el_paso_text = "El Paso"
    x_idearoot = idea_kid_shop(_root=True, _agenda_economy_id=el_paso_text)

    # WHEN
    x_idearoot.set_idea_label(_label=el_paso_text)

    # THEN
    assert x_idearoot._label == el_paso_text


def test_IdeaUnit_set_idea_label_DoesRaisesError():
    # GIVEN
    el_paso_text = "El Paso"
    x_idearoot = idea_kid_shop(_root=True, _agenda_economy_id=el_paso_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        x_idearoot.set_idea_label(_label=casa_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{el_paso_text}'"
    )


def test_IdeaUnit_set_idea_label_RaisesErrorWhen_agenda_economy_id_IsNone():
    # GIVEN
    x_idearoot = idea_kid_shop(_root=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        x_idearoot.set_idea_label(_label=casa_text)
    assert (
        str(excinfo.value)
        == f"Cannot set idearoot to string other than '{root_label()}'"
    )


def test_IdeaUnit_set_idea_label_agenda_economy_id_EqualRootLabelDoesNotRaisesError():
    # GIVEN
    x_idearoot = idea_kid_shop(_root=True, _agenda_economy_id=root_label())

    # WHEN
    x_idearoot.set_idea_label(_label=root_label())

    # THEN
    assert x_idearoot._label == root_label()
