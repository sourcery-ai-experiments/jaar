from src.tools.file import open_file, save_file
from src.economy.clerk import clerkUnit, clerkunit_shop
from src.economy.examples.example_clerks import (
    get_6node_agenda as example_get_6node_agenda,
    get_6node_agenda as example_get_7nodeJRootWithH_agenda,
)
from src.economy.examples.clerk_env_kit import (
    get_temp_clerkunit_dir,
    get_temp_economy_id,
    clerk_dir_setup_cleanup,
)
from os import path as os_path


def test_clerkUnit_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_clerkunit_dir()

    # WHEN
    bob_clerkadmin = clerkUnit(bob_text, env_dir, get_temp_economy_id())

    # THEN
    assert bob_clerkadmin._clerk_cid != None
    assert bob_clerkadmin._env_dir != None
    assert bob_clerkadmin._economy_id != None
    assert bob_clerkadmin._road_delimiter is None
    assert bob_clerkadmin._clerkunit_dir is None
    assert bob_clerkadmin._contract_file_name is None
    assert bob_clerkadmin._contract_file_path is None
    assert bob_clerkadmin._agenda_output_file_name is None
    assert bob_clerkadmin._agenda_output_file_path is None
    assert bob_clerkadmin._forum_file_name is None
    assert bob_clerkadmin._agendas_forum_dir is None
    assert bob_clerkadmin._agendas_depot_dir is None
    assert bob_clerkadmin._agendas_ignore_dir is None
    assert bob_clerkadmin._agendas_digest_dir is None


def test_clerkUnit_set_dir_CorrectSetsclerkUnitAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_clerkunit_dir()
    bob_clerkadmin = clerkUnit(bob_text, env_dir, get_temp_economy_id())
    assert bob_clerkadmin._clerkunit_dir is None
    assert bob_clerkadmin._agenda_output_file_name is None
    assert bob_clerkadmin._agenda_output_file_path is None
    assert bob_clerkadmin._forum_file_name is None
    assert bob_clerkadmin._agendas_forum_dir is None
    assert bob_clerkadmin._agendas_depot_dir is None
    assert bob_clerkadmin._agendas_ignore_dir is None
    assert bob_clerkadmin._agendas_digest_dir is None
    assert bob_clerkadmin._contract_file_name is None
    assert bob_clerkadmin._contract_file_path is None
    # WHEN
    bob_clerkadmin.set_dirs()

    # THEN
    assert bob_clerkadmin._clerkunit_dir != None
    assert bob_clerkadmin._agenda_output_file_name != None
    assert bob_clerkadmin._agenda_output_file_path != None
    assert bob_clerkadmin._forum_file_name != None
    assert bob_clerkadmin._agendas_forum_dir != None
    assert bob_clerkadmin._agendas_depot_dir != None
    assert bob_clerkadmin._agendas_ignore_dir != None
    assert bob_clerkadmin._agendas_digest_dir != None
    assert bob_clerkadmin._contract_file_name != None
    assert bob_clerkadmin._contract_file_path != None

    healers_drectory_folder = "clerkunits"
    x_clerkunits_dir = f"{env_dir}/{healers_drectory_folder}"
    x_clerkunit_dir = f"{x_clerkunits_dir}/{bob_text}"
    x_forum_file_name = f"{bob_text}.json"
    x_contract_file_name = "contract_agenda.json"
    x_contract_file_path = f"{x_clerkunit_dir}/{x_contract_file_name}"
    x_agenda_output_file_name = "output_agenda.json"
    x_agenda_output_file_path = f"{x_clerkunit_dir}/{x_agenda_output_file_name}"
    agendas_str = "agendas"
    x_agendas_depot_dir = f"{x_clerkunit_dir}/{agendas_str}"
    x_agendas_ignore_dir = f"{x_clerkunit_dir}/ignores"
    x_agendas_digest_dir = f"{x_clerkunit_dir}/digests"
    x_agendas_forum_dir = f"{env_dir}/{agendas_str}"
    assert bob_clerkadmin._clerkunits_dir == x_clerkunits_dir
    assert bob_clerkadmin._clerkunit_dir == x_clerkunit_dir
    assert bob_clerkadmin._contract_file_name == x_contract_file_name
    assert bob_clerkadmin._contract_file_path == x_contract_file_path
    assert bob_clerkadmin._agenda_output_file_name == x_agenda_output_file_name
    assert bob_clerkadmin._agenda_output_file_path == x_agenda_output_file_path
    assert bob_clerkadmin._agendas_depot_dir == x_agendas_depot_dir
    assert bob_clerkadmin._agendas_ignore_dir == x_agendas_ignore_dir
    assert bob_clerkadmin._agendas_digest_dir == x_agendas_digest_dir
    assert bob_clerkadmin._forum_file_name == x_forum_file_name
    assert bob_clerkadmin._agendas_forum_dir == x_agendas_forum_dir


def test_clerkUnit_create_core_dir_and_files_CreatesDirsAndFiles(
    clerk_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_clerkunit_dir()
    jul_clerkunit = clerkUnit(
        _clerk_cid=jul_text,
        _env_dir=env_dir,
        _economy_id=get_temp_economy_id(),
        _road_delimiter=",",
    )
    jul_clerkunit.set_dirs()
    assert os_path.exists(jul_clerkunit._clerkunits_dir) is False
    assert os_path.exists(jul_clerkunit._clerkunit_dir) is False
    assert os_path.exists(jul_clerkunit._contract_file_path) is False
    assert os_path.isdir(jul_clerkunit._clerkunit_dir) is False
    assert os_path.exists(jul_clerkunit._agendas_depot_dir) is False
    assert os_path.exists(jul_clerkunit._agendas_digest_dir) is False
    assert os_path.exists(jul_clerkunit._agendas_ignore_dir) is False

    # WHEN
    x_agenda = example_get_7nodeJRootWithH_agenda()
    jul_clerkunit.create_core_dir_and_files(x_agenda)

    # THEN check agendas src directory created
    print(f"Checking {jul_clerkunit._clerkunits_dir=}")
    print(f"Checking {jul_clerkunit._clerkunit_dir=}")
    assert os_path.exists(jul_clerkunit._clerkunits_dir)
    assert os_path.exists(jul_clerkunit._clerkunit_dir)
    assert os_path.exists(jul_clerkunit._contract_file_path)
    assert os_path.isdir(jul_clerkunit._clerkunit_dir)
    assert os_path.exists(jul_clerkunit._agendas_depot_dir)
    assert os_path.exists(jul_clerkunit._agendas_digest_dir)
    assert os_path.exists(jul_clerkunit._agendas_ignore_dir)


def test_clerkUnit_create_core_dir_and_files_DoesNotOverWritecontractAgenda(
    clerk_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_clerkunit_dir()
    jul_clerkunit = clerkunit_shop(jul_text, env_dir, get_temp_economy_id())
    jul_clerkunit.set_dirs()
    x_agenda = example_get_7nodeJRootWithH_agenda()
    jul_clerkunit.create_core_dir_and_files(x_agenda)
    assert os_path.exists(jul_clerkunit._contract_file_path)
    # jul_cx = agenda_get_from_json(open_file(jul_clerkunit._contract_file_path))
    ex1 = "teesting text"
    save_file(
        dest_dir=jul_clerkunit._clerkunit_dir,
        file_name=jul_clerkunit._contract_file_name,
        file_text=ex1,
    )
    assert (
        open_file(jul_clerkunit._clerkunit_dir, jul_clerkunit._contract_file_name)
        == ex1
    )

    # WHEN
    jul_clerkunit.create_core_dir_and_files(x_agenda)

    # THEN
    assert (
        open_file(jul_clerkunit._clerkunit_dir, jul_clerkunit._contract_file_name)
        == ex1
    )


def test_clerkUnit_set_clerk_cid_WorksCorrectly(clerk_dir_setup_cleanup):
    # GIVEN create healer
    env_dir = get_temp_clerkunit_dir()

    old_bob_text = "bob"
    jul_clerkunit = clerkunit_shop(old_bob_text, env_dir, get_temp_economy_id())
    x_agenda = example_get_7nodeJRootWithH_agenda()
    jul_clerkunit.set_dirs()
    jul_clerkunit.create_core_dir_and_files(x_agenda)
    old_clerkunit_dir = jul_clerkunit._clerkunit_dir
    # old_clerkunit_dir = f"{env_dir}/clerkunits/{old_healer_text}"
    print(f"{jul_clerkunit._clerkunit_dir}")
    clerkunits_text = "clerkunits"
    clerkunits_dir = f"{env_dir}/clerkunits"
    print(f"{clerkunits_dir}/{old_bob_text}")
    contract_file_name = "contract_agenda.json"
    old_contract_file_path = f"{old_clerkunit_dir}/{contract_file_name}"

    assert os_path.exists(old_clerkunit_dir)
    assert os_path.isdir(old_clerkunit_dir)
    assert os_path.exists(old_contract_file_path)

    tim_text = "tim"
    new_clerkunit_dir = f"{clerkunits_dir}/{tim_text}"
    new_contract_file_path = f"{new_clerkunit_dir}/{contract_file_name}"
    assert os_path.exists(new_clerkunit_dir) == False
    assert os_path.isdir(new_clerkunit_dir) == False
    assert os_path.exists(new_contract_file_path) == False

    # WHEN
    jul_clerkunit.set_clerk_cid(new_cid=tim_text)

    # THEN
    assert os_path.exists(old_clerkunit_dir) == False
    assert os_path.isdir(old_clerkunit_dir) == False
    assert os_path.exists(old_contract_file_path) == False
    assert os_path.exists(new_clerkunit_dir)
    assert os_path.isdir(new_clerkunit_dir)
    assert os_path.exists(new_contract_file_path)


def test_clerkunit_auto_output_to_forum_SavesAgendaToForumDir(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    bob_clerkadmin = clerkunit_shop(
        bob_text, get_temp_clerkunit_dir(), get_temp_economy_id()
    )
    x_agenda = example_get_6node_agenda()
    x_agenda.set_agent_id(new_agent_id=bob_text)
    bob_clerkadmin.create_core_dir_and_files(x_agenda)

    forum_file_path = (
        f"{bob_clerkadmin._agendas_forum_dir}/{bob_clerkadmin._forum_file_name}"
    )
    print(f"{forum_file_path=}")
    assert os_path.exists(forum_file_path) is False

    # WHEN
    bob_clerkadmin.save_agenda_to_forum(x_agenda)

    # THEN
    assert os_path.exists(forum_file_path)
