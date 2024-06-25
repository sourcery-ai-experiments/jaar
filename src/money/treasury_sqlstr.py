from src._road.road import create_road_without_root_node, RoadUnit, OwnerID, PersonID
from src._instrument.sqlite import (
    sqlite_bool,
    sqlite_null,
    sqlite_text,
    sqlite_to_python,
    get_row_count_sqlstr,
    get_single_result,
)
from src._world.world import WorldUnit, PersonUnit
from dataclasses import dataclass
from sqlite3 import Connection


def get_river_score_select_sqlstr(cash_master):
    return f"""
SELECT 
  cash_master
, src_owner_id
, SUM(reach_coin_close - reach_coin_start) range_sum
FROM river_reach
WHERE cash_master = '{cash_master}'
GROUP BY cash_master, src_owner_id
ORDER BY range_sum DESC
;
"""


def get_river_reach_table_final_insert_sqlstr(cash_master: OwnerID) -> str:
    reach_final_sqlstr = get_river_reach_table_final_select_sqlstr(cash_master)
    return get_river_reach_table_insert_sqlstr(reach_final_sqlstr)


def get_river_reach_table_insert_sqlstr(select_query: str) -> str:
    return f"""
INSERT INTO river_reach (cash_master, src_owner_id, set_num, reach_coin_start, reach_coin_close)
{select_query}
;
"""


def get_river_reach_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS river_reach (
  cash_master VARCHAR(255) NOT NULL
, src_owner_id VARCHAR(255) NOT NULL
, set_num INT NOT NULL
, reach_coin_start FLOAT NOT NULL
, reach_coin_close FLOAT NOT NULL
, FOREIGN KEY(cash_master) REFERENCES worldunit(owner_id)
, FOREIGN KEY(src_owner_id) REFERENCES worldunit(owner_id)
)
;
"""


def get_river_reach_table_touch_select_sqlstr(cash_master: OwnerID) -> str:
    return f"""
    SELECT 
    block.cash_master
    , block.src_owner_id src
    , block.dst_owner_id dst
    , CASE 
        WHEN block.cash_start < circle.coin_start 
            AND block.cash_close > circle.coin_start
            AND block.cash_close <= circle.coin_close
            THEN circle.coin_start --'leftside' 
        WHEN block.cash_start >= circle.coin_start 
            AND block.cash_start < circle.coin_close
            AND block.cash_close > circle.coin_close
            THEN block.cash_start --'rightside' 
        WHEN block.cash_start < circle.coin_start 
            AND block.cash_close > circle.coin_close
            THEN circle.coin_start --'outside' 
        WHEN block.cash_start >= circle.coin_start 
            AND block.cash_close <= circle.coin_close
            THEN block.cash_start --'inside' 
            END reach_start
    , CASE 
        WHEN block.cash_start < circle.coin_start 
            AND block.cash_close > circle.coin_start
            AND block.cash_close <= circle.coin_close
            THEN block.cash_close --'leftside' 
        WHEN block.cash_start >= circle.coin_start 
            AND block.cash_start < circle.coin_close
            AND block.cash_close > circle.coin_close
            THEN circle.coin_close --'rightside' 
        WHEN block.cash_start < circle.coin_start 
            AND block.cash_close > circle.coin_close
            THEN circle.coin_close --'outside' 
        WHEN block.cash_start >= circle.coin_start 
            AND block.cash_close <= circle.coin_close
            THEN block.cash_close --'inside' 
            END reach_close
    FROM river_block block
    JOIN river_circle circle on 
            (block.cash_start < circle.coin_start 
            AND block.cash_close > circle.coin_close)
        OR     (block.cash_start >= circle.coin_start 
            AND block.cash_close <= circle.coin_close)
        OR     (block.cash_start < circle.coin_start 
            AND block.cash_close > circle.coin_start
            AND block.cash_close <= circle.coin_close)
        OR     (block.cash_start >= circle.coin_start 
            AND block.cash_start < circle.coin_close
            AND block.cash_close > circle.coin_close)
    WHERE block.cash_master = '{cash_master}'
        AND block.src_owner_id != block.cash_master
    ORDER BY 
    block.src_owner_id
    , block.dst_owner_id
    , block.cash_start
    , block.cash_close
"""


def get_river_reach_table_final_select_sqlstr(cash_master: OwnerID) -> str:
    return f"""
WITH reach_inter(coin_mstr, src, dst, reach_start, reach_close) AS (
{get_river_reach_table_touch_select_sqlstr(cash_master)}
),
reach_order(
  coin_mstr
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
    reach_inter.coin_mstr
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
  coin_mstr
, src
, prev_src
, src_step
, range_step
, delta_step
, prev_start
, prev_close
, reach_start
, reach_close
) AS (
    SELECT
    coin_mstr
    , src
    , prev_src
    , src_step
    , range_step
    , CASE 
        WHEN src_step =1 AND range_step =1 
        THEN 1
        ELSE src_step + range_step
        END delta_step
    , prev_start
    , prev_close
    , reach_start
    , reach_close
    FROM reach_order
)
, reach_sets_num (  
  coin_mstr
, src
, set_num
, prev_start
, prev_close
, reach_start
, reach_close
) AS (
    SELECT
      coin_mstr
    , src
    , SUM(delta_step) OVER (ORDER BY src, reach_start, reach_close) set_num
    , prev_start
    , prev_close
    , reach_start
    , reach_close
    FROM reach_step
)
SELECT 
  coin_mstr
, src
, set_num 
, MIN(reach_start) reach_start
, MAX(reach_close) reach_close
FROM reach_sets_num
GROUP BY coin_mstr, src, set_num
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
    cash_master: every cash starts with a owner_id as cred source
        All river blocks with destination cash owner_id stop. For that cash range
        there is no more block
    src_owner_id: owner_id that is source of cred
    dst_owner_id: owner_id that is destination of cred.
    cash_start: range of cash influenced start
    cash_close: range of cash influenced close
    block_num: the sequence number of rewards before this one
    parent_block_num: river blocks can have multiple children but only one parent
    river_tree_level: how many ancestors between cash_master first cred outblock
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
, FOREIGN KEY(cash_master) REFERENCES worldunit(owner_id)
, FOREIGN KEY(src_owner_id) REFERENCES worldunit(owner_id)
, FOREIGN KEY(dst_owner_id) REFERENCES worldunit(owner_id)
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
, coin_start FLOAT NOT NULL
, coin_close FLOAT NOT NULL
, FOREIGN KEY(cash_master) REFERENCES worldunit(owner_id)
, FOREIGN KEY(dst_owner_id) REFERENCES worldunit(owner_id)
)
;
"""


def get_river_circle_table_insert_sqlstr(cash_owner_id: str) -> str:
    """Table that stores discontinuous cash ranges that circle back from source (cash_master)
    to final destination (cash_master)
    Columns
    cash_master: every cash starts with a owner_id as cred source
    dst_owner_id: owner_id that is destination of cred.
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
, coin_start
, coin_close
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
    coin_start: float
    coin_close: float


def get_river_circle_dict(
    db_conn: Connection, cash_owner_id: str
) -> dict[str:RiverCircleUnit]:
    sqlstr = f"""
SELECT
  cash_master
, dst_owner_id
, circle_num
, coin_start
, coin_close
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
            coin_start=row[3],
            coin_close=row[4],
        )
        dict_x[river_circle_x.circle_num] = river_circle_x
    return dict_x


# PersonTreasuryUnit
@dataclass
class PersonTreasuryUnit:
    cash_master: str
    due_owner_id: str
    due_total: float
    debt: float
    due_diff: float
    cred_score: float
    voice_rank: int


def get_persontreasuryunit_dict(
    db_conn: Connection, cash_owner_id: str
) -> dict[str:PersonTreasuryUnit]:
    sqlstr = f"""
SELECT
  owner_id cash_master
, person_id due_owner_id
, _treasury_due_paid due_total
, _world_agenda_ratio_debt debt
, (_world_agenda_ratio_debt - _treasury_due_paid) due_diff
FROM world_personunit
WHERE cash_master = '{cash_owner_id}'
    AND _treasury_due_paid IS NOT NULL
;
"""
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        persontreasuryunit_x = PersonTreasuryUnit(
            cash_master=row[0],
            due_owner_id=row[1],
            due_total=row[2],
            debt=row[3],
            due_diff=row[4],
            cred_score=None,
            voice_rank=None,
        )
        dict_x[persontreasuryunit_x.due_owner_id] = persontreasuryunit_x
    return dict_x


# world
def get_worldunit_table_create_sqlstr() -> str:
    """Create table that references the owner_id of every world."""
    return """
CREATE TABLE IF NOT EXISTS worldunit (
  owner_id VARCHAR(255) PRIMARY KEY ASC
, real_id VARCHAR(255) NOT NULL
, rational INT NULL
, UNIQUE(owner_id)
)
;
"""


def get_worldunit_table_insert_sqlstr(x_world: WorldUnit) -> str:
    return f"""
INSERT INTO worldunit (
  real_id
, owner_id
, rational
)
VALUES (
  '{x_world._real_id}' 
, '{x_world._owner_id}' 
, NULL
)
;
"""


def get_worldunits_select_sqlstr():
    return """
SELECT 
  owner_id
, rational
FROM worldunit
;
"""


@dataclass
class WorldTreasuryUnit:
    owner_id: OwnerID
    rational: bool


def get_worldtreasuryunits_dict(
    db_conn: Connection,
) -> dict[OwnerID:WorldTreasuryUnit]:
    results = db_conn.execute(get_worldunits_select_sqlstr())
    dict_x = {}
    for row in results.fetchall():
        x_worldtreasuryunit = WorldTreasuryUnit(
            owner_id=row[0], rational=sqlite_to_python(row[1])
        )
        dict_x[x_worldtreasuryunit.owner_id] = x_worldtreasuryunit
    return dict_x


def get_worldunit_update_sqlstr(world: WorldUnit) -> str:
    return f"""
UPDATE worldunit
SET rational = {sqlite_text(world._rational)}
WHERE owner_id = '{world._owner_id}'
;
"""


# personunit
def get_world_personunit_table_create_sqlstr() -> str:
    """Create table that holds the starting river metrics for every world's person. All the metrics."""
    return """
CREATE TABLE IF NOT EXISTS world_personunit (
  owner_id VARCHAR(255) NOT NULL 
, person_id VARCHAR(255) NOT NULL
, _world_cred FLOAT
, _world_debt FLOAT
, _world_agenda_cred FLOAT
, _world_agenda_debt FLOAT
, _world_agenda_ratio_cred FLOAT
, _world_agenda_ratio_debt FLOAT
, _credor_operational INT
, _debtor_operational INT
, _treasury_due_paid FLOAT
, _treasury_due_diff FLOAT
, _treasury_cred_score FLOAT
, _treasury_voice_rank INT
, _treasury_voice_hx_lowest_rank INT
, FOREIGN KEY(owner_id) REFERENCES worldunit(owner_id)
, FOREIGN KEY(person_id) REFERENCES worldunit(owner_id)
, UNIQUE(owner_id, person_id)
)
;
"""


def get_world_personunit_table_update_treasury_due_paid_sqlstr(
    cash_owner_id: OwnerID,
) -> str:
    return f"""
UPDATE world_personunit
SET _treasury_due_paid = (
    SELECT SUM(block.cash_close-block.cash_start) 
    FROM river_block block
    WHERE block.cash_master='{cash_owner_id}' 
        AND block.dst_owner_id=block.cash_master
        AND block.src_owner_id = world_personunit.person_id
    )
WHERE EXISTS (
    SELECT block.cash_close
    FROM river_block block
    WHERE world_personunit.owner_id='{cash_owner_id}' 
        AND world_personunit.person_id = block.dst_owner_id
)
;
"""


def get_world_personunit_table_update_cred_score_sqlstr(
    cash_owner_id: OwnerID,
) -> str:
    return f"""
UPDATE world_personunit
SET _treasury_cred_score = (
    SELECT SUM(reach_coin_close - reach_coin_start) range_sum
    FROM river_reach reach
    WHERE reach.cash_master = world_personunit.owner_id
        AND reach.src_owner_id = world_personunit.person_id
    )
WHERE world_personunit.owner_id = '{cash_owner_id}'
;
"""


def get_world_personunit_table_update_treasury_voice_rank_sqlstr(
    owner_id: OwnerID,
) -> str:
    return f"""
UPDATE world_personunit
SET _treasury_voice_rank = 
    (
    SELECT rn
    FROM (
        SELECT p2.person_id
        , row_number() over (order by p2._treasury_cred_score DESC) rn
        FROM world_personunit p2
        WHERE p2.owner_id = '{owner_id}'
    ) p3
    WHERE p3.person_id = world_personunit.person_id AND world_personunit.owner_id = '{owner_id}'
    )
WHERE world_personunit.owner_id = '{owner_id}'
;
"""


def get_world_personunit_table_insert_sqlstr(
    x_world: WorldUnit, x_personunit: PersonUnit
) -> str:
    """Create table that holds a the output cred metrics."""
    return f"""
INSERT INTO world_personunit (
  owner_id
, person_id
, _world_cred
, _world_debt
, _world_agenda_cred
, _world_agenda_debt
, _world_agenda_ratio_cred
, _world_agenda_ratio_debt
, _credor_operational
, _debtor_operational
, _treasury_due_paid
, _treasury_due_diff
, _treasury_cred_score
, _treasury_voice_rank
, _treasury_voice_hx_lowest_rank
)
VALUES (
  '{x_world._owner_id}' 
, '{x_personunit.person_id}'
, {sqlite_null(x_personunit._world_cred)} 
, {sqlite_null(x_personunit._world_debt)}
, {sqlite_null(x_personunit._world_agenda_cred)}
, {sqlite_null(x_personunit._world_agenda_debt)}
, {sqlite_null(x_personunit._world_agenda_ratio_cred)}
, {sqlite_null(x_personunit._world_agenda_ratio_debt)}
, {sqlite_bool(x_personunit._credor_operational)}
, {sqlite_bool(x_personunit._debtor_operational)}
, {sqlite_null(x_personunit._treasury_due_paid)}
, {sqlite_null(x_personunit._treasury_due_diff)}
, {sqlite_null(x_personunit._treasury_cred_score)}
, {sqlite_null(x_personunit._treasury_voice_rank)}
, {sqlite_null(x_personunit._treasury_voice_hx_lowest_rank)}
)
;
"""


@dataclass
class PersonDBUnit(PersonUnit):
    owner_id: str = None


def get_personview_dict(
    db_conn: Connection, payer_owner_id: OwnerID
) -> dict[PersonID:PersonDBUnit]:
    sqlstr = f"""
SELECT 
  owner_id
, person_id
, _world_cred
, _world_debt
, _world_agenda_cred
, _world_agenda_debt
, _world_agenda_ratio_cred
, _world_agenda_ratio_debt
, _credor_operational
, _debtor_operational
, _treasury_due_paid
, _treasury_due_diff
, _treasury_cred_score
, _treasury_voice_rank
, _treasury_voice_hx_lowest_rank
FROM world_personunit
WHERE owner_id = '{payer_owner_id}' 
;
"""
    dict_x = {}
    results = db_conn.execute(sqlstr)

    for row in results.fetchall():
        personview_x = PersonDBUnit(
            owner_id=row[0],
            person_id=row[1],
            _world_cred=row[2],
            _world_debt=row[3],
            _world_agenda_cred=row[4],
            _world_agenda_debt=row[5],
            _world_agenda_ratio_cred=row[6],
            _world_agenda_ratio_debt=row[7],
            _credor_operational=row[8],
            _debtor_operational=row[9],
            _treasury_due_paid=row[10],
            _treasury_due_diff=row[11],
            _treasury_cred_score=row[12],
            _treasury_voice_rank=row[13],
            _treasury_voice_hx_lowest_rank=row[14],
        )
        dict_x[personview_x.person_id] = personview_x
    return dict_x


@dataclass
class RiverLedgerUnit:
    owner_id: str
    cash_onset: float
    cash_cease: float
    _personviews: dict[str:PersonDBUnit]
    river_tree_level: int
    block_num: int

    def get_range(self):
        return self.cash_cease - self.cash_onset


def get_river_ledger_unit(
    db_conn: Connection, river_block_x: RiverBlockUnit = None
) -> RiverLedgerUnit:
    personview_x = get_personview_dict(db_conn, river_block_x.dst_owner_id)
    return RiverLedgerUnit(
        owner_id=river_block_x.dst_owner_id,
        cash_onset=river_block_x.cash_start,
        cash_cease=river_block_x.cash_close,
        _personviews=personview_x,
        river_tree_level=river_block_x.river_tree_level,
        block_num=river_block_x.block_num,
    )


# world_ideaunit
def get_world_ideaunit_table_create_sqlstr() -> str:
    """table that holds every road and its owner_id"""
    return """
CREATE TABLE IF NOT EXISTS world_ideaunit (
  owner_id VARCHAR(255) NOT NULL
, idea_road VARCHAR(1000) NOT NULL
)
;
"""


def get_world_ideaunit_row_count(db_conn: Connection, owner_id: str) -> str:
    sqlstr = f"""
{get_row_count_sqlstr("world_ideaunit")} 
WHERE owner_id = '{owner_id}'
;
"""
    return get_single_result(db_conn, sqlstr)


@dataclass
class IdeaCatalog:
    owner_id: str
    idea_road: str


def get_world_ideaunit_table_insert_sqlstr(
    world_ideaunit: IdeaCatalog,
) -> str:
    # return f"""INSERT INTO world_ideaunit (owner_id, idea_road) VALUES ('{world_ideaunit.owner_id}', '{world_ideaunit.idea_road}');"""
    return f"""
INSERT INTO world_ideaunit (
  owner_id
, idea_road
)
VALUES (
  '{world_ideaunit.owner_id}'
, '{create_road_without_root_node(world_ideaunit.idea_road)}'
)
;
"""


def get_world_ideaunit_dict(db_conn: Connection, search_road: RoadUnit = None):
    if search_road is None:
        where_clause = ""
    else:
        search_road_without_root_node = create_road_without_root_node(search_road)
        where_clause = f"WHERE idea_road = '{search_road_without_root_node}'"
    sqlstr = f"""
SELECT 
  owner_id
, idea_road
FROM world_ideaunit
{where_clause}
;
"""
    results = db_conn.execute(sqlstr)

    dict_x = {}
    for row in results.fetchall():
        world_ideaunit_x = IdeaCatalog(owner_id=row[0], idea_road=row[1])
        dict_key = f"{world_ideaunit_x.owner_id} {world_ideaunit_x.idea_road}"
        dict_x[dict_key] = world_ideaunit_x
    return dict_x


# world_idea_factunit
def get_world_idea_factunit_table_create_sqlstr() -> str:
    """table that holds every fact base and pick of every world. missing open/nigh. (clearly not used, maybe add in the future)"""
    return """
CREATE TABLE IF NOT EXISTS world_idea_factunit (
  owner_id VARCHAR(255) NOT NULL
, base VARCHAR(1000) NOT NULL
, pick VARCHAR(1000) NOT NULL
)
;
"""


def get_world_idea_factunit_row_count(db_conn: Connection, owner_id: str) -> str:
    sqlstr = f"""
{get_row_count_sqlstr("world_idea_factunit")} WHERE owner_id = '{owner_id}'
;
"""
    return get_single_result(db_conn, sqlstr)


@dataclass
class FactCatalog:
    owner_id: str
    base: str
    pick: str


def get_world_idea_factunit_table_insert_sqlstr(
    world_idea_factunit: FactCatalog,
) -> str:
    return f"""
INSERT INTO world_idea_factunit (
  owner_id
, base
, pick
)
VALUES (
  '{world_idea_factunit.owner_id}'
, '{world_idea_factunit.base}'
, '{world_idea_factunit.pick}'
)
;
"""


# world_beliefunit
def get_world_beliefunit_table_create_sqlstr() -> str:
    return """
CREATE TABLE IF NOT EXISTS world_beliefunit (
  owner_id VARCHAR(255) NOT NULL
, beliefunit_belief_id VARCHAR(1000) NOT NULL
)
;
"""


def get_world_beliefunit_row_count(db_conn: Connection, owner_id: str) -> str:
    sqlstr = f"""
{get_row_count_sqlstr("world_beliefunit")} WHERE owner_id = '{owner_id}'
;
"""
    return get_single_result(db_conn, sqlstr)


@dataclass
class BeliefUnitCatalog:
    owner_id: str
    beliefunit_belief_id: str


def get_world_beliefunit_table_insert_sqlstr(
    world_beliefunit: BeliefUnitCatalog,
) -> str:
    return f"""
INSERT INTO world_beliefunit (
  owner_id
, beliefunit_belief_id
)
VALUES (
  '{world_beliefunit.owner_id}'
, '{world_beliefunit.beliefunit_belief_id}'
)
;
"""


def get_world_beliefunit_dict(db_conn: Connection) -> dict[str:BeliefUnitCatalog]:
    sqlstr = """
SELECT 
  owner_id
, beliefunit_belief_id
FROM world_beliefunit
;
"""
    results = db_conn.execute(sqlstr)

    dict_x = {}
    for row in results.fetchall():
        world_beliefunit_x = BeliefUnitCatalog(
            owner_id=row[0], beliefunit_belief_id=row[1]
        )
        dict_key = (
            f"{world_beliefunit_x.owner_id} {world_beliefunit_x.beliefunit_belief_id}"
        )
        dict_x[dict_key] = world_beliefunit_x
    return dict_x


def get_calendar_table_create_sqlstr():
    return """
CREATE TABLE IF NOT EXISTS calendar (
  owner_id VARCHAR(255) NOT NULL
, report_time_road VARCHAR(10000) NOT NULL
, report_date_range_start INT NOT NULL
, report_date_range_cease INT NOT NULL
, report_interval_length INT NOT NULL
, report_interval_agenda_task_max_count INT NOT NULL
, report_interval_agenda_state_max_count INT NOT NULL
, time_begin INT NOT NULL
, time_close INT NOT NULL
, agenda_idea_road VARCHAR(255) NOT NULL
, agenda_weight INT NOT NULL
, task INT NOT NULL
, FOREIGN KEY(owner_id) REFERENCES worldunit(owner_id)
)
;
"""


@dataclass
class CalendarReport:
    owner_id: OwnerID = (None,)
    time_road: RoadUnit = None
    date_range_start: int = None
    interval_count: int = None
    interval_length: int = None
    agenda_max_count_task: int = None
    agenda_max_count_state: int = None

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
class CalendarAgendaUnit:
    calendarreport: CalendarReport
    time_begin: int
    time_close: int
    agenda_idea_road: RoadUnit
    agenda_weight: float
    task: bool


def get_calendar_table_insert_sqlstr(x_obj: CalendarAgendaUnit):
    return f"""
INSERT INTO calendar (
  owner_id
, report_time_road
, report_date_range_start
, report_date_range_cease
, report_interval_length
, report_interval_agenda_task_max_count
, report_interval_agenda_state_max_count
, time_begin
, time_close
, agenda_idea_road
, agenda_weight
, task)
VALUES (
  '{x_obj.calendarreport.owner_id}'
, '{x_obj.calendarreport.time_road}'
, {sqlite_null(x_obj.calendarreport.date_range_start)}
, {sqlite_null(x_obj.calendarreport.get_date_range_cease())}
, {sqlite_null(x_obj.calendarreport.interval_length)}
, {sqlite_null(x_obj.calendarreport.agenda_max_count_task)}
, {sqlite_null(x_obj.calendarreport.agenda_max_count_state)}
, {sqlite_null(x_obj.time_begin)}
, {sqlite_null(x_obj.time_close)}
, '{x_obj.agenda_idea_road}'
, {sqlite_null(x_obj.agenda_weight)}
, {sqlite_bool(x_obj.task)}
)
;
"""


def get_world_personunit_table_insert_sqlstr(
    x_world: WorldUnit, x_personunit: PersonUnit
) -> str:
    """Create table that holds a the output cred metrics."""
    return f"""
INSERT INTO world_personunit (
  owner_id
, person_id
, _world_cred
, _world_debt
, _world_agenda_cred
, _world_agenda_debt
, _world_agenda_ratio_cred
, _world_agenda_ratio_debt
, _credor_operational
, _debtor_operational
, _treasury_due_paid
, _treasury_due_diff
, _treasury_cred_score
, _treasury_voice_rank
, _treasury_voice_hx_lowest_rank
)
VALUES (
  '{x_world._owner_id}' 
, '{x_personunit.person_id}'
, {sqlite_null(x_personunit._world_cred)} 
, {sqlite_null(x_personunit._world_debt)}
, {sqlite_null(x_personunit._world_agenda_cred)}
, {sqlite_null(x_personunit._world_agenda_debt)}
, {sqlite_null(x_personunit._world_agenda_ratio_cred)}
, {sqlite_null(x_personunit._world_agenda_ratio_debt)}
, {sqlite_bool(x_personunit._credor_operational)}
, {sqlite_bool(x_personunit._debtor_operational)}
, {sqlite_null(x_personunit._treasury_due_paid)}
, {sqlite_null(x_personunit._treasury_due_diff)}
, {sqlite_null(x_personunit._treasury_cred_score)}
, {sqlite_null(x_personunit._treasury_voice_rank)}
, {sqlite_null(x_personunit._treasury_voice_hx_lowest_rank)}
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
    list_x = [get_worldunit_table_create_sqlstr()]
    list_x.append(get_world_idea_factunit_table_create_sqlstr())
    list_x.append(get_world_ideaunit_table_create_sqlstr())
    list_x.append(get_world_personunit_table_create_sqlstr())
    list_x.append(get_river_block_table_create_sqlstr())
    list_x.append(get_river_circle_table_create_sqlstr())
    list_x.append(get_river_reach_table_create_sqlstr())
    list_x.append(get_world_beliefunit_table_create_sqlstr())
    list_x.append(get_calendar_table_create_sqlstr())
    return list_x
