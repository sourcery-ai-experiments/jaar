from src._road.road import get_default_econ_root_roadnode as root_label, create_road
from src.world.topic import topicunit_shop, opinionunit_shop


def test_TopicUnit_is_meaningful_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)

    # WHEN / THEN
    assert len(cook_topic.opinionunits) == 0
    assert cook_topic.is_meaningful() == False

    # WHEN / THEN
    cheap_opinionunit = opinionunit_shop(create_road(cook_road, "cheap food"), -2)
    cook_topic.set_opinionunit(cheap_opinionunit)
    assert len(cook_topic.opinionunits) == 1
    assert cook_topic.is_meaningful() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    farm_opinionunit = opinionunit_shop(create_road(cook_road, farm_text), 3)
    cook_topic.set_opinionunit(farm_opinionunit)
    assert len(cook_topic.opinionunits) == 2
    assert cook_topic.is_meaningful()

    # WHEN / THEN
    cook_topic.del_opinionunit(create_road(cook_road, farm_text))
    assert len(cook_topic.opinionunits) == 1
    assert cook_topic.is_meaningful() == False

    # WHEN / THEN
    plastic_opinionunit = opinionunit_shop(create_road(cook_road, "plastic pots"), -5)
    cook_topic.set_opinionunit(plastic_opinionunit)
    assert len(cook_topic.opinionunits) == 2
    assert cook_topic.is_meaningful() == False

    # WHEN / THEN
    metal_opinionunit = opinionunit_shop(create_road(cook_road, "metal pots"), 7)
    cook_topic.set_opinionunit(metal_opinionunit)
    assert len(cook_topic.opinionunits) == 3
    assert cook_topic.is_meaningful()


def test_TopicUnit_is_tribal_ReturnsCorrectBool():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_topic = topicunit_shop(cook_road)

    # WHEN / THEN
    assert cook_topic.is_tribal() == False

    # WHEN / THEN
    cheap_road = create_road(cook_road, "cheap food")
    cheap_opinionunit = opinionunit_shop(cheap_road, -2, love=77)
    cook_topic.set_opinionunit(cheap_opinionunit)
    assert cook_topic.is_tribal() == False

    # WHEN / THEN
    farm_text = "farm fresh"
    farm_road = create_road(cook_road, farm_text)
    farm_opinionunit = opinionunit_shop(farm_road, -2, love=-55)
    cook_topic.set_opinionunit(farm_opinionunit)
    assert cook_topic.is_tribal()

    # WHEN / THEN
    cook_topic.del_opinionunit(farm_road)
    assert len(cook_topic.opinionunits) == 1
    assert cook_topic.is_tribal() == False

    # WHEN / THEN
    plastic_road = create_road(cook_road, "plastic pots")
    plastic_opinionunit = opinionunit_shop(plastic_road, -2, love=99)
    cook_topic.set_opinionunit(plastic_opinionunit)
    assert len(cook_topic.opinionunits) == 2
    assert cook_topic.is_tribal() == False

    # WHEN / THEN
    metal_road = create_road(cook_road, "metal pots")
    metal_opinionunit = opinionunit_shop(metal_road, -2, love=-44)
    cook_topic.set_opinionunit(metal_opinionunit)
    assert len(cook_topic.opinionunits) == 3
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
    cook_topic.set_opinionunit(opinionunit_shop(warm_proc_road, affect=44, love=-9))
    cook_topic.set_opinionunit(opinionunit_shop(cold_proc_road, affect=-5, love=-4))
    cook_topic.set_opinionunit(opinionunit_shop(warm_farm_road, affect=33, love=77))
    cook_topic.set_opinionunit(opinionunit_shop(cold_farm_road, affect=-7, love=88))
    assert len(cook_topic.opinionunits) == 4
    assert cook_topic.is_tribal()
    assert cook_topic.is_meaningful()
    assert cook_topic.is_dialectic()

    # WHEN / THEN
    cook_topic.del_opinionunit(cold_proc_road)
    assert len(cook_topic.opinionunits) == 3
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
    cheap_opinionunit = opinionunit_shop(create_road(cook_road, "cheap food"), -2)
    cook_topic.set_opinionunit(cheap_opinionunit, set_metrics=False)
    farm_text = "farm fresh"
    farm_opinionunit = opinionunit_shop(create_road(cook_road, farm_text), 3)
    cook_topic.set_opinionunit(farm_opinionunit, set_metrics=False)
    assert len(cook_topic.opinionunits) == 2
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
    cheap_opinionunit = opinionunit_shop(cheap_road, -2, love=77)
    cook_topic.set_opinionunit(cheap_opinionunit, set_metrics=False)
    farm_text = "farm fresh"
    farm_road = create_road(cook_road, farm_text)
    farm_opinionunit = opinionunit_shop(farm_road, -2, love=-55)
    cook_topic.set_opinionunit(farm_opinionunit, set_metrics=False)
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
    warm_proc_opinionunit = opinionunit_shop(warm_proc_road, affect=44, love=-9)
    cold_proc_opinionunit = opinionunit_shop(cold_proc_road, affect=-5, love=-4)
    warm_farm_opinionunit = opinionunit_shop(warm_farm_road, affect=33, love=77)
    cold_farm_opinionunit = opinionunit_shop(cold_farm_road, affect=-7, love=88)
    cook_topic.set_opinionunit(warm_proc_opinionunit, set_metrics=False)
    cook_topic.set_opinionunit(cold_proc_opinionunit, set_metrics=False)
    cook_topic.set_opinionunit(warm_farm_opinionunit, set_metrics=False)
    cook_topic.set_opinionunit(cold_farm_opinionunit, set_metrics=False)
    assert len(cook_topic.opinionunits) == 4
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
    cook_topic.del_opinionunit(cold_proc_road)
    assert len(cook_topic.opinionunits) == 3
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
    cook_topic.set_opinionunit(opinionunit_shop(cold_proc_road, affect=-5, love=-4))
    # THEN
    assert cook_topic._calc_is_tribal
    assert cook_topic._calc_is_meaningful
    assert cook_topic._calc_is_dialectic


def test_TopicUnit_set_metrics_SetsOpinionUnit_ratio_AttrsCorrectly():
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
    cook_topic.set_opinionunit(
        opinionunit_shop(warm_proc_road, warm_proc_affect, warm_proc_love),
        set_metrics=False,
    )
    cook_topic.set_opinionunit(
        opinionunit_shop(cold_proc_road, cold_proc_affect, cold_proc_love),
        set_metrics=False,
    )
    cook_topic.set_opinionunit(
        opinionunit_shop(warm_farm_road, warm_farm_affect, warm_farm_love),
        set_metrics=False,
    )
    cook_topic.set_opinionunit(
        opinionunit_shop(cold_farm_road, cold_farm_affect, cold_farm_love),
        set_metrics=False,
    )
    warm_proc_opinionunit = cook_topic.get_opinionunit(warm_proc_road)
    cold_proc_opinionunit = cook_topic.get_opinionunit(cold_proc_road)
    warm_farm_opinionunit = cook_topic.get_opinionunit(warm_farm_road)
    cold_farm_opinionunit = cook_topic.get_opinionunit(cold_farm_road)

    assert warm_proc_opinionunit._topic_affect_ratio is None
    assert cold_proc_opinionunit._topic_affect_ratio is None
    assert warm_farm_opinionunit._topic_affect_ratio is None
    assert cold_farm_opinionunit._topic_affect_ratio is None
    assert warm_proc_opinionunit._topic_love_ratio is None
    assert cold_proc_opinionunit._topic_love_ratio is None
    assert warm_farm_opinionunit._topic_love_ratio is None
    assert cold_farm_opinionunit._topic_love_ratio is None

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

    assert (
        warm_proc_opinionunit._topic_affect_ratio == warm_proc_affect / good_affect_sum
    )
    assert (
        cold_proc_opinionunit._topic_affect_ratio == cold_proc_affect / bad_affect_sum
    )
    assert (
        warm_farm_opinionunit._topic_affect_ratio == warm_farm_affect / good_affect_sum
    )
    assert (
        cold_farm_opinionunit._topic_affect_ratio == cold_farm_affect / bad_affect_sum
    )
    assert warm_proc_opinionunit._topic_love_ratio == warm_proc_love / out_tribe_sum
    assert cold_proc_opinionunit._topic_love_ratio == cold_proc_love / out_tribe_sum
    assert warm_farm_opinionunit._topic_love_ratio == warm_farm_love / in_tribe_sum
    assert cold_farm_opinionunit._topic_love_ratio == cold_farm_love / in_tribe_sum
