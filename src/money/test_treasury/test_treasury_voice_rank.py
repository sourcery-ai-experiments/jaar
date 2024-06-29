from src._instrument.file import save_file, delete_dir
from src._road.jaar_config import get_descending_text
from src._world.char import charunit_shop
from src._world.world import worldunit_shop
from src.listen.meld_files import get_file_names_in_voice_rank_order
from src.listen.listen import create_job_file_from_duty_file
from src.money.money import moneyunit_shop
from src.money.examples.econ_env import env_dir_setup_cleanup, get_texas_hubunit


def test_get_file_names_in_voice_rank_order_GetsCorrectFileOrder(env_dir_setup_cleanup):
    # GIVEN
    temp_dir = f"{get_texas_hubunit().reals_dir}/voice_rank_order_temp"
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
    ava_charunit = charunit_shop(char_id=ava_text)
    bob_charunit = charunit_shop(char_id=bob_text)
    cal_charunit = charunit_shop(char_id=cal_text)
    dom_charunit = charunit_shop(char_id=dom_text)
    elu_charunit = charunit_shop(char_id=elu_text)

    yao_world = worldunit_shop(_owner_id=yao_text)
    ava_charunit.set_treasury_attr(None, None, None, voice_rank=33)
    bob_charunit.set_treasury_attr(None, None, None, voice_rank=33)
    cal_charunit.set_treasury_attr(None, None, None, voice_rank=77)
    dom_charunit.set_treasury_attr(None, None, None, voice_rank=55)
    elu_charunit.set_treasury_attr(None, None, None, voice_rank=99)
    yao_world.set_charunit(ava_charunit)
    yao_world.set_charunit(bob_charunit)
    yao_world.set_charunit(cal_charunit)
    yao_world.set_charunit(dom_charunit)
    yao_world.set_charunit(elu_charunit)

    x1 = get_file_names_in_voice_rank_order(yao_world, meldees_dir=temp_dir)
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
    ava_charunit._set_treasury_voice_hx_lowest_rank(11)

    # THEN
    assert ava_charunit._treasury_voice_rank == bob_charunit._treasury_voice_rank
    assert ava_charunit._treasury_voice_hx_lowest_rank == 11
    assert bob_charunit._treasury_voice_hx_lowest_rank == 33
    x2 = get_file_names_in_voice_rank_order(yao_world, meldees_dir=temp_dir)
    assert ava_filename == x2[4]
    assert bob_filename == x2[3]

    delete_dir(temp_dir)


def test_MoneyUnit_treasury_set_manager_voice_ranks_CorrectlyUpdatesRecords_type_1234(
    env_dir_setup_cleanup,
):
    # GIVEN
    texas_hubunit = get_texas_hubunit()
    x_money = moneyunit_shop(texas_hubunit)
    ava_text = "Ava"
    bob_text = "Bob"
    cal_text = "Cal"
    dom_text = "Dom"
    elu_text = "Elu"

    yao_text = "Yao"
    yao_duty0_world = worldunit_shop(_owner_id=yao_text)
    yao_duty0_world.set_charunit(charunit_shop(ava_text))
    yao_duty0_world.set_charunit(charunit_shop(bob_text))
    yao_duty0_world.set_charunit(charunit_shop(cal_text))
    yao_duty0_world.set_charunit(charunit_shop(dom_text))
    yao_duty0_world.set_charunit(charunit_shop(elu_text))
    texas_hubunit.save_duty_world(yao_duty0_world)
    create_job_file_from_duty_file(texas_hubunit, yao_text)
    yao_duty1_world = texas_hubunit.get_duty_world(yao_text)
    assert yao_duty1_world.get_char(ava_text)._treasury_voice_rank is None
    assert yao_duty1_world.get_char(bob_text)._treasury_voice_rank is None
    assert yao_duty1_world.get_char(cal_text)._treasury_voice_rank is None
    assert yao_duty1_world.get_char(dom_text)._treasury_voice_rank is None
    assert yao_duty1_world.get_char(elu_text)._treasury_voice_rank is None

    # WHEN
    x_money.set_duty_voice_ranks(yao_text, sort_order=get_descending_text())

    # THEN
    yao_duty2_world = texas_hubunit.get_duty_world(yao_text)
    assert yao_duty2_world.get_char(ava_text)._treasury_voice_rank != None
    assert yao_duty2_world.get_char(bob_text)._treasury_voice_rank != None
    assert yao_duty2_world.get_char(cal_text)._treasury_voice_rank != None
    assert yao_duty2_world.get_char(dom_text)._treasury_voice_rank != None
    assert yao_duty2_world.get_char(elu_text)._treasury_voice_rank != None
    assert yao_duty2_world.get_char(ava_text)._treasury_voice_rank == 0
    assert yao_duty2_world.get_char(bob_text)._treasury_voice_rank == 1
    assert yao_duty2_world.get_char(cal_text)._treasury_voice_rank == 2
    assert yao_duty2_world.get_char(dom_text)._treasury_voice_rank == 3
    assert yao_duty2_world.get_char(elu_text)._treasury_voice_rank == 4
