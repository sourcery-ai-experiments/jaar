from src.agenda.fact import factunit_shop
from src.agenda.reason_fact import (
    reasonunit_shop,
    premiseunit_shop,
    RoadUnit,
    beliefunit_shop,
)
from src._road.road import get_default_real_id_roadnode as root_label, create_road


def test_FactUnit_find_replace_road_CorrectlyModifies_parent_road():
    # GIVEN Fact with _parent_road that will be different
    old_casa_text = "casa1"
    old_casa_road = create_road(root_label(), old_casa_text)
    bloomers_text = "bloomers"
    old_bloomers_road = create_road(old_casa_road, bloomers_text)
    roses_text = "roses"
    old_roses_road = create_road(old_bloomers_road, roses_text)
    fact_x = factunit_shop(roses_text, _parent_road=old_bloomers_road)
    assert create_road(fact_x._parent_road) == old_bloomers_road
    assert create_road(fact_x._parent_road, fact_x._label) == old_roses_road

    # WHEN
    new_casa = "casa2"
    new_casa_road = create_road(root_label(), new_casa)
    fact_x.find_replace_road(old_road=old_casa_road, new_road=new_casa_road)

    # THEN
    new_bloomers_road = create_road(new_casa_road, bloomers_text)
    new_roses_road = create_road(new_bloomers_road, roses_text)
    assert create_road(fact_x._parent_road) == new_bloomers_road
    assert create_road(fact_x._parent_road, fact_x._label) == new_roses_road


def test_FactUnit_find_replace_road_CorrectlyModifies_range_source_road_numeric_road():
    # GIVEN Fact with special road and numeric road that will be different
    casa_text = "casa1"
    casa_road = create_road(root_label(), casa_text)
    bloomers_text = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_text)
    roses_text = "roses"
    roses_road = create_road(bloomers_road, roses_text)
    old_water_text = "water"
    old_water_road = create_road(root_label(), old_water_text)
    rain_text = "rain"
    snow_text = "snow"
    old_rain_road = create_road(old_water_road, rain_text)
    old_snow_road = create_road(old_water_road, snow_text)
    farm_text = "farm"
    farm_road = create_road(root_label(), farm_text)
    fertilizer_text = "fertilizer"
    fertilizer_road = create_road(farm_road, fertilizer_text)
    farm_road = create_road(root_label(), farm_text)
    fact_x = factunit_shop(
        _label=roses_text,
        _parent_road=bloomers_road,
        _range_source_road=old_rain_road,
        _numeric_road=old_snow_road,
    )
    assert fact_x._range_source_road == old_rain_road
    assert fact_x._numeric_road == old_snow_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = create_road(root_label(), new_water_text)
    new_rain_road = create_road(new_water_road, rain_text)
    new_snow_road = create_road(new_water_road, snow_text)
    fact_x.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert fact_x._range_source_road == new_rain_road
    assert fact_x._numeric_road == new_snow_road


def test_FactUnit_find_replace_road_CorrectlyModifies_reasonunits():
    # GIVEN Fact with reason that will be different
    casa_text = "casa1"
    casa_road = create_road(root_label(), casa_text)
    bloomers_text = "bloomers"
    bloomers_road = create_road(casa_road, bloomers_text)
    roses_text = "roses"
    roses_road = create_road(bloomers_road, roses_text)
    # reason roads
    old_water_text = "water"
    old_water_road = create_road(root_label(), old_water_text)
    rain_text = "rain"
    old_rain_road = create_road(old_water_road, rain_text)
    # create reasonunit
    premise_x = premiseunit_shop(need=old_rain_road)
    premises_x = {premise_x.need: premise_x}
    reason_x = reasonunit_shop(old_water_road, premises=premises_x)
    reasons_x = {reason_x.base: reason_x}
    fact_x = factunit_shop(roses_text, _reasonunits=reasons_x)
    # check asserts
    assert fact_x._reasonunits.get(old_water_road) != None
    old_water_rain_reason = fact_x._reasonunits[old_water_road]
    assert old_water_rain_reason.base == old_water_road
    assert old_water_rain_reason.premises.get(old_rain_road) != None
    water_rain_l_premise = old_water_rain_reason.premises[old_rain_road]
    assert water_rain_l_premise.need == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = create_road(root_label(), new_water_text)
    assert fact_x._reasonunits.get(new_water_road) is None
    fact_x.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert fact_x._reasonunits.get(old_water_road) is None
    assert fact_x._reasonunits.get(new_water_road) != None
    new_water_rain_reason = fact_x._reasonunits[new_water_road]
    assert new_water_rain_reason.base == new_water_road
    new_rain_road = create_road(new_water_road, rain_text)
    assert new_water_rain_reason.premises.get(old_rain_road) is None
    assert new_water_rain_reason.premises.get(new_rain_road) != None
    new_water_rain_l_premise = new_water_rain_reason.premises[new_rain_road]
    assert new_water_rain_l_premise.need == new_rain_road

    print(f"{len(fact_x._reasonunits)=}")
    reason_obj = fact_x._reasonunits.get(new_water_road)
    assert reason_obj != None

    print(f"{len(reason_obj.premises)=}")
    premise_obj = reason_obj.premises.get(new_rain_road)
    assert premise_obj != None
    assert premise_obj.need == new_rain_road


def test_FactUnit_find_replace_road_CorrectlyModifies_beliefunits():
    # GIVEN Fact with beliefunit that will be different
    roses_text = "roses"
    old_water_text = "water"
    old_water_road = create_road(root_label(), old_water_text)
    rain_text = "rain"
    old_rain_road = create_road(old_water_road, rain_text)

    beliefunit_x = beliefunit_shop(base=old_water_road, pick=old_rain_road)
    beliefunits_x = {beliefunit_x.base: beliefunit_x}
    fact_x = factunit_shop(roses_text, _beliefunits=beliefunits_x)
    assert fact_x._beliefunits[old_water_road] != None
    old_water_rain_beliefunit = fact_x._beliefunits[old_water_road]
    assert old_water_rain_beliefunit.base == old_water_road
    assert old_water_rain_beliefunit.pick == old_rain_road

    # WHEN
    new_water_text = "h2o"
    new_water_road = create_road(root_label(), new_water_text)
    assert fact_x._beliefunits.get(new_water_road) is None
    fact_x.find_replace_road(old_road=old_water_road, new_road=new_water_road)

    # THEN
    assert fact_x._beliefunits.get(old_water_road) is None
    assert fact_x._beliefunits.get(new_water_road) != None
    new_water_rain_beliefunit = fact_x._beliefunits[new_water_road]
    assert new_water_rain_beliefunit.base == new_water_road
    new_rain_road = create_road(new_water_road, rain_text)
    assert new_water_rain_beliefunit.pick == new_rain_road

    print(f"{len(fact_x._beliefunits)=}")
    beliefunit_obj = fact_x._beliefunits.get(new_water_road)
    assert beliefunit_obj != None
    assert beliefunit_obj.base == new_water_road
    assert beliefunit_obj.pick == new_rain_road


def test_FactUnit_get_obj_key_ReturnsCorrectInfo():
    # GIVEN
    red_text = "red"

    # WHEN
    red_fact = factunit_shop(red_text)

    # THEN
    assert red_fact.get_obj_key() == red_text


def test_FactUnit_set_road_delimiter_CorrectlyModifiesReasonRoadUnits():
    # GIVEN
    casa_text = "casa"
    casa_fact = factunit_shop(casa_text)
    casa_fact.set_parent_road("")

    # WHEN
    slash_text = "/"
    casa_fact.set_road_delimiter(slash_text)

    # THEN
    assert casa_fact._road_delimiter == slash_text
