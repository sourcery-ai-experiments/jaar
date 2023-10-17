# from lw.pact import PactUnit
from src.pact.pact import PactUnit
from src.pact.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    copy_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from src.pact.examples.example_pacts import (
    pact_v001 as example_pacts_pact_v001,
    pact_v002 as example_pacts_pact_v002,
    get_pact_1Task_1CE0MinutesRequired_1AcptFact as example_pacts_get_pact_1Task_1CE0MinutesRequired_1AcptFact,
    get_pact_with7amCleanTableRequired as example_pacts_get_pact_with7amCleanTableRequired,
    get_pact_base_time_example as example_pacts_get_pact_base_time_example,
    get_pact_x1_3levels_1required_1acptfacts as example_pacts_get_pact_x1_3levels_1required_1acptfacts,
)

from src.cure.cure import CureUnit, cureunit_shop
from src.cure.examples.example_healers import (
    get_1node_pact as example_healers_get_1node_pact,
    get_7nodeJRootWithH_pact as example_healers_get_7nodeJRootWithH_pact,
    get_pact_2CleanNodesRandomWeights as example_healers_get_pact_2CleanNodesRandomWeights,
    get_pact_3CleanNodesRandomWeights as example_healers_get_pact_3CleanNodesRandomWeights,
)
from os import listdir as os_listdir, rename as os_rename, path as os_path
from pytest import fixture as pytest_fixture


def get_temp_env_handle():
    return "ex_env04"


def get_temp_env_dir():
    return f"{get_test_cures_dir()}/{get_temp_env_handle()}"


def get_test_cures_dir():
    return "src/cure/examples/cures"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_temp_env_dir()
    x_func_delete_dir(dir=env_dir)
    yield env_dir
    x_func_delete_dir(dir=env_dir)


def create_pact_file_for_cures(cure_dir: str, pact_healer: str):
    pact_x = PactUnit(_healer=pact_healer)
    pact_dir = f"{cure_dir}/pacts"
    # file_path = f"{pact_dir}/{pact_x._healer}.json"
    # if not path.exists(file_path):
    # print(f"{file_path=} {pact_x._healer=}")

    x_func_save_file(
        dest_dir=pact_dir,
        file_title=f"{pact_x._healer}.json",
        file_text=pact_x.get_json(),
    )


def create_example_cures_list():
    return x_func_dir_files(
        dir_path=get_test_cures_dir(), include_dirs=True, include_files=False
    )


def setup_test_example_environment():
    _delete_and_set_ex3()
    _delete_and_set_ex4()
    _delete_and_set_ex5()
    _delete_and_set_ex6()


def _delete_and_set_ex3():
    cure_handle = "ex3"
    sx = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_func_delete_dir(sx.get_object_root_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    sx.save_public_pact(pact_x=example_healers_get_1node_pact())
    sx.save_public_pact(
        pact_x=example_pacts_get_pact_1Task_1CE0MinutesRequired_1AcptFact()
    )
    sx.save_public_pact(pact_x=example_pacts_pact_v001())
    sx.save_public_pact(pact_x=example_pacts_pact_v002())

    # sx.set_healer(healer_x=healerunit_shop(title="w1", env_dir=sx.get_object_root_dir()))
    # sx.set_healer(healer_x=healerunit_shop(title="w2", env_dir=sx.get_object_root_dir()))
    xia_text = "Xia"
    sx.create_new_healerunit(healer_title=xia_text)
    healer_text = "Mypact"
    sx.set_healer_depotlink(
        xia_text, pact_healer=healer_text, depotlink_type="blind_trust"
    )
    # w1_obj = sx.get_healer_obj(title=w1_text)

    bob_text = "bob wurld"
    create_pact_file_for_cures(sx.get_object_root_dir(), bob_text)
    # print(f"create pact_list {w1_text=}")
    sx.create_depotlink_to_generated_pact(
        healer_title=xia_text, pact_healer=bob_text, depotlink_type="ignore"
    )
    land_text = "tim wurld"
    create_pact_file_for_cures(cure_dir=sx.get_object_root_dir(), pact_healer=land_text)
    sx.create_depotlink_to_generated_pact(
        healer_title=xia_text, pact_healer=land_text, depotlink_type="blind_trust"
    )
    # sx.create_depotlink_to_generated_pact(healer_title=w1_text, pact_healer="test9")
    # sx.create_depotlink_to_generated_pact(healer_title=w1_text, pact_healer="Bobs pact")
    sx.save_healer_file(healer_title=xia_text)
    # print(f"WHAT WHAT {sx.get_object_root_dir()}")
    # print(f"WHAT WHAT {sx.get_object_root_dir()}/healers/w1/w1.json")
    # file_text = x_func_open_file(
    #     dest_dir=f"{sx.get_object_root_dir}/healers/w1", file_title="w1.json"
    # )
    # print(f"{file_text=}")
    # print(f"{len(sx._healerunits.get(w1_text)._depotlinks)=}")
    # print(f"{sx._healerunits.get(w1_text)._depotlinks.get(bob_text)=}")
    # print(f"{sx._healerunits.get(w1_text).get_json=}")

    w2_text = "w2"
    sx.create_new_healerunit(
        healer_title=w2_text
    )  # , env_dir=sx.get_object_root_dir())
    sx.save_healer_file(healer_title=w2_text)


def _delete_and_set_ex4():
    cure_handle = "ex4"
    sx = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_func_delete_dir(sx.get_object_root_dir())
    sx.create_dirs_if_null(in_memory_bank=True)
    sx.save_public_pact(example_healers_get_7nodeJRootWithH_pact())
    sx.save_public_pact(example_pacts_get_pact_with7amCleanTableRequired())
    sx.save_public_pact(example_pacts_get_pact_base_time_example())
    sx.save_public_pact(example_pacts_get_pact_x1_3levels_1required_1acptfacts())


def _delete_and_set_ex5():
    cure_handle = "ex5"
    sx = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_func_delete_dir(sx.get_object_root_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    # ethical code ernie
    # ethical code steve
    # ethical code Jessica
    # ethical code Francine
    # ethical code Clay
    pact_1 = example_healers_get_pact_2CleanNodesRandomWeights(_healer="ernie")
    pact_2 = example_healers_get_pact_2CleanNodesRandomWeights(_healer="steve")
    pact_3 = example_healers_get_pact_2CleanNodesRandomWeights(_healer="jessica")
    pact_4 = example_healers_get_pact_2CleanNodesRandomWeights(_healer="francine")
    pact_5 = example_healers_get_pact_2CleanNodesRandomWeights(_healer="clay")

    sx.save_public_pact(pact_x=pact_1)
    sx.save_public_pact(pact_x=pact_2)
    sx.save_public_pact(pact_x=pact_3)
    sx.save_public_pact(pact_x=pact_4)
    sx.save_public_pact(pact_x=pact_5)

    sx.create_new_healerunit(healer_title=pact_1._healer)
    sx.create_new_healerunit(healer_title=pact_2._healer)
    sx.create_new_healerunit(healer_title=pact_3._healer)
    sx.create_new_healerunit(healer_title=pact_4._healer)
    sx.create_new_healerunit(healer_title=pact_5._healer)

    sx.set_healer_depotlink(pact_1._healer, pact_2._healer, "blind_trust", 3, 3.1)
    sx.set_healer_depotlink(pact_1._healer, pact_3._healer, "blind_trust", 7, 7.1)
    sx.set_healer_depotlink(pact_1._healer, pact_4._healer, "blind_trust", 4, 4.1)
    sx.set_healer_depotlink(pact_1._healer, pact_5._healer, "blind_trust", 5, 5.1)

    sx.set_healer_depotlink(pact_2._healer, pact_1._healer, "blind_trust", 3, 3.1)
    sx.set_healer_depotlink(pact_2._healer, pact_3._healer, "blind_trust", 7, 7.1)
    sx.set_healer_depotlink(pact_2._healer, pact_4._healer, "blind_trust", 4, 4.1)
    icx = example_healers_get_pact_3CleanNodesRandomWeights()
    sx.set_healer_depotlink(pact_2._healer, pact_5._healer, "ignore", 5, 5.1, icx)

    sx.set_healer_depotlink(pact_3._healer, pact_1._healer, "blind_trust", 3, 3.1)
    sx.set_healer_depotlink(pact_3._healer, pact_2._healer, "blind_trust", 7, 7.1)
    sx.set_healer_depotlink(pact_3._healer, pact_4._healer, "blind_trust", 4, 4.1)
    sx.set_healer_depotlink(pact_3._healer, pact_5._healer, "blind_trust", 5, 5.1)

    sx.set_healer_depotlink(pact_4._healer, pact_1._healer, "blind_trust", 3, 3.1)
    sx.set_healer_depotlink(pact_4._healer, pact_2._healer, "blind_trust", 7, 7.1)
    sx.set_healer_depotlink(pact_4._healer, pact_3._healer, "blind_trust", 4, 4.1)
    sx.set_healer_depotlink(pact_4._healer, pact_5._healer, "blind_trust", 5, 5.1)

    sx.set_healer_depotlink(pact_5._healer, pact_1._healer, "blind_trust", 3, 3.1)
    sx.set_healer_depotlink(pact_5._healer, pact_2._healer, "blind_trust", 7, 7.1)
    sx.set_healer_depotlink(pact_5._healer, pact_3._healer, "blind_trust", 4, 4.1)
    sx.set_healer_depotlink(pact_5._healer, pact_4._healer, "blind_trust", 5, 5.1)

    sx.save_healer_file(healer_title=pact_1._healer)
    sx.save_healer_file(healer_title=pact_2._healer)
    sx.save_healer_file(healer_title=pact_3._healer)
    sx.save_healer_file(healer_title=pact_4._healer)
    sx.save_healer_file(healer_title=pact_5._healer)


def _delete_and_set_ex6():
    cure_handle = "ex6"
    sx = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_func_delete_dir(sx.get_object_root_dir())
    sx.create_dirs_if_null(in_memory_bank=False)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_pact = PactUnit(_healer=sal_text)
    sal_pact.add_partyunit(title=bob_text, creditor_weight=2)
    sal_pact.add_partyunit(title=tom_text, creditor_weight=7)
    sal_pact.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_pact(pact_x=sal_pact)

    bob_pact = PactUnit(_healer=bob_text)
    bob_pact.add_partyunit(title=sal_text, creditor_weight=3)
    bob_pact.add_partyunit(title=ava_text, creditor_weight=1)
    sx.save_public_pact(pact_x=bob_pact)

    tom_pact = PactUnit(_healer=tom_text)
    tom_pact.add_partyunit(title=sal_text, creditor_weight=2)
    sx.save_public_pact(pact_x=tom_pact)

    ava_pact = PactUnit(_healer=ava_text)
    ava_pact.add_partyunit(title=elu_text, creditor_weight=2)
    sx.save_public_pact(pact_x=ava_pact)

    elu_pact = PactUnit(_healer=elu_text)
    elu_pact.add_partyunit(title=ava_text, creditor_weight=19)
    elu_pact.add_partyunit(title=sal_text, creditor_weight=1)
    sx.save_public_pact(pact_x=elu_pact)

    sx.refresh_bank_metrics()
    sx.set_river_sphere_for_pact(pact_healer=sal_text, max_flows_count=100)


def create_example_cure(cure_handle: str):
    sx = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    sx.create_dirs_if_null(in_memory_bank=True)


def delete_dir_example_cure(cure_obj: CureUnit):
    x_func_delete_dir(cure_obj.get_object_root_dir())


def rename_example_cure(cure_obj: CureUnit, new_title):
    # base_dir = cure_obj.get_object_root_dir()
    base_dir = "src/cure/examples/cures"
    src_dir = f"{base_dir}/{cure_obj.handle}"
    dst_dir = f"{base_dir}/{new_title}"
    os_rename(src=src_dir, dst=dst_dir)
    cure_obj.set_cureunit_handle(handle=new_title)


class InvalidCureCopyException(Exception):
    pass


def copy_evaluation_cure(src_handle: str, dest_handle: str):
    base_dir = "src/cure/examples/cures"
    new_dir = f"{base_dir}/{dest_handle}"
    if os_path.exists(new_dir):
        raise InvalidCureCopyException(
            f"Cannot copy cure to '{new_dir}' directory because '{new_dir}' exists."
        )
    # base_dir = cure_obj.get_object_root_dir()
    src_dir = f"{base_dir}/{src_handle}"
    dest_dir = f"{base_dir}/{dest_handle}"
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
