from src._road.road import create_road
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.promise import create_promise
from copy import deepcopy as copy_deepcopy


def test_create_promise_EmptyParametersDoNotChangeAgenda():
    # GIVEN
    sue_text = "Sue"
    sue_agenda = agendaunit_shop(sue_text)
    old_sue_agenda = copy_deepcopy(sue_agenda)

    # WHEN
    empty_road = create_road("")
    create_promise(x_agenda=sue_agenda, promise_road=empty_road)

    # THEN
    assert sue_agenda == old_sue_agenda

    # WHEN
    create_promise(x_agenda=sue_agenda, promise_road=None)

    # THEN
    assert sue_agenda == old_sue_agenda


def test_create_promise_CorrectlyAddsPromiseToAgenda():
    # GIVEN
    sue_text = "Sue"
    new_sue_agenda = agendaunit_shop(sue_text)
    old_sue_agenda = copy_deepcopy(new_sue_agenda)

    # WHEN
    clean_road = new_sue_agenda.make_l1_road("clean")
    create_promise(new_sue_agenda, clean_road)

    # THEN
    assert new_sue_agenda != old_sue_agenda
    assert old_sue_agenda.idea_exists(clean_road) == False
    assert new_sue_agenda.idea_exists(clean_road)
    clean_idea = new_sue_agenda.get_idea_obj(clean_road)
    assert clean_idea.promise


def test_create_promise_CorrectlyChangesAgendaNonPromiseIdeaToPromiseIdea():
    # GIVEN
    sue_text = "Sue"
    sue_agenda = agendaunit_shop(sue_text)
    clean_text = "clean"
    clean_idea = ideaunit_shop(clean_text)
    clean_road = sue_agenda.make_l1_road(clean_text)
    floor_text = "floor"
    floor_road = sue_agenda.make_road(clean_road, floor_text)
    floor_idea = ideaunit_shop(floor_text, promise=True)

    sue_agenda.add_l1_idea(clean_idea)
    sue_agenda.add_idea(floor_idea, clean_road)
    old_clean_idea = sue_agenda.get_idea_obj(clean_road)
    old_floor_idea = sue_agenda.get_idea_obj(floor_road)
    assert old_clean_idea.promise == False
    assert old_floor_idea.promise

    # WHEN
    create_promise(sue_agenda, clean_road)

    # THEN
    assert sue_agenda.idea_exists(clean_road)
    assert sue_agenda.idea_exists(floor_road)
    new_clean_idea = sue_agenda.get_idea_obj(clean_road)
    new_floor_idea = sue_agenda.get_idea_obj(floor_road)
    assert new_clean_idea.promise
    assert new_floor_idea.promise


def test_create_promise_CorrectlySets_suffgroup():
    # GIVEN
    sue_text = "Sue"
    sue_agenda = agendaunit_shop(sue_text)
    clean_text = "clean"
    clean_road = sue_agenda.make_l1_road(clean_text)
    floor_text = "floor"
    floor_road = sue_agenda.make_road(clean_road, floor_text)
    bob_text = "Bob"
    floor_idea = ideaunit_shop(floor_text, promise=True)
    floor_idea._assignedunit.set_suffgroup(bob_text)
    sue_agenda.add_idea(floor_idea, clean_road)
    floor_idea = sue_agenda.get_idea_obj(floor_road)
    assert floor_idea._assignedunit.suffgroup_exists(bob_text) == False

    # WHEN
    create_promise(sue_agenda, floor_road, bob_text)

    # THEN
    assert floor_idea._assignedunit.suffgroup_exists(bob_text)
    yao_text = "Yao"
    assert sue_agenda.get_party(yao_text) is None
    assert floor_idea._assignedunit.suffgroup_exists(yao_text) == False

    # WHEN
    create_promise(sue_agenda, floor_road, yao_text)

    # THEN
    assert sue_agenda.get_party(yao_text) != None
    assert floor_idea._assignedunit.suffgroup_exists(yao_text)
