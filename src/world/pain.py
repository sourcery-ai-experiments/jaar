from dataclasses import dataclass
from src.project.project import ProjectHandle
from src.deal.deal import PersonName


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


def projectlink_shop(handle: ProjectHandle, weight: float = None) -> ProjectLink:
    if weight is None:
        weight = 1
    return ProjectLink(handle=handle, weight=weight)


@dataclass
class HealerLink:
    person_name: PersonName
    weight: float
    in_tribe: bool
    _projectlinks: dict[ProjectHandle:ProjectLink] = None
    _relative_weight: float = None
    _person_importance: float = None

    def set_projectlinks_weight_metrics(self):
        total_projectlinks_weight = sum(
            x_projectlink.weight for x_projectlink in self._projectlinks.values()
        )
        for x_projectlink in self._projectlinks.values():
            x_projectlink.set_relative_weight(
                x_projectlink.weight / total_projectlinks_weight
            )
            x_projectlink.set_person_importance(
                x_projectlink._relative_weight * self._person_importance
            )

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_person_importance(self, person_importance: float):
        self._person_importance = person_importance
        self.set_projectlinks_weight_metrics()

    def set_projectlinks_empty_if_none(self):
        if self._projectlinks is None:
            self._projectlinks = {}

    def set_projectlink(self, projectlink: ProjectLink):
        self._projectlinks[projectlink.handle] = projectlink

    def get_projectlink(self, projecthandle: ProjectHandle) -> ProjectLink:
        return self._projectlinks.get(projecthandle)

    def del_projectlink(self, projecthandle: ProjectHandle):
        self._projectlinks.pop(projecthandle)

    def get_projectlinks_dict(self) -> dict:
        return {
            projectlink_x.handle: projectlink_x.get_dict()
            for projectlink_x in self._projectlinks.values()
        }

    def get_dict(self):
        return {
            "person_name": self.person_name,
            "weight": self.weight,
            "_projectlinks": self.get_projectlinks_dict(),
        }


def healerlink_shop(
    person_name: PersonName, weight: float = None, in_tribe: bool = None
) -> HealerLink:
    if weight is None:
        weight = 1
    x_healer = HealerLink(person_name=person_name, weight=weight, in_tribe=in_tribe)
    x_healer.set_projectlinks_empty_if_none()
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
