from src.economy.actor import actorunit_shop
from src.economy.examples.example_actors import get_contract_assignment_laundry_example1
from src.economy.examples.actor_env_kit import (
    actor_dir_setup_cleanup,
    get_temp_actor_dir,
    get_temp_economy_title,
)


def test_actor_save_contract_to_depot_assignment_link_CorrectlyCreatesAssignmentFile(
    actor_dir_setup_cleanup,
):
    # GIVEN
    america_cx = get_contract_assignment_laundry_example1()
    america_cx.set_economy_title(get_temp_economy_title())
    joachim_text = "Joachim"
    joachim_ux = actorunit_shop(
        joachim_text, get_temp_actor_dir(), get_temp_economy_title()
    )
    joachim_ux.create_core_dir_and_files()
    print(f"{america_cx._idearoot._label=}")
    assert america_cx._idearoot._label == get_temp_economy_title()
    assert america_cx._owner == "America"
    print(f"{america_cx._owner} {america_cx._idearoot._label=}")

    # WHEN
    joachim_ux.set_depot_contract(contract_x=america_cx, depotlink_type="assignment")
    output_cx = joachim_ux._admin.get_remelded_output_contract()

    # THEN
    assert output_cx != None
    output_cx.set_contract_metrics()
    assert len(output_cx._idea_dict.keys()) == 9

    casa_text = "casa"
    casa_road = f"{get_temp_economy_title()},{casa_text}"
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
