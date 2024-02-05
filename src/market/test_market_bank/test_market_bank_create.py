from src.market.market import marketunit_shop, MarketUnit
from src.market.examples.market_env_kit import (
    get_temp_env_market_id,
    get_test_markets_dir,
    env_dir_setup_cleanup,
)
from src.market.bank_sqlstr import get_db_tables, get_db_columns
from src.instrument.file import open_file
from src.instrument.python import get_nested_value, x_get_dict


def check_table_column_existence(tables_dict: dict, x_market: MarketUnit) -> bool:
    with x_market.get_bank_conn() as bank_conn:
        db_tables = get_db_tables(bank_conn)
        db_tables_columns = get_db_columns(bank_conn)

    for table_name, table_dict in tables_dict.items():
        print(f"Table: {table_name}")
        if db_tables.get(table_name) is None:
            return False

        db_columns = set(db_tables_columns.get(table_name).keys())
        config_columns = set(table_dict.get("columns").keys())
        diff_columns = db_columns.symmetric_difference(config_columns)
        print(f"Table: {table_name} Column differences: {diff_columns}")

        if diff_columns:
            return False

    return True


def test_market_create_dirs_if_null_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # GIVEN create market
    x_market = marketunit_shop(get_temp_env_market_id(), get_test_markets_dir())

    # WHEN
    x_market.create_dirs_if_null(in_memory_bank=True)

    # THEN
    # grab config.json
    config_text = open_file(dest_dir="src/market", file_name="bank_db_config.json")
    config_dict = x_get_dict(config_text)
    tables_dict = get_nested_value(config_dict, ["tables"])

    assert check_table_column_existence(tables_dict, x_market)
