from src.agenda.agenda import (
    get_from_json as agendaunit_get_from_json,
    get_dict_of_agenda_from_dict,
    get_meld_of_agenda_files,
    PersonPID,
    AgendaUnit,
    agendaunit_shop,
    partyunit_shop,
    get_from_json as agendaunit_get_from_json,
    PartyPID,
)
from src.agenda.x_func import (
    x_get_json,
    single_dir_create_if_null,
    save_file as x_func_save_file,
    dir_files as x_func_dir_files,
    open_file as x_func_open_file,
    delete_dir as x_func_delete_dir,
)
from src.culture.y_func import rename_dir
from dataclasses import dataclass
from os import path as os_path
from json import loads as json_loads


class InvalidcouncilException(Exception):
    pass


class CouncilCID(PersonPID):
    pass


@dataclass
class CouncilAdmin:
    _council_cid: CouncilCID
    _env_dir: str
    _culture_title: str
    _councilunit_dir: str = None
    _councilunits_dir: str = None
    _seed_file_name: str = None
    _seed_file_path: str = None
    _agenda_output_file_name: str = None
    _agenda_output_file_path: str = None
    _public_file_name: str = None
    _agendas_public_dir: str = None
    _agendas_depot_dir: str = None
    _agendas_ignore_dir: str = None
    _agendas_digest_dir: str = None

    def set_dirs(self):
        env_councilunits_folder = "councilunits"
        agendas_str = "agendas"
        self._councilunits_dir = f"{self._env_dir}/{env_councilunits_folder}"
        self._councilunit_dir = f"{self._councilunits_dir}/{self._council_cid}"
        self._seed_file_name = "seed_agenda.json"
        self._seed_file_path = f"{self._councilunit_dir}/{self._seed_file_name}"
        self._agenda_output_file_name = "output_agenda.json"
        self._agenda_output_file_path = (
            f"{self._councilunit_dir}/{self._agenda_output_file_name}"
        )
        self._public_file_name = f"{self._council_cid}.json"
        self._agendas_public_dir = f"{self._env_dir}/{agendas_str}"
        self._agendas_depot_dir = f"{self._councilunit_dir}/{agendas_str}"
        self._agendas_ignore_dir = f"{self._councilunit_dir}/ignores"
        self._agendas_digest_dir = f"{self._councilunit_dir}/digests"

    def set_council_cid(self, new_cid: CouncilCID):
        old_councilunit_dir = self._councilunit_dir
        self._council_cid = new_cid
        self.set_dirs()

        rename_dir(src=old_councilunit_dir, dst=self._councilunit_dir)

    def create_core_dir_and_files(self, seed_agenda: AgendaUnit = None):
        single_dir_create_if_null(x_path=self._councilunit_dir)
        single_dir_create_if_null(x_path=self._agendas_public_dir)
        single_dir_create_if_null(x_path=self._agendas_depot_dir)
        single_dir_create_if_null(x_path=self._agendas_digest_dir)
        single_dir_create_if_null(x_path=self._agendas_ignore_dir)
        if seed_agenda is None and self._seed_agenda_exists() == False:
            self.save_seed_agenda(self._get_empty_seed_agenda())
        elif seed_agenda != None and self._seed_agenda_exists() == False:
            self.save_seed_agenda(seed_agenda)

    def _save_agenda_to_path(
        self, x_agenda: AgendaUnit, dest_dir: str, file_name: str = None
    ):
        if file_name is None:
            file_name = f"{x_agenda._healer}.json"
        # if dest_dir == self._agendas_public_dir:
        #     file_name = self._public_file_name
        x_func_save_file(
            dest_dir=dest_dir,
            file_name=file_name,
            file_text=x_agenda.get_json(),
            replace=True,
        )

    def save_agenda_to_public(self, x_agenda: AgendaUnit):
        dest_dir = self._agendas_public_dir
        self._save_agenda_to_path(x_agenda, dest_dir)

    def save_ignore_agenda(self, x_agenda: AgendaUnit, src_agenda_healer: str):
        dest_dir = self._agendas_ignore_dir
        file_name = None
        if src_agenda_healer != None:
            file_name = f"{src_agenda_healer}.json"
        else:
            file_name = f"{x_agenda._healer}.json"
        self._save_agenda_to_path(x_agenda, dest_dir, file_name)

    def save_agenda_to_digest(
        self, x_agenda: AgendaUnit, src_agenda_healer: str = None
    ):
        dest_dir = self._agendas_digest_dir
        file_name = None
        if src_agenda_healer != None:
            file_name = f"{src_agenda_healer}.json"
        else:
            file_name = f"{x_agenda._healer}.json"
        self._save_agenda_to_path(x_agenda, dest_dir, file_name)

    def save_seed_agenda(self, x_agenda: AgendaUnit):
        x_agenda.set_healer(self._council_cid)
        self._save_agenda_to_path(x_agenda, self._councilunit_dir, self._seed_file_name)

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
        dest_dir = self._councilunit_dir
        file_name = self._agenda_output_file_name
        self._save_agenda_to_path(x_agenda, dest_dir, file_name)

    def open_public_agenda(self, healer: PersonPID) -> str:
        file_name_x = f"{healer}.json"
        return x_func_open_file(self._agendas_public_dir, file_name_x)

    def open_depot_agenda(self, healer: PersonPID) -> AgendaUnit:
        file_name_x = f"{healer}.json"
        x_agenda_json = x_func_open_file(self._agendas_depot_dir, file_name_x)
        return agendaunit_get_from_json(x_agenda_json=x_agenda_json)

    def open_ignore_agenda(self, healer: PersonPID) -> AgendaUnit:
        ignore_file_name = f"{healer}.json"
        agenda_json = x_func_open_file(self._agendas_ignore_dir, ignore_file_name)
        agenda_obj = agendaunit_get_from_json(x_agenda_json=agenda_json)
        agenda_obj.set_agenda_metrics()
        return agenda_obj

    def open_seed_agenda(self) -> AgendaUnit:
        x_agenda = None
        if not self._seed_agenda_exists():
            self.save_seed_agenda(self._get_empty_seed_agenda())
        x_json = x_func_open_file(self._councilunit_dir, self._seed_file_name)
        x_agenda = agendaunit_get_from_json(x_agenda_json=x_json)
        x_agenda.set_agenda_metrics()
        return x_agenda

    def open_output_agenda(self) -> AgendaUnit:
        x_agenda_json = x_func_open_file(
            self._councilunit_dir, self._agenda_output_file_name
        )
        x_agenda = agendaunit_get_from_json(x_agenda_json)
        x_agenda.set_agenda_metrics()
        return x_agenda

    def _get_empty_seed_agenda(self):
        x_agenda = agendaunit_shop(_healer=self._council_cid, _weight=0)
        x_agenda.add_partyunit(pid=self._council_cid)
        x_agenda.set_culture_title(self._culture_title)
        return x_agenda

    def erase_depot_agenda(self, healer):
        x_func_delete_dir(f"{self._agendas_depot_dir}/{healer}.json")

    def erase_digest_agenda(self, healer):
        x_func_delete_dir(f"{self._agendas_digest_dir}/{healer}.json")

    def erase_seed_agenda_file(self):
        x_func_delete_dir(dir=f"{self._councilunit_dir}/{self._seed_file_name}")

    def raise_exception_if_no_file(self, dir_type: str, healer: str):
        x_agenda_file_name = f"{healer}.json"
        if dir_type == "depot":
            x_agenda_file_path = f"{self._agendas_depot_dir}/{x_agenda_file_name}"
        if not os_path.exists(x_agenda_file_path):
            raise InvalidcouncilException(
                f"Healer {self._council_cid} cannot find agenda {healer} in {x_agenda_file_path}"
            )

    def _seed_agenda_exists(self) -> bool:
        bool_x = None
        try:
            x_func_open_file(self._councilunit_dir, self._seed_file_name)
            bool_x = True
        except Exception:
            bool_x = False
        return bool_x

    def get_remelded_output_agenda(self) -> AgendaUnit:
        self.save_output_agenda()
        return self.open_output_agenda()

    def save_refreshed_output_to_public(self):
        self.save_agenda_to_public(self.get_remelded_output_agenda())


def counciladmin_shop(
    _council_cid: CouncilCID, _env_dir: str, _culture_title: str
) -> CouncilAdmin:
    x_counciladmin = CouncilAdmin(
        _council_cid=_council_cid,
        _env_dir=_env_dir,
        _culture_title=_culture_title,
    )
    x_counciladmin.set_dirs()
    return x_counciladmin


@dataclass
class CouncilUnit:
    _admin: CouncilAdmin = None
    _seed: AgendaUnit = None

    def refresh_depot_agendas(self):
        for party_x in self._seed._partys.values():
            if party_x.pid != self._admin._council_cid:
                party_agenda = agendaunit_get_from_json(
                    x_agenda_json=self._admin.open_public_agenda(party_x.pid)
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
            new_x_agenda.set_culture_title(self._admin._culture_title)
            self.set_ignore_agenda_file(new_x_agenda, new_x_agenda._healer)

    def _set_assignment_depotlink(self, outer_healer):
        src_agenda = self._admin.open_depot_agenda(outer_healer)
        src_agenda.set_agenda_metrics()
        empty_agenda = agendaunit_shop(_healer=self._admin._council_cid)
        empty_agenda.set_culture_title(self._admin._culture_title)
        assign_agenda = src_agenda.get_assignment(
            empty_agenda, self.get_seed()._partys, self._admin._council_cid
        )
        assign_agenda.set_agenda_metrics()
        self._admin.save_agenda_to_digest(assign_agenda, src_agenda._healer)

    def _set_partyunit_depotlink(
        self,
        pid: PartyPID,
        link_type: str = None,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        party_x = self.get_seed().get_party(pid)
        if party_x is None:
            self.get_seed().set_partyunit(
                partyunit_shop(
                    pid=pid,
                    depotlink_type=link_type,
                    creditor_weight=creditor_weight,
                    debtor_weight=debtor_weight,
                )
            )
        else:
            party_x.set_depotlink_type(link_type, creditor_weight, debtor_weight)

    def del_depot_agenda(self, agenda_healer: str):
        self._del_depotlink(partypid=agenda_healer)
        self._admin.erase_depot_agenda(agenda_healer)
        self._admin.erase_digest_agenda(agenda_healer)

    def _del_depotlink(self, partypid: PartyPID):
        self._seed.get_party(partypid).del_depotlink_type()

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
    def set_env_dir(self, env_dir: str, council_cid: CouncilCID, culture_title: str):
        self._admin = counciladmin_shop(
            _council_cid=council_cid,
            _env_dir=env_dir,
            _culture_title=culture_title,
        )

    def create_core_dir_and_files(self, seed_agenda: AgendaUnit = None):
        self._admin.create_core_dir_and_files(seed_agenda)


def councilunit_shop(
    pid: str, env_dir: str, culture_title: str, _auto_output_to_public: bool = None
) -> CouncilUnit:
    x_council = CouncilUnit()
    x_council.set_env_dir(env_dir, pid, culture_title=culture_title)
    x_council.get_seed()
    x_council._seed._set_auto_output_to_public(_auto_output_to_public)
    x_council.set_seed()
    return x_council
