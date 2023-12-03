from src.culture.culture import cultureunit_shop
from src.culture.council import councilunit_shop
from src.world.world import (
    WorldUnit,
    worldunit_shop,
    CultureAddress,
    cultureaddress_shop,
)
from src.world.examples.world_env_kit import get_test_worlds_dir
from src.world.person import personunit_shop
from pytest import raises as pytest_raises


def test_CultureAddress_exists():
    # GIVEN
    luca_text = "Luca"
    luca_dict = {luca_text: 0}
    texas_text = "Texas"

    # WHEN
    texas_address = CultureAddress(person_ids=luca_dict, culture_qid=texas_text)

    # THEN
    assert texas_address.culture_qid == texas_text
    assert texas_address.person_ids == luca_dict


def test_cultureaddress_shop_ReturnsCorrectObject():
    # GIVEN
    luca_text = "Luca"
    luca_dict = {luca_text: 0}
    texas_text = "Texas"

    # WHEN
    texas_address = cultureaddress_shop(person_ids=luca_dict, culture_qid=texas_text)

    # THEN
    assert texas_address.culture_qid == texas_text
    assert texas_address.person_ids == luca_dict


def test_CultureAddress_add_person_id_CorrectChangesAttribute():
    # GIVEN
    texas_text = "Texas"
    texas_address = cultureaddress_shop(culture_qid=texas_text)
    assert texas_address.person_ids == {}

    # WHEN
    luca_text = "Luca"
    texas_address.add_person_id(luca_text)

    # THEN
    luca_dict = {luca_text: 0}
    assert texas_address.person_ids == luca_dict


def test_worldunit_add_cultural_connection_CorrectlyCreatesObj():
    # GIVEN
    dallas_text = "dallas"
    x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Luca"
    x_world.add_personunit(luca_text)
    luca_person = x_world.get_personunit_from_memory(luca_text)
    texas_text = "Texas"
    luca_person.add_cultureunit(texas_text)
    texas_culture = luca_person.get_cultureunit(texas_text)
    kari_text = "kari"
    assert texas_culture._councilunits.get(kari_text) is None
    assert x_world.personunit_exists(kari_text) == False

    # WHEN
    x_world.add_cultural_connection(
        culture_person_id=luca_text, culture_qid=texas_text, council_person_id=kari_text
    )

    # THEN
    assert x_world.personunit_exists(kari_text)
    assert texas_culture._councilunits.get(kari_text) != None
