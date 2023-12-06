from src.agenda.road import get_road
from src.world.concern import (
    CultureAddress,
    cultureaddress_shop,
    create_cultureaddress,
    ConcernUnit,
    concernunit_shop,
    create_concernunit,
    UrgeUnit,
    urgeunit_shop,
    create_urgeunit,
)
from src.world.examples.world_env_kit import get_test_worlds_dir
from src.world.person import personunit_shop
from pytest import raises as pytest_raises


def get_example_concernunit():
    luca_text = "Luca"
    texas_text = "Texas"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    food_text = "food"
    good_text = "good food"
    bad_text = "bad food"
    farm_text = "farm"
    well_text = "farm well"
    poor_text = "farm poorly"
    return create_concernunit(
        cultureaddress=texas_cultureaddress,
        concern=food_text,
        good=good_text,
        bad=bad_text,
        action=farm_text,
        positive=well_text,
        negative=poor_text,
    )


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


def test_CultureAddress_get_any_pid_ReturnsCorrectObj():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_address = create_cultureaddress(luca_text, texas_text)

    # WHEN
    any_pid = texas_address.get_any_pid()

    # THEN
    assert any_pid == luca_text


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
    assert farm_concernunit._action_positive is None
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
    farm_positive = get_road(farm_subject, "farm well")
    farm_negative = get_road(farm_subject, "farm poorly")

    # WHEN
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        concern_subject=food_subject,
        concern_good=food_good,
        concern_bad=food_bad,
        action_subject=farm_subject,
        action_positive=farm_positive,
        action_negative=farm_negative,
    )

    # THEN
    assert farm_concernunit._concern_subject == food_subject
    assert farm_concernunit._concern_good == food_good
    assert farm_concernunit._concern_bad == food_bad
    assert farm_concernunit._action_subject == farm_subject
    assert farm_concernunit._action_positive == farm_positive
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
    farm_positive = get_road(farm_subject, "farm well")
    farm_negative = get_road(farm_subject, "farm poorly")
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        concern_subject=food_subject,
        concern_good=food_good,
        concern_bad=food_bad,
        action_subject=farm_subject,
        action_positive=farm_positive,
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
    farm_positive = get_road(farm_subject, "farm well")
    farm_negative = get_road(farm_subject, "farm poorly")
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        concern_subject=food_subject,
        concern_good=food_good,
        concern_bad=food_bad,
        action_subject=farm_subject,
        action_positive=farm_positive,
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


def test_ConcernUnit_set_good_EmptySubjectRaisesErrorCorrectly():
    # GIVEN
    farm_concernunit = get_example_concernunit()
    texas_cultureaddress = farm_concernunit.cultureaddress
    food_subject = get_road(texas_cultureaddress.culture_qid, "food")
    food_good = get_road(food_subject, "good food")
    food_bad = get_road(food_subject, "bad food")

    # WHEN / THEN
    environ_road = get_road(texas_cultureaddress.culture_qid, "")
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_good(environ_road, food_good, food_bad)
    assert (
        str(excinfo.value)
        == f"ConcernUnit subject level 1 cannot be empty. ({environ_road})"
    )


def test_ConcernUnit_set_good_NotCultureRootRaisesSubjectErrorCorrectly():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    food_subject = get_road(texas_cultureaddress.culture_qid, "food")
    food_good = get_road(food_subject, "good food")
    food_bad = get_road(food_subject, "bad food")
    farm_subject = get_road(texas_cultureaddress.culture_qid, "farm")
    farm_positive = get_road(farm_subject, "farm well")
    farm_negative = get_road(farm_subject, "farm poorly")
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        concern_subject=food_subject,
        concern_good=food_good,
        concern_bad=food_bad,
        action_subject=farm_subject,
        action_positive=farm_positive,
        action_negative=farm_negative,
    )

    environ_text = "environment"
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


def test_ConcernUnit_set_good_RaisesDouble_culture_qid_SubjectErrorCorrectly():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    food_subject = get_road(texas_cultureaddress.culture_qid, "food")
    food_good = get_road(food_subject, "good food")
    food_bad = get_road(food_subject, "bad food")
    farm_subject = get_road(texas_cultureaddress.culture_qid, "farm")
    farm_positive = get_road(farm_subject, "farm well")
    farm_negative = get_road(farm_subject, "farm poorly")
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        concern_subject=food_subject,
        concern_good=food_good,
        concern_bad=food_bad,
        action_subject=farm_subject,
        action_positive=farm_positive,
        action_negative=farm_negative,
    )

    double_culture_qid = get_road(
        texas_cultureaddress.culture_qid, texas_cultureaddress.culture_qid
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_good(double_culture_qid, farm_positive, farm_negative)
    assert (
        str(excinfo.value)
        == f"ConcernUnit setting concern_subject '{double_culture_qid}' failed because first child node cannot be culture_qid as bug asumption check."
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
    farm_positive = get_road(farm_subject, "farm well")
    farm_negative = get_road(farm_subject, "farm poorly")
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        concern_subject=food_subject,
        concern_good=food_good,
        concern_bad=food_bad,
        action_subject=farm_subject,
        action_positive=farm_positive,
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
    assert farm_concernunit._action_positive == safe_road
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
    farm_positive = get_road(farm_subject, "farm well")
    farm_negative = get_road(farm_subject, "farm poorly")
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        concern_subject=food_subject,
        concern_good=food_good,
        concern_bad=food_bad,
        action_subject=farm_subject,
        action_positive=farm_positive,
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


def test_ConcernUnit_get_str_summary_ReturnsCorrectObj():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    food_text = "food"
    good_text = "good food"
    bad_text = "bad food"
    action_text = "farming"
    positive_text = "farm well"
    negative_text = "farm poorly"
    farm_concernunit = create_concernunit(
        texas_cultureaddress,
        concern=food_text,
        good=good_text,
        bad=bad_text,
        action=action_text,
        positive=positive_text,
        negative=negative_text,
    )

    # WHEN / THEN
    farm_summary_string = f"""
Within ['{luca_text}']'s {texas_text} culture subject: {food_text}
 {bad_text} is bad. 
 {good_text} is good.
 Within the action domain of '{action_text}'
 It is good to {positive_text}
 It is bad to {negative_text}"""
    assert farm_concernunit.get_str_summary() == farm_summary_string


def test_create_concernunit_CorrectlyCreatesObj():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    food_text = "food"
    good_text = "good food"
    bad_text = "bad food"
    farm_text = "farm"
    well_text = "farm well"
    poor_text = "farm poorly"

    # WHEN
    farm_concernunit = create_concernunit(
        cultureaddress=texas_cultureaddress,
        concern=food_text,
        good=good_text,
        bad=bad_text,
        action=farm_text,
        positive=well_text,
        negative=poor_text,
    )

    # THEN
    assert farm_concernunit.cultureaddress == texas_cultureaddress
    with_root_food_subject = get_road(texas_cultureaddress.culture_qid, food_text)
    with_root_food_good = get_road(with_root_food_subject, good_text)
    with_root_food_bad = get_road(with_root_food_subject, bad_text)
    assert farm_concernunit._concern_subject == with_root_food_subject
    assert farm_concernunit._concern_good == with_root_food_good
    assert farm_concernunit._concern_bad == with_root_food_bad

    with_root_farm_subject = get_road(texas_cultureaddress.culture_qid, farm_text)
    with_root_farm_positive = get_road(with_root_farm_subject, well_text)
    with_root_farm_negative = get_road(with_root_farm_subject, poor_text)
    assert farm_concernunit._action_subject == with_root_farm_subject
    assert farm_concernunit._action_positive == with_root_farm_positive
    assert farm_concernunit._action_negative == with_root_farm_negative


def test_UrgeUnit_exists():
    # GIVEN / WHEN
    farm_urgeunit = UrgeUnit()

    # THEN
    assert farm_urgeunit._concernunit is None
    assert farm_urgeunit._actor_pids is None
    assert farm_urgeunit._urger_pid is None


def test_urgeunit_shop_ReturnsCorrectObj():
    # GIVEN
    farm_concernunit = get_example_concernunit()

    # WHEN
    bob_text = "Bob"
    bob_dict = {bob_text: None}
    yao_text = "Yao"
    farm_urgeunit = urgeunit_shop(
        _concernunit=farm_concernunit, _actor_pids=bob_dict, _urger_pid=yao_text
    )

    # THEN
    assert farm_urgeunit._concernunit == farm_concernunit
    assert farm_urgeunit._actor_pids == bob_dict
    assert farm_urgeunit._urger_pid == yao_text


def test_create_urgeunit_ReturnsCorrectObj():
    # GIVEN
    farm_concernunit = get_example_concernunit()

    # WHEN
    bob_text = "Bob"
    farm_urgeunit = create_urgeunit(farm_concernunit, actor_id=bob_text)

    # THEN
    assert farm_urgeunit._concernunit == farm_concernunit
    bob_dict = {bob_text: None}
    assert farm_urgeunit._actor_pids == bob_dict
    assert farm_urgeunit._urger_pid == "Luca"


def test_UrgeUnit_add_actor_pid_CorrectlyChangesAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_urgeunit = create_urgeunit(get_example_concernunit(), actor_id=bob_text)
    assert len(farm_urgeunit._actor_pids) == 1

    # WHEN
    yao_text = "Yao"
    farm_urgeunit.add_actor_id(pid=yao_text)

    # THEN
    actor_pid_dict = {bob_text: None, yao_text: None}
    assert farm_urgeunit._actor_pids == actor_pid_dict


def test_UrgeUnit_get_str_summary_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    farm_urgeunit = create_urgeunit(get_example_concernunit(), bob_text)
    yao_text = "Yao"
    farm_urgeunit.add_actor_id(yao_text)

    texas_text = "Texas"
    luca_text = "Luca"
    food_text = "food"
    good_text = "good food"
    bad_text = "bad food"
    action_text = "farm"
    positive_text = "farm well"
    negative_text = "farm poorly"

    # WHEN / THEN
    farm_summary_string = f"""
Within ['{luca_text}']'s {texas_text} culture subject: {food_text}
 {bad_text} is bad. 
 {good_text} is good.
 Within the action domain of '{action_text}'
 It is good to {positive_text}
 It is bad to {negative_text}
 ['{bob_text}', '{yao_text}'] are asked to be good."""
    assert farm_urgeunit.get_str_summary() == farm_summary_string
