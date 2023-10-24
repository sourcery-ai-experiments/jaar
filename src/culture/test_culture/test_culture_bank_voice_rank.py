from src.agenda.agenda import agendaunit_shop
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


def test_culture_bank_set_manager_voice_ranks_CorrectlyUpdatesRecords_type_arbitrary(
    env_dir_setup_cleanup,
):
    # GIVEN
    culture_handle = get_temp_env_handle()
    x_culture = cultureunit_shop(culture_handle, get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)
    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"
    x_culture._manager_name = sal_text
    x_culture.refresh_bank_agenda_data()

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
