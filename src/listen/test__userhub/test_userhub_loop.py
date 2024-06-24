from src._road.jaar_config import get_test_real_id as real_id
from src._road.road import create_road
from src.listen.userhub import userhub_shop
from src.listen.examples.example_listen_truths import get_truth_with_4_levels
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)


def test_UserHub_get_perspective_truth_ReturnsTruthWith_owner_idSetToUserHub_person_id():
    # GIVEN
    bob_text = "Bob"
    bob_truthunit = get_truth_with_4_levels()
    bob_truthunit.set_owner_id(bob_text)

    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)

    # WHEN
    perspective_truthunit = sue_userhub.get_perspective_truth(bob_truthunit)

    # THEN
    assert perspective_truthunit.get_dict() != bob_truthunit.get_dict()
    assert perspective_truthunit._owner_id == sue_text
    perspective_truthunit.set_owner_id(bob_text)
    assert perspective_truthunit.get_dict() == bob_truthunit.get_dict()


def test_UserHub_get_dw_perspective_truth_ReturnsTruthWith_owner_idSetToUserHub_person_id(
    env_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    bob_truthunit = get_truth_with_4_levels()
    bob_truthunit.set_owner_id(bob_text)
    bob_userhub = userhub_shop(env_dir(), real_id(), bob_text)
    bob_userhub.save_live_truth(bob_truthunit)

    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text)

    # WHEN
    perspective_truthunit = sue_userhub.get_dw_perspective_truth(bob_text)

    # THEN
    assert perspective_truthunit._owner_id == sue_text
    assert perspective_truthunit.get_dict() != bob_truthunit.get_dict()
    perspective_truthunit.set_owner_id(bob_text)
    assert perspective_truthunit.get_dict() == bob_truthunit.get_dict()


def test_UserHub_rj_perspective_truth_ReturnsTruthWith_owner_idSetToUserHub_person_id(
    env_dir_setup_cleanup,
):
    # GIVEN
    nation_text = "nation-state"
    nation_road = create_road(real_id(), nation_text)
    iowa_road = create_road(nation_road, "Iowa")

    bob_text = "Bob"
    yao_text = "Yao"
    yao_truthunit = get_truth_with_4_levels()
    yao_truthunit.set_owner_id(yao_text)

    bob_iowa_userhub = userhub_shop(env_dir(), real_id(), bob_text, iowa_road)
    bob_iowa_userhub.save_job_truth(yao_truthunit)

    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), real_id(), sue_text, iowa_road)

    # WHEN
    perspective_truthunit = sue_userhub.rj_perspective_truth(bob_text, yao_text)

    # THEN
    assert perspective_truthunit._owner_id == sue_text
    assert perspective_truthunit.get_dict() != yao_truthunit.get_dict()
    perspective_truthunit.set_owner_id(yao_text)
    assert perspective_truthunit.get_dict() == yao_truthunit.get_dict()
