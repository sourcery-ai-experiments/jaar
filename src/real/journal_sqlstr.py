from src.atom.quark import (
    get_quark_columns_build,
    quark_hx_table_name,
    quark_mstr_table_name,
    QuarkUnit,
)
from src._road.road import RoadUnit

# from src._instrument.sqlite import (
#     sqlite_bool,
#     sqlite_null,
#     sqlite_text,
#     sqlite_to_python,
# )
# from dataclasses import dataclass
# from sqlite3 import Connection


def get_quark_hx_table_create_sqlstr() -> str:
    """Create table that hold quark_hx."""
    x_str = f"""
CREATE TABLE IF NOT EXISTS {quark_hx_table_name()} (
  person_id VARCHAR(255) NOT NULL"""

    for x_key, x_value in get_quark_columns_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    x_str = f"""{x_str}
)
;"""
    return x_str


def get_quark_hx_table_insert_sqlstr(x_quark: QuarkUnit) -> str:
    return x_quark.get_insert_sqlstr()


def get_quark_mstr_table_create_sqlstr() -> str:
    """Create table that holds quarkunits."""
    x_str = f"""
CREATE TABLE IF NOT EXISTS {quark_mstr_table_name()} (
  person_id VARCHAR(255) NOT NULL
, {quark_hx_table_name()}_row_id INT NOT NULL"""

    for x_key, x_value in get_quark_columns_build().items():
        if x_value == "TEXT":
            x_value = "VARCHAR(255)"
        x_str = f"""{x_str}\n, {x_key} {x_value} NULL"""

    x_str = f"""{x_str}
)
;"""
    return x_str


def get_quark_nuc_link_table_create_sqlstr() -> str:
    return """
CREATE TABLE quark_nuc_link
(
  quark_rowid INT NOT NULL
, nuc_rowid INT NOT NULL
, UNIQUE(quark_rowid, nuc_rowid)
, CONSTRAINT quark_fk FOREIGN KEY (quark_rowid) REFERENCES quark_mstr (rowid)
, CONSTRAINT nuc_fk FOREIGN KEY (nuc_rowid) REFERENCES nuc_mstr (rowid)
)
;"""


def get_nuc_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS nuc_mstr (
  author_person_id VARCHAR(255) NOT NULL
, author_nuc_number INT NOT NULL
, UNIQUE(author_person_id, author_nuc_number)
)
;"""


def get_nuc_atom_link_table_create_sqlstr() -> str:
    return """
CREATE TABLE nuc_atom_link
(
  nuc_rowid INT NOT NULL
, atom_rowid INT NOT NULL
, UNIQUE(nuc_rowid, atom_rowid)
, CONSTRAINT quark_fk FOREIGN KEY (nuc_rowid) REFERENCES nuc_mstr (rowid)
, CONSTRAINT nuc_fk FOREIGN KEY (atom_rowid) REFERENCES atom_mstr (rowid)
)
;"""


def get_atom_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS atom_mstr (
  author_person_id VARCHAR(255) NOT NULL
, author_atom_number INT NOT NULL
, UNIQUE(author_person_id, author_atom_number)
)
;"""


def get_atom_person_link_table_create_sqlstr() -> str:
    return """
CREATE TABLE atom_person_link
(
  atom_rowid INT NOT NULL
, person_rowid INT NOT NULL
, UNIQUE(atom_rowid, person_rowid)
, CONSTRAINT nuc_fk FOREIGN KEY (atom_rowid) REFERENCES atom_mstr (rowid)
, CONSTRAINT person_fk FOREIGN KEY (person_rowid) REFERENCES person (rowid)
)
;"""


def get_person_mstr_table_create_sqlstr() -> str:
    return """
CREATE TABLE person_mstr
(
  person_id VARCHAR(255) NOT NULL
, UNIQUE(person_id)
)
;"""


def get_road_ref_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS road_ref (
  road VARCHAR(255) NOT NULL
, delimiter VARCHAR(255) NOT NULL
, UNIQUE(road, delimiter)
)
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


def get_create_table_if_not_exist_sqlstrs() -> list[str]:
    list_x = [get_quark_hx_table_create_sqlstr()]
    list_x.append(get_quark_mstr_table_create_sqlstr())
    list_x.append(get_quark_nuc_link_table_create_sqlstr())
    list_x.append(get_nuc_table_create_sqlstr())
    list_x.append(get_nuc_atom_link_table_create_sqlstr())
    list_x.append(get_atom_table_create_sqlstr())
    list_x.append(get_atom_person_link_table_create_sqlstr())
    list_x.append(get_person_mstr_table_create_sqlstr())
    list_x.append(get_road_ref_table_create_sqlstr())
    return list_x


# get_db_tables(treasury_conn: Connection) -> dict[str:int]:
# get_db_columns(treasury_conn: Connection) -> dict[str : dict[str:int]]:
