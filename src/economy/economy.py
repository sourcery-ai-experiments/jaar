from src.contract.contract import (
    ContractUnit,
    get_from_json as get_contract_from_json,
    partylink_shop,
    PartyTitle,
)
from src.contract.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from src.economy.owner import OwnerUnit, ownerunit_shop
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection
from src.economy.bank_sqlstr import (
    get_river_flow_table_delete_sqlstr,
    get_river_flow_table_insert_sqlstr,
    get_river_tparty_table_delete_sqlstr,
    get_river_tparty_table_insert_sqlstr,
    get_river_tparty_dict,
    get_river_bucket_table_insert_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
    get_ledger_table_insert_sqlstr,
    get_contract_table_insert_sqlstr,
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


class EconomyTag(str):
    pass


@dataclass
class EconomyUnit:
    tag: EconomyTag
    economys_dir: str
    _ownerunits: dict[str:OwnerUnit] = None
    _bank_db = None

    def set_contract_bank_attrs(self, contract_owner: str):
        contract_obj = self.get_public_contract(contract_owner)

        for groupunit_x in contract_obj._groups.values():
            if groupunit_x._partylinks_set_by_economy_road != None:
                groupunit_x.clear_partylinks()
                ic = get_idea_catalog_dict(
                    self.get_bank_conn(), groupunit_x._partylinks_set_by_economy_road
                )
                for idea_catalog in ic.values():
                    if contract_owner != idea_catalog.contract_owner:
                        partylink_x = partylink_shop(title=idea_catalog.contract_owner)
                        groupunit_x.set_partylink(partylink_x)
        self.save_public_contract(contract_obj)

        # refresh bank metrics
        self.refresh_bank_metrics()

    # banking
    def set_river_sphere_for_contract(
        self, contract_owner: str, max_flows_count: int = None
    ):
        self._clear_all_source_river_data(contract_owner)
        general_bucket = [self._get_root_river_ledger_unit(contract_owner)]

        if max_flows_count is None:
            max_flows_count = 40

        flows_count = 0
        while flows_count < max_flows_count and general_bucket != []:
            parent_contract_ledger = general_bucket.pop(0)

            parent_range = parent_contract_ledger.get_range()
            parent_close = parent_contract_ledger.currency_cease
            curr_onset = parent_contract_ledger.currency_onset

            ledgers_len = len(parent_contract_ledger._ledgers.values())
            ledgers_count = 0
            for led_x in parent_contract_ledger._ledgers.values():
                ledgers_count += 1

                curr_range = parent_range * led_x._contract_agenda_ratio_credit
                curr_close = curr_onset + curr_range

                # implies last element in dict
                if ledgers_count == ledgers_len and curr_close != parent_close:
                    curr_close = parent_close

                river_flow_x = RiverFlowUnit(
                    currency_contract_owner=contract_owner,
                    src_title=led_x.contract_owner,
                    dst_title=led_x.party_title,
                    currency_start=curr_onset,
                    currency_close=curr_close,
                    flow_num=flows_count,
                    parent_flow_num=parent_contract_ledger.flow_num,
                    river_tree_level=parent_contract_ledger.river_tree_level + 1,
                )
                river_ledger_x = self._insert_river_flow_grab_river_ledger(river_flow_x)
                if river_ledger_x != None:
                    general_bucket.append(river_ledger_x)

                flows_count += 1
                if flows_count >= max_flows_count:
                    break

                # change curr_onset for next
                curr_onset += curr_range

        self._set_river_tpartys_buckets(contract_owner)

    def _insert_river_flow_grab_river_ledger(
        self, river_flow_x: RiverFlowUnit
    ) -> RiverLedgerUnit:
        river_ledger_x = None

        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_flow_table_insert_sqlstr(river_flow_x))

            if river_flow_x.flow_returned() == False:
                river_ledger_x = get_river_ledger_unit(bank_conn, river_flow_x)

        return river_ledger_x

    def _clear_all_source_river_data(self, contract_owner: str):
        with self.get_bank_conn() as bank_conn:
            flow_s = get_river_flow_table_delete_sqlstr(contract_owner)
            mstr_s = get_river_tparty_table_delete_sqlstr(contract_owner)
            bank_conn.execute(flow_s)
            bank_conn.execute(mstr_s)

    def _get_root_river_ledger_unit(self, contract_owner: str) -> RiverLedgerUnit:
        default_currency_onset = 0.0
        default_currency_cease = 1.0
        default_root_river_tree_level = 0
        default_root_flow_num = None  # maybe change to 1?
        default_root_parent_flow_num = None
        root_river_flow = RiverFlowUnit(
            currency_contract_owner=contract_owner,
            src_title=None,
            dst_title=contract_owner,
            currency_start=default_currency_onset,
            currency_close=default_currency_cease,
            flow_num=default_root_flow_num,
            parent_flow_num=default_root_parent_flow_num,
            river_tree_level=default_root_river_tree_level,
        )
        with self.get_bank_conn() as bank_conn:
            source_river_ledger = get_river_ledger_unit(bank_conn, root_river_flow)
        return source_river_ledger

    def _set_river_tpartys_buckets(self, contract_owner: str):
        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_tparty_table_insert_sqlstr(contract_owner))
            bank_conn.execute(get_river_bucket_table_insert_sqlstr(contract_owner))

            sal_river_tpartys = get_river_tparty_dict(bank_conn, contract_owner)
            contract_x = self.get_public_contract(owner=contract_owner)
            contract_x.set_banking_attr_partyunits(sal_river_tpartys)
            self.save_public_contract(contract_x=contract_x)

    def get_river_tpartys(self, contract_owner: str) -> dict[str:RiverTpartyUnit]:
        with self.get_bank_conn() as bank_conn:
            river_tpartys = get_river_tparty_dict(bank_conn, contract_owner)
        return river_tpartys

    def refresh_bank_metrics(self, in_memory: bool = None):
        if in_memory is None and self._bank_db != None:
            in_memory = True
        self._create_bank_db(in_memory=in_memory, overwrite=True)
        self._bank_populate_contracts_data()

    def _bank_populate_contracts_data(self):
        for file_title in self.get_public_dir_file_titles_list():
            contract_json = x_func_open_file(self.get_public_dir(), file_title)
            contractunit_x = get_contract_from_json(cx_json=contract_json)
            contractunit_x.set_contract_metrics()

            self._bank_insert_contractunit(contractunit_x)
            self._bank_insert_partyunit(contractunit_x)
            self._bank_insert_groupunit(contractunit_x)
            self._bank_insert_ideaunit(contractunit_x)
            self._bank_insert_acptfact(contractunit_x)

    def _bank_insert_contractunit(self, contractunit_x: ContractUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            cur.execute(get_contract_table_insert_sqlstr(contract_x=contractunit_x))

    def _bank_insert_partyunit(self, contractunit_x: ContractUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for partyunit_x in contractunit_x._partys.values():
                sqlstr = get_ledger_table_insert_sqlstr(contractunit_x, partyunit_x)
                cur.execute(sqlstr)

    def _bank_insert_groupunit(self, contractunit_x: ContractUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for groupunit_x in contractunit_x._groups.values():
                groupunit_catalog_x = GroupUnitCatalog(
                    contract_owner=contractunit_x._owner,
                    groupunit_brand=groupunit_x.brand,
                    partylinks_set_by_economy_road=groupunit_x._partylinks_set_by_economy_road,
                )
                sqlstr = get_groupunit_catalog_table_insert_sqlstr(groupunit_catalog_x)
                cur.execute(sqlstr)

    def _bank_insert_ideaunit(self, contractunit_x: ContractUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for idea_x in contractunit_x._idea_dict.values():
                idea_catalog_x = IdeaCatalog(contractunit_x._owner, idea_x.get_road())
                sqlstr = get_idea_catalog_table_insert_sqlstr(idea_catalog_x)
                cur.execute(sqlstr)

    def _bank_insert_acptfact(self, contractunit_x: ContractUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for acptfact_x in contractunit_x._idearoot._acptfactunits.values():
                acptfact_catalog_x = AcptFactCatalog(
                    contract_owner=contractunit_x._owner,
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

    def set_economyunit_tag(self, tag: str):
        self.tag = tag

    def get_bank_db_path(self):
        return f"{self.get_object_root_dir()}/bank.db"

    def get_object_root_dir(self):
        return f"{self.economys_dir}/{self.tag}"

    def _create_main_file_if_null(self, x_dir):
        economy_file_title = "economy.json"
        x_func_save_file(
            dest_dir=x_dir,
            file_title=economy_file_title,
            file_text="",
        )

    def create_dirs_if_null(self, in_memory_bank: bool = None):
        economy_dir = self.get_object_root_dir()
        contracts_dir = self.get_public_dir()
        owners_dir = self.get_owners_dir()
        single_dir_create_if_null(x_path=economy_dir)
        single_dir_create_if_null(x_path=contracts_dir)
        single_dir_create_if_null(x_path=owners_dir)
        self._create_main_file_if_null(x_dir=economy_dir)
        self._create_bank_db(in_memory=in_memory_bank, overwrite=True)

    # OwnerUnit management
    def get_owners_dir(self):
        return f"{self.get_object_root_dir()}/owners"

    def get_owner_dir_paths_list(self):
        return list(
            x_func_dir_files(
                dir_path=self.get_owners_dir(),
                remove_extensions=False,
                include_dirs=True,
            ).keys()
        )

    def set_ownerunits_empty_if_null(self):
        if self._ownerunits is None:
            self._ownerunits = {}

    def create_new_ownerunit(self, owner_title: str):
        self.set_ownerunits_empty_if_null()
        print(f"{self.tag=}")
        ux = ownerunit_shop(owner_title, self.get_object_root_dir(), self.tag)
        ux.create_core_dir_and_files()
        self._ownerunits[ux._admin._owner_title] = ux

    def get_owner_obj(self, title: str) -> OwnerUnit:
        return None if self._ownerunits.get(title) is None else self._ownerunits[title]

    def create_ownerunit_from_public(self, title: str):
        cx = self.get_public_contract(owner=title)
        owner_x = ownerunit_shop(title=cx._owner, env_dir=self.get_object_root_dir())
        self.set_ownerunits_empty_if_null()
        self.set_ownerunit_to_economy(owner_x)

    def set_ownerunit_to_economy(self, owner: OwnerUnit):
        self._ownerunits[owner._admin._owner_title] = owner
        self.save_owner_file(owner_title=owner._admin._owner_title)

    def save_owner_file(self, owner_title: str):
        owner_x = self.get_owner_obj(title=owner_title)
        owner_x._admin.save_isol_contract(owner_x.get_isol())

    def rename_ownerunit(self, old_title: str, new_title: str):
        owner_x = self.get_owner_obj(title=old_title)
        old_owner_dir = owner_x._admin._owner_dir
        owner_x._admin.set_owner_title(new_title=new_title)
        self.set_ownerunit_to_economy(owner=owner_x)
        x_func_delete_dir(old_owner_dir)
        self.del_owner_from_economy(owner_title=old_title)

    def del_owner_from_economy(self, owner_title):
        self._ownerunits.pop(owner_title)

    def del_owner_dir(self, owner_title: str):
        x_func_delete_dir(f"{self.get_owners_dir()}/{owner_title}")

    # public dir management
    def get_public_dir(self):
        return f"{self.get_object_root_dir()}/contracts"

    def get_ignores_dir(self, owner_title: str):
        per_x = self.get_owner_obj(owner_title)
        return per_x._admin._contracts_ignore_dir

    def get_public_contract(self, owner: str) -> ContractUnit:
        return get_contract_from_json(
            x_func_open_file(dest_dir=self.get_public_dir(), file_title=f"{owner}.json")
        )

    def get_contract_from_ignores_dir(
        self, owner_title: str, _owner: str
    ) -> ContractUnit:
        return get_contract_from_json(
            x_func_open_file(
                dest_dir=self.get_ignores_dir(owner_title=owner_title),
                file_title=f"{_owner}.json",
            )
        )

    def set_ignore_contract_file(self, owner_title: str, contract_obj: ContractUnit):
        owner_x = self.get_owner_obj(title=owner_title)
        owner_x.set_ignore_contract_file(
            contractunit=contract_obj, src_contract_owner=contract_obj._owner
        )

    def rename_public_contract(self, old_owner: str, new_owner: str):
        contract_x = self.get_public_contract(owner=old_owner)
        contract_x.set_owner(new_owner=new_owner)
        self.save_public_contract(contract_x=contract_x)
        self.del_public_contract(contract_x_owner=old_owner)

    def del_public_contract(self, contract_x_owner: str):
        x_func_delete_dir(f"{self.get_public_dir()}/{contract_x_owner}.json")

    def save_public_contract(self, contract_x: ContractUnit):
        contract_x.set_economy_tag(economy_tag=self.tag)
        x_func_save_file(
            dest_dir=self.get_public_dir(),
            file_title=f"{contract_x._owner}.json",
            file_text=contract_x.get_json(),
        )

    def reload_all_owners_src_contractunits(self):
        for owner_x in self._ownerunits.values():
            owner_x.refresh_depot_contracts()

    def get_public_dir_file_titles_list(self):
        return list(x_func_dir_files(dir_path=self.get_public_dir()).keys())

    # contracts_dir to owner_contracts_dir management
    def _owner_set_depot_contract(
        self,
        ownerunit: OwnerUnit,
        contractunit: ContractUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_contract: ContractUnit = None,
    ):
        ownerunit.set_depot_contract(
            contract_x=contractunit,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )
        if depotlink_type == "ignore" and ignore_contract != None:
            ownerunit.set_ignore_contract_file(
                contractunit=ignore_contract, src_contract_owner=contractunit._owner
            )

    def set_owner_depotlink(
        self,
        owner_title: str,
        contract_owner: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_contract: ContractUnit = None,
    ):
        owner_x = self.get_owner_obj(title=owner_title)
        contract_x = self.get_public_contract(owner=contract_owner)
        self._owner_set_depot_contract(
            ownerunit=owner_x,
            contractunit=contract_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
            ignore_contract=ignore_contract,
        )

    def create_depotlink_to_generated_contract(
        self,
        owner_title: str,
        contract_owner: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        owner_x = self.get_owner_obj(title=owner_title)
        contract_x = ContractUnit(_owner=contract_owner)
        self._owner_set_depot_contract(
            ownerunit=owner_x,
            contractunit=contract_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def update_depotlink(
        self,
        owner_title: str,
        partytitle: PartyTitle,
        depotlink_type: str,
        creditor_weight: str,
        debtor_weight: str,
    ):
        owner_x = self.get_owner_obj(title=owner_title)
        contract_x = self.get_public_contract(_owner=partytitle)
        self._owner_set_depot_contract(
            ownerunit=owner_x,
            contractunit=contract_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def del_depotlink(self, owner_title: str, contractunit_owner: str):
        owner_x = self.get_owner_obj(title=owner_title)
        owner_x.del_depot_contract(contract_owner=contractunit_owner)

    # Owner output_contract
    def get_output_contract(self, owner_title: str) -> ContractUnit:
        owner_x = self.get_owner_obj(title=owner_title)
        return owner_x._admin.get_remelded_output_contract()


def economyunit_shop(
    tag: str,
    economys_dir: str,
    _ownerunits: dict[str:OwnerUnit] = None,
    in_memory_bank: bool = None,
):
    if in_memory_bank is None:
        in_memory_bank = True
    economy_x = EconomyUnit(tag=tag, economys_dir=economys_dir, _ownerunits=_ownerunits)
    economy_x.create_dirs_if_null(in_memory_bank=in_memory_bank)
    return economy_x
