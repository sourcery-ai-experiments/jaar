from src.agenda.idea import IdeaKid
from src.agenda.required_idea import (
    acptfactunit_shop,
    sufffactunit_shop,
    RequiredUnit,
    acptfactunit_shop,
)
from src.agenda.agenda import (
    DealUnit,
    agendaunit_shop,
    get_from_json as agenda_get_from_json,
)
from src.agenda.x_func import open_file as x_func_open_file
from src.agenda.examples.agenda_env import agenda_env


def agenda_v001() -> DealUnit:
    return agenda_get_from_json(
        x_func_open_file(dest_dir=agenda_env(), file_title="example_agenda1.json")
    )


def agenda_v001_with_large_goal() -> DealUnit:
    x_agenda = agenda_v001()
    day_minute_text = "day_minute"
    day_minute_road = f"{x_agenda._culture_handle},{day_minute_text}"
    month_week_text = "month_week"
    month_week_road = f"{x_agenda._culture_handle},{month_week_text}"
    nations_text = "Nation-States"
    nations_road = f"{x_agenda._culture_handle},{nations_text}"
    mood_text = "Moods"
    mood_road = f"{x_agenda._culture_handle},{mood_text}"
    aaron_text = "Aaron Donald sphere"
    aaron_road = f"{x_agenda._culture_handle},{aaron_text}"
    # internet_text = "Internet"
    # internet_road = f"{x_agenda._culture_handle},{internet_text}"
    year_month_text = "year_month"
    year_month_road = f"{x_agenda._culture_handle},{year_month_text}"
    season_text = "Seasons"
    season_road = f"{x_agenda._culture_handle},{season_text}"
    ced_week_text = "ced_week"
    ced_week_road = f"{x_agenda._culture_handle},{ced_week_text}"
    # water_text = "WaterBeing"
    # water_road = f"{x_agenda._culture_handle},{water_text}"
    weekdays_text = "weekdays"
    weekdays_road = f"{x_agenda._culture_handle},{weekdays_text}"
    # movie_text = "No Movie playing"
    # movie_road = f"{x_agenda._culture_handle},{movie_text}"

    x_agenda.set_acptfact(base=aaron_road, pick=aaron_road)
    x_agenda.set_acptfact(base=ced_week_road, pick=ced_week_road, open=0, nigh=53)
    x_agenda.set_acptfact(base=day_minute_road, pick=day_minute_road, open=0, nigh=1399)
    # x_agenda.set_acptfact(base=internet, pick=internet)
    x_agenda.set_acptfact(base=month_week_road, pick=month_week_road, open=0, nigh=5)
    x_agenda.set_acptfact(base=mood_road, pick=mood_road)
    # x_agenda.set_acptfact(base=movie, pick=movie)
    x_agenda.set_acptfact(base=nations_road, pick=nations_road)
    x_agenda.set_acptfact(base=season_road, pick=season_road)
    x_agenda.set_acptfact(base=year_month_road, pick=year_month_road, open=0, nigh=12)
    # x_agenda.set_acptfact(base=water, pick=water)
    x_agenda.set_acptfact(base=weekdays_road, pick=weekdays_road)

    return x_agenda


def agenda_v002() -> DealUnit:
    return agenda_get_from_json(
        x_func_open_file(dest_dir=agenda_env(), file_title="example_agenda2.json")
    )


def get_agenda_with_4_levels() -> DealUnit:
    healer_text = "Noa"
    x_agenda = agendaunit_shop(_healer=healer_text, _weight=10)
    print(f"{x_agenda._auto_output_to_public=}")

    work = "work"
    idea_kid_work = IdeaKid(_weight=30, _label=work, promise=True)
    x_agenda.add_idea(idea_kid=idea_kid_work, pad=x_agenda._culture_handle)

    cat = "feed cat"
    idea_kid_feedcat = IdeaKid(_weight=30, _label=cat, promise=True)
    x_agenda.add_idea(idea_kid=idea_kid_feedcat, pad=x_agenda._culture_handle)

    week_text = "weekdays"
    week_road = f"{x_agenda._culture_handle},{week_text}"
    idea_kid_weekdays = IdeaKid(_weight=40, _label=week_text)
    x_agenda.add_idea(idea_kid=idea_kid_weekdays, pad=x_agenda._culture_handle)

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

    x_agenda.add_idea(idea_grandkidU, week_road)
    x_agenda.add_idea(idea_grandkidM, week_road)
    x_agenda.add_idea(idea_grandkidT, week_road)
    x_agenda.add_idea(idea_grandkidW, week_road)
    x_agenda.add_idea(idea_grandkidR, week_road)
    x_agenda.add_idea(idea_grandkidF, week_road)
    x_agenda.add_idea(idea_grandkidA, week_road)

    states_text = "nation-state"
    states_road = f"{x_agenda._culture_handle},{states_text}"
    idea_kid_states = IdeaKid(_weight=30, _label=states_text)
    x_agenda.add_idea(idea_kid=idea_kid_states, pad=f"{x_agenda._culture_handle}")

    usa_text = "USA"
    usa_road = f"{states_road},{usa_text}"
    france_text = "France"
    brazil_text = "Brazil"
    idea_grandkid_usa = IdeaKid(_weight=50, _label=usa_text)
    idea_grandkid_france = IdeaKid(_weight=50, _label=france_text)
    idea_grandkid_brazil = IdeaKid(_weight=50, _label=brazil_text)
    x_agenda.add_idea(idea_grandkid_france, states_road)
    x_agenda.add_idea(idea_grandkid_brazil, states_road)
    x_agenda.add_idea(idea_grandkid_usa, states_road)

    texas_text = "Texas"
    oregon_text = "Oregon"
    idea_grandgrandkid_usa_texas = IdeaKid(_weight=50, _label=texas_text)
    idea_grandgrandkid_usa_oregon = IdeaKid(_weight=50, _label=oregon_text)
    x_agenda.add_idea(idea_grandgrandkid_usa_texas, usa_road)
    x_agenda.add_idea(idea_grandgrandkid_usa_oregon, usa_road)
    return x_agenda


def get_agenda_with_4_levels_and_2requireds() -> DealUnit:
    x_agenda = get_agenda_with_4_levels()
    week_text = "weekdays"
    week_road = f"{x_agenda._culture_handle},{week_text}"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"
    week_required = RequiredUnit(base=week_road, sufffacts={})
    week_required.set_sufffact(wed_road)

    nation_text = "nation-state"
    nation_road = f"{x_agenda._culture_handle},{nation_text}"
    usa_text = "USA"
    usa_road = f"{nation_road},{usa_text}"
    nation_required = RequiredUnit(base=nation_road, sufffacts={})
    nation_required.set_sufffact(usa_road)

    work_text = "work"
    work_road = f"{x_agenda._culture_handle},{work_text}"
    x_agenda.edit_idea_attr(road=work_road, required=week_required)
    x_agenda.edit_idea_attr(road=work_road, required=nation_required)
    return x_agenda


def get_agenda_with_4_levels_and_2requireds_2acptfacts() -> DealUnit:
    x_agenda = get_agenda_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = f"{x_agenda._culture_handle},{week_text}"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"
    states_text = "nation-state"
    states_road = f"{x_agenda._culture_handle},{states_text}"
    usa_text = "USA"
    usa_road = f"{states_road},{usa_text}"
    x_agenda.set_acptfact(base=week_road, pick=wed_road)
    x_agenda.set_acptfact(base=states_road, pick=usa_road)
    return x_agenda


def get_agenda_with7amCleanTableRequired() -> DealUnit:
    x_agenda = get_agenda_with_4_levels_and_2requireds_2acptfacts()

    time_text = "timetech"
    time_road = f"{x_agenda._culture_handle},{time_text}"
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

    x_agenda.add_idea(time_idea, x_agenda._culture_handle)
    x_agenda.add_idea(day24hr_idea, time_road)
    x_agenda.add_idea(am_idea, day24hr_road)
    x_agenda.add_idea(pm_idea, day24hr_road)
    x_agenda.add_idea(n1_idea, am_road)  # idea_am
    x_agenda.add_idea(n2_idea, am_road)  # idea_am
    x_agenda.add_idea(n3_idea, am_road)  # idea_am

    house_text = "housework"
    house_road = f"{x_agenda._culture_handle},{house_text}"
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

    x_agenda.add_idea(idea_kid=house_idea, pad=x_agenda._culture_handle)
    x_agenda.add_idea(idea_kid=clean_idea, pad=house_road)
    x_agenda.add_idea(idea_kid=dish_idea, pad=clean_road)
    x_agenda.add_idea(idea_kid=soap_idea, pad=clean_road)
    x_agenda.add_idea(idea_kid=grab_idea, pad=soap_road)

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
    x_agenda.edit_idea_attr(road=clean_road, required=clean_table_7am_required)
    work_text = "work"
    work_road = f"{x_agenda._culture_handle},{work_text}"
    x_agenda.edit_idea_attr(road=work_road, required=clean_table_7am_required)
    return x_agenda


def get_agenda_1Task_1CE0MinutesRequired_1AcptFact() -> DealUnit:
    healer_text = "Bob"
    x_agenda = agendaunit_shop(_healer=healer_text, _weight=10)
    ced_min_label = "CE0_minutes"
    ced_minutes = IdeaKid(_label=ced_min_label)
    ced_road = f"{x_agenda._culture_handle},{ced_min_label}"
    x_agenda.add_idea(idea_kid=ced_minutes, pad=x_agenda._culture_handle)
    mail_label = "obtain mail"
    mail_task = IdeaKid(_label=mail_label, promise=True)
    x_agenda.add_idea(idea_kid=mail_task, pad=x_agenda._culture_handle)

    sufffact_x = sufffactunit_shop(need=ced_road, open=80, nigh=90)
    x_task_required = RequiredUnit(
        base=sufffact_x.need, sufffacts={sufffact_x.need: sufffact_x}
    )
    mail_road = f"{x_agenda._culture_handle},{mail_label}"
    x_agenda.edit_idea_attr(road=mail_road, required=x_task_required)

    x_acptfact = acptfactunit_shop(base=ced_road, pick=ced_road, open=85, nigh=95)
    # print(
    #     f"1Task_1CE0MinutesRequired_1AcptFact 2. {len(x_agenda._idearoot._kids)=} {x_acptfact.base=}"
    # )
    x_agenda.set_acptfact(
        base=x_acptfact.base,
        pick=x_acptfact.pick,
        open=x_acptfact.open,
        nigh=x_acptfact.nigh,
    )
    # print(f"1Task_1CE0MinutesRequired_1AcptFact 3. {len(x_agenda._idearoot._kids)=}")

    return x_agenda


def get_agenda_x1_3levels_1required_1acptfacts() -> DealUnit:
    healer_text = "Kol"
    x_agenda = agendaunit_shop(_healer=healer_text, _weight=10)
    shave_text = "shave"
    shave_road = f"{x_agenda._culture_handle},{shave_text}"
    idea_kid_shave = IdeaKid(_weight=30, _label=shave_text, promise=True)
    x_agenda.add_idea(idea_kid=idea_kid_shave, pad=x_agenda._culture_handle)
    week_text = "weekdays"
    week_road = f"{x_agenda._culture_handle},{week_text}"
    week_idea = IdeaKid(_weight=40, _label=week_text)
    x_agenda.add_idea(idea_kid=week_idea, pad=x_agenda._culture_handle)

    sun_text = "Sunday"
    sun_road = f"{week_road},{sun_text}"
    church_text = "Church"
    church_road = f"{sun_road},{church_text}"
    mon_text = "Monday"
    mon_road = f"{week_road},{mon_text}"
    idea_grandkidU = IdeaKid(_weight=20, _label=sun_text)
    idea_grandkidM = IdeaKid(_weight=20, _label=mon_text)
    x_agenda.add_idea(idea_kid=idea_grandkidU, pad=week_road)
    x_agenda.add_idea(idea_kid=idea_grandkidM, pad=week_road)

    shave_sufffact_x = sufffactunit_shop(need=mon_road)
    shave_required = RequiredUnit(
        base=week_road,
        sufffacts={shave_sufffact_x.need: shave_sufffact_x},
    )

    x_agenda.edit_idea_attr(road=shave_road, required=shave_required)
    x_agenda.set_acptfact(base=week_road, pick=sun_road)
    acptfactunit_x = acptfactunit_shop(base=week_road, pick=church_road)
    x_agenda.edit_idea_attr(road=shave_road, acptfactunit=acptfactunit_x)
    return x_agenda


def get_agenda_base_time_example() -> DealUnit:
    healer_text = "Sue"
    x_agenda = agendaunit_shop(_healer=healer_text)
    plant = "plant"
    x_idea = IdeaKid(_label=plant)
    x_agenda.add_idea(x_idea, pad=healer_text)

    return x_agenda


def get_agenda_irrational_example() -> DealUnit:
    # this agenda has no conclusive goal because 2 promise ideas are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active_status == True, egg._active_status is set to False
    # Step 1: if egg._active_status == False, chicken._active_status is set to False
    # Step 2: if chicken._active_status == False, egg._active_status is set to True
    # Step 3: if egg._active_status == True, chicken._active_status is set to True
    # Step 4: back to step 0.
    # after x_agenda.set_agenda_metrics these should be true:
    # 1. x_agenda._irrational == True
    # 2. x_agenda._tree_traverse_count = x_agenda._max_tree_traverse

    healer_text = "Mad Hatter"
    x_agenda = agendaunit_shop(_healer=healer_text, _weight=10)
    x_agenda.set_max_tree_traverse(3)

    egg_text = "egg first"
    egg_road = f"{x_agenda._culture_handle},{egg_text}"
    x_agenda.add_idea(idea_kid=IdeaKid(_label=egg_text), pad=x_agenda._culture_handle)

    chicken_text = "chicken first"
    chicken_road = f"{x_agenda._culture_handle},{chicken_text}"
    x_agenda.add_idea(
        idea_kid=IdeaKid(_label=chicken_text), pad=x_agenda._culture_handle
    )

    # set egg promise is True when chicken first is False
    x_agenda.edit_idea_attr(
        road=egg_road,
        promise=True,
        required_base=chicken_road,
        required_suff_idea_active_status=True,
    )

    # set chick promise is True when egg first is False
    x_agenda.edit_idea_attr(
        road=chicken_road,
        promise=True,
        required_base=egg_road,
        required_suff_idea_active_status=False,
    )

    return x_agenda


def get_assignment_agenda_example1():
    healer_text = "Neo"
    x_agenda = agendaunit_shop(_healer=healer_text)
    casa_text = "casa"
    casa_road = f"{x_agenda._culture_handle},{casa_text}"
    floor_text = "mop floor"
    floor_road = f"{casa_road},{floor_text}"
    floor_idea = IdeaKid(_label=floor_text, promise=True)
    x_agenda.add_idea(idea_kid=floor_idea, pad=casa_road)

    unim_text = "unimportant"
    unim_road = f"{x_agenda._culture_handle},{unim_text}"
    unim_idea = IdeaKid(_label=unim_text)
    x_agenda.add_idea(idea_kid=unim_idea, pad=x_agenda._culture_handle)

    status_text = "cleaniness status"
    status_road = f"{casa_road},{status_text}"
    status_idea = IdeaKid(_label=status_text)
    x_agenda.add_idea(idea_kid=status_idea, pad=casa_road)

    clean_text = "clean"
    clean_road = f"{status_road},{clean_text}"
    clean_idea = IdeaKid(_label=clean_text)
    x_agenda.add_idea(idea_kid=clean_idea, pad=status_road)

    very_much_text = "very_much"
    very_much_road = f"{clean_road},{very_much_text}"
    very_much_idea = IdeaKid(_label=very_much_text)
    x_agenda.add_idea(idea_kid=very_much_idea, pad=clean_road)

    moderately_text = "moderately"
    moderately_road = f"{clean_road},{moderately_text}"
    moderately_idea = IdeaKid(_label=moderately_text)
    x_agenda.add_idea(idea_kid=moderately_idea, pad=clean_road)

    dirty_text = "dirty"
    dirty_road = f"{status_road},{dirty_text}"
    dirty_idea = IdeaKid(_label=dirty_text)
    x_agenda.add_idea(idea_kid=dirty_idea, pad=status_road)

    floor_required = RequiredUnit(base=status_road, sufffacts={})
    floor_required.set_sufffact(sufffact=status_road)
    x_agenda.edit_idea_attr(road=floor_road, required=floor_required)

    return x_agenda
