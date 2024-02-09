from src._prime.road import (
    RoadNode,
    PersonID,
    PersonRoad,
    ProblemID,
    ProblemRoad,
    HealerID,
    MarketID,
    AgentID,
    PartyID,
    RoadUnit,
    MarketRoad,
    AgendaRoad,
    change_road,
    is_sub_road,
    get_all_road_nodes,
    get_terminus_node,
    find_replace_road_key_dict,
    get_parent_road_from_road,
    create_road_without_root_node,
    get_root_node_from_road,
    road_validate,
    get_ancestor_roads,
    get_forefather_roads,
    get_default_market_root_roadnode as root_label,
    create_road_from_nodes,
    create_road,
    get_diff_road,
    create_road,
    is_heir_road,
    default_road_delimiter_if_none,
    replace_road_delimiter,
    get_single_roadnode,
    validate_roadnode,
)
from pytest import raises as pytest_raises
from dataclasses import dataclass
from inspect import getdoc as inspect_getdoc


def test_RoadNode_exists():
    # GIVEN
    empty_str = ""
    # WHEN
    x_road = RoadNode(empty_str)
    # THEN
    assert x_road == empty_str
    assert (
        inspect_getdoc(x_road)
        == "A string presentation of a tree node. Nodes cannot contain RoadUnit delimiter"
    )


def test_RoadUnit_exists():
    # GIVEN
    empty_str = ""
    # WHEN
    x_road = RoadUnit(empty_str)
    # THEN
    assert x_road == empty_str
    assert (
        inspect_getdoc(x_road)
        == "A string presentation of a tree path. RoadNodes are seperated by road delimiter"
    )


def test_road_is_sub_road_correctlyReturnsBool():
    # WHEN
    casa_text = "casa"
    casa_road = f"{root_label()}{default_road_delimiter_if_none()}{casa_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{casa_road}{default_road_delimiter_if_none()}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{bloomers_road}{default_road_delimiter_if_none()}{roses_text}"

    # WHEN / THEN
    assert is_sub_road(bloomers_road, bloomers_road)
    assert is_sub_road(roses_road, bloomers_road)
    assert is_sub_road(bloomers_road, roses_road) == False


def test_road_road_validate_correctlyReturnsRoadUnit():
    x_s = default_road_delimiter_if_none()
    _market_id = "x"
    casa_road = f"{_market_id}{x_s}casa"
    source_road = f"{_market_id}{x_s}source"
    fun_road = f"{_market_id}{x_s}fun"
    assert road_validate(None, x_s, _market_id) == ""
    assert road_validate("", x_s, _market_id) == ""
    assert road_validate(f"{_market_id}{x_s}casa", x_s, _market_id) == casa_road
    assert road_validate(f"A{x_s}casa", x_s, _market_id) == casa_road
    assert road_validate(f"{x_s}source", x_s, _market_id) == source_road
    assert road_validate(f"source{x_s}fun", x_s, _market_id) == fun_road
    assert road_validate("source", x_s, _market_id) == _market_id
    assert road_validate(f"AA{x_s}casa", x_s, _market_id) == casa_road


def test_road_create_road_ReturnsCorrectRoadUnitWith_delimiter():
    # GIVEN
    rose_text = "rose"
    comma_delimiter = ","
    comma_delimiter_rose_road = f"{root_label()}{comma_delimiter}{rose_text}"
    assert create_road(root_label(), rose_text) == comma_delimiter_rose_road

    # WHEN
    slash_delimiter = "/"
    slash_delimiter_rose_road = f"{root_label()}{slash_delimiter}{rose_text}"
    generated_rose_road = create_road(
        root_label(), rose_text, delimiter=slash_delimiter
    )

    # THEN
    assert generated_rose_road != comma_delimiter_rose_road
    assert generated_rose_road == slash_delimiter_rose_road

    # WHEN
    brackets_road = create_road(root_label(), rose_text, delimiter=slash_delimiter)

    # THEN
    assert generated_rose_road == brackets_road
    assert slash_delimiter_rose_road == brackets_road


def test_road_change_road_CorrectlyRoadUnit():
    # GIVEN
    casa_text = "casa"
    casa_road = create_road(root_label(), casa_text)
    bloomers_text = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_text)
    plants_text = "plants"
    plants_road = create_road(casa_road, plants_text)
    roses_text = "roses"
    old_roses_road = create_road(bloomers_road, roses_text)
    new_roses_road = create_road(plants_road, roses_text)

    print(f"{change_road(old_roses_road, bloomers_road, plants_road)}")

    # WHEN / THEN
    assert change_road(bloomers_road, bloomers_road, bloomers_road) == bloomers_road
    assert change_road(old_roses_road, bloomers_road, plants_road) == new_roses_road
    assert change_road(old_roses_road, "random_text", plants_road) == old_roses_road


def test_road_get_all_road_nodes_ReturnsRoadNodes():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}{x_s}{roses_text}"

    # WHEN/THENs
    root_list = [root_label()]
    assert get_all_road_nodes(road=root_label()) == root_list
    casa_list = [root_label(), casa_text]
    assert get_all_road_nodes(road=casa_road) == casa_list
    bloomers_list = [root_label(), casa_text, bloomers_text]
    assert get_all_road_nodes(road=bloomers_road) == bloomers_list
    roses_list = [root_label(), casa_text, bloomers_text, roses_text]
    assert get_all_road_nodes(road=roses_road) == roses_list


def test_road_get_terminus_node_ReturnsRoadNode():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_text}"

    # WHEN/THENs
    assert get_terminus_node(road=root_label()) == root_label()
    assert get_terminus_node(road=casa_road) == casa_text
    assert get_terminus_node(road=bloomers_road) == bloomers_text
    assert get_terminus_node(road=roses_road) == roses_text


def test_road_get_terminus_node_ReturnsRoadNodeWhenNonDefaultDelimiter():
    # GIVEN
    casa_text = "casa"
    bloomers_text = "bloomers"
    roses_text = "roses"
    slash_text = default_road_delimiter_if_none()
    slash_casa_road = f"{root_label()}{slash_text}{casa_text}"
    slash_bloomers_road = f"{slash_casa_road}{slash_text}{bloomers_text}"
    slash_roses_road = f"{slash_bloomers_road}{slash_text}{roses_text}"

    # WHEN/THENs
    assert get_terminus_node(root_label(), slash_text) == root_label()
    assert get_terminus_node(slash_casa_road, slash_text) == casa_text
    assert get_terminus_node(slash_bloomers_road, slash_text) == bloomers_text
    assert get_terminus_node(slash_roses_road, slash_text) == roses_text


def test_road_get_root_node_from_road_ReturnsRoadNode():
    # GIVEN
    casa_text = "casa"
    casa_road = create_road(root_label(), casa_text)
    bloomers_text = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_text)
    roses_text = "roses"
    roses_road = create_road(casa_text, roses_text)

    # WHEN/THENs
    assert get_root_node_from_road(root_label()) == root_label()
    assert get_root_node_from_road(casa_road) == root_label()
    assert get_root_node_from_road(bloomers_road) == root_label()
    assert get_root_node_from_road(roses_road) == casa_text


def test_road_get_parent_road_from_road_works():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_text}"

    # WHEN/THENs
    assert get_parent_road_from_road(road=root_label()) == ""
    assert get_parent_road_from_road(road=casa_road) == root_label()
    assert get_parent_road_from_road(road=bloomers_road) == casa_road
    assert get_parent_road_from_road(road=roses_road) == bloomers_road


def test_road_create_road_without_root_node_WorksCorrectly():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    casa_without_root_road = f"{x_s}{casa_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}"
    bloomers_without_root_road = f"{x_s}{casa_text}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}{x_s}{roses_text}"
    roses_without_root_road = f"{x_s}{casa_text}{x_s}{bloomers_text}{x_s}{roses_text}"

    # WHEN/THENs
    assert create_road_without_root_node(road=root_label()) == x_s
    assert create_road_without_root_node(road=casa_road) == casa_without_root_road
    assert (
        create_road_without_root_node(road=bloomers_road) == bloomers_without_root_road
    )
    assert create_road_without_root_node(road=roses_road) == roses_without_root_road
    road_without_node = create_road_without_root_node(road=roses_road)
    with pytest_raises(Exception) as excinfo:
        create_road_without_root_node(road=road_without_node)
    assert (
        str(excinfo.value)
        == f"Cannot create_road_without_root_node of '{road_without_node}' because it has no root node."
    )


@dataclass
class EmptyObj:
    x_road: RoadUnit = ""

    def find_replace_road(self, old_road, new_road):
        self.x_road = change_road(self.x_road, old_road=old_road, new_road=new_road)

    def get_obj_key(self) -> RoadUnit:
        return self.x_road


def test_road_find_replace_road_key_dict_ReturnsCorrectDict_Scenario1():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    old_seasons_road = f"{root_label()}{x_s}casa{x_s}seasons"
    old_dict_x = {old_seasons_road: EmptyObj(old_seasons_road)}
    assert old_dict_x.get(old_seasons_road) != None

    # WHEN
    new_seasons_road = f"{root_label()}{x_s}casa{x_s}kookies"
    new_dict_x = find_replace_road_key_dict(
        dict_x=old_dict_x, old_road=old_seasons_road, new_road=new_seasons_road
    )

    assert new_dict_x != {}
    assert len(new_dict_x) == 1
    print(f"{new_dict_x=}")
    assert new_dict_x.get(new_seasons_road) != None
    assert new_dict_x.get(old_seasons_road) is None


def test_road_get_ancestor_roads_ReturnsAncestorRoadUnits():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    nation_text = "nation-state"
    nation_road = f"{root_label()}{x_s}{nation_text}"
    usa_text = "USA"
    usa_road = f"{nation_road}{x_s}{usa_text}"
    texas_text = "Texas"
    texas_road = f"{usa_road}{x_s}{texas_text}"

    # WHEN
    x_roads = get_ancestor_roads(road=texas_road)

    # THEN
    print(f"{texas_road=}")
    assert x_roads != None
    texas_ancestor_roads = [
        texas_road,
        usa_road,
        nation_road,
        root_label(),
    ]
    assert x_roads == texas_ancestor_roads

    # WHEN
    assert get_ancestor_roads(None) == []
    assert get_ancestor_roads("") == [""]
    assert get_ancestor_roads(root_label()) == [root_label()]


def test_road_get_forefather_roads_ReturnsAncestorRoadUnitsWithoutSource():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    nation_text = "nation-state"
    nation_road = f"{root_label()}{x_s}{nation_text}"
    usa_text = "USA"
    usa_road = f"{nation_road}{x_s}{usa_text}"
    texas_text = "Texas"
    texas_road = f"{usa_road}{x_s}{texas_text}"

    # WHEN
    x_roads = get_forefather_roads(road=texas_road)

    # THEN
    print(f"{texas_road=}")
    assert x_roads != None
    texas_forefather_roads = {
        nation_road: None,
        usa_road: None,
        root_label(): None,
    }
    assert x_roads == texas_forefather_roads


def test_road_get_default_market_root_roadnode_ReturnsCorrectObj():
    assert root_label() == "A"


def test_road_create_road_from_nodes_WorksCorrectly():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    root_list = get_all_road_nodes(root_label())
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    casa_list = get_all_road_nodes(casa_road)
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}"
    bloomers_list = get_all_road_nodes(bloomers_road)
    roses_text = "roses"
    roses_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}{x_s}{roses_text}"
    roses_list = get_all_road_nodes(roses_road)

    # WHEN / THEN
    assert root_label() == create_road_from_nodes(root_list)
    assert casa_road == create_road_from_nodes(casa_list)
    assert bloomers_road == create_road_from_nodes(bloomers_list)
    assert roses_road == create_road_from_nodes(roses_list)


def test_road_create_road_WorksCorrectly():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{root_label()}{x_s}{casa_text}{x_s}{bloomers_text}{x_s}{roses_text}"

    # WHEN / THEN
    assert root_label() == create_road(None, root_label())
    assert root_label() == create_road("", root_label())
    assert casa_road == create_road(root_label(), casa_text)
    assert bloomers_road == create_road(casa_road, bloomers_text)
    assert roses_road == create_road(bloomers_road, roses_text)
    assert roses_road == create_road(roses_road, None)


def test_raodnode_exists():
    # GIVEN
    empty_text = ""

    # WHEN
    new_obj = RoadNode(empty_text)

    # THEN
    assert new_obj == empty_text


def test_raodnode_is_node_ReturnsCorrectBool():
    # WHEN / THEN
    x_raodnode = RoadNode("")
    assert x_raodnode.is_node()

    # WHEN / THEN
    x_s = default_road_delimiter_if_none()
    x_raodnode = RoadNode(f"casa{x_s}kitchen")
    assert x_raodnode.is_node() == False


def test_get_diff_road_ReturnsCorrectObj():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    casa_text = "casa"
    casa_road = f"{root_label()}{x_s}{casa_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{casa_road}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_text}"

    # WHEN / THEN
    print(f"{casa_road=}")
    print(f"{bloomers_road=}")
    assert get_diff_road(bloomers_road, casa_road) == bloomers_text
    assert get_diff_road(roses_road, bloomers_road) == roses_text
    bloomers_rose_road = create_road(bloomers_text, roses_text)
    print(f"{bloomers_rose_road=}")
    assert get_diff_road(roses_road, casa_road) == bloomers_rose_road


def test_is_heir_road_CorrectlyIdentifiesHeirs():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    usa_text = "USA"
    usa_road = f"{root_label()}{x_s}Nation-States{x_s}{usa_text}"
    texas_text = "Texas"
    texas_road = f"{usa_road}{x_s}{texas_text}"
    # earth_text = "earth"
    # earth_road = f"{earth_text}"
    # sea_text = "sea"
    # sea_road = f"{earth_road}{x_s}{sea_text}"
    # seaside_text = "seaside"
    # seaside_road = f"{earth_road}{x_s}{seaside_text}"

    # WHEN / THEN
    assert is_heir_road(src=usa_road, heir=usa_road)
    assert is_heir_road(src=usa_road, heir=texas_road)
    assert is_heir_road(f"earth{x_s}sea", f"earth{x_s}seaside{x_s}beach") == False
    assert is_heir_road(src=f"earth{x_s}sea", heir=f"earth{x_s}seaside") == False


def test_replace_road_delimiter_ReturnsNewObj():
    # GIVEN
    casa_text = "casa"
    gen_casa_road = create_road(root_label(), casa_text)
    comma_delimiter = default_road_delimiter_if_none()
    comma_delimiter_casa_road = f"{root_label()}{comma_delimiter}{casa_text}"
    assert comma_delimiter == ","
    assert gen_casa_road == comma_delimiter_casa_road

    # WHEN
    slash_delimiter = "/"
    gen_casa_road = replace_road_delimiter(
        gen_casa_road, old_delimiter=comma_delimiter, new_delimiter=slash_delimiter
    )

    # THEN
    slash_delimiter_casa_road = f"{root_label()}{slash_delimiter}{casa_text}"
    assert gen_casa_road == slash_delimiter_casa_road


def test_replace_road_delimiter_CorrectlyRaisesError():
    # GIVEN
    cooker_text = "cooker/cleaner"
    gen_cooker_road = create_road(root_label(), cooker_text)
    comma_delimiter = default_road_delimiter_if_none()
    comma_delimiter_cooker_road = f"{root_label()}{comma_delimiter}{cooker_text}"
    assert comma_delimiter == ","
    assert gen_cooker_road == comma_delimiter_cooker_road

    # WHEN / THEN
    slash_delimiter = "/"
    with pytest_raises(Exception) as excinfo:
        gen_cooker_road = replace_road_delimiter(
            gen_cooker_road,
            old_delimiter=comma_delimiter,
            new_delimiter=slash_delimiter,
        )
    assert (
        str(excinfo.value)
        == f"Cannot replace_road_delimiter '{comma_delimiter}' with '{slash_delimiter}' because the new one already exists in road '{gen_cooker_road}'."
    )


def test_replace_road_delimiter_WhenNewdelimiterIsFirstCharacterInRoadUnitRaisesError():
    # GIVEN
    cooker_text = "/cooker"
    cleaner_text = "cleaner"
    comma_delimiter = default_road_delimiter_if_none()
    comma_delimiter_cooker_road = f"{cooker_text}{comma_delimiter}{cleaner_text}"
    assert comma_delimiter == ","

    # WHEN / THEN
    slash_delimiter = "/"
    with pytest_raises(Exception) as excinfo:
        comma_delimiter_cooker_road = replace_road_delimiter(
            comma_delimiter_cooker_road,
            old_delimiter=comma_delimiter,
            new_delimiter=slash_delimiter,
        )
    assert (
        str(excinfo.value)
        == f"Cannot replace_road_delimiter '{comma_delimiter}' with '{slash_delimiter}' because the new one already exists in road '{comma_delimiter_cooker_road}'."
    )


def test_MarketRoad_Exists():
    # GIVEN
    texas_text = "texas"

    # WHEN
    texas_marketroad = MarketRoad(texas_text)

    # THEN
    assert texas_marketroad != None
    assert texas_marketroad == texas_text
    assert (
        inspect_getdoc(texas_marketroad)
        == """RodeUnit with node and road seperated by WorldUnit._road_delimiter:
PersonID
ProblemID
HealerID
MarketID"""
    )


def test_ProblemID_exists():
    # GIVEN
    empty_str = ""
    # WHEN
    x_road = ProblemID(empty_str)
    # THEN
    assert x_road == empty_str
    assert (
        inspect_getdoc(x_road) == "A RoadNode used to identify a PersonUnit's Problem"
    )


def test_HealerID_exists():
    # GIVEN
    bob_text = "Bob"
    # WHEN
    bob_healer_id = HealerID(bob_text)
    # THEN
    assert bob_healer_id == bob_text
    assert (
        inspect_getdoc(bob_healer_id)
        == "A RoadNode used to identify a Problem's Healer"
    )


def test_MarketID_exists():
    # GIVEN
    bob_text = "Bob"
    # WHEN
    bob_market_id = MarketID(bob_text)
    # THEN
    assert bob_market_id == bob_text
    assert (
        inspect_getdoc(bob_market_id) == "A RoadNode used to identify a Healer's Market"
    )


def test_AgentID_exists():
    # GIVEN
    bob_text = "Bob"
    # WHEN
    bob_agent_id = AgentID(bob_text)
    # THEN
    assert bob_agent_id == bob_text
    assert (
        inspect_getdoc(bob_agent_id)
        == "A RoadNode used to identify a AgendaUnit's agent_id"
    )


def test_PartyID_exists():
    # GIVEN
    bob_text = "Bob"
    # WHEN
    bob_party_id = PartyID(bob_text)
    # THEN
    assert bob_party_id == bob_text
    assert (
        inspect_getdoc(bob_party_id)
        == "Every PartyID object is AgentID, must follow AgentID format."
    )


def test_ProblemRoad_Exists():
    # GIVEN
    bob_road = create_road("problem1", "Bob")
    texas_road = create_road(bob_road, "texas")
    sports_road = create_road(texas_road, "sports")

    # WHEN
    sports_problemroad = ProblemRoad(sports_road)

    # THEN
    assert sports_problemroad != None
    assert sports_problemroad == sports_road
    assert (
        inspect_getdoc(sports_problemroad)
        == """RodeUnit with following nodes seperated by WorldUnit._road_delimiter:
ProblemID (Must Exist)
HealerID
MarketRoad"""
    )


def test_PersonRoad_Exists():
    # GIVEN
    problem1_road = create_road(PersonID("Tim"), ProblemID("problem1"))
    bob_road = create_road(problem1_road, HealerID("Bob"))
    texas_road = create_road(bob_road, MarketID("texas"))
    sports_road = create_road(texas_road, "sports")

    # WHEN
    sports_problemroad = PersonRoad(sports_road)

    # THEN
    assert sports_problemroad != None
    assert sports_problemroad == sports_road
    assert (
        inspect_getdoc(sports_problemroad)
        == """RodeUnit with following nodes seperated by WorldUnit._road_delimiter:
PersonID (Must Exist)
ProblemID
HealerID
MarketRoad"""
    )


def test_AgendaRoad_Exists():
    # GIVEN
    texas_road = create_road("Bob", "texas")
    sports_road = create_road(texas_road, "sports")
    yao_agendaroad = create_road(texas_road, "Yao")

    # WHEN
    yao_agendaroad = AgendaRoad(sports_road)

    # THEN
    assert yao_agendaroad != None
    assert yao_agendaroad == sports_road
    assert (
        inspect_getdoc(yao_agendaroad)
        == """RodeUnit with nodes seperated by Agenda._road_delimiter that
starts with MarketID"""
    )


def test_get_single_roadnode_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    yao_text = "Yao"
    food_text = "food"
    ohio_text = "Ohio"
    bob_road = create_road_from_nodes([bob_text, food_text, yao_text, ohio_text])

    # WHEN / THEN
    person_id_text = "PersonID"
    problem_id_text = "ProblemID"
    healer_id_text = "HealerID"
    market_id_text = "MarketID"
    personroad_text = "PersonRoad"

    assert get_single_roadnode(personroad_text, bob_text, problem_id_text) is None
    assert get_single_roadnode(personroad_text, bob_text, healer_id_text) is None
    assert get_single_roadnode(personroad_text, bob_text, market_id_text) is None

    assert get_single_roadnode(personroad_text, bob_road, person_id_text) == bob_text
    assert get_single_roadnode(personroad_text, bob_road, problem_id_text) == food_text
    assert get_single_roadnode(personroad_text, bob_road, healer_id_text) == yao_text
    assert get_single_roadnode(personroad_text, bob_road, market_id_text) == ohio_text


def test_validate_roadnode_RaisesErrorWhenNotRoadNode():
    # GIVEN
    bob_text = "Bob, Tom"
    slash_text = "/"
    assert bob_text == validate_roadnode(bob_text, x_delimiter=slash_text)

    # WHEN
    comma_text = ","
    with pytest_raises(Exception) as excinfo:
        bob_text == validate_roadnode(bob_text, x_delimiter=comma_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{comma_text}'"
    )


def test_validate_roadnode_RaisesErrorWhenRoadNode():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Tom"
    assert bob_text == validate_roadnode(
        bob_text, x_delimiter=slash_text, not_roadnode_required=True
    )

    # WHEN
    comma_text = ","
    with pytest_raises(Exception) as excinfo:
        bob_text == validate_roadnode(
            bob_text, x_delimiter=comma_text, not_roadnode_required=True
        )
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to not be a RoadNode. Must contain delimiter: '{comma_text}'"
    )
