from src.agenda.reason_idea import (
    BeliefUnit,
    beliefunit_shop,
    beliefheir_shop,
    BeliefCore,
    beliefunit_shop as c_beliefunit,
    beliefunits_get_from_dict,
)
from src._road.road import (
    get_default_econ_root_roadnode as root_label,
    create_road,
)
from pytest import raises as pytest_raises


def test_BeliefUnit_exists():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)

    # WHEN
    sunday_belief = BeliefUnit(base=weekday_road, pick=sunday_road, open=1.9, nigh=2.3)

    # THEN
    print(sunday_belief)
    assert sunday_belief != None
    assert sunday_belief.base == weekday_road
    assert sunday_belief.pick == sunday_road
    assert sunday_belief.open == 1.9
    assert sunday_belief.nigh == 2.3


def test_BeliefUnit_clear_range_SetsAttrCorrectly_1():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    weekday_belief = beliefunit_shop(weekday_road, weekday_road, open=1.0, nigh=5.0)
    assert weekday_belief.open == 1.0
    assert weekday_belief.nigh == 5.0

    # WHEN
    weekday_belief.set_range_null()

    # THEN
    assert weekday_belief.open is None
    assert weekday_belief.nigh is None


def test_BeliefUnit_clear_range_SetsAttrCorrectly_2():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    weekday_belief = beliefunit_shop(weekday_road, weekday_road, open=1.0, nigh=5.0)

    # WHEN
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)
    weekday_belief.set_attr(pick=sunday_road)
    # THEN
    assert weekday_belief.pick == sunday_road

    # WHEN
    weekday_belief.set_attr(open=45)
    # THEN
    assert weekday_belief.open == 45

    # WHEN
    weekday_belief.set_attr(nigh=65)
    # THEN
    assert weekday_belief.nigh == 65


def test_BeliefUnit_get_dict_ReturnsDict():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)
    x_open = 35
    x_nigh = 50
    sunday_belief = beliefunit_shop(
        base=weekday_road, pick=sunday_road, open=x_open, nigh=x_nigh
    )
    print(sunday_belief)

    # WHEN
    belief_dict = sunday_belief.get_dict()

    # THEN
    assert belief_dict != None
    static_dict = {
        "base": weekday_road,
        "pick": sunday_road,
        "open": x_open,
        "nigh": x_nigh,
    }
    assert belief_dict == static_dict


def test_BeliefUnit_get_dict_ReturnsPartialDict():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)
    sunday_belief = beliefunit_shop(base=weekday_road, pick=sunday_road)
    print(sunday_belief)

    # WHEN
    belief_dict = sunday_belief.get_dict()

    # THEN
    assert belief_dict != None
    static_dict = {
        "base": weekday_road,
        "pick": sunday_road,
    }
    assert belief_dict == static_dict


def test_BeliefUnit_find_replace_road_SetsAttrCorrectly():
    # GIVEN
    weekday_text = "weekday"
    old_weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    old_sunday_road = create_road(old_weekday_road, sunday_text)
    sunday_belief = beliefunit_shop(base=old_weekday_road, pick=old_sunday_road)
    print(sunday_belief)
    assert sunday_belief.base == old_weekday_road
    assert sunday_belief.pick == old_sunday_road

    # WHEN
    old_road = root_label()
    new_road = "fun"
    sunday_belief.find_replace_road(old_road=old_road, new_road=new_road)
    new_weekday_road = create_road(new_road, weekday_text)
    new_sunday_road = create_road(new_weekday_road, sunday_text)

    # THEN
    assert sunday_belief.base == new_weekday_road
    assert sunday_belief.pick == new_sunday_road


def test_BeliefHeir_IsChangedByBeliefUnit():
    # GIVEN
    ced_min_text = "ced_minute"
    min_road = create_road(root_label(), ced_min_text)
    ced_beliefheir = beliefheir_shop(min_road, min_road, 10.0, 30.0)
    ced_beliefunit = beliefunit_shop(min_road, min_road, 20.0, 30.0)
    assert ced_beliefheir.open == 10

    # WHEN
    ced_beliefheir.transform(beliefunit=ced_beliefunit)

    # THEN
    assert ced_beliefheir.open == 20

    # GIVEN
    ced_beliefheir = beliefheir_shop(min_road, min_road, 10.0, 30.0)
    ced_beliefunit = beliefunit_shop(min_road, min_road, 30.0, 30.0)
    assert ced_beliefheir.open == 10

    # WHEN
    ced_beliefheir.transform(beliefunit=ced_beliefunit)
    assert ced_beliefheir.open == 30

    # GIVEN
    ced_beliefheir = beliefheir_shop(min_road, min_road, 10.0, 30.0)
    ced_beliefunit = beliefunit_shop(min_road, min_road, 35.0, 57.0)
    assert ced_beliefheir.open == 10

    # WHEN
    ced_beliefheir.transform(beliefunit=ced_beliefunit)

    # THEN
    assert ced_beliefheir.open == 10

    # GIVEN
    ced_beliefheir = beliefheir_shop(min_road, min_road, 10.0, 30.0)
    ced_beliefunit = beliefunit_shop(min_road, min_road, 5.0, 7.0)
    assert ced_beliefheir.open == 10

    # WHEN
    ced_beliefheir.transform(beliefunit=ced_beliefunit)

    # THEN
    assert ced_beliefheir.open == 10


def test_BeliefHeir_is_range_ReturnsRangeStatus():
    # GIVEN
    ced_min_text = "ced_minute"
    min_road = create_road(root_label(), ced_min_text)

    # WHEN
    x_beliefheir = beliefheir_shop(base=min_road, pick=min_road)
    assert x_beliefheir.is_range() == False

    # THEN
    x_beliefheir = beliefheir_shop(min_road, pick=min_road, open=10.0, nigh=30.0)
    assert x_beliefheir.is_range() == True


def test_beliefheir_is_range_ReturnsRangeStatus():
    # GIVEN
    ced_min_text = "ced_minute"
    min_road = create_road(root_label(), ced_min_text)

    # WHEN
    x_beliefheir = beliefheir_shop(base=min_road, pick=min_road)

    # THEN
    assert x_beliefheir.is_range() == False

    # WHEN
    x_beliefheir = beliefheir_shop(min_road, pick=min_road, open=10.0, nigh=30.0)

    # THEN
    assert x_beliefheir.is_range() == True


def test_BeliefCore_get_obj_key_SetsAttrCorrectly():
    # GIVEN
    ced_min_text = "ced_minute"
    min_road = create_road(root_label(), ced_min_text)
    secs_text = "secs"
    secs_road = create_road(min_road, secs_text)

    # WHEN
    x_beliefcore = BeliefCore(base=min_road, pick=secs_road)

    # THEN
    assert x_beliefcore.get_obj_key() == min_road


def test_beliefcores_meld_CorrectlyMeldSimilarObjs_v1():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    hc_x1 = c_beliefunit(base=tech_road, pick=bowl_road)
    hc_y1 = c_beliefunit(base=tech_road, pick=bowl_road)

    # WHEN/THEN
    assert hc_x1 == hc_x1.meld(hc_y1)  # meld is a BeliefCore method


def test_beliefcores_meld_CorrectlyMeldSimilarObjs_v2():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    hc_x2 = c_beliefunit(base=tech_road, pick=bowl_road, open=45, nigh=55)
    hc_y2 = c_beliefunit(base=tech_road, pick=bowl_road, open=45, nigh=55)

    # WHEN/THEN
    assert hc_x2 == hc_x2.meld(hc_y2)


def test_beliefcores_meld_CorrectlyMeldDifferentObjs_v1():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    dish_text = "dish"
    dish_road = create_road(tech_road, dish_text)
    bowl_af = c_beliefunit(base=tech_road, pick=bowl_road)
    dish_af = c_beliefunit(base=tech_road, pick=dish_road)

    # WHEN/THEN
    assert dish_af == bowl_af.meld(dish_af)  # meld is a BeliefCore method


def test_beliefcores_meld_CorrectlyMeldDifferentObjs_v2():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    dish_text = "dish"
    dish_road = create_road(tech_road, dish_text)
    bowl_af = c_beliefunit(base=tech_road, pick=bowl_road, open=45, nigh=55)
    dish_af = c_beliefunit(base=tech_road, pick=dish_road, open=45, nigh=55)
    # WHEN/THEN
    assert dish_af == bowl_af.meld(dish_af)


def test_beliefcores_meld_raises_NotSameBaseRoadUnitError():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    hc_x = c_beliefunit(base=tech_road, pick=tech_road)
    hc_y = c_beliefunit(base=bowl_road, pick=tech_road)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y, same_reason=True)  # meld is a BeliefCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: base={hc_y.base} is different self.base='{hc_x.base}'"
    )


def test_beliefcores_meld_raises_NotSameBeliefRoadUnitError():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    hc_x = c_beliefunit(base=tech_road, pick=tech_road, open=1, nigh=3)
    hc_y = c_beliefunit(base=tech_road, pick=bowl_road, open=1, nigh=3)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y, same_reason=True)  # meld is a BeliefCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: pick={hc_y.pick} is different self.pick='{hc_x.pick}'"
    )


def test_beliefcores_meld_raises_NotSameOpenError():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    hc_x = c_beliefunit(base=tech_road, pick=bowl_road, open=6, nigh=55)
    hc_y = c_beliefunit(base=tech_road, pick=bowl_road, open=1, nigh=55)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y, same_reason=True)  # meld is a BeliefCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: base={hc_y.base} open={hc_y.open} is different self.open={hc_x.open}"
    )


def test_beliefcores_meld_raises_NotSameNighError():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    hc_x = c_beliefunit(base=tech_road, pick=bowl_road, open=1, nigh=34)
    hc_y = c_beliefunit(base=tech_road, pick=bowl_road, open=1, nigh=55)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y, same_reason=True)  # meld is a BeliefCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: base={hc_y.base} nigh={hc_y.nigh} is different self.nigh={hc_x.nigh}"
    )


def test_beliefunits_get_from_dict_CorrectlyBuildsObj():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)
    static_dict = {
        weekday_road: {
            "base": weekday_road,
            "pick": sunday_road,
            "open": None,
            "nigh": None,
        }
    }

    # WHEN
    beliefs_dict = beliefunits_get_from_dict(static_dict)

    # THEN
    assert len(beliefs_dict) == 1
    weekday_belief = beliefs_dict.get(weekday_road)
    assert weekday_belief == beliefunit_shop(base=weekday_road, pick=sunday_road)


def test_beliefunits_get_from_dict_CorrectlyBuildsObjFromIncompleteDict():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)
    static_dict = {
        weekday_road: {
            "base": weekday_road,
            "pick": sunday_road,
        }
    }

    # WHEN
    beliefs_dict = beliefunits_get_from_dict(static_dict)

    # THEN
    weekday_belief = beliefs_dict.get(weekday_road)
    assert weekday_belief == beliefunit_shop(base=weekday_road, pick=sunday_road)
