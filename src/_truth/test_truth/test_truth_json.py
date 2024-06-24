from src._instrument.python import x_is_json, get_dict_from_json
from src._road.road import default_road_delimiter_if_none
from src._truth.belief import beliefunit_shop, balancelink_shop
from src._truth.other import otherlink_shop
from src._truth.healer import healerhold_shop
from src._truth.reason_assign import assignedunit_shop
from src._truth.reason_idea import factunit_shop
from src._truth.idea import ideaunit_shop
from src._truth.truth import (
    truthunit_shop,
    get_from_json as truthunit_get_from_json,
    get_dict_of_truth_from_dict,
)
from src._truth.examples.example_truths import (
    truth_v001 as example_truths_truth_v001,
    get_truth_x1_3levels_1reason_1facts as example_truths_get_truth_x1_3levels_1reason_1facts,
    get_truth_base_time_example as example_truths_get_truth_base_time_example,
)
from pytest import raises as pytest_raises


def test_TruthUnit_get_dict_ReturnsDictObject():
    # GIVEN
    x_truth = example_truths_truth_v001()
    day_hour_text = "day_hour"
    day_hour_road = x_truth.make_l1_road(day_hour_text)
    day_hour_idea = x_truth.get_idea_obj(day_hour_road)
    day_hour_idea._originunit.set_originlink(other_id="Bob", weight=2)
    x_truth.set_fact(
        base=day_hour_road,
        pick=day_hour_road,
        open=0,
        nigh=23,
    )
    time_minute = x_truth.make_l1_road("day_minute")
    x_truth.set_fact(base=time_minute, pick=time_minute, open=0, nigh=1440)
    yao_text = "Yao"
    x_truth._originunit.set_originlink(yao_text, 1)
    truth_weight = 23
    x_truth._weight = truth_weight
    x_other_credor_pool = 22
    x_other_debtor_pool = 22
    x_truth.set_other_credor_pool(x_other_credor_pool)
    x_truth.set_other_debtor_pool(x_other_debtor_pool)
    override_text = "override"
    x_truth.set_meld_strategy(override_text)
    x_last_atom_id = 77
    x_truth.set_last_atom_id(x_last_atom_id)

    # WHEN
    truth_dict = x_truth.get_dict()

    # THEN
    assert truth_dict != None
    assert str(type(truth_dict)) == "<class 'dict'>"
    assert truth_dict["_owner_id"] == x_truth._owner_id
    assert truth_dict["_real_id"] == x_truth._real_id
    assert truth_dict["_weight"] == x_truth._weight
    assert truth_dict["_weight"] == truth_weight
    assert truth_dict["_max_tree_traverse"] == x_truth._max_tree_traverse
    assert truth_dict["_road_delimiter"] == x_truth._road_delimiter
    assert truth_dict["_other_credor_pool"] == x_truth._other_credor_pool
    assert truth_dict["_other_debtor_pool"] == x_truth._other_debtor_pool
    assert truth_dict["_other_debtor_pool"] == x_truth._other_debtor_pool
    assert truth_dict["_meld_strategy"] == x_truth._meld_strategy
    assert truth_dict["_last_atom_id"] == x_truth._last_atom_id
    assert len(truth_dict["_others"]) == len(x_truth._others)
    assert len(truth_dict["_others"]) != 12
    assert len(truth_dict["_beliefs"]) == 12
    assert len(truth_dict["_beliefs"]) != len(x_truth._beliefs)

    x_idearoot = x_truth._idearoot
    idearoot_dict = truth_dict["_idearoot"]
    _kids = "_kids"
    _range_source_road = "_range_source_road"
    _numeric_road = "_numeric_road"
    assert x_idearoot._label == x_truth._real_id
    assert idearoot_dict["_label"] == x_idearoot._label
    assert idearoot_dict["_weight"] != truth_weight
    assert idearoot_dict["_weight"] == x_idearoot._weight
    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    # check an ideakid._range_source_road attribute
    month_week_text = "month_week"
    month_week_road = x_truth.make_l1_road(month_week_text)
    month_week_idea_x = x_truth.get_idea_obj(month_week_road)
    print("check real_id,month_week...range_source_road equal to...")
    month_week_special_dict = idearoot_dict[_kids][month_week_text][_range_source_road]
    assert month_week_special_dict != None
    assert month_week_special_dict == x_truth.make_l1_road("ced_week")
    assert month_week_special_dict == month_week_idea_x._range_source_road

    # check an ideakid._numeric_road attribute
    num1_text = "numeric_road_test"
    num1_road = x_truth.make_l1_road(num1_text)
    num1_idea_x = x_truth.get_idea_obj(num1_road)
    print(f"check {num1_road}...numeric_road equal to...")
    num1_dict_numeric_road = idearoot_dict[_kids][num1_text][_numeric_road]
    assert num1_dict_numeric_road != None
    assert num1_dict_numeric_road == month_week_road
    assert num1_dict_numeric_road == num1_idea_x._numeric_road

    originunit_text = "_originunit"
    day_hour_originunit_dict = idearoot_dict[_kids][day_hour_text][originunit_text]
    assert day_hour_originunit_dict == day_hour_idea._originunit.get_dict()
    _links = "_links"
    x_truth_originlink = truth_dict[originunit_text][_links][yao_text]
    print(f"{x_truth_originlink=}")
    assert x_truth_originlink
    assert x_truth_originlink["other_id"] == yao_text
    assert x_truth_originlink["weight"] == 1


def test_TruthUnit_get_dict_ReturnsDictWith_idearoot_assignedunit():
    # GIVEN
    run_text = "runners"
    tom_truth = truthunit_shop("Tom")
    x_assignedunit = assignedunit_shop()
    x_assignedunit.set_suffbelief(belief_id=run_text)
    tom_truth.edit_idea_attr(assignedunit=x_assignedunit, road=tom_truth._real_id)

    # WHEN
    truth_dict = tom_truth.get_dict()
    idearoot_dict = truth_dict.get("_idearoot")

    # THEN
    assert idearoot_dict["_assignedunit"] == x_assignedunit.get_dict()
    assert idearoot_dict["_assignedunit"] == {"_suffbeliefs": {run_text: run_text}}


def test_TruthUnit_get_dict_ReturnsDictWith_idearoot_healerhold():
    # GIVEN
    tom_truth = truthunit_shop("Tom")
    yao_text = "Yao"
    tom_truth.add_otherunit(yao_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_otherlink(otherlink_shop(yao_text))
    tom_truth.set_beliefunit(run_beliefunit)
    run_healerhold = healerhold_shop()
    run_healerhold.set_belief_id(x_belief_id=run_text)
    tom_truth.edit_idea_attr(road=tom_truth._real_id, healerhold=run_healerhold)

    # WHEN
    truth_dict = tom_truth.get_dict()
    idearoot_dict = truth_dict.get("_idearoot")

    # THEN
    assert idearoot_dict["_healerhold"] == run_healerhold.get_dict()


def test_TruthUnit_get_dict_ReturnsDictWith_ideakid_AssignedUnit():
    # GIVEN
    tom_truth = truthunit_shop("Tom")
    run_text = ",run"
    tom_truth.set_beliefunit(y_beliefunit=beliefunit_shop(run_text))

    morn_text = "morning"
    morn_road = tom_truth.make_l1_road(morn_text)
    tom_truth.add_l1_idea(ideaunit_shop(morn_text))
    x_assignedunit = assignedunit_shop()
    x_assignedunit.set_suffbelief(belief_id=run_text)
    tom_truth.edit_idea_attr(assignedunit=x_assignedunit, road=morn_road)

    # WHEN
    truth_dict = tom_truth.get_dict()
    idearoot_dict = truth_dict.get("_idearoot")

    # THEN
    _kids = "_kids"
    _assignedunit = "_assignedunit"

    assigned_dict_x = idearoot_dict[_kids][morn_text][_assignedunit]
    assert assigned_dict_x == x_assignedunit.get_dict()
    assert assigned_dict_x == {"_suffbeliefs": {run_text: run_text}}


def test_TruthUnit_get_json_ReturnsCorrectJSON_SimpleExample():
    # GIVEN
    zia_truth = example_truths_get_truth_x1_3levels_1reason_1facts()
    tiger_real_id = "tiger"
    zia_truth.set_real_id(tiger_real_id)
    seven_int = 7
    zia_truth._pixel = seven_int
    x_penny = 0.3
    zia_truth._penny = x_penny
    override_text = "override"
    zia_truth.set_meld_strategy(override_text)
    yao_text = "Yao"
    zia_truth.add_otherunit(yao_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_otherlink(otherlink_shop(yao_text))
    zia_truth.set_beliefunit(run_beliefunit)
    run_healerhold = healerhold_shop({run_text})
    zia_truth.edit_idea_attr(road=zia_truth._real_id, healerhold=run_healerhold)
    zia_truth.edit_idea_attr(road=zia_truth._real_id, problem_bool=True)

    # WHEN
    x_json = zia_truth.get_json()

    # THEN
    _kids = "_kids"

    assert x_json != None
    assert True == x_is_json(x_json)
    truth_dict = get_dict_from_json(x_json)

    assert truth_dict["_owner_id"] == zia_truth._owner_id
    assert truth_dict["_real_id"] == zia_truth._real_id
    assert truth_dict["_weight"] == zia_truth._weight
    assert truth_dict["_meld_strategy"] == zia_truth._meld_strategy
    assert truth_dict["_pixel"] == zia_truth._pixel
    assert truth_dict["_penny"] == zia_truth._penny
    with pytest_raises(Exception) as excinfo:
        truth_dict["_other_credor_pool"]
    assert str(excinfo.value) == "'_other_credor_pool'"
    with pytest_raises(Exception) as excinfo:
        truth_dict["_other_debtor_pool"]
    assert str(excinfo.value) == "'_other_debtor_pool'"
    with pytest_raises(Exception) as excinfo:
        truth_dict["_last_atom_id"]

    x_idearoot = zia_truth._idearoot
    idearoot_dict = truth_dict.get("_idearoot")

    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    shave_text = "shave"
    shave_dict = idearoot_dict[_kids][shave_text]
    shave_factunits = shave_dict["_factunits"]
    print(f"{shave_factunits=}")
    assert len(shave_factunits) == 1
    assert len(shave_factunits) == len(x_idearoot._kids[shave_text]._factunits)
    idearoot_healerhold = idearoot_dict["_healerhold"]
    print(f"{idearoot_healerhold=}")
    assert len(idearoot_healerhold) == 1
    assert x_idearoot._healerhold.any_belief_id_exists()
    assert x_idearoot._problem_bool


def test_TruthUnit_get_json_ReturnsCorrectJSON_BigExample():
    # GIVEN
    yao_truth = example_truths_truth_v001()
    day_hour_text = "day_hour"
    day_hour_road = yao_truth.make_l1_road(day_hour_text)
    yao_truth.set_fact(base=day_hour_road, pick=day_hour_road, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = yao_truth.make_l1_road(day_min_text)
    yao_truth.set_fact(base=day_min_road, pick=day_min_road, open=0, nigh=59)
    factunit_x = factunit_shop(day_min_road, day_min_road, 5, 59)
    yao_truth.edit_idea_attr(road=factunit_x.base, factunit=factunit_x)
    yao_truth.set_max_tree_traverse(int_x=2)
    yao_text = "Yao"
    yao_truth._originunit.set_originlink(yao_text, 1)

    # WHEN
    truth_dict = get_dict_from_json(json_x=yao_truth.get_json())

    # THEN
    _kids = "_kids"
    assert truth_dict["_owner_id"] == yao_truth._owner_id
    assert truth_dict["_real_id"] == yao_truth._real_id
    assert truth_dict["_weight"] == yao_truth._weight
    assert truth_dict["_max_tree_traverse"] == 2
    assert truth_dict["_max_tree_traverse"] == yao_truth._max_tree_traverse
    assert truth_dict["_road_delimiter"] == yao_truth._road_delimiter

    x_idearoot = yao_truth._idearoot
    idearoot_dict = truth_dict.get("_idearoot")
    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    kids = idearoot_dict[_kids]
    day_min_dict = kids[day_min_text]
    day_min_factunits_dict = day_min_dict["_factunits"]
    day_min_idea_x = yao_truth.get_idea_obj(day_min_road)
    print(f"{day_min_factunits_dict=}")
    assert len(day_min_factunits_dict) == 1
    assert len(day_min_factunits_dict) == len(day_min_idea_x._factunits)

    _reasonunits = "_reasonunits"
    cont_text = "Freelancing"
    ulti_text = "Ultimate Frisbee"
    cont_road = yao_truth.make_l1_road(cont_text)
    ulti_road = yao_truth.make_l1_road(ulti_text)
    cont_idea = yao_truth.get_idea_obj(cont_road)
    ulti_idea = yao_truth.get_idea_obj(ulti_road)
    cont_reasonunits_dict = idearoot_dict[_kids][cont_text][_reasonunits]
    ulti_reasonunits_dict = idearoot_dict[_kids][ulti_text][_reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_idea._reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_idea._reasonunits)
    originunit_text = "_originunit"
    _links = "_links"
    assert len(truth_dict[originunit_text][_links])


def test_truthunit_get_from_json_ReturnsCorrectObjSimpleExample():
    # GIVEN
    zia_truth = example_truths_get_truth_x1_3levels_1reason_1facts()
    zia_truth.set_max_tree_traverse(23)
    tiger_real_id = "tiger"
    zia_truth.set_real_id(tiger_real_id)
    zia_pixel = 0.5
    zia_truth._pixel = zia_pixel
    zia_penny = 2
    zia_truth._penny = zia_penny
    zia_other_credor_pool = 2
    zia_other_debtor_pool = 2
    zia_truth.set_other_credor_pool(zia_other_credor_pool)
    zia_truth.set_other_debtor_pool(zia_other_debtor_pool)
    zia_last_atom_id = 73
    zia_truth.set_last_atom_id(zia_last_atom_id)

    shave_text = "shave"
    shave_road = zia_truth.make_l1_road(shave_text)
    shave_idea_y1 = zia_truth.get_idea_obj(shave_road)
    shave_idea_y1._originunit.set_originlink(other_id="Sue", weight=4.3)
    shave_idea_y1._problem_bool = True
    # print(f"{shave_road=}")
    # print(f"{json_shave_idea._label=} {json_shave_idea._parent_road=}")

    sue_text = "Sue"
    zia_truth.add_otherunit(other_id=sue_text)
    tim_text = "Tim"
    zia_truth.add_otherunit(other_id=tim_text)
    run_text = ",runners"
    run_belief = beliefunit_shop(belief_id=run_text)
    run_belief.set_otherlink(otherlink=otherlink_shop(other_id=sue_text))
    run_belief.set_otherlink(otherlink=otherlink_shop(other_id=tim_text))
    zia_truth.set_beliefunit(y_beliefunit=run_belief)

    run_assignedunit = assignedunit_shop()
    run_assignedunit.set_suffbelief(belief_id=run_text)
    zia_truth.edit_idea_attr(zia_truth._real_id, assignedunit=run_assignedunit)
    tim_assignedunit = assignedunit_shop()
    tim_assignedunit.set_suffbelief(belief_id=tim_text)
    zia_truth.edit_idea_attr(shave_road, assignedunit=tim_assignedunit)
    zia_truth.edit_idea_attr(shave_road, balancelink=balancelink_shop(tim_text))
    zia_truth.edit_idea_attr(shave_road, balancelink=balancelink_shop(sue_text))
    zia_truth.edit_idea_attr(zia_truth._real_id, balancelink=balancelink_shop(sue_text))
    # add healerhold to shave ideaunit
    run_healerhold = healerhold_shop({run_text})
    zia_truth.edit_idea_attr(shave_road, healerhold=run_healerhold)

    yao_text = "Yao"
    zia_truth._originunit.set_originlink(yao_text, 1)
    override_text = "override"
    zia_truth.set_meld_strategy(override_text)

    # WHEN
    x_json = zia_truth.get_json()
    assert x_is_json(x_json) == True
    json_truth = truthunit_get_from_json(x_truth_json=x_json)

    # THEN
    assert str(type(json_truth)).find(".truth.TruthUnit'>") > 0
    assert json_truth._owner_id != None
    assert json_truth._owner_id == zia_truth._owner_id
    assert json_truth._real_id == zia_truth._real_id
    assert json_truth._pixel == zia_pixel
    assert json_truth._pixel == zia_truth._pixel
    assert json_truth._penny == zia_penny
    assert json_truth._penny == zia_truth._penny
    assert json_truth._max_tree_traverse == 23
    assert json_truth._max_tree_traverse == zia_truth._max_tree_traverse
    assert json_truth._road_delimiter == zia_truth._road_delimiter
    assert json_truth._other_credor_pool == zia_truth._other_credor_pool
    assert json_truth._other_debtor_pool == zia_truth._other_debtor_pool
    assert json_truth._other_credor_pool == zia_other_credor_pool
    assert json_truth._other_debtor_pool == zia_other_debtor_pool
    assert json_truth._meld_strategy == zia_truth._meld_strategy
    assert json_truth._meld_strategy == override_text
    assert json_truth._last_atom_id == zia_truth._last_atom_id
    assert json_truth._last_atom_id == zia_last_atom_id
    print(f"{json_truth._beliefs.keys()=}")
    print(f"{zia_truth._beliefs.keys()=}")
    assert json_truth._beliefs == zia_truth._beliefs

    json_idearoot = json_truth._idearoot
    assert json_idearoot._parent_road == ""
    assert json_idearoot._parent_road == zia_truth._idearoot._parent_road
    assert json_idearoot._reasonunits == {}
    assert json_idearoot._assignedunit == zia_truth._idearoot._assignedunit
    assert json_idearoot._assignedunit == run_assignedunit
    assert len(json_idearoot._factunits) == 1
    assert len(json_idearoot._balancelinks) == 1

    assert len(json_truth._idearoot._kids) == 2

    weekday_text = "weekdays"
    weekday_road = json_truth.make_l1_road(weekday_text)
    weekday_idea_x = json_truth.get_idea_obj(weekday_road)
    assert len(weekday_idea_x._kids) == 2

    sunday_text = "Sunday"
    sunday_road = json_truth.make_road(weekday_road, sunday_text)
    sunday_idea = json_truth.get_idea_obj(sunday_road)
    assert sunday_idea._weight == 20

    json_shave_idea = json_truth.get_idea_obj(shave_road)
    zia_shave_idea = zia_truth.get_idea_obj(shave_road)
    assert len(json_shave_idea._reasonunits) == 1
    assert json_shave_idea._assignedunit == zia_shave_idea._assignedunit
    assert json_shave_idea._assignedunit == tim_assignedunit
    assert json_shave_idea._originunit == zia_shave_idea._originunit
    print(f"{json_shave_idea._healerhold=}")
    assert json_shave_idea._healerhold == zia_shave_idea._healerhold
    assert len(json_shave_idea._balancelinks) == 2
    assert len(json_shave_idea._factunits) == 1
    assert zia_shave_idea._problem_bool
    assert json_shave_idea._problem_bool == zia_shave_idea._problem_bool

    assert len(json_truth._originunit._links) == 1
    assert json_truth._originunit == zia_truth._originunit


def test_truthunit_get_from_json_ReturnsCorrectObj_road_delimiter_Example():
    # GIVEN
    slash_delimiter = "/"
    before_bob_truth = truthunit_shop("Bob", _road_delimiter=slash_delimiter)
    assert before_bob_truth._road_delimiter != default_road_delimiter_if_none()

    # WHEN
    bob_json = before_bob_truth.get_json()
    after_bob_truth = truthunit_get_from_json(bob_json)

    # THEN
    assert after_bob_truth._road_delimiter != default_road_delimiter_if_none()
    assert after_bob_truth._road_delimiter == slash_delimiter
    assert after_bob_truth._road_delimiter == before_bob_truth._road_delimiter


def test_truthunit_get_from_json_ReturnsCorrectObj_road_delimiter_OtherExample():
    # GIVEN
    slash_delimiter = "/"
    before_bob_truth = truthunit_shop("Bob", _road_delimiter=slash_delimiter)
    bob_text = ",Bob"
    before_bob_truth.add_otherunit(bob_text)
    assert before_bob_truth.other_exists(bob_text)

    # WHEN
    bob_json = before_bob_truth.get_json()
    after_bob_truth = truthunit_get_from_json(bob_json)

    # THEN
    after_bob_otherunit = after_bob_truth.get_other(bob_text)
    assert after_bob_otherunit._road_delimiter == slash_delimiter


def test_truthunit_get_from_json_ReturnsCorrectObj_road_delimiter_BeliefExample():
    # GIVEN
    slash_delimiter = "/"
    before_bob_truth = truthunit_shop("Bob", _road_delimiter=slash_delimiter)
    swimmers_text = f"{slash_delimiter}Swimmers"
    before_bob_truth.set_beliefunit(
        beliefunit_shop(swimmers_text, _road_delimiter=slash_delimiter)
    )
    assert before_bob_truth.get_beliefunit(swimmers_text) != None

    # WHEN
    bob_json = before_bob_truth.get_json()
    after_bob_truth = truthunit_get_from_json(bob_json)

    # THEN
    after_bob_beliefunit = after_bob_truth.get_beliefunit(swimmers_text)
    assert after_bob_beliefunit._road_delimiter == slash_delimiter


def test_truthunit_get_from_json_jsonExportCorrectyExportsTruthUnit_weight():
    # GIVEN
    x1_truth = example_truths_truth_v001()
    x1_truth._weight = 15
    assert 15 == x1_truth._weight
    assert x1_truth._idearoot._weight != x1_truth._weight
    assert x1_truth._idearoot._weight == 1

    # WHEN
    x2_truth = truthunit_get_from_json(x1_truth.get_json())

    # THEN
    assert x1_truth._weight == 15
    assert x1_truth._weight == x2_truth._weight
    assert x1_truth._idearoot._weight == 1
    assert x1_truth._idearoot._weight == x2_truth._idearoot._weight
    assert x1_truth._idearoot._kids == x2_truth._idearoot._kids


def test_get_dict_of_truth_from_dict_ReturnsDictOfTruthUnits():
    # GIVEN
    x1_truth = example_truths_truth_v001()
    x2_truth = example_truths_get_truth_x1_3levels_1reason_1facts()
    x3_truth = example_truths_get_truth_base_time_example()
    print(f"{x1_truth._owner_id}")
    print(f"{x2_truth._owner_id}")
    print(f"{x3_truth._owner_id}")

    cn_dict_of_dicts = {
        x1_truth._owner_id: x1_truth.get_dict(),
        x2_truth._owner_id: x2_truth.get_dict(),
        x3_truth._owner_id: x3_truth.get_dict(),
    }

    # WHEN
    ccn_dict_of_obj = get_dict_of_truth_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x1_truth._owner_id) != None
    assert ccn_dict_of_obj.get(x2_truth._owner_id) != None
    assert ccn_dict_of_obj.get(x3_truth._owner_id) != None
    cc1_idea_root = ccn_dict_of_obj.get(x1_truth._owner_id)._idearoot
    assert cc1_idea_root._originunit == x1_truth._idearoot._originunit
    assert ccn_dict_of_obj.get(x1_truth._owner_id)._idea_dict == x1_truth._idea_dict
    assert ccn_dict_of_obj.get(x1_truth._owner_id) == x1_truth
    ccn2_truth = ccn_dict_of_obj.get(x2_truth._owner_id)
    assert ccn2_truth._idearoot._label == x2_truth._idearoot._label
    assert ccn2_truth._idearoot._parent_road == x2_truth._idearoot._parent_road
    shave_road = ccn2_truth.make_l1_road("shave")
    week_road = ccn2_truth.make_l1_road("weekdays")
    assert ccn2_truth.get_idea_obj(shave_road) == x2_truth.get_idea_obj(shave_road)
    assert ccn2_truth.get_idea_obj(week_road) == x2_truth.get_idea_obj(week_road)
    assert ccn2_truth._idearoot == x2_truth._idearoot
    print(f"{ccn2_truth._idea_dict.keys()=}")
    print(f"{x2_truth._idea_dict.keys()=}")
    assert ccn2_truth._idea_dict == x2_truth._idea_dict
    assert ccn2_truth == x2_truth
    ccn_truth3 = ccn_dict_of_obj.get(x3_truth._owner_id)
    x3_truth.calc_truth_metrics()
    assert ccn_truth3 == x3_truth
