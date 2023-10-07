from dataclasses import dataclass


class PersonName(str):
    pass


@dataclass
class PersonUnit:
    name: PersonName = None
    person_dir: str = None


#     def _set_world_dirs(self):
#         self._persons_dir = f"{self.worlds_dir}/persons"


def personunit_shop(name: PersonName, person_dir: str = None) -> PersonUnit:
    if person_dir is None:
        person_dir = ""
    return PersonUnit(name=name, person_dir=person_dir)


#     world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
#     world_x._set_world_dirs()
#     return world_x
