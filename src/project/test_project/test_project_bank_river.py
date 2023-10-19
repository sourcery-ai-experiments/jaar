from src.deal.deal import dealunit_shop
from src.project.project import projectunit_shop
from src.project.examples.project_env_kit import (
    get_temp_env_handle,
    get_test_projects_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from src.project.y_func import check_connection, get_single_result_back
from src.project.bank_sqlstr import (
    get_river_tally_dict,
    get_river_flow_dict,
    get_table_count_sqlstr,
)


def test_project_set_river_sphere_for_deal_CorrectlyPopulatesriver_tallyTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example project with 4 Healers, each with 3 Partyunits = 12 ledger rows
    project_handle = get_temp_env_handle()
    x_project = projectunit_shop(
        handle=project_handle, projects_dir=get_test_projects_dir()
    )
    x_project.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"

    sal = dealunit_shop(_healer=sal_text)
    sal.add_partyunit(title=bob_text, creditor_weight=1)
    sal.add_partyunit(title=tom_text, creditor_weight=3)
    x_project.save_public_deal(x_deal=sal)

    bob = dealunit_shop(_healer=bob_text)
    bob.add_partyunit(title=sal_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=bob)

    tom = dealunit_shop(_healer=tom_text)
    tom.add_partyunit(title=sal_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=tom)

    x_project.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_project.get_bank_conn(), sqlstr_count_ledger) == 4

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 0
    )
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    x_project.set_river_sphere_for_deal(deal_healer=sal_text)

    # THEN
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 4
    )
    with x_project.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_deal_healer=sal_text)

    flow_0 = river_flows.get(0)
    flow_1 = river_flows.get(1)
    assert flow_1.src_healer == "sal" and flow_1.dst_healer == "tom"
    assert flow_1.river_tree_level == 1
    assert flow_1.currency_start == 0.25
    assert flow_1.currency_close == 1
    assert flow_1.parent_flow_num is None
    flow_2 = river_flows.get(2)
    flow_3 = river_flows.get(3)
    assert flow_3.src_healer == "tom" and flow_3.dst_healer == "sal"
    assert flow_3.river_tree_level == 2
    assert flow_3.parent_flow_num == 1

    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 2
    )

    with x_project.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, sal_text)
    assert len(river_tallys) == 2
    river_sal_tax_bob = river_tallys.get(bob_text)
    river_sal_tax_tom = river_tallys.get(tom_text)

    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")

    assert river_sal_tax_bob.tax_total == 0.25
    assert river_sal_tax_tom.tax_total == 0.75


def test_project_set_river_sphere_for_deal_CorrectlyPopulatesriver_tallyTable02(
    env_dir_setup_cleanup,
):
    # GIVEN 4 deals, 100% of river flows to sal
    project_handle = get_temp_env_handle()
    x_project = projectunit_shop(
        handle=project_handle, projects_dir=get_test_projects_dir()
    )
    x_project.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"

    sal = dealunit_shop(_healer=sal_text)
    sal.add_partyunit(title=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    x_project.save_public_deal(x_deal=sal)

    bob = dealunit_shop(_healer=bob_text)
    bob.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=1)
    bob.add_partyunit(title=tom_text, creditor_weight=1, debtor_weight=1)
    x_project.save_public_deal(x_deal=bob)

    tom = dealunit_shop(_healer=tom_text)
    tom.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=8)
    x_project.save_public_deal(x_deal=tom)

    elu = dealunit_shop(_healer=elu_text)
    elu.add_partyunit(title=sal_text, creditor_weight=1, debtor_weight=8)
    x_project.save_public_deal(x_deal=elu)
    x_project.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_project.get_bank_conn(), sqlstr_count_ledger) == 6

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 0
    )
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    x_project.set_river_sphere_for_deal(deal_healer=sal_text)

    # THEN
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 9
    )
    with x_project.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_deal_healer=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 1
    )

    with x_project.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, sal_text)
    assert len(river_tallys) == 1
    assert river_tallys.get(bob_text) is None
    assert river_tallys.get(tom_text) is None
    river_sal_tax_elu = river_tallys.get(elu_text)

    print(f"{river_sal_tax_elu=}")
    assert river_sal_tax_elu.tax_total == 1.0


def test_project_set_river_sphere_for_deal_CorrectlyPopulatesriver_tallyTable03(
    env_dir_setup_cleanup,
):
    # GIVEN 4 deals, 85% of river flows to sal
    project_handle = get_temp_env_handle()
    x_project = projectunit_shop(
        handle=project_handle, projects_dir=get_test_projects_dir()
    )
    x_project.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"

    sal_deal = dealunit_shop(_healer=sal_text)
    sal_deal.add_partyunit(title=bob_text, creditor_weight=2)
    sal_deal.add_partyunit(title=tom_text, creditor_weight=7)
    sal_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=sal_deal)

    bob_deal = dealunit_shop(_healer=bob_text)
    bob_deal.add_partyunit(title=sal_text, creditor_weight=3)
    bob_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=bob_deal)

    tom_deal = dealunit_shop(_healer=tom_text)
    tom_deal.add_partyunit(title=sal_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=tom_deal)

    ava_deal = dealunit_shop(_healer=ava_text)
    x_project.save_public_deal(x_deal=ava_deal)
    x_project.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_project.get_bank_conn(), sqlstr_count_ledger) == 6

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 0
    )
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    x_project.set_river_sphere_for_deal(deal_healer=sal_text)

    # THEN
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 6
    )
    with x_project.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_deal_healer=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 2
    )

    with x_project.get_bank_conn() as bank_conn:
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


def test_project_set_river_sphere_for_deal_CorrectlyPopulatesriver_tallyTable04(
    env_dir_setup_cleanup,
):
    # GIVEN 5 deals, 85% of river flows to sal, left over %15 goes on endless loop
    project_handle = get_temp_env_handle()
    x_project = projectunit_shop(
        handle=project_handle, projects_dir=get_test_projects_dir()
    )
    x_project.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_deal = dealunit_shop(_healer=sal_text)
    sal_deal.add_partyunit(title=bob_text, creditor_weight=2)
    sal_deal.add_partyunit(title=tom_text, creditor_weight=7)
    sal_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=sal_deal)

    bob_deal = dealunit_shop(_healer=bob_text)
    bob_deal.add_partyunit(title=sal_text, creditor_weight=3)
    bob_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=bob_deal)

    tom_deal = dealunit_shop(_healer=tom_text)
    tom_deal.add_partyunit(title=sal_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=tom_deal)

    ava_deal = dealunit_shop(_healer=ava_text)
    ava_deal.add_partyunit(title=elu_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=ava_deal)

    elu_deal = dealunit_shop(_healer=elu_text)
    elu_deal.add_partyunit(title=ava_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=elu_deal)

    x_project.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_project.get_bank_conn(), sqlstr_count_ledger) == 8

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 0
    )
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    x_project.set_river_sphere_for_deal(deal_healer=sal_text)

    # THEN
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 40
    )
    # with x_project.get_bank_conn() as bank_conn:
    #     river_flows = get_river_flow_dict(bank_conn, currency_deal_healer=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 2
    )

    with x_project.get_bank_conn() as bank_conn:
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


def test_project_set_river_sphere_for_deal_CorrectlyPopulatesriver_tallyTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 deals, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    project_handle = get_temp_env_handle()
    x_project = projectunit_shop(
        handle=project_handle, projects_dir=get_test_projects_dir()
    )
    x_project.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_deal = dealunit_shop(_healer=sal_text)
    sal_deal.add_partyunit(title=bob_text, creditor_weight=2)
    sal_deal.add_partyunit(title=tom_text, creditor_weight=7)
    sal_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=sal_deal)

    bob_deal = dealunit_shop(_healer=bob_text)
    bob_deal.add_partyunit(title=sal_text, creditor_weight=3)
    bob_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=bob_deal)

    tom_deal = dealunit_shop(_healer=tom_text)
    tom_deal.add_partyunit(title=sal_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=tom_deal)

    ava_deal = dealunit_shop(_healer=ava_text)
    ava_deal.add_partyunit(title=elu_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=ava_deal)

    elu_deal = dealunit_shop(_healer=elu_text)
    elu_deal.add_partyunit(title=ava_text, creditor_weight=19)
    elu_deal.add_partyunit(title=sal_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=elu_deal)

    x_project.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_project.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 0
    )
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    x_project.set_river_sphere_for_deal(deal_healer=sal_text)

    # THEN
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 40
    )
    # with x_project.get_bank_conn() as bank_conn:
    #     river_flows = get_river_flow_dict(bank_conn, currency_deal_healer=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 3
    )

    with x_project.get_bank_conn() as bank_conn:
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


def test_project_set_river_sphere_for_deal_CorrectlyDeletesPreviousRiver(
    env_dir_setup_cleanup,
):
    # GIVEN 4 deals, 100% of river flows to sal
    project_handle = get_temp_env_handle()
    x_project = projectunit_shop(
        handle=project_handle, projects_dir=get_test_projects_dir()
    )
    x_project.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"

    sal = dealunit_shop(_healer=sal_text)
    sal.add_partyunit(title=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    x_project.save_public_deal(x_deal=sal)

    bob = dealunit_shop(_healer=bob_text)
    bob.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=1)
    bob.add_partyunit(title=tom_text, creditor_weight=1, debtor_weight=1)
    x_project.save_public_deal(x_deal=bob)

    tom = dealunit_shop(_healer=tom_text)
    tom.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=8)
    x_project.save_public_deal(x_deal=tom)

    elu = dealunit_shop(_healer=elu_text)
    elu.add_partyunit(title=sal_text, creditor_weight=1, debtor_weight=8)
    x_project.save_public_deal(x_deal=elu)
    x_project.refresh_bank_metrics()

    x_project.set_river_sphere_for_deal(deal_healer=sal_text)
    x_project.set_river_sphere_for_deal(deal_healer=elu_text)

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 16
    )

    with x_project.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_deal_healer=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 3
    )

    # WHEN
    # sal.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=4)
    # x_project.save_public_deal(x_deal=sal)
    x_project.set_river_sphere_for_deal(deal_healer=sal_text)

    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 16
    )
    with x_project.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_deal_healer=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 3
    )


def test_project_set_river_sphere_for_deal_CorrectlyUsesMaxFlowsCount(
    env_dir_setup_cleanup,
):
    # GIVEN 5 deals, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    project_handle = get_temp_env_handle()
    x_project = projectunit_shop(
        handle=project_handle, projects_dir=get_test_projects_dir()
    )
    x_project.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_deal = dealunit_shop(_healer=sal_text)
    sal_deal.add_partyunit(title=bob_text, creditor_weight=2)
    sal_deal.add_partyunit(title=tom_text, creditor_weight=7)
    sal_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=sal_deal)

    bob_deal = dealunit_shop(_healer=bob_text)
    bob_deal.add_partyunit(title=sal_text, creditor_weight=3)
    bob_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=bob_deal)

    tom_deal = dealunit_shop(_healer=tom_text)
    tom_deal.add_partyunit(title=sal_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=tom_deal)

    ava_deal = dealunit_shop(_healer=ava_text)
    ava_deal.add_partyunit(title=elu_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=ava_deal)

    elu_deal = dealunit_shop(_healer=elu_text)
    elu_deal.add_partyunit(title=ava_text, creditor_weight=19)
    elu_deal.add_partyunit(title=sal_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=elu_deal)

    x_project.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_project.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 0
    )
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    mtc = 13
    x_project.set_river_sphere_for_deal(deal_healer=sal_text, max_flows_count=mtc)

    # THEN
    with x_project.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_deal_healer=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow)
        == mtc
    )


def test_project_set_river_sphere_for_deal_CorrectlyPopulatesriver_tallyTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 deals, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    project_handle = get_temp_env_handle()
    x_project = projectunit_shop(
        handle=project_handle, projects_dir=get_test_projects_dir()
    )
    x_project.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_deal = dealunit_shop(_healer=sal_text)
    sal_deal.add_partyunit(title=bob_text, creditor_weight=2)
    sal_deal.add_partyunit(title=tom_text, creditor_weight=7)
    sal_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=sal_deal)

    bob_deal = dealunit_shop(_healer=bob_text)
    bob_deal.add_partyunit(title=sal_text, creditor_weight=3)
    bob_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=bob_deal)

    tom_deal = dealunit_shop(_healer=tom_text)
    tom_deal.add_partyunit(title=sal_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=tom_deal)

    ava_deal = dealunit_shop(_healer=ava_text)
    ava_deal.add_partyunit(title=elu_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=ava_deal)

    elu_deal = dealunit_shop(_healer=elu_text)
    elu_deal.add_partyunit(title=ava_text, creditor_weight=19)
    elu_deal.add_partyunit(title=sal_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=elu_deal)

    x_project.refresh_bank_metrics()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_project.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_flow = get_table_count_sqlstr("river_flow")
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 0
    )
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    x_project.set_river_sphere_for_deal(deal_healer=sal_text)

    # THEN
    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_flow) == 40
    )
    with x_project.get_bank_conn() as bank_conn:
        river_flows = get_river_flow_dict(bank_conn, currency_deal_healer=sal_text)
    # for river_flow in river_flows.values():
    #     print(f"{river_flow=}")

    assert (
        get_single_result_back(x_project.get_bank_conn(), sqlstr_count_river_tally) == 3
    )

    with x_project.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, sal_text)
    river_tallys = x_project.get_river_tallys(sal_text)
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


def test_project_set_river_sphere_for_deal_CorrectlyBuildsASingleContinuousRange(
    env_dir_setup_cleanup,
):
    # GIVEN 5 deals, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    project_handle = get_temp_env_handle()
    x_project = projectunit_shop(
        handle=project_handle, projects_dir=get_test_projects_dir()
    )
    x_project.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_deal = dealunit_shop(_healer=sal_text)
    sal_deal.add_partyunit(title=bob_text, creditor_weight=2)
    sal_deal.add_partyunit(title=tom_text, creditor_weight=7)
    sal_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=sal_deal)

    bob_deal = dealunit_shop(_healer=bob_text)
    bob_deal.add_partyunit(title=sal_text, creditor_weight=3)
    bob_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=bob_deal)

    tom_deal = dealunit_shop(_healer=tom_text)
    tom_deal.add_partyunit(title=sal_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=tom_deal)

    ava_deal = dealunit_shop(_healer=ava_text)
    ava_deal.add_partyunit(title=elu_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=ava_deal)

    elu_deal = dealunit_shop(_healer=elu_text)
    elu_deal.add_partyunit(title=ava_text, creditor_weight=19)
    elu_deal.add_partyunit(title=sal_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=elu_deal)

    x_project.refresh_bank_metrics()

    # WHEN
    x_project.set_river_sphere_for_deal(deal_healer=sal_text, max_flows_count=100)

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
        --  WHERE dst_healer = 'sal' and currency_healer = dst_healer
        ORDER BY rt1.currency_start, rt1.currency_close
    ) x
    WHERE x.prev_diff <> 0
        AND ABS(x.prev_diff) < 0.0000000000000001
    ;
    
    """
    with x_project.get_bank_conn() as bank_conn:
        assert get_single_result_back(bank_conn, count_range_fails_sql) == 0


def test_project_set_river_sphere_for_deal_CorrectlyUpatesDealPartyUnits(
    env_dir_setup_cleanup,
):
    # GIVEN 5 deals, 85% of river flows to sal, left over %15 goes on endless loop that slowly bleeds to sal
    project_handle = get_temp_env_handle()
    x_project = projectunit_shop(
        handle=project_handle, projects_dir=get_test_projects_dir()
    )
    x_project.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_deal_src = dealunit_shop(_healer=sal_text)
    sal_deal_src.add_partyunit(title=bob_text, creditor_weight=2, debtor_weight=2)
    sal_deal_src.add_partyunit(title=tom_text, creditor_weight=2, debtor_weight=1)
    sal_deal_src.add_partyunit(title=ava_text, creditor_weight=2, debtor_weight=2)
    x_project.save_public_deal(x_deal=sal_deal_src)

    bob_deal = dealunit_shop(_healer=bob_text)
    bob_deal.add_partyunit(title=sal_text, creditor_weight=3)
    bob_deal.add_partyunit(title=ava_text, creditor_weight=1)
    x_project.save_public_deal(x_deal=bob_deal)

    tom_deal = dealunit_shop(_healer=tom_text)
    tom_deal.add_partyunit(title=sal_text)
    x_project.save_public_deal(x_deal=tom_deal)

    ava_deal = dealunit_shop(_healer=ava_text)
    ava_deal.add_partyunit(title=elu_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=ava_deal)

    elu_deal = dealunit_shop(_healer=elu_text)
    elu_deal.add_partyunit(title=ava_text, creditor_weight=8)
    elu_deal.add_partyunit(title=sal_text, creditor_weight=2)
    x_project.save_public_deal(x_deal=elu_deal)

    x_project.refresh_bank_metrics()
    sal_deal_before = x_project.get_public_deal(healer=sal_text)

    x_project.set_river_sphere_for_deal(deal_healer=sal_text, max_flows_count=100)
    assert len(sal_deal_before._partys) == 3
    print(f"{len(sal_deal_before._partys)=}")
    bob_party = sal_deal_before._partys.get(bob_text)
    tom_party = sal_deal_before._partys.get(tom_text)
    ava_party = sal_deal_before._partys.get(ava_text)
    assert bob_party._bank_tax_paid is None
    assert bob_party._bank_tax_diff is None
    assert tom_party._bank_tax_paid is None
    assert tom_party._bank_tax_diff is None
    assert ava_party._bank_tax_paid is None
    assert ava_party._bank_tax_diff is None

    # WHEN
    x_project.set_river_sphere_for_deal(deal_healer=sal_text)

    # THEN
    sal_river_tallys = x_project.get_river_tallys(deal_healer=sal_text)
    assert len(sal_river_tallys) == 3

    sal_deal_after = x_project.get_public_deal(healer=sal_text)

    bob_tally = sal_river_tallys.get(bob_text)
    tom_tally = sal_river_tallys.get(tom_text)
    elu_tally = sal_river_tallys.get(elu_text)
    assert bob_tally.tax_healer == bob_text
    assert tom_tally.tax_healer == tom_text
    assert elu_tally.tax_healer == elu_text
    assert bob_tally.currency_healer == sal_text
    assert tom_tally.currency_healer == sal_text
    assert elu_tally.currency_healer == sal_text

    bob_party = sal_deal_after._partys.get(bob_text)
    tom_party = sal_deal_after._partys.get(tom_text)
    ava_party = sal_deal_after._partys.get(ava_text)
    elu_party = sal_deal_after._partys.get(elu_text)

    assert bob_tally.tax_total == bob_party._bank_tax_paid
    assert bob_tally.tax_diff == bob_party._bank_tax_diff
    assert tom_tally.tax_total == tom_party._bank_tax_paid
    assert tom_tally.tax_diff == tom_party._bank_tax_diff
    assert elu_party is None
    assert elu_tally.tax_total < 0.31 and elu_tally.tax_total > 0.3
    assert elu_tally.tax_diff is None

    # for tally_uid, sal_river_tally in sal_river_tallys.items():
    #     print(f"{tally_uid=} {sal_river_tally=}")
    #     assert sal_river_tally.currency_healer == sal_text
    #     assert sal_river_tally.tax_healer in [bob_text, tom_text, elu_text]
    #     partyunit_x = sal_deal_after._partys.get(sal_river_tally.tax_healer)
    #     if partyunit_x != None:
    #         # print(
    #         #     f"{sal_river_tally.currency_healer=} {sal_river_tally.tax_healer=} {partyunit_x.title=} tax_total: {sal_river_tally.tax_total} Tax Paid: {partyunit_x._bank_tax_paid}"
    #         # )
    #         # print(
    #         #     f"{sal_river_tally.currency_healer=} {sal_river_tally.tax_healer=} {partyunit_x.title=} tax_diff:  {sal_river_tally.tax_diff} Tax Paid: {partyunit_x._bank_tax_diff}"
    #         # )
    #         assert sal_river_tally.tax_total == partyunit_x._bank_tax_paid
    #         assert sal_river_tally.tax_diff == partyunit_x._bank_tax_diff

    assert sal_river_tallys.get(ava_text) is None
    assert ava_party._bank_tax_paid is None
    assert ava_party._bank_tax_diff is None

    # for partyunit_x in sal_deal_after._partys.values():
    #     print(f"sal_deal_after {partyunit_x.title=} {partyunit_x._bank_tax_paid=}")
    #     river_tally_x = sal_river_tallys.get(partyunit_x.title)
    #     if river_tally_x is None:
    #         assert partyunit_x._bank_tax_paid is None
    #         assert partyunit_x._bank_tax_diff is None
    #     else:
    #         assert partyunit_x._bank_tax_paid != None
    #         assert partyunit_x._bank_tax_diff != None
    # assert sal_deal_after != sal_deal_before
