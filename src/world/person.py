from dataclasses import dataclass
from src.fix.fix import FixUnit, FixHandle, fixunit_shop
from src.world.pain import PainKind, PainUnit, PersonName, painunit_shop


@dataclass
class PersonUnit:
    name: PersonName = None
    person_dir: str = None
    _fixs: dict[FixHandle:FixUnit] = None
    _pains: dict[PainKind:PainUnit] = None

    def set_pains_empty_if_none(self):
        if self._pains is None:
            self._pains = {}

    def create_painunit_from_kind(self, pain_kind: PainKind):
        self._pains[pain_kind] = painunit_shop(kind=pain_kind)

    def set_painunit(self, painunit: PainUnit):
        self._pains[painunit.kind] = painunit

    def get_painunit(self, pain_kind: PainKind) -> PainUnit:
        return self._pains.get(pain_kind)

    def del_painunit(self, pain_kind: PainKind):
        self._pains.pop(pain_kind)

    def set_painunits_weight_metrics(self):
        total_painunits_weight = sum(
            x_painunit.weight for x_painunit in self._pains.values()
        )
        for x_painunit in self._pains.values():
            x_painunit.set_relative_weight(x_painunit.weight / total_painunits_weight)

    def set_fixunits_weight_metrics(self):
        self.set_painunits_weight_metrics()
        fixunit_handles = {x_fixunit.handle: 0 for x_fixunit in self._fixs.values()}

        for x_painunit in self._pains.values():
            for x_healerlink in x_painunit._healerlinks.values():
                for x_fixlink in x_healerlink._fixlinks.values():
                    fixunit_handles[x_fixlink.handle] += x_fixlink._person_importance

        for x_fixunit_handle, x_fixunit_person_importance in fixunit_handles.items():
            self._fixs.get(x_fixunit_handle).set_person_importance(
                x_fixunit_person_importance
            )

    def set_fixs_empty_if_none(self):
        if self._fixs is None:
            self._fixs = {}

    def set_fixunit(self, fix_handle: FixHandle):
        fixs_dir = f"{self.person_dir}/fixs"
        self._fixs[fix_handle] = fixunit_shop(handle=fix_handle, fixs_dir=fixs_dir)

    def get_fixunit(self, fix_handle: FixHandle) -> FixUnit:
        return self._fixs.get(fix_handle)

    def del_fixunit(self, fix_handle: FixHandle):
        self._fixs.pop(fix_handle)

    def get_fixs_dict(self) -> dict:
        return {fixunit_x.handle: None for fixunit_x in self._fixs.values()}

    def get_pains_dict(self) -> dict:
        return {
            painunit_x.kind: painunit_x.get_dict()
            for painunit_x in self._pains.values()
        }

    def get_dict(self) -> dict:
        return {
            "name": self.name,
            "_fixs": self.get_fixs_dict(),
            "_pains": self.get_pains_dict(),
        }


def personunit_shop(name: PersonName, person_dir: str = None) -> PersonUnit:
    if person_dir is None:
        person_dir = ""
    person_x = PersonUnit(name=name, person_dir=person_dir)
    person_x.set_fixs_empty_if_none()
    person_x.set_pains_empty_if_none()
    return person_x


#     world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
#     world_x._set_world_dirs()
#     return world_x
