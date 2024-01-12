from src.economy.economy import economyunit_shop
from src.economy.examples.economy_env_kit import (
    get_temp_env_economy_id,
    get_test_economys_dir,
    env_dir_setup_cleanup,
)
from src.economy.treasury_sqlstr import get_db_tables, get_db_columns


def test_economy_create_dirs_if_null_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # GIVEN create economy
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())

    # WHEN
    x_economy.create_dirs_if_null(in_memory_treasury=True)

    # THEN
    with x_economy.get_treasury_conn() as treasury_conn:
        db_tables = get_db_tables(treasury_conn)
        db_tables_columns = get_db_columns(treasury_conn)

    # row_count = 0
    # for table_name, table_x in tables_dict.items():
    #     row_count += 1
    #     print(f" {table_x=} {row_count}. {table_name=}")

    healer_text = "healer"
    rational_text = "rational"
    agendaunit_text = "agendaunit"
    agendaunit_columns = {healer_text: 1, rational_text: 1}

    agenda_healer_text = "agenda_healer"
    pid_text = "pid"
    _agenda_credit_text = "_agenda_credit"
    _agenda_debt_text = "_agenda_debt"
    _agenda_intent_credit_text = "_agenda_intent_credit"
    _agenda_intent_debt_text = "_agenda_intent_debt"
    _agenda_intent_ratio_credit_text = "_agenda_intent_ratio_credit"
    _agenda_intent_ratio_debt_text = "_agenda_intent_ratio_debt"
    _creditor_active_text = "_creditor_active"
    _debtor_active_text = "_debtor_active"
    _treasury_credit_score_text = "_treasury_credit_score"
    _treasury_voice_rank_text = "_treasury_voice_rank"
    _treasury_voice_hx_lowest_rank_text = "_treasury_voice_hx_lowest_rank"
    _treasury_tax_paid_text = "_treasury_tax_paid"
    _treasury_tax_diff_text = "_treasury_tax_diff"
    _title_text = "_title"
    partyunit_text = "partyunit"
    partyunit_columns = {
        agenda_healer_text: 1,
        pid_text: 1,
        _agenda_credit_text: 1,
        _agenda_debt_text: 1,
        _agenda_intent_credit_text: 1,
        _agenda_intent_debt_text: 1,
        _agenda_intent_ratio_credit_text: 1,
        _agenda_intent_ratio_debt_text: 1,
        _creditor_active_text: 1,
        _debtor_active_text: 1,
        _treasury_tax_paid_text: 1,
        _treasury_tax_diff_text: 1,
        _treasury_credit_score_text: 1,
        _treasury_voice_rank_text: 1,
        _treasury_voice_hx_lowest_rank_text: 1,
        _title_text: 1,
    }

    currency_master_text = "currency_master"
    src_healer_text = "src_healer"
    dst_healer_text = "dst_healer"
    currency_start_text = "currency_start"
    currency_close_text = "currency_close"
    block_num_text = "block_num"
    parent_block_num_text = "parent_block_num"
    river_tree_level_text = "river_tree_level"
    river_block_text = "river_block"
    river_block_columns = {
        currency_master_text: 1,
        src_healer_text: 1,
        dst_healer_text: 1,
        currency_start_text: 1,
        currency_close_text: 1,
        block_num_text: 1,
        parent_block_num_text: 1,
        river_tree_level_text: 1,
    }

    circle_num_text = "circle_num"
    curr_start_text = "curr_start"
    curr_close_text = "curr_close"
    river_circle_text = "river_circle"
    river_circle_columns = {
        currency_master_text: 1,
        dst_healer_text: 1,
        circle_num_text: 1,
        curr_start_text: 1,
        curr_close_text: 1,
    }

    currency_master_text
    src_healer_text
    set_num_text = "set_num"
    reach_curr_start_text = "reach_curr_start"
    reach_curr_close_text = "reach_curr_close"
    river_reach_text = "river_reach"
    river_reach_columns = {
        currency_master_text: 1,
        src_healer_text: 1,
        set_num_text: 1,
        reach_curr_start_text: 1,
        reach_curr_close_text: 1,
    }

    idea_road_text = "idea_road"
    idea_catalog_text = "idea_catalog"
    idea_catalog_columns = {agenda_healer_text: 1, idea_road_text: 1}

    base_text = "base"
    pick_text = "pick"
    belief_catalog_text = "belief_catalog"
    belief_catalog_columns = {agenda_healer_text: 1, base_text: 1, pick_text: 1}

    groupunit_brand_text = "groupunit_brand"
    partylinks_set_by_economy_road_text = "partylinks_set_by_economy_road"
    groupunit_catalog_text = "groupunit_catalog"
    groupunit_catalog_columns = {
        agenda_healer_text: 1,
        groupunit_brand_text: 1,
        partylinks_set_by_economy_road_text: 1,
    }

    time_road_text = "time_road"
    report_date_range_start_text = "report_date_range_start"
    report_date_range_cease_text = "report_date_range_cease"
    report_interval_length_text = "report_interval_length"
    report_interval_intent_task_max_count_text = "report_interval_intent_task_max_count"
    report_interval_intent_state_max_count_text = (
        "report_interval_intent_state_max_count"
    )
    time_begin_text = "time_begin"
    time_close_text = "time_close"
    intent_idea_road_text = "intent_idea_road"
    intent_weight_text = "intent_weight"
    task_text = "task"
    calendar_text = "calendar"
    calendar_columns = {
        time_road_text: 1,
        report_date_range_start_text: 1,
        report_date_range_cease_text: 1,
        report_interval_length_text: 1,
        report_interval_intent_task_max_count_text: 1,
        report_interval_intent_state_max_count_text: 1,
        time_begin_text: 1,
        time_close_text: 1,
        intent_idea_road_text: 1,
        intent_weight_text: 1,
        task_text: 1,
    }

    curr_tables = {
        agendaunit_text: agendaunit_columns,
        partyunit_text: partyunit_columns,
        river_block_text: river_block_columns,
        river_circle_text: river_circle_columns,
        river_reach_text: river_reach_columns,
        idea_catalog_text: idea_catalog_columns,
        belief_catalog_text: belief_catalog_columns,
        groupunit_catalog_text: groupunit_catalog_columns,
        calendar_text: calendar_columns,
    }

    # for x_table_key, x_table_value in db_tables.items():
    #     print(f"{x_table_key=} {x_table_value=} {curr_tables.get(x_table_key)=}")
    #     assert curr_tables.get(x_table_key) != None

    assert db_tables.get(belief_catalog_text) != None  # 6
    assert db_tables.get(agendaunit_text) != None  # 0
    assert db_tables.get(groupunit_catalog_text) != None  # 7
    assert db_tables.get(idea_catalog_text) != None  # 5
    assert db_tables.get(partyunit_text) != None  # 1
    assert db_tables.get(river_circle_text) != None  # 4
    assert db_tables.get(river_block_text) != None  # 3
    assert db_tables.get(river_reach_text) != None  # 8
    assert db_tables.get(calendar_text) != None  # 9
    assert len(db_tables) == 9
    assert len(db_tables) == len(curr_tables)
    assert len(db_tables) == len(db_tables_columns)

    # for y_table_key, y_columns_value in db_tables_columns.items():
    #     for y_column_key, y_column_value in y_columns_value.items():
    #         print(f"{y_table_key=} {y_column_key=}")
    #     assert curr_tables.get(y_table_key) == y_columns_value

    assert db_tables_columns.get(belief_catalog_text) == belief_catalog_columns
    assert db_tables_columns.get(agendaunit_text) == agendaunit_columns
    assert db_tables_columns.get(groupunit_catalog_text) == groupunit_catalog_columns
    assert db_tables_columns.get(idea_catalog_text) == idea_catalog_columns
    assert db_tables_columns.get(partyunit_text) == partyunit_columns
    assert db_tables_columns.get(river_circle_text) == river_circle_columns
    assert db_tables_columns.get(river_block_text) == river_block_columns
