# from src.world.examples.examples import (
#     get_farm_wantunit as examples_get_farm_wantunit,
#     get_farm_requestunit as examples_get_farm_requestunit,
# )
from src._prime.road import create_road
from src._prime.deal import dealunit_shop, sectionunit_shop
from src._prime.examples.example_topics import (
    get_cooking_topic,
    get_speedboats_action_topic,
    get_climate_topic,
    get_gasheater_action_topic,
)


def test_DealUnit_set_sectionunit_SetsAttrCorrectly():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    assert farm_dealunit._sectionunits == {}

    # WHEN
    x_int = 7
    farm_dealunit.set_sectionunit(sectionunit_shop(x_int))

    # THEN
    assert len(farm_dealunit._sectionunits) == 1
    assert farm_dealunit._sectionunits.get(x_int) != None
    assert farm_dealunit._sectionunits.get(x_int) == sectionunit_shop(x_int)


def test_DealUnit_get_sectionunit_ReturnsCorrectObj():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    one_text = "1"
    farm_dealunit.set_sectionunit(sectionunit_shop(one_text))

    # WHEN / THEN
    assert farm_dealunit.get_sectionunit(one_text) != None


def test_DealUnit_sectionunit_exists_ReturnsCorrectObj():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    one_text = "1"
    assert farm_dealunit.sectionunit_exists(one_text) == False

    # WHEN
    farm_dealunit.set_sectionunit(sectionunit_shop(one_text))

    # THEN
    assert farm_dealunit.sectionunit_exists(one_text)


def test_DealUnit_del_sectionunit_CorrectlySetsAttr():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    one_text = "1"
    farm_dealunit.set_sectionunit(sectionunit_shop(one_text))
    assert farm_dealunit.sectionunit_exists(one_text)

    # WHEN
    farm_dealunit.del_sectionunit(one_text)

    # THEN
    assert farm_dealunit.sectionunit_exists(one_text) == False


def test_DealUnit_add_sectionunit_SetsAttrCorrectly():
    # GIVEN
    farm_dealunit = dealunit_shop(_author="Bob", _reader="Tim")
    assert farm_dealunit._sectionunits == {}

    # WHEN
    one_sectionunit = farm_dealunit.add_sectionunit()

    # THEN
    assert one_sectionunit.uid == 1
    assert one_sectionunit.get_section_id() == "Section 0001"
    assert len(farm_dealunit._sectionunits) == 1
    assert farm_dealunit.get_sectionunit(one_sectionunit.uid) != None

    # WHEN
    two_sectionunit = farm_dealunit.add_sectionunit()

    # THEN
    assert two_sectionunit.uid == 2
    assert two_sectionunit.get_section_id() == "Section 0002"
    assert len(farm_dealunit._sectionunits) == 2
    assert farm_dealunit.get_sectionunit(two_sectionunit.uid) != None
