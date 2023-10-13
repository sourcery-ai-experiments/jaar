from dataclasses import dataclass
from src.heal.heal import HealUnit, HealKind, healunit_shop


class PainKind(str):
    pass


@dataclass
class PainUnit:
    pass


class PersonName(str):
    pass


@dataclass
class PersonUnit:
    name: PersonName = None
    person_dir: str = None
    _heals: dict[HealKind:HealUnit] = None
    _pains: dict[PainKind:PainUnit] = None

    def set_heals_empty_if_none(self):
        if self._heals is None:
            self._heals = {}

    def set_pains_empty_if_none(self):
        if self._pains is None:
            self._pains = {}

    def create_heal(self, heal_kind: HealKind):
        heals_dir = f"{self.person_dir}/heals"
        self._heals[heal_kind] = healunit_shop(kind=heal_kind, heals_dir=heals_dir)

    def get_heal_obj(self, heal_kind: HealKind) -> HealUnit:
        return self._heals.get(heal_kind)


def personunit_shop(name: PersonName, person_dir: str = None) -> PersonUnit:
    if person_dir is None:
        person_dir = ""
    person_x = PersonUnit(name=name, person_dir=person_dir)
    person_x.set_heals_empty_if_none()
    person_x.set_pains_empty_if_none()
    return person_x


#     world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
#     world_x._set_world_dirs()
#     return world_x
