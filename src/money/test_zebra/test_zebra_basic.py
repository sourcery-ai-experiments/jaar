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


def test_RiverBook_Exists():
    # GIVEN / WHEN
    x_riverbook = RiverBook()

    # THEN
    assert x_riverbook.owner_id is None
    assert x_riverbook.userhub is None
    assert x_riverbook.book_money_amount is None


def test_riverbook_shop_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(None, None, yao_text)

    # WHEN
    bob_book_money_amount = 1000
    bob_text = "Bob"
    bob_riverbook = riverbook_shop(yao_userhub, bob_text, bob_book_money_amount)

    # THEN
    assert bob_riverbook.owner_id == bob_text
    assert bob_riverbook.userhub == yao_userhub
    assert bob_riverbook.book_money_amount == bob_book_money_amount
    assert bob_riverbook._rivergrants == {}


def test_create_riverbook_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.add_otherunit(yao_text)
    yao_agenda.add_otherunit(sue_text)
    yao_userhub = userhub_shop(None, None, yao_text)
    yao_book_money_amount = 500

    # WHEN
    yao_credorledger = get_credorledger(yao_agenda)
    yao_riverbook = create_riverbook(
        yao_userhub, yao_text, yao_credorledger, yao_book_money_amount
    )

    # THEN
    assert yao_riverbook.userhub == yao_userhub
    assert yao_riverbook.owner_id == yao_text
    assert yao_riverbook.book_money_amount == yao_book_money_amount
    assert yao_riverbook._rivergrants == {yao_text: 250, sue_text: 250}


def test_RiverCylce_Exists():
    # GIVEN / WHEN
    x_rivercycle = RiverCycle()

    # THEN
    assert x_rivercycle.userhub is None
    assert x_rivercycle.number is None
    assert x_rivercycle.credorledgers is None
    assert x_rivercycle.riverbooks is None
    assert x_rivercycle.cycle_money_amount is None


def test_rivercycle_shop_ReturnsCorrectObj():
    # GIVEN
    one_int = 1
    yao_userhub = userhub_shop(None, None, "Yao")

    # WHEN
    one_rivercycle = rivercycle_shop(yao_userhub, one_int)

    # THEN
    assert one_rivercycle.userhub == yao_userhub
    assert one_rivercycle.number == 1
    assert one_rivercycle.credorledgers == {}
    assert one_rivercycle.riverbooks == {}
    assert one_rivercycle.cycle_money_amount == yao_userhub.econ_money_magnitude


def test_RiverCylce_set_riverbook_CorrectlySetsAttr():
    # GIVEN
    one_int = 1
    yao_userhub = userhub_shop(None, None, "Yao")
    one_rivercycle = rivercycle_shop(yao_userhub, one_int)
    yao_cycle_money_amount = 555
    bob_text = "Bob"
    bob_riverbook = riverbook_shop(yao_userhub, bob_text, yao_cycle_money_amount)
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle.set_riverbook(bob_riverbook)

    # THEN
    assert one_rivercycle.riverbooks == {bob_text: bob_riverbook}


# def test_RiverCylce_create_cylce_ledger_ReturnsCorrectObjOneRiverBook():
#     # GIVEN
#     one_int = 1
#     one_rivercycle = rivercycle_shop(one_int)
#     money_amount = default_money_magnitude()
#     yao_text = "Yao"
#     yao_riverbook = riverbook_shop(yao_text, money_amount, penny=None)
#     one_rivercycle.set_riverbook(yao_riverbook)

#     # WHEN
#     one_cylceledger = one_rivercycle.create_cylceledger()

#     # THEN
#     assert one_cylceledger == {yao_text, money_amount}


# def test_RiverCylce_create_cylce_ledger_ReturnsCorrectObjTwoRiverBooks():
#     # GIVEN
#     one_int = 1
#     one_rivercycle = rivercycle_shop(one_int, money_amount=default_money_magnitude())
#     money_amount = one_rivercycle.money_amount
#     yao_text = "Yao"
#     bob_text = "Yao"
#     yao_money = money_amount / 2
#     bob_money = money_amount / 2
#     yao_riverbook = riverbook_shop(yao_text, yao_money, penny=None)
#     bob_riverbook = riverbook_shop(bob_text, bob_money, penny=None)
#     one_rivercycle.set_riverbook(yao_riverbook)
#     one_rivercycle.set_riverbook(bob_riverbook)

#     # WHEN
#     one_cylceledger = one_rivercycle.create_cylceledger()

#     # THEN
#     assert one_cylceledger == {yao_text: yao_money, bob_text: bob_money}


def test_create_init_rivercycle_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(None, None, yao_text)
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.add_otherunit(yao_text)
    yao_credorledger = get_credorledger(yao_agenda)
    all_credorledgers = {yao_text: yao_credorledger}

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(yao_userhub, all_credorledgers)

    # THEN
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    assert yao_init_rivercycle.riverbooks.get(yao_text) != None


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
