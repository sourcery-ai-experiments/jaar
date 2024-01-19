from src._prime.road import (
    default_road_delimiter_if_none,
    EconomyID,
    PersonID,
    EconomyAddress,
    create_economyaddress,
)
from dataclasses import dataclass
from src.economy.economy import EconomyUnit, economyunit_shop
from src.world.problem import (
    ProblemID,
    ProblemUnit,
    problemunit_shop,
    healerlink_shop,
    economylink_shop,
)


class InvalidEconomyException(Exception):
    pass


@dataclass
class PersonUnit:
    pid: PersonID = None
    person_dir: str = None
    _economys: dict[EconomyID:EconomyUnit] = None
    _problems: dict[ProblemID:ProblemUnit] = None
    _road_delimiter: str = None

    def create_problemunit_from_problem_id(self, x_problem_id: ProblemID):
        self._problems[x_problem_id] = problemunit_shop(problem_id=x_problem_id)

    def set_problemunit(self, problemunit: ProblemUnit):
        self._problems[problemunit.problem_id] = problemunit

    def get_problemunit(self, x_problem_id: ProblemID) -> ProblemUnit:
        return self._problems.get(x_problem_id)

    def del_problemunit(self, x_problem_id: ProblemID):
        self._problems.pop(x_problem_id)

    def set_problemunits_weight_metrics(self):
        total_problemunits_weight = sum(
            x_problemunit.weight for x_problemunit in self._problems.values()
        )
        for x_problemunit in self._problems.values():
            x_problemunit.set_relative_weight(
                x_problemunit.weight / total_problemunits_weight
            )

    def economylink_exists(self, economy_id: EconomyID) -> bool:
        return any(
            x_problemunit.economylink_exists(economy_id)
            for x_problemunit in self._problems.values()
        )

    def all_economyunits_linked_to_problem(self) -> bool:
        return all(
            self.economylink_exists(x_economy_id) != False
            for x_economy_id in self._economys.keys()
        )

    def set_economyunit(
        self,
        economy_id: EconomyID,
        replace: bool = False,
        x_problem_id: ProblemID = None,
    ):
        if x_problem_id != None:
            self.create_problemunit_from_problem_id(x_problem_id)
            x_problemunit = self.get_problemunit(x_problem_id)
            x_problemunit.set_healerlink(healerlink_shop(self.pid))
            xao_healerlink = x_problemunit.get_healerlink(self.pid)
            xao_healerlink.set_economylink(economylink_shop(economy_id))

        if self.economylink_exists(economy_id) == False:
            raise InvalidEconomyException(
                f"Cannot set_economyunit {economy_id} because no justifying problem exists."
            )

        if self.economyunit_exists(economy_id) == False or (
            self.economyunit_exists(economy_id) and replace
        ):
            economys_dir = f"{self.person_dir}/economys"
            self._economys[economy_id] = economyunit_shop(
                economy_id=economy_id,
                economys_dir=economys_dir,
                _manager_pid=self.pid,
                _road_delimiter=self._road_delimiter,
            )

    def get_economyaddress(self, economy_id: EconomyID) -> EconomyAddress:
        if self.economyunit_exists(economy_id) == False:
            raise InvalidEconomyException(
                f"Cannot get economyaddress for {self.pid} because economy {economy_id} does not exist"
            )

        return create_economyaddress(self.pid, economy_id, self._road_delimiter)

    def economyunit_exists(self, economy_id: EconomyID):
        return self._economys.get(economy_id) != None

    def get_economyunit(self, economy_id: EconomyID) -> EconomyUnit:
        return self._economys.get(economy_id)

    def del_economyunit(self, economy_id: EconomyID):
        self._economys.pop(economy_id)

    def get_economys_dict(self) -> dict:
        return {
            economyunit_x.economy_id: None for economyunit_x in self._economys.values()
        }

    def get_problems_dict(self) -> dict:
        return {
            problemunit_x.problem_id: problemunit_x.get_dict()
            for problemunit_x in self._problems.values()
        }

    def get_dict(self) -> dict:
        return {
            "pid": self.pid,
            "_economys": self.get_economys_dict(),
            "_problems": self.get_problems_dict(),
        }


def personunit_shop(
    pid: PersonID, person_dir: str = None, _road_delimiter: str = None
) -> PersonUnit:
    if person_dir is None:
        person_dir = ""
    return PersonUnit(
        pid=pid,
        person_dir=person_dir,
        _economys={},
        _problems={},
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )


#     world_x = WorldUnit(mark=mark, worlds_dir=worlds_dir)
#     world_x._set_world_dirs()
#     return world_x
