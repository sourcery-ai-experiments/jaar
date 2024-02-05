from src._prime.road import default_road_delimiter_if_none
from src.x_econ.problem import problemunit_shop, healerlink_shop, marketlink_shop
from src.x_econ.econ import EconUnit, econunit_shop
from src.x_econ.examples.econ_env_kit import (
    get_test_econs_dir,
    econs_dir_setup_cleanup,
)

from src.x_econ.person import personunit_shop, problemunit_shop
from pytest import raises as pytest_raises


def test_EconUnit_exists(econs_dir_setup_cleanup):
    dallas_text = "dallas"
    x_econ = EconUnit(mark=dallas_text, econs_dir=get_test_econs_dir())
    assert x_econ.mark == dallas_text
    assert x_econ.econs_dir == get_test_econs_dir()
    assert x_econ._persons_dir is None
    assert x_econ._personunits is None
    assert x_econ._deals_dir is None
    assert x_econ._dealunits is None
    assert x_econ._max_deal_uid is None
    assert x_econ._road_delimiter is None


def test_econunit_shop_ReturnsEconUnit(econs_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    x_econ = econunit_shop(mark=dallas_text, econs_dir=get_test_econs_dir())

    # THEN
    assert x_econ.mark == dallas_text
    assert x_econ.econs_dir == get_test_econs_dir()
    assert x_econ._persons_dir != None
    assert x_econ._personunits == {}
    assert x_econ._deals_dir != None
    assert x_econ._dealunits == {}
    assert x_econ._max_deal_uid == 0
    assert x_econ._road_delimiter == default_road_delimiter_if_none()


def test_econunit_shop_ReturnsEconUnitWith_road_delimiter(econs_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    slash_text = "/"

    # WHEN
    x_econ = econunit_shop(
        mark=dallas_text, econs_dir=get_test_econs_dir(), _road_delimiter=slash_text
    )

    # THEN
    assert x_econ._road_delimiter == slash_text


def test_EconUnit__set_econ_dirs_SetsPersonDir(econs_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    x_econ = EconUnit(mark=dallas_text, econs_dir=get_test_econs_dir())
    assert x_econ._persons_dir is None

    # WHEN
    x_econ._set_econ_dirs()

    # THEN
    assert x_econ._econ_dir == f"{get_test_econs_dir()}/{dallas_text}"
    assert x_econ._persons_dir == f"{get_test_econs_dir()}/{dallas_text}/persons"
    assert x_econ._deals_dir == f"{get_test_econs_dir()}/{dallas_text}/deals"


def test_econunit_shop_SetsEconsDirs(econs_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"

    # WHEN
    x_econ = econunit_shop(mark=dallas_text, econs_dir=get_test_econs_dir())

    # THEN
    assert x_econ.mark == dallas_text
    assert x_econ._econ_dir == f"{get_test_econs_dir()}/{dallas_text}"
    assert x_econ._persons_dir == f"{x_econ._econ_dir}/persons"


def test_EconUnit__set_person_in_memory_CorrectlySetsPerson(econs_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    x_econ = econunit_shop(mark=dallas_text, econs_dir=get_test_econs_dir())
    assert x_econ._personunits == {}

    # WHEN
    luca_text = "Luca"
    luca_person = personunit_shop(person_id=luca_text)
    x_econ._set_person_in_memory(personunit=luca_person)

    # THEN
    assert x_econ._personunits != {}
    assert len(x_econ._personunits) == 1
    assert x_econ._personunits[luca_text] == luca_person
    assert x_econ._econ_dir == f"{get_test_econs_dir()}/{dallas_text}"
    assert x_econ._persons_dir == f"{x_econ._econ_dir}/persons"


def test_EconUnit_personunit_exists_ReturnsCorrectBool(econs_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    x_econ = econunit_shop(mark=dallas_text, econs_dir=get_test_econs_dir())
    assert x_econ._personunits == {}

    # WHEN / THEN
    luca_text = "Luca"
    assert x_econ.personunit_exists(luca_text) == False

    # WHEN / THEN
    luca_person = personunit_shop(person_id=luca_text)
    x_econ._set_person_in_memory(personunit=luca_person)
    assert x_econ.personunit_exists(luca_text)


def test_EconUnit_set_personunit_CorrectlySetsPerson(econs_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    slash_text = "/"
    x_econ = econunit_shop(dallas_text, get_test_econs_dir(), slash_text)
    luca_text = "Luca"
    luca_person_dir = f"{x_econ._persons_dir}/{luca_text}"

    # WHEN
    x_econ.set_personunit(luca_text)

    # THEN
    assert x_econ._personunits[luca_text] != None
    assert x_econ._personunits[luca_text].person_dir == luca_person_dir
    assert x_econ._personunits[luca_text]._road_delimiter == slash_text
    luca_person_obj = personunit_shop(
        person_id=luca_text, person_dir=luca_person_dir, _road_delimiter=slash_text
    )
    assert x_econ._personunits[luca_text] == luca_person_obj


def test_EconUnit_set_personunit_RaisesErrorIfPersonExists(econs_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    x_econ = econunit_shop(mark=dallas_text, econs_dir=get_test_econs_dir())
    luca_text = "Luca"
    luca_person_dir = f"{x_econ._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(person_id=luca_text, person_dir=luca_person_dir)
    x_econ.set_personunit(luca_text)
    assert x_econ._personunits[luca_text] != None
    assert x_econ._personunits[luca_text].person_dir == luca_person_dir
    assert x_econ._personunits[luca_text] == luca_person_obj

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_econ.set_personunit(luca_text)
    assert str(excinfo.value) == f"set_personunit fail: {luca_text} already exists"


def test_EconUnit__set_person_in_memory_CorrectlyCreatesObj(econs_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    x_econ = econunit_shop(mark=dallas_text, econs_dir=get_test_econs_dir())
    luca_text = "Luca"
    assert x_econ.personunit_exists(luca_text) == False

    # WHEN
    luca_person_dir = f"{x_econ._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(person_id=luca_text, person_dir=luca_person_dir)
    x_econ._set_person_in_memory(luca_person_obj)

    # THEN
    assert x_econ.personunit_exists(luca_text)
    assert x_econ._personunits.get(luca_text).person_dir == luca_person_dir
    assert x_econ._personunits.get(luca_text) == luca_person_obj


def test_EconUnit__set_person_in_memory_CorrectlyReplacesObj(econs_dir_setup_cleanup):
    # GIVEN
    dallas_text = "dallas"
    x_econ = econunit_shop(mark=dallas_text, econs_dir=get_test_econs_dir())
    luca_text = "Luca"
    x_econ.set_personunit(luca_text)
    luca_person = x_econ.get_personunit_from_memory(luca_text)
    luca_person.set_problemunit(problemunit_shop("Bob"))
    assert x_econ.personunit_exists(luca_text)
    assert len(x_econ._personunits.get(luca_text)._problems) == 1

    # WHEN
    luca_person_dir = f"{x_econ._persons_dir}/{luca_text}"
    x_econ._set_person_in_memory(
        personunit_shop(person_id=luca_text, person_dir=luca_person_dir)
    )

    # THEN
    assert len(x_econ._personunits.get(luca_text)._problems) == 0


def test_EconUnit_get_personunit_from_memory_ReturnsPerson(
    econs_dir_setup_cleanup,
):
    # GIVEN
    dallas_text = "dallas"
    x_econ = econunit_shop(mark=dallas_text, econs_dir=get_test_econs_dir())
    luca_text = "Luca"
    luca_person_dir = f"{x_econ._persons_dir}/{luca_text}"
    luca_person_obj = personunit_shop(person_id=luca_text, person_dir=luca_person_dir)
    x_econ.set_personunit(luca_text)

    # WHEN
    luca_gotten_obj = x_econ.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj != None
    assert luca_gotten_obj.person_dir == luca_person_dir
    assert luca_gotten_obj == luca_person_obj


def test_EconUnit_get_personunit_from_memory_ReturnsNone(
    econs_dir_setup_cleanup,
):
    # GIVEN
    dallas_text = "dallas"
    x_econ = econunit_shop(mark=dallas_text, econs_dir=get_test_econs_dir())
    luca_text = "Luca"

    # WHEN
    luca_gotten_obj = x_econ.get_personunit_from_memory(luca_text)

    # THEN
    assert luca_gotten_obj is None


def test_EconUnit_create_person_market_SetsCorrectObjs_healerlink_marketlink_marketunit(
    econs_dir_setup_cleanup,
):
    # GIVEN
    x_econ = econunit_shop(mark="Oregon", econs_dir=get_test_econs_dir())
    yao_text = "Yao"

    # WHEN
    knee_text = "knee"
    tim_text = "Tim"
    rest_text = "rest"
    x_econ.create_person_market(
        person_id=yao_text,
        x_problem_id=knee_text,
        healer_id=tim_text,
        market_id=rest_text,
    )

    # THEN
    yao_personunit = x_econ.get_personunit_from_memory(yao_text)
    tim_healerlink = healerlink_shop(tim_text)
    tim_healerlink.set_marketlink(marketlink_shop(rest_text))
    static_knee_problemunit = problemunit_shop(knee_text)
    static_knee_problemunit.set_healerlink(tim_healerlink)
    gen_knee_problemunit = yao_personunit.get_problem_obj(knee_text)
    assert gen_knee_problemunit._healerlinks == static_knee_problemunit._healerlinks
    assert gen_knee_problemunit == static_knee_problemunit
    assert yao_personunit.get_marketunit(rest_text) is None

    tim_personunit = x_econ.get_personunit_from_memory(tim_text)
    rest_marketunit = tim_personunit.get_marketunit(rest_text)
    assert rest_marketunit.get_forum_agenda(yao_text) != None
    assert rest_marketunit.get_forum_agenda(tim_text) != None
