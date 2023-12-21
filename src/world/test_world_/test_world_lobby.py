from src.agenda.road import get_road
from src.agenda.required_idea import acptfactunit_shop
from src.world.world import worldunit_shop
from src.world.lobby import (
    create_economyaddress,
    create_lobbyunit,
    create_concernunit,
)
from src.world.examples.world_env_kit import (
    get_temp_world_dir,
    get_temp_economy_id,
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
    luca_person.set_economyunit(texas_text)
    texas_economy = luca_person.get_economyunit(texas_text)
    kari_text = "kari"
    texas_economyaddress = create_economyaddress(luca_text, texas_text)
    assert texas_economy._councilunits.get(kari_text) is None
    assert x_world.personunit_exists(kari_text) == False

    # WHEN
    x_world.add_cultural_connection(texas_economyaddress, kari_text)

    # THEN
    assert x_world.personunit_exists(kari_text)
    assert texas_economy._councilunits.get(kari_text) != None


def test_worldunit_apply_lobbyunit_CorrectlyCreates_seed_agendas(
    worlds_dir_setup_cleanup,
):
    # GIVEN lobbyer and lobbyee seed_agendas does not exist
    w1_text = "w1"
    x_world = worldunit_shop(w1_text, get_test_worlds_dir())
    yao_text = "Yao"
    x_world.set_personunit(yao_text)
    yao_person = x_world.get_personunit_from_memory(yao_text)
    texas_text = "Texas"
    yao_person.set_economyunit(texas_text)
    texas_economy = yao_person.get_economyunit(texas_text)
    texas_public_dir = texas_economy.get_public_dir()

    highway_concernunit = create_concernunit(
        economyaddress=create_economyaddress(yao_text, texas_text),
        action="flying in airplanes",
        positive="Do not fly",
        negative="Continue flying",
        reason="global environment",
        good="healthy",
        bad="boiling",
    )
    tim_text = "Tim"
    xio_text = "Xio"
    highway_lobbyunit = create_lobbyunit(
        concernunit=highway_concernunit, lobbyee_pid=tim_text, lobbyer_pid=xio_text
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
    assert texas_economy.get_councilunit(tim_text).get_seed() != None
    assert texas_economy.get_councilunit(xio_text).get_seed() != None
    assert texas_economy.get_councilunit(yao_text).get_seed() != None


def test_worldunit_apply_lobbyunit_CorrectlyAddsTaskTo_lobbyer_seed_agenda(
    worlds_dir_setup_cleanup,
):
    x_world = worldunit_shop("w1", get_test_worlds_dir())
    yao_text = "Yao"
    x_world.set_personunit(yao_text)
    yao_person = x_world.get_personunit_from_memory(yao_text)
    texas_text = "Texas"
    yao_person.set_economyunit(texas_text)
    texas_economy = yao_person.get_economyunit(texas_text)

    flying_text = "flying in airplanes"
    no_fly_text = "Do not fly"
    yesfly_text = "Continue flying"
    weather_text = "global weather"
    healthy_text = "healthy"
    boiling_text = "boiling"

    highway_concernunit = create_concernunit(
        economyaddress=create_economyaddress(yao_text, texas_text),
        action=flying_text,
        positive=no_fly_text,
        negative=yesfly_text,
        reason=weather_text,
        good=healthy_text,
        bad=boiling_text,
    )
    tim_text = "Tim"
    xio_text = "Xio"
    action_weight = 7
    highway_lobbyunit = create_lobbyunit(
        concernunit=highway_concernunit,
        lobbyee_pid=tim_text,
        lobbyer_pid=xio_text,
        action_weight=action_weight,
    )

    # WHEN
    x_world.apply_lobbyunit(highway_lobbyunit)

    # THEN
    xio_seed = texas_economy.get_councilunit(xio_text).get_seed()
    xio_partyunit = xio_seed.get_party(xio_text)
    tim_partyunit = xio_seed.get_party(tim_text)
    assert xio_partyunit != None
    assert tim_partyunit != None
    assert tim_partyunit.creditor_weight == 1
    assert tim_partyunit.debtor_weight == 1
    flying_road = get_road(texas_economy.economy_id, flying_text)
    no_fly_road = get_road(flying_road, no_fly_text)
    yesfly_road = get_road(flying_road, yesfly_text)
    weather_road = get_road(texas_economy.economy_id, weather_text)
    healthy_road = get_road(weather_road, healthy_text)
    boiling_road = get_road(weather_road, boiling_text)
    print(f"{xio_seed._idea_dict.keys()=}")
    print(f"{flying_road=}")
    print(f"{no_fly_road=}")
    flying_idea = xio_seed.get_idea_kid(flying_road)
    no_fly_idea = xio_seed.get_idea_kid(no_fly_road)
    yesfly_idea = xio_seed.get_idea_kid(yesfly_road)
    weather_idea = xio_seed.get_idea_kid(weather_road)
    healthy_idea = xio_seed.get_idea_kid(healthy_road)
    boiling_idea = xio_seed.get_idea_kid(boiling_road)
    assert flying_idea != None
    assert no_fly_idea != None
    assert yesfly_idea != None
    assert weather_idea != None
    assert healthy_idea != None
    assert boiling_idea != None

    assert flying_idea.promise == False
    assert no_fly_idea.promise
    assert yesfly_idea.promise == False
    assert weather_idea.promise == False
    assert healthy_idea.promise == False
    assert boiling_idea.promise == False

    assert len(flying_idea._requiredunits) == 0
    assert len(no_fly_idea._requiredunits) == 1
    assert len(yesfly_idea._requiredunits) == 0
    assert len(weather_idea._requiredunits) == 0
    assert len(healthy_idea._requiredunits) == 0
    assert len(boiling_idea._requiredunits) == 0

    assert no_fly_idea._requiredunits.get(weather_road) != None
    weather_requiredunit = no_fly_idea._requiredunits.get(weather_road)
    assert len(weather_requiredunit.sufffacts) == 1
    assert weather_requiredunit.sufffacts.get(boiling_road) != None

    assert flying_idea._weight == 1
    assert no_fly_idea._weight != 1
    assert no_fly_idea._weight == action_weight
    assert yesfly_idea._weight == 1
    assert weather_idea._weight == 1
    assert healthy_idea._weight == 1
    assert boiling_idea._weight == 1

    assert flying_idea._assignedunit._suffgroups.get(tim_text) != None
    assert no_fly_idea._assignedunit._suffgroups.get(tim_text) != None
    assert yesfly_idea._assignedunit._suffgroups.get(tim_text) != None
    assert weather_idea._assignedunit._suffgroups.get(tim_text) != None
    assert healthy_idea._assignedunit._suffgroups.get(tim_text) != None
    assert boiling_idea._assignedunit._suffgroups.get(tim_text) != None

    assert flying_idea._balancelinks.get(tim_text) != None
    assert no_fly_idea._balancelinks.get(tim_text) != None
    assert yesfly_idea._balancelinks.get(tim_text) != None
    assert weather_idea._balancelinks.get(tim_text) != None
    assert healthy_idea._balancelinks.get(tim_text) != None
    assert boiling_idea._balancelinks.get(tim_text) != None

    xio_acptfactunits = xio_seed._idearoot._acptfactunits
    assert len(xio_acptfactunits) == 1
    static_weather_acptfactunit = acptfactunit_shop(weather_road, pick=boiling_road)
    assert xio_acptfactunits.get(weather_road) == static_weather_acptfactunit
    assert len(xio_seed.get_intent_items()) == 0

    # check tim seed
    tim_seed = texas_economy.get_councilunit(tim_text).get_seed()
    assert tim_seed.get_party(xio_text) != None
    assert tim_seed.get_party(xio_text).debtor_weight == 7
    # check tim public
    tim_public = texas_economy.get_public_agenda(tim_text)
    assert len(tim_public.get_intent_items()) == 1
    assert tim_public.get_intent_items()[0].get_idea_road() == no_fly_road


# def test_worldunit_apply_lobbyunit_CorrectlyAddsTaskTo_intent(worlds_dir_setup_cleanup):
#     # GIVEN lobbyees public_agenda intent is empty
#     # WHEN worldunit lobbyunit is applyed
#     # THEN lobbyees public_agenda intent is non-empty
#     assert 1 == 2
