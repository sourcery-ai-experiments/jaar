from src._instrument.file import open_file, dir_files, delete_dir, set_dir, save_file
from src._road.jaar_config import init_change_id
from src._road.road import get_default_real_id_roadnode as root_label
from src.change.change import changeunit_shop, get_json_filename
from src.change.filehub import filehub_shop
from src.change.examples.example_atoms import get_atom_example_ideaunit_knee
from src.change.examples.example_changes import (
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
