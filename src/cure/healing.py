from src.pact.pact import (
    get_from_json as pactunit_get_from_json,
    get_dict_of_pact_from_dict,
    get_meld_of_pact_files,
    PersonName,
    PactUnit,
    partyunit_shop,
    get_from_json as pactunit_get_from_json,
    PartyTitle,
)
from src.pact.x_func import (
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


class InvalidHealingException(Exception):
    pass


@dataclass
class HealingAdmin:
    _healing_title: str
    _env_dir: str
    _cure_handle: str
    _healingunit_dir: str = None
    _healingunits_dir: str = None
    _isol_file_title: str = None
    _isol_file_path: str = None
    _pact_output_file_title: str = None
    _pact_output_file_path: str = None
    _public_file_title: str = None
    _pacts_public_dir: str = None
    _pacts_depot_dir: str = None
    _pacts_ignore_dir: str = None
    _pacts_bond_dir: str = None
    _pacts_digest_dir: str = None

    def set_dirs(self):
        env_healingunits_folder = "healingunits"
        pacts_str = "pacts"
        self._healingunits_dir = f"{self._env_dir}/{env_healingunits_folder}"
        self._healingunit_dir = f"{self._healingunits_dir}/{self._healing_title}"
        self._isol_file_title = "isol_pact.json"
        self._isol_file_path = f"{self._healingunit_dir}/{self._isol_file_title}"
        self._pact_output_file_title = "output_pact.json"
        self._pact_output_file_path = (
            f"{self._healingunit_dir}/{self._pact_output_file_title}"
        )
        self._public_file_title = f"{self._healing_title}.json"
        self._pacts_public_dir = f"{self._env_dir}/{pacts_str}"
        self._pacts_depot_dir = f"{self._healingunit_dir}/{pacts_str}"
        self._pacts_ignore_dir = f"{self._healingunit_dir}/ignores"
        self._pacts_bond_dir = f"{self._healingunit_dir}/bonds"
        self._pacts_digest_dir = f"{self._healingunit_dir}/digests"

    def set_healing_title(self, new_title: str):
        old_healingunit_dir = self._healingunit_dir
        self._healing_title = new_title
        self.set_dirs()

        rename_dir(src=old_healingunit_dir, dst=self._healingunit_dir)

    def create_core_dir_and_files(self, isol_pact: PactUnit = None):
        single_dir_create_if_null(x_path=self._healingunit_dir)
        single_dir_create_if_null(x_path=self._pacts_public_dir)
        single_dir_create_if_null(x_path=self._pacts_depot_dir)
        single_dir_create_if_null(x_path=self._pacts_digest_dir)
        single_dir_create_if_null(x_path=self._pacts_ignore_dir)
        single_dir_create_if_null(x_path=self._pacts_bond_dir)
        if isol_pact is None and self._isol_pact_exists() == False:
            self.save_isol_pact(self._get_empty_isol_pact())
        elif isol_pact != None and self._isol_pact_exists() == False:
            self.save_isol_pact(isol_pact)

    def _save_pact_to_path(
        self, pact_x: PactUnit, dest_dir: str, file_title: str = None
    ):
        if file_title is None:
            file_title = f"{pact_x._healer}.json"
        # if dest_dir == self._pacts_public_dir:
        #     file_title = self._public_file_title
        x_func_save_file(
            dest_dir=dest_dir,
            file_title=file_title,
            file_text=pact_x.get_json(),
            replace=True,
        )

    def save_pact_to_public(self, pact_x: PactUnit):
        dest_dir = self._pacts_public_dir
        self._save_pact_to_path(pact_x, dest_dir)

    def save_ignore_pact(self, pact_x: PactUnit, src_pact_healer: str):
        dest_dir = self._pacts_ignore_dir
        file_title = None
        if src_pact_healer != None:
            file_title = f"{src_pact_healer}.json"
        else:
            file_title = f"{pact_x._healer}.json"
        self._save_pact_to_path(pact_x, dest_dir, file_title)

    def save_pact_to_digest(self, pact_x: PactUnit, src_pact_healer: str = None):
        dest_dir = self._pacts_digest_dir
        file_title = None
        if src_pact_healer != None:
            file_title = f"{src_pact_healer}.json"
        else:
            file_title = f"{pact_x._healer}.json"
        self._save_pact_to_path(pact_x, dest_dir, file_title)

    def save_isol_pact(self, pact_x: PactUnit):
        pact_x.set_healer(self._healing_title)
        self._save_pact_to_path(pact_x, self._healingunit_dir, self._isol_file_title)

    def save_pact_to_depot(self, pact_x: PactUnit):
        dest_dir = self._pacts_depot_dir
        self._save_pact_to_path(pact_x, dest_dir)

    def save_output_pact(self) -> PactUnit:
        isol_pact_x = self.open_isol_pact()
        isol_pact_x.meld(isol_pact_x, party_weight=1)
        pact_x = get_meld_of_pact_files(
            primary_pact=isol_pact_x,
            meldees_dir=self._pacts_digest_dir,
        )
        dest_dir = self._healingunit_dir
        file_title = self._pact_output_file_title
        self._save_pact_to_path(pact_x, dest_dir, file_title)

    def open_public_pact(self, healer: PersonName) -> str:
        file_title_x = f"{healer}.json"
        return x_func_open_file(self._pacts_public_dir, file_title_x)

    def open_depot_pact(self, healer: PersonName) -> PactUnit:
        file_title_x = f"{healer}.json"
        x_pact_json = x_func_open_file(self._pacts_depot_dir, file_title_x)
        return pactunit_get_from_json(x_pact_json=x_pact_json)

    def open_ignore_pact(self, healer: PersonName) -> PactUnit:
        ignore_file_title = f"{healer}.json"
        pact_json = x_func_open_file(self._pacts_ignore_dir, ignore_file_title)
        pact_obj = pactunit_get_from_json(x_pact_json=pact_json)
        pact_obj.set_pact_metrics()
        return pact_obj

    def open_isol_pact(self) -> PactUnit:
        x_pact = None
        if not self._isol_pact_exists():
            self.save_isol_pact(self._get_empty_isol_pact())
        ct = x_func_open_file(self._healingunit_dir, self._isol_file_title)
        x_pact = pactunit_get_from_json(x_pact_json=ct)
        x_pact.set_pact_metrics()
        return x_pact

    def open_output_pact(self) -> PactUnit:
        x_pact_json = x_func_open_file(
            self._healingunit_dir, self._pact_output_file_title
        )
        x_pact = pactunit_get_from_json(x_pact_json)
        x_pact.set_pact_metrics()
        return x_pact

    def _get_empty_isol_pact(self):
        x_pact = PactUnit(_healer=self._healing_title, _weight=0)
        x_pact.add_partyunit(title=self._healing_title)
        x_pact.set_cure_handle(self._cure_handle)
        return x_pact

    def erase_depot_pact(self, healer):
        x_func_delete_dir(f"{self._pacts_depot_dir}/{healer}.json")

    def erase_digest_pact(self, healer):
        x_func_delete_dir(f"{self._pacts_digest_dir}/{healer}.json")

    def erase_isol_pact_file(self):
        x_func_delete_dir(dir=f"{self._healingunit_dir}/{self._isol_file_title}")

    def raise_exception_if_no_file(self, dir_type: str, healer: str):
        x_pact_file_title = f"{healer}.json"
        if dir_type == "depot":
            x_pact_file_path = f"{self._pacts_depot_dir}/{x_pact_file_title}"
        if not os_path.exists(x_pact_file_path):
            raise InvalidHealingException(
                f"Healer {self._healing_title} cannot find pact {healer} in {x_pact_file_path}"
            )

    def _isol_pact_exists(self):
        bool_x = None
        try:
            x_func_open_file(self._healingunit_dir, self._isol_file_title)
            bool_x = True
        except Exception:
            bool_x = False
        return bool_x

    def get_remelded_output_pact(self):
        self.save_output_pact()
        return self.open_output_pact()

    def save_refreshed_output_to_public(self):
        self.save_pact_to_public(self.get_remelded_output_pact())


def healingadmin_shop(
    _healing_title: str, _env_dir: str, _cure_handle: str
) -> HealingAdmin:
    uax = HealingAdmin(
        _healing_title=_healing_title, _env_dir=_env_dir, _cure_handle=_cure_handle
    )
    uax.set_dirs()
    return uax


@dataclass
class HealingUnit:
    _admin: HealingAdmin = None
    _isol: PactUnit = None

    def refresh_depot_pacts(self):
        for party_x in self._isol._partys.values():
            if party_x.title != self._admin._healing_title:
                party_pact = pactunit_get_from_json(
                    x_pact_json=self._admin.open_public_pact(party_x.title)
                )
                self.set_depot_pact(
                    pact_x=party_pact,
                    depotlink_type=party_x.depotlink_type,
                    creditor_weight=party_x.creditor_weight,
                    debtor_weight=party_x.debtor_weight,
                )

    def set_depot_pact(
        self,
        pact_x: PactUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        self.set_isol_if_empty()
        self._admin.save_pact_to_depot(pact_x)
        self._set_depotlink(
            pact_x._healer, depotlink_type, creditor_weight, debtor_weight
        )
        if self.get_isol()._auto_output_to_public:
            self._admin.save_refreshed_output_to_public()

    def _set_depotlinks_empty_if_null(self):
        self.set_isol_if_empty()
        self._isol.set_partys_empty_if_null()

    def _set_depotlink(
        self,
        outer_healer: str,
        link_type: str = None,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        self._admin.raise_exception_if_no_file("depot", outer_healer)
        self._set_partyunit_depotlink(
            outer_healer, link_type, creditor_weight, debtor_weight
        )

        if link_type == "assignment":
            self._set_assignment_depotlink(outer_healer)
        elif link_type == "blind_trust":
            x_pact = self._admin.open_depot_pact(healer=outer_healer)
            self._admin.save_pact_to_digest(x_pact)
        elif link_type == "ignore":
            new_x_pact = PactUnit(_healer=outer_healer)
            new_x_pact.set_cure_handle(self._admin._cure_handle)
            self.set_ignore_pact_file(new_x_pact, new_x_pact._healer)

    def _set_assignment_depotlink(self, outer_healer):
        src_pact = self._admin.open_depot_pact(outer_healer)
        src_pact.set_pact_metrics()
        empty_pact = PactUnit(_healer=self._admin._healing_title)
        empty_pact.set_cure_handle(self._admin._cure_handle)
        assign_pact = src_pact.get_assignment(
            empty_pact, self.get_isol()._partys, self._admin._healing_title
        )
        assign_pact.set_pact_metrics()
        self._admin.save_pact_to_digest(assign_pact, src_pact._healer)

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

    def del_depot_pact(self, pact_healer: str):
        self._del_depotlink(partytitle=pact_healer)
        self._admin.erase_depot_pact(pact_healer)
        self._admin.erase_digest_pact(pact_healer)

    def _del_depotlink(self, partytitle: PartyTitle):
        self._isol.get_party(partytitle).del_depotlink_type()

    def get_isol(self):
        if self._isol is None:
            self._isol = self._admin.open_isol_pact()
        return self._isol

    def set_isol(self, pact_x: PactUnit = None):
        if pact_x != None:
            self._isol = pact_x
        self._admin.save_isol_pact(self._isol)
        self._isol = None

    def set_isol_if_empty(self):
        # if self._isol is None:
        self.get_isol()

    def set_ignore_pact_file(self, pactunit: PactUnit, src_pact_healer: str):
        self._admin.save_ignore_pact(pactunit, src_pact_healer)
        self._admin.save_pact_to_digest(pactunit, src_pact_healer)

    # housekeeping
    def set_env_dir(self, env_dir: str, healing_title: str, cure_handle: str):
        self._admin = healingadmin_shop(
            _healing_title=healing_title, _env_dir=env_dir, _cure_handle=cure_handle
        )

    def create_core_dir_and_files(self, isol_pact: PactUnit = None):
        self._admin.create_core_dir_and_files(isol_pact)


def healingunit_shop(
    title: str, env_dir: str, cure_handle: str, _auto_output_to_public: bool = None
) -> HealingUnit:
    x_healing = HealingUnit()
    x_healing.set_env_dir(env_dir, title, cure_handle=cure_handle)
    x_healing.get_isol()
    x_healing._isol._set_auto_output_to_public(_auto_output_to_public)
    x_healing.set_isol()
    return x_healing
