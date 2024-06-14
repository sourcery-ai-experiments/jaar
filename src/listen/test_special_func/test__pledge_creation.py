from src._road.road import create_road
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.listen.special_func import create_pledge
from copy import deepcopy as copy_deepcopy


def test_create_pledge_SameAgendaWithEmptyParameters():
    # GIVEN
    sue_text = "Sue"
    sue_agenda = agendaunit_shop(sue_text)
    old_sue_agenda = copy_deepcopy(sue_agenda)

    # WHEN
    empty_road = create_road("")
    create_pledge(x_agenda=sue_agenda, pledge_road=empty_road)

    # THEN
    assert sue_agenda == old_sue_agenda

    # WHEN
    create_pledge(x_agenda=sue_agenda, pledge_road=None)

    # THEN
    assert sue_agenda == old_sue_agenda


def test_create_pledge_CorrectlyAddspledgeToAgenda():
    # GIVEN
    sue_text = "Sue"
    new_sue_agenda = agendaunit_shop(sue_text)
    old_sue_agenda = copy_deepcopy(new_sue_agenda)

    # WHEN
    clean_road = new_sue_agenda.make_l1_road("clean")
    create_pledge(new_sue_agenda, clean_road)

    # THEN
    assert new_sue_agenda != old_sue_agenda
    assert old_sue_agenda.idea_exists(clean_road) is False
    assert new_sue_agenda.idea_exists(clean_road)
    clean_idea = new_sue_agenda.get_idea_obj(clean_road)
    assert clean_idea.pledge


def test_create_pledge_CorrectlyModifiesAgendaNonpledgeIdeaTopledgeIdea():
    # GIVEN
    sue_text = "Sue"
    sue_agenda = agendaunit_shop(sue_text)
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    clean_road = sue_agenda.make_l1_road(clean_text)
    floor_text = "floor"
    floor_road = sue_agenda.make_road(clean_road, floor_text)
    floor_idea = ideaunit_shop(floor_text, pledge=True)

    sue_agenda.add_l1_idea(clean_idea)
    sue_agenda.add_idea(floor_idea, clean_road)
    old_clean_idea = sue_agenda.get_idea_obj(clean_road)
    old_floor_idea = sue_agenda.get_idea_obj(floor_road)
    assert old_clean_idea.pledge is False
    assert old_floor_idea.pledge

    # WHEN
    create_pledge(sue_agenda, clean_road)

    # THEN
    assert sue_agenda.idea_exists(clean_road)
    assert sue_agenda.idea_exists(floor_road)
    new_clean_idea = sue_agenda.get_idea_obj(clean_road)
    new_floor_idea = sue_agenda.get_idea_obj(floor_road)
    assert new_clean_idea.pledge
    assert new_floor_idea.pledge


def test_create_pledge_CorrectlySets_suffbelief():
    # GIVEN
    sue_text = "Sue"
    sue_agenda = agendaunit_shop(sue_text)
    clean_text = "clean"
    clean_road = sue_agenda.make_l1_road(clean_text)
    floor_text = "floor"
    floor_road = sue_agenda.make_road(clean_road, floor_text)
    bob_text = "Bob"
    floor_idea = ideaunit_shop(floor_text, pledge=True)
    floor_idea._assignedunit.set_suffbelief(bob_text)
    sue_agenda.add_idea(floor_idea, clean_road)
    floor_idea = sue_agenda.get_idea_obj(floor_road)
    assert floor_idea._assignedunit.suffbelief_exists(bob_text) is False

    # WHEN
    create_pledge(sue_agenda, floor_road, bob_text)

    # THEN
    assert floor_idea._assignedunit.suffbelief_exists(bob_text)
    yao_text = "Yao"
    assert sue_agenda.party_exists(yao_text) is False
    assert floor_idea._assignedunit.suffbelief_exists(yao_text) is False

    # WHEN
    create_pledge(sue_agenda, floor_road, yao_text)

    # THEN
    assert sue_agenda.party_exists(yao_text)
    assert floor_idea._assignedunit.suffbelief_exists(yao_text)
