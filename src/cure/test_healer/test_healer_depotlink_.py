from src.deal.deal import DealUnit, get_from_json as deal_get_from_json
from src.deal.x_func import (
    count_files as x_func_count_files,
    open_file as x_func_open_file,
)
from src.cure.healing import healingunit_shop
from src.cure.examples.example_healers import (
    get_2node_deal,
    get_deal_2CleanNodesRandomWeights as get_cal2nodes,
    get_deal_3CleanNodesRandomWeights as get_cal3nodes,
    get_deal_assignment_laundry_example1 as get_america_assign_ex,
)
from src.cure.examples.healer_env_kit import (
    healer_dir_setup_cleanup,
    get_temp_healingunit_dir,
    get_temp_cure_handle,
    create_deal_file,
)
from src.cure.examples.cure_env_kit import get_temp_env_handle
from src.cure.cure import cureunit_shop
from os import path as os_path
from pytest import raises as pytest_raises


def test_healingunit_set_depotlink_RaisesErrorWhenDealDoesNotExist(
    healer_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_temp_healingunit_dir()
    sue_cx = healingunit_shop(sue_text, env_dir, get_temp_cure_handle())
    sue_cx.set_isol_if_empty()
    tim_text = "Tim"
    assert list(sue_cx._isol._partys.keys()) == [sue_text]

    # WHEN / THEN
    file_path_x = f"{sue_cx._admin._deals_depot_dir}/{tim_text}.json"
    print(f"{file_path_x=}")
    with pytest_raises(Exception) as excinfo:
        sue_cx._set_depotlink(outer_healer=tim_text)
    assert (
        str(excinfo.value)
        == f"Healer {sue_text} cannot find deal {tim_text} in {file_path_x}"
    )


def test_healingunit_set_depotlink_CorrectlySetsIsolPartys(healer_dir_setup_cleanup):
    # GIVEN
    yao_text = "yao"
    env_dir = get_temp_healingunit_dir()
    yao_ux = healingunit_shop(yao_text, env_dir, get_temp_cure_handle())
    yao_ux.set_isol_if_empty()
    sue_text = "sue"
    create_deal_file(yao_ux._admin._deals_depot_dir, sue_text)
    assert list(yao_ux._isol._partys.keys()) == [yao_text]

    # WHEN
    yao_ux._set_depotlink(outer_healer=sue_text)

    # THEN
    assert list(yao_ux._isol._partys.keys()) == [yao_text, sue_text]
    assert yao_ux._isol.get_party(sue_text).depotlink_type is None


def test_healingunit_set_depotlink_CorrectlySetsAssignment(healer_dir_setup_cleanup):
    # GIVEN
    america_cx = get_america_assign_ex()
    print(f"{len(america_cx._idea_dict)=}")
    joachim_text = "Joachim"
    joachim_ux = healingunit_shop(
        joachim_text, get_temp_healingunit_dir(), get_temp_cure_handle()
    )
    joachim_ux.create_core_dir_and_files()
    joachim_ux.set_isol_if_empty()
    joachim_ux._admin.save_deal_to_depot(america_cx)
    assert joachim_ux.get_isol().get_party(america_cx._healer) is None
    america_digest_path = (
        f"{joachim_ux._admin._deals_digest_dir}/{america_cx._healer}.json"
    )
    assert os_path.exists(america_digest_path) is False

    # WHEN
    assignment_text = "assignment"
    joachim_ux._set_depotlink(america_cx._healer, link_type=assignment_text)

    # THEN
    assert (
        joachim_ux.get_isol().get_party(america_cx._healer).depotlink_type
        == assignment_text
    )
    assert os_path.exists(america_digest_path)
    digest_cx = deal_get_from_json(
        x_func_open_file(
            dest_dir=joachim_ux._admin._deals_digest_dir,
            file_title=f"{america_cx._healer}.json",
        )
    )
    print(f"{digest_cx._healer=}")
    print(f"{len(digest_cx._idea_dict)=}")
    digest_cx.set_deal_metrics()
    assert len(digest_cx._idea_dict) == 9
    assert digest_cx._healer == joachim_text


def test_healingunit_del_depot_deal_CorrectlyDeletesObj(healer_dir_setup_cleanup):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_healingunit_dir()
    bob_cx = healingunit_shop(bob_text, env_dir, get_temp_cure_handle())
    yao_text = "Yao"
    create_deal_file(bob_cx._admin._deals_depot_dir, yao_text)
    assignment_text = "assignment"
    bob_cx._set_depotlinks_empty_if_null()
    bob_cx._set_depotlink(yao_text, link_type=assignment_text)
    assert list(bob_cx._isol._partys.keys()) == [bob_text, yao_text]
    assert bob_cx._isol.get_party(yao_text).depotlink_type == assignment_text

    # WHEN
    bob_cx.del_depot_deal(deal_healer=yao_text)

    # THEN
    assert list(bob_cx._isol._partys.keys()) == [bob_text, yao_text]
    assert bob_cx._isol.get_party(yao_text).depotlink_type is None


def test_healingunit_del_depot_deal_CorrectlyDeletesBlindTrustFile(
    healer_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_healingunit_dir()
    bob_cx = healingunit_shop(bob_text, env_dir, get_temp_cure_handle())
    lai_text = "Lai"
    create_deal_file(bob_cx._admin._deals_depot_dir, lai_text)
    bob_cx.set_isol_if_empty()
    bob_cx._set_depotlink(lai_text, link_type="blind_trust")
    assert x_func_count_files(dir_path=bob_cx._admin._deals_depot_dir) == 1
    assert x_func_count_files(dir_path=bob_cx._admin._deals_digest_dir) == 1

    # WHEN
    bob_cx.del_depot_deal(deal_healer=lai_text)

    # THEN
    assert x_func_count_files(dir_path=bob_cx._admin._deals_depot_dir) == 0
    assert x_func_count_files(dir_path=bob_cx._admin._deals_digest_dir) == 0


def test_healingunit_set_depot_deal_SavesFileCorrectly(
    healer_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_healingunit_dir()
    bob_cx = healingunit_shop(bob_text, env_dir, get_temp_cure_handle())
    cal1 = get_2node_deal()
    assert (
        x_func_count_files(bob_cx._admin._deals_depot_dir) is None
    )  # dir does not exist

    # WHEN
    bob_cx.set_isol_if_empty()
    bob_cx.set_depot_deal(deal_x=cal1, depotlink_type="blind_trust")

    # THEN
    print(f"Saving to {bob_cx._admin._deals_depot_dir=}")
    # for path_x in os_scandir(ux._admin._deals_depot_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(bob_cx._admin._deals_depot_dir) == 1


def test_healingunit_delete_ignore_depotlink_CorrectlyDeletesObj(
    healer_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_healingunit_dir()
    bob_cx = healingunit_shop(bob_text, env_dir, get_temp_cure_handle())
    yao_text = "Yao"
    create_deal_file(bob_cx._admin._deals_depot_dir, yao_text)
    assignment_text = "assignment"
    bob_cx.set_isol_if_empty()
    bob_cx._set_depotlink(yao_text, link_type=assignment_text)
    assert list(bob_cx._isol._partys.keys()) == [bob_text, yao_text]
    assert bob_cx._isol.get_party(yao_text).depotlink_type == assignment_text

    # WHEN
    bob_cx.del_depot_deal(deal_healer=yao_text)

    # THEN
    assert list(bob_cx._isol._partys.keys()) == [bob_text, yao_text]
    assert bob_cx._isol.get_party(yao_text).depotlink_type is None


def test_healingunit_del_depot_deal_CorrectlyDoesNotDeletesIgnoreFile(
    healer_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    env_dir = get_temp_healingunit_dir()
    bob_cx = healingunit_shop(bob_text, env_dir, get_temp_cure_handle())
    zia_text = "Zia"
    create_deal_file(bob_cx._admin._deals_depot_dir, zia_text)
    bob_cx.set_isol_if_empty()
    bob_cx._set_depotlink(zia_text, link_type="ignore")
    assert x_func_count_files(dir_path=bob_cx._admin._deals_depot_dir) == 1
    assert x_func_count_files(dir_path=bob_cx._admin._deals_digest_dir) == 1
    assert x_func_count_files(dir_path=bob_cx._admin._deals_ignore_dir) == 1

    # WHEN
    bob_cx.del_depot_deal(deal_healer=zia_text)

    # THEN
    assert x_func_count_files(dir_path=bob_cx._admin._deals_depot_dir) == 0
    assert x_func_count_files(dir_path=bob_cx._admin._deals_digest_dir) == 0
    assert x_func_count_files(dir_path=bob_cx._admin._deals_ignore_dir) == 1


def test_healingunit_set_ignore_deal_file_CorrectlyUpdatesIgnoreFile(
    healer_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_healingunit_dir()
    bob_ux = healingunit_shop(bob_text, env_dir, get_temp_cure_handle())
    zia_text = "Zia"
    create_deal_file(bob_ux._admin._deals_depot_dir, zia_text)
    bob_ux.set_isol_if_empty()
    bob_ux._set_depotlink(zia_text, link_type="ignore")
    assert x_func_count_files(dir_path=bob_ux._admin._deals_ignore_dir) == 1
    cx1 = bob_ux._admin.open_ignore_deal(healer=zia_text)
    assert len(cx1._partys) == 0
    cx1.add_partyunit(title="tim")
    assert len(cx1._partys) == 1

    # WHEN
    zia_deal = DealUnit(_healer=zia_text)
    bob_ux.set_ignore_deal_file(zia_deal, src_deal_healer=None)

    # THEN
    cx2 = bob_ux._admin.open_ignore_deal(healer=zia_text)
    assert len(cx2._partys) == 0
    assert x_func_count_files(dir_path=bob_ux._admin._deals_ignore_dir) == 1


def test_healingunit_refresh_depotlinks_CorrectlyPullsAllPublicDeals(
    healer_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_healingunit_dir()
    cure_handle = get_temp_env_handle()
    sx = cureunit_shop(handle=cure_handle, cures_dir=env_dir)
    yao_text = "Yao"
    sx.create_new_healingunit(healing_title=yao_text)
    yao_deal = sx.get_healingunit(title=yao_text)
    assert len(yao_deal._admin.get_remelded_output_deal().get_idea_list()) == 1

    ernie_text = "ernie"
    ernie_deal = get_cal2nodes(_healer=ernie_text)
    steve_text = "steve"
    old_steve_deal = get_cal2nodes(_healer=steve_text)
    sx.save_public_deal(deal_x=ernie_deal)
    sx.save_public_deal(deal_x=old_steve_deal)
    yao_deal.set_depot_deal(deal_x=ernie_deal, depotlink_type="blind_trust")
    yao_deal.set_depot_deal(deal_x=old_steve_deal, depotlink_type="blind_trust")

    assert len(yao_deal._admin.get_remelded_output_deal().get_idea_list()) == 4
    new_steve_deal = get_cal3nodes(_healer=steve_text)
    sx.save_public_deal(deal_x=new_steve_deal)
    print(f"{env_dir=} {yao_deal._admin._deals_public_dir=}")
    # for file_title in x_func_dir_files(dir_path=env_dir):
    #     print(f"{bob_cx._admin._deals_public_dir=} {file_title=}")

    # for file_title in x_func_dir_files(dir_path=bob_cx._admin._deals_public_dir):
    #     print(f"{bob_cx._admin._deals_public_dir=} {file_title=}")

    # WHEN
    yao_deal.refresh_depot_deals()

    # THEN
    assert len(yao_deal._admin.get_remelded_output_deal().get_idea_list()) == 5
