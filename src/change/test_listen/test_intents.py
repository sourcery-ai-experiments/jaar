from src._instrument.file import delete_dir
from src._road.worldnox import save_file, get_file_name
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.change.agendahub import agendahub_shop, pipeline_role_job_text as role_job
from src.change.listen import create_listen_basis, listen_to_speakers_intent
from src.change.examples.change_env import (
    get_change_temp_env_dir,
    env_dir_setup_cleanup,
    get_texas_agendahub,
    get_texas_road,
)
from src.change.examples.example_listen import (
    cook_text,
    clean_text,
    run_text,
    casa_road,
    cook_road,
    eat_road,
    hungry_road,
    full_road,
    clean_road,
    run_road,
    get_example_yao_speaker,
    get_example_zia_speaker,
    get_example_bob_speaker,
)
from os.path import exists as os_path_exists


def test_listen_to_speakers_intent_AddsTasksToJobAgendaWhenNo_suffgroupIsSet(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_src_listener = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_src_listener.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_src_listener.set_party_pool(zia_pool)

    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_agendaunit.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    agendahub = agendahub_shop(None, None, yao_text, get_texas_road(), role_job())
    agendahub.save_job_agenda(zia_agendaunit)
    new_agenda = create_listen_basis(yao_src_listener)
    assert len(new_agenda.get_intent_dict()) == 0

    # WHEN
    print(f"{len(new_agenda.get_idea_dict())=}")
    listen_to_speakers_intent(new_agenda, agendahub, yao_src_listener)

    # THEN
    assert len(new_agenda.get_intent_dict()) == 2


def test_listen_to_speakers_intent_AddsTasksToJobAgenda(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_src_listener = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_src_listener.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_src_listener.set_party_pool(zia_pool)

    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_agendaunit.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road())
    cook_ideaunit = zia_agendaunit.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    agendahub = agendahub_shop(None, None, yao_text, get_texas_road(), role_job())
    save_file(agendahub.jobs_dir(), get_file_name(zia_text), zia_agendaunit.get_json())
    # zia_file_path = f"{jobs_dir}/{zia_text}.json"
    # print(f"{os_path_exists(zia_file_path)=}")
    new_agenda = create_listen_basis(yao_src_listener)
    assert len(new_agenda.get_intent_dict()) == 0

    # WHEN
    print(f"{len(new_agenda.get_idea_dict())=}")
    listen_to_speakers_intent(new_agenda, agendahub, yao_src_listener)

    # THEN
    assert len(new_agenda.get_intent_dict()) == 2


def test_listen_to_speakers_intent_AddsTasksToJobAgendaWithDetailsDecidedBy_debtor_weight(
    env_dir_setup_cleanup,
):
    # GIVEN
    zia_speaker = get_example_zia_speaker()
    bob_speaker = get_example_bob_speaker()
    bob_speaker.edit_idea_attr(
        road=cook_road(),
        reason_del_premise_base=eat_road(),
        reason_del_premise_need=hungry_road(),
    )
    bob_cook_ideaunit = bob_speaker.get_idea_obj(cook_road())
    zia_cook_ideaunit = zia_speaker.get_idea_obj(cook_road())
    assert bob_cook_ideaunit != zia_cook_ideaunit
    assert len(zia_cook_ideaunit._reasonunits) == 1
    assert len(bob_cook_ideaunit._reasonunits) == 0
    zia_text = zia_speaker._owner_id
    bob_text = bob_speaker._owner_id
    texas_agendahub = get_texas_agendahub()
    texas_agendahub.save_job_agenda(zia_speaker)
    texas_agendahub.save_job_agenda(bob_speaker)

    yao_src = get_example_yao_speaker()
    new_yao1_agenda = create_listen_basis(yao_src)
    assert new_yao1_agenda.idea_exists(cook_road()) == False

    # WHEN
    listen_to_speakers_intent(new_yao1_agenda, texas_agendahub, yao_src)

    # THEN
    assert new_yao1_agenda.idea_exists(cook_road())
    new_cook_idea = new_yao1_agenda.get_idea_obj(cook_road())
    zia_partyunit = new_yao1_agenda.get_party(zia_text)
    bob_partyunit = new_yao1_agenda.get_party(bob_text)
    assert zia_partyunit.debtor_weight < bob_partyunit.debtor_weight
    assert new_cook_idea.get_reasonunit(eat_road()) is None

    yao_zia_debtor_weight = 15
    yao_bob_debtor_weight = 5
    yao_src.add_partyunit(zia_text, None, yao_zia_debtor_weight)
    yao_src.add_partyunit(bob_text, None, yao_bob_debtor_weight)
    yao_src.set_party_pool(100)
    new_yao2_agenda = create_listen_basis(yao_src)
    assert new_yao2_agenda.idea_exists(cook_road()) == False

    # WHEN
    listen_to_speakers_intent(new_yao2_agenda, texas_agendahub, yao_src)

    # THEN
    assert new_yao2_agenda.idea_exists(cook_road())
    new_cook_idea = new_yao2_agenda.get_idea_obj(cook_road())
    zia_partyunit = new_yao2_agenda.get_party(zia_text)
    bob_partyunit = new_yao2_agenda.get_party(bob_text)
    assert zia_partyunit.debtor_weight > bob_partyunit.debtor_weight
    zia_eat_reasonunit = zia_cook_ideaunit.get_reasonunit(eat_road())
    assert new_cook_idea.get_reasonunit(eat_road()) == zia_eat_reasonunit


def test_listen_to_speakers_intent_ProcessesIrrationalAgenda(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_src_listener = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_creditor_weight = 57
    sue_debtor_weight = 51
    yao_src_listener.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_src_listener.add_partyunit(sue_text, sue_creditor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_src_listener.set_party_pool(yao_pool)
    roles_dir = f"{get_change_temp_env_dir()}/roles"
    save_file(roles_dir, yao_text, yao_src_listener.get_json())

    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_agendaunit.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road())
    cook_ideaunit = zia_agendaunit.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    agendahub = agendahub_shop(None, None, yao_text, get_texas_road(), role_job())
    save_file(agendahub.jobs_dir(), get_file_name(zia_text), zia_agendaunit.get_json())

    sue_agendaunit = agendaunit_shop(sue_text)
    sue_agendaunit.set_max_tree_traverse(5)
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    vacuum_text = "vacuum"
    vacuum_road = sue_agendaunit.make_l1_road(vacuum_text)
    sue_agendaunit.add_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = sue_agendaunit.get_idea_obj(vacuum_road)
    vacuum_ideaunit._assignedunit.set_suffgroup(yao_text)

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
    save_file(agendahub.jobs_dir(), get_file_name(sue_text), sue_agendaunit.get_json())

    # WHEN
    new_agenda = create_listen_basis(yao_src_listener)
    listen_to_speakers_intent(new_agenda, agendahub, yao_src_listener)

    # THEN irrational agenda is ignored
    assert len(new_agenda.get_intent_dict()) != 3
    assert len(new_agenda.get_intent_dict()) == 2
    zia_partyunit = new_agenda.get_party(zia_text)
    sue_partyunit = new_agenda.get_party(sue_text)
    print(f"{sue_partyunit.debtor_weight=}")
    print(f"{sue_partyunit._irrational_debtor_weight=}")
    assert zia_partyunit._irrational_debtor_weight == 0
    assert sue_partyunit._irrational_debtor_weight == 51


def test_listen_to_speakers_intent_ProcessesMissingDebtorJobAgenda(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    agendahub = agendahub_shop(None, None, yao_text, get_texas_road(), role_job())
    sue_file_path = f"{agendahub.jobs_dir()}/Sue.json"
    delete_dir(sue_file_path)  # don't know why I have to do this...
    print(f"{os_path_exists(sue_file_path)=}")
    yao_src_listener = agendaunit_shop(yao_text)
    zia_text = "Zia"
    sue_text = "Sue"
    zia_creditor_weight = 47
    sue_creditor_weight = 57
    zia_debtor_weight = 41
    sue_debtor_weight = 51
    yao_src_listener.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_src_listener.add_partyunit(sue_text, sue_creditor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_src_listener.set_party_pool(yao_pool)
    yao_json = yao_src_listener.get_json()
    save_file(agendahub.roles_dir(), get_file_name(yao_text), yao_json)

    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_agendaunit.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road())
    cook_ideaunit = zia_agendaunit.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    agendahub = agendahub_shop(None, None, yao_text, get_texas_road(), role_job())
    save_file(agendahub.jobs_dir(), get_file_name(zia_text), zia_agendaunit.get_json())

    # WHEN
    new_agenda = create_listen_basis(yao_src_listener)
    listen_to_speakers_intent(new_agenda, agendahub, yao_src_listener)

    # THEN irrational agenda is ignored
    assert len(new_agenda.get_intent_dict()) != 3
    assert len(new_agenda.get_intent_dict()) == 2
    zia_partyunit = new_agenda.get_party(zia_text)
    sue_partyunit = new_agenda.get_party(sue_text)
    print(f"{sue_partyunit.debtor_weight=}")
    print(f"{sue_partyunit._missing_job_debtor_weight=}")
    assert zia_partyunit._missing_job_debtor_weight == 0
    assert sue_partyunit._missing_job_debtor_weight == 51


def test_listen_to_speakers_intent_ListensToOwner_role_AndNotOwner_job(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_src_listener = agendaunit_shop(yao_text)
    yao_text = "Yao"
    yao_creditor_weight = 57
    yao_debtor_weight = 51
    yao_src_listener.add_partyunit(yao_text, yao_creditor_weight, yao_debtor_weight)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    yao_src_listener.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_pool = 87
    yao_src_listener.set_party_pool(yao_pool)
    # save yao without task to roles
    agendahub = agendahub_shop(None, None, yao_text, get_texas_road(), role_job())
    save_file(agendahub.roles_dir(), yao_text, yao_src_listener.get_json())

    # Save Zia to jobs
    zia_text = "Zia"
    zia_agendaunit = agendaunit_shop(zia_text)
    zia_agendaunit.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_agendaunit.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_agendaunit.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_agendaunit.get_idea_obj(clean_road())
    cook_ideaunit = zia_agendaunit.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    agendahub = agendahub_shop(None, None, yao_text, get_texas_road(), role_job())
    save_file(agendahub.jobs_dir(), get_file_name(zia_text), zia_agendaunit.get_json())

    # save yao with task to roles
    yao_job = agendaunit_shop(yao_text)
    vacuum_text = "vacuum"
    vacuum_road = yao_job.make_l1_road(vacuum_text)
    yao_job.add_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = yao_job.get_idea_obj(vacuum_road)
    vacuum_ideaunit._assignedunit.set_suffgroup(yao_text)
    save_file(agendahub.jobs_dir(), get_file_name(yao_text), yao_job.get_json())

    # WHEN
    new_agenda = create_listen_basis(yao_src_listener)
    listen_to_speakers_intent(new_agenda, agendahub, yao_src_listener)

    # THEN irrational agenda is ignored
    assert len(new_agenda.get_intent_dict()) != 3
    assert len(new_agenda.get_intent_dict()) == 2


def test_listen_to_speakers_intent_GetsIntentFromSrcAgendaNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # GIVEN
    # yao_src_listener has task run_road
    # yao_speaker has task clean_road
    # new_yao_agenda picks yao_src_listener task run_road and not clean_road
    yao_src_listener = get_example_yao_speaker()
    assert yao_src_listener.idea_exists(run_road()) == False
    assert yao_src_listener.idea_exists(clean_road()) == False
    yao_src_listener.add_idea(ideaunit_shop(run_text(), pledge=True), casa_road())

    yao_speaker = get_example_yao_speaker()
    assert yao_speaker.idea_exists(run_road()) == False
    assert yao_speaker.idea_exists(clean_road()) == False
    yao_speaker.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    texas_agendahub = get_texas_agendahub()
    texas_agendahub.save_job_agenda(yao_speaker)

    new_yao_agenda = create_listen_basis(yao_src_listener)
    assert new_yao_agenda.idea_exists(run_road()) == False
    assert new_yao_agenda.idea_exists(clean_road()) == False

    # WHEN
    listen_to_speakers_intent(new_yao_agenda, texas_agendahub, yao_src_listener)

    # THEN
    assert new_yao_agenda.idea_exists(clean_road()) == False
    assert new_yao_agenda.idea_exists(run_road())
