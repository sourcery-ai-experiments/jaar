from src._road.road import get_default_real_id_roadnode as root_label
from src.listen.hubunit import hubunit_shop
from src.listen.special_func import add_mind_pledge, add_mind_fact
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)


def test_add_mind_pledge_Addspledgegift(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_label(), sue_text)
    sue_hubunit.initialize_gift_mind_files()
    old_sue_mind = sue_hubunit.get_mind_world()
    clean_text = "clean"
    clean_road = old_sue_mind.make_l1_road(clean_text)
    one_int = 1
    print(f"{sue_hubunit.gift_file_path(one_int)=}")
    assert sue_hubunit.gift_file_exists(one_int) is False
    old_sue_mind = sue_hubunit.get_mind_world()
    assert old_sue_mind.idea_exists(clean_road) is False

    # WHEN
    add_mind_pledge(sue_hubunit, clean_road)

    # THEN
    assert sue_hubunit.gift_file_exists(one_int)
    new_sue_mind = sue_hubunit.get_mind_world()
    assert new_sue_mind.idea_exists(clean_road)


def test_add_mind_pledge_SetsmindWorldpledgeIdea_heldbelief(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_label(), sue_text)
    sue_hubunit.initialize_gift_mind_files()
    old_sue_mind = sue_hubunit.get_mind_world()
    clean_text = "clean"
    clean_road = old_sue_mind.make_l1_road(clean_text)
    assert old_sue_mind.idea_exists(clean_road) is False

    # WHEN
    bob_text = "Bob"
    add_mind_pledge(sue_hubunit, clean_road, x_heldbelief=bob_text)

    # THEN
    new_sue_mind = sue_hubunit.get_mind_world()
    assert new_sue_mind.idea_exists(clean_road)
    clean_idea = new_sue_mind.get_idea_obj(clean_road)
    print(f"{clean_idea._cultureunit._heldbeliefs=}")
    assert clean_idea._cultureunit.heldbelief_exists(bob_text)


def test_add_mind_pledge_CanAdd_reasonunit(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_label(), sue_text)
    sue_hubunit.initialize_gift_mind_files()
    old_sue_mind = sue_hubunit.get_mind_world()
    clean_text = "clean"
    clean_road = old_sue_mind.make_l1_road(clean_text)
    house_estimation_text = "house_estimation"
    house_estimation_road = old_sue_mind.make_l1_road(house_estimation_text)
    dirty_text = "dirty"
    dirty_road = old_sue_mind.make_road(house_estimation_road, dirty_text)
    assert old_sue_mind.idea_exists(dirty_road) is False

    # WHEN
    add_mind_pledge(sue_hubunit, clean_road, reason_premise=dirty_road)

    # THEN
    new_sue_mind = sue_hubunit.get_mind_world()
    clean_idea = new_sue_mind.get_idea_obj(clean_road)
    print(f"{clean_idea._reasonunits.keys()=}")
    assert clean_idea.get_reasonunit(house_estimation_road) != None
    house_reasonunit = clean_idea.get_reasonunit(house_estimation_road)
    assert house_reasonunit.get_premise(dirty_road) != None


def test_add_mind_fact_CanAdd_factunit(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_hubunit = hubunit_shop(env_dir(), root_label(), sue_text)
    sue_hubunit.initialize_gift_mind_files()
    old_sue_mind = sue_hubunit.get_mind_world()
    house_estimation_text = "house_estimation"
    house_estimation_road = old_sue_mind.make_l1_road(house_estimation_text)
    dirty_text = "dirty"
    dirty_road = old_sue_mind.make_road(house_estimation_road, dirty_text)
    assert old_sue_mind.idea_exists(dirty_road) is False
    assert old_sue_mind.get_fact(dirty_road) is None

    # WHEN
    add_mind_fact(sue_hubunit, dirty_road)

    # THEN
    new_sue_mind = sue_hubunit.get_mind_world()
    assert new_sue_mind.idea_exists(dirty_road)
    assert new_sue_mind.get_fact(house_estimation_road) != None
    assert new_sue_mind.get_fact(house_estimation_road).pick == dirty_road
