from src._road.road import default_road_delimiter_if_none
from src.agenda.party import partylink_shop
from src.agenda.group import groupunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.instrument.file import delete_dir
from src.econ.clerk import (
    clerkunit_shop,
    ClerkUnit,
    save_file_to_guts,
    save_file_to_jobs,
    get_owner_file_name,
)
from src.econ.econ import get_econ_jobs_dir, get_econ_guts_dir
from src.econ.examples.econ_env_kit import (
    env_dir_setup_cleanup,
    get_test_econ_dir,
    get_temp_env_world_id,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_ClerkUnit_exists():
    # GIVEN / WHEN
    x_clerk = ClerkUnit()

    # GIVEN
    assert x_clerk != None
    assert x_clerk._clerk_id is None
    assert x_clerk._econ_dir is None
    assert x_clerk._guts_dir is None
    assert x_clerk._jobs_dir is None
    assert x_clerk._role_file_path is None
    # assert x_clerk._road_delimiter is None
    assert x_clerk._role is None
    assert x_clerk._job is None
    assert x_clerk._roll is None


def test_ClerkUnit_set_clerk_id_SetsArribute():
    # GIVEN
    x_clerk = ClerkUnit()
    assert x_clerk._clerk_id is None

    # WHEN
    tim_text = "Tim"
    x_clerk.set_clerk_id(tim_text)

    # THEN
    assert x_clerk._clerk_id == tim_text


def test_ClerkUnit_set_econ_dir_SetsArribute():
    # GIVEN
    x_clerk = ClerkUnit()
    assert x_clerk._econ_dir is None

    # WHEN
    x_dir = get_test_econ_dir()
    x_clerk.set_econ_dir(x_dir)

    # THEN
    assert x_clerk._econ_dir == x_dir


# def test_ClerkUnit_set_road_delimiter_SetsArribute():
#     # GIVEN
#     x_clerk = ClerkUnit()
#     assert x_clerk._road_delimiter is None

#     # WHEN
#     slash_text = "/"
#     x_clerk.set_road_delimiter(slash_text)

#     # THEN
#     assert x_clerk._road_delimiter == slash_text


def test_ClerkUnit_set_clerkunit_dirs_SetsArributes():
    # GIVEN
    x_clerk = ClerkUnit()
    tim_text = "Tim"
    x_clerk.set_clerk_id(tim_text)
    x_dir = get_test_econ_dir()
    x_clerk.set_econ_dir(x_dir)

    # WHEN
    x_clerk._set_clerkunit_dirs()

    # THEN
    assert x_clerk._guts_dir == get_econ_guts_dir(x_dir)
    assert x_clerk._jobs_dir == get_econ_jobs_dir(x_dir)


def test_clerkunit_shop_DoesNotCreateJob(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"

    # WHEN
    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir(), create_job=False)

    # GIVEN
    assert yao_clerk._clerk_id != None
    assert yao_clerk._clerk_id == yao_text
    assert yao_clerk._econ_dir == get_test_econ_dir()
    assert yao_clerk._role is None
    assert yao_clerk._roll == []
    assert yao_clerk._job is None


def test_ClerkUnit_set_role_SetsArributesWhenFileExists(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    save_file_to_guts(get_test_econ_dir(), yao_agenda)
    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir(), create_job=False)
    assert yao_clerk._role is None

    # WHEN
    yao_clerk._set_role()

    # THEN
    assert yao_clerk._role.get_dict() == yao_agenda.get_dict()


def test_ClerkUnit_set_role_SetsArributesWhenFileDoesNotExist(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir(), create_job=False)
    assert yao_clerk._role is None

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        yao_clerk._set_role()
    assert (
        str(excinfo.value)
        == f"Role agenda file '{get_owner_file_name(yao_text)}' does not exist."
    )


def test_ClerkUnit_set_roll_SetsArribute(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    yao_agenda.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_agenda.set_agenda_metrics()
    save_file_to_guts(get_test_econ_dir(), yao_agenda)
    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir(), create_job=False)
    yao_clerk._set_role()
    assert yao_clerk._roll == []

    # WHEN
    yao_clerk._set_roll()

    # THEN
    assert yao_clerk._roll != [(zia_text, zia_creditor_weight)]
    assert yao_clerk._roll == [(zia_text, zia_debtor_weight)]


def test_ClerkUnit_set_empty_job_SetsArributeEmptyAgendaUnit(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    slash_text = "/"
    yao_agenda = agendaunit_shop(yao_text, _road_delimiter=slash_text)
    yao_agenda.add_l1_idea(ideaunit_shop("Texas"))
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    zia_creditor_pool = 87
    zia_debtor_pool = 81
    yao_agenda.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    swim_group = groupunit_shop(f"{slash_text}swimmers", _road_delimiter=slash_text)
    swim_group.set_partylink(partylink_shop(zia_text))
    yao_agenda.set_groupunit(swim_group)
    yao_agenda.set_party_creditor_pool(zia_creditor_pool, True)
    yao_agenda.set_party_debtor_pool(zia_debtor_pool, True)
    save_file_to_guts(get_test_econ_dir(), yao_agenda)
    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir(), create_job=False)
    yao_clerk._set_role()
    assert yao_clerk._roll == []

    # WHEN
    yao_clerk._set_empty_job()

    # THEN
    assert yao_clerk._job._owner_id == yao_agenda._owner_id
    assert yao_clerk._job._world_id == yao_agenda._world_id
    assert yao_clerk._job._last_gift_id == yao_agenda._last_gift_id
    assert yao_clerk._job.get_partys_dict() == yao_agenda.get_partys_dict()
    assert yao_clerk._job.get_groupunits_dict() == yao_agenda.get_groupunits_dict()
    assert yao_clerk._job._road_delimiter == yao_agenda._road_delimiter
    assert yao_clerk._job._planck == yao_agenda._planck
    assert yao_clerk._job._money_desc == yao_agenda._money_desc
    assert yao_clerk._job._party_creditor_pool == yao_agenda._party_creditor_pool
    assert yao_clerk._job._party_debtor_pool == yao_agenda._party_debtor_pool
    yao_clerk._job.set_agenda_metrics()
    assert len(yao_clerk._job._idea_dict) != len(yao_agenda._idea_dict)
    assert len(yao_clerk._job._idea_dict) == 1


def test_clerkunit_shop_CreatesEmptyJob(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.set_agenda_metrics()
    save_file_to_guts(get_test_econ_dir(), yao_agenda)

    # WHEN
    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir())

    # GIVEN
    assert yao_clerk._clerk_id != None
    assert yao_clerk._clerk_id == yao_text
    assert yao_clerk._econ_dir == get_test_econ_dir()
    assert yao_clerk._role._idea_dict == yao_agenda._idea_dict
    assert yao_clerk._role == yao_agenda
    assert yao_clerk._roll == []
    assert yao_clerk._job.get_dict() == yao_agenda.get_dict()


# # def test_clerkunit_auto_output_job_to_jobs_SavesAgendaTojobsDirWhenTrue(
# #     env_dir_setup_cleanup,
# # ):
# #     # GIVEN
# #     env_dir = get_temp_clerkunit_dir()
# #     x_world_id = get_temp_econ_id()
# #     tim_text = "Tim"
# #     tim_agenda = agendaunit_shop(tim_text, x_world_id, _auto_output_job_to_jobs=True)
# #     jobs_text = "jobs"
# #     jobs_file_name = f"{tim_agenda._owner_id}.json"
# #     jobs_file_path = f"{get_temp_clerkunit_dir()}/{jobs_text}/{jobs_file_name}"
# #     print(f"{jobs_file_path=}")
# #     # jobs_file_path = f"src/econ/examples/ex_env/agendas/{jobs_file_name}"
# #     x_clerk = clerkunit_shop(tim_text, env_dir, x_econ_id)
# #     x_clerk.create_core_dir_and_files()
# #     assert os_path.exists(jobs_file_path) is False

# #     # WHEN
# #     x_clerk._set_depot_agenda(tim_agenda)

# #     # THEN
# #     assert os_path.exists(jobs_file_path)


# # def test_clerkunit_auto_output_job_to_jobs_DoesNotSaveAgendaTojobsDirWhenFalse(
# #     env_dir_setup_cleanup,
# # ):
# #     # GIVEN
# #     env_dir = get_temp_clerkunit_dir()
# #     x_econ_id = get_temp_econ_id()
# #     tim_text = "Tim"
# #     jobs_file_name = f"{tim_text}.json"
# #     jobs_file_path = f"{get_temp_clerkunit_dir()}/agendas/{jobs_file_name}"
# #     print(f"{jobs_file_path=}")
# #     # jobs_file_path = f"src/econ/examples/ex_env/agendas/{jobs_file_name}"
# #     x_clerk = clerkunit_shop(tim_text, env_dir, x_econ_id, False)
# #     x_clerk.create_core_dir_and_files()
# #     assert os_path.exists(jobs_file_path) is False

# #     # WHEN
# #     x_clerk._set_depot_agenda(agendaunit_shop(tim_text))

# #     # THEN
# #     assert os_path.exists(jobs_file_path) is False


# def test_clerkunit_get_role_createsEmptyAgendaWhenFileDoesNotExist(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     slash_text = "/"
#     tim_clerk = ClerkUnit(
#         _clerk_id="Tim",
#         _econ_dir=get_temp_clerkunit_dir(),
#         _econ_id=get_temp_econ_id(),
#         _road_delimiter=slash_text,
#     )
#     tim_clerk.set_econ_dir(
#         env_dir=get_temp_clerkunit_dir(),
#         clerk_id="Tim",
#         econ_id=get_temp_econ_id(),
#         _road_delimiter=default_road_delimiter_if_none(slash_text),
#     )
#     tim_clerk.set_clerkunit_dirs()
#     tim_clerk.create_core_dir_and_files()
#     assert os_path.exists(tim_clerk._role_file_path)
#     delete_dir(dir=tim_clerk._role_file_path)
#     assert os_path.exists(tim_clerk._role_file_path) is False
#     assert tim_clerk._role is None

#     # WHEN
#     role_agenda = tim_clerk.get_role()

#     # THEN
#     assert os_path.exists(tim_clerk._role_file_path)
#     assert tim_clerk._role != None
#     assert role_agenda._road_delimiter != None
#     assert role_agenda._road_delimiter == slash_text


# def test_clerkunit_get_role_getsMemoryAgendaIfExists(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     tim_text = "Tim"
#     tim_clerk = clerkunit_shop(tim_text, get_temp_clerkunit_dir(), get_temp_econ_id())
#     tim_clerk.create_core_dir_and_files()
#     role_file_path = f"{tim_clerk._clerkunit_dir}/{tim_clerk._role_file_name}"
#     role_agenda1 = tim_clerk.get_role()
#     assert os_path.exists(role_file_path)
#     assert tim_clerk._role != None

#     # WHEN
#     ray_text = "Ray"
#     tim_clerk._role = agendaunit_shop(_owner_id=ray_text)
#     role_agenda2 = tim_clerk.get_role()

#     # THEN
#     assert role_agenda2._owner_id == ray_text
#     assert role_agenda2 != role_agenda1

#     # WHEN
#     tim_clerk._role = None
#     role_agenda3 = tim_clerk.get_role()

#     # THEN
#     assert role_agenda3._owner_id != ray_text
#     assert role_agenda3 == role_agenda1


# def test_clerkunit_set_role_savesroleAgendaSet_role_None(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     tim_text = "Tim"
#     tim_clerk = clerkunit_shop(tim_text, get_temp_clerkunit_dir(), get_temp_econ_id())
#     tim_clerk.create_core_dir_and_files()
#     role_file_path = f"{tim_clerk._clerkunit_dir}/{tim_clerk._role_file_name}"
#     role_agenda1 = tim_clerk.get_role()
#     assert os_path.exists(role_file_path)
#     assert tim_clerk._role != None

#     # WHEN
#     uid_text = "Not a actual uid"
#     tim_clerk._role._idearoot._uid = uid_text
#     tim_clerk.set_role()

#     # THEN
#     assert os_path.exists(role_file_path)
#     assert tim_clerk._role is None
#     role_agenda2 = tim_clerk.get_role()
#     assert role_agenda2._idearoot._uid == uid_text


# def test_clerkunit_set_role_savesGivenAgendaSet_role_None(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     tim_text = "Tim"
#     tim_clerk = clerkunit_shop(tim_text, get_temp_clerkunit_dir(), get_temp_econ_id())
#     tim_clerk.create_core_dir_and_files()
#     role_file_path = f"{tim_clerk._clerkunit_dir}/{tim_clerk._role_file_name}"
#     role_agenda1 = tim_clerk.get_role()
#     assert os_path.exists(role_file_path)
#     assert tim_clerk._role != None

#     # WHEN
#     role_uid_text = "this is ._role uid"
#     tim_clerk._role._idearoot._uid = role_uid_text

#     new_agenda = agendaunit_shop(_owner_id=tim_text)
#     new_agenda_uid_text = "this is pulled AgendaUnit uid"
#     new_agenda._idearoot._uid = new_agenda_uid_text

#     tim_clerk.set_role(new_agenda)

#     # THEN
#     assert os_path.exists(role_file_path)
#     assert tim_clerk._role is None
#     assert tim_clerk.get_role()._idearoot._uid != role_uid_text
#     assert tim_clerk.get_role()._idearoot._uid == new_agenda_uid_text

#     # GIVEN
#     tim_clerk.set_role(new_agenda)
#     assert os_path.exists(role_file_path)
#     assert tim_clerk._role is None

#     # WHEN
#     tim_clerk.set_role_if_empty()

#     # THEN
#     assert tim_clerk._role != None
#     assert os_path.exists(role_file_path)

#     # WHEN
#     role_uid_text = "this is ._role uid"
#     tim_clerk._role._idearoot._uid = role_uid_text


# def test_clerkunit_set_role_if_emtpy_DoesNotReplace_role(
#     env_dir_setup_cleanup,
# ):
#     # GIVEN
#     tim_text = "Tim"
#     tim_clerk = clerkunit_shop(tim_text, get_temp_clerkunit_dir(), get_temp_econ_id())
#     tim_clerk.create_core_dir_and_files()
#     saved_agenda = agendaunit_shop(_owner_id=tim_text)
#     saved_agenda_uid_text = "this is pulled AgendaUnit uid"
#     saved_agenda._idearoot._uid = saved_agenda_uid_text
#     tim_clerk.set_role(saved_agenda)
#     tim_clerk.get_role()
#     assert tim_clerk._role != None

#     # WHEN
#     role_uid_text = "this is ._role uid"
#     tim_clerk._role._idearoot._uid = role_uid_text
#     tim_clerk.set_role_if_empty()

#     # THEN
#     assert tim_clerk._role != None
#     assert tim_clerk._role._idearoot._uid == role_uid_text
#     assert tim_clerk._role._idearoot._uid != saved_agenda_uid_text
