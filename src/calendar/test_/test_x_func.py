from src.calendar.x_func import (
    dir_files as x_func_dir_files,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    count_files as x_func_count_files,
    return1ifnone as x_func_return1ifnone,
)
from src.system.examples.actor_env_kit import (
    actor_dir_setup_cleanup,
    get_temp_actor_dir,
    create_calendar_file,
)
from pytest import raises as pytest_raises


def test_x_func_dir_files_correctlyGrabsFileData(actor_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_actor_dir()
    x1_file_name = "x1.txt"
    x2_file_name = "x2.txt"
    x1_file_text = "trying this"
    x2_file_text = "look there"
    x_func_save_file(dest_dir=env_dir, file_name=x1_file_name, file_text=x1_file_text)
    x_func_save_file(dest_dir=env_dir, file_name=x2_file_name, file_text=x2_file_text)

    # WHEN
    files_dict = x_func_dir_files(dir_path=env_dir)

    # THEN
    assert len(files_dict) == 2
    assert files_dict.get(x1_file_name) == x1_file_text
    assert files_dict.get(x2_file_name) == x2_file_text


def test_x_func_dir_files_removesFileExtension(actor_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_actor_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x1_file_text = "trying this"
    x2_file_text = "look there"
    x_func_save_file(dest_dir=env_dir, file_name=x1_file_name, file_text=x1_file_text)
    x_func_save_file(dest_dir=env_dir, file_name=x2_file_name, file_text=x2_file_text)

    # WHEN
    files_dict = x_func_dir_files(dir_path=env_dir, remove_extensions=True)

    # THEN
    assert files_dict.get(x1_name) == x1_file_text
    assert files_dict.get(x2_name) == x2_file_text


def test_x_func_dir_files_returnsSubDirs(actor_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_actor_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x1_file_text = "trying this"
    x2_file_text = "look there"
    x_func_save_file(
        dest_dir=f"{env_dir}/{x1_name}", file_name=x1_file_name, file_text=x1_file_text
    )
    x_func_save_file(
        dest_dir=f"{env_dir}/{x2_name}", file_name=x2_file_name, file_text=x2_file_text
    )

    # WHEN
    files_dict = x_func_dir_files(
        dir_path=env_dir, remove_extensions=True, include_dirs=True
    )

    # THEN
    assert files_dict.get(x1_name) == True
    assert files_dict.get(x2_name) == True


def test_x_func_dir_files_doesNotReturnsFiles(actor_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_actor_dir()
    x1_name = "x1"
    x1_file_ext = "txt"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x1_file_text = "trying this"
    x_func_save_file(dest_dir=env_dir, file_name=x1_file_name, file_text=x1_file_text)
    x2_name = "x2"
    x2_file_ext = "json"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x2_file_text = "look there"
    x_func_save_file(
        dest_dir=f"{env_dir}/{x2_name}", file_name=x2_file_name, file_text=x2_file_text
    )

    # WHEN
    files_dict = x_func_dir_files(dir_path=env_dir, include_files=False)

    # THEN
    print(f"{files_dict.get(x1_file_name)=}")
    with pytest_raises(Exception) as excinfo:
        files_dict[x1_file_name]
    assert str(excinfo.value) == "'x1.txt'"
    assert files_dict.get(x2_name) == True
    assert len(files_dict) == 1


def test_x_func_open_file_OpensFilesCorrectlyWhenGivenDirectoryAndFileName(
    actor_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_actor_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x1_file_text = "trying this"
    x2_file_text = "look there"
    print(f"{env_dir=} {x1_file_name=}")
    x_func_save_file(dest_dir=env_dir, file_name=x1_file_name, file_text=x1_file_text)
    x_func_save_file(dest_dir=env_dir, file_name=x2_file_name, file_text=x2_file_text)

    # WHEN / THEN
    assert x_func_open_file(dest_dir=env_dir, file_name=x1_file_name) == x1_file_text
    assert x_func_open_file(dest_dir=env_dir, file_name=x2_file_name) == x2_file_text


def test_x_func_open_file_OpensFilesCorrectlyWhenGivenOnlyFilePath(
    actor_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_actor_dir()
    x1_name = "x1"
    x2_name = "x2"
    x1_file_ext = "txt"
    x2_file_ext = "json"
    x1_file_name = f"{x1_name}.{x1_file_ext}"
    x2_file_name = f"{x2_name}.{x2_file_ext}"
    x1_file_text = "trying this"
    x2_file_text = "look there"
    x1_file_path = f"{env_dir}/{x1_file_name}"
    x2_file_path = f"{env_dir}/{x2_file_name}"

    print(f"{env_dir=} {x1_file_name=}")
    print(f"{env_dir=} {x1_file_name=}")
    x_func_save_file(dest_dir=env_dir, file_name=x1_file_name, file_text=x1_file_text)
    x_func_save_file(dest_dir=env_dir, file_name=x2_file_name, file_text=x2_file_text)

    # WHEN / THEN
    assert x_func_open_file(dest_dir=x1_file_path, file_name=None) == x1_file_text
    assert x_func_open_file(dest_dir=x2_file_path, file_name=None) == x2_file_text


def test_x_func_save_file_ReplacesFileAsDefault(actor_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_actor_dir()
    x_old_name = "x_old"
    # x_new_name = "x_new"
    x_old_file_ext = "txt"
    # x_new_file_ext = "json"
    x_old_file_name = f"{x_old_name}.{x_old_file_ext}"
    # x_new_file_name = f"{x_new_name}.{x_new_file_ext}"
    x_old_file_text = "trying this"
    x_new_file_text = "look there"
    print(f"{env_dir=} {x_old_file_name=}")
    x_func_save_file(
        dest_dir=env_dir, file_name=x_old_file_name, file_text=x_old_file_text
    )
    assert (
        x_func_open_file(dest_dir=env_dir, file_name=x_old_file_name) == x_old_file_text
    )

    # WHEN
    x_func_save_file(
        dest_dir=env_dir,
        file_name=x_old_file_name,
        file_text=x_new_file_text,
        replace=None,
    )

    # THEN
    assert (
        x_func_open_file(dest_dir=env_dir, file_name=x_old_file_name) == x_new_file_text
    )


def test_x_func_save_file_DoesNotreplaceFile(actor_dir_setup_cleanup):
    # GIVEN
    env_dir = get_temp_actor_dir()
    x_old_name = "x_old"
    # x_new_name = "x_new"
    x_old_file_ext = "txt"
    # x_new_file_ext = "json"
    x_old_file_name = f"{x_old_name}.{x_old_file_ext}"
    # x_new_file_name = f"{x_new_name}.{x_new_file_ext}"
    x_old_file_text = "trying this"
    x_new_file_text = "look there"
    print(f"{env_dir=} {x_old_file_name=}")
    x_func_save_file(
        dest_dir=env_dir, file_name=x_old_file_name, file_text=x_old_file_text
    )
    assert (
        x_func_open_file(dest_dir=env_dir, file_name=x_old_file_name) == x_old_file_text
    )

    # WHEN
    x_func_save_file(
        dest_dir=env_dir,
        file_name=x_old_file_name,
        file_text=x_new_file_text,
        replace=False,
    )

    # THEN
    assert (
        x_func_open_file(dest_dir=env_dir, file_name=x_old_file_name) == x_old_file_text
    )


def test_x_func_count_files_ReturnsNoneIfDirectoryDoesNotExist(
    actor_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_actor_dir()
    does_not_exist_dir = f"{env_dir}/swim"

    # WHEN
    dir_count = x_func_count_files(dir_path=does_not_exist_dir)

    # THEN
    assert dir_count is None


def test_x_func_return1ifNone():
    # GIVEN / WHEN / THEN
    assert x_func_return1ifnone(None) == 1
    assert x_func_return1ifnone(2) == 2
    assert x_func_return1ifnone(-3) == -3
