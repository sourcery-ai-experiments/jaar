from src._prime.road import create_road, default_road_delimiter_if_none, create_proad
from src.market.market import (
    get_temp_env_problem_id,
    get_temp_env_market_id,
    get_temp_env_healer_id,
    get_temp_env_person_id,
)
from src.world.problem import healerlink_shop, marketlink_shop
from src.world.person import PersonUnit, personunit_shop
from src.world.problem import problemunit_shop
from pytest import raises as pytest_raises
from src.world.examples.world_env_kit import (
    get_temp_world_dir,
    worlds_dir_setup_cleanup,
)
from src.instrument.file import get_proad_dir


def test_PersonUnit_exists():
    # GIVEN / WHEN
    x_person = PersonUnit()

    # THEN
    assert x_person.person_id is None
    assert x_person.person_dir is None
    assert x_person._markets is None
    assert x_person._market_metrics is None
    assert x_person._problembeams is None
    assert x_person._problems is None
    assert x_person._road_delimiter is None


def test_PersonUnit_set_person_id_CorrectlySetsAttr():
    # GIVEN / WHEN
    x_person = PersonUnit()
    assert x_person.person_id is None

    # GIVEN
    yao_text = "Yao"
    x_person.set_person_id(yao_text)

    # THEN
    assert x_person.person_id == yao_text


def test_PersonUnit_set_person_id_RaisesErrorIf_person_id_Contains_road_delimiter():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        personunit_shop(person_id=bob_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_personunit_shop_ReturnsNonePersonUnitWithCorrectAttrs_v1():
    # GIVEN
    sue_text = "Sue"
    sue_personroad = create_road(sue_text, "problem1")
    sue_personroad = create_road(sue_personroad, "healer1")
    sue_personroad = create_road(sue_personroad, "market1")

    # WHEN
    x_person = personunit_shop(person_id=sue_text)

    # THEN
    assert x_person.person_id == sue_text
    assert x_person.person_dir == f"/persons/{sue_text}"
    assert x_person._markets == {}
    assert x_person._problembeams == {}
    assert x_person._problems == {}
    assert x_person._road_delimiter == default_road_delimiter_if_none()


def test_PersonUnit_create_problemunit_from_problem_id_CorrectlyCreatesProblemUnit():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)

    # WHEN
    knee_text = "knee discomfort"
    yao_personunit.create_problemunit_from_problem_id(knee_text)

    # THEN
    knee_problem = yao_personunit._problems.get(knee_text)
    assert knee_problem != None
    assert knee_problem.problem_id == knee_text


def test_PersonUnit_create_problemunit_from_problem_id_CorrectlyCreatesProblemUnit():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)

    # WHEN
    knee_text = "knee discomfort"
    knee_problemunit = problemunit_shop(knee_text)
    yao_personunit.set_problemunit(knee_problemunit)

    # THEN
    knee_problem = yao_personunit._problems.get(knee_text)
    assert knee_problem != None
    assert knee_problem.problem_id == knee_text


def test_PersonUnit_get_problemunit_CorrectlyGetsProblemUnit():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    knee_text = "knee discomfort"
    yao_personunit.create_problemunit_from_problem_id(knee_text)

    # WHEN
    knee_problem = yao_personunit.get_problem_obj(knee_text)

    # THEN
    assert knee_problem != None
    assert knee_problem.problem_id == knee_text


def test_PersonUnit_marketlink_exists_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    knee_text = "knee discomfort"
    yao_personunit.create_problemunit_from_problem_id(knee_text)
    texas_text = "Texas"
    knee_problem = yao_personunit.get_problem_obj(knee_text)
    knee_problem.set_healerlink(healerlink_shop(yao_text))
    yao_healerlink = knee_problem.get_healerlink(yao_text)
    assert yao_personunit.marketlink_exists(texas_text) == False

    # WHEN
    yao_healerlink.set_marketlink(marketlink_shop(texas_text))

    # THEN
    assert yao_personunit.marketlink_exists(texas_text)

    # WHEN
    yao_healerlink.del_marketlink(texas_text)


def test_PersonUnit_del_problemunit_CorrectlyDeletesProblemUnit():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    knee_text = "knee discomfort"
    yao_personunit.create_problemunit_from_problem_id(knee_text)
    before_knee_problem = yao_personunit.get_problem_obj(knee_text)
    assert before_knee_problem != None
    assert before_knee_problem.problem_id == knee_text

    # WHEN
    yao_personunit.del_problemunit(knee_text)

    # THEN
    after_knee_problem = yao_personunit.get_problem_obj(knee_text)
    assert after_knee_problem is None


def test_PersonUnit_set_marketunit_RaisesErrorIfNoAssociatedProblemExists():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)

    # WHEN/THEN
    diet_text = "diet"
    with pytest_raises(Exception) as excinfo:
        yao_personunit.set_marketunit(market_id=diet_text)
    assert (
        str(excinfo.value)
        == f"Cannot set_marketunit {diet_text} because no justifying problem exists."
    )


def test_PersonUnit_set_marketunit_CorrectlyCreatesMarketUnit_v1():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    knee_text = "knee discomfort"
    diet_problem_dir = f"/problems/{knee_text}"
    yao_personunit.create_problemunit_from_problem_id(knee_text)
    knee_problem = yao_personunit.get_problem_obj(knee_text)
    knee_problem.set_healerlink(healerlink_shop(yao_text))
    yao_healerlink = knee_problem.get_healerlink(yao_text)
    diet_healer_dir = f"{diet_problem_dir}/healers/{yao_text}"
    diet_text = "diet"
    yao_healerlink.set_marketlink(marketlink_shop(diet_text))
    diet_market_dir = f"{diet_healer_dir}/markets/{diet_text}"
    assert yao_personunit._markets == {}

    # WHEN
    yao_personunit.set_marketunit(diet_text, x_problem_id=knee_text)

    # THEN
    # diet_market = yao_person.get_market()
    assert yao_personunit._problems != {}
    assert yao_personunit._markets != {}
    diet_market = yao_personunit._markets.get(diet_text)
    assert diet_market != None
    assert diet_market.market_id == diet_text
    assert diet_market._healer_id == yao_text
    print(f"         {diet_market_dir=}")
    print(f"{diet_market.markets_dir=}")
    diet_proad = create_proad(yao_text, knee_text, yao_text, diet_text)
    assert diet_market.markets_dir == get_proad_dir(diet_proad)


def test_PersonUnit_set_marketunit_CorrectlyCreatesMarketUnit_v2():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    knee_text = "knee discomfort"
    yao_personunit.create_problemunit_from_problem_id(knee_text)
    knee_problem = yao_personunit.get_problem_obj(knee_text)
    sue_text = "Sue"
    knee_problem.set_healerlink(healerlink_shop(sue_text))
    sue_healerlink = knee_problem.get_healerlink(sue_text)
    diet_text = "diet"
    sue_healerlink.set_marketlink(marketlink_shop(diet_text))
    assert yao_personunit._markets == {}
    assert yao_personunit.healer_exists(sue_text)

    # WHEN
    yao_personunit.set_marketunit(
        diet_text, x_problem_id=knee_text, x_healer_id=sue_text
    )

    # THEN
    # diet_market = yao_person.get_market()
    diet_market = yao_personunit._markets.get(diet_text)
    assert diet_market != None
    assert diet_market.market_id == diet_text
    assert diet_market._healer_id == sue_text
    diet_proad = create_proad(yao_text, knee_text, sue_text, diet_text)
    # print(f"         {diet_market_dir=}")
    # print(f"{diet_market.markets_dir=}")
    assert diet_market.markets_dir == get_proad_dir(diet_proad)


def test_PersonUnit_set_marketunit_CorrectlyCreatesMarketLink():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    diet_text = "diet"
    assert yao_personunit.marketlink_exists(diet_text) == False

    # WHEN
    knee_text = "knee discomfort"
    yao_personunit.set_marketunit(market_id=diet_text, x_problem_id=knee_text)

    # THEN
    assert yao_personunit.marketlink_exists(diet_text)


def test_PersonUnit_marketunit_exists_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    diet_text = "diet"
    assert yao_personunit.marketunit_exists(diet_text) == False

    # WHEN
    yao_personunit.set_marketunit(market_id=diet_text, x_problem_id="Knee")

    # THEN
    assert yao_personunit.marketunit_exists(diet_text)


def test_PersonUnit_all_marketunits_linked_to_problem_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    cooking_text = "cooking"
    hunger_text = "Hunger"
    diet_text = "diet"
    knee_text = "knee"
    yao_personunit.set_marketunit(diet_text, x_problem_id="self-image")
    gym_text = "gym"
    yao_personunit.set_marketunit(gym_text, x_problem_id=knee_text)
    yao_personunit.set_marketunit(cooking_text, x_problem_id=hunger_text)
    yao_personunit.del_problemunit(hunger_text)
    assert yao_personunit.all_marketunits_linked_to_problem() == False

    # WHEN
    hunger_problemunit = problemunit_shop(hunger_text)
    hunger_problemunit.set_healerlink(healerlink_shop(yao_text))
    yao_healerlink = hunger_problemunit.get_healerlink(yao_text)
    yao_healerlink.set_marketlink(marketlink_shop(cooking_text))
    yao_personunit.set_problemunit(hunger_problemunit)

    # THEN
    assert yao_personunit.all_marketunits_linked_to_problem()

    # WHEN
    yao_personunit.del_problemunit(knee_text)
    assert yao_personunit.all_marketunits_linked_to_problem() == False

    # WHEN
    yao_personunit.del_marketunit(gym_text)

    # THEN
    assert yao_personunit.all_marketunits_linked_to_problem()


def test_PersonUnit_get_marketunit_CorrectlyGetsMarketUnit():
    # GIVEN
    yao_text = "Yao"
    yao_personunit = personunit_shop(person_id=yao_text)
    diet_text = "diet"
    knee_text = "knee"
    yao_personunit.set_marketunit(diet_text, x_problem_id=knee_text)

    # WHEN
    diet_market = yao_personunit.get_marketunit(diet_text)

    # THEN
    assert diet_market != None
    assert diet_market.market_id == diet_text

    diet_proad = create_proad(yao_text, knee_text, yao_text, diet_text)
    # diet_market_dir = get_proad_dir(diet_proad)
    # print(f"         {diet_market_dir=}")
    # print(f"{diet_market.markets_dir=}")
    assert diet_market.markets_dir == get_proad_dir(diet_proad)


def test_PersonUnit_del_marketunit_CorrectlyDeletesMarketUnit():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    diet_text = "diet"
    knee_text = "knee"
    yao_personunit.set_marketunit(diet_text, x_problem_id=knee_text)
    before_diet_market = yao_personunit.get_marketunit(diet_text)
    assert before_diet_market != None
    assert before_diet_market.market_id == diet_text

    diet_proad = create_proad(yao_text, knee_text, yao_text, diet_text)
    # diet_market_dir = get_proad_dir(diet_proad)
    # print(f"                {diet_market_dir=}")
    # print(f"{before_diet_market.markets_dir=}")
    assert before_diet_market.markets_dir == get_proad_dir(diet_proad)

    # WHEN
    yao_personunit.del_marketunit(diet_text)

    # THEN
    after_diet_market = yao_personunit.get_marketunit(diet_text)
    assert after_diet_market is None


def test_PersonUnit_make_personroad_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_personunit = personunit_shop(person_id=yao_text)
    assert yao_personunit._road_delimiter != None
    ohio_text = "Ohio"
    knee_text = "Knee"
    yao_personunit.set_marketunit(ohio_text, x_problem_id=knee_text)
    assert yao_personunit.marketunit_exists(ohio_text)
    knee_problemunit = yao_personunit.get_problem_obj(knee_text)
    sue_text = "Sue"
    knee_problemunit.set_healerlink(healerlink_shop(sue_text))
    sue_healerlink = knee_problemunit.get_healerlink(sue_text)
    sue_healerlink.set_marketlink(marketlink_shop(ohio_text))

    iowa_text = "Iowa"
    leg_text = "Leg"
    yao_personunit.set_marketunit(iowa_text, x_problem_id=leg_text)

    # WHEN / THEN
    yao_1_proad = "Yao"
    assert yao_1_proad == yao_personunit.make_proad()
    yao_2_proad = create_road(yao_1_proad, knee_text)
    assert yao_2_proad == yao_personunit.make_proad(knee_text)
    yao_3_proad = create_road(yao_2_proad, sue_text)
    assert yao_3_proad == yao_personunit.make_proad(knee_text, sue_text)
    yao_4_proad = create_road(yao_3_proad, ohio_text)
    assert yao_4_proad == yao_personunit.make_proad(knee_text, sue_text, ohio_text)


def test_PersonUnit_make_personroad_RaisesException():
    # GIVEN
    yao_text = "Yao"
    yao_personunit = personunit_shop(person_id=yao_text)
    assert yao_personunit._road_delimiter != None
    ohio_text = "Ohio"
    knee_text = "Knee"
    yao_personunit.set_marketunit(ohio_text, x_problem_id=knee_text)
    knee_problemunit = yao_personunit.get_problem_obj(knee_text)
    sue_text = "Sue"
    knee_problemunit.set_healerlink(healerlink_shop(sue_text))
    sue_healerlink = knee_problemunit.get_healerlink(sue_text)
    sue_healerlink.set_marketlink(marketlink_shop(ohio_text))

    iowa_text = "Iowa"
    leg_text = "Leg"
    yao_personunit.set_marketunit(iowa_text, x_problem_id=leg_text)

    # WHEN / THEN
    arm_text = "Arm"
    with pytest_raises(Exception) as excinfo:
        yao_personunit.make_proad(arm_text)
    assert str(excinfo.value) == f"proad: ProblemID '{arm_text}' does not exist."

    # WHEN / THEN
    bob_text = "Bob"
    with pytest_raises(Exception) as excinfo:
        yao_personunit.make_proad(knee_text, bob_text)
    assert str(excinfo.value) == f"proad: HealerID '{bob_text}' does not exist."

    # WHEN / THEN
    idaho_text = "Idaho"
    with pytest_raises(Exception) as excinfo:
        yao_personunit.make_proad(knee_text, sue_text, idaho_text)
    assert str(excinfo.value) == f"proad: MarketID '{idaho_text}' does not exist."


def test_PersonUnit_get_problemunits_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_personunit = personunit_shop(person_id=yao_text)
    knee_text = "Knee"
    yao_personunit.set_problemunit(problemunit_shop(knee_text))
    arm_text = "Arm"
    yao_personunit.set_problemunit(problemunit_shop(arm_text))
    leg_text = "Leg"
    yao_personunit.set_problemunit(problemunit_shop(leg_text))

    # WHEN
    x_problemunits = yao_personunit.get_problemunits()

    # THEN
    knee_proad = yao_personunit.make_proad(knee_text)
    arm_proad = yao_personunit.make_proad(arm_text)
    leg_proad = yao_personunit.make_proad(leg_text)

    assert x_problemunits.get(knee_proad) != None
    assert x_problemunits.get(arm_proad) != None
    assert x_problemunits.get(leg_proad) != None
    assert len(x_problemunits) == 3


def test_PersonUnit_get_healerlink_objs_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_personunit = personunit_shop(person_id=yao_text)
    knee_text = "Knee"
    yao_personunit.set_problemunit(problemunit_shop(knee_text))
    knee_problemunit = yao_personunit.get_problem_obj(knee_text)
    knee_problemunit.set_healerlink(healerlink_shop(sue_text))
    arm_text = "Arm"
    yao_personunit.set_problemunit(problemunit_shop(arm_text))
    arm_problemunit = yao_personunit.get_problem_obj(arm_text)
    arm_problemunit.set_healerlink(healerlink_shop(yao_text))
    leg_text = "Leg"
    yao_personunit.set_problemunit(problemunit_shop(leg_text))
    leg_problemunit = yao_personunit.get_problem_obj(leg_text)
    leg_problemunit.set_healerlink(healerlink_shop(sue_text))
    leg_problemunit.set_healerlink(healerlink_shop(yao_text))

    # WHEN
    x_healerlinks = yao_personunit.get_healerlink_objs()

    # THEN
    knee_sue_proad = yao_personunit.make_proad(knee_text, sue_text)
    arm_yao_proad = yao_personunit.make_proad(arm_text, yao_text)
    leg_sue_proad = yao_personunit.make_proad(leg_text, sue_text)
    leg_yao_proad = yao_personunit.make_proad(leg_text, sue_text)

    print(f"{x_healerlinks.keys()=}")
    assert x_healerlinks.get(knee_sue_proad) != None
    assert x_healerlinks.get(arm_yao_proad) != None
    assert x_healerlinks.get(leg_sue_proad) != None
    assert x_healerlinks.get(leg_yao_proad) != None
    knee_sue_healerlink = knee_problemunit.get_healerlink(sue_text)
    arm_yao_healerlink = arm_problemunit.get_healerlink(yao_text)
    leg_sue_healerlink = leg_problemunit.get_healerlink(sue_text)
    leg_yao_healerlink = leg_problemunit.get_healerlink(sue_text)
    assert x_healerlinks.get(knee_sue_proad) == knee_sue_healerlink
    assert x_healerlinks.get(arm_yao_proad) == arm_yao_healerlink
    assert x_healerlinks.get(leg_sue_proad) == leg_sue_healerlink
    assert x_healerlinks.get(leg_yao_proad) == leg_yao_healerlink
    assert len(x_healerlinks) == 4


def test_PersonUnit_get_marketslink_objs_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_personunit = personunit_shop(person_id=yao_text)
    ohio_text = "Ohio"
    knee_text = "Knee"
    yao_personunit.set_marketunit(ohio_text, x_problem_id=knee_text)
    knee_problemunit = yao_personunit.get_problem_obj(knee_text)
    sue_text = "Sue"
    knee_problemunit.set_healerlink(healerlink_shop(sue_text))
    sue_healerlink = knee_problemunit.get_healerlink(sue_text)
    sue_healerlink.set_marketlink(marketlink_shop(ohio_text))

    iowa_text = "Iowa"
    leg_text = "Leg"
    yao_personunit.set_marketunit(iowa_text, x_problem_id=leg_text)
    assert yao_personunit.problem_exists(knee_text)

    # WHEN
    x_marketlinks = yao_personunit.get_marketslink_objs()

    # THEN
    knee_yao_ohio_proad = yao_personunit.make_proad(knee_text, yao_text, ohio_text)
    knee_sue_ohio_proad = yao_personunit.make_proad(knee_text, sue_text, ohio_text)
    leg_yao_iowa_proad = yao_personunit.make_proad(leg_text, yao_text, iowa_text)

    print(f"{x_marketlinks.keys()=}")
    assert x_marketlinks.get(knee_yao_ohio_proad) != None
    assert x_marketlinks.get(knee_sue_ohio_proad) != None
    assert x_marketlinks.get(leg_yao_iowa_proad) != None
    assert len(x_marketlinks) == 3
