from src.agenda.agenda import AgendaUnit, agendaunit_shop
from datetime import datetime
from random import randint


def test_time_get_time_min_from_dt_ReturnsCorrectObj():
    kia_agenda = agendaunit_shop(_owner_id="Kia")
    kia_agenda.set_time_hreg_facts(c400_count=6)
    assert kia_agenda.get_time_min_from_dt(dt=datetime(2000, 1, 1, 0, 0))
    assert kia_agenda.get_time_min_from_dt(dt=datetime(1, 1, 1, 0, 0)) == 527040
    assert kia_agenda.get_time_min_from_dt(dt=datetime(1, 1, 2, 0, 0)) == 527040 + 1440
    assert kia_agenda.get_time_min_from_dt(dt=datetime(400, 1, 1, 0, 0)) == 210379680
    assert kia_agenda.get_time_min_from_dt(dt=datetime(800, 1, 1, 0, 0)) == 420759360
    assert kia_agenda.get_time_min_from_dt(dt=datetime(1200, 1, 1, 0, 0)) == 631139040


def test_get_time_400Yearsegment_from_min_ReturnsCorrectObj():
    kia_agenda = agendaunit_shop("Kia")
    kia_agenda.set_time_hreg_facts(c400_count=6)
    assert kia_agenda.get_time_c400_from_min(min=0)[0] == 0
    assert kia_agenda.get_time_c400_from_min(min=210379680)[0] == 1
    assert kia_agenda.get_time_c400_from_min(min=210379681)[0] == 1
    assert kia_agenda.get_time_c400_from_min(min=841518720)[0] == 4


def test_get_time_c400year_from_min_ReturnsCorrectObj():
    kia_agenda = agendaunit_shop("Kia")
    kia_agenda.set_time_hreg_facts(c400_count=6)
    assert kia_agenda.get_time_c400yr_from_min(min=0)[0] == 0
    assert kia_agenda.get_time_c400yr_from_min(min=1)[0] == 0
    assert kia_agenda.get_time_c400yr_from_min(min=1)[2] == 1
    assert kia_agenda.get_time_c400yr_from_min(min=210379680)[0] == 0
    assert kia_agenda.get_time_c400yr_from_min(min=210379680)[0] == 0
    assert kia_agenda.get_time_c400yr_from_min(min=210379681)[0] == 0
    assert kia_agenda.get_time_c400yr_from_min(min=841518720)[0] == 0
    assert kia_agenda.get_time_c400yr_from_min(min=576000)[0] == 1
    assert kia_agenda.get_time_c400yr_from_min(min=4608000)[0] == 8
    assert kia_agenda.get_time_c400yr_from_min(min=157785120)[0] == 300


def _check_time_conversion_with_random_inputs(x_agenda: AgendaUnit):
    py_dt = datetime(
        year=randint(1, 2800),
        month=randint(1, 12),
        day=randint(1, 28),
        hour=randint(0, 23),
        minute=randint(0, 59),
    )
    print(f"Attempt {py_dt=}")
    assert py_dt == x_agenda.get_time_dt_from_min(x_agenda.get_time_min_from_dt(py_dt))


def test_get_time_dt_from_min_ReturnsCorrectObj():
    kia_agenda = agendaunit_shop(_owner_id="Kia")
    kia_agenda.set_time_hreg_facts(c400_count=6)
    assert kia_agenda.get_time_dt_from_min(min=5000000)
    # assert kia_agenda.get_time_dt_from_min(
    #     min=kia_agenda.get_time_min_from_dt(dt=datetime(2000, 1, 1, 0, 0))
    # ) == datetime(2000, 1, 1, 0, 0)
    assert kia_agenda.get_time_dt_from_min(min=420759360) == datetime(800, 1, 1, 0, 0)
    assert kia_agenda.get_time_dt_from_min(min=631139040) == datetime(1200, 1, 1, 0, 0)
    assert kia_agenda.get_time_dt_from_min(min=631751040) == datetime(1201, 3, 1, 0, 0)
    assert kia_agenda.get_time_dt_from_min(min=631751060) == datetime(1201, 3, 1, 0, 20)

    x_minutes = 1063903680
    assert kia_agenda.get_time_dt_from_min(min=x_minutes) == datetime(
        2022, 10, 29, 0, 0
    )
    x_next_day = x_minutes + 1440
    assert kia_agenda.get_time_dt_from_min(min=x_next_day) == datetime(
        2022, 10, 30, 0, 0
    )

    _check_time_conversion_with_random_inputs(kia_agenda)
    _check_time_conversion_with_random_inputs(kia_agenda)
    _check_time_conversion_with_random_inputs(kia_agenda)

    # for year, month, day, hr, min in .product(
    #     range(479, 480), range(1, 3), range(20, 28), range(12, 14), range(1430, 1440)
    # ):
    #     # for day in range(1, 32):
    #     # # print(f"assert for {year=} {month=} {day=}")
    #     # with contextlib.suppress(Exception):
    #     print(f"Attempt get_time_from_dt {year=} {month=} {day=} {hr=} {min=}")
    #     py_dt = datetime(year, month, day, 0, 0)
    #     jaja_min = x_agenda.get_time_min_from_dt(dt=py_dt)
    #     # print(f"assert for {year=} {month=} {day=} {jaja_min}")

    #     jaja_dt = x_agenda.get_time_dt_from_min(min=jaja_min)
    #     print(
    #         f"assert attempted for {year=} {month=} {day} \t {jaja_min} Jaja too large: {str(jaja_dt-py_dt)} ({py_dt=})"
    #     )
    #     assert py_dt == jaja_dt

    # if dt_exist:

    # for year in range(480, 481):
    #     for month in range(1, 12):
    #         for day in range(1, 30):
    #             assert x_agenda.get_time_dt_from_min(
    #                 min=x_agenda.get_time_min_from_dt(dt=datetime(year, month, day, 0, 0))
    #             ) == datetime(year, month, day, 0, 0)


def test_get_time_():
    # GIVEN
    kia_agenda = agendaunit_shop(_owner_id="Kia")
    kia_agenda.set_time_hreg_facts(c400_count=6)

    kia_agenda.calc_agenda_metrics()
    # for fact_x in fact_list:
    #     if fact_x._label in ["min2010", "years"]:
    #         print(
    #             f"{fact_x._parent_road=} \t{fact_x._label=} {fact_x._begin=} {fact_x._close=} {fact_x._addin=}"
    #         )

    # WHEN
    kia_agenda.set_time_beliefs(
        open=datetime(2000, 1, 1, 0, 0), nigh=datetime(2003, 11, 15, 4, 0)
    )

    # THEN
    time_text = "time"
    time_road = kia_agenda.make_l1_road(time_text)
    jaja_text = "jajatime"
    jaja_road = kia_agenda.make_road(time_road, jaja_text)
    assert kia_agenda._factroot._beliefunits[jaja_road]
    assert kia_agenda._factroot._beliefunits[jaja_road].open == 1051898400  # - 1440
    assert kia_agenda._factroot._beliefunits[jaja_road].nigh == 1053934800  # - 1440


# def test_time_hreg_set_exists():
#     x_agenda = agendaunit_shop(_owner_id=bob_text)
#     x_agenda.set_time_hreg_facts(c400_count=6)
#     fact_x = x_agenda.get_fact_obj(x_agenda.make_l1_road("hreg")
#     assert fact_x != None
#     assert x_agenda.get_kid("hreg"]
#     for kid in x_agenda.get_kid("hreg"]._kids.values():
#         print(f"hreg kid= {kid._label=}")

#     assert len(x_agenda.get_kid("hreg"]._kids) > 0


# def test_time_hreg_set_creates_fact():
#     x_agenda = examples.get_agenda_base_time_example()

#     hreg_label = "hreg"
#     with pytest.raises(KeyError) as excinfo:
#         x_agenda.get_kid(hreg_label]
#     assert str(excinfo.value) == f"'{hreg_label}'"
#     print(f"added {hreg_label}")
#     x_agenda.set_time_hreg_facts(c400_count=6)
#     hreg_fact = x_agenda.get_kid(hreg_label]
#     assert hreg_fact != None
#     assert hreg_fact._begin == 0
#     assert hreg_fact._close == 1262278080


# def test_time_hreg_set_CorrectlyCreatesWeekdayFact():
#     x_agenda = examples.get_agenda_base_time_example()
#     x_agenda.set_time_hreg_facts(c400_count=6)
#     weekday_label = "weekday"
#     weekday = x_agenda.get_fact_obj(x_agenda.make_l1_road("hreg,{weekday_label}")
#     assert weekday != None
#     assert weekday._begin == 0
#     assert weekday._close == 7
#     assert weekday.get_kid("Sunday"] != None
#     assert weekday.get_kid("Monday"] != None
#     assert weekday.get_kid("Tuesday"] != None
#     assert weekday.get_kid("Wednesday"] != None
#     assert weekday.get_kid("Thursday"] != None
#     assert weekday.get_kid("Friday"] != None
#     assert weekday.get_kid("Saturday"] != None


# def test_time_hreg_set_CorrectlyCreates400YearsegmentCount():
#     x_agenda = examples.get_agenda_base_time_example()
#     c400_count = 6
#     x_agenda.set_time_hreg_facts(c400_count=c400_count)

#     timetech_label = "400 year segment"
#     timetech_road = x_agenda.make_l1_road("hreg,{timetech_label}"
#     print(f"{timetech_road=}")
#     timetech = x_agenda.get_fact_obj(timetech_road)
#     assert timetech != None
#     assert timetech._begin == 0
#     assert timetech._close == c400_count


# def test_time_hreg_set_CorrectlyCreates400YearsegmentYears():
#     h_x_agenda = examples.get_agenda_base_time_example()
#     c400_count = 6
#     h_x_agenda.set_time_hreg_facts(c400_count=c400_count)

#     hy400_label = "segment400year_years"
#     hy400_road = x_agenda.make_l1_road("hreg,{hy400_label}"
#     print(f"{hy400_road=}")
#     hy400_fact = h_x_agenda.get_fact_obj(hy400_road)
#     assert hy400_fact != None
#     assert hy400_fact._begin is None
#     assert hy400_fact._close is None
#     assert hy400_fact.divisor == 400

#     hy400c1_label = "100yr regular"
#     hy400c1_road = create_road(hy400_road,hy400c1_label)
#     print(f"{hy400c1_road=}")
#     hy400c1_fact = hy400_fact.get_kid(hy400c1_label]
#     assert hy400c1_fact != None
#     assert hy400c1_fact._begin == 0
#     assert hy400c1_fact._close == 100
#     assert hy400c1_fact.divisor is None

#     hy400c14y_label = "regular 4yr"
#     hy400c14y_road = create_road(hy400c1_road,hy400c14y_label}"
#     print(f"{hy400c14y_road=}")
#     hy400c14y_fact = hy400c1_fact.get_kid(hy400c14y_label]
#     assert hy400c14y_fact != None
#     assert hy400c14y_fact._begin is None
#     assert hy400c14y_fact._close is None
#     assert hy400c14y_fact.divisor == 4

#     hy400c3_label = "300yr range"
#     hy400c3_road = create_road(hy400_road,hy400c3_label}"
#     print(f"{hy400c3_road=}")
#     hy400c3_fact = hy400_fact.get_kid(hy400c3_label]
#     assert hy400c3_fact != None
#     assert hy400c3_fact._begin == 100
#     assert hy400c3_fact._close == 400
#     assert hy400c3_fact.divisor is None

#     hy400c3c1_label = "100yr no century leap"
#     hy400c3c1_road = create_road(hy400c3_road,hy400c3c1_label}"
#     print(f"{hy400c3c1_road=}")
#     hy400c3c1_fact = hy400c3_fact.get_kid(hy400c3c1_label]
#     assert hy400c3c1_fact != None
#     assert hy400c3c1_fact._begin is None
#     assert hy400c3c1_fact._close is None
#     assert hy400c3c1_fact.divisor == 100

#     hy400c3c14y_label = "4yr no leap"
#     hy400c3c14y_road = create_road(hy400c3c1_road,hy400c3c14y_label}"
#     print(f"{hy400c3c14y_road=}")
#     hy400c3c14y_fact = hy400c3c1_fact.get_kid(hy400c3c14y_label]
#     assert hy400c3c14y_fact != None
#     assert hy400c3c14y_fact._begin == 0
#     assert hy400c3c14y_fact._close == 4
#     assert hy400c3c14y_fact.divisor is None

#     hy400c3c196_label = "96yr range"
#     hy400c3c196_road = create_road(hy400c3c1_road,hy400c3c196_label}"
#     print(f"{hy400c3c196_road=}")
#     hy400c3c196_fact = hy400c3c1_fact.get_kid(hy400c3c196_label]
#     assert hy400c3c196_fact != None
#     assert hy400c3c196_fact._begin == 4
#     assert hy400c3c196_fact._close == 100
#     assert hy400c3c196_fact.divisor is None

#     hy400c3c196ry_label = "regular 4yr"
#     hy400c3c196ry_road = create_road(hy400c3c196_road,hy400c3c196ry_label}"
#     print(f"{hy400c3c196ry_road=}")
#     hy400c3c196ry_fact = hy400c3c196_fact.get_kid(hy400c3c196ry_label]
#     assert hy400c3c196ry_fact != None
#     assert hy400c3c196ry_fact._begin is None
#     assert hy400c3c196ry_fact._close is None
#     assert hy400c3c196ry_fact.divisor == 4


# def test_time_hreg_set_CorrectlyCreates400YearsegmentYears():
#     h_x_agenda = examples.get_agenda_base_time_example()
#     c400_count = 6
#     h_x_agenda.set_time_hreg_facts(c400_count=c400_count)

#     hy400_label = "segment400year_days"
#     hy400_road = x_agenda.make_l1_road("hreg,{hy400_label}"
#     print(f"{hy400_road=}")
#     hy400_fact = h_x_agenda.get_fact_obj(hy400_road)
#     assert hy400_fact != None
#     assert hy400_fact._begin is None
#     assert hy400_fact._close is None
#     assert hy400_fact.divisor == 146097


# def test_time_hreg_set_CorrectlyCreatesDayRange():
#     x_agenda = examples.get_agenda_base_time_example()
#     x_agenda.set_time_hreg_facts(c400_count=6)
#     timetech = x_agenda.get_fact_obj(x_agenda.make_l1_road("hreg,day_range")
#     assert timetech != None
#     assert timetech._begin == 0
#     assert timetech._close == 876582

# x_x_agenda = agendaunit_shop()
# x_agenda.get_fact_obj({x_agenda.make_l1_road("hreg,weekday"})

# wed_premise_x = premiseunit_shop(need=wednesday_road)
# woork_wk_reason = reasonunit_shop(weekday_road, premises={wed_premise.need: wed_premise})
# print(f"{type(woork_wk_reason.base)=}")
# print(f"{woork_wk_reason.base=}")
# agenda_x.edit_fact_attr(road=woork_road, reason=woork_wk_reason)
# woork_fact = agenda_x.get_kid("woork"]
# assert woork_fact._reasonunits != None
# print(woork_fact._reasonunits)
# assert woork_fact._reasonunits[weekday_road] != None
# assert woork_fact._reasonunits[weekday_road] == woork_wk_reason

# x_agenda = examples.get_agenda_gregorian_years()


def test_get_jajatime_repeating_legible_text_correctlyText():
    # GIVEN
    noa_agenda = agendaunit_shop(_owner_id="Noa")
    noa_agenda.set_time_hreg_facts(c400_count=7)

    # WHEN / THEN
    every_day_8am_text = noa_agenda.get_jajatime_repeating_legible_text(
        open=480, nigh=480, divisor=1440
    )
    print(f"ReturnsDailyText {every_day_8am_text=}")
    assert every_day_8am_text == "every day at 8am"

    every_2nd_day_8_10am_text = noa_agenda.get_jajatime_repeating_legible_text(
        open=490, nigh=490, divisor=2880
    )
    print(f"ReturnsEvery2DaysText: {every_2nd_day_8_10am_text=}")
    assert every_2nd_day_8_10am_text == "every 2nd day at 8:10am"

    ReturnsEvery6DaysText = noa_agenda.get_jajatime_repeating_legible_text(
        open=480, nigh=480, divisor=8640
    )
    print(f"ReturnsEvery6DaysText: {ReturnsEvery6DaysText=}")
    assert ReturnsEvery6DaysText == "every 6th day at 8am"

    every_saturday_8am_text = noa_agenda.get_jajatime_repeating_legible_text(
        open=480, nigh=480, divisor=10080
    )
    print(f"ReturnsWeeklyText: {every_saturday_8am_text=}")
    assert every_saturday_8am_text == "every Saturday at 8am"

    sat_2nd_8am_text = noa_agenda.get_jajatime_repeating_legible_text(
        open=480, nigh=480, divisor=20160
    )
    print(f"ReturnsEvery2WeeksText: {sat_2nd_8am_text=}")
    assert sat_2nd_8am_text == "every 2nd Saturday at 8am"

    sat_6th_8am_text = noa_agenda.get_jajatime_repeating_legible_text(
        open=480, nigh=480, divisor=60480
    )
    print(f"ReturnsEvery6WeeksText: {sat_6th_8am_text=}")
    assert sat_6th_8am_text == "every 6th Saturday at 8am"

    feb_1st_9am_text = noa_agenda.get_jajatime_repeating_legible_text(
        open=1064041020.0, nigh=1064041020.0
    )
    print(f"ReturnsOneTimeEventCorrectlyMorning: {feb_1st_9am_text=}")
    assert feb_1st_9am_text == "Wed Feb 1st, 2023 at 9am"

    feb_1st_7pm_text = noa_agenda.get_jajatime_repeating_legible_text(
        open=1064041620.0, nigh=1064041620.0
    )
    print(f"ReturnsOneTimeEventCorrectlyMorning: {feb_1st_9am_text=}")
    assert feb_1st_7pm_text == "Wed Feb 1st, 2023 at 7pm"

    feb_2nd_12am_text = noa_agenda.get_jajatime_repeating_legible_text(
        open=1064041920.0, nigh=1064041920.0
    )
    print(f"ReturnsOneTimeEventCorrectlyMidnight {feb_2nd_12am_text=}")
    assert feb_2nd_12am_text == "Thu Feb 2nd, 2023 at 12am"
