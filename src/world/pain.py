from dataclasses import dataclass
from src.cure.cure import CureHandle
from src.pact.pact import PersonName


@dataclass
class CureLink:
    handle: CureHandle
    weight: float
    _relative_weight: float = None
    _person_importance: float = None

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_person_importance(self, person_importance: float):
        self._person_importance = person_importance

    def get_dict(self) -> dict:
        return {"handle": self.handle, "weight": self.weight}


def curelink_shop(handle: CureHandle, weight: float = None) -> CureLink:
    if weight is None:
        weight = 1
    return CureLink(handle=handle, weight=weight)


@dataclass
class HealerLink:
    person_name: PersonName
    weight: float
    in_tribe: bool
    _curelinks: dict[CureHandle:CureLink] = None
    _relative_weight: float = None
    _person_importance: float = None

    def set_curelinks_weight_metrics(self):
        total_curelinks_weight = sum(
            x_curelink.weight for x_curelink in self._curelinks.values()
        )
        for x_curelink in self._curelinks.values():
            x_curelink.set_relative_weight(x_curelink.weight / total_curelinks_weight)
            x_curelink.set_person_importance(
                x_curelink._relative_weight * self._person_importance
            )

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_person_importance(self, person_importance: float):
        self._person_importance = person_importance
        self.set_curelinks_weight_metrics()

    def set_curelinks_empty_if_none(self):
        if self._curelinks is None:
            self._curelinks = {}

    def set_curelink(self, curelink: CureLink):
        self._curelinks[curelink.handle] = curelink

    def get_curelink(self, curehandle: CureHandle) -> CureLink:
        return self._curelinks.get(curehandle)

    def del_curelink(self, curehandle: CureHandle):
        self._curelinks.pop(curehandle)

    def get_curelinks_dict(self) -> dict:
        return {
            curelink_x.handle: curelink_x.get_dict()
            for curelink_x in self._curelinks.values()
        }

    def get_dict(self):
        return {
            "person_name": self.person_name,
            "weight": self.weight,
            "_curelinks": self.get_curelinks_dict(),
        }


def healerlink_shop(
    person_name: PersonName, weight: float = None, in_tribe: bool = None
) -> HealerLink:
    if weight is None:
        weight = 1
    x_healer = HealerLink(person_name=person_name, weight=weight, in_tribe=in_tribe)
    x_healer.set_curelinks_empty_if_none()
    return x_healer


class PainKind(str):
    pass


@dataclass
class PainUnit:
    kind: PainKind
    weight: float = None
    _healerlinks: dict[PersonName:HealerLink] = None
    _relative_weight: float = None
    _person_importance: float = None

    def set_healerlinks_weight_metrics(self):
        total_healerlinks_weight = sum(
            x_healerlink.weight for x_healerlink in self._healerlinks.values()
        )

        for x_healerlink in self._healerlinks.values():
            x_healerlink.set_relative_weight(
                x_healerlink.weight / total_healerlinks_weight
            )
            x_healerlink.set_person_importance(
                x_healerlink._relative_weight * self._person_importance
            )

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight
        self.set_person_importance(self._relative_weight)

    def set_person_importance(self, person_importance: float):
        self._person_importance = person_importance
        self.set_healerlinks_weight_metrics()

    def set_healerlinks_empty_if_none(self):
        if self._healerlinks is None:
            self._healerlinks = {}

    def set_healerlink(self, healerlink: HealerLink):
        self._healerlinks[healerlink.person_name] = healerlink

    def get_healerlink(self, person_name: PersonName) -> HealerLink:
        return self._healerlinks.get(person_name)

    def del_healerlink(self, person_name: PersonName):
        self._healerlinks.pop(person_name)

    def get_healerlinks_dict(self) -> dict:
        return {
            healerlink_x.person_name: healerlink_x.get_dict()
            for healerlink_x in self._healerlinks.values()
        }

    def get_dict(self):
        return {
            "kind": self.kind,
            "weight": self.weight,
            "_healerlinks": self.get_healerlinks_dict(),
        }


def painunit_shop(kind: PainKind, weight: float = None) -> PainUnit:
    if weight is None:
        weight = 1
    pain_x = PainUnit(kind=kind, weight=weight)
    pain_x.set_healerlinks_empty_if_none()
    return pain_x
