from dataclasses import dataclass


class WorldMark(str):
    pass


@dataclass
class WorldUnit:
    mark: WorldMark
    worlds_dir: str
    persons_dir: str = None

    def _set_world_dirs(self):
        self.persons_dir = f"{self.worlds_dir}/persons"


def worldunit_shop(mark: WorldMark, worlds_dir: str) -> WorldUnit:
    world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
    world_x._set_world_dirs()
    return world_x
