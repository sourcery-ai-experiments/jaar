from lib.agent.x_func import from_list_get_active_status
from lib.agent.test_agent.example_agents import (
    get_agent_with_4_levels_and_2requireds,
    get_agent_with7amCleanTableRequired,
    agent_v001,
)
from lib.agent.idea import IdeaKid
from lib.agent.required import sufffactunit_shop, RequiredUnit, RequiredHeir
from lib.agent.road import Road
from lib.agent.agent import AgentUnit


def test_agent_yoke_dict_isDictionaryAndIsFullyPopulated():
    # GIVEN
    agent_x = get_agent_with_4_levels_and_2requireds()

    # WHEN
    agent_x.set_agent_metrics()

    # THEN
    assert len(agent_x._idea_dict) == 17


def test_agent_get_idea_list_SetsSatiateStatusCorrectlyWhenAcptFactSaysNo():
    # GIVEN
    agent_x = get_agent_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = f"{agent_x._desc},{week_text}"
    sun_text = "Sunday"
    sun_road = f"{week_road},{sun_text}"

    # WHEN
    agent_x.set_acptfact(base=week_road, pick=sun_road)
    idea_list = agent_x.get_idea_list()

    # THEN
    assert idea_list
    assert len(idea_list) == 17
    for curr_idea in idea_list:
        if curr_idea._desc == "Work":
            assert curr_idea._active_status == False


def test_agent_get_idea_list_SetsSatiateStatusCorrectlyWhenAcptFactChanges():
    # GIVEN
    agent_x = get_agent_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = f"{agent_x._desc},{week_text}"
    sun_text = "Wednesday"
    sun_road = f"{week_road},{sun_text}"
    work_text = "Work"

    # WHEN
    agent_x.set_acptfact(base=week_road, pick=sun_road)

    # THEN
    idea_list = agent_x.get_idea_list()
    assert idea_list
    assert len(idea_list) == 17
    for curr_idea in idea_list:
        if curr_idea._desc == work_text:
            assert curr_idea._active_status == False

    # WHEN
    states_text = "nation-state"
    states_road = f"{agent_x._desc},{states_text}"
    usa_text = "USA"
    usa_road = f"{states_road},{usa_text}"
    agent_x.set_acptfact(base=states_road, pick=usa_road)

    # THEN
    idea_list = agent_x.get_idea_list()
    assert idea_list
    assert len(idea_list) == 17
    for curr_idea in idea_list:
        if curr_idea._desc == work_text:
            assert curr_idea._active_status == True

    # WHEN
    france_text = "France"
    france_road = f"{states_road},{france_text}"
    agent_x.set_acptfact(base=states_road, pick=france_road)

    # THEN
    idea_list = agent_x.get_idea_list()
    assert idea_list
    assert len(idea_list) == 17
    for curr_idea in idea_list:
        if curr_idea._desc == work_text:
            assert curr_idea._active_status == False


def test_agent_get_idea_list_returns_correct_list():
    # GIVEN
    agent_x = get_agent_with_4_levels_and_2requireds()
    week_text = "weekdays"
    week_road = f"{agent_x._desc},{week_text}"
    wed_text = "Wednesday"
    wed_road = f"{week_road},{wed_text}"
    state_text = "nation-state"
    state_road = f"{agent_x._desc},{state_text}"
    france_text = "France"
    france_road = f"{state_road},{france_text}"
    agent_x.set_acptfact(base=week_road, pick=wed_road)
    agent_x.set_acptfact(base=state_road, pick=france_road)

    work_text = "work"
    work_road = f"{agent_x._desc},{work_text}"
    work_idea = agent_x.get_idea_kid(work_road)
    print(f"{agent_x._desc=} {len(work_idea._requiredunits)=}")
    # print(f"{work_idea._requiredunits=}")
    print(f"{agent_x._desc=} {len(agent_x._idearoot._acptfactunits)=}")
    # print(f"{agent_x._idearoot._acptfactunits=}")

    idea_list = agent_x.get_idea_list()
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
    agent_x.set_acptfact(base=state_road, pick=oregon_road)

    # THEN
    temp_idea = IdeaKid(
        _walk=f"{agent_x._desc}",
        _kids=None,
        _weight=30,
        _desc=work_text,
        _level=1,
        _requiredunits=x1_requiredunits,
        _requiredheirs=x1_requiredheirs,
        _active_status=True,
        promise=True,
    )

    print("iterate through every idea...")
    for curr_idea in idea_list:
        if str(type(curr_idea)).find(".idea.IdeaKid'>") > 0:
            assert curr_idea._active_status != None

        # print("")
        # print(f"{curr_idea._desc=}")
        # print(f"{len(curr_idea._requiredunits)=}")
        print(
            f"  iterate through every requiredheir... {len(curr_idea._requiredheirs)=} {curr_idea._desc=}"
        )
        # print(f"{curr_idea._requiredheirs=}")
        for required in curr_idea._requiredheirs.values():
            assert str(type(required)).find(".required.RequiredHeir'>") > 0
            print(f"    {required.base=}")
            assert required._status != None
            for sufffact_x in required.sufffacts.values():
                assert sufffact_x._status != None

        if curr_idea._desc == temp_idea._desc:
            # print(idea)
            print(f"\nlook at {curr_idea.get_road()=}")
            assert curr_idea._desc == temp_idea._desc
            assert curr_idea._walk == temp_idea._walk
            # print(f"{curr_idea._requiredheirs=}")
            curr_requiredheir_state = curr_idea._requiredheirs[state_road]
            print(f"  {curr_requiredheir_state=}")
            print(f"  {curr_requiredheir_state._status=}\n")
            # print("temp_idea._requiredheirs")
            temp_requiredheir_state = temp_idea._requiredheirs[state_road]
            # print(f"{temp_idea._requiredheirs=}")
            print(f"  {temp_requiredheir_state=}")
            print(f"  {temp_requiredheir_state._status=}\n")
            assert len(curr_idea._requiredheirs) == len(temp_idea._requiredheirs)
            for lh in curr_idea._requiredheirs.values():
                print(f"    {curr_idea._desc=}")
                print(f"    {lh.base=}")
                print(f"    {lh._task=}")
                temp_idea_rh_lh_base = temp_idea._requiredheirs[lh.base]
                print(f"    {temp_idea_rh_lh_base._task=}")

                assert lh._task == temp_idea_rh_lh_base._task
                for w in lh.sufffacts.values():
                    print(f"      sufffacts: {w=}")
                    w_need = temp_idea_rh_lh_base.sufffacts[w.need]
                    print(f"      {w_need=}")
                    assert w._task == w_need._task
                    assert w._status == w_need._status
                assert lh.sufffacts == temp_idea_rh_lh_base.sufffacts
            assert curr_idea._requiredheirs == temp_idea._requiredheirs


def test_agent_set_agent_metrics_CorrectlyClears_agent_coin():
    # GIVEN
    ax = get_agent_with7amCleanTableRequired()
    src_text = "src"
    work_text = "work"
    catt_text = "feed cat"
    week_text = "weekdays"
    ax._idearoot._agent_coin_onset = 13
    ax._idearoot._agent_coin_cease = 13
    ax._idearoot._kids.get(work_text)._agent_coin_onset = 13
    ax._idearoot._kids.get(work_text)._agent_coin_cease = 13
    ax._idearoot._kids.get(catt_text)._agent_coin_onset = 13
    ax._idearoot._kids.get(catt_text)._agent_coin_cease = 13
    ax._idearoot._kids.get(week_text)._agent_coin_onset = 13
    ax._idearoot._kids.get(week_text)._agent_coin_cease = 13

    assert ax._idearoot._agent_coin_onset == 13
    assert ax._idearoot._agent_coin_cease == 13
    assert ax._idearoot._kids.get(work_text)._agent_coin_onset == 13
    assert ax._idearoot._kids.get(work_text)._agent_coin_cease == 13
    assert ax._idearoot._kids.get(catt_text)._agent_coin_onset == 13
    assert ax._idearoot._kids.get(catt_text)._agent_coin_cease == 13
    assert ax._idearoot._kids.get(week_text)._agent_coin_onset == 13
    assert ax._idearoot._kids.get(week_text)._agent_coin_cease == 13

    # WHEN
    ax.set_agent_metrics()

    # THEN
    assert ax._idearoot._agent_coin_onset != 13
    assert ax._idearoot._agent_coin_cease != 13
    assert ax._idearoot._kids.get(work_text)._agent_coin_onset != 13
    assert ax._idearoot._kids.get(work_text)._agent_coin_cease != 13
    assert ax._idearoot._kids.get(catt_text)._agent_coin_onset != 13
    assert ax._idearoot._kids.get(catt_text)._agent_coin_cease != 13
    assert ax._idearoot._kids.get(week_text)._agent_coin_onset != 13
    assert ax._idearoot._kids.get(week_text)._agent_coin_cease != 13


def test_agent_get_idea_list_CorrectlyCalculatesIdeaAttr_agent_coin():
    # GIVEN
    src_text = "src"
    ax = AgentUnit(_weight=10, _desc=src_text)

    auto_text = "auto"
    auto_idea = IdeaKid(_desc=auto_text, _weight=10)
    ax.add_idea(idea_kid=auto_idea, walk=src_text)

    barn_text = "barn"
    barn_road = f"{src_text},{barn_text}"
    barn_idea = IdeaKid(_desc=barn_text, _weight=60)
    ax.add_idea(idea_kid=barn_idea, walk=src_text)
    lamb_text = "lambs"
    lamb_road = f"{barn_road},{lamb_text}"
    lamb_idea = IdeaKid(_desc=lamb_text, _weight=1)
    ax.add_idea(idea_kid=lamb_idea, walk=barn_road)
    duck_text = "ducks"
    duck_road = f"{barn_road},{duck_text}"
    duck_idea = IdeaKid(_desc=duck_text, _weight=2)
    ax.add_idea(idea_kid=duck_idea, walk=barn_road)

    coal_text = "coal"
    coal_idea = IdeaKid(_desc=coal_text, _weight=30)
    ax.add_idea(idea_kid=coal_idea, walk=src_text)

    assert ax._idearoot._agent_coin_onset is None
    assert ax._idearoot._agent_coin_cease is None
    assert ax._idearoot._kids.get(auto_text)._agent_coin_onset is None
    assert ax._idearoot._kids.get(auto_text)._agent_coin_cease is None
    assert ax._idearoot._kids.get(barn_text)._agent_coin_onset is None
    assert ax._idearoot._kids.get(barn_text)._agent_coin_cease is None
    assert ax._idearoot._kids.get(coal_text)._agent_coin_onset is None
    assert ax._idearoot._kids.get(coal_text)._agent_coin_cease is None
    lamb_before = ax.get_idea_kid(road=lamb_road)
    assert lamb_before._agent_coin_onset is None
    assert lamb_before._agent_coin_cease is None
    duck_before = ax.get_idea_kid(road=duck_road)
    assert duck_before._agent_coin_onset is None
    assert duck_before._agent_coin_cease is None

    # WHEN
    ax.set_agent_metrics()

    # THEN
    assert ax._idearoot._agent_coin_onset == 0.0
    assert ax._idearoot._agent_coin_cease == 1.0
    assert ax._idearoot._kids.get(auto_text)._agent_coin_onset == 0.0
    assert ax._idearoot._kids.get(auto_text)._agent_coin_cease == 0.1
    assert ax._idearoot._kids.get(barn_text)._agent_coin_onset == 0.1
    assert ax._idearoot._kids.get(barn_text)._agent_coin_cease == 0.7
    assert ax._idearoot._kids.get(coal_text)._agent_coin_onset == 0.7
    assert ax._idearoot._kids.get(coal_text)._agent_coin_cease == 1.0

    duck_after = ax.get_idea_kid(road=duck_road)
    assert duck_after._agent_coin_onset == 0.1
    assert duck_after._agent_coin_cease == 0.5
    lamb_after = ax.get_idea_kid(road=lamb_road)
    assert lamb_after._agent_coin_onset == 0.5
    assert lamb_after._agent_coin_cease == 0.7


def test_agent_get_idea_list_without_root_CorrectlyCalculatesIdeaAttributes():
    # GIVEN / WHEN
    agent_x = get_agent_with7amCleanTableRequired()

    # THEN
    for idea in agent_x.get_idea_list_without_idearoot():
        print(f"{idea._desc=}")
        assert str(type(idea)).find(".idea.IdeaKid'>") > 0


def test_agent_get_idea_list_CorrectlyCalculatesRangeAttributes():
    # GIVEN
    agent_x = get_agent_with7amCleanTableRequired()
    idea_list = agent_x.get_idea_list()
    for idea in idea_list:
        if idea._desc == "clean table":
            # for required in idea._requiredunits.values():
            #     print(f"{idea._desc=} {required}")
            assert idea._active_status == False

    # set acptfacts as midnight to 8am
    day24hr_base = f"{agent_x._desc},timetech,24hr day"
    day24hr_pick = f"{agent_x._desc},timetech,24hr day"
    day24hr_open = 0.0
    day24hr_nigh = 8.0

    # WHEN
    agent_x.set_acptfact(
        base=day24hr_base, pick=day24hr_pick, open=day24hr_open, nigh=day24hr_nigh
    )

    # THEN
    idea_list = agent_x.get_idea_list()
    temp_idea = None
    for idea in idea_list:
        # print(f"{idea._active_status=} {idea._desc=}")
        if idea._desc == "clean table":
            temp_idea = idea
            # for required in idea._requiredunits.values():
            #     print(f"{idea._desc=} {required}")
    assert temp_idea._active_status == True

    # WHEN
    # set acptfacts as 8am to 10am
    day24hr_open = 8.0
    day24hr_nigh = 10.0
    print(agent_x._idearoot._acptfactunits["src,timetech,24hr day"])
    agent_x.set_acptfact(
        base=day24hr_base, pick=day24hr_pick, open=day24hr_open, nigh=day24hr_nigh
    )
    print(agent_x._idearoot._acptfactunits["src,timetech,24hr day"])
    print(agent_x._idearoot._kids["housework"]._kids["clean table"]._requiredunits)
    # agent_x._idearoot._kids["housework"]._kids["clean table"]._active_status = None

    # THEN
    idea_list = agent_x.get_idea_list()
    for idea in idea_list:
        if idea._desc == "clean table":
            temp_idea = idea
            # for required in idea._requiredunits.values():
            #     print(f"{idea._desc=} {required}")
    assert temp_idea._active_status == False


def test_get_agenda_items():
    # GIVEN
    agent_x = get_agent_with_4_levels_and_2requireds()

    # WHEN
    promise_items = agent_x.get_agenda_items()

    # THEN
    assert promise_items != None
    assert len(promise_items) > 0
    assert len(promise_items) == 1


def test_exammple_idea_list_HasCorrectData():
    agent_x = agent_v001()
    print(f"{agent_x.get_required_bases()=}")
    # day_hour = "TlME,day_hour"
    # agent_x.set_acptfact(base=day_hour, pick=day_hour, open=0, nigh=23)
    hour_minute = "TlME,day_minute"
    agent_x.set_acptfact(base=hour_minute, pick=hour_minute, open=0, nigh=1439)
    print("yeahyea")
    mood = "TlME,Moods"
    agent_x.set_acptfact(base=mood, pick=mood)
    print(f"{agent_x.get_required_bases()=}")
    year_month = "TlME,year_month"
    agent_x.set_acptfact(base=year_month, pick=year_month)
    internet = "TlME,Internet"
    agent_x.set_acptfact(base=internet, pick=internet)
    assert agent_x != None
    # print(f"{agent_x._desc=}")
    # print(f"{len(agent_x._idearoot._kids)=}")
    if agent_x._idearoot._kids["Ultimate Frisbee"]._desc == "Ultimate Frisbee":
        assert agent_x._idearoot._kids["Ultimate Frisbee"]._requiredunits != None
    assert agent_x._desc != None

    for acptfact in agent_x._idearoot._acptfactunits.values():
        print(f"{acptfact=}")

    idea_list = agent_x.get_idea_list()
    # print(f"{str(type(idea))=}")
    # print(f"{len(idea_list)=}")
    for idea in idea_list:
        assert (
            str(type(idea)).find(".idea.IdeaRoot'>") > 0
            or str(type(idea)).find(".idea.IdeaKid'>") > 0
        )
        # print(f"{idea._desc=}")
        if idea._desc == "laundry monday":
            for required in idea._requiredunits.values():
                print(f"{idea._desc=} {required.base=}")  # {required.sufffacts=}")
            assert idea._active_status == False

    agent_x.set_acptfact(base="TlME,weekdays", pick="TlME,weekdays,Monday")
    idea_list = agent_x.get_idea_list()
    for idea in idea_list:
        assert (
            str(type(idea)).find(".idea.IdeaRoot'>") > 0
            or str(type(idea)).find(".idea.IdeaKid'>") > 0
        )

        if idea._desc == "laundry monday":
            assert idea._active_status == False


def test_exammple_idea_list_OptionWeekdaysCorrectlyWork():
    # GIVEN
    agent_x = agent_v001()
    day_hour = "TlME,day_hour"
    agent_x.set_acptfact(base=day_hour, pick=day_hour, open=0, nigh=23)
    day_minute = "TlME,day_minute"
    agent_x.set_acptfact(base=day_minute, pick=day_minute, open=0, nigh=59)
    month_week = "TlME,month_week"
    agent_x.set_acptfact(base=month_week, pick=month_week)
    nations = "TlME,Nation-States"
    agent_x.set_acptfact(base=nations, pick=nations)
    mood = "TlME,Moods"
    agent_x.set_acptfact(base=mood, pick=mood)
    aaron = "TlME,Aaron Donald sphere"
    agent_x.set_acptfact(base=aaron, pick=aaron)
    internet = "TlME,Internet"
    agent_x.set_acptfact(base=internet, pick=internet)
    year_month = "TlME,year_month"
    agent_x.set_acptfact(base=year_month, pick=year_month, open=0, nigh=1000)

    idea_list = agent_x.get_idea_list()
    missing_acptfacts = agent_x.get_missing_acptfact_bases()
    for missing_acptfact, count in missing_acptfacts.items():
        print(f"{missing_acptfact=} {count=}")

    weekday_road = "TlME,weekdays"
    mon_road = "TlME,weekdays,Monday"
    tue_road = "TlME,weekdays,Tuesday"
    mon_sufffact_x = sufffactunit_shop(need=mon_road)
    tue_sufffact_x = sufffactunit_shop(need=tue_road)
    mt_sufffacts = {
        mon_sufffact_x.need: mon_sufffact_x,
        tue_sufffact_x.need: tue_sufffact_x,
    }
    mt_required = RequiredUnit(base=weekday_road, sufffacts=mt_sufffacts)
    mt_required_x = RequiredHeir(base=weekday_road, sufffacts=mt_sufffacts)
    agent_x._idearoot.set_required_unit(required=mt_required)
    # print(f"{agent_x._requiredunits[weekday_road].base=}")
    # print(f"{agent_x._requiredunits[weekday_road].sufffacts[mon_road].need=}")
    # print(f"{agent_x._requiredunits[weekday_road].sufffacts[tue_road].need=}")
    for sufffact_x in agent_x._idearoot._requiredunits[weekday_road].sufffacts.values():
        assert sufffact_x == mt_required.sufffacts[sufffact_x.need]
    assert agent_x._idearoot._requiredunits[weekday_road] == mt_required

    # WHEN
    idea_list = agent_x.get_idea_list()

    # THEN
    for sufffact_x in agent_x._idearoot._requiredheirs[weekday_road].sufffacts.values():
        assert sufffact_x == mt_required.sufffacts[sufffact_x.need]
    assert agent_x._idearoot._requiredheirs[weekday_road] == mt_required_x

    bird_walk = "TlME,casa"
    bird_desc = "say hi to birds"
    bird_road = Road(f"{bird_walk},{bird_desc}")
    assert from_list_get_active_status(road=bird_road, idea_list=idea_list) == False

    agent_x.set_acptfact(base="TlME,weekdays", pick="TlME,weekdays,Monday")
    idea_list = agent_x.get_idea_list()
    casa_idea = agent_x._idearoot._kids["casa"]
    twee_idea = casa_idea._kids["say hi to birds"]
    print(f"{len(agent_x._idearoot._requiredheirs)=}")
    print(f"{len(casa_idea._requiredheirs)=}")
    print(f"{len(twee_idea._requiredheirs)=}")

    # assert YR.get_active_status(road=bird_idea, idea_list=idea_list) == True

    # agent_x.set_acptfact(base="TlME,weekdays", pick="TlME,weekdays,Tuesday")
    # idea_list = agent_x.get_idea_list()
    # assert YR.get_active_status(road=bird_idea, idea_list=idea_list) == True

    # agent_x.set_acptfact(base="TlME,weekdays", pick="TlME,weekdays,Wednesday")
    # idea_list = agent_x.get_idea_list()
    # assert YR.get_active_status(road=bird_idea, idea_list=idea_list) == False


def test_exammple_idea_list_Every6WeeksRequired():
    # GIVEN
    agent_x = agent_v001()
    src_text = "TlME"
    day_text = "day_hour"
    day_road = f"{src_text},{day_text}"
    min_text = "day_minute"
    min_road = f"{src_text},{day_text}"

    # WHEN
    agent_x.set_acptfact(base=day_road, pick=day_road, open=0, nigh=23)
    agent_x.set_acptfact(base=min_road, pick=min_road, open=0, nigh=59)
    idea_list = agent_x.get_idea_list()

    # THEN
    ced_week_base = f"{src_text},ced_week"

    sufffact_divisor = None
    sufffact_open = None
    sufffact_nigh = None
    print(f"{len(idea_list)=}")
    for idea in idea_list:
        # print(f"{idea._walk=}")

        if idea._desc == "clean sheets couch blankets":
            print(f"{idea._walk=}")
            for required in idea._requiredunits.values():
                if required.base == ced_week_base:
                    for sufffact_x in required.sufffacts.values():
                        print(f"{idea._desc=} {required.base=} {sufffact_x=}")
                        sufffact_divisor = sufffact_x.divisor
                        sufffact_open = sufffact_x.open
                        sufffact_nigh = sufffact_x.nigh
            # print(f"{idea._requiredunits=}")
            assert idea._active_status == False
    assert sufffact_divisor == 6
    assert sufffact_open == 1
    print(
        "There exists a idea with a required_base TlME,ced_week that also has lemmet div =6 and open/nigh =1"
    )
    # print(f"{len(idea_list)=}")
    ced_week_open = 6001

    # WHEN
    agent_x.set_acptfact(
        base=ced_week_base, pick=ced_week_base, open=ced_week_open, nigh=ced_week_open
    )
    nation_text = "Nation-States"
    nation_road = f"{src_text},{nation_text}"
    agent_x.set_acptfact(base=nation_road, pick=nation_road)
    print(
        f"Nation-states set and also acptfact set: {ced_week_base=} with {ced_week_open=} and {ced_week_open=}"
    )
    print(f"{agent_x._idearoot._acptfactunits=}")
    idea_list = agent_x.get_idea_list()

    # THEN
    clean_sheets_status = None
    for idea in idea_list:
        if idea._desc == "clean sheets couch blankets":
            for required in idea._requiredunits.values():
                if required.base == ced_week_base:
                    for sufffact_x in required.sufffacts.values():
                        print(f"{idea._desc=} {required.base=} {sufffact_x=}")
                        assert sufffact_x.divisor == 6 and sufffact_x.open == 1
            print(f"{agent_x._idearoot._acptfactunits=}")
            clean_sheets_status = True
    print(f"{len(idea_list)=}")
    assert clean_sheets_status == True


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
                        f"{idea._desc=} base:{required.base} need:{sufffact_x.need} open:{sufffact_x.open} nigh:{sufffact_x.nigh} div:{sufffact_x.divisor} status:{sufffact_x._status}"
                    )


def test_exammple_idea_list_EveryIdeaHasSatiateStatus():
    # GIVEN
    agent_x = agent_v001()

    # WHEN
    idea_list = agent_x.get_idea_list()

    # THEN
    print(f"{len(idea_list)=}")
    first_idea_kid_count = 0
    first_idea_kid_none_count = 0
    first_idea_kid_true_count = 0
    first_idea_kid_false_count = 0
    idea_kid_count = 0
    for idea in idea_list:
        if str(type(idea)).find(".idea.IdeaKid'>") > 0:
            first_idea_kid_count += 1
            if idea._active_status is None:
                first_idea_kid_none_count += 1
            elif idea._active_status:
                first_idea_kid_true_count += 1
            elif idea._active_status == False:
                first_idea_kid_false_count += 1

    print(f"{first_idea_kid_count=}")
    print(f"{first_idea_kid_none_count=}")
    print(f"{first_idea_kid_true_count=}")
    print(f"{first_idea_kid_false_count=}")
    for idea in idea_list:
        if str(type(idea)).find(".idea.IdeaKid'>") > 0:
            idea_kid_count += 1
            if idea._active_status is None:
                print(f"{idea._desc=} {idea_kid_count=}")
            assert idea._active_status in (True, False)
    assert idea_kid_count == len(idea_list) - 1


def test_exammple_idea_list_EveryOtherMonthWorks():
    # GIVEN
    agent_x = agent_v001()
    src_road = "TlME"
    minute_text = "day_minute"
    minute_road = f"{src_road},{minute_text}"
    agent_x.set_acptfact(base=minute_road, pick=minute_road, open=0, nigh=1399)
    month_text = "month_week"
    month_road = f"{src_road},{month_text}"
    agent_x.set_acptfact(base=month_road, pick=month_road)
    nations_text = "Nation-States"
    nations_road = f"{src_road},{nations_text}"
    agent_x.set_acptfact(base=nations_road, pick=nations_road)
    mood_text = "Moods"
    mood_road = f"{src_road},{mood_text}"
    agent_x.set_acptfact(base=mood_road, pick=mood_road)
    aaron_text = "Aaron Donald sphere"
    aaron_road = f"{src_road},{aaron_text}"
    agent_x.set_acptfact(base=aaron_road, pick=aaron_road)
    internet_text = "Internet"
    internet_road = f"{src_road},{internet_text}"
    agent_x.set_acptfact(base=internet_road, pick=internet_road)
    weekdays_text = "weekdays"
    weekdays_road = f"{src_road},{weekdays_text}"
    agent_x.set_acptfact(base=weekdays_road, pick=weekdays_road)
    idea_list = agent_x.get_idea_list()
    print(f"{len(idea_list)=}")

    casa_text = "casa"
    casa_road = f"{src_road},{casa_text}"
    clean_text = "cleaning"
    clean_road = f"{casa_road},{clean_text}"
    mat_desc = "deep clean play mat"
    mat_road = Road(f"{clean_road},{mat_desc}")
    # commented out since it's difficult to understand
    assert from_list_get_active_status(road=mat_road, idea_list=idea_list) == False

    year_month_base = "TlME,year_month"
    print(f"{year_month_base=}, {year_month_base=}")

    # WHEN
    agent_x.set_acptfact(base=year_month_base, pick=year_month_base, open=0, nigh=8)
    ced_week = "TlME,ced_week"
    agent_x.set_acptfact(base=ced_week, pick=ced_week, open=0, nigh=4)

    # THEN
    idea_list = agent_x.get_idea_list()
    print(f"{len(idea_list)=}")
    print(f"{len(agent_x._idearoot._acptfactunits)=}")
    # from_list_get_active_status(road=mat_road, idea_list=idea_list)
    assert from_list_get_active_status(road=mat_road, idea_list=idea_list)
