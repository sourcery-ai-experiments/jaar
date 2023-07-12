from lib.polity.polity import PolityUnit
from lib.agent.agent import AgentUnit
from lib.agent.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from lib.polity.test_polity.env_tools import (
    get_temp_env_name,
    get_test_politys_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from lib.polity.y_func import check_connection, get_single_result_back
from sqlite3 import connect as sqlite3_connect, Connection


def test_polity_create_bank_db_if_null_CreatesBankDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create polity
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    e1.create_dirs_if_null()

    # clear out any bank.db file
    x_func_delete_dir(dir=e1.get_bank_db_path())
    assert os_path.exists(e1.get_bank_db_path()) == False

    # WHEN
    e1._create_bank_db_if_null()

    # THEN
    assert os_path.exists(e1.get_bank_db_path())


def test_polity_create_bank_db_if_null_CanCreateBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create polity
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    # clear out any bank.db file
    e1._bank_db = None
    assert e1._bank_db is None
    assert os_path.exists(e1.get_bank_db_path()) == False

    # WHEN
    e1._create_bank_db_if_null(in_memory=True)

    # THEN
    assert e1._bank_db != None
    assert os_path.exists(e1.get_bank_db_path()) == False


def test_polity_refresh_bank_metrics_CanConnectToBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create polity
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    e1.create_dirs_if_null(in_memory_bank=True)
    # e1._create_bank_db_if_null(in_memory=True)
    assert os_path.exists(e1.get_bank_db_path()) == False

    # WHEN
    e1.refresh_bank_metrics()

    # THEN
    assert os_path.exists(e1.get_bank_db_path()) == False


def test_polity_get_bank_db_conn_CreatesBankDBIfItDoesNotExist(env_dir_setup_cleanup):
    # GIVEN create polity
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(e1.get_bank_conn())
    assert str(excinfo.value) == f"unable to open database file"

    # WHEN
    e1.create_dirs_if_null(in_memory_bank=True)

    # THEN
    assert check_connection(e1.get_bank_conn())


def test_polity_create_dirs_if_null_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # GIVEN create polity
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())

    # WHEN
    e1.create_dirs_if_null(in_memory_bank=True)

    # THEN
    with e1.get_bank_conn() as bank_conn:
        sqlstr = "SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;"
        print(f"{sqlstr=}")
        results = bank_conn.execute(sqlstr)

        row_count = 0
        tables_dict = {"agentunits": 0, "ledger": 0, "river_tally": 0, "river_flow": 0}
        for row in results:
            row_count += 1
            print(f"Polity '{e1.name}' {row_count}. bank_db table '{row[0]}'")
            if tables_dict.get(row[0]) != None:
                tables_dict[row[0]] = 1

    row_count = 0
    for table_name, table_x in tables_dict.items():
        row_count += 1
        print(f" {table_x=} {row_count}. {table_name=}")
        assert table_x == 1


def test_polity_refresh_bank_metrics_CorrectlyPopulatesLedgerTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example polity with 4 Persons, each with 3 Allyunits = 12 ledger rows
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    bob = AgentUnit(_desc=bob_text)
    bob.add_allyunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    bob.add_allyunit(name=sal_text, creditor_weight=1, debtor_weight=4)
    bob.add_allyunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob)

    sal = AgentUnit(_desc=sal_text)
    sal.add_allyunit(name=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_allyunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    sal.add_allyunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    e1.save_agentunit_obj_to_agents_dir(agent_x=sal)

    tom = AgentUnit(_desc=tom_text)
    tom.add_allyunit(name=bob_text, creditor_weight=3, debtor_weight=1)
    tom.add_allyunit(name=sal_text, creditor_weight=1, debtor_weight=4)
    tom.add_allyunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom)

    elu = AgentUnit(_desc=elu_text)
    elu.add_allyunit(name=bob_text, creditor_weight=3, debtor_weight=1)
    elu.add_allyunit(name=tom_text, creditor_weight=1, debtor_weight=4)
    elu.add_allyunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    e1.save_agentunit_obj_to_agents_dir(agent_x=elu)

    sqlstr_count_ledger = "SELECT COUNT(*) FROM ledger;"
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 0

    # WHEN
    e1.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 12


def test_polity_refresh_bank_metrics_CorrectlyPopulatesAgentTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example polity with 4 Persons, each with 3 Allyunits = 12 ledger rows
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=bob_text))
    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=tom_text))
    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=sal_text))
    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=elu_text))

    sqlstr_count_agents = "SELECT COUNT(*) FROM agentunits;"
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_agents) == 0

    # WHEN
    e1.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_agents) == 4


def test_polity_refresh_bank_metrics_CorrectlyPopulatesAgentTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example polity with 4 Persons, each with 3 Allyunits = 12 ledger rows
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=bob_text))
    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=tom_text))
    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=sal_text))
    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=elu_text))

    sqlstr_count_agents = "SELECT COUNT(*) FROM agentunits;"
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_agents) == 0

    # WHEN
    e1.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_agents) == 4
