from src._instrument.file import save_file
from src._road.jaar_config import get_test_real_id as real_id
from src._road.road import create_road
from src.listen.userhub import userhub_shop
from src.listen.examples.examples import get_agenda_with_4_levels
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)


def test_UserHub_PipelineMethodsReturnCorrectObjs_role_job():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    temp_env_dir = env_dir()

    # WHEN
    sue_userhub = userhub_shop(temp_env_dir, None, sue_text, nation_road)

    # THEN
    bob_text = "Bob"
    assert sue_userhub.rolejob_role_file_name(bob_text) == f"{bob_text}.json"
    assert sue_userhub.rolejob_role_file_name(sue_text) == f"{sue_text}.json"
    sue_jobs_dir = sue_userhub.jobs_dir()
    assert sue_userhub.rolejob_role_dir(healer_id=sue_text) == sue_jobs_dir
    yao_text = "Yao"
    yao_userhub = userhub_shop(temp_env_dir, None, yao_text, nation_road)
    yao_jobs_dir = yao_userhub.jobs_dir()
    assert sue_userhub.rolejob_role_dir(healer_id=yao_text) == yao_jobs_dir
    yao_bob_job_path = yao_userhub.job_path(bob_text)
    assert yao_bob_job_path == sue_userhub.rj_speaker_file_path(
        healer_id=yao_text, speaker_id=bob_text
    )


def test_UserHub_PipelineMethodsReturnCorrectObjs_duty_work():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    temp_env_dir = env_dir()

    # WHEN
    sue_userhub = userhub_shop(temp_env_dir, None, sue_text, nation_road)

    # THEN
    bob_text = "Bob"

    bob_userhub = userhub_shop(env_dir(), sue_userhub.real_id, person_id=bob_text)
    assert sue_userhub.dw_speaker_dir(bob_text) == bob_userhub.work_dir()
    assert sue_userhub.dw_speaker_file_name(bob_text) == bob_userhub.work_file_name()
    assert sue_userhub.dw_speaker_file_path(bob_text) == bob_userhub.work_path()


def test_UserHub_PipelineMethodsReturnCorrectObjs_job_workScenario1():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    iowa_road = create_road(nation_road, "Iowa")
    ohio_road = create_road(nation_road, "Ohio")

    # WHEN
    sue_userhub = userhub_shop(None, None, sue_text, nation_road)
    s_reals_dir = sue_userhub.reals_dir
    sue_real_id = sue_userhub.real_id
    iowa_userhub = userhub_shop(s_reals_dir, sue_real_id, sue_text, iowa_road)
    ohio_userhub = userhub_shop(s_reals_dir, sue_real_id, sue_text, ohio_road)

    # THEN
    assert sue_userhub.econ_road == nation_road
    print(f"{iowa_userhub.econ_dir()=}")
    print(f"{ohio_userhub.econ_dir()=}")
    assert sue_userhub.econ_dir() != iowa_userhub.econ_dir()
    assert sue_userhub.econ_dir() != ohio_userhub.econ_dir()
    assert sue_userhub.jw_speaker_dir(sue_text, iowa_road) == iowa_userhub.jobs_dir()
    assert sue_userhub.jw_speaker_dir(sue_text, ohio_road) == ohio_userhub.jobs_dir()
    ohio_job_path = ohio_userhub.job_path(sue_text)
    assert sue_userhub.jw_speaker_file_path(sue_text, ohio_road) == ohio_job_path

    # assert sue_userhub.jw_speaker_file_name() == f"{sue_text}.json"
    # assert sue_userhub.jw_listener_dir() == sue_userhub.duty_dir()
    # assert sue_userhub.jw_listener_file_name() == f"{sue_text}.json"
    # assert sue_userhub.jw_destination_dir() == sue_userhub.work_dir()
    # assert sue_userhub.jw_destination_file_name() == f"{sue_text}.json"


def test_UserHub_PipelineMethodsReturnCorrectObjs_job_workScenario2():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    iowa_road = create_road(nation_road, "Iowa")
    ohio_road = create_road(nation_road, "Ohio")

    # WHEN
    sue_userhub = userhub_shop(None, None, sue_text, nation_road)
    reals_dir = sue_userhub.reals_dir
    bob_text = "Bob"
    iowa_userhub = userhub_shop(reals_dir, real_id(), bob_text, iowa_road)
    ohio_userhub = userhub_shop(reals_dir, real_id(), bob_text, ohio_road)

    # THEN
    assert sue_userhub.econ_road == nation_road
    print(f"{iowa_userhub.econ_dir()=}")
    print(f"{ohio_userhub.econ_dir()=}")
    assert sue_userhub.econ_dir() != iowa_userhub.econ_dir()
    assert sue_userhub.econ_dir() != ohio_userhub.econ_dir()
    assert sue_userhub.jw_speaker_dir(bob_text, iowa_road) == iowa_userhub.jobs_dir()
    assert sue_userhub.jw_speaker_dir(bob_text, ohio_road) == ohio_userhub.jobs_dir()
    ohio_job_path = ohio_userhub.job_path(sue_text)
    assert sue_userhub.jw_speaker_file_path(bob_text, ohio_road) == ohio_job_path
    # assert sue_userhub.jw_speaker_file_name() == f"{sue_text}.json"
    # assert sue_userhub.jw_listener_dir() == sue_userhub.duty_dir()
    # assert sue_userhub.jw_listener_file_name() == f"{sue_text}.json"
    # assert sue_userhub.jw_destination_dir() == sue_userhub.work_dir()
    # assert sue_userhub.jw_destination_file_name() == f"{sue_text}.json"


def test_UserHub_get_perspective_agenda_ReturnsAgendaWith_owner_idSetToUserHub_person_id():
    # GIVEN
    bob_text = "Bob"
    bob_agendaunit = get_agenda_with_4_levels()
    bob_agendaunit.set_owner_id(bob_text)

    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)

    # WHEN
    perspective_agendaunit = sue_userhub.get_perspective_agenda(bob_agendaunit)

    # THEN
    assert perspective_agendaunit.get_dict() != bob_agendaunit.get_dict()
    assert perspective_agendaunit._owner_id == sue_text
    perspective_agendaunit.set_owner_id(bob_text)
    assert perspective_agendaunit.get_dict() == bob_agendaunit.get_dict()


def test_UserHub_get_dw_perspective_agenda_ReturnsAgendaWith_owner_idSetToUserHub_person_id(
    env_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    bob_agendaunit = get_agenda_with_4_levels()
    bob_agendaunit.set_owner_id(bob_text)
    bob_userhub = userhub_shop(env_dir(), real_id(), bob_text)
    bob_userhub.save_work_agenda(bob_agendaunit)

    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)

    # WHEN
    perspective_agendaunit = sue_userhub.get_dw_perspective_agenda(bob_text)

    # THEN
    assert perspective_agendaunit._owner_id == sue_text
    assert perspective_agendaunit.get_dict() != bob_agendaunit.get_dict()
    perspective_agendaunit.set_owner_id(bob_text)
    assert perspective_agendaunit.get_dict() == bob_agendaunit.get_dict()


def test_UserHub_rj_perspective_agenda_ReturnsAgendaWith_owner_idSetToUserHub_person_id(
    env_dir_setup_cleanup,
):
    # GIVEN
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    iowa_road = create_road(nation_road, "Iowa")

    bob_text = "Bob"
    yao_text = "Yao"
    yao_agendaunit = get_agenda_with_4_levels()
    yao_agendaunit.set_owner_id(yao_text)

    bob_iowa_userhub = userhub_shop(env_dir(), real_id(), bob_text, iowa_road)
    bob_iowa_userhub.save_job_agenda(yao_agendaunit)

    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, iowa_road)

    # WHEN
    perspective_agendaunit = sue_userhub.rj_perspective_agenda(bob_text, yao_text)

    # THEN
    assert perspective_agendaunit._owner_id == sue_text
    assert perspective_agendaunit.get_dict() != yao_agendaunit.get_dict()
    perspective_agendaunit.set_owner_id(yao_text)
    assert perspective_agendaunit.get_dict() == yao_agendaunit.get_dict()
