from src._instrument.file import (
    get_directory_path,
    save_file,
    open_file,
    delete_dir,
    dir_files,
    set_dir,
    get_integer_filenames,
)
from src._instrument.python import get_empty_set_if_none
from src._instrument.sqlite import sqlite_connection
from src._road.jaar_config import (
    roles_str,
    jobs_str,
    get_rootpart_of_econ_dir,
    treasury_file_name,
    get_atoms_folder,
    get_test_real_id,
    get_test_reals_dir,
    get_init_atom_id_if_None,
    get_json_filename,
    init_atom_id,
)
from src._road.finance import default_planck_if_none, default_penny_if_none
from src._road.road import (
    PersonID,
    RealID,
    RoadNode,
    RoadUnit,
    rebuild_road,
    get_all_road_nodes,
    validate_roadnode,
    default_road_delimiter_if_none,
)
from src.agenda.agenda import (
    AgendaUnit,
    get_from_json as agendaunit_get_from_json,
    agendaunit_shop,
)
from src.atom.quark import (
    QuarkUnit,
    get_from_json as quarkunit_get_from_json,
    modify_agenda_with_quarkunit,
)
from src.listen.basis_agendas import get_default_work_agenda
from src.atom.atom import AtomUnit, atomunit_shop, create_atomunit_from_files
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from sqlite3 import connect as sqlite3_connect, Connection


class Invalid_duty_Exception(Exception):
    pass


class Invalid_work_Exception(Exception):
    pass


class SaveAtomFileException(Exception):
    pass


class AtomFileMissingException(Exception):
    pass


class PersonCreateMoneyUnitsException(Exception):
    pass


class _econ_roadMissingException(Exception):
    pass


def get_econ_roles_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{roles_str()}"


def get_econ_jobs_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{jobs_str()}"


# def pipeline_duty_work_text() -> str:
#     return "duty_work"


# def pipeline_role_job_text() -> str:
#     return "role_job"


# def pipeline_job_work_text() -> str:
#     return "job_work"


@dataclass
class UserHub:
    person_id: PersonID = None
    reals_dir: str = None
    real_id: str = None
    econ_road: RoadUnit = None
    road_delimiter: str = None
    planck: float = None
    penny: float = None

    def real_dir(self):
        return f"{self.reals_dir}/{self.real_id}"

    def persons_dir(self):
        return f"{self.real_dir()}/persons"

    def person_dir(self):
        return f"{self.persons_dir()}/{self.person_id}"

    def econs_dir(self):
        return f"{self.person_dir()}/econs"

    def quarks_dir(self):
        return f"{self.person_dir()}/quarks"

    def atoms_dir(self):
        return f"{self.person_dir()}/{get_atoms_folder()}"

    def duty_dir(self) -> str:
        return f"{self.person_dir()}/duty"

    def work_dir(self) -> str:
        return f"{self.person_dir()}/work"

    def duty_file_name(self):
        return get_json_filename(self.person_id)

    def duty_file_path(self):
        return f"{self.duty_dir()}/{self.duty_file_name()}"

    def work_file_name(self):
        return get_json_filename(self.person_id)

    def work_path(self):
        return f"{self.work_dir()}/{self.work_file_name()}"

    def save_file_duty(self, file_text: str, replace: bool):
        save_file(
            dest_dir=self.duty_dir(),
            file_name=self.duty_file_name(),
            file_text=file_text,
            replace=replace,
        )

    def save_file_work(self, file_text: str, replace: bool):
        save_file(
            dest_dir=self.work_dir(),
            file_name=self.work_file_name(),
            file_text=file_text,
            replace=replace,
        )

    def duty_file_exists(self) -> bool:
        return os_path_exists(self.duty_file_path())

    def work_file_exists(self) -> bool:
        return os_path_exists(self.work_path())

    def open_file_duty(self):
        return open_file(self.duty_dir(), self.duty_file_name())

    def save_duty_agenda(self, x_agenda: AgendaUnit):
        if x_agenda._owner_id != self.person_id:
            raise Invalid_duty_Exception(
                f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{self.person_id}''s duty agenda."
            )
        self.save_file_duty(x_agenda.get_json(), True)

    def get_duty_agenda(self) -> AgendaUnit:
        if self.duty_file_exists() is False:
            return None
        file_content = self.open_file_duty()
        return agendaunit_get_from_json(file_content)

    def default_duty_agenda(self) -> AgendaUnit:
        x_agendaunit = agendaunit_shop(
            _owner_id=self.person_id,
            _real_id=self.real_id,
            _road_delimiter=self.road_delimiter,
            _planck=self.planck,
            _penny=self.penny,
        )
        x_agendaunit._last_atom_id = init_atom_id()
        return x_agendaunit

    def delete_duty_file(self):
        delete_dir(self.duty_file_path())

    def open_file_work(self):
        return open_file(self.work_dir(), self.work_file_name())

    def get_max_quark_file_number(self) -> int:
        if not os_path_exists(self.quarks_dir()):
            return None
        quark_files_dict = dir_files(self.quarks_dir(), True, include_files=True)
        quark_filenames = quark_files_dict.keys()
        quark_file_numbers = {int(quark_filename) for quark_filename in quark_filenames}
        return max(quark_file_numbers, default=None)

    def _get_next_quark_file_number(self) -> int:
        max_file_number = self.get_max_quark_file_number()
        return 0 if max_file_number is None else max_file_number + 1

    def quark_file_name(self, quark_number: int) -> str:
        return f"{quark_number}.json"

    def quark_file_path(self, quark_number: int) -> str:
        return f"{self.quarks_dir()}/{self.quark_file_name(quark_number)}"

    def _save_valid_quark_file(self, x_quark: QuarkUnit, file_number: int):
        save_file(
            self.quarks_dir(),
            self.quark_file_name(file_number),
            x_quark.get_json(),
            replace=False,
        )
        return file_number

    def save_quark_file(self, x_quark: QuarkUnit):
        x_quark_filename = self._get_next_quark_file_number()
        return self._save_valid_quark_file(x_quark, x_quark_filename)

    def quark_file_exists(self, quark_number: int) -> bool:
        return os_path_exists(self.quark_file_path(quark_number))

    def delete_quark_file(self, quark_number: int):
        delete_dir(self.quark_file_path(quark_number))

    def _get_agenda_from_quark_files(self) -> AgendaUnit:
        x_agenda = agendaunit_shop(self.person_id, self.real_id)
        if self.quark_file_exists(self.get_max_quark_file_number()):
            x_quark_files = dir_files(self.quarks_dir(), delete_extensions=True)
            sorted_quark_filenames = sorted(list(x_quark_files.keys()))

            for x_quark_filename in sorted_quark_filenames:
                x_file_text = x_quark_files.get(x_quark_filename)
                x_quark = quarkunit_get_from_json(x_file_text)
                modify_agenda_with_quarkunit(x_agenda, x_quark)
        return x_agenda

    def get_max_atom_file_number(self) -> int:
        if not os_path_exists(self.atoms_dir()):
            return None
        atoms_dir = self.atoms_dir()
        atom_filenames = dir_files(atoms_dir, True, include_files=True).keys()
        atom_file_numbers = {int(filename) for filename in atom_filenames}
        return max(atom_file_numbers, default=None)

    def _get_next_atom_file_number(self) -> int:
        max_file_number = self.get_max_atom_file_number()
        init_atom_id = get_init_atom_id_if_None()
        return init_atom_id if max_file_number is None else max_file_number + 1

    def atom_file_name(self, atom_id: int) -> str:
        return get_json_filename(atom_id)

    def atom_file_path(self, atom_id: int) -> bool:
        atom_filename = self.atom_file_name(atom_id)
        return f"{self.atoms_dir()}/{atom_filename}"

    def atom_file_exists(self, atom_id: int) -> bool:
        return os_path_exists(self.atom_file_path(atom_id))

    def validate_atomunit(self, x_atomunit: AtomUnit) -> AtomUnit:
        if x_atomunit._quarks_dir != self.quarks_dir():
            x_atomunit._quarks_dir = self.quarks_dir()
        if x_atomunit._atoms_dir != self.atoms_dir():
            x_atomunit._atoms_dir = self.atoms_dir()
        if x_atomunit._atom_id != self._get_next_atom_file_number():
            x_atomunit._atom_id = self._get_next_atom_file_number()
        if x_atomunit._giver != self.person_id:
            x_atomunit._giver = self.person_id
        if x_atomunit._nuc_start != self._get_next_quark_file_number():
            x_atomunit._nuc_start = self._get_next_quark_file_number()
        return x_atomunit

    def save_atom_file(
        self,
        x_atom: AtomUnit,
        replace: bool = True,
        correct_invalid_attrs: bool = True,
    ) -> AtomUnit:
        if correct_invalid_attrs:
            x_atom = self.validate_atomunit(x_atom)

        if x_atom._quarks_dir != self.quarks_dir():
            raise SaveAtomFileException(
                f"AtomUnit file cannot be saved because atomunit._quarks_dir is incorrect: {x_atom._quarks_dir}. It must be {self.quarks_dir()}."
            )
        if x_atom._atoms_dir != self.atoms_dir():
            raise SaveAtomFileException(
                f"AtomUnit file cannot be saved because atomunit._atoms_dir is incorrect: {x_atom._atoms_dir}. It must be {self.atoms_dir()}."
            )
        if x_atom._giver != self.person_id:
            raise SaveAtomFileException(
                f"AtomUnit file cannot be saved because atomunit._giver is incorrect: {x_atom._giver}. It must be {self.person_id}."
            )
        atom_filename = self.atom_file_name(x_atom._atom_id)
        if not replace and self.atom_file_exists(x_atom._atom_id):
            raise SaveAtomFileException(
                f"AtomUnit file {atom_filename} already exists and cannot be saved over."
            )
        x_atom.save_files()
        return x_atom

    def _del_atom_file(self, atom_id: int):
        delete_dir(self.atom_file_path(atom_id))

    def _default_atomunit(self) -> AtomUnit:
        return atomunit_shop(
            _giver=self.person_id,
            _atom_id=self._get_next_atom_file_number(),
            _quarks_dir=self.quarks_dir(),
            _atoms_dir=self.atoms_dir(),
        )

    def create_save_atom_file(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        new_atomunit = self._default_atomunit()
        new_nucunit = new_atomunit._nucunit
        new_nucunit.add_all_different_quarkunits(before_agenda, after_agenda)
        self.save_atom_file(new_atomunit)

    def get_atomunit(self, atom_id: int) -> AtomUnit:
        if self.atom_file_exists(atom_id) is False:
            raise AtomFileMissingException(
                f"AtomUnit file_number {atom_id} does not exist."
            )
        x_atoms_dir = self.atoms_dir()
        x_quarks_dir = self.quarks_dir()
        return create_atomunit_from_files(x_atoms_dir, atom_id, x_quarks_dir)

    def _merge_any_atoms(self, x_agenda: AgendaUnit) -> AgendaUnit:
        atoms_dir = self.atoms_dir()
        atom_ints = get_integer_filenames(atoms_dir, x_agenda._last_atom_id)
        if len(atom_ints) == 0:
            return copy_deepcopy(x_agenda)

        for atom_int in atom_ints:
            x_atom = self.get_atomunit(atom_int)
            new_agenda = x_atom._nucunit.get_edited_agenda(x_agenda)
        return new_agenda

    def _create_initial_atom_files_from_default(self):
        x_atomunit = atomunit_shop(
            _giver=self.person_id,
            _atom_id=get_init_atom_id_if_None(),
            _atoms_dir=self.atoms_dir(),
            _quarks_dir=self.quarks_dir(),
        )
        x_atomunit._nucunit.add_all_different_quarkunits(
            before_agenda=self.default_duty_agenda(),
            after_agenda=self.default_duty_agenda(),
        )
        x_atomunit.save_files()

    def _create_duty_from_atoms(self):
        x_agenda = self._merge_any_atoms(self.default_duty_agenda())
        self.save_duty_agenda(x_agenda)

    def _create_initial_atom_and_duty_files(self):
        self._create_initial_atom_files_from_default()
        self._create_duty_from_atoms()

    def _create_initial_atom_files_from_duty(self):
        x_atomunit = self._default_atomunit()
        x_atomunit._nucunit.add_all_different_quarkunits(
            before_agenda=self.default_duty_agenda(),
            after_agenda=self.get_duty_agenda(),
        )
        x_atomunit.save_files()

    def initialize_atom_duty_files(self):
        x_duty_file_exists = self.duty_file_exists()
        atom_file_exists = self.atom_file_exists(init_atom_id())
        if x_duty_file_exists is False and atom_file_exists is False:
            self._create_initial_atom_and_duty_files()
        elif x_duty_file_exists is False and atom_file_exists:
            self._create_duty_from_atoms()
        elif x_duty_file_exists and atom_file_exists is False:
            self._create_initial_atom_files_from_duty()

    def append_atoms_to_duty_file(self):
        duty_agenda = self.get_duty_agenda()
        duty_agenda = self._merge_any_atoms(duty_agenda)
        self.save_duty_agenda(duty_agenda)
        return self.get_duty_agenda()

    def econ_dir(self) -> str:
        return get_econ_path(self, self.econ_road)

    def create_econ_dir_if_missing(self):
        set_dir(self.econ_dir())

    def owner_file_name(self, owner_id: PersonID) -> str:
        return get_json_filename(owner_id)

    def treasury_file_name(self) -> str:
        return treasury_file_name()

    def treasury_db_path(self) -> str:
        return f"{self.econ_dir()}/{treasury_file_name()}"

    def role_path(self, owner_id: PersonID) -> str:
        return f"{self.roles_dir()}/{self.owner_file_name(owner_id)}"

    def job_path(self, owner_id: PersonID) -> str:
        return f"{self.jobs_dir()}/{self.owner_file_name(owner_id)}"

    def roles_dir(self) -> str:
        return get_econ_roles_dir(self.econ_dir())

    def jobs_dir(self) -> str:
        return get_econ_jobs_dir(self.econ_dir())

    def get_jobs_dir_file_names_list(self):
        try:
            return list(dir_files(self.jobs_dir(), True).keys())
        except Exception:
            return []

    def save_role_agenda(self, x_agenda: AgendaUnit):
        x_file_name = self.owner_file_name(x_agenda._owner_id)
        save_file(self.roles_dir(), x_file_name, x_agenda.get_json())

    def save_job_agenda(self, x_agenda: AgendaUnit):
        x_file_name = self.owner_file_name(x_agenda._owner_id)
        save_file(self.jobs_dir(), x_file_name, x_agenda.get_json())

    def save_work_agenda(self, x_agenda: AgendaUnit):
        if x_agenda._owner_id != self.person_id:
            raise Invalid_work_Exception(
                f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{self.person_id}''s work agenda."
            )
        self.save_file_work(x_agenda.get_json(), True)

    def initialize_work_file(self, duty: AgendaUnit):
        if self.work_file_exists() is False:
            self.save_work_agenda(get_default_work_agenda(duty))

    def role_file_exists(self, owner_id: PersonID) -> bool:
        return os_path_exists(self.role_path(owner_id))

    def job_file_exists(self, owner_id: PersonID) -> bool:
        return os_path_exists(self.job_path(owner_id))

    def get_role_agenda(self, owner_id: PersonID) -> AgendaUnit:
        if self.role_file_exists(owner_id) is False:
            return None
        file_content = open_file(self.roles_dir(), self.owner_file_name(owner_id))
        return agendaunit_get_from_json(file_content)

    def get_job_agenda(self, owner_id: PersonID) -> AgendaUnit:
        if self.job_file_exists(owner_id) is False:
            return None
        file_content = open_file(self.jobs_dir(), self.owner_file_name(owner_id))
        return agendaunit_get_from_json(file_content)

    def get_work_agenda(self) -> AgendaUnit:
        if self.work_file_exists() is False:
            return None
        file_content = self.open_file_work()
        return agendaunit_get_from_json(file_content)

    def delete_role_file(self, owner_id: PersonID):
        delete_dir(self.role_path(owner_id))

    def delete_job_file(self, owner_id: PersonID):
        delete_dir(self.job_path(owner_id))

    def delete_treasury_db_file(self):
        delete_dir(self.treasury_db_path())

    def rj_speaker_file_name(self, speaker_id: PersonID) -> str:
        return get_json_filename(speaker_id)

    def rj_speaker_dir(self, healer_id: PersonID) -> str:
        healer_userhub = userhub_shop(
            self.reals_dir, self.real_id, healer_id, self.econ_road
        )
        return healer_userhub.jobs_dir()

    def rj_speaker_file_path(self, healer_id: PersonID, speaker_id: PersonID) -> str:
        reals_dir = self.reals_dir
        real_id = self.real_id
        healer_userhub = userhub_shop(reals_dir, real_id, healer_id, self.econ_road)
        return healer_userhub.job_path(owner_id=speaker_id)

    def dw_speaker_file_name(self, person_id: PersonID) -> str:
        return get_json_filename(person_id)

    def dw_speaker_dir(self, x_person_id: PersonID) -> str:
        speaker_userhub = userhub_shop(
            reals_dir=self.reals_dir,
            real_id=self.real_id,
            person_id=x_person_id,
            road_delimiter=self.road_delimiter,
            planck=self.planck,
        )
        return speaker_userhub.work_dir()

    def dw_speaker_file_path(self, x_person_id: PersonID) -> str:
        return f"{self.dw_speaker_dir(x_person_id)}/{self.dw_speaker_file_name(x_person_id)}"

    def dw_speaker_agenda(self, speaker_id: PersonID) -> AgendaUnit:
        speaker_userhub = userhub_shop(
            reals_dir=self.reals_dir,
            real_id=self.real_id,
            person_id=speaker_id,
            road_delimiter=self.road_delimiter,
            planck=self.planck,
        )
        return speaker_userhub.get_work_agenda()

    def jw_speaker_dir(self, x_person_id: PersonID, x_econ_path: RoadUnit) -> str:
        speaker_userhub = userhub_shop(
            reals_dir=self.reals_dir,
            real_id=self.real_id,
            person_id=x_person_id,
            econ_road=x_econ_path,
            road_delimiter=self.road_delimiter,
            planck=self.planck,
        )
        return speaker_userhub.jobs_dir()

    def jw_speaker_file_path(self, x_person_id: PersonID, x_econ_path: RoadUnit) -> str:
        jw_dir = self.jw_speaker_dir(x_person_id, x_econ_path)
        return f"{jw_dir}/{self.owner_file_name(self.person_id)}"

    def get_perspective_agenda(self, speaker: AgendaUnit) -> AgendaUnit:
        # get copy of agenda without any metrics
        perspective_agenda = agendaunit_get_from_json(speaker.get_json())
        perspective_agenda.set_owner_id(self.person_id)
        return perspective_agenda

    def get_dw_perspective_agenda(self, speaker_id: PersonID) -> AgendaUnit:
        return self.get_perspective_agenda(self.dw_speaker_agenda(speaker_id))

    def rj_speaker_agenda(
        self, healer_id: PersonID, speaker_id: PersonID
    ) -> AgendaUnit:
        speaker_userhub = userhub_shop(
            reals_dir=self.reals_dir,
            real_id=self.real_id,
            person_id=healer_id,
            econ_road=self.econ_road,
            road_delimiter=self.road_delimiter,
            planck=self.planck,
        )
        return speaker_userhub.get_job_agenda(speaker_id)

    def rj_perspective_agenda(
        self, healer_id: PersonID, speaker_id: PersonID
    ) -> AgendaUnit:
        speaker_job = self.rj_speaker_agenda(healer_id, speaker_id)
        return self.get_perspective_agenda(speaker_job)

    def get_econ_roads(self):
        x_duty_agenda = self.get_duty_agenda()
        x_duty_agenda.calc_agenda_metrics()
        if x_duty_agenda._econs_justified is False:
            x_str = f"Cannot set '{self.person_id}' duty agenda moneyunits because 'AgendaUnit._econs_justified' is False."
            raise PersonCreateMoneyUnitsException(x_str)
        if x_duty_agenda._econs_buildable is False:
            x_str = f"Cannot set '{self.person_id}' duty agenda moneyunits because 'AgendaUnit._econs_buildable' is False."
            raise PersonCreateMoneyUnitsException(x_str)
        person_healer_dict = x_duty_agenda._healers_dict.get(self.person_id)
        if person_healer_dict is None:
            return get_empty_set_if_none(None)
        econ_roads = x_duty_agenda._healers_dict.get(self.person_id).keys()
        return get_empty_set_if_none(econ_roads)

    def save_all_duty_roles(self):
        duty = self.get_duty_agenda()
        for x_econ_road in self.get_econ_roads():
            self.econ_road = x_econ_road
            self.save_role_agenda(duty)
        self.econ_road = None

    def create_treasury_db_file(self):
        self.create_econ_dir_if_missing()
        with sqlite3_connect(self.treasury_db_path()) as conn:
            pass

    def treasury_db_file_exists(self) -> bool:
        return os_path_exists(self.treasury_db_path())

    def treasury_db_file_conn(self) -> Connection:
        if self.econ_road is None:
            raise _econ_roadMissingException(
                f"userhub cannot connect to treasury_db_file because econ_road is {self.econ_road}"
            )
        if self.treasury_db_file_exists() is False:
            self.create_treasury_db_file()
        return sqlite_connection(self.treasury_db_path())

    def create_duty_treasury_db_files(self):
        for x_econ_road in self.get_econ_roads():
            self.econ_road = x_econ_road
            self.create_treasury_db_file()
        self.econ_road = None


def userhub_shop(
    reals_dir: str,
    real_id: RealID,
    person_id: PersonID = None,
    econ_road: RoadUnit = None,
    road_delimiter: str = None,
    planck: float = None,
    penny: float = None,
) -> UserHub:
    if reals_dir is None:
        reals_dir = get_test_reals_dir()
    if real_id is None:
        real_id = get_test_real_id()

    return UserHub(
        reals_dir=reals_dir,
        real_id=real_id,
        person_id=validate_roadnode(person_id, road_delimiter),
        econ_road=econ_road,
        road_delimiter=default_road_delimiter_if_none(road_delimiter),
        planck=default_planck_if_none(planck),
        penny=default_penny_if_none(penny),
    )


def get_econ_path(x_userhub: UserHub, x_road: RoadNode) -> str:
    econ_root = get_rootpart_of_econ_dir()
    x_road = rebuild_road(x_road, x_userhub.real_id, econ_root)
    x_list = get_all_road_nodes(x_road, x_userhub.road_delimiter)
    return f"{x_userhub.econs_dir()}{get_directory_path(x_list=[*x_list])}"
