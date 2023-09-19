from src.contract.contract import ContractUnit
from src.contract.member import MemberUnit
from src.contract.road import get_road_without_root_node
from src.economy.y_func import sqlite_bool, sqlite_null
from src.contract.road import Road
from dataclasses import dataclass
from sqlite3 import Connection


def get_table_count_sqlstr(table_name: str) -> str:
    return f"SELECT COUNT(*) FROM {table_name}"


def get_river_flow_table_delete_sqlstr(currency_contract_name: str) -> str:
    return f"""
        DELETE FROM river_flow
        WHERE currency_name = '{currency_contract_name}' 
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
        , FOREIGN KEY(currency_name) REFERENCES contractunits(name)
        , FOREIGN KEY(src_name) REFERENCES contractunits(name)
        , FOREIGN KEY(dst_name) REFERENCES contractunits(name)
        )
        ;
    """


@dataclass
class RiverFlowUnit:
    currency_contract_name: str
    src_name: str
    dst_name: str
    currency_start: float
    currency_close: float
    flow_num: int
    parent_flow_num: int
    river_tree_level: int

    def flow_returned(self) -> bool:
        return self.currency_contract_name == self.dst_name


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
          '{river_flow_x.currency_contract_name}'
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
    db_conn: str, currency_contract_name: str
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
        WHERE currency_name = '{currency_contract_name}' 
        ;
    """
    dict_x = {}
    cursor_x = db_conn.cursor()
    results_cursor_x = cursor_x.execute(sqlstr)
    results_x = results_cursor_x.fetchall()

    for count_x, row in enumerate(results_x):
        river_flow_x = RiverFlowUnit(
            currency_contract_name=row[0],
            src_name=row[1],
            dst_name=row[2],
            currency_start=row[3],
            currency_close=row[4],
            flow_num=row[5],
            parent_flow_num=row[6],
            river_tree_level=row[7],
        )
        dict_x[count_x] = river_flow_x
    return dict_x


def get_river_bucket_table_delete_sqlstr(currency_contract_name: str) -> str:
    return f"""
        DELETE FROM river_bucket
        WHERE currency_name = '{currency_contract_name}' 
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
        , FOREIGN KEY(currency_name) REFERENCES contractunits(name)
        , FOREIGN KEY(dst_name) REFERENCES contractunits(name)
        )
    ;
    """


def get_river_bucket_table_insert_sqlstr(currency_contract_name: str) -> str:
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
            WHERE currency_name = '{currency_contract_name}' and dst_name = currency_name 
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
    db_conn: Connection, currency_contract_name: str
) -> dict[str:RiverBucketUnit]:
    sqlstr = f"""
        SELECT
          currency_name
        , dst_name
        , bucket_num
        , curr_start
        , curr_close
        FROM river_bucket
        WHERE currency_name = '{currency_contract_name}'
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


def get_river_tmember_table_delete_sqlstr(currency_contract_name: str) -> str:
    return f"""
        DELETE FROM river_tmember
        WHERE currency_name = '{currency_contract_name}' 
        ;
    """


def get_river_tmember_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS river_tmember (
          currency_name VARCHAR(255) NOT NULL
        , tax_name VARCHAR(255) NOT NULL
        , tax_total FLOAT NOT NULL
        , debt FLOAT NULL
        , tax_diff FLOAT NULL
        , FOREIGN KEY(currency_name) REFERENCES contractunits(name)
        , FOREIGN KEY(tax_name) REFERENCES contractunits(name)
        )
    ;
    """


def get_river_tmember_table_insert_sqlstr(currency_contract_name: str) -> str:
    return f"""
        INSERT INTO river_tmember (
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
        , l._contract_agenda_ratio_debt
        , l._contract_agenda_ratio_debt - SUM(rt.currency_close-rt.currency_start)
        FROM river_flow rt
        LEFT JOIN ledger l ON l.contract_name = rt.currency_name AND l.member_name = rt.src_name
        WHERE rt.currency_name='{currency_contract_name}' and rt.dst_name=rt.currency_name
        GROUP BY rt.currency_name, rt.src_name
        ;
    """


@dataclass
class RiverTmemberUnit:
    currency_name: str
    tax_name: str
    tax_total: float
    debt: float
    tax_diff: float


def get_river_tmember_dict(
    db_conn: Connection, currency_contract_name: str
) -> dict[str:RiverTmemberUnit]:
    sqlstr = f"""
        SELECT
          currency_name
        , tax_name
        , tax_total
        , debt
        , tax_diff
        FROM river_tmember
        WHERE currency_name = '{currency_contract_name}'
        ;
    """
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        river_tmember_x = RiverTmemberUnit(
            currency_name=row[0],
            tax_name=row[1],
            tax_total=row[2],
            debt=row[3],
            tax_diff=row[4],
        )
        dict_x[river_tmember_x.tax_name] = river_tmember_x
    return dict_x


def get_contract_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS contractunits (
          name VARCHAR(255) PRIMARY KEY ASC
        , UNIQUE(name)
        )
    ;
    """


def get_contract_table_insert_sqlstr(contract_x: ContractUnit) -> str:
    return f"""
        INSERT INTO contractunits (
            name
            )
        VALUES (
            '{contract_x._owner}' 
        )
        ;
        """


def get_ledger_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS ledger (
          contract_name INTEGER 
        , member_name INTEGER
        , _contract_credit FLOAT
        , _contract_debt FLOAT
        , _contract_agenda_credit FLOAT
        , _contract_agenda_debt FLOAT
        , _contract_agenda_ratio_credit FLOAT
        , _contract_agenda_ratio_debt FLOAT
        , _creditor_active INT
        , _debtor_active INT
        , FOREIGN KEY(contract_name) REFERENCES contractunits(name)
        , FOREIGN KEY(member_name) REFERENCES contractunits(name)
        , UNIQUE(contract_name, member_name)
        )
    ;
    """


def get_ledger_table_insert_sqlstr(
    contract_x: ContractUnit, memberunit_x: MemberUnit
) -> str:
    return f"""
        INSERT INTO ledger (
              contract_name
            , member_name
            , _contract_credit
            , _contract_debt
            , _contract_agenda_credit
            , _contract_agenda_debt
            , _contract_agenda_ratio_credit
            , _contract_agenda_ratio_debt
            , _creditor_active
            , _debtor_active
            )
        VALUES (
            '{contract_x._owner}' 
            , '{memberunit_x.name}'
            , {sqlite_null(memberunit_x._contract_credit)} 
            , {sqlite_null(memberunit_x._contract_debt)}
            , {sqlite_null(memberunit_x._contract_agenda_credit)}
            , {sqlite_null(memberunit_x._contract_agenda_debt)}
            , {sqlite_null(memberunit_x._contract_agenda_ratio_credit)}
            , {sqlite_null(memberunit_x._contract_agenda_ratio_debt)}
            , {sqlite_bool(memberunit_x._creditor_active)}
            , {sqlite_bool(memberunit_x._debtor_active)}
        )
        ;
        """


@dataclass
class LedgerUnit:
    contract_name: str
    member_name: str
    _contract_credit: float
    _contract_debt: float
    _contract_agenda_credit: float
    _contract_agenda_debt: float
    _contract_agenda_ratio_credit: float
    _contract_agenda_ratio_debt: float
    _creditor_active: float
    _debtor_active: float


def get_ledger_dict(db_conn: Connection, payer_name: str) -> dict[str:LedgerUnit]:
    sqlstr = f"""
        SELECT 
          contract_name
        , member_name
        , _contract_credit
        , _contract_debt
        , _contract_agenda_credit
        , _contract_agenda_debt
        , _contract_agenda_ratio_credit
        , _contract_agenda_ratio_debt
        , _creditor_active
        , _debtor_active
        FROM ledger
        WHERE contract_name = '{payer_name}' 
        ;
    """
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        ledger_x = LedgerUnit(
            contract_name=row[0],
            member_name=row[1],
            _contract_credit=row[2],
            _contract_debt=row[3],
            _contract_agenda_credit=row[4],
            _contract_agenda_debt=row[5],
            _contract_agenda_ratio_credit=row[6],
            _contract_agenda_ratio_debt=row[7],
            _creditor_active=row[8],
            _debtor_active=row[9],
        )
        dict_x[ledger_x.member_name] = ledger_x
    return dict_x


@dataclass
class RiverLedgerUnit:
    contract_name: str
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
    return RiverLedgerUnit(
        contract_name=river_flow_x.dst_name,
        currency_onset=river_flow_x.currency_start,
        currency_cease=river_flow_x.currency_close,
        _ledgers=ledger_x,
        river_tree_level=river_flow_x.river_tree_level,
        flow_num=river_flow_x.flow_num,
    )


def get_idea_catalog_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS idea_catalog (
          contract_name VARCHAR(255) NOT NULL
        , idea_road VARCHAR(1000) NOT NULL
        )
        ;
    """


def get_idea_catalog_table_count(db_conn: Connection, contract_name: str) -> str:
    sqlstr = f"""
        {get_table_count_sqlstr("idea_catalog")} WHERE contract_name = '{contract_name}'
        ;
    """
    results = db_conn.execute(sqlstr)
    contract_row_count = 0
    for row in results.fetchall():
        contract_row_count = row[0]
    return contract_row_count


@dataclass
class IdeaCatalog:
    contract_name: str
    idea_road: str


def get_idea_catalog_table_insert_sqlstr(
    idea_catalog: IdeaCatalog,
) -> str:
    # return f"""INSERT INTO idea_catalog (contract_name, idea_road) VALUES ('{idea_catalog.contract_name}', '{idea_catalog.idea_road}');"""
    return f"""
        INSERT INTO idea_catalog (
          contract_name
        , idea_road
        )
        VALUES (
          '{idea_catalog.contract_name}'
        , '{get_road_without_root_node(idea_catalog.idea_road)}'
        )
        ;
    """


def get_idea_catalog_dict(db_conn: Connection, search_road: Road = None):
    if search_road is None:
        where_clause = ""
    else:
        search_road_without_root_node = get_road_without_root_node(search_road)
        where_clause = f"WHERE idea_road = '{search_road_without_root_node}'"
    sqlstr = f"""
        SELECT 
          contract_name
        , idea_road
        FROM idea_catalog
        {where_clause}
        ;
    """
    results = db_conn.execute(sqlstr)

    dict_x = {}
    for row in results.fetchall():
        idea_catalog_x = IdeaCatalog(contract_name=row[0], idea_road=row[1])
        dict_key = f"{idea_catalog_x.contract_name} {idea_catalog_x.idea_road}"
        dict_x[dict_key] = idea_catalog_x
    return dict_x


def get_acptfact_catalog_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS acptfact_catalog (
          contract_name VARCHAR(255) NOT NULL
        , base VARCHAR(1000) NOT NULL
        , pick VARCHAR(1000) NOT NULL
        )
        ;
    """


def get_acptfact_catalog_table_count(db_conn: Connection, contract_name: str) -> str:
    sqlstr = f"""
        {get_table_count_sqlstr("acptfact_catalog")} WHERE contract_name = '{contract_name}'
        ;
    """
    results = db_conn.execute(sqlstr)
    contract_row_count = 0
    for row in results.fetchall():
        contract_row_count = row[0]
    return contract_row_count


@dataclass
class AcptFactCatalog:
    contract_name: str
    base: str
    pick: str


def get_acptfact_catalog_table_insert_sqlstr(
    acptfact_catalog: AcptFactCatalog,
) -> str:
    return f"""
        INSERT INTO acptfact_catalog (
          contract_name
        , base
        , pick
        )
        VALUES (
          '{acptfact_catalog.contract_name}'
        , '{acptfact_catalog.base}'
        , '{acptfact_catalog.pick}'
        )
        ;
    """


def get_groupunit_catalog_table_create_sqlstr() -> str:
    return """
        CREATE TABLE IF NOT EXISTS groupunit_catalog (
          contract_name VARCHAR(255) NOT NULL
        , groupunit_name VARCHAR(1000) NOT NULL
        , memberlinks_set_by_economy_road VARCHAR(1000) NULL
        )
        ;
    """


def get_groupunit_catalog_table_count(db_conn: Connection, contract_name: str) -> str:
    sqlstr = f"""
        {get_table_count_sqlstr("groupunit_catalog")} WHERE contract_name = '{contract_name}'
        ;
    """
    results = db_conn.execute(sqlstr)
    contract_row_count = 0
    for row in results.fetchall():
        contract_row_count = row[0]
    return contract_row_count


@dataclass
class GroupUnitCatalog:
    contract_name: str
    groupunit_name: str
    memberlinks_set_by_economy_road: str


def get_groupunit_catalog_table_insert_sqlstr(
    groupunit_catalog: GroupUnitCatalog,
) -> str:
    return f"""
        INSERT INTO groupunit_catalog (
          contract_name
        , groupunit_name
        , memberlinks_set_by_economy_road
        )
        VALUES (
          '{groupunit_catalog.contract_name}'
        , '{groupunit_catalog.groupunit_name}'
        , '{groupunit_catalog.memberlinks_set_by_economy_road}'
        )
        ;
    """


def get_groupunit_catalog_dict(db_conn: Connection) -> dict[str:GroupUnitCatalog]:
    sqlstr = """
        SELECT 
          contract_name
        , groupunit_name
        , memberlinks_set_by_economy_road
        FROM groupunit_catalog
        ;
    """
    results = db_conn.execute(sqlstr)

    dict_x = {}
    for row in results.fetchall():
        groupunit_catalog_x = GroupUnitCatalog(
            contract_name=row[0],
            groupunit_name=row[1],
            memberlinks_set_by_economy_road=row[2],
        )
        dict_key = (
            f"{groupunit_catalog_x.contract_name} {groupunit_catalog_x.groupunit_name}"
        )
        dict_x[dict_key] = groupunit_catalog_x
    return dict_x


def get_create_table_if_not_exist_sqlstrs() -> list[str]:
    list_x = [get_contract_table_create_sqlstr()]
    list_x.append(get_acptfact_catalog_table_create_sqlstr())
    list_x.append(get_idea_catalog_table_create_sqlstr())
    list_x.append(get_ledger_table_create_sqlstr())
    list_x.append(get_river_flow_table_create_sqlstr())
    list_x.append(get_river_bucket_table_create_sqlstr())
    list_x.append(get_river_tmember_table_create_sqlstr())
    list_x.append(get_groupunit_catalog_table_create_sqlstr())
    return list_x


def get_db_tables(bank_conn: Connection):
    sqlstr = "SELECT name FROM sqlite_schema WHERE type='table' ORDER BY name;"
    results = bank_conn.execute(sqlstr)

    return {row[0]: 1 for row in results}
