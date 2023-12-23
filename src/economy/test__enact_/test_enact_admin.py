from src.agenda.x_func import (
    open_file as x_func_open_file,
    save_file as x_func_save_file,
)
from src.economy.enact import EnactUnit, enactunit_shop
from src.economy.examples.example_enacts import (
    get_6node_agenda as example_healers_get_6node_agenda,
    get_6node_agenda as example_healers_get_7nodeJRootWithH_agenda,
)
from src.economy.examples.enact_env_kit import (
    get_temp_enactunit_dir,
    get_temp_economy_id,
    enact_dir_setup_cleanup,
)
from os import path as os_path


def test_EnactUnit_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_enactunit_dir()

    # WHEN
    bob_enactadmin = EnactUnit(bob_text, env_dir, get_temp_economy_id())

    # THEN
    assert bob_enactadmin._enact_cid != None
    assert bob_enactadmin._env_dir != None
    assert bob_enactadmin._economy_id != None
    assert bob_enactadmin._road_node_delimiter is None
    assert bob_enactadmin._enactunit_dir is None
    assert bob_enactadmin._contract_file_name is None
    assert bob_enactadmin._contract_file_path is None
    assert bob_enactadmin._agenda_output_file_name is None
    assert bob_enactadmin._agenda_output_file_path is None
    assert bob_enactadmin._public_file_name is None
    assert bob_enactadmin._agendas_public_dir is None
    assert bob_enactadmin._agendas_depot_dir is None
    assert bob_enactadmin._agendas_ignore_dir is None
    assert bob_enactadmin._agendas_digest_dir is None


def test_EnactUnit_set_dir_CorrectSetsEnactUnitAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_enactunit_dir()
    bob_enactadmin = EnactUnit(bob_text, env_dir, get_temp_economy_id())
    assert bob_enactadmin._enactunit_dir is None
    assert bob_enactadmin._agenda_output_file_name is None
    assert bob_enactadmin._agenda_output_file_path is None
    assert bob_enactadmin._public_file_name is None
    assert bob_enactadmin._agendas_public_dir is None
    assert bob_enactadmin._agendas_depot_dir is None
    assert bob_enactadmin._agendas_ignore_dir is None
    assert bob_enactadmin._agendas_digest_dir is None
    assert bob_enactadmin._contract_file_name is None
    assert bob_enactadmin._contract_file_path is None
    # WHEN
    bob_enactadmin.set_dirs()

    # THEN
    assert bob_enactadmin._enactunit_dir != None
    assert bob_enactadmin._agenda_output_file_name != None
    assert bob_enactadmin._agenda_output_file_path != None
    assert bob_enactadmin._public_file_name != None
    assert bob_enactadmin._agendas_public_dir != None
    assert bob_enactadmin._agendas_depot_dir != None
    assert bob_enactadmin._agendas_ignore_dir != None
    assert bob_enactadmin._agendas_digest_dir != None
    assert bob_enactadmin._contract_file_name != None
    assert bob_enactadmin._contract_file_path != None

    healers_drectory_folder = "enactunits"
    x_enactunits_dir = f"{env_dir}/{healers_drectory_folder}"
    x_enactunit_dir = f"{x_enactunits_dir}/{bob_text}"
    x_public_file_name = f"{bob_text}.json"
    x_contract_file_name = "contract_agenda.json"
    x_contract_file_path = f"{x_enactunit_dir}/{x_contract_file_name}"
    x_agenda_output_file_name = "output_agenda.json"
    x_agenda_output_file_path = f"{x_enactunit_dir}/{x_agenda_output_file_name}"
    agendas_str = "agendas"
    x_agendas_depot_dir = f"{x_enactunit_dir}/{agendas_str}"
    x_agendas_ignore_dir = f"{x_enactunit_dir}/ignores"
    x_agendas_digest_dir = f"{x_enactunit_dir}/digests"
    x_agendas_public_dir = f"{env_dir}/{agendas_str}"
    assert bob_enactadmin._enactunits_dir == x_enactunits_dir
    assert bob_enactadmin._enactunit_dir == x_enactunit_dir
    assert bob_enactadmin._contract_file_name == x_contract_file_name
    assert bob_enactadmin._contract_file_path == x_contract_file_path
    assert bob_enactadmin._agenda_output_file_name == x_agenda_output_file_name
    assert bob_enactadmin._agenda_output_file_path == x_agenda_output_file_path
    assert bob_enactadmin._agendas_depot_dir == x_agendas_depot_dir
    assert bob_enactadmin._agendas_ignore_dir == x_agendas_ignore_dir
    assert bob_enactadmin._agendas_digest_dir == x_agendas_digest_dir
    assert bob_enactadmin._public_file_name == x_public_file_name
    assert bob_enactadmin._agendas_public_dir == x_agendas_public_dir


def test_EnactUnit_create_core_dir_and_files_CreatesDirsAndFiles(
    enact_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_enactunit_dir()
    jul_enactunit = EnactUnit(
        _enact_cid=jul_text,
        _env_dir=env_dir,
        _economy_id=get_temp_economy_id(),
        _road_node_delimiter=",",
    )
    jul_enactunit.set_dirs()
    assert os_path.exists(jul_enactunit._enactunits_dir) is False
    assert os_path.exists(jul_enactunit._enactunit_dir) is False
    assert os_path.exists(jul_enactunit._contract_file_path) is False
    assert os_path.isdir(jul_enactunit._enactunit_dir) is False
    assert os_path.exists(jul_enactunit._agendas_depot_dir) is False
    assert os_path.exists(jul_enactunit._agendas_digest_dir) is False
    assert os_path.exists(jul_enactunit._agendas_ignore_dir) is False

    # WHEN
    x_agenda = example_healers_get_7nodeJRootWithH_agenda()
    jul_enactunit.create_core_dir_and_files(x_agenda)

    # THEN check agendas src directory created
    print(f"Checking {jul_enactunit._enactunits_dir=}")
    print(f"Checking {jul_enactunit._enactunit_dir=}")
    assert os_path.exists(jul_enactunit._enactunits_dir)
    assert os_path.exists(jul_enactunit._enactunit_dir)
    assert os_path.exists(jul_enactunit._contract_file_path)
    assert os_path.isdir(jul_enactunit._enactunit_dir)
    assert os_path.exists(jul_enactunit._agendas_depot_dir)
    assert os_path.exists(jul_enactunit._agendas_digest_dir)
    assert os_path.exists(jul_enactunit._agendas_ignore_dir)


def test_EnactUnit_create_core_dir_and_files_DoesNotOverWritecontractAgenda(
    enact_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_enactunit_dir()
    jul_enactunit = enactunit_shop(jul_text, env_dir, get_temp_economy_id())
    jul_enactunit.set_dirs()
    x_agenda = example_healers_get_7nodeJRootWithH_agenda()
    jul_enactunit.create_core_dir_and_files(x_agenda)
    assert os_path.exists(jul_enactunit._contract_file_path)
    # jul_cx = agenda_get_from_json(x_func_open_file(jul_enactunit._contract_file_path))
    ex1 = "teesting text"
    x_func_save_file(
        dest_dir=jul_enactunit._enactunit_dir,
        file_name=jul_enactunit._contract_file_name,
        file_text=ex1,
    )
    assert (
        x_func_open_file(
            jul_enactunit._enactunit_dir, jul_enactunit._contract_file_name
        )
        == ex1
    )

    # WHEN
    jul_enactunit.create_core_dir_and_files(x_agenda)

    # THEN
    assert (
        x_func_open_file(
            jul_enactunit._enactunit_dir, jul_enactunit._contract_file_name
        )
        == ex1
    )


def test_EnactUnit_set_enact_cid_WorksCorrectly(enact_dir_setup_cleanup):
    # GIVEN create healer
    env_dir = get_temp_enactunit_dir()

    old_healer_text = "bob"
    jul_enactunit = enactunit_shop(old_healer_text, env_dir, get_temp_economy_id())
    x_agenda = example_healers_get_7nodeJRootWithH_agenda()
    jul_enactunit.set_dirs()
    jul_enactunit.create_core_dir_and_files(x_agenda)
    old_enactunit_dir = jul_enactunit._enactunit_dir
    # old_enactunit_dir = f"{env_dir}/enactunits/{old_healer_text}"
    print(f"{jul_enactunit._enactunit_dir}")
    enactunits_text = "enactunits"
    enactunits_dir = f"{env_dir}/enactunits"
    print(f"{enactunits_dir}/{old_healer_text}")
    contract_file_name = "contract_agenda.json"
    old_contract_file_path = f"{old_enactunit_dir}/{contract_file_name}"

    assert os_path.exists(old_enactunit_dir)
    assert os_path.isdir(old_enactunit_dir)
    assert os_path.exists(old_contract_file_path)

    new_healer_text = "tim"
    new_enactunit_dir = f"{enactunits_dir}/{new_healer_text}"
    new_contract_file_path = f"{new_enactunit_dir}/{contract_file_name}"
    assert os_path.exists(new_enactunit_dir) == False
    assert os_path.isdir(new_enactunit_dir) == False
    assert os_path.exists(new_contract_file_path) == False

    # WHEN
    jul_enactunit.set_enact_cid(new_cid=new_healer_text)

    # THEN
    assert os_path.exists(old_enactunit_dir) == False
    assert os_path.isdir(old_enactunit_dir) == False
    assert os_path.exists(old_contract_file_path) == False
    assert os_path.exists(new_enactunit_dir)
    assert os_path.isdir(new_enactunit_dir)
    assert os_path.exists(new_contract_file_path)


def test_enactunit_auto_output_to_public_SavesAgendaToPublicDir(
    enact_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    bob_enactadmin = enactunit_shop(
        bob_text, get_temp_enactunit_dir(), get_temp_economy_id()
    )
    x_agenda = example_healers_get_6node_agenda()
    x_agenda.set_healer(new_healer=bob_text)
    bob_enactadmin.create_core_dir_and_files(x_agenda)

    public_file_path = (
        f"{bob_enactadmin._agendas_public_dir}/{bob_enactadmin._public_file_name}"
    )
    print(f"{public_file_path=}")
    assert os_path.exists(public_file_path) is False

    # WHEN
    bob_enactadmin.save_agenda_to_public(x_agenda)

    # THEN
    assert os_path.exists(public_file_path)
