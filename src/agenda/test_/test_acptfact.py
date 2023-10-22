from src.agenda.required_idea import (
    AcptFactUnit,
    acptfactunit_shop,
    acptfactheir_shop,
    Road,
    AcptFactCore,
    acptfactunit_shop as c_acptfactunit,
)
from src.agenda.road import get_default_culture_root_label as root_label
from pytest import raises as pytest_raises


def test_AcptFactUnit_exists():
    sunday_road = f"{root_label()},weekdays,Sunday"
    weekday_road = f"{root_label()},weekdays"
    sunday_cx_acptfact = AcptFactUnit(
        base=weekday_road, pick=sunday_road, open=1.9, nigh=2.3
    )
    print(sunday_cx_acptfact)
    assert sunday_cx_acptfact != None
    assert sunday_cx_acptfact.base == weekday_road
    assert sunday_cx_acptfact.pick == sunday_road
    assert sunday_cx_acptfact.open == 1.9
    assert sunday_cx_acptfact.nigh == 2.3


def test_AcptFactUnit_clear_range_works_1():
    weekday_road = f"{root_label()},weekdays"
    sunday_acptfact = acptfactunit_shop(
        base=weekday_road, pick=weekday_road, open=1.0, nigh=5.0
    )
    assert sunday_acptfact.open == 1.0
    assert sunday_acptfact.nigh == 5.0
    sunday_acptfact.set_range_null()
    assert sunday_acptfact.open is None
    assert sunday_acptfact.nigh is None


def test_AcptFactUnit_clear_range_works_2():
    # Given
    weekday_road = f"{root_label()},weekdays"
    weekday_acptfact = acptfactunit_shop(
        base=weekday_road, pick=weekday_road, open=1.0, nigh=5.0
    )
    # When
    sunday_road = f"{root_label()},weekdays,Sunday"
    weekday_acptfact.set_attr(pick=sunday_road)
    # Then
    assert weekday_acptfact.pick == sunday_road

    # When
    weekday_acptfact.set_attr(open=45)
    # Then
    assert weekday_acptfact.open == 45

    # When
    weekday_acptfact.set_attr(nigh=65)
    # Then
    assert weekday_acptfact.nigh == 65


def test_AcptFactUnit_get_dict_works():
    weekday_road = f"{root_label()},weekdays"
    sunday_road = f"{weekday_road},Sunday"
    sunday_cx_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    print(sunday_cx_acptfact)
    acptfact_dict = sunday_cx_acptfact.get_dict()
    assert acptfact_dict != None
    static_dict = {
        "base": weekday_road,
        "pick": sunday_road,
        "open": None,
        "nigh": None,
    }
    assert acptfact_dict == static_dict


def test_AcptFactUnit_find_replace_road_works():
    # GIVEN
    weekday_text = "weekday"
    old_weekday_road = f"{root_label()},{weekday_text}"
    old_sunday_road = f"{root_label()},{weekday_text},Sunday"
    sunday_acptfact = acptfactunit_shop(base=old_weekday_road, pick=old_sunday_road)
    print(sunday_acptfact)
    assert sunday_acptfact.base == old_weekday_road
    assert sunday_acptfact.pick == old_sunday_road

    # WHEN
    old_road = root_label()
    new_road = "fun"
    sunday_acptfact.find_replace_road(old_road=old_road, new_road=new_road)
    new_weekday_road = f"{new_road},{weekday_text}"
    new_sunday_road = f"{new_weekday_road},Sunday"

    # THEN
    assert sunday_acptfact.base == new_weekday_road
    assert sunday_acptfact.pick == new_sunday_road


def test_AcptFactHeir_IsChangedByAcptFactUnit():
    ced_road = Road(f"{root_label()},ced_minute")

    ced_acptfactheir = acptfactheir_shop(ced_road, ced_road, 10.0, 30.0)
    ced_acptfactunit = acptfactunit_shop(ced_road, ced_road, 20.0, 30.0)
    assert ced_acptfactheir.open == 10
    ced_acptfactheir.transform(acptfactunit=ced_acptfactunit)
    assert ced_acptfactheir.open == 20

    ced_acptfactheir = acptfactheir_shop(ced_road, ced_road, 10.0, 30.0)
    ced_acptfactunit = acptfactunit_shop(ced_road, ced_road, 30.0, 30.0)
    assert ced_acptfactheir.open == 10
    ced_acptfactheir.transform(acptfactunit=ced_acptfactunit)
    assert ced_acptfactheir.open == 30

    ced_acptfactheir = acptfactheir_shop(ced_road, ced_road, 10.0, 30.0)
    ced_acptfactunit = acptfactunit_shop(ced_road, ced_road, 35.0, 57.0)
    assert ced_acptfactheir.open == 10
    ced_acptfactheir.transform(acptfactunit=ced_acptfactunit)
    assert ced_acptfactheir.open == 10

    ced_acptfactheir = acptfactheir_shop(ced_road, ced_road, 10.0, 30.0)
    ced_acptfactunit = acptfactunit_shop(ced_road, ced_road, 5.0, 7.0)
    assert ced_acptfactheir.open == 10
    ced_acptfactheir.transform(acptfactunit=ced_acptfactunit)
    assert ced_acptfactheir.open == 10


def test_AcptFactHeir_is_range_ReturnsRangeStatus():
    ced_road = Road(f"{root_label()},ced_minute")
    x_acptfactheir = acptfactheir_shop(base=ced_road, pick=ced_road)
    assert x_acptfactheir.is_range() == False

    x_acptfactheir = acptfactheir_shop(
        base=ced_road, pick=ced_road, open=10.0, nigh=30.0
    )
    assert x_acptfactheir.is_range() == True


def test_acptfactheir_is_range_ReturnsRangeStatus():
    ced_road = Road(f"{root_label()},ced_minute")
    x_acptfactheir = acptfactheir_shop(base=ced_road, pick=ced_road)
    assert x_acptfactheir.is_range() == False

    x_acptfactheir = acptfactheir_shop(
        base=ced_road, pick=ced_road, open=10.0, nigh=30.0
    )
    assert x_acptfactheir.is_range() == True


def test_AcptFactCore_get_key_road_works():
    ced_road = Road(f"{root_label()},ced_minute")
    secs_road = Road(f"{root_label()},ced_minute, seconds")
    x_acptfactcore = AcptFactCore(base=ced_road, pick=secs_road)
    assert x_acptfactcore.get_key_road() == ced_road


def test_acptfactcores_meld_CorrectlyMeldLikeObjs_v1():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"
    hc_x1 = c_acptfactunit(base=tech_road, pick=bowl_road)
    hc_y1 = c_acptfactunit(base=tech_road, pick=bowl_road)

    # WHEN/THEN
    assert hc_x1 == hc_x1.meld(hc_y1)  # meld is a AcptFactCore method


def test_acptfactcores_meld_CorrectlyMeldLikeObjs_v2():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"
    hc_x2 = c_acptfactunit(base=tech_road, pick=bowl_road, open=45, nigh=55)
    hc_y2 = c_acptfactunit(base=tech_road, pick=bowl_road, open=45, nigh=55)

    # WHEN/THEN
    assert hc_x2 == hc_x2.meld(hc_y2)


def test_acptfactcores_meld_CorrectlyMeldDifferentObjs_v1():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"
    dish_text = "dish"
    dish_road = f"{root_label()},{tech_text},{dish_text}"
    bowl_af = c_acptfactunit(base=tech_road, pick=bowl_road)
    dish_af = c_acptfactunit(base=tech_road, pick=dish_road)

    # WHEN/THEN
    assert dish_af == bowl_af.meld(dish_af)  # meld is a AcptFactCore method


def test_acptfactcores_meld_CorrectlyMeldDifferentObjs_v2():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"
    dish_text = "dish"
    dish_road = f"{root_label()},{tech_text},{dish_text}"
    bowl_af = c_acptfactunit(base=tech_road, pick=bowl_road, open=45, nigh=55)
    dish_af = c_acptfactunit(base=tech_road, pick=dish_road, open=45, nigh=55)
    # WHEN/THEN
    assert dish_af == bowl_af.meld(dish_af)


def test_acptfactcores_meld_raises_NotSameBaseRoadError():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"
    hc_x = c_acptfactunit(base=tech_road, pick=tech_road)
    hc_y = c_acptfactunit(base=bowl_road, pick=tech_road)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y, same_required=True)  # meld is a AcptFactCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: base={hc_y.base} is different self.base='{hc_x.base}'"
    )


def test_acptfactcores_meld_raises_NotSameAcptFactRoadError():
    # GIVEN
    tech_text = "tech"
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"
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
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"
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
    tech_road = f"{root_label()},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{root_label()},{tech_text},{bowl_text}"
    hc_x = c_acptfactunit(base=tech_road, pick=bowl_road, open=1, nigh=34)
    hc_y = c_acptfactunit(base=tech_road, pick=bowl_road, open=1, nigh=55)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y, same_required=True)  # meld is a AcptFactCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: base={hc_y.base} nigh={hc_y.nigh} is different self.nigh={hc_x.nigh}"
    )
