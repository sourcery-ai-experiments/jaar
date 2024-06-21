from src.agenda.agenda import agendaunit_shop
from src.listen.userhub import userhub_shop
from src.money.river_cycle import (
    create_riverbook,
    RiverCycle,
    rivercycle_shop,
    create_init_rivercycle,
    get_init_rivercycle_cycleledger,
    get_credorledger,
)


def test_RiverCylce_Exists():
    # GIVEN / WHEN
    x_rivercycle = RiverCycle()

    # THEN
    assert x_rivercycle.userhub is None
    assert x_rivercycle.number is None
    assert x_rivercycle.econ_credorledgers is None
    assert x_rivercycle.riverbooks is None


def test_rivercycle_shop_ReturnsCorrectObj():
    # GIVEN
    one_int = 1
    yao_userhub = userhub_shop(None, None, "Yao")

    # WHEN
    one_rivercycle = rivercycle_shop(yao_userhub, one_int)

    # THEN
    assert one_rivercycle.userhub == yao_userhub
    assert one_rivercycle.number == 1
    assert one_rivercycle.econ_credorledgers == {}
    assert one_rivercycle.riverbooks == {}


def test_RiverCylce_set_complete_riverbook_CorrectlySetsAttr():
    # GIVEN
    one_int = 1
    yao_userhub = userhub_shop(None, None, "Yao")
    one_rivercycle = rivercycle_shop(yao_userhub, one_int)
    bob_book_money_amount = 555
    bob_text = "Bob"
    bob_riverbook = create_riverbook(yao_userhub, bob_text, {}, bob_book_money_amount)
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle._set_complete_riverbook(bob_riverbook)

    # THEN
    assert one_rivercycle.riverbooks == {bob_text: bob_riverbook}


def test_RiverCylce_add_riverbook_CorrectlySetsAttr():
    # GIVEN
    one_int = 1
    yao_text = "Yao"
    yao_userhub = userhub_shop(None, None, yao_text)
    bob_text = "Bob"
    econ_credorledger = {bob_text: {yao_text: 75, bob_text: 25}}
    one_rivercycle = rivercycle_shop(yao_userhub, one_int, econ_credorledger)
    bob_book_money_amount = 500
    assert one_rivercycle.riverbooks == {}

    # WHEN
    one_rivercycle.add_riverbook(bob_text, bob_book_money_amount)

    # THEN
    bob_credorledger = econ_credorledger.get(bob_text)
    bob_riverbook = create_riverbook(
        yao_userhub, bob_text, bob_credorledger, bob_book_money_amount
    )
    assert one_rivercycle.riverbooks == {bob_text: bob_riverbook}


def test_RiverCylce_create_cylce_ledger_ReturnsCorrectObjOneRiverBook():
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(None, None, yao_text)
    one_int = 1
    yao_credorledger = {yao_text: {yao_text: 334.0}}
    one_rivercycle = rivercycle_shop(yao_userhub, one_int, yao_credorledger)
    book_money_amount = 450
    one_rivercycle.add_riverbook(yao_text, book_money_amount)

    # WHEN
    one_cylceledger = one_rivercycle.create_cylceledger()

    # THEN
    assert one_cylceledger == {yao_text: book_money_amount}


def test_RiverCylce_create_cylce_ledger_ReturnsCorrectObjTwoRiverBooks():
    # GIVEN
    yao_text = "Yao"
    bob_text = "Bob"
    yao_userhub = userhub_shop(None, None, yao_text)
    one_int = 1
    econ_credorledgers = {yao_text: {yao_text: 75, bob_text: 25}}
    one_rivercycle = rivercycle_shop(yao_userhub, one_int, econ_credorledgers)
    book_money_amount = 500
    one_rivercycle.add_riverbook(yao_text, book_money_amount)

    # WHEN
    one_cylceledger = one_rivercycle.create_cylceledger()

    # THEN
    yao_money = book_money_amount * 0.75
    bob_money = book_money_amount * 0.25
    assert one_cylceledger == {yao_text: yao_money, bob_text: bob_money}


def test_create_init_rivercycle_ReturnsObjScenarioOne_otherunit():
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(None, None, yao_text)
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.add_otherunit(yao_text)
    yao_credorledger = get_credorledger(yao_agenda)
    econ_credorledgers = {yao_text: yao_credorledger}

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(yao_userhub, econ_credorledgers)

    # THEN
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    assert yao_init_rivercycle.riverbooks.get(yao_text) != None


def test_create_init_rivercycle_ReturnsObjScenarioThree_otherunit():
    # GIVEN
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_credor_weight = 7
    bob_credor_weight = 3
    zia_credor_weight = 10
    yao_userhub = userhub_shop(None, None, yao_text)
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.add_otherunit(yao_text, yao_credor_weight)
    yao_agenda.add_otherunit(bob_text, bob_credor_weight)
    yao_agenda.add_otherunit(zia_text, zia_credor_weight)
    yao_credorledger = get_credorledger(yao_agenda)
    econ_credorledgers = {yao_text: yao_credorledger}
    print(f"{econ_credorledgers=}")

    # WHEN
    yao_init_rivercycle = create_init_rivercycle(yao_userhub, econ_credorledgers)

    # THEN
    assert yao_init_rivercycle.number == 0
    assert len(yao_init_rivercycle.riverbooks) == 1
    yao_riverbook = yao_init_rivercycle.riverbooks.get(yao_text)
    assert yao_riverbook != None
    assert len(yao_riverbook._rivergrants) == 3
    assert yao_riverbook._rivergrants.get(yao_text) == 350000000
    assert yao_riverbook._rivergrants.get(bob_text) == 150000000
    assert yao_riverbook._rivergrants.get(zia_text) == 500000000


def test_get_init_rivercycle_cycleledger_ReturnsObj():
    # GIVEN
    yao_text = "Yao"
    bob_text = "Bob"
    zia_text = "Zia"
    yao_credor_weight = 7
    bob_credor_weight = 3
    zia_credor_weight = 10
    yao_userhub = userhub_shop(None, None, yao_text)
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.add_otherunit(yao_text, yao_credor_weight)
    yao_agenda.add_otherunit(bob_text, bob_credor_weight)
    yao_agenda.add_otherunit(zia_text, zia_credor_weight)
    yao_credorledger = get_credorledger(yao_agenda)
    econ_credorledgers = {yao_text: yao_credorledger}

    # WHEN
    yao_init_rivercycle_cycleledger = get_init_rivercycle_cycleledger(
        yao_userhub, econ_credorledgers
    )

    # THEN
    assert len(yao_init_rivercycle_cycleledger) == 3
    assert yao_init_rivercycle_cycleledger.get(yao_text) == 350000000
    assert yao_init_rivercycle_cycleledger.get(bob_text) == 150000000
    assert yao_init_rivercycle_cycleledger.get(zia_text) == 500000000
