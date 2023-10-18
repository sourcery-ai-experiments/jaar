from src.deal.x_func import (
    open_file as x_func_open_file,
    save_file as x_func_save_file,
)
from src.project.harvest import HarvestAdmin, harvestadmin_shop
from src.project.examples.example_harvests import (
    get_6node_deal as example_healers_get_6node_deal,
    get_6node_deal as example_healers_get_7nodeJRootWithH_deal,
)
from src.project.examples.harvest_env_kit import (
    get_temp_harvestunit_dir,
    get_temp_project_handle,
    harvest_dir_setup_cleanup,
)
from os import path as os_path


def test_HarvestAdmin_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_harvestunit_dir()

    # WHEN
    pdx = HarvestAdmin(bob_text, env_dir, get_temp_project_handle())

    # THEN
    assert pdx._harvest_title != None
    assert pdx._env_dir != None
    assert pdx._project_handle != None
    assert pdx._harvestunit_dir is None
    assert pdx._seed_file_title is None
    assert pdx._seed_file_path is None
    assert pdx._deal_output_file_title is None
    assert pdx._deal_output_file_path is None
    assert pdx._public_file_title is None
    assert pdx._deals_public_dir is None
    assert pdx._deals_depot_dir is None
    assert pdx._deals_ignore_dir is None
    assert pdx._deals_digest_dir is None


def test_HarvestAdmin_set_dir_CorrectSetsHarvestAdminAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_harvestunit_dir()
    pdx = HarvestAdmin(bob_text, env_dir, get_temp_project_handle())
    assert pdx._harvestunit_dir is None
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
    assert pdx._harvestunit_dir != None
    assert pdx._deal_output_file_title != None
    assert pdx._deal_output_file_path != None
    assert pdx._public_file_title != None
    assert pdx._deals_public_dir != None
    assert pdx._deals_depot_dir != None
    assert pdx._deals_ignore_dir != None
    assert pdx._deals_digest_dir != None
    assert pdx._seed_file_title != None
    assert pdx._seed_file_path != None

    healers_drectory_folder = "harvestunits"
    x_harvestunits_dir = f"{env_dir}/{healers_drectory_folder}"
    x_harvestunit_dir = f"{x_harvestunits_dir}/{bob_text}"
    x_public_file_title = f"{bob_text}.json"
    x_seed_file_title = "seed_deal.json"
    x_seed_file_path = f"{x_harvestunit_dir}/{x_seed_file_title}"
    x_deal_output_file_title = "output_deal.json"
    x_deal_output_file_path = f"{x_harvestunit_dir}/{x_deal_output_file_title}"
    deals_str = "deals"
    x_deals_depot_dir = f"{x_harvestunit_dir}/{deals_str}"
    x_deals_ignore_dir = f"{x_harvestunit_dir}/ignores"
    x_deals_digest_dir = f"{x_harvestunit_dir}/digests"
    x_deals_public_dir = f"{env_dir}/{deals_str}"
    assert pdx._harvestunits_dir == x_harvestunits_dir
    assert pdx._harvestunit_dir == x_harvestunit_dir
    assert pdx._seed_file_title == x_seed_file_title
    assert pdx._seed_file_path == x_seed_file_path
    assert pdx._deal_output_file_title == x_deal_output_file_title
    assert pdx._deal_output_file_path == x_deal_output_file_path
    assert pdx._deals_depot_dir == x_deals_depot_dir
    assert pdx._deals_ignore_dir == x_deals_ignore_dir
    assert pdx._deals_digest_dir == x_deals_digest_dir
    assert pdx._public_file_title == x_public_file_title
    assert pdx._deals_public_dir == x_deals_public_dir


def test_HarvestAdmin_create_core_dir_and_files_CreatesDirsAndFiles(
    harvest_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_harvestunit_dir()
    pdx = harvestadmin_shop(jul_text, env_dir, get_temp_project_handle())
    pdx.set_dirs()
    assert os_path.exists(pdx._harvestunits_dir) is False
    assert os_path.exists(pdx._harvestunit_dir) is False
    assert os_path.exists(pdx._seed_file_path) is False
    assert os_path.isdir(pdx._harvestunit_dir) is False
    assert os_path.exists(pdx._deals_depot_dir) is False
    assert os_path.exists(pdx._deals_digest_dir) is False
    assert os_path.exists(pdx._deals_ignore_dir) is False

    # WHEN
    deal_x = example_healers_get_7nodeJRootWithH_deal()
    pdx.create_core_dir_and_files(deal_x)

    # THEN check deals src directory created
    print(f"Checking {pdx._harvestunits_dir=}")
    print(f"Checking {pdx._harvestunit_dir=}")
    assert os_path.exists(pdx._harvestunits_dir)
    assert os_path.exists(pdx._harvestunit_dir)
    assert os_path.exists(pdx._seed_file_path)
    assert os_path.isdir(pdx._harvestunit_dir)
    assert os_path.exists(pdx._deals_depot_dir)
    assert os_path.exists(pdx._deals_digest_dir)
    assert os_path.exists(pdx._deals_ignore_dir)


def test_HarvestAdmin_create_core_dir_and_files_DoesNotOverWriteseedDeal(
    harvest_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_harvestunit_dir()
    jul_pdx = harvestadmin_shop(jul_text, env_dir, get_temp_project_handle())
    jul_pdx.set_dirs()
    deal_x = example_healers_get_7nodeJRootWithH_deal()
    jul_pdx.create_core_dir_and_files(deal_x)
    assert os_path.exists(jul_pdx._seed_file_path)
    # jul_cx = deal_get_from_json(x_func_open_file(jul_pdx._seed_file_path))
    ex1 = "teesting text"
    x_func_save_file(
        dest_dir=jul_pdx._harvestunit_dir,
        file_title=jul_pdx._seed_file_title,
        file_text=ex1,
    )
    assert x_func_open_file(jul_pdx._harvestunit_dir, jul_pdx._seed_file_title) == ex1

    # WHEN
    jul_pdx.create_core_dir_and_files(deal_x)

    # THEN
    assert x_func_open_file(jul_pdx._harvestunit_dir, jul_pdx._seed_file_title) == ex1


def test_HarvestAdmin_set_harvest_title_WorksCorrectly(harvest_dir_setup_cleanup):
    # GIVEN create healer
    env_dir = get_temp_harvestunit_dir()

    old_healer_text = "bob"
    pdx = harvestadmin_shop(old_healer_text, env_dir, get_temp_project_handle())
    deal_x = example_healers_get_7nodeJRootWithH_deal()
    pdx.set_dirs()
    pdx.create_core_dir_and_files(deal_x)
    old_harvestunit_dir = pdx._harvestunit_dir
    # old_harvestunit_dir = f"{env_dir}/harvestunits/{old_healer_text}"
    print(f"{pdx._harvestunit_dir}")
    print(f"{env_dir}/harvestunits/{old_healer_text}")
    seed_file_title = "seed_deal.json"
    old_seed_file_path = f"{old_harvestunit_dir}/{seed_file_title}"

    assert os_path.exists(old_harvestunit_dir)
    assert os_path.isdir(old_harvestunit_dir)
    assert os_path.exists(old_seed_file_path)

    new_healer_text = "tim"
    new_harvestunit_dir = f"{env_dir}/harvestunits/{new_healer_text}"
    new_seed_file_path = f"{new_harvestunit_dir}/{seed_file_title}"
    assert os_path.exists(new_harvestunit_dir) == False
    assert os_path.isdir(new_harvestunit_dir) == False
    assert os_path.exists(new_seed_file_path) == False

    # WHEN
    pdx.set_harvest_title(new_title=new_healer_text)

    # THEN
    assert os_path.exists(old_harvestunit_dir) == False
    assert os_path.isdir(old_harvestunit_dir) == False
    assert os_path.exists(old_seed_file_path) == False
    assert os_path.exists(new_harvestunit_dir)
    assert os_path.isdir(new_harvestunit_dir)
    assert os_path.exists(new_seed_file_path)


def test_harvestunit_auto_output_to_public_SavesDealToPublicDir(
    harvest_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    pdx = harvestadmin_shop(
        bob_text, get_temp_harvestunit_dir(), get_temp_project_handle()
    )
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
