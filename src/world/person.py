from dataclasses import dataclass
from src.cure.cure import CureUnit, CureHandle, cureunit_shop
from src.world.pain import PainKind, PainUnit, PersonName, painunit_shop


@dataclass
class PersonUnit:
    name: PersonName = None
    person_dir: str = None
    _cures: dict[CureHandle:CureUnit] = None
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

    def set_cures_empty_if_none(self):
        if self._cures is None:
            self._cures = {}

    def set_cureunit(self, cure_handle: CureHandle):
        cures_dir = f"{self.person_dir}/cures"
        self._cures[cure_handle] = cureunit_shop(
            handle=cure_handle, cures_dir=cures_dir
        )

    def get_cureunit(self, cure_handle: CureHandle) -> CureUnit:
        return self._cures.get(cure_handle)

    def del_cureunit(self, cure_handle: CureHandle):
        self._cures.pop(cure_handle)

    def get_cures_dict(self) -> dict:
        return {cureunit_x.handle: None for cureunit_x in self._cures.values()}

    def get_pains_dict(self) -> dict:
        return {
            painunit_x.kind: painunit_x.get_dict()
            for painunit_x in self._pains.values()
        }

    def get_dict(self) -> dict:
        return {
            "name": self.name,
            "_cures": self.get_cures_dict(),
            "_pains": self.get_pains_dict(),
        }


def personunit_shop(name: PersonName, person_dir: str = None) -> PersonUnit:
    if person_dir is None:
        person_dir = ""
    person_x = PersonUnit(name=name, person_dir=person_dir)
    person_x.set_cures_empty_if_none()
    person_x.set_pains_empty_if_none()
    return person_x


#     world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
#     world_x._set_world_dirs()
#     return world_x
