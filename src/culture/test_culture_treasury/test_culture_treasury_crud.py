from src.agenda.agenda import agendaunit_shop
from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_qid,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from src.culture.treasury_sqlstr import (
    get_agendaunits_select_sqlstr,
    get_agendatreasuryunits_dict,
)


def test_culture_treasury_get_agendaunits_ReturnsCorrectEmptyObj(env_dir_setup_cleanup):
    # GIVEN
    culture_qid = get_temp_env_qid()
    x_culture = cultureunit_shop(culture_qid, get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_treasury=True)
    x_culture.refresh_treasury_public_agendas_data()

    # WHEN
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_culture.get_treasury_conn())

    # THEN
    assert len(x_agendatreasuryunits) == 0


def test_culture_treasury_get_agendaunits_ReturnsCorrectNoneObj(env_dir_setup_cleanup):
    # GIVEN
    culture_qid = get_temp_env_qid()
    x_culture = cultureunit_shop(culture_qid, get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_treasury=True)
    x_culture.refresh_treasury_public_agendas_data()
    assert len(get_agendatreasuryunits_dict(x_culture.get_treasury_conn())) == 0

    # WHEN
    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"
    x_culture.save_public_agenda(agendaunit_shop(_healer=sal_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=bob_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=tom_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=ava_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=elu_text))
    x_culture.refresh_treasury_public_agendas_data()
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_culture.get_treasury_conn())

    # THEN
    assert len(x_agendatreasuryunits) == 5
    assert x_agendatreasuryunits.get(sal_text) != None
    assert x_agendatreasuryunits.get(bob_text) != None
    assert x_agendatreasuryunits.get(tom_text) != None
    assert x_agendatreasuryunits.get(ava_text) != None
    assert x_agendatreasuryunits.get(elu_text) != None
    assert x_agendatreasuryunits.get(sal_text).healer == sal_text
    assert x_agendatreasuryunits.get(bob_text).healer == bob_text
    assert x_agendatreasuryunits.get(tom_text).healer == tom_text
    assert x_agendatreasuryunits.get(ava_text).healer == ava_text
    assert x_agendatreasuryunits.get(elu_text).healer == elu_text
    print(f"{x_agendatreasuryunits.get(sal_text)=}")
    print(f"{x_agendatreasuryunits.get(bob_text)=}")
    print(f"{x_agendatreasuryunits.get(tom_text)=}")
    print(f"{x_agendatreasuryunits.get(ava_text)=}")
    print(f"{x_agendatreasuryunits.get(elu_text)=}")
    assert x_agendatreasuryunits.get(sal_text).rational is None
    assert x_agendatreasuryunits.get(bob_text).rational is None
    assert x_agendatreasuryunits.get(tom_text).rational is None
    assert x_agendatreasuryunits.get(ava_text).rational is None
    assert x_agendatreasuryunits.get(elu_text).rational is None


def test_culture_treasury_treasury_set_agendaunit_attrs_CorrectlyUpdatesRecord(
    env_dir_setup_cleanup,
):
    # GIVEN
    culture_qid = get_temp_env_qid()
    x_culture = cultureunit_shop(culture_qid, get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_treasury=True)
    x_culture.refresh_treasury_public_agendas_data()
    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"
    sal_agenda = agendaunit_shop(_healer=sal_text)
    bob_agenda = agendaunit_shop(_healer=bob_text)
    tom_agenda = agendaunit_shop(_healer=tom_text)
    ava_agenda = agendaunit_shop(_healer=ava_text)
    elu_agenda = agendaunit_shop(_healer=elu_text)
    x_culture.save_public_agenda(sal_agenda)
    x_culture.save_public_agenda(bob_agenda)
    x_culture.save_public_agenda(tom_agenda)
    x_culture.save_public_agenda(ava_agenda)
    x_culture.save_public_agenda(elu_agenda)
    x_culture.refresh_treasury_public_agendas_data()
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_culture.get_treasury_conn())
    assert x_agendatreasuryunits.get(sal_text).rational is None
    assert x_agendatreasuryunits.get(bob_text).rational is None

    # WHEN
    sal_agenda.set_agenda_metrics()
    bob_rational = False
    bob_agenda._rational = bob_rational
    x_culture._treasury_set_agendaunit_attrs(sal_agenda)
    x_culture._treasury_set_agendaunit_attrs(bob_agenda)

    # THEN
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_culture.get_treasury_conn())
    print(f"{x_agendatreasuryunits.get(sal_text)=}")
    print(f"{x_agendatreasuryunits.get(bob_text)=}")
    print(f"{x_agendatreasuryunits.get(tom_text)=}")
    print(f"{x_agendatreasuryunits.get(ava_text)=}")
    print(f"{x_agendatreasuryunits.get(elu_text)=}")
    assert x_agendatreasuryunits.get(sal_text).rational
    assert x_agendatreasuryunits.get(bob_text).rational == bob_rational
