from src.contract.x_func import from_list_get_active_status
from src.contract.examples.example_contracts import (
    get_contract_with_4_levels_and_2requireds,
    get_contract_with7amCleanTableRequired,
    contract_v001,
)
from src.contract.idea import IdeaKid
from src.contract.required_idea import sufffactunit_shop, RequiredUnit, RequiredHeir
from src.contract.road import Road
from src.contract.contract import ContractUnit


def _check_all_elements_in_dict_are_correct_type(x_dict: dict, type_str: str) -> bool:
    bool_x = True
    for x_value in x_dict.values():
        if type_str not in str(type(x_value)):
            bool_x = False
        print(f"/t{type(x_value)=} {type_str=} {str(type(x_value)).find(type_str)=}")
    return bool_x


def test_contract_yoke_dict_isDictionaryAndIsFullyPopulated():
    # GIVEN
    cx = get_contract_with_4_levels_and_2requireds()

    # WHEN
    cx.set_contract_metrics()

    # THEN
    assert len(cx._idea_dict) == 17


def test_contract_get_idea_list_SetsSatiateStatusCorrectlyWhenAcptFactSaysNo():
    # GIVEN
    cx = get_contract_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = f"{cx._healing_handle},{week_text}"
    sun_text = "Sunday"
    sun_road = f"{week_road},{sun_text}"

    # WHEN
    cx.set_acptfact(base=week_road, pick=sun_road)
    idea_list = cx.get_idea_list()

    # THEN
    assert idea_list
    assert len(idea_list) == 17

    # for idea in cx._idea_dict.values():
    #     print(f"{work_road=} {idea.get_road()=}")
    work_text = "work"
    work_road = f"{cx._healing_handle},{work_text}"
    assert cx._idea_dict.get(work_road)._active_status == False


def test_contract_get_idea_list_SetsSatiateStatusCorrectlyWhenAcptFactChanges():
    # GIVEN
    cx = get_contract_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = f"{cx._healing_handle},{week_text}"
    sun_text = "Wednesday"
    sun_road = f"{week_road},{sun_text}"
    work_text = "work"
    work_road = f"{cx._healing_handle},{work_text}"

    # WHEN
    cx.set_acptfact(base=week_road, pick=sun_road)

    # THEN
    idea_list = cx.get_idea_list()
    assert idea_list
    assert len(idea_list) == 17
    assert cx._idea_dict.get(work_road)._active_status == False

    # WHEN
    states_text = "nation-state"
    states_road = f"{cx._healing_handle},{states_text}"
    usa_text = "USA"
    usa_road = f"{states_road},{usa_text}"
    cx.set_acptfact(base=states_road, pick=usa_road)

    # THEN
    idea_list = cx.get_idea_list()
    assert idea_list
    assert len(idea_list) == 17
    assert cx._idea_dict.get(work_road)._active_status

    # WHEN
    france_text = "France"
    france_road = f"{states_road},{france_text}"
    cx.set_acptfact(base=states_road, pick=france_road)

    # THEN
    idea_list = cx.get_idea_list()
    assert idea_list
    assert len(idea_list) == 17
    assert cx._idea_dict.get(work_road)._active_status == False


def test_contract_get_idea_list_returns_correct_list():
    # GIVEN
    cx = get_contract_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = f"{cx._healing_handle},{week_text}"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"
    state_text = "nation-state"
    state_road = f"{cx._healing_handle},{state_text}"
    france_text = "France"
    france_road = f"{state_road},{france_text}"
    cx.set_acptfact(base=week_road, pick=wed_road)
    cx.set_acptfact(base=state_road, pick=france_road)

    work_text = "work"
    work_road = f"{cx._healing_handle},{work_text}"
    work_idea = cx.get_idea_kid(work_road)
    print(f"{cx._healer=} {len(work_idea._requiredunits)=}")
    # print(f"{work_idea._requiredunits=}")
    print(f"{cx._healer=} {len(cx._idearoot._acptfactunits)=}")
    # print(f"{cx._idearoot._acptfactunits=}")

    idea_list = cx.get_idea_list()
    assert idea_list
    assert len(idea_list) == 17

    usa_text = "USA"
    usa_road = f"{state_road},{usa_text}"
    oregon_text = "Oregon"
    oregon_road = f"{usa_road},{oregon_text}"

    wed = sufffactunit_shop(need=wed_road)
    wed._status = True
    wed._task = False
    usa = sufffactunit_shop(need=usa_road)
    usa._status = True
    usa._task = False

    wed_lu = RequiredUnit(base=week_road, sufffacts={wed.need: wed})
    sta_lu = RequiredUnit(base=state_road, sufffacts={usa.need: usa})
    wed_lh = RequiredHeir(
        base=week_road,
        sufffacts={wed.need: wed},
        _status=True,
        _task=False,
        _curr_idea_active_status=True,
    )
    sta_lh = RequiredHeir(
        base=state_road,
        sufffacts={usa.need: usa},
        _status=True,
        _task=False,
        _curr_idea_active_status=True,
    )

    x1_requiredunits = {
        wed_lu.base: wed_lu,
        sta_lu.base: sta_lu,
    }
    x1_requiredheirs = {
        wed_lh.base: wed_lh,
        sta_lh.base: sta_lh,
    }

    # WHEN
    cx.set_acptfact(base=state_road, pick=oregon_road)

    # THEN
    work_idea = cx._idea_dict.get(work_road)
    print(f"\nlook at {work_idea.get_road()=}")
    assert work_idea._walk == f"{cx._healing_handle}"
    assert work_idea._kids == {}
    assert work_idea._weight == 30
    assert work_idea._label == work_text
    assert work_idea._level == 1
    assert work_idea._active_status
    assert work_idea.promise
    # print(f"{work_idea._requiredheirs=}")
    curr_requiredheir_state = work_idea._requiredheirs[state_road]
    print(f"  {curr_requiredheir_state=}")
    print(f"  {curr_requiredheir_state._status=}\n")
    # assert work_idea._requiredheirs == x1_requiredheirs

    assert len(work_idea._requiredheirs) == len(x1_requiredheirs)
    week_requiredheir = work_idea._requiredheirs.get(week_road)
    # usa_sufffact = week_requiredheir.sufffacts.get(usa_road)
    print(f"    {work_idea._label=}")
    # print(f"    {usa_sufffact.base=}")
    # print(f"    {usa_sufffact._task=}")
    # print(f"    {usa_sufffact._task=}")
    assert week_requiredheir._task == False
    # print(f"      sufffacts: {w=}")
    # w_need = usa_sufffact.sufffacts[wed_road].need
    # print(f"      {w_need=}")
    # assert usa_sufffact._task == w_need._task
    # assert usa_sufffact._status == w_need._status
    # assert week_requiredheir.sufffacts == week_requiredheir.sufffacts

    # assert work_idea._requiredunits == x1_requiredunits

    # print("iterate through every idea...")
    # for curr_idea in idea_list:
    #     if str(type(curr_idea)).find(".idea.IdeaKid'>") > 0:
    #         assert curr_idea._active_status != None

    #     # print("")
    #     # print(f"{curr_idea._label=}")
    #     # print(f"{len(curr_idea._requiredunits)=}")
    #     print(
    #         f"  {curr_idea._label} iterate through every requiredheir... {len(curr_idea._requiredheirs)=} {curr_idea._label=}"
    #     )
    #     # print(f"{curr_idea._requiredheirs=}")
    #     for required in curr_idea._requiredheirs.values():
    #         assert str(type(required)).find(".required.RequiredHeir'>") > 0
    #         print(f"    {required.base=}")
    #         assert required._status != None
    #         for sufffact_x in required.sufffacts.values():
    #             assert sufffact_x._status != None
    #         assert _check_all_elements_in_dict_are_correct_type(
    #             x_dict=required.sufffacts, type_str="src.contract.required.SuffFactUnit"
    #         )


def test_contract_set_contract_metrics_CorrectlyClears_contract_coin():
    # GIVEN
    cx = get_contract_with7amCleanTableRequired()
    work_text = "work"
    catt_text = "feed cat"
    week_text = "weekdays"
    cx._idearoot._contract_coin_onset = 13
    cx._idearoot._contract_coin_cease = 13
    cx._idearoot._kids.get(work_text)._contract_coin_onset = 13
    cx._idearoot._kids.get(work_text)._contract_coin_cease = 13
    cx._idearoot._kids.get(catt_text)._contract_coin_onset = 13
    cx._idearoot._kids.get(catt_text)._contract_coin_cease = 13
    cx._idearoot._kids.get(week_text)._contract_coin_onset = 13
    cx._idearoot._kids.get(week_text)._contract_coin_cease = 13

    assert cx._idearoot._contract_coin_onset == 13
    assert cx._idearoot._contract_coin_cease == 13
    assert cx._idearoot._kids.get(work_text)._contract_coin_onset == 13
    assert cx._idearoot._kids.get(work_text)._contract_coin_cease == 13
    assert cx._idearoot._kids.get(catt_text)._contract_coin_onset == 13
    assert cx._idearoot._kids.get(catt_text)._contract_coin_cease == 13
    assert cx._idearoot._kids.get(week_text)._contract_coin_onset == 13
    assert cx._idearoot._kids.get(week_text)._contract_coin_cease == 13

    # WHEN
    cx.set_contract_metrics()

    # THEN
    assert cx._idearoot._contract_coin_onset != 13
    assert cx._idearoot._contract_coin_cease != 13
    assert cx._idearoot._kids.get(work_text)._contract_coin_onset != 13
    assert cx._idearoot._kids.get(work_text)._contract_coin_cease != 13
    assert cx._idearoot._kids.get(catt_text)._contract_coin_onset != 13
    assert cx._idearoot._kids.get(catt_text)._contract_coin_cease != 13
    assert cx._idearoot._kids.get(week_text)._contract_coin_onset != 13
    assert cx._idearoot._kids.get(week_text)._contract_coin_cease != 13


def test_contract_get_idea_list_CorrectlyCalculatesIdeaAttr_contract_coin():
    # GIVEN
    healer_text = "Yao"
    cx = ContractUnit(_healer=healer_text, _weight=10)

    auto_text = "auto"
    auto_idea = IdeaKid(_label=auto_text, _weight=10)
    cx.add_idea(idea_kid=auto_idea, walk=cx._healing_handle)

    barn_text = "barn"
    barn_road = f"{cx._healing_handle},{barn_text}"
    barn_idea = IdeaKid(_label=barn_text, _weight=60)
    cx.add_idea(idea_kid=barn_idea, walk=cx._healing_handle)
    lamb_text = "lambs"
    lamb_road = f"{barn_road},{lamb_text}"
    lamb_idea = IdeaKid(_label=lamb_text, _weight=1)
    cx.add_idea(idea_kid=lamb_idea, walk=barn_road)
    duck_text = "ducks"
    duck_road = f"{barn_road},{duck_text}"
    duck_idea = IdeaKid(_label=duck_text, _weight=2)
    cx.add_idea(idea_kid=duck_idea, walk=barn_road)

    coal_text = "coal"
    coal_idea = IdeaKid(_label=coal_text, _weight=30)
    cx.add_idea(idea_kid=coal_idea, walk=cx._healing_handle)

    assert cx._idearoot._contract_coin_onset is None
    assert cx._idearoot._contract_coin_cease is None
    assert cx._idearoot._kids.get(auto_text)._contract_coin_onset is None
    assert cx._idearoot._kids.get(auto_text)._contract_coin_cease is None
    assert cx._idearoot._kids.get(barn_text)._contract_coin_onset is None
    assert cx._idearoot._kids.get(barn_text)._contract_coin_cease is None
    assert cx._idearoot._kids.get(coal_text)._contract_coin_onset is None
    assert cx._idearoot._kids.get(coal_text)._contract_coin_cease is None
    lamb_before = cx.get_idea_kid(road=lamb_road)
    assert lamb_before._contract_coin_onset is None
    assert lamb_before._contract_coin_cease is None
    duck_before = cx.get_idea_kid(road=duck_road)
    assert duck_before._contract_coin_onset is None
    assert duck_before._contract_coin_cease is None

    # WHEN
    cx.set_contract_metrics()

    # THEN
    assert cx._idearoot._contract_coin_onset == 0.0
    assert cx._idearoot._contract_coin_cease == 1.0
    assert cx._idearoot._kids.get(auto_text)._contract_coin_onset == 0.0
    assert cx._idearoot._kids.get(auto_text)._contract_coin_cease == 0.1
    assert cx._idearoot._kids.get(barn_text)._contract_coin_onset == 0.1
    assert cx._idearoot._kids.get(barn_text)._contract_coin_cease == 0.7
    assert cx._idearoot._kids.get(coal_text)._contract_coin_onset == 0.7
    assert cx._idearoot._kids.get(coal_text)._contract_coin_cease == 1.0

    duck_after = cx.get_idea_kid(road=duck_road)
    assert duck_after._contract_coin_onset == 0.1
    assert duck_after._contract_coin_cease == 0.5
    lamb_after = cx.get_idea_kid(road=lamb_road)
    assert lamb_after._contract_coin_onset == 0.5
    assert lamb_after._contract_coin_cease == 0.7


def test_contract_get_idea_list_without_root_CorrectlyCalculatesIdeaAttributes():
    # GIVEN
    cx = get_contract_with7amCleanTableRequired()

    # WHEN
    idea_list_without_idearoot = cx.get_idea_list_without_idearoot()
    idea_list_with_idearoot = cx.get_idea_list()

    # THEN
    assert len(idea_list_without_idearoot) == 28
    assert len(idea_list_without_idearoot) + 1 == len(idea_list_with_idearoot)

    # for idea in cx.get_idea_list_without_idearoot():
    #     assert str(type(idea)).find(".idea.IdeaKid'>") > 0

    # for idea in cx.get_idea_list_without_idearoot():
    #     print(f"{idea._label=}")


def test_contract_get_idea_list_CorrectlyCalculatesRangeAttributes():
    # GIVEN
    cx = get_contract_with7amCleanTableRequired()
    idea_list = cx.get_idea_list()
    house_text = "housework"
    house_road = f"{cx._healing_handle},{house_text}"
    clean_text = "clean table"
    clean_road = f"{house_road},{clean_text}"
    assert cx._idea_dict.get(clean_road)._active_status == False

    # set acptfacts as midnight to 8am
    time_text = "timetech"
    time_road = f"{cx._healing_handle},{time_text}"
    day24hr_text = "24hr day"
    day24hr_road = f"{time_road},{day24hr_text}"
    day24hr_base = day24hr_road
    day24hr_pick = day24hr_road
    day24hr_open = 0.0
    day24hr_nigh = 8.0

    # WHEN
    cx.set_acptfact(
        base=day24hr_base, pick=day24hr_pick, open=day24hr_open, nigh=day24hr_nigh
    )

    # THEN
    cx.set_contract_metrics()
    assert cx._idea_dict.get(clean_road)._active_status

    # WHEN
    # set acptfacts as 8am to 10am
    day24hr_open = 8.0
    day24hr_nigh = 10.0
    print(cx._idearoot._acptfactunits[day24hr_road])
    cx.set_acptfact(
        base=day24hr_base, pick=day24hr_pick, open=day24hr_open, nigh=day24hr_nigh
    )
    print(cx._idearoot._acptfactunits[day24hr_road])
    print(cx._idearoot._kids[house_text]._kids[clean_text]._requiredunits)
    # cx._idearoot._kids["housework"]._kids[clean_text]._active_status = None

    # THEN
    cx.set_contract_metrics()
    assert cx._idea_dict.get(clean_road)._active_status == False


def test_get_agenda_items():
    # GIVEN
    cx = get_contract_with_4_levels_and_2requireds()

    # WHEN
    promise_items = cx.get_agenda_items()

    # THEN
    assert promise_items != None
    assert len(promise_items) > 0
    assert len(promise_items) == 1


def test_exammple_idea_list_HasCorrectData():
    cx = contract_v001()
    print(f"{cx.get_required_bases()=}")
    # day_hour = f"{cx._healing_handle},day_hour"
    # cx.set_acptfact(base=day_hour, pick=day_hour, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = f"{cx._healing_handle},{day_min_text}"
    cx.set_acptfact(base=day_min_road, pick=day_min_road, open=0, nigh=1439)

    mood_text = "Moods"
    mood_road = f"{cx._healing_handle},{mood_text}"
    cx.set_acptfact(base=mood_road, pick=mood_road)
    print(f"{cx.get_required_bases()=}")

    yr_mon_text = "year_month"
    yr_mon_road = f"{cx._healing_handle},{yr_mon_text}"
    cx.set_acptfact(base=yr_mon_road, pick=yr_mon_road)
    inter_text = "Internet"
    inter_road = f"{cx._healing_handle},{inter_text}"
    cx.set_acptfact(base=inter_road, pick=inter_road)
    assert cx != None
    # print(f"{cx._healer=}")
    # print(f"{len(cx._idearoot._kids)=}")
    ulty_text = "Ultimate Frisbee"
    ulty_road = f"{cx._healing_handle},{ulty_text}"

    # if cx._idearoot._kids["Ultimate Frisbee"]._label == "Ultimate Frisbee":
    assert cx._idearoot._kids[ulty_text]._requiredunits != None
    assert cx._healer != None

    # for acptfact in cx._idearoot._acptfactunits.values():
    #     print(f"{acptfact=}")

    idea_list = cx.get_idea_list()
    # print(f"{str(type(idea))=}")
    # print(f"{len(idea_list)=}")
    laundry_text = "laundry monday"
    laundry_road = f"{cx._healing_handle},casa,cleaning,{laundry_text}"

    # for idea in idea_list:
    #     assert (
    #         str(type(idea)).find(".idea.IdeaRoot'>") > 0
    #         or str(type(idea)).find(".idea.IdeaKid'>") > 0
    #     )
    #     # print(f"{idea._label=}")
    #     if idea._label == laundry_text:
    #         for required in idea._requiredunits.values():
    #             print(f"{idea._label=} {required.base=}")  # {required.sufffacts=}")
    # assert idea._active_status == False
    assert cx._idea_dict.get(laundry_road)._active_status == False

    # WHEN
    week_text = "weekdays"
    week_road = f"{cx._healing_handle},{week_text}"
    mon_text = "Monday"
    mon_road = f"{week_road},{mon_text}"
    cx.set_acptfact(base=week_road, pick=mon_road)

    cx.set_contract_metrics()

    # THEN
    assert cx._idea_dict.get(laundry_road)._active_status == False


def test_exammple_idea_list_OptionWeekdaysCorrectlyWork():
    # GIVEN
    cx = contract_v001()

    day_hr_text = "day_hour"
    day_hr_road = f"{cx._healing_handle},{day_hr_text}"
    cx.set_acptfact(base=day_hr_road, pick=day_hr_road, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = f"{cx._healing_handle},{day_min_text}"
    cx.set_acptfact(base=day_min_road, pick=day_min_road, open=0, nigh=59)
    mon_wk_text = "month_week"
    mon_wk_road = f"{cx._healing_handle},{mon_wk_text}"
    cx.set_acptfact(base=mon_wk_road, pick=mon_wk_road)
    nation_text = "Nation-States"
    nation_road = f"{cx._healing_handle},{nation_text}"
    cx.set_acptfact(base=nation_road, pick=nation_road)
    mood_text = "Moods"
    mood_road = f"{cx._healing_handle},{mood_text}"
    cx.set_acptfact(base=mood_road, pick=mood_road)
    aaron_text = "Aaron Donald sphere"
    aaron_road = f"{cx._healing_handle},{aaron_text}"
    cx.set_acptfact(base=aaron_road, pick=aaron_road)
    inter_text = "Internet"
    inter_road = f"{cx._healing_handle},{inter_text}"
    cx.set_acptfact(base=inter_road, pick=inter_road)
    yr_mon_text = "year_month"
    yr_mon_road = f"{cx._healing_handle},{yr_mon_text}"
    cx.set_acptfact(base=yr_mon_road, pick=yr_mon_road, open=0, nigh=1000)

    idea_list = cx.get_idea_list()
    missing_acptfacts = cx.get_missing_acptfact_bases()
    # for missing_acptfact, count in missing_acptfacts.items():
    #     print(f"{missing_acptfact=} {count=}")

    week_road = f"{cx._healing_handle},weekdays"
    mon_road = f"{week_road},Monday"
    tue_road = f"{week_road},Tuesday"
    mon_sufffact_x = sufffactunit_shop(need=mon_road)
    tue_sufffact_x = sufffactunit_shop(need=tue_road)
    mt_sufffacts = {
        mon_sufffact_x.need: mon_sufffact_x,
        tue_sufffact_x.need: tue_sufffact_x,
    }
    mt_required = RequiredUnit(base=week_road, sufffacts=mt_sufffacts)
    mt_required_x = RequiredHeir(base=week_road, sufffacts=mt_sufffacts)
    cx._idearoot.set_required_unit(required=mt_required)
    # print(f"{cx._requiredunits[week_road].base=}")
    # print(f"{cx._requiredunits[week_road].sufffacts[mon_road].need=}")
    # print(f"{cx._requiredunits[week_road].sufffacts[tue_road].need=}")
    print(f"{cx._idearoot._requiredunits[week_road].sufffacts=}")
    sufffact_mon = cx._idearoot._requiredunits[week_road].sufffacts.get(mon_road)
    sufffact_tue = cx._idearoot._requiredunits[week_road].sufffacts.get(tue_road)
    assert sufffact_mon
    assert sufffact_mon == mt_required.sufffacts[sufffact_mon.need]
    assert sufffact_tue
    assert sufffact_tue == mt_required.sufffacts[sufffact_tue.need]
    assert cx._idearoot._requiredunits[week_road] == mt_required

    # WHEN
    idea_list = cx.get_idea_list()

    # THEN
    assert sufffact_mon
    assert sufffact_mon == mt_required.sufffacts[sufffact_mon.need]
    assert sufffact_tue
    assert sufffact_tue == mt_required.sufffacts[sufffact_tue.need]

    assert cx._idearoot._requiredheirs[week_road] == mt_required_x

    casa_text = "casa"
    casa_road = f"{cx._healing_handle},{casa_text}"
    bird_text = "say hi to birds"
    bird_road = Road(f"{casa_road},{bird_text}")
    assert from_list_get_active_status(road=bird_road, idea_list=idea_list) == False

    cx.set_acptfact(base=week_road, pick=mon_road)
    idea_list = cx.get_idea_list()
    casa_idea = cx._idearoot._kids[casa_text]
    twee_idea = casa_idea._kids[bird_text]
    print(f"{len(cx._idearoot._requiredheirs)=}")
    print(f"{len(casa_idea._requiredheirs)=}")
    print(f"{len(twee_idea._requiredheirs)=}")

    # assert YR.get_active_status(road=bird_idea, idea_list=idea_list) == True

    # cx.set_acptfact(base=f"{cx._healing_handle},weekdays", pick=f"{cx._healing_handle},weekdays,Tuesday")
    # idea_list = cx.get_idea_list()
    # assert YR.get_active_status(road=bird_idea, idea_list=idea_list) == True

    # cx.set_acptfact(base=f"{cx._healing_handle},weekdays", pick=f"{cx._healing_handle},weekdays,Wednesday")
    # idea_list = cx.get_idea_list()
    # assert YR.get_active_status(road=bird_idea, idea_list=idea_list) == False


def test_exammple_idea_list_Every6WeeksRequired():
    # GIVEN
    cx = contract_v001()
    day_text = "day_hour"
    day_road = f"{cx._healing_handle},{day_text}"
    min_text = "day_minute"
    min_road = f"{cx._healing_handle},{day_text}"

    # WHEN
    cx.set_acptfact(base=day_road, pick=day_road, open=0, nigh=23)
    cx.set_acptfact(base=min_road, pick=min_road, open=0, nigh=59)
    idea_list = cx.get_idea_list()

    # THEN
    ced_week_base = f"{cx._healing_handle},ced_week"

    sufffact_divisor = None
    sufffact_open = None
    sufffact_nigh = None
    print(f"{len(idea_list)=}")

    clean_sheet_road = f"{cx._healing_handle},casa,cleaning,clean sheets couch blankets"
    clean_sheet_idea = cx.get_idea_kid(road=clean_sheet_road)
    # print(f"{clean_sheet_idea._requiredunits.values()=}")
    ced_week_required = clean_sheet_idea._requiredunits.get(ced_week_base)
    ced_week_suffact = ced_week_required.sufffacts.get(ced_week_base)
    print(
        f"{clean_sheet_idea._label=} {ced_week_required.base=} {ced_week_suffact.need=}"
    )
    # print(f"{clean_sheet_idea._label=} {ced_week_required.base=} {sufffact_x=}")
    sufffact_divisor = ced_week_suffact.divisor
    sufffact_open = ced_week_suffact.open
    sufffact_nigh = ced_week_suffact.nigh
    # print(f"{idea._requiredunits=}")
    assert clean_sheet_idea._active_status == False

    # for idea in idea_list:
    #     # print(f"{idea._walk=}")
    #     if idea._label == "clean sheets couch blankets":
    #         print(f"{idea.get_road()=}")

    assert sufffact_divisor == 6
    assert sufffact_open == 1
    print(
        "There exists a idea with a required_base TlME,ced_week that also has lemmet div =6 and open/nigh =1"
    )
    # print(f"{len(idea_list)=}")
    ced_week_open = 6001

    # WHEN
    cx.set_acptfact(
        base=ced_week_base, pick=ced_week_base, open=ced_week_open, nigh=ced_week_open
    )
    nation_text = "Nation-States"
    nation_road = f"{cx._healing_handle},{nation_text}"
    cx.set_acptfact(base=nation_road, pick=nation_road)
    print(
        f"Nation-states set and also acptfact set: {ced_week_base=} with {ced_week_open=} and {ced_week_open=}"
    )
    print(f"{cx._idearoot._acptfactunits=}")
    idea_list = cx.get_idea_list()

    # THEN
    week_text = "ced_week"
    week_road = f"{cx._healing_handle},{week_text}"
    clean_couch_text = "clean sheets couch blankets"
    clean_couch_road = f"{cx._healing_handle},casa,cleaning,{clean_couch_text}"
    clean_couch_idea = cx.get_idea_kid(road=clean_couch_road)
    week_required = clean_couch_idea._requiredunits.get(week_road)
    week_sufffact = week_required.sufffacts.get(week_road)
    print(f"{clean_couch_idea._label=} {week_required.base=} {week_sufffact=}")
    assert week_sufffact.divisor == 6 and week_sufffact.open == 1


def print_sufffact_info(road: str, idea_list):
    satiate_status = None
    sufffact_divisor = None
    sufffact_open = None
    sufffact_nigh = None

    for idea in idea_list:
        if idea._walk == road:
            for required in idea._requiredunits.values():
                for sufffact_x in required.sufffacts.values():
                    print(
                        f"{idea._label=} base:{required.base} need:{sufffact_x.need} open:{sufffact_x.open} nigh:{sufffact_x.nigh} div:{sufffact_x.divisor} status:{sufffact_x._status}"
                    )


def test_exammple_idea_list_EveryIdeaHasSatiateStatus():
    # GIVEN
    cx = contract_v001()

    # WHEN
    idea_list = cx.get_idea_list()

    # THEN
    print(f"{len(idea_list)=}")
    # first_idea_kid_count = 0
    # first_idea_kid_none_count = 0
    # first_idea_kid_true_count = 0
    # first_idea_kid_false_count = 0
    # for idea in idea_list:
    #     if str(type(idea)).find(".idea.IdeaKid'>") > 0:
    #         first_idea_kid_count += 1
    #         if idea._active_status is None:
    #             first_idea_kid_none_count += 1
    #         elif idea._active_status:
    #             first_idea_kid_true_count += 1
    #         elif idea._active_status == False:
    #             first_idea_kid_false_count += 1

    # print(f"{first_idea_kid_count=}")
    # print(f"{first_idea_kid_none_count=}")
    # print(f"{first_idea_kid_true_count=}")
    # print(f"{first_idea_kid_false_count=}")

    # idea_kid_count = 0
    # for idea in idea_list_without_idearoot:
    #     idea_kid_count += 1
    #     print(f"{idea._label=} {idea_kid_count=}")
    #     assert idea._active_status != None
    #     assert idea._active_status in (True, False)
    # assert idea_kid_count == len(idea_list_without_idearoot)

    assert len(idea_list) - 1 == sum(idea._active_status != None for idea in idea_list)
    assert 1 == sum(idea._active_status is None for idea in idea_list)


def test_exammple_idea_list_EveryOtherMonthWorks():
    # GIVEN
    cx = contract_v001()
    minute_text = "day_minute"
    minute_road = f"{cx._healing_handle},{minute_text}"
    cx.set_acptfact(base=minute_road, pick=minute_road, open=0, nigh=1399)
    month_text = "month_week"
    month_road = f"{cx._healing_handle},{month_text}"
    cx.set_acptfact(base=month_road, pick=month_road)
    nations_text = "Nation-States"
    nations_road = f"{cx._healing_handle},{nations_text}"
    cx.set_acptfact(base=nations_road, pick=nations_road)
    mood_text = "Moods"
    mood_road = f"{cx._healing_handle},{mood_text}"
    cx.set_acptfact(base=mood_road, pick=mood_road)
    aaron_text = "Aaron Donald sphere"
    aaron_road = f"{cx._healing_handle},{aaron_text}"
    cx.set_acptfact(base=aaron_road, pick=aaron_road)
    internet_text = "Internet"
    internet_road = f"{cx._healing_handle},{internet_text}"
    cx.set_acptfact(base=internet_road, pick=internet_road)
    weekdays_text = "weekdays"
    weekdays_road = f"{cx._healing_handle},{weekdays_text}"
    cx.set_acptfact(base=weekdays_road, pick=weekdays_road)
    idea_list = cx.get_idea_list()
    print(f"{len(idea_list)=}")

    casa_text = "casa"
    casa_road = f"{cx._healing_handle},{casa_text}"
    clean_text = "cleaning"
    clean_road = f"{casa_road},{clean_text}"
    mat_label = "deep clean play mat"
    mat_road = Road(f"{clean_road},{mat_label}")
    # commented out since it's difficult to understand
    assert from_list_get_active_status(road=mat_road, idea_list=idea_list) == False

    year_month_base = f"{cx._healing_handle},year_month"
    print(f"{year_month_base=}, {year_month_base=}")

    # WHEN
    cx.set_acptfact(base=year_month_base, pick=year_month_base, open=0, nigh=8)
    ced_week = f"{cx._healing_handle},ced_week"
    cx.set_acptfact(base=ced_week, pick=ced_week, open=0, nigh=4)

    # THEN
    idea_list = cx.get_idea_list()
    print(f"{len(idea_list)=}")
    print(f"{len(cx._idearoot._acptfactunits)=}")
    # from_list_get_active_status(road=mat_road, idea_list=idea_list)
    assert from_list_get_active_status(road=mat_road, idea_list=idea_list)
