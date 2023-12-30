from src.world.examples.examples import (
    get_farm_concernunit as examples_get_farm_concernunit,
)
from src.agenda.road import create_road, default_road_delimiter_if_none
from src.agenda.belief import create_beliefunit
from src.world.lobby import (
    EconomyAddress,
    economyaddress_shop,
    ConcernUnit,
    concernunit_shop,
    create_concernunit,
)
from pytest import raises as pytest_raises


def test_EconomyAddress_exists():
    # GIVEN
    luca_text = "Luca"
    war_text = "war"
    texas_text = "Texas"
    slash_text = "/"

    # WHEN
    texas_address = EconomyAddress(
        pain=war_text,
        treasurer_pid=luca_text,
        economy_id=texas_text,
        _road_delimiter=slash_text,
    )

    # THEN
    assert texas_address.pain == war_text
    assert texas_address.treasurer_pid == luca_text
    assert texas_address.economy_id == texas_text
    assert texas_address._road_delimiter == slash_text


def test_economyaddress_shop_ReturnsCorrectObject():
    # GIVEN
    luca_text = "Luca"
    war_text = "war"
    texas_text = "Texas"
    slash_text = "/"

    # WHEN
    texas_address = economyaddress_shop(
        pain=war_text,
        treasurer_pid=luca_text,
        economy_id=texas_text,
        _road_delimiter=slash_text,
    )

    # THEN
    assert texas_address.pain == war_text
    assert texas_address.treasurer_pid == luca_text
    assert texas_address.economy_id == texas_text
    assert texas_address._road_delimiter == slash_text


def test_economyaddress_shop_ReturnsCorrectObjectWithDefault_road_delimiter():
    # GIVEN
    luca_text = "Luca"
    texas_text = "Texas"
    war_text = "war"

    # WHEN
    texas_address = economyaddress_shop(war_text, luca_text, texas_text)

    # THEN
    assert texas_address._road_delimiter == default_road_delimiter_if_none()


def test_EconomyAddress_set_treasurer_pid_CorrectChangesAttribute():
    # GIVEN
    luca_text = "Luca"
    texas_text = "Texas"
    war_text = "war"

    # WHEN
    texas_address = economyaddress_shop(war_text, luca_text, texas_text)
    assert texas_address.treasurer_pid == luca_text

    # WHEN
    karl_text = "Karl"
    texas_address.set_treasurer_pid(karl_text)

    # THEN
    assert texas_address.treasurer_pid == karl_text


def test_ConcernUnit_exists():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_economyaddress = economyaddress_shop("war", luca_text, texas_text)

    # WHEN
    farm_concernunit = ConcernUnit(texas_economyaddress)

    # THEN
    assert farm_concernunit.issue is None
    assert farm_concernunit.fix is None
    assert farm_concernunit.economyaddress == texas_economyaddress


def test_concernunit_shop_ReturnsCorrectObj():
    # GIVEN
    texas_economyaddress = economyaddress_shop("war", "Luca", "Texas")

    food_road = create_road(texas_economyaddress.economy_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_beliefunit = create_beliefunit(food_road, good=farm_text, bad=cheap_text)

    cultivate_road = create_road(texas_economyaddress.economy_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_beliefunit = create_beliefunit(
        cultivate_road, good=well_text, bad=poor_text
    )

    # WHEN
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        issue=food_beliefunit,
        fix=cultivate_beliefunit,
    )

    # THEN
    assert farm_concernunit.issue == food_beliefunit
    assert farm_concernunit.fix == cultivate_beliefunit
    assert farm_concernunit.economyaddress == texas_economyaddress
    assert (
        farm_concernunit.get_economyaddress_road_delimiter()
        == default_road_delimiter_if_none(texas_economyaddress._road_delimiter)
    )


def test_ConcernUnit_set_issue_SetsAttributesCorrectly():
    # GIVEN
    texas_economyaddress = economyaddress_shop("war", "Luca", "Texas")
    food_road = create_road(texas_economyaddress.economy_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_beliefunit = create_beliefunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = create_road(texas_economyaddress.economy_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_beliefunit = create_beliefunit(
        cultivate_road, good=well_text, bad=poor_text
    )
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        issue=food_beliefunit,
        fix=cultivate_beliefunit,
    )

    # WHEN
    environ_road = create_road(texas_economyaddress.economy_id, "environment")
    soil_road = create_road(environ_road, "soil")
    unsafe_text = "unsafe soil"
    fertile_text = "fertile soil"
    soil_beliefunit = create_beliefunit(soil_road, good=fertile_text, bad=unsafe_text)

    farm_concernunit.set_issue(soil_beliefunit)

    # THEN
    assert farm_concernunit.issue == soil_beliefunit


def test_ConcernUnit_set_issue_EmptySubjectRaisesErrorCorrectly():
    # GIVEN
    farm_concernunit = examples_get_farm_concernunit()
    texas_economyaddress = farm_concernunit.economyaddress
    food_road = create_road(texas_economyaddress.economy_id, "")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_beliefunit = create_beliefunit(food_road, good=farm_text, bad=cheap_text)

    # WHEN / THEN
    environ_road = create_road(texas_economyaddress.economy_id, "")
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_issue(food_beliefunit)
    assert (
        str(excinfo.value)
        == f"ConcernUnit subject level 1 cannot be empty. ({environ_road})"
    )


def test_ConcernUnit_set_issue_NotEconomyRootRaisesSubjectErrorCorrectly():
    # GIVEN
    texas_economyaddress = economyaddress_shop("war", "Luca", "Texas")
    food_road = create_road(texas_economyaddress.economy_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_beliefunit = create_beliefunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = create_road(texas_economyaddress.economy_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_beliefunit = create_beliefunit(
        cultivate_road, good=well_text, bad=poor_text
    )
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        issue=food_beliefunit,
        fix=cultivate_beliefunit,
    )

    environ_text = "environment"
    incorrect_soil_road = create_road(environ_text, "soil")
    infertile_text = "infertile soil"
    fertile_text = "fertile soil"
    # infertile_road = create_road(incorrect_soil_road, "infertile soil")
    # fertile_road = create_road(incorrect_soil_road, "fertile soil")
    incorrect_soil_beliefunit = create_beliefunit(
        incorrect_soil_road, good=fertile_text, bad=infertile_text
    )

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_issue(incorrect_soil_beliefunit)
    assert (
        str(excinfo.value)
        == f"ConcernUnit setting concern_subject '{incorrect_soil_road}' failed because economy_id is not first node."
    )


def test_ConcernUnit_set_issue_RaisesDouble_economy_id_SubjectErrorCorrectly():
    # GIVEN
    texas_economyaddress = economyaddress_shop("war", "Luca", "Texas")
    texas_economy_id = texas_economyaddress.economy_id
    food_road = create_road(texas_economy_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_beliefunit = create_beliefunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = create_road(texas_economy_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_beliefunit = create_beliefunit(
        cultivate_road, good=well_text, bad=poor_text
    )
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        issue=food_beliefunit,
        fix=cultivate_beliefunit,
    )

    # WHEN / THEN
    double_economy_id = create_road(texas_economy_id, texas_economy_id)
    double_economy_beliefunit = create_beliefunit(
        double_economy_id, farm_text, cheap_text
    )
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_issue(double_economy_beliefunit)
    assert (
        str(excinfo.value)
        == f"ConcernUnit setting concern_subject '{double_economy_id}' failed because first child node cannot be economy_id as bug asumption check."
    )


def test_ConcernUnit_set_fix_SetsAttributesCorrectly():
    # GIVEN
    texas_economyaddress = economyaddress_shop("war", "Luca", "Texas")
    texas_economy_id = texas_economyaddress.economy_id
    food_road = create_road(texas_economy_id, "food")
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_beliefunit = create_beliefunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = create_road(texas_economy_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_beliefunit = create_beliefunit(
        cultivate_road, good=well_text, bad=poor_text
    )
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        issue=food_beliefunit,
        fix=cultivate_beliefunit,
    )

    # WHEN
    home_road = create_road(texas_economyaddress.economy_id, "home")
    cook_road = create_road(home_road, "cook")
    cook_beliefunit = create_beliefunit(cook_road, good="unsafe cook", bad="safe cook")
    farm_concernunit.set_fix(cook_beliefunit)

    # THEN
    assert farm_concernunit.fix == cook_beliefunit


def test_ConcernUnit_get_str_summary_ReturnsCorrectObj():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_economyaddress = economyaddress_shop("war", luca_text, texas_text)
    texas_economy_id = texas_economyaddress.economy_id
    food_text = "food"
    food_road = create_road(texas_economy_id, food_text)
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_beliefunit = create_beliefunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_text = "cultivate"
    cultivate_road = create_road(texas_economy_id, cultivate_text)
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_beliefunit = create_beliefunit(
        cultivate_road, good=well_text, bad=poor_text
    )
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        issue=food_beliefunit,
        fix=cultivate_beliefunit,
    )

    # WHEN / THEN
    farm_summary_string = f"""Within {luca_text}'s {texas_text} economy subject: {food_text}
 {cheap_text} is bad. 
 {farm_text} is good.
 Within the fix domain of '{cultivate_text}'
 It is good to {well_text}
 It is bad to {poor_text}"""
    assert farm_concernunit.get_str_summary() == farm_summary_string


def test_ConcernUnit_get_beliefunit_ideas_ReturnsCorrectObj():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_economyaddress = economyaddress_shop("war", luca_text, texas_text)
    texas_economy_id = texas_economyaddress.economy_id
    food_text = "food"
    food_road = create_road(texas_economy_id, food_text)
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_beliefunit = create_beliefunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_text = "cultivate"
    cultivate_road = create_road(texas_economy_id, cultivate_text)
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_beliefunit = create_beliefunit(
        cultivate_road, good=well_text, bad=poor_text
    )
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        issue=food_beliefunit,
        fix=cultivate_beliefunit,
    )

    # WHEN
    farm_beliefunit_ideas = farm_concernunit.get_beliefunit_ideas()

    # THEN
    print(f"{farm_beliefunit_ideas.keys()=}")
    assert farm_beliefunit_ideas.get(food_road) != None
    farm_road = create_road(food_road, farm_text)
    cheap_road = create_road(food_road, cheap_text)
    assert farm_beliefunit_ideas.get(farm_road)
    assert farm_beliefunit_ideas.get(cheap_road)
    assert farm_beliefunit_ideas.get(cultivate_road)
    well_road = create_road(cultivate_road, well_text)
    poor_road = create_road(cultivate_road, poor_text)
    assert farm_beliefunit_ideas.get(well_road)
    assert farm_beliefunit_ideas.get(poor_road)


def test_create_concernunit_CorrectlyCreatesObj():
    # GIVEN
    texas_economyaddress = economyaddress_shop("war", "Luca", "Texas")
    food_text = "food"
    food_road = create_road(texas_economyaddress.economy_id, food_text)
    farm_text = "farm food"
    cheap_text = "cheap food"
    food_beliefunit = create_beliefunit(food_road, good=farm_text, bad=cheap_text)
    cultivate_road = create_road(texas_economyaddress.economy_id, "cultivate")
    well_text = "cultivate well"
    poor_text = "cultivate poorly"
    cultivate_beliefunit = create_beliefunit(
        cultivate_road, good=well_text, bad=poor_text
    )
    farm_concernunit = concernunit_shop(
        texas_economyaddress,
        issue=food_beliefunit,
        fix=cultivate_beliefunit,
    )

    # THEN
    assert farm_concernunit.economyaddress == texas_economyaddress
    assert farm_concernunit.issue == food_beliefunit
    assert farm_concernunit.fix == cultivate_beliefunit


def test_create_concernunit_CorrectlyCreatesObjWithCorrect_delimiter():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"
    texas_economyaddress = economyaddress_shop("war", luca_text, texas_text)

    enjoy_text = "enjoying life"
    food_text = "food"
    texas_no_food_road = create_road(enjoy_text, food_text)
    farm_text = "farm food"
    cheap_text = "cheap food"

    work_text = "working"
    cultivate_text = "cultivate"
    texas_no_cultivate_road = create_road(work_text, cultivate_text)
    well_text = "cultivate well"
    poor_text = "cultivate poorly"

    # WHEN
    farm_concernunit = create_concernunit(
        economyaddress=texas_economyaddress,
        issue=texas_no_food_road,
        good=farm_text,
        bad=cheap_text,
        fix=texas_no_cultivate_road,
        positive=well_text,
        negative=poor_text,
    )

    # THEN
    assert farm_concernunit.economyaddress == texas_economyaddress
    texas_yes_enjoy_road = create_road(texas_economyaddress.economy_id, enjoy_text)
    texas_yes_food_road = create_road(texas_yes_enjoy_road, food_text)
    texas_yes_food_beliefunit = create_beliefunit(
        texas_yes_food_road, farm_text, cheap_text
    )
    assert farm_concernunit.issue == texas_yes_food_beliefunit

    texas_yes_work_road = create_road(texas_economyaddress.economy_id, work_text)
    texas_yes_cultivate_road = create_road(texas_yes_work_road, cultivate_text)
    texas_yes_cultivate_beliefunit = create_beliefunit(
        texas_yes_cultivate_road, well_text, poor_text
    )
    assert farm_concernunit.fix == texas_yes_cultivate_beliefunit
