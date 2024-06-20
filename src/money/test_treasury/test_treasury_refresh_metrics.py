from src._road.road import create_road
from src.agenda.agenda import (
    agendaunit_shop,
    ideaunit_shop,
    beliefunit_shop,
    otherlink_shop,
)
from src.money.money import moneyunit_shop
from src.money.examples.econ_env import (
    temp_real_id,
    get_texas_userhub,
    env_dir_setup_cleanup,
)
from src._instrument.sqlite import get_single_result
from src.money.treasury_sqlstr import (
    get_agenda_ideaunit_row_count,
    IdeaCatalog,
    get_agenda_ideaunit_table_insert_sqlstr,
    get_agenda_ideaunit_dict,
    get_agenda_idea_factunit_row_count,
    FactCatalog,
    get_agenda_idea_factunit_table_insert_sqlstr,
    get_agenda_beliefunit_row_count,
    BeliefUnitCatalog,
    get_agenda_beliefunit_table_insert_sqlstr,
    get_agenda_beliefunit_dict,
)
from src.money.examples.example_econ_agendas import (
    get_3node_agenda,
    get_6node_agenda,
    get_agenda_3CleanNodesRandomWeights,
)
from src._instrument.sqlite import get_single_result, get_row_count_sqlstr


def test_MoneyUnit_refresh_treasury_job_agendas_data_CorrectlyDeletesOldTreasuryInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=True)

    bob_text = "Bob"
    tom_text = "Tom"

    bob_agentunit = agendaunit_shop(bob_text)
    bob_agentunit.add_otherunit(tom_text, credor_weight=3, debtor_weight=1)
    x_money.userhub.save_job_agenda(bob_agentunit)
    x_money.refresh_treasury_job_agendas_data()
    otherunit_count_sqlstr = get_row_count_sqlstr("agenda_otherunit")
    assert get_single_result(x_money.get_treasury_conn(), otherunit_count_sqlstr) == 1

    # WHEN
    x_money.refresh_treasury_job_agendas_data()

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), otherunit_count_sqlstr) == 1


def test_MoneyUnit_refresh_treasury_job_agendas_data_CorrectlyDeletesOldTreasuryFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=False)

    bob_text = "Bob"
    tom_text = "Tom"

    bob_agentunit = agendaunit_shop(bob_text)
    bob_agentunit.add_otherunit(tom_text, credor_weight=3, debtor_weight=1)
    x_money.userhub.save_job_agenda(bob_agentunit)
    x_money.refresh_treasury_job_agendas_data()
    otherunit_count_sqlstr = get_row_count_sqlstr("agenda_otherunit")
    assert get_single_result(x_money.get_treasury_conn(), otherunit_count_sqlstr) == 1

    # WHEN
    x_money.refresh_treasury_job_agendas_data()

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), otherunit_count_sqlstr) == 1


def test_MoneyUnit_refresh_treasury_job_agendas_data_CorrectlyPopulatesOtherunitTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 OtherUnits = 12 otherunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=True)

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"
    elu_text = "Elu"

    bob_agentunit = agendaunit_shop(bob_text)
    bob_agentunit.add_otherunit(tom_text, credor_weight=3, debtor_weight=1)
    bob_agentunit.add_otherunit(sal_text, credor_weight=1, debtor_weight=4)
    bob_agentunit.add_otherunit(elu_text, credor_weight=1, debtor_weight=4)
    x_money.userhub.save_job_agenda(bob_agentunit)

    sal_agentunit = agendaunit_shop(sal_text)
    sal_agentunit.add_otherunit(bob_text, credor_weight=1, debtor_weight=4)
    sal_agentunit.add_otherunit(tom_text, credor_weight=3, debtor_weight=1)
    sal_agentunit.add_otherunit(elu_text, credor_weight=1, debtor_weight=4)
    x_money.userhub.save_job_agenda(sal_agentunit)

    tom_agentunit = agendaunit_shop(tom_text)
    tom_agentunit.add_otherunit(bob_text, credor_weight=3, debtor_weight=1)
    tom_agentunit.add_otherunit(sal_text, credor_weight=1, debtor_weight=4)
    tom_agentunit.add_otherunit(elu_text, credor_weight=1, debtor_weight=4)
    x_money.userhub.save_job_agenda(tom_agentunit)

    elu_agentunit = agendaunit_shop(elu_text)
    elu_agentunit.add_otherunit(bob_text, credor_weight=3, debtor_weight=1)
    elu_agentunit.add_otherunit(tom_text, credor_weight=1, debtor_weight=4)
    elu_agentunit.add_otherunit(elu_text, credor_weight=1, debtor_weight=4)
    x_money.userhub.save_job_agenda(elu_agentunit)

    otherunit_count_sqlstr = get_row_count_sqlstr("agenda_otherunit")
    assert get_single_result(x_money.get_treasury_conn(), otherunit_count_sqlstr) == 0

    # WHEN
    x_money.refresh_treasury_job_agendas_data()

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), otherunit_count_sqlstr) == 12


def test_MoneyUnit_refresh_treasury_job_agendas_data_CorrectlyPopulatesAgendaTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 OtherUnits = 12 otherunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=True)

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"
    elu_text = "Elu"

    x_money.userhub.save_job_agenda(agendaunit_shop(bob_text))
    x_money.userhub.save_job_agenda(agendaunit_shop(tom_text))
    x_money.userhub.save_job_agenda(agendaunit_shop(sal_text))
    x_money.userhub.save_job_agenda(agendaunit_shop(elu_text))

    agenda_count_sqlstrs = get_row_count_sqlstr("agendaunit")
    assert get_single_result(x_money.get_treasury_conn(), agenda_count_sqlstrs) == 0

    # WHEN
    x_money.refresh_treasury_job_agendas_data()

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), agenda_count_sqlstrs) == 4


def test_MoneyUnit_refresh_treasury_job_agendas_data_CorrectlyPopulatesAgendaTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 OtherUnits = 12 otherunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=True)

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"
    elu_text = "Elu"

    x_money.userhub.save_job_agenda(agendaunit_shop(bob_text))
    x_money.userhub.save_job_agenda(agendaunit_shop(tom_text))
    x_money.userhub.save_job_agenda(agendaunit_shop(sal_text))
    x_money.userhub.save_job_agenda(agendaunit_shop(elu_text))

    agenda_count_sqlstrs = get_row_count_sqlstr("agendaunit")
    assert get_single_result(x_money.get_treasury_conn(), agenda_count_sqlstrs) == 0

    # WHEN
    x_money.refresh_treasury_job_agendas_data()

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), agenda_count_sqlstrs) == 4


def test_MoneyUnit_refresh_treasury_job_agendas_data_CorrectlyPopulates_agenda_beliefunit(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.create_treasury_db(in_memory=True)

    bob_text = "Bob"
    tom_text = "Tom"
    elu_text = "Elu"
    bob_agenda = agendaunit_shop(bob_text)
    tom_agenda = agendaunit_shop(tom_text)
    bob_agenda.add_otherunit(other_id=tom_text)
    tom_agenda.add_otherunit(other_id=bob_text)
    tom_agenda.add_otherunit(other_id=elu_text)
    x_money.userhub.save_job_agenda(bob_agenda)
    x_money.userhub.save_job_agenda(tom_agenda)

    sqlstr = get_row_count_sqlstr("agenda_beliefunit")
    assert get_single_result(x_money.get_treasury_conn(), sqlstr) == 0

    # WHEN
    x_money.refresh_treasury_job_agendas_data()

    # THEN
    assert get_single_result(x_money.get_treasury_conn(), sqlstr) == 3


def test_MoneyUnit_get_agenda_ideaunit_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_agendas_data()

    bob_text = "Bob"
    with x_money.get_treasury_conn() as treasury_conn:
        assert get_agenda_ideaunit_row_count(treasury_conn, bob_text) == 0

    # WHEN
    resources_road = create_road(temp_real_id(), "resources")
    water_road = create_road(resources_road, "water")
    water_agenda_ideaunit = IdeaCatalog(owner_id=bob_text, idea_road=water_road)
    water_insert_sqlstr = get_agenda_ideaunit_table_insert_sqlstr(water_agenda_ideaunit)
    with x_money.get_treasury_conn() as treasury_conn:
        print(water_insert_sqlstr)
        treasury_conn.execute(water_insert_sqlstr)

    # THEN
    assert get_agenda_ideaunit_row_count(treasury_conn, bob_text) == 1


def test_MoneyUnit_refresh_treasury_job_agendas_data_Populates_agenda_ideaunit_table(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 OtherUnits = 12 otherunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_agendas_data()

    bob_text = "Bob"
    sal_text = "Sal"
    tim_text = "Tim"
    bob_agenda = get_3node_agenda()
    tim_agenda = get_6node_agenda()
    sal_agenda = get_agenda_3CleanNodesRandomWeights()
    bob_agenda.set_owner_id(new_owner_id=bob_text)
    tim_agenda.set_owner_id(new_owner_id=tim_text)
    sal_agenda.set_owner_id(new_owner_id=sal_text)
    x_money.userhub.save_job_agenda(bob_agenda)
    x_money.userhub.save_job_agenda(tim_agenda)
    x_money.userhub.save_job_agenda(sal_agenda)

    with x_money.get_treasury_conn() as treasury_conn:
        assert get_agenda_ideaunit_row_count(treasury_conn, bob_text) == 0

    # WHEN
    x_money.refresh_treasury_job_agendas_data()

    # THEN
    with x_money.get_treasury_conn() as treasury_conn:
        assert get_agenda_ideaunit_row_count(treasury_conn, bob_text) == 3
        assert get_agenda_ideaunit_row_count(treasury_conn, tim_text) == 6
        assert get_agenda_ideaunit_row_count(treasury_conn, sal_text) == 5


def test_MoneyUnit_get_agenda_ideaunit_dict_ReturnsCorrectData(env_dir_setup_cleanup):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_agendas_data()

    bob_text = "Bob"
    sal_text = "Sal"
    tim_text = "Tim"
    elu_text = "Elu"
    bob_agenda = get_3node_agenda()
    tim_agenda = get_6node_agenda()
    sal_agenda = get_agenda_3CleanNodesRandomWeights()
    elu_agenda = get_6node_agenda()
    bob_agenda.set_owner_id(new_owner_id=bob_text)
    tim_agenda.set_owner_id(new_owner_id=tim_text)
    sal_agenda.set_owner_id(new_owner_id=sal_text)
    elu_agenda.set_owner_id(new_owner_id=elu_text)
    x_money.userhub.save_job_agenda(bob_agenda)
    x_money.userhub.save_job_agenda(tim_agenda)
    x_money.userhub.save_job_agenda(sal_agenda)
    x_money.userhub.save_job_agenda(elu_agenda)
    x_money.refresh_treasury_job_agendas_data()
    i_count_sqlstr = get_row_count_sqlstr("agenda_ideaunit")
    with x_money.get_treasury_conn() as treasury_conn:
        print(f"{i_count_sqlstr=}")
        assert get_single_result(x_money.get_treasury_conn(), i_count_sqlstr) == 20

    # WHEN / THEN
    assert len(get_agenda_ideaunit_dict(x_money.get_treasury_conn())) == 20
    b_road = create_road(temp_real_id(), "B")
    assert len(get_agenda_ideaunit_dict(x_money.get_treasury_conn(), b_road)) == 3
    c_road = create_road(temp_real_id(), "C")
    ce_road = create_road(c_road, "E")
    assert len(get_agenda_ideaunit_dict(x_money.get_treasury_conn(), ce_road)) == 2
    ex_road = create_road(temp_real_id())
    assert len(get_agenda_ideaunit_dict(x_money.get_treasury_conn(), ex_road)) == 4


def test_MoneyUnit_get_agenda_idea_factunit_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 OtherUnits = 12 otherunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_agendas_data()

    bob_text = "Bob"
    with x_money.get_treasury_conn() as treasury_conn:
        assert get_agenda_idea_factunit_row_count(treasury_conn, bob_text) == 0

    # WHEN
    weather_road = create_road(temp_real_id(), "weather")
    weather_rain = FactCatalog(
        owner_id=bob_text,
        base=weather_road,
        pick=create_road(weather_road, "rain"),
    )
    water_insert_sqlstr = get_agenda_idea_factunit_table_insert_sqlstr(weather_rain)
    with x_money.get_treasury_conn() as treasury_conn:
        print(water_insert_sqlstr)
        treasury_conn.execute(water_insert_sqlstr)

    # THEN
    assert get_agenda_idea_factunit_row_count(treasury_conn, bob_text) == 1


def test_refresh_treasury_job_agendas_data_Populates_agenda_idea_factunit_table(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 OtherUnits = 12 otherunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_agendas_data()

    # create 3 agendas with varying numbers of facts
    bob_text = "Bob"
    sal_text = "Sal"
    tim_text = "Tim"
    bob_agenda = get_3node_agenda()
    tim_agenda = get_6node_agenda()
    sal_agenda = get_agenda_3CleanNodesRandomWeights()
    bob_agenda.set_owner_id(new_owner_id=bob_text)
    tim_agenda.set_owner_id(new_owner_id=tim_text)
    sal_agenda.set_owner_id(new_owner_id=sal_text)
    c_text = "C"
    c_road = tim_agenda.make_l1_road(c_text)
    f_text = "F"
    f_road = create_road(c_road, f_text)
    b_text = "B"
    b_road = tim_agenda.make_l1_road(b_text)
    # for idea_x in tim_agenda._idea_dict.values():
    #     print(f"{f_road=} {idea_x.get_road()=}")
    tim_agenda.set_fact(base=c_road, pick=f_road)

    bob_agenda.set_fact(base=c_road, pick=f_road)
    bob_agenda.set_fact(base=b_road, pick=b_road)

    casa_text = "casa"
    casa_road = sal_agenda.make_l1_road(casa_text)
    cookery_text = "clean cookery"
    cookery_road = create_road(casa_road, cookery_text)
    sal_agenda.set_fact(base=cookery_road, pick=cookery_road)

    x_money.userhub.save_job_agenda(bob_agenda)
    x_money.userhub.save_job_agenda(tim_agenda)
    x_money.userhub.save_job_agenda(sal_agenda)

    with x_money.get_treasury_conn() as treasury_conn:
        assert get_agenda_idea_factunit_row_count(treasury_conn, bob_text) == 0
        assert get_agenda_idea_factunit_row_count(treasury_conn, tim_text) == 0
        assert get_agenda_idea_factunit_row_count(treasury_conn, sal_text) == 0

    # WHEN
    x_money.refresh_treasury_job_agendas_data()

    # THEN
    print(f"{get_agenda_idea_factunit_row_count(treasury_conn, bob_text)=}")
    print(f"{get_agenda_idea_factunit_row_count(treasury_conn, tim_text)=}")
    print(f"{get_agenda_idea_factunit_row_count(treasury_conn, sal_text)=}")
    with x_money.get_treasury_conn() as treasury_conn:
        assert get_agenda_idea_factunit_row_count(treasury_conn, bob_text) == 2
        assert get_agenda_idea_factunit_row_count(treasury_conn, tim_text) == 1
        assert get_agenda_idea_factunit_row_count(treasury_conn, sal_text) == 1


def test_MoneyUnit_get_agenda_beliefunit_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 OtherUnits = 12 otherunit rows
    x_money = moneyunit_shop(get_texas_userhub())
    x_money.refresh_treasury_job_agendas_data()

    bob_text = "Bob"
    with x_money.get_treasury_conn() as treasury_conn:
        assert get_agenda_beliefunit_row_count(treasury_conn, bob_text) == 0

    # WHEN
    bob_belief_x = BeliefUnitCatalog(
        owner_id=bob_text,
        beliefunit_belief_id="US Dollar",
    )
    bob_belief_sqlstr = get_agenda_beliefunit_table_insert_sqlstr(bob_belief_x)
    with x_money.get_treasury_conn() as treasury_conn:
        print(bob_belief_sqlstr)
        treasury_conn.execute(bob_belief_sqlstr)

    # THEN
    assert get_agenda_beliefunit_row_count(treasury_conn, bob_text) == 1


def test_MoneyUnit_get_agenda_beliefunit_dict_ReturnsBeliefUnitData(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_money = moneyunit_shop(get_texas_userhub())

    bob_text = "Bob"
    tom_text = "Tom"
    elu_text = "Elu"
    bob_agenda = agendaunit_shop(bob_text)
    tom_agenda = agendaunit_shop(tom_text)
    bob_agenda.add_otherunit(other_id=tom_text)
    tom_agenda.add_otherunit(other_id=bob_text)
    tom_agenda.add_otherunit(other_id=elu_text)
    x_money.userhub.save_job_agenda(bob_agenda)
    x_money.userhub.save_job_agenda(tom_agenda)
    x_money.refresh_treasury_job_agendas_data()
    sqlstr = get_row_count_sqlstr("agenda_beliefunit")
    assert get_single_result(x_money.get_treasury_conn(), sqlstr) == 3

    # WHEN
    with x_money.get_treasury_conn() as treasury_conn:
        print("try to grab BeliefUnit data")
        agenda_beliefunit_dict = get_agenda_beliefunit_dict(db_conn=treasury_conn)

    # THEN
    assert len(agenda_beliefunit_dict) == 3
    bob_agenda_tom_belief = f"{bob_text} {tom_text}"
    tom_bob_agenda_belief = f"{tom_text} {bob_text}"
    tom_agenda_elu_belief = f"{tom_text} {elu_text}"
    assert agenda_beliefunit_dict.get(bob_agenda_tom_belief) != None
    assert agenda_beliefunit_dict.get(tom_bob_agenda_belief) != None
    assert agenda_beliefunit_dict.get(tom_agenda_elu_belief) != None
