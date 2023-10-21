from src.agenda.agenda import agendaunit_shop, originunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
)
from src.agenda.x_func import (
    open_file as x_func_open_file,
    count_files as x_func_count_files,
)
from src.culture.kitchen import kitchenunit_shop
from src.culture.examples.example_kitchens import (
    get_2node_agenda as example_healers_get_2node_agenda,
    get_7nodeJRoot_agenda as example_healers_get_7nodeJRoot_agenda,
)
from src.culture.examples.kitchen_env_kit import (
    kitchen_dir_setup_cleanup,
    get_temp_kitchenunit_dir,
    get_temp_culture_handle,
)
from os import path as os_path
from pytest import raises as pytest_raises


# def test_healer_save_seed_agenda_CreateStartingDealFile(
#     kitchen_dir_setup_cleanup,
# ):
#     # GIVEN
#     lai_title = "Lai"
#     env_dir = get_temp_kitchenunit_dir()
#     lai_agenda = kitchenunit_shop(title=lai_title, env_dir=env_dir)
#     lai_seed_file_title = lai_agenda._admin._seed_file_title
#     with pytest_raises(Exception) as excinfo:
#         x_func_open_file(lai_agenda._admin._kitchenunit_dir, lai_seed_file_title)
#     assert (
#         str(excinfo.value)
#         == f"Could not load file {lai_agenda._admin._seed_file_path} (2, 'No such file or directory')"
#     )

#     # WHEN
#     lai_agenda._admin.save_seed_agenda(
#         agenda_x=example_agendas_get_agenda_with_4_levels()
#     )

#     # THEN
#     assert x_func_open_file(lai_agenda._admin._kitchenunit_dir, lai_seed_file_title) != None


def test_healeropen_seed_agenda_WhenStartingDealFileDoesNotExists(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    env_dir = get_temp_kitchenunit_dir()
    culture_handle_text = get_temp_culture_handle()
    ux = kitchenunit_shop(
        title=tim_text, env_dir=env_dir, culture_handle=culture_handle_text
    )

    # WHEN
    seed_agenda = ux._admin.open_seed_agenda()
    assert seed_agenda != None
    assert seed_agenda._culture_handle == culture_handle_text

    # THEN
    x_agenda = agendaunit_shop(_healer=tim_text)
    x_agenda.set_culture_handle(get_temp_culture_handle())
    x_agenda.set_agenda_metrics()
    # x_idearoot = idearoot_shop(_label=p_title, _pad="")
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


def test_healer_save_seed_agenda_seedPersonNameMustBeHealer(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    p_title = "Game1"
    env_dir = get_temp_kitchenunit_dir()
    ux = kitchenunit_shop(p_title, env_dir, get_temp_culture_handle())
    cx1 = example_agendas_get_agenda_with_4_levels()
    assert cx1._healer != p_title

    # WHEN
    ux._admin.save_seed_agenda(x_agenda=cx1)

    # THEN
    assert ux._admin.open_seed_agenda()._healer == ux._admin._kitchen_title


def test_healer_open_seed_agenda_WhenStartingDealFileExists(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    p_title = "Game1"
    env_dir = get_temp_kitchenunit_dir()
    ux = kitchenunit_shop(p_title, env_dir, get_temp_culture_handle())
    ux._admin.save_seed_agenda(x_agenda=example_agendas_get_agenda_with_4_levels())

    # WHEN
    assert ux._admin.open_seed_agenda() != None
    seed_agenda = ux._admin.open_seed_agenda()

    # THEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.set_healer(new_healer=p_title)
    x_agenda.set_agenda_metrics()

    assert seed_agenda._idearoot._kids == x_agenda._idearoot._kids
    assert seed_agenda._idearoot == x_agenda._idearoot
    assert seed_agenda._idearoot._acptfactunits == {}
    assert seed_agenda._partys == {}
    assert seed_agenda._groups == {}
    assert seed_agenda._healer == ux._admin._kitchen_title


def test_healer_erase_seed_agenda_file_DeletesFileCorrectly(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    p_title = "Game1"
    env_dir = get_temp_kitchenunit_dir()
    ux = kitchenunit_shop(p_title, env_dir, get_temp_culture_handle())
    ux._admin.save_seed_agenda(example_agendas_get_agenda_with_4_levels())
    file_title = ux._admin._seed_file_title
    assert x_func_open_file(ux._admin._kitchenunit_dir, file_title) != None

    # WHEN
    ux._admin.erase_seed_agenda_file()

    # THEN
    with pytest_raises(Exception) as excinfo:
        x_func_open_file(ux._admin._kitchenunit_dir, file_title)
    assert (
        str(excinfo.value)
        == f"Could not load file {ux._admin._kitchenunit_dir}/seed_agenda.json (2, 'No such file or directory')"
    )


def test_kitchenunit_save_agenda_to_digest_SavesFileCorrectly(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    kitchen_title = "healer1"
    env_dir = get_temp_kitchenunit_dir()
    ux = kitchenunit_shop(kitchen_title, env_dir, get_temp_culture_handle())
    ux.create_core_dir_and_files()
    cx = example_healers_get_2node_agenda()
    src_agenda_healer = cx._healer
    assert x_func_count_files(ux._admin._agendas_digest_dir) == 0

    # WHEN
    ux._admin.save_agenda_to_digest(cx, src_agenda_healer=src_agenda_healer)

    # THEN
    cx_file_title = f"{cx._healer}.json"
    digest_file_path = f"{ux._admin._agendas_digest_dir}/{cx_file_title}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(ux._admin._agendas_digest_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(ux._admin._agendas_digest_dir) == 1
    digest_x_agenda_json = x_func_open_file(
        dest_dir=ux._admin._agendas_digest_dir,
        file_title=f"{src_agenda_healer}.json",
    )
    assert digest_x_agenda_json == cx.get_json()


def test_presonunit__set_depotlink_CorrectlySets_blind_trust_DigestDeal(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_temp_kitchenunit_dir()
    sue_cx = kitchenunit_shop(sue_text, env_dir, get_temp_culture_handle())
    sue_cx.create_core_dir_and_files()
    cx = example_healers_get_2node_agenda()
    src_agenda_healer = cx._healer
    assert x_func_count_files(sue_cx._admin._agendas_digest_dir) == 0

    # WHEN
    sue_cx.set_depot_agenda(x_agenda=cx, depotlink_type="blind_trust")

    # THEN
    cx_file_title = f"{cx._healer}.json"
    digest_file_path = f"{sue_cx._admin._agendas_digest_dir}/{cx_file_title}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(sue_cx._admin._agendas_digest_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(sue_cx._admin._agendas_digest_dir) == 1
    digest_x_agenda_json = x_func_open_file(
        dest_dir=sue_cx._admin._agendas_digest_dir,
        file_title=f"{src_agenda_healer}.json",
    )
    assert digest_x_agenda_json == cx.get_json()


def test_healer_get_remelded_output_agenda_withEmptyDigestDict(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    kitchen_title_x = "boots3"
    ux = kitchenunit_shop(
        kitchen_title_x, get_temp_kitchenunit_dir(), get_temp_culture_handle()
    )
    ux.create_core_dir_and_files()
    sx_output_before = ux._admin.get_remelded_output_agenda()
    assert str(type(sx_output_before)).find(".agenda.AgendaUnit'>")
    assert sx_output_before._healer == kitchen_title_x
    assert sx_output_before._idearoot._label == get_temp_culture_handle()
    # ux.set_digested_agenda(agenda_x=AgendaUnit(_healer="digested1"))

    # WHEN
    sx_output_after = ux._admin.get_remelded_output_agenda()

    # THEN
    healer_agenda_x = agendaunit_shop(_healer=kitchen_title_x, _weight=0.0)
    healer_agenda_x.set_culture_handle(get_temp_culture_handle())
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


def test_healer_get_remelded_output_agenda_with1DigestedDeal(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    env_dir = get_temp_kitchenunit_dir()
    ux = kitchenunit_shop(yao_text, env_dir, get_temp_culture_handle())
    ux.create_core_dir_and_files()
    sx_output_old = ux._admin.get_remelded_output_agenda()
    assert str(type(sx_output_old)).find(".agenda.AgendaUnit'>")
    assert sx_output_old._healer == yao_text
    assert sx_output_old._idearoot._label == get_temp_culture_handle()
    input_agenda = example_healers_get_2node_agenda()
    input_agenda.meld(input_agenda)
    ux.set_depot_agenda(x_agenda=input_agenda, depotlink_type="blind_trust")

    # WHEN
    sx_output_new = ux._admin.get_remelded_output_agenda()

    # THEN
    assert str(type(sx_output_new)).find(".agenda.AgendaUnit'>")

    assert sx_output_new._weight == 0
    assert sx_output_new._weight != input_agenda._weight
    sx_idearoot = sx_output_new._idearoot
    input_idearoot = input_agenda._idearoot
    assert sx_idearoot._pad == input_idearoot._pad
    assert sx_idearoot._acptfactunits == input_idearoot._acptfactunits
    input_b_idea = input_idearoot._kids.get("B")
    sx_output_new_b_idea = sx_idearoot._kids.get("B")
    assert sx_output_new_b_idea._pad == input_b_idea._pad
    assert sx_output_new._idearoot._kids == input_agenda._idearoot._kids
    assert sx_idearoot._kids_total_weight == input_idearoot._kids_total_weight
    assert sx_idearoot == input_idearoot
    assert sx_output_new._healer != input_agenda._healer
    assert sx_output_new != input_agenda


# def test_healer_set_digested_agenda_with2Groups(kitchen_dir_setup_cleanup):
#     # GIVEN
#     env_dir = get_temp_kitchenunit_dir()
#     ux = kitchenunit_shop(title="test8", env_dir=env_dir)
#     sx_output_old = ux._admin.get_remelded_output_agenda()
#     assert str(type(sx_output_old)).find(".agenda.AgendaUnit'>")
#     assert sx_output_old._groups == {}
#     assert sx_output_old._partys == {}
#     assert sx_output_old._acptfacts == {}

#     src1 = "test1"
#     src1_road = Road(f"{src1}")
#     s1 = agendaunit_shop(_healer=src1)

#     ceci_text = "Ceci"
#     s1.set_partyunit(partyunit=PartyUnit(title=ceci_text))
#     swim_text = "swimmers"
#     swim_group = BraUnit(title=swim_text)
#     swim_group.set_partylink(partylink=partylink_shop(title=ceci_text))
#     s1.set_groupunit(groupunit=swim_group)

#     yaya_text = "yaya"
#     yaya_road = Road(f"{src1},{yaya_text}")
#     s1.add_idea(idea_kid=ideacore_shop(_label=yaya_text), pad=src1_road)
#     s1.set_acptfact(base=yaya_road, acptfact=yaya_road)

#     assert s1._groups.get(swim_text).title == swim_text
#     assert s1._partys.get(ceci_text).title == ceci_text
#     assert s1._idearoot._label == src1
#     assert s1._acptfacts.get(yaya_road).base == yaya_road

#     # WHEN
#     ux.set_single_digested_agenda(_agenda_healer="test1", digest_agenda_x=s1)
#     sx_output_new = ux._admin.get_remelded_output_agenda()

#     # THEN
#     assert str(type(sx_output_new)).find(".agenda.AgendaUnit'>")
#     assert sx_output_new._acptfacts == s1._acptfacts
#     assert sx_output_new._partys == s1._partys
#     assert sx_output_new._groups == s1._groups
#     assert sx_output_new._weight == s1._weight
#     assert sx_output_new._weight == s1._weight
#     assert sx_output_new._idearoot._pad == s1._idearoot._pad
#     assert sx_output_new._idearoot._acptfactunits == s1._idearoot._acptfactunits
#     assert sx_output_new._idearoot._kids == s1._idearoot._kids
#     assert sx_output_new._idearoot._kids_total_weight == s1._idearoot._kids_total_weight
#     assert sx_output_new._idearoot == s1._idearoot
#     assert sx_output_new._label != s1._label
#     assert sx_output_new != s1


def test_healer_seed_agenda_CorrectlysHasOriginLinksWithHealerAsSource(
    kitchen_dir_setup_cleanup,
):
    # GIVEN
    # kitchenunit with seed_agenda and no other depot agendas
    yao_text = "Yao"
    seed_origin_weight = 1
    yao_originunit = originunit_shop()
    yao_originunit.set_originlink(title=yao_text, weight=seed_origin_weight)
    seed_agenda_x = example_healers_get_7nodeJRoot_agenda()
    seed_agenda_x.set_healer(yao_text)

    assert seed_agenda_x._idearoot._originunit == originunit_shop()
    assert seed_agenda_x._idearoot._originunit != yao_originunit

    ux = kitchenunit_shop(
        yao_text, get_temp_kitchenunit_dir(), get_temp_culture_handle()
    )
    ux.create_core_dir_and_files()
    ux._admin.save_seed_agenda(x_agenda=seed_agenda_x)

    # WHEN
    output_agenda_x = ux._admin.get_remelded_output_agenda()

    # THEN
    assert output_agenda_x._idearoot._originunit == originunit_shop()
    d_road = "J,A,C,D"
    d_idea = output_agenda_x.get_idea_kid(road=d_road)
    assert d_idea._originunit == yao_originunit

    print(f"{output_agenda_x._originunit=}")
    assert output_agenda_x._originunit == yao_originunit

    output_originlink = output_agenda_x._originunit._links.get(yao_text)
    assert output_originlink.title == yao_text
    assert output_originlink.weight == seed_origin_weight
