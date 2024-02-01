from src._prime.road import (
    create_road,
    default_road_delimiter_if_none,
    create_economyaddress,
)
from src.world.problem import healerlink_shop, economylink_shop
from src.world.person import PersonUnit, personunit_shop
from src.world.problem import problemunit_shop
from pytest import raises as pytest_raises


def test_PersonUnit_exists():
    # GIVEN / WHEN
    x_person = PersonUnit()

    # THEN
    assert x_person.person_id is None
    assert x_person.person_dir is None
    assert x_person._economys is None
    assert x_person._problems is None
    assert x_person._primary_contract_road is None
    assert x_person._primary_contract_active is None
    assert x_person._primary_contract_obj is None
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
    sue_personroad = create_road(sue_personroad, "economy1")

    # WHEN
    x_person = personunit_shop(
        person_id=sue_text, _primary_contract_road=sue_personroad
    )

    # THEN
    assert x_person.person_id == sue_text
    assert x_person.person_dir == f"/persons/{sue_text}"
    assert x_person._economys == {}
    assert x_person._problems == {}
    assert x_person._primary_contract_road == sue_personroad
    assert x_person._primary_contract_active
    assert x_person._primary_contract_obj is None
    assert x_person._road_delimiter == default_road_delimiter_if_none()


def test_personunit_shop_ReturnsPersonUnitWithCorrectAttrs_v2():
    # GIVEN
    dallas_text = "dallas"
    dallas_dir = ""
    slash_text = "/"
    x_primary_contract_active = False

    # WHEN
    x_person = personunit_shop(
        person_id=dallas_text,
        person_dir=dallas_dir,
        _primary_contract_active=x_primary_contract_active,
        _road_delimiter=slash_text,
    )

    # THEN
    assert x_person.person_id == dallas_text
    assert x_person.person_dir == dallas_dir
    assert x_person._primary_contract_active == x_primary_contract_active
    assert x_person._road_delimiter == slash_text


def test_PersonUnit_set_primary_contract_active_CorrectlySetsAttr():
    # GIVEN
    yao_text = "Yao"
    yao_personunit = personunit_shop(person_id=yao_text)
    assert yao_personunit._primary_contract_active

    # WHEN
    x_primary_contract_active = False
    yao_personunit.set_primary_contract_active(x_primary_contract_active)

    # THEN
    assert yao_personunit._primary_contract_active == x_primary_contract_active


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


def test_PersonUnit_economylink_exists_ReturnsCorrectObj():
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
    assert yao_personunit.economylink_exists(texas_text) == False

    # WHEN
    yao_healerlink.set_economylink(economylink_shop(texas_text))

    # THEN
    assert yao_personunit.economylink_exists(texas_text)

    # WHEN
    yao_healerlink.del_economylink(texas_text)


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


def test_PersonUnit_set_economyunit_RaisesErrorIfNoAssociatedProblemExists():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)

    # WHEN/THEN
    diet_text = "diet"
    with pytest_raises(Exception) as excinfo:
        yao_personunit.set_economyunit(economy_id=diet_text)
    assert (
        str(excinfo.value)
        == f"Cannot set_economyunit {diet_text} because no justifying problem exists."
    )


def test_PersonUnit_set_economyunit_CorrectlyCreatesEconomyUnit():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    knee_text = "knee discomfort"
    yao_personunit.create_problemunit_from_problem_id(knee_text)
    diet_text = "diet"
    knee_problem = yao_personunit.get_problem_obj(knee_text)
    knee_problem.set_healerlink(healerlink_shop(yao_text))
    yao_healerlink = knee_problem.get_healerlink(yao_text)
    yao_healerlink.set_economylink(economylink_shop(diet_text))
    assert yao_personunit._economys == {}
    assert yao_personunit._primary_contract_road is None

    # WHEN
    yao_personunit.set_economyunit(economy_id=diet_text)

    # THEN
    # diet_economy = yao_person.get_economy()
    assert yao_personunit._problems != {}
    assert yao_personunit._economys != {}
    diet_economy = yao_personunit._economys.get(diet_text)
    assert diet_economy != None
    assert diet_economy.economy_id == diet_text
    assert diet_economy.economys_dir == f"{yao_person_dir}/economys"
    assert yao_personunit._primary_contract_road == yao_personunit.make_proad(
        knee_text, yao_text, diet_text
    )


def test_PersonUnit_set_economyunit_CorrectlyCreatesEconomyLink():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    diet_text = "diet"
    assert yao_personunit.economylink_exists(diet_text) == False

    # WHEN
    knee_text = "knee discomfort"
    yao_personunit.set_economyunit(economy_id=diet_text, x_problem_id=knee_text)

    # THEN
    assert yao_personunit.economylink_exists(diet_text)


def test_PersonUnit_economyunit_exists_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    diet_text = "diet"
    assert yao_personunit.economyunit_exists(diet_text) == False

    # WHEN
    yao_personunit.set_economyunit(economy_id=diet_text, x_problem_id="Knee")

    # THEN
    assert yao_personunit.economyunit_exists(diet_text)


def test_PersonUnit_all_economyunits_linked_to_problem_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    cooking_text = "cooking"
    hunger_text = "Hunger"
    diet_text = "diet"
    knee_text = "knee"
    yao_personunit.set_economyunit(diet_text, x_problem_id="self-image")
    gym_text = "gym"
    yao_personunit.set_economyunit(gym_text, x_problem_id=knee_text)
    yao_personunit.set_economyunit(cooking_text, x_problem_id=hunger_text)
    yao_personunit.del_problemunit(hunger_text)
    assert yao_personunit.all_economyunits_linked_to_problem() == False

    # WHEN
    hunger_problemunit = problemunit_shop(hunger_text)
    hunger_problemunit.set_healerlink(healerlink_shop(yao_text))
    yao_healerlink = hunger_problemunit.get_healerlink(yao_text)
    yao_healerlink.set_economylink(economylink_shop(cooking_text))
    yao_personunit.set_problemunit(hunger_problemunit)

    # THEN
    assert yao_personunit.all_economyunits_linked_to_problem()

    # WHEN
    yao_personunit.del_problemunit(knee_text)
    assert yao_personunit.all_economyunits_linked_to_problem() == False

    # WHEN
    yao_personunit.del_economyunit(gym_text)

    # THEN
    assert yao_personunit.all_economyunits_linked_to_problem()


def test_PersonUnit_get_economyunit_CorrectlyGetsEconomyUnit():
    # GIVEN
    yao_text = "Yao"
    yao_personunit = personunit_shop(person_id=yao_text)
    diet_text = "diet"
    yao_personunit.set_economyunit(diet_text, x_problem_id="Knee")

    # WHEN
    diet_economy = yao_personunit.get_economyunit(diet_text)

    # THEN
    assert diet_economy != None
    assert diet_economy.economy_id == diet_text
    assert diet_economy.economys_dir == f"{yao_personunit.person_dir}/economys"


def test_PersonUnit_get_economyaddress_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    diet_text = "diet"
    yao_personunit.set_economyunit(diet_text, x_problem_id="Knee")

    # WHEN
    diet_economyaddress = yao_personunit.get_economyaddress(diet_text)

    # THEN
    assert diet_economyaddress != None
    assert diet_economyaddress == create_road(yao_text, diet_text)


def test_PersonUnit_get_economyaddress_RaisesException():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    diet_text = "diet"
    yao_personunit.set_economyunit(diet_text, x_problem_id="Knee")

    # WHEN/THEN
    texas_text = "Texas"
    with pytest_raises(Exception) as excinfo:
        yao_personunit.get_economyaddress(texas_text)
    assert (
        str(excinfo.value)
        == f"Cannot get economyaddress for {yao_text} because economy {texas_text} does not exist"
    )


def test_PersonUnit_del_economyunit_CorrectlyDeletesEconomyUnit():
    # GIVEN
    yao_text = "Yao"
    yao_person_dir = f"/persons/{yao_text}"
    yao_personunit = personunit_shop(person_id=yao_text, person_dir=yao_person_dir)
    diet_text = "diet"
    yao_personunit.set_economyunit(diet_text, x_problem_id="Knee")
    before_diet_economy = yao_personunit.get_economyunit(diet_text)
    assert before_diet_economy != None
    assert before_diet_economy.economy_id == diet_text
    assert before_diet_economy.economys_dir == f"{yao_person_dir}/economys"

    # WHEN
    yao_personunit.del_economyunit(diet_text)

    # THEN
    after_diet_economy = yao_personunit.get_economyunit(diet_text)
    assert after_diet_economy is None


def test_PersonUnit_is_primary_contract_road_valid_ReturnsCorrectBool():
    # GIVEN
    yao_text = "Yao"
    yao_personunit = personunit_shop(person_id=yao_text)
    assert yao_personunit._primary_contract_road is None
    assert yao_personunit.is_primary_contract_road_valid() == False

    # WHEN
    diet_text = "diet"
    knee_text = "knee"
    yao_personunit.set_economyunit(diet_text, x_problem_id=knee_text)

    # THEN
    diet_proad = yao_personunit.make_proad(knee_text, yao_text, diet_text)
    assert yao_personunit._primary_contract_road == diet_proad
    assert yao_personunit.is_primary_contract_road_valid()


def test_PersonUnit_make_personroad_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_personunit = personunit_shop(person_id=yao_text)
    assert yao_personunit._road_delimiter != None
    ohio_text = "Ohio"
    knee_text = "Knee"
    yao_personunit.set_economyunit(ohio_text, x_problem_id=knee_text)
    assert yao_personunit.economyunit_exists(ohio_text)
    knee_problemunit = yao_personunit.get_problem_obj(knee_text)
    sue_text = "Sue"
    knee_problemunit.set_healerlink(healerlink_shop(sue_text))
    sue_healerlink = knee_problemunit.get_healerlink(sue_text)
    sue_healerlink.set_economylink(economylink_shop(ohio_text))

    iowa_text = "Iowa"
    leg_text = "Leg"
    yao_personunit.set_economyunit(iowa_text, x_problem_id=leg_text)
    assert yao_personunit._primary_contract_road != None

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
    yao_personunit.set_economyunit(ohio_text, x_problem_id=knee_text)
    knee_problemunit = yao_personunit.get_problem_obj(knee_text)
    sue_text = "Sue"
    knee_problemunit.set_healerlink(healerlink_shop(sue_text))
    sue_healerlink = knee_problemunit.get_healerlink(sue_text)
    sue_healerlink.set_economylink(economylink_shop(ohio_text))

    iowa_text = "Iowa"
    leg_text = "Leg"
    yao_personunit.set_economyunit(iowa_text, x_problem_id=leg_text)
    assert yao_personunit._primary_contract_road != None

    # WHEN / THEN
    arm_text = "Arm"
    with pytest_raises(Exception) as excinfo:
        yao_personunit.make_proad(arm_text)
    assert (
        str(excinfo.value)
        == f"PersonRoad make failure: ProblemID '{arm_text}' does not exist."
    )

    # WHEN / THEN
    bob_text = "Bob"
    with pytest_raises(Exception) as excinfo:
        yao_personunit.make_proad(knee_text, bob_text)
    assert (
        str(excinfo.value)
        == f"PersonRoad make failure: HealerID '{bob_text}' does not exist."
    )

    # WHEN / THEN
    idaho_text = "Idaho"
    with pytest_raises(Exception) as excinfo:
        yao_personunit.make_proad(knee_text, sue_text, idaho_text)
    assert (
        str(excinfo.value)
        == f"PersonRoad make failure: EconomyID '{idaho_text}' does not exist."
    )


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


def test_PersonUnit_get_economyslink_objs_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    yao_personunit = personunit_shop(person_id=yao_text)
    ohio_text = "Ohio"
    knee_text = "Knee"
    yao_personunit.set_economyunit(ohio_text, x_problem_id=knee_text)
    knee_problemunit = yao_personunit.get_problem_obj(knee_text)
    sue_text = "Sue"
    knee_problemunit.set_healerlink(healerlink_shop(sue_text))
    sue_healerlink = knee_problemunit.get_healerlink(sue_text)
    sue_healerlink.set_economylink(economylink_shop(ohio_text))

    iowa_text = "Iowa"
    leg_text = "Leg"
    yao_personunit.set_economyunit(iowa_text, x_problem_id=leg_text)
    assert yao_personunit.problem_exists(knee_text)

    # WHEN
    x_economylinks = yao_personunit.get_economyslink_objs()

    # THEN
    knee_yao_ohio_proad = yao_personunit.make_proad(knee_text, yao_text, ohio_text)
    knee_sue_ohio_proad = yao_personunit.make_proad(knee_text, sue_text, ohio_text)
    leg_yao_iowa_proad = yao_personunit.make_proad(leg_text, yao_text, iowa_text)

    print(f"{x_economylinks.keys()=}")
    assert x_economylinks.get(knee_yao_ohio_proad) != None
    assert x_economylinks.get(knee_sue_ohio_proad) != None
    assert x_economylinks.get(leg_yao_iowa_proad) != None
    assert len(x_economylinks) == 3
