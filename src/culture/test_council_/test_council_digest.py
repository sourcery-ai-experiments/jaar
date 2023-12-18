from src.agenda.agenda import agendaunit_shop, originunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
)
from src.agenda.x_func import (
    open_file as x_func_open_file,
    count_files as x_func_count_files,
)
from src.culture.council import councilunit_shop
from src.culture.examples.example_councils import (
    get_2node_agenda as example_healers_get_2node_agenda,
    get_7nodeJRoot_agenda as example_healers_get_7nodeJRoot_agenda,
)
from src.culture.examples.council_env_kit import (
    council_dir_setup_cleanup,
    get_temp_councilunit_dir,
    get_temp_culture_id,
)
from os import path as os_path
from pytest import raises as pytest_raises


# def test_healer_save_seed_agenda_CreateStartingAgendaFile(
#     council_dir_setup_cleanup,
# ):
#     # GIVEN
#     lai_pid = "Lai"
#     env_dir = get_temp_councilunit_dir()
#     lai_agenda = councilunit_shop(pid=lai_pid, env_dir=env_dir)
#     lai_seed_file_name = lai_agenda._seed_file_name
#     with pytest_raises(Exception) as excinfo:
#         x_func_open_file(lai_agenda._councilunit_dir, lai_seed_file_name)
#     assert (
#         str(excinfo.value)
#         == f"Could not load file {lai_agenda._seed_file_path} (2, 'No such file or directory')"
#     )

#     # WHEN
#     lai_agenda.save_seed_agenda(
#         agenda_x=example_agendas_get_agenda_with_4_levels()
#     )

#     # THEN
#     assert x_func_open_file(lai_agenda._councilunit_dir, lai_seed_file_name) != None


def test_healeropen_seed_agenda_WhenStartingAgendaFileDoesNotExists(
    council_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    env_dir = get_temp_councilunit_dir()
    culture_id_text = get_temp_culture_id()
    x_council = councilunit_shop(
        pid=tim_text, env_dir=env_dir, culture_id=culture_id_text
    )

    # WHEN
    seed_agenda = x_council.open_seed_agenda()
    assert seed_agenda != None
    assert seed_agenda._culture_id == culture_id_text

    # THEN
    x_agenda = agendaunit_shop(_healer=tim_text)
    x_agenda.set_culture_id(get_temp_culture_id())
    x_agenda.set_agenda_metrics()
    # x_idearoot = idearoot_shop(_label=gio_text, _pad="")
    # x_idearoot.set_balancelines_empty_if_null()
    # x_idearoot.set_kids_empty_if_null()
    # x_idearoot.set_balancelink_empty_if_null()
    # x_idearoot.set_balanceheir_empty_if_null()
    # x_idearoot.set_requiredunits_empty_if_null()
    # x_idearoot.set_requiredheirs_empty_if_null()
    # x_idearoot._agenda_importance = 1
    # x_idearoot._level = 0
    # x_idearoot._ancestor_promise_count = 0
    # x_idearoot._descendant_promise_count = 0
    # x_idearoot._all_party_credit = True
    # x_idearoot._all_party_debt = True

    assert seed_agenda._idearoot == x_agenda._idearoot
    assert seed_agenda._idearoot._acptfactunits == {}
    assert list(seed_agenda._partys.keys()) == [tim_text]
    assert list(seed_agenda._groups.keys()) == [tim_text]


def test_healer_save_seed_agenda_seedPersonIDMustBeHealer(
    council_dir_setup_cleanup,
):
    # GIVEN
    gio_text = "Gio"
    env_dir = get_temp_councilunit_dir()
    x_council = councilunit_shop(gio_text, env_dir, get_temp_culture_id())
    x_agenda = example_agendas_get_agenda_with_4_levels()
    assert x_agenda._healer != gio_text

    # WHEN
    x_council.save_seed_agenda(x_agenda=x_agenda)

    # THEN
    assert x_council.open_seed_agenda()._healer == x_council._council_cid


def test_healer_open_seed_agenda_WhenStartingAgendaFileExists(
    council_dir_setup_cleanup,
):
    # GIVEN
    gio_text = "Gio"
    x_council = councilunit_shop(
        gio_text, get_temp_councilunit_dir(), get_temp_culture_id()
    )
    x_council.save_seed_agenda(x_agenda=example_agendas_get_agenda_with_4_levels())

    # WHEN
    assert x_council.open_seed_agenda() != None
    seed_agenda = x_council.open_seed_agenda()

    # THEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.set_healer(new_healer=gio_text)
    x_agenda.set_agenda_metrics()

    assert seed_agenda._idearoot._kids == x_agenda._idearoot._kids
    assert seed_agenda._idearoot == x_agenda._idearoot
    assert seed_agenda._idearoot._acptfactunits == {}
    assert seed_agenda._partys == {}
    assert seed_agenda._groups == {}
    assert seed_agenda._healer == x_council._council_cid


def test_healer_erase_seed_agenda_file_DeletesFileCorrectly(
    council_dir_setup_cleanup,
):
    # GIVEN
    gio_text = "Gio"
    env_dir = get_temp_councilunit_dir()
    x_council = councilunit_shop(gio_text, env_dir, get_temp_culture_id())
    x_council.save_seed_agenda(example_agendas_get_agenda_with_4_levels())
    file_name = x_council._seed_file_name
    assert x_func_open_file(x_council._councilunit_dir, file_name) != None

    # WHEN
    x_council.erase_seed_agenda_file()

    # THEN
    with pytest_raises(Exception) as excinfo:
        x_func_open_file(x_council._councilunit_dir, file_name)
    assert (
        str(excinfo.value)
        == f"Could not load file {x_council._councilunit_dir}/seed_agenda.json (2, 'No such file or directory')"
    )


def test_councilunit_save_agenda_to_digest_SavesFileCorrectly(
    council_dir_setup_cleanup,
):
    # GIVEN
    council_cid = "healer1"
    env_dir = get_temp_councilunit_dir()
    x_council = councilunit_shop(council_cid, env_dir, get_temp_culture_id())
    x_council.create_core_dir_and_files()
    x_agenda = example_healers_get_2node_agenda()
    src_agenda_healer = x_agenda._healer
    assert x_func_count_files(x_council._agendas_digest_dir) == 0

    # WHEN
    x_council.save_agenda_to_digest(x_agenda, src_agenda_healer=src_agenda_healer)

    # THEN
    x_agenda_file_name = f"{x_agenda._healer}.json"
    digest_file_path = f"{x_council._agendas_digest_dir}/{x_agenda_file_name}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(x_council._agendas_digest_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(x_council._agendas_digest_dir) == 1
    digest_x_agenda_json = x_func_open_file(
        dest_dir=x_council._agendas_digest_dir,
        file_name=f"{src_agenda_healer}.json",
    )
    assert digest_x_agenda_json == x_agenda.get_json()


def test_presonunit__set_depotlink_CorrectlySets_blind_trust_DigestAgenda(
    council_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_temp_councilunit_dir()
    sue_agenda = councilunit_shop(sue_text, env_dir, get_temp_culture_id())
    sue_agenda.create_core_dir_and_files()
    x_agenda = example_healers_get_2node_agenda()
    src_agenda_healer = x_agenda._healer
    assert x_func_count_files(sue_agenda._agendas_digest_dir) == 0
    print(f"{x_agenda._culture_id=}")

    # WHEN
    sue_agenda.set_depot_agenda(x_agenda=x_agenda, depotlink_type="blind_trust")

    # THEN
    x_agenda_file_name = f"{x_agenda._healer}.json"
    digest_file_path = f"{sue_agenda._agendas_digest_dir}/{x_agenda_file_name}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(sue_agenda._agendas_digest_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(sue_agenda._agendas_digest_dir) == 1
    digest_x_agenda_json = x_func_open_file(
        dest_dir=sue_agenda._agendas_digest_dir,
        file_name=f"{src_agenda_healer}.json",
    )
    assert digest_x_agenda_json == x_agenda.get_json()


def test_healer_get_remelded_output_agenda_withEmptyDigestDict(
    council_dir_setup_cleanup,
):
    # GIVEN
    council_cid_x = "boots3"
    x_council = councilunit_shop(
        council_cid_x, get_temp_councilunit_dir(), get_temp_culture_id()
    )
    x_council.create_core_dir_and_files()
    x_agenda_output_before = x_council.get_remelded_output_agenda()
    assert str(type(x_agenda_output_before)).find(".agenda.AgendaUnit'>")
    assert x_agenda_output_before._healer == council_cid_x
    assert x_agenda_output_before._idearoot._label == get_temp_culture_id()
    # x_council.set_digested_agenda(agenda_x=agendaunit_shop(_healer="digested1"))

    # WHEN
    sx_output_after = x_council.get_remelded_output_agenda()

    # THEN
    healer_agenda_x = agendaunit_shop(_healer=council_cid_x, _weight=0.0)
    healer_agenda_x.set_culture_id(get_temp_culture_id())
    healer_agenda_x._idearoot._pad = ""
    healer_agenda_x.set_agenda_metrics()

    assert str(type(sx_output_after)).find(".agenda.AgendaUnit'>")
    assert sx_output_after._weight == healer_agenda_x._weight
    assert sx_output_after._idearoot._pad == healer_agenda_x._idearoot._pad
    assert (
        sx_output_after._idearoot._acptfactunits
        == healer_agenda_x._idearoot._acptfactunits
    )
    assert sx_output_after._idearoot == healer_agenda_x._idearoot


def test_healer_get_remelded_output_agenda_with1DigestedAgenda(
    council_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    env_dir = get_temp_councilunit_dir()
    x_council = councilunit_shop(yao_text, env_dir, get_temp_culture_id())
    x_council.create_core_dir_and_files()
    x_agenda_output_before = x_council.get_remelded_output_agenda()
    assert str(type(x_agenda_output_before)).find(".agenda.AgendaUnit'>")
    assert x_agenda_output_before._healer == yao_text
    assert x_agenda_output_before._idearoot._label == get_temp_culture_id()
    input_agenda = example_healers_get_2node_agenda()
    input_agenda.meld(input_agenda)
    x_council.set_depot_agenda(x_agenda=input_agenda, depotlink_type="blind_trust")

    # WHEN
    new_output_agenda = x_council.get_remelded_output_agenda()

    # THEN
    assert str(type(new_output_agenda)).find(".agenda.AgendaUnit'>")

    assert new_output_agenda._weight == 0
    assert new_output_agenda._weight != input_agenda._weight
    sx_idearoot = new_output_agenda._idearoot
    input_idearoot = input_agenda._idearoot
    assert sx_idearoot._pad == input_idearoot._pad
    assert sx_idearoot._acptfactunits == input_idearoot._acptfactunits
    input_b_idea = input_idearoot._kids.get("B")
    new_output_agenda_b_idea = sx_idearoot._kids.get("B")
    assert new_output_agenda_b_idea._pad == input_b_idea._pad
    assert new_output_agenda._idearoot._kids == input_agenda._idearoot._kids
    assert sx_idearoot._kids_total_weight == input_idearoot._kids_total_weight
    assert sx_idearoot == input_idearoot
    assert new_output_agenda._healer != input_agenda._healer
    assert new_output_agenda != input_agenda


# def test_healer_set_digested_agenda_with2Groups(council_dir_setup_cleanup):
#     # GIVEN
#     env_dir = get_temp_councilunit_dir()
#     x_council = councilunit_shop(pid="test8", env_dir=env_dir)
#     x_agenda_output_before = x_council.get_remelded_output_agenda()
#     assert str(type(x_agenda_output_before)).find(".agenda.AgendaUnit'>")
#     assert x_agenda_output_before._groups == {}
#     assert x_agenda_output_before._partys == {}
#     assert x_agenda_output_before._acptfacts == {}

#     src1 = "test1"
#     src1_road = f"{src1}"
#     s1 = agendaunit_shop(_healer=src1)

#     ceci_text = "Ceci"
#     s1.set_partyunit(partyunit=PartyUnit(pid=ceci_text))
#     swim_text = "swimmers"
#     swim_group = BraUnit(pid=swim_text)
#     swim_group.set_partylink(partylink=partylink_shop(pid=ceci_text))
#     s1.set_groupunit(groupunit=swim_group)

#     yaya_text = "yaya"
#     yaya_road = f"{src1},{yaya_text}"
#     s1.add_idea(ideacore_shop(yaya_text), pad=src1_road)
#     s1.set_acptfact(base=yaya_road, acptfact=yaya_road)

#     assert s1._groups.get(swim_text).pid == swim_text
#     assert s1._partys.get(ceci_text).pid == ceci_text
#     assert s1._idearoot._label == src1
#     assert s1._acptfacts.get(yaya_road).base == yaya_road

#     # WHEN
#     x_council.set_single_digested_agenda(_agenda_healer="test1", digest_agenda_x=s1)
#     new_output_agenda = x_council.get_remelded_output_agenda()

#     # THEN
#     assert str(type(new_output_agenda)).find(".agenda.AgendaUnit'>")
#     assert new_output_agenda._acptfacts == s1._acptfacts
#     assert new_output_agenda._partys == s1._partys
#     assert new_output_agenda._groups == s1._groups
#     assert new_output_agenda._weight == s1._weight
#     assert new_output_agenda._weight == s1._weight
#     assert new_output_agenda._idearoot._pad == s1._idearoot._pad
#     assert new_output_agenda._idearoot._acptfactunits == s1._idearoot._acptfactunits
#     assert new_output_agenda._idearoot._kids == s1._idearoot._kids
#     assert new_output_agenda._idearoot._kids_total_weight == s1._idearoot._kids_total_weight
#     assert new_output_agenda._idearoot == s1._idearoot
#     assert new_output_agenda._label != s1._label
#     assert new_output_agenda != s1


def test_healer_seed_agenda_CorrectlysHasOriginLinksWithHealerAsSource(
    council_dir_setup_cleanup,
):
    # GIVEN
    # councilunit with seed_agenda and no other depot agendas
    yao_text = "Yao"
    seed_origin_weight = 1
    yao_originunit = originunit_shop()
    yao_originunit.set_originlink(pid=yao_text, weight=seed_origin_weight)
    seed_agenda_x = example_healers_get_7nodeJRoot_agenda()
    seed_agenda_x.set_healer(yao_text)

    assert seed_agenda_x._idearoot._originunit == originunit_shop()
    assert seed_agenda_x._idearoot._originunit != yao_originunit

    x_council = councilunit_shop(
        yao_text, get_temp_councilunit_dir(), get_temp_culture_id()
    )
    x_council.create_core_dir_and_files()
    x_council.save_seed_agenda(x_agenda=seed_agenda_x)

    # WHEN
    output_agenda_x = x_council.get_remelded_output_agenda()

    # THEN
    print(f"{output_agenda_x._culture_id=} {output_agenda_x._idearoot._label=}")
    print(f"{output_agenda_x._idearoot._kids.keys()=}")
    assert output_agenda_x._idearoot._originunit == originunit_shop()
    a_road = output_agenda_x.make_road(output_agenda_x._culture_id, "A")
    c_road = output_agenda_x.make_road(output_agenda_x._culture_id, "C")
    d_road = output_agenda_x.make_road(c_road, "D")
    print(f"{d_road=}")
    d_idea = output_agenda_x.get_idea_kid(d_road)
    assert d_idea._originunit == yao_originunit

    print(f"{output_agenda_x._originunit=}")
    assert output_agenda_x._originunit == yao_originunit

    output_originlink = output_agenda_x._originunit._links.get(yao_text)
    assert output_originlink.pid == yao_text
    assert output_originlink.weight == seed_origin_weight
