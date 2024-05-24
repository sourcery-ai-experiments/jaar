from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.graphic import display_ideatree
from src.econ.job_creator import (
    get_file_in_roles,
    save_file_to_roles,
    get_owner_file_name,
)
from src.econ.econ import treasury_db_filename, get_rootpart_of_econ_dir
from src.real.person import PersonUnit, personunit_shop
from pytest import raises as pytest_raises
from src.real.examples.real_env_kit import reals_dir_setup_cleanup
from os.path import exists as os_path_exists


def test_PersonUnit_get_person_econ_dir_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    texas_text = "texas"
    dallas_text = "dallas"
    elpaso_text = "el paso"
    kern_text = "kern"
    idearoot = get_rootpart_of_econ_dir()

    # WHEN
    texas_path = sue_person._get_person_econ_dir([idearoot, texas_text])
    dallas_path = sue_person._get_person_econ_dir([idearoot, texas_text, dallas_text])
    elpaso_path = sue_person._get_person_econ_dir([idearoot, texas_text, elpaso_text])
    kern_path = sue_person._get_person_econ_dir(
        [idearoot, texas_text, elpaso_text, kern_text]
    )

    # THEN
    idearoot_dir = f"{sue_person._econs_dir}/{get_rootpart_of_econ_dir()}"
    assert texas_path == f"{idearoot_dir}/{texas_text}"
    assert dallas_path == f"{idearoot_dir}/{texas_text}/{dallas_text}"
    assert elpaso_path == f"{idearoot_dir}/{texas_text}/{elpaso_text}"
    assert kern_path == f"{idearoot_dir}/{texas_text}/{elpaso_text}/{kern_text}"


def test_PersonUnit_create_econ_dir_CreatesDir(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    assert os_path_exists(sue_person._econs_dir)
    dallas_text = "dallas"
    dallas_list = [dallas_text]
    dallas_dir = sue_person._get_person_econ_dir(dallas_list)
    print(f"{dallas_dir=}")
    assert os_path_exists(dallas_dir) == False

    # WHEN
    sue_person._create_econ_dir(dallas_text)

    # THEN
    print(f"{dallas_dir=}")
    assert os_path_exists(dallas_dir)


def test_PersonUnit_create_econunit_CreatesEconUnit(reals_dir_setup_cleanup):
    # GIVEN
    pound_text = "#"
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text, _road_delimiter=pound_text)
    sue_duty_agenda = sue_person.get_duty_file_agenda()
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    dallas_dir = sue_person._create_econ_dir(dallas_road)
    dallas_db_path = f"{dallas_dir}/{treasury_db_filename()}"
    print(f"{dallas_dir=}")
    print(f"{dallas_db_path=}")
    assert os_path_exists(dallas_db_path) == False
    assert sue_person._econ_objs == {}

    # WHEN
    sue_person._create_econunit(dallas_road)

    # THEN
    assert os_path_exists(dallas_db_path)
    assert sue_person._econ_objs != {}
    assert sue_person._econ_objs.get(dallas_road) != None
    dallas_econunit = sue_person._econ_objs.get(dallas_road)
    assert dallas_econunit.real_id == sue_person.real_id
    assert dallas_econunit.econ_dir == dallas_dir
    assert dallas_econunit._manager_person_id == sue_text
    assert dallas_econunit._road_delimiter == sue_person._road_delimiter


def test_PersonUnit_create_person_econunits_RaisesErrorWhen__econs_justified_IsFalse(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_duty_agenda = sue_person.get_duty_file_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_duty_agenda.add_idea(ideaunit_shop(dallas_text), texas_road)
    sue_duty_agenda.edit_idea_attr(texas_road, healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.edit_idea_attr(dallas_road, healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.set_agenda_metrics()
    assert sue_duty_agenda._econs_justified == False
    sue_person.save_duty_file(sue_duty_agenda)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.create_person_econunits(econ_exceptions=False)
    assert (
        str(excinfo.value)
        == f"Cannot set '{sue_text}' duty agenda econunits because 'AgendaUnit._econs_justified' is False."
    )


def test_PersonUnit_create_person_econunits_RaisesErrorWhen__econs_buildable_IsFalse(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_duty_agenda = sue_person.get_duty_file_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Tex/as"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_duty_agenda.edit_idea_attr(texas_road, healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.set_agenda_metrics()
    assert sue_duty_agenda._econs_justified
    assert sue_duty_agenda._econs_buildable == False
    sue_person.save_duty_file(sue_duty_agenda)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.create_person_econunits()
    assert (
        str(excinfo.value)
        == f"Cannot set '{sue_text}' duty agenda econunits because 'AgendaUnit._econs_buildable' is False."
    )


def test_PersonUnit_create_person_econunits_CreatesEconUnits(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_duty_agenda = sue_person.get_duty_file_agenda()
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
    sue_duty_agenda.set_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    sue_person.save_duty_file(sue_duty_agenda)

    dallas_dir = sue_person._create_econ_dir(dallas_road)
    elpaso_dir = sue_person._create_econ_dir(elpaso_road)
    dallas_db_path = f"{dallas_dir}/{treasury_db_filename()}"
    elpaso_db_path = f"{elpaso_dir}/{treasury_db_filename()}"
    print(f"{dallas_dir=}")
    print(f"{elpaso_db_path=}")
    print(f"{dallas_db_path=}")
    print(f"{elpaso_db_path=}")
    assert os_path_exists(dallas_db_path) == False
    assert os_path_exists(elpaso_db_path) == False
    assert sue_person._econ_objs == {}

    # WHEN
    sue_person.create_person_econunits()

    # THEN
    assert os_path_exists(dallas_db_path)
    assert os_path_exists(elpaso_db_path)
    assert sue_person._econ_objs != {}
    assert sue_person._econ_objs.get(dallas_road) != None
    assert sue_person._econ_objs.get(elpaso_road) != None


def test_PersonUnit_create_person_econunits_DeletesEconUnits(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_duty_agenda = sue_person.get_duty_file_agenda()
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
    sue_duty_agenda.set_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    sue_person.save_duty_file(sue_duty_agenda)
    dallas_dir = sue_person._create_econ_dir(dallas_road)
    elpaso_dir = sue_person._create_econ_dir(elpaso_road)
    dallas_db_path = f"{dallas_dir}/{treasury_db_filename()}"
    elpaso_db_path = f"{elpaso_dir}/{treasury_db_filename()}"
    print(f"{dallas_dir=}")
    print(f"{elpaso_db_path=}")
    print(f"{dallas_db_path=}")
    print(f"{elpaso_db_path=}")
    sue_person.create_person_econunits()
    assert os_path_exists(dallas_db_path)
    assert os_path_exists(elpaso_db_path)
    assert sue_person._econ_objs.get(dallas_road) != None
    assert sue_person._econ_objs.get(elpaso_road) != None

    # WHEN
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({}))
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    sue_duty_agenda.set_agenda_metrics()
    sue_person.save_duty_file(sue_duty_agenda)
    sue_person.create_person_econunits()

    # THEN
    assert sue_person._econ_objs.get(dallas_road) != None
    assert sue_person._econ_objs.get(elpaso_road) is None
    assert os_path_exists(dallas_db_path)
    assert os_path_exists(elpaso_db_path) == False


def test_PersonUnit_get_econ_ReturnsCorrectObj(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_duty_agenda = sue_person.get_duty_file_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(dallas_idea, texas_road)
    sue_duty_agenda.set_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    sue_person.save_duty_file(sue_duty_agenda)
    dallas_dir = sue_person._create_econ_dir(dallas_road)
    print(f"{dallas_dir=}")
    assert sue_person._econ_objs == {}

    # WHEN
    sue_person.create_person_econunits()
    dallas_econ = sue_person.get_econ(dallas_road)

    # THEN
    assert dallas_econ != None
    assert dallas_econ.real_id == sue_person.real_id
    assert sue_person._econ_objs.get(dallas_road) == dallas_econ


def test_PersonUnit_set_econunit_role_CorrectlySets_role(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_duty_agenda = sue_person.get_duty_file_agenda()
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
    sue_duty_agenda.set_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    sue_person.save_duty_file(sue_duty_agenda)
    sue_person.create_person_econunits()
    print(f"{sue_person._econ_objs.keys()=}")
    dallas_econ = sue_person.get_econ(dallas_road)
    sue_file_name = get_owner_file_name(sue_text)
    sue_role_file_path = f"{dallas_econ.get_roles_dir()}/{sue_file_name}"
    assert os_path_exists(sue_role_file_path) == False

    # WHEN
    sue_person.set_econunit_role(dallas_road, sue_duty_agenda)

    # THEN
    assert os_path_exists(sue_role_file_path)


def test_PersonUnit_set_econunits_role_CorrectlySets_roles(reals_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_duty_agenda = sue_person.get_duty_file_agenda()
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
    # sue_duty_agenda.set_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    sue_person.save_duty_file(sue_duty_agenda)
    sue_person.create_person_econunits()
    sue_file_name = get_owner_file_name(sue_text)
    dallas_econ = sue_person.get_econ(dallas_road)
    dallas_sue_role_file_path = f"{dallas_econ.get_roles_dir()}/{sue_file_name}"
    elpaso_econ = sue_person.get_econ(elpaso_road)
    elpaso_sue_role_file_path = f"{elpaso_econ.get_roles_dir()}/{sue_file_name}"
    assert os_path_exists(dallas_sue_role_file_path) == False
    assert os_path_exists(elpaso_sue_role_file_path) == False

    # WHEN
    sue_person.set_econunits_role(sue_duty_agenda)

    # THEN
    assert os_path_exists(dallas_sue_role_file_path)
    assert os_path_exists(elpaso_sue_role_file_path)


def test_PersonUnit_set_person_econunits_role_CorrectlySetsroles(
    reals_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_duty_agenda = sue_person.get_duty_file_agenda()
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
    # sue_duty_agenda.set_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    sue_person.save_duty_file(sue_duty_agenda)
    sue_person.create_person_econunits()
    sue_file_name = get_owner_file_name(sue_text)
    dallas_econ = sue_person.get_econ(dallas_road)
    dallas_sue_role_file_path = f"{dallas_econ.get_roles_dir()}/{sue_file_name}"
    elpaso_econ = sue_person.get_econ(elpaso_road)
    elpaso_sue_role_file_path = f"{elpaso_econ.get_roles_dir()}/{sue_file_name}"
    assert os_path_exists(dallas_sue_role_file_path) == False
    assert os_path_exists(elpaso_sue_role_file_path) == False

    # WHEN
    sue_person.set_person_econunits_role()

    # THEN
    assert os_path_exists(dallas_sue_role_file_path)
    assert os_path_exists(elpaso_sue_role_file_path)
