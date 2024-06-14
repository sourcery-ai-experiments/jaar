from src._instrument.file import delete_dir, save_file
from src._road.jaar_config import get_json_filename
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.listen.userhub import userhub_shop
from src.listen.listen import create_listen_basis, listen_to_intents_duty_work
from src.listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
    get_dakota_userhub,
)
from src.listen.examples.example_listen import (
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


def test_listen_to_intents_duty_work_AddsTasksToAgendaWhenNo_suffgroupIsSet(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_duty = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_duty.add_partyunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_duty.set_party_pool(zia_pool)
    yao_userhub = userhub_shop(env_dir(), None, yao_text)
    yao_userhub.save_duty_agenda(yao_duty)

    zia_work = agendaunit_shop(zia_text)
    zia_work.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_work.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_work.add_partyunit(yao_text, debtor_weight=12)
    zia_userhub = userhub_shop(env_dir(), None, zia_text)
    zia_userhub.save_work_agenda(zia_work)

    new_yao_work = create_listen_basis(yao_duty)
    assert len(new_yao_work.get_intent_dict()) == 0

    # WHEN
    print(f"{len(new_yao_work.get_idea_dict())=}")
    listen_to_intents_duty_work(new_yao_work, yao_userhub)

    # THEN
    assert len(new_yao_work.get_intent_dict()) == 2


def test_listen_to_intents_duty_work_AddsTasksToAgenda(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_duty = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_duty.add_partyunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_duty.set_party_pool(zia_pool)
    yao_userhub = userhub_shop(env_dir(), None, yao_text)
    yao_userhub.save_duty_agenda(yao_duty)

    zia_work = agendaunit_shop(zia_text)
    zia_work.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_work.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_work.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_work.get_idea_obj(clean_road())
    cook_ideaunit = zia_work.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    zia_userhub = userhub_shop(env_dir(), None, zia_text)
    zia_userhub.save_work_agenda(zia_work)
    new_yao_work = create_listen_basis(yao_duty)
    assert len(new_yao_work.get_intent_dict()) == 0

    # WHEN
    print(f"{len(new_yao_work.get_idea_dict())=}")
    listen_to_intents_duty_work(new_yao_work, yao_userhub)

    # THEN
    assert len(new_yao_work.get_intent_dict()) == 2


def test_listen_to_intents_duty_work_AddsTasksToAgendaWithDetailsDecidedBy_debtor_weight(
    env_dir_setup_cleanup,
):
    # GIVEN
    zia_work = get_example_zia_speaker()
    bob_work = get_example_bob_speaker()
    bob_work.edit_idea_attr(
        road=cook_road(),
        reason_del_premise_base=eat_road(),
        reason_del_premise_need=hungry_road(),
    )
    bob_cook_ideaunit = bob_work.get_idea_obj(cook_road())
    zia_cook_ideaunit = zia_work.get_idea_obj(cook_road())
    assert bob_cook_ideaunit != zia_cook_ideaunit
    assert len(zia_cook_ideaunit._reasonunits) == 1
    assert len(bob_cook_ideaunit._reasonunits) == 0
    zia_text = zia_work._owner_id
    bob_text = bob_work._owner_id
    zia_userhub = userhub_shop(env_dir(), None, zia_text)
    bob_userhub = userhub_shop(env_dir(), None, bob_text)
    zia_userhub.save_work_agenda(zia_work)
    bob_userhub.save_work_agenda(bob_work)

    yao_duty = get_example_yao_speaker()
    yao_text = yao_duty._owner_id
    yao_userhub = userhub_shop(env_dir(), None, yao_text)
    yao_userhub.save_duty_agenda(yao_duty)

    new_yao_work1 = create_listen_basis(yao_duty)
    assert new_yao_work1.idea_exists(cook_road()) is False

    # WHEN
    listen_to_intents_duty_work(new_yao_work1, yao_userhub)

    # THEN
    assert new_yao_work1.idea_exists(cook_road())
    new_cook_idea = new_yao_work1.get_idea_obj(cook_road())
    zia_partyunit = new_yao_work1.get_party(zia_text)
    bob_partyunit = new_yao_work1.get_party(bob_text)
    assert zia_partyunit.debtor_weight < bob_partyunit.debtor_weight
    assert new_cook_idea.get_reasonunit(eat_road()) is None

    yao_zia_debtor_weight = 15
    yao_bob_debtor_weight = 5
    yao_duty.add_partyunit(zia_text, None, yao_zia_debtor_weight)
    yao_duty.add_partyunit(bob_text, None, yao_bob_debtor_weight)
    yao_duty.set_party_pool(100)
    new_yao_work2 = create_listen_basis(yao_duty)
    assert new_yao_work2.idea_exists(cook_road()) is False

    # WHEN
    listen_to_intents_duty_work(new_yao_work2, yao_userhub)

    # THEN
    assert new_yao_work2.idea_exists(cook_road())
    new_cook_idea = new_yao_work2.get_idea_obj(cook_road())
    zia_partyunit = new_yao_work2.get_party(zia_text)
    bob_partyunit = new_yao_work2.get_party(bob_text)
    assert zia_partyunit.debtor_weight > bob_partyunit.debtor_weight
    zia_eat_reasonunit = zia_cook_ideaunit.get_reasonunit(eat_road())
    assert new_cook_idea.get_reasonunit(eat_road()) == zia_eat_reasonunit


def test_listen_to_intents_duty_work_ProcessesIrrationalAgenda(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_duty = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_credor_weight = 57
    sue_debtor_weight = 51
    yao_duty.add_partyunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_duty.add_partyunit(sue_text, sue_credor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_duty.set_party_pool(yao_pool)
    yao_userhub = userhub_shop(env_dir(), None, yao_text)
    yao_userhub.save_duty_agenda(yao_duty)

    zia_text = "Zia"
    zia_work = agendaunit_shop(zia_text)
    zia_work.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_work.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_work.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_work.get_idea_obj(clean_road())
    cook_ideaunit = zia_work.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    zia_userhub = userhub_shop(env_dir(), None, zia_text)
    zia_userhub.save_work_agenda(zia_work)

    sue_work = agendaunit_shop(sue_text)
    sue_work.set_max_tree_traverse(5)
    zia_work.add_partyunit(yao_text, debtor_weight=12)
    vacuum_text = "vacuum"
    vacuum_road = sue_work.make_l1_road(vacuum_text)
    sue_work.add_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = sue_work.get_idea_obj(vacuum_road)
    vacuum_ideaunit._assignedunit.set_suffgroup(yao_text)

    egg_text = "egg first"
    egg_road = sue_work.make_l1_road(egg_text)
    sue_work.add_l1_idea(ideaunit_shop(egg_text))
    chicken_text = "chicken first"
    chicken_road = sue_work.make_l1_road(chicken_text)
    sue_work.add_l1_idea(ideaunit_shop(chicken_text))
    # set egg pledge is True when chicken first is False
    sue_work.edit_idea_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_suff_idea_active=True,
    )
    # set chick pledge is True when egg first is False
    sue_work.edit_idea_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_suff_idea_active=False,
    )
    sue_userhub = userhub_shop(env_dir(), None, sue_text)
    sue_userhub.save_work_agenda(sue_work)

    # WHEN
    new_yao_work = create_listen_basis(yao_duty)
    listen_to_intents_duty_work(new_yao_work, yao_userhub)

    # THEN irrational agenda is ignored
    assert len(new_yao_work.get_intent_dict()) != 3
    assert len(new_yao_work.get_intent_dict()) == 2
    zia_partyunit = new_yao_work.get_party(zia_text)
    sue_partyunit = new_yao_work.get_party(sue_text)
    print(f"{sue_partyunit.debtor_weight=}")
    print(f"{sue_partyunit._irrational_debtor_weight=}")
    assert zia_partyunit._irrational_debtor_weight == 0
    assert sue_partyunit._irrational_debtor_weight == 51


def test_listen_to_intents_duty_work_ProcessesMissingDebtorAgenda(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(env_dir(), None, yao_text)
    delete_dir(yao_userhub.duty_file_path())  # don't know why I have to do this...
    print(f"{os_path_exists(yao_userhub.duty_file_path())=}")
    yao_duty = agendaunit_shop(yao_text)
    zia_text = "Zia"
    sue_text = "Sue"
    zia_credor_weight = 47
    sue_credor_weight = 57
    zia_debtor_weight = 41
    sue_debtor_weight = 51
    yao_duty.add_partyunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_duty.add_partyunit(sue_text, sue_credor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_duty.set_party_pool(yao_pool)
    yao_userhub.save_duty_agenda(yao_duty)

    zia_work = agendaunit_shop(zia_text)
    zia_work.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_work.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_work.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_work.get_idea_obj(clean_road())
    cook_ideaunit = zia_work.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    zia_userhub = userhub_shop(env_dir(), None, zia_text)
    zia_userhub.save_work_agenda(zia_work)

    # WHEN
    new_yao_work = create_listen_basis(yao_duty)
    listen_to_intents_duty_work(new_yao_work, yao_userhub)

    # THEN irrational agenda is ignored
    assert len(new_yao_work.get_intent_dict()) != 3
    assert len(new_yao_work.get_intent_dict()) == 2
    zia_partyunit = new_yao_work.get_party(zia_text)
    sue_partyunit = new_yao_work.get_party(sue_text)
    print(f"{sue_partyunit.debtor_weight=}")
    print(f"{sue_partyunit._inallocable_debtor_weight=}")
    assert zia_partyunit._inallocable_debtor_weight == 0
    assert sue_partyunit._inallocable_debtor_weight == 51


def test_listen_to_intents_duty_work_ListensToOwner_duty_AndNotOwner_work(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_duty = agendaunit_shop(yao_text)
    yao_text = "Yao"
    yao_credor_weight = 57
    yao_debtor_weight = 51
    yao_duty.add_partyunit(yao_text, yao_credor_weight, yao_debtor_weight)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    yao_duty.add_partyunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_pool = 87
    yao_duty.set_party_pool(yao_pool)
    # save yao without task to roles
    yao_userhub = userhub_shop(env_dir(), None, yao_text)
    yao_userhub.save_duty_agenda(yao_duty)

    # Save Zia to work
    zia_text = "Zia"
    zia_work = agendaunit_shop(zia_text)
    zia_work.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_work.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_work.add_partyunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_work.get_idea_obj(clean_road())
    cook_ideaunit = zia_work.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    cook_ideaunit._assignedunit.set_suffgroup(yao_text)
    zia_userhub = userhub_shop(env_dir(), None, zia_text)
    zia_userhub.save_work_agenda(zia_work)

    # save yao with task to roles
    yao_old_work = agendaunit_shop(yao_text)
    vacuum_text = "vacuum"
    vacuum_road = yao_old_work.make_l1_road(vacuum_text)
    yao_old_work.add_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = yao_old_work.get_idea_obj(vacuum_road)
    vacuum_ideaunit._assignedunit.set_suffgroup(yao_text)
    yao_userhub.save_work_agenda(yao_old_work)

    # WHEN
    new_yao_work = create_listen_basis(yao_duty)
    listen_to_intents_duty_work(new_yao_work, yao_userhub)

    # THEN irrational agenda is ignored
    assert len(new_yao_work.get_intent_dict()) != 3
    assert len(new_yao_work.get_intent_dict()) == 2
