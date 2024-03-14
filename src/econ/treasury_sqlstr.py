from src.agenda.agenda import AgendaUnit, PartyUnit
from src._road.road import create_road_without_root_node, RoadUnit, PersonID, PartyID
from src.instrument.sqlite import (
    sqlite_bool,
    sqlite_null,
    sqlite_text,
    sqlite_to_python,
    get_row_count_sqlstr,
    get_single_result,
)
from dataclasses import dataclass
from sqlite3 import Connection


def get_river_score_select_sqlstr(cash_master):
    return f"""
SELECT 
  cash_master
, src_owner_id
, SUM(reach_curr_close - reach_curr_start) range_sum
FROM river_reach
WHERE cash_master = '{cash_master}'
GROUP BY cash_master, src_owner_id
ORDER BY range_sum DESC
;
"""


def get_river_reach_table_final_insert_sqlstr(cash_master: PersonID) -> str:
    reach_final_sqlstr = get_river_reach_table_final_select_sqlstr(cash_master)
    return get_river_reach_table_insert_sqlstr(reach_final_sqlstr)


def get_river_reach_table_insert_sqlstr(select_query: str) -> str:
    return f"""
INSERT INTO river_reach (cash_master, src_owner_id, set_num, reach_curr_start, reach_curr_close)
{select_query}
;
"""


def get_river_reach_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS river_reach (
  cash_master VARCHAR(255) NOT NULL
, src_owner_id VARCHAR(255) NOT NULL
, set_num INT NOT NULL
, reach_curr_start FLOAT NOT NULL
, reach_curr_close FLOAT NOT NULL
, FOREIGN KEY(cash_master) REFERENCES agendaunit(owner_id)
, FOREIGN KEY(src_owner_id) REFERENCES agendaunit(owner_id)
)
;
"""


def get_river_reach_table_touch_select_sqlstr(cash_master: PersonID) -> str:
    return f"""
    SELECT 
    block.cash_master
    , block.src_owner_id src
    , block.dst_owner_id dst
    , CASE 
        WHEN block.cash_start < circle.curr_start 
            AND block.cash_close > circle.curr_start
            AND block.cash_close <= circle.curr_close
            THEN circle.curr_start --'leftside' 
        WHEN block.cash_start >= circle.curr_start 
            AND block.cash_start < circle.curr_close
            AND block.cash_close > circle.curr_close
            THEN block.cash_start --'rightside' 
        WHEN block.cash_start < circle.curr_start 
            AND block.cash_close > circle.curr_close
            THEN circle.curr_start --'outside' 
        WHEN block.cash_start >= circle.curr_start 
            AND block.cash_close <= circle.curr_close
            THEN block.cash_start --'inside' 
            END reach_start
    , CASE 
        WHEN block.cash_start < circle.curr_start 
            AND block.cash_close > circle.curr_start
            AND block.cash_close <= circle.curr_close
            THEN block.cash_close --'leftside' 
        WHEN block.cash_start >= circle.curr_start 
            AND block.cash_start < circle.curr_close
            AND block.cash_close > circle.curr_close
            THEN circle.curr_close --'rightside' 
        WHEN block.cash_start < circle.curr_start 
            AND block.cash_close > circle.curr_close
            THEN circle.curr_close --'outside' 
        WHEN block.cash_start >= circle.curr_start 
            AND block.cash_close <= circle.curr_close
            THEN block.cash_close --'inside' 
            END reach_close
    FROM river_block block
    JOIN river_circle circle on 
            (block.cash_start < circle.curr_start 
            AND block.cash_close > circle.curr_close)
        OR     (block.cash_start >= circle.curr_start 
            AND block.cash_close <= circle.curr_close)
        OR     (block.cash_start < circle.curr_start 
            AND block.cash_close > circle.curr_start
            AND block.cash_close <= circle.curr_close)
        OR     (block.cash_start >= circle.curr_start 
            AND block.cash_start < circle.curr_close
            AND block.cash_close > circle.curr_close)
    WHERE block.cash_master = '{cash_master}'
        AND block.src_owner_id != block.cash_master
    ORDER BY 
    block.src_owner_id
    , block.dst_owner_id
    , block.cash_start
    , block.cash_close
"""


def get_river_reach_table_final_select_sqlstr(cash_master: PersonID) -> str:
    return f"""
WITH reach_inter(curr_mstr, src, dst, reach_start, reach_close) AS (
{get_river_reach_table_touch_select_sqlstr(cash_master)}
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


# river_block
def get_river_block_table_delete_sqlstr(cash_owner_id: str) -> str:
    return f"""
DELETE FROM river_block
WHERE cash_master = '{cash_owner_id}' 
;
"""


def get_river_block_table_create_sqlstr() -> str:
    """Table that stores each block of cash from src_owner_id to dst_owner_id.
    cash_master: every cash starts with a owner_id as credit source
        All river blocks with destination cash owner_id stop. For that cash range
        there is no more block
    src_owner_id: owner_id that is source of credit
    dst_owner_id: owner_id that is destination of credit.
    cash_start: range of cash influenced start
    cash_close: range of cash influenced close
    block_num: the sequence number of transactions before this one
    parent_block_num: river blocks can have multiple children but only one parent
    river_tree_level: how many ancestors between cash_master first credit outblock
        and this river block
    JSchalk 24 Oct 2023
    """
    return """
CREATE TABLE IF NOT EXISTS river_block (
  cash_master VARCHAR(255) NOT NULL
, src_owner_id VARCHAR(255) NOT NULL
, dst_owner_id VARCHAR(255) NOT NULL
, cash_start FLOAT NOT NULL
, cash_close FLOAT NOT NULL
, block_num INT NOT NULL
, parent_block_num INT NULL
, river_tree_level INT NOT NULL
, FOREIGN KEY(cash_master) REFERENCES agendaunit(owner_id)
, FOREIGN KEY(src_owner_id) REFERENCES agendaunit(owner_id)
, FOREIGN KEY(dst_owner_id) REFERENCES agendaunit(owner_id)
)
;
"""


@dataclass
class RiverBlockUnit:
    cash_owner_id: str
    src_owner_id: str
    dst_owner_id: str
    cash_start: float
    cash_close: float
    block_num: int
    parent_block_num: int
    river_tree_level: int

    def block_returned(self) -> bool:
        return self.cash_owner_id == self.dst_owner_id


def get_river_block_table_insert_sqlstr(
    river_block_x: RiverBlockUnit,
) -> str:
    return f"""
INSERT INTO river_block (
  cash_master
, src_owner_id
, dst_owner_id
, cash_start 
, cash_close
, block_num
, parent_block_num
, river_tree_level
)
VALUES (
  '{river_block_x.cash_owner_id}'
, '{river_block_x.src_owner_id}'
, '{river_block_x.dst_owner_id}'
, {sqlite_null(river_block_x.cash_start)}
, {sqlite_null(river_block_x.cash_close)}
, {river_block_x.block_num}
, {sqlite_null(river_block_x.parent_block_num)}
, {river_block_x.river_tree_level}
)
;
"""


def get_river_block_dict(db_conn: str, cash_owner_id: str) -> dict[str:RiverBlockUnit]:
    sqlstr = f"""
SELECT 
  cash_master
, src_owner_id
, dst_owner_id
, cash_start
, cash_close
, block_num
, parent_block_num
, river_tree_level
FROM river_block
WHERE cash_master = '{cash_owner_id}' 
;
"""
    dict_x = {}
    cursor_x = db_conn.cursor()
    results_cursor_x = cursor_x.execute(sqlstr)
    results_x = results_cursor_x.fetchall()

    for count_x, row in enumerate(results_x):
        river_block_x = RiverBlockUnit(
            cash_owner_id=row[0],
            src_owner_id=row[1],
            dst_owner_id=row[2],
            cash_start=row[3],
            cash_close=row[4],
            block_num=row[5],
            parent_block_num=row[6],
            river_tree_level=row[7],
        )
        dict_x[count_x] = river_block_x
    return dict_x


# river_circle
def get_river_circle_table_delete_sqlstr(cash_owner_id: str) -> str:
    return f"""
DELETE FROM river_circle
WHERE cash_master = '{cash_owner_id}' 
;
"""


def get_river_circle_table_create_sqlstr() -> str:
    """Check get_river_circle_table_insert_sqlstrget_river_circle_table_insert_sqlstr doc string"""
    return """
CREATE TABLE IF NOT EXISTS river_circle (
  cash_master VARCHAR(255) NOT NULL
, dst_owner_id VARCHAR(255) NOT NULL
, circle_num INT NOT NULL
, curr_start FLOAT NOT NULL
, curr_close FLOAT NOT NULL
, FOREIGN KEY(cash_master) REFERENCES agendaunit(owner_id)
, FOREIGN KEY(dst_owner_id) REFERENCES agendaunit(owner_id)
)
;
"""


def get_river_circle_table_insert_sqlstr(cash_owner_id: str) -> str:
    """Table that stores discontinuous cash ranges that circle back from source (cash_master)
    to final destination (cash_master)
    Columns
    cash_master: every cash starts with a owner_id as credit source
    dst_owner_id: owner_id that is destination of credit.
        All river blocks with destination owner_id are summed into ranges called circles
    circle_num: all destination owner_id circles have a unique number. (sequential 0, 1, 2...)
    cash_start: range of circle start
    cash_close: range of circle close
    JSchalk 24 Oct 2023
    """
    return f"""
INSERT INTO river_circle (
  cash_master
, dst_owner_id
, circle_num
, curr_start
, curr_close
)
SELECT 
  cash_master
, dst_owner_id
, cash_circle_num
, min(cash_start) cash_circle_start
, max(cash_close) cash_circle_close
FROM  (
SELECT *, SUM(step) OVER (ORDER BY cash_start) AS cash_circle_num
FROM  (
    SELECT 
    CASE 
    WHEN lag(cash_close) OVER (ORDER BY cash_start) < cash_start 
        OR lag(cash_close) OVER (ORDER BY cash_start) = NULL 
    THEN 1
    ELSE 0
    END AS step
    , *
    FROM  river_block
    WHERE cash_master = '{cash_owner_id}' and dst_owner_id = cash_master 
    ) b
) c
GROUP BY cash_master, dst_owner_id, cash_circle_num
ORDER BY cash_circle_start
;
"""


@dataclass
class RiverCircleUnit:
    cash_master: str
    dst_owner_id: str
    circle_num: int
    curr_start: float
    curr_close: float


def get_river_circle_dict(
    db_conn: Connection, cash_owner_id: str
) -> dict[str:RiverCircleUnit]:
    sqlstr = f"""
SELECT
  cash_master
, dst_owner_id
, circle_num
, curr_start
, curr_close
FROM river_circle
WHERE cash_master = '{cash_owner_id}'
;
"""
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        river_circle_x = RiverCircleUnit(
            cash_master=row[0],
            dst_owner_id=row[1],
            circle_num=row[2],
            curr_start=row[3],
            curr_close=row[4],
        )
        dict_x[river_circle_x.circle_num] = river_circle_x
    return dict_x


# PartyTreasuryUnit
@dataclass
class PartyTreasuryUnit:
    cash_master: str
    due_owner_id: str
    due_total: float
    debt: float
    due_diff: float
    credit_score: float
    voice_rank: int


def get_partytreasuryunit_dict(
    db_conn: Connection, cash_owner_id: str
) -> dict[str:PartyTreasuryUnit]:
    sqlstr = f"""
SELECT
  owner_id cash_master
, party_id due_owner_id
, _treasury_due_paid due_total
, _agenda_intent_ratio_debt debt
, (_agenda_intent_ratio_debt - _treasury_due_paid) due_diff
FROM agenda_partyunit
WHERE cash_master = '{cash_owner_id}'
    AND _treasury_due_paid IS NOT NULL
;
"""
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        partytreasuryunit_x = PartyTreasuryUnit(
            cash_master=row[0],
            due_owner_id=row[1],
            due_total=row[2],
            debt=row[3],
            due_diff=row[4],
            credit_score=None,
            voice_rank=None,
        )
        dict_x[partytreasuryunit_x.due_owner_id] = partytreasuryunit_x
    return dict_x


# agenda
def get_agendaunit_table_create_sqlstr() -> str:
    """Create table that references the person_id of every agenda. The owner_id pip of the one running that agenda's clerk."""
    return """
CREATE TABLE IF NOT EXISTS agendaunit (
  owner_id VARCHAR(255) PRIMARY KEY ASC
, rational INT NULL
, UNIQUE(owner_id)
)
;
"""


def get_agendaunit_table_insert_sqlstr(x_agenda: AgendaUnit) -> str:
    return f"""
INSERT INTO agendaunit (
  owner_id
, rational
)
VALUES (
  '{x_agenda._owner_id}' 
, NULL
)
;
"""


def get_agendaunits_select_sqlstr():
    return """
SELECT 
  owner_id
, rational
FROM agendaunit
;
"""


@dataclass
class AgendaTreasuryUnit:
    owner_id: PersonID
    rational: bool


def get_agendatreasuryunits_dict(
    db_conn: Connection,
) -> dict[PersonID:AgendaTreasuryUnit]:
    results = db_conn.execute(get_agendaunits_select_sqlstr())
    dict_x = {}
    for row in results.fetchall():
        x_agendatreasuryunit = AgendaTreasuryUnit(
            owner_id=row[0], rational=sqlite_to_python(row[1])
        )
        dict_x[x_agendatreasuryunit.owner_id] = x_agendatreasuryunit
    return dict_x


def get_agendaunit_update_sqlstr(agenda: AgendaUnit) -> str:
    return f"""
UPDATE agendaunit
SET rational = {sqlite_text(agenda._rational)}
WHERE owner_id = '{agenda._owner_id}'
;
"""


# partyunit
def get_agenda_partyunit_table_create_sqlstr() -> str:
    """Create table that holds the starting river metrics for every agenda's party. All the metrics."""
    return """
CREATE TABLE IF NOT EXISTS agenda_partyunit (
  owner_id VARCHAR(255) NOT NULL 
, party_id VARCHAR(255) NOT NULL
, _agenda_credit FLOAT
, _agenda_debt FLOAT
, _agenda_intent_credit FLOAT
, _agenda_intent_debt FLOAT
, _agenda_intent_ratio_credit FLOAT
, _agenda_intent_ratio_debt FLOAT
, _creditor_operational INT
, _debtor_operational INT
, _treasury_due_paid FLOAT
, _treasury_due_diff FLOAT
, _treasury_credit_score FLOAT
, _treasury_voice_rank INT
, _treasury_voice_hx_lowest_rank INT
, FOREIGN KEY(owner_id) REFERENCES agendaunit(owner_id)
, FOREIGN KEY(party_id) REFERENCES agendaunit(owner_id)
, UNIQUE(owner_id, party_id)
)
;
"""


def get_agenda_partyunit_table_update_treasury_due_paid_sqlstr(
    cash_owner_id: PersonID,
) -> str:
    return f"""
UPDATE agenda_partyunit
SET _treasury_due_paid = (
    SELECT SUM(block.cash_close-block.cash_start) 
    FROM river_block block
    WHERE block.cash_master='{cash_owner_id}' 
        AND block.dst_owner_id=block.cash_master
        AND block.src_owner_id = agenda_partyunit.party_id
    )
WHERE EXISTS (
    SELECT block.cash_close
    FROM river_block block
    WHERE agenda_partyunit.owner_id='{cash_owner_id}' 
        AND agenda_partyunit.party_id = block.dst_owner_id
)
;
"""


def get_agenda_partyunit_table_update_credit_score_sqlstr(
    cash_owner_id: PersonID,
) -> str:
    return f"""
UPDATE agenda_partyunit
SET _treasury_credit_score = (
    SELECT SUM(reach_curr_close - reach_curr_start) range_sum
    FROM river_reach reach
    WHERE reach.cash_master = agenda_partyunit.owner_id
        AND reach.src_owner_id = agenda_partyunit.party_id
    )
WHERE agenda_partyunit.owner_id = '{cash_owner_id}'
;
"""


def get_agenda_partyunit_table_update_treasury_voice_rank_sqlstr(
    owner_id: PersonID,
) -> str:
    return f"""
UPDATE agenda_partyunit
SET _treasury_voice_rank = 
    (
    SELECT rn
    FROM (
        SELECT p2.party_id
        , row_number() over (order by p2._treasury_credit_score DESC) rn
        FROM agenda_partyunit p2
        WHERE p2.owner_id = '{owner_id}'
    ) p3
    WHERE p3.party_id = agenda_partyunit.party_id AND agenda_partyunit.owner_id = '{owner_id}'
    )
WHERE agenda_partyunit.owner_id = '{owner_id}'
;
"""


def get_agenda_partyunit_table_insert_sqlstr(
    x_agenda: AgendaUnit, x_partyunit: PartyUnit
) -> str:
    """Create table that holds a the output credit metrics."""
    return f"""
INSERT INTO agenda_partyunit (
  owner_id
, party_id
, _agenda_credit
, _agenda_debt
, _agenda_intent_credit
, _agenda_intent_debt
, _agenda_intent_ratio_credit
, _agenda_intent_ratio_debt
, _creditor_operational
, _debtor_operational
, _treasury_due_paid
, _treasury_due_diff
, _treasury_credit_score
, _treasury_voice_rank
, _treasury_voice_hx_lowest_rank
)
VALUES (
  '{x_agenda._owner_id}' 
, '{x_partyunit.party_id}'
, {sqlite_null(x_partyunit._agenda_credit)} 
, {sqlite_null(x_partyunit._agenda_debt)}
, {sqlite_null(x_partyunit._agenda_intent_credit)}
, {sqlite_null(x_partyunit._agenda_intent_debt)}
, {sqlite_null(x_partyunit._agenda_intent_ratio_credit)}
, {sqlite_null(x_partyunit._agenda_intent_ratio_debt)}
, {sqlite_bool(x_partyunit._creditor_operational)}
, {sqlite_bool(x_partyunit._debtor_operational)}
, {sqlite_null(x_partyunit._treasury_due_paid)}
, {sqlite_null(x_partyunit._treasury_due_diff)}
, {sqlite_null(x_partyunit._treasury_credit_score)}
, {sqlite_null(x_partyunit._treasury_voice_rank)}
, {sqlite_null(x_partyunit._treasury_voice_hx_lowest_rank)}
)
;
"""


@dataclass
class PartyDBUnit(PartyUnit):
    owner_id: str = None


def get_partyview_dict(
    db_conn: Connection, payer_owner_id: PersonID
) -> dict[PartyID:PartyDBUnit]:
    sqlstr = f"""
SELECT 
  owner_id
, party_id
, _agenda_credit
, _agenda_debt
, _agenda_intent_credit
, _agenda_intent_debt
, _agenda_intent_ratio_credit
, _agenda_intent_ratio_debt
, _creditor_operational
, _debtor_operational
, _treasury_due_paid
, _treasury_due_diff
, _treasury_credit_score
, _treasury_voice_rank
, _treasury_voice_hx_lowest_rank
FROM agenda_partyunit
WHERE owner_id = '{payer_owner_id}' 
;
"""
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        partyview_x = PartyDBUnit(
            owner_id=row[0],
            party_id=row[1],
            _agenda_credit=row[2],
            _agenda_debt=row[3],
            _agenda_intent_credit=row[4],
            _agenda_intent_debt=row[5],
            _agenda_intent_ratio_credit=row[6],
            _agenda_intent_ratio_debt=row[7],
            _creditor_operational=row[8],
            _debtor_operational=row[9],
            _treasury_due_paid=row[10],
            _treasury_due_diff=row[11],
            _treasury_credit_score=row[12],
            _treasury_voice_rank=row[13],
            _treasury_voice_hx_lowest_rank=row[14],
        )
        dict_x[partyview_x.party_id] = partyview_x
    return dict_x


@dataclass
class RiverLedgerUnit:
    owner_id: str
    cash_onset: float
    cash_cease: float
    _partyviews: dict[str:PartyDBUnit]
    river_tree_level: int
    block_num: int

    def get_range(self):
        return self.cash_cease - self.cash_onset


def get_river_ledger_unit(
    db_conn: Connection, river_block_x: RiverBlockUnit = None
) -> RiverLedgerUnit:
    partyview_x = get_partyview_dict(db_conn, river_block_x.dst_owner_id)
    return RiverLedgerUnit(
        owner_id=river_block_x.dst_owner_id,
        cash_onset=river_block_x.cash_start,
        cash_cease=river_block_x.cash_close,
        _partyviews=partyview_x,
        river_tree_level=river_block_x.river_tree_level,
        block_num=river_block_x.block_num,
    )


# agenda_ideaunit
def get_agenda_ideaunit_table_create_sqlstr() -> str:
    """table that holds every road and its owner_id"""
    return """
CREATE TABLE IF NOT EXISTS agenda_ideaunit (
  owner_id VARCHAR(255) NOT NULL
, idea_road VARCHAR(1000) NOT NULL
)
;
"""


def get_agenda_ideaunit_row_count(db_conn: Connection, owner_id: str) -> str:
    sqlstr = f"""
{get_row_count_sqlstr("agenda_ideaunit")} 
WHERE owner_id = '{owner_id}'
;
"""
    return get_single_result(db_conn, sqlstr)


@dataclass
class IdeaCatalog:
    owner_id: str
    idea_road: str


def get_agenda_ideaunit_table_insert_sqlstr(
    agenda_ideaunit: IdeaCatalog,
) -> str:
    # return f"""INSERT INTO agenda_ideaunit (owner_id, idea_road) VALUES ('{agenda_ideaunit.owner_id}', '{agenda_ideaunit.idea_road}');"""
    return f"""
INSERT INTO agenda_ideaunit (
  owner_id
, idea_road
)
VALUES (
  '{agenda_ideaunit.owner_id}'
, '{create_road_without_root_node(agenda_ideaunit.idea_road)}'
)
;
"""


def get_agenda_ideaunit_dict(db_conn: Connection, search_road: RoadUnit = None):
    if search_road is None:
        where_clause = ""
    else:
        search_road_without_root_node = create_road_without_root_node(search_road)
        where_clause = f"WHERE idea_road = '{search_road_without_root_node}'"
    sqlstr = f"""
SELECT 
  owner_id
, idea_road
FROM agenda_ideaunit
{where_clause}
;
"""
    results = db_conn.execute(sqlstr)

    dict_x = {}
    for row in results.fetchall():
        agenda_ideaunit_x = IdeaCatalog(owner_id=row[0], idea_road=row[1])
        dict_key = f"{agenda_ideaunit_x.owner_id} {agenda_ideaunit_x.idea_road}"
        dict_x[dict_key] = agenda_ideaunit_x
    return dict_x


# agenda_idea_beliefunit
def get_agenda_idea_beliefunit_table_create_sqlstr() -> str:
    """table that holds every belief base and pick of every agenda. missing open/nigh. (clearly not used, maybe add in the future)"""
    return """
CREATE TABLE IF NOT EXISTS agenda_idea_beliefunit (
  owner_id VARCHAR(255) NOT NULL
, base VARCHAR(1000) NOT NULL
, pick VARCHAR(1000) NOT NULL
)
;
"""


def get_agenda_idea_beliefunit_row_count(db_conn: Connection, owner_id: str) -> str:
    sqlstr = f"""
{get_row_count_sqlstr("agenda_idea_beliefunit")} WHERE owner_id = '{owner_id}'
;
"""
    return get_single_result(db_conn, sqlstr)


@dataclass
class BeliefCatalog:
    owner_id: str
    base: str
    pick: str


def get_agenda_idea_beliefunit_table_insert_sqlstr(
    agenda_idea_beliefunit: BeliefCatalog,
) -> str:
    return f"""
INSERT INTO agenda_idea_beliefunit (
  owner_id
, base
, pick
)
VALUES (
  '{agenda_idea_beliefunit.owner_id}'
, '{agenda_idea_beliefunit.base}'
, '{agenda_idea_beliefunit.pick}'
)
;
"""


# agenda_groupunit
def get_agenda_groupunit_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS agenda_groupunit (
  owner_id VARCHAR(255) NOT NULL
, groupunit_group_id VARCHAR(1000) NOT NULL
, treasury_partylinks VARCHAR(1000) NULL
)
;
"""


def get_agenda_groupunit_row_count(db_conn: Connection, owner_id: str) -> str:
    sqlstr = f"""
{get_row_count_sqlstr("agenda_groupunit")} WHERE owner_id = '{owner_id}'
;
"""
    return get_single_result(db_conn, sqlstr)


@dataclass
class GroupUnitCatalog:
    owner_id: str
    groupunit_group_id: str
    treasury_partylinks: str


def get_agenda_groupunit_table_insert_sqlstr(
    agenda_groupunit: GroupUnitCatalog,
) -> str:
    return f"""
INSERT INTO agenda_groupunit (
  owner_id
, groupunit_group_id
, treasury_partylinks
)
VALUES (
  '{agenda_groupunit.owner_id}'
, '{agenda_groupunit.groupunit_group_id}'
, '{agenda_groupunit.treasury_partylinks}'
)
;
"""


def get_agenda_groupunit_dict(db_conn: Connection) -> dict[str:GroupUnitCatalog]:
    sqlstr = """
SELECT 
  owner_id
, groupunit_group_id
, treasury_partylinks
FROM agenda_groupunit
;
"""
    results = db_conn.execute(sqlstr)

    dict_x = {}
    for row in results.fetchall():
        agenda_groupunit_x = GroupUnitCatalog(
            owner_id=row[0],
            groupunit_group_id=row[1],
            treasury_partylinks=row[2],
        )
        dict_key = (
            f"{agenda_groupunit_x.owner_id} {agenda_groupunit_x.groupunit_group_id}"
        )
        dict_x[dict_key] = agenda_groupunit_x
    return dict_x


def get_calendar_table_create_sqlstr():
    return """
CREATE TABLE IF NOT EXISTS calendar (
  owner_id VARCHAR(255) NOT NULL
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
, FOREIGN KEY(owner_id) REFERENCES agendaunit(owner_id)
)
;
"""


@dataclass
class CalendarReport:
    owner_id: PersonID = (None,)
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
  owner_id
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
  '{x_obj.calendarreport.owner_id}'
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


def get_agenda_partyunit_table_insert_sqlstr(
    x_agenda: AgendaUnit, x_partyunit: PartyUnit
) -> str:
    """Create table that holds a the output credit metrics."""
    return f"""
INSERT INTO agenda_partyunit (
  owner_id
, party_id
, _agenda_credit
, _agenda_debt
, _agenda_intent_credit
, _agenda_intent_debt
, _agenda_intent_ratio_credit
, _agenda_intent_ratio_debt
, _creditor_operational
, _debtor_operational
, _treasury_due_paid
, _treasury_due_diff
, _treasury_credit_score
, _treasury_voice_rank
, _treasury_voice_hx_lowest_rank
)
VALUES (
  '{x_agenda._owner_id}' 
, '{x_partyunit.party_id}'
, {sqlite_null(x_partyunit._agenda_credit)} 
, {sqlite_null(x_partyunit._agenda_debt)}
, {sqlite_null(x_partyunit._agenda_intent_credit)}
, {sqlite_null(x_partyunit._agenda_intent_debt)}
, {sqlite_null(x_partyunit._agenda_intent_ratio_credit)}
, {sqlite_null(x_partyunit._agenda_intent_ratio_debt)}
, {sqlite_bool(x_partyunit._creditor_operational)}
, {sqlite_bool(x_partyunit._debtor_operational)}
, {sqlite_null(x_partyunit._treasury_due_paid)}
, {sqlite_null(x_partyunit._treasury_due_diff)}
, {sqlite_null(x_partyunit._treasury_credit_score)}
, {sqlite_null(x_partyunit._treasury_voice_rank)}
, {sqlite_null(x_partyunit._treasury_voice_hx_lowest_rank)}
)
;
"""


def get_calendar_table_delete_sqlstr(calendar_owner_id: str) -> str:
    return f"""
DELETE FROM calendar
WHERE owner_id = '{calendar_owner_id}' 
;
"""


def get_create_table_if_not_exist_sqlstrs() -> list[str]:
    list_x = [get_agendaunit_table_create_sqlstr()]
    list_x.append(get_agenda_idea_beliefunit_table_create_sqlstr())
    list_x.append(get_agenda_ideaunit_table_create_sqlstr())
    list_x.append(get_agenda_partyunit_table_create_sqlstr())
    list_x.append(get_river_block_table_create_sqlstr())
    list_x.append(get_river_circle_table_create_sqlstr())
    list_x.append(get_river_reach_table_create_sqlstr())
    list_x.append(get_agenda_groupunit_table_create_sqlstr())
    list_x.append(get_calendar_table_create_sqlstr())
    return list_x
