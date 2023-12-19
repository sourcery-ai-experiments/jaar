from src.agenda.agenda import agendaunit_shop
from src.economy.economy import EconomyUnit
from src.world.concern import EconomyAddress, LobbyUnit
from src.world.person import PersonID, PersonUnit, personunit_shop
from dataclasses import dataclass


class PersonExistsException(Exception):
    pass


class WorldMark(str):  # Created to help track the concept
    pass


@dataclass
class WorldUnit:
    mark: WorldMark
    worlds_dir: str
    _persons_dir: str = None
    _world_dir: str = None
    _personunits: dict[PersonID:PersonUnit] = None

    def apply_lobbyunit(self, x_lobbyunit: LobbyUnit):
        for lobbyee_pid in x_lobbyunit._lobbyee_pids.keys():
            self.set_personunit(lobbyee_pid, replace_alert=False)
        self.set_personunit(x_lobbyunit._lobbyer_pid, replace_alert=False)
        x_economyaddress = x_lobbyunit._concernunit.economyaddress

        for x_person_id in x_economyaddress.person_ids.keys():
            self.set_personunit(x_person_id, replace_alert=False)
            x_personunit = self.get_personunit_from_memory(x_person_id)
            x_economyunit = x_personunit.get_economyunit(x_economyaddress.economy_id)
            x_economyunit.full_setup_councilunit(x_person_id)
            x_economyunit.full_setup_councilunit(x_lobbyunit._lobbyer_pid)
            for lobbyee_pid in x_lobbyunit._lobbyee_pids.keys():
                x_economyunit.full_setup_councilunit(lobbyee_pid)

    def _get_person_dir(self, person_id):
        return f"{self._persons_dir}/{person_id}"

    def _set_world_dirs(self):
        self._world_dir = f"{self.worlds_dir}/{self.mark}"
        self._persons_dir = f"{self._world_dir}/persons"

    def _set_personunits_empty_if_null(self):
        if self._personunits is None:
            self._personunits = {}

    def personunit_exists(self, person_id: PersonID):
        return self._personunits.get(person_id) != None

    def _set_person_in_memory(self, personunit: PersonUnit):
        self._personunits[personunit.pid] = personunit

    def set_personunit(
        self,
        person_id: PersonID,
        replace_personunit: bool = False,
        replace_alert: bool = True,
    ):
        x_personunit = personunit_shop(person_id, self._get_person_dir(person_id))
        if self.personunit_exists(x_personunit.pid) == False and not replace_personunit:
            self._set_person_in_memory(x_personunit)
        elif replace_alert:
            raise PersonExistsException(
                f"set_personunit fail: {x_personunit.pid} already exists"
            )

    def get_personunit_from_memory(self, person_id: PersonID) -> PersonUnit:
        return self._personunits.get(person_id)

    def add_cultural_connection(
        self,
        economyaddress: EconomyAddress,
        council_person_id: PersonID,
    ):
        economy_id = economyaddress.economy_id

        for economy_person_id in economyaddress.person_ids.keys():
            if self.personunit_exists(economy_person_id) == False:
                self.set_personunit(economy_person_id)
            x_personunit = self.get_personunit_from_memory(economy_person_id)

            if x_personunit.economyunit_exists(economy_id) == False:
                x_personunit.set_economyunit(economy_id)
            x_economy = x_personunit.get_economyunit(economy_id)

            if self.personunit_exists(council_person_id) == False:
                self.set_personunit(council_person_id)

            if x_economy.councilunit_exists(economy_person_id) == False:
                x_economy.add_councilunit(economy_person_id)
            if x_economy.councilunit_exists(council_person_id) == False:
                x_economy.add_councilunit(council_person_id)

    def get_priority_agenda(self, person_id: PersonID):
        x_personunit = self.get_personunit_from_memory(person_id)
        x_agenda = agendaunit_shop(person_id)
        for x_economyunit in x_personunit._economys.values():
            public_agenda = x_economyunit.get_public_agenda(person_id)
            public_agenda.set_economy_id(x_agenda._economy_id)
            x_agenda.meld(public_agenda)
        return x_agenda


def worldunit_shop(mark: WorldMark, worlds_dir: str) -> WorldUnit:
    world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
    world_x._set_world_dirs()
    world_x._set_personunits_empty_if_null()
    return world_x
