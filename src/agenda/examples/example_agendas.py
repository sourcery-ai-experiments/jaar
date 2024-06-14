from src._road.road import RoadUnit
from src.agenda.oath import oathunit_shop
from src.agenda.reason_oath import (
    beliefunit_shop,
    premiseunit_shop,
    reasonunit_shop,
    beliefunit_shop,
)
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as agendaunit_get_from_json,
)
from src.agenda.reason_assign import assignedunit_shop
from src.agenda.examples.agenda_env import get_agenda_examples_dir as env_dir
from src._instrument.file import open_file


def agenda_v001() -> AgendaUnit:
    return agendaunit_get_from_json(open_file(env_dir(), "example_agenda1.json"))


def agenda_v001_with_large_intent() -> AgendaUnit:
    yao_agenda = agenda_v001()
    day_minute_road = yao_agenda.make_l1_road("day_minute")
    month_week_road = yao_agenda.make_l1_road("month_week")
    nations_road = yao_agenda.make_l1_road("Nation-States")
    mood_road = yao_agenda.make_l1_road("Moods")
    aaron_road = yao_agenda.make_l1_road("Aaron Donald things effected by him")
    year_month_road = yao_agenda.make_l1_road("year_month")
    season_road = yao_agenda.make_l1_road("Seasons")
    ced_week_road = yao_agenda.make_l1_road("ced_week")
    weekdays_road = yao_agenda.make_l1_road("weekdays")

    yao_agenda.set_belief(base=aaron_road, pick=aaron_road)
    yao_agenda.set_belief(base=ced_week_road, pick=ced_week_road, open=0, nigh=53)
    yao_agenda.set_belief(base=day_minute_road, pick=day_minute_road, open=0, nigh=1399)
    # yao_agenda.set_belief(base=internet, pick=internet)
    yao_agenda.set_belief(base=month_week_road, pick=month_week_road, open=0, nigh=5)
    yao_agenda.set_belief(base=mood_road, pick=mood_road)
    # yao_agenda.set_belief(base=movie, pick=movie)
    yao_agenda.set_belief(base=nations_road, pick=nations_road)
    yao_agenda.set_belief(base=season_road, pick=season_road)
    yao_agenda.set_belief(base=year_month_road, pick=year_month_road, open=0, nigh=12)
    # yao_agenda.set_belief(base=water, pick=water)
    yao_agenda.set_belief(base=weekdays_road, pick=weekdays_road)
    return yao_agenda


def agenda_v002() -> AgendaUnit:
    bob_agenda = agendaunit_get_from_json(open_file(env_dir(), "example_agenda2.json"))
    print(f"{bob_agenda._real_id=} {bob_agenda._road_delimiter=}")
    return bob_agenda


def get_agenda_with_4_levels() -> AgendaUnit:
    sue_agenda = agendaunit_shop(_owner_id="Sue", _weight=10)

    casa = "casa"
    oath_kid_casa = oathunit_shop(casa, _weight=30, pledge=True)
    sue_agenda.add_l1_oath(oath_kid_casa)

    cat = "feed cat"
    oath_kid_feedcat = oathunit_shop(cat, _weight=30, pledge=True)
    sue_agenda.add_l1_oath(oath_kid_feedcat)

    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    oath_kid_weekdays = oathunit_shop(week_text, _weight=40)
    sue_agenda.add_l1_oath(oath_kid_weekdays)

    sun_text = "Sunday"
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"

    oath_grandkidU = oathunit_shop(sun_text, _weight=20)
    oath_grandkidM = oathunit_shop(mon_text, _weight=20)
    oath_grandkidT = oathunit_shop(tue_text, _weight=20)
    oath_grandkidW = oathunit_shop(wed_text, _weight=20)
    oath_grandkidR = oathunit_shop(thu_text, _weight=30)
    oath_grandkidF = oathunit_shop(fri_text, _weight=40)
    oath_grandkidA = oathunit_shop(sat_text, _weight=50)

    sue_agenda.add_oath(oath_grandkidU, week_road)
    sue_agenda.add_oath(oath_grandkidM, week_road)
    sue_agenda.add_oath(oath_grandkidT, week_road)
    sue_agenda.add_oath(oath_grandkidW, week_road)
    sue_agenda.add_oath(oath_grandkidR, week_road)
    sue_agenda.add_oath(oath_grandkidF, week_road)
    sue_agenda.add_oath(oath_grandkidA, week_road)

    states_text = "nation-state"
    states_road = sue_agenda.make_l1_road(states_text)
    oath_kid_states = oathunit_shop(states_text, _weight=30)
    sue_agenda.add_l1_oath(oath_kid_states)

    usa_text = "USA"
    usa_road = sue_agenda.make_road(states_road, usa_text)
    france_text = "France"
    brazil_text = "Brazil"
    oath_grandkid_usa = oathunit_shop(usa_text, _weight=50)
    oath_grandkid_france = oathunit_shop(france_text, _weight=50)
    oath_grandkid_brazil = oathunit_shop(brazil_text, _weight=50)
    sue_agenda.add_oath(oath_grandkid_france, states_road)
    sue_agenda.add_oath(oath_grandkid_brazil, states_road)
    sue_agenda.add_oath(oath_grandkid_usa, states_road)

    texas_text = "Texas"
    oregon_text = "Oregon"
    oath_grandgrandkid_usa_texas = oathunit_shop(texas_text, _weight=50)
    oath_grandgrandkid_usa_oregon = oathunit_shop(oregon_text, _weight=50)
    sue_agenda.add_oath(oath_grandgrandkid_usa_texas, usa_road)
    sue_agenda.add_oath(oath_grandgrandkid_usa_oregon, usa_road)
    return sue_agenda


def get_agenda_with_4_levels_and_2reasons() -> AgendaUnit:
    sue_agenda = get_agenda_with_4_levels()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = sue_agenda.make_road(week_road, wed_text)
    week_reason = reasonunit_shop(week_road)
    week_reason.set_premise(wed_road)

    nation_text = "nation-state"
    nation_road = sue_agenda.make_l1_road(nation_text)
    usa_text = "USA"
    usa_road = sue_agenda.make_road(nation_road, usa_text)
    nation_reason = reasonunit_shop(nation_road)
    nation_reason.set_premise(usa_road)

    casa_text = "casa"
    casa_road = sue_agenda.make_l1_road(casa_text)
    sue_agenda.edit_oath_attr(road=casa_road, reason=week_reason)
    sue_agenda.edit_oath_attr(road=casa_road, reason=nation_reason)
    return sue_agenda


def get_agenda_with_4_levels_and_2reasons_2beliefs() -> AgendaUnit:
    sue_agenda = get_agenda_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = sue_agenda.make_road(week_road, wed_text)
    states_text = "nation-state"
    states_road = sue_agenda.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_agenda.make_road(states_road, usa_text)
    sue_agenda.set_belief(base=week_road, pick=wed_road)
    sue_agenda.set_belief(base=states_road, pick=usa_road)
    return sue_agenda


def get_agenda_with7amCleanTableReason() -> AgendaUnit:
    sue_agenda = get_agenda_with_4_levels_and_2reasons_2beliefs()

    time_text = "timetech"
    time_road = sue_agenda.make_l1_road(time_text)
    time_oath = oathunit_shop(time_text)

    day24hr_text = "24hr day"
    day24hr_road = sue_agenda.make_road(time_road, day24hr_text)
    day24hr_oath = oathunit_shop(day24hr_text, _begin=0.0, _close=24.0)

    am_text = "am"
    am_road = sue_agenda.make_road(day24hr_road, am_text)
    pm_text = "pm"
    n1_text = "1"
    n2_text = "2"
    n3_text = "3"
    am_oath = oathunit_shop(am_text, _begin=0, _close=12)
    pm_oath = oathunit_shop(pm_text, _begin=12, _close=24)
    n1_oath = oathunit_shop(n1_text, _begin=1, _close=2)
    n2_oath = oathunit_shop(n2_text, _begin=2, _close=3)
    n3_oath = oathunit_shop(n3_text, _begin=3, _close=4)

    sue_agenda.add_l1_oath(time_oath)
    sue_agenda.add_oath(day24hr_oath, time_road)
    sue_agenda.add_oath(am_oath, day24hr_road)
    sue_agenda.add_oath(pm_oath, day24hr_road)
    sue_agenda.add_oath(n1_oath, am_road)  # oath_am
    sue_agenda.add_oath(n2_oath, am_road)  # oath_am
    sue_agenda.add_oath(n3_oath, am_road)  # oath_am

    house_text = "housemanagement"
    house_road = sue_agenda.make_l1_road(house_text)
    clean_text = "clean table"
    clean_road = sue_agenda.make_road(house_road, clean_text)
    dish_text = "remove dishs"
    soap_text = "get soap"
    soap_road = sue_agenda.make_road(clean_road, soap_text)
    grab_text = "grab soap"
    grab_road = sue_agenda.make_road(soap_road, grab_text)
    house_oath = oathunit_shop(house_text)
    clean_oath = oathunit_shop(clean_text, pledge=True)
    dish_oath = oathunit_shop(dish_text, pledge=True)
    soap_oath = oathunit_shop(soap_text, pledge=True)
    grab_oath = oathunit_shop(grab_text, pledge=True)

    sue_agenda.add_l1_oath(house_oath)
    sue_agenda.add_oath(clean_oath, house_road)
    sue_agenda.add_oath(dish_oath, clean_road)
    sue_agenda.add_oath(soap_oath, clean_road)
    sue_agenda.add_oath(grab_oath, soap_road)

    clean_table_7am_base = day24hr_road
    clean_table_7am_premise_road = day24hr_road
    clean_table_7am_premise_open = 7.0
    clean_table_7am_premise_nigh = 7.0
    clean_table_7am_reason = reasonunit_shop(clean_table_7am_base)
    clean_table_7am_reason.set_premise(
        premise=clean_table_7am_premise_road,
        open=clean_table_7am_premise_open,
        nigh=clean_table_7am_premise_nigh,
    )
    sue_agenda.edit_oath_attr(road=clean_road, reason=clean_table_7am_reason)
    casa_text = "casa"
    casa_road = sue_agenda.make_l1_road(casa_text)
    sue_agenda.edit_oath_attr(road=casa_road, reason=clean_table_7am_reason)
    return sue_agenda


def get_agenda_1Task_1CE0MinutesReason_1Belief() -> AgendaUnit:
    bob_agenda = agendaunit_shop(_owner_id="Bob", _weight=10)
    ced_min_label = "CE0_minutes"
    ced_minutes = oathunit_shop(ced_min_label)
    ced_road = bob_agenda.make_l1_road(ced_min_label)
    bob_agenda.add_l1_oath(ced_minutes)
    mail_label = "obtain mail"
    mail_task = oathunit_shop(mail_label, pledge=True)
    bob_agenda.add_l1_oath(mail_task)

    premise_x = premiseunit_shop(need=ced_road, open=80, nigh=90)
    x_task_reason = reasonunit_shop(
        base=premise_x.need, premises={premise_x.need: premise_x}
    )
    mail_road = bob_agenda.make_l1_road(mail_label)
    bob_agenda.edit_oath_attr(road=mail_road, reason=x_task_reason)

    x_belief = beliefunit_shop(base=ced_road, pick=ced_road, open=85, nigh=95)
    # print(
    #     f"1Task_1CE0MinutesReason_1Belief 2. {len(bob_agenda._oathroot._kids)=} {x_belief.base=}"
    # )
    bob_agenda.set_belief(
        base=x_belief.base,
        pick=x_belief.pick,
        open=x_belief.open,
        nigh=x_belief.nigh,
    )
    # print(f"1Task_1CE0MinutesReason_1Belief 3. {len(bob_agenda._oathroot._kids)=}")

    return bob_agenda


def get_agenda_x1_3levels_1reason_1beliefs() -> AgendaUnit:
    zia_agenda = agendaunit_shop(_owner_id="Zia", _weight=10)
    shave_text = "shave"
    shave_road = zia_agenda.make_l1_road(shave_text)
    oath_kid_shave = oathunit_shop(shave_text, _weight=30, pledge=True)
    zia_agenda.add_l1_oath(oath_kid_shave)
    week_text = "weekdays"
    week_road = zia_agenda.make_l1_road(week_text)
    week_oath = oathunit_shop(week_text, _weight=40)
    zia_agenda.add_l1_oath(week_oath)

    sun_text = "Sunday"
    sun_road = zia_agenda.make_road(week_road, sun_text)
    church_text = "Church"
    church_road = zia_agenda.make_road(sun_road, church_text)
    mon_text = "Monday"
    mon_road = zia_agenda.make_road(week_road, mon_text)
    oath_grandkidU = oathunit_shop(sun_text, _weight=20)
    oath_grandkidM = oathunit_shop(mon_text, _weight=20)
    zia_agenda.add_oath(oath_grandkidU, week_road)
    zia_agenda.add_oath(oath_grandkidM, week_road)

    shave_reason = reasonunit_shop(week_road)
    shave_reason.set_premise(mon_road)

    zia_agenda.edit_oath_attr(road=shave_road, reason=shave_reason)
    zia_agenda.set_belief(base=week_road, pick=sun_road)
    beliefunit_x = beliefunit_shop(base=week_road, pick=church_road)
    zia_agenda.edit_oath_attr(road=shave_road, beliefunit=beliefunit_x)
    return zia_agenda


def get_agenda_base_time_example() -> AgendaUnit:
    sue_agenda = agendaunit_shop(_owner_id="Sue")
    sue_agenda.add_l1_oath(oathunit_shop("casa"))
    return sue_agenda


def get_agenda_irrational_example() -> AgendaUnit:
    # this agenda has no conclusive intent because 2 pledge oaths are in contradiction
    # "egg first" is true when "chicken first" is false
    # "chicken first" is true when "egg first" is true
    # Step 0: if chicken._active == True, egg._active is set to False
    # Step 1: if egg._active is False, chicken._active is set to False
    # Step 2: if chicken._active is False, egg._active is set to True
    # Step 3: if egg._active == True, chicken._active is set to True
    # Step 4: back to step 0.
    # after hatter_agenda.calc_agenda_metrics these should be true:
    # 1. hatter_agenda._irrational == True
    # 2. hatter_agenda._tree_traverse_count = hatter_agenda._max_tree_traverse

    hatter_agenda = agendaunit_shop(_owner_id="Mad Hatter", _weight=10)
    hatter_agenda.set_max_tree_traverse(3)

    egg_text = "egg first"
    egg_road = hatter_agenda.make_l1_road(egg_text)
    hatter_agenda.add_l1_oath(oathunit_shop(egg_text))

    chicken_text = "chicken first"
    chicken_road = hatter_agenda.make_l1_road(chicken_text)
    hatter_agenda.add_l1_oath(oathunit_shop(chicken_text))

    # set egg pledge is True when chicken first is False
    hatter_agenda.edit_oath_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_suff_oath_active=True,
    )

    # set chick pledge is True when egg first is False
    hatter_agenda.edit_oath_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_suff_oath_active=False,
    )

    return hatter_agenda


def get_assignment_agenda_example1():
    neo_agenda = agendaunit_shop("Neo")
    casa_text = "casa"
    casa_road = neo_agenda.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = neo_agenda.make_road(casa_road, floor_text)
    floor_oath = oathunit_shop(floor_text, pledge=True)
    neo_agenda.add_oath(floor_oath, casa_road)
    neo_agenda.add_l1_oath(oathunit_shop("unimportant"))

    status_text = "cleaniness status"
    status_road = neo_agenda.make_road(casa_road, status_text)
    neo_agenda.add_oath(oathunit_shop(status_text), casa_road)

    clean_text = "clean"
    clean_road = neo_agenda.make_road(status_road, clean_text)
    neo_agenda.add_oath(oathunit_shop(clean_text), status_road)
    neo_agenda.add_oath(oathunit_shop("very_much"), clean_road)
    neo_agenda.add_oath(oathunit_shop("moderately"), clean_road)
    neo_agenda.add_oath(oathunit_shop("dirty"), status_road)

    floor_reason = reasonunit_shop(status_road)
    floor_reason.set_premise(premise=status_road)
    neo_agenda.edit_oath_attr(road=floor_road, reason=floor_reason)
    return neo_agenda


def get_agenda_assignment_laundry_example1() -> AgendaUnit:
    amos_text = "Amos"
    amos_agenda = agendaunit_shop(_owner_id=amos_text)
    cali_text = "Cali"
    amos_agenda.add_partyunit(amos_text)
    amos_agenda.add_partyunit(cali_text)

    casa_text = "casa"
    basket_text = "laundry basket status"
    b_full_text = "full"
    b_smel_text = "smelly"
    b_bare_text = "bare"
    b_fine_text = "fine"
    b_half_text = "half full"
    do_laundry_text = "do_laundry"
    casa_road = amos_agenda.make_l1_road(casa_text)
    basket_road = amos_agenda.make_road(casa_road, basket_text)
    b_full_road = amos_agenda.make_road(basket_road, b_full_text)
    b_smel_road = amos_agenda.make_road(basket_road, b_smel_text)
    laundry_task_road = amos_agenda.make_road(casa_road, do_laundry_text)
    amos_agenda.add_l1_oath(oathunit_shop(casa_text))
    amos_agenda.add_oath(oathunit_shop(basket_text), casa_road)
    amos_agenda.add_oath(oathunit_shop(b_full_text), basket_road)
    amos_agenda.add_oath(oathunit_shop(b_smel_text), basket_road)
    amos_agenda.add_oath(oathunit_shop(b_bare_text), basket_road)
    amos_agenda.add_oath(oathunit_shop(b_fine_text), basket_road)
    amos_agenda.add_oath(oathunit_shop(b_half_text), basket_road)
    amos_agenda.add_oath(oathunit_shop(do_laundry_text, pledge=True), casa_road)

    # laundry requirement
    amos_agenda.edit_oath_attr(
        road=laundry_task_road, reason_base=basket_road, reason_premise=b_full_road
    )
    # laundry requirement
    amos_agenda.edit_oath_attr(
        road=laundry_task_road, reason_base=basket_road, reason_premise=b_smel_road
    )
    # assign Cali to task
    cali_assignunit = assignedunit_shop()
    cali_assignunit.set_suffidea(cali_text)
    amos_agenda.edit_oath_attr(road=laundry_task_road, assignedunit=cali_assignunit)
    # print(f"{basket_road=}")
    # print(f"{amos_agenda._real_id=}")
    amos_agenda.set_belief(base=basket_road, pick=b_full_road)

    return amos_agenda


def get_agenda_with_tuesday_cleaning_task() -> AgendaUnit:
    bob_agenda = agendaunit_shop("Bob")
    bob_agenda.set_time_hreg_oaths(7)

    casa_text = "casa"
    casa_road = bob_agenda.make_l1_road(casa_text)
    laundry_text = "do_laundry"
    laundry_road = bob_agenda.make_road(casa_road, laundry_text)
    chill_text = "chill"
    chill_road = bob_agenda.make_road(casa_road, chill_text)
    bob_agenda.add_l1_oath(oathunit_shop(casa_text))
    jajatime_road = bob_agenda.make_road(bob_agenda.make_l1_road("time"), "jajatime")
    bob_agenda.set_belief(jajatime_road, jajatime_road, 1064131200, 1064136133)

    bob_agenda.add_oath(oathunit_shop(laundry_text, pledge=True), casa_road)
    bob_agenda.edit_oath_attr(
        road=laundry_road,
        reason_base=jajatime_road,
        reason_premise=jajatime_road,
        reason_premise_open=5760.0,
        reason_premise_nigh=5760.0,
        reason_premise_divisor=10080.0,
    )
    bob_agenda.add_oath(oathunit_shop(chill_text, pledge=True), casa_road)
    bob_agenda.edit_oath_attr(
        road=chill_road,
        reason_base=jajatime_road,
        reason_premise=jajatime_road,
        reason_premise_open=5760.0,
        reason_premise_nigh=7160.0,
        reason_premise_divisor=10080.0,
    )
    # # print(f"{bob_agenda._oathroot._beliefunits.values()=}")
    # laundry_reasonunit = bob_agenda.get_oath_obj(laundry_road).get_reasonunit(
    #     jajatime_road
    # )
    # laundry_premise = laundry_reasonunit.get_premise(jajatime_road)
    # # print(f"{laundry_reasonunit.base=} {laundry_premise=}")
    # bob_agenda.calc_agenda_metrics()
    # for x_oathunit in bob_agenda._oath_dict.values():
    #     if x_oathunit._label in [laundry_text]:
    # print(f"{x_oathunit._label=} {x_oathunit._begin=} {x_oathunit._close=}")
    # print(f"{x_oathunit._kids.keys()=}")
    # jaja_beliefheir = x_oathunit._beliefheirs.get(jajatime_road)
    # print(f"{jaja_beliefheir.open % 10080=}")
    # print(f"{jaja_beliefheir.nigh % 10080=}")

    # print(f"{bob_agenda.get_intent_dict().keys()=}")

    return bob_agenda


# class YR:
def from_list_get_active(
    road: RoadUnit, oath_dict: dict, asse_bool: bool = None
) -> bool:
    active = None
    temp_oath = None

    active_true_count = 0
    active_false_count = 0
    for oath in oath_dict.values():
        if oath.get_road() == road:
            temp_oath = oath
            print(
                f"searched for OathUnit {temp_oath.get_road()} found {temp_oath._active=}"
            )

        if oath._active:
            active_true_count += 1
        elif oath._active is False:
            active_false_count += 1

    active = temp_oath._active
    print(
        f"Set active: {oath._label=} {active} {active_true_count=} {active_false_count=}"
    )

    if asse_bool in {True, False}:
        if active != asse_bool:
            yr_elucidation(temp_oath)

        assert active == asse_bool
    else:
        yr_elucidation(temp_oath)
    return active


def yr_print_oath_base_info(oath, filter: bool):
    for l in oath._reasonheirs.values():
        if l._status == filter:
            print(
                f"  ReasonHeir '{l.base}' Base LH:{l._status} W:{len(l.premises)}"  # \t_task {l._task}"
            )
            if str(type(oath)).find(".oath.OathUnit'>") > 0:
                yr_print_belief(
                    lh_base=l.base,
                    lh_status=l._status,
                    premises=l.premises,
                    beliefheirs=oath._beliefheirs,
                )


def yr_elucidation(oath):
    str1 = f"'{yr_d(oath._parent_road)}' oath"
    str2 = f" has ReasonU:{yr_x(oath._reasonunits)} LH:{yr_x(oath._reasonheirs)}"
    str3 = f" {str(type(oath))}"
    str4 = " "
    if str(type(oath)).find(".oath.OathUnit'>") > 0:
        str3 = f" Beliefs:{yr_x(oath._beliefheirs)} Status: {oath._active}"

        print(f"\n{str1}{str2}{str3}")
        hh_wo_matched_reason = []
        for hh in oath._beliefheirs.values():
            hh_wo_matched_reason = []
            try:
                oath._reasonheirs[hh.base]
            except Exception:
                hh_wo_matched_reason.append(hh.base)

        for base in hh_wo_matched_reason:
            print(f"Beliefs that don't matter to this Oath: {base}")

    # if oath._reasonunits != None:
    #     for lu in oath._reasonunits.values():
    #         print(f"  ReasonUnit   '{lu.base}' premises: {len(lu.premises)} ")
    if oath._reasonheirs != None:
        filter_x = True
        yr_print_oath_base_info(oath=oath, filter=True)

        filter_x = False
        print("\nReasons that failed:")

        for l in oath._reasonheirs.values():
            if l._status == filter_x:
                print(
                    f"  ReasonHeir '{l.base}' Base LH:{l._status} W:{len(l.premises)}"  # \t_task {l._task}"
                )
                if str(type(oath)).find(".oath.OathUnit'>") > 0:
                    yr_print_belief(
                        lh_base=l.base,
                        lh_status=l._status,
                        premises=l.premises,
                        beliefheirs=oath._beliefheirs,
                    )
                print("")
    # print(oath._beliefheirs)
    # print(f"{(oath._beliefheirs != None)=}")
    # print(f"{len(oath._beliefheirs)=} ")

    print("")


def yr_print_belief(lh_base, lh_status, premises, beliefheirs):
    for ww in premises.values():
        ww_open = ""
        ww_open = f"\topen:{ww.open}" if ww.open != None else ""
        ww_nigh = ""
        ww_nigh = f"\tnigh:{ww.nigh}" if ww.nigh != None else ""
        ww_task = f" Task: {ww._task}"
        hh_open = ""
        hh_nigh = ""
        hh_pick = ""
        print(
            f"\t    '{lh_base}' Premise LH:{lh_status} W:{ww._status}\tneed:{ww.need}{ww_open}{ww_nigh}"
        )

        for hh in beliefheirs.values():
            if hh.base == lh_base:
                if hh.open != None:
                    hh_open = f"\topen:{hh.open}"
                if hh.nigh != None:
                    hh_nigh = f"\tnigh:{hh.nigh}"
                hh_pick = hh.pick
                # if hh_pick != "":
                print(
                    f"\t    '{hh.base}' Belief LH:{lh_status} W:{ww._status}\tBelief:{hh_pick}{hh_open}{hh_nigh}"
                )
        if hh_pick == "":
            print(f"\t    Base: No Belief")


def yr_d(self):
    return "no road" if self is None else self[self.find(",") + 1 :]


def yr_x(self):
    return 0 if self is None else len(self)
