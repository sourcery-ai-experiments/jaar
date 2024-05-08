from src._road.road import default_road_delimiter_if_none
from src.agenda.party import partylink_shop
from src.agenda.group import groupunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.instrument.file import dir_files
from src.econ.clerk import (
    clerkunit_shop,
    ClerkUnit,
    save_file_to_roles,
    save_file_to_jobs,
    get_owner_file_name,
)
from src.econ.econ import get_econ_jobs_dir, get_econ_roles_dir
from src.econ.examples.econ_env_kit import (
    env_dir_setup_cleanup,
    get_test_econ_dir,
    get_temp_env_world_id,
)
from os import path as os_path
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_ClerkUnit_exists():
    # GIVEN / WHEN
    x_clerk = ClerkUnit()

    # GIVEN
    assert x_clerk != None
    assert x_clerk._clerk_id is None
    assert x_clerk._econ_dir is None
    assert x_clerk._roles_dir is None
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
    assert x_clerk._roles_dir == get_econ_roles_dir(x_dir)
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
    assert yao_clerk._roll == {}
    assert yao_clerk._job is None


def test_ClerkUnit_set_role_SetsArributesWhenFileExists(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    save_file_to_roles(get_test_econ_dir(), yao_agenda)
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
    save_file_to_roles(get_test_econ_dir(), yao_agenda)
    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir(), create_job=False)
    yao_clerk._set_role()
    assert yao_clerk._roll == {}

    # WHEN
    yao_clerk._set_roll()

    # THEN
    zia_partyunit = yao_agenda.get_party(zia_text)
    assert yao_clerk._roll == {zia_text: zia_partyunit}


def test_ClerkUnit_set_roll_SetsArributeIgnoresZero_debtor_weight(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    wei_text = "Wei"
    wei_creditor_weight = 67
    wei_debtor_weight = 0
    yao_agenda.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_agenda.add_partyunit(wei_text, wei_creditor_weight, wei_debtor_weight)
    yao_agenda.set_agenda_metrics()
    save_file_to_roles(get_test_econ_dir(), yao_agenda)
    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir(), create_job=False)
    yao_clerk._set_role()
    assert yao_clerk._roll == {}

    # WHEN
    yao_clerk._set_roll()

    # THEN
    # assert yao_clerk._roll != {zia_text: zia_partyunit}
    zia_partyunit = yao_agenda.get_party(zia_text)
    assert yao_clerk._roll == {zia_text: zia_partyunit}


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
    save_file_to_roles(get_test_econ_dir(), yao_agenda)
    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir(), create_job=False)
    yao_clerk._set_role()
    assert yao_clerk._job is None

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


def test_ClerkUnit_listen_to_roll_AddsTasksToJobAgenda(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_agendaunit = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_agendaunit.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_agendaunit.set_party_pool(zia_pool)
    save_file_to_roles(get_test_econ_dir(), yao_agendaunit)

    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    clean_road = zia_agendaunit.make_l1_road(clean_text)
    cook_road = zia_agendaunit.make_l1_road(cook_text)
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, promise=True))
    zia_agendaunit.add_l1_idea(ideaunit_shop(cook_text, _weight=3, promise=True))
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_agendaunit.get_idea_obj(cook_road)
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    save_file_to_jobs(get_test_econ_dir(), zia_agendaunit)

    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir(), create_job=False)
    yao_clerk._set_role()
    yao_clerk._set_roll()
    yao_clerk._set_empty_job()
    assert len(yao_clerk._job.get_intent_dict()) == 0

    # WHEN
    yao_clerk._listen_to_roll()

    # THEN
    assert len(yao_clerk._job.get_intent_dict()) == 2


def test_ClerkUnit_listen_to_roll_AddsTasksToJobAgendaWhen_suffgroupIsEmpty(
    env_dir_setup_cleanup,
):
    # GIVEN
    zia_text = "Zia"
    yao_text = "Yao"
    yao_agendaunit = agendaunit_shop(yao_text)
    yao_agendaunit.add_partyunit(zia_text)
    yao_agendaunit.set_party_pool(100)
    save_file_to_roles(get_test_econ_dir(), yao_agendaunit)

    cook_text = "cook"
    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_l1_idea(ideaunit_shop(cook_text, promise=True))
    save_file_to_jobs(get_test_econ_dir(), zia_agendaunit)

    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir(), create_job=False)
    yao_clerk._set_role()
    yao_clerk._set_roll()
    yao_clerk._set_empty_job()
    assert len(yao_clerk._job.get_intent_dict()) == 0

    # WHEN
    yao_clerk._listen_to_roll()

    # THEN
    assert len(yao_clerk._job.get_intent_dict()) == 1


def test_ClerkUnit_listen_to_roll_IgnoresIrrationalAgenda(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_agendaunit = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    sue_text = "Sue"
    yao_agendaunit.add_partyunit(zia_text, 47, 41)
    yao_agendaunit.add_partyunit(sue_text, 57, 51)
    yao_agendaunit.set_party_pool(87)
    save_file_to_roles(get_test_econ_dir(), yao_agendaunit)

    clean_text = "clean"
    cook_text = "cook"
    clean_road = zia_agendaunit.make_l1_road(clean_text)
    cook_road = zia_agendaunit.make_l1_road(cook_text)
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, promise=True))
    zia_agendaunit.add_l1_idea(ideaunit_shop(cook_text, _weight=3, promise=True))
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_agendaunit.get_idea_obj(cook_road)
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    save_file_to_jobs(get_test_econ_dir(), zia_agendaunit)

    sue_agendaunit = agendaunit_shop(sue_text)
    sue_agendaunit.set_max_tree_traverse(5)
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    vaccum_text = "Vaccum"
    vaccum_road = sue_agendaunit.make_l1_road(vaccum_text)
    sue_agendaunit.add_l1_idea(ideaunit_shop(vaccum_text, promise=True))
    vaccum_ideaunit = sue_agendaunit.get_idea_obj(vaccum_road)
    vaccum_ideaunit._assignedunit.set_suffgroup(yao_text)

    egg_text = "egg first"
    egg_road = sue_agendaunit.make_l1_road(egg_text)
    sue_agendaunit.add_l1_idea(ideaunit_shop(egg_text))
    chicken_text = "chicken first"
    chicken_road = sue_agendaunit.make_l1_road(chicken_text)
    sue_agendaunit.add_l1_idea(ideaunit_shop(chicken_text))
    # set egg promise is True when chicken first is False
    sue_agendaunit.edit_idea_attr(
        road=egg_road,
        promise=True,
        reason_base=chicken_road,
        reason_suff_idea_active=True,
    )
    # set chick promise is True when egg first is False
    sue_agendaunit.edit_idea_attr(
        road=chicken_road,
        promise=True,
        reason_base=egg_road,
        reason_suff_idea_active=False,
    )
    save_file_to_jobs(get_test_econ_dir(), sue_agendaunit)

    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir(), create_job=False)
    yao_clerk._set_role()
    yao_clerk._set_roll()
    yao_clerk._set_empty_job()
    # print(f"{yao_clerk._jobs_dir=}")
    # print(f"{dir_files(yao_clerk._jobs_dir).keys()=}")

    assert len(yao_clerk._job.get_intent_dict()) == 0

    # WHEN
    yao_clerk._listen_to_roll()

    # THEN irrational agenda is ignored
    assert len(yao_clerk._job.get_intent_dict()) != 3
    assert len(yao_clerk._job.get_intent_dict()) == 2


def test_ClerkUnit_listen_to_roll_ListensToOwner_role_AndNotOwner_job(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_role_agendaunit = agendaunit_shop(yao_text)
    yao_text = "Yao"
    yao_creditor_weight = 57
    yao_debtor_weight = 51
    yao_role_agendaunit.add_partyunit(yao_text, yao_creditor_weight, yao_debtor_weight)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    yao_role_agendaunit.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_pool = 87
    yao_role_agendaunit.set_party_pool(yao_pool)
    # save yao without task to roles
    save_file_to_roles(get_test_econ_dir(), yao_role_agendaunit)

    # Save Zia to jobs
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    clean_road = zia_agendaunit.make_l1_road(clean_text)
    cook_road = zia_agendaunit.make_l1_road(cook_text)
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, promise=True))
    zia_agendaunit.add_l1_idea(ideaunit_shop(cook_text, _weight=3, promise=True))
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_agendaunit.get_idea_obj(cook_road)
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    save_file_to_jobs(get_test_econ_dir(), zia_agendaunit)

    # save yao with task to roles
    yao_job_agendaunit = agendaunit_shop(yao_text)
    yao_job_agendaunit.set_max_tree_traverse(5)
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    vaccum_text = "Vaccum"
    vaccum_road = yao_job_agendaunit.make_l1_road(vaccum_text)
    yao_job_agendaunit.add_l1_idea(ideaunit_shop(vaccum_text, promise=True))
    vaccum_ideaunit = yao_job_agendaunit.get_idea_obj(vaccum_road)
    vaccum_ideaunit._assignedunit.set_suffgroup(yao_text)
    save_file_to_jobs(get_test_econ_dir(), yao_job_agendaunit)

    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir(), create_job=False)
    yao_clerk._set_role()
    yao_clerk._set_roll()
    yao_clerk._set_empty_job()
    # print(f"{yao_clerk._jobs_dir=}")
    # print(f"{dir_files(yao_clerk._jobs_dir).keys()=}")

    assert len(yao_clerk._job.get_intent_dict()) == 0

    # WHEN
    yao_clerk._listen_to_roll()

    # THEN irrational agenda is ignored
    assert len(yao_clerk._job.get_intent_dict()) != 3
    assert len(yao_clerk._job.get_intent_dict()) == 2


def test_clerkunit_shop_CreatesEmptyJob(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_agenda = agendaunit_shop(yao_text)
    yao_agenda.set_agenda_metrics()
    save_file_to_roles(get_test_econ_dir(), yao_agenda)
    yao_job_file_path = f"{get_test_econ_dir()}/jobs/{get_owner_file_name(yao_text)}"
    assert os_path_exists(yao_job_file_path) == False

    # WHEN
    yao_clerk = clerkunit_shop(yao_text, get_test_econ_dir())

    # GIVEN
    assert yao_clerk._clerk_id != None
    assert yao_clerk._clerk_id == yao_text
    assert yao_clerk._econ_dir == get_test_econ_dir()
    assert yao_clerk._role._idea_dict == yao_agenda._idea_dict
    assert yao_clerk._role == yao_agenda
    assert yao_clerk._roll == {}
    assert yao_clerk._job.get_dict() == yao_agenda.get_dict()
    assert os_path_exists(yao_job_file_path)


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
