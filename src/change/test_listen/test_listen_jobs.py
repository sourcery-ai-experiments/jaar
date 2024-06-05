from src._road.road import RoadUnit, create_road, get_default_real_id_roadnode, RoadNode
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import AgendaUnit, agendaunit_shop
from src.change.agendahub import agendahub_shop, AgendaHub, pipeline_duty_work_text
from src.change.listen import listen_to_person_jobs
from src.change.examples.change_env import (
    env_dir_setup_cleanup,
    get_change_temp_env_dir,
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


def get_example_yao_agenda() -> AgendaUnit:
    yao_text = "Yao"
    zia_text = "Zia"
    bob_text = "Bob"
    yao_speaker = agendaunit_shop(yao_text, get_default_real_id_roadnode())
    yao_speaker.add_idea(ideaunit_shop(run_text()), casa_road())
    yao_speaker.add_partyunit(yao_text, debtor_weight=10)
    yao_speaker.add_partyunit(zia_text, debtor_weight=30)
    yao_speaker.add_partyunit(bob_text, debtor_weight=40)
    yao_speaker.set_party_pool(80)
    return yao_speaker


def get_example_yao_job1_speaker() -> AgendaUnit:
    yao_text = "Yao"
    yao_speaker = get_example_yao_agenda()
    yao_speaker.del_idea_obj(run_road())
    yao_speaker.set_party_pool(40)
    yao_speaker.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    yao_speaker.add_idea(ideaunit_shop(hungry_text()), eat_road())
    yao_speaker.add_idea(ideaunit_shop(full_text()), eat_road())
    cook_ideaunit = yao_speaker.get_idea_obj(cook_road())
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_speaker.edit_reason(cook_road(), eat_road(), hungry_road())
    yao_speaker.set_belief(eat_road(), hungry_road())
    return yao_speaker


def get_example_yao_job2_speaker() -> AgendaUnit:
    yao_text = "Yao"
    yao_speaker = get_example_yao_agenda()
    yao_speaker.del_idea_obj(run_road())
    yao_speaker.set_party_pool(30)
    yao_speaker.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    yao_speaker.add_idea(ideaunit_shop(hungry_text()), eat_road())
    yao_speaker.add_idea(ideaunit_shop(full_text()), eat_road())
    cook_ideaunit = yao_speaker.get_idea_obj(cook_road())
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_speaker.edit_reason(cook_road(), eat_road(), hungry_road())
    yao_speaker.set_belief(eat_road(), hungry_road())

    yao_speaker.add_idea(ideaunit_shop(sweep_text(), pledge=True), casa_road())
    yao_speaker.add_idea(ideaunit_shop(dirty_text()), sanitation_road())
    yao_speaker.add_idea(ideaunit_shop(clean_text()), sanitation_road())
    yao_speaker.edit_reason(sweep_road(), sanitation_road(), dirty_road())
    yao_speaker.set_belief(sweep_road(), dirty_road())
    return yao_speaker


def get_example_yao_job3_speaker() -> AgendaUnit:
    yao_speaker = get_example_yao_agenda()
    yao_speaker.del_idea_obj(run_road())
    yao_speaker.set_party_pool(10)
    yao_speaker.add_idea(ideaunit_shop(sweep_text(), pledge=True), casa_road())
    yao_speaker.add_idea(ideaunit_shop(dirty_text()), sanitation_road())
    yao_speaker.add_idea(ideaunit_shop(clean_text()), sanitation_road())
    yao_speaker.edit_reason(sweep_road(), sanitation_road(), dirty_road())
    yao_speaker.set_belief(sweep_road(), dirty_road())
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


def get_yao_ohio_agendahub() -> AgendaHub:
    yao_agenda = get_example_yao_agenda()
    return agendahub_shop(
        reals_dir=get_change_temp_env_dir(),
        real_id=yao_agenda._real_id,
        person_id=yao_agenda._owner_id,
        econ_road=get_ohio_road(),
        nox_type=pipeline_duty_work_text(),
    )


def get_yao_iowa_agendahub() -> AgendaHub:
    yao_agenda = get_example_yao_agenda()
    return agendahub_shop(
        reals_dir=get_change_temp_env_dir(),
        real_id=yao_agenda._real_id,
        person_id=yao_agenda._owner_id,
        econ_road=get_iowa_road(),
        nox_type=pipeline_duty_work_text(),
    )


def get_zia_utah_agendahub() -> AgendaHub:
    yao_agenda = get_example_yao_agenda()
    return agendahub_shop(
        reals_dir=get_change_temp_env_dir(),
        real_id=yao_agenda._real_id,
        person_id="Zia",
        econ_road=get_utah_road(),
        nox_type=pipeline_duty_work_text(),
    )


def get_example_yao_duty_with_3_healers():
    yao_duty = get_example_yao_agenda()
    yao_text = yao_duty.get_party("Yao").party_id
    bob_text = yao_duty.get_party("Bob").party_id
    zia_text = yao_duty.get_party("Zia").party_id
    iowa_idea = ideaunit_shop(get_iowa_text(), _problem_bool=True)
    ohio_idea = ideaunit_shop(get_ohio_text(), _problem_bool=True)
    utah_idea = ideaunit_shop(get_utah_text(), _problem_bool=True)
    iowa_idea._healerhold.set_group_id(get_yao_iowa_agendahub().person_id)
    ohio_idea._healerhold.set_group_id(get_yao_ohio_agendahub().person_id)
    utah_idea._healerhold.set_group_id(get_zia_utah_agendahub().person_id)
    yao_duty.add_idea(iowa_idea, get_usa_road())
    yao_duty.add_idea(ohio_idea, get_usa_road())
    yao_duty.add_idea(utah_idea, get_usa_road())

    return yao_duty


def test_listen_to_person_jobs_Pipeline_Scenario0(env_dir_setup_cleanup):
    # GIVEN
    # yao0_duty with 3 debotors of different creditor_weights
    # yao_job1 with 1 task, belief that doesn't want that task
    # yao_job2 with 2 tasks, one is same belief wants task
    # yao_job3 with 1 new task, belief stays with it

    yao_duty0 = get_example_yao_duty_with_3_healers()
    yao_duty0.del_idea_obj(run_road())
    yao_duty0.add_l1_idea(ideaunit_shop(get_location_text()))
    yao_duty0.add_idea(ideaunit_shop(get_in_ocean_text()), get_location_road())
    yao_duty0.add_idea(ideaunit_shop(get_on_land_text()), get_location_road())
    yao_duty0.add_l1_idea(ideaunit_shop(get_swim_text(), pledge=True))
    yao_duty0.edit_reason(get_swim_road(), get_location_road(), get_in_ocean_road())
    yao_duty0.calc_agenda_metrics()
    assert yao_duty0._econ_dict.get(get_iowa_road())
    assert yao_duty0._econ_dict.get(get_ohio_road())
    assert yao_duty0._econ_dict.get(get_utah_road())
    assert len(yao_duty0._econ_dict) == 3
    print(f"{yao_duty0._idea_dict.keys()=}")

    yao_text = yao_duty0._owner_id
    yao_job1 = get_example_yao_job1_speaker()
    yao_job2 = get_example_yao_job2_speaker()
    yao_job3 = get_example_yao_job3_speaker()
    yao_iowa_agendahub = get_yao_iowa_agendahub()
    yao_ohio_agendahub = get_yao_ohio_agendahub()
    zia_utah_agendahub = get_zia_utah_agendahub()
    # delete_dir(yao_iowa_agendahub.persons_dir())
    assert yao_iowa_agendahub.duty_file_exists() == False
    assert yao_iowa_agendahub.work_file_exists() == False
    assert yao_iowa_agendahub.job_file_exists(yao_text) == False
    assert yao_ohio_agendahub.job_file_exists(yao_text) == False
    assert zia_utah_agendahub.job_file_exists(yao_text) == False
    yao_iowa_agendahub.save_duty_agenda(yao_duty0)
    yao_iowa_agendahub.save_job_agenda(yao_job1)
    yao_ohio_agendahub.save_job_agenda(yao_job2)
    zia_utah_agendahub.save_job_agenda(yao_job3)
    assert yao_iowa_agendahub.duty_file_exists()
    assert yao_iowa_agendahub.job_file_exists(yao_text)
    assert yao_ohio_agendahub.job_file_exists(yao_text)
    assert zia_utah_agendahub.job_file_exists(yao_text)

    # WHEN
    assert yao_iowa_agendahub.work_file_exists() == False
    listen_to_person_jobs(yao_iowa_agendahub)
    assert yao_iowa_agendahub.work_file_exists()

    yao_work = yao_iowa_agendahub.get_work_agenda()
    yao_work.calc_agenda_metrics()
    assert yao_work._partys.keys() == yao_duty0._partys.keys()
    assert yao_work.get_party(yao_text)._irrational_debtor_weight == 0
    assert yao_work.get_groupunits_dict() == yao_duty0.get_groupunits_dict()
    assert len(yao_work._idea_dict) == 10
    print(f"{yao_work._idea_dict.keys()=}")
    print(f"{yao_work.get_beliefunits_dict().keys()=}")
    assert yao_work.idea_exists(cook_road())
    assert yao_work.idea_exists(clean_road())
    assert yao_work.idea_exists(run_road()) == False
    assert len(yao_work._idearoot._beliefunits) == 2
    assert yao_work != yao_duty0


def test_listen_to_person_jobs_Pipeline_Scenario1_yao_duty_CanOnlyReferenceItself(
    env_dir_setup_cleanup,
):
    # GIVEN
    # yao0_duty with 3 debotors of different creditor_weights
    # yao_job1 with 1 task, belief that doesn't want that task
    # yao_job2 with 2 tasks, one is same belief wants task
    # yao_job3 with 1 new task, belief stays with it

    yao_duty0 = get_example_yao_duty_with_3_healers()
    yao_duty0.add_l1_idea(ideaunit_shop(get_location_text()))
    yao_duty0.add_idea(ideaunit_shop(get_in_ocean_text()), get_location_road())
    yao_duty0.add_idea(ideaunit_shop(get_on_land_text()), get_location_road())
    yao_duty0.add_l1_idea(ideaunit_shop(get_swim_text(), pledge=True))
    yao_duty0.edit_reason(get_swim_road(), get_location_road(), get_in_ocean_road())
    yao_duty0.set_belief(get_location_road(), get_in_ocean_road())
    print(f"{yao_duty0.get_belief(get_location_road())=}")
    yao_duty0.del_idea_obj(run_road())
    assert yao_duty0._econ_dict.get(get_iowa_road())
    assert yao_duty0._econ_dict.get(get_ohio_road())
    assert yao_duty0._econ_dict.get(get_utah_road())
    yao_duty0.calc_agenda_metrics()
    assert len(yao_duty0._econ_dict) == 3
    # print(f"{yao_duty0._idea_dict.keys()=}")

    yao_text = yao_duty0._owner_id
    yao_job1 = get_example_yao_job1_speaker()
    yao_job2 = get_example_yao_job2_speaker()
    yao_job3 = get_example_yao_job3_speaker()
    yao_iowa_agendahub = get_yao_iowa_agendahub()
    yao_ohio_agendahub = get_yao_ohio_agendahub()
    zia_utah_agendahub = get_zia_utah_agendahub()
    # delete_dir(yao_iowa_agendahub.persons_dir())
    assert yao_iowa_agendahub.duty_file_exists() == False
    assert yao_iowa_agendahub.work_file_exists() == False
    assert yao_iowa_agendahub.job_file_exists(yao_text) == False
    assert yao_ohio_agendahub.job_file_exists(yao_text) == False
    assert zia_utah_agendahub.job_file_exists(yao_text) == False
    print(f"{yao_duty0.get_belief(get_location_road())=}")
    yao_iowa_agendahub.save_duty_agenda(yao_duty0)
    # yao_iowa_agendahub.save_job_agenda(yao_job1)
    # yao_ohio_agendahub.save_job_agenda(yao_job2)
    # zia_utah_agendahub.save_job_agenda(yao_job3)
    assert yao_iowa_agendahub.duty_file_exists()
    assert yao_iowa_agendahub.job_file_exists(yao_text) == False
    assert yao_ohio_agendahub.job_file_exists(yao_text) == False
    assert zia_utah_agendahub.job_file_exists(yao_text) == False

    # WHEN
    assert yao_iowa_agendahub.work_file_exists() == False
    listen_to_person_jobs(yao_iowa_agendahub)
    assert yao_iowa_agendahub.work_file_exists()

    yao_work = yao_iowa_agendahub.get_work_agenda()
    yao_work.calc_agenda_metrics()
    assert yao_work._partys.keys() == yao_duty0._partys.keys()
    assert yao_work.get_party(yao_text)._irrational_debtor_weight == 0
    assert yao_work.get_groupunits_dict() == yao_duty0.get_groupunits_dict()
    assert len(yao_work._idea_dict) == 4
    print(f"{yao_work._idea_dict.keys()=}")
    print(f"{yao_work.get_beliefunits_dict().keys()=}")
    assert yao_work.idea_exists(cook_road()) == False
    assert yao_work.idea_exists(clean_road()) == False
    assert yao_work.idea_exists(run_road()) == False
    assert yao_work.idea_exists(get_swim_road())
    assert yao_work.idea_exists(get_in_ocean_road())
    assert yao_work.idea_exists(get_on_land_road()) == False
    assert yao_work.get_belief(get_location_road()) != None
    assert yao_work.get_belief(get_location_road()).pick == get_in_ocean_road()
    assert len(yao_work.get_intent_dict()) == 1
    assert len(yao_work._idearoot._beliefunits) == 1
    assert yao_work != yao_duty0
