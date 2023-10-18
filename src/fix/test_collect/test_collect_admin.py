from src.deal.x_func import (
    open_file as x_func_open_file,
    save_file as x_func_save_file,
)
from src.fix.collect import CollectAdmin, collectadmin_shop
from src.fix.examples.example_collects import (
    get_6node_deal as example_healers_get_6node_deal,
    get_6node_deal as example_healers_get_7nodeJRootWithH_deal,
)
from src.fix.examples.collect_env_kit import (
    get_temp_collectunit_dir,
    get_temp_fix_handle,
    collect_dir_setup_cleanup,
)
from os import path as os_path


def test_admin_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_collectunit_dir()

    # WHEN
    pdx = CollectAdmin(bob_text, env_dir, get_temp_fix_handle())

    # THEN
    assert pdx._collect_title != None
    assert pdx._env_dir != None
    assert pdx._fix_handle != None
    assert pdx._collectunit_dir is None
    assert pdx._seed_file_title is None
    assert pdx._seed_file_path is None
    assert pdx._deal_output_file_title is None
    assert pdx._deal_output_file_path is None
    assert pdx._public_file_title is None
    assert pdx._deals_public_dir is None
    assert pdx._deals_depot_dir is None
    assert pdx._deals_ignore_dir is None
    assert pdx._deals_digest_dir is None


def test_CollectAdmin_set_dir_CorrectSetsCollectAdminAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_collectunit_dir()
    pdx = CollectAdmin(bob_text, env_dir, get_temp_fix_handle())
    assert pdx._collectunit_dir is None
    assert pdx._deal_output_file_title is None
    assert pdx._deal_output_file_path is None
    assert pdx._public_file_title is None
    assert pdx._deals_public_dir is None
    assert pdx._deals_depot_dir is None
    assert pdx._deals_ignore_dir is None
    assert pdx._deals_digest_dir is None
    assert pdx._seed_file_title is None
    assert pdx._seed_file_path is None
    # WHEN
    pdx.set_dirs()

    # THEN
    assert pdx._collectunit_dir != None
    assert pdx._deal_output_file_title != None
    assert pdx._deal_output_file_path != None
    assert pdx._public_file_title != None
    assert pdx._deals_public_dir != None
    assert pdx._deals_depot_dir != None
    assert pdx._deals_ignore_dir != None
    assert pdx._deals_digest_dir != None
    assert pdx._seed_file_title != None
    assert pdx._seed_file_path != None

    healers_drectory_folder = "collectunits"
    x_collectunits_dir = f"{env_dir}/{healers_drectory_folder}"
    x_collectunit_dir = f"{x_collectunits_dir}/{bob_text}"
    x_public_file_title = f"{bob_text}.json"
    x_seed_file_title = "seed_deal.json"
    x_seed_file_path = f"{x_collectunit_dir}/{x_seed_file_title}"
    x_deal_output_file_title = "output_deal.json"
    x_deal_output_file_path = f"{x_collectunit_dir}/{x_deal_output_file_title}"
    deals_str = "deals"
    x_deals_depot_dir = f"{x_collectunit_dir}/{deals_str}"
    x_deals_ignore_dir = f"{x_collectunit_dir}/ignores"
    x_deals_digest_dir = f"{x_collectunit_dir}/digests"
    x_deals_public_dir = f"{env_dir}/{deals_str}"
    assert pdx._collectunits_dir == x_collectunits_dir
    assert pdx._collectunit_dir == x_collectunit_dir
    assert pdx._seed_file_title == x_seed_file_title
    assert pdx._seed_file_path == x_seed_file_path
    assert pdx._deal_output_file_title == x_deal_output_file_title
    assert pdx._deal_output_file_path == x_deal_output_file_path
    assert pdx._deals_depot_dir == x_deals_depot_dir
    assert pdx._deals_ignore_dir == x_deals_ignore_dir
    assert pdx._deals_digest_dir == x_deals_digest_dir
    assert pdx._public_file_title == x_public_file_title
    assert pdx._deals_public_dir == x_deals_public_dir


def test_CollectAdmin_create_core_dir_and_files_CreatesDirsAndFiles(
    collect_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_collectunit_dir()
    pdx = CollectAdmin(jul_text, env_dir, get_temp_fix_handle())
    pdx.set_dirs()
    assert os_path.exists(pdx._collectunits_dir) is False
    assert os_path.exists(pdx._collectunit_dir) is False
    assert os_path.exists(pdx._seed_file_path) is False
    assert os_path.isdir(pdx._collectunit_dir) is False
    assert os_path.exists(pdx._deals_depot_dir) is False
    assert os_path.exists(pdx._deals_digest_dir) is False
    assert os_path.exists(pdx._deals_ignore_dir) is False

    # WHEN
    deal_x = example_healers_get_7nodeJRootWithH_deal()
    pdx.create_core_dir_and_files(deal_x)

    # THEN check deals src directory created
    print(f"Checking {pdx._collectunits_dir=}")
    print(f"Checking {pdx._collectunit_dir=}")
    assert os_path.exists(pdx._collectunits_dir)
    assert os_path.exists(pdx._collectunit_dir)
    assert os_path.exists(pdx._seed_file_path)
    assert os_path.isdir(pdx._collectunit_dir)
    assert os_path.exists(pdx._deals_depot_dir)
    assert os_path.exists(pdx._deals_digest_dir)
    assert os_path.exists(pdx._deals_ignore_dir)


def test_CollectAdmin_create_core_dir_and_files_DoesNotOverWriteseedDeal(
    collect_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_collectunit_dir()
    jul_pdx = CollectAdmin(jul_text, env_dir, get_temp_fix_handle())
    jul_pdx.set_dirs()
    deal_x = example_healers_get_7nodeJRootWithH_deal()
    jul_pdx.create_core_dir_and_files(deal_x)
    assert os_path.exists(jul_pdx._seed_file_path)
    # jul_cx = deal_get_from_json(x_func_open_file(jul_pdx._seed_file_path))
    ex1 = "teesting text"
    x_func_save_file(
        dest_dir=jul_pdx._collectunit_dir,
        file_title=jul_pdx._seed_file_title,
        file_text=ex1,
    )
    assert x_func_open_file(jul_pdx._collectunit_dir, jul_pdx._seed_file_title) == ex1

    # WHEN
    jul_pdx.create_core_dir_and_files(deal_x)

    # THEN
    assert x_func_open_file(jul_pdx._collectunit_dir, jul_pdx._seed_file_title) == ex1


def test_CollectAdmin_set_collect_title_WorksCorrectly(collect_dir_setup_cleanup):
    # GIVEN create healer
    env_dir = get_temp_collectunit_dir()

    old_healer_text = "bob"
    pdx = CollectAdmin(old_healer_text, env_dir, get_temp_fix_handle())
    deal_x = example_healers_get_7nodeJRootWithH_deal()
    pdx.set_dirs()
    pdx.create_core_dir_and_files(deal_x)
    old_collectunit_dir = pdx._collectunit_dir
    # old_collectunit_dir = f"{env_dir}/collectunits/{old_healer_text}"
    print(f"{pdx._collectunit_dir}")
    print(f"{env_dir}/collectunits/{old_healer_text}")
    seed_file_title = "seed_deal.json"
    old_seed_file_path = f"{old_collectunit_dir}/{seed_file_title}"

    assert os_path.exists(old_collectunit_dir)
    assert os_path.isdir(old_collectunit_dir)
    assert os_path.exists(old_seed_file_path)

    new_healer_text = "tim"
    new_collectunit_dir = f"{env_dir}/collectunits/{new_healer_text}"
    new_seed_file_path = f"{new_collectunit_dir}/{seed_file_title}"
    assert os_path.exists(new_collectunit_dir) == False
    assert os_path.isdir(new_collectunit_dir) == False
    assert os_path.exists(new_seed_file_path) == False

    # WHEN
    pdx.set_collect_title(new_title=new_healer_text)

    # THEN
    assert os_path.exists(old_collectunit_dir) == False
    assert os_path.isdir(old_collectunit_dir) == False
    assert os_path.exists(old_seed_file_path) == False
    assert os_path.exists(new_collectunit_dir)
    assert os_path.isdir(new_collectunit_dir)
    assert os_path.exists(new_seed_file_path)


def test_collectunit_auto_output_to_public_SavesDealToPublicDir(
    collect_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    pdx = collectadmin_shop(bob_text, get_temp_collectunit_dir(), get_temp_fix_handle())
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
