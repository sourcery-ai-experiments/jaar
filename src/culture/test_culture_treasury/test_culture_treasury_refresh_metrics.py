from src.agenda.road import get_road
from src.agenda.agenda import (
    agendaunit_shop,
    ideacore_shop,
    groupunit_shop,
    partylink_shop,
)
from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    get_temp_env_qid,
    get_test_cultures_dir,
    env_dir_setup_cleanup,
)
from src.culture.y_func import get_single_result
from src.culture.treasury_sqlstr import (
    get_table_count_sqlstr,
    get_idea_catalog_table_count,
    IdeaCatalog,
    get_idea_catalog_table_insert_sqlstr,
    get_idea_catalog_dict,
    get_acptfact_catalog_table_count,
    AcptFactCatalog,
    get_acptfact_catalog_table_insert_sqlstr,
    get_groupunit_catalog_table_count,
    GroupUnitCatalog,
    get_groupunit_catalog_table_insert_sqlstr,
    get_groupunit_catalog_dict,
    get_table_count_sqlstr,
)
from src.culture.examples.example_councils import (
    get_3node_agenda,
    get_6node_agenda,
    get_agenda_3CleanNodesRandomWeights,
)
from src.culture.y_func import get_single_result


def test_culture_refresh_treasury_public_agendas_data_CorrectlyDeletesOldTreasuryInMemory(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(
        qid=get_temp_env_qid(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_treasury=True)

    bob_text = "bob"
    tom_text = "tom"

    bob = agendaunit_shop(_healer=bob_text)
    bob.add_partyunit(pid=tom_text, creditor_weight=3, debtor_weight=1)
    x_culture.save_public_agenda(bob)
    x_culture.refresh_treasury_public_agendas_data()
    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_culture.get_treasury_conn(), partyunit_count_sqlstr) == 1

    # WHEN
    x_culture.refresh_treasury_public_agendas_data()

    # THEN
    assert get_single_result(x_culture.get_treasury_conn(), partyunit_count_sqlstr) == 1


def test_culture_refresh_treasury_public_agendas_data_CorrectlyDeletesOldTreasuryFile(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(
        qid=get_temp_env_qid(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_treasury=False)

    bob_text = "bob"
    tom_text = "tom"

    bob = agendaunit_shop(_healer=bob_text)
    bob.add_partyunit(pid=tom_text, creditor_weight=3, debtor_weight=1)
    x_culture.save_public_agenda(bob)
    x_culture.refresh_treasury_public_agendas_data()
    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_culture.get_treasury_conn(), partyunit_count_sqlstr) == 1

    # WHEN
    x_culture.refresh_treasury_public_agendas_data()

    # THEN
    assert get_single_result(x_culture.get_treasury_conn(), partyunit_count_sqlstr) == 1


def test_culture_refresh_treasury_public_agendas_data_CorrectlyPopulatesPartyunitTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 partyunit rows
    x_culture = cultureunit_shop(
        qid=get_temp_env_qid(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_treasury=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    bob = agendaunit_shop(_healer=bob_text)
    bob.add_partyunit(pid=tom_text, creditor_weight=3, debtor_weight=1)
    bob.add_partyunit(pid=sal_text, creditor_weight=1, debtor_weight=4)
    bob.add_partyunit(pid=elu_text, creditor_weight=1, debtor_weight=4)
    x_culture.save_public_agenda(bob)

    sal = agendaunit_shop(_healer=sal_text)
    sal.add_partyunit(pid=bob_text, creditor_weight=1, debtor_weight=4)
    sal.add_partyunit(pid=tom_text, creditor_weight=3, debtor_weight=1)
    sal.add_partyunit(pid=elu_text, creditor_weight=1, debtor_weight=4)
    x_culture.save_public_agenda(sal)

    tom = agendaunit_shop(_healer=tom_text)
    tom.add_partyunit(pid=bob_text, creditor_weight=3, debtor_weight=1)
    tom.add_partyunit(pid=sal_text, creditor_weight=1, debtor_weight=4)
    tom.add_partyunit(pid=elu_text, creditor_weight=1, debtor_weight=4)
    x_culture.save_public_agenda(tom)

    elu = agendaunit_shop(_healer=elu_text)
    elu.add_partyunit(pid=bob_text, creditor_weight=3, debtor_weight=1)
    elu.add_partyunit(pid=tom_text, creditor_weight=1, debtor_weight=4)
    elu.add_partyunit(pid=elu_text, creditor_weight=1, debtor_weight=4)
    x_culture.save_public_agenda(elu)

    partyunit_count_sqlstr = get_table_count_sqlstr("partyunit")
    assert get_single_result(x_culture.get_treasury_conn(), partyunit_count_sqlstr) == 0

    # WHEN
    x_culture.refresh_treasury_public_agendas_data()

    # THEN
    assert (
        get_single_result(x_culture.get_treasury_conn(), partyunit_count_sqlstr) == 12
    )


def test_culture_refresh_treasury_public_agendas_data_CorrectlyPopulatesAgendaTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 partyunit rows
    x_culture = cultureunit_shop(
        qid=get_temp_env_qid(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_treasury=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    x_culture.save_public_agenda(agendaunit_shop(_healer=bob_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=tom_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=sal_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=elu_text))

    agenda_count_sqlstrs = get_table_count_sqlstr("agendaunit")
    assert get_single_result(x_culture.get_treasury_conn(), agenda_count_sqlstrs) == 0

    # WHEN
    x_culture.refresh_treasury_public_agendas_data()

    # THEN
    assert get_single_result(x_culture.get_treasury_conn(), agenda_count_sqlstrs) == 4


def test_culture_refresh_treasury_public_agendas_data_CorrectlyPopulatesAgendaTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 partyunit rows
    x_culture = cultureunit_shop(
        qid=get_temp_env_qid(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_treasury=True)

    bob_text = "bob"
    tom_text = "tom"
    sal_text = "sal"
    elu_text = "elu"

    x_culture.save_public_agenda(agendaunit_shop(_healer=bob_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=tom_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=sal_text))
    x_culture.save_public_agenda(agendaunit_shop(_healer=elu_text))

    agenda_count_sqlstrs = get_table_count_sqlstr("agendaunit")
    assert get_single_result(x_culture.get_treasury_conn(), agenda_count_sqlstrs) == 0

    # WHEN
    x_culture.refresh_treasury_public_agendas_data()

    # THEN
    assert get_single_result(x_culture.get_treasury_conn(), agenda_count_sqlstrs) == 4


def test_culture_refresh_treasury_public_agendas_data_CorrectlyPopulates_groupunit_catalog(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(
        qid=get_temp_env_qid(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_treasury=True)

    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"
    bob_agenda = agendaunit_shop(_healer=bob_text)
    tom_agenda = agendaunit_shop(_healer=tom_text)
    bob_agenda.add_partyunit(pid=tom_text)
    tom_agenda.add_partyunit(pid=bob_text)
    tom_agenda.add_partyunit(pid=elu_text)
    x_culture.save_public_agenda(bob_agenda)
    x_culture.save_public_agenda(tom_agenda)

    sqlstr = get_table_count_sqlstr("groupunit_catalog")
    assert get_single_result(x_culture.get_treasury_conn(), sqlstr) == 0

    # WHEN
    x_culture.refresh_treasury_public_agendas_data()

    # THEN
    assert get_single_result(x_culture.get_treasury_conn(), sqlstr) == 3


def test_culture_set_agenda_treasury_attrs_CorrectlyPopulatesAgenda_Groupunit_Partylinks(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(
        qid=get_temp_env_qid(), cultures_dir=get_test_cultures_dir()
    )
    x_culture.create_dirs_if_null(in_memory_treasury=True)

    # create 4 agendas, 1 with group "swimming expert" linked to 1 party
    # two others have idea get_road(root_label()},sports,swimming"
    # run set_treasury_metrics
    # assert
    # _partylinks_set_by_culture_road
    # assert group "swimming expert" has 1 party
    # change groupunit "swimming expert" _partylinks_set_by_culture_road ==  get_road(root_label()}sports,swimmer"
    # run set_treasury_metrics
    # assert group "swimming expert" has 2 different party

    sal_text = "sal"
    bob_text = "bob"
    tom_text = "tom"
    ava_text = "ava"

    sal_agenda = agendaunit_shop(_healer=sal_text)
    bob_agenda = agendaunit_shop(_healer=bob_text)
    tom_agenda = agendaunit_shop(_healer=tom_text)
    ava_agenda = agendaunit_shop(_healer=ava_text)

    swim_text = "swimming"
    sports_text = "sports"
    sal_sports_road = get_road(x_culture.qid, sports_text)
    bob_sports_road = get_road(x_culture.qid, sports_text)
    tom_sports_road = get_road(x_culture.qid, sports_text)

    sal_agenda.add_idea(ideacore_shop(swim_text), pad=sal_sports_road)
    bob_agenda.add_idea(ideacore_shop(swim_text), pad=bob_sports_road)
    tom_agenda.add_idea(ideacore_shop(swim_text), pad=tom_sports_road)

    sal_agenda.add_partyunit(pid=bob_text, creditor_weight=2, debtor_weight=2)

    swim_group_text = "swimming expert"
    swim_group_unit = groupunit_shop(brand=swim_group_text)
    bob_link = partylink_shop(pid=bob_text)
    swim_group_unit.set_partylink(partylink=bob_link)
    sal_agenda.set_groupunit(groupunit=swim_group_unit)

    x_culture.save_public_agenda(sal_agenda)
    x_culture.save_public_agenda(bob_agenda)
    x_culture.save_public_agenda(tom_agenda)
    x_culture.save_public_agenda(ava_agenda)

    x_culture.set_agenda_treasury_attrs(x_healer=sal_text)
    e1_sal_agenda = x_culture.get_public_agenda(healer=sal_text)
    assert len(e1_sal_agenda._groups.get(swim_group_text)._partys) == 1

    # WHEN
    # change groupunit "swimming expert" _partylinks_set_by_culture_road ==  get_road(root_label()},sports,swimmer"
    sal_swim_road = get_road(sal_sports_road, swim_text)
    swim_group_unit.set_attr(_partylinks_set_by_culture_road=sal_swim_road)
    sal_agenda.set_groupunit(groupunit=swim_group_unit)
    x_culture.save_public_agenda(sal_agenda)
    x_culture.set_agenda_treasury_attrs(x_healer=sal_text)

    # THEN
    e1_sal_agenda = x_culture.get_public_agenda(healer=sal_text)
    assert len(e1_sal_agenda._groups.get(swim_group_text)._partys) == 2


def test_culture_get_idea_catalog_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(get_temp_env_qid(), get_test_cultures_dir())
    x_culture.refresh_treasury_public_agendas_data()

    bob_text = "bob"
    with x_culture.get_treasury_conn() as treasury_conn:
        assert get_idea_catalog_table_count(treasury_conn, bob_text) == 0

    # WHEN
    element_road = get_road(get_temp_env_qid(), "elements")
    water_road = get_road(element_road, "water")
    water_idea_catalog = IdeaCatalog(agenda_healer=bob_text, idea_road=water_road)
    water_insert_sqlstr = get_idea_catalog_table_insert_sqlstr(water_idea_catalog)
    with x_culture.get_treasury_conn() as treasury_conn:
        print(water_insert_sqlstr)
        treasury_conn.execute(water_insert_sqlstr)

    # THEN
    assert get_idea_catalog_table_count(treasury_conn, bob_text) == 1


def test_culture_refresh_treasury_public_agendas_data_Populates_idea_catalog_table(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 partyunit rows
    x_culture = cultureunit_shop(get_temp_env_qid(), get_test_cultures_dir())
    x_culture.refresh_treasury_public_agendas_data()

    bob_text = "bob"
    sal_text = "sal"
    tim_text = "tim"
    bob_agenda = get_3node_agenda()
    tim_agenda = get_6node_agenda()
    sal_agenda = get_agenda_3CleanNodesRandomWeights()
    bob_agenda.set_healer(new_healer=bob_text)
    tim_agenda.set_healer(new_healer=tim_text)
    sal_agenda.set_healer(new_healer=sal_text)
    x_culture.save_public_agenda(bob_agenda)
    x_culture.save_public_agenda(tim_agenda)
    x_culture.save_public_agenda(sal_agenda)

    with x_culture.get_treasury_conn() as treasury_conn:
        assert get_idea_catalog_table_count(treasury_conn, bob_text) == 0

    # WHEN
    x_culture.refresh_treasury_public_agendas_data()

    # THEN
    with x_culture.get_treasury_conn() as treasury_conn:
        assert get_idea_catalog_table_count(treasury_conn, bob_text) == 3
        assert get_idea_catalog_table_count(treasury_conn, tim_text) == 6
        assert get_idea_catalog_table_count(treasury_conn, sal_text) == 5


def test_culture_get_idea_catalog_dict_ReturnsCorrectData(env_dir_setup_cleanup):
    # GIVEN
    x_culture = cultureunit_shop(get_temp_env_qid(), get_test_cultures_dir())
    x_culture.refresh_treasury_public_agendas_data()

    bob_text = "bob"
    sal_text = "sal"
    tim_text = "tim"
    elu_text = "elu"
    bob_agenda = get_3node_agenda()
    tim_agenda = get_6node_agenda()
    sal_agenda = get_agenda_3CleanNodesRandomWeights()
    elu_agenda = get_6node_agenda()
    bob_agenda.set_healer(new_healer=bob_text)
    tim_agenda.set_healer(new_healer=tim_text)
    sal_agenda.set_healer(new_healer=sal_text)
    elu_agenda.set_healer(new_healer=elu_text)
    x_culture.save_public_agenda(bob_agenda)
    x_culture.save_public_agenda(tim_agenda)
    x_culture.save_public_agenda(sal_agenda)
    x_culture.save_public_agenda(elu_agenda)
    x_culture.refresh_treasury_public_agendas_data()
    i_count_sqlstr = get_table_count_sqlstr("idea_catalog")
    with x_culture.get_treasury_conn() as treasury_conn:
        print(f"{i_count_sqlstr=}")
        assert get_single_result(x_culture.get_treasury_conn(), i_count_sqlstr) == 20

    # WHEN / THEN
    assert len(get_idea_catalog_dict(x_culture.get_treasury_conn())) == 20
    b_road = get_road(get_temp_env_qid(), "B")
    assert len(get_idea_catalog_dict(x_culture.get_treasury_conn(), b_road)) == 3
    c_road = get_road(get_temp_env_qid(), "C")
    ce_road = get_road(c_road, "E")
    assert len(get_idea_catalog_dict(x_culture.get_treasury_conn(), ce_road)) == 2
    ex_road = get_road(get_temp_env_qid())
    assert len(get_idea_catalog_dict(x_culture.get_treasury_conn(), ex_road)) == 4


def test_culture_get_acptfact_catalog_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 partyunit rows
    x_culture = cultureunit_shop(get_temp_env_qid(), get_test_cultures_dir())
    x_culture.refresh_treasury_public_agendas_data()

    bob_text = "bob"
    with x_culture.get_treasury_conn() as treasury_conn:
        assert get_acptfact_catalog_table_count(treasury_conn, bob_text) == 0

    # WHEN
    weather_road = get_road(get_temp_env_qid(), "weather")
    weather_rain = AcptFactCatalog(
        agenda_healer=bob_text,
        base=weather_road,
        pick=get_road(weather_road, "rain"),
    )
    water_insert_sqlstr = get_acptfact_catalog_table_insert_sqlstr(weather_rain)
    with x_culture.get_treasury_conn() as treasury_conn:
        print(water_insert_sqlstr)
        treasury_conn.execute(water_insert_sqlstr)

    # THEN
    assert get_acptfact_catalog_table_count(treasury_conn, bob_text) == 1


def test_refresh_treasury_public_agendas_data_Populates_acptfact_catalog_table(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 partyunit rows
    x_culture = cultureunit_shop(get_temp_env_qid(), get_test_cultures_dir())
    x_culture.refresh_treasury_public_agendas_data()

    # TODO create 3 agendas with varying numbers of acpt facts
    bob_text = "bob"
    sal_text = "sal"
    tim_text = "tim"
    bob_agenda = get_3node_agenda()
    tim_agenda = get_6node_agenda()
    sal_agenda = get_agenda_3CleanNodesRandomWeights()
    bob_agenda.set_healer(new_healer=bob_text)
    tim_agenda.set_healer(new_healer=tim_text)
    sal_agenda.set_healer(new_healer=sal_text)
    c_text = "C"
    c_road = get_road(tim_agenda._healer, c_text)
    f_text = "F"
    f_road = get_road(c_road, f_text)
    b_text = "B"
    b_road = get_road(tim_agenda._healer, b_text)
    # for idea_x in tim_agenda._idea_dict.values():
    #     print(f"{f_road=} {idea_x.get_idea_road()=}")
    tim_agenda.set_acptfact(base=c_road, pick=f_road)

    bob_agenda.set_acptfact(base=c_road, pick=f_road)
    bob_agenda.set_acptfact(base=b_road, pick=b_road)

    casa_text = "casa"
    casa_road = get_road(sal_agenda._healer, casa_text)
    cookery_text = "clean cookery"
    cookery_road = get_road(casa_road, cookery_text)
    sal_agenda.set_acptfact(base=cookery_road, pick=cookery_road)

    x_culture.save_public_agenda(bob_agenda)
    x_culture.save_public_agenda(tim_agenda)
    x_culture.save_public_agenda(sal_agenda)

    with x_culture.get_treasury_conn() as treasury_conn:
        assert get_acptfact_catalog_table_count(treasury_conn, bob_text) == 0
        assert get_acptfact_catalog_table_count(treasury_conn, tim_text) == 0
        assert get_acptfact_catalog_table_count(treasury_conn, sal_text) == 0

    # WHEN
    x_culture.refresh_treasury_public_agendas_data()

    # THEN
    print(f"{get_acptfact_catalog_table_count(treasury_conn, bob_text)=}")
    print(f"{get_acptfact_catalog_table_count(treasury_conn, tim_text)=}")
    print(f"{get_acptfact_catalog_table_count(treasury_conn, sal_text)=}")
    with x_culture.get_treasury_conn() as treasury_conn:
        assert get_acptfact_catalog_table_count(treasury_conn, bob_text) == 2
        assert get_acptfact_catalog_table_count(treasury_conn, tim_text) == 1
        assert get_acptfact_catalog_table_count(treasury_conn, sal_text) == 1


def test_culture_get_groupunit_catalog_table_insert_sqlstr_CorrectlyPopulatesTable01(
    env_dir_setup_cleanup,
):
    # GIVEN Create example culture with 4 Healers, each with 3 Partyunits = 12 partyunit rows
    x_culture = cultureunit_shop(get_temp_env_qid(), get_test_cultures_dir())
    x_culture.refresh_treasury_public_agendas_data()

    bob_text = "bob"
    with x_culture.get_treasury_conn() as treasury_conn:
        assert get_groupunit_catalog_table_count(treasury_conn, bob_text) == 0

    # WHEN
    bob_group_x = GroupUnitCatalog(
        agenda_healer=bob_text,
        groupunit_brand="US Dollar",
        partylinks_set_by_culture_road=get_road(get_temp_env_qid(), "USA"),
    )
    bob_group_sqlstr = get_groupunit_catalog_table_insert_sqlstr(bob_group_x)
    with x_culture.get_treasury_conn() as treasury_conn:
        print(bob_group_sqlstr)
        treasury_conn.execute(bob_group_sqlstr)

    # THEN
    assert get_groupunit_catalog_table_count(treasury_conn, bob_text) == 1


def test_get_groupunit_catalog_dict_CorrectlyReturnsGroupUnitData(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_culture = cultureunit_shop(get_temp_env_qid(), get_test_cultures_dir())

    bob_text = "bob"
    tom_text = "tom"
    elu_text = "elu"
    bob_agenda = agendaunit_shop(_healer=bob_text)
    tom_agenda = agendaunit_shop(_healer=tom_text)
    bob_agenda.add_partyunit(pid=tom_text)
    tom_agenda.add_partyunit(pid=bob_text)
    tom_agenda.add_partyunit(pid=elu_text)
    x_culture.save_public_agenda(bob_agenda)
    x_culture.save_public_agenda(tom_agenda)
    x_culture.refresh_treasury_public_agendas_data()
    sqlstr = get_table_count_sqlstr("groupunit_catalog")
    assert get_single_result(x_culture.get_treasury_conn(), sqlstr) == 3

    # WHEN
    with x_culture.get_treasury_conn() as treasury_conn:
        print("try to grab GroupUnit data")
        groupunit_catalog_dict = get_groupunit_catalog_dict(db_conn=treasury_conn)

    # THEN
    assert len(groupunit_catalog_dict) == 3
    bob_agenda_tom_group = f"{bob_text} {tom_text}"
    tom_bob_agenda_group = f"{tom_text} {bob_text}"
    tom_agenda_elu_group = f"{tom_text} {elu_text}"
    assert groupunit_catalog_dict.get(bob_agenda_tom_group) != None
    assert groupunit_catalog_dict.get(tom_bob_agenda_group) != None
    assert groupunit_catalog_dict.get(tom_agenda_elu_group) != None
