from src.agenda.agenda import (
    get_from_json as agendaunit_get_from_json,
    get_dict_of_agenda_from_dict,
    get_meld_of_agenda_files,
    PersonName,
    AgendaUnit,
    agendaunit_shop,
    partyunit_shop,
    get_from_json as agendaunit_get_from_json,
    PartyTitle,
)
from src.agenda.x_func import (
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
    _culture_handle: str
    _kitchenunit_dir: str = None
    _kitchenunits_dir: str = None
    _seed_file_title: str = None
    _seed_file_path: str = None
    _agenda_output_file_title: str = None
    _agenda_output_file_path: str = None
    _public_file_title: str = None
    _agendas_public_dir: str = None
    _agendas_depot_dir: str = None
    _agendas_ignore_dir: str = None
    _agendas_digest_dir: str = None

    def set_dirs(self):
        env_kitchenunits_folder = "kitchenunits"
        agendas_str = "agendas"
        self._kitchenunits_dir = f"{self._env_dir}/{env_kitchenunits_folder}"
        self._kitchenunit_dir = f"{self._kitchenunits_dir}/{self._kitchen_title}"
        self._seed_file_title = "seed_agenda.json"
        self._seed_file_path = f"{self._kitchenunit_dir}/{self._seed_file_title}"
        self._agenda_output_file_title = "output_agenda.json"
        self._agenda_output_file_path = (
            f"{self._kitchenunit_dir}/{self._agenda_output_file_title}"
        )
        self._public_file_title = f"{self._kitchen_title}.json"
        self._agendas_public_dir = f"{self._env_dir}/{agendas_str}"
        self._agendas_depot_dir = f"{self._kitchenunit_dir}/{agendas_str}"
        self._agendas_ignore_dir = f"{self._kitchenunit_dir}/ignores"
        self._agendas_digest_dir = f"{self._kitchenunit_dir}/digests"

    def set_kitchen_title(self, new_title: str):
        old_kitchenunit_dir = self._kitchenunit_dir
        self._kitchen_title = new_title
        self.set_dirs()

        rename_dir(src=old_kitchenunit_dir, dst=self._kitchenunit_dir)

    def create_core_dir_and_files(self, seed_agenda: AgendaUnit = None):
        single_dir_create_if_null(x_path=self._kitchenunit_dir)
        single_dir_create_if_null(x_path=self._agendas_public_dir)
        single_dir_create_if_null(x_path=self._agendas_depot_dir)
        single_dir_create_if_null(x_path=self._agendas_digest_dir)
        single_dir_create_if_null(x_path=self._agendas_ignore_dir)
        if seed_agenda is None and self._seed_agenda_exists() == False:
            self.save_seed_agenda(self._get_empty_seed_agenda())
        elif seed_agenda != None and self._seed_agenda_exists() == False:
            self.save_seed_agenda(seed_agenda)

    def _save_agenda_to_path(
        self, x_agenda: AgendaUnit, dest_dir: str, file_title: str = None
    ):
        if file_title is None:
            file_title = f"{x_agenda._healer}.json"
        # if dest_dir == self._agendas_public_dir:
        #     file_title = self._public_file_title
        x_func_save_file(
            dest_dir=dest_dir,
            file_title=file_title,
            file_text=x_agenda.get_json(),
            replace=True,
        )

    def save_agenda_to_public(self, x_agenda: AgendaUnit):
        dest_dir = self._agendas_public_dir
        self._save_agenda_to_path(x_agenda, dest_dir)

    def save_ignore_agenda(self, x_agenda: AgendaUnit, src_agenda_healer: str):
        dest_dir = self._agendas_ignore_dir
        file_title = None
        if src_agenda_healer != None:
            file_title = f"{src_agenda_healer}.json"
        else:
            file_title = f"{x_agenda._healer}.json"
        self._save_agenda_to_path(x_agenda, dest_dir, file_title)

    def save_agenda_to_digest(
        self, x_agenda: AgendaUnit, src_agenda_healer: str = None
    ):
        dest_dir = self._agendas_digest_dir
        file_title = None
        if src_agenda_healer != None:
            file_title = f"{src_agenda_healer}.json"
        else:
            file_title = f"{x_agenda._healer}.json"
        self._save_agenda_to_path(x_agenda, dest_dir, file_title)

    def save_seed_agenda(self, x_agenda: AgendaUnit):
        x_agenda.set_healer(self._kitchen_title)
        self._save_agenda_to_path(
            x_agenda, self._kitchenunit_dir, self._seed_file_title
        )

    def save_agenda_to_depot(self, x_agenda: AgendaUnit):
        dest_dir = self._agendas_depot_dir
        self._save_agenda_to_path(x_agenda, dest_dir)

    def save_output_agenda(self) -> AgendaUnit:
        x_seed_agenda = self.open_seed_agenda()
        x_seed_agenda.meld(x_seed_agenda, party_weight=1)
        x_agenda = get_meld_of_agenda_files(
            primary_agenda=x_seed_agenda,
            meldees_dir=self._agendas_digest_dir,
        )
        dest_dir = self._kitchenunit_dir
        file_title = self._agenda_output_file_title
        self._save_agenda_to_path(x_agenda, dest_dir, file_title)

    def open_public_agenda(self, healer: PersonName) -> str:
        file_title_x = f"{healer}.json"
        return x_func_open_file(self._agendas_public_dir, file_title_x)

    def open_depot_agenda(self, healer: PersonName) -> AgendaUnit:
        file_title_x = f"{healer}.json"
        x_agenda_json = x_func_open_file(self._agendas_depot_dir, file_title_x)
        return agendaunit_get_from_json(x_agenda_json=x_agenda_json)

    def open_ignore_agenda(self, healer: PersonName) -> AgendaUnit:
        ignore_file_title = f"{healer}.json"
        agenda_json = x_func_open_file(self._agendas_ignore_dir, ignore_file_title)
        agenda_obj = agendaunit_get_from_json(x_agenda_json=agenda_json)
        agenda_obj.set_agenda_metrics()
        return agenda_obj

    def open_seed_agenda(self) -> AgendaUnit:
        x_agenda = None
        if not self._seed_agenda_exists():
            self.save_seed_agenda(self._get_empty_seed_agenda())
        ct = x_func_open_file(self._kitchenunit_dir, self._seed_file_title)
        x_agenda = agendaunit_get_from_json(x_agenda_json=ct)
        x_agenda.set_agenda_metrics()
        return x_agenda

    def open_output_agenda(self) -> AgendaUnit:
        x_agenda_json = x_func_open_file(
            self._kitchenunit_dir, self._agenda_output_file_title
        )
        x_agenda = agendaunit_get_from_json(x_agenda_json)
        x_agenda.set_agenda_metrics()
        return x_agenda

    def _get_empty_seed_agenda(self):
        x_agenda = agendaunit_shop(_healer=self._kitchen_title, _weight=0)
        x_agenda.add_partyunit(title=self._kitchen_title)
        x_agenda.set_culture_handle(self._culture_handle)
        return x_agenda

    def erase_depot_agenda(self, healer):
        x_func_delete_dir(f"{self._agendas_depot_dir}/{healer}.json")

    def erase_digest_agenda(self, healer):
        x_func_delete_dir(f"{self._agendas_digest_dir}/{healer}.json")

    def erase_seed_agenda_file(self):
        x_func_delete_dir(dir=f"{self._kitchenunit_dir}/{self._seed_file_title}")

    def raise_exception_if_no_file(self, dir_type: str, healer: str):
        x_agenda_file_title = f"{healer}.json"
        if dir_type == "depot":
            x_agenda_file_path = f"{self._agendas_depot_dir}/{x_agenda_file_title}"
        if not os_path.exists(x_agenda_file_path):
            raise InvalidkitchenException(
                f"Healer {self._kitchen_title} cannot find agenda {healer} in {x_agenda_file_path}"
            )

    def _seed_agenda_exists(self) -> bool:
        bool_x = None
        try:
            x_func_open_file(self._kitchenunit_dir, self._seed_file_title)
            bool_x = True
        except Exception:
            bool_x = False
        return bool_x

    def get_remelded_output_agenda(self) -> AgendaUnit:
        self.save_output_agenda()
        return self.open_output_agenda()

    def save_refreshed_output_to_public(self):
        self.save_agenda_to_public(self.get_remelded_output_agenda())


def kitchenadmin_shop(
    _kitchen_title: str, _env_dir: str, _culture_handle: str
) -> KitchenAdmin:
    x_kitchenadmin = KitchenAdmin(
        _kitchen_title=_kitchen_title,
        _env_dir=_env_dir,
        _culture_handle=_culture_handle,
    )
    x_kitchenadmin.set_dirs()
    return x_kitchenadmin


@dataclass
class KitchenUnit:
    _admin: KitchenAdmin = None
    _seed: AgendaUnit = None

    def refresh_depot_agendas(self):
        for party_x in self._seed._partys.values():
            if party_x.title != self._admin._kitchen_title:
                party_agenda = agendaunit_get_from_json(
                    x_agenda_json=self._admin.open_public_agenda(party_x.title)
                )
                self.set_depot_agenda(
                    x_agenda=party_agenda,
                    depotlink_type=party_x.depotlink_type,
                    creditor_weight=party_x.creditor_weight,
                    debtor_weight=party_x.debtor_weight,
                )

    def set_depot_agenda(
        self,
        x_agenda: AgendaUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        self.set_seed_if_empty()
        self._admin.save_agenda_to_depot(x_agenda)
        self._set_depotlink(
            x_agenda._healer, depotlink_type, creditor_weight, debtor_weight
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
            x_agenda = self._admin.open_depot_agenda(healer=outer_healer)
            self._admin.save_agenda_to_digest(x_agenda)
        elif link_type == "ignore":
            new_x_agenda = agendaunit_shop(_healer=outer_healer)
            new_x_agenda.set_culture_handle(self._admin._culture_handle)
            self.set_ignore_agenda_file(new_x_agenda, new_x_agenda._healer)

    def _set_assignment_depotlink(self, outer_healer):
        src_agenda = self._admin.open_depot_agenda(outer_healer)
        src_agenda.set_agenda_metrics()
        empty_agenda = agendaunit_shop(_healer=self._admin._kitchen_title)
        empty_agenda.set_culture_handle(self._admin._culture_handle)
        assign_agenda = src_agenda.get_assignment(
            empty_agenda, self.get_seed()._partys, self._admin._kitchen_title
        )
        assign_agenda.set_agenda_metrics()
        self._admin.save_agenda_to_digest(assign_agenda, src_agenda._healer)

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

    def del_depot_agenda(self, agenda_healer: str):
        self._del_depotlink(partytitle=agenda_healer)
        self._admin.erase_depot_agenda(agenda_healer)
        self._admin.erase_digest_agenda(agenda_healer)

    def _del_depotlink(self, partytitle: PartyTitle):
        self._seed.get_party(partytitle).del_depotlink_type()

    def get_seed(self):
        if self._seed is None:
            self._seed = self._admin.open_seed_agenda()
        return self._seed

    def set_seed(self, x_agenda: AgendaUnit = None):
        if x_agenda != None:
            self._seed = x_agenda
        self._admin.save_seed_agenda(self._seed)
        self._seed = None

    def set_seed_if_empty(self):
        # if self._seed is None:
        self.get_seed()

    def set_ignore_agenda_file(self, agendaunit: AgendaUnit, src_agenda_healer: str):
        self._admin.save_ignore_agenda(agendaunit, src_agenda_healer)
        self._admin.save_agenda_to_digest(agendaunit, src_agenda_healer)

    # housekeeping
    def set_env_dir(self, env_dir: str, kitchen_title: str, culture_handle: str):
        self._admin = kitchenadmin_shop(
            _kitchen_title=kitchen_title,
            _env_dir=env_dir,
            _culture_handle=culture_handle,
        )

    def create_core_dir_and_files(self, seed_agenda: AgendaUnit = None):
        self._admin.create_core_dir_and_files(seed_agenda)


def kitchenunit_shop(
    title: str, env_dir: str, culture_handle: str, _auto_output_to_public: bool = None
) -> KitchenUnit:
    x_kitchen = KitchenUnit()
    x_kitchen.set_env_dir(env_dir, title, culture_handle=culture_handle)
    x_kitchen.get_seed()
    x_kitchen._seed._set_auto_output_to_public(_auto_output_to_public)
    x_kitchen.set_seed()
    return x_kitchen
