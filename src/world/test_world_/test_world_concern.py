from src.world.world import worldunit_shop
from src.world.concern import create_cultureaddress
from src.world.examples.world_env_kit import get_test_worlds_dir


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
    texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    assert texas_culture._councilunits.get(kari_text) is None
    assert x_world.personunit_exists(kari_text) == False

    # WHEN
    x_world.add_cultural_connection(texas_cultureaddress, kari_text)

    # THEN
    assert x_world.personunit_exists(kari_text)
    assert texas_culture._councilunits.get(kari_text) != None
