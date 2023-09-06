# from os import listdir as os_listdir
from pytest import fixture as pytest_fixture
from src.calendar.calendar import CalendarUnit
from src.calendar.x_func import delete_dir, save_file as x_func_save_file


def get_temp_person_dir():
    return "src/system/examples/ex_env"


@pytest_fixture()
def person_dir_setup_cleanup():
    person_dir = get_temp_person_dir()
    delete_dir(dir=person_dir)
    yield person_dir
    delete_dir(dir=person_dir)


def create_calendar_file_for_person(calendar_person_dir: str, calendar_owner: str):
    calendar_x = CalendarUnit(_owner=calendar_owner)
    # file_path = f"{calendar_person_dir}/{calendar_x._owner}.json"
    # # if not path.exists(file_path):
    # print(f"{file_path=} {calendar_x._owner=}")
    # with open(f"{file_path}", "w") as f:
    #     print(f" saving {calendar_x._owner=} to {file_path=}")
    #     f.write(calendar_x.get_json())
    x_func_save_file(
        dest_dir=calendar_person_dir,
        file_name=f"{calendar_x._owner}.json",
        file_text=calendar_x.get_json(),
    )
    # print(f"print all {calendar_dir=} {os_listdir(path=calendar_dir)}")
    # for file_path_y in os_listdir(path=calendar_dir):
    #     print(f"{file_path_y}")
