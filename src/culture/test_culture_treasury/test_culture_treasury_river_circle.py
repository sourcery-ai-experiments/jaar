from src.agenda.agenda import agendaunit_shop
from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_qid,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from src.culture.treasury_sqlstr import (
    get_river_circle_table_insert_sqlstr,
    get_river_circle_dict,
    get_river_circle_table_delete_sqlstr,
)


def test_get_river_circle_table_delete_sqlstr_CorrectlyDeletesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows
    x_culture = cultureunit_shop(get_temp_env_qid(), get_test_cultures_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(pid=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(pid=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(pid=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(bob_agenda)

    x_culture.refresh_treasury_public_agendas_data()
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text)

    with x_culture.get_treasury_conn() as treasury_conn:
        assert len(get_river_circle_dict(treasury_conn, sal_text)) > 0

    # WHEN
    sqlstr = get_river_circle_table_delete_sqlstr(sal_text)
    with x_culture.get_treasury_conn() as treasury_conn:
        treasury_conn.execute(sqlstr)

    # THEN
    with x_culture.get_treasury_conn() as treasury_conn:
        assert len(get_river_circle_dict(treasury_conn, sal_text)) == 0


def test_get_river_circle_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 ledger rows
    x_culture = cultureunit_shop(get_temp_env_qid(), get_test_cultures_dir())

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"
    elu_text = "elu"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    sal_agenda.add_partyunit(pid=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(pid=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(sal_agenda)

    bob_agenda = agendaunit_shop(_healer=bob_text)
    bob_agenda.add_partyunit(pid=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(pid=ava_text, creditor_weight=1)
    x_culture.save_public_agenda(bob_agenda)

    tom_agenda = agendaunit_shop(_healer=tom_text)
    tom_agenda.add_partyunit(pid=sal_text, creditor_weight=2)
    x_culture.save_public_agenda(tom_agenda)

    ava_agenda = agendaunit_shop(_healer=ava_text)
    ava_agenda.add_partyunit(pid=elu_text, creditor_weight=2)
    x_culture.save_public_agenda(ava_agenda)

    elu_agenda = agendaunit_shop(_healer=elu_text)
    elu_agenda.add_partyunit(pid=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(pid=sal_text, creditor_weight=1)
    x_culture.save_public_agenda(elu_agenda)

    x_culture.refresh_treasury_public_agendas_data()
    x_culture.set_credit_flow_for_agenda(agenda_healer=sal_text, max_blocks_count=100)
    with x_culture.get_treasury_conn() as treasury_conn:
        treasury_conn.execute(get_river_circle_table_delete_sqlstr(sal_text))
        assert (
            len(get_river_circle_dict(treasury_conn, currency_agenda_healer=sal_text))
            == 0
        )

    # WHEN / THEN
    mstr_sqlstr = get_river_circle_table_insert_sqlstr(currency_agenda_healer=sal_text)
    with x_culture.get_treasury_conn() as treasury_conn:
        print(mstr_sqlstr)
        treasury_conn.execute(mstr_sqlstr)
        # river_blocks = get_river_block_dict(treasury_conn, currency_agenda_healer=sal_text)
        # for river_block in river_blocks.values():
        #     print(f"{river_block=}")

    # THEN
    with x_culture.get_treasury_conn() as treasury_conn:
        river_circles = get_river_circle_dict(
            treasury_conn, currency_agenda_healer=sal_text
        )
        # for river_circle in river_circles.values():
        #     print(f"huh {river_circle=}")

    assert len(river_circles) == 2
    # for river_circle in river_circles:
    #     print(f"{river_circle=}")

    circle_0 = river_circles[0]
    assert circle_0.currency_master == sal_text
    assert circle_0.dst_healer == sal_text
    assert circle_0.circle_num == 0
    assert circle_0.curr_start == 0.04401266686517654
    assert circle_0.curr_close == 0.1

    circle_1 = river_circles[1]
    assert circle_1.currency_master == sal_text
    assert circle_1.dst_healer == sal_text
    assert circle_1.circle_num == 1
    assert circle_1.curr_start == 0.12316456150798766
    assert circle_1.curr_close == 1.0

    # for value in river_circles.values():
    #     assert value.currency_master == sal_text
    #     assert value.dst_healer == sal_text
    #     assert value.circle_num in [0, 1]
    #     assert value.curr_start in [0.12316456150798766, 0.04401266686517654]
    #     assert value.curr_close in [0.1, 1.0]
