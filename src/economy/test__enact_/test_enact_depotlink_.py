from src.agenda.agenda import agendaunit_shop, get_from_json as agenda_get_from_json
from src.agenda.x_func import (
    count_files as x_func_count_files,
    open_file as x_func_open_file,
)
from src.economy.enact import enactunit_shop
from src.economy.examples.example_enacts import (
    get_2node_agenda,
    get_agenda_2CleanNodesRandomWeights as get_cal2nodes,
    get_agenda_3CleanNodesRandomWeights as get_cal3nodes,
    get_agenda_assignment_laundry_example1 as get_amer_assign_ex,
)
from src.economy.examples.enact_env_kit import (
    enact_dir_setup_cleanup,
    get_temp_enactunit_dir,
    get_temp_economy_id,
    create_agenda_file,
)
from src.economy.examples.economy_env_kit import get_temp_env_economy_id
from src.economy.economy import economyunit_shop
from os import path as os_path
from pytest import raises as pytest_raises


def test_enactunit_set_depotlink_RaisesErrorWhenAgendaDoesNotExist(
    enact_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    env_dir = get_temp_enactunit_dir()
    sue_agenda = enactunit_shop(sue_text, env_dir, get_temp_economy_id())
    sue_agenda.set_contract_if_empty()
    tim_text = "Tim"
    assert list(sue_agenda._contract._partys.keys()) == [sue_text]

    # WHEN / THEN
    file_path_x = f"{sue_agenda._agendas_depot_dir}/{tim_text}.json"
    print(f"{file_path_x=}")
    with pytest_raises(Exception) as excinfo:
        sue_agenda._set_depotlink(outer_healer=tim_text)
    assert (
        str(excinfo.value)
        == f"Healer {sue_text} cannot find agenda {tim_text} in {file_path_x}"
    )


def test_enactunit_set_depotlink_CorrectlySetscontractPartys(
    enact_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "yao"
    env_dir = get_temp_enactunit_dir()
    yao_ux = enactunit_shop(yao_text, env_dir, get_temp_economy_id())
    yao_ux.set_contract_if_empty()
    sue_text = "sue"
    create_agenda_file(yao_ux._agendas_depot_dir, sue_text)
    assert list(yao_ux._contract._partys.keys()) == [yao_text]

    # WHEN
    yao_ux._set_depotlink(outer_healer=sue_text)

    # THEN
    assert list(yao_ux._contract._partys.keys()) == [yao_text, sue_text]
    assert yao_ux._contract.get_party(sue_text).depotlink_type is None


def test_enactunit_set_depotlink_CorrectlySetsAssignment(enact_dir_setup_cleanup):
    # GIVEN
    amer_agenda = get_amer_assign_ex()
    print(f"{len(amer_agenda._idea_dict)=}")
    cali_text = "Cali"
    cali_ux = enactunit_shop(cali_text, get_temp_enactunit_dir(), get_temp_economy_id())
    cali_ux.create_core_dir_and_files()
    cali_ux.set_contract_if_empty()
    cali_ux.save_agenda_to_depot(amer_agenda)
    assert cali_ux.get_contract().get_party(amer_agenda._healer) is None
    amer_digest_path = f"{cali_ux._agendas_digest_dir}/{amer_agenda._healer}.json"
    assert os_path.exists(amer_digest_path) is False

    # WHEN
    assignment_text = "assignment"
    cali_ux._set_depotlink(amer_agenda._healer, link_type=assignment_text)

    # THEN
    assert (
        cali_ux.get_contract().get_party(amer_agenda._healer).depotlink_type
        == assignment_text
    )
    assert os_path.exists(amer_digest_path)
    digest_agenda = agenda_get_from_json(
        x_func_open_file(
            dest_dir=cali_ux._agendas_digest_dir,
            file_name=f"{amer_agenda._healer}.json",
        )
    )
    print(f"{digest_agenda._healer=}")
    print(f"{len(digest_agenda._idea_dict)=}")
    digest_agenda.set_agenda_metrics()
    assert len(digest_agenda._idea_dict) == 9
    assert digest_agenda._healer == cali_text


def test_enactunit_del_depot_agenda_CorrectlyDeletesObj(enact_dir_setup_cleanup):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_enactunit_dir()
    bob_agenda = enactunit_shop(bob_text, env_dir, get_temp_economy_id())
    yao_text = "Yao"
    create_agenda_file(bob_agenda._agendas_depot_dir, yao_text)
    assignment_text = "assignment"
    bob_agenda._set_depotlink(yao_text, link_type=assignment_text)
    assert list(bob_agenda._contract._partys.keys()) == [bob_text, yao_text]
    assert bob_agenda._contract.get_party(yao_text).depotlink_type == assignment_text

    # WHEN
    bob_agenda.del_depot_agenda(agenda_healer=yao_text)

    # THEN
    assert list(bob_agenda._contract._partys.keys()) == [bob_text, yao_text]
    assert bob_agenda._contract.get_party(yao_text).depotlink_type is None


def test_enactunit_del_depot_agenda_CorrectlyDeletesBlindTrustFile(
    enact_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_enactunit_dir()
    bob_agenda = enactunit_shop(bob_text, env_dir, get_temp_economy_id())
    lai_text = "Lai"
    create_agenda_file(bob_agenda._agendas_depot_dir, lai_text)
    bob_agenda.set_contract_if_empty()
    bob_agenda._set_depotlink(lai_text, link_type="blind_trust")
    assert x_func_count_files(dir_path=bob_agenda._agendas_depot_dir) == 1
    assert x_func_count_files(dir_path=bob_agenda._agendas_digest_dir) == 1

    # WHEN
    bob_agenda.del_depot_agenda(agenda_healer=lai_text)

    # THEN
    assert x_func_count_files(dir_path=bob_agenda._agendas_depot_dir) == 0
    assert x_func_count_files(dir_path=bob_agenda._agendas_digest_dir) == 0


def test_enactunit_set_depot_agenda_SavesFileCorrectly(
    enact_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_enactunit_dir()
    bob_agenda = enactunit_shop(bob_text, env_dir, get_temp_economy_id())
    cal1 = get_2node_agenda()
    assert (
        x_func_count_files(bob_agenda._agendas_depot_dir) is None
    )  # dir does not exist

    # WHEN
    bob_agenda.set_contract_if_empty()
    bob_agenda.set_depot_agenda(x_agenda=cal1, depotlink_type="blind_trust")

    # THEN
    print(f"Saving to {bob_agenda._agendas_depot_dir=}")
    # for path_x in os_scandir(ux._agendas_depot_dir):
    #     print(f"{path_x=}")
    assert x_func_count_files(bob_agenda._agendas_depot_dir) == 1


def test_enactunit_delete_ignore_depotlink_CorrectlyDeletesObj(
    enact_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_enactunit_dir()
    bob_agenda = enactunit_shop(bob_text, env_dir, get_temp_economy_id())
    yao_text = "Yao"
    create_agenda_file(bob_agenda._agendas_depot_dir, yao_text)
    assignment_text = "assignment"
    bob_agenda.set_contract_if_empty()
    bob_agenda._set_depotlink(yao_text, link_type=assignment_text)
    assert list(bob_agenda._contract._partys.keys()) == [bob_text, yao_text]
    assert bob_agenda._contract.get_party(yao_text).depotlink_type == assignment_text

    # WHEN
    bob_agenda.del_depot_agenda(agenda_healer=yao_text)

    # THEN
    assert list(bob_agenda._contract._partys.keys()) == [bob_text, yao_text]
    assert bob_agenda._contract.get_party(yao_text).depotlink_type is None


def test_enactunit_del_depot_agenda_CorrectlyDoesNotDeletesIgnoreFile(
    enact_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "bob"
    env_dir = get_temp_enactunit_dir()
    bob_agenda = enactunit_shop(bob_text, env_dir, get_temp_economy_id())
    zia_text = "Zia"
    create_agenda_file(bob_agenda._agendas_depot_dir, zia_text)
    bob_agenda.set_contract_if_empty()
    bob_agenda._set_depotlink(zia_text, link_type="ignore")
    assert x_func_count_files(dir_path=bob_agenda._agendas_depot_dir) == 1
    assert x_func_count_files(dir_path=bob_agenda._agendas_digest_dir) == 1
    assert x_func_count_files(dir_path=bob_agenda._agendas_ignore_dir) == 1

    # WHEN
    bob_agenda.del_depot_agenda(agenda_healer=zia_text)

    # THEN
    assert x_func_count_files(dir_path=bob_agenda._agendas_depot_dir) == 0
    assert x_func_count_files(dir_path=bob_agenda._agendas_digest_dir) == 0
    assert x_func_count_files(dir_path=bob_agenda._agendas_ignore_dir) == 1


def test_enactunit_set_ignore_agenda_file_CorrectlyUpdatesIgnoreFile(
    enact_dir_setup_cleanup,
):
    # GIVEN
    bob_text = "Bob"
    env_dir = get_temp_enactunit_dir()
    bob_ux = enactunit_shop(bob_text, env_dir, get_temp_economy_id())
    zia_text = "Zia"
    create_agenda_file(bob_ux._agendas_depot_dir, zia_text)
    bob_ux.set_contract_if_empty()
    bob_ux._set_depotlink(zia_text, link_type="ignore")
    assert x_func_count_files(dir_path=bob_ux._agendas_ignore_dir) == 1
    cx1 = bob_ux.open_ignore_agenda(healer=zia_text)
    assert len(cx1._partys) == 0
    cx1.add_partyunit(pid="tim")
    assert len(cx1._partys) == 1

    # WHEN
    zia_agenda = agendaunit_shop(_healer=zia_text)
    bob_ux.set_ignore_agenda_file(zia_agenda, src_agenda_healer=None)

    # THEN
    cx2 = bob_ux.open_ignore_agenda(healer=zia_text)
    assert len(cx2._partys) == 0
    assert x_func_count_files(dir_path=bob_ux._agendas_ignore_dir) == 1


def test_enactunit_refresh_depotlinks_CorrectlyPullsAllPublicAgendas(
    enact_dir_setup_cleanup,
):
    # GIVEN
    env_dir = get_temp_enactunit_dir()
    economy_id = get_temp_env_economy_id()
    sx = economyunit_shop(economy_id=economy_id, economys_dir=env_dir)
    yao_text = "Yao"
    sx.create_new_enactunit(enact_cid=yao_text)
    yao_agenda = sx.get_enactunit(cid=yao_text)
    assert len(yao_agenda.get_remelded_output_agenda().get_idea_list()) == 1

    ernie_text = "ernie"
    ernie_agenda = get_cal2nodes(_healer=ernie_text)
    steve_text = "steve"
    old_steve_agenda = get_cal2nodes(_healer=steve_text)
    sx.save_public_agenda(ernie_agenda)
    sx.save_public_agenda(old_steve_agenda)
    yao_agenda.set_depot_agenda(x_agenda=ernie_agenda, depotlink_type="blind_trust")
    yao_agenda.set_depot_agenda(x_agenda=old_steve_agenda, depotlink_type="blind_trust")

    assert len(yao_agenda.get_remelded_output_agenda().get_idea_list()) == 4
    new_steve_agenda = get_cal3nodes(_healer=steve_text)
    sx.save_public_agenda(new_steve_agenda)
    print(f"{env_dir=} {yao_agenda._agendas_public_dir=}")
    # for file_name in x_func_dir_files(dir_path=env_dir):
    #     print(f"{bob_agenda._agendas_public_dir=} {file_name=}")

    # for file_name in x_func_dir_files(dir_path=bob_agenda._agendas_public_dir):
    #     print(f"{bob_agenda._agendas_public_dir=} {file_name=}")

    # WHEN
    yao_agenda.refresh_depot_agendas()

    # THEN
    assert len(yao_agenda.get_remelded_output_agenda().get_idea_list()) == 5
