from lib.polity.polity import PolityUnit
from lib.agent.agent import AgentUnit
from lib.agent.ally import allyunit_shop
from lib.polity.examples.env_tools import (
    get_temp_env_name,
    get_test_politys_dir,
    env_dir_setup_cleanup,
)
from lib.polity.bank_sqlstr import (
    get_river_flow_table_insert_sqlstr as river_flow_insert,
    get_river_flow_dict,
    get_river_bucket_table_insert_sqlstr,
    get_river_bucket_dict,
    get_river_bucket_table_delete_sqlstr,
    get_river_tally_table_insert_sqlstr,
    get_river_tally_dict,
    get_ledger_table_insert_sqlstr,
    get_ledger_dict,
    LedgerUnit,
    RiverLedgerUnit,
    RiverFlowUnit,
    get_river_ledger_unit,
)


def test_polity_get_ledger_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example polity with 4 Persons, each with 3 Allyunits = 12 ledger rows
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    e1.create_dirs_if_null(in_memory_bank=True)
    e1.refresh_bank_metrics()

    bob_text = "bob"
    tim_text = "tim"
    agent_x = AgentUnit(_desc=bob_text)
    allyunit_x = allyunit_shop(
        name=tim_text,
        _agent_credit=0.9,
        _agent_debt=0.8,
        _agent_agenda_credit=0.7,
        _agent_agenda_debt=0.6,
        _agent_agenda_ratio_credit=0.5,
        _agent_agenda_ratio_debt=0.4,
        _creditor_active=True,
        _debtor_active=False,
    )

    insert_sqlstr = get_ledger_table_insert_sqlstr(
        agent_x=agent_x, allyunit_x=allyunit_x
    )
    print(insert_sqlstr)

    # WHEN
    with e1.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr)

    ledger_dict = get_ledger_dict(db_conn=e1.get_bank_conn(), payer_name=bob_text)
    ledger_x = None
    for value in ledger_dict.values():
        ledger_x = value

    # THEN
    assert ledger_x.agent_name == bob_text
    assert ledger_x.ally_name == tim_text
    assert ledger_x._agent_credit == 0.9
    assert ledger_x._agent_debt == 0.8
    assert ledger_x._agent_agenda_credit == 0.7
    assert ledger_x._agent_agenda_debt == 0.6
    assert ledger_x._agent_agenda_ratio_credit == 0.5
    assert ledger_x._agent_agenda_ratio_debt == 0.4
    assert ledger_x._creditor_active
    assert ledger_x._debtor_active == False


def test_RiverFlowUnit_exists():
    # GIVEN
    bob_text = "bob"
    tom_text = "tom"
    currency_onset = 400
    currency_cease = 600
    river_tree_level = 6
    flow_num = 89
    parent_flow_num = None

    # WHEN
    river_flow_x = RiverFlowUnit(
        currency_agent_name=bob_text,
        src_name=None,
        dst_name=tom_text,
        currency_start=currency_onset,
        currency_close=currency_cease,
        flow_num=flow_num,
        parent_flow_num=parent_flow_num,
        river_tree_level=river_tree_level,
    )

    # THEN
    assert river_flow_x.currency_agent_name == bob_text
    assert river_flow_x.src_name is None
    assert river_flow_x.dst_name == tom_text
    assert river_flow_x.currency_start == currency_onset
    assert river_flow_x.currency_close == currency_cease
    assert river_flow_x.flow_num == flow_num
    assert river_flow_x.parent_flow_num == parent_flow_num
    assert river_flow_x.river_tree_level == river_tree_level


def test_RiverFlowUnit_flow_returned_WorksCorrectly():
    # GIVEN
    bob_text = "bob"
    sal_text = "sal"
    tom_text = "tom"
    currency_onset = 400
    currency_cease = 600
    river_tree_level = 6
    flow_num = 89
    parent_flow_num = None

    # WHEN
    river_flow_x = RiverFlowUnit(
        currency_agent_name=bob_text,
        src_name=sal_text,
        dst_name=tom_text,
        currency_start=currency_onset,
        currency_close=currency_cease,
        flow_num=flow_num,
        parent_flow_num=parent_flow_num,
        river_tree_level=river_tree_level,
    )
    assert river_flow_x.currency_agent_name != river_flow_x.dst_name

    # THEN
    assert river_flow_x.flow_returned() == False

    # WHEN
    river_flow_x.dst_name = bob_text

    # THEN
    assert river_flow_x.flow_returned()


def test_get_river_ledger_unit_CorrectlyReturnsRiverLedgerUnit(env_dir_setup_cleanup):
    # GIVEN Create example polity with 4 Persons, each with 3 Allyunits = 12 ledger rows
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    e1.create_dirs_if_null(in_memory_bank=True)
    e1.refresh_bank_metrics()

    bob_text = "bob"
    sal_text = "sal"
    agent_bob = AgentUnit(_desc=bob_text)
    allyunit_sal = allyunit_shop(
        name=sal_text,
        _agent_credit=0.9,
        _agent_debt=0.8,
        _agent_agenda_credit=0.7,
        _agent_agenda_debt=0.6,
        _agent_agenda_ratio_credit=0.5,
        _agent_agenda_ratio_debt=0.4,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_sal = get_ledger_table_insert_sqlstr(
        agent_x=agent_bob, allyunit_x=allyunit_sal
    )

    tim_text = "tim"
    allyunit_tim = allyunit_shop(
        name=tim_text,
        _agent_credit=0.012,
        _agent_debt=0.017,
        _agent_agenda_credit=0.077,
        _agent_agenda_debt=0.066,
        _agent_agenda_ratio_credit=0.051,
        _agent_agenda_ratio_debt=0.049,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_tim = get_ledger_table_insert_sqlstr(
        agent_x=agent_bob, allyunit_x=allyunit_tim
    )

    with e1.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr_sal)
        bank_conn.execute(insert_sqlstr_tim)
        ledger_dict_x = get_ledger_dict(db_conn=bank_conn, payer_name=bob_text)

    # WHEN
    river_flow_x = RiverFlowUnit(
        currency_agent_name=bob_text,
        src_name=None,
        dst_name=bob_text,
        currency_start=0.225,
        currency_close=0.387,
        flow_num=51,
        parent_flow_num=6,
        river_tree_level=4,
    )
    with e1.get_bank_conn() as bank_conn:
        river_ledger_x = get_river_ledger_unit(bank_conn, river_flow_x)

    # THEN
    assert river_ledger_x.agent_name == bob_text
    assert river_ledger_x.currency_onset == 0.225
    assert river_ledger_x.currency_cease == 0.387
    assert river_ledger_x.river_tree_level == 4
    assert river_ledger_x._ledgers == ledger_dict_x
    assert river_ledger_x.flow_num == 51


def test_river_flow_insert_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example polity with 4 Persons, each with 3 Allyunits = 12 ledger rows
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tim_text = "tim"
    sal_text = "sal"

    river_flow_unit = RiverFlowUnit(
        currency_agent_name=bob_text,
        src_name=tim_text,
        dst_name=sal_text,
        currency_start=0.2,
        currency_close=0.5,
        flow_num=5,
        river_tree_level=6,
        parent_flow_num=8,
    )
    insert_sqlstr = river_flow_insert(river_flow_unit)
    print(insert_sqlstr)

    # WHEN
    with e1.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr)
        river_flows = get_river_flow_dict(bank_conn, currency_agent_name=bob_text)
        print(f"{river_flows=}")

    # THEN
    for value in river_flows.values():
        assert value.currency_agent_name == bob_text
        assert value.src_name == tim_text
        assert value.dst_name == sal_text
        assert value.currency_start == 0.2
        assert value.currency_close == 0.5
        assert value.flow_num == 5
        assert value.river_tree_level == 6
        assert value.parent_flow_num == 8


def test_RiverLedgerUnit_Exists():
    # GIVEN
    bob_text = "bob"
    sal_text = "sal"
    tom_text = "tom"
    ledger_unit_01 = LedgerUnit(
        agent_name=bob_text,
        ally_name=sal_text,
        _agent_credit=0.66,
        _agent_debt=0.2,
        _agent_agenda_credit=0.4,
        _agent_agenda_debt=0.15,
        _agent_agenda_ratio_credit=0.5,
        _agent_agenda_ratio_debt=0.12,
        _creditor_active=True,
        _debtor_active=True,
    )
    ledger_unit_02 = LedgerUnit(
        agent_name=bob_text,
        ally_name=tom_text,
        _agent_credit=0.05,
        _agent_debt=0.09,
        _agent_agenda_credit=0.055,
        _agent_agenda_debt=0.0715,
        _agent_agenda_ratio_credit=0.00995,
        _agent_agenda_ratio_debt=0.00012,
        _creditor_active=True,
        _debtor_active=True,
    )
    ledger_dict = {
        ledger_unit_01.ally_name: ledger_unit_01,
        ledger_unit_02.ally_name: ledger_unit_02,
    }

    # WHEN
    river_ledger_unit = RiverLedgerUnit(
        agent_name=bob_text,
        currency_onset=0.6,
        currency_cease=0.8,
        _ledgers=ledger_dict,
        river_tree_level=7,
        flow_num=89,
    )

    # THEN
    assert river_ledger_unit.agent_name == bob_text
    assert river_ledger_unit.currency_onset == 0.6
    assert river_ledger_unit.currency_cease == 0.8
    assert river_ledger_unit.river_tree_level == 7
    assert river_ledger_unit.flow_num == 89
    assert river_ledger_unit._ledgers == ledger_dict
    assert abs(river_ledger_unit.get_range() - 0.2) < 0.00000001


def test_get_river_tally_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example polity with 4 Persons, each with 3 Allyunits = 12 ledger rows
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
    e1.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"

    agent_bob = AgentUnit(_desc=bob_text)
    allyunit_tom = allyunit_shop(
        name=tom_text,
        _agent_credit=0.9,
        _agent_debt=0.8,
        _agent_agenda_credit=0.7,
        _agent_agenda_debt=0.6,
        _agent_agenda_ratio_credit=0.5,
        _agent_agenda_ratio_debt=0.411,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_tom = get_ledger_table_insert_sqlstr(
        agent_x=agent_bob, allyunit_x=allyunit_tom
    )
    allyunit_sal = allyunit_shop(
        name=sal_text,
        _agent_credit=0.9,
        _agent_debt=0.8,
        _agent_agenda_credit=0.7,
        _agent_agenda_debt=0.6,
        _agent_agenda_ratio_credit=0.5,
        _agent_agenda_ratio_debt=0.455,
        _creditor_active=True,
        _debtor_active=False,
    )
    insert_sqlstr_sal = get_ledger_table_insert_sqlstr(
        agent_x=agent_bob, allyunit_x=allyunit_sal
    )

    river_flow_1 = RiverFlowUnit(bob_text, bob_text, tom_text, 0.0, 0.2, 0, None, 1)
    river_flow_2 = RiverFlowUnit(bob_text, bob_text, sal_text, 0.2, 1.0, 0, None, 1)
    river_flow_3 = RiverFlowUnit(bob_text, tom_text, bob_text, 0.0, 0.2, 1, 0, 2)
    river_flow_4 = RiverFlowUnit(bob_text, sal_text, bob_text, 0.2, 1.0, 1, 0, 2)
    sb0 = river_flow_insert(river_flow_1)
    sb1 = river_flow_insert(river_flow_2)
    st0 = river_flow_insert(river_flow_3)
    ss0 = river_flow_insert(river_flow_4)

    with e1.get_bank_conn() as bank_conn:
        bank_conn.execute(insert_sqlstr_tom)
        bank_conn.execute(insert_sqlstr_sal)
        bank_conn.execute(sb0)
        bank_conn.execute(sb1)
        bank_conn.execute(st0)
        bank_conn.execute(ss0)

    # WHEN
    mstr_sqlstr = get_river_tally_table_insert_sqlstr(currency_agent_name=bob_text)
    with e1.get_bank_conn() as bank_conn:
        print(mstr_sqlstr)
        bank_conn.execute(mstr_sqlstr)

    # THEN
    with e1.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, currency_agent_name=bob_text)
        print(f"{river_tallys=}")

    assert len(river_tallys) == 2

    for value in river_tallys.values():
        assert value.currency_name == bob_text
        assert value.tax_name in [tom_text, sal_text]
        assert value.tax_total in [0.2, 0.8]
        assert value.debt in [0.411, 0.455]
        assert round(value.tax_diff, 15) in [0.211, -0.345]


def test_get_river_bucket_table_delete_sqlstr_CorrectlyDeletesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example polity with 4 Persons, each with 3 Allyunits = 12 ledger rows
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
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

    e1.refresh_bank_metrics()
    e1.set_river_sphere_for_agent(agent_name=sal_text)

    with e1.get_bank_conn() as bank_conn:
        assert len(get_river_bucket_dict(bank_conn, sal_text)) > 0

    # WHEN
    sqlstr = get_river_bucket_table_delete_sqlstr(sal_text)
    with e1.get_bank_conn() as bank_conn:
        bank_conn.execute(sqlstr)

    # THEN
    with e1.get_bank_conn() as bank_conn:
        assert len(get_river_bucket_dict(bank_conn, sal_text)) == 0


def test_get_river_bucket_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example polity with 4 Persons, each with 3 Allyunits = 12 ledger rows
    polity_name = get_temp_env_name()
    e1 = PolityUnit(name=polity_name, politys_dir=get_test_politys_dir())
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
    e1.set_river_sphere_for_agent(agent_name=sal_text, max_flows_count=100)
    with e1.get_bank_conn() as bank_conn:
        bank_conn.execute(get_river_bucket_table_delete_sqlstr(sal_text))
        assert len(get_river_bucket_dict(bank_conn, currency_agent_name=sal_text)) == 0

    # WHEN / THEN
    mstr_sqlstr = get_river_bucket_table_insert_sqlstr(currency_agent_name=sal_text)
    with e1.get_bank_conn() as bank_conn:
        print(mstr_sqlstr)
        bank_conn.execute(mstr_sqlstr)
        # river_flows = get_river_flow_dict(bank_conn, currency_agent_name=sal_text)
        # for river_flow in river_flows.values():
        #     print(f"{river_flow=}")

    # THEN
    with e1.get_bank_conn() as bank_conn:
        river_buckets = get_river_bucket_dict(bank_conn, currency_agent_name=sal_text)
        for river_bucket in river_buckets.values():
            print(f"huh {river_bucket=}")

    assert len(river_buckets) == 2

    for value in river_buckets.values():
        assert value.currency_name == sal_text
        assert value.dst_name == sal_text
        assert value.bucket_num in [0, 1]
        assert value.curr_start in [0.12316456150798766, 0.04401266686517654]
        assert value.curr_close in [0.1, 1.0]
