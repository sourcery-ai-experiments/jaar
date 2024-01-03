from src.agenda.road import (
    RoadUnit,
    PersonID,
    EconomyID,
    PersonRoad,
    EconomyAddress,
    create_economyaddress,
    get_economyaddress_from_personroad,
    get_economyroad_from_personroad,
    change_road,
    is_sub_road,
    get_all_road_nodes,
    get_terminus_node_from_road,
    find_replace_road_key_dict,
    get_parent_road_from_road,
    create_road_without_root_node,
    get_root_node_from_road,
    road_validate,
    get_ancestor_roads,
    get_forefather_roads,
    get_default_economy_root_roadnode as root_label,
    create_road_from_nodes,
    create_road,
    RoadNode,
    get_diff_road,
    create_road,
    is_heir_road,
    default_road_delimiter_if_none,
    replace_road_delimiter,
)
from src.agenda.required_idea import sufffactunit_shop
from src.agenda.idea import IdeaUnit
from pytest import raises as pytest_raises


def test_RoadUnit_exists():
    # GIVEN
    empty_str = ""
    # WHEN
    x_road = RoadUnit(empty_str)
    # THEN
    assert x_road == empty_str


def test_road_is_sub_road_correctlyReturnsBool():
    # WHEN
    healer_text = "healer"
    healer_road = f"{root_label()}{default_road_delimiter_if_none()}{healer_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{healer_road}{default_road_delimiter_if_none()}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{bloomers_road}{default_road_delimiter_if_none()}{roses_text}"

    # WHEN / THEN
    assert is_sub_road(bloomers_road, bloomers_road)
    assert is_sub_road(roses_road, bloomers_road)
    assert is_sub_road(bloomers_road, roses_road) == False


def test_road_road_validate_correctlyReturnsRoadUnit():
    x_s = default_road_delimiter_if_none()
    _economy_id = "x"
    casa_road = f"{_economy_id}{x_s}casa"
    source_road = f"{_economy_id}{x_s}source"
    fun_road = f"{_economy_id}{x_s}fun"
    assert road_validate(None, x_s, _economy_id) == ""
    assert road_validate("", x_s, _economy_id) == ""
    assert road_validate(f"{_economy_id}{x_s}casa", x_s, _economy_id) == casa_road
    assert road_validate(f"A{x_s}casa", x_s, _economy_id) == casa_road
    assert road_validate(f"{x_s}source", x_s, _economy_id) == source_road
    assert road_validate(f"source{x_s}fun", x_s, _economy_id) == fun_road
    assert road_validate("source", x_s, _economy_id) == _economy_id
    assert road_validate(f"AA{x_s}casa", x_s, _economy_id) == casa_road


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
    healer_text = "healer"
    healer_road = create_road(root_label(), healer_text)
    bloomers_text = "bloomers"
    bloomers_road = create_road(healer_road, bloomers_text)
    plants_text = "plants"
    plants_road = create_road(healer_road, plants_text)
    roses_text = "roses"
    old_roses_road = create_road(bloomers_road, roses_text)
    new_roses_road = create_road(plants_road, roses_text)

    print(f"{change_road(old_roses_road, bloomers_road, plants_road)}")

    # WHEN / THEN
    assert change_road(bloomers_road, bloomers_road, bloomers_road) == bloomers_road
    assert change_road(old_roses_road, bloomers_road, plants_road) == new_roses_road
    assert change_road(old_roses_road, "random_text", plants_road) == old_roses_road


def test_road_get_all_road_nodes_CorrectlyReturnsRoadNodes():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    healer_text = "healer"
    healer_road = f"{root_label()}{x_s}{healer_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{healer_text}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = (
        f"{root_label()}{x_s}{healer_text}{x_s}{bloomers_text}{x_s}{roses_text}"
    )

    # WHEN/THENs
    root_list = [root_label()]
    assert get_all_road_nodes(road=root_label()) == root_list
    healer_list = [root_label(), healer_text]
    assert get_all_road_nodes(road=healer_road) == healer_list
    bloomers_list = [root_label(), healer_text, bloomers_text]
    assert get_all_road_nodes(road=bloomers_road) == bloomers_list
    roses_list = [root_label(), healer_text, bloomers_text, roses_text]
    assert get_all_road_nodes(road=roses_road) == roses_list


def test_road_get_terminus_node_from_road_CorrectlyReturnsRoadNode():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    healer_text = "healer"
    healer_road = f"{root_label()}{x_s}{healer_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{healer_road}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_text}"

    # WHEN/THENs
    assert get_terminus_node_from_road(road=root_label()) == root_label()
    assert get_terminus_node_from_road(road=healer_road) == healer_text
    assert get_terminus_node_from_road(road=bloomers_road) == bloomers_text
    assert get_terminus_node_from_road(road=roses_road) == roses_text


def test_road_get_terminus_node_from_road_CorrectlyReturnsRoadNodeWhenNonDefaultDelimiter():
    # GIVEN
    healer_text = "healer"
    bloomers_text = "bloomers"
    roses_text = "roses"
    slash_text = default_road_delimiter_if_none()
    slash_healer_road = f"{root_label()}{slash_text}{healer_text}"
    slash_bloomers_road = f"{slash_healer_road}{slash_text}{bloomers_text}"
    slash_roses_road = f"{slash_bloomers_road}{slash_text}{roses_text}"

    # WHEN/THENs
    assert get_terminus_node_from_road(root_label(), slash_text) == root_label()
    assert get_terminus_node_from_road(slash_healer_road, slash_text) == healer_text
    assert get_terminus_node_from_road(slash_bloomers_road, slash_text) == bloomers_text
    assert get_terminus_node_from_road(slash_roses_road, slash_text) == roses_text


def test_road_get_root_node_from_road_CorrectlyReturnsRoadNode():
    # GIVEN
    healer_text = "healer"
    healer_road = create_road(root_label(), healer_text)
    bloomers_text = "bloomers"
    bloomers_road = create_road(healer_road, bloomers_text)
    roses_text = "roses"
    roses_road = create_road(healer_text, roses_text)

    # WHEN/THENs
    assert get_root_node_from_road(root_label()) == root_label()
    assert get_root_node_from_road(healer_road) == root_label()
    assert get_root_node_from_road(bloomers_road) == root_label()
    assert get_root_node_from_road(roses_road) == healer_text


def test_road_get_parent_road_from_road_works():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    healer_text = "healer"
    healer_road = f"{root_label()}{x_s}{healer_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{healer_road}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_text}"

    # WHEN/THENs
    assert get_parent_road_from_road(road=root_label()) == ""
    assert get_parent_road_from_road(road=healer_road) == root_label()
    assert get_parent_road_from_road(road=bloomers_road) == healer_road
    assert get_parent_road_from_road(road=roses_road) == bloomers_road


def test_road_create_road_without_root_node_WorksCorrectly():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    healer_text = "healer"
    healer_road = f"{root_label()}{x_s}{healer_text}"
    healer_without_root_road = f"{x_s}{healer_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{healer_text}{x_s}{bloomers_text}"
    bloomers_without_root_road = f"{x_s}{healer_text}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = (
        f"{root_label()}{x_s}{healer_text}{x_s}{bloomers_text}{x_s}{roses_text}"
    )
    roses_without_root_road = f"{x_s}{healer_text}{x_s}{bloomers_text}{x_s}{roses_text}"

    # WHEN/THENs
    assert create_road_without_root_node(road=root_label()) == x_s
    assert create_road_without_root_node(road=healer_road) == healer_without_root_road
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


def test_road_find_replace_road_key_dict_ReturnsCorrectDict_Scenario1():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    old_seasons_road = f"{root_label()}{x_s}healer{x_s}seasons"
    old_sufffact_x = sufffactunit_shop(need=old_seasons_road)
    old_sufffacts_x = {old_sufffact_x.need: old_sufffact_x}

    assert old_sufffacts_x.get(old_seasons_road) == old_sufffact_x

    # WHEN
    new_seasons_road = f"{root_label()}{x_s}healer{x_s}kookies"
    new_sufffacts_x = find_replace_road_key_dict(
        dict_x=old_sufffacts_x, old_road=old_seasons_road, new_road=new_seasons_road
    )
    new_sufffact_x = sufffactunit_shop(need=new_seasons_road)

    assert new_sufffacts_x.get(new_seasons_road) == new_sufffact_x
    assert new_sufffacts_x.get(old_seasons_road) is None


def test_road_find_replace_road_key_dict_ReturnsCorrectDict_ChangeEconomyIDScenario():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    old_economy_id = "El Paso"
    healer_text = "healer"
    old_healer_road = f"{old_economy_id}{x_s}{healer_text}"
    seasons_text = "seasons"
    old_seasons_road = f"{old_healer_road}{x_s}{seasons_text}"
    old_sufffact_x = sufffactunit_shop(need=old_seasons_road)
    old_sufffacts_x = {old_sufffact_x.need: old_sufffact_x}

    assert old_sufffacts_x.get(old_seasons_road) == old_sufffact_x

    # WHEN
    new_economy_id = "Austin"
    new_healer_road = f"{new_economy_id}{x_s}{healer_text}"
    new_seasons_road = f"{new_healer_road}{x_s}{seasons_text}"
    new_sufffacts_x = find_replace_road_key_dict(
        dict_x=old_sufffacts_x, old_road=old_seasons_road, new_road=new_seasons_road
    )
    new_sufffact_x = sufffactunit_shop(need=new_seasons_road)

    assert new_sufffacts_x.get(new_seasons_road) == new_sufffact_x
    assert new_sufffacts_x.get(old_seasons_road) is None


def test_road_get_ancestor_roads_CorrectlyReturnsAncestorRoadUnits():
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


def test_road_get_forefather_roads_CorrectlyReturnsAncestorRoadUnitsWithoutSource():
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


def test_road_get_default_economy_root_roadnode_ReturnsCorrectObj():
    assert root_label() == "A"


def test_road_create_road_from_nodes_WorksCorrectly():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    root_list = get_all_road_nodes(root_label())
    healer_text = "healer"
    healer_road = f"{root_label()}{x_s}{healer_text}"
    healer_list = get_all_road_nodes(healer_road)
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{healer_text}{x_s}{bloomers_text}"
    bloomers_list = get_all_road_nodes(bloomers_road)
    roses_text = "roses"
    roses_road = (
        f"{root_label()}{x_s}{healer_text}{x_s}{bloomers_text}{x_s}{roses_text}"
    )
    roses_list = get_all_road_nodes(roses_road)

    # WHEN / THEN
    assert root_label() == create_road_from_nodes(root_list)
    assert healer_road == create_road_from_nodes(healer_list)
    assert bloomers_road == create_road_from_nodes(bloomers_list)
    assert roses_road == create_road_from_nodes(roses_list)


def test_road_create_road_WorksCorrectly():
    # GIVEN
    x_s = default_road_delimiter_if_none()
    healer_text = "healer"
    healer_road = f"{root_label()}{x_s}{healer_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()}{x_s}{healer_text}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = (
        f"{root_label()}{x_s}{healer_text}{x_s}{bloomers_text}{x_s}{roses_text}"
    )

    # WHEN / THEN
    assert root_label() == create_road(None, root_label())
    assert root_label() == create_road("", root_label())
    assert healer_road == create_road(root_label(), healer_text)
    assert bloomers_road == create_road(healer_road, bloomers_text)
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
    healer_text = "healer"
    healer_road = f"{root_label()}{x_s}{healer_text}"
    bloomers_text = "bloomers"
    bloomers_road = f"{healer_road}{x_s}{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{bloomers_road}{x_s}{roses_text}"

    # WHEN / THEN
    print(f"{healer_road=}")
    print(f"{bloomers_road=}")
    assert get_diff_road(bloomers_road, healer_road) == bloomers_text
    assert get_diff_road(roses_road, bloomers_road) == roses_text
    bloomers_rose_road = create_road(bloomers_text, roses_text)
    print(f"{bloomers_rose_road=}")
    assert get_diff_road(roses_road, healer_road) == bloomers_rose_road


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


def test_replace_road_delimiter_CorrectlyReturnsNewObj():
    # GIVEN
    healer_text = "healer"
    gen_healer_road = create_road(root_label(), healer_text)
    comma_delimiter = default_road_delimiter_if_none()
    comma_delimiter_healer_road = f"{root_label()}{comma_delimiter}{healer_text}"
    assert comma_delimiter == ","
    assert gen_healer_road == comma_delimiter_healer_road

    # WHEN
    slash_delimiter = "/"
    gen_healer_road = replace_road_delimiter(
        gen_healer_road, old_delimiter=comma_delimiter, new_delimiter=slash_delimiter
    )

    # THEN
    slash_delimiter_healer_road = f"{root_label()}{slash_delimiter}{healer_text}"
    assert gen_healer_road == slash_delimiter_healer_road


def test_replace_road_delimiter_CorrectlyRaisesError():
    # GIVEN
    cooker_text = "cooker/cleaner"
    gen_cooker_road = create_road(root_label(), cooker_text)
    comma_delimiter = default_road_delimiter_if_none()
    comma_delimiter_cooker_road = f"{root_label()}{comma_delimiter}{cooker_text}"
    assert comma_delimiter == ","
    assert gen_cooker_road == comma_delimiter_cooker_road

    # WHEN
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

    # WHEN
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


def test_EconomyRoad_Exists():
    # GIVEN
    bob_texas_text = "bob,texas"

    # WHEN
    bob_texas_economyaddress = EconomyAddress(bob_texas_text)

    # THEN
    assert bob_texas_economyaddress != None
    assert bob_texas_economyaddress == bob_texas_text


def test_EconomyAddress_Exists():
    # GIVEN
    bob_texas_text = "bob,texas"

    # WHEN
    bob_texas_economyaddress = EconomyAddress(bob_texas_text)

    # THEN
    assert bob_texas_economyaddress != None
    assert bob_texas_economyaddress == bob_texas_text


def test_create_economyaddress_ReturnsCorrect():
    # GIVEN
    bob_text = "Bob"
    bob_person_id = PersonID(bob_text)
    texas_text = "Texas"
    texas_economy_id = EconomyID(texas_text)

    # WHEN
    bob_texas_economyaddress = create_economyaddress(bob_person_id, texas_economy_id)

    # THEN
    assert bob_texas_economyaddress != None
    bob_texas_road = create_road("Bob", "Texas")
    assert bob_texas_economyaddress == EconomyAddress(bob_texas_road)


def test_PersonRoad_Exists():
    # GIVEN
    texas_road = create_road("bob", "texas")
    sports_road = create_road(texas_road, "sports")

    # WHEN
    sports_personroad = PersonRoad(sports_road)

    # THEN
    assert sports_personroad != None
    assert sports_personroad == sports_road


def test_get_economyaddress_from_personroad_ReturnsCorrectObj():
    # GIVEN
    bob_text = "Bob"
    bob_person_id = PersonID(bob_text)
    texas_text = "Texas"
    texas_economy_id = EconomyID(texas_text)
    sports_road = create_road(
        create_economyaddress(bob_person_id, texas_economy_id), "sports"
    )
    sports_personroad = PersonRoad(sports_road)

    # WHEN
    bob_texas_economyaddress = get_economyaddress_from_personroad(sports_personroad)

    # THEN
    assert bob_texas_economyaddress == create_economyaddress(
        bob_person_id, texas_economy_id
    )


def test_get_economyroad_from_personroad_ReturnsCorrectObj():
    # GIVEN
    bob_text = "bob"
    texas_text = "texas"
    bob_texas_road = create_road(bob_text, texas_text)
    roses_text = "roses"
    bob_roses_road = create_road(bob_texas_road, roses_text)

    # WHEN
    texas_roses_road = get_economyroad_from_personroad(bob_roses_road)

    # THEN
    print(f"{texas_roses_road=}")
    assert texas_roses_road == create_road(texas_text, roses_text)
