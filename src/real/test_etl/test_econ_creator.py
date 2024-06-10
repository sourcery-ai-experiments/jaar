from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.graphic import display_ideatree
from src.listen.filehub import filehub_shop
from src.real.econ_creator import (
    init_treasury_db_file,
    create_duty_treasury_db_files,
    init_treasury_db_file,
    set_all_role_files,
    set_person_moneyunits_role,
)
from src.real.examples.real_env import env_dir_setup_cleanup
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_init_treasury_db_file_CreatesAndReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    pound_text = "#"
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text, None, road_delimiter=pound_text)
    sue_filehub.save_duty_agenda(sue_filehub.default_duty_agenda())
    sue_duty_agenda = sue_filehub.get_duty_agenda()

    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    sue_filehub.econ_road = dallas_road
    sue_filehub.initialize_atom_duty_files()
    dallas_db_path = sue_filehub.treasury_db_path()
    print(f"{dallas_db_path=}")
    assert os_path_exists(dallas_db_path) is False

    # WHEN
    sue_dallas_moneyunit = init_treasury_db_file(sue_filehub, dallas_road)

    # THEN
    assert os_path_exists(dallas_db_path)
    assert sue_dallas_moneyunit.filehub.real_id == sue_filehub.real_id
    assert sue_dallas_moneyunit.filehub.person_id == sue_text
    assert sue_dallas_moneyunit.filehub.road_delimiter == sue_filehub.road_delimiter


def test_create_duty_treasury_db_files_RaisesErrorWhen__econs_justified_IsFalse(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text, None)
    sue_filehub.save_duty_agenda(sue_filehub.default_duty_agenda())
    sue_duty_agenda = sue_filehub.get_duty_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_duty_agenda.add_idea(ideaunit_shop(dallas_text), texas_road)
    sue_duty_agenda.edit_idea_attr(texas_road, healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.edit_idea_attr(dallas_road, healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.calc_agenda_metrics()
    assert sue_duty_agenda._econs_justified is False
    sue_filehub.save_duty_agenda(sue_duty_agenda)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        create_duty_treasury_db_files(sue_filehub)
    assert (
        str(excinfo.value)
        == f"Cannot set '{sue_text}' duty agenda moneyunits because 'AgendaUnit._econs_justified' is False."
    )


def test_create_duty_treasury_db_files_RaisesErrorWhen__econs_buildable_IsFalse(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text, None)
    sue_filehub.save_duty_agenda(sue_filehub.default_duty_agenda())
    sue_duty_agenda = sue_filehub.get_duty_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Tex/as"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_duty_agenda.edit_idea_attr(texas_road, healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.calc_agenda_metrics()
    assert sue_duty_agenda._econs_justified
    assert sue_duty_agenda._econs_buildable is False
    sue_filehub.save_duty_agenda(sue_duty_agenda)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        create_duty_treasury_db_files(sue_filehub)
    assert (
        str(excinfo.value)
        == f"Cannot set '{sue_text}' duty agenda moneyunits because 'AgendaUnit._econs_buildable' is False."
    )


def test_create_duty_treasury_db_files_CreatesMoneyUnits(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text, None)
    sue_filehub.save_duty_agenda(sue_filehub.default_duty_agenda())
    sue_duty_agenda = sue_filehub.get_duty_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    elpaso_text = "el paso"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    elpaso_road = sue_duty_agenda.make_road(texas_road, elpaso_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(dallas_idea, texas_road)
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    sue_duty_agenda.calc_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    sue_filehub.save_duty_agenda(sue_duty_agenda)

    dallas_filehub = filehub_shop(None, None, sue_text, dallas_road)
    elpaso_filehub = filehub_shop(None, None, sue_text, elpaso_road)
    print(f"{dallas_filehub.treasury_db_path()=}")
    print(f"{elpaso_filehub.treasury_db_path()=}")
    assert os_path_exists(dallas_filehub.treasury_db_path()) is False
    assert os_path_exists(elpaso_filehub.treasury_db_path()) is False

    # WHEN
    create_duty_treasury_db_files(sue_filehub)

    # THEN
    assert os_path_exists(dallas_filehub.treasury_db_path())
    assert os_path_exists(elpaso_filehub.treasury_db_path())


def test_get_econ_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text, None)
    sue_filehub.save_duty_agenda(sue_filehub.default_duty_agenda())
    sue_duty_agenda = sue_filehub.get_duty_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(dallas_idea, texas_road)
    sue_duty_agenda.calc_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    sue_filehub.save_duty_agenda(sue_duty_agenda)

    # WHEN
    create_duty_treasury_db_files(sue_filehub)
    dallas_money = init_treasury_db_file(sue_filehub, dallas_road)

    # THEN
    assert dallas_money != None
    assert dallas_money.filehub.real_id == sue_filehub.real_id


def test_set_all_role_files_CorrectlySets_roles(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text, None)
    sue_filehub.save_duty_agenda(sue_filehub.default_duty_agenda())
    sue_duty_agenda = sue_filehub.get_duty_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(dallas_idea, texas_road)
    elpaso_text = "el paso"
    elpaso_road = sue_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    # sue_duty_agenda.calc_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    sue_filehub.save_duty_agenda(sue_duty_agenda)
    create_duty_treasury_db_files(sue_filehub)
    sue_file_name = sue_filehub.owner_file_name(sue_text)
    dallas_money = init_treasury_db_file(sue_filehub, dallas_road)
    dallas_sue_role_file_path = f"{dallas_money.filehub.roles_dir()}/{sue_file_name}"
    elpaso_money = init_treasury_db_file(sue_filehub, elpaso_road)
    elpaso_sue_role_file_path = f"{elpaso_money.filehub.roles_dir()}/{sue_file_name}"
    assert os_path_exists(dallas_sue_role_file_path) is False
    assert os_path_exists(elpaso_sue_role_file_path) is False

    # WHEN
    set_all_role_files(sue_filehub, sue_duty_agenda)

    # THEN
    assert os_path_exists(dallas_sue_role_file_path)
    assert os_path_exists(elpaso_sue_role_file_path)


def test_set_person_moneyunits_role_CorrectlySetsroles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(None, None, sue_text, None)
    sue_filehub.save_duty_agenda(sue_filehub.default_duty_agenda())
    sue_duty_agenda = sue_filehub.get_duty_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(dallas_idea, texas_road)
    elpaso_text = "el paso"
    elpaso_road = sue_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    # sue_duty_agenda.calc_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    sue_filehub.save_duty_agenda(sue_duty_agenda)
    create_duty_treasury_db_files(sue_filehub)
    sue_file_name = sue_filehub.owner_file_name(sue_text)
    dallas_money = init_treasury_db_file(sue_filehub, dallas_road)
    dallas_sue_role_file_path = f"{dallas_money.filehub.roles_dir()}/{sue_file_name}"
    elpaso_money = init_treasury_db_file(sue_filehub, elpaso_road)
    elpaso_sue_role_file_path = f"{elpaso_money.filehub.roles_dir()}/{sue_file_name}"
    assert os_path_exists(dallas_sue_role_file_path) is False
    assert os_path_exists(elpaso_sue_role_file_path) is False

    # WHEN
    set_person_moneyunits_role(sue_filehub)

    # THEN
    assert os_path_exists(dallas_sue_role_file_path)
    assert os_path_exists(elpaso_sue_role_file_path)
