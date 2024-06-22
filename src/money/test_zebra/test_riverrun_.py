from src.money.examples.example_credorledgers import (
    example_yao_bob_zia_credorledgers,
    example_yao_bob_zia_taxledger,
    example_yao_userhub,
)
from src.money.river_cycle import RiverRun, riverrun_shop


def test_RiverRun_Exists():
    # GIVEN / WHEN
    x_riverrun = RiverRun()

    # THEN
    # create RiverRun and
    assert x_riverrun.userhub is None
    assert x_riverrun.number is None
    assert x_riverrun.econ_credorledgers is None
    assert x_riverrun.taxledger is None
    assert x_riverrun.cycle_count is None
    assert x_riverrun.cycle_max is None


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
    # GIVEN / WHEN
    ten_int = 10
    yao_userhub = example_yao_userhub()
    econ_credorledgers = example_yao_bob_zia_credorledgers()
    x_cycle_max = 10
    x_taxledger = example_yao_bob_zia_taxledger()

    x_riverrun = riverrun_shop(
        userhub=yao_userhub,
        number=ten_int,
        econ_credorledgers=econ_credorledgers,
        taxledger=x_taxledger,
        cycle_max=x_cycle_max,
    )

    # THEN
    # create RiverRun and
    assert x_riverrun.userhub == yao_userhub
    assert x_riverrun.number == ten_int
    assert x_riverrun.econ_credorledgers == econ_credorledgers
    assert x_riverrun.taxledger == x_taxledger
    assert x_riverrun.cycle_count == 0
    assert x_riverrun.cycle_max == x_cycle_max


def test_riverrun_shop_ReturnsCorrectObjWithoutArgs():
    # GIVEN / WHEN
    yao_userhub = example_yao_userhub()

    x_riverrun = riverrun_shop(userhub=yao_userhub)

    # THEN
    # create RiverRun and
    assert x_riverrun.userhub == yao_userhub
    assert x_riverrun.number == 0
    assert x_riverrun.econ_credorledgers == {}
    assert x_riverrun.taxledger == {}
    assert x_riverrun.cycle_count == 0
    assert x_riverrun.cycle_max == 10


def test_RiverRun_set_econ_credorledger_CorrectChangesAttr():
    # GIVEN / WHEN
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
