from dataclasses import dataclass
from src.world.person import PersonName, PersonUnit


class WorldMark(str):
    pass


@dataclass
class WorldUnit:
    mark: WorldMark
    worlds_dir: str
    _persons_dir: str = None
    _persons_obj: dict[PersonName:PersonUnit] = None

    def _set_world_dirs(self):
        self._persons_dir = f"{self.worlds_dir}/persons"

    def _set_persons_obj_empty_if_null(self):
        if self._persons_obj is None:
            self._persons_obj = {}

    def set_person_in_memory(self, personunit: PersonUnit):
        self._set_persons_obj_empty_if_null()
        self._persons_obj[personunit.name] = personunit


def worldunit_shop(mark: WorldMark, worlds_dir: str) -> WorldUnit:
    world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
    world_x._set_world_dirs()
    world_x._set_persons_obj_empty_if_null()
    return world_x
