from dataclasses import dataclass
from src.economy.economy import EconomyUnit, EconomyQID, economyunit_shop
from src.world.pain import PainGenus, PainUnit, PersonID, painunit_shop


@dataclass
class PersonUnit:
    pid: PersonID = None
    person_dir: str = None
    _economys: dict[EconomyQID:EconomyUnit] = None
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

    def set_economys_empty_if_none(self):
        if self._economys is None:
            self._economys = {}

    def set_economyunit(self, economy_id: EconomyQID, replace: bool = False):
        if (self.economyunit_exists(economy_id) and replace) or self.economyunit_exists(
            economy_id
        ) == False:
            economys_dir = f"{self.person_dir}/economys"
            self._economys[economy_id] = economyunit_shop(
                economy_id=economy_id, economys_dir=economys_dir, _manager_pid=self.pid
            )

    def economyunit_exists(self, economy_id: EconomyQID):
        return self._economys.get(economy_id) != None

    def get_economyunit(self, economy_id: EconomyQID) -> EconomyUnit:
        return self._economys.get(economy_id)

    def del_economyunit(self, economy_id: EconomyQID):
        self._economys.pop(economy_id)

    def get_economys_dict(self) -> dict:
        return {
            economyunit_x.economy_id: None for economyunit_x in self._economys.values()
        }

    def get_pains_dict(self) -> dict:
        return {
            painunit_x.genus: painunit_x.get_dict()
            for painunit_x in self._pains.values()
        }

    def get_dict(self) -> dict:
        return {
            "pid": self.pid,
            "_economys": self.get_economys_dict(),
            "_pains": self.get_pains_dict(),
        }


def personunit_shop(pid: PersonID, person_dir: str = None) -> PersonUnit:
    if person_dir is None:
        person_dir = ""
    x_person = PersonUnit(pid=pid, person_dir=person_dir)
    x_person.set_economys_empty_if_none()
    x_person.set_pains_empty_if_none()
    return x_person


#     world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
#     world_x._set_world_dirs()
#     return world_x
