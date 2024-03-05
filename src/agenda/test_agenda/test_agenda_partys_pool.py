from src.agenda.agenda import agendaunit_shop
from pytest import raises as pytest_raises


def test_AgendaUnit_set_party_creditor_pool_CorrectlySetsInt():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_worker_id=zia_text)
    assert zia_agenda._party_creditor_pool is None
    # WHEN
    x_party_creditor_pool = 11
    zia_agenda.set_party_creditor_pool(x_party_creditor_pool)
    # THEN
    assert zia_agenda._party_creditor_pool == x_party_creditor_pool


def test_AgendaUnit_set_party_creditor_pool_CorrectlyChanges_partys_creditor_weight():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_creditor_weight = 73
    wei_creditor_weight = 79
    zia_creditor_weight = 83
    zia_agenda = agendaunit_shop(_worker_id=zia_text)
    zia_agenda.add_partyunit(yao_text, creditor_weight=yao_creditor_weight)
    zia_agenda.add_partyunit(wei_text, creditor_weight=wei_creditor_weight)
    zia_agenda.add_partyunit(zia_text, creditor_weight=zia_creditor_weight)
    x_sum = yao_creditor_weight + wei_creditor_weight + zia_creditor_weight
    zia_agenda.set_party_creditor_pool(x_sum)
    assert zia_agenda._party_creditor_pool == x_sum
    assert zia_agenda.get_party(yao_text).creditor_weight == yao_creditor_weight
    assert zia_agenda.get_party(wei_text).creditor_weight == wei_creditor_weight
    assert zia_agenda.get_party(zia_text).creditor_weight == zia_creditor_weight

    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    zia_agenda.set_party_creditor_pool(new_sum, update_partys_creditor_weight=True)

    # THEN
    assert zia_agenda._party_creditor_pool == new_sum
    new_yao_creditor_weight = yao_creditor_weight * new_ratio
    new_wei_creditor_weight = wei_creditor_weight * new_ratio
    new_zia_creditor_weight = zia_creditor_weight * new_ratio
    assert zia_agenda.get_party(yao_text).creditor_weight == new_yao_creditor_weight
    assert zia_agenda.get_party(wei_text).creditor_weight == new_wei_creditor_weight
    assert zia_agenda.get_party(zia_text).creditor_weight == new_zia_creditor_weight


def test_AgendaUnit_set_party_creditor_pool_CorrectlyChanges_partys_creditor_weightWithEmpty_partys():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_worker_id=zia_text)

    # WHEN
    x_party_creditor_pool = 77
    zia_agenda.set_party_creditor_pool(
        x_party_creditor_pool, update_partys_creditor_weight=True
    )

    # THEN
    assert zia_agenda._party_creditor_pool == x_party_creditor_pool


def test_AgendaUnit_set_party_debtor_pool_CorrectlySetsInt():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_worker_id=zia_text)
    assert zia_agenda._party_debtor_pool is None

    # WHEN
    x_party_debtor_pool = 13
    zia_agenda.set_party_debtor_pool(x_party_debtor_pool)
    # THEN
    assert zia_agenda._party_debtor_pool == x_party_debtor_pool


def test_AgendaUnit_set_party_debtor_pool_CorrectlyChanges_partys_debtor_weight():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_debtor_weight = 73
    wei_debtor_weight = 79
    zia_debtor_weight = 83
    zia_agenda = agendaunit_shop(_worker_id=zia_text)
    zia_agenda.add_partyunit(yao_text, debtor_weight=yao_debtor_weight)
    zia_agenda.add_partyunit(wei_text, debtor_weight=wei_debtor_weight)
    zia_agenda.add_partyunit(zia_text, debtor_weight=zia_debtor_weight)
    x_sum = yao_debtor_weight + wei_debtor_weight + zia_debtor_weight
    zia_agenda.set_party_debtor_pool(x_sum)
    assert zia_agenda._party_debtor_pool == x_sum
    assert zia_agenda.get_party(yao_text).debtor_weight == yao_debtor_weight
    assert zia_agenda.get_party(wei_text).debtor_weight == wei_debtor_weight
    assert zia_agenda.get_party(zia_text).debtor_weight == zia_debtor_weight

    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    zia_agenda.set_party_debtor_pool(new_sum, update_partys_debtor_weight=True)

    # THEN
    assert zia_agenda._party_debtor_pool == new_sum
    new_yao_debtor_weight = yao_debtor_weight * new_ratio
    new_wei_debtor_weight = wei_debtor_weight * new_ratio
    new_zia_debtor_weight = zia_debtor_weight * new_ratio
    assert zia_agenda.get_party(yao_text).debtor_weight == new_yao_debtor_weight
    assert zia_agenda.get_party(wei_text).debtor_weight == new_wei_debtor_weight
    assert zia_agenda.get_party(zia_text).debtor_weight == new_zia_debtor_weight


def test_AgendaUnit_set_party_debtor_pool_CorrectlyChanges_partys_debtor_weightWithEmpty_partys():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_worker_id=zia_text)

    # WHEN
    x_party_debtor_pool = 77
    zia_agenda.set_party_debtor_pool(
        x_party_debtor_pool, update_partys_debtor_weight=True
    )

    # THEN
    assert zia_agenda._party_debtor_pool == x_party_debtor_pool
