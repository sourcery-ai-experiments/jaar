from src.world.examples.examples import (
    get_farm_concernunit as examples_get_farm_concernunit,
    get_farm_lobbyunit as examples_get_farm_lobbyunit,
)
from src.agenda.road import get_road, get_node_delimiter, create_forkunit
from src.world.concern import (
    EconomyAddress,
    economyaddress_shop,
    create_economyaddress,
    ConcernUnit,
    concernunit_shop,
    create_concernunit,
    LobbyUnit,
    lobbyunit_shop,
    create_lobbyunit,
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
        person_ids=luca_dict, economy_id=texas_text, _road_node_delimiter=slash_text
    )

    # THEN
    assert texas_address.economy_id == texas_text
    assert texas_address._road_node_delimiter == slash_text
    assert texas_address.person_ids == luca_dict


def test_economyaddress_shop_ReturnsCorrectObject():
    # GIVEN
    luca_text = "Luca"
    luca_dict = {luca_text: 0}
    texas_text = "Texas"
    slash_text = "/"

    # WHEN
    texas_address = economyaddress_shop(
        person_ids=luca_dict, economy_id=texas_text, _road_node_delimiter=slash_text
    )

    # THEN
    assert texas_address.economy_id == texas_text
    assert texas_address.person_ids == luca_dict
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


def test_EconomyAddress_add_person_id_CorrectChangesAttribute():
    # GIVEN
    texas_text = "Texas"
    texas_address = economyaddress_shop(economy_id=texas_text)
    assert texas_address.person_ids == {}

    # WHEN
    luca_text = "Luca"
    texas_address.add_person_id(luca_text)

    # THEN
    luca_dict = {luca_text: 0}
    assert texas_address.person_ids == luca_dict


def test_create_economyaddress_ReturnsCorrectObj():
    # GIVEN
    texas_text = "Texas"
    luca_text = "Luca"

    # WHEN
    texas_address = create_economyaddress(luca_text, texas_text)

    # THEN
    luca_dict = {luca_text: 0}
    assert texas_address.economy_id == texas_text
    assert texas_address.person_ids == luca_dict


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
    assert farm_concernunit.when is None
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
        when=food_forkunit,
        action=cultivate_forkunit,
    )

    # THEN
    assert farm_concernunit.when == food_forkunit
    assert farm_concernunit.action == cultivate_forkunit
    assert farm_concernunit.economyaddress == texas_economyaddress
    assert farm_concernunit.get_road_node_delimiter() == get_node_delimiter(
        texas_economyaddress._road_node_delimiter
    )


def test_ConcernUnit_set_when_SetsAttributesCorrectly():
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
        when=food_forkunit,
        action=cultivate_forkunit,
    )

    # WHEN
    environ_road = get_road(texas_economyaddress.economy_id, "environment")
    soil_road = get_road(environ_road, "soil")
    unsafe_text = "unsafe soil"
    fertile_text = "fertile soil"
    soil_forkunit = create_forkunit(soil_road, good=fertile_text, bad=unsafe_text)

    farm_concernunit.set_when(soil_forkunit)

    # THEN
    assert farm_concernunit.when == soil_forkunit


def test_ConcernUnit_set_when_EmptySubjectRaisesErrorCorrectly():
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
        farm_concernunit.set_when(food_forkunit)
    assert (
        str(excinfo.value)
        == f"ConcernUnit subject level 1 cannot be empty. ({environ_road})"
    )


def test_ConcernUnit_set_when_NotEconomyRootRaisesSubjectErrorCorrectly():
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
        when=food_forkunit,
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
        farm_concernunit.set_when(incorrect_soil_forkunit)
    assert (
        str(excinfo.value)
        == f"ConcernUnit setting concern_subject '{incorrect_soil_road}' failed because economy_id is not first node."
    )


def test_ConcernUnit_set_when_RaisesDouble_economy_id_SubjectErrorCorrectly():
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
        when=food_forkunit,
        action=cultivate_forkunit,
    )

    # WHEN / THEN
    double_economy_id = get_road(texas_economy_id, texas_economy_id)
    double_economy_forkunit = create_forkunit(double_economy_id, farm_text, cheap_text)
    with pytest_raises(Exception) as excinfo:
        farm_concernunit.set_when(double_economy_forkunit)
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
        when=food_forkunit,
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
        when=food_forkunit,
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
        when=food_forkunit,
        action=cultivate_forkunit,
    )

    # THEN
    assert farm_concernunit.economyaddress == texas_economyaddress
    assert farm_concernunit.when == food_forkunit
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
        when=texas_no_food_road,
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
    assert farm_concernunit.when == texas_yes_food_forkunit

    texas_yes_work_road = get_road(texas_economyaddress.economy_id, work_text)
    texas_yes_cultivate_road = get_road(texas_yes_work_road, cultivate_text)
    texas_yes_cultivate_forkunit = create_forkunit(
        texas_yes_cultivate_road, well_text, poor_text
    )
    assert farm_concernunit.action == texas_yes_cultivate_forkunit


def test_LobbyUnit_exists():
    # GIVEN / WHEN
    farm_lobbyunit = LobbyUnit()

    # THEN
    assert farm_lobbyunit._concernunit is None
    assert farm_lobbyunit._lobbyee_pids is None
    assert farm_lobbyunit._lobbyee_groups is None
    assert farm_lobbyunit._lobbyer_pid is None


def test_lobbyunit_shop_ReturnsCorrectObj():
    # GIVEN
    farm_concernunit = examples_get_farm_concernunit()

    # WHEN
    bob_text = "Bob"
    bob_dict = {bob_text: None}
    yao_text = "Yao"
    aggie_text = "aggie"
    aggie_dict = {aggie_text: aggie_text}
    farm_lobbyunit = lobbyunit_shop(
        _concernunit=farm_concernunit,
        _lobbyee_pids=bob_dict,
        _lobbyee_groups=aggie_dict,
        _lobbyer_pid=yao_text,
    )

    # THEN
    assert farm_lobbyunit._concernunit == farm_concernunit
    assert farm_lobbyunit._lobbyee_pids == bob_dict
    assert farm_lobbyunit._lobbyee_groups == aggie_dict
    assert farm_lobbyunit._lobbyer_pid == yao_text


def test_LobbyUnit_add_lobbyee_pid_CorrectlyChangesAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_lobbyunit = create_lobbyunit(
        examples_get_farm_concernunit(), lobbyee_pid=bob_text
    )
    assert len(farm_lobbyunit._lobbyee_pids) == 1

    # WHEN
    yao_text = "Yao"
    farm_lobbyunit.add_lobbyee_pid(pid=yao_text)

    # THEN
    lobbyee_pid_dict = {bob_text: None, yao_text: None}
    assert farm_lobbyunit._lobbyee_pids == lobbyee_pid_dict


def test_LobbyUnit_add_groupbrand_CorrectlyChangesAttribute():
    # GIVEN
    bob_text = "Bob"
    bob_dict = {bob_text: None}
    farm_lobbyunit = lobbyunit_shop(
        examples_get_farm_concernunit(), _lobbyee_pids=bob_dict
    )
    assert len(farm_lobbyunit._lobbyee_groups) == 0

    # WHEN
    swim_text = "swimmers"
    farm_lobbyunit.add_lobbyee_groupbrand(swim_text)

    # THEN
    swim_dict = {swim_text: swim_text}
    assert farm_lobbyunit._lobbyee_groups == swim_dict


def test_create_lobbyunit_ReturnsCorrectObj():
    # GIVEN
    farm_concernunit = examples_get_farm_concernunit()

    # WHEN
    bob_text = "Bob"
    farm_lobbyunit = create_lobbyunit(farm_concernunit, lobbyee_pid=bob_text)

    # THEN
    assert farm_lobbyunit._concernunit == farm_concernunit
    bob_dict = {bob_text: None}
    assert farm_lobbyunit._lobbyee_pids == bob_dict
    bob_group_dict = {bob_text: bob_text}
    assert farm_lobbyunit._lobbyee_groups == bob_group_dict
    assert farm_lobbyunit._lobbyer_pid == "Luca"


def test_LobbyUnit_get_str_summary_ReturnsCorrectObj():
    # GIVEN
    farm_lobbyunit = examples_get_farm_lobbyunit()

    # WHEN
    generated_farm_str = farm_lobbyunit.get_str_summary()

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
    static_farm_string = f"""LobbyUnit: Within ['{luca_text}']'s {texas_text} economy subject: {food_text}
 {cheap_text} is bad. 
 {farm_text} is good.
 Within the action domain of '{action_text}'
 It is good to {positive_text}
 It is bad to {negative_text}
 ['{bob_text}', '{yao_text}'] are in groups ['{real_text}'] and are asked to be good."""

    assert generated_farm_str == static_farm_string
