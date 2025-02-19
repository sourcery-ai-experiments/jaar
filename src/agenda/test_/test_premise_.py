from src.agenda.reason_idea import (
    PremiseUnit,
    premiseunit_shop,
    beliefheir_shop,
    premiseunit_shop,
    premises_get_from_dict,
)
from src._road.road import (
    get_default_world_id_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
    find_replace_road_key_dict,
)
from pytest import raises as pytest_raises


def test_PremiseUnit_Exists():
    # GIVEN
    gig_text = "gig"
    gig_road = create_road(root_label(), gig_text)
    email_text = "check email"
    email_road = create_road(gig_road, email_text)

    # WHEN
    email_premise = PremiseUnit(need=email_road)

    # THEN
    assert email_premise.need == email_road
    assert email_premise.open is None
    assert email_premise.nigh is None
    assert email_premise.divisor is None
    assert email_premise._status is None
    assert email_premise._task is None
    assert email_premise.delimiter is None


def test_premiseunit_shop_ReturnsCorrectObj():
    # GIVEN
    gig_text = "gig"
    gig_road = create_road(root_label(), gig_text)
    email_text = "check email"
    email_road = create_road(gig_road, email_text)

    # WHEN
    email_premise = premiseunit_shop(need=email_road)

    # THEN
    assert email_premise.need == email_road


def test_PremiseUnit_clear_status_CorrectlySetsAttrs():
    # WHEN
    gig_text = "gig"
    gig_road = create_road(root_label(), gig_text)
    gig_premise = premiseunit_shop(need=gig_road)
    # THEN
    assert gig_premise._status is None

    # GIVEN
    gig_premise._status = True
    assert gig_premise._status

    # WHEN
    gig_premise.clear_status()

    # THEN
    assert gig_premise._status is None


def test_PremiseUnit_is_range_CorrectlyIdentifiesRangeStatus():
    # GIVEN
    gig_text = "gig"
    gig_road = create_road(root_label(), gig_text)

    # WHEN
    gig_premise = premiseunit_shop(need=gig_road, open=1, nigh=3)
    # THEN
    assert gig_premise._is_range() == True

    # WHEN
    gig_premise = premiseunit_shop(need=gig_road)
    # THEN
    assert gig_premise._is_range() == False

    # WHEN
    gig_premise = premiseunit_shop(need=gig_road, divisor=5, open=3, nigh=3)
    # THEN
    assert gig_premise._is_range() == False


def test_PremiseUnit_is_segregate_CorrectlyIdentifiesSegregateStatus():
    # GIVEN
    gig_text = "gig"
    gig_road = create_road(root_label(), gig_text)

    # WHEN
    gig_premise = premiseunit_shop(need=gig_road, open=1, nigh=3)
    # THEN
    assert gig_premise._is_segregate() == False

    # WHEN
    gig_premise = premiseunit_shop(need=gig_road)
    # THEN
    assert gig_premise._is_segregate() == False

    # WHEN
    gig_premise = premiseunit_shop(need=gig_road, divisor=5, open=3, nigh=3)
    # THEN
    assert gig_premise._is_segregate() == True


def test_PremiseUnit_is_in_lineage_CorrectlyIdentifiesLineage():
    # GIVEN
    nation_road = create_road(root_label(), "Nation-States")
    usa_road = create_road(nation_road, "USA")
    texas_road = create_road(usa_road, "Texas")
    idaho_road = create_road(usa_road, "Idaho")
    texas_belief = beliefheir_shop(base=usa_road, pick=texas_road)

    # WHEN / THEN
    texas_premise = premiseunit_shop(need=texas_road)
    assert texas_premise.is_in_lineage(belief_pick=texas_belief.pick)

    # WHEN / THEN
    idaho_premise = premiseunit_shop(need=idaho_road)
    assert idaho_premise.is_in_lineage(belief_pick=texas_belief.pick) == False

    # WHEN / THEN
    usa_premise = premiseunit_shop(need=usa_road)
    assert usa_premise.is_in_lineage(belief_pick=texas_belief.pick)

    # GIVEN
    sea_road = create_road("earth", "sea")  # "earth,sea"
    sea_premise = premiseunit_shop(need=sea_road)

    # THEN
    sea_belief = beliefheir_shop(base=sea_road, pick=sea_road)
    assert sea_premise.is_in_lineage(belief_pick=sea_belief.pick)
    seaside_road = create_road("earth", "seaside")  # "earth,seaside,beach"
    seaside_beach_road = create_road(seaside_road, "beach")  # "earth,seaside,beach"
    seaside_belief = beliefheir_shop(seaside_beach_road, seaside_beach_road)
    assert sea_premise.is_in_lineage(belief_pick=seaside_belief.pick) == False


def test_PremiseUnit_is_in_lineage_CorrectlyIdentifiesLineageWithNonDefaultDelimiter():
    # GIVEN
    slash_text = "/"
    nation_road = create_road(root_label(), "Nation-States", delimiter=slash_text)
    usa_road = create_road(nation_road, "USA", delimiter=slash_text)
    texas_road = create_road(usa_road, "Texas", delimiter=slash_text)
    idaho_road = create_road(usa_road, "Idaho", delimiter=slash_text)

    # WHEN
    texas_belief = beliefheir_shop(base=usa_road, pick=texas_road)

    # THEN
    texas_premise = premiseunit_shop(need=texas_road, delimiter=slash_text)
    assert texas_premise.is_in_lineage(belief_pick=texas_belief.pick)

    idaho_premise = premiseunit_shop(need=idaho_road, delimiter=slash_text)
    assert idaho_premise.is_in_lineage(belief_pick=texas_belief.pick) == False

    usa_premise = premiseunit_shop(need=usa_road, delimiter=slash_text)
    print(f"  {usa_premise.need=}")
    print(f"{texas_belief.pick=}")
    assert usa_premise.is_in_lineage(belief_pick=texas_belief.pick)

    # GIVEN
    # "earth,sea"
    # "earth,seaside"
    # "earth,seaside,beach"
    sea_road = create_road("earth", "sea", delimiter=slash_text)
    seaside_road = create_road("earth", "seaside", delimiter=slash_text)
    seaside_beach_road = create_road(seaside_road, "beach", delimiter=slash_text)

    # WHEN
    sea_premise = premiseunit_shop(need=sea_road, delimiter=slash_text)

    # THEN
    sea_belief = beliefheir_shop(base=sea_road, pick=sea_road)
    assert sea_premise.is_in_lineage(belief_pick=sea_belief.pick)
    seaside_belief = beliefheir_shop(seaside_beach_road, seaside_beach_road)
    assert sea_premise.is_in_lineage(belief_pick=seaside_belief.pick) == False


def test_PremiseUnit_get_range_segregate_status_ReturnsCorrectStatusBoolForRangePremise():
    # GIVEN
    yr_text = "ced_year"
    yr_road = create_road(root_label(), yr_text)
    yr_premise = premiseunit_shop(need=yr_road, open=3, nigh=13)

    # WHEN / THEN
    yr_belief = beliefheir_shop(base=yr_road, open=5, nigh=11, pick=yr_road)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == True

    yr_belief = beliefheir_shop(base=yr_road, open=1, nigh=11, pick=yr_road)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == True

    yr_belief = beliefheir_shop(base=yr_road, open=8, nigh=17, pick=yr_road)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == True

    yr_belief = beliefheir_shop(base=yr_road, open=0, nigh=2, pick=yr_road)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == False

    yr_belief = beliefheir_shop(base=yr_road, open=15, nigh=19, pick=yr_road)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == False

    yr_belief = beliefheir_shop(base=yr_road, open=1, nigh=19, pick=yr_road)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == True

    # boundary tests
    yr_belief = beliefheir_shop(base=yr_road, open=13, nigh=19, pick=yr_road)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == False

    yr_belief = beliefheir_shop(base=yr_road, open=0, nigh=3, pick=yr_road)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == True


def test_PremiseUnit_get_range_segregate_status_ReturnsCorrectStatusBoolForSegregatePremise():
    # GIVEN
    yr_text = "ced_year"
    yr_road = create_road(root_label(), yr_text)
    yr_premise = premiseunit_shop(need=yr_road, divisor=5, open=0, nigh=0)

    # WHEN / THEN
    yr_belief = beliefheir_shop(base=yr_road, pick=yr_road, open=5, nigh=5)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == True

    yr_belief = beliefheir_shop(base=yr_road, pick=yr_road, open=6, nigh=6)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == False

    yr_belief = beliefheir_shop(base=yr_road, pick=yr_road, open=4, nigh=6)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == True

    yr_belief = beliefheir_shop(base=yr_road, pick=yr_road, open=3, nigh=4)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == False

    # GIVEN
    yr_premise = premiseunit_shop(need=yr_road, divisor=5, open=0, nigh=2)

    # WHEN / THEN
    yr_belief = beliefheir_shop(base=yr_road, pick=yr_road, open=2, nigh=2)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == False

    yr_belief = beliefheir_shop(base=yr_road, pick=yr_road, open=102, nigh=102)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == False

    yr_belief = beliefheir_shop(base=yr_road, pick=yr_road, open=1, nigh=4)
    assert yr_premise._get_range_segregate_status(beliefheir=yr_belief) == True


def test_PremiseUnitUnit_is_range_or_segregate_ReturnsCorrectBool():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)

    # WHEN / THEN
    wkday_premise = premiseunit_shop(need=wkday_road)
    assert wkday_premise._is_range_or_segregate() == False

    wkday_premise = premiseunit_shop(need=wkday_road, open=5, nigh=13)
    assert wkday_premise._is_range_or_segregate() == True

    wkday_premise = premiseunit_shop(need=wkday_road, divisor=17, open=7, nigh=7)
    assert wkday_premise._is_range_or_segregate() == True


def test_PremiseUnitUnit_get_premise_status_ReturnsCorrect_active():
    # WHEN assumes belief is in lineage
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wkday_premise = premiseunit_shop(need=wkday_road)

    # WHEN / THEN
    wkday_belief = beliefheir_shop(base=wkday_road, pick=wkday_road)
    assert wkday_premise._get_active(beliefheir=wkday_belief) == True
    # if belief has range but premise does not reqquire range, belief's range does not matter
    wkday_belief = beliefheir_shop(base=wkday_road, pick=wkday_road, open=0, nigh=2)
    assert wkday_premise._get_active(beliefheir=wkday_belief) == True


def test_PremiseUnitUnit_get_active_returnsCorrectRanged_active():
    # GIVEN assumes belief is in lineage
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wkday_premise = premiseunit_shop(need=wkday_road, open=3, nigh=7)

    # WHEN / THEN
    wkday_belief = beliefheir_shop(base=wkday_road, pick=wkday_road)
    assert wkday_premise._get_active(beliefheir=wkday_belief) == False
    wkday_belief = beliefheir_shop(base=wkday_road, pick=wkday_road, open=0, nigh=2)
    assert wkday_premise._get_active(beliefheir=wkday_belief) == False


def test_PremiseUnitUnit_set_status_CorrectlySets_status_WhenBeliefUnitIsNull():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    after_text = "afternoon"
    after_road = create_road(wkday_road, after_text)
    premise_2 = premiseunit_shop(need=after_road)
    agenda_belief_2 = None
    assert premise_2._status is None

    # WHEN
    premise_2.set_status(x_beliefheir=agenda_belief_2)

    # GIVEN
    assert premise_2._status == False


def test_PremiseUnitUnit_set_status_CorrectlySetsStatusOfSimple():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_premise = premiseunit_shop(need=wed_road)
    agenda_belief = beliefheir_shop(base=wkday_road, pick=wed_road)
    assert wed_premise._status is None

    # WHEN
    wed_premise.set_status(x_beliefheir=agenda_belief)

    # THEN
    assert wed_premise._status == True


def test_PremiseUnit_set_status_CorrectlySetsStatus_2():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_after_text = "afternoon"
    wed_after_road = create_road(wed_road, wed_after_text)
    wed_after_premise = premiseunit_shop(need=wed_after_road)
    assert wed_after_premise._status is None

    # WHEN
    wed_belief = beliefheir_shop(base=wkday_road, pick=wed_road)
    wed_after_premise.set_status(x_beliefheir=wed_belief)

    # THEN
    assert wed_after_premise._status == True


def test_PremiseUnit_set_status_CorrectlySetsStatus_3():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_noon_text = "noon"
    wed_noon_road = create_road(wed_road, wed_noon_text)
    wed_premise = premiseunit_shop(need=wed_road)
    assert wed_premise._status is None

    # WHEN
    noon_belief = beliefheir_shop(base=wkday_road, pick=wed_noon_road)
    wed_premise.set_status(x_beliefheir=noon_belief)

    # THEN
    assert wed_premise._status == True


def test_PremiseUnit_set_status_CorrectlySetsStatus_4():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    thu_text = "thursday"
    thu_road = create_road(wkday_road, thu_text)
    wed_premise = premiseunit_shop(need=wed_road)
    thu_belief = beliefheir_shop(base=wkday_road, pick=thu_road)
    assert wed_premise._status is None
    assert wed_premise.is_in_lineage(belief_pick=thu_belief.pick) == False
    assert thu_belief.open is None
    assert thu_belief.nigh is None

    # WHEN
    wed_premise.set_status(x_beliefheir=thu_belief)

    # THEN
    assert wed_premise._status == False


def test_PremiseUnit_set_status_CorrectlySetsStatus_5():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_sun_text = "sunny"
    wed_sun_road = create_road(wed_road, wed_sun_text)
    wed_rain_text = "rainy"
    wed_rain_road = create_road(wed_road, wed_rain_text)
    wed_sun_premise = premiseunit_shop(need=wed_sun_road)
    assert wed_sun_premise._status is None

    # WHEN
    wed_rain_belief = beliefheir_shop(base=wkday_road, pick=wed_rain_road)
    wed_sun_premise.set_status(x_beliefheir=wed_rain_belief)

    # THEN
    assert wed_sun_premise._status == False


def test_PremiseUnit_set_status_CorrectlySetsTimeRangeStatusTrue():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    hr24_text = "24hr"
    hr24_road = create_road(timetech_road, hr24_text)
    hr24_premise = premiseunit_shop(need=hr24_road, open=7, nigh=7)
    assert hr24_premise._status is None

    # WHEN
    range_0_to_8_belief = beliefheir_shop(hr24_road, hr24_road, open=0, nigh=8)
    hr24_premise.set_status(x_beliefheir=range_0_to_8_belief)

    # THEN
    assert hr24_premise._status == True


def test_PremiseUnit_set_task_CorrectlySetsTaskBool_01():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    no_range_premise = premiseunit_shop(need=hr24_road)
    no_range_premise._status = False

    # WHEN / THEN
    no_range_belief = beliefheir_shop(base=hr24_road, pick=hr24_road)
    assert no_range_premise._get_task_status(beliefheir=no_range_belief) == False


def test_PremiseUnit_set_task_CorrectlySetsTaskBoolRangeTrue():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    range_5_to_31_premise = premiseunit_shop(need=hr24_road, open=5, nigh=31)
    range_5_to_31_premise._status = True

    # WHEN / THEN
    range_7_to_41_belief = beliefheir_shop(hr24_road, hr24_road, open=7, nigh=41)
    assert range_5_to_31_premise._get_task_status(range_7_to_41_belief) == True


def test_PremiseUnit_set_task_CorrectlySetsTaskBoolRangeFalse():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    range_5_to_31_premise = premiseunit_shop(need=hr24_road, open=5, nigh=31)
    range_5_to_31_premise._status = True

    # WHEN / THEN
    range_7_to_21_belief = beliefheir_shop(hr24_road, hr24_road, open=7, nigh=21)
    assert range_5_to_31_premise._get_task_status(range_7_to_21_belief) == False


def test_PremiseUnit_set_task_CorrectlySetsTaskBoolSegregateFalse_01():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    o0_n0_d5_premise = premiseunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_3_to_5_belief = beliefheir_shop(hr24_road, hr24_road, open=3, nigh=5)
    assert o0_n0_d5_premise._get_task_status(range_3_to_5_belief) == False


def test_PremiseUnit_set_task_CorrectlySetsTaskBoolSegregateFalse_03():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    o0_n0_d5_premise = premiseunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_premise._status = False

    # WHEN / THEN
    range_5_to_7_belief = beliefheir_shop(hr24_road, hr24_road, open=5, nigh=7)
    assert o0_n0_d5_premise._get_task_status(range_5_to_7_belief) == False


def test_PremiseUnit_set_task_CorrectlySetsTaskBoolSegregateTrue_01():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    o0_n0_d5_premise = premiseunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_5_to_7_belief = beliefheir_shop(hr24_road, hr24_road, open=5, nigh=7)
    assert o0_n0_d5_premise._get_task_status(range_5_to_7_belief) == True


def test_PremiseUnit_set_task_CorrectlySetsTaskBoolSegregateTrue_02():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    o0_n0_d5_premise = premiseunit_shop(need=hr24_road, divisor=5, open=0, nigh=0)
    o0_n0_d5_premise._status = True

    # WHEN / THEN
    range_5_to_5_belief = beliefheir_shop(hr24_road, hr24_road, open=5, nigh=5)
    assert o0_n0_d5_premise._get_task_status(beliefheir=range_5_to_5_belief) == False


def test_PremiseUnit_set_task_NotNull():
    # GIVEN
    week_text = "weekdays"
    week_road = create_road(root_label(), week_text)
    wed_text = "Wednesday"
    wed_road = create_road(week_road, wed_text)
    wed_premise = premiseunit_shop(need=wed_road)
    wed_premise._status = True

    # GIVEN
    beliefheir = beliefheir_shop(base=week_road, pick=wed_road)

    # THEN
    assert wed_premise._get_task_status(beliefheir=beliefheir) == False


def test_PremiseUnit_set_status_CorrectlySetsTimeRangeTaskTrue_v1():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    range_2_to_7_premise = premiseunit_shop(need=hr24_road, open=2, nigh=7)
    assert range_2_to_7_premise._status is None
    assert range_2_to_7_premise._task is None

    # WHEN
    range_0_to_5_belief = beliefheir_shop(hr24_road, hr24_road, open=0, nigh=5)
    range_2_to_7_premise.set_status(x_beliefheir=range_0_to_5_belief)

    # THEN
    assert range_2_to_7_premise._status == True
    assert range_2_to_7_premise._task == False


def test_PremiseUnit_set_status_CorrectlySetsTimeRangeTaskTrue_v2():
    # GIVEN
    hr24_text = "24hr"
    hr24_road = create_road(root_label(), hr24_text)
    range_2_to_7_premise = premiseunit_shop(need=hr24_road, open=2, nigh=7)
    range_0_to_8_belief = beliefheir_shop(hr24_road, hr24_road, open=0, nigh=8)
    assert range_2_to_7_premise._status is None

    # WHEN
    range_2_to_7_premise.set_status(x_beliefheir=range_0_to_8_belief)
    # THEN
    assert range_2_to_7_premise._status == True
    assert range_2_to_7_premise._task == True

    # GIVEN
    range_3_to_5_belief = beliefheir_shop(hr24_road, hr24_road, open=3, nigh=5)
    # WHEN
    range_2_to_7_premise.set_status(x_beliefheir=range_3_to_5_belief)
    # THEN
    assert range_2_to_7_premise._status
    assert range_2_to_7_premise._task == False

    # GIVEN
    range_8_to_8_belief = beliefheir_shop(hr24_road, hr24_road, open=8, nigh=8)
    # WHEN
    range_2_to_7_premise.set_status(x_beliefheir=range_8_to_8_belief)
    assert range_2_to_7_premise._status == False
    assert range_2_to_7_premise._task == False


def test_PremiseUnit_set_status_CorrectlySetsTimeRangeStatusFalse():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    hr24_text = "24hr"
    hr24_road = create_road(timetech_road, hr24_text)
    hr24_premise = premiseunit_shop(need=hr24_road, open=7, nigh=7)
    assert hr24_premise._status is None

    # WHEN
    agenda_belief = beliefheir_shop(base=hr24_road, pick=hr24_road, open=8, nigh=10)
    hr24_premise.set_status(x_beliefheir=agenda_belief)

    # THEN
    assert hr24_premise._status == False


def test_PremiseUnit_set_status_CorrectlySetCEDWeekStatusFalse():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    o1_n1_d6_premise = premiseunit_shop(need=week_road, divisor=6, open=1, nigh=1)
    assert o1_n1_d6_premise._status is None

    # WHEN
    range_6_to_6_belief = beliefheir_shop(week_road, week_road, open=6, nigh=6)
    o1_n1_d6_premise.set_status(x_beliefheir=range_6_to_6_belief)

    # THEN
    assert o1_n1_d6_premise._status == False


def test_PremiseUnit_set_status_CorrectlySetCEDWeekStatusTrue():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_premise = premiseunit_shop(need=week_road, divisor=6, open=1, nigh=1)
    agenda_belief = beliefheir_shop(base=week_road, pick=week_road, open=7, nigh=7)
    assert week_premise._status is None

    # WHEN
    week_premise.set_status(x_beliefheir=agenda_belief)

    # THEN
    assert week_premise._status == True


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithDvisiorAndOpenNigh():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_premise = premiseunit_shop(need=week_road, divisor=6, open=1, nigh=1)

    # WHEN
    premise_dict = week_premise.get_dict()

    # THEN
    assert premise_dict != None
    static_dict = {"need": week_road, "open": 1, "nigh": 1, "divisor": 6}
    assert premise_dict == static_dict


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithOpenAndNigh():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_premise = premiseunit_shop(need=week_road, open=1, nigh=4)

    # WHEN
    premise_dict = week_premise.get_dict()

    # THEN
    assert premise_dict != None
    static_dict = {"need": week_road, "open": 1, "nigh": 4}
    assert premise_dict == static_dict


def test_PremiseUnit_get_dict_ReturnsCorrectDictWithOnlyRoadUnit():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_premise = premiseunit_shop(need=week_road)

    # WHEN
    premise_dict = week_premise.get_dict()

    # THEN
    assert premise_dict != None
    static_dict = {"need": week_road}
    assert premise_dict == static_dict


def test_PremiseUnit_get_obj_key():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    week_premise = premiseunit_shop(need=week_road)

    # WHEN / THEN
    assert week_premise.get_obj_key() == week_road


def test_PremiseUnit_find_replace_road_gigs():
    # GIVEN
    old_root_road = root_label()
    weekday_text = "weekday"
    weekday_road = create_road(root_label(), weekday_text)
    sunday_text = "Sunday"
    old_sunday_road = create_road(weekday_road, sunday_text)
    sunday_premise = premiseunit_shop(need=old_sunday_road)
    print(sunday_premise)
    assert sunday_premise.need == old_sunday_road

    # WHEN
    new_road = "fun"
    sunday_premise.find_replace_road(old_road=old_root_road, new_road=new_road)
    new_weekday_road = create_road(new_road, weekday_text)
    new_sunday_road = create_road(new_weekday_road, sunday_text)

    # THEN
    assert sunday_premise.need == new_sunday_road


def test_PremiseUnit_meld_gigs():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    x1_premise = premiseunit_shop(need=week_road)
    y1_premise = premiseunit_shop(need=week_road)

    # WHEN/THEN
    assert x1_premise == x1_premise.meld(y1_premise)

    # GIVEN
    x_premise2 = premiseunit_shop(need=week_road, open=45, nigh=55)
    y2_premise = premiseunit_shop(need=week_road, open=45, nigh=55)
    # WHEN/THEN
    assert x_premise2 == x_premise2.meld(y2_premise)


def test_PremiseUnit_meld_raises_NotSameRoadUnitError():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    week_text = "ced_week"
    week_road = create_road(timetech_road, week_text)
    x_premise = premiseunit_shop(need=week_road)
    y_premise = premiseunit_shop(need=timetech_road)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_premise == x_premise.meld(y_premise)
    assert (
        str(excinfo.value)
        == f"Meld fail: need={y_premise.need} is different self.need='{x_premise.need}'"
    )


def test_PremiseUnit_meld_raises_NotSameOpenError():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    x_premise = premiseunit_shop(need=timetech_road, open=1, nigh=3, divisor=8)
    y_premise = premiseunit_shop(need=timetech_road, open=0, nigh=3, divisor=8)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_premise == x_premise.meld(y_premise)
    assert (
        str(excinfo.value)
        == f"Meld fail: need={y_premise.need} open={y_premise.open} is different self.open={x_premise.open}"
    )


def test_PremiseUnit_meld_raises_NotSameNighError():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    x_premise = premiseunit_shop(need=timetech_road, open=1, nigh=5, divisor=8)
    y_premise = premiseunit_shop(need=timetech_road, open=1, nigh=3, divisor=8)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_premise == x_premise.meld(y_premise)
    assert (
        str(excinfo.value)
        == f"Meld fail: need={y_premise.need} nigh={y_premise.nigh} is different self.nigh={x_premise.nigh}"
    )


def test_PremiseUnit_meld_raises_NotSameDivisorError():
    # GIVEN
    timetech_text = "timetech"
    timetech_road = create_road(root_label(), timetech_text)
    x_premise = premiseunit_shop(need=timetech_road, open=1, nigh=5, divisor=8)
    y_premise = premiseunit_shop(need=timetech_road, open=1, nigh=5, divisor=10)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x_premise == x_premise.meld(y_premise)
    assert (
        str(excinfo.value)
        == f"Meld fail: need={y_premise.need} divisor={y_premise.divisor} is different self.divisor={x_premise.divisor}"
    )


def test_PremiseUnits_get_from_dict_ReturnsCompleteObj():
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
    premises_dict = premises_get_from_dict(static_dict)

    # THEN
    assert len(premises_dict) == 1
    weekday_premise = premises_dict.get(weekday_road)
    assert weekday_premise == premiseunit_shop(weekday_road, 1, 30, divisor=5)


def test_PremiseUnits_get_from_dict_CorrectlyBuildsObjFromIncompleteDict():
    # GIVEN
    weekday_text = "weekdays"
    weekday_road = create_road(root_label(), weekday_text)
    static_dict = {weekday_road: {"need": weekday_road}}

    # WHEN
    premises_dict = premises_get_from_dict(static_dict)

    # THEN
    assert len(premises_dict) == 1
    weekday_premise = premises_dict.get(weekday_road)
    assert weekday_premise == premiseunit_shop(weekday_road)


def test_PremiseUnitsUnit_set_delimiter_SetsAttrsCorrectly():
    # GIVEN
    week_text = "weekday"
    sun_text = "Sunday"
    slash_text = "/"
    slash_week_road = create_road(root_label(), week_text, delimiter=slash_text)
    slash_sun_road = create_road(slash_week_road, sun_text, delimiter=slash_text)
    sun_premiseunit = premiseunit_shop(slash_sun_road, delimiter=slash_text)
    assert sun_premiseunit.delimiter == slash_text
    assert sun_premiseunit.need == slash_sun_road

    # WHEN
    star_text = "*"
    sun_premiseunit.set_delimiter(new_delimiter=star_text)

    # THEN
    assert sun_premiseunit.delimiter == star_text
    star_week_road = create_road(root_label(), week_text, delimiter=star_text)
    star_sun_road = create_road(star_week_road, sun_text, delimiter=star_text)
    assert sun_premiseunit.need == star_sun_road


def test_road_find_replace_road_key_dict_ReturnsCorrectPremisesUnit_Scenario1():
    # GIVEN
    casa_road = create_road(root_label(), "casa")
    old_seasons_road = create_road(casa_road, "seasons")
    old_premise_x = premiseunit_shop(need=old_seasons_road)
    old_premises_x = {old_premise_x.need: old_premise_x}

    assert old_premises_x.get(old_seasons_road) == old_premise_x

    # WHEN
    new_seasons_road = create_road(casa_road, "kookies")
    new_premises_x = find_replace_road_key_dict(
        dict_x=old_premises_x, old_road=old_seasons_road, new_road=new_seasons_road
    )
    new_premise_x = premiseunit_shop(need=new_seasons_road)

    assert new_premises_x.get(new_seasons_road) == new_premise_x
    assert new_premises_x.get(old_seasons_road) is None


def test_road_find_replace_road_key_dict_ReturnsCorrectPremisesUnit_Change_world_id_Scenario():
    # GIVEN
    old_world_id = "El Paso"
    casa_text = "casa"
    old_casa_road = create_road(old_world_id, casa_text)
    seasons_text = "seasons"
    old_seasons_road = create_road(old_casa_road, seasons_text)
    old_premise_x = premiseunit_shop(need=old_seasons_road)
    old_premises_x = {old_premise_x.need: old_premise_x}

    assert old_premises_x.get(old_seasons_road) == old_premise_x

    # WHEN
    new_world_id = "Austin"
    new_casa_road = create_road(new_world_id, casa_text)
    new_seasons_road = create_road(new_casa_road, seasons_text)

    new_premises_x = find_replace_road_key_dict(
        dict_x=old_premises_x, old_road=old_seasons_road, new_road=new_seasons_road
    )
    new_premise_x = premiseunit_shop(need=new_seasons_road)

    assert new_premises_x.get(new_seasons_road) == new_premise_x
    assert new_premises_x.get(old_seasons_road) is None
