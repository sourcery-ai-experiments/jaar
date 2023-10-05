from dataclasses import dataclass


class PersonTitle(str):
    pass


# @dataclass
# class PersonUnit:
#     mark: PersonTitle
#     person_dir: str

#     def _set_world_dirs(self):
#         self.persons_dir = f"{self.worlds_dir}/persons"


# def worldunit_shop(mark: WorldMark, worlds_dir: str) -> WorldUnit:
#     world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
#     world_x._set_world_dirs()
#     return world_x
