from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels_and_2reasons,
    get_agenda_with7amCleanTableReason,
    agenda_v001,
    from_list_get_active,
)
from src.agenda.idea import ideaunit_shop
from src.agenda.reason_idea import (
    premiseunit_shop,
    reasonunit_shop,
    reasonheir_shop,
)
from src.agenda.agenda import agendaunit_shop


def _check_all_objects_in_dict_are_correct_type(x_dict: dict, type_str: str) -> bool:
    bool_x = True
    for x_value in x_dict.values():
        if type_str not in str(type(x_value)):
            bool_x = False
        print(f"/t{type(x_value)=} {type_str=} {str(type(x_value)).find(type_str)=}")
    return bool_x


def test_agenda_idea_dict_isDictionaryAndIsFullyPopulated():
    # GIVEN
    x_agenda = get_agenda_with_4_levels_and_2reasons()

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    assert len(x_agenda._idea_dict) == 17


def test_agenda_get_idea_list_SetsSatiateStatusCorrectlyWhenBeliefSaysNo():
    # GIVEN
    x_agenda = get_agenda_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = x_agenda.make_road(week_road, sun_text)

    # WHEN
    x_agenda.set_belief(base=week_road, pick=sun_road)
    idea_list = x_agenda.get_idea_list()

    # THEN
    assert idea_list
    assert len(idea_list) == 17

    # for idea in x_agenda._idea_dict.values():
    #     print(f"{work_road=} {idea.get_road()=}")
    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)
    assert x_agenda._idea_dict.get(work_road)._active == False


def test_agenda_get_idea_list_SetsSatiateStatusCorrectlyWhenBeliefChanges():
    # GIVEN
    x_agenda = get_agenda_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    sun_text = "Wednesday"
    sun_road = x_agenda.make_road(week_road, sun_text)
    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)

    # WHEN
    x_agenda.set_belief(base=week_road, pick=sun_road)

    # THEN
    idea_list = x_agenda.get_idea_list()
    assert idea_list
    assert len(idea_list) == 17
    assert x_agenda._idea_dict.get(work_road)._active == False

    # WHEN
    states_text = "nation-state"
    states_road = x_agenda.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = x_agenda.make_road(states_road, usa_text)
    x_agenda.set_belief(base=states_road, pick=usa_road)

    # THEN
    idea_list = x_agenda.get_idea_list()
    assert idea_list
    assert len(idea_list) == 17
    assert x_agenda._idea_dict.get(work_road)._active

    # WHEN
    france_text = "France"
    france_road = x_agenda.make_road(states_road, france_text)
    x_agenda.set_belief(base=states_road, pick=france_road)

    # THEN
    idea_list = x_agenda.get_idea_list()
    assert idea_list
    assert len(idea_list) == 17
    assert x_agenda._idea_dict.get(work_road)._active == False


def test_agenda_get_idea_list_returns_correct_list():
    # GIVEN
    x_agenda = get_agenda_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = x_agenda.make_road(week_road, wed_text)
    state_text = "nation-state"
    state_road = x_agenda.make_l1_road(state_text)
    france_text = "France"
    france_road = x_agenda.make_road(state_road, france_text)
    x_agenda.set_belief(base=week_road, pick=wed_road)
    x_agenda.set_belief(base=state_road, pick=france_road)

    work_text = "work"
    work_road = x_agenda.make_l1_road(work_text)
    work_idea = x_agenda.get_idea_obj(work_road)
    print(f"{x_agenda._agent_id=} {len(work_idea._reasonunits)=}")
    # print(f"{work_idea._reasonunits=}")
    print(f"{x_agenda._agent_id=} {len(x_agenda._idearoot._beliefunits)=}")
    # print(f"{x_agenda._idearoot._beliefunits=}")

    idea_list = x_agenda.get_idea_list()
    assert idea_list
    assert len(idea_list) == 17

    usa_text = "USA"
    usa_road = x_agenda.make_road(state_road, usa_text)
    oregon_text = "Oregon"
    oregon_road = x_agenda.make_road(usa_road, oregon_text)

    wed = premiseunit_shop(need=wed_road)
    wed._status = True
    wed._task = False
    usa = premiseunit_shop(need=usa_road)
    usa._status = True
    usa._task = False

    wed_lu = reasonunit_shop(week_road, premises={wed.need: wed})
    sta_lu = reasonunit_shop(state_road, premises={usa.need: usa})
    wed_lh = reasonheir_shop(
        base=week_road,
        premises={wed.need: wed},
        _status=True,
        _task=False,
        _curr_idea_active=True,
    )
    sta_lh = reasonheir_shop(
        base=state_road,
        premises={usa.need: usa},
        _status=True,
        _task=False,
        _curr_idea_active=True,
    )

    x1_reasonunits = {
        wed_lu.base: wed_lu,
        sta_lu.base: sta_lu,
    }
    x1_reasonheirs = {
        wed_lh.base: wed_lh,
        sta_lh.base: sta_lh,
    }

    # WHEN
    x_agenda.set_belief(base=state_road, pick=oregon_road)

    # THEN
    work_idea = x_agenda._idea_dict.get(work_road)
    print(f"\nlook at {work_idea.get_road()=}")
    assert work_idea._parent_road == x_agenda._economy_id
    assert work_idea._kids == {}
    assert work_idea._weight == 30
    assert work_idea._label == work_text
    assert work_idea._level == 1
    assert work_idea._active
    assert work_idea.promise
    # print(f"{work_idea._reasonheirs=}")
    curr_reasonheir_state = work_idea._reasonheirs[state_road]
    print(f"  {curr_reasonheir_state=}")
    print(f"  {curr_reasonheir_state._status=}\n")
    # assert work_idea._reasonheirs == x1_reasonheirs

    assert len(work_idea._reasonheirs) == len(x1_reasonheirs)
    week_reasonheir = work_idea._reasonheirs.get(week_road)
    # usa_premise = week_reasonheir.premises.get(usa_road)
    print(f"    {work_idea._label=}")
    # print(f"    {usa_premise.base=}")
    # print(f"    {usa_premise._task=}")
    # print(f"    {usa_premise._task=}")
    assert week_reasonheir._task == False
    # print(f"      premises: {w=}")
    # w_need = usa_premise.premises[wed_road].need
    # print(f"      {w_need=}")
    # assert usa_premise._task == w_need._task
    # assert usa_premise._status == w_need._status
    # assert week_reasonheir.premises == week_reasonheir.premises

    # assert work_idea._reasonunits == x1_reasonunits

    # print("iterate through every idea...")
    # for curr_idea in idea_list:
    #     if str(type(curr_idea)).find(".idea.IdeaUnit'>") > 0:
    #         assert curr_idea._active != None

    #     # print("")
    #     # print(f"{curr_idea._label=}")
    #     # print(f"{len(curr_idea._reasonunits)=}")
    #     print(
    #         f"  {curr_idea._label} iterate through every reasonheir... {len(curr_idea._reasonheirs)=} {curr_idea._label=}"
    #     )
    #     # print(f"{curr_idea._reasonheirs=}")
    #     for reason in curr_idea._reasonheirs.values():
    #         assert str(type(reason)).find(".reason.ReasonHeir'>") > 0
    #         print(f"    {reason.base=}")
    #         assert reason._status != None
    #         for premise_x in reason.premises.values():
    #             assert premise_x._status != None
    #         assert _check_all_objects_in_dict_are_correct_type(
    #             x_dict=reason.premises, type_str="src.agenda.reason.PremiseUnit"
    #         )


def test_agenda_set_agenda_metrics_CorrectlyClears_agenda_coin():
    # GIVEN
    x_agenda = get_agenda_with7amCleanTableReason()
    work_road = x_agenda.make_l1_road("work")
    catt_road = x_agenda.make_l1_road("feed cat")
    week_road = x_agenda.make_l1_road("weekdays")
    x_agenda._idearoot._agenda_coin_onset = 13
    x_agenda._idearoot._agenda_coin_cease = 13
    x_agenda.get_idea_obj(work_road)._agenda_coin_onset = 13
    x_agenda.get_idea_obj(work_road)._agenda_coin_cease = 13
    x_agenda.get_idea_obj(catt_road)._agenda_coin_onset = 13
    x_agenda.get_idea_obj(catt_road)._agenda_coin_cease = 13
    x_agenda.get_idea_obj(week_road)._agenda_coin_onset = 13
    x_agenda.get_idea_obj(week_road)._agenda_coin_cease = 13

    assert x_agenda._idearoot._agenda_coin_onset == 13
    assert x_agenda._idearoot._agenda_coin_cease == 13
    assert x_agenda.get_idea_obj(work_road)._agenda_coin_onset == 13
    assert x_agenda.get_idea_obj(work_road)._agenda_coin_cease == 13
    assert x_agenda.get_idea_obj(catt_road)._agenda_coin_onset == 13
    assert x_agenda.get_idea_obj(catt_road)._agenda_coin_cease == 13
    assert x_agenda.get_idea_obj(week_road)._agenda_coin_onset == 13
    assert x_agenda.get_idea_obj(week_road)._agenda_coin_cease == 13

    # WHEN
    x_agenda.set_agenda_metrics()

    # THEN
    assert x_agenda._idearoot._agenda_coin_onset != 13
    assert x_agenda._idearoot._agenda_coin_cease != 13
    assert x_agenda.get_idea_obj(work_road)._agenda_coin_onset != 13
    assert x_agenda.get_idea_obj(work_road)._agenda_coin_cease != 13
    assert x_agenda.get_idea_obj(catt_road)._agenda_coin_onset != 13
    assert x_agenda.get_idea_obj(catt_road)._agenda_coin_cease != 13
    assert x_agenda.get_idea_obj(week_road)._agenda_coin_onset != 13
    assert x_agenda.get_idea_obj(week_road)._agenda_coin_cease != 13


def test_agenda_get_idea_list_CorrectlyCalculatesIdeaAttr_agenda_coin():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao", _weight=10)

    auto_text = "auto"
    auto_road = yao_agenda.make_l1_road(auto_text)
    auto_idea = ideaunit_shop(auto_text, _weight=10)
    yao_agenda.add_l1_idea(auto_idea)

    barn_text = "barn"
    barn_road = yao_agenda.make_l1_road(barn_text)
    barn_idea = ideaunit_shop(barn_text, _weight=60)
    yao_agenda.add_l1_idea(barn_idea)
    lamb_text = "lambs"
    lamb_road = yao_agenda.make_road(barn_road, lamb_text)
    lamb_idea = ideaunit_shop(lamb_text, _weight=1)
    yao_agenda.add_idea(lamb_idea, parent_road=barn_road)
    duck_text = "ducks"
    duck_road = yao_agenda.make_road(barn_road, duck_text)
    duck_idea = ideaunit_shop(duck_text, _weight=2)
    yao_agenda.add_idea(duck_idea, parent_road=barn_road)

    coal_text = "coal"
    coal_road = yao_agenda.make_l1_road(coal_text)
    coal_idea = ideaunit_shop(coal_text, _weight=30)
    yao_agenda.add_l1_idea(coal_idea)

    assert yao_agenda._idearoot._agenda_coin_onset is None
    assert yao_agenda._idearoot._agenda_coin_cease is None
    assert yao_agenda.get_idea_obj(auto_road)._agenda_coin_onset is None
    assert yao_agenda.get_idea_obj(auto_road)._agenda_coin_cease is None
    assert yao_agenda.get_idea_obj(barn_road)._agenda_coin_onset is None
    assert yao_agenda.get_idea_obj(barn_road)._agenda_coin_cease is None
    assert yao_agenda.get_idea_obj(coal_road)._agenda_coin_onset is None
    assert yao_agenda.get_idea_obj(coal_road)._agenda_coin_cease is None
    lamb_before = yao_agenda.get_idea_obj(road=lamb_road)
    assert lamb_before._agenda_coin_onset is None
    assert lamb_before._agenda_coin_cease is None
    duck_before = yao_agenda.get_idea_obj(road=duck_road)
    assert duck_before._agenda_coin_onset is None
    assert duck_before._agenda_coin_cease is None

    # WHEN
    yao_agenda.set_agenda_metrics()

    # THEN
    assert yao_agenda._idearoot._agenda_coin_onset == 0.0
    assert yao_agenda._idearoot._agenda_coin_cease == 1.0
    assert yao_agenda.get_idea_obj(auto_road)._agenda_coin_onset == 0.0
    assert yao_agenda.get_idea_obj(auto_road)._agenda_coin_cease == 0.1
    assert yao_agenda.get_idea_obj(barn_road)._agenda_coin_onset == 0.1
    assert yao_agenda.get_idea_obj(barn_road)._agenda_coin_cease == 0.7
    assert yao_agenda.get_idea_obj(coal_road)._agenda_coin_onset == 0.7
    assert yao_agenda.get_idea_obj(coal_road)._agenda_coin_cease == 1.0

    duck_after = yao_agenda.get_idea_obj(road=duck_road)
    assert duck_after._agenda_coin_onset == 0.1
    assert duck_after._agenda_coin_cease == 0.5
    lamb_after = yao_agenda.get_idea_obj(road=lamb_road)
    assert lamb_after._agenda_coin_onset == 0.5
    assert lamb_after._agenda_coin_cease == 0.7


def test_agenda_get_idea_list_without_root_CorrectlyCalculatesIdeaAttributes():
    # GIVEN
    x_agenda = get_agenda_with7amCleanTableReason()

    # WHEN
    idea_list_without_idearoot = x_agenda.get_idea_list_without_idearoot()
    idea_list_with_idearoot = x_agenda.get_idea_list()

    # THEN
    assert len(idea_list_without_idearoot) == 28
    assert len(idea_list_without_idearoot) + 1 == len(idea_list_with_idearoot)

    # for idea in x_agenda.get_idea_list_without_idearoot():
    #     assert str(type(idea)).find(".idea.IdeaUnit'>") > 0

    # for idea in x_agenda.get_idea_list_without_idearoot():
    #     print(f"{idea._label=}")


def test_agenda_get_idea_list_CorrectlyCalculatesRangeAttributes():
    # GIVEN
    x_agenda = get_agenda_with7amCleanTableReason()
    idea_list = x_agenda.get_idea_list()
    house_text = "housework"
    house_road = x_agenda.make_l1_road(house_text)
    clean_text = "clean table"
    clean_road = x_agenda.make_road(house_road, clean_text)
    assert x_agenda._idea_dict.get(clean_road)._active == False

    # set beliefs as midnight to 8am
    time_text = "timetech"
    time_road = x_agenda.make_l1_road(time_text)
    day24hr_text = "24hr day"
    day24hr_road = x_agenda.make_road(time_road, day24hr_text)
    day24hr_base = day24hr_road
    day24hr_pick = day24hr_road
    day24hr_open = 0.0
    day24hr_nigh = 8.0

    # WHEN
    x_agenda.set_belief(
        base=day24hr_base, pick=day24hr_pick, open=day24hr_open, nigh=day24hr_nigh
    )

    # THEN
    x_agenda.set_agenda_metrics()
    assert x_agenda._idea_dict.get(clean_road)._active

    # WHEN
    # set beliefs as 8am to 10am
    day24hr_open = 8.0
    day24hr_nigh = 10.0
    print(x_agenda._idearoot._beliefunits[day24hr_road])
    x_agenda.set_belief(
        base=day24hr_base, pick=day24hr_pick, open=day24hr_open, nigh=day24hr_nigh
    )
    print(x_agenda._idearoot._beliefunits[day24hr_road])
    print(x_agenda._idearoot._kids[house_text]._kids[clean_text]._reasonunits)
    # x_agenda._idearoot._kids["housework"]._kids[clean_text]._active = None

    # THEN
    x_agenda.set_agenda_metrics()
    assert x_agenda._idea_dict.get(clean_road)._active == False


def test_get_intent_dict():
    # GIVEN
    x_agenda = get_agenda_with_4_levels_and_2reasons()

    # WHEN
    promise_items = x_agenda.get_intent_dict()

    # THEN
    assert promise_items != None
    assert len(promise_items) > 0
    assert len(promise_items) == 1


def test_exammple_idea_list_HasCorrectData():
    x_agenda = agenda_v001()
    print(f"{x_agenda.get_reason_bases()=}")
    # day_hour = f"{x_agenda._economy_id},day_hour"
    # x_agenda.set_belief(base=day_hour, pick=day_hour, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = x_agenda.make_l1_road(day_min_text)
    x_agenda.set_belief(base=day_min_road, pick=day_min_road, open=0, nigh=1439)

    mood_text = "Moods"
    mood_road = x_agenda.make_l1_road(mood_text)
    x_agenda.set_belief(base=mood_road, pick=mood_road)
    print(f"{x_agenda.get_reason_bases()=}")

    yr_mon_text = "year_month"
    yr_mon_road = x_agenda.make_l1_road(yr_mon_text)
    x_agenda.set_belief(base=yr_mon_road, pick=yr_mon_road)
    inter_text = "Internet"
    inter_road = x_agenda.make_l1_road(inter_text)
    x_agenda.set_belief(base=inter_road, pick=inter_road)
    assert x_agenda != None
    # print(f"{x_agenda._agent_id=}")
    # print(f"{len(x_agenda._idearoot._kids)=}")
    ulty_text = "Ultimate Frisbee"
    ulty_road = x_agenda.make_l1_road(ulty_text)

    # if x_agenda._idearoot._kids["Ultimate Frisbee"]._label == "Ultimate Frisbee":
    assert x_agenda._idearoot._kids[ulty_text]._reasonunits != None
    assert x_agenda._agent_id != None

    # for belief in x_agenda._idearoot._beliefunits.values():
    #     print(f"{belief=}")

    idea_list = x_agenda.get_idea_list()
    # print(f"{str(type(idea))=}")
    # print(f"{len(idea_list)=}")
    laundry_text = "laundry monday"
    casa_road = x_agenda.make_l1_road("casa")
    cleaning_road = x_agenda.make_road(casa_road, "cleaning")
    laundry_road = x_agenda.make_road(cleaning_road, laundry_text)

    # for idea in idea_list:
    #     assert (
    #         str(type(idea)).find(".idea.IdeaUnit'>") > 0
    #         or str(type(idea)).find(".idea.IdeaUnit'>") > 0
    #     )
    #     # print(f"{idea._label=}")
    #     if idea._label == laundry_text:
    #         for reason in idea._reasonunits.values():
    #             print(f"{idea._label=} {reason.base=}")  # {reason.premises=}")
    # assert idea._active == False
    assert x_agenda._idea_dict.get(laundry_road)._active == False

    # WHEN
    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    mon_text = "Monday"
    mon_road = x_agenda.make_road(week_road, mon_text)
    x_agenda.set_belief(base=week_road, pick=mon_road)

    x_agenda.set_agenda_metrics()

    # THEN
    assert x_agenda._idea_dict.get(laundry_road)._active == False


def test_exammple_idea_list_OptionWeekdaysCorrectlyWork():
    # GIVEN
    x_agenda = agenda_v001()

    day_hr_text = "day_hour"
    day_hr_road = x_agenda.make_l1_road(day_hr_text)
    x_agenda.set_belief(base=day_hr_road, pick=day_hr_road, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = x_agenda.make_l1_road(day_min_text)
    x_agenda.set_belief(base=day_min_road, pick=day_min_road, open=0, nigh=59)
    mon_wk_text = "month_week"
    mon_wk_road = x_agenda.make_l1_road(mon_wk_text)
    x_agenda.set_belief(base=mon_wk_road, pick=mon_wk_road)
    nation_text = "Nation-States"
    nation_road = x_agenda.make_l1_road(nation_text)
    x_agenda.set_belief(base=nation_road, pick=nation_road)
    mood_text = "Moods"
    mood_road = x_agenda.make_l1_road(mood_text)
    x_agenda.set_belief(base=mood_road, pick=mood_road)
    aaron_text = "Aaron Donald things effected by him"
    aaron_road = x_agenda.make_l1_road(aaron_text)
    x_agenda.set_belief(base=aaron_road, pick=aaron_road)
    inter_text = "Internet"
    inter_road = x_agenda.make_l1_road(inter_text)
    x_agenda.set_belief(base=inter_road, pick=inter_road)
    yr_mon_text = "year_month"
    yr_mon_road = x_agenda.make_l1_road(yr_mon_text)
    x_agenda.set_belief(base=yr_mon_road, pick=yr_mon_road, open=0, nigh=1000)

    idea_list = x_agenda.get_idea_list()
    missing_beliefs = x_agenda.get_missing_belief_bases()
    # for missing_belief, count in missing_beliefs.items():
    #     print(f"{missing_belief=} {count=}")

    week_text = "weekdays"
    week_road = x_agenda.make_l1_road(week_text)
    mon_text = "Monday"
    mon_road = x_agenda.make_road(week_road, mon_text)
    tue_text = "Tuesday"
    tue_road = x_agenda.make_road(week_road, tue_text)
    mon_premise_x = premiseunit_shop(need=mon_road)
    mon_premise_x._status = False
    mon_premise_x._task = False
    tue_premise_x = premiseunit_shop(need=tue_road)
    tue_premise_x._status = False
    tue_premise_x._task = False
    mt_premises = {
        mon_premise_x.need: mon_premise_x,
        tue_premise_x.need: tue_premise_x,
    }
    mt_reasonunit = reasonunit_shop(week_road, premises=mt_premises)
    mt_reasonheir = reasonheir_shop(week_road, premises=mt_premises, _status=False)
    x_idearoot = x_agenda.get_idea_obj(x_agenda._economy_id)
    x_idearoot.set_reasonunit(reason=mt_reasonunit)
    # print(f"{x_agenda._reasonunits[week_road].base=}")
    # print(f"{x_agenda._reasonunits[week_road].premises[mon_road].need=}")
    # print(f"{x_agenda._reasonunits[week_road].premises[tue_road].need=}")
    week_reasonunit = x_idearoot._reasonunits[week_road]
    print(f"{week_reasonunit.premises=}")
    premise_mon = week_reasonunit.premises.get(mon_road)
    premise_tue = week_reasonunit.premises.get(tue_road)
    assert premise_mon
    assert premise_mon == mt_reasonunit.premises[premise_mon.need]
    assert premise_tue
    assert premise_tue == mt_reasonunit.premises[premise_tue.need]
    assert week_reasonunit == mt_reasonunit

    # WHEN
    idea_list = x_agenda.get_idea_list()

    # THEN
    gen_week_reasonheir = x_idearoot.get_reasonheir(week_road)
    gen_mon_premise = gen_week_reasonheir.premises.get(mon_road)
    assert gen_mon_premise._status == mt_reasonheir.premises.get(mon_road)._status
    assert gen_mon_premise == mt_reasonheir.premises.get(mon_road)
    assert gen_week_reasonheir.premises == mt_reasonheir.premises
    assert gen_week_reasonheir == mt_reasonheir

    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    bird_text = "say hi to birds"
    bird_road = x_agenda.make_road(casa_road, bird_text)
    assert from_list_get_active(road=bird_road, idea_list=idea_list) == False

    # x_agenda.set_belief(base=week_road, pick=mon_road)
    # idea_list = x_agenda.get_idea_list()
    # casa_idea = x_idearoot._kids[casa_text]
    # twee_idea = casa_idea._kids[bird_text]
    # print(f"{len(x_idearoot._reasonheirs)=}")
    # print(f"{len(casa_idea._reasonheirs)=}")
    # print(f"{len(twee_idea._reasonheirs)=}")

    # assert YR.get_active(road=bird_idea, idea_list=idea_list) == True

    # x_agenda.set_belief(base=f"{x_agenda._economy_id},weekdays", pick=f"{x_agenda._economy_id},weekdays,Tuesday")
    # idea_list = x_agenda.get_idea_list()
    # assert YR.get_active(road=bird_idea, idea_list=idea_list) == True

    # x_agenda.set_belief(base=f"{x_agenda._economy_id},weekdays", pick=f"{x_agenda._economy_id},weekdays,Wednesday")
    # idea_list = x_agenda.get_idea_list()
    # assert YR.get_active(road=bird_idea, idea_list=idea_list) == False


def test_exammple_idea_list_Every6WeeksReason():
    # GIVEN
    x_agenda = agenda_v001()
    day_text = "day_hour"
    day_road = x_agenda.make_l1_road(day_text)
    min_text = "day_minute"
    min_road = x_agenda.make_l1_road(day_text)

    # WHEN
    x_agenda.set_belief(base=day_road, pick=day_road, open=0, nigh=23)
    x_agenda.set_belief(base=min_road, pick=min_road, open=0, nigh=59)
    idea_list = x_agenda.get_idea_list()

    # THEN
    ced_week_base = x_agenda.make_l1_road("ced_week")

    premise_divisor = None
    premise_open = None
    premise_nigh = None
    print(f"{len(idea_list)=}")

    casa_road = x_agenda.make_l1_road("casa")
    cleaning_road = x_agenda.make_road(casa_road, "cleaning")
    clean_couch_road = x_agenda.make_road(cleaning_road, "clean sheets couch blankets")
    clean_sheet_idea = x_agenda.get_idea_obj(clean_couch_road)
    # print(f"{clean_sheet_idea._reasonunits.values()=}")
    ced_week_reason = clean_sheet_idea._reasonunits.get(ced_week_base)
    ced_week_premise = ced_week_reason.premises.get(ced_week_base)
    print(
        f"{clean_sheet_idea._label=} {ced_week_reason.base=} {ced_week_premise.need=}"
    )
    # print(f"{clean_sheet_idea._label=} {ced_week_reason.base=} {premise_x=}")
    premise_divisor = ced_week_premise.divisor
    premise_open = ced_week_premise.open
    premise_nigh = ced_week_premise.nigh
    # print(f"{idea._reasonunits=}")
    assert clean_sheet_idea._active == False

    # for idea in idea_list:
    #     # print(f"{idea._parent_road=}")
    #     if idea._label == "clean sheets couch blankets":
    #         print(f"{idea.get_road()=}")

    assert premise_divisor == 6
    assert premise_open == 1
    print(
        f"There exists a idea with a reason_base {ced_week_base} that also has lemmet div =6 and open/nigh =1"
    )
    # print(f"{len(idea_list)=}")
    ced_week_open = 6001

    # WHEN
    x_agenda.set_belief(
        base=ced_week_base, pick=ced_week_base, open=ced_week_open, nigh=ced_week_open
    )
    nation_text = "Nation-States"
    nation_road = x_agenda.make_l1_road(nation_text)
    x_agenda.set_belief(base=nation_road, pick=nation_road)
    print(
        f"Nation-states set and also belief set: {ced_week_base=} with {ced_week_open=} and {ced_week_open=}"
    )
    print(f"{x_agenda._idearoot._beliefunits=}")
    idea_list = x_agenda.get_idea_list()

    # THEN
    week_text = "ced_week"
    week_road = x_agenda.make_l1_road(week_text)
    casa_road = x_agenda.make_l1_road("casa")
    cleaning_road = x_agenda.make_road(casa_road, "cleaning")
    clean_couch_text = "clean sheets couch blankets"
    clean_couch_road = x_agenda.make_road(cleaning_road, clean_couch_text)
    clean_couch_idea = x_agenda.get_idea_obj(road=clean_couch_road)
    week_reason = clean_couch_idea._reasonunits.get(week_road)
    week_premise = week_reason.premises.get(week_road)
    print(f"{clean_couch_idea._label=} {week_reason.base=} {week_premise=}")
    assert week_premise.divisor == 6 and week_premise.open == 1


def print_premise_info(road: str, idea_list):
    satiate_status = None
    premise_divisor = None
    premise_open = None
    premise_nigh = None

    for idea in idea_list:
        if idea._parent_road == road:
            for reason in idea._reasonunits.values():
                for premise_x in reason.premises.values():
                    print(
                        f"{idea._label=} base:{reason.base} need:{premise_x.need} open:{premise_x.open} nigh:{premise_x.nigh} div:{premise_x.divisor} status:{premise_x._status}"
                    )


def test_exammple_idea_list_EveryIdeaHasSatiateStatus():
    # GIVEN
    x_agenda = agenda_v001()

    # WHEN
    idea_list = x_agenda.get_idea_list()

    # THEN
    print(f"{len(idea_list)=}")
    # first_idea_kid_count = 0
    # first_idea_kid_none_count = 0
    # first_idea_kid_true_count = 0
    # first_idea_kid_false_count = 0
    # for idea in idea_list:
    #     if str(type(idea)).find(".idea.IdeaUnit'>") > 0:
    #         first_idea_kid_count += 1
    #         if idea._active is None:
    #             first_idea_kid_none_count += 1
    #         elif idea._active:
    #             first_idea_kid_true_count += 1
    #         elif idea._active == False:
    #             first_idea_kid_false_count += 1

    # print(f"{first_idea_kid_count=}")
    # print(f"{first_idea_kid_none_count=}")
    # print(f"{first_idea_kid_true_count=}")
    # print(f"{first_idea_kid_false_count=}")

    # idea_kid_count = 0
    # for idea in idea_list_without_idearoot:
    #     idea_kid_count += 1
    #     print(f"{idea._label=} {idea_kid_count=}")
    #     assert idea._active != None
    #     assert idea._active in (True, False)
    # assert idea_kid_count == len(idea_list_without_idearoot)

    assert len(idea_list) == sum(idea._active != None for idea in idea_list)


def test_exammple_idea_list_EveryOtherMonthWorks():
    # GIVEN
    x_agenda = agenda_v001()
    minute_text = "day_minute"
    minute_road = x_agenda.make_l1_road(minute_text)
    x_agenda.set_belief(base=minute_road, pick=minute_road, open=0, nigh=1399)
    month_text = "month_week"
    month_road = x_agenda.make_l1_road(month_text)
    x_agenda.set_belief(base=month_road, pick=month_road)
    nations_text = "Nation-States"
    nations_road = x_agenda.make_l1_road(nations_text)
    x_agenda.set_belief(base=nations_road, pick=nations_road)
    mood_text = "Moods"
    mood_road = x_agenda.make_l1_road(mood_text)
    x_agenda.set_belief(base=mood_road, pick=mood_road)
    aaron_text = "Aaron Donald things effected by him"
    aaron_road = x_agenda.make_l1_road(aaron_text)
    x_agenda.set_belief(base=aaron_road, pick=aaron_road)
    internet_text = "Internet"
    internet_road = x_agenda.make_l1_road(internet_text)
    x_agenda.set_belief(base=internet_road, pick=internet_road)
    weekdays_text = "weekdays"
    weekdays_road = x_agenda.make_l1_road(weekdays_text)
    x_agenda.set_belief(base=weekdays_road, pick=weekdays_road)
    idea_list = x_agenda.get_idea_list()
    print(f"{len(idea_list)=}")

    casa_text = "casa"
    casa_road = x_agenda.make_l1_road(casa_text)
    clean_text = "cleaning"
    clean_road = x_agenda.make_road(casa_road, clean_text)
    mat_label = "deep clean play mat"
    mat_road = x_agenda.make_road(clean_road, mat_label)
    assert from_list_get_active(road=mat_road, idea_list=idea_list) == False

    year_month_base = x_agenda.make_l1_road("year_month")
    print(f"{year_month_base=}, {year_month_base=}")

    # WHEN
    x_agenda.set_belief(base=year_month_base, pick=year_month_base, open=0, nigh=8)
    ced_week = x_agenda.make_l1_road("ced_week")
    x_agenda.set_belief(base=ced_week, pick=ced_week, open=0, nigh=4)

    # THEN
    idea_list = x_agenda.get_idea_list()
    print(f"{len(idea_list)=}")
    print(f"{len(x_agenda._idearoot._beliefunits)=}")
    # from_list_get_active(road=mat_road, idea_list=idea_list)
    assert from_list_get_active(road=mat_road, idea_list=idea_list)
