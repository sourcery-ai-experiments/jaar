from src.agenda.agenda import agendaunit_shop
from pytest import raises as pytest_raises


def test_AgendaUnit_set_party_creditor_pool_CorrectlySetsInt():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")
    assert zia_agenda._party_creditor_pool is None
    # WHEN
    x_party_creditor_pool = 11
    zia_agenda.set_party_creditor_pool(x_party_creditor_pool)
    # THEN
    assert zia_agenda._party_creditor_pool == x_party_creditor_pool


def test_AgendaUnit_set_party_creditor_pool_CorrectlySets_partys_creditor_weightWithEmpty_partys():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")

    # WHEN
    x_party_creditor_pool = 77
    zia_agenda.set_party_creditor_pool(
        x_party_creditor_pool, update_partys_creditor_weight=True
    )

    # THEN
    assert zia_agenda._party_creditor_pool == x_party_creditor_pool


def test_AgendaUnit_set_party_creditor_pool_RaisesErrorWhenArgIsNotMultiple():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(zia_text)
    x_party_creditor_pool = 23
    zia_agenda.set_party_creditor_pool(x_party_creditor_pool)
    assert zia_agenda._planck == 1
    assert zia_agenda._party_creditor_pool == x_party_creditor_pool

    # WHEN
    new_party_creditor_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_agenda.set_party_creditor_pool(new_party_creditor_pool)
    assert (
        str(excinfo.value)
        == f"Agenda '{zia_text}' cannot set _party_creditor_pool='{new_party_creditor_pool}'. It is not divisible by planck '{zia_agenda._planck}'"
    )


def test_AgendaUnit_set_party_creditor_pool_CorrectlyModifies_partys_creditor_weight():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_creditor_weight = 73
    wei_creditor_weight = 79
    zia_creditor_weight = 83
    zia_agenda = agendaunit_shop(_owner_id=zia_text)
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
    new_ratio = 2
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


def test_AgendaUnit_set_party_creditor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_planckAND_correct_planck_issuesIsFalse():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_creditor_weight = 73
    wei_creditor_weight = 79
    zia_creditor_weight = 83
    zia_agenda = agendaunit_shop(zia_text)
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
    print(f"{new_sum=}")
    new_sum = int(new_sum)
    print(f"{new_sum=}")
    zia_agenda.set_party_creditor_pool(
        new_party_creditor_pool=new_sum,
        update_partys_creditor_weight=True,
        correct_planck_issues=False,
    )

    # THEN
    assert zia_agenda._party_creditor_pool == new_sum
    party_yao_creditor_weight = zia_agenda.get_party(yao_text).creditor_weight
    party_wei_creditor_weight = zia_agenda.get_party(wei_text).creditor_weight
    party_zia_creditor_weight = zia_agenda.get_party(zia_text).creditor_weight
    assert party_yao_creditor_weight == (yao_creditor_weight * new_ratio) - 0.5
    assert party_wei_creditor_weight == (wei_creditor_weight * new_ratio) - 0.5
    assert party_zia_creditor_weight == (zia_creditor_weight * new_ratio) - 0.5
    assert zia_agenda.get_partyunits_creditor_weight_sum() == 116
    assert (
        zia_agenda.get_partyunits_creditor_weight_sum()
        != zia_agenda._party_creditor_pool
    )


def test_AgendaUnit_set_party_creditor_pool_SetAttrWhenEmpty_correct_planck_issues_IsTrue():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")

    # WHEN
    new_sum = 5000
    zia_agenda.set_party_creditor_pool(
        new_party_creditor_pool=new_sum,
        update_partys_creditor_weight=True,
        correct_planck_issues=True,
    )

    # THEN
    assert zia_agenda._party_creditor_pool == new_sum
    assert zia_agenda.get_partyunits_creditor_weight_sum() == 0


def test_AgendaUnit_set_party_creditor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_planckAND_correct_planck_issuesIsTrue():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_creditor_weight = 73
    wei_creditor_weight = 79
    zia_creditor_weight = 83
    zia_agenda = agendaunit_shop(zia_text)
    zia_agenda.add_partyunit(yao_text, creditor_weight=yao_creditor_weight)
    zia_agenda.add_partyunit(wei_text, creditor_weight=wei_creditor_weight)
    zia_agenda.add_partyunit(zia_text, creditor_weight=zia_creditor_weight)
    x_sum = yao_creditor_weight + wei_creditor_weight + zia_creditor_weight
    zia_agenda.set_party_creditor_pool(x_sum)
    1
    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    new_sum = int(new_sum)
    zia_agenda.set_party_creditor_pool(
        new_party_creditor_pool=new_sum,
        update_partys_creditor_weight=True,
        correct_planck_issues=True,
    )

    # THEN
    assert zia_agenda._party_creditor_pool == new_sum
    assert zia_agenda.get_partyunits_creditor_weight_sum() == 117
    planck_valid_yao_creditor_weight = (yao_creditor_weight * new_ratio) - 0.5
    planck_valid_wei_creditor_weight = (wei_creditor_weight * new_ratio) - 0.5
    planck_valid_zia_creditor_weight = (zia_creditor_weight * new_ratio) - 0.5
    party_yao_creditor_weight = zia_agenda.get_party(yao_text).creditor_weight
    party_wei_creditor_weight = zia_agenda.get_party(wei_text).creditor_weight
    party_zia_creditor_weight = zia_agenda.get_party(zia_text).creditor_weight
    assert party_yao_creditor_weight == planck_valid_yao_creditor_weight
    assert party_wei_creditor_weight == planck_valid_wei_creditor_weight
    assert party_zia_creditor_weight == planck_valid_zia_creditor_weight + 1
    assert (
        zia_agenda.get_partyunits_creditor_weight_sum()
        == zia_agenda._party_creditor_pool
    )


def test_AgendaUnit_set_party_debtor_pool_CorrectlySetsInt():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_owner_id=zia_text)
    assert zia_agenda._party_debtor_pool is None

    # WHEN
    x_party_debtor_pool = 13
    zia_agenda.set_party_debtor_pool(x_party_debtor_pool)
    # THEN
    assert zia_agenda._party_debtor_pool == x_party_debtor_pool


def test_AgendaUnit_set_party_debtor_pool_CorrectlySets_partys_debtor_weightWithEmpty_partys():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_owner_id=zia_text)

    # WHEN
    x_party_debtor_pool = 77
    zia_agenda.set_party_debtor_pool(
        x_party_debtor_pool, update_partys_debtor_weight=True
    )

    # THEN
    assert zia_agenda._party_debtor_pool == x_party_debtor_pool


def test_AgendaUnit_set_party_debtor_pool_RaisesErrorWhenArgIsNotMultiple():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(zia_text)
    x_party_debtor_pool = 23
    zia_agenda.set_party_debtor_pool(
        x_party_debtor_pool, update_partys_debtor_weight=True
    )
    assert zia_agenda._planck == 1
    assert zia_agenda._party_debtor_pool == x_party_debtor_pool

    # WHEN
    new_party_debtor_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_agenda.set_party_debtor_pool(
            new_party_debtor_pool, update_partys_debtor_weight=True
        )
    assert (
        str(excinfo.value)
        == f"Agenda '{zia_text}' cannot set _party_debtor_pool='{new_party_debtor_pool}'. It is not divisible by planck '{zia_agenda._planck}'"
    )


def test_AgendaUnit_set_party_debtor_pool_CorrectlyModifies_partys_debtor_weight():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_debtor_weight = 73
    wei_debtor_weight = 79
    zia_debtor_weight = 83
    zia_agenda = agendaunit_shop(_owner_id=zia_text)
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
    new_ratio = 2
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


def test_AgendaUnit_set_party_debtor_pool_SetAttrWhenEmpty_correct_planck_issues_IsTrue():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")

    # WHEN
    new_sum = 5000
    zia_agenda.set_party_debtor_pool(
        new_party_debtor_pool=new_sum,
        update_partys_debtor_weight=True,
        correct_planck_issues=True,
    )

    # THEN
    assert zia_agenda._party_debtor_pool == new_sum
    assert zia_agenda.get_partyunits_debtor_weight_sum() == 0


def test_AgendaUnit_set_party_debtor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_planckAND_correct_planck_issuesIsFalse():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_debtor_weight = 73
    wei_debtor_weight = 79
    zia_debtor_weight = 83
    zia_agenda = agendaunit_shop(zia_text)
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
    print(f"{new_sum=}")
    new_sum = int(new_sum)
    print(f"{new_sum=}")
    zia_agenda.set_party_debtor_pool(
        new_party_debtor_pool=new_sum,
        update_partys_debtor_weight=True,
        correct_planck_issues=False,
    )

    # THEN
    assert zia_agenda._party_debtor_pool == new_sum
    party_yao_debtor_weight = zia_agenda.get_party(yao_text).debtor_weight
    party_wei_debtor_weight = zia_agenda.get_party(wei_text).debtor_weight
    party_zia_debtor_weight = zia_agenda.get_party(zia_text).debtor_weight
    assert party_yao_debtor_weight == (yao_debtor_weight * new_ratio) - 0.5
    assert party_wei_debtor_weight == (wei_debtor_weight * new_ratio) - 0.5
    assert party_zia_debtor_weight == (zia_debtor_weight * new_ratio) - 0.5
    assert zia_agenda.get_partyunits_debtor_weight_sum() == 116
    assert (
        zia_agenda.get_partyunits_debtor_weight_sum() != zia_agenda._party_debtor_pool
    )


def test_AgendaUnit_set_party_debtor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_planckAND_correct_planck_issuesIsTrue():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_debtor_weight = 73
    wei_debtor_weight = 79
    zia_debtor_weight = 83
    zia_agenda = agendaunit_shop(zia_text)
    zia_agenda.add_partyunit(yao_text, debtor_weight=yao_debtor_weight)
    zia_agenda.add_partyunit(wei_text, debtor_weight=wei_debtor_weight)
    zia_agenda.add_partyunit(zia_text, debtor_weight=zia_debtor_weight)
    x_sum = yao_debtor_weight + wei_debtor_weight + zia_debtor_weight
    zia_agenda.set_party_debtor_pool(x_sum)
    1
    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    new_sum = int(new_sum)
    zia_agenda.set_party_debtor_pool(
        new_party_debtor_pool=new_sum,
        update_partys_debtor_weight=True,
        correct_planck_issues=True,
    )

    # THEN
    assert zia_agenda._party_debtor_pool == new_sum
    assert zia_agenda.get_partyunits_debtor_weight_sum() == 117
    planck_valid_yao_debtor_weight = (yao_debtor_weight * new_ratio) - 0.5
    planck_valid_wei_debtor_weight = (wei_debtor_weight * new_ratio) - 0.5
    planck_valid_zia_debtor_weight = (zia_debtor_weight * new_ratio) - 0.5
    party_yao_debtor_weight = zia_agenda.get_party(yao_text).debtor_weight
    party_wei_debtor_weight = zia_agenda.get_party(wei_text).debtor_weight
    party_zia_debtor_weight = zia_agenda.get_party(zia_text).debtor_weight
    assert party_yao_debtor_weight == planck_valid_yao_debtor_weight
    assert party_wei_debtor_weight == planck_valid_wei_debtor_weight
    assert party_zia_debtor_weight == planck_valid_zia_debtor_weight + 1
    assert (
        zia_agenda.get_partyunits_debtor_weight_sum() == zia_agenda._party_debtor_pool
    )


def test_AgendaUnit_set_party_pool_CorrectlySetsAttrs():
    # GIVEN
    zia_text = "Zia"
    old_party_creditor_pool = 77
    old_party_debtor_pool = 88
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(zia_text)
    zia_agenda.set_party_creditor_pool(old_party_creditor_pool)
    zia_agenda.set_party_debtor_pool(old_party_debtor_pool)
    assert zia_agenda._party_creditor_pool == old_party_creditor_pool
    assert zia_agenda._party_debtor_pool == old_party_debtor_pool

    # WHEN
    new_party_pool = 200
    zia_agenda.set_party_pool(new_party_pool)

    # THEN
    assert zia_agenda._party_creditor_pool == new_party_pool
    assert zia_agenda._party_debtor_pool == new_party_pool
