from src.agenda.agenda import AgendaUnit, agendaunit_shop
from src.agenda.atom import (
    AgendaAtom,
    get_from_json as agendaatom_get_from_json,
    change_agenda_with_agendaatom,
)
from src.real.person import ChapUnit
from src._instrument.file import (
    save_file,
    open_file,
    set_dir,
    get_directory_path,
    get_all_dirs_with_file,
    get_parts_dir,
    delete_dir,
    dir_files,
    get_integer_filenames,
)
from os.path import exists as os_path_exists


def chap_save_atom_file(x_chapunit: ChapUnit, x_atom: AgendaAtom):
    x_filename = _get_next_atom_file_number(x_chapunit)
    return _save_valid_atom_file(x_chapunit, x_atom, x_filename)


def _save_valid_atom_file(x_chapunit: ChapUnit, x_atom: AgendaAtom, file_number: int):
    save_file(x_chapunit._atoms_dir, f"{file_number}.json", x_atom.get_json())
    return file_number


def chap_atom_file_exists(x_chapunit, filename: int) -> bool:
    return os_path_exists(f"{x_chapunit._atoms_dir}/{filename}.json")


def _delete_atom_file(x_chapunit: ChapUnit, filename: int):
    delete_dir(f"{x_chapunit._atoms_dir}/{filename}.json")


def _get_agenda_from_atom_files(x_chapunit: ChapUnit) -> AgendaUnit:
    x_agenda = agendaunit_shop(x_chapunit.person_id, x_chapunit.real_id)
    x_atom_files = dir_files(x_chapunit._atoms_dir, delete_extensions=True)
    sorted_atom_filenames = sorted(list(x_atom_files.keys()))

    for x_atom_filename in sorted_atom_filenames:
        x_file_text = x_atom_files.get(x_atom_filename)
        x_atom = agendaatom_get_from_json(x_file_text)
        change_agenda_with_agendaatom(x_agenda, x_atom)
    return x_agenda


def _get_max_atom_file_number(x_chapunit: ChapUnit) -> int:
    if not os_path_exists(x_chapunit._atoms_dir):
        return None
    atom_files_dict = dir_files(x_chapunit._atoms_dir, True, include_files=True)
    atom_filenames = atom_files_dict.keys()
    atom_file_numbers = {int(atom_filename) for atom_filename in atom_filenames}
    return max(atom_file_numbers, default=None)


def _get_next_atom_file_number(x_chapunit: ChapUnit) -> str:
    max_file_number = _get_max_atom_file_number(x_chapunit)
    return 0 if max_file_number is None else max_file_number + 1
