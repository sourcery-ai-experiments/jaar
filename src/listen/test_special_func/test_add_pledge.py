from src._road.road import get_default_real_id_roadnode as root_label
from src.listen.userhub import userhub_shop
from src.listen.special_func import add_duty_pledge
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
    assert old_sue_duty.idea_exists(clean_road) is False

    # WHEN
    add_duty_pledge(sue_userhub, clean_road)

    # THEN
    assert sue_userhub.atom_file_exists(one_int)
    new_sue_duty = sue_userhub.get_duty_agenda()
    assert new_sue_duty.idea_exists(clean_road)


def test_add_duty_pledge_SetsDutyAgendapledgeIdea_suffgroup(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_userhub = userhub_shop(env_dir(), root_label(), sue_text)
    sue_userhub.initialize_atom_duty_files()
    old_sue_duty = sue_userhub.get_duty_agenda()
    clean_text = "clean"
    clean_road = old_sue_duty.make_l1_road(clean_text)
    assert old_sue_duty.idea_exists(clean_road) is False

    # WHEN
    bob_text = "Bob"
    add_duty_pledge(sue_userhub, clean_road, x_suffgroup=bob_text)

    # THEN
    new_sue_duty = sue_userhub.get_duty_agenda()
    assert new_sue_duty.idea_exists(clean_road)
    clean_idea = new_sue_duty.get_idea_obj(clean_road)
    print(f"{clean_idea._assignedunit._suffgroups=}")
    assert clean_idea._assignedunit.suffgroup_exists(bob_text)


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
    assert old_sue_duty.idea_exists(clean_road) is False

    # WHEN
    add_duty_pledge(sue_userhub, clean_road, reason_premise=dirty_road)

    # THEN
    new_sue_duty = sue_userhub.get_duty_agenda()
    clean_idea = new_sue_duty.get_idea_obj(clean_road)
    print(f"{clean_idea._reasonunits.keys()=}")
    assert clean_idea.get_reasonunit(house_estimation_road) != None
    house_reasonunit = clean_idea.get_reasonunit(house_estimation_road)
    assert house_reasonunit.get_premise(dirty_road) != None
