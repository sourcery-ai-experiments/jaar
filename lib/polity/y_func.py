from sqlite3 import connect as sqlite3_connect, Connection


def sqlite_null(obj_x):
    return "NULL" if obj_x is None else obj_x


def sqlite_bool(int_x) -> bool:
    """convert_sqlite_true_to_python_true"""
    return "NULL" if int_x is None else int_x == 1


def sqlite_text(bool_x) -> str:
    """convert_sqlite_true_to_python_true"""
    if bool_x == True:
        return_str = "TRUE"
    elif bool_x == False:
        return_str = "FALSE"
    else:
        raise TypeError("function requires boolean")
    return return_str


def check_connection(conn) -> bool:
    try:
        conn.cursor()
        return True
    except Exception as ex:
        return False


def get_single_result_back(db_conn: Connection, sqlstr: str) -> str:
    results = db_conn.execute(sqlstr)
    return results.fetchone()[0]
