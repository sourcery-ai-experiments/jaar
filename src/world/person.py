from dataclasses import dataclass
from src.culture.culture import CultureUnit, CultureQID, cultureunit_shop
from src.world.pain import PainGenus, PainUnit, PersonID, painunit_shop


@dataclass
class PersonUnit:
    pid: PersonID = None
    person_dir: str = None
    _cultures: dict[CultureQID:CultureUnit] = None
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

    def set_cultures_empty_if_none(self):
        if self._cultures is None:
            self._cultures = {}

    def add_cultureunit(self, culture_qid: CultureQID):
        cultures_dir = f"{self.person_dir}/cultures"
        self._cultures[culture_qid] = cultureunit_shop(
            qid=culture_qid, cultures_dir=cultures_dir, _manager_pid=self.pid
        )

    def get_cultureunit(self, culture_qid: CultureQID) -> CultureUnit:
        return self._cultures.get(culture_qid)

    def del_cultureunit(self, culture_qid: CultureQID):
        self._cultures.pop(culture_qid)

    def get_cultures_dict(self) -> dict:
        return {cultureunit_x.qid: None for cultureunit_x in self._cultures.values()}

    def get_pains_dict(self) -> dict:
        return {
            painunit_x.genus: painunit_x.get_dict()
            for painunit_x in self._pains.values()
        }

    def get_dict(self) -> dict:
        return {
            "pid": self.pid,
            "_cultures": self.get_cultures_dict(),
            "_pains": self.get_pains_dict(),
        }


def personunit_shop(pid: PersonID, person_dir: str = None) -> PersonUnit:
    if person_dir is None:
        person_dir = ""
    x_person = PersonUnit(pid=pid, person_dir=person_dir)
    x_person.set_cultures_empty_if_none()
    x_person.set_pains_empty_if_none()
    return x_person


#     world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
#     world_x._set_world_dirs()
#     return world_x
