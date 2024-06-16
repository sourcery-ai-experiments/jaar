from src.agenda.agenda import agendaunit_shop
from pytest import raises as pytest_raises


def test_AgendaUnit_set_guy_credor_pool_CorrectlySetsInt():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")
    assert zia_agenda._guy_credor_pool is None
    # WHEN
    x_guy_credor_pool = 11
    zia_agenda.set_guy_credor_pool(x_guy_credor_pool)
    # THEN
    assert zia_agenda._guy_credor_pool == x_guy_credor_pool


def test_AgendaUnit_set_guy_credor_pool_CorrectlySets_guys_credor_weightWithEmpty_guys():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")

    # WHEN
    x_guy_credor_pool = 77
    zia_agenda.set_guy_credor_pool(x_guy_credor_pool, update_guys_credor_weight=True)

    # THEN
    assert zia_agenda._guy_credor_pool == x_guy_credor_pool


def test_AgendaUnit_set_guy_credor_pool_RaisesErrorWhenArgIsNotMultiple():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(zia_text)
    x_guy_credor_pool = 23
    zia_agenda.set_guy_credor_pool(x_guy_credor_pool)
    assert zia_agenda._planck == 1
    assert zia_agenda._guy_credor_pool == x_guy_credor_pool

    # WHEN
    new_guy_credor_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_agenda.set_guy_credor_pool(new_guy_credor_pool)
    assert (
        str(excinfo.value)
        == f"Agenda '{zia_text}' cannot set _guy_credor_pool='{new_guy_credor_pool}'. It is not divisible by planck '{zia_agenda._planck}'"
    )


def test_AgendaUnit_set_guy_credor_pool_CorrectlyModifies_guys_credor_weight():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_credor_weight = 73
    wei_credor_weight = 79
    zia_credor_weight = 83
    zia_agenda = agendaunit_shop(_owner_id=zia_text)
    zia_agenda.add_guyunit(yao_text, credor_weight=yao_credor_weight)
    zia_agenda.add_guyunit(wei_text, credor_weight=wei_credor_weight)
    zia_agenda.add_guyunit(zia_text, credor_weight=zia_credor_weight)
    x_sum = yao_credor_weight + wei_credor_weight + zia_credor_weight
    zia_agenda.set_guy_credor_pool(x_sum)
    assert zia_agenda._guy_credor_pool == x_sum
    assert zia_agenda.get_guy(yao_text).credor_weight == yao_credor_weight
    assert zia_agenda.get_guy(wei_text).credor_weight == wei_credor_weight
    assert zia_agenda.get_guy(zia_text).credor_weight == zia_credor_weight

    # WHEN
    new_ratio = 2
    new_sum = x_sum * new_ratio
    zia_agenda.set_guy_credor_pool(new_sum, update_guys_credor_weight=True)

    # THEN
    assert zia_agenda._guy_credor_pool == new_sum
    new_yao_credor_weight = yao_credor_weight * new_ratio
    new_wei_credor_weight = wei_credor_weight * new_ratio
    new_zia_credor_weight = zia_credor_weight * new_ratio
    assert zia_agenda.get_guy(yao_text).credor_weight == new_yao_credor_weight
    assert zia_agenda.get_guy(wei_text).credor_weight == new_wei_credor_weight
    assert zia_agenda.get_guy(zia_text).credor_weight == new_zia_credor_weight


def test_AgendaUnit_set_guy_credor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_planckAND_correct_planck_issuesIsFalse():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_credor_weight = 73
    wei_credor_weight = 79
    zia_credor_weight = 83
    zia_agenda = agendaunit_shop(zia_text)
    zia_agenda.add_guyunit(yao_text, credor_weight=yao_credor_weight)
    zia_agenda.add_guyunit(wei_text, credor_weight=wei_credor_weight)
    zia_agenda.add_guyunit(zia_text, credor_weight=zia_credor_weight)
    x_sum = yao_credor_weight + wei_credor_weight + zia_credor_weight
    zia_agenda.set_guy_credor_pool(x_sum)
    assert zia_agenda._guy_credor_pool == x_sum
    assert zia_agenda.get_guy(yao_text).credor_weight == yao_credor_weight
    assert zia_agenda.get_guy(wei_text).credor_weight == wei_credor_weight
    assert zia_agenda.get_guy(zia_text).credor_weight == zia_credor_weight

    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    print(f"{new_sum=}")
    new_sum = int(new_sum)
    print(f"{new_sum=}")
    zia_agenda.set_guy_credor_pool(
        new_guy_credor_pool=new_sum,
        update_guys_credor_weight=True,
        correct_planck_issues=False,
    )

    # THEN
    assert zia_agenda._guy_credor_pool == new_sum
    guy_yao_credor_weight = zia_agenda.get_guy(yao_text).credor_weight
    guy_wei_credor_weight = zia_agenda.get_guy(wei_text).credor_weight
    guy_zia_credor_weight = zia_agenda.get_guy(zia_text).credor_weight
    assert guy_yao_credor_weight == (yao_credor_weight * new_ratio) - 0.5
    assert guy_wei_credor_weight == (wei_credor_weight * new_ratio) - 0.5
    assert guy_zia_credor_weight == (zia_credor_weight * new_ratio) - 0.5
    assert zia_agenda.get_guyunits_credor_weight_sum() == 116
    assert zia_agenda.get_guyunits_credor_weight_sum() != zia_agenda._guy_credor_pool


def test_AgendaUnit_set_guy_credor_pool_SetAttrWhenEmpty_correct_planck_issues_IsTrue():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")

    # WHEN
    new_sum = 5000
    zia_agenda.set_guy_credor_pool(
        new_guy_credor_pool=new_sum,
        update_guys_credor_weight=True,
        correct_planck_issues=True,
    )

    # THEN
    assert zia_agenda._guy_credor_pool == new_sum
    assert zia_agenda.get_guyunits_credor_weight_sum() == 0


def test_AgendaUnit_set_guy_credor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_planckAND_correct_planck_issuesIsTrue():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_credor_weight = 73
    wei_credor_weight = 79
    zia_credor_weight = 83
    zia_agenda = agendaunit_shop(zia_text)
    zia_agenda.add_guyunit(yao_text, credor_weight=yao_credor_weight)
    zia_agenda.add_guyunit(wei_text, credor_weight=wei_credor_weight)
    zia_agenda.add_guyunit(zia_text, credor_weight=zia_credor_weight)
    x_sum = yao_credor_weight + wei_credor_weight + zia_credor_weight
    zia_agenda.set_guy_credor_pool(x_sum)
    1
    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    new_sum = int(new_sum)
    zia_agenda.set_guy_credor_pool(
        new_guy_credor_pool=new_sum,
        update_guys_credor_weight=True,
        correct_planck_issues=True,
    )

    # THEN
    assert zia_agenda._guy_credor_pool == new_sum
    assert zia_agenda.get_guyunits_credor_weight_sum() == 117
    planck_valid_yao_credor_weight = (yao_credor_weight * new_ratio) - 0.5
    planck_valid_wei_credor_weight = (wei_credor_weight * new_ratio) - 0.5
    planck_valid_zia_credor_weight = (zia_credor_weight * new_ratio) - 0.5
    guy_yao_credor_weight = zia_agenda.get_guy(yao_text).credor_weight
    guy_wei_credor_weight = zia_agenda.get_guy(wei_text).credor_weight
    guy_zia_credor_weight = zia_agenda.get_guy(zia_text).credor_weight
    assert guy_yao_credor_weight == planck_valid_yao_credor_weight
    assert guy_wei_credor_weight == planck_valid_wei_credor_weight
    assert guy_zia_credor_weight == planck_valid_zia_credor_weight + 1
    assert zia_agenda.get_guyunits_credor_weight_sum() == zia_agenda._guy_credor_pool


def test_AgendaUnit_set_guy_debtor_pool_CorrectlySetsInt():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_owner_id=zia_text)
    assert zia_agenda._guy_debtor_pool is None

    # WHEN
    x_guy_debtor_pool = 13
    zia_agenda.set_guy_debtor_pool(x_guy_debtor_pool)
    # THEN
    assert zia_agenda._guy_debtor_pool == x_guy_debtor_pool


def test_AgendaUnit_set_guy_debtor_pool_CorrectlySets_guys_debtor_weightWithEmpty_guys():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(_owner_id=zia_text)

    # WHEN
    x_guy_debtor_pool = 77
    zia_agenda.set_guy_debtor_pool(x_guy_debtor_pool, update_guys_debtor_weight=True)

    # THEN
    assert zia_agenda._guy_debtor_pool == x_guy_debtor_pool


def test_AgendaUnit_set_guy_debtor_pool_RaisesErrorWhenArgIsNotMultiple():
    # GIVEN
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(zia_text)
    x_guy_debtor_pool = 23
    zia_agenda.set_guy_debtor_pool(x_guy_debtor_pool, update_guys_debtor_weight=True)
    assert zia_agenda._planck == 1
    assert zia_agenda._guy_debtor_pool == x_guy_debtor_pool

    # WHEN
    new_guy_debtor_pool = 13.5
    with pytest_raises(Exception) as excinfo:
        zia_agenda.set_guy_debtor_pool(
            new_guy_debtor_pool, update_guys_debtor_weight=True
        )
    assert (
        str(excinfo.value)
        == f"Agenda '{zia_text}' cannot set _guy_debtor_pool='{new_guy_debtor_pool}'. It is not divisible by planck '{zia_agenda._planck}'"
    )


def test_AgendaUnit_set_guy_debtor_pool_CorrectlyModifies_guys_debtor_weight():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_debtor_weight = 73
    wei_debtor_weight = 79
    zia_debtor_weight = 83
    zia_agenda = agendaunit_shop(_owner_id=zia_text)
    zia_agenda.add_guyunit(yao_text, debtor_weight=yao_debtor_weight)
    zia_agenda.add_guyunit(wei_text, debtor_weight=wei_debtor_weight)
    zia_agenda.add_guyunit(zia_text, debtor_weight=zia_debtor_weight)
    x_sum = yao_debtor_weight + wei_debtor_weight + zia_debtor_weight
    zia_agenda.set_guy_debtor_pool(x_sum)
    assert zia_agenda._guy_debtor_pool == x_sum
    assert zia_agenda.get_guy(yao_text).debtor_weight == yao_debtor_weight
    assert zia_agenda.get_guy(wei_text).debtor_weight == wei_debtor_weight
    assert zia_agenda.get_guy(zia_text).debtor_weight == zia_debtor_weight

    # WHEN
    new_ratio = 2
    new_sum = x_sum * new_ratio
    zia_agenda.set_guy_debtor_pool(new_sum, update_guys_debtor_weight=True)

    # THEN
    assert zia_agenda._guy_debtor_pool == new_sum
    new_yao_debtor_weight = yao_debtor_weight * new_ratio
    new_wei_debtor_weight = wei_debtor_weight * new_ratio
    new_zia_debtor_weight = zia_debtor_weight * new_ratio
    assert zia_agenda.get_guy(yao_text).debtor_weight == new_yao_debtor_weight
    assert zia_agenda.get_guy(wei_text).debtor_weight == new_wei_debtor_weight
    assert zia_agenda.get_guy(zia_text).debtor_weight == new_zia_debtor_weight


def test_AgendaUnit_set_guy_debtor_pool_SetAttrWhenEmpty_correct_planck_issues_IsTrue():
    # GIVEN
    zia_agenda = agendaunit_shop("Zia")

    # WHEN
    new_sum = 5000
    zia_agenda.set_guy_debtor_pool(
        new_guy_debtor_pool=new_sum,
        update_guys_debtor_weight=True,
        correct_planck_issues=True,
    )

    # THEN
    assert zia_agenda._guy_debtor_pool == new_sum
    assert zia_agenda.get_guyunits_debtor_weight_sum() == 0


def test_AgendaUnit_set_guy_debtor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_planckAND_correct_planck_issuesIsFalse():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_debtor_weight = 73
    wei_debtor_weight = 79
    zia_debtor_weight = 83
    zia_agenda = agendaunit_shop(zia_text)
    zia_agenda.add_guyunit(yao_text, debtor_weight=yao_debtor_weight)
    zia_agenda.add_guyunit(wei_text, debtor_weight=wei_debtor_weight)
    zia_agenda.add_guyunit(zia_text, debtor_weight=zia_debtor_weight)
    x_sum = yao_debtor_weight + wei_debtor_weight + zia_debtor_weight
    zia_agenda.set_guy_debtor_pool(x_sum)
    assert zia_agenda._guy_debtor_pool == x_sum
    assert zia_agenda.get_guy(yao_text).debtor_weight == yao_debtor_weight
    assert zia_agenda.get_guy(wei_text).debtor_weight == wei_debtor_weight
    assert zia_agenda.get_guy(zia_text).debtor_weight == zia_debtor_weight

    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    print(f"{new_sum=}")
    new_sum = int(new_sum)
    print(f"{new_sum=}")
    zia_agenda.set_guy_debtor_pool(
        new_guy_debtor_pool=new_sum,
        update_guys_debtor_weight=True,
        correct_planck_issues=False,
    )

    # THEN
    assert zia_agenda._guy_debtor_pool == new_sum
    guy_yao_debtor_weight = zia_agenda.get_guy(yao_text).debtor_weight
    guy_wei_debtor_weight = zia_agenda.get_guy(wei_text).debtor_weight
    guy_zia_debtor_weight = zia_agenda.get_guy(zia_text).debtor_weight
    assert guy_yao_debtor_weight == (yao_debtor_weight * new_ratio) - 0.5
    assert guy_wei_debtor_weight == (wei_debtor_weight * new_ratio) - 0.5
    assert guy_zia_debtor_weight == (zia_debtor_weight * new_ratio) - 0.5
    assert zia_agenda.get_guyunits_debtor_weight_sum() == 116
    assert zia_agenda.get_guyunits_debtor_weight_sum() != zia_agenda._guy_debtor_pool


def test_AgendaUnit_set_guy_debtor_pool_CorrectlySetsAttrsWhenWeightsNotDivisibleBy_planckAND_correct_planck_issuesIsTrue():
    # GIVEN
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    yao_debtor_weight = 73
    wei_debtor_weight = 79
    zia_debtor_weight = 83
    zia_agenda = agendaunit_shop(zia_text)
    zia_agenda.add_guyunit(yao_text, debtor_weight=yao_debtor_weight)
    zia_agenda.add_guyunit(wei_text, debtor_weight=wei_debtor_weight)
    zia_agenda.add_guyunit(zia_text, debtor_weight=zia_debtor_weight)
    x_sum = yao_debtor_weight + wei_debtor_weight + zia_debtor_weight
    zia_agenda.set_guy_debtor_pool(x_sum)
    1
    # WHEN
    new_ratio = 0.5
    new_sum = x_sum * new_ratio
    new_sum = int(new_sum)
    zia_agenda.set_guy_debtor_pool(
        new_guy_debtor_pool=new_sum,
        update_guys_debtor_weight=True,
        correct_planck_issues=True,
    )

    # THEN
    assert zia_agenda._guy_debtor_pool == new_sum
    assert zia_agenda.get_guyunits_debtor_weight_sum() == 117
    planck_valid_yao_debtor_weight = (yao_debtor_weight * new_ratio) - 0.5
    planck_valid_wei_debtor_weight = (wei_debtor_weight * new_ratio) - 0.5
    planck_valid_zia_debtor_weight = (zia_debtor_weight * new_ratio) - 0.5
    guy_yao_debtor_weight = zia_agenda.get_guy(yao_text).debtor_weight
    guy_wei_debtor_weight = zia_agenda.get_guy(wei_text).debtor_weight
    guy_zia_debtor_weight = zia_agenda.get_guy(zia_text).debtor_weight
    assert guy_yao_debtor_weight == planck_valid_yao_debtor_weight
    assert guy_wei_debtor_weight == planck_valid_wei_debtor_weight
    assert guy_zia_debtor_weight == planck_valid_zia_debtor_weight + 1
    assert zia_agenda.get_guyunits_debtor_weight_sum() == zia_agenda._guy_debtor_pool


def test_AgendaUnit_set_guy_pool_CorrectlySetsAttrs():
    # GIVEN
    zia_text = "Zia"
    old_guy_credor_pool = 77
    old_guy_debtor_pool = 88
    zia_text = "Zia"
    zia_agenda = agendaunit_shop(zia_text)
    zia_agenda.set_guy_credor_pool(old_guy_credor_pool)
    zia_agenda.set_guy_debtor_pool(old_guy_debtor_pool)
    assert zia_agenda._guy_credor_pool == old_guy_credor_pool
    assert zia_agenda._guy_debtor_pool == old_guy_debtor_pool

    # WHEN
    new_guy_pool = 200
    zia_agenda.set_guy_pool(new_guy_pool)

    # THEN
    assert zia_agenda._guy_credor_pool == new_guy_pool
    assert zia_agenda._guy_debtor_pool == new_guy_pool
