from src.agenda.agenda import agendaunit_shop
from src.econ.econ import econunit_shop
from src.econ.examples.econ_env_kit import (
    get_temp_env_world_id,
    get_test_econ_dir,
    env_dir_setup_cleanup,
)
from src.econ.treasury_sqlstr import (
    get_river_circle_table_insert_sqlstr,
    get_river_circle_dict,
    get_river_circle_table_delete_sqlstr,
)


def test_get_river_circle_table_delete_sqlstr_CorrectlyDeletesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 Partyunits = 12 ledger rows
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.save_file_to_jobs(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.save_file_to_jobs(bob_agenda)

    x_econ.refresh_treasury_job_agendas_data()
    x_econ.set_credit_flow_for_agenda(owner_id=sal_text)

    with x_econ.get_treasury_conn() as treasury_conn:
        assert len(get_river_circle_dict(treasury_conn, sal_text)) > 0

    # WHEN
    sqlstr = get_river_circle_table_delete_sqlstr(sal_text)
    with x_econ.get_treasury_conn() as treasury_conn:
        treasury_conn.execute(sqlstr)

    # THEN
    with x_econ.get_treasury_conn() as treasury_conn:
        assert len(get_river_circle_dict(treasury_conn, sal_text)) == 0


def test_get_river_circle_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 Partyunits = 12 ledger rows
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"
    elu_text = "Elu"

    sal_agenda = agendaunit_shop(_owner_id=sal_text)
    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2)
    sal_agenda.add_partyunit(party_id=tom_text, creditor_weight=7)
    sal_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.save_file_to_jobs(sal_agenda)

    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    bob_agenda.add_partyunit(party_id=sal_text, creditor_weight=3)
    bob_agenda.add_partyunit(party_id=ava_text, creditor_weight=1)
    x_econ.save_file_to_jobs(bob_agenda)

    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    tom_agenda.add_partyunit(party_id=sal_text, creditor_weight=2)
    x_econ.save_file_to_jobs(tom_agenda)

    ava_agenda = agendaunit_shop(_owner_id=ava_text)
    ava_agenda.add_partyunit(party_id=elu_text, creditor_weight=2)
    x_econ.save_file_to_jobs(ava_agenda)

    elu_agenda = agendaunit_shop(_owner_id=elu_text)
    elu_agenda.add_partyunit(party_id=ava_text, creditor_weight=19)
    elu_agenda.add_partyunit(party_id=sal_text, creditor_weight=1)
    x_econ.save_file_to_jobs(elu_agenda)

    x_econ.refresh_treasury_job_agendas_data()
    x_econ.set_credit_flow_for_agenda(owner_id=sal_text, max_blocks_count=100)
    with x_econ.get_treasury_conn() as treasury_conn:
        treasury_conn.execute(get_river_circle_table_delete_sqlstr(sal_text))
        assert len(get_river_circle_dict(treasury_conn, cash_owner_id=sal_text)) == 0

    # WHEN / THEN
    mstr_sqlstr = get_river_circle_table_insert_sqlstr(cash_owner_id=sal_text)
    with x_econ.get_treasury_conn() as treasury_conn:
        print(mstr_sqlstr)
        treasury_conn.execute(mstr_sqlstr)
        # river_blocks = get_river_block_dict(treasury_conn, cash_owner_id=sal_text)
        # for river_block in river_blocks.values():
        #     print(f"{river_block=}")

    # THEN
    with x_econ.get_treasury_conn() as treasury_conn:
        river_circles = get_river_circle_dict(treasury_conn, cash_owner_id=sal_text)
        # for river_circle in river_circles.values():
        #     print(f"huh {river_circle=}")

    assert len(river_circles) == 2
    # for river_circle in river_circles:
    #     print(f"{river_circle=}")

    circle_0 = river_circles[0]
    assert circle_0.cash_master == sal_text
    assert circle_0.dst_owner_id == sal_text
    assert circle_0.circle_num == 0
    assert circle_0.curr_start == 0.04401266686517654
    assert circle_0.curr_close == 0.1

    circle_1 = river_circles[1]
    assert circle_1.cash_master == sal_text
    assert circle_1.dst_owner_id == sal_text
    assert circle_1.circle_num == 1
    assert circle_1.curr_start == 0.12316456150798766
    assert circle_1.curr_close == 1.0

    # for value in river_circles.values():
    #     assert value.cash_master == sal_text
    #     assert value.dst_owner_id == sal_text
    #     assert value.circle_num in [0, 1]
    #     assert value.curr_start in [0.12316456150798766, 0.04401266686517654]
    #     assert value.curr_close in [0.1, 1.0]
