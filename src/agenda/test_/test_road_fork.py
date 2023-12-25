from src.agenda.road import (
    get_default_economy_root_label as root_label,
    get_road,
    get_node_delimiter,
)
from src.agenda.fork import (
    ForkUnit,
    forkunit_shop,
    create_forkunit,
    ProngUnit,
    prongunit_shop,
)
from pytest import raises as pytest_raises


def test_ProngUnit_exists():
    # GIVEN
    gas_road = get_road(root_label(), "gas cooking")

    # WHEN
    beef_prong = ProngUnit(road=gas_road)

    # THEN
    assert beef_prong != None
    assert beef_prong.road == gas_road
    assert beef_prong.affect is None
    assert beef_prong.love is None


def test_ProngUnit_set_affect_CorrectSetsAttrs():
    # GIVEN
    gas_road = get_road(root_label(), "gas cooking")
    beef_prong = ProngUnit(road=gas_road)
    assert beef_prong.affect is None

    # WHEN
    beef_affect = -3
    beef_prong.set_affect(beef_affect)

    # THEN
    assert beef_prong.affect == beef_affect


def test_ProngUnit_set_love_CorrectSetsAttrs():
    # GIVEN
    gas_road = get_road(root_label(), "gas cooking")
    beef_prong = ProngUnit(road=gas_road)
    assert beef_prong.love is None

    # WHEN
    beef_love = -7
    beef_prong.set_love(beef_love)

    # THEN
    assert beef_prong.love == beef_love


def test_prongunit_shop_CorrectlyReturnsObj():
    # GIVEN
    gas_road = get_road(root_label(), "gas cooking")

    # WHEN
    cook_prong = prongunit_shop(road=gas_road, affect=7, love=11)

    # THEN
    assert cook_prong.road == gas_road
    assert cook_prong.affect == 7
    assert cook_prong.love == 11


def test_prongunit_shop_Sets_love_NoneIf():
    # GIVEN
    gas_road = get_road(root_label(), "gas cooking")

    # WHEN
    cook_prong = prongunit_shop(road=gas_road, affect=7)

    # THEN
    assert cook_prong.road == gas_road
    assert cook_prong.affect == 7
    assert cook_prong.love == 0


def test_ProngUnit_set_affect_CorrectlyRaisesNoneZeroAffectException():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cheap_road = get_road(cook_road, "cheap food")
    cheap_prong = prongunit_shop(cheap_road, affect=-5)

    # WHEN
    zero_int = 0
    with pytest_raises(Exception) as excinfo:
        cheap_prong.set_affect(x_affect=zero_int)
    assert (
        str(excinfo.value)
        == f"set_affect affect parameter {zero_int} must be Non-zero number"
    )


def test_ForkUnit_exists():
    # GIVEN / WHEN
    x_fork = ForkUnit()

    # THEN
    assert x_fork != None
    assert x_fork.base is None
    assert x_fork.prongs is None
    assert x_fork.delimiter is None


def test_forkunit_shop_CorrectlyReturnsObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")

    # WHEN
    cook_fork = forkunit_shop(base=cook_road)

    # THEN
    assert cook_fork.base == cook_road
    assert cook_fork.prongs == {}
    assert cook_fork.delimiter == get_node_delimiter()


def test_ForkUnit_set_prong_CorrectlySetsAttr():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    assert cook_fork.prongs == {}

    # WHEN
    cheap_road = get_road(cook_road, "cheap food")
    x_affect = -2
    cheap_prong = prongunit_shop(cheap_road, affect=x_affect)
    cook_fork.set_prong(x_prongunit=cheap_prong)

    # THEN
    assert cook_fork.prongs != {}
    assert cook_fork.prongs.get(cheap_road) != None
    assert cook_fork.prongs.get(cheap_road) == cheap_prong


def test_ForkUnit_del_prong_CorrectlySetsAttr():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    cheap_road = get_road(cook_road, "cheap food")
    metal_road = get_road(cook_road, "metal pots")
    cheap_prong = prongunit_shop(cheap_road, affect=-2)
    metal_prong = prongunit_shop(metal_road, affect=3)
    cook_fork.set_prong(cheap_prong)
    cook_fork.set_prong(metal_prong)
    assert len(cook_fork.prongs) == 2
    assert cook_fork.prongs.get(cheap_road) != None
    assert cook_fork.prongs.get(metal_road) != None

    # WHEN
    cook_fork.del_prong(cheap_road)

    # THEN
    assert len(cook_fork.prongs) == 1
    assert cook_fork.prongs.get(cheap_road) is None
    assert cook_fork.prongs.get(metal_road) != None


def test_ForkUnit_get_prongs_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_affect = 3
    farm_prongunit = prongunit_shop(farm_road, farm_affect)
    cook_fork.set_prong(farm_prongunit)
    cheap_road = get_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_fork.set_prong(prongunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_good_prongs = cook_fork.get_prongs(good=True)

    # THEN
    assert x_good_prongs != {}
    assert len(x_good_prongs) == 1
    assert x_good_prongs.get(farm_road) == farm_prongunit


def test_ForkUnit_get_prongs_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_affect = 3
    farm_prongunit = prongunit_shop(farm_road, farm_affect)
    cook_fork.set_prong(farm_prongunit)
    cheap_road = get_road(cook_road, "cheap food")
    cheap_affect = -3
    cheap_prongunit = prongunit_shop(cheap_road, cheap_affect)
    cook_fork.set_prong(cheap_prongunit)

    # WHEN
    x_bad_prongs = cook_fork.get_prongs(bad=True)

    # THEN
    assert x_bad_prongs != {}
    assert len(x_bad_prongs) == 1
    assert x_bad_prongs.get(cheap_road) == cheap_prongunit


def test_ForkUnit_get_1_prong_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_affect = 3
    cook_fork.set_prong(prongunit_shop(farm_road, farm_affect))
    cheap_road = get_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_fork.set_prong(prongunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_prong = cook_fork.get_1_prong(good=True)

    # THEN
    assert x_bad_prong == farm_road


def test_ForkUnit_get_1_prong_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_affect = 3
    cook_fork.set_prong(prongunit_shop(farm_road, farm_affect))
    cheap_road = get_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_fork.set_prong(prongunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_prong = cook_fork.get_1_prong(bad=True)

    # THEN
    assert x_bad_prong == cheap_road


def test_ForkUnit_get_prongs_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_love = 3
    farm_prongunit = prongunit_shop(farm_road, -2, love=farm_love)
    cook_fork.set_prong(farm_prongunit)
    cheap_road = get_road(cook_road, "cheap food")
    cheap_love = -3
    cook_fork.set_prong(prongunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_in_tribe_prongs = cook_fork.get_prongs(in_tribe=True)

    # THEN
    assert x_in_tribe_prongs != {}
    assert len(x_in_tribe_prongs) == 1
    assert x_in_tribe_prongs.get(farm_road) == farm_prongunit


def test_ForkUnit_get_prongs_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_love = 3
    farm_prongunit = prongunit_shop(farm_road, -2, love=farm_love)
    cook_fork.set_prong(farm_prongunit)
    cheap_road = get_road(cook_road, "cheap food")
    cheap_love = -3
    cheap_prongunit = prongunit_shop(cheap_road, -2, love=cheap_love)
    cook_fork.set_prong(cheap_prongunit)

    # WHEN
    x_out_tribe_prongs = cook_fork.get_prongs(out_tribe=True)

    # THEN.
    assert x_out_tribe_prongs != {}
    assert len(x_out_tribe_prongs) == 1
    assert x_out_tribe_prongs.get(cheap_road) == cheap_prongunit


def test_ForkUnit_get_1_prong_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_love = 3
    cook_fork.set_prong(prongunit_shop(farm_road, -2, love=farm_love))
    cheap_road = get_road(cook_road, "cheap food")
    cheap_love = -3
    cook_fork.set_prong(prongunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_prong = cook_fork.get_1_prong(in_tribe=True)

    # THEN
    assert x_out_tribe_prong == farm_road


def test_ForkUnit_get_1_prong_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    farm_road = get_road(cook_road, "farm food")
    farm_love = 3
    cook_fork.set_prong(prongunit_shop(farm_road, -2, love=farm_love))
    cheap_road = get_road(cook_road, "cheap food")
    cheap_love = -3
    cook_fork.set_prong(prongunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_prong = cook_fork.get_1_prong(out_tribe=True)

    # THEN
    assert x_out_tribe_prong == cheap_road


def test_ForkUnit_set_prongs_CorrectlyRaisesForkSubRoadUnitException():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    go_road = "going out"
    go_cheap_road = get_road(go_road, "cheap food")
    go_cheap_prongunit = prongunit_shop(go_cheap_road, affect=-3)

    # WHEN
    x_affect = -2
    with pytest_raises(Exception) as excinfo:
        cook_fork.set_prong(go_cheap_prongunit)
    assert (
        str(excinfo.value)
        == f"ForkUnit cannot set prong '{go_cheap_road}' because base road is '{cook_road}'."
    )


def test_ForkUnit_is_moral_ReturnsCorrectBool():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)

    # WHEN / THEN
    assert len(cook_fork.prongs) == 0
    assert cook_fork.is_moral() == False

    # WHEN / THEN
    cheap_prong = prongunit_shop(get_road(cook_road, "cheap food"), -2)
    cook_fork.set_prong(cheap_prong)
    assert len(cook_fork.prongs) == 1
    assert cook_fork.is_moral() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    farm_prong = prongunit_shop(get_road(cook_road, farm_text), 3)
    cook_fork.set_prong(farm_prong)
    assert len(cook_fork.prongs) == 2
    assert cook_fork.is_moral()

    # WHEN / THEN
    cook_fork.del_prong(get_road(cook_road, farm_text))
    assert len(cook_fork.prongs) == 1
    assert cook_fork.is_moral() == False

    # WHEN / THEN
    plastic_prong = prongunit_shop(get_road(cook_road, "plastic pots"), -5)
    cook_fork.set_prong(plastic_prong)
    assert len(cook_fork.prongs) == 2
    assert cook_fork.is_moral() == False

    # WHEN / THEN
    metal_prong = prongunit_shop(get_road(cook_road, "metal pots"), 7)
    cook_fork.set_prong(metal_prong)
    assert len(cook_fork.prongs) == 3
    assert cook_fork.is_moral()


def test_ForkUnit_is_tribal_ReturnsCorrectBool():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)

    # WHEN / THEN
    assert cook_fork.is_tribal() == False

    # WHEN / THEN
    cheap_road = get_road(cook_road, "cheap food")
    cheap_prong = prongunit_shop(cheap_road, -2, love=77)
    cook_fork.set_prong(cheap_prong)
    assert cook_fork.is_tribal() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    farm_road = get_road(cook_road, farm_text)
    farm_prong = prongunit_shop(farm_road, -2, love=-55)
    cook_fork.set_prong(farm_prong)
    assert cook_fork.is_tribal()

    # WHEN / THEN
    cook_fork.del_prong(farm_road)
    assert len(cook_fork.prongs) == 1
    assert cook_fork.is_tribal() == False

    # WHEN / THEN
    plastic_road = get_road(cook_road, "plastic pots")
    plastic_prong = prongunit_shop(plastic_road, -2, love=99)
    cook_fork.set_prong(plastic_prong)
    assert len(cook_fork.prongs) == 2
    assert cook_fork.is_tribal() == False

    # WHEN / THEN
    metal_road = get_road(cook_road, "metal pots")
    metal_prong = prongunit_shop(metal_road, -2, love=-44)
    cook_fork.set_prong(metal_prong)
    assert len(cook_fork.prongs) == 3
    assert cook_fork.is_tribal()


def test_ForkUnit_is_dialectic_ReturnsCorrectBool_v1():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)

    # WHEN / THEN
    assert cook_fork.is_tribal() == False
    assert cook_fork.is_moral() == False
    assert cook_fork.is_dialectic() == False


def test_ForkUnit_is_dialectic_ReturnsCorrectBool_v2():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    warm_proc_road = get_road(cook_road, "warm processed food")
    cold_proc_road = get_road(cook_road, "cold processed food")
    warm_farm_road = get_road(cook_road, "warm farmed food")
    cold_farm_road = get_road(cook_road, "cold farmed food")
    cook_fork.set_prong(prongunit_shop(warm_proc_road, affect=44, love=-9))
    cook_fork.set_prong(prongunit_shop(cold_proc_road, affect=-5, love=-4))
    cook_fork.set_prong(prongunit_shop(warm_farm_road, affect=33, love=77))
    cook_fork.set_prong(prongunit_shop(cold_farm_road, affect=-7, love=88))
    assert len(cook_fork.prongs) == 4
    assert cook_fork.is_tribal()
    assert cook_fork.is_moral()
    assert cook_fork.is_dialectic()

    # WHEN / THEN
    cook_fork.del_prong(cold_proc_road)
    assert len(cook_fork.prongs) == 3
    assert cook_fork.is_tribal()
    assert cook_fork.is_moral()
    assert cook_fork.is_dialectic() == False


def test_ForkUnit_get_all_roads_ReturnsCorrectObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")
    cook_fork = forkunit_shop(cook_road)
    cheap_text = "cheap food"
    farm_text = "farm fresh"
    plastic_text = "plastic pots"
    metal_text = "metal pots"
    cook_fork.set_prong(prongunit_shop(get_road(cook_road, cheap_text), -2))
    cook_fork.set_prong(prongunit_shop(get_road(cook_road, farm_text), 3))
    cook_fork.set_prong(prongunit_shop(get_road(cook_road, plastic_text), -5))
    cook_fork.set_prong(prongunit_shop(get_road(cook_road, metal_text), 7))
    assert len(cook_fork.prongs) == 4

    # WHEN
    all_roads_dict = cook_fork.get_all_roads()

    # THEN
    assert len(all_roads_dict) == 5
    assert all_roads_dict.get(cook_road) != None
    cheap_road = get_road(cook_road, cheap_text)
    farm_road = get_road(cook_road, farm_text)
    plastic_road = get_road(cook_road, plastic_text)
    metal_road = get_road(cook_road, metal_text)
    assert all_roads_dict.get(cheap_road) != None
    assert all_roads_dict.get(farm_road) != None
    assert all_roads_dict.get(plastic_road) != None
    assert all_roads_dict.get(metal_road) != None
    assert len(cook_fork.prongs) == 4


def test_create_forkunit_CorrectlyReturnsObj():
    # GIVEN
    cook_road = get_road(root_label(), "cooking")

    # WHEN
    farm_text = "farm food"
    cheap_text = "cheap food"
    cook_fork = create_forkunit(base=cook_road, good=farm_text, bad=cheap_text)

    # THEN
    assert cook_fork.base == cook_road
    assert cook_fork.prongs != {}
    farm_road = get_road(cook_road, farm_text)
    cheap_road = get_road(cook_road, cheap_text)
    assert cook_fork.prongs.get(farm_road) == prongunit_shop(farm_road, 1)
    assert cook_fork.prongs.get(cheap_road) == prongunit_shop(cheap_road, -1)
