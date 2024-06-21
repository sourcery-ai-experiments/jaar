from src._road.finance import default_penny_if_none, default_money_magnitude
from src.agenda.agenda import agendaunit_shop
from src.listen.userhub import userhub_shop
from src.money.river_cycle import (
    RiverBook,
    riverbook_shop,
    create_riverbook,
    RiverCycle,
    rivercycle_shop,
    create_init_rivercycle,
    RiverRun,
    get_credorledger,
)


# def test_RiverRun_Exists():
#     # GIVEN / WHEN
#     x_riverrun = RiverRun()

#     # THEN
#     # create RiverRun and
#     assert x_riverrun.healer_id is None
#     assert x_riverrun.number is None
#     assert x_riverrun.cycle_curr is None
#     assert x_riverrun.cyclc_next is None
#     assert x_riverrun.cycle_count is None
#     assert x_riverrun.cycle_max is None
#     assert x_riverrun.debtledger is None
#     assert x_riverrun.tax_due_ledger is None
#     assert x_riverrun.money_amount is None
#     assert x_riverrun.penny is None
