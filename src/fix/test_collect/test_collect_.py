from src.deal.deal import DealUnit
from src.deal.x_func import (
    count_files as x_func_count_files,
    open_file as x_func_open_file,
    delete_dir as x_func_delete_dir,
)
from src.fix.collect import collectunit_shop
from src.fix.examples.collect_env_kit import (
    collect_dir_setup_cleanup,
    get_temp_collectunit_dir,
    get_temp_fix_handle,
)
from os import path as os_path


def test_collectunit_exists(collect_dir_setup_cleanup):
    # GIVEN
    healer_text = "test1"

    # WHEN
    ux = collectunit_shop(
        title=healer_text,
        env_dir=get_temp_collectunit_dir(),
        fix_handle=get_temp_fix_handle(),
    )

    # GIVEN
    assert ux._admin._collect_title != None
    assert ux._admin._fix_handle != None
    assert ux._admin._fix_handle == get_temp_fix_handle()
    assert ux._seed is None


def test_collectunit_auto_output_to_public_SavesDealToPublicDirWhenTrue(
    collect_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_collectunit_dir()
    fix_handle = get_temp_fix_handle()
    tim_text = "Tim"
    public_file_title = f"{tim_text}.json"
    public_file_path = f"{get_temp_collectunit_dir()}/deals/{public_file_title}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/fix/examples/ex_env/deals/{public_file_title}"
    ux = collectunit_shop(tim_text, env_dir, fix_handle, _auto_output_to_public=True)
    ux.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    tim_deal = DealUnit(_healer=tim_text)
    tim_deal.set_fix_handle(fix_handle)
    ux.set_depot_deal(tim_deal, "blind_trust")

    # THEN
    assert os_path.exists(public_file_path)


def test_collectunit_auto_output_to_public_DoesNotSaveDealToPublicDirWhenFalse(
    collect_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_collectunit_dir()
    fix_handle = get_temp_fix_handle()
    tim_text = "Tim"
    public_file_title = f"{tim_text}.json"
    public_file_path = f"{get_temp_collectunit_dir()}/deals/{public_file_title}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/fix/examples/ex_env/deals/{public_file_title}"
    ux = collectunit_shop(tim_text, env_dir, fix_handle, _auto_output_to_public=False)
    ux.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    ux.set_depot_deal(DealUnit(_healer=tim_text), depotlink_type="blind_trust")

    # THEN
    assert os_path.exists(public_file_path) is False


def test_collectunit_get_seed_createsEmptyDealWhenFileDoesNotExist(
    collect_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_ux = collectunit_shop(
        tim_text, get_temp_collectunit_dir(), get_temp_fix_handle()
    )
    tim_ux.create_core_dir_and_files()
    assert os_path.exists(tim_ux._admin._seed_file_path)
    x_func_delete_dir(dir=tim_ux._admin._seed_file_path)
    assert os_path.exists(tim_ux._admin._seed_file_path) is False
    assert tim_ux._seed is None

    # WHEN
    cx_seed = tim_ux.get_seed()

    # THEN
    assert os_path.exists(tim_ux._admin._seed_file_path)
    assert tim_ux._seed != None


def test_collectunit_get_seed_getsMemoryDealIfExists(
    collect_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_ux = collectunit_shop(
        tim_text, get_temp_collectunit_dir(), get_temp_fix_handle()
    )
    tim_ux.create_core_dir_and_files()
    seed_file_path = (
        f"{tim_ux._admin._collectunit_dir}/{tim_ux._admin._seed_file_title}"
    )
    cx_seed1 = tim_ux.get_seed()
    assert os_path.exists(seed_file_path)
    assert tim_ux._seed != None

    # WHEN
    ray_text = "Ray"
    tim_ux._seed = DealUnit(_healer=ray_text)
    cx_seed2 = tim_ux.get_seed()

    # THEN
    assert cx_seed2._healer == ray_text
    assert cx_seed2 != cx_seed1

    # WHEN
    tim_ux._seed = None
    cx_seed3 = tim_ux.get_seed()

    # THEN
    assert cx_seed3._healer != ray_text
    assert cx_seed3 == cx_seed1


def test_collectunit_set_seed_savesseedDealSet_seed_None(
    collect_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_ux = collectunit_shop(
        tim_text, get_temp_collectunit_dir(), get_temp_fix_handle()
    )
    tim_ux.create_core_dir_and_files()
    seed_file_path = (
        f"{tim_ux._admin._collectunit_dir}/{tim_ux._admin._seed_file_title}"
    )
    cx_seed1 = tim_ux.get_seed()
    assert os_path.exists(seed_file_path)
    assert tim_ux._seed != None

    # WHEN
    uid_text = "Not a real uid"
    tim_ux._seed._idearoot._uid = uid_text
    tim_ux.set_seed()

    # THEN
    assert os_path.exists(seed_file_path)
    assert tim_ux._seed is None
    cx_seed2 = tim_ux.get_seed()
    assert cx_seed2._idearoot._uid == uid_text


def test_collectunit_set_seed_savesGivenDealSet_seed_None(
    collect_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    ux = collectunit_shop(tim_text, get_temp_collectunit_dir(), get_temp_fix_handle())
    ux.create_core_dir_and_files()
    seed_file_path = f"{ux._admin._collectunit_dir}/{ux._admin._seed_file_title}"
    cx_seed1 = ux.get_seed()
    assert os_path.exists(seed_file_path)
    assert ux._seed != None

    # WHEN
    seed_uid_text = "this is ._seed uid"
    ux._seed._idearoot._uid = seed_uid_text

    new_cx = DealUnit(_healer=tim_text)
    new_cx_uid_text = "this is pulled DealUnit uid"
    new_cx._idearoot._uid = new_cx_uid_text

    ux.set_seed(new_cx)

    # THEN
    assert os_path.exists(seed_file_path)
    assert ux._seed is None
    assert ux.get_seed()._idearoot._uid != seed_uid_text
    assert ux.get_seed()._idearoot._uid == new_cx_uid_text

    # GIVEN
    ux.set_seed(new_cx)
    assert os_path.exists(seed_file_path)
    assert ux._seed is None

    # WHEN
    ux.set_seed_if_empty()

    # THEN
    assert ux._seed != None
    assert os_path.exists(seed_file_path)

    # WHEN
    seed_uid_text = "this is ._seed uid"
    ux._seed._idearoot._uid = seed_uid_text


def test_collectunit_set_seed_if_emtpy_DoesNotReplace_seed(
    collect_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    ux = collectunit_shop(tim_text, get_temp_collectunit_dir(), get_temp_fix_handle())
    ux.create_core_dir_and_files()
    saved_cx = DealUnit(_healer=tim_text)
    saved_cx_uid_text = "this is pulled DealUnit uid"
    saved_cx._idearoot._uid = saved_cx_uid_text
    ux.set_seed(saved_cx)
    ux.get_seed()
    assert ux._seed != None

    # WHEN
    seed_uid_text = "this is ._seed uid"
    ux._seed._idearoot._uid = seed_uid_text
    ux.set_seed_if_empty()

    # THEN
    assert ux._seed != None
    assert ux._seed._idearoot._uid == seed_uid_text
    assert ux._seed._idearoot._uid != saved_cx_uid_text
