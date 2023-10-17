from src.oath.oath import (
    get_from_json as oathunit_get_from_json,
    get_dict_of_oath_from_dict,
    get_meld_of_oath_files,
    PersonName,
    OathUnit,
    partyunit_shop,
    get_from_json as oathunit_get_from_json,
    PartyTitle,
)
from src.oath.x_func import (
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
    _oath_output_file_title: str = None
    _oath_output_file_path: str = None
    _public_file_title: str = None
    _oaths_public_dir: str = None
    _oaths_depot_dir: str = None
    _oaths_ignore_dir: str = None
    _oaths_digest_dir: str = None

    def set_dirs(self):
        env_healingunits_folder = "healingunits"
        oaths_str = "oaths"
        self._healingunits_dir = f"{self._env_dir}/{env_healingunits_folder}"
        self._healingunit_dir = f"{self._healingunits_dir}/{self._healing_title}"
        self._isol_file_title = "isol_oath.json"
        self._isol_file_path = f"{self._healingunit_dir}/{self._isol_file_title}"
        self._oath_output_file_title = "output_oath.json"
        self._oath_output_file_path = (
            f"{self._healingunit_dir}/{self._oath_output_file_title}"
        )
        self._public_file_title = f"{self._healing_title}.json"
        self._oaths_public_dir = f"{self._env_dir}/{oaths_str}"
        self._oaths_depot_dir = f"{self._healingunit_dir}/{oaths_str}"
        self._oaths_ignore_dir = f"{self._healingunit_dir}/ignores"
        self._oaths_digest_dir = f"{self._healingunit_dir}/digests"

    def set_healing_title(self, new_title: str):
        old_healingunit_dir = self._healingunit_dir
        self._healing_title = new_title
        self.set_dirs()

        rename_dir(src=old_healingunit_dir, dst=self._healingunit_dir)

    def create_core_dir_and_files(self, isol_oath: OathUnit = None):
        single_dir_create_if_null(x_path=self._healingunit_dir)
        single_dir_create_if_null(x_path=self._oaths_public_dir)
        single_dir_create_if_null(x_path=self._oaths_depot_dir)
        single_dir_create_if_null(x_path=self._oaths_digest_dir)
        single_dir_create_if_null(x_path=self._oaths_ignore_dir)
        if isol_oath is None and self._isol_oath_exists() == False:
            self.save_isol_oath(self._get_empty_isol_oath())
        elif isol_oath != None and self._isol_oath_exists() == False:
            self.save_isol_oath(isol_oath)

    def _save_oath_to_path(
        self, oath_x: OathUnit, dest_dir: str, file_title: str = None
    ):
        if file_title is None:
            file_title = f"{oath_x._healer}.json"
        # if dest_dir == self._oaths_public_dir:
        #     file_title = self._public_file_title
        x_func_save_file(
            dest_dir=dest_dir,
            file_title=file_title,
            file_text=oath_x.get_json(),
            replace=True,
        )

    def save_oath_to_public(self, oath_x: OathUnit):
        dest_dir = self._oaths_public_dir
        self._save_oath_to_path(oath_x, dest_dir)

    def save_ignore_oath(self, oath_x: OathUnit, src_oath_healer: str):
        dest_dir = self._oaths_ignore_dir
        file_title = None
        if src_oath_healer != None:
            file_title = f"{src_oath_healer}.json"
        else:
            file_title = f"{oath_x._healer}.json"
        self._save_oath_to_path(oath_x, dest_dir, file_title)

    def save_oath_to_digest(self, oath_x: OathUnit, src_oath_healer: str = None):
        dest_dir = self._oaths_digest_dir
        file_title = None
        if src_oath_healer != None:
            file_title = f"{src_oath_healer}.json"
        else:
            file_title = f"{oath_x._healer}.json"
        self._save_oath_to_path(oath_x, dest_dir, file_title)

    def save_isol_oath(self, oath_x: OathUnit):
        oath_x.set_healer(self._healing_title)
        self._save_oath_to_path(oath_x, self._healingunit_dir, self._isol_file_title)

    def save_oath_to_depot(self, oath_x: OathUnit):
        dest_dir = self._oaths_depot_dir
        self._save_oath_to_path(oath_x, dest_dir)

    def save_output_oath(self) -> OathUnit:
        isol_oath_x = self.open_isol_oath()
        isol_oath_x.meld(isol_oath_x, party_weight=1)
        oath_x = get_meld_of_oath_files(
            primary_oath=isol_oath_x,
            meldees_dir=self._oaths_digest_dir,
        )
        dest_dir = self._healingunit_dir
        file_title = self._oath_output_file_title
        self._save_oath_to_path(oath_x, dest_dir, file_title)

    def open_public_oath(self, healer: PersonName) -> str:
        file_title_x = f"{healer}.json"
        return x_func_open_file(self._oaths_public_dir, file_title_x)

    def open_depot_oath(self, healer: PersonName) -> OathUnit:
        file_title_x = f"{healer}.json"
        x_oath_json = x_func_open_file(self._oaths_depot_dir, file_title_x)
        return oathunit_get_from_json(x_oath_json=x_oath_json)

    def open_ignore_oath(self, healer: PersonName) -> OathUnit:
        ignore_file_title = f"{healer}.json"
        oath_json = x_func_open_file(self._oaths_ignore_dir, ignore_file_title)
        oath_obj = oathunit_get_from_json(x_oath_json=oath_json)
        oath_obj.set_oath_metrics()
        return oath_obj

    def open_isol_oath(self) -> OathUnit:
        x_oath = None
        if not self._isol_oath_exists():
            self.save_isol_oath(self._get_empty_isol_oath())
        ct = x_func_open_file(self._healingunit_dir, self._isol_file_title)
        x_oath = oathunit_get_from_json(x_oath_json=ct)
        x_oath.set_oath_metrics()
        return x_oath

    def open_output_oath(self) -> OathUnit:
        x_oath_json = x_func_open_file(
            self._healingunit_dir, self._oath_output_file_title
        )
        x_oath = oathunit_get_from_json(x_oath_json)
        x_oath.set_oath_metrics()
        return x_oath

    def _get_empty_isol_oath(self):
        x_oath = OathUnit(_healer=self._healing_title, _weight=0)
        x_oath.add_partyunit(title=self._healing_title)
        x_oath.set_cure_handle(self._cure_handle)
        return x_oath

    def erase_depot_oath(self, healer):
        x_func_delete_dir(f"{self._oaths_depot_dir}/{healer}.json")

    def erase_digest_oath(self, healer):
        x_func_delete_dir(f"{self._oaths_digest_dir}/{healer}.json")

    def erase_isol_oath_file(self):
        x_func_delete_dir(dir=f"{self._healingunit_dir}/{self._isol_file_title}")

    def raise_exception_if_no_file(self, dir_type: str, healer: str):
        x_oath_file_title = f"{healer}.json"
        if dir_type == "depot":
            x_oath_file_path = f"{self._oaths_depot_dir}/{x_oath_file_title}"
        if not os_path.exists(x_oath_file_path):
            raise InvalidHealingException(
                f"Healer {self._healing_title} cannot find oath {healer} in {x_oath_file_path}"
            )

    def _isol_oath_exists(self):
        bool_x = None
        try:
            x_func_open_file(self._healingunit_dir, self._isol_file_title)
            bool_x = True
        except Exception:
            bool_x = False
        return bool_x

    def get_remelded_output_oath(self):
        self.save_output_oath()
        return self.open_output_oath()

    def save_refreshed_output_to_public(self):
        self.save_oath_to_public(self.get_remelded_output_oath())


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
    _isol: OathUnit = None

    def refresh_depot_oaths(self):
        for party_x in self._isol._partys.values():
            if party_x.title != self._admin._healing_title:
                party_oath = oathunit_get_from_json(
                    x_oath_json=self._admin.open_public_oath(party_x.title)
                )
                self.set_depot_oath(
                    oath_x=party_oath,
                    depotlink_type=party_x.depotlink_type,
                    creditor_weight=party_x.creditor_weight,
                    debtor_weight=party_x.debtor_weight,
                )

    def set_depot_oath(
        self,
        oath_x: OathUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        self.set_isol_if_empty()
        self._admin.save_oath_to_depot(oath_x)
        self._set_depotlink(
            oath_x._healer, depotlink_type, creditor_weight, debtor_weight
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
            x_oath = self._admin.open_depot_oath(healer=outer_healer)
            self._admin.save_oath_to_digest(x_oath)
        elif link_type == "ignore":
            new_x_oath = OathUnit(_healer=outer_healer)
            new_x_oath.set_cure_handle(self._admin._cure_handle)
            self.set_ignore_oath_file(new_x_oath, new_x_oath._healer)

    def _set_assignment_depotlink(self, outer_healer):
        src_oath = self._admin.open_depot_oath(outer_healer)
        src_oath.set_oath_metrics()
        empty_oath = OathUnit(_healer=self._admin._healing_title)
        empty_oath.set_cure_handle(self._admin._cure_handle)
        assign_oath = src_oath.get_assignment(
            empty_oath, self.get_isol()._partys, self._admin._healing_title
        )
        assign_oath.set_oath_metrics()
        self._admin.save_oath_to_digest(assign_oath, src_oath._healer)

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

    def del_depot_oath(self, oath_healer: str):
        self._del_depotlink(partytitle=oath_healer)
        self._admin.erase_depot_oath(oath_healer)
        self._admin.erase_digest_oath(oath_healer)

    def _del_depotlink(self, partytitle: PartyTitle):
        self._isol.get_party(partytitle).del_depotlink_type()

    def get_isol(self):
        if self._isol is None:
            self._isol = self._admin.open_isol_oath()
        return self._isol

    def set_isol(self, oath_x: OathUnit = None):
        if oath_x != None:
            self._isol = oath_x
        self._admin.save_isol_oath(self._isol)
        self._isol = None

    def set_isol_if_empty(self):
        # if self._isol is None:
        self.get_isol()

    def set_ignore_oath_file(self, oathunit: OathUnit, src_oath_healer: str):
        self._admin.save_ignore_oath(oathunit, src_oath_healer)
        self._admin.save_oath_to_digest(oathunit, src_oath_healer)

    # housekeeping
    def set_env_dir(self, env_dir: str, healing_title: str, cure_handle: str):
        self._admin = healingadmin_shop(
            _healing_title=healing_title, _env_dir=env_dir, _cure_handle=cure_handle
        )

    def create_core_dir_and_files(self, isol_oath: OathUnit = None):
        self._admin.create_core_dir_and_files(isol_oath)


def healingunit_shop(
    title: str, env_dir: str, cure_handle: str, _auto_output_to_public: bool = None
) -> HealingUnit:
    x_healing = HealingUnit()
    x_healing.set_env_dir(env_dir, title, cure_handle=cure_handle)
    x_healing.get_isol()
    x_healing._isol._set_auto_output_to_public(_auto_output_to_public)
    x_healing.set_isol()
    return x_healing
