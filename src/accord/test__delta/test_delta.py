# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road, PartyID
from src.accord.delta import DeltaUnit, deltaunit_shop


def test_DeltaUnit_exists():
    # GIVEN
    bob_text = "Bob"

    # WHEN
    x_deltaunit = DeltaUnit(
        party_id=bob_text,
        creditor_weight=2,
        debtor_weight=3,
        depotlink_type="",
    )

    # THEN
    assert x_deltaunit.party_id == bob_text
    assert x_deltaunit.creditor_weight == 2
    assert x_deltaunit.debtor_weight == 3
    assert x_deltaunit.depotlink_type == ""


def test_deltaunit_shop_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    # mess_problem_road = create_road(jack_text, "mess")
    # femi_healer_road = create_road(mess_problem_road, "Femi")
    # ohio_economy_road = create_road(femi_healer_road, "Ohio")
    # jack_agent_road = create_road(ohio_economy_road, jack_text)
    # adam_party_road = create_road(jack_agent_road, "Adam")

    # WHEN
    adam_deltaunit = deltaunit_shop(party_id=yao_text)

    # THEN
    assert adam_deltaunit.party_id == yao_text
    assert adam_deltaunit.creditor_weight == 0
    assert adam_deltaunit.debtor_weight == 0
    assert adam_deltaunit.depotlink_type == "assignment"


# def test_DeltaUnit_set_topiclink_SetsAttrCorrectly():
#     # GIVEN
#     one_text = "1"
#     farm_deltaunit = deltaunit_shop(one_text)
#     assert farm_deltaunit._topiclinks == {}

#     # WHEN
#     cook_topiclink = topiclink_shop(base=create_road(root_label(), "cooking"))
#     farm_deltaunit.set_topiclink(cook_topiclink)

#     # THEN
#     assert len(farm_deltaunit._topiclinks) == 1
#     assert farm_deltaunit._topiclinks.get(cook_topiclink.base) != None
#     assert farm_deltaunit._topiclinks.get(cook_topiclink.base) == cook_topiclink


# def test_DeltaUnit_edit_attr_SetsAttrCorrectly():
#     # GIVEN
#     one_text = "1"
#     farm_deltaunit = deltaunit_shop(one_text)
#     assert farm_deltaunit.author_weight == 1
#     assert farm_deltaunit.reader_weight == 1
#     assert farm_deltaunit._relative_author_weight == 0
#     assert farm_deltaunit._relative_reader_weight == 0

#     # WHEN
#     new_author_weight = 7
#     new_reader_weight = 7
#     new_relative_author_weight = 0.66
#     new_relative_reader_weight = 0.43
#     farm_deltaunit.edit_attr(
#         author_weight=new_author_weight,
#         reader_weight=new_reader_weight,
#         _relative_author_weight=new_relative_author_weight,
#         _relative_reader_weight=new_relative_reader_weight,
#     )

#     # THEN
#     assert farm_deltaunit.author_weight != 1
#     assert farm_deltaunit.reader_weight != 1
#     assert farm_deltaunit.author_weight == new_author_weight
#     assert farm_deltaunit.reader_weight == new_reader_weight
#     assert farm_deltaunit._relative_author_weight != 0
#     assert farm_deltaunit._relative_reader_weight != 0
#     assert farm_deltaunit._relative_author_weight == new_relative_author_weight
#     assert farm_deltaunit._relative_reader_weight == new_relative_reader_weight
