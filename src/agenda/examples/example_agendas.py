from src._road.road import RoadUnit
from src.agenda.fact import factunit_shop
from src.agenda.reason_fact import (
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
    fact_kid_casa = factunit_shop(casa, _weight=30, pledge=True)
    sue_agenda.add_l1_fact(fact_kid_casa)

    cat = "feed cat"
    fact_kid_feedcat = factunit_shop(cat, _weight=30, pledge=True)
    sue_agenda.add_l1_fact(fact_kid_feedcat)

    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    fact_kid_weekdays = factunit_shop(week_text, _weight=40)
    sue_agenda.add_l1_fact(fact_kid_weekdays)

    sun_text = "Sunday"
    mon_text = "Monday"
    tue_text = "Tuesday"
    wed_text = "Wednesday"
    thu_text = "Thursday"
    fri_text = "Friday"
    sat_text = "Saturday"

    fact_grandkidU = factunit_shop(sun_text, _weight=20)
    fact_grandkidM = factunit_shop(mon_text, _weight=20)
    fact_grandkidT = factunit_shop(tue_text, _weight=20)
    fact_grandkidW = factunit_shop(wed_text, _weight=20)
    fact_grandkidR = factunit_shop(thu_text, _weight=30)
    fact_grandkidF = factunit_shop(fri_text, _weight=40)
    fact_grandkidA = factunit_shop(sat_text, _weight=50)

    sue_agenda.add_fact(fact_grandkidU, week_road)
    sue_agenda.add_fact(fact_grandkidM, week_road)
    sue_agenda.add_fact(fact_grandkidT, week_road)
    sue_agenda.add_fact(fact_grandkidW, week_road)
    sue_agenda.add_fact(fact_grandkidR, week_road)
    sue_agenda.add_fact(fact_grandkidF, week_road)
    sue_agenda.add_fact(fact_grandkidA, week_road)

    states_text = "nation-state"
    states_road = sue_agenda.make_l1_road(states_text)
    fact_kid_states = factunit_shop(states_text, _weight=30)
    sue_agenda.add_l1_fact(fact_kid_states)

    usa_text = "USA"
    usa_road = sue_agenda.make_road(states_road, usa_text)
    france_text = "France"
    brazil_text = "Brazil"
    fact_grandkid_usa = factunit_shop(usa_text, _weight=50)
    fact_grandkid_france = factunit_shop(france_text, _weight=50)
    fact_grandkid_brazil = factunit_shop(brazil_text, _weight=50)
    sue_agenda.add_fact(fact_grandkid_france, states_road)
    sue_agenda.add_fact(fact_grandkid_brazil, states_road)
    sue_agenda.add_fact(fact_grandkid_usa, states_road)

    texas_text = "Texas"
    oregon_text = "Oregon"
    fact_grandgrandkid_usa_texas = factunit_shop(texas_text, _weight=50)
    fact_grandgrandkid_usa_oregon = factunit_shop(oregon_text, _weight=50)
    sue_agenda.add_fact(fact_grandgrandkid_usa_texas, usa_road)
    sue_agenda.add_fact(fact_grandgrandkid_usa_oregon, usa_road)
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
    sue_agenda.edit_fact_attr(road=casa_road, reason=week_reason)
    sue_agenda.edit_fact_attr(road=casa_road, reason=nation_reason)
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
    time_fact = factunit_shop(time_text)

    day24hr_text = "24hr day"
    day24hr_road = sue_agenda.make_road(time_road, day24hr_text)
    day24hr_fact = factunit_shop(day24hr_text, _begin=0.0, _close=24.0)

    am_text = "am"
    am_road = sue_agenda.make_road(day24hr_road, am_text)
    pm_text = "pm"
    n1_text = "1"
    n2_text = "2"
    n3_text = "3"
    am_fact = factunit_shop(am_text, _begin=0, _close=12)
    pm_fact = factunit_shop(pm_text, _begin=12, _close=24)
    n1_fact = factunit_shop(n1_text, _begin=1, _close=2)
    n2_fact = factunit_shop(n2_text, _begin=2, _close=3)
    n3_fact = factunit_shop(n3_text, _begin=3, _close=4)

    sue_agenda.add_l1_fact(time_fact)
    sue_agenda.add_fact(day24hr_fact, time_road)
    sue_agenda.add_fact(am_fact, day24hr_road)
    sue_agenda.add_fact(pm_fact, day24hr_road)
    sue_agenda.add_fact(n1_fact, am_road)  # fact_am
    sue_agenda.add_fact(n2_fact, am_road)  # fact_am
    sue_agenda.add_fact(n3_fact, am_road)  # fact_am

    house_text = "housemanagement"
    house_road = sue_agenda.make_l1_road(house_text)
    clean_text = "clean table"
    clean_road = sue_agenda.make_road(house_road, clean_text)
    dish_text = "remove dishs"
    soap_text = "get soap"
    soap_road = sue_agenda.make_road(clean_road, soap_text)
    grab_text = "grab soap"
    grab_road = sue_agenda.make_road(soap_road, grab_text)
    house_fact = factunit_shop(house_text)
    clean_fact = factunit_shop(clean_text, pledge=True)
    dish_fact = factunit_shop(dish_text, pledge=True)
    soap_fact = factunit_shop(soap_text, pledge=True)
    grab_fact = factunit_shop(grab_text, pledge=True)

    sue_agenda.add_l1_fact(house_fact)
    sue_agenda.add_fact(clean_fact, house_road)
    sue_agenda.add_fact(dish_fact, clean_road)
    sue_agenda.add_fact(soap_fact, clean_road)
    sue_agenda.add_fact(grab_fact, soap_road)

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
    sue_agenda.edit_fact_attr(road=clean_road, reason=clean_table_7am_reason)
    casa_text = "casa"
    casa_road = sue_agenda.make_l1_road(casa_text)
    sue_agenda.edit_fact_attr(road=casa_road, reason=clean_table_7am_reason)
    return sue_agenda


def get_agenda_1Task_1CE0MinutesReason_1Belief() -> AgendaUnit:
    bob_agenda = agendaunit_shop(_owner_id="Bob", _weight=10)
    ced_min_label = "CE0_minutes"
    ced_minutes = factunit_shop(ced_min_label)
    ced_road = bob_agenda.make_l1_road(ced_min_label)
    bob_agenda.add_l1_fact(ced_minutes)
    mail_label = "obtain mail"
    mail_task = factunit_shop(mail_label, pledge=True)
    bob_agenda.add_l1_fact(mail_task)

    premise_x = premiseunit_shop(need=ced_road, open=80, nigh=90)
    x_task_reason = reasonunit_shop(
        base=premise_x.need, premises={premise_x.need: premise_x}
    )
    mail_road = bob_agenda.make_l1_road(mail_label)
    bob_agenda.edit_fact_attr(road=mail_road, reason=x_task_reason)

    x_belief = beliefunit_shop(base=ced_road, pick=ced_road, open=85, nigh=95)
    # print(
    #     f"1Task_1CE0MinutesReason_1Belief 2. {len(bob_agenda._factroot._kids)=} {x_belief.base=}"
    # )
    bob_agenda.set_belief(
        base=x_belief.base,
        pick=x_belief.pick,
        open=x_belief.open,
        nigh=x_belief.nigh,
    )
    # print(f"1Task_1CE0MinutesReason_1Belief 3. {len(bob_agenda._factroot._kids)=}")

    return bob_agenda


def get_agenda_x1_3levels_1reason_1beliefs() -> AgendaUnit:
    zia_agenda = agendaunit_shop(_owner_id="Zia", _weight=10)
    shave_text = "shave"
    shave_road = zia_agenda.make_l1_road(shave_text)
    fact_kid_shave = factunit_shop(shave_text, _weight=30, pledge=True)
    zia_agenda.add_l1_fact(fact_kid_shave)
    week_text = "weekdays"
    week_road = zia_agenda.make_l1_road(week_text)
    week_fact = factunit_shop(week_text, _weight=40)
    zia_agenda.add_l1_fact(week_fact)

    sun_text = "Sunday"
    sun_road = zia_agenda.make_road(week_road, sun_text)
    church_text = "Church"
    church_road = zia_agenda.make_road(sun_road, church_text)
    mon_text = "Monday"
    mon_road = zia_agenda.make_road(week_road, mon_text)
    fact_grandkidU = factunit_shop(sun_text, _weight=20)
    fact_grandkidM = factunit_shop(mon_text, _weight=20)
    zia_agenda.add_fact(fact_grandkidU, week_road)
    zia_agenda.add_fact(fact_grandkidM, week_road)

    shave_reason = reasonunit_shop(week_road)
    shave_reason.set_premise(mon_road)

    zia_agenda.edit_fact_attr(road=shave_road, reason=shave_reason)
    zia_agenda.set_belief(base=week_road, pick=sun_road)
    beliefunit_x = beliefunit_shop(base=week_road, pick=church_road)
    zia_agenda.edit_fact_attr(road=shave_road, beliefunit=beliefunit_x)
    return zia_agenda


def get_agenda_base_time_example() -> AgendaUnit:
    sue_agenda = agendaunit_shop(_owner_id="Sue")
    sue_agenda.add_l1_fact(factunit_shop("casa"))
    return sue_agenda


def get_agenda_irrational_example() -> AgendaUnit:
    # this agenda has no conclusive intent because 2 pledge facts are in contradiction
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
    hatter_agenda.add_l1_fact(factunit_shop(egg_text))

    chicken_text = "chicken first"
    chicken_road = hatter_agenda.make_l1_road(chicken_text)
    hatter_agenda.add_l1_fact(factunit_shop(chicken_text))

    # set egg pledge is True when chicken first is False
    hatter_agenda.edit_fact_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_suff_fact_active=True,
    )

    # set chick pledge is True when egg first is False
    hatter_agenda.edit_fact_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_suff_fact_active=False,
    )

    return hatter_agenda


def get_assignment_agenda_example1():
    neo_agenda = agendaunit_shop("Neo")
    casa_text = "casa"
    casa_road = neo_agenda.make_l1_road(casa_text)
    floor_text = "mop floor"
    floor_road = neo_agenda.make_road(casa_road, floor_text)
    floor_fact = factunit_shop(floor_text, pledge=True)
    neo_agenda.add_fact(floor_fact, casa_road)
    neo_agenda.add_l1_fact(factunit_shop("unimportant"))

    status_text = "cleaniness status"
    status_road = neo_agenda.make_road(casa_road, status_text)
    neo_agenda.add_fact(factunit_shop(status_text), casa_road)

    clean_text = "clean"
    clean_road = neo_agenda.make_road(status_road, clean_text)
    neo_agenda.add_fact(factunit_shop(clean_text), status_road)
    neo_agenda.add_fact(factunit_shop("very_much"), clean_road)
    neo_agenda.add_fact(factunit_shop("moderately"), clean_road)
    neo_agenda.add_fact(factunit_shop("dirty"), status_road)

    floor_reason = reasonunit_shop(status_road)
    floor_reason.set_premise(premise=status_road)
    neo_agenda.edit_fact_attr(road=floor_road, reason=floor_reason)
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
    amos_agenda.add_l1_fact(factunit_shop(casa_text))
    amos_agenda.add_fact(factunit_shop(basket_text), casa_road)
    amos_agenda.add_fact(factunit_shop(b_full_text), basket_road)
    amos_agenda.add_fact(factunit_shop(b_smel_text), basket_road)
    amos_agenda.add_fact(factunit_shop(b_bare_text), basket_road)
    amos_agenda.add_fact(factunit_shop(b_fine_text), basket_road)
    amos_agenda.add_fact(factunit_shop(b_half_text), basket_road)
    amos_agenda.add_fact(factunit_shop(do_laundry_text, pledge=True), casa_road)

    # laundry requirement
    amos_agenda.edit_fact_attr(
        road=laundry_task_road, reason_base=basket_road, reason_premise=b_full_road
    )
    # laundry requirement
    amos_agenda.edit_fact_attr(
        road=laundry_task_road, reason_base=basket_road, reason_premise=b_smel_road
    )
    # assign Cali to task
    cali_assignunit = assignedunit_shop()
    cali_assignunit.set_suffidea(cali_text)
    amos_agenda.edit_fact_attr(road=laundry_task_road, assignedunit=cali_assignunit)
    # print(f"{basket_road=}")
    # print(f"{amos_agenda._real_id=}")
    amos_agenda.set_belief(base=basket_road, pick=b_full_road)

    return amos_agenda


def get_agenda_with_tuesday_cleaning_task() -> AgendaUnit:
    bob_agenda = agendaunit_shop("Bob")
    bob_agenda.set_time_hreg_facts(7)

    casa_text = "casa"
    casa_road = bob_agenda.make_l1_road(casa_text)
    laundry_text = "do_laundry"
    laundry_road = bob_agenda.make_road(casa_road, laundry_text)
    chill_text = "chill"
    chill_road = bob_agenda.make_road(casa_road, chill_text)
    bob_agenda.add_l1_fact(factunit_shop(casa_text))
    jajatime_road = bob_agenda.make_road(bob_agenda.make_l1_road("time"), "jajatime")
    bob_agenda.set_belief(jajatime_road, jajatime_road, 1064131200, 1064136133)

    bob_agenda.add_fact(factunit_shop(laundry_text, pledge=True), casa_road)
    bob_agenda.edit_fact_attr(
        road=laundry_road,
        reason_base=jajatime_road,
        reason_premise=jajatime_road,
        reason_premise_open=5760.0,
        reason_premise_nigh=5760.0,
        reason_premise_divisor=10080.0,
    )
    bob_agenda.add_fact(factunit_shop(chill_text, pledge=True), casa_road)
    bob_agenda.edit_fact_attr(
        road=chill_road,
        reason_base=jajatime_road,
        reason_premise=jajatime_road,
        reason_premise_open=5760.0,
        reason_premise_nigh=7160.0,
        reason_premise_divisor=10080.0,
    )
    # # print(f"{bob_agenda._factroot._beliefunits.values()=}")
    # laundry_reasonunit = bob_agenda.get_fact_obj(laundry_road).get_reasonunit(
    #     jajatime_road
    # )
    # laundry_premise = laundry_reasonunit.get_premise(jajatime_road)
    # # print(f"{laundry_reasonunit.base=} {laundry_premise=}")
    # bob_agenda.calc_agenda_metrics()
    # for x_factunit in bob_agenda._fact_dict.values():
    #     if x_factunit._label in [laundry_text]:
    # print(f"{x_factunit._label=} {x_factunit._begin=} {x_factunit._close=}")
    # print(f"{x_factunit._kids.keys()=}")
    # jaja_beliefheir = x_factunit._beliefheirs.get(jajatime_road)
    # print(f"{jaja_beliefheir.open % 10080=}")
    # print(f"{jaja_beliefheir.nigh % 10080=}")

    # print(f"{bob_agenda.get_intent_dict().keys()=}")

    return bob_agenda


# class YR:
def from_list_get_active(
    road: RoadUnit, fact_dict: dict, asse_bool: bool = None
) -> bool:
    active = None
    temp_fact = None

    active_true_count = 0
    active_false_count = 0
    for fact in fact_dict.values():
        if fact.get_road() == road:
            temp_fact = fact
            print(
                f"searched for FactUnit {temp_fact.get_road()} found {temp_fact._active=}"
            )

        if fact._active:
            active_true_count += 1
        elif fact._active is False:
            active_false_count += 1

    active = temp_fact._active
    print(
        f"Set active: {fact._label=} {active} {active_true_count=} {active_false_count=}"
    )

    if asse_bool in {True, False}:
        if active != asse_bool:
            yr_elucidation(temp_fact)

        assert active == asse_bool
    else:
        yr_elucidation(temp_fact)
    return active


def yr_print_fact_base_info(fact, filter: bool):
    for l in fact._reasonheirs.values():
        if l._status == filter:
            print(
                f"  ReasonHeir '{l.base}' Base LH:{l._status} W:{len(l.premises)}"  # \t_task {l._task}"
            )
            if str(type(fact)).find(".fact.FactUnit'>") > 0:
                yr_print_belief(
                    lh_base=l.base,
                    lh_status=l._status,
                    premises=l.premises,
                    beliefheirs=fact._beliefheirs,
                )


def yr_elucidation(fact):
    str1 = f"'{yr_d(fact._parent_road)}' fact"
    str2 = f" has ReasonU:{yr_x(fact._reasonunits)} LH:{yr_x(fact._reasonheirs)}"
    str3 = f" {str(type(fact))}"
    str4 = " "
    if str(type(fact)).find(".fact.FactUnit'>") > 0:
        str3 = f" Beliefs:{yr_x(fact._beliefheirs)} Status: {fact._active}"

        print(f"\n{str1}{str2}{str3}")
        hh_wo_matched_reason = []
        for hh in fact._beliefheirs.values():
            hh_wo_matched_reason = []
            try:
                fact._reasonheirs[hh.base]
            except Exception:
                hh_wo_matched_reason.append(hh.base)

        for base in hh_wo_matched_reason:
            print(f"Beliefs that don't matter to this Fact: {base}")

    # if fact._reasonunits != None:
    #     for lu in fact._reasonunits.values():
    #         print(f"  ReasonUnit   '{lu.base}' premises: {len(lu.premises)} ")
    if fact._reasonheirs != None:
        filter_x = True
        yr_print_fact_base_info(fact=fact, filter=True)

        filter_x = False
        print("\nReasons that failed:")

        for l in fact._reasonheirs.values():
            if l._status == filter_x:
                print(
                    f"  ReasonHeir '{l.base}' Base LH:{l._status} W:{len(l.premises)}"  # \t_task {l._task}"
                )
                if str(type(fact)).find(".fact.FactUnit'>") > 0:
                    yr_print_belief(
                        lh_base=l.base,
                        lh_status=l._status,
                        premises=l.premises,
                        beliefheirs=fact._beliefheirs,
                    )
                print("")
    # print(fact._beliefheirs)
    # print(f"{(fact._beliefheirs != None)=}")
    # print(f"{len(fact._beliefheirs)=} ")

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
