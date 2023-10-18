from dataclasses import dataclass
from src.fix.fix import FixHandle
from src.deal.deal import PersonName


@dataclass
class FixLink:
    handle: FixHandle
    weight: float
    _relative_weight: float = None
    _person_importance: float = None

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_person_importance(self, person_importance: float):
        self._person_importance = person_importance

    def get_dict(self) -> dict:
        return {"handle": self.handle, "weight": self.weight}


def fixlink_shop(handle: FixHandle, weight: float = None) -> FixLink:
    if weight is None:
        weight = 1
    return FixLink(handle=handle, weight=weight)


@dataclass
class HealerLink:
    person_name: PersonName
    weight: float
    in_tribe: bool
    _fixlinks: dict[FixHandle:FixLink] = None
    _relative_weight: float = None
    _person_importance: float = None

    def set_fixlinks_weight_metrics(self):
        total_fixlinks_weight = sum(
            x_fixlink.weight for x_fixlink in self._fixlinks.values()
        )
        for x_fixlink in self._fixlinks.values():
            x_fixlink.set_relative_weight(x_fixlink.weight / total_fixlinks_weight)
            x_fixlink.set_person_importance(
                x_fixlink._relative_weight * self._person_importance
            )

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_person_importance(self, person_importance: float):
        self._person_importance = person_importance
        self.set_fixlinks_weight_metrics()

    def set_fixlinks_empty_if_none(self):
        if self._fixlinks is None:
            self._fixlinks = {}

    def set_fixlink(self, fixlink: FixLink):
        self._fixlinks[fixlink.handle] = fixlink

    def get_fixlink(self, fixhandle: FixHandle) -> FixLink:
        return self._fixlinks.get(fixhandle)

    def del_fixlink(self, fixhandle: FixHandle):
        self._fixlinks.pop(fixhandle)

    def get_fixlinks_dict(self) -> dict:
        return {
            fixlink_x.handle: fixlink_x.get_dict()
            for fixlink_x in self._fixlinks.values()
        }

    def get_dict(self):
        return {
            "person_name": self.person_name,
            "weight": self.weight,
            "_fixlinks": self.get_fixlinks_dict(),
        }


def healerlink_shop(
    person_name: PersonName, weight: float = None, in_tribe: bool = None
) -> HealerLink:
    if weight is None:
        weight = 1
    x_healer = HealerLink(person_name=person_name, weight=weight, in_tribe=in_tribe)
    x_healer.set_fixlinks_empty_if_none()
    return x_healer


class PainGenus(str):
    pass


@dataclass
class PainUnit:
    genus: PainGenus
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
            "genus": self.genus,
            "weight": self.weight,
            "_healerlinks": self.get_healerlinks_dict(),
        }


def painunit_shop(genus: PainGenus, weight: float = None) -> PainUnit:
    if weight is None:
        weight = 1
    pain_x = PainUnit(genus=genus, weight=weight)
    pain_x.set_healerlinks_empty_if_none()
    return pain_x
