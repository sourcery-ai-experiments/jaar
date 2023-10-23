from src.agenda.agenda import agendaunit_shop
from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_handle,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from src.culture.bank_sqlstr import (
    get_agendaunit_update_sqlstr,
    get_agendaunits_select_sqlstr,
    get_agendabankunits_dict,
)


def test_culture_bank_get_agendaunits_ReturnsCorrectEmptyObj(env_dir_setup_cleanup):
    # GIVEN
    culture_handle = get_temp_env_handle()
    x_culture = cultureunit_shop(culture_handle, get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)
    x_culture.refresh_bank_agenda_data()

    # WHEN
    x_agendabankunits = get_agendabankunits_dict(x_culture.get_bank_conn())

    # THEN
    assert len(x_agendabankunits) == 0


def test_culture_bank_get_agendaunits_ReturnsCorrectNoneObj(env_dir_setup_cleanup):
    # GIVEN
    culture_handle = get_temp_env_handle()
    x_culture = cultureunit_shop(culture_handle, get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)
    x_culture.refresh_bank_agenda_data()
    assert len(get_agendabankunits_dict(x_culture.get_bank_conn())) == 0

    # WHEN
    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"
    x_culture.save_public_agenda(agendaunit_shop(_healer=sal_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=bob_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=tom_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=ava_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=elu_text))
    x_culture.refresh_bank_agenda_data()
    x_agendabankunits = get_agendabankunits_dict(x_culture.get_bank_conn())

    # THEN
    assert len(x_agendabankunits) == 5
    assert x_agendabankunits.get(sal_text) != None
    assert x_agendabankunits.get(bob_text) != None
    assert x_agendabankunits.get(tom_text) != None
    assert x_agendabankunits.get(ava_text) != None
    assert x_agendabankunits.get(elu_text) != None
    assert x_agendabankunits.get(sal_text).healer == sal_text
    assert x_agendabankunits.get(bob_text).healer == bob_text
    assert x_agendabankunits.get(tom_text).healer == tom_text
    assert x_agendabankunits.get(ava_text).healer == ava_text
    assert x_agendabankunits.get(elu_text).healer == elu_text
    print(f"{x_agendabankunits.get(sal_text)=}")
    print(f"{x_agendabankunits.get(bob_text)=}")
    print(f"{x_agendabankunits.get(tom_text)=}")
    print(f"{x_agendabankunits.get(ava_text)=}")
    print(f"{x_agendabankunits.get(elu_text)=}")


def test_culture_bank_set_single_agendaunit_voice_rank_CorrectlyUpdatesRecord(
    env_dir_setup_cleanup,
):
    # GIVEN
    culture_handle = get_temp_env_handle()
    x_culture = cultureunit_shop(culture_handle, get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)
    x_culture.refresh_bank_agenda_data()
    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"
    x_culture.save_public_agenda(agendaunit_shop(_healer=sal_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=bob_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=tom_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=ava_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=elu_text))
    x_culture.refresh_bank_agenda_data()
    x_agendabankunits = get_agendabankunits_dict(x_culture.get_bank_conn())
    assert x_agendabankunits.get(sal_text).voice_rank is None
    assert x_agendabankunits.get(bob_text).voice_rank is None

    # WHEN
    sal_voice_rank = 0
    bob_voice_rank = 1
    x_culture._set_single_agendaunit_voice_rank(sal_text, voice_rank=sal_voice_rank)
    x_culture._set_single_agendaunit_voice_rank(bob_text, voice_rank=bob_voice_rank)

    # THEN
    x_agendabankunits = get_agendabankunits_dict(x_culture.get_bank_conn())
    print(f"{x_agendabankunits.get(sal_text)=}")
    print(f"{x_agendabankunits.get(bob_text)=}")
    print(f"{x_agendabankunits.get(tom_text)=}")
    print(f"{x_agendabankunits.get(ava_text)=}")
    print(f"{x_agendabankunits.get(elu_text)=}")
    assert x_agendabankunits.get(sal_text).voice_rank == sal_voice_rank
    assert x_agendabankunits.get(bob_text).voice_rank == bob_voice_rank


def test_culture_bank_set_all_agendaunit_voice_ranks_CorrectlyUpdatesRecords(
    env_dir_setup_cleanup,
):
    # GIVEN
    culture_handle = get_temp_env_handle()
    x_culture = cultureunit_shop(culture_handle, get_test_cultures_dir())
    x_culture.create_dirs_if_null(in_memory_bank=True)
    x_culture.refresh_bank_agenda_data()
    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"
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
    x_culture._set_single_agendaunit_voice_rank(sal_text, voice_rank=old_sal_voice_rank)
    x_culture._set_single_agendaunit_voice_rank(bob_text, voice_rank=old_bob_voice_rank)
    x_culture._set_single_agendaunit_voice_rank(tom_text, voice_rank=old_tom_voice_rank)
    x_culture._set_single_agendaunit_voice_rank(ava_text, voice_rank=old_ava_voice_rank)
    x_culture._set_single_agendaunit_voice_rank(elu_text, voice_rank=old_elu_voice_rank)
    x_agendabankunits = get_agendabankunits_dict(x_culture.get_bank_conn())
    assert x_agendabankunits.get(sal_text).voice_rank == old_sal_voice_rank
    assert x_agendabankunits.get(bob_text).voice_rank == old_bob_voice_rank
    assert x_agendabankunits.get(tom_text).voice_rank == old_tom_voice_rank
    assert x_agendabankunits.get(ava_text).voice_rank == old_ava_voice_rank
    assert x_agendabankunits.get(elu_text).voice_rank == old_elu_voice_rank

    # WHEN
    x_culture.set_all_agendaunit_voice_ranks()

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
