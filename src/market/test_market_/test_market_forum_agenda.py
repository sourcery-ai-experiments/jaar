from src.agenda.agenda import agendaunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_1Task_1CE0MinutesReason_1Belief as example_agendas_get_agenda_1Task_1CE0MinutesReason_1Belief,
)
from src.market.market import marketunit_shop
from src.market.examples.example_clerks import (
    get_1node_agenda as example_get_1node_agenda,
    get_1node_agenda as example_get_7nodeJRootWithH_agenda,
)
from src.market.examples.market_env_kit import (
    get_temp_env_market_id,
    get_test_markets_dir,
    env_dir_setup_cleanup,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_market_set_agenda_CreatesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    x_market_id = get_temp_env_market_id()
    x_market = marketunit_shop(x_market_id, markets_dir=get_test_markets_dir())
    x_market.set_market_dirs()
    y_agenda = example_get_1node_agenda()
    y_path = f"{x_market.get_forum_dir()}/{y_agenda._agent_id}.json"
    assert os_path.exists(y_path) == False

    # WHEN
    x_market.save_forum_agenda(y_agenda)

    # THEN
    print(f"{y_path=}")
    assert os_path.exists(y_path)


def test_market_get_agenda_currentlyGetsAgenda(env_dir_setup_cleanup):
    # GIVEN
    x_market_id = get_temp_env_market_id()
    x_market = marketunit_shop(x_market_id, markets_dir=get_test_markets_dir())
    x_market.set_market_dirs(in_memory_bank=True)
    y_agenda = example_get_7nodeJRootWithH_agenda()
    x_market.save_forum_agenda(y_agenda)

    # WHEN / THEN
    assert x_market.get_forum_agenda(agent_id=y_agenda._agent_id) == y_agenda


def test_market_change_forum_agent_id_ChangesAgendaPersonID(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_market_id = get_temp_env_market_id()
    x_market = marketunit_shop(x_market_id, get_test_markets_dir())
    x_market.set_market_dirs(in_memory_bank=True)
    old_agent_id = "old1"
    y_agenda = agendaunit_shop(_agent_id=old_agent_id)
    old_y_agenda_path = f"{x_market.get_forum_dir()}/{old_agent_id}.json"
    x_market.save_forum_agenda(y_agenda)
    print(f"{old_y_agenda_path=}")

    # WHEN
    new_agent_id = "new1"
    new_y_agenda_path = f"{x_market.get_forum_dir()}/{new_agent_id}.json"
    assert os_path.exists(new_y_agenda_path) == False
    assert os_path.exists(old_y_agenda_path)
    x_market.change_forum_agent_id(
        old_agent_id=old_agent_id, new_agent_id=new_agent_id
    )

    # THEN
    assert os_path.exists(old_y_agenda_path) == False
    assert os_path.exists(new_y_agenda_path)


def test_market_Sets_idearoot_Label(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_market_id = get_temp_env_market_id()
    x_market = marketunit_shop(x_market_id, markets_dir=get_test_markets_dir())
    x_market.set_market_dirs(in_memory_bank=True)
    old_x_agenda = example_agendas_get_agenda_1Task_1CE0MinutesReason_1Belief()
    assert old_x_agenda._idearoot._label == "A"

    # WHEN
    x_market.save_forum_agenda(old_x_agenda)

    # THEN
    new_x_agenda = x_market.get_forum_agenda(old_x_agenda._agent_id)
    assert new_x_agenda._idearoot._label == x_market_id
