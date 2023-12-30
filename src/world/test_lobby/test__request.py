from src.world.examples.examples import (
    get_farm_concernunit as examples_get_farm_concernunit,
    get_farm_requestunit as examples_get_farm_requestunit,
)
from src.world.lobby import RequestUnit, requestunit_shop, create_requestunit


def test_RequestUnit_exists():
    # GIVEN / WHEN
    farm_requestunit = RequestUnit()

    # THEN
    assert farm_requestunit._concernunit is None
    assert farm_requestunit._requestee_pids is None
    assert farm_requestunit._requestee_groups is None
    assert farm_requestunit._requester_pid is None


def test_requestunit_shop_ReturnsCorrectObj():
    # GIVEN
    farm_concernunit = examples_get_farm_concernunit()

    # WHEN
    bob_text = "Bob"
    bob_dict = {bob_text: None}
    yao_text = "Yao"
    aggie_text = "aggie"
    aggie_dict = {aggie_text: aggie_text}
    farm_requestunit = requestunit_shop(
        _concernunit=farm_concernunit,
        _requestee_pids=bob_dict,
        _requestee_groups=aggie_dict,
        _requester_pid=yao_text,
    )

    # THEN
    assert farm_requestunit._concernunit == farm_concernunit
    assert farm_requestunit._requestee_pids == bob_dict
    assert farm_requestunit._requestee_groups == aggie_dict
    assert farm_requestunit._requester_pid == yao_text


def test_RequestUnit_add_requestee_pid_CorrectlyChangesAttribute():
    # GIVEN
    bob_text = "Bob"
    farm_requestunit = create_requestunit(
        examples_get_farm_concernunit(), requestee_pid=bob_text
    )
    assert len(farm_requestunit._requestee_pids) == 1

    # WHEN
    yao_text = "Yao"
    farm_requestunit.add_requestee_pid(pid=yao_text)

    # THEN
    requestee_pid_dict = {bob_text: None, yao_text: None}
    assert farm_requestunit._requestee_pids == requestee_pid_dict


def test_RequestUnit_add_groupbrand_CorrectlyChangesAttribute():
    # GIVEN
    bob_text = "Bob"
    bob_dict = {bob_text: None}
    farm_requestunit = requestunit_shop(
        examples_get_farm_concernunit(), _requestee_pids=bob_dict
    )
    assert len(farm_requestunit._requestee_groups) == 0

    # WHEN
    swim_text = "swimmers"
    farm_requestunit.add_requestee_groupbrand(swim_text)

    # THEN
    swim_dict = {swim_text: swim_text}
    assert farm_requestunit._requestee_groups == swim_dict


def test_create_requestunit_ReturnsCorrectObj():
    # GIVEN
    farm_concernunit = examples_get_farm_concernunit()

    # WHEN
    bob_text = "Bob"
    farm_requestunit = create_requestunit(farm_concernunit, requestee_pid=bob_text)

    # THEN
    assert farm_requestunit._concernunit == farm_concernunit
    assert farm_requestunit._fix_weight == 1
    bob_dict = {bob_text: None}
    assert farm_requestunit._requestee_pids == bob_dict
    bob_group_dict = {bob_text: bob_text}
    assert farm_requestunit._requestee_groups == bob_group_dict
    assert farm_requestunit._requester_pid == "Luca"


def test_RequestUnit_get_str_summary_ReturnsCorrectObj():
    # GIVEN
    farm_requestunit = examples_get_farm_requestunit()

    # WHEN
    generated_farm_str = farm_requestunit.get_str_summary()

    # THEN
    bob_text = "Bob"
    real_text = "Real Farmers"
    yao_text = "Yao"
    texas_text = "Texas"
    luca_text = "Luca"
    food_text = "food"
    farm_text = "farm food"
    cheap_text = "cheap food"
    fix_text = "cultivate"
    positive_text = "cultivate well"
    negative_text = "cultivate poorly"
    static_farm_string = f"""RequestUnit: Within {luca_text}'s {texas_text} economy subject: {food_text}
 {cheap_text} is bad. 
 {farm_text} is good.
 Within the fix domain of '{fix_text}'
 It is good to {positive_text}
 It is bad to {negative_text}
 ['{bob_text}', '{yao_text}'] are in groups ['{real_text}'] and are asked to be good."""

    assert generated_farm_str == static_farm_string
