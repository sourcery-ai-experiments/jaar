from dataclasses import dataclass
from src.cure.cure import CureUnit, CureHandle, cureunit_shop


@dataclass
class CureLink:
    kind: CureHandle
    weight: float

    def get_dict(self) -> dict:
        return {"kind": self.kind, "weight": self.weight}


def curelink_shop(kind: CureHandle, weight: float = None) -> CureLink:
    if weight is None:
        weight = 1
    return CureLink(kind=kind, weight=weight)


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
    _curelinks: dict[CureHandle:CureLink] = None
    _healerlinks: dict[PersonName:HealerLink] = None

    def set_curelinks_empty_if_none(self):
        if self._curelinks is None:
            self._curelinks = {}

    def set_curelink(self, curelink: CureLink):
        self._curelinks[curelink.kind] = curelink

    def get_curelink(self, curehandle: CureHandle) -> CureLink:
        return self._curelinks.get(curehandle)

    def del_curelink(self, curehandle: CureHandle):
        self._curelinks.pop(curehandle)

    def set_healerlinks_empty_if_none(self):
        if self._healerlinks is None:
            self._healerlinks = {}

    def set_healerlink(self, healerlink: HealerLink):
        self._healerlinks[healerlink.person_name] = healerlink

    def get_healerlink(self, person_name: PersonName) -> HealerLink:
        return self._healerlinks.get(person_name)

    def del_healerlink(self, person_name: PersonName):
        self._healerlinks.pop(person_name)

    def get_curelinks_dict(self) -> dict:
        return {
            curelink_x.kind: curelink_x.get_dict()
            for curelink_x in self._curelinks.values()
        }

    def get_healerlinks_dict(self) -> dict:
        return {
            healerlink_x.person_name: healerlink_x.get_dict()
            for healerlink_x in self._healerlinks.values()
        }

    def get_dict(self):
        return {
            "kind": self.kind,
            "_curelinks": self.get_curelinks_dict(),
            "_healerlinks": self.get_healerlinks_dict(),
        }


def painunit_shop(kind: PainKind):
    pain_x = PainUnit(kind=kind)
    pain_x.set_curelinks_empty_if_none()
    pain_x.set_healerlinks_empty_if_none()
    return pain_x
