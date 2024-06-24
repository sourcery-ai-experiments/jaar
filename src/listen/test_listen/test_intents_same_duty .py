from src._instrument.file import delete_dir, save_file
from src._road.jaar_config import get_json_filename
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.listen.userhub import userhub_shop
from src.listen.listen import create_listen_basis, listen_to_intents_same_duty
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


def test_listen_to_intents_same_duty_AddsTasksToAgendaWhenNo_suffbeliefIsSet(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_same = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_same.add_otherunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_same.set_other_pool(zia_pool)
    yao_userhub = userhub_shop(env_dir(), None, yao_text)
    yao_userhub.save_same_agenda(yao_same)

    zia_duty = agendaunit_shop(zia_text)
    zia_duty.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_duty.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_duty.add_otherunit(yao_text, debtor_weight=12)
    zia_userhub = userhub_shop(env_dir(), None, zia_text)
    zia_userhub.save_duty_agenda(zia_duty)

    new_yao_duty = create_listen_basis(yao_same)
    assert len(new_yao_duty.get_intent_dict()) == 0

    # WHEN
    print(f"{len(new_yao_duty.get_idea_dict())=}")
    listen_to_intents_same_duty(new_yao_duty, yao_userhub)

    # THEN
    assert len(new_yao_duty.get_intent_dict()) == 2


def test_listen_to_intents_same_duty_AddsTasksToAgenda(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_same = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_same.add_otherunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_same.set_other_pool(zia_pool)
    yao_userhub = userhub_shop(env_dir(), None, yao_text)
    yao_userhub.save_same_agenda(yao_same)

    zia_duty = agendaunit_shop(zia_text)
    zia_duty.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_duty.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_duty.add_otherunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_duty.get_idea_obj(clean_road())
    cook_ideaunit = zia_duty.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffbelief(yao_text)
    cook_ideaunit._assignedunit.set_suffbelief(yao_text)
    zia_userhub = userhub_shop(env_dir(), None, zia_text)
    zia_userhub.save_duty_agenda(zia_duty)
    new_yao_duty = create_listen_basis(yao_same)
    assert len(new_yao_duty.get_intent_dict()) == 0

    # WHEN
    print(f"{len(new_yao_duty.get_idea_dict())=}")
    listen_to_intents_same_duty(new_yao_duty, yao_userhub)

    # THEN
    assert len(new_yao_duty.get_intent_dict()) == 2


def test_listen_to_intents_same_duty_AddsTasksToAgendaWithDetailsDecidedBy_debtor_weight(
    env_dir_setup_cleanup,
):
    # GIVEN
    zia_duty = get_example_zia_speaker()
    bob_duty = get_example_bob_speaker()
    bob_duty.edit_idea_attr(
        road=cook_road(),
        reason_del_premise_base=eat_road(),
        reason_del_premise_need=hungry_road(),
    )
    bob_cook_ideaunit = bob_duty.get_idea_obj(cook_road())
    zia_cook_ideaunit = zia_duty.get_idea_obj(cook_road())
    assert bob_cook_ideaunit != zia_cook_ideaunit
    assert len(zia_cook_ideaunit._reasonunits) == 1
    assert len(bob_cook_ideaunit._reasonunits) == 0
    zia_text = zia_duty._owner_id
    bob_text = bob_duty._owner_id
    zia_userhub = userhub_shop(env_dir(), None, zia_text)
    bob_userhub = userhub_shop(env_dir(), None, bob_text)
    zia_userhub.save_duty_agenda(zia_duty)
    bob_userhub.save_duty_agenda(bob_duty)

    yao_same = get_example_yao_speaker()
    yao_text = yao_same._owner_id
    yao_userhub = userhub_shop(env_dir(), None, yao_text)
    yao_userhub.save_same_agenda(yao_same)

    new_yao_duty1 = create_listen_basis(yao_same)
    assert new_yao_duty1.idea_exists(cook_road()) is False

    # WHEN
    listen_to_intents_same_duty(new_yao_duty1, yao_userhub)

    # THEN
    assert new_yao_duty1.idea_exists(cook_road())
    new_cook_idea = new_yao_duty1.get_idea_obj(cook_road())
    zia_otherunit = new_yao_duty1.get_other(zia_text)
    bob_otherunit = new_yao_duty1.get_other(bob_text)
    assert zia_otherunit.debtor_weight < bob_otherunit.debtor_weight
    assert new_cook_idea.get_reasonunit(eat_road()) is None

    yao_zia_debtor_weight = 15
    yao_bob_debtor_weight = 5
    yao_same.add_otherunit(zia_text, None, yao_zia_debtor_weight)
    yao_same.add_otherunit(bob_text, None, yao_bob_debtor_weight)
    yao_same.set_other_pool(100)
    new_yao_duty2 = create_listen_basis(yao_same)
    assert new_yao_duty2.idea_exists(cook_road()) is False

    # WHEN
    listen_to_intents_same_duty(new_yao_duty2, yao_userhub)

    # THEN
    assert new_yao_duty2.idea_exists(cook_road())
    new_cook_idea = new_yao_duty2.get_idea_obj(cook_road())
    zia_otherunit = new_yao_duty2.get_other(zia_text)
    bob_otherunit = new_yao_duty2.get_other(bob_text)
    assert zia_otherunit.debtor_weight > bob_otherunit.debtor_weight
    zia_eat_reasonunit = zia_cook_ideaunit.get_reasonunit(eat_road())
    assert new_cook_idea.get_reasonunit(eat_road()) == zia_eat_reasonunit


def test_listen_to_intents_same_duty_ProcessesIrrationalAgenda(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_same = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_credor_weight = 57
    sue_debtor_weight = 51
    yao_same.add_otherunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_same.add_otherunit(sue_text, sue_credor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_same.set_other_pool(yao_pool)
    yao_userhub = userhub_shop(env_dir(), None, yao_text)
    yao_userhub.save_same_agenda(yao_same)

    zia_text = "Zia"
    zia_duty = agendaunit_shop(zia_text)
    zia_duty.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_duty.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_duty.add_otherunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_duty.get_idea_obj(clean_road())
    cook_ideaunit = zia_duty.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffbelief(yao_text)
    cook_ideaunit._assignedunit.set_suffbelief(yao_text)
    zia_userhub = userhub_shop(env_dir(), None, zia_text)
    zia_userhub.save_duty_agenda(zia_duty)

    sue_duty = agendaunit_shop(sue_text)
    sue_duty.set_max_tree_traverse(5)
    zia_duty.add_otherunit(yao_text, debtor_weight=12)
    vacuum_text = "vacuum"
    vacuum_road = sue_duty.make_l1_road(vacuum_text)
    sue_duty.add_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = sue_duty.get_idea_obj(vacuum_road)
    vacuum_ideaunit._assignedunit.set_suffbelief(yao_text)

    egg_text = "egg first"
    egg_road = sue_duty.make_l1_road(egg_text)
    sue_duty.add_l1_idea(ideaunit_shop(egg_text))
    chicken_text = "chicken first"
    chicken_road = sue_duty.make_l1_road(chicken_text)
    sue_duty.add_l1_idea(ideaunit_shop(chicken_text))
    # set egg pledge is True when chicken first is False
    sue_duty.edit_idea_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_suff_idea_active=True,
    )
    # set chick pledge is True when egg first is False
    sue_duty.edit_idea_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_suff_idea_active=False,
    )
    sue_userhub = userhub_shop(env_dir(), None, sue_text)
    sue_userhub.save_duty_agenda(sue_duty)

    # WHEN
    new_yao_duty = create_listen_basis(yao_same)
    listen_to_intents_same_duty(new_yao_duty, yao_userhub)

    # THEN irrational agenda is ignored
    assert len(new_yao_duty.get_intent_dict()) != 3
    assert len(new_yao_duty.get_intent_dict()) == 2
    zia_otherunit = new_yao_duty.get_other(zia_text)
    sue_otherunit = new_yao_duty.get_other(sue_text)
    print(f"{sue_otherunit.debtor_weight=}")
    print(f"{sue_otherunit._irrational_debtor_weight=}")
    assert zia_otherunit._irrational_debtor_weight == 0
    assert sue_otherunit._irrational_debtor_weight == 51


def test_listen_to_intents_same_duty_ProcessesMissingDebtorAgenda(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_userhub = userhub_shop(env_dir(), None, yao_text)
    delete_dir(yao_userhub.same_file_path())  # don't know why I have to do this...
    print(f"{os_path_exists(yao_userhub.same_file_path())=}")
    yao_same = agendaunit_shop(yao_text)
    zia_text = "Zia"
    sue_text = "Sue"
    zia_credor_weight = 47
    sue_credor_weight = 57
    zia_debtor_weight = 41
    sue_debtor_weight = 51
    yao_same.add_otherunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_same.add_otherunit(sue_text, sue_credor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_same.set_other_pool(yao_pool)
    yao_userhub.save_same_agenda(yao_same)

    zia_duty = agendaunit_shop(zia_text)
    zia_duty.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_duty.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_duty.add_otherunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_duty.get_idea_obj(clean_road())
    cook_ideaunit = zia_duty.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffbelief(yao_text)
    cook_ideaunit._assignedunit.set_suffbelief(yao_text)
    zia_userhub = userhub_shop(env_dir(), None, zia_text)
    zia_userhub.save_duty_agenda(zia_duty)

    # WHEN
    new_yao_duty = create_listen_basis(yao_same)
    listen_to_intents_same_duty(new_yao_duty, yao_userhub)

    # THEN irrational agenda is ignored
    assert len(new_yao_duty.get_intent_dict()) != 3
    assert len(new_yao_duty.get_intent_dict()) == 2
    zia_otherunit = new_yao_duty.get_other(zia_text)
    sue_otherunit = new_yao_duty.get_other(sue_text)
    print(f"{sue_otherunit.debtor_weight=}")
    print(f"{sue_otherunit._inallocable_debtor_weight=}")
    assert zia_otherunit._inallocable_debtor_weight == 0
    assert sue_otherunit._inallocable_debtor_weight == 51


def test_listen_to_intents_same_duty_ListensToOwner_same_AndNotOwner_duty(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_same = agendaunit_shop(yao_text)
    yao_text = "Yao"
    yao_credor_weight = 57
    yao_debtor_weight = 51
    yao_same.add_otherunit(yao_text, yao_credor_weight, yao_debtor_weight)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    yao_same.add_otherunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_pool = 87
    yao_same.set_other_pool(yao_pool)
    # save yao without task to roles
    yao_userhub = userhub_shop(env_dir(), None, yao_text)
    yao_userhub.save_same_agenda(yao_same)

    # Save Zia to duty
    zia_text = "Zia"
    zia_duty = agendaunit_shop(zia_text)
    zia_duty.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_duty.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_duty.add_otherunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_duty.get_idea_obj(clean_road())
    cook_ideaunit = zia_duty.get_idea_obj(cook_road())
    clean_ideaunit._assignedunit.set_suffbelief(yao_text)
    cook_ideaunit._assignedunit.set_suffbelief(yao_text)
    zia_userhub = userhub_shop(env_dir(), None, zia_text)
    zia_userhub.save_duty_agenda(zia_duty)

    # save yao with task to roles
    yao_old_duty = agendaunit_shop(yao_text)
    vacuum_text = "vacuum"
    vacuum_road = yao_old_duty.make_l1_road(vacuum_text)
    yao_old_duty.add_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = yao_old_duty.get_idea_obj(vacuum_road)
    vacuum_ideaunit._assignedunit.set_suffbelief(yao_text)
    yao_userhub.save_duty_agenda(yao_old_duty)

    # WHEN
    new_yao_duty = create_listen_basis(yao_same)
    listen_to_intents_same_duty(new_yao_duty, yao_userhub)

    # THEN irrational agenda is ignored
    assert len(new_yao_duty.get_intent_dict()) != 3
    assert len(new_yao_duty.get_intent_dict()) == 2
