from sqlite3 import Connection


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
        print(f"{type(x_value)=}")
        if str(type(x_value)) != "<class 'int'>":
            x_value = f"'{x_value}'"

        if values_str == "":
            values_str = f"""{values_str}
  {x_value}"""
        else:
            values_str = f"""{values_str}
, {x_value}"""

    x_str = f"""{x_str}{columns_str}
)
VALUES ({values_str}
)
;"""
    print(x_str)
    return x_str
