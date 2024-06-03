from src._road.road import (
    default_road_delimiter_if_none,
    create_road_from_nodes,
    create_road,
    get_default_real_id_roadnode as root_label,
)
from src._road.finance import default_planck_if_none
from src._road.jaar_config import (
    get_changes_folder,
    duty_str,
    work_str,
    get_test_reals_dir,
    get_test_real_id,
    get_rootpart_of_econ_dir,
)
from src.change.agendahub import (
    usernox_shop,
    get_econ_path,
    AgendaHub,
    agendahub_shop,
    get_nox_type_set,
)
from src.change.examples.examples import get_agenda_with_4_levels
from src.change.examples.change_env import (
    get_texas_agendahub,
    env_dir_setup_cleanup,
    get_change_temp_env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_get_econ_path_ReturnsCorrectObj():
    # GIVEN
    sue_text = "Sue"
    peru_text = "peru"
    sue_usernox = usernox_shop(None, real_id=peru_text, person_id=sue_text)
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
    texas_path = get_econ_path(sue_usernox, texas_road)
    dallas_path = get_econ_path(sue_usernox, dallas_road)
    elpaso_path = get_econ_path(sue_usernox, elpaso_road)
    kern_path = get_econ_path(sue_usernox, kern_road)

    # THEN
    idearoot_dir = f"{sue_usernox.econs_dir()}/{get_rootpart_of_econ_dir()}"
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
    assert texas_path == get_econ_path(sue_usernox, diff_root_texas_road)
    assert dallas_path == get_econ_path(sue_usernox, diff_root_dallas_road)
    assert elpaso_path == get_econ_path(sue_usernox, diff_root_elpaso_road)


def test_get_nox_type_set_ReturnsObj():
    # GIVEN / WHEN / THEN
    assert get_nox_type_set() == {"duty_work", "role_job", "job_work"}


def test_AgendaHub_Exists():
    # GIVEN / WHEN
    x_agendahub = AgendaHub()

    # THEN
    assert x_agendahub.reals_dir is None
    assert x_agendahub.real_id is None
    assert x_agendahub.person_id is None
    assert x_agendahub.econ_road is None
    assert x_agendahub._nox_type is None
    assert x_agendahub._road_delimiter is None
    assert x_agendahub._planck is None


def test_agendahub_shop_ReturnsCorrectObjWhenEmpty():
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)

    # WHEN
    sue_agendahub = agendahub_shop(None, None, sue_text, texas_road)

    # THEN
    assert sue_agendahub.reals_dir == get_test_reals_dir()
    assert sue_agendahub.real_id == get_test_real_id()
    assert sue_agendahub.real_dir() == f"{get_test_reals_dir()}/{get_test_real_id()}"
    assert sue_agendahub.person_id == sue_text
    assert sue_agendahub._road_delimiter == default_road_delimiter_if_none()
    assert sue_agendahub._planck == default_planck_if_none()
    assert sue_agendahub.persons_dir() == f"{sue_agendahub.real_dir()}/persons"
    x_usernox = usernox_shop(None, None, sue_text)
    assert sue_agendahub.econ_road == texas_road
    assert sue_agendahub.econ_dir() == get_econ_path(x_usernox, texas_road)
    bob_text = "Bob"
    assert sue_agendahub.roles_dir() == f"{sue_agendahub.econ_dir()}/roles"
    assert sue_agendahub.jobs_dir() == f"{sue_agendahub.econ_dir()}/jobs"
    sue_roles_dir = sue_agendahub.roles_dir()
    assert sue_agendahub.role_path(bob_text) == f"{sue_roles_dir}/{bob_text}.json"
    sue_jobs_dir = sue_agendahub.jobs_dir()
    assert sue_agendahub.job_path(bob_text) == f"{sue_jobs_dir}/{bob_text}.json"


def test_AgendaHub_save_file_role_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_agendahub = agendahub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    assert os_path_exists(sue_agendahub.role_path(bob_text)) == False

    # WHEN
    sue_agendahub.save_file_role(bob_agenda)

    # THEN
    assert os_path_exists(sue_agendahub.role_path(bob_text))


def test_AgendaHub_role_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_agendahub = agendahub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    assert sue_agendahub.role_file_exists(bob_text) == False

    # WHEN
    sue_agendahub.save_file_role(bob_agenda)

    # THEN
    assert sue_agendahub.role_file_exists(bob_text)


def test_AgendaHub_get_role_agenda_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_agendahub = agendahub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    sue_agendahub.save_file_role(bob_agenda)

    # WHEN / THEN
    assert sue_agendahub.get_role_agenda(bob_text).get_dict() == bob_agenda.get_dict()


def test_AgendaHub_delete_role_file_DeletesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    texas_agendahub = get_texas_agendahub()
    sue_agenda = get_agenda_with_4_levels()
    sue_text = sue_agenda._owner_id
    texas_agendahub.save_file_role(sue_agenda)
    print(f"{texas_agendahub.role_path(sue_text)=}")
    role_path = texas_agendahub.role_path(sue_text)
    assert os_path_exists(role_path)

    # WHEN
    texas_agendahub.delete_role_file(sue_text)

    # THEN
    assert os_path_exists(role_path) == False


def test_AgendaHub_save_file_job_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_agendahub = agendahub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    assert os_path_exists(sue_agendahub.job_path(bob_text)) == False

    # WHEN
    sue_agendahub.save_file_job(bob_agenda)

    # THEN
    assert os_path_exists(sue_agendahub.job_path(bob_text))


def test_AgendaHub_job_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_agendahub = agendahub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    assert sue_agendahub.job_file_exists(bob_text) == False

    # WHEN
    sue_agendahub.save_file_job(bob_agenda)

    # THEN
    assert sue_agendahub.job_file_exists(bob_text)


def test_AgendaHub_get_job_agenda_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    nation_text = "nation-state"
    nation_road = create_road(root_label(), nation_text)
    usa_text = "USA"
    usa_road = create_road(nation_road, usa_text)
    texas_text = "Texas"
    texas_road = create_road(usa_road, texas_text)
    temp_env_dir = get_change_temp_env_dir()
    sue_agendahub = agendahub_shop(temp_env_dir, None, sue_text, texas_road)
    bob_text = "Bob"
    bob_agenda = get_agenda_with_4_levels()
    bob_agenda.set_owner_id(bob_text)
    sue_agendahub.save_file_job(bob_agenda)

    # WHEN / THEN
    assert sue_agendahub.get_job_agenda(bob_text).get_dict() == bob_agenda.get_dict()


def test_AgendaHub_delete_job_file_DeletesAgendaFile(env_dir_setup_cleanup):
    # GIVEN
    texas_agendahub = get_texas_agendahub()
    sue_agenda = get_agenda_with_4_levels()
    sue_text = sue_agenda._owner_id
    texas_agendahub.save_file_job(sue_agenda)
    print(f"{texas_agendahub.job_path(sue_text)=}")
    job_path = texas_agendahub.job_path(sue_text)
    assert os_path_exists(job_path)

    # WHEN
    texas_agendahub.delete_job_file(sue_text)

    # THEN
    assert os_path_exists(job_path) == False
