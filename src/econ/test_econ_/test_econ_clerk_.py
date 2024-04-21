from src.agenda.agenda import agendaunit_shop
from src.econ.econ import econunit_shop
from src.econ.clerk import clerkunit_shop
from src.econ.examples.econ_env_kit import (
    get_test_econ_dir,
    get_temp_env_world_id,
    env_dir_setup_cleanup,
    get_test_econ_dir,
)
from os import path as os_path
from pytest import raises as pytest_raises


def test_EconUnit_create_clerkunit_SetsAttrCorrecty(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())
    print(f"create env '{get_temp_env_world_id()}' directories.")
    yao_text = "Yao"
    yao_dir = f"{x_econ.get_clerkunits_dir()}/{yao_text}"
    yao_agenda = agendaunit_shop(yao_text)
    x_econ.save_file_to_guts(yao_agenda)
    print(f"{yao_dir=}")
    assert os_path.exists(yao_dir) == False
    assert x_econ._clerkunits.get(yao_text) is None

    # WHEN
    x_econ.create_clerkunit(clerk_id=yao_text)

    # THEN
    print(f"{yao_dir=}")
    assert x_econ._clerkunits.get(yao_text) != None
    assert os_path.exists(yao_dir)


def test_EconUnit_clerkunit_exists_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())
    x_econ.save_file_to_guts(agendaunit_shop(yao_text))
    assert x_econ.clerkunit_exists(yao_text) == False

    # WHEN
    x_econ.create_clerkunit(clerk_id=yao_text)

    # THEN
    assert x_econ.clerkunit_exists(yao_text)


def test_EconUnit_delete_clerkunit_DeletesCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())
    x_econ.save_file_to_guts(agendaunit_shop(yao_text))
    yao_dir = f"{x_econ.get_clerkunits_dir()}/{yao_text}"
    assert os_path.exists(yao_dir) == False

    x_econ.create_clerkunit(clerk_id=yao_text)
    assert os_path.exists(yao_dir)
    assert x_econ.clerkunit_exists(yao_text)

    # WHEN
    x_econ.delete_clerkunit(yao_text)

    # THEN
    assert os_path.exists(yao_dir)
    assert x_econ.clerkunit_exists(yao_text) == False


def test_EconUnit_get_clerkunit_ReturnsCorrectObj(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())
    x_econ.save_file_to_guts(agendaunit_shop(yao_text))
    x_econ.create_clerkunit(clerk_id=yao_text)
    assert x_econ.clerkunit_exists(yao_text)

    # WHEN
    yao_clerkunit = x_econ.get_clerkunit(yao_text)

    # THEN
    assert yao_clerkunit != None


def test_EconUnit_get_clerkunit_RaisesCorrectError(env_dir_setup_cleanup):
    # GIVEN
    yao_text = "Yao"
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())
    assert x_econ.clerkunit_exists(yao_text) == False

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        x_econ.get_clerkunit(yao_text)
    assert str(excinfo.value) == f"ClerkUnit '{yao_text}' does not exist in memory."


def test_EconUnit_create_clerkunit_ReturnsObj(env_dir_setup_cleanup):
    # GIVEN
    x_econ = econunit_shop(get_temp_env_world_id(), get_test_econ_dir())
    yao_text = "Yao"
    x_econ.save_file_to_guts(agendaunit_shop(yao_text))

    # WHEN
    yao_clerkunit = x_econ.create_clerkunit(clerk_id=yao_text)

    # THEN
    assert yao_clerkunit != None
