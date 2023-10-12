from src.world.world import WorldUnit, worldunit_shop
from src.world.examples.world_env_kit import get_test_worlds_dir
from src.world.person import personunit_shop


def test_worldunit_exists():
    dallas_text = "dallas"
    wx = WorldUnit(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert wx.mark == dallas_text
    assert wx.worlds_dir == get_test_worlds_dir()
    assert wx._persons_dir is None


def test_worldunit_shop_ReturnsWorldUnit():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    wx = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())

    # THEN
    assert wx.mark == dallas_text
    assert wx.worlds_dir == get_test_worlds_dir()
    assert wx._persons_obj == {}


def test_worldunit__set_world_dirs_SetsPersonDir():
    # GIVEN
    dallas_text = "dallas"
    wx = WorldUnit(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert wx._persons_dir is None

    # WHEN
    wx._set_world_dirs()

    # THEN
    assert wx._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert wx._persons_dir == f"{get_test_worlds_dir()}/{dallas_text}/persons"


def test_worldunit_shop_SetsWorldsDirs():
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    wx = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())

    # THEN
    assert wx.mark == dallas_text
    assert wx._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert wx._persons_dir == f"{wx._world_dir}/persons"


def test_worldunit__set_person_in_memory_CorrectlySetsPerson():
    # GIVEN
    dallas_text = "dallas"
    wx = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    assert wx._persons_obj == {}

    # WHEN
    luca_text = "Luca"
    luca_person = personunit_shop(name=luca_text)
    wx._set_person_in_memory(personunit=luca_person)

    # THEN
    assert wx._persons_obj != {}
    assert len(wx._persons_obj) == 1
    assert wx._persons_obj[luca_text] == luca_person
    assert wx._world_dir == f"{get_test_worlds_dir()}/{dallas_text}"
    assert wx._persons_dir == f"{wx._world_dir}/persons"


def test_worldunit__create_person_from_name_CorrectlySetsPerson():
    # GIVEN
    dallas_text = "dallas"
    wx = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    luca_person_dir = f"{wx._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(name=luca_text, person_dir=luca_person_dir)

    # WHEN
    wx._create_person_from_name(luca_text)

    # THEN
    assert wx._persons_obj[luca_text] != None
    assert wx._persons_obj[luca_text].person_dir == luca_person_dir
    assert wx._persons_obj[luca_text] == luca_person_obj


def test_worldunit_get_personunit_from_memory_CorrectlyReturnsPerson():
    # GIVEN
    dallas_text = "dallas"
    wx = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    luca_person_dir = f"{wx._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(name=luca_text, person_dir=luca_person_dir)
    wx._create_person_from_name(luca_text)

    # WHEN
    luca_gotten_obj = wx.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj != None
    assert luca_gotten_obj.person_dir == luca_person_dir
    assert luca_gotten_obj == luca_person_obj


def test_worldunit_get_personunit_from_memory_CorrectlyReturnsNone():
    # GIVEN
    dallas_text = "dallas"
    wx = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"

    # WHEN
    luca_gotten_obj = wx.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj is None
