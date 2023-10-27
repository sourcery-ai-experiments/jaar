from src.agenda.agenda import agendaunit_shop
from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_handle,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from src.culture.y_func import check_connection, get_single_result_back
from src.culture.bank_sqlstr import (
    get_river_tally_dict,
    get_river_block_dict,
    get_table_count_sqlstr,
)


def test_culture_set_credit_flow_for_agenda_CorrectlyPopulatesriver_tallyTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"

    sal = agendaunit_shop(_healer=sal_text)
    sal.add_partyunit(title=bob_text, creditor_weight=1)
    sal.add_partyunit(title=tom_text, creditor_weight=3)
    x_culture.save_public_agenda(x_agenda=sal)

    bob = agendaunit_shop(_healer=bob_text)
    bob.add_partyunit(title=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob)

    tom = agendaunit_shop(_healer=tom_text)
    tom.add_partyunit(title=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=tom)

    x_culture.refresh_bank_public_agendas_data()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_ledger) == 4

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_block = get_table_count_sqlstr("river_block")
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block) == 0
    )
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block) == 4
    )
    with x_culture.get_bank_conn() as bank_conn:
        river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)

    block_0 = river_blocks.get(0)
    block_1 = river_blocks.get(1)
    assert block_1.src_healer == "sal" and block_1.dst_healer == "tom"
    assert block_1.river_tree_level == 1
    assert block_1.currency_start == 0.25
    assert block_1.currency_close == 1
    assert block_1.parent_block_num is None
    block_2 = river_blocks.get(2)
    block_3 = river_blocks.get(3)
    assert block_3.src_healer == "tom" and block_3.dst_healer == "sal"
    assert block_3.river_tree_level == 2
    assert block_3.parent_block_num == 1

    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 2
    )

    with x_culture.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, sal_text)
    assert len(river_tallys) == 2
    river_sal_tax_bob = river_tallys.get(bob_text)
    river_sal_tax_tom = river_tallys.get(tom_text)

    print(f"{river_sal_tax_bob=}")
    print(f"{river_sal_tax_tom=}")

    assert river_sal_tax_bob.tax_total == 0.25
    assert river_sal_tax_tom.tax_total == 0.75


def test_culture_set_credit_flow_for_agenda_CorrectlyPopulatesriver_tallyTable02(
    env_dir_setup_cleanup,
):
    # GIVEN 4 agendas, 100% of river blocks to sal
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"

    sal = agendaunit_shop(_healer=sal_text)
    sal.add_partyunit(title=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal)

    bob = agendaunit_shop(_healer=bob_text)
    bob.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=1)
    bob.add_partyunit(title=tom_text, creditor_weight=1, debtor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob)

    tom = agendaunit_shop(_healer=tom_text)
    tom.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=8)
    x_culture.save_public_agenda(x_agenda=tom)

    elu = agendaunit_shop(_healer=elu_text)
    elu.add_partyunit(title=sal_text, creditor_weight=1, debtor_weight=8)
    x_culture.save_public_agenda(x_agenda=elu)
    x_culture.refresh_bank_public_agendas_data()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_ledger) == 6

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_block = get_table_count_sqlstr("river_block")
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block) == 0
    )
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block) == 9
    )
    with x_culture.get_bank_conn() as bank_conn:
        river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 1
    )

    with x_culture.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, sal_text)
    assert len(river_tallys) == 1
    assert river_tallys.get(bob_text) is None
    assert river_tallys.get(tom_text) is None
    river_sal_tax_elu = river_tallys.get(elu_text)

    print(f"{river_sal_tax_elu=}")
    assert river_sal_tax_elu.tax_total == 1.0


def test_culture_set_credit_flow_for_agenda_CorrectlyPopulatesriver_tallyTable03(
    env_dir_setup_cleanup,
):
    # GIVEN 4 agendas, 85% of river blocks to sal
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(title=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(title=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(title=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(title=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    x_culture.save_public_agenda(x_agenda=ava_agenda)
    x_culture.refresh_bank_public_agendas_data()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_ledger) == 6

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_block = get_table_count_sqlstr("river_block")
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block) == 0
    )
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block) == 6
    )
    with x_culture.get_bank_conn() as bank_conn:
        river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 2
    )

    with x_culture.get_bank_conn() as bank_conn:
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


def test_culture_set_credit_flow_for_agenda_CorrectlyPopulatesriver_tallyTable04(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(title=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(title=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(title=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(title=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(title=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(title=ava_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=elu_agenda)

    x_culture.refresh_bank_public_agendas_data()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_ledger) == 8

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_block = get_table_count_sqlstr("river_block")
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block) == 0
    )
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block)
        == 40
    )
    # with x_culture.get_bank_conn() as bank_conn:
    #     river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 2
    )

    with x_culture.get_bank_conn() as bank_conn:
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


def test_culture_set_credit_flow_for_agenda_CorrectlyPopulatesriver_tallyTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(title=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(title=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(title=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(title=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(title=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(title=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(title=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=elu_agenda)

    x_culture.refresh_bank_public_agendas_data()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_block = get_table_count_sqlstr("river_block")
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block) == 0
    )
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block)
        == 40
    )
    # with x_culture.get_bank_conn() as bank_conn:
    #     river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 3
    )

    with x_culture.get_bank_conn() as bank_conn:
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


def test_culture_set_credit_flow_for_agenda_CorrectlyDeletesPreviousRiver(
    env_dir_setup_cleanup,
):
    # GIVEN 4 agendas, 100% of river blocks to sal
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"

    sal = agendaunit_shop(_healer=sal_text)
    sal.add_partyunit(title=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal)

    bob = agendaunit_shop(_healer=bob_text)
    bob.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=1)
    bob.add_partyunit(title=tom_text, creditor_weight=1, debtor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob)

    tom = agendaunit_shop(_healer=tom_text)
    tom.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=8)
    x_culture.save_public_agenda(x_agenda=tom)

    elu = agendaunit_shop(_healer=elu_text)
    elu.add_partyunit(title=sal_text, creditor_weight=1, debtor_weight=8)
    x_culture.save_public_agenda(x_agenda=elu)
    x_culture.refresh_bank_public_agendas_data()

    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)
    x_culture.set_credit_flow_for_agenda(agenda_healer=elu_text)

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_block = get_table_count_sqlstr("river_block")
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block)
        == 16
    )

    with x_culture.get_bank_conn() as bank_conn:
        river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 3
    )

    # WHEN
    # sal.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=4)
    # x_culture.save_public_agenda(x_agenda=sal)
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block)
        == 16
    )
    with x_culture.get_bank_conn() as bank_conn:
        river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 3
    )


def test_culture_set_credit_flow_for_agenda_CorrectlyUsesMaxblocksCount(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(title=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(title=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(title=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(title=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(title=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(title=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(title=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=elu_agenda)

    x_culture.refresh_bank_public_agendas_data()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_block = get_table_count_sqlstr("river_block")
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block) == 0
    )
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    mbc = 13
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text, max_blocks_count=mbc)

    # THEN
    # with x_culture.get_bank_conn() as bank_conn:
    #     river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block)
        == mbc
    )


def test_culture_set_credit_flow_for_agenda_CorrectlyPopulatesriver_tallyTable05(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(title=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(title=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(title=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(title=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(title=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(title=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(title=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=elu_agenda)

    x_culture.refresh_bank_public_agendas_data()

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_ledger) == 9

    sqlstr_count_river_tally = get_table_count_sqlstr("river_tally")
    sqlstr_count_river_block = get_table_count_sqlstr("river_block")
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block) == 0
    )
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 0
    )

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_block)
        == 40
    )
    with x_culture.get_bank_conn() as bank_conn:
        river_blocks = get_river_block_dict(bank_conn, currency_agenda_healer=sal_text)
    # for river_block in river_blocks.values():
    #     print(f"{river_block=}")

    assert (
        get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_river_tally) == 3
    )

    with x_culture.get_bank_conn() as bank_conn:
        river_tallys = get_river_tally_dict(bank_conn, sal_text)
    river_tallys = x_culture.get_river_tallys(sal_text)
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


def test_culture_set_credit_flow_for_agenda_CorrectlyBuildsASingleContinuousRange(
    env_dir_setup_cleanup,
):
    # GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(title=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(title=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(title=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(title=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(title=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(title=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(title=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=elu_agenda)

    x_culture.refresh_bank_public_agendas_data()

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text, max_blocks_count=100)

    # THEN
    count_range_fails_sql = """
    SELECT COUNT(*)
    FROM (
        SELECT 
            rt1.currency_start current_row_start
        , lag(currency_close) OVER (ORDER BY currency_start, currency_close) AS prev_close
        , lag(currency_close) OVER (ORDER BY currency_start, currency_close) - rt1.currency_start prev_diff
        , rt1.block_num or_block_num
        , lag(block_num) OVER (ORDER BY currency_start, currency_close) AS prev_block_num
        , rt1.parent_block_num or_parent_block_num
        , lag(parent_block_num) OVER (ORDER BY currency_start, currency_close) AS prev_parent_block_num
        , river_tree_level
        , lag(river_tree_level) OVER (ORDER BY currency_start, currency_close) AS prev_parent_river_tree_level
        FROM river_block rt1
        --  WHERE dst_healer = 'sal' and currency_healer = dst_healer
        ORDER BY rt1.currency_start, rt1.currency_close
    ) x
    WHERE x.prev_diff <> 0
        AND ABS(x.prev_diff) < 0.0000000000000001
    ;
    
    """
    with x_culture.get_bank_conn() as bank_conn:
        assert get_single_result_back(bank_conn, count_range_fails_sql) == 0


def test_culture_set_credit_flow_for_agenda_CorrectlyUpatesAgendaPartyUnits(
    env_dir_setup_cleanup,
):
    """GIVEN 5 agendas, 85% of river blocks to sal, left over %15 goes on endless loop that slowly bleeds to sal"""
    # GIVEN
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda_src = agendaunit_shop(_healer=sal_text)
    sal_agenda_src.add_partyunit(title=bob_text, creditor_weight=2, debtor_weight=2)
    sal_agenda_src.add_partyunit(title=tom_text, creditor_weight=2, debtor_weight=1)
    sal_agenda_src.add_partyunit(title=ava_text, creditor_weight=2, debtor_weight=2)
    x_culture.save_public_agenda(x_agenda=sal_agenda_src)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(title=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(title=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(title=sal_text)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(title=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(title=ava_text, creditor_weight=8)
    elu_agenda.add_partyunit(title=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(x_agenda=elu_agenda)

    x_culture.refresh_bank_public_agendas_data()
    sal_agenda_before = x_culture.get_public_agenda(healer=sal_text)

    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text, max_blocks_count=100)
    assert len(sal_agenda_before._partys) == 3
    print(f"{len(sal_agenda_before._partys)=}")
    bob_party = sal_agenda_before._partys.get(bob_text)
    tom_party = sal_agenda_before._partys.get(tom_text)
    ava_party = sal_agenda_before._partys.get(ava_text)
    assert bob_party._bank_tax_paid is None
    assert tom_party._bank_tax_paid is None
    assert ava_party._bank_tax_paid is None
    assert bob_party._bank_tax_diff is None
    assert tom_party._bank_tax_diff is None
    assert ava_party._bank_tax_diff is None
    assert bob_party._bank_voice_rank is None
    assert tom_party._bank_voice_rank is None
    assert ava_party._bank_voice_rank is None
    assert bob_party._bank_voice_hx_lowest_rank is None
    assert tom_party._bank_voice_hx_lowest_rank is None
    assert ava_party._bank_voice_hx_lowest_rank is None

    # WHEN
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    # THEN
    sal_river_tallys = x_culture.get_river_tallys(agenda_healer=sal_text)
    assert len(sal_river_tallys) == 3
    bob_tally = sal_river_tallys.get(bob_text)
    tom_tally = sal_river_tallys.get(tom_text)
    elu_tally = sal_river_tallys.get(elu_text)
    assert bob_tally.tax_healer == bob_text
    assert tom_tally.tax_healer == tom_text
    assert elu_tally.tax_healer == elu_text
    assert bob_tally.currency_healer == sal_text
    assert tom_tally.currency_healer == sal_text
    assert elu_tally.currency_healer == sal_text

    sal_agenda_after = x_culture.get_public_agenda(healer=sal_text)
    bob_party = sal_agenda_after._partys.get(bob_text)
    tom_party = sal_agenda_after._partys.get(tom_text)
    ava_party = sal_agenda_after._partys.get(ava_text)
    elu_party = sal_agenda_after._partys.get(elu_text)

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
    #     partyunit_x = sal_agenda_after._partys.get(sal_river_tally.tax_healer)
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

    # for partyunit_x in sal_agenda_after._partys.values():
    #     print(f"sal_agenda_after {partyunit_x.title=} {partyunit_x._bank_tax_paid=}")
    #     river_tally_x = sal_river_tallys.get(partyunit_x.title)
    #     if river_tally_x is None:
    #         assert partyunit_x._bank_tax_paid is None
    #         assert partyunit_x._bank_tax_diff is None
    #     else:
    #         assert partyunit_x._bank_tax_paid != None
    #         assert partyunit_x._bank_tax_diff != None
    # assert sal_agenda_after != sal_agenda_before
