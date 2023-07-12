from lib.agent.required import (
    AcptFactUnit,
    acptfactunit_shop,
    acptfactheir_shop,
    Road,
    AcptFactCore,
    acptfactunit_shop as c_acptfactunit,
)
from pytest import raises as pytest_raises


def test_AcptFactUnit_exists():
    sunday_road = "src,weekdays,Sunday"
    weekday_road = "src,weekdays"
    sunday_lw_acptfact = AcptFactUnit(
        base=weekday_road, pick=sunday_road, open=1.9, nigh=2.3
    )
    print(sunday_lw_acptfact)
    assert sunday_lw_acptfact != None
    assert sunday_lw_acptfact.base == weekday_road
    assert sunday_lw_acptfact.pick == sunday_road
    assert sunday_lw_acptfact.open == 1.9
    assert sunday_lw_acptfact.nigh == 2.3


def test_AcptFactUnit_clear_range_works_1():
    weekday_road = "src,weekdays"
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
    weekday_road = "src,weekdays"
    weekday_acptfact = acptfactunit_shop(
        base=weekday_road, pick=weekday_road, open=1.0, nigh=5.0
    )
    # When
    sunday_road = "src,weekdays,Sunday"
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
    sunday_road = "src,weekdays,Sunday"
    weekday_road = "src,weekdays"
    sunday_lw_acptfact = acptfactunit_shop(base=weekday_road, pick=sunday_road)
    print(sunday_lw_acptfact)
    acptfact_dict = sunday_lw_acptfact.get_dict()
    assert acptfact_dict != None
    static_dict = {
        "base": "src,weekdays",
        "pick": "src,weekdays,Sunday",
        "open": None,
        "nigh": None,
    }
    assert acptfact_dict == static_dict


def test_AcptFactUnit_find_replace_road_works():
    # GIVEN
    src = "src"
    weekday_text = "weekday"
    old_weekday_road = f"{src},{weekday_text}"
    old_sunday_road = f"{src},{weekday_text},Sunday"
    sunday_acptfact = acptfactunit_shop(base=old_weekday_road, pick=old_sunday_road)
    print(sunday_acptfact)
    assert sunday_acptfact.base == old_weekday_road
    assert sunday_acptfact.pick == old_sunday_road

    # WHEN
    old_road = f"{src}"
    new_road = "fun"
    sunday_acptfact.find_replace_road(old_road=old_road, new_road=new_road)
    new_weekday_road = f"{new_road},{weekday_text}"
    new_sunday_road = f"{new_road},{weekday_text},Sunday"

    # THEN
    assert sunday_acptfact.base == new_weekday_road
    assert sunday_acptfact.pick == new_sunday_road


def test_AcptFactHeir_IsChangedByAcptFactUnit():
    ced_road = Road("prom,ced_minute")

    ced_acptfactheir = acptfactheir_shop(
        base=ced_road, pick=ced_road, open=10.0, nigh=30.0
    )
    ced_acptfactunit = acptfactunit_shop(
        base=ced_road, pick=ced_road, open=20.0, nigh=30.0
    )
    assert ced_acptfactheir.open == 10
    ced_acptfactheir.transform(acptfactunit=ced_acptfactunit)
    assert ced_acptfactheir.open == 20

    ced_acptfactheir = acptfactheir_shop(
        base=ced_road, pick=ced_road, open=10.0, nigh=30.0
    )
    ced_acptfactunit = acptfactunit_shop(
        base=ced_road, pick=ced_road, open=30.0, nigh=30.0
    )
    assert ced_acptfactheir.open == 10
    ced_acptfactheir.transform(acptfactunit=ced_acptfactunit)
    assert ced_acptfactheir.open == 30

    ced_acptfactheir = acptfactheir_shop(
        base=ced_road, pick=ced_road, open=10.0, nigh=30.0
    )
    ced_acptfactunit = acptfactunit_shop(
        base=ced_road, pick=ced_road, open=35.0, nigh=57.0
    )
    assert ced_acptfactheir.open == 10
    ced_acptfactheir.transform(acptfactunit=ced_acptfactunit)
    assert ced_acptfactheir.open == 10

    ced_acptfactheir = acptfactheir_shop(
        base=ced_road, pick=ced_road, open=10.0, nigh=30.0
    )
    ced_acptfactunit = acptfactunit_shop(
        base=ced_road, pick=ced_road, open=5.0, nigh=7.0
    )
    assert ced_acptfactheir.open == 10
    ced_acptfactheir.transform(acptfactunit=ced_acptfactunit)
    assert ced_acptfactheir.open == 10


def test_AcptFactHeir_is_range_ReturnsRangeStatus():
    ced_road = Road("prom,ced_minute")
    x_acptfactheir = acptfactheir_shop(base=ced_road, pick=ced_road)
    assert x_acptfactheir.is_range() == False

    x_acptfactheir = acptfactheir_shop(
        base=ced_road, pick=ced_road, open=10.0, nigh=30.0
    )
    assert x_acptfactheir.is_range() == True


def test_acptfactheir_is_range_ReturnsRangeStatus():
    ced_road = Road("prom,ced_minute")
    x_acptfactheir = acptfactheir_shop(base=ced_road, pick=ced_road)
    assert x_acptfactheir.is_range() == False

    x_acptfactheir = acptfactheir_shop(
        base=ced_road, pick=ced_road, open=10.0, nigh=30.0
    )
    assert x_acptfactheir.is_range() == True


def test_AcptFactCore_get_key_road_works():
    ced_road = Road("prom,ced_minute")
    secs_road = Road("prom,ced_minute, seconds")
    x_acptfactcore = AcptFactCore(base=ced_road, pick=secs_road)
    assert x_acptfactcore.get_key_road() == ced_road


def test_acptfactcores_meld_works():
    # GIVEN
    src = "casa"
    tech_text = "tech"
    tech_road = f"{src},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{src},{tech_text},{bowl_text}"
    hc_x1 = c_acptfactunit(base=tech_road, pick=bowl_road)
    hc_y1 = c_acptfactunit(base=tech_road, pick=bowl_road)

    # WHEN/THEN
    assert hc_x1 == hc_x1.meld(hc_y1)  # meld is a AcptFactCore method

    # GIVEN
    hc_x2 = c_acptfactunit(base=tech_road, pick=bowl_road, open=45, nigh=55)
    hc_y2 = c_acptfactunit(base=tech_road, pick=bowl_road, open=45, nigh=55)
    # WHEN/THEN
    assert hc_x2 == hc_x2.meld(hc_y2)


def test_acptfactcores_meld_raises_NotSameBaseRoadError():
    # GIVEN
    src = "casa"
    tech_text = "tech"
    tech_road = f"{src},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{src},{tech_text},{bowl_text}"
    hc_x = c_acptfactunit(base=tech_road, pick=tech_road)
    hc_y = c_acptfactunit(base=bowl_road, pick=tech_road)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y)  # meld is a AcptFactCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: base={hc_y.base} is different self.base='{hc_x.base}'"
    )


def test_acptfactcores_meld_raises_NotSameAcptFactRoadError():
    # GIVEN
    src = "casa"
    tech_text = "tech"
    tech_road = f"{src},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{src},{tech_text},{bowl_text}"
    hc_x = c_acptfactunit(base=tech_road, pick=tech_road, open=1, nigh=3)
    hc_y = c_acptfactunit(base=tech_road, pick=bowl_road, open=1, nigh=3)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y)  # meld is a AcptFactCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: pick={hc_y.pick} is different self.pick='{hc_x.pick}'"
    )


def test_acptfactcores_meld_raises_NotSameOpenError():
    # GIVEN
    src = "casa"
    tech_text = "tech"
    tech_road = f"{src},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{src},{tech_text},{bowl_text}"
    hc_x = c_acptfactunit(base=tech_road, pick=bowl_road, open=6, nigh=55)
    hc_y = c_acptfactunit(base=tech_road, pick=bowl_road, open=1, nigh=55)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y)  # meld is a AcptFactCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: base={hc_y.base} open={hc_y.open} is different self.open={hc_x.open}"
    )


def test_acptfactcores_meld_raises_NotSameNighError():
    # GIVEN
    src = "casa"
    tech_text = "tech"
    tech_road = f"{src},{tech_text}"
    bowl_text = "bowl"
    bowl_road = f"{src},{tech_text},{bowl_text}"
    hc_x = c_acptfactunit(base=tech_road, pick=bowl_road, open=1, nigh=34)
    hc_y = c_acptfactunit(base=tech_road, pick=bowl_road, open=1, nigh=55)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        hc_x == hc_x.meld(hc_y)  # meld is a AcptFactCore method
    assert (
        str(excinfo.value)
        == f"Meld fail: base={hc_y.base} nigh={hc_y.nigh} is different self.nigh={hc_x.nigh}"
    )
