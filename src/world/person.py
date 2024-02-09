from src._prime.road import (
    default_road_delimiter_if_none,
    MarketID,
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
from src.market.market import MarketUnit, marketunit_shop
from src.world.problem import (
    ProblemID,
    ProblemUnit,
    problemunit_shop,
    HealerLink,
    healerlink_shop,
    marketlink_shop,
    MarketLink,
)
from src.instrument.file import get_proad_dir
from dataclasses import dataclass
from plotly.express import treemap, Constant
from pandas import DataFrame
from numpy import average


class InvalidMarketException(Exception):
    pass


class PRoadFailureException(Exception):
    pass


@dataclass
class ProblemBeam:
    person_id: str = None
    healer_id: str = None
    healer_weight: int = None
    healer_relative_weight: float = None
    healer_person_clout: float = None
    problem_id: str = None
    problem_weight: int = None
    problem_relative_weight: float = None
    problem_person_clout: float = None
    market_id: str = None
    market_weight: int = None
    market_relative_weight: float = None
    market_person_clout: float = None
    _road_delimiter: str = None
    _proad: PersonRoad = None

    def set_proad(self):
        self._proad = create_proad(
            person_id=self.person_id,
            problem_id=self.problem_id,
            healer_id=self.healer_id,
            market_id=self.market_id,
            delimiter=self._road_delimiter,
        )


def problembeam_shop(
    person_id: str = None,
    healer_id: str = None,
    healer_weight: int = None,
    healer_relative_weight: float = None,
    healer_person_clout: float = None,
    problem_id: str = None,
    problem_weight: int = None,
    problem_relative_weight: float = None,
    problem_person_clout: float = None,
    market_id: str = None,
    market_weight: int = None,
    market_relative_weight: float = None,
    market_person_clout: float = None,
    _road_delimiter: str = None,
):
    x_problembeam = ProblemBeam(
        person_id=person_id,
        healer_id=healer_id,
        healer_weight=healer_weight,
        healer_relative_weight=healer_relative_weight,
        healer_person_clout=healer_person_clout,
        problem_id=problem_id,
        problem_weight=problem_weight,
        problem_relative_weight=problem_relative_weight,
        problem_person_clout=problem_person_clout,
        market_id=market_id,
        market_weight=market_weight,
        market_relative_weight=market_relative_weight,
        market_person_clout=market_person_clout,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    x_problembeam.set_proad()
    return x_problembeam


@dataclass
class MarketMetric:
    market_id: MarketID
    _person_clout: float = None

    def add_person_clout(self, x_float: float):
        self._person_clout += x_float

    def clear_person_clout(self):
        self._person_clout = 0


def marketmetric_shop(market_id: str = None):
    x_marketmetric = MarketMetric(market_id)
    x_marketmetric._person_clout = 0
    return x_marketmetric


@dataclass
class PersonUnit:
    person_id: PersonID = None
    person_dir: str = None
    _markets: dict[MarketID:MarketUnit] = None
    _market_metrics: dict[MarketID:MarketUnit] = None
    _problembeams: dict[PersonRoad:ProblemBeam] = None
    _problems: dict[ProblemID:ProblemUnit] = None
    _road_delimiter: str = None

    def make_proad(
        self,
        problem_id: ProblemID = None,
        healer_id: HealerID = None,
        market_id: MarketID = None,
    ) -> RoadUnit:
        if problem_id != None:
            problem_id_text = f"proad: ProblemID '{problem_id}' does not exist."
            if self.problem_exists(problem_id) == False:
                raise PRoadFailureException(problem_id_text)

        if healer_id != None:
            healer_id_text = f"proad: HealerID '{healer_id}' does not exist."
            if self.healer_exists(healer_id) == False:
                raise PRoadFailureException(healer_id_text)

        if market_id != None:
            market_id_text = f"proad: MarketID '{market_id}' does not exist."
            if self.marketlink_exists(market_id) == False:
                raise PRoadFailureException(market_id_text)

        return create_proad(
            person_id=self.person_id,
            problem_id=problem_id,
            healer_id=healer_id,
            market_id=market_id,
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

    def set_person_metrics(self):
        total_problemunits_weight = sum(
            x_problemunit.weight for x_problemunit in self._problems.values()
        )
        for x_problemunit in self._problems.values():
            x_problemunit.set_relative_weight(
                x_problemunit.weight / total_problemunits_weight
            )
        self._set_problembeams()
        self._set_market_metrics()

    def _set_problembeams(self):
        self._problembeams = {}
        for x_problemunit in self.get_problemunits().values():
            for x_healerlink in x_problemunit.get_healerlink_objs().values():
                for x_marketlink in x_healerlink._marketlinks.values():
                    x_problembeam = problembeam_shop(
                        person_id=self.person_id,
                        problem_id=x_problemunit.problem_id,
                        problem_weight=x_problemunit.weight,
                        problem_relative_weight=x_problemunit._relative_weight,
                        problem_person_clout=x_problemunit._person_clout,
                        healer_id=x_healerlink.healer_id,
                        healer_weight=x_healerlink.weight,
                        healer_relative_weight=x_healerlink._relative_weight,
                        healer_person_clout=x_healerlink._person_clout,
                        market_id=x_marketlink.market_id,
                        market_weight=x_marketlink.weight,
                        market_relative_weight=x_marketlink._relative_weight,
                        market_person_clout=x_marketlink._person_clout,
                        _road_delimiter=self._road_delimiter,
                    )
                    x_problembeam.set_proad()
                    self._problembeams[x_problembeam._proad] = x_problembeam

    def _set_market_metrics(self):
        self._clear_marketmetrics()

        for x_problembeam in self._problembeams.values():
            if self._market_metrics.get(x_problembeam.market_id) is None:
                self._market_metrics[x_problembeam.market_id] = marketmetric_shop(
                    x_problembeam.market_id
                )
            x_marketmetric = self._market_metrics.get(x_problembeam.market_id)
            print(f"{x_marketmetric._person_clout=}")
            x_marketmetric.add_person_clout(x_problembeam.market_person_clout)
            print(f"{x_marketmetric._person_clout=}")

    def _clear_marketmetrics(self):
        for x_marketmetric in self._market_metrics.values():
            x_marketmetric.clear_person_clout()

    def marketlink_exists(self, market_id: MarketID) -> bool:
        return any(
            x_problemunit.marketlink_exists(market_id)
            for x_problemunit in self._problems.values()
        )

    def all_marketunits_linked_to_problem(self) -> bool:
        return all(
            self.marketlink_exists(x_market_id) != False
            for x_market_id in self._markets.keys()
        )

    def set_marketunit(
        self,
        market_id: MarketID,
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
            x_healerlink.set_marketlink(marketlink_shop(market_id))

        if self.marketlink_exists(market_id) == False:
            raise InvalidMarketException(
                f"Cannot set_marketunit {market_id} because no justifying problem exists."
            )

        if self.marketunit_exists(market_id) == False or replace:
            x_marketunit = marketunit_shop(
                market_id, _road_delimiter=self._road_delimiter
            )
            x_marketunit.set_proad_nodes(self.person_id, x_problem_id, x_healer_id)
            x_marketunit.markets_dir = get_proad_dir(
                self.make_proad(
                    x_marketunit._problem_id,
                    x_marketunit._healer_id,
                    x_marketunit.market_id,
                )
            )
            self._markets[market_id] = x_marketunit

    def marketunit_exists(self, market_id: MarketID) -> bool:
        return self._markets.get(market_id) != None

    def get_marketunit(self, market_id: MarketID) -> MarketUnit:
        return self._markets.get(market_id)

    def del_marketunit(self, market_id: MarketID):
        self._markets.pop(market_id)

    def get_markets_dict(self) -> dict:
        return {
            marketunit_x.market_id: None for marketunit_x in self._markets.values()
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

    def get_marketslink_objs(self) -> dict[MarketID:MarketLink]:
        x_dict = {}
        for x_healerlink_proad, x_healerlink in self.get_healerlink_objs().items():
            x_problem_id = self._get_single_proad_node(x_healerlink_proad, "ProblemID")
            for x_key, x_obj in x_healerlink._marketlinks.items():
                x_healer_id = x_healerlink.healer_id
                x_dict[self.make_proad(x_problem_id, x_healer_id, x_key)] = x_obj
        return x_dict

    def get_dict(self) -> dict[str:str]:
        return {
            "person_id": self.person_id,
            "person_dir": self.person_dir,
            "_markets": self.get_markets_dict(),
            "_problems": self.get_problems_dict(),
        }

    def popup_visualization(
        self, marketlink_by_problem: bool = False, show_fig: bool = True
    ):
        if marketlink_by_problem:
            # grab all marketlink data
            el_data = []

            for x_problemunit in self.get_problemunits().values():
                for x_healerlink in x_problemunit.get_healerlink_objs().values():
                    el_data.extend(
                        [
                            self.person_id,
                            x_problemunit.problem_id,
                            x_problemunit.weight,
                            x_healerlink.healer_id,
                            x_healerlink.weight,
                            x_marketlink.market_id,
                            x_marketlink.weight,
                        ]
                        for x_marketlink in x_healerlink._marketlinks.values()
                    )
            # initialize list of lists

            # Create the pandas DataFrame
            df = DataFrame(
                el_data,
                columns=[
                    "PersonID",
                    "ProblemID",
                    "Problem Weight",
                    "HealerID",
                    "Healer Weight",
                    "MarketID",
                    "Market Weight",
                ],
            )
            fig = treemap(
                df,
                path=[Constant("PersonID"), "ProblemID", "HealerID", "MarketID"],
                values="Market Weight",
                # color="lifeExp",
                # hover_data=["iso_alpha"],
                # color_continuous_scale="RdBu",
                # color_continuous_midpoint=average(df["Market Weight"], weights=df["pop"]),
            )
            fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
            if show_fig:
                fig.show()


def personunit_shop(
    person_id: PersonID,
    person_dir: str = None,
    _road_delimiter: str = None,
) -> PersonUnit:
    x_personunit = PersonUnit(
        person_dir=person_dir,
        _markets={},
        _market_metrics={},
        _problems={},
        _problembeams={},
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    x_personunit.set_person_id(person_id)
    return x_personunit


def get_from_json(x_person_json: str) -> PersonUnit:
    # return get_from_dict(x_get_dict(x_person_json))
    return None


def get_from_dict(person_dict: dict) -> PersonUnit:
    return None
