from dataclasses import dataclass
from src.healing.healing import HealingUnit, HealingHandle, healingunit_shop
from src.world.pain import PainKind, PainUnit, PersonName, painunit_shop


@dataclass
class PersonUnit:
    name: PersonName = None
    person_dir: str = None
    _healings: dict[HealingHandle:HealingUnit] = None
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

    def set_healings_empty_if_none(self):
        if self._healings is None:
            self._healings = {}

    def set_healingunit(self, healing_handle: HealingHandle):
        healings_dir = f"{self.person_dir}/healings"
        self._healings[healing_handle] = healingunit_shop(
            handle=healing_handle, healings_dir=healings_dir
        )

    def get_healingunit(self, healing_handle: HealingHandle) -> HealingUnit:
        return self._healings.get(healing_handle)

    def del_healingunit(self, healing_handle: HealingHandle):
        self._healings.pop(healing_handle)

    def get_healings_dict(self) -> dict:
        return {healingunit_x.handle: None for healingunit_x in self._healings.values()}

    def get_pains_dict(self) -> dict:
        return {
            painunit_x.kind: painunit_x.get_dict()
            for painunit_x in self._pains.values()
        }

    def get_dict(self) -> dict:
        return {
            "name": self.name,
            "_healings": self.get_healings_dict(),
            "_pains": self.get_pains_dict(),
        }


def personunit_shop(name: PersonName, person_dir: str = None) -> PersonUnit:
    if person_dir is None:
        person_dir = ""
    person_x = PersonUnit(name=name, person_dir=person_dir)
    person_x.set_healings_empty_if_none()
    person_x.set_pains_empty_if_none()
    return person_x


#     world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
#     world_x._set_world_dirs()
#     return world_x
