from src.deal.x_func import (
    open_file as x_func_open_file,
    save_file as x_func_save_file,
)
from src.fix.healing import HealingAdmin, healingadmin_shop
from src.fix.examples.example_healers import (
    get_6node_deal as example_healers_get_6node_deal,
    get_6node_deal as example_healers_get_7nodeJRootWithH_deal,
)
from src.fix.examples.healer_env_kit import (
    get_temp_healingunit_dir,
    get_temp_fix_handle,
    healer_dir_setup_cleanup,
)
from os import path as os_path


def test_admin_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_healingunit_dir()

    # WHEN
    pdx = HealingAdmin(bob_text, env_dir, get_temp_fix_handle())

    # THEN
    assert pdx._healing_title != None
    assert pdx._env_dir != None
    assert pdx._fix_handle != None
    assert pdx._healingunit_dir is None
    assert pdx._isol_file_title is None
    assert pdx._isol_file_path is None
    assert pdx._deal_output_file_title is None
    assert pdx._deal_output_file_path is None
    assert pdx._public_file_title is None
    assert pdx._deals_public_dir is None
    assert pdx._deals_depot_dir is None
    assert pdx._deals_ignore_dir is None
    assert pdx._deals_digest_dir is None


def test_HealingAdmin_set_dir_CorrectSetsHealingAdminAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_healingunit_dir()
    pdx = HealingAdmin(bob_text, env_dir, get_temp_fix_handle())
    assert pdx._healingunit_dir is None
    assert pdx._deal_output_file_title is None
    assert pdx._deal_output_file_path is None
    assert pdx._public_file_title is None
    assert pdx._deals_public_dir is None
    assert pdx._deals_depot_dir is None
    assert pdx._deals_ignore_dir is None
    assert pdx._deals_digest_dir is None
    assert pdx._isol_file_title is None
    assert pdx._isol_file_path is None
    # WHEN
    pdx.set_dirs()

    # THEN
    assert pdx._healingunit_dir != None
    assert pdx._deal_output_file_title != None
    assert pdx._deal_output_file_path != None
    assert pdx._public_file_title != None
    assert pdx._deals_public_dir != None
    assert pdx._deals_depot_dir != None
    assert pdx._deals_ignore_dir != None
    assert pdx._deals_digest_dir != None
    assert pdx._isol_file_title != None
    assert pdx._isol_file_path != None

    healers_drectory_folder = "healingunits"
    x_healingunits_dir = f"{env_dir}/{healers_drectory_folder}"
    x_healingunit_dir = f"{x_healingunits_dir}/{bob_text}"
    x_public_file_title = f"{bob_text}.json"
    x_isol_file_title = "isol_deal.json"
    x_isol_file_path = f"{x_healingunit_dir}/{x_isol_file_title}"
    x_deal_output_file_title = "output_deal.json"
    x_deal_output_file_path = f"{x_healingunit_dir}/{x_deal_output_file_title}"
    deals_str = "deals"
    x_deals_depot_dir = f"{x_healingunit_dir}/{deals_str}"
    x_deals_ignore_dir = f"{x_healingunit_dir}/ignores"
    x_deals_digest_dir = f"{x_healingunit_dir}/digests"
    x_deals_public_dir = f"{env_dir}/{deals_str}"
    assert pdx._healingunits_dir == x_healingunits_dir
    assert pdx._healingunit_dir == x_healingunit_dir
    assert pdx._isol_file_title == x_isol_file_title
    assert pdx._isol_file_path == x_isol_file_path
    assert pdx._deal_output_file_title == x_deal_output_file_title
    assert pdx._deal_output_file_path == x_deal_output_file_path
    assert pdx._deals_depot_dir == x_deals_depot_dir
    assert pdx._deals_ignore_dir == x_deals_ignore_dir
    assert pdx._deals_digest_dir == x_deals_digest_dir
    assert pdx._public_file_title == x_public_file_title
    assert pdx._deals_public_dir == x_deals_public_dir


def test_HealingAdmin_create_core_dir_and_files_CreatesDirsAndFiles(
    healer_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_healingunit_dir()
    pdx = HealingAdmin(jul_text, env_dir, get_temp_fix_handle())
    pdx.set_dirs()
    assert os_path.exists(pdx._healingunits_dir) is False
    assert os_path.exists(pdx._healingunit_dir) is False
    assert os_path.exists(pdx._isol_file_path) is False
    assert os_path.isdir(pdx._healingunit_dir) is False
    assert os_path.exists(pdx._deals_depot_dir) is False
    assert os_path.exists(pdx._deals_digest_dir) is False
    assert os_path.exists(pdx._deals_ignore_dir) is False

    # WHEN
    deal_x = example_healers_get_7nodeJRootWithH_deal()
    pdx.create_core_dir_and_files(deal_x)

    # THEN check deals src directory created
    print(f"Checking {pdx._healingunits_dir=}")
    print(f"Checking {pdx._healingunit_dir=}")
    assert os_path.exists(pdx._healingunits_dir)
    assert os_path.exists(pdx._healingunit_dir)
    assert os_path.exists(pdx._isol_file_path)
    assert os_path.isdir(pdx._healingunit_dir)
    assert os_path.exists(pdx._deals_depot_dir)
    assert os_path.exists(pdx._deals_digest_dir)
    assert os_path.exists(pdx._deals_ignore_dir)


def test_HealingAdmin_create_core_dir_and_files_DoesNotOverWriteIsolDeal(
    healer_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_healingunit_dir()
    jul_pdx = HealingAdmin(jul_text, env_dir, get_temp_fix_handle())
    jul_pdx.set_dirs()
    deal_x = example_healers_get_7nodeJRootWithH_deal()
    jul_pdx.create_core_dir_and_files(deal_x)
    assert os_path.exists(jul_pdx._isol_file_path)
    # jul_cx = deal_get_from_json(x_func_open_file(jul_pdx._isol_file_path))
    ex1 = "teesting text"
    x_func_save_file(
        dest_dir=jul_pdx._healingunit_dir,
        file_title=jul_pdx._isol_file_title,
        file_text=ex1,
    )
    assert x_func_open_file(jul_pdx._healingunit_dir, jul_pdx._isol_file_title) == ex1

    # WHEN
    jul_pdx.create_core_dir_and_files(deal_x)

    # THEN
    assert x_func_open_file(jul_pdx._healingunit_dir, jul_pdx._isol_file_title) == ex1


def test_HealingAdmin_set_healing_title_WorksCorrectly(healer_dir_setup_cleanup):
    # GIVEN create healer
    env_dir = get_temp_healingunit_dir()

    old_healer_text = "bob"
    pdx = HealingAdmin(old_healer_text, env_dir, get_temp_fix_handle())
    deal_x = example_healers_get_7nodeJRootWithH_deal()
    pdx.set_dirs()
    pdx.create_core_dir_and_files(deal_x)
    old_healingunit_dir = pdx._healingunit_dir
    # old_healingunit_dir = f"{env_dir}/healingunits/{old_healer_text}"
    print(f"{pdx._healingunit_dir}")
    print(f"{env_dir}/healingunits/{old_healer_text}")
    isol_file_title = "isol_deal.json"
    old_isol_file_path = f"{old_healingunit_dir}/{isol_file_title}"

    assert os_path.exists(old_healingunit_dir)
    assert os_path.isdir(old_healingunit_dir)
    assert os_path.exists(old_isol_file_path)

    new_healer_text = "tim"
    new_healingunit_dir = f"{env_dir}/healingunits/{new_healer_text}"
    new_isol_file_path = f"{new_healingunit_dir}/{isol_file_title}"
    assert os_path.exists(new_healingunit_dir) == False
    assert os_path.isdir(new_healingunit_dir) == False
    assert os_path.exists(new_isol_file_path) == False

    # WHEN
    pdx.set_healing_title(new_title=new_healer_text)

    # THEN
    assert os_path.exists(old_healingunit_dir) == False
    assert os_path.isdir(old_healingunit_dir) == False
    assert os_path.exists(old_isol_file_path) == False
    assert os_path.exists(new_healingunit_dir)
    assert os_path.isdir(new_healingunit_dir)
    assert os_path.exists(new_isol_file_path)


def test_healingunit_auto_output_to_public_SavesDealToPublicDir(
    healer_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    pdx = healingadmin_shop(bob_text, get_temp_healingunit_dir(), get_temp_fix_handle())
    deal_x = example_healers_get_6node_deal()
    deal_x.set_healer(new_healer=bob_text)
    pdx.create_core_dir_and_files(deal_x)

    public_file_path = f"{pdx._deals_public_dir}/{pdx._public_file_title}"
    print(f"{public_file_path=}")
    assert os_path.exists(public_file_path) is False

    # WHEN
    pdx.save_deal_to_public(deal_x=deal_x)

    # THEN
    assert os_path.exists(public_file_path)
