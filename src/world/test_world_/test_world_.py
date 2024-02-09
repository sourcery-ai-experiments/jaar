from src._prime.road import default_road_delimiter_if_none
from src.world.world import WorldUnit, worldunit_shop
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)

from src.world.person import personunit_shop
from pytest import raises as pytest_raises


def test_WorldUnit_exists(worlds_dir_setup_cleanup):
    dallas_text = "dallas"
    world = WorldUnit(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert world.mark == dallas_text
    assert world.worlds_dir == get_test_worlds_dir()
    assert world._persons_dir is None
    assert world._personunits is None
    assert world._deals_dir is None
    assert world._dealunits is None
    assert world._max_deal_uid is None
    assert world._road_delimiter is None


def test_worldunit_shop_ReturnsWorldUnit(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())

    # THEN
    assert world.mark == dallas_text
    assert world.worlds_dir == get_test_worlds_dir()
    assert world._persons_dir != None
    assert world._personunits == {}
    assert world._deals_dir != None
    assert world._dealunits == {}
    assert world._max_deal_uid == 0
    assert world._road_delimiter == default_road_delimiter_if_none()


def test_worldunit_shop_ReturnsWorldUnitWith_road_delimiter(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    slash_text = "/"

    # WHEN
    world = worldunit_shop(
        mark=dallas_text, worlds_dir=get_test_worlds_dir(), _road_delimiter=slash_text
    )

    # THEN
    assert world._road_delimiter == slash_text


def test_WorldUnit__set_world_dirs_SetsPersonDir(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    world = WorldUnit(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert world._persons_dir is None

    # WHEN
    world._set_world_dirs()

    # THEN
    assert world._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert world._persons_dir == f"{get_test_worlds_dir()}/{dallas_text}/persons"
    assert world._deals_dir == f"{get_test_worlds_dir()}/{dallas_text}/deals"


def test_worldunit_shop_SetsWorldsDirs(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())

    # THEN
    assert world.mark == dallas_text
    assert world._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert world._persons_dir == f"{world._world_dir}/persons"


def test_WorldUnit__set_person_in_memory_CorrectlySetsPerson(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert world._personunits == {}

    # WHEN
    luca_text = "Luca"
    luca_person = personunit_shop(person_id=luca_text)
    world._set_person_in_memory(personunit=luca_person)

    # THEN
    assert world._personunits != {}
    assert len(world._personunits) == 1
    assert world._personunits[luca_text] == luca_person
    assert world._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert world._persons_dir == f"{world._world_dir}/persons"


def test_WorldUnit_personunit_exists_ReturnsCorrectBool(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert world._personunits == {}

    # WHEN / THEN
    luca_text = "Luca"
    assert world.personunit_exists(luca_text) == False

    # WHEN / THEN
    luca_person = personunit_shop(person_id=luca_text)
    world._set_person_in_memory(personunit=luca_person)
    assert world.personunit_exists(luca_text)


def test_WorldUnit_set_personunit_CorrectlySetsPerson(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    slash_text = "/"
    world = worldunit_shop(dallas_text, get_test_worlds_dir(), slash_text)
    luca_text = "Luca"
    luca_person_dir = f"{world._persons_dir}/{luca_text}"

    # WHEN
    world.set_personunit(luca_text)

    # THEN
    assert world._personunits[luca_text] != None
    assert world._personunits[luca_text].person_dir == luca_person_dir
    assert world._personunits[luca_text]._road_delimiter == slash_text
    luca_person_obj = personunit_shop(
        person_id=luca_text, person_dir=luca_person_dir, _road_delimiter=slash_text
    )
    assert world._personunits[luca_text] == luca_person_obj


def test_WorldUnit_set_personunit_RaisesErrorIfPersonExists(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    luca_person_dir = f"{world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(person_id=luca_text, person_dir=luca_person_dir)
    world.set_personunit(luca_text)
    assert world._personunits[luca_text] != None
    assert world._personunits[luca_text].person_dir == luca_person_dir
    assert world._personunits[luca_text] == luca_person_obj

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        world.set_personunit(luca_text)
    assert str(excinfo.value) == f"set_personunit fail: {luca_text} already exists"


def test_WorldUnit__set_person_in_memory_CorrectlyCreatesObj(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    assert world.personunit_exists(luca_text) == False

    # WHEN
    luca_person_dir = f"{world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(person_id=luca_text, person_dir=luca_person_dir)
    world._set_person_in_memory(luca_person_obj)

    # THEN
    assert world.personunit_exists(luca_text)
    assert world._personunits.get(luca_text).person_dir == luca_person_dir
    assert world._personunits.get(luca_text) == luca_person_obj


# def test_WorldUnit__set_person_in_memory_CorrectlyReplacesObj(worlds_dir_setup_cleanup):
#     # GIVEN
#     dallas_text = "dallas"
#     world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
#     luca_text = "Luca"
#     world.set_personunit(luca_text)
#     luca_person = world.get_personunit_from_memory(luca_text)
#     assert world.personunit_exists(luca_text)

#     # WHEN
#     luca_person_dir = f"{world._persons_dir}/{luca_text}"
#     world._set_person_in_memory(
#         personunit_shop(person_id=luca_text, person_dir=luca_person_dir)
#     )


def test_WorldUnit_get_personunit_from_memory_ReturnsPerson(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    dallas_text = "dallas"
    world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    luca_person_dir = f"{world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(person_id=luca_text, person_dir=luca_person_dir)
    world.set_personunit(luca_text)

    # WHEN
    luca_gotten_obj = world.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj != None
    assert luca_gotten_obj.person_dir == luca_person_dir
    assert luca_gotten_obj == luca_person_obj


def test_WorldUnit_get_personunit_from_memory_ReturnsNone(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    dallas_text = "dallas"
    world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"

    # WHEN
    luca_gotten_obj = world.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj is None
