from src.agenda.party import partylink_shop
from src.agenda.group import groupunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.econ.job_creator import (
    save_role_file,
    save_job_file,
    get_owner_file_name,
    get_job_file,
    _get_empty_job,
    get_role_file,
    _get_roll,
    _listen_to_roll,
    create_job_file_from_role_file,
)
from src.econ.econ import get_econ_jobs_dir, get_econ_roles_dir
from src.econ.examples.econ_env_kit import (
    env_dir_setup_cleanup,
    get_test_econ_dir,
    get_temp_env_real_id,
)
from os.path import exists as os_path_exists


def test_get_role_file_ReturnsCorrectAgendaWhenFileExists(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    save_role_file(get_test_econ_dir(), yao_role)

    # WHEN
    yao_role = get_role_file(get_test_econ_dir(), yao_text)

    # THEN
    assert yao_role.get_dict() == yao_role.get_dict()


def test_get_roll_ReturnsObj():
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_role.set_agenda_metrics()

    # WHEN
    yao_roll = _get_roll(yao_role)

    # THEN
    zia_partyunit = yao_role.get_party(zia_text)
    assert yao_roll == {zia_text: zia_partyunit}


def test_get_roll_ReturnsObjIgnoresZero_debtor_weight():
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    wei_text = "Wei"
    wei_creditor_weight = 67
    wei_debtor_weight = 0
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_role.add_partyunit(wei_text, wei_creditor_weight, wei_debtor_weight)
    yao_role.set_agenda_metrics()

    # WHEN
    yao_roll = _get_roll(yao_role)

    # THEN
    zia_partyunit = yao_role.get_party(zia_text)
    assert yao_roll == {zia_text: zia_partyunit}


def test_get_empty_job_ReturnsEmptyAgendaUnit():
    # GIVEN
    yao_text = "Yao"
    slash_text = "/"
    yao_role = agendaunit_shop(yao_text, _road_delimiter=slash_text)
    yao_role.add_l1_idea(ideaunit_shop("Texas"))
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    zia_creditor_pool = 87
    zia_debtor_pool = 81
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    swim_group = groupunit_shop(f"{slash_text}swimmers", _road_delimiter=slash_text)
    swim_group.set_partylink(partylink_shop(zia_text))
    yao_role.set_groupunit(swim_group)
    yao_role.set_party_creditor_pool(zia_creditor_pool, True)
    yao_role.set_party_debtor_pool(zia_debtor_pool, True)

    # WHEN
    yao_empty_job = _get_empty_job(yao_role)

    # THEN
    assert yao_empty_job._owner_id == yao_role._owner_id
    assert yao_empty_job._real_id == yao_role._real_id
    assert yao_empty_job._last_gift_id == yao_role._last_gift_id
    assert yao_empty_job.get_partys_dict() == yao_role.get_partys_dict()
    assert yao_empty_job.get_groupunits_dict() == yao_role.get_groupunits_dict()
    assert yao_empty_job._road_delimiter == yao_role._road_delimiter
    assert yao_empty_job._planck == yao_role._planck
    assert yao_empty_job._money_desc == yao_role._money_desc
    assert yao_empty_job._party_creditor_pool == yao_role._party_creditor_pool
    assert yao_empty_job._party_debtor_pool == yao_role._party_debtor_pool
    yao_empty_job.set_agenda_metrics()
    assert len(yao_empty_job._idea_dict) != len(yao_role._idea_dict)
    assert len(yao_empty_job._idea_dict) == 1


def test_listen_to_roll_AddsTasksToJobAgenda(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_role.set_party_pool(zia_pool)

    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    clean_road = zia_agendaunit.make_l1_road(clean_text)
    cook_road = zia_agendaunit.make_l1_road(cook_text)
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, pledge=True))
    zia_agendaunit.add_l1_idea(ideaunit_shop(cook_text, _weight=3, pledge=True))
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_agendaunit.get_idea_obj(cook_road)
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    save_job_file(get_test_econ_dir(), zia_agendaunit)

    before_yao_job = _get_empty_job(yao_role)
    assert len(before_yao_job.get_intent_dict()) == 0

    # WHEN
    yao_job = _listen_to_roll(get_test_econ_dir(), yao_role)

    # THEN
    assert len(yao_job.get_intent_dict()) == 2


def test_listen_to_roll_IgnoresIrrationalAgenda(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_creditor_weight = 57
    sue_debtor_weight = 51
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_role.add_partyunit(sue_text, sue_creditor_weight, sue_debtor_weight)
    yao_pool = 87
    yao_role.set_party_pool(yao_pool)
    save_role_file(get_test_econ_dir(), yao_role)

    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    clean_road = zia_agendaunit.make_l1_road(clean_text)
    cook_road = zia_agendaunit.make_l1_road(cook_text)
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, pledge=True))
    zia_agendaunit.add_l1_idea(ideaunit_shop(cook_text, _weight=3, pledge=True))
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_agendaunit.get_idea_obj(cook_road)
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    save_job_file(get_test_econ_dir(), zia_agendaunit)

    sue_agendaunit = agendaunit_shop(sue_text)
    sue_agendaunit.set_max_tree_traverse(5)
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    vaccum_text = "Vaccum"
    vaccum_road = sue_agendaunit.make_l1_road(vaccum_text)
    sue_agendaunit.add_l1_idea(ideaunit_shop(vaccum_text, pledge=True))
    vaccum_ideaunit = sue_agendaunit.get_idea_obj(vaccum_road)
    vaccum_ideaunit._assignedunit.set_suffgroup(yao_text)

    egg_text = "egg first"
    egg_road = sue_agendaunit.make_l1_road(egg_text)
    sue_agendaunit.add_l1_idea(ideaunit_shop(egg_text))
    chicken_text = "chicken first"
    chicken_road = sue_agendaunit.make_l1_road(chicken_text)
    sue_agendaunit.add_l1_idea(ideaunit_shop(chicken_text))
    # set egg pledge is True when chicken first is False
    sue_agendaunit.edit_idea_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_suff_idea_active=True,
    )
    # set chick pledge is True when egg first is False
    sue_agendaunit.edit_idea_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_suff_idea_active=False,
    )
    save_job_file(get_test_econ_dir(), sue_agendaunit)

    # WHEN
    yao_job = _listen_to_roll(get_test_econ_dir(), yao_role)

    # THEN irrational agenda is ignored
    assert len(yao_job.get_intent_dict()) != 3
    assert len(yao_job.get_intent_dict()) == 2


def test_listen_to_roll_ListensToOwner_role_AndNotOwner_job(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    yao_text = "Yao"
    yao_creditor_weight = 57
    yao_debtor_weight = 51
    yao_role.add_partyunit(yao_text, yao_creditor_weight, yao_debtor_weight)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    yao_role.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_pool = 87
    yao_role.set_party_pool(yao_pool)
    # save yao without task to roles
    save_role_file(get_test_econ_dir(), yao_role)

    # Save Zia to jobs
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    clean_text = "clean"
    cook_text = "cook"
    clean_road = zia_agendaunit.make_l1_road(clean_text)
    cook_road = zia_agendaunit.make_l1_road(cook_text)
    zia_agendaunit.add_l1_idea(ideaunit_shop(clean_text, pledge=True))
    zia_agendaunit.add_l1_idea(ideaunit_shop(cook_text, _weight=3, pledge=True))
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road)
    cook_ideaunit = zia_agendaunit.get_idea_obj(cook_road)
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    save_job_file(get_test_econ_dir(), zia_agendaunit)

    # save yao with task to roles
    yao_job = agendaunit_shop(yao_text)
    vaccum_text = "Vaccum"
    vaccum_road = yao_job.make_l1_road(vaccum_text)
    yao_job.add_l1_idea(ideaunit_shop(vaccum_text, pledge=True))
    vaccum_ideaunit = yao_job.get_idea_obj(vaccum_road)
    vaccum_ideaunit._assignedunit.set_suffgroup(yao_text)
    save_job_file(get_test_econ_dir(), yao_job)

    # WHEN
    yao_job = _listen_to_roll(get_test_econ_dir(), yao_role)

    # THEN irrational agenda is ignored
    assert len(yao_job.get_intent_dict()) != 3
    print(f"{yao_job.get_intent_dict().keys()=}")
    assert len(yao_job.get_intent_dict()) == 2


def test_create_job_file_from_role_file_CreatesEmptyJob(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    yao_role.set_agenda_metrics()
    save_role_file(get_test_econ_dir(), yao_role)
    yao_job_file_path = f"{get_test_econ_dir()}/jobs/{get_owner_file_name(yao_text)}"
    assert os_path_exists(yao_job_file_path) == False

    # WHEN
    yao_job = create_job_file_from_role_file(get_test_econ_dir(), yao_text)

    # GIVEN
    assert yao_job._owner_id != None
    assert yao_job._owner_id == yao_text
    assert yao_job.get_dict() == yao_role.get_dict()
    assert os_path_exists(yao_job_file_path)
