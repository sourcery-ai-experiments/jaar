from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.listen.userhub import userhub_shop
from src.real.real import RealUnit, realunit_shop
from src.real.examples.real_env import get_test_reals_dir

# from src.agenda.graphic import display_ideatree


def create_example_real1() -> RealUnit:
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    yao_text = "Yao"
    music_real.init_person_econs(yao_text)
    yao_userhub = userhub_shop(None, music_text, yao_text, None)
    yao_duty_agenda = yao_userhub.get_duty_agenda()

    yao_duty_agenda.set_party_credor_pool(101)
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
    x_userhub = userhub_shop(
        reals_dir=yao_userhub.reals_dir,
        real_id=yao_userhub.real_id,
        person_id=yao_userhub.person_id,
        econ_road=None,
        road_delimiter=yao_userhub.road_delimiter,
        planck=yao_userhub.planck,
    )
    x_userhub.save_duty_agenda(yao_duty_agenda)
    yao_userhub.create_duty_treasury_db_files()

    # WHEN
    music_real._set_all_healer_roles(yao_text)

    return music_real


def create_example_real2() -> RealUnit:
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    music_real.init_person_econs(yao_text)
    yao_userhub = userhub_shop(None, music_text, yao_text, None)
    wei_userhub = userhub_shop(None, music_text, wei_text, None)
    zia_userhub = userhub_shop(None, music_text, zia_text, None)
    music_real.init_person_econs(wei_text)
    music_real.init_person_econs(zia_text)
    yao_duty_agenda = yao_userhub.get_duty_agenda()
    wei_duty_agenda = wei_userhub.get_duty_agenda()
    zia_duty_agenda = zia_userhub.get_duty_agenda()

    yao_duty_agenda.set_party_credor_pool(101)
    wei_duty_agenda.set_party_credor_pool(75)
    zia_duty_agenda.set_party_credor_pool(52)
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
    yao_userhub.save_duty_agenda(yao_duty_agenda)
    wei_userhub.save_duty_agenda(wei_duty_agenda)
    zia_userhub.save_duty_agenda(zia_duty_agenda)
    yao_userhub.create_duty_treasury_db_files()
    wei_userhub.create_duty_treasury_db_files()
    zia_userhub.create_duty_treasury_db_files()
    music_real._set_all_healer_roles(yao_text)
    music_real._set_all_healer_roles(wei_text)
    music_real._set_all_healer_roles(zia_text)

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
    yao_userhub = userhub_shop(None, music_text, yao_text, None)
    wei_userhub = userhub_shop(None, music_text, wei_text, None)
    zia_userhub = userhub_shop(None, music_text, zia_text, None)
    yao_duty_agenda = yao_userhub.get_duty_agenda()
    wei_duty_agenda = wei_userhub.get_duty_agenda()
    zia_duty_agenda = zia_userhub.get_duty_agenda()

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
    yao_userhub.save_duty_agenda(yao_duty_agenda)
    wei_userhub.save_duty_agenda(wei_duty_agenda)
    zia_userhub.save_duty_agenda(zia_duty_agenda)

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
    yao_userhub = userhub_shop(None, music_text, yao_text, None)
    wei_userhub = userhub_shop(None, music_text, wei_text, None)
    zia_userhub = userhub_shop(None, music_text, zia_text, None)
    yao_duty_agenda = yao_userhub.get_duty_agenda()
    wei_duty_agenda = wei_userhub.get_duty_agenda()
    zia_duty_agenda = zia_userhub.get_duty_agenda()

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
    yao_duty_agenda.set_party_credor_pool(101)
    wei_duty_agenda.set_party_credor_pool(75)
    zia_duty_agenda.set_party_credor_pool(52)
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
    yao_userhub.save_duty_agenda(yao_duty_agenda)
    wei_userhub.save_duty_agenda(wei_duty_agenda)
    zia_userhub.save_duty_agenda(zia_duty_agenda)

    return music_real
