from src.world.examples.examples import (
    get_farm_concernunit as examples_get_farm_concernunit,
    get_farm_urgeunit as examples_get_farm_urgeunit,
)
from src.agenda.road import get_road, get_node_delimiter, create_forkroad
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
from pytest import raises as pytest_raises


def test_CultureAddress_exists():
    # GIVEN
    luca_text = "Luca"
    luca_dict = {luca_text: 0}
    texas_text = "Texas"
    slash_text = "/"

    # WHEN
    texas_address = CultureAddress(
        person_ids=luca_dict, culture_id=texas_text, _road_node_delimiter=slash_text
    )

    # THEN
    assert texas_address.culture_id == texas_text
    assert texas_address._road_node_delimiter == slash_text
    assert texas_address.person_ids == luca_dict


def test_cultureaddress_shop_ReturnsCorrectObject():
    # GIVEN
    luca_text = "Luca"
    luca_dict = {luca_text: 0}
    texas_text = "Texas"
    slash_text = "/"

    # WHEN
    texas_address = cultureaddress_shop(
        person_ids=luca_dict, culture_id=texas_text, _road_node_delimiter=slash_text
    )

    # THEN
    assert texas_address.culture_id == texas_text
    assert texas_address.person_ids == luca_dict
    assert texas_address._road_node_delimiter == slash_text


def test_cultureaddress_shop_ReturnsCorrectObjectWithDefault_road_node_delimiter():
    # GIVEN
    luca_text = "Luca"
    luca_dict = {luca_text: 0}
    texas_text = "Texas"

    # WHEN
    texas_address = cultureaddress_shop(luca_dict, texas_text)

    # THEN
    assert texas_address._road_node_delimiter == get_node_delimiter()


def test_CultureAddress_add_person_id_CorrectChangesAttribute():
    # GIVEN
    texas_text = "Texas"
    texas_address = cultureaddress_shop(culture_id=texas_text)
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
    assert texas_address.culture_id == texas_text
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
    assert farm_concernunit.why is None
    assert farm_concernunit.action is None
    assert farm_concernunit.cultureaddress == texas_cultureaddress


def test_concernunit_shop_ReturnsCorrectObj():
    # GIVEN
    texas_cultureaddress = create_cultureaddress("Luca", "Texas")

    food_road = get_road(texas_cultureaddress.culture_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkroad = create_forkroad(food_road, good=farm_text, bad=cheap_text)

    cultivate_road = get_road(texas_cultureaddress.culture_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkroad = create_forkroad(cultivate_road, good=well_text, bad=poor_text)

    # WHEN
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        why=food_forkroad,
        action=cultivate_forkroad,
    )

    # THEN
    assert farm_concernunit.why == food_forkroad
    assert farm_concernunit.action == cultivate_forkroad
    assert farm_concernunit.cultureaddress == texas_cultureaddress
    assert farm_concernunit.get_road_node_delimiter() == get_node_delimiter(
        texas_cultureaddress._road_node_delimiter
    )


def test_ConcernUnit_set_why_SetsAttributesCorrectly():
    # GIVEN
    texas_cultureaddress = create_cultureaddress("Luca", "Texas")
    food_road = get_road(texas_cultureaddress.culture_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkroad = create_forkroad(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = get_road(texas_cultureaddress.culture_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkroad = create_forkroad(cultivate_road, good=well_text, bad=poor_text)
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        why=food_forkroad,
        action=cultivate_forkroad,
    )

    # WHEN
    environ_road = get_road(texas_cultureaddress.culture_id, "environment")
    soil_road = get_road(environ_road, "soil")
    unsafe_text = "unsafe soil"
    fertile_text = "fertile soil"
    soil_forkroad = create_forkroad(soil_road, good=fertile_text, bad=unsafe_text)

    farm_concernunit.set_why(soil_forkroad)

    # THEN
    assert farm_concernunit.why == soil_forkroad


def test_ConcernUnit_set_why_EmptySubjectRaisesErrorCorrectly():
    # GIVEN
    farm_concernunit = examples_get_farm_concernunit()
    texas_cultureaddress = farm_concernunit.cultureaddress
    food_road = get_road(texas_cultureaddress.culture_id, "")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkroad = create_forkroad(food_road, good=farm_text, bad=cheap_text)

    # WHEN / THEN
    environ_road = get_road(texas_cultureaddress.culture_id, "")
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_why(food_forkroad)
    assert (
        str(excinfo.value)
        == f"ConcernUnit subject level 1 cannot be empty. ({environ_road})"
    )


def test_ConcernUnit_set_why_NotCultureRootRaisesSubjectErrorCorrectly():
    # GIVEN
    texas_cultureaddress = create_cultureaddress("Luca", "Texas")
    food_road = get_road(texas_cultureaddress.culture_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkroad = create_forkroad(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = get_road(texas_cultureaddress.culture_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkroad = create_forkroad(cultivate_road, good=well_text, bad=poor_text)
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        why=food_forkroad,
        action=cultivate_forkroad,
    )

    environ_text = "environment"
    incorrect_soil_road = get_road(environ_text, "soil")
    infertile_text = "infertile soil"
    fertile_text = "fertile soil"
    # infertile_road = get_road(incorrect_soil_road, "infertile soil")
    # fertile_road = get_road(incorrect_soil_road, "fertile soil")
    incorrect_soil_forkroad = create_forkroad(
        incorrect_soil_road, good=fertile_text, bad=infertile_text
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_why(incorrect_soil_forkroad)
    assert (
        str(excinfo.value)
        == f"ConcernUnit setting concern_subject '{incorrect_soil_road}' failed because culture_id is not first node."
    )


def test_ConcernUnit_set_why_RaisesDouble_culture_id_SubjectErrorCorrectly():
    # GIVEN
    texas_cultureaddress = create_cultureaddress("Luca", "Texas")
    texas_culture_id = texas_cultureaddress.culture_id
    food_road = get_road(texas_culture_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkroad = create_forkroad(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = get_road(texas_culture_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkroad = create_forkroad(cultivate_road, good=well_text, bad=poor_text)
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        why=food_forkroad,
        action=cultivate_forkroad,
    )

    # WHEN / THEN
    double_culture_id = get_road(texas_culture_id, texas_culture_id)
    double_culture_forkroad = create_forkroad(double_culture_id, farm_text, cheap_text)
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_why(double_culture_forkroad)
    assert (
        str(excinfo.value)
        == f"ConcernUnit setting concern_subject '{double_culture_id}' failed because first child node cannot be culture_id as bug asumption check."
    )


def test_ConcernUnit_set_action_SetsAttributesCorrectly():
    # GIVEN
    texas_cultureaddress = create_cultureaddress("Luca", "Texas")
    texas_culture_id = texas_cultureaddress.culture_id
    food_road = get_road(texas_culture_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkroad = create_forkroad(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = get_road(texas_culture_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkroad = create_forkroad(cultivate_road, good=well_text, bad=poor_text)
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        why=food_forkroad,
        action=cultivate_forkroad,
    )

    # WHEN
    home_road = get_road(texas_cultureaddress.culture_id, "home")
    cook_road = get_road(home_road, "cook")
    cook_forkroad = create_forkroad(cook_road, good="unsafe cook", bad="safe cook")
    farm_concernunit.set_action(cook_forkroad)

    # THEN
    assert farm_concernunit.action == cook_forkroad


def test_ConcernUnit_get_str_summary_ReturnsCorrectObj():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    texas_culture_id = texas_cultureaddress.culture_id
    food_text = "food"
    food_road = get_road(texas_culture_id, food_text)
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkroad = create_forkroad(food_road, good=farm_text, bad=cheap_text)
    cultivate_text = "cultivate"
    cultivate_road = get_road(texas_culture_id, cultivate_text)
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkroad = create_forkroad(cultivate_road, good=well_text, bad=poor_text)
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        why=food_forkroad,
        action=cultivate_forkroad,
    )

    # WHEN / THEN
    farm_summary_string = f"""Within ['{luca_text}']'s {texas_text} culture subject: {food_text}
 {cheap_text} is bad. 
 {farm_text} is good.
 Within the action domain of '{cultivate_text}'
 It is good to {well_text}
 It is bad to {poor_text}"""
    assert farm_concernunit.get_str_summary() == farm_summary_string


def test_create_concernunit_CorrectlyCreatesObj():
    # GIVEN
    texas_cultureaddress = create_cultureaddress("Luca", "Texas")
    food_text = "food"
    food_road = get_road(texas_cultureaddress.culture_id, food_text)
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkroad = create_forkroad(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = get_road(texas_cultureaddress.culture_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkroad = create_forkroad(cultivate_road, good=well_text, bad=poor_text)
    farm_concernunit = concernunit_shop(
        texas_cultureaddress,
        why=food_forkroad,
        action=cultivate_forkroad,
    )

    # THEN
    assert farm_concernunit.cultureaddress == texas_cultureaddress
    assert farm_concernunit.why == food_forkroad
    assert farm_concernunit.action == cultivate_forkroad


def test_create_concernunit_CorrectlyCreatesObjWithCorrect_delimiter():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)

    enjoy_text = "enjoying life"
    food_text = "food"
    texas_no_food_road = get_road(enjoy_text, food_text)
    farm_text = "farm food"
    cheap_text = "cheap food"

    work_text = "working"
    cultivate_text = "cultivate"
    texas_no_cultivate_road = get_road(work_text, cultivate_text)
    well_text = "cultivate well"
    poor_text = "cultivate poorly"

    # WHEN
    farm_concernunit = create_concernunit(
        cultureaddress=texas_cultureaddress,
        why=texas_no_food_road,
        good=farm_text,
        bad=cheap_text,
        action=texas_no_cultivate_road,
        positive=well_text,
        negative=poor_text,
    )

    # THEN
    assert farm_concernunit.cultureaddress == texas_cultureaddress
    texas_yes_enjoy_road = get_road(texas_cultureaddress.culture_id, enjoy_text)
    texas_yes_food_road = get_road(texas_yes_enjoy_road, food_text)
    texas_yes_food_forkroad = create_forkroad(
        texas_yes_food_road, farm_text, cheap_text
    )
    assert farm_concernunit.why == texas_yes_food_forkroad

    texas_yes_work_road = get_road(texas_cultureaddress.culture_id, work_text)
    texas_yes_cultivate_road = get_road(texas_yes_work_road, cultivate_text)
    texas_yes_cultivate_forkroad = create_forkroad(
        texas_yes_cultivate_road, well_text, poor_text
    )
    assert farm_concernunit.action == texas_yes_cultivate_forkroad


def test_UrgeUnit_exists():
    # GIVEN / WHEN
    farm_urgeunit = UrgeUnit()

    # THEN
    assert farm_urgeunit._concernunit is None
    assert farm_urgeunit._actor_pids is None
    assert farm_urgeunit._actor_groups is None
    assert farm_urgeunit._urger_pid is None


def test_urgeunit_shop_ReturnsCorrectObj():
    # GIVEN
    farm_concernunit = examples_get_farm_concernunit()

    # WHEN
    bob_text = "Bob"
    bob_dict = {bob_text: None}
    yao_text = "Yao"
    aggie_text = "aggie"
    aggie_dict = {aggie_text: aggie_text}
    farm_urgeunit = urgeunit_shop(
        _concernunit=farm_concernunit,
        _actor_pids=bob_dict,
        _actor_groups=aggie_dict,
        _urger_pid=yao_text,
    )

    # THEN
    assert farm_urgeunit._concernunit == farm_concernunit
    assert farm_urgeunit._actor_pids == bob_dict
    assert farm_urgeunit._actor_groups == aggie_dict
    assert farm_urgeunit._urger_pid == yao_text


def test_UrgeUnit_add_actor_pid_CorrectlyChangesAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_urgeunit = create_urgeunit(examples_get_farm_concernunit(), actor_pid=bob_text)
    assert len(farm_urgeunit._actor_pids) == 1

    # WHEN
    yao_text = "Yao"
    farm_urgeunit.add_actor_pid(pid=yao_text)

    # THEN
    actor_pid_dict = {bob_text: None, yao_text: None}
    assert farm_urgeunit._actor_pids == actor_pid_dict


def test_UrgeUnit_add_groupbrand_CorrectlyChangesAttribute():
    # GIVEN
    bob_text = "Bob"
    bob_dict = {bob_text: None}
    farm_urgeunit = urgeunit_shop(examples_get_farm_concernunit(), _actor_pids=bob_dict)
    assert len(farm_urgeunit._actor_groups) == 0

    # WHEN
    swim_text = "swimmers"
    farm_urgeunit.add_actor_groupbrand(swim_text)

    # THEN
    swim_dict = {swim_text: swim_text}
    assert farm_urgeunit._actor_groups == swim_dict


def test_create_urgeunit_ReturnsCorrectObj():
    # GIVEN
    farm_concernunit = examples_get_farm_concernunit()

    # WHEN
    bob_text = "Bob"
    farm_urgeunit = create_urgeunit(farm_concernunit, actor_pid=bob_text)

    # THEN
    assert farm_urgeunit._concernunit == farm_concernunit
    bob_dict = {bob_text: None}
    assert farm_urgeunit._actor_pids == bob_dict
    bob_group_dict = {bob_text: bob_text}
    assert farm_urgeunit._actor_groups == bob_group_dict
    assert farm_urgeunit._urger_pid == "Luca"


def test_UrgeUnit_get_str_summary_ReturnsCorrectObj():
    # GIVEN
    farm_urgeunit = examples_get_farm_urgeunit()

    # WHEN
    generated_farm_str = farm_urgeunit.get_str_summary()

    # THEN
    bob_text = "Bob"
    real_text = "Real Farmers"
    yao_text = "Yao"
    texas_text = "Texas"
    luca_text = "Luca"
    food_text = "food"
    farm_text = "farm food"
    cheap_text = "cheap food"
    action_text = "cultivate"
    positive_text = "cultivate well"
    negative_text = "cultivate poorly"
    static_farm_string = f"""UrgeUnit: Within ['{luca_text}']'s {texas_text} culture subject: {food_text}
 {cheap_text} is bad. 
 {farm_text} is good.
 Within the action domain of '{action_text}'
 It is good to {positive_text}
 It is bad to {negative_text}
 ['{bob_text}', '{yao_text}'] are in groups ['{real_text}'] and are asked to be good."""

    assert generated_farm_str == static_farm_string
