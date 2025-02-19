from src.agenda.group import balancelink_shop
from src.agenda.party import partylink_shop
from src.agenda.reason_idea import beliefunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.group import groupunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.atom import atom_insert, atom_update, atom_delete
from src.agenda.book import BookUnit, bookunit_shop
from src.agenda.examples.example_agendas import get_agenda_with_4_levels
from src.instrument.python import get_nested_value, get_empty_list_if_None
from copy import deepcopy as copy_deepcopy


def print_agendaatom_keys(x_bookunit: BookUnit):
    for x_agendaatom in get_delete_agendaatom_list(x_bookunit):
        print(
            f"DELETE {x_agendaatom.category} {list(x_agendaatom.required_args.values())}"
        )
    for x_agendaatom in get_update_agendaatom_list(x_bookunit):
        print(
            f"UPDATE {x_agendaatom.category} {list(x_agendaatom.required_args.values())}"
        )
    for x_agendaatom in get_insert_agendaatom_list(x_bookunit):
        print(
            f"INSERT {x_agendaatom.category} {list(x_agendaatom.required_args.values())}"
        )


def get_delete_agendaatom_list(x_bookunit: BookUnit) -> list:
    return get_empty_list_if_None(
        x_bookunit._get_crud_agendaatoms_list().get(atom_delete())
    )


def get_insert_agendaatom_list(x_bookunit: BookUnit):
    return get_empty_list_if_None(
        x_bookunit._get_crud_agendaatoms_list().get(atom_insert())
    )


def get_update_agendaatom_list(x_bookunit: BookUnit):
    return get_empty_list_if_None(
        x_bookunit._get_crud_agendaatoms_list().get(atom_update())
    )


def get_agendaatom_total_count(x_bookunit: BookUnit) -> int:
    return (
        len(get_delete_agendaatom_list(x_bookunit))
        + len(get_insert_agendaatom_list(x_bookunit))
        + len(get_update_agendaatom_list(x_bookunit))
    )


def test_BookUnit_create_agendaatoms_CorrectHandlesEmptyAgendas():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_bookunit = bookunit_shop()
    assert sue_bookunit.agendaatoms == {}

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(sue_agenda, sue_agenda)

    # THEN
    assert sue_bookunit.agendaatoms == {}


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_partyunit_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agenda = agendaunit_shop(sue_text)
    after_sue_agenda = copy_deepcopy(before_sue_agenda)
    rico_text = "Rico"
    rico_creditor_weight = 33
    rico_debtor_weight = 44
    after_sue_agenda.add_partyunit(rico_text, rico_creditor_weight, rico_debtor_weight)

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(before_sue_agenda, after_sue_agenda)

    # THEN
    assert len(sue_bookunit.agendaatoms.get(atom_insert()).get("agenda_partyunit")) == 1
    sue_insert_dict = sue_bookunit.agendaatoms.get(atom_insert())
    sue_partyunit_dict = sue_insert_dict.get("agenda_partyunit")
    rico_agendaatom = sue_partyunit_dict.get(rico_text)
    assert rico_agendaatom.get_value("party_id") == rico_text
    assert rico_agendaatom.get_value("creditor_weight") == rico_creditor_weight
    assert rico_agendaatom.get_value("debtor_weight") == rico_debtor_weight

    print(f"{get_agendaatom_total_count(sue_bookunit)=}")
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_partyunit_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_agenda = agendaunit_shop(sue_text)
    before_sue_agenda.add_partyunit("Yao")
    before_sue_agenda.add_partyunit("Zia")

    after_sue_agenda = copy_deepcopy(before_sue_agenda)

    rico_text = "Rico"
    before_sue_agenda.add_partyunit(rico_text)

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(before_sue_agenda, after_sue_agenda)

    # THEN
    rico_agendaatom = get_nested_value(
        sue_bookunit.agendaatoms, [atom_delete(), "agenda_partyunit", rico_text]
    )
    assert rico_agendaatom.get_value("party_id") == rico_text

    print(f"{get_agendaatom_total_count(sue_bookunit)=}")
    print_agendaatom_keys(sue_bookunit)
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_partyunit_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_agenda = agendaunit_shop(sue_text)
    after_sue_agenda = copy_deepcopy(before_sue_agenda)
    rico_text = "Rico"
    before_sue_agenda.add_partyunit(rico_text)
    rico_creditor_weight = 33
    rico_debtor_weight = 44
    after_sue_agenda.add_partyunit(rico_text, rico_creditor_weight, rico_debtor_weight)

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(before_sue_agenda, after_sue_agenda)

    # THEN
    x_keylist = [atom_update(), "agenda_partyunit", rico_text]
    rico_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert rico_agendaatom.get_value("party_id") == rico_text
    assert rico_agendaatom.get_value("creditor_weight") == rico_creditor_weight
    assert rico_agendaatom.get_value("debtor_weight") == rico_debtor_weight

    print(f"{get_agendaatom_total_count(sue_bookunit)=}")
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_AgendaUnit_simple_attrs_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_agenda = agendaunit_shop(sue_text)
    after_sue_agenda = copy_deepcopy(before_sue_agenda)
    x_agendaUnit_weight = 55
    x_planck = 0.5
    x_max_tree_traverse = 66
    x_meld_strategy = "override"
    x_money_desc = "dragon funds"
    x_party_creditor_pool = 77
    x_party_debtor_pool = 88
    after_sue_agenda._weight = x_agendaUnit_weight
    after_sue_agenda._planck = x_planck
    after_sue_agenda.set_max_tree_traverse(x_max_tree_traverse)
    after_sue_agenda.set_meld_strategy(x_meld_strategy)
    after_sue_agenda.set_money_desc(x_money_desc)
    after_sue_agenda.set_party_creditor_pool(x_party_creditor_pool)
    after_sue_agenda.set_party_debtor_pool(x_party_debtor_pool)

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(before_sue_agenda, after_sue_agenda)

    # THEN
    x_keylist = [atom_update(), "agendaunit"]
    rico_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert rico_agendaatom.get_value("_max_tree_traverse") == x_max_tree_traverse
    assert rico_agendaatom.get_value("_meld_strategy") == x_meld_strategy
    assert rico_agendaatom.get_value("_money_desc") == x_money_desc
    assert rico_agendaatom.get_value("_party_creditor_pool") == x_party_creditor_pool
    assert rico_agendaatom.get_value("_party_debtor_pool") == x_party_debtor_pool
    assert rico_agendaatom.get_value("_weight") == x_agendaUnit_weight
    assert rico_agendaatom.get_value("_planck") == x_planck

    print(f"{get_agendaatom_total_count(sue_bookunit)=}")
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_group_partylink_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    rico_text = "Rico"
    carm_text = "Carmen"
    after_sue_agendaunit.add_partyunit(rico_text)
    after_sue_agendaunit.add_partyunit(carm_text)
    run_text = ",runners"
    x_treasury_partylinks = "Yao"
    run_groupunit = groupunit_shop(run_text, _treasury_partylinks=x_treasury_partylinks)
    rico_creditor_weight = 77
    rico_debtor_weight = 88
    rico_partylink = partylink_shop(rico_text, rico_creditor_weight, rico_debtor_weight)
    run_groupunit.set_partylink(rico_partylink)
    run_groupunit.set_partylink(partylink_shop(carm_text))
    after_sue_agendaunit.set_groupunit(run_groupunit)
    # print(f"{after_sue_agendaunit.get_groupunit(run_text)=}")

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    x_keylist = [atom_insert(), "agenda_groupunit", run_text]
    rico_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert rico_agendaatom.get_value("group_id") == run_text
    # print(f"\n{sue_bookunit.agendaatoms=}")
    print(f"\n{rico_agendaatom=}")
    assert rico_agendaatom.get_value("_treasury_partylinks") == x_treasury_partylinks

    x_keylist = [atom_insert(), "agenda_group_partylink", run_text, rico_text]
    rico_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert rico_agendaatom.get_value("group_id") == run_text
    assert rico_agendaatom.get_value("party_id") == rico_text
    assert rico_agendaatom.get_value("creditor_weight") == rico_creditor_weight
    assert rico_agendaatom.get_value("debtor_weight") == rico_debtor_weight

    print_agendaatom_keys(sue_bookunit)
    print(f"{get_agendaatom_total_count(sue_bookunit)=}")
    assert len(get_delete_agendaatom_list(sue_bookunit)) == 0
    assert len(get_insert_agendaatom_list(sue_bookunit)) == 5
    assert len(get_delete_agendaatom_list(sue_bookunit)) == 0
    assert get_agendaatom_total_count(sue_bookunit) == 5


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_group_partylink_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_agendaunit.add_partyunit(rico_text)
    before_sue_agendaunit.add_partyunit(carm_text)
    run_text = ",runners"
    x_treasury_partylinks = "Yao"
    run_groupunit = groupunit_shop(run_text, _treasury_partylinks=x_treasury_partylinks)
    before_rico_creditor_weight = 77
    before_rico_debtor_weight = 88
    run_groupunit.set_partylink(
        partylink_shop(
            rico_text, before_rico_creditor_weight, before_rico_debtor_weight
        )
    )
    run_groupunit.set_partylink(partylink_shop(carm_text))
    before_sue_agendaunit.set_groupunit(run_groupunit)
    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_run_groupunit = after_sue_agendaunit.get_groupunit(run_text)
    swim_text = "swimming"
    after_run_groupunit._treasury_partylinks = swim_text
    after_rico_creditor_weight = 55
    after_rico_debtor_weight = 66
    after_run_groupunit.edit_partylink(
        rico_text, after_rico_creditor_weight, after_rico_debtor_weight
    )

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    x_keylist = [atom_update(), "agenda_groupunit", run_text]
    rico_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert rico_agendaatom.get_value("group_id") == run_text
    # print(f"\n{sue_bookunit.agendaatoms=}")
    print(f"\n{rico_agendaatom=}")
    assert rico_agendaatom.get_value("_treasury_partylinks") == swim_text

    x_keylist = [atom_update(), "agenda_group_partylink", run_text, rico_text]
    rico_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert rico_agendaatom.get_value("group_id") == run_text
    assert rico_agendaatom.get_value("party_id") == rico_text
    assert rico_agendaatom.get_value("creditor_weight") == after_rico_creditor_weight
    assert rico_agendaatom.get_value("debtor_weight") == after_rico_debtor_weight

    print(f"{get_agendaatom_total_count(sue_bookunit)=}")
    assert get_agendaatom_total_count(sue_bookunit) == 2


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_group_partylink_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_agendaunit.add_partyunit(rico_text)
    before_sue_agendaunit.add_partyunit(carm_text)
    before_sue_agendaunit.add_partyunit(dizz_text)
    run_text = ",runners"
    run_groupunit = groupunit_shop(run_text)
    run_groupunit.set_partylink(partylink_shop(rico_text))
    run_groupunit.set_partylink(partylink_shop(carm_text))
    fly_text = ",flyers"
    fly_groupunit = groupunit_shop(fly_text)
    fly_groupunit.set_partylink(partylink_shop(rico_text))
    fly_groupunit.set_partylink(partylink_shop(carm_text))
    fly_groupunit.set_partylink(partylink_shop(dizz_text))
    before_sue_agendaunit.set_groupunit(run_groupunit)
    before_sue_agendaunit.set_groupunit(fly_groupunit)
    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_sue_agendaunit.del_groupunit(run_text)
    after_fly_groupunit = after_sue_agendaunit.get_groupunit(fly_text)
    after_fly_groupunit.del_partylink(dizz_text)
    assert len(before_sue_agendaunit.get_groupunit(fly_text)._partys) == 3
    assert len(before_sue_agendaunit.get_groupunit(run_text)._partys) == 2
    assert len(after_sue_agendaunit.get_groupunit(fly_text)._partys) == 2
    assert after_sue_agendaunit.get_groupunit(run_text) is None

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    x_keylist = [atom_delete(), "agenda_groupunit", run_text]
    rico_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert rico_agendaatom.get_value("group_id") == run_text

    x_keylist = [atom_delete(), "agenda_group_partylink", fly_text, dizz_text]
    rico_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert rico_agendaatom.get_value("group_id") == fly_text
    assert rico_agendaatom.get_value("party_id") == dizz_text

    print(f"{get_agendaatom_total_count(sue_bookunit)=}")
    print_agendaatom_keys(sue_bookunit)
    assert len(get_delete_agendaatom_list(sue_bookunit)) == 4
    assert len(get_insert_agendaatom_list(sue_bookunit)) == 0
    assert len(get_update_agendaatom_list(sue_bookunit)) == 0
    assert get_agendaatom_total_count(sue_bookunit) == 4


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    street_text = "street ball"
    street_road = before_sue_agendaunit.make_road(ball_road, street_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(street_text), ball_road)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_agendaunit.make_road(sports_road, disc_text)
    music_text = "music"
    before_sue_agendaunit.add_l1_idea(ideaunit_shop(music_text))
    before_sue_agendaunit.add_idea(ideaunit_shop(disc_text), sports_road)
    # create after without ball_idea and street_idea
    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_sue_agendaunit.del_idea_obj(ball_road)

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    x_category = "agenda_ideaunit"
    print(f"{sue_bookunit.agendaatoms.get(atom_delete()).get(x_category).keys()=}")

    x_keylist = [atom_delete(), "agenda_ideaunit", ball_road, street_text]
    street_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert street_agendaatom.get_value("parent_road") == ball_road
    assert street_agendaatom.get_value("label") == street_text

    x_keylist = [atom_delete(), "agenda_ideaunit", sports_road, ball_text]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("parent_road") == sports_road
    assert ball_agendaatom.get_value("label") == ball_text

    print(f"{get_agendaatom_total_count(sue_bookunit)=}")
    assert get_agendaatom_total_count(sue_bookunit) == 2


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    street_text = "street ball"
    street_road = before_sue_agendaunit.make_road(ball_road, street_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(street_text), ball_road)

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    disc_text = "Ultimate Disc"
    disc_road = after_sue_agendaunit.make_road(sports_road, disc_text)
    after_sue_agendaunit.add_idea(ideaunit_shop(disc_text), sports_road)
    music_text = "music"
    music_begin = 34
    music_close = 78
    music_meld_strategy = "override"
    music_weight = 55
    music_promise = True
    music_road = after_sue_agendaunit.make_l1_road(music_text)
    after_sue_agendaunit.add_l1_idea(
        ideaunit_shop(
            music_text,
            _begin=music_begin,
            _close=music_close,
            _meld_strategy=music_meld_strategy,
            _weight=music_weight,
            promise=music_promise,
        )
    )

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print_agendaatom_keys(sue_bookunit)

    x_keylist = [atom_insert(), "agenda_ideaunit", sports_road, disc_text]
    street_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert street_agendaatom.get_value("parent_road") == sports_road
    assert street_agendaatom.get_value("label") == disc_text

    x_keylist = [
        atom_insert(),
        "agenda_ideaunit",
        after_sue_agendaunit._world_id,
        music_text,
    ]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("label") == music_text
    assert ball_agendaatom.get_value("parent_road") == after_sue_agendaunit._world_id
    assert ball_agendaatom.get_value("_begin") == music_begin
    assert ball_agendaatom.get_value("_close") == music_close
    assert ball_agendaatom.get_value("_meld_strategy") == music_meld_strategy
    assert ball_agendaatom.get_value("_weight") == music_weight
    assert ball_agendaatom.get_value("promise") == music_promise

    assert get_agendaatom_total_count(sue_bookunit) == 2


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    music_text = "music"
    before_music_begin = 34
    before_music_close = 78
    before_music_meld_strategy = "override"
    before_music_weight = 55
    before_music_promise = True
    music_road = before_sue_agendaunit.make_l1_road(music_text)
    before_sue_agendaunit.add_l1_idea(
        ideaunit_shop(
            music_text,
            _begin=before_music_begin,
            _close=before_music_close,
            _meld_strategy=before_music_meld_strategy,
            _weight=before_music_weight,
            promise=before_music_promise,
        )
    )

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_music_begin = 99
    after_music_close = 111
    after_music_meld_strategy = "default"
    after_music_weight = 22
    after_music_promise = False
    after_sue_agendaunit.edit_idea_attr(
        music_road,
        begin=after_music_begin,
        close=after_music_close,
        meld_strategy=after_music_meld_strategy,
        weight=after_music_weight,
        promise=after_music_promise,
    )

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print_agendaatom_keys(sue_bookunit)

    x_keylist = [
        atom_update(),
        "agenda_ideaunit",
        after_sue_agendaunit._world_id,
        music_text,
    ]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("parent_road") == after_sue_agendaunit._world_id
    assert ball_agendaatom.get_value("label") == music_text
    assert ball_agendaatom.get_value("_begin") == after_music_begin
    assert ball_agendaatom.get_value("_close") == after_music_close
    assert ball_agendaatom.get_value("_meld_strategy") == after_music_meld_strategy
    assert ball_agendaatom.get_value("_weight") == after_music_weight
    assert ball_agendaatom.get_value("promise") == after_music_promise

    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_balancelink_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_au.add_partyunit(rico_text)
    before_sue_au.add_partyunit(carm_text)
    before_sue_au.add_partyunit(dizz_text)
    run_text = ",runners"
    run_groupunit = groupunit_shop(run_text)
    run_groupunit.set_partylink(partylink_shop(rico_text))
    run_groupunit.set_partylink(partylink_shop(carm_text))
    fly_text = ",flyers"
    fly_groupunit = groupunit_shop(fly_text)
    fly_groupunit.set_partylink(partylink_shop(rico_text))
    fly_groupunit.set_partylink(partylink_shop(carm_text))
    fly_groupunit.set_partylink(partylink_shop(dizz_text))
    before_sue_au.set_groupunit(run_groupunit)
    before_sue_au.set_groupunit(fly_groupunit)
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

    after_sue_agendaunit = copy_deepcopy(before_sue_au)
    after_sue_agendaunit.edit_idea_attr(disc_road, balancelink_del=run_text)

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(before_sue_au, after_sue_agendaunit)

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")

    x_keylist = [atom_delete(), "agenda_idea_balancelink", disc_road, run_text]
    run_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert run_agendaatom.get_value("road") == disc_road
    assert run_agendaatom.get_value("group_id") == run_text

    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_balancelink_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    dizz_text = "Dizzy"
    before_sue_au.add_partyunit(rico_text)
    before_sue_au.add_partyunit(carm_text)
    before_sue_au.add_partyunit(dizz_text)
    run_text = ",runners"
    run_groupunit = groupunit_shop(run_text)
    run_groupunit.set_partylink(partylink_shop(rico_text))
    run_groupunit.set_partylink(partylink_shop(carm_text))
    fly_text = ",flyers"
    fly_groupunit = groupunit_shop(fly_text)
    fly_groupunit.set_partylink(partylink_shop(rico_text))
    fly_groupunit.set_partylink(partylink_shop(carm_text))
    fly_groupunit.set_partylink(partylink_shop(dizz_text))
    before_sue_au.set_groupunit(run_groupunit)
    before_sue_au.set_groupunit(fly_groupunit)
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
    after_run_creditor_weight = 44
    after_run_debtor_weight = 66
    after_sue_au.edit_idea_attr(
        disc_road,
        balancelink=balancelink_shop(
            run_text,
            creditor_weight=after_run_creditor_weight,
            debtor_weight=after_run_debtor_weight,
        ),
    )

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(before_sue_au, after_sue_au)

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")

    x_keylist = [atom_insert(), "agenda_idea_balancelink", disc_road, run_text]
    run_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert run_agendaatom.get_value("road") == disc_road
    assert run_agendaatom.get_value("group_id") == run_text
    assert run_agendaatom.get_value("road") == disc_road
    assert run_agendaatom.get_value("group_id") == run_text
    assert run_agendaatom.get_value("creditor_weight") == after_run_creditor_weight
    assert run_agendaatom.get_value("debtor_weight") == after_run_debtor_weight

    assert get_agendaatom_total_count(sue_bookunit) == 2


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_balancelink_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_au.add_partyunit(rico_text)
    before_sue_au.add_partyunit(carm_text)
    run_text = ",runners"
    run_groupunit = groupunit_shop(run_text)
    run_groupunit.set_partylink(partylink_shop(rico_text))
    before_sue_au.set_groupunit(run_groupunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_idea(ideaunit_shop(ball_text), sports_road)
    before_sue_au.edit_idea_attr(ball_road, balancelink=balancelink_shop(run_text))
    run_balancelink = before_sue_au.get_idea_obj(ball_road)._balancelinks.get(run_text)

    after_sue_agendaunit = copy_deepcopy(before_sue_au)
    after_creditor_weight = 55
    after_debtor_weight = 66
    after_sue_agendaunit.edit_idea_attr(
        ball_road,
        balancelink=balancelink_shop(
            group_id=run_text,
            creditor_weight=after_creditor_weight,
            debtor_weight=after_debtor_weight,
        ),
    )
    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(before_sue_au, after_sue_agendaunit)

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")

    x_keylist = [atom_update(), "agenda_idea_balancelink", ball_road, run_text]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("road") == ball_road
    assert ball_agendaatom.get_value("group_id") == run_text
    assert ball_agendaatom.get_value("creditor_weight") == after_creditor_weight
    assert ball_agendaatom.get_value("debtor_weight") == after_debtor_weight
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_beliefunit_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    bend_text = "bendable"
    bend_road = before_sue_agendaunit.make_road(knee_road, bend_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(bend_text), knee_road)
    broken_text = "broke cartilage"
    broken_road = before_sue_agendaunit.make_road(knee_road, broken_text)
    before_sue_agendaunit.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_agendaunit.add_idea(ideaunit_shop(broken_text), knee_road)
    before_broken_open = 11
    before_broken_nigh = 22
    before_sue_agendaunit.edit_idea_attr(
        ball_road,
        beliefunit=beliefunit_shop(
            knee_road, bend_road, before_broken_open, before_broken_nigh
        ),
    )

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_broken_open = 55
    after_broken_nigh = 66
    after_sue_agendaunit.edit_idea_attr(
        ball_road,
        beliefunit=beliefunit_shop(
            knee_road, broken_road, after_broken_open, after_broken_nigh
        ),
    )

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")

    x_keylist = [atom_update(), "agenda_idea_beliefunit", ball_road, knee_road]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("road") == ball_road
    assert ball_agendaatom.get_value("base") == knee_road
    assert ball_agendaatom.get_value("pick") == broken_road
    assert ball_agendaatom.get_value("open") == after_broken_open
    assert ball_agendaatom.get_value("nigh") == after_broken_nigh
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_beliefunit_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_agendaunit.make_road(knee_road, broken_text)
    before_sue_agendaunit.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_agendaunit.add_idea(ideaunit_shop(broken_text), knee_road)

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_broken_open = 55
    after_broken_nigh = 66
    after_sue_agendaunit.edit_idea_attr(
        road=ball_road,
        beliefunit=beliefunit_shop(
            base=knee_road,
            pick=broken_road,
            open=after_broken_open,
            nigh=after_broken_nigh,
        ),
    )

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")
    x_keylist = [atom_insert(), "agenda_idea_beliefunit", ball_road, knee_road]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("road") == ball_road
    assert ball_agendaatom.get_value("base") == knee_road
    assert ball_agendaatom.get_value("pick") == broken_road
    assert ball_agendaatom.get_value("open") == after_broken_open
    assert ball_agendaatom.get_value("nigh") == after_broken_nigh
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_beliefunit_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_agendaunit.make_road(knee_road, broken_text)
    before_sue_agendaunit.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_agendaunit.add_idea(ideaunit_shop(broken_text), knee_road)

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    before_broken_open = 55
    before_broken_nigh = 66
    before_sue_agendaunit.edit_idea_attr(
        road=ball_road,
        beliefunit=beliefunit_shop(
            base=knee_road,
            pick=broken_road,
            open=before_broken_open,
            nigh=before_broken_nigh,
        ),
    )

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")
    x_keylist = [atom_delete(), "agenda_idea_beliefunit", ball_road, knee_road]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("road") == ball_road
    assert ball_agendaatom.get_value("base") == knee_road
    assert ball_agendaatom.get_value("road") == ball_road
    assert ball_agendaatom.get_value("base") == knee_road
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_reason_premiseunit_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    before_sue_agendaunit.add_l1_idea(ideaunit_shop(knee_text))
    broken_text = "broke cartilage"
    broken_road = before_sue_agendaunit.make_road(knee_road, broken_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(broken_text), knee_road)
    bend_text = "bend"
    bend_road = before_sue_agendaunit.make_road(knee_road, bend_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(bend_text), knee_road)
    before_sue_agendaunit.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=bend_road
    )

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    broken_open = 45
    broken_nigh = 77
    broken_divisor = 3
    after_sue_agendaunit.edit_idea_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=broken_open,
        reason_premise_nigh=broken_nigh,
        reason_premise_divisor=broken_divisor,
    )

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")
    x_keylist = [
        atom_insert(),
        "agenda_idea_reason_premiseunit",
        ball_road,
        knee_road,
        broken_road,
    ]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("road") == ball_road
    assert ball_agendaatom.get_value("base") == knee_road
    assert ball_agendaatom.get_value("need") == broken_road
    assert ball_agendaatom.get_value("open") == broken_open
    assert ball_agendaatom.get_value("nigh") == broken_nigh
    assert ball_agendaatom.get_value("divisor") == broken_divisor
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_reason_premiseunit_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    before_sue_agendaunit.add_l1_idea(ideaunit_shop(knee_text))
    broken_text = "broke cartilage"
    broken_road = before_sue_agendaunit.make_road(knee_road, broken_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(broken_text), knee_road)
    bend_text = "bend"
    bend_road = before_sue_agendaunit.make_road(knee_road, bend_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(bend_text), knee_road)
    before_sue_agendaunit.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=bend_road
    )
    broken_open = 45
    broken_nigh = 77
    broken_divisor = 3
    before_sue_agendaunit.edit_idea_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=broken_open,
        reason_premise_nigh=broken_nigh,
        reason_premise_divisor=broken_divisor,
    )
    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_sue_agendaunit.edit_idea_attr(
        ball_road,
        reason_del_premise_base=knee_road,
        reason_del_premise_need=broken_road,
    )

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")
    x_keylist = [
        atom_delete(),
        "agenda_idea_reason_premiseunit",
        ball_road,
        knee_road,
        broken_road,
    ]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("road") == ball_road
    assert ball_agendaatom.get_value("base") == knee_road
    assert ball_agendaatom.get_value("need") == broken_road
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_reason_premiseunit_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    before_sue_agendaunit.add_l1_idea(ideaunit_shop(knee_text))
    broken_text = "broke cartilage"
    broken_road = before_sue_agendaunit.make_road(knee_road, broken_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(broken_text), knee_road)
    bend_text = "bend"
    bend_road = before_sue_agendaunit.make_road(knee_road, bend_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(bend_text), knee_road)
    before_sue_agendaunit.edit_idea_attr(
        ball_road, reason_base=knee_road, reason_premise=bend_road
    )
    before_broken_open = 111
    before_broken_nigh = 777
    before_broken_divisor = 13
    before_sue_agendaunit.edit_idea_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=before_broken_open,
        reason_premise_nigh=before_broken_nigh,
        reason_premise_divisor=before_broken_divisor,
    )

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_broken_open = 333
    after_broken_nigh = 555
    after_broken_divisor = 78
    after_sue_agendaunit.edit_idea_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=after_broken_open,
        reason_premise_nigh=after_broken_nigh,
        reason_premise_divisor=after_broken_divisor,
    )

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")
    x_keylist = [
        atom_update(),
        "agenda_idea_reason_premiseunit",
        ball_road,
        knee_road,
        broken_road,
    ]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("road") == ball_road
    assert ball_agendaatom.get_value("base") == knee_road
    assert ball_agendaatom.get_value("need") == broken_road
    assert ball_agendaatom.get_value("open") == after_broken_open
    assert ball_agendaatom.get_value("nigh") == after_broken_nigh
    assert ball_agendaatom.get_value("divisor") == after_broken_divisor
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_reasonunit_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_agendaunit.make_road(knee_road, medical_text)
    before_sue_agendaunit.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_agendaunit.add_idea(ideaunit_shop(medical_text), knee_road)

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_medical_suff_idea_active = False
    after_sue_agendaunit.edit_idea_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_suff_idea_active=after_medical_suff_idea_active,
    )

    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")
    x_keylist = [
        atom_insert(),
        "agenda_idea_reasonunit",
        ball_road,
        medical_road,
    ]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("road") == ball_road
    assert ball_agendaatom.get_value("base") == medical_road
    assert (
        ball_agendaatom.get_value("suff_idea_active") == after_medical_suff_idea_active
    )
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_reasonunit_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_agendaunit.make_road(knee_road, medical_text)
    before_sue_agendaunit.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_agendaunit.add_idea(ideaunit_shop(medical_text), knee_road)
    before_medical_suff_idea_active = True
    before_sue_agendaunit.edit_idea_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_suff_idea_active=before_medical_suff_idea_active,
    )

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_medical_suff_idea_active = False
    after_sue_agendaunit.edit_idea_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_suff_idea_active=after_medical_suff_idea_active,
    )

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")
    x_keylist = [
        atom_update(),
        "agenda_idea_reasonunit",
        ball_road,
        medical_road,
    ]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("road") == ball_road
    assert ball_agendaatom.get_value("base") == medical_road
    assert (
        ball_agendaatom.get_value("suff_idea_active") == after_medical_suff_idea_active
    )
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_reasonunit_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_agendaunit.make_road(knee_road, medical_text)
    before_sue_agendaunit.add_l1_idea(ideaunit_shop(knee_text))
    before_sue_agendaunit.add_idea(ideaunit_shop(medical_text), knee_road)
    before_medical_suff_idea_active = True
    before_sue_agendaunit.edit_idea_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_suff_idea_active=before_medical_suff_idea_active,
    )

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_ball_idea = after_sue_agendaunit.get_idea_obj(ball_road)
    after_ball_idea.del_reasonunit_base(medical_road)

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")
    x_keylist = [
        atom_delete(),
        "agenda_idea_reasonunit",
        ball_road,
        medical_road,
    ]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("road") == ball_road
    assert ball_agendaatom.get_value("base") == medical_road
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_suffgroup_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_agendaunit.add_partyunit(rico_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_ball_ideaunit = after_sue_agendaunit.get_idea_obj(ball_road)
    after_ball_ideaunit._assignedunit.set_suffgroup(rico_text)

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")
    x_keylist = [
        atom_insert(),
        "agenda_idea_suffgroup",
        ball_road,
        rico_text,
    ]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("road") == ball_road
    assert ball_agendaatom.get_value("group_id") == rico_text
    assert get_agendaatom_total_count(sue_bookunit) == 1


def test_BookUnit_add_all_different_agendaatoms_Creates_AgendaAtom_idea_suffgroup_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_agendaunit.add_partyunit(rico_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_idea(ideaunit_shop(ball_text), sports_road)
    before_ball_ideaunit = before_sue_agendaunit.get_idea_obj(ball_road)
    before_ball_ideaunit._assignedunit.set_suffgroup(rico_text)

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_ball_ideaunit = after_sue_agendaunit.get_idea_obj(ball_road)
    after_ball_ideaunit._assignedunit.del_suffgroup(rico_text)

    # WHEN
    sue_bookunit = bookunit_shop()
    sue_bookunit.add_all_different_agendaatoms(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_agendaatom_keys(sue_bookunit)=}")
    x_keylist = [
        atom_delete(),
        "agenda_idea_suffgroup",
        ball_road,
        rico_text,
    ]
    ball_agendaatom = get_nested_value(sue_bookunit.agendaatoms, x_keylist)
    assert ball_agendaatom.get_value("road") == ball_road
    assert ball_agendaatom.get_value("group_id") == rico_text
    assert get_agendaatom_total_count(sue_bookunit) == 1
