from src._world.person import personlink_shop
from src._world.beliefunit import (
    BalanceLine,
    balanceline_shop,
    BeliefUnit,
    beliefunit_shop,
    BeliefID,
    BalanceLink,
    balancelink_shop,
    balancelinks_get_from_json,
    balanceheir_shop,
    get_from_json as beliefunits_get_from_json,
    get_beliefunit_from_dict,
    get_beliefunits_from_dict,
)
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src._instrument.python import x_is_json, get_json_from_dict
from pytest import raises as pytest_raises


def test_BeliefUnit_set_personlink_CorrectlySetsAttr():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_person = personlink_shop(
        person_id=todd_text, credor_weight=13, debtor_weight=7
    )
    mery_person = personlink_shop(
        person_id=mery_text, credor_weight=23, debtor_weight=5
    )

    swimmers_belief = beliefunit_shop(belief_id=",swimmers", _persons={})

    # WHEN
    swimmers_belief.set_personlink(todd_person)
    swimmers_belief.set_personlink(mery_person)

    # THEN
    swimmers_persons = {
        todd_person.person_id: todd_person,
        mery_person.person_id: mery_person,
    }
    assert swimmers_belief._persons == swimmers_persons


def test_BeliefUnit_get_personlink_ReturnsCorrectObj():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    swimmers_belief = beliefunit_shop(belief_id=",swimmers", _persons={})
    swimmers_belief.set_personlink(personlink_shop(todd_text, 13, 7))
    swimmers_belief.set_personlink(personlink_shop(mery_text, 23, 5))

    # WHEN / THEN
    assert swimmers_belief.get_personlink(todd_text) != None
    assert swimmers_belief.get_personlink(mery_text) != None
    assert swimmers_belief.get_personlink("todd") is None


def test_BeliefUnit_edit_personlink_CorrectlySetsAttr():
    # GIVEN
    todd_text = "Todd"
    old_todd_credor_weight = 13
    todd_debtor_weight = 7
    swimmers_belief = beliefunit_shop(belief_id=",swimmers")
    swimmers_belief.set_personlink(
        personlink_shop(todd_text, old_todd_credor_weight, todd_debtor_weight)
    )
    todd_personlink = swimmers_belief.get_personlink(todd_text)
    assert todd_personlink.credor_weight == old_todd_credor_weight

    # WHEN
    new_todd_credor_weight = 17
    swimmers_belief.edit_personlink(
        person_id=todd_text, credor_weight=new_todd_credor_weight
    )

    # THEN
    assert todd_personlink.credor_weight == new_todd_credor_weight


def test_personlink_exists_ReturnsCorrectObj():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    swimmers_belief = beliefunit_shop(belief_id=",swimmers", _persons={})
    swimmers_belief.set_personlink(personlink_shop(todd_text, 13, 7))
    swimmers_belief.set_personlink(personlink_shop(mery_text, 23, 5))

    # WHEN / THEN
    assert swimmers_belief.personlink_exists(todd_text)
    assert swimmers_belief.personlink_exists(mery_text)
    assert swimmers_belief.personlink_exists("todd") is False


def test_BeliefUnit_del_personlink_SetsAttrCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_person = personlink_shop(person_id=todd_text)
    mery_person = personlink_shop(person_id=mery_text)
    swimmers_persons = {
        todd_person.person_id: todd_person,
        mery_person.person_id: mery_person,
    }
    swimmers_belief = beliefunit_shop(belief_id=",swimmers", _persons={})
    swimmers_belief.set_personlink(todd_person)
    swimmers_belief.set_personlink(mery_person)
    assert len(swimmers_belief._persons) == 2
    assert swimmers_belief._persons == swimmers_persons

    # WHEN
    swimmers_belief.del_personlink(person_id=todd_text)

    # THEN
    assert len(swimmers_belief._persons) == 1
    assert swimmers_belief._persons.get(todd_text) is None


def test_BeliefUnit_clear_personlinks_SetsAttrCorrectly():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_person = personlink_shop(person_id=todd_text)
    mery_person = personlink_shop(person_id=mery_text)
    swimmers_persons = {
        todd_person.person_id: todd_person,
        mery_person.person_id: mery_person,
    }
    swimmers_belief = beliefunit_shop(belief_id=",swimmers", _persons={})
    swimmers_belief.set_personlink(todd_person)
    swimmers_belief.set_personlink(mery_person)
    assert len(swimmers_belief._persons) == 2
    assert swimmers_belief._persons == swimmers_persons

    # WHEN
    swimmers_belief.clear_personlinks()

    # THEN
    assert len(swimmers_belief._persons) == 0
    assert swimmers_belief._persons.get(todd_text) is None


def test_BeliefUnit_reset_world_importance_reset_personlinks():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_person = personlink_shop(
        person_id=todd_text,
        _world_cred=0.13,
        _world_debt=0.7,
        _world_agenda_cred=0.53,
        _world_agenda_debt=0.77,
    )
    mery_person = personlink_shop(
        person_id=mery_text,
        _world_cred=0.23,
        _world_debt=0.5,
        _world_agenda_cred=0.54,
        _world_agenda_debt=0.57,
    )
    bikers_persons = {
        todd_person.person_id: todd_person,
        mery_person.person_id: mery_person,
    }
    bikers_belief_id = ",bikers"
    bikers_beliefunit = beliefunit_shop(belief_id=bikers_belief_id)
    bikers_beliefunit._world_cred = (0.33,)
    bikers_beliefunit._world_debt = (0.44,)
    bikers_beliefunit._world_agenda_cred = (0.1,)
    bikers_beliefunit._world_agenda_debt = (0.2,)
    bikers_beliefunit.set_personlink(personlink=todd_person)
    bikers_beliefunit.set_personlink(personlink=mery_person)
    print(f"{bikers_beliefunit}")
    biker_personlink_todd = bikers_beliefunit._persons.get(todd_text)
    assert biker_personlink_todd._world_cred == 0.13
    assert biker_personlink_todd._world_debt == 0.7
    assert biker_personlink_todd._world_agenda_cred == 0.53
    assert biker_personlink_todd._world_agenda_debt == 0.77

    biker_personlink_mery = bikers_beliefunit._persons.get(mery_text)
    assert biker_personlink_mery._world_cred == 0.23
    assert biker_personlink_mery._world_debt == 0.5
    assert biker_personlink_mery._world_agenda_cred == 0.54
    assert biker_personlink_mery._world_agenda_debt == 0.57

    # WHEN
    bikers_beliefunit.reset_world_cred_debt()

    # THEN
    assert biker_personlink_todd._world_cred == 0
    assert biker_personlink_todd._world_debt == 0
    assert biker_personlink_todd._world_agenda_cred == 0
    assert biker_personlink_todd._world_agenda_debt == 0
    assert biker_personlink_mery._world_cred == 0
    assert biker_personlink_mery._world_debt == 0
    assert biker_personlink_mery._world_agenda_cred == 0
    assert biker_personlink_mery._world_agenda_debt == 0


def test_personlink_meld_ReturnsCorrectObj_BaseScenario():
    # GIVEN
    todd_person = personlink_shop(person_id="Todd")
    merry_person = personlink_shop(person_id="Merry")
    bikers_belief_id = ",bikers"
    bikers_belief = beliefunit_shop(belief_id=bikers_belief_id, _persons={})
    bikers_belief.set_personlink(personlink=todd_person)
    bikers_belief.set_personlink(personlink=merry_person)

    x2_belief = beliefunit_shop(belief_id=bikers_belief_id, _persons={})

    # WHEN
    bikers_belief.meld(exterior_belief=x2_belief)
    print(f"{bikers_belief.belief_id=} {x2_belief.belief_id=}")

    # THEN
    assert len(bikers_belief._persons) == 2


def test_personlink_meld_ReturnsCorrectObj_GainScenario():
    # GIVEN
    todd_text = "Todd"
    mery_text = "Merry"
    todd_person = personlink_shop(
        person_id=todd_text, credor_weight=13, debtor_weight=7
    )
    mery_person = personlink_shop(
        person_id=mery_text, credor_weight=23, debtor_weight=5
    )
    bikers_belief_id = ",bikers"
    bikers_belief = beliefunit_shop(belief_id=bikers_belief_id, _persons={})

    x2_belief = beliefunit_shop(belief_id=bikers_belief_id, _persons={})
    x2_belief.set_personlink(personlink=todd_person)
    x2_belief.set_personlink(personlink=mery_person)

    # WHEN
    bikers_belief.meld(exterior_belief=x2_belief)

    # THEN
    assert len(bikers_belief._persons) == 2
    assert bikers_belief._persons.get(todd_text) != None
