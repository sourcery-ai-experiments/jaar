from src.system.person import personunit_shop
import src.system.examples.example_persons as example_persons
from src.system.examples.person_env_kit import (
    person_dir_setup_cleanup,
    get_temp_person_dir,
    create_calendar_file_for_person,
)
from src.system.examples.env_kit import get_temp_env_name
from src.system.system import SystemUnit
from os import path as os_path, scandir as os_scandir
from pytest import raises as pytest_raises
from src.calendar.x_func import (
    count_files as x_func_count_files,
    dir_files as x_func_dir_files,
)


def test_person_save_calendar_to_depot_assignment_link_CorrectlyCreatesAssignmentFile():
    pass
