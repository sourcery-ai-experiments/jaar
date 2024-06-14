from src._road.road import get_default_real_id_roadnode as root_label
from src.listen.userhub import userhub_shop
from src.listen.special_func import add_duty_pledge, add_duty_belief
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)


def test_add_duty_pledge_Addspledgeatom(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text)
    sue_userhub.initialize_atom_duty_files()
    old_sue_duty = sue_userhub.get_duty_agenda()
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    one_int = 1
    print(f"{sue_userhub.atom_file_path(one_int)=}")
    assert sue_userhub.atom_file_exists(one_int) is False
    old_sue_duty = sue_userhub.get_duty_agenda()
    assert old_sue_duty.fact_exists(clean_road) is False

    # WHEN
    add_duty_pledge(sue_userhub, clean_road)

    # THEN
    assert sue_userhub.atom_file_exists(one_int)
    new_sue_duty = sue_userhub.get_duty_agenda()
    assert new_sue_duty.fact_exists(clean_road)


def test_add_duty_pledge_SetsDutyAgendapledgeFact_suffidea(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text)
    sue_userhub.initialize_atom_duty_files()
    old_sue_duty = sue_userhub.get_duty_agenda()
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    assert old_sue_duty.fact_exists(clean_road) is False

    # WHEN
    bob_text = "Bob"
    add_duty_pledge(sue_userhub, clean_road, x_suffidea=bob_text)

    # THEN
    new_sue_duty = sue_userhub.get_duty_agenda()
    assert new_sue_duty.fact_exists(clean_road)
    clean_fact = new_sue_duty.get_fact_obj(clean_road)
    print(f"{clean_fact._assignedunit._suffideas=}")
    assert clean_fact._assignedunit.suffidea_exists(bob_text)


def test_add_duty_pledge_CanAdd_reasonunit(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text)
    sue_userhub.initialize_atom_duty_files()
    old_sue_duty = sue_userhub.get_duty_agenda()
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    house_estimation_text = "house_estimation"
    house_estimation_road = old_sue_duty.make_l1_road(house_estimation_text)
    dirty_text = "dirty"
    dirty_road = old_sue_duty.make_road(house_estimation_road, dirty_text)
    assert old_sue_duty.fact_exists(dirty_road) is False

    # WHEN
    add_duty_pledge(sue_userhub, clean_road, reason_premise=dirty_road)

    # THEN
    new_sue_duty = sue_userhub.get_duty_agenda()
    clean_fact = new_sue_duty.get_fact_obj(clean_road)
    print(f"{clean_fact._reasonunits.keys()=}")
    assert clean_fact.get_reasonunit(house_estimation_road) != None
    house_reasonunit = clean_fact.get_reasonunit(house_estimation_road)
    assert house_reasonunit.get_premise(dirty_road) != None


def test_add_duty_belief_CanAdd_beliefunit(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text)
    sue_userhub.initialize_atom_duty_files()
    old_sue_duty = sue_userhub.get_duty_agenda()
    house_estimation_text = "house_estimation"
    house_estimation_road = old_sue_duty.make_l1_road(house_estimation_text)
    dirty_text = "dirty"
    dirty_road = old_sue_duty.make_road(house_estimation_road, dirty_text)
    assert old_sue_duty.fact_exists(dirty_road) is False
    assert old_sue_duty.get_belief(dirty_road) is None

    # WHEN
    add_duty_belief(sue_userhub, dirty_road)

    # THEN
    new_sue_duty = sue_userhub.get_duty_agenda()
    assert new_sue_duty.fact_exists(dirty_road)
    assert new_sue_duty.get_belief(house_estimation_road) != None
    assert new_sue_duty.get_belief(house_estimation_road).pick == dirty_road
