from src._instrument.file import save_file
from src._road.jaar_config import duty_str, work_str
from src._road.road import create_road, get_default_real_id_roadnode as root_label
from src.change.agendanox import usernox_shop, agendanox_shop, pipeline_role_job_text
from src.change.examples.examples import get_agenda_with_4_levels
from src.change.examples.change_env import (
    env_dir_setup_cleanup,
    get_change_temp_env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_AgendaNox_agendanox_shop_RaisesErrorWhen_nox_type_IsInvalid():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    temp_env_dir = get_change_temp_env_dir()
    x_nox_type = "work_duty1"

    with pytest_raises(Exception) as excinfo:
        agendanox_shop(temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type)
    assert str(excinfo.value) == f"'{x_nox_type}' is an invalid nox_type"


def test_AgendaNox_agendanox_shop_When_nox_typeIs_role_job_AttrsAreCorrect():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    temp_env_dir = get_change_temp_env_dir()
    x_nox_type = "role_job"

    # WHEN
    sue_agendanox = agendanox_shop(
        temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type
    )

    # THEN
    assert sue_agendanox._nox_type == "role_job"
    assert sue_agendanox._nox_type == x_nox_type
    bob_text = "Bob"
    assert sue_agendanox.speaker_dir(bob_text) == sue_agendanox.jobs_dir()
    assert sue_agendanox.speaker_file_name(bob_text) == f"{bob_text}.json"
    assert sue_agendanox.listener_dir(bob_text) == sue_agendanox.roles_dir()
    assert sue_agendanox.listener_file_name(bob_text) == f"{bob_text}.json"
    assert sue_agendanox.destination_dir(bob_text) == sue_agendanox.jobs_dir()
    assert sue_agendanox.destination_file_name(bob_text) == f"{bob_text}.json"


def test_AgendaNox_agendanox_shop_When_nox_typeIs_duty_work_AttrsAreCorrect():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    temp_env_dir = get_change_temp_env_dir()
    x_nox_type = "duty_work"

    # WHEN
    sue_agendanox = agendanox_shop(
        temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type
    )

    # THEN
    assert sue_agendanox._nox_type == "duty_work"
    assert sue_agendanox._nox_type == x_nox_type
    bob_text = "Bob"
    bob_usernox = usernox_shop(
        reals_dir=sue_agendanox.reals_dir,
        real_id=sue_agendanox.real_id,
        person_id=bob_text,
    )
    assert sue_agendanox.speaker_dir(bob_text) == bob_usernox.person_dir()
    assert sue_agendanox.speaker_file_name(bob_text) == f"{work_str()}.json"
    assert sue_agendanox.listener_dir(bob_text) == sue_agendanox.person_dir()
    assert sue_agendanox.listener_file_name(bob_text) == f"{duty_str()}.json"
    assert sue_agendanox.destination_dir(bob_text) == sue_agendanox.person_dir()
    assert sue_agendanox.destination_file_name(bob_text) == f"{work_str()}.json"


# def test_AgendaNox_agendanox_shop_When_nox_typeIs_job_work_AttrsAreCorrect(
#
# ):
#     # GIVEN
#     sue_text = "Sue"
#     nation_text = "nation-state"
#     nation_road = create_road(root_label(), nation_text)
#     temp_env_dir = get_change_temp_env_dir()
#     x_nox_type = "job_work"

#     # WHEN
#     sue_agendanox = agendanox_shop(
#         temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type
#     )

#     # THEN
#     assert sue_agendanox._nox_type == "job_work"
#     assert sue_agendanox._nox_type == x_nox_type
#     bob_text = "Bob"
#     bob_agendanox = agendanox_shop(
#         reals_dir=sue_agendanox.reals_dir,
#         real_id=sue_agendanox.real_id,
#         person_id=bob_text,
#         econ_road=nation_road,

#     )
#     assert sue_agendanox.speaker_dir(bob_text) == bob_usernox.person_dir()
#     assert sue_agendanox.speaker_file_name(bob_text) == f"{work_str()}.json"
#     assert sue_agendanox.listener_dir(bob_text) == sue_agendanox.person_dir()
#     assert sue_agendanox.listener_file_name(bob_text) == f"{duty_str()}.json"
#     assert sue_agendanox.destination_dir(bob_text) == sue_agendanox.person_dir()
#     assert sue_agendanox.destination_file_name(bob_text) == f"{work_str()}.json"


def test_AgendaNox_get_speaker_agenda_ReturnsObjWhenFileDoesNotExists(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    temp_env_dir = get_change_temp_env_dir()
    x_nox_type = "role_job"
    sue_agendanox = agendanox_shop(
        temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type
    )

    # WHEN / THEN
    assert sue_agendanox.get_speaker_agenda(sue_text) is None


def test_AgendaNox_get_speaker_agenda_ReturnsObj_role_job(env_dir_setup_cleanup):
    # GIVEN
    old_sue_agendaunit = get_agenda_with_4_levels()
    sue_text = old_sue_agendaunit._owner_id
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    env_dir = get_change_temp_env_dir()
    real_id = root_label()
    sue_agendanox = agendanox_shop(
        env_dir, real_id, sue_text, nation_road, nox_type=pipeline_role_job_text()
    )
    speaker_dir = sue_agendanox.speaker_dir(sue_text)
    speaker_file_name = sue_agendanox.speaker_file_name(sue_text)
    save_file(speaker_dir, speaker_file_name, old_sue_agendaunit.get_json())

    # WHEN
    new_sue_agendaunit = sue_agendanox.get_speaker_agenda(sue_text)

    # THEN
    assert old_sue_agendaunit.get_dict() == new_sue_agendaunit.get_dict()
    assert new_sue_agendaunit._owner_id == sue_text


def test_AgendaNox_get_listener_agenda_ReturnsObjWhenFileDoesNotExists(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    temp_env_dir = get_change_temp_env_dir()
    x_nox_type = "role_job"
    sue_agendanox = agendanox_shop(
        temp_env_dir, None, sue_text, nation_road, nox_type=x_nox_type
    )

    # WHEN / THEN
    assert sue_agendanox.get_listener_agenda(sue_text) is None


def test_AgendaNox_get_listener_agenda_ReturnsObj_role_job(env_dir_setup_cleanup):
    # GIVEN
    old_sue_agendaunit = get_agenda_with_4_levels()
    sue_text = old_sue_agendaunit._owner_id
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    env_dir = get_change_temp_env_dir()
    real_id = root_label()
    sue_agendanox = agendanox_shop(
        env_dir, real_id, sue_text, nation_road, nox_type=pipeline_role_job_text()
    )
    listener_dir = sue_agendanox.listener_dir(sue_text)
    listener_file_name = sue_agendanox.listener_file_name(sue_text)
    save_file(listener_dir, listener_file_name, old_sue_agendaunit.get_json())

    # WHEN
    new_sue_agendaunit = sue_agendanox.get_listener_agenda(sue_text)

    # THEN
    assert old_sue_agendaunit.get_dict() == new_sue_agendaunit.get_dict()
    assert new_sue_agendaunit._owner_id == sue_text
