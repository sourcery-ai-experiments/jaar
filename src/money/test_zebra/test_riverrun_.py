from src.money.examples.example_credorledgers import (
    example_yao_bob_zia_credorledgers,
    example_yao_bob_zia_tax_dues,
    example_yao_userhub,
)
from src.money.riverrun import RiverRun, riverrun_shop


def test_RiverRun_Exists():
    # GIVEN / WHEN
    x_riverrun = RiverRun()

    # THEN
    assert x_riverrun.userhub is None
    assert x_riverrun.number is None
    assert x_riverrun.econ_credorledgers is None
    assert x_riverrun.tax_dues is None
    assert x_riverrun.cycle_max is None
    # calculated fields
    assert x_riverrun._rivergrades is None
    assert x_riverrun._grants is None
    assert x_riverrun._tax_yields is None
    assert x_riverrun._cycle_count is None
    assert x_riverrun._debtor_count is None
    assert x_riverrun._credor_count is None


def test_RiverRun_set_cycle_max_CorrectlySetsAttr():
    # GIVEN
    x_riverrun = RiverRun()
    assert x_riverrun.cycle_max is None

    # WHEN / THEN
    x_riverrun.set_cycle_max(10)
    assert x_riverrun.cycle_max == 10

    # WHEN / THEN
    x_riverrun.set_cycle_max(10.0)
    assert x_riverrun.cycle_max == 10

    # WHEN / THEN
    x_riverrun.set_cycle_max(-10.0)
    assert x_riverrun.cycle_max == 0

    # WHEN / THEN
    x_riverrun.set_cycle_max(10.8)
    assert x_riverrun.cycle_max == 10


def test_riverrun_shop_ReturnsCorrectObjWithArg():
    # GIVEN
    ten_int = 10
    yao_userhub = example_yao_userhub()
    econ_credorledgers = example_yao_bob_zia_credorledgers()
    x_cycle_max = 10
    x_tax_dues = example_yao_bob_zia_tax_dues()

    # WHEN
    x_riverrun = riverrun_shop(
        userhub=yao_userhub,
        number=ten_int,
        econ_credorledgers=econ_credorledgers,
        tax_dues=x_tax_dues,
        cycle_max=x_cycle_max,
    )

    # THEN
    assert x_riverrun.userhub == yao_userhub
    assert x_riverrun.number == ten_int
    assert x_riverrun.econ_credorledgers == econ_credorledgers
    assert x_riverrun.tax_dues == x_tax_dues
    assert x_riverrun._rivergrades == {}
    assert x_riverrun._grants == {}
    assert x_riverrun._tax_yields == {}
    assert x_riverrun._cycle_count == 0
    assert x_riverrun.cycle_max == x_cycle_max


def test_riverrun_shop_ReturnsCorrectObjWithoutArgs():
    # GIVEN
    yao_userhub = example_yao_userhub()

    # WHEN
    x_riverrun = riverrun_shop(userhub=yao_userhub)

    # THEN
    assert x_riverrun.userhub == yao_userhub
    assert x_riverrun.number == 0
    assert x_riverrun.econ_credorledgers == {}
    assert x_riverrun.tax_dues == {}
    assert x_riverrun._rivergrades == {}
    assert x_riverrun._grants == {}
    assert x_riverrun._tax_yields == {}
    assert x_riverrun._cycle_count == 0
    assert x_riverrun.cycle_max == 10


def test_RiverRun_set_econ_credorledger_CorrectChangesAttr():
    # GIVEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    yao_credor_weight = 500
    x_riverrun = riverrun_shop(yao_userhub)
    assert x_riverrun.econ_credorledgers == {}

    # WHEN
    x_riverrun.set_econ_credorledger(
        owner_id=yao_text, other_id=yao_text, other_credor_weight=yao_credor_weight
    )

    # THEN
    assert x_riverrun.econ_credorledgers == {yao_text: {yao_text: yao_credor_weight}}


def test_RiverRun_delete_econ_credorledgers_owner_CorrectChangesAttr():
    # GIVEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    bob_text = "Bob"
    sue_text = "Sue"
    x_riverrun = riverrun_shop(yao_userhub)
    x_riverrun.set_econ_credorledger(yao_text, yao_text, 1)
    x_riverrun.set_econ_credorledger(bob_text, bob_text, 1)
    x_riverrun.set_econ_credorledger(bob_text, sue_text, 1)
    assert x_riverrun.econ_credorledgers == {
        yao_text: {yao_text: 1},
        bob_text: {bob_text: 1, sue_text: 1},
    }

    # WHEN
    x_riverrun.delete_econ_credorledgers_owner(bob_text)

    # THEN
    assert x_riverrun.econ_credorledgers == {yao_text: {yao_text: 1}}


def test_RiverRun_get_all_econ_credorledger_other_ids_ReturnsCorrectObj():
    # GIVEN
    yao_userhub = example_yao_userhub()
    yao_text = "Yao"
    bob_text = "Bob"
    sue_text = "Sue"
    zia_text = "Zia"
    xio_text = "Xio"
    x_riverrun = riverrun_shop(yao_userhub)

    # WHEN
    all_others_ids = x_riverrun.get_all_econ_credorledger_other_ids()
    # THEN
    assert all_others_ids == set()

    # WHEN
    x_riverrun.set_econ_credorledger(yao_text, yao_text, 1)
    x_riverrun.set_econ_credorledger(yao_text, bob_text, 1)
    all_others_ids = x_riverrun.get_all_econ_credorledger_other_ids()
    # THEN
    assert all_others_ids == {yao_text, bob_text}

    # WHEN
    x_riverrun.set_econ_credorledger(zia_text, bob_text, 1)
    all_others_ids = x_riverrun.get_all_econ_credorledger_other_ids()
    # THEN
    assert all_others_ids == {yao_text, bob_text, zia_text}

    # WHEN
    x_riverrun.set_econ_credorledger(xio_text, sue_text, 1)
    all_others_ids = x_riverrun.get_all_econ_credorledger_other_ids()
    # THEN
    assert all_others_ids == {yao_text, bob_text, zia_text, xio_text, sue_text}
