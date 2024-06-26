from src._world.belieflink import belieflink_shop
from src._world.beliefunit import beliefunit_shop
from src._world.person import personlink_shop, personunit_shop


def test_BeliefUnit_set_personlink_CorrectlySetsAttr():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_personlink = personlink_shop(yao_text, credor_weight=13, debtor_weight=7)
    sue_personlink = personlink_shop(sue_text, credor_weight=23, debtor_weight=5)
    swimmers_beliefunit = beliefunit_shop(",swimmers")

    # WHEN
    swimmers_beliefunit.set_personlink(yao_personlink)
    swimmers_beliefunit.set_personlink(sue_personlink)

    # THEN
    swimmers_persons = {
        yao_personlink.person_id: yao_personlink,
        sue_personlink.person_id: sue_personlink,
    }
    assert swimmers_beliefunit._persons == swimmers_persons


def test_BeliefUnit_get_personlink_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    swimmers_beliefunit = beliefunit_shop(",swimmers")
    swimmers_beliefunit.set_personlink(personlink_shop(yao_text, 13, 7))
    swimmers_beliefunit.set_personlink(personlink_shop(sue_text, 23, 5))

    # WHEN / THEN
    assert swimmers_beliefunit.get_personlink(yao_text) != None
    assert swimmers_beliefunit.get_personlink(sue_text) != None
    assert swimmers_beliefunit.get_personlink("Bob") is None


def test_BeliefUnit_edit_personlink_CorrectlySetsAttr():
    # GIVEN
    yao_text = "Yao"
    old_yao_credor_weight = 13
    yao_debtor_weight = 7
    swimmers_beliefunit = beliefunit_shop(",swimmers")
    swimmers_beliefunit.set_personlink(
        personlink_shop(yao_text, old_yao_credor_weight, yao_debtor_weight)
    )
    yao_personlink = swimmers_beliefunit.get_personlink(yao_text)
    assert yao_personlink.credor_weight == old_yao_credor_weight

    # WHEN
    new_yao_credor_weight = 17
    swimmers_beliefunit.edit_personlink(yao_text, credor_weight=new_yao_credor_weight)

    # THEN
    assert yao_personlink.credor_weight == new_yao_credor_weight


def test_personlink_exists_ReturnsCorrectObj():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    swimmers_beliefunit = beliefunit_shop(",swimmers")
    swimmers_beliefunit.set_personlink(personlink_shop(yao_text, 13, 7))
    swimmers_beliefunit.set_personlink(personlink_shop(sue_text, 23, 5))

    # WHEN / THEN
    assert swimmers_beliefunit.personlink_exists(yao_text)
    assert swimmers_beliefunit.personlink_exists(sue_text)
    assert swimmers_beliefunit.personlink_exists("yao") is False


def test_BeliefUnit_del_personlink_SetsAttrCorrectly():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_personlink = personlink_shop(yao_text)
    sue_personlink = personlink_shop(sue_text)
    swimmers_persons = {
        yao_personlink.person_id: yao_personlink,
        sue_personlink.person_id: sue_personlink,
    }
    swimmers_beliefunit = beliefunit_shop(",swimmers")
    swimmers_beliefunit.set_personlink(yao_personlink)
    swimmers_beliefunit.set_personlink(sue_personlink)
    assert len(swimmers_beliefunit._persons) == 2
    assert swimmers_beliefunit._persons == swimmers_persons

    # WHEN
    swimmers_beliefunit.del_personlink(yao_text)

    # THEN
    assert len(swimmers_beliefunit._persons) == 1
    assert swimmers_beliefunit._persons.get(yao_text) is None


def test_BeliefUnit_clear_personlinks_SetsAttrCorrectly():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_personlink = personlink_shop(yao_text)
    sue_personlink = personlink_shop(sue_text)
    swimmers_persons = {
        yao_personlink.person_id: yao_personlink,
        sue_personlink.person_id: sue_personlink,
    }
    swimmers_beliefunit = beliefunit_shop(",swimmers")
    swimmers_beliefunit.set_personlink(yao_personlink)
    swimmers_beliefunit.set_personlink(sue_personlink)
    assert len(swimmers_beliefunit._persons) == 2
    assert swimmers_beliefunit._persons == swimmers_persons

    # WHEN
    swimmers_beliefunit.clear_personlinks()

    # THEN
    assert len(swimmers_beliefunit._persons) == 0
    assert swimmers_beliefunit._persons.get(yao_text) is None


def test_BeliefUnit_reset_world_importance_reset_personlinks():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_personlink = personlink_shop(
        person_id=yao_text,
        _world_cred=0.13,
        _world_debt=0.7,
        _world_agenda_cred=0.53,
        _world_agenda_debt=0.77,
    )
    sue_personlink = personlink_shop(
        person_id=sue_text,
        _world_cred=0.23,
        _world_debt=0.5,
        _world_agenda_cred=0.54,
        _world_agenda_debt=0.57,
    )
    bikers_personlinks = {
        yao_personlink.person_id: yao_personlink,
        sue_personlink.person_id: sue_personlink,
    }
    bikers_belief_id = ",bikers"
    bikers_beliefunit = beliefunit_shop(bikers_belief_id)
    bikers_beliefunit._world_cred = (0.33,)
    bikers_beliefunit._world_debt = (0.44,)
    bikers_beliefunit._world_agenda_cred = (0.1,)
    bikers_beliefunit._world_agenda_debt = (0.2,)
    bikers_beliefunit.set_personlink(yao_personlink)
    bikers_beliefunit.set_personlink(sue_personlink)
    print(f"{bikers_beliefunit}")
    biker_personlink_yao = bikers_beliefunit._persons.get(yao_text)
    assert biker_personlink_yao._world_cred == 0.13
    assert biker_personlink_yao._world_debt == 0.7
    assert biker_personlink_yao._world_agenda_cred == 0.53
    assert biker_personlink_yao._world_agenda_debt == 0.77

    biker_personlink_sue = bikers_beliefunit._persons.get(sue_text)
    assert biker_personlink_sue._world_cred == 0.23
    assert biker_personlink_sue._world_debt == 0.5
    assert biker_personlink_sue._world_agenda_cred == 0.54
    assert biker_personlink_sue._world_agenda_debt == 0.57

    # WHEN
    bikers_beliefunit.reset_world_cred_debt()

    # THEN
    assert biker_personlink_yao._world_cred == 0
    assert biker_personlink_yao._world_debt == 0
    assert biker_personlink_yao._world_agenda_cred == 0
    assert biker_personlink_yao._world_agenda_debt == 0
    assert biker_personlink_sue._world_cred == 0
    assert biker_personlink_sue._world_debt == 0
    assert biker_personlink_sue._world_agenda_cred == 0
    assert biker_personlink_sue._world_agenda_debt == 0


def test_personlink_meld_ReturnsCorrectObj_BaseScenario():
    # GIVEN
    yao_personlink = personlink_shop(person_id="Yao")
    sue_personlink = personlink_shop(person_id="Sue")
    bikers_belief_id = ",bikers"
    bikers_beliefunit = beliefunit_shop(bikers_belief_id)
    bikers_beliefunit.set_personlink(yao_personlink)
    bikers_beliefunit.set_personlink(sue_personlink)

    x2_beliefunit = beliefunit_shop(bikers_belief_id)

    # WHEN
    bikers_beliefunit.meld(exterior_belief=x2_beliefunit)
    print(f"{bikers_beliefunit.belief_id=} {x2_beliefunit.belief_id=}")

    # THEN
    assert len(bikers_beliefunit._persons) == 2


def test_personlink_meld_ReturnsCorrectObj_GainScenario():
    # GIVEN
    yao_text = "Yao"
    sue_text = "Sue"
    yao_personlink = personlink_shop(yao_text, credor_weight=13, debtor_weight=7)
    sue_personlink = personlink_shop(sue_text, credor_weight=23, debtor_weight=5)
    bikers_belief_id = ",bikers"
    bikers_beliefunit = beliefunit_shop(bikers_belief_id)

    x2_beliefunit = beliefunit_shop(bikers_belief_id)
    x2_beliefunit.set_personlink(yao_personlink)
    x2_beliefunit.set_personlink(sue_personlink)

    # WHEN
    bikers_beliefunit.meld(exterior_belief=x2_beliefunit)

    # THEN
    assert len(bikers_beliefunit._persons) == 2
    assert bikers_beliefunit._persons.get(yao_text) != None


# def test_migrate_beliefunits_to_belieflinks_MigratesEmptySet():
#     # GIVEN
#     run_text = "Run"
#     fly_text = "Fly"
#     run_belieflink = belieflink_shop(run_text)
#     fly_belieflink = belieflink_shop(fly_text)

#     # WHEN


#     # THEN

#     assert 1 == 2
