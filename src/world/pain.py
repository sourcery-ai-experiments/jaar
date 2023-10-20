from dataclasses import dataclass
from src.culture.culture import ProjectHandle
from src.agenda.agenda import PersonName


@dataclass
class ProjectLink:
    handle: ProjectHandle
    weight: float
    _relative_weight: float = None
    _person_importance: float = None

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_person_importance(self, person_importance: float):
        self._person_importance = person_importance

    def get_dict(self) -> dict:
        return {"handle": self.handle, "weight": self.weight}


def culturelink_shop(handle: ProjectHandle, weight: float = None) -> ProjectLink:
    if weight is None:
        weight = 1
    return ProjectLink(handle=handle, weight=weight)


@dataclass
class HealerLink:
    person_name: PersonName
    weight: float
    in_tribe: bool
    _culturelinks: dict[ProjectHandle:ProjectLink] = None
    _relative_weight: float = None
    _person_importance: float = None

    def set_culturelinks_weight_metrics(self):
        total_culturelinks_weight = sum(
            x_culturelink.weight for x_culturelink in self._culturelinks.values()
        )
        for x_culturelink in self._culturelinks.values():
            x_culturelink.set_relative_weight(
                x_culturelink.weight / total_culturelinks_weight
            )
            x_culturelink.set_person_importance(
                x_culturelink._relative_weight * self._person_importance
            )

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_person_importance(self, person_importance: float):
        self._person_importance = person_importance
        self.set_culturelinks_weight_metrics()

    def set_culturelinks_empty_if_none(self):
        if self._culturelinks is None:
            self._culturelinks = {}

    def set_culturelink(self, culturelink: ProjectLink):
        self._culturelinks[culturelink.handle] = culturelink

    def get_culturelink(self, culturehandle: ProjectHandle) -> ProjectLink:
        return self._culturelinks.get(culturehandle)

    def del_culturelink(self, culturehandle: ProjectHandle):
        self._culturelinks.pop(culturehandle)

    def get_culturelinks_dict(self) -> dict:
        return {
            culturelink_x.handle: culturelink_x.get_dict()
            for culturelink_x in self._culturelinks.values()
        }

    def get_dict(self):
        return {
            "person_name": self.person_name,
            "weight": self.weight,
            "_culturelinks": self.get_culturelinks_dict(),
        }


def healerlink_shop(
    person_name: PersonName, weight: float = None, in_tribe: bool = None
) -> HealerLink:
    if weight is None:
        weight = 1
    x_healer = HealerLink(person_name=person_name, weight=weight, in_tribe=in_tribe)
    x_healer.set_culturelinks_empty_if_none()
    return x_healer


class PainGenus(str):  # Created to help track the concept
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
