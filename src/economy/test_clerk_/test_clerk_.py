from src.agenda.road import get_node_delimiter
from src.agenda.agenda import agendaunit_shop
from src.agenda.x_func import delete_dir as x_func_delete_dir
from src.economy.clerk import clerkunit_shop, clerkUnit
from src.economy.examples.clerk_env_kit import (
    clerk_dir_setup_cleanup,
    get_temp_clerkunit_dir,
    get_temp_economy_id,
)
from os import path as os_path


def test_clerkUnit_exists(clerk_dir_setup_cleanup):
    # GIVEN / WHEN
    x_clerk = clerkUnit()

    # GIVEN
    assert x_clerk != None
    assert x_clerk._contract is None
    assert x_clerk._clerk_cid is None
    assert x_clerk._env_dir is None
    assert x_clerk._economy_id is None
    assert x_clerk._clerkunit_dir is None
    assert x_clerk._clerkunits_dir is None
    assert x_clerk._contract_file_name is None
    assert x_clerk._contract_file_path is None
    assert x_clerk._agenda_output_file_name is None
    assert x_clerk._agenda_output_file_path is None
    assert x_clerk._public_file_name is None
    assert x_clerk._agendas_public_dir is None
    assert x_clerk._agendas_depot_dir is None
    assert x_clerk._agendas_ignore_dir is None
    assert x_clerk._agendas_digest_dir is None
    assert x_clerk._road_node_delimiter is None


def test_clerkunit_shop_exists(clerk_dir_setup_cleanup):
    # GIVEN
    x_pid = "test1"

    # WHEN
    x_clerk = clerkunit_shop(
        pid=x_pid,
        env_dir=get_temp_clerkunit_dir(),
        economy_id=get_temp_economy_id(),
    )

    # GIVEN
    assert x_clerk._clerk_cid != None
    assert x_clerk._economy_id != None
    assert x_clerk._economy_id == get_temp_economy_id()
    assert x_clerk._road_node_delimiter == get_node_delimiter()
    assert x_clerk._contract != None
    assert x_clerk._contract._economy_id == get_temp_economy_id()


def test_clerkunit_auto_output_to_public_SavesAgendaToPublicDirWhenTrue(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_clerkunit_dir()
    x_economy_id = get_temp_economy_id()
    tim_text = "Tim"
    public_file_name = f"{tim_text}.json"
    public_file_path = f"{get_temp_clerkunit_dir()}/agendas/{public_file_name}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/economy/examples/ex_env/agendas/{public_file_name}"
    x_clerk = clerkunit_shop(
        tim_text, env_dir, x_economy_id, _auto_output_to_public=True
    )
    x_clerk.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    tim_agenda = agendaunit_shop(_healer=tim_text)
    tim_agenda.set_economy_id(x_economy_id)
    x_clerk.set_depot_agenda(tim_agenda, "blind_trust")

    # THEN
    assert os_path.exists(public_file_path)


def test_clerkunit_auto_output_to_public_DoesNotSaveAgendaToPublicDirWhenFalse(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_clerkunit_dir()
    x_economy_id = get_temp_economy_id()
    tim_text = "Tim"
    public_file_name = f"{tim_text}.json"
    public_file_path = f"{get_temp_clerkunit_dir()}/agendas/{public_file_name}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/economy/examples/ex_env/agendas/{public_file_name}"
    x_clerk = clerkunit_shop(tim_text, env_dir, x_economy_id, False)
    x_clerk.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    x_clerk.set_depot_agenda(agendaunit_shop(tim_text), depotlink_type="blind_trust")

    # THEN
    assert os_path.exists(public_file_path) is False


def test_clerkunit_get_contract_createsEmptyAgendaWhenFileDoesNotExist(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    slash_text = "/"
    tim_clerk = clerkUnit(
        _clerk_cid="Tim",
        _env_dir=get_temp_clerkunit_dir(),
        _economy_id=get_temp_economy_id(),
        _road_node_delimiter=slash_text,
    )
    tim_clerk.set_env_dir(
        env_dir=get_temp_clerkunit_dir(),
        clerk_cid="Tim",
        economy_id=get_temp_economy_id(),
        _road_node_delimiter=get_node_delimiter(slash_text),
    )
    tim_clerk.set_dirs()
    tim_clerk.create_core_dir_and_files()
    assert os_path.exists(tim_clerk._contract_file_path)
    x_func_delete_dir(dir=tim_clerk._contract_file_path)
    assert os_path.exists(tim_clerk._contract_file_path) is False
    assert tim_clerk._contract is None

    # WHEN
    contract_agenda = tim_clerk.get_contract()

    # THEN
    assert os_path.exists(tim_clerk._contract_file_path)
    assert tim_clerk._contract != None
    assert contract_agenda._road_node_delimiter != None
    assert contract_agenda._road_node_delimiter == slash_text


def test_clerkunit_get_contract_getsMemoryAgendaIfExists(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_clerk = clerkunit_shop(
        tim_text, get_temp_clerkunit_dir(), get_temp_economy_id()
    )
    tim_clerk.create_core_dir_and_files()
    contract_file_path = f"{tim_clerk._clerkunit_dir}/{tim_clerk._contract_file_name}"
    contract_agenda1 = tim_clerk.get_contract()
    assert os_path.exists(contract_file_path)
    assert tim_clerk._contract != None

    # WHEN
    ray_text = "Ray"
    tim_clerk._contract = agendaunit_shop(_healer=ray_text)
    contract_agenda2 = tim_clerk.get_contract()

    # THEN
    assert contract_agenda2._healer == ray_text
    assert contract_agenda2 != contract_agenda1

    # WHEN
    tim_clerk._contract = None
    contract_agenda3 = tim_clerk.get_contract()

    # THEN
    assert contract_agenda3._healer != ray_text
    assert contract_agenda3 == contract_agenda1


def test_clerkunit_set_contract_savescontractAgendaSet_contract_None(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_clerk = clerkunit_shop(
        tim_text, get_temp_clerkunit_dir(), get_temp_economy_id()
    )
    tim_clerk.create_core_dir_and_files()
    contract_file_path = f"{tim_clerk._clerkunit_dir}/{tim_clerk._contract_file_name}"
    contract_agenda1 = tim_clerk.get_contract()
    assert os_path.exists(contract_file_path)
    assert tim_clerk._contract != None

    # WHEN
    uid_text = "Not a real uid"
    tim_clerk._contract._idearoot._uid = uid_text
    tim_clerk.set_contract()

    # THEN
    assert os_path.exists(contract_file_path)
    assert tim_clerk._contract is None
    contract_agenda2 = tim_clerk.get_contract()
    assert contract_agenda2._idearoot._uid == uid_text


def test_clerkunit_set_contract_savesGivenAgendaSet_contract_None(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_clerk = clerkunit_shop(
        tim_text, get_temp_clerkunit_dir(), get_temp_economy_id()
    )
    tim_clerk.create_core_dir_and_files()
    contract_file_path = f"{tim_clerk._clerkunit_dir}/{tim_clerk._contract_file_name}"
    contract_agenda1 = tim_clerk.get_contract()
    assert os_path.exists(contract_file_path)
    assert tim_clerk._contract != None

    # WHEN
    contract_uid_text = "this is ._contract uid"
    tim_clerk._contract._idearoot._uid = contract_uid_text

    new_agenda = agendaunit_shop(_healer=tim_text)
    new_agenda_uid_text = "this is pulled AgendaUnit uid"
    new_agenda._idearoot._uid = new_agenda_uid_text

    tim_clerk.set_contract(new_agenda)

    # THEN
    assert os_path.exists(contract_file_path)
    assert tim_clerk._contract is None
    assert tim_clerk.get_contract()._idearoot._uid != contract_uid_text
    assert tim_clerk.get_contract()._idearoot._uid == new_agenda_uid_text

    # GIVEN
    tim_clerk.set_contract(new_agenda)
    assert os_path.exists(contract_file_path)
    assert tim_clerk._contract is None

    # WHEN
    tim_clerk.set_contract_if_empty()

    # THEN
    assert tim_clerk._contract != None
    assert os_path.exists(contract_file_path)

    # WHEN
    contract_uid_text = "this is ._contract uid"
    tim_clerk._contract._idearoot._uid = contract_uid_text


def test_clerkunit_set_contract_if_emtpy_DoesNotReplace_contract(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_clerk = clerkunit_shop(
        tim_text, get_temp_clerkunit_dir(), get_temp_economy_id()
    )
    tim_clerk.create_core_dir_and_files()
    saved_agenda = agendaunit_shop(_healer=tim_text)
    saved_agenda_uid_text = "this is pulled AgendaUnit uid"
    saved_agenda._idearoot._uid = saved_agenda_uid_text
    tim_clerk.set_contract(saved_agenda)
    tim_clerk.get_contract()
    assert tim_clerk._contract != None

    # WHEN
    contract_uid_text = "this is ._contract uid"
    tim_clerk._contract._idearoot._uid = contract_uid_text
    tim_clerk.set_contract_if_empty()

    # THEN
    assert tim_clerk._contract != None
    assert tim_clerk._contract._idearoot._uid == contract_uid_text
    assert tim_clerk._contract._idearoot._uid != saved_agenda_uid_text
