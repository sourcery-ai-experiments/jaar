from src.agenda.oath import oathunit_shop
from src._road.road import get_default_real_id_roadnode as root_label
from pytest import raises as pytest_raises


def test_oathunit_shop_With_root_ReturnsCorrectObj():
    # GIVEN / WHEN
    x_oathroot = oathunit_shop(_root=True)

    # THEN
    assert x_oathroot
    assert x_oathroot._root
    assert x_oathroot._label == root_label()
    assert x_oathroot._kids == {}
    assert x_oathroot._root == True


def test_OathUnit_set_oath_label_get_default_real_id_roadnode_DoesNotRaisesError():
    # GIVEN
    x_oathroot = oathunit_shop(_root=True)

    # WHEN

    x_oathroot.set_oath_label(_label=root_label())

    # THEN
    assert x_oathroot._label == root_label()


def test_OathUnit_set_oath_label_CorrectlyDoesNotRaisesError():
    # GIVEN
    el_paso_text = "El Paso"
    x_oathroot = oathunit_shop(_root=True, _agenda_real_id=el_paso_text)

    # WHEN
    x_oathroot.set_oath_label(_label=el_paso_text)

    # THEN
    assert x_oathroot._label == el_paso_text


def test_OathUnit_set_oath_label_DoesRaisesError():
    # GIVEN
    el_paso_text = "El Paso"
    x_oathroot = oathunit_shop(_root=True, _agenda_real_id=el_paso_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        x_oathroot.set_oath_label(_label=casa_text)
    assert (
        str(excinfo.value)
        == f"Cannot set oathroot to string other than '{el_paso_text}'"
    )


def test_OathUnit_set_oath_label_RaisesErrorWhen_agenda_real_id_IsNone():
    # GIVEN
    x_oathroot = oathunit_shop(_root=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        x_oathroot.set_oath_label(_label=casa_text)
    assert (
        str(excinfo.value)
        == f"Cannot set oathroot to string other than '{root_label()}'"
    )


def test_OathUnit_set_oath_label_agenda_real_id_EqualRootLabelDoesNotRaisesError():
    # GIVEN
    x_oathroot = oathunit_shop(_root=True, _agenda_real_id=root_label())

    # WHEN
    x_oathroot.set_oath_label(_label=root_label())

    # THEN
    assert x_oathroot._label == root_label()
