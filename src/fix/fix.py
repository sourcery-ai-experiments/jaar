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
from src.fix.remedy import RemedyUnit, remedyunit_shop
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from src.fix.bank_sqlstr import (
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


class FixHandle(str):
    pass


@dataclass
class FixUnit:
    handle: FixHandle
    fixs_dir: str
    _person_importance: float = None
    _remedyunits: dict[str:RemedyUnit] = None
    _bank_db = None

    def set_person_importance(self, person_importance: float):
        self._person_importance = person_importance

    # banking
    def set_deal_bank_attrs(self, deal_healer: str):
        deal_obj = self.get_public_deal(deal_healer)

        for groupunit_x in deal_obj._groups.values():
            if groupunit_x._partylinks_set_by_fix_road != None:
                groupunit_x.clear_partylinks()
                ic = get_idea_catalog_dict(
                    self.get_bank_conn(), groupunit_x._partylinks_set_by_fix_road
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
                    partylinks_set_by_fix_road=groupunit_x._partylinks_set_by_fix_road,
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

    def set_fixunit_handle(self, handle: str):
        self.handle = handle

    def get_bank_db_path(self):
        return f"{self.get_object_root_dir()}/bank.db"

    def get_object_root_dir(self):
        return f"{self.fixs_dir}/{self.handle}"

    def _create_main_file_if_null(self, x_dir):
        fix_file_title = "fix.json"
        x_func_save_file(
            dest_dir=x_dir,
            file_title=fix_file_title,
            file_text="",
        )

    def create_dirs_if_null(self, in_memory_bank: bool = None):
        fix_dir = self.get_object_root_dir()
        deals_dir = self.get_public_dir()
        remedyunits_dir = self.get_remedyunits_dir()
        single_dir_create_if_null(x_path=fix_dir)
        single_dir_create_if_null(x_path=deals_dir)
        single_dir_create_if_null(x_path=remedyunits_dir)
        self._create_main_file_if_null(x_dir=fix_dir)
        self._create_bank_db(in_memory=in_memory_bank, overwrite=True)

    # RemedyUnit management
    def get_remedyunits_dir(self):
        return f"{self.get_object_root_dir()}/remedyunits"

    def get_remedyunit_dir_paths_list(self):
        return list(
            x_func_dir_files(
                dir_path=self.get_remedyunits_dir(),
                remove_extensions=False,
                include_dirs=True,
            ).keys()
        )

    def set_remedyunits_empty_if_null(self):
        if self._remedyunits is None:
            self._remedyunits = {}

    def create_new_remedyunit(self, remedy_title: str):
        self.set_remedyunits_empty_if_null()
        ux = remedyunit_shop(remedy_title, self.get_object_root_dir(), self.handle)
        ux.create_core_dir_and_files()
        self._remedyunits[ux._admin._remedy_title] = ux

    def get_remedyunit(self, title: str) -> RemedyUnit:
        return (
            None if self._remedyunits.get(title) is None else self._remedyunits[title]
        )

    def create_remedyunit_from_public(self, title: str):
        x_deal = self.get_public_deal(healer=title)
        x_remedyunit = remedyunit_shop(
            title=x_deal._healer, env_dir=self.get_object_root_dir()
        )
        self.set_remedyunits_empty_if_null()
        self.set_remedyunit_to_fix(x_remedyunit)

    def set_remedyunit_to_fix(self, remedyunit: RemedyUnit):
        self._remedyunits[remedyunit._admin._remedy_title] = remedyunit
        self.save_remedyunit_file(remedy_title=remedyunit._admin._remedy_title)

    def save_remedyunit_file(self, remedy_title: str):
        x_remedyunit = self.get_remedyunit(title=remedy_title)
        x_remedyunit._admin.save_isol_deal(x_remedyunit.get_isol())

    def rename_remedyunit(self, old_title: str, new_title: str):
        remedy_x = self.get_remedyunit(title=old_title)
        old_remedyunit_dir = remedy_x._admin._remedyunit_dir
        remedy_x._admin.set_remedy_title(new_title=new_title)
        self.set_remedyunit_to_fix(remedy_x)
        x_func_delete_dir(old_remedyunit_dir)
        self.del_remedyunit_from_fix(remedy_title=old_title)

    def del_remedyunit_from_fix(self, remedy_title):
        self._remedyunits.pop(remedy_title)

    def del_remedyunit_dir(self, remedy_title: str):
        x_func_delete_dir(f"{self.get_remedyunits_dir()}/{remedy_title}")

    # public dir management
    def get_public_dir(self):
        return f"{self.get_object_root_dir()}/deals"

    def get_ignores_dir(self, remedy_title: str):
        per_x = self.get_remedyunit(remedy_title)
        return per_x._admin._deals_ignore_dir

    def get_public_deal(self, healer: str) -> DealUnit:
        return get_deal_from_json(
            x_func_open_file(
                dest_dir=self.get_public_dir(), file_title=f"{healer}.json"
            )
        )

    def get_deal_from_ignores_dir(self, remedy_title: str, _healer: str) -> DealUnit:
        return get_deal_from_json(
            x_func_open_file(
                dest_dir=self.get_ignores_dir(remedy_title=remedy_title),
                file_title=f"{_healer}.json",
            )
        )

    def set_ignore_deal_file(self, remedy_title: str, deal_obj: DealUnit):
        x_remedyunit = self.get_remedyunit(title=remedy_title)
        x_remedyunit.set_ignore_deal_file(
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
        deal_x.set_fix_handle(fix_handle=self.handle)
        x_func_save_file(
            dest_dir=self.get_public_dir(),
            file_title=f"{deal_x._healer}.json",
            file_text=deal_x.get_json(),
        )

    def reload_all_remedyunits_src_dealunits(self):
        for x_remedyunit in self._remedyunits.values():
            x_remedyunit.refresh_depot_deals()

    def get_public_dir_file_titles_list(self):
        return list(x_func_dir_files(dir_path=self.get_public_dir()).keys())

    # deals_dir to healer_deals_dir management
    def _remedyunit_set_depot_deal(
        self,
        remedyunit: RemedyUnit,
        dealunit: DealUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_deal: DealUnit = None,
    ):
        remedyunit.set_depot_deal(
            deal_x=dealunit,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )
        if depotlink_type == "ignore" and ignore_deal != None:
            remedyunit.set_ignore_deal_file(
                dealunit=ignore_deal, src_deal_healer=dealunit._healer
            )

    def set_healer_depotlink(
        self,
        remedy_title: str,
        deal_healer: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_deal: DealUnit = None,
    ):
        x_remedyunit = self.get_remedyunit(title=remedy_title)
        deal_x = self.get_public_deal(healer=deal_healer)
        self._remedyunit_set_depot_deal(
            remedyunit=x_remedyunit,
            dealunit=deal_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
            ignore_deal=ignore_deal,
        )

    def create_depotlink_to_generated_deal(
        self,
        remedy_title: str,
        deal_healer: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        x_remedyunit = self.get_remedyunit(title=remedy_title)
        deal_x = DealUnit(_healer=deal_healer)
        self._remedyunit_set_depot_deal(
            remedyunit=x_remedyunit,
            dealunit=deal_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def update_depotlink(
        self,
        remedy_title: str,
        partytitle: PartyTitle,
        depotlink_type: str,
        creditor_weight: str,
        debtor_weight: str,
    ):
        x_remedyunit = self.get_remedyunit(title=remedy_title)
        deal_x = self.get_public_deal(_healer=partytitle)
        self._remedyunit_set_depot_deal(
            remedyunit=x_remedyunit,
            dealunit=deal_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def del_depotlink(self, remedy_title: str, dealunit_healer: str):
        x_remedyunit = self.get_remedyunit(title=remedy_title)
        x_remedyunit.del_depot_deal(deal_healer=dealunit_healer)

    # Healer output_deal
    def get_output_deal(self, remedy_title: str) -> DealUnit:
        x_remedyunit = self.get_remedyunit(title=remedy_title)
        return x_remedyunit._admin.get_remelded_output_deal()


def fixunit_shop(
    handle: str,
    fixs_dir: str,
    _remedyunits: dict[str:RemedyUnit] = None,
    in_memory_bank: bool = None,
):
    if in_memory_bank is None:
        in_memory_bank = True
    fix_x = FixUnit(handle=handle, fixs_dir=fixs_dir, _remedyunits=_remedyunits)
    fix_x.create_dirs_if_null(in_memory_bank=in_memory_bank)
    return fix_x
