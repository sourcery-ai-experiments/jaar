# from lw.oath import OathUnit
from src.oath.oath import OathUnit
from src.oath.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    copy_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from src.oath.examples.example_oaths import (
    oath_v001 as example_oaths_oath_v001,
    oath_v002 as example_oaths_oath_v002,
    get_oath_1Task_1CE0MinutesRequired_1AcptFact as example_oaths_get_oath_1Task_1CE0MinutesRequired_1AcptFact,
    get_oath_with7amCleanTableRequired as example_oaths_get_oath_with7amCleanTableRequired,
    get_oath_base_time_example as example_oaths_get_oath_base_time_example,
    get_oath_x1_3levels_1required_1acptfacts as example_oaths_get_oath_x1_3levels_1required_1acptfacts,
)

from src.cure.cure import CureUnit, cureunit_shop
from src.cure.examples.example_healers import (
    get_1node_oath as example_healers_get_1node_oath,
    get_7nodeJRootWithH_oath as example_healers_get_7nodeJRootWithH_oath,
    get_oath_2CleanNodesRandomWeights as example_healers_get_oath_2CleanNodesRandomWeights,
    get_oath_3CleanNodesRandomWeights as example_healers_get_oath_3CleanNodesRandomWeights,
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


def create_oath_file_for_cures(cure_dir: str, oath_healer: str):
    oath_x = OathUnit(_healer=oath_healer)
    oath_dir = f"{cure_dir}/oaths"
    # file_path = f"{oath_dir}/{oath_x._healer}.json"
    # if not path.exists(file_path):
    # print(f"{file_path=} {oath_x._healer=}")

    x_func_save_file(
        dest_dir=oath_dir,
        file_title=f"{oath_x._healer}.json",
        file_text=oath_x.get_json(),
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
    x_cure = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_func_delete_dir(x_cure.get_object_root_dir())
    x_cure.create_dirs_if_null(in_memory_bank=True)

    x_cure.save_public_oath(oath_x=example_healers_get_1node_oath())
    x_cure.save_public_oath(
        oath_x=example_oaths_get_oath_1Task_1CE0MinutesRequired_1AcptFact()
    )
    x_cure.save_public_oath(oath_x=example_oaths_oath_v001())
    x_cure.save_public_oath(oath_x=example_oaths_oath_v002())

    # x_cure.set_healer(x_healing=healingunit_shop(title="w1", env_dir=x_cure.get_object_root_dir()))
    # x_cure.set_healer(x_healing=healingunit_shop(title="w2", env_dir=x_cure.get_object_root_dir()))
    xia_text = "Xia"
    x_cure.create_new_healingunit(healing_title=xia_text)
    healer_text = "Myoath"
    x_cure.set_healer_depotlink(
        xia_text, oath_healer=healer_text, depotlink_type="blind_trust"
    )
    # w1_obj = x_cure.get_healingunit(title=w1_text)

    bob_text = "bob wurld"
    create_oath_file_for_cures(x_cure.get_object_root_dir(), bob_text)
    # print(f"create oath_list {w1_text=}")
    x_cure.create_depotlink_to_generated_oath(
        healing_title=xia_text, oath_healer=bob_text, depotlink_type="ignore"
    )
    land_text = "tim wurld"
    create_oath_file_for_cures(
        cure_dir=x_cure.get_object_root_dir(), oath_healer=land_text
    )
    x_cure.create_depotlink_to_generated_oath(
        healing_title=xia_text, oath_healer=land_text, depotlink_type="blind_trust"
    )
    # x_cure.create_depotlink_to_generated_oath(healing_title=w1_text, oath_healer="test9")
    # x_cure.create_depotlink_to_generated_oath(healing_title=w1_text, oath_healer="Bobs oath")
    x_cure.save_healingunit_file(healing_title=xia_text)
    # print(f"WHAT WHAT {x_cure.get_object_root_dir()}")
    # print(f"WHAT WHAT {x_cure.get_object_root_dir()}/healingunits/w1/w1.json")
    # file_text = x_func_open_file(
    #     dest_dir=f"{x_cure.get_object_root_dir}/healingunits/w1", file_title="w1.json"
    # )
    # print(f"{file_text=}")
    # print(f"{len(x_cure._healingunits.get(w1_text)._depotlinks)=}")
    # print(f"{x_cure._healingunits.get(w1_text)._depotlinks.get(bob_text)=}")
    # print(f"{x_cure._healingunits.get(w1_text).get_json=}")

    w2_text = "w2"
    x_cure.create_new_healingunit(healing_title=w2_text)
    # , env_dir=x_cure.get_object_root_dir())
    x_cure.save_healingunit_file(healing_title=w2_text)


def _delete_and_set_ex4():
    cure_handle = "ex4"
    x_cure = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_func_delete_dir(x_cure.get_object_root_dir())
    x_cure.create_dirs_if_null(in_memory_bank=True)
    x_cure.save_public_oath(example_healers_get_7nodeJRootWithH_oath())
    x_cure.save_public_oath(example_oaths_get_oath_with7amCleanTableRequired())
    x_cure.save_public_oath(example_oaths_get_oath_base_time_example())
    x_cure.save_public_oath(example_oaths_get_oath_x1_3levels_1required_1acptfacts())


def _delete_and_set_ex5():
    cure_handle = "ex5"
    x_cure = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_func_delete_dir(x_cure.get_object_root_dir())
    x_cure.create_dirs_if_null(in_memory_bank=True)

    # ethical code ernie
    # ethical code steve
    # ethical code Jessica
    # ethical code Francine
    # ethical code Clay
    oath_1 = example_healers_get_oath_2CleanNodesRandomWeights(_healer="ernie")
    oath_2 = example_healers_get_oath_2CleanNodesRandomWeights(_healer="steve")
    oath_3 = example_healers_get_oath_2CleanNodesRandomWeights(_healer="jessica")
    oath_4 = example_healers_get_oath_2CleanNodesRandomWeights(_healer="francine")
    oath_5 = example_healers_get_oath_2CleanNodesRandomWeights(_healer="clay")

    x_cure.save_public_oath(oath_x=oath_1)
    x_cure.save_public_oath(oath_x=oath_2)
    x_cure.save_public_oath(oath_x=oath_3)
    x_cure.save_public_oath(oath_x=oath_4)
    x_cure.save_public_oath(oath_x=oath_5)

    x_cure.create_new_healingunit(healing_title=oath_1._healer)
    x_cure.create_new_healingunit(healing_title=oath_2._healer)
    x_cure.create_new_healingunit(healing_title=oath_3._healer)
    x_cure.create_new_healingunit(healing_title=oath_4._healer)
    x_cure.create_new_healingunit(healing_title=oath_5._healer)

    x_cure.set_healer_depotlink(oath_1._healer, oath_2._healer, "blind_trust", 3, 3.1)
    x_cure.set_healer_depotlink(oath_1._healer, oath_3._healer, "blind_trust", 7, 7.1)
    x_cure.set_healer_depotlink(oath_1._healer, oath_4._healer, "blind_trust", 4, 4.1)
    x_cure.set_healer_depotlink(oath_1._healer, oath_5._healer, "blind_trust", 5, 5.1)

    x_cure.set_healer_depotlink(oath_2._healer, oath_1._healer, "blind_trust", 3, 3.1)
    x_cure.set_healer_depotlink(oath_2._healer, oath_3._healer, "blind_trust", 7, 7.1)
    x_cure.set_healer_depotlink(oath_2._healer, oath_4._healer, "blind_trust", 4, 4.1)
    x_oath = example_healers_get_oath_3CleanNodesRandomWeights()
    x_cure.set_healer_depotlink(
        oath_2._healer, oath_5._healer, "ignore", 5, 5.1, x_oath
    )

    x_cure.set_healer_depotlink(oath_3._healer, oath_1._healer, "blind_trust", 3, 3.1)
    x_cure.set_healer_depotlink(oath_3._healer, oath_2._healer, "blind_trust", 7, 7.1)
    x_cure.set_healer_depotlink(oath_3._healer, oath_4._healer, "blind_trust", 4, 4.1)
    x_cure.set_healer_depotlink(oath_3._healer, oath_5._healer, "blind_trust", 5, 5.1)

    x_cure.set_healer_depotlink(oath_4._healer, oath_1._healer, "blind_trust", 3, 3.1)
    x_cure.set_healer_depotlink(oath_4._healer, oath_2._healer, "blind_trust", 7, 7.1)
    x_cure.set_healer_depotlink(oath_4._healer, oath_3._healer, "blind_trust", 4, 4.1)
    x_cure.set_healer_depotlink(oath_4._healer, oath_5._healer, "blind_trust", 5, 5.1)

    x_cure.set_healer_depotlink(oath_5._healer, oath_1._healer, "blind_trust", 3, 3.1)
    x_cure.set_healer_depotlink(oath_5._healer, oath_2._healer, "blind_trust", 7, 7.1)
    x_cure.set_healer_depotlink(oath_5._healer, oath_3._healer, "blind_trust", 4, 4.1)
    x_cure.set_healer_depotlink(oath_5._healer, oath_4._healer, "blind_trust", 5, 5.1)

    x_cure.save_healingunit_file(healing_title=oath_1._healer)
    x_cure.save_healingunit_file(healing_title=oath_2._healer)
    x_cure.save_healingunit_file(healing_title=oath_3._healer)
    x_cure.save_healingunit_file(healing_title=oath_4._healer)
    x_cure.save_healingunit_file(healing_title=oath_5._healer)


def _delete_and_set_ex6():
    cure_handle = "ex6"
    x_cure = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_func_delete_dir(x_cure.get_object_root_dir())
    x_cure.create_dirs_if_null(in_memory_bank=False)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_oath = OathUnit(_healer=sal_text)
    sal_oath.add_partyunit(title=bob_text, creditor_weight=2)
    sal_oath.add_partyunit(title=tom_text, creditor_weight=7)
    sal_oath.add_partyunit(title=ava_text, creditor_weight=1)
    x_cure.save_public_oath(oath_x=sal_oath)

    bob_oath = OathUnit(_healer=bob_text)
    bob_oath.add_partyunit(title=sal_text, creditor_weight=3)
    bob_oath.add_partyunit(title=ava_text, creditor_weight=1)
    x_cure.save_public_oath(oath_x=bob_oath)

    tom_oath = OathUnit(_healer=tom_text)
    tom_oath.add_partyunit(title=sal_text, creditor_weight=2)
    x_cure.save_public_oath(oath_x=tom_oath)

    ava_oath = OathUnit(_healer=ava_text)
    ava_oath.add_partyunit(title=elu_text, creditor_weight=2)
    x_cure.save_public_oath(oath_x=ava_oath)

    elu_oath = OathUnit(_healer=elu_text)
    elu_oath.add_partyunit(title=ava_text, creditor_weight=19)
    elu_oath.add_partyunit(title=sal_text, creditor_weight=1)
    x_cure.save_public_oath(oath_x=elu_oath)

    x_cure.refresh_bank_metrics()
    x_cure.set_river_sphere_for_oath(oath_healer=sal_text, max_flows_count=100)


def create_example_cure(cure_handle: str):
    x_cure = cureunit_shop(handle=cure_handle, cures_dir=get_test_cures_dir())
    x_cure.create_dirs_if_null(in_memory_bank=True)


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
