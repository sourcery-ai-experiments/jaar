# from src._road.road import default_road_delimiter_if_none
from src._road.road import RoadUnit, create_road, get_default_real_id_roadnode, RoadNode
from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import AgendaUnit, agendaunit_shop
from src.change.agendahub import agendahub_shop, AgendaHub, pipeline_duty_work_text

# from src.agenda.graphic import display_ideatree
from src.real.admin_duty import get_duty_file_agenda
from src.real.econ_creator import create_person_econunits
from src.real.real import RealUnit, realunit_shop
from src.real.examples.real_env_kit import (
    get_test_reals_dir,
    reals_dir_setup_cleanup,
    get_test_real_id,
)


def create_example_real1() -> RealUnit:
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    yao_text = "Yao"
    music_real.init_person_econs(yao_text)
    yao_agendahub = agendahub_shop(None, music_text, yao_text, None)
    yao_duty_agenda = get_duty_file_agenda(yao_agendahub)

    yao_duty_agenda.set_party_creditor_pool(101)
    yao_duty_agenda.set_party_debtor_pool(1000)

    yao_duty_agenda.add_partyunit(yao_text, 34, 600)
    yao_duty_agenda.calc_agenda_metrics()
    texas_text = "Texas"
    texas_road = yao_duty_agenda.make_l1_road(texas_text)
    yao_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = yao_duty_agenda.make_road(texas_road, dallas_text)
    dallas_healerhold = healerhold_shop({yao_text})
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=dallas_healerhold)
    elpaso_text = "el paso"
    elpaso_road = yao_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_healerhold = healerhold_shop({yao_text})
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=elpaso_healerhold)

    yao_duty_agenda.add_idea(dallas_idea, texas_road)
    yao_duty_agenda.add_idea(elpaso_idea, texas_road)
    # display_agenda(yao_duty_agenda.calc_agenda_metrics(), mode="Econ").show()
    x_agendahub = agendahub_shop(
        reals_dir=yao_agendahub.reals_dir,
        real_id=yao_agendahub.real_id,
        person_id=yao_agendahub.person_id,
        econ_road=None,
        road_delimiter=yao_agendahub._road_delimiter,
        planck=yao_agendahub._planck,
    )
    x_agendahub.save_duty_agenda(yao_duty_agenda)
    create_person_econunits(yao_agendahub)

    # WHEN
    music_real.set_person_econunits_dirs(yao_text)

    return music_real


def create_example_real2() -> RealUnit:
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    music_real.init_person_econs(yao_text)
    yao_agendahub = agendahub_shop(None, music_text, yao_text, None)
    wei_agendahub = agendahub_shop(None, music_text, wei_text, None)
    zia_agendahub = agendahub_shop(None, music_text, zia_text, None)
    music_real.init_person_econs(wei_text)
    music_real.init_person_econs(zia_text)
    yao_duty_agenda = get_duty_file_agenda(yao_agendahub)
    wei_duty_agenda = get_duty_file_agenda(wei_agendahub)
    zia_duty_agenda = get_duty_file_agenda(zia_agendahub)

    yao_duty_agenda.set_party_creditor_pool(101)
    wei_duty_agenda.set_party_creditor_pool(75)
    zia_duty_agenda.set_party_creditor_pool(52)
    yao_duty_agenda.set_party_debtor_pool(1000)
    wei_duty_agenda.set_party_debtor_pool(750)
    zia_duty_agenda.set_party_debtor_pool(500)

    yao_duty_agenda.add_partyunit(yao_text, 34, 600)
    yao_duty_agenda.add_partyunit(zia_text, 57, 300)
    yao_duty_agenda.add_partyunit(wei_text, 10, 100)
    wei_duty_agenda.add_partyunit(yao_text, 37, 100)
    wei_duty_agenda.add_partyunit(wei_text, 11, 400)
    wei_duty_agenda.add_partyunit(zia_text, 27, 250)
    zia_duty_agenda.add_partyunit(yao_text, 14, 100)
    zia_duty_agenda.add_partyunit(zia_text, 38, 400)
    texas_text = "Texas"
    texas_road = yao_duty_agenda.make_l1_road(texas_text)
    yao_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    wei_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    zia_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = yao_duty_agenda.make_road(texas_road, dallas_text)
    dallas_healerhold = healerhold_shop({yao_text, zia_text})
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=dallas_healerhold)
    elpaso_text = "el paso"
    elpaso_road = yao_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_healerhold = healerhold_shop({yao_text})
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=elpaso_healerhold)

    yao_duty_agenda.add_idea(dallas_idea, texas_road)
    yao_duty_agenda.add_idea(elpaso_idea, texas_road)
    wei_duty_agenda.add_idea(dallas_idea, texas_road)
    wei_duty_agenda.add_idea(elpaso_idea, texas_road)
    zia_duty_agenda.add_idea(dallas_idea, texas_road)
    zia_duty_agenda.add_idea(elpaso_idea, texas_road)
    # display_agenda(yao_duty_agenda.calc_agenda_metrics(), mode="Econ").show()
    yao_agendahub.save_duty_agenda(yao_duty_agenda)
    wei_agendahub.save_duty_agenda(wei_duty_agenda)
    zia_agendahub.save_duty_agenda(zia_duty_agenda)
    create_person_econunits(yao_agendahub)
    create_person_econunits(wei_agendahub)
    create_person_econunits(zia_agendahub)
    # yao_dallas_econ = yao_get_econunit(dallas_road)
    # zia_dallas_econ = zia_get_econunit(dallas_road)
    music_real.set_person_econunits_dirs(yao_text)
    music_real.set_person_econunits_dirs(wei_text)
    music_real.set_person_econunits_dirs(zia_text)

    return music_real


def create_example_real3() -> RealUnit:
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    music_real.init_person_econs(yao_text)
    music_real.init_person_econs(wei_text)
    music_real.init_person_econs(zia_text)
    yao_agendahub = agendahub_shop(None, music_text, yao_text, None)
    wei_agendahub = agendahub_shop(None, music_text, wei_text, None)
    zia_agendahub = agendahub_shop(None, music_text, zia_text, None)
    yao_duty_agenda = get_duty_file_agenda(yao_agendahub)
    wei_duty_agenda = get_duty_file_agenda(wei_agendahub)
    zia_duty_agenda = get_duty_file_agenda(zia_agendahub)

    casa_text = "casa"
    casa_road = yao_duty_agenda.make_l1_road(casa_text)
    yao_duty_agenda.add_l1_idea(ideaunit_shop(casa_text))
    wei_duty_agenda.add_l1_idea(ideaunit_shop(casa_text))
    zia_duty_agenda.add_l1_idea(ideaunit_shop(casa_text))
    clean_text = "clean"
    clean_road = yao_duty_agenda.make_road(casa_road, clean_text)
    bath_text = "clean bathroom"
    hall_text = "clean hall"

    yao_duty_agenda.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    yao_duty_agenda.add_idea(ideaunit_shop(bath_text, pledge=True), clean_road)
    yao_duty_agenda.add_idea(ideaunit_shop(hall_text, pledge=True), clean_road)
    # yao_duty_agenda.calc_agenda_metrics()
    # display_ideatree(yao_duty_agenda, mode="Econ").show()

    wei_duty_agenda.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    wei_duty_agenda.add_idea(ideaunit_shop(bath_text, pledge=True), clean_road)

    zia_duty_agenda.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    zia_duty_agenda.add_idea(ideaunit_shop(bath_text, pledge=True), clean_road)
    zia_duty_agenda.add_idea(ideaunit_shop(hall_text, pledge=True), clean_road)

    # display_ideatree(yao_duty_agenda, mode="Econ").show()
    yao_agendahub.save_duty_agenda(yao_duty_agenda)
    wei_agendahub.save_duty_agenda(wei_duty_agenda)
    zia_agendahub.save_duty_agenda(zia_duty_agenda)

    return music_real


def create_example_real4() -> RealUnit:
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    music_real.init_person_econs(yao_text)
    music_real.init_person_econs(wei_text)
    music_real.init_person_econs(zia_text)
    yao_agendahub = agendahub_shop(None, music_text, yao_text, None)
    wei_agendahub = agendahub_shop(None, music_text, wei_text, None)
    zia_agendahub = agendahub_shop(None, music_text, zia_text, None)
    yao_duty_agenda = get_duty_file_agenda(yao_agendahub)
    wei_duty_agenda = get_duty_file_agenda(wei_agendahub)
    zia_duty_agenda = get_duty_file_agenda(zia_agendahub)

    casa_text = "casa"
    casa_road = yao_duty_agenda.make_l1_road(casa_text)
    yao_duty_agenda.add_l1_idea(ideaunit_shop(casa_text))
    wei_duty_agenda.add_l1_idea(ideaunit_shop(casa_text))
    zia_duty_agenda.add_l1_idea(ideaunit_shop(casa_text))
    clean_text = "clean"
    clean_road = yao_duty_agenda.make_road(casa_road, clean_text)
    bath_text = "clean bathroom"
    hall_text = "clean hall"

    yao_duty_agenda.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    yao_duty_agenda.add_idea(ideaunit_shop(bath_text, pledge=True), clean_road)
    yao_duty_agenda.add_idea(ideaunit_shop(hall_text, pledge=True), clean_road)
    # yao_duty_agenda.calc_agenda_metrics()
    # display_ideatree(yao_duty_agenda, mode="Econ").show()

    wei_duty_agenda.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    wei_duty_agenda.add_idea(ideaunit_shop(bath_text, pledge=True), clean_road)

    zia_duty_agenda.add_idea(ideaunit_shop(clean_text, pledge=True), casa_road)
    zia_duty_agenda.add_idea(ideaunit_shop(bath_text, pledge=True), clean_road)
    zia_duty_agenda.add_idea(ideaunit_shop(hall_text, pledge=True), clean_road)

    # display_ideatree(yao_duty_agenda, mode="Econ").show()
    yao_duty_agenda.set_party_creditor_pool(101)
    wei_duty_agenda.set_party_creditor_pool(75)
    zia_duty_agenda.set_party_creditor_pool(52)
    yao_duty_agenda.set_party_debtor_pool(1000)
    wei_duty_agenda.set_party_debtor_pool(750)
    zia_duty_agenda.set_party_debtor_pool(500)

    yao_duty_agenda.add_partyunit(yao_text, 34, 600)
    yao_duty_agenda.add_partyunit(zia_text, 57, 300)
    yao_duty_agenda.add_partyunit(wei_text, 10, 100)
    wei_duty_agenda.add_partyunit(yao_text, 37, 100)
    wei_duty_agenda.add_partyunit(wei_text, 11, 400)
    wei_duty_agenda.add_partyunit(zia_text, 27, 250)
    zia_duty_agenda.add_partyunit(yao_text, 14, 100)
    zia_duty_agenda.add_partyunit(zia_text, 38, 400)

    texas_text = "Texas"
    texas_road = yao_duty_agenda.make_l1_road(texas_text)
    yao_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    wei_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    zia_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = yao_duty_agenda.make_road(texas_road, dallas_text)
    dallas_healerhold = healerhold_shop({yao_text, zia_text})
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=dallas_healerhold)
    elpaso_text = "el paso"
    elpaso_road = yao_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_healerhold = healerhold_shop({yao_text})
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=elpaso_healerhold)

    yao_duty_agenda.add_idea(dallas_idea, texas_road)
    yao_duty_agenda.add_idea(elpaso_idea, texas_road)
    wei_duty_agenda.add_idea(dallas_idea, texas_road)
    wei_duty_agenda.add_idea(elpaso_idea, texas_road)
    zia_duty_agenda.add_idea(dallas_idea, texas_road)
    zia_duty_agenda.add_idea(elpaso_idea, texas_road)
    # display_agenda(yao_duty_agenda.calc_agenda_metrics(), mode="Econ").show()
    yao_agendahub.save_duty_agenda(yao_duty_agenda)
    wei_agendahub.save_duty_agenda(wei_duty_agenda)
    zia_agendahub.save_duty_agenda(zia_duty_agenda)
    # create_person_econunits(yao_agendahub)
    # wei_create_person_econunits()
    # zia_create_person_econunits()
    # yao_dallas_econ = yao_get_econunit(dallas_road)
    # zia_dallas_econ = zia_get_econunit(dallas_road)
    # yao_elpaso_econ = yao_get_econunit(elpaso_road)
    # yao_dallas_econ.agendahub.save_role_agenda(yao_duty_agenda)
    # yao_dallas_econ.agendahub.save_role_agenda(wei_duty_agenda)
    # yao_dallas_econ.agendahub.save_role_agenda(zia_duty_agenda)
    # zia_dallas_econ.agendahub.save_role_agenda(yao_duty_agenda)
    # zia_dallas_econ.agendahub.save_role_agenda(wei_duty_agenda)
    # zia_dallas_econ.agendahub.save_role_agenda(zia_duty_agenda)
    # yao_elpaso_econ.agendahub.save_role_agenda(yao_duty_agenda)
    # yao_elpaso_econ.agendahub.save_role_agenda(wei_duty_agenda)
    # yao_elpaso_econ.agendahub.save_role_agenda(zia_duty_agenda)
    # music_real.set_all_econunits_role(yao_text)
    # music_real.set_all_econunits_role(wei_text)
    # music_real.set_all_econunits_role(zia_text)

    return music_real


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


def get_iowa_road() -> RoadUnit:
    return create_road(get_usa_road(), "Iowa")


def get_ohio_road() -> RoadUnit:
    return create_road(get_usa_road(), "Ohio")


def get_utah_road() -> RoadUnit:
    return create_road(get_usa_road(), "Utah")


def get_yao_ohio_agendahub() -> AgendaHub:
    yao_agenda = get_example_yao_agenda()
    return agendahub_shop(
        reals_dir=get_test_reals_dir(),
        real_id=yao_agenda._real_id,
        person_id=yao_agenda._owner_id,
        econ_road=get_ohio_road(),
        nox_type=pipeline_duty_work_text(),
    )


def get_yao_iowa_agendahub() -> AgendaHub:
    yao_agenda = get_example_yao_agenda()
    return agendahub_shop(
        reals_dir=get_test_reals_dir(),
        real_id=yao_agenda._real_id,
        person_id=yao_agenda._owner_id,
        econ_road=get_iowa_road(),
        nox_type=pipeline_duty_work_text(),
    )


def get_zia_utah_agendahub() -> AgendaHub:
    yao_agenda = get_example_yao_agenda()
    return agendahub_shop(
        reals_dir=get_test_reals_dir(),
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
