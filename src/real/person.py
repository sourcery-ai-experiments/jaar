from src._instrument.python import get_empty_dict_if_none
from src._instrument.file import (
    set_dir,
    get_directory_path,
    get_all_dirs_with_file,
    get_parts_dir,
    delete_dir,
)
from src._road.finance import default_planck_if_none
from src._road.road import (
    default_road_delimiter_if_none,
    PersonID,
    RoadUnit,
    RoadNode,
    get_all_road_nodes,
    change_road,
    create_road_from_nodes,
)
from src.agenda.agenda import AgendaUnit
from src.econ.econ import (
    EconUnit,
    econunit_shop,
    treasury_db_filename,
    get_rootpart_of_econ_dir,
)
from src.real.nook import (
    NookUnit,
    get_duty_file_agenda,
    nookunit_shop,
    nookunit_create_core_dir_and_files,
)
from dataclasses import dataclass


class InvalidEconException(Exception):
    pass


class PersonCreateEconUnitsException(Exception):
    pass


@dataclass
class PersonUnit:
    nook: NookUnit = None
    _duty_obj: AgendaUnit = None
    _work_obj: AgendaUnit = None
    _econ_objs: dict[RoadUnit:EconUnit] = None

    def _get_person_econ_dir(self, x_list: list[RoadNode]) -> str:
        return f"{self.nook._econs_dir}{get_directory_path(x_list=[*x_list])}"

    def _create_econ_dir(self, x_roadunit: RoadUnit) -> str:
        econ_root = get_rootpart_of_econ_dir()
        x_roadunit = change_road(x_roadunit, self.nook.real_id, econ_root)
        road_nodes = get_all_road_nodes(x_roadunit, self.nook._road_delimiter)
        x_econ_path = self._get_person_econ_dir(road_nodes)
        set_dir(x_econ_path)
        return x_econ_path

    def _create_econunit(self, econ_roadunit: RoadUnit):
        x_econ_path = self._create_econ_dir(econ_roadunit)
        x_econunit = econunit_shop(
            real_id=self.nook.real_id,
            econ_dir=x_econ_path,
            _manager_person_id=self.nook.person_id,
            _road_delimiter=self.nook._road_delimiter,
        )
        x_econunit.set_econ_dirs()
        self._econ_objs[econ_roadunit] = x_econunit

    def create_person_econunits(self, econ_exceptions: bool = True):
        x_duty_agenda = get_duty_file_agenda(self.nook)
        x_duty_agenda.calc_agenda_metrics(econ_exceptions)
        if x_duty_agenda._econs_justified == False:
            raise PersonCreateEconUnitsException(
                f"Cannot set '{self.nook.person_id}' duty agenda econunits because 'AgendaUnit._econs_justified' is False."
            )
        if x_duty_agenda._econs_buildable == False:
            raise PersonCreateEconUnitsException(
                f"Cannot set '{self.nook.person_id}' duty agenda econunits because 'AgendaUnit._econs_buildable' is False."
            )

        x_person_econs = x_duty_agenda._healers_dict.get(self.nook.person_id)
        x_person_econs = get_empty_dict_if_none(x_person_econs)
        self._econ_objs = {}
        for econ_idea in x_person_econs.values():
            self._create_econunit(econ_roadunit=econ_idea.get_road())

        # delete any
        x_treasury_dirs = get_all_dirs_with_file(
            treasury_db_filename(), self.nook._econs_dir
        )
        for treasury_dir in x_treasury_dirs:
            treasury_road = create_road_from_nodes(get_parts_dir(treasury_dir))
            treasury_road = change_road(
                treasury_road, get_rootpart_of_econ_dir(), self.nook.real_id
            )
            if x_person_econs.get(treasury_road) is None:
                dir_to_delete = f"{self.nook._econs_dir}/{treasury_dir}"
                delete_dir(dir_to_delete)

    def get_econ(self, econ_road: RoadUnit) -> EconUnit:
        return self._econ_objs.get(econ_road)

    def set_econunit_role(self, econ_road: RoadUnit, role: AgendaUnit):
        x_econ = self.get_econ(econ_road)
        x_econ.save_role_file(role)

    def set_econunits_role(self, role: AgendaUnit):
        for x_econ_road in self._econ_objs.keys():
            self.set_econunit_role(x_econ_road, role)

    def set_person_econunits_role(self):
        self.set_econunits_role(self._duty_obj)


def personunit_shop(
    person_id: PersonID,
    real_id: str = None,
    reals_dir: str = None,
    _econ_objs: dict[RoadUnit:EconUnit] = None,
    _road_delimiter: str = None,
    _planck: float = None,
    create_files: bool = True,
) -> PersonUnit:
    x_nookunit = nookunit_shop(
        reals_dir=reals_dir,
        real_id=real_id,
        person_id=person_id,
        road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        planck=default_planck_if_none(_planck),
    )
    x_personunit = PersonUnit(x_nookunit, _econ_objs=get_empty_dict_if_none(_econ_objs))
    if create_files:
        nookunit_create_core_dir_and_files(x_nookunit)
        x_personunit._duty_obj = get_duty_file_agenda(x_nookunit)
    return x_personunit
