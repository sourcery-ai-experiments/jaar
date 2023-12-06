from src.agenda.road import get_road
from src.culture.council import councilunit_shop
from src.culture.examples.example_councils import (
    get_agenda_assignment_laundry_example1,
)
from src.culture.examples.council_env_kit import (
    council_dir_setup_cleanup,
    get_temp_councilunit_dir,
    get_temp_culture_qid,
)


def test_healer_save_agenda_to_depot_assignment_link_CorrectlyCreatesAssignmentFile(
    council_dir_setup_cleanup,
):
    # GIVEN
    amer_agenda = get_agenda_assignment_laundry_example1()
    amer_agenda.set_culture_qid(get_temp_culture_qid())
    cali_text = "Cali"
    cali_ux = councilunit_shop(
        cali_text, get_temp_councilunit_dir(), get_temp_culture_qid()
    )
    cali_ux.create_core_dir_and_files()
    print(f"{amer_agenda._idearoot._label=}")
    assert amer_agenda._idearoot._label == get_temp_culture_qid()
    assert amer_agenda._healer == "Amer"
    print(f"{amer_agenda._healer} {amer_agenda._idearoot._label=}")

    # WHEN
    cali_ux.set_depot_agenda(x_agenda=amer_agenda, depotlink_type="assignment")
    output_agenda = cali_ux._admin.get_remelded_output_agenda()

    # THEN
    assert output_agenda != None
    output_agenda.set_agenda_metrics()
    assert len(output_agenda._idea_dict.keys()) == 9

    casa_text = "casa"
    casa_road = get_road(get_temp_culture_qid(), casa_text)
    basket_text = "laundry basket status"
    basket_road = get_road(casa_road, basket_text)
    b_full_text = "full"
    b_full_road = get_road(basket_road, b_full_text)
    b_smel_text = "smelly"
    b_smel_road = get_road(basket_road, b_smel_text)
    b_bare_text = "bare"
    b_bare_road = get_road(basket_road, b_bare_text)
    b_fine_text = "fine"
    b_fine_road = get_road(basket_road, b_fine_text)
    b_half_text = "half full"
    b_half_road = get_road(basket_road, b_half_text)
    laundry_task_text = "do_laundry"
    laundry_task_road = get_road(casa_road, laundry_task_text)
    assert output_agenda._idea_dict.get(casa_road) != None
    assert output_agenda._idea_dict.get(basket_road) != None
    assert output_agenda._idea_dict.get(b_full_road) != None
    assert output_agenda._idea_dict.get(b_smel_road) != None
    assert output_agenda._idea_dict.get(b_bare_road) != None
    assert output_agenda._idea_dict.get(b_fine_road) != None
    assert output_agenda._idea_dict.get(b_half_road) != None
    assert output_agenda._idea_dict.get(laundry_task_road) != None

    laundry_do_idea = output_agenda.get_idea_kid(laundry_task_road)
    print(f"{laundry_do_idea.promise=}")
    print(f"{laundry_do_idea._requiredunits.keys()=}")
    print(f"{laundry_do_idea._requiredunits.get(basket_road).sufffacts.keys()=}")
    print(f"{laundry_do_idea._acptfactheirs=}")
    print(f"{laundry_do_idea._assignedunit=}")

    assert laundry_do_idea.promise == True
    assert list(laundry_do_idea._requiredunits.keys()) == [basket_road]
    laundry_do_sufffacts = laundry_do_idea._requiredunits.get(basket_road).sufffacts
    assert list(laundry_do_sufffacts.keys()) == [b_full_road, b_smel_road]
    assert list(laundry_do_idea._assignedunit._suffgroups.keys()) == [cali_text]
    assert list(laundry_do_idea._acptfactheirs.keys()) == [basket_road]

    assert laundry_do_idea._acptfactheirs.get(basket_road).pick == b_full_road

    assert len(output_agenda.get_intent_items()) == 1
    assert output_agenda.get_intent_items()[0]._label == "do_laundry"
