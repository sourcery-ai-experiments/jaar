from src.agenda.road import RoadPath, get_road_from_road_and_node, get_node_delimiter
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as get_agenda_from_json,
    partylink_shop,
    PartyPID,
    PersonID,
    EconomyID,
)
from src.agenda.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
    get_empty_dict_if_null,
)
from src.economy.enact import EnactUnit, enactunit_shop, EnactCID
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from src.economy.treasury_sqlstr import (
    get_partytreasuryunit_dict,
    get_partyunit_table_insert_sqlstr,
    get_partyunit_table_update_treasury_tax_paid_sqlstr,
    get_partyunit_table_update_credit_score_sqlstr,
    get_partyunit_table_update_treasury_voice_rank_sqlstr,
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
    get_idea_catalog_table_insert_sqlstr,
    get_idea_catalog_dict,
    AcptFactCatalog,
    get_acptfact_catalog_table_insert_sqlstr,
    GroupUnitCatalog,
    get_groupunit_catalog_table_insert_sqlstr,
    get_groupunit_catalog_dict,
    get_agendatreasuryunits_dict,
    get_agendaunit_update_sqlstr,
)


@dataclass
class EconomyUnit:
    economy_id: EconomyID
    economys_dir: str
    _manager_pid: PersonID = None
    _enactunits: dict[str:EnactUnit] = None
    _treasury_db = None
    _road_node_delimiter: str = None

    def set_road_node_delimiter(self, new_road_node_delimiter: str):
        self._road_node_delimiter = get_node_delimiter(new_road_node_delimiter)

    def set_manager_pid(self, person_id: PersonID):
        self._manager_pid = person_id

    # treasurying
    def set_voice_ranks(self, healer: PersonID, sort_order: str):
        if sort_order == "descretional":
            x_enact = self.get_enactunit(healer)
            x_contract = x_enact.get_contract()
            for count_x, x_partyunit in enumerate(x_contract._partys.values()):
                x_partyunit.set_treasury_voice_rank(count_x)
            x_enact.set_contract(x_contract)
            x_enact.save_refreshed_output_to_public()

    def set_agenda_treasury_attrs(self, x_healer: PersonID):
        healer_agenda = self.get_public_agenda(x_healer)

        for groupunit_x in healer_agenda._groups.values():
            if groupunit_x._partylinks_set_by_economy_road != None:
                groupunit_x.clear_partylinks()
                ic = get_idea_catalog_dict(
                    self.get_treasury_conn(),
                    groupunit_x._partylinks_set_by_economy_road,
                )
                for idea_catalog in ic.values():
                    if x_healer != idea_catalog.agenda_healer:
                        partylink_x = partylink_shop(pid=idea_catalog.agenda_healer)
                        groupunit_x.set_partylink(partylink_x)
        self.save_public_agenda(healer_agenda)
        self.refresh_treasury_public_agendas_data()

    def set_credit_flow_for_agenda(
        self, agenda_healer: PersonID, max_blocks_count: int = None
    ):
        self._clear_all_source_river_data(agenda_healer)
        if max_blocks_count is None:
            max_blocks_count = 40
        self._set_river_blocks(agenda_healer, max_blocks_count)
        self._set_partytreasuryunits_circles(agenda_healer)

    def _set_river_blocks(self, x_agenda_healer: PersonID, max_blocks_count: int):
        # changes in river_block loop
        general_circle = [self._get_root_river_ledger_unit(x_agenda_healer)]
        blocks_count = 0  # changes in river_block loop
        while blocks_count < max_blocks_count and general_circle != []:
            parent_agenda_ledger = general_circle.pop(0)
            ledgers_len = len(parent_agenda_ledger._partyviews.values())
            parent_range = parent_agenda_ledger.get_range()
            parent_close = parent_agenda_ledger.currency_cease

            curr_onset = (
                parent_agenda_ledger.currency_onset
            )  # changes in river_block loop
            ledgers_count = 0  # changes in river_block loop
            for x_child_ledger in parent_agenda_ledger._partyviews.values():
                ledgers_count += 1

                curr_range = parent_range * x_child_ledger._agenda_intent_ratio_credit
                curr_close = curr_onset + curr_range

                # implies last element in dict
                if ledgers_count == ledgers_len and curr_close != parent_close:
                    curr_close = parent_close

                river_block_x = RiverBlockUnit(
                    currency_agenda_healer=x_agenda_healer,
                    src_healer=x_child_ledger.agenda_healer,
                    dst_healer=x_child_ledger.pid,
                    currency_start=curr_onset,
                    currency_close=curr_close,
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

    def _clear_all_source_river_data(self, agenda_healer: str):
        with self.get_treasury_conn() as treasury_conn:
            block_s = get_river_block_table_delete_sqlstr(agenda_healer)
            treasury_conn.execute(block_s)

    def _get_root_river_ledger_unit(self, agenda_healer: str) -> RiverLedgerUnit:
        default_currency_onset = 0.0
        default_currency_cease = 1.0
        default_root_river_tree_level = 0
        default_root_block_num = None  # maybe change to 1?
        default_root_parent_block_num = None
        root_river_block = RiverBlockUnit(
            currency_agenda_healer=agenda_healer,
            src_healer=None,
            dst_healer=agenda_healer,
            currency_start=default_currency_onset,
            currency_close=default_currency_cease,
            block_num=default_root_block_num,
            parent_block_num=default_root_parent_block_num,
            river_tree_level=default_root_river_tree_level,
        )
        with self.get_treasury_conn() as treasury_conn:
            source_river_ledger = get_river_ledger_unit(treasury_conn, root_river_block)
        return source_river_ledger

    def _set_partytreasuryunits_circles(self, agenda_healer: str):
        with self.get_treasury_conn() as treasury_conn:
            treasury_conn.execute(get_river_circle_table_insert_sqlstr(agenda_healer))
            treasury_conn.execute(
                get_river_reach_table_final_insert_sqlstr(agenda_healer)
            )
            treasury_conn.execute(
                get_partyunit_table_update_treasury_tax_paid_sqlstr(agenda_healer)
            )
            treasury_conn.execute(
                get_partyunit_table_update_credit_score_sqlstr(agenda_healer)
            )
            treasury_conn.execute(
                get_partyunit_table_update_treasury_voice_rank_sqlstr(agenda_healer)
            )

            sal_partytreasuryunits = get_partytreasuryunit_dict(
                treasury_conn, agenda_healer
            )
            x_agenda = self.get_public_agenda(healer=agenda_healer)
            set_treasury_partytreasuryunits_to_agenda_partyunits(
                x_agenda, sal_partytreasuryunits
            )
            self.save_public_agenda(x_agenda)

    def get_partytreasuryunits(self, agenda_healer: str) -> dict[str:PartyTreasuryUnit]:
        with self.get_treasury_conn() as treasury_conn:
            partytreasuryunits = get_partytreasuryunit_dict(
                treasury_conn, agenda_healer
            )
        return partytreasuryunits

    def refresh_treasury_public_agendas_data(self, in_memory: bool = None):
        if in_memory is None and self._treasury_db != None:
            in_memory = True
        self._create_treasury_db(in_memory=in_memory, overwrite=True)
        self._treasury_populate_agendas_data()

    def _treasury_populate_agendas_data(self):
        for file_name in self.get_public_dir_file_names_list():
            agenda_json = x_func_open_file(self.get_public_dir(), file_name)
            agendaunit_x = get_agenda_from_json(x_agenda_json=agenda_json)
            agendaunit_x.set_agenda_metrics()

            self._treasury_insert_agendaunit(agendaunit_x)
            self._treasury_insert_partyunit(agendaunit_x)
            self._treasury_insert_groupunit(agendaunit_x)
            self._treasury_insert_ideaunit(agendaunit_x)
            self._treasury_insert_acptfact(agendaunit_x)

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
                sqlstr = get_partyunit_table_insert_sqlstr(agendaunit_x, x_partyunit)
                cur.execute(sqlstr)

    def _treasury_insert_groupunit(self, agendaunit_x: AgendaUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            for groupunit_x in agendaunit_x._groups.values():
                groupunit_catalog_x = GroupUnitCatalog(
                    agenda_healer=agendaunit_x._healer,
                    groupunit_brand=groupunit_x.brand,
                    partylinks_set_by_economy_road=groupunit_x._partylinks_set_by_economy_road,
                )
                sqlstr = get_groupunit_catalog_table_insert_sqlstr(groupunit_catalog_x)
                cur.execute(sqlstr)

    def _treasury_insert_ideaunit(self, agendaunit_x: AgendaUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            for idea_x in agendaunit_x._idea_dict.values():
                idea_catalog_x = IdeaCatalog(
                    agendaunit_x._healer, idea_x.get_idea_road()
                )
                sqlstr = get_idea_catalog_table_insert_sqlstr(idea_catalog_x)
                cur.execute(sqlstr)

    def _treasury_insert_acptfact(self, agendaunit_x: AgendaUnit):
        with self.get_treasury_conn() as treasury_conn:
            cur = treasury_conn.cursor()
            for acptfact_x in agendaunit_x._idearoot._acptfactunits.values():
                acptfact_catalog_x = AcptFactCatalog(
                    agenda_healer=agendaunit_x._healer,
                    base=acptfact_x.base,
                    pick=acptfact_x.pick,
                )
                sqlstr = get_acptfact_catalog_table_insert_sqlstr(acptfact_catalog_x)
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
        x_func_delete_dir(dir=self.get_treasury_db_path())

    def set_economy_id(self, economy_id: str):
        self.economy_id = economy_id

    def get_treasury_db_path(self):
        return f"{self.get_object_root_dir()}/treasury.db"

    def get_object_root_dir(self):
        return f"{self.economys_dir}/{self.economy_id}"

    def _create_main_file_if_null(self, x_dir):
        economy_file_name = "economy.json"
        x_func_save_file(
            dest_dir=x_dir,
            file_name=economy_file_name,
            file_text="",
        )

    def create_dirs_if_null(self, in_memory_treasury: bool = None):
        economy_dir = self.get_object_root_dir()
        agendas_dir = self.get_public_dir()
        enactunits_dir = self.get_enactunits_dir()
        single_dir_create_if_null(x_path=economy_dir)
        single_dir_create_if_null(x_path=agendas_dir)
        single_dir_create_if_null(x_path=enactunits_dir)
        self._create_main_file_if_null(x_dir=economy_dir)
        self._create_treasury_db(in_memory=in_memory_treasury, overwrite=True)

    # EnactUnit management
    def get_enactunits_dir(self):
        return f"{self.get_object_root_dir()}/enactunits"

    def get_enactunit_dir_paths_list(self):
        return list(
            x_func_dir_files(
                dir_path=self.get_enactunits_dir(),
                remove_extensions=False,
                include_dirs=True,
            ).keys()
        )

    def add_enactunit(self, pid: PersonID, _auto_output_to_public: bool = None):
        x_enactunit = enactunit_shop(
            pid=pid,
            env_dir=self.get_object_root_dir(),
            economy_id=self.economy_id,
            _auto_output_to_public=_auto_output_to_public,
        )
        self.set_enactunit(enactunit=x_enactunit)

    def enactunit_exists(self, cid: EnactCID):
        return self._enactunits.get(cid) != None

    def create_new_enactunit(self, enact_cid: EnactCID):
        x_enactunit = enactunit_shop(
            enact_cid, self.get_object_root_dir(), self.economy_id
        )
        x_enactunit.create_core_dir_and_files()
        self._enactunits[x_enactunit._enact_cid] = x_enactunit

    def get_enactunit(self, cid: EnactCID) -> EnactUnit:
        return self._enactunits.get(cid)

    def set_enactunit(self, enactunit: EnactUnit):
        self._enactunits[enactunit._enact_cid] = enactunit
        self.save_enactunit_file(enact_cid=enactunit._enact_cid)

    def save_enactunit_file(self, enact_cid: EnactCID):
        x_enactunit = self.get_enactunit(cid=enact_cid)
        x_enactunit.save_contract_agenda(x_enactunit.get_contract())

    def change_enactunit_cid(self, old_cid: EnactCID, new_cid: EnactCID):
        enact_x = self.get_enactunit(cid=old_cid)
        old_enactunit_dir = enact_x._enactunit_dir
        enact_x.set_enact_cid(new_cid=new_cid)
        self.set_enactunit(enact_x)
        x_func_delete_dir(old_enactunit_dir)
        self.del_enactunit_from_economy(enact_cid=old_cid)

    def del_enactunit_from_economy(self, enact_cid: EnactCID):
        self._enactunits.pop(enact_cid)

    def del_enactunit_dir(self, enact_cid: EnactCID):
        x_func_delete_dir(f"{self.get_enactunits_dir()}/{enact_cid}")

    def full_setup_enactunit(self, healer_id: PersonID):
        self.add_enactunit(healer_id, _auto_output_to_public=True)
        requestee_enactunit = self.get_enactunit(healer_id)
        requestee_enactunit.create_core_dir_and_files()
        requestee_enactunit.save_refreshed_output_to_public()

    # public dir management
    def get_public_dir(self):
        return f"{self.get_object_root_dir()}/agendas"

    def get_ignores_dir(self, enact_cid: EnactCID):
        per_x = self.get_enactunit(enact_cid)
        return per_x._agendas_ignore_dir

    def get_public_agenda(self, healer: str) -> AgendaUnit:
        return get_agenda_from_json(
            x_func_open_file(dest_dir=self.get_public_dir(), file_name=f"{healer}.json")
        )

    def get_agenda_from_ignores_dir(
        self, enact_cid: EnactCID, _healer: str
    ) -> AgendaUnit:
        return get_agenda_from_json(
            x_func_open_file(
                dest_dir=self.get_ignores_dir(enact_cid=enact_cid),
                file_name=f"{_healer}.json",
            )
        )

    def set_ignore_agenda_file(self, enact_cid: EnactCID, agenda_obj: AgendaUnit):
        x_enactunit = self.get_enactunit(cid=enact_cid)
        x_enactunit.set_ignore_agenda_file(
            agendaunit=agenda_obj, src_agenda_healer=agenda_obj._healer
        )

    def change_public_agenda_healer(self, old_healer: str, new_healer: str):
        x_agenda = self.get_public_agenda(healer=old_healer)
        x_agenda.set_healer(new_healer=new_healer)
        self.save_public_agenda(x_agenda)
        self.del_public_agenda(x_agenda_healer=old_healer)

    def del_public_agenda(self, x_agenda_healer: str):
        x_func_delete_dir(f"{self.get_public_dir()}/{x_agenda_healer}.json")

    def save_public_agenda(self, x_agenda: AgendaUnit):
        x_agenda.set_economy_id(economy_id=self.economy_id)
        x_func_save_file(
            dest_dir=self.get_public_dir(),
            file_name=f"{x_agenda._healer}.json",
            file_text=x_agenda.get_json(),
        )

    def reload_all_enactunits_src_agendaunits(self):
        for x_enactunit in self._enactunits.values():
            x_enactunit.refresh_depot_agendas()

    def get_public_dir_file_names_list(self):
        return list(x_func_dir_files(dir_path=self.get_public_dir()).keys())

    # agendas_dir to healer_agendas_dir management
    def _enactunit_set_depot_agenda(
        self,
        enactunit: EnactUnit,
        agendaunit: AgendaUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_agenda: AgendaUnit = None,
    ):
        enactunit.set_depot_agenda(
            x_agenda=agendaunit,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )
        if depotlink_type == "ignore" and ignore_agenda != None:
            enactunit.set_ignore_agenda_file(
                agendaunit=ignore_agenda, src_agenda_healer=agendaunit._healer
            )

    def set_healer_depotlink(
        self,
        enact_cid: EnactCID,
        agenda_healer: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_agenda: AgendaUnit = None,
    ):
        x_enactunit = self.get_enactunit(cid=enact_cid)
        x_agenda = self.get_public_agenda(healer=agenda_healer)
        self._enactunit_set_depot_agenda(
            enactunit=x_enactunit,
            agendaunit=x_agenda,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
            ignore_agenda=ignore_agenda,
        )

    def create_depotlink_to_generated_agenda(
        self,
        enact_cid: EnactCID,
        agenda_healer: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        x_enactunit = self.get_enactunit(cid=enact_cid)
        x_agenda = agendaunit_shop(_healer=agenda_healer)
        self._enactunit_set_depot_agenda(
            enactunit=x_enactunit,
            agendaunit=x_agenda,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def update_depotlink(
        self,
        enact_cid: EnactCID,
        partypid: PartyPID,
        depotlink_type: str,
        creditor_weight: str,
        debtor_weight: str,
    ):
        x_enactunit = self.get_enactunit(cid=enact_cid)
        x_agenda = self.get_public_agenda(_healer=partypid)
        self._enactunit_set_depot_agenda(
            enactunit=x_enactunit,
            agendaunit=x_agenda,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def del_depotlink(self, enact_cid: EnactCID, agendaunit_healer: str):
        x_enactunit = self.get_enactunit(cid=enact_cid)
        x_enactunit.del_depot_agenda(agenda_healer=agendaunit_healer)

    # Healer output_agenda
    def get_output_agenda(self, enact_cid: EnactCID) -> AgendaUnit:
        x_enactunit = self.get_enactunit(cid=enact_cid)
        return x_enactunit.get_remelded_output_agenda()

    def build_economy_road(self, road_wo_economy_root: RoadPath = None):
        if road_wo_economy_root is None or road_wo_economy_root == "":
            return self.economy_id
        else:
            return get_road_from_road_and_node(
                pad=self.economy_id,
                terminus_node=road_wo_economy_root,
                delimiter=self._road_node_delimiter,
            )


def economyunit_shop(
    economy_id: EconomyID,
    economys_dir: str,
    _manager_pid: PersonID = None,
    _enactunits: dict[str:EnactUnit] = None,
    in_memory_treasury: bool = None,
    _road_node_delimiter: str = None,
) -> EconomyUnit:
    if in_memory_treasury is None:
        in_memory_treasury = True
    economy_x = EconomyUnit(
        economy_id=economy_id,
        economys_dir=economys_dir,
        _enactunits=get_empty_dict_if_null(_enactunits),
    )
    economy_x.set_road_node_delimiter(_road_node_delimiter)
    economy_x.set_manager_pid(_manager_pid)
    economy_x.create_dirs_if_null(in_memory_treasury=in_memory_treasury)
    return economy_x


def set_treasury_partytreasuryunits_to_agenda_partyunits(
    x_agenda: AgendaUnit, partytreasuryunits: dict[str:PartyTreasuryUnit]
):
    for x_partyunit in x_agenda._partys.values():
        x_partyunit.clear_treasurying_data()
        partytreasuryunit = partytreasuryunits.get(x_partyunit.pid)
        if partytreasuryunit != None:
            x_partyunit.set_treasurying_data(
                tax_paid=partytreasuryunit.tax_total,
                tax_diff=partytreasuryunit.tax_diff,
                credit_score=partytreasuryunit.credit_score,
                voice_rank=partytreasuryunit.voice_rank,
            )
