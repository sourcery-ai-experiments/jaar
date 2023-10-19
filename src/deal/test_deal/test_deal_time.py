from src.deal.deal import DealUnit, dealunit_shop
from datetime import datetime
from random import randint


def test_time_get_time_min_from_dt_WorksCorrectly():
    healer_text = "Kia"
    x_deal = dealunit_shop(_healer=healer_text)
    x_deal.set_time_hreg_ideas(c400_count=6)
    assert x_deal.get_time_min_from_dt(dt=datetime(2000, 1, 1, 0, 0))
    assert x_deal.get_time_min_from_dt(dt=datetime(1, 1, 1, 0, 0)) == 527040
    assert x_deal.get_time_min_from_dt(dt=datetime(1, 1, 2, 0, 0)) == 527040 + 1440
    assert x_deal.get_time_min_from_dt(dt=datetime(400, 1, 1, 0, 0)) == 210379680
    assert x_deal.get_time_min_from_dt(dt=datetime(800, 1, 1, 0, 0)) == 420759360
    assert x_deal.get_time_min_from_dt(dt=datetime(1200, 1, 1, 0, 0)) == 631139040


def test_get_time_400YearCycle_from_min_WorksCorrectly():
    healer_text = "Kia"
    x_deal = dealunit_shop(_healer=healer_text)
    x_deal.set_time_hreg_ideas(c400_count=6)
    assert x_deal.get_time_c400_from_min(min=0)[0] == 0
    assert x_deal.get_time_c400_from_min(min=210379680)[0] == 1
    assert x_deal.get_time_c400_from_min(min=210379681)[0] == 1
    assert x_deal.get_time_c400_from_min(min=841518720)[0] == 4


def test_get_time_c400year_from_min_WorksCorrectly():
    healer_text = "Kia"
    x_deal = dealunit_shop(_healer=healer_text)
    x_deal.set_time_hreg_ideas(c400_count=6)
    assert x_deal.get_time_c400yr_from_min(min=0)[0] == 0
    assert x_deal.get_time_c400yr_from_min(min=1)[0] == 0
    assert x_deal.get_time_c400yr_from_min(min=1)[2] == 1
    assert x_deal.get_time_c400yr_from_min(min=210379680)[0] == 0
    assert x_deal.get_time_c400yr_from_min(min=210379680)[0] == 0
    assert x_deal.get_time_c400yr_from_min(min=210379681)[0] == 0
    assert x_deal.get_time_c400yr_from_min(min=841518720)[0] == 0
    assert x_deal.get_time_c400yr_from_min(min=576000)[0] == 1
    assert x_deal.get_time_c400yr_from_min(min=4608000)[0] == 8
    assert x_deal.get_time_c400yr_from_min(min=157785120)[0] == 300


def _check_time_conversion_works_with_random_inputs(x_deal: DealUnit):
    py_dt = datetime(
        year=randint(1, 2800),
        month=randint(1, 12),
        day=randint(1, 28),
        hour=randint(0, 23),
        minute=randint(0, 59),
    )
    print(f"Attempt {py_dt=}")
    assert py_dt == x_deal.get_time_dt_from_min(
        min=x_deal.get_time_min_from_dt(dt=py_dt)
    )


def test_get_time_dt_from_min_WorksCorrectly():
    healer_text = "Kia"
    x_deal = dealunit_shop(_healer=healer_text)
    x_deal.set_time_hreg_ideas(c400_count=6)
    assert x_deal.get_time_dt_from_min(min=5000000)
    # assert x_deal.get_time_dt_from_min(
    #     min=x_deal.get_time_min_from_dt(dt=datetime(2000, 1, 1, 0, 0))
    # ) == datetime(2000, 1, 1, 0, 0)
    assert x_deal.get_time_dt_from_min(min=420759360) == datetime(800, 1, 1, 0, 0)
    assert x_deal.get_time_dt_from_min(min=631139040) == datetime(1200, 1, 1, 0, 0)
    assert x_deal.get_time_dt_from_min(min=631751040) == datetime(1201, 3, 1, 0, 0)
    assert x_deal.get_time_dt_from_min(min=631751060) == datetime(1201, 3, 1, 0, 20)

    x_minutes = 1063903680
    assert x_deal.get_time_dt_from_min(min=x_minutes) == datetime(2022, 10, 29, 0, 0)
    x_next_day = x_minutes + 1440
    assert x_deal.get_time_dt_from_min(min=x_next_day) == datetime(2022, 10, 30, 0, 0)

    _check_time_conversion_works_with_random_inputs(x_deal)
    _check_time_conversion_works_with_random_inputs(x_deal)
    _check_time_conversion_works_with_random_inputs(x_deal)

    # for year, month, day, hr, min in .product(
    #     range(479, 480), range(1, 3), range(20, 28), range(12, 14), range(1430, 1440)
    # ):
    #     # for day in range(1, 32):
    #     # # print(f"assert for {year=} {month=} {day=}")
    #     # with contextlib.suppress(Exception):
    #     print(f"Attempt get_time_from_dt {year=} {month=} {day=} {hr=} {min=}")
    #     py_dt = datetime(year, month, day, 0, 0)
    #     jaja_min = x_deal.get_time_min_from_dt(dt=py_dt)
    #     # print(f"assert for {year=} {month=} {day=} {jaja_min}")

    #     jaja_dt = x_deal.get_time_dt_from_min(min=jaja_min)
    #     print(
    #         f"assert attempted for {year=} {month=} {day} \t {jaja_min} Jaja too large: {str(jaja_dt-py_dt)} ({py_dt=})"
    #     )
    #     assert py_dt == jaja_dt

    # if dt_exist:

    # for year in range(480, 481):
    #     for month in range(1, 12):
    #         for day in range(1, 30):
    #             assert x_deal.get_time_dt_from_min(
    #                 min=x_deal.get_time_min_from_dt(dt=datetime(year, month, day, 0, 0))
    #             ) == datetime(year, month, day, 0, 0)


def test_get_time_():
    # Given
    healer_text = "Kia"
    x_deal = dealunit_shop(_healer=healer_text)
    x_deal.set_time_hreg_ideas(c400_count=6)

    idea_list = x_deal.get_idea_list()
    # for idea_x in idea_list:
    #     if idea_x._label in ["min2010", "years"]:
    #         print(
    #             f"{idea_x._pad=} \t{idea_x._label=} {idea_x._begin=} {idea_x._close=} {idea_x._addin=}"
    #         )

    # When
    x_deal.set_time_acptfacts(
        open=datetime(2000, 1, 1, 0, 0), nigh=datetime(2003, 11, 15, 4, 0)
    )

    # Then
    time_text = "time"
    time_road = f"{x_deal._project_handle},{time_text}"
    jaja_text = "jajatime"
    jaja_road = f"{time_road},{jaja_text}"
    assert x_deal._idearoot._acptfactunits[jaja_road]
    assert x_deal._idearoot._acptfactunits[jaja_road].open == 1051898400  # - 1440
    assert x_deal._idearoot._acptfactunits[jaja_road].nigh == 1053934800  # - 1440


# def test_time_hreg_set_exists():
#     x_deal = dealunit_shop(_healer=healer_text)
#     x_deal.set_time_hreg_ideas(c400_count=6)
#     idea_x = x_deal.get_idea_kid(road=f"{root_label()},hreg")
#     assert idea_x != None
#     assert x_deal._kids["hreg"]
#     for kid in x_deal._kids["hreg"]._kids.values():
#         print(f"hreg kid= {kid._label=}")

#     assert len(x_deal._kids["hreg"]._kids) > 0


# def test_time_hreg_set_creates_idea():
#     x_deal = examples.get_deal_base_time_example()

#     hreg_title = "hreg"
#     with pytest.raises(KeyError) as excinfo:
#         x_deal._kids[hreg_title]
#     assert str(excinfo.value) == f"'{hreg_title}'"
#     print(f"added {hreg_title}")
#     x_deal.set_time_hreg_ideas(c400_count=6)
#     hreg_idea = x_deal._kids[hreg_title]
#     assert hreg_idea != None
#     assert hreg_idea._begin == 0
#     assert hreg_idea._close == 1262278080


# def test_time_hreg_set_CorrectlyCreatesWeekdayIdea():
#     x_deal = examples.get_deal_base_time_example()
#     x_deal.set_time_hreg_ideas(c400_count=6)
#     weekday_title = "weekday"
#     weekday = x_deal.get_idea_kid(road=f"{root_label()},hreg,{weekday_title}")
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
#     x_deal = examples.get_deal_base_time_example()
#     c400_count = 6
#     x_deal.set_time_hreg_ideas(c400_count=c400_count)

#     timetech_title = "400 year cycle"
#     timetech_road = f"{root_label()},hreg,{timetech_title}"
#     print(f"{timetech_road=}")
#     timetech = x_deal.get_idea_kid(road=timetech_road)
#     assert timetech != None
#     assert timetech._begin == 0
#     assert timetech._close == c400_count


# def test_time_hreg_set_CorrectlyCreates400YearCycleYears():
#     h_x_deal = examples.get_deal_base_time_example()
#     c400_count = 6
#     h_x_deal.set_time_hreg_ideas(c400_count=c400_count)

#     hy400_title = "cycle400year_years"
#     hy400_road = f"{root_label()},hreg,{hy400_title}"
#     print(f"{hy400_road=}")
#     hy400_idea = h_x_deal.get_idea_kid(road=hy400_road)
#     assert hy400_idea != None
#     assert hy400_idea._begin is None
#     assert hy400_idea._close is None
#     assert hy400_idea.divisor == 400

#     hy400c1_title = "100yr regular"
#     hy400c1_road = f"{hy400_road},{hy400c1_title}"
#     print(f"{hy400c1_road=}")
#     hy400c1_idea = hy400_idea._kids[hy400c1_title]
#     assert hy400c1_idea != None
#     assert hy400c1_idea._begin == 0
#     assert hy400c1_idea._close == 100
#     assert hy400c1_idea.divisor is None

#     hy400c14y_title = "regular 4yr"
#     hy400c14y_road = f"{hy400c1_road},{hy400c14y_title}"
#     print(f"{hy400c14y_road=}")
#     hy400c14y_idea = hy400c1_idea._kids[hy400c14y_title]
#     assert hy400c14y_idea != None
#     assert hy400c14y_idea._begin is None
#     assert hy400c14y_idea._close is None
#     assert hy400c14y_idea.divisor == 4

#     hy400c3_title = "300yr range"
#     hy400c3_road = f"{hy400_road},{hy400c3_title}"
#     print(f"{hy400c3_road=}")
#     hy400c3_idea = hy400_idea._kids[hy400c3_title]
#     assert hy400c3_idea != None
#     assert hy400c3_idea._begin == 100
#     assert hy400c3_idea._close == 400
#     assert hy400c3_idea.divisor is None

#     hy400c3c1_title = "100yr no century leap"
#     hy400c3c1_road = f"{hy400c3_road},{hy400c3c1_title}"
#     print(f"{hy400c3c1_road=}")
#     hy400c3c1_idea = hy400c3_idea._kids[hy400c3c1_title]
#     assert hy400c3c1_idea != None
#     assert hy400c3c1_idea._begin is None
#     assert hy400c3c1_idea._close is None
#     assert hy400c3c1_idea.divisor == 100

#     hy400c3c14y_title = "4yr no leap"
#     hy400c3c14y_road = f"{hy400c3c1_road},{hy400c3c14y_title}"
#     print(f"{hy400c3c14y_road=}")
#     hy400c3c14y_idea = hy400c3c1_idea._kids[hy400c3c14y_title]
#     assert hy400c3c14y_idea != None
#     assert hy400c3c14y_idea._begin == 0
#     assert hy400c3c14y_idea._close == 4
#     assert hy400c3c14y_idea.divisor is None

#     hy400c3c196_title = "96yr range"
#     hy400c3c196_road = f"{hy400c3c1_road},{hy400c3c196_title}"
#     print(f"{hy400c3c196_road=}")
#     hy400c3c196_idea = hy400c3c1_idea._kids[hy400c3c196_title]
#     assert hy400c3c196_idea != None
#     assert hy400c3c196_idea._begin == 4
#     assert hy400c3c196_idea._close == 100
#     assert hy400c3c196_idea.divisor is None

#     hy400c3c196ry_title = "regular 4yr"
#     hy400c3c196ry_road = f"{hy400c3c196_road},{hy400c3c196ry_title}"
#     print(f"{hy400c3c196ry_road=}")
#     hy400c3c196ry_idea = hy400c3c196_idea._kids[hy400c3c196ry_title]
#     assert hy400c3c196ry_idea != None
#     assert hy400c3c196ry_idea._begin is None
#     assert hy400c3c196ry_idea._close is None
#     assert hy400c3c196ry_idea.divisor == 4


# def test_time_hreg_set_CorrectlyCreates400YearCycleYears():
#     h_x_deal = examples.get_deal_base_time_example()
#     c400_count = 6
#     h_x_deal.set_time_hreg_ideas(c400_count=c400_count)

#     hy400_title = "cycle400year_days"
#     hy400_road = f"{root_label()},hreg,{hy400_title}"
#     print(f"{hy400_road=}")
#     hy400_idea = h_x_deal.get_idea_kid(road=hy400_road)
#     assert hy400_idea != None
#     assert hy400_idea._begin is None
#     assert hy400_idea._close is None
#     assert hy400_idea.divisor == 146097


# def test_time_hreg_set_CorrectlyCreatesDayRange():
#     x_deal = examples.get_deal_base_time_example()
#     x_deal.set_time_hreg_ideas(c400_count=6)
#     timetech = x_deal.get_idea_kid(road=f"{root_label()},hreg,day_range")
#     assert timetech != None
#     assert timetech._begin == 0
#     assert timetech._close == 876582

# x_x_deal = dealunit_shop()
# x_deal.get_idea_kid(road={f"{root_label()},hreg,weekday"})

# wed_sufffact_x = sufffactunit_shop(need=wednesday_road)
# work_wk_required = RequiredUnit(base=weekday_road, sufffacts={wed_sufffact.need: wed_sufffact})
# print(f"{type(work_wk_required.base)=}")
# print(f"{work_wk_required.base=}")
# deal_x.edit_idea_attr(road=work_road, required=work_wk_required)
# work_idea = deal_x._kids["work"]
# assert work_idea._requiredunits != None
# print(work_idea._requiredunits)
# assert work_idea._requiredunits[weekday_road] != None
# assert work_idea._requiredunits[weekday_road] == work_wk_required

# x_deal = examples.get_deal_gregorian_years()


def test_get_jajatime_repeating_legible_text_correctlyText():
    # GIVEN
    healer_text = "Noa"
    x_deal = dealunit_shop(_healer=healer_text)
    x_deal.set_time_hreg_ideas(c400_count=7)

    # WHEN / THEN
    print("ReturnsDailyText")
    assert (
        x_deal.get_jajatime_repeating_legible_text(open=480, nigh=480, divisor=1440)
        == "every day at 8am"
    )

    print("ReturnsEvery2DaysText")
    assert (
        x_deal.get_jajatime_repeating_legible_text(open=490, nigh=490, divisor=2880)
        == "every 2nd day at 8:10am"
    )

    print("ReturnsEvery6DaysText")
    assert (
        x_deal.get_jajatime_repeating_legible_text(open=480, nigh=480, divisor=8640)
        == "every 6th day at 8am"
    )

    print("ReturnsWeeklyText")
    assert (
        x_deal.get_jajatime_repeating_legible_text(open=480, nigh=480, divisor=10080)
        == "every Saturday at 8am"
    )

    print("ReturnsEvery2WeeksText")
    assert (
        x_deal.get_jajatime_repeating_legible_text(open=480, nigh=480, divisor=20160)
        == "every 2nd Saturday at 8am"
    )

    print("ReturnsEvery6WeeksText")
    assert (
        x_deal.get_jajatime_repeating_legible_text(open=480, nigh=480, divisor=60480)
        == "every 6th Saturday at 8am"
    )

    print("ReturnsOneTimeEventCorrectlyMorning")
    assert (
        x_deal.get_jajatime_repeating_legible_text(open=1064041020.0, nigh=1064041020.0)
        == "Wed Feb 1st, 2023 at 9am"
    )

    print("ReturnsOneTimeEventCorrectlyEvening")
    assert (
        x_deal.get_jajatime_repeating_legible_text(open=1064041620.0, nigh=1064041620.0)
        == "Wed Feb 1st, 2023 at 7pm"
    )

    print("ReturnsOneTimeEventCorrectlyMidnight")
    assert (
        x_deal.get_jajatime_repeating_legible_text(open=1064041920.0, nigh=1064041920.0)
        == "Thu Feb 2nd, 2023 at 12am"
    )
