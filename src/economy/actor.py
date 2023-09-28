from src.contract.member import get_depotlink_types, memberunit_shop
from src.contract.contract import (
    get_from_json as contractunit_get_from_json,
    get_dict_of_contract_from_dict,
    get_meld_of_contract_files,
    ContractOwner,
)
from src.contract.idea import IdeaRoot
from src.contract.member import MemberName
from src.contract.contract import (
    ContractUnit,
    get_from_json as contractunit_get_from_json,
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


class InvalidActorException(Exception):
    pass


@dataclass
class ActorAdmin:
    _actor_name: str
    _env_dir: str
    _economy_title: str
    _actor_dir: str = None
    _actors_dir: str = None
    _isol_file_name: str = None
    _isol_file_path: str = None
    _contract_output_file_name: str = None
    _contract_output_file_path: str = None
    _public_file_name: str = None
    _contracts_public_dir: str = None
    _contracts_depot_dir: str = None
    _contracts_ignore_dir: str = None
    _contracts_bond_dir: str = None
    _contracts_digest_dir: str = None

    def set_dirs(self):
        env_actors_dir_name = "actors"
        contracts_str = "contracts"
        self._actors_dir = f"{self._env_dir}/{env_actors_dir_name}"
        self._actor_dir = f"{self._actors_dir}/{self._actor_name}"
        self._isol_file_name = "isol_contract.json"
        self._isol_file_path = f"{self._actor_dir}/{self._isol_file_name}"
        self._contract_output_file_name = "output_contract.json"
        self._contract_output_file_path = (
            f"{self._actor_dir}/{self._contract_output_file_name}"
        )
        self._public_file_name = f"{self._actor_name}.json"
        self._contracts_public_dir = f"{self._env_dir}/{contracts_str}"
        self._contracts_depot_dir = f"{self._actor_dir}/{contracts_str}"
        self._contracts_ignore_dir = f"{self._actor_dir}/ignores"
        self._contracts_bond_dir = f"{self._actor_dir}/bonds"
        self._contracts_digest_dir = f"{self._actor_dir}/digests"

    def set_actor_name(self, new_name: str):
        old_actor_dir = self._actor_dir
        self._actor_name = new_name
        self.set_dirs()

        rename_dir(src=old_actor_dir, dst=self._actor_dir)

    def create_core_dir_and_files(self, isol_cx: ContractUnit = None):
        single_dir_create_if_null(x_path=self._actor_dir)
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
        self, contract_x: ContractUnit, dest_dir: str, file_name: str = None
    ):
        if file_name is None:
            file_name = f"{contract_x._owner}.json"
        # if dest_dir == self._contracts_public_dir:
        #     file_name = self._public_file_name
        x_func_save_file(
            dest_dir=dest_dir,
            file_name=file_name,
            file_text=contract_x.get_json(),
            replace=True,
        )

    def save_contract_to_public(self, contract_x: ContractUnit):
        dest_dir = self._contracts_public_dir
        self._save_contract_to_path(contract_x, dest_dir)

    def save_ignore_contract(self, contract_x: ContractUnit, src_contract_owner: str):
        dest_dir = self._contracts_ignore_dir
        file_name = None
        if src_contract_owner != None:
            file_name = f"{src_contract_owner}.json"
        else:
            file_name = f"{contract_x._owner}.json"
        self._save_contract_to_path(contract_x, dest_dir, file_name)

    def save_contract_to_digest(
        self, contract_x: ContractUnit, src_contract_owner: str = None
    ):
        dest_dir = self._contracts_digest_dir
        file_name = None
        if src_contract_owner != None:
            file_name = f"{src_contract_owner}.json"
        else:
            file_name = f"{contract_x._owner}.json"
        self._save_contract_to_path(contract_x, dest_dir, file_name)

    def save_isol_contract(self, contract_x: ContractUnit):
        contract_x.set_owner(self._actor_name)
        self._save_contract_to_path(contract_x, self._actor_dir, self._isol_file_name)

    def save_contract_to_depot(self, contract_x: ContractUnit):
        dest_dir = self._contracts_depot_dir
        self._save_contract_to_path(contract_x, dest_dir)

    def save_output_contract(self) -> ContractUnit:
        isol_contract_x = self.open_isol_contract()
        isol_contract_x.meld(isol_contract_x, member_weight=1)
        contract_x = get_meld_of_contract_files(
            cx_primary=isol_contract_x,
            meldees_dir=self._contracts_digest_dir,
        )
        dest_dir = self._actor_dir
        file_name = self._contract_output_file_name
        self._save_contract_to_path(contract_x, dest_dir, file_name)

    def open_public_contract(self, owner: ContractOwner) -> str:
        file_name_x = f"{owner}.json"
        return x_func_open_file(self._contracts_public_dir, file_name_x)

    def open_depot_contract(self, owner: ContractOwner) -> ContractUnit:
        file_name_x = f"{owner}.json"
        cx_json = x_func_open_file(self._contracts_depot_dir, file_name_x)
        return contractunit_get_from_json(cx_json=cx_json)

    def open_ignore_contract(self, owner: ContractOwner) -> ContractUnit:
        ignore_file_name = f"{owner}.json"
        contract_json = x_func_open_file(self._contracts_ignore_dir, ignore_file_name)
        contract_obj = contractunit_get_from_json(cx_json=contract_json)
        contract_obj.set_contract_metrics()
        return contract_obj

    def open_isol_contract(self) -> ContractUnit:
        cx = None
        if not self._isol_contract_exists():
            self.save_isol_contract(self._get_empty_isol_contract())
        ct = x_func_open_file(self._actor_dir, self._isol_file_name)
        cx = contractunit_get_from_json(cx_json=ct)
        cx.set_contract_metrics()
        return cx

    def open_output_contract(self) -> ContractUnit:
        cx_json = x_func_open_file(self._actor_dir, self._contract_output_file_name)
        cx_obj = contractunit_get_from_json(cx_json)
        cx_obj.set_contract_metrics()
        return cx_obj

    def _get_empty_isol_contract(self):
        cx = ContractUnit(_owner=self._actor_name, _weight=0)
        cx.add_memberunit(name=self._actor_name)
        cx.set_economy_title(self._economy_title)
        return cx

    def erase_depot_contract(self, owner):
        x_func_delete_dir(f"{self._contracts_depot_dir}/{owner}.json")

    def erase_digest_contract(self, owner):
        x_func_delete_dir(f"{self._contracts_digest_dir}/{owner}.json")

    def erase_isol_contract_file(self):
        x_func_delete_dir(dir=f"{self._actor_dir}/{self._isol_file_name}")

    def raise_exception_if_no_file(self, dir_type: str, owner: str):
        cx_file_name = f"{owner}.json"
        if dir_type == "depot":
            cx_file_path = f"{self._contracts_depot_dir}/{cx_file_name}"
        if not os_path.exists(cx_file_path):
            raise InvalidActorException(
                f"Actor {self._actor_name} cannot find contract {owner} in {cx_file_path}"
            )

    def _isol_contract_exists(self):
        bool_x = None
        try:
            x_func_open_file(self._actor_dir, self._isol_file_name)
            bool_x = True
        except Exception:
            bool_x = False
        return bool_x

    def get_remelded_output_contract(self):
        self.save_output_contract()
        return self.open_output_contract()

    def save_refreshed_output_to_public(self):
        self.save_contract_to_public(self.get_remelded_output_contract())


def actoradmin_shop(_actor_name: str, _env_dir: str, _economy_title: str) -> ActorAdmin:
    uax = ActorAdmin(
        _actor_name=_actor_name, _env_dir=_env_dir, _economy_title=_economy_title
    )
    uax.set_dirs()
    return uax


@dataclass
class ActorUnit:
    _admin: ActorAdmin = None
    _isol: ContractUnit = None

    def refresh_depot_contracts(self):
        for member_x in self._isol._members.values():
            if member_x.name != self._admin._actor_name:
                member_contract = contractunit_get_from_json(
                    cx_json=self._admin.open_public_contract(member_x.name)
                )
                self.set_depot_contract(
                    contract_x=member_contract,
                    depotlink_type=member_x.depotlink_type,
                    creditor_weight=member_x.creditor_weight,
                    debtor_weight=member_x.debtor_weight,
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
        self._isol.set_members_empty_if_null()

    def _set_depotlink(
        self,
        outer_owner: str,
        link_type: str = None,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        self._admin.raise_exception_if_no_file("depot", outer_owner)
        self._set_memberunit_depotlink(
            outer_owner, link_type, creditor_weight, debtor_weight
        )

        if link_type == "assignment":
            self._set_assignment_depotlink(outer_owner)
        elif link_type == "blind_trust":
            cx_obj = self._admin.open_depot_contract(owner=outer_owner)
            self._admin.save_contract_to_digest(cx_obj)
        elif link_type == "ignore":
            new_cx_obj = ContractUnit(_owner=outer_owner)
            new_cx_obj.set_economy_title(self._admin._economy_title)
            self.set_ignore_contract_file(new_cx_obj, new_cx_obj._owner)

    def _set_assignment_depotlink(self, outer_owner):
        src_cx = self._admin.open_depot_contract(outer_owner)
        src_cx.set_contract_metrics()
        empty_cx = ContractUnit(_owner=self._admin._actor_name)
        empty_cx.set_economy_title(self._admin._economy_title)
        assign_cx = src_cx.get_assignment(
            empty_cx, self.get_isol()._members, self._admin._actor_name
        )
        assign_cx.set_contract_metrics()
        self._admin.save_contract_to_digest(assign_cx, src_cx._owner)

    def _set_memberunit_depotlink(
        self,
        name: MemberName,
        link_type: str = None,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        member_x = self.get_isol().get_member(name)
        if member_x is None:
            self.get_isol().set_memberunit(
                memberunit_shop(
                    name=name,
                    depotlink_type=link_type,
                    creditor_weight=creditor_weight,
                    debtor_weight=debtor_weight,
                )
            )
        else:
            member_x.set_depotlink_type(link_type, creditor_weight, debtor_weight)

    def del_depot_contract(self, contract_owner: str):
        self._del_depotlink(membername=contract_owner)
        self._admin.erase_depot_contract(contract_owner)
        self._admin.erase_digest_contract(contract_owner)

    def _del_depotlink(self, membername: MemberName):
        self._isol.get_member(membername).del_depotlink_type()

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
    def set_env_dir(self, env_dir: str, actor_name: str, economy_title: str):
        self._admin = actoradmin_shop(
            _actor_name=actor_name, _env_dir=env_dir, _economy_title=economy_title
        )

    def create_core_dir_and_files(self, isol_cx: ContractUnit = None):
        self._admin.create_core_dir_and_files(isol_cx)


def actorunit_shop(
    name: str, env_dir: str, economy_title: str, _auto_output_to_public: bool = None
) -> ActorUnit:
    actor_x = ActorUnit()
    actor_x.set_env_dir(env_dir, name, economy_title=economy_title)
    actor_x.get_isol()
    actor_x._isol._set_auto_output_to_public(_auto_output_to_public)
    actor_x.set_isol()
    return actor_x
