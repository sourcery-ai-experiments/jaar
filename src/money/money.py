from src._instrument.file import delete_dir
from src._road.jaar_config import default_river_blocks_count
from src._road.road import OwnerID
from src._world.other import otherlink_shop
from src._world.world import WorldUnit
from src.listen.userhub import UserHub
from src.money.treasury_sqlstr import (
    get_othertreasuryunit_dict,
    get_world_otherunit_table_insert_sqlstr,
    get_world_otherunit_table_update_treasury_due_paid_sqlstr as update_treasury_due_paid_sqlstr,
    get_world_otherunit_table_update_cred_score_sqlstr as update_cred_score_sqlstr,
    get_world_otherunit_table_update_treasury_voice_rank_sqlstr as update_treasury_voice_rank_sqlstr,
    get_river_block_table_delete_sqlstr,
    get_river_block_table_insert_sqlstr,
    get_river_circle_table_insert_sqlstr,
    get_river_reach_table_final_insert_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
    get_worldunit_table_insert_sqlstr,
    get_river_ledger_unit,
    OtherDBUnit,
    RiverLedgerUnit,
    RiverBlockUnit,
    OtherTreasuryUnit,
    IdeaCatalog,
    get_world_ideaunit_table_insert_sqlstr,
    get_world_ideaunit_dict,
    FactCatalog,
    get_world_idea_factunit_table_insert_sqlstr,
    BeliefUnitCatalog,
    get_world_beliefunit_table_insert_sqlstr,
    get_world_beliefunit_dict,
    get_worldtreasuryunits_dict,
    get_worldunit_update_sqlstr,
    CalendarReport,
    CalendarAgendaUnit,
    get_calendar_table_insert_sqlstr,
    get_calendar_table_delete_sqlstr,
)
from sqlite3 import connect as sqlite3_connect, Connection
from dataclasses import dataclass


class AgendaBaseDoesNotExistException(Exception):
    pass


@dataclass
class MoneyUnit:
    userhub: UserHub
    _treasury_db = None

    # treasurying
    def set_cred_flow_for_world(self, owner_id: OwnerID, max_blocks_count: int = None):
        self._clear_all_source_river_data(owner_id)
        if max_blocks_count is None:
            max_blocks_count = default_river_blocks_count()
        self._set_river_blocks(owner_id, max_blocks_count)
        self._set_othertreasuryunits_circles(owner_id)

    def _clear_all_source_river_data(self, owner_id: str):
        with self.get_treasury_conn() as treasury_conn:
            block_s = get_river_block_table_delete_sqlstr(owner_id)
            treasury_conn.execute(block_s)

    def _set_river_blocks(self, x_owner_id: OwnerID, max_blocks_count: int):
        # Transformations in river_block loop
        general_circle = [self._get_root_river_ledger_unit(x_owner_id)]
        blocks_count = 0  # Transformations in river_block loop
        while blocks_count < max_blocks_count and general_circle != []:
            parent_world_ledger = general_circle.pop(0)
            ledgers_len = len(parent_world_ledger._otherviews.values())
            parent_range = parent_world_ledger.get_range()
            parent_close = parent_world_ledger.cash_cease

            # Transformations in river_block loop
            coin_onset = parent_world_ledger.cash_onset
            ledgers_count = 0
            for x_child_ledger in parent_world_ledger._otherviews.values():
                ledgers_count += 1

                coin_range = parent_range * x_child_ledger._world_agenda_ratio_cred
                coin_close = coin_onset + coin_range

                # implies last object in dict
                if ledgers_count == ledgers_len and coin_close != parent_close:
                    coin_close = parent_close

                river_block_x = RiverBlockUnit(
                    cash_owner_id=x_owner_id,
                    src_owner_id=x_child_ledger.owner_id,
                    dst_owner_id=x_child_ledger.other_id,
                    cash_start=coin_onset,
                    cash_close=coin_close,
                    block_num=blocks_count,
                    parent_block_num=parent_world_ledger.block_num,
                    river_tree_level=parent_world_ledger.river_tree_level + 1,
                )
                river_ledger_x = self._insert_river_block_grab_river_ledger(
                    river_block_x
                )
                if river_ledger_x != None:
                    general_circle.append(river_ledger_x)

                blocks_count += 1
                if blocks_count >= max_blocks_count:
                    break

                # set coin_onset for next loop
                coin_onset += coin_range

    def _insert_river_block_grab_river_ledger(
        self, river_block_x: RiverBlockUnit
    ) -> RiverLedgerUnit:
        river_ledger_x = None

        with self.get_treasury_conn() as treasury_conn:
            treasury_conn.execute(get_river_block_table_insert_sqlstr(river_block_x))

            if river_block_x.block_returned() is False:
                river_ledger_x = get_river_ledger_unit(treasury_conn, river_block_x)

        return river_ledger_x

    def _get_root_river_ledger_unit(self, owner_id: str) -> RiverLedgerUnit:
        default_cash_onset = 0.0
        default_cash_cease = 1.0
        default_root_river_tree_level = 0
        default_root_block_num = None  # maybe 1?
        default_root_parent_block_num = None
        root_river_block = RiverBlockUnit(
            cash_owner_id=owner_id,
            src_owner_id=None,
            dst_owner_id=owner_id,
            cash_start=default_cash_onset,
            cash_close=default_cash_cease,
            block_num=default_root_block_num,
            parent_block_num=default_root_parent_block_num,
            river_tree_level=default_root_river_tree_level,
        )
        with self.get_treasury_conn() as treasury_conn:
            source_river_ledger = get_river_ledger_unit(treasury_conn, root_river_block)
        return source_river_ledger

    def _set_othertreasuryunits_circles(self, owner_id: str):
        with self.get_treasury_conn() as treasury_conn:
            treasury_conn.execute(get_river_circle_table_insert_sqlstr(owner_id))
            treasury_conn.execute(get_river_reach_table_final_insert_sqlstr(owner_id))
            treasury_conn.execute(update_treasury_due_paid_sqlstr(owner_id))
            treasury_conn.execute(update_cred_score_sqlstr(owner_id))
            treasury_conn.execute(update_treasury_voice_rank_sqlstr(owner_id))

            sal_othertreasuryunits = get_othertreasuryunit_dict(treasury_conn, owner_id)
            x_world = self.userhub.get_job_world(owner_id=owner_id)
            set_treasury_othertreasuryunits_to_world_otherunits(
                x_world, sal_othertreasuryunits
            )
            self.userhub.save_job_world(x_world)

    def get_othertreasuryunits(self, owner_id: str) -> dict[str:OtherTreasuryUnit]:
        with self.get_treasury_conn() as treasury_conn:
            othertreasuryunits = get_othertreasuryunit_dict(treasury_conn, owner_id)
        return othertreasuryunits

    def refresh_treasury_job_worlds_data(self, in_memory: bool = None):
        if in_memory is None and self._treasury_db != None:
            in_memory = True
        self.create_treasury_db(in_memory=in_memory, overwrite=True)
        self._treasury_populate_worlds_data()

    def _treasury_populate_worlds_data(self):
        for person_id in self.userhub.get_jobs_dir_file_names_list():
            worldunit_x = self.userhub.get_job_world(person_id)
            worldunit_x.calc_world_metrics()

            self._treasury_insert_worldunit(worldunit_x)
            self._treasury_insert_otherunit(worldunit_x)
            self._treasury_insert_beliefunit(worldunit_x)
            self._treasury_insert_ideaunit(worldunit_x)
            self._treasury_insert_fact(worldunit_x)

    def _treasury_insert_worldunit(self, worldunit_x: WorldUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            cur.execute(get_worldunit_table_insert_sqlstr(x_world=worldunit_x))

    def _treasury_set_worldunit_attrs(self, world: WorldUnit):
        with self.get_treasury_conn() as treasury_conn:
            treasury_conn.execute(get_worldunit_update_sqlstr(world))

    def _treasury_insert_otherunit(self, worldunit_x: WorldUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            for x_otherunit in worldunit_x._others.values():
                sqlstr = get_world_otherunit_table_insert_sqlstr(
                    worldunit_x, x_otherunit
                )
                cur.execute(sqlstr)

    def _treasury_insert_beliefunit(self, worldunit_x: WorldUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            for beliefunit_x in worldunit_x._beliefs.values():
                world_beliefunit_x = BeliefUnitCatalog(
                    owner_id=worldunit_x._owner_id,
                    beliefunit_belief_id=beliefunit_x.belief_id,
                )
                sqlstr = get_world_beliefunit_table_insert_sqlstr(world_beliefunit_x)
                cur.execute(sqlstr)

    def _treasury_insert_ideaunit(self, worldunit_x: WorldUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            for idea_x in worldunit_x._idea_dict.values():
                world_ideaunit_x = IdeaCatalog(worldunit_x._owner_id, idea_x.get_road())
                sqlstr = get_world_ideaunit_table_insert_sqlstr(world_ideaunit_x)
                cur.execute(sqlstr)

    def _treasury_insert_fact(self, worldunit_x: WorldUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            for fact_x in worldunit_x._idearoot._factunits.values():
                world_idea_factunit_x = FactCatalog(
                    owner_id=worldunit_x._owner_id,
                    base=fact_x.base,
                    pick=fact_x.pick,
                )
                sqlstr = get_world_idea_factunit_table_insert_sqlstr(
                    world_idea_factunit_x
                )
                cur.execute(sqlstr)

    def get_treasury_conn(self) -> Connection:
        if self._treasury_db is None:
            return self.userhub.treasury_db_file_conn()
        else:
            return self._treasury_db

    def create_treasury_db(
        self, in_memory: bool = None, overwrite: bool = None
    ) -> Connection:
        if overwrite:
            self._treasury_db = None
            self.userhub.delete_treasury_db_file()

        treasury_file_new = True
        if in_memory:
            self._treasury_db = sqlite3_connect(":memory:")
        else:
            self.userhub.create_treasury_db_file()

        if treasury_file_new:
            with self.get_treasury_conn() as treasury_conn:
                for sqlstr in get_create_table_if_not_exist_sqlstrs():
                    treasury_conn.execute(sqlstr)

    def insert_agenda_into_treasury(
        self, x_worldunit: WorldUnit, x_calendarreport: CalendarReport
    ):
        if x_worldunit.idea_exists(x_calendarreport.time_road) is False:
            raise AgendaBaseDoesNotExistException(
                f"Agenda base cannot be '{x_calendarreport.time_road}' because it does not exist in world '{x_worldunit._owner_id}'."
            )

        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()

            del_sqlstr = get_calendar_table_delete_sqlstr(x_calendarreport.owner_id)
            cur.execute(del_sqlstr)
            for _ in range(x_calendarreport.interval_count):
                x_worldunit.set_fact(
                    base=x_calendarreport.time_road,
                    pick=x_calendarreport.time_road,
                    open=x_calendarreport.get_interval_begin(_),
                    nigh=x_calendarreport.get_interval_close(_),
                )
                x_agenda_items = x_worldunit.get_agenda_dict(
                    base=x_calendarreport.time_road
                )
                for agenda_item in x_agenda_items.values():
                    x_calendaragendaunit = CalendarAgendaUnit(
                        calendarreport=x_calendarreport,
                        time_begin=x_calendarreport.get_interval_begin(_),
                        time_close=x_calendarreport.get_interval_close(_),
                        agenda_idea_road=agenda_item.get_road(),
                        agenda_weight=agenda_item._world_importance,
                        task=agenda_item._task,
                    )
                    sqlstr = get_calendar_table_insert_sqlstr(x_calendaragendaunit)
                    cur.execute(sqlstr)

    # exporting metrics to world files
    def set_role_voice_ranks(self, owner_id: OwnerID, sort_order: str):
        if sort_order == "descending":
            owner_role = self.userhub.get_role_world(owner_id)
            for count_x, x_otherunit in enumerate(owner_role._others.values()):
                x_otherunit.set_treasury_voice_rank(count_x)
            self.userhub.save_role_world(owner_role)


def moneyunit_shop(x_userhub: UserHub, in_memory_treasury: bool = None) -> MoneyUnit:
    if in_memory_treasury is None:
        in_memory_treasury = True

    x_moneyunit = MoneyUnit(x_userhub)
    x_moneyunit.create_treasury_db(in_memory=in_memory_treasury)
    return x_moneyunit


def set_treasury_othertreasuryunits_to_world_otherunits(
    x_world: WorldUnit, othertreasuryunits: dict[str:OtherTreasuryUnit]
):
    for x_otherunit in x_world._others.values():
        x_otherunit.clear_treasurying_data()
        othertreasuryunit = othertreasuryunits.get(x_otherunit.other_id)
        if othertreasuryunit != None:
            x_otherunit.set_treasury_attr(
                _treasury_due_paid=othertreasuryunit.due_total,
                _treasury_due_diff=othertreasuryunit.due_diff,
                cred_score=othertreasuryunit.cred_score,
                voice_rank=othertreasuryunit.voice_rank,
            )
