from src.deal.x_func import (
    open_file as x_func_open_file,
    save_file as x_func_save_file,
)
from src.project.kitchen import KitchenAdmin, kitchenadmin_shop
from src.project.examples.example_kitchens import (
    get_6node_deal as example_healers_get_6node_deal,
    get_6node_deal as example_healers_get_7nodeJRootWithH_deal,
)
from src.project.examples.kitchen_env_kit import (
    get_temp_kitchenunit_dir,
    get_temp_project_handle,
    kitchen_dir_setup_cleanup,
)
from os import path as os_path


def test_KitchenAdmin_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_kitchenunit_dir()

    # WHEN
    bob_kitchenadmin = KitchenAdmin(bob_text, env_dir, get_temp_project_handle())

    # THEN
    assert bob_kitchenadmin._kitchen_title != None
    assert bob_kitchenadmin._env_dir != None
    assert bob_kitchenadmin._project_handle != None
    assert bob_kitchenadmin._kitchenunit_dir is None
    assert bob_kitchenadmin._seed_file_title is None
    assert bob_kitchenadmin._seed_file_path is None
    assert bob_kitchenadmin._deal_output_file_title is None
    assert bob_kitchenadmin._deal_output_file_path is None
    assert bob_kitchenadmin._public_file_title is None
    assert bob_kitchenadmin._deals_public_dir is None
    assert bob_kitchenadmin._deals_depot_dir is None
    assert bob_kitchenadmin._deals_ignore_dir is None
    assert bob_kitchenadmin._deals_digest_dir is None


def test_KitchenAdmin_set_dir_CorrectSetsKitchenAdminAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_kitchenunit_dir()
    bob_kitchenadmin = KitchenAdmin(bob_text, env_dir, get_temp_project_handle())
    assert bob_kitchenadmin._kitchenunit_dir is None
    assert bob_kitchenadmin._deal_output_file_title is None
    assert bob_kitchenadmin._deal_output_file_path is None
    assert bob_kitchenadmin._public_file_title is None
    assert bob_kitchenadmin._deals_public_dir is None
    assert bob_kitchenadmin._deals_depot_dir is None
    assert bob_kitchenadmin._deals_ignore_dir is None
    assert bob_kitchenadmin._deals_digest_dir is None
    assert bob_kitchenadmin._seed_file_title is None
    assert bob_kitchenadmin._seed_file_path is None
    # WHEN
    bob_kitchenadmin.set_dirs()

    # THEN
    assert bob_kitchenadmin._kitchenunit_dir != None
    assert bob_kitchenadmin._deal_output_file_title != None
    assert bob_kitchenadmin._deal_output_file_path != None
    assert bob_kitchenadmin._public_file_title != None
    assert bob_kitchenadmin._deals_public_dir != None
    assert bob_kitchenadmin._deals_depot_dir != None
    assert bob_kitchenadmin._deals_ignore_dir != None
    assert bob_kitchenadmin._deals_digest_dir != None
    assert bob_kitchenadmin._seed_file_title != None
    assert bob_kitchenadmin._seed_file_path != None

    healers_drectory_folder = "kitchenunits"
    x_kitchenunits_dir = f"{env_dir}/{healers_drectory_folder}"
    x_kitchenunit_dir = f"{x_kitchenunits_dir}/{bob_text}"
    x_public_file_title = f"{bob_text}.json"
    x_seed_file_title = "seed_deal.json"
    x_seed_file_path = f"{x_kitchenunit_dir}/{x_seed_file_title}"
    x_deal_output_file_title = "output_deal.json"
    x_deal_output_file_path = f"{x_kitchenunit_dir}/{x_deal_output_file_title}"
    deals_str = "deals"
    x_deals_depot_dir = f"{x_kitchenunit_dir}/{deals_str}"
    x_deals_ignore_dir = f"{x_kitchenunit_dir}/ignores"
    x_deals_digest_dir = f"{x_kitchenunit_dir}/digests"
    x_deals_public_dir = f"{env_dir}/{deals_str}"
    assert bob_kitchenadmin._kitchenunits_dir == x_kitchenunits_dir
    assert bob_kitchenadmin._kitchenunit_dir == x_kitchenunit_dir
    assert bob_kitchenadmin._seed_file_title == x_seed_file_title
    assert bob_kitchenadmin._seed_file_path == x_seed_file_path
    assert bob_kitchenadmin._deal_output_file_title == x_deal_output_file_title
    assert bob_kitchenadmin._deal_output_file_path == x_deal_output_file_path
    assert bob_kitchenadmin._deals_depot_dir == x_deals_depot_dir
    assert bob_kitchenadmin._deals_ignore_dir == x_deals_ignore_dir
    assert bob_kitchenadmin._deals_digest_dir == x_deals_digest_dir
    assert bob_kitchenadmin._public_file_title == x_public_file_title
    assert bob_kitchenadmin._deals_public_dir == x_deals_public_dir


def test_KitchenAdmin_create_core_dir_and_files_CreatesDirsAndFiles(
    kitchen_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_kitchenunit_dir()
    jul_kitchenadmin = kitchenadmin_shop(jul_text, env_dir, get_temp_project_handle())
    jul_kitchenadmin.set_dirs()
    assert os_path.exists(jul_kitchenadmin._kitchenunits_dir) is False
    assert os_path.exists(jul_kitchenadmin._kitchenunit_dir) is False
    assert os_path.exists(jul_kitchenadmin._seed_file_path) is False
    assert os_path.isdir(jul_kitchenadmin._kitchenunit_dir) is False
    assert os_path.exists(jul_kitchenadmin._deals_depot_dir) is False
    assert os_path.exists(jul_kitchenadmin._deals_digest_dir) is False
    assert os_path.exists(jul_kitchenadmin._deals_ignore_dir) is False

    # WHEN
    x_deal = example_healers_get_7nodeJRootWithH_deal()
    jul_kitchenadmin.create_core_dir_and_files(x_deal)

    # THEN check deals src directory created
    print(f"Checking {jul_kitchenadmin._kitchenunits_dir=}")
    print(f"Checking {jul_kitchenadmin._kitchenunit_dir=}")
    assert os_path.exists(jul_kitchenadmin._kitchenunits_dir)
    assert os_path.exists(jul_kitchenadmin._kitchenunit_dir)
    assert os_path.exists(jul_kitchenadmin._seed_file_path)
    assert os_path.isdir(jul_kitchenadmin._kitchenunit_dir)
    assert os_path.exists(jul_kitchenadmin._deals_depot_dir)
    assert os_path.exists(jul_kitchenadmin._deals_digest_dir)
    assert os_path.exists(jul_kitchenadmin._deals_ignore_dir)


def test_KitchenAdmin_create_core_dir_and_files_DoesNotOverWriteseedDeal(
    kitchen_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_kitchenunit_dir()
    jul_kitchenadmin = kitchenadmin_shop(jul_text, env_dir, get_temp_project_handle())
    jul_kitchenadmin.set_dirs()
    x_deal = example_healers_get_7nodeJRootWithH_deal()
    jul_kitchenadmin.create_core_dir_and_files(x_deal)
    assert os_path.exists(jul_kitchenadmin._seed_file_path)
    # jul_cx = deal_get_from_json(x_func_open_file(jul_kitchenadmin._seed_file_path))
    ex1 = "teesting text"
    x_func_save_file(
        dest_dir=jul_kitchenadmin._kitchenunit_dir,
        file_title=jul_kitchenadmin._seed_file_title,
        file_text=ex1,
    )
    assert (
        x_func_open_file(
            jul_kitchenadmin._kitchenunit_dir, jul_kitchenadmin._seed_file_title
        )
        == ex1
    )

    # WHEN
    jul_kitchenadmin.create_core_dir_and_files(x_deal)

    # THEN
    assert (
        x_func_open_file(
            jul_kitchenadmin._kitchenunit_dir, jul_kitchenadmin._seed_file_title
        )
        == ex1
    )


def test_KitchenAdmin_set_kitchen_title_WorksCorrectly(kitchen_dir_setup_cleanup):
    # GIVEN create healer
    env_dir = get_temp_kitchenunit_dir()

    old_healer_text = "bob"
    jul_kitchenadmin = kitchenadmin_shop(
        old_healer_text, env_dir, get_temp_project_handle()
    )
    x_deal = example_healers_get_7nodeJRootWithH_deal()
    jul_kitchenadmin.set_dirs()
    jul_kitchenadmin.create_core_dir_and_files(x_deal)
    old_kitchenunit_dir = jul_kitchenadmin._kitchenunit_dir
    # old_kitchenunit_dir = f"{env_dir}/kitchenunits/{old_healer_text}"
    print(f"{jul_kitchenadmin._kitchenunit_dir}")
    print(f"{env_dir}/kitchenunits/{old_healer_text}")
    seed_file_title = "seed_deal.json"
    old_seed_file_path = f"{old_kitchenunit_dir}/{seed_file_title}"

    assert os_path.exists(old_kitchenunit_dir)
    assert os_path.isdir(old_kitchenunit_dir)
    assert os_path.exists(old_seed_file_path)

    new_healer_text = "tim"
    new_kitchenunit_dir = f"{env_dir}/kitchenunits/{new_healer_text}"
    new_seed_file_path = f"{new_kitchenunit_dir}/{seed_file_title}"
    assert os_path.exists(new_kitchenunit_dir) == False
    assert os_path.isdir(new_kitchenunit_dir) == False
    assert os_path.exists(new_seed_file_path) == False

    # WHEN
    jul_kitchenadmin.set_kitchen_title(new_title=new_healer_text)

    # THEN
    assert os_path.exists(old_kitchenunit_dir) == False
    assert os_path.isdir(old_kitchenunit_dir) == False
    assert os_path.exists(old_seed_file_path) == False
    assert os_path.exists(new_kitchenunit_dir)
    assert os_path.isdir(new_kitchenunit_dir)
    assert os_path.exists(new_seed_file_path)


def test_kitchenunit_auto_output_to_public_SavesDealToPublicDir(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    bob_kitchenadmin = kitchenadmin_shop(
        bob_text, get_temp_kitchenunit_dir(), get_temp_project_handle()
    )
    x_deal = example_healers_get_6node_deal()
    x_deal.set_healer(new_healer=bob_text)
    bob_kitchenadmin.create_core_dir_and_files(x_deal)

    public_file_path = (
        f"{bob_kitchenadmin._deals_public_dir}/{bob_kitchenadmin._public_file_title}"
    )
    print(f"{public_file_path=}")
    assert os_path.exists(public_file_path) is False

    # WHEN
    bob_kitchenadmin.save_deal_to_public(x_deal)

    # THEN
    assert os_path.exists(public_file_path)
