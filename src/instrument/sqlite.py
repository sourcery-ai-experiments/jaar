from sqlite3 import Connection, connect as sqlite3_connect
from dataclasses import dataclass


def sqlite_null(obj_x):
    return "NULL" if obj_x is None else obj_x


def sqlite_bool(int_x) -> bool:
    """convert_sqlite_true_to_python_true"""
    return "NULL" if int_x is None else int_x == 1


def sqlite_text(bool_x) -> str:
    """convert_python_bool_to_SQLITE_bool"""
    if bool_x == True:
        x_text = "TRUE"
    elif bool_x == False:
        x_text = "FALSE"
    else:
        raise TypeError("function requires boolean")
    return x_text


def sqlite_to_python(query_value) -> str:
    """Convert SQLite string to Python None or True"""
    return None if query_value == "NULL" else query_value


def check_connection(conn: Connection) -> bool:
    try:
        conn.cursor()
        return True
    except Exception as ex:
        return False


def get_single_result(db_conn: Connection, sqlstr: str) -> str:
    results = db_conn.execute(sqlstr)
    return results.fetchone()[0]


def create_insert_sqlstr(
    x_table: str, x_columns: list[str], x_values: list[str]
) -> str:
    x_str = f"""INSERT INTO {x_table} ("""
    columns_str = ""
    for x_column in x_columns:
        if columns_str == "":
            columns_str = f"""{columns_str}
  {x_column}"""
        else:
            columns_str = f"""{columns_str}
, {x_column}"""
    values_str = ""
    for x_value in x_values:
        if str(type(x_value)) != "<class 'int'>":
            x_value = f"'{x_value}'"

        if values_str == "":
            values_str = f"""{values_str}
  {x_value}"""
        else:
            values_str = f"""{values_str}
, {x_value}"""

    return f"""{x_str}{columns_str}
)
VALUES ({values_str}
)
;"""


def dict_factory(cursor, row):
    fields = [column[0] for column in cursor.description]
    return dict(zip(fields, row))


@dataclass
class RowData:
    tablename: str = None
    row_dict: str = None


class row_dict_Exception(Exception):
    pass


def rowdata_shop(
    tablename: str,
    row_dict: str,
):
    if str(type(row_dict)) != "<class 'dict'>":
        raise row_dict_Exception("row_dict is not dictionary")
    x_dict = {x_key: x_value for x_key, x_value in row_dict.items() if x_value != None}
    return RowData(tablename, x_dict)


def get_rowdata(tablename: str, x_conn: Connection, select_sqlstr: str) -> RowData:
    x_conn.row_factory = dict_factory
    results = x_conn.execute(select_sqlstr)
    row1 = results.fetchone()
    return rowdata_shop(tablename, row1)
