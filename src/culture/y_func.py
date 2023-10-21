from sqlite3 import Connection


def sqlite_null(obj_x):
    return "NULL" if obj_x is None else obj_x


def sqlite_bool(int_x) -> bool:
    """convert_sqlite_true_to_python_true"""
    return "NULL" if int_x is None else int_x == 1


def sqlite_text(bool_x) -> str:
    """convert_sqlite_true_to_python_true"""
    if bool_x == True:
        x_text = "TRUE"
    elif bool_x == False:
        x_text = "FALSE"
    else:
        raise TypeError("function requires boolean")
    return x_text


def sqlite_to_python(query_value) -> str:
    return None if query_value == "NULL" else query_value


def check_connection(conn: Connection) -> bool:
    try:
        conn.cursor()
        return True
    except Exception as ex:
        return False


def get_single_result_back(db_conn: Connection, sqlstr: str) -> str:
    results = db_conn.execute(sqlstr)
    return results.fetchone()[0]
