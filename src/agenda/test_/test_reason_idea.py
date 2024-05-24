from src.agenda.reason_idea import (
    ReasonCore,
    reasoncore_shop,
    reasonheir_shop,
    reasonunit_shop,
    beliefheir_shop,
    premiseunit_shop,
    reasons_get_from_dict,
)
from src._road.road import (
    get_default_real_id_roadnode as root_label,
    create_road,
    default_road_delimiter_if_none,
)
from pytest import raises as pytest_raises


def test_ReasonCore_attributesExist():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_premise = premiseunit_shop(need=wed_road)
    premises = {wed_premise.need: wed_premise}

    # WHEN
    wkday_reason = ReasonCore(
        base=wkday_road, premises=premises, suff_idea_active=False
    )

    # THEN
    assert wkday_reason.base == wkday_road
    assert wkday_reason.premises == premises
    assert wkday_reason.suff_idea_active == False
    assert wkday_reason.delimiter is None


def test_reasoncore_shop_ReturnsCorrectAttrWith_delimiter():
    # GIVEN
    slash_text = "/"
    gig_text = "gig"
    gig_road = create_road(root_label(), gig_text, delimiter=slash_text)
    print(f"{gig_road=} ")

    # WHEN
    gig_reason = reasonheir_shop(gig_road, delimiter=slash_text)

    # THEN
    assert gig_reason.delimiter == slash_text


def test_reasonheir_shop_ReturnsCorrectObj():
    # GIVEN
    gig_text = "gig"
    gig_road = create_road(root_label(), gig_text)

    # WHEN
    gig_reason = reasonheir_shop(gig_road)

    # THEN
    assert gig_reason.premises == {}
    assert gig_reason.delimiter == default_road_delimiter_if_none()


def test_ReasonHeir_clear_CorrectlyClearsField():
    # GIVEN
    gig_text = "gig"
    gig_road = create_road(root_label(), gig_text)
    email_text = "check email"
    email_road = create_road(gig_road, email_text)
    email_premise = premiseunit_shop(need=email_road)
    email_premises = {email_premise.need: email_premise}

    # WHEN
    gig_reason = reasonheir_shop(base=gig_road, premises=email_premises)
    # THEN
    assert gig_reason._status is None

    # GIVEN
    gig_reason._status = True
    assert gig_reason._status
    # WHEN
    gig_reason.clear_status()
    # THEN
    assert gig_reason._status is None
    assert gig_reason._base_idea_active is None


def test_ReasonHeir_set_status_CorrectlySetsStatus():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    fri_text = "friday"
    fri_road = create_road(wkday_road, fri_text)
    thu_text = "thursday"
    thu_road = create_road(wkday_road, thu_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_noon_text = "noon"
    wed_noon_road = create_road(wed_road, wed_noon_text)
    wed_premise = premiseunit_shop(need=wed_road)
    wed_premises = {wed_premise.need: wed_premise}
    wkday_reason = reasonheir_shop(base=wkday_road, premises=wed_premises)
    assert wkday_reason._status is None
    # WHEN
    wkday_belief = beliefheir_shop(base=wkday_road, pick=wed_noon_road)
    wkday_beliefs = {wkday_belief.base: wkday_belief}
    wkday_reason.set_status(beliefs=wkday_beliefs)
    # THEN
    assert wkday_reason._status == True

    # GIVEN
    thu_premise = premiseunit_shop(need=thu_road)
    two_premises = {wed_premise.need: wed_premise, thu_premise.need: thu_premise}
    two_reason = reasonheir_shop(base=wkday_road, premises=two_premises)
    assert two_reason._status is None
    # WHEN
    noon_belief = beliefheir_shop(base=wkday_road, pick=wed_noon_road)
    noon_beliefs = {noon_belief.base: noon_belief}
    two_reason.set_status(beliefs=noon_beliefs)
    # THEN
    assert two_reason._status == True

    # GIVEN
    two_reason.clear_status()
    assert two_reason._status is None
    # WHEN
    fri_belief = beliefheir_shop(base=wkday_road, pick=fri_road)
    fri_beliefs = {fri_belief.base: fri_belief}
    two_reason.set_status(beliefs=fri_beliefs)
    # THEN
    assert two_reason._status == False


def test_ReasonHeir_set_status_EmptyBeliefCorrectlySetsStatus():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_premise = premiseunit_shop(need=wed_road)
    wed_premises = {wed_premise.need: wed_premise}
    wkday_reason = reasonheir_shop(base=wkday_road, premises=wed_premises)
    assert wkday_reason._status is None
    wkday_reason.set_status(beliefs=None)
    assert wkday_reason._status == False


def test_ReasonHeir_set_base_idea_active_Correctly():
    # GIVEN
    day_text = "day"
    day_road = create_road(root_label(), day_text)
    day_reason = reasonheir_shop(base=day_road)
    assert day_reason._base_idea_active is None

    # WHEN
    day_reason.set_base_idea_active(bool_x=True)

    # THEN
    assert day_reason._base_idea_active


def test_ReasonHeir_set_status_AgendaTrueCorrectlySetsStatusTrue():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    week_reason = reasonheir_shop(base=wkday_road, suff_idea_active=True)
    week_reason.set_base_idea_active(bool_x=True)
    assert week_reason._status is None

    # WHEN
    week_reason.set_status(beliefs=None)

    # THEN
    assert week_reason._status == True


def test_ReasonHeir_set_status_AgendaFalseCorrectlySetsStatusTrue():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wkday_reason = reasonheir_shop(wkday_road, suff_idea_active=False)
    wkday_reason.set_base_idea_active(bool_x=False)
    assert wkday_reason._status is None

    # WHEN
    wkday_reason.set_status(beliefs=None)

    # THEN
    assert wkday_reason._status == True


def test_ReasonHeir_set_status_AgendaTrueCorrectlySetsStatusFalse():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wkday_reason = reasonheir_shop(wkday_road, suff_idea_active=True)
    wkday_reason.set_base_idea_active(bool_x=False)
    assert wkday_reason._status is None

    # WHEN
    wkday_reason.set_status(beliefs=None)

    # THEN
    assert wkday_reason._status == False


def test_ReasonHeir_set_status_AgendaNoneCorrectlySetsStatusFalse():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wkday_reason = reasonheir_shop(wkday_road, suff_idea_active=True)
    wkday_reason.set_base_idea_active(bool_x=None)
    assert wkday_reason._status is None

    # WHEN
    wkday_reason.set_status(beliefs={})

    # THEN
    assert wkday_reason._status == False


def test_reasonunit_shop_ReturnsCorrectObj():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)

    # WHEN
    wkday_reasonunit = reasonunit_shop(wkday_road)

    # THEN
    assert wkday_reasonunit.premises == {}
    assert wkday_reasonunit.delimiter == default_road_delimiter_if_none()


def test_ReasonUnit_get_dict_ReturnsCorrectDictWithSinglethu_premiseequireds():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    wed_premise = premiseunit_shop(need=wed_road)
    wed_premises = {wed_premise.need: wed_premise}
    wkday_reason = reasonunit_shop(wkday_road, premises=wed_premises)

    # WHEN
    wkday_reason_dict = wkday_reason.get_dict()

    # THEN
    assert wkday_reason_dict != None
    static_wkday_reason_dict = {
        "base": wkday_road,
        "premises": {wed_road: {"need": wed_road}},
    }
    print(wkday_reason_dict)
    assert wkday_reason_dict == static_wkday_reason_dict


def test_ReasonUnit_get_dict_ReturnsCorrectDictWith_suff_idea_active():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wkday_suff_idea_active = True
    wkday_reason = reasonunit_shop(wkday_road, suff_idea_active=wkday_suff_idea_active)

    # WHEN
    wkday_reason_dict = wkday_reason.get_dict()

    # THEN
    assert wkday_reason_dict != None
    static_wkday_reason_dict = {
        "base": wkday_road,
        "suff_idea_active": wkday_suff_idea_active,
    }
    print(wkday_reason_dict)
    assert wkday_reason_dict == static_wkday_reason_dict


def test_ReasonUnit_get_dict_ReturnsCorrectDictWithTwoPremisesReasons():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = create_road(wkday_road, wed_text)
    thu_text = "thursday"
    thu_road = create_road(wkday_road, thu_text)
    wed_premise = premiseunit_shop(need=wed_road)
    thu_premise = premiseunit_shop(need=thu_road)
    two_premises = {wed_premise.need: wed_premise, thu_premise.need: thu_premise}
    wkday_reason = reasonunit_shop(wkday_road, premises=two_premises)

    # WHEN
    wkday_reason_dict = wkday_reason.get_dict()

    # THEN
    assert wkday_reason_dict != None
    static_wkday_reason_dict = {
        "base": wkday_road,
        "premises": {wed_road: {"need": wed_road}, thu_road: {"need": thu_road}},
    }
    print(wkday_reason_dict)
    assert wkday_reason_dict == static_wkday_reason_dict


def test_reasons_get_from_dict_ReturnsCorrectObj():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = create_road(root_label(), wkday_text)
    wkday_suff_idea_active = False
    wkday_reasonunit = reasonunit_shop(
        wkday_road, suff_idea_active=wkday_suff_idea_active
    )
    x_wkday_reasonunits_dict = {wkday_reasonunit.base: wkday_reasonunit.get_dict()}
    assert x_wkday_reasonunits_dict != None
    static_wkday_reason_dict = {
        wkday_road: {
            "base": wkday_road,
            "suff_idea_active": wkday_suff_idea_active,
        }
    }
    assert x_wkday_reasonunits_dict == static_wkday_reason_dict

    # WHEN
    reasonunits_dict = reasons_get_from_dict(x_wkday_reasonunits_dict)

    # THEN
    assert len(reasonunits_dict) == 1
    assert reasonunits_dict.get(wkday_reasonunit.base) == wkday_reasonunit


def test_ReasonHeir_correctSetsActionState():
    # GIVEN
    day_text = "ced_day"
    day_road = create_road(root_label(), day_text)
    range_3_to_6_premise = premiseunit_shop(need=day_road, open=3, nigh=6)
    range_3_to_6_premises = {range_3_to_6_premise.need: range_3_to_6_premise}
    range_3_to_6_reason = reasonheir_shop(day_road, range_3_to_6_premises)
    assert range_3_to_6_reason._status is None

    # WHEN
    range_5_to_8_belief = beliefheir_shop(day_road, day_road, open=5, nigh=8)
    range_5_to_8_beliefs = {range_5_to_8_belief.base: range_5_to_8_belief}
    range_3_to_6_reason.set_status(beliefs=range_5_to_8_beliefs)
    # THEN
    assert range_3_to_6_reason._status == True
    assert range_3_to_6_reason._task == True

    # WHEN
    range_5_to_6_belief = beliefheir_shop(day_road, day_road, open=5, nigh=6)
    range_5_to_6_beliefs = {range_5_to_6_belief.base: range_5_to_6_belief}
    range_3_to_6_reason.set_status(beliefs=range_5_to_6_beliefs)
    # THEN
    assert range_3_to_6_reason._status == True
    assert range_3_to_6_reason._task == False

    # WHEN
    range_0_to_1_belief = beliefheir_shop(day_road, day_road, open=0, nigh=1)
    range_0_to_1_beliefs = {range_0_to_1_belief.base: range_0_to_1_belief}
    range_3_to_6_reason.set_status(beliefs=range_0_to_1_beliefs)
    # THEN
    assert range_3_to_6_reason._status == False
    assert range_3_to_6_reason._task is None


def test_ReasonCore_get_premises_count():
    # GIVEN
    day_text = "day"
    day_road = create_road(root_label(), day_text)

    # WHEN
    day_reason = reasoncore_shop(base=day_road)
    # THEN
    assert day_reason.get_premises_count() == 0

    # WHEN
    range_3_to_6_premise = premiseunit_shop(need=day_road, open=3, nigh=6)
    range_3_to_6_premises = {range_3_to_6_premise.need: range_3_to_6_premise}
    day_reason = reasoncore_shop(base=day_road, premises=range_3_to_6_premises)
    # THEN
    assert day_reason.get_premises_count() == 1


def test_ReasonCore_set_premise_CorrectlySetsPremise():
    # GIVEN
    day_text = "day"
    day_road = create_road(root_label(), day_text)
    day_reason = reasoncore_shop(base=day_road)
    assert day_reason.get_premises_count() == 0

    # WHEN
    day_reason.set_premise(premise=day_road, open=3, nigh=6)

    # THEN
    assert day_reason.get_premises_count() == 1
    range_3_to_6_premise = premiseunit_shop(need=day_road, open=3, nigh=6)
    premises = {range_3_to_6_premise.need: range_3_to_6_premise}
    assert day_reason.premises == premises


def test_ReasonCore_get_single_premis_ReturnsCorrectObj():
    # GIVEN
    day_road = create_road(root_label(), "day")
    day_reason = reasoncore_shop(base=day_road)
    day_reason.set_premise(premise=day_road, open=3, nigh=6)
    day_reason.set_premise(premise=day_road, open=7, nigh=10)
    noon_road = create_road(day_road, "noon")
    day_reason.set_premise(premise=noon_road)
    assert day_reason.get_premises_count() == 2

    # WHEN / THEN
    assert day_reason.get_premise(premise=day_road).open == 7
    assert day_reason.get_premise(premise=noon_road).open is None


def test_ReasonCore_del_premise_CorrectlyDeletesPremise():
    # GIVEN
    day_text = "day"
    day_road = create_road(root_label(), day_text)
    day_reason = reasoncore_shop(base=day_road)
    day_reason.set_premise(premise=day_road, open=3, nigh=6)
    assert day_reason.get_premises_count() == 1

    # WHEN
    day_reason.del_premise(premise=day_road)

    # THEN
    assert day_reason.get_premises_count() == 0


def test_ReasonCore_find_replace_road_gigs():
    # GIVEN
    weekday_text = "weekday"
    sunday_text = "Sunday"
    old_weekday_road = create_road(root_label(), weekday_text)
    old_sunday_road = create_road(old_weekday_road, sunday_text)
    x_reason = reasoncore_shop(base=old_weekday_road)
    x_reason.set_premise(premise=old_sunday_road)
    # print(f"{x_reason=}")
    assert x_reason.base == old_weekday_road
    assert len(x_reason.premises) == 1
    print(f"{x_reason.premises=}")
    assert x_reason.premises.get(old_sunday_road).need == old_sunday_road

    # WHEN
    old_road = root_label()
    new_road = "fun"
    x_reason.find_replace_road(old_road=old_road, new_road=new_road)
    new_weekday_road = create_road(new_road, weekday_text)
    new_sunday_road = create_road(new_weekday_road, sunday_text)

    # THEN
    assert x_reason.base == new_weekday_road
    assert len(x_reason.premises) == 1
    assert x_reason.premises.get(new_sunday_road) != None
    assert x_reason.premises.get(old_sunday_road) is None
    print(f"{x_reason.premises=}")
    assert x_reason.premises.get(new_sunday_road).need == new_sunday_road


def test_ReasonCore_set_delimiter_SetsAttrsCorrectly():
    # GIVEN
    week_text = "weekday"
    sun_text = "Sunday"
    slash_text = "/"
    slash_week_road = create_road(root_label(), week_text, delimiter=slash_text)
    slash_sun_road = create_road(slash_week_road, sun_text, delimiter=slash_text)
    week_reasonunit = reasoncore_shop(slash_week_road, delimiter=slash_text)
    week_reasonunit.set_premise(slash_sun_road)
    assert week_reasonunit.delimiter == slash_text
    assert week_reasonunit.base == slash_week_road
    assert week_reasonunit.premises.get(slash_sun_road).need == slash_sun_road

    # WHEN
    star_text = "*"
    week_reasonunit.set_delimiter(new_delimiter=star_text)

    # THEN
    assert week_reasonunit.delimiter == star_text
    star_week_road = create_road(root_label(), week_text, delimiter=star_text)
    star_sun_road = create_road(star_week_road, sun_text, delimiter=star_text)
    assert week_reasonunit.base == star_week_road
    assert week_reasonunit.premises.get(star_sun_road) != None
    assert week_reasonunit.premises.get(star_sun_road).need == star_sun_road


def test_ReasonCore_get_obj_key():
    # GIVEN
    gig_text = "gig"
    gig_road = create_road(root_label(), gig_text)
    email_text = "check email"
    email_road = create_road(gig_road, email_text)
    email_premise = premiseunit_shop(need=email_road)
    premises_x = {email_premise.need: email_premise}

    # WHEN
    x_reason = reasonheir_shop(gig_road, premises=premises_x)

    # THEN
    assert x_reason.get_obj_key() == gig_road


def test_ReasonCore_meld_ReturnsCorrectObj_BaseScenario():
    # GIVEN
    tech_text = "timetech"
    tech_road = create_road(root_label(), tech_text)
    week_text = "ced_week"
    week_road = create_road(tech_road, week_text)

    x1_reason = reasoncore_shop(base=tech_road)
    x1_reason.set_premise(premise=week_road)

    x2_reason = reasoncore_shop(base=tech_road)
    x2_reason.set_premise(premise=week_road)

    # WHEN/THEN
    assert x1_reason == x1_reason.meld(other_reason=x2_reason)


def test_ReasonCore_meld_ReturnsCorrectObj_AddPremisescenario():
    # GIVEN
    tech_text = "timetech"
    tech_road = create_road(root_label(), tech_text)
    week_text = "ced_week"
    week_road = create_road(tech_road, week_text)

    x1_reason = reasoncore_shop(base=tech_road)
    x1_reason.set_premise(premise=week_road)

    x2_reason = reasoncore_shop(base=tech_road)
    year_text = "year"
    year_road = create_road(tech_road, year_text)
    x2_reason.set_premise(premise=year_road, open=45, nigh=55)

    # WHEN/THEN
    x1_reason.meld(other_reason=x2_reason)

    # THEN
    assert len(x1_reason.premises) == 2


def test_ReasonCore_meld_raises_NotSameRoadUnitError():
    # GIVEN
    tech_text = "timetech"
    tech_road = create_road(root_label(), tech_text)
    week_text = "ced_week"
    week_road = create_road(tech_road, week_text)

    x1_reason = reasoncore_shop(base=tech_road)
    x2_reason = reasoncore_shop(base=week_road)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x1_reason.meld(x2_reason)
    assert (
        str(excinfo.value)
        == f"Meld fail: reason={x2_reason.base} is different self.base='{x1_reason.base}'"
    )
