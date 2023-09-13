from src.system.system import SystemUnit
from src.system.examples.system_env_kit import (
    get_temp_env_name,
    env_dir_setup_cleanup,
    get_test_systems_dir,
)
from src.calendar.road import get_global_root_label as root_label
from src.system.examples.example_persons import get_calendar_assignment_laundry_example1


def test_system_ChangingOnePersonsFactChangesAnotherAgenda(env_dir_setup_cleanup):
    sx = SystemUnit(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    # GIVEN
    america_text = "America"
    sx.create_new_personunit(person_name=america_text)
    america_px = sx.sys_get_person_obj(name=america_text)
    america_px.set_isol(get_calendar_assignment_laundry_example1())

    casa_text = "casa"
    casa_road = f"{root_label()},{casa_text}"
    basket_text = "laundry basket status"
    basket_road = f"{casa_road},{basket_text}"
    b_full_text = "full"
    b_full_road = f"{basket_road},{b_full_text}"
    b_bare_text = "bare"
    b_bare_road = f"{basket_road},{b_bare_text}"
    # set basket status to "bare"
    isol_x = america_px.get_isol().set_acptfact(base=basket_road, pick=b_bare_road)
    america_px.set_isol(isol_x)
    # save fact change to public
    america_px._admin.save_refreshed_output_to_public()
    # print(f"{sx.get_public_calendar(america_text)._idearoot._acptfactunits.keys()=}")
    america_output = sx.get_public_calendar(america_text)

    # create assignment for Joachim
    joachim_text = "Joachim"
    sx.create_new_personunit(person_name=joachim_text)
    joachim_px = sx.sys_get_person_obj(name=joachim_text)
    joachim_px.set_depot_calendar(america_output, "assignment")
    old_joachim_cx = sx.get_person_output_calendar(joachim_text)
    # print(f"{old_joachim_cx._members.keys()=}")
    # print(f"{old_joachim_cx._idearoot._acptfactunits.keys()=}")
    basket_acptfact = old_joachim_cx._idearoot._acptfactunits.get(basket_road)
    # print(f"Joachim: {basket_acptfact.base=} {basket_acptfact.pick=}")
    assert len(old_joachim_cx.get_agenda_items()) == 0

    # WHEN
    # set basket status to "full"
    america_px.get_isol().set_acptfact(base=basket_road, pick=b_full_road)
    america_px.set_isol()
    america_px._admin.save_refreshed_output_to_public()

    joachim_px.refresh_depot_calendars()
    new_joachim_cx = joachim_px._admin.get_remelded_output_calendar()

    # new_public_america = sx.get_public_calendar(america_text)
    # a_basket_acptfact = new_public_america._idearoot._acptfactunits.get(basket_road)
    # print(f"America after when {a_basket_acptfact.base=} {a_basket_acptfact.pick=}")

    # THEN
    # print(f"{new_joachim_cx._members.keys()=}")
    # basket_acptfact = new_joachim_cx._idearoot._acptfactunits.get(basket_road)
    # print(f"{basket_acptfact.base=} {basket_acptfact.pick=}")
    # print(f"{len(new_joachim_cx._idearoot._acptfactunits.keys())=}")
    assert len(new_joachim_cx.get_agenda_items()) == 1
    laundry_task_text = "do_laundry"
    laundry_task_road = f"{casa_road},{laundry_task_text}"
    assert new_joachim_cx.get_agenda_items()[0].get_road() == laundry_task_road
