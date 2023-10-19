from src.deal.deal import dealunit_shop
from src.deal.x_func import delete_dir as x_func_delete_dir
from src.project.kitchen import kitchenunit_shop, KitchenUnit
from src.project.examples.kitchen_env_kit import (
    kitchen_dir_setup_cleanup,
    get_temp_kitchenunit_dir,
    get_temp_project_handle,
)
from os import path as os_path


def test_KitchenUnit_exists(kitchen_dir_setup_cleanup):
    # GIVEN / WHEN
    x_kitchen = KitchenUnit()

    # GIVEN
    assert x_kitchen._admin is None
    assert x_kitchen._seed is None


def test_kitchenunit_shop_exists(kitchen_dir_setup_cleanup):
    # GIVEN
    x_title = "test1"

    # WHEN
    x_kitchen = kitchenunit_shop(
        title=x_title,
        env_dir=get_temp_kitchenunit_dir(),
        project_handle=get_temp_project_handle(),
    )

    # GIVEN
    assert x_kitchen._admin._kitchen_title != None
    assert x_kitchen._admin._project_handle != None
    assert x_kitchen._admin._project_handle == get_temp_project_handle()
    assert x_kitchen._seed is None


def test_kitchenunit_auto_output_to_public_SavesDealToPublicDirWhenTrue(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_kitchenunit_dir()
    x_handle = get_temp_project_handle()
    tim_text = "Tim"
    public_file_title = f"{tim_text}.json"
    public_file_path = f"{get_temp_kitchenunit_dir()}/deals/{public_file_title}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/project/examples/ex_env/deals/{public_file_title}"
    x_kitchen = kitchenunit_shop(
        tim_text, env_dir, x_handle, _auto_output_to_public=True
    )
    x_kitchen.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    tim_deal = dealunit_shop(_healer=tim_text)
    tim_deal.set_project_handle(x_handle)
    x_kitchen.set_depot_deal(tim_deal, "blind_trust")

    # THEN
    assert os_path.exists(public_file_path)


def test_kitchenunit_auto_output_to_public_DoesNotSaveDealToPublicDirWhenFalse(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_kitchenunit_dir()
    x_handle = get_temp_project_handle()
    tim_text = "Tim"
    public_file_title = f"{tim_text}.json"
    public_file_path = f"{get_temp_kitchenunit_dir()}/deals/{public_file_title}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/project/examples/ex_env/deals/{public_file_title}"
    x_kitchen = kitchenunit_shop(tim_text, env_dir, x_handle, False)
    x_kitchen.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    x_kitchen.set_depot_deal(dealunit_shop(tim_text), depotlink_type="blind_trust")

    # THEN
    assert os_path.exists(public_file_path) is False


def test_kitchenunit_get_seed_createsEmptyDealWhenFileDoesNotExist(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_kitchen = kitchenunit_shop(
        tim_text, get_temp_kitchenunit_dir(), get_temp_project_handle()
    )
    tim_kitchen.create_core_dir_and_files()
    assert os_path.exists(tim_kitchen._admin._seed_file_path)
    x_func_delete_dir(dir=tim_kitchen._admin._seed_file_path)
    assert os_path.exists(tim_kitchen._admin._seed_file_path) is False
    assert tim_kitchen._seed is None

    # WHEN
    seed_deal = tim_kitchen.get_seed()

    # THEN
    assert os_path.exists(tim_kitchen._admin._seed_file_path)
    assert tim_kitchen._seed != None


def test_kitchenunit_get_seed_getsMemoryDealIfExists(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_kitchen = kitchenunit_shop(
        tim_text, get_temp_kitchenunit_dir(), get_temp_project_handle()
    )
    tim_kitchen.create_core_dir_and_files()
    seed_file_path = (
        f"{tim_kitchen._admin._kitchenunit_dir}/{tim_kitchen._admin._seed_file_title}"
    )
    seed_deal1 = tim_kitchen.get_seed()
    assert os_path.exists(seed_file_path)
    assert tim_kitchen._seed != None

    # WHEN
    ray_text = "Ray"
    tim_kitchen._seed = dealunit_shop(_healer=ray_text)
    seed_deal2 = tim_kitchen.get_seed()

    # THEN
    assert seed_deal2._healer == ray_text
    assert seed_deal2 != seed_deal1

    # WHEN
    tim_kitchen._seed = None
    seed_deal3 = tim_kitchen.get_seed()

    # THEN
    assert seed_deal3._healer != ray_text
    assert seed_deal3 == seed_deal1


def test_kitchenunit_set_seed_savesseedDealSet_seed_None(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_kitchen = kitchenunit_shop(
        tim_text, get_temp_kitchenunit_dir(), get_temp_project_handle()
    )
    tim_kitchen.create_core_dir_and_files()
    seed_file_path = (
        f"{tim_kitchen._admin._kitchenunit_dir}/{tim_kitchen._admin._seed_file_title}"
    )
    seed_deal1 = tim_kitchen.get_seed()
    assert os_path.exists(seed_file_path)
    assert tim_kitchen._seed != None

    # WHEN
    uid_text = "Not a real uid"
    tim_kitchen._seed._idearoot._uid = uid_text
    tim_kitchen.set_seed()

    # THEN
    assert os_path.exists(seed_file_path)
    assert tim_kitchen._seed is None
    seed_deal2 = tim_kitchen.get_seed()
    assert seed_deal2._idearoot._uid == uid_text


def test_kitchenunit_set_seed_savesGivenDealSet_seed_None(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_kitchen = kitchenunit_shop(
        tim_text, get_temp_kitchenunit_dir(), get_temp_project_handle()
    )
    tim_kitchen.create_core_dir_and_files()
    seed_file_path = (
        f"{tim_kitchen._admin._kitchenunit_dir}/{tim_kitchen._admin._seed_file_title}"
    )
    seed_deal1 = tim_kitchen.get_seed()
    assert os_path.exists(seed_file_path)
    assert tim_kitchen._seed != None

    # WHEN
    seed_uid_text = "this is ._seed uid"
    tim_kitchen._seed._idearoot._uid = seed_uid_text

    new_deal = dealunit_shop(_healer=tim_text)
    new_deal_uid_text = "this is pulled DealUnit uid"
    new_deal._idearoot._uid = new_deal_uid_text

    tim_kitchen.set_seed(new_deal)

    # THEN
    assert os_path.exists(seed_file_path)
    assert tim_kitchen._seed is None
    assert tim_kitchen.get_seed()._idearoot._uid != seed_uid_text
    assert tim_kitchen.get_seed()._idearoot._uid == new_deal_uid_text

    # GIVEN
    tim_kitchen.set_seed(new_deal)
    assert os_path.exists(seed_file_path)
    assert tim_kitchen._seed is None

    # WHEN
    tim_kitchen.set_seed_if_empty()

    # THEN
    assert tim_kitchen._seed != None
    assert os_path.exists(seed_file_path)

    # WHEN
    seed_uid_text = "this is ._seed uid"
    tim_kitchen._seed._idearoot._uid = seed_uid_text


def test_kitchenunit_set_seed_if_emtpy_DoesNotReplace_seed(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_kitchen = kitchenunit_shop(
        tim_text, get_temp_kitchenunit_dir(), get_temp_project_handle()
    )
    tim_kitchen.create_core_dir_and_files()
    saved_deal = dealunit_shop(_healer=tim_text)
    saved_deal_uid_text = "this is pulled DealUnit uid"
    saved_deal._idearoot._uid = saved_deal_uid_text
    tim_kitchen.set_seed(saved_deal)
    tim_kitchen.get_seed()
    assert tim_kitchen._seed != None

    # WHEN
    seed_uid_text = "this is ._seed uid"
    tim_kitchen._seed._idearoot._uid = seed_uid_text
    tim_kitchen.set_seed_if_empty()

    # THEN
    assert tim_kitchen._seed != None
    assert tim_kitchen._seed._idearoot._uid == seed_uid_text
    assert tim_kitchen._seed._idearoot._uid != saved_deal_uid_text
