from lib.agent.required import (
    sufffactunit_shop,
    acptfactheir_shop,
    Road,
    sufffactunit_shop,
)
from pytest import raises as pytest_raises


def test_sufffact_attributesExist():
    email = "src,work,check email"
    sufffact_x = sufffactunit_shop(need=email)
    assert sufffact_x.need == email


def test_sufffact_clear_works():
    sufffact_x = sufffactunit_shop(need="src,work,check email")
    assert sufffact_x._status is None
    sufffact_x._status = True
    assert sufffact_x._status
    sufffact_x.clear_status()
    assert sufffact_x._status is None


def test_sufffact_is_range_CorrectlyIdenitiesRangeStatus():
    sufffact_x = sufffactunit_shop(need="src,work", open=1, nigh=3)
    assert sufffact_x._is_range() == True
    sufffact_x = sufffactunit_shop(need="src,work")
    assert sufffact_x._is_range() == False
    sufffact_x = sufffactunit_shop(need="src,work", divisor=5, open=3, nigh=3)
    assert sufffact_x._is_range() == False


def test_sufffact_is_range_CorrectlyIdenitiesSegregateStatus():
    sufffact_x = sufffactunit_shop(need="src,work", open=1, nigh=3)
    assert sufffact_x._is_segregate() == False
    sufffact_x = sufffactunit_shop(need="src,work")
    assert sufffact_x._is_segregate() == False
    sufffact_x = sufffactunit_shop(need="src,work", divisor=5, open=3, nigh=3)
    assert sufffact_x._is_segregate() == True


def test_sufffact_is_in_lineage_CorrectlyIdentifiesLineage():
    texas_road = "prom,Nation-States,USA,Texas"
    oregon_road = "prom,Nation-States,USA,Oregon"
    usa_road = "prom,Nation-States,USA"
    texas_acptfact = acptfactheir_shop(base=usa_road, pick=texas_road)
    texas_sufffact_x = sufffactunit_shop(need=texas_road)
    usa_sufffact_x = sufffactunit_shop(need=usa_road)
    oregon_sufffact_x = sufffactunit_shop(need=oregon_road)
    assert texas_sufffact_x.is_in_lineage(acptfact_pick=texas_acptfact.pick)
    assert usa_sufffact_x.is_in_lineage(acptfact_pick=texas_acptfact.pick)
    assert oregon_sufffact_x.is_in_lineage(acptfact_pick=texas_acptfact.pick) == False

    sea_road = "earth,sea"
    seaside_road = "earth,seaside,beach"
    sea_acptfact = acptfactheir_shop(base=sea_road, pick=sea_road)
    seaside_acptfact = acptfactheir_shop(base=seaside_road, pick=seaside_road)
    sea_sufffact_x = sufffactunit_shop(need=sea_road)
    assert sea_sufffact_x.is_in_lineage(acptfact_pick=sea_acptfact.pick)
    assert sea_sufffact_x.is_in_lineage(acptfact_pick=seaside_acptfact.pick) == False


def test_sufffact_get_range_segregate_status_ReturnsCorrectStatusBoolForRangeSuffFact():
    road_x = Road("casa,ced_year")
    sufffact_x = sufffactunit_shop(need=road_x, open=3, nigh=13)
    x_acptfact = acptfactheir_shop(base=road_x, open=5, nigh=11, pick=road_x)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == True
    x_acptfact = acptfactheir_shop(base=road_x, open=1, nigh=11, pick=road_x)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == True
    x_acptfact = acptfactheir_shop(base=road_x, open=8, nigh=17, pick=road_x)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == True
    x_acptfact = acptfactheir_shop(base=road_x, open=0, nigh=2, pick=road_x)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == False
    x_acptfact = acptfactheir_shop(base=road_x, open=15, nigh=19, pick=road_x)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == False
    x_acptfact = acptfactheir_shop(base=road_x, open=1, nigh=19, pick=road_x)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == True
    # boundary tests
    x_acptfact = acptfactheir_shop(base=road_x, open=13, nigh=19, pick=road_x)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == False
    x_acptfact = acptfactheir_shop(base=road_x, open=0, nigh=3, pick=road_x)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == True


def test_sufffact_get_range_segregate_status_ReturnsCorrectStatusBoolForSegregateSuffFact():
    road_x = Road("casa,ced_year")
    sufffact_x = sufffactunit_shop(need=road_x, divisor=5, open=0, nigh=0)
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x, open=5, nigh=5)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == True
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x, open=6, nigh=6)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == False
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x, open=4, nigh=6)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == True
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x, open=3, nigh=4)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == False

    sufffact_x = sufffactunit_shop(need=road_x, divisor=5, open=0, nigh=2)
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x, open=2, nigh=2)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == False
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x, open=102, nigh=102)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == False
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x, open=1, nigh=4)
    assert sufffact_x._get_range_segregate_status(acptfactheir=x_acptfact) == True


def test_sufffact_is_range_or_segregate_ReturnsCorrectBool():
    road_x = Road("casa,weekday")
    sufffact_x = sufffactunit_shop(need=road_x)
    assert sufffact_x._is_range_or_segregate() == False
    sufffact_x = sufffactunit_shop(need=road_x, open=5, nigh=13)
    assert sufffact_x._is_range_or_segregate() == True
    sufffact_x = sufffactunit_shop(need=road_x, divisor=17, open=7, nigh=7)
    assert sufffact_x._is_range_or_segregate() == True


def test_get_sufffact_status_returnsCorrectsufffactstatus():
    # assumes acptfact is already in lineage is already
    road_x = Road("casa,weekday")
    sufffact_x = sufffactunit_shop(need=road_x)
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x)
    assert sufffact_x._get_active_status(acptfactheir=x_acptfact) == True
    # if acptfact has range but sufffact does not reqquire range, acptfact's range does not matter
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x, open=0, nigh=2)
    assert sufffact_x._get_active_status(acptfactheir=x_acptfact) == True


def test_get_sufffact_status_returnsCorrectRangedsufffactstatus():
    # assumes acptfact is already in lineage is already
    road_x = Road("casa,weekday")
    sufffact_x = sufffactunit_shop(need=road_x, open=3, nigh=7)
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x)
    assert sufffact_x._get_active_status(acptfactheir=x_acptfact) == False
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x, open=0, nigh=2)
    assert sufffact_x._get_active_status(acptfactheir=x_acptfact) == False


def test_sufffact_set_status_CorrectlySetsStatusWhenAcptFactIsNull():
    sufffact_2 = sufffactunit_shop(need="casa,weekday,wednesday,wed_afternoon")
    agent_acptfact_2 = None
    assert sufffact_2._status is None
    sufffact_2.set_status(acptfactheir=agent_acptfact_2)
    assert sufffact_2._status == False


def test_sufffact_set_status_CorrectlySetsStatusOfSimple():
    sufffact_x = sufffactunit_shop(need="casa,weekday,wednesday")
    agent_acptfact = acptfactheir_shop(
        base="casa,weekday", pick="casa,weekday,wednesday"
    )
    assert sufffact_x._status is None
    sufffact_x.set_status(acptfactheir=agent_acptfact)
    assert sufffact_x._status == True


def test_sufffact_set_status_CorrectlySetsStatus_2():
    sufffact_2 = sufffactunit_shop(need="casa,weekday,wednesday,wed_afternoon")
    agent_acptfact_2 = acptfactheir_shop(
        base="casa,weekday", pick="casa,weekday,wednesday"
    )
    assert sufffact_2._status is None
    sufffact_2.set_status(acptfactheir=agent_acptfact_2)
    assert sufffact_2._status == True


def test_sufffact_set_status_CorrectlySetsStatus_3():
    sufffact_3 = sufffactunit_shop(need="casa,weekday,wednesday")
    agent_acptfact_3 = acptfactheir_shop(
        base="casa,weekday", pick="casa,weekday,wednesday,noon"
    )
    assert sufffact_3._status is None
    sufffact_3.set_status(acptfactheir=agent_acptfact_3)
    assert sufffact_3._status == True


def test_sufffact_set_status_CorrectlySetsStatus_4():
    sufffact_4 = sufffactunit_shop(need="casa,weekday,wednesday")
    agent_acptfact_4 = acptfactheir_shop(
        base="casa,weekday", pick="casa,weekday,thursday"
    )
    assert sufffact_4._status is None
    assert sufffact_4.is_in_lineage(acptfact_pick=agent_acptfact_4.pick) == False
    assert agent_acptfact_4.open is None
    assert agent_acptfact_4.nigh is None
    sufffact_4.set_status(acptfactheir=agent_acptfact_4)
    assert sufffact_4._status == False


def test_sufffact_set_status_CorrectlySetsStatus_5():
    sufffact_5 = sufffactunit_shop(need="casa,weekday,wednesday,sunny")
    agent_acptfact_5 = acptfactheir_shop(base="casa,weekday", pick="casa,weekday,rainy")
    assert sufffact_5._status is None
    sufffact_5.set_status(acptfactheir=agent_acptfact_5)
    assert sufffact_5._status == False


def test_sufffact_set_status_CorrectlySetsTimeRangeStatusTrue():
    sufffact_x = sufffactunit_shop(need="casa,timetech,24hr", open=7, nigh=7)
    agent_acptfact = acptfactheir_shop(
        base="casa,timetech,24hr", pick="casa,timetech,24hr", open=0, nigh=8
    )
    assert sufffact_x._status is None
    sufffact_x.set_status(acptfactheir=agent_acptfact)
    assert sufffact_x._status == True


def test_sufffact_set_task_CorrectlySetsTaskBool_01():
    road_x = "casa,24hr"
    sufffact_x = sufffactunit_shop(need=road_x)
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x)
    sufffact_x._status = False
    assert sufffact_x._get_task_status(acptfactheir=x_acptfact) == False


def test_sufffact_set_task_CorrectlySetsTaskBoolRangeTrue():
    road_x = "casa,24hr"
    sufffact_x = sufffactunit_shop(need=road_x, open=5, nigh=31)
    x_acptfact = acptfactheir_shop(base=road_x, open=7, nigh=41, pick=road_x)
    sufffact_x._status = True
    assert sufffact_x._get_task_status(acptfactheir=x_acptfact) == True


def test_sufffact_set_task_CorrectlySetsTaskBoolRangeFalse():
    road_x = "casa,24hr"
    sufffact_x = sufffactunit_shop(need=road_x, open=5, nigh=31)
    x_acptfact = acptfactheir_shop(base=road_x, open=7, nigh=21, pick=road_x)
    sufffact_x._status = True
    assert sufffact_x._get_task_status(acptfactheir=x_acptfact) == False


def test_sufffact_set_task_CorrectlySetsTaskBoolSegregateFalse_01():
    road_x = "casa,24hr"
    sufffact_x = sufffactunit_shop(need=road_x, divisor=5, open=0, nigh=0)
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x, open=3, nigh=5)
    sufffact_x._status = True
    assert sufffact_x._get_task_status(acptfactheir=x_acptfact) == False


def test_sufffact_set_task_CorrectlySetsTaskBoolSegregateFalse_03():
    road_x = "casa,24hr"
    sufffact_x = sufffactunit_shop(need=road_x, divisor=5, open=0, nigh=0)
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x, open=5, nigh=7)
    sufffact_x._status = False
    assert sufffact_x._get_task_status(acptfactheir=x_acptfact) == False


def test_sufffact_set_task_CorrectlySetsTaskBoolSegregateTrue_01():
    road_x = "casa,24hr"
    sufffact_x = sufffactunit_shop(need=road_x, divisor=5, open=0, nigh=0)
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x, open=5, nigh=7)
    sufffact_x._status = True
    assert sufffact_x._get_task_status(acptfactheir=x_acptfact) == True


def test_sufffact_set_task_CorrectlySetsTaskBoolSegregateTrue_02():
    road_x = "casa,24hr"
    sufffact_x = sufffactunit_shop(need=road_x, divisor=5, open=0, nigh=0)
    x_acptfact = acptfactheir_shop(base=road_x, pick=road_x, open=5, nigh=5)
    sufffact_x._status = True
    assert sufffact_x._get_task_status(acptfactheir=x_acptfact)


def test_sufffact_set_task_NotNull():
    road_x = "prom,weekdays,Wednesday"
    sufffact_x = sufffactunit_shop(need=road_x)
    sufffact_x._status = True

    x_base_road = "prom,weekdays"
    acptfactheir = acptfactheir_shop(base=x_base_road, pick=road_x)

    assert sufffact_x._get_task_status(acptfactheir=acptfactheir) == False


def test_sufffact_set_status_CorrectlySetsTimeRangeTaskTrue_v1():
    sufffact_x = sufffactunit_shop(need="casa,24hr", open=2, nigh=7)
    agent_acptfact = acptfactheir_shop(
        base="casa,24hr", pick="casa,24hr", open=0, nigh=5
    )
    assert sufffact_x._status is None
    sufffact_x.set_status(acptfactheir=agent_acptfact)
    assert sufffact_x._status == True
    assert sufffact_x._task == False


def test_sufffact_set_status_CorrectlySetsTimeRangeTaskTrue_v2():
    # sourcery skip: extract-duplicate-method
    sufffact_x = sufffactunit_shop(need="casa,24hr", open=2, nigh=7)
    agent_acptfact = acptfactheir_shop(
        base="casa,24hr", pick="casa,24hr", open=0, nigh=8
    )
    assert sufffact_x._status is None
    sufffact_x.set_status(acptfactheir=agent_acptfact)
    assert sufffact_x._status == True
    assert sufffact_x._task == True

    agent_acptfact = acptfactheir_shop(
        base="casa,24hr", pick="casa,24hr", open=3, nigh=5
    )
    sufffact_x.set_status(acptfactheir=agent_acptfact)
    assert sufffact_x._status
    assert sufffact_x._task == False

    agent_acptfact = acptfactheir_shop(
        base="casa,24hr", pick="casa,24hr", open=8, nigh=8
    )
    sufffact_x.set_status(acptfactheir=agent_acptfact)
    assert sufffact_x._status == False
    assert sufffact_x._task == False


def test_sufffact_set_status_CorrectlySetsTimeRangeStatusFalse():
    sufffact_x = sufffactunit_shop(need="casa,timetech,24hr", open=7, nigh=7)
    agent_acptfact = acptfactheir_shop(
        base="casa,timetech,24hr", pick="casa,timetech,24hr", open=8, nigh=10
    )
    assert sufffact_x._status is None
    sufffact_x.set_status(acptfactheir=agent_acptfact)
    assert sufffact_x._status == False


def test_sufffact_set_status_CorrectlySetCEDWeekStatusFalse():
    sufffact_x = sufffactunit_shop(
        need="casa,timetech,ced_week", divisor=6, open=1, nigh=1
    )
    agent_acptfact = acptfactheir_shop(
        base="casa,timetech,ced_week", pick="casa,timetech,ced_week", open=6, nigh=6
    )
    assert sufffact_x._status is None
    sufffact_x.set_status(acptfactheir=agent_acptfact)
    assert sufffact_x._status == False


def test_sufffact_set_status_CorrectlySetCEDWeekStatusTrue():
    sufffact_x = sufffactunit_shop(
        need="casa,timetech,ced_week", divisor=6, open=1, nigh=1
    )
    agent_acptfact = acptfactheir_shop(
        base="casa,timetech,ced_week", pick="casa,timetech,ced_week", open=7, nigh=7
    )
    assert sufffact_x._status is None
    sufffact_x.set_status(acptfactheir=agent_acptfact)
    assert sufffact_x._status == True


def test_sufffact_get_dict_ReturnsCorrectDictWithDvisiorAndOpenNigh():
    sufffact_x = sufffactunit_shop(
        need="casa,timetech,ced_week", divisor=6, open=1, nigh=1
    )
    sufffact_dict = sufffact_x.get_dict()
    assert sufffact_dict != None
    static_dict = {
        "need": "casa,timetech,ced_week",
        "open": 1,
        "nigh": 1,
        "divisor": 6,
    }
    assert sufffact_dict == static_dict


def test_sufffact_get_dict_ReturnsCorrectDictWithOpenAndNigh():
    sufffact_x = sufffactunit_shop(need="casa,timetech,ced_week", open=1, nigh=4)
    sufffact_dict = sufffact_x.get_dict()
    assert sufffact_dict != None
    static_dict = {
        "need": "casa,timetech,ced_week",
        "open": 1,
        "nigh": 4,
        "divisor": None,
    }
    assert sufffact_dict == static_dict


def test_sufffact_get_dict_ReturnsCorrectDictWithOnlyRoad():
    sufffact_x = sufffactunit_shop(need="casa,timetech,ced_week")
    sufffact_dict = sufffact_x.get_dict()
    assert sufffact_dict != None
    static_dict = {
        "need": "casa,timetech,ced_week",
        "open": None,
        "nigh": None,
        "divisor": None,
    }
    assert sufffact_dict == static_dict


def test_sufffact_get_key_road():
    sufffact_x = sufffactunit_shop(need="casa,timetech,ced_week")
    assert sufffact_x.get_key_road() == Road("casa,timetech,ced_week")


def test_sufffact_find_replace_road_works():
    # GIVEN
    src = "src"
    weekday_text = "weekday"
    old_sunday_road = f"{src},{weekday_text},Sunday"
    sunday_sufffact_x = sufffactunit_shop(need=old_sunday_road)
    print(sunday_sufffact_x)
    assert sunday_sufffact_x.need == old_sunday_road

    # WHEN
    old_road = f"{src}"
    new_road = "fun"
    sunday_sufffact_x.find_replace_road(old_road=old_road, new_road=new_road)
    new_sunday_road = f"{new_road},{weekday_text},Sunday"

    # THEN
    assert sunday_sufffact_x.need == new_sunday_road


def test_sufffact_meld_works():
    # GIVEN
    sufffact_x1 = sufffactunit_shop(need="casa,timetech,ced_week")
    sufffact_y1 = sufffactunit_shop(need="casa,timetech,ced_week")

    # WHEN/THEN
    assert sufffact_x1 == sufffact_x1.meld(sufffact_y1)

    # GIVEN
    sufffact_x2 = sufffactunit_shop(need="casa,timetech,ced_week", open=45, nigh=55)
    sufffact_y2 = sufffactunit_shop(need="casa,timetech,ced_week", open=45, nigh=55)
    # WHEN/THEN
    assert sufffact_x2 == sufffact_x2.meld(sufffact_y2)


def test_sufffact_meld_raises_NotSameRoadError():
    # GIVEN
    sufffact_x = sufffactunit_shop(need="casa,timetech,ced_week")
    sufffact_y = sufffactunit_shop(need="casa,timetech")

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        sufffact_x == sufffact_x.meld(sufffact_y)
    assert (
        str(excinfo.value)
        == f"Meld fail: need={sufffact_y.need} is different self.need='{sufffact_x.need}'"
    )


def test_sufffact_meld_raises_NotSameOpenError():
    # GIVEN
    sufffact_x = sufffactunit_shop(need="casa,timetech", open=1, nigh=3, divisor=8)
    sufffact_y = sufffactunit_shop(need="casa,timetech", open=0, nigh=3, divisor=8)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        sufffact_x == sufffact_x.meld(sufffact_y)
    assert (
        str(excinfo.value)
        == f"Meld fail: need={sufffact_y.need} open={sufffact_y.open} is different self.open={sufffact_x.open}"
    )


def test_sufffact_meld_raises_NotSameNighError():
    # GIVEN
    sufffact_x = sufffactunit_shop(need="casa,timetech", open=1, nigh=5, divisor=8)
    sufffact_y = sufffactunit_shop(need="casa,timetech", open=1, nigh=3, divisor=8)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        sufffact_x == sufffact_x.meld(sufffact_y)
    assert (
        str(excinfo.value)
        == f"Meld fail: need={sufffact_y.need} nigh={sufffact_y.nigh} is different self.nigh={sufffact_x.nigh}"
    )


def test_sufffact_meld_raises_NotSameDivisorError():
    # GIVEN
    sufffact_x = sufffactunit_shop(need="casa,timetech", open=1, nigh=5, divisor=8)
    sufffact_y = sufffactunit_shop(need="casa,timetech", open=1, nigh=5, divisor=10)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        sufffact_x == sufffact_x.meld(sufffact_y)
    assert (
        str(excinfo.value)
        == f"Meld fail: need={sufffact_y.need} divisor={sufffact_y.divisor} is different self.divisor={sufffact_x.divisor}"
    )
