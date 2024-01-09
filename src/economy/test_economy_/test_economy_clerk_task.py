from src._prime.road import create_road
from src.economy.economy import economyunit_shop
from src.economy.examples.economy_env_kit import (
    get_temp_env_economy_id,
    env_dir_setup_cleanup,
    get_test_economys_dir,
)
from src.economy.examples.example_clerks import (
    get_agenda_assignment_laundry_example1,
)


def test_economy_ChangingOneHealersFactChangesAnotherAgenda(env_dir_setup_cleanup):
    # GIVEN
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())
    amer_text = "Amer"
    x_economy.create_new_clerkunit(clerk_cid=amer_text)
    amer_clerk = x_economy.get_clerkunit(cid=amer_text)
    laundry_agenda = get_agenda_assignment_laundry_example1()
    laundry_agenda.set_economy_id(x_economy.economy_id)
    amer_clerk.set_contract(laundry_agenda)

    casa_text = "casa"
    basket_text = "laundry basket status"
    casa_road = x_economy.build_economy_road(casa_text)
    basket_road = create_road(casa_road, basket_text)
    # print(f"{x1_casa_road=} {basket_road=}")
    # print(f"{x1_casa_road=} {x1_basket_road=}")
    b_full_text = "full"
    b_full_road = create_road(basket_road, b_full_text)
    b_bare_text = "bare"
    b_bare_road = create_road({basket_road}, {b_bare_text})
    # set basket status to "bare"
    contract_x = amer_clerk.get_contract().set_fact(base=basket_road, pick=b_bare_road)
    amer_clerk.set_contract(contract_x)
    # save fact change to public
    amer_clerk.save_refreshed_output_to_public()
    # print(f"{x_economy.get_public_agenda(amer_text)._idearoot._factunits.keys()=}")
    amer_output = x_economy.get_public_agenda(amer_text)

    # create assignment for Cali
    cali_text = "Cali"
    x_economy.create_new_clerkunit(clerk_cid=cali_text)
    cali_clerk = x_economy.get_clerkunit(cid=cali_text)
    cali_clerk.set_depot_agenda(amer_output, "assignment")
    old_cali_agenda = x_economy.get_output_agenda(cali_text)
    # print(f"{old_cali_agenda._partys.keys()=}")
    # print(f"{old_cali_agenda._idearoot._factunits.keys()=}")
    basket_fact = old_cali_agenda._idearoot._factunits.get(basket_road)
    # print(f"Cali: {basket_fact.base=} {basket_fact.pick=}")
    assert len(old_cali_agenda.get_intent_items()) == 0

    # WHEN
    # set basket status to "full"
    amer_clerk.get_contract().set_fact(base=basket_road, pick=b_full_road)
    amer_clerk.set_contract()
    amer_clerk.save_refreshed_output_to_public()

    cali_clerk.refresh_depot_agendas()
    new_cali_agenda = cali_clerk.get_remelded_output_agenda()

    # new_public_amer = x_economy.get_public_agenda(amer_text)
    # a_basket_fact = new_public_amer._idearoot._factunits.get(basket_road)
    # print(f"Amer after when {a_basket_fact.base=} {a_basket_fact.pick=}")

    # THEN
    # print(f"{new_cali_agenda._partys.keys()=}")
    # basket_fact = new_cali_agenda._idearoot._factunits.get(basket_road)
    # print(f"{basket_fact.base=} {basket_fact.pick=}")
    # print(f"{len(new_cali_agenda._idearoot._factunits.keys())=}")
    assert len(new_cali_agenda.get_intent_items()) == 1
    laundry_task_text = "do_laundry"
    casa_road = x_economy.build_economy_road(casa_text)
    laundry_task_road = create_road(casa_road, laundry_task_text)
    assert new_cali_agenda.get_intent_items()[0].get_road() == laundry_task_road


def test_economy_clerk_MeldOrderChangesOutputFact(env_dir_setup_cleanup):
    # GIVEN
    x_economy = economyunit_shop(get_temp_env_economy_id(), get_test_economys_dir())
    amer_text = "Amer"
    beto_text = "Beto"
    x_economy.create_new_clerkunit(clerk_cid=amer_text)
    x_economy.create_new_clerkunit(clerk_cid=beto_text)
    amer_clerk = x_economy.get_clerkunit(cid=amer_text)
    beto_clerk = x_economy.get_clerkunit(cid=beto_text)
    # print(f"{beto_clerk=}")
    laundry_agenda = get_agenda_assignment_laundry_example1()
    laundry_agenda.set_economy_id(x_economy.economy_id)
    amer_clerk.set_contract(laundry_agenda)
    beto_clerk.set_contract(laundry_agenda)

    casa_text = "casa"
    casa_road = create_road(x_economy.economy_id, casa_text)
    basket_text = "laundry basket status"
    basket_road = create_road(casa_road, basket_text)
    b_full_text = "full"
    b_full_road = create_road(basket_road, b_full_text)
    b_bare_text = "bare"
    b_bare_road = create_road(basket_road, b_bare_text)

    # amer public laundry fact as "full"
    amer_contract_x = amer_clerk.get_contract().set_fact(basket_road, b_full_road)
    beto_contract_x = beto_clerk.get_contract().set_fact(basket_road, b_bare_road)

    amer_clerk.set_contract(amer_contract_x)
    beto_clerk.set_contract(beto_contract_x)
    amer_clerk.save_refreshed_output_to_public()
    beto_clerk.save_refreshed_output_to_public()
    amer_output = x_economy.get_public_agenda(amer_text)
    beto_output = x_economy.get_public_agenda(beto_text)

    cali_text = "Cali"
    x_economy.create_new_clerkunit(cali_text)
    cali_kichen = x_economy.get_clerkunit(cali_text)
    cali_kichen.set_depot_agenda(beto_output, "assignment")
    cali_kichen.set_depot_agenda(amer_output, "assignment")

    # WHEN
    cali_kichen.save_refreshed_output_to_public()

    # THEN
    old_cali_output = x_economy.get_public_agenda(cali_text)
    assert len(old_cali_output.get_intent_items()) == 0
    old_cali_facts = old_cali_output._idearoot._factunits
    # print(f"{old_cali_output._idearoot._factunits=}")
    assert old_cali_facts.get(basket_road) != None
    old_cali_basket_fact = old_cali_facts.get(basket_road)
    # print(f"{old_cali_basket_fact.base=}")
    # print(f"{old_cali_basket_fact.pick=}")
    # print(f"{old_cali_basket_fact.open=}")
    # print(f"{old_cali_basket_fact.nigh=}")
    assert old_cali_basket_fact.pick == b_bare_road

    # WHEN voice_rank is changed
    cali_contract = cali_kichen.get_contract()
    cali_amer_party = cali_contract.get_party(amer_text)
    cali_beto_party = cali_contract.get_party(beto_text)
    amer_voice_rank = 45
    beto_voice_rank = 100
    cali_amer_party.set_treasurying_data(None, None, None, voice_rank=amer_voice_rank)
    cali_beto_party.set_treasurying_data(None, None, None, voice_rank=beto_voice_rank)
    # print(f"{cali_amer_party._treasury_voice_rank=} {amer_voice_rank=}")
    # print(f"{cali_beto_party._treasury_voice_rank=} {beto_voice_rank=}")

    cali_kichen.set_contract(cali_contract)

    print("get new contract...")
    # new_cali_contract = cali_kichen.get_contract()
    # new_cali_amer_party = new_cali_contract.get_party(amer_text)
    # new_cali_beto_party = new_cali_contract.get_party(beto_text)
    # print(f"{new_cali_amer_party._treasury_voice_rank=} ")
    # print(f"{new_cali_beto_party._treasury_voice_rank=} ")

    cali_kichen.save_refreshed_output_to_public()

    # THEN final fact changed
    new_cali_output = x_economy.get_public_agenda(cali_text)
    assert len(new_cali_output.get_intent_items()) == 1
    new_cali_facts = new_cali_output._idearoot._factunits
    # print(f"{new_cali_output._idearoot._factunits=}")
    assert new_cali_facts.get(basket_road) != None
    new_cali_basket_fact = new_cali_facts.get(basket_road)
    print(f"{new_cali_basket_fact.base=}")
    print(f"{new_cali_basket_fact.pick=}")
    print(f"{new_cali_basket_fact.open=}")
    print(f"{new_cali_basket_fact.nigh=}")
    assert new_cali_basket_fact.pick == b_full_road
