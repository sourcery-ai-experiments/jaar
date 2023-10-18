from src.deal.x_func import (
    open_file as x_func_open_file,
    save_file as x_func_save_file,
)
from src.fix.remedy import RemedyAdmin, remedyadmin_shop
from src.fix.examples.example_remedys import (
    get_6node_deal as example_healers_get_6node_deal,
    get_6node_deal as example_healers_get_7nodeJRootWithH_deal,
)
from src.fix.examples.remedy_env_kit import (
    get_temp_remedyunit_dir,
    get_temp_fix_handle,
    remedy_dir_setup_cleanup,
)
from os import path as os_path


def test_admin_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_remedyunit_dir()

    # WHEN
    pdx = RemedyAdmin(bob_text, env_dir, get_temp_fix_handle())

    # THEN
    assert pdx._remedy_title != None
    assert pdx._env_dir != None
    assert pdx._fix_handle != None
    assert pdx._remedyunit_dir is None
    assert pdx._isol_file_title is None
    assert pdx._isol_file_path is None
    assert pdx._deal_output_file_title is None
    assert pdx._deal_output_file_path is None
    assert pdx._public_file_title is None
    assert pdx._deals_public_dir is None
    assert pdx._deals_depot_dir is None
    assert pdx._deals_ignore_dir is None
    assert pdx._deals_digest_dir is None


def test_RemedyAdmin_set_dir_CorrectSetsRemedyAdminAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_remedyunit_dir()
    pdx = RemedyAdmin(bob_text, env_dir, get_temp_fix_handle())
    assert pdx._remedyunit_dir is None
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
    assert pdx._remedyunit_dir != None
    assert pdx._deal_output_file_title != None
    assert pdx._deal_output_file_path != None
    assert pdx._public_file_title != None
    assert pdx._deals_public_dir != None
    assert pdx._deals_depot_dir != None
    assert pdx._deals_ignore_dir != None
    assert pdx._deals_digest_dir != None
    assert pdx._isol_file_title != None
    assert pdx._isol_file_path != None

    healers_drectory_folder = "remedyunits"
    x_remedyunits_dir = f"{env_dir}/{healers_drectory_folder}"
    x_remedyunit_dir = f"{x_remedyunits_dir}/{bob_text}"
    x_public_file_title = f"{bob_text}.json"
    x_isol_file_title = "isol_deal.json"
    x_isol_file_path = f"{x_remedyunit_dir}/{x_isol_file_title}"
    x_deal_output_file_title = "output_deal.json"
    x_deal_output_file_path = f"{x_remedyunit_dir}/{x_deal_output_file_title}"
    deals_str = "deals"
    x_deals_depot_dir = f"{x_remedyunit_dir}/{deals_str}"
    x_deals_ignore_dir = f"{x_remedyunit_dir}/ignores"
    x_deals_digest_dir = f"{x_remedyunit_dir}/digests"
    x_deals_public_dir = f"{env_dir}/{deals_str}"
    assert pdx._remedyunits_dir == x_remedyunits_dir
    assert pdx._remedyunit_dir == x_remedyunit_dir
    assert pdx._isol_file_title == x_isol_file_title
    assert pdx._isol_file_path == x_isol_file_path
    assert pdx._deal_output_file_title == x_deal_output_file_title
    assert pdx._deal_output_file_path == x_deal_output_file_path
    assert pdx._deals_depot_dir == x_deals_depot_dir
    assert pdx._deals_ignore_dir == x_deals_ignore_dir
    assert pdx._deals_digest_dir == x_deals_digest_dir
    assert pdx._public_file_title == x_public_file_title
    assert pdx._deals_public_dir == x_deals_public_dir


def test_RemedyAdmin_create_core_dir_and_files_CreatesDirsAndFiles(
    remedy_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_remedyunit_dir()
    pdx = RemedyAdmin(jul_text, env_dir, get_temp_fix_handle())
    pdx.set_dirs()
    assert os_path.exists(pdx._remedyunits_dir) is False
    assert os_path.exists(pdx._remedyunit_dir) is False
    assert os_path.exists(pdx._isol_file_path) is False
    assert os_path.isdir(pdx._remedyunit_dir) is False
    assert os_path.exists(pdx._deals_depot_dir) is False
    assert os_path.exists(pdx._deals_digest_dir) is False
    assert os_path.exists(pdx._deals_ignore_dir) is False

    # WHEN
    deal_x = example_healers_get_7nodeJRootWithH_deal()
    pdx.create_core_dir_and_files(deal_x)

    # THEN check deals src directory created
    print(f"Checking {pdx._remedyunits_dir=}")
    print(f"Checking {pdx._remedyunit_dir=}")
    assert os_path.exists(pdx._remedyunits_dir)
    assert os_path.exists(pdx._remedyunit_dir)
    assert os_path.exists(pdx._isol_file_path)
    assert os_path.isdir(pdx._remedyunit_dir)
    assert os_path.exists(pdx._deals_depot_dir)
    assert os_path.exists(pdx._deals_digest_dir)
    assert os_path.exists(pdx._deals_ignore_dir)


def test_RemedyAdmin_create_core_dir_and_files_DoesNotOverWriteIsolDeal(
    remedy_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_remedyunit_dir()
    jul_pdx = RemedyAdmin(jul_text, env_dir, get_temp_fix_handle())
    jul_pdx.set_dirs()
    deal_x = example_healers_get_7nodeJRootWithH_deal()
    jul_pdx.create_core_dir_and_files(deal_x)
    assert os_path.exists(jul_pdx._isol_file_path)
    # jul_cx = deal_get_from_json(x_func_open_file(jul_pdx._isol_file_path))
    ex1 = "teesting text"
    x_func_save_file(
        dest_dir=jul_pdx._remedyunit_dir,
        file_title=jul_pdx._isol_file_title,
        file_text=ex1,
    )
    assert x_func_open_file(jul_pdx._remedyunit_dir, jul_pdx._isol_file_title) == ex1

    # WHEN
    jul_pdx.create_core_dir_and_files(deal_x)

    # THEN
    assert x_func_open_file(jul_pdx._remedyunit_dir, jul_pdx._isol_file_title) == ex1


def test_RemedyAdmin_set_remedy_title_WorksCorrectly(remedy_dir_setup_cleanup):
    # GIVEN create healer
    env_dir = get_temp_remedyunit_dir()

    old_healer_text = "bob"
    pdx = RemedyAdmin(old_healer_text, env_dir, get_temp_fix_handle())
    deal_x = example_healers_get_7nodeJRootWithH_deal()
    pdx.set_dirs()
    pdx.create_core_dir_and_files(deal_x)
    old_remedyunit_dir = pdx._remedyunit_dir
    # old_remedyunit_dir = f"{env_dir}/remedyunits/{old_healer_text}"
    print(f"{pdx._remedyunit_dir}")
    print(f"{env_dir}/remedyunits/{old_healer_text}")
    isol_file_title = "isol_deal.json"
    old_isol_file_path = f"{old_remedyunit_dir}/{isol_file_title}"

    assert os_path.exists(old_remedyunit_dir)
    assert os_path.isdir(old_remedyunit_dir)
    assert os_path.exists(old_isol_file_path)

    new_healer_text = "tim"
    new_remedyunit_dir = f"{env_dir}/remedyunits/{new_healer_text}"
    new_isol_file_path = f"{new_remedyunit_dir}/{isol_file_title}"
    assert os_path.exists(new_remedyunit_dir) == False
    assert os_path.isdir(new_remedyunit_dir) == False
    assert os_path.exists(new_isol_file_path) == False

    # WHEN
    pdx.set_remedy_title(new_title=new_healer_text)

    # THEN
    assert os_path.exists(old_remedyunit_dir) == False
    assert os_path.isdir(old_remedyunit_dir) == False
    assert os_path.exists(old_isol_file_path) == False
    assert os_path.exists(new_remedyunit_dir)
    assert os_path.isdir(new_remedyunit_dir)
    assert os_path.exists(new_isol_file_path)


def test_remedyunit_auto_output_to_public_SavesDealToPublicDir(
    remedy_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    pdx = remedyadmin_shop(bob_text, get_temp_remedyunit_dir(), get_temp_fix_handle())
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
