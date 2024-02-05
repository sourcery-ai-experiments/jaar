# from lw.agenda import AgendaUnit
from src.agenda.agenda import agendaunit_shop
from src.instrument.file import (
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
    get_agenda_1Task_1CE0MinutesReason_1Belief as example_agendas_get_agenda_1Task_1CE0MinutesReason_1Belief,
    get_agenda_with7amCleanTableReason as example_agendas_get_agenda_with7amCleanTableReason,
    get_agenda_base_time_example as example_agendas_get_agenda_base_time_example,
    get_agenda_x1_3levels_1reason_1beliefs as example_agendas_get_agenda_x1_3levels_1reason_1beliefs,
)
from src.market.market import (
    MarketUnit,
    marketunit_shop,
    get_temp_env_market_id,
    get_temp_env_healer_id,
    get_temp_env_person_id,
    get_temp_env_problem_id,
)
from src.market.examples.example_clerks import (
    get_1node_agenda as example_get_1node_agenda,
    get_7nodeJRootWithH_agenda as example_get_7nodeJRootWithH_agenda,
    get_agenda_2CleanNodesRandomWeights as example_get_agenda_2CleanNodesRandomWeights,
    get_agenda_3CleanNodesRandomWeights as example_get_agenda_3CleanNodesRandomWeights,
)
from os import listdir as os_listdir, rename as os_rename, path as os_path
from pytest import fixture as pytest_fixture


def get_temp_env_dir():
    return f"{get_test_markets_dir()}/{get_temp_env_market_id()}"


def get_test_markets_dir():
    return "src/market/examples/markets"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_temp_env_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)


def create_agenda_file_for_markets(market_dir: str, agent_id: str):
    x_agenda = agendaunit_shop(_agent_id=agent_id)
    agenda_dir = f"{market_dir}/agendas"
    # file_path = f"{agenda_dir}/{x_agenda._agent_id}.json"
    # if not path.exists(file_path):
    # print(f"{file_path=} {x_agenda._agent_id=}")

    save_file(
        dest_dir=agenda_dir,
        file_name=f"{x_agenda._agent_id}.json",
        file_text=x_agenda.get_json(),
    )


def create_example_markets_list():
    return dir_files(
        dir_path=get_test_markets_dir(), include_dirs=True, include_files=False
    )


def setup_test_example_environment():
    _delete_and_set_ex3()
    _delete_and_set_ex4()
    _delete_and_set_ex5()
    _delete_and_set_ex6()


def _delete_and_set_ex3():
    market_id = "ex3"
    x_market = marketunit_shop(
        market_id=market_id, markets_dir=get_test_markets_dir()
    )
    delete_dir(x_market.get_object_root_dir())
    x_market.create_dirs_if_null(in_memory_treasury=True)
    x_market.save_forum_agenda(example_get_1node_agenda())
    x_market.save_forum_agenda(
        example_agendas_get_agenda_1Task_1CE0MinutesReason_1Belief()
    )
    example_agenda_v001 = example_agendas_agenda_v001()
    example_agenda_v002 = example_agendas_agenda_v002()
    x_market.save_forum_agenda(example_agenda_v001)
    x_market.save_forum_agenda(example_agenda_v002)

    # x_market.set_agent_id(x_clerk=clerkunit_shop(agent_id="w1", env_dir=x_market.get_object_root_dir()))
    # x_market.set_agent_id(x_clerk=clerkunit_shop(agent_id="w2", env_dir=x_market.get_object_root_dir()))
    xia_text = "Xia"
    x_market.create_new_clerkunit(clerk_id=xia_text)
    bob_text = example_agenda_v002._agent_id
    x_market.set_clerk_depotlink(
        xia_text, agenda_agent_id=bob_text, depotlink_type="blind_trust"
    )
    # w1_obj = x_market.get_clerkunit(cid=w1_text)

    bob_text = "bob wurld"
    create_agenda_file_for_markets(x_market.get_object_root_dir(), bob_text)
    # print(f"create agenda_list {w1_text=}")
    x_market.create_depotlink_to_generated_agenda(
        clerk_id=xia_text, agent_id=bob_text, depotlink_type="ignore"
    )
    land_text = "tim wurld"
    create_agenda_file_for_markets(
        market_dir=x_market.get_object_root_dir(), agent_id=land_text
    )
    x_market.create_depotlink_to_generated_agenda(
        clerk_id=xia_text, agent_id=land_text, depotlink_type="blind_trust"
    )
    # x_market.create_depotlink_to_generated_agenda(clerk_id=w1_text, agent_id="test9")
    # x_market.create_depotlink_to_generated_agenda(clerk_id=w1_text, agent_id="Bobs agenda")
    x_market.save_clerkunit_file(clerk_id=xia_text)
    # print(f"WHAT WHAT {x_market.get_object_root_dir()}")
    # print(f"WHAT WHAT {x_market.get_object_root_dir()}/clerkunits/w1/w1.json")
    # file_text = open_file(
    #     dest_dir=f"{x_market.get_object_root_dir}/clerkunits/w1", file_name="w1.json"
    # )
    # print(f"{file_text=}")
    # print(f"{len(x_market._clerkunits.get(w1_text)._depotlinks)=}")
    # print(f"{x_market._clerkunits.get(w1_text)._depotlinks.get(bob_text)=}")
    # print(f"{x_market._clerkunits.get(w1_text).get_json=}")

    w2_text = "w2"
    x_market.create_new_clerkunit(clerk_id=w2_text)
    # , env_dir=x_market.get_object_root_dir())
    x_market.save_clerkunit_file(clerk_id=w2_text)


def _delete_and_set_ex4():
    x_market_id = "ex4"
    x_market = marketunit_shop(x_market_id, markets_dir=get_test_markets_dir())
    delete_dir(x_market.get_object_root_dir())
    x_market.create_dirs_if_null(in_memory_treasury=True)
    x_market.save_forum_agenda(example_get_7nodeJRootWithH_agenda())
    x_market.save_forum_agenda(example_agendas_get_agenda_with7amCleanTableReason())
    x_market.save_forum_agenda(example_agendas_get_agenda_base_time_example())
    x_market.save_forum_agenda(
        example_agendas_get_agenda_x1_3levels_1reason_1beliefs()
    )


def _delete_and_set_ex5():
    x_market_id = "ex5"
    x_p = marketunit_shop(x_market_id, markets_dir=get_test_markets_dir())
    delete_dir(x_p.get_object_root_dir())
    x_p.create_dirs_if_null(in_memory_treasury=True)

    # ethical code ernie
    # ethical code steve
    # ethical code Jessica
    # ethical code Francine
    # ethical code Clayenda
    ag_1 = example_get_agenda_2CleanNodesRandomWeights("ernie")
    ag_2 = example_get_agenda_2CleanNodesRandomWeights("steve")
    ag_3 = example_get_agenda_2CleanNodesRandomWeights("jessica")
    ag_4 = example_get_agenda_2CleanNodesRandomWeights("francine")
    ag_5 = example_get_agenda_2CleanNodesRandomWeights("clay")

    x_p.save_forum_agenda(ag_1)
    x_p.save_forum_agenda(ag_2)
    x_p.save_forum_agenda(ag_3)
    x_p.save_forum_agenda(ag_4)
    x_p.save_forum_agenda(ag_5)

    x_p.create_new_clerkunit(clerk_id=ag_1._agent_id)
    x_p.create_new_clerkunit(clerk_id=ag_2._agent_id)
    x_p.create_new_clerkunit(clerk_id=ag_3._agent_id)
    x_p.create_new_clerkunit(clerk_id=ag_4._agent_id)
    x_p.create_new_clerkunit(clerk_id=ag_5._agent_id)

    x_p.set_clerk_depotlink(ag_1._agent_id, ag_2._agent_id, "blind_trust", 3, 3.1)
    x_p.set_clerk_depotlink(ag_1._agent_id, ag_3._agent_id, "blind_trust", 7, 7.1)
    x_p.set_clerk_depotlink(ag_1._agent_id, ag_4._agent_id, "blind_trust", 4, 4.1)
    x_p.set_clerk_depotlink(ag_1._agent_id, ag_5._agent_id, "blind_trust", 5, 5.1)

    x_p.set_clerk_depotlink(ag_2._agent_id, ag_1._agent_id, "blind_trust", 3, 3.1)
    x_p.set_clerk_depotlink(ag_2._agent_id, ag_3._agent_id, "blind_trust", 7, 7.1)
    x_p.set_clerk_depotlink(ag_2._agent_id, ag_4._agent_id, "blind_trust", 4, 4.1)
    x_agenda = example_get_agenda_3CleanNodesRandomWeights()
    x_p.set_clerk_depotlink(ag_2._agent_id, ag_5._agent_id, "ignore", 5, 5.1, x_agenda)

    x_p.set_clerk_depotlink(ag_3._agent_id, ag_1._agent_id, "blind_trust", 3, 3.1)
    x_p.set_clerk_depotlink(ag_3._agent_id, ag_2._agent_id, "blind_trust", 7, 7.1)
    x_p.set_clerk_depotlink(ag_3._agent_id, ag_4._agent_id, "blind_trust", 4, 4.1)
    x_p.set_clerk_depotlink(ag_3._agent_id, ag_5._agent_id, "blind_trust", 5, 5.1)

    x_p.set_clerk_depotlink(ag_4._agent_id, ag_1._agent_id, "blind_trust", 3, 3.1)
    x_p.set_clerk_depotlink(ag_4._agent_id, ag_2._agent_id, "blind_trust", 7, 7.1)
    x_p.set_clerk_depotlink(ag_4._agent_id, ag_3._agent_id, "blind_trust", 4, 4.1)
    x_p.set_clerk_depotlink(ag_4._agent_id, ag_5._agent_id, "blind_trust", 5, 5.1)

    x_p.set_clerk_depotlink(ag_5._agent_id, ag_1._agent_id, "blind_trust", 3, 3.1)
    x_p.set_clerk_depotlink(ag_5._agent_id, ag_2._agent_id, "blind_trust", 7, 7.1)
    x_p.set_clerk_depotlink(ag_5._agent_id, ag_3._agent_id, "blind_trust", 4, 4.1)
    x_p.set_clerk_depotlink(ag_5._agent_id, ag_4._agent_id, "blind_trust", 5, 5.1)

    x_p.save_clerkunit_file(clerk_id=ag_1._agent_id)
    x_p.save_clerkunit_file(clerk_id=ag_2._agent_id)
    x_p.save_clerkunit_file(clerk_id=ag_3._agent_id)
    x_p.save_clerkunit_file(clerk_id=ag_4._agent_id)
    x_p.save_clerkunit_file(clerk_id=ag_5._agent_id)


def _delete_and_set_ex6(x_market_id: str = None):
    if x_market_id is None:
        x_market_id = "ex6"
    x_market = marketunit_shop(x_market_id, markets_dir=get_test_markets_dir())
    delete_dir(x_market.get_object_root_dir())
    x_market.create_dirs_if_null(in_memory_treasury=False)

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_agent_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_agent_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_market.save_forum_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_agent_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_market.save_forum_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_agent_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_market.save_forum_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_agent_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_market.save_forum_agenda(elu_agenda)

    x_market.refresh_treasury_forum_agendas_data()
    x_market.set_credit_flow_for_agenda(agent_id=sal_text, max_blocks_count=100)

    return x_market


def create_example_market(market_id: str):
    x_market = marketunit_shop(
        market_id=market_id, markets_dir=get_test_markets_dir()
    )
    x_market.create_dirs_if_null(in_memory_treasury=True)


def delete_dir_example_market(market_obj: MarketUnit):
    delete_dir(market_obj.get_object_root_dir())


def change_market_id_example_market(market_obj: MarketUnit, new_market_id):
    # base_dir = market_obj.get_object_root_dir()
    base_dir = "src/market/examples/markets"
    src_dir = f"{base_dir}/{market_obj.market_id}"
    dst_dir = f"{base_dir}/{new_market_id}"
    os_rename(src=src_dir, dst=dst_dir)
    market_obj.set_market_id(market_id=new_market_id)


class InvalidmarketCopyException(Exception):
    pass


def copy_evaluation_market(src_market_id: str, dest_market_id: str):
    base_dir = "src/market/examples/markets"
    new_dir = f"{base_dir}/{dest_market_id}"
    if os_path.exists(new_dir):
        raise InvalidmarketCopyException(
            f"Cannot copy market to '{new_dir}' directory because '{new_dir}' exists."
        )
    # base_dir = market_obj.get_object_root_dir()
    src_dir = f"{base_dir}/{src_market_id}"
    dest_dir = f"{base_dir}/{dest_market_id}"
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
