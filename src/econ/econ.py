from src._road.road import (
    RoadUnit,
    create_road,
    default_road_delimiter_if_none,
    OwnerID,
    HealerID,
    PersonID,
    RealID,
    validate_roadnode,
)
from src._road.worlddir import EconDir
from src.agenda.party import partylink_shop
from src.agenda.agenda import AgendaUnit, get_from_json as get_agenda_from_json
from src._instrument.file import set_dir, delete_dir, open_file, dir_files
from src.econ.job_creator import (
    PersonID,
    get_econ_roles_dir,
    get_econ_jobs_dir,
    save_role_file,
    save_job_file,
    get_role_file,
    get_job_file,
    get_file_name,
    create_job_file_from_role_file,
)
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from src.econ.treasury_sqlstr import (
    get_partytreasuryunit_dict,
    get_agenda_partyunit_table_insert_sqlstr,
    get_agenda_partyunit_table_update_treasury_due_paid_sqlstr,
    get_agenda_partyunit_table_update_credit_score_sqlstr,
    get_agenda_partyunit_table_update_treasury_voice_rank_sqlstr,
    get_river_block_table_delete_sqlstr,
    get_river_block_table_insert_sqlstr,
    get_river_circle_table_insert_sqlstr,
    get_river_reach_table_final_insert_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
    get_agendaunit_table_insert_sqlstr,
    get_river_ledger_unit,
    PartyDBUnit,
    RiverLedgerUnit,
    RiverBlockUnit,
    PartyTreasuryUnit,
    IdeaCatalog,
    get_agenda_ideaunit_table_insert_sqlstr,
    get_agenda_ideaunit_dict,
    BeliefCatalog,
    get_agenda_idea_beliefunit_table_insert_sqlstr,
    GroupUnitCatalog,
    get_agenda_groupunit_table_insert_sqlstr,
    get_agenda_groupunit_dict,
    get_agendatreasuryunits_dict,
    get_agendaunit_update_sqlstr,
    CalendarReport,
    CalendarIntentUnit,
    get_calendar_table_insert_sqlstr,
    get_calendar_table_delete_sqlstr,
)


def temp_real_id():
    return "ex_econ04"


def get_temp_env_healer_id():
    return "ex_healer04"


def temp_person_id():
    return "ex_person04"


def get_temp_env_problem_id():
    return "ex_problem04"


class IntentBaseDoesNotExistException(Exception):
    pass


def treasury_db_filename() -> str:
    return "treasury.db"


@dataclass
class EconUnit:
    econdir: EconDir
    _treasury_db = None

    # Admin
    def econ_dir(self) -> str:
        return self.econdir.econ_dir()

    def set_econ_dirs(self, in_memory_treasury: bool = None):
        set_dir(x_path=self.econdir.econ_dir())
        set_dir(x_path=self.get_roles_dir())
        set_dir(x_path=self.get_jobs_dir())
        self._create_treasury_db(in_memory=in_memory_treasury, overwrite=True)

    def set_road_delimiter(self, new_road_delimiter: str):
        self._road_delimiter = default_road_delimiter_if_none(new_road_delimiter)

    # treasurying
    def set_role_voice_ranks(self, owner_id: OwnerID, sort_order: str):
        if sort_order == "descending":
            owner_role = self.get_role_file(owner_id)
            for count_x, x_partyunit in enumerate(owner_role._partys.values()):
                x_partyunit.set_treasury_voice_rank(count_x)
            save_role_file(self.econ_dir(), owner_role)

    def set_agenda_treasury_attrs(self, x_owner_id: OwnerID):
        x_agenda = self.get_job_file(x_owner_id)

        for groupunit_x in x_agenda._groups.values():
            if groupunit_x._treasury_partylinks != None:
                groupunit_x.clear_partylinks()
                ic = get_agenda_ideaunit_dict(
                    self.get_treasury_conn(),
                    groupunit_x._treasury_partylinks,
                )
                for agenda_ideaunit in ic.values():
                    if x_owner_id != agenda_ideaunit.owner_id:
                        partylink_x = partylink_shop(party_id=agenda_ideaunit.owner_id)
                        groupunit_x.set_partylink(partylink_x)
        self.save_job_file(x_agenda)
        self.refresh_treasury_job_agendas_data()

    def set_credit_flow_for_agenda(
        self, owner_id: OwnerID, max_blocks_count: int = None
    ):
        self._clear_all_source_river_data(owner_id)
        if max_blocks_count is None:
            max_blocks_count = 40
        self._set_river_blocks(owner_id, max_blocks_count)
        self._set_partytreasuryunits_circles(owner_id)

    def _set_river_blocks(self, x_owner_id: OwnerID, max_blocks_count: int):
        # Transformations in river_block loop
        general_circle = [self._get_root_river_ledger_unit(x_owner_id)]
        blocks_count = 0  # Transformations in river_block loop
        while blocks_count < max_blocks_count and general_circle != []:
            parent_agenda_ledger = general_circle.pop(0)
            ledgers_len = len(parent_agenda_ledger._partyviews.values())
            parent_range = parent_agenda_ledger.get_range()
            parent_close = parent_agenda_ledger.cash_cease

            # Transformations in river_block loop
            coin_onset = parent_agenda_ledger.cash_onset
            ledgers_count = 0
            for x_child_ledger in parent_agenda_ledger._partyviews.values():
                ledgers_count += 1

                coin_range = parent_range * x_child_ledger._agenda_intent_ratio_credit
                coin_close = coin_onset + coin_range

                # implies last object in dict
                if ledgers_count == ledgers_len and coin_close != parent_close:
                    coin_close = parent_close

                river_block_x = RiverBlockUnit(
                    cash_owner_id=x_owner_id,
                    src_owner_id=x_child_ledger.owner_id,
                    dst_owner_id=x_child_ledger.party_id,
                    cash_start=coin_onset,
                    cash_close=coin_close,
                    block_num=blocks_count,
                    parent_block_num=parent_agenda_ledger.block_num,
                    river_tree_level=parent_agenda_ledger.river_tree_level + 1,
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

            if river_block_x.block_returned() == False:
                river_ledger_x = get_river_ledger_unit(treasury_conn, river_block_x)

        return river_ledger_x

    def _clear_all_source_river_data(self, owner_id: str):
        with self.get_treasury_conn() as treasury_conn:
            block_s = get_river_block_table_delete_sqlstr(owner_id)
            treasury_conn.execute(block_s)

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

    def _set_partytreasuryunits_circles(self, owner_id: str):
        with self.get_treasury_conn() as treasury_conn:
            treasury_conn.execute(get_river_circle_table_insert_sqlstr(owner_id))
            treasury_conn.execute(get_river_reach_table_final_insert_sqlstr(owner_id))
            treasury_conn.execute(
                get_agenda_partyunit_table_update_treasury_due_paid_sqlstr(owner_id)
            )
            treasury_conn.execute(
                get_agenda_partyunit_table_update_credit_score_sqlstr(owner_id)
            )
            treasury_conn.execute(
                get_agenda_partyunit_table_update_treasury_voice_rank_sqlstr(owner_id)
            )

            sal_partytreasuryunits = get_partytreasuryunit_dict(treasury_conn, owner_id)
            x_agenda = self.get_job_file(owner_id=owner_id)
            set_treasury_partytreasuryunits_to_agenda_partyunits(
                x_agenda, sal_partytreasuryunits
            )
            self.save_job_file(x_agenda)

    def get_partytreasuryunits(self, owner_id: str) -> dict[str:PartyTreasuryUnit]:
        with self.get_treasury_conn() as treasury_conn:
            partytreasuryunits = get_partytreasuryunit_dict(treasury_conn, owner_id)
        return partytreasuryunits

    def refresh_treasury_job_agendas_data(self, in_memory: bool = None):
        if in_memory is None and self._treasury_db != None:
            in_memory = True
        self._create_treasury_db(in_memory=in_memory, overwrite=True)
        self._treasury_populate_agendas_data()

    def _treasury_populate_agendas_data(self):
        for file_name in self.get_jobs_dir_file_names_list():
            agenda_json = open_file(self.get_jobs_dir(), file_name)
            agendaunit_x = get_agenda_from_json(x_agenda_json=agenda_json)
            agendaunit_x.calc_agenda_metrics()

            self._treasury_insert_agendaunit(agendaunit_x)
            self._treasury_insert_partyunit(agendaunit_x)
            self._treasury_insert_groupunit(agendaunit_x)
            self._treasury_insert_ideaunit(agendaunit_x)
            self._treasury_insert_belief(agendaunit_x)

    def _treasury_insert_agendaunit(self, agendaunit_x: AgendaUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            cur.execute(get_agendaunit_table_insert_sqlstr(x_agenda=agendaunit_x))

    def _treasury_set_agendaunit_attrs(self, agenda: AgendaUnit):
        with self.get_treasury_conn() as treasury_conn:
            treasury_conn.execute(get_agendaunit_update_sqlstr(agenda))

    def _treasury_insert_partyunit(self, agendaunit_x: AgendaUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            for x_partyunit in agendaunit_x._partys.values():
                sqlstr = get_agenda_partyunit_table_insert_sqlstr(
                    agendaunit_x, x_partyunit
                )
                cur.execute(sqlstr)

    def _treasury_insert_groupunit(self, agendaunit_x: AgendaUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            for groupunit_x in agendaunit_x._groups.values():
                agenda_groupunit_x = GroupUnitCatalog(
                    owner_id=agendaunit_x._owner_id,
                    groupunit_group_id=groupunit_x.group_id,
                    treasury_partylinks=groupunit_x._treasury_partylinks,
                )
                sqlstr = get_agenda_groupunit_table_insert_sqlstr(agenda_groupunit_x)
                cur.execute(sqlstr)

    def _treasury_insert_ideaunit(self, agendaunit_x: AgendaUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            for idea_x in agendaunit_x._idea_dict.values():
                agenda_ideaunit_x = IdeaCatalog(
                    agendaunit_x._owner_id, idea_x.get_road()
                )
                sqlstr = get_agenda_ideaunit_table_insert_sqlstr(agenda_ideaunit_x)
                cur.execute(sqlstr)

    def _treasury_insert_belief(self, agendaunit_x: AgendaUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            for belief_x in agendaunit_x._idearoot._beliefunits.values():
                agenda_idea_beliefunit_x = BeliefCatalog(
                    owner_id=agendaunit_x._owner_id,
                    base=belief_x.base,
                    pick=belief_x.pick,
                )
                sqlstr = get_agenda_idea_beliefunit_table_insert_sqlstr(
                    agenda_idea_beliefunit_x
                )
                cur.execute(sqlstr)

    def get_treasury_conn(self) -> Connection:
        if self._treasury_db is None:
            return sqlite3_connect(self.get_treasury_db_path())
        else:
            return self._treasury_db

    def _create_treasury_db(
        self, in_memory: bool = None, overwrite: bool = None
    ) -> Connection:
        if overwrite:
            self._delete_treasury()

        treasury_file_new = True
        if in_memory:
            self._treasury_db = sqlite3_connect(":memory:")
        else:
            sqlite3_connect(self.get_treasury_db_path())

        if treasury_file_new:
            with self.get_treasury_conn() as treasury_conn:
                for sqlstr in get_create_table_if_not_exist_sqlstrs():
                    treasury_conn.execute(sqlstr)

    def _delete_treasury(self):
        self._treasury_db = None
        delete_dir(self.get_treasury_db_path())

    def get_treasury_db_path(self):
        return f"{self.econdir.econ_dir()}/{treasury_db_filename()}"

    # roles dir management
    def get_roles_dir(self):
        return get_econ_roles_dir(self.econdir.econ_dir())

    def save_role_file(self, x_agenda: AgendaUnit):
        x_agenda.set_real_id(self.econdir.real_id)
        save_role_file(self.econdir.econ_dir(), x_agenda)

    def get_role_file(self, owner_id: PersonID) -> AgendaUnit:
        return get_role_file(self.econdir.econ_dir(), owner_id)

    def delete_role_file(self, x_owner_id: PersonID):
        delete_dir(f"{self.get_roles_dir()}/{get_file_name(x_owner_id)}")

    # jobs dir management
    def get_jobs_dir(self):
        return get_econ_jobs_dir(self.econdir.econ_dir())

    def save_job_file(self, x_agenda: AgendaUnit):
        x_agenda.set_real_id(self.econdir.real_id)
        save_job_file(self.econdir.econ_dir(), x_agenda)

    def create_job_file_from_role_file(self, person_id: PersonID) -> AgendaUnit:
        return create_job_file_from_role_file(self.econdir.econ_dir(), person_id)

    def get_job_file(self, owner_id: str) -> AgendaUnit:
        econ_dir = self.econdir.econ_dir()
        return get_job_file(econ_dir, owner_id, return_None_if_missing=False)

    def delete_job_file(self, x_owner_id: PersonID):
        delete_dir(f"{self.get_jobs_dir()}/{get_file_name(x_owner_id)}")

    def modify_job_owner_id(self, old_owner_id: OwnerID, new_owner_id: OwnerID):
        x_agenda = self.get_job_file(old_owner_id)
        x_agenda.set_owner_id(new_owner_id)
        self.save_job_file(x_agenda)
        self.delete_job_file(old_owner_id)

    def get_jobs_dir_file_names_list(self):
        return list(dir_files(dir_path=self.get_jobs_dir()).keys())

    def insert_intent_into_treasury(
        self, x_agendaunit: AgendaUnit, x_calendarreport: CalendarReport
    ):
        if x_agendaunit.idea_exists(x_calendarreport.time_road) == False:
            raise IntentBaseDoesNotExistException(
                f"Intent base cannot be '{x_calendarreport.time_road}' because it does not exist in agenda '{x_agendaunit._owner_id}'."
            )

        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()

            del_sqlstr = get_calendar_table_delete_sqlstr(x_calendarreport.owner_id)
            cur.execute(del_sqlstr)
            for _ in range(x_calendarreport.interval_count):
                x_agendaunit.set_belief(
                    base=x_calendarreport.time_road,
                    pick=x_calendarreport.time_road,
                    open=x_calendarreport.get_interval_begin(_),
                    nigh=x_calendarreport.get_interval_close(_),
                )
                x_intent_items = x_agendaunit.get_intent_dict(
                    base=x_calendarreport.time_road
                )
                for intent_item in x_intent_items.values():
                    x_calendarintentunit = CalendarIntentUnit(
                        calendarreport=x_calendarreport,
                        time_begin=x_calendarreport.get_interval_begin(_),
                        time_close=x_calendarreport.get_interval_close(_),
                        intent_idea_road=intent_item.get_road(),
                        intent_weight=intent_item._agenda_importance,
                        task=intent_item._task,
                    )
                    sqlstr = get_calendar_table_insert_sqlstr(x_calendarintentunit)
                    cur.execute(sqlstr)


def econunit_shop(x_econdir: EconDir, in_memory_treasury: bool = None) -> EconUnit:
    if in_memory_treasury is None:
        in_memory_treasury = True

    x_econdir.real_id = validate_roadnode(x_econdir.real_id, x_econdir._road_delimiter)
    econ_x = EconUnit(x_econdir)
    econ_x.set_econ_dirs(in_memory_treasury=in_memory_treasury)
    return econ_x


def set_treasury_partytreasuryunits_to_agenda_partyunits(
    x_agenda: AgendaUnit, partytreasuryunits: dict[str:PartyTreasuryUnit]
):
    for x_partyunit in x_agenda._partys.values():
        x_partyunit.clear_treasurying_data()
        partytreasuryunit = partytreasuryunits.get(x_partyunit.party_id)
        if partytreasuryunit != None:
            x_partyunit.set_treasurying_data(
                due_paid=partytreasuryunit.due_total,
                due_diff=partytreasuryunit.due_diff,
                credit_score=partytreasuryunit.credit_score,
                voice_rank=partytreasuryunit.voice_rank,
            )
