from src.agenda.agenda import agendaunit_shop
from src.agenda.x_func import delete_dir as x_func_delete_dir
from src.culture.council import councilunit_shop, CouncilUnit
from src.culture.examples.council_env_kit import (
    council_dir_setup_cleanup,
    get_temp_councilunit_dir,
    get_temp_culture_title,
)
from os import path as os_path


def test_CouncilUnit_exists(council_dir_setup_cleanup):
    # GIVEN / WHEN
    x_council = CouncilUnit()

    # GIVEN
    assert x_council._admin is None
    assert x_council._seed is None


def test_councilunit_shop_exists(council_dir_setup_cleanup):
    # GIVEN
    x_pid = "test1"

    # WHEN
    x_council = councilunit_shop(
        pid=x_pid,
        env_dir=get_temp_councilunit_dir(),
        culture_title=get_temp_culture_title(),
    )

    # GIVEN
    assert x_council._admin._council_cid != None
    assert x_council._admin._culture_title != None
    assert x_council._admin._culture_title == get_temp_culture_title()
    assert x_council._seed is None


def test_councilunit_auto_output_to_public_SavesAgendaToPublicDirWhenTrue(
    council_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_councilunit_dir()
    x_title = get_temp_culture_title()
    tim_text = "Tim"
    public_file_name = f"{tim_text}.json"
    public_file_path = f"{get_temp_councilunit_dir()}/agendas/{public_file_name}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/culture/examples/ex_env/agendas/{public_file_name}"
    x_council = councilunit_shop(
        tim_text, env_dir, x_title, _auto_output_to_public=True
    )
    x_council.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    tim_agenda = agendaunit_shop(_healer=tim_text)
    tim_agenda.set_culture_title(x_title)
    x_council.set_depot_agenda(tim_agenda, "blind_trust")

    # THEN
    assert os_path.exists(public_file_path)


def test_councilunit_auto_output_to_public_DoesNotSaveAgendaToPublicDirWhenFalse(
    council_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_councilunit_dir()
    x_title = get_temp_culture_title()
    tim_text = "Tim"
    public_file_name = f"{tim_text}.json"
    public_file_path = f"{get_temp_councilunit_dir()}/agendas/{public_file_name}"
    print(f"{public_file_path=}")
    # public_file_path = f"src/culture/examples/ex_env/agendas/{public_file_name}"
    x_council = councilunit_shop(tim_text, env_dir, x_title, False)
    x_council.create_core_dir_and_files()
    assert os_path.exists(public_file_path) is False

    # WHEN
    x_council.set_depot_agenda(agendaunit_shop(tim_text), depotlink_type="blind_trust")

    # THEN
    assert os_path.exists(public_file_path) is False


def test_councilunit_get_seed_createsEmptyAgendaWhenFileDoesNotExist(
    council_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_council = councilunit_shop(
        tim_text, get_temp_councilunit_dir(), get_temp_culture_title()
    )
    tim_council.create_core_dir_and_files()
    assert os_path.exists(tim_council._admin._seed_file_path)
    x_func_delete_dir(dir=tim_council._admin._seed_file_path)
    assert os_path.exists(tim_council._admin._seed_file_path) is False
    assert tim_council._seed is None

    # WHEN
    seed_agenda = tim_council.get_seed()

    # THEN
    assert os_path.exists(tim_council._admin._seed_file_path)
    assert tim_council._seed != None


def test_councilunit_get_seed_getsMemoryAgendaIfExists(
    council_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_council = councilunit_shop(
        tim_text, get_temp_councilunit_dir(), get_temp_culture_title()
    )
    tim_council.create_core_dir_and_files()
    seed_file_path = (
        f"{tim_council._admin._councilunit_dir}/{tim_council._admin._seed_file_name}"
    )
    seed_agenda1 = tim_council.get_seed()
    assert os_path.exists(seed_file_path)
    assert tim_council._seed != None

    # WHEN
    ray_text = "Ray"
    tim_council._seed = agendaunit_shop(_healer=ray_text)
    seed_agenda2 = tim_council.get_seed()

    # THEN
    assert seed_agenda2._healer == ray_text
    assert seed_agenda2 != seed_agenda1

    # WHEN
    tim_council._seed = None
    seed_agenda3 = tim_council.get_seed()

    # THEN
    assert seed_agenda3._healer != ray_text
    assert seed_agenda3 == seed_agenda1


def test_councilunit_set_seed_savesseedAgendaSet_seed_None(
    council_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_council = councilunit_shop(
        tim_text, get_temp_councilunit_dir(), get_temp_culture_title()
    )
    tim_council.create_core_dir_and_files()
    seed_file_path = (
        f"{tim_council._admin._councilunit_dir}/{tim_council._admin._seed_file_name}"
    )
    seed_agenda1 = tim_council.get_seed()
    assert os_path.exists(seed_file_path)
    assert tim_council._seed != None

    # WHEN
    uid_text = "Not a real uid"
    tim_council._seed._idearoot._uid = uid_text
    tim_council.set_seed()

    # THEN
    assert os_path.exists(seed_file_path)
    assert tim_council._seed is None
    seed_agenda2 = tim_council.get_seed()
    assert seed_agenda2._idearoot._uid == uid_text


def test_councilunit_set_seed_savesGivenAgendaSet_seed_None(
    council_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_council = councilunit_shop(
        tim_text, get_temp_councilunit_dir(), get_temp_culture_title()
    )
    tim_council.create_core_dir_and_files()
    seed_file_path = (
        f"{tim_council._admin._councilunit_dir}/{tim_council._admin._seed_file_name}"
    )
    seed_agenda1 = tim_council.get_seed()
    assert os_path.exists(seed_file_path)
    assert tim_council._seed != None

    # WHEN
    seed_uid_text = "this is ._seed uid"
    tim_council._seed._idearoot._uid = seed_uid_text

    new_agenda = agendaunit_shop(_healer=tim_text)
    new_agenda_uid_text = "this is pulled AgendaUnit uid"
    new_agenda._idearoot._uid = new_agenda_uid_text

    tim_council.set_seed(new_agenda)

    # THEN
    assert os_path.exists(seed_file_path)
    assert tim_council._seed is None
    assert tim_council.get_seed()._idearoot._uid != seed_uid_text
    assert tim_council.get_seed()._idearoot._uid == new_agenda_uid_text

    # GIVEN
    tim_council.set_seed(new_agenda)
    assert os_path.exists(seed_file_path)
    assert tim_council._seed is None

    # WHEN
    tim_council.set_seed_if_empty()

    # THEN
    assert tim_council._seed != None
    assert os_path.exists(seed_file_path)

    # WHEN
    seed_uid_text = "this is ._seed uid"
    tim_council._seed._idearoot._uid = seed_uid_text


def test_councilunit_set_seed_if_emtpy_DoesNotReplace_seed(
    council_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    tim_council = councilunit_shop(
        tim_text, get_temp_councilunit_dir(), get_temp_culture_title()
    )
    tim_council.create_core_dir_and_files()
    saved_agenda = agendaunit_shop(_healer=tim_text)
    saved_agenda_uid_text = "this is pulled AgendaUnit uid"
    saved_agenda._idearoot._uid = saved_agenda_uid_text
    tim_council.set_seed(saved_agenda)
    tim_council.get_seed()
    assert tim_council._seed != None

    # WHEN
    seed_uid_text = "this is ._seed uid"
    tim_council._seed._idearoot._uid = seed_uid_text
    tim_council.set_seed_if_empty()

    # THEN
    assert tim_council._seed != None
    assert tim_council._seed._idearoot._uid == seed_uid_text
    assert tim_council._seed._idearoot._uid != saved_agenda_uid_text
