from dataclasses import dataclass
from src.heal.heal import HealUnit, HealKind, healunit_shop
from src.world.pain import PainKind, PainUnit, PersonName, painunit_shop


@dataclass
class PersonUnit:
    name: PersonName = None
    person_dir: str = None
    _heals: dict[HealKind:HealUnit] = None
    _pains: dict[PainKind:PainUnit] = None

    def set_pains_empty_if_none(self):
        if self._pains is None:
            self._pains = {}

    def set_painunit(self, pain_kind: PainKind):
        self._pains[pain_kind] = painunit_shop(kind=pain_kind)

    def get_painunit(self, pain_kind: PainKind) -> PainUnit:
        return self._pains.get(pain_kind)

    def del_painunit(self, pain_kind: PainKind):
        self._pains.pop(pain_kind)

    def set_heals_empty_if_none(self):
        if self._heals is None:
            self._heals = {}

    def set_healunit(self, heal_kind: HealKind):
        heals_dir = f"{self.person_dir}/heals"
        self._heals[heal_kind] = healunit_shop(kind=heal_kind, heals_dir=heals_dir)

    def get_healunit(self, heal_kind: HealKind) -> HealUnit:
        return self._heals.get(heal_kind)

    def del_healunit(self, heal_kind: HealKind):
        self._heals.pop(heal_kind)

    def get_heals_dict(self) -> dict:
        return {healunit_x.kind: None for healunit_x in self._heals.values()}

    def get_pains_dict(self) -> dict:
        return {
            painunit_x.kind: painunit_x.get_dict()
            for painunit_x in self._pains.values()
        }

    def get_dict(self) -> dict:
        return {
            "name": self.name,
            "_heals": self.get_heals_dict(),
            "_pains": self.get_pains_dict(),
        }


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
