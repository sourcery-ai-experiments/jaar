from src.deal.deal import (
    DealUnit,
    get_from_json as get_deal_from_json,
    partylink_shop,
    PartyTitle,
)
from src.deal.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from src.project.harvest import HarvestUnit, harvestunit_shop
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from src.project.bank_sqlstr import (
    get_river_flow_table_delete_sqlstr,
    get_river_flow_table_insert_sqlstr,
    get_river_tparty_table_delete_sqlstr,
    get_river_tparty_table_insert_sqlstr,
    get_river_tparty_dict,
    get_river_bucket_table_insert_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
    get_ledger_table_insert_sqlstr,
    get_deal_table_insert_sqlstr,
    get_river_ledger_unit,
    LedgerUnit,
    RiverLedgerUnit,
    RiverFlowUnit,
    RiverTpartyUnit,
    IdeaCatalog,
    get_idea_catalog_table_insert_sqlstr,
    get_idea_catalog_dict,
    AcptFactCatalog,
    get_acptfact_catalog_table_insert_sqlstr,
    GroupUnitCatalog,
    get_groupunit_catalog_table_insert_sqlstr,
    get_groupunit_catalog_dict,
)


class ProjectHandle(str):
    pass


@dataclass
class ProjectUnit:
    handle: ProjectHandle
    projects_dir: str
    _person_importance: float = None
    _harvestunits: dict[str:HarvestUnit] = None
    _bank_db = None

    def set_person_importance(self, person_importance: float):
        self._person_importance = person_importance

    # banking
    def set_deal_bank_attrs(self, deal_healer: str):
        deal_obj = self.get_public_deal(deal_healer)

        for groupunit_x in deal_obj._groups.values():
            if groupunit_x._partylinks_set_by_project_road != None:
                groupunit_x.clear_partylinks()
                ic = get_idea_catalog_dict(
                    self.get_bank_conn(), groupunit_x._partylinks_set_by_project_road
                )
                for idea_catalog in ic.values():
                    if deal_healer != idea_catalog.deal_healer:
                        partylink_x = partylink_shop(title=idea_catalog.deal_healer)
                        groupunit_x.set_partylink(partylink_x)
        self.save_public_deal(deal_obj)

        # refresh bank metrics
        self.refresh_bank_metrics()

    def set_river_sphere_for_deal(self, deal_healer: str, max_flows_count: int = None):
        self._clear_all_source_river_data(deal_healer)
        general_bucket = [self._get_root_river_ledger_unit(deal_healer)]

        if max_flows_count is None:
            max_flows_count = 40

        flows_count = 0
        while flows_count < max_flows_count and general_bucket != []:
            parent_deal_ledger = general_bucket.pop(0)

            parent_range = parent_deal_ledger.get_range()
            parent_close = parent_deal_ledger.currency_cease
            curr_onset = parent_deal_ledger.currency_onset

            ledgers_len = len(parent_deal_ledger._ledgers.values())
            ledgers_count = 0
            for led_x in parent_deal_ledger._ledgers.values():
                ledgers_count += 1

                curr_range = parent_range * led_x._deal_agenda_ratio_credit
                curr_close = curr_onset + curr_range

                # implies last element in dict
                if ledgers_count == ledgers_len and curr_close != parent_close:
                    curr_close = parent_close

                river_flow_x = RiverFlowUnit(
                    currency_deal_healer=deal_healer,
                    src_title=led_x.deal_healer,
                    dst_title=led_x.party_title,
                    currency_start=curr_onset,
                    currency_close=curr_close,
                    flow_num=flows_count,
                    parent_flow_num=parent_deal_ledger.flow_num,
                    river_tree_level=parent_deal_ledger.river_tree_level + 1,
                )
                river_ledger_x = self._insert_river_flow_grab_river_ledger(river_flow_x)
                if river_ledger_x != None:
                    general_bucket.append(river_ledger_x)

                flows_count += 1
                if flows_count >= max_flows_count:
                    break

                # change curr_onset for next
                curr_onset += curr_range

        self._set_river_tpartys_buckets(deal_healer)

    def _insert_river_flow_grab_river_ledger(
        self, river_flow_x: RiverFlowUnit
    ) -> RiverLedgerUnit:
        river_ledger_x = None

        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_flow_table_insert_sqlstr(river_flow_x))

            if river_flow_x.flow_returned() == False:
                river_ledger_x = get_river_ledger_unit(bank_conn, river_flow_x)

        return river_ledger_x

    def _clear_all_source_river_data(self, deal_healer: str):
        with self.get_bank_conn() as bank_conn:
            flow_s = get_river_flow_table_delete_sqlstr(deal_healer)
            mstr_s = get_river_tparty_table_delete_sqlstr(deal_healer)
            bank_conn.execute(flow_s)
            bank_conn.execute(mstr_s)

    def _get_root_river_ledger_unit(self, deal_healer: str) -> RiverLedgerUnit:
        default_currency_onset = 0.0
        default_currency_cease = 1.0
        default_root_river_tree_level = 0
        default_root_flow_num = None  # maybe change to 1?
        default_root_parent_flow_num = None
        root_river_flow = RiverFlowUnit(
            currency_deal_healer=deal_healer,
            src_title=None,
            dst_title=deal_healer,
            currency_start=default_currency_onset,
            currency_close=default_currency_cease,
            flow_num=default_root_flow_num,
            parent_flow_num=default_root_parent_flow_num,
            river_tree_level=default_root_river_tree_level,
        )
        with self.get_bank_conn() as bank_conn:
            source_river_ledger = get_river_ledger_unit(bank_conn, root_river_flow)
        return source_river_ledger

    def _set_river_tpartys_buckets(self, deal_healer: str):
        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_tparty_table_insert_sqlstr(deal_healer))
            bank_conn.execute(get_river_bucket_table_insert_sqlstr(deal_healer))

            sal_river_tpartys = get_river_tparty_dict(bank_conn, deal_healer)
            deal_x = self.get_public_deal(healer=deal_healer)
            deal_x.set_banking_attr_partyunits(sal_river_tpartys)
            self.save_public_deal(deal_x=deal_x)

    def get_river_tpartys(self, deal_healer: str) -> dict[str:RiverTpartyUnit]:
        with self.get_bank_conn() as bank_conn:
            river_tpartys = get_river_tparty_dict(bank_conn, deal_healer)
        return river_tpartys

    def refresh_bank_metrics(self, in_memory: bool = None):
        if in_memory is None and self._bank_db != None:
            in_memory = True
        self._create_bank_db(in_memory=in_memory, overwrite=True)
        self._bank_populate_deals_data()

    def _bank_populate_deals_data(self):
        for file_title in self.get_public_dir_file_titles_list():
            deal_json = x_func_open_file(self.get_public_dir(), file_title)
            dealunit_x = get_deal_from_json(x_deal_json=deal_json)
            dealunit_x.set_deal_metrics()

            self._bank_insert_dealunit(dealunit_x)
            self._bank_insert_partyunit(dealunit_x)
            self._bank_insert_groupunit(dealunit_x)
            self._bank_insert_ideaunit(dealunit_x)
            self._bank_insert_acptfact(dealunit_x)

    def _bank_insert_dealunit(self, dealunit_x: DealUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            cur.execute(get_deal_table_insert_sqlstr(deal_x=dealunit_x))

    def _bank_insert_partyunit(self, dealunit_x: DealUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for partyunit_x in dealunit_x._partys.values():
                sqlstr = get_ledger_table_insert_sqlstr(dealunit_x, partyunit_x)
                cur.execute(sqlstr)

    def _bank_insert_groupunit(self, dealunit_x: DealUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for groupunit_x in dealunit_x._groups.values():
                groupunit_catalog_x = GroupUnitCatalog(
                    deal_healer=dealunit_x._healer,
                    groupunit_brand=groupunit_x.brand,
                    partylinks_set_by_project_road=groupunit_x._partylinks_set_by_project_road,
                )
                sqlstr = get_groupunit_catalog_table_insert_sqlstr(groupunit_catalog_x)
                cur.execute(sqlstr)

    def _bank_insert_ideaunit(self, dealunit_x: DealUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for idea_x in dealunit_x._idea_dict.values():
                idea_catalog_x = IdeaCatalog(dealunit_x._healer, idea_x.get_road())
                sqlstr = get_idea_catalog_table_insert_sqlstr(idea_catalog_x)
                cur.execute(sqlstr)

    def _bank_insert_acptfact(self, dealunit_x: DealUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for acptfact_x in dealunit_x._idearoot._acptfactunits.values():
                acptfact_catalog_x = AcptFactCatalog(
                    deal_healer=dealunit_x._healer,
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

    def set_projectunit_handle(self, handle: str):
        self.handle = handle

    def get_bank_db_path(self):
        return f"{self.get_object_root_dir()}/bank.db"

    def get_object_root_dir(self):
        return f"{self.projects_dir}/{self.handle}"

    def _create_main_file_if_null(self, x_dir):
        project_file_title = "project.json"
        x_func_save_file(
            dest_dir=x_dir,
            file_title=project_file_title,
            file_text="",
        )

    def create_dirs_if_null(self, in_memory_bank: bool = None):
        project_dir = self.get_object_root_dir()
        deals_dir = self.get_public_dir()
        harvestunits_dir = self.get_harvestunits_dir()
        single_dir_create_if_null(x_path=project_dir)
        single_dir_create_if_null(x_path=deals_dir)
        single_dir_create_if_null(x_path=harvestunits_dir)
        self._create_main_file_if_null(x_dir=project_dir)
        self._create_bank_db(in_memory=in_memory_bank, overwrite=True)

    # HarvestUnit management
    def get_harvestunits_dir(self):
        return f"{self.get_object_root_dir()}/harvestunits"

    def get_harvestunit_dir_paths_list(self):
        return list(
            x_func_dir_files(
                dir_path=self.get_harvestunits_dir(),
                remove_extensions=False,
                include_dirs=True,
            ).keys()
        )

    def set_harvestunits_empty_if_null(self):
        if self._harvestunits is None:
            self._harvestunits = {}

    def create_new_harvestunit(self, harvest_title: str):
        self.set_harvestunits_empty_if_null()
        ux = harvestunit_shop(harvest_title, self.get_object_root_dir(), self.handle)
        ux.create_core_dir_and_files()
        self._harvestunits[ux._admin._harvest_title] = ux

    def get_harvestunit(self, title: str) -> HarvestUnit:
        return (
            None if self._harvestunits.get(title) is None else self._harvestunits[title]
        )

    def create_harvestunit_from_public(self, title: str):
        x_deal = self.get_public_deal(healer=title)
        x_harvestunit = harvestunit_shop(
            title=x_deal._healer, env_dir=self.get_object_root_dir()
        )
        self.set_harvestunits_empty_if_null()
        self.set_harvestunit_to_project(x_harvestunit)

    def set_harvestunit_to_project(self, harvestunit: HarvestUnit):
        self._harvestunits[harvestunit._admin._harvest_title] = harvestunit
        self.save_harvestunit_file(harvest_title=harvestunit._admin._harvest_title)

    def save_harvestunit_file(self, harvest_title: str):
        x_harvestunit = self.get_harvestunit(title=harvest_title)
        x_harvestunit._admin.save_seed_deal(x_harvestunit.get_seed())

    def rename_harvestunit(self, old_title: str, new_title: str):
        harvest_x = self.get_harvestunit(title=old_title)
        old_harvestunit_dir = harvest_x._admin._harvestunit_dir
        harvest_x._admin.set_harvest_title(new_title=new_title)
        self.set_harvestunit_to_project(harvest_x)
        x_func_delete_dir(old_harvestunit_dir)
        self.del_harvestunit_from_project(harvest_title=old_title)

    def del_harvestunit_from_project(self, harvest_title):
        self._harvestunits.pop(harvest_title)

    def del_harvestunit_dir(self, harvest_title: str):
        x_func_delete_dir(f"{self.get_harvestunits_dir()}/{harvest_title}")

    # public dir management
    def get_public_dir(self):
        return f"{self.get_object_root_dir()}/deals"

    def get_ignores_dir(self, harvest_title: str):
        per_x = self.get_harvestunit(harvest_title)
        return per_x._admin._deals_ignore_dir

    def get_public_deal(self, healer: str) -> DealUnit:
        return get_deal_from_json(
            x_func_open_file(
                dest_dir=self.get_public_dir(), file_title=f"{healer}.json"
            )
        )

    def get_deal_from_ignores_dir(self, harvest_title: str, _healer: str) -> DealUnit:
        return get_deal_from_json(
            x_func_open_file(
                dest_dir=self.get_ignores_dir(harvest_title=harvest_title),
                file_title=f"{_healer}.json",
            )
        )

    def set_ignore_deal_file(self, harvest_title: str, deal_obj: DealUnit):
        x_harvestunit = self.get_harvestunit(title=harvest_title)
        x_harvestunit.set_ignore_deal_file(
            dealunit=deal_obj, src_deal_healer=deal_obj._healer
        )

    def rename_public_deal(self, old_healer: str, new_healer: str):
        deal_x = self.get_public_deal(healer=old_healer)
        deal_x.set_healer(new_healer=new_healer)
        self.save_public_deal(deal_x=deal_x)
        self.del_public_deal(deal_x_healer=old_healer)

    def del_public_deal(self, deal_x_healer: str):
        x_func_delete_dir(f"{self.get_public_dir()}/{deal_x_healer}.json")

    def save_public_deal(self, deal_x: DealUnit):
        deal_x.set_project_handle(project_handle=self.handle)
        x_func_save_file(
            dest_dir=self.get_public_dir(),
            file_title=f"{deal_x._healer}.json",
            file_text=deal_x.get_json(),
        )

    def reload_all_harvestunits_src_dealunits(self):
        for x_harvestunit in self._harvestunits.values():
            x_harvestunit.refresh_depot_deals()

    def get_public_dir_file_titles_list(self):
        return list(x_func_dir_files(dir_path=self.get_public_dir()).keys())

    # deals_dir to healer_deals_dir management
    def _harvestunit_set_depot_deal(
        self,
        harvestunit: HarvestUnit,
        dealunit: DealUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_deal: DealUnit = None,
    ):
        harvestunit.set_depot_deal(
            deal_x=dealunit,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )
        if depotlink_type == "ignore" and ignore_deal != None:
            harvestunit.set_ignore_deal_file(
                dealunit=ignore_deal, src_deal_healer=dealunit._healer
            )

    def set_healer_depotlink(
        self,
        harvest_title: str,
        deal_healer: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_deal: DealUnit = None,
    ):
        x_harvestunit = self.get_harvestunit(title=harvest_title)
        deal_x = self.get_public_deal(healer=deal_healer)
        self._harvestunit_set_depot_deal(
            harvestunit=x_harvestunit,
            dealunit=deal_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
            ignore_deal=ignore_deal,
        )

    def create_depotlink_to_generated_deal(
        self,
        harvest_title: str,
        deal_healer: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        x_harvestunit = self.get_harvestunit(title=harvest_title)
        deal_x = DealUnit(_healer=deal_healer)
        self._harvestunit_set_depot_deal(
            harvestunit=x_harvestunit,
            dealunit=deal_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def update_depotlink(
        self,
        harvest_title: str,
        partytitle: PartyTitle,
        depotlink_type: str,
        creditor_weight: str,
        debtor_weight: str,
    ):
        x_harvestunit = self.get_harvestunit(title=harvest_title)
        deal_x = self.get_public_deal(_healer=partytitle)
        self._harvestunit_set_depot_deal(
            harvestunit=x_harvestunit,
            dealunit=deal_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def del_depotlink(self, harvest_title: str, dealunit_healer: str):
        x_harvestunit = self.get_harvestunit(title=harvest_title)
        x_harvestunit.del_depot_deal(deal_healer=dealunit_healer)

    # Healer output_deal
    def get_output_deal(self, harvest_title: str) -> DealUnit:
        x_harvestunit = self.get_harvestunit(title=harvest_title)
        return x_harvestunit._admin.get_remelded_output_deal()


def projectunit_shop(
    handle: str,
    projects_dir: str,
    _harvestunits: dict[str:HarvestUnit] = None,
    in_memory_bank: bool = None,
):
    if in_memory_bank is None:
        in_memory_bank = True
    project_x = ProjectUnit(
        handle=handle, projects_dir=projects_dir, _harvestunits=_harvestunits
    )
    project_x.create_dirs_if_null(in_memory_bank=in_memory_bank)
    return project_x
