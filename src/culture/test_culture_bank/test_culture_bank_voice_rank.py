from src.agenda.agenda import (
    agendaunit_shop,
    get_file_names_in_voice_rank_order,
    partyunit_shop,
)
from src.agenda.x_func import (
    save_file as x_func_save_file,
    delete_dir as x_func_delete_dir,
)
from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_title,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from src.culture.bank_sqlstr import (
    get_agendaunits_select_sqlstr,
    get_agendabankunits_dict,
)


def test_get_file_names_in_voice_rank_order_GetsCorrectFileOrder(env_dir_setup_cleanup):
    # GIVEN
    temp_dir = f"{get_test_cultures_dir()}/voice_rank_order_temp"
    print(f"{temp_dir=}")
    yao_text = "yao"

    ava_text = "ava"
    bob_text = "bob"
    cal_text = "cal"
    dom_text = "dom"
    elu_text = "elu"
    ava_filename = f"{ava_text}.json"
    bob_filename = f"{bob_text}.json"
    cal_filename = f"{cal_text}.json"
    dom_filename = f"{dom_text}.json"
    elu_filename = f"{elu_text}.json"
    empty_str = ""
    x_func_save_file(temp_dir, ava_filename, empty_str)
    x_func_save_file(temp_dir, bob_filename, empty_str)
    x_func_save_file(temp_dir, cal_filename, empty_str)
    x_func_save_file(temp_dir, dom_filename, empty_str)
    x_func_save_file(temp_dir, elu_filename, empty_str)
    ava_partyunit = partyunit_shop(handle=ava_text)
    bob_partyunit = partyunit_shop(handle=bob_text)
    cal_partyunit = partyunit_shop(handle=cal_text)
    dom_partyunit = partyunit_shop(handle=dom_text)
    elu_partyunit = partyunit_shop(handle=elu_text)

    yao_agenda = agendaunit_shop(_healer=yao_text)
    ava_partyunit.set_banking_data(None, None, None, voice_rank=33)
    bob_partyunit.set_banking_data(None, None, None, voice_rank=33)
    cal_partyunit.set_banking_data(None, None, None, voice_rank=77)
    dom_partyunit.set_banking_data(None, None, None, voice_rank=55)
    elu_partyunit.set_banking_data(None, None, None, voice_rank=99)
    yao_agenda.set_partyunit(ava_partyunit)
    yao_agenda.set_partyunit(bob_partyunit)
    yao_agenda.set_partyunit(cal_partyunit)
    yao_agenda.set_partyunit(dom_partyunit)
    yao_agenda.set_partyunit(elu_partyunit)

    x1 = get_file_names_in_voice_rank_order(yao_agenda, meldees_dir=temp_dir)
    assert x1 != None
    # for file_name in x1:
    #     print(f"{file_name=}")
    assert x1 == [
        elu_filename,
        cal_filename,
        dom_filename,
        ava_filename,
        bob_filename,
    ]
    assert ava_filename == x1[3]
    assert bob_filename == x1[4]

    # WHEN
    ava_partyunit._set_bank_voice_hx_lowest_rank(11)

    # THEN
    assert ava_partyunit._bank_voice_rank == bob_partyunit._bank_voice_rank
    assert ava_partyunit._bank_voice_hx_lowest_rank == 11
    assert bob_partyunit._bank_voice_hx_lowest_rank == 33
    x2 = get_file_names_in_voice_rank_order(yao_agenda, meldees_dir=temp_dir)
    assert ava_filename == x2[4]
    assert bob_filename == x2[3]

    x_func_delete_dir(temp_dir)


def test_culture_bank_set_manager_voice_ranks_CorrectlyUpdatesRecords_type_arbitrary(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(get_temp_env_title(), get_test_cultures_dir())
    ava_text = "ava"
    bob_text = "bob"
    cal_text = "cal"
    dom_text = "dom"
    elu_text = "elu"

    yao_text = "yao"
    yao_new_agenda = agendaunit_shop(_healer=yao_text)
    yao_new_agenda.set_partyunit(partyunit_shop(ava_text))
    yao_new_agenda.set_partyunit(partyunit_shop(bob_text))
    yao_new_agenda.set_partyunit(partyunit_shop(cal_text))
    yao_new_agenda.set_partyunit(partyunit_shop(dom_text))
    yao_new_agenda.set_partyunit(partyunit_shop(elu_text))
    x_culture.create_new_councilunit(yao_text)
    yao_council = x_culture.get_councilunit(dub=yao_text)
    yao_council.set_seed(yao_new_agenda)

    yao_seed_agenda = yao_council.get_seed()
    ava_partyunit = yao_seed_agenda.get_party(ava_text)
    bob_partyunit = yao_seed_agenda.get_party(bob_text)
    cal_partyunit = yao_seed_agenda.get_party(cal_text)
    dom_partyunit = yao_seed_agenda.get_party(dom_text)
    elu_partyunit = yao_seed_agenda.get_party(elu_text)
    assert ava_partyunit._bank_voice_rank is None
    assert bob_partyunit._bank_voice_rank is None
    assert cal_partyunit._bank_voice_rank is None
    assert dom_partyunit._bank_voice_rank is None
    assert elu_partyunit._bank_voice_rank is None

    # WHEN
    arbitrary_text = "arbitary"
    x_culture.set_voice_ranks(yao_text, sort_order=arbitrary_text)

    # THEN
    yao_public_agenda = x_culture.get_public_agenda(yao_text)
    ava_partyunit = yao_public_agenda.get_party(ava_text)
    bob_partyunit = yao_public_agenda.get_party(bob_text)
    cal_partyunit = yao_public_agenda.get_party(cal_text)
    dom_partyunit = yao_public_agenda.get_party(dom_text)
    elu_partyunit = yao_public_agenda.get_party(elu_text)
    assert ava_partyunit._bank_voice_rank != None
    assert bob_partyunit._bank_voice_rank != None
    assert cal_partyunit._bank_voice_rank != None
    assert dom_partyunit._bank_voice_rank != None
    assert elu_partyunit._bank_voice_rank != None
    assert ava_partyunit._bank_voice_rank == 0
    assert bob_partyunit._bank_voice_rank == 1
    assert cal_partyunit._bank_voice_rank == 2
    assert dom_partyunit._bank_voice_rank == 3
    assert elu_partyunit._bank_voice_rank == 4
