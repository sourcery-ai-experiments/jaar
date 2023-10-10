from dataclasses import dataclass
from src.economy.economy import EconomyUnit, EconomyTag, economyunit_shop


class PersonName(str):
    pass


@dataclass
class PersonUnit:
    name: PersonName = None
    person_dir: str = None
    _economys: dict[EconomyTag:EconomyUnit] = None

    def set_economys_empty_if_none(self):
        if self._economys is None:
            self._economys = {}

    def create_economy(self, economy_tag: EconomyTag):
        economys_dir = f"{self.person_dir}/economys"
        self._economys[economy_tag] = economyunit_shop(
            tag=economy_tag, economys_dir=economys_dir
        )

    def get_economy_obj(self, economy_tag: EconomyTag) -> EconomyUnit:
        return self._economys.get(economy_tag)


#     def _set_world_dirs(self):
#         self._persons_dir = f"{self.worlds_dir}/persons"


def personunit_shop(name: PersonName, person_dir: str = None) -> PersonUnit:
    if person_dir is None:
        person_dir = ""
    person_x = PersonUnit(name=name, person_dir=person_dir)
    person_x.set_economys_empty_if_none()
    return person_x


#     world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
#     world_x._set_world_dirs()
#     return world_x
