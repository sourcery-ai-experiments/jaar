from src.system.system import systemunit_shop
from src.system.examples.system_env_kit import (
    get_temp_env_name,
    env_dir_setup_cleanup,
    get_test_systems_dir,
)
from src.calendar.road import get_global_root_label as root_label
from src.calendar.calendar import CalendarUnit
from src.system.examples.example_authors import get_calendar_assignment_laundry_example1


def test_system_ChangingOneAuthorsFactChangesAnotherAgenda(env_dir_setup_cleanup):
    sx = systemunit_shop(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    # GIVEN
    america_text = "America"
    sx.create_new_authorunit(author_name=america_text)
    america_ux = sx.get_author_obj(name=america_text)
    america_ux.set_isol(get_calendar_assignment_laundry_example1())

    casa_text = "casa"
    casa_road = f"{root_label()},{casa_text}"
    basket_text = "laundry basket status"
    basket_road = f"{casa_road},{basket_text}"
    b_full_text = "full"
    b_full_road = f"{basket_road},{b_full_text}"
    b_bare_text = "bare"
    b_bare_road = f"{basket_road},{b_bare_text}"
    # set basket status to "bare"
    isol_x = america_ux.get_isol().set_acptfact(base=basket_road, pick=b_bare_road)
    america_ux.set_isol(isol_x)
    # save fact change to public
    america_ux._admin.save_refreshed_output_to_public()
    # print(f"{sx.get_public_calendar(america_text)._idearoot._acptfactunits.keys()=}")
    america_output = sx.get_public_calendar(america_text)

    # create assignment for Joachim
    joachim_text = "Joachim"
    sx.create_new_authorunit(author_name=joachim_text)
    joachim_ux = sx.get_author_obj(name=joachim_text)
    joachim_ux.set_depot_calendar(america_output, "assignment")
    old_joachim_cx = sx.get_output_calendar(joachim_text)
    # print(f"{old_joachim_cx._members.keys()=}")
    # print(f"{old_joachim_cx._idearoot._acptfactunits.keys()=}")
    basket_acptfact = old_joachim_cx._idearoot._acptfactunits.get(basket_road)
    # print(f"Joachim: {basket_acptfact.base=} {basket_acptfact.pick=}")
    assert len(old_joachim_cx.get_agenda_items()) == 0

    # WHEN
    # set basket status to "full"
    america_ux.get_isol().set_acptfact(base=basket_road, pick=b_full_road)
    america_ux.set_isol()
    america_ux._admin.save_refreshed_output_to_public()

    joachim_ux.refresh_depot_calendars()
    new_joachim_cx = joachim_ux._admin.get_remelded_output_calendar()

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


def test_system_create_task_CorrectlyCreatesTask(env_dir_setup_cleanup):
    sx = systemunit_shop(name=get_temp_env_name(), systems_dir=get_test_systems_dir())
    sx.create_dirs_if_null(in_memory_bank=True)

    america_text = "America"
    joachim_text = "Joachim"
    casa_text = "casa"
    casa_road = f"{root_label()},{casa_text}"
    do_laundry_text = "do_laundry"
    do_laundry_road = f"{casa_road},{do_laundry_text}"
    req_base_text = "laundry basket status"
    req_base_road = f"{casa_road},{req_base_text}"
    req_pick_full_text = "full"
    req_pick_full_road = f"{req_base_road},{req_pick_full_text}"
    req_pick_smel_text = "smelly"
    req_pick_smel_road = f"{req_base_road},{req_pick_smel_text}"
    req_picks = {req_pick_full_road: -1, req_pick_smel_road: -1}
    req_pick_bare_text = "bare"
    req_pick_bare_road = f"{req_base_road},{req_pick_bare_text}"
    req_pick_fine_text = "fine"
    req_pick_fine_road = f"{req_base_road},{req_pick_fine_text}"
    req_pick_half_text = "half full"
    req_pick_half_road = f"{req_base_road},{req_pick_half_text}"
    req_not_picks = {
        req_pick_bare_road: -1,
        req_pick_fine_road: -1,
        req_pick_half_road: -1,
    }
    for_group_x = {america_text: -1, joachim_text: -1}
    assigned_group_x = {joachim_text: -1}
    sx.create_task(
        from_author=america_text,
        to_group=joachim_text,
        group_members={joachim_text},
        task_road=do_laundry_road,
        required_base=req_base_road,
        required_picks=req_picks,
        required_not_picks=req_not_picks,
        for_groups=for_group_x,
        assigned_group=assigned_group_x,
        create_missing_ideas=True,
    )

    # # WHEN
    # america_author.save_output_calendar_to_public()
    # new_joa_author = sx.get_author_obj(name=joachim_text)
    # new_joa_author.save_output_calendar_to_public()
    # new_joa_dest_c = sx.get_public_calendar(joachim_text)
    # new_joa_agenda = new_joa_dest_c.get_agenda_items()
    # assert len(new_joa_agenda) == 1
    # print(f"{new_joa_agenda[0]._label=}")
    # assert new_joa_agenda[0]._label == task_text
    joachim_cx = sx.get_public_calendar(joachim_text)

    assert len(joachim_cx.get_agenda_items()) == 1
    assert joachim_cx.get_agenda_items()[0].get_road() == do_laundry_road

    # sx.create_new_authorunit(author_name=america_text)
    # america_author = sx.get_author_obj(name=america_text)
    # america_author.save_output_calendar_to_public()
    # assert sx.get_public_calendar(america_text) != None

    # # Create author2

    # sx.create_new_authorunit(author_name=joachim_text)
    # old_joa_author = sx.get_author_obj(name=joachim_text)
    # old_joa_author._set_depotlink(america_cx._ownert, depotlink_type="blind_trust")
    # old_joa_author.save_output_calendar_to_public()
    # old_joa_dest_c = sx.get_public_calendar(joachim_text)
    # old_joa_agenda = old_joa_dest_c.get_agenda_items()
    # # assert len(old_joa_agenda) == 0

    # # # Create author1 task:
    # # #  create joachim member in America calendar
    # america_author._set_depotlink(joachim_text)
