from src._instrument.python import x_is_json, get_dict_from_json
from src._road.road import default_road_delimiter_if_none
from src._world.beliefunit import beliefunit_shop, fiscallink_shop
from src._world.char import charlink_shop
from src._world.healer import healerhold_shop
from src._world.reason_culture import cultureunit_shop
from src._world.reason_idea import factunit_shop
from src._world.idea import ideaunit_shop
from src._world.world import (
    worldunit_shop,
    get_from_json as worldunit_get_from_json,
    get_dict_of_world_from_dict,
)
from src._world.examples.example_worlds import (
    world_v001 as example_worlds_world_v001,
    get_world_x1_3levels_1reason_1facts as example_worlds_get_world_x1_3levels_1reason_1facts,
    get_world_base_time_example as example_worlds_get_world_base_time_example,
)
from pytest import raises as pytest_raises


def test_WorldUnit_get_dict_SetsCharUnit_beliefholds():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    sue_credor_weight = 11
    sue_debtor_weight = 13
    zia_text = "Zia"
    zia_credor_weight = 17
    zia_debtor_weight = 23
    bob_world = worldunit_shop("Bob")
    bob_world.add_charunit(yao_text)
    bob_world.add_charunit(sue_text)
    bob_world.add_charunit(zia_text)
    run_text = ",Run"
    bob_world.set_beliefunit(beliefunit_shop(run_text))
    run_beliefunit = bob_world.get_beliefunit(run_text)
    sue_run_charlink = charlink_shop(sue_text, sue_credor_weight, sue_debtor_weight)
    zia_run_charlink = charlink_shop(zia_text, zia_credor_weight, zia_debtor_weight)
    run_beliefunit.set_charlink(sue_run_charlink)
    run_beliefunit.set_charlink(zia_run_charlink)
    assert len(bob_world.get_beliefunit(run_text)._chars) == 2
    assert len(bob_world.get_char(yao_text)._beliefholds) == 0
    assert len(bob_world.get_char(sue_text)._beliefholds) == 0

    # WHEN
    bob_world.get_dict()

    # THEN
    assert len(bob_world.get_char(sue_text)._beliefholds) == 2
    assert len(bob_world.get_char(zia_text)._beliefholds) == 2
    sue_charunit = bob_world.get_char(sue_text)
    zia_charunit = bob_world.get_char(zia_text)
    sue_beliefhold = sue_charunit.get_beliefhold(run_text)
    zia_beliefhold = zia_charunit.get_beliefhold(run_text)
    assert sue_beliefhold.credor_weight == sue_credor_weight
    assert sue_beliefhold.debtor_weight == sue_debtor_weight
    assert zia_beliefhold.credor_weight == zia_credor_weight
    assert zia_beliefhold.debtor_weight == zia_debtor_weight


def test_WorldUnit_get_dict_ReturnsDictObject():
    # GIVEN
    x_world = example_worlds_world_v001()
    day_hour_text = "day_hour"
    day_hour_road = x_world.make_l1_road(day_hour_text)
    day_hour_idea = x_world.get_idea_obj(day_hour_road)
    day_hour_idea._originunit.set_originlink(char_id="Bob", weight=2)
    x_world.set_fact(
        base=day_hour_road,
        pick=day_hour_road,
        open=0,
        nigh=23,
    )
    time_minute = x_world.make_l1_road("day_minute")
    x_world.set_fact(base=time_minute, pick=time_minute, open=0, nigh=1440)
    yao_text = "Yao"
    x_world._originunit.set_originlink(yao_text, 1)
    world_weight = 23
    x_world._weight = world_weight
    x_char_credor_pool = 22
    x_char_debtor_pool = 22
    x_world.set_char_credor_pool(x_char_credor_pool)
    x_world.set_char_debtor_pool(x_char_debtor_pool)
    override_text = "override"
    x_world.set_meld_strategy(override_text)
    x_last_gift_id = 77
    x_world.set_last_gift_id(x_last_gift_id)

    # WHEN
    world_dict = x_world.get_dict()

    # THEN
    assert world_dict != None
    assert str(type(world_dict)) == "<class 'dict'>"
    assert world_dict["_owner_id"] == x_world._owner_id
    assert world_dict["_real_id"] == x_world._real_id
    assert world_dict["_weight"] == x_world._weight
    assert world_dict["_weight"] == world_weight
    assert world_dict["_max_tree_traverse"] == x_world._max_tree_traverse
    assert world_dict["_road_delimiter"] == x_world._road_delimiter
    assert world_dict["_char_credor_pool"] == x_world._char_credor_pool
    assert world_dict["_char_debtor_pool"] == x_world._char_debtor_pool
    assert world_dict["_char_debtor_pool"] == x_world._char_debtor_pool
    assert world_dict["_meld_strategy"] == x_world._meld_strategy
    assert world_dict["_last_gift_id"] == x_world._last_gift_id
    assert len(world_dict["_chars"]) == len(x_world._chars)
    assert len(world_dict["_chars"]) != 12
    assert len(world_dict["_beliefs"]) == 12
    assert len(world_dict["_beliefs"]) != len(x_world._beliefs)

    x_idearoot = x_world._idearoot
    idearoot_dict = world_dict["_idearoot"]
    _kids = "_kids"
    _range_source_road = "_range_source_road"
    _numeric_road = "_numeric_road"
    assert x_idearoot._label == x_world._real_id
    assert idearoot_dict["_label"] == x_idearoot._label
    assert idearoot_dict["_weight"] != world_weight
    assert idearoot_dict["_weight"] == x_idearoot._weight
    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    # check an ideakid._range_source_road attribute
    month_week_text = "month_week"
    month_week_road = x_world.make_l1_road(month_week_text)
    month_week_idea_x = x_world.get_idea_obj(month_week_road)
    print("check real_id,month_week...range_source_road equal to...")
    month_week_special_dict = idearoot_dict[_kids][month_week_text][_range_source_road]
    assert month_week_special_dict != None
    assert month_week_special_dict == x_world.make_l1_road("ced_week")
    assert month_week_special_dict == month_week_idea_x._range_source_road

    # check an ideakid._numeric_road attribute
    num1_text = "numeric_road_test"
    num1_road = x_world.make_l1_road(num1_text)
    num1_idea_x = x_world.get_idea_obj(num1_road)
    print(f"check {num1_road}...numeric_road equal to...")
    num1_dict_numeric_road = idearoot_dict[_kids][num1_text][_numeric_road]
    assert num1_dict_numeric_road != None
    assert num1_dict_numeric_road == month_week_road
    assert num1_dict_numeric_road == num1_idea_x._numeric_road

    originunit_text = "_originunit"
    day_hour_originunit_dict = idearoot_dict[_kids][day_hour_text][originunit_text]
    assert day_hour_originunit_dict == day_hour_idea._originunit.get_dict()
    _links = "_links"
    x_world_originlink = world_dict[originunit_text][_links][yao_text]
    print(f"{x_world_originlink=}")
    assert x_world_originlink
    assert x_world_originlink["char_id"] == yao_text
    assert x_world_originlink["weight"] == 1


def test_WorldUnit_get_dict_ReturnsDictWith_idearoot_cultureunit():
    # GIVEN
    run_text = "runners"
    tom_world = worldunit_shop("Tom")
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_heldbelief(belief_id=run_text)
    tom_world.edit_idea_attr(cultureunit=x_cultureunit, road=tom_world._real_id)

    # WHEN
    world_dict = tom_world.get_dict()
    idearoot_dict = world_dict.get("_idearoot")

    # THEN
    assert idearoot_dict["_cultureunit"] == x_cultureunit.get_dict()
    assert idearoot_dict["_cultureunit"] == {"_heldbeliefs": [run_text]}


def test_WorldUnit_get_dict_ReturnsDictWith_idearoot_healerhold():
    # GIVEN
    tom_world = worldunit_shop("Tom")
    yao_text = "Yao"
    tom_world.add_charunit(yao_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_charlink(charlink_shop(yao_text))
    tom_world.set_beliefunit(run_beliefunit)
    run_healerhold = healerhold_shop()
    run_healerhold.set_belief_id(x_belief_id=run_text)
    tom_world.edit_idea_attr(road=tom_world._real_id, healerhold=run_healerhold)

    # WHEN
    world_dict = tom_world.get_dict()
    idearoot_dict = world_dict.get("_idearoot")

    # THEN
    assert idearoot_dict["_healerhold"] == run_healerhold.get_dict()


def test_WorldUnit_get_dict_ReturnsDictWith_ideakid_CultureUnit():
    # GIVEN
    tom_world = worldunit_shop("Tom")
    run_text = ",run"
    tom_world.set_beliefunit(y_beliefunit=beliefunit_shop(run_text))

    morn_text = "morning"
    morn_road = tom_world.make_l1_road(morn_text)
    tom_world.add_l1_idea(ideaunit_shop(morn_text))
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_heldbelief(belief_id=run_text)
    tom_world.edit_idea_attr(cultureunit=x_cultureunit, road=morn_road)

    # WHEN
    world_dict = tom_world.get_dict()
    idearoot_dict = world_dict.get("_idearoot")

    # THEN
    _kids = "_kids"
    _cultureunit = "_cultureunit"

    culture_dict_x = idearoot_dict[_kids][morn_text][_cultureunit]
    assert culture_dict_x == x_cultureunit.get_dict()
    assert culture_dict_x == {"_heldbeliefs": [run_text]}


def test_WorldUnit_get_json_ReturnsCorrectJSON_SimpleExample():
    # GIVEN
    zia_world = example_worlds_get_world_x1_3levels_1reason_1facts()
    tiger_real_id = "tiger"
    zia_world.set_real_id(tiger_real_id)
    seven_int = 7
    zia_world._pixel = seven_int
    x_penny = 0.3
    zia_world._penny = x_penny
    override_text = "override"
    zia_world.set_meld_strategy(override_text)
    yao_text = "Yao"
    zia_world.add_charunit(yao_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_charlink(charlink_shop(yao_text))
    zia_world.set_beliefunit(run_beliefunit)
    run_healerhold = healerhold_shop({run_text})
    zia_world.edit_idea_attr(road=zia_world._real_id, healerhold=run_healerhold)
    zia_world.edit_idea_attr(road=zia_world._real_id, problem_bool=True)

    # WHEN
    x_json = zia_world.get_json()

    # THEN
    _kids = "_kids"

    assert x_json != None
    assert True == x_is_json(x_json)
    world_dict = get_dict_from_json(x_json)

    assert world_dict["_owner_id"] == zia_world._owner_id
    assert world_dict["_real_id"] == zia_world._real_id
    assert world_dict["_weight"] == zia_world._weight
    assert world_dict["_meld_strategy"] == zia_world._meld_strategy
    assert world_dict["_pixel"] == zia_world._pixel
    assert world_dict["_penny"] == zia_world._penny
    with pytest_raises(Exception) as excinfo:
        world_dict["_char_credor_pool"]
    assert str(excinfo.value) == "'_char_credor_pool'"
    with pytest_raises(Exception) as excinfo:
        world_dict["_char_debtor_pool"]
    assert str(excinfo.value) == "'_char_debtor_pool'"
    with pytest_raises(Exception) as excinfo:
        world_dict["_last_gift_id"]

    x_idearoot = zia_world._idearoot
    idearoot_dict = world_dict.get("_idearoot")

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


def test_WorldUnit_get_json_ReturnsCorrectJSON_BigExample():
    # GIVEN
    yao_world = example_worlds_world_v001()
    day_hour_text = "day_hour"
    day_hour_road = yao_world.make_l1_road(day_hour_text)
    yao_world.set_fact(base=day_hour_road, pick=day_hour_road, open=0, nigh=23)
    day_min_text = "day_minute"
    day_min_road = yao_world.make_l1_road(day_min_text)
    yao_world.set_fact(base=day_min_road, pick=day_min_road, open=0, nigh=59)
    factunit_x = factunit_shop(day_min_road, day_min_road, 5, 59)
    yao_world.edit_idea_attr(road=factunit_x.base, factunit=factunit_x)
    yao_world.set_max_tree_traverse(int_x=2)
    yao_text = "Yao"
    yao_world._originunit.set_originlink(yao_text, 1)

    # WHEN
    world_dict = get_dict_from_json(json_x=yao_world.get_json())

    # THEN
    _kids = "_kids"
    assert world_dict["_owner_id"] == yao_world._owner_id
    assert world_dict["_real_id"] == yao_world._real_id
    assert world_dict["_weight"] == yao_world._weight
    assert world_dict["_max_tree_traverse"] == 2
    assert world_dict["_max_tree_traverse"] == yao_world._max_tree_traverse
    assert world_dict["_road_delimiter"] == yao_world._road_delimiter

    x_idearoot = yao_world._idearoot
    idearoot_dict = world_dict.get("_idearoot")
    assert len(idearoot_dict[_kids]) == len(x_idearoot._kids)

    kids = idearoot_dict[_kids]
    day_min_dict = kids[day_min_text]
    day_min_factunits_dict = day_min_dict["_factunits"]
    day_min_idea_x = yao_world.get_idea_obj(day_min_road)
    print(f"{day_min_factunits_dict=}")
    assert len(day_min_factunits_dict) == 1
    assert len(day_min_factunits_dict) == len(day_min_idea_x._factunits)

    _reasonunits = "_reasonunits"
    cont_text = "Freelancing"
    ulti_text = "Ultimate Frisbee"
    cont_road = yao_world.make_l1_road(cont_text)
    ulti_road = yao_world.make_l1_road(ulti_text)
    cont_idea = yao_world.get_idea_obj(cont_road)
    ulti_idea = yao_world.get_idea_obj(ulti_road)
    cont_reasonunits_dict = idearoot_dict[_kids][cont_text][_reasonunits]
    ulti_reasonunits_dict = idearoot_dict[_kids][ulti_text][_reasonunits]
    assert len(cont_reasonunits_dict) == len(cont_idea._reasonunits)
    assert len(ulti_reasonunits_dict) == len(ulti_idea._reasonunits)
    originunit_text = "_originunit"
    _links = "_links"
    assert len(world_dict[originunit_text][_links])


def test_worldunit_get_from_json_ReturnsCorrectObjSimpleExample():
    # GIVEN
    zia_world = example_worlds_get_world_x1_3levels_1reason_1facts()
    zia_world.set_max_tree_traverse(23)
    tiger_real_id = "tiger"
    zia_world.set_real_id(tiger_real_id)
    zia_pixel = 0.5
    zia_world._pixel = zia_pixel
    zia_penny = 2
    zia_world._penny = zia_penny
    zia_char_credor_pool = 2
    zia_char_debtor_pool = 2
    zia_world.set_char_credor_pool(zia_char_credor_pool)
    zia_world.set_char_debtor_pool(zia_char_debtor_pool)
    zia_last_gift_id = 73
    zia_world.set_last_gift_id(zia_last_gift_id)

    shave_text = "shave"
    shave_road = zia_world.make_l1_road(shave_text)
    shave_idea_y1 = zia_world.get_idea_obj(shave_road)
    shave_idea_y1._originunit.set_originlink(char_id="Sue", weight=4.3)
    shave_idea_y1._problem_bool = True
    # print(f"{shave_road=}")
    # print(f"{json_shave_idea._label=} {json_shave_idea._parent_road=}")

    sue_text = "Sue"
    zia_world.add_charunit(char_id=sue_text)
    tim_text = "Tim"
    zia_world.add_charunit(char_id=tim_text)
    run_text = ",runners"
    run_belief = beliefunit_shop(belief_id=run_text)
    run_belief.set_charlink(charlink=charlink_shop(char_id=sue_text))
    run_belief.set_charlink(charlink=charlink_shop(char_id=tim_text))
    zia_world.set_beliefunit(y_beliefunit=run_belief)

    run_cultureunit = cultureunit_shop()
    run_cultureunit.set_heldbelief(belief_id=run_text)
    zia_world.edit_idea_attr(zia_world._real_id, cultureunit=run_cultureunit)
    tim_cultureunit = cultureunit_shop()
    tim_cultureunit.set_heldbelief(belief_id=tim_text)
    zia_world.edit_idea_attr(shave_road, cultureunit=tim_cultureunit)
    zia_world.edit_idea_attr(shave_road, fiscallink=fiscallink_shop(tim_text))
    zia_world.edit_idea_attr(shave_road, fiscallink=fiscallink_shop(sue_text))
    zia_world.edit_idea_attr(zia_world._real_id, fiscallink=fiscallink_shop(sue_text))
    # add healerhold to shave ideaunit
    run_healerhold = healerhold_shop({run_text})
    zia_world.edit_idea_attr(shave_road, healerhold=run_healerhold)

    yao_text = "Yao"
    zia_world._originunit.set_originlink(yao_text, 1)
    override_text = "override"
    zia_world.set_meld_strategy(override_text)

    # WHEN
    x_json = zia_world.get_json()
    assert x_is_json(x_json) == True
    json_world = worldunit_get_from_json(x_world_json=x_json)

    # THEN
    assert str(type(json_world)).find(".world.WorldUnit'>") > 0
    assert json_world._owner_id != None
    assert json_world._owner_id == zia_world._owner_id
    assert json_world._real_id == zia_world._real_id
    assert json_world._pixel == zia_pixel
    assert json_world._pixel == zia_world._pixel
    assert json_world._penny == zia_penny
    assert json_world._penny == zia_world._penny
    assert json_world._max_tree_traverse == 23
    assert json_world._max_tree_traverse == zia_world._max_tree_traverse
    assert json_world._road_delimiter == zia_world._road_delimiter
    assert json_world._char_credor_pool == zia_world._char_credor_pool
    assert json_world._char_debtor_pool == zia_world._char_debtor_pool
    assert json_world._char_credor_pool == zia_char_credor_pool
    assert json_world._char_debtor_pool == zia_char_debtor_pool
    assert json_world._meld_strategy == zia_world._meld_strategy
    assert json_world._meld_strategy == override_text
    assert json_world._last_gift_id == zia_world._last_gift_id
    assert json_world._last_gift_id == zia_last_gift_id
    print(f"{json_world._beliefs.keys()=}")
    print(f"{zia_world._beliefs.keys()=}")
    assert json_world._beliefs == zia_world._beliefs

    json_idearoot = json_world._idearoot
    assert json_idearoot._parent_road == ""
    assert json_idearoot._parent_road == zia_world._idearoot._parent_road
    assert json_idearoot._reasonunits == {}
    assert json_idearoot._cultureunit == zia_world._idearoot._cultureunit
    assert json_idearoot._cultureunit == run_cultureunit
    assert len(json_idearoot._factunits) == 1
    assert len(json_idearoot._fiscallinks) == 1

    assert len(json_world._idearoot._kids) == 2

    weekday_text = "weekdays"
    weekday_road = json_world.make_l1_road(weekday_text)
    weekday_idea_x = json_world.get_idea_obj(weekday_road)
    assert len(weekday_idea_x._kids) == 2

    sunday_text = "Sunday"
    sunday_road = json_world.make_road(weekday_road, sunday_text)
    sunday_idea = json_world.get_idea_obj(sunday_road)
    assert sunday_idea._weight == 20

    json_shave_idea = json_world.get_idea_obj(shave_road)
    zia_shave_idea = zia_world.get_idea_obj(shave_road)
    assert len(json_shave_idea._reasonunits) == 1
    assert json_shave_idea._cultureunit == zia_shave_idea._cultureunit
    assert json_shave_idea._cultureunit == tim_cultureunit
    assert json_shave_idea._originunit == zia_shave_idea._originunit
    print(f"{json_shave_idea._healerhold=}")
    assert json_shave_idea._healerhold == zia_shave_idea._healerhold
    assert len(json_shave_idea._fiscallinks) == 2
    assert len(json_shave_idea._factunits) == 1
    assert zia_shave_idea._problem_bool
    assert json_shave_idea._problem_bool == zia_shave_idea._problem_bool

    assert len(json_world._originunit._links) == 1
    assert json_world._originunit == zia_world._originunit


def test_worldunit_get_from_json_ReturnsCorrectObj_road_delimiter_Example():
    # GIVEN
    slash_delimiter = "/"
    before_bob_world = worldunit_shop("Bob", _road_delimiter=slash_delimiter)
    assert before_bob_world._road_delimiter != default_road_delimiter_if_none()

    # WHEN
    bob_json = before_bob_world.get_json()
    after_bob_world = worldunit_get_from_json(bob_json)

    # THEN
    assert after_bob_world._road_delimiter != default_road_delimiter_if_none()
    assert after_bob_world._road_delimiter == slash_delimiter
    assert after_bob_world._road_delimiter == before_bob_world._road_delimiter


def test_worldunit_get_from_json_ReturnsCorrectObj_road_delimiter_CharExample():
    # GIVEN
    slash_delimiter = "/"
    before_bob_world = worldunit_shop("Bob", _road_delimiter=slash_delimiter)
    bob_text = ",Bob"
    before_bob_world.add_charunit(bob_text)
    assert before_bob_world.char_exists(bob_text)

    # WHEN
    bob_json = before_bob_world.get_json()
    after_bob_world = worldunit_get_from_json(bob_json)

    # THEN
    after_bob_charunit = after_bob_world.get_char(bob_text)
    assert after_bob_charunit._road_delimiter == slash_delimiter


def test_worldunit_get_from_json_ReturnsCorrectObj_road_delimiter_BeliefExample():
    # GIVEN
    slash_delimiter = "/"
    before_bob_world = worldunit_shop("Bob", _road_delimiter=slash_delimiter)
    yao_text = "Yao"
    swim_text = f"{slash_delimiter}Swimmers"
    swim_beliefunit = beliefunit_shop(swim_text, _road_delimiter=slash_delimiter)
    swim_beliefunit.set_charlink(charlink_shop(yao_text))
    before_bob_world.add_charunit(yao_text)
    before_bob_world.set_beliefunit(swim_beliefunit)
    assert before_bob_world.get_beliefunit(swim_text) != None

    # WHEN
    bob_json = before_bob_world.get_json()
    after_bob_world = worldunit_get_from_json(bob_json)

    # THEN
    after_bob_beliefunit = after_bob_world.get_beliefunit(swim_text)
    assert after_bob_beliefunit._road_delimiter == slash_delimiter


def test_worldunit_get_from_json_jsonExportCorrectyExportsWorldUnit_weight():
    # GIVEN
    x1_world = example_worlds_world_v001()
    x1_world._weight = 15
    assert 15 == x1_world._weight
    assert x1_world._idearoot._weight != x1_world._weight
    assert x1_world._idearoot._weight == 1

    # WHEN
    x2_world = worldunit_get_from_json(x1_world.get_json())

    # THEN
    assert x1_world._weight == 15
    assert x1_world._weight == x2_world._weight
    assert x1_world._idearoot._weight == 1
    assert x1_world._idearoot._weight == x2_world._idearoot._weight
    assert x1_world._idearoot._kids == x2_world._idearoot._kids


def test_get_dict_of_world_from_dict_ReturnsDictOfWorldUnits():
    # GIVEN
    x1_world = example_worlds_world_v001()
    x2_world = example_worlds_get_world_x1_3levels_1reason_1facts()
    x3_world = example_worlds_get_world_base_time_example()
    print(f"{x1_world._owner_id}")
    print(f"{x2_world._owner_id}")
    print(f"{x3_world._owner_id}")

    cn_dict_of_dicts = {
        x1_world._owner_id: x1_world.get_dict(),
        x2_world._owner_id: x2_world.get_dict(),
        x3_world._owner_id: x3_world.get_dict(),
    }
    x1_world.clear_charunits_beliefholds()
    x2_world.clear_charunits_beliefholds()
    x3_world.clear_charunits_beliefholds()

    # WHEN
    ccn_dict_of_obj = get_dict_of_world_from_dict(cn_dict_of_dicts)

    # THEN
    assert ccn_dict_of_obj.get(x1_world._owner_id) != None
    assert ccn_dict_of_obj.get(x2_world._owner_id) != None
    assert ccn_dict_of_obj.get(x3_world._owner_id) != None
    cc1_idea_root = ccn_dict_of_obj.get(x1_world._owner_id)._idearoot
    assert cc1_idea_root._originunit == x1_world._idearoot._originunit
    assert ccn_dict_of_obj.get(x1_world._owner_id)._idea_dict == x1_world._idea_dict
    assert ccn_dict_of_obj.get(x1_world._owner_id) == x1_world
    ccn2_world = ccn_dict_of_obj.get(x2_world._owner_id)
    assert ccn2_world._idearoot._label == x2_world._idearoot._label
    assert ccn2_world._idearoot._parent_road == x2_world._idearoot._parent_road
    shave_road = ccn2_world.make_l1_road("shave")
    week_road = ccn2_world.make_l1_road("weekdays")
    assert ccn2_world.get_idea_obj(shave_road) == x2_world.get_idea_obj(shave_road)
    assert ccn2_world.get_idea_obj(week_road) == x2_world.get_idea_obj(week_road)
    assert ccn2_world._idearoot == x2_world._idearoot
    print(f"{ccn2_world._idea_dict.keys()=}")
    print(f"{x2_world._idea_dict.keys()=}")
    assert ccn2_world._idea_dict == x2_world._idea_dict
    assert ccn2_world == x2_world
    ccn_world3 = ccn_dict_of_obj.get(x3_world._owner_id)
    x3_world.calc_world_metrics()
    assert ccn_world3 == x3_world
