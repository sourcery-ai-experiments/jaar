from dataclasses import dataclass
from src.culture.culture import CultureTitle
from src.agenda.agenda import PersonPID


@dataclass
class CultureLink:
    title: CultureTitle
    weight: float
    _relative_weight: float = None
    _manager_importance: float = None

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_manager_importance(self, person_importance: float):
        self._manager_importance = person_importance

    def get_dict(self) -> dict:
        return {"title": self.title, "weight": self.weight}


def culturelink_shop(title: CultureTitle, weight: float = None) -> CultureLink:
    if weight is None:
        weight = 1
    return CultureLink(title=title, weight=weight)


@dataclass
class HealerLink:
    person_pid: PersonPID
    weight: float
    in_tribe: bool
    _culturelinks: dict[CultureTitle:CultureLink] = None
    _relative_weight: float = None
    _manager_importance: float = None

    def set_culturelinks_weight_metrics(self):
        total_culturelinks_weight = sum(
            x_culturelink.weight for x_culturelink in self._culturelinks.values()
        )
        for x_culturelink in self._culturelinks.values():
            x_culturelink.set_relative_weight(
                x_culturelink.weight / total_culturelinks_weight
            )
            x_culturelink.set_manager_importance(
                x_culturelink._relative_weight * self._manager_importance
            )

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_manager_importance(self, person_importance: float):
        self._manager_importance = person_importance
        self.set_culturelinks_weight_metrics()

    def set_culturelinks_empty_if_none(self):
        if self._culturelinks is None:
            self._culturelinks = {}

    def set_culturelink(self, culturelink: CultureLink):
        self._culturelinks[culturelink.title] = culturelink

    def get_culturelink(self, culturetitle: CultureTitle) -> CultureLink:
        return self._culturelinks.get(culturetitle)

    def del_culturelink(self, culturetitle: CultureTitle):
        self._culturelinks.pop(culturetitle)

    def get_culturelinks_dict(self) -> dict:
        return {
            culturelink_x.title: culturelink_x.get_dict()
            for culturelink_x in self._culturelinks.values()
        }

    def get_dict(self):
        return {
            "person_pid": self.person_pid,
            "weight": self.weight,
            "_culturelinks": self.get_culturelinks_dict(),
        }


def healerlink_shop(
    person_pid: PersonPID, weight: float = None, in_tribe: bool = None
) -> HealerLink:
    if weight is None:
        weight = 1
    x_healer = HealerLink(person_pid=person_pid, weight=weight, in_tribe=in_tribe)
    x_healer.set_culturelinks_empty_if_none()
    return x_healer


class PainGenus(str):  # Created to help track the concept
    pass


@dataclass
class PainUnit:
    genus: PainGenus
    weight: float = None
    _healerlinks: dict[PersonPID:HealerLink] = None
    _relative_weight: float = None
    _manager_importance: float = None

    def set_healerlinks_weight_metrics(self):
        total_healerlinks_weight = sum(
            x_healerlink.weight for x_healerlink in self._healerlinks.values()
        )

        for x_healerlink in self._healerlinks.values():
            x_healerlink.set_relative_weight(
                x_healerlink.weight / total_healerlinks_weight
            )
            x_healerlink.set_manager_importance(
                x_healerlink._relative_weight * self._manager_importance
            )

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight
        self.set_manager_importance(self._relative_weight)

    def set_manager_importance(self, person_importance: float):
        self._manager_importance = person_importance
        self.set_healerlinks_weight_metrics()

    def set_healerlinks_empty_if_none(self):
        if self._healerlinks is None:
            self._healerlinks = {}

    def set_healerlink(self, healerlink: HealerLink):
        self._healerlinks[healerlink.person_pid] = healerlink

    def get_healerlink(self, person_pid: PersonPID) -> HealerLink:
        return self._healerlinks.get(person_pid)

    def del_healerlink(self, person_pid: PersonPID):
        self._healerlinks.pop(person_pid)

    def get_healerlinks_dict(self) -> dict:
        return {
            healerlink_x.person_pid: healerlink_x.get_dict()
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
