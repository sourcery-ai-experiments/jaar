from src.world.world import worldunit_shop
from src.world.concern import create_cultureaddress, create_urgeunit, create_concernunit
from src.world.examples.world_env_kit import (
    get_temp_world_dir,
    get_temp_culture_qid,
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)
from os import path as os_path


def test_worldunit_add_cultural_connection_CorrectlyCreatesObj(
    worlds_dir_setup_cleanup,
):
    # GIVEN
    dallas_text = "dallas"
    x_world = worldunit_shop(mark=dallas_text, worlds_dir=get_test_worlds_dir())
    luca_text = "Lucas"
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


def test_worldunit_apply_urgeunit_CorrectlyCreates_seed_agendas(
    worlds_dir_setup_cleanup,
):
    # GIVEN urger and actor seed_agendas does not exist
    x_world = worldunit_shop(get_temp_world_dir(), get_test_worlds_dir())
    luca_text = "Tom"
    x_world.add_personunit(luca_text)
    luca_person = x_world.get_personunit_from_memory(luca_text)
    texas_text = "Texas"
    luca_person.add_cultureunit(texas_text)
    texas_culture = luca_person.get_cultureunit(texas_text)
    culture_public_dir = texas_culture.get_public_dir()
    tim_text = "Tim"
    luca_texas_cultureaddress = create_cultureaddress(luca_text, texas_text)
    highway_concernunit = create_concernunit(luca_texas_cultureaddress)
    highway_urgeunit = create_urgeunit(highway_concernunit, actor_pid=tim_text)

    public_tim_file_name = f"{tim_text}.json"
    public_tim_file_path = f"{culture_public_dir}/{public_tim_file_name}"
    print(f"{public_tim_file_path=}")
    # public_file_path = f"src/culture/examples/ex_env/agendas/{public_file_name}"
    assert os_path.exists(public_tim_file_path) is False

    # WHEN
    x_world.apply_urgeunit()

    # THEN
    assert os_path.exists(public_tim_file_path)

    # WHEN worldunit urgeunit is applyed
    # THEN seed agendas do exist
    assert 1 == 2


def test_worldunit_apply_urgeunit_CorrectlyAddsTaskTo_urger_seed_agenda(
    worlds_dir_setup_cleanup,
):
    # GIVEN urger and actor seed_agendas does not exist
    # WHEN worldunit urgeunit is applyed
    # THEN urger seed_agenda has
    assert 1 == 2


def test_worldunit_apply_urgeunit_CorrectlyAddsTaskTo_intent(worlds_dir_setup_cleanup):
    # GIVEN actors public_agenda intent is empty
    # WHEN worldunit urgeunit is applyed
    # THEN actors public_agenda intent is non-empty
    assert 1 == 2
