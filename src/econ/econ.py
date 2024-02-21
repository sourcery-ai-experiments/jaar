from src._road.road import (
    RoadUnit,
    create_road,
    default_road_delimiter_if_none,
    WorkerID,
    HealerID,
    PersonID,
    PartyID,
    EconID,
    validate_roadnode,
)
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as get_agenda_from_json,
    partylink_shop,
)
from src.instrument.file import (
    set_dir,
    delete_dir,
    save_file,
    open_file,
    dir_files,
)
from src.instrument.python import get_empty_dict_if_none
from src.econ.clerk import ClerkUnit, clerkunit_shop, ClerkID
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


def get_temp_env_econ_id():
    return "ex_econ04"


def get_temp_env_healer_id():
    return "ex_healer04"


def get_temp_env_person_id():
    return "ex_person04"


def get_temp_env_problem_id():
    return "ex_problem04"


class IntentBaseDoesNotExistException(Exception):
    pass


def treasury_db_filename() -> str:
    return "treasury.db"


@dataclass
class EconUnit:
    econ_id: EconID = None
    econ_dir: str = None
    _manager_person_id: HealerID = None
    _clerkunits: dict[str:ClerkUnit] = None
    _treasury_db = None
    _road_delimiter: str = None

    # Admin
    def set_econ_id(self, econ_id: str):
        self.econ_id = validate_roadnode(econ_id, self._road_delimiter)

    def get_object_root_dir(self):
        return self.econ_dir

    def _create_main_file_if_null(self, x_dir):
        econ_file_name = "econ.json"
        save_file(
            dest_dir=x_dir,
            file_name=econ_file_name,
            file_text="",
        )

    def set_econ_dirs(self, in_memory_treasury: bool = None):
        agendas_dir = self.get_forum_dir()
        clerkunits_dir = self.get_clerkunits_dir()
        set_dir(x_path=self.get_object_root_dir())
        set_dir(x_path=agendas_dir)
        set_dir(x_path=clerkunits_dir)
        self._create_main_file_if_null(x_dir=self.get_object_root_dir())
        self._create_treasury_db(in_memory=in_memory_treasury, overwrite=True)

    def set_road_delimiter(self, new_road_delimiter: str):
        self._road_delimiter = default_road_delimiter_if_none(new_road_delimiter)

    # treasurying
    def set_voice_ranks(self, worker_id: WorkerID, sort_order: str):
        if sort_order == "descretional":
            x_clerk = self.get_clerkunit(worker_id)
            x_role = x_clerk.get_role()
            for count_x, x_partyunit in enumerate(x_role._partys.values()):
                x_partyunit.set_treasury_voice_rank(count_x)
            x_clerk.set_role(x_role)
            x_clerk.save_refreshed_job_to_forum()

    def set_agenda_treasury_attrs(self, x_worker_id: WorkerID):
        x_agenda = self.get_job_agenda_file(x_worker_id)

        for groupunit_x in x_agenda._groups.values():
            if groupunit_x._treasury_partylinks != None:
                groupunit_x.clear_partylinks()
                ic = get_agenda_ideaunit_dict(
                    self.get_treasury_conn(),
                    groupunit_x._treasury_partylinks,
                )
                for agenda_ideaunit in ic.values():
                    if x_worker_id != agenda_ideaunit.worker_id:
                        partylink_x = partylink_shop(party_id=agenda_ideaunit.worker_id)
                        groupunit_x.set_partylink(partylink_x)
        self.save_job_agenda_to_forum(x_agenda)
        self.refresh_treasury_job_agendas_data()

    def set_credit_flow_for_agenda(
        self, worker_id: WorkerID, max_blocks_count: int = None
    ):
        self._clear_all_source_river_data(worker_id)
        if max_blocks_count is None:
            max_blocks_count = 40
        self._set_river_blocks(worker_id, max_blocks_count)
        self._set_partytreasuryunits_circles(worker_id)

    def _set_river_blocks(self, x_worker_id: WorkerID, max_blocks_count: int):
        # changes in river_block loop
        general_circle = [self._get_root_river_ledger_unit(x_worker_id)]
        blocks_count = 0  # changes in river_block loop
        while blocks_count < max_blocks_count and general_circle != []:
            parent_agenda_ledger = general_circle.pop(0)
            ledgers_len = len(parent_agenda_ledger._partyviews.values())
            parent_range = parent_agenda_ledger.get_range()
            parent_close = parent_agenda_ledger.cash_cease

            # changes in river_block loop
            curr_onset = parent_agenda_ledger.cash_onset
            ledgers_count = 0
            for x_child_ledger in parent_agenda_ledger._partyviews.values():
                ledgers_count += 1

                curr_range = parent_range * x_child_ledger._agenda_intent_ratio_credit
                curr_close = curr_onset + curr_range

                # implies last object in dict
                if ledgers_count == ledgers_len and curr_close != parent_close:
                    curr_close = parent_close

                river_block_x = RiverBlockUnit(
                    cash_worker_id=x_worker_id,
                    src_worker_id=x_child_ledger.worker_id,
                    dst_worker_id=x_child_ledger.party_id,
                    cash_start=curr_onset,
                    cash_close=curr_close,
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

                # change curr_onset for next
                curr_onset += curr_range

    def _insert_river_block_grab_river_ledger(
        self, river_block_x: RiverBlockUnit
    ) -> RiverLedgerUnit:
        river_ledger_x = None

        with self.get_treasury_conn() as treasury_conn:
            treasury_conn.execute(get_river_block_table_insert_sqlstr(river_block_x))

            if river_block_x.block_returned() == False:
                river_ledger_x = get_river_ledger_unit(treasury_conn, river_block_x)

        return river_ledger_x

    def _clear_all_source_river_data(self, worker_id: str):
        with self.get_treasury_conn() as treasury_conn:
            block_s = get_river_block_table_delete_sqlstr(worker_id)
            treasury_conn.execute(block_s)

    def _get_root_river_ledger_unit(self, worker_id: str) -> RiverLedgerUnit:
        default_cash_onset = 0.0
        default_cash_cease = 1.0
        default_root_river_tree_level = 0
        default_root_block_num = None  # maybe change to 1?
        default_root_parent_block_num = None
        root_river_block = RiverBlockUnit(
            cash_worker_id=worker_id,
            src_worker_id=None,
            dst_worker_id=worker_id,
            cash_start=default_cash_onset,
            cash_close=default_cash_cease,
            block_num=default_root_block_num,
            parent_block_num=default_root_parent_block_num,
            river_tree_level=default_root_river_tree_level,
        )
        with self.get_treasury_conn() as treasury_conn:
            source_river_ledger = get_river_ledger_unit(treasury_conn, root_river_block)
        return source_river_ledger

    def _set_partytreasuryunits_circles(self, worker_id: str):
        with self.get_treasury_conn() as treasury_conn:
            treasury_conn.execute(get_river_circle_table_insert_sqlstr(worker_id))
            treasury_conn.execute(get_river_reach_table_final_insert_sqlstr(worker_id))
            treasury_conn.execute(
                get_agenda_partyunit_table_update_treasury_due_paid_sqlstr(worker_id)
            )
            treasury_conn.execute(
                get_agenda_partyunit_table_update_credit_score_sqlstr(worker_id)
            )
            treasury_conn.execute(
                get_agenda_partyunit_table_update_treasury_voice_rank_sqlstr(worker_id)
            )

            sal_partytreasuryunits = get_partytreasuryunit_dict(
                treasury_conn, worker_id
            )
            x_agenda = self.get_job_agenda_file(worker_id=worker_id)
            set_treasury_partytreasuryunits_to_agenda_partyunits(
                x_agenda, sal_partytreasuryunits
            )
            self.save_job_agenda_to_forum(x_agenda)

    def get_partytreasuryunits(self, worker_id: str) -> dict[str:PartyTreasuryUnit]:
        with self.get_treasury_conn() as treasury_conn:
            partytreasuryunits = get_partytreasuryunit_dict(treasury_conn, worker_id)
        return partytreasuryunits

    def refresh_treasury_job_agendas_data(self, in_memory: bool = None):
        if in_memory is None and self._treasury_db != None:
            in_memory = True
        self._create_treasury_db(in_memory=in_memory, overwrite=True)
        self._treasury_populate_agendas_data()

    def _treasury_populate_agendas_data(self):
        for file_name in self.get_forum_dir_file_names_list():
            agenda_json = open_file(self.get_forum_dir(), file_name)
            agendaunit_x = get_agenda_from_json(x_agenda_json=agenda_json)
            agendaunit_x.set_agenda_metrics()

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
                    worker_id=agendaunit_x._worker_id,
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
                    agendaunit_x._worker_id, idea_x.get_road()
                )
                sqlstr = get_agenda_ideaunit_table_insert_sqlstr(agenda_ideaunit_x)
                cur.execute(sqlstr)

    def _treasury_insert_belief(self, agendaunit_x: AgendaUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            for belief_x in agendaunit_x._idearoot._beliefunits.values():
                agenda_idea_beliefunit_x = BeliefCatalog(
                    worker_id=agendaunit_x._worker_id,
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
        delete_dir(dir=self.get_treasury_db_path())

    def get_treasury_db_path(self):
        return f"{self.get_object_root_dir()}/{treasury_db_filename()}"

    # ClerkUnit management
    def get_clerkunits_dir(self):
        return f"{self.get_object_root_dir()}/clerkunits"

    def get_clerkunit_dir_paths_list(self):
        return list(
            dir_files(
                dir_path=self.get_clerkunits_dir(),
                delete_extensions=False,
                include_dirs=True,
            ).keys()
        )

    def add_clerkunit(
        self, worker_id: WorkerID, _auto_output_job_to_forum: bool = None
    ):
        x_clerkunit = clerkunit_shop(
            worker_id=worker_id,
            env_dir=self.get_object_root_dir(),
            econ_id=self.econ_id,
            _auto_output_job_to_forum=_auto_output_job_to_forum,
        )
        self.set_clerkunit(clerkunit=x_clerkunit)

    def clerkunit_exists(self, clerk_id: ClerkID):
        return self._clerkunits.get(clerk_id) != None

    def create_new_clerkunit(self, clerk_id: ClerkID):
        x_clerkunit = clerkunit_shop(clerk_id, self.get_object_root_dir(), self.econ_id)
        x_clerkunit.create_core_dir_and_files()
        self._clerkunits[x_clerkunit._clerk_id] = x_clerkunit

    def get_clerkunit(self, clerk_id: ClerkID) -> ClerkUnit:
        return self._clerkunits.get(clerk_id)

    def set_clerkunit(self, clerkunit: ClerkUnit):
        self._clerkunits[clerkunit._clerk_id] = clerkunit
        self.save_clerkunit_file(clerk_id=clerkunit._clerk_id)

    def save_clerkunit_file(self, clerk_id: ClerkID):
        x_clerkunit = self.get_clerkunit(clerk_id=clerk_id)
        x_clerkunit.save_role_agenda(x_clerkunit.get_role())

    def change_clerkunit_clerk_id(self, old_clerk_id: ClerkID, new_clerk_id: ClerkID):
        clerk_x = self.get_clerkunit(clerk_id=old_clerk_id)
        old_clerkunit_dir = clerk_x._clerkunit_dir
        clerk_x.set_clerk_id(new_clerk_id=new_clerk_id)
        self.set_clerkunit(clerk_x)
        delete_dir(old_clerkunit_dir)
        self.del_clerkunit_from_econ(clerk_id=old_clerk_id)

    def del_clerkunit_from_econ(self, clerk_id: ClerkID):
        self._clerkunits.pop(clerk_id)

    def del_clerkunit_dir(self, clerk_id: ClerkID):
        delete_dir(f"{self.get_clerkunits_dir()}/{clerk_id}")

    def full_setup_clerkunit(self, worker_id: WorkerID):
        self.add_clerkunit(worker_id, _auto_output_job_to_forum=True)
        requestee_clerkunit = self.get_clerkunit(worker_id)
        requestee_clerkunit.create_core_dir_and_files()
        requestee_clerkunit.save_refreshed_job_to_forum()

    # forum dir management
    def get_forum_dir(self):
        return f"{self.get_object_root_dir()}/forum"

    def get_ignores_dir(self, clerk_id: ClerkID):
        per_x = self.get_clerkunit(clerk_id)
        return per_x._agendas_ignore_dir

    def get_job_agenda_file(self, worker_id: str) -> AgendaUnit:
        return get_agenda_from_json(
            open_file(dest_dir=self.get_forum_dir(), file_name=f"{worker_id}.json")
        )

    def get_agenda_from_ignores_dir(
        self, clerk_id: ClerkID, _worker_id: WorkerID
    ) -> AgendaUnit:
        return get_agenda_from_json(
            open_file(
                dest_dir=self.get_ignores_dir(clerk_id=clerk_id),
                file_name=f"{_worker_id}.json",
            )
        )

    def set_ignore_agenda_file(self, clerk_id: ClerkID, agenda_obj: AgendaUnit):
        x_clerkunit = self.get_clerkunit(clerk_id=clerk_id)
        x_clerkunit.set_ignore_agenda_file(
            agendaunit=agenda_obj, src_worker_id=agenda_obj._worker_id
        )

    def change_job_worker_id(self, old_worker_id: WorkerID, new_worker_id: WorkerID):
        x_agenda = self.get_job_agenda_file(worker_id=old_worker_id)
        x_agenda.set_worker_id(new_worker_id=new_worker_id)
        self.save_job_agenda_to_forum(x_agenda)
        self.del_job_agenda(x_worker_id=old_worker_id)

    def del_job_agenda(self, x_worker_id: str):
        delete_dir(f"{self.get_forum_dir()}/{x_worker_id}.json")

    def save_job_agenda_to_forum(self, x_agenda: AgendaUnit):
        x_agenda.set_world_id(world_id=self.econ_id)
        save_file(
            dest_dir=self.get_forum_dir(),
            file_name=f"{x_agenda._worker_id}.json",
            file_text=x_agenda.get_json(),
        )

    def reload_all_clerkunits_job_agendas(self):
        for x_clerkunit in self._clerkunits.values():
            x_clerkunit.refresh_depot_agendas()

    def get_forum_dir_file_names_list(self):
        return list(dir_files(dir_path=self.get_forum_dir()).keys())

    # agendas_dir to worker_id_agendas_dir management
    def _clerkunit_set_depot_agenda(
        self,
        clerkunit: ClerkUnit,
        agendaunit: AgendaUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_agenda: AgendaUnit = None,
    ):
        clerkunit.set_depot_agenda(
            x_agenda=agendaunit,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )
        if depotlink_type == "ignore" and ignore_agenda != None:
            clerkunit.set_ignore_agenda_file(
                agendaunit=ignore_agenda, src_worker_id=agendaunit._worker_id
            )

    def set_clerk_depotlink(
        self,
        clerk_id: ClerkID,
        agenda_worker_id: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_agenda: AgendaUnit = None,
    ):
        x_clerkunit = self.get_clerkunit(clerk_id=clerk_id)
        x_agenda = self.get_job_agenda_file(worker_id=agenda_worker_id)
        self._clerkunit_set_depot_agenda(
            clerkunit=x_clerkunit,
            agendaunit=x_agenda,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
            ignore_agenda=ignore_agenda,
        )

    def create_depotlink_to_generated_agenda(
        self,
        clerk_id: ClerkID,
        worker_id: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        x_clerkunit = self.get_clerkunit(clerk_id=clerk_id)
        x_agenda = agendaunit_shop(_worker_id=worker_id)
        self._clerkunit_set_depot_agenda(
            clerkunit=x_clerkunit,
            agendaunit=x_agenda,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def update_depotlink(
        self,
        clerk_id: ClerkID,
        party_id: PartyID,
        depotlink_type: str,
        creditor_weight: str,
        debtor_weight: str,
    ):
        x_clerkunit = self.get_clerkunit(clerk_id=clerk_id)
        x_agenda = self.get_job_agenda(_worker_id=party_id)
        self._clerkunit_set_depot_agenda(
            clerkunit=x_clerkunit,
            agendaunit=x_agenda,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def del_depotlink(self, clerk_id: ClerkID, agendaunit_worker_id: WorkerID):
        x_clerkunit = self.get_clerkunit(clerk_id=clerk_id)
        x_clerkunit.del_depot_agenda(worker_id=agendaunit_worker_id)

    # Healer output_agenda
    def get_refreshed_job(self, clerk_id: ClerkID) -> AgendaUnit:
        x_clerkunit = self.get_clerkunit(clerk_id=clerk_id)
        return x_clerkunit.get_remelded_output_agenda()

    def build_econ_road(self, road_wo_econ_root: RoadUnit = None):
        if road_wo_econ_root is None or road_wo_econ_root == "":
            return self.econ_id
        else:
            return create_road(
                parent_road=self.econ_id,
                terminus_node=road_wo_econ_root,
                delimiter=self._road_delimiter,
            )

    def insert_intent_into_treasury(
        self, x_agendaunit: AgendaUnit, x_calendarreport: CalendarReport
    ):
        if x_agendaunit.idea_exists(x_calendarreport.time_road) == False:
            raise IntentBaseDoesNotExistException(
                f"Intent base cannot be '{x_calendarreport.time_road}' because it does not exist in agenda '{x_agendaunit._worker_id}'."
            )

        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()

            del_sqlstr = get_calendar_table_delete_sqlstr(x_calendarreport.worker_id)
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


def econunit_shop(
    econ_id: EconID,
    econ_dir: str = None,
    _manager_person_id: PersonID = None,
    _clerkunits: dict[WorkerID:ClerkUnit] = None,
    in_memory_treasury: bool = None,
    _road_delimiter: str = None,
) -> EconUnit:
    if in_memory_treasury is None:
        in_memory_treasury = True
    if econ_dir is None:
        econ_dir = f"/{econ_id}"
    econ_x = EconUnit(
        econ_dir=econ_dir,
        _clerkunits=get_empty_dict_if_none(_clerkunits),
    )
    if _manager_person_id is None:
        _manager_person_id = get_temp_env_person_id()
    econ_x.set_road_delimiter(_road_delimiter)
    econ_x.set_econ_id(econ_id=econ_id)
    econ_x._manager_person_id = _manager_person_id
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
