from src.tools.file import delete_dir, dir_files
from pytest import fixture as pytest_fixture


def get_temp_economy_id():
    return "ex_env77"


def get_temp_world_dir():
    return f"{get_test_worlds_dir()}/{get_temp_economy_id()}"


def get_test_worlds_dir():
    return "src/world/examples/worlds"


@pytest_fixture()
def worlds_dir_setup_cleanup():
    env_dir = get_test_worlds_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)


def create_example_worlds_list():
    return dir_files(
        dir_path=get_test_worlds_dir(), include_dirs=True, include_files=False
    )


# def create_example_world(world_genus: str):
#     sx = worldunit_shop(genus=world_genus, worlds_dir=get_test_worlds_dir())
#     sx.create_dirs_if_null(in_memory_treasury=True)


# def delete_dir_example_world(world_obj: EconomyUnit):
#     delete_dir(world_obj.get_object_root_dir())


# def renam_example_world(world_obj: EconomyUnit, new_pid):
#     # base_dir = world_obj.get_object_root_dir()
#     base_dir = "src/world/examples/worlds"
#     src_dir = f"{base_dir}/{world_obj.genus}"
#     dst_dir = f"{base_dir}/{new_pid}"
#     os_renam(src=src_dir, dst=dst_dir)
#     world_obj.set_worldunit_genus(genus=new_pid)


# class InvalideconomyCopyException(Exception):
#     pass


# def copy_evaluation_world(src_economy_id: str, dest_economy_id: str):
#     base_dir = "src/world/examples/worlds"
#     new_dir = f"{base_dir}/{dest_economy_id}"
#     if os_path.exists(new_dir):
#         raise InvalideconomyCopyException(
#             f"Cannot copy world to '{new_dir}' directory because '{new_dir}' exists."
#         )
#     # base_dir = world_obj.get_object_root_dir()
#     src_dir = f"{base_dir}/{src_economy_id}"
#     dest_dir = f"{base_dir}/{dest_economy_id}"
#     copy_dir(src_dir=src_dir, dest_dir=dest_dir)
