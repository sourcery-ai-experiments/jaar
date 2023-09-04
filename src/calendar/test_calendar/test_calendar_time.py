from src.calendar.calendar import CalendarUnit
from datetime import datetime
from random import randint


def test_time_get_time_min_from_dt_WorksCorrectly():
    g_lw = CalendarUnit(_owner="src")
    g_lw.set_time_hreg_ideas(c400_count=6)
    assert g_lw.get_time_min_from_dt(dt=datetime(2000, 1, 1, 0, 0))
    assert g_lw.get_time_min_from_dt(dt=datetime(1, 1, 1, 0, 0)) == 527040
    assert g_lw.get_time_min_from_dt(dt=datetime(1, 1, 2, 0, 0)) == 527040 + 1440
    assert g_lw.get_time_min_from_dt(dt=datetime(400, 1, 1, 0, 0)) == 210379680
    assert g_lw.get_time_min_from_dt(dt=datetime(800, 1, 1, 0, 0)) == 420759360
    assert g_lw.get_time_min_from_dt(dt=datetime(1200, 1, 1, 0, 0)) == 631139040


def test_get_time_400YearCycle_from_min_WorksCorrectly():
    g_lw = CalendarUnit(_owner="src")
    g_lw.set_time_hreg_ideas(c400_count=6)
    assert g_lw.get_time_c400_from_min(min=0)[0] == 0
    assert g_lw.get_time_c400_from_min(min=210379680)[0] == 1
    assert g_lw.get_time_c400_from_min(min=210379681)[0] == 1
    assert g_lw.get_time_c400_from_min(min=841518720)[0] == 4


def test_get_time_c400year_from_min_WorksCorrectly():
    g_lw = CalendarUnit(_owner="src")
    g_lw.set_time_hreg_ideas(c400_count=6)
    assert g_lw.get_time_c400yr_from_min(min=0)[0] == 0
    assert g_lw.get_time_c400yr_from_min(min=1)[0] == 0
    assert g_lw.get_time_c400yr_from_min(min=1)[2] == 1
    assert g_lw.get_time_c400yr_from_min(min=210379680)[0] == 0
    assert g_lw.get_time_c400yr_from_min(min=210379680)[0] == 0
    assert g_lw.get_time_c400yr_from_min(min=210379681)[0] == 0
    assert g_lw.get_time_c400yr_from_min(min=841518720)[0] == 0
    assert g_lw.get_time_c400yr_from_min(min=576000)[0] == 1
    assert g_lw.get_time_c400yr_from_min(min=4608000)[0] == 8
    assert g_lw.get_time_c400yr_from_min(min=157785120)[0] == 300


def _check_time_conversion_works_with_random_inputs(ax: CalendarUnit):
    py_dt = datetime(
        year=randint(1, 2800),
        month=randint(1, 12),
        day=randint(1, 28),
        hour=randint(0, 23),
        minute=randint(0, 59),
    )
    print(f"Attempt {py_dt=}")
    assert py_dt == ax.get_time_dt_from_min(min=ax.get_time_min_from_dt(dt=py_dt))


def test_get_time_dt_from_min_WorksCorrectly():
    g_lw = CalendarUnit(_owner="src")
    g_lw.set_time_hreg_ideas(c400_count=6)
    assert g_lw.get_time_dt_from_min(min=5000000)
    # assert g_lw.get_time_dt_from_min(
    #     min=g_lw.get_time_min_from_dt(dt=datetime(2000, 1, 1, 0, 0))
    # ) == datetime(2000, 1, 1, 0, 0)
    assert g_lw.get_time_dt_from_min(min=420759360) == datetime(800, 1, 1, 0, 0)
    assert g_lw.get_time_dt_from_min(min=631139040) == datetime(1200, 1, 1, 0, 0)
    assert g_lw.get_time_dt_from_min(min=631751040) == datetime(1201, 3, 1, 0, 0)
    assert g_lw.get_time_dt_from_min(min=631751060) == datetime(1201, 3, 1, 0, 20)

    x_minutes = 1063903680
    assert g_lw.get_time_dt_from_min(min=x_minutes) == datetime(2022, 10, 29, 0, 0)
    x_next_day = x_minutes + 1440
    assert g_lw.get_time_dt_from_min(min=x_next_day) == datetime(2022, 10, 30, 0, 0)

    _check_time_conversion_works_with_random_inputs(g_lw)
    _check_time_conversion_works_with_random_inputs(g_lw)
    _check_time_conversion_works_with_random_inputs(g_lw)

    # for year, month, day, hr, min in .product(
    #     range(479, 480), range(1, 3), range(20, 28), range(12, 14), range(1430, 1440)
    # ):
    #     # for day in range(1, 32):
    #     # # print(f"assert for {year=} {month=} {day=}")
    #     # with contextlib.suppress(Exception):
    #     print(f"Attempt get_time_from_dt {year=} {month=} {day=} {hr=} {min=}")
    #     py_dt = datetime(year, month, day, 0, 0)
    #     jaja_min = g_lw.get_time_min_from_dt(dt=py_dt)
    #     # print(f"assert for {year=} {month=} {day=} {jaja_min}")

    #     jaja_dt = g_lw.get_time_dt_from_min(min=jaja_min)
    #     print(
    #         f"assert attempted for {year=} {month=} {day} \t {jaja_min} Jaja too large: {str(jaja_dt-py_dt)} ({py_dt=})"
    #     )
    #     assert py_dt == jaja_dt

    # if dt_exist:

    # for year in range(480, 481):
    #     for month in range(1, 12):
    #         for day in range(1, 30):
    #             assert g_lw.get_time_dt_from_min(
    #                 min=g_lw.get_time_min_from_dt(dt=datetime(year, month, day, 0, 0))
    #             ) == datetime(year, month, day, 0, 0)


def test_get_time_():
    # Given
    g_lw = CalendarUnit(_owner="src")
    g_lw.set_time_hreg_ideas(c400_count=6)

    idea_list = g_lw.get_idea_list()
    # for idea_x in idea_list:
    #     if idea_x._desc in ["min2010", "years"]:
    #         print(
    #             f"{idea_x._walk=} \t{idea_x._desc=} {idea_x._begin=} {idea_x._close=} {idea_x._addin=}"
    #         )

    # When
    g_lw.set_time_acptfacts(
        open=datetime(2000, 1, 1, 0, 0), nigh=datetime(2003, 11, 15, 4, 0)
    )

    # Then
    assert g_lw._idearoot._acptfactunits[f"{g_lw._owner},time,jajatime"]
    assert (
        g_lw._idearoot._acptfactunits[f"{g_lw._owner},time,jajatime"].open == 1051898400
    )  # - 1440
    assert (
        g_lw._idearoot._acptfactunits[f"{g_lw._owner},time,jajatime"].nigh == 1053934800
    )  # - 1440


# def test_time_hreg_set_exists():
#     g_lw = CalendarUnit(_owner="src")
#     g_lw.set_time_hreg_ideas(c400_count=6)
#     idea_x = g_lw.get_idea_kid(road="src,hreg")
#     assert idea_x != None
#     assert g_lw._kids["hreg"]
#     for kid in g_lw._kids["hreg"]._kids.values():
#         print(f"hreg kid= {kid._desc=}")

#     assert len(g_lw._kids["hreg"]._kids) > 0


# def test_time_hreg_set_creates_idea():
#     g_lw = examples.get_calendar_base_time_example()

#     hreg_name = "hreg"
#     with pytest.raises(KeyError) as excinfo:
#         g_lw._kids[hreg_name]
#     assert str(excinfo.value) == f"'{hreg_name}'"
#     print(f"added {hreg_name}")
#     g_lw.set_time_hreg_ideas(c400_count=6)
#     hreg_idea = g_lw._kids[hreg_name]
#     assert hreg_idea != None
#     assert hreg_idea._begin == 0
#     assert hreg_idea._close == 1262278080


# def test_time_hreg_set_CorrectlyCreatesWeekdayIdea():
#     g_lw = examples.get_calendar_base_time_example()
#     g_lw.set_time_hreg_ideas(c400_count=6)
#     weekday_name = "weekday"
#     weekday = g_lw.get_idea_kid(road=f"src,hreg,{weekday_name}")
#     assert weekday != None
#     assert weekday._begin == 0
#     assert weekday._close == 7
#     assert weekday._kids["Sunday"] != None
#     assert weekday._kids["Monday"] != None
#     assert weekday._kids["Tuesday"] != None
#     assert weekday._kids["Wednesday"] != None
#     assert weekday._kids["Thursday"] != None
#     assert weekday._kids["Friday"] != None
#     assert weekday._kids["Saturday"] != None


# def test_time_hreg_set_CorrectlyCreates400YearCycleCount():
#     g_lw = examples.get_calendar_base_time_example()
#     c400_count = 6
#     g_lw.set_time_hreg_ideas(c400_count=c400_count)

#     timetech_name = "400 year cycle"
#     timetech_road = f"src,hreg,{timetech_name}"
#     print(f"{timetech_road=}")
#     timetech = g_lw.get_idea_kid(road=timetech_road)
#     assert timetech != None
#     assert timetech._begin == 0
#     assert timetech._close == c400_count


# def test_time_hreg_set_CorrectlyCreates400YearCycleYears():
#     h_lw = examples.get_calendar_base_time_example()
#     c400_count = 6
#     h_lw.set_time_hreg_ideas(c400_count=c400_count)

#     hy400_name = "cycle400year_years"
#     hy400_road = f"src,hreg,{hy400_name}"
#     print(f"{hy400_road=}")
#     hy400_idea = h_lw.get_idea_kid(road=hy400_road)
#     assert hy400_idea != None
#     assert hy400_idea._begin is None
#     assert hy400_idea._close is None
#     assert hy400_idea.divisor == 400

#     hy400c1_name = "100yr regular"
#     hy400c1_road = f"{hy400_road},{hy400c1_name}"
#     print(f"{hy400c1_road=}")
#     hy400c1_idea = hy400_idea._kids[hy400c1_name]
#     assert hy400c1_idea != None
#     assert hy400c1_idea._begin == 0
#     assert hy400c1_idea._close == 100
#     assert hy400c1_idea.divisor is None

#     hy400c14y_name = "regular 4yr"
#     hy400c14y_road = f"{hy400c1_road},{hy400c14y_name}"
#     print(f"{hy400c14y_road=}")
#     hy400c14y_idea = hy400c1_idea._kids[hy400c14y_name]
#     assert hy400c14y_idea != None
#     assert hy400c14y_idea._begin is None
#     assert hy400c14y_idea._close is None
#     assert hy400c14y_idea.divisor == 4

#     hy400c3_name = "300yr range"
#     hy400c3_road = f"{hy400_road},{hy400c3_name}"
#     print(f"{hy400c3_road=}")
#     hy400c3_idea = hy400_idea._kids[hy400c3_name]
#     assert hy400c3_idea != None
#     assert hy400c3_idea._begin == 100
#     assert hy400c3_idea._close == 400
#     assert hy400c3_idea.divisor is None

#     hy400c3c1_name = "100yr no century leap"
#     hy400c3c1_road = f"{hy400c3_road},{hy400c3c1_name}"
#     print(f"{hy400c3c1_road=}")
#     hy400c3c1_idea = hy400c3_idea._kids[hy400c3c1_name]
#     assert hy400c3c1_idea != None
#     assert hy400c3c1_idea._begin is None
#     assert hy400c3c1_idea._close is None
#     assert hy400c3c1_idea.divisor == 100

#     hy400c3c14y_name = "4yr no leap"
#     hy400c3c14y_road = f"{hy400c3c1_road},{hy400c3c14y_name}"
#     print(f"{hy400c3c14y_road=}")
#     hy400c3c14y_idea = hy400c3c1_idea._kids[hy400c3c14y_name]
#     assert hy400c3c14y_idea != None
#     assert hy400c3c14y_idea._begin == 0
#     assert hy400c3c14y_idea._close == 4
#     assert hy400c3c14y_idea.divisor is None

#     hy400c3c196_name = "96yr range"
#     hy400c3c196_road = f"{hy400c3c1_road},{hy400c3c196_name}"
#     print(f"{hy400c3c196_road=}")
#     hy400c3c196_idea = hy400c3c1_idea._kids[hy400c3c196_name]
#     assert hy400c3c196_idea != None
#     assert hy400c3c196_idea._begin == 4
#     assert hy400c3c196_idea._close == 100
#     assert hy400c3c196_idea.divisor is None

#     hy400c3c196ry_name = "regular 4yr"
#     hy400c3c196ry_road = f"{hy400c3c196_road},{hy400c3c196ry_name}"
#     print(f"{hy400c3c196ry_road=}")
#     hy400c3c196ry_idea = hy400c3c196_idea._kids[hy400c3c196ry_name]
#     assert hy400c3c196ry_idea != None
#     assert hy400c3c196ry_idea._begin is None
#     assert hy400c3c196ry_idea._close is None
#     assert hy400c3c196ry_idea.divisor == 4


# def test_time_hreg_set_CorrectlyCreates400YearCycleYears():
#     h_lw = examples.get_calendar_base_time_example()
#     c400_count = 6
#     h_lw.set_time_hreg_ideas(c400_count=c400_count)

#     hy400_name = "cycle400year_days"
#     hy400_road = f"src,hreg,{hy400_name}"
#     print(f"{hy400_road=}")
#     hy400_idea = h_lw.get_idea_kid(road=hy400_road)
#     assert hy400_idea != None
#     assert hy400_idea._begin is None
#     assert hy400_idea._close is None
#     assert hy400_idea.divisor == 146097


# def test_time_hreg_set_CorrectlyCreatesDayRange():
#     g_lw = examples.get_calendar_base_time_example()
#     g_lw.set_time_hreg_ideas(c400_count=6)
#     timetech = g_lw.get_idea_kid(road="src,hreg,day_range")
#     assert timetech != None
#     assert timetech._begin == 0
#     assert timetech._close == 876582

# x_lw = CalendarUnit()
# g_lw.get_idea_kid(road={"src,hreg,weekday"})

# wed_sufffact_x = sufffactunit_shop(need=wednesday_road)
# work_wk_required = RequiredUnit(base=weekday_road, sufffacts={wed_sufffact.need: wed_sufffact})
# print(f"{type(work_wk_required.base)=}")
# print(f"{work_wk_required.base=}")
# calendar_x.edit_idea_attr(road=work_road, required=work_wk_required)
# work_idea = calendar_x._kids["work"]
# assert work_idea._requiredunits != None
# print(work_idea._requiredunits)
# assert work_idea._requiredunits[weekday_road] != None
# assert work_idea._requiredunits[weekday_road] == work_wk_required

# g_lw = examples.get_calendar_gregorian_years()


def test_get_jajatime_repeating_legible_text_correctlyText():
    # GIVEN
    src_text = "src"
    cx = CalendarUnit(_owner=src_text)
    cx.set_time_hreg_ideas(c400_count=7)

    # WHEN / THEN
    print("ReturnsDailyText")
    assert (
        cx.get_jajatime_repeating_legible_text(open=480, nigh=480, divisor=1440)
        == "every day at 8am"
    )

    print("ReturnsEvery2DaysText")
    assert (
        cx.get_jajatime_repeating_legible_text(open=490, nigh=490, divisor=2880)
        == "every 2nd day at 8:10am"
    )

    print("ReturnsEvery6DaysText")
    assert (
        cx.get_jajatime_repeating_legible_text(open=480, nigh=480, divisor=8640)
        == "every 6th day at 8am"
    )

    print("ReturnsWeeklyText")
    assert (
        cx.get_jajatime_repeating_legible_text(open=480, nigh=480, divisor=10080)
        == "every Saturday at 8am"
    )

    print("ReturnsEvery2WeeksText")
    assert (
        cx.get_jajatime_repeating_legible_text(open=480, nigh=480, divisor=20160)
        == "every 2nd Saturday at 8am"
    )

    print("ReturnsEvery6WeeksText")
    assert (
        cx.get_jajatime_repeating_legible_text(open=480, nigh=480, divisor=60480)
        == "every 6th Saturday at 8am"
    )

    print("ReturnsOneTimeEventCorrectlyMorning")
    assert (
        cx.get_jajatime_repeating_legible_text(open=1064041020.0, nigh=1064041020.0)
        == "Wed Feb 1st, 2023 at 9am"
    )

    print("ReturnsOneTimeEventCorrectlyEvening")
    assert (
        cx.get_jajatime_repeating_legible_text(open=1064041620.0, nigh=1064041620.0)
        == "Wed Feb 1st, 2023 at 7pm"
    )

    print("ReturnsOneTimeEventCorrectlyMidnight")
    assert (
        cx.get_jajatime_repeating_legible_text(open=1064041920.0, nigh=1064041920.0)
        == "Thu Feb 2nd, 2023 at 12am"
    )
