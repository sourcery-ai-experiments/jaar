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
    assert x_moveunit.insert_stirs is None
    assert x_moveunit.delete_stirs is None
    assert x_moveunit.update_stirs is None


def test_moveunit_shop_ReturnsCorrectObj():
    # GIVEN
    sue_road = get_sue_personroad()

    # WHEN
    sue_moveunit = moveunit_shop(sue_road)

    # THEN
    assert sue_moveunit.agenda_road == sue_road
    assert sue_moveunit.insert_stirs == {}
    assert sue_moveunit.delete_stirs == {}
    assert sue_moveunit.update_stirs == {}
