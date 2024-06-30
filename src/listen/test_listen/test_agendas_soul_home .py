from src._instrument.file import delete_dir, save_file
from src._road.jaar_config import get_json_filename
from src._world.idea import ideaunit_shop
from src._world.world import worldunit_shop
from src.listen.hubunit import hubunit_shop
from src.listen.listen import create_listen_basis, listen_to_agendas_soul_being
from src.listen.examples.listen_env import (
    get_listen_temp_env_dir as env_dir,
    env_dir_setup_cleanup,
    get_dakota_hubunit,
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


def test_listen_to_agendas_soul_being_AddsTasksToWorldWhenNo_heldbeliefIsSet(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_soul = worldunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_soul.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_soul.set_char_pool(zia_pool)
    yao_hubunit = hubunit_shop(env_dir(), None, yao_text)
    yao_hubunit.save_soul_world(yao_soul)

    zia_being = worldunit_shop(zia_text)
    zia_being.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_being.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_being.add_charunit(yao_text, debtor_weight=12)
    zia_hubunit = hubunit_shop(env_dir(), None, zia_text)
    zia_hubunit.save_being_world(zia_being)

    new_yao_being = create_listen_basis(yao_soul)
    assert len(new_yao_being.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_being.get_idea_dict())=}")
    listen_to_agendas_soul_being(new_yao_being, yao_hubunit)

    # THEN
    assert len(new_yao_being.get_agenda_dict()) == 2


def test_listen_to_agendas_soul_being_AddsTasksToWorld(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_soul = worldunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_soul.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_soul.set_char_pool(zia_pool)
    yao_hubunit = hubunit_shop(env_dir(), None, yao_text)
    yao_hubunit.save_soul_world(yao_soul)

    zia_being = worldunit_shop(zia_text)
    zia_being.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_being.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_being.add_charunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_being.get_idea_obj(clean_road())
    cook_ideaunit = zia_being.get_idea_obj(cook_road())
    clean_ideaunit._cultureunit.set_heldbelief(yao_text)
    cook_ideaunit._cultureunit.set_heldbelief(yao_text)
    zia_hubunit = hubunit_shop(env_dir(), None, zia_text)
    zia_hubunit.save_being_world(zia_being)
    new_yao_being = create_listen_basis(yao_soul)
    assert len(new_yao_being.get_agenda_dict()) == 0

    # WHEN
    print(f"{len(new_yao_being.get_idea_dict())=}")
    listen_to_agendas_soul_being(new_yao_being, yao_hubunit)

    # THEN
    assert len(new_yao_being.get_agenda_dict()) == 2


def test_listen_to_agendas_soul_being_AddsTasksToWorldWithDetailsDecidedBy_debtor_weight(
    env_dir_setup_cleanup,
):
    # GIVEN
    zia_being = get_example_zia_speaker()
    bob_being = get_example_bob_speaker()
    bob_being.edit_idea_attr(
        road=cook_road(),
        reason_del_premise_base=eat_road(),
        reason_del_premise_need=hungry_road(),
    )
    bob_cook_ideaunit = bob_being.get_idea_obj(cook_road())
    zia_cook_ideaunit = zia_being.get_idea_obj(cook_road())
    assert bob_cook_ideaunit != zia_cook_ideaunit
    assert len(zia_cook_ideaunit._reasonunits) == 1
    assert len(bob_cook_ideaunit._reasonunits) == 0
    zia_text = zia_being._owner_id
    bob_text = bob_being._owner_id
    zia_hubunit = hubunit_shop(env_dir(), None, zia_text)
    bob_hubunit = hubunit_shop(env_dir(), None, bob_text)
    zia_hubunit.save_being_world(zia_being)
    bob_hubunit.save_being_world(bob_being)

    yao_soul = get_example_yao_speaker()
    yao_text = yao_soul._owner_id
    yao_hubunit = hubunit_shop(env_dir(), None, yao_text)
    yao_hubunit.save_soul_world(yao_soul)

    new_yao_being1 = create_listen_basis(yao_soul)
    assert new_yao_being1.idea_exists(cook_road()) is False

    # WHEN
    listen_to_agendas_soul_being(new_yao_being1, yao_hubunit)

    # THEN
    assert new_yao_being1.idea_exists(cook_road())
    new_cook_idea = new_yao_being1.get_idea_obj(cook_road())
    zia_charunit = new_yao_being1.get_char(zia_text)
    bob_charunit = new_yao_being1.get_char(bob_text)
    assert zia_charunit.debtor_weight < bob_charunit.debtor_weight
    assert new_cook_idea.get_reasonunit(eat_road()) is None

    yao_zia_debtor_weight = 15
    yao_bob_debtor_weight = 5
    yao_soul.add_charunit(zia_text, None, yao_zia_debtor_weight)
    yao_soul.add_charunit(bob_text, None, yao_bob_debtor_weight)
    yao_soul.set_char_pool(100)
    new_yao_being2 = create_listen_basis(yao_soul)
    assert new_yao_being2.idea_exists(cook_road()) is False

    # WHEN
    listen_to_agendas_soul_being(new_yao_being2, yao_hubunit)

    # THEN
    assert new_yao_being2.idea_exists(cook_road())
    new_cook_idea = new_yao_being2.get_idea_obj(cook_road())
    zia_charunit = new_yao_being2.get_char(zia_text)
    bob_charunit = new_yao_being2.get_char(bob_text)
    assert zia_charunit.debtor_weight > bob_charunit.debtor_weight
    zia_eat_reasonunit = zia_cook_ideaunit.get_reasonunit(eat_road())
    assert new_cook_idea.get_reasonunit(eat_road()) == zia_eat_reasonunit


def test_listen_to_agendas_soul_being_ProcessesIrrationalWorld(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_soul = worldunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    sue_text = "Sue"
    sue_credor_weight = 57
    sue_debtor_weight = 51
    yao_soul.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_soul.add_charunit(sue_text, sue_credor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_soul.set_char_pool(yao_pool)
    yao_hubunit = hubunit_shop(env_dir(), None, yao_text)
    yao_hubunit.save_soul_world(yao_soul)

    zia_text = "Zia"
    zia_being = worldunit_shop(zia_text)
    zia_being.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_being.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_being.add_charunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_being.get_idea_obj(clean_road())
    cook_ideaunit = zia_being.get_idea_obj(cook_road())
    clean_ideaunit._cultureunit.set_heldbelief(yao_text)
    cook_ideaunit._cultureunit.set_heldbelief(yao_text)
    zia_hubunit = hubunit_shop(env_dir(), None, zia_text)
    zia_hubunit.save_being_world(zia_being)

    sue_being = worldunit_shop(sue_text)
    sue_being.set_max_tree_traverse(5)
    zia_being.add_charunit(yao_text, debtor_weight=12)
    vacuum_text = "vacuum"
    vacuum_road = sue_being.make_l1_road(vacuum_text)
    sue_being.add_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = sue_being.get_idea_obj(vacuum_road)
    vacuum_ideaunit._cultureunit.set_heldbelief(yao_text)

    egg_text = "egg first"
    egg_road = sue_being.make_l1_road(egg_text)
    sue_being.add_l1_idea(ideaunit_shop(egg_text))
    chicken_text = "chicken first"
    chicken_road = sue_being.make_l1_road(chicken_text)
    sue_being.add_l1_idea(ideaunit_shop(chicken_text))
    # set egg pledge is True when chicken first is False
    sue_being.edit_idea_attr(
        road=egg_road,
        pledge=True,
        reason_base=chicken_road,
        reason_suff_idea_active=True,
    )
    # set chick pledge is True when egg first is False
    sue_being.edit_idea_attr(
        road=chicken_road,
        pledge=True,
        reason_base=egg_road,
        reason_suff_idea_active=False,
    )
    sue_hubunit = hubunit_shop(env_dir(), None, sue_text)
    sue_hubunit.save_being_world(sue_being)

    # WHEN
    new_yao_being = create_listen_basis(yao_soul)
    listen_to_agendas_soul_being(new_yao_being, yao_hubunit)

    # THEN irrational world is ignored
    assert len(new_yao_being.get_agenda_dict()) != 3
    assert len(new_yao_being.get_agenda_dict()) == 2
    zia_charunit = new_yao_being.get_char(zia_text)
    sue_charunit = new_yao_being.get_char(sue_text)
    print(f"{sue_charunit.debtor_weight=}")
    print(f"{sue_charunit._irrational_debtor_weight=}")
    assert zia_charunit._irrational_debtor_weight == 0
    assert sue_charunit._irrational_debtor_weight == 51


def test_listen_to_agendas_soul_being_ProcessesMissingDebtorWorld(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_hubunit = hubunit_shop(env_dir(), None, yao_text)
    delete_dir(yao_hubunit.soul_file_path())  # don't know why I have to do this...
    print(f"{os_path_exists(yao_hubunit.soul_file_path())=}")
    yao_soul = worldunit_shop(yao_text)
    zia_text = "Zia"
    sue_text = "Sue"
    zia_credor_weight = 47
    sue_credor_weight = 57
    zia_debtor_weight = 41
    sue_debtor_weight = 51
    yao_soul.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_soul.add_charunit(sue_text, sue_credor_weight, sue_debtor_weight)
    yao_pool = 92
    yao_soul.set_char_pool(yao_pool)
    yao_hubunit.save_soul_world(yao_soul)

    zia_being = worldunit_shop(zia_text)
    zia_being.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_being.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_being.add_charunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_being.get_idea_obj(clean_road())
    cook_ideaunit = zia_being.get_idea_obj(cook_road())
    clean_ideaunit._cultureunit.set_heldbelief(yao_text)
    cook_ideaunit._cultureunit.set_heldbelief(yao_text)
    zia_hubunit = hubunit_shop(env_dir(), None, zia_text)
    zia_hubunit.save_being_world(zia_being)

    # WHEN
    new_yao_being = create_listen_basis(yao_soul)
    listen_to_agendas_soul_being(new_yao_being, yao_hubunit)

    # THEN irrational world is ignored
    assert len(new_yao_being.get_agenda_dict()) != 3
    assert len(new_yao_being.get_agenda_dict()) == 2
    zia_charunit = new_yao_being.get_char(zia_text)
    sue_charunit = new_yao_being.get_char(sue_text)
    print(f"{sue_charunit.debtor_weight=}")
    print(f"{sue_charunit._inallocable_debtor_weight=}")
    assert zia_charunit._inallocable_debtor_weight == 0
    assert sue_charunit._inallocable_debtor_weight == 51


def test_listen_to_agendas_soul_being_ListensToOwner_soul_AndNotOwner_being(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_soul = worldunit_shop(yao_text)
    yao_text = "Yao"
    yao_credor_weight = 57
    yao_debtor_weight = 51
    yao_soul.add_charunit(yao_text, yao_credor_weight, yao_debtor_weight)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    yao_soul.add_charunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_pool = 87
    yao_soul.set_char_pool(yao_pool)
    # save yao without task to dutys
    yao_hubunit = hubunit_shop(env_dir(), None, yao_text)
    yao_hubunit.save_soul_world(yao_soul)

    # Save Zia to being
    zia_text = "Zia"
    zia_being = worldunit_shop(zia_text)
    zia_being.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    zia_being.add_idea(ideaunit_shop(cook_text(), pledge=True), casa_road())
    zia_being.add_charunit(yao_text, debtor_weight=12)
    clean_ideaunit = zia_being.get_idea_obj(clean_road())
    cook_ideaunit = zia_being.get_idea_obj(cook_road())
    clean_ideaunit._cultureunit.set_heldbelief(yao_text)
    cook_ideaunit._cultureunit.set_heldbelief(yao_text)
    zia_hubunit = hubunit_shop(env_dir(), None, zia_text)
    zia_hubunit.save_being_world(zia_being)

    # save yao with task to dutys
    yao_old_being = worldunit_shop(yao_text)
    vacuum_text = "vacuum"
    vacuum_road = yao_old_being.make_l1_road(vacuum_text)
    yao_old_being.add_l1_idea(ideaunit_shop(vacuum_text, pledge=True))
    vacuum_ideaunit = yao_old_being.get_idea_obj(vacuum_road)
    vacuum_ideaunit._cultureunit.set_heldbelief(yao_text)
    yao_hubunit.save_being_world(yao_old_being)

    # WHEN
    new_yao_being = create_listen_basis(yao_soul)
    listen_to_agendas_soul_being(new_yao_being, yao_hubunit)

    # THEN irrational world is ignored
    assert len(new_yao_being.get_agenda_dict()) != 3
    assert len(new_yao_being.get_agenda_dict()) == 2
