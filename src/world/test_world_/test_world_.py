from src._prime.road import default_road_delimiter_if_none
from src.world.problem import problemunit_shop, healerlink_shop, marketlink_shop
from src.world.world import WorldUnit, worldunit_shop
from src.world.examples.world_env_kit import (
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)

from src.world.person import personunit_shop, problemunit_shop
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


def test_WorldUnit__set_person_in_memory_CorrectlyReplacesObj(worlds_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    world.set_personunit(luca_text)
    luca_person = world.get_personunit_from_memory(luca_text)
    luca_person.set_problemunit(problemunit_shop("Bob"))
    assert world.personunit_exists(luca_text)
    assert len(world._personunits.get(luca_text)._problems) == 1

    # WHEN
    luca_person_dir = f"{world._persons_dir}/{luca_text}"
    world._set_person_in_memory(
        personunit_shop(person_id=luca_text, person_dir=luca_person_dir)
    )

    # THEN
    assert len(world._personunits.get(luca_text)._problems) == 0


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


def test_WorldUnit_create_person_market_SetsCorrectObjs_healerlink_marketlink_marketunit(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    world = worldunit_shop(mark="Oregon", worlds_dir=get_test_worlds_dir())
    yao_text = "Yao"

    # WHEN
    knee_text = "knee"
    tim_text = "Tim"
    rest_text = "rest"
    world.create_person_market(
        person_id=yao_text,
        x_problem_id=knee_text,
        healer_id=tim_text,
        market_id=rest_text,
    )

    # THEN
    yao_personunit = world.get_personunit_from_memory(yao_text)
    tim_healerlink = healerlink_shop(tim_text)
    tim_healerlink.set_marketlink(marketlink_shop(rest_text))
    static_knee_problemunit = problemunit_shop(knee_text)
    static_knee_problemunit.set_healerlink(tim_healerlink)
    gen_knee_problemunit = yao_personunit.get_problem_obj(knee_text)
    assert gen_knee_problemunit._healerlinks == static_knee_problemunit._healerlinks
    assert gen_knee_problemunit == static_knee_problemunit
    assert yao_personunit.get_marketunit(rest_text) is None

    tim_personunit = world.get_personunit_from_memory(tim_text)
    rest_marketunit = tim_personunit.get_marketunit(rest_text)
    assert rest_marketunit.get_forum_agenda(yao_text) != None
    assert rest_marketunit.get_forum_agenda(tim_text) != None
