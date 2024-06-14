from src.agenda.fact import factunit_shop
from src._road.road import get_default_real_id_roadnode as root_label
from pytest import raises as pytest_raises


def test_factunit_shop_With_root_ReturnsCorrectObj():
    # GIVEN / WHEN
    x_factroot = factunit_shop(_root=True)

    # THEN
    assert x_factroot
    assert x_factroot._root
    assert x_factroot._label == root_label()
    assert x_factroot._kids == {}
    assert x_factroot._root == True


def test_FactUnit_set_fact_label_get_default_real_id_roadnode_DoesNotRaisesError():
    # GIVEN
    x_factroot = factunit_shop(_root=True)

    # WHEN

    x_factroot.set_fact_label(_label=root_label())

    # THEN
    assert x_factroot._label == root_label()


def test_FactUnit_set_fact_label_CorrectlyDoesNotRaisesError():
    # GIVEN
    el_paso_text = "El Paso"
    x_factroot = factunit_shop(_root=True, _agenda_real_id=el_paso_text)

    # WHEN
    x_factroot.set_fact_label(_label=el_paso_text)

    # THEN
    assert x_factroot._label == el_paso_text


def test_FactUnit_set_fact_label_DoesRaisesError():
    # GIVEN
    el_paso_text = "El Paso"
    x_factroot = factunit_shop(_root=True, _agenda_real_id=el_paso_text)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        x_factroot.set_fact_label(_label=casa_text)
    assert (
        str(excinfo.value)
        == f"Cannot set factroot to string other than '{el_paso_text}'"
    )


def test_FactUnit_set_fact_label_RaisesErrorWhen_agenda_real_id_IsNone():
    # GIVEN
    x_factroot = factunit_shop(_root=True)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        casa_text = "casa"
        x_factroot.set_fact_label(_label=casa_text)
    assert (
        str(excinfo.value)
        == f"Cannot set factroot to string other than '{root_label()}'"
    )


def test_FactUnit_set_fact_label_agenda_real_id_EqualRootLabelDoesNotRaisesError():
    # GIVEN
    x_factroot = factunit_shop(_root=True, _agenda_real_id=root_label())

    # WHEN
    x_factroot.set_fact_label(_label=root_label())

    # THEN
    assert x_factroot._label == root_label()
