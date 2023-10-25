from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as get_agenda_from_json,
    partylink_shop,
    PartyTitle,
    PersonName,
)
from src.agenda.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from src.culture.kitchen import KitchenUnit, kitchenunit_shop, KitchenDub
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from src.culture.bank_sqlstr import (
    get_river_flow_table_delete_sqlstr,
    get_river_flow_table_insert_sqlstr,
    get_river_tally_table_delete_sqlstr,
    get_river_tally_table_insert_sqlstr,
    get_river_tally_dict,
    get_river_bucket_table_insert_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
    get_ledger_table_insert_sqlstr,
    get_agendaunit_table_insert_sqlstr,
    get_river_ledger_unit,
    LedgerUnit,
    RiverLedgerUnit,
    RiverFlowUnit,
    RiverTallyUnit,
    IdeaCatalog,
    get_idea_catalog_table_insert_sqlstr,
    get_idea_catalog_dict,
    AcptFactCatalog,
    get_acptfact_catalog_table_insert_sqlstr,
    GroupUnitCatalog,
    get_groupunit_catalog_table_insert_sqlstr,
    get_groupunit_catalog_dict,
    get_agendabankunits_dict,
    get_agendaunit_update_sqlstr,
)


class CultureHandle(str):  # Created to help track the concept
    pass


@dataclass
class CultureUnit:
    handle: CultureHandle
    cultures_dir: str
    _manager_name: PersonName = None
    _kitchenunits: dict[str:KitchenUnit] = None
    _bank_db = None

    def set_manager_name(self, person_name: PersonName):
        self._manager_name = person_name

    # banking
    def set_voice_ranks(self, healer: PersonName, sort_order: str):
        if sort_order == "arbitary":
            x_kitchen = self.get_kitchenunit(healer)
            x_seed = x_kitchen.get_seed()
            for count_x, x_partyunit in enumerate(x_seed._partys.values()):
                x_partyunit.set_bank_voice_rank(count_x)
            x_kitchen.set_seed(x_seed)
            x_kitchen._admin.save_refreshed_output_to_public()

    def set_agenda_bank_attrs(self, agenda_healer: str):
        agenda_obj = self.get_public_agenda(agenda_healer)

        for groupunit_x in agenda_obj._groups.values():
            if groupunit_x._partylinks_set_by_culture_road != None:
                groupunit_x.clear_partylinks()
                ic = get_idea_catalog_dict(
                    self.get_bank_conn(), groupunit_x._partylinks_set_by_culture_road
                )
                for idea_catalog in ic.values():
                    if agenda_healer != idea_catalog.agenda_healer:
                        partylink_x = partylink_shop(title=idea_catalog.agenda_healer)
                        groupunit_x.set_partylink(partylink_x)
        self.save_public_agenda(agenda_obj)

        # refresh bank metrics
        self.refresh_bank_agenda_data()

    def set_river_lake_for_agenda(
        self, agenda_healer: PersonName, max_flows_count: int = None
    ):
        self._clear_all_source_river_data(agenda_healer)
        if max_flows_count is None:
            max_flows_count = 40
        self._set_river_flows(agenda_healer, max_flows_count)
        self._set_river_tallys_buckets(agenda_healer)

    def _set_river_flows(self, x_agenda_healer: PersonName, max_flows_count: int):
        # changes in river_flow loop
        general_bucket = [self._get_root_river_ledger_unit(x_agenda_healer)]
        flows_count = 0  # changes in river_flow loop
        while flows_count < max_flows_count and general_bucket != []:
            parent_agenda_ledger = general_bucket.pop(0)
            ledgers_len = len(parent_agenda_ledger._ledgers.values())
            parent_range = parent_agenda_ledger.get_range()
            parent_close = parent_agenda_ledger.currency_cease

            curr_onset = (
                parent_agenda_ledger.currency_onset
            )  # changes in river_flow loop
            ledgers_count = 0  # changes in river_flow loop
            for x_child_ledger in parent_agenda_ledger._ledgers.values():
                ledgers_count += 1

                curr_range = parent_range * x_child_ledger._agenda_goal_ratio_credit
                curr_close = curr_onset + curr_range

                # implies last element in dict
                if ledgers_count == ledgers_len and curr_close != parent_close:
                    curr_close = parent_close

                river_flow_x = RiverFlowUnit(
                    currency_agenda_healer=x_agenda_healer,
                    src_healer=x_child_ledger.agenda_healer,
                    dst_healer=x_child_ledger.party_title,
                    currency_start=curr_onset,
                    currency_close=curr_close,
                    flow_num=flows_count,
                    parent_flow_num=parent_agenda_ledger.flow_num,
                    river_tree_level=parent_agenda_ledger.river_tree_level + 1,
                )
                river_ledger_x = self._insert_river_flow_grab_river_ledger(river_flow_x)
                if river_ledger_x != None:
                    general_bucket.append(river_ledger_x)

                flows_count += 1
                if flows_count >= max_flows_count:
                    break

                # change curr_onset for next
                curr_onset += curr_range

    def _insert_river_flow_grab_river_ledger(
        self, river_flow_x: RiverFlowUnit
    ) -> RiverLedgerUnit:
        river_ledger_x = None

        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_flow_table_insert_sqlstr(river_flow_x))

            if river_flow_x.flow_returned() == False:
                river_ledger_x = get_river_ledger_unit(bank_conn, river_flow_x)

        return river_ledger_x

    def _clear_all_source_river_data(self, agenda_healer: str):
        with self.get_bank_conn() as bank_conn:
            flow_s = get_river_flow_table_delete_sqlstr(agenda_healer)
            mstr_s = get_river_tally_table_delete_sqlstr(agenda_healer)
            bank_conn.execute(flow_s)
            bank_conn.execute(mstr_s)

    def _get_root_river_ledger_unit(self, agenda_healer: str) -> RiverLedgerUnit:
        default_currency_onset = 0.0
        default_currency_cease = 1.0
        default_root_river_tree_level = 0
        default_root_flow_num = None  # maybe change to 1?
        default_root_parent_flow_num = None
        root_river_flow = RiverFlowUnit(
            currency_agenda_healer=agenda_healer,
            src_healer=None,
            dst_healer=agenda_healer,
            currency_start=default_currency_onset,
            currency_close=default_currency_cease,
            flow_num=default_root_flow_num,
            parent_flow_num=default_root_parent_flow_num,
            river_tree_level=default_root_river_tree_level,
        )
        with self.get_bank_conn() as bank_conn:
            source_river_ledger = get_river_ledger_unit(bank_conn, root_river_flow)
        return source_river_ledger

    def _set_river_tallys_buckets(self, agenda_healer: str):
        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_tally_table_insert_sqlstr(agenda_healer))
            bank_conn.execute(get_river_bucket_table_insert_sqlstr(agenda_healer))

            sal_river_tallys = get_river_tally_dict(bank_conn, agenda_healer)
            x_agenda = self.get_public_agenda(healer=agenda_healer)
            set_bank_river_tallys_to_agenda_partyunits(x_agenda, sal_river_tallys)
            self.save_public_agenda(x_agenda=x_agenda)

    def get_river_tallys(self, agenda_healer: str) -> dict[str:RiverTallyUnit]:
        with self.get_bank_conn() as bank_conn:
            river_tallys = get_river_tally_dict(bank_conn, agenda_healer)
        return river_tallys

    def refresh_bank_agenda_data(self, in_memory: bool = None):
        if in_memory is None and self._bank_db != None:
            in_memory = True
        self._create_bank_db(in_memory=in_memory, overwrite=True)
        self._bank_populate_agendas_data()

    def _bank_populate_agendas_data(self):
        for file_name in self.get_public_dir_file_names_list():
            agenda_json = x_func_open_file(self.get_public_dir(), file_name)
            agendaunit_x = get_agenda_from_json(x_agenda_json=agenda_json)
            agendaunit_x.set_agenda_metrics()

            self._bank_insert_agendaunit(agendaunit_x)
            self._bank_insert_partyunit(agendaunit_x)
            self._bank_insert_groupunit(agendaunit_x)
            self._bank_insert_ideaunit(agendaunit_x)
            self._bank_insert_acptfact(agendaunit_x)

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
            for partyunit_x in agendaunit_x._partys.values():
                sqlstr = get_ledger_table_insert_sqlstr(agendaunit_x, partyunit_x)
                cur.execute(sqlstr)

    def _bank_insert_groupunit(self, agendaunit_x: AgendaUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for groupunit_x in agendaunit_x._groups.values():
                groupunit_catalog_x = GroupUnitCatalog(
                    agenda_healer=agendaunit_x._healer,
                    groupunit_brand=groupunit_x.brand,
                    partylinks_set_by_culture_road=groupunit_x._partylinks_set_by_culture_road,
                )
                sqlstr = get_groupunit_catalog_table_insert_sqlstr(groupunit_catalog_x)
                cur.execute(sqlstr)

    def _bank_insert_ideaunit(self, agendaunit_x: AgendaUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for idea_x in agendaunit_x._idea_dict.values():
                idea_catalog_x = IdeaCatalog(agendaunit_x._healer, idea_x.get_road())
                sqlstr = get_idea_catalog_table_insert_sqlstr(idea_catalog_x)
                cur.execute(sqlstr)

    def _bank_insert_acptfact(self, agendaunit_x: AgendaUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for acptfact_x in agendaunit_x._idearoot._acptfactunits.values():
                acptfact_catalog_x = AcptFactCatalog(
                    agenda_healer=agendaunit_x._healer,
                    base=acptfact_x.base,
                    pick=acptfact_x.pick,
                )
                sqlstr = get_acptfact_catalog_table_insert_sqlstr(acptfact_catalog_x)
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
        x_func_delete_dir(dir=self.get_bank_db_path())

    def set_cultureunit_handle(self, handle: str):
        self.handle = handle

    def get_bank_db_path(self):
        return f"{self.get_object_root_dir()}/bank.db"

    def get_object_root_dir(self):
        return f"{self.cultures_dir}/{self.handle}"

    def _create_main_file_if_null(self, x_dir):
        culture_file_name = "culture.json"
        x_func_save_file(
            dest_dir=x_dir,
            file_name=culture_file_name,
            file_text="",
        )

    def create_dirs_if_null(self, in_memory_bank: bool = None):
        culture_dir = self.get_object_root_dir()
        agendas_dir = self.get_public_dir()
        kitchenunits_dir = self.get_kitchenunits_dir()
        single_dir_create_if_null(x_path=culture_dir)
        single_dir_create_if_null(x_path=agendas_dir)
        single_dir_create_if_null(x_path=kitchenunits_dir)
        self._create_main_file_if_null(x_dir=culture_dir)
        self._create_bank_db(in_memory=in_memory_bank, overwrite=True)

    # KitchenUnit management
    def get_kitchenunits_dir(self):
        return f"{self.get_object_root_dir()}/kitchenunits"

    def get_kitchenunit_dir_paths_list(self):
        return list(
            x_func_dir_files(
                dir_path=self.get_kitchenunits_dir(),
                remove_extensions=False,
                include_dirs=True,
            ).keys()
        )

    def set_kitchenunits_empty_if_null(self):
        if self._kitchenunits is None:
            self._kitchenunits = {}

    def create_new_kitchenunit(self, kitchen_dub: KitchenDub):
        self.set_kitchenunits_empty_if_null()
        ux = kitchenunit_shop(kitchen_dub, self.get_object_root_dir(), self.handle)
        ux.create_core_dir_and_files()
        self._kitchenunits[ux._admin._kitchen_dub] = ux

    def get_kitchenunit(self, dub: KitchenDub) -> KitchenUnit:
        return None if self._kitchenunits.get(dub) is None else self._kitchenunits[dub]

    def set_kitchenunit_to_culture(self, kitchenunit: KitchenUnit):
        self._kitchenunits[kitchenunit._admin._kitchen_dub] = kitchenunit
        self.save_kitchenunit_file(kitchen_dub=kitchenunit._admin._kitchen_dub)

    def save_kitchenunit_file(self, kitchen_dub: KitchenDub):
        x_kitchenunit = self.get_kitchenunit(dub=kitchen_dub)
        x_kitchenunit._admin.save_seed_agenda(x_kitchenunit.get_seed())

    def rename_kitchenunit(self, old_dub: KitchenDub, new_dub: KitchenDub):
        kitchen_x = self.get_kitchenunit(dub=old_dub)
        old_kitchenunit_dir = kitchen_x._admin._kitchenunit_dir
        kitchen_x._admin.set_kitchen_dub(new_dub=new_dub)
        self.set_kitchenunit_to_culture(kitchen_x)
        x_func_delete_dir(old_kitchenunit_dir)
        self.del_kitchenunit_from_culture(kitchen_dub=old_dub)

    def del_kitchenunit_from_culture(self, kitchen_dub: KitchenDub):
        self._kitchenunits.pop(kitchen_dub)

    def del_kitchenunit_dir(self, kitchen_dub: KitchenDub):
        x_func_delete_dir(f"{self.get_kitchenunits_dir()}/{kitchen_dub}")

    # public dir management
    def get_public_dir(self):
        return f"{self.get_object_root_dir()}/agendas"

    def get_ignores_dir(self, kitchen_dub: KitchenDub):
        per_x = self.get_kitchenunit(kitchen_dub)
        return per_x._admin._agendas_ignore_dir

    def get_public_agenda(self, healer: str) -> AgendaUnit:
        return get_agenda_from_json(
            x_func_open_file(dest_dir=self.get_public_dir(), file_name=f"{healer}.json")
        )

    def get_agenda_from_ignores_dir(
        self, kitchen_dub: KitchenDub, _healer: str
    ) -> AgendaUnit:
        return get_agenda_from_json(
            x_func_open_file(
                dest_dir=self.get_ignores_dir(kitchen_dub=kitchen_dub),
                file_name=f"{_healer}.json",
            )
        )

    def set_ignore_agenda_file(self, kitchen_dub: KitchenDub, agenda_obj: AgendaUnit):
        x_kitchenunit = self.get_kitchenunit(dub=kitchen_dub)
        x_kitchenunit.set_ignore_agenda_file(
            agendaunit=agenda_obj, src_agenda_healer=agenda_obj._healer
        )

    def rename_public_agenda(self, old_healer: str, new_healer: str):
        x_agenda = self.get_public_agenda(healer=old_healer)
        x_agenda.set_healer(new_healer=new_healer)
        self.save_public_agenda(x_agenda=x_agenda)
        self.del_public_agenda(x_agenda_healer=old_healer)

    def del_public_agenda(self, x_agenda_healer: str):
        x_func_delete_dir(f"{self.get_public_dir()}/{x_agenda_healer}.json")

    def save_public_agenda(self, x_agenda: AgendaUnit):
        x_agenda.set_culture_handle(culture_handle=self.handle)
        x_func_save_file(
            dest_dir=self.get_public_dir(),
            file_name=f"{x_agenda._healer}.json",
            file_text=x_agenda.get_json(),
        )

    def reload_all_kitchenunits_src_agendaunits(self):
        for x_kitchenunit in self._kitchenunits.values():
            x_kitchenunit.refresh_depot_agendas()

    def get_public_dir_file_names_list(self):
        return list(x_func_dir_files(dir_path=self.get_public_dir()).keys())

    # agendas_dir to healer_agendas_dir management
    def _kitchenunit_set_depot_agenda(
        self,
        kitchenunit: KitchenUnit,
        agendaunit: AgendaUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_agenda: AgendaUnit = None,
    ):
        kitchenunit.set_depot_agenda(
            x_agenda=agendaunit,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )
        if depotlink_type == "ignore" and ignore_agenda != None:
            kitchenunit.set_ignore_agenda_file(
                agendaunit=ignore_agenda, src_agenda_healer=agendaunit._healer
            )

    def set_healer_depotlink(
        self,
        kitchen_dub: KitchenDub,
        agenda_healer: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_agenda: AgendaUnit = None,
    ):
        x_kitchenunit = self.get_kitchenunit(dub=kitchen_dub)
        x_agenda = self.get_public_agenda(healer=agenda_healer)
        self._kitchenunit_set_depot_agenda(
            kitchenunit=x_kitchenunit,
            agendaunit=x_agenda,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
            ignore_agenda=ignore_agenda,
        )

    def create_depotlink_to_generated_agenda(
        self,
        kitchen_dub: KitchenDub,
        agenda_healer: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        x_kitchenunit = self.get_kitchenunit(dub=kitchen_dub)
        x_agenda = agendaunit_shop(_healer=agenda_healer)
        self._kitchenunit_set_depot_agenda(
            kitchenunit=x_kitchenunit,
            agendaunit=x_agenda,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def update_depotlink(
        self,
        kitchen_dub: KitchenDub,
        partytitle: PartyTitle,
        depotlink_type: str,
        creditor_weight: str,
        debtor_weight: str,
    ):
        x_kitchenunit = self.get_kitchenunit(dub=kitchen_dub)
        x_agenda = self.get_public_agenda(_healer=partytitle)
        self._kitchenunit_set_depot_agenda(
            kitchenunit=x_kitchenunit,
            agendaunit=x_agenda,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def del_depotlink(self, kitchen_dub: KitchenDub, agendaunit_healer: str):
        x_kitchenunit = self.get_kitchenunit(dub=kitchen_dub)
        x_kitchenunit.del_depot_agenda(agenda_healer=agendaunit_healer)

    # Healer output_agenda
    def get_output_agenda(self, kitchen_dub: KitchenDub) -> AgendaUnit:
        x_kitchenunit = self.get_kitchenunit(dub=kitchen_dub)
        return x_kitchenunit._admin.get_remelded_output_agenda()


def cultureunit_shop(
    handle: CultureHandle,
    cultures_dir: str,
    _manager_name: PersonName = None,
    _kitchenunits: dict[str:KitchenUnit] = None,
    in_memory_bank: bool = None,
):
    if in_memory_bank is None:
        in_memory_bank = True
    culture_x = CultureUnit(
        handle=handle,
        cultures_dir=cultures_dir,
        _kitchenunits=_kitchenunits,
    )
    culture_x.set_manager_name(_manager_name)
    culture_x.create_dirs_if_null(in_memory_bank=in_memory_bank)
    return culture_x


def set_bank_river_tallys_to_agenda_partyunits(
    x_agenda: AgendaUnit, river_tallys: dict[str:]
):
    for partyunit_x in x_agenda._partys.values():
        partyunit_x.clear_banking_data()
        river_tally = river_tallys.get(partyunit_x.title)
        if river_tally != None:
            partyunit_x.set_banking_data(
                tax_paid=river_tally.tax_total,
                tax_diff=river_tally.tax_diff,
                credit_score=river_tally.credit_score,
                voice_rank=river_tally.voice_rank,
            )
