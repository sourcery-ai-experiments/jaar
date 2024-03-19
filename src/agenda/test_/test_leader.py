from src.agenda.leader import LeaderUnit, leaderunit_shop, leaderunit_get_from_dict
from src.agenda.group import GroupID, groupunit_shop
from src.agenda.party import partylink_shop
from src.agenda.agenda import agendaunit_shop
from pytest import raises as pytest_raises


def test_LeaderUnit_exists():
    # GIVEN
    run_text = ",runners"
    run_group_ids = {run_text}

    # WHEN
    x_leaderunit = LeaderUnit(_group_ids=run_group_ids)

    # THEN
    assert x_leaderunit
    assert x_leaderunit._group_ids == run_group_ids


def test_leaderunit_shop_ReturnsCorrectWithCorrectAttributes_v1():
    # GIVEN
    run_text = ",runners"
    run_group_ids = {run_text}

    # WHEN
    x_leaderunit = leaderunit_shop(_group_ids=run_group_ids)

    # THEN
    assert x_leaderunit
    assert x_leaderunit._group_ids == run_group_ids


def test_leaderunit_shop_ifEmptyReturnsCorrectWithCorrectAttributes():
    # GIVEN / WHEN
    x_leaderunit = leaderunit_shop()

    # THEN
    assert x_leaderunit
    assert x_leaderunit._group_ids == set()


def test_LeaderUnit_get_dict_ReturnsCorrectDictWithSingleGroup_id():
    # GIVEN
    bob_group_id = GroupID("Bob")
    run_group_ids = {bob_group_id}
    assigned_x = leaderunit_shop(_group_ids=run_group_ids)

    # WHEN
    obj_dict = assigned_x.get_dict()

    # THEN
    assert obj_dict != None
    run_list = [bob_group_id]
    example_dict = {"leaderunit_group_ids": run_list}
    print(f"{example_dict=}")
    assert obj_dict == example_dict


def test_LeaderUnit_set_group_id_CorrectlySets_group_ids_v1():
    # GIVEN
    x_leaderunit = leaderunit_shop()
    assert len(x_leaderunit._group_ids) == 0

    # WHEN
    jim_text = "Jim"
    x_leaderunit.set_group_id(x_group_id=jim_text)

    # THEN
    assert len(x_leaderunit._group_ids) == 1


def test_LeaderUnit_del_group_id_CorrectlyDeletes_group_ids_v1():
    # GIVEN
    x_leaderunit = leaderunit_shop()
    jim_text = "Jim"
    sue_text = "Sue"
    x_leaderunit.set_group_id(x_group_id=jim_text)
    x_leaderunit.set_group_id(x_group_id=sue_text)
    assert len(x_leaderunit._group_ids) == 2

    # WHEN
    x_leaderunit.del_group_id(x_group_id=sue_text)

    # THEN
    assert len(x_leaderunit._group_ids) == 1


def test_LeaderUnit_group_id_exists_ReturnsCorrectObj():
    # GIVEN
    x_leaderunit = leaderunit_shop()
    jim_text = "Jim"
    sue_text = "Sue"
    assert x_leaderunit.group_id_exists(jim_text) == False
    assert x_leaderunit.group_id_exists(sue_text) == False

    # WHEN
    x_leaderunit.set_group_id(x_group_id=jim_text)

    # THEN
    assert x_leaderunit.group_id_exists(jim_text)
    assert x_leaderunit.group_id_exists(sue_text) == False


def test_LeaderUnit_any_group_id_exists_ReturnsCorrectObj():
    # GIVEN
    x_leaderunit = leaderunit_shop()
    assert x_leaderunit.any_group_id_exists() == False

    # WHEN / THEN
    sue_text = "Sue"
    x_leaderunit.set_group_id(x_group_id=sue_text)
    assert x_leaderunit.any_group_id_exists()

    # WHEN / THEN
    jim_text = "Jim"
    x_leaderunit.set_group_id(x_group_id=jim_text)
    assert x_leaderunit.any_group_id_exists()

    # WHEN / THEN
    x_leaderunit.del_group_id(x_group_id=jim_text)
    assert x_leaderunit.any_group_id_exists()

    # WHEN / THEN
    x_leaderunit.del_group_id(x_group_id=sue_text)
    assert x_leaderunit.any_group_id_exists() == False


def test_leaderunit_get_from_dict_ReturnsCorrectObj():
    # GIVEN
    empty_dict = {}

    # WHEN / THEN
    assert leaderunit_get_from_dict(empty_dict) == leaderunit_shop()

    # WHEN / THEN
    sue_text = "Sue"
    jim_text = "Jim"
    static_leaderunit = leaderunit_shop()
    static_leaderunit.set_group_id(x_group_id=sue_text)
    static_leaderunit.set_group_id(x_group_id=jim_text)

    sue_dict = {"leaderunit_group_ids": [sue_text, jim_text]}
    assert leaderunit_get_from_dict(sue_dict) == static_leaderunit
