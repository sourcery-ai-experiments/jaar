from src.agenda.required_idea import (
    AcptFactUnit,
    acptfactunit_shop,
    acptfactheir_shop,
    RoadUnit,
    AcptFactCore,
    acptfactunit_shop as c_acptfactunit,
    acptfactunits_get_from_dict,
)
from src.agenda.road import get_default_economy_root_label as root_label, create_road
from pytest import raises as pytest_raises


def test_AcptFactUnit_exists():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)

    # WHEN
    sunday_acptfact = AcptFactUnit(
        base=weekday_road, pick=sunday_road, open=1.9, nigh=2.3
    )

    # THEN
    print(sunday_acptfact)
    assert sunday_acptfact != None
    assert sunday_acptfact.base == weekday_road
    assert sunday_acptfact.pick == sunday_road
    assert sunday_acptfact.open == 1.9
    assert sunday_acptfact.nigh == 2.3


def test_AcptFactUnit_clear_range_works_1():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    weekday_acptfact = acptfactunit_shop(weekday_road, weekday_road, open=1.0, nigh=5.0)
    assert weekday_acptfact.open == 1.0
    assert weekday_acptfact.nigh == 5.0

    # WHEN
    weekday_acptfact.set_range_null()

    # THEN
    assert weekday_acptfact.open is None
    assert weekday_acptfact.nigh is None


def test_AcptFactUnit_clear_range_works_2():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    weekday_acptfact = acptfactunit_shop(weekday_road, weekday_road, open=1.0, nigh=5.0)

    # WHEN
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)
    weekday_acptfact.set_attr(pick=sunday_road)
    # THEN
    assert weekday_acptfact.pick == sunday_road

    # WHEN
    weekday_acptfact.set_attr(open=45)
    # THEN
    assert weekday_acptfact.open == 45

    # WHEN
    weekday_acptfact.set_attr(nigh=65)
    # THEN
    assert weekday_acptfact.nigh == 65


def test_AcptFactUnit_get_dict_CorrectlyReturnsDict():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)
    x_open = 35
    x_nigh = 50
    sunday_acptfact = acptfactunit_shop(
        base=weekday_road, pick=sunday_road, open=x_open, nigh=x_nigh
    )
    print(sunday_acptfact)

    # WHEN
    acptfact_dict = sunday_acptfact.get_dict()

    # THEN
    assert acptfact_dict != None
    static_dict = {
        "base": weekday_road,
        "pick": sunday_road,
        "open": x_open,
        "nigh": x_nigh,
    }
    assert acptfact_dict == static_dict


def test_AcptFactUnit_get_dict_CorrectlyReturnsPartialDict():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    sunday_road = create_road(weekday_road, sunday_text)
    sunday_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    print(sunday_acptfact)

    # WHEN
    acptfact_dict = sunday_acptfact.get_dict()

    # THEN
    assert acptfact_dict != None
    static_dict = {
        "base": weekday_road,
        "pick": sunday_road,
    }
    assert acptfact_dict == static_dict


def test_AcptFactUnit_find_replace_road_works():
    # GIVEN
    weekday_text = "weekday"
    old_weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    old_sunday_road = create_road(old_weekday_road, sunday_text)
    sunday_acptfact = acptfactunit_shop(base=old_weekday_road, pick=old_sunday_road)
    print(sunday_acptfact)
    assert sunday_acptfact.base == old_weekday_road
    assert sunday_acptfact.pick == old_sunday_road

    # WHEN
    old_road = root_label()
    new_road = "fun"
    sunday_acptfact.find_replace_road(old_road=old_road, new_road=new_road)
    new_weekday_road = create_road(new_road, weekday_text)
    new_sunday_road = create_road(new_weekday_road, sunday_text)

    # THEN
    assert sunday_acptfact.base == new_weekday_road
    assert sunday_acptfact.pick == new_sunday_road


def test_AcptFactHeir_IsChangedByAcptFactUnit():
    # GIVEN
    ced_min_text = "ced_minute"
    min_road = create_road(root_label(), ced_min_text)
    ced_acptfactheir = acptfactheir_shop(min_road, min_road, 10.0, 30.0)
    ced_acptfactunit = acptfactunit_shop(min_road, min_road, 20.0, 30.0)
    assert ced_acptfactheir.open == 10

    # WHEN
    ced_acptfactheir.transform(acptfactunit=ced_acptfactunit)

    # THEN
    assert ced_acptfactheir.open == 20

    # GIVEN
    ced_acptfactheir = acptfactheir_shop(min_road, min_road, 10.0, 30.0)
    ced_acptfactunit = acptfactunit_shop(min_road, min_road, 30.0, 30.0)
    assert ced_acptfactheir.open == 10

    # WHEN
    ced_acptfactheir.transform(acptfactunit=ced_acptfactunit)
    assert ced_acptfactheir.open == 30

    # GIVEN
    ced_acptfactheir = acptfactheir_shop(min_road, min_road, 10.0, 30.0)
    ced_acptfactunit = acptfactunit_shop(min_road, min_road, 35.0, 57.0)
    assert ced_acptfactheir.open == 10

    # WHEN
    ced_acptfactheir.transform(acptfactunit=ced_acptfactunit)

    # THEN
    assert ced_acptfactheir.open == 10

    # GIVEN
    ced_acptfactheir = acptfactheir_shop(min_road, min_road, 10.0, 30.0)
    ced_acptfactunit = acptfactunit_shop(min_road, min_road, 5.0, 7.0)
    assert ced_acptfactheir.open == 10

    # WHEN
    ced_acptfactheir.transform(acptfactunit=ced_acptfactunit)

    # THEN
    assert ced_acptfactheir.open == 10


def test_AcptFactHeir_is_range_ReturnsRangeStatus():
    # GIVEN
    ced_min_text = "ced_minute"
    min_road = create_road(root_label(), ced_min_text)

    # WHEN
    x_acptfactheir = acptfactheir_shop(base=min_road, pick=min_road)
    assert x_acptfactheir.is_range() == False

    # THEN
    x_acptfactheir = acptfactheir_shop(min_road, pick=min_road, open=10.0, nigh=30.0)
    assert x_acptfactheir.is_range() == True


def test_acptfactheir_is_range_ReturnsRangeStatus():
    # GIVEN
    ced_min_text = "ced_minute"
    min_road = create_road(root_label(), ced_min_text)

    # WHEN
    x_acptfactheir = acptfactheir_shop(base=min_road, pick=min_road)

    # THEN
    assert x_acptfactheir.is_range() == False

    # WHEN
    x_acptfactheir = acptfactheir_shop(min_road, pick=min_road, open=10.0, nigh=30.0)

    # THEN
    assert x_acptfactheir.is_range() == True


def test_AcptFactCore_get_key_road_works():
    # GIVEN
    ced_min_text = "ced_minute"
    min_road = create_road(root_label(), ced_min_text)
    secs_text = "seconds"
    secs_road = create_road(min_road, secs_text)

    # WHEN
    x_acptfactcore = AcptFactCore(base=min_road, pick=secs_road)

    # THEN
    assert x_acptfactcore.get_key_road() == min_road


def test_acptfactcores_meld_CorrectlyMeldLikeObjs_v1():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    hc_x1 = c_acptfactunit(base=tech_road, pick=bowl_road)
    hc_y1 = c_acptfactunit(base=tech_road, pick=bowl_road)

    # WHEN/THEN
    assert hc_x1 == hc_x1.meld(hc_y1)  # meld is a AcptFactCore method


def test_acptfactcores_meld_CorrectlyMeldLikeObjs_v2():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    hc_x2 = c_acptfactunit(base=tech_road, pick=bowl_road, open=45, nigh=55)
    hc_y2 = c_acptfactunit(base=tech_road, pick=bowl_road, open=45, nigh=55)

    # WHEN/THEN
    assert hc_x2 == hc_x2.meld(hc_y2)


def test_acptfactcores_meld_CorrectlyMeldDifferentObjs_v1():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    dish_text = "dish"
    dish_road = create_road(tech_road, dish_text)
    bowl_af = c_acptfactunit(base=tech_road, pick=bowl_road)
    dish_af = c_acptfactunit(base=tech_road, pick=dish_road)

    # WHEN/THEN
    assert dish_af == bowl_af.meld(dish_af)  # meld is a AcptFactCore method


def test_acptfactcores_meld_CorrectlyMeldDifferentObjs_v2():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    dish_text = "dish"
    dish_road = create_road(tech_road, dish_text)
    bowl_af = c_acptfactunit(base=tech_road, pick=bowl_road, open=45, nigh=55)
    dish_af = c_acptfactunit(base=tech_road, pick=dish_road, open=45, nigh=55)
    # WHEN/THEN
    assert dish_af == bowl_af.meld(dish_af)


def test_acptfactcores_meld_raises_NotSameBaseRoadUnitError():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    hc_x = c_acptfactunit(base=tech_road, pick=tech_road)
    hc_y = c_acptfactunit(base=bowl_road, pick=tech_road)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y, same_required=True)  # meld is a AcptFactCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: base={hc_y.base} is different self.base='{hc_x.base}'"
    )


def test_acptfactcores_meld_raises_NotSameAcptFactRoadUnitError():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    hc_x = c_acptfactunit(base=tech_road, pick=tech_road, open=1, nigh=3)
    hc_y = c_acptfactunit(base=tech_road, pick=bowl_road, open=1, nigh=3)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y, same_required=True)  # meld is a AcptFactCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: pick={hc_y.pick} is different self.pick='{hc_x.pick}'"
    )


def test_acptfactcores_meld_raises_NotSameOpenError():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    hc_x = c_acptfactunit(base=tech_road, pick=bowl_road, open=6, nigh=55)
    hc_y = c_acptfactunit(base=tech_road, pick=bowl_road, open=1, nigh=55)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y, same_required=True)  # meld is a AcptFactCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: base={hc_y.base} open={hc_y.open} is different self.open={hc_x.open}"
    )


def test_acptfactcores_meld_raises_NotSameNighError():
    # GIVEN
    tech_text = "tech"
    tech_road = create_road(root_label(), tech_text)
    bowl_text = "bowl"
    bowl_road = create_road(tech_road, bowl_text)
    hc_x = c_acptfactunit(base=tech_road, pick=bowl_road, open=1, nigh=34)
    hc_y = c_acptfactunit(base=tech_road, pick=bowl_road, open=1, nigh=55)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y, same_required=True)  # meld is a AcptFactCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: base={hc_y.base} nigh={hc_y.nigh} is different self.nigh={hc_x.nigh}"
    )


def test_acptfactunits_get_from_dict_CorrectlyBuildsObj():
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
    acptfacts_dict = acptfactunits_get_from_dict(static_dict)

    # THEN
    assert len(acptfacts_dict) == 1
    weekday_acptfact = acptfacts_dict.get(weekday_road)
    assert weekday_acptfact == acptfactunit_shop(base=weekday_road, pick=sunday_road)


def test_acptfactunits_get_from_dict_CorrectlyBuildsObjFromIncompleteDict():
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
    acptfacts_dict = acptfactunits_get_from_dict(static_dict)

    # THEN
    weekday_acptfact = acptfacts_dict.get(weekday_road)
    assert weekday_acptfact == acptfactunit_shop(base=weekday_road, pick=sunday_road)
