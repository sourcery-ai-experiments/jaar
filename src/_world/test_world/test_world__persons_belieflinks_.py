from src._world.person import personlink_shop
from src._world.belieflink import belieflink_shop
from src._world.beliefunit import beliefunit_shop
from src._world.world import worldunit_shop


def test_WorldUnit_migrate_beliefunits_to_belieflinks_MigratesEmptySet():
    # GIVEN
    bob_world = worldunit_shop("Bob")
    assert bob_world._persons == {}

    # WHEN
    bob_world._migrate_beliefunits_to_belieflinks()

    # THEN
    assert bob_world._persons == {}


def test_WorldUnit_migrate_beliefunits_to_belieflinks_Migrates_personlinks_Without_credor_weight():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    bob_world = worldunit_shop("Bob")
    bob_world.add_personunit(yao_text)
    bob_world.add_personunit(sue_text)
    bob_world.add_personunit(zia_text)
    run_text = ",Run"
    bob_world.set_beliefunit(beliefunit_shop(run_text))
    run_beliefunit = bob_world.get_beliefunit(run_text)
    run_beliefunit.set_personlink(personlink_shop(sue_text))
    run_beliefunit.set_personlink(personlink_shop(zia_text))
    assert len(bob_world.get_beliefunit(yao_text)._persons) == 1
    assert len(bob_world.get_beliefunit(sue_text)._persons) == 1
    assert len(bob_world.get_beliefunit(zia_text)._persons) == 1
    assert len(bob_world.get_beliefunit(run_text)._persons) == 2
    assert len(bob_world.get_person(yao_text)._belieflinks) == 0
    assert len(bob_world.get_person(sue_text)._belieflinks) == 0

    # WHEN
    bob_world._migrate_beliefunits_to_belieflinks()

    # THEN
    assert len(bob_world.get_beliefunit(yao_text)._persons) == 1
    assert len(bob_world.get_beliefunit(sue_text)._persons) == 1
    assert len(bob_world.get_beliefunit(zia_text)._persons) == 1
    assert len(bob_world.get_beliefunit(run_text)._persons) == 2
    assert len(bob_world.get_person(yao_text)._belieflinks) == 1
    assert len(bob_world.get_person(sue_text)._belieflinks) == 2
    assert len(bob_world.get_person(zia_text)._belieflinks) == 2
    yao_personunit = bob_world.get_person(yao_text)
    yao_belieflink = belieflink_shop(yao_text)
    assert yao_personunit.get_belieflink(yao_text) == yao_belieflink

    # GIVEN
    run_beliefunit.del_personlink(zia_text)
    assert len(bob_world.get_beliefunit(run_text)._persons) == 1

    # WHEN
    bob_world._migrate_beliefunits_to_belieflinks()

    # THEN
    assert len(bob_world.get_beliefunit(sue_text)._persons) == 1
    assert len(bob_world.get_beliefunit(zia_text)._persons) == 1
    assert len(bob_world.get_beliefunit(run_text)._persons) == 1
    assert len(bob_world.get_person(sue_text)._belieflinks) == 2
    assert len(bob_world.get_person(zia_text)._belieflinks) == 1


def test_WorldUnit_migrate_beliefunits_to_belieflinks_Migrates_personlinks_With_credor_weight():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    bob_world = worldunit_shop("Bob")
    bob_world.add_personunit(yao_text)
    bob_world.add_personunit(sue_text)
    bob_world.add_personunit(zia_text)
    run_text = ",Run"
    bob_world.set_beliefunit(beliefunit_shop(run_text))
    run_beliefunit = bob_world.get_beliefunit(run_text)
    sue_run_credor_weight = 11
    sue_run_debtor_weight = 13
    zia_run_credor_weight = 17
    zia_run_debtor_weight = 23
    sue_run_personlink = personlink_shop(
        sue_text, sue_run_credor_weight, sue_run_debtor_weight
    )
    zia_run_personlink = personlink_shop(
        zia_text, zia_run_credor_weight, zia_run_debtor_weight
    )
    run_beliefunit.set_personlink(sue_run_personlink)
    run_beliefunit.set_personlink(zia_run_personlink)
    assert len(bob_world.get_beliefunit(run_text)._persons) == 2
    assert len(bob_world.get_person(yao_text)._belieflinks) == 0
    assert len(bob_world.get_person(sue_text)._belieflinks) == 0

    # WHEN
    bob_world._migrate_beliefunits_to_belieflinks()

    # THEN
    assert len(bob_world.get_person(sue_text)._belieflinks) == 2
    assert len(bob_world.get_person(zia_text)._belieflinks) == 2
    sue_personunit = bob_world.get_person(sue_text)
    zia_personunit = bob_world.get_person(zia_text)
    sue_belieflink = sue_personunit.get_belieflink(run_text)
    zia_belieflink = zia_personunit.get_belieflink(run_text)
    assert sue_belieflink.credor_weight == sue_run_credor_weight
    assert sue_belieflink.debtor_weight == sue_run_debtor_weight
    assert zia_belieflink.credor_weight == zia_run_credor_weight
    assert zia_belieflink.debtor_weight == zia_run_debtor_weight


def test_WorldUnit_migrate_belieflinks_to_beliefunits_MigratesEmptySet():
    # GIVEN
    bob_world = worldunit_shop("Bob")
    assert bob_world._persons == {}
    assert bob_world._beliefs == {}

    # WHEN
    bob_world._migrate_belieflinks_to_beliefunits()

    # THEN
    assert bob_world._persons == {}
    assert bob_world._beliefs == {}


def test_WorldUnit_migrate_belieflinks_to_beliefunits_Migrates_personlinks_Without_credor_weight():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    bob_world = worldunit_shop("Bob")
    bob_world.add_personunit(yao_text)
    bob_world.add_personunit(sue_text)
    bob_world.add_personunit(zia_text)
    yao_personunit = bob_world.get_person(yao_text)
    sue_personunit = bob_world.get_person(sue_text)
    zia_personunit = bob_world.get_person(zia_text)
    yao_personunit.set_belieflink(belieflink_shop(yao_text))
    sue_personunit.set_belieflink(belieflink_shop(sue_text))
    zia_personunit.set_belieflink(belieflink_shop(zia_text))
    run_text = ",Run"
    sue_personunit.set_belieflink(belieflink_shop(run_text))
    zia_personunit.set_belieflink(belieflink_shop(run_text))
    assert len(bob_world.get_person(yao_text)._belieflinks) == 1
    assert len(bob_world.get_person(sue_text)._belieflinks) == 2
    assert len(bob_world.get_person(zia_text)._belieflinks) == 2
    assert len(bob_world.get_person(zia_text)._belieflinks) == 2
    assert set(bob_world._beliefs.keys()) == {yao_text, sue_text, zia_text}

    # WHEN
    bob_world._migrate_belieflinks_to_beliefunits()

    # THEN
    assert len(bob_world.get_beliefunit(yao_text)._persons) == 1
    assert len(bob_world.get_beliefunit(sue_text)._persons) == 1
    assert len(bob_world.get_beliefunit(zia_text)._persons) == 1
    assert len(bob_world.get_beliefunit(run_text)._persons) == 2
    assert len(bob_world.get_person(yao_text)._belieflinks) == 0
    assert len(bob_world.get_person(sue_text)._belieflinks) == 0
    assert len(bob_world.get_person(zia_text)._belieflinks) == 0

    run_beliefunit = bob_world.get_beliefunit(run_text)
    assert run_beliefunit._persons.get(zia_text) == personlink_shop(zia_text)
    assert run_beliefunit._persons.get(sue_text) == personlink_shop(sue_text)
    yao_personunit = bob_world.get_person(yao_text)
    assert yao_personunit.get_belieflink(yao_text) is None


def test_WorldUnit_migrate_belieflinks_to_beliefunits_Migrates_personlinks_With_credor_weight():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    zia_text = "Zia"
    bob_world = worldunit_shop("Bob")
    bob_world.add_personunit(yao_text)
    bob_world.add_personunit(sue_text)
    bob_world.add_personunit(zia_text)
    yao_personunit = bob_world.get_person(yao_text)
    sue_personunit = bob_world.get_person(sue_text)
    zia_personunit = bob_world.get_person(zia_text)
    yao_personunit.set_belieflink(belieflink_shop(yao_text))
    sue_personunit.set_belieflink(belieflink_shop(sue_text))
    zia_personunit.set_belieflink(belieflink_shop(zia_text))
    run_text = ",Run"
    sue_run_credor_weight = 11
    sue_run_debtor_weight = 13
    zia_run_credor_weight = 17
    zia_run_debtor_weight = 23
    sue_run_belieflink = belieflink_shop(
        run_text, sue_run_credor_weight, sue_run_debtor_weight
    )
    zia_run_belieflink = belieflink_shop(
        run_text, zia_run_credor_weight, zia_run_debtor_weight
    )
    sue_personunit.set_belieflink(sue_run_belieflink)
    zia_personunit.set_belieflink(zia_run_belieflink)
    assert len(bob_world.get_person(yao_text)._belieflinks) == 1
    assert len(bob_world.get_person(sue_text)._belieflinks) == 2
    assert len(bob_world.get_person(zia_text)._belieflinks) == 2
    assert len(bob_world.get_person(zia_text)._belieflinks) == 2
    assert set(bob_world._beliefs.keys()) == {yao_text, sue_text, zia_text}

    # WHEN
    bob_world._migrate_belieflinks_to_beliefunits()

    # THEN
    assert len(bob_world.get_beliefunit(yao_text)._persons) == 1
    assert len(bob_world.get_beliefunit(sue_text)._persons) == 1
    assert len(bob_world.get_beliefunit(zia_text)._persons) == 1
    assert len(bob_world.get_beliefunit(run_text)._persons) == 2
    assert len(bob_world.get_person(yao_text)._belieflinks) == 0
    assert len(bob_world.get_person(sue_text)._belieflinks) == 0
    assert len(bob_world.get_person(zia_text)._belieflinks) == 0

    static_sue_run_personlink = personlink_shop(
        sue_text, sue_run_credor_weight, sue_run_debtor_weight
    )
    static_zia_run_personlink = personlink_shop(
        zia_text, zia_run_credor_weight, zia_run_debtor_weight
    )
    run_beliefunit = bob_world.get_beliefunit(run_text)
    assert run_beliefunit._persons.get(zia_text) != None
    assert run_beliefunit._persons.get(sue_text) != None
    gen_zia_run_personlink = run_beliefunit._persons.get(zia_text)
    gen_sue_run_personlink = run_beliefunit._persons.get(sue_text)
    assert gen_sue_run_personlink == static_sue_run_personlink
    assert gen_zia_run_personlink == static_zia_run_personlink
