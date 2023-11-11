from dataclasses import dataclass
from src.world.person import PersonPID, PersonUnit, personunit_shop


class WorldMark(str):  # Created to help track the concept
    pass


@dataclass
class WorldUnit:
    mark: WorldMark
    worlds_dir: str
    _persons_dir: str = None
    _world_dir: str = None
    _persons_obj: dict[PersonPID:PersonUnit] = None

    def _set_world_dirs(self):
        self._world_dir = f"{self.worlds_dir}/{self.mark}"
        self._persons_dir = f"{self._world_dir}/persons"

    def _set_persons_obj_empty_if_null(self):
        if self._persons_obj is None:
            self._persons_obj = {}

    def _set_person_in_memory(self, personunit: PersonUnit):
        self._persons_obj[personunit.pid] = personunit

    def _create_person_from_pid(self, person_pid: PersonPID):
        x_person_dir = f"{self._persons_dir}/{person_pid}"
        x_person_obj = personunit_shop(pid=person_pid, person_dir=x_person_dir)
        self._set_person_in_memory(x_person_obj)

    def get_personunit_from_memory(self, person_pid: PersonPID) -> PersonUnit:
        return self._persons_obj.get(person_pid)


def worldunit_shop(mark: WorldMark, worlds_dir: str) -> WorldUnit:
    world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
    world_x._set_world_dirs()
    world_x._set_persons_obj_empty_if_null()
    return world_x
