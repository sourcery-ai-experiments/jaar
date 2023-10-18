from dataclasses import dataclass
from src.project.project import projectUnit, projectHandle, projectunit_shop
from src.world.pain import PainGenus, PainUnit, PersonName, painunit_shop


@dataclass
class PersonUnit:
    name: PersonName = None
    person_dir: str = None
    _projects: dict[projectHandle:projectUnit] = None
    _pains: dict[PainGenus:PainUnit] = None

    def set_pains_empty_if_none(self):
        if self._pains is None:
            self._pains = {}

    def create_painunit_from_genus(self, pain_genus: PainGenus):
        self._pains[pain_genus] = painunit_shop(genus=pain_genus)

    def set_painunit(self, painunit: PainUnit):
        self._pains[painunit.genus] = painunit

    def get_painunit(self, pain_genus: PainGenus) -> PainUnit:
        return self._pains.get(pain_genus)

    def del_painunit(self, pain_genus: PainGenus):
        self._pains.pop(pain_genus)

    def set_painunits_weight_metrics(self):
        total_painunits_weight = sum(
            x_painunit.weight for x_painunit in self._pains.values()
        )
        for x_painunit in self._pains.values():
            x_painunit.set_relative_weight(x_painunit.weight / total_painunits_weight)

    def set_projectunits_weight_metrics(self):
        self.set_painunits_weight_metrics()
        projectunit_handles = {
            x_projectunit.handle: 0 for x_projectunit in self._projects.values()
        }

        for x_painunit in self._pains.values():
            for x_healerlink in x_painunit._healerlinks.values():
                for x_projectlink in x_healerlink._projectlinks.values():
                    projectunit_handles[
                        x_projectlink.handle
                    ] += x_projectlink._person_importance

        for (
            x_projectunit_handle,
            x_projectunit_person_importance,
        ) in projectunit_handles.items():
            self._projects.get(x_projectunit_handle).set_person_importance(
                x_projectunit_person_importance
            )

    def set_projects_empty_if_none(self):
        if self._projects is None:
            self._projects = {}

    def set_projectunit(self, project_handle: projectHandle):
        projects_dir = f"{self.person_dir}/projects"
        self._projects[project_handle] = projectunit_shop(
            handle=project_handle, projects_dir=projects_dir
        )

    def get_projectunit(self, project_handle: projectHandle) -> projectUnit:
        return self._projects.get(project_handle)

    def del_projectunit(self, project_handle: projectHandle):
        self._projects.pop(project_handle)

    def get_projects_dict(self) -> dict:
        return {projectunit_x.handle: None for projectunit_x in self._projects.values()}

    def get_pains_dict(self) -> dict:
        return {
            painunit_x.genus: painunit_x.get_dict()
            for painunit_x in self._pains.values()
        }

    def get_dict(self) -> dict:
        return {
            "name": self.name,
            "_projects": self.get_projects_dict(),
            "_pains": self.get_pains_dict(),
        }


def personunit_shop(name: PersonName, person_dir: str = None) -> PersonUnit:
    if person_dir is None:
        person_dir = ""
    person_x = PersonUnit(name=name, person_dir=person_dir)
    person_x.set_projects_empty_if_none()
    person_x.set_pains_empty_if_none()
    return person_x


#     world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
#     world_x._set_world_dirs()
#     return world_x
