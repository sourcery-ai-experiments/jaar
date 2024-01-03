# from lw.agenda import AgendaUnit
from src.agenda.agenda import agendaunit_shop
from src.tools.file import (
    single_dir_create_if_null,
    delete_dir,
    copy_dir,
    save_file,
    open_file,
    dir_files,
)
from src.agenda.examples.example_agendas import (
    agenda_v001 as example_agendas_agenda_v001,
    agenda_v002 as example_agendas_agenda_v002,
    get_agenda_1Task_1CE0MinutesRequired_1AcptFact as example_agendas_get_agenda_1Task_1CE0MinutesRequired_1AcptFact,
    get_agenda_with7amCleanTableRequired as example_agendas_get_agenda_with7amCleanTableRequired,
    get_agenda_base_time_example as example_agendas_get_agenda_base_time_example,
    get_agenda_x1_3levels_1required_1acptfacts as example_agendas_get_agenda_x1_3levels_1required_1acptfacts,
)

from src.economy.economy import EconomyUnit, economyunit_shop
from src.economy.examples.example_clerks import (
    get_1node_agenda as example_healers_get_1node_agenda,
    get_7nodeJRootWithH_agenda as example_healers_get_7nodeJRootWithH_agenda,
    get_agenda_2CleanNodesRandomWeights as example_healers_get_agenda_2CleanNodesRandomWeights,
    get_agenda_3CleanNodesRandomWeights as example_healers_get_agenda_3CleanNodesRandomWeights,
)
from os import listdir as os_listdir, rename as os_rename, path as os_path
from pytest import fixture as pytest_fixture


def get_temp_env_economy_id():
    return "ex_env04"


def get_temp_env_dir():
    return f"{get_test_economys_dir()}/{get_temp_env_economy_id()}"


def get_test_economys_dir():
    return "src/economy/examples/economys"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)


def create_agenda_file_for_economys(economy_dir: str, agenda_healer: str):
    x_agenda = agendaunit_shop(_healer=agenda_healer)
    agenda_dir = f"{economy_dir}/agendas"
    # file_path = f"{agenda_dir}/{x_agenda._healer}.json"
    # if not path.exists(file_path):
    # print(f"{file_path=} {x_agenda._healer=}")

    save_file(
        dest_dir=agenda_dir,
        file_name=f"{x_agenda._healer}.json",
        file_text=x_agenda.get_json(),
    )


def create_example_economys_list():
    return dir_files(
        dir_path=get_test_economys_dir(), include_dirs=True, include_files=False
    )


def setup_test_example_environment():
    _delete_and_set_ex3()
    _delete_and_set_ex4()
    _delete_and_set_ex5()
    _delete_and_set_ex6()


def _delete_and_set_ex3():
    economy_id = "ex3"
    x_economy = economyunit_shop(
        economy_id=economy_id, economys_dir=get_test_economys_dir()
    )
    delete_dir(x_economy.get_object_root_dir())
    x_economy.create_dirs_if_null(in_memory_treasury=True)
    x_economy.save_public_agenda(example_healers_get_1node_agenda())
    x_economy.save_public_agenda(
        example_agendas_get_agenda_1Task_1CE0MinutesRequired_1AcptFact()
    )
    example_agenda_v001 = example_agendas_agenda_v001()
    example_agenda_v002 = example_agendas_agenda_v002()
    x_economy.save_public_agenda(example_agenda_v001)
    x_economy.save_public_agenda(example_agenda_v002)

    # x_economy.set_healer(x_clerk=clerkunit_shop(pid="w1", env_dir=x_economy.get_object_root_dir()))
    # x_economy.set_healer(x_clerk=clerkunit_shop(pid="w2", env_dir=x_economy.get_object_root_dir()))
    xia_text = "Xia"
    x_economy.create_new_clerkunit(clerk_cid=xia_text)
    healer_text = example_agenda_v002._healer
    x_economy.set_healer_depotlink(
        xia_text, agenda_healer=healer_text, depotlink_type="blind_trust"
    )
    # w1_obj = x_economy.get_clerkunit(cid=w1_text)

    bob_text = "bob wurld"
    create_agenda_file_for_economys(x_economy.get_object_root_dir(), bob_text)
    # print(f"create agenda_list {w1_text=}")
    x_economy.create_depotlink_to_generated_agenda(
        clerk_cid=xia_text, agenda_healer=bob_text, depotlink_type="ignore"
    )
    land_text = "tim wurld"
    create_agenda_file_for_economys(
        economy_dir=x_economy.get_object_root_dir(), agenda_healer=land_text
    )
    x_economy.create_depotlink_to_generated_agenda(
        clerk_cid=xia_text, agenda_healer=land_text, depotlink_type="blind_trust"
    )
    # x_economy.create_depotlink_to_generated_agenda(clerk_cid=w1_text, agenda_healer="test9")
    # x_economy.create_depotlink_to_generated_agenda(clerk_cid=w1_text, agenda_healer="Bobs agenda")
    x_economy.save_clerkunit_file(clerk_cid=xia_text)
    # print(f"WHAT WHAT {x_economy.get_object_root_dir()}")
    # print(f"WHAT WHAT {x_economy.get_object_root_dir()}/clerkunits/w1/w1.json")
    # file_text = open_file(
    #     dest_dir=f"{x_economy.get_object_root_dir}/clerkunits/w1", file_name="w1.json"
    # )
    # print(f"{file_text=}")
    # print(f"{len(x_economy._clerkunits.get(w1_text)._depotlinks)=}")
    # print(f"{x_economy._clerkunits.get(w1_text)._depotlinks.get(bob_text)=}")
    # print(f"{x_economy._clerkunits.get(w1_text).get_json=}")

    w2_text = "w2"
    x_economy.create_new_clerkunit(clerk_cid=w2_text)
    # , env_dir=x_economy.get_object_root_dir())
    x_economy.save_clerkunit_file(clerk_cid=w2_text)


def _delete_and_set_ex4():
    x_economy_id = "ex4"
    x_economy = economyunit_shop(x_economy_id, economys_dir=get_test_economys_dir())
    delete_dir(x_economy.get_object_root_dir())
    x_economy.create_dirs_if_null(in_memory_treasury=True)
    x_economy.save_public_agenda(example_healers_get_7nodeJRootWithH_agenda())
    x_economy.save_public_agenda(example_agendas_get_agenda_with7amCleanTableRequired())
    x_economy.save_public_agenda(example_agendas_get_agenda_base_time_example())
    x_economy.save_public_agenda(
        example_agendas_get_agenda_x1_3levels_1required_1acptfacts()
    )


def _delete_and_set_ex5():
    x_economy_id = "ex5"
    x_p = economyunit_shop(x_economy_id, economys_dir=get_test_economys_dir())
    delete_dir(x_p.get_object_root_dir())
    x_p.create_dirs_if_null(in_memory_treasury=True)

    # ethical code ernie
    # ethical code steve
    # ethical code Jessica
    # ethical code Francine
    # ethical code Clay
    agenda_1 = example_healers_get_agenda_2CleanNodesRandomWeights(_healer="ernie")
    agenda_2 = example_healers_get_agenda_2CleanNodesRandomWeights(_healer="steve")
    agenda_3 = example_healers_get_agenda_2CleanNodesRandomWeights(_healer="jessica")
    agenda_4 = example_healers_get_agenda_2CleanNodesRandomWeights(_healer="francine")
    agenda_5 = example_healers_get_agenda_2CleanNodesRandomWeights(_healer="clay")

    x_p.save_public_agenda(agenda_1)
    x_p.save_public_agenda(agenda_2)
    x_p.save_public_agenda(agenda_3)
    x_p.save_public_agenda(agenda_4)
    x_p.save_public_agenda(agenda_5)

    x_p.create_new_clerkunit(clerk_cid=agenda_1._healer)
    x_p.create_new_clerkunit(clerk_cid=agenda_2._healer)
    x_p.create_new_clerkunit(clerk_cid=agenda_3._healer)
    x_p.create_new_clerkunit(clerk_cid=agenda_4._healer)
    x_p.create_new_clerkunit(clerk_cid=agenda_5._healer)

    x_p.set_healer_depotlink(agenda_1._healer, agenda_2._healer, "blind_trust", 3, 3.1)
    x_p.set_healer_depotlink(agenda_1._healer, agenda_3._healer, "blind_trust", 7, 7.1)
    x_p.set_healer_depotlink(agenda_1._healer, agenda_4._healer, "blind_trust", 4, 4.1)
    x_p.set_healer_depotlink(agenda_1._healer, agenda_5._healer, "blind_trust", 5, 5.1)

    x_p.set_healer_depotlink(agenda_2._healer, agenda_1._healer, "blind_trust", 3, 3.1)
    x_p.set_healer_depotlink(agenda_2._healer, agenda_3._healer, "blind_trust", 7, 7.1)
    x_p.set_healer_depotlink(agenda_2._healer, agenda_4._healer, "blind_trust", 4, 4.1)
    x_agenda = example_healers_get_agenda_3CleanNodesRandomWeights()
    x_p.set_healer_depotlink(
        agenda_2._healer, agenda_5._healer, "ignore", 5, 5.1, x_agenda
    )

    x_p.set_healer_depotlink(agenda_3._healer, agenda_1._healer, "blind_trust", 3, 3.1)
    x_p.set_healer_depotlink(agenda_3._healer, agenda_2._healer, "blind_trust", 7, 7.1)
    x_p.set_healer_depotlink(agenda_3._healer, agenda_4._healer, "blind_trust", 4, 4.1)
    x_p.set_healer_depotlink(agenda_3._healer, agenda_5._healer, "blind_trust", 5, 5.1)

    x_p.set_healer_depotlink(agenda_4._healer, agenda_1._healer, "blind_trust", 3, 3.1)
    x_p.set_healer_depotlink(agenda_4._healer, agenda_2._healer, "blind_trust", 7, 7.1)
    x_p.set_healer_depotlink(agenda_4._healer, agenda_3._healer, "blind_trust", 4, 4.1)
    x_p.set_healer_depotlink(agenda_4._healer, agenda_5._healer, "blind_trust", 5, 5.1)

    x_p.set_healer_depotlink(agenda_5._healer, agenda_1._healer, "blind_trust", 3, 3.1)
    x_p.set_healer_depotlink(agenda_5._healer, agenda_2._healer, "blind_trust", 7, 7.1)
    x_p.set_healer_depotlink(agenda_5._healer, agenda_3._healer, "blind_trust", 4, 4.1)
    x_p.set_healer_depotlink(agenda_5._healer, agenda_4._healer, "blind_trust", 5, 5.1)

    x_p.save_clerkunit_file(clerk_cid=agenda_1._healer)
    x_p.save_clerkunit_file(clerk_cid=agenda_2._healer)
    x_p.save_clerkunit_file(clerk_cid=agenda_3._healer)
    x_p.save_clerkunit_file(clerk_cid=agenda_4._healer)
    x_p.save_clerkunit_file(clerk_cid=agenda_5._healer)


def _delete_and_set_ex6(x_economy_id: str = None):
    if x_economy_id is None:
        x_economy_id = "ex6"
    x_economy = economyunit_shop(x_economy_id, economys_dir=get_test_economys_dir())
    delete_dir(x_economy.get_object_root_dir())
    x_economy.create_dirs_if_null(in_memory_treasury=False)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(pid=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(pid=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(pid=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_economy.save_public_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(pid=sal_text, creditor_weight=2)
    x_economy.save_public_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(pid=elu_text, creditor_weight=2)
    x_economy.save_public_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(pid=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(pid=sal_text, creditor_weight=1)
    x_economy.save_public_agenda(elu_agenda)

    x_economy.refresh_treasury_public_agendas_data()
    x_economy.set_credit_flow_for_agenda(agenda_healer=sal_text, max_blocks_count=100)

    return x_economy


def create_example_economy(economy_id: str):
    x_economy = economyunit_shop(
        economy_id=economy_id, economys_dir=get_test_economys_dir()
    )
    x_economy.create_dirs_if_null(in_memory_treasury=True)


def delete_dir_example_economy(economy_obj: EconomyUnit):
    delete_dir(economy_obj.get_object_root_dir())


def change_economy_id_example_economy(economy_obj: EconomyUnit, new_economy_id):
    # base_dir = economy_obj.get_object_root_dir()
    base_dir = "src/economy/examples/economys"
    src_dir = f"{base_dir}/{economy_obj.economy_id}"
    dst_dir = f"{base_dir}/{new_economy_id}"
    os_rename(src=src_dir, dst=dst_dir)
    economy_obj.set_economy_id(economy_id=new_economy_id)


class InvalideconomyCopyException(Exception):
    pass


def copy_evaluation_economy(src_economy_id: str, dest_economy_id: str):
    base_dir = "src/economy/examples/economys"
    new_dir = f"{base_dir}/{dest_economy_id}"
    if os_path.exists(new_dir):
        raise InvalideconomyCopyException(
            f"Cannot copy economy to '{new_dir}' directory because '{new_dir}' exists."
        )
    # base_dir = economy_obj.get_object_root_dir()
    src_dir = f"{base_dir}/{src_economy_id}"
    dest_dir = f"{base_dir}/{dest_economy_id}"
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
