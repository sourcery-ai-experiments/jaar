from src._road.road import (
    default_road_delimiter_if_none,
    create_road_from_nodes,
    create_road,
    get_default_real_id_roadnode as root_label,
)
from src._road.finance import default_planck_if_none, default_penny_if_none
from src._road.jaar_config import (
    get_atoms_folder,
    get_test_reals_dir,
    get_test_real_id,
    get_rootpart_of_econ_dir,
)
from src.agenda.agenda import agendaunit_shop
from src.listen.filehub import FileHub, filehub_shop, get_econ_path, get_nox_type_set
from src.listen.examples.examples import get_agenda_with_4_levels
from src.listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
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
    assert x_filehub.penny is None


def test_filehub_shop_ReturnsCorrectObj():
    # GIVEN
    x_reals_dir = "src/real/examples"
    x_real_id = "music"
    sue_text = "Sue"
    x_road_delimiter = "/"
    x_planck = 3
    x_penny = 0.3

    # WHEN
    x_filehub = filehub_shop(
        x_reals_dir,
        x_real_id,
        sue_text,
        None,
        None,
        x_road_delimiter,
        x_planck,
        penny=x_penny,
    )

    # THEN
    assert x_filehub.reals_dir == x_reals_dir
    assert x_filehub.real_id == x_real_id
    assert x_filehub.person_id == sue_text
    assert x_filehub.road_delimiter == x_road_delimiter
    assert x_filehub.planck == x_planck
    assert x_filehub.penny == x_penny

    assert x_filehub.real_dir() == f"{x_reals_dir}/{x_real_id}"
    assert x_filehub.persons_dir() == f"{x_filehub.real_dir()}/persons"
    assert x_filehub.person_dir() == f"{x_filehub.persons_dir()}/{sue_text}"
    assert x_filehub.econs_dir() == f"{x_filehub.person_dir()}/econs"
    assert x_filehub.quarks_dir() == f"{x_filehub.person_dir()}/quarks"
    assert x_filehub.duty_dir() == f"{x_filehub.person_dir()}/duty"
    assert x_filehub.work_dir() == f"{x_filehub.person_dir()}/work"
    assert x_filehub.atoms_dir() == f"{x_filehub.person_dir()}/{get_atoms_folder()}"
    assert x_filehub.duty_file_name() == f"{sue_text}.json"
    x_duty_file_path = f"{x_filehub.duty_dir()}/{x_filehub.duty_file_name()}"
    assert x_filehub.duty_file_path() == x_duty_file_path
    assert x_filehub.work_file_name() == f"{sue_text}.json"
    x_workpath = f"{x_filehub.work_dir()}/{x_filehub.work_file_name()}"
    assert x_filehub.work_path() == x_workpath


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
    assert sue_filehub.penny == default_penny_if_none()
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


def test_filehub_shop_RaisesErrorIf_person_id_Contains_road_delimiter():
    # GIVEN
    slash_text = "/"
    bob_text = f"Bob{slash_text}Sue"

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        filehub_shop(None, None, person_id=bob_text, road_delimiter=slash_text)
    assert (
        str(excinfo.value)
        == f"'{bob_text}' needs to be a RoadNode. Cannot contain delimiter: '{slash_text}'"
    )


def test_FileHub_save_file_duty_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), None, sue_text)
    assert os_path_exists(sue_filehub.duty_file_path()) is False

    # WHEN
    sue_filehub.save_file_duty(file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_filehub.duty_file_path())


def test_FileHub_duty_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), None, sue_text)
    assert sue_filehub.duty_file_exists() is False

    # WHEN
    sue_filehub.save_file_duty(file_text="fooboo", replace=True)

    # THEN
    assert sue_filehub.duty_file_exists()


def test_FileHub_open_file_duty_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), None, sue_text)
    example_text = "fooboo"
    sue_filehub.save_file_duty(example_text, replace=True)

    # WHEN / THEN
    assert sue_filehub.open_file_duty() == example_text


def test_FileHub_save_file_work_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), None, sue_text)
    assert os_path_exists(sue_filehub.work_path()) is False

    # WHEN
    sue_filehub.save_file_work(file_text="fooboo", replace=True)

    # THEN
    assert os_path_exists(sue_filehub.work_path())


def test_FileHub_work_file_exists_ReturnsCorrectBool(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), None, sue_text)
    assert sue_filehub.work_file_exists() is False

    # WHEN
    sue_filehub.save_file_work(file_text="fooboo", replace=True)

    # THEN
    assert sue_filehub.work_file_exists()


def test_FileHub_open_file_work_OpensFile(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), None, sue_text)
    example_text = "fooboo"
    sue_filehub.save_file_work(example_text, replace=True)

    # WHEN / THEN
    assert sue_filehub.open_file_work() == example_text


def test_FileHub_save_duty_agenda_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_agendaunit = get_agenda_with_4_levels()
    sue_text = sue_agendaunit._owner_id
    real_id = root_label()
    sue_filehub = filehub_shop(env_dir(), real_id, sue_text, None)

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

    real_id = root_label()
    sue_filehub = filehub_shop(env_dir(), real_id, sue_text, None)

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
    sue_filehub = filehub_shop(env_dir(), None, sue_text, texas_road)
    sue_filehub.save_duty_agenda(sue_agendaunit)

    # WHEN / THEN
    assert sue_filehub.get_duty_agenda().get_dict() == sue_agendaunit.get_dict()


def test_FileHub_save_work_agenda_CorrectlySavesFile(env_dir_setup_cleanup):
    # GIVEN
    sue_agendaunit = get_agenda_with_4_levels()
    sue_text = sue_agendaunit._owner_id

    real_id = root_label()
    sue_filehub = filehub_shop(env_dir(), real_id, sue_text, None)

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
    sue_filehub = filehub_shop(env_dir(), None, sue_text, texas_road)
    sue_filehub.save_work_agenda(sue_agendaunit)

    # WHEN / THEN
    assert sue_filehub.get_work_agenda().get_dict() == sue_agendaunit.get_dict()


def test_FileHub_save_work_agenda_RaisesErrorWhenAgenda_work_id_IsWrong(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"

    real_id = root_label()
    sue_filehub = filehub_shop(env_dir(), real_id, sue_text, None)

    # WHEN / THEN
    yao_text = "yao"
    with pytest_raises(Exception) as excinfo:
        sue_filehub.save_work_agenda(agendaunit_shop(yao_text))
    assert (
        str(excinfo.value)
        == f"AgendaUnit with owner_id '{yao_text}' cannot be saved as person_id '{sue_text}''s work agenda."
    )
