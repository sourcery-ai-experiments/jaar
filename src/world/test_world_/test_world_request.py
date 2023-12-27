from src.agenda.road import create_road
from src.agenda.required_idea import acptfactunit_shop
from src.world.world import worldunit_shop
from src.world.request import (
    create_economyaddress,
    create_requestunit,
    create_concernunit,
)
from src.world.examples.world_env_kit import (
    get_temp_world_dir,
    get_temp_economy_id,
    get_test_worlds_dir,
    worlds_dir_setup_cleanup,
)
from os import path as os_path


def test_worldunit_add_economy_connection_CorrectlyCreatesObj(
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
    assert texas_economy._clerkunits.get(kari_text) is None
    assert x_world.personunit_exists(kari_text) == False

    # WHEN
    x_world.add_economy_connection(texas_economyaddress, kari_text)

    # THEN
    assert x_world.personunit_exists(kari_text)
    assert texas_economy._clerkunits.get(kari_text) != None


def test_worldunit_apply_requestunit_CorrectlyCreates_contract_agendas(
    worlds_dir_setup_cleanup,
):
    # GIVEN requester and requestee contract_agendas does not exist
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
    highway_requestunit = create_requestunit(
        concernunit=highway_concernunit, requestee_pid=tim_text, requester_pid=xio_text
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
    x_world.apply_requestunit(highway_requestunit)

    # THEN
    assert x_world.get_personunit_from_memory(tim_text) != None
    assert x_world.get_personunit_from_memory(xio_text) != None
    print(f"{public_tim_file_path=}")
    assert os_path.exists(public_tim_file_path)
    assert os_path.exists(public_xio_file_path)
    assert os_path.exists(public_yao_file_path)
    assert texas_economy.get_clerkunit(tim_text).get_contract() != None
    assert texas_economy.get_clerkunit(xio_text).get_contract() != None
    assert texas_economy.get_clerkunit(yao_text).get_contract() != None


def test_worldunit_apply_requestunit_CorrectlyAddsTaskTo_requester_contract_agenda(
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
    highway_requestunit = create_requestunit(
        concernunit=highway_concernunit,
        requestee_pid=tim_text,
        requester_pid=xio_text,
        action_weight=action_weight,
    )

    # WHEN
    x_world.apply_requestunit(highway_requestunit)

    # THEN
    xio_contract = texas_economy.get_clerkunit(xio_text).get_contract()
    xio_partyunit = xio_contract.get_party(xio_text)
    tim_partyunit = xio_contract.get_party(tim_text)
    assert xio_partyunit != None
    assert tim_partyunit != None
    assert tim_partyunit.creditor_weight == 1
    assert tim_partyunit.debtor_weight == 1
    flying_road = create_road(texas_economy.economy_id, flying_text)
    no_fly_road = create_road(flying_road, no_fly_text)
    yesfly_road = create_road(flying_road, yesfly_text)
    weather_road = create_road(texas_economy.economy_id, weather_text)
    healthy_road = create_road(weather_road, healthy_text)
    boiling_road = create_road(weather_road, boiling_text)
    print(f"{xio_contract._idea_dict.keys()=}")
    print(f"{flying_road=}")
    print(f"{no_fly_road=}")
    flying_idea = xio_contract.get_idea_kid(flying_road)
    no_fly_idea = xio_contract.get_idea_kid(no_fly_road)
    yesfly_idea = xio_contract.get_idea_kid(yesfly_road)
    weather_idea = xio_contract.get_idea_kid(weather_road)
    healthy_idea = xio_contract.get_idea_kid(healthy_road)
    boiling_idea = xio_contract.get_idea_kid(boiling_road)
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

    assert flying_idea._assignedunit.get_suffgroup(tim_text) != None
    assert no_fly_idea._assignedunit.get_suffgroup(tim_text) != None
    assert yesfly_idea._assignedunit.get_suffgroup(tim_text) != None
    assert weather_idea._assignedunit.get_suffgroup(tim_text) != None
    assert healthy_idea._assignedunit.get_suffgroup(tim_text) != None
    assert boiling_idea._assignedunit.get_suffgroup(tim_text) != None

    assert flying_idea._balancelinks.get(tim_text) != None
    assert no_fly_idea._balancelinks.get(tim_text) != None
    assert yesfly_idea._balancelinks.get(tim_text) != None
    assert weather_idea._balancelinks.get(tim_text) != None
    assert healthy_idea._balancelinks.get(tim_text) != None
    assert boiling_idea._balancelinks.get(tim_text) != None

    xio_acptfactunits = xio_contract._idearoot._acptfactunits
    assert len(xio_acptfactunits) == 1
    static_weather_acptfactunit = acptfactunit_shop(weather_road, pick=boiling_road)
    assert xio_acptfactunits.get(weather_road) == static_weather_acptfactunit
    assert len(xio_contract.get_intent_items()) == 0

    # check tim contract
    tim_contract = texas_economy.get_clerkunit(tim_text).get_contract()
    assert tim_contract.get_party(xio_text) != None
    assert tim_contract.get_party(xio_text).debtor_weight == 7
    # check tim public
    tim_public = texas_economy.get_public_agenda(tim_text)
    assert len(tim_public.get_intent_items()) == 1
    assert tim_public.get_intent_items()[0].get_road() == no_fly_road


def test_worldunit_apply_requestunit_CorrectlyAppliesGroup(worlds_dir_setup_cleanup):
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
    environmentalist_text = "Environmentalist"
    action_weight = 7
    highway_requestunit = create_requestunit(
        concernunit=highway_concernunit,
        requestee_pid=tim_text,
        requestee_group=environmentalist_text,
        requester_pid=xio_text,
        action_weight=action_weight,
    )

    # WHEN
    x_world.apply_requestunit(highway_requestunit)

    # THEN
    xio_contract = texas_economy.get_clerkunit(xio_text).get_contract()
    xio_partyunit = xio_contract.get_party(xio_text)
    tim_partyunit = xio_contract.get_party(tim_text)
    assert xio_partyunit != None
    assert tim_partyunit != None
    assert tim_partyunit.creditor_weight == 1
    assert tim_partyunit.debtor_weight == 1
    assert xio_contract._groups.get(environmentalist_text) != None
    environmentalist_group = xio_contract.get_groupunit(environmentalist_text)
    assert len(environmentalist_group._partys) == 1
    assert environmentalist_group.get_partylink(tim_text) != None

    flying_road = create_road(texas_economy.economy_id, flying_text)
    no_fly_road = create_road(flying_road, no_fly_text)
    yesfly_road = create_road(flying_road, yesfly_text)
    weather_road = create_road(texas_economy.economy_id, weather_text)
    healthy_road = create_road(weather_road, healthy_text)
    boiling_road = create_road(weather_road, boiling_text)
    flying_idea = xio_contract.get_idea_kid(flying_road)
    no_fly_idea = xio_contract.get_idea_kid(no_fly_road)
    yesfly_idea = xio_contract.get_idea_kid(yesfly_road)
    weather_idea = xio_contract.get_idea_kid(weather_road)
    healthy_idea = xio_contract.get_idea_kid(healthy_road)
    boiling_idea = xio_contract.get_idea_kid(boiling_road)

    assert flying_idea._assignedunit.get_suffgroup(tim_text) is None
    assert no_fly_idea._assignedunit.get_suffgroup(tim_text) is None
    assert yesfly_idea._assignedunit.get_suffgroup(tim_text) is None
    assert weather_idea._assignedunit.get_suffgroup(tim_text) is None
    assert healthy_idea._assignedunit.get_suffgroup(tim_text) is None
    assert boiling_idea._assignedunit.get_suffgroup(tim_text) is None

    assert flying_idea._assignedunit.get_suffgroup(environmentalist_text) != None
    assert no_fly_idea._assignedunit.get_suffgroup(environmentalist_text) != None
    assert yesfly_idea._assignedunit.get_suffgroup(environmentalist_text) != None
    assert weather_idea._assignedunit.get_suffgroup(environmentalist_text) != None
    assert healthy_idea._assignedunit.get_suffgroup(environmentalist_text) != None
    assert boiling_idea._assignedunit.get_suffgroup(environmentalist_text) != None

    xio_acptfactunits = xio_contract._idearoot._acptfactunits
    assert len(xio_acptfactunits) == 1
    static_weather_acptfactunit = acptfactunit_shop(weather_road, pick=boiling_road)
    assert xio_acptfactunits.get(weather_road) == static_weather_acptfactunit
    assert len(xio_contract.get_intent_items()) == 0

    # check tim contract
    tim_contract = texas_economy.get_clerkunit(tim_text).get_contract()
    assert tim_contract.get_party(xio_text) != None
    assert tim_contract.get_party(xio_text).debtor_weight == 7
    # check tim public
    tim_public = texas_economy.get_public_agenda(tim_text)
    assert len(tim_public.get_intent_items()) == 1
    assert tim_public.get_intent_items()[0].get_road() == no_fly_road


# def test_worldunit_apply_requestunit_Multiple_requestunitsCreateMultiple_intent_items(
#     worlds_dir_setup_cleanup,
# ):
#     x_world = worldunit_shop("w1", get_test_worlds_dir())
#     yao_text = "Yao"
#     x_world.set_personunit(yao_text)
#     yao_person = x_world.get_personunit_from_memory(yao_text)
#     texas_text = "Texas"
#     yao_person.set_economyunit(texas_text)
#     texas_economy = yao_person.get_economyunit(texas_text)

#     fly_concernunit = create_concernunit(
#         economyaddress=create_economyaddress(yao_text, texas_text),
#         action="flying in airplanes",
#         positive="Do not fly",
#         negative="Continue flying",
#         reason="global weather",
#         good="healthy",
#         bad="boiling",
#     )
#     sue_text = "Sue"
#     tim_text = "Tim"
#     xio_text = "Xio"
#     action_weight = 7
#     fly_requestunit = create_requestunit(fly_concernunit, tim_text, xio_text, action_weight)
#     fly_requestunit = create_requestunit(fly_concernunit, tim_text, xio_text, action_weight)
#     fly_requestunit = create_requestunit(fly_concernunit, yao_text, xio_text, action_weight)

#     # WHEN
#     x_world.apply_requestunit(fly_requestunit)
#     x_world.apply_requestunit(fly_requestunit)
