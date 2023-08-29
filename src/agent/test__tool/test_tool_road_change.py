from src.agent.tool import ToolCore
from src.agent.required import RequiredUnit, sufffactunit_shop, Road, acptfactunit_shop
from pytest import raises as pytest_raises


def test_tool_find_replace_road_Changes_walk():
    # GIVEN Tool with _walk that will be changed
    src = "src"
    old_person = "person1"
    bloomers_text = "bloomers"
    bloomers_road = f"{src},{old_person},{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{src},{old_person},{bloomers_text},{roses_text}"
    tool_x = ToolCore(_desc=roses_text, _walk=bloomers_road)
    assert Road(f"{tool_x._walk}") == bloomers_road
    assert Road(f"{tool_x._walk},{tool_x._desc}") == roses_road

    # WHEN
    new_person = "person1"
    old_person_road = f"{src},{old_person}"
    new_person_road = f"{src},{new_person}"
    tool_x.find_replace_road(old_road=old_person_road, new_road=new_person_road)

    # THEN
    new_bloomers_road = f"{src},{new_person},{bloomers_text}"
    new_roses_road = f"{src},{new_person},{bloomers_text},{roses_text}"
    assert Road(f"{tool_x._walk}") == new_bloomers_road
    assert Road(f"{tool_x._walk},{tool_x._desc}") == new_roses_road


def test_tool_find_replace_road_Changes_special_road_numeric_road():
    # GIVEN Tool with special road and numeric road that will be changed
    src = "src"
    person = "person"
    bloomers_text = "bloomers"
    bloomers_road = f"{src},{person},{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{src},{person},{bloomers_text},{roses_text}"
    old_water_text = "water"
    old_water_road = f"{src},{old_water_text}"
    rain_text = "rain"
    snow_text = "snow"
    old_rain_road = f"{src},{old_water_text},{rain_text}"
    old_snow_road = f"{src},{old_water_text},{snow_text}"
    farm_text = "farm"
    farm_road = f"{src},{farm_text}"
    fertilizer_text = "fertilizer"
    fertilizer_road = f"{src},{farm_text},{fertilizer_text}"
    farm_road = f"{src},{farm_text}"
    tool_x = ToolCore(
        _desc=roses_text,
        _walk=bloomers_road,
        _special_road=old_rain_road,
        _numeric_road=old_snow_road,
    )
    assert tool_x._special_road == old_rain_road
    assert tool_x._numeric_road == old_snow_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = f"{src},{new_water_text}"
    new_rain_road = f"{src},{new_water_text},{rain_text}"
    new_snow_road = f"{src},{new_water_text},{snow_text}"
    tool_x.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert tool_x._special_road == new_rain_road
    assert tool_x._numeric_road == new_snow_road


def test_tool_find_replace_road_Changes_requiredunits():
    # GIVEN Tool with required that will be changed
    src = "src"
    person = "person"
    bloomers_text = "bloomers"
    roses_text = "roses"
    roses_road = f"{src},{person},{bloomers_text},{roses_text}"
    # required roads
    old_water_text = "water"
    old_water_road = f"{src},{old_water_text}"
    rain_text = "rain"
    old_rain_road = f"{src},{old_water_text},{rain_text}"
    # create requiredunit
    sufffact_x = sufffactunit_shop(need=old_rain_road)
    sufffacts_x = {sufffact_x.need: sufffact_x}
    required_x = RequiredUnit(base=old_water_road, sufffacts=sufffacts_x)
    requireds_x = {required_x.base: required_x}
    tool_x = ToolCore(_desc=roses_text, _requiredunits=requireds_x)
    # confirm asserts
    assert tool_x._requiredunits.get(old_water_road) != None
    old_water_rain_required = tool_x._requiredunits[old_water_road]
    assert old_water_rain_required.base == old_water_road
    assert old_water_rain_required.sufffacts.get(old_rain_road) != None
    water_rain_l_sufffact = old_water_rain_required.sufffacts[old_rain_road]
    assert water_rain_l_sufffact.need == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = f"{src},{new_water_text}"
    assert tool_x._requiredunits.get(new_water_road) is None
    tool_x.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert tool_x._requiredunits.get(old_water_road) is None
    assert tool_x._requiredunits.get(new_water_road) != None
    new_water_rain_required = tool_x._requiredunits[new_water_road]
    assert new_water_rain_required.base == new_water_road
    new_rain_road = f"{src},{new_water_text},{rain_text}"
    assert new_water_rain_required.sufffacts.get(old_rain_road) is None
    assert new_water_rain_required.sufffacts.get(new_rain_road) != None
    new_water_rain_l_sufffact = new_water_rain_required.sufffacts[new_rain_road]
    assert new_water_rain_l_sufffact.need == new_rain_road

    print(f"{len(tool_x._requiredunits)=}")
    required_obj = tool_x._requiredunits.get(new_water_road)
    assert required_obj != None

    print(f"{len(required_obj.sufffacts)=}")
    sufffact_obj = required_obj.sufffacts.get(new_rain_road)
    assert sufffact_obj != None
    assert sufffact_obj.need == new_rain_road


def test_tool_find_replace_road_Changes_acptfactunits():
    # GIVEN Tool with acptfactunit that will be changed
    src = "src"
    person = "person"
    bloomers_text = "bloomers"
    # bloomers_road = f"{src},{person},{bloomers_text}"
    roses_text = "roses"
    # roses_road = f"{src},{person},{bloomers_text},{roses_text}"
    old_water_text = "water"
    old_water_road = f"{src},{old_water_text}"
    rain_text = "rain"
    old_rain_road = f"{src},{old_water_text},{rain_text}"

    acptfactunit_x = acptfactunit_shop(base=old_water_road, pick=old_rain_road)
    acptfactunits_x = {acptfactunit_x.base: acptfactunit_x}
    tool_x = ToolCore(_desc=roses_text, _acptfactunits=acptfactunits_x)
    assert tool_x._acptfactunits[old_water_road] != None
    old_water_rain_acptfactunit = tool_x._acptfactunits[old_water_road]
    assert old_water_rain_acptfactunit.base == old_water_road
    assert old_water_rain_acptfactunit.pick == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = f"{src},{new_water_text}"
    assert tool_x._acptfactunits.get(new_water_road) is None
    tool_x.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert tool_x._acptfactunits.get(old_water_road) is None
    assert tool_x._acptfactunits.get(new_water_road) != None
    new_water_rain_acptfactunit = tool_x._acptfactunits[new_water_road]
    assert new_water_rain_acptfactunit.base == new_water_road
    new_rain_road = f"{src},{new_water_text},{rain_text}"
    assert new_water_rain_acptfactunit.pick == new_rain_road

    print(f"{len(tool_x._acptfactunits)=}")
    acptfactunit_obj = tool_x._acptfactunits.get(new_water_road)
    assert acptfactunit_obj != None
    assert acptfactunit_obj.base == new_water_road
    assert acptfactunit_obj.pick == new_rain_road


def test_tool_get_key_road_returnsCorrectInfo():
    red_text = "red"
    tool_red = ToolCore(_desc=red_text)
    assert tool_red.get_key_road() == red_text
