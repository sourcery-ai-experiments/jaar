from src._prime.road import (
    get_default_economy_root_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from src._prime.issue import (
    IssueUnit,
    issueunit_shop,
    create_issueunit,
    factunit_shop,
)
from pytest import raises as pytest_raises


def test_IssueUnit_exists():
    # GIVEN / WHEN
    x_issue = IssueUnit()

    # THEN
    assert x_issue != None
    assert x_issue.base is None
    assert x_issue.action is None
    assert x_issue.factunits is None
    assert x_issue.delimiter is None
    assert x_issue.actors is None
    assert x_issue._calc_is_meaningful is None
    assert x_issue._calc_is_tribal is None
    assert x_issue._calc_is_dialectic is None


def test_issueunit_shop_CorrectlyReturnsObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")

    # WHEN
    cook_issue = issueunit_shop(base=cook_road)

    # THEN
    assert cook_issue.base == cook_road
    assert cook_issue.action == False
    assert cook_issue.factunits == {}
    assert cook_issue.delimiter == default_road_delimiter_if_none()
    assert cook_issue.actors == {}
    assert cook_issue._calc_is_meaningful == False
    assert cook_issue._calc_is_tribal == False
    assert cook_issue._calc_is_dialectic == False


def test_IssueUnit_set_action_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    assert cook_issue.action == False

    # WHEN / THEN
    cook_issue.set_action(True)
    assert cook_issue.action

    # WHEN / THEN
    cook_issue.set_action(False)
    assert cook_issue.action == False


def test_IssueUnit_set_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    assert cook_issue.actors == {}

    # WHEN
    bob_text = "Bob"
    cook_issue.set_actor(x_actor=bob_text)

    # THEN
    assert cook_issue.actors != {}
    assert cook_issue.actors.get(bob_text) != None
    assert cook_issue.actors.get(bob_text) == bob_text


def test_IssueUnit_del_actor_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    cook_issue.set_actor(bob_text)
    cook_issue.set_actor(yao_text)
    assert len(cook_issue.actors) == 2
    assert cook_issue.actors.get(bob_text) != None
    assert cook_issue.actors.get(yao_text) != None

    # WHEN
    cook_issue.del_actor(bob_text)

    # THEN
    assert len(cook_issue.actors) == 1
    assert cook_issue.actors.get(bob_text) is None
    assert cook_issue.actors.get(yao_text) != None


def test_IssueUnit_get_actor_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    cook_issue.set_actor(bob_text)
    cook_issue.set_actor(yao_text)

    # WHEN
    bob_actor = cook_issue.get_actor(bob_text)

    # THEN
    assert bob_actor != None
    assert bob_actor == bob_text


def test_IssueUnit_actor_exists_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    bob_text = "Bob"
    yao_text = "Yao"
    assert cook_issue.actor_exists(bob_text) == False
    assert cook_issue.actor_exists(yao_text) == False

    # WHEN / THEN
    cook_issue.set_actor(bob_text)
    cook_issue.set_actor(yao_text)
    assert cook_issue.actor_exists(bob_text)
    assert cook_issue.actor_exists(yao_text)

    # WHEN / THEN
    cook_issue.del_actor(yao_text)
    assert cook_issue.actor_exists(bob_text)
    assert cook_issue.actor_exists(yao_text) == False


def test_IssueUnit_set_factunit_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    assert cook_issue.factunits == {}

    # WHEN
    cheap_road = create_road(cook_road, "cheap food")
    x_affect = -2
    cheap_factunit = factunit_shop(cheap_road, affect=x_affect)
    cook_issue.set_factunit(x_factunit=cheap_factunit)

    # THEN
    assert cook_issue.factunits != {}
    assert cook_issue.factunits.get(cheap_road) != None
    assert cook_issue.factunits.get(cheap_road) == cheap_factunit


def test_IssueUnit_del_factunit_CorrectlySetsAttr():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    cheap_road = create_road(cook_road, "cheap food")
    metal_road = create_road(cook_road, "metal pots")
    cheap_factunit = factunit_shop(cheap_road, affect=-2)
    metal_factunit = factunit_shop(metal_road, affect=3)
    cook_issue.set_factunit(cheap_factunit)
    cook_issue.set_factunit(metal_factunit)
    assert len(cook_issue.factunits) == 2
    assert cook_issue.factunits.get(cheap_road) != None
    assert cook_issue.factunits.get(metal_road) != None

    # WHEN
    cook_issue.del_factunit(cheap_road)

    # THEN
    assert len(cook_issue.factunits) == 1
    assert cook_issue.factunits.get(cheap_road) is None
    assert cook_issue.factunits.get(metal_road) != None


def test_IssueUnit_get_factunits_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    farm_factunit = factunit_shop(farm_road, farm_affect)
    cook_issue.set_factunit(farm_factunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_issue.set_factunit(factunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_good_factunits = cook_issue.get_factunits(good=True)

    # THEN
    assert x_good_factunits != {}
    assert len(x_good_factunits) == 1
    assert x_good_factunits.get(farm_road) == farm_factunit


def test_IssueUnit_get_factunits_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    farm_factunit = factunit_shop(farm_road, farm_affect)
    cook_issue.set_factunit(farm_factunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cheap_factunit = factunit_shop(cheap_road, cheap_affect)
    cook_issue.set_factunit(cheap_factunit)

    # WHEN
    x_bad_factunits = cook_issue.get_factunits(bad=True)

    # THEN
    assert x_bad_factunits != {}
    assert len(x_bad_factunits) == 1
    assert x_bad_factunits.get(cheap_road) == cheap_factunit


def test_IssueUnit_get_1_factunit_ReturnsCorrectObj_good():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_issue.set_factunit(factunit_shop(farm_road, farm_affect))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_issue.set_factunit(factunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_factunit = cook_issue.get_1_factunit(good=True)

    # THEN
    assert x_bad_factunit == farm_road


def test_IssueUnit_get_1_factunit_ReturnsCorrectObj_bad():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_affect = 3
    cook_issue.set_factunit(factunit_shop(farm_road, farm_affect))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_affect = -3
    cook_issue.set_factunit(factunit_shop(cheap_road, cheap_affect))

    # WHEN
    x_bad_factunit = cook_issue.get_1_factunit(bad=True)

    # THEN
    assert x_bad_factunit == cheap_road


def test_IssueUnit_get_factunits_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    farm_factunit = factunit_shop(farm_road, -2, love=farm_love)
    cook_issue.set_factunit(farm_factunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_issue.set_factunit(factunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_in_tribe_factunits = cook_issue.get_factunits(in_tribe=True)

    # THEN
    assert x_in_tribe_factunits != {}
    assert len(x_in_tribe_factunits) == 1
    assert x_in_tribe_factunits.get(farm_road) == farm_factunit


def test_IssueUnit_get_factunits_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    farm_factunit = factunit_shop(farm_road, -2, love=farm_love)
    cook_issue.set_factunit(farm_factunit)
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cheap_factunit = factunit_shop(cheap_road, -2, love=cheap_love)
    cook_issue.set_factunit(cheap_factunit)

    # WHEN
    x_out_tribe_factunits = cook_issue.get_factunits(out_tribe=True)

    # THEN.
    assert x_out_tribe_factunits != {}
    assert len(x_out_tribe_factunits) == 1
    assert x_out_tribe_factunits.get(cheap_road) == cheap_factunit


def test_IssueUnit_get_1_factunit_ReturnsCorrectObj_in_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    cook_issue.set_factunit(factunit_shop(farm_road, -2, love=farm_love))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_issue.set_factunit(factunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_factunit = cook_issue.get_1_factunit(in_tribe=True)

    # THEN
    assert x_out_tribe_factunit == farm_road


def test_IssueUnit_get_1_factunit_ReturnsCorrectObj_out_tribe():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    farm_road = create_road(cook_road, "farm food")
    farm_love = 3
    cook_issue.set_factunit(factunit_shop(farm_road, -2, love=farm_love))
    cheap_road = create_road(cook_road, "cheap food")
    cheap_love = -3
    cook_issue.set_factunit(factunit_shop(cheap_road, -2, love=cheap_love))

    # WHEN
    x_out_tribe_factunit = cook_issue.get_1_factunit(out_tribe=True)

    # THEN
    assert x_out_tribe_factunit == cheap_road


def test_IssueUnit_set_factunits_CorrectlyRaisesIssueSubRoadUnitException():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    go_road = "going out"
    go_cheap_road = create_road(go_road, "cheap food")
    go_cheap_factunit = factunit_shop(go_cheap_road, affect=-3)

    # WHEN
    x_affect = -2
    with pytest_raises(Exception) as excinfo:
        cook_issue.set_factunit(go_cheap_factunit)
    assert (
        str(excinfo.value)
        == f"IssueUnit cannot set factunit '{go_cheap_road}' because base road is '{cook_road}'."
    )


def test_IssueUnit_get_all_roads_ReturnsCorrectObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")
    cook_issue = issueunit_shop(cook_road)
    cheap_text = "cheap food"
    farm_text = "farm fresh"
    plastic_text = "plastic pots"
    metal_text = "metal pots"
    cook_issue.set_factunit(factunit_shop(create_road(cook_road, cheap_text), -2))
    cook_issue.set_factunit(factunit_shop(create_road(cook_road, farm_text), 3))
    cook_issue.set_factunit(factunit_shop(create_road(cook_road, plastic_text), -5))
    cook_issue.set_factunit(factunit_shop(create_road(cook_road, metal_text), 7))
    assert len(cook_issue.factunits) == 4

    # WHEN
    all_roads_dict = cook_issue.get_all_roads()

    # THEN
    assert len(all_roads_dict) == 5
    assert all_roads_dict.get(cook_road) != None
    cheap_road = create_road(cook_road, cheap_text)
    farm_road = create_road(cook_road, farm_text)
    plastic_road = create_road(cook_road, plastic_text)
    metal_road = create_road(cook_road, metal_text)
    assert all_roads_dict.get(cheap_road) != None
    assert all_roads_dict.get(farm_road) != None
    assert all_roads_dict.get(plastic_road) != None
    assert all_roads_dict.get(metal_road) != None
    assert len(cook_issue.factunits) == 4


def test_create_issueunit_CorrectlyReturnsObj():
    # GIVEN
    cook_road = create_road(root_label(), "cooking")

    # WHEN
    farm_text = "farm food"
    cheap_text = "cheap food"
    cook_issue = create_issueunit(base=cook_road, good=farm_text, bad=cheap_text)

    # THEN
    assert cook_issue.base == cook_road
    assert cook_issue.factunits != {}
    farm_road = create_road(cook_road, farm_text)
    cheap_road = create_road(cook_road, cheap_text)
    assert cook_issue.factunits.get(farm_road) == factunit_shop(farm_road, 1)
    assert cook_issue.factunits.get(cheap_road) == factunit_shop(cheap_road, -1)
