from src.agenda.x_func import (
    open_file as x_func_open_file,
    save_file as x_func_save_file,
)
from src.culture.council import CouncilAdmin, counciladmin_shop
from src.culture.examples.example_councils import (
    get_6node_agenda as example_healers_get_6node_agenda,
    get_6node_agenda as example_healers_get_7nodeJRootWithH_agenda,
)
from src.culture.examples.council_env_kit import (
    get_temp_councilunit_dir,
    get_temp_culture_handle,
    council_dir_setup_cleanup,
)
from os import path as os_path


def test_CouncilAdmin_exists():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_councilunit_dir()

    # WHEN
    bob_counciladmin = CouncilAdmin(bob_text, env_dir, get_temp_culture_handle())

    # THEN
    assert bob_counciladmin._council_dub != None
    assert bob_counciladmin._env_dir != None
    assert bob_counciladmin._culture_handle != None
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


def test_CouncilAdmin_set_dir_CorrectSetsCouncilAdminAttribute():
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_councilunit_dir()
    bob_counciladmin = CouncilAdmin(bob_text, env_dir, get_temp_culture_handle())
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


def test_CouncilAdmin_create_core_dir_and_files_CreatesDirsAndFiles(
    council_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_councilunit_dir()
    jul_counciladmin = counciladmin_shop(jul_text, env_dir, get_temp_culture_handle())
    jul_counciladmin.set_dirs()
    assert os_path.exists(jul_counciladmin._councilunits_dir) is False
    assert os_path.exists(jul_counciladmin._councilunit_dir) is False
    assert os_path.exists(jul_counciladmin._seed_file_path) is False
    assert os_path.isdir(jul_counciladmin._councilunit_dir) is False
    assert os_path.exists(jul_counciladmin._agendas_depot_dir) is False
    assert os_path.exists(jul_counciladmin._agendas_digest_dir) is False
    assert os_path.exists(jul_counciladmin._agendas_ignore_dir) is False

    # WHEN
    x_agenda = example_healers_get_7nodeJRootWithH_agenda()
    jul_counciladmin.create_core_dir_and_files(x_agenda)

    # THEN check agendas src directory created
    print(f"Checking {jul_counciladmin._councilunits_dir=}")
    print(f"Checking {jul_counciladmin._councilunit_dir=}")
    assert os_path.exists(jul_counciladmin._councilunits_dir)
    assert os_path.exists(jul_counciladmin._councilunit_dir)
    assert os_path.exists(jul_counciladmin._seed_file_path)
    assert os_path.isdir(jul_counciladmin._councilunit_dir)
    assert os_path.exists(jul_counciladmin._agendas_depot_dir)
    assert os_path.exists(jul_counciladmin._agendas_digest_dir)
    assert os_path.exists(jul_counciladmin._agendas_ignore_dir)


def test_CouncilAdmin_create_core_dir_and_files_DoesNotOverWriteseedAgenda(
    council_dir_setup_cleanup,
):
    # GIVEN create healer
    jul_text = "julian"
    env_dir = get_temp_councilunit_dir()
    jul_counciladmin = counciladmin_shop(jul_text, env_dir, get_temp_culture_handle())
    jul_counciladmin.set_dirs()
    x_agenda = example_healers_get_7nodeJRootWithH_agenda()
    jul_counciladmin.create_core_dir_and_files(x_agenda)
    assert os_path.exists(jul_counciladmin._seed_file_path)
    # jul_cx = agenda_get_from_json(x_func_open_file(jul_counciladmin._seed_file_path))
    ex1 = "teesting text"
    x_func_save_file(
        dest_dir=jul_counciladmin._councilunit_dir,
        file_name=jul_counciladmin._seed_file_name,
        file_text=ex1,
    )
    assert (
        x_func_open_file(
            jul_counciladmin._councilunit_dir, jul_counciladmin._seed_file_name
        )
        == ex1
    )

    # WHEN
    jul_counciladmin.create_core_dir_and_files(x_agenda)

    # THEN
    assert (
        x_func_open_file(
            jul_counciladmin._councilunit_dir, jul_counciladmin._seed_file_name
        )
        == ex1
    )


def test_CouncilAdmin_set_council_dub_WorksCorrectly(council_dir_setup_cleanup):
    # GIVEN create healer
    env_dir = get_temp_councilunit_dir()

    old_healer_text = "bob"
    jul_counciladmin = counciladmin_shop(
        old_healer_text, env_dir, get_temp_culture_handle()
    )
    x_agenda = example_healers_get_7nodeJRootWithH_agenda()
    jul_counciladmin.set_dirs()
    jul_counciladmin.create_core_dir_and_files(x_agenda)
    old_councilunit_dir = jul_counciladmin._councilunit_dir
    # old_councilunit_dir = f"{env_dir}/councilunits/{old_healer_text}"
    print(f"{jul_counciladmin._councilunit_dir}")
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
    jul_counciladmin.set_council_dub(new_dub=new_healer_text)

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
    bob_counciladmin = counciladmin_shop(
        bob_text, get_temp_councilunit_dir(), get_temp_culture_handle()
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
