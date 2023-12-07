from src.agenda.x_func import (
    delete_dir as x_func_delete_dir,
    dir_files as x_func_dir_files,
)
from pytest import fixture as pytest_fixture


def get_temp_env_qid():
    return "ex_env77"


def get_temp_env_dir():
    return f"{get_test_worlds_dir()}/{get_temp_env_qid()}"


def get_test_worlds_dir():
    return "src/world/examples/worlds"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_temp_env_dir()
    x_func_delete_dir(dir=env_dir)
    yield env_dir
    x_func_delete_dir(dir=env_dir)


def create_example_worlds_list():
    return x_func_dir_files(
        dir_path=get_test_worlds_dir(), include_dirs=True, include_files=False
    )


# def create_example_world(world_genus: str):
#     sx = worldunit_shop(genus=world_genus, worlds_dir=get_test_worlds_dir())
#     sx.create_dirs_if_null(in_memory_treasury=True)


# def delete_dir_example_world(world_obj: CultureUnit):
#     x_func_delete_dir(world_obj.get_object_root_dir())


# def renam_example_world(world_obj: CultureUnit, new_pid):
#     # base_dir = world_obj.get_object_root_dir()
#     base_dir = "src/world/examples/worlds"
#     src_dir = f"{base_dir}/{world_obj.genus}"
#     dst_dir = f"{base_dir}/{new_pid}"
#     os_renam(src=src_dir, dst=dst_dir)
#     world_obj.set_worldunit_genus(genus=new_pid)


# class InvalidcultureCopyException(Exception):
#     pass


# def copy_evaluation_world(src_qid: str, dest_qid: str):
#     base_dir = "src/world/examples/worlds"
#     new_dir = f"{base_dir}/{dest_qid}"
#     if os_path.exists(new_dir):
#         raise InvalidcultureCopyException(
#             f"Cannot copy world to '{new_dir}' directory because '{new_dir}' exists."
#         )
#     # base_dir = world_obj.get_object_root_dir()
#     src_dir = f"{base_dir}/{src_qid}"
#     dest_dir = f"{base_dir}/{dest_qid}"
#     copy_dir(src_dir=src_dir, dest_dir=dest_dir)
