from lib.world.world import WorldUnit
from lib.agent.agent import AgentUnit
from lib.world.examples.env_tools import (
    get_temp_env_name,
    get_test_worlds_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from lib.world.y_func import check_connection, get_single_result_back
from lib.world.bank_sqlstr import (
    get_river_tally_dict,
    get_river_flow_dict,
    get_table_count_sqlstr,
)


def test_world_set_river_sphere_for_agent_CorrectlyPopulatesriver_tallyTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example world with 4 Persons, each with 3 Allyunits = 12 ledger rows
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"

    sal = AgentUnit(_desc=sal_text)
    sal.add_allyunit(name=bob_text, creditor_weight=1)
    sal.add_allyunit(name=tom_text, creditor_weight=3)
    e1.save_agentunit_obj_to_agents_dir(agent_x=sal)

    bob = AgentUnit(_desc=bob_text)
    bob.add_allyunit(name=sal_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob)

    tom = AgentUnit(_desc=tom_text)
    tom.add_allyunit(name=sal_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom)

    e1.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 4

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 0

    # WHEN
    e1.set_river_sphere_for_agent(agent_name=sal_text)

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 4
    with e1.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_agent_name=sal_text)

    flow_0 = river_flows.get(0)
    flow_1 = river_flows.get(1)
    assert flow_1.src_name == "sal" and flow_1.dst_name == "tom"
    assert flow_1.river_tree_level == 1
    assert flow_1.currency_start == 0.25
    assert flow_1.currency_close == 1
    assert flow_1.parent_flow_num is None
    flow_2 = river_flows.get(2)
    flow_3 = river_flows.get(3)
    assert flow_3.src_name == "tom" and flow_3.dst_name == "sal"
    assert flow_3.river_tree_level == 2
    assert flow_3.parent_flow_num == 1

    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 2

    with e1.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, sal_text)
    assert len(river_tallys) == 2
    river_sal_tax_bob = river_tallys.get(bob_text)
    river_sal_tax_tom = river_tallys.get(tom_text)

    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")

    assert river_sal_tax_bob.tax_total == 0.25
    assert river_sal_tax_tom.tax_total == 0.75


def test_world_set_river_sphere_for_agent_CorrectlyPopulatesriver_tallyTable02(
    env_dir_setup_cleanup,
):
    # GIVEN 4 agents, 100% of river flows to sal
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"

    sal = AgentUnit(_desc=sal_text)
    sal.add_allyunit(name=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_allyunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=sal)

    bob = AgentUnit(_desc=bob_text)
    bob.add_allyunit(name=elu_text, creditor_weight=1, debtor_weight=1)
    bob.add_allyunit(name=tom_text, creditor_weight=1, debtor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob)

    tom = AgentUnit(_desc=tom_text)
    tom.add_allyunit(name=elu_text, creditor_weight=1, debtor_weight=8)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom)

    elu = AgentUnit(_desc=elu_text)
    elu.add_allyunit(name=sal_text, creditor_weight=1, debtor_weight=8)
    e1.save_agentunit_obj_to_agents_dir(agent_x=elu)
    e1.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 6

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 0

    # WHEN
    e1.set_river_sphere_for_agent(agent_name=sal_text)

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 9
    with e1.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_agent_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 1

    with e1.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, sal_text)
    assert len(river_tallys) == 1
    assert river_tallys.get(bob_text) is None
    assert river_tallys.get(tom_text) is None
    river_sal_tax_elu = river_tallys.get(elu_text)

    print(f"{river_sal_tax_elu=}")
    assert river_sal_tax_elu.tax_total == 1.0


def test_world_set_river_sphere_for_agent_CorrectlyPopulatesriver_tallyTable03(
    env_dir_setup_cleanup,
):
    # GIVEN 4 agents, 85% of river flows to sal
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"

    sal_agent = AgentUnit(_desc=sal_text)
    sal_agent.add_allyunit(name=bob_text, creditor_weight=2)
    sal_agent.add_allyunit(name=tom_text, creditor_weight=7)
    sal_agent.add_allyunit(name=ava_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=sal_agent)

    bob_agent = AgentUnit(_desc=bob_text)
    bob_agent.add_allyunit(name=sal_text, creditor_weight=3)
    bob_agent.add_allyunit(name=ava_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob_agent)

    tom_agent = AgentUnit(_desc=tom_text)
    tom_agent.add_allyunit(name=sal_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom_agent)

    ava_agent = AgentUnit(_desc=ava_text)
    e1.save_agentunit_obj_to_agents_dir(agent_x=ava_agent)
    e1.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 6

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 0

    # WHEN
    e1.set_river_sphere_for_agent(agent_name=sal_text)

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 6
    with e1.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_agent_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 2

    with e1.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, sal_text)
    assert len(river_tallys) == 2
    assert river_tallys.get(bob_text) != None
    assert river_tallys.get(tom_text) != None
    assert river_tallys.get(ava_text) is None

    river_sal_tax_bob = river_tallys.get(bob_text)
    print(f"{river_sal_tax_bob=}")
    river_sal_tax_tom = river_tallys.get(tom_text)
    print(f"{river_sal_tax_tom=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert river_sal_tax_tom.tax_total == 0.7


def test_world_set_river_sphere_for_agent_CorrectlyPopulatesriver_tallyTable04(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agents, 85% of river flows to sal, left over %15 goes on endless loop
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agent = AgentUnit(_desc=sal_text)
    sal_agent.add_allyunit(name=bob_text, creditor_weight=2)
    sal_agent.add_allyunit(name=tom_text, creditor_weight=7)
    sal_agent.add_allyunit(name=ava_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=sal_agent)

    bob_agent = AgentUnit(_desc=bob_text)
    bob_agent.add_allyunit(name=sal_text, creditor_weight=3)
    bob_agent.add_allyunit(name=ava_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob_agent)

    tom_agent = AgentUnit(_desc=tom_text)
    tom_agent.add_allyunit(name=sal_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom_agent)

    ava_agent = AgentUnit(_desc=ava_text)
    ava_agent.add_allyunit(name=elu_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=ava_agent)

    elu_agent = AgentUnit(_desc=elu_text)
    elu_agent.add_allyunit(name=ava_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=elu_agent)

    e1.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 8

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 0

    # WHEN
    e1.set_river_sphere_for_agent(agent_name=sal_text)

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 40
    # with e1.get_bank_conn() as bank_conn:
    #     river_flows = get_river_flow_dict(bank_conn, currency_agent_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 2

    with e1.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, sal_text)
    assert len(river_tallys) == 2
    assert river_tallys.get(bob_text) != None
    assert river_tallys.get(tom_text) != None
    assert river_tallys.get(ava_text) is None

    river_sal_tax_bob = river_tallys.get(bob_text)
    print(f"{river_sal_tax_bob=}")
    river_sal_tax_tom = river_tallys.get(tom_text)
    print(f"{river_sal_tax_tom=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert river_sal_tax_tom.tax_total == 0.7


def test_world_set_river_sphere_for_agent_CorrectlyPopulatesriver_tallyTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agents, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agent = AgentUnit(_desc=sal_text)
    sal_agent.add_allyunit(name=bob_text, creditor_weight=2)
    sal_agent.add_allyunit(name=tom_text, creditor_weight=7)
    sal_agent.add_allyunit(name=ava_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=sal_agent)

    bob_agent = AgentUnit(_desc=bob_text)
    bob_agent.add_allyunit(name=sal_text, creditor_weight=3)
    bob_agent.add_allyunit(name=ava_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob_agent)

    tom_agent = AgentUnit(_desc=tom_text)
    tom_agent.add_allyunit(name=sal_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom_agent)

    ava_agent = AgentUnit(_desc=ava_text)
    ava_agent.add_allyunit(name=elu_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=ava_agent)

    elu_agent = AgentUnit(_desc=elu_text)
    elu_agent.add_allyunit(name=ava_text, creditor_weight=19)
    elu_agent.add_allyunit(name=sal_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=elu_agent)

    e1.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 0

    # WHEN
    e1.set_river_sphere_for_agent(agent_name=sal_text)

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 40
    # with e1.get_bank_conn() as bank_conn:
    #     river_flows = get_river_flow_dict(bank_conn, currency_agent_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 3

    with e1.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, sal_text)
    assert len(river_tallys) == 3
    assert river_tallys.get(bob_text) != None
    assert river_tallys.get(tom_text) != None
    assert river_tallys.get(elu_text) != None
    assert river_tallys.get(ava_text) is None

    river_sal_tax_bob = river_tallys.get(bob_text)
    river_sal_tax_tom = river_tallys.get(tom_text)
    river_sal_tax_elu = river_tallys.get(elu_text)
    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")
    print(f"{river_sal_tax_elu=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert round(river_sal_tax_tom.tax_total, 15) == 0.7
    # assert round(river_sal_tax_elu.tax_total, 15) == 0.048741092066406
    assert round(river_sal_tax_elu.tax_total, 15) == 0.0378017640625


def test_world_set_river_sphere_for_agent_CorrectlyDeletesPreviousRiver(
    env_dir_setup_cleanup,
):
    # GIVEN 4 agents, 100% of river flows to sal
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"

    sal = AgentUnit(_desc=sal_text)
    sal.add_allyunit(name=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_allyunit(name=tom_text, creditor_weight=3, debtor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=sal)

    bob = AgentUnit(_desc=bob_text)
    bob.add_allyunit(name=elu_text, creditor_weight=1, debtor_weight=1)
    bob.add_allyunit(name=tom_text, creditor_weight=1, debtor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob)

    tom = AgentUnit(_desc=tom_text)
    tom.add_allyunit(name=elu_text, creditor_weight=1, debtor_weight=8)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom)

    elu = AgentUnit(_desc=elu_text)
    elu.add_allyunit(name=sal_text, creditor_weight=1, debtor_weight=8)
    e1.save_agentunit_obj_to_agents_dir(agent_x=elu)
    e1.refresh_bank_metrics()

    e1.set_river_sphere_for_agent(agent_name=sal_text)
    e1.set_river_sphere_for_agent(agent_name=elu_text)

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 16

    with e1.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_agent_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 3

    # WHEN
    # sal.add_allyunit(name=elu_text, creditor_weight=1, debtor_weight=4)
    # e1.save_agentunit_obj_to_agents_dir(agent_x=sal)
    e1.set_river_sphere_for_agent(agent_name=sal_text)

    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 16
    with e1.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_agent_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 3


def test_world_set_river_sphere_for_agent_CorrectlyUsesMaxFlowsCount(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agents, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agent = AgentUnit(_desc=sal_text)
    sal_agent.add_allyunit(name=bob_text, creditor_weight=2)
    sal_agent.add_allyunit(name=tom_text, creditor_weight=7)
    sal_agent.add_allyunit(name=ava_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=sal_agent)

    bob_agent = AgentUnit(_desc=bob_text)
    bob_agent.add_allyunit(name=sal_text, creditor_weight=3)
    bob_agent.add_allyunit(name=ava_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob_agent)

    tom_agent = AgentUnit(_desc=tom_text)
    tom_agent.add_allyunit(name=sal_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom_agent)

    ava_agent = AgentUnit(_desc=ava_text)
    ava_agent.add_allyunit(name=elu_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=ava_agent)

    elu_agent = AgentUnit(_desc=elu_text)
    elu_agent.add_allyunit(name=ava_text, creditor_weight=19)
    elu_agent.add_allyunit(name=sal_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=elu_agent)

    e1.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 0

    # WHEN
    mtc = 13
    e1.set_river_sphere_for_agent(agent_name=sal_text, max_flows_count=mtc)

    # THEN
    with e1.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_agent_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == mtc


def test_world_set_river_sphere_for_agent_CorrectlyPopulatesriver_tallyTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agents, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agent = AgentUnit(_desc=sal_text)
    sal_agent.add_allyunit(name=bob_text, creditor_weight=2)
    sal_agent.add_allyunit(name=tom_text, creditor_weight=7)
    sal_agent.add_allyunit(name=ava_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=sal_agent)

    bob_agent = AgentUnit(_desc=bob_text)
    bob_agent.add_allyunit(name=sal_text, creditor_weight=3)
    bob_agent.add_allyunit(name=ava_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob_agent)

    tom_agent = AgentUnit(_desc=tom_text)
    tom_agent.add_allyunit(name=sal_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom_agent)

    ava_agent = AgentUnit(_desc=ava_text)
    ava_agent.add_allyunit(name=elu_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=ava_agent)

    elu_agent = AgentUnit(_desc=elu_text)
    elu_agent.add_allyunit(name=ava_text, creditor_weight=19)
    elu_agent.add_allyunit(name=sal_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=elu_agent)

    e1.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 0
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 0

    # WHEN
    e1.set_river_sphere_for_agent(agent_name=sal_text)

    # THEN
    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_flow) == 40
    with e1.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_agent_name=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert get_single_result_back(e1.get_bank_conn(), sqlstr_count_river_tally) == 3

    with e1.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, sal_text)
    river_tallys = e1.get_river_tallys(sal_text)
    assert len(river_tallys) == 3
    assert river_tallys.get(bob_text) != None
    assert river_tallys.get(tom_text) != None
    assert river_tallys.get(elu_text) != None
    assert river_tallys.get(ava_text) is None

    river_sal_tax_bob = river_tallys.get(bob_text)
    river_sal_tax_tom = river_tallys.get(tom_text)
    river_sal_tax_elu = river_tallys.get(elu_text)
    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")
    print(f"{river_sal_tax_elu=}")

    assert round(river_sal_tax_bob.tax_total, 15) == 0.15
    assert round(river_sal_tax_tom.tax_total, 15) == 0.7
    # assert round(river_sal_tax_elu.tax_total, 15) == 0.048741092066406
    assert round(river_sal_tax_elu.tax_total, 15) == 0.0378017640625


def test_world_set_river_sphere_for_agent_CorrectlyBuildsASingleContinuousRange(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agents, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agent = AgentUnit(_desc=sal_text)
    sal_agent.add_allyunit(name=bob_text, creditor_weight=2)
    sal_agent.add_allyunit(name=tom_text, creditor_weight=7)
    sal_agent.add_allyunit(name=ava_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=sal_agent)

    bob_agent = AgentUnit(_desc=bob_text)
    bob_agent.add_allyunit(name=sal_text, creditor_weight=3)
    bob_agent.add_allyunit(name=ava_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob_agent)

    tom_agent = AgentUnit(_desc=tom_text)
    tom_agent.add_allyunit(name=sal_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom_agent)

    ava_agent = AgentUnit(_desc=ava_text)
    ava_agent.add_allyunit(name=elu_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=ava_agent)

    elu_agent = AgentUnit(_desc=elu_text)
    elu_agent.add_allyunit(name=ava_text, creditor_weight=19)
    elu_agent.add_allyunit(name=sal_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=elu_agent)

    e1.refresh_bank_metrics()

    # WHEN
    e1.set_river_sphere_for_agent(agent_name=sal_text, max_flows_count=100)

    # THEN
    count_range_fails_sql = """
    SELECT COUNT(*)
    FROM (
        SELECT 
            rt1.currency_start current_row_start
        , lag(currency_close) OVER (ORDER BY currency_start, currency_close) AS prev_close
        , lag(currency_close) OVER (ORDER BY currency_start, currency_close) - rt1.currency_start prev_diff
        , rt1.flow_num or_flow_num
        , lag(flow_num) OVER (ORDER BY currency_start, currency_close) AS prev_flow_num
        , rt1.parent_flow_num or_parent_flow_num
        , lag(parent_flow_num) OVER (ORDER BY currency_start, currency_close) AS prev_parent_flow_num
        , river_tree_level
        , lag(river_tree_level) OVER (ORDER BY currency_start, currency_close) AS prev_parent_river_tree_level
        FROM river_flow rt1
        --  WHERE dst_name = 'sal' and currency_name = dst_name
        ORDER BY rt1.currency_start, rt1.currency_close
    ) x
    WHERE x.prev_diff <> 0
        AND ABS(x.prev_diff) < 0.0000000000000001
    ;
    
    """
    with e1.get_bank_conn() as bank_conn:
        assert get_single_result_back(bank_conn, count_range_fails_sql) == 0


def test_world_set_river_sphere_for_agent_CorrectlyUpatesAgentAllyUnits(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agents, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    world_name = get_temp_env_name()
    e1 = WorldUnit(name=world_name, worlds_dir=get_test_worlds_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agent_src = AgentUnit(_desc=sal_text)
    sal_agent_src.add_allyunit(name=bob_text, creditor_weight=2, debtor_weight=2)
    sal_agent_src.add_allyunit(name=tom_text, creditor_weight=2, debtor_weight=1)
    sal_agent_src.add_allyunit(name=ava_text, creditor_weight=2, debtor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=sal_agent_src)

    bob_agent = AgentUnit(_desc=bob_text)
    bob_agent.add_allyunit(name=sal_text, creditor_weight=3)
    bob_agent.add_allyunit(name=ava_text, creditor_weight=1)
    e1.save_agentunit_obj_to_agents_dir(agent_x=bob_agent)

    tom_agent = AgentUnit(_desc=tom_text)
    tom_agent.add_allyunit(name=sal_text)
    e1.save_agentunit_obj_to_agents_dir(agent_x=tom_agent)

    ava_agent = AgentUnit(_desc=ava_text)
    ava_agent.add_allyunit(name=elu_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=ava_agent)

    elu_agent = AgentUnit(_desc=elu_text)
    elu_agent.add_allyunit(name=ava_text, creditor_weight=8)
    elu_agent.add_allyunit(name=sal_text, creditor_weight=2)
    e1.save_agentunit_obj_to_agents_dir(agent_x=elu_agent)

    e1.refresh_bank_metrics()
    sal_agent_before = e1.get_agent_from_agents_dir(_desc=sal_text)

    e1.set_river_sphere_for_agent(agent_name=sal_text, max_flows_count=100)
    assert len(sal_agent_before._allys) == 3
    print(f"{len(sal_agent_before._allys)=}")
    bob_ally = sal_agent_before._allys.get(bob_text)
    tom_ally = sal_agent_before._allys.get(tom_text)
    ava_ally = sal_agent_before._allys.get(ava_text)
    assert bob_ally._bank_tax_paid is None
    assert bob_ally._bank_tax_diff is None
    assert tom_ally._bank_tax_paid is None
    assert tom_ally._bank_tax_diff is None
    assert ava_ally._bank_tax_paid is None
    assert ava_ally._bank_tax_diff is None

    # WHEN
    e1.set_river_sphere_for_agent(agent_name=sal_text)

    # THEN
    sal_river_tallys = e1.get_river_tallys(agent_name=sal_text)
    assert len(sal_river_tallys) == 3

    sal_agent_after = e1.get_agent_from_agents_dir(_desc=sal_text)

    bob_tally = sal_river_tallys.get(bob_text)
    tom_tally = sal_river_tallys.get(tom_text)
    elu_tally = sal_river_tallys.get(elu_text)
    assert bob_tally.tax_name == bob_text
    assert tom_tally.tax_name == tom_text
    assert elu_tally.tax_name == elu_text
    assert bob_tally.currency_name == sal_text
    assert tom_tally.currency_name == sal_text
    assert elu_tally.currency_name == sal_text

    bob_ally = sal_agent_after._allys.get(bob_text)
    tom_ally = sal_agent_after._allys.get(tom_text)
    ava_ally = sal_agent_after._allys.get(ava_text)
    elu_ally = sal_agent_after._allys.get(elu_text)

    assert bob_tally.tax_total == bob_ally._bank_tax_paid
    assert bob_tally.tax_diff == bob_ally._bank_tax_diff
    assert tom_tally.tax_total == tom_ally._bank_tax_paid
    assert tom_tally.tax_diff == tom_ally._bank_tax_diff
    assert elu_ally is None
    assert elu_tally.tax_total < 0.31 and elu_tally.tax_total > 0.3
    assert elu_tally.tax_diff is None

    # for tally_uid, sal_river_tally in sal_river_tallys.items():
    #     print(f"{tally_uid=} {sal_river_tally=}")
    #     assert sal_river_tally.currency_name == sal_text
    #     assert sal_river_tally.tax_name in [bob_text, tom_text, elu_text]
    #     allyunit_x = sal_agent_after._allys.get(sal_river_tally.tax_name)
    #     if allyunit_x != None:
    #         # print(
    #         #     f"{sal_river_tally.currency_name=} {sal_river_tally.tax_name=} {allyunit_x.name=} tax_total: {sal_river_tally.tax_total} Tax Paid: {allyunit_x._bank_tax_paid}"
    #         # )
    #         # print(
    #         #     f"{sal_river_tally.currency_name=} {sal_river_tally.tax_name=} {allyunit_x.name=} tax_diff:  {sal_river_tally.tax_diff} Tax Paid: {allyunit_x._bank_tax_diff}"
    #         # )
    #         assert sal_river_tally.tax_total == allyunit_x._bank_tax_paid
    #         assert sal_river_tally.tax_diff == allyunit_x._bank_tax_diff

    assert sal_river_tallys.get(ava_text) is None
    assert ava_ally._bank_tax_paid is None
    assert ava_ally._bank_tax_diff is None

    # for allyunit_x in sal_agent_after._allys.values():
    #     print(f"sal_agent_after {allyunit_x.name=} {allyunit_x._bank_tax_paid=}")
    #     river_tally_x = sal_river_tallys.get(allyunit_x.name)
    #     if river_tally_x is None:
    #         assert allyunit_x._bank_tax_paid is None
    #         assert allyunit_x._bank_tax_diff is None
    #     else:
    #         assert allyunit_x._bank_tax_paid != None
    #         assert allyunit_x._bank_tax_diff != None
    # assert sal_agent_after != sal_agent_before
