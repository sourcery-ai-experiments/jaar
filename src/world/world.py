from src.culture.culture import CultureUnit
from src.world.concern import CultureAddress, LobbyUnit
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
        x_cultureaddress = x_lobbyunit._concernunit.cultureaddress

        for x_person_id in x_cultureaddress.person_ids.keys():
            self.set_personunit(x_person_id, replace_alert=False)
            x_personunit = self.get_personunit_from_memory(x_person_id)
            x_cultureunit = x_personunit.get_cultureunit(x_cultureaddress.culture_id)
            x_cultureunit.full_setup_councilunit(x_person_id)
            x_cultureunit.full_setup_councilunit(x_lobbyunit._lobbyer_pid)
            for lobbyee_pid in x_lobbyunit._lobbyee_pids.keys():
                x_cultureunit.full_setup_councilunit(lobbyee_pid)

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
        cultureaddress: CultureAddress,
        council_person_id: PersonID,
    ):
        culture_id = cultureaddress.culture_id

        for culture_person_id in cultureaddress.person_ids.keys():
            if self.personunit_exists(culture_person_id) == False:
                self.set_personunit(culture_person_id)
            x_personunit = self.get_personunit_from_memory(culture_person_id)

            if x_personunit.cultureunit_exists(culture_id) == False:
                x_personunit.set_cultureunit(culture_id)
            x_culture = x_personunit.get_cultureunit(culture_id)

            if self.personunit_exists(council_person_id) == False:
                self.set_personunit(council_person_id)

            if x_culture.councilunit_exists(culture_person_id) == False:
                x_culture.add_councilunit(culture_person_id)
            if x_culture.councilunit_exists(council_person_id) == False:
                x_culture.add_councilunit(council_person_id)


def worldunit_shop(mark: WorldMark, worlds_dir: str) -> WorldUnit:
    world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
    world_x._set_world_dirs()
    world_x._set_personunits_empty_if_null()
    return world_x
