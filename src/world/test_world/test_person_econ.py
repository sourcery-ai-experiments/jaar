from src._prime.road import get_all_road_nodes
from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.graphic import display_agenda
from src.world.person import PersonUnit, personunit_shop
from pytest import raises as pytest_raises
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    get_test_world_id,
    worlds_dir_setup_cleanup,
)
from os.path import exists as os_path_exists
from src.instrument.file import delete_dir, dir_files, open_file, set_dir, save_file


def test_PersonUnit_get_econ_path_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    idearoot = "idearoot"
    texas_text = "texas"
    dallas_text = "dallas"
    elpaso_text = "el paso"
    kern_text = "kern"

    # WHEN
    texas_path = sue_person._get_econ_path([idearoot, texas_text])
    dallas_path = sue_person._get_econ_path([idearoot, texas_text, dallas_text])
    elpaso_path = sue_person._get_econ_path([idearoot, texas_text, elpaso_text])
    kern_path = sue_person._get_econ_path(
        [idearoot, texas_text, elpaso_text, kern_text]
    )

    # THEN
    idearoot_dir = f"{sue_person._econs_dir}/idearoot"
    assert texas_path == f"{idearoot_dir}/{texas_text}"
    assert dallas_path == f"{idearoot_dir}/{texas_text}/{dallas_text}"
    assert elpaso_path == f"{idearoot_dir}/{texas_text}/{elpaso_text}"
    assert kern_path == f"{idearoot_dir}/{texas_text}/{elpaso_text}/{kern_text}"


def test_PersonUnit_create_econ_dir_CreatesDir(worlds_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_person.create_core_dir_and_files()
    assert os_path_exists(sue_person._econs_dir)
    dallas_text = "dallas"
    dallas_list = [dallas_text]
    dallas_dir = sue_person._get_econ_path(dallas_list)
    print(f"{dallas_dir=}")
    assert os_path_exists(dallas_dir) == False

    # WHEN
    sue_person._create_econ_dir(dallas_text)

    # THEN
    print(f"{dallas_dir=}")
    assert os_path_exists(dallas_dir)


def test_PersonUnit_create_econunit_CreatesEconUnit(worlds_dir_setup_cleanup):
    # GIVEN
    pound_text = "#"
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text, _road_delimiter=pound_text)
    sue_person.create_core_dir_and_files()
    sue_gut_agenda = sue_person.get_gut_file_agenda()
    texas_text = "Texas"
    texas_road = sue_gut_agenda.make_l1_road(texas_text)
    dallas_text = "dallas"
    dallas_road = sue_gut_agenda.make_road(texas_road, dallas_text)
    dallas_dir = sue_person._create_econ_dir(dallas_road)
    dallas_db_path = f"{dallas_dir}/treasury.db"
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
    assert dallas_econunit.econ_id == dallas_text
    assert dallas_econunit.econ_dir == dallas_dir
    assert dallas_econunit._manager_person_id == sue_text
    assert dallas_econunit._road_delimiter == sue_person._road_delimiter


def test_PersonUnit_create_person_econunits_RaisesErrorWhen__econs_justified_IsFalse(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_person.create_core_dir_and_files()
    sue_gut_agenda = sue_person.get_gut_file_agenda()
    sue_gut_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_gut_agenda.make_l1_road(texas_text)
    dallas_text = "dallas"
    dallas_road = sue_gut_agenda.make_road(texas_road, dallas_text)
    sue_gut_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_gut_agenda.add_idea(ideaunit_shop(dallas_text), texas_road)
    sue_gut_agenda.edit_idea_attr(texas_road, healerhold=healerhold_shop({sue_text}))
    sue_gut_agenda.edit_idea_attr(dallas_road, healerhold=healerhold_shop({sue_text}))
    sue_gut_agenda.set_agenda_metrics()
    assert sue_gut_agenda._econs_justified == False
    sue_person._save_agenda_to_gut_path(sue_gut_agenda)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.create_person_econunits(econ_exceptions=False)
    assert (
        str(excinfo.value)
        == f"Cannot set '{sue_text}' gut agenda econunits because 'AgendaUnit._econs_justified' is False."
    )


def test_PersonUnit_create_person_econunits_RaisesErrorWhen__econs_buildable_IsFalse(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_person.create_core_dir_and_files()
    sue_gut_agenda = sue_person.get_gut_file_agenda()
    sue_gut_agenda.add_partyunit(sue_text)
    texas_text = "Tex/as"
    texas_road = sue_gut_agenda.make_l1_road(texas_text)
    sue_gut_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_gut_agenda.edit_idea_attr(texas_road, healerhold=healerhold_shop({sue_text}))
    sue_gut_agenda.set_agenda_metrics()
    assert sue_gut_agenda._econs_justified
    assert sue_gut_agenda._econs_buildable == False
    sue_person._save_agenda_to_gut_path(sue_gut_agenda)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_person.create_person_econunits()
    assert (
        str(excinfo.value)
        == f"Cannot set '{sue_text}' gut agenda econunits because 'AgendaUnit._econs_buildable' is False."
    )


def test_PersonUnit_create_person_econunits_CreatesEconUnits(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_person.create_core_dir_and_files()
    sue_gut_agenda = sue_person.get_gut_file_agenda()
    sue_gut_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_gut_agenda.make_l1_road(texas_text)
    sue_gut_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    elpaso_text = "el paso"
    dallas_road = sue_gut_agenda.make_road(texas_road, dallas_text)
    elpaso_road = sue_gut_agenda.make_road(texas_road, elpaso_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_gut_agenda.add_idea(dallas_idea, texas_road)
    sue_gut_agenda.add_idea(elpaso_idea, texas_road)
    sue_gut_agenda.set_agenda_metrics()
    # display_agenda(sue_gut_agenda, mode="Econ").show()
    sue_person._save_agenda_to_gut_path(sue_gut_agenda)

    dallas_dir = sue_person._create_econ_dir(dallas_road)
    elpaso_dir = sue_person._create_econ_dir(elpaso_road)
    dallas_db_path = f"{dallas_dir}/treasury.db"
    elpaso_db_path = f"{elpaso_dir}/treasury.db"
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


def test_PersonUnit_create_person_econunits_DeletesEconUnits(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_person.create_core_dir_and_files()
    sue_gut_agenda = sue_person.get_gut_file_agenda()
    sue_gut_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_gut_agenda.make_l1_road(texas_text)
    sue_gut_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    elpaso_text = "el paso"
    dallas_road = sue_gut_agenda.make_road(texas_road, dallas_text)
    elpaso_road = sue_gut_agenda.make_road(texas_road, elpaso_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_gut_agenda.add_idea(dallas_idea, texas_road)
    sue_gut_agenda.add_idea(elpaso_idea, texas_road)
    sue_gut_agenda.set_agenda_metrics()
    # display_agenda(sue_gut_agenda, mode="Econ").show()
    sue_person._save_agenda_to_gut_path(sue_gut_agenda)
    dallas_dir = sue_person._create_econ_dir(dallas_road)
    elpaso_dir = sue_person._create_econ_dir(elpaso_road)
    dallas_db_path = f"{dallas_dir}/treasury.db"
    elpaso_db_path = f"{elpaso_dir}/treasury.db"
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
    sue_gut_agenda.add_idea(elpaso_idea, texas_road)
    sue_gut_agenda.set_agenda_metrics()
    sue_person._save_agenda_to_gut_path(sue_gut_agenda)
    sue_person.create_person_econunits()

    # THEN
    assert sue_person._econ_objs.get(dallas_road) != None
    assert sue_person._econ_objs.get(elpaso_road) is None
    assert os_path_exists(dallas_db_path)
    assert os_path_exists(elpaso_db_path) == False
