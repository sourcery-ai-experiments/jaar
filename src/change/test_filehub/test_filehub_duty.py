from src._instrument.file import open_file, dir_files, delete_dir, set_dir, save_file
from src._road.jaar_config import init_change_id
from src._road.road import get_default_real_id_roadnode as root_label
from src.change.change import changeunit_shop, get_json_filename
from src.change.filehub import filehub_shop
from src.change.examples.example_change_atoms import get_atom_example_ideaunit_knee
from src.change.examples.example_change_changes import (
    get_sue_changeunit,
    sue_1atomunits_changeunit,
    sue_2atomunits_changeunit,
    sue_3atomunits_changeunit,
    sue_4atomunits_changeunit,
)
from src.change.examples.change_env import (
    env_dir_setup_cleanup,
    get_change_temp_env_dir as env_dir,
)


def test_FileHub_default_duty_agenda_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    slash_text = "/"
    point_five_float = 0.5
    sue_filehub = filehub_shop(
        env_dir(),
        root_label(),
        sue_text,
        econ_road=None,
        nox_type=None,
        road_delimiter=slash_text,
        planck=point_five_float,
    )

    # WHEN
    sue_default_duty = sue_filehub.default_duty_agenda()

    # THEN
    assert sue_default_duty._real_id == sue_filehub.real_id
    assert sue_default_duty._owner_id == sue_filehub.person_id
    assert sue_default_duty._road_delimiter == sue_filehub.road_delimiter
    assert sue_default_duty._planck == sue_filehub.planck


def test_FileHub_get_duty_agenda_IfFileMissingCreatesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)

    delete_dir(sue_filehub.real_dir())
    assert sue_filehub.duty_file_exists() is False

    # WHEN
    sue_duty = sue_filehub.get_duty_agenda()

    # THEN
    assert sue_filehub.duty_file_exists()
    default_duty = sue_filehub.default_duty_agenda()
    assert sue_duty.get_dict() == default_duty.get_dict()


def test_FileHub_delete_duty_file_DeletesDutyFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), root_label(), sue_text)
    sue_duty = sue_filehub.get_duty_agenda()
    assert sue_filehub.duty_file_exists()

    # WHEN
    sue_filehub.delete_duty_file()

    # THEN
    assert sue_filehub.duty_file_exists() == False
