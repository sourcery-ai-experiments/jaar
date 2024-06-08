from src._instrument.file import (
    get_directory_path,
    save_file,
    open_file,
    delete_dir,
    dir_files,
    set_dir,
    get_integer_filenames,
)
from src._road.jaar_config import (
    roles_str,
    jobs_str,
    get_rootpart_of_econ_dir,
    treasury_str,
    treasury_file_name,
    get_changes_folder,
    get_test_real_id,
    get_test_reals_dir,
    get_init_change_id_if_None,
    get_json_filename,
    init_change_id,
)
from src._road.finance import default_planck_if_none
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
from src._road.worldnox import get_file_name
from src.agenda.agenda import (
    AgendaUnit,
    get_from_json as agendaunit_get_from_json,
    agendaunit_shop,
)
from src.change.atom import (
    AgendaAtom,
    get_from_json as agendaatom_get_from_json,
    modify_agenda_with_agendaatom,
)
from src.change.change import ChangeUnit, changeunit_shop, create_changeunit_from_files
from os.path import exists as os_path_exists
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass


class Invalid_nox_type_Exception(Exception):
    pass


class Invalid_duty_Exception(Exception):
    pass


class Invalid_work_Exception(Exception):
    pass


class SaveChangeFileException(Exception):
    pass


class ChangeFileMissingException(Exception):
    pass


def get_econ_roles_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{roles_str()}"


def get_econ_jobs_dir(x_econ_dir: str) -> str:
    return f"{x_econ_dir}/{jobs_str()}"


def get_nox_type_set() -> set[str]:
    return {
        pipeline_duty_work_text(),
        pipeline_role_job_text(),
        pipeline_job_work_text(),
    }


def pipeline_duty_work_text() -> str:
    return "duty_work"


def pipeline_role_job_text() -> str:
    return "role_job"


def pipeline_job_work_text() -> str:
    return "job_work"


@dataclass
class FileHub:
    person_id: PersonID = None
    reals_dir: str = None
    real_id: str = None
    econ_road: RoadUnit = None
    _nox_type: str = None  # can be "duty_work", "role_job", "job_work"
    road_delimiter: str = None
    planck: float = None

    def real_dir(self):
        return f"{self.reals_dir}/{self.real_id}"

    def persons_dir(self):
        return f"{self.real_dir()}/persons"

    def person_dir(self):
        return f"{self.persons_dir()}/{self.person_id}"

    def econs_dir(self):
        return f"{self.person_dir()}/econs"

    def atoms_dir(self):
        return f"{self.person_dir()}/atoms"

    def changes_dir(self):
        return f"{self.person_dir()}/{get_changes_folder()}"

    def duty_dir(self) -> str:
        return f"{self.person_dir()}/duty"

    def work_dir(self) -> str:
        return f"{self.person_dir()}/work"

    def duty_file_name(self):
        return get_file_name(self.person_id)

    def duty_file_path(self):
        return f"{self.duty_dir()}/{self.duty_file_name()}"

    def work_file_name(self):
        return get_file_name(self.person_id)

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
        if self.duty_file_exists() == False:
            return None
        file_content = self.open_file_duty()
        return agendaunit_get_from_json(file_content)

    def default_duty_agenda(self) -> AgendaUnit:
        real_id = self.real_id
        road_delimiter = self.road_delimiter
        planck = self.planck
        x_agendaunit = agendaunit_shop(self.person_id, real_id, road_delimiter, planck)
        x_agendaunit._last_change_id = init_change_id()
        return x_agendaunit

    def delete_duty_file(self):
        delete_dir(self.duty_file_path())

    def open_file_work(self):
        return open_file(self.work_dir(), self.work_file_name())

    def get_max_atom_file_number(self) -> int:
        if not os_path_exists(self.atoms_dir()):
            return None
        atom_files_dict = dir_files(self.atoms_dir(), True, include_files=True)
        atom_filenames = atom_files_dict.keys()
        atom_file_numbers = {int(atom_filename) for atom_filename in atom_filenames}
        return max(atom_file_numbers, default=None)

    def _get_next_atom_file_number(self) -> int:
        max_file_number = self.get_max_atom_file_number()
        return 0 if max_file_number is None else max_file_number + 1

    def atom_file_name(self, atom_number: int) -> str:
        return f"{atom_number}.json"

    def atom_file_path(self, atom_number: int) -> str:
        return f"{self.atoms_dir()}/{self.atom_file_name(atom_number)}"

    def _save_valid_atom_file(self, x_atom: AgendaAtom, file_number: int):
        save_file(
            self.atoms_dir(),
            self.atom_file_name(file_number),
            x_atom.get_json(),
            replace=False,
        )
        return file_number

    def save_atom_file(self, x_atom: AgendaAtom):
        x_atom_filename = self._get_next_atom_file_number()
        return self._save_valid_atom_file(x_atom, x_atom_filename)

    def atom_file_exists(self, atom_number: int) -> bool:
        return os_path_exists(self.atom_file_path(atom_number))

    def delete_atom_file(self, atom_number: int):
        delete_dir(self.atom_file_path(atom_number))

    def _get_agenda_from_atom_files(self) -> AgendaUnit:
        x_agenda = agendaunit_shop(self.person_id, self.real_id)
        if self.atom_file_exists(self.get_max_atom_file_number()):
            x_atom_files = dir_files(self.atoms_dir(), delete_extensions=True)
            sorted_atom_filenames = sorted(list(x_atom_files.keys()))

            for x_atom_filename in sorted_atom_filenames:
                x_file_text = x_atom_files.get(x_atom_filename)
                x_atom = agendaatom_get_from_json(x_file_text)
                modify_agenda_with_agendaatom(x_agenda, x_atom)
        return x_agenda

    def get_max_change_file_number(self) -> int:
        if not os_path_exists(self.changes_dir()):
            return None
        changes_dir = self.changes_dir()
        change_filenames = dir_files(changes_dir, True, include_files=True).keys()
        change_file_numbers = {int(filename) for filename in change_filenames}
        return max(change_file_numbers, default=None)

    def _get_next_change_file_number(self) -> int:
        max_file_number = self.get_max_change_file_number()
        init_change_id = get_init_change_id_if_None()
        return init_change_id if max_file_number is None else max_file_number + 1

    def change_file_name(self, change_id: int) -> str:
        return get_json_filename(change_id)

    def change_file_path(self, change_id: int) -> bool:
        change_filename = self.change_file_name(change_id)
        return f"{self.changes_dir()}/{change_filename}"

    def change_file_exists(self, change_id: int) -> bool:
        return os_path_exists(self.change_file_path(change_id))

    def validate_changeunit(self, x_changeunit: ChangeUnit) -> ChangeUnit:
        if x_changeunit._atoms_dir != self.atoms_dir():
            x_changeunit._atoms_dir = self.atoms_dir()
        if x_changeunit._changes_dir != self.changes_dir():
            x_changeunit._changes_dir = self.changes_dir()
        if x_changeunit._change_id != self._get_next_change_file_number():
            x_changeunit._change_id = self._get_next_change_file_number()
        if x_changeunit._giver != self.person_id:
            x_changeunit._giver = self.person_id
        if x_changeunit._book_start != self._get_next_atom_file_number():
            x_changeunit._book_start = self._get_next_atom_file_number()
        return x_changeunit

    def save_change_file(
        self,
        x_change: ChangeUnit,
        replace: bool = True,
        correct_invalid_attrs: bool = True,
    ) -> ChangeUnit:
        if correct_invalid_attrs:
            x_change = self.validate_changeunit(x_change)

        if x_change._atoms_dir != self.atoms_dir():
            raise SaveChangeFileException(
                f"ChangeUnit file cannot be saved because changeunit._atoms_dir is incorrect: {x_change._atoms_dir}. It must be {self.atoms_dir()}."
            )
        if x_change._changes_dir != self.changes_dir():
            raise SaveChangeFileException(
                f"ChangeUnit file cannot be saved because changeunit._changes_dir is incorrect: {x_change._changes_dir}. It must be {self.changes_dir()}."
            )
        if x_change._giver != self.person_id:
            raise SaveChangeFileException(
                f"ChangeUnit file cannot be saved because changeunit._giver is incorrect: {x_change._giver}. It must be {self.person_id}."
            )
        change_filename = self.change_file_name(x_change._change_id)
        if not replace and self.change_file_exists(x_change._change_id):
            raise SaveChangeFileException(
                f"ChangeUnit file {change_filename} already exists and cannot be saved over."
            )
        x_change.save_files()
        return x_change

    def _del_change_file(self, change_id: int):
        delete_dir(self.change_file_path(change_id))

    def _default_changeunit(self) -> ChangeUnit:
        return changeunit_shop(
            _giver=self.person_id,
            _change_id=self._get_next_change_file_number(),
            _atoms_dir=self.atoms_dir(),
            _changes_dir=self.changes_dir(),
        )

    def create_save_change_file(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        new_changeunit = self._default_changeunit()
        new_bookunit = new_changeunit._bookunit
        new_bookunit.add_all_different_agendaatoms(before_agenda, after_agenda)
        self.save_change_file(new_changeunit)

    def get_changeunit(self, change_id: int) -> ChangeUnit:
        if self.change_file_exists(change_id) == False:
            raise ChangeFileMissingException(
                f"ChangeUnit file_number {change_id} does not exist."
            )
        x_changes_dir = self.changes_dir()
        x_atoms_dir = self.atoms_dir()
        return create_changeunit_from_files(x_changes_dir, change_id, x_atoms_dir)

    def _merge_any_changes(self, x_agenda: AgendaUnit) -> AgendaUnit:
        changes_dir = self.changes_dir()
        change_ints = get_integer_filenames(changes_dir, x_agenda._last_change_id)
        if len(change_ints) == 0:
            return copy_deepcopy(x_agenda)

        for change_int in change_ints:
            x_change = self.get_changeunit(change_int)
            new_agenda = x_change._bookunit.get_edited_agenda(x_agenda)
        return new_agenda

    def _create_initial_change_files_from_default(self):
        x_changeunit = changeunit_shop(
            _giver=self.person_id,
            _change_id=get_init_change_id_if_None(),
            _changes_dir=self.changes_dir(),
            _atoms_dir=self.atoms_dir(),
        )
        x_changeunit._bookunit.add_all_different_agendaatoms(
            before_agenda=self.default_duty_agenda(),
            after_agenda=self.default_duty_agenda(),
        )
        x_changeunit.save_files()

    def _create_duty_from_changes(self):
        x_agenda = self._merge_any_changes(self.default_duty_agenda())
        self.save_duty_agenda(x_agenda)

    def _create_initial_change_and_duty_files(self):
        self._create_initial_change_files_from_default()
        self._create_duty_from_changes()

    def _create_initial_change_files_from_duty(self):
        x_changeunit = self._default_changeunit()
        x_changeunit._bookunit.add_all_different_agendaatoms(
            before_agenda=self.default_duty_agenda(),
            after_agenda=self.get_duty_agenda(),
        )
        x_changeunit.save_files()

    def initialize_change_duty_files(self):
        x_duty_file_exists = self.duty_file_exists()
        change_file_exists = self.change_file_exists(init_change_id())
        if x_duty_file_exists == False and change_file_exists == False:
            self._create_initial_change_and_duty_files()
        elif x_duty_file_exists == False and change_file_exists:
            self._create_duty_from_changes()
        elif x_duty_file_exists and change_file_exists == False:
            self._create_initial_change_files_from_duty()

    def econ_dir(self) -> str:
        return get_econ_path(self, self.econ_road)

    def create_econ_dir_if_missing(self):
        set_dir(self.econ_dir())

    def owner_file_name(self, owner_id: PersonID) -> str:
        return get_file_name(owner_id)

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

    def role_file_exists(self, owner_id: PersonID) -> bool:
        return os_path_exists(self.role_path(owner_id))

    def job_file_exists(self, owner_id: PersonID) -> bool:
        return os_path_exists(self.job_path(owner_id))

    def get_role_agenda(self, owner_id: PersonID) -> AgendaUnit:
        if self.role_file_exists(owner_id) == False:
            return None
        file_content = open_file(self.roles_dir(), self.owner_file_name(owner_id))
        return agendaunit_get_from_json(file_content)

    def get_job_agenda(self, owner_id: PersonID) -> AgendaUnit:
        file_content = open_file(self.jobs_dir(), self.owner_file_name(owner_id))
        return agendaunit_get_from_json(file_content)

    def get_work_agenda(self) -> AgendaUnit:
        file_content = self.open_file_work()
        return agendaunit_get_from_json(file_content)

    def delete_role_file(self, owner_id: PersonID):
        delete_dir(self.role_path(owner_id))

    def delete_job_file(self, owner_id: PersonID):
        delete_dir(self.job_path(owner_id))

    def set_nox_type(self, nox_type: str):
        if nox_type is None or nox_type in get_nox_type_set():
            self._nox_type = nox_type
        else:
            raise Invalid_nox_type_Exception(f"'{nox_type}' is an invalid nox_type")

    def speaker_dir(self, x_person_id: PersonID = None, x_econ_path: RoadUnit = None):
        if self._nox_type == pipeline_role_job_text():
            return self.jobs_dir()
        if self._nox_type == pipeline_duty_work_text():
            speaker_filehub = filehub_shop(
                reals_dir=self.reals_dir,
                real_id=self.real_id,
                person_id=x_person_id,
                road_delimiter=self.road_delimiter,
                planck=self.planck,
            )
            return speaker_filehub.work_dir()
        if self._nox_type == pipeline_job_work_text():
            speaker_filehub = filehub_shop(
                reals_dir=self.reals_dir,
                real_id=self.real_id,
                person_id=x_person_id,
                econ_road=x_econ_path,
                road_delimiter=self.road_delimiter,
                planck=self.planck,
            )
            return speaker_filehub.jobs_dir()

    def speaker_file_name(self, x_arg=None) -> str:
        if self._nox_type == pipeline_role_job_text():
            return get_file_name(x_arg)
        if self._nox_type == pipeline_duty_work_text():
            return get_file_name(self.person_id)
        if self._nox_type == pipeline_job_work_text():
            return get_file_name(self.person_id)

    def listener_dir(self, x_arg=None) -> str:
        if self._nox_type == pipeline_role_job_text():
            return self.roles_dir()
        if self._nox_type == pipeline_duty_work_text():
            return self.duty_dir()
        if self._nox_type == pipeline_job_work_text():
            return self.duty_dir()

    def listener_file_name(self, x_arg=None) -> str:
        if self._nox_type == pipeline_role_job_text():
            return get_file_name(x_arg)
        if self._nox_type == pipeline_duty_work_text():
            return get_file_name(self.person_id)
        if self._nox_type == pipeline_job_work_text():
            return get_file_name(self.person_id)

    def destination_dir(self, x_arg=None) -> str:
        if self._nox_type == pipeline_role_job_text():
            return self.jobs_dir()
        if self._nox_type == pipeline_duty_work_text():
            return self.work_dir()
        if self._nox_type == pipeline_job_work_text():
            return self.work_dir()

    def destination_file_name(self, x_arg=None) -> str:
        if self._nox_type == pipeline_role_job_text():
            return get_file_name(x_arg)
        if self._nox_type == pipeline_duty_work_text():
            return get_file_name(self.person_id)
        if self._nox_type == pipeline_job_work_text():
            return get_file_name(self.person_id)

    def get_speaker_agenda(
        self, person_id: PersonID, return_None_if_missing: bool = True
    ) -> AgendaUnit:
        speaker_dir = self.speaker_dir(person_id)
        speaker_file_name = self.speaker_file_name(person_id)
        x_file_path = f"{speaker_dir}/{speaker_file_name}"
        if os_path_exists(x_file_path) or not return_None_if_missing:
            file_contents = open_file(speaker_dir, speaker_file_name)
            return agendaunit_get_from_json(file_contents)
        else:
            None

    def get_listener_agenda(self, person_id: PersonID) -> AgendaUnit:
        listener_dir = self.listener_dir(person_id)
        listener_file_name = self.listener_file_name(person_id)
        x_file_path = f"{listener_dir}/{listener_file_name}"
        if os_path_exists(x_file_path):
            file_contents = open_file(listener_dir, listener_file_name)
            return agendaunit_get_from_json(file_contents)
        else:
            None


def filehub_shop(
    reals_dir: str,
    real_id: RealID,
    person_id: PersonID = None,
    econ_road: RoadUnit = None,
    nox_type: str = None,
    road_delimiter: str = None,
    planck: float = None,
) -> FileHub:
    if reals_dir is None:
        reals_dir = get_test_reals_dir()
    if real_id is None:
        real_id = get_test_real_id()

    x_filehub = FileHub(
        reals_dir=reals_dir,
        real_id=real_id,
        person_id=validate_roadnode(person_id, road_delimiter),
        econ_road=econ_road,
        road_delimiter=default_road_delimiter_if_none(road_delimiter),
        planck=default_planck_if_none(planck),
    )
    x_filehub.set_nox_type(nox_type)
    return x_filehub


def get_econ_path(x_filehub: FileHub, x_road: RoadNode) -> str:
    econ_root = get_rootpart_of_econ_dir()
    x_road = rebuild_road(x_road, x_filehub.real_id, econ_root)
    x_list = get_all_road_nodes(x_road, x_filehub.road_delimiter)
    return f"{x_filehub.econs_dir()}{get_directory_path(x_list=[*x_list])}"
