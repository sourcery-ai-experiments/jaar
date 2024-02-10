from src._prime.road import (
    PersonRoad,
    get_single_roadnode as get_node,
    default_road_delimiter_if_none,
)
from os import (
    path as os_path,
    makedirs as os_makedirs,
    unlink as os_unlink,
    scandir as os_scandir,
    listdir as os_listdir,
    rename as os_rename,
)
from shutil import rmtree as shutil_rmtree, copytree as shutil_copytree


def single_dir_create_if_null(x_path: str):
    if not os_path.exists(x_path):
        os_makedirs(x_path)


def delete_dir(dir: str):
    if os_path.exists(dir):
        if os_path.isdir(dir):
            shutil_rmtree(path=dir)
        elif os_path.isfile(dir):
            os_unlink(path=dir)


class InvalidFileCopyException(Exception):
    pass


def copy_dir(src_dir: str, dest_dir: str):
    if os_path.exists(dest_dir):
        raise InvalidFileCopyException(
            f"Cannot copy '{src_dir}' to '{dest_dir}' since '{dest_dir}' exists"
        )
    else:
        shutil_copytree(src=src_dir, dst=dest_dir)


def save_file(dest_dir: str, file_name: str, file_text: str, replace: bool = None):
    # print(f"{dest_dir=} {file_name=} {replace=}")
    if replace is None:
        replace = True

    if not os_path.exists(path=dest_dir):
        os_makedirs(dest_dir)

    file_path = f"{dest_dir}/{file_name}"
    if (os_path.exists(path=file_path) and replace) or os_path.exists(
        path=file_path
    ) == False:
        with open(file_path, "w") as f:
            f.write(file_text)
            f.close()


class CouldNotOpenFileException(Exception):
    pass


def open_file(dest_dir: str, file_name: str):
    file_path = dest_dir if file_name is None else f"{dest_dir}/{file_name}"
    text_x = ""
    try:
        with open(file_path, "r") as f:
            text_x = f.read()
            f.close()
    except Exception as e:
        raise CouldNotOpenFileException(
            f"Could not load file {file_path} {e.args}"
        ) from e
    return text_x


def count_files(dir_path: str) -> int:
    return (
        sum(bool(path_x.is_file()) for path_x in os_scandir(dir_path))
        if os_path.exists(path=dir_path)
        else None
    )


def dir_files(
    dir_path: str, delete_extensions: bool = None, include_dirs=None, include_files=None
) -> dict[str:str]:
    if include_dirs is None:
        include_dirs = True
    if include_files is None:
        include_files = True

    dict_x = {}
    for obj_name in os_listdir(dir_path):
        dict_key = None
        file_name = None
        file_path = None
        file_text = None
        obj_path = f"{dir_path}/{obj_name}"
        if os_path.isfile(obj_path) and include_files:
            file_name = obj_name
            file_path = f"{dir_path}/{file_name}"
            # print(f" {os_path.isdir(file_path)=}")
            file_text = open_file(dest_dir=dir_path, file_name=file_name)
            dict_key = (
                os_path.splitext(file_name)[0] if delete_extensions else file_name
            )
            dict_x[dict_key] = file_text

        if os_path.isdir(obj_path) and include_dirs:
            dict_key = obj_name
            file_text = True
            dict_x[dict_key] = file_text
    return dict_x


def rename_dir(src, dst):
    os_rename(src=src, dst=dst)
