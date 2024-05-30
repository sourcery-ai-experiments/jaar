from src._road.road import create_road
from src.agenda.agenda import (
    agendaunit_shop,
    ideaunit_shop,
    groupunit_shop,
    partylink_shop,
)
from src.econ.econ import econunit_shop
from src.econ.examples.econ_env_kit import (
    get_temp_env_real_id,
    get_test_econ_dir,
    env_dir_setup_cleanup,
)
from src._instrument.sqlite import get_single_result
from src.econ.treasury_sqlstr import (
    get_agenda_ideaunit_row_count,
    IdeaCatalog,
    get_agenda_ideaunit_table_insert_sqlstr,
    get_agenda_ideaunit_dict,
    get_agenda_idea_beliefunit_row_count,
    BeliefCatalog,
    get_agenda_idea_beliefunit_table_insert_sqlstr,
    get_agenda_groupunit_row_count,
    GroupUnitCatalog,
    get_agenda_groupunit_table_insert_sqlstr,
    get_agenda_groupunit_dict,
)
from src.econ.examples.example_econ_agendas import (
    get_3node_agenda,
    get_6node_agenda,
    get_agenda_3CleanNodesRandomWeights,
)
from src._instrument.sqlite import get_single_result, get_row_count_sqlstr


def test_EconUnit_refresh_treasury_job_agendas_data_CorrectlyDeletesOldTreasuryInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ = econunit_shop(real_id=get_temp_env_real_id(), econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)

    bob_text = "Bob"
    tom_text = "Tom"

    bob_agentunit = agendaunit_shop(_owner_id=bob_text)
    bob_agentunit.add_partyunit(party_id=tom_text, creditor_weight=3, debtor_weight=1)
    x_econ.save_job_file(bob_agentunit)
    x_econ.refresh_treasury_job_agendas_data()
    partyunit_count_sqlstr = get_row_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_econ.get_treasury_conn(), partyunit_count_sqlstr) == 1

    # WHEN
    x_econ.refresh_treasury_job_agendas_data()

    # THEN
    assert get_single_result(x_econ.get_treasury_conn(), partyunit_count_sqlstr) == 1


def test_EconUnit_refresh_treasury_job_agendas_data_CorrectlyDeletesOldTreasuryFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ = econunit_shop(real_id=get_temp_env_real_id(), econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=False)

    bob_text = "Bob"
    tom_text = "Tom"

    bob_agentunit = agendaunit_shop(_owner_id=bob_text)
    bob_agentunit.add_partyunit(party_id=tom_text, creditor_weight=3, debtor_weight=1)
    x_econ.save_job_file(bob_agentunit)
    x_econ.refresh_treasury_job_agendas_data()
    partyunit_count_sqlstr = get_row_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_econ.get_treasury_conn(), partyunit_count_sqlstr) == 1

    # WHEN
    x_econ.refresh_treasury_job_agendas_data()

    # THEN
    assert get_single_result(x_econ.get_treasury_conn(), partyunit_count_sqlstr) == 1


def test_EconUnit_refresh_treasury_job_agendas_data_CorrectlyPopulatesPartyunitTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 PartyUnits = 12 partyunit rows
    x_econ = econunit_shop(real_id=get_temp_env_real_id(), econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"
    elu_text = "Elu"

    bob_agentunit = agendaunit_shop(_owner_id=bob_text)
    bob_agentunit.add_partyunit(party_id=tom_text, creditor_weight=3, debtor_weight=1)
    bob_agentunit.add_partyunit(party_id=sal_text, creditor_weight=1, debtor_weight=4)
    bob_agentunit.add_partyunit(party_id=elu_text, creditor_weight=1, debtor_weight=4)
    x_econ.save_job_file(bob_agentunit)

    sal_agentunit = agendaunit_shop(_owner_id=sal_text)
    sal_agentunit.add_partyunit(party_id=bob_text, creditor_weight=1, debtor_weight=4)
    sal_agentunit.add_partyunit(party_id=tom_text, creditor_weight=3, debtor_weight=1)
    sal_agentunit.add_partyunit(party_id=elu_text, creditor_weight=1, debtor_weight=4)
    x_econ.save_job_file(sal_agentunit)

    tom_agentunit = agendaunit_shop(_owner_id=tom_text)
    tom_agentunit.add_partyunit(party_id=bob_text, creditor_weight=3, debtor_weight=1)
    tom_agentunit.add_partyunit(party_id=sal_text, creditor_weight=1, debtor_weight=4)
    tom_agentunit.add_partyunit(party_id=elu_text, creditor_weight=1, debtor_weight=4)
    x_econ.save_job_file(tom_agentunit)

    elu_agentunit = agendaunit_shop(_owner_id=elu_text)
    elu_agentunit.add_partyunit(party_id=bob_text, creditor_weight=3, debtor_weight=1)
    elu_agentunit.add_partyunit(party_id=tom_text, creditor_weight=1, debtor_weight=4)
    elu_agentunit.add_partyunit(party_id=elu_text, creditor_weight=1, debtor_weight=4)
    x_econ.save_job_file(elu_agentunit)

    partyunit_count_sqlstr = get_row_count_sqlstr("agenda_partyunit")
    assert get_single_result(x_econ.get_treasury_conn(), partyunit_count_sqlstr) == 0

    # WHEN
    x_econ.refresh_treasury_job_agendas_data()

    # THEN
    assert get_single_result(x_econ.get_treasury_conn(), partyunit_count_sqlstr) == 12


def test_EconUnit_refresh_treasury_job_agendas_data_CorrectlyPopulatesAgendaTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 PartyUnits = 12 partyunit rows
    x_econ = econunit_shop(real_id=get_temp_env_real_id(), econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"
    elu_text = "Elu"

    x_econ.save_job_file(agendaunit_shop(_owner_id=bob_text))
    x_econ.save_job_file(agendaunit_shop(_owner_id=tom_text))
    x_econ.save_job_file(agendaunit_shop(_owner_id=sal_text))
    x_econ.save_job_file(agendaunit_shop(_owner_id=elu_text))

    agenda_count_sqlstrs = get_row_count_sqlstr("agendaunit")
    assert get_single_result(x_econ.get_treasury_conn(), agenda_count_sqlstrs) == 0

    # WHEN
    x_econ.refresh_treasury_job_agendas_data()

    # THEN
    assert get_single_result(x_econ.get_treasury_conn(), agenda_count_sqlstrs) == 4


def test_EconUnit_refresh_treasury_job_agendas_data_CorrectlyPopulatesAgendaTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 PartyUnits = 12 partyunit rows
    x_econ = econunit_shop(real_id=get_temp_env_real_id(), econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)

    bob_text = "Bob"
    tom_text = "Tom"
    sal_text = "Sal"
    elu_text = "Elu"

    x_econ.save_job_file(agendaunit_shop(_owner_id=bob_text))
    x_econ.save_job_file(agendaunit_shop(_owner_id=tom_text))
    x_econ.save_job_file(agendaunit_shop(_owner_id=sal_text))
    x_econ.save_job_file(agendaunit_shop(_owner_id=elu_text))

    agenda_count_sqlstrs = get_row_count_sqlstr("agendaunit")
    assert get_single_result(x_econ.get_treasury_conn(), agenda_count_sqlstrs) == 0

    # WHEN
    x_econ.refresh_treasury_job_agendas_data()

    # THEN
    assert get_single_result(x_econ.get_treasury_conn(), agenda_count_sqlstrs) == 4


def test_EconUnit_refresh_treasury_job_agendas_data_CorrectlyPopulates_agenda_groupunit(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ = econunit_shop(real_id=get_temp_env_real_id(), econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)

    bob_text = "Bob"
    tom_text = "Tom"
    elu_text = "Elu"
    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    bob_agenda.add_partyunit(party_id=tom_text)
    tom_agenda.add_partyunit(party_id=bob_text)
    tom_agenda.add_partyunit(party_id=elu_text)
    x_econ.save_job_file(bob_agenda)
    x_econ.save_job_file(tom_agenda)

    sqlstr = get_row_count_sqlstr("agenda_groupunit")
    assert get_single_result(x_econ.get_treasury_conn(), sqlstr) == 0

    # WHEN
    x_econ.refresh_treasury_job_agendas_data()

    # THEN
    assert get_single_result(x_econ.get_treasury_conn(), sqlstr) == 3


def test_EconUnit_set_agenda_treasury_attrs_CorrectlyPopulatesAgenda_partylinks(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ = econunit_shop(real_id=get_temp_env_real_id(), econ_dir=get_test_econ_dir())
    x_econ.set_econ_dirs(in_memory_treasury=True)

    # create 4 agendas, 1 with group "swimming expert" linked to 1 party
    # two others have idea create_road(root_label()},sports,swimming"
    # run set_treasury_metrics
    # assert
    # _treasury_partylinks
    # assert group "swimming expert" has 1 party
    # modify groupunit "swimming expert" _treasury_partylinks ==  create_road(root_label()}sports,swimmer"
    # run set_treasury_metrics
    # assert group "swimming expert" has 2 different party
    x_real_id = x_econ.real_id

    sal_text = "Sal"
    bob_text = "Bob"
    tom_text = "Tom"
    ava_text = "Ava"

    sal_agenda = agendaunit_shop(sal_text, x_real_id)
    bob_agenda = agendaunit_shop(bob_text, x_real_id)
    tom_agenda = agendaunit_shop(tom_text, x_real_id)
    ava_agenda = agendaunit_shop(ava_text, x_real_id)

    swim_text = "swimming"
    sports_text = "sports"
    sal_sports_road = create_road(x_real_id, sports_text)
    bob_sports_road = create_road(x_real_id, sports_text)
    tom_sports_road = create_road(x_real_id, sports_text)

    sal_agenda.add_idea(ideaunit_shop(swim_text), parent_road=sal_sports_road)
    bob_agenda.add_idea(ideaunit_shop(swim_text), parent_road=bob_sports_road)
    tom_agenda.add_idea(ideaunit_shop(swim_text), parent_road=tom_sports_road)

    sal_agenda.add_partyunit(party_id=bob_text, creditor_weight=2, debtor_weight=2)

    swim_group_text = ",swimming experts"
    swim_group_unit = groupunit_shop(group_id=swim_group_text)
    bob_link = partylink_shop(party_id=bob_text)
    swim_group_unit.set_partylink(partylink=bob_link)
    sal_agenda.set_groupunit(y_groupunit=swim_group_unit)

    x_econ.save_job_file(sal_agenda)
    x_econ.save_job_file(bob_agenda)
    x_econ.save_job_file(tom_agenda)
    x_econ.save_job_file(ava_agenda)

    x_econ.set_agenda_treasury_attrs(x_owner_id=sal_text)
    e1_sal_agenda = x_econ.get_job_file(owner_id=sal_text)
    assert len(e1_sal_agenda._groups.get(swim_group_text)._partys) == 1

    # WHEN
    # modify groupunit "swimming expert" _treasury_partylinks ==  create_road(root_label()},sports,swimmer"
    sal_swim_road = create_road(sal_sports_road, swim_text)
    swim_group_unit.set_attr(_treasury_partylinks=sal_swim_road)
    sal_agenda.set_groupunit(y_groupunit=swim_group_unit)
    x_econ.save_job_file(sal_agenda)
    x_econ.set_agenda_treasury_attrs(x_owner_id=sal_text)

    # THEN
    e1_sal_agenda = x_econ.get_job_file(owner_id=sal_text)
    assert len(e1_sal_agenda._groups.get(swim_group_text)._partys) == 2


def test_EconUnit_get_agenda_ideaunit_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())
    x_econ.refresh_treasury_job_agendas_data()

    bob_text = "Bob"
    with x_econ.get_treasury_conn() as treasury_conn:
        assert get_agenda_ideaunit_row_count(treasury_conn, bob_text) == 0

    # WHEN
    resources_road = create_road(get_temp_env_real_id(), "resources")
    water_road = create_road(resources_road, "water")
    water_agenda_ideaunit = IdeaCatalog(owner_id=bob_text, idea_road=water_road)
    water_insert_sqlstr = get_agenda_ideaunit_table_insert_sqlstr(water_agenda_ideaunit)
    with x_econ.get_treasury_conn() as treasury_conn:
        print(water_insert_sqlstr)
        treasury_conn.execute(water_insert_sqlstr)

    # THEN
    assert get_agenda_ideaunit_row_count(treasury_conn, bob_text) == 1


def test_EconUnit_refresh_treasury_job_agendas_data_Populates_agenda_ideaunit_table(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 PartyUnits = 12 partyunit rows
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())
    x_econ.refresh_treasury_job_agendas_data()

    bob_text = "Bob"
    sal_text = "Sal"
    tim_text = "Tim"
    bob_agenda = get_3node_agenda()
    tim_agenda = get_6node_agenda()
    sal_agenda = get_agenda_3CleanNodesRandomWeights()
    bob_agenda.set_owner_id(new_owner_id=bob_text)
    tim_agenda.set_owner_id(new_owner_id=tim_text)
    sal_agenda.set_owner_id(new_owner_id=sal_text)
    x_econ.save_job_file(bob_agenda)
    x_econ.save_job_file(tim_agenda)
    x_econ.save_job_file(sal_agenda)

    with x_econ.get_treasury_conn() as treasury_conn:
        assert get_agenda_ideaunit_row_count(treasury_conn, bob_text) == 0

    # WHEN
    x_econ.refresh_treasury_job_agendas_data()

    # THEN
    with x_econ.get_treasury_conn() as treasury_conn:
        assert get_agenda_ideaunit_row_count(treasury_conn, bob_text) == 3
        assert get_agenda_ideaunit_row_count(treasury_conn, tim_text) == 6
        assert get_agenda_ideaunit_row_count(treasury_conn, sal_text) == 5


def test_EconUnit_get_agenda_ideaunit_dict_ReturnsCorrectData(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())
    x_econ.refresh_treasury_job_agendas_data()

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
    x_econ.save_job_file(bob_agenda)
    x_econ.save_job_file(tim_agenda)
    x_econ.save_job_file(sal_agenda)
    x_econ.save_job_file(elu_agenda)
    x_econ.refresh_treasury_job_agendas_data()
    i_count_sqlstr = get_row_count_sqlstr("agenda_ideaunit")
    with x_econ.get_treasury_conn() as treasury_conn:
        print(f"{i_count_sqlstr=}")
        assert get_single_result(x_econ.get_treasury_conn(), i_count_sqlstr) == 20

    # WHEN / THEN
    assert len(get_agenda_ideaunit_dict(x_econ.get_treasury_conn())) == 20
    b_road = create_road(get_temp_env_real_id(), "B")
    assert len(get_agenda_ideaunit_dict(x_econ.get_treasury_conn(), b_road)) == 3
    c_road = create_road(get_temp_env_real_id(), "C")
    ce_road = create_road(c_road, "E")
    assert len(get_agenda_ideaunit_dict(x_econ.get_treasury_conn(), ce_road)) == 2
    ex_road = create_road(get_temp_env_real_id())
    assert len(get_agenda_ideaunit_dict(x_econ.get_treasury_conn(), ex_road)) == 4


def test_EconUnit_get_agenda_idea_beliefunit_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 PartyUnits = 12 partyunit rows
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())
    x_econ.refresh_treasury_job_agendas_data()

    bob_text = "Bob"
    with x_econ.get_treasury_conn() as treasury_conn:
        assert get_agenda_idea_beliefunit_row_count(treasury_conn, bob_text) == 0

    # WHEN
    weather_road = create_road(get_temp_env_real_id(), "weather")
    weather_rain = BeliefCatalog(
        owner_id=bob_text,
        base=weather_road,
        pick=create_road(weather_road, "rain"),
    )
    water_insert_sqlstr = get_agenda_idea_beliefunit_table_insert_sqlstr(weather_rain)
    with x_econ.get_treasury_conn() as treasury_conn:
        print(water_insert_sqlstr)
        treasury_conn.execute(water_insert_sqlstr)

    # THEN
    assert get_agenda_idea_beliefunit_row_count(treasury_conn, bob_text) == 1


def test_refresh_treasury_job_agendas_data_Populates_agenda_idea_beliefunit_table(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 PartyUnits = 12 partyunit rows
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())
    x_econ.refresh_treasury_job_agendas_data()

    # create 3 agendas with varying numbers of beliefs
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
    tim_agenda.set_belief(base=c_road, pick=f_road)

    bob_agenda.set_belief(base=c_road, pick=f_road)
    bob_agenda.set_belief(base=b_road, pick=b_road)

    casa_text = "casa"
    casa_road = sal_agenda.make_l1_road(casa_text)
    cookery_text = "clean cookery"
    cookery_road = create_road(casa_road, cookery_text)
    sal_agenda.set_belief(base=cookery_road, pick=cookery_road)

    x_econ.save_job_file(bob_agenda)
    x_econ.save_job_file(tim_agenda)
    x_econ.save_job_file(sal_agenda)

    with x_econ.get_treasury_conn() as treasury_conn:
        assert get_agenda_idea_beliefunit_row_count(treasury_conn, bob_text) == 0
        assert get_agenda_idea_beliefunit_row_count(treasury_conn, tim_text) == 0
        assert get_agenda_idea_beliefunit_row_count(treasury_conn, sal_text) == 0

    # WHEN
    x_econ.refresh_treasury_job_agendas_data()

    # THEN
    print(f"{get_agenda_idea_beliefunit_row_count(treasury_conn, bob_text)=}")
    print(f"{get_agenda_idea_beliefunit_row_count(treasury_conn, tim_text)=}")
    print(f"{get_agenda_idea_beliefunit_row_count(treasury_conn, sal_text)=}")
    with x_econ.get_treasury_conn() as treasury_conn:
        assert get_agenda_idea_beliefunit_row_count(treasury_conn, bob_text) == 2
        assert get_agenda_idea_beliefunit_row_count(treasury_conn, tim_text) == 1
        assert get_agenda_idea_beliefunit_row_count(treasury_conn, sal_text) == 1


def test_EconUnit_get_agenda_groupunit_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example econ with 4 Healers, each with 3 PartyUnits = 12 partyunit rows
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())
    x_econ.refresh_treasury_job_agendas_data()

    bob_text = "Bob"
    with x_econ.get_treasury_conn() as treasury_conn:
        assert get_agenda_groupunit_row_count(treasury_conn, bob_text) == 0

    # WHEN
    bob_group_x = GroupUnitCatalog(
        owner_id=bob_text,
        groupunit_group_id="US Dollar",
        treasury_partylinks=create_road(get_temp_env_real_id(), "USA"),
    )
    bob_group_sqlstr = get_agenda_groupunit_table_insert_sqlstr(bob_group_x)
    with x_econ.get_treasury_conn() as treasury_conn:
        print(bob_group_sqlstr)
        treasury_conn.execute(bob_group_sqlstr)

    # THEN
    assert get_agenda_groupunit_row_count(treasury_conn, bob_text) == 1


def test_EconUnit_get_agenda_groupunit_dict_ReturnsGroupUnitData(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_real_id(), get_test_econ_dir())

    bob_text = "Bob"
    tom_text = "Tom"
    elu_text = "Elu"
    bob_agenda = agendaunit_shop(_owner_id=bob_text)
    tom_agenda = agendaunit_shop(_owner_id=tom_text)
    bob_agenda.add_partyunit(party_id=tom_text)
    tom_agenda.add_partyunit(party_id=bob_text)
    tom_agenda.add_partyunit(party_id=elu_text)
    x_econ.save_job_file(bob_agenda)
    x_econ.save_job_file(tom_agenda)
    x_econ.refresh_treasury_job_agendas_data()
    sqlstr = get_row_count_sqlstr("agenda_groupunit")
    assert get_single_result(x_econ.get_treasury_conn(), sqlstr) == 3

    # WHEN
    with x_econ.get_treasury_conn() as treasury_conn:
        print("try to grab GroupUnit data")
        agenda_groupunit_dict = get_agenda_groupunit_dict(db_conn=treasury_conn)

    # THEN
    assert len(agenda_groupunit_dict) == 3
    bob_agenda_tom_group = f"{bob_text} {tom_text}"
    tom_bob_agenda_group = f"{tom_text} {bob_text}"
    tom_agenda_elu_group = f"{tom_text} {elu_text}"
    assert agenda_groupunit_dict.get(bob_agenda_tom_group) != None
    assert agenda_groupunit_dict.get(tom_bob_agenda_group) != None
    assert agenda_groupunit_dict.get(tom_agenda_elu_group) != None
