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
    get_temp_env_handle,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from src.culture.bank_sqlstr import (
    get_agendaunits_select_sqlstr,
    get_agendabankunits_dict,
)


def test_get_file_names_in_voice_rank_order_GetsCorrectFileOrder(env_dir_setup_cleanup):
    # GIVEN
    temp_dir = f"{get_test_cultures_dir()}/ex7"
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
    ava_partyunit = partyunit_shop(title=ava_text)
    bob_partyunit = partyunit_shop(title=bob_text)
    cal_partyunit = partyunit_shop(title=cal_text)
    dom_partyunit = partyunit_shop(title=dom_text)
    elu_partyunit = partyunit_shop(title=elu_text)

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
    for file_name in x1:
        print(f"{file_name=}")
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
    x_culture = cultureunit_shop(get_temp_env_handle(), get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)
    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"
    x_culture._manager_name = sal_text
    x_culture.create_new_kitchenunit()
    x_culture.save_public_agenda(agendaunit_shop(_healer=sal_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=bob_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=tom_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=ava_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=elu_text))
    x_culture.refresh_bank_agenda_data()
    x_agendabankunits = get_agendabankunits_dict(x_culture.get_bank_conn())
    old_sal_voice_rank = -10
    old_bob_voice_rank = -45
    old_tom_voice_rank = -13
    old_ava_voice_rank = 3
    old_elu_voice_rank = 4
    x_culture._bank_set_agendaunit_attrs(sal_text, voice_rank=old_sal_voice_rank)
    x_culture._bank_set_agendaunit_attrs(bob_text, voice_rank=old_bob_voice_rank)
    x_culture._bank_set_agendaunit_attrs(tom_text, voice_rank=old_tom_voice_rank)
    x_culture._bank_set_agendaunit_attrs(ava_text, voice_rank=old_ava_voice_rank)
    x_culture._bank_set_agendaunit_attrs(elu_text, voice_rank=old_elu_voice_rank)
    x_agendabankunits = get_agendabankunits_dict(x_culture.get_bank_conn())
    assert x_agendabankunits.get(sal_text).voice_rank == old_sal_voice_rank
    assert x_agendabankunits.get(bob_text).voice_rank == old_bob_voice_rank
    assert x_agendabankunits.get(tom_text).voice_rank == old_tom_voice_rank
    assert x_agendabankunits.get(ava_text).voice_rank == old_ava_voice_rank
    assert x_agendabankunits.get(elu_text).voice_rank == old_elu_voice_rank

    # WHEN
    x_culture.set_manager_voice_ranks(sort_order="arbitrary")

    # THEN
    x_agendabankunits = get_agendabankunits_dict(x_culture.get_bank_conn())
    print(f"{x_agendabankunits.get(sal_text)=}")
    print(f"{x_agendabankunits.get(bob_text)=}")
    print(f"{x_agendabankunits.get(tom_text)=}")
    print(f"{x_agendabankunits.get(ava_text)=}")
    print(f"{x_agendabankunits.get(elu_text)=}")
    new_sal_voice_rank = 3
    new_bob_voice_rank = 1
    new_tom_voice_rank = 4
    new_ava_voice_rank = 0
    new_elu_voice_rank = 2
    assert x_agendabankunits.get(sal_text).voice_rank == new_sal_voice_rank
    assert x_agendabankunits.get(bob_text).voice_rank == new_bob_voice_rank
    assert x_agendabankunits.get(tom_text).voice_rank == new_tom_voice_rank
    assert x_agendabankunits.get(ava_text).voice_rank == new_ava_voice_rank
    assert x_agendabankunits.get(elu_text).voice_rank == new_elu_voice_rank
