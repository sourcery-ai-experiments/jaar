from src.agenda.agenda import (
    get_from_json as agendaunit_get_from_json,
    get_dict_of_agenda_from_dict,
    get_meld_of_agenda_files,
    PersonID,
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
from src.agenda.road import get_node_delimiter
from src.economy.y_func import rename_dir
from dataclasses import dataclass
from os import path as os_path
from json import loads as json_loads


class InvalidenactException(Exception):
    pass


class EnactCID(PersonID):
    pass


@dataclass
class EnactUnit:
    _enact_cid: EnactCID = None
    _env_dir: str = None
    _economy_id: str = None
    _enactunit_dir: str = None
    _enactunits_dir: str = None
    _contract_file_name: str = None
    _contract_file_path: str = None
    _agenda_output_file_name: str = None
    _agenda_output_file_path: str = None
    _public_file_name: str = None
    _agendas_public_dir: str = None
    _agendas_depot_dir: str = None
    _agendas_ignore_dir: str = None
    _agendas_digest_dir: str = None
    _road_node_delimiter: str = None
    _contract: AgendaUnit = None

    def refresh_depot_agendas(self):
        for party_x in self._contract._partys.values():
            if party_x.pid != self._enact_cid:
                party_agenda = agendaunit_get_from_json(
                    x_agenda_json=self.open_public_agenda(party_x.pid)
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
        self.set_contract_if_empty()
        self.save_agenda_to_depot(x_agenda)
        self._set_depotlink(
            x_agenda._healer, depotlink_type, creditor_weight, debtor_weight
        )
        if self.get_contract()._auto_output_to_public:
            self.save_refreshed_output_to_public()

    def _set_depotlink(
        self,
        outer_healer: str,
        link_type: str = None,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        self.raise_exception_if_no_file("depot", outer_healer)
        self._set_partyunit_depotlink(
            outer_healer, link_type, creditor_weight, debtor_weight
        )

        if link_type == "assignment":
            self._set_assignment_depotlink(outer_healer)
        elif link_type == "blind_trust":
            x_agenda = self.open_depot_agenda(healer=outer_healer)
            self.save_agenda_to_digest(x_agenda)
        elif link_type == "ignore":
            new_x_agenda = agendaunit_shop(_healer=outer_healer)
            new_x_agenda.set_economy_id(self._economy_id)
            self.set_ignore_agenda_file(new_x_agenda, new_x_agenda._healer)

    def _set_assignment_depotlink(self, outer_healer):
        src_agenda = self.open_depot_agenda(outer_healer)
        src_agenda.set_agenda_metrics()
        empty_agenda = agendaunit_shop(_healer=self._enact_cid)
        empty_agenda.set_economy_id(self._economy_id)
        assign_agenda = src_agenda.get_assignment(
            empty_agenda, self.get_contract()._partys, self._enact_cid
        )
        assign_agenda.set_agenda_metrics()
        self.save_agenda_to_digest(assign_agenda, src_agenda._healer)

    def _set_partyunit_depotlink(
        self,
        pid: PartyPID,
        link_type: str = None,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        party_x = self.get_contract().get_party(pid)
        if party_x is None:
            self.get_contract().set_partyunit(
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
        self.erase_depot_agenda(agenda_healer)
        self.erase_digest_agenda(agenda_healer)

    def _del_depotlink(self, partypid: PartyPID):
        self._contract.get_party(partypid).del_depotlink_type()

    def get_contract(self):
        if self._contract is None:
            self._contract = self.open_contract_agenda()
        return self._contract

    def set_contract(self, x_agenda: AgendaUnit = None):
        if x_agenda != None:
            self._contract = x_agenda
        self.save_contract_agenda(self._contract)
        self._contract = None

    def set_contract_if_empty(self):
        # if self._contract is None:
        self.get_contract()

    def set_ignore_agenda_file(self, agendaunit: AgendaUnit, src_agenda_healer: str):
        self.save_ignore_agenda(agendaunit, src_agenda_healer)
        self.save_agenda_to_digest(agendaunit, src_agenda_healer)

    # housekeeping
    def set_env_dir(
        self,
        env_dir: str,
        enact_cid: EnactCID,
        economy_id: str,
        _road_node_delimiter: str = None,
    ):
        self._enact_cid = enact_cid
        self._env_dir = env_dir
        self._economy_id = economy_id
        self._road_node_delimiter = get_node_delimiter(_road_node_delimiter)

    def set_dirs(self):
        env_enactunits_folder = "enactunits"
        agendas_str = "agendas"
        self._enactunits_dir = f"{self._env_dir}/{env_enactunits_folder}"
        self._enactunit_dir = f"{self._enactunits_dir}/{self._enact_cid}"
        self._contract_file_name = "contract_agenda.json"
        self._contract_file_path = f"{self._enactunit_dir}/{self._contract_file_name}"
        self._agenda_output_file_name = "output_agenda.json"
        self._agenda_output_file_path = (
            f"{self._enactunit_dir}/{self._agenda_output_file_name}"
        )
        self._public_file_name = f"{self._enact_cid}.json"
        self._agendas_public_dir = f"{self._env_dir}/{agendas_str}"
        self._agendas_depot_dir = f"{self._enactunit_dir}/{agendas_str}"
        self._agendas_ignore_dir = f"{self._enactunit_dir}/ignores"
        self._agendas_digest_dir = f"{self._enactunit_dir}/digests"

    def set_enact_cid(self, new_cid: EnactCID):
        old_enactunit_dir = self._enactunit_dir
        self._enact_cid = new_cid
        self.set_dirs()

        rename_dir(src=old_enactunit_dir, dst=self._enactunit_dir)

    def create_core_dir_and_files(self, contract_agenda: AgendaUnit = None):
        single_dir_create_if_null(x_path=self._enactunit_dir)
        single_dir_create_if_null(x_path=self._agendas_public_dir)
        single_dir_create_if_null(x_path=self._agendas_depot_dir)
        single_dir_create_if_null(x_path=self._agendas_digest_dir)
        single_dir_create_if_null(x_path=self._agendas_ignore_dir)

        if contract_agenda is None and self._contract_agenda_exists() == False:
            self.save_contract_agenda(self._get_empty_contract_agenda())
        elif contract_agenda != None and self._contract_agenda_exists() == False:
            self.save_contract_agenda(contract_agenda)

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

    def save_contract_agenda(self, x_agenda: AgendaUnit):
        x_agenda.set_healer(self._enact_cid)
        x_agenda.set_road_node_delimiter(self._road_node_delimiter)
        self._save_agenda_to_path(
            x_agenda, self._enactunit_dir, self._contract_file_name
        )

    def save_agenda_to_depot(self, x_agenda: AgendaUnit):
        dest_dir = self._agendas_depot_dir
        self._save_agenda_to_path(x_agenda, dest_dir)

    def save_output_agenda(self) -> AgendaUnit:
        x_contract_agenda = self.open_contract_agenda()
        x_contract_agenda.meld(x_contract_agenda, party_weight=1)
        x_agenda = get_meld_of_agenda_files(
            primary_agenda=x_contract_agenda,
            meldees_dir=self._agendas_digest_dir,
        )
        dest_dir = self._enactunit_dir
        file_name = self._agenda_output_file_name
        self._save_agenda_to_path(x_agenda, dest_dir, file_name)

    def open_public_agenda(self, healer: PersonID) -> str:
        file_name_x = f"{healer}.json"
        return x_func_open_file(self._agendas_public_dir, file_name_x)

    def open_depot_agenda(self, healer: PersonID) -> AgendaUnit:
        file_name_x = f"{healer}.json"
        x_agenda_json = x_func_open_file(self._agendas_depot_dir, file_name_x)
        return agendaunit_get_from_json(x_agenda_json=x_agenda_json)

    def open_ignore_agenda(self, healer: PersonID) -> AgendaUnit:
        ignore_file_name = f"{healer}.json"
        agenda_json = x_func_open_file(self._agendas_ignore_dir, ignore_file_name)
        agenda_obj = agendaunit_get_from_json(x_agenda_json=agenda_json)
        agenda_obj.set_agenda_metrics()
        return agenda_obj

    def open_contract_agenda(self) -> AgendaUnit:
        x_agenda = None
        if not self._contract_agenda_exists():
            self.save_contract_agenda(self._get_empty_contract_agenda())
        x_json = x_func_open_file(self._enactunit_dir, self._contract_file_name)
        x_agenda = agendaunit_get_from_json(x_agenda_json=x_json)
        x_agenda.set_agenda_metrics()
        return x_agenda

    def open_output_agenda(self) -> AgendaUnit:
        x_agenda_json = x_func_open_file(
            self._enactunit_dir, self._agenda_output_file_name
        )
        x_agenda = agendaunit_get_from_json(x_agenda_json)
        x_agenda.set_agenda_metrics()
        return x_agenda

    def _get_empty_contract_agenda(self):
        x_agenda = agendaunit_shop(
            _healer=self._enact_cid,
            _weight=0,
            _road_node_delimiter=self._road_node_delimiter,
        )
        x_agenda.add_partyunit(pid=self._enact_cid)
        x_agenda.set_economy_id(self._economy_id)
        return x_agenda

    def erase_depot_agenda(self, healer):
        x_func_delete_dir(f"{self._agendas_depot_dir}/{healer}.json")

    def erase_digest_agenda(self, healer):
        x_func_delete_dir(f"{self._agendas_digest_dir}/{healer}.json")

    def erase_contract_agenda_file(self):
        x_func_delete_dir(dir=f"{self._enactunit_dir}/{self._contract_file_name}")

    def raise_exception_if_no_file(self, dir_type: str, healer: str):
        x_agenda_file_name = f"{healer}.json"
        if dir_type == "depot":
            x_agenda_file_path = f"{self._agendas_depot_dir}/{x_agenda_file_name}"
        if not os_path.exists(x_agenda_file_path):
            raise InvalidenactException(
                f"Healer {self._enact_cid} cannot find agenda {healer} in {x_agenda_file_path}"
            )

    def _contract_agenda_exists(self) -> bool:
        bool_x = None
        try:
            x_func_open_file(self._enactunit_dir, self._contract_file_name)
            bool_x = True
        except Exception:
            bool_x = False
        return bool_x

    def get_remelded_output_agenda(self) -> AgendaUnit:
        self.save_output_agenda()
        return self.open_output_agenda()

    def save_refreshed_output_to_public(self):
        self.save_agenda_to_public(self.get_remelded_output_agenda())


def enactunit_shop(
    pid: str,
    env_dir: str,
    economy_id: str,
    _auto_output_to_public: bool = None,
    _road_node_delimiter: str = None,
) -> EnactUnit:
    x_enact = EnactUnit()
    x_enact.set_env_dir(
        env_dir=env_dir,
        enact_cid=pid,
        economy_id=economy_id,
        _road_node_delimiter=get_node_delimiter(_road_node_delimiter),
    )
    x_enact.set_dirs()
    x_enact.get_contract()
    x_enact._contract._set_auto_output_to_public(_auto_output_to_public)
    # x_enact.save_contract_agenda(x_enact.get_contract())
    x_enact.get_contract()
    return x_enact
