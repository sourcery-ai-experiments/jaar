from src.agent.agent import AgentUnit
from src.agent.tool import ToolKid
from src.agent.examples.example_agents import (
    get_agent_with_4_levels_and_2requireds_2acptfacts,
)
from pytest import raises as pytest_raises
from src.agent.required import Road, AcptFactUnit


def test_tool_desc_fails_when_tool_does_not_exist():
    # GIVEN
    src = "src"
    work_text = "work"
    work_road = f"{src},{work_text}"
    swim_text = "swim"
    sx = AgentUnit(_desc=src)
    sx.add_tool(walk=src, tool_kid=ToolKid(_desc=work_text))
    sx.add_tool(walk=work_road, tool_kid=ToolKid(_desc=swim_text))

    # When/Then
    no_tool_road = Road(f"{src},bees")
    with pytest_raises(Exception) as excinfo:
        sx.edit_tool_desc(old_road=no_tool_road, new_desc="pigeons")
    assert (
        str(excinfo.value)
        == f"Getting tool_desc='bees' failed no item at '{no_tool_road}'"
    )


# when editing a tool description it's possible that the change breaks a required.base, sufffact.need or acptfact.base or acptfact.acptfact
# fixing this quickly looks difficult. Maybe push it off
def test_where_level0_tool_desc_change_breaks_tool_walk_of_child_tools():
    # GIVEN
    src = "src"
    work_text = "work"
    work_road = f"{src},{work_text}"
    swim_text = "swim"
    swim_road = f"{src},{work_text},{swim_text}"
    sx = AgentUnit(_desc=src)
    sx.add_tool(walk=src, tool_kid=ToolKid(_desc=work_text))
    sx.add_tool(walk=work_road, tool_kid=ToolKid(_desc=swim_text))
    assert sx._desc == src
    assert sx._toolroot._desc == src
    work_tool = sx.get_tool_kid(road=work_road)
    assert work_tool._walk == src
    swim_tool = sx.get_tool_kid(road=swim_road)
    assert swim_tool._walk == work_road

    # WHEN
    moon = "moon"
    sx.edit_tool_desc(old_road=src, new_desc=moon)

    # THEN
    assert sx._desc == src  # does not change agent name
    assert sx._toolroot._desc == moon
    assert sx._toolroot._walk == ""
    assert work_tool._walk == moon
    assert swim_tool._walk == f"{moon},{work_text}"


def test_tool_find_replace_road_Changes_kids_scenario1():
    # GIVEN Tool with kids that will be changed
    src = "src"
    old_person_text = "person"
    old_person_road = Road(f"{src},{old_person_text}")
    bloomers_text = "bloomers"
    old_bloomers_road = Road(f"{src},{old_person_text},{bloomers_text}")
    roses_text = "roses"
    old_roses_road = Road(f"{src},{old_person_text},{bloomers_text},{roses_text}")
    red_text = "red"
    old_red_road = Road(
        f"{src},{old_person_text},{bloomers_text},{roses_text},{red_text}"
    )

    sx = AgentUnit(_desc=src)
    sx.add_tool(walk=src, tool_kid=ToolKid(_desc=old_person_text))
    sx.add_tool(walk=old_person_road, tool_kid=ToolKid(_desc=bloomers_text))
    sx.add_tool(walk=old_bloomers_road, tool_kid=ToolKid(_desc=roses_text))
    sx.add_tool(walk=old_roses_road, tool_kid=ToolKid(_desc=red_text))
    r_tool_roses = sx.get_tool_kid(old_roses_road)
    r_tool_bloomers = sx.get_tool_kid(old_bloomers_road)

    assert r_tool_bloomers._kids.get(roses_text) != None
    assert r_tool_roses._walk == old_bloomers_road
    assert r_tool_roses._kids.get(red_text) != None
    r_tool_red = r_tool_roses._kids.get(red_text)
    assert r_tool_red._walk == old_roses_road

    # WHEN
    new_person_text = "globe"
    new_person_road = Road(f"{src},{new_person_text}")
    sx.edit_tool_desc(old_road=old_person_road, new_desc=new_person_text)

    # THEN
    assert sx._toolroot._kids.get(new_person_text) != None
    assert sx._toolroot._kids.get(old_person_text) is None

    assert r_tool_bloomers._walk == new_person_road
    assert r_tool_bloomers._kids.get(roses_text) != None

    r_tool_roses = r_tool_bloomers._kids.get(roses_text)
    new_bloomers_road = Road(f"{src},{new_person_text},{bloomers_text}")
    assert r_tool_roses._walk == new_bloomers_road
    assert r_tool_roses._kids.get(red_text) != None
    r_tool_red = r_tool_roses._kids.get(red_text)
    new_roses_road = Road(f"{src},{new_person_text},{bloomers_text},{roses_text}")
    assert r_tool_red._walk == new_roses_road


def test_agent_edit_tool_desc_Changes_acptfactunits():
    # GIVEN agent with acptfactunits that will be changed
    src = "src"
    person = "person"
    bloomers_text = "bloomers"
    bloomers_road = f"{src},{person},{bloomers_text}"
    roses_text = "roses"
    roses_road = f"{src},{person},{bloomers_text},{roses_text}"
    old_water_text = "water"
    old_water_road = f"{src},{old_water_text}"
    rain_text = "rain"
    old_rain_road = f"{src},{old_water_text},{rain_text}"

    sx = AgentUnit(_desc=src)
    sx.add_tool(walk=src, tool_kid=ToolKid(_desc=person))
    sx.add_tool(walk=bloomers_road, tool_kid=ToolKid(_desc=roses_text))
    sx.add_tool(walk=old_water_road, tool_kid=ToolKid(_desc=rain_text))
    sx.set_acptfact(base=old_water_road, pick=old_rain_road)

    tool_x = sx.get_tool_kid(road=roses_road)
    assert sx._toolroot._acptfactunits[old_water_road] != None
    old_water_rain_acptfactunit = sx._toolroot._acptfactunits[old_water_road]
    assert old_water_rain_acptfactunit.base == old_water_road
    assert old_water_rain_acptfactunit.pick == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = f"{src},{new_water_text}"
    sx.add_tool(walk=src, tool_kid=ToolKid(_desc=new_water_text))
    assert sx._toolroot._acptfactunits.get(new_water_road) is None
    sx.edit_tool_desc(old_road=old_water_road, new_desc=new_water_text)

    # THEN
    assert sx._toolroot._acptfactunits.get(old_water_road) is None
    assert sx._toolroot._acptfactunits.get(new_water_road) != None
    new_water_rain_acptfactunit = sx._toolroot._acptfactunits[new_water_road]
    assert new_water_rain_acptfactunit.base == new_water_road
    new_rain_road = f"{src},{new_water_text},{rain_text}"
    assert new_water_rain_acptfactunit.pick == new_rain_road

    assert sx._toolroot._acptfactunits.get(new_water_road)
    acptfactunit_obj = sx._toolroot._acptfactunits.get(new_water_road)
    # for acptfactunit_key, acptfactunit_obj in sx._toolroot._acptfactunits.items():
    #     assert acptfactunit_key == new_water_road
    assert acptfactunit_obj.base == new_water_road
    assert acptfactunit_obj.pick == new_rain_road


def test_agent_edit_tool_desc_ChangesToolRoot_special_road():
    # GIVEN this should never happen but it's not currently banned
    src = "src"
    old_person_text = "person"
    old_person_road = Road(f"{src},{old_person_text}")
    sx = AgentUnit(_desc=src)
    sx.add_tool(walk=src, tool_kid=ToolKid(_desc=old_person_text))
    sx.edit_tool_attr(road=src, special_road=old_person_road)
    assert sx._toolroot._special_road == old_person_road

    # WHEN
    new_person_text = "globe"
    sx.edit_tool_desc(old_road=old_person_road, new_desc=new_person_text)

    # THEN
    new_person_road = Road(f"{src},{new_person_text}")
    assert sx._toolroot._special_road == new_person_road


def test_agent_edit_tool_desc_ChangesToolKidN_special_road():
    src = "src"
    person_text = "person"
    person_road = Road(f"{src},{person_text}")
    old_water_text = "water"
    old_water_road = f"{src},{person_text},{old_water_text}"
    rain_text = "rain"
    old_rain_road = f"{src},{person_text},{old_water_text},{rain_text}"
    mood_text = "mood"
    mood_road = Road(f"{src},{mood_text}")

    sx = AgentUnit(_desc=src)
    sx.add_tool(walk=src, tool_kid=ToolKid(_desc=person_text))
    sx.add_tool(walk=person_road, tool_kid=ToolKid(_desc=old_water_text))
    sx.add_tool(walk=old_water_road, tool_kid=ToolKid(_desc=rain_text))
    sx.add_tool(walk=src, tool_kid=ToolKid(_desc=mood_text))

    sx.edit_tool_attr(road=mood_road, special_road=old_rain_road)
    mood_tool = sx.get_tool_kid(road=mood_road)
    assert mood_tool._special_road == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_rain_road = f"{src},{person_text},{new_water_text},{rain_text}"
    sx.edit_tool_desc(old_road=old_water_road, new_desc=new_water_text)

    # THEN
    # for tool_x in sx._toolroot._kids.values():
    #     print(f"{tool_x._walk=} {tool_x._desc=}")
    #     tool_x.set_kids_empty_if_null()
    #     for tool_y in tool_x._kids.values():
    #         print(f"{tool_y._walk=} {tool_y._desc=}")
    #         tool_y.set_kids_empty_if_null()
    #         for tool_z in tool_y._kids.values():
    #             print(f"{tool_z._walk=} {tool_z._desc=}")
    assert mood_tool._special_road == new_rain_road


def test_agent_desc_change_ChangesToolRequiredUnitsScenario1():
    # GIVEN
    agent_x = get_agent_with_4_levels_and_2requireds_2acptfacts()
    old_weekday_text = "weekdays"
    old_weekday_road = f"{agent_x._desc},{old_weekday_text}"
    wednesday_text = "Wednesday"
    old_wednesday_road = f"{agent_x._desc},{old_weekday_text},{wednesday_text}"
    work_tool = agent_x.get_tool_kid(f"{agent_x._desc},work")
    usa = f"{agent_x._desc},nation-state,USA"
    nationstate = f"{agent_x._desc},nation-state"
    # work_wk_required = RequiredUnit(base=weekday, sufffacts={wed_sufffact.need: wed_sufffact})
    # nation_required = RequiredUnit(base=nationstate, sufffacts={usa_sufffact.need: usa_sufffact})
    assert len(work_tool._requiredunits) == 2
    assert work_tool._requiredunits.get(old_weekday_road) != None
    wednesday_tool = agent_x.get_tool_kid(old_weekday_road)
    work_weekday_required = work_tool._requiredunits.get(old_weekday_road)
    assert work_weekday_required.sufffacts.get(old_wednesday_road) != None
    assert (
        work_weekday_required.sufffacts.get(old_wednesday_road).need
        == old_wednesday_road
    )
    new_weekday_text = "days of week"
    new_weekday_road = f"{agent_x._desc},{new_weekday_text}"
    new_wednesday_road = f"{agent_x._desc},{new_weekday_text},{wednesday_text}"
    assert work_tool._requiredunits.get(new_weekday_text) is None

    # WHEN
    # for key_x, required_x in work_tool._requiredunits.items():
    #     print(f"Before {key_x=} {required_x.base=}")
    print(f"BEFORE {wednesday_tool._desc=}")
    print(f"BEFORE {wednesday_tool._walk=}")
    agent_x.edit_tool_desc(old_road=old_weekday_road, new_desc=new_weekday_text)
    # for key_x, required_x in work_tool._requiredunits.items():
    #     print(f"AFTER {key_x=} {required_x.base=}")
    print(f"AFTER {wednesday_tool._desc=}")
    print(f"AFTER {wednesday_tool._walk=}")

    # THEN
    assert work_tool._requiredunits.get(new_weekday_road) != None
    assert work_tool._requiredunits.get(old_weekday_road) is None
    work_weekday_required = work_tool._requiredunits.get(new_weekday_road)
    assert work_weekday_required.sufffacts.get(new_wednesday_road) != None
    assert (
        work_weekday_required.sufffacts.get(new_wednesday_road).need
        == new_wednesday_road
    )
    assert len(work_tool._requiredunits) == 2


def test_agent_agent_and_toolroot_desc_edit_CorrectlyChangesBoth():
    # GIVEN
    agent_x = get_agent_with_4_levels_and_2requireds_2acptfacts()
    old_desc = "src"
    assert agent_x._desc == old_desc
    assert agent_x._toolroot._desc == old_desc
    mid_desc1 = "tim"
    agent_x.edit_tool_desc(old_road=old_desc, new_desc=mid_desc1)
    assert agent_x._desc == old_desc
    assert agent_x._toolroot._desc == mid_desc1

    # WHEN
    new_desc2 = "bob"
    agent_x.agent_and_toolroot_desc_edit(new_desc=new_desc2)

    # THEN
    assert agent_x._desc == new_desc2
    assert agent_x._toolroot._desc == new_desc2
