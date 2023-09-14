from src.system.person import personunit_shop
from src.system.examples.example_persons import get_calendar_assignment_laundry_example1
from src.system.examples.person_env_kit import (
    person_dir_setup_cleanup,
    get_temp_person_dir,
)
from src.calendar.road import get_global_root_label as root_label


def test_person_save_calendar_to_depot_assignment_link_CorrectlyCreatesAssignmentFile(
    person_dir_setup_cleanup,
):
    # GIVEN
    america_cx = get_calendar_assignment_laundry_example1()
    joachim_text = "Joachim"
    joachim_px = personunit_shop(joachim_text, get_temp_person_dir())
    joachim_px.create_core_dir_and_files()

    # WHEN
    joachim_px.set_depot_calendar(calendar_x=america_cx, depotlink_type="assignment")
    output_cx = joachim_px._admin.get_remelded_output_calendar()

    # THEN
    assert output_cx != None
    output_cx.set_calendar_metrics()
    assert len(output_cx._idea_dict.keys()) == 9

    casa_text = "casa"
    casa_road = f"{root_label()},{casa_text}"
    basket_text = "laundry basket status"
    basket_road = f"{casa_road},{basket_text}"
    b_full_text = "full"
    b_full_road = f"{basket_road},{b_full_text}"
    b_smel_text = "smelly"
    b_smel_road = f"{basket_road},{b_smel_text}"
    b_bare_text = "bare"
    b_bare_road = f"{basket_road},{b_bare_text}"
    b_fine_text = "fine"
    b_fine_road = f"{basket_road},{b_fine_text}"
    b_half_text = "half full"
    b_half_road = f"{basket_road},{b_half_text}"
    laundry_task_text = "do_laundry"
    laundry_task_road = f"{casa_road},{laundry_task_text}"
    assert output_cx._idea_dict.get(casa_road) != None
    assert output_cx._idea_dict.get(basket_road) != None
    assert output_cx._idea_dict.get(b_full_road) != None
    assert output_cx._idea_dict.get(b_smel_road) != None
    assert output_cx._idea_dict.get(b_bare_road) != None
    assert output_cx._idea_dict.get(b_fine_road) != None
    assert output_cx._idea_dict.get(b_half_road) != None
    assert output_cx._idea_dict.get(laundry_task_road) != None

    laundry_do_idea = output_cx.get_idea_kid(laundry_task_road)
    print(f"{laundry_do_idea.promise=}")
    print(f"{laundry_do_idea._requiredunits.keys()=}")
    print(f"{laundry_do_idea._requiredunits.get(basket_road).sufffacts.keys()=}")
    print(f"{laundry_do_idea._acptfactheirs=}")
    print(f"{laundry_do_idea._assignedunit=}")

    assert laundry_do_idea.promise == True
    assert list(laundry_do_idea._requiredunits.keys()) == [basket_road]
    laundry_do_sufffacts = laundry_do_idea._requiredunits.get(basket_road).sufffacts
    assert list(laundry_do_sufffacts.keys()) == [b_full_road, b_smel_road]
    assert list(laundry_do_idea._assignedunit._suffgroups.keys()) == [joachim_text]
    assert list(laundry_do_idea._acptfactheirs.keys()) == [basket_road]

    assert laundry_do_idea._acptfactheirs.get(basket_road).pick == b_full_road

    assert len(output_cx.get_agenda_items()) == 1
    assert output_cx.get_agenda_items()[0]._label == "do_laundry"
