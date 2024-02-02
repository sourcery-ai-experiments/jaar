from src._prime.road import (
    default_road_delimiter_if_none,
    EconomyID,
    PersonID,
    HealerID,
    validate_roadnode,
    PersonRoad,
    RoadUnit,
    RoadNode,
    get_single_roadnode,
    create_proad,
)
from src.agenda.agenda import AgendaUnit
from src.economy.economy import EconomyUnit, economyunit_shop
from src.world.problem import (
    ProblemID,
    ProblemUnit,
    problemunit_shop,
    HealerLink,
    healerlink_shop,
    economylink_shop,
    EconomyLink,
)
from src.tools.file import get_proad_dir
from dataclasses import dataclass


class InvalidEconomyException(Exception):
    pass


class PRoadFailureException(Exception):
    pass


@dataclass
class PersonUnit:
    person_id: PersonID = None
    person_dir: str = None
    _economys: dict[EconomyID:EconomyUnit] = None
    _problems: dict[ProblemID:ProblemUnit] = None
    _primary_contract_road: PersonRoad = None
    _primary_contract_active: bool = None
    _primary_contract_obj: AgendaUnit = None
    _road_delimiter: str = None

    def make_proad(
        self,
        problem_id: ProblemID = None,
        healer_id: HealerID = None,
        economy_id: EconomyID = None,
    ) -> RoadUnit:
        if problem_id != None:
            problem_id_text = f"proad: ProblemID '{problem_id}' does not exist."
            if self.problem_exists(problem_id) == False:
                raise PRoadFailureException(problem_id_text)

        if healer_id != None:
            healer_id_text = f"proad: HealerID '{healer_id}' does not exist."
            if self.healer_exists(healer_id) == False:
                raise PRoadFailureException(healer_id_text)

        if economy_id != None:
            economy_id_text = f"proad: EconomyID '{economy_id}' does not exist."
            if self.economylink_exists(economy_id) == False:
                raise PRoadFailureException(economy_id_text)

        return create_proad(
            person_id=self.person_id,
            problem_id=problem_id,
            healer_id=healer_id,
            economy_id=economy_id,
            delimiter=self._road_delimiter,
        )

    def _get_single_proad_node(
        self, x_road: PersonRoad, roadnode_type: RoadNode
    ) -> RoadNode:
        return get_single_roadnode(
            roadunit_type="PersonRoad",
            x_roadunit=x_road,
            roadnode_type=roadnode_type,
            delimiter=self._road_delimiter,
        )

    def healer_exists(self, healer_id: HealerID) -> bool:
        return any(
            x_problemunit.healer_exists(healer_id)
            for x_problemunit in self._problems.values()
        )

    def problem_exists(self, problem_id: ProblemID) -> bool:
        return self._problems.get(problem_id) != None

    def set_primary_contract_active(self, _primary_contract_active: bool):
        self._primary_contract_active = _primary_contract_active

    def is_primary_contract_road_valid(self) -> bool:
        return self._primary_contract_road != None

    def set_person_id(self, x_person_id: PersonID):
        self.person_id = validate_roadnode(x_person_id, self._road_delimiter)
        if self.person_dir is None:
            self.person_dir = f"/persons/{self.person_id}"

    def create_problemunit_from_problem_id(self, x_problem_id: ProblemID):
        self._problems[x_problem_id] = problemunit_shop(problem_id=x_problem_id)

    def set_problemunit(self, problemunit: ProblemUnit):
        self._problems[problemunit.problem_id] = problemunit

    def get_problem_obj(self, x_problem_id: ProblemID) -> ProblemUnit:
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
        x_healer_id: HealerID = None,
    ):
        if x_healer_id is None:
            x_healer_id = self.person_id

        if x_problem_id != None:
            self.create_problemunit_from_problem_id(x_problem_id)
            x_problemunit = self.get_problem_obj(x_problem_id)
            x_problemunit.set_healerlink(healerlink_shop(x_healer_id))
            x_healerlink = x_problemunit.get_healerlink(x_healer_id)
            x_healerlink.set_economylink(economylink_shop(economy_id))

        if self.economylink_exists(economy_id) == False:
            raise InvalidEconomyException(
                f"Cannot set_economyunit {economy_id} because no justifying problem exists."
            )

        if self.economyunit_exists(economy_id) == False or replace:
            x_economyunit = economyunit_shop(
                economy_id, _road_delimiter=self._road_delimiter
            )
            x_economyunit.set_proad_nodes(self.person_id, x_problem_id, x_healer_id)
            x_economyunit.economys_dir = get_proad_dir(
                self.make_proad(
                    x_economyunit._problem_id,
                    x_economyunit._healer_id,
                    x_economyunit.economy_id,
                )
            )
            self._economys[economy_id] = x_economyunit

        if self._primary_contract_road is None and len(self._economys) == 1:
            if x_problem_id is None:
                x_problem_id = list(self._problems.keys())[0]
            self._primary_contract_road = self.make_proad(
                x_problem_id, x_healer_id, economy_id
            )

    def economyunit_exists(self, economy_id: EconomyID) -> bool:
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

    def get_problemunits(self) -> dict[ProblemID:ProblemUnit]:
        return {
            self.make_proad(x_problem_id): x_problem_obj
            for x_problem_id, x_problem_obj in self._problems.items()
        }

    def get_healerlink_objs(self) -> dict[HealerID:HealerLink]:
        x_dict = {}
        for x_problemunit in self.get_problemunits().values():
            for x_key, x_obj in x_problemunit.get_healerlink_objs().items():
                x_dict[self.make_proad(x_problemunit.problem_id, x_key)] = x_obj
        return x_dict

    def get_economyslink_objs(self) -> dict[EconomyID:EconomyLink]:
        x_dict = {}
        for x_healerlink_proad, x_healerlink in self.get_healerlink_objs().items():
            x_problem_id = self._get_single_proad_node(x_healerlink_proad, "ProblemID")
            for x_key, x_obj in x_healerlink._economylinks.items():
                x_healer_id = x_healerlink.healer_id
                x_dict[self.make_proad(x_problem_id, x_healer_id, x_key)] = x_obj
        return x_dict

    def get_dict(self) -> dict[str:str]:
        return {
            "person_id": self.person_id,
            "person_dir": self.person_dir,
            "_economys": self.get_economys_dict(),
            "_primary_contract_road": self._primary_contract_road,
            "_primary_contract_active": self._primary_contract_active,
            "_problems": self.get_problems_dict(),
        }


def personunit_shop(
    person_id: PersonID,
    person_dir: str = None,
    _road_delimiter: str = None,
    _primary_contract_road: PersonRoad = None,
    _primary_contract_active: bool = None,
) -> PersonUnit:
    if _primary_contract_active is None:
        _primary_contract_active = True
    x_personunit = PersonUnit(
        person_dir=person_dir,
        _economys={},
        _problems={},
        _primary_contract_road=_primary_contract_road,
        _primary_contract_active=_primary_contract_active,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    x_personunit.set_person_id(person_id)
    return x_personunit


def get_from_json(x_person_json: str) -> PersonUnit:
    # return get_from_dict(x_get_dict(x_person_json))
    return None


def get_from_dict(person_dict: dict) -> PersonUnit:
    return None
