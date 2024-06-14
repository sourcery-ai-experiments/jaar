from src._instrument.python import x_is_json, get_dict_from_json
from src._road.road import default_road_delimiter_if_none
from src.agenda.idea import ideaunit_shop, balancelink_shop
from src.agenda.party import partylink_shop
from src.agenda.healer import healerhold_shop
from src.agenda.reason_assign import assignedunit_shop
from src.agenda.reason_fact import beliefunit_shop
from src.agenda.fact import factunit_shop
from src.agenda.agenda import (
    agendaunit_shop,
    get_from_json as agendaunit_get_from_json,
    get_dict_of_agenda_from_dict,
)
from src.agenda.examples.example_agendas import (
    agenda_v001 as example_agendas_agenda_v001,
    get_agenda_x1_3levels_1reason_1beliefs as example_agendas_get_agenda_x1_3levels_1reason_1beliefs,
    get_agenda_base_time_example as example_agendas_get_agenda_base_time_example,
)
from pytest import raises as pytest_raises


def test_AgendaUnit_get_dict_ReturnsDictObject():
    # GIVEN
    x_agenda = example_agendas_agenda_v001()
    day_hour_text = "day_hour"
    day_hour_road = x_agenda.make_l1_road(day_hour_text)
    day_hour_fact = x_agenda.get_fact_obj(day_hour_road)
    day_hour_fact._originunit.set_originlink(party_id="Bob", weight=2)
    x_agenda.set_belief(
        base=day_hour_road,
        pick=day_hour_road,
        open=0,
        nigh=23,
    )
    time_minute = x_agenda.make_l1_road("day_minute")
    x_agenda.set_belief(base=time_minute, pick=time_minute, open=0, nigh=1440)
    yao_text = "Yao"
    x_agenda._originunit.set_originlink(yao_text, 1)
    agenda_weight = 23
    x_agenda._weight = agenda_weight
    x_party_credor_pool = 22
    x_party_debtor_pool = 22
    x_agenda.set_party_credor_pool(x_party_credor_pool)
    x_agenda.set_party_debtor_pool(x_party_debtor_pool)
    override_text = "override"
    x_agenda.set_meld_strategy(override_text)
    x_last_atom_id = 77
    x_agenda.set_last_atom_id(x_last_atom_id)

    # WHEN
    agenda_dict = x_agenda.get_dict()

    # THEN
    assert agenda_dict != None
    assert str(type(agenda_dict)) == "<class 'dict'>"
    assert agenda_dict["_owner_id"] == x_agenda._owner_id
    assert agenda_dict["_real_id"] == x_agenda._real_id
    assert agenda_dict["_weight"] == x_agenda._weight
    assert agenda_dict["_weight"] == agenda_weight
    assert agenda_dict["_max_tree_traverse"] == x_agenda._max_tree_traverse
    assert agenda_dict["_road_delimiter"] == x_agenda._road_delimiter
    assert agenda_dict["_party_credor_pool"] == x_agenda._party_credor_pool
    assert agenda_dict["_party_debtor_pool"] == x_agenda._party_debtor_pool
    assert agenda_dict["_party_debtor_pool"] == x_agenda._party_debtor_pool
    assert agenda_dict["_meld_strategy"] == x_agenda._meld_strategy
    assert agenda_dict["_last_atom_id"] == x_agenda._last_atom_id
    assert len(agenda_dict["_partys"]) == len(x_agenda._partys)
    assert len(agenda_dict["_partys"]) != 12
    assert len(agenda_dict["_ideas"]) == 12
    assert len(agenda_dict["_ideas"]) != len(x_agenda._ideas)

    x_factroot = x_agenda._factroot
    factroot_dict = agenda_dict["_factroot"]
    _kids = "_kids"
    _range_source_road = "_range_source_road"
    _numeric_road = "_numeric_road"
    assert x_factroot._label == x_agenda._real_id
    assert factroot_dict["_label"] == x_factroot._label
    assert factroot_dict["_weight"] != agenda_weight
    assert factroot_dict["_weight"] == x_factroot._weight
    assert len(factroot_dict[_kids]) == len(x_factroot._kids)

    # check an factkid._range_source_road attribute
    month_week_text = "month_week"
    month_week_road = x_agenda.make_l1_road(month_week_text)
    month_week_fact_x = x_agenda.get_fact_obj(month_week_road)
    print("check real_id,month_week...range_source_road equal to...")
    month_week_special_dict = factroot_dict[_kids][month_week_text][_range_source_road]
    assert month_week_special_dict != None
    assert month_week_special_dict == x_agenda.make_l1_road("ced_week")
    assert month_week_special_dict == month_week_fact_x._range_source_road

    # check an factkid._numeric_road attribute
    num1_text = "numeric_road_test"
    num1_road = x_agenda.make_l1_road(num1_text)
    num1_fact_x = x_agenda.get_fact_obj(num1_road)
    print(f"check {num1_road}...numeric_road equal to...")
    num1_dict_numeric_road = factroot_dict[_kids][num1_text][_numeric_road]
    assert num1_dict_numeric_road != None
    assert num1_dict_numeric_road == month_week_road
    assert num1_dict_numeric_road == num1_fact_x._numeric_road

    originunit_text = "_originunit"
    day_hour_originunit_dict = factroot_dict[_kids][day_hour_text][originunit_text]
    assert day_hour_originunit_dict == day_hour_fact._originunit.get_dict()
    _links = "_links"
    x_agenda_originlink = agenda_dict[originunit_text][_links][yao_text]
    print(f"{x_agenda_originlink=}")
    assert x_agenda_originlink
    assert x_agenda_originlink["party_id"] == yao_text
    assert x_agenda_originlink["weight"] == 1


def test_AgendaUnit_get_dict_ReturnsDictWith_factroot_assignedunit():
    # GIVEN
    run_text = "runners"
    tom_agenda = agendaunit_shop("Tom")
    x_assignedunit = assignedunit_shop()
    x_assignedunit.set_suffidea(idea_id=run_text)
    tom_agenda.edit_fact_attr(assignedunit=x_assignedunit, road=tom_agenda._real_id)

    # WHEN
    agenda_dict = tom_agenda.get_dict()
    factroot_dict = agenda_dict.get("_factroot")

    # THEN
    assert factroot_dict["_assignedunit"] == x_assignedunit.get_dict()
    assert factroot_dict["_assignedunit"] == {"_suffideas": {run_text: run_text}}


def test_AgendaUnit_get_dict_ReturnsDictWith_factroot_healerhold():
    # GIVEN
    tom_agenda = agendaunit_shop("Tom")
    yao_text = "Yao"
    tom_agenda.add_partyunit(yao_text)
    run_text = ",runners"
    run_ideaunit = ideaunit_shop(run_text)
    run_ideaunit.set_partylink(partylink_shop(yao_text))
    tom_agenda.set_ideaunit(run_ideaunit)
    run_healerhold = healerhold_shop()
    run_healerhold.set_idea_id(x_idea_id=run_text)
    tom_agenda.edit_fact_attr(road=tom_agenda._real_id, healerhold=run_healerhold)

    # WHEN
    agenda_dict = tom_agenda.get_dict()
    factroot_dict = agenda_dict.get("_factroot")

    # THEN
    assert factroot_dict["_healerhold"] == run_healerhold.get_dict()


def test_AgendaUnit_get_dict_ReturnsDictWith_factkid_AssignedUnit():
    # GIVEN
    tom_agenda = agendaunit_shop("Tom")
    run_text = ",run"
    tom_agenda.set_ideaunit(y_ideaunit=ideaunit_shop(run_text))

    morn_text = "morning"
    morn_road = tom_agenda.make_l1_road(morn_text)
    tom_agenda.add_l1_fact(factunit_shop(morn_text))
    x_assignedunit = assignedunit_shop()
    x_assignedunit.set_suffidea(idea_id=run_text)
    tom_agenda.edit_fact_attr(assignedunit=x_assignedunit, road=morn_road)

    # WHEN
    agenda_dict = tom_agenda.get_dict()
    factroot_dict = agenda_dict.get("_factroot")

    # THEN
    _kids = "_kids"
    _assignedunit = "_assignedunit"

    assigned_dict_x = factroot_dict[_kids][morn_text][_assignedunit]
    assert assigned_dict_x == x_assignedunit.get_dict()
    assert assigned_dict_x == {"_suffideas": {run_text: run_text}}


def test_AgendaUnit_get_json_ReturnsCorrectJSON_SimpleExample():
    # GIVEN
    zia_agenda = example_agendas_get_agenda_x1_3levels_1reason_1beliefs()
    tiger_real_id = "tiger"
    zia_agenda.set_real_id(tiger_real_id)
    seven_int = 7
    zia_agenda._planck = seven_int
    x_penny = 0.3
    zia_agenda._penny = x_penny
    override_text = "override"
    zia_agenda.set_meld_strategy(override_text)
    yao_text = "Yao"
    zia_agenda.add_partyunit(yao_text)
    run_text = ",runners"
    run_ideaunit = ideaunit_shop(run_text)
    run_ideaunit.set_partylink(partylink_shop(yao_text))
    zia_agenda.set_ideaunit(run_ideaunit)
    run_healerhold = healerhold_shop({run_text})
    zia_agenda.edit_fact_attr(road=zia_agenda._real_id, healerhold=run_healerhold)
    zia_agenda.edit_fact_attr(road=zia_agenda._real_id, problem_bool=True)

    # WHEN
    x_json = zia_agenda.get_json()

    # THEN
    _kids = "_kids"

    assert x_json != None
    assert True == x_is_json(x_json)
    agenda_dict = get_dict_from_json(x_json)

    assert agenda_dict["_owner_id"] == zia_agenda._owner_id
    assert agenda_dict["_real_id"] == zia_agenda._real_id
    assert agenda_dict["_weight"] == zia_agenda._weight
    assert agenda_dict["_meld_strategy"] == zia_agenda._meld_strategy
    assert agenda_dict["_planck"] == zia_agenda._planck
    assert agenda_dict["_penny"] == zia_agenda._penny
    with pytest_raises(Exception) as excinfo:
        agenda_dict["_party_credor_pool"]
    assert str(excinfo.value) == "'_party_credor_pool'"
    with pytest_raises(Exception) as excinfo:
        agenda_dict["_party_debtor_pool"]
    assert str(excinfo.value) == "'_party_debtor_pool'"
    with pytest_raises(Exception) as excinfo:
        agenda_dict["_last_atom_id"]

    x_factroot = zia_agenda._factroot
    factroot_dict = agenda_dict.get("_factroot")

    assert len(factroot_dict[_kids]) == len(x_factroot._kids)

    shave_text = "shave"
    shave_dict = factroot_dict[_kids][shave_text]
    shave_beliefunits = shave_dict["_beliefunits"]
    print(f"{shave_beliefunits=}")
    assert len(shave_beliefunits) == 1
    assert len(shave_beliefunits) == len(x_factroot._kids[shave_text]._beliefunits)
    factroot_healerhold = factroot_dict["_healerhold"]
    print(f"{factroot_healerhold=}")
    assert len(factroot_healerhold) == 1
    assert x_factroot._healerhold.any_idea_id_exists()
    assert x_factroot._problem_bool


def test_AgendaUnit_get_json_ReturnsCorrectJSON_BigExample():
    # GIVEN
    yao_agenda = example_agendas_agenda_v001()
    day_hour_text = "day_hour"
    day_hour_road = yao_agenda.make_l1_road(day_hour_text)
    yao_agenda.set_belief(base=day_hour_road, pick=day_hour_road, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = yao_agenda.make_l1_road(day_min_text)
    yao_agenda.set_belief(base=day_min_road, pick=day_min_road, open=0, nigh=59)
    beliefunit_x = beliefunit_shop(day_min_road, day_min_road, 5, 59)
    yao_agenda.edit_fact_attr(road=beliefunit_x.base, beliefunit=beliefunit_x)
    yao_agenda.set_max_tree_traverse(int_x=2)
    yao_text = "Yao"
    yao_agenda._originunit.set_originlink(yao_text, 1)

    # WHEN
    agenda_dict = get_dict_from_json(json_x=yao_agenda.get_json())

    # THEN
    _kids = "_kids"
    assert agenda_dict["_owner_id"] == yao_agenda._owner_id
    assert agenda_dict["_real_id"] == yao_agenda._real_id
    assert agenda_dict["_weight"] == yao_agenda._weight
    assert agenda_dict["_max_tree_traverse"] == 2
    assert agenda_dict["_max_tree_traverse"] == yao_agenda._max_tree_traverse
    assert agenda_dict["_road_delimiter"] == yao_agenda._road_delimiter

    x_factroot = yao_agenda._factroot
    factroot_dict = agenda_dict.get("_factroot")
    assert len(factroot_dict[_kids]) == len(x_factroot._kids)

    kids = factroot_dict[_kids]
    day_min_dict = kids[day_min_text]
    day_min_beliefunits_dict = day_min_dict["_beliefunits"]
    day_min_fact_x = yao_agenda.get_fact_obj(day_min_road)
    print(f"{day_min_beliefunits_dict=}")
    assert len(day_min_beliefunits_dict) == 1
    assert len(day_min_beliefunits_dict) == len(day_min_fact_x._beliefunits)

    _reasonunits = "_reasonunits"
    cont_text = "Freelancing"
    ulti_text = "Ultimate Frisbee"
    cont_road = yao_agenda.make_l1_road(cont_text)
    ulti_road = yao_agenda.make_l1_road(ulti_text)
    cont_fact = yao_agenda.get_fact_obj(cont_road)
    ulti_fact = yao_agenda.get_fact_obj(ulti_road)
    cont_reasonunits_dict = factroot_dict[_kids][cont_text][_reasonunits]
    ulti_reasonunits_dict = factroot_dict[_kids][ulti_text][_reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_fact._reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_fact._reasonunits)
    originunit_text = "_originunit"
    _links = "_links"
    assert len(agenda_dict[originunit_text][_links])


def test_agendaunit_get_from_json_ReturnsCorrectObjSimpleExample():
    # GIVEN
    zia_agenda = example_agendas_get_agenda_x1_3levels_1reason_1beliefs()
    zia_agenda.set_max_tree_traverse(23)
    tiger_real_id = "tiger"
    zia_agenda.set_real_id(tiger_real_id)
    zia_planck = 0.5
    zia_agenda._planck = zia_planck
    zia_penny = 0.07
    zia_agenda._penny = zia_penny
    zia_party_credor_pool = 2
    zia_party_debtor_pool = 2
    zia_agenda.set_party_credor_pool(zia_party_credor_pool)
    zia_agenda.set_party_debtor_pool(zia_party_debtor_pool)
    zia_last_atom_id = 73
    zia_agenda.set_last_atom_id(zia_last_atom_id)

    shave_text = "shave"
    shave_road = zia_agenda.make_l1_road(shave_text)
    shave_fact_y1 = zia_agenda.get_fact_obj(shave_road)
    shave_fact_y1._originunit.set_originlink(party_id="Sue", weight=4.3)
    shave_fact_y1._problem_bool = True
    # print(f"{shave_road=}")
    # print(f"{json_shave_fact._label=} {json_shave_fact._parent_road=}")

    sue_text = "Sue"
    zia_agenda.add_partyunit(party_id=sue_text)
    tim_text = "Tim"
    zia_agenda.add_partyunit(party_id=tim_text)
    run_text = ",runners"
    run_idea = ideaunit_shop(idea_id=run_text)
    run_idea.set_partylink(partylink=partylink_shop(party_id=sue_text))
    run_idea.set_partylink(partylink=partylink_shop(party_id=tim_text))
    zia_agenda.set_ideaunit(y_ideaunit=run_idea)

    run_assignedunit = assignedunit_shop()
    run_assignedunit.set_suffidea(idea_id=run_text)
    zia_agenda.edit_fact_attr(zia_agenda._real_id, assignedunit=run_assignedunit)
    tim_assignedunit = assignedunit_shop()
    tim_assignedunit.set_suffidea(idea_id=tim_text)
    zia_agenda.edit_fact_attr(shave_road, assignedunit=tim_assignedunit)
    zia_agenda.edit_fact_attr(shave_road, balancelink=balancelink_shop(tim_text))
    zia_agenda.edit_fact_attr(shave_road, balancelink=balancelink_shop(sue_text))
    zia_agenda.edit_fact_attr(
        zia_agenda._real_id, balancelink=balancelink_shop(sue_text)
    )
    # add healerhold to shave factunit
    run_healerhold = healerhold_shop({run_text})
    zia_agenda.edit_fact_attr(shave_road, healerhold=run_healerhold)

    yao_text = "Yao"
    zia_agenda._originunit.set_originlink(yao_text, 1)
    override_text = "override"
    zia_agenda.set_meld_strategy(override_text)

    # WHEN
    x_json = zia_agenda.get_json()
    assert x_is_json(x_json) == True
    json_agenda = agendaunit_get_from_json(x_agenda_json=x_json)

    # THEN
    assert str(type(json_agenda)).find(".agenda.AgendaUnit'>") > 0
    assert json_agenda._owner_id != None
    assert json_agenda._owner_id == zia_agenda._owner_id
    assert json_agenda._real_id == zia_agenda._real_id
    assert json_agenda._planck == zia_planck
    assert json_agenda._planck == zia_agenda._planck
    assert json_agenda._penny == zia_penny
    assert json_agenda._penny == zia_agenda._penny
    assert json_agenda._max_tree_traverse == 23
    assert json_agenda._max_tree_traverse == zia_agenda._max_tree_traverse
    assert json_agenda._road_delimiter == zia_agenda._road_delimiter
    assert json_agenda._party_credor_pool == zia_agenda._party_credor_pool
    assert json_agenda._party_debtor_pool == zia_agenda._party_debtor_pool
    assert json_agenda._party_credor_pool == zia_party_credor_pool
    assert json_agenda._party_debtor_pool == zia_party_debtor_pool
    assert json_agenda._meld_strategy == zia_agenda._meld_strategy
    assert json_agenda._meld_strategy == override_text
    assert json_agenda._last_atom_id == zia_agenda._last_atom_id
    assert json_agenda._last_atom_id == zia_last_atom_id
    print(f"{json_agenda._ideas.keys()=}")
    print(f"{zia_agenda._ideas.keys()=}")
    assert json_agenda._ideas == zia_agenda._ideas

    json_factroot = json_agenda._factroot
    assert json_factroot._parent_road == ""
    assert json_factroot._parent_road == zia_agenda._factroot._parent_road
    assert json_factroot._reasonunits == {}
    assert json_factroot._assignedunit == zia_agenda._factroot._assignedunit
    assert json_factroot._assignedunit == run_assignedunit
    assert len(json_factroot._beliefunits) == 1
    assert len(json_factroot._balancelinks) == 1

    assert len(json_agenda._factroot._kids) == 2

    weekday_text = "weekdays"
    weekday_road = json_agenda.make_l1_road(weekday_text)
    weekday_fact_x = json_agenda.get_fact_obj(weekday_road)
    assert len(weekday_fact_x._kids) == 2

    sunday_text = "Sunday"
    sunday_road = json_agenda.make_road(weekday_road, sunday_text)
    sunday_fact = json_agenda.get_fact_obj(sunday_road)
    assert sunday_fact._weight == 20

    json_shave_fact = json_agenda.get_fact_obj(shave_road)
    zia_shave_fact = zia_agenda.get_fact_obj(shave_road)
    assert len(json_shave_fact._reasonunits) == 1
    assert json_shave_fact._assignedunit == zia_shave_fact._assignedunit
    assert json_shave_fact._assignedunit == tim_assignedunit
    assert json_shave_fact._originunit == zia_shave_fact._originunit
    print(f"{json_shave_fact._healerhold=}")
    assert json_shave_fact._healerhold == zia_shave_fact._healerhold
    assert len(json_shave_fact._balancelinks) == 2
    assert len(json_shave_fact._beliefunits) == 1
    assert zia_shave_fact._problem_bool
    assert json_shave_fact._problem_bool == zia_shave_fact._problem_bool

    assert len(json_agenda._originunit._links) == 1
    assert json_agenda._originunit == zia_agenda._originunit


def test_agendaunit_get_from_json_ReturnsCorrectObj_road_delimiter_Example():
    # GIVEN
    slash_delimiter = "/"
    before_bob_agenda = agendaunit_shop("Bob", _road_delimiter=slash_delimiter)
    assert before_bob_agenda._road_delimiter != default_road_delimiter_if_none()

    # WHEN
    bob_json = before_bob_agenda.get_json()
    after_bob_agenda = agendaunit_get_from_json(bob_json)

    # THEN
    assert after_bob_agenda._road_delimiter != default_road_delimiter_if_none()
    assert after_bob_agenda._road_delimiter == slash_delimiter
    assert after_bob_agenda._road_delimiter == before_bob_agenda._road_delimiter


def test_agendaunit_get_from_json_ReturnsCorrectObj_road_delimiter_PartyExample():
    # GIVEN
    slash_delimiter = "/"
    before_bob_agenda = agendaunit_shop("Bob", _road_delimiter=slash_delimiter)
    bob_text = ",Bob"
    before_bob_agenda.add_partyunit(bob_text)
    assert before_bob_agenda.party_exists(bob_text)

    # WHEN
    bob_json = before_bob_agenda.get_json()
    after_bob_agenda = agendaunit_get_from_json(bob_json)

    # THEN
    after_bob_partyunit = after_bob_agenda.get_party(bob_text)
    assert after_bob_partyunit._road_delimiter == slash_delimiter


def test_agendaunit_get_from_json_ReturnsCorrectObj_road_delimiter_IdeaExample():
    # GIVEN
    slash_delimiter = "/"
    before_bob_agenda = agendaunit_shop("Bob", _road_delimiter=slash_delimiter)
    swimmers_text = f"{slash_delimiter}Swimmers"
    before_bob_agenda.set_ideaunit(
        ideaunit_shop(swimmers_text, _road_delimiter=slash_delimiter)
    )
    assert before_bob_agenda.get_ideaunit(swimmers_text) != None

    # WHEN
    bob_json = before_bob_agenda.get_json()
    after_bob_agenda = agendaunit_get_from_json(bob_json)

    # THEN
    after_bob_ideaunit = after_bob_agenda.get_ideaunit(swimmers_text)
    assert after_bob_ideaunit._road_delimiter == slash_delimiter


def test_agendaunit_get_from_json_jsonExportCorrectyExportsAgendaUnit_weight():
    # GIVEN
    x1_agenda = example_agendas_agenda_v001()
    x1_agenda._weight = 15
    assert 15 == x1_agenda._weight
    assert x1_agenda._factroot._weight != x1_agenda._weight
    assert x1_agenda._factroot._weight == 1

    # WHEN
    x2_agenda = agendaunit_get_from_json(x1_agenda.get_json())

    # THEN
    assert x1_agenda._weight == 15
    assert x1_agenda._weight == x2_agenda._weight
    assert x1_agenda._factroot._weight == 1
    assert x1_agenda._factroot._weight == x2_agenda._factroot._weight
    assert x1_agenda._factroot._kids == x2_agenda._factroot._kids


def test_get_dict_of_agenda_from_dict_ReturnsDictOfAgendaUnits():
    # GIVEN
    x1_agenda = example_agendas_agenda_v001()
    x2_agenda = example_agendas_get_agenda_x1_3levels_1reason_1beliefs()
    x3_agenda = example_agendas_get_agenda_base_time_example()
    print(f"{x1_agenda._owner_id}")
    print(f"{x2_agenda._owner_id}")
    print(f"{x3_agenda._owner_id}")

    cn_dict_of_dicts = {
        x1_agenda._owner_id: x1_agenda.get_dict(),
        x2_agenda._owner_id: x2_agenda.get_dict(),
        x3_agenda._owner_id: x3_agenda.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_agenda_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x1_agenda._owner_id) != None
    assert ccn_dict_of_obj.get(x2_agenda._owner_id) != None
    assert ccn_dict_of_obj.get(x3_agenda._owner_id) != None
    cc1_fact_root = ccn_dict_of_obj.get(x1_agenda._owner_id)._factroot
    assert cc1_fact_root._originunit == x1_agenda._factroot._originunit
    assert ccn_dict_of_obj.get(x1_agenda._owner_id)._fact_dict == x1_agenda._fact_dict
    assert ccn_dict_of_obj.get(x1_agenda._owner_id) == x1_agenda
    ccn2_agenda = ccn_dict_of_obj.get(x2_agenda._owner_id)
    assert ccn2_agenda._factroot._label == x2_agenda._factroot._label
    assert ccn2_agenda._factroot._parent_road == x2_agenda._factroot._parent_road
    shave_road = ccn2_agenda.make_l1_road("shave")
    week_road = ccn2_agenda.make_l1_road("weekdays")
    assert ccn2_agenda.get_fact_obj(shave_road) == x2_agenda.get_fact_obj(shave_road)
    assert ccn2_agenda.get_fact_obj(week_road) == x2_agenda.get_fact_obj(week_road)
    assert ccn2_agenda._factroot == x2_agenda._factroot
    print(f"{ccn2_agenda._fact_dict.keys()=}")
    print(f"{x2_agenda._fact_dict.keys()=}")
    assert ccn2_agenda._fact_dict == x2_agenda._fact_dict
    assert ccn2_agenda == x2_agenda
    ccn_agenda3 = ccn_dict_of_obj.get(x3_agenda._owner_id)
    x3_agenda.calc_agenda_metrics()
    assert ccn_agenda3 == x3_agenda
