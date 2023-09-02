from src.calendar.idea import IdeaKid
from src.calendar.required_idea import (
    acptfactunit_shop,
    sufffactunit_shop,
    RequiredUnit,
    acptfactunit_shop,
)
from src.calendar.calendar import CalendarUnit, get_from_json
from src.calendar.x_func import open_file as x_func_open_file
from src.calendar.examples.get_calendar_examples_dir import get_calendar_examples_dir


def calendar_v001() -> CalendarUnit:
    return get_from_json(
        x_func_open_file(
            dest_dir=get_calendar_examples_dir(), file_name="example_calendar1.json"
        )
    )


def calendar_v001_with_large_agenda() -> CalendarUnit:
    a1 = calendar_v001()
    day_minute_text = "day_minute"
    day_minute_road = f"{a1._owner},{day_minute_text}"
    month_week_text = "month_week"
    month_week_road = f"{a1._owner},{month_week_text}"
    nations_text = "Nation-States"
    nations_road = f"{a1._owner},{nations_text}"
    mood_text = "Moods"
    mood_road = f"{a1._owner},{mood_text}"
    aaron_text = "Aaron Donald sphere"
    aaron_road = f"{a1._owner},{aaron_text}"
    # internet_text = "Internet"
    # internet_road = f"{a1._owner},{internet_text}"
    year_month_text = "year_month"
    year_month_road = f"{a1._owner},{year_month_text}"
    season_text = "Seasons"
    season_road = f"{a1._owner},{season_text}"
    ced_week_text = "ced_week"
    ced_week_road = f"{a1._owner},{ced_week_text}"
    # water_text = "WaterBeing"
    # water_road = f"{a1._owner},{water_text}"
    weekdays_text = "weekdays"
    weekdays_road = f"{a1._owner},{weekdays_text}"
    # movie_text = "No Movie playing"
    # movie_road = f"{a1._owner},{movie_text}"

    a1.set_acptfact(base=aaron_road, pick=aaron_road)
    a1.set_acptfact(base=ced_week_road, pick=ced_week_road, open=0, nigh=53)
    a1.set_acptfact(base=day_minute_road, pick=day_minute_road, open=0, nigh=1399)
    # a1.set_acptfact(base=internet, pick=internet)
    a1.set_acptfact(base=month_week_road, pick=month_week_road, open=0, nigh=5)
    a1.set_acptfact(base=mood_road, pick=mood_road)
    # a1.set_acptfact(base=movie, pick=movie)
    a1.set_acptfact(base=nations_road, pick=nations_road)
    a1.set_acptfact(base=season_road, pick=season_road)
    a1.set_acptfact(base=year_month_road, pick=year_month_road, open=0, nigh=12)
    # a1.set_acptfact(base=water, pick=water)
    a1.set_acptfact(base=weekdays_road, pick=weekdays_road)

    return a1


def calendar_v002() -> CalendarUnit:
    return get_from_json(
        x_func_open_file(
            dest_dir=get_calendar_examples_dir(), file_name="example_calendar2.json"
        )
    )


def get_calendar_with_4_levels() -> CalendarUnit:
    src_road = "src"
    calendar_x = CalendarUnit(_owner=src_road, _weight=10)

    work = "work"
    idea_kid_work = IdeaKid(_weight=30, _desc=work, promise=True)
    calendar_x.add_idea(idea_kid=idea_kid_work, walk=src_road)

    cat = "feed cat"
    idea_kid_feedcat = IdeaKid(_weight=30, _desc=cat, promise=True)
    calendar_x.add_idea(idea_kid=idea_kid_feedcat, walk=src_road)

    week_text = "weekdays"
    week_road = f"{src_road},{week_text}"
    idea_kid_weekdays = IdeaKid(_weight=40, _desc=week_text)
    calendar_x.add_idea(idea_kid=idea_kid_weekdays, walk=src_road)

    sun_text = "Sunday"
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"

    idea_grandkidU = IdeaKid(_weight=20, _desc=sun_text)
    idea_grandkidM = IdeaKid(_weight=20, _desc=mon_text)
    idea_grandkidT = IdeaKid(_weight=20, _desc=tue_text)
    idea_grandkidW = IdeaKid(_weight=20, _desc=wed_text)
    idea_grandkidR = IdeaKid(_weight=30, _desc=thu_text)
    idea_grandkidF = IdeaKid(_weight=40, _desc=fri_text)
    idea_grandkidA = IdeaKid(_weight=50, _desc=sat_text)

    calendar_x.add_idea(idea_grandkidU, week_road)
    calendar_x.add_idea(idea_grandkidM, week_road)
    calendar_x.add_idea(idea_grandkidT, week_road)
    calendar_x.add_idea(idea_grandkidW, week_road)
    calendar_x.add_idea(idea_grandkidR, week_road)
    calendar_x.add_idea(idea_grandkidF, week_road)
    calendar_x.add_idea(idea_grandkidA, week_road)

    states_text = "nation-state"
    states_road = f"{src_road},{states_text}"
    idea_kid_states = IdeaKid(_weight=30, _desc=states_text)
    calendar_x.add_idea(idea_kid=idea_kid_states, walk=f"{src_road}")

    usa_text = "USA"
    usa_road = f"{states_road},{usa_text}"
    france_text = "France"
    brazil_text = "Brazil"
    idea_grandkid_usa = IdeaKid(_weight=50, _desc=usa_text)
    idea_grandkid_france = IdeaKid(_weight=50, _desc=france_text)
    idea_grandkid_brazil = IdeaKid(_weight=50, _desc=brazil_text)
    calendar_x.add_idea(idea_grandkid_france, states_road)
    calendar_x.add_idea(idea_grandkid_brazil, states_road)
    calendar_x.add_idea(idea_grandkid_usa, states_road)

    texas_text = "Texas"
    oregon_text = "Oregon"
    idea_grandgrandkid_usa_texas = IdeaKid(_weight=50, _desc=texas_text)
    idea_grandgrandkid_usa_oregon = IdeaKid(_weight=50, _desc=oregon_text)
    calendar_x.add_idea(idea_grandgrandkid_usa_texas, usa_road)
    calendar_x.add_idea(idea_grandgrandkid_usa_oregon, usa_road)
    return calendar_x


def get_calendar_with_4_levels_and_2requireds() -> CalendarUnit:
    calendar_x = get_calendar_with_4_levels()
    week_road = f"{calendar_x._owner},weekdays"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"
    wed_sufffact = sufffactunit_shop(need=wed_road)

    nation_road = f"{calendar_x._owner},nation-state"
    usa_road = f"{nation_road},USA"
    usa_sufffact_x = sufffactunit_shop(need=usa_road)
    work_wk_required = RequiredUnit(
        base=week_road, sufffacts={wed_sufffact.need: wed_sufffact}
    )
    nation_required = RequiredUnit(
        base=nation_road, sufffacts={usa_sufffact_x.need: usa_sufffact_x}
    )
    work_text = "work"
    work_road = f"{calendar_x._owner},{work_text}"
    calendar_x.edit_idea_attr(road=work_road, required=work_wk_required)
    calendar_x.edit_idea_attr(road=work_road, required=nation_required)
    return calendar_x


def get_calendar_with_4_levels_and_2requireds_2acptfacts() -> CalendarUnit:
    calendar_x = get_calendar_with_4_levels_and_2requireds()
    wednesday = f"{calendar_x._owner},weekdays,Wednesday"
    weekday = f"{calendar_x._owner},weekdays"
    states = f"{calendar_x._owner},nation-state"
    usa_road = f"{calendar_x._owner},nation-state,USA"
    calendar_x.set_acptfact(base=weekday, pick=wednesday)
    calendar_x.set_acptfact(base=states, pick=usa_road)
    return calendar_x


def get_calendar_with7amCleanTableRequired() -> CalendarUnit:
    calendar_x = get_calendar_with_4_levels_and_2requireds_2acptfacts()
    src = calendar_x._owner
    timetech = "timetech"
    day_24hr = "24hr day"
    am = "am"
    pm = "pm"
    idea_timeline = IdeaKid(_weight=40, _desc=timetech)
    idea_24hr_day = IdeaKid(_weight=40, _desc=day_24hr, _begin=0.0, _close=24.0)
    idea_am = IdeaKid(_weight=50, _desc=am, _begin=0, _close=12)
    idea_01 = IdeaKid(_weight=50, _desc="1", _begin=1, _close=2)
    idea_02 = IdeaKid(_weight=50, _desc="2", _begin=2, _close=3)
    idea_03 = IdeaKid(_weight=50, _desc="3", _begin=3, _close=4)
    idea_pm = IdeaKid(_weight=50, _desc=pm, _begin=12, _close=24)

    time_road = f"{src},{timetech}"
    day24hr_road = f"{time_road},{day_24hr}"
    am_road = f"{day_24hr},{am}"
    calendar_x.add_idea(idea_timeline, src)
    calendar_x.add_idea(idea_24hr_day, time_road)
    calendar_x.add_idea(idea_am, day24hr_road)
    calendar_x.add_idea(idea_pm, day24hr_road)
    calendar_x.add_idea(idea_01, am_road)  # idea_am
    calendar_x.add_idea(idea_02, am_road)  # idea_am
    calendar_x.add_idea(idea_03, am_road)  # idea_am

    housework = "housework"
    house_road = f"{src},{housework}"
    clean_table = "clean table"
    clean_road = f"{house_road},{clean_table}"
    remove_dish = "remove dishs"
    get_soap = "get soap"
    get_soap_road = f"{clean_road},{get_soap}"
    remove_dish = "remove dishs"
    idea_housework = IdeaKid(_weight=40, _desc=housework)
    idea_cleantable = IdeaKid(_weight=40, _desc=clean_table, promise=True)
    idea_tabledishs = IdeaKid(_weight=40, _desc=remove_dish, promise=True)
    idea_tablesoap = IdeaKid(_weight=40, _desc=get_soap, promise=True)
    idea_grabsoap = IdeaKid(_weight=40, _desc="grab soap", promise=True)

    calendar_x.add_idea(idea_kid=idea_housework, walk=src)
    calendar_x.add_idea(idea_kid=idea_cleantable, walk=house_road)
    calendar_x.add_idea(idea_kid=idea_tabledishs, walk=clean_road)
    calendar_x.add_idea(idea_kid=idea_tablesoap, walk=clean_road)
    calendar_x.add_idea(idea_kid=idea_grabsoap, walk=get_soap_road)

    clean_table_7am_base = day24hr_road
    clean_table_7am_sufffact_road = day24hr_road
    clean_table_7am_sufffact_open = 7.0
    clean_table_7am_sufffact_nigh = 7.0
    clean_table_7am_sufffact_x = sufffactunit_shop(
        need=clean_table_7am_sufffact_road,
        open=clean_table_7am_sufffact_open,
        nigh=clean_table_7am_sufffact_nigh,
    )
    clean_table_7am_required = RequiredUnit(
        base=clean_table_7am_base,
        sufffacts={clean_table_7am_sufffact_x.need: clean_table_7am_sufffact_x},
    )
    calendar_x.edit_idea_attr(
        road=f"{calendar_x._owner},housework,clean table",
        required=clean_table_7am_required,
    )
    calendar_x.edit_idea_attr(
        road=f"{calendar_x._owner},work", required=clean_table_7am_required
    )
    return calendar_x


def get_calendar_1Task_1CE0MinutesRequired_1AcptFact() -> CalendarUnit:
    lw_desc = "test45"
    calendar_x = CalendarUnit(_owner=lw_desc, _weight=10)
    ced_min_desc = "CE0_minutes"
    ced_minutes = IdeaKid(_desc=ced_min_desc)
    ced_road = f"{lw_desc},{ced_min_desc}"
    calendar_x.add_idea(idea_kid=ced_minutes, walk=lw_desc)
    mail_desc = "obtain mail"
    mail_task = IdeaKid(_desc=mail_desc, promise=True)
    calendar_x.add_idea(idea_kid=mail_task, walk=lw_desc)

    sufffact_x = sufffactunit_shop(need=ced_road, open=80, nigh=90)
    x_task_required = RequiredUnit(
        base=sufffact_x.need, sufffacts={sufffact_x.need: sufffact_x}
    )
    mail_road = f"{lw_desc},{mail_desc}"
    calendar_x.edit_idea_attr(road=mail_road, required=x_task_required)

    x_acptfact = acptfactunit_shop(base=ced_road, pick=ced_road, open=85, nigh=95)
    # print(
    #     f"1Task_1CE0MinutesRequired_1AcptFact 2. {len(calendar_x._idearoot._kids)=} {x_acptfact.base=}"
    # )
    calendar_x.set_acptfact(
        base=x_acptfact.base,
        pick=x_acptfact.pick,
        open=x_acptfact.open,
        nigh=x_acptfact.nigh,
    )
    # print(f"1Task_1CE0MinutesRequired_1AcptFact 3. {len(calendar_x._idearoot._kids)=}")

    return calendar_x


def get_calendar_x1_3levels_1required_1acptfacts() -> CalendarUnit:
    prom = "prom"
    x_calendar = CalendarUnit(_owner=prom, _weight=10)
    idea_kid_shave = IdeaKid(_weight=30, _desc="shave", promise=True)
    x_calendar.add_idea(idea_kid=idea_kid_shave, walk=prom)
    weekdays = "weekdays"
    idea_kid_weekdays = IdeaKid(_weight=40, _desc=weekdays)
    x_calendar.add_idea(idea_kid=idea_kid_weekdays, walk=prom)

    idea_grandkidU = IdeaKid(_weight=20, _desc="Sunday")
    idea_grandkidM = IdeaKid(_weight=20, _desc="Monday")
    week_road = f"{prom},{weekdays}"
    x_calendar.add_idea(idea_kid=idea_grandkidU, walk=week_road)
    x_calendar.add_idea(idea_kid=idea_grandkidM, walk=week_road)

    shave_base = "prom,weekdays"
    shave_sufffact_road = "prom,weekdays,Monday"
    shave_sufffact_x = sufffactunit_shop(need=shave_sufffact_road)
    shave_required = RequiredUnit(
        base=shave_base,
        sufffacts={shave_sufffact_x.need: shave_sufffact_x},
    )

    x_calendar.edit_idea_attr(road="prom,shave", required=shave_required)
    x_calendar.set_acptfact(base="prom,weekdays", pick="prom,weekdays,Sunday")
    acptfactunit_x = acptfactunit_shop(
        base="prom,weekdays", pick="prom,weekdays,Sunday,church"
    )
    x_calendar.edit_idea_attr(road="prom,shave", acptfactunit=acptfactunit_x)
    return x_calendar


def get_calendar_base_time_example() -> CalendarUnit:
    g_src = "src"
    g_lw = CalendarUnit(_owner=g_src)
    plant = "plant"
    x_idea = IdeaKid(_desc=plant)
    g_lw.add_idea(x_idea, walk=g_src)

    return g_lw


def get_calendar_irrational_example() -> CalendarUnit:
    # this calendar has no conclusive agenda because 2 promise ideas are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active_status == True, egg._active_status is set to False
    # Step 1: if egg._active_status == False, chicken._active_status is set to False
    # Step 2: if chicken._active_status == False, egg._active_status is set to True
    # Step 3: if egg._active_status == True, chicken._active_status is set to True
    # Step 4: back to step 0.
    # after calendar_x.set_calendar_metrics these should be true:
    # 1. calendar_x._irrational == True
    # 2. calendar_x._tree_traverse_count = calendar_x._max_tree_traverse

    src_road = "src"
    calendar_x = CalendarUnit(_owner=src_road, _weight=10)
    calendar_x.set_max_tree_traverse(3)

    egg_text = "egg first"
    egg_road = f"{src_road},{egg_text}"
    calendar_x.add_idea(idea_kid=IdeaKid(_desc=egg_text), walk=src_road)

    chicken_text = "chicken first"
    chicken_road = f"{src_road},{chicken_text}"
    calendar_x.add_idea(idea_kid=IdeaKid(_desc=chicken_text), walk=src_road)

    # set egg promise is True when chicken first is False
    calendar_x.edit_idea_attr(
        road=egg_road,
        promise=True,
        required_base=chicken_road,
        required_suff_idea_active_status=True,
    )

    # set chick promise is True when egg first is False
    calendar_x.edit_idea_attr(
        road=chicken_road,
        promise=True,
        required_base=egg_road,
        required_suff_idea_active_status=False,
    )

    return calendar_x
