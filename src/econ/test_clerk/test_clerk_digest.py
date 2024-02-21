from src.agenda.agenda import agendaunit_shop, originunit_shop
from src.agenda.examples.example_agendas import (
    get_agenda_with_4_levels as example_agendas_get_agenda_with_4_levels,
)
from src.instrument.file import open_file, count_files
from src.econ.clerk import clerkunit_shop
from src.econ.examples.example_clerks import (
    get_2node_agenda as example_get_2node_agenda,
    get_7nodeJRoot_agenda as example_get_7nodeJRoot_agenda,
)
from src.econ.examples.clerk_env_kit import (
    clerk_dir_setup_cleanup,
    get_temp_clerkunit_dir,
    get_temp_econ_id,
)
from os import path as os_path
from pytest import raises as pytest_raises


# def test_ClerkUnit_save_role_agenda_CreateStartingAgendaFile(
#     clerk_dir_setup_cleanup,
# ):
#     # GIVEN
#     lai_worker_id = "Lai"
#     env_dir = get_temp_clerkunit_dir()
#     lai_agenda = clerkunit_shop(worker_id=lai_worker_id, env_dir=env_dir)
#     lai_role_file_name = lai_agenda._role_file_name
#     with pytest_raises(Exception) as excinfo:
#         open_file(lai_agenda._clerkunit_dir, lai_role_file_name)
#     assert (
#         str(excinfo.value)
#         == f"Could not load file {lai_agenda._role_file_path} (2, 'No such file or directory')"
#     )

#     # WHEN
#     lai_agenda.save_role_agenda(
#         agenda_x=example_agendas_get_agenda_with_4_levels()
#     )

#     # THEN
#     assert open_file(lai_agenda._clerkunit_dir, lai_role_file_name) != None


def test_ClerkUnitopen_role_file_WhenStartingAgendaFileDoesNotExists(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    tim_text = "Tim"
    env_dir = get_temp_clerkunit_dir()
    econ_id_text = get_temp_econ_id()
    x_clerk = clerkunit_shop(worker_id=tim_text, env_dir=env_dir, econ_id=econ_id_text)

    # WHEN
    role_agenda = x_clerk.open_role_file()
    assert role_agenda != None
    assert role_agenda._world_id == econ_id_text

    # THEN
    x_agenda = agendaunit_shop(_worker_id=tim_text)
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda.set_agenda_metrics()
    # x_idearoot = ideaunit_shop(_root=True, _label=gio_text, _parent_road="")
    # x_idearoot._agenda_importance = 1
    # x_idearoot._level = 0
    # x_idearoot._ancestor_promise_count = 0
    # x_idearoot._descendant_promise_count = 0
    # x_idearoot._all_party_credit = True
    # x_idearoot._all_party_debt = True

    assert role_agenda._idearoot == x_agenda._idearoot
    assert role_agenda._idearoot._beliefunits == {}
    assert list(role_agenda._partys.keys()) == [tim_text]
    assert list(role_agenda._groups.keys()) == [tim_text]


def test_ClerkUnit_save_role_agenda_rolePersonIDMustBeHealer(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    gio_text = "Gio"
    env_dir = get_temp_clerkunit_dir()
    x_clerk = clerkunit_shop(gio_text, env_dir, get_temp_econ_id())
    x_agenda = example_agendas_get_agenda_with_4_levels()
    assert x_agenda._worker_id != gio_text

    # WHEN
    x_clerk.save_role_agenda(x_agenda=x_agenda)

    # THEN
    assert x_clerk.open_role_file()._worker_id == x_clerk._clerk_id


def test_ClerkUnit_open_role_file_WhenStartingAgendaFileExists(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    gio_text = "Gio"
    x_clerk = clerkunit_shop(gio_text, get_temp_clerkunit_dir(), get_temp_econ_id())
    x_clerk.save_role_agenda(x_agenda=example_agendas_get_agenda_with_4_levels())

    # WHEN
    assert x_clerk.open_role_file() != None
    role_agenda = x_clerk.open_role_file()

    # THEN
    x_agenda = example_agendas_get_agenda_with_4_levels()
    x_agenda.set_worker_id(new_worker_id=gio_text)
    x_agenda.set_agenda_metrics()

    assert role_agenda._idearoot._kids == x_agenda._idearoot._kids
    assert role_agenda._idearoot == x_agenda._idearoot
    assert role_agenda._idearoot._beliefunits == {}
    assert role_agenda._partys == {}
    assert role_agenda._groups == {}
    assert role_agenda._worker_id == x_clerk._clerk_id


def test_ClerkUnit_erase_role_agenda_file_DeletesFileCorrectly(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    gio_text = "Gio"
    env_dir = get_temp_clerkunit_dir()
    x_clerk = clerkunit_shop(gio_text, env_dir, get_temp_econ_id())
    x_clerk.save_role_agenda(example_agendas_get_agenda_with_4_levels())
    file_name = x_clerk._role_file_name
    assert open_file(x_clerk._clerkunit_dir, file_name) != None

    # WHEN
    x_clerk.erase_role_agenda_file()

    # THEN
    with pytest_raises(Exception) as excinfo:
        open_file(x_clerk._clerkunit_dir, file_name)
    assert (
        str(excinfo.value)
        == f"Could not load file {x_clerk._clerkunit_dir}/role_agenda.json (2, 'No such file or directory')"
    )


def test_clerkunit_save_agenda_to_digest_SavesFileCorrectly(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    clerk_id = "Yao"
    env_dir = get_temp_clerkunit_dir()
    x_clerk = clerkunit_shop(clerk_id, env_dir, get_temp_econ_id())
    x_clerk.create_core_dir_and_files()
    x_agenda = example_get_2node_agenda()
    src_worker_id = x_agenda._worker_id
    assert count_files(x_clerk._agendas_digest_dir) == 0

    # WHEN
    x_clerk.save_agenda_to_digest(x_agenda, src_worker_id=src_worker_id)

    # THEN
    x_agenda_file_name = f"{x_agenda._worker_id}.json"
    digest_file_path = f"{x_clerk._agendas_digest_dir}/{x_agenda_file_name}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(x_clerk._agendas_digest_dir):
    #     print(f"{path_x=}")
    assert count_files(x_clerk._agendas_digest_dir) == 1
    digest_x_agenda_json = open_file(
        dest_dir=x_clerk._agendas_digest_dir,
        file_name=f"{src_worker_id}.json",
    )
    assert digest_x_agenda_json == x_agenda.get_json()


def test_presonunit__set_depotlink_CorrectlySets_blind_trust_DigestAgenda(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_temp_clerkunit_dir()
    sue_agenda = clerkunit_shop(sue_text, env_dir, get_temp_econ_id())
    sue_agenda.create_core_dir_and_files()
    x_agenda = example_get_2node_agenda()
    src_worker_id = x_agenda._worker_id
    assert count_files(sue_agenda._agendas_digest_dir) == 0
    print(f"{x_agenda._world_id=}")

    # WHEN
    sue_agenda.set_depot_agenda(x_agenda=x_agenda, depotlink_type="blind_trust")

    # THEN
    x_agenda_file_name = f"{x_agenda._worker_id}.json"
    digest_file_path = f"{sue_agenda._agendas_digest_dir}/{x_agenda_file_name}"
    print(f"Saving to {digest_file_path=}")
    assert os_path.exists(digest_file_path)
    # for path_x in os_scandir(sue_agenda._agendas_digest_dir):
    #     print(f"{path_x=}")
    assert count_files(sue_agenda._agendas_digest_dir) == 1
    digest_x_agenda_json = open_file(
        dest_dir=sue_agenda._agendas_digest_dir,
        file_name=f"{src_worker_id}.json",
    )
    assert digest_x_agenda_json == x_agenda.get_json()


def test_ClerkUnit_get_remelded_output_agenda_withEmptyDigestDict(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    clerk_id_x = "boots3"
    x_clerk = clerkunit_shop(clerk_id_x, get_temp_clerkunit_dir(), get_temp_econ_id())
    x_clerk.create_core_dir_and_files()
    x_agenda_output_before = x_clerk.get_remelded_output_agenda()
    assert str(type(x_agenda_output_before)).find(".agenda.AgendaUnit'>")
    assert x_agenda_output_before._worker_id == clerk_id_x
    assert x_agenda_output_before._idearoot._label == get_temp_econ_id()
    # x_clerk.set_digested_agenda(agenda_x=agendaunit_shop(_worker_id="digested1"))

    # WHEN
    sx_output_after = x_clerk.get_remelded_output_agenda()

    # THEN
    x_agenda = agendaunit_shop(_worker_id=clerk_id_x, _weight=0.0)
    x_agenda.set_world_id(get_temp_econ_id())
    x_agenda._idearoot._parent_road = ""
    x_agenda.set_agenda_metrics()

    assert str(type(sx_output_after)).find(".agenda.AgendaUnit'>")
    assert sx_output_after._weight == x_agenda._weight
    assert sx_output_after._idearoot._parent_road == x_agenda._idearoot._parent_road
    assert sx_output_after._idearoot._beliefunits == x_agenda._idearoot._beliefunits
    assert sx_output_after._idearoot == x_agenda._idearoot


def test_ClerkUnit_get_remelded_output_agenda_with1DigestedAgenda(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    env_dir = get_temp_clerkunit_dir()
    yao_clerk = clerkunit_shop(yao_text, env_dir, get_temp_econ_id())
    yao_clerk.create_core_dir_and_files()
    x_agenda_output_before = yao_clerk.get_remelded_output_agenda()
    assert str(type(x_agenda_output_before)).find(".agenda.AgendaUnit'>")
    assert x_agenda_output_before._worker_id == yao_text
    assert x_agenda_output_before._idearoot._label == get_temp_econ_id()
    input_agenda = example_get_2node_agenda()
    input_agenda.meld(input_agenda)
    input_idearoot = input_agenda._idearoot
    input_b_idea = input_idearoot.get_kid("B")
    assert input_b_idea._agenda_world_id == get_temp_econ_id()
    yao_clerk.set_depot_agenda(x_agenda=input_agenda, depotlink_type="blind_trust")

    # WHEN
    new_output_agenda = yao_clerk.get_remelded_output_agenda()

    # THEN
    assert str(type(new_output_agenda)).find(".agenda.AgendaUnit'>")

    assert new_output_agenda._weight == 0
    assert new_output_agenda._weight != input_agenda._weight
    assert new_output_agenda._world_id == input_agenda._world_id
    sx_idearoot = new_output_agenda._idearoot
    assert sx_idearoot._agenda_world_id == input_idearoot._agenda_world_id
    assert sx_idearoot._parent_road == input_idearoot._parent_road
    assert sx_idearoot._beliefunits == input_idearoot._beliefunits
    new_output_agenda_b_idea = sx_idearoot.get_kid("B")
    assert new_output_agenda_b_idea._parent_road == input_b_idea._parent_road
    assert new_output_agenda_b_idea._agenda_world_id == input_b_idea._agenda_world_id
    assert new_output_agenda._idearoot._kids == input_agenda._idearoot._kids
    assert sx_idearoot._kids_total_weight == input_idearoot._kids_total_weight
    assert sx_idearoot == input_idearoot
    assert new_output_agenda._worker_id != input_agenda._worker_id
    assert new_output_agenda != input_agenda


# def test_ClerkUnit_set_digested_agenda_with2Groups(clerk_dir_setup_cleanup):
#     # GIVEN
#     env_dir = get_temp_clerkunit_dir()
#     x_clerk = clerkunit_shop(worker_id="test8", env_dir=env_dir)
#     x_agenda_output_before = x_clerk.get_remelded_output_agenda()
#     assert str(type(x_agenda_output_before)).find(".agenda.AgendaUnit'>")
#     assert x_agenda_output_before._groups == {}
#     assert x_agenda_output_before._partys == {}
#     assert x_agenda_output_before._beliefs == {}

#     src1 = "test1"
#     src1_road = f"{src1}"
#     s1 = agendaunit_shop(_worker_id=src1)

#     ceci_text = "Ceci"
#     s1.set_partyunit(partyunit=PartyUnit(worker_id=ceci_text))
#     swim_text = "swimmers"
#     swim_group = BraUnit(worker_id=swim_text)
#     swim_group.set_partylink(partylink=partylink_shop(party_id=ceci_text))
#     s1.set_groupunit(y_groupunit=swim_group)

#     yaya_text = "yaya"
#     yaya_road = create_road(src1,yaya_text)
#     s1.add_idea(ideaunit_shop(yaya_text), parent_road=src1_road)
#     s1.set_belief(base=yaya_road, belief=yaya_road)

#     assert s1._groups.get(swim_text).worker_id == swim_text
#     assert s1._partys.get(ceci_text).worker_id == ceci_text
#     assert s1._idearoot._label == src1
#     assert s1._beliefs.get(yaya_road).base == yaya_road

#     # WHEN
#     x_clerk.set_single_digested_agenda(_worker_id="test1", digest_agenda_x=s1)
#     new_output_agenda = x_clerk.get_remelded_output_agenda()

#     # THEN
#     assert str(type(new_output_agenda)).find(".agenda.AgendaUnit'>")
#     assert new_output_agenda._beliefs == s1._beliefs
#     assert new_output_agenda._partys == s1._partys
#     assert new_output_agenda._groups == s1._groups
#     assert new_output_agenda._weight == s1._weight
#     assert new_output_agenda._weight == s1._weight
#     assert new_output_agenda._idearoot._parent_road == s1._idearoot._parent_road
#     assert new_output_agenda._idearoot._beliefunits == s1._idearoot._beliefunits
#     assert new_output_agenda._idearoot._kids == s1._idearoot._kids
#     assert new_output_agenda._idearoot._kids_total_weight == s1._idearoot._kids_total_weight
#     assert new_output_agenda._idearoot == s1._idearoot
#     assert new_output_agenda._label != s1._label
#     assert new_output_agenda != s1


def test_ClerkUnit_role_agenda_CorrectlysHasOriginLinksWithHealerAsSource(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    # clerkunit with role_agenda and no other depot agendas
    yao_text = "Yao"
    role_origin_weight = 1
    yao_originunit = originunit_shop()
    yao_originunit.set_originlink(party_id=yao_text, weight=role_origin_weight)
    role_agenda_x = example_get_7nodeJRoot_agenda()
    role_agenda_x.set_worker_id(yao_text)

    assert role_agenda_x._idearoot._originunit == originunit_shop()
    assert role_agenda_x._idearoot._originunit != yao_originunit

    x_clerk = clerkunit_shop(yao_text, get_temp_clerkunit_dir(), get_temp_econ_id())
    x_clerk.create_core_dir_and_files()
    x_clerk.save_role_agenda(x_agenda=role_agenda_x)

    # WHEN
    output_agenda_x = x_clerk.get_remelded_output_agenda()

    # THEN
    print(f"{output_agenda_x._world_id=} {output_agenda_x._idearoot._label=}")
    print(f"{output_agenda_x._idearoot._kids.keys()=}")
    assert output_agenda_x._idearoot._originunit == originunit_shop()
    a_road = output_agenda_x.make_l1_road("A")
    c_road = output_agenda_x.make_l1_road("C")
    d_road = output_agenda_x.make_road(c_road, "D")
    print(f"{d_road=}")
    d_idea = output_agenda_x.get_idea_obj(d_road)
    assert d_idea._originunit == yao_originunit

    print(f"{output_agenda_x._originunit=}")
    assert output_agenda_x._originunit == yao_originunit

    output_originlink = output_agenda_x._originunit._links.get(yao_text)
    assert output_originlink.party_id == yao_text
    assert output_originlink.weight == role_origin_weight
