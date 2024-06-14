from src.agenda.oath import oathunit_shop
from src.agenda.agenda import agendaunit_shop
from src.listen.listen import (
    create_listen_basis,
    listen_to_beliefs_role_job,
    listen_to_intents_role_job,
)
from src.listen.examples.listen_env import get_texas_userhub, env_dir_setup_cleanup
from src.listen.examples.example_listen import (
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
    get_example_bob_speaker,
)


def test_listen_to_beliefs_role_job_SetsSingleBeliefUnit_v1(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    zia_text = "Zia"
    zia_credor_weight = 47
    zia_debtor_weight = 41
    zia_pool = 87
    yao_role.add_partyunit(zia_text, zia_credor_weight, zia_debtor_weight)
    yao_role.set_party_pool(zia_pool)
    sue_texas_userhub = get_texas_userhub()
    sue_texas_userhub.save_role_agenda(yao_role)

    zia_job = get_example_zia_speaker()
    sue_texas_userhub.save_job_agenda(zia_job)
    print(f"         {sue_texas_userhub.job_path(zia_text)=}")

    new_yao_job = create_listen_basis(yao_role)
    assert new_yao_job.get_missing_belief_bases().get(eat_road()) is None
    listen_to_intents_role_job(new_yao_job, sue_texas_userhub)
    assert new_yao_job.get_missing_belief_bases().get(eat_road()) != None

    # WHEN
    listen_to_beliefs_role_job(new_yao_job, sue_texas_userhub)

    # THEN
    assert new_yao_job.get_missing_belief_bases().get(eat_road()) is None


def test_listen_to_beliefs_role_job_SetsSingleBeliefUnitWithOtherTask(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_text = "Yao"
    yao_role = agendaunit_shop(yao_text)
    yao_credor_weight = 47
    yao_debtor_weight = 41
    yao_pool = 87
    zia_text = "Zia"
    yao_role.add_partyunit(zia_text, yao_credor_weight, yao_debtor_weight)
    yao_role.set_party_pool(yao_pool)
    sue_texas_userhub = get_texas_userhub()
    sue_texas_userhub.save_role_agenda(yao_role)

    zia_job = get_example_zia_speaker()
    zia_job.add_oath(oathunit_shop(clean_text(), pledge=True), casa_road())
    clean_oathunit = zia_job.get_oath_obj(clean_road())
    clean_oathunit._assignedunit.set_suffidea(yao_text)
    sue_texas_userhub.save_job_agenda(zia_job)

    new_yao_job = create_listen_basis(yao_role)
    assert new_yao_job.get_missing_belief_bases().get(eat_road()) is None
    listen_to_intents_role_job(new_yao_job, sue_texas_userhub)
    assert new_yao_job.get_missing_belief_bases().get(eat_road()) != None
    assert new_yao_job.get_belief(eat_road()) is None

    # WHEN
    listen_to_beliefs_role_job(new_yao_job, sue_texas_userhub)

    # THEN
    assert new_yao_job.get_belief(eat_road()) != None


def test_listen_to_beliefs_role_job_GetsBeliefsFromSrcAgendaSelfNotSpeakerSelf(
    env_dir_setup_cleanup,
):
    # GIVEN
    # yao_role has belief eat_road = full
    # yao_job has belief eat_road = hungry
    # new_yao_job picks yao_role belief eat_road = full
    yao_role = get_example_yao_speaker()
    yao_role.set_belief(eat_road(), full_road())
    sue_texas_userhub = get_texas_userhub()
    sue_texas_userhub.save_role_agenda(yao_role)
    print(f"{sue_texas_userhub.role_path(yao_role)=}")
    assert yao_role.get_belief(eat_road()).pick == full_road()

    old_yao_job = get_example_yao_speaker()
    assert old_yao_job.get_belief(eat_road()).pick == hungry_road()
    sue_texas_userhub.save_job_agenda(old_yao_job)

    new_yao_job = create_listen_basis(yao_role)
    assert new_yao_job.get_belief(eat_road()) is None
    assert new_yao_job.get_missing_belief_bases().get(eat_road()) is None
    listen_to_intents_role_job(new_yao_job, sue_texas_userhub)
    assert new_yao_job.get_missing_belief_bases().get(eat_road()) != None

    # WHEN
    listen_to_beliefs_role_job(new_yao_job, sue_texas_userhub)

    # THEN
    assert new_yao_job.get_belief(eat_road()) != None
    assert new_yao_job.get_belief(eat_road()).pick == full_road()


def test_listen_to_beliefs_role_job_ConfirmNoBeliefPickedFromOwnersSpeakerDirAgenda_v1(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_role = get_example_yao_speaker()
    yao_role.del_belief(eat_road())
    assert yao_role.get_belief(eat_road()) is None
    sue_texas_userhub = get_texas_userhub()
    sue_texas_userhub.save_role_agenda(yao_role)

    zia_job = get_example_zia_speaker()
    zia_job.set_belief(eat_road(), eat_road())
    assert zia_job.get_belief(eat_road()).pick == eat_road()
    sue_texas_userhub.save_job_agenda(zia_job)

    old_yao_job = get_example_yao_speaker()
    assert old_yao_job.get_belief(eat_road()).pick == hungry_road()
    sue_texas_userhub.save_job_agenda(old_yao_job)

    new_yao_job = create_listen_basis(yao_role)
    assert new_yao_job.get_belief(eat_road()) is None
    assert new_yao_job.get_missing_belief_bases().get(eat_road()) is None
    listen_to_intents_role_job(new_yao_job, sue_texas_userhub)
    print(f"{new_yao_job.get_missing_belief_bases().keys()=}")
    print(f"{new_yao_job._oathroot._beliefunits.keys()=}")
    assert new_yao_job.get_missing_belief_bases().get(eat_road()) != None

    # WHEN
    listen_to_beliefs_role_job(new_yao_job, sue_texas_userhub)

    # THEN
    assert yao_role.get_belief(eat_road()) is None
    assert zia_job.get_belief(eat_road()).pick == eat_road()
    assert old_yao_job.get_belief(eat_road()).pick == hungry_road()
    assert new_yao_job.get_belief(eat_road()).pick == eat_road()


def test_listen_to_beliefs_role_job_SetsPrioritizesSelfBeliefsOverOthers(
    env_dir_setup_cleanup,
):
    # GIVEN
    yao_role = get_example_yao_speaker()
    yao_role.set_belief(eat_road(), full_road())
    assert yao_role.get_belief(eat_road()).pick == full_road()
    sue_texas_userhub = get_texas_userhub()
    sue_texas_userhub.save_role_agenda(yao_role)

    zia_job = get_example_zia_speaker()
    zia_job.set_belief(eat_road(), hungry_road())
    assert zia_job.get_belief(eat_road()).pick == hungry_road()
    sue_texas_userhub.save_job_agenda(zia_job)

    new_yao_job = create_listen_basis(yao_role)
    assert new_yao_job.get_belief(eat_road()) is None
    assert new_yao_job.get_missing_belief_bases().get(eat_road()) is None
    listen_to_intents_role_job(new_yao_job, sue_texas_userhub)
    assert new_yao_job.get_missing_belief_bases().get(eat_road()) != None

    # WHEN
    listen_to_beliefs_role_job(new_yao_job, sue_texas_userhub)

    # THEN
    assert new_yao_job.get_belief(eat_road()) != None
    assert new_yao_job.get_belief(eat_road()).pick == full_road()


def test_listen_to_beliefs_role_job_ConfirmNoBeliefPickedFromOwnersSpeakerDirAgenda_v2(
    env_dir_setup_cleanup,
):
    # GIVEN
    zia_job = get_example_zia_speaker()
    zia_text = zia_job._owner_id
    zia_job.set_belief(eat_road(), eat_road())
    assert zia_job.get_belief(eat_road()).pick == eat_road()
    sue_texas_userhub = get_texas_userhub()
    sue_texas_userhub.save_job_agenda(zia_job)

    bob_job = get_example_bob_speaker()
    bob_text = bob_job._owner_id
    assert bob_job.get_belief(eat_road()).pick == hungry_road()
    sue_texas_userhub.save_job_agenda(bob_job)

    yao_role = get_example_yao_speaker()
    yao_role.del_belief(eat_road())
    assert yao_role.get_belief(eat_road()) is None
    sue_texas_userhub.save_role_agenda(yao_role)

    new_yao_job1 = create_listen_basis(yao_role)
    assert new_yao_job1.get_belief(eat_road()) is None
    assert new_yao_job1.get_missing_belief_bases().get(eat_road()) is None
    listen_to_intents_role_job(new_yao_job1, sue_texas_userhub)
    print(f"{new_yao_job1.get_missing_belief_bases().keys()=}")
    print(f"{new_yao_job1._oathroot._beliefunits.keys()=}")
    assert new_yao_job1.get_missing_belief_bases().get(eat_road()) != None

    # WHEN
    listen_to_beliefs_role_job(new_yao_job1, sue_texas_userhub)

    # THEN
    assert yao_role.get_belief(eat_road()) is None
    zia_partyunit = new_yao_job1.get_party(zia_text)
    bob_partyunit = new_yao_job1.get_party(bob_text)
    assert zia_partyunit.debtor_weight < bob_partyunit.debtor_weight
    assert bob_job.get_belief(eat_road()).pick == hungry_road()
    assert zia_job.get_belief(eat_road()).pick == eat_road()
    assert new_yao_job1.get_belief(eat_road()).pick == hungry_road()

    # WHEN
    yao_zia_debtor_weight = 15
    yao_bob_debtor_weight = 5
    yao_role.add_partyunit(zia_text, None, yao_zia_debtor_weight)
    yao_role.add_partyunit(bob_text, None, yao_bob_debtor_weight)
    yao_role.set_party_pool(100)
    new_yao_job2 = create_listen_basis(yao_role)
    listen_to_intents_role_job(new_yao_job2, sue_texas_userhub)
    listen_to_beliefs_role_job(new_yao_job2, sue_texas_userhub)

    # THEN
    zia_partyunit = new_yao_job2.get_party(zia_text)
    bob_partyunit = new_yao_job2.get_party(bob_text)
    assert zia_partyunit.debtor_weight > bob_partyunit.debtor_weight
    assert bob_job.get_belief(eat_road()).pick == hungry_road()
    assert zia_job.get_belief(eat_road()).pick == eat_road()
    assert new_yao_job2.get_belief(eat_road()).pick == eat_road()


# def test_listen_to_beliefs_role_job_SetsBelief(env_dir_setup_cleanup):
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
#     sue_speaker.add_oath(oathunit_shop(clean_text), status_road)
#     sue_speaker.add_oath(oathunit_shop(dirty_text), status_road)
#     sue_speaker.add_oath(oathunit_shop(sweep_text, pledge=True), casa_road)
#     sue_speaker.edit_oath_attr(
#         sweep_road, reason_base=status_road, reason_premise=dirty_road
#     )
#     sweep_oath = sue_speaker.get_oath_obj(sweep_road)
#     sweep_oath._assignedunit.set_suffidea(yao_text)

#     sue_texas_userhub = get_texas_userhub()
#     sue_texas_userhub.save_job_agenda(sue_text, sue_speaker.get_json(), True)
#     yao_role = agendaunit_shop(yao_text)
#     yao_role.add_partyunit(yao_text)
#     yao_role.add_partyunit(sue_text)
#     new_yao_job = create_listen_basis(yao_role)
#     print(f"{new_yao_job.get_oath_dict().keys()=}")
#     # assert new_yao_job.get_missing_belief_bases().get(status_road) is None
#     listen_to_intents_role_job(new_yao_job, texas_userhub)
#     print(f"{new_yao_job.get_oath_dict().keys()=}")
#     assert new_yao_job.get_missing_belief_bases().get(status_road) != None

#     # assert new_yao_job.get_missing_belief_bases().keys() == {status_road}
#     # sue_speaker.set_belief(status_road, clean_road, create_missing_oaths=True)

#     # # WHEN
#     # listen_to_beliefs_role_job(yao_role, yao_job, missing_belief_bases)

#     # # THEN
#     # assert len(yao_role.get_missing_belief_bases().keys()) == 0
#     assert 1 == 3


# def test_listen_to_beliefs_role_job_DoesNotOverrideBelief():
#     # GIVEN
#     yao_text = "Yao"
#     yao_role = agendaunit_shop(yao_text)
#     yao_role.add_partyunit(yao_text)
#     yao_role.set_party_pool(20)
#     casa_text = "casa"
#     casa_road = yao_role.make_l1_road(casa_text)
#     status_text = "status"
#     status_road = yao_role.make_road(casa_road, status_text)
#     clean_text = "clean"
#     clean_road = yao_role.make_road(status_road, clean_text)
#     dirty_text = "dirty"
#     dirty_road = yao_role.make_road(status_road, dirty_text)
#     sweep_text = "sweep"
#     sweep_road = yao_role.make_road(casa_road, sweep_text)
#     fridge_text = "fridge"
#     fridge_road = yao_role.make_road(casa_road, fridge_text)
#     running_text = "running"
#     running_road = yao_role.make_road(fridge_road, running_text)

#     yao_role.add_oath(oathunit_shop(running_text), fridge_road)
#     yao_role.add_oath(oathunit_shop(clean_text), status_road)
#     yao_role.add_oath(oathunit_shop(dirty_text), status_road)
#     yao_role.add_oath(oathunit_shop(sweep_text, pledge=True), casa_road)
#     yao_role.edit_oath_attr(
#         sweep_road, reason_base=status_road, reason_premise=dirty_road
#     )
#     yao_role.edit_oath_attr(
#         sweep_road, reason_base=fridge_road, reason_premise=running_road
#     )
#     assert len(yao_role.get_missing_belief_bases()) == 2
#     yao_role.set_belief(status_road, dirty_road)
#     assert len(yao_role.get_missing_belief_bases()) == 1
#     assert yao_role.get_belief(status_road).pick == dirty_road

#     # WHEN
#     yao_job = agendaunit_shop(yao_text)
#     yao_job.set_belief(status_road, clean_road, create_missing_oaths=True)
#     yao_job.set_belief(fridge_road, running_road, create_missing_oaths=True)
#     missing_belief_bases = list(yao_role.get_missing_belief_bases().keys())
#     listen_to_beliefs_role_job(yao_role, yao_job, missing_belief_bases)

#     # THEN
#     assert len(yao_role.get_missing_belief_bases()) == 0
#     # did not grab speaker's beliefunit
#     assert yao_role.get_belief(status_road).pick == dirty_road
#     # grabed speaker's beliefunit
#     assert yao_role.get_belief(fridge_road).pick == running_road
