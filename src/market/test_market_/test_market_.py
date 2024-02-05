from src._prime.road import default_road_delimiter_if_none, create_road
from src.instrument.file import delete_dir
from os import path as os_path
from src.market.market import (
    MarketUnit,
    marketunit_shop,
    get_temp_env_person_id,
    get_temp_env_problem_id,
    get_temp_env_healer_id,
    get_temp_env_market_id,
)
from src.market.examples.market_env_kit import (
    get_test_markets_dir,
    change_market_id_example_market,
    copy_evaluation_market,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises


def test_MarketUnit_exists():
    # GIVEN
    x_market_id = "test1"

    # WHEN
    x_market = MarketUnit(x_market_id, markets_dir=get_test_markets_dir())

    # THEN
    assert x_market.market_id == x_market_id
    assert x_market.markets_dir == get_test_markets_dir()
    assert x_market._manager_person_id is None
    assert x_market._problem_id is None
    assert x_market._healer_id is None
    assert x_market._road_delimiter is None


def test_MarketUnit_set_market_id_CorrectlySetsAttr():
    # GIVEN
    x_marketunit = MarketUnit()
    assert x_marketunit.market_id is None

    # WHEN
    texas_text = "texas"
    x_marketunit.set_market_id(texas_text)

    # THEN
    assert x_marketunit.market_id == texas_text


def test_MarketUnit_set_proad_nodes_CorrectsSetAttrsGivenVariables():
    # GIVEN
    x_market_id = get_temp_env_market_id()
    x_market = MarketUnit(market_id=x_market_id)

    # WHEN
    zia_text = "Zia"
    knee_text = "knee"
    sue_text = "Sue"
    x_market.set_proad_nodes(
        person_id=zia_text, problem_id=knee_text, healer_id=sue_text
    )

    # THEN
    assert x_market._manager_person_id == zia_text
    assert x_market._problem_id == knee_text
    assert x_market._healer_id == sue_text


def test_MarketUnit_set_proad_nodes_CorrectsSetsAttrsGivenNones():
    # GIVEN
    x_market_id = get_temp_env_market_id()
    x_market = MarketUnit(market_id=x_market_id)

    # WHEN
    x_market.set_proad_nodes()

    # THEN
    assert x_market._manager_person_id == get_temp_env_person_id()
    assert x_market._problem_id == get_temp_env_problem_id()
    assert x_market._healer_id == get_temp_env_healer_id()


def test_marketunit_shop_ReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_market_id = get_temp_env_market_id()
    market_dir = f"src/market/examples/markets/{x_market_id}"
    sue_text = "Sue"
    assert os_path.exists(market_dir) is False
    knee_text = "knee"
    zia_text = "knee"

    # WHEN
    x_market = marketunit_shop(
        x_market_id,
        get_test_markets_dir(),
        _manager_person_id=sue_text,
        _problem_id=knee_text,
        _healer_id=zia_text,
    )

    # THEN
    assert x_market != None
    assert x_market.market_id == x_market_id
    assert os_path.exists(market_dir)
    assert x_market._treasury_db != None
    assert x_market._manager_person_id == sue_text
    assert x_market._problem_id == knee_text
    assert x_market._healer_id == zia_text
    assert x_market._clerkunits == {}
    assert x_market._road_delimiter == default_road_delimiter_if_none()


def test_marketunit_shop_ReturnsObj_WithTempNames(env_dir_setup_cleanup):
    # GIVEN
    x_market_id = get_temp_env_market_id()
    # assert os_path.exists(market_dir) is False

    # WHEN
    x_market = marketunit_shop(x_market_id)

    # THEN
    assert x_market != None
    assert x_market.market_id == x_market_id
    # assert os_path.exists(market_dir)
    assert x_market._treasury_db != None
    assert x_market._manager_person_id == get_temp_env_person_id()
    assert x_market._problem_id == get_temp_env_problem_id()
    assert x_market._healer_id == get_temp_env_healer_id()
    assert x_market._clerkunits == {}
    assert x_market._road_delimiter == default_road_delimiter_if_none()


def test_marketunit_shop_RaisesErrorIfParameterContains_road_delimiter():
    # GIVEN
    slash_text = "/"
    texas_text = f"Texas{slash_text}Arkansas"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        marketunit_shop(market_id=texas_text, _road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{texas_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_MarketUnit_set_road_delimiter_CorrectSetsAttribute(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_market_id = get_temp_env_market_id()
    market_dir = f"src/market/examples/markets/{x_market_id}"
    sue_text = "Sue"
    x_market = marketunit_shop(
        x_market_id, get_test_markets_dir(), _manager_person_id=sue_text
    )
    assert x_market._road_delimiter == default_road_delimiter_if_none()

    # WHEN
    slash_text = "/"
    x_market.set_road_delimiter(slash_text)

    # THEN
    assert x_market._road_delimiter == slash_text


def test_MarketUnit_create_dirs_if_null_CreatesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create market
    x_market_id = get_temp_env_market_id()
    x_market = MarketUnit(x_market_id, markets_dir=get_test_markets_dir())
    print(f"{get_test_markets_dir()=} {x_market.markets_dir=}")
    # delete_dir(x_market.get_object_root_dir())
    print(f"delete {x_market.get_object_root_dir()=}")
    market_dir = f"src/market/examples/markets/{x_market_id}"
    market_file_name = "market.json"
    market_file_path = f"{market_dir}/{market_file_name}"
    forum_text = "forum"
    forum_dir = f"{market_dir}/{forum_text}"
    clerkunits_dir = f"{market_dir}/clerkunits"
    treasury_file_name = "treasury.db"
    treasury_file_path = f"{market_dir}/{treasury_file_name}"

    assert os_path.exists(market_dir) is False
    assert os_path.isdir(market_dir) is False
    assert os_path.exists(market_file_path) is False
    assert os_path.exists(forum_dir) is False
    assert os_path.exists(clerkunits_dir) is False
    assert os_path.exists(treasury_file_path) is False

    # WHEN
    x_market.create_dirs_if_null(in_memory_treasury=False)

    # THEN check agendas src directory created
    assert os_path.exists(market_dir)
    assert os_path.isdir(market_dir)
    assert os_path.exists(market_file_path)
    assert os_path.exists(forum_dir)
    assert os_path.exists(clerkunits_dir)
    assert os_path.exists(treasury_file_path)
    assert x_market.get_object_root_dir() == market_dir
    assert x_market.get_forum_dir() == forum_dir
    assert x_market.get_clerkunits_dir() == clerkunits_dir
    assert x_market.get_treasury_db_path() == treasury_file_path


def test_change_market_id_example_market_CorrectlyChangesDirAndFiles(
    env_dir_setup_cleanup,
):
    # GIVEN create market
    old_x_market_id = get_temp_env_market_id()
    old_market_dir = f"src/market/examples/markets/{old_x_market_id}"
    old_market_file_name = "market.json"
    old_market_file_path = f"{old_market_dir}/{old_market_file_name}"
    forum_text = "forum"
    old_forum_dir = f"{old_market_dir}/{forum_text}"
    old_clerkunits_dir = f"{old_market_dir}/clerkunits"

    new_x_market_id = "ex_env1"
    new_market_dir = f"src/market/examples/markets/{new_x_market_id}"
    new_market_file_name = "market.json"
    new_market_file_path = f"{new_market_dir}/{new_market_file_name}"
    forum_text = "forum"
    new_forum_dir = f"{new_market_dir}/{forum_text}"
    new_clerkunits_dir = f"{new_market_dir}/clerkunits"
    delete_dir(dir=new_market_dir)
    print(f"{new_market_dir=}")

    x_market = marketunit_shop(
        market_id=old_x_market_id, markets_dir=get_test_markets_dir()
    )
    # delete_dir(x_market.get_object_root_dir())
    # print(f"{x_market.get_object_root_dir()=}")

    x_market.create_dirs_if_null(in_memory_treasury=True)

    assert os_path.exists(old_market_dir)
    assert os_path.isdir(old_market_dir)
    assert os_path.exists(old_market_file_path)
    assert os_path.exists(old_forum_dir)
    assert os_path.exists(old_clerkunits_dir)
    assert x_market.get_forum_dir() == old_forum_dir
    assert x_market.get_clerkunits_dir() == old_clerkunits_dir

    assert os_path.exists(new_market_dir) is False
    assert os_path.isdir(new_market_dir) is False
    assert os_path.exists(new_market_file_path) is False
    assert os_path.exists(new_forum_dir) is False
    assert os_path.exists(new_clerkunits_dir) is False
    assert x_market.get_forum_dir() != new_forum_dir
    assert x_market.get_clerkunits_dir() != new_clerkunits_dir
    assert x_market.market_id != new_x_market_id

    # WHEN
    change_market_id_example_market(
        market_obj=x_market, new_market_id=new_x_market_id
    )

    # THEN check agendas src directory created
    assert os_path.exists(old_market_dir) is False
    assert os_path.isdir(old_market_dir) is False
    assert os_path.exists(old_market_file_path) is False
    assert os_path.exists(old_forum_dir) is False
    assert os_path.exists(old_clerkunits_dir) is False
    assert x_market.get_forum_dir() != old_forum_dir
    assert x_market.get_clerkunits_dir() != old_clerkunits_dir

    assert os_path.exists(new_market_dir)
    assert os_path.isdir(new_market_dir)
    assert os_path.exists(new_market_file_path)
    assert os_path.exists(new_forum_dir)
    assert os_path.exists(new_clerkunits_dir)
    assert x_market.get_forum_dir() == new_forum_dir
    assert x_market.get_clerkunits_dir() == new_clerkunits_dir
    assert x_market.market_id == new_x_market_id

    # Undo change to directory
    # delete_dir(dir=old_market_dir)
    # print(f"{old_market_dir=}")
    delete_dir(dir=new_market_dir)
    print(f"{new_market_dir=}")


def test_copy_evaluation_market_CorrectlyCopiesDirAndFiles(env_dir_setup_cleanup):
    # GIVEN create market
    old_x_market_id = get_temp_env_market_id()
    old_market_dir = f"src/market/examples/markets/{old_x_market_id}"
    old_market_file_name = "market.json"
    old_market_file_path = f"{old_market_dir}/{old_market_file_name}"
    forum_text = "forum"
    old_forum_dir = f"{old_market_dir}/{forum_text}"
    old_clerkunits_dir = f"{old_market_dir}/clerkunits"

    x_market = marketunit_shop(old_x_market_id, get_test_markets_dir())
    x_market.create_dirs_if_null()

    assert os_path.exists(old_market_dir)
    assert os_path.isdir(old_market_dir)
    assert os_path.exists(old_market_file_path)
    assert os_path.exists(old_forum_dir)
    assert os_path.exists(old_clerkunits_dir)
    assert x_market.get_forum_dir() == old_forum_dir
    assert x_market.get_clerkunits_dir() == old_clerkunits_dir

    new_x_market_id = "ex_env1"
    new_market_dir = f"src/market/examples/markets/{new_x_market_id}"
    new_market_file_name = "market.json"
    new_market_file_path = f"{new_market_dir}/{new_market_file_name}"
    new_forum_dir = f"{new_market_dir}/{forum_text}"
    new_clerkunits_dir = f"{new_market_dir}/clerkunits"

    assert os_path.exists(new_market_dir) is False
    assert os_path.isdir(new_market_dir) is False
    assert os_path.exists(new_market_file_path) is False
    assert os_path.exists(new_forum_dir) is False
    assert os_path.exists(new_clerkunits_dir) is False
    assert x_market.get_forum_dir() != new_forum_dir
    assert x_market.get_clerkunits_dir() != new_clerkunits_dir
    assert x_market.market_id != new_x_market_id

    # WHEN
    copy_evaluation_market(
        src_market_id=x_market.market_id, dest_market_id=new_x_market_id
    )

    # THEN check agendas src directory created
    assert os_path.exists(old_market_dir)
    assert os_path.isdir(old_market_dir)
    assert os_path.exists(old_market_file_path)
    assert os_path.exists(old_forum_dir)
    assert os_path.exists(old_clerkunits_dir)
    assert x_market.get_forum_dir() == old_forum_dir
    assert x_market.get_clerkunits_dir() == old_clerkunits_dir

    assert os_path.exists(new_market_dir)
    assert os_path.isdir(new_market_dir)
    assert os_path.exists(new_market_file_path)
    assert os_path.exists(new_forum_dir)
    assert os_path.exists(new_clerkunits_dir)
    assert x_market.get_forum_dir() != new_forum_dir
    assert x_market.get_clerkunits_dir() != new_clerkunits_dir
    assert x_market.market_id != new_x_market_id

    # Undo change to directory
    # delete_dir(x_market.get_object_root_dir())
    # delete_dir(dir=old_market_dir)
    delete_dir(dir=new_market_dir)


def test_copy_evaluation_market_CorrectlyRaisesError(env_dir_setup_cleanup):
    # GIVEN create market
    old_x_market_id = get_temp_env_market_id()
    x_market = marketunit_shop(old_x_market_id, get_test_markets_dir())
    x_market.create_dirs_if_null()

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        copy_evaluation_market(
            src_market_id=x_market.market_id, dest_market_id=old_x_market_id
        )
    assert (
        str(excinfo.value)
        == f"Cannot copy market to '{x_market.get_object_root_dir()}' directory because '{x_market.get_object_root_dir()}' exists."
    )


def test_MarketUnit_get_road_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    x_market_id = get_temp_env_market_id()
    x_market = marketunit_shop(x_market_id, markets_dir=get_test_markets_dir())
    bob_text = "Bob"
    market_road_with_woot = create_road(x_market.market_id, bob_text)
    market_road_wo_root = bob_text
    # healer_list_wo_root = get_all_road_nodes(market_road_wo_root)
    bloomers_text = "bloomers"
    bloomers_road_with_root = create_road(market_road_with_woot, bloomers_text)
    bloomers_road_wo_root = create_road(market_road_wo_root, bloomers_text)
    # bloomers_list_wo_root = get_all_road_nodes(bloomers_road_wo_root)
    roses_text = "roses"
    roses_road_with_root = create_road(bloomers_road_with_root, roses_text)
    roses_road_wo_root = create_road(bloomers_road_wo_root, roses_text)
    # roses_list_wo_root = get_all_road_nodes(roses_road_wo_root)

    # WHEN / THEN
    assert x_market.market_id == x_market.build_market_road()
    assert market_road_with_woot == x_market.build_market_road(market_road_wo_root)
    assert bloomers_road_with_root == x_market.build_market_road(
        bloomers_road_wo_root
    )
    assert roses_road_with_root == x_market.build_market_road(roses_road_wo_root)
