from src.agenda.required_idea import (
    sufffactunit_shop,
    acptfactheir_shop,
    sufffactunit_shop,
    sufffacts_get_from_dict,
)
from src.agenda.road import get_default_economy_root_label as root_label, create_road
from pytest import raises as pytest_raises


def test_sufffact_attributesExist():
    # GIVEN
    work_text = "work"
    work_road = create_road(root_label(), work_text)
    email_text = "check email"
    email_road = create_road(work_road, email_text)

    # WHEN
    email_sufffact = sufffactunit_shop(need=email_road)

    # THEN
    assert email_sufffact.need == email_road


def test_sufffact_clear_works():
    # WHEN
    work_text = "work"
    work_road = create_road(root_label(), work_text)
    work_sufffact = sufffactunit_shop(need=work_road)
    # THEN
    assert work_sufffact._status is None

    # GIVEN
    work_sufffact._status = True
    assert work_sufffact._status

    # WHEN
    work_sufffact.clear_status()

    # THEN
    assert work_sufffact._status is None


def test_sufffact_is_range_CorrectlyIdenitiesRangeStatus():
    # GIVEN
    work_text = "work"
    work_road = create_road(root_label(), work_text)

    # WHEN
    work_sufffact = sufffactunit_shop(need=work_road, open=1, nigh=3)
    # THEN
    assert work_sufffact._is_range() == True

    # WHEN
    work_sufffact = sufffactunit_shop(need=work_road)
    # THEN
    assert work_sufffact._is_range() == False

    # WHEN
    work_sufffact = sufffactunit_shop(need=work_road, divisor=5, open=3, nigh=3)
    # THEN
    assert work_sufffact._is_range() == False


def test_sufffact_is_range_CorrectlyIdenitiesSegregateStatus():
    # GIVEN
    work_text = "work"
    work_road = create_road(root_label(), work_text)

    # WHEN
    work_sufffact = sufffactunit_shop(need=work_road, open=1, nigh=3)
    # THEN
    assert work_sufffact._is_segregate() == False

    # WHEN
    work_sufffact = sufffactunit_shop(need=work_road)
    # THEN
    assert work_sufffact._is_segregate() == False

    # WHEN
    work_sufffact = sufffactunit_shop(need=work_road, divisor=5, open=3, nigh=3)
    # THEN
    assert work_sufffact._is_segregate() == True


def test_sufffact_is_in_lineage_CorrectlyIdentifiesLineage():
    # GIVEN
    nation_road = create_road(root_label(), "Nation-States")
    usa_road = create_road(nation_road, "USA")
    texas_road = create_road(usa_road, "Texas")
    idaho_road = create_road(usa_road, "Idaho")

    # WHEN
    texas_acptfact = acptfactheir_shop(base=usa_road, pick=texas_road)

    # THEN
    texas_sufffact = sufffactunit_shop(need=texas_road)
    assert texas_sufffact.is_in_lineage(acptfact_pick=texas_acptfact.pick)

    idaho_sufffact = sufffactunit_shop(need=idaho_road)
    assert idaho_sufffact.is_in_lineage(acptfact_pick=texas_acptfact.pick) == False

    usa_sufffact = sufffactunit_shop(need=usa_road)
    assert usa_sufffact.is_in_lineage(acptfact_pick=texas_acptfact.pick)

    # GIVEN
    sea_road = create_road("earth", "sea")  # "earth,sea"
    seaside_road = create_road("earth", "seaside")  # "earth,seaside,beach"
    seaside_beach_road = create_road(seaside_road, "beach")  # "earth,seaside,beach"

    # WHEN
    sea_sufffact = sufffactunit_shop(need=sea_road)

    # THEN
    sea_acptfact = acptfactheir_shop(base=sea_road, pick=sea_road)
    assert sea_sufffact.is_in_lineage(acptfact_pick=sea_acptfact.pick)
    seaside_acptfact = acptfactheir_shop(seaside_beach_road, seaside_beach_road)
    assert sea_sufffact.is_in_lineage(acptfact_pick=seaside_acptfact.pick) == False


def test_sufffact_is_in_lineage_CorrectlyIdentifiesLineageWithNonDefaultDelimiter():
    # GIVEN
    slash_text = "/"
    nation_road = create_road(root_label(), "Nation-States", delimiter=slash_text)
    usa_road = create_road(nation_road, "USA", delimiter=slash_text)
    texas_road = create_road(usa_road, "Texas", delimiter=slash_text)
    idaho_road = create_road(usa_road, "Idaho", delimiter=slash_text)

    # WHEN
    texas_acptfact = acptfactheir_shop(base=usa_road, pick=texas_road)

    # THEN
    texas_sufffact = sufffactunit_shop(need=texas_road, delimiter=slash_text)
    assert texas_sufffact.is_in_lineage(acptfact_pick=texas_acptfact.pick)

    idaho_sufffact = sufffactunit_shop(need=idaho_road, delimiter=slash_text)
    assert idaho_sufffact.is_in_lineage(acptfact_pick=texas_acptfact.pick) == False

    usa_sufffact = sufffactunit_shop(need=usa_road, delimiter=slash_text)
    print(f"  {usa_sufffact.need=}")
    print(f"{texas_acptfact.pick=}")
    assert usa_sufffact.is_in_lineage(acptfact_pick=texas_acptfact.pick)

    # GIVEN
    sea_road = create_road("earth", "sea", delimiter=slash_text)  # "earth,sea"
    seaside_road = create_road(
        "earth", "seaside", delimiter=slash_text
    )  # "earth,seaside,beach"
    seaside_beach_road = create_road(
        seaside_road, "beach", delimiter=slash_text
    )  # "earth,seaside,beach"

    # WHEN
    sea_sufffact = sufffactunit_shop(need=sea_road, delimiter=slash_text)

    # THEN
    sea_acptfact = acptfactheir_shop(base=sea_road, pick=sea_road)
    assert sea_sufffact.is_in_lineage(acptfact_pick=sea_acptfact.pick)
    seaside_acptfact = acptfactheir_shop(seaside_beach_road, seaside_beach_road)
    assert sea_sufffact.is_in_lineage(acptfact_pick=seaside_acptfact.pick) == False


def test_sufffact_get_range_segregate_status_ReturnsCorrectStatusBoolForRangeSuffFact():
    # GIVEN
    yr_text = "ced_year"
    yr_road = create_road(root_label(), yr_text)
    yr_sufffact = sufffactunit_shop(need=yr_road, open=3, nigh=13)

    # WHEN / THEN
    yr_acptfact = acptfactheir_shop(base=yr_road, open=5, nigh=11, pick=yr_road)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == True

    yr_acptfact = acptfactheir_shop(base=yr_road, open=1, nigh=11, pick=yr_road)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == True

    yr_acptfact = acptfactheir_shop(base=yr_road, open=8, nigh=17, pick=yr_road)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == True

    yr_acptfact = acptfactheir_shop(base=yr_road, open=0, nigh=2, pick=yr_road)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == False

    yr_acptfact = acptfactheir_shop(base=yr_road, open=15, nigh=19, pick=yr_road)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == False

    yr_acptfact = acptfactheir_shop(base=yr_road, open=1, nigh=19, pick=yr_road)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == True

    # boundary tests
    yr_acptfact = acptfactheir_shop(base=yr_road, open=13, nigh=19, pick=yr_road)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == False

    yr_acptfact = acptfactheir_shop(base=yr_road, open=0, nigh=3, pick=yr_road)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == True


def test_sufffact_get_range_segregate_status_ReturnsCorrectStatusBoolForSegregateSuffFact():
    # GIVEN
    yr_text = "ced_year"
    yr_road = create_road(root_label(), yr_text)
    yr_sufffact = sufffactunit_shop(need=yr_road, divisor=5, open=0, nigh=0)

    # WHEN / THEN
    yr_acptfact = acptfactheir_shop(base=yr_road, pick=yr_road, open=5, nigh=5)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == True

    yr_acptfact = acptfactheir_shop(base=yr_road, pick=yr_road, open=6, nigh=6)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == False

    yr_acptfact = acptfactheir_shop(base=yr_road, pick=yr_road, open=4, nigh=6)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == True

    yr_acptfact = acptfactheir_shop(base=yr_road, pick=yr_road, open=3, nigh=4)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == False

    # GIVEN
    yr_sufffact = sufffactunit_shop(need=yr_road, divisor=5, open=0, nigh=2)

    # WHEN / THEN
    yr_acptfact = acptfactheir_shop(base=yr_road, pick=yr_road, open=2, nigh=2)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == False

    yr_acptfact = acptfactheir_shop(base=yr_road, pick=yr_road, open=102, nigh=102)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == False

    yr_acptfact = acptfactheir_shop(base=yr_road, pick=yr_road, open=1, nigh=4)
    assert yr_sufffact._get_range_segregate_status(acptfactheir=yr_acptfact) == True


def test_sufffact_is_range_or_segregate_ReturnsCorrectBool():
    # GIVE
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)

    # WHEN / THEN
    wkday_sufffact = sufffactunit_shop(need=wkday_road)
    assert wkday_sufffact._is_range_or_segregate() == False

    wkday_sufffact = sufffactunit_shop(need=wkday_road, open=5, nigh=13)
    assert wkday_sufffact._is_range_or_segregate() == True

    wkday_sufffact = sufffactunit_shop(need=wkday_road, divisor=17, open=7, nigh=7)
    assert wkday_sufffact._is_range_or_segregate() == True


def test_get_sufffact_status_returnsCorrectsufffactstatus():
    # WHEN assumes acptfact is in lineage
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wkday_sufffact = sufffactunit_shop(need=wkday_road)

    # WHEN / THEN
    wkday_acptfact = acptfactheir_shop(base=wkday_road, pick=wkday_road)
    assert wkday_sufffact._get_active_status(acptfactheir=wkday_acptfact) == True
    # if acptfact has range but sufffact does not reqquire range, acptfact's range does not matter
    wkday_acptfact = acptfactheir_shop(base=wkday_road, pick=wkday_road, open=0, nigh=2)
    assert wkday_sufffact._get_active_status(acptfactheir=wkday_acptfact) == True


def test_get_sufffact_status_returnsCorrectRangedsufffactstatus():
    # GIVEN assumes acptfact is in lineage
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wkday_sufffact = sufffactunit_shop(need=wkday_road, open=3, nigh=7)

    # WHEN / THEN
    wkday_acptfact = acptfactheir_shop(base=wkday_road, pick=wkday_road)
    assert wkday_sufffact._get_active_status(acptfactheir=wkday_acptfact) == False
    wkday_acptfact = acptfactheir_shop(base=wkday_road, pick=wkday_road, open=0, nigh=2)
    assert wkday_sufffact._get_active_status(acptfactheir=wkday_acptfact) == False


def test_sufffact_set_status_CorrectlySetsStatusWhenAcptFactIsNull():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    after_text = "afternoon"
    after_road = create_road(wkday_road, after_text)
    sufffact_2 = sufffactunit_shop(need=after_road)
    agenda_acptfact_2 = None
    assert sufffact_2._status is None

    # WHEN
    sufffact_2.set_status(acptfactheir=agenda_acptfact_2)

    # GIVEN
    assert sufffact_2._status == False


def test_sufffact_set_status_CorrectlySetsStatusOfSimple():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_sufffact = sufffactunit_shop(need=wed_road)
    agenda_acptfact = acptfactheir_shop(base=wkday_road, pick=wed_road)
    assert wed_sufffact._status is None

    # WHEN
    wed_sufffact.set_status(acptfactheir=agenda_acptfact)

    # THEN
    assert wed_sufffact._status == True


def test_sufffact_set_status_CorrectlySetsStatus_2():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_after_text = "afternoon"
    wed_after_road = create_road(wed_road, wed_after_text)
    wed_after_sufffact = sufffactunit_shop(need=wed_after_road)
    assert wed_after_sufffact._status is None

    # WHEN
    wed_acptfact = acptfactheir_shop(base=wkday_road, pick=wed_road)
    wed_after_sufffact.set_status(acptfactheir=wed_acptfact)

    # THEN
    assert wed_after_sufffact._status == True


def test_sufffact_set_status_CorrectlySetsStatus_3():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_noon_text = "noon"
    wed_noon_road = create_road(wed_road, wed_noon_text)
    wed_sufffact = sufffactunit_shop(need=wed_road)
    assert wed_sufffact._status is None

    # WHEN
    noon_acptfact = acptfactheir_shop(base=wkday_road, pick=wed_noon_road)
    wed_sufffact.set_status(acptfactheir=noon_acptfact)

    # THEN
    assert wed_sufffact._status == True


def test_sufffact_set_status_CorrectlySetsStatus_4():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    thu_text = "thursday"
    thu_road = create_road(wkday_road, thu_text)
    wed_sufffact = sufffactunit_shop(need=wed_road)
    thu_acptfact = acptfactheir_shop(base=wkday_road, pick=thu_road)
    assert wed_sufffact._status is None
    assert wed_sufffact.is_in_lineage(acptfact_pick=thu_acptfact.pick) == False
    assert thu_acptfact.open is None
    assert thu_acptfact.nigh is None

    # WHEN
    wed_sufffact.set_status(acptfactheir=thu_acptfact)

    # THEN
    assert wed_sufffact._status == False


def test_sufffact_set_status_CorrectlySetsStatus_5():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_sun_text = "sunny"
    wed_sun_road = create_road(wed_road, wed_sun_text)
    wed_rain_text = "rainy"
    wed_rain_road = create_road(wed_road, wed_rain_text)
    wed_sun_sufffact = sufffactunit_shop(need=wed_sun_road)
    assert wed_sun_sufffact._status is None

    # WHEN
    wed_rain_acptfact = acptfactheir_shop(base=wkday_road, pick=wed_rain_road)
    wed_sun_sufffact.set_status(acptfactheir=wed_rain_acptfact)

    # THEN
    assert wed_sun_sufffact._status == False


def test_sufffact_set_status_CorrectlySetsTimeRangeStatusTrue():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    hr24_text = "24hr"
    hr24_road = create_road(timetech_road, hr24_text)
    hr24_sufffact = sufffactunit_shop(need=hr24_road, open=7, nigh=7)
    assert hr24_sufffact._status is None

    # WHEN
    range_0_to_8_acptfact = acptfactheir_shop(hr24_road, hr24_road, open=0, nigh=8)
    hr24_sufffact.set_status(acptfactheir=range_0_to_8_acptfact)

    # THEN
    assert hr24_sufffact._status == True


def test_sufffact_set_task_CorrectlySetsTaskBool_01():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    no_range_sufffact = sufffactunit_shop(need=hr24_road)
    no_range_sufffact._status = False

    # WHEN / THEN
    no_range_acptfact = acptfactheir_shop(base=hr24_road, pick=hr24_road)
    assert no_range_sufffact._get_task_status(acptfactheir=no_range_acptfact) == False


def test_sufffact_set_task_CorrectlySetsTaskBoolRangeTrue():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    range_5_to_31_sufffact = sufffactunit_shop(need=hr24_road, open=5, nigh=31)
    range_5_to_31_sufffact._status = True

    # WHEN / THEN
    range_7_to_41_acptfact = acptfactheir_shop(hr24_road, hr24_road, open=7, nigh=41)
    assert range_5_to_31_sufffact._get_task_status(range_7_to_41_acptfact) == True


def test_sufffact_set_task_CorrectlySetsTaskBoolRangeFalse():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    range_5_to_31_sufffact = sufffactunit_shop(need=hr24_road, open=5, nigh=31)
    range_5_to_31_sufffact._status = True

    # WHEN / THEN
    range_7_to_21_acptfact = acptfactheir_shop(hr24_road, hr24_road, open=7, nigh=21)
    assert range_5_to_31_sufffact._get_task_status(range_7_to_21_acptfact) == False


def test_sufffact_set_task_CorrectlySetsTaskBoolSegregateFalse_01():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    o0_n0_d5_sufffact = sufffactunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_sufffact._status = True

    # WHEN / THEN
    range_3_to_5_acptfact = acptfactheir_shop(hr24_road, hr24_road, open=3, nigh=5)
    assert o0_n0_d5_sufffact._get_task_status(range_3_to_5_acptfact) == False


def test_sufffact_set_task_CorrectlySetsTaskBoolSegregateFalse_03():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    o0_n0_d5_sufffact = sufffactunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_sufffact._status = False

    # WHEN / THEN
    range_5_to_7_acptfact = acptfactheir_shop(hr24_road, hr24_road, open=5, nigh=7)
    assert o0_n0_d5_sufffact._get_task_status(range_5_to_7_acptfact) == False


def test_sufffact_set_task_CorrectlySetsTaskBoolSegregateTrue_01():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    o0_n0_d5_sufffact = sufffactunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_sufffact._status = True

    # WHEN / THEN
    range_5_to_7_acptfact = acptfactheir_shop(hr24_road, hr24_road, open=5, nigh=7)
    assert o0_n0_d5_sufffact._get_task_status(range_5_to_7_acptfact) == True


def test_sufffact_set_task_CorrectlySetsTaskBoolSegregateTrue_02():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    o0_n0_d5_sufffact = sufffactunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_sufffact._status = True

    # WHEN / THEN
    range_5_to_5_acptfact = acptfactheir_shop(hr24_road, hr24_road, open=5, nigh=5)
    assert o0_n0_d5_sufffact._get_task_status(acptfactheir=range_5_to_5_acptfact)


def test_sufffact_set_task_NotNull():
    # GIVEN
    week_text = "weekdays"
    week_road = create_road(root_label(), week_text)
    wed_text = "Wednesday"
    wed_road = create_road(week_road, wed_text)
    wed_sufffact = sufffactunit_shop(need=wed_road)
    wed_sufffact._status = True

    # GIVEN
    acptfactheir = acptfactheir_shop(base=week_road, pick=wed_road)

    # THEN
    assert wed_sufffact._get_task_status(acptfactheir=acptfactheir) == False


def test_sufffact_set_status_CorrectlySetsTimeRangeTaskTrue_v1():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    range_2_to_7_sufffact = sufffactunit_shop(need=hr24_road, open=2, nigh=7)
    assert range_2_to_7_sufffact._status is None
    assert range_2_to_7_sufffact._task is None

    # WHEN
    range_0_to_5_acptfact = acptfactheir_shop(hr24_road, hr24_road, open=0, nigh=5)
    range_2_to_7_sufffact.set_status(acptfactheir=range_0_to_5_acptfact)

    # THEN
    assert range_2_to_7_sufffact._status == True
    assert range_2_to_7_sufffact._task == False


def test_sufffact_set_status_CorrectlySetsTimeRangeTaskTrue_v2():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    range_2_to_7_sufffact = sufffactunit_shop(need=hr24_road, open=2, nigh=7)
    range_0_to_8_acptfact = acptfactheir_shop(hr24_road, hr24_road, open=0, nigh=8)
    assert range_2_to_7_sufffact._status is None

    # WHEN
    range_2_to_7_sufffact.set_status(acptfactheir=range_0_to_8_acptfact)
    # THEN
    assert range_2_to_7_sufffact._status == True
    assert range_2_to_7_sufffact._task == True

    # GIVEN
    range_3_to_5_acptfact = acptfactheir_shop(hr24_road, hr24_road, open=3, nigh=5)
    # WHEN
    range_2_to_7_sufffact.set_status(acptfactheir=range_3_to_5_acptfact)
    # THEN
    assert range_2_to_7_sufffact._status
    assert range_2_to_7_sufffact._task == False

    # GIVEN
    range_8_to_8_acptfact = acptfactheir_shop(hr24_road, hr24_road, open=8, nigh=8)
    # WHEN
    range_2_to_7_sufffact.set_status(acptfactheir=range_8_to_8_acptfact)
    assert range_2_to_7_sufffact._status == False
    assert range_2_to_7_sufffact._task == False


def test_sufffact_set_status_CorrectlySetsTimeRangeStatusFalse():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    hr24_text = "24hr"
    hr24_road = create_road(timetech_road, hr24_text)
    hr24_sufffact = sufffactunit_shop(need=hr24_road, open=7, nigh=7)
    assert hr24_sufffact._status is None

    # WHEN
    agenda_acptfact = acptfactheir_shop(base=hr24_road, pick=hr24_road, open=8, nigh=10)
    hr24_sufffact.set_status(acptfactheir=agenda_acptfact)

    # THEN
    assert hr24_sufffact._status == False


def test_sufffact_set_status_CorrectlySetCEDWeekStatusFalse():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    o1_n1_d6_sufffact = sufffactunit_shop(need=week_road, divisor=6, open=1, nigh=1)
    assert o1_n1_d6_sufffact._status is None

    # WHEN
    range_6_to_6_acptfact = acptfactheir_shop(week_road, week_road, open=6, nigh=6)
    o1_n1_d6_sufffact.set_status(acptfactheir=range_6_to_6_acptfact)

    # THEN
    assert o1_n1_d6_sufffact._status == False


def test_sufffact_set_status_CorrectlySetCEDWeekStatusTrue():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_sufffact = sufffactunit_shop(need=week_road, divisor=6, open=1, nigh=1)
    agenda_acptfact = acptfactheir_shop(base=week_road, pick=week_road, open=7, nigh=7)
    assert week_sufffact._status is None

    # WHEN
    week_sufffact.set_status(acptfactheir=agenda_acptfact)

    # THEN
    assert week_sufffact._status == True


def test_sufffact_get_dict_ReturnsCorrectDictWithDvisiorAndOpenNigh():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_sufffact = sufffactunit_shop(need=week_road, divisor=6, open=1, nigh=1)

    # WHEN
    sufffact_dict = week_sufffact.get_dict()

    # THEN
    assert sufffact_dict != None
    static_dict = {"need": week_road, "open": 1, "nigh": 1, "divisor": 6}
    assert sufffact_dict == static_dict


def test_sufffact_get_dict_ReturnsCorrectDictWithOpenAndNigh():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_sufffact = sufffactunit_shop(need=week_road, open=1, nigh=4)

    # WHEN
    sufffact_dict = week_sufffact.get_dict()

    # THEN
    assert sufffact_dict != None
    static_dict = {"need": week_road, "open": 1, "nigh": 4}
    assert sufffact_dict == static_dict


def test_sufffact_get_dict_ReturnsCorrectDictWithOnlyRoadUnit():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_sufffact = sufffactunit_shop(need=week_road)

    # WHEN
    sufffact_dict = week_sufffact.get_dict()

    # THEN
    assert sufffact_dict != None
    static_dict = {"need": week_road}
    assert sufffact_dict == static_dict


def test_sufffact_get_key_road():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_sufffact = sufffactunit_shop(need=week_road)

    # WHEN / THEN
    assert week_sufffact.get_key_road() == week_road


def test_sufffact_find_replace_road_works():
    # GIVEN
    old_root_road = root_label()
    weekday_text = "weekday"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    old_sunday_road = create_road(weekday_road, sunday_text)
    sunday_sufffact = sufffactunit_shop(need=old_sunday_road)
    print(sunday_sufffact)
    assert sunday_sufffact.need == old_sunday_road

    # WHEN
    new_road = "fun"
    sunday_sufffact.find_replace_road(old_road=old_root_road, new_road=new_road)
    new_weekday_road = create_road(new_road, weekday_text)
    new_sunday_road = create_road(new_weekday_road, sunday_text)

    # THEN
    assert sunday_sufffact.need == new_sunday_road


def test_sufffact_meld_works():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    x1_sufffact = sufffactunit_shop(need=week_road)
    y1_sufffact = sufffactunit_shop(need=week_road)

    # WHEN/THEN
    assert x1_sufffact == x1_sufffact.meld(y1_sufffact)

    # GIVEN
    x_sufffact2 = sufffactunit_shop(need=week_road, open=45, nigh=55)
    y2_sufffact = sufffactunit_shop(need=week_road, open=45, nigh=55)
    # WHEN/THEN
    assert x_sufffact2 == x_sufffact2.meld(y2_sufffact)


def test_sufffact_meld_raises_NotSameRoadUnitError():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    x_sufffact = sufffactunit_shop(need=week_road)
    y_sufffact = sufffactunit_shop(need=timetech_road)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_sufffact == x_sufffact.meld(y_sufffact)
    assert (
        str(excinfo.value)
        == f"Meld fail: need={y_sufffact.need} is different self.need='{x_sufffact.need}'"
    )


def test_sufffact_meld_raises_NotSameOpenError():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    x_sufffact = sufffactunit_shop(need=timetech_road, open=1, nigh=3, divisor=8)
    y_sufffact = sufffactunit_shop(need=timetech_road, open=0, nigh=3, divisor=8)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_sufffact == x_sufffact.meld(y_sufffact)
    assert (
        str(excinfo.value)
        == f"Meld fail: need={y_sufffact.need} open={y_sufffact.open} is different self.open={x_sufffact.open}"
    )


def test_sufffact_meld_raises_NotSameNighError():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    x_sufffact = sufffactunit_shop(need=timetech_road, open=1, nigh=5, divisor=8)
    y_sufffact = sufffactunit_shop(need=timetech_road, open=1, nigh=3, divisor=8)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_sufffact == x_sufffact.meld(y_sufffact)
    assert (
        str(excinfo.value)
        == f"Meld fail: need={y_sufffact.need} nigh={y_sufffact.nigh} is different self.nigh={x_sufffact.nigh}"
    )


def test_sufffact_meld_raises_NotSameDivisorError():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    x_sufffact = sufffactunit_shop(need=timetech_road, open=1, nigh=5, divisor=8)
    y_sufffact = sufffactunit_shop(need=timetech_road, open=1, nigh=5, divisor=10)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_sufffact == x_sufffact.meld(y_sufffact)
    assert (
        str(excinfo.value)
        == f"Meld fail: need={y_sufffact.need} divisor={y_sufffact.divisor} is different self.divisor={x_sufffact.divisor}"
    )


def test_sufffacts_get_from_dict_CorrectlyReturnsCompleteObj():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    static_dict = {
        weekday_road: {
            "need": weekday_road,
            "open": 1,
            "nigh": 30,
            "divisor": 5,
        }
    }

    # WHEN
    sufffacts_dict = sufffacts_get_from_dict(static_dict)

    # THEN
    assert len(sufffacts_dict) == 1
    weekday_sufffact = sufffacts_dict.get(weekday_road)
    assert weekday_sufffact == sufffactunit_shop(weekday_road, 1, 30, divisor=5)


def test_sufffacts_get_from_dict_CorrectlyBuildsObjFromIncompleteDict():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    static_dict = {weekday_road: {"need": weekday_road}}

    # WHEN
    sufffacts_dict = sufffacts_get_from_dict(static_dict)

    # THEN
    assert len(sufffacts_dict) == 1
    weekday_sufffact = sufffacts_dict.get(weekday_road)
    assert weekday_sufffact == sufffactunit_shop(weekday_road)


def test_SuffFactsUnit_set_delimiter_SetsAttrsCorrectly():
    # GIVEN
    week_text = "weekday"
    sun_text = "Sunday"
    slash_text = "/"
    slash_week_road = create_road(root_label(), week_text, delimiter=slash_text)
    slash_sun_road = create_road(slash_week_road, sun_text, delimiter=slash_text)
    sun_sufffactunit = sufffactunit_shop(slash_sun_road, delimiter=slash_text)
    assert sun_sufffactunit.delimiter == slash_text
    assert sun_sufffactunit.need == slash_sun_road

    # WHEN
    star_text = "*"
    sun_sufffactunit.set_delimiter(new_delimiter=star_text)

    # THEN
    assert sun_sufffactunit.delimiter == star_text
    star_week_road = create_road(root_label(), week_text, delimiter=star_text)
    star_sun_road = create_road(star_week_road, sun_text, delimiter=star_text)
    assert sun_sufffactunit.need == star_sun_road
