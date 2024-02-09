from src._prime.road import AgentID, PersonID, PartyID, ClerkID
from src.agenda.agenda import (
    get_from_json as agendaunit_get_from_json,
    get_meld_of_agenda_files,
    AgendaUnit,
    agendaunit_shop,
    partyunit_shop,
    get_from_json as agendaunit_get_from_json,
)
from src.instrument.file import (
    single_dir_create_if_null,
    save_file,
    open_file,
    delete_dir,
    rename_dir as x_func_rename_dir,
)
from src._prime.road import default_road_delimiter_if_none
from dataclasses import dataclass
from os import path as os_path


class InvalidclerkException(Exception):
    pass


@dataclass
class ClerkUnit:
    _clerk_id: ClerkID = None
    _env_dir: str = None
    _market_id: str = None
    _clerkunit_dir: str = None
    _clerkunits_dir: str = None
    _contract_file_name: str = None
    _contract_file_path: str = None
    _agenda_output_file_name: str = None
    _agenda_output_file_path: str = None
    _forum_file_name: str = None
    _forum_dir: str = None
    _agendas_depot_dir: str = None
    _agendas_ignore_dir: str = None
    _agendas_digest_dir: str = None
    _road_delimiter: str = None
    _contract: AgendaUnit = None

    def refresh_depot_agendas(self):
        for party_x in self._contract._partys.values():
            if party_x.party_id != self._clerk_id:
                party_agenda = agendaunit_get_from_json(
                    x_agenda_json=self.open_forum_agenda(party_x.party_id)
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
            x_agenda._agent_id, depotlink_type, creditor_weight, debtor_weight
        )
        if self.get_contract()._auto_output_to_forum:
            self.save_refreshed_output_to_forum()

    def _set_depotlink(
        self,
        outer_agent_id: str,
        link_type: str = None,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        self.raise_exception_if_no_file("depot", outer_agent_id)
        self._set_partyunit_depotlink(
            outer_agent_id, link_type, creditor_weight, debtor_weight
        )

        if link_type == "assignment":
            self._set_assignment_depotlink(outer_agent_id)
        elif link_type == "blind_trust":
            x_agenda = self.open_depot_agenda(agent_id=outer_agent_id)
            self.save_agenda_to_digest(x_agenda)
        elif link_type == "ignore":
            new_x_agenda = agendaunit_shop(_agent_id=outer_agent_id)
            new_x_agenda.set_world_id(self._market_id)
            self.set_ignore_agenda_file(new_x_agenda, new_x_agenda._agent_id)

    def _set_assignment_depotlink(self, outer_agent_id):
        depot_agenda = self.open_depot_agenda(outer_agent_id)
        depot_agenda.set_agenda_metrics()
        empty_agenda = agendaunit_shop(_agent_id=self._clerk_id)
        empty_agenda.set_world_id(self._market_id)
        assign_agenda = depot_agenda.get_assignment(
            empty_agenda, self.get_contract()._partys, self._clerk_id
        )
        assign_agenda.set_agenda_metrics()
        self.save_agenda_to_digest(assign_agenda, depot_agenda._agent_id)

    def _set_partyunit_depotlink(
        self,
        party_id: PartyID,
        link_type: str = None,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        party_x = self.get_contract().get_party(party_id)
        if party_x is None:
            self.get_contract().set_partyunit(
                partyunit_shop(
                    party_id=party_id,
                    depotlink_type=link_type,
                    creditor_weight=creditor_weight,
                    debtor_weight=debtor_weight,
                )
            )
        else:
            party_x.set_depotlink_type(link_type, creditor_weight, debtor_weight)

    def del_depot_agenda(self, agent_id: AgentID):
        self._del_depotlink(party_id=agent_id)
        self.erase_depot_agenda(agent_id)
        self.erase_digest_agenda(agent_id)

    def _del_depotlink(self, party_id: PartyID):
        self._contract.get_party(party_id).del_depotlink_type()

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

    def set_ignore_agenda_file(self, agendaunit: AgendaUnit, src_agent_id: str):
        self.save_ignore_agenda(agendaunit, src_agent_id)
        self.save_agenda_to_digest(agendaunit, src_agent_id)

    # housekeeping
    def set_env_dir(
        self,
        env_dir: str,
        clerk_id: ClerkID,
        market_id: str,
        _road_delimiter: str = None,
    ):
        self._clerk_id = clerk_id
        self._env_dir = env_dir
        self._market_id = market_id
        self._road_delimiter = default_road_delimiter_if_none(_road_delimiter)

    def set_dirs(self):
        env_clerkunits_folder = "clerkunits"
        self._clerkunits_dir = f"{self._env_dir}/{env_clerkunits_folder}"
        self._clerkunit_dir = f"{self._clerkunits_dir}/{self._clerk_id}"
        self._contract_file_name = "contract_agenda.json"
        self._contract_file_path = f"{self._clerkunit_dir}/{self._contract_file_name}"
        self._agenda_output_file_name = "output_agenda.json"
        self._agenda_output_file_path = (
            f"{self._clerkunit_dir}/{self._agenda_output_file_name}"
        )
        self._forum_file_name = f"{self._clerk_id}.json"
        forum_text = "forum"
        depot_text = "depot"
        self._forum_dir = f"{self._env_dir}/{forum_text}"
        self._agendas_depot_dir = f"{self._clerkunit_dir}/{depot_text}"
        self._agendas_ignore_dir = f"{self._clerkunit_dir}/ignores"
        self._agendas_digest_dir = f"{self._clerkunit_dir}/digests"

    def set_clerk_id(self, new_cid: ClerkID):
        old_clerkunit_dir = self._clerkunit_dir
        self._clerk_id = new_cid
        self.set_dirs()

        x_func_rename_dir(src=old_clerkunit_dir, dst=self._clerkunit_dir)

    def create_core_dir_and_files(self, contract_agenda: AgendaUnit = None):
        single_dir_create_if_null(x_path=self._clerkunit_dir)
        single_dir_create_if_null(x_path=self._forum_dir)
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
            file_name = f"{x_agenda._agent_id}.json"
        # if dest_dir == self._forum_dir:
        #     file_name = self._forum_file_name
        save_file(
            dest_dir=dest_dir,
            file_name=file_name,
            file_text=x_agenda.get_json(),
            replace=True,
        )

    def save_agenda_to_forum(self, x_agenda: AgendaUnit):
        dest_dir = self._forum_dir
        self._save_agenda_to_path(x_agenda, dest_dir)

    def save_ignore_agenda(self, x_agenda: AgendaUnit, src_agent_id: str):
        dest_dir = self._agendas_ignore_dir
        file_name = None
        if src_agent_id != None:
            file_name = f"{src_agent_id}.json"
        else:
            file_name = f"{x_agenda._agent_id}.json"
        self._save_agenda_to_path(x_agenda, dest_dir, file_name)

    def save_agenda_to_digest(self, x_agenda: AgendaUnit, src_agent_id: str = None):
        dest_dir = self._agendas_digest_dir
        file_name = None
        if src_agent_id != None:
            file_name = f"{src_agent_id}.json"
        else:
            file_name = f"{x_agenda._agent_id}.json"
        self._save_agenda_to_path(x_agenda, dest_dir, file_name)

    def save_contract_agenda(self, x_agenda: AgendaUnit):
        x_agenda.set_agent_id(self._clerk_id)
        x_agenda.set_road_delimiter(self._road_delimiter)
        self._save_agenda_to_path(
            x_agenda, self._clerkunit_dir, self._contract_file_name
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
        dest_dir = self._clerkunit_dir
        file_name = self._agenda_output_file_name
        self._save_agenda_to_path(x_agenda, dest_dir, file_name)

    def open_forum_agenda(self, agent_id: PersonID) -> str:
        file_name_x = f"{agent_id}.json"
        print(f"{self._forum_dir=}")
        return open_file(self._forum_dir, file_name_x)

    def open_depot_agenda(self, agent_id: PersonID) -> AgendaUnit:
        file_name_x = f"{agent_id}.json"
        x_agenda_json = open_file(self._agendas_depot_dir, file_name_x)
        return agendaunit_get_from_json(x_agenda_json=x_agenda_json)

    def open_ignore_agenda(self, agent_id: PersonID) -> AgendaUnit:
        ignore_file_name = f"{agent_id}.json"
        agenda_json = open_file(self._agendas_ignore_dir, ignore_file_name)
        agenda_obj = agendaunit_get_from_json(x_agenda_json=agenda_json)
        agenda_obj.set_agenda_metrics()
        return agenda_obj

    def open_contract_agenda(self) -> AgendaUnit:
        x_agenda = None
        if not self._contract_agenda_exists():
            self.save_contract_agenda(self._get_empty_contract_agenda())
        x_json = open_file(self._clerkunit_dir, self._contract_file_name)
        x_agenda = agendaunit_get_from_json(x_agenda_json=x_json)
        x_agenda.set_agenda_metrics()
        return x_agenda

    def open_output_agenda(self) -> AgendaUnit:
        x_agenda_json = open_file(self._clerkunit_dir, self._agenda_output_file_name)
        x_agenda = agendaunit_get_from_json(x_agenda_json)
        x_agenda.set_agenda_metrics()
        return x_agenda

    def _get_empty_contract_agenda(self):
        x_agenda = agendaunit_shop(
            _agent_id=self._clerk_id,
            _weight=0,
            _road_delimiter=self._road_delimiter,
        )
        x_agenda.add_partyunit(party_id=self._clerk_id)
        x_agenda.set_world_id(self._market_id)
        return x_agenda

    def erase_depot_agenda(self, agent_id):
        delete_dir(f"{self._agendas_depot_dir}/{agent_id}.json")

    def erase_digest_agenda(self, agent_id):
        delete_dir(f"{self._agendas_digest_dir}/{agent_id}.json")

    def erase_contract_agenda_file(self):
        delete_dir(dir=f"{self._clerkunit_dir}/{self._contract_file_name}")

    def raise_exception_if_no_file(self, dir_type: str, agent_id: str):
        x_agenda_file_name = f"{agent_id}.json"
        if dir_type == "depot":
            x_agenda_file_path = f"{self._agendas_depot_dir}/{x_agenda_file_name}"
        if not os_path.exists(x_agenda_file_path):
            raise InvalidclerkException(
                f"agent_id {self._clerk_id} cannot find agenda {agent_id} in {x_agenda_file_path}"
            )

    def _contract_agenda_exists(self) -> bool:
        bool_x = None
        try:
            open_file(self._clerkunit_dir, self._contract_file_name)
            bool_x = True
        except Exception:
            bool_x = False
        return bool_x

    def get_remelded_output_agenda(self) -> AgendaUnit:
        self.save_output_agenda()
        return self.open_output_agenda()

    def save_refreshed_output_to_forum(self):
        self.save_agenda_to_forum(self.get_remelded_output_agenda())


def clerkunit_shop(
    agent_id: AgentID,
    env_dir: str,
    market_id: str,
    _auto_output_to_forum: bool = None,
    _road_delimiter: str = None,
) -> ClerkUnit:
    x_clerk = ClerkUnit()
    x_clerk.set_env_dir(
        env_dir=env_dir,
        clerk_id=agent_id,
        market_id=market_id,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    x_clerk.set_dirs()
    x_clerk.get_contract()
    x_clerk._contract._set_auto_output_to_forum(_auto_output_to_forum)
    # x_clerk.save_contract_agenda(x_clerk.get_contract())
    x_clerk.get_contract()
    return x_clerk
