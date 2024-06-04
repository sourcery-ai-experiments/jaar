from src._road.jaar_config import work_str
from src.agenda.agenda import agendaunit_shop, get_from_json as agendaunit_get_from_json
from src.change.agendahub import agendahub_shop
from src.change.listen import listen_to_person_jobs
from src.real.admin_work import initialize_work_file
from src.real.real import realunit_shop
from src.real.examples.real_env_kit import (
    get_test_reals_dir,
    get_test_real_id,
    reals_dir_setup_cleanup,
)
from src.real.examples.example_reals import (
    get_example_yao_duty_with_3_healers,
    get_example_yao_job1_speaker,
    get_example_yao_job2_speaker,
    get_example_yao_job3_speaker,
    get_yao_iowa_agendahub,
    get_yao_ohio_agendahub,
    get_zia_utah_agendahub,
    get_iowa_road,
    get_ohio_road,
    get_utah_road,
    run_road,
    clean_road,
    cook_road,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists
from src._instrument.file import open_file, save_file, delete_dir


def test_work_file_exists_ReturnsCorrectBool(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_work_file_name = f"{work_str()}.json"
    sue_work_path = f"{sue_person_dir}/{sue_work_file_name}"
    print(f"{sue_work_path=}")
    assert os_path_exists(sue_work_path) == False
    sue_agendahub = agendahub_shop(None, None, sue_text, None)
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id())
    initialize_work_file(sue_agendahub, sue_agenda)
    assert sue_agendahub.work_file_exists()
    delete_dir(sue_agendahub.work_path())
    assert os_path_exists(sue_work_path) == False
    assert sue_agendahub.work_file_exists() == False

    # WHEN
    save_file(
        dest_dir=sue_agendahub.person_dir(),
        file_name=sue_agendahub.work_file_name(),
        file_text=agendaunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_work_path)
    assert sue_agendahub.work_file_exists()


def test_save_work_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_agendahub = agendahub_shop(None, None, sue_text, None)
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id())
    initialize_work_file(sue_agendahub, sue_agenda)
    assert sue_agendahub.work_file_exists()
    delete_dir(sue_agendahub.work_path())
    assert sue_agendahub.work_file_exists() == False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text)
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    sue_agendahub.save_work_agenda(sue_agenda)

    # THEN
    assert sue_agendahub.work_file_exists()

    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_work_file_name = f"{work_str()}.json"
    work_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda.party_exists(bob_text)

    # # WHEN
    sue2_agenda = agendaunit_shop(sue_text)
    zia_text = "Zia"
    sue2_agenda.add_partyunit(zia_text)
    sue_agendahub.save_work_agenda(sue2_agenda)

    # THEN
    work_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda.party_exists(zia_text)


def test_save_work_file_RaisesErrorWhenAgenda_work_id_IsWrong(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_agendahub = agendahub_shop(None, None, sue_text, None)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_agendahub.save_work_agenda(agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s work agenda."
    )


def test_initialize_work_file_CorrectlySavesFile(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_agendahub = agendahub_shop(None, None, sue_text, None)
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id())
    initialize_work_file(sue_agendahub, sue_agenda)
    assert sue_agendahub.work_file_exists()
    delete_dir(sue_agendahub.work_path())
    assert sue_agendahub.work_file_exists() == False

    # WHEN
    initialize_work_file(sue_agendahub, sue_agenda)

    # THEN
    work_agenda = sue_agendahub.get_work_agenda()
    assert work_agenda._real_id == get_test_real_id()
    assert work_agenda._owner_id == sue_text
    bob_text = "Bob"
    assert work_agenda.party_exists(bob_text) == False

    # GIVEN
    sue_agenda = agendaunit_shop(sue_text)
    sue_agenda.add_partyunit(bob_text)
    sue_agendahub.save_work_agenda(sue_agenda)
    work_agenda = sue_agendahub.get_work_agenda()
    assert work_agenda.get_party(bob_text)

    # WHEN
    initialize_work_file(sue_agendahub, sue_agenda)

    # THEN
    work_agenda = sue_agendahub.get_work_agenda()
    assert work_agenda.get_party(bob_text)


def test_initialize_work_file_CorrectlyDoesNotOverwrite(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_planck = 7
    sue_agendahub = agendahub_shop(None, None, sue_text, None, planck=sue_planck)
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id(), _planck=sue_planck)
    initialize_work_file(sue_agendahub, sue_agenda)
    assert sue_agendahub.work_file_exists()
    delete_dir(sue_agendahub.work_path())
    assert sue_agendahub.work_file_exists() == False

    # WHEN
    bob_text = "Bob"
    sue_agenda.add_partyunit(bob_text)
    initialize_work_file(sue_agendahub, sue_agenda)

    # THEN
    assert sue_agendahub.work_file_exists()

    sue_real_dir = f"{get_test_reals_dir()}/{get_test_real_id()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_work_file_name = f"{work_str()}.json"
    work_file_text = open_file(dest_dir=sue_person_dir, file_name=sue_work_file_name)
    print(f"{work_file_text=}")
    work_agenda = agendaunit_get_from_json(work_file_text)
    assert work_agenda._real_id == get_test_real_id()
    assert work_agenda._owner_id == sue_text
    assert work_agenda._planck == sue_planck


def test_initialize_work_file_CreatesDirsAndFiles(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_agendahub = agendahub_shop(None, None, sue_text, None)
    delete_dir(sue_agendahub.real_dir())
    assert os_path_exists(sue_agendahub.work_path()) is False

    # WHEN
    sue_agenda = agendaunit_shop(sue_text, get_test_real_id())
    initialize_work_file(sue_agendahub, sue_agenda)

    # THEN
    assert os_path_exists(sue_agendahub.work_path())


def test_listen_to_person_jobs_Pipeline_Scenario0(reals_dir_setup_cleanup):
    # GIVEN
    # yao0_duty with 3 debotors of different creditor_weights
    # yao_job1 with 1 task, belief that doesn't want that task
    # yao_job2 with 2 tasks, one is same belief wants task
    # yao_job3 with 1 new task, belief stays with it

    yao_duty0 = get_example_yao_duty_with_3_healers()
    yao_duty0.calc_agenda_metrics()
    assert yao_duty0._econ_dict.get(get_iowa_road())
    assert yao_duty0._econ_dict.get(get_ohio_road())
    assert yao_duty0._econ_dict.get(get_utah_road())
    yao_duty0.del_idea_obj(run_road())
    yao_duty0.calc_agenda_metrics()
    assert len(yao_duty0._econ_dict) == 3
    print(f"{yao_duty0._idea_dict.keys()=}")

    yao_text = yao_duty0._owner_id
    yao_job1 = get_example_yao_job1_speaker()
    yao_job2 = get_example_yao_job2_speaker()
    yao_job3 = get_example_yao_job3_speaker()
    yao_iowa_agendahub = get_yao_iowa_agendahub()
    yao_ohio_agendahub = get_yao_ohio_agendahub()
    yao_utah_agendahub = get_zia_utah_agendahub()
    assert yao_iowa_agendahub.duty_file_exists() == False
    assert yao_iowa_agendahub.work_file_exists() == False
    assert yao_iowa_agendahub.job_file_exists(yao_text) == False
    assert yao_ohio_agendahub.job_file_exists(yao_text) == False
    assert yao_utah_agendahub.job_file_exists(yao_text) == False
    yao_iowa_agendahub.save_duty_agenda(yao_duty0)
    yao_iowa_agendahub.save_job_agenda(yao_job1)
    yao_ohio_agendahub.save_job_agenda(yao_job2)
    yao_utah_agendahub.save_job_agenda(yao_job3)
    assert yao_iowa_agendahub.duty_file_exists()
    assert yao_iowa_agendahub.job_file_exists(yao_text)
    assert yao_ohio_agendahub.job_file_exists(yao_text)
    assert yao_utah_agendahub.job_file_exists(yao_text)

    # yao_job1 saves texas econ, healer is yao
    # yao job2 saves texas_econ, healer is yao
    # yao_job3 saves texas_econ, healer is bob

    # WHEN
    assert yao_iowa_agendahub.work_file_exists() == False
    listen_to_person_jobs(yao_iowa_agendahub)
    assert yao_iowa_agendahub.work_file_exists()

    yao_work = yao_iowa_agendahub.get_work_agenda()
    yao_work.calc_agenda_metrics()
    assert yao_work._partys.keys() == yao_duty0._partys.keys()
    assert yao_work.get_party(yao_text)._irrational_debtor_weight == 0
    assert yao_work.get_groupunits_dict() == yao_duty0.get_groupunits_dict()
    assert len(yao_work._idea_dict) == 11
    print(f"{yao_work._idea_dict.keys()=}")
    print(f"{yao_work.get_beliefunits_dict().keys()=}")
    assert yao_work.idea_exists(cook_road())
    assert yao_work.idea_exists(clean_road())
    assert len(yao_work._idearoot._beliefunits) == 2
    assert yao_work != yao_duty0
    assert yao_work.idea_exists(run_road())
