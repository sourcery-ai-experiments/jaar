from src.contract.road import (
    Road,
    change_road,
    is_sub_road,
    get_all_road_nodes,
    get_terminus_node_from_road,
    find_replace_road_key_dict,
    get_walk_from_road,
    get_road_without_root_node,
    road_validate,
    get_ancestor_roads,
    get_forefather_roads,
    get_default_economy_root_label as root_label,
    get_road_from_nodes,
)
from src.contract.required_idea import sufffactunit_shop
from src.contract.idea import IdeaCore
from pytest import raises as pytest_raises


def test_road_exists():
    new_obj = Road("")
    assert new_obj == ""


def test_road_is_sub_road_correctlyReturnsBool():
    owner = "owner"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_label()},{owner},{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{root_label()},{owner},{bloomers_text},{roses_text}"

    assert is_sub_road(bloomers_road, bloomers_road)
    assert is_sub_road(roses_road, bloomers_road)
    assert is_sub_road(bloomers_road, roses_road) == False


def test_road_road_validate_correctlyReturnsRoad():
    assert road_validate(None) == ""
    assert road_validate(Road("")) == ""
    assert road_validate(Road(f"{root_label()},casa")) == f"{root_label()},casa"
    assert road_validate(Road("A,casa")) == f"{root_label()},casa"
    assert road_validate(Road(",source")) == f"{root_label()},source"
    assert road_validate(Road("source,fun")) == f"{root_label()},fun"
    assert road_validate(Road("source")) == root_label()
    assert road_validate(Road("AA,casa")) == f"{root_label()},casa"


def test_road_change_road_correctlyRoad():
    owner = "owner"
    bloomers_text = "bloomers"
    bloomers_road = Road(f"{root_label()},{owner},{bloomers_text}")
    plants_text = "plants"
    plants_road = Road(f"{root_label()},{owner},{plants_text}")
    roses_text = "roses"
    old_roses_road = Road(f"{root_label()},{owner},{bloomers_text},{roses_text}")
    new_roses_road = Road(f"{root_label()},{owner},{plants_text},{roses_text}")
    # taff_text = "taff"
    # new_roses_road = Road(f"{root_label()},{owner},{bloomers_text},{taff_text}")

    print(f"{change_road(old_roses_road, bloomers_road, plants_road)}")

    assert change_road(bloomers_road, bloomers_road, bloomers_road) == bloomers_road
    assert change_road(old_roses_road, bloomers_road, plants_road) == new_roses_road
    assert change_road(old_roses_road, "random_text", plants_road) == old_roses_road


def test_road_get_all_road_nodes_works():
    # GIVEN
    owner_text = "owner"
    owner_road = Road(f"{root_label()},{owner_text}")
    bloomers_text = "bloomers"
    bloomers_road = Road(f"{root_label()},{owner_text},{bloomers_text}")
    roses_text = "roses"
    roses_road = Road(f"{root_label()},{owner_text},{bloomers_text},{roses_text}")

    # WHEN/THENs
    root_list = [root_label()]
    assert get_all_road_nodes(road=root_label()) == root_list
    owner_list = [root_label(), owner_text]
    assert get_all_road_nodes(road=owner_road) == owner_list
    bloomers_list = [root_label(), owner_text, bloomers_text]
    assert get_all_road_nodes(road=bloomers_road) == bloomers_list
    roses_list = [root_label(), owner_text, bloomers_text, roses_text]
    assert get_all_road_nodes(road=roses_road) == roses_list


def test_road_get_terminus_node_from_road_works():
    # GIVEN
    owner_text = "owner"
    owner_road = Road(f"{root_label()},{owner_text}")
    bloomers_text = "bloomers"
    bloomers_road = Road(f"{root_label()},{owner_text},{bloomers_text}")
    roses_text = "roses"
    roses_road = Road(f"{root_label()},{owner_text},{bloomers_text},{roses_text}")

    # WHEN/THENs
    assert get_terminus_node_from_road(road=root_label()) == root_label()
    assert get_terminus_node_from_road(road=owner_road) == owner_text
    assert get_terminus_node_from_road(road=bloomers_road) == bloomers_text
    assert get_terminus_node_from_road(road=roses_road) == roses_text


def test_road_get_walk_from_road_works():
    # GIVEN
    owner_text = "owner"
    owner_road = Road(f"{root_label()},{owner_text}")
    bloomers_text = "bloomers"
    bloomers_road = Road(f"{root_label()},{owner_text},{bloomers_text}")
    roses_text = "roses"
    roses_road = Road(f"{root_label()},{owner_text},{bloomers_text},{roses_text}")

    # WHEN/THENs
    assert get_walk_from_road(road=root_label()) == ""
    assert get_walk_from_road(road=owner_road) == root_label()
    assert get_walk_from_road(road=bloomers_road) == owner_road
    assert get_walk_from_road(road=roses_road) == bloomers_road


def test_road_get_road_without_root_node_WorksCorrectly():
    # GIVEN
    owner_text = "owner"
    owner_road = Road(f"{root_label()},{owner_text}")
    owner_without_root_road = Road(f",{owner_text}")
    bloomers_text = "bloomers"
    bloomers_road = Road(f"{root_label()},{owner_text},{bloomers_text}")
    bloomers_without_root_road = Road(f",{owner_text},{bloomers_text}")
    roses_text = "roses"
    roses_road = Road(f"{root_label()},{owner_text},{bloomers_text},{roses_text}")
    roses_without_root_road = Road(f",{owner_text},{bloomers_text},{roses_text}")

    # WHEN/THENs
    assert get_road_without_root_node(road=root_label()) == ","
    assert get_road_without_root_node(road=owner_road) == owner_without_root_road
    assert get_road_without_root_node(road=bloomers_road) == bloomers_without_root_road
    assert get_road_without_root_node(road=roses_road) == roses_without_root_road
    road_without_node = get_road_without_root_node(road=roses_road)
    with pytest_raises(Exception) as excinfo:
        get_road_without_root_node(road=road_without_node)
    assert (
        str(excinfo.value)
        == f"Cannot get_road_without_root_node of '{road_without_node}' because it has no root node."
    )


def test_road_find_replace_road_key_dict_ReturnsCorrectDict_Scenario1():
    # GIVEN
    old_seasons_road = f"{root_label()},owner,seasons"
    old_sufffact_x = sufffactunit_shop(need=old_seasons_road)
    old_sufffacts_x = {old_sufffact_x.need: old_sufffact_x}

    assert old_sufffacts_x.get(old_seasons_road) == old_sufffact_x

    # WHEN
    new_seasons_road = f"{root_label()},owner,kookies"
    new_sufffacts_x = find_replace_road_key_dict(
        dict_x=old_sufffacts_x, old_road=old_seasons_road, new_road=new_seasons_road
    )
    new_sufffact_x = sufffactunit_shop(need=new_seasons_road)

    assert new_sufffacts_x.get(new_seasons_road) == new_sufffact_x
    assert new_sufffacts_x.get(old_seasons_road) is None


def test_road_find_replace_road_key_dict_ReturnsCorrectDict_ChangeEconomyTagScenario():
    # GIVEN
    old_economy_tag = "El Paso"
    owner_text = "owner"
    old_owner_road = f"{old_economy_tag},{owner_text}"
    seasons_text = "seasons"
    old_seasons_road = f"{old_owner_road},{seasons_text}"
    old_sufffact_x = sufffactunit_shop(need=old_seasons_road)
    old_sufffacts_x = {old_sufffact_x.need: old_sufffact_x}

    assert old_sufffacts_x.get(old_seasons_road) == old_sufffact_x

    # WHEN
    new_economy_tag = "Austin"
    new_owner_road = f"{new_economy_tag},{owner_text}"
    new_seasons_road = f"{new_owner_road},{seasons_text}"
    new_sufffacts_x = find_replace_road_key_dict(
        dict_x=old_sufffacts_x, old_road=old_seasons_road, new_road=new_seasons_road
    )
    new_sufffact_x = sufffactunit_shop(need=new_seasons_road)

    assert new_sufffacts_x.get(new_seasons_road) == new_sufffact_x
    assert new_sufffacts_x.get(old_seasons_road) is None


# def test_find_replace_road_key_dict_ReturnsCorrectDict_Scenario2():
#     # sourcery skip: extract-duplicate-method
#     # GIVEN
#     src = f"{root_label()}"
#     owner_text = "owner"
#     owner_road = Road(f"{root_label()},{owner_text}")
#     bloomers_text = "bloomers"
#     bloomers_road = Road(f"{root_label()},{owner_text},{bloomers_text}")
#     old_roses_text = "roses"
#     old_roses_road = Road(f"{root_label()},{owner_text},{bloomers_text},{old_roses_text}")
#     idea_roses = IdeaCore(_label=old_roses_text, _walk=bloomers_road)
#     idea_bloomers = IdeaCore(_label=bloomers_text, _walk=owner_road)
#     idea_bloomers.add_kid(idea_kid=idea_roses)

#     for idea_key, idea_obj in idea_bloomers._kids.items():
#         assert idea_key == old_roses_text
#         assert idea_obj.get_key_road() == old_roses_text
#         assert idea_obj._label == old_roses_text

#     # WHEN
#     new_roses_text = "roses2"
#     new_roses_road = Road(ff"{root_label()},owner,{new_roses_text}")
#     new_kids_x = find_replace_road_key_dict(
#         dict_x=idea_bloomers._kids,
#         old_road=old_roses_road,
#         new_road=new_roses_road,
#         key_is_last_node=True,
#     )

#     # THEN
#     for idea_key, idea_obj in new_kids_x.items():
#         assert idea_key == new_roses_text
#         assert idea_obj.get_key_road() == new_roses_text
#         assert idea_obj._label == new_roses_text
#     assert new_kids_x.get(old_roses_road) is None


def test_road_get_ancestor_roads_CorrectlyReturnsAncestorRoads():
    # GIVEN
    nation_text = "nation-state"
    nation_road = f"{root_label()},{nation_text}"
    usa_text = "USA"
    usa_road = f"{nation_road},{usa_text}"
    texas_text = "Texas"
    texas_road = f"{usa_road},{texas_text}"

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


def test_road_get_forefather_roads_CorrectlyReturnsAncestorRoadsWithoutSource():
    # GIVEN
    nation_text = "nation-state"
    nation_road = f"{root_label()},{nation_text}"
    usa_text = "USA"
    usa_road = f"{nation_road},{usa_text}"
    texas_text = "Texas"
    texas_road = f"{usa_road},{texas_text}"

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


def test_road_get_default_economy_root_label_ReturnsCorrectObj():
    assert root_label() == "A"


def test_road_get_road_from_nodes_WorksCorrectly():
    # GIVEN
    root_list = get_all_road_nodes(root_label())
    owner_text = "owner"
    owner_road = Road(f"{root_label()},{owner_text}")
    owner_list = get_all_road_nodes(owner_road)
    bloomers_text = "bloomers"
    bloomers_road = Road(f"{root_label()},{owner_text},{bloomers_text}")
    bloomers_list = get_all_road_nodes(bloomers_road)
    roses_text = "roses"
    roses_road = Road(f"{root_label()},{owner_text},{bloomers_text},{roses_text}")
    roses_list = get_all_road_nodes(roses_road)

    # WHEN / THEN
    assert root_label() == get_road_from_nodes(root_list)
    assert owner_road == get_road_from_nodes(owner_list)
    assert bloomers_road == get_road_from_nodes(bloomers_list)
    assert roses_road == get_road_from_nodes(roses_list)
