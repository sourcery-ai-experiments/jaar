from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src._prime.topic import (
    TopicUnit,
    topicunit_shop,
    create_topicunit,
    FactUnit,
    factunit_shop,
)
from pytest import raises as pytest_raises


def test_TopicUnit_is_meaningful_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)

    # WHEN / THEN
    assert len(cook_topic.factunits) == 0
    assert cook_topic.is_meaningful() == False

    # WHEN / THEN
    cheap_factunit = factunit_shop(create_road(cook_road, "cheap food"), -2)
    cook_topic.set_factunit(cheap_factunit)
    assert len(cook_topic.factunits) == 1
    assert cook_topic.is_meaningful() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    farm_factunit = factunit_shop(create_road(cook_road, farm_text), 3)
    cook_topic.set_factunit(farm_factunit)
    assert len(cook_topic.factunits) == 2
    assert cook_topic.is_meaningful()

    # WHEN / THEN
    cook_topic.del_factunit(create_road(cook_road, farm_text))
    assert len(cook_topic.factunits) == 1
    assert cook_topic.is_meaningful() == False

    # WHEN / THEN
    plastic_factunit = factunit_shop(create_road(cook_road, "plastic pots"), -5)
    cook_topic.set_factunit(plastic_factunit)
    assert len(cook_topic.factunits) == 2
    assert cook_topic.is_meaningful() == False

    # WHEN / THEN
    metal_factunit = factunit_shop(create_road(cook_road, "metal pots"), 7)
    cook_topic.set_factunit(metal_factunit)
    assert len(cook_topic.factunits) == 3
    assert cook_topic.is_meaningful()


def test_TopicUnit_is_tribal_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)

    # WHEN / THEN
    assert cook_topic.is_tribal() == False

    # WHEN / THEN
    cheap_road = create_road(cook_road, "cheap food")
    cheap_factunit = factunit_shop(cheap_road, -2, love=77)
    cook_topic.set_factunit(cheap_factunit)
    assert cook_topic.is_tribal() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    farm_road = create_road(cook_road, farm_text)
    farm_factunit = factunit_shop(farm_road, -2, love=-55)
    cook_topic.set_factunit(farm_factunit)
    assert cook_topic.is_tribal()

    # WHEN / THEN
    cook_topic.del_factunit(farm_road)
    assert len(cook_topic.factunits) == 1
    assert cook_topic.is_tribal() == False

    # WHEN / THEN
    plastic_road = create_road(cook_road, "plastic pots")
    plastic_factunit = factunit_shop(plastic_road, -2, love=99)
    cook_topic.set_factunit(plastic_factunit)
    assert len(cook_topic.factunits) == 2
    assert cook_topic.is_tribal() == False

    # WHEN / THEN
    metal_road = create_road(cook_road, "metal pots")
    metal_factunit = factunit_shop(metal_road, -2, love=-44)
    cook_topic.set_factunit(metal_factunit)
    assert len(cook_topic.factunits) == 3
    assert cook_topic.is_tribal()


def test_TopicUnit_is_dialectic_ReturnsCorrectBool_v1():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)

    # WHEN / THEN
    assert cook_topic.is_tribal() == False
    assert cook_topic.is_meaningful() == False
    assert cook_topic.is_dialectic() == False


def test_TopicUnit_is_dialectic_ReturnsCorrectBool_v2():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    warm_proc_road = create_road(cook_road, "warm processed food")
    cold_proc_road = create_road(cook_road, "cold processed food")
    warm_farm_road = create_road(cook_road, "warm farmed food")
    cold_farm_road = create_road(cook_road, "cold farmed food")
    cook_topic.set_factunit(factunit_shop(warm_proc_road, affect=44, love=-9))
    cook_topic.set_factunit(factunit_shop(cold_proc_road, affect=-5, love=-4))
    cook_topic.set_factunit(factunit_shop(warm_farm_road, affect=33, love=77))
    cook_topic.set_factunit(factunit_shop(cold_farm_road, affect=-7, love=88))
    assert len(cook_topic.factunits) == 4
    assert cook_topic.is_tribal()
    assert cook_topic.is_meaningful()
    assert cook_topic.is_dialectic()

    # WHEN / THEN
    cook_topic.del_factunit(cold_proc_road)
    assert len(cook_topic.factunits) == 3
    assert cook_topic.is_tribal()
    assert cook_topic.is_meaningful()
    assert cook_topic.is_dialectic() == False


def test_TopicUnit_set_metrics_SetsAttr_calc_is_meaningful_Correctly():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    assert cook_topic._calc_is_meaningful == False

    # WHEN
    cook_topic.set_metrics()
    # THEN
    assert cook_topic._calc_is_meaningful == False

    # GIVEN
    cheap_factunit = factunit_shop(create_road(cook_road, "cheap food"), -2)
    cook_topic.set_factunit(cheap_factunit, set_metrics=False)
    farm_text = "farm fresh"
    farm_factunit = factunit_shop(create_road(cook_road, farm_text), 3)
    cook_topic.set_factunit(farm_factunit, set_metrics=False)
    assert len(cook_topic.factunits) == 2
    assert cook_topic.is_meaningful()
    assert cook_topic._calc_is_meaningful == False

    # WHEN
    cook_topic.set_metrics()
    # THEN
    assert cook_topic._calc_is_meaningful


def test_TopicUnit_set_metrics_SetsAttr_calc_is_tribal_Correctly():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    assert cook_topic.is_tribal() == False
    # WHEN
    cook_topic.set_metrics()
    # THEN
    assert cook_topic.is_tribal() == False

    # WHEN / THEN
    cheap_road = create_road(cook_road, "cheap food")
    cheap_factunit = factunit_shop(cheap_road, -2, love=77)
    cook_topic.set_factunit(cheap_factunit, set_metrics=False)
    farm_text = "farm fresh"
    farm_road = create_road(cook_road, farm_text)
    farm_factunit = factunit_shop(farm_road, -2, love=-55)
    cook_topic.set_factunit(farm_factunit, set_metrics=False)
    assert cook_topic.is_tribal()
    assert cook_topic._calc_is_tribal == False
    # WHEN
    cook_topic.set_metrics()
    # THEN
    assert cook_topic._calc_is_tribal


def test_TopicUnit_set_metrics_SetsAttr_calc_is_dialectic_Correctly():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    warm_proc_road = create_road(cook_road, "warm processed food")
    cold_proc_road = create_road(cook_road, "cold processed food")
    warm_farm_road = create_road(cook_road, "warm farmed food")
    cold_farm_road = create_road(cook_road, "cold farmed food")
    warm_proc_factunit = factunit_shop(warm_proc_road, affect=44, love=-9)
    cold_proc_factunit = factunit_shop(cold_proc_road, affect=-5, love=-4)
    warm_farm_factunit = factunit_shop(warm_farm_road, affect=33, love=77)
    cold_farm_factunit = factunit_shop(cold_farm_road, affect=-7, love=88)
    cook_topic.set_factunit(warm_proc_factunit, set_metrics=False)
    cook_topic.set_factunit(cold_proc_factunit, set_metrics=False)
    cook_topic.set_factunit(warm_farm_factunit, set_metrics=False)
    cook_topic.set_factunit(cold_farm_factunit, set_metrics=False)
    assert len(cook_topic.factunits) == 4
    assert cook_topic.is_tribal()
    assert cook_topic.is_meaningful()
    assert cook_topic.is_dialectic()
    assert cook_topic._calc_is_tribal == False
    assert cook_topic._calc_is_meaningful == False
    assert cook_topic._calc_is_dialectic == False

    # WHEN
    cook_topic.set_metrics()
    # THEN
    assert cook_topic._calc_is_tribal
    assert cook_topic._calc_is_meaningful
    assert cook_topic._calc_is_dialectic

    # GIVEN
    cook_topic.del_factunit(cold_proc_road)
    assert len(cook_topic.factunits) == 3
    assert cook_topic.is_tribal()
    assert cook_topic.is_meaningful()
    assert cook_topic.is_dialectic() == False

    # WHEN
    cook_topic.set_metrics()
    # THEN
    assert cook_topic._calc_is_tribal
    assert cook_topic._calc_is_meaningful
    assert cook_topic._calc_is_dialectic == False

    # WHEN
    cook_topic.set_factunit(factunit_shop(cold_proc_road, affect=-5, love=-4))
    # THEN
    assert cook_topic._calc_is_tribal
    assert cook_topic._calc_is_meaningful
    assert cook_topic._calc_is_dialectic


def test_TopicUnit_set_metrics_SetsFactUnit_ratio_AttrsCorrectly():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)
    warm_proc_road = create_road(cook_road, "warm processed food")
    cold_proc_road = create_road(cook_road, "cold processed food")
    warm_farm_road = create_road(cook_road, "warm farmed food")
    cold_farm_road = create_road(cook_road, "cold farmed food")
    warm_proc_affect = 44
    cold_proc_affect = -5
    warm_farm_affect = 33
    cold_farm_affect = -7
    warm_proc_love = -9
    cold_proc_love = -4
    warm_farm_love = 77
    cold_farm_love = 88
    cook_topic.set_factunit(
        factunit_shop(warm_proc_road, warm_proc_affect, warm_proc_love), False
    )
    cook_topic.set_factunit(
        factunit_shop(cold_proc_road, cold_proc_affect, cold_proc_love), False
    )
    cook_topic.set_factunit(
        factunit_shop(warm_farm_road, warm_farm_affect, warm_farm_love), False
    )
    cook_topic.set_factunit(
        factunit_shop(cold_farm_road, cold_farm_affect, cold_farm_love), False
    )
    warm_proc_factunit = cook_topic.get_factunit(warm_proc_road)
    cold_proc_factunit = cook_topic.get_factunit(cold_proc_road)
    warm_farm_factunit = cook_topic.get_factunit(warm_farm_road)
    cold_farm_factunit = cook_topic.get_factunit(cold_farm_road)

    assert warm_proc_factunit._topic_affect_ratio is None
    assert cold_proc_factunit._topic_affect_ratio is None
    assert warm_farm_factunit._topic_affect_ratio is None
    assert cold_farm_factunit._topic_affect_ratio is None
    assert warm_proc_factunit._topic_love_ratio is None
    assert cold_proc_factunit._topic_love_ratio is None
    assert warm_farm_factunit._topic_love_ratio is None
    assert cold_farm_factunit._topic_love_ratio is None

    # WHEN
    cook_topic.set_metrics()

    # THEN
    good_affect_sum = warm_proc_affect + warm_farm_affect
    bad_affect_sum = cold_proc_affect + cold_farm_affect
    in_tribe_sum = warm_farm_love + cold_farm_love
    out_tribe_sum = warm_proc_love + cold_proc_love

    warm_proc_affect = 44
    cold_proc_affect = -5
    warm_farm_affect = 33
    cold_farm_affect = -7
    warm_proc_love = -9
    cold_proc_love = -4
    warm_farm_love = 77
    cold_farm_love = 88

    assert warm_proc_factunit._topic_affect_ratio == warm_proc_affect / good_affect_sum
    assert cold_proc_factunit._topic_affect_ratio == cold_proc_affect / bad_affect_sum
    assert warm_farm_factunit._topic_affect_ratio == warm_farm_affect / good_affect_sum
    assert cold_farm_factunit._topic_affect_ratio == cold_farm_affect / bad_affect_sum
    assert warm_proc_factunit._topic_love_ratio == warm_proc_love / out_tribe_sum
    assert cold_proc_factunit._topic_love_ratio == cold_proc_love / out_tribe_sum
    assert warm_farm_factunit._topic_love_ratio == warm_farm_love / in_tribe_sum
    assert cold_farm_factunit._topic_love_ratio == cold_farm_love / in_tribe_sum
