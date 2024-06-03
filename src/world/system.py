# from src.change.agendanox import agendanox_shop
# from src._road.finance import default_planck_if_none
# from src._road.road import (
#     default_road_delimiter_if_none,
#     PersonID,
#     validate_roadnode,
#     RoadUnit,
#     RoadNode,
#     get_all_road_nodes,
#     rebuild_road,
#     create_road_from_nodes,
# )
# from src.agenda.group import GroupID
# from src.agenda.agenda import (
#     AgendaUnit,
#     agendaunit_shop,
#     get_from_json as agendaunit_get_from_json,
# )
# from src.change.atom import (
#     AgendaAtom,
#     get_from_json as agendaatom_get_from_json,
#     modify_agenda_with_agendaatom,
# )
# from src.agenda.pledge import create_pledge
# from src.econ.econ import EconUnit, econunit_shop, treasury_db_filename
# from src.real.change import (
#     ChangeUnit,
#     changeunit_shop,
#     get_json_filename as changeunit_get_json_filename,
#     create_changeunit_from_files,
#     init_change_id,
#     get_init_change_id_if_None,
#     get_changes_folder,
# )
# from src.real.examples.real_env_kit import get_test_reals_dir, get_test_real_id
# from src._instrument.python import get_empty_dict_if_none
# from src._instrument.file import (
#     save_file,
#     open_file,
#     set_dir,
#     get_directory_path,
#     get_all_dirs_with_file,
#     get_parts_dir,
#     delete_dir,
#     dir_files,
#     get_integer_filenames,
# )
# from dataclasses import dataclass
# from os.path import exists as os_path_exists
# from copy import deepcopy as copy_deepcopy


# class InvalidEconException(Exception):
#     pass


# class PersonCreateEconUnitsException(Exception):
#     pass


# class Invalid_duty_Exception(Exception):
#     pass


# class Invalid_work_Exception(Exception):
#     pass


# class SaveChangeFileException(Exception):
#     pass


# class ChangeFileMissingException(Exception):
#     pass


# @dataclass
# class neUnit:
#     person_id: PersonID = None
#     reals_dir: str = None
#     real_id: str = None
#     persons_dir: str = None
#     person_dir: str = None
#     _econs_dir: str = None
#     _atoms_dir: str = None
#     _duty_obj: AgendaUnit = None
#     _duty_file_name: str = None
#     _duty_path: str = None
#     _work_obj: AgendaUnit = None
#     _work_file_name: str = None
#     _work_path: str = None
#     _econ_objs: dict[RoadUnit:EconUnit] = None
#     _road_delimiter: str = None
#     _planck: float = None

#     def set_person_id(self, x_person_id: PersonID):
#         self.person_id = validate_roadnode(x_person_id, self._road_delimiter)
#         if self.real_id is None:
#             self.real_id = get_test_real_id()
#         if self.reals_dir is None:
#             self.reals_dir = get_test_reals_dir()
#         self.real_dir = f"{self.reals_dir}/{self.real_id}"
#         self.persons_dir = f"{self.real_dir}/persons"
#         self.person_dir = f"{self.persons_dir}/{self.person_id}"
#         self._econs_dir = f"{self.person_dir}/econs"
#         self._atoms_dir = f"{self.person_dir}/atoms"
#         if self._duty_file_name is None:
#             self._duty_file_name = f"{duty_str()}.json"
#         if self._duty_path is None:
#             self._duty_path = f"{self.person_dir}/{self._duty_file_name}"
#         if self._work_file_name is None:
#             self._work_file_name = f"{work_str()}.json"
#         if self._work_path is None:
#             self._work_path = f"{self.person_dir}/{self._work_file_name}"

#     def create_core_dir_and_files(self):
#         set_dir(self.real_dir)
#         set_dir(self.persons_dir)
#         set_dir(self.person_dir)
#         set_dir(self._econs_dir)
#         set_dir(self._atoms_dir)
#         self.initialize_change_duty_files()
#         self.initialize_work_file()

#     def initialize_change_duty_files(self):
#         duty_file_exists = self.duty_file_exists()
#         change_file_exists = self.changeunit_file_exists(init_change_id())
#         if duty_file_exists == False and change_file_exists == False:
#             self._create_initial_change_and_duty_files()
#         elif duty_file_exists == False and change_file_exists:
#             self._create_duty_from_changes()
#         elif duty_file_exists and change_file_exists == False:
#             self._create_initial_change_from_duty()

#     def _create_initial_change_and_duty_files(self):
#         default_duty_agenda = agendaunit_shop(
#             self.person_id, self.real_id, self._road_delimiter, self._planck
#         )
#         x_changeunit = changeunit_shop(
#             _giver=self.person_id,
#             _change_id=get_init_change_id_if_None(),
#             _changes_dir=self._changes_dir,
#             _atoms_dir=self._atoms_dir,
#         )

#     def initialize_work_file(self):
#         if self.work_file_exists() == False:
#             default_work_agenda = agendaunit_shop(
#                 self.person_id, self.real_id, self._road_delimiter, self._planck
#             )
#             self.save_work_file(default_work_agenda)

#     def duty_file_exists(self) -> bool:
#         return os_path_exists(self._duty_path)

#     def work_file_exists(self) -> bool:
#         return os_path_exists(self._work_path)

#     def save_duty_file(self, x_agenda: AgendaUnit, replace: bool = True):
#         if x_agenda._owner_id != self.person_id:
#             raise Invalid_duty_Exception(
#                 f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{self.person_id}''s duty agenda."
#             )
#         if replace in {True, False}:
#             save_file(
#                 dest_dir=self.person_dir,
#                 file_name=self._duty_file_name,
#                 file_text=x_agenda.get_json(),
#                 replace=replace,
#             )

#     def save_work_file(self, x_agenda: AgendaUnit, replace: bool = True):
#         if x_agenda._owner_id != self.person_id:
#             raise Invalid_work_Exception(
#                 f"AgendaUnit with owner_id '{x_agenda._owner_id}' cannot be saved as person_id '{self.person_id}''s work agenda."
#             )
#         if replace in {True, False}:
#             save_file(
#                 dest_dir=self.person_dir,
#                 file_name=self._work_file_name,
#                 file_text=x_agenda.get_json(),
#                 replace=replace,
#             )

#     def get_duty_file_agenda(self) -> AgendaUnit:
#         duty_json = open_file(dest_dir=self.person_dir, file_name=self._duty_file_name)
#         return agendaunit_get_from_json(duty_json)

#     def get_work_file_agenda(self) -> AgendaUnit:
#         work_json = open_file(dest_dir=self.person_dir, file_name=self._work_file_name)
#         return agendaunit_get_from_json(work_json)

#     def load_duty_file(self):
#         self._duty_obj = get_duty_file_agenda(x_usernox)

#     def load_work_file(self):
#         self._work_obj = self.get_work_file_agenda()

#     def changeunit_file_exists(self, change_id: int) -> bool:
#         change_filename = changeunit_get_json_filename(change_id)
#         return os_path_exists(f"{self._changes_dir}/{change_filename}")

#     def get_max_change_file_number(self) -> int:
#         if not os_path_exists(self._changes_dir):
#             return None
#         change_filenames = dir_files(self._changes_dir, True, include_files=True).keys()
#         change_file_numbers = {int(change_filename) for change_filename in change_filenames}
#         return max(change_file_numbers, default=None)

#     def _get_next_change_file_number(self) -> int:
#         max_file_number = self.get_max_change_file_number()
#         return (
#             get_init_change_id_if_None()
#             if max_file_number is None
#             else max_file_number + 1
#         )

#     def save_changeunit_file(
#         self, x_change: ChangeUnit, replace: bool = True, _invalid_attrs: bool = True
#     ) -> ChangeUnit:
#         if _invalid_attrs:
#             x_change = validate_changeunit(x_change)

#         if x_change._atoms_dir != self._atoms_dir:
#             raise SaveChangeFileException(
#                 f"ChangeUnit file cannot be saved because changeunit._atoms_dir is incorrect: {x_change.atoms_dir()}. It must be {self.atoms_dir()}."
#             )
#         if x_change._changes_dir != self._changes_dir:
#             raise SaveChangeFileException(
#                 f"ChangeUnit file cannot be saved because changeunit._changes_dir is incorrect: {x_change._changes_dir}. It must be {self._changes_dir}."
#             )
#         if x_change._giver != self.person_id:
#             raise SaveChangeFileException(
#                 f"ChangeUnit file cannot be saved because changeunit._giver is incorrect: {x_change._giver}. It must be {self.person_id}."
#             )
#         change_filename = changeunit_get_json_filename(x_change._change_id)
#         if not replace and self.changeunit_file_exists(x_change._change_id):
#             raise SaveChangeFileException(
#                 f"ChangeUnit file {change_filename} already exists and cannot be saved over."
#             )
#         x_change.save_files()
#         return x_change

#     def _create_new_changeunit(self) -> ChangeUnit:
#         return changeunit_shop(
#             _giver=self.person_id,
#             _change_id=self._get_next_change_file_number(),
#             _atoms_dir=self._atoms_dir,
#             _changes_dir=self._changes_dir,
#         )

#     def validate_changeunit(self, x_changeunit: ChangeUnit) -> ChangeUnit:
#         if x_changeunit._atoms_dir != self._atoms_dir:
#             x_changeunit._atoms_dir = self._atoms_dir
#         if x_changeunit._changes_dir != self._changes_dir:
#             x_changeunit._changes_dir = self._changes_dir
#         if x_changeunit._change_id != self._get_next_change_file_number():
#             x_changeunit._change_id = self._get_next_change_file_number()
#         if x_changeunit._giver != self.person_id:
#             x_changeunit._giver = self.person_id
#         if x_changeunit._book_start != self._get_next_atom_file_number(x_usernox):
#             x_changeunit._book_start = self._get_next_atom_file_number(x_usernox)
#         return x_changeunit

#     def get_changeunit(self, file_number: int) -> ChangeUnit:
#         if self.changeunit_file_exists(file_number) == False:
#             raise ChangeFileMissingException(
#                 f"ChangeUnit file_number {file_number} does not exist."
#             )
#         return create_changeunit_from_files(
#             changes_dir=self._changes_dir, change_id=file_number, atoms_dir=self._atoms_dir
#         )

#     def del_changeunit_file(self, file_number: int):
#         delete_dir(f"{self._changes_dir}/{changeunit_get_json_filename(file_number)}")

#     def _merge_changes_into_agenda(self, x_agenda: AgendaUnit) -> AgendaUnit:
#         change_ints = get_integer_filenames(self._changes_dir, x_agenda._last_change_id)
#         for change_int in change_ints:
#             x_change = get_changeunit(change_int)
#             new_agenda = x_change._bookunit.get_edited_agenda(x_agenda)

#             update_text = "UPDATE"
#             x_agendaunit = x_change._bookunit.agendaatoms.get(update_text)
#         return new_agenda

#     def _save_valid_atom_file(self, x_atom: AgendaAtom, file_number: int):
#         save_file(self._atoms_dir, f"{file_number}.json", x_atom.get_json())
#         return file_number

#     def atom_file_exists(self, filename: int) -> bool:
#         return os_path_exists(f"{self.atoms_dir()}/{filename}.json")

#     def _delete_atom_file(self, filename: int):
#         delete_dir(f"{self.atoms_dir()}/{filename}.json")

#     def _get_max_atom_file_number(self) -> int:
#         if not os_path_exists(self._atoms_dir):
#             return None
#         atom_filenames = dir_files(
#             dir_path=self._atoms_dir, delete_extensions=True, include_files=True
#         ).keys()
#         atom_file_numbers = {int(atom_filename) for atom_filename in atom_filenames}
#         return max(atom_file_numbers, default=None)

#     def _get_next_atom_file_number(self) -> str:
#         max_file_number = self._get_max_atom_file_number()
#         return 0 if max_file_number is None else max_file_number + 1

#     def save_atom_file(self, x_atom: AgendaAtom):
#         x_filename = self._get_next_atom_file_number(x_usernox)
#         return self._save_valid_atom_file(x_atom, x_filename)

#     def _get_agenda_from_atom_files(self) -> AgendaUnit:
#         x_agenda = agendaunit_shop(_owner_id=self.person_id, _real_id=self.real_id)
#         x_atom_files = dir_files(self._atoms_dir, delete_extensions=True)
#         sorted_atom_filenames = sorted(list(x_atom_files.keys()))

#         for x_atom_filename in sorted_atom_filenames:
#             x_file_text = x_atom_files.get(x_atom_filename)
#             x_atom = agendaatom_get_from_json(x_file_text)
#             modify_agenda_with_agendaatom(x_agenda, x_atom)
#         return x_agenda

#     def get_rootpart_of_econ_dir(self):
#         return "idearoot"

#     def _get_person_econ_dir(self, x_list: list[RoadNode]) -> str:
#         return f"{self_econs_dir()}{get_directory_path(x_list=[*x_list])}"

#     def _create_econ_dir(self, x_roadunit: RoadUnit) -> str:
#         x_roadunit = rebuild_road(
#             x_roadunit, self.real_id, self.get_rootpart_of_econ_dir()
#         )
#         road_nodes = get_all_road_nodes(x_roadunit, delimiter=self._road_delimiter)
#         x_econ_path = self._get_person_econ_dir(road_nodes)
#         set_dir(x_econ_path)
#         return x_econ_path

#     def _create_econunit(self, econ_roadunit: RoadUnit):
#         x_econ_path = self._create_econ_dir(econ_roadunit)
#         x_econunit = econunit_shop(
#             real_id=self.real_id,
#             econ_dir=x_econ_path,
#             _manager_person_id=self.person_id,
#             _road_delimiter=self._road_delimiter,
#         )
#         x_econunit.set_econ_dirs()
#         self._econ_objs[econ_roadunit] = x_econunit

#     def create_person_econunits(self, econ_exceptions: bool = True):
#         x_duty_agenda = get_duty_file_agenda(x_usernox)
#         x_duty_agenda.calc_agenda_metrics(econ_exceptions)
#         if x_duty_agenda._econs_justified == False:
#             raise PersonCreateEconUnitsException(
#                 f"Cannot set '{self.person_id}' duty agenda econunits because 'AgendaUnit._econs_justified' is False."
#             )
#         if x_duty_agenda._econs_buildable == False:
#             raise PersonCreateEconUnitsException(
#                 f"Cannot set '{self.person_id}' duty agenda econunits because 'AgendaUnit._econs_buildable' is False."
#             )

#         x_person_econs = x_duty_agenda._healers_dict.get(self.person_id)
#         x_person_econs = get_empty_dict_if_none(x_person_econs)
#         self._econ_objs = {}
#         for econ_idea in x_person_econs.values():
#             self._create_econunit(econ_roadunit=econ_idea.get_road())

#         # delete any
#         x_treasury_dirs = get_all_dirs_with_file(
#             treasury_db_filename(), self._econs_dir
#         )
#         for treasury_dir in x_treasury_dirs:
#             treasury_road = create_road_from_nodes(get_parts_dir(treasury_dir))
#             treasury_road = rebuild_road(
#                 treasury_road, self.get_rootpart_of_econ_dir(), self.real_id
#             )
#             if x_person_econs.get(treasury_road) is None:
#                 dir_to_delete = f"{self_econs_dir()}/{treasury_dir}"
#                 delete_dir(dir_to_delete)

#     def get_econ(self, econ_road: RoadUnit) -> EconUnit:
#         return self._econ_objs.get(econ_road)

#     def set_econunit_role(self, econ_road: RoadUnit, role: AgendaUnit):
#         x_econ = self.get_econ(econ_road)
#         x_econ.agendanox.save_file_role(role)

#     def set_econunits_role(self, role: AgendaUnit):
#         for x_econ_road in self._econ_objs.keys():
#             self.set_econunit_role(x_econ_road, role)

#     def set_person_econunits_role(self):
#         self.set_econunits_role(get_duty_file_agenda(x_usernox))

#     def add_pledge_change(self, pledge_road: RoadUnit, x_suffgroup: GroupID = None):
#         duty_agenda = get_duty_file_agenda(x_usernox)
#         old_duty_agenda = copy_deepcopy(duty_agenda)
#         create_pledge(duty_agenda, pledge_road, x_suffgroup)
#         next_changeunit = _create_new_changeunit(x_usernox)
#         next_changeunit._bookunit.add_all_different_agendaatoms(
#             old_duty_agenda, duty_agenda
#         )
#         next_changeunit.save_files()
#         self.append_changes_to_duty_file()

#     def create_save_changeunit(self, before_agenda: AgendaUnit, after_agenda: AgendaUnit):
#         new_changeunit = _create_new_changeunit(x_usernox)
#         new_changeunit._bookunit.add_all_different_agendaatoms(
#             before_agenda, after_agenda
#         )
#         self.save_changeunit_file(new_changeunit)

#     def append_changes_to_duty_file(self):
#         self.save_duty_file(_merge_changes_into_agenda(get_duty_file_agenda(x_usernox)))
#         return get_duty_file_agenda(x_usernox)
