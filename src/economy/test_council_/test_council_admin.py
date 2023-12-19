from src.agenda.x_func import (
    open_file as x_func_open_file,
    save_file as x_func_save_file,
)
from src.economy.council import CouncilUnit, councilunit_shop
from src.economy.examples.example_councils import (
    get_6node_agenda as example_healers_get_6node_agenda,
    get_6node_agenda as example_healers_get_7nodeJRootWithH_agenda,
)
from src.economy.examples.council_env_kit import (
    get_temp_councilunit_dir,
    get_temp_economy_id,
    council_dir_setup_cleanup,
)
from os import path as os_path


def test_CouncilUnit_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_councilunit_dir()

    # WHEN
    bob_counciladmin = CouncilUnit(bob_text, env_dir, get_temp_economy_id())

    # THEN
    assert bob_counciladmin._council_cid != None
    assert bob_counciladmin._env_dir != None
    assert bob_counciladmin._economy_id != None
    assert bob_counciladmin._road_node_delimiter is None
    assert bob_counciladmin._councilunit_dir is None
    assert bob_counciladmin._seed_file_name is None
    assert bob_counciladmin._seed_file_path is None
    assert bob_counciladmin._agenda_output_file_name is None
    assert bob_counciladmin._agenda_output_file_path is None
    assert bob_counciladmin._public_file_name is None
    assert bob_counciladmin._agendas_public_dir is None
    assert bob_counciladmin._agendas_depot_dir is None
    assert bob_counciladmin._agendas_ignore_dir is None
    assert bob_counciladmin._agendas_digest_dir is None


def test_CouncilUnit_set_dir_CorrectSetsCouncilUnitAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_councilunit_dir()
    bob_counciladmin = CouncilUnit(bob_text, env_dir, get_temp_economy_id())
    assert bob_counciladmin._councilunit_dir is None
    assert bob_counciladmin._agenda_output_file_name is None
    assert bob_counciladmin._agenda_output_file_path is None
    assert bob_counciladmin._public_file_name is None
    assert bob_counciladmin._agendas_public_dir is None
    assert bob_counciladmin._agendas_depot_dir is None
    assert bob_counciladmin._agendas_ignore_dir is None
    assert bob_counciladmin._agendas_digest_dir is None
    assert bob_counciladmin._seed_file_name is None
    assert bob_counciladmin._seed_file_path is None
    # WHEN
    bob_counciladmin.set_dirs()

    # THEN
    assert bob_counciladmin._councilunit_dir != None
    assert bob_counciladmin._agenda_output_file_name != None
    assert bob_counciladmin._agenda_output_file_path != None
    assert bob_counciladmin._public_file_name != None
    assert bob_counciladmin._agendas_public_dir != None
    assert bob_counciladmin._agendas_depot_dir != None
    assert bob_counciladmin._agendas_ignore_dir != None
    assert bob_counciladmin._agendas_digest_dir != None
    assert bob_counciladmin._seed_file_name != None
    assert bob_counciladmin._seed_file_path != None

    healers_drectory_folder = "councilunits"
    x_councilunits_dir = f"{env_dir}/{healers_drectory_folder}"
    x_councilunit_dir = f"{x_councilunits_dir}/{bob_text}"
    x_public_file_name = f"{bob_text}.json"
    x_seed_file_name = "seed_agenda.json"
    x_seed_file_path = f"{x_councilunit_dir}/{x_seed_file_name}"
    x_agenda_output_file_name = "output_agenda.json"
    x_agenda_output_file_path = f"{x_councilunit_dir}/{x_agenda_output_file_name}"
    agendas_str = "agendas"
    x_agendas_depot_dir = f"{x_councilunit_dir}/{agendas_str}"
    x_agendas_ignore_dir = f"{x_councilunit_dir}/ignores"
    x_agendas_digest_dir = f"{x_councilunit_dir}/digests"
    x_agendas_public_dir = f"{env_dir}/{agendas_str}"
    assert bob_counciladmin._councilunits_dir == x_councilunits_dir
    assert bob_counciladmin._councilunit_dir == x_councilunit_dir
    assert bob_counciladmin._seed_file_name == x_seed_file_name
    assert bob_counciladmin._seed_file_path == x_seed_file_path
    assert bob_counciladmin._agenda_output_file_name == x_agenda_output_file_name
    assert bob_counciladmin._agenda_output_file_path == x_agenda_output_file_path
    assert bob_counciladmin._agendas_depot_dir == x_agendas_depot_dir
    assert bob_counciladmin._agendas_ignore_dir == x_agendas_ignore_dir
    assert bob_counciladmin._agendas_digest_dir == x_agendas_digest_dir
    assert bob_counciladmin._public_file_name == x_public_file_name
    assert bob_counciladmin._agendas_public_dir == x_agendas_public_dir


def test_CouncilUnit_create_core_dir_and_files_CreatesDirsAndFiles(
    council_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_councilunit_dir()
    jul_councilunit = CouncilUnit(
        _council_cid=jul_text,
        _env_dir=env_dir,
        _economy_id=get_temp_economy_id(),
        _road_node_delimiter=",",
    )
    jul_councilunit.set_dirs()
    assert os_path.exists(jul_councilunit._councilunits_dir) is False
    assert os_path.exists(jul_councilunit._councilunit_dir) is False
    assert os_path.exists(jul_councilunit._seed_file_path) is False
    assert os_path.isdir(jul_councilunit._councilunit_dir) is False
    assert os_path.exists(jul_councilunit._agendas_depot_dir) is False
    assert os_path.exists(jul_councilunit._agendas_digest_dir) is False
    assert os_path.exists(jul_councilunit._agendas_ignore_dir) is False

    # WHEN
    x_agenda = example_healers_get_7nodeJRootWithH_agenda()
    jul_councilunit.create_core_dir_and_files(x_agenda)

    # THEN check agendas src directory created
    print(f"Checking {jul_councilunit._councilunits_dir=}")
    print(f"Checking {jul_councilunit._councilunit_dir=}")
    assert os_path.exists(jul_councilunit._councilunits_dir)
    assert os_path.exists(jul_councilunit._councilunit_dir)
    assert os_path.exists(jul_councilunit._seed_file_path)
    assert os_path.isdir(jul_councilunit._councilunit_dir)
    assert os_path.exists(jul_councilunit._agendas_depot_dir)
    assert os_path.exists(jul_councilunit._agendas_digest_dir)
    assert os_path.exists(jul_councilunit._agendas_ignore_dir)


def test_CouncilUnit_create_core_dir_and_files_DoesNotOverWriteseedAgenda(
    council_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_councilunit_dir()
    jul_councilunit = councilunit_shop(jul_text, env_dir, get_temp_economy_id())
    jul_councilunit.set_dirs()
    x_agenda = example_healers_get_7nodeJRootWithH_agenda()
    jul_councilunit.create_core_dir_and_files(x_agenda)
    assert os_path.exists(jul_councilunit._seed_file_path)
    # jul_cx = agenda_get_from_json(x_func_open_file(jul_councilunit._seed_file_path))
    ex1 = "teesting text"
    x_func_save_file(
        dest_dir=jul_councilunit._councilunit_dir,
        file_name=jul_councilunit._seed_file_name,
        file_text=ex1,
    )
    assert (
        x_func_open_file(
            jul_councilunit._councilunit_dir, jul_councilunit._seed_file_name
        )
        == ex1
    )

    # WHEN
    jul_councilunit.create_core_dir_and_files(x_agenda)

    # THEN
    assert (
        x_func_open_file(
            jul_councilunit._councilunit_dir, jul_councilunit._seed_file_name
        )
        == ex1
    )


def test_CouncilUnit_set_council_cid_WorksCorrectly(council_dir_setup_cleanup):
    # GIVEN create healer
    env_dir = get_temp_councilunit_dir()

    old_healer_text = "bob"
    jul_councilunit = councilunit_shop(old_healer_text, env_dir, get_temp_economy_id())
    x_agenda = example_healers_get_7nodeJRootWithH_agenda()
    jul_councilunit.set_dirs()
    jul_councilunit.create_core_dir_and_files(x_agenda)
    old_councilunit_dir = jul_councilunit._councilunit_dir
    # old_councilunit_dir = f"{env_dir}/councilunits/{old_healer_text}"
    print(f"{jul_councilunit._councilunit_dir}")
    councilunits_text = "councilunits"
    councilunits_dir = f"{env_dir}/councilunits"
    print(f"{councilunits_dir}/{old_healer_text}")
    seed_file_name = "seed_agenda.json"
    old_seed_file_path = f"{old_councilunit_dir}/{seed_file_name}"

    assert os_path.exists(old_councilunit_dir)
    assert os_path.isdir(old_councilunit_dir)
    assert os_path.exists(old_seed_file_path)

    new_healer_text = "tim"
    new_councilunit_dir = f"{councilunits_dir}/{new_healer_text}"
    new_seed_file_path = f"{new_councilunit_dir}/{seed_file_name}"
    assert os_path.exists(new_councilunit_dir) == False
    assert os_path.isdir(new_councilunit_dir) == False
    assert os_path.exists(new_seed_file_path) == False

    # WHEN
    jul_councilunit.set_council_cid(new_cid=new_healer_text)

    # THEN
    assert os_path.exists(old_councilunit_dir) == False
    assert os_path.isdir(old_councilunit_dir) == False
    assert os_path.exists(old_seed_file_path) == False
    assert os_path.exists(new_councilunit_dir)
    assert os_path.isdir(new_councilunit_dir)
    assert os_path.exists(new_seed_file_path)


def test_councilunit_auto_output_to_public_SavesAgendaToPublicDir(
    council_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    bob_counciladmin = councilunit_shop(
        bob_text, get_temp_councilunit_dir(), get_temp_economy_id()
    )
    x_agenda = example_healers_get_6node_agenda()
    x_agenda.set_healer(new_healer=bob_text)
    bob_counciladmin.create_core_dir_and_files(x_agenda)

    public_file_path = (
        f"{bob_counciladmin._agendas_public_dir}/{bob_counciladmin._public_file_name}"
    )
    print(f"{public_file_path=}")
    assert os_path.exists(public_file_path) is False

    # WHEN
    bob_counciladmin.save_agenda_to_public(x_agenda)

    # THEN
    assert os_path.exists(public_file_path)
