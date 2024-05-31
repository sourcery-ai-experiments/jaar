from src._instrument.file import delete_dir, copy_dir, save_file, dir_files
from src._road.road import create_road_from_nodes, RoadUnit
from src._road.worlddir import econdir_shop, EconDir
from src.agenda.agenda import agendaunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with7amCleanTableReason as example_agendas_get_agenda_with7amCleanTableReason,
    get_agenda_base_time_example as example_agendas_get_agenda_base_time_example,
    get_agenda_x1_3levels_1reason_1beliefs as example_agendas_get_agenda_x1_3levels_1reason_1beliefs,
)
from src.econ.econ import EconUnit, econunit_shop, temp_real_id, temp_person_id
from src.econ.examples.example_econ_agendas import (
    get_7nodeJRootWithH_agenda as example_get_7nodeJRootWithH_agenda,
)
from os import rename as os_rename, path as os_path
from pytest import fixture as pytest_fixture


def temp_real_dir():
    return f"{temp_reals_dir()}/{temp_real_id()}"


def temp_reals_dir():
    return "src/econ/examples/reals"


@pytest_fixture()
def env_dir_setup_cleanup():
    env_dir = temp_reals_dir()
    delete_dir(env_dir)
    yield env_dir
    delete_dir(env_dir)


def get_texas_road() -> RoadUnit:
    naton_text = "nation-state"
    usa_text = "usa"
    texas_text = "texas"
    return create_road_from_nodes([naton_text, usa_text, texas_text])


def get_texas_econdir() -> EconDir:
    return econdir_shop(
        temp_reals_dir(), temp_real_id(), temp_person_id(), get_texas_road()
    )


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
    return dir_files(dir_path=temp_reals_dir(), include_dirs=True, include_files=False)


def setup_test_example_environment():
    # _delete_and_set_ex3()
    _delete_and_set_ex4()
    # _delete_and_set_ex5()
    _delete_and_set_ex6()


def _delete_and_set_ex4():
    ex4_id = "ex4"
    ex4_econdir = get_texas_econdir()
    ex4_econdir.real_id = ex4_id
    x_econ = econunit_shop(ex4_econdir)
    delete_dir(x_econ.get_object_root_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)
    x_econ.save_job_file(example_get_7nodeJRootWithH_agenda())
    x_econ.save_job_file(example_agendas_get_agenda_with7amCleanTableReason())
    x_econ.save_job_file(example_agendas_get_agenda_base_time_example())
    x_econ.save_job_file(example_agendas_get_agenda_x1_3levels_1reason_1beliefs())


def _delete_and_set_ex6(ex6_id: str = None):
    if ex6_id is None:
        ex6_id = "ex6"
    ex6_econdir = get_texas_econdir()
    ex6_econdir.real_id = ex6_id
    x_econ = econunit_shop(ex6_econdir)
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
    x_econ.save_job_file(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.save_job_file(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_econ.save_job_file(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_econ.save_job_file(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_econ.save_job_file(elu_agenda)

    x_econ.refresh_treasury_job_agendas_data()
    x_econ.set_credit_flow_for_agenda(owner_id=sal_text, max_blocks_count=100)

    return x_econ


# def modify_real_id_example_econ(
#     econ_obj: EconUnit, src_econdir: EconDir, dst_econdir: EconDir, new_real_id
# ):
#     src_dir = src_econdir.econ_dir()
#     dst_dir = dst_econdir.econ_dir()
#     print(f"     {os_path.exists(src_dir)=}")
#     print(f"     {src_dir=}")
#     print(f"     {dst_dir=}")

#     os_rename(src=src_dir, dst=dst_dir)
#     econ_obj.set_real_id(real_id=new_real_id)
#     econ_obj.econ_dir = dst_dir


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
