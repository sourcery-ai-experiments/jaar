from src.world.examples.examples import (
    get_farm_concernunit as examples_get_farm_concernunit,
    get_farm_lobbyunit as examples_get_farm_lobbyunit,
)
from src.world.lobby import LobbyUnit, lobbyunit_shop, create_lobbyunit


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
    assert farm_lobbyunit._action_weight == 1
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
