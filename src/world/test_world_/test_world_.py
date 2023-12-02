from src.world.world import WorldUnit, worldunit_shop
from src.world.examples.world_env_kit import get_test_worlds_dir
from src.world.person import personunit_shop, painunit_shop
from pytest import raises as pytest_raises


def test_worldunit_exists():
    dallas_text = "dallas"
    x_world = WorldUnit(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert x_world.mark == dallas_text
    assert x_world.worlds_dir == get_test_worlds_dir()
    assert x_world._persons_dir is None


def test_worldunit_shop_ReturnsWorldUnit():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())

    # THEN
    assert x_world.mark == dallas_text
    assert x_world.worlds_dir == get_test_worlds_dir()
    assert x_world._personunits == {}


def test_worldunit__set_world_dirs_SetsPersonDir():
    # GIVEN
    dallas_text = "dallas"
    x_world = WorldUnit(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert x_world._persons_dir is None

    # WHEN
    x_world._set_world_dirs()

    # THEN
    assert x_world._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert x_world._persons_dir == f"{get_test_worlds_dir()}/{dallas_text}/persons"


def test_worldunit_shop_SetsWorldsDirs():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())

    # THEN
    assert x_world.mark == dallas_text
    assert x_world._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert x_world._persons_dir == f"{x_world._world_dir}/persons"


def test_worldunit__set_person_in_memory_CorrectlySetsPerson():
    # GIVEN
    dallas_text = "dallas"
    x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert x_world._personunits == {}

    # WHEN
    luca_text = "Luca"
    luca_person = personunit_shop(pid=luca_text)
    x_world._set_person_in_memory(personunit=luca_person)

    # THEN
    assert x_world._personunits != {}
    assert len(x_world._personunits) == 1
    assert x_world._personunits[luca_text] == luca_person
    assert x_world._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert x_world._persons_dir == f"{x_world._world_dir}/persons"


def test_worldunit_personunit_exists_ReturnsCorrectBool():
    # GIVEN
    dallas_text = "dallas"
    x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert x_world._personunits == {}

    # WHEN / THEN
    luca_text = "Luca"
    assert x_world.personunit_exists(luca_text) == False

    # WHEN / THEN
    luca_person = personunit_shop(pid=luca_text)
    x_world._set_person_in_memory(personunit=luca_person)
    assert x_world.personunit_exists(luca_text)


def test_worldunit_add_personunit_CorrectlySetsPerson():
    # GIVEN
    dallas_text = "dallas"
    x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    luca_person_dir = f"{x_world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(pid=luca_text, person_dir=luca_person_dir)

    # WHEN
    x_world.add_personunit(luca_text)

    # THEN
    assert x_world._personunits[luca_text] != None
    assert x_world._personunits[luca_text].person_dir == luca_person_dir
    assert x_world._personunits[luca_text] == luca_person_obj


def test_worldunit_add_personunit_RaisesErrorIfPersonExists():
    # GIVEN
    dallas_text = "dallas"
    x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    luca_person_dir = f"{x_world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(pid=luca_text, person_dir=luca_person_dir)
    x_world.add_personunit(luca_text)
    assert x_world._personunits[luca_text] != None
    assert x_world._personunits[luca_text].person_dir == luca_person_dir
    assert x_world._personunits[luca_text] == luca_person_obj

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_world.add_personunit(luca_text)
    assert str(excinfo.value) == f"add_personunit fail: {luca_text} already exists"


def test_worldunit_set_personunit_CorrectlyCreatesObj():
    # GIVEN
    dallas_text = "dallas"
    x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    assert x_world.personunit_exists(luca_text) == False

    # WHEN
    luca_person_dir = f"{x_world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(pid=luca_text, person_dir=luca_person_dir)
    x_world.set_personunit(luca_person_obj)

    # THEN
    assert x_world.personunit_exists(luca_text)
    assert x_world._personunits.get(luca_text).person_dir == luca_person_dir
    assert x_world._personunits.get(luca_text) == luca_person_obj


def test_worldunit_set_personunit_CorrectlyReplacesObj():
    # GIVEN
    dallas_text = "dallas"
    x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    x_world.add_personunit(luca_text)
    luca_person = x_world.get_personunit_from_memory(luca_text)
    luca_person.set_painunit(painunit_shop("Bob"))
    assert x_world.personunit_exists(luca_text)
    assert len(x_world._personunits.get(luca_text)._pains) == 1

    # WHEN
    luca_person_dir = f"{x_world._persons_dir}/{luca_text}"
    x_world.set_personunit(personunit_shop(pid=luca_text, person_dir=luca_person_dir))

    # THEN
    assert len(x_world._personunits.get(luca_text)._pains) == 0


def test_worldunit_get_personunit_from_memory_CorrectlyReturnsPerson():
    # GIVEN
    dallas_text = "dallas"
    x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    luca_person_dir = f"{x_world._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(pid=luca_text, person_dir=luca_person_dir)
    x_world.add_personunit(luca_text)

    # WHEN
    luca_gotten_obj = x_world.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj != None
    assert luca_gotten_obj.person_dir == luca_person_dir
    assert luca_gotten_obj == luca_person_obj


def test_worldunit_get_personunit_from_memory_CorrectlyReturnsNone():
    # GIVEN
    dallas_text = "dallas"
    x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"

    # WHEN
    luca_gotten_obj = x_world.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj is None
