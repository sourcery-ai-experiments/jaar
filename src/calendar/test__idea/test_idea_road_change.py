from src.calendar.idea import IdeaCore
from src.calendar.required_idea import (
    RequiredUnit,
    sufffactunit_shop,
    Road,
    acptfactunit_shop,
)
from src.calendar.road import get_global_root_desc as root_desc
from pytest import raises as pytest_raises


def test_idea_find_replace_road_Changes_walk():
    # GIVEN Idea with _walk that will be changed
    old_person = "person1"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_desc()},{old_person},{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{root_desc()},{old_person},{bloomers_text},{roses_text}"
    idea_x = IdeaCore(_desc=roses_text, _walk=bloomers_road)
    assert Road(f"{idea_x._walk}") == bloomers_road
    assert Road(f"{idea_x._walk},{idea_x._desc}") == roses_road

    # WHEN
    new_person = "person1"
    old_person_road = f"{root_desc()},{old_person}"
    new_person_road = f"{root_desc()},{new_person}"
    idea_x.find_replace_road(old_road=old_person_road, new_road=new_person_road)

    # THEN
    new_bloomers_road = f"{root_desc()},{new_person},{bloomers_text}"
    new_roses_road = f"{root_desc()},{new_person},{bloomers_text},{roses_text}"
    assert Road(f"{idea_x._walk}") == new_bloomers_road
    assert Road(f"{idea_x._walk},{idea_x._desc}") == new_roses_road


def test_idea_find_replace_road_Changes_special_road_numeric_road():
    # GIVEN Idea with special road and numeric road that will be changed
    person = "person"
    bloomers_text = "bloomers"
    bloomers_road = f"{root_desc()},{person},{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{root_desc()},{person},{bloomers_text},{roses_text}"
    old_water_text = "water"
    old_water_road = f"{root_desc()},{old_water_text}"
    rain_text = "rain"
    snow_text = "snow"
    old_rain_road = f"{root_desc()},{old_water_text},{rain_text}"
    old_snow_road = f"{root_desc()},{old_water_text},{snow_text}"
    farm_text = "farm"
    farm_road = f"{root_desc()},{farm_text}"
    fertilizer_text = "fertilizer"
    fertilizer_road = f"{root_desc()},{farm_text},{fertilizer_text}"
    farm_road = f"{root_desc()},{farm_text}"
    idea_x = IdeaCore(
        _desc=roses_text,
        _walk=bloomers_road,
        _special_road=old_rain_road,
        _numeric_road=old_snow_road,
    )
    assert idea_x._special_road == old_rain_road
    assert idea_x._numeric_road == old_snow_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = f"{root_desc()},{new_water_text}"
    new_rain_road = f"{root_desc()},{new_water_text},{rain_text}"
    new_snow_road = f"{root_desc()},{new_water_text},{snow_text}"
    idea_x.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert idea_x._special_road == new_rain_road
    assert idea_x._numeric_road == new_snow_road


def test_idea_find_replace_road_Changes_requiredunits():
    # GIVEN Idea with required that will be changed
    person = "person"
    bloomers_text = "bloomers"
    roses_text = "roses"
    roses_road = f"{root_desc()},{person},{bloomers_text},{roses_text}"
    # required roads
    old_water_text = "water"
    old_water_road = f"{root_desc()},{old_water_text}"
    rain_text = "rain"
    old_rain_road = f"{root_desc()},{old_water_text},{rain_text}"
    # create requiredunit
    sufffact_x = sufffactunit_shop(need=old_rain_road)
    sufffacts_x = {sufffact_x.need: sufffact_x}
    required_x = RequiredUnit(base=old_water_road, sufffacts=sufffacts_x)
    requireds_x = {required_x.base: required_x}
    idea_x = IdeaCore(_desc=roses_text, _requiredunits=requireds_x)
    # confirm asserts
    assert idea_x._requiredunits.get(old_water_road) != None
    old_water_rain_required = idea_x._requiredunits[old_water_road]
    assert old_water_rain_required.base == old_water_road
    assert old_water_rain_required.sufffacts.get(old_rain_road) != None
    water_rain_l_sufffact = old_water_rain_required.sufffacts[old_rain_road]
    assert water_rain_l_sufffact.need == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = f"{root_desc()},{new_water_text}"
    assert idea_x._requiredunits.get(new_water_road) is None
    idea_x.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert idea_x._requiredunits.get(old_water_road) is None
    assert idea_x._requiredunits.get(new_water_road) != None
    new_water_rain_required = idea_x._requiredunits[new_water_road]
    assert new_water_rain_required.base == new_water_road
    new_rain_road = f"{root_desc()},{new_water_text},{rain_text}"
    assert new_water_rain_required.sufffacts.get(old_rain_road) is None
    assert new_water_rain_required.sufffacts.get(new_rain_road) != None
    new_water_rain_l_sufffact = new_water_rain_required.sufffacts[new_rain_road]
    assert new_water_rain_l_sufffact.need == new_rain_road

    print(f"{len(idea_x._requiredunits)=}")
    required_obj = idea_x._requiredunits.get(new_water_road)
    assert required_obj != None

    print(f"{len(required_obj.sufffacts)=}")
    sufffact_obj = required_obj.sufffacts.get(new_rain_road)
    assert sufffact_obj != None
    assert sufffact_obj.need == new_rain_road


def test_idea_find_replace_road_Changes_acptfactunits():
    # GIVEN Idea with acptfactunit that will be changed
    person = "person"
    bloomers_text = "bloomers"
    # bloomers_road = f"{root_desc()},{person},{bloomers_text}"
    roses_text = "roses"
    # roses_road = f"{root_desc()},{person},{bloomers_text},{roses_text}"
    old_water_text = "water"
    old_water_road = f"{root_desc()},{old_water_text}"
    rain_text = "rain"
    old_rain_road = f"{root_desc()},{old_water_text},{rain_text}"

    acptfactunit_x = acptfactunit_shop(base=old_water_road, pick=old_rain_road)
    acptfactunits_x = {acptfactunit_x.base: acptfactunit_x}
    idea_x = IdeaCore(_desc=roses_text, _acptfactunits=acptfactunits_x)
    assert idea_x._acptfactunits[old_water_road] != None
    old_water_rain_acptfactunit = idea_x._acptfactunits[old_water_road]
    assert old_water_rain_acptfactunit.base == old_water_road
    assert old_water_rain_acptfactunit.pick == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = f"{root_desc()},{new_water_text}"
    assert idea_x._acptfactunits.get(new_water_road) is None
    idea_x.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert idea_x._acptfactunits.get(old_water_road) is None
    assert idea_x._acptfactunits.get(new_water_road) != None
    new_water_rain_acptfactunit = idea_x._acptfactunits[new_water_road]
    assert new_water_rain_acptfactunit.base == new_water_road
    new_rain_road = f"{root_desc()},{new_water_text},{rain_text}"
    assert new_water_rain_acptfactunit.pick == new_rain_road

    print(f"{len(idea_x._acptfactunits)=}")
    acptfactunit_obj = idea_x._acptfactunits.get(new_water_road)
    assert acptfactunit_obj != None
    assert acptfactunit_obj.base == new_water_road
    assert acptfactunit_obj.pick == new_rain_road


def test_idea_get_key_road_returnsCorrectInfo():
    red_text = "red"
    idea_red = IdeaCore(_desc=red_text)
    assert idea_red.get_key_road() == red_text
