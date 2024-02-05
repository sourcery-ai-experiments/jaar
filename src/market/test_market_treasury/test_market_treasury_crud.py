from src.agenda.agenda import agendaunit_shop
from src.market.market import marketunit_shop
from src.market.examples.market_env_kit import (
    get_temp_env_market_id,
    get_test_markets_dir,
    env_dir_setup_cleanup,
)
from src.market.treasury_sqlstr import get_agendatreasuryunits_dict


def test_market_treasury_get_agendaunits_ReturnsCorrectEmptyObj(env_dir_setup_cleanup):
    # GIVEN
    market_id = get_temp_env_market_id()
    x_market = marketunit_shop(market_id, get_test_markets_dir())
    x_market.create_dirs_if_null(in_memory_treasury=True)
    x_market.refresh_treasury_forum_agendas_data()

    # WHEN
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_market.get_treasury_conn())

    # THEN
    assert len(x_agendatreasuryunits) == 0


def test_market_treasury_get_agendaunits_ReturnsCorrectNoneObj(env_dir_setup_cleanup):
    # GIVEN
    market_id = get_temp_env_market_id()
    x_market = marketunit_shop(market_id, get_test_markets_dir())
    x_market.create_dirs_if_null(in_memory_treasury=True)
    x_market.refresh_treasury_forum_agendas_data()
    assert len(get_agendatreasuryunits_dict(x_market.get_treasury_conn())) == 0

    # WHEN
    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"
    x_market.save_forum_agenda(agendaunit_shop(_agent_id=sal_text))
    x_market.save_forum_agenda(agendaunit_shop(_agent_id=bob_text))
    x_market.save_forum_agenda(agendaunit_shop(_agent_id=tom_text))
    x_market.save_forum_agenda(agendaunit_shop(_agent_id=ava_text))
    x_market.save_forum_agenda(agendaunit_shop(_agent_id=elu_text))
    x_market.refresh_treasury_forum_agendas_data()
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_market.get_treasury_conn())

    # THEN
    assert len(x_agendatreasuryunits) == 5
    assert x_agendatreasuryunits.get(sal_text) != None
    assert x_agendatreasuryunits.get(bob_text) != None
    assert x_agendatreasuryunits.get(tom_text) != None
    assert x_agendatreasuryunits.get(ava_text) != None
    assert x_agendatreasuryunits.get(elu_text) != None
    assert x_agendatreasuryunits.get(sal_text).agent_id == sal_text
    assert x_agendatreasuryunits.get(bob_text).agent_id == bob_text
    assert x_agendatreasuryunits.get(tom_text).agent_id == tom_text
    assert x_agendatreasuryunits.get(ava_text).agent_id == ava_text
    assert x_agendatreasuryunits.get(elu_text).agent_id == elu_text
    print(f"{x_agendatreasuryunits.get(sal_text)=}")
    print(f"{x_agendatreasuryunits.get(bob_text)=}")
    print(f"{x_agendatreasuryunits.get(tom_text)=}")
    print(f"{x_agendatreasuryunits.get(ava_text)=}")
    print(f"{x_agendatreasuryunits.get(elu_text)=}")
    assert x_agendatreasuryunits.get(sal_text).rational is None
    assert x_agendatreasuryunits.get(bob_text).rational is None
    assert x_agendatreasuryunits.get(tom_text).rational is None
    assert x_agendatreasuryunits.get(ava_text).rational is None
    assert x_agendatreasuryunits.get(elu_text).rational is None


def test_market_treasury_treasury_set_agendaunit_attrs_CorrectlyUpdatesRecord(
    env_dir_setup_cleanup,
):
    # GIVEN
    market_id = get_temp_env_market_id()
    x_market = marketunit_shop(market_id, get_test_markets_dir())
    x_market.create_dirs_if_null(in_memory_treasury=True)
    x_market.refresh_treasury_forum_agendas_data()
    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"
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
    x_market.refresh_treasury_forum_agendas_data()
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_market.get_treasury_conn())
    assert x_agendatreasuryunits.get(sal_text).rational is None
    assert x_agendatreasuryunits.get(bob_text).rational is None

    # WHEN
    sal_agenda.set_agenda_metrics()
    bob_rational = False
    bob_agenda._rational = bob_rational
    x_market._treasury_set_agendaunit_attrs(sal_agenda)
    x_market._treasury_set_agendaunit_attrs(bob_agenda)

    # THEN
    x_agendatreasuryunits = get_agendatreasuryunits_dict(x_market.get_treasury_conn())
    print(f"{x_agendatreasuryunits.get(sal_text)=}")
    print(f"{x_agendatreasuryunits.get(bob_text)=}")
    print(f"{x_agendatreasuryunits.get(tom_text)=}")
    print(f"{x_agendatreasuryunits.get(ava_text)=}")
    print(f"{x_agendatreasuryunits.get(elu_text)=}")
    assert x_agendatreasuryunits.get(sal_text).rational
    assert x_agendatreasuryunits.get(bob_text).rational == bob_rational
