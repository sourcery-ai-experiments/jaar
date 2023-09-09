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
from src.calendar.road import get_global_root_label as root_label


def calendar_v001() -> CalendarUnit:
    return get_from_json(
        x_func_open_file(
            dest_dir=get_calendar_examples_dir(), file_name="example_calendar1.json"
        )
    )


def calendar_v001_with_large_agenda() -> CalendarUnit:
    a1 = calendar_v001()
    day_minute_text = "day_minute"
    day_minute_road = f"{root_label()},{day_minute_text}"
    month_week_text = "month_week"
    month_week_road = f"{root_label()},{month_week_text}"
    nations_text = "Nation-States"
    nations_road = f"{root_label()},{nations_text}"
    mood_text = "Moods"
    mood_road = f"{root_label()},{mood_text}"
    aaron_text = "Aaron Donald sphere"
    aaron_road = f"{root_label()},{aaron_text}"
    # internet_text = "Internet"
    # internet_road = f"{root_label()},{internet_text}"
    year_month_text = "year_month"
    year_month_road = f"{root_label()},{year_month_text}"
    season_text = "Seasons"
    season_road = f"{root_label()},{season_text}"
    ced_week_text = "ced_week"
    ced_week_road = f"{root_label()},{ced_week_text}"
    # water_text = "WaterBeing"
    # water_road = f"{root_label()},{water_text}"
    weekdays_text = "weekdays"
    weekdays_road = f"{root_label()},{weekdays_text}"
    # movie_text = "No Movie playing"
    # movie_road = f"{root_label()},{movie_text}"

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
    owner_text = "Noa"
    calendar_x = CalendarUnit(_owner=owner_text, _weight=10)

    work = "work"
    idea_kid_work = IdeaKid(_weight=30, _label=work, promise=True)
    calendar_x.add_idea(idea_kid=idea_kid_work, walk=root_label())

    cat = "feed cat"
    idea_kid_feedcat = IdeaKid(_weight=30, _label=cat, promise=True)
    calendar_x.add_idea(idea_kid=idea_kid_feedcat, walk=root_label())

    week_text = "weekdays"
    week_road = f"{root_label()},{week_text}"
    idea_kid_weekdays = IdeaKid(_weight=40, _label=week_text)
    calendar_x.add_idea(idea_kid=idea_kid_weekdays, walk=root_label())

    sun_text = "Sunday"
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"

    idea_grandkidU = IdeaKid(_weight=20, _label=sun_text)
    idea_grandkidM = IdeaKid(_weight=20, _label=mon_text)
    idea_grandkidT = IdeaKid(_weight=20, _label=tue_text)
    idea_grandkidW = IdeaKid(_weight=20, _label=wed_text)
    idea_grandkidR = IdeaKid(_weight=30, _label=thu_text)
    idea_grandkidF = IdeaKid(_weight=40, _label=fri_text)
    idea_grandkidA = IdeaKid(_weight=50, _label=sat_text)

    calendar_x.add_idea(idea_grandkidU, week_road)
    calendar_x.add_idea(idea_grandkidM, week_road)
    calendar_x.add_idea(idea_grandkidT, week_road)
    calendar_x.add_idea(idea_grandkidW, week_road)
    calendar_x.add_idea(idea_grandkidR, week_road)
    calendar_x.add_idea(idea_grandkidF, week_road)
    calendar_x.add_idea(idea_grandkidA, week_road)

    states_text = "nation-state"
    states_road = f"{root_label()},{states_text}"
    idea_kid_states = IdeaKid(_weight=30, _label=states_text)
    calendar_x.add_idea(idea_kid=idea_kid_states, walk=f"{root_label()}")

    usa_text = "USA"
    usa_road = f"{states_road},{usa_text}"
    france_text = "France"
    brazil_text = "Brazil"
    idea_grandkid_usa = IdeaKid(_weight=50, _label=usa_text)
    idea_grandkid_france = IdeaKid(_weight=50, _label=france_text)
    idea_grandkid_brazil = IdeaKid(_weight=50, _label=brazil_text)
    calendar_x.add_idea(idea_grandkid_france, states_road)
    calendar_x.add_idea(idea_grandkid_brazil, states_road)
    calendar_x.add_idea(idea_grandkid_usa, states_road)

    texas_text = "Texas"
    oregon_text = "Oregon"
    idea_grandgrandkid_usa_texas = IdeaKid(_weight=50, _label=texas_text)
    idea_grandgrandkid_usa_oregon = IdeaKid(_weight=50, _label=oregon_text)
    calendar_x.add_idea(idea_grandgrandkid_usa_texas, usa_road)
    calendar_x.add_idea(idea_grandgrandkid_usa_oregon, usa_road)
    return calendar_x


def get_calendar_with_4_levels_and_2requireds() -> CalendarUnit:
    calendar_x = get_calendar_with_4_levels()
    week_text = "weekdays"
    week_road = f"{root_label()},{week_text}"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"
    week_required = RequiredUnit(base=week_road, sufffacts={})
    week_required.set_sufffact(wed_road)

    nation_text = "nation-state"
    nation_road = f"{root_label()},{nation_text}"
    usa_text = "USA"
    usa_road = f"{nation_road},{usa_text}"
    nation_required = RequiredUnit(base=nation_road, sufffacts={})
    nation_required.set_sufffact(usa_road)

    work_text = "work"
    work_road = f"{root_label()},{work_text}"
    calendar_x.edit_idea_attr(road=work_road, required=week_required)
    calendar_x.edit_idea_attr(road=work_road, required=nation_required)
    return calendar_x


def get_calendar_with_4_levels_and_2requireds_2acptfacts() -> CalendarUnit:
    calendar_x = get_calendar_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = f"{root_label()},{week_text}"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"
    states_text = "nation-state"
    states_road = f"{root_label()},{states_text}"
    usa_text = "USA"
    usa_road = f"{states_road},{usa_text}"
    calendar_x.set_acptfact(base=week_road, pick=wed_road)
    calendar_x.set_acptfact(base=states_road, pick=usa_road)
    return calendar_x


def get_calendar_with7amCleanTableRequired() -> CalendarUnit:
    calendar_x = get_calendar_with_4_levels_and_2requireds_2acptfacts()

    time_text = "timetech"
    time_road = f"{root_label()},{time_text}"
    time_idea = IdeaKid(_label=time_text)

    day24hr_text = "24hr day"
    day24hr_road = f"{time_road},{day24hr_text}"
    day24hr_idea = IdeaKid(_label=day24hr_text, _begin=0.0, _close=24.0)

    am_text = "am"
    am_road = f"{day24hr_road},{am_text}"
    pm_text = "pm"
    n1_text = "1"
    n2_text = "2"
    n3_text = "3"
    am_idea = IdeaKid(_label=am_text, _begin=0, _close=12)
    pm_idea = IdeaKid(_label=pm_text, _begin=12, _close=24)
    n1_idea = IdeaKid(_label=n1_text, _begin=1, _close=2)
    n2_idea = IdeaKid(_label=n2_text, _begin=2, _close=3)
    n3_idea = IdeaKid(_label=n3_text, _begin=3, _close=4)

    calendar_x.add_idea(time_idea, root_label())
    calendar_x.add_idea(day24hr_idea, time_road)
    calendar_x.add_idea(am_idea, day24hr_road)
    calendar_x.add_idea(pm_idea, day24hr_road)
    calendar_x.add_idea(n1_idea, am_road)  # idea_am
    calendar_x.add_idea(n2_idea, am_road)  # idea_am
    calendar_x.add_idea(n3_idea, am_road)  # idea_am

    house_text = "housework"
    house_road = f"{root_label()},{house_text}"
    clean_text = "clean table"
    clean_road = f"{house_road},{clean_text}"
    dish_text = "remove dishs"
    soap_text = "get soap"
    soap_road = f"{clean_road},{soap_text}"
    grab_text = "grab soap"
    grab_road = f"{soap_road},{grab_text}"
    house_idea = IdeaKid(_label=house_text)
    clean_idea = IdeaKid(_label=clean_text, promise=True)
    dish_idea = IdeaKid(_label=dish_text, promise=True)
    soap_idea = IdeaKid(_label=soap_text, promise=True)
    grab_idea = IdeaKid(_label=grab_text, promise=True)

    calendar_x.add_idea(idea_kid=house_idea, walk=root_label())
    calendar_x.add_idea(idea_kid=clean_idea, walk=house_road)
    calendar_x.add_idea(idea_kid=dish_idea, walk=clean_road)
    calendar_x.add_idea(idea_kid=soap_idea, walk=clean_road)
    calendar_x.add_idea(idea_kid=grab_idea, walk=soap_road)

    clean_table_7am_base = day24hr_road
    clean_table_7am_sufffact_road = day24hr_road
    clean_table_7am_sufffact_open = 7.0
    clean_table_7am_sufffact_nigh = 7.0
    clean_table_7am_required = RequiredUnit(base=clean_table_7am_base, sufffacts={})
    clean_table_7am_required.set_sufffact(
        sufffact=clean_table_7am_sufffact_road,
        open=clean_table_7am_sufffact_open,
        nigh=clean_table_7am_sufffact_nigh,
    )
    calendar_x.edit_idea_attr(road=clean_road, required=clean_table_7am_required)
    work_text = "work"
    work_road = f"{root_label()},{work_text}"
    calendar_x.edit_idea_attr(road=work_road, required=clean_table_7am_required)
    return calendar_x


def get_calendar_1Task_1CE0MinutesRequired_1AcptFact() -> CalendarUnit:
    owner_text = "Bob"
    calendar_x = CalendarUnit(_owner=owner_text, _weight=10)
    ced_min_label = "CE0_minutes"
    ced_minutes = IdeaKid(_label=ced_min_label)
    ced_road = f"{root_label()},{ced_min_label}"
    calendar_x.add_idea(idea_kid=ced_minutes, walk=root_label())
    mail_label = "obtain mail"
    mail_task = IdeaKid(_label=mail_label, promise=True)
    calendar_x.add_idea(idea_kid=mail_task, walk=root_label())

    sufffact_x = sufffactunit_shop(need=ced_road, open=80, nigh=90)
    x_task_required = RequiredUnit(
        base=sufffact_x.need, sufffacts={sufffact_x.need: sufffact_x}
    )
    mail_road = f"{root_label()},{mail_label}"
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
    owner_text = "Kol"
    x_calendar = CalendarUnit(_owner=owner_text, _weight=10)
    shave_text = "shave"
    shave_road = f"{root_label()},{shave_text}"
    idea_kid_shave = IdeaKid(_weight=30, _label=shave_text, promise=True)
    x_calendar.add_idea(idea_kid=idea_kid_shave, walk=root_label())
    week_text = "weekdays"
    week_road = f"{root_label()},{week_text}"
    week_idea = IdeaKid(_weight=40, _label=week_text)
    x_calendar.add_idea(idea_kid=week_idea, walk=root_label())

    sun_text = "Sunday"
    sun_road = f"{week_road},{sun_text}"
    church_text = "Church"
    church_road = f"{sun_road},{church_text}"
    mon_text = "Monday"
    mon_road = f"{week_road},{mon_text}"
    idea_grandkidU = IdeaKid(_weight=20, _label=sun_text)
    idea_grandkidM = IdeaKid(_weight=20, _label=mon_text)
    x_calendar.add_idea(idea_kid=idea_grandkidU, walk=week_road)
    x_calendar.add_idea(idea_kid=idea_grandkidM, walk=week_road)

    shave_sufffact_x = sufffactunit_shop(need=mon_road)
    shave_required = RequiredUnit(
        base=week_road,
        sufffacts={shave_sufffact_x.need: shave_sufffact_x},
    )

    x_calendar.edit_idea_attr(road=shave_road, required=shave_required)
    x_calendar.set_acptfact(base=week_road, pick=sun_road)
    acptfactunit_x = acptfactunit_shop(base=week_road, pick=church_road)
    x_calendar.edit_idea_attr(road=shave_road, acptfactunit=acptfactunit_x)
    return x_calendar


def get_calendar_base_time_example() -> CalendarUnit:
    owner_text = "Sue"
    calendar_x = CalendarUnit(_owner=owner_text)
    plant = "plant"
    x_idea = IdeaKid(_label=plant)
    calendar_x.add_idea(x_idea, walk=owner_text)

    return calendar_x


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

    owner_text = "Mad Hatter"
    calendar_x = CalendarUnit(_owner=owner_text, _weight=10)
    calendar_x.set_max_tree_traverse(3)

    egg_text = "egg first"
    egg_road = f"{root_label()},{egg_text}"
    calendar_x.add_idea(idea_kid=IdeaKid(_label=egg_text), walk=root_label())

    chicken_text = "chicken first"
    chicken_road = f"{root_label()},{chicken_text}"
    calendar_x.add_idea(idea_kid=IdeaKid(_label=chicken_text), walk=root_label())

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


def get_assignment_calendar_example1():
    owner_text = "Neo"
    cx = CalendarUnit(_owner=owner_text)
    casa_text = "casa"
    casa_road = f"{root_label()},{casa_text}"
    floor_text = "mop floor"
    floor_road = f"{casa_road},{floor_text}"
    floor_idea = IdeaKid(_label=floor_text, promise=True)
    cx.add_idea(idea_kid=floor_idea, walk=casa_road)

    unim_text = "unimportant"
    unim_road = f"{root_label()},{unim_text}"
    unim_idea = IdeaKid(_label=unim_text)
    cx.add_idea(idea_kid=unim_idea, walk=root_label())

    status_text = "cleaniness status"
    status_road = f"{casa_road},{status_text}"
    status_idea = IdeaKid(_label=status_text)
    cx.add_idea(idea_kid=status_idea, walk=casa_road)

    clean_text = "clean"
    clean_road = f"{status_road},{clean_text}"
    clean_idea = IdeaKid(_label=clean_text)
    cx.add_idea(idea_kid=clean_idea, walk=status_road)

    really_text = "really"
    really_road = f"{clean_road},{really_text}"
    really_idea = IdeaKid(_label=really_text)
    cx.add_idea(idea_kid=really_idea, walk=clean_road)

    kinda_text = "kinda"
    kinda_road = f"{clean_road},{kinda_text}"
    kinda_idea = IdeaKid(_label=kinda_text)
    cx.add_idea(idea_kid=kinda_idea, walk=clean_road)

    dirty_text = "dirty"
    dirty_road = f"{status_road},{dirty_text}"
    dirty_idea = IdeaKid(_label=dirty_text)
    cx.add_idea(idea_kid=dirty_idea, walk=status_road)

    floor_required = RequiredUnit(base=status_road, sufffacts={})
    floor_required.set_sufffact(sufffact=status_road)
    cx.edit_idea_attr(road=floor_road, required=floor_required)

    return cx
