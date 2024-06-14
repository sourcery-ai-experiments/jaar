from src.agenda.oath import oathunit_shop
from src.agenda.agenda import agendaunit_shop


def test_agendaAddingOathWithAddinCorrectlyTransformsRangeScenario1():
    # GIVEN
    mia_agenda = agendaunit_shop("Mia", _weight=10)

    l1 = "level1"
    mia_agenda.add_l1_oath(oathunit_shop(l1, _weight=30))
    l1_road = mia_agenda.make_l1_road(l1)

    rx1 = "range_root_example"
    mia_agenda.add_oath(oathunit_shop(rx1, _weight=30), parent_road=l1_road)
    rx1_road = mia_agenda.make_road(l1_road, rx1)
    mia_agenda.edit_oath_attr(road=rx1_road, begin=10, close=25)

    y_oath = mia_agenda.get_oath_obj(rx1_road)
    print(f"Add example child oath to road='{rx1_road}'")

    rcA = "range_child_example"
    mia_agenda.add_oath(oathunit_shop(rcA, _weight=30, _begin=10, _close=25), rx1_road)

    rcA_road = mia_agenda.make_road(rx1_road, rcA)
    x_oath = mia_agenda.get_oath_obj(rcA_road)

    assert x_oath._begin == 10
    assert x_oath._close == 25

    # WHEN
    mia_agenda.edit_oath_attr(road=rcA_road, addin=7)

    # THEN
    assert x_oath._begin == 17
    assert x_oath._close == 32


def test_agendaAddingOathWithAddinCorrectlyTransformsRangeScenario2():
    # GIVEN
    bob_agenda = agendaunit_shop(_owner_id="Bob", _weight=10)

    l1 = "level1"
    bob_agenda.add_l1_oath(oathunit_shop(l1, _weight=30))
    l1_road = bob_agenda.make_l1_road(l1)

    rx1 = "range_root_example"
    bob_agenda.add_oath(oathunit_shop(rx1, _weight=30), parent_road=l1_road)
    rx1_road = bob_agenda.make_road(l1_road, rx1)
    bob_agenda.edit_oath_attr(road=rx1_road, begin=10, close=25)

    y_oath = bob_agenda.get_oath_obj(rx1_road)
    print(f"Add example child oath to road='{rx1_road}'")

    rcA = "range_child_example"
    bob_agenda.add_oath(oathunit_shop(rcA, _weight=30, _begin=10, _close=25), rx1_road)

    rcA_road = bob_agenda.make_road(rx1_road, rcA)
    x_oath = bob_agenda.get_oath_obj(rcA_road)

    assert x_oath._begin == 10
    assert x_oath._close == 25
    assert x_oath._addin is None

    # WHEN
    bob_agenda.edit_oath_attr(road=rcA_road, addin=15, denom=5)

    # THEN
    assert x_oath._begin == 5
    assert x_oath._close == 8
    assert x_oath._addin == 15
    assert x_oath._denom == 5


def test_get_oath_ranged_kids_ReturnsAllChildren():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    noa_agenda.set_time_hreg_oaths(c400_count=7)

    # WHEN
    time_road = noa_agenda.make_l1_road("time")
    tech_road = noa_agenda.make_road(time_road, "tech")
    week_road = noa_agenda.make_road(tech_road, "week")
    ranged_oaths = noa_agenda.get_oath_ranged_kids(oath_road=week_road)

    # # THEN
    assert len(ranged_oaths) == 7


def test_get_oath_ranged_kids_ReturnsSomeChildrenScen1():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    noa_agenda.set_time_hreg_oaths(c400_count=7)

    # WHEN
    time_road = noa_agenda.make_l1_road("time")
    tech_road = noa_agenda.make_road(time_road, "tech")
    week_road = noa_agenda.make_road(tech_road, "week")
    begin_x = 1440
    close_x = 4 * 1440
    ranged_oaths = noa_agenda.get_oath_ranged_kids(week_road, begin_x, close_x)

    # THEN
    # for oath_x in ranged_oaths.values():
    #     print(
    #         f"{begin_x=} {close_x=} {oath_x._label=} {oath_x._begin=} {oath_x._close=} "
    #     )
    assert len(ranged_oaths) == 3


def test_get_oath_ranged_kids_ReturnsSomeChildrenScen2():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    noa_agenda.set_time_hreg_oaths(c400_count=7)

    # WHEN THEN
    time_road = noa_agenda.make_l1_road("time")
    tech_road = noa_agenda.make_road(time_road, "tech")
    week_road = noa_agenda.make_road(tech_road, "week")
    assert len(noa_agenda.get_oath_ranged_kids(week_road, begin=0, close=1440)) == 1
    assert len(noa_agenda.get_oath_ranged_kids(week_road, begin=0, close=2000)) == 2
    assert len(noa_agenda.get_oath_ranged_kids(week_road, begin=0, close=3000)) == 3


def test_get_oath_ranged_kids_ReturnsSomeChildrenScen3():
    # GIVEN
    noa_agenda = agendaunit_shop("Noa")
    noa_agenda.set_time_hreg_oaths(c400_count=7)

    # WHEN THEN
    time_road = noa_agenda.make_l1_road("time")
    tech_road = noa_agenda.make_road(time_road, "tech")
    week_road = noa_agenda.make_road(tech_road, "week")
    assert len(noa_agenda.get_oath_ranged_kids(oath_road=week_road, begin=0)) == 1
    assert len(noa_agenda.get_oath_ranged_kids(oath_road=week_road, begin=1440)) == 1
