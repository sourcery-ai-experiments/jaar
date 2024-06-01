from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.listen import (
    get_debtors_roll,
    get_ordered_debtors_roll,
    listen_to_speaker_belief,
)


def test_set_listen_to_speaker_belief_SetsBelief():
    # GIVEN
    yao_text = "Yao"
    yao_listener = agendaunit_shop(yao_text)
    casa_text = "casa"
    casa_road = yao_listener.make_l1_road(casa_text)
    status_text = "status"
    status_road = yao_listener.make_road(casa_road, status_text)
    clean_text = "clean"
    clean_road = yao_listener.make_road(status_road, clean_text)
    dirty_text = "dirty"
    dirty_road = yao_listener.make_road(status_road, dirty_text)
    sweep_text = "sweep"
    sweep_road = yao_listener.make_road(casa_road, sweep_text)

    yao_listener.add_partyunit(yao_text)
    yao_listener.set_party_pool(20)
    yao_listener.add_idea(ideaunit_shop(clean_text), status_road)
    yao_listener.add_idea(ideaunit_shop(dirty_text), status_road)
    yao_listener.add_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
    yao_listener.edit_idea_attr(
        sweep_road, reason_base=status_road, reason_premise=dirty_road
    )
    missing_belief_bases = list(yao_listener.get_missing_belief_bases().keys())

    yao_speaker = agendaunit_shop(yao_text)
    yao_speaker.set_belief(status_road, clean_road, create_missing_ideas=True)
    assert yao_listener.get_missing_belief_bases().keys() == {status_road}

    # WHEN
    listen_to_speaker_belief(yao_listener, yao_speaker, missing_belief_bases)

    # THEN
    assert len(yao_listener.get_missing_belief_bases().keys()) == 0


# def test_set_listen_to_speaker_belief_DoesNotOverrideBelief():
#     # GIVEN
#     yao_text = "Yao"
#     yao_listener = agendaunit_shop(yao_text)
#     yao_listener.add_partyunit(yao_text)
#     yao_listener.set_party_pool(20)
#     casa_text = "casa"
#     casa_road = yao_listener.make_l1_road(casa_text)
#     status_text = "status"
#     status_road = yao_listener.make_road(casa_road, status_text)
#     clean_text = "clean"
#     clean_road = yao_listener.make_road(status_road, clean_text)
#     dirty_text = "dirty"
#     dirty_road = yao_listener.make_road(status_road, dirty_text)
#     sweep_text = "sweep"
#     sweep_road = yao_listener.make_road(casa_road, sweep_text)
#     fridge_text = "fridge"
#     fridge_road = yao_listener.make_road(casa_road, fridge_text)
#     running_text = "running"
#     running_road = yao_listener.make_road(fridge_road, running_text)

#     yao_listener.add_idea(ideaunit_shop(running_text), fridge_road)
#     yao_listener.add_idea(ideaunit_shop(clean_text), status_road)
#     yao_listener.add_idea(ideaunit_shop(dirty_text), status_road)
#     yao_listener.add_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
#     yao_listener.edit_idea_attr(
#         sweep_road, reason_base=status_road, reason_premise=dirty_road
#     )
#     yao_listener.edit_idea_attr(
#         sweep_road, reason_base=fridge_road, reason_premise=running_road
#     )
#     assert len(yao_listener.get_missing_belief_bases()) == 2
#     yao_listener.set_belief(status_road, dirty_road)
#     assert len(yao_listener.get_missing_belief_bases()) == 1
#     assert yao_listener.get_belief(status_road).pick == dirty_road

#     # WHEN
#     yao_speaker = agendaunit_shop(yao_text)
#     yao_speaker.set_belief(status_road, clean_road, create_missing_ideas=True)
#     yao_speaker.set_belief(fridge_road, running_road, create_missing_ideas=True)
#     missing_belief_bases = list(yao_listener.get_missing_belief_bases().keys())
#     listen_to_speaker_belief(yao_listener, yao_speaker, missing_belief_bases)

#     # THEN
#     assert len(yao_listener.get_missing_belief_bases()) == 0
#     # did not grab speaker's beliefunit
#     assert yao_listener.get_belief(status_road).pick == dirty_road
#     # grabed speaker's beliefunit
#     assert yao_listener.get_belief(fridge_road).pick == running_road
