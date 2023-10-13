from src.contract.contract import (
    get_from_json as contractunit_get_from_json,
    get_dict_of_contract_from_dict,
    get_meld_of_contract_files,
    ContractOwner,
    ContractUnit,
    partyunit_shop,
    get_from_json as contractunit_get_from_json,
    PartyTitle,
)
from src.contract.x_func import (
    x_get_json,
    single_dir_create_if_null,
    rename_dir,
    save_file as x_func_save_file,
    dir_files as x_func_dir_files,
    open_file as x_func_open_file,
    delete_dir as x_func_delete_dir,
)
from dataclasses import dataclass
from os import path as os_path
from json import loads as json_loads


class InvalidOwnerException(Exception):
    pass


@dataclass
class OwnerAdmin:
    _owner_title: str
    _env_dir: str
    _goal_tag: str
    _owner_dir: str = None
    _owners_dir: str = None
    _isol_file_title: str = None
    _isol_file_path: str = None
    _contract_output_file_title: str = None
    _contract_output_file_path: str = None
    _public_file_title: str = None
    _contracts_public_dir: str = None
    _contracts_depot_dir: str = None
    _contracts_ignore_dir: str = None
    _contracts_bond_dir: str = None
    _contracts_digest_dir: str = None

    def set_dirs(self):
        env_owners_dir_title = "owners"
        contracts_str = "contracts"
        self._owners_dir = f"{self._env_dir}/{env_owners_dir_title}"
        self._owner_dir = f"{self._owners_dir}/{self._owner_title}"
        self._isol_file_title = "isol_contract.json"
        self._isol_file_path = f"{self._owner_dir}/{self._isol_file_title}"
        self._contract_output_file_title = "output_contract.json"
        self._contract_output_file_path = (
            f"{self._owner_dir}/{self._contract_output_file_title}"
        )
        self._public_file_title = f"{self._owner_title}.json"
        self._contracts_public_dir = f"{self._env_dir}/{contracts_str}"
        self._contracts_depot_dir = f"{self._owner_dir}/{contracts_str}"
        self._contracts_ignore_dir = f"{self._owner_dir}/ignores"
        self._contracts_bond_dir = f"{self._owner_dir}/bonds"
        self._contracts_digest_dir = f"{self._owner_dir}/digests"

    def set_owner_title(self, new_title: str):
        old_owner_dir = self._owner_dir
        self._owner_title = new_title
        self.set_dirs()

        rename_dir(src=old_owner_dir, dst=self._owner_dir)

    def create_core_dir_and_files(self, isol_cx: ContractUnit = None):
        single_dir_create_if_null(x_path=self._owner_dir)
        single_dir_create_if_null(x_path=self._contracts_public_dir)
        single_dir_create_if_null(x_path=self._contracts_depot_dir)
        single_dir_create_if_null(x_path=self._contracts_digest_dir)
        single_dir_create_if_null(x_path=self._contracts_ignore_dir)
        single_dir_create_if_null(x_path=self._contracts_bond_dir)
        if isol_cx is None and self._isol_contract_exists() == False:
            self.save_isol_contract(self._get_empty_isol_contract())
        elif isol_cx != None and self._isol_contract_exists() == False:
            self.save_isol_contract(isol_cx)

    def _save_contract_to_path(
        self, contract_x: ContractUnit, dest_dir: str, file_title: str = None
    ):
        if file_title is None:
            file_title = f"{contract_x._owner}.json"
        # if dest_dir == self._contracts_public_dir:
        #     file_title = self._public_file_title
        x_func_save_file(
            dest_dir=dest_dir,
            file_title=file_title,
            file_text=contract_x.get_json(),
            replace=True,
        )

    def save_contract_to_public(self, contract_x: ContractUnit):
        dest_dir = self._contracts_public_dir
        self._save_contract_to_path(contract_x, dest_dir)

    def save_ignore_contract(self, contract_x: ContractUnit, src_contract_owner: str):
        dest_dir = self._contracts_ignore_dir
        file_title = None
        if src_contract_owner != None:
            file_title = f"{src_contract_owner}.json"
        else:
            file_title = f"{contract_x._owner}.json"
        self._save_contract_to_path(contract_x, dest_dir, file_title)

    def save_contract_to_digest(
        self, contract_x: ContractUnit, src_contract_owner: str = None
    ):
        dest_dir = self._contracts_digest_dir
        file_title = None
        if src_contract_owner != None:
            file_title = f"{src_contract_owner}.json"
        else:
            file_title = f"{contract_x._owner}.json"
        self._save_contract_to_path(contract_x, dest_dir, file_title)

    def save_isol_contract(self, contract_x: ContractUnit):
        contract_x.set_owner(self._owner_title)
        self._save_contract_to_path(contract_x, self._owner_dir, self._isol_file_title)

    def save_contract_to_depot(self, contract_x: ContractUnit):
        dest_dir = self._contracts_depot_dir
        self._save_contract_to_path(contract_x, dest_dir)

    def save_output_contract(self) -> ContractUnit:
        isol_contract_x = self.open_isol_contract()
        isol_contract_x.meld(isol_contract_x, party_weight=1)
        contract_x = get_meld_of_contract_files(
            cx_primary=isol_contract_x,
            meldees_dir=self._contracts_digest_dir,
        )
        dest_dir = self._owner_dir
        file_title = self._contract_output_file_title
        self._save_contract_to_path(contract_x, dest_dir, file_title)

    def open_public_contract(self, owner: ContractOwner) -> str:
        file_title_x = f"{owner}.json"
        return x_func_open_file(self._contracts_public_dir, file_title_x)

    def open_depot_contract(self, owner: ContractOwner) -> ContractUnit:
        file_title_x = f"{owner}.json"
        cx_json = x_func_open_file(self._contracts_depot_dir, file_title_x)
        return contractunit_get_from_json(cx_json=cx_json)

    def open_ignore_contract(self, owner: ContractOwner) -> ContractUnit:
        ignore_file_title = f"{owner}.json"
        contract_json = x_func_open_file(self._contracts_ignore_dir, ignore_file_title)
        contract_obj = contractunit_get_from_json(cx_json=contract_json)
        contract_obj.set_contract_metrics()
        return contract_obj

    def open_isol_contract(self) -> ContractUnit:
        cx = None
        if not self._isol_contract_exists():
            self.save_isol_contract(self._get_empty_isol_contract())
        ct = x_func_open_file(self._owner_dir, self._isol_file_title)
        cx = contractunit_get_from_json(cx_json=ct)
        cx.set_contract_metrics()
        return cx

    def open_output_contract(self) -> ContractUnit:
        cx_json = x_func_open_file(self._owner_dir, self._contract_output_file_title)
        cx_obj = contractunit_get_from_json(cx_json)
        cx_obj.set_contract_metrics()
        return cx_obj

    def _get_empty_isol_contract(self):
        cx = ContractUnit(_owner=self._owner_title, _weight=0)
        cx.add_partyunit(title=self._owner_title)
        cx.set_goal_tag(self._goal_tag)
        return cx

    def erase_depot_contract(self, owner):
        x_func_delete_dir(f"{self._contracts_depot_dir}/{owner}.json")

    def erase_digest_contract(self, owner):
        x_func_delete_dir(f"{self._contracts_digest_dir}/{owner}.json")

    def erase_isol_contract_file(self):
        x_func_delete_dir(dir=f"{self._owner_dir}/{self._isol_file_title}")

    def raise_exception_if_no_file(self, dir_type: str, owner: str):
        cx_file_title = f"{owner}.json"
        if dir_type == "depot":
            cx_file_path = f"{self._contracts_depot_dir}/{cx_file_title}"
        if not os_path.exists(cx_file_path):
            raise InvalidOwnerException(
                f"Owner {self._owner_title} cannot find contract {owner} in {cx_file_path}"
            )

    def _isol_contract_exists(self):
        bool_x = None
        try:
            x_func_open_file(self._owner_dir, self._isol_file_title)
            bool_x = True
        except Exception:
            bool_x = False
        return bool_x

    def get_remelded_output_contract(self):
        self.save_output_contract()
        return self.open_output_contract()

    def save_refreshed_output_to_public(self):
        self.save_contract_to_public(self.get_remelded_output_contract())


def owneradmin_shop(_owner_title: str, _env_dir: str, _goal_tag: str) -> OwnerAdmin:
    uax = OwnerAdmin(_owner_title=_owner_title, _env_dir=_env_dir, _goal_tag=_goal_tag)
    uax.set_dirs()
    return uax


@dataclass
class OwnerUnit:
    _admin: OwnerAdmin = None
    _isol: ContractUnit = None

    def refresh_depot_contracts(self):
        for party_x in self._isol._partys.values():
            if party_x.title != self._admin._owner_title:
                party_contract = contractunit_get_from_json(
                    cx_json=self._admin.open_public_contract(party_x.title)
                )
                self.set_depot_contract(
                    contract_x=party_contract,
                    depotlink_type=party_x.depotlink_type,
                    creditor_weight=party_x.creditor_weight,
                    debtor_weight=party_x.debtor_weight,
                )

    def set_depot_contract(
        self,
        contract_x: ContractUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        self.set_isol_if_empty()
        self._admin.save_contract_to_depot(contract_x)
        self._set_depotlink(
            contract_x._owner, depotlink_type, creditor_weight, debtor_weight
        )
        if self.get_isol()._auto_output_to_public:
            self._admin.save_refreshed_output_to_public()

    def _set_depotlinks_empty_if_null(self):
        self.set_isol_if_empty()
        self._isol.set_partys_empty_if_null()

    def _set_depotlink(
        self,
        outer_owner: str,
        link_type: str = None,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        self._admin.raise_exception_if_no_file("depot", outer_owner)
        self._set_partyunit_depotlink(
            outer_owner, link_type, creditor_weight, debtor_weight
        )

        if link_type == "assignment":
            self._set_assignment_depotlink(outer_owner)
        elif link_type == "blind_trust":
            cx_obj = self._admin.open_depot_contract(owner=outer_owner)
            self._admin.save_contract_to_digest(cx_obj)
        elif link_type == "ignore":
            new_cx_obj = ContractUnit(_owner=outer_owner)
            new_cx_obj.set_goal_tag(self._admin._goal_tag)
            self.set_ignore_contract_file(new_cx_obj, new_cx_obj._owner)

    def _set_assignment_depotlink(self, outer_owner):
        src_cx = self._admin.open_depot_contract(outer_owner)
        src_cx.set_contract_metrics()
        empty_cx = ContractUnit(_owner=self._admin._owner_title)
        empty_cx.set_goal_tag(self._admin._goal_tag)
        assign_cx = src_cx.get_assignment(
            empty_cx, self.get_isol()._partys, self._admin._owner_title
        )
        assign_cx.set_contract_metrics()
        self._admin.save_contract_to_digest(assign_cx, src_cx._owner)

    def _set_partyunit_depotlink(
        self,
        title: PartyTitle,
        link_type: str = None,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        party_x = self.get_isol().get_party(title)
        if party_x is None:
            self.get_isol().set_partyunit(
                partyunit_shop(
                    title=title,
                    depotlink_type=link_type,
                    creditor_weight=creditor_weight,
                    debtor_weight=debtor_weight,
                )
            )
        else:
            party_x.set_depotlink_type(link_type, creditor_weight, debtor_weight)

    def del_depot_contract(self, contract_owner: str):
        self._del_depotlink(partytitle=contract_owner)
        self._admin.erase_depot_contract(contract_owner)
        self._admin.erase_digest_contract(contract_owner)

    def _del_depotlink(self, partytitle: PartyTitle):
        self._isol.get_party(partytitle).del_depotlink_type()

    def get_isol(self):
        if self._isol is None:
            self._isol = self._admin.open_isol_contract()
        return self._isol

    def set_isol(self, contract_x: ContractUnit = None):
        if contract_x != None:
            self._isol = contract_x
        self._admin.save_isol_contract(self._isol)
        self._isol = None

    def set_isol_if_empty(self):
        # if self._isol is None:
        self.get_isol()

    def set_ignore_contract_file(
        self, contractunit: ContractUnit, src_contract_owner: str
    ):
        self._admin.save_ignore_contract(contractunit, src_contract_owner)
        self._admin.save_contract_to_digest(contractunit, src_contract_owner)

    # housekeeping
    def set_env_dir(self, env_dir: str, owner_title: str, goal_tag: str):
        self._admin = owneradmin_shop(
            _owner_title=owner_title, _env_dir=env_dir, _goal_tag=goal_tag
        )

    def create_core_dir_and_files(self, isol_cx: ContractUnit = None):
        self._admin.create_core_dir_and_files(isol_cx)


def ownerunit_shop(
    title: str, env_dir: str, goal_tag: str, _auto_output_to_public: bool = None
) -> OwnerUnit:
    owner_x = OwnerUnit()
    owner_x.set_env_dir(env_dir, title, goal_tag=goal_tag)
    owner_x.get_isol()
    owner_x._isol._set_auto_output_to_public(_auto_output_to_public)
    owner_x.set_isol()
    return owner_x
