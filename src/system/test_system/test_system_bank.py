from src.system.system import SystemUnit
from src.agent.agent import AgentUnit
from src.agent.idea import IdeaKid
from src.agent.group import groupunit_shop
from src.agent.member import memberlink_shop
from src.agent.x_func import delete_dir as x_func_delete_dir
from os import path as os_path
from src.system.examples.env_kit import (
    get_temp_env_name,
    get_test_systems_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from src.system.y_func import check_connection, get_single_result_back
from sqlite3 import connect as sqlite3_connect, Connection
from src.system.bank_sqlstr import (
    get_db_tables,
    get_groupunit_catalog_table_count,
    get_table_count_sqlstr,
)


def test_system_create_bank_db_CreatesBankDBIfItDoesNotExist(
    env_dir_setup_cleanup,
):
    # GIVEN create system
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null()

    # clear out any bank.db file
    x_func_delete_dir(dir=e1.get_bank_db_path())
    assert os_path.exists(e1.get_bank_db_path()) == False

    # WHEN
    e1._create_bank_db()

    # THEN
    assert os_path.exists(e1.get_bank_db_path())


def test_system_create_bank_db_CanCreateBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create system
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    # clear out any bank.db file
    e1._bank_db = None
    assert e1._bank_db is None
    assert os_path.exists(e1.get_bank_db_path()) == False

    # WHEN
    e1._create_bank_db(in_memory=True)

    # THEN
    assert e1._bank_db != None
    assert os_path.exists(e1.get_bank_db_path()) == False


def test_system_refresh_bank_metrics_CanConnectToBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN create system
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null(in_memory_bank=True)
    # e1._create_bank_db(in_memory=True)
    assert os_path.exists(e1.get_bank_db_path()) == False

    # WHEN
    e1.refresh_bank_metrics()

    # THEN
    assert os_path.exists(e1.get_bank_db_path()) == False


def test_system_get_bank_db_conn_CreatesBankDBIfItDoesNotExist(env_dir_setup_cleanup):
    # GIVEN create system
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        check_connection(e1.get_bank_conn())
    assert str(excinfo.value) == "unable to open database file"

    # WHEN
    e1.create_dirs_if_null(in_memory_bank=True)

    # THEN
    assert check_connection(e1.get_bank_conn())


def test_system_create_dirs_if_null_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # GIVEN create system
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())

    # WHEN
    e1.create_dirs_if_null(in_memory_bank=True)

    # THEN
    with e1.get_bank_conn() as bank_conn:
        tables_dict = get_db_tables(bank_conn)

    # row_count = 0
    # for table_name, table_x in tables_dict.items():
    #     row_count += 1
    #     print(f" {table_x=} {row_count}. {table_name=}")

    curr_tables = {
        0: "agentunits",
        1: "ledger",
        2: "river_tmember",
        3: "river_flow",
        4: "river_bucket",
        5: "idea_catalog",
        6: "acptfact_catalog",
        7: "groupunit_catalog",
    }

    assert tables_dict.get(curr_tables[0]) != None
    assert tables_dict.get(curr_tables[1]) != None
    assert tables_dict.get(curr_tables[2]) != None
    assert tables_dict.get(curr_tables[3]) != None
    assert tables_dict.get(curr_tables[4]) != None
    assert tables_dict.get(curr_tables[5]) != None
    assert tables_dict.get(curr_tables[6]) != None
    assert tables_dict.get(curr_tables[7]) != None
    assert len(tables_dict) == len(curr_tables)


def test_system_refresh_bank_metrics_CorrectlyDeletesOldBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"

    bob = AgentUnit(_desc=bob_text)
    bob.add_memberunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob)
    e1.refresh_bank_metrics()
    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 1

    # WHEN
    e1.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 1


def test_system_refresh_bank_metrics_CorrectlyDeletesOldBankFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null(in_memory_bank=False)

    bob_text = "bob"
    tom_text = "tom"

    bob = AgentUnit(_desc=bob_text)
    bob.add_memberunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob)
    e1.refresh_bank_metrics()
    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 1

    # WHEN
    e1.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 1


def test_system_refresh_bank_metrics_CorrectlyPopulatesLedgerTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example system with 4 Persons, each with 3 Memberunits = 12 ledger rows
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    bob = AgentUnit(_desc=bob_text)
    bob.add_memberunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    bob.add_memberunit(name=sal_text, creditor_weight=1, debtor_weight=4)
    bob.add_memberunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob)

    sal = AgentUnit(_desc=sal_text)
    sal.add_memberunit(name=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_memberunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    sal.add_memberunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    e1.save_agentunit_obj_to_agents_dir(agent_x=sal)

    tom = AgentUnit(_desc=tom_text)
    tom.add_memberunit(name=bob_text, creditor_weight=3, debtor_weight=1)
    tom.add_memberunit(name=sal_text, creditor_weight=1, debtor_weight=4)
    tom.add_memberunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom)

    elu = AgentUnit(_desc=elu_text)
    elu.add_memberunit(name=bob_text, creditor_weight=3, debtor_weight=1)
    elu.add_memberunit(name=tom_text, creditor_weight=1, debtor_weight=4)
    elu.add_memberunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    e1.save_agentunit_obj_to_agents_dir(agent_x=elu)

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 0

    # WHEN
    e1.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 12


def test_system_refresh_bank_metrics_CorrectlyPopulatesAgentTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example system with 4 Persons, each with 3 Memberunits = 12 ledger rows
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=bob_text))
    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=tom_text))
    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=sal_text))
    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=elu_text))

    sqlstr_count_agents = get_table_count_sqlstr("agentunits")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_agents) == 0

    # WHEN
    e1.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_agents) == 4


def test_system_refresh_bank_metrics_CorrectlyPopulatesAgentTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example system with 4 Persons, each with 3 Memberunits = 12 ledger rows
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=bob_text))
    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=tom_text))
    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=sal_text))
    e1.save_agentunit_obj_to_agents_dir(agent_x=AgentUnit(_desc=elu_text))

    sqlstr_count_agents = get_table_count_sqlstr("agentunits")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_agents) == 0

    # WHEN
    e1.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_agents) == 4


def test_system_refresh_bank_metrics_CorrectlyPopulates_groupunit_catalog(
    env_dir_setup_cleanup,
):
    # GIVEN
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"
    bob_agent = AgentUnit(_desc=bob_text)
    tom_agent = AgentUnit(_desc=tom_text)
    bob_agent.add_memberunit(name=tom_text)
    tom_agent.add_memberunit(name=bob_text)
    tom_agent.add_memberunit(name=elu_text)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob_agent)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom_agent)

    sqlstr = get_table_count_sqlstr("groupunit_catalog")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr) == 0

    # WHEN
    e1.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr) == 3


def test_system_set_agent_attr_defined_by_system_CorrectlyPopulatesAgent_Groupunit_Memberlinks(
    env_dir_setup_cleanup,
):
    # GIVEN
    e1 = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    # create 4 agents, 1 with group "swimming expert" linked to 1 member
    # two others have idea "src,sports,swimming"
    # run set_bank_metrics
    # assert
    # _memberlinks_set_by_system_road
    # assert group "swimming expert" has 1 member
    # change groupunit "swimming expert" _memberlinks_set_by_system_road ==  "root_desc,sports,swimmer"
    # run set_bank_metrics
    # assert group "swimming expert" has 2 different member

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"

    sal_agent = AgentUnit(_desc=sal_text)
    bob_agent = AgentUnit(_desc=bob_text)
    tom_agent = AgentUnit(_desc=tom_text)
    ava_agent = AgentUnit(_desc=ava_text)

    swim_text = "swimming"
    sports_text = "sports"
    sal_sports_road = f"{sal_agent._desc},{sports_text}"
    bob_sports_road = f"{bob_agent._desc},{sports_text}"
    tom_sports_road = f"{tom_agent._desc},{sports_text}"

    sal_agent.add_idea(idea_kid=IdeaKid(_desc=swim_text), walk=sal_sports_road)
    bob_agent.add_idea(idea_kid=IdeaKid(_desc=swim_text), walk=bob_sports_road)
    tom_agent.add_idea(idea_kid=IdeaKid(_desc=swim_text), walk=tom_sports_road)

    sal_agent.add_memberunit(name=bob_text, creditor_weight=2, debtor_weight=2)

    swim_group_text = "swimming expert"
    swim_group_unit = groupunit_shop(name=swim_group_text)
    bob_link = memberlink_shop(name=bob_text)
    swim_group_unit.set_memberlink(memberlink=bob_link)
    sal_agent.set_groupunit(groupunit=swim_group_unit)

    e1.save_agentunit_obj_to_agents_dir(agent_x=sal_agent)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob_agent)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom_agent)
    e1.save_agentunit_obj_to_agents_dir(agent_x=ava_agent)

    e1.set_agent_attr_defined_by_system(agent_name=sal_text)
    e1_sal_agent = e1.get_agent_from_agents_dir(_desc=sal_text)
    assert len(e1_sal_agent._groups.get(swim_group_text)._members) == 1

    # WHEN
    # change groupunit "swimming expert" _memberlinks_set_by_system_road ==  "root_desc,sports,swimmer"
    sal_swim_road = f"{sal_sports_road},{swim_text}"
    swim_group_unit.set_attr(_memberlinks_set_by_system_road=sal_swim_road)
    sal_agent.set_groupunit(groupunit=swim_group_unit)
    e1.save_agentunit_obj_to_agents_dir(agent_x=sal_agent)
    e1.set_agent_attr_defined_by_system(agent_name=sal_text)

    # THEN
    e1_sal_agent = e1.get_agent_from_agents_dir(_desc=sal_text)
    assert len(e1_sal_agent._groups.get(swim_group_text)._members) == 2
