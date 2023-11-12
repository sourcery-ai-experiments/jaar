from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_title,
    env_dir_setup_cleanup,
    get_test_cultures_dir,
)
from src.culture.examples.example_councils import (
    get_agenda_assignment_laundry_example1,
)


def test_culture_ChangingOneHealersFactChangesAnotherAgenda(env_dir_setup_cleanup):
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())

    # GIVEN
    amer_text = "Amer"
    x_culture.create_new_councilunit(council_cid=amer_text)
    amer_council = x_culture.get_councilunit(cid=amer_text)
    laundry_agenda = get_agenda_assignment_laundry_example1()
    laundry_agenda.set_culture_title(x_culture.title)
    amer_council.set_seed(laundry_agenda)

    casa_text = "casa"
    casa_road = f"{x_culture.title},{casa_text}"
    basket_text = "laundry basket status"
    basket_road = f"{casa_road},{basket_text}"
    b_full_text = "full"
    b_full_road = f"{basket_road},{b_full_text}"
    b_bare_text = "bare"
    b_bare_road = f"{basket_road},{b_bare_text}"
    # set basket status to "bare"
    seed_x = amer_council.get_seed().set_acptfact(base=basket_road, pick=b_bare_road)
    amer_council.set_seed(seed_x)
    # save fact change to public
    amer_council._admin.save_refreshed_output_to_public()
    # print(f"{x_culture.get_public_agenda(amer_text)._idearoot._acptfactunits.keys()=}")
    amer_output = x_culture.get_public_agenda(amer_text)

    # create assignment for Cali
    cali_text = "Cali"
    x_culture.create_new_councilunit(council_cid=cali_text)
    cali_council = x_culture.get_councilunit(cid=cali_text)
    cali_council.set_depot_agenda(amer_output, "assignment")
    old_cali_agenda = x_culture.get_output_agenda(cali_text)
    # print(f"{old_cali_agenda._partys.keys()=}")
    # print(f"{old_cali_agenda._idearoot._acptfactunits.keys()=}")
    basket_acptfact = old_cali_agenda._idearoot._acptfactunits.get(basket_road)
    # print(f"Cali: {basket_acptfact.base=} {basket_acptfact.pick=}")
    assert len(old_cali_agenda.get_intent_items()) == 0

    # WHEN
    # set basket status to "full"
    amer_council.get_seed().set_acptfact(base=basket_road, pick=b_full_road)
    amer_council.set_seed()
    amer_council._admin.save_refreshed_output_to_public()

    cali_council.refresh_depot_agendas()
    new_cali_agenda = cali_council._admin.get_remelded_output_agenda()

    # new_public_amer = x_culture.get_public_agenda(amer_text)
    # a_basket_acptfact = new_public_amer._idearoot._acptfactunits.get(basket_road)
    # print(f"Amer after when {a_basket_acptfact.base=} {a_basket_acptfact.pick=}")

    # THEN
    # print(f"{new_cali_agenda._partys.keys()=}")
    # basket_acptfact = new_cali_agenda._idearoot._acptfactunits.get(basket_road)
    # print(f"{basket_acptfact.base=} {basket_acptfact.pick=}")
    # print(f"{len(new_cali_agenda._idearoot._acptfactunits.keys())=}")
    assert len(new_cali_agenda.get_intent_items()) == 1
    laundry_task_text = "do_laundry"
    laundry_task_road = f"{casa_road},{laundry_task_text}"
    assert new_cali_agenda.get_intent_items()[0].get_road() == laundry_task_road


def test_culture_council_MeldOrderChangesOutputAcptFact(env_dir_setup_cleanup):
    # GIVEN
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())
    amer_text = "Amer"
    beto_text = "Beto"
    x_culture.create_new_councilunit(council_cid=amer_text)
    x_culture.create_new_councilunit(council_cid=beto_text)
    amer_council = x_culture.get_councilunit(cid=amer_text)
    beto_council = x_culture.get_councilunit(cid=beto_text)
    # print(f"{beto_council=}")
    laundry_agenda = get_agenda_assignment_laundry_example1()
    laundry_agenda.set_culture_title(x_culture.title)
    amer_council.set_seed(laundry_agenda)
    beto_council.set_seed(laundry_agenda)

    casa_text = "casa"
    casa_road = f"{x_culture.title},{casa_text}"
    basket_text = "laundry basket status"
    basket_road = f"{casa_road},{basket_text}"
    b_full_text = "full"
    b_full_road = f"{basket_road},{b_full_text}"
    b_bare_text = "bare"
    b_bare_road = f"{basket_road},{b_bare_text}"

    # amer public laundry acptfact as "full"
    amer_seed_x = amer_council.get_seed().set_acptfact(basket_road, b_full_road)
    beto_seed_x = beto_council.get_seed().set_acptfact(basket_road, b_bare_road)

    amer_council.set_seed(amer_seed_x)
    beto_council.set_seed(beto_seed_x)
    amer_council._admin.save_refreshed_output_to_public()
    beto_council._admin.save_refreshed_output_to_public()
    amer_output = x_culture.get_public_agenda(amer_text)
    beto_output = x_culture.get_public_agenda(beto_text)

    cali_text = "Cali"
    x_culture.create_new_councilunit(cali_text)
    cali_kichen = x_culture.get_councilunit(cali_text)
    cali_kichen.set_depot_agenda(beto_output, "assignment")
    cali_kichen.set_depot_agenda(amer_output, "assignment")

    # WHEN
    cali_kichen._admin.save_refreshed_output_to_public()

    # THEN
    old_cali_output = x_culture.get_public_agenda(cali_text)
    assert len(old_cali_output.get_intent_items()) == 0
    old_cali_acptfacts = old_cali_output._idearoot._acptfactunits
    # print(f"{old_cali_output._idearoot._acptfactunits=}")
    assert old_cali_acptfacts.get(basket_road) != None
    old_cali_basket_acptfact = old_cali_acptfacts.get(basket_road)
    # print(f"{old_cali_basket_acptfact.base=}")
    # print(f"{old_cali_basket_acptfact.pick=}")
    # print(f"{old_cali_basket_acptfact.open=}")
    # print(f"{old_cali_basket_acptfact.nigh=}")
    assert old_cali_basket_acptfact.pick == b_bare_road

    # WHEN voice_rank is changed
    cali_seed = cali_kichen.get_seed()
    cali_amer_party = cali_seed.get_party(amer_text)
    cali_beto_party = cali_seed.get_party(beto_text)
    amer_voice_rank = 45
    beto_voice_rank = 100
    cali_amer_party.set_banking_data(None, None, None, voice_rank=amer_voice_rank)
    cali_beto_party.set_banking_data(None, None, None, voice_rank=beto_voice_rank)
    # print(f"{cali_amer_party._bank_voice_rank=} {amer_voice_rank=}")
    # print(f"{cali_beto_party._bank_voice_rank=} {beto_voice_rank=}")

    cali_kichen.set_seed(cali_seed)

    print("get new seed...")
    # new_cali_seed = cali_kichen.get_seed()
    # new_cali_amer_party = new_cali_seed.get_party(amer_text)
    # new_cali_beto_party = new_cali_seed.get_party(beto_text)
    # print(f"{new_cali_amer_party._bank_voice_rank=} ")
    # print(f"{new_cali_beto_party._bank_voice_rank=} ")

    cali_kichen._admin.save_refreshed_output_to_public()

    # THEN final acptfact changed
    new_cali_output = x_culture.get_public_agenda(cali_text)
    assert len(new_cali_output.get_intent_items()) == 1
    new_cali_acptfacts = new_cali_output._idearoot._acptfactunits
    # print(f"{new_cali_output._idearoot._acptfactunits=}")
    assert new_cali_acptfacts.get(basket_road) != None
    new_cali_basket_acptfact = new_cali_acptfacts.get(basket_road)
    print(f"{new_cali_basket_acptfact.base=}")
    print(f"{new_cali_basket_acptfact.pick=}")
    print(f"{new_cali_basket_acptfact.open=}")
    print(f"{new_cali_basket_acptfact.nigh=}")
    assert new_cali_basket_acptfact.pick == b_full_road
