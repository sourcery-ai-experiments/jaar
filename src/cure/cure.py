from src.pact.pact import (
    ContractUnit,
    get_from_json as get_pact_from_json,
    partylink_shop,
    PartyTitle,
)
from src.pact.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from src.cure.healer import HealerUnit, healerunit_shop
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from src.cure.bank_sqlstr import (
    get_river_flow_table_delete_sqlstr,
    get_river_flow_table_insert_sqlstr,
    get_river_tparty_table_delete_sqlstr,
    get_river_tparty_table_insert_sqlstr,
    get_river_tparty_dict,
    get_river_bucket_table_insert_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
    get_ledger_table_insert_sqlstr,
    get_pact_table_insert_sqlstr,
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


class CureHandle(str):
    pass


@dataclass
class CureUnit:
    handle: CureHandle
    cures_dir: str
    _person_importance: float = None
    _healerunits: dict[str:HealerUnit] = None
    _bank_db = None

    def set_person_importance(self, person_importance: float):
        self._person_importance = person_importance

    def set_pact_bank_attrs(self, pact_healer: str):
        pact_obj = self.get_public_pact(pact_healer)

        for groupunit_x in pact_obj._groups.values():
            if groupunit_x._partylinks_set_by_cure_road != None:
                groupunit_x.clear_partylinks()
                ic = get_idea_catalog_dict(
                    self.get_bank_conn(), groupunit_x._partylinks_set_by_cure_road
                )
                for idea_catalog in ic.values():
                    if pact_healer != idea_catalog.pact_healer:
                        partylink_x = partylink_shop(title=idea_catalog.pact_healer)
                        groupunit_x.set_partylink(partylink_x)
        self.save_public_pact(pact_obj)

        # refresh bank metrics
        self.refresh_bank_metrics()

    # banking
    def set_river_sphere_for_pact(self, pact_healer: str, max_flows_count: int = None):
        self._clear_all_source_river_data(pact_healer)
        general_bucket = [self._get_root_river_ledger_unit(pact_healer)]

        if max_flows_count is None:
            max_flows_count = 40

        flows_count = 0
        while flows_count < max_flows_count and general_bucket != []:
            parent_pact_ledger = general_bucket.pop(0)

            parent_range = parent_pact_ledger.get_range()
            parent_close = parent_pact_ledger.currency_cease
            curr_onset = parent_pact_ledger.currency_onset

            ledgers_len = len(parent_pact_ledger._ledgers.values())
            ledgers_count = 0
            for led_x in parent_pact_ledger._ledgers.values():
                ledgers_count += 1

                curr_range = parent_range * led_x._pact_agenda_ratio_credit
                curr_close = curr_onset + curr_range

                # implies last element in dict
                if ledgers_count == ledgers_len and curr_close != parent_close:
                    curr_close = parent_close

                river_flow_x = RiverFlowUnit(
                    currency_pact_healer=pact_healer,
                    src_title=led_x.pact_healer,
                    dst_title=led_x.party_title,
                    currency_start=curr_onset,
                    currency_close=curr_close,
                    flow_num=flows_count,
                    parent_flow_num=parent_pact_ledger.flow_num,
                    river_tree_level=parent_pact_ledger.river_tree_level + 1,
                )
                river_ledger_x = self._insert_river_flow_grab_river_ledger(river_flow_x)
                if river_ledger_x != None:
                    general_bucket.append(river_ledger_x)

                flows_count += 1
                if flows_count >= max_flows_count:
                    break

                # change curr_onset for next
                curr_onset += curr_range

        self._set_river_tpartys_buckets(pact_healer)

    def _insert_river_flow_grab_river_ledger(
        self, river_flow_x: RiverFlowUnit
    ) -> RiverLedgerUnit:
        river_ledger_x = None

        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_flow_table_insert_sqlstr(river_flow_x))

            if river_flow_x.flow_returned() == False:
                river_ledger_x = get_river_ledger_unit(bank_conn, river_flow_x)

        return river_ledger_x

    def _clear_all_source_river_data(self, pact_healer: str):
        with self.get_bank_conn() as bank_conn:
            flow_s = get_river_flow_table_delete_sqlstr(pact_healer)
            mstr_s = get_river_tparty_table_delete_sqlstr(pact_healer)
            bank_conn.execute(flow_s)
            bank_conn.execute(mstr_s)

    def _get_root_river_ledger_unit(self, pact_healer: str) -> RiverLedgerUnit:
        default_currency_onset = 0.0
        default_currency_cease = 1.0
        default_root_river_tree_level = 0
        default_root_flow_num = None  # maybe change to 1?
        default_root_parent_flow_num = None
        root_river_flow = RiverFlowUnit(
            currency_pact_healer=pact_healer,
            src_title=None,
            dst_title=pact_healer,
            currency_start=default_currency_onset,
            currency_close=default_currency_cease,
            flow_num=default_root_flow_num,
            parent_flow_num=default_root_parent_flow_num,
            river_tree_level=default_root_river_tree_level,
        )
        with self.get_bank_conn() as bank_conn:
            source_river_ledger = get_river_ledger_unit(bank_conn, root_river_flow)
        return source_river_ledger

    def _set_river_tpartys_buckets(self, pact_healer: str):
        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_tparty_table_insert_sqlstr(pact_healer))
            bank_conn.execute(get_river_bucket_table_insert_sqlstr(pact_healer))

            sal_river_tpartys = get_river_tparty_dict(bank_conn, pact_healer)
            pact_x = self.get_public_pact(healer=pact_healer)
            pact_x.set_banking_attr_partyunits(sal_river_tpartys)
            self.save_public_pact(pact_x=pact_x)

    def get_river_tpartys(self, pact_healer: str) -> dict[str:RiverTpartyUnit]:
        with self.get_bank_conn() as bank_conn:
            river_tpartys = get_river_tparty_dict(bank_conn, pact_healer)
        return river_tpartys

    def refresh_bank_metrics(self, in_memory: bool = None):
        if in_memory is None and self._bank_db != None:
            in_memory = True
        self._create_bank_db(in_memory=in_memory, overwrite=True)
        self._bank_populate_pacts_data()

    def _bank_populate_pacts_data(self):
        for file_title in self.get_public_dir_file_titles_list():
            pact_json = x_func_open_file(self.get_public_dir(), file_title)
            pactunit_x = get_pact_from_json(cx_json=pact_json)
            pactunit_x.set_pact_metrics()

            self._bank_insert_pactunit(pactunit_x)
            self._bank_insert_partyunit(pactunit_x)
            self._bank_insert_groupunit(pactunit_x)
            self._bank_insert_ideaunit(pactunit_x)
            self._bank_insert_acptfact(pactunit_x)

    def _bank_insert_pactunit(self, pactunit_x: ContractUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            cur.execute(get_pact_table_insert_sqlstr(pact_x=pactunit_x))

    def _bank_insert_partyunit(self, pactunit_x: ContractUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for partyunit_x in pactunit_x._partys.values():
                sqlstr = get_ledger_table_insert_sqlstr(pactunit_x, partyunit_x)
                cur.execute(sqlstr)

    def _bank_insert_groupunit(self, pactunit_x: ContractUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for groupunit_x in pactunit_x._groups.values():
                groupunit_catalog_x = GroupUnitCatalog(
                    pact_healer=pactunit_x._healer,
                    groupunit_brand=groupunit_x.brand,
                    partylinks_set_by_cure_road=groupunit_x._partylinks_set_by_cure_road,
                )
                sqlstr = get_groupunit_catalog_table_insert_sqlstr(groupunit_catalog_x)
                cur.execute(sqlstr)

    def _bank_insert_ideaunit(self, pactunit_x: ContractUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for idea_x in pactunit_x._idea_dict.values():
                idea_catalog_x = IdeaCatalog(pactunit_x._healer, idea_x.get_road())
                sqlstr = get_idea_catalog_table_insert_sqlstr(idea_catalog_x)
                cur.execute(sqlstr)

    def _bank_insert_acptfact(self, pactunit_x: ContractUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for acptfact_x in pactunit_x._idearoot._acptfactunits.values():
                acptfact_catalog_x = AcptFactCatalog(
                    pact_healer=pactunit_x._healer,
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

    def set_cureunit_handle(self, handle: str):
        self.handle = handle

    def get_bank_db_path(self):
        return f"{self.get_object_root_dir()}/bank.db"

    def get_object_root_dir(self):
        return f"{self.cures_dir}/{self.handle}"

    def _create_main_file_if_null(self, x_dir):
        cure_file_title = "cure.json"
        x_func_save_file(
            dest_dir=x_dir,
            file_title=cure_file_title,
            file_text="",
        )

    def create_dirs_if_null(self, in_memory_bank: bool = None):
        cure_dir = self.get_object_root_dir()
        pacts_dir = self.get_public_dir()
        healers_dir = self.get_healers_dir()
        single_dir_create_if_null(x_path=cure_dir)
        single_dir_create_if_null(x_path=pacts_dir)
        single_dir_create_if_null(x_path=healers_dir)
        self._create_main_file_if_null(x_dir=cure_dir)
        self._create_bank_db(in_memory=in_memory_bank, overwrite=True)

    # HealerUnit management
    def get_healers_dir(self):
        return f"{self.get_object_root_dir()}/healers"

    def get_healer_dir_paths_list(self):
        return list(
            x_func_dir_files(
                dir_path=self.get_healers_dir(),
                remove_extensions=False,
                include_dirs=True,
            ).keys()
        )

    def set_healerunits_empty_if_null(self):
        if self._healerunits is None:
            self._healerunits = {}

    def create_new_healerunit(self, healer_title: str):
        self.set_healerunits_empty_if_null()
        ux = healerunit_shop(healer_title, self.get_object_root_dir(), self.handle)
        ux.create_core_dir_and_files()
        self._healerunits[ux._admin._healer_title] = ux

    def get_healer_obj(self, title: str) -> HealerUnit:
        return (
            None if self._healerunits.get(title) is None else self._healerunits[title]
        )

    def create_healerunit_from_public(self, title: str):
        cx = self.get_public_pact(healer=title)
        healer_x = healerunit_shop(title=cx._healer, env_dir=self.get_object_root_dir())
        self.set_healerunits_empty_if_null()
        self.set_healerunit_to_cure(healer_x)

    def set_healerunit_to_cure(self, healer: HealerUnit):
        self._healerunits[healer._admin._healer_title] = healer
        self.save_healer_file(healer_title=healer._admin._healer_title)

    def save_healer_file(self, healer_title: str):
        healer_x = self.get_healer_obj(title=healer_title)
        healer_x._admin.save_isol_pact(healer_x.get_isol())

    def rename_healerunit(self, old_title: str, new_title: str):
        healer_x = self.get_healer_obj(title=old_title)
        old_healer_dir = healer_x._admin._healer_dir
        healer_x._admin.set_healer_title(new_title=new_title)
        self.set_healerunit_to_cure(healer=healer_x)
        x_func_delete_dir(old_healer_dir)
        self.del_healer_from_cure(healer_title=old_title)

    def del_healer_from_cure(self, healer_title):
        self._healerunits.pop(healer_title)

    def del_healer_dir(self, healer_title: str):
        x_func_delete_dir(f"{self.get_healers_dir()}/{healer_title}")

    # public dir management
    def get_public_dir(self):
        return f"{self.get_object_root_dir()}/pacts"

    def get_ignores_dir(self, healer_title: str):
        per_x = self.get_healer_obj(healer_title)
        return per_x._admin._pacts_ignore_dir

    def get_public_pact(self, healer: str) -> ContractUnit:
        return get_pact_from_json(
            x_func_open_file(
                dest_dir=self.get_public_dir(), file_title=f"{healer}.json"
            )
        )

    def get_pact_from_ignores_dir(
        self, healer_title: str, _healer: str
    ) -> ContractUnit:
        return get_pact_from_json(
            x_func_open_file(
                dest_dir=self.get_ignores_dir(healer_title=healer_title),
                file_title=f"{_healer}.json",
            )
        )

    def set_ignore_pact_file(self, healer_title: str, pact_obj: ContractUnit):
        healer_x = self.get_healer_obj(title=healer_title)
        healer_x.set_ignore_pact_file(
            pactunit=pact_obj, src_pact_healer=pact_obj._healer
        )

    def rename_public_pact(self, old_healer: str, new_healer: str):
        pact_x = self.get_public_pact(healer=old_healer)
        pact_x.set_healer(new_healer=new_healer)
        self.save_public_pact(pact_x=pact_x)
        self.del_public_pact(pact_x_healer=old_healer)

    def del_public_pact(self, pact_x_healer: str):
        x_func_delete_dir(f"{self.get_public_dir()}/{pact_x_healer}.json")

    def save_public_pact(self, pact_x: ContractUnit):
        pact_x.set_cure_handle(cure_handle=self.handle)
        x_func_save_file(
            dest_dir=self.get_public_dir(),
            file_title=f"{pact_x._healer}.json",
            file_text=pact_x.get_json(),
        )

    def reload_all_healers_src_pactunits(self):
        for healer_x in self._healerunits.values():
            healer_x.refresh_depot_pacts()

    def get_public_dir_file_titles_list(self):
        return list(x_func_dir_files(dir_path=self.get_public_dir()).keys())

    # pacts_dir to healer_pacts_dir management
    def _healer_set_depot_pact(
        self,
        healerunit: HealerUnit,
        pactunit: ContractUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_pact: ContractUnit = None,
    ):
        healerunit.set_depot_pact(
            pact_x=pactunit,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )
        if depotlink_type == "ignore" and ignore_pact != None:
            healerunit.set_ignore_pact_file(
                pactunit=ignore_pact, src_pact_healer=pactunit._healer
            )

    def set_healer_depotlink(
        self,
        healer_title: str,
        pact_healer: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_pact: ContractUnit = None,
    ):
        healer_x = self.get_healer_obj(title=healer_title)
        pact_x = self.get_public_pact(healer=pact_healer)
        self._healer_set_depot_pact(
            healerunit=healer_x,
            pactunit=pact_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
            ignore_pact=ignore_pact,
        )

    def create_depotlink_to_generated_pact(
        self,
        healer_title: str,
        pact_healer: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        healer_x = self.get_healer_obj(title=healer_title)
        pact_x = ContractUnit(_healer=pact_healer)
        self._healer_set_depot_pact(
            healerunit=healer_x,
            pactunit=pact_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def update_depotlink(
        self,
        healer_title: str,
        partytitle: PartyTitle,
        depotlink_type: str,
        creditor_weight: str,
        debtor_weight: str,
    ):
        healer_x = self.get_healer_obj(title=healer_title)
        pact_x = self.get_public_pact(_healer=partytitle)
        self._healer_set_depot_pact(
            healerunit=healer_x,
            pactunit=pact_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def del_depotlink(self, healer_title: str, pactunit_healer: str):
        healer_x = self.get_healer_obj(title=healer_title)
        healer_x.del_depot_pact(pact_healer=pactunit_healer)

    # Healer output_pact
    def get_output_pact(self, healer_title: str) -> ContractUnit:
        healer_x = self.get_healer_obj(title=healer_title)
        return healer_x._admin.get_remelded_output_pact()


def cureunit_shop(
    handle: str,
    cures_dir: str,
    _healerunits: dict[str:HealerUnit] = None,
    in_memory_bank: bool = None,
):
    if in_memory_bank is None:
        in_memory_bank = True
    cure_x = CureUnit(handle=handle, cures_dir=cures_dir, _healerunits=_healerunits)
    cure_x.create_dirs_if_null(in_memory_bank=in_memory_bank)
    return cure_x
