from src._instrument.file import dir_files as file_dir_files
from src.listen.userhub import userhub_shop
from src.listen.examples.example_listen_quarks import (
    get_quark_example_factunit_knee,
    get_quark_example_ideaunit_sports,
    get_quark_example_ideaunit_ball,
    get_quark_example_ideaunit_knee,
)
from src.listen.examples.listen_env import (
    get_listen_temp_env_dir as reals_dir,
    get_default_real_id_roadnode as real_id,
    env_dir_setup_cleanup,
)
from os.path import exists as os_path_exists


def test_UserHub_quark_file_name_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(reals_dir(), real_id(), yao_text)
    one_int = 1

    # WHEN
    one_quark_file_name = yao_userhub.quark_file_name(one_int)

    # THEN
    assert one_quark_file_name == f"{one_int}.json"


def test_UserHub_quark_file_path_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(reals_dir(), real_id(), yao_text)
    one_int = 1

    # WHEN
    one_quark_file_path = yao_userhub.quark_file_path(one_int)

    # THEN
    one_quark_file_name = yao_userhub.quark_file_name(one_int)
    assert one_quark_file_path == f"{yao_userhub.quarks_dir()}/{one_quark_file_name}"


def test_UserHub_save_valid_quark_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(reals_dir(), real_id(), yao_text)
    one_int = 1
    assert os_path_exists(yao_userhub.quark_file_path(one_int)) is False

    # WHEN
    knee_quark = get_quark_example_factunit_knee()
    quark_num = yao_userhub._save_valid_quark_file(knee_quark, one_int)

    # THEN
    assert os_path_exists(yao_userhub.quark_file_path(one_int))
    assert quark_num == one_int


def test_UserHub_quark_file_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(reals_dir(), real_id(), yao_text)
    five_int = 5
    assert os_path_exists(yao_userhub.quark_file_path(five_int)) is False
    assert yao_userhub.quark_file_exists(five_int) is False

    # WHEN
    yao_userhub._save_valid_quark_file(get_quark_example_factunit_knee(), five_int)

    # THEN
    assert os_path_exists(yao_userhub.quark_file_path(five_int))
    assert yao_userhub.quark_file_exists(five_int)


def test_UserHub_delete_quark_file_CorrectlyDeletesFile(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    yao_userhub._save_valid_quark_file(get_quark_example_factunit_knee(), ten_int)
    assert yao_userhub.quark_file_exists(ten_int)

    # WHEN
    yao_userhub.delete_quark_file(ten_int)

    # THEN
    assert yao_userhub.quark_file_exists(ten_int) is False


def test_UserHub_get_max_quark_file_number_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    yao_userhub._save_valid_quark_file(get_quark_example_factunit_knee(), ten_int)
    assert yao_userhub.quark_file_exists(ten_int)

    # WHEN / THEN
    assert yao_userhub.get_max_quark_file_number() == ten_int


def test_UserHub_get_max_quark_file_number_ReturnsCorrectObjWhenDirIsEmpty(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(reals_dir(), real_id(), yao_text)

    # WHEN / THEN
    assert yao_userhub.get_max_quark_file_number() is None


def test_UserHub_get_next_quark_file_number_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(reals_dir(), real_id(), yao_text)
    # WHEN / THEN
    assert yao_userhub._get_next_quark_file_number() == 0

    ten_int = 10
    yao_userhub._save_valid_quark_file(get_quark_example_factunit_knee(), ten_int)
    assert yao_userhub.quark_file_exists(ten_int)

    # WHEN / THEN
    assert yao_userhub._get_next_quark_file_number() == 11


def test_UserHub_save_quark_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(reals_dir(), real_id(), yao_text)
    ten_int = 10
    yao_userhub._save_valid_quark_file(get_quark_example_factunit_knee(), ten_int)
    assert yao_userhub.get_max_quark_file_number() == ten_int
    eleven_int = ten_int + 1
    assert yao_userhub.quark_file_exists(eleven_int) is False

    # WHEN
    quark_num1 = yao_userhub.save_quark_file(get_quark_example_factunit_knee())

    # THEN
    assert yao_userhub.get_max_quark_file_number() != ten_int
    assert yao_userhub.get_max_quark_file_number() == eleven_int
    assert yao_userhub.quark_file_exists(eleven_int)
    assert quark_num1 == eleven_int
    quark_num2 = yao_userhub.save_quark_file(get_quark_example_factunit_knee())
    assert quark_num2 == 12


def test_UserHub_get_world_from_quark_files_ReturnsFileWithZeroQuarks(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(reals_dir(), real_id(), yao_text)

    # WHEN
    yao_world = yao_userhub._get_world_from_quark_files()

    # THEN
    assert yao_world._owner_id == yao_text
    assert yao_world._real_id == yao_userhub.real_id
    assert yao_world._road_delimiter == yao_userhub.road_delimiter
    assert yao_world._pixel == yao_userhub.pixel


def test_UserHub_get_world_from_quark_files_ReturnsCorrectFile_SimpleIdea(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(reals_dir(), real_id(), yao_text)

    # save quark files
    sports_quark = get_quark_example_ideaunit_sports(yao_userhub.real_id)
    yao_userhub.save_quark_file(sports_quark)

    # WHEN
    yao_world = yao_userhub._get_world_from_quark_files()

    # THEN
    assert yao_world._owner_id == yao_text
    assert yao_world._real_id == yao_userhub.real_id
    assert yao_world._road_delimiter == yao_userhub.road_delimiter
    sports_text = "sports"
    sports_road = yao_world.make_l1_road(sports_text)

    assert yao_world.idea_exists(sports_road)


def test_UserHub_get_world_from_quark_files_ReturnsCorrectFile_WithFactUnit(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(reals_dir(), real_id(), yao_text)

    # save quark files
    x_real_id = yao_userhub.real_id
    yao_userhub.save_quark_file(get_quark_example_ideaunit_sports(x_real_id))
    yao_userhub.save_quark_file(get_quark_example_ideaunit_ball(x_real_id))
    yao_userhub.save_quark_file(get_quark_example_ideaunit_knee(x_real_id))
    yao_userhub.save_quark_file(get_quark_example_factunit_knee(x_real_id))
    print(f"{file_dir_files(yao_userhub.quarks_dir()).keys()=}")

    # WHEN
    yao_world = yao_userhub._get_world_from_quark_files()

    # THEN
    assert yao_world._owner_id == yao_text
    assert yao_world._real_id == yao_userhub.real_id
    assert yao_world._road_delimiter == yao_userhub.road_delimiter
    sports_text = "sports"
    sports_road = yao_world.make_l1_road(sports_text)

    assert yao_world.idea_exists(sports_road)
