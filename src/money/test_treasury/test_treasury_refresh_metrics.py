from src._road.road import create_road
from src._world.world import (
    worldunit_shop,
    ideaunit_shop,
    beliefunit_shop,
    charlink_shop,
)
from src.money.money import moneyunit_shop
from src.money.examples.econ_env import (
    temp_real_id,
    get_texas_userhub,
    env_dir_setup_cleanup,
)
from src._instrument.sqlite import get_single_result
from src.money.treasury_sqlstr import (
    get_world_ideaunit_row_count,
    IdeaCatalog,
    get_world_ideaunit_table_insert_sqlstr,
    get_world_ideaunit_dict,
    get_world_idea_factunit_row_count,
    FactCatalog,
    get_world_idea_factunit_table_insert_sqlstr,
    get_world_beliefunit_row_count,
    BeliefUnitCatalog,
    get_world_beliefunit_table_insert_sqlstr,
    get_world_beliefunit_dict,
)
from src.money.examples.example_econ_worlds import (
    get_3node_world,
    get_6node_world,
    get_world_3CleanNodesRandomWeights,
)
from src._instrument.sqlite import get_single_result, get_row_count_sqlstr


def test_MoneyUnit_refresh_treasury_job_worlds_data_CorrectlyDeletesOldTreasuryInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=True)

    bob_text = "Bob"
    tom_text = "Tom"

    bob_worldunit = worldunit_shop(bob_text)
    bob_worldunit.add_charunit(tom_text, credor_weight=3, debtor_weight=1)
    x_money.userhub.save_job_world(bob_worldunit)
    x_money.refresh_treasury_job_worlds_data()
    charunit_count_sqlstr = get_row_count_sqlstr("world_charunit")
    assert get_single_result(x_money.get_treasury_conn(), charunit_count_sqlstr) == 1

    # WHEN
    x_money.refresh_treasury_job_worlds_data()

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), charunit_count_sqlstr) == 1


def test_MoneyUnit_refresh_treasury_job_worlds_data_CorrectlyDeletesOldTreasuryFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=False)

    bob_text = "Bob"
    tom_text = "Tom"

    bob_worldunit = worldunit_shop(bob_text)
    bob_worldunit.add_charunit(tom_text, credor_weight=3, debtor_weight=1)
    x_money.userhub.save_job_world(bob_worldunit)
    x_money.refresh_treasury_job_worlds_data()
    charunit_count_sqlstr = get_row_count_sqlstr("world_charunit")
    assert get_single_result(x_money.get_treasury_conn(), charunit_count_sqlstr) == 1

    # WHEN
    x_money.refresh_treasury_job_worlds_data()

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), charunit_count_sqlstr) == 1


def test_MoneyUnit_refresh_treasury_job_worlds_data_CorrectlyPopulatesCharunitTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 CharUnits = 12 charunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=True)

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"
    elu_text = "Elu"

    bob_worldunit = worldunit_shop(bob_text)
    bob_worldunit.add_charunit(tom_text, credor_weight=3, debtor_weight=1)
    bob_worldunit.add_charunit(sal_text, credor_weight=1, debtor_weight=4)
    bob_worldunit.add_charunit(elu_text, credor_weight=1, debtor_weight=4)
    x_money.userhub.save_job_world(bob_worldunit)

    sal_worldunit = worldunit_shop(sal_text)
    sal_worldunit.add_charunit(bob_text, credor_weight=1, debtor_weight=4)
    sal_worldunit.add_charunit(tom_text, credor_weight=3, debtor_weight=1)
    sal_worldunit.add_charunit(elu_text, credor_weight=1, debtor_weight=4)
    x_money.userhub.save_job_world(sal_worldunit)

    tom_worldunit = worldunit_shop(tom_text)
    tom_worldunit.add_charunit(bob_text, credor_weight=3, debtor_weight=1)
    tom_worldunit.add_charunit(sal_text, credor_weight=1, debtor_weight=4)
    tom_worldunit.add_charunit(elu_text, credor_weight=1, debtor_weight=4)
    x_money.userhub.save_job_world(tom_worldunit)

    elu_worldunit = worldunit_shop(elu_text)
    elu_worldunit.add_charunit(bob_text, credor_weight=3, debtor_weight=1)
    elu_worldunit.add_charunit(tom_text, credor_weight=1, debtor_weight=4)
    elu_worldunit.add_charunit(elu_text, credor_weight=1, debtor_weight=4)
    x_money.userhub.save_job_world(elu_worldunit)

    charunit_count_sqlstr = get_row_count_sqlstr("world_charunit")
    assert get_single_result(x_money.get_treasury_conn(), charunit_count_sqlstr) == 0

    # WHEN
    x_money.refresh_treasury_job_worlds_data()

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), charunit_count_sqlstr) == 12


def test_MoneyUnit_refresh_treasury_job_worlds_data_CorrectlyPopulatesWorldTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 CharUnits = 12 charunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=True)

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"
    elu_text = "Elu"

    x_money.userhub.save_job_world(worldunit_shop(bob_text))
    x_money.userhub.save_job_world(worldunit_shop(tom_text))
    x_money.userhub.save_job_world(worldunit_shop(sal_text))
    x_money.userhub.save_job_world(worldunit_shop(elu_text))

    world_count_sqlstrs = get_row_count_sqlstr("worldunit")
    assert get_single_result(x_money.get_treasury_conn(), world_count_sqlstrs) == 0

    # WHEN
    x_money.refresh_treasury_job_worlds_data()

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), world_count_sqlstrs) == 4


def test_MoneyUnit_refresh_treasury_job_worlds_data_CorrectlyPopulatesWorldTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 CharUnits = 12 charunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=True)

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"
    elu_text = "Elu"

    x_money.userhub.save_job_world(worldunit_shop(bob_text))
    x_money.userhub.save_job_world(worldunit_shop(tom_text))
    x_money.userhub.save_job_world(worldunit_shop(sal_text))
    x_money.userhub.save_job_world(worldunit_shop(elu_text))

    world_count_sqlstrs = get_row_count_sqlstr("worldunit")
    assert get_single_result(x_money.get_treasury_conn(), world_count_sqlstrs) == 0

    # WHEN
    x_money.refresh_treasury_job_worlds_data()

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), world_count_sqlstrs) == 4


def test_MoneyUnit_refresh_treasury_job_worlds_data_CorrectlyPopulates_world_beliefunit(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=True)

    bob_text = "Bob"
    tom_text = "Tom"
    elu_text = "Elu"
    bob_world = worldunit_shop(bob_text)
    tom_world = worldunit_shop(tom_text)
    bob_world.add_charunit(char_id=tom_text)
    tom_world.add_charunit(char_id=bob_text)
    tom_world.add_charunit(char_id=elu_text)
    x_money.userhub.save_job_world(bob_world)
    x_money.userhub.save_job_world(tom_world)

    sqlstr = get_row_count_sqlstr("world_beliefunit")
    assert get_single_result(x_money.get_treasury_conn(), sqlstr) == 0

    # WHEN
    x_money.refresh_treasury_job_worlds_data()

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), sqlstr) == 3


def test_MoneyUnit_get_world_ideaunit_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_worlds_data()

    bob_text = "Bob"
    with x_money.get_treasury_conn() as treasury_conn:
        assert get_world_ideaunit_row_count(treasury_conn, bob_text) == 0

    # WHEN
    resources_road = create_road(temp_real_id(), "resources")
    water_road = create_road(resources_road, "water")
    water_world_ideaunit = IdeaCatalog(owner_id=bob_text, idea_road=water_road)
    water_insert_sqlstr = get_world_ideaunit_table_insert_sqlstr(water_world_ideaunit)
    with x_money.get_treasury_conn() as treasury_conn:
        print(water_insert_sqlstr)
        treasury_conn.execute(water_insert_sqlstr)

    # THEN
    assert get_world_ideaunit_row_count(treasury_conn, bob_text) == 1


def test_MoneyUnit_refresh_treasury_job_worlds_data_Populates_world_ideaunit_table(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 CharUnits = 12 charunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_worlds_data()

    bob_text = "Bob"
    sal_text = "Sal"
    tim_text = "Tim"
    bob_world = get_3node_world()
    tim_world = get_6node_world()
    sal_world = get_world_3CleanNodesRandomWeights()
    bob_world.set_owner_id(new_owner_id=bob_text)
    tim_world.set_owner_id(new_owner_id=tim_text)
    sal_world.set_owner_id(new_owner_id=sal_text)
    x_money.userhub.save_job_world(bob_world)
    x_money.userhub.save_job_world(tim_world)
    x_money.userhub.save_job_world(sal_world)

    with x_money.get_treasury_conn() as treasury_conn:
        assert get_world_ideaunit_row_count(treasury_conn, bob_text) == 0

    # WHEN
    x_money.refresh_treasury_job_worlds_data()

    # THEN
    with x_money.get_treasury_conn() as treasury_conn:
        assert get_world_ideaunit_row_count(treasury_conn, bob_text) == 3
        assert get_world_ideaunit_row_count(treasury_conn, tim_text) == 6
        assert get_world_ideaunit_row_count(treasury_conn, sal_text) == 5


def test_MoneyUnit_get_world_ideaunit_dict_ReturnsCorrectData(env_dir_setup_cleanup):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_worlds_data()

    bob_text = "Bob"
    sal_text = "Sal"
    tim_text = "Tim"
    elu_text = "Elu"
    bob_world = get_3node_world()
    tim_world = get_6node_world()
    sal_world = get_world_3CleanNodesRandomWeights()
    elu_world = get_6node_world()
    bob_world.set_owner_id(new_owner_id=bob_text)
    tim_world.set_owner_id(new_owner_id=tim_text)
    sal_world.set_owner_id(new_owner_id=sal_text)
    elu_world.set_owner_id(new_owner_id=elu_text)
    x_money.userhub.save_job_world(bob_world)
    x_money.userhub.save_job_world(tim_world)
    x_money.userhub.save_job_world(sal_world)
    x_money.userhub.save_job_world(elu_world)
    x_money.refresh_treasury_job_worlds_data()
    i_count_sqlstr = get_row_count_sqlstr("world_ideaunit")
    with x_money.get_treasury_conn() as treasury_conn:
        print(f"{i_count_sqlstr=}")
        assert get_single_result(x_money.get_treasury_conn(), i_count_sqlstr) == 20

    # WHEN / THEN
    assert len(get_world_ideaunit_dict(x_money.get_treasury_conn())) == 20
    b_road = create_road(temp_real_id(), "B")
    assert len(get_world_ideaunit_dict(x_money.get_treasury_conn(), b_road)) == 3
    c_road = create_road(temp_real_id(), "C")
    ce_road = create_road(c_road, "E")
    assert len(get_world_ideaunit_dict(x_money.get_treasury_conn(), ce_road)) == 2
    ex_road = create_road(temp_real_id())
    assert len(get_world_ideaunit_dict(x_money.get_treasury_conn(), ex_road)) == 4


def test_MoneyUnit_get_world_idea_factunit_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 CharUnits = 12 charunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_worlds_data()

    bob_text = "Bob"
    with x_money.get_treasury_conn() as treasury_conn:
        assert get_world_idea_factunit_row_count(treasury_conn, bob_text) == 0

    # WHEN
    weather_road = create_road(temp_real_id(), "weather")
    weather_rain = FactCatalog(
        owner_id=bob_text,
        base=weather_road,
        pick=create_road(weather_road, "rain"),
    )
    water_insert_sqlstr = get_world_idea_factunit_table_insert_sqlstr(weather_rain)
    with x_money.get_treasury_conn() as treasury_conn:
        print(water_insert_sqlstr)
        treasury_conn.execute(water_insert_sqlstr)

    # THEN
    assert get_world_idea_factunit_row_count(treasury_conn, bob_text) == 1


def test_refresh_treasury_job_worlds_data_Populates_world_idea_factunit_table(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 CharUnits = 12 charunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_worlds_data()

    # create 3 worlds with varying numbers of facts
    bob_text = "Bob"
    sal_text = "Sal"
    tim_text = "Tim"
    bob_world = get_3node_world()
    tim_world = get_6node_world()
    sal_world = get_world_3CleanNodesRandomWeights()
    bob_world.set_owner_id(new_owner_id=bob_text)
    tim_world.set_owner_id(new_owner_id=tim_text)
    sal_world.set_owner_id(new_owner_id=sal_text)
    c_text = "C"
    c_road = tim_world.make_l1_road(c_text)
    f_text = "F"
    f_road = create_road(c_road, f_text)
    b_text = "B"
    b_road = tim_world.make_l1_road(b_text)
    # for idea_x in tim_world._idea_dict.values():
    #     print(f"{f_road=} {idea_x.get_road()=}")
    tim_world.set_fact(base=c_road, pick=f_road)

    bob_world.set_fact(base=c_road, pick=f_road)
    bob_world.set_fact(base=b_road, pick=b_road)

    casa_text = "casa"
    casa_road = sal_world.make_l1_road(casa_text)
    cookery_text = "clean cookery"
    cookery_road = create_road(casa_road, cookery_text)
    sal_world.set_fact(base=cookery_road, pick=cookery_road)

    x_money.userhub.save_job_world(bob_world)
    x_money.userhub.save_job_world(tim_world)
    x_money.userhub.save_job_world(sal_world)

    with x_money.get_treasury_conn() as treasury_conn:
        assert get_world_idea_factunit_row_count(treasury_conn, bob_text) == 0
        assert get_world_idea_factunit_row_count(treasury_conn, tim_text) == 0
        assert get_world_idea_factunit_row_count(treasury_conn, sal_text) == 0

    # WHEN
    x_money.refresh_treasury_job_worlds_data()

    # THEN
    print(f"{get_world_idea_factunit_row_count(treasury_conn, bob_text)=}")
    print(f"{get_world_idea_factunit_row_count(treasury_conn, tim_text)=}")
    print(f"{get_world_idea_factunit_row_count(treasury_conn, sal_text)=}")
    with x_money.get_treasury_conn() as treasury_conn:
        assert get_world_idea_factunit_row_count(treasury_conn, bob_text) == 2
        assert get_world_idea_factunit_row_count(treasury_conn, tim_text) == 1
        assert get_world_idea_factunit_row_count(treasury_conn, sal_text) == 1


def test_MoneyUnit_get_world_beliefunit_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 CharUnits = 12 charunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_worlds_data()

    bob_text = "Bob"
    with x_money.get_treasury_conn() as treasury_conn:
        assert get_world_beliefunit_row_count(treasury_conn, bob_text) == 0

    # WHEN
    bob_belief_x = BeliefUnitCatalog(
        owner_id=bob_text,
        beliefunit_belief_id="US Dollar",
    )
    bob_belief_sqlstr = get_world_beliefunit_table_insert_sqlstr(bob_belief_x)
    with x_money.get_treasury_conn() as treasury_conn:
        print(bob_belief_sqlstr)
        treasury_conn.execute(bob_belief_sqlstr)

    # THEN
    assert get_world_beliefunit_row_count(treasury_conn, bob_text) == 1


def test_MoneyUnit_get_world_beliefunit_dict_ReturnsBeliefUnitData(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())

    bob_text = "Bob"
    tom_text = "Tom"
    elu_text = "Elu"
    bob_world = worldunit_shop(bob_text)
    tom_world = worldunit_shop(tom_text)
    bob_world.add_charunit(char_id=tom_text)
    tom_world.add_charunit(char_id=bob_text)
    tom_world.add_charunit(char_id=elu_text)
    x_money.userhub.save_job_world(bob_world)
    x_money.userhub.save_job_world(tom_world)
    x_money.refresh_treasury_job_worlds_data()
    sqlstr = get_row_count_sqlstr("world_beliefunit")
    assert get_single_result(x_money.get_treasury_conn(), sqlstr) == 3

    # WHEN
    with x_money.get_treasury_conn() as treasury_conn:
        print("try to grab BeliefUnit data")
        world_beliefunit_dict = get_world_beliefunit_dict(db_conn=treasury_conn)

    # THEN
    assert len(world_beliefunit_dict) == 3
    bob_world_tom_belief = f"{bob_text} {tom_text}"
    tom_bob_world_belief = f"{tom_text} {bob_text}"
    tom_world_elu_belief = f"{tom_text} {elu_text}"
    assert world_beliefunit_dict.get(bob_world_tom_belief) != None
    assert world_beliefunit_dict.get(tom_bob_world_belief) != None
    assert world_beliefunit_dict.get(tom_world_elu_belief) != None
