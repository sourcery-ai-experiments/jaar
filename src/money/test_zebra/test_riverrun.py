from src._road.finance import default_penny_if_none, default_money_magnitude
from src.agenda.agenda import agendaunit_shop
from src.listen.userhub import userhub_shop
from src.money.examples.example_credorledgers import (
    example_yao_bob_zia_credorledgers,
    example_yao_bob_zia_due_taxs,
    example_yao_userhub,
)
from src.money.river_cycle import (
    RiverBook,
    riverbook_shop,
    create_riverbook,
    RiverCycle,
    rivercycle_shop,
    create_init_rivercycle,
    RiverRun,
    get_credorledger,
    riverrun_shop,
)


def test_RiverRun_Exists():
    # GIVEN / WHEN
    x_riverrun = RiverRun()

    # THEN
    # create RiverRun and
    assert x_riverrun.userhub is None
    assert x_riverrun.number is None
    assert x_riverrun.econ_credorledgers is None
    assert x_riverrun.due_taxes is None
    assert x_riverrun.cycle_count is None
    assert x_riverrun.cycle_max is None


def test_riverrun_shop_ReturnsCorrectObj():
    # GIVEN / WHEN
    ten_int = 10
    yao_userhub = example_yao_userhub()
    econ_credorledgers = example_yao_bob_zia_credorledgers()
    x_due_taxs = example_yao_bob_zia_due_taxs()
    x_cycle_max = 10

    x_riverrun = riverrun_shop(
        userhub=ten_int,
        number=yao_userhub,
        econ_credorledgers=econ_credorledgers,
        due_taxes=x_due_taxs,
        cycle_max=x_cycle_max,
    )

    # THEN
    # create RiverRun and
    assert x_riverrun.userhub == ten_int
    assert x_riverrun.number == yao_userhub
    assert x_riverrun.econ_credorledgers == econ_credorledgers
    assert x_riverrun.due_taxes == x_due_taxs
    assert x_riverrun.cycle_count == 0
    assert x_riverrun.cycle_max == x_cycle_max
