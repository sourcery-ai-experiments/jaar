from src.economy.clerk import clerkunit_shop
from src.economy.examples.example_clerks import (
    get_agenda_assignment_laundry_example1,
)
from src.economy.examples.clerk_env_kit import (
    clerk_dir_setup_cleanup,
    get_temp_clerkunit_dir,
    get_temp_economy_id,
)


def test_healer_save_agenda_to_depot_assignment_link_CorrectlyCreatesAssignmentFile(
    clerk_dir_setup_cleanup,
):
    # GIVEN
    amos_agenda = get_agenda_assignment_laundry_example1()
    amos_agenda.set_economy_id(get_temp_economy_id())
    cali_text = "Cali"
    cali_ux = clerkunit_shop(cali_text, get_temp_clerkunit_dir(), get_temp_economy_id())
    cali_ux.create_core_dir_and_files()
    print(f"{amos_agenda._idearoot._label=}")
    assert amos_agenda._idearoot._label == get_temp_economy_id()
    assert amos_agenda._healer == "Amos"
    print(f"{amos_agenda._healer} {amos_agenda._idearoot._label=}")

    # WHEN
    cali_ux.set_depot_agenda(x_agenda=amos_agenda, depotlink_type="assignment")
    output_agenda = cali_ux.get_remelded_output_agenda()

    # THEN
    assert output_agenda != None
    output_agenda.set_agenda_metrics()
    assert len(output_agenda._idea_dict.keys()) == 9

    casa_text = "casa"
    casa_road = output_agenda.make_l1_road(casa_text)
    basket_text = "laundry basket status"
    basket_road = output_agenda.make_road(casa_road, basket_text)
    b_full_text = "full"
    b_full_road = output_agenda.make_road(basket_road, b_full_text)
    b_smel_text = "smelly"
    b_smel_road = output_agenda.make_road(basket_road, b_smel_text)
    b_bare_text = "bare"
    b_bare_road = output_agenda.make_road(basket_road, b_bare_text)
    b_fine_text = "fine"
    b_fine_road = output_agenda.make_road(basket_road, b_fine_text)
    b_half_text = "half full"
    b_half_road = output_agenda.make_road(basket_road, b_half_text)
    laundry_task_text = "do_laundry"
    laundry_task_road = output_agenda.make_road(casa_road, laundry_task_text)
    assert output_agenda._idea_dict.get(casa_road) != None
    assert output_agenda._idea_dict.get(basket_road) != None
    assert output_agenda._idea_dict.get(b_full_road) != None
    assert output_agenda._idea_dict.get(b_smel_road) != None
    assert output_agenda._idea_dict.get(b_bare_road) != None
    assert output_agenda._idea_dict.get(b_fine_road) != None
    assert output_agenda._idea_dict.get(b_half_road) != None
    assert output_agenda._idea_dict.get(laundry_task_road) != None

    laundry_do_idea = output_agenda.get_idea_obj(laundry_task_road)
    print(f"{laundry_do_idea.promise=}")
    print(f"{laundry_do_idea._reasonunits.keys()=}")
    print(f"{laundry_do_idea._reasonunits.get(basket_road).premises.keys()=}")
    print(f"{laundry_do_idea._beliefheirs=}")
    print(f"{laundry_do_idea._assignedunit=}")

    assert laundry_do_idea.promise == True
    assert list(laundry_do_idea._reasonunits.keys()) == [basket_road]
    laundry_do_premises = laundry_do_idea._reasonunits.get(basket_road).premises
    assert list(laundry_do_premises.keys()) == [b_full_road, b_smel_road]
    assert list(laundry_do_idea._assignedunit._suffgroups.keys()) == [cali_text]
    assert list(laundry_do_idea._beliefheirs.keys()) == [basket_road]

    assert laundry_do_idea._beliefheirs.get(basket_road).pick == b_full_road

    assert len(output_agenda.get_intent_dict()) == 1
    assert laundry_task_road in output_agenda.get_intent_dict().keys()
