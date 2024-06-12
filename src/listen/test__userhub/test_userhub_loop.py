from src._instrument.file import save_file
from src._road.jaar_config import get_test_real_id as real_id
from src._road.road import create_road
from src.listen.userhub import (
    userhub_shop,
    pipeline_role_job_text,
    pipeline_duty_work_text,
    pipeline_job_work_text,
)
from src.listen.examples.examples import get_agenda_with_4_levels
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises


def test_userhub_shop_RaisesErrorWhen_nox_type_IsInvalid():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    temp_env_dir = env_dir()
    x_nox_type = "work_duty1"

    with pytest_raises(Exception) as excinfo:
        userhub_shop(temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type)
    assert str(excinfo.value) == f"'{x_nox_type}' is an invalid nox_type"


def test_userhub_shop_AttrsAreCorrectWhen_nox_typeIs_role_job():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    temp_env_dir = env_dir()
    x_nox_type = pipeline_role_job_text()

    # WHEN
    sue_userhub = userhub_shop(
        temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type
    )

    # THEN
    assert sue_userhub._nox_type == "role_job"
    assert sue_userhub._nox_type == x_nox_type
    bob_text = "Bob"
    assert sue_userhub.speaker_dir(bob_text) == sue_userhub.jobs_dir()
    assert sue_userhub.speaker_file_name(bob_text) == f"{bob_text}.json"
    assert sue_userhub.listener_dir(bob_text) == sue_userhub.roles_dir()
    assert sue_userhub.listener_file_name(bob_text) == f"{bob_text}.json"
    assert sue_userhub.destination_dir(bob_text) == sue_userhub.jobs_dir()
    assert sue_userhub.destination_file_name(bob_text) == f"{bob_text}.json"


def test_UserHub_AttrsAreCorrectWhen_nox_typeIs_duty_work():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    temp_env_dir = env_dir()
    x_nox_type = pipeline_duty_work_text()

    # WHEN
    sue_userhub = userhub_shop(
        temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type
    )

    # THEN
    assert sue_userhub._nox_type == "duty_work"
    assert sue_userhub._nox_type == x_nox_type
    bob_text = "Bob"
    bob_userhub = userhub_shop(
        reals_dir=sue_userhub.reals_dir,
        real_id=sue_userhub.real_id,
        person_id=bob_text,
    )
    assert sue_userhub.speaker_dir(bob_text) == bob_userhub.work_dir()
    assert sue_userhub.speaker_file_name(bob_text) == f"{bob_text}.json"
    assert sue_userhub.listener_dir(bob_text) == sue_userhub.duty_dir()
    assert sue_userhub.listener_file_name(bob_text) == f"{sue_text}.json"
    assert sue_userhub.destination_dir(bob_text) == sue_userhub.work_dir()
    assert sue_userhub.destination_file_name(bob_text) == f"{sue_text}.json"


def test_UserHub_AttrsAreCorrectWhen_nox_typeIs_job_workScenario1():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    iowa_road = create_road(nation_road, "Iowa")
    ohio_road = create_road(nation_road, "Ohio")
    job_work = pipeline_job_work_text()

    # WHEN
    sue_userhub = userhub_shop(None, None, sue_text, nation_road, nox_type=job_work)
    s_reals_dir = sue_userhub.reals_dir
    sue_real_id = sue_userhub.real_id
    iowa_userhub = userhub_shop(s_reals_dir, sue_real_id, sue_text, iowa_road, job_work)
    ohio_userhub = userhub_shop(s_reals_dir, sue_real_id, sue_text, ohio_road, job_work)

    # THEN
    assert sue_userhub._nox_type == "job_work"
    assert sue_userhub._nox_type == job_work
    assert sue_userhub.econ_road == nation_road
    print(f"{iowa_userhub.econ_dir()=}")
    print(f"{ohio_userhub.econ_dir()=}")
    assert sue_userhub.econ_dir() != iowa_userhub.econ_dir()
    assert sue_userhub.econ_dir() != ohio_userhub.econ_dir()
    assert sue_userhub.speaker_dir(sue_text, iowa_road) == iowa_userhub.jobs_dir()
    assert sue_userhub.speaker_dir(sue_text, ohio_road) == ohio_userhub.jobs_dir()
    assert sue_userhub.speaker_file_name() == f"{sue_text}.json"
    assert sue_userhub.listener_dir() == sue_userhub.duty_dir()
    assert sue_userhub.listener_file_name() == f"{sue_text}.json"
    assert sue_userhub.destination_dir() == sue_userhub.work_dir()
    assert sue_userhub.destination_file_name() == f"{sue_text}.json"


def test_UserHub_AttrsAreCorrectWhen_nox_typeIs_job_workScenario2():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    iowa_road = create_road(nation_road, "Iowa")
    ohio_road = create_road(nation_road, "Ohio")
    job_work = pipeline_job_work_text()

    # WHEN
    sue_userhub = userhub_shop(None, None, sue_text, nation_road, nox_type=job_work)
    reals_dir = sue_userhub.reals_dir
    sue_real_id = sue_userhub.real_id
    bob_text = "Bob"
    iowa_userhub = userhub_shop(reals_dir, sue_real_id, bob_text, iowa_road, job_work)
    ohio_userhub = userhub_shop(reals_dir, sue_real_id, bob_text, ohio_road, job_work)

    # THEN
    assert sue_userhub._nox_type == "job_work"
    assert sue_userhub._nox_type == job_work
    assert sue_userhub.econ_road == nation_road
    print(f"{iowa_userhub.econ_dir()=}")
    print(f"{ohio_userhub.econ_dir()=}")
    assert sue_userhub.econ_dir() != iowa_userhub.econ_dir()
    assert sue_userhub.econ_dir() != ohio_userhub.econ_dir()
    assert sue_userhub.speaker_dir(bob_text, iowa_road) == iowa_userhub.jobs_dir()
    assert sue_userhub.speaker_dir(bob_text, ohio_road) == ohio_userhub.jobs_dir()
    assert sue_userhub.speaker_file_name() == f"{sue_text}.json"
    assert sue_userhub.listener_dir() == sue_userhub.duty_dir()
    assert sue_userhub.listener_file_name() == f"{sue_text}.json"
    assert sue_userhub.destination_dir() == sue_userhub.work_dir()
    assert sue_userhub.destination_file_name() == f"{sue_text}.json"


def test_UserHub_get_speaker_agenda_ReturnsObjWhenFileDoesNotExists():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    temp_env_dir = env_dir()
    x_nox_type = "role_job"
    sue_userhub = userhub_shop(
        temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type
    )

    # WHEN / THEN
    assert sue_userhub.get_speaker_agenda(sue_text) is None


def test_UserHub_get_speaker_agenda_ReturnsObj_role_job(env_dir_setup_cleanup):
    # GIVEN
    old_sue_agendaunit = get_agenda_with_4_levels()
    sue_text = old_sue_agendaunit._owner_id
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    sue_userhub = userhub_shop(
        env_dir(), real_id(), sue_text, nation_road, nox_type=pipeline_role_job_text()
    )
    speaker_dir = sue_userhub.speaker_dir(sue_text)
    speaker_file_name = sue_userhub.speaker_file_name(sue_text)
    save_file(speaker_dir, speaker_file_name, old_sue_agendaunit.get_json())

    # WHEN
    new_sue_agendaunit = sue_userhub.get_speaker_agenda(sue_text)

    # THEN
    assert old_sue_agendaunit.get_dict() == new_sue_agendaunit.get_dict()
    assert new_sue_agendaunit._owner_id == sue_text


def test_UserHub_get_perspective_agenda_ReturnsAgendaWith_owner_idSetToUserHub_person_id(
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
    perspective_agendaunit = sue_userhub.get_perspective_agenda(bob_agendaunit)

    # THEN
    assert perspective_agendaunit.get_dict() != bob_agendaunit.get_dict()
    assert perspective_agendaunit._owner_id == sue_text
    perspective_agendaunit.set_owner_id(bob_text)
    assert perspective_agendaunit.get_dict() == bob_agendaunit.get_dict()


def test_UserHub_get_speaker_perspective_ReturnsAgendaWith_owner_idSetToUserHub_person_id(
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
    sue_userhub.set_nox_type(pipeline_duty_work_text())

    # WHEN
    perspective_agendaunit = sue_userhub.get_speaker_perspective(bob_text)

    # THEN
    assert perspective_agendaunit.get_dict() != bob_agendaunit.get_dict()
    assert perspective_agendaunit._owner_id == sue_text
    perspective_agendaunit.set_owner_id(bob_text)
    assert perspective_agendaunit.get_dict() == bob_agendaunit.get_dict()


def test_UserHub_get_listener_agenda_ReturnsObjWhenFileDoesNotExists(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    temp_env_dir = env_dir()
    x_nox_type = "role_job"
    sue_userhub = userhub_shop(
        temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type
    )

    # WHEN / THEN
    assert sue_userhub.get_listener_agenda(sue_text) is None


def test_UserHub_get_listener_agenda_ReturnsObj_role_job(env_dir_setup_cleanup):
    # GIVEN
    old_sue_agendaunit = get_agenda_with_4_levels()
    sue_text = old_sue_agendaunit._owner_id
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    sue_userhub = userhub_shop(
        env_dir(), real_id(), sue_text, nation_road, nox_type=pipeline_role_job_text()
    )
    listener_dir = sue_userhub.listener_dir(sue_text)
    listener_file_name = sue_userhub.listener_file_name(sue_text)
    save_file(listener_dir, listener_file_name, old_sue_agendaunit.get_json())

    # WHEN
    new_sue_agendaunit = sue_userhub.get_listener_agenda(sue_text)

    # THEN
    assert old_sue_agendaunit.get_dict() == new_sue_agendaunit.get_dict()
    assert new_sue_agendaunit._owner_id == sue_text
