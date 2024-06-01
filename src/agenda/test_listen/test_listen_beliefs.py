from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import agendaunit_shop
from src.agenda.listen import (
    create_listen_basis,
    listen_to_speakers_belief,
    listen_to_speakers_intent,
)
from src.agenda.examples.agenda_env import get_texas_econnox, env_dir_setup_cleanup
from src.agenda.examples.example_listen import (
    casa_text,
    cook_text,
    eat_text,
    hungry_text,
    full_text,
    clean_text,
    casa_road,
    cook_road,
    eat_road,
    hungry_road,
    full_road,
    clean_road,
    get_example_zia_speaker,
    get_example_yao_speaker,
)


def test_listen_to_speakers_belief_SetsSingleBeliefUnit_v1(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_listener = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_creditor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_listener.add_partyunit(zia_text, zia_creditor_weight, zia_debtor_weight)
    yao_listener.set_party_pool(zia_pool)

    zia_speaker = get_example_zia_speaker()
    texas_econnox = get_texas_econnox()
    texas_econnox.save_file_job(zia_text, zia_speaker.get_json(), True)

    new_yao_agenda = create_listen_basis(yao_listener)
    assert new_yao_agenda.get_missing_belief_bases().get(eat_road()) is None
    listen_to_speakers_intent(new_yao_agenda, texas_econnox.jobs_dir(), yao_listener)
    assert new_yao_agenda.get_missing_belief_bases().get(eat_road()) != None

    # WHEN
    listen_to_speakers_belief(new_yao_agenda, texas_econnox.jobs_dir(), yao_listener)

    # THEN
    assert new_yao_agenda.get_missing_belief_bases().get(eat_road()) is None


def test_listen_to_speakers_belief_SetsSingleBeliefUnitWithOtherTask(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_listener = agendaunit_shop(yao_text)
    yao_creditor_weight = 47
    yao_debtor_weight = 41
    yao_pool = 87
    zia_text = "Zia"
    yao_listener.add_partyunit(zia_text, yao_creditor_weight, yao_debtor_weight)
    yao_listener.set_party_pool(yao_pool)

    zia_speaker = get_example_zia_speaker()
    zia_speaker.add_idea(ideaunit_shop(clean_text(), pledge=True), casa_road())
    clean_ideaunit = zia_speaker.get_idea_obj(clean_road())
    clean_ideaunit._assignedunit.set_suffgroup(yao_text)
    texas_econnox = get_texas_econnox()
    texas_econnox.save_file_job(zia_text, zia_speaker.get_json(), True)

    new_yao_agenda = create_listen_basis(yao_listener)
    assert new_yao_agenda.get_missing_belief_bases().get(eat_road()) is None
    listen_to_speakers_intent(new_yao_agenda, texas_econnox.jobs_dir(), yao_listener)
    assert new_yao_agenda.get_missing_belief_bases().get(eat_road()) != None
    assert new_yao_agenda.get_belief(eat_road()) is None

    # WHEN
    listen_to_speakers_belief(new_yao_agenda, texas_econnox.jobs_dir(), yao_listener)

    # THEN
    assert new_yao_agenda.get_belief(eat_road()) != None


def test_listen_to_speaker_belief_GetsBeliefsFromSrcAgendaSelfNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # GIVEN
    # yao_src_listener has belief eat_road = full
    # yao_speaker has belief eat_road = hungry
    # new_yao_agenda picks yao_src_listener belief eat_road = full
    yao_src_listener = get_example_yao_speaker()
    yao_src_listener.set_belief(eat_road(), full_road())
    assert yao_src_listener.get_belief(eat_road()).pick == full_road()

    yao_speaker = get_example_yao_speaker()
    assert yao_speaker.get_belief(eat_road()).pick == hungry_road()
    texas_econnox = get_texas_econnox()
    texas_econnox.save_file_job("Yao", yao_speaker.get_json(), True)

    new_yao_agenda = create_listen_basis(yao_src_listener)
    assert new_yao_agenda.get_belief(eat_road()) is None
    assert new_yao_agenda.get_missing_belief_bases().get(eat_road()) is None
    listen_to_speakers_intent(
        new_yao_agenda, texas_econnox.jobs_dir(), yao_src_listener
    )
    assert new_yao_agenda.get_missing_belief_bases().get(eat_road()) != None

    # WHEN
    listen_to_speakers_belief(
        new_yao_agenda, texas_econnox.jobs_dir(), yao_src_listener
    )

    # THEN
    assert new_yao_agenda.get_belief(eat_road()) != None
    assert new_yao_agenda.get_belief(eat_road()).pick == full_road()


def test_listen_to_speaker_belief_SetsPrioritizesSelfBeliefsOverOthers(
    env_dir_setup_cleanup,
):
    # GIVEN
    # yao_src_listener has belief eat_road = full
    # zia_speaker has belief eat_road = hungry
    # new_yao_agenda picks yao_src_listener belief eat_road = full
    yao_src_listener = get_example_yao_speaker()
    yao_src_listener.set_belief(eat_road(), full_road())
    assert yao_src_listener.get_belief(eat_road()).pick == full_road()

    zia_speaker = get_example_zia_speaker()
    zia_speaker.set_belief(eat_road(), hungry_road())
    assert zia_speaker.get_belief(eat_road()).pick == hungry_road()
    texas_econnox = get_texas_econnox()
    texas_econnox.save_file_job("Zia", zia_speaker.get_json(), True)

    new_yao_agenda = create_listen_basis(yao_src_listener)
    assert new_yao_agenda.get_belief(eat_road()) is None
    assert new_yao_agenda.get_missing_belief_bases().get(eat_road()) is None
    listen_to_speakers_intent(
        new_yao_agenda, texas_econnox.jobs_dir(), yao_src_listener
    )
    assert new_yao_agenda.get_missing_belief_bases().get(eat_road()) != None

    # WHEN
    listen_to_speakers_belief(
        new_yao_agenda, texas_econnox.jobs_dir(), yao_src_listener
    )

    # THEN
    assert new_yao_agenda.get_belief(eat_road()) != None
    assert new_yao_agenda.get_belief(eat_road()).pick == full_road()


# def test_listen_to_speaker_belief_SetsBelief(env_dir_setup_cleanup):
#     # GIVEN
#     yao_text = "Yao"
#     sue_text = "Sue"
#     sue_speaker = agendaunit_shop(yao_text)
#     casa_text = "casa"
#     casa_road = sue_speaker.make_l1_road(casa_text)
#     status_text = "status"
#     status_road = sue_speaker.make_road(casa_road, status_text)
#     clean_text = "clean"
#     clean_road = sue_speaker.make_road(status_road, clean_text)
#     dirty_text = "dirty"
#     dirty_road = sue_speaker.make_road(status_road, dirty_text)
#     sweep_text = "sweep"
#     sweep_road = sue_speaker.make_road(casa_road, sweep_text)

#     sue_speaker.add_partyunit(yao_text)
#     sue_speaker.set_party_pool(20)
#     sue_speaker.add_idea(ideaunit_shop(clean_text), status_road)
#     sue_speaker.add_idea(ideaunit_shop(dirty_text), status_road)
#     sue_speaker.add_idea(ideaunit_shop(sweep_text, pledge=True), casa_road)
#     sue_speaker.edit_idea_attr(
#         sweep_road, reason_base=status_road, reason_premise=dirty_road
#     )
#     sweep_idea = sue_speaker.get_idea_obj(sweep_road)
#     sweep_idea._assignedunit.set_suffgroup(yao_text)

#     texas_econnox = get_texas_econnox()
#     texas_econnox.save_file_job(sue_text, sue_speaker.get_json(), True)
#     yao_listener = agendaunit_shop(yao_text)
#     yao_listener.add_partyunit(yao_text)
#     yao_listener.add_partyunit(sue_text)
#     new_yao_agenda = create_listen_basis(yao_listener)
#     print(f"{new_yao_agenda.get_idea_dict().keys()=}")
#     # assert new_yao_agenda.get_missing_belief_bases().get(status_road) is None
#     listen_to_speakers_intent(new_yao_agenda, texas_econnox.jobs_dir())
#     print(f"{new_yao_agenda.get_idea_dict().keys()=}")
#     assert new_yao_agenda.get_missing_belief_bases().get(status_road) != None

#     # assert new_yao_agenda.get_missing_belief_bases().keys() == {status_road}
#     # sue_speaker.set_belief(status_road, clean_road, create_missing_ideas=True)

#     # # WHEN
#     # listen_to_speakers_belief(yao_listener, yao_speaker, missing_belief_bases)

#     # # THEN
#     # assert len(yao_listener.get_missing_belief_bases().keys()) == 0
#     assert 1 == 3


# def test_listen_to_speaker_belief_DoesNotOverrideBelief():
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
