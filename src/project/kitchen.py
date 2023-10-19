from src.deal.deal import (
    get_from_json as dealunit_get_from_json,
    get_dict_of_deal_from_dict,
    get_meld_of_deal_files,
    PersonName,
    DealUnit,
    dealunit_shop,
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


class InvalidkitchenException(Exception):
    pass


@dataclass
class KitchenAdmin:
    _kitchen_title: str
    _env_dir: str
    _project_handle: str
    _kitchenunit_dir: str = None
    _kitchenunits_dir: str = None
    _seed_file_title: str = None
    _seed_file_path: str = None
    _deal_output_file_title: str = None
    _deal_output_file_path: str = None
    _public_file_title: str = None
    _deals_public_dir: str = None
    _deals_depot_dir: str = None
    _deals_ignore_dir: str = None
    _deals_digest_dir: str = None

    def set_dirs(self):
        env_kitchenunits_folder = "kitchenunits"
        deals_str = "deals"
        self._kitchenunits_dir = f"{self._env_dir}/{env_kitchenunits_folder}"
        self._kitchenunit_dir = f"{self._kitchenunits_dir}/{self._kitchen_title}"
        self._seed_file_title = "seed_deal.json"
        self._seed_file_path = f"{self._kitchenunit_dir}/{self._seed_file_title}"
        self._deal_output_file_title = "output_deal.json"
        self._deal_output_file_path = (
            f"{self._kitchenunit_dir}/{self._deal_output_file_title}"
        )
        self._public_file_title = f"{self._kitchen_title}.json"
        self._deals_public_dir = f"{self._env_dir}/{deals_str}"
        self._deals_depot_dir = f"{self._kitchenunit_dir}/{deals_str}"
        self._deals_ignore_dir = f"{self._kitchenunit_dir}/ignores"
        self._deals_digest_dir = f"{self._kitchenunit_dir}/digests"

    def set_kitchen_title(self, new_title: str):
        old_kitchenunit_dir = self._kitchenunit_dir
        self._kitchen_title = new_title
        self.set_dirs()

        rename_dir(src=old_kitchenunit_dir, dst=self._kitchenunit_dir)

    def create_core_dir_and_files(self, seed_deal: DealUnit = None):
        single_dir_create_if_null(x_path=self._kitchenunit_dir)
        single_dir_create_if_null(x_path=self._deals_public_dir)
        single_dir_create_if_null(x_path=self._deals_depot_dir)
        single_dir_create_if_null(x_path=self._deals_digest_dir)
        single_dir_create_if_null(x_path=self._deals_ignore_dir)
        if seed_deal is None and self._seed_deal_exists() == False:
            self.save_seed_deal(self._get_empty_seed_deal())
        elif seed_deal != None and self._seed_deal_exists() == False:
            self.save_seed_deal(seed_deal)

    def _save_deal_to_path(
        self, x_deal: DealUnit, dest_dir: str, file_title: str = None
    ):
        if file_title is None:
            file_title = f"{x_deal._healer}.json"
        # if dest_dir == self._deals_public_dir:
        #     file_title = self._public_file_title
        x_func_save_file(
            dest_dir=dest_dir,
            file_title=file_title,
            file_text=x_deal.get_json(),
            replace=True,
        )

    def save_deal_to_public(self, x_deal: DealUnit):
        dest_dir = self._deals_public_dir
        self._save_deal_to_path(x_deal, dest_dir)

    def save_ignore_deal(self, x_deal: DealUnit, src_deal_healer: str):
        dest_dir = self._deals_ignore_dir
        file_title = None
        if src_deal_healer != None:
            file_title = f"{src_deal_healer}.json"
        else:
            file_title = f"{x_deal._healer}.json"
        self._save_deal_to_path(x_deal, dest_dir, file_title)

    def save_deal_to_digest(self, x_deal: DealUnit, src_deal_healer: str = None):
        dest_dir = self._deals_digest_dir
        file_title = None
        if src_deal_healer != None:
            file_title = f"{src_deal_healer}.json"
        else:
            file_title = f"{x_deal._healer}.json"
        self._save_deal_to_path(x_deal, dest_dir, file_title)

    def save_seed_deal(self, x_deal: DealUnit):
        x_deal.set_healer(self._kitchen_title)
        self._save_deal_to_path(x_deal, self._kitchenunit_dir, self._seed_file_title)

    def save_deal_to_depot(self, x_deal: DealUnit):
        dest_dir = self._deals_depot_dir
        self._save_deal_to_path(x_deal, dest_dir)

    def save_output_deal(self) -> DealUnit:
        x_seed_deal = self.open_seed_deal()
        x_seed_deal.meld(x_seed_deal, party_weight=1)
        x_deal = get_meld_of_deal_files(
            primary_deal=x_seed_deal,
            meldees_dir=self._deals_digest_dir,
        )
        dest_dir = self._kitchenunit_dir
        file_title = self._deal_output_file_title
        self._save_deal_to_path(x_deal, dest_dir, file_title)

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

    def open_seed_deal(self) -> DealUnit:
        x_deal = None
        if not self._seed_deal_exists():
            self.save_seed_deal(self._get_empty_seed_deal())
        ct = x_func_open_file(self._kitchenunit_dir, self._seed_file_title)
        x_deal = dealunit_get_from_json(x_deal_json=ct)
        x_deal.set_deal_metrics()
        return x_deal

    def open_output_deal(self) -> DealUnit:
        x_deal_json = x_func_open_file(
            self._kitchenunit_dir, self._deal_output_file_title
        )
        x_deal = dealunit_get_from_json(x_deal_json)
        x_deal.set_deal_metrics()
        return x_deal

    def _get_empty_seed_deal(self):
        x_deal = dealunit_shop(_healer=self._kitchen_title, _weight=0)
        x_deal.add_partyunit(title=self._kitchen_title)
        x_deal.set_project_handle(self._project_handle)
        return x_deal

    def erase_depot_deal(self, healer):
        x_func_delete_dir(f"{self._deals_depot_dir}/{healer}.json")

    def erase_digest_deal(self, healer):
        x_func_delete_dir(f"{self._deals_digest_dir}/{healer}.json")

    def erase_seed_deal_file(self):
        x_func_delete_dir(dir=f"{self._kitchenunit_dir}/{self._seed_file_title}")

    def raise_exception_if_no_file(self, dir_type: str, healer: str):
        x_deal_file_title = f"{healer}.json"
        if dir_type == "depot":
            x_deal_file_path = f"{self._deals_depot_dir}/{x_deal_file_title}"
        if not os_path.exists(x_deal_file_path):
            raise InvalidkitchenException(
                f"Healer {self._kitchen_title} cannot find deal {healer} in {x_deal_file_path}"
            )

    def _seed_deal_exists(self):
        bool_x = None
        try:
            x_func_open_file(self._kitchenunit_dir, self._seed_file_title)
            bool_x = True
        except Exception:
            bool_x = False
        return bool_x

    def get_remelded_output_deal(self):
        self.save_output_deal()
        return self.open_output_deal()

    def save_refreshed_output_to_public(self):
        self.save_deal_to_public(self.get_remelded_output_deal())


def kitchenadmin_shop(
    _kitchen_title: str, _env_dir: str, _project_handle: str
) -> KitchenAdmin:
    x_kitchenadmin = KitchenAdmin(
        _kitchen_title=_kitchen_title,
        _env_dir=_env_dir,
        _project_handle=_project_handle,
    )
    x_kitchenadmin.set_dirs()
    return x_kitchenadmin


@dataclass
class KitchenUnit:
    _admin: KitchenAdmin = None
    _seed: DealUnit = None

    def refresh_depot_deals(self):
        for party_x in self._seed._partys.values():
            if party_x.title != self._admin._kitchen_title:
                party_deal = dealunit_get_from_json(
                    x_deal_json=self._admin.open_public_deal(party_x.title)
                )
                self.set_depot_deal(
                    x_deal=party_deal,
                    depotlink_type=party_x.depotlink_type,
                    creditor_weight=party_x.creditor_weight,
                    debtor_weight=party_x.debtor_weight,
                )

    def set_depot_deal(
        self,
        x_deal: DealUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        self.set_seed_if_empty()
        self._admin.save_deal_to_depot(x_deal)
        self._set_depotlink(
            x_deal._healer, depotlink_type, creditor_weight, debtor_weight
        )
        if self.get_seed()._auto_output_to_public:
            self._admin.save_refreshed_output_to_public()

    def _set_depotlinks_empty_if_null(self):
        self.set_seed_if_empty()
        self._seed.set_partys_empty_if_null()

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
            new_x_deal = dealunit_shop(_healer=outer_healer)
            new_x_deal.set_project_handle(self._admin._project_handle)
            self.set_ignore_deal_file(new_x_deal, new_x_deal._healer)

    def _set_assignment_depotlink(self, outer_healer):
        src_deal = self._admin.open_depot_deal(outer_healer)
        src_deal.set_deal_metrics()
        empty_deal = dealunit_shop(_healer=self._admin._kitchen_title)
        empty_deal.set_project_handle(self._admin._project_handle)
        assign_deal = src_deal.get_assignment(
            empty_deal, self.get_seed()._partys, self._admin._kitchen_title
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
        party_x = self.get_seed().get_party(title)
        if party_x is None:
            self.get_seed().set_partyunit(
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
        self._seed.get_party(partytitle).del_depotlink_type()

    def get_seed(self):
        if self._seed is None:
            self._seed = self._admin.open_seed_deal()
        return self._seed

    def set_seed(self, x_deal: DealUnit = None):
        if x_deal != None:
            self._seed = x_deal
        self._admin.save_seed_deal(self._seed)
        self._seed = None

    def set_seed_if_empty(self):
        # if self._seed is None:
        self.get_seed()

    def set_ignore_deal_file(self, dealunit: DealUnit, src_deal_healer: str):
        self._admin.save_ignore_deal(dealunit, src_deal_healer)
        self._admin.save_deal_to_digest(dealunit, src_deal_healer)

    # housekeeping
    def set_env_dir(self, env_dir: str, kitchen_title: str, project_handle: str):
        self._admin = kitchenadmin_shop(
            _kitchen_title=kitchen_title,
            _env_dir=env_dir,
            _project_handle=project_handle,
        )

    def create_core_dir_and_files(self, seed_deal: DealUnit = None):
        self._admin.create_core_dir_and_files(seed_deal)


def kitchenunit_shop(
    title: str, env_dir: str, project_handle: str, _auto_output_to_public: bool = None
) -> KitchenUnit:
    x_kitchen = KitchenUnit()
    x_kitchen.set_env_dir(env_dir, title, project_handle=project_handle)
    x_kitchen.get_seed()
    x_kitchen._seed._set_auto_output_to_public(_auto_output_to_public)
    x_kitchen.set_seed()
    return x_kitchen
