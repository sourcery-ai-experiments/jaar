# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road, PartyID
from src.deal.partyedit import PartyEditUnit, partyeditunit_shop


def test_PartyEditUnit_exists():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"

    # WHEN
    x_partyeditunit = PartyEditUnit(
        member=yao_text,
        party_id=bob_text,
        creditor_weight=2,
        debtor_weight=3,
        depotlink_type="",
    )

    # THEN
    assert x_partyeditunit.party_id == bob_text
    assert x_partyeditunit.creditor_weight == 2
    assert x_partyeditunit.debtor_weight == 3
    assert x_partyeditunit.depotlink_type == ""


def test_partyeditunit_shop_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    # mess_problem_road = create_road(jack_text, "mess")
    # femi_healer_road = create_road(mess_problem_road, "Femi")
    # ohio_economy_road = create_road(femi_healer_road, "Ohio")
    # jack_agent_road = create_road(ohio_economy_road, jack_text)
    # adam_party_road = create_road(jack_agent_road, "Adam")

    # WHEN
    adam_partyeditunit = partyeditunit_shop(member=bob_text, party_id=yao_text)

    # THEN
    assert adam_partyeditunit.member == bob_text
    assert adam_partyeditunit.party_id == yao_text
    assert adam_partyeditunit.creditor_weight == 0
    assert adam_partyeditunit.debtor_weight == 0
    assert adam_partyeditunit.depotlink_type == "assignment"


def test_PartyEditUnit_set_member_SetsAttrCorrectly():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    farm_partyeditunit = partyeditunit_shop(bob_text, yao_text)
    assert farm_partyeditunit.member == bob_text

    # WHEN
    sue_text = "Sue"
    farm_partyeditunit.set_member(sue_text)

    # THEN
    assert farm_partyeditunit.member == sue_text


# def test_PartyEditUnit_edit_attr_SetsAttrCorrectly():
#     # GIVEN
#     one_text = "1"
#     farm_partyeditunit = partyeditunit_shop(one_text)
#     assert farm_partyeditunit.author_weight == 1
#     assert farm_partyeditunit.reader_weight == 1
#     assert farm_partyeditunit._relative_author_weight == 0
#     assert farm_partyeditunit._relative_reader_weight == 0

#     # WHEN
#     new_author_weight = 7
#     new_reader_weight = 7
#     new_relative_author_weight = 0.66
#     new_relative_reader_weight = 0.43
#     farm_partyeditunit.edit_attr(
#         author_weight=new_author_weight,
#         reader_weight=new_reader_weight,
#         _relative_author_weight=new_relative_author_weight,
#         _relative_reader_weight=new_relative_reader_weight,
#     )

#     # THEN
#     assert farm_partyeditunit.author_weight != 1
#     assert farm_partyeditunit.reader_weight != 1
#     assert farm_partyeditunit.author_weight == new_author_weight
#     assert farm_partyeditunit.reader_weight == new_reader_weight
#     assert farm_partyeditunit._relative_author_weight != 0
#     assert farm_partyeditunit._relative_reader_weight != 0
#     assert farm_partyeditunit._relative_author_weight == new_relative_author_weight
#     assert farm_partyeditunit._relative_reader_weight == new_relative_reader_weight
