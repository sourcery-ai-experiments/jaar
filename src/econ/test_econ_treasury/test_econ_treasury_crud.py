from src.change.filehub import filehub_shop
from src.agenda.agenda import agendaunit_shop
from src.econ.econ import econunit_shop
from src.econ.examples.econ_env_kit import get_texas_filehub, env_dir_setup_cleanup
from src.econ.treasury_sqlstr import get_agendatreasuryunits_dict


def test_EconUnit_treasury_get_agendaunits_ReturnsCorrectEmptyObj(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ = econunit_shop(get_texas_filehub())
    x_econ.create_treasury_db(in_memory=True)
    x_econ.refresh_treasury_job_agendas_data()

    # WHEN
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_econ.get_treasury_conn())

    # THEN
    assert len(x_agendatreasuryunits) == 0


def test_EconUnit_treasury_get_agendaunits_ReturnsCorrectNoneObj(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_texas_filehub())
    x_econ.create_treasury_db(in_memory=True)
    x_econ.refresh_treasury_job_agendas_data()
    assert len(get_agendatreasuryunits_dict(x_econ.get_treasury_conn())) == 0

    # WHEN
    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"
    x_econ.filehub.save_job_agenda(agendaunit_shop(_owner_id=sal_text))
    x_econ.filehub.save_job_agenda(agendaunit_shop(_owner_id=bob_text))
    x_econ.filehub.save_job_agenda(agendaunit_shop(_owner_id=tom_text))
    x_econ.filehub.save_job_agenda(agendaunit_shop(_owner_id=ava_text))
    x_econ.filehub.save_job_agenda(agendaunit_shop(_owner_id=elu_text))
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


def test_EconUnit_treasury_treasury_set_agendaunit_attrs_CorrectlyUpdatesRecord(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ = econunit_shop(get_texas_filehub())
    x_econ.create_treasury_db(in_memory=True)
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
    x_econ.filehub.save_job_agenda(sal_agenda)
    x_econ.filehub.save_job_agenda(bob_agenda)
    x_econ.filehub.save_job_agenda(tom_agenda)
    x_econ.filehub.save_job_agenda(ava_agenda)
    x_econ.filehub.save_job_agenda(elu_agenda)
    x_econ.refresh_treasury_job_agendas_data()
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_econ.get_treasury_conn())
    assert x_agendatreasuryunits.get(sal_text).rational is None
    assert x_agendatreasuryunits.get(bob_text).rational is None

    # WHEN
    sal_agenda.calc_agenda_metrics()
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
