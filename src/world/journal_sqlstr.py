from src.agenda.atom import get_atom_columns_build
from src.agenda.agenda import AgendaUnit, PartyUnit
from src._road.road import create_road_without_root_node, RoadUnit, PersonID, PartyID
from src.instrument.sqlite import (
    sqlite_bool,
    sqlite_null,
    sqlite_text,
    sqlite_to_python,
)
from dataclasses import dataclass
from sqlite3 import Connection


def get_deal_hx_table_create_sqlstr() -> str:
    """Create table that hold deal_hx."""
    x_str = """
CREATE TABLE IF NOT EXISTS deal_hx (
, person_id VARCHAR(255) NOT NULL"""

    for x_key, x_value in get_atom_columns_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    return x_str


def get_deal_curr_table_create_sqlstr() -> str:
    """Create table that hold deal_hx."""
    x_str = """
CREATE TABLE IF NOT EXISTS deal_hx (
, person_id VARCHAR(255) NOT NULL"""

    for x_key, x_value in get_atom_columns_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    return x_str


# def get_agendaunit_table_insert_sqlstr(x_agenda: AgendaUnit) -> str:
#     return f"""
# INSERT INTO agendaunit (
#   worker_id
# , rational
# )
# VALUES (
#   '{x_agenda._worker_id}'
# , NULL
# )
# ;
# """


# def get_agendaunits_select_sqlstr():
#     return """
# SELECT
#   worker_id
# , rational
# FROM agendaunit
# ;
# """


def get_create_table_if_not_exist_sqlstrs() -> list[str]:
    list_x = [get_deal_hx_table_create_sqlstr()]
    list_x.append(get_deal_curr_table_create_sqlstr())
    return list_x


def get_db_tables(treasury_conn: Connection) -> dict[str:int]:
    sqlstr = "SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;"
    results = treasury_conn.execute(sqlstr)

    return {row[0]: 1 for row in results}


def get_db_columns(treasury_conn: Connection) -> dict[str : dict[str:int]]:
    table_names = get_db_tables(treasury_conn)
    table_column_dict = {}
    for table_name in table_names.keys():
        sqlstr = f"SELECT name FROM PRAGMA_TABLE_INFO('{table_name}');"
        results = treasury_conn.execute(sqlstr)
        table_column_dict[table_name] = {row[0]: 1 for row in results}

    return table_column_dict
