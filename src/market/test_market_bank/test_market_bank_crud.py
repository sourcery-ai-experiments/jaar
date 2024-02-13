from src.agenda.agenda import agendaunit_shop
from src.market.market import marketunit_shop
from src.market.examples.market_env_kit import (
    get_temp_env_market_id,
    get_test_markets_dir,
    env_dir_setup_cleanup,
)
from src.market.bank_sqlstr import get_agendabankunits_dict


def test_market_bank_get_agendaunits_ReturnsCorrectEmptyObj(env_dir_setup_cleanup):
    # GIVEN
    market_id = get_temp_env_market_id()
    x_market = marketunit_shop(market_id, get_test_markets_dir())
    x_market.create_dirs_if_null(in_memory_bank=True)
    x_market.refresh_bank_forum_agendas_data()

    # WHEN
    x_agendabankunits = get_agendabankunits_dict(x_market.get_bank_conn())

    # THEN
    assert len(x_agendabankunits) == 0


def test_market_bank_get_agendaunits_ReturnsCorrectNoneObj(env_dir_setup_cleanup):
    # GIVEN
    market_id = get_temp_env_market_id()
    x_market = marketunit_shop(market_id, get_test_markets_dir())
    x_market.create_dirs_if_null(in_memory_bank=True)
    x_market.refresh_bank_forum_agendas_data()
    assert len(get_agendabankunits_dict(x_market.get_bank_conn())) == 0

    # WHEN
    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"
    x_market.save_forum_agenda(agendaunit_shop(_agent_id=sal_text))
    x_market.save_forum_agenda(agendaunit_shop(_agent_id=bob_text))
    x_market.save_forum_agenda(agendaunit_shop(_agent_id=tom_text))
    x_market.save_forum_agenda(agendaunit_shop(_agent_id=ava_text))
    x_market.save_forum_agenda(agendaunit_shop(_agent_id=elu_text))
    x_market.refresh_bank_forum_agendas_data()
    x_agendabankunits = get_agendabankunits_dict(x_market.get_bank_conn())

    # THEN
    assert len(x_agendabankunits) == 5
    assert x_agendabankunits.get(sal_text) != None
    assert x_agendabankunits.get(bob_text) != None
    assert x_agendabankunits.get(tom_text) != None
    assert x_agendabankunits.get(ava_text) != None
    assert x_agendabankunits.get(elu_text) != None
    assert x_agendabankunits.get(sal_text).agent_id == sal_text
    assert x_agendabankunits.get(bob_text).agent_id == bob_text
    assert x_agendabankunits.get(tom_text).agent_id == tom_text
    assert x_agendabankunits.get(ava_text).agent_id == ava_text
    assert x_agendabankunits.get(elu_text).agent_id == elu_text
    print(f"{x_agendabankunits.get(sal_text)=}")
    print(f"{x_agendabankunits.get(bob_text)=}")
    print(f"{x_agendabankunits.get(tom_text)=}")
    print(f"{x_agendabankunits.get(ava_text)=}")
    print(f"{x_agendabankunits.get(elu_text)=}")
    assert x_agendabankunits.get(sal_text).rational is None
    assert x_agendabankunits.get(bob_text).rational is None
    assert x_agendabankunits.get(tom_text).rational is None
    assert x_agendabankunits.get(ava_text).rational is None
    assert x_agendabankunits.get(elu_text).rational is None


def test_market_bank_bank_set_agendaunit_attrs_CorrectlyUpdatesRecord(
    env_dir_setup_cleanup,
):
    # GIVEN
    market_id = get_temp_env_market_id()
    x_market = marketunit_shop(market_id, get_test_markets_dir())
    x_market.create_dirs_if_null(in_memory_bank=True)
    x_market.refresh_bank_forum_agendas_data()
    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"
    sal_agenda = agendaunit_shop(_agent_id=sal_text)
    bob_agenda = agendaunit_shop(_agent_id=bob_text)
    tom_agenda = agendaunit_shop(_agent_id=tom_text)
    ava_agenda = agendaunit_shop(_agent_id=ava_text)
    elu_agenda = agendaunit_shop(_agent_id=elu_text)
    x_market.save_forum_agenda(sal_agenda)
    x_market.save_forum_agenda(bob_agenda)
    x_market.save_forum_agenda(tom_agenda)
    x_market.save_forum_agenda(ava_agenda)
    x_market.save_forum_agenda(elu_agenda)
    x_market.refresh_bank_forum_agendas_data()
    x_agendabankunits = get_agendabankunits_dict(x_market.get_bank_conn())
    assert x_agendabankunits.get(sal_text).rational is None
    assert x_agendabankunits.get(bob_text).rational is None

    # WHEN
    sal_agenda.set_agenda_metrics()
    bob_rational = False
    bob_agenda._rational = bob_rational
    x_market._bank_set_agendaunit_attrs(sal_agenda)
    x_market._bank_set_agendaunit_attrs(bob_agenda)

    # THEN
    x_agendabankunits = get_agendabankunits_dict(x_market.get_bank_conn())
    print(f"{x_agendabankunits.get(sal_text)=}")
    print(f"{x_agendabankunits.get(bob_text)=}")
    print(f"{x_agendabankunits.get(tom_text)=}")
    print(f"{x_agendabankunits.get(ava_text)=}")
    print(f"{x_agendabankunits.get(elu_text)=}")
    assert x_agendabankunits.get(sal_text).rational
    assert x_agendabankunits.get(bob_text).rational == bob_rational
