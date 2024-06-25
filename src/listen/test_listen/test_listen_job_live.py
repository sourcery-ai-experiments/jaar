from src._road.road import RoadUnit, create_road, get_default_real_id_roadnode, RoadNode
from src._world.idea import ideaunit_shop
from src._world.world import WorldUnit, worldunit_shop
from src.listen.userhub import userhub_shop, UserHub
from src.listen.listen import listen_to_person_jobs, create_job_file_from_role_file
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
    get_texas_userhub,
)


def casa_text() -> str:
    return "casa"


def cook_text() -> str:
    return "cook"


def eat_text() -> str:
    return "eat"


def hungry_text() -> str:
    return "hungry"


def full_text() -> str:
    return "full"


def sanitation_text():
    return "sanitation"


def clean_text():
    return "clean"


def dirty_text():
    return "dirty"


def sweep_text():
    return "sweep"


def run_text():
    return "run"


def casa_road() -> RoadUnit:
    return create_road(get_default_real_id_roadnode(), casa_text())


def cook_road() -> RoadUnit:
    return create_road(casa_road(), cook_text())


def eat_road() -> RoadUnit:
    return create_road(casa_road(), eat_text())


def hungry_road() -> RoadUnit:
    return create_road(eat_road(), hungry_text())


def full_road() -> RoadUnit:
    return create_road(eat_road(), full_text())


def sanitation_road() -> RoadUnit:
    return create_road(casa_road(), sanitation_text())


def clean_road() -> RoadUnit:
    return create_road(sanitation_road(), clean_text())


def dirty_road() -> RoadUnit:
    return create_road(sanitation_road(), dirty_text())


def sweep_road() -> RoadUnit:
    return create_road(casa_road(), sweep_text())


def run_road() -> RoadUnit:
    return create_road(casa_road(), run_text())


def get_example_yao_world() -> WorldUnit:
    yao_text = "Yao"
    zia_text = "Zia"
    bob_text = "Bob"
    yao_speaker = worldunit_shop(yao_text, get_default_real_id_roadnode())
    yao_speaker.add_idea(ideaunit_shop(run_text()), casa_road())
    yao_speaker.add_otherunit(yao_text, debtor_weight=10)
    yao_speaker.add_otherunit(zia_text, debtor_weight=30)
    yao_speaker.add_otherunit(bob_text, debtor_weight=40)
    yao_speaker.set_other_pool(80)
    return yao_speaker


def get_example_yao_job1_speaker() -> WorldUnit:
    yao_text = "Yao"
    yao_speaker = get_example_yao_world()
    yao_speaker.del_idea_obj(run_road())
    yao_speaker.set_other_pool(40)
    yao_speaker.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    yao_speaker.add_idea(ideaunit_shop(hungry_text()), eat_road())
    yao_speaker.add_idea(ideaunit_shop(full_text()), eat_road())
    cook_ideaunit = yao_speaker.get_idea_obj(cook_road())
    cook_ideaunit._assignedunit.set_suffbelief(yao_text)
    yao_speaker.edit_reason(cook_road(), eat_road(), hungry_road())
    yao_speaker.set_fact(eat_road(), hungry_road())
    return yao_speaker


def get_example_yao_job2_speaker() -> WorldUnit:
    yao_text = "Yao"
    yao_speaker = get_example_yao_world()
    yao_speaker.del_idea_obj(run_road())
    yao_speaker.set_other_pool(30)
    yao_speaker.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    yao_speaker.add_idea(ideaunit_shop(hungry_text()), eat_road())
    yao_speaker.add_idea(ideaunit_shop(full_text()), eat_road())
    cook_ideaunit = yao_speaker.get_idea_obj(cook_road())
    cook_ideaunit._assignedunit.set_suffbelief(yao_text)
    yao_speaker.edit_reason(cook_road(), eat_road(), hungry_road())
    yao_speaker.set_fact(eat_road(), hungry_road())

    yao_speaker.add_idea(ideaunit_shop(sweep_text(), pledge=True), casa_road())
    yao_speaker.add_idea(ideaunit_shop(dirty_text()), sanitation_road())
    yao_speaker.add_idea(ideaunit_shop(clean_text()), sanitation_road())
    yao_speaker.edit_reason(sweep_road(), sanitation_road(), dirty_road())
    yao_speaker.set_fact(sweep_road(), dirty_road())
    return yao_speaker


def get_example_yao_job3_speaker() -> WorldUnit:
    yao_speaker = get_example_yao_world()
    yao_speaker.del_idea_obj(run_road())
    yao_speaker.set_other_pool(10)
    yao_speaker.add_idea(ideaunit_shop(sweep_text(), pledge=True), casa_road())
    yao_speaker.add_idea(ideaunit_shop(dirty_text()), sanitation_road())
    yao_speaker.add_idea(ideaunit_shop(clean_text()), sanitation_road())
    yao_speaker.edit_reason(sweep_road(), sanitation_road(), dirty_road())
    yao_speaker.set_fact(sweep_road(), dirty_road())
    return yao_speaker


def get_usa_road() -> RoadUnit:
    return create_road(get_default_real_id_roadnode(), "USA")


def get_iowa_text() -> RoadNode:
    return "Iowa"


def get_ohio_text() -> RoadNode:
    return "Ohio"


def get_utah_text() -> RoadNode:
    return "Utah"


def get_swim_text() -> RoadNode:
    return "swim"


def get_location_text() -> RoadNode:
    return "location"


def get_in_ocean_text() -> RoadNode:
    return "in_ocean"


def get_on_land_text() -> RoadNode:
    return "on_land"


def get_iowa_road() -> RoadUnit:
    return create_road(get_usa_road(), get_iowa_text())


def get_ohio_road() -> RoadUnit:
    return create_road(get_usa_road(), get_ohio_text())


def get_utah_road() -> RoadUnit:
    return create_road(get_usa_road(), get_utah_text())


def get_swim_road() -> RoadUnit:
    return create_road(get_default_real_id_roadnode(), get_swim_text())


def get_location_road() -> RoadUnit:
    return create_road(get_default_real_id_roadnode(), get_location_text())


def get_in_ocean_road() -> RoadUnit:
    return create_road(get_location_road(), get_in_ocean_text())


def get_on_land_road() -> RoadUnit:
    return create_road(get_location_road(), get_on_land_text())


def get_yao_ohio_userhub() -> UserHub:
    yao_world = get_example_yao_world()
    return userhub_shop(
        reals_dir=env_dir(),
        real_id=yao_world._real_id,
        person_id=yao_world._owner_id,
        econ_road=get_ohio_road(),
        # pipeline_same_live_text(),
    )


def get_yao_iowa_userhub() -> UserHub:
    yao_world = get_example_yao_world()
    return userhub_shop(
        reals_dir=env_dir(),
        real_id=yao_world._real_id,
        person_id=yao_world._owner_id,
        econ_road=get_iowa_road(),
        # pipeline_same_live_text(),
    )


def get_zia_utah_userhub() -> UserHub:
    yao_world = get_example_yao_world()
    return userhub_shop(
        reals_dir=env_dir(),
        real_id=yao_world._real_id,
        person_id="Zia",
        econ_road=get_utah_road(),
        # pipeline_same_live_text(),
    )


def get_example_yao_same_with_3_healers():
    yao_same = get_example_yao_world()
    yao_text = yao_same.get_other("Yao").other_id
    bob_text = yao_same.get_other("Bob").other_id
    zia_text = yao_same.get_other("Zia").other_id
    iowa_idea = ideaunit_shop(get_iowa_text(), _problem_bool=True)
    ohio_idea = ideaunit_shop(get_ohio_text(), _problem_bool=True)
    utah_idea = ideaunit_shop(get_utah_text(), _problem_bool=True)
    iowa_idea._healerhold.set_belief_id(get_yao_iowa_userhub().person_id)
    ohio_idea._healerhold.set_belief_id(get_yao_ohio_userhub().person_id)
    utah_idea._healerhold.set_belief_id(get_zia_utah_userhub().person_id)
    yao_same.add_idea(iowa_idea, get_usa_road())
    yao_same.add_idea(ohio_idea, get_usa_road())
    yao_same.add_idea(utah_idea, get_usa_road())

    return yao_same


def test_listen_to_person_jobs_Pipeline_Scenario0(env_dir_setup_cleanup):
    # GIVEN
    # yao0_same with 3 debotors of different credor_weights
    # yao_job1 with 1 task, fact that doesn't want that task
    # yao_job2 with 2 tasks, one is equal fact wants task
    # yao_job3 with 1 new task, fact stays with it

    yao_same0 = get_example_yao_same_with_3_healers()
    yao_same0.del_idea_obj(run_road())
    yao_same0.add_l1_idea(ideaunit_shop(get_location_text()))
    yao_same0.add_idea(ideaunit_shop(get_in_ocean_text()), get_location_road())
    yao_same0.add_idea(ideaunit_shop(get_on_land_text()), get_location_road())
    yao_same0.add_l1_idea(ideaunit_shop(get_swim_text(), pledge=True))
    yao_same0.edit_reason(get_swim_road(), get_location_road(), get_in_ocean_road())
    yao_same0.calc_world_metrics()
    assert yao_same0._econ_dict.get(get_iowa_road())
    assert yao_same0._econ_dict.get(get_ohio_road())
    assert yao_same0._econ_dict.get(get_utah_road())
    assert len(yao_same0._econ_dict) == 3
    print(f"{yao_same0._idea_dict.keys()=}")

    yao_text = yao_same0._owner_id
    yao_job1 = get_example_yao_job1_speaker()
    yao_job2 = get_example_yao_job2_speaker()
    yao_job3 = get_example_yao_job3_speaker()
    yao_iowa_userhub = get_yao_iowa_userhub()
    yao_ohio_userhub = get_yao_ohio_userhub()
    zia_utah_userhub = get_zia_utah_userhub()
    # delete_dir(yao_iowa_userhub.persons_dir())
    assert yao_iowa_userhub.same_file_exists() is False
    assert yao_iowa_userhub.live_file_exists() is False
    assert yao_iowa_userhub.job_file_exists(yao_text) is False
    assert yao_ohio_userhub.job_file_exists(yao_text) is False
    assert zia_utah_userhub.job_file_exists(yao_text) is False
    yao_iowa_userhub.save_same_world(yao_same0)
    yao_iowa_userhub.save_job_world(yao_job1)
    yao_ohio_userhub.save_job_world(yao_job2)
    zia_utah_userhub.save_job_world(yao_job3)
    assert yao_iowa_userhub.same_file_exists()
    assert yao_iowa_userhub.job_file_exists(yao_text)
    assert yao_ohio_userhub.job_file_exists(yao_text)
    assert zia_utah_userhub.job_file_exists(yao_text)

    # WHEN
    assert yao_iowa_userhub.live_file_exists() is False
    listen_to_person_jobs(yao_iowa_userhub)
    assert yao_iowa_userhub.live_file_exists()

    yao_live = yao_iowa_userhub.get_live_world()
    yao_live.calc_world_metrics()
    assert yao_live._others.keys() == yao_same0._others.keys()
    assert yao_live.get_other(yao_text)._irrational_debtor_weight == 0
    assert yao_live.get_beliefunits_dict() == yao_same0.get_beliefunits_dict()
    assert len(yao_live._idea_dict) == 10
    print(f"{yao_live._idea_dict.keys()=}")
    print(f"{yao_live.get_factunits_dict().keys()=}")
    assert yao_live.idea_exists(cook_road())
    assert yao_live.idea_exists(clean_road())
    assert yao_live.idea_exists(run_road()) is False
    assert len(yao_live._idearoot._factunits) == 2
    assert yao_live != yao_same0


def test_listen_to_person_jobs_Pipeline_Scenario1_yao_same_CanOnlyReferenceItself(
    env_dir_setup_cleanup,
):
    # GIVEN
    # yao0_same with 3 debotors of different credor_weights
    # yao_job1 with 1 task, fact that doesn't want that task
    # yao_job2 with 2 tasks, one is equal fact wants task
    # yao_job3 with 1 new task, fact stays with it

    yao_same0 = get_example_yao_same_with_3_healers()
    yao_same0.add_l1_idea(ideaunit_shop(get_location_text()))
    yao_same0.add_idea(ideaunit_shop(get_in_ocean_text()), get_location_road())
    yao_same0.add_idea(ideaunit_shop(get_on_land_text()), get_location_road())
    yao_same0.add_l1_idea(ideaunit_shop(get_swim_text(), pledge=True))
    yao_same0.edit_reason(get_swim_road(), get_location_road(), get_in_ocean_road())
    yao_same0.set_fact(get_location_road(), get_in_ocean_road())
    print(f"{yao_same0.get_fact(get_location_road())=}")
    yao_same0.del_idea_obj(run_road())
    assert yao_same0._econ_dict.get(get_iowa_road())
    assert yao_same0._econ_dict.get(get_ohio_road())
    assert yao_same0._econ_dict.get(get_utah_road())
    yao_same0.calc_world_metrics()
    assert len(yao_same0._econ_dict) == 3
    # print(f"{yao_same0._idea_dict.keys()=}")

    yao_text = yao_same0._owner_id
    yao_job1 = get_example_yao_job1_speaker()
    yao_job2 = get_example_yao_job2_speaker()
    yao_job3 = get_example_yao_job3_speaker()
    yao_iowa_userhub = get_yao_iowa_userhub()
    yao_ohio_userhub = get_yao_ohio_userhub()
    zia_utah_userhub = get_zia_utah_userhub()
    # delete_dir(yao_iowa_userhub.persons_dir())
    assert yao_iowa_userhub.same_file_exists() is False
    assert yao_iowa_userhub.live_file_exists() is False
    assert yao_iowa_userhub.job_file_exists(yao_text) is False
    assert yao_ohio_userhub.job_file_exists(yao_text) is False
    assert zia_utah_userhub.job_file_exists(yao_text) is False
    print(f"{yao_same0.get_fact(get_location_road())=}")
    yao_iowa_userhub.save_same_world(yao_same0)
    # yao_iowa_userhub.save_job_world(yao_job1)
    # yao_ohio_userhub.save_job_world(yao_job2)
    # zia_utah_userhub.save_job_world(yao_job3)
    assert yao_iowa_userhub.same_file_exists()
    assert yao_iowa_userhub.job_file_exists(yao_text) is False
    assert yao_ohio_userhub.job_file_exists(yao_text) is False
    assert zia_utah_userhub.job_file_exists(yao_text) is False

    # WHEN
    assert yao_iowa_userhub.live_file_exists() is False
    listen_to_person_jobs(yao_iowa_userhub)
    assert yao_iowa_userhub.live_file_exists()

    yao_live = yao_iowa_userhub.get_live_world()
    yao_live.calc_world_metrics()
    assert yao_live._others.keys() == yao_same0._others.keys()
    assert yao_live.get_other(yao_text)._irrational_debtor_weight == 0
    assert yao_live.get_beliefunits_dict() == yao_same0.get_beliefunits_dict()
    assert len(yao_live._idea_dict) == 4
    print(f"{yao_live._idea_dict.keys()=}")
    print(f"{yao_live.get_factunits_dict().keys()=}")
    assert yao_live.idea_exists(cook_road()) is False
    assert yao_live.idea_exists(clean_road()) is False
    assert yao_live.idea_exists(run_road()) is False
    assert yao_live.idea_exists(get_swim_road())
    assert yao_live.idea_exists(get_in_ocean_road())
    assert yao_live.idea_exists(get_on_land_road()) is False
    assert yao_live.get_fact(get_location_road()) != None
    assert yao_live.get_fact(get_location_road()).pick == get_in_ocean_road()
    assert len(yao_live.get_agenda_dict()) == 1
    assert len(yao_live._idearoot._factunits) == 1
    assert yao_live != yao_same0


def test_create_job_file_from_role_file_CreatesEmptyJob(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_role = worldunit_shop(yao_text)
    sue_texas_userhub = get_texas_userhub()
    sue_texas_userhub.save_role_world(yao_role)
    assert sue_texas_userhub.job_file_exists(yao_text) is False

    # WHEN
    create_job_file_from_role_file(sue_texas_userhub, yao_text)

    # GIVEN
    assert sue_texas_userhub.job_file_exists(yao_text)
    yao_job = sue_texas_userhub.get_job_world(yao_text)
    assert yao_job._owner_id != None
    assert yao_job._owner_id == yao_text
    assert yao_job.get_dict() == yao_role.get_dict()
