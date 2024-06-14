from src.agenda.graphic import display_facttree
from src.agenda.party import partyunit_shop
from src.agenda.idea import IdeaID, balancelink_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.healer import healerhold_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels_and_2reasons,
    get_agenda_with7amCleanTableReason,
    agenda_v001,
    from_list_get_active,
)
from src.agenda.fact import factunit_shop
from src.agenda.reason_fact import (
    premiseunit_shop,
    reasonunit_shop,
    reasonheir_shop,
)
from src.agenda.agenda import agendaunit_shop


def test_AgendaUnit_get_tree_metrics_TracksReasonsThatHaveNoBeliefBases():
    yao_agenda = agenda_v001()
    yao_agenda_metrics = yao_agenda.get_tree_metrics()

    print(f"{yao_agenda_metrics.level_count=}")
    print(f"{yao_agenda_metrics.reason_bases=}")
    assert yao_agenda_metrics != None
    reason_bases_x = yao_agenda_metrics.reason_bases
    assert reason_bases_x != None
    assert len(reason_bases_x) > 0


def test_AgendaUnit_get_missing_belief_bases_ReturnsAllBasesNotCoveredByBeliefs():
    yao_agenda = agenda_v001()
    missing_bases = yao_agenda.get_missing_belief_bases()
    assert missing_bases != None
    print(f"{missing_bases=}")
    print(f"{len(missing_bases)=}")
    assert len(missing_bases) == 11

    yao_agenda.set_belief(
        base=yao_agenda.make_l1_road("day_minute"),
        pick=yao_agenda.make_l1_road("day_minute"),
        open=0,
        nigh=1439,
    )
    missing_bases = yao_agenda.get_missing_belief_bases()

    assert len(missing_bases) == 11


def test_AgendaUnit_3AdvocatesNofactunit_shop():
    # GIVEN
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"

    zia_agenda = agendaunit_shop("Zia")
    au_rico = partyunit_shop(party_id=rico_text)
    au_carm = partyunit_shop(party_id=carm_text)
    au_patr = partyunit_shop(party_id=patr_text)
    # print(f"{rico=}")
    zia_agenda.set_partyunit(partyunit=au_rico)
    zia_agenda.set_partyunit(partyunit=au_carm)
    zia_agenda.set_partyunit(partyunit=au_patr)
    zia_agenda._factroot.set_balancelink(
        balancelink=balancelink_shop(idea_id=IdeaID(rico_text), credor_weight=10)
    )
    zia_agenda._factroot.set_balancelink(
        balancelink=balancelink_shop(idea_id=IdeaID(carm_text), credor_weight=10)
    )
    zia_agenda._factroot.set_balancelink(
        balancelink=balancelink_shop(idea_id=IdeaID(patr_text), credor_weight=10)
    )

    # WHEN
    assert zia_agenda.get_partys_metrics() != None
    partys_metrics = zia_agenda.get_partys_metrics()

    # THEN
    balancelink_rico = partys_metrics[rico_text]
    balancelink_carm = partys_metrics[carm_text]
    balancelink_patr = partys_metrics[patr_text]
    assert balancelink_rico.idea_id != None
    assert balancelink_carm.idea_id != None
    assert balancelink_patr.idea_id != None
    assert balancelink_rico.idea_id == rico_text
    assert balancelink_carm.idea_id == carm_text
    assert balancelink_patr.idea_id == patr_text
    all_ideas = zia_agenda._ideas
    ideaunit_rico = all_ideas[rico_text]
    ideaunit_carm = all_ideas[carm_text]
    ideaunit_patr = all_ideas[patr_text]
    assert ideaunit_rico._party_mirror == True
    assert ideaunit_carm._party_mirror == True
    assert ideaunit_patr._party_mirror == True


def _check_all_objects_in_dict_are_correct_type(x_dict: dict, type_str: str) -> bool:
    bool_x = True
    for x_value in x_dict.values():
        if type_str not in str(type(x_value)):
            bool_x = False
        print(f"/t{type(x_value)=} {type_str=} {str(type(x_value)).find(type_str)=}")
    return bool_x


def test_AgendaUnit_calc_agenda_metrics_CreatesFullyPopulated_fact_dict():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons()

    # WHEN
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert len(sue_agenda._fact_dict) == 17


def test_AgendaUnit_calc_agenda_metrics_SetsSatiateStatusCorrectlyWhenBeliefSaysNo():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = sue_agenda.make_road(week_road, sun_text)

    # for fact in sue_agenda._fact_dict.values():
    #     print(f"{casa_road=} {fact.get_road()=}")
    casa_text = "casa"
    casa_road = sue_agenda.make_l1_road(casa_text)
    assert sue_agenda.get_fact_obj(casa_road)._active is None

    # WHEN
    sue_agenda.set_belief(base=week_road, pick=sun_road)
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert sue_agenda._fact_dict != {}
    assert len(sue_agenda._fact_dict) == 17

    # for fact in sue_agenda._fact_dict.values():
    #     print(f"{casa_road=} {fact.get_road()=}")
    assert sue_agenda.get_fact_obj(casa_road)._active is False


def test_AgendaUnit_calc_agenda_metrics_SetsSatiateStatusCorrectlyWhenBeliefModifies():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    sun_text = "Wednesday"
    sun_road = sue_agenda.make_road(week_road, sun_text)
    casa_text = "casa"
    casa_road = sue_agenda.make_l1_road(casa_text)

    # WHEN
    sue_agenda.set_belief(base=week_road, pick=sun_road)

    # THEN
    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._fact_dict
    assert len(sue_agenda._fact_dict) == 17
    assert sue_agenda._fact_dict.get(casa_road)._active is False

    # WHEN
    states_text = "nation-state"
    states_road = sue_agenda.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_agenda.make_road(states_road, usa_text)
    sue_agenda.set_belief(base=states_road, pick=usa_road)

    # THEN
    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._fact_dict
    assert len(sue_agenda._fact_dict) == 17
    assert sue_agenda._fact_dict.get(casa_road)._active

    # WHEN
    france_text = "France"
    france_road = sue_agenda.make_road(states_road, france_text)
    sue_agenda.set_belief(base=states_road, pick=france_road)

    # THEN
    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._fact_dict
    assert len(sue_agenda._fact_dict) == 17
    assert sue_agenda._fact_dict.get(casa_road)._active is False


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_fact_dict():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    wed_text = "Wednesday"
    wed_road = sue_agenda.make_road(week_road, wed_text)
    state_text = "nation-state"
    state_road = sue_agenda.make_l1_road(state_text)
    france_text = "France"
    france_road = sue_agenda.make_road(state_road, france_text)
    sue_agenda.set_belief(base=week_road, pick=wed_road)
    sue_agenda.set_belief(base=state_road, pick=france_road)

    casa_text = "casa"
    casa_road = sue_agenda.make_l1_road(casa_text)
    casa_fact = sue_agenda.get_fact_obj(casa_road)
    print(f"{sue_agenda._owner_id=} {len(casa_fact._reasonunits)=}")
    # print(f"{casa_fact._reasonunits=}")
    print(f"{sue_agenda._owner_id=} {len(sue_agenda._factroot._beliefunits)=}")
    # print(f"{sue_agenda._factroot._beliefunits=}")

    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._fact_dict
    assert len(sue_agenda._fact_dict) == 17

    usa_text = "USA"
    usa_road = sue_agenda.make_road(state_road, usa_text)
    oregon_text = "Oregon"
    oregon_road = sue_agenda.make_road(usa_road, oregon_text)

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
        _base_fact_active=True,
    )
    sta_lh = reasonheir_shop(
        base=state_road,
        premises={usa.need: usa},
        _status=True,
        _task=False,
        _base_fact_active=True,
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
    sue_agenda.set_belief(base=state_road, pick=oregon_road)

    # THEN
    casa_fact = sue_agenda._fact_dict.get(casa_road)
    print(f"\nlook at {casa_fact.get_road()=}")
    assert casa_fact._parent_road == sue_agenda._real_id
    assert casa_fact._kids == {}
    assert casa_fact._weight == 30
    assert casa_fact._label == casa_text
    assert casa_fact._level == 1
    assert casa_fact._active
    assert casa_fact.pledge
    # print(f"{casa_fact._reasonheirs=}")
    x_reasonheir_state = casa_fact._reasonheirs[state_road]
    print(f"  {x_reasonheir_state=}")
    print(f"  {x_reasonheir_state._status=}\n")
    # assert casa_fact._reasonheirs == x1_reasonheirs

    assert len(casa_fact._reasonheirs) == len(x1_reasonheirs)
    week_reasonheir = casa_fact._reasonheirs.get(week_road)
    # usa_premise = week_reasonheir.premises.get(usa_road)
    print(f"    {casa_fact._label=}")
    # print(f"    {usa_premise.base=}")
    # print(f"    {usa_premise._task=}")
    # print(f"    {usa_premise._task=}")
    assert week_reasonheir._task is False
    # print(f"      premises: {w=}")
    # w_need = usa_premise.premises[wed_road].need
    # print(f"      {w_need=}")
    # assert usa_premise._task == w_need._task
    # assert usa_premise._status == w_need._status
    # assert week_reasonheir.premises == week_reasonheir.premises

    # assert casa_fact._reasonunits == x1_reasonunits

    # print("iterate through every fact...")
    # for x_fact in fact_dict:
    #     if str(type(x_fact)).find(".fact.FactUnit'>") > 0:
    #         assert x_fact._active != None

    #     # print("")
    #     # print(f"{x_fact._label=}")
    #     # print(f"{len(x_fact._reasonunits)=}")
    #     print(
    #         f"  {x_fact._label} iterate through every reasonheir... {len(x_fact._reasonheirs)=} {x_fact._label=}"
    #     )
    #     # print(f"{x_fact._reasonheirs=}")
    #     for reason in x_fact._reasonheirs.values():
    #         assert str(type(reason)).find(".reason.ReasonHeir'>") > 0
    #         print(f"    {reason.base=}")
    #         assert reason._status != None
    #         for premise_x in reason.premises.values():
    #             assert premise_x._status != None
    #         assert _check_all_objects_in_dict_are_correct_type(
    #             x_dict=reason.premises, type_str="src.agenda.reason.PremiseUnit"
    #         )


def test_AgendaUnit_calc_agenda_metrics_CorrectlyClears_agenda_fund():
    # GIVEN
    x_agenda = get_agenda_with7amCleanTableReason()
    casa_road = x_agenda.make_l1_road("casa")
    catt_road = x_agenda.make_l1_road("feed cat")
    week_road = x_agenda.make_l1_road("weekdays")
    x_agenda._factroot._agenda_fund_onset = 13
    x_agenda._factroot._agenda_fund_cease = 13
    x_agenda.get_fact_obj(casa_road)._agenda_fund_onset = 13
    x_agenda.get_fact_obj(casa_road)._agenda_fund_cease = 13
    x_agenda.get_fact_obj(catt_road)._agenda_fund_onset = 13
    x_agenda.get_fact_obj(catt_road)._agenda_fund_cease = 13
    x_agenda.get_fact_obj(week_road)._agenda_fund_onset = 13
    x_agenda.get_fact_obj(week_road)._agenda_fund_cease = 13

    assert x_agenda._factroot._agenda_fund_onset == 13
    assert x_agenda._factroot._agenda_fund_cease == 13
    assert x_agenda.get_fact_obj(casa_road)._agenda_fund_onset == 13
    assert x_agenda.get_fact_obj(casa_road)._agenda_fund_cease == 13
    assert x_agenda.get_fact_obj(catt_road)._agenda_fund_onset == 13
    assert x_agenda.get_fact_obj(catt_road)._agenda_fund_cease == 13
    assert x_agenda.get_fact_obj(week_road)._agenda_fund_onset == 13
    assert x_agenda.get_fact_obj(week_road)._agenda_fund_cease == 13

    # WHEN
    x_agenda.calc_agenda_metrics()

    # THEN
    assert x_agenda._factroot._agenda_fund_onset != 13
    assert x_agenda._factroot._agenda_fund_cease != 13
    assert x_agenda.get_fact_obj(casa_road)._agenda_fund_onset != 13
    assert x_agenda.get_fact_obj(casa_road)._agenda_fund_cease != 13
    assert x_agenda.get_fact_obj(catt_road)._agenda_fund_onset != 13
    assert x_agenda.get_fact_obj(catt_road)._agenda_fund_cease != 13
    assert x_agenda.get_fact_obj(week_road)._agenda_fund_onset != 13
    assert x_agenda.get_fact_obj(week_road)._agenda_fund_cease != 13


def test_AgendaUnit_calc_agenda_metrics_CorrectlyCalculatesFactAttr_agenda_fund():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao", _weight=10)

    auto_text = "auto"
    auto_road = yao_agenda.make_l1_road(auto_text)
    auto_fact = factunit_shop(auto_text, _weight=10)
    yao_agenda.add_l1_fact(auto_fact)

    barn_text = "barn"
    barn_road = yao_agenda.make_l1_road(barn_text)
    barn_fact = factunit_shop(barn_text, _weight=60)
    yao_agenda.add_l1_fact(barn_fact)
    lamb_text = "lambs"
    lamb_road = yao_agenda.make_road(barn_road, lamb_text)
    lamb_fact = factunit_shop(lamb_text, _weight=1)
    yao_agenda.add_fact(lamb_fact, parent_road=barn_road)
    duck_text = "ducks"
    duck_road = yao_agenda.make_road(barn_road, duck_text)
    duck_fact = factunit_shop(duck_text, _weight=2)
    yao_agenda.add_fact(duck_fact, parent_road=barn_road)

    coal_text = "coal"
    coal_road = yao_agenda.make_l1_road(coal_text)
    coal_fact = factunit_shop(coal_text, _weight=30)
    yao_agenda.add_l1_fact(coal_fact)

    assert yao_agenda._factroot._agenda_fund_onset is None
    assert yao_agenda._factroot._agenda_fund_cease is None
    assert yao_agenda.get_fact_obj(auto_road)._agenda_fund_onset is None
    assert yao_agenda.get_fact_obj(auto_road)._agenda_fund_cease is None
    assert yao_agenda.get_fact_obj(barn_road)._agenda_fund_onset is None
    assert yao_agenda.get_fact_obj(barn_road)._agenda_fund_cease is None
    assert yao_agenda.get_fact_obj(coal_road)._agenda_fund_onset is None
    assert yao_agenda.get_fact_obj(coal_road)._agenda_fund_cease is None
    lamb_before = yao_agenda.get_fact_obj(road=lamb_road)
    assert lamb_before._agenda_fund_onset is None
    assert lamb_before._agenda_fund_cease is None
    duck_before = yao_agenda.get_fact_obj(road=duck_road)
    assert duck_before._agenda_fund_onset is None
    assert duck_before._agenda_fund_cease is None

    # WHEN
    yao_agenda.calc_agenda_metrics()

    # THEN
    assert yao_agenda._factroot._agenda_fund_onset == 0.0
    assert yao_agenda._factroot._agenda_fund_cease == 1.0
    assert yao_agenda.get_fact_obj(auto_road)._agenda_fund_onset == 0.0
    assert yao_agenda.get_fact_obj(auto_road)._agenda_fund_cease == 0.1
    assert yao_agenda.get_fact_obj(barn_road)._agenda_fund_onset == 0.1
    assert yao_agenda.get_fact_obj(barn_road)._agenda_fund_cease == 0.7
    assert yao_agenda.get_fact_obj(coal_road)._agenda_fund_onset == 0.7
    assert yao_agenda.get_fact_obj(coal_road)._agenda_fund_cease == 1.0

    duck_after = yao_agenda.get_fact_obj(road=duck_road)
    assert duck_after._agenda_fund_onset == 0.1
    assert duck_after._agenda_fund_cease == 0.5
    lamb_after = yao_agenda.get_fact_obj(road=lamb_road)
    assert lamb_after._agenda_fund_onset == 0.5
    assert lamb_after._agenda_fund_cease == 0.7


def test_AgendaUnit_get_fact_list_without_root_CorrectlyCalculatesFactAttributes():
    # GIVEN
    x_agenda = get_agenda_with7amCleanTableReason()

    # WHEN
    fact_list_without_factroot = x_agenda.get_fact_list_without_factroot()
    fact_dict_with_factroot = x_agenda.get_fact_dict()

    # THEN
    assert len(fact_list_without_factroot) == 28
    assert len(fact_list_without_factroot) + 1 == len(fact_dict_with_factroot)

    # for fact in x_agenda.get_fact_list_without_factroot():
    #     assert str(type(fact)).find(".fact.FactUnit'>") > 0

    # for fact in x_agenda.get_fact_list_without_factroot():
    #     print(f"{fact._label=}")


def test_AgendaUnit_calc_agenda_metrics_CorrectlyCalculatesRangeAttributes():
    # GIVEN
    sue_agenda = get_agenda_with7amCleanTableReason()
    sue_agenda.calc_agenda_metrics()
    house_text = "housemanagement"
    house_road = sue_agenda.make_l1_road(house_text)
    clean_text = "clean table"
    clean_road = sue_agenda.make_road(house_road, clean_text)
    assert sue_agenda._fact_dict.get(clean_road)._active is False

    # set beliefs as midnight to 8am
    time_text = "timetech"
    time_road = sue_agenda.make_l1_road(time_text)
    day24hr_text = "24hr day"
    day24hr_road = sue_agenda.make_road(time_road, day24hr_text)
    day24hr_base = day24hr_road
    day24hr_pick = day24hr_road
    day24hr_open = 0.0
    day24hr_nigh = 8.0

    # WHEN
    sue_agenda.set_belief(
        base=day24hr_base, pick=day24hr_pick, open=day24hr_open, nigh=day24hr_nigh
    )

    # THEN
    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._fact_dict.get(clean_road)._active

    # WHEN
    # set beliefs as 8am to 10am
    day24hr_open = 8.0
    day24hr_nigh = 10.0
    print(sue_agenda._factroot._beliefunits[day24hr_road])
    sue_agenda.set_belief(
        base=day24hr_base, pick=day24hr_pick, open=day24hr_open, nigh=day24hr_nigh
    )
    print(sue_agenda._factroot._beliefunits[day24hr_road])
    print(sue_agenda._factroot._kids[house_text]._kids[clean_text]._reasonunits)
    # sue_agenda._factroot._kids["housemanagement"]._kids[clean_text]._active = None

    # THEN
    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._fact_dict.get(clean_road)._active is False


def test_get_intent_dict_ReturnsCorrectObj():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons()

    # WHEN
    pledge_items = sue_agenda.get_intent_dict()

    # THEN
    assert pledge_items != None
    assert len(pledge_items) > 0
    assert len(pledge_items) == 1


def test_AgendaUnit_calc_agenda_metrics_CorrectlySetsData_agenda_v001():
    yao_agenda = agenda_v001()
    print(f"{yao_agenda.get_reason_bases()=}")
    # day_hour = f"{yao_agenda._real_id},day_hour"
    # yao_agenda.set_belief(base=day_hour, pick=day_hour, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = yao_agenda.make_l1_road(day_min_text)
    yao_agenda.set_belief(base=day_min_road, pick=day_min_road, open=0, nigh=1439)

    mood_text = "Moods"
    mood_road = yao_agenda.make_l1_road(mood_text)
    yao_agenda.set_belief(base=mood_road, pick=mood_road)
    print(f"{yao_agenda.get_reason_bases()=}")

    yr_mon_text = "year_month"
    yr_mon_road = yao_agenda.make_l1_road(yr_mon_text)
    yao_agenda.set_belief(base=yr_mon_road, pick=yr_mon_road)
    inter_text = "Internet"
    inter_road = yao_agenda.make_l1_road(inter_text)
    yao_agenda.set_belief(base=inter_road, pick=inter_road)
    assert yao_agenda != None
    # print(f"{yao_agenda._owner_id=}")
    # print(f"{len(yao_agenda._factroot._kids)=}")
    ulty_text = "Ultimate Frisbee"
    ulty_road = yao_agenda.make_l1_road(ulty_text)

    # if yao_agenda._factroot._kids["Ultimate Frisbee"]._label == "Ultimate Frisbee":
    assert yao_agenda._factroot._kids[ulty_text]._reasonunits != None
    assert yao_agenda._owner_id != None

    # for belief in yao_agenda._factroot._beliefunits.values():
    #     print(f"{belief=}")

    yao_agenda.calc_agenda_metrics()
    # print(f"{str(type(fact))=}")
    # print(f"{len(fact_dict)=}")
    laundry_text = "laundry monday"
    casa_road = yao_agenda.make_l1_road("casa")
    cleaning_road = yao_agenda.make_road(casa_road, "cleaning")
    laundry_road = yao_agenda.make_road(cleaning_road, laundry_text)

    # for fact in fact_dict:
    #     assert (
    #         str(type(fact)).find(".fact.FactUnit'>") > 0
    #         or str(type(fact)).find(".fact.FactUnit'>") > 0
    #     )
    #     # print(f"{fact._label=}")
    #     if fact._label == laundry_text:
    #         for reason in fact._reasonunits.values():
    #             print(f"{fact._label=} {reason.base=}")  # {reason.premises=}")
    # assert fact._active is False
    assert yao_agenda._fact_dict.get(laundry_road)._active is False

    # WHEN
    week_text = "weekdays"
    week_road = yao_agenda.make_l1_road(week_text)
    mon_text = "Monday"
    mon_road = yao_agenda.make_road(week_road, mon_text)
    yao_agenda.set_belief(base=week_road, pick=mon_road)
    yao_agenda.calc_agenda_metrics()

    # THEN
    assert yao_agenda._fact_dict.get(laundry_road)._active is False


def test_AgendaUnit_calc_agenda_metrics_OptionWeekdaysReturnsCorrectObj_agenda_v001():
    # GIVEN
    yao_agenda = agenda_v001()

    day_hr_text = "day_hour"
    day_hr_road = yao_agenda.make_l1_road(day_hr_text)
    yao_agenda.set_belief(base=day_hr_road, pick=day_hr_road, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = yao_agenda.make_l1_road(day_min_text)
    yao_agenda.set_belief(base=day_min_road, pick=day_min_road, open=0, nigh=59)
    mon_wk_text = "month_week"
    mon_wk_road = yao_agenda.make_l1_road(mon_wk_text)
    yao_agenda.set_belief(base=mon_wk_road, pick=mon_wk_road)
    nation_text = "Nation-States"
    nation_road = yao_agenda.make_l1_road(nation_text)
    yao_agenda.set_belief(base=nation_road, pick=nation_road)
    mood_text = "Moods"
    mood_road = yao_agenda.make_l1_road(mood_text)
    yao_agenda.set_belief(base=mood_road, pick=mood_road)
    aaron_text = "Aaron Donald things effected by him"
    aaron_road = yao_agenda.make_l1_road(aaron_text)
    yao_agenda.set_belief(base=aaron_road, pick=aaron_road)
    inter_text = "Internet"
    inter_road = yao_agenda.make_l1_road(inter_text)
    yao_agenda.set_belief(base=inter_road, pick=inter_road)
    yr_mon_text = "year_month"
    yr_mon_road = yao_agenda.make_l1_road(yr_mon_text)
    yao_agenda.set_belief(base=yr_mon_road, pick=yr_mon_road, open=0, nigh=1000)

    yao_agenda.calc_agenda_metrics()
    missing_beliefs = yao_agenda.get_missing_belief_bases()
    # for missing_belief, count in missing_beliefs.items():
    #     print(f"{missing_belief=} {count=}")

    week_text = "weekdays"
    week_road = yao_agenda.make_l1_road(week_text)
    mon_text = "Monday"
    mon_road = yao_agenda.make_road(week_road, mon_text)
    tue_text = "Tuesday"
    tue_road = yao_agenda.make_road(week_road, tue_text)
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
    x_factroot = yao_agenda.get_fact_obj(yao_agenda._real_id)
    x_factroot.set_reasonunit(reason=mt_reasonunit)
    # print(f"{yao_agenda._reasonunits[week_road].base=}")
    # print(f"{yao_agenda._reasonunits[week_road].premises[mon_road].need=}")
    # print(f"{yao_agenda._reasonunits[week_road].premises[tue_road].need=}")
    week_reasonunit = x_factroot._reasonunits[week_road]
    print(f"{week_reasonunit.premises=}")
    premise_mon = week_reasonunit.premises.get(mon_road)
    premise_tue = week_reasonunit.premises.get(tue_road)
    assert premise_mon
    assert premise_mon == mt_reasonunit.premises[premise_mon.need]
    assert premise_tue
    assert premise_tue == mt_reasonunit.premises[premise_tue.need]
    assert week_reasonunit == mt_reasonunit

    # WHEN
    fact_dict = yao_agenda.get_fact_dict()

    # THEN
    gen_week_reasonheir = x_factroot.get_reasonheir(week_road)
    gen_mon_premise = gen_week_reasonheir.premises.get(mon_road)
    assert gen_mon_premise._status == mt_reasonheir.premises.get(mon_road)._status
    assert gen_mon_premise == mt_reasonheir.premises.get(mon_road)
    assert gen_week_reasonheir.premises == mt_reasonheir.premises
    assert gen_week_reasonheir == mt_reasonheir

    casa_text = "casa"
    casa_road = yao_agenda.make_l1_road(casa_text)
    bird_text = "say hi to birds"
    bird_road = yao_agenda.make_road(casa_road, bird_text)
    assert from_list_get_active(road=bird_road, fact_dict=fact_dict) is False

    # yao_agenda.set_belief(base=week_road, pick=mon_road)
    # fact_dict = yao_agenda.get_fact_dict()
    # casa_fact = x_factroot._kids[casa_text]
    # twee_fact = casa_fact._kids[bird_text]
    # print(f"{len(x_factroot._reasonheirs)=}")
    # print(f"{len(casa_fact._reasonheirs)=}")
    # print(f"{len(twee_fact._reasonheirs)=}")

    # assert YR.get_active(road=bird_fact, fact_dict=fact_dict) == True

    # yao_agenda.set_belief(base=f"{yao_agenda._real_id},weekdays", pick=f"{yao_agenda._real_id},weekdays,Tuesday")
    # fact_dict = yao_agenda.get_fact_dict()
    # assert YR.get_active(road=bird_fact, fact_dict=fact_dict) == True

    # yao_agenda.set_belief(base=f"{yao_agenda._real_id},weekdays", pick=f"{yao_agenda._real_id},weekdays,Wednesday")
    # fact_dict = yao_agenda.get_fact_dict()
    # assert YR.get_active(road=bird_fact, fact_dict=fact_dict) is False


def test_AgendaUnit_calc_agenda_metrics_CorrectlySetsFactUnitsActiveWithEvery6WeeksReason_agenda_v001():
    # GIVEN
    yao_agenda = agenda_v001()
    day_text = "day_hour"
    day_road = yao_agenda.make_l1_road(day_text)
    min_text = "day_minute"
    min_road = yao_agenda.make_l1_road(day_text)

    # WHEN
    yao_agenda.set_belief(base=day_road, pick=day_road, open=0, nigh=23)
    yao_agenda.set_belief(base=min_road, pick=min_road, open=0, nigh=59)
    yao_agenda.calc_agenda_metrics()

    # THEN
    ced_week_base = yao_agenda.make_l1_road("ced_week")

    premise_divisor = None
    premise_open = None
    premise_nigh = None
    print(f"{len(yao_agenda._fact_dict)=}")

    casa_road = yao_agenda.make_l1_road("casa")
    cleaning_road = yao_agenda.make_road(casa_road, "cleaning")
    clean_couch_road = yao_agenda.make_road(
        cleaning_road, "clean sheets couch blankets"
    )
    clean_sheet_fact = yao_agenda.get_fact_obj(clean_couch_road)
    # print(f"{clean_sheet_fact._reasonunits.values()=}")
    ced_week_reason = clean_sheet_fact._reasonunits.get(ced_week_base)
    ced_week_premise = ced_week_reason.premises.get(ced_week_base)
    print(
        f"{clean_sheet_fact._label=} {ced_week_reason.base=} {ced_week_premise.need=}"
    )
    # print(f"{clean_sheet_fact._label=} {ced_week_reason.base=} {premise_x=}")
    premise_divisor = ced_week_premise.divisor
    premise_open = ced_week_premise.open
    premise_nigh = ced_week_premise.nigh
    # print(f"{fact._reasonunits=}")
    assert clean_sheet_fact._active is False

    # for fact in fact_dict:
    #     # print(f"{fact._parent_road=}")
    #     if fact._label == "clean sheets couch blankets":
    #         print(f"{fact.get_road()=}")

    assert premise_divisor == 6
    assert premise_open == 1
    print(
        f"There exists a fact with a reason_base {ced_week_base} that also has lemmet div =6 and open/nigh =1"
    )
    # print(f"{len(fact_dict)=}")
    ced_week_open = 6001

    # WHEN
    yao_agenda.set_belief(
        base=ced_week_base, pick=ced_week_base, open=ced_week_open, nigh=ced_week_open
    )
    nation_text = "Nation-States"
    nation_road = yao_agenda.make_l1_road(nation_text)
    yao_agenda.set_belief(base=nation_road, pick=nation_road)
    print(
        f"Nation-states set and also belief set: {ced_week_base=} with {ced_week_open=} and {ced_week_open=}"
    )
    print(f"{yao_agenda._factroot._beliefunits=}")
    yao_agenda.calc_agenda_metrics()

    # THEN
    week_text = "ced_week"
    week_road = yao_agenda.make_l1_road(week_text)
    casa_road = yao_agenda.make_l1_road("casa")
    cleaning_road = yao_agenda.make_road(casa_road, "cleaning")
    clean_couch_text = "clean sheets couch blankets"
    clean_couch_road = yao_agenda.make_road(cleaning_road, clean_couch_text)
    clean_couch_fact = yao_agenda.get_fact_obj(road=clean_couch_road)
    week_reason = clean_couch_fact._reasonunits.get(week_road)
    week_premise = week_reason.premises.get(week_road)
    print(f"{clean_couch_fact._label=} {week_reason.base=} {week_premise=}")
    assert week_premise.divisor == 6 and week_premise.open == 1


def test_AgendaUnit_calc_agenda_metrics_EveryFactHasActiveStatus_agenda_v001():
    # GIVEN
    yao_agenda = agenda_v001()

    # WHEN
    yao_agenda.calc_agenda_metrics()

    # THEN
    print(f"{len(yao_agenda._fact_dict)=}")
    # first_fact_kid_count = 0
    # first_fact_kid_none_count = 0
    # first_fact_kid_true_count = 0
    # first_fact_kid_false_count = 0
    # for fact in fact_list:
    #     if str(type(fact)).find(".fact.FactUnit'>") > 0:
    #         first_fact_kid_count += 1
    #         if fact._active is None:
    #             first_fact_kid_none_count += 1
    #         elif fact._active:
    #             first_fact_kid_true_count += 1
    #         elif fact._active is False:
    #             first_fact_kid_false_count += 1

    # print(f"{first_fact_kid_count=}")
    # print(f"{first_fact_kid_none_count=}")
    # print(f"{first_fact_kid_true_count=}")
    # print(f"{first_fact_kid_false_count=}")

    # fact_kid_count = 0
    # for fact in fact_list_without_factroot:
    #     fact_kid_count += 1
    #     print(f"{fact._label=} {fact_kid_count=}")
    #     assert fact._active != None
    #     assert fact._active in (True, False)
    # assert fact_kid_count == len(fact_list_without_factroot)

    assert len(yao_agenda._fact_dict) == sum(
        fact._active != None for fact in yao_agenda._fact_dict.values()
    )


def test_AgendaUnit_calc_agenda_metrics_EveryOtherMonthReturnsCorrectObj_agenda_v001():
    # GIVEN
    yao_agenda = agenda_v001()
    minute_text = "day_minute"
    minute_road = yao_agenda.make_l1_road(minute_text)
    yao_agenda.set_belief(base=minute_road, pick=minute_road, open=0, nigh=1399)
    month_text = "month_week"
    month_road = yao_agenda.make_l1_road(month_text)
    yao_agenda.set_belief(base=month_road, pick=month_road)
    nations_text = "Nation-States"
    nations_road = yao_agenda.make_l1_road(nations_text)
    yao_agenda.set_belief(base=nations_road, pick=nations_road)
    mood_text = "Moods"
    mood_road = yao_agenda.make_l1_road(mood_text)
    yao_agenda.set_belief(base=mood_road, pick=mood_road)
    aaron_text = "Aaron Donald things effected by him"
    aaron_road = yao_agenda.make_l1_road(aaron_text)
    yao_agenda.set_belief(base=aaron_road, pick=aaron_road)
    internet_text = "Internet"
    internet_road = yao_agenda.make_l1_road(internet_text)
    yao_agenda.set_belief(base=internet_road, pick=internet_road)
    weekdays_text = "weekdays"
    weekdays_road = yao_agenda.make_l1_road(weekdays_text)
    yao_agenda.set_belief(base=weekdays_road, pick=weekdays_road)
    fact_dict = yao_agenda.get_fact_dict()
    print(f"{len(fact_dict)=}")

    casa_text = "casa"
    casa_road = yao_agenda.make_l1_road(casa_text)
    clean_text = "cleaning"
    clean_road = yao_agenda.make_road(casa_road, clean_text)
    mat_label = "deep clean play mat"
    mat_road = yao_agenda.make_road(clean_road, mat_label)
    assert from_list_get_active(road=mat_road, fact_dict=fact_dict) is False

    year_month_base = yao_agenda.make_l1_road("year_month")
    print(f"{year_month_base=}, {year_month_base=}")

    # WHEN
    yao_agenda.set_belief(base=year_month_base, pick=year_month_base, open=0, nigh=8)
    ced_week = yao_agenda.make_l1_road("ced_week")
    yao_agenda.set_belief(base=ced_week, pick=ced_week, open=0, nigh=4)
    yao_agenda.calc_agenda_metrics()

    # THEN
    print(f"{len(fact_dict)=}")
    print(f"{len(yao_agenda._factroot._beliefunits)=}")
    # from_list_get_active(road=mat_road, fact_dict=fact_dict)
    assert from_list_get_active(road=mat_road, fact_dict=yao_agenda._fact_dict)


def test_AgendaUnit_calc_agenda_metrics_CorrectlySetsEmpty_sum_healerhold_importance():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    assert sue_agenda._sum_healerhold_importance == 0
    assert sue_agenda._econ_dict == {}

    # WHEN
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert sue_agenda._sum_healerhold_importance == 0
    assert sue_agenda._econ_dict == {}


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_sum_healerhold_importance():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons()
    sue_agenda.add_partyunit("Sue")
    sue_agenda.calc_agenda_metrics()
    nation_road = sue_agenda.make_l1_road("nation-state")
    usa_road = sue_agenda.make_road(nation_road, "USA")
    oregon_road = sue_agenda.make_road(usa_road, "Oregon")
    sue_healerhold = healerhold_shop({"Sue"})
    sue_agenda.edit_fact_attr(oregon_road, problem_bool=True, healerhold=sue_healerhold)
    oregon_fact = sue_agenda.get_fact_obj(oregon_road)
    print(f"{oregon_fact._agenda_importance=}")
    assert sue_agenda._sum_healerhold_importance == 0
    assert oregon_fact._healerhold_importance == 0

    # WHEN
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert sue_agenda._sum_healerhold_importance == 0.038461538461538464
    assert oregon_fact._healerhold_importance == 1

    # WHEN
    week_road = sue_agenda.make_l1_road("weekdays")
    sue_agenda.edit_fact_attr(week_road, problem_bool=True)
    mon_road = sue_agenda.make_road(week_road, "Monday")
    sue_agenda.edit_fact_attr(mon_road, healerhold=sue_healerhold)
    mon_fact = sue_agenda.get_fact_obj(mon_road)
    # print(f"{mon_fact._problem_bool=} {mon_fact._agenda_importance=}")
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert sue_agenda._sum_healerhold_importance != 0.038461538461538464
    assert sue_agenda._sum_healerhold_importance == 0.06923076923076923
    assert oregon_fact._healerhold_importance == 0.5555555555555556
    assert mon_fact._healerhold_importance == 0.4444444444444444

    # WHEN
    tue_road = sue_agenda.make_road(week_road, "Tuesday")
    sue_agenda.edit_fact_attr(tue_road, healerhold=sue_healerhold)
    tue_fact = sue_agenda.get_fact_obj(tue_road)
    # print(f"{tue_fact._problem_bool=} {tue_fact._agenda_importance=}")
    # sat_road = sue_agenda.make_road(week_road, "Saturday")
    # sat_fact = sue_agenda.get_fact_obj(sat_road)
    # print(f"{sat_fact._problem_bool=} {sat_fact._agenda_importance=}")
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert sue_agenda._sum_healerhold_importance != 0.06923076923076923
    assert sue_agenda._sum_healerhold_importance == 0.1
    assert oregon_fact._healerhold_importance == 0.38461538461538464
    assert mon_fact._healerhold_importance == 0.3076923076923077
    assert tue_fact._healerhold_importance == 0.3076923076923077

    # WHEN
    sue_agenda.edit_fact_attr(week_road, healerhold=sue_healerhold)
    week_fact = sue_agenda.get_fact_obj(week_road)
    print(
        f"{week_fact._label=} {week_fact._problem_bool=} {week_fact._agenda_importance=}"
    )
    sue_agenda.calc_agenda_metrics()
    # THEN
    # display_facttree(sue_agenda, "Econ").show()
    assert sue_agenda._sum_healerhold_importance == 0
    assert oregon_fact._healerhold_importance == 0
    assert mon_fact._healerhold_importance == 0
    assert tue_fact._healerhold_importance == 0


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_econ_dict_v1():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons()
    sue_agenda.add_partyunit("Sue")
    sue_agenda.calc_agenda_metrics()
    nation_road = sue_agenda.make_l1_road("nation-state")
    usa_road = sue_agenda.make_road(nation_road, "USA")
    oregon_road = sue_agenda.make_road(usa_road, "Oregon")
    sue_healerhold = healerhold_shop({"Sue"})
    sue_agenda.edit_fact_attr(oregon_road, problem_bool=True, healerhold=sue_healerhold)
    assert len(sue_agenda._econ_dict) == 0
    assert sue_agenda._econ_dict.get(oregon_road) is None

    # WHEN
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert len(sue_agenda._econ_dict) == 1
    assert sue_agenda._econ_dict.get(oregon_road) != None

    # WHEN
    week_road = sue_agenda.make_l1_road("weekdays")
    sue_agenda.edit_fact_attr(week_road, problem_bool=True)
    mon_road = sue_agenda.make_road(week_road, "Monday")
    sue_agenda.edit_fact_attr(mon_road, healerhold=sue_healerhold)
    # mon_fact = sue_agenda.get_fact_obj(mon_road)
    # print(f"{mon_fact._problem_bool=} {mon_fact._agenda_importance=}")
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert len(sue_agenda._econ_dict) == 2
    assert sue_agenda._econ_dict.get(oregon_road) != None
    assert sue_agenda._econ_dict.get(mon_road) != None

    # WHEN
    tue_road = sue_agenda.make_road(week_road, "Tuesday")
    sue_agenda.edit_fact_attr(tue_road, healerhold=sue_healerhold)
    # tue_fact = sue_agenda.get_fact_obj(tue_road)
    # print(f"{tue_fact._problem_bool=} {tue_fact._agenda_importance=}")
    # sat_road = sue_agenda.make_road(week_road, "Saturday")
    # sat_fact = sue_agenda.get_fact_obj(sat_road)
    # print(f"{sat_fact._problem_bool=} {sat_fact._agenda_importance=}")
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert len(sue_agenda._econ_dict) == 3
    assert sue_agenda._econ_dict.get(oregon_road) != None
    assert sue_agenda._econ_dict.get(mon_road) != None
    assert sue_agenda._econ_dict.get(tue_road) != None

    # WHEN
    sue_agenda.edit_fact_attr(week_road, healerhold=sue_healerhold)
    week_fact = sue_agenda.get_fact_obj(week_road)
    print(
        f"{week_fact._label=} {week_fact._problem_bool=} {week_fact._agenda_importance=}"
    )
    sue_agenda.calc_agenda_metrics()
    # THEN
    # display_facttree(sue_agenda, "Econ").show()
    assert len(sue_agenda._econ_dict) == 0
    assert sue_agenda._econ_dict == {}


# def test_agenda_metrics_CorrectlySets_healers_dict():
#     # GIVEN
#     sue_text = "Sue"
#     bob_text = "Bob"
#     sue_agenda = get_agenda_with_4_levels_and_2reasons()
#     sue_agenda.add_partyunit(sue_text)
#     sue_agenda.add_partyunit(bob_text)
#     assert sue_agenda._healers_dict == {}

#     # WHEN
#     sue_agenda.calc_agenda_metrics()
#     # THEN
#     assert sue_agenda._healers_dict == {}

#     # GIVEN
#     nation_road = sue_agenda.make_l1_road("nation-state")
#     usa_road = sue_agenda.make_road(nation_road, "USA")
#     oregon_road = sue_agenda.make_road(usa_road, "Oregon")
#     sue_healerhold = healerhold_shop({sue_text})
#     sue_agenda.edit_fact_attr(oregon_road, problem_bool=True, healerhold=sue_healerhold)

#     week_road = sue_agenda.make_l1_road("weekdays")
#     bob_healerhold = healerhold_shop({bob_text})
#     sue_agenda.edit_fact_attr(week_road, problem_bool=True, healerhold=bob_healerhold)
#     assert sue_agenda._healers_dict == {}

#     # WHEN
#     sue_agenda.calc_agenda_metrics()

#     # THEN
#     assert len(sue_agenda._healers_dict) == 2
#     week_fact = sue_agenda.get_fact_obj(week_road)
#     assert sue_agenda._healers_dict.get(bob_text) == {week_road: week_fact}
#     oregon_fact = sue_agenda.get_fact_obj(oregon_road)
#     assert sue_agenda._healers_dict.get(sue_text) == {oregon_road: oregon_fact}


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_healers_dict():
    # GIVEN
    sue_text = "Sue"
    bob_text = "Bob"
    sue_agenda = get_agenda_with_4_levels_and_2reasons()
    sue_agenda.add_partyunit(sue_text)
    sue_agenda.add_partyunit(bob_text)
    assert sue_agenda._healers_dict == {}

    # WHEN
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert sue_agenda._healers_dict == {}

    # GIVEN
    nation_road = sue_agenda.make_l1_road("nation-state")
    usa_road = sue_agenda.make_road(nation_road, "USA")
    oregon_road = sue_agenda.make_road(usa_road, "Oregon")
    sue_healerhold = healerhold_shop({sue_text})
    sue_agenda.edit_fact_attr(oregon_road, problem_bool=True, healerhold=sue_healerhold)

    week_road = sue_agenda.make_l1_road("weekdays")
    bob_healerhold = healerhold_shop({bob_text})
    sue_agenda.edit_fact_attr(week_road, problem_bool=True, healerhold=bob_healerhold)
    assert sue_agenda._healers_dict == {}

    # WHEN
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert len(sue_agenda._healers_dict) == 2
    week_fact = sue_agenda.get_fact_obj(week_road)
    assert sue_agenda._healers_dict.get(bob_text) == {week_road: week_fact}
    oregon_fact = sue_agenda.get_fact_obj(oregon_road)
    assert sue_agenda._healers_dict.get(sue_text) == {oregon_road: oregon_fact}


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_econs_buildable_True():
    # GIVEN
    sue_text = "Sue"
    bob_text = "Bob"
    sue_agenda = get_agenda_with_4_levels_and_2reasons()
    sue_agenda.add_partyunit(sue_text)
    sue_agenda.add_partyunit(bob_text)
    assert sue_agenda._econs_buildable is False

    # WHEN
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert sue_agenda._econs_buildable

    # GIVEN
    nation_road = sue_agenda.make_l1_road("nation-state")
    usa_road = sue_agenda.make_road(nation_road, "USA")
    oregon_road = sue_agenda.make_road(usa_road, "Oregon")
    sue_healerhold = healerhold_shop({sue_text})
    sue_agenda.edit_fact_attr(oregon_road, problem_bool=True, healerhold=sue_healerhold)

    week_road = sue_agenda.make_l1_road("weekdays")
    bob_healerhold = healerhold_shop({bob_text})
    sue_agenda.edit_fact_attr(week_road, problem_bool=True, healerhold=bob_healerhold)

    # WHEN
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert sue_agenda._econs_buildable


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_econs_buildable_False():
    # GIVEN
    sue_text = "Sue"
    bob_text = "Bob"
    sue_agenda = get_agenda_with_4_levels_and_2reasons()
    sue_agenda.add_partyunit(sue_text)
    sue_agenda.add_partyunit(bob_text)
    assert sue_agenda._econs_buildable is False

    # WHEN
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert sue_agenda._econs_buildable

    # GIVEN
    nation_road = sue_agenda.make_l1_road("nation-state")
    usa_road = sue_agenda.make_road(nation_road, "USA")
    oregon_road = sue_agenda.make_road(usa_road, "Oregon")
    bend_text = "Be/nd"
    bend_road = sue_agenda.make_road(oregon_road, bend_text)
    sue_agenda.add_fact(factunit_shop(bend_text), oregon_road)
    sue_healerhold = healerhold_shop({sue_text})
    sue_agenda.edit_fact_attr(bend_road, problem_bool=True, healerhold=sue_healerhold)
    assert sue_agenda._econs_buildable

    # WHEN
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert sue_agenda._econs_buildable is False
