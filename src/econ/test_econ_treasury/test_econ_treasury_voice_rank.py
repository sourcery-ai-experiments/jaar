from src.agenda.agenda import (
    agendaunit_shop,
    get_file_names_in_voice_rank_order,
    partyunit_shop,
)
from src.instrument.file import (
    save_file,
    delete_dir,
)
from src.econ.econ import econunit_shop, save_file_to_roles
from src.econ.examples.econ_env_kit import (
    get_temp_env_world_id,
    get_test_econ_dir,
    env_dir_setup_cleanup,
)


def test_get_file_names_in_voice_rank_order_GetsCorrectFileOrder(env_dir_setup_cleanup):
    # GIVEN
    temp_dir = f"{get_test_econ_dir()}/voice_rank_order_temp"
    print(f"{temp_dir=}")
    yao_text = "Yao"

    ava_text = "Ava"
    bob_text = "Bob"
    cal_text = "Cal"
    dom_text = "Dom"
    elu_text = "Elu"
    ava_filename = f"{ava_text}.json"
    bob_filename = f"{bob_text}.json"
    cal_filename = f"{cal_text}.json"
    dom_filename = f"{dom_text}.json"
    elu_filename = f"{elu_text}.json"
    empty_str = ""
    save_file(temp_dir, ava_filename, empty_str)
    save_file(temp_dir, bob_filename, empty_str)
    save_file(temp_dir, cal_filename, empty_str)
    save_file(temp_dir, dom_filename, empty_str)
    save_file(temp_dir, elu_filename, empty_str)
    ava_partyunit = partyunit_shop(party_id=ava_text)
    bob_partyunit = partyunit_shop(party_id=bob_text)
    cal_partyunit = partyunit_shop(party_id=cal_text)
    dom_partyunit = partyunit_shop(party_id=dom_text)
    elu_partyunit = partyunit_shop(party_id=elu_text)

    yao_agenda = agendaunit_shop(_owner_id=yao_text)
    ava_partyunit.set_treasurying_data(None, None, None, voice_rank=33)
    bob_partyunit.set_treasurying_data(None, None, None, voice_rank=33)
    cal_partyunit.set_treasurying_data(None, None, None, voice_rank=77)
    dom_partyunit.set_treasurying_data(None, None, None, voice_rank=55)
    elu_partyunit.set_treasurying_data(None, None, None, voice_rank=99)
    yao_agenda.set_partyunit(ava_partyunit)
    yao_agenda.set_partyunit(bob_partyunit)
    yao_agenda.set_partyunit(cal_partyunit)
    yao_agenda.set_partyunit(dom_partyunit)
    yao_agenda.set_partyunit(elu_partyunit)

    x1 = get_file_names_in_voice_rank_order(yao_agenda, meldees_dir=temp_dir)
    assert x1 != None
    # for file_name in x1:
    #     print(f"{file_name=}")
    assert x1 == [
        elu_filename,
        cal_filename,
        dom_filename,
        ava_filename,
        bob_filename,
    ]
    assert ava_filename == x1[3]
    assert bob_filename == x1[4]

    # WHEN
    ava_partyunit._set_treasury_voice_hx_lowest_rank(11)

    # THEN
    assert ava_partyunit._treasury_voice_rank == bob_partyunit._treasury_voice_rank
    assert ava_partyunit._treasury_voice_hx_lowest_rank == 11
    assert bob_partyunit._treasury_voice_hx_lowest_rank == 33
    x2 = get_file_names_in_voice_rank_order(yao_agenda, meldees_dir=temp_dir)
    assert ava_filename == x2[4]
    assert bob_filename == x2[3]

    delete_dir(temp_dir)


def test_EconUnit_treasury_set_manager_voice_ranks_CorrectlyUpdatesRecords_type_1234(
    env_dir_setup_cleanup,
):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())
    ava_text = "Ava"
    bob_text = "Bob"
    cal_text = "Cal"
    dom_text = "Dom"
    elu_text = "Elu"

    yao_text = "Yao"
    yao_role0_agenda = agendaunit_shop(_owner_id=yao_text)
    yao_role0_agenda.set_partyunit(partyunit_shop(ava_text))
    yao_role0_agenda.set_partyunit(partyunit_shop(bob_text))
    yao_role0_agenda.set_partyunit(partyunit_shop(cal_text))
    yao_role0_agenda.set_partyunit(partyunit_shop(dom_text))
    yao_role0_agenda.set_partyunit(partyunit_shop(elu_text))
    save_file_to_roles(x_econ.econ_dir, yao_role0_agenda)
    x_econ.create_clerkunit(yao_text)
    yao_role1_agenda = x_econ.get_file_in_roles(yao_text)
    assert yao_role1_agenda.get_party(ava_text)._treasury_voice_rank is None
    assert yao_role1_agenda.get_party(bob_text)._treasury_voice_rank is None
    assert yao_role1_agenda.get_party(cal_text)._treasury_voice_rank is None
    assert yao_role1_agenda.get_party(dom_text)._treasury_voice_rank is None
    assert yao_role1_agenda.get_party(elu_text)._treasury_voice_rank is None

    # WHEN
    descending_text = "descending"
    x_econ.set_role_voice_ranks(yao_text, sort_order=descending_text)

    # THEN
    yao_role2_agenda = x_econ.get_file_in_roles(yao_text)
    assert yao_role2_agenda.get_party(ava_text)._treasury_voice_rank != None
    assert yao_role2_agenda.get_party(bob_text)._treasury_voice_rank != None
    assert yao_role2_agenda.get_party(cal_text)._treasury_voice_rank != None
    assert yao_role2_agenda.get_party(dom_text)._treasury_voice_rank != None
    assert yao_role2_agenda.get_party(elu_text)._treasury_voice_rank != None
    assert yao_role2_agenda.get_party(ava_text)._treasury_voice_rank == 0
    assert yao_role2_agenda.get_party(bob_text)._treasury_voice_rank == 1
    assert yao_role2_agenda.get_party(cal_text)._treasury_voice_rank == 2
    assert yao_role2_agenda.get_party(dom_text)._treasury_voice_rank == 3
    assert yao_role2_agenda.get_party(elu_text)._treasury_voice_rank == 4
