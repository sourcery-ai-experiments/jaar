from src._prime.road import get_single_roadnode
from src._prime.meld import get_meld_default
from src.agenda.agenda import agendaunit_shop
from src.world.move import MoveUnit, moveunit_shop
from src.world.examples.example_deals import get_sue_personroad


def test_MoveUnit_exists():
    # GIVEN / WHEN
    x_moveunit = MoveUnit()

    # THEN
    assert x_moveunit.agenda_road is None
    assert x_moveunit.stirs is None


def test_moveunit_shop_ReturnsCorrectObj():
    # GIVEN
    sue_road = get_sue_personroad()

    # WHEN
    sue_moveunit = moveunit_shop(sue_road)

    # THEN
    assert sue_moveunit.agenda_road == sue_road
    assert sue_moveunit.stirs == {}


def test_MoveUnit_get_after_agenda_ReturnsCorrectObj_SimplestScenario():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)

    # WHEN
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
    sue_weight = 55
    before_sue_agendaunit = agendaunit_shop(sue_text, _weight=sue_weight)
    after_sue_agendaunit = sue_moveunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    assert after_sue_agendaunit._weight == sue_weight
    assert after_sue_agendaunit == before_sue_agendaunit


def test_MoveUnit_set_stir_CorrectlySets_AgendaUnit_max_tree_traverse():
    # GIVEN
    crud_text = "crud"
    update_text = "UPDATE"
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    assert sue_moveunit.stirs == {}

    # WHEN
    new1_value = 55
    attr_name = "AgendaUnit._weight"
    sue_moveunit.set_stir(attr_name, update_text, arg1=new1_value)
    # THEN
    assert len(sue_moveunit.stirs) == 1
    stir_dict = sue_moveunit.stirs.get(attr_name)
    assert stir_dict == {crud_text: update_text, attr_name: new1_value}

    # WHEN
    new2_value = 66
    attr_name = "_max_tree_traverse"
    sue_moveunit.set_stir(attr_name, update_text, arg1=new2_value)
    # THEN
    assert len(sue_moveunit.stirs) == 2
    stir_dict = sue_moveunit.stirs.get(attr_name)
    assert stir_dict == {crud_text: update_text, attr_name: new2_value}

    # WHEN
    new3_value = 77
    attr_name = "_party_creditor_pool"
    sue_moveunit.set_stir(attr_name, update_text, arg1=new3_value)
    # THEN
    assert len(sue_moveunit.stirs) == 3
    stir_dict = sue_moveunit.stirs.get(attr_name)
    assert stir_dict == {crud_text: update_text, attr_name: new3_value}

    # WHEN
    new4_value = 88
    attr_name = "_party_debtor_pool"
    sue_moveunit.set_stir(attr_name, update_text, arg1=new4_value)
    # THEN
    assert len(sue_moveunit.stirs) == 4
    stir_dict = sue_moveunit.stirs.get(attr_name)
    assert stir_dict == {crud_text: update_text, attr_name: new4_value}

    # WHEN
    new5_value = "override"
    attr_name = "_meld_strategy"
    sue_moveunit.set_stir(attr_name, update_text, arg1=new5_value)
    # THEN
    assert len(sue_moveunit.stirs) == 5
    stir_dict = sue_moveunit.stirs.get(attr_name)
    assert stir_dict == {crud_text: update_text, attr_name: new5_value}


def test_MoveUnit_get_after_agenda_ReturnsCorrectObj_AgendaUnit_weight():
    # GIVEN
    sue_road = get_sue_personroad()
    sue_moveunit = moveunit_shop(sue_road)
    sue_text = get_single_roadnode("PersonRoad", sue_road, "PersonID")
    sue_weight = 44
    before_sue_agendaunit = agendaunit_shop(sue_text, _weight=sue_weight)
    update_text = "UPDATE"

    new1_value = 55
    attr_name = "AgendaUnit._weight"
    sue_moveunit.set_stir(attr_name, update_text, arg1=new1_value)

    new2_value = 66
    attr_name = "_max_tree_traverse"
    sue_moveunit.set_stir(attr_name, update_text, arg1=new2_value)

    new3_value = 77
    attr_name = "_party_creditor_pool"
    sue_moveunit.set_stir(attr_name, update_text, arg1=new3_value)

    new4_value = 88
    attr_name = "_party_debtor_pool"
    sue_moveunit.set_stir(attr_name, update_text, arg1=new4_value)

    new5_value = "override"
    attr_name = "_meld_strategy"
    sue_moveunit.set_stir(attr_name, update_text, arg1=new5_value)

    # WHEN
    after_sue_agendaunit = sue_moveunit.get_after_agenda(before_sue_agendaunit)

    # THEN
    print(f"{sue_moveunit.stirs=}")
    assert after_sue_agendaunit._weight == new1_value
    assert after_sue_agendaunit._weight != before_sue_agendaunit._weight
    assert after_sue_agendaunit._max_tree_traverse == new2_value
    assert after_sue_agendaunit._party_creditor_pool == new3_value
    assert after_sue_agendaunit._party_debtor_pool == new4_value
    assert after_sue_agendaunit._meld_strategy == new5_value
