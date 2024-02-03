from src.economy.economy import economyunit_shop, EconomyUnit
from src.economy.examples.economy_env_kit import (
    get_temp_env_economy_id,
    get_test_economys_dir,
    env_dir_setup_cleanup,
)
from src.economy.treasury_sqlstr import get_db_tables, get_db_columns
from src.tools.file import open_file
from src.tools.python import get_nested_value, x_get_dict


def check_table_column_existence(tables_dict: dict, x_economy: EconomyUnit) -> bool:
    with x_economy.get_treasury_conn() as treasury_conn:
        db_tables = get_db_tables(treasury_conn)
        db_tables_columns = get_db_columns(treasury_conn)

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


def test_economy_create_dirs_if_null_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # GIVEN create economy
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())

    # WHEN
    x_economy.create_dirs_if_null(in_memory_treasury=True)

    # THEN
    # grab config.json
    config_text = open_file(dest_dir="src/economy", file_name="treasury_db_config.json")
    config_dict = x_get_dict(config_text)
    tables_dict = get_nested_value(config_dict, ["tables"])

    assert check_table_column_existence(tables_dict, x_economy)
