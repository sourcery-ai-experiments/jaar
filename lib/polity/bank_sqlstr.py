from lib.agent.agent import AgentUnit
from lib.agent.ally import AllyUnit
from lib.polity.y_func import sqlite_bool, sqlite_null
from dataclasses import dataclass
from sqlite3 import Connection


def get_river_flow_table_delete_sqlstr(currency_agent_name: str) -> str:
    return f"""
        DELETE FROM river_flow
        WHERE currency_name = '{currency_agent_name}' 
        ;
    """


def get_river_flow_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS river_flow (
          currency_name VARCHAR(255) NOT NULL
        , src_name VARCHAR(255) NOT NULL
        , dst_name VARCHAR(255) NOT NULL
        , currency_start FLOAT NOT NULL
        , currency_close FLOAT NOT NULL
        , flow_num INT NOT NULL
        , parent_flow_num INT NULL
        , river_tree_level INT NOT NULL
        , FOREIGN KEY(currency_name) REFERENCES agentunits(name)
        , FOREIGN KEY(src_name) REFERENCES agentunits(name)
        , FOREIGN KEY(dst_name) REFERENCES agentunits(name)
        )
        ;
    """


@dataclass
class RiverFlowUnit:
    currency_agent_name: str
    src_name: str
    dst_name: str
    currency_start: float
    currency_close: float
    flow_num: int
    parent_flow_num: int
    river_tree_level: int

    def flow_returned(self) -> bool:
        if self.currency_agent_name == self.dst_name:
            return True
        else:
            return False


def get_river_flow_table_insert_sqlstr(
    river_flow_x: RiverFlowUnit,
) -> str:
    return f"""
        INSERT INTO river_flow (
          currency_name
        , src_name
        , dst_name
        , currency_start 
        , currency_close
        , flow_num
        , parent_flow_num
        , river_tree_level
        )
        VALUES (
          '{river_flow_x.currency_agent_name}'
        , '{river_flow_x.src_name}'
        , '{river_flow_x.dst_name}'
        , {sqlite_null(river_flow_x.currency_start)}
        , {sqlite_null(river_flow_x.currency_close)}
        , {river_flow_x.flow_num}
        , {sqlite_null(river_flow_x.parent_flow_num)}
        , {river_flow_x.river_tree_level}
        )
        ;
    """


def get_river_flow_dict(
    db_conn: str, currency_agent_name: str
) -> dict[str:RiverFlowUnit]:
    sqlstr = f"""
        SELECT 
          currency_name
        , src_name
        , dst_name
        , currency_start
        , currency_close
        , flow_num
        , parent_flow_num
        , river_tree_level
        FROM river_flow
        WHERE currency_name = '{currency_agent_name}' 
        ;
    """
    dict_x = {}
    cursor_x = db_conn.cursor()
    results_cursor_x = cursor_x.execute(sqlstr)
    results_x = results_cursor_x.fetchall()

    count_x = 0
    for row in results_x:
        river_flow_x = RiverFlowUnit(
            currency_agent_name=row[0],
            src_name=row[1],
            dst_name=row[2],
            currency_start=row[3],
            currency_close=row[4],
            flow_num=row[5],
            parent_flow_num=row[6],
            river_tree_level=row[7],
        )
        dict_x[count_x] = river_flow_x
        count_x += 1
    return dict_x


def get_river_bucket_table_delete_sqlstr(currency_agent_name: str) -> str:
    return f"""
        DELETE FROM river_bucket
        WHERE currency_name = '{currency_agent_name}' 
        ;
    """


def get_river_bucket_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS river_bucket (
          currency_name VARCHAR(255) NOT NULL
        , dst_name VARCHAR(255) NOT NULL
        , bucket_num INT NOT NULL
        , curr_start FLOAT NOT NULL
        , curr_close FLOAT NOT NULL
        , FOREIGN KEY(currency_name) REFERENCES agentunits(name)
        , FOREIGN KEY(dst_name) REFERENCES agentunits(name)
        )
    ;
    """


def get_river_bucket_table_insert_sqlstr(currency_agent_name: str) -> str:
    return f"""
        INSERT INTO river_bucket (
          currency_name
        , dst_name
        , bucket_num
        , curr_start
        , curr_close
        )
        SELECT 
          currency_name
        , dst_name
        , currency_bucket_num
        , min(currency_start) currency_bucket_start
        , max(currency_close) currency_bucket_close
        FROM  (
        SELECT *, SUM(step) OVER (ORDER BY currency_start) AS currency_bucket_num
        FROM  (
            SELECT 
            CASE 
            WHEN lag(currency_close) OVER (ORDER BY currency_start) < currency_start 
                OR lag(currency_close) OVER (ORDER BY currency_start) = NULL 
            THEN 1
            ELSE 0
            END AS step
            , *
            FROM  river_flow
            WHERE currency_name = '{currency_agent_name}' and dst_name = currency_name 
            ) b
        ) c
        GROUP BY currency_name, dst_name, currency_bucket_num
        ORDER BY currency_bucket_start
        ;
    """


@dataclass
class RiverBucketUnit:
    currency_name: str
    dst_name: str
    bucket_num: int
    curr_start: float
    curr_close: float


def get_river_bucket_dict(
    db_conn: Connection, currency_agent_name: str
) -> dict[str:RiverBucketUnit]:
    sqlstr = f"""
        SELECT
          currency_name
        , dst_name
        , bucket_num
        , curr_start
        , curr_close
        FROM river_bucket
        WHERE currency_name = '{currency_agent_name}'
        ;
    """
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        river_bucket_x = RiverBucketUnit(
            currency_name=row[0],
            dst_name=row[1],
            bucket_num=row[2],
            curr_start=row[3],
            curr_close=row[4],
        )
        dict_x[river_bucket_x.bucket_num] = river_bucket_x
    return dict_x


def get_river_tally_table_delete_sqlstr(currency_agent_name: str) -> str:
    return f"""
        DELETE FROM river_tally
        WHERE currency_name = '{currency_agent_name}' 
        ;
    """


def get_river_tally_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS river_tally (
          currency_name VARCHAR(255) NOT NULL
        , tax_name VARCHAR(255) NOT NULL
        , tax_total FLOAT NOT NULL
        , debt FLOAT NULL
        , tax_diff FLOAT NULL
        , FOREIGN KEY(currency_name) REFERENCES agentunits(name)
        , FOREIGN KEY(tax_name) REFERENCES agentunits(name)
        )
    ;
    """


def get_river_tally_table_insert_sqlstr(currency_agent_name: str) -> str:
    return f"""
        INSERT INTO river_tally (
          currency_name
        , tax_name
        , tax_total
        , debt
        , tax_diff
        )
        SELECT 
          rt.currency_name
        , rt.src_name
        , SUM(rt.currency_close-rt.currency_start) tax_paid
        , l._agent_agenda_ratio_debt
        , l._agent_agenda_ratio_debt - SUM(rt.currency_close-rt.currency_start)
        FROM river_flow rt
        LEFT JOIN ledger l ON l.agent_name = rt.currency_name AND l.ally_name = rt.src_name
        WHERE rt.currency_name='{currency_agent_name}' and rt.dst_name=rt.currency_name
        GROUP BY rt.currency_name, rt.src_name
        ;
    """


@dataclass
class RiverTallyUnit:
    currency_name: str
    tax_name: str
    tax_total: float
    debt: float
    tax_diff: float


def get_river_tally_dict(
    db_conn: Connection, currency_agent_name: str
) -> dict[str:RiverTallyUnit]:
    sqlstr = f"""
        SELECT
          currency_name
        , tax_name
        , tax_total
        , debt
        , tax_diff
        FROM river_tally
        WHERE currency_name = '{currency_agent_name}'
        ;
    """
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        river_tally_x = RiverTallyUnit(
            currency_name=row[0],
            tax_name=row[1],
            tax_total=row[2],
            debt=row[3],
            tax_diff=row[4],
        )
        dict_x[river_tally_x.tax_name] = river_tally_x
    return dict_x


def get_agent_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS agentunits (
          name VARCHAR(255) PRIMARY KEY ASC
        , UNIQUE(name)
        )
    ;
    """


def get_agent_table_insert_sqlstr(agent_x: AgentUnit) -> str:
    return f"""
        INSERT INTO agentunits (
            name
            )
        VALUES (
            '{agent_x._desc}' 
        )
        ;
        """


def get_ledger_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS ledger (
          agent_name INTEGER 
        , ally_name INTEGER
        , _agent_credit FLOAT
        , _agent_debt FLOAT
        , _agent_agenda_credit FLOAT
        , _agent_agenda_debt FLOAT
        , _agent_agenda_ratio_credit FLOAT
        , _agent_agenda_ratio_debt FLOAT
        , _creditor_active INT
        , _debtor_active INT
        , FOREIGN KEY(agent_name) REFERENCES agentunits(name)
        , FOREIGN KEY(ally_name) REFERENCES agentunits(name)
        , UNIQUE(agent_name, ally_name)
        )
    ;
    """


def get_ledger_table_insert_sqlstr(agent_x: AgentUnit, allyunit_x: AllyUnit) -> str:
    sqlstr = f"""
        INSERT INTO ledger (
              agent_name
            , ally_name
            , _agent_credit
            , _agent_debt
            , _agent_agenda_credit
            , _agent_agenda_debt
            , _agent_agenda_ratio_credit
            , _agent_agenda_ratio_debt
            , _creditor_active
            , _debtor_active
            )
        VALUES (
            '{agent_x._desc}' 
            , '{allyunit_x.name}'
            , {sqlite_null(allyunit_x._agent_credit)} 
            , {sqlite_null(allyunit_x._agent_debt)}
            , {sqlite_null(allyunit_x._agent_agenda_credit)}
            , {sqlite_null(allyunit_x._agent_agenda_debt)}
            , {sqlite_null(allyunit_x._agent_agenda_ratio_credit)}
            , {sqlite_null(allyunit_x._agent_agenda_ratio_debt)}
            , {sqlite_bool(allyunit_x._creditor_active)}
            , {sqlite_bool(allyunit_x._debtor_active)}
        )
        ;
        """
    # x_str = sqlstr.replace("\n        ", "")
    # print(f"{x_str=}")
    return sqlstr


@dataclass
class LedgerUnit:
    agent_name: str
    ally_name: str
    _agent_credit: float
    _agent_debt: float
    _agent_agenda_credit: float
    _agent_agenda_debt: float
    _agent_agenda_ratio_credit: float
    _agent_agenda_ratio_debt: float
    _creditor_active: float
    _debtor_active: float


def get_ledger_dict(db_conn: Connection, payer_name: str) -> dict[str:LedgerUnit]:
    sqlstr = f"""
        SELECT 
          agent_name
        , ally_name
        , _agent_credit
        , _agent_debt
        , _agent_agenda_credit
        , _agent_agenda_debt
        , _agent_agenda_ratio_credit
        , _agent_agenda_ratio_debt
        , _creditor_active
        , _debtor_active
        FROM ledger
        WHERE agent_name = '{payer_name}' 
        ;
    """
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        ledger_x = LedgerUnit(
            agent_name=row[0],
            ally_name=row[1],
            _agent_credit=row[2],
            _agent_debt=row[3],
            _agent_agenda_credit=row[4],
            _agent_agenda_debt=row[5],
            _agent_agenda_ratio_credit=row[6],
            _agent_agenda_ratio_debt=row[7],
            _creditor_active=row[8],
            _debtor_active=row[9],
        )
        dict_x[ledger_x.ally_name] = ledger_x
    return dict_x


@dataclass
class RiverLedgerUnit:
    agent_name: str
    currency_onset: float
    currency_cease: float
    _ledgers: dict[str:LedgerUnit]
    river_tree_level: int
    flow_num: int

    def get_range(self):
        return self.currency_cease - self.currency_onset


def get_river_ledger_unit(
    db_conn: Connection, river_flow_x: RiverFlowUnit = None
) -> RiverLedgerUnit:
    ledger_x = get_ledger_dict(db_conn, river_flow_x.dst_name)
    river_ledger_unit = RiverLedgerUnit(
        agent_name=river_flow_x.dst_name,
        currency_onset=river_flow_x.currency_start,
        currency_cease=river_flow_x.currency_close,
        _ledgers=ledger_x,
        river_tree_level=river_flow_x.river_tree_level,
        flow_num=river_flow_x.flow_num,
    )
    return river_ledger_unit


def get_create_table_if_not_exist_sqlstrs() -> list[str]:
    list_x = []
    list_x.append(get_agent_table_create_sqlstr())
    list_x.append(get_ledger_table_create_sqlstr())
    list_x.append(get_river_flow_table_create_sqlstr())
    list_x.append(get_river_bucket_table_create_sqlstr())
    list_x.append(get_river_tally_table_create_sqlstr())
    return list_x
