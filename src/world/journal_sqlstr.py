from src.agenda.atom import (
    get_atom_columns_build,
    atom_hx_table_name,
    atom_curr_table_name,
    AgendaAtom,
)
from src._road.road import RoadUnit
from src.instrument.sqlite import (
    sqlite_bool,
    sqlite_null,
    sqlite_text,
    sqlite_to_python,
)
from dataclasses import dataclass
from sqlite3 import Connection


def get_road_ref_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS road_ref (
  road VARCHAR(MAX) NOT NULL
, delimiter VARCHAR(255) NOT NULL
, UNIQUE(road, delimiter)
;"""


def get_road_ref_table_single_insert_sqlstr(road: RoadUnit, delimiter: str) -> str:
    return f"""
INSERT OR IGNORE INTO road_ref (road, delimiter) 
VALUES (
  '{road}'
, '{delimiter}'
)
;"""


def get_road_ref_table_row_id_select_sqlstr(road: RoadUnit, delimiter: str) -> str:
    return f"""
SELECT rowid FROM road_ref  
WHERE road = '{road}' 
  AND delimiter = '{delimiter}'
)
;"""


def get_atom_hx_table_create_sqlstr() -> str:
    """Create table that hold atom_hx."""
    x_str = f"""
CREATE TABLE IF NOT EXISTS {atom_hx_table_name()} (
, person_id VARCHAR(255) NOT NULL"""

    for x_key, x_value in get_atom_columns_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    return x_str


def get_atom_hx_table_insert_sqlstr(x_atom: AgendaAtom) -> str:
    return x_atom.get_insert_sqlstr()


def get_atom_curr_table_create_sqlstr() -> str:
    """Create table that holds atom current."""
    x_str = f"""
CREATE TABLE IF NOT EXISTS {atom_curr_table_name()} (
, person_id VARCHAR(255) NOT NULL
, {atom_hx_table_name()}_row_id INT NOT NULL"""

    for x_key, x_value in get_atom_columns_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    return x_str


def get_create_table_if_not_exist_sqlstrs() -> list[str]:
    list_x = [get_atom_hx_table_create_sqlstr()]
    list_x.append(get_atom_curr_table_create_sqlstr())
    list_x.append(get_road_ref_table_create_sqlstr())
    return list_x


# get_db_tables(treasury_conn: Connection) -> dict[str:int]:
# get_db_columns(treasury_conn: Connection) -> dict[str : dict[str:int]]:
