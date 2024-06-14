from src.agenda.idea import balancelink_shop
from src.agenda.party import partylink_shop
from src.agenda.reason_oath import beliefunit_shop
from src.agenda.oath import oathunit_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.atom.quark import quark_insert, quark_update, quark_delete
from src.atom.nuc import NucUnit, nucunit_shop
from src.listen.examples.examples import get_agenda_with_4_levels
from src._instrument.python import get_nested_value, get_empty_list_if_None
from copy import deepcopy as copy_deepcopy


def print_quarkunit_keys(x_nucunit: NucUnit):
    for x_quarkunit in get_delete_quarkunit_list(x_nucunit):
        print(
            f"DELETE {x_quarkunit.category} {list(x_quarkunit.required_args.values())}"
        )
    for x_quarkunit in get_update_quarkunit_list(x_nucunit):
        print(
            f"UPDATE {x_quarkunit.category} {list(x_quarkunit.required_args.values())}"
        )
    for x_quarkunit in get_insert_quarkunit_list(x_nucunit):
        print(
            f"INSERT {x_quarkunit.category} {list(x_quarkunit.required_args.values())}"
        )


def get_delete_quarkunit_list(x_nucunit: NucUnit) -> list:
    return get_empty_list_if_None(
        x_nucunit._get_crud_quarkunits_list().get(quark_delete())
    )


def get_insert_quarkunit_list(x_nucunit: NucUnit):
    return get_empty_list_if_None(
        x_nucunit._get_crud_quarkunits_list().get(quark_insert())
    )


def get_update_quarkunit_list(x_nucunit: NucUnit):
    return get_empty_list_if_None(
        x_nucunit._get_crud_quarkunits_list().get(quark_update())
    )


def get_quarkunit_total_count(x_nucunit: NucUnit) -> int:
    return (
        len(get_delete_quarkunit_list(x_nucunit))
        + len(get_insert_quarkunit_list(x_nucunit))
        + len(get_update_quarkunit_list(x_nucunit))
    )


def test_NucUnit_create_quarkunits_CorrectHandlesEmptyAgendas():
    # GIVEN
    sue_agenda = get_agenda_with_4_levels()
    sue_nucunit = nucunit_shop()
    assert sue_nucunit.quarkunits == {}

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(sue_agenda, sue_agenda)

    # THEN
    assert sue_nucunit.quarkunits == {}


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_partyunit_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agenda = agendaunit_shop(sue_text)
    after_sue_agenda = copy_deepcopy(before_sue_agenda)
    rico_text = "Rico"
    rico_credor_weight = 33
    rico_debtor_weight = 44
    after_sue_agenda.add_partyunit(rico_text, rico_credor_weight, rico_debtor_weight)

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(before_sue_agenda, after_sue_agenda)

    # THEN
    assert len(sue_nucunit.quarkunits.get(quark_insert()).get("agenda_partyunit")) == 1
    sue_insert_dict = sue_nucunit.quarkunits.get(quark_insert())
    sue_partyunit_dict = sue_insert_dict.get("agenda_partyunit")
    rico_quarkunit = sue_partyunit_dict.get(rico_text)
    assert rico_quarkunit.get_value("party_id") == rico_text
    assert rico_quarkunit.get_value("credor_weight") == rico_credor_weight
    assert rico_quarkunit.get_value("debtor_weight") == rico_debtor_weight

    print(f"{get_quarkunit_total_count(sue_nucunit)=}")
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_partyunit_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_agenda = agendaunit_shop(sue_text)
    before_sue_agenda.add_partyunit("Yao")
    before_sue_agenda.add_partyunit("Zia")

    after_sue_agenda = copy_deepcopy(before_sue_agenda)

    rico_text = "Rico"
    before_sue_agenda.add_partyunit(rico_text)

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(before_sue_agenda, after_sue_agenda)

    # THEN
    rico_quarkunit = get_nested_value(
        sue_nucunit.quarkunits, [quark_delete(), "agenda_partyunit", rico_text]
    )
    assert rico_quarkunit.get_value("party_id") == rico_text

    print(f"{get_quarkunit_total_count(sue_nucunit)=}")
    print_quarkunit_keys(sue_nucunit)
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_partyunit_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_agenda = agendaunit_shop(sue_text)
    after_sue_agenda = copy_deepcopy(before_sue_agenda)
    rico_text = "Rico"
    before_sue_agenda.add_partyunit(rico_text)
    rico_credor_weight = 33
    rico_debtor_weight = 44
    after_sue_agenda.add_partyunit(rico_text, rico_credor_weight, rico_debtor_weight)

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(before_sue_agenda, after_sue_agenda)

    # THEN
    x_keylist = [quark_update(), "agenda_partyunit", rico_text]
    rico_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert rico_quarkunit.get_value("party_id") == rico_text
    assert rico_quarkunit.get_value("credor_weight") == rico_credor_weight
    assert rico_quarkunit.get_value("debtor_weight") == rico_debtor_weight

    print(f"{get_quarkunit_total_count(sue_nucunit)=}")
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_AgendaUnit_simple_attrs_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_agenda = agendaunit_shop(sue_text)
    after_sue_agenda = copy_deepcopy(before_sue_agenda)
    x_agendaUnit_weight = 55
    x_planck = 0.5
    x_max_tree_traverse = 66
    x_meld_strategy = "override"
    x_monetary_desc = "dragon funds"
    x_party_credor_pool = 77
    x_party_debtor_pool = 88
    after_sue_agenda._weight = x_agendaUnit_weight
    after_sue_agenda._planck = x_planck
    after_sue_agenda.set_max_tree_traverse(x_max_tree_traverse)
    after_sue_agenda.set_meld_strategy(x_meld_strategy)
    after_sue_agenda.set_monetary_desc(x_monetary_desc)
    after_sue_agenda.set_party_credor_pool(x_party_credor_pool)
    after_sue_agenda.set_party_debtor_pool(x_party_debtor_pool)

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(before_sue_agenda, after_sue_agenda)

    # THEN
    x_keylist = [quark_update(), "agendaunit"]
    rico_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert rico_quarkunit.get_value("_max_tree_traverse") == x_max_tree_traverse
    assert rico_quarkunit.get_value("_meld_strategy") == x_meld_strategy
    assert rico_quarkunit.get_value("_monetary_desc") == x_monetary_desc
    assert rico_quarkunit.get_value("_party_credor_pool") == x_party_credor_pool
    assert rico_quarkunit.get_value("_party_debtor_pool") == x_party_debtor_pool
    assert rico_quarkunit.get_value("_weight") == x_agendaUnit_weight
    assert rico_quarkunit.get_value("_planck") == x_planck

    print(f"{get_quarkunit_total_count(sue_nucunit)=}")
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_idea_partylink_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    rico_text = "Rico"
    carm_text = "Carmen"
    after_sue_agendaunit.add_partyunit(rico_text)
    after_sue_agendaunit.add_partyunit(carm_text)
    run_text = ",runners"
    run_ideaunit = ideaunit_shop(run_text)
    rico_credor_weight = 77
    rico_debtor_weight = 88
    rico_partylink = partylink_shop(rico_text, rico_credor_weight, rico_debtor_weight)
    run_ideaunit.set_partylink(rico_partylink)
    run_ideaunit.set_partylink(partylink_shop(carm_text))
    after_sue_agendaunit.set_ideaunit(run_ideaunit)
    # print(f"{after_sue_agendaunit.get_ideaunit(run_text)=}")

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    x_keylist = [quark_insert(), "agenda_ideaunit", run_text]
    rico_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert rico_quarkunit.get_value("idea_id") == run_text
    # print(f"\n{sue_nucunit.quarkunits=}")
    print(f"\n{rico_quarkunit=}")

    x_keylist = [quark_insert(), "agenda_idea_partylink", run_text, rico_text]
    rico_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert rico_quarkunit.get_value("idea_id") == run_text
    assert rico_quarkunit.get_value("party_id") == rico_text
    assert rico_quarkunit.get_value("credor_weight") == rico_credor_weight
    assert rico_quarkunit.get_value("debtor_weight") == rico_debtor_weight

    print_quarkunit_keys(sue_nucunit)
    print(f"{get_quarkunit_total_count(sue_nucunit)=}")
    assert len(get_delete_quarkunit_list(sue_nucunit)) == 0
    assert len(get_insert_quarkunit_list(sue_nucunit)) == 5
    assert len(get_delete_quarkunit_list(sue_nucunit)) == 0
    assert get_quarkunit_total_count(sue_nucunit) == 5


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_idea_partylink_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_agendaunit.add_partyunit(rico_text)
    before_sue_agendaunit.add_partyunit(carm_text)
    run_text = ",runners"
    run_ideaunit = ideaunit_shop(run_text)
    before_rico_credor_weight = 77
    before_rico_debtor_weight = 88
    run_ideaunit.set_partylink(
        partylink_shop(rico_text, before_rico_credor_weight, before_rico_debtor_weight)
    )
    run_ideaunit.set_partylink(partylink_shop(carm_text))
    before_sue_agendaunit.set_ideaunit(run_ideaunit)
    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_run_ideaunit = after_sue_agendaunit.get_ideaunit(run_text)
    after_rico_credor_weight = 55
    after_rico_debtor_weight = 66
    after_run_ideaunit.edit_partylink(
        rico_text, after_rico_credor_weight, after_rico_debtor_weight
    )

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    # x_keylist = [quark_update(), "agenda_ideaunit", run_text]
    # rico_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    # assert rico_quarkunit.get_value("idea_id") == run_text
    # print(f"\n{sue_nucunit.quarkunits=}")
    # print(f"\n{rico_quarkunit=}")

    x_keylist = [quark_update(), "agenda_idea_partylink", run_text, rico_text]
    rico_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert rico_quarkunit.get_value("idea_id") == run_text
    assert rico_quarkunit.get_value("party_id") == rico_text
    assert rico_quarkunit.get_value("credor_weight") == after_rico_credor_weight
    assert rico_quarkunit.get_value("debtor_weight") == after_rico_debtor_weight

    print(f"{get_quarkunit_total_count(sue_nucunit)=}")
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_idea_partylink_delete():
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
    run_ideaunit = ideaunit_shop(run_text)
    run_ideaunit.set_partylink(partylink_shop(rico_text))
    run_ideaunit.set_partylink(partylink_shop(carm_text))
    fly_text = ",flyers"
    fly_ideaunit = ideaunit_shop(fly_text)
    fly_ideaunit.set_partylink(partylink_shop(rico_text))
    fly_ideaunit.set_partylink(partylink_shop(carm_text))
    fly_ideaunit.set_partylink(partylink_shop(dizz_text))
    before_sue_agendaunit.set_ideaunit(run_ideaunit)
    before_sue_agendaunit.set_ideaunit(fly_ideaunit)
    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_sue_agendaunit.del_ideaunit(run_text)
    after_fly_ideaunit = after_sue_agendaunit.get_ideaunit(fly_text)
    after_fly_ideaunit.del_partylink(dizz_text)
    assert len(before_sue_agendaunit.get_ideaunit(fly_text)._partys) == 3
    assert len(before_sue_agendaunit.get_ideaunit(run_text)._partys) == 2
    assert len(after_sue_agendaunit.get_ideaunit(fly_text)._partys) == 2
    assert after_sue_agendaunit.get_ideaunit(run_text) is None

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    x_keylist = [quark_delete(), "agenda_ideaunit", run_text]
    rico_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert rico_quarkunit.get_value("idea_id") == run_text

    x_keylist = [quark_delete(), "agenda_idea_partylink", fly_text, dizz_text]
    rico_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert rico_quarkunit.get_value("idea_id") == fly_text
    assert rico_quarkunit.get_value("party_id") == dizz_text

    print(f"{get_quarkunit_total_count(sue_nucunit)=}")
    print_quarkunit_keys(sue_nucunit)
    assert len(get_delete_quarkunit_list(sue_nucunit)) == 4
    assert len(get_insert_quarkunit_list(sue_nucunit)) == 0
    assert len(get_update_quarkunit_list(sue_nucunit)) == 0
    assert get_quarkunit_total_count(sue_nucunit) == 4


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_oath(oathunit_shop(ball_text), sports_road)
    street_text = "street ball"
    street_road = before_sue_agendaunit.make_road(ball_road, street_text)
    before_sue_agendaunit.add_oath(oathunit_shop(street_text), ball_road)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_agendaunit.make_road(sports_road, disc_text)
    music_text = "music"
    before_sue_agendaunit.add_l1_oath(oathunit_shop(music_text))
    before_sue_agendaunit.add_oath(oathunit_shop(disc_text), sports_road)
    # create after without ball_oath and street_oath
    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_sue_agendaunit.del_oath_obj(ball_road)

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    x_category = "agenda_oathunit"
    print(f"{sue_nucunit.quarkunits.get(quark_delete()).get(x_category).keys()=}")

    x_keylist = [quark_delete(), "agenda_oathunit", ball_road, street_text]
    street_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert street_quarkunit.get_value("parent_road") == ball_road
    assert street_quarkunit.get_value("label") == street_text

    x_keylist = [quark_delete(), "agenda_oathunit", sports_road, ball_text]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("parent_road") == sports_road
    assert ball_quarkunit.get_value("label") == ball_text

    print(f"{get_quarkunit_total_count(sue_nucunit)=}")
    assert get_quarkunit_total_count(sue_nucunit) == 2


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_oath(oathunit_shop(ball_text), sports_road)
    street_text = "street ball"
    street_road = before_sue_agendaunit.make_road(ball_road, street_text)
    before_sue_agendaunit.add_oath(oathunit_shop(street_text), ball_road)

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    disc_text = "Ultimate Disc"
    disc_road = after_sue_agendaunit.make_road(sports_road, disc_text)
    after_sue_agendaunit.add_oath(oathunit_shop(disc_text), sports_road)
    music_text = "music"
    music_begin = 34
    music_close = 78
    music_meld_strategy = "override"
    music_weight = 55
    music_pledge = True
    music_road = after_sue_agendaunit.make_l1_road(music_text)
    after_sue_agendaunit.add_l1_oath(
        oathunit_shop(
            music_text,
            _begin=music_begin,
            _close=music_close,
            _meld_strategy=music_meld_strategy,
            _weight=music_weight,
            pledge=music_pledge,
        )
    )

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print_quarkunit_keys(sue_nucunit)

    x_keylist = [quark_insert(), "agenda_oathunit", sports_road, disc_text]
    street_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert street_quarkunit.get_value("parent_road") == sports_road
    assert street_quarkunit.get_value("label") == disc_text

    x_keylist = [
        quark_insert(),
        "agenda_oathunit",
        after_sue_agendaunit._real_id,
        music_text,
    ]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("label") == music_text
    assert ball_quarkunit.get_value("parent_road") == after_sue_agendaunit._real_id
    assert ball_quarkunit.get_value("_begin") == music_begin
    assert ball_quarkunit.get_value("_close") == music_close
    assert ball_quarkunit.get_value("_meld_strategy") == music_meld_strategy
    assert ball_quarkunit.get_value("_weight") == music_weight
    assert ball_quarkunit.get_value("pledge") == music_pledge

    assert get_quarkunit_total_count(sue_nucunit) == 2


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_update():
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
    before_music_pledge = True
    music_road = before_sue_agendaunit.make_l1_road(music_text)
    before_sue_agendaunit.add_l1_oath(
        oathunit_shop(
            music_text,
            _begin=before_music_begin,
            _close=before_music_close,
            _meld_strategy=before_music_meld_strategy,
            _weight=before_music_weight,
            pledge=before_music_pledge,
        )
    )

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_music_begin = 99
    after_music_close = 111
    after_music_meld_strategy = "default"
    after_music_weight = 22
    after_music_pledge = False
    after_sue_agendaunit.edit_oath_attr(
        music_road,
        begin=after_music_begin,
        close=after_music_close,
        meld_strategy=after_music_meld_strategy,
        weight=after_music_weight,
        pledge=after_music_pledge,
    )

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print_quarkunit_keys(sue_nucunit)

    x_keylist = [
        quark_update(),
        "agenda_oathunit",
        after_sue_agendaunit._real_id,
        music_text,
    ]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("parent_road") == after_sue_agendaunit._real_id
    assert ball_quarkunit.get_value("label") == music_text
    assert ball_quarkunit.get_value("_begin") == after_music_begin
    assert ball_quarkunit.get_value("_close") == after_music_close
    assert ball_quarkunit.get_value("_meld_strategy") == after_music_meld_strategy
    assert ball_quarkunit.get_value("_weight") == after_music_weight
    assert ball_quarkunit.get_value("pledge") == after_music_pledge

    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_balancelink_delete():
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
    run_ideaunit = ideaunit_shop(run_text)
    run_ideaunit.set_partylink(partylink_shop(rico_text))
    run_ideaunit.set_partylink(partylink_shop(carm_text))
    fly_text = ",flyers"
    fly_ideaunit = ideaunit_shop(fly_text)
    fly_ideaunit.set_partylink(partylink_shop(rico_text))
    fly_ideaunit.set_partylink(partylink_shop(carm_text))
    fly_ideaunit.set_partylink(partylink_shop(dizz_text))
    before_sue_au.set_ideaunit(run_ideaunit)
    before_sue_au.set_ideaunit(fly_ideaunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_au.make_road(sports_road, disc_text)
    before_sue_au.add_oath(oathunit_shop(ball_text), sports_road)
    before_sue_au.add_oath(oathunit_shop(disc_text), sports_road)
    before_sue_au.edit_oath_attr(ball_road, balancelink=balancelink_shop(run_text))
    before_sue_au.edit_oath_attr(ball_road, balancelink=balancelink_shop(fly_text))
    before_sue_au.edit_oath_attr(disc_road, balancelink=balancelink_shop(run_text))
    before_sue_au.edit_oath_attr(disc_road, balancelink=balancelink_shop(fly_text))

    after_sue_agendaunit = copy_deepcopy(before_sue_au)
    after_sue_agendaunit.edit_oath_attr(disc_road, balancelink_del=run_text)

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(before_sue_au, after_sue_agendaunit)

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")

    x_keylist = [quark_delete(), "agenda_oath_balancelink", disc_road, run_text]
    run_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert run_quarkunit.get_value("road") == disc_road
    assert run_quarkunit.get_value("idea_id") == run_text

    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_balancelink_insert():
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
    run_ideaunit = ideaunit_shop(run_text)
    run_ideaunit.set_partylink(partylink_shop(rico_text))
    run_ideaunit.set_partylink(partylink_shop(carm_text))
    fly_text = ",flyers"
    fly_ideaunit = ideaunit_shop(fly_text)
    fly_ideaunit.set_partylink(partylink_shop(rico_text))
    fly_ideaunit.set_partylink(partylink_shop(carm_text))
    fly_ideaunit.set_partylink(partylink_shop(dizz_text))
    before_sue_au.set_ideaunit(run_ideaunit)
    before_sue_au.set_ideaunit(fly_ideaunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    disc_text = "Ultimate Disc"
    disc_road = before_sue_au.make_road(sports_road, disc_text)
    before_sue_au.add_oath(oathunit_shop(ball_text), sports_road)
    before_sue_au.add_oath(oathunit_shop(disc_text), sports_road)
    before_sue_au.edit_oath_attr(ball_road, balancelink=balancelink_shop(run_text))
    before_sue_au.edit_oath_attr(disc_road, balancelink=balancelink_shop(fly_text))
    after_sue_au = copy_deepcopy(before_sue_au)
    after_sue_au.edit_oath_attr(ball_road, balancelink=balancelink_shop(fly_text))
    after_run_credor_weight = 44
    after_run_debtor_weight = 66
    after_sue_au.edit_oath_attr(
        disc_road,
        balancelink=balancelink_shop(
            run_text,
            credor_weight=after_run_credor_weight,
            debtor_weight=after_run_debtor_weight,
        ),
    )

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(before_sue_au, after_sue_au)

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")

    x_keylist = [quark_insert(), "agenda_oath_balancelink", disc_road, run_text]
    run_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert run_quarkunit.get_value("road") == disc_road
    assert run_quarkunit.get_value("idea_id") == run_text
    assert run_quarkunit.get_value("road") == disc_road
    assert run_quarkunit.get_value("idea_id") == run_text
    assert run_quarkunit.get_value("credor_weight") == after_run_credor_weight
    assert run_quarkunit.get_value("debtor_weight") == after_run_debtor_weight

    assert get_quarkunit_total_count(sue_nucunit) == 2


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_balancelink_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_au = agendaunit_shop(sue_text)
    rico_text = "Rico"
    carm_text = "Carmen"
    before_sue_au.add_partyunit(rico_text)
    before_sue_au.add_partyunit(carm_text)
    run_text = ",runners"
    run_ideaunit = ideaunit_shop(run_text)
    run_ideaunit.set_partylink(partylink_shop(rico_text))
    before_sue_au.set_ideaunit(run_ideaunit)
    sports_text = "sports"
    sports_road = before_sue_au.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_au.make_road(sports_road, ball_text)
    before_sue_au.add_oath(oathunit_shop(ball_text), sports_road)
    before_sue_au.edit_oath_attr(ball_road, balancelink=balancelink_shop(run_text))
    run_balancelink = before_sue_au.get_oath_obj(ball_road)._balancelinks.get(run_text)

    after_sue_agendaunit = copy_deepcopy(before_sue_au)
    after_credor_weight = 55
    after_debtor_weight = 66
    after_sue_agendaunit.edit_oath_attr(
        ball_road,
        balancelink=balancelink_shop(
            idea_id=run_text,
            credor_weight=after_credor_weight,
            debtor_weight=after_debtor_weight,
        ),
    )
    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(before_sue_au, after_sue_agendaunit)

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")

    x_keylist = [quark_update(), "agenda_oath_balancelink", ball_road, run_text]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("road") == ball_road
    assert ball_quarkunit.get_value("idea_id") == run_text
    assert ball_quarkunit.get_value("credor_weight") == after_credor_weight
    assert ball_quarkunit.get_value("debtor_weight") == after_debtor_weight
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_beliefunit_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_oath(oathunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    bend_text = "bendable"
    bend_road = before_sue_agendaunit.make_road(knee_road, bend_text)
    before_sue_agendaunit.add_oath(oathunit_shop(bend_text), knee_road)
    broken_text = "broke cartilage"
    broken_road = before_sue_agendaunit.make_road(knee_road, broken_text)
    before_sue_agendaunit.add_l1_oath(oathunit_shop(knee_text))
    before_sue_agendaunit.add_oath(oathunit_shop(broken_text), knee_road)
    before_broken_open = 11
    before_broken_nigh = 22
    before_sue_agendaunit.edit_oath_attr(
        ball_road,
        beliefunit=beliefunit_shop(
            knee_road, bend_road, before_broken_open, before_broken_nigh
        ),
    )

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_broken_open = 55
    after_broken_nigh = 66
    after_sue_agendaunit.edit_oath_attr(
        ball_road,
        beliefunit=beliefunit_shop(
            knee_road, broken_road, after_broken_open, after_broken_nigh
        ),
    )

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")

    x_keylist = [quark_update(), "agenda_oath_beliefunit", ball_road, knee_road]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("road") == ball_road
    assert ball_quarkunit.get_value("base") == knee_road
    assert ball_quarkunit.get_value("pick") == broken_road
    assert ball_quarkunit.get_value("open") == after_broken_open
    assert ball_quarkunit.get_value("nigh") == after_broken_nigh
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_beliefunit_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_oath(oathunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_agendaunit.make_road(knee_road, broken_text)
    before_sue_agendaunit.add_l1_oath(oathunit_shop(knee_text))
    before_sue_agendaunit.add_oath(oathunit_shop(broken_text), knee_road)

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_broken_open = 55
    after_broken_nigh = 66
    after_sue_agendaunit.edit_oath_attr(
        road=ball_road,
        beliefunit=beliefunit_shop(
            base=knee_road,
            pick=broken_road,
            open=after_broken_open,
            nigh=after_broken_nigh,
        ),
    )

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")
    x_keylist = [quark_insert(), "agenda_oath_beliefunit", ball_road, knee_road]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("road") == ball_road
    assert ball_quarkunit.get_value("base") == knee_road
    assert ball_quarkunit.get_value("pick") == broken_road
    assert ball_quarkunit.get_value("open") == after_broken_open
    assert ball_quarkunit.get_value("nigh") == after_broken_nigh
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_beliefunit_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_oath(oathunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    broken_text = "broke cartilage"
    broken_road = before_sue_agendaunit.make_road(knee_road, broken_text)
    before_sue_agendaunit.add_l1_oath(oathunit_shop(knee_text))
    before_sue_agendaunit.add_oath(oathunit_shop(broken_text), knee_road)

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    before_broken_open = 55
    before_broken_nigh = 66
    before_sue_agendaunit.edit_oath_attr(
        road=ball_road,
        beliefunit=beliefunit_shop(
            base=knee_road,
            pick=broken_road,
            open=before_broken_open,
            nigh=before_broken_nigh,
        ),
    )

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")
    x_keylist = [quark_delete(), "agenda_oath_beliefunit", ball_road, knee_road]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("road") == ball_road
    assert ball_quarkunit.get_value("base") == knee_road
    assert ball_quarkunit.get_value("road") == ball_road
    assert ball_quarkunit.get_value("base") == knee_road
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_reason_premiseunit_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_oath(oathunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    before_sue_agendaunit.add_l1_oath(oathunit_shop(knee_text))
    broken_text = "broke cartilage"
    broken_road = before_sue_agendaunit.make_road(knee_road, broken_text)
    before_sue_agendaunit.add_oath(oathunit_shop(broken_text), knee_road)
    bend_text = "bend"
    bend_road = before_sue_agendaunit.make_road(knee_road, bend_text)
    before_sue_agendaunit.add_oath(oathunit_shop(bend_text), knee_road)
    before_sue_agendaunit.edit_oath_attr(
        ball_road, reason_base=knee_road, reason_premise=bend_road
    )

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    broken_open = 45
    broken_nigh = 77
    broken_divisor = 3
    after_sue_agendaunit.edit_oath_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=broken_open,
        reason_premise_nigh=broken_nigh,
        reason_premise_divisor=broken_divisor,
    )

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")
    x_keylist = [
        quark_insert(),
        "agenda_oath_reason_premiseunit",
        ball_road,
        knee_road,
        broken_road,
    ]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("road") == ball_road
    assert ball_quarkunit.get_value("base") == knee_road
    assert ball_quarkunit.get_value("need") == broken_road
    assert ball_quarkunit.get_value("open") == broken_open
    assert ball_quarkunit.get_value("nigh") == broken_nigh
    assert ball_quarkunit.get_value("divisor") == broken_divisor
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_reason_premiseunit_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_oath(oathunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    before_sue_agendaunit.add_l1_oath(oathunit_shop(knee_text))
    broken_text = "broke cartilage"
    broken_road = before_sue_agendaunit.make_road(knee_road, broken_text)
    before_sue_agendaunit.add_oath(oathunit_shop(broken_text), knee_road)
    bend_text = "bend"
    bend_road = before_sue_agendaunit.make_road(knee_road, bend_text)
    before_sue_agendaunit.add_oath(oathunit_shop(bend_text), knee_road)
    before_sue_agendaunit.edit_oath_attr(
        ball_road, reason_base=knee_road, reason_premise=bend_road
    )
    broken_open = 45
    broken_nigh = 77
    broken_divisor = 3
    before_sue_agendaunit.edit_oath_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=broken_open,
        reason_premise_nigh=broken_nigh,
        reason_premise_divisor=broken_divisor,
    )
    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_sue_agendaunit.edit_oath_attr(
        ball_road,
        reason_del_premise_base=knee_road,
        reason_del_premise_need=broken_road,
    )

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")
    x_keylist = [
        quark_delete(),
        "agenda_oath_reason_premiseunit",
        ball_road,
        knee_road,
        broken_road,
    ]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("road") == ball_road
    assert ball_quarkunit.get_value("base") == knee_road
    assert ball_quarkunit.get_value("need") == broken_road
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_reason_premiseunit_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_oath(oathunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    before_sue_agendaunit.add_l1_oath(oathunit_shop(knee_text))
    broken_text = "broke cartilage"
    broken_road = before_sue_agendaunit.make_road(knee_road, broken_text)
    before_sue_agendaunit.add_oath(oathunit_shop(broken_text), knee_road)
    bend_text = "bend"
    bend_road = before_sue_agendaunit.make_road(knee_road, bend_text)
    before_sue_agendaunit.add_oath(oathunit_shop(bend_text), knee_road)
    before_sue_agendaunit.edit_oath_attr(
        ball_road, reason_base=knee_road, reason_premise=bend_road
    )
    before_broken_open = 111
    before_broken_nigh = 777
    before_broken_divisor = 13
    before_sue_agendaunit.edit_oath_attr(
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
    after_sue_agendaunit.edit_oath_attr(
        ball_road,
        reason_base=knee_road,
        reason_premise=broken_road,
        reason_premise_open=after_broken_open,
        reason_premise_nigh=after_broken_nigh,
        reason_premise_divisor=after_broken_divisor,
    )

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")
    x_keylist = [
        quark_update(),
        "agenda_oath_reason_premiseunit",
        ball_road,
        knee_road,
        broken_road,
    ]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("road") == ball_road
    assert ball_quarkunit.get_value("base") == knee_road
    assert ball_quarkunit.get_value("need") == broken_road
    assert ball_quarkunit.get_value("open") == after_broken_open
    assert ball_quarkunit.get_value("nigh") == after_broken_nigh
    assert ball_quarkunit.get_value("divisor") == after_broken_divisor
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_reasonunit_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_oath(oathunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_agendaunit.make_road(knee_road, medical_text)
    before_sue_agendaunit.add_l1_oath(oathunit_shop(knee_text))
    before_sue_agendaunit.add_oath(oathunit_shop(medical_text), knee_road)

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_medical_suff_oath_active = False
    after_sue_agendaunit.edit_oath_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_suff_oath_active=after_medical_suff_oath_active,
    )

    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")
    x_keylist = [
        quark_insert(),
        "agenda_oath_reasonunit",
        ball_road,
        medical_road,
    ]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("road") == ball_road
    assert ball_quarkunit.get_value("base") == medical_road
    assert (
        ball_quarkunit.get_value("suff_oath_active") == after_medical_suff_oath_active
    )
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_reasonunit_update():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_oath(oathunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_agendaunit.make_road(knee_road, medical_text)
    before_sue_agendaunit.add_l1_oath(oathunit_shop(knee_text))
    before_sue_agendaunit.add_oath(oathunit_shop(medical_text), knee_road)
    before_medical_suff_oath_active = True
    before_sue_agendaunit.edit_oath_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_suff_oath_active=before_medical_suff_oath_active,
    )

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_medical_suff_oath_active = False
    after_sue_agendaunit.edit_oath_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_suff_oath_active=after_medical_suff_oath_active,
    )

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")
    x_keylist = [
        quark_update(),
        "agenda_oath_reasonunit",
        ball_road,
        medical_road,
    ]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("road") == ball_road
    assert ball_quarkunit.get_value("base") == medical_road
    assert (
        ball_quarkunit.get_value("suff_oath_active") == after_medical_suff_oath_active
    )
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_reasonunit_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_oath(oathunit_shop(ball_text), sports_road)
    knee_text = "knee"
    knee_road = before_sue_agendaunit.make_l1_road(knee_text)
    medical_text = "get medical attention"
    medical_road = before_sue_agendaunit.make_road(knee_road, medical_text)
    before_sue_agendaunit.add_l1_oath(oathunit_shop(knee_text))
    before_sue_agendaunit.add_oath(oathunit_shop(medical_text), knee_road)
    before_medical_suff_oath_active = True
    before_sue_agendaunit.edit_oath_attr(
        road=ball_road,
        reason_base=medical_road,
        reason_suff_oath_active=before_medical_suff_oath_active,
    )

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_ball_oath = after_sue_agendaunit.get_oath_obj(ball_road)
    after_ball_oath.del_reasonunit_base(medical_road)

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")
    x_keylist = [
        quark_delete(),
        "agenda_oath_reasonunit",
        ball_road,
        medical_road,
    ]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("road") == ball_road
    assert ball_quarkunit.get_value("base") == medical_road
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_suffidea_insert():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_agendaunit.add_partyunit(rico_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_oath(oathunit_shop(ball_text), sports_road)

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_ball_oathunit = after_sue_agendaunit.get_oath_obj(ball_road)
    after_ball_oathunit._assignedunit.set_suffidea(rico_text)

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")
    x_keylist = [
        quark_insert(),
        "agenda_oath_suffidea",
        ball_road,
        rico_text,
    ]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("road") == ball_road
    assert ball_quarkunit.get_value("idea_id") == rico_text
    assert get_quarkunit_total_count(sue_nucunit) == 1


def test_NucUnit_add_all_different_quarkunits_Creates_QuarkUnit_oath_suffidea_delete():
    # GIVEN
    sue_text = "Sue"
    before_sue_agendaunit = agendaunit_shop(sue_text)
    rico_text = "Rico"
    before_sue_agendaunit.add_partyunit(rico_text)
    sports_text = "sports"
    sports_road = before_sue_agendaunit.make_l1_road(sports_text)
    ball_text = "basketball"
    ball_road = before_sue_agendaunit.make_road(sports_road, ball_text)
    before_sue_agendaunit.add_oath(oathunit_shop(ball_text), sports_road)
    before_ball_oathunit = before_sue_agendaunit.get_oath_obj(ball_road)
    before_ball_oathunit._assignedunit.set_suffidea(rico_text)

    after_sue_agendaunit = copy_deepcopy(before_sue_agendaunit)
    after_ball_oathunit = after_sue_agendaunit.get_oath_obj(ball_road)
    after_ball_oathunit._assignedunit.del_suffidea(rico_text)

    # WHEN
    sue_nucunit = nucunit_shop()
    sue_nucunit.add_all_different_quarkunits(
        before_sue_agendaunit, after_sue_agendaunit
    )

    # THEN
    print(f"{print_quarkunit_keys(sue_nucunit)=}")
    x_keylist = [
        quark_delete(),
        "agenda_oath_suffidea",
        ball_road,
        rico_text,
    ]
    ball_quarkunit = get_nested_value(sue_nucunit.quarkunits, x_keylist)
    assert ball_quarkunit.get_value("road") == ball_road
    assert ball_quarkunit.get_value("idea_id") == rico_text
    assert get_quarkunit_total_count(sue_nucunit) == 1
