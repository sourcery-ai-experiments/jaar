from src._prime.road import (
    default_road_delimiter_if_none,
    MarketID,
    PersonID,
    HealerID,
    ProblemID,
    validate_roadnode,
    RoadUnit,
    RoadNode,
    get_all_road_nodes,
    get_terminus_node,
)
from src.world.examples.world_env_kit import get_test_worlds_dir, get_test_world_id
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as agenda_get_from_json,
)
from src.market.market import MarketUnit, marketunit_shop
from src.instrument.python import get_empty_dict_if_none
from src.instrument.file import (
    save_file,
    open_file,
    set_dir,
    get_directory_path,
)
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
    worlds_dir: str = None
    world_id: str = None
    persons_dir: str = None
    person_dir: str = None
    _markets_dir: str = None
    _gut_obj: AgendaUnit = None
    _gut_file_name: str = None
    _gut_path: str = None
    _market_objs: dict[RoadUnit:MarketUnit] = None
    _road_delimiter: str = None

    def set_person_id(self, x_person_id: PersonID):
        self.person_id = validate_roadnode(x_person_id, self._road_delimiter)
        if self.world_id is None:
            self.world_id = get_test_world_id()
        if self.worlds_dir is None:
            self.worlds_dir = get_test_worlds_dir()
        self.world_dir = f"{self.worlds_dir}/{self.world_id}"
        self.persons_dir = f"{self.world_dir}/persons"
        self.person_dir = f"{self.persons_dir}/{self.person_id}"
        self._markets_dir = f"{self.person_dir}/markets"
        if self._gut_file_name is None:
            self._gut_file_name = "gut.json"
        if self._gut_path is None:
            self._gut_path = f"{self.person_dir}/{self._gut_file_name}"

    def gut_file_exists(self) -> bool:
        return os_path_exists(self._gut_path)

    def _save_agenda_to_gut_path(self, x_agenda: AgendaUnit, replace: bool = True):
        if replace in {True, False}:
            save_file(
                dest_dir=self.person_dir,
                file_name=self._gut_file_name,
                file_text=x_agenda.get_json(),
                replace=replace,
            )

    def create_core_dir_and_files(self):
        set_dir(self.world_dir)
        set_dir(self.persons_dir)
        set_dir(self.person_dir)
        set_dir(self._markets_dir)
        self.create_gut_file_if_does_not_exist()

    def create_gut_file_if_does_not_exist(self):
        if self.gut_file_exists() == False:
            self._save_agenda_to_gut_path(
                agendaunit_shop(
                    _agent_id=self.person_id,
                    _world_id=self.world_id,
                    _road_delimiter=self._road_delimiter,
                )
            )

    def get_gut_file_agenda(self) -> AgendaUnit:
        gut_json = open_file(dest_dir=self.person_dir, file_name=self._gut_file_name)
        return agenda_get_from_json(gut_json)

    def load_gut_file(self):
        self._gut_obj = self.get_gut_file_agenda()

    def _get_market_path(self, x_list: list[RoadNode]) -> str:
        idearoot_list = ["idearoot", *x_list]
        return f"{self._markets_dir}{get_directory_path(x_list=idearoot_list)}"

    def _create_market_dir(self, x_roadunit: RoadUnit) -> str:
        road_nodes = get_all_road_nodes(x_roadunit, delimiter=self._road_delimiter)
        x_market_path = self._get_market_path(road_nodes)
        set_dir(x_market_path)
        return x_market_path

    def _create_marketunit(self, x_roadunit: RoadUnit):
        x_market_path = self._create_market_dir(x_roadunit)
        terminus_node = get_terminus_node(x_roadunit, delimiter=self._road_delimiter)
        x_marketunit = marketunit_shop(
            market_id=terminus_node,
            market_dir=x_market_path,
            _manager_person_id=self.person_id,
            _road_delimiter=self._road_delimiter,
        )
        x_marketunit.set_market_dirs()
        self._market_objs[x_roadunit] = x_marketunit

        # set manager_person_id contract

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
    world_id: str = None,
    worlds_dir: str = None,
    _market_objs: dict[RoadUnit:MarketUnit] = None,
    _road_delimiter: str = None,
) -> PersonUnit:
    x_personunit = PersonUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        _market_objs=get_empty_dict_if_none(_market_objs),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    x_personunit.set_person_id(person_id)
    return x_personunit


def get_from_json(x_person_json: str) -> PersonUnit:
    return None


def get_from_dict(person_dict: dict) -> PersonUnit:
    return None
