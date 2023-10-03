from src.contract.contract import (
    ContractUnit,
    get_from_json as contract_get_from_json,
    get_meld_of_contract_files,
)
from src.contract.examples.contract_env import contract_env
from src.contract.idea import IdeaCore, IdeaKid
from src.contract.road import Road
from src.contract.required_idea import RequiredUnit
from src.contract.party import partylink_shop
from src.contract.group import groupunit_shop, balancelink_shop
from src.contract.examples.example_contracts import (
    get_contract_with_4_levels as example_contracts_get_contract_with_4_levels,
    get_contract_with_4_levels_and_2requireds as example_contracts_get_contract_with_4_levels_and_2requireds,
    get_contract_with7amCleanTableRequired as example_contracts_get_contract_with7amCleanTableRequired,
    get_contract_with_4_levels_and_2requireds_2acptfacts as example_contracts_get_contract_with_4_levels_and_2requireds_2acptfacts,
    contract_v001 as example_contracts_contract_v001,
)
from src.contract.x_func import (
    dir_files as x_func_dir_files,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
)
from src.economy.examples.economy_env_kit import (
    env_dir_setup_cleanup,
    get_temp_env_dir,
)
from pytest import raises as pytest_raises


def test_contractunit_get_bond_status_ReturnsCorrectBool():
    # GIVEN
    jessi_text = "jessi"
    cx = ContractUnit(_owner=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")

    # WHEN\THEN no action idea exists
    cx.add_idea(idea_kid=IdeaKid(_label=casa_text), walk=jessi_text)
    assert cx.get_bond_status() == False

    # WHEN\THEN 1 action idea exists
    clean_cookery_text = "clean cookery"
    cx.add_idea(
        idea_kid=IdeaKid(_label=clean_cookery_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status()

    # WHEN\THEN 2 action idea exists
    clean_hallway_text = "clean hallway"
    cx.add_idea(
        idea_kid=IdeaKid(_label=clean_hallway_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status() == False

    # WHEN\THEN 1 action idea deleted (1 total)
    clean_hallway_road = Road(f"{jessi_text},{casa_text},{clean_hallway_text}")
    cx.del_idea_kid(road=clean_hallway_road)
    assert cx.get_bond_status()

    # WHEN\THEN 1 action idea deleted (0 total)
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")
    cx.del_idea_kid(road=clean_cookery_road)
    assert cx.get_bond_status() == False

    # for idea_kid in cx._idearoot._kids.values():
    #     print(f"after {idea_kid._label=} {idea_kid.promise=}")


def test_contractunit_get_bond_status_ReturnsCorrectBoolWhenOnlyActionIdeaBalanceHeirsMatchContractGroups():
    # GIVEN
    jessi_text = "jessi"
    cx = ContractUnit(_owner=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_idea(idea_kid=IdeaKid(_label=casa_text), walk=jessi_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_label=clean_cookery_text, promise=True), walk=casa_road
    )
    tom_text = "tom"
    cx.add_partyunit(name=tom_text)
    assert cx.get_bond_status() == False

    # WHEN
    cx.edit_idea_attr(
        road=clean_cookery_road, balancelink=balancelink_shop(brand=tom_text)
    )
    # THEN
    assert cx.get_bond_status()

    # WHEN
    bob_text = "bob"
    cx.add_partyunit(name=bob_text)
    # THEN
    assert cx.get_bond_status() == False


def test_contractunit_get_bond_status_ChecksActionIdeaGroupsheirsEqualContractGroupunits():
    # GIVEN
    jessi_text = "jessi"
    cx = ContractUnit(_owner=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_idea(idea_kid=IdeaKid(_label=casa_text), walk=jessi_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_label=clean_cookery_text, promise=True), walk=casa_road
    )
    tom_text = "tom"
    cx.add_partyunit(name=tom_text)
    assert cx.get_bond_status() == False

    # WHEN
    cx.edit_idea_attr(
        road=clean_cookery_road, balancelink=balancelink_shop(brand=tom_text)
    )
    clean_cookery_idea = cx.get_idea_kid(road=clean_cookery_road)
    assert len(clean_cookery_idea._balanceheirs) == 1
    # THEN
    assert cx.get_bond_status()

    # WHEN
    bob_text = "bob"
    cx.add_partyunit(name=bob_text)
    # THEN
    assert cx.get_bond_status() == False


def test_contractunit_get_bond_status_ChecksActionIdeaGroupsheirsEqualContractGroupunits2():
    # GIVEN
    jessi_text = "jessi"
    cx = ContractUnit(_owner=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{jessi_text},{casa_text}")
    cx.add_idea(idea_kid=IdeaKid(_label=casa_text), walk=jessi_text)
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{jessi_text},{casa_text},{clean_cookery_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_label=clean_cookery_text, promise=True), walk=casa_road
    )
    assert cx.get_bond_status()

    tom_text = "tom"
    cx.add_partyunit(name=tom_text)
    bob_text = "bob"
    cx.add_partyunit(name=bob_text)
    home_occupants_text = "home occupants"
    home_occupants_groupunit = groupunit_shop(brand=home_occupants_text)
    home_occupants_groupunit.set_partylink(partylink=partylink_shop(name=tom_text))
    home_occupants_groupunit.set_partylink(partylink=partylink_shop(name=bob_text))
    cx.set_groupunit(groupunit=home_occupants_groupunit)
    assert cx.get_bond_status() == False

    # WHEN
    cx.edit_idea_attr(
        road=clean_cookery_road, balancelink=balancelink_shop(brand=home_occupants_text)
    )
    # THEN
    assert cx.get_bond_status()

    # WHEN
    yuri_text = "yuri"
    cx.add_partyunit(name=yuri_text)

    # THEN
    assert cx.get_bond_status() == False


# def test_contractunit_get_bond_status_ChecksOnlyNecessaryIdeasExist_MultipleScenario():
#     # GIVEN
#     jessi_text = "jessi"
#     cx = ContractUnit(_owner=jessi_text)
#     casa_text = "case"
#     casa_road = Road(f"{cx._economy_title},{casa_text}")
#     cx.add_idea(idea_kid=IdeaKid(_label=casa_text), walk=jessi_text)
#     clean_cookery_text = "clean cookery"
#     clean_cookery_road = Road(f"{cx._economy_title},{casa_text},{clean_cookery_text}")

#     # WHEN/THEN
#     cx.add_idea(
#         idea_kid=IdeaKid(_label=clean_cookery_text, promise=True), walk=casa_road
#     )
#     assert cx.get_bond_status()

#     # WHEN/THEN
#     water_text = "water"
#     water_road = Road(f"{cx._economy_title},{water_text}")
#     cx.add_idea(idea_kid=IdeaKid(_label=water_text), walk=jessi_text)
#     assert cx.get_bond_status() == False

#     rain_text = "rain"
#     rain_road = Road(f"{cx._economy_title},{water_text},{rain_text}")
#     cx.add_idea(idea_kid=IdeaKid(_label=rain_text), walk=water_road)

#     # WHEN/THEN
#     cx.edit_idea_attr(
#         road=clean_cookery_road, required_base=water_road, required_sufffact=rain_road
#     )
#     assert cx.get_bond_status()


def test_contractunit_get_contract_sprung_from_single_idea_ReturnsCorrectContractScenario1():
    # GIVEN
    jessi_text = "jessi"
    cx = ContractUnit(_owner=jessi_text)
    casa_text = "case"
    casa_road = Road(f"{cx._economy_title},{casa_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_label=casa_text, _begin=-1, _close=19), walk=cx._economy_title
    )
    clean_cookery_text = "clean cookery"
    clean_cookery_road = Road(f"{cx._economy_title},{casa_text},{clean_cookery_text}")
    cx.add_idea(
        idea_kid=IdeaKid(_label=clean_cookery_text, promise=True, _begin=2, _close=4),
        walk=casa_road,
    )
    water_text = "water"
    water_road = Road(f"{cx._economy_title},{water_text}")
    cx.add_idea(idea_kid=IdeaKid(_label=water_text), walk=cx._economy_title)
    assert cx.get_bond_status() == False

    # WHEN
    bond_contract = cx.get_contract_sprung_from_single_idea(road=clean_cookery_road)

    # THEN
    # assert bond_contract._label == clean_cookery_text
    print(f"{len(bond_contract._idea_dict)=}")
    assert len(bond_contract._idea_dict) == 3
    b_src_idea = bond_contract.get_idea_kid(road=cx._economy_title)
    source_x_idea = cx.get_idea_kid(road=cx._economy_title)
    assert b_src_idea._uid == source_x_idea._uid
    assert b_src_idea._begin == source_x_idea._begin
    assert b_src_idea._close == source_x_idea._close
    assert b_src_idea != source_x_idea

    b_casa_idea = bond_contract.get_idea_kid(road=casa_road)
    src_casa_idea = cx.get_idea_kid(road=casa_road)
    assert b_casa_idea._uid == src_casa_idea._uid
    assert b_casa_idea._begin == src_casa_idea._begin
    assert b_casa_idea._close == src_casa_idea._close
    assert b_casa_idea != src_casa_idea

    b_clean_cookery_idea = bond_contract.get_idea_kid(road=clean_cookery_road)
    src_clean_cookery_idea = cx.get_idea_kid(road=clean_cookery_road)
    assert b_clean_cookery_idea._uid == src_clean_cookery_idea._uid
    assert b_clean_cookery_idea._begin == src_clean_cookery_idea._begin
    assert b_clean_cookery_idea._close == src_clean_cookery_idea._close
    assert b_clean_cookery_idea != src_clean_cookery_idea

    assert bond_contract._idearoot._kids.get(water_text) is None

    # for byx in bond_contract._idea_dict.values():
    #     cyx = cx.get_idea_kid(road=byx.get_road())
    #     assert byx._uid == cyx._uid
    #     print(f"{byx.get_road()=} {byx._begin=} {byx._close=}")
    #     print(f"{cyx.get_road()=} {cyx._begin=} {cyx._close=}")
    #     assert byx._begin == cyx._begin
    #     assert byx._close == cyx._close
    #     for yx4 in byx._kids.values():
    #         assert yx4._label == cyx._kids.get(yx4._label)._label
    #     for cx3 in cyx._kids.values():
    #         if cx3._label == water_text:
    #             print(f"checking src contract idea kid_label='{cx3._label}'")
    #             assert byx._kids.get(cx3._label) is None
    #         else:
    #             assert cx3._label == byx._kids.get(cx3._label)._label
    #     # assert len(byx._kids) != len(cyx._kids)
    #     # assert byx._kids_total_weight != cyx._kids_total_weight
    #     # assert byx._kids != cyx._kids
    #     assert byx != cyx

    assert len(bond_contract._idea_dict) == 3
    assert bond_contract._idearoot._kids.get(water_text) is None


def test_contractunit_export_all_bonds_ExportsFileOfBonds_2files(env_dir_setup_cleanup):
    # GIVEN
    cx = example_contracts_get_contract_with_4_levels_and_2requireds_2acptfacts()
    cx_idea_list = cx.get_idea_list()
    action_count = sum(bool(yx.promise) for yx in cx_idea_list)
    assert action_count == 2
    with pytest_raises(Exception) as excinfo:
        x_func_dir_files(dir_path=get_temp_env_dir())

    sys_word_part1 = "sys"  # the built word might be find and replaced in the future.
    sys_word_part2 = "tem"  # the built word might be find and replaced in the future.
    assert (
        str(excinfo.value)
        == f"[WinError 3] The {sys_word_part1}{sys_word_part2} cannot find the path specified: '{get_temp_env_dir()}'"
    )

    # WHEN
    cx.export_all_bonds(dir=get_temp_env_dir())

    # THEN
    # for bond_file_x in x_func_dir_files(dir_path=get_temp_env_dir()).keys():
    #     print(f"files exported {bond_file_x=}")

    assert len(x_func_dir_files(dir_path=get_temp_env_dir())) == 2


# deactivated since it takes too long
# def test_contractunit_export_all_bonds_ExportsFileOfBonds_69files(env_dir_setup_cleanup):
#     # GIVEN
#     cx = example_contracts_contract_v001()
#     cx_idea_list = cx.get_idea_list()
#     action_count = 0
#     for yx in cx_idea_list:
#         if yx.promise:
#             action_count += 1
#     assert action_count == 69
#     # WHEN/THEN
#     with pytest_raises(Exception) as excinfo:
#         assert x_func_dir_files(dir_path=get_temp_env_dir())
#     assert (
#         str(excinfo.value)
#         == f"[WinError 3] Cannot find the path specified: '{get_temp_env_dir()}'"
#     )

#     # WHEN
#     cx.export_all_bonds(dir=get_temp_env_dir())

#     # THEN
#     for bond_file_x in x_func_dir_files(dir_path=get_temp_env_dir()).keys():
#         print(f"files exported {bond_file_x=}")

#     assert len(x_func_dir_files(dir_path=get_temp_env_dir())) == action_count


# def test_contractunit_export_all_bonds_ReturnsDictOfBonds(env_dir_setup_cleanup):
#     # GIVEN
#     cx = example_contracts_get_contract_with_4_levels_and_2requireds_2acptfacts()
#     cx_idea_list = cx.get_idea_list()
#     action_count = sum(bool(yx.promise) for yx in cx_idea_list)
#     assert action_count == 2

#     # WHEN
#     cx.export_all_bonds(dir=get_temp_env_dir())

#     # THEN
#     dir_files = x_func_dir_files(dir_path=get_temp_env_dir())
#     file_17_name = "17.json"
#     assert dir_files[file_17_name]
#     json_17 = x_func_open_file(dest_dir=get_temp_env_dir(), file_name=file_17_name)
#     bond_17 = contract_get_from_json(cx_json=json_17)
#     assert bond_17.get_bond_status()

#     file_2_name = "2.json"
#     assert dir_files[file_2_name]
#     json_2 = x_func_open_file(dest_dir=get_temp_env_dir(), file_name=file_2_name)
#     bond_2 = contract_get_from_json(cx_json=json_2)
#     assert bond_2.get_bond_status()


def test_contractunit_get_meld_of_contract_files_MeldsIntoSourceContract_Scenario1(
    env_dir_setup_cleanup,
):
    # GIVEN
    owner_text = "Nia"
    primary_cx = ContractUnit(_owner=owner_text, _weight=10)

    work = "work"
    idea_kid_work = IdeaKid(_weight=30, _label=work, promise=True)
    primary_cx.add_idea(idea_kid=idea_kid_work, walk=f"{primary_cx._economy_title}")

    cat = "feed cat"
    idea_kid_feedcat = IdeaKid(_weight=20, _label=cat, promise=True)
    primary_cx.add_idea(idea_kid=idea_kid_feedcat, walk=f"{primary_cx._economy_title}")

    primary_cx.export_all_bonds(dir=get_temp_env_dir())
    cat_t = "feed cat"
    src_cat_idea = primary_cx._idearoot._kids.get(cat_t)
    src_cat_idea.set_originunit_empty_if_null()

    # WHEN
    new_cx = get_meld_of_contract_files(
        cx_primary=primary_cx,
        meldees_dir=get_temp_env_dir(),
    )

    # THEN
    assert primary_cx._weight == new_cx._weight
    assert primary_cx._idearoot._weight == new_cx._idearoot._weight
    src_cat_idea = primary_cx._idearoot._kids.get(cat_t)
    new_cat_idea = new_cx._idearoot._kids.get(cat_t)
    assert src_cat_idea._contract_coin_onset == new_cat_idea._contract_coin_onset
    assert src_cat_idea._originunit == new_cat_idea._originunit
    assert src_cat_idea == new_cat_idea
    assert primary_cx._idearoot._kids == new_cx._idearoot._kids
    assert primary_cx._idearoot == new_cx._idearoot
    assert primary_cx == new_cx


# def test_contractunit_get_meld_of_contract_files_MeldsIntoSourceContract_Scenario2(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     sourrcecx = ContractUnit(_owner=owner_text, _weight=10)

#     work_text = "work"
#     work_road = f"{cx._economy_title},{work_text}"

#     cat_text = "feed cat"
#     cat_idea = IdeaKid(_weight=20, _label=cat_text, promise=True)
#     sourrce_cx.add_idea(idea_kid=cat_idea, walk=work_road)

#     plant_text = "water plant"
#     plant_idea = IdeaKid(_weight=30, _label=plant_text, promise=True)
#     sourrce_cx.add_idea(idea_kid=plant_idea, walk=work_road)
#     sourrce_cx.export_all_bonds(dir=get_temp_env_dir())

#     # WHEN
#     new_cx = get_meld_of_contract_files(
#         contractunit=ContractUnit(_owner=sourrce_cx._owner, _weight=0), dir=get_temp_env_dir()
#     )

#     # THEN
#     assert sourrce_cx._weight == new_cx._weight
#     assert sourrce_cx._idearoot._weight == new_cx._idearoot._weight
#     assert len(sourrce_cx._idearoot._kids) == 1
#     assert len(sourrce_cx._idearoot._kids) == len(new_cx._idearoot._kids)
#     sourrce_work_idea = sourrce_cx._idearoot._kids.get(work_text)
#     new_work_idea = new_cx._idearoot._kids.get(work_text)
#     sourrce_cat_idea = sourrce_work_idea._kids.get(cat_text)
#     new_cat_idea = new_work_idea._kids.get(cat_text)
#     print(f"{sourrce_cat_idea._contract_importance=} {new_cat_idea._contract_importance=}")
#     assert sourrce_cat_idea._weight == new_cat_idea._weight
#     assert sourrce_work_idea._kids.get(cat_text) == new_work_idea._kids.get(cat_text)

#     assert sourrce_cx._idearoot._kids.get(cat_text) == new_cx._idearoot._kids.get(cat_text)
#     assert sourrce_cx._idearoot._kids == new_cx._idearoot._kids
#     assert sourrce_cx._idearoot == new_cx._idearoot
#     assert sourrce_cx == new_cx


# - [ ] create test_contractunit_get_bond_status_ReturnsFalseWhenNotOnlyActionIdeaAcptFactsExist
