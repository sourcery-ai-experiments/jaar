from dataclasses import dataclass
from src.world.person import PersonID, PersonUnit, personunit_shop


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
    _persons_obj: dict[PersonID:PersonUnit] = None

    def get_person_dir(self, person_id):
        return f"{self._persons_dir}/{person_id}"

    def _set_world_dirs(self):
        self._world_dir = f"{self.worlds_dir}/{self.mark}"
        self._persons_dir = f"{self._world_dir}/persons"

    def _set_persons_obj_empty_if_null(self):
        if self._persons_obj is None:
            self._persons_obj = {}

    def _set_person_in_memory(self, personunit: PersonUnit):
        self._persons_obj[personunit.pid] = personunit

    def set_personunit(self, personunit: PersonUnit):
        self._set_person_in_memory(personunit)

    def add_personunit(self, person_id: PersonID):
        x_personunit = personunit_shop(person_id, self.get_person_dir(person_id))
        if self._persons_obj.get(x_personunit.pid) is None:
            self.set_personunit(x_personunit)
        else:
            raise PersonExistsException(
                f"add_personunit fail: {x_personunit.pid} already exists"
            )

    def get_personunit_from_memory(self, person_id: PersonID) -> PersonUnit:
        return self._persons_obj.get(person_id)


def worldunit_shop(mark: WorldMark, worlds_dir: str) -> WorldUnit:
    world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
    world_x._set_world_dirs()
    world_x._set_persons_obj_empty_if_null()
    return world_x
