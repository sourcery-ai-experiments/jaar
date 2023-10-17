from src.oath.required_idea import (
    RequiredCore,
    RequiredHeir,
    RequiredUnit,
    acptfactheir_shop,
    sufffactunit_shop,
    Road,
)
from src.oath.road import get_default_cure_root_label as root_label
from pytest import raises as pytest_raises


def test_RequiredCore_attributesExist():
    ced_day = "casa,weekday"
    sufffact_x = sufffactunit_shop(need="casa,weekday,wednesday")
    sufffacts = {sufffact_x.need: sufffact_x}
    required = RequiredCore(
        base=ced_day, sufffacts=sufffacts, suff_idea_active_status=False
    )
    assert required.base == ced_day
    assert required.sufffacts == sufffacts
    assert required.suff_idea_active_status == False


def test_RequiredHeir_clear_works():
    email_road = f"{root_label()},work,check email"
    sufffact_x = sufffactunit_shop(need=email_road)
    sufffacts = {sufffact_x.need: sufffact_x}
    base = f"{root_label()},work"
    required = RequiredHeir(base=base, sufffacts=sufffacts)
    assert required._status is None
    required._status = True
    assert required._status
    required.clear_status()
    assert required._status is None
    assert required._curr_idea_active_status is None


def test_RequiredHeir_set_status_CorrectlySetsStatus():
    sufffact_x = sufffactunit_shop(need="casa,weekday,wednesday")
    sufffacts = {sufffact_x.need: sufffact_x}
    required = RequiredHeir(base="casa,weekday", sufffacts=sufffacts)
    x_acptfact = acptfactheir_shop(
        base="casa,weekday", pick="casa,weekday,wednesday,noon"
    )
    x_acptfacts = {x_acptfact.base: x_acptfact}
    assert required._status is None
    required.set_status(acptfacts=x_acptfacts)
    assert required._status == True

    sufffactW = sufffactunit_shop(need="casa,weekday,wednesday")
    sufffactR = sufffactunit_shop(need="casa,weekday,thursday")
    sufffacts = {sufffactW.need: sufffactW, sufffactR.need: sufffactR}
    required = RequiredHeir(base="casa,weekday", sufffacts=sufffacts)
    x_acptfact = acptfactheir_shop(
        base="casa,weekday", pick="casa,weekday,wednesday,noon"
    )
    x_acptfacts = {x_acptfact.base: x_acptfact}
    assert required._status is None
    required.set_status(acptfacts=x_acptfacts)
    assert required._status == True

    sufffactW = sufffactunit_shop(need="casa,weekday,wednesday")
    sufffactR = sufffactunit_shop(need="casa,weekday,thursday")
    sufffacts = {sufffactW.need: sufffactW, sufffactR.need: sufffactR}
    required = RequiredHeir(base="casa,weekday", sufffacts=sufffacts)
    x_acptfact = acptfactheir_shop(base="casa,weekday", pick="casa,weekday,friday")
    x_acptfacts = {x_acptfact.base: x_acptfact}
    assert required._status is None
    required.set_status(acptfacts=x_acptfacts)
    assert required._status == False


def test_RequiredHeir_set_status_EmptyAcptFactCorrectlySetsStatus():
    sufffact_x = sufffactunit_shop(need="casa,weekday,wednesday")
    sufffacts = {sufffact_x.need: sufffact_x}
    required = RequiredHeir(base="casa,weekday", sufffacts=sufffacts)
    assert required._status is None
    required.set_status(acptfacts=None)
    assert required._status == False


def test_RequiredHeir_set_curr_idea_active_status_Correctly():
    # GIVEN
    ced_day = "casa,ced_day"
    required = RequiredHeir(base=ced_day, sufffacts=None)
    assert required._curr_idea_active_status is None

    # WHEN
    required.set_curr_idea_active_status(bool_x=True)

    # THEN
    assert required._curr_idea_active_status


def test_RequiredHeir_set_status_AgendaTrueCorrectlySetsStatusTrue():
    # GIVEN
    required = RequiredHeir(
        base="casa,weekday", sufffacts={}, suff_idea_active_status=True
    )
    required.set_curr_idea_active_status(bool_x=True)
    assert required._status is None

    # WHEN
    required.set_status(acptfacts=None)

    # THEN
    assert required._status == True


def test_RequiredHeir_set_status_AgendaFalseCorrectlySetsStatusTrue():
    # GIVEN
    required = RequiredHeir(
        base="casa,weekday", sufffacts={}, suff_idea_active_status=False
    )
    required.set_curr_idea_active_status(bool_x=False)
    assert required._status is None
    # WHEN
    required.set_status(acptfacts=None)
    # THEN
    assert required._status == True


def test_RequiredHeir_set_status_AgendaTrueCorrectlySetsStatusFalse():
    # GIVEN
    required = RequiredHeir(
        base="casa,weekday", sufffacts={}, suff_idea_active_status=True
    )
    required.set_curr_idea_active_status(bool_x=False)
    assert required._status is None
    # WHEN
    required.set_status(acptfacts=None)
    # THEN
    assert required._status == False


def test_RequiredHeir_set_status_AgendaNoneCorrectlySetsStatusFalse():
    # GIVEN
    required = RequiredHeir(
        base="casa,weekday", sufffacts={}, suff_idea_active_status=True
    )
    required.set_curr_idea_active_status(bool_x=None)
    assert required._status is None
    # WHEN
    required.set_status(acptfacts={})
    # THEN
    assert required._status == False


def test_RequiredUnit_get_dict_ReturnsCorrectDictWithSingleSuffFactRequireds():
    sufffact_x = sufffactunit_shop(need="casa,weekday,wednesday")
    sufffacts = {sufffact_x.need: sufffact_x}
    required = RequiredUnit(base="casa,weekday", sufffacts=sufffacts)
    x_required_dict = required.get_dict()
    assert x_required_dict != None
    static_required_dict = {
        "base": "casa,weekday",
        "sufffacts": {
            "casa,weekday,wednesday": {
                "need": "casa,weekday,wednesday",
                "open": None,
                "nigh": None,
                "divisor": None,
            }
        },
    }
    print(x_required_dict)
    assert x_required_dict == static_required_dict


def test_RequiredUnit_get_dict_ReturnsCorrectDictWithTwoSuffFactsRequireds():
    sufffact1 = sufffactunit_shop(need="casa,weekday,wednesday")
    sufffact2 = sufffactunit_shop(need="casa,weekday,thursday")
    sufffacts = {sufffact1.need: sufffact1, sufffact2.need: sufffact2}
    required = RequiredUnit(base="casa,weekday", sufffacts=sufffacts)
    x_required_dict = required.get_dict()
    assert x_required_dict != None
    static_required_dict = {
        "base": "casa,weekday",
        "sufffacts": {
            "casa,weekday,wednesday": {
                "need": "casa,weekday,wednesday",
                "open": None,
                "nigh": None,
                "divisor": None,
            },
            "casa,weekday,thursday": {
                "need": "casa,weekday,thursday",
                "open": None,
                "nigh": None,
                "divisor": None,
            },
        },
    }
    print(x_required_dict)
    assert x_required_dict == static_required_dict


def test_RequiredHeir_correctSetsActionState():
    ced_day = "casa,ced_day"
    sufffact_x = sufffactunit_shop(need=ced_day, open=3, nigh=6)
    sufffacts = {sufffact_x.need: sufffact_x}
    required = RequiredHeir(base=ced_day, sufffacts=sufffacts)
    x_acptfact = acptfactheir_shop(base=ced_day, pick=ced_day, open=5, nigh=8)
    x_acptfacts = {x_acptfact.base: x_acptfact}
    assert required._status is None
    required.set_status(acptfacts=x_acptfacts)
    assert required._status == True
    assert required._task == True

    x_acptfact = acptfactheir_shop(base=ced_day, pick=ced_day, open=5, nigh=6)
    x_acptfacts = {x_acptfact.base: x_acptfact}
    required.set_status(acptfacts=x_acptfacts)
    assert required._status == True
    assert required._task == False

    x_acptfact = acptfactheir_shop(base=ced_day, pick=ced_day, open=0, nigh=1)
    x_acptfacts = {x_acptfact.base: x_acptfact}
    required.set_status(acptfacts=x_acptfacts)
    assert required._status == False
    assert required._task is None


def test_RequiredCore_set_empty_if_null_WorksCorrectly():
    ced_day = "casa,ced_day"
    required = RequiredCore(base=ced_day, sufffacts=None)
    assert required.sufffacts is None
    required.set_empty_if_null()
    assert required.sufffacts == {}


def test_RequiredCore_get_sufffacts_count():
    ced_day = "casa,ced_day"

    required = RequiredCore(base=ced_day, sufffacts=None)
    assert required.get_sufffacts_count() == 0
    sufffact_x = sufffactunit_shop(need=ced_day, open=3, nigh=6)
    sufffacts = {sufffact_x.need: sufffact_x}
    required = RequiredCore(base=ced_day, sufffacts=sufffacts)
    assert required.get_sufffacts_count() == 1


def test_RequiredCore_set_sufffact_CorrectlySetsSuffFact():
    # Given
    ced_day = "casa,ced_day"
    required = RequiredCore(base=ced_day, sufffacts=None)
    assert required.get_sufffacts_count() == 0

    # When
    required.set_sufffact(sufffact=ced_day, open=3, nigh=6)

    # Then
    assert required.get_sufffacts_count() == 1
    sufffact_x = sufffactunit_shop(need=ced_day, open=3, nigh=6)
    sufffacts = {sufffact_x.need: sufffact_x}
    assert required.sufffacts == sufffacts


def test_RequiredCore_del_sufffact_CorrectlyDeletesSuffFact():
    # Given
    ced_day = "casa,ced_day"
    required = RequiredCore(base=ced_day, sufffacts=None)
    required.set_sufffact(sufffact=ced_day, open=3, nigh=6)
    assert required.get_sufffacts_count() == 1
    # When
    required.del_sufffact(sufffact=ced_day)
    # Then
    assert required.get_sufffacts_count() == 0


def test_RequiredCore_find_replace_road_works():
    # GIVEN
    weekday_text = "weekday"
    sunday_text = "Sunday"
    old_weekday_road = f"{root_label()},{weekday_text}"
    old_sunday_road = f"{root_label()},{weekday_text},{sunday_text}"
    # sunday_sufffact_x = sufffactunit_shop(need=old_sunday_road)
    required_x = RequiredCore(base=old_weekday_road, sufffacts=None)
    required_x.set_sufffact(sufffact=old_sunday_road)
    # print(f"{required_x=}")
    assert required_x.base == old_weekday_road
    assert len(required_x.sufffacts) == 1
    print(f"{required_x.sufffacts=}")
    assert required_x.sufffacts.get(old_sunday_road).need == old_sunday_road

    # WHEN
    old_road = f"{root_label()}"
    new_road = "fun"
    required_x.find_replace_road(old_road=old_road, new_road=new_road)
    new_weekday_road = f"{new_road},{weekday_text}"
    new_sunday_road = f"{new_road},{weekday_text},{sunday_text}"

    # THEN
    assert required_x.base == new_weekday_road
    assert len(required_x.sufffacts) == 1
    assert required_x.sufffacts.get(new_sunday_road) != None
    assert required_x.sufffacts.get(old_sunday_road) is None
    print(f"{required_x.sufffacts=}")
    assert required_x.sufffacts.get(new_sunday_road).need == new_sunday_road


def test_RequiredCore_get_key_road():
    email_road = f"{root_label()},work,check email"
    sufffact_x = sufffactunit_shop(need=Road(email_road))
    sufffacts_x = {sufffact_x.need: sufffact_x}
    base = Road(f"{root_label()},work")
    required_x = RequiredHeir(base=base, sufffacts=sufffacts_x)
    assert required_x.get_key_road() == base


def test_RequiredCore_meld_BaseScenarioWorks():
    # GIVEN
    tech_text = "timetech"
    tech_road = f"{root_label()},{tech_text}"
    week_text = "ced_week"
    week_road = f"{root_label()},{tech_text},{week_text}"

    required_x1 = RequiredCore(base=tech_road, sufffacts={})
    required_x1.set_sufffact(sufffact=week_road)

    required_x2 = RequiredCore(base=tech_road, sufffacts={})
    required_x2.set_sufffact(sufffact=week_road)

    # WHEN/THEN
    assert required_x1 == required_x1.meld(other_required=required_x2)


def test_RequiredCore_meld_AddSuffFactscenarioWorks():
    # GIVEN
    tech_text = "timetech"
    tech_road = f"{root_label()},{tech_text}"
    week_text = "ced_week"
    week_road = f"{root_label()},{tech_text},{week_text}"

    required_x1 = RequiredCore(base=tech_road, sufffacts={})
    required_x1.set_sufffact(sufffact=week_road)

    required_x2 = RequiredCore(base=tech_road, sufffacts={})
    year_text = "year"
    year_road = f"{root_label()},{tech_text},{year_text}"
    required_x2.set_sufffact(sufffact=year_road, open=45, nigh=55)

    # WHEN/THEN
    required_x1.meld(other_required=required_x2)

    # THEN
    assert len(required_x1.sufffacts) == 2


def test_RequiredCore_meld_raises_NotSameRoadError():
    # GIVEN
    tech_text = "timetech"
    tech_road = f"{root_label()},{tech_text}"
    week_text = "ced_week"
    week_road = f"{root_label()},{tech_text},{week_text}"

    required_x1 = RequiredCore(base=tech_road, sufffacts={})
    required_x2 = RequiredCore(base=week_road, sufffacts={})

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        required_x1.meld(required_x2)
    assert (
        str(excinfo.value)
        == f"Meld fail: required={required_x2.base} is different self.base='{required_x1.base}'"
    )
