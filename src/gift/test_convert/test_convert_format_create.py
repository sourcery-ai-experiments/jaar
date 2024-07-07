from src._road.jaar_refer import sue_str, bob_str, yao_str
from src._world.beliefhold import beliefhold_shop
from src._world.world import worldunit_shop
from src.gift.convert import (
    jaar_format_0001_char_v0_0_0,
    jaar_format_0002_beliefhold_v0_0_0,
    get_convert_format_dict,
    create_convert_format,
)


def test_create_convert_format_Arg_jaar_format_0001_char_v0_0_0():
    # GIVEN
    sue_text = sue_str()
    bob_text = bob_str()
    yao_text = yao_str()
    music_pool = 100
    sue_credor_weight = 11
    bob_credor_weight = 13
    yao_credor_weight = music_pool - sue_credor_weight - bob_credor_weight
    sue_debtor_weight = 23
    bob_debtor_weight = 29
    yao_debtor_weight = music_pool - sue_debtor_weight - bob_debtor_weight
    music_real_id = "music56"
    music_worldunit = worldunit_shop(sue_text, music_real_id)
    music_worldunit.add_charunit(sue_text, sue_credor_weight, sue_debtor_weight)
    music_worldunit.add_charunit(bob_text, bob_credor_weight, bob_debtor_weight)
    music_worldunit.add_charunit(yao_text, yao_credor_weight, yao_debtor_weight)
    music_worldunit.set_char_pool(music_pool)

    # WHEN
    x_convert_format = jaar_format_0001_char_v0_0_0()
    music_array2d_format = create_convert_format(music_worldunit, x_convert_format)

    # THEN
    array_headers = music_array2d_format[0]
    convert_format_dict = get_convert_format_dict(x_convert_format)
    assert array_headers == list(convert_format_dict.keys())
    array_bob = music_array2d_format[1]
    assert array_bob[0] == music_real_id
    assert array_bob[1] == music_worldunit._owner_id
    assert array_bob[2] == music_pool
    assert array_bob[3] == bob_text
    assert array_bob[4] == bob_credor_weight
    assert array_bob[5] == bob_debtor_weight

    array_sue = music_array2d_format[2]
    assert array_sue[0] == music_real_id
    assert array_sue[1] == music_worldunit._owner_id
    assert array_sue[2] == music_pool
    assert array_sue[3] == sue_text
    assert array_sue[4] == sue_credor_weight
    assert array_sue[5] == sue_debtor_weight

    array_yao = music_array2d_format[3]
    assert array_yao[0] == music_real_id
    assert array_yao[1] == music_worldunit._owner_id
    assert array_yao[2] == music_pool
    assert array_yao[3] == yao_text
    assert array_yao[4] == yao_credor_weight
    assert array_yao[5] == yao_debtor_weight

    assert len(music_array2d_format) == 4


def test_create_convert_format_Arg_jaar_format_0002_beliefhold_v0_0_0():
    # GIVEN
    sue_text = sue_str()
    bob_text = bob_str()
    yao_text = yao_str()
    music_real_id = "music56"
    music_worldunit = worldunit_shop(sue_text, music_real_id)
    music_worldunit.add_charunit(sue_text)
    music_worldunit.add_charunit(bob_text)
    music_worldunit.add_charunit(yao_text)
    sue_charunit = music_worldunit.get_char(sue_text)
    bob_charunit = music_worldunit.get_char(bob_text)
    yao_charunit = music_worldunit.get_char(yao_text)
    iowa_text = ",Iowa"
    sue_iowa_credor_weight = 37
    bob_iowa_credor_weight = 43
    yao_iowa_credor_weight = 51
    sue_iowa_debtor_weight = 57
    bob_iowa_debtor_weight = 61
    yao_iowa_debtor_weight = 67
    ohio_text = ",Ohio"
    yao_ohio_credor_weight = 73
    yao_ohio_debtor_weight = 67
    sue_iowa_beliefhold = beliefhold_shop(iowa_text, sue_iowa_credor_weight)
    bob_iowa_beliefhold = beliefhold_shop(iowa_text, bob_iowa_credor_weight)
    yao_iowa_beliefhold = beliefhold_shop(iowa_text, yao_iowa_credor_weight)
    sue_iowa_beliefhold.debtor_weight = sue_iowa_debtor_weight
    bob_iowa_beliefhold.debtor_weight = bob_iowa_debtor_weight
    yao_iowa_beliefhold.debtor_weight = yao_iowa_debtor_weight
    sue_charunit.set_beliefhold(sue_iowa_beliefhold)
    bob_charunit.set_beliefhold(bob_iowa_beliefhold)
    yao_charunit.set_beliefhold(yao_iowa_beliefhold)

    yao_ohio_beliefhold = beliefhold_shop(ohio_text, yao_ohio_credor_weight)
    yao_ohio_beliefhold.debtor_weight = yao_ohio_debtor_weight
    yao_charunit.set_beliefhold(yao_ohio_beliefhold)

    # WHEN
    x_convert_format = jaar_format_0002_beliefhold_v0_0_0()
    music_array2d_format = create_convert_format(music_worldunit, x_convert_format)

    # THEN
    array_headers = music_array2d_format[0]
    convert_format_dict = get_convert_format_dict(x_convert_format)
    assert array_headers == list(convert_format_dict.keys())
    array_bob_iowa = music_array2d_format[1]
    assert array_bob_iowa[0] == music_real_id
    assert array_bob_iowa[1] == music_worldunit._owner_id
    assert array_bob_iowa[2] == bob_text
    assert array_bob_iowa[3] == iowa_text
    assert array_bob_iowa[4] == bob_iowa_credor_weight
    assert array_bob_iowa[5] == bob_iowa_debtor_weight

    array_sue_iowa = music_array2d_format[2]
    assert array_sue_iowa[0] == music_real_id
    assert array_sue_iowa[1] == music_worldunit._owner_id
    assert array_sue_iowa[2] == sue_text
    assert array_sue_iowa[3] == iowa_text
    assert array_sue_iowa[4] == sue_iowa_credor_weight
    assert array_sue_iowa[5] == sue_iowa_debtor_weight

    array_yao_iowa = music_array2d_format[3]
    assert array_yao_iowa[0] == music_real_id
    assert array_yao_iowa[1] == music_worldunit._owner_id
    assert array_yao_iowa[2] == yao_text
    assert array_yao_iowa[3] == iowa_text
    assert array_yao_iowa[4] == yao_iowa_credor_weight
    assert array_yao_iowa[5] == yao_iowa_debtor_weight

    array_yao_ohio = music_array2d_format[4]
    assert array_yao_ohio[0] == music_real_id
    assert array_yao_ohio[1] == music_worldunit._owner_id
    assert array_yao_ohio[2] == yao_text
    assert array_yao_ohio[3] == ohio_text
    assert array_yao_ohio[4] == yao_ohio_credor_weight
    assert array_yao_ohio[5] == yao_ohio_debtor_weight

    assert len(music_array2d_format) == 5
