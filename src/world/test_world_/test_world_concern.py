from src.agenda.road import get_road
from src.world.world import worldunit_shop
from src.world.concern import (
    create_cultureaddress,
    create_lobbyunit,
    create_concernunit,
)
from src.world.examples.world_env_kit import (
    get_temp_world_dir,
    get_temp_culture_id,
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
    x_world.set_personunit(luca_text)
    luca_person = x_world.get_personunit_from_memory(luca_text)
    texas_text = "Texas"
    luca_person.set_cultureunit(texas_text)
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


def test_worldunit_apply_lobbyunit_CorrectlyCreates_seed_agendas(
    worlds_dir_setup_cleanup,
):
    # GIVEN lobbyr and actor seed_agendas does not exist
    w1_text = "w1"
    x_world = worldunit_shop(w1_text, get_test_worlds_dir())
    yao_text = "Yao"
    x_world.set_personunit(yao_text)
    yao_person = x_world.get_personunit_from_memory(yao_text)
    texas_text = "Texas"
    yao_person.set_cultureunit(texas_text)
    texas_culture = yao_person.get_cultureunit(texas_text)
    texas_public_dir = texas_culture.get_public_dir()

    highway_concernunit = create_concernunit(
        cultureaddress=create_cultureaddress(yao_text, texas_text),
        action="flying in airplanes",
        positive="Do not fly",
        negative="Continue flying",
        when="global environment",
        good="healthy",
        bad="boiling",
    )
    tim_text = "Tim"
    xio_text = "Xio"
    highway_lobbyunit = create_lobbyunit(
        concernunit=highway_concernunit, actor_pid=tim_text, lobbyr_pid=xio_text
    )
    assert x_world.get_personunit_from_memory(tim_text) is None
    assert x_world.get_personunit_from_memory(xio_text) is None
    public_tim_file_path = f"{texas_public_dir}/{tim_text}.json"
    public_xio_file_path = f"{texas_public_dir}/{xio_text}.json"
    public_yao_file_path = f"{texas_public_dir}/{yao_text}.json"
    assert os_path.exists(public_tim_file_path) is False
    assert os_path.exists(public_xio_file_path) is False
    assert os_path.exists(public_yao_file_path) is False

    # WHEN
    x_world.apply_lobbyunit(highway_lobbyunit)

    # THEN
    assert x_world.get_personunit_from_memory(tim_text) != None
    assert x_world.get_personunit_from_memory(xio_text) != None
    print(f"{public_tim_file_path=}")
    assert os_path.exists(public_tim_file_path)
    assert os_path.exists(public_xio_file_path)
    assert os_path.exists(public_yao_file_path)
    assert texas_culture.get_councilunit(tim_text).get_seed() != None
    assert texas_culture.get_councilunit(xio_text).get_seed() != None
    assert texas_culture.get_councilunit(yao_text).get_seed() != None


def test_worldunit_apply_lobbyunit_CorrectlyAddsTaskTo_lobbyr_seed_agenda(
    worlds_dir_setup_cleanup,
):
    x_world = worldunit_shop("w1", get_test_worlds_dir())
    yao_text = "Yao"
    x_world.set_personunit(yao_text)
    yao_person = x_world.get_personunit_from_memory(yao_text)
    texas_text = "Texas"
    yao_person.set_cultureunit(texas_text)
    texas_culture = yao_person.get_cultureunit(texas_text)
    texas_public_dir = texas_culture.get_public_dir()

    flying_text = "flying in airplanes"
    no_fly_text = "Do not fly"
    yesfly_text = "Continue flying"
    weather_text = "global weather"
    healthy_text = "healthy"
    boiling_text = "boiling"

    highway_concernunit = create_concernunit(
        cultureaddress=create_cultureaddress(yao_text, texas_text),
        action=flying_text,
        positive=no_fly_text,
        negative=yesfly_text,
        when=weather_text,
        good=healthy_text,
        bad=boiling_text,
    )
    tim_text = "Tim"
    xio_text = "Xio"
    highway_lobbyunit = create_lobbyunit(
        concernunit=highway_concernunit, actor_pid=tim_text, lobbyr_pid=xio_text
    )

    # WHEN
    x_world.apply_lobbyunit(highway_lobbyunit)

    # THEN
    tim_seed = texas_culture.get_councilunit(tim_text).get_seed()
    xio_seed = texas_culture.get_councilunit(xio_text).get_seed()
    yao_seed = texas_culture.get_councilunit(yao_text).get_seed()
    texas_road = get_road(texas_culture.set_culture_id, texas_text)
    flying_road = get_road(texas_road, flying_text)
    no_fly_road = get_road(flying_road, no_fly_text)
    yesfly_road = get_road(flying_road, yesfly_text)
    weather_road = get_road(texas_road, weather_text)
    healthy_road = get_road(weather_road, healthy_text)
    boiling_road = get_road(weather_road, boiling_text)
    # assert tim_seed.get_idea_kid() != None
    # assert xio_seed. != None
    # assert yao_seed. != None
    assert 1 == 2


# def test_worldunit_apply_lobbyunit_CorrectlyAddsTaskTo_intent(worlds_dir_setup_cleanup):
#     # GIVEN actors public_agenda intent is empty
#     # WHEN worldunit lobbyunit is applyed
#     # THEN actors public_agenda intent is non-empty
#     assert 1 == 2
