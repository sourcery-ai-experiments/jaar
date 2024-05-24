# from lw.agenda import AgendaUnit
from src.agenda.agenda import agendaunit_shop
from src._instrument.file import (
    # set_dir,
    delete_dir,
    copy_dir,
    save_file,
    # open_file,
    dir_files,
)
from src.agenda.examples.example_agendas import (
    # agenda_v001 as example_agendas_agenda_v001,
    # agenda_v002 as example_agendas_agenda_v002,
    # get_agenda_1Task_1CE0MinutesReason_1Belief as example_agendas_get_agenda_1Task_1CE0MinutesReason_1Belief,
    get_agenda_with7amCleanTableReason as example_agendas_get_agenda_with7amCleanTableReason,
    get_agenda_base_time_example as example_agendas_get_agenda_base_time_example,
    get_agenda_x1_3levels_1reason_1beliefs as example_agendas_get_agenda_x1_3levels_1reason_1beliefs,
)
from src.econ.econ import (
    EconUnit,
    econunit_shop,
    get_temp_env_real_id,
)
from src.econ.examples.example_econ_agendas import (
    get_7nodeJRootWithH_agenda as example_get_7nodeJRootWithH_agenda,
    # get_agenda_2CleanNodesRandomWeights as example_get_agenda_2CleanNodesRandomWeights,
    # get_agenda_3CleanNodesRandomWeights as example_get_agenda_3CleanNodesRandomWeights,
)
from os import rename as os_rename, path as os_path
from pytest import fixture as pytest_fixture


def get_test_econ_dir():
    return f"{get_test_econs_dir()}/{get_temp_env_real_id()}"


def get_test_econs_dir():
    return "src/econ/examples/econs"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = get_test_econ_dir()
    delete_dir(dir=env_dir)
    yield env_dir
    delete_dir(dir=env_dir)


def create_agenda_file_for_econs(econ_dir: str, owner_id: str):
    x_agenda = agendaunit_shop(_owner_id=owner_id)
    agenda_dir = f"{econ_dir}/agendas"
    # file_path = f"{agenda_dir}/{x_agenda._owner_id}.json"
    # if not path.exists(file_path):
    # print(f"{file_path=} {x_agenda._owner_id=}")

    save_file(
        dest_dir=agenda_dir,
        file_name=f"{x_agenda._owner_id}.json",
        file_text=x_agenda.get_json(),
    )


def create_example_econs_list():
    return dir_files(
        dir_path=get_test_econs_dir(), include_dirs=True, include_files=False
    )


def setup_test_example_environment():
    # _delete_and_set_ex3()
    _delete_and_set_ex4()
    # _delete_and_set_ex5()
    _delete_and_set_ex6()


def _delete_and_set_ex4():
    ex4_id = "ex4"
    ex4_dir = f"{get_test_econs_dir()}/{ex4_id}"
    x_econ = econunit_shop(ex4_id, econ_dir=ex4_dir)
    delete_dir(x_econ.get_object_root_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    x_econ.save_file_to_jobs(example_get_7nodeJRootWithH_agenda())
    x_econ.save_file_to_jobs(example_agendas_get_agenda_with7amCleanTableReason())
    x_econ.save_file_to_jobs(example_agendas_get_agenda_base_time_example())
    x_econ.save_file_to_jobs(example_agendas_get_agenda_x1_3levels_1reason_1beliefs())


def _delete_and_set_ex6(ex6_id: str = None):
    if ex6_id is None:
        ex6_id = "ex6"
    ex6_dir = f"{get_test_econs_dir()}/{ex6_id}"
    x_econ = econunit_shop(ex6_id, econ_dir=ex6_dir)
    delete_dir(x_econ.get_object_root_dir())
    x_econ.set_econ_dirs(in_memory_treasury=False)

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.save_file_to_jobs(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.save_file_to_jobs(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_econ.save_file_to_jobs(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_econ.save_file_to_jobs(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_econ.save_file_to_jobs(elu_agenda)

    x_econ.refresh_treasury_job_agendas_data()
    x_econ.set_credit_flow_for_agenda(owner_id=sal_text, max_blocks_count=100)

    return x_econ


def create_example_econ(real_id: str):
    x_econ = econunit_shop(real_id=real_id, econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)


def delete_dir_example_econ(econ_obj: EconUnit):
    delete_dir(econ_obj.get_object_root_dir())


def change_real_id_example_econ(econ_obj: EconUnit, new_real_id):
    # base_dir = econ_obj.get_object_root_dir()
    base_dir = "src/econ/examples/econs"
    src_dir = f"{base_dir}/{econ_obj.real_id}"
    dst_dir = f"{base_dir}/{new_real_id}"
    os_rename(src=src_dir, dst=dst_dir)
    econ_obj.set_real_id(real_id=new_real_id)
    econ_obj.econ_dir = dst_dir


class InvalideconCopyException(Exception):
    pass


def copy_evaluation_econ(src_real_id: str, dest_real_id: str):
    base_dir = "src/econ/examples/econs"
    new_dir = f"{base_dir}/{dest_real_id}"
    if os_path.exists(new_dir):
        raise InvalideconCopyException(
            f"Cannot copy econ to '{new_dir}' directory because '{new_dir}' exists."
        )
    # base_dir = econ_obj.get_object_root_dir()
    src_dir = f"{base_dir}/{src_real_id}"
    dest_dir = f"{base_dir}/{dest_real_id}"
    copy_dir(src_dir=src_dir, dest_dir=dest_dir)
