from src._road.road import (
    default_road_delimiter_if_none,
    create_road_from_nodes,
    create_road,
    get_default_real_id_roadnode as root_label,
)
from src._road.finance import default_planck_if_none
from src._road.jaar_config import (
    get_test_reals_dir,
    get_test_real_id,
    get_rootpart_of_econ_dir,
)
from src.agenda.agenda import agendaunit_shop
from src.change.filehub import (
    get_econ_path,
    FileHub,
    filehub_shop,
    get_nox_type_set,
)
from src.change.examples.examples import get_agenda_with_4_levels
from src.change.examples.change_env import (
    get_texas_filehub,
    get_change_temp_env_dir,
    env_dir_setup_cleanup,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_get_econ_path_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    peru_text = "peru"
    sue_filehub = filehub_shop(None, real_id=peru_text, person_id=sue_text)
    texas_text = "texas"
    dallas_text = "dallas"
    elpaso_text = "el paso"
    kern_text = "kern"
    idearoot = get_rootpart_of_econ_dir()
    texas_road = create_road_from_nodes([idearoot, texas_text])
    dallas_road = create_road_from_nodes([idearoot, texas_text, dallas_text])
    elpaso_road = create_road_from_nodes([idearoot, texas_text, elpaso_text])
    kern_road = create_road_from_nodes([idearoot, texas_text, elpaso_text, kern_text])

    # WHEN
    texas_path = get_econ_path(sue_filehub, texas_road)
    dallas_path = get_econ_path(sue_filehub, dallas_road)
    elpaso_path = get_econ_path(sue_filehub, elpaso_road)
    kern_path = get_econ_path(sue_filehub, kern_road)

    # THEN
    idearoot_dir = f"{sue_filehub.econs_dir()}/{get_rootpart_of_econ_dir()}"
    print(f"{kern_road=}")
    print(f"{idearoot_dir=}")
    assert texas_path == f"{idearoot_dir}/{texas_text}"
    assert dallas_path == f"{idearoot_dir}/{texas_text}/{dallas_text}"
    assert elpaso_path == f"{idearoot_dir}/{texas_text}/{elpaso_text}"
    assert kern_path == f"{idearoot_dir}/{texas_text}/{elpaso_text}/{kern_text}"

    # WHEN / THEN
    diff_root_texas_road = create_road_from_nodes([peru_text, texas_text])
    diff_root_dallas_road = create_road_from_nodes([peru_text, texas_text, dallas_text])
    diff_root_elpaso_road = create_road_from_nodes([peru_text, texas_text, elpaso_text])
    assert texas_path == get_econ_path(sue_filehub, diff_root_texas_road)
    assert dallas_path == get_econ_path(sue_filehub, diff_root_dallas_road)
    assert elpaso_path == get_econ_path(sue_filehub, diff_root_elpaso_road)


def test_get_nox_type_set_ReturnsObj():
    # GIVEN / WHEN / THEN
    assert get_nox_type_set() == {"duty_work", "role_job", "job_work"}


def test_FileHub_Exists():
    # GIVEN / WHEN
    x_filehub = FileHub()

    # THEN
    assert x_filehub.reals_dir is None
    assert x_filehub.real_id is None
    assert x_filehub.person_id is None
    assert x_filehub.econ_road is None
    assert x_filehub._nox_type is None
    assert x_filehub.road_delimiter is None
    assert x_filehub.planck is None


def test_filehub_shop_ReturnsCorrectObjWhenEmpty():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)

    # WHEN
    sue_filehub = filehub_shop(None, None, sue_text, texas_road)

    # THEN
    assert sue_filehub.reals_dir == get_test_reals_dir()
    assert sue_filehub.real_id == get_test_real_id()
    assert sue_filehub.real_dir() == f"{get_test_reals_dir()}/{get_test_real_id()}"
    assert sue_filehub.person_id == sue_text
    assert sue_filehub.road_delimiter == default_road_delimiter_if_none()
    assert sue_filehub.planck == default_planck_if_none()
    assert sue_filehub.persons_dir() == f"{sue_filehub.real_dir()}/persons"
    x_filehub = filehub_shop(None, None, sue_text)
    assert sue_filehub.econ_road == texas_road
    assert sue_filehub.econ_dir() == get_econ_path(x_filehub, texas_road)
    bob_text = "Bob"
    assert sue_filehub.roles_dir() == f"{sue_filehub.econ_dir()}/roles"
    assert sue_filehub.jobs_dir() == f"{sue_filehub.econ_dir()}/jobs"
    sue_roles_dir = sue_filehub.roles_dir()
    assert sue_filehub.role_path(bob_text) == f"{sue_roles_dir}/{bob_text}.json"
    sue_jobs_dir = sue_filehub.jobs_dir()
    assert sue_filehub.job_path(bob_text) == f"{sue_jobs_dir}/{bob_text}.json"
    treasury_file_name = "treasury.db"
    treasury_file_path = f"{sue_filehub.econ_dir()}/{treasury_file_name}"
    assert sue_filehub.treasury_file_name() == treasury_file_name
    assert sue_filehub.treasury_db_path() == treasury_file_path


def test_FileHub_create_econ_dir_if_missing_CreatesDirectory(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    assert os_path_exists(sue_filehub.econ_dir()) is False

    # WHEN
    sue_filehub.create_econ_dir_if_missing()

    # THEN
    assert os_path_exists(sue_filehub.econ_dir())


def test_FileHub_save_role_agenda_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    assert os_path_exists(sue_filehub.role_path(bob_text)) is False

    # WHEN
    sue_filehub.save_role_agenda(bob_agenda)

    # THEN
    assert os_path_exists(sue_filehub.role_path(bob_text))


def test_FileHub_role_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    assert sue_filehub.role_file_exists(bob_text) is False

    # WHEN
    sue_filehub.save_role_agenda(bob_agenda)

    # THEN
    assert sue_filehub.role_file_exists(bob_text)


def test_FileHub_get_role_agenda_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    sue_filehub.save_role_agenda(bob_agenda)

    # WHEN / THEN
    assert sue_filehub.get_role_agenda(bob_text).get_dict() == bob_agenda.get_dict()


def test_FileHub_delete_role_file_DeletesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    texas_filehub = get_texas_filehub()
    sue_agenda = get_agenda_with_4_levels()
    sue_text = sue_agenda._owner_id
    texas_filehub.save_role_agenda(sue_agenda)
    print(f"{texas_filehub.role_path(sue_text)=}")
    role_path = texas_filehub.role_path(sue_text)
    assert os_path_exists(role_path)

    # WHEN
    texas_filehub.delete_role_file(sue_text)

    # THEN
    assert os_path_exists(role_path) is False


def test_FileHub_save_job_agenda_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    assert os_path_exists(sue_filehub.job_path(bob_text)) is False

    # WHEN
    sue_filehub.save_job_agenda(bob_agenda)

    # THEN
    assert os_path_exists(sue_filehub.job_path(bob_text))


def test_FileHub_job_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    assert sue_filehub.job_file_exists(bob_text) is False

    # WHEN
    sue_filehub.save_job_agenda(bob_agenda)

    # THEN
    assert sue_filehub.job_file_exists(bob_text)


def test_FileHub_get_job_agenda_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    sue_filehub.save_job_agenda(bob_agenda)

    # WHEN / THEN
    assert sue_filehub.get_job_agenda(bob_text).get_dict() == bob_agenda.get_dict()


def test_FileHub_delete_job_file_DeletesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    texas_filehub = get_texas_filehub()
    sue_agenda = get_agenda_with_4_levels()
    sue_text = sue_agenda._owner_id
    texas_filehub.save_job_agenda(sue_agenda)
    print(f"{texas_filehub.job_path(sue_text)=}")
    job_path = texas_filehub.job_path(sue_text)
    assert os_path_exists(job_path)

    # WHEN
    texas_filehub.delete_job_file(sue_text)

    # THEN
    assert os_path_exists(job_path) is False


def test_FileHub_save_duty_agenda_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_agendaunit = get_agenda_with_4_levels()
    sue_text = sue_agendaunit._owner_id
    env_dir = get_change_temp_env_dir()
    real_id = root_label()
    sue_filehub = filehub_shop(env_dir, real_id, sue_text, None)

    print(f"{sue_filehub.duty_file_path()=}")
    assert sue_filehub.duty_file_exists() is False

    # WHEN
    sue_filehub.save_duty_agenda(sue_agendaunit)

    # THEN
    assert sue_filehub.duty_file_exists()


def test_FileHub_save_duty_agenda_RaisesErrorWhenAgenda_work_id_IsWrong(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_change_temp_env_dir()
    real_id = root_label()
    sue_filehub = filehub_shop(env_dir, real_id, sue_text, None)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_filehub.save_duty_agenda(agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s duty agenda."
    )


def test_FileHub_get_duty_agenda_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_agendaunit = get_agenda_with_4_levels()
    sue_text = sue_agendaunit._owner_id
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    sue_filehub.save_duty_agenda(sue_agendaunit)

    # WHEN / THEN
    assert sue_filehub.get_duty_agenda().get_dict() == sue_agendaunit.get_dict()


def test_FileHub_save_work_agenda_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_agendaunit = get_agenda_with_4_levels()
    sue_text = sue_agendaunit._owner_id
    env_dir = get_change_temp_env_dir()
    real_id = root_label()
    sue_filehub = filehub_shop(env_dir, real_id, sue_text, None)

    print(f"{sue_filehub.work_path()=}")
    assert sue_filehub.work_file_exists() is False

    # WHEN
    sue_filehub.save_work_agenda(sue_agendaunit)

    # THEN
    assert sue_filehub.work_file_exists()


def test_FileHub_get_work_agenda_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_agendaunit = get_agenda_with_4_levels()
    sue_text = sue_agendaunit._owner_id
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_filehub = filehub_shop(temp_env_dir, None, sue_text, texas_road)
    sue_filehub.save_work_agenda(sue_agendaunit)

    # WHEN / THEN
    assert sue_filehub.get_work_agenda().get_dict() == sue_agendaunit.get_dict()


def test_FileHub_save_work_agenda_RaisesErrorWhenAgenda_work_id_IsWrong(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_change_temp_env_dir()
    real_id = root_label()
    sue_filehub = filehub_shop(env_dir, real_id, sue_text, None)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_filehub.save_work_agenda(agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s work agenda."
    )
