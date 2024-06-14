from src.agenda.graphic import display_oathtree
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
from src.agenda.oath import oathunit_shop
from src.agenda.reason_oath import (
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


def test_AgendaUnit_3AdvocatesNooathunit_shop():
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
    zia_agenda._oathroot.set_balancelink(
        balancelink=balancelink_shop(idea_id=IdeaID(rico_text), credor_weight=10)
    )
    zia_agenda._oathroot.set_balancelink(
        balancelink=balancelink_shop(idea_id=IdeaID(carm_text), credor_weight=10)
    )
    zia_agenda._oathroot.set_balancelink(
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


def test_AgendaUnit_calc_agenda_metrics_CreatesFullyPopulated_oath_dict():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons()

    # WHEN
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert len(sue_agenda._oath_dict) == 17


def test_AgendaUnit_calc_agenda_metrics_SetsSatiateStatusCorrectlyWhenBeliefSaysNo():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons()
    week_text = "weekdays"
    week_road = sue_agenda.make_l1_road(week_text)
    sun_text = "Sunday"
    sun_road = sue_agenda.make_road(week_road, sun_text)

    # for oath in sue_agenda._oath_dict.values():
    #     print(f"{casa_road=} {oath.get_road()=}")
    casa_text = "casa"
    casa_road = sue_agenda.make_l1_road(casa_text)
    assert sue_agenda.get_oath_obj(casa_road)._active is None

    # WHEN
    sue_agenda.set_belief(base=week_road, pick=sun_road)
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert sue_agenda._oath_dict != {}
    assert len(sue_agenda._oath_dict) == 17

    # for oath in sue_agenda._oath_dict.values():
    #     print(f"{casa_road=} {oath.get_road()=}")
    assert sue_agenda.get_oath_obj(casa_road)._active is False


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
    assert sue_agenda._oath_dict
    assert len(sue_agenda._oath_dict) == 17
    assert sue_agenda._oath_dict.get(casa_road)._active is False

    # WHEN
    states_text = "nation-state"
    states_road = sue_agenda.make_l1_road(states_text)
    usa_text = "USA"
    usa_road = sue_agenda.make_road(states_road, usa_text)
    sue_agenda.set_belief(base=states_road, pick=usa_road)

    # THEN
    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._oath_dict
    assert len(sue_agenda._oath_dict) == 17
    assert sue_agenda._oath_dict.get(casa_road)._active

    # WHEN
    france_text = "France"
    france_road = sue_agenda.make_road(states_road, france_text)
    sue_agenda.set_belief(base=states_road, pick=france_road)

    # THEN
    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._oath_dict
    assert len(sue_agenda._oath_dict) == 17
    assert sue_agenda._oath_dict.get(casa_road)._active is False


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_oath_dict():
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
    casa_oath = sue_agenda.get_oath_obj(casa_road)
    print(f"{sue_agenda._owner_id=} {len(casa_oath._reasonunits)=}")
    # print(f"{casa_oath._reasonunits=}")
    print(f"{sue_agenda._owner_id=} {len(sue_agenda._oathroot._beliefunits)=}")
    # print(f"{sue_agenda._oathroot._beliefunits=}")

    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._oath_dict
    assert len(sue_agenda._oath_dict) == 17

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
        _base_oath_active=True,
    )
    sta_lh = reasonheir_shop(
        base=state_road,
        premises={usa.need: usa},
        _status=True,
        _task=False,
        _base_oath_active=True,
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
    casa_oath = sue_agenda._oath_dict.get(casa_road)
    print(f"\nlook at {casa_oath.get_road()=}")
    assert casa_oath._parent_road == sue_agenda._real_id
    assert casa_oath._kids == {}
    assert casa_oath._weight == 30
    assert casa_oath._label == casa_text
    assert casa_oath._level == 1
    assert casa_oath._active
    assert casa_oath.pledge
    # print(f"{casa_oath._reasonheirs=}")
    x_reasonheir_state = casa_oath._reasonheirs[state_road]
    print(f"  {x_reasonheir_state=}")
    print(f"  {x_reasonheir_state._status=}\n")
    # assert casa_oath._reasonheirs == x1_reasonheirs

    assert len(casa_oath._reasonheirs) == len(x1_reasonheirs)
    week_reasonheir = casa_oath._reasonheirs.get(week_road)
    # usa_premise = week_reasonheir.premises.get(usa_road)
    print(f"    {casa_oath._label=}")
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

    # assert casa_oath._reasonunits == x1_reasonunits

    # print("iterate through every oath...")
    # for x_oath in oath_dict:
    #     if str(type(x_oath)).find(".oath.OathUnit'>") > 0:
    #         assert x_oath._active != None

    #     # print("")
    #     # print(f"{x_oath._label=}")
    #     # print(f"{len(x_oath._reasonunits)=}")
    #     print(
    #         f"  {x_oath._label} iterate through every reasonheir... {len(x_oath._reasonheirs)=} {x_oath._label=}"
    #     )
    #     # print(f"{x_oath._reasonheirs=}")
    #     for reason in x_oath._reasonheirs.values():
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
    x_agenda._oathroot._agenda_fund_onset = 13
    x_agenda._oathroot._agenda_fund_cease = 13
    x_agenda.get_oath_obj(casa_road)._agenda_fund_onset = 13
    x_agenda.get_oath_obj(casa_road)._agenda_fund_cease = 13
    x_agenda.get_oath_obj(catt_road)._agenda_fund_onset = 13
    x_agenda.get_oath_obj(catt_road)._agenda_fund_cease = 13
    x_agenda.get_oath_obj(week_road)._agenda_fund_onset = 13
    x_agenda.get_oath_obj(week_road)._agenda_fund_cease = 13

    assert x_agenda._oathroot._agenda_fund_onset == 13
    assert x_agenda._oathroot._agenda_fund_cease == 13
    assert x_agenda.get_oath_obj(casa_road)._agenda_fund_onset == 13
    assert x_agenda.get_oath_obj(casa_road)._agenda_fund_cease == 13
    assert x_agenda.get_oath_obj(catt_road)._agenda_fund_onset == 13
    assert x_agenda.get_oath_obj(catt_road)._agenda_fund_cease == 13
    assert x_agenda.get_oath_obj(week_road)._agenda_fund_onset == 13
    assert x_agenda.get_oath_obj(week_road)._agenda_fund_cease == 13

    # WHEN
    x_agenda.calc_agenda_metrics()

    # THEN
    assert x_agenda._oathroot._agenda_fund_onset != 13
    assert x_agenda._oathroot._agenda_fund_cease != 13
    assert x_agenda.get_oath_obj(casa_road)._agenda_fund_onset != 13
    assert x_agenda.get_oath_obj(casa_road)._agenda_fund_cease != 13
    assert x_agenda.get_oath_obj(catt_road)._agenda_fund_onset != 13
    assert x_agenda.get_oath_obj(catt_road)._agenda_fund_cease != 13
    assert x_agenda.get_oath_obj(week_road)._agenda_fund_onset != 13
    assert x_agenda.get_oath_obj(week_road)._agenda_fund_cease != 13


def test_AgendaUnit_calc_agenda_metrics_CorrectlyCalculatesOathAttr_agenda_fund():
    # GIVEN
    yao_agenda = agendaunit_shop("Yao", _weight=10)

    auto_text = "auto"
    auto_road = yao_agenda.make_l1_road(auto_text)
    auto_oath = oathunit_shop(auto_text, _weight=10)
    yao_agenda.add_l1_oath(auto_oath)

    barn_text = "barn"
    barn_road = yao_agenda.make_l1_road(barn_text)
    barn_oath = oathunit_shop(barn_text, _weight=60)
    yao_agenda.add_l1_oath(barn_oath)
    lamb_text = "lambs"
    lamb_road = yao_agenda.make_road(barn_road, lamb_text)
    lamb_oath = oathunit_shop(lamb_text, _weight=1)
    yao_agenda.add_oath(lamb_oath, parent_road=barn_road)
    duck_text = "ducks"
    duck_road = yao_agenda.make_road(barn_road, duck_text)
    duck_oath = oathunit_shop(duck_text, _weight=2)
    yao_agenda.add_oath(duck_oath, parent_road=barn_road)

    coal_text = "coal"
    coal_road = yao_agenda.make_l1_road(coal_text)
    coal_oath = oathunit_shop(coal_text, _weight=30)
    yao_agenda.add_l1_oath(coal_oath)

    assert yao_agenda._oathroot._agenda_fund_onset is None
    assert yao_agenda._oathroot._agenda_fund_cease is None
    assert yao_agenda.get_oath_obj(auto_road)._agenda_fund_onset is None
    assert yao_agenda.get_oath_obj(auto_road)._agenda_fund_cease is None
    assert yao_agenda.get_oath_obj(barn_road)._agenda_fund_onset is None
    assert yao_agenda.get_oath_obj(barn_road)._agenda_fund_cease is None
    assert yao_agenda.get_oath_obj(coal_road)._agenda_fund_onset is None
    assert yao_agenda.get_oath_obj(coal_road)._agenda_fund_cease is None
    lamb_before = yao_agenda.get_oath_obj(road=lamb_road)
    assert lamb_before._agenda_fund_onset is None
    assert lamb_before._agenda_fund_cease is None
    duck_before = yao_agenda.get_oath_obj(road=duck_road)
    assert duck_before._agenda_fund_onset is None
    assert duck_before._agenda_fund_cease is None

    # WHEN
    yao_agenda.calc_agenda_metrics()

    # THEN
    assert yao_agenda._oathroot._agenda_fund_onset == 0.0
    assert yao_agenda._oathroot._agenda_fund_cease == 1.0
    assert yao_agenda.get_oath_obj(auto_road)._agenda_fund_onset == 0.0
    assert yao_agenda.get_oath_obj(auto_road)._agenda_fund_cease == 0.1
    assert yao_agenda.get_oath_obj(barn_road)._agenda_fund_onset == 0.1
    assert yao_agenda.get_oath_obj(barn_road)._agenda_fund_cease == 0.7
    assert yao_agenda.get_oath_obj(coal_road)._agenda_fund_onset == 0.7
    assert yao_agenda.get_oath_obj(coal_road)._agenda_fund_cease == 1.0

    duck_after = yao_agenda.get_oath_obj(road=duck_road)
    assert duck_after._agenda_fund_onset == 0.1
    assert duck_after._agenda_fund_cease == 0.5
    lamb_after = yao_agenda.get_oath_obj(road=lamb_road)
    assert lamb_after._agenda_fund_onset == 0.5
    assert lamb_after._agenda_fund_cease == 0.7


def test_AgendaUnit_get_oath_list_without_root_CorrectlyCalculatesOathAttributes():
    # GIVEN
    x_agenda = get_agenda_with7amCleanTableReason()

    # WHEN
    oath_list_without_oathroot = x_agenda.get_oath_list_without_oathroot()
    oath_dict_with_oathroot = x_agenda.get_oath_dict()

    # THEN
    assert len(oath_list_without_oathroot) == 28
    assert len(oath_list_without_oathroot) + 1 == len(oath_dict_with_oathroot)

    # for oath in x_agenda.get_oath_list_without_oathroot():
    #     assert str(type(oath)).find(".oath.OathUnit'>") > 0

    # for oath in x_agenda.get_oath_list_without_oathroot():
    #     print(f"{oath._label=}")


def test_AgendaUnit_calc_agenda_metrics_CorrectlyCalculatesRangeAttributes():
    # GIVEN
    sue_agenda = get_agenda_with7amCleanTableReason()
    sue_agenda.calc_agenda_metrics()
    house_text = "housemanagement"
    house_road = sue_agenda.make_l1_road(house_text)
    clean_text = "clean table"
    clean_road = sue_agenda.make_road(house_road, clean_text)
    assert sue_agenda._oath_dict.get(clean_road)._active is False

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
    assert sue_agenda._oath_dict.get(clean_road)._active

    # WHEN
    # set beliefs as 8am to 10am
    day24hr_open = 8.0
    day24hr_nigh = 10.0
    print(sue_agenda._oathroot._beliefunits[day24hr_road])
    sue_agenda.set_belief(
        base=day24hr_base, pick=day24hr_pick, open=day24hr_open, nigh=day24hr_nigh
    )
    print(sue_agenda._oathroot._beliefunits[day24hr_road])
    print(sue_agenda._oathroot._kids[house_text]._kids[clean_text]._reasonunits)
    # sue_agenda._oathroot._kids["housemanagement"]._kids[clean_text]._active = None

    # THEN
    sue_agenda.calc_agenda_metrics()
    assert sue_agenda._oath_dict.get(clean_road)._active is False


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
    # print(f"{len(yao_agenda._oathroot._kids)=}")
    ulty_text = "Ultimate Frisbee"
    ulty_road = yao_agenda.make_l1_road(ulty_text)

    # if yao_agenda._oathroot._kids["Ultimate Frisbee"]._label == "Ultimate Frisbee":
    assert yao_agenda._oathroot._kids[ulty_text]._reasonunits != None
    assert yao_agenda._owner_id != None

    # for belief in yao_agenda._oathroot._beliefunits.values():
    #     print(f"{belief=}")

    yao_agenda.calc_agenda_metrics()
    # print(f"{str(type(oath))=}")
    # print(f"{len(oath_dict)=}")
    laundry_text = "laundry monday"
    casa_road = yao_agenda.make_l1_road("casa")
    cleaning_road = yao_agenda.make_road(casa_road, "cleaning")
    laundry_road = yao_agenda.make_road(cleaning_road, laundry_text)

    # for oath in oath_dict:
    #     assert (
    #         str(type(oath)).find(".oath.OathUnit'>") > 0
    #         or str(type(oath)).find(".oath.OathUnit'>") > 0
    #     )
    #     # print(f"{oath._label=}")
    #     if oath._label == laundry_text:
    #         for reason in oath._reasonunits.values():
    #             print(f"{oath._label=} {reason.base=}")  # {reason.premises=}")
    # assert oath._active is False
    assert yao_agenda._oath_dict.get(laundry_road)._active is False

    # WHEN
    week_text = "weekdays"
    week_road = yao_agenda.make_l1_road(week_text)
    mon_text = "Monday"
    mon_road = yao_agenda.make_road(week_road, mon_text)
    yao_agenda.set_belief(base=week_road, pick=mon_road)
    yao_agenda.calc_agenda_metrics()

    # THEN
    assert yao_agenda._oath_dict.get(laundry_road)._active is False


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
    x_oathroot = yao_agenda.get_oath_obj(yao_agenda._real_id)
    x_oathroot.set_reasonunit(reason=mt_reasonunit)
    # print(f"{yao_agenda._reasonunits[week_road].base=}")
    # print(f"{yao_agenda._reasonunits[week_road].premises[mon_road].need=}")
    # print(f"{yao_agenda._reasonunits[week_road].premises[tue_road].need=}")
    week_reasonunit = x_oathroot._reasonunits[week_road]
    print(f"{week_reasonunit.premises=}")
    premise_mon = week_reasonunit.premises.get(mon_road)
    premise_tue = week_reasonunit.premises.get(tue_road)
    assert premise_mon
    assert premise_mon == mt_reasonunit.premises[premise_mon.need]
    assert premise_tue
    assert premise_tue == mt_reasonunit.premises[premise_tue.need]
    assert week_reasonunit == mt_reasonunit

    # WHEN
    oath_dict = yao_agenda.get_oath_dict()

    # THEN
    gen_week_reasonheir = x_oathroot.get_reasonheir(week_road)
    gen_mon_premise = gen_week_reasonheir.premises.get(mon_road)
    assert gen_mon_premise._status == mt_reasonheir.premises.get(mon_road)._status
    assert gen_mon_premise == mt_reasonheir.premises.get(mon_road)
    assert gen_week_reasonheir.premises == mt_reasonheir.premises
    assert gen_week_reasonheir == mt_reasonheir

    casa_text = "casa"
    casa_road = yao_agenda.make_l1_road(casa_text)
    bird_text = "say hi to birds"
    bird_road = yao_agenda.make_road(casa_road, bird_text)
    assert from_list_get_active(road=bird_road, oath_dict=oath_dict) is False

    # yao_agenda.set_belief(base=week_road, pick=mon_road)
    # oath_dict = yao_agenda.get_oath_dict()
    # casa_oath = x_oathroot._kids[casa_text]
    # twee_oath = casa_oath._kids[bird_text]
    # print(f"{len(x_oathroot._reasonheirs)=}")
    # print(f"{len(casa_oath._reasonheirs)=}")
    # print(f"{len(twee_oath._reasonheirs)=}")

    # assert YR.get_active(road=bird_oath, oath_dict=oath_dict) == True

    # yao_agenda.set_belief(base=f"{yao_agenda._real_id},weekdays", pick=f"{yao_agenda._real_id},weekdays,Tuesday")
    # oath_dict = yao_agenda.get_oath_dict()
    # assert YR.get_active(road=bird_oath, oath_dict=oath_dict) == True

    # yao_agenda.set_belief(base=f"{yao_agenda._real_id},weekdays", pick=f"{yao_agenda._real_id},weekdays,Wednesday")
    # oath_dict = yao_agenda.get_oath_dict()
    # assert YR.get_active(road=bird_oath, oath_dict=oath_dict) is False


def test_AgendaUnit_calc_agenda_metrics_CorrectlySetsOathUnitsActiveWithEvery6WeeksReason_agenda_v001():
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
    print(f"{len(yao_agenda._oath_dict)=}")

    casa_road = yao_agenda.make_l1_road("casa")
    cleaning_road = yao_agenda.make_road(casa_road, "cleaning")
    clean_couch_road = yao_agenda.make_road(
        cleaning_road, "clean sheets couch blankets"
    )
    clean_sheet_oath = yao_agenda.get_oath_obj(clean_couch_road)
    # print(f"{clean_sheet_oath._reasonunits.values()=}")
    ced_week_reason = clean_sheet_oath._reasonunits.get(ced_week_base)
    ced_week_premise = ced_week_reason.premises.get(ced_week_base)
    print(
        f"{clean_sheet_oath._label=} {ced_week_reason.base=} {ced_week_premise.need=}"
    )
    # print(f"{clean_sheet_oath._label=} {ced_week_reason.base=} {premise_x=}")
    premise_divisor = ced_week_premise.divisor
    premise_open = ced_week_premise.open
    premise_nigh = ced_week_premise.nigh
    # print(f"{oath._reasonunits=}")
    assert clean_sheet_oath._active is False

    # for oath in oath_dict:
    #     # print(f"{oath._parent_road=}")
    #     if oath._label == "clean sheets couch blankets":
    #         print(f"{oath.get_road()=}")

    assert premise_divisor == 6
    assert premise_open == 1
    print(
        f"There exists a oath with a reason_base {ced_week_base} that also has lemmet div =6 and open/nigh =1"
    )
    # print(f"{len(oath_dict)=}")
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
    print(f"{yao_agenda._oathroot._beliefunits=}")
    yao_agenda.calc_agenda_metrics()

    # THEN
    week_text = "ced_week"
    week_road = yao_agenda.make_l1_road(week_text)
    casa_road = yao_agenda.make_l1_road("casa")
    cleaning_road = yao_agenda.make_road(casa_road, "cleaning")
    clean_couch_text = "clean sheets couch blankets"
    clean_couch_road = yao_agenda.make_road(cleaning_road, clean_couch_text)
    clean_couch_oath = yao_agenda.get_oath_obj(road=clean_couch_road)
    week_reason = clean_couch_oath._reasonunits.get(week_road)
    week_premise = week_reason.premises.get(week_road)
    print(f"{clean_couch_oath._label=} {week_reason.base=} {week_premise=}")
    assert week_premise.divisor == 6 and week_premise.open == 1


def test_AgendaUnit_calc_agenda_metrics_EveryOathHasActiveStatus_agenda_v001():
    # GIVEN
    yao_agenda = agenda_v001()

    # WHEN
    yao_agenda.calc_agenda_metrics()

    # THEN
    print(f"{len(yao_agenda._oath_dict)=}")
    # first_oath_kid_count = 0
    # first_oath_kid_none_count = 0
    # first_oath_kid_true_count = 0
    # first_oath_kid_false_count = 0
    # for oath in oath_list:
    #     if str(type(oath)).find(".oath.OathUnit'>") > 0:
    #         first_oath_kid_count += 1
    #         if oath._active is None:
    #             first_oath_kid_none_count += 1
    #         elif oath._active:
    #             first_oath_kid_true_count += 1
    #         elif oath._active is False:
    #             first_oath_kid_false_count += 1

    # print(f"{first_oath_kid_count=}")
    # print(f"{first_oath_kid_none_count=}")
    # print(f"{first_oath_kid_true_count=}")
    # print(f"{first_oath_kid_false_count=}")

    # oath_kid_count = 0
    # for oath in oath_list_without_oathroot:
    #     oath_kid_count += 1
    #     print(f"{oath._label=} {oath_kid_count=}")
    #     assert oath._active != None
    #     assert oath._active in (True, False)
    # assert oath_kid_count == len(oath_list_without_oathroot)

    assert len(yao_agenda._oath_dict) == sum(
        oath._active != None for oath in yao_agenda._oath_dict.values()
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
    oath_dict = yao_agenda.get_oath_dict()
    print(f"{len(oath_dict)=}")

    casa_text = "casa"
    casa_road = yao_agenda.make_l1_road(casa_text)
    clean_text = "cleaning"
    clean_road = yao_agenda.make_road(casa_road, clean_text)
    mat_label = "deep clean play mat"
    mat_road = yao_agenda.make_road(clean_road, mat_label)
    assert from_list_get_active(road=mat_road, oath_dict=oath_dict) is False

    year_month_base = yao_agenda.make_l1_road("year_month")
    print(f"{year_month_base=}, {year_month_base=}")

    # WHEN
    yao_agenda.set_belief(base=year_month_base, pick=year_month_base, open=0, nigh=8)
    ced_week = yao_agenda.make_l1_road("ced_week")
    yao_agenda.set_belief(base=ced_week, pick=ced_week, open=0, nigh=4)
    yao_agenda.calc_agenda_metrics()

    # THEN
    print(f"{len(oath_dict)=}")
    print(f"{len(yao_agenda._oathroot._beliefunits)=}")
    # from_list_get_active(road=mat_road, oath_dict=oath_dict)
    assert from_list_get_active(road=mat_road, oath_dict=yao_agenda._oath_dict)


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
    sue_agenda.edit_oath_attr(oregon_road, problem_bool=True, healerhold=sue_healerhold)
    oregon_oath = sue_agenda.get_oath_obj(oregon_road)
    print(f"{oregon_oath._agenda_importance=}")
    assert sue_agenda._sum_healerhold_importance == 0
    assert oregon_oath._healerhold_importance == 0

    # WHEN
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert sue_agenda._sum_healerhold_importance == 0.038461538461538464
    assert oregon_oath._healerhold_importance == 1

    # WHEN
    week_road = sue_agenda.make_l1_road("weekdays")
    sue_agenda.edit_oath_attr(week_road, problem_bool=True)
    mon_road = sue_agenda.make_road(week_road, "Monday")
    sue_agenda.edit_oath_attr(mon_road, healerhold=sue_healerhold)
    mon_oath = sue_agenda.get_oath_obj(mon_road)
    # print(f"{mon_oath._problem_bool=} {mon_oath._agenda_importance=}")
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert sue_agenda._sum_healerhold_importance != 0.038461538461538464
    assert sue_agenda._sum_healerhold_importance == 0.06923076923076923
    assert oregon_oath._healerhold_importance == 0.5555555555555556
    assert mon_oath._healerhold_importance == 0.4444444444444444

    # WHEN
    tue_road = sue_agenda.make_road(week_road, "Tuesday")
    sue_agenda.edit_oath_attr(tue_road, healerhold=sue_healerhold)
    tue_oath = sue_agenda.get_oath_obj(tue_road)
    # print(f"{tue_oath._problem_bool=} {tue_oath._agenda_importance=}")
    # sat_road = sue_agenda.make_road(week_road, "Saturday")
    # sat_oath = sue_agenda.get_oath_obj(sat_road)
    # print(f"{sat_oath._problem_bool=} {sat_oath._agenda_importance=}")
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert sue_agenda._sum_healerhold_importance != 0.06923076923076923
    assert sue_agenda._sum_healerhold_importance == 0.1
    assert oregon_oath._healerhold_importance == 0.38461538461538464
    assert mon_oath._healerhold_importance == 0.3076923076923077
    assert tue_oath._healerhold_importance == 0.3076923076923077

    # WHEN
    sue_agenda.edit_oath_attr(week_road, healerhold=sue_healerhold)
    week_oath = sue_agenda.get_oath_obj(week_road)
    print(
        f"{week_oath._label=} {week_oath._problem_bool=} {week_oath._agenda_importance=}"
    )
    sue_agenda.calc_agenda_metrics()
    # THEN
    # display_oathtree(sue_agenda, "Econ").show()
    assert sue_agenda._sum_healerhold_importance == 0
    assert oregon_oath._healerhold_importance == 0
    assert mon_oath._healerhold_importance == 0
    assert tue_oath._healerhold_importance == 0


def test_AgendaUnit_calc_agenda_metrics_CorrectlySets_econ_dict_v1():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels_and_2reasons()
    sue_agenda.add_partyunit("Sue")
    sue_agenda.calc_agenda_metrics()
    nation_road = sue_agenda.make_l1_road("nation-state")
    usa_road = sue_agenda.make_road(nation_road, "USA")
    oregon_road = sue_agenda.make_road(usa_road, "Oregon")
    sue_healerhold = healerhold_shop({"Sue"})
    sue_agenda.edit_oath_attr(oregon_road, problem_bool=True, healerhold=sue_healerhold)
    assert len(sue_agenda._econ_dict) == 0
    assert sue_agenda._econ_dict.get(oregon_road) is None

    # WHEN
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert len(sue_agenda._econ_dict) == 1
    assert sue_agenda._econ_dict.get(oregon_road) != None

    # WHEN
    week_road = sue_agenda.make_l1_road("weekdays")
    sue_agenda.edit_oath_attr(week_road, problem_bool=True)
    mon_road = sue_agenda.make_road(week_road, "Monday")
    sue_agenda.edit_oath_attr(mon_road, healerhold=sue_healerhold)
    # mon_oath = sue_agenda.get_oath_obj(mon_road)
    # print(f"{mon_oath._problem_bool=} {mon_oath._agenda_importance=}")
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert len(sue_agenda._econ_dict) == 2
    assert sue_agenda._econ_dict.get(oregon_road) != None
    assert sue_agenda._econ_dict.get(mon_road) != None

    # WHEN
    tue_road = sue_agenda.make_road(week_road, "Tuesday")
    sue_agenda.edit_oath_attr(tue_road, healerhold=sue_healerhold)
    # tue_oath = sue_agenda.get_oath_obj(tue_road)
    # print(f"{tue_oath._problem_bool=} {tue_oath._agenda_importance=}")
    # sat_road = sue_agenda.make_road(week_road, "Saturday")
    # sat_oath = sue_agenda.get_oath_obj(sat_road)
    # print(f"{sat_oath._problem_bool=} {sat_oath._agenda_importance=}")
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert len(sue_agenda._econ_dict) == 3
    assert sue_agenda._econ_dict.get(oregon_road) != None
    assert sue_agenda._econ_dict.get(mon_road) != None
    assert sue_agenda._econ_dict.get(tue_road) != None

    # WHEN
    sue_agenda.edit_oath_attr(week_road, healerhold=sue_healerhold)
    week_oath = sue_agenda.get_oath_obj(week_road)
    print(
        f"{week_oath._label=} {week_oath._problem_bool=} {week_oath._agenda_importance=}"
    )
    sue_agenda.calc_agenda_metrics()
    # THEN
    # display_oathtree(sue_agenda, "Econ").show()
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
#     sue_agenda.edit_oath_attr(oregon_road, problem_bool=True, healerhold=sue_healerhold)

#     week_road = sue_agenda.make_l1_road("weekdays")
#     bob_healerhold = healerhold_shop({bob_text})
#     sue_agenda.edit_oath_attr(week_road, problem_bool=True, healerhold=bob_healerhold)
#     assert sue_agenda._healers_dict == {}

#     # WHEN
#     sue_agenda.calc_agenda_metrics()

#     # THEN
#     assert len(sue_agenda._healers_dict) == 2
#     week_oath = sue_agenda.get_oath_obj(week_road)
#     assert sue_agenda._healers_dict.get(bob_text) == {week_road: week_oath}
#     oregon_oath = sue_agenda.get_oath_obj(oregon_road)
#     assert sue_agenda._healers_dict.get(sue_text) == {oregon_road: oregon_oath}


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
    sue_agenda.edit_oath_attr(oregon_road, problem_bool=True, healerhold=sue_healerhold)

    week_road = sue_agenda.make_l1_road("weekdays")
    bob_healerhold = healerhold_shop({bob_text})
    sue_agenda.edit_oath_attr(week_road, problem_bool=True, healerhold=bob_healerhold)
    assert sue_agenda._healers_dict == {}

    # WHEN
    sue_agenda.calc_agenda_metrics()

    # THEN
    assert len(sue_agenda._healers_dict) == 2
    week_oath = sue_agenda.get_oath_obj(week_road)
    assert sue_agenda._healers_dict.get(bob_text) == {week_road: week_oath}
    oregon_oath = sue_agenda.get_oath_obj(oregon_road)
    assert sue_agenda._healers_dict.get(sue_text) == {oregon_road: oregon_oath}


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
    sue_agenda.edit_oath_attr(oregon_road, problem_bool=True, healerhold=sue_healerhold)

    week_road = sue_agenda.make_l1_road("weekdays")
    bob_healerhold = healerhold_shop({bob_text})
    sue_agenda.edit_oath_attr(week_road, problem_bool=True, healerhold=bob_healerhold)

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
    sue_agenda.add_oath(oathunit_shop(bend_text), oregon_road)
    sue_healerhold = healerhold_shop({sue_text})
    sue_agenda.edit_oath_attr(bend_road, problem_bool=True, healerhold=sue_healerhold)
    assert sue_agenda._econs_buildable

    # WHEN
    sue_agenda.calc_agenda_metrics()
    # THEN
    assert sue_agenda._econs_buildable is False
