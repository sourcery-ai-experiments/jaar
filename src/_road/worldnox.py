from src._instrument.file import save_file, open_file
from src._road.finance import default_planck_if_none
from src._road.road import (
    default_road_delimiter_if_none,
    PersonID,
    RealID,
    validate_roadnode,
)
from src._road.jaar_config import (
    get_changes_folder,
    get_test_reals_dir,
    get_test_real_id,
    get_json_filename,
)
from os.path import exists as os_path_exists
from dataclasses import dataclass


def get_file_name(x_person_id: PersonID) -> str:
    return get_json_filename(x_person_id)


@dataclass
class RealNox:
    reals_dir: str = None
    real_id: str = None
    _road_delimiter: str = None
    _planck: float = None

    def real_dir(self) -> str:
        return f"{self.reals_dir}/{self.real_id}"

    def persons_dir(self) -> str:
        return f"{self.real_dir()}/persons"

    def person_dir(self, person_id: PersonID) -> str:
        return f"{self.persons_dir()}/{person_id}"

    def econs_dir(self, person_id: PersonID) -> str:
        return f"{self.person_dir(person_id)}/econs"

    def atoms_dir(self, person_id: PersonID) -> str:
        return f"{self.person_dir(person_id)}/atoms"

    def changes_dir(self, person_id: PersonID) -> str:
        return f"{self.person_dir(person_id)}/{get_changes_folder()}"

    def duty_dir(self, person_id: PersonID) -> str:
        return f"{self.person_dir(person_id)}/duty"

    def work_dir(self, person_id: PersonID) -> str:
        return f"{self.person_dir(person_id)}/work"

    def duty_file_name(self, person_id: PersonID):
        return get_file_name(person_id)

    def duty_path(self, person_id: PersonID) -> str:
        return f"{self.person_dir(person_id)}/{self.duty_file_name(person_id)}"

    def work_file_name(self, person_id: PersonID):
        return get_file_name(person_id)

    def work_path(self, person_id: PersonID) -> str:
        return f"{self.person_dir(person_id)}/{self.work_file_name(person_id)}"

    def save_file_duty(self, person_id: PersonID, file_text: str, replace: bool):
        save_file(
            dest_dir=self.person_dir(person_id),
            file_name=self.duty_file_name(person_id),
            file_text=file_text,
            replace=replace,
        )

    def save_file_work(self, person_id: PersonID, file_text: str, replace: bool):
        save_file(
            dest_dir=self.person_dir(person_id),
            file_name=self.work_file_name(person_id),
            file_text=file_text,
            replace=replace,
        )

    def duty_file_exists(self, person_id: PersonID) -> bool:
        return os_path_exists(self.duty_path(person_id))

    def work_file_exists(self, person_id: PersonID) -> bool:
        return os_path_exists(self.work_path(person_id))

    def open_file_duty(self, person_id: PersonID):
        return open_file(self.person_dir(person_id), self.duty_file_name(person_id))

    def open_file_work(self, person_id: PersonID) -> str:
        return open_file(self.person_dir(person_id), self.work_file_name(person_id))


def realnox_shop(
    reals_dir: str,
    real_id: RealID,
    road_delimiter: str = None,
    planck: float = None,
) -> RealNox:
    if reals_dir is None:
        reals_dir = get_test_reals_dir()
    if real_id is None:
        real_id = get_test_real_id()

    return RealNox(
        real_id=validate_roadnode(real_id, road_delimiter),
        reals_dir=reals_dir,
        _road_delimiter=default_road_delimiter_if_none(road_delimiter),
        _planck=default_planck_if_none(planck),
    )
