from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.listen.filehub import filehub_shop

# from src.agenda.graphic import display_ideatree
from src.real.econ_creator import create_duty_treasury_dbs
from src.real.real import RealUnit, realunit_shop
from src.real.examples.real_env import get_test_reals_dir


def create_example_real1() -> RealUnit:
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    yao_text = "Yao"
    music_real.init_person_econs(yao_text)
    yao_filehub = filehub_shop(None, music_text, yao_text, None)
    yao_duty_agenda = yao_filehub.get_duty_agenda()

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
    x_filehub = filehub_shop(
        reals_dir=yao_filehub.reals_dir,
        real_id=yao_filehub.real_id,
        person_id=yao_filehub.person_id,
        econ_road=None,
        road_delimiter=yao_filehub.road_delimiter,
        planck=yao_filehub.planck,
    )
    x_filehub.save_duty_agenda(yao_duty_agenda)
    create_duty_treasury_dbs(yao_filehub)

    # WHEN
    music_real.set_person_moneyunits_dirs(yao_text)

    return music_real


def create_example_real2() -> RealUnit:
    # GIVEN
    music_text = "music"
    music_real = realunit_shop(music_text, get_test_reals_dir(), in_memory_journal=True)
    yao_text = "Yao"
    wei_text = "Wei"
    zia_text = "Zia"
    music_real.init_person_econs(yao_text)
    yao_filehub = filehub_shop(None, music_text, yao_text, None)
    wei_filehub = filehub_shop(None, music_text, wei_text, None)
    zia_filehub = filehub_shop(None, music_text, zia_text, None)
    music_real.init_person_econs(wei_text)
    music_real.init_person_econs(zia_text)
    yao_duty_agenda = yao_filehub.get_duty_agenda()
    wei_duty_agenda = wei_filehub.get_duty_agenda()
    zia_duty_agenda = zia_filehub.get_duty_agenda()

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
    yao_filehub.save_duty_agenda(yao_duty_agenda)
    wei_filehub.save_duty_agenda(wei_duty_agenda)
    zia_filehub.save_duty_agenda(zia_duty_agenda)
    create_duty_treasury_dbs(yao_filehub)
    create_duty_treasury_dbs(wei_filehub)
    create_duty_treasury_dbs(zia_filehub)
    # yao_dallas_econ = yao_init_moneyunit(dallas_road)
    # zia_dallas_econ = zia_init_moneyunit(dallas_road)
    music_real.set_person_moneyunits_dirs(yao_text)
    music_real.set_person_moneyunits_dirs(wei_text)
    music_real.set_person_moneyunits_dirs(zia_text)

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
    yao_filehub = filehub_shop(None, music_text, yao_text, None)
    wei_filehub = filehub_shop(None, music_text, wei_text, None)
    zia_filehub = filehub_shop(None, music_text, zia_text, None)
    yao_duty_agenda = yao_filehub.get_duty_agenda()
    wei_duty_agenda = wei_filehub.get_duty_agenda()
    zia_duty_agenda = zia_filehub.get_duty_agenda()

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
    yao_filehub.save_duty_agenda(yao_duty_agenda)
    wei_filehub.save_duty_agenda(wei_duty_agenda)
    zia_filehub.save_duty_agenda(zia_duty_agenda)

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
    yao_filehub = filehub_shop(None, music_text, yao_text, None)
    wei_filehub = filehub_shop(None, music_text, wei_text, None)
    zia_filehub = filehub_shop(None, music_text, zia_text, None)
    yao_duty_agenda = yao_filehub.get_duty_agenda()
    wei_duty_agenda = wei_filehub.get_duty_agenda()
    zia_duty_agenda = zia_filehub.get_duty_agenda()

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
    yao_filehub.save_duty_agenda(yao_duty_agenda)
    wei_filehub.save_duty_agenda(wei_duty_agenda)
    zia_filehub.save_duty_agenda(zia_duty_agenda)
    # create_duty_treasury_dbs(yao_filehub)
    # wei_create_duty_treasury_dbs()
    # zia_create_duty_treasury_dbs()
    # yao_dallas_econ = yao_init_moneyunit(dallas_road)
    # zia_dallas_econ = zia_init_moneyunit(dallas_road)
    # yao_elpaso_econ = yao_init_moneyunit(elpaso_road)
    # yao_dallas_money.filehub.save_role_agenda(yao_duty_agenda)
    # yao_dallas_money.filehub.save_role_agenda(wei_duty_agenda)
    # yao_dallas_money.filehub.save_role_agenda(zia_duty_agenda)
    # zia_dallas_money.filehub.save_role_agenda(yao_duty_agenda)
    # zia_dallas_money.filehub.save_role_agenda(wei_duty_agenda)
    # zia_dallas_money.filehub.save_role_agenda(zia_duty_agenda)
    # yao_elpaso_money.filehub.save_role_agenda(yao_duty_agenda)
    # yao_elpaso_money.filehub.save_role_agenda(wei_duty_agenda)
    # yao_elpaso_money.filehub.save_role_agenda(zia_duty_agenda)
    # music_real.set_all_moneyunits_role(yao_text)
    # music_real.set_all_moneyunits_role(wei_text)
    # music_real.set_all_moneyunits_role(zia_text)

    return music_real
