from src.agenda.agenda import agendaunit_shop, get_from_json as agendaunit_get_from_json
from src.instrument.file import count_files, open_file
from src.econ.clerk import clerkunit_shop
from src.econ.examples.example_clerks import (
    get_2node_agenda,
    get_agenda_2CleanNodesRandomWeights as get_cal2nodes,
    get_agenda_3CleanNodesRandomWeights as get_cal3nodes,
    get_agenda_assignment_laundry_example1 as get_amer_assign_ex,
)
from src.econ.examples.clerk_env_kit import (
    clerk_dir_setup_cleanup,
    get_temp_clerkunit_dir,
    get_temp_econ_id,
    create_agenda_file,
)
from src.econ.examples.econ_env_kit import get_temp_env_econ_id
from src.econ.econ import econunit_shop
from os.path import exists as os_path_exists
from pytest import raises as pytest_raises


def test_ClerkUnit_open_job_agenda_ReturnsEmptyAgendaIfNoFileExists(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_clerkunit_dir()
    econ_id = get_temp_env_econ_id()
    x_econ = econunit_shop(econ_id=econ_id, econ_dir=env_dir)
    yao_text = "Yao"
    x_econ.create_new_clerkunit(clerk_id=yao_text)
    yao_clerkunit = x_econ.get_clerkunit(clerk_id=yao_text)
    ernie_text = "ernie"
    ernie_filename = f"{ernie_text}.json"
    assert os_path_exists(f"{x_econ.get_forum_dir()}/{ernie_filename}") == False

    # WHEN
    ernie_agendaunit = yao_clerkunit.open_job_agenda(ernie_text)

    # THEN
    assert ernie_agendaunit == agendaunit_shop()
    assert os_path_exists(f"{x_econ.get_forum_dir()}/{ernie_filename}") == False


def test_ClerkUnit_set_depotlink_RaisesErrorWhenAgendaDoesNotExist(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_temp_clerkunit_dir()
    sue_agenda = clerkunit_shop(sue_text, env_dir, get_temp_econ_id())
    sue_agenda.set_role_if_empty()
    tim_text = "Tim"
    assert list(sue_agenda._role._partys.keys()) == [sue_text]

    # WHEN / THEN
    file_path_x = f"{sue_agenda._agendas_depot_dir}/{tim_text}.json"
    print(f"{file_path_x=}")
    with pytest_raises(Exception) as excinfo:
        sue_agenda._set_depotlink(outer_owner_id=tim_text)
    assert (
        str(excinfo.value)
        == f"owner_id {sue_text} cannot find agenda {tim_text} in {file_path_x}"
    )


def test_ClerkUnit_set_depotlink_CorrectlySetsrolePartys(clerk_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    env_dir = get_temp_clerkunit_dir()
    yao_ux = clerkunit_shop(yao_text, env_dir, get_temp_econ_id())
    yao_ux.set_role_if_empty()
    sue_text = "Sue"
    create_agenda_file(yao_ux._agendas_depot_dir, sue_text)
    assert list(yao_ux._role._partys.keys()) == [yao_text]

    # WHEN
    yao_ux._set_depotlink(outer_owner_id=sue_text)

    # THEN
    assert list(yao_ux._role._partys.keys()) == [yao_text, sue_text]
    assert yao_ux._role.get_party(sue_text).depotlink_type is None


# def test_ClerkUnit_set_partyunit_depotlink_CorrectlySetsrolePartysWhen_depotlink_type_IsNone(
#     clerk_dir_setup_cleanup,
# ):
#     # GIVEN
#     yao_text = "Yao"
#     env_dir = get_temp_clerkunit_dir()
#     yao_ux = clerkunit_shop(yao_text, env_dir, get_temp_econ_id())
#     yao_ux.set_role_if_empty()
#     sue_text = "Sue"
#     create_agenda_file(yao_ux._agendas_depot_dir, sue_text)
#     assert list(yao_ux._role._partys.keys()) == [yao_text]

#     # WHEN
#     yao_ux._set_partyunit_depotlink(sue_text)

#     # THEN
#     assert list(yao_ux._role._partys.keys()) == [yao_text, sue_text]
#     assert yao_ux._role.get_party(sue_text).depotlink_type is None


def test_ClerkUnit_set_depotlink_CorrectlySetsAssignment(clerk_dir_setup_cleanup):
    # GIVEN
    amer_agenda = get_amer_assign_ex()
    print(f"{len(amer_agenda._idea_dict)=}")
    cali_text = "Cali"
    cali_ux = clerkunit_shop(cali_text, get_temp_clerkunit_dir(), get_temp_econ_id())
    cali_ux.create_core_dir_and_files()
    cali_ux.set_role_if_empty()
    cali_ux.save_agenda_to_depot(amer_agenda)
    assert cali_ux.get_role().get_party(amer_agenda._owner_id) is None
    amer_digest_path = f"{cali_ux._agendas_digest_dir}/{amer_agenda._owner_id}.json"
    assert os_path_exists(amer_digest_path) is False

    # WHEN
    assignment_text = "assignment"
    print("next set depotlink")
    cali_ux._set_depotlink(amer_agenda._owner_id, link_type=assignment_text)
    print("after set depotlink")

    # THEN
    assert (
        cali_ux.get_role().get_party(amer_agenda._owner_id).depotlink_type
        == assignment_text
    )
    assert os_path_exists(amer_digest_path)
    digest_agenda = agendaunit_get_from_json(
        open_file(
            dest_dir=cali_ux._agendas_digest_dir,
            file_name=f"{amer_agenda._owner_id}.json",
        )
    )
    print(f"{digest_agenda._owner_id=}")
    print(f"{len(digest_agenda._idea_dict)=}")
    digest_agenda.set_agenda_metrics()
    assert len(digest_agenda._idea_dict) == 9
    assert digest_agenda._owner_id == cali_text


def test_ClerkUnit_del_depot_agenda_CorrectlyDeletesObj(clerk_dir_setup_cleanup):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_clerkunit_dir()
    bob_agenda = clerkunit_shop(bob_text, env_dir, get_temp_econ_id())
    yao_text = "Yao"
    create_agenda_file(bob_agenda._agendas_depot_dir, yao_text)
    assignment_text = "assignment"
    bob_agenda._set_depotlink(yao_text, link_type=assignment_text)
    assert list(bob_agenda._role._partys.keys()) == [bob_text, yao_text]
    assert bob_agenda._role.get_party(yao_text).depotlink_type == assignment_text

    # WHEN
    bob_agenda.del_depot_agenda(owner_id=yao_text)

    # THEN
    assert list(bob_agenda._role._partys.keys()) == [bob_text, yao_text]
    assert bob_agenda._role.get_party(yao_text).depotlink_type is None


def test_ClerkUnit_del_depot_agenda_CorrectlyDeletesBlindTrustFile(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_clerkunit_dir()
    bob_agenda = clerkunit_shop(bob_text, env_dir, get_temp_econ_id())
    lai_text = "Lai"
    create_agenda_file(bob_agenda._agendas_depot_dir, lai_text)
    bob_agenda.set_role_if_empty()
    bob_agenda._set_depotlink(lai_text, link_type="blind_trust")
    assert count_files(dir_path=bob_agenda._agendas_depot_dir) == 1
    assert count_files(dir_path=bob_agenda._agendas_digest_dir) == 1

    # WHEN
    bob_agenda.del_depot_agenda(owner_id=lai_text)

    # THEN
    assert count_files(dir_path=bob_agenda._agendas_depot_dir) == 0
    assert count_files(dir_path=bob_agenda._agendas_digest_dir) == 0


def test_ClerkUnit_set_depot_agenda_SavesFileCorrectly(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_clerkunit_dir()
    bob_agenda = clerkunit_shop(bob_text, env_dir, get_temp_econ_id())
    cal1 = get_2node_agenda()
    assert count_files(bob_agenda._agendas_depot_dir) is None  # dir does not exist

    # WHEN
    bob_agenda.set_role_if_empty()
    bob_agenda.set_depot_agenda(x_agenda=cal1, depotlink_type="blind_trust")

    # THEN
    print(f"Saving to {bob_agenda._agendas_depot_dir=}")
    # for path_x in os_scandir(ux._agendas_depot_dir):
    #     print(f"{path_x=}")
    assert count_files(bob_agenda._agendas_depot_dir) == 1


def test_ClerkUnit_delete_ignore_depotlink_CorrectlyDeletesObj(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_clerkunit_dir()
    bob_agenda = clerkunit_shop(bob_text, env_dir, get_temp_econ_id())
    yao_text = "Yao"
    create_agenda_file(bob_agenda._agendas_depot_dir, yao_text)
    assignment_text = "assignment"
    bob_agenda.set_role_if_empty()
    bob_agenda._set_depotlink(yao_text, link_type=assignment_text)
    assert list(bob_agenda._role._partys.keys()) == [bob_text, yao_text]
    assert bob_agenda._role.get_party(yao_text).depotlink_type == assignment_text

    # WHEN
    bob_agenda.del_depot_agenda(owner_id=yao_text)

    # THEN
    assert list(bob_agenda._role._partys.keys()) == [bob_text, yao_text]
    assert bob_agenda._role.get_party(yao_text).depotlink_type is None


def test_ClerkUnit_del_depot_agenda_CorrectlyDoesNotDeletesIgnoreFile(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_clerkunit_dir()
    bob_agenda = clerkunit_shop(bob_text, env_dir, get_temp_econ_id())
    zia_text = "Zia"
    create_agenda_file(bob_agenda._agendas_depot_dir, zia_text)
    bob_agenda.set_role_if_empty()
    bob_agenda._set_depotlink(zia_text, link_type="ignore")
    assert count_files(dir_path=bob_agenda._agendas_depot_dir) == 1
    assert count_files(dir_path=bob_agenda._agendas_digest_dir) == 1
    assert count_files(dir_path=bob_agenda._agendas_ignore_dir) == 1

    # WHEN
    bob_agenda.del_depot_agenda(owner_id=zia_text)

    # THEN
    assert count_files(dir_path=bob_agenda._agendas_depot_dir) == 0
    assert count_files(dir_path=bob_agenda._agendas_digest_dir) == 0
    assert count_files(dir_path=bob_agenda._agendas_ignore_dir) == 1


def test_ClerkUnit_set_ignore_agenda_file_CorrectlyUpdatesIgnoreFile(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_clerkunit_dir()
    bob_ux = clerkunit_shop(bob_text, env_dir, get_temp_econ_id())
    zia_text = "Zia"
    create_agenda_file(bob_ux._agendas_depot_dir, zia_text)
    bob_ux.set_role_if_empty()
    bob_ux._set_depotlink(zia_text, link_type="ignore")
    assert count_files(dir_path=bob_ux._agendas_ignore_dir) == 1
    cx1 = bob_ux.open_ignore_agenda(owner_id=zia_text)
    assert len(cx1._partys) == 0
    cx1.add_partyunit(party_id="Tim")
    assert len(cx1._partys) == 1

    # WHEN
    zia_agenda = agendaunit_shop(_owner_id=zia_text)
    bob_ux.set_ignore_agenda_file(zia_agenda, src_owner_id=None)

    # THEN
    cx2 = bob_ux.open_ignore_agenda(owner_id=zia_text)
    assert len(cx2._partys) == 0
    assert count_files(dir_path=bob_ux._agendas_ignore_dir) == 1


def test_ClerkUnit_refresh_depot_agendas_CorrectlyPullsAllForumAgendas(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_clerkunit_dir()
    econ_id = get_temp_env_econ_id()
    sx = econunit_shop(econ_id=econ_id, econ_dir=env_dir)
    yao_text = "Yao"
    sx.create_new_clerkunit(clerk_id=yao_text)
    yao_agenda = sx.get_clerkunit(clerk_id=yao_text)
    assert len(yao_agenda.get_remelded_output_agenda().get_idea_dict()) == 1

    ernie_text = "ernie"
    ernie_agenda = get_cal2nodes(_owner_id=ernie_text)
    steve_text = "steve"
    old_steve_agenda = get_cal2nodes(_owner_id=steve_text)
    sx.save_job_agenda_to_forum(ernie_agenda)
    sx.save_job_agenda_to_forum(old_steve_agenda)
    yao_agenda.set_depot_agenda(x_agenda=ernie_agenda, depotlink_type="blind_trust")
    yao_agenda.set_depot_agenda(x_agenda=old_steve_agenda, depotlink_type="blind_trust")

    assert len(yao_agenda.get_remelded_output_agenda().get_idea_dict()) == 4
    new_steve_agenda = get_cal3nodes(_owner_id=steve_text)
    sx.save_job_agenda_to_forum(new_steve_agenda)
    print(f"{env_dir=} {yao_agenda._forum_dir=}")
    # for file_name in dir_files(dir_path=env_dir):
    #     print(f"{bob_agenda._forum_dir=} {file_name=}")

    # for file_name in dir_files(dir_path=bob_agenda._forum_dir):
    #     print(f"{bob_agenda._forum_dir=} {file_name=}")

    # WHEN
    yao_agenda.refresh_depot_agendas()

    # THEN
    assert len(yao_agenda.get_remelded_output_agenda().get_idea_dict()) == 5
