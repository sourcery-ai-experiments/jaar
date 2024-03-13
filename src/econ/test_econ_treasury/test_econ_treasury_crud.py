from src.agenda.agenda import agendaunit_shop
from src.econ.econ import econunit_shop
from src.econ.examples.econ_env_kit import (
    get_temp_env_econ_id,
    get_test_econ_dir,
    env_dir_setup_cleanup,
)
from src.econ.treasury_sqlstr import get_agendatreasuryunits_dict


def test_econ_treasury_get_agendaunits_ReturnsCorrectEmptyObj(env_dir_setup_cleanup):
    # GIVEN
    econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(econ_id, get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    x_econ.refresh_treasury_job_agendas_data()

    # WHEN
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_econ.get_treasury_conn())

    # THEN
    assert len(x_agendatreasuryunits) == 0


def test_econ_treasury_get_agendaunits_ReturnsCorrectNoneObj(env_dir_setup_cleanup):
    # GIVEN
    econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(econ_id, get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    x_econ.refresh_treasury_job_agendas_data()
    assert len(get_agendatreasuryunits_dict(x_econ.get_treasury_conn())) == 0

    # WHEN
    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"
    x_econ.save_job_agenda_to_forum(agendaunit_shop(_owner_id=sal_text))
    x_econ.save_job_agenda_to_forum(agendaunit_shop(_owner_id=bob_text))
    x_econ.save_job_agenda_to_forum(agendaunit_shop(_owner_id=tom_text))
    x_econ.save_job_agenda_to_forum(agendaunit_shop(_owner_id=ava_text))
    x_econ.save_job_agenda_to_forum(agendaunit_shop(_owner_id=elu_text))
    x_econ.refresh_treasury_job_agendas_data()
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_econ.get_treasury_conn())

    # THEN
    assert len(x_agendatreasuryunits) == 5
    assert x_agendatreasuryunits.get(sal_text) != None
    assert x_agendatreasuryunits.get(bob_text) != None
    assert x_agendatreasuryunits.get(tom_text) != None
    assert x_agendatreasuryunits.get(ava_text) != None
    assert x_agendatreasuryunits.get(elu_text) != None
    assert x_agendatreasuryunits.get(sal_text).owner_id == sal_text
    assert x_agendatreasuryunits.get(bob_text).owner_id == bob_text
    assert x_agendatreasuryunits.get(tom_text).owner_id == tom_text
    assert x_agendatreasuryunits.get(ava_text).owner_id == ava_text
    assert x_agendatreasuryunits.get(elu_text).owner_id == elu_text
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


def test_econ_treasury_treasury_set_agendaunit_attrs_CorrectlyUpdatesRecord(
    env_dir_setup_cleanup,
):
    # GIVEN
    econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(econ_id, get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    x_econ.refresh_treasury_job_agendas_data()
    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"
    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    x_econ.save_job_agenda_to_forum(sal_agenda)
    x_econ.save_job_agenda_to_forum(bob_agenda)
    x_econ.save_job_agenda_to_forum(tom_agenda)
    x_econ.save_job_agenda_to_forum(ava_agenda)
    x_econ.save_job_agenda_to_forum(elu_agenda)
    x_econ.refresh_treasury_job_agendas_data()
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_econ.get_treasury_conn())
    assert x_agendatreasuryunits.get(sal_text).rational is None
    assert x_agendatreasuryunits.get(bob_text).rational is None

    # WHEN
    sal_agenda.set_agenda_metrics()
    bob_rational = False
    bob_agenda._rational = bob_rational
    x_econ._treasury_set_agendaunit_attrs(sal_agenda)
    x_econ._treasury_set_agendaunit_attrs(bob_agenda)

    # THEN
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_econ.get_treasury_conn())
    print(f"{x_agendatreasuryunits.get(sal_text)=}")
    print(f"{x_agendatreasuryunits.get(bob_text)=}")
    print(f"{x_agendatreasuryunits.get(tom_text)=}")
    print(f"{x_agendatreasuryunits.get(ava_text)=}")
    print(f"{x_agendatreasuryunits.get(elu_text)=}")
    assert x_agendatreasuryunits.get(sal_text).rational
    assert x_agendatreasuryunits.get(bob_text).rational == bob_rational
