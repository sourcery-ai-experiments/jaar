from src.oath.oath import OathUnit
from src.oath.x_func import (
    count_files as x_func_count_files,
    open_file as x_func_open_file,
    delete_dir as x_func_delete_dir,
)
from src.cure.healing import healingunit_shop
from src.cure.examples.healer_env_kit import (
    healer_dir_setup_cleanup,
    get_temp_healingunit_dir,
    get_temp_cure_handle,
)
from os import path as os_path


def test_healingunit_exists(healer_dir_setup_cleanup):
    # GIVEN
    healer_text = "test1"

    # WHEN
    ux = healingunit_shop(
        title=healer_text,
        env_dir=get_temp_healingunit_dir(),
        cure_handle=get_temp_cure_handle(),
    )

    # GIVEN
    assert ux._admin._healing_title != None
    assert ux._admin._cure_handle != None
    assert ux._admin._cure_handle == get_temp_cure_handle()
    assert ux._isol is None


def test_healingunit_auto_output_to_public_SavesOathToPublicDirWhenTrue(
    healer_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_healingunit_dir()
    cure_handle = get_temp_cure_handle()
    tim_text = "Tim"
    public_file_title = f"{tim_text}.json"
    public_file_path = f"{get_temp_healingunit_dir()}/oaths/{public_file_title}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/cure/examples/ex_env/oaths/{public_file_title}"
    ux = healingunit_shop(tim_text, env_dir, cure_handle, _auto_output_to_public=True)
    ux.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    tim_oath = OathUnit(_healer=tim_text)
    tim_oath.set_cure_handle(cure_handle)
    ux.set_depot_oath(tim_oath, "blind_trust")

    # THEN
    assert os_path.exists(public_file_path)


def test_healingunit_auto_output_to_public_DoesNotSaveOathToPublicDirWhenFalse(
    healer_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_healingunit_dir()
    cure_handle = get_temp_cure_handle()
    tim_text = "Tim"
    public_file_title = f"{tim_text}.json"
    public_file_path = f"{get_temp_healingunit_dir()}/oaths/{public_file_title}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/cure/examples/ex_env/oaths/{public_file_title}"
    ux = healingunit_shop(tim_text, env_dir, cure_handle, _auto_output_to_public=False)
    ux.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    ux.set_depot_oath(OathUnit(_healer=tim_text), depotlink_type="blind_trust")

    # THEN
    assert os_path.exists(public_file_path) is False


def test_healingunit_get_isol_createsEmptyOathWhenFileDoesNotExist(
    healer_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_ux = healingunit_shop(
        tim_text, get_temp_healingunit_dir(), get_temp_cure_handle()
    )
    tim_ux.create_core_dir_and_files()
    assert os_path.exists(tim_ux._admin._isol_file_path)
    x_func_delete_dir(dir=tim_ux._admin._isol_file_path)
    assert os_path.exists(tim_ux._admin._isol_file_path) is False
    assert tim_ux._isol is None

    # WHEN
    cx_isol = tim_ux.get_isol()

    # THEN
    assert os_path.exists(tim_ux._admin._isol_file_path)
    assert tim_ux._isol != None


def test_healingunit_get_isol_getsMemoryOathIfExists(
    healer_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_ux = healingunit_shop(
        tim_text, get_temp_healingunit_dir(), get_temp_cure_handle()
    )
    tim_ux.create_core_dir_and_files()
    isol_file_path = (
        f"{tim_ux._admin._healingunit_dir}/{tim_ux._admin._isol_file_title}"
    )
    cx_isol1 = tim_ux.get_isol()
    assert os_path.exists(isol_file_path)
    assert tim_ux._isol != None

    # WHEN
    ray_text = "Ray"
    tim_ux._isol = OathUnit(_healer=ray_text)
    cx_isol2 = tim_ux.get_isol()

    # THEN
    assert cx_isol2._healer == ray_text
    assert cx_isol2 != cx_isol1

    # WHEN
    tim_ux._isol = None
    cx_isol3 = tim_ux.get_isol()

    # THEN
    assert cx_isol3._healer != ray_text
    assert cx_isol3 == cx_isol1


def test_healingunit_set_isol_savesIsolOathSet_isol_None(
    healer_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_ux = healingunit_shop(
        tim_text, get_temp_healingunit_dir(), get_temp_cure_handle()
    )
    tim_ux.create_core_dir_and_files()
    isol_file_path = (
        f"{tim_ux._admin._healingunit_dir}/{tim_ux._admin._isol_file_title}"
    )
    cx_isol1 = tim_ux.get_isol()
    assert os_path.exists(isol_file_path)
    assert tim_ux._isol != None

    # WHEN
    uid_text = "Not a real uid"
    tim_ux._isol._idearoot._uid = uid_text
    tim_ux.set_isol()

    # THEN
    assert os_path.exists(isol_file_path)
    assert tim_ux._isol is None
    cx_isol2 = tim_ux.get_isol()
    assert cx_isol2._idearoot._uid == uid_text


def test_healingunit_set_isol_savesGivenOathSet_isol_None(
    healer_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    ux = healingunit_shop(tim_text, get_temp_healingunit_dir(), get_temp_cure_handle())
    ux.create_core_dir_and_files()
    isol_file_path = f"{ux._admin._healingunit_dir}/{ux._admin._isol_file_title}"
    cx_isol1 = ux.get_isol()
    assert os_path.exists(isol_file_path)
    assert ux._isol != None

    # WHEN
    isol_uid_text = "this is ._isol uid"
    ux._isol._idearoot._uid = isol_uid_text

    new_cx = OathUnit(_healer=tim_text)
    new_cx_uid_text = "this is pulled OathUnit uid"
    new_cx._idearoot._uid = new_cx_uid_text

    ux.set_isol(new_cx)

    # THEN
    assert os_path.exists(isol_file_path)
    assert ux._isol is None
    assert ux.get_isol()._idearoot._uid != isol_uid_text
    assert ux.get_isol()._idearoot._uid == new_cx_uid_text

    # GIVEN
    ux.set_isol(new_cx)
    assert os_path.exists(isol_file_path)
    assert ux._isol is None

    # WHEN
    ux.set_isol_if_empty()

    # THEN
    assert ux._isol != None
    assert os_path.exists(isol_file_path)

    # WHEN
    isol_uid_text = "this is ._isol uid"
    ux._isol._idearoot._uid = isol_uid_text


def test_healingunit_set_isol_if_emtpy_DoesNotReplace_isol(
    healer_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    ux = healingunit_shop(tim_text, get_temp_healingunit_dir(), get_temp_cure_handle())
    ux.create_core_dir_and_files()
    saved_cx = OathUnit(_healer=tim_text)
    saved_cx_uid_text = "this is pulled OathUnit uid"
    saved_cx._idearoot._uid = saved_cx_uid_text
    ux.set_isol(saved_cx)
    ux.get_isol()
    assert ux._isol != None

    # WHEN
    isol_uid_text = "this is ._isol uid"
    ux._isol._idearoot._uid = isol_uid_text
    ux.set_isol_if_empty()

    # THEN
    assert ux._isol != None
    assert ux._isol._idearoot._uid == isol_uid_text
    assert ux._isol._idearoot._uid != saved_cx_uid_text
