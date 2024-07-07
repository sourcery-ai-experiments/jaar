from src._road.jaar_refer import sue_str, bob_str, yao_str
from src._world.world import worldunit_shop
from src.gift.convert import (
    jaar_format_0001_char_v0_0_0,
    get_convert_format_dict,
    create_convert_format,
)

# test that given WorldUnit "jaar_format_0001_char_v0_0_0" format can be created
# format


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
