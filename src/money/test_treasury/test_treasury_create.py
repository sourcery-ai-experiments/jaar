from src.money.money import moneyunit_shop, MoneyUnit
from src.money.examples.econ_env import env_dir_setup_cleanup, get_texas_hubunit
from src._instrument.sqlite import get_db_tables, get_db_columns
from src._instrument.file import open_file
from src._instrument.python import get_nested_value, get_dict_from_json


def check_table_column_existence(tables_dict: dict, x_money: MoneyUnit) -> bool:
    with x_money.get_treasury_conn() as treasury_conn:
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


def test_MoneyUnit_set_econ_dirs_CorrectlyCreatesDBTables(env_dir_setup_cleanup):
    # GIVEN create econ
    x_money = moneyunit_shop(get_texas_hubunit())

    # WHEN
    x_money.create_treasury_db(in_memory=True)

    # THEN
    # grab config.json
    config_text = open_file(dest_dir="src/money", file_name="treasury_db_config.json")
    config_dict = get_dict_from_json(config_text)
    tables_dict = get_nested_value(config_dict, ["tables"])

    assert check_table_column_existence(tables_dict, x_money)
