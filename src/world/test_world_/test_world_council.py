from src.agenda.road import get_road
from src.culture.culture import cultureunit_shop
from src.culture.council import councilunit_shop
from src.world.world import (
    worldunit_shop,
    CultureAddress,
    cultureaddress_shop,
    create_cultureaddress,
    ConcernUnit,
    concernunit_shop,
)
from src.world.examples.world_env_kit import get_test_worlds_dir
from src.world.person import personunit_shop
from pytest import raises as pytest_raises


def test_CultureAddress_exists():
    # GIVEN
    luca_text = "Luca"
    luca_dict = {luca_text: 0}
    texas_text = "Texas"

    # WHEN
    texas_address = CultureAddress(person_ids=luca_dict, culture_qid=texas_text)

    # THEN
    assert texas_address.culture_qid == texas_text
    assert texas_address.person_ids == luca_dict


def test_cultureaddress_shop_ReturnsCorrectObject():
    # GIVEN
    luca_text = "Luca"
    luca_dict = {luca_text: 0}
    texas_text = "Texas"

    # WHEN
    texas_address = cultureaddress_shop(person_ids=luca_dict, culture_qid=texas_text)

    # THEN
    assert texas_address.culture_qid == texas_text
    assert texas_address.person_ids == luca_dict


def test_CultureAddress_add_person_id_CorrectChangesAttribute():
    # GIVEN
    texas_text = "Texas"
    texas_address = cultureaddress_shop(culture_qid=texas_text)
    assert texas_address.person_ids == {}

    # WHEN
    luca_text = "Luca"
    texas_address.add_person_id(luca_text)

    # THEN
    luca_dict = {luca_text: 0}
    assert texas_address.person_ids == luca_dict


def test_create_cultureaddress_ReturnsCorrectObj():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"

    # WHEN
    texas_address = create_cultureaddress(luca_text, texas_text)

    # THEN
    luca_dict = {luca_text: 0}
    assert texas_address.culture_qid == texas_text
    assert texas_address.person_ids == luca_dict


def test_worldunit_add_cultural_connection_CorrectlyCreatesObj():
    # GIVEN
    dallas_text = "dallas"
    x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    x_world.add_personunit(luca_text)
    luca_person = x_world.get_personunit_from_memory(luca_text)
    texas_text = "Texas"
    luca_person.add_cultureunit(texas_text)
    texas_culture = luca_person.get_cultureunit(texas_text)
    kari_text = "kari"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    assert texas_culture._councilunits.get(kari_text) is None
    assert x_world.personunit_exists(kari_text) == False

    # WHEN
    x_world.add_cultural_connection(texas_cultureaddress, kari_text)

    # THEN
    assert x_world.personunit_exists(kari_text)
    assert texas_culture._councilunits.get(kari_text) != None


def test_ConcernUnit_exists():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)

    # WHEN
    farm_concernunit = ConcernUnit(texas_cultureaddress)

    # THEN
    assert farm_concernunit._concern_subject is None
    assert farm_concernunit._concern_good is None
    assert farm_concernunit._concern_bad is None
    assert farm_concernunit._action_subject is None
    assert farm_concernunit._action_postive is None
    assert farm_concernunit._action_negative is None
    assert farm_concernunit.cultureaddress == texas_cultureaddress


def test_concernunit_shop_ReturnsCorrectObj():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    food_subject = get_road(texas_cultureaddress.culture_qid, "food")
    food_good = get_road(food_subject, "good food")
    food_bad = get_road(food_subject, "bad food")
    farm_subject = get_road(texas_cultureaddress.culture_qid, "farm")
    farm_postive = get_road(farm_subject, "farm well")
    farm_negative = get_road(farm_subject, "farm poorly")

    # WHEN
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        concern_subject=food_subject,
        concern_good=food_good,
        concern_bad=food_bad,
        action_subject=farm_subject,
        action_postive=farm_postive,
        action_negative=farm_negative,
    )

    # THEN
    assert farm_concernunit._concern_subject == food_subject
    assert farm_concernunit._concern_good == food_good
    assert farm_concernunit._concern_bad == food_bad
    assert farm_concernunit._action_subject == farm_subject
    assert farm_concernunit._action_postive == farm_postive
    assert farm_concernunit._action_negative == farm_negative
    assert farm_concernunit.cultureaddress == texas_cultureaddress


def test_ConcernUnit_set_good_SetsAttributesCorrectly():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    food_subject = get_road(texas_cultureaddress.culture_qid, "food")
    food_good = get_road(food_subject, "good food")
    food_bad = get_road(food_subject, "bad food")
    farm_subject = get_road(texas_cultureaddress.culture_qid, "farm")
    farm_postive = get_road(farm_subject, "farm well")
    farm_negative = get_road(farm_subject, "farm poorly")
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        concern_subject=food_subject,
        concern_good=food_good,
        concern_bad=food_bad,
        action_subject=farm_subject,
        action_postive=farm_postive,
        action_negative=farm_negative,
    )

    # WHEN
    environ_road = get_road(texas_cultureaddress.culture_qid, "environment")
    soil_road = get_road(environ_road, "soil")
    unsafe_road = get_road(soil_road, "unsafe soil")
    fertile_road = get_road(soil_road, "fertile soil")
    farm_concernunit.set_good(soil_road, fertile_road, unsafe_road)

    # THEN
    assert farm_concernunit._concern_subject == soil_road
    assert farm_concernunit._concern_good == fertile_road
    assert farm_concernunit._concern_bad == unsafe_road


def test_ConcernUnit_set_good_RaisesGoodBadErrorCorrectly():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    food_subject = get_road(texas_cultureaddress.culture_qid, "food")
    food_good = get_road(food_subject, "good food")
    food_bad = get_road(food_subject, "bad food")
    farm_subject = get_road(texas_cultureaddress.culture_qid, "farm")
    farm_postive = get_road(farm_subject, "farm well")
    farm_negative = get_road(farm_subject, "farm poorly")
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        concern_subject=food_subject,
        concern_good=food_good,
        concern_bad=food_bad,
        action_subject=farm_subject,
        action_postive=farm_postive,
        action_negative=farm_negative,
    )

    environ_road = get_road(texas_cultureaddress.culture_qid, "environment")
    soil_road = get_road(environ_road, "soil")
    correct_infertile_road = get_road(soil_road, "infertile soil")
    correct_fertile_road = get_road(soil_road, "fertile soil")
    error_infertile_road = get_road(food_subject, "infertile soil")
    error_fertile_road = get_road(food_subject, "fertile soil")

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_good(soil_road, correct_fertile_road, error_infertile_road)
    assert (
        str(excinfo.value)
        == f"ConcernUnit setting concern_bad '{error_infertile_road}' failed because subject road '{soil_road}' is not subroad"
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_good(soil_road, error_fertile_road, correct_infertile_road)
    assert (
        str(excinfo.value)
        == f"ConcernUnit setting concern_good '{error_fertile_road}' failed because subject road '{soil_road}' is not subroad"
    )


def test_ConcernUnit_set_good_RaisesSubjectErrorCorrectly():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    food_subject = get_road(texas_cultureaddress.culture_qid, "food")
    food_good = get_road(food_subject, "good food")
    food_bad = get_road(food_subject, "bad food")
    farm_subject = get_road(texas_cultureaddress.culture_qid, "farm")
    farm_postive = get_road(farm_subject, "farm well")
    farm_negative = get_road(farm_subject, "farm poorly")
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        concern_subject=food_subject,
        concern_good=food_good,
        concern_bad=food_bad,
        action_subject=farm_subject,
        action_postive=farm_postive,
        action_negative=farm_negative,
    )

    environ_text = "environment"
    environ_road = get_road(texas_cultureaddress.culture_qid, environ_text)
    incorrect_soil_road = get_road(environ_text, "soil")
    infertile_road = get_road(incorrect_soil_road, "infertile soil")
    fertile_road = get_road(incorrect_soil_road, "fertile soil")

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_good(incorrect_soil_road, fertile_road, infertile_road)
    assert (
        str(excinfo.value)
        == f"ConcernUnit setting concern_subject '{incorrect_soil_road}' failed because culture_qid is not first node."
    )


def test_ConcernUnit_set_action_SetsAttributesCorrectly():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    food_subject = get_road(texas_cultureaddress.culture_qid, "food")
    food_good = get_road(food_subject, "good food")
    food_bad = get_road(food_subject, "bad food")
    farm_subject = get_road(texas_cultureaddress.culture_qid, "farm")
    farm_postive = get_road(farm_subject, "farm well")
    farm_negative = get_road(farm_subject, "farm poorly")
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        concern_subject=food_subject,
        concern_good=food_good,
        concern_bad=food_bad,
        action_subject=farm_subject,
        action_postive=farm_postive,
        action_negative=farm_negative,
    )

    # WHEN
    home_road = get_road(texas_cultureaddress.culture_qid, "home")
    cook_road = get_road(home_road, "cook")
    unsafe_road = get_road(cook_road, "unsafe cook")
    safe_road = get_road(cook_road, "safe cook")
    farm_concernunit.set_action(cook_road, safe_road, unsafe_road)

    # THEN
    assert farm_concernunit._action_subject == cook_road
    assert farm_concernunit._action_postive == safe_road
    assert farm_concernunit._action_negative == unsafe_road


def test_ConcernUnit_set_action_RaisesErrorCorrectly():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    food_subject = get_road(texas_cultureaddress.culture_qid, "food")
    food_good = get_road(food_subject, "good food")
    food_bad = get_road(food_subject, "bad food")
    farm_subject = get_road(texas_cultureaddress.culture_qid, "farm")
    farm_postive = get_road(farm_subject, "farm well")
    farm_negative = get_road(farm_subject, "farm poorly")
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        concern_subject=food_subject,
        concern_good=food_good,
        concern_bad=food_bad,
        action_subject=farm_subject,
        action_postive=farm_postive,
        action_negative=farm_negative,
    )

    environ_road = get_road(texas_cultureaddress.culture_qid, "environment")
    cook_road = get_road(environ_road, "cook")
    correct_unsafe_road = get_road(cook_road, "unsafe cook")
    correct_safe_road = get_road(cook_road, "safe cook")
    error_unsafe_road = get_road(food_subject, "unsafe cook")
    error_safe_road = get_road(food_subject, "safe cook")

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_action(cook_road, correct_safe_road, error_unsafe_road)
    assert (
        str(excinfo.value)
        == f"ConcernUnit setting action_negative '{error_unsafe_road}' failed because subject road '{cook_road}' is not subroad"
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_action(cook_road, error_safe_road, correct_unsafe_road)
    assert (
        str(excinfo.value)
        == f"ConcernUnit setting action_positive '{error_safe_road}' failed because subject road '{cook_road}' is not subroad"
    )
