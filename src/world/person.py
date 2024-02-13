from src._prime.road import (
    default_road_delimiter_if_none,
    MarketID,
    PersonID,
    HealerID,
    ProblemID,
    validate_roadnode,
    PersonRoad,
    RoadUnit,
    RoadNode,
    get_single_roadnode,
)
from src.world.examples.world_env_kit import get_temp_world_dir
from src.agenda.agenda import AgendaUnit, agendaunit_shop
from src.market.market import MarketUnit
from src.instrument.file import save_file
from dataclasses import dataclass
from plotly.express import treemap, Constant
from pandas import DataFrame
from numpy import average
from os.path import exists as os_path_exists, isdir as os_path_isdir


class InvalidMarketException(Exception):
    pass


@dataclass
class PersonUnit:
    person_id: PersonID = None
    world_dir: str = None
    persons_dir: str = None
    person_dir: str = None
    _gut_obj: AgendaUnit = None
    _gut_file_name: str = None
    _gut_path: str = None
    _markets: dict[MarketID:MarketUnit] = None
    _market_metrics: dict[MarketID:MarketUnit] = None
    _problems: dict[ProblemID:] = None
    _road_delimiter: str = None

    def healer_exists(self, healer_id: HealerID) -> bool:
        return any(
            x_problemunit.healer_exists(healer_id)
            for x_problemunit in self._problems.values()
        )

    def problem_exists(self, problem_id: ProblemID) -> bool:
        return self._problems.get(problem_id) != None

    def set_person_id(self, x_person_id: PersonID):
        self.person_id = validate_roadnode(x_person_id, self._road_delimiter)
        if self.world_dir is None:
            self.world_dir = get_temp_world_dir()
        self.persons_dir = f"{self.world_dir}/persons"
        self.person_dir = f"{self.persons_dir}/{self.person_id}"
        if self._gut_file_name is None:
            self._gut_file_name = "gut.json"
        if self._gut_path is None:
            self._gut_path = f"{self.person_dir}/{self._gut_file_name}"

    def create_and_save_new_gut(self):
        gut_agenda = agendaunit_shop(_agent_id=self.person_id)
        save_file(
            dest_dir=self.person_dir,
            file_name=self._gut_file_name,
            file_text=gut_agenda.get_json(),
            replace=False,
        )

    # def _set_market_metrics(self):
    #     self._clear_marketmetrics()

    #     for x_problembeam in self._problembeams.values():
    #         if self._market_metrics.get(x_problembeam.market_id) is None:
    #             self._market_metrics[x_problembeam.market_id] = marketmetric_shop(
    #                 x_problembeam.market_id
    #             )
    #         x_marketmetric = self._market_metrics.get(x_problembeam.market_id)
    #         print(f"{x_marketmetric._person_clout=}")
    #         x_marketmetric.add_person_clout(x_problembeam.market_person_clout)
    #         print(f"{x_marketmetric._person_clout=}")

    def _clear_marketmetrics(self):
        for x_marketmetric in self._market_metrics.values():
            x_marketmetric.clear_person_clout()

    # def popup_visualization(
    #     self, marketlink_by_problem: bool = False, show_fig: bool = True
    # ):
    #     if marketlink_by_problem:
    #         # grab all marketlink data
    #         el_data = []

    #         for x_problemunit in self.get_problemunits().values():
    #                 el_data.extend(
    #                     [
    #                         self.person_id,
    #                         x_problemunit.problem_id,
    #                         x_problemunit.weight,
    #                         x_.healer_id,
    #                         x_.weight,
    #                         x_marketlink.market_id,
    #                         x_marketlink.weight,
    #                     ]
    #                     for x_marketlink in x_._marketlinks.values()
    #                 )
    #         # initialize list of lists

    #         # Create the pandas DataFrame
    #         df = DataFrame(
    #             el_data,
    #             columns=[
    #                 "PersonID",
    #                 "ProblemID",
    #                 "Problem Weight",
    #                 "HealerID",
    #                 "Healer Weight",
    #                 "MarketID",
    #                 "Market Weight",
    #             ],
    #         )
    #         fig = treemap(
    #             df,
    #             path=[Constant("PersonID"), "ProblemID", "HealerID", "MarketID"],
    #             values="Market Weight",
    #             # color="lifeExp",
    #             # hover_data=["iso_alpha"],
    #             # color_continuous_scale="RdBu",
    #             # color_continuous_midpoint=average(df["Market Weight"], weights=df["pop"]),
    #         )
    #         fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    #         if show_fig:
    #             fig.show()


def personunit_shop(
    person_id: PersonID,
    world_dir: str = None,
    _road_delimiter: str = None,
) -> PersonUnit:
    x_personunit = PersonUnit(
        world_dir=world_dir,
        _markets={},
        _market_metrics={},
        _problems={},
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    x_personunit.set_person_id(person_id)
    # if os_path_exists(x_personunit._gut_path) == False:
    x_personunit.create_and_save_new_gut()

    return x_personunit


def get_from_json(x_person_json: str) -> PersonUnit:
    # return get_from_dict(x_get_dict(x_person_json))
    return None


def get_from_dict(person_dict: dict) -> PersonUnit:
    return None
