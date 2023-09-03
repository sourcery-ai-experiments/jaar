from src.calendar.road import (
    Road,
    change_road,
    is_sub_road_in_src_road,
    get_all_road_nodes_in_list,
    get_terminus_node_from_road,
    find_replace_road_key_dict,
    get_walk_from_road,
    get_road_without_root_node,
    road_validate,
    get_ancestor_roads,
    get_global_root_desc,
)
from src.calendar.required_idea import sufffactunit_shop
from src.calendar.idea import IdeaCore
from pytest import raises as pytest_raises


def test_road_exists():
    new_obj = Road("")
    assert new_obj == ""


def test_road_is_sub_road_in_src_road_correctlyReturnsBool():
    src = "src"
    person = "person"
    bloomers_text = "bloomers"
    bloomers_road = f"{src},{person},{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{src},{person},{bloomers_text},{roses_text}"

    assert is_sub_road_in_src_road(bloomers_road, bloomers_road)
    assert is_sub_road_in_src_road(roses_road, bloomers_road)
    assert is_sub_road_in_src_road(bloomers_road, roses_road) == False


def test_road_road_validate_correctlyReturnsRoad():
    assert road_validate(Road("")) == ""
    assert road_validate(Road(",src")) == ",src"
    assert road_validate(Road("src,fun")) == "src,fun"


def test_road_change_road_correctlyRoad():
    src = "src"
    person = "person"
    bloomers_text = "bloomers"
    bloomers_road = Road(f"{src},{person},{bloomers_text}")
    plants_text = "plants"
    plants_road = Road(f"{src},{person},{plants_text}")
    roses_text = "roses"
    old_roses_road = Road(f"{src},{person},{bloomers_text},{roses_text}")
    new_roses_road = Road(f"{src},{person},{plants_text},{roses_text}")
    # taff_text = "taff"
    # new_roses_road = Road(f"{src},{person},{bloomers_text},{taff_text}")

    print(f"{change_road(old_roses_road, bloomers_road, plants_road)}")

    assert change_road(bloomers_road, bloomers_road, bloomers_road) == bloomers_road
    assert change_road(old_roses_road, bloomers_road, plants_road) == new_roses_road
    assert change_road(old_roses_road, "random_text", plants_road) == old_roses_road


def test_road_get_all_road_nodes_in_list_works():
    # GIVEN
    src_text = "src"
    src_road = Road("src")
    person_text = "person"
    person_road = Road(f"{src_text},{person_text}")
    bloomers_text = "bloomers"
    bloomers_road = Road(f"{src_text},{person_text},{bloomers_text}")
    roses_text = "roses"
    roses_road = Road(f"{src_text},{person_text},{bloomers_text},{roses_text}")

    # WHEN/THENs
    src_list = [src_text]
    assert get_all_road_nodes_in_list(road=src_road) == src_list
    person_list = [src_text, person_text]
    assert get_all_road_nodes_in_list(road=person_road) == person_list
    bloomers_list = [src_text, person_text, bloomers_text]
    assert get_all_road_nodes_in_list(road=bloomers_road) == bloomers_list
    roses_list = [src_text, person_text, bloomers_text, roses_text]
    assert get_all_road_nodes_in_list(road=roses_road) == roses_list


def test_road_get_all_road_nodes_in_list_works():
    # GIVEN
    src_text = "src"
    src_road = Road("src")
    person_text = "person"
    person_road = Road(f"{src_text},{person_text}")
    bloomers_text = "bloomers"
    bloomers_road = Road(f"{src_text},{person_text},{bloomers_text}")
    roses_text = "roses"
    roses_road = Road(f"{src_text},{person_text},{bloomers_text},{roses_text}")

    # WHEN/THENs
    src_list = [src_text]
    assert get_all_road_nodes_in_list(road=src_road) == src_list
    person_list = [src_text, person_text]
    assert get_all_road_nodes_in_list(road=person_road) == person_list
    bloomers_list = [src_text, person_text, bloomers_text]
    assert get_all_road_nodes_in_list(road=bloomers_road) == bloomers_list
    roses_list = [src_text, person_text, bloomers_text, roses_text]
    assert get_all_road_nodes_in_list(road=roses_road) == roses_list


def test_road_get_terminus_node_from_road_works():
    # GIVEN
    src_text = "src"
    src_road = Road("src")
    person_text = "person"
    person_road = Road(f"{src_text},{person_text}")
    bloomers_text = "bloomers"
    bloomers_road = Road(f"{src_text},{person_text},{bloomers_text}")
    roses_text = "roses"
    roses_road = Road(f"{src_text},{person_text},{bloomers_text},{roses_text}")

    # WHEN/THENs
    assert get_terminus_node_from_road(road=src_road) == src_text
    assert get_terminus_node_from_road(road=person_road) == person_text
    assert get_terminus_node_from_road(road=bloomers_road) == bloomers_text
    assert get_terminus_node_from_road(road=roses_road) == roses_text


def test_road_get_walk_from_road_works():
    # GIVEN
    src_text = "src"
    src_road = Road("src")
    person_text = "person"
    person_road = Road(f"{src_text},{person_text}")
    bloomers_text = "bloomers"
    bloomers_road = Road(f"{src_text},{person_text},{bloomers_text}")
    roses_text = "roses"
    roses_road = Road(f"{src_text},{person_text},{bloomers_text},{roses_text}")

    # WHEN/THENs
    assert get_walk_from_road(road=src_road) == ""
    assert get_walk_from_road(road=person_road) == src_road
    assert get_walk_from_road(road=bloomers_road) == person_road
    assert get_walk_from_road(road=roses_road) == bloomers_road


def test_road_get_road_without_root_node_works():
    # GIVEN
    src_text = "src"
    src_road = Road("src")
    person_text = "person"
    person_road = Road(f"{src_text},{person_text}")
    person_without_src_road = Road(f",{person_text}")
    bloomers_text = "bloomers"
    bloomers_road = Road(f"{src_text},{person_text},{bloomers_text}")
    bloomers_without_src_road = Road(f",{person_text},{bloomers_text}")
    roses_text = "roses"
    roses_road = Road(f"{src_text},{person_text},{bloomers_text},{roses_text}")
    roses_without_src_road = Road(f",{person_text},{bloomers_text},{roses_text}")

    # WHEN/THENs
    assert get_road_without_root_node(road=src_road) == ","
    assert get_road_without_root_node(road=person_road) == person_without_src_road
    assert get_road_without_root_node(road=bloomers_road) == bloomers_without_src_road
    assert get_road_without_root_node(road=roses_road) == roses_without_src_road
    road_without_node = get_road_without_root_node(road=roses_road)
    with pytest_raises(Exception) as excinfo:
        get_road_without_root_node(road=road_without_node)
    assert (
        str(excinfo.value)
        == f"Cannot get_road_without_root_node of '{road_without_node}' because it has no root node."
    )


def test_find_replace_road_key_dict_ReturnsCorrectDict_Scenario1():
    # GIVEN
    old_seasons_road = "src,person,seasons"
    old_sufffact_x = sufffactunit_shop(need=old_seasons_road)
    old_sufffacts_x = {old_sufffact_x.need: old_sufffact_x}

    assert old_sufffacts_x.get(old_seasons_road) == old_sufffact_x

    # WHEN
    new_seasons_road = "src,person,kookies"
    new_sufffacts_x = find_replace_road_key_dict(
        dict_x=old_sufffacts_x, old_road=old_seasons_road, new_road=new_seasons_road
    )
    new_sufffact_x = sufffactunit_shop(need=new_seasons_road)

    assert new_sufffacts_x.get(new_seasons_road) == new_sufffact_x
    assert new_sufffacts_x.get(old_seasons_road) is None


# def test_find_replace_road_key_dict_ReturnsCorrectDict_Scenario2():
#     # sourcery skip: extract-duplicate-method
#     # GIVEN
#     src = "src"
#     person_text = "person"
#     person_road = Road(f"{src},{person_text}")
#     bloomers_text = "bloomers"
#     bloomers_road = Road(f"{src},{person_text},{bloomers_text}")
#     old_roses_text = "roses"
#     old_roses_road = Road(f"{src},{person_text},{bloomers_text},{old_roses_text}")
#     idea_roses = IdeaCore(_desc=old_roses_text, _walk=bloomers_road)
#     idea_bloomers = IdeaCore(_desc=bloomers_text, _walk=person_road)
#     idea_bloomers.add_kid(idea_kid=idea_roses)

#     for idea_key, idea_obj in idea_bloomers._kids.items():
#         assert idea_key == old_roses_text
#         assert idea_obj.get_key_road() == old_roses_text
#         assert idea_obj._desc == old_roses_text

#     # WHEN
#     new_roses_text = "roses2"
#     new_roses_road = Road(f"src,person,{new_roses_text}")
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
#         assert idea_obj._desc == new_roses_text
#     assert new_kids_x.get(old_roses_road) is None


def test_get_ancestor_roads_CorrectlyReturnsAncestorRoads():
    road = "src,nation-state,USA,Texas"
    x_roads = get_ancestor_roads(road=road)
    assert x_roads != None
    texas_ancestor_roads = [
        "src,nation-state,USA,Texas",
        "src,nation-state,USA",
        "src,nation-state",
        "src",
    ]
    assert x_roads == texas_ancestor_roads


def test_get_global_root_desc_ReturnsCorrectObj():
    assert get_global_root_desc() == "A"
