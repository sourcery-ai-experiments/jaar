from src._prime.road import (
    RoadUnit,
    create_road,
    default_road_delimiter_if_none,
    AgentID,
    HealerID,
    ProblemID,
    PersonID,
    PartyID,
    MarketID,
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
from src.market.clerk import ClerkUnit, clerkunit_shop, ClerkID
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from src.market.bank_sqlstr import (
    get_partybankunit_dict,
    get_agenda_partyunit_table_insert_sqlstr,
    get_agenda_partyunit_table_update_bank_due_paid_sqlstr,
    get_agenda_partyunit_table_update_credit_score_sqlstr,
    get_agenda_partyunit_table_update_bank_voice_rank_sqlstr,
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
    PartyBankUnit,
    IdeaCatalog,
    get_agenda_ideaunit_table_insert_sqlstr,
    get_agenda_ideaunit_dict,
    BeliefCatalog,
    get_agenda_idea_beliefunit_table_insert_sqlstr,
    GroupUnitCatalog,
    get_agenda_groupunit_table_insert_sqlstr,
    get_agenda_groupunit_dict,
    get_agendabankunits_dict,
    get_agendaunit_update_sqlstr,
    CalendarReport,
    CalendarIntentUnit,
    get_calendar_table_insert_sqlstr,
    get_calendar_table_delete_sqlstr,
)


def get_temp_env_market_id():
    return "ex_market04"


def get_temp_env_healer_id():
    return "ex_healer04"


def get_temp_env_person_id():
    return "ex_person04"


def get_temp_env_problem_id():
    return "ex_problem04"


class IntentBaseDoesNotExistException(Exception):
    pass


@dataclass
class MarketUnit:
    market_id: MarketID = None
    markets_dir: str = None
    _manager_person_id: HealerID = None
    _clerkunits: dict[str:ClerkUnit] = None
    _bank_db = None
    _road_delimiter: str = None

    def set_road_delimiter(self, new_road_delimiter: str):
        self._road_delimiter = default_road_delimiter_if_none(new_road_delimiter)

    # banking
    def set_voice_ranks(self, agent_id: AgentID, sort_order: str):
        if sort_order == "descretional":
            x_clerk = self.get_clerkunit(agent_id)
            x_contract = x_clerk.get_contract()
            for count_x, x_partyunit in enumerate(x_contract._partys.values()):
                x_partyunit.set_bank_voice_rank(count_x)
            x_clerk.set_contract(x_contract)
            x_clerk.save_refreshed_output_to_forum()

    def set_agenda_bank_attrs(self, x_agent_id: AgentID):
        x_agenda = self.get_forum_agenda(x_agent_id)

        for groupunit_x in x_agenda._groups.values():
            if groupunit_x._bank_partylinks != None:
                groupunit_x.clear_partylinks()
                ic = get_agenda_ideaunit_dict(
                    self.get_bank_conn(),
                    groupunit_x._bank_partylinks,
                )
                for agenda_ideaunit in ic.values():
                    if x_agent_id != agenda_ideaunit.agent_id:
                        partylink_x = partylink_shop(party_id=agenda_ideaunit.agent_id)
                        groupunit_x.set_partylink(partylink_x)
        self.save_forum_agenda(x_agenda)
        self.refresh_bank_forum_agendas_data()

    def set_credit_flow_for_agenda(
        self, agent_id: AgentID, max_blocks_count: int = None
    ):
        self._clear_all_source_river_data(agent_id)
        if max_blocks_count is None:
            max_blocks_count = 40
        self._set_river_blocks(agent_id, max_blocks_count)
        self._set_partybankunits_circles(agent_id)

    def _set_river_blocks(self, x_agent_id: AgentID, max_blocks_count: int):
        # changes in river_block loop
        general_circle = [self._get_root_river_ledger_unit(x_agent_id)]
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
                    cash_agent_id=x_agent_id,
                    src_agent_id=x_child_ledger.agent_id,
                    dst_agent_id=x_child_ledger.party_id,
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

        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_block_table_insert_sqlstr(river_block_x))

            if river_block_x.block_returned() == False:
                river_ledger_x = get_river_ledger_unit(bank_conn, river_block_x)

        return river_ledger_x

    def _clear_all_source_river_data(self, agent_id: str):
        with self.get_bank_conn() as bank_conn:
            block_s = get_river_block_table_delete_sqlstr(agent_id)
            bank_conn.execute(block_s)

    def _get_root_river_ledger_unit(self, agent_id: str) -> RiverLedgerUnit:
        default_cash_onset = 0.0
        default_cash_cease = 1.0
        default_root_river_tree_level = 0
        default_root_block_num = None  # maybe change to 1?
        default_root_parent_block_num = None
        root_river_block = RiverBlockUnit(
            cash_agent_id=agent_id,
            src_agent_id=None,
            dst_agent_id=agent_id,
            cash_start=default_cash_onset,
            cash_close=default_cash_cease,
            block_num=default_root_block_num,
            parent_block_num=default_root_parent_block_num,
            river_tree_level=default_root_river_tree_level,
        )
        with self.get_bank_conn() as bank_conn:
            source_river_ledger = get_river_ledger_unit(bank_conn, root_river_block)
        return source_river_ledger

    def _set_partybankunits_circles(self, agent_id: str):
        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_circle_table_insert_sqlstr(agent_id))
            bank_conn.execute(get_river_reach_table_final_insert_sqlstr(agent_id))
            bank_conn.execute(
                get_agenda_partyunit_table_update_bank_due_paid_sqlstr(agent_id)
            )
            bank_conn.execute(
                get_agenda_partyunit_table_update_credit_score_sqlstr(agent_id)
            )
            bank_conn.execute(
                get_agenda_partyunit_table_update_bank_voice_rank_sqlstr(agent_id)
            )

            sal_partybankunits = get_partybankunit_dict(bank_conn, agent_id)
            x_agenda = self.get_forum_agenda(agent_id=agent_id)
            set_bank_partybankunits_to_agenda_partyunits(x_agenda, sal_partybankunits)
            self.save_forum_agenda(x_agenda)

    def get_partybankunits(self, agent_id: str) -> dict[str:PartyBankUnit]:
        with self.get_bank_conn() as bank_conn:
            partybankunits = get_partybankunit_dict(bank_conn, agent_id)
        return partybankunits

    def refresh_bank_forum_agendas_data(self, in_memory: bool = None):
        if in_memory is None and self._bank_db != None:
            in_memory = True
        self._create_bank_db(in_memory=in_memory, overwrite=True)
        self._bank_populate_agendas_data()

    def _bank_populate_agendas_data(self):
        for file_name in self.get_forum_dir_file_names_list():
            agenda_json = open_file(self.get_forum_dir(), file_name)
            agendaunit_x = get_agenda_from_json(x_agenda_json=agenda_json)
            agendaunit_x.set_agenda_metrics()

            self._bank_insert_agendaunit(agendaunit_x)
            self._bank_insert_partyunit(agendaunit_x)
            self._bank_insert_groupunit(agendaunit_x)
            self._bank_insert_ideaunit(agendaunit_x)
            self._bank_insert_belief(agendaunit_x)

    def _bank_insert_agendaunit(self, agendaunit_x: AgendaUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            cur.execute(get_agendaunit_table_insert_sqlstr(x_agenda=agendaunit_x))

    def _bank_set_agendaunit_attrs(self, agenda: AgendaUnit):
        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_agendaunit_update_sqlstr(agenda))

    def _bank_insert_partyunit(self, agendaunit_x: AgendaUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for x_partyunit in agendaunit_x._partys.values():
                sqlstr = get_agenda_partyunit_table_insert_sqlstr(
                    agendaunit_x, x_partyunit
                )
                cur.execute(sqlstr)

    def _bank_insert_groupunit(self, agendaunit_x: AgendaUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for groupunit_x in agendaunit_x._groups.values():
                agenda_groupunit_x = GroupUnitCatalog(
                    agent_id=agendaunit_x._agent_id,
                    groupunit_group_id=groupunit_x.group_id,
                    bank_partylinks=groupunit_x._bank_partylinks,
                )
                sqlstr = get_agenda_groupunit_table_insert_sqlstr(agenda_groupunit_x)
                cur.execute(sqlstr)

    def _bank_insert_ideaunit(self, agendaunit_x: AgendaUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for idea_x in agendaunit_x._idea_dict.values():
                agenda_ideaunit_x = IdeaCatalog(
                    agendaunit_x._agent_id, idea_x.get_road()
                )
                sqlstr = get_agenda_ideaunit_table_insert_sqlstr(agenda_ideaunit_x)
                cur.execute(sqlstr)

    def _bank_insert_belief(self, agendaunit_x: AgendaUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for belief_x in agendaunit_x._idearoot._beliefunits.values():
                agenda_idea_beliefunit_x = BeliefCatalog(
                    agent_id=agendaunit_x._agent_id,
                    base=belief_x.base,
                    pick=belief_x.pick,
                )
                sqlstr = get_agenda_idea_beliefunit_table_insert_sqlstr(
                    agenda_idea_beliefunit_x
                )
                cur.execute(sqlstr)

    def get_bank_conn(self) -> Connection:
        if self._bank_db is None:
            return sqlite3_connect(self.get_bank_db_path())
        else:
            return self._bank_db

    def _create_bank_db(
        self, in_memory: bool = None, overwrite: bool = None
    ) -> Connection:
        if overwrite:
            self._delete_bank()

        bank_file_new = True
        if in_memory:
            self._bank_db = sqlite3_connect(":memory:")
        else:
            sqlite3_connect(self.get_bank_db_path())

        if bank_file_new:
            with self.get_bank_conn() as bank_conn:
                for sqlstr in get_create_table_if_not_exist_sqlstrs():
                    bank_conn.execute(sqlstr)

    def _delete_bank(self):
        self._bank_db = None
        delete_dir(dir=self.get_bank_db_path())

    def set_market_id(self, market_id: str):
        self.market_id = validate_roadnode(market_id, self._road_delimiter)

    def get_bank_db_path(self):
        return f"{self.get_object_root_dir()}/bank.db"

    def get_object_root_dir(self):
        return f"{self.markets_dir}/{self.market_id}"

    def _create_main_file_if_null(self, x_dir):
        market_file_name = "market.json"
        save_file(
            dest_dir=x_dir,
            file_name=market_file_name,
            file_text="",
        )

    def set_market_dirs(self, in_memory_bank: bool = None):
        market_dir = self.get_object_root_dir()
        agendas_dir = self.get_forum_dir()
        clerkunits_dir = self.get_clerkunits_dir()
        set_dir(x_path=market_dir)
        set_dir(x_path=agendas_dir)
        set_dir(x_path=clerkunits_dir)
        self._create_main_file_if_null(x_dir=market_dir)
        self._create_bank_db(in_memory=in_memory_bank, overwrite=True)

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

    def add_clerkunit(self, agent_id: AgentID, _auto_output_to_forum: bool = None):
        x_clerkunit = clerkunit_shop(
            agent_id=agent_id,
            env_dir=self.get_object_root_dir(),
            market_id=self.market_id,
            _auto_output_to_forum=_auto_output_to_forum,
        )
        self.set_clerkunit(clerkunit=x_clerkunit)

    def clerkunit_exists(self, cid: ClerkID):
        return self._clerkunits.get(cid) != None

    def create_new_clerkunit(self, clerk_id: ClerkID):
        x_clerkunit = clerkunit_shop(
            clerk_id, self.get_object_root_dir(), self.market_id
        )
        x_clerkunit.create_core_dir_and_files()
        self._clerkunits[x_clerkunit._clerk_id] = x_clerkunit

    def get_clerkunit(self, cid: ClerkID) -> ClerkUnit:
        return self._clerkunits.get(cid)

    def set_clerkunit(self, clerkunit: ClerkUnit):
        self._clerkunits[clerkunit._clerk_id] = clerkunit
        self.save_clerkunit_file(clerk_id=clerkunit._clerk_id)

    def save_clerkunit_file(self, clerk_id: ClerkID):
        x_clerkunit = self.get_clerkunit(cid=clerk_id)
        x_clerkunit.save_contract_agenda(x_clerkunit.get_contract())

    def change_clerkunit_cid(self, old_cid: ClerkID, new_cid: ClerkID):
        clerk_x = self.get_clerkunit(cid=old_cid)
        old_clerkunit_dir = clerk_x._clerkunit_dir
        clerk_x.set_clerk_id(new_cid=new_cid)
        self.set_clerkunit(clerk_x)
        delete_dir(old_clerkunit_dir)
        self.del_clerkunit_from_market(clerk_id=old_cid)

    def del_clerkunit_from_market(self, clerk_id: ClerkID):
        self._clerkunits.pop(clerk_id)

    def del_clerkunit_dir(self, clerk_id: ClerkID):
        delete_dir(f"{self.get_clerkunits_dir()}/{clerk_id}")

    def full_setup_clerkunit(self, agent_id: AgentID):
        self.add_clerkunit(agent_id, _auto_output_to_forum=True)
        requestee_clerkunit = self.get_clerkunit(agent_id)
        requestee_clerkunit.create_core_dir_and_files()
        requestee_clerkunit.save_refreshed_output_to_forum()

    # forum dir management
    def get_forum_dir(self):
        return f"{self.get_object_root_dir()}/forum"

    def get_ignores_dir(self, clerk_id: ClerkID):
        per_x = self.get_clerkunit(clerk_id)
        return per_x._agendas_ignore_dir

    def get_forum_agenda(self, agent_id: str) -> AgendaUnit:
        return get_agenda_from_json(
            open_file(dest_dir=self.get_forum_dir(), file_name=f"{agent_id}.json")
        )

    def get_agenda_from_ignores_dir(
        self, clerk_id: ClerkID, _agent_id: AgentID
    ) -> AgendaUnit:
        return get_agenda_from_json(
            open_file(
                dest_dir=self.get_ignores_dir(clerk_id=clerk_id),
                file_name=f"{_agent_id}.json",
            )
        )

    def set_ignore_agenda_file(self, clerk_id: ClerkID, agenda_obj: AgendaUnit):
        x_clerkunit = self.get_clerkunit(cid=clerk_id)
        x_clerkunit.set_ignore_agenda_file(
            agendaunit=agenda_obj, src_agent_id=agenda_obj._agent_id
        )

    def change_forum_agent_id(self, old_agent_id: AgentID, new_agent_id: AgentID):
        x_agenda = self.get_forum_agenda(agent_id=old_agent_id)
        x_agenda.set_agent_id(new_agent_id=new_agent_id)
        self.save_forum_agenda(x_agenda)
        self.del_forum_agenda(x_agent_id=old_agent_id)

    def del_forum_agenda(self, x_agent_id: str):
        delete_dir(f"{self.get_forum_dir()}/{x_agent_id}.json")

    def save_forum_agenda(self, x_agenda: AgendaUnit):
        x_agenda.set_world_id(world_id=self.market_id)
        save_file(
            dest_dir=self.get_forum_dir(),
            file_name=f"{x_agenda._agent_id}.json",
            file_text=x_agenda.get_json(),
        )

    def reload_all_clerkunits_forum_agendaunits(self):
        for x_clerkunit in self._clerkunits.values():
            x_clerkunit.refresh_depot_agendas()

    def get_forum_dir_file_names_list(self):
        return list(dir_files(dir_path=self.get_forum_dir()).keys())

    # agendas_dir to agent_id_agendas_dir management
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
                agendaunit=ignore_agenda, src_agent_id=agendaunit._agent_id
            )

    def set_clerk_depotlink(
        self,
        clerk_id: ClerkID,
        agenda_agent_id: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_agenda: AgendaUnit = None,
    ):
        x_clerkunit = self.get_clerkunit(cid=clerk_id)
        x_agenda = self.get_forum_agenda(agent_id=agenda_agent_id)
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
        agent_id: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        x_clerkunit = self.get_clerkunit(cid=clerk_id)
        x_agenda = agendaunit_shop(_agent_id=agent_id)
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
        x_clerkunit = self.get_clerkunit(cid=clerk_id)
        x_agenda = self.get_forum_agenda(_agent_id=party_id)
        self._clerkunit_set_depot_agenda(
            clerkunit=x_clerkunit,
            agendaunit=x_agenda,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def del_depotlink(self, clerk_id: ClerkID, agendaunit_agent_id: AgentID):
        x_clerkunit = self.get_clerkunit(cid=clerk_id)
        x_clerkunit.del_depot_agenda(agent_id=agendaunit_agent_id)

    # Healer output_agenda
    def get_output_agenda(self, clerk_id: ClerkID) -> AgendaUnit:
        x_clerkunit = self.get_clerkunit(cid=clerk_id)
        return x_clerkunit.get_remelded_output_agenda()

    def build_market_road(self, road_wo_market_root: RoadUnit = None):
        if road_wo_market_root is None or road_wo_market_root == "":
            return self.market_id
        else:
            return create_road(
                parent_road=self.market_id,
                terminus_node=road_wo_market_root,
                delimiter=self._road_delimiter,
            )

    def insert_intent_into_bank(
        self, x_agendaunit: AgendaUnit, x_calendarreport: CalendarReport
    ):
        if x_agendaunit.idea_exists(x_calendarreport.time_road) == False:
            raise IntentBaseDoesNotExistException(
                f"Intent base cannot be '{x_calendarreport.time_road}' because it does not exist in agenda '{x_agendaunit._agent_id}'."
            )

        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()

            del_sqlstr = get_calendar_table_delete_sqlstr(x_calendarreport.agent_id)
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


def marketunit_shop(
    market_id: MarketID,
    markets_dir: str = None,
    _manager_person_id: PersonID = None,
    _clerkunits: dict[AgentID:ClerkUnit] = None,
    in_memory_bank: bool = None,
    _road_delimiter: str = None,
) -> MarketUnit:
    if in_memory_bank is None:
        in_memory_bank = True
    if markets_dir is None:
        markets_dir = f"/markets/{market_id}"
    market_x = MarketUnit(
        markets_dir=markets_dir,
        _clerkunits=get_empty_dict_if_none(_clerkunits),
    )
    if _manager_person_id is None:
        _manager_person_id = get_temp_env_person_id()
    market_x.set_road_delimiter(_road_delimiter)
    market_x.set_market_id(market_id=market_id)
    market_x._manager_person_id = _manager_person_id
    market_x.set_market_dirs(in_memory_bank=in_memory_bank)
    return market_x


def set_bank_partybankunits_to_agenda_partyunits(
    x_agenda: AgendaUnit, partybankunits: dict[str:PartyBankUnit]
):
    for x_partyunit in x_agenda._partys.values():
        x_partyunit.clear_banking_data()
        partybankunit = partybankunits.get(x_partyunit.party_id)
        if partybankunit != None:
            x_partyunit.set_banking_data(
                due_paid=partybankunit.due_total,
                due_diff=partybankunit.due_diff,
                credit_score=partybankunit.credit_score,
                voice_rank=partybankunit.voice_rank,
            )
