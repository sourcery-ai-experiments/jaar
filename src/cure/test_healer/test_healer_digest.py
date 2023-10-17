from src.pact.pact import ContractUnit, originunit_shop
from src.pact.examples.example_pacts import (
    get_pact_with_4_levels as example_pacts_get_pact_with_4_levels,
)
from src.pact.x_func import (
    open_file as x_func_open_file,
    count_files as x_func_count_files,
)
from src.cure.healer import healerunit_shop
from src.cure.examples.example_healers import (
    get_2node_pact as example_healers_get_2node_pact,
    get_7nodeJRoot_pact as example_healers_get_7nodeJRoot_pact,
)
from src.cure.examples.healer_env_kit import (
    healer_dir_setup_cleanup,
    get_temp_healer_dir,
    get_temp_cure_handle,
)
from os import path as os_path
from pytest import raises as pytest_raises


# def test_healer_save_isol_pact_CreateStartingContractFile(
#     healer_dir_setup_cleanup,
# ):
#     # GIVEN
#     lai_title = "Lai"
#     env_dir = get_temp_healer_dir()
#     lai_pact = healerunit_shop(title=lai_title, env_dir=env_dir)
#     lai_isol_file_title = lai_pact._admin._isol_file_title
#     with pytest_raises(Exception) as excinfo:
#         x_func_open_file(lai_pact._admin._healer_dir, lai_isol_file_title)
#     assert (
#         str(excinfo.value)
#         == f"Could not load file {lai_pact._admin._isol_file_path} (2, 'No such file or directory')"
#     )

#     # WHEN
#     lai_pact._admin.save_isol_pact(
#         pact_x=example_pacts_get_pact_with_4_levels()
#     )

#     # THEN
#     assert x_func_open_file(lai_pact._admin._healer_dir, lai_isol_file_title) != None


def test_healeropen_isol_pact_WhenStartingContractFileDoesNotExists(
    healer_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    env_dir = get_temp_healer_dir()
    cure_handle_text = get_temp_cure_handle()
    ux = healerunit_shop(title=tim_text, env_dir=env_dir, cure_handle=cure_handle_text)

    # WHEN
    isol_pact = ux._admin.open_isol_pact()
    assert isol_pact != None
    assert isol_pact._cure_handle == cure_handle_text

    # THEN
    x_pact = ContractUnit(_healer=tim_text)
    x_pact.set_cure_handle(get_temp_cure_handle())
    x_pact.set_pact_metrics()
    # x_idearoot = IdeaRoot(_label=p_title, _pad="")
    # x_idearoot.set_balancelines_empty_if_null()
    # x_idearoot.set_kids_empty_if_null()
    # x_idearoot.set_balancelink_empty_if_null()
    # x_idearoot.set_balanceheir_empty_if_null()
    # x_idearoot.set_requiredunits_empty_if_null()
    # x_idearoot.set_requiredheirs_empty_if_null()
    # x_idearoot._pact_importance = 1
    # x_idearoot._level = 0
    # x_idearoot._ancestor_promise_count = 0
    # x_idearoot._descendant_promise_count = 0
    # x_idearoot._all_party_credit = True
    # x_idearoot._all_party_debt = True

    assert isol_pact._idearoot == x_pact._idearoot
    assert isol_pact._idearoot._acptfactunits == {}
    assert list(isol_pact._partys.keys()) == [tim_text]
    assert list(isol_pact._groups.keys()) == [tim_text]


def test_healer_save_isol_pact_IsolContractHealerMustBeHealer(
    healer_dir_setup_cleanup,
):
    # GIVEN
    p_title = "Game1"
    env_dir = get_temp_healer_dir()
    ux = healerunit_shop(p_title, env_dir, get_temp_cure_handle())
    cx1 = example_pacts_get_pact_with_4_levels()
    assert cx1._healer != p_title

    # WHEN
    ux._admin.save_isol_pact(pact_x=cx1)

    # THEN
    assert ux._admin.open_isol_pact()._healer == ux._admin._healer_title


def test_healer_open_isol_pact_WhenStartingContractFileExists(
    healer_dir_setup_cleanup,
):
    # GIVEN
    p_title = "Game1"
    env_dir = get_temp_healer_dir()
    ux = healerunit_shop(p_title, env_dir, get_temp_cure_handle())
    ux._admin.save_isol_pact(pact_x=example_pacts_get_pact_with_4_levels())

    # WHEN
    assert ux._admin.open_isol_pact() != None
    isol_pact = ux._admin.open_isol_pact()

    # THEN
    x_pact = example_pacts_get_pact_with_4_levels()
    x_pact.set_healer(new_healer=p_title)
    x_pact.set_pact_metrics()

    assert isol_pact._idearoot._kids == x_pact._idearoot._kids
    assert isol_pact._idearoot == x_pact._idearoot
    assert isol_pact._idearoot._acptfactunits == {}
    assert isol_pact._partys == {}
    assert isol_pact._groups == {}
    assert isol_pact._healer == ux._admin._healer_title


def test_healer_erase_isol_pact_file_DeletesFileCorrectly(
    healer_dir_setup_cleanup,
):
    # GIVEN
    p_title = "Game1"
    env_dir = get_temp_healer_dir()
    ux = healerunit_shop(p_title, env_dir, get_temp_cure_handle())
    ux._admin.save_isol_pact(example_pacts_get_pact_with_4_levels())
    file_title = ux._admin._isol_file_title
    assert x_func_open_file(ux._admin._healer_dir, file_title) != None

    # WHEN
    ux._admin.erase_isol_pact_file()

    # THEN
    with pytest_raises(Exception) as excinfo:
        x_func_open_file(ux._admin._healer_dir, file_title)
    assert (
        str(excinfo.value)
        == f"Could not load file {ux._admin._healer_dir}/isol_pact.json (2, 'No such file or directory')"
    )


def test_healerunit_save_pact_to_digest_SavesFileCorrectly(
    healer_dir_setup_cleanup,
):
    # GIVEN
    healer_title = "healer1"
    env_dir = get_temp_healer_dir()
    ux = healerunit_shop(healer_title, env_dir, get_temp_cure_handle())
    ux.create_core_dir_and_files()
    cx = example_healers_get_2node_pact()
    src_pact_healer = cx._healer
    assert x_func_count_files(ux._admin._pacts_digest_dir) == 0

    # WHEN
    ux._admin.save_pact_to_digest(cx, src_pact_healer=src_pact_healer)

    # THEN
    cx_file_title = f"{cx._healer}.json"
    digest_file_path = f"{ux._admin._pacts_digest_dir}/{cx_file_title}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(ux._admin._pacts_digest_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(ux._admin._pacts_digest_dir) == 1
    digest_cx_json = x_func_open_file(
        dest_dir=ux._admin._pacts_digest_dir,
        file_title=f"{src_pact_healer}.json",
    )
    assert digest_cx_json == cx.get_json()


def test_presonunit__set_depotlink_CorrectlySets_blind_trust_DigestContract(
    healer_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_temp_healer_dir()
    sue_cx = healerunit_shop(sue_text, env_dir, get_temp_cure_handle())
    sue_cx.create_core_dir_and_files()
    cx = example_healers_get_2node_pact()
    src_pact_healer = cx._healer
    assert x_func_count_files(sue_cx._admin._pacts_digest_dir) == 0

    # WHEN
    sue_cx.set_depot_pact(pact_x=cx, depotlink_type="blind_trust")

    # THEN
    cx_file_title = f"{cx._healer}.json"
    digest_file_path = f"{sue_cx._admin._pacts_digest_dir}/{cx_file_title}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(sue_cx._admin._pacts_digest_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(sue_cx._admin._pacts_digest_dir) == 1
    digest_cx_json = x_func_open_file(
        dest_dir=sue_cx._admin._pacts_digest_dir,
        file_title=f"{src_pact_healer}.json",
    )
    assert digest_cx_json == cx.get_json()


def test_healer_get_remelded_output_pact_withEmptyDigestDict(
    healer_dir_setup_cleanup,
):
    # GIVEN
    healer_title_x = "boots3"
    ux = healerunit_shop(healer_title_x, get_temp_healer_dir(), get_temp_cure_handle())
    ux.create_core_dir_and_files()
    sx_output_before = ux._admin.get_remelded_output_pact()
    assert str(type(sx_output_before)).find(".pact.ContractUnit'>")
    assert sx_output_before._healer == healer_title_x
    assert sx_output_before._idearoot._label == get_temp_cure_handle()
    # ux.set_digested_pact(pact_x=ContractUnit(_healer="digested1"))

    # WHEN
    sx_output_after = ux._admin.get_remelded_output_pact()

    # THEN
    healer_pact_x = ContractUnit(_healer=healer_title_x, _weight=0.0)
    healer_pact_x.set_cure_handle(get_temp_cure_handle())
    healer_pact_x._idearoot._pad = ""
    healer_pact_x.set_pact_metrics()

    assert str(type(sx_output_after)).find(".pact.ContractUnit'>")
    assert sx_output_after._weight == healer_pact_x._weight
    assert sx_output_after._idearoot._pad == healer_pact_x._idearoot._pad
    assert (
        sx_output_after._idearoot._acptfactunits
        == healer_pact_x._idearoot._acptfactunits
    )
    assert sx_output_after._idearoot == healer_pact_x._idearoot


def test_healer_get_remelded_output_pact_with1DigestedContract(
    healer_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    env_dir = get_temp_healer_dir()
    ux = healerunit_shop(yao_text, env_dir, get_temp_cure_handle())
    ux.create_core_dir_and_files()
    sx_output_old = ux._admin.get_remelded_output_pact()
    assert str(type(sx_output_old)).find(".pact.ContractUnit'>")
    assert sx_output_old._healer == yao_text
    assert sx_output_old._idearoot._label == get_temp_cure_handle()
    input_pact = example_healers_get_2node_pact()
    input_pact.meld(input_pact)
    ux.set_depot_pact(pact_x=input_pact, depotlink_type="blind_trust")

    # WHEN
    sx_output_new = ux._admin.get_remelded_output_pact()

    # THEN
    assert str(type(sx_output_new)).find(".pact.ContractUnit'>")

    assert sx_output_new._weight == 0
    assert sx_output_new._weight != input_pact._weight
    sx_idearoot = sx_output_new._idearoot
    input_idearoot = input_pact._idearoot
    assert sx_idearoot._pad == input_idearoot._pad
    assert sx_idearoot._acptfactunits == input_idearoot._acptfactunits
    input_b_idea = input_idearoot._kids.get("B")
    sx_output_new_b_idea = sx_idearoot._kids.get("B")
    assert sx_output_new_b_idea._pad == input_b_idea._pad
    assert sx_output_new._idearoot._kids == input_pact._idearoot._kids
    assert sx_idearoot._kids_total_weight == input_idearoot._kids_total_weight
    assert sx_idearoot == input_idearoot
    assert sx_output_new._healer != input_pact._healer
    assert sx_output_new != input_pact


# def test_healer_set_digested_pact_with2Groups(healer_dir_setup_cleanup):
#     # GIVEN
#     env_dir = get_temp_healer_dir()
#     ux = healerunit_shop(title="test8", env_dir=env_dir)
#     sx_output_old = ux._admin.get_remelded_output_pact()
#     assert str(type(sx_output_old)).find(".pact.ContractUnit'>")
#     assert sx_output_old._groups == {}
#     assert sx_output_old._partys == {}
#     assert sx_output_old._acptfacts == {}

#     src1 = "test1"
#     src1_road = Road(f"{src1}")
#     s1 = ContractUnit(_healer=src1)

#     ceci_text = "Ceci"
#     s1.set_partyunit(partyunit=PartyUnit(title=ceci_text))
#     swim_text = "swimmers"
#     swim_group = BraUnit(title=swim_text)
#     swim_group.set_partylink(partylink=partylink_shop(title=ceci_text))
#     s1.set_groupunit(groupunit=swim_group)

#     yaya_text = "yaya"
#     yaya_road = Road(f"{src1},{yaya_text}")
#     s1.add_idea(idea_kid=IdeaKid(_label=yaya_text), pad=src1_road)
#     s1.set_acptfact(base=yaya_road, acptfact=yaya_road)

#     assert s1._groups.get(swim_text).title == swim_text
#     assert s1._partys.get(ceci_text).title == ceci_text
#     assert s1._idearoot._label == src1
#     assert s1._acptfacts.get(yaya_road).base == yaya_road

#     # WHEN
#     ux.set_single_digested_pact(_pact_healer="test1", digest_pact_x=s1)
#     sx_output_new = ux._admin.get_remelded_output_pact()

#     # THEN
#     assert str(type(sx_output_new)).find(".pact.ContractUnit'>")
#     assert sx_output_new._acptfacts == s1._acptfacts
#     assert sx_output_new._partys == s1._partys
#     assert sx_output_new._groups == s1._groups
#     assert sx_output_new._weight == s1._weight
#     assert sx_output_new._weight == s1._weight
#     assert sx_output_new._idearoot._pad == s1._idearoot._pad
#     assert sx_output_new._idearoot._acptfactunits == s1._idearoot._acptfactunits
#     assert sx_output_new._idearoot._kids == s1._idearoot._kids
#     assert sx_output_new._idearoot._kids_total_weight == s1._idearoot._kids_total_weight
#     assert sx_output_new._idearoot == s1._idearoot
#     assert sx_output_new._label != s1._label
#     assert sx_output_new != s1


def test_healer_isol_pact_CorrectlysHasOriginLinksWithHealerAsSource(
    healer_dir_setup_cleanup,
):
    # GIVEN
    # healerunit with isol_pact and no other depot pacts
    yao_text = "Yao"
    isol_origin_weight = 1
    yao_originunit = originunit_shop()
    yao_originunit.set_originlink(title=yao_text, weight=isol_origin_weight)
    isol_pact_x = example_healers_get_7nodeJRoot_pact()
    isol_pact_x.set_healer(yao_text)

    assert isol_pact_x._idearoot._originunit == originunit_shop()
    assert isol_pact_x._idearoot._originunit != yao_originunit

    ux = healerunit_shop(yao_text, get_temp_healer_dir(), get_temp_cure_handle())
    ux.create_core_dir_and_files()
    ux._admin.save_isol_pact(pact_x=isol_pact_x)

    # WHEN
    output_pact_x = ux._admin.get_remelded_output_pact()

    # THEN
    assert output_pact_x._idearoot._originunit == originunit_shop()
    d_road = "J,A,C,D"
    d_idea = output_pact_x.get_idea_kid(road=d_road)
    assert d_idea._originunit == yao_originunit

    print(f"{output_pact_x._originunit=}")
    assert output_pact_x._originunit == yao_originunit

    output_originlink = output_pact_x._originunit._links.get(yao_text)
    assert output_originlink.title == yao_text
    assert output_originlink.weight == isol_origin_weight
