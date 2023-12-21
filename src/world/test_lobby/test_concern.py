from src.world.examples.examples import (
    get_farm_concernunit as examples_get_farm_concernunit,
)
from src.agenda.road import get_road, get_node_delimiter, create_forkunit
from src.world.lobby import (
    EconomyAddress,
    economyaddress_shop,
    create_economyaddress,
    ConcernUnit,
    concernunit_shop,
    create_concernunit,
)
from pytest import raises as pytest_raises


def test_EconomyAddress_exists():
    # GIVEN
    luca_text = "Luca"
    luca_dict = {luca_text: 0}
    texas_text = "Texas"
    slash_text = "/"

    # WHEN
    texas_address = EconomyAddress(
        treasurer_pids=luca_dict, economy_id=texas_text, _road_node_delimiter=slash_text
    )

    # THEN
    assert texas_address.economy_id == texas_text
    assert texas_address._road_node_delimiter == slash_text
    assert texas_address.treasurer_pids == luca_dict


def test_economyaddress_shop_ReturnsCorrectObject():
    # GIVEN
    luca_text = "Luca"
    luca_dict = {luca_text: 0}
    texas_text = "Texas"
    slash_text = "/"

    # WHEN
    texas_address = economyaddress_shop(
        treasurer_pids=luca_dict, economy_id=texas_text, _road_node_delimiter=slash_text
    )

    # THEN
    assert texas_address.economy_id == texas_text
    assert texas_address.treasurer_pids == luca_dict
    assert texas_address._road_node_delimiter == slash_text


def test_economyaddress_shop_ReturnsCorrectObjectWithDefault_road_node_delimiter():
    # GIVEN
    luca_text = "Luca"
    luca_dict = {luca_text: 0}
    texas_text = "Texas"

    # WHEN
    texas_address = economyaddress_shop(luca_dict, texas_text)

    # THEN
    assert texas_address._road_node_delimiter == get_node_delimiter()


def test_EconomyAddress_add_treasurer_pid_CorrectChangesAttribute():
    # GIVEN
    texas_text = "Texas"
    texas_address = economyaddress_shop(economy_id=texas_text)
    assert texas_address.treasurer_pids == {}

    # WHEN
    luca_text = "Luca"
    texas_address.add_treasurer_pid(luca_text)

    # THEN
    luca_dict = {luca_text: 0}
    assert texas_address.treasurer_pids == luca_dict


def test_create_economyaddress_ReturnsCorrectObj():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"

    # WHEN
    texas_address = create_economyaddress(luca_text, texas_text)

    # THEN
    luca_dict = {luca_text: 0}
    assert texas_address.economy_id == texas_text
    assert texas_address.treasurer_pids == luca_dict


def test_EconomyAddress_get_any_pid_ReturnsCorrectObj():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_address = create_economyaddress(luca_text, texas_text)

    # WHEN
    any_pid = texas_address.get_any_pid()

    # THEN
    assert any_pid == luca_text


def test_ConcernUnit_exists():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_economyaddress = create_economyaddress(luca_text, texas_text)

    # WHEN
    farm_concernunit = ConcernUnit(texas_economyaddress)

    # THEN
    assert farm_concernunit.reason is None
    assert farm_concernunit.action is None
    assert farm_concernunit.economyaddress == texas_economyaddress


def test_concernunit_shop_ReturnsCorrectObj():
    # GIVEN
    texas_economyaddress = create_economyaddress("Luca", "Texas")

    food_road = get_road(texas_economyaddress.economy_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkunit = create_forkunit(food_road, good=farm_text, bad=cheap_text)

    cultivate_road = get_road(texas_economyaddress.economy_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkunit = create_forkunit(cultivate_road, good=well_text, bad=poor_text)

    # WHEN
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        reason=food_forkunit,
        action=cultivate_forkunit,
    )

    # THEN
    assert farm_concernunit.reason == food_forkunit
    assert farm_concernunit.action == cultivate_forkunit
    assert farm_concernunit.economyaddress == texas_economyaddress
    assert farm_concernunit.get_road_node_delimiter() == get_node_delimiter(
        texas_economyaddress._road_node_delimiter
    )


def test_ConcernUnit_set_reason_SetsAttributesCorrectly():
    # GIVEN
    texas_economyaddress = create_economyaddress("Luca", "Texas")
    food_road = get_road(texas_economyaddress.economy_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkunit = create_forkunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = get_road(texas_economyaddress.economy_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkunit = create_forkunit(cultivate_road, good=well_text, bad=poor_text)
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        reason=food_forkunit,
        action=cultivate_forkunit,
    )

    # WHEN
    environ_road = get_road(texas_economyaddress.economy_id, "environment")
    soil_road = get_road(environ_road, "soil")
    unsafe_text = "unsafe soil"
    fertile_text = "fertile soil"
    soil_forkunit = create_forkunit(soil_road, good=fertile_text, bad=unsafe_text)

    farm_concernunit.set_reason(soil_forkunit)

    # THEN
    assert farm_concernunit.reason == soil_forkunit


def test_ConcernUnit_set_reason_EmptySubjectRaisesErrorCorrectly():
    # GIVEN
    farm_concernunit = examples_get_farm_concernunit()
    texas_economyaddress = farm_concernunit.economyaddress
    food_road = get_road(texas_economyaddress.economy_id, "")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkunit = create_forkunit(food_road, good=farm_text, bad=cheap_text)

    # WHEN / THEN
    environ_road = get_road(texas_economyaddress.economy_id, "")
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_reason(food_forkunit)
    assert (
        str(excinfo.value)
        == f"ConcernUnit subject level 1 cannot be empty. ({environ_road})"
    )


def test_ConcernUnit_set_reason_NotEconomyRootRaisesSubjectErrorCorrectly():
    # GIVEN
    texas_economyaddress = create_economyaddress("Luca", "Texas")
    food_road = get_road(texas_economyaddress.economy_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkunit = create_forkunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = get_road(texas_economyaddress.economy_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkunit = create_forkunit(cultivate_road, good=well_text, bad=poor_text)
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        reason=food_forkunit,
        action=cultivate_forkunit,
    )

    environ_text = "environment"
    incorrect_soil_road = get_road(environ_text, "soil")
    infertile_text = "infertile soil"
    fertile_text = "fertile soil"
    # infertile_road = get_road(incorrect_soil_road, "infertile soil")
    # fertile_road = get_road(incorrect_soil_road, "fertile soil")
    incorrect_soil_forkunit = create_forkunit(
        incorrect_soil_road, good=fertile_text, bad=infertile_text
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_reason(incorrect_soil_forkunit)
    assert (
        str(excinfo.value)
        == f"ConcernUnit setting concern_subject '{incorrect_soil_road}' failed because economy_id is not first node."
    )


def test_ConcernUnit_set_reason_RaisesDouble_economy_id_SubjectErrorCorrectly():
    # GIVEN
    texas_economyaddress = create_economyaddress("Luca", "Texas")
    texas_economy_id = texas_economyaddress.economy_id
    food_road = get_road(texas_economy_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkunit = create_forkunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = get_road(texas_economy_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkunit = create_forkunit(cultivate_road, good=well_text, bad=poor_text)
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        reason=food_forkunit,
        action=cultivate_forkunit,
    )

    # WHEN / THEN
    double_economy_id = get_road(texas_economy_id, texas_economy_id)
    double_economy_forkunit = create_forkunit(double_economy_id, farm_text, cheap_text)
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_reason(double_economy_forkunit)
    assert (
        str(excinfo.value)
        == f"ConcernUnit setting concern_subject '{double_economy_id}' failed because first child node cannot be economy_id as bug asumption check."
    )


def test_ConcernUnit_set_action_SetsAttributesCorrectly():
    # GIVEN
    texas_economyaddress = create_economyaddress("Luca", "Texas")
    texas_economy_id = texas_economyaddress.economy_id
    food_road = get_road(texas_economy_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkunit = create_forkunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = get_road(texas_economy_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkunit = create_forkunit(cultivate_road, good=well_text, bad=poor_text)
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        reason=food_forkunit,
        action=cultivate_forkunit,
    )

    # WHEN
    home_road = get_road(texas_economyaddress.economy_id, "home")
    cook_road = get_road(home_road, "cook")
    cook_forkunit = create_forkunit(cook_road, good="unsafe cook", bad="safe cook")
    farm_concernunit.set_action(cook_forkunit)

    # THEN
    assert farm_concernunit.action == cook_forkunit


def test_ConcernUnit_get_str_summary_ReturnsCorrectObj():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_economyaddress = create_economyaddress(luca_text, texas_text)
    texas_economy_id = texas_economyaddress.economy_id
    food_text = "food"
    food_road = get_road(texas_economy_id, food_text)
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkunit = create_forkunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_text = "cultivate"
    cultivate_road = get_road(texas_economy_id, cultivate_text)
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkunit = create_forkunit(cultivate_road, good=well_text, bad=poor_text)
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        reason=food_forkunit,
        action=cultivate_forkunit,
    )

    # WHEN / THEN
    farm_summary_string = f"""Within ['{luca_text}']'s {texas_text} economy subject: {food_text}
 {cheap_text} is bad. 
 {farm_text} is good.
 Within the action domain of '{cultivate_text}'
 It is good to {well_text}
 It is bad to {poor_text}"""
    assert farm_concernunit.get_str_summary() == farm_summary_string


def test_ConcernUnit_get_forkunit_ideas_ReturnsCorrectObj():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_economyaddress = create_economyaddress(luca_text, texas_text)
    texas_economy_id = texas_economyaddress.economy_id
    food_text = "food"
    food_road = get_road(texas_economy_id, food_text)
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkunit = create_forkunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_text = "cultivate"
    cultivate_road = get_road(texas_economy_id, cultivate_text)
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkunit = create_forkunit(cultivate_road, good=well_text, bad=poor_text)
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        reason=food_forkunit,
        action=cultivate_forkunit,
    )

    # WHEN
    farm_forkunit_ideas = farm_concernunit.get_forkunit_ideas()

    # THEN
    print(f"{farm_forkunit_ideas.keys()=}")
    assert farm_forkunit_ideas.get(food_road) != None
    farm_road = get_road(food_road, farm_text)
    cheap_road = get_road(food_road, cheap_text)
    assert farm_forkunit_ideas.get(farm_road)
    assert farm_forkunit_ideas.get(cheap_road)
    assert farm_forkunit_ideas.get(cultivate_road)
    well_road = get_road(cultivate_road, well_text)
    poor_road = get_road(cultivate_road, poor_text)
    assert farm_forkunit_ideas.get(well_road)
    assert farm_forkunit_ideas.get(poor_road)


def test_create_concernunit_CorrectlyCreatesObj():
    # GIVEN
    texas_economyaddress = create_economyaddress("Luca", "Texas")
    food_text = "food"
    food_road = get_road(texas_economyaddress.economy_id, food_text)
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_forkunit = create_forkunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = get_road(texas_economyaddress.economy_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_forkunit = create_forkunit(cultivate_road, good=well_text, bad=poor_text)
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        reason=food_forkunit,
        action=cultivate_forkunit,
    )

    # THEN
    assert farm_concernunit.economyaddress == texas_economyaddress
    assert farm_concernunit.reason == food_forkunit
    assert farm_concernunit.action == cultivate_forkunit


def test_create_concernunit_CorrectlyCreatesObjWithCorrect_delimiter():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_economyaddress = create_economyaddress(luca_text, texas_text)

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
        economyaddress=texas_economyaddress,
        reason=texas_no_food_road,
        good=farm_text,
        bad=cheap_text,
        action=texas_no_cultivate_road,
        positive=well_text,
        negative=poor_text,
    )

    # THEN
    assert farm_concernunit.economyaddress == texas_economyaddress
    texas_yes_enjoy_road = get_road(texas_economyaddress.economy_id, enjoy_text)
    texas_yes_food_road = get_road(texas_yes_enjoy_road, food_text)
    texas_yes_food_forkunit = create_forkunit(
        texas_yes_food_road, farm_text, cheap_text
    )
    assert farm_concernunit.reason == texas_yes_food_forkunit

    texas_yes_work_road = get_road(texas_economyaddress.economy_id, work_text)
    texas_yes_cultivate_road = get_road(texas_yes_work_road, cultivate_text)
    texas_yes_cultivate_forkunit = create_forkunit(
        texas_yes_cultivate_road, well_text, poor_text
    )
    assert farm_concernunit.action == texas_yes_cultivate_forkunit
