from src.agenda.agenda import (
    agendaunit_shop,
    ideacore_shop,
    groupunit_shop,
    partylink_shop,
)
from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_handle,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from src.culture.y_func import get_single_result_back
from src.culture.bank_sqlstr import (
    get_db_tables,
    get_db_columns,
    get_table_count_sqlstr,
)


def test_culture_create_dirs_if_null_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # GIVEN create culture
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())

    # WHEN
    x_culture.create_dirs_if_null(in_memory_bank=True)

    # THEN
    with x_culture.get_bank_conn() as bank_conn:
        db_tables = get_db_tables(bank_conn)
        db_tables_columns = get_db_columns(bank_conn)

    # row_count = 0
    # for table_mame, table_x in tables_dict.items():
    #     row_count += 1
    #     print(f" {table_x=} {row_count}. {table_mame=}")

    healer_text = "healer"
    voice_rank_text = "voice_rank"
    agendaunit_text = "agendaunit"
    agendaunit_columns = {healer_text: 1, voice_rank_text: 1}

    agenda_healer_text = "agenda_healer"
    party_title_text = "party_title"
    _agenda_credit_text = "_agenda_credit"
    _agenda_debt_text = "_agenda_debt"
    _agenda_goal_credit_text = "_agenda_goal_credit"
    _agenda_goal_debt_text = "_agenda_goal_debt"
    _agenda_goal_ratio_credit_text = "_agenda_goal_ratio_credit"
    _agenda_goal_ratio_debt_text = "_agenda_goal_ratio_debt"
    _creditor_active_text = "_creditor_active"
    _debtor_active_text = "_debtor_active"
    ledger_text = "ledger"
    ledger_columns = {
        agenda_healer_text: 1,
        party_title_text: 1,
        _agenda_credit_text: 1,
        _agenda_debt_text: 1,
        _agenda_goal_credit_text: 1,
        _agenda_goal_debt_text: 1,
        _agenda_goal_ratio_credit_text: 1,
        _agenda_goal_ratio_debt_text: 1,
        _creditor_active_text: 1,
        _debtor_active_text: 1,
    }

    currency_healer_text = "currency_healer"
    tax_healer_text = "tax_healer"
    tax_total_text = "tax_total"
    debt_text = "debt"
    tax_diff_text = "tax_diff"
    river_tally_text = "river_tally"
    river_tally_columns = {
        currency_healer_text: 1,
        tax_healer_text: 1,
        tax_total_text: 1,
        debt_text: 1,
        tax_diff_text: 1,
    }

    src_healer_text = "src_healer"
    dst_healer_text = "dst_healer"
    currency_start_text = "currency_start"
    currency_close_text = "currency_close"
    flow_num_text = "flow_num"
    parent_flow_num_text = "parent_flow_num"
    river_tree_level_text = "river_tree_level"
    river_flow_text = "river_flow"
    river_flow_columns = {
        currency_healer_text: 1,
        src_healer_text: 1,
        dst_healer_text: 1,
        currency_start_text: 1,
        currency_close_text: 1,
        flow_num_text: 1,
        parent_flow_num_text: 1,
        river_tree_level_text: 1,
    }

    bucket_num_text = "bucket_num"
    curr_start_text = "curr_start"
    curr_close_text = "curr_close"
    river_bucket_text = "river_bucket"
    river_bucket_columns = {
        currency_healer_text: 1,
        dst_healer_text: 1,
        bucket_num_text: 1,
        curr_start_text: 1,
        curr_close_text: 1,
    }

    idea_road_text = "idea_road"
    idea_catalog_text = "idea_catalog"
    idea_catalog_columns = {agenda_healer_text: 1, idea_road_text: 1}

    base_text = "base"
    pick_text = "pick"
    acptfact_catalog_text = "acptfact_catalog"
    acptfact_catalog_columns = {agenda_healer_text: 1, base_text: 1, pick_text: 1}

    groupunit_brand_text = "groupunit_brand"
    partylinks_set_by_culture_road_text = "partylinks_set_by_culture_road"
    groupunit_catalog_text = "groupunit_catalog"
    groupunit_catalog_columns = {
        agenda_healer_text: 1,
        groupunit_brand_text: 1,
        partylinks_set_by_culture_road_text: 1,
    }

    curr_tables = {
        agendaunit_text: agendaunit_columns,
        ledger_text: ledger_columns,
        river_tally_text: river_tally_columns,
        river_flow_text: river_flow_columns,
        river_bucket_text: river_bucket_columns,
        idea_catalog_text: idea_catalog_columns,
        acptfact_catalog_text: acptfact_catalog_columns,
        groupunit_catalog_text: groupunit_catalog_columns,
    }

    # for x_table_key, x_table_value in db_tables.items():
    #     print(f"{x_table_key=} {x_table_value=} {curr_tables.get(x_table_key)=}")
    #     assert curr_tables.get(x_table_key) != None

    assert db_tables.get(acptfact_catalog_text) != None  # 6
    assert db_tables.get(agendaunit_text) != None  # 0
    assert db_tables.get(groupunit_catalog_text) != None  # 7
    assert db_tables.get(idea_catalog_text) != None  # 5
    assert db_tables.get(ledger_text) != None  # 1
    assert db_tables.get(river_bucket_text) != None  # 4
    assert db_tables.get(river_flow_text) != None  # 3
    assert db_tables.get(river_tally_text) != None  # 2
    assert len(db_tables) == 8
    assert len(db_tables) == len(curr_tables)
    assert len(db_tables) == len(db_tables_columns)

    # for y_table_key, y_columns_value in db_tables_columns.items():
    #     for y_column_key, y_column_value in y_columns_value.items():
    #         print(f"{y_table_key=} {y_column_key=}")
    #     assert curr_tables.get(y_table_key) == y_columns_value

    assert db_tables_columns.get(agendaunit_text) == agendaunit_columns
    assert db_tables_columns.get(acptfact_catalog_text) == acptfact_catalog_columns
    assert db_tables_columns.get(agendaunit_text) == agendaunit_columns
    assert db_tables_columns.get(groupunit_catalog_text) == groupunit_catalog_columns
    assert db_tables_columns.get(idea_catalog_text) == idea_catalog_columns
    assert db_tables_columns.get(ledger_text) == ledger_columns
    assert db_tables_columns.get(river_bucket_text) == river_bucket_columns
    assert db_tables_columns.get(river_flow_text) == river_flow_columns
    assert db_tables_columns.get(river_tally_text) == river_tally_columns


def test_culture_refresh_bank_metrics_CorrectlyDeletesOldBankInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(
        handle=get_temp_env_handle(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"

    bob = agendaunit_shop(_healer=bob_text)
    bob.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob)
    x_culture.refresh_bank_metrics()
    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_ledger) == 1

    # WHEN
    x_culture.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_ledger) == 1


def test_culture_refresh_bank_metrics_CorrectlyDeletesOldBankFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(
        handle=get_temp_env_handle(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_bank=False)

    bob_text = "bob"
    tom_text = "tom"

    bob = agendaunit_shop(_healer=bob_text)
    bob.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    x_culture.save_public_agenda(x_agenda=bob)
    x_culture.refresh_bank_metrics()
    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_ledger) == 1

    # WHEN
    x_culture.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_ledger) == 1


def test_culture_refresh_bank_metrics_CorrectlyPopulatesLedgerTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows
    x_culture = cultureunit_shop(
        handle=get_temp_env_handle(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    bob = agendaunit_shop(_healer=bob_text)
    bob.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    bob.add_partyunit(title=sal_text, creditor_weight=1, debtor_weight=4)
    bob.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=4)
    x_culture.save_public_agenda(x_agenda=bob)

    sal = agendaunit_shop(_healer=sal_text)
    sal.add_partyunit(title=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_partyunit(title=tom_text, creditor_weight=3, debtor_weight=1)
    sal.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=4)
    x_culture.save_public_agenda(x_agenda=sal)

    tom = agendaunit_shop(_healer=tom_text)
    tom.add_partyunit(title=bob_text, creditor_weight=3, debtor_weight=1)
    tom.add_partyunit(title=sal_text, creditor_weight=1, debtor_weight=4)
    tom.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=4)
    x_culture.save_public_agenda(x_agenda=tom)

    elu = agendaunit_shop(_healer=elu_text)
    elu.add_partyunit(title=bob_text, creditor_weight=3, debtor_weight=1)
    elu.add_partyunit(title=tom_text, creditor_weight=1, debtor_weight=4)
    elu.add_partyunit(title=elu_text, creditor_weight=1, debtor_weight=4)
    x_culture.save_public_agenda(x_agenda=elu)

    sqlstr_count_ledger = get_table_count_sqlstr("ledger")
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_ledger) == 0

    # WHEN
    x_culture.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_ledger) == 12


def test_culture_refresh_bank_metrics_CorrectlyPopulatesDealTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows
    x_culture = cultureunit_shop(
        handle=get_temp_env_handle(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    x_culture.save_public_agenda(x_agenda=agendaunit_shop(_healer=bob_text))
    x_culture.save_public_agenda(x_agenda=agendaunit_shop(_healer=tom_text))
    x_culture.save_public_agenda(x_agenda=agendaunit_shop(_healer=sal_text))
    x_culture.save_public_agenda(x_agenda=agendaunit_shop(_healer=elu_text))

    sqlstr_count_agendas = get_table_count_sqlstr("agendaunit")
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_agendas) == 0

    # WHEN
    x_culture.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_agendas) == 4


def test_culture_refresh_bank_metrics_CorrectlyPopulatesDealTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows
    x_culture = cultureunit_shop(
        handle=get_temp_env_handle(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    x_culture.save_public_agenda(x_agenda=agendaunit_shop(_healer=bob_text))
    x_culture.save_public_agenda(x_agenda=agendaunit_shop(_healer=tom_text))
    x_culture.save_public_agenda(x_agenda=agendaunit_shop(_healer=sal_text))
    x_culture.save_public_agenda(x_agenda=agendaunit_shop(_healer=elu_text))

    sqlstr_count_agendas = get_table_count_sqlstr("agendaunit")
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_agendas) == 0

    # WHEN
    x_culture.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr_count_agendas) == 4


def test_culture_refresh_bank_metrics_CorrectlyPopulates_groupunit_catalog(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(
        handle=get_temp_env_handle(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_bank=True)

    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"
    bob_agenda = agendaunit_shop(_healer=bob_text)
    tom_agenda = agendaunit_shop(_healer=tom_text)
    bob_agenda.add_partyunit(title=tom_text)
    tom_agenda.add_partyunit(title=bob_text)
    tom_agenda.add_partyunit(title=elu_text)
    x_culture.save_public_agenda(x_agenda=bob_agenda)
    x_culture.save_public_agenda(x_agenda=tom_agenda)

    sqlstr = get_table_count_sqlstr("groupunit_catalog")
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr) == 0

    # WHEN
    x_culture.refresh_bank_metrics()

    # THEN
    assert get_single_result_back(x_culture.get_bank_conn(), sqlstr) == 3


def test_culture_set_agenda_bank_attrs_CorrectlyPopulatesDeal_Groupunit_Partylinks(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(
        handle=get_temp_env_handle(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_bank=True)

    # create 4 agendas, 1 with group "swimming expert" linked to 1 party
    # two others have idea f"{root_label()},sports,swimming"
    # run set_bank_metrics
    # assert
    # _partylinks_set_by_culture_road
    # assert group "swimming expert" has 1 party
    # change groupunit "swimming expert" _partylinks_set_by_culture_road ==  f"{root_label()}sports,swimmer"
    # run set_bank_metrics
    # assert group "swimming expert" has 2 different party

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    bob_agenda = agendaunit_shop(_healer=bob_text)
    tom_agenda = agendaunit_shop(_healer=tom_text)
    ava_agenda = agendaunit_shop(_healer=ava_text)

    swim_text = "swimming"
    sports_text = "sports"
    sal_sports_road = f"{x_culture.handle},{sports_text}"
    bob_sports_road = f"{x_culture.handle},{sports_text}"
    tom_sports_road = f"{x_culture.handle},{sports_text}"

    sal_agenda.add_idea(idea_kid=ideacore_shop(_label=swim_text), pad=sal_sports_road)
    bob_agenda.add_idea(idea_kid=ideacore_shop(_label=swim_text), pad=bob_sports_road)
    tom_agenda.add_idea(idea_kid=ideacore_shop(_label=swim_text), pad=tom_sports_road)

    sal_agenda.add_partyunit(title=bob_text, creditor_weight=2, debtor_weight=2)

    swim_group_text = "swimming expert"
    swim_group_unit = groupunit_shop(brand=swim_group_text)
    bob_link = partylink_shop(title=bob_text)
    swim_group_unit.set_partylink(partylink=bob_link)
    sal_agenda.set_groupunit(groupunit=swim_group_unit)

    x_culture.save_public_agenda(x_agenda=sal_agenda)
    x_culture.save_public_agenda(x_agenda=bob_agenda)
    x_culture.save_public_agenda(x_agenda=tom_agenda)
    x_culture.save_public_agenda(x_agenda=ava_agenda)

    x_culture.set_agenda_bank_attrs(agenda_healer=sal_text)
    e1_sal_agenda = x_culture.get_public_agenda(healer=sal_text)
    assert len(e1_sal_agenda._groups.get(swim_group_text)._partys) == 1

    # WHEN
    # change groupunit "swimming expert" _partylinks_set_by_culture_road ==  f"{root_label()},sports,swimmer"
    sal_swim_road = f"{sal_sports_road},{swim_text}"
    swim_group_unit.set_attr(_partylinks_set_by_culture_road=sal_swim_road)
    sal_agenda.set_groupunit(groupunit=swim_group_unit)
    x_culture.save_public_agenda(x_agenda=sal_agenda)
    x_culture.set_agenda_bank_attrs(agenda_healer=sal_text)

    # THEN
    e1_sal_agenda = x_culture.get_public_agenda(healer=sal_text)
    assert len(e1_sal_agenda._groups.get(swim_group_text)._partys) == 2
