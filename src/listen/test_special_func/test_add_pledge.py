from src._road.road import get_default_real_id_roadnode as root_label
from src.listen.userhub import userhub_shop
from src.listen.special_func import add_same_pledge, add_same_fact
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)


def test_add_same_pledge_Addspledgeatom(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text)
    sue_userhub.initialize_atom_same_files()
    old_sue_same = sue_userhub.get_same_world()
    clean_text = "clean"
    clean_road = old_sue_same.make_l1_road(clean_text)
    one_int = 1
    print(f"{sue_userhub.atom_file_path(one_int)=}")
    assert sue_userhub.atom_file_exists(one_int) is False
    old_sue_same = sue_userhub.get_same_world()
    assert old_sue_same.idea_exists(clean_road) is False

    # WHEN
    add_same_pledge(sue_userhub, clean_road)

    # THEN
    assert sue_userhub.atom_file_exists(one_int)
    new_sue_same = sue_userhub.get_same_world()
    assert new_sue_same.idea_exists(clean_road)


def test_add_same_pledge_SetsSameWorldpledgeIdea_suffbelief(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text)
    sue_userhub.initialize_atom_same_files()
    old_sue_same = sue_userhub.get_same_world()
    clean_text = "clean"
    clean_road = old_sue_same.make_l1_road(clean_text)
    assert old_sue_same.idea_exists(clean_road) is False

    # WHEN
    bob_text = "Bob"
    add_same_pledge(sue_userhub, clean_road, x_suffbelief=bob_text)

    # THEN
    new_sue_same = sue_userhub.get_same_world()
    assert new_sue_same.idea_exists(clean_road)
    clean_idea = new_sue_same.get_idea_obj(clean_road)
    print(f"{clean_idea._assignedunit._suffbeliefs=}")
    assert clean_idea._assignedunit.suffbelief_exists(bob_text)


def test_add_same_pledge_CanAdd_reasonunit(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text)
    sue_userhub.initialize_atom_same_files()
    old_sue_same = sue_userhub.get_same_world()
    clean_text = "clean"
    clean_road = old_sue_same.make_l1_road(clean_text)
    house_estimation_text = "house_estimation"
    house_estimation_road = old_sue_same.make_l1_road(house_estimation_text)
    dirty_text = "dirty"
    dirty_road = old_sue_same.make_road(house_estimation_road, dirty_text)
    assert old_sue_same.idea_exists(dirty_road) is False

    # WHEN
    add_same_pledge(sue_userhub, clean_road, reason_premise=dirty_road)

    # THEN
    new_sue_same = sue_userhub.get_same_world()
    clean_idea = new_sue_same.get_idea_obj(clean_road)
    print(f"{clean_idea._reasonunits.keys()=}")
    assert clean_idea.get_reasonunit(house_estimation_road) != None
    house_reasonunit = clean_idea.get_reasonunit(house_estimation_road)
    assert house_reasonunit.get_premise(dirty_road) != None


def test_add_same_fact_CanAdd_factunit(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text)
    sue_userhub.initialize_atom_same_files()
    old_sue_same = sue_userhub.get_same_world()
    house_estimation_text = "house_estimation"
    house_estimation_road = old_sue_same.make_l1_road(house_estimation_text)
    dirty_text = "dirty"
    dirty_road = old_sue_same.make_road(house_estimation_road, dirty_text)
    assert old_sue_same.idea_exists(dirty_road) is False
    assert old_sue_same.get_fact(dirty_road) is None

    # WHEN
    add_same_fact(sue_userhub, dirty_road)

    # THEN
    new_sue_same = sue_userhub.get_same_world()
    assert new_sue_same.idea_exists(dirty_road)
    assert new_sue_same.get_fact(house_estimation_road) != None
    assert new_sue_same.get_fact(house_estimation_road).pick == dirty_road
