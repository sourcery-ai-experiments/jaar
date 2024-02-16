from src._road.road import default_road_delimiter_if_none
from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.world.world import WorldUnit, worldunit_shop
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)

from src.world.person import personunit_shop
from pytest import raises as pytest_raises


def test_WorldUnit_exists(worlds_dir_setup_cleanup):
    music_text = "music"
    music_world = WorldUnit(world_id=music_text, worlds_dir=get_test_worlds_dir())
    assert music_world.world_id == music_text
    assert music_world.worlds_dir == get_test_worlds_dir()
    assert music_world._persons_dir is None
    assert music_world._personunits is None
    assert music_world._deals_dir is None
    assert music_world._dealunits is None
    assert music_world._max_deal_uid is None
    assert music_world._road_delimiter is None


def test_worldunit_shop_ReturnsWorldUnit(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"

    # WHEN
    music_world = worldunit_shop(world_id=music_text, worlds_dir=get_test_worlds_dir())

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
        _road_delimiter=slash_text,
    )

    # THEN
    assert music_world._road_delimiter == slash_text


def test_WorldUnit__set_world_dirs_SetsPersonDir(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_world = WorldUnit(world_id=music_text, worlds_dir=get_test_worlds_dir())
    assert music_world._persons_dir is None

    # WHEN
    music_world._set_world_dirs()

    # THEN
    assert music_world._world_dir == f"{get_test_worlds_dir()}/{music_text}"
    assert music_world._persons_dir == f"{get_test_worlds_dir()}/{music_text}/persons"
    assert music_world._deals_dir == f"{get_test_worlds_dir()}/{music_text}/deals"


def test_worldunit_shop_SetsWorldsDirs(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"

    # WHEN
    music_world = worldunit_shop(world_id=music_text, worlds_dir=get_test_worlds_dir())

    # THEN
    assert music_world.world_id == music_text
    assert music_world._world_dir == f"{get_test_worlds_dir()}/{music_text}"
    assert music_world._persons_dir == f"{music_world._world_dir}/persons"


def test_WorldUnit__set_person_in_memory_CorrectlySetsPerson(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(world_id=music_text, worlds_dir=get_test_worlds_dir())
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
    music_world = worldunit_shop(world_id=music_text, worlds_dir=get_test_worlds_dir())
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
    music_world = worldunit_shop(music_text, get_test_worlds_dir(), slash_text)
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
    music_world = worldunit_shop(world_id=music_text, worlds_dir=get_test_worlds_dir())
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
    music_world = worldunit_shop(world_id=music_text, worlds_dir=get_test_worlds_dir())
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


def test_WorldUnit_get_personunit_from_memory_ReturnsPerson(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(world_id=music_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    luca_person_dir = f"{music_world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(
        person_id=luca_text,
        world_id=music_world.world_id,
        worlds_dir=music_world.worlds_dir,
    )
    music_world.add_personunit(luca_text)

    # WHEN
    luca_gotten_obj = music_world.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj != None
    assert luca_gotten_obj.person_dir == luca_person_dir
    assert luca_gotten_obj == luca_person_obj


def test_WorldUnit_get_personunit_from_memory_ReturnsNone(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(world_id=music_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"

    # WHEN
    luca_gotten_obj = music_world.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj is None


def test_WorldUnit_get_person_gut_ReturnsCorrectObj(worlds_dir_setup_cleanup):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(music_text, get_test_worlds_dir())
    luca_text = "Luca"
    music_world.add_personunit(luca_text)
    luca_person = music_world.get_personunit_from_memory(luca_text)
    bob_text = "Bob"
    luca_gut = luca_person.get_gut_file_agenda()
    luca_gut.add_partyunit(bob_text)
    luca_person._save_agenda_to_gut_path(luca_gut)

    # WHEN
    gen_luca_gut = music_world.get_person_gut(luca_text)

    # THEN
    assert gen_luca_gut != None
    assert gen_luca_gut.get_party(bob_text) != None


def test_WorldUnit_set_person_econunits_contract_CorrectlySetsContracts(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    music_text = "music"
    music_world = worldunit_shop(music_text, get_test_worlds_dir())
    luca_text = "Luca"
    music_world.add_personunit(luca_text)

    sue_text = "Sue"
    sue_person = personunit_shop(person_id=sue_text)
    sue_person.create_core_dir_and_files()
    sue_gut_agenda = sue_person.get_gut_file_agenda()
    sue_gut_agenda.add_partyunit(sue_text)
    bob_text = "Bob"
    sue_gut_agenda.add_partyunit(bob_text)
    texas_text = "Texas"
    texas_road = sue_gut_agenda.make_l1_road(texas_text)
    sue_gut_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = sue_gut_agenda.make_road(texas_road, dallas_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    sue_gut_agenda.add_idea(dallas_idea, texas_road)
    elpaso_text = "el paso"
    elpaso_road = sue_gut_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_gut_agenda.add_idea(elpaso_idea, texas_road)
    # sue_gut_agenda.set_agenda_metrics()
    # display_agenda(sue_gut_agenda, mode="Econ").show()
    sue_person._save_agenda_to_gut_path(sue_gut_agenda)
    sue_person.create_person_econunits()
    dallas_econ = sue_person.get_econ(dallas_road)
    dallas_econ.create_new_clerkunit(sue_text)
    dallas_sue_clerk = dallas_econ.get_clerkunit(sue_text)
    assert dallas_sue_clerk.get_contract().get_party(bob_text) is None
    # assert elpaso_sue_clerk.get_contract().get_party(bob_text) is None

    # WHEN
    sue_person.set_person_econunits_contract()

    # THEN
    assert dallas_sue_clerk.get_contract().get_party(bob_text) != None
    elpaso_econ = sue_person.get_econ(elpaso_road)
    elpaso_econ.create_new_clerkunit(sue_text)
    elpaso_sue_clerk = dallas_econ.get_clerkunit(sue_text)
    assert elpaso_sue_clerk.get_contract().get_party(bob_text) != None
