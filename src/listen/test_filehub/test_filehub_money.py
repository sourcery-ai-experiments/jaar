from src.agenda.healer import healerhold_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.graphic import display_ideatree
from src.listen.filehub import filehub_shop
from src.listen.examples.listen_env import (
    env_dir_setup_cleanup,
    get_listen_temp_env_dir as env_dir,
)
from pytest import raises as pytest_raises
from os.path import exists as os_path_exists


def test_FileHub_get_econ_roads_RaisesErrorWhen__econs_justified_IsFalse(
    env_dir_setup_cleanup,
):

    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), None, sue_text, None)
    sue_filehub.save_duty_agenda(sue_filehub.default_duty_agenda())
    sue_duty_agenda = sue_filehub.get_duty_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_duty_agenda.add_idea(ideaunit_shop(dallas_text), texas_road)
    sue_duty_agenda.edit_idea_attr(texas_road, healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.edit_idea_attr(dallas_road, healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.calc_agenda_metrics()
    assert sue_duty_agenda._econs_justified is False
    sue_filehub.save_duty_agenda(sue_duty_agenda)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_filehub.get_econ_roads()
    assert (
        str(excinfo.value)
        == f"Cannot set '{sue_text}' duty agenda moneyunits because 'AgendaUnit._econs_justified' is False."
    )


def test_FileHub_get_econ_roads_RaisesErrorWhen__econs_buildable_IsFalse(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), None, sue_text, None)
    sue_filehub.save_duty_agenda(sue_filehub.default_duty_agenda())
    sue_duty_agenda = sue_filehub.get_duty_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Tex/as"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    sue_duty_agenda.edit_idea_attr(texas_road, healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.calc_agenda_metrics()
    assert sue_duty_agenda._econs_justified
    assert sue_duty_agenda._econs_buildable is False
    sue_filehub.save_duty_agenda(sue_duty_agenda)

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sue_filehub.get_econ_roads()
    assert (
        str(excinfo.value)
        == f"Cannot set '{sue_text}' duty agenda moneyunits because 'AgendaUnit._econs_buildable' is False."
    )


def test_FileHub_get_econ_roads_CreatesMoneyUnits(env_dir_setup_cleanup):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), None, sue_text, None)
    sue_filehub.save_duty_agenda(sue_filehub.default_duty_agenda())
    sue_duty_agenda = sue_filehub.get_duty_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    elpaso_text = "el paso"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    elpaso_road = sue_duty_agenda.make_road(texas_road, elpaso_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(dallas_idea, texas_road)
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    sue_duty_agenda.calc_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    sue_filehub.save_duty_agenda(sue_duty_agenda)

    # WHEN
    sue_econ_roads = sue_filehub.get_econ_roads()

    # THEN
    assert len(sue_econ_roads) == 2
    assert dallas_road in sue_econ_roads
    assert elpaso_road in sue_econ_roads


def test_FileHub_save_all_duty_roles_CorrectlySetsroles(
    env_dir_setup_cleanup,
):
    # GIVEN
    sue_text = "Sue"
    sue_filehub = filehub_shop(env_dir(), None, sue_text, None)
    sue_filehub.save_duty_agenda(sue_filehub.default_duty_agenda())
    sue_duty_agenda = sue_filehub.get_duty_agenda()
    sue_duty_agenda.add_partyunit(sue_text)
    bob_text = "Bob"
    sue_duty_agenda.add_partyunit(bob_text)
    texas_text = "Texas"
    texas_road = sue_duty_agenda.make_l1_road(texas_text)
    sue_duty_agenda.add_l1_idea(ideaunit_shop(texas_text, _problem_bool=True))
    dallas_text = "dallas"
    dallas_road = sue_duty_agenda.make_road(texas_road, dallas_text)
    dallas_idea = ideaunit_shop(dallas_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(dallas_idea, texas_road)
    elpaso_text = "el paso"
    elpaso_road = sue_duty_agenda.make_road(texas_road, elpaso_text)
    elpaso_idea = ideaunit_shop(elpaso_text, _healerhold=healerhold_shop({sue_text}))
    sue_duty_agenda.add_idea(elpaso_idea, texas_road)
    # sue_duty_agenda.calc_agenda_metrics()
    # display_ideatree(sue_duty_agenda, mode="Econ").show()
    sue_filehub.save_duty_agenda(sue_duty_agenda)
    sue_dallas_filehub = filehub_shop(env_dir(), None, sue_text, dallas_road)
    sue_elpaso_filehub = filehub_shop(env_dir(), None, sue_text, elpaso_road)
    assert os_path_exists(sue_dallas_filehub.role_path(sue_text)) is False
    assert os_path_exists(sue_elpaso_filehub.role_path(sue_text)) is False
    assert sue_filehub.econ_road is None

    # WHEN
    sue_filehub.save_all_duty_roles()

    # THEN
    assert os_path_exists(sue_dallas_filehub.role_path(sue_text))
    assert os_path_exists(sue_elpaso_filehub.role_path(sue_text))
    assert sue_filehub.econ_road is None
