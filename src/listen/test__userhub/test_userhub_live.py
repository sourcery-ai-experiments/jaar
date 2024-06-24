from src._instrument.file import open_file, save_file, delete_dir
from src._road.road import get_default_real_id_roadnode as root_label
from src._truth.truth import truthunit_shop, get_from_json as truthunit_get_from_json
from src.listen.userhub import userhub_shop
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_UserHub_live_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    assert os_path_exists(sue_userhub.live_path()) is False
    assert sue_userhub.live_file_exists() is False

    # WHEN
    save_file(
        dest_dir=sue_userhub.live_dir(),
        file_name=sue_userhub.live_file_name(),
        file_text=truthunit_shop(sue_text).get_json(),
    )

    # THEN
    assert os_path_exists(sue_userhub.live_path())
    assert sue_userhub.live_file_exists()


def test_UserHub_save_live_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    assert sue_userhub.live_file_exists() is False

    # WHEN
    sue_truth = truthunit_shop(sue_text)
    bob_text = "Bob"
    sue_truth.add_otherunit(bob_text)
    sue_userhub.save_live_truth(sue_truth)

    # THEN
    assert sue_userhub.live_file_exists()

    live_file_text = open_file(sue_userhub.live_dir(), sue_userhub.live_file_name())
    print(f"{live_file_text=}")
    live_truth = truthunit_get_from_json(live_file_text)
    assert live_truth.other_exists(bob_text)

    # # WHEN
    sue2_truth = truthunit_shop(sue_text)
    zia_text = "Zia"
    sue2_truth.add_otherunit(zia_text)
    sue_userhub.save_live_truth(sue2_truth)

    # THEN
    live_file_text = open_file(sue_userhub.live_dir(), sue_userhub.live_file_name())
    print(f"{live_file_text=}")
    live_truth = truthunit_get_from_json(live_file_text)
    assert live_truth.other_exists(zia_text)


def test_UserHub_save_live_file_RaisesErrorWhenTruth_live_id_IsWrong(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_userhub.save_live_truth(truthunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"TruthUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s live truth."
    )


def test_UserHub_initialize_live_file_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    sue_truth = truthunit_shop(sue_text, root_label())
    assert sue_userhub.live_file_exists() is False

    # WHEN
    sue_userhub.initialize_live_file(sue_truth)

    # THEN
    live_truth = sue_userhub.get_live_truth()
    assert live_truth._real_id == root_label()
    assert live_truth._owner_id == sue_text
    bob_text = "Bob"
    assert live_truth.other_exists(bob_text) is False

    # GIVEN
    sue_truth = truthunit_shop(sue_text)
    sue_truth.add_otherunit(bob_text)
    sue_userhub.save_live_truth(sue_truth)
    live_truth = sue_userhub.get_live_truth()
    assert live_truth.get_other(bob_text)

    # WHEN
    sue_userhub.initialize_live_file(sue_truth)

    # THEN
    live_truth = sue_userhub.get_live_truth()
    assert live_truth.get_other(bob_text)


def test_UserHub_initialize_live_file_CorrectlyDoesNotOverwrite(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_real_dir = f"{env_dir()}/{root_label()}"
    sue_pixel = 7
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None, pixel=sue_pixel)
    sue_truth = truthunit_shop(sue_text, root_label(), _pixel=sue_pixel)
    sue_userhub.initialize_live_file(sue_truth)
    assert sue_userhub.live_file_exists()
    delete_dir(sue_userhub.live_path())
    assert sue_userhub.live_file_exists() is False

    # WHEN
    bob_text = "Bob"
    sue_truth.add_otherunit(bob_text)
    sue_userhub.initialize_live_file(sue_truth)

    # THEN
    assert sue_userhub.live_file_exists()

    sue_real_dir = f"{env_dir()}/{root_label()}"
    sue_persons_dir = f"{sue_real_dir}/persons"
    sue_person_dir = f"{sue_persons_dir}/{sue_text}"
    sue_live_dir = f"{sue_person_dir}/live"
    sue_live_file_name = f"{sue_text}.json"
    live_file_text = open_file(dest_dir=sue_live_dir, file_name=sue_live_file_name)
    print(f"{live_file_text=}")
    live_truth = truthunit_get_from_json(live_file_text)
    assert live_truth._real_id == root_label()
    assert live_truth._owner_id == sue_text
    assert live_truth._pixel == sue_pixel


def test_UserHub_initialize_live_file_CreatesDirsAndFiles(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text, None)
    delete_dir(sue_userhub.real_dir())
    assert os_path_exists(sue_userhub.live_path()) is False

    # WHEN
    sue_truth = truthunit_shop(sue_text, root_label())
    sue_userhub.initialize_live_file(sue_truth)

    # THEN
    assert os_path_exists(sue_userhub.live_path())
