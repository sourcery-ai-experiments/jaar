from dataclasses import dataclass
from src.healing.healing import HealingUnit, HealingHandle, healingunit_shop


@dataclass
class HealingLink:
    kind: HealingHandle
    weight: float

    def get_dict(self) -> dict:
        return {"kind": self.kind, "weight": self.weight}


def healinglink_shop(kind: HealingHandle, weight: float = None) -> HealingLink:
    if weight is None:
        weight = 1
    return HealingLink(kind=kind, weight=weight)


class PersonName(str):
    pass


@dataclass
class HealerLink:
    person_name: PersonName
    weight: float
    in_tribe: bool

    def get_dict(self):
        return {"person_name": self.person_name, "weight": self.weight}


def healerlink_shop(
    person_name: PersonName, weight: float = None, in_tribe: bool = None
) -> HealerLink:
    if weight is None:
        weight = 1

    return HealerLink(person_name=person_name, weight=weight, in_tribe=in_tribe)


class PainKind(str):
    pass


@dataclass
class PainUnit:
    kind: PainKind
    _healinglinks: dict[HealingHandle:HealingLink] = None
    _healerlinks: dict[PersonName:HealerLink] = None

    def set_healinglinks_empty_if_none(self):
        if self._healinglinks is None:
            self._healinglinks = {}

    def set_healinglink(self, healinglink: HealingLink):
        self._healinglinks[healinglink.kind] = healinglink

    def get_healinglink(self, healinghandle: HealingHandle) -> HealingLink:
        return self._healinglinks.get(healinghandle)

    def del_healinglink(self, healinghandle: HealingHandle):
        self._healinglinks.pop(healinghandle)

    def set_healerlinks_empty_if_none(self):
        if self._healerlinks is None:
            self._healerlinks = {}

    def set_healerlink(self, healerlink: HealerLink):
        self._healerlinks[healerlink.person_name] = healerlink

    def get_healerlink(self, person_name: PersonName) -> HealerLink:
        return self._healerlinks.get(person_name)

    def del_healerlink(self, person_name: PersonName):
        self._healerlinks.pop(person_name)

    def get_healinglinks_dict(self) -> dict:
        return {
            healinglink_x.kind: healinglink_x.get_dict()
            for healinglink_x in self._healinglinks.values()
        }

    def get_healerlinks_dict(self) -> dict:
        return {
            healerlink_x.person_name: healerlink_x.get_dict()
            for healerlink_x in self._healerlinks.values()
        }

    def get_dict(self):
        return {
            "kind": self.kind,
            "_healinglinks": self.get_healinglinks_dict(),
            "_healerlinks": self.get_healerlinks_dict(),
        }


def painunit_shop(kind: PainKind):
    pain_x = PainUnit(kind=kind)
    pain_x.set_healinglinks_empty_if_none()
    pain_x.set_healerlinks_empty_if_none()
    return pain_x
