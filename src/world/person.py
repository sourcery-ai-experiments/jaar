from src._prime.road import (
    default_road_delimiter_if_none,
    PersonID,
    EconID,
    validate_roadnode,
    RoadUnit,
    RoadNode,
    get_all_road_nodes,
    get_terminus_node,
    change_road,
    create_road_from_nodes,
)
from src.world.examples.world_env_kit import get_test_worlds_dir, get_test_world_id
from src.agenda.agenda import (
    AgendaUnit,
    agendaunit_shop,
    get_from_json as agenda_get_from_json,
)
from src.econ.econ import EconUnit, econunit_shop, treasury_db_filename
from src.instrument.python import get_empty_dict_if_none
from src.instrument.file import (
    save_file,
    open_file,
    set_dir,
    get_directory_path,
    get_all_dirs_with_file,
    get_parts_dir,
    delete_dir,
)
from dataclasses import dataclass
from plotly.express import treemap, Constant
from pandas import DataFrame
from numpy import average
from os.path import exists as os_path_exists, isdir as os_path_isdir


class InvalidEconException(Exception):
    pass


class PersonCreateEconUnitsException(Exception):
    pass


@dataclass
class PersonUnit:
    person_id: PersonID = None
    worlds_dir: str = None
    world_id: str = None
    persons_dir: str = None
    person_dir: str = None
    _econs_dir: str = None
    _gut_obj: AgendaUnit = None
    _gut_file_name: str = None
    _gut_path: str = None
    _econ_objs: dict[RoadUnit:EconUnit] = None
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
        self._econs_dir = f"{self.person_dir}/econs"
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
        set_dir(self._econs_dir)
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

    def get_rootpart_of_econ_dir(self):
        return "idearoot"

    def load_gut_file(self):
        self._gut_obj = self.get_gut_file_agenda()

    def _get_person_econ_dir(self, x_list: list[RoadNode]) -> str:
        return f"{self._econs_dir}{get_directory_path(x_list=[*x_list])}"

    def _create_econ_dir(self, x_roadunit: RoadUnit) -> str:
        x_roadunit = change_road(
            x_roadunit, self.world_id, self.get_rootpart_of_econ_dir()
        )
        road_nodes = get_all_road_nodes(x_roadunit, delimiter=self._road_delimiter)
        x_econ_path = self._get_person_econ_dir(road_nodes)
        set_dir(x_econ_path)
        return x_econ_path

    def _create_econunit(self, econ_roadunit: RoadUnit):
        x_econ_path = self._create_econ_dir(econ_roadunit)
        x_econunit = econunit_shop(
            econ_id=get_terminus_node(econ_roadunit, delimiter=self._road_delimiter),
            econ_dir=x_econ_path,
            _manager_person_id=self.person_id,
            _road_delimiter=self._road_delimiter,
        )
        x_econunit.set_econ_dirs()
        self._econ_objs[econ_roadunit] = x_econunit

    def create_person_econunits(self, econ_exceptions: bool = True):
        x_gut_agenda = self.get_gut_file_agenda()
        x_gut_agenda.set_agenda_metrics(econ_exceptions)
        if x_gut_agenda._econs_justified == False:
            raise PersonCreateEconUnitsException(
                f"Cannot set '{self.person_id}' gut agenda econunits because 'AgendaUnit._econs_justified' is False."
            )
        if x_gut_agenda._econs_buildable == False:
            raise PersonCreateEconUnitsException(
                f"Cannot set '{self.person_id}' gut agenda econunits because 'AgendaUnit._econs_buildable' is False."
            )

        x_person_econs = x_gut_agenda._healers_dict.get(self.person_id)
        x_person_econs = get_empty_dict_if_none(x_person_econs)
        self._econ_objs = {}
        for econ_idea in x_person_econs.values():
            self._create_econunit(econ_roadunit=econ_idea.get_road())

        # delete any
        curr_treasury_dirs = get_all_dirs_with_file(
            treasury_db_filename(), self._econs_dir
        )
        for treasury_dir in curr_treasury_dirs:
            treasury_road = create_road_from_nodes(get_parts_dir(treasury_dir))
            treasury_road = change_road(
                treasury_road, self.get_rootpart_of_econ_dir(), self.world_id
            )
            if x_person_econs.get(treasury_road) is None:
                dir_to_delete = f"{self._econs_dir}/{treasury_dir}"
                delete_dir(dir_to_delete)

    def get_econ(self, econ_road: RoadUnit) -> EconUnit:
        return self._econ_objs.get(econ_road)

    def set_econunit_contract(self, econ_road: RoadUnit, contract: AgendaUnit):
        x_econ = self.get_econ(econ_road)
        if x_econ.clerkunit_exists(contract._agent_id) == False:
            x_econ.create_new_clerkunit(contract._agent_id)
        x_clerkunit = x_econ.get_clerkunit(contract._agent_id)
        x_clerkunit.set_contract(contract)

    def set_econunits_contract(self, contract: AgendaUnit):
        for x_econ_road in self._econ_objs.keys():
            self.set_econunit_contract(x_econ_road, contract)

    def set_person_econunits_contract(self):
        self.set_econunits_contract(self.get_gut_file_agenda())

    # def popup_visualization(
    #     self, econlink_by_problem: bool = False, show_fig: bool = True
    # ):
    #     if econlink_by_problem:
    #         # grab all econlink data
    #         el_data = []

    #         for x_problemunit in self.get_problemunits().values():
    #                 el_data.extend(
    #                     [
    #                         self.person_id,
    #                         x_problemunit.problem_id,
    #                         x_problemunit.weight,
    #                         x_.healer_id,
    #                         x_.weight,
    #                         x_econlink.econ_id,
    #                         x_econlink.weight,
    #                     ]
    #                     for x_econlink in x_._econlinks.values()
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
    #                 "EconID",
    #                 "Econ Weight",
    #             ],
    #         )
    #         fig = treemap(
    #             df,
    #             path=[Constant("PersonID"), "ProblemID", "HealerID", "EconID"],
    #             values="Econ Weight",
    #             # color="lifeExp",
    #             # hover_data=["iso_alpha"],
    #             # color_continuous_scale="RdBu",
    #             # color_continuous_midpoint=average(df["Econ Weight"], weights=df["pop"]),
    #         )
    #         fig.update_layout(margin=dict(t=50, l=25, r=25, b=25))
    #         if show_fig:
    #             fig.show()


def personunit_shop(
    person_id: PersonID,
    world_id: str = None,
    worlds_dir: str = None,
    _econ_objs: dict[RoadUnit:EconUnit] = None,
    _road_delimiter: str = None,
) -> PersonUnit:
    x_personunit = PersonUnit(
        world_id=world_id,
        worlds_dir=worlds_dir,
        _econ_objs=get_empty_dict_if_none(_econ_objs),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    x_personunit.set_person_id(person_id)
    return x_personunit


def get_from_json(x_person_json: str) -> PersonUnit:
    return None


def get_from_dict(person_dict: dict) -> PersonUnit:
    return None
