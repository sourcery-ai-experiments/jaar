from src._road.road import default_road_delimiter_if_none
from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.world.world import WorldUnit, worldunit_shop
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)

from src.world.person import personunit_shop
from os import path as os_path
from pytest import raises as pytest_raises


def test_WorldUnit_exists(worlds_dir_setup_cleanup):
    music_text = "music"
    music_world = WorldUnit(world_id=music_text, worlds_dir=get_test_worlds_dir())
    assert music_world.world_id == music_text
    assert music_world.worlds_dir == get_test_worlds_dir()
    assert music_world._persons_dir is None
    assert music_world._journal_db is None
    assert music_world._personunits is None
    assert music_world._deals_dir is None
    assert music_world._dealunits is None
    assert music_world._max_deal_uid is None
    assert music_world._road_delimiter is None


def test_worldunit_shop_ReturnsWorldUnit(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"

    # WHEN
    music_world = worldunit_shop(
        world_id=music_text, worlds_dir=get_test_worlds_dir(), in_memory_journal_db=True
    )

    # THEN
    assert music_world.world_id == music_text
    assert music_world.worlds_dir == get_test_worlds_dir()
    assert music_world._persons_dir != None
    assert music_world._personunits == {}
    assert music_world._deals_dir != None
    assert music_world._dealunits == {}
    assert music_world._max_deal_uid == 0
    assert music_world._road_delimiter == default_road_delimiter_if_none()


def test_worldunit_shop_ReturnsWorldUnitWith_road_delimiter(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    slash_text = "/"

    # WHEN
    music_world = worldunit_shop(
        world_id=music_text,
        worlds_dir=get_test_worlds_dir(),
        in_memory_journal_db=True,
        _road_delimiter=slash_text,
    )

    # THEN
    assert music_world._road_delimiter == slash_text


def test_WorldUnit__set_world_dirs_SetsPersonDir(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_world = WorldUnit(world_id=music_text, worlds_dir=get_test_worlds_dir())
    x_world_dir = f"{get_test_worlds_dir()}/{music_text}"
    x_persons_dir = f"{x_world_dir}/persons"
    x_deals_dir = f"{x_world_dir}/deals"
    journal_file_name = "journal.db"
    journal_file_path = f"{x_world_dir}/{journal_file_name}"

    assert music_world._world_dir is None
    assert music_world._persons_dir is None
    assert music_world._deals_dir is None
    assert os_path.exists(x_world_dir) is False
    assert os_path.isdir(x_world_dir) is False
    assert os_path.exists(x_persons_dir) is False
    assert os_path.exists(x_deals_dir) is False
    assert os_path.exists(journal_file_path) is False

    # WHEN
    music_world._set_world_dirs()

    # THEN
    assert music_world._world_dir == x_world_dir
    assert music_world._persons_dir == x_persons_dir
    assert music_world._deals_dir == x_deals_dir
    assert os_path.exists(x_world_dir)
    assert os_path.isdir(x_world_dir)
    assert os_path.exists(x_persons_dir)
    assert os_path.exists(x_deals_dir)
    assert os_path.exists(journal_file_path)


def test_worldunit_shop_SetsWorldsDirs(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"

    # WHEN
    music_world = worldunit_shop(
        world_id=music_text, worlds_dir=get_test_worlds_dir(), in_memory_journal_db=True
    )

    # THEN
    assert music_world.world_id == music_text
    assert music_world._world_dir == f"{get_test_worlds_dir()}/{music_text}"
    assert music_world._persons_dir == f"{music_world._world_dir}/persons"


def test_WorldUnit__set_person_in_memory_CorrectlySetsPerson(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(
        world_id=music_text, worlds_dir=get_test_worlds_dir(), in_memory_journal_db=True
    )
    assert music_world._personunits == {}

    # WHEN
    luca_text = "Luca"
    luca_person = personunit_shop(person_id=luca_text)
    music_world._set_person_in_memory(personunit=luca_person)

    # THEN
    assert music_world._personunits != {}
    assert len(music_world._personunits) == 1
    assert music_world._personunits[luca_text] == luca_person
    assert music_world._world_dir == f"{get_test_worlds_dir()}/{music_text}"
    assert music_world._persons_dir == f"{music_world._world_dir}/persons"


def test_WorldUnit_personunit_exists_ReturnsCorrectBool(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(
        world_id=music_text, worlds_dir=get_test_worlds_dir(), in_memory_journal_db=True
    )
    assert music_world._personunits == {}

    # WHEN / THEN
    luca_text = "Luca"
    assert music_world.personunit_exists(luca_text) == False

    # WHEN / THEN
    luca_person = personunit_shop(person_id=luca_text)
    music_world._set_person_in_memory(personunit=luca_person)
    assert music_world.personunit_exists(luca_text)


def test_WorldUnit_add_personunit_CorrectlySetsPerson(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    slash_text = "/"
    music_world = worldunit_shop(
        music_text,
        get_test_worlds_dir(),
        _road_delimiter=slash_text,
        in_memory_journal_db=True,
    )
    luca_text = "Luca"
    luca_person_dir = f"{music_world._persons_dir}/{luca_text}"

    # WHEN
    music_world.add_personunit(luca_text)

    # THEN
    assert music_world._personunits[luca_text] != None
    print(f"{get_test_worlds_dir()=}")
    print(f"      {luca_person_dir=}")
    music_world_luca_dir = music_world._personunits[luca_text].person_dir
    print(f"     {music_world_luca_dir=}")
    assert music_world._personunits[luca_text].person_dir == luca_person_dir
    assert music_world._personunits[luca_text]._road_delimiter == slash_text
    luca_person_obj = personunit_shop(
        person_id=luca_text,
        world_id=music_text,
        worlds_dir=music_world.worlds_dir,
        _road_delimiter=slash_text,
    )
    assert music_world._personunits[luca_text].worlds_dir == luca_person_obj.worlds_dir
    assert music_world._personunits[luca_text].world_id == luca_person_obj.world_id
    assert music_world._personunits[luca_text] == luca_person_obj


def test_WorldUnit_add_personunit_RaisesErrorIfPersonExists(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(
        world_id=music_text, worlds_dir=get_test_worlds_dir(), in_memory_journal_db=True
    )
    luca_text = "Luca"
    luca_person_dir = f"{music_world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(
        person_id=luca_text,
        world_id=music_text,
        worlds_dir=music_world.worlds_dir,
    )
    music_world.add_personunit(luca_text)
    assert music_world._personunits[luca_text] != None
    assert music_world._personunits[luca_text].person_dir == luca_person_dir
    assert music_world._personunits[luca_text] == luca_person_obj

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        music_world.add_personunit(luca_text)
    assert str(excinfo.value) == f"add_personunit fail: {luca_text} already exists"


def test_WorldUnit__set_person_in_memory_CorrectlyCreatesObj(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(
        world_id=music_text, worlds_dir=get_test_worlds_dir(), in_memory_journal_db=True
    )
    luca_text = "Luca"
    assert music_world.personunit_exists(luca_text) == False

    # WHEN
    luca_person_dir = f"{music_world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(
        person_id=luca_text,
        world_id=music_world.world_id,
        worlds_dir=music_world.worlds_dir,
    )
    music_world._set_person_in_memory(luca_person_obj)

    # THEN
    assert music_world.personunit_exists(luca_text)
    assert music_world._personunits.get(luca_text).person_dir == luca_person_dir
    assert music_world._personunits.get(luca_text) == luca_person_obj


def test_WorldUnit_get_personunit_ReturnsPerson(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(
        world_id=music_text, worlds_dir=get_test_worlds_dir(), in_memory_journal_db=True
    )
    luca_text = "Luca"
    luca_person_dir = f"{music_world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(
        person_id=luca_text,
        world_id=music_world.world_id,
        worlds_dir=music_world.worlds_dir,
    )
    music_world.add_personunit(luca_text)

    # WHEN
    luca_gotten_obj = music_world.get_personunit(luca_text)

    # THEN
    assert luca_gotten_obj != None
    assert luca_gotten_obj.person_dir == luca_person_dir
    assert luca_gotten_obj == luca_person_obj


def test_WorldUnit_get_personunit_ReturnsNone(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(
        world_id=music_text, worlds_dir=get_test_worlds_dir(), in_memory_journal_db=True
    )
    luca_text = "Luca"

    # WHEN
    luca_gotten_obj = music_world.get_personunit(luca_text)

    # THEN
    assert luca_gotten_obj is None


def test_WorldUnit_get_person_gut_ReturnsCorrectObj(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(
        music_text, get_test_worlds_dir(), in_memory_journal_db=True
    )
    luca_text = "Luca"
    music_world.add_personunit(luca_text)
    luca_person = music_world.get_personunit(luca_text)
    bob_text = "Bob"
    luca_gut = luca_person.get_gut_file_agenda()
    luca_gut.add_partyunit(bob_text)
    luca_person._save_gut_file(luca_gut)

    # WHEN
    gen_luca_gut = music_world.get_person_gut(luca_text)

    # THEN
    assert gen_luca_gut != None
    assert gen_luca_gut.get_party(bob_text) != None


def test_WorldUnit_set_all_econunits_contract_CorrectlySetsroles(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(
        music_text, get_test_worlds_dir(), in_memory_journal_db=True
    )
    luca_text = "Luca"
    todd_text = "Todd"
    luca_person = music_world.add_personunit(luca_text)
    todd_person = music_world.add_personunit(todd_text)
    luca_gut_agenda = luca_person.get_gut_file_agenda()
    todd_gut_agenda = todd_person.get_gut_file_agenda()

    luca_gut_agenda.add_partyunit(luca_text)
    luca_gut_agenda.add_partyunit(todd_text)
    todd_gut_agenda.add_partyunit(luca_text)
    todd_gut_agenda.add_partyunit(todd_text)
    texas_text = "Texas"
    texas_road = luca_gut_agenda.make_l1_road(texas_text)
    luca_gut_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    todd_gut_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = luca_gut_agenda.make_road(texas_road, dallas_text)
    dallas_healerhold = healerhold_shop({luca_text, todd_text})
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=dallas_healerhold)
    elpaso_text = "el paso"
    elpaso_road = luca_gut_agenda.make_road(texas_road, elpaso_text)
    elpaso_healerhold = healerhold_shop({luca_text})
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=elpaso_healerhold)

    luca_gut_agenda.add_idea(dallas_idea, texas_road)
    luca_gut_agenda.add_idea(elpaso_idea, texas_road)
    todd_gut_agenda.add_idea(dallas_idea, texas_road)
    todd_gut_agenda.add_idea(elpaso_idea, texas_road)
    # display_agenda(luca_gut_agenda.set_agenda_metrics(), mode="Econ").show()
    luca_person._save_gut_file(luca_gut_agenda)
    todd_person._save_gut_file(todd_gut_agenda)
    luca_person.create_person_econunits()
    todd_person.create_person_econunits()
    luca_dallas_econ = luca_person.get_econ(dallas_road)
    todd_dallas_econ = todd_person.get_econ(dallas_road)
    luca_dallas_econ.create_new_clerkunit(luca_text)
    luca_dallas_econ.create_new_clerkunit(todd_text)
    todd_dallas_econ.create_new_clerkunit(luca_text)
    todd_dallas_econ.create_new_clerkunit(todd_text)
    luca_dallas_luca_clerk = luca_dallas_econ.get_clerkunit(luca_text)
    luca_dallas_todd_clerk = luca_dallas_econ.get_clerkunit(todd_text)
    todd_dallas_luca_clerk = todd_dallas_econ.get_clerkunit(luca_text)
    todd_dallas_todd_clerk = todd_dallas_econ.get_clerkunit(todd_text)
    print(f"{luca_dallas_todd_clerk.get_role()._partys.keys()=}")
    assert todd_dallas_todd_clerk.open_role_file().get_party(luca_text) is None
    assert todd_dallas_luca_clerk.open_role_file().get_party(todd_text) is None
    assert luca_dallas_todd_clerk.open_role_file().get_party(luca_text) is None
    assert luca_dallas_luca_clerk.open_role_file().get_party(todd_text) is None

    # WHEN
    music_world.set_all_econunits_contract(luca_text)

    # THEN
    assert todd_dallas_todd_clerk.open_role_file().get_party(luca_text) is None
    assert luca_dallas_todd_clerk.open_role_file().get_party(luca_text) is None
    assert todd_dallas_luca_clerk.open_role_file().get_party(todd_text) != None
    assert luca_dallas_luca_clerk.open_role_file().get_party(todd_text) != None

    # WHEN
    music_world.set_all_econunits_contract(todd_text)

    # THEN
    assert todd_dallas_todd_clerk.open_role_file().get_party(luca_text) != None
    assert luca_dallas_todd_clerk.open_role_file().get_party(luca_text) != None
