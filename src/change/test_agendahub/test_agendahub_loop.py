from src._instrument.file import save_file
from src._road.jaar_config import duty_str, work_str
from src._road.road import create_road, get_default_real_id_roadnode as root_label
from src.change.agendahub import (
    usernox_shop,
    agendahub_shop,
    pipeline_role_job_text,
    pipeline_duty_work_text,
    pipeline_job_work_text,
)
from src.change.examples.examples import get_agenda_with_4_levels
from src.change.examples.change_env import (
    env_dir_setup_cleanup,
    get_change_temp_env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_agendahub_shop_RaisesErrorWhen_nox_type_IsInvalid():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    temp_env_dir = get_change_temp_env_dir()
    x_nox_type = "work_duty1"

    with pytest_raises(Exception) as excinfo:
        agendahub_shop(temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type)
    assert str(excinfo.value) == f"'{x_nox_type}' is an invalid nox_type"


def test_agendahub_shop_AttrsAreCorrectWhen_nox_typeIs_role_job():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    temp_env_dir = get_change_temp_env_dir()
    x_nox_type = pipeline_role_job_text()

    # WHEN
    sue_agendahub = agendahub_shop(
        temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type
    )

    # THEN
    assert sue_agendahub._nox_type == "role_job"
    assert sue_agendahub._nox_type == x_nox_type
    bob_text = "Bob"
    assert sue_agendahub.speaker_dir(bob_text) == sue_agendahub.jobs_dir()
    assert sue_agendahub.speaker_file_name(bob_text) == f"{bob_text}.json"
    assert sue_agendahub.listener_dir(bob_text) == sue_agendahub.roles_dir()
    assert sue_agendahub.listener_file_name(bob_text) == f"{bob_text}.json"
    assert sue_agendahub.destination_dir(bob_text) == sue_agendahub.jobs_dir()
    assert sue_agendahub.destination_file_name(bob_text) == f"{bob_text}.json"


def test_AgendaHub_AttrsAreCorrectWhen_nox_typeIs_duty_work():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    temp_env_dir = get_change_temp_env_dir()
    x_nox_type = pipeline_duty_work_text()

    # WHEN
    sue_agendahub = agendahub_shop(
        temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type
    )

    # THEN
    assert sue_agendahub._nox_type == "duty_work"
    assert sue_agendahub._nox_type == x_nox_type
    bob_text = "Bob"
    bob_usernox = usernox_shop(
        reals_dir=sue_agendahub.reals_dir,
        real_id=sue_agendahub.real_id,
        person_id=bob_text,
    )
    assert sue_agendahub.speaker_dir(bob_text) == bob_usernox.person_dir()
    assert sue_agendahub.speaker_file_name(bob_text) == f"{work_str()}.json"
    assert sue_agendahub.listener_dir(bob_text) == sue_agendahub.person_dir()
    assert sue_agendahub.listener_file_name(bob_text) == f"{duty_str()}.json"
    assert sue_agendahub.destination_dir(bob_text) == sue_agendahub.person_dir()
    assert sue_agendahub.destination_file_name(bob_text) == f"{work_str()}.json"


def test_AgendaHub_AttrsAreCorrectWhen_nox_typeIs_job_workScenario1():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    iowa_road = create_road(nation_road, "Iowa")
    ohio_road = create_road(nation_road, "Ohio")
    job_work = pipeline_job_work_text()

    # WHEN
    sue_agendahub = agendahub_shop(None, None, sue_text, nation_road, nox_type=job_work)
    reals_dir = sue_agendahub.reals_dir
    real_id = sue_agendahub.real_id
    iowa_agendahub = agendahub_shop(reals_dir, real_id, sue_text, iowa_road, job_work)
    ohio_agendahub = agendahub_shop(reals_dir, real_id, sue_text, ohio_road, job_work)

    # THEN
    assert sue_agendahub._nox_type == "job_work"
    assert sue_agendahub._nox_type == job_work
    assert sue_agendahub.econ_road == nation_road
    assert sue_agendahub.econ_dir() != iowa_agendahub.econ_dir()
    assert sue_agendahub.econ_dir() != ohio_agendahub.econ_dir()
    assert sue_agendahub.speaker_dir(sue_text, iowa_road) == iowa_agendahub.jobs_dir()
    assert sue_agendahub.speaker_dir(sue_text, ohio_road) == ohio_agendahub.jobs_dir()
    assert sue_agendahub.speaker_file_name() == f"{sue_text}.json"
    assert sue_agendahub.listener_dir() == sue_agendahub.person_dir()
    assert sue_agendahub.listener_file_name() == f"{duty_str()}.json"
    assert sue_agendahub.destination_dir() == sue_agendahub.person_dir()
    assert sue_agendahub.destination_file_name() == f"{work_str()}.json"


def test_AgendaHub_AttrsAreCorrectWhen_nox_typeIs_job_workScenario2():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    iowa_road = create_road(nation_road, "Iowa")
    ohio_road = create_road(nation_road, "Ohio")
    job_work = pipeline_job_work_text()

    # WHEN
    sue_agendahub = agendahub_shop(None, None, sue_text, nation_road, nox_type=job_work)
    reals_dir = sue_agendahub.reals_dir
    real_id = sue_agendahub.real_id
    bob_text = "Bob"
    iowa_agendahub = agendahub_shop(reals_dir, real_id, bob_text, iowa_road, job_work)
    ohio_agendahub = agendahub_shop(reals_dir, real_id, bob_text, ohio_road, job_work)

    # THEN
    assert sue_agendahub._nox_type == "job_work"
    assert sue_agendahub._nox_type == job_work
    assert sue_agendahub.econ_road == nation_road
    assert sue_agendahub.econ_dir() != iowa_agendahub.econ_dir()
    assert sue_agendahub.econ_dir() != ohio_agendahub.econ_dir()
    assert sue_agendahub.speaker_dir(bob_text, iowa_road) == iowa_agendahub.jobs_dir()
    assert sue_agendahub.speaker_dir(bob_text, ohio_road) == ohio_agendahub.jobs_dir()
    assert sue_agendahub.speaker_file_name() == f"{sue_text}.json"
    assert sue_agendahub.listener_dir() == sue_agendahub.person_dir()
    assert sue_agendahub.listener_file_name() == f"{duty_str()}.json"
    assert sue_agendahub.destination_dir() == sue_agendahub.person_dir()
    assert sue_agendahub.destination_file_name() == f"{work_str()}.json"


def test_AgendaHub_get_speaker_agenda_ReturnsObjWhenFileDoesNotExists():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    temp_env_dir = get_change_temp_env_dir()
    x_nox_type = "role_job"
    sue_agendahub = agendahub_shop(
        temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type
    )

    # WHEN / THEN
    assert sue_agendahub.get_speaker_agenda(sue_text) is None


def test_AgendaHub_get_speaker_agenda_ReturnsObj_role_job(env_dir_setup_cleanup):
    # GIVEN
    old_sue_agendaunit = get_agenda_with_4_levels()
    sue_text = old_sue_agendaunit._owner_id
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    env_dir = get_change_temp_env_dir()
    real_id = root_label()
    sue_agendahub = agendahub_shop(
        env_dir, real_id, sue_text, nation_road, nox_type=pipeline_role_job_text()
    )
    speaker_dir = sue_agendahub.speaker_dir(sue_text)
    speaker_file_name = sue_agendahub.speaker_file_name(sue_text)
    save_file(speaker_dir, speaker_file_name, old_sue_agendaunit.get_json())

    # WHEN
    new_sue_agendaunit = sue_agendahub.get_speaker_agenda(sue_text)

    # THEN
    assert old_sue_agendaunit.get_dict() == new_sue_agendaunit.get_dict()
    assert new_sue_agendaunit._owner_id == sue_text


def test_AgendaHub_get_listener_agenda_ReturnsObjWhenFileDoesNotExists(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    temp_env_dir = get_change_temp_env_dir()
    x_nox_type = "role_job"
    sue_agendahub = agendahub_shop(
        temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type
    )

    # WHEN / THEN
    assert sue_agendahub.get_listener_agenda(sue_text) is None


def test_AgendaHub_get_listener_agenda_ReturnsObj_role_job(env_dir_setup_cleanup):
    # GIVEN
    old_sue_agendaunit = get_agenda_with_4_levels()
    sue_text = old_sue_agendaunit._owner_id
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    env_dir = get_change_temp_env_dir()
    real_id = root_label()
    sue_agendahub = agendahub_shop(
        env_dir, real_id, sue_text, nation_road, nox_type=pipeline_role_job_text()
    )
    listener_dir = sue_agendahub.listener_dir(sue_text)
    listener_file_name = sue_agendahub.listener_file_name(sue_text)
    save_file(listener_dir, listener_file_name, old_sue_agendaunit.get_json())

    # WHEN
    new_sue_agendaunit = sue_agendahub.get_listener_agenda(sue_text)

    # THEN
    assert old_sue_agendaunit.get_dict() == new_sue_agendaunit.get_dict()
    assert new_sue_agendaunit._owner_id == sue_text
