from src.agenda.healer import HealerUnit, healerunit_shop, healerunit_get_from_dict
from src.agenda.group import GroupID


def test_HealerUnit_exists():
    # GIVEN
    run_text = ",runners"
    run_group_ids = {run_text}

    # WHEN
    x_healerunit = HealerUnit(_group_ids=run_group_ids)

    # THEN
    assert x_healerunit
    assert x_healerunit._group_ids == run_group_ids


def test_healerunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    run_text = ",runners"
    run_group_ids = {run_text}

    # WHEN
    x_healerunit = healerunit_shop(_group_ids=run_group_ids)

    # THEN
    assert x_healerunit
    assert x_healerunit._group_ids == run_group_ids


def test_healerunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # GIVEN / WHEN
    x_healerunit = healerunit_shop()

    # THEN
    assert x_healerunit
    assert x_healerunit._group_ids == set()


def test_HealerUnit_get_dict_ReturnsCorrectDictWithSingleGroup_id():
    # GIVEN
    bob_group_id = GroupID("Bob")
    run_group_ids = {bob_group_id}
    assigned_x = healerunit_shop(_group_ids=run_group_ids)

    # WHEN
    obj_dict = assigned_x.get_dict()

    # THEN
    assert obj_dict != None
    run_list = [bob_group_id]
    example_dict = {"healerunit_group_ids": run_list}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_HealerUnit_set_group_id_CorrectlySets_group_ids_v1():
    # GIVEN
    x_healerunit = healerunit_shop()
    assert len(x_healerunit._group_ids) == 0

    # WHEN
    jim_text = "Jim"
    x_healerunit.set_group_id(x_group_id=jim_text)

    # THEN
    assert len(x_healerunit._group_ids) == 1


def test_HealerUnit_del_group_id_CorrectlyDeletes_group_ids_v1():
    # GIVEN
    x_healerunit = healerunit_shop()
    jim_text = "Jim"
    sue_text = "Sue"
    x_healerunit.set_group_id(x_group_id=jim_text)
    x_healerunit.set_group_id(x_group_id=sue_text)
    assert len(x_healerunit._group_ids) == 2

    # WHEN
    x_healerunit.del_group_id(x_group_id=sue_text)

    # THEN
    assert len(x_healerunit._group_ids) == 1


def test_HealerUnit_group_id_exists_ReturnsCorrectObj():
    # GIVEN
    x_healerunit = healerunit_shop()
    jim_text = "Jim"
    sue_text = "Sue"
    assert x_healerunit.group_id_exists(jim_text) == False
    assert x_healerunit.group_id_exists(sue_text) == False

    # WHEN
    x_healerunit.set_group_id(x_group_id=jim_text)

    # THEN
    assert x_healerunit.group_id_exists(jim_text)
    assert x_healerunit.group_id_exists(sue_text) == False


def test_HealerUnit_any_group_id_exists_ReturnsCorrectObj():
    # GIVEN
    x_healerunit = healerunit_shop()
    assert x_healerunit.any_group_id_exists() == False

    # WHEN / THEN
    sue_text = "Sue"
    x_healerunit.set_group_id(x_group_id=sue_text)
    assert x_healerunit.any_group_id_exists()

    # WHEN / THEN
    jim_text = "Jim"
    x_healerunit.set_group_id(x_group_id=jim_text)
    assert x_healerunit.any_group_id_exists()

    # WHEN / THEN
    x_healerunit.del_group_id(x_group_id=jim_text)
    assert x_healerunit.any_group_id_exists()

    # WHEN / THEN
    x_healerunit.del_group_id(x_group_id=sue_text)
    assert x_healerunit.any_group_id_exists() == False


def test_healerunit_get_from_dict_ReturnsCorrectObj():
    # GIVEN
    empty_dict = {}

    # WHEN / THEN
    assert healerunit_get_from_dict(empty_dict) == healerunit_shop()

    # WHEN / THEN
    sue_text = "Sue"
    jim_text = "Jim"
    static_healerunit = healerunit_shop()
    static_healerunit.set_group_id(x_group_id=sue_text)
    static_healerunit.set_group_id(x_group_id=jim_text)

    sue_dict = {"healerunit_group_ids": [sue_text, jim_text]}
    assert healerunit_get_from_dict(sue_dict) == static_healerunit
