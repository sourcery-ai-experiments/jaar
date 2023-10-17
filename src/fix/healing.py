from src.deal.deal import (
    get_from_json as dealunit_get_from_json,
    get_dict_of_deal_from_dict,
    get_meld_of_deal_files,
    PersonName,
    DealUnit,
    partyunit_shop,
    get_from_json as dealunit_get_from_json,
    PartyTitle,
)
from src.deal.x_func import (
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
    _fix_handle: str
    _healingunit_dir: str = None
    _healingunits_dir: str = None
    _isol_file_title: str = None
    _isol_file_path: str = None
    _deal_output_file_title: str = None
    _deal_output_file_path: str = None
    _public_file_title: str = None
    _deals_public_dir: str = None
    _deals_depot_dir: str = None
    _deals_ignore_dir: str = None
    _deals_digest_dir: str = None

    def set_dirs(self):
        env_healingunits_folder = "healingunits"
        deals_str = "deals"
        self._healingunits_dir = f"{self._env_dir}/{env_healingunits_folder}"
        self._healingunit_dir = f"{self._healingunits_dir}/{self._healing_title}"
        self._isol_file_title = "isol_deal.json"
        self._isol_file_path = f"{self._healingunit_dir}/{self._isol_file_title}"
        self._deal_output_file_title = "output_deal.json"
        self._deal_output_file_path = (
            f"{self._healingunit_dir}/{self._deal_output_file_title}"
        )
        self._public_file_title = f"{self._healing_title}.json"
        self._deals_public_dir = f"{self._env_dir}/{deals_str}"
        self._deals_depot_dir = f"{self._healingunit_dir}/{deals_str}"
        self._deals_ignore_dir = f"{self._healingunit_dir}/ignores"
        self._deals_digest_dir = f"{self._healingunit_dir}/digests"

    def set_healing_title(self, new_title: str):
        old_healingunit_dir = self._healingunit_dir
        self._healing_title = new_title
        self.set_dirs()

        rename_dir(src=old_healingunit_dir, dst=self._healingunit_dir)

    def create_core_dir_and_files(self, isol_deal: DealUnit = None):
        single_dir_create_if_null(x_path=self._healingunit_dir)
        single_dir_create_if_null(x_path=self._deals_public_dir)
        single_dir_create_if_null(x_path=self._deals_depot_dir)
        single_dir_create_if_null(x_path=self._deals_digest_dir)
        single_dir_create_if_null(x_path=self._deals_ignore_dir)
        if isol_deal is None and self._isol_deal_exists() == False:
            self.save_isol_deal(self._get_empty_isol_deal())
        elif isol_deal != None and self._isol_deal_exists() == False:
            self.save_isol_deal(isol_deal)

    def _save_deal_to_path(
        self, deal_x: DealUnit, dest_dir: str, file_title: str = None
    ):
        if file_title is None:
            file_title = f"{deal_x._healer}.json"
        # if dest_dir == self._deals_public_dir:
        #     file_title = self._public_file_title
        x_func_save_file(
            dest_dir=dest_dir,
            file_title=file_title,
            file_text=deal_x.get_json(),
            replace=True,
        )

    def save_deal_to_public(self, deal_x: DealUnit):
        dest_dir = self._deals_public_dir
        self._save_deal_to_path(deal_x, dest_dir)

    def save_ignore_deal(self, deal_x: DealUnit, src_deal_healer: str):
        dest_dir = self._deals_ignore_dir
        file_title = None
        if src_deal_healer != None:
            file_title = f"{src_deal_healer}.json"
        else:
            file_title = f"{deal_x._healer}.json"
        self._save_deal_to_path(deal_x, dest_dir, file_title)

    def save_deal_to_digest(self, deal_x: DealUnit, src_deal_healer: str = None):
        dest_dir = self._deals_digest_dir
        file_title = None
        if src_deal_healer != None:
            file_title = f"{src_deal_healer}.json"
        else:
            file_title = f"{deal_x._healer}.json"
        self._save_deal_to_path(deal_x, dest_dir, file_title)

    def save_isol_deal(self, deal_x: DealUnit):
        deal_x.set_healer(self._healing_title)
        self._save_deal_to_path(deal_x, self._healingunit_dir, self._isol_file_title)

    def save_deal_to_depot(self, deal_x: DealUnit):
        dest_dir = self._deals_depot_dir
        self._save_deal_to_path(deal_x, dest_dir)

    def save_output_deal(self) -> DealUnit:
        isol_deal_x = self.open_isol_deal()
        isol_deal_x.meld(isol_deal_x, party_weight=1)
        deal_x = get_meld_of_deal_files(
            primary_deal=isol_deal_x,
            meldees_dir=self._deals_digest_dir,
        )
        dest_dir = self._healingunit_dir
        file_title = self._deal_output_file_title
        self._save_deal_to_path(deal_x, dest_dir, file_title)

    def open_public_deal(self, healer: PersonName) -> str:
        file_title_x = f"{healer}.json"
        return x_func_open_file(self._deals_public_dir, file_title_x)

    def open_depot_deal(self, healer: PersonName) -> DealUnit:
        file_title_x = f"{healer}.json"
        x_deal_json = x_func_open_file(self._deals_depot_dir, file_title_x)
        return dealunit_get_from_json(x_deal_json=x_deal_json)

    def open_ignore_deal(self, healer: PersonName) -> DealUnit:
        ignore_file_title = f"{healer}.json"
        deal_json = x_func_open_file(self._deals_ignore_dir, ignore_file_title)
        deal_obj = dealunit_get_from_json(x_deal_json=deal_json)
        deal_obj.set_deal_metrics()
        return deal_obj

    def open_isol_deal(self) -> DealUnit:
        x_deal = None
        if not self._isol_deal_exists():
            self.save_isol_deal(self._get_empty_isol_deal())
        ct = x_func_open_file(self._healingunit_dir, self._isol_file_title)
        x_deal = dealunit_get_from_json(x_deal_json=ct)
        x_deal.set_deal_metrics()
        return x_deal

    def open_output_deal(self) -> DealUnit:
        x_deal_json = x_func_open_file(
            self._healingunit_dir, self._deal_output_file_title
        )
        x_deal = dealunit_get_from_json(x_deal_json)
        x_deal.set_deal_metrics()
        return x_deal

    def _get_empty_isol_deal(self):
        x_deal = DealUnit(_healer=self._healing_title, _weight=0)
        x_deal.add_partyunit(title=self._healing_title)
        x_deal.set_fix_handle(self._fix_handle)
        return x_deal

    def erase_depot_deal(self, healer):
        x_func_delete_dir(f"{self._deals_depot_dir}/{healer}.json")

    def erase_digest_deal(self, healer):
        x_func_delete_dir(f"{self._deals_digest_dir}/{healer}.json")

    def erase_isol_deal_file(self):
        x_func_delete_dir(dir=f"{self._healingunit_dir}/{self._isol_file_title}")

    def raise_exception_if_no_file(self, dir_type: str, healer: str):
        x_deal_file_title = f"{healer}.json"
        if dir_type == "depot":
            x_deal_file_path = f"{self._deals_depot_dir}/{x_deal_file_title}"
        if not os_path.exists(x_deal_file_path):
            raise InvalidHealingException(
                f"Healer {self._healing_title} cannot find deal {healer} in {x_deal_file_path}"
            )

    def _isol_deal_exists(self):
        bool_x = None
        try:
            x_func_open_file(self._healingunit_dir, self._isol_file_title)
            bool_x = True
        except Exception:
            bool_x = False
        return bool_x

    def get_remelded_output_deal(self):
        self.save_output_deal()
        return self.open_output_deal()

    def save_refreshed_output_to_public(self):
        self.save_deal_to_public(self.get_remelded_output_deal())


def healingadmin_shop(
    _healing_title: str, _env_dir: str, _fix_handle: str
) -> HealingAdmin:
    uax = HealingAdmin(
        _healing_title=_healing_title, _env_dir=_env_dir, _fix_handle=_fix_handle
    )
    uax.set_dirs()
    return uax


@dataclass
class HealingUnit:
    _admin: HealingAdmin = None
    _isol: DealUnit = None

    def refresh_depot_deals(self):
        for party_x in self._isol._partys.values():
            if party_x.title != self._admin._healing_title:
                party_deal = dealunit_get_from_json(
                    x_deal_json=self._admin.open_public_deal(party_x.title)
                )
                self.set_depot_deal(
                    deal_x=party_deal,
                    depotlink_type=party_x.depotlink_type,
                    creditor_weight=party_x.creditor_weight,
                    debtor_weight=party_x.debtor_weight,
                )

    def set_depot_deal(
        self,
        deal_x: DealUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        self.set_isol_if_empty()
        self._admin.save_deal_to_depot(deal_x)
        self._set_depotlink(
            deal_x._healer, depotlink_type, creditor_weight, debtor_weight
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
            x_deal = self._admin.open_depot_deal(healer=outer_healer)
            self._admin.save_deal_to_digest(x_deal)
        elif link_type == "ignore":
            new_x_deal = DealUnit(_healer=outer_healer)
            new_x_deal.set_fix_handle(self._admin._fix_handle)
            self.set_ignore_deal_file(new_x_deal, new_x_deal._healer)

    def _set_assignment_depotlink(self, outer_healer):
        src_deal = self._admin.open_depot_deal(outer_healer)
        src_deal.set_deal_metrics()
        empty_deal = DealUnit(_healer=self._admin._healing_title)
        empty_deal.set_fix_handle(self._admin._fix_handle)
        assign_deal = src_deal.get_assignment(
            empty_deal, self.get_isol()._partys, self._admin._healing_title
        )
        assign_deal.set_deal_metrics()
        self._admin.save_deal_to_digest(assign_deal, src_deal._healer)

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

    def del_depot_deal(self, deal_healer: str):
        self._del_depotlink(partytitle=deal_healer)
        self._admin.erase_depot_deal(deal_healer)
        self._admin.erase_digest_deal(deal_healer)

    def _del_depotlink(self, partytitle: PartyTitle):
        self._isol.get_party(partytitle).del_depotlink_type()

    def get_isol(self):
        if self._isol is None:
            self._isol = self._admin.open_isol_deal()
        return self._isol

    def set_isol(self, deal_x: DealUnit = None):
        if deal_x != None:
            self._isol = deal_x
        self._admin.save_isol_deal(self._isol)
        self._isol = None

    def set_isol_if_empty(self):
        # if self._isol is None:
        self.get_isol()

    def set_ignore_deal_file(self, dealunit: DealUnit, src_deal_healer: str):
        self._admin.save_ignore_deal(dealunit, src_deal_healer)
        self._admin.save_deal_to_digest(dealunit, src_deal_healer)

    # housekeeping
    def set_env_dir(self, env_dir: str, healing_title: str, fix_handle: str):
        self._admin = healingadmin_shop(
            _healing_title=healing_title, _env_dir=env_dir, _fix_handle=fix_handle
        )

    def create_core_dir_and_files(self, isol_deal: DealUnit = None):
        self._admin.create_core_dir_and_files(isol_deal)


def healingunit_shop(
    title: str, env_dir: str, fix_handle: str, _auto_output_to_public: bool = None
) -> HealingUnit:
    x_healing = HealingUnit()
    x_healing.set_env_dir(env_dir, title, fix_handle=fix_handle)
    x_healing.get_isol()
    x_healing._isol._set_auto_output_to_public(_auto_output_to_public)
    x_healing.set_isol()
    return x_healing
