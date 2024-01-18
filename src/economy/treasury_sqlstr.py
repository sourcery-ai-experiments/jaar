from src.agenda.agenda import AgendaUnit, PartyUnit, RoadUnit, PersonID, PartyID
from src._prime.road import create_road_without_root_node
from src.tools.sqlite import sqlite_bool, sqlite_null, sqlite_text, sqlite_to_python
from dataclasses import dataclass
from sqlite3 import Connection


def get_river_score_select_sqlstr(currency_master):
    return f"""
SELECT 
  currency_master
, src_healer
, SUM(reach_curr_close - reach_curr_start) range_sum
FROM river_reach
WHERE currency_master = '{currency_master}'
GROUP BY currency_master, src_healer
ORDER BY range_sum DESC
;
"""


def get_river_reach_table_final_insert_sqlstr(currency_master: PersonID) -> str:
    reach_final_sqlstr = get_river_reach_table_final_select_sqlstr(currency_master)
    return get_river_reach_table_insert_sqlstr(reach_final_sqlstr)


def get_river_reach_table_insert_sqlstr(select_query: str) -> str:
    return f"""
INSERT INTO river_reach (currency_master, src_healer, set_num, reach_curr_start, reach_curr_close)
{select_query}
;
"""


def get_river_reach_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS river_reach (
  currency_master VARCHAR(255) NOT NULL
, src_healer VARCHAR(255) NOT NULL
, set_num INT NOT NULL
, reach_curr_start FLOAT NOT NULL
, reach_curr_close FLOAT NOT NULL
, FOREIGN KEY(currency_master) REFERENCES agendaunit(healer)
, FOREIGN KEY(src_healer) REFERENCES agendaunit(healer)
)
;
"""


def get_river_reach_table_touch_select_sqlstr(currency_master: PersonID) -> str:
    return f"""
    SELECT 
    block.currency_master
    , block.src_healer src
    , block.dst_healer dst
    , CASE 
        WHEN block.currency_start < circle.curr_start 
            AND block.currency_close > circle.curr_start
            AND block.currency_close <= circle.curr_close
            THEN circle.curr_start --'leftside' 
        WHEN block.currency_start >= circle.curr_start 
            AND block.currency_start < circle.curr_close
            AND block.currency_close > circle.curr_close
            THEN block.currency_start --'rightside' 
        WHEN block.currency_start < circle.curr_start 
            AND block.currency_close > circle.curr_close
            THEN circle.curr_start --'outside' 
        WHEN block.currency_start >= circle.curr_start 
            AND block.currency_close <= circle.curr_close
            THEN block.currency_start --'inside' 
            END reach_start
    , CASE 
        WHEN block.currency_start < circle.curr_start 
            AND block.currency_close > circle.curr_start
            AND block.currency_close <= circle.curr_close
            THEN block.currency_close --'leftside' 
        WHEN block.currency_start >= circle.curr_start 
            AND block.currency_start < circle.curr_close
            AND block.currency_close > circle.curr_close
            THEN circle.curr_close --'rightside' 
        WHEN block.currency_start < circle.curr_start 
            AND block.currency_close > circle.curr_close
            THEN circle.curr_close --'outside' 
        WHEN block.currency_start >= circle.curr_start 
            AND block.currency_close <= circle.curr_close
            THEN block.currency_close --'inside' 
            END reach_close
    FROM river_block block
    JOIN river_circle circle on 
            (block.currency_start < circle.curr_start 
            AND block.currency_close > circle.curr_close)
        OR     (block.currency_start >= circle.curr_start 
            AND block.currency_close <= circle.curr_close)
        OR     (block.currency_start < circle.curr_start 
            AND block.currency_close > circle.curr_start
            AND block.currency_close <= circle.curr_close)
        OR     (block.currency_start >= circle.curr_start 
            AND block.currency_start < circle.curr_close
            AND block.currency_close > circle.curr_close)
    WHERE block.currency_master = '{currency_master}'
        AND block.src_healer != block.currency_master
    ORDER BY 
    block.src_healer
    , block.dst_healer
    , block.currency_start
    , block.currency_close
"""


def get_river_reach_table_final_select_sqlstr(currency_master: PersonID) -> str:
    return f"""
WITH reach_inter(curr_mstr, src, dst, reach_start, reach_close) AS (
{get_river_reach_table_touch_select_sqlstr(currency_master)}
),
reach_order(
  curr_mstr
, src
, prev_src
, src_step
, reach_start
, prev_start
, range_step
, reach_close
, prev_close
) AS (
    SELECT 
    reach_inter.curr_mstr
    , reach_inter.src
    , IFNULL(
        LAG(reach_inter.src, 1) OVER(ORDER BY 
        reach_inter.src
        , reach_inter.dst
        , reach_inter.reach_start
        , reach_inter.reach_close
        )
      , reach_inter.src) prev_src
    , CASE 
        WHEN 
          IFNULL(
            LAG(reach_inter.src, 1) OVER(ORDER BY 
            reach_inter.src
            , reach_inter.dst
            , reach_inter.reach_start
            , reach_inter.reach_close
            )
          , reach_inter.src) 
          = reach_inter.src
        THEN 0
        ELSE 1
        END src_step
    , reach_inter.reach_start
    , IFNULL(
        LAG(reach_start, 1) OVER(ORDER BY 
        reach_inter.src
        , reach_inter.dst
        , reach_inter.reach_start
        , reach_inter.reach_close
        ) 
      , reach_start) prev_start
    , CASE
      WHEN
        IFNULL(
        LAG(reach_close, 1) OVER(ORDER BY 
        reach_inter.src
        , reach_inter.dst
        , reach_inter.reach_start
        , reach_inter.reach_close
        ) 
      , reach_close) < reach_inter.reach_start
      THEN 1
      ELSE 0
      END range_step
    , reach_inter.reach_close
    , IFNULL(
        LAG(reach_close, 1) OVER(ORDER BY 
        reach_inter.src
        , reach_inter.dst
        , reach_inter.reach_start
        , reach_inter.reach_close
        ) 
      , reach_close) prev_close
    FROM reach_inter
) 
, reach_step (  
  curr_mstr
, src
, prev_src
, src_step
, range_step
, change_step
, prev_start
, prev_close
, reach_start
, reach_close
) AS (
    SELECT
    curr_mstr
    , src
    , prev_src
    , src_step
    , range_step
    , CASE 
        WHEN src_step =1 AND range_step =1 
        THEN 1
        ELSE src_step + range_step
        END change_step
    , prev_start
    , prev_close
    , reach_start
    , reach_close
    FROM reach_order
)
, reach_sets_num (  
  curr_mstr
, src
, set_num
, prev_start
, prev_close
, reach_start
, reach_close
) AS (
    SELECT
      curr_mstr
    , src
    , SUM(change_step) OVER (ORDER BY src, reach_start, reach_close) set_num
    , prev_start
    , prev_close
    , reach_start
    , reach_close
    FROM reach_step
)
SELECT 
  curr_mstr
, src
, set_num 
, MIN(reach_start) reach_start
, MAX(reach_close) reach_close
FROM reach_sets_num
GROUP BY curr_mstr, src, set_num
"""


def get_table_count_sqlstr(table_name: str) -> str:
    return f"SELECT COUNT(*) FROM {table_name}"


# river_block
def get_river_block_table_delete_sqlstr(currency_agenda_healer: str) -> str:
    return f"""
DELETE FROM river_block
WHERE currency_master = '{currency_agenda_healer}' 
;
"""


def get_river_block_table_create_sqlstr() -> str:
    """Table that stores each block of currency from src_healer to dst_healer.
    currency_master: every currency starts with a healer as credit source
        All river blocks with destination currency healer stop. For that currency range
        there is no more block
    src_healer: healer that is source of credit
    dst_healer: healer that is destination of credit.
    currency_start: range of currency influenced start
    currency_close: range of currency influenced close
    block_num: the sequence number of transactions before this one
    parent_block_num: river blocks can have multiple children but only one parent
    river_tree_level: how many ancestors between currency_master first credit outblock
        and this river block
    JSchalk 24 Oct 2023
    """
    return """
CREATE TABLE IF NOT EXISTS river_block (
  currency_master VARCHAR(255) NOT NULL
, src_healer VARCHAR(255) NOT NULL
, dst_healer VARCHAR(255) NOT NULL
, currency_start FLOAT NOT NULL
, currency_close FLOAT NOT NULL
, block_num INT NOT NULL
, parent_block_num INT NULL
, river_tree_level INT NOT NULL
, FOREIGN KEY(currency_master) REFERENCES agendaunit(healer)
, FOREIGN KEY(src_healer) REFERENCES agendaunit(healer)
, FOREIGN KEY(dst_healer) REFERENCES agendaunit(healer)
)
;
"""


@dataclass
class RiverBlockUnit:
    currency_agenda_healer: str
    src_healer: str
    dst_healer: str
    currency_start: float
    currency_close: float
    block_num: int
    parent_block_num: int
    river_tree_level: int

    def block_returned(self) -> bool:
        return self.currency_agenda_healer == self.dst_healer


def get_river_block_table_insert_sqlstr(
    river_block_x: RiverBlockUnit,
) -> str:
    return f"""
INSERT INTO river_block (
  currency_master
, src_healer
, dst_healer
, currency_start 
, currency_close
, block_num
, parent_block_num
, river_tree_level
)
VALUES (
  '{river_block_x.currency_agenda_healer}'
, '{river_block_x.src_healer}'
, '{river_block_x.dst_healer}'
, {sqlite_null(river_block_x.currency_start)}
, {sqlite_null(river_block_x.currency_close)}
, {river_block_x.block_num}
, {sqlite_null(river_block_x.parent_block_num)}
, {river_block_x.river_tree_level}
)
;
"""


def get_river_block_dict(
    db_conn: str, currency_agenda_healer: str
) -> dict[str:RiverBlockUnit]:
    sqlstr = f"""
SELECT 
  currency_master
, src_healer
, dst_healer
, currency_start
, currency_close
, block_num
, parent_block_num
, river_tree_level
FROM river_block
WHERE currency_master = '{currency_agenda_healer}' 
;
"""
    dict_x = {}
    cursor_x = db_conn.cursor()
    results_cursor_x = cursor_x.execute(sqlstr)
    results_x = results_cursor_x.fetchall()

    for count_x, row in enumerate(results_x):
        river_block_x = RiverBlockUnit(
            currency_agenda_healer=row[0],
            src_healer=row[1],
            dst_healer=row[2],
            currency_start=row[3],
            currency_close=row[4],
            block_num=row[5],
            parent_block_num=row[6],
            river_tree_level=row[7],
        )
        dict_x[count_x] = river_block_x
    return dict_x


# river_circle
def get_river_circle_table_delete_sqlstr(currency_agenda_healer: str) -> str:
    return f"""
DELETE FROM river_circle
WHERE currency_master = '{currency_agenda_healer}' 
;
"""


def get_river_circle_table_create_sqlstr() -> str:
    """Check get_river_circle_table_insert_sqlstrget_river_circle_table_insert_sqlstr doc string"""
    return """
CREATE TABLE IF NOT EXISTS river_circle (
  currency_master VARCHAR(255) NOT NULL
, dst_healer VARCHAR(255) NOT NULL
, circle_num INT NOT NULL
, curr_start FLOAT NOT NULL
, curr_close FLOAT NOT NULL
, FOREIGN KEY(currency_master) REFERENCES agendaunit(healer)
, FOREIGN KEY(dst_healer) REFERENCES agendaunit(healer)
)
;
"""


def get_river_circle_table_insert_sqlstr(currency_agenda_healer: str) -> str:
    """Table that stores discontinuous currency ranges that circle back from source (currency_master)
    to final destination (currency_master)
    Columns
    currency_master: every currency starts with a healer as credit source
    dst_healer: healer that is destination of credit.
        All river blocks with destination healer are summed into ranges called circles
    circle_num: all destination healer circles have a unique number. (sequential 0, 1, 2...)
    currency_start: range of circle start
    currency_close: range of circle close
    JSchalk 24 Oct 2023
    """
    return f"""
INSERT INTO river_circle (
  currency_master
, dst_healer
, circle_num
, curr_start
, curr_close
)
SELECT 
  currency_master
, dst_healer
, currency_circle_num
, min(currency_start) currency_circle_start
, max(currency_close) currency_circle_close
FROM  (
SELECT *, SUM(step) OVER (ORDER BY currency_start) AS currency_circle_num
FROM  (
    SELECT 
    CASE 
    WHEN lag(currency_close) OVER (ORDER BY currency_start) < currency_start 
        OR lag(currency_close) OVER (ORDER BY currency_start) = NULL 
    THEN 1
    ELSE 0
    END AS step
    , *
    FROM  river_block
    WHERE currency_master = '{currency_agenda_healer}' and dst_healer = currency_master 
    ) b
) c
GROUP BY currency_master, dst_healer, currency_circle_num
ORDER BY currency_circle_start
;
"""


@dataclass
class RiverCircleUnit:
    currency_master: str
    dst_healer: str
    circle_num: int
    curr_start: float
    curr_close: float


def get_river_circle_dict(
    db_conn: Connection, currency_agenda_healer: str
) -> dict[str:RiverCircleUnit]:
    sqlstr = f"""
SELECT
  currency_master
, dst_healer
, circle_num
, curr_start
, curr_close
FROM river_circle
WHERE currency_master = '{currency_agenda_healer}'
;
"""
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        river_circle_x = RiverCircleUnit(
            currency_master=row[0],
            dst_healer=row[1],
            circle_num=row[2],
            curr_start=row[3],
            curr_close=row[4],
        )
        dict_x[river_circle_x.circle_num] = river_circle_x
    return dict_x


# PartyTreasuryUnit
@dataclass
class PartyTreasuryUnit:
    currency_master: str
    tax_healer: str
    tax_total: float
    debt: float
    tax_diff: float
    credit_score: float
    voice_rank: int


def get_partytreasuryunit_dict(
    db_conn: Connection, currency_agenda_healer: str
) -> dict[str:PartyTreasuryUnit]:
    sqlstr = f"""
SELECT
  agenda_healer currency_master
, pid tax_healer
, _treasury_tax_paid tax_total
, _agenda_intent_ratio_debt debt
, (_agenda_intent_ratio_debt - _treasury_tax_paid) tax_diff
FROM partyunit
WHERE currency_master = '{currency_agenda_healer}'
    AND _treasury_tax_paid IS NOT NULL
;
"""
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        partytreasuryunit_x = PartyTreasuryUnit(
            currency_master=row[0],
            tax_healer=row[1],
            tax_total=row[2],
            debt=row[3],
            tax_diff=row[4],
            credit_score=None,
            voice_rank=None,
        )
        dict_x[partytreasuryunit_x.tax_healer] = partytreasuryunit_x
    return dict_x


# agenda
def get_agendaunit_table_create_sqlstr() -> str:
    """Create table that references the pid of every agenda. The healer pip of the one running that agenda's clerk."""
    return """
CREATE TABLE IF NOT EXISTS agendaunit (
  healer VARCHAR(255) PRIMARY KEY ASC
, rational INT NULL
, UNIQUE(healer)
)
;
"""


def get_agendaunit_table_insert_sqlstr(x_agenda: AgendaUnit) -> str:
    return f"""
INSERT INTO agendaunit (
  healer
, rational
)
VALUES (
  '{x_agenda._agent_id}' 
, NULL
)
;
"""


def get_agendaunits_select_sqlstr():
    return """
SELECT 
  healer
, rational
FROM agendaunit
;
"""


@dataclass
class AgendaTreasuryUnit:
    healer: PersonID
    rational: bool


def get_agendatreasuryunits_dict(
    db_conn: Connection,
) -> dict[PersonID:AgendaTreasuryUnit]:
    results = db_conn.execute(get_agendaunits_select_sqlstr())
    dict_x = {}
    for row in results.fetchall():
        x_agendatreasuryunit = AgendaTreasuryUnit(
            healer=row[0], rational=sqlite_to_python(row[1])
        )
        dict_x[x_agendatreasuryunit.healer] = x_agendatreasuryunit
    return dict_x


def get_agendaunit_update_sqlstr(agenda: AgendaUnit) -> str:
    return f"""
UPDATE agendaunit
SET rational = {sqlite_text(agenda._rational)}
WHERE healer = '{agenda._agent_id}'
;
"""


# partyunit
def get_partyunit_table_create_sqlstr() -> str:
    """Create table that holds the starting river metrics for every agenda's party. All the metrics."""
    return """
CREATE TABLE IF NOT EXISTS partyunit (
  agenda_healer VARCHAR(255) NOT NULL 
, pid VARCHAR(255) NOT NULL
, _agenda_credit FLOAT
, _agenda_debt FLOAT
, _agenda_intent_credit FLOAT
, _agenda_intent_debt FLOAT
, _agenda_intent_ratio_credit FLOAT
, _agenda_intent_ratio_debt FLOAT
, _creditor_active INT
, _debtor_active INT
, _treasury_tax_paid FLOAT
, _treasury_tax_diff FLOAT
, _treasury_credit_score FLOAT
, _treasury_voice_rank INT
, _treasury_voice_hx_lowest_rank INT
, _title VARCHAR(255)
, FOREIGN KEY(agenda_healer) REFERENCES agendaunit(healer)
, FOREIGN KEY(pid) REFERENCES agendaunit(healer)
, UNIQUE(agenda_healer, pid)
)
;
"""


def get_partyunit_table_update_treasury_tax_paid_sqlstr(
    currency_agenda_healer: PersonID,
) -> str:
    return f"""
UPDATE partyunit
SET _treasury_tax_paid = (
    SELECT SUM(block.currency_close-block.currency_start) 
    FROM river_block block
    WHERE block.currency_master='{currency_agenda_healer}' 
        AND block.dst_healer=block.currency_master
        AND block.src_healer = partyunit.pid
    )
WHERE EXISTS (
    SELECT block.currency_close
    FROM river_block block
    WHERE partyunit.agenda_healer='{currency_agenda_healer}' 
        AND partyunit.pid = block.dst_healer
)
;
"""


def get_partyunit_table_update_credit_score_sqlstr(
    currency_agenda_healer: PersonID,
) -> str:
    return f"""
UPDATE partyunit
SET _treasury_credit_score = (
    SELECT SUM(reach_curr_close - reach_curr_start) range_sum
    FROM river_reach reach
    WHERE reach.currency_master = partyunit.agenda_healer
        AND reach.src_healer = partyunit.pid
    )
WHERE partyunit.agenda_healer = '{currency_agenda_healer}'
;
"""


def get_partyunit_table_update_treasury_voice_rank_sqlstr(
    agenda_healer: PersonID,
) -> str:
    return f"""
UPDATE partyunit
SET _treasury_voice_rank = 
    (
    SELECT rn
    FROM (
        SELECT p2.pid
        , row_number() over (order by p2._treasury_credit_score DESC) rn
        FROM partyunit p2
        WHERE p2.agenda_healer = '{agenda_healer}'
    ) p3
    WHERE p3.pid = partyunit.pid AND partyunit.agenda_healer = '{agenda_healer}'
    )
WHERE partyunit.agenda_healer = '{agenda_healer}'
;
"""


def get_partyunit_table_insert_sqlstr(
    x_agenda: AgendaUnit, x_partyunit: PartyUnit
) -> str:
    """Create table that holds a the output credit metrics."""
    return f"""
INSERT INTO partyunit (
  agenda_healer
, pid
, _agenda_credit
, _agenda_debt
, _agenda_intent_credit
, _agenda_intent_debt
, _agenda_intent_ratio_credit
, _agenda_intent_ratio_debt
, _creditor_active
, _debtor_active
, _treasury_tax_paid
, _treasury_tax_diff
, _treasury_credit_score
, _treasury_voice_rank
, _treasury_voice_hx_lowest_rank
, _title
)
VALUES (
  '{x_agenda._agent_id}' 
, '{x_partyunit.pid}'
, {sqlite_null(x_partyunit._agenda_credit)} 
, {sqlite_null(x_partyunit._agenda_debt)}
, {sqlite_null(x_partyunit._agenda_intent_credit)}
, {sqlite_null(x_partyunit._agenda_intent_debt)}
, {sqlite_null(x_partyunit._agenda_intent_ratio_credit)}
, {sqlite_null(x_partyunit._agenda_intent_ratio_debt)}
, {sqlite_bool(x_partyunit._creditor_active)}
, {sqlite_bool(x_partyunit._debtor_active)}
, {sqlite_null(x_partyunit._treasury_tax_paid)}
, {sqlite_null(x_partyunit._treasury_tax_diff)}
, {sqlite_null(x_partyunit._treasury_credit_score)}
, {sqlite_null(x_partyunit._treasury_voice_rank)}
, {sqlite_null(x_partyunit._treasury_voice_hx_lowest_rank)}
, '{x_partyunit._title}'
)
;
"""


@dataclass
class PartyDBUnit(PartyUnit):
    agenda_healer: str = None


def get_partyview_dict(
    db_conn: Connection, payer_healer: PersonID
) -> dict[PartyID:PartyDBUnit]:
    sqlstr = f"""
SELECT 
  agenda_healer
, pid
, _agenda_credit
, _agenda_debt
, _agenda_intent_credit
, _agenda_intent_debt
, _agenda_intent_ratio_credit
, _agenda_intent_ratio_debt
, _creditor_active
, _debtor_active
, _treasury_tax_paid
, _treasury_tax_diff
, _treasury_credit_score
, _treasury_voice_rank
, _treasury_voice_hx_lowest_rank
, _title
FROM partyunit
WHERE agenda_healer = '{payer_healer}' 
;
"""
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        partyview_x = PartyDBUnit(
            agenda_healer=row[0],
            pid=row[1],
            _agenda_credit=row[2],
            _agenda_debt=row[3],
            _agenda_intent_credit=row[4],
            _agenda_intent_debt=row[5],
            _agenda_intent_ratio_credit=row[6],
            _agenda_intent_ratio_debt=row[7],
            _creditor_active=row[8],
            _debtor_active=row[9],
            _treasury_tax_paid=row[10],
            _treasury_tax_diff=row[11],
            _treasury_credit_score=row[12],
            _treasury_voice_rank=row[13],
            _treasury_voice_hx_lowest_rank=row[14],
            _title=row[15],
        )
        dict_x[partyview_x.pid] = partyview_x
    return dict_x


@dataclass
class RiverLedgerUnit:
    agenda_healer: str
    currency_onset: float
    currency_cease: float
    _partyviews: dict[str:PartyDBUnit]
    river_tree_level: int
    block_num: int

    def get_range(self):
        return self.currency_cease - self.currency_onset


def get_river_ledger_unit(
    db_conn: Connection, river_block_x: RiverBlockUnit = None
) -> RiverLedgerUnit:
    partyview_x = get_partyview_dict(db_conn, river_block_x.dst_healer)
    return RiverLedgerUnit(
        agenda_healer=river_block_x.dst_healer,
        currency_onset=river_block_x.currency_start,
        currency_cease=river_block_x.currency_close,
        _partyviews=partyview_x,
        river_tree_level=river_block_x.river_tree_level,
        block_num=river_block_x.block_num,
    )


# idea_catalog
def get_idea_catalog_table_create_sqlstr() -> str:
    """table that holds every road and its healer"""
    return """
CREATE TABLE IF NOT EXISTS idea_catalog (
  agenda_healer VARCHAR(255) NOT NULL
, idea_road VARCHAR(1000) NOT NULL
)
;
"""


def get_idea_catalog_table_count(db_conn: Connection, agenda_healer: str) -> str:
    sqlstr = f"""
{get_table_count_sqlstr("idea_catalog")} 
WHERE agenda_healer = '{agenda_healer}'
;
"""
    results = db_conn.execute(sqlstr)
    agenda_row_count = 0
    for row in results.fetchall():
        agenda_row_count = row[0]
    return agenda_row_count


@dataclass
class IdeaCatalog:
    agenda_healer: str
    idea_road: str


def get_idea_catalog_table_insert_sqlstr(
    idea_catalog: IdeaCatalog,
) -> str:
    # return f"""INSERT INTO idea_catalog (agenda_healer, idea_road) VALUES ('{idea_catalog.agenda_healer}', '{idea_catalog.idea_road}');"""
    return f"""
INSERT INTO idea_catalog (
  agenda_healer
, idea_road
)
VALUES (
  '{idea_catalog.agenda_healer}'
, '{create_road_without_root_node(idea_catalog.idea_road)}'
)
;
"""


def get_idea_catalog_dict(db_conn: Connection, search_road: RoadUnit = None):
    if search_road is None:
        where_clause = ""
    else:
        search_road_without_root_node = create_road_without_root_node(search_road)
        where_clause = f"WHERE idea_road = '{search_road_without_root_node}'"
    sqlstr = f"""
SELECT 
  agenda_healer
, idea_road
FROM idea_catalog
{where_clause}
;
"""
    results = db_conn.execute(sqlstr)

    dict_x = {}
    for row in results.fetchall():
        idea_catalog_x = IdeaCatalog(agenda_healer=row[0], idea_road=row[1])
        dict_key = f"{idea_catalog_x.agenda_healer} {idea_catalog_x.idea_road}"
        dict_x[dict_key] = idea_catalog_x
    return dict_x


# belief_catalog
def get_belief_catalog_table_create_sqlstr() -> str:
    """table that holds every belief base and pick of every agenda. missing open/nigh. (clearly not used, maybe add in the future)"""
    return """
CREATE TABLE IF NOT EXISTS belief_catalog (
  agenda_healer VARCHAR(255) NOT NULL
, base VARCHAR(1000) NOT NULL
, pick VARCHAR(1000) NOT NULL
)
;
"""


def get_belief_catalog_table_count(db_conn: Connection, agenda_healer: str) -> str:
    sqlstr = f"""
{get_table_count_sqlstr("belief_catalog")} WHERE agenda_healer = '{agenda_healer}'
;
"""
    results = db_conn.execute(sqlstr)
    agenda_row_count = 0
    for row in results.fetchall():
        agenda_row_count = row[0]
    return agenda_row_count


@dataclass
class BeliefCatalog:
    agenda_healer: str
    base: str
    pick: str


def get_belief_catalog_table_insert_sqlstr(
    belief_catalog: BeliefCatalog,
) -> str:
    return f"""
INSERT INTO belief_catalog (
  agenda_healer
, base
, pick
)
VALUES (
  '{belief_catalog.agenda_healer}'
, '{belief_catalog.base}'
, '{belief_catalog.pick}'
)
;
"""


# groupunit_catalog
def get_groupunit_catalog_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS groupunit_catalog (
  agenda_healer VARCHAR(255) NOT NULL
, groupunit_brand VARCHAR(1000) NOT NULL
, partylinks_set_by_economy_road VARCHAR(1000) NULL
)
;
"""


def get_groupunit_catalog_table_count(db_conn: Connection, agenda_healer: str) -> str:
    sqlstr = f"""
{get_table_count_sqlstr("groupunit_catalog")} WHERE agenda_healer = '{agenda_healer}'
;
"""
    results = db_conn.execute(sqlstr)
    agenda_row_count = 0
    for row in results.fetchall():
        agenda_row_count = row[0]
    return agenda_row_count


@dataclass
class GroupUnitCatalog:
    agenda_healer: str
    groupunit_brand: str
    partylinks_set_by_economy_road: str


def get_groupunit_catalog_table_insert_sqlstr(
    groupunit_catalog: GroupUnitCatalog,
) -> str:
    return f"""
INSERT INTO groupunit_catalog (
  agenda_healer
, groupunit_brand
, partylinks_set_by_economy_road
)
VALUES (
  '{groupunit_catalog.agenda_healer}'
, '{groupunit_catalog.groupunit_brand}'
, '{groupunit_catalog.partylinks_set_by_economy_road}'
)
;
"""


def get_groupunit_catalog_dict(db_conn: Connection) -> dict[str:GroupUnitCatalog]:
    sqlstr = """
SELECT 
  agenda_healer
, groupunit_brand
, partylinks_set_by_economy_road
FROM groupunit_catalog
;
"""
    results = db_conn.execute(sqlstr)

    dict_x = {}
    for row in results.fetchall():
        groupunit_catalog_x = GroupUnitCatalog(
            agenda_healer=row[0],
            groupunit_brand=row[1],
            partylinks_set_by_economy_road=row[2],
        )
        dict_key = (
            f"{groupunit_catalog_x.agenda_healer} {groupunit_catalog_x.groupunit_brand}"
        )
        dict_x[dict_key] = groupunit_catalog_x
    return dict_x


def get_calendar_table_create_sqlstr():
    return """
CREATE TABLE IF NOT EXISTS calendar (
  healer VARCHAR(255) NOT NULL
, report_time_road VARCHAR(10000) NOT NULL
, report_date_range_start INT NOT NULL
, report_date_range_cease INT NOT NULL
, report_interval_length INT NOT NULL
, report_interval_intent_task_max_count INT NOT NULL
, report_interval_intent_state_max_count INT NOT NULL
, time_begin INT NOT NULL
, time_close INT NOT NULL
, intent_idea_road VARCHAR(255) NOT NULL
, intent_weight INT NOT NULL
, task INT NOT NULL
, FOREIGN KEY(healer) REFERENCES agendaunit(healer)
)
;
"""


@dataclass
class CalendarReport:
    healer: PersonID = (None,)
    time_road: RoadUnit = None
    date_range_start: int = None
    interval_count: int = None
    interval_length: int = None
    intent_max_count_task: int = None
    intent_max_count_state: int = None

    def get_date_range_length(self) -> int:
        return self.interval_length * self.interval_count

    def get_date_range_cease(self) -> int:
        return self.date_range_start + self.get_date_range_length()

    def get_interval_begin(self, interval_num: int) -> int:
        return self.date_range_start + (self.interval_length * interval_num)

    def get_interval_close(self, interval_num: int) -> int:
        interval_num += 1
        return self.date_range_start + (self.interval_length * interval_num)


@dataclass
class CalendarIntentUnit:
    calendarreport: CalendarReport
    time_begin: int
    time_close: int
    intent_idea_road: RoadUnit
    intent_weight: float
    task: bool


def get_calendar_table_insert_sqlstr(x_obj: CalendarIntentUnit):
    return f"""
INSERT INTO calendar (
  healer
, report_time_road
, report_date_range_start
, report_date_range_cease
, report_interval_length
, report_interval_intent_task_max_count
, report_interval_intent_state_max_count
, time_begin
, time_close
, intent_idea_road
, intent_weight
, task)
VALUES (
  '{x_obj.calendarreport.healer}'
, '{x_obj.calendarreport.time_road}'
, {sqlite_null(x_obj.calendarreport.date_range_start)}
, {sqlite_null(x_obj.calendarreport.get_date_range_cease())}
, {sqlite_null(x_obj.calendarreport.interval_length)}
, {sqlite_null(x_obj.calendarreport.intent_max_count_task)}
, {sqlite_null(x_obj.calendarreport.intent_max_count_state)}
, {sqlite_null(x_obj.time_begin)}
, {sqlite_null(x_obj.time_close)}
, '{x_obj.intent_idea_road}'
, {sqlite_null(x_obj.intent_weight)}
, {sqlite_bool(x_obj.task)}
)
;
"""


def get_partyunit_table_insert_sqlstr(
    x_agenda: AgendaUnit, x_partyunit: PartyUnit
) -> str:
    """Create table that holds a the output credit metrics."""
    return f"""
INSERT INTO partyunit (
  agenda_healer
, pid
, _agenda_credit
, _agenda_debt
, _agenda_intent_credit
, _agenda_intent_debt
, _agenda_intent_ratio_credit
, _agenda_intent_ratio_debt
, _creditor_active
, _debtor_active
, _treasury_tax_paid
, _treasury_tax_diff
, _treasury_credit_score
, _treasury_voice_rank
, _treasury_voice_hx_lowest_rank
, _title
)
VALUES (
  '{x_agenda._agent_id}' 
, '{x_partyunit.pid}'
, {sqlite_null(x_partyunit._agenda_credit)} 
, {sqlite_null(x_partyunit._agenda_debt)}
, {sqlite_null(x_partyunit._agenda_intent_credit)}
, {sqlite_null(x_partyunit._agenda_intent_debt)}
, {sqlite_null(x_partyunit._agenda_intent_ratio_credit)}
, {sqlite_null(x_partyunit._agenda_intent_ratio_debt)}
, {sqlite_bool(x_partyunit._creditor_active)}
, {sqlite_bool(x_partyunit._debtor_active)}
, {sqlite_null(x_partyunit._treasury_tax_paid)}
, {sqlite_null(x_partyunit._treasury_tax_diff)}
, {sqlite_null(x_partyunit._treasury_credit_score)}
, {sqlite_null(x_partyunit._treasury_voice_rank)}
, {sqlite_null(x_partyunit._treasury_voice_hx_lowest_rank)}
, '{x_partyunit._title}'
)
;
"""


def get_calendar_table_delete_sqlstr(calendar_healer: str) -> str:
    return f"""
DELETE FROM calendar
WHERE healer = '{calendar_healer}' 
;
"""


def get_create_table_if_not_exist_sqlstrs() -> list[str]:
    list_x = [get_agendaunit_table_create_sqlstr()]
    list_x.append(get_belief_catalog_table_create_sqlstr())
    list_x.append(get_idea_catalog_table_create_sqlstr())
    list_x.append(get_partyunit_table_create_sqlstr())
    list_x.append(get_river_block_table_create_sqlstr())
    list_x.append(get_river_circle_table_create_sqlstr())
    list_x.append(get_river_reach_table_create_sqlstr())
    list_x.append(get_groupunit_catalog_table_create_sqlstr())
    list_x.append(get_calendar_table_create_sqlstr())
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
