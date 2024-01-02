# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
# from src.world.lobby import LobbyUnit, lobbyunit_shop, create_requestunit


# def test_LobbyUnit_exists():
#     # GIVEN / WHEN
#     bob_farm_lobbyunit = LobbyUnit()

#     # THEN
#     assert bob_farm_lobbyunit._src_requestunit is None
#     assert bob_farm_lobbyunit._dst_requestunit is None


# def test_lobbyunit_shop_ReturnsCorrectObj():
#     # GIVEN
#     farm_requestnunit = examples_get_farm_requestunit()

#     # WHEN
#     farm_lobbyunit = lobbyunit_shop(
#         _src_requestunit=farm_requestnunit,
#         _dst_requestunit=-1,
#     )

#     # THEN
#     assert farm_lobbyunit._src_requestunit == farm_requestnunit
#     assert farm_lobbyunit._dst_requestunit == -1


# def test_create_lobbyunit_ReturnsCorrectObj():
#     # GIVEN
#     farm_requestunit = examples_get_farm_requestunit()

#     # WHEN
#     bob_text = "Bob"
#     farm_requestunit = create_requestunit(farm_wantunit, requestee_pid=bob_text)

#     # THEN
#     assert farm_requestunit._wantunit == farm_wantunit
#     assert farm_requestunit._action_weight == 1
#     bob_dict = {bob_text: None}
#     assert farm_requestunit._requestee_pids == bob_dict
#     bob_group_dict = {bob_text: bob_text}
#     assert farm_requestunit._requestee_groups == bob_group_dict
#     assert farm_requestunit._requester_pid == "Luca"


# def test_RequestUnit_get_str_summary_ReturnsCorrectObj():
#     # GIVEN
#     farm_requestunit = examples_get_farm_requestunit()

#     # WHEN
#     generated_farm_str = farm_requestunit.get_str_summary()

#     # THEN
#     bob_text = "Bob"
#     real_text = "Real Farmers"
#     yao_text = "Yao"
#     texas_text = "Texas"
#     luca_text = "Luca"
#     food_text = "food"
#     farm_text = "farm food"
#     cheap_text = "cheap food"
#     action_text = "cultivate"
#     positive_text = "cultivate well"
#     negative_text = "cultivate poorly"
#     static_farm_string = f"""RequestUnit: Within {luca_text}'s {texas_text} economy subject: {food_text}
#  {cheap_text} is bad.
#  {farm_text} is good.
#  Within the action domain of '{action_text}'
#  It is good to {positive_text}
#  It is bad to {negative_text}
#  ['{bob_text}', '{yao_text}'] are in groups ['{real_text}'] and are asked to be good."""

#     assert generated_farm_str == static_farm_string
