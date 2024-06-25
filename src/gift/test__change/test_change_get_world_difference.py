from src._world.belief import balancelink_shop
from src._world.other import otherlink_shop
from src._world.reason_idea import factunit_shop
from src._world.idea import ideaunit_shop
from src._world.belief import beliefunit_shop
from src._world.world import worldunit_shop
from src.gift.atom import atom_insert, atom_update, atom_delete
from src.gift.change import ChangeUnit, changeunit_shop
from src.listen.examples.example_listen_worlds import get_world_with_4_levels
from src._instrument.python import get_nested_value, get_empty_list_if_None
from copy import deepcopy as copy_deepcopy


def print_atomunit_keys(x_changeunit: ChangeUnit):
    for x_atomunit in get_delete_atomunit_list(x_changeunit):
        print(f"DELETE {x_atomunit.category} {list(x_atomunit.required_args.values())}")
    for x_atomunit in get_update_atomunit_list(x_changeunit):
        print(f"UPDATE {x_atomunit.category} {list(x_atomunit.required_args.values())}")
    for x_atomunit in get_insert_atomunit_list(x_changeunit):
        print(f"INSERT {x_atomunit.category} {list(x_atomunit.required_args.values())}")


def get_delete_atomunit_list(x_changeunit: ChangeUnit) -> list:
    return get_empty_list_if_None(
        x_changeunit._get_crud_atomunits_list().get(atom_delete())
    )


def get_insert_atomunit_list(x_changeunit: ChangeUnit):
    return get_empty_list_if_None(
        x_changeunit._get_crud_atomunits_list().get(atom_insert())
    )


def get_update_atomunit_list(x_changeunit: ChangeUnit):
    return get_empty_list_if_None(
        x_changeunit._get_crud_atomunits_list().get(atom_update())
    )


def get_atomunit_total_count(x_changeunit: ChangeUnit) -> int:
    return (
        len(get_delete_atomunit_list(x_changeunit))
        + len(get_insert_atomunit_list(x_changeunit))
        + len(get_update_atomunit_list(x_changeunit))
    )


def test_ChangeUnit_create_atomunits_CorrectHandlesEmptyWorlds():
    # GIVEN
    sue_world = get_world_with_4_levels()
    sue_changeunit = changeunit_shop()
    assert sue_changeunit.atomunits == {}

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(sue_world, sue_world)

    # THEN
    assert sue_changeunit.atomunits == {}


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_otherunit_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_world = worldunit_shop(sue_text)
    after_sue_world = copy_deepcopy(before_sue_world)
    rico_text = "Rico"
    rico_credor_weight = 33
    rico_debtor_weight = 44
    after_sue_world.add_otherunit(rico_text, rico_credor_weight, rico_debtor_weight)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_world, after_sue_world)

    # THEN
    assert len(sue_changeunit.atomunits.get(atom_insert()).get("world_otherunit")) == 1
    sue_insert_dict = sue_changeunit.atomunits.get(atom_insert())
    sue_otherunit_dict = sue_insert_dict.get("world_otherunit")
    rico_atomunit = sue_otherunit_dict.get(rico_text)
    assert rico_atomunit.get_value("other_id") == rico_text
    assert rico_atomunit.get_value("credor_weight") == rico_credor_weight
    assert rico_atomunit.get_value("debtor_weight") == rico_debtor_weight

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_otherunit_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_world = worldunit_shop(sue_text)
    before_sue_world.add_otherunit("Yao")
    before_sue_world.add_otherunit("Zia")

    after_sue_world = copy_deepcopy(before_sue_world)

    rico_text = "Rico"
    before_sue_world.add_otherunit(rico_text)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_world, after_sue_world)

    # THEN
    rico_atomunit = get_nested_value(
        sue_changeunit.atomunits, [atom_delete(), "world_otherunit", rico_text]
    )
    assert rico_atomunit.get_value("other_id") == rico_text

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    print_atomunit_keys(sue_changeunit)
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_otherunit_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_world = worldunit_shop(sue_text)
    after_sue_world = copy_deepcopy(before_sue_world)
    rico_text = "Rico"
    before_sue_world.add_otherunit(rico_text)
    rico_credor_weight = 33
    rico_debtor_weight = 44
    after_sue_world.add_otherunit(rico_text, rico_credor_weight, rico_debtor_weight)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_world, after_sue_world)

    # THEN
    x_keylist = [atom_update(), "world_otherunit", rico_text]
    rico_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert rico_atomunit.get_value("other_id") == rico_text
    assert rico_atomunit.get_value("credor_weight") == rico_credor_weight
    assert rico_atomunit.get_value("debtor_weight") == rico_debtor_weight

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_WorldUnit_simple_attrs_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_world = worldunit_shop(sue_text)
    after_sue_world = copy_deepcopy(before_sue_world)
    x_worldUnit_weight = 55
    x_pixel = 0.5
    x_max_tree_traverse = 66
    x_meld_strategy = "override"
    x_monetary_desc = "dragon funds"
    x_other_credor_pool = 77
    x_other_debtor_pool = 88
    after_sue_world._weight = x_worldUnit_weight
    after_sue_world._pixel = x_pixel
    after_sue_world.set_max_tree_traverse(x_max_tree_traverse)
    after_sue_world.set_meld_strategy(x_meld_strategy)
    after_sue_world.set_monetary_desc(x_monetary_desc)
    after_sue_world.set_other_credor_pool(x_other_credor_pool)
    after_sue_world.set_other_debtor_pool(x_other_debtor_pool)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_world, after_sue_world)

    # THEN
    x_keylist = [atom_update(), "worldunit"]
    rico_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert rico_atomunit.get_value("_max_tree_traverse") == x_max_tree_traverse
    assert rico_atomunit.get_value("_meld_strategy") == x_meld_strategy
    assert rico_atomunit.get_value("_monetary_desc") == x_monetary_desc
    assert rico_atomunit.get_value("_other_credor_pool") == x_other_credor_pool
    assert rico_atomunit.get_value("_other_debtor_pool") == x_other_debtor_pool
    assert rico_atomunit.get_value("_weight") == x_worldUnit_weight
    assert rico_atomunit.get_value("_pixel") == x_pixel

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_belief_otherlink_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    rico_text = "Rico"
    carm_text = "Carmen"
    after_sue_worldunit.add_otherunit(rico_text)
    after_sue_worldunit.add_otherunit(carm_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    rico_credor_weight = 77
    rico_debtor_weight = 88
    rico_otherlink = otherlink_shop(rico_text, rico_credor_weight, rico_debtor_weight)
    run_beliefunit.set_otherlink(rico_otherlink)
    run_beliefunit.set_otherlink(otherlink_shop(carm_text))
    after_sue_worldunit.set_beliefunit(run_beliefunit)
    # print(f"{after_sue_worldunit.get_beliefunit(run_text)=}")

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    x_keylist = [atom_insert(), "world_beliefunit", run_text]
    rico_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert rico_atomunit.get_value("belief_id") == run_text
    # print(f"\n{sue_changeunit.atomunits=}")
    print(f"\n{rico_atomunit=}")

    x_keylist = [atom_insert(), "world_belief_otherlink", run_text, rico_text]
    rico_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert rico_atomunit.get_value("belief_id") == run_text
    assert rico_atomunit.get_value("other_id") == rico_text
    assert rico_atomunit.get_value("credor_weight") == rico_credor_weight
    assert rico_atomunit.get_value("debtor_weight") == rico_debtor_weight

    print_atomunit_keys(sue_changeunit)
    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert len(get_delete_atomunit_list(sue_changeunit)) == 0
    assert len(get_insert_atomunit_list(sue_changeunit)) == 5
    assert len(get_delete_atomunit_list(sue_changeunit)) == 0
    assert get_atomunit_total_count(sue_changeunit) == 5


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_belief_otherlink_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_worldunit.add_otherunit(rico_text)
    before_sue_worldunit.add_otherunit(carm_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    before_rico_credor_weight = 77
    before_rico_debtor_weight = 88
    run_beliefunit.set_otherlink(
        otherlink_shop(rico_text, before_rico_credor_weight, before_rico_debtor_weight)
    )
    run_beliefunit.set_otherlink(otherlink_shop(carm_text))
    before_sue_worldunit.set_beliefunit(run_beliefunit)
    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    after_run_beliefunit = after_sue_worldunit.get_beliefunit(run_text)
    after_rico_credor_weight = 55
    after_rico_debtor_weight = 66
    after_run_beliefunit.edit_otherlink(
        rico_text, after_rico_credor_weight, after_rico_debtor_weight
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    # x_keylist = [atom_update(), "world_beliefunit", run_text]
    # rico_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    # assert rico_atomunit.get_value("belief_id") == run_text
    # print(f"\n{sue_changeunit.atomunits=}")
    # print(f"\n{rico_atomunit=}")

    x_keylist = [atom_update(), "world_belief_otherlink", run_text, rico_text]
    rico_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert rico_atomunit.get_value("belief_id") == run_text
    assert rico_atomunit.get_value("other_id") == rico_text
    assert rico_atomunit.get_value("credor_weight") == after_rico_credor_weight
    assert rico_atomunit.get_value("debtor_weight") == after_rico_debtor_weight

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_belief_otherlink_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_worldunit.add_otherunit(rico_text)
    before_sue_worldunit.add_otherunit(carm_text)
    before_sue_worldunit.add_otherunit(dizz_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_otherlink(otherlink_shop(rico_text))
    run_beliefunit.set_otherlink(otherlink_shop(carm_text))
    fly_text = ",flyers"
    fly_beliefunit = beliefunit_shop(fly_text)
    fly_beliefunit.set_otherlink(otherlink_shop(rico_text))
    fly_beliefunit.set_otherlink(otherlink_shop(carm_text))
    fly_beliefunit.set_otherlink(otherlink_shop(dizz_text))
    before_sue_worldunit.set_beliefunit(run_beliefunit)
    before_sue_worldunit.set_beliefunit(fly_beliefunit)
    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    after_sue_worldunit.del_beliefunit(run_text)
    after_fly_beliefunit = after_sue_worldunit.get_beliefunit(fly_text)
    after_fly_beliefunit.del_otherlink(dizz_text)
    assert len(before_sue_worldunit.get_beliefunit(fly_text)._others) == 3
    assert len(before_sue_worldunit.get_beliefunit(run_text)._others) == 2
    assert len(after_sue_worldunit.get_beliefunit(fly_text)._others) == 2
    assert after_sue_worldunit.get_beliefunit(run_text) is None

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    x_keylist = [atom_delete(), "world_beliefunit", run_text]
    rico_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert rico_atomunit.get_value("belief_id") == run_text

    x_keylist = [atom_delete(), "world_belief_otherlink", fly_text, dizz_text]
    rico_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert rico_atomunit.get_value("belief_id") == fly_text
    assert rico_atomunit.get_value("other_id") == dizz_text

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    print_atomunit_keys(sue_changeunit)
    assert len(get_delete_atomunit_list(sue_changeunit)) == 4
    assert len(get_insert_atomunit_list(sue_changeunit)) == 0
    assert len(get_update_atomunit_list(sue_changeunit)) == 0
    assert get_atomunit_total_count(sue_changeunit) == 4


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    street_text = "street ball"
    street_road = before_sue_worldunit.make_road(ball_road, street_text)
    before_sue_worldunit.add_idea(ideaunit_shop(street_text), ball_road)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_worldunit.make_road(sports_road, disc_text)
    music_text = "music"
    before_sue_worldunit.add_l1_idea(ideaunit_shop(music_text))
    before_sue_worldunit.add_idea(ideaunit_shop(disc_text), sports_road)
    # create after without ball_idea and street_idea
    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    after_sue_worldunit.del_idea_obj(ball_road)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    x_category = "world_ideaunit"
    print(f"{sue_changeunit.atomunits.get(atom_delete()).get(x_category).keys()=}")

    x_keylist = [atom_delete(), "world_ideaunit", ball_road, street_text]
    street_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert street_atomunit.get_value("parent_road") == ball_road
    assert street_atomunit.get_value("label") == street_text

    x_keylist = [atom_delete(), "world_ideaunit", sports_road, ball_text]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("parent_road") == sports_road
    assert ball_atomunit.get_value("label") == ball_text

    print(f"{get_atomunit_total_count(sue_changeunit)=}")
    assert get_atomunit_total_count(sue_changeunit) == 2


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    street_text = "street ball"
    street_road = before_sue_worldunit.make_road(ball_road, street_text)
    before_sue_worldunit.add_idea(ideaunit_shop(street_text), ball_road)

    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    disc_text = "Ultimate Disc"
    disc_road = after_sue_worldunit.make_road(sports_road, disc_text)
    after_sue_worldunit.add_idea(ideaunit_shop(disc_text), sports_road)
    music_text = "music"
    music_begin = 34
    music_close = 78
    music_meld_strategy = "override"
    music_weight = 55
    music_pledge = True
    music_road = after_sue_worldunit.make_l1_road(music_text)
    after_sue_worldunit.add_l1_idea(
        ideaunit_shop(
            music_text,
            _begin=music_begin,
            _close=music_close,
            _meld_strategy=music_meld_strategy,
            _weight=music_weight,
            pledge=music_pledge,
        )
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    print_atomunit_keys(sue_changeunit)

    x_keylist = [atom_insert(), "world_ideaunit", sports_road, disc_text]
    street_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert street_atomunit.get_value("parent_road") == sports_road
    assert street_atomunit.get_value("label") == disc_text

    x_keylist = [
        atom_insert(),
        "world_ideaunit",
        after_sue_worldunit._real_id,
        music_text,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("label") == music_text
    assert ball_atomunit.get_value("parent_road") == after_sue_worldunit._real_id
    assert ball_atomunit.get_value("_begin") == music_begin
    assert ball_atomunit.get_value("_close") == music_close
    assert ball_atomunit.get_value("_meld_strategy") == music_meld_strategy
    assert ball_atomunit.get_value("_weight") == music_weight
    assert ball_atomunit.get_value("pledge") == music_pledge

    assert get_atomunit_total_count(sue_changeunit) == 2


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    music_text = "music"
    before_music_begin = 34
    before_music_close = 78
    before_music_meld_strategy = "override"
    before_music_weight = 55
    before_music_pledge = True
    music_road = before_sue_worldunit.make_l1_road(music_text)
    before_sue_worldunit.add_l1_idea(
        ideaunit_shop(
            music_text,
            _begin=before_music_begin,
            _close=before_music_close,
            _meld_strategy=before_music_meld_strategy,
            _weight=before_music_weight,
            pledge=before_music_pledge,
        )
    )

    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    after_music_begin = 99
    after_music_close = 111
    after_music_meld_strategy = "default"
    after_music_weight = 22
    after_music_pledge = False
    after_sue_worldunit.edit_idea_attr(
        music_road,
        begin=after_music_begin,
        close=after_music_close,
        meld_strategy=after_music_meld_strategy,
        weight=after_music_weight,
        pledge=after_music_pledge,
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    print_atomunit_keys(sue_changeunit)

    x_keylist = [
        atom_update(),
        "world_ideaunit",
        after_sue_worldunit._real_id,
        music_text,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("parent_road") == after_sue_worldunit._real_id
    assert ball_atomunit.get_value("label") == music_text
    assert ball_atomunit.get_value("_begin") == after_music_begin
    assert ball_atomunit.get_value("_close") == after_music_close
    assert ball_atomunit.get_value("_meld_strategy") == after_music_meld_strategy
    assert ball_atomunit.get_value("_weight") == after_music_weight
    assert ball_atomunit.get_value("pledge") == after_music_pledge

    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_balancelink_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_au.add_otherunit(rico_text)
    before_sue_au.add_otherunit(carm_text)
    before_sue_au.add_otherunit(dizz_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_otherlink(otherlink_shop(rico_text))
    run_beliefunit.set_otherlink(otherlink_shop(carm_text))
    fly_text = ",flyers"
    fly_beliefunit = beliefunit_shop(fly_text)
    fly_beliefunit.set_otherlink(otherlink_shop(rico_text))
    fly_beliefunit.set_otherlink(otherlink_shop(carm_text))
    fly_beliefunit.set_otherlink(otherlink_shop(dizz_text))
    before_sue_au.set_beliefunit(run_beliefunit)
    before_sue_au.set_beliefunit(fly_beliefunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_au.make_road(sports_road, disc_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_au.add_idea(ideaunit_shop(disc_text), sports_road)
    before_sue_au.edit_idea_attr(ball_road, balancelink=balancelink_shop(run_text))
    before_sue_au.edit_idea_attr(ball_road, balancelink=balancelink_shop(fly_text))
    before_sue_au.edit_idea_attr(disc_road, balancelink=balancelink_shop(run_text))
    before_sue_au.edit_idea_attr(disc_road, balancelink=balancelink_shop(fly_text))

    after_sue_worldunit = copy_deepcopy(before_sue_au)
    after_sue_worldunit.edit_idea_attr(disc_road, balancelink_del=run_text)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_au, after_sue_worldunit)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")

    x_keylist = [atom_delete(), "world_idea_balancelink", disc_road, run_text]
    run_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert run_atomunit.get_value("road") == disc_road
    assert run_atomunit.get_value("belief_id") == run_text

    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_balancelink_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_au.add_otherunit(rico_text)
    before_sue_au.add_otherunit(carm_text)
    before_sue_au.add_otherunit(dizz_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_otherlink(otherlink_shop(rico_text))
    run_beliefunit.set_otherlink(otherlink_shop(carm_text))
    fly_text = ",flyers"
    fly_beliefunit = beliefunit_shop(fly_text)
    fly_beliefunit.set_otherlink(otherlink_shop(rico_text))
    fly_beliefunit.set_otherlink(otherlink_shop(carm_text))
    fly_beliefunit.set_otherlink(otherlink_shop(dizz_text))
    before_sue_au.set_beliefunit(run_beliefunit)
    before_sue_au.set_beliefunit(fly_beliefunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_au.make_road(sports_road, disc_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_au.add_idea(ideaunit_shop(disc_text), sports_road)
    before_sue_au.edit_idea_attr(ball_road, balancelink=balancelink_shop(run_text))
    before_sue_au.edit_idea_attr(disc_road, balancelink=balancelink_shop(fly_text))
    after_sue_au = copy_deepcopy(before_sue_au)
    after_sue_au.edit_idea_attr(ball_road, balancelink=balancelink_shop(fly_text))
    after_run_credor_weight = 44
    after_run_debtor_weight = 66
    after_sue_au.edit_idea_attr(
        disc_road,
        balancelink=balancelink_shop(
            run_text,
            credor_weight=after_run_credor_weight,
            debtor_weight=after_run_debtor_weight,
        ),
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_au, after_sue_au)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")

    x_keylist = [atom_insert(), "world_idea_balancelink", disc_road, run_text]
    run_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert run_atomunit.get_value("road") == disc_road
    assert run_atomunit.get_value("belief_id") == run_text
    assert run_atomunit.get_value("road") == disc_road
    assert run_atomunit.get_value("belief_id") == run_text
    assert run_atomunit.get_value("credor_weight") == after_run_credor_weight
    assert run_atomunit.get_value("debtor_weight") == after_run_debtor_weight

    assert get_atomunit_total_count(sue_changeunit) == 2


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_balancelink_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = worldunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_au.add_otherunit(rico_text)
    before_sue_au.add_otherunit(carm_text)
    run_text = ",runners"
    run_beliefunit = beliefunit_shop(run_text)
    run_beliefunit.set_otherlink(otherlink_shop(rico_text))
    before_sue_au.set_beliefunit(run_beliefunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_au.edit_idea_attr(ball_road, balancelink=balancelink_shop(run_text))
    run_balancelink = before_sue_au.get_idea_obj(ball_road)._balancelinks.get(run_text)

    after_sue_worldunit = copy_deepcopy(before_sue_au)
    after_credor_weight = 55
    after_debtor_weight = 66
    after_sue_worldunit.edit_idea_attr(
        ball_road,
        balancelink=balancelink_shop(
            belief_id=run_text,
            credor_weight=after_credor_weight,
            debtor_weight=after_debtor_weight,
        ),
    )
    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(before_sue_au, after_sue_worldunit)

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")

    x_keylist = [atom_update(), "world_idea_balancelink", ball_road, run_text]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("belief_id") == run_text
    assert ball_atomunit.get_value("credor_weight") == after_credor_weight
    assert ball_atomunit.get_value("debtor_weight") == after_debtor_weight
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_factunit_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_worldunit.make_l1_road(knee_text)
    bend_text = "bendable"
    bend_road = before_sue_worldunit.make_road(knee_road, bend_text)
    before_sue_worldunit.add_idea(ideaunit_shop(bend_text), knee_road)
    broken_text = "broke cartilage"
    broken_road = before_sue_worldunit.make_road(knee_road, broken_text)
    before_sue_worldunit.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_worldunit.add_idea(ideaunit_shop(broken_text), knee_road)
    before_broken_open = 11
    before_broken_nigh = 22
    before_sue_worldunit.edit_idea_attr(
        ball_road,
        factunit=factunit_shop(
            knee_road, bend_road, before_broken_open, before_broken_nigh
        ),
    )

    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    after_broken_open = 55
    after_broken_nigh = 66
    after_sue_worldunit.edit_idea_attr(
        ball_road,
        factunit=factunit_shop(
            knee_road, broken_road, after_broken_open, after_broken_nigh
        ),
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")

    x_keylist = [atom_update(), "world_idea_factunit", ball_road, knee_road]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("pick") == broken_road
    assert ball_atomunit.get_value("open") == after_broken_open
    assert ball_atomunit.get_value("nigh") == after_broken_nigh
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_factunit_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_worldunit.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_worldunit.make_road(knee_road, broken_text)
    before_sue_worldunit.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_worldunit.add_idea(ideaunit_shop(broken_text), knee_road)

    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    after_broken_open = 55
    after_broken_nigh = 66
    after_sue_worldunit.edit_idea_attr(
        road=ball_road,
        factunit=factunit_shop(
            base=knee_road,
            pick=broken_road,
            open=after_broken_open,
            nigh=after_broken_nigh,
        ),
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [atom_insert(), "world_idea_factunit", ball_road, knee_road]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("pick") == broken_road
    assert ball_atomunit.get_value("open") == after_broken_open
    assert ball_atomunit.get_value("nigh") == after_broken_nigh
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_factunit_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_worldunit.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_worldunit.make_road(knee_road, broken_text)
    before_sue_worldunit.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_worldunit.add_idea(ideaunit_shop(broken_text), knee_road)

    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    before_broken_open = 55
    before_broken_nigh = 66
    before_sue_worldunit.edit_idea_attr(
        road=ball_road,
        factunit=factunit_shop(
            base=knee_road,
            pick=broken_road,
            open=before_broken_open,
            nigh=before_broken_nigh,
        ),
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [atom_delete(), "world_idea_factunit", ball_road, knee_road]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reason_premiseunit_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_worldunit.make_l1_road(knee_text)
    before_sue_worldunit.add_l1_idea(ideaunit_shop(knee_text))
    broken_text = "broke cartilage"
    broken_road = before_sue_worldunit.make_road(knee_road, broken_text)
    before_sue_worldunit.add_idea(ideaunit_shop(broken_text), knee_road)
    bend_text = "bend"
    bend_road = before_sue_worldunit.make_road(knee_road, bend_text)
    before_sue_worldunit.add_idea(ideaunit_shop(bend_text), knee_road)
    before_sue_worldunit.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=bend_road
    )

    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    broken_open = 45
    broken_nigh = 77
    broken_divisor = 3
    after_sue_worldunit.edit_idea_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=broken_open,
        reason_premise_nigh=broken_nigh,
        reason_premise_divisor=broken_divisor,
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_insert(),
        "world_idea_reason_premiseunit",
        ball_road,
        knee_road,
        broken_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("need") == broken_road
    assert ball_atomunit.get_value("open") == broken_open
    assert ball_atomunit.get_value("nigh") == broken_nigh
    assert ball_atomunit.get_value("divisor") == broken_divisor
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reason_premiseunit_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_worldunit.make_l1_road(knee_text)
    before_sue_worldunit.add_l1_idea(ideaunit_shop(knee_text))
    broken_text = "broke cartilage"
    broken_road = before_sue_worldunit.make_road(knee_road, broken_text)
    before_sue_worldunit.add_idea(ideaunit_shop(broken_text), knee_road)
    bend_text = "bend"
    bend_road = before_sue_worldunit.make_road(knee_road, bend_text)
    before_sue_worldunit.add_idea(ideaunit_shop(bend_text), knee_road)
    before_sue_worldunit.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=bend_road
    )
    broken_open = 45
    broken_nigh = 77
    broken_divisor = 3
    before_sue_worldunit.edit_idea_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=broken_open,
        reason_premise_nigh=broken_nigh,
        reason_premise_divisor=broken_divisor,
    )
    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    after_sue_worldunit.edit_idea_attr(
        ball_road,
        reason_del_premise_base=knee_road,
        reason_del_premise_need=broken_road,
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_delete(),
        "world_idea_reason_premiseunit",
        ball_road,
        knee_road,
        broken_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("need") == broken_road
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reason_premiseunit_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_worldunit.make_l1_road(knee_text)
    before_sue_worldunit.add_l1_idea(ideaunit_shop(knee_text))
    broken_text = "broke cartilage"
    broken_road = before_sue_worldunit.make_road(knee_road, broken_text)
    before_sue_worldunit.add_idea(ideaunit_shop(broken_text), knee_road)
    bend_text = "bend"
    bend_road = before_sue_worldunit.make_road(knee_road, bend_text)
    before_sue_worldunit.add_idea(ideaunit_shop(bend_text), knee_road)
    before_sue_worldunit.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=bend_road
    )
    before_broken_open = 111
    before_broken_nigh = 777
    before_broken_divisor = 13
    before_sue_worldunit.edit_idea_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=before_broken_open,
        reason_premise_nigh=before_broken_nigh,
        reason_premise_divisor=before_broken_divisor,
    )

    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    after_broken_open = 333
    after_broken_nigh = 555
    after_broken_divisor = 78
    after_sue_worldunit.edit_idea_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=after_broken_open,
        reason_premise_nigh=after_broken_nigh,
        reason_premise_divisor=after_broken_divisor,
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_update(),
        "world_idea_reason_premiseunit",
        ball_road,
        knee_road,
        broken_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == knee_road
    assert ball_atomunit.get_value("need") == broken_road
    assert ball_atomunit.get_value("open") == after_broken_open
    assert ball_atomunit.get_value("nigh") == after_broken_nigh
    assert ball_atomunit.get_value("divisor") == after_broken_divisor
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reasonunit_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_worldunit.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_worldunit.make_road(knee_road, medical_text)
    before_sue_worldunit.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_worldunit.add_idea(ideaunit_shop(medical_text), knee_road)

    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    after_medical_suff_idea_active = False
    after_sue_worldunit.edit_idea_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_suff_idea_active=after_medical_suff_idea_active,
    )

    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_insert(),
        "world_idea_reasonunit",
        ball_road,
        medical_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == medical_road
    assert ball_atomunit.get_value("suff_idea_active") == after_medical_suff_idea_active
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reasonunit_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_worldunit.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_worldunit.make_road(knee_road, medical_text)
    before_sue_worldunit.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_worldunit.add_idea(ideaunit_shop(medical_text), knee_road)
    before_medical_suff_idea_active = True
    before_sue_worldunit.edit_idea_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_suff_idea_active=before_medical_suff_idea_active,
    )

    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    after_medical_suff_idea_active = False
    after_sue_worldunit.edit_idea_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_suff_idea_active=after_medical_suff_idea_active,
    )

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_update(),
        "world_idea_reasonunit",
        ball_road,
        medical_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == medical_road
    assert ball_atomunit.get_value("suff_idea_active") == after_medical_suff_idea_active
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_reasonunit_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_worldunit.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_worldunit.make_road(knee_road, medical_text)
    before_sue_worldunit.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_worldunit.add_idea(ideaunit_shop(medical_text), knee_road)
    before_medical_suff_idea_active = True
    before_sue_worldunit.edit_idea_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_suff_idea_active=before_medical_suff_idea_active,
    )

    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    after_ball_idea = after_sue_worldunit.get_idea_obj(ball_road)
    after_ball_idea.del_reasonunit_base(medical_road)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_delete(),
        "world_idea_reasonunit",
        ball_road,
        medical_road,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("base") == medical_road
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_suffbelief_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_worldunit.add_otherunit(rico_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)

    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    after_ball_ideaunit = after_sue_worldunit.get_idea_obj(ball_road)
    after_ball_ideaunit._assignedunit.set_suffbelief(rico_text)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_insert(),
        "world_idea_suffbelief",
        ball_road,
        rico_text,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("belief_id") == rico_text
    assert get_atomunit_total_count(sue_changeunit) == 1


def test_ChangeUnit_add_all_different_atomunits_Creates_AtomUnit_idea_suffbelief_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_worldunit = worldunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_worldunit.add_otherunit(rico_text)
    sports_text = "sports"
    sports_road = before_sue_worldunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_worldunit.make_road(sports_road, ball_text)
    before_sue_worldunit.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_ideaunit = before_sue_worldunit.get_idea_obj(ball_road)
    before_ball_ideaunit._assignedunit.set_suffbelief(rico_text)

    after_sue_worldunit = copy_deepcopy(before_sue_worldunit)
    after_ball_ideaunit = after_sue_worldunit.get_idea_obj(ball_road)
    after_ball_ideaunit._assignedunit.del_suffbelief(rico_text)

    # WHEN
    sue_changeunit = changeunit_shop()
    sue_changeunit.add_all_different_atomunits(
        before_sue_worldunit, after_sue_worldunit
    )

    # THEN
    print(f"{print_atomunit_keys(sue_changeunit)=}")
    x_keylist = [
        atom_delete(),
        "world_idea_suffbelief",
        ball_road,
        rico_text,
    ]
    ball_atomunit = get_nested_value(sue_changeunit.atomunits, x_keylist)
    assert ball_atomunit.get_value("road") == ball_road
    assert ball_atomunit.get_value("belief_id") == rico_text
    assert get_atomunit_total_count(sue_changeunit) == 1
