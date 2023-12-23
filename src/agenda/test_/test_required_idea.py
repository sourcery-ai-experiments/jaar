from src.agenda.required_idea import (
    RequiredCore,
    requiredcore_shop,
    requiredheir_shop,
    requiredunit_shop,
    acptfactheir_shop,
    sufffactunit_shop,
)
from src.agenda.road import (
    get_default_economy_root_label as root_label,
    get_road,
    get_node_delimiter,
)
from pytest import raises as pytest_raises


def test_RequiredCore_attributesExist():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = get_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = get_road(wkday_road, wed_text)
    wed_sufffact = sufffactunit_shop(need=wed_road)
    sufffacts = {wed_sufffact.need: wed_sufffact}

    # WHEN
    wkday_required = RequiredCore(
        base=wkday_road, sufffacts=sufffacts, suff_idea_active_status=False
    )

    # THEN
    assert wkday_required.base == wkday_road
    assert wkday_required.sufffacts == sufffacts
    assert wkday_required.suff_idea_active_status == False
    assert wkday_required.delimiter is None


def test_requiredcore_shop_ReturnsCorrectAttrWith_delimiter():
    # GIVEN
    slash_text = "/"
    work_text = "work"
    work_road = get_road(root_label(), work_text, delimiter=slash_text)
    print(f"{work_road=} ")

    # WHEN
    work_required = requiredheir_shop(work_road, delimiter=slash_text)

    # THEN
    assert work_required.delimiter == slash_text


def test_requiredheir_shop_ReturnsCorrectObj():
    # GIVEN
    work_text = "work"
    work_road = get_road(root_label(), work_text)

    # WHEN
    work_required = requiredheir_shop(work_road)

    # THEN
    assert work_required.sufffacts == {}
    assert work_required.delimiter == get_node_delimiter()


def test_RequiredHeir_clear_CorrectlyClearsField():
    # GIVEN
    work_text = "work"
    work_road = get_road(root_label(), work_text)
    email_text = "check email"
    email_road = get_road(work_road, email_text)
    email_sufffact = sufffactunit_shop(need=email_road)
    email_sufffacts = {email_sufffact.need: email_sufffact}

    # WHEN
    work_required = requiredheir_shop(base=work_road, sufffacts=email_sufffacts)
    # THEN
    assert work_required._status is None

    # GIVEN
    work_required._status = True
    assert work_required._status
    # WHEN
    work_required.clear_status()
    # THEN
    assert work_required._status is None
    assert work_required._curr_idea_active_status is None


def test_RequiredHeir_set_status_CorrectlySetsStatus():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = get_road(root_label(), wkday_text)
    fri_text = "friday"
    fri_road = get_road(wkday_road, fri_text)
    thu_text = "thursday"
    thu_road = get_road(wkday_road, thu_text)
    wed_text = "wednesday"
    wed_road = get_road(wkday_road, wed_text)
    wed_noon_text = "noon"
    wed_noon_road = get_road(wed_road, wed_noon_text)
    wed_sufffact = sufffactunit_shop(need=wed_road)
    wed_sufffacts = {wed_sufffact.need: wed_sufffact}
    wkday_required = requiredheir_shop(base=wkday_road, sufffacts=wed_sufffacts)
    assert wkday_required._status is None
    # WHEN
    wkday_acptfact = acptfactheir_shop(base=wkday_road, pick=wed_noon_road)
    wkday_acptfacts = {wkday_acptfact.base: wkday_acptfact}
    wkday_required.set_status(acptfacts=wkday_acptfacts)
    # THEN
    assert wkday_required._status == True

    # GIVEN
    thu_sufffact = sufffactunit_shop(need=thu_road)
    two_sufffacts = {wed_sufffact.need: wed_sufffact, thu_sufffact.need: thu_sufffact}
    two_required = requiredheir_shop(base=wkday_road, sufffacts=two_sufffacts)
    assert two_required._status is None
    # WHEN
    noon_acptfact = acptfactheir_shop(base=wkday_road, pick=wed_noon_road)
    noon_acptfacts = {noon_acptfact.base: noon_acptfact}
    two_required.set_status(acptfacts=noon_acptfacts)
    # THEN
    assert two_required._status == True

    # GIVEN
    two_required.clear_status()
    assert two_required._status is None
    # WHEN
    fri_acptfact = acptfactheir_shop(base=wkday_road, pick=fri_road)
    fri_acptfacts = {fri_acptfact.base: fri_acptfact}
    two_required.set_status(acptfacts=fri_acptfacts)
    # THEN
    assert two_required._status == False


def test_RequiredHeir_set_status_EmptyAcptFactCorrectlySetsStatus():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = get_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = get_road(wkday_road, wed_text)
    wed_sufffact = sufffactunit_shop(need=wed_road)
    wed_sufffacts = {wed_sufffact.need: wed_sufffact}
    wkday_required = requiredheir_shop(base=wkday_road, sufffacts=wed_sufffacts)
    assert wkday_required._status is None
    wkday_required.set_status(acptfacts=None)
    assert wkday_required._status == False


def test_RequiredHeir_set_curr_idea_active_status_Correctly():
    # GIVEN
    day_text = "day"
    day_road = get_road(root_label(), day_text)
    day_required = requiredheir_shop(base=day_road)
    assert day_required._curr_idea_active_status is None

    # WHEN
    day_required.set_curr_idea_active_status(bool_x=True)

    # THEN
    assert day_required._curr_idea_active_status


def test_RequiredHeir_set_status_AgendaTrueCorrectlySetsStatusTrue():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = get_road(root_label(), wkday_text)
    week_required = requiredheir_shop(base=wkday_road, suff_idea_active_status=True)
    week_required.set_curr_idea_active_status(bool_x=True)
    assert week_required._status is None

    # WHEN
    week_required.set_status(acptfacts=None)

    # THEN
    assert week_required._status == True


def test_RequiredHeir_set_status_AgendaFalseCorrectlySetsStatusTrue():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = get_road(root_label(), wkday_text)
    wkday_required = requiredheir_shop(wkday_road, suff_idea_active_status=False)
    wkday_required.set_curr_idea_active_status(bool_x=False)
    assert wkday_required._status is None

    # WHEN
    wkday_required.set_status(acptfacts=None)

    # THEN
    assert wkday_required._status == True


def test_RequiredHeir_set_status_AgendaTrueCorrectlySetsStatusFalse():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = get_road(root_label(), wkday_text)
    wkday_required = requiredheir_shop(wkday_road, suff_idea_active_status=True)
    wkday_required.set_curr_idea_active_status(bool_x=False)
    assert wkday_required._status is None

    # WHEN
    wkday_required.set_status(acptfacts=None)

    # THEN
    assert wkday_required._status == False


def test_RequiredHeir_set_status_AgendaNoneCorrectlySetsStatusFalse():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = get_road(root_label(), wkday_text)
    wkday_required = requiredheir_shop(wkday_road, suff_idea_active_status=True)
    wkday_required.set_curr_idea_active_status(bool_x=None)
    assert wkday_required._status is None

    # WHEN
    wkday_required.set_status(acptfacts={})

    # THEN
    assert wkday_required._status == False


def test_requiredunit_shop_ReturnsCorrectObj():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = get_road(root_label(), wkday_text)

    # WHEN
    wkday_requiredunit = requiredunit_shop(wkday_road)

    # THEN
    assert wkday_requiredunit.sufffacts == {}
    assert wkday_requiredunit.delimiter == get_node_delimiter()


def test_RequiredUnit_get_dict_ReturnsCorrectDictWithSinglethu_sufffactequireds():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = get_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = get_road(wkday_road, wed_text)
    wed_sufffact = sufffactunit_shop(need=wed_road)
    wed_sufffacts = {wed_sufffact.need: wed_sufffact}
    wkday_required = requiredunit_shop(wkday_road, sufffacts=wed_sufffacts)

    # WHEN
    wkday_required_dict = wkday_required.get_dict()

    # THEN
    assert wkday_required_dict != None
    static_wkday_required_dict = {
        "base": wkday_road,
        "sufffacts": {wed_road: {"need": wed_road}},
    }
    print(wkday_required_dict)
    assert wkday_required_dict == static_wkday_required_dict


def test_RequiredUnit_get_dict_ReturnsCorrectDictWithTwoSuffFactsRequireds():
    # GIVEN
    wkday_text = "weekday"
    wkday_road = get_road(root_label(), wkday_text)
    wed_text = "wednesday"
    wed_road = get_road(wkday_road, wed_text)
    thu_text = "thursday"
    thu_road = get_road(wkday_road, thu_text)
    wed_sufffact = sufffactunit_shop(need=wed_road)
    thu_sufffact = sufffactunit_shop(need=thu_road)
    two_sufffacts = {wed_sufffact.need: wed_sufffact, thu_sufffact.need: thu_sufffact}
    wkday_required = requiredunit_shop(wkday_road, sufffacts=two_sufffacts)

    # WHEN
    wkday_required_dict = wkday_required.get_dict()

    # THEN
    assert wkday_required_dict != None
    static_wkday_required_dict = {
        "base": wkday_road,
        "sufffacts": {wed_road: {"need": wed_road}, thu_road: {"need": thu_road}},
    }
    print(wkday_required_dict)
    assert wkday_required_dict == static_wkday_required_dict


def test_RequiredHeir_correctSetsActionState():
    # GIVEN
    day_text = "ced_day"
    day_road = get_road(root_label(), day_text)
    range_3_to_6_sufffact = sufffactunit_shop(need=day_road, open=3, nigh=6)
    range_3_to_6_sufffacts = {range_3_to_6_sufffact.need: range_3_to_6_sufffact}
    range_3_to_6_required = requiredheir_shop(day_road, range_3_to_6_sufffacts)
    assert range_3_to_6_required._status is None

    # WHEN
    range_5_to_8_acptfact = acptfactheir_shop(day_road, day_road, open=5, nigh=8)
    range_5_to_8_acptfacts = {range_5_to_8_acptfact.base: range_5_to_8_acptfact}
    range_3_to_6_required.set_status(acptfacts=range_5_to_8_acptfacts)
    # THEN
    assert range_3_to_6_required._status == True
    assert range_3_to_6_required._task == True

    # WHEN
    range_5_to_6_acptfact = acptfactheir_shop(day_road, day_road, open=5, nigh=6)
    range_5_to_6_acptfacts = {range_5_to_6_acptfact.base: range_5_to_6_acptfact}
    range_3_to_6_required.set_status(acptfacts=range_5_to_6_acptfacts)
    # THEN
    assert range_3_to_6_required._status == True
    assert range_3_to_6_required._task == False

    # WHEN
    range_0_to_1_acptfact = acptfactheir_shop(day_road, day_road, open=0, nigh=1)
    range_0_to_1_acptfacts = {range_0_to_1_acptfact.base: range_0_to_1_acptfact}
    range_3_to_6_required.set_status(acptfacts=range_0_to_1_acptfacts)
    # THEN
    assert range_3_to_6_required._status == False
    assert range_3_to_6_required._task is None


def test_RequiredCore_get_sufffacts_count():
    # GIVEN
    day_text = "day"
    day_road = get_road(root_label(), day_text)

    # WHEN
    day_required = requiredcore_shop(base=day_road)
    # THEN
    assert day_required.get_sufffacts_count() == 0

    # WHEN
    range_3_to_6_sufffact = sufffactunit_shop(need=day_road, open=3, nigh=6)
    range_3_to_6_sufffacts = {range_3_to_6_sufffact.need: range_3_to_6_sufffact}
    day_required = requiredcore_shop(base=day_road, sufffacts=range_3_to_6_sufffacts)
    # THEN
    assert day_required.get_sufffacts_count() == 1


def test_RequiredCore_set_sufffact_CorrectlySetsSuffFact():
    # GIVEN
    day_text = "day"
    day_road = get_road(root_label(), day_text)
    day_required = requiredcore_shop(base=day_road)
    assert day_required.get_sufffacts_count() == 0

    # WHEN
    day_required.set_sufffact(sufffact=day_road, open=3, nigh=6)

    # THEN
    assert day_required.get_sufffacts_count() == 1
    range_3_to_6_sufffact = sufffactunit_shop(need=day_road, open=3, nigh=6)
    sufffacts = {range_3_to_6_sufffact.need: range_3_to_6_sufffact}
    assert day_required.sufffacts == sufffacts


def test_RequiredCore_del_sufffact_CorrectlyDeletesSuffFact():
    # GIVEN
    day_text = "day"
    day_road = get_road(root_label(), day_text)
    day_required = requiredcore_shop(base=day_road)
    day_required.set_sufffact(sufffact=day_road, open=3, nigh=6)
    assert day_required.get_sufffacts_count() == 1

    # WHEN
    day_required.del_sufffact(sufffact=day_road)

    # THEN
    assert day_required.get_sufffacts_count() == 0


def test_RequiredCore_find_replace_road_works():
    # GIVEN
    weekday_text = "weekday"
    sunday_text = "Sunday"
    old_weekday_road = get_road(root_label(), weekday_text)
    old_sunday_road = get_road(old_weekday_road, sunday_text)
    x_required = requiredcore_shop(base=old_weekday_road)
    x_required.set_sufffact(sufffact=old_sunday_road)
    # print(f"{x_required=}")
    assert x_required.base == old_weekday_road
    assert len(x_required.sufffacts) == 1
    print(f"{x_required.sufffacts=}")
    assert x_required.sufffacts.get(old_sunday_road).need == old_sunday_road

    # WHEN
    old_road = root_label()
    new_road = "fun"
    x_required.find_replace_road(old_road=old_road, new_road=new_road)
    new_weekday_road = get_road(new_road, weekday_text)
    new_sunday_road = get_road(new_weekday_road, sunday_text)

    # THEN
    assert x_required.base == new_weekday_road
    assert len(x_required.sufffacts) == 1
    assert x_required.sufffacts.get(new_sunday_road) != None
    assert x_required.sufffacts.get(old_sunday_road) is None
    print(f"{x_required.sufffacts=}")
    assert x_required.sufffacts.get(new_sunday_road).need == new_sunday_road


def test_RequiredCore_set_delimiter_SetsAttrsCorrectly():
    # GIVEN
    week_text = "weekday"
    sun_text = "Sunday"
    slash_text = "/"
    slash_week_road = get_road(root_label(), week_text, delimiter=slash_text)
    slash_sun_road = get_road(slash_week_road, sun_text, delimiter=slash_text)
    week_requiredunit = requiredcore_shop(slash_week_road, delimiter=slash_text)
    week_requiredunit.set_sufffact(slash_sun_road)
    assert week_requiredunit.delimiter == slash_text
    assert week_requiredunit.base == slash_week_road
    assert week_requiredunit.sufffacts.get(slash_sun_road).need == slash_sun_road

    # WHEN
    star_text = "*"
    week_requiredunit.set_delimiter(new_delimiter=star_text)

    # THEN
    assert week_requiredunit.delimiter == star_text
    star_week_road = get_road(root_label(), week_text, delimiter=star_text)
    star_sun_road = get_road(star_week_road, sun_text, delimiter=star_text)
    assert week_requiredunit.base == star_week_road
    assert week_requiredunit.sufffacts.get(star_sun_road) != None
    assert week_requiredunit.sufffacts.get(star_sun_road).need == star_sun_road


def test_RequiredCore_get_key_road():
    # GIVEN
    work_text = "work"
    work_road = get_road(root_label(), work_text)
    email_text = "check email"
    email_road = get_road(work_road, email_text)
    email_sufffact = sufffactunit_shop(need=email_road)
    sufffacts_x = {email_sufffact.need: email_sufffact}

    # WHEN
    x_required = requiredheir_shop(work_road, sufffacts=sufffacts_x)

    # THEN
    assert x_required.get_key_road() == work_road


def test_RequiredCore_meld_BaseScenarioWorks():
    # GIVEN
    tech_text = "timetech"
    tech_road = get_road(root_label(), tech_text)
    week_text = "ced_week"
    week_road = get_road(tech_road, week_text)

    x1_required = requiredcore_shop(base=tech_road)
    x1_required.set_sufffact(sufffact=week_road)

    x2_required = requiredcore_shop(base=tech_road)
    x2_required.set_sufffact(sufffact=week_road)

    # WHEN/THEN
    assert x1_required == x1_required.meld(other_required=x2_required)


def test_RequiredCore_meld_AddSuffFactscenarioWorks():
    # GIVEN
    tech_text = "timetech"
    tech_road = get_road(root_label(), tech_text)
    week_text = "ced_week"
    week_road = get_road(tech_road, week_text)

    x1_required = requiredcore_shop(base=tech_road)
    x1_required.set_sufffact(sufffact=week_road)

    x2_required = requiredcore_shop(base=tech_road)
    year_text = "year"
    year_road = get_road(tech_road, year_text)
    x2_required.set_sufffact(sufffact=year_road, open=45, nigh=55)

    # WHEN/THEN
    x1_required.meld(other_required=x2_required)

    # THEN
    assert len(x1_required.sufffacts) == 2


def test_RequiredCore_meld_raises_NotSameRoadUnitError():
    # GIVEN
    tech_text = "timetech"
    tech_road = get_road(root_label(), tech_text)
    week_text = "ced_week"
    week_road = get_road(tech_road, week_text)

    x1_required = requiredcore_shop(base=tech_road)
    x2_required = requiredcore_shop(base=week_road)

    # WHEN/THEN
    with pytest_raises(Exception) as excinfo:
        x1_required.meld(x2_required)
    assert (
        str(excinfo.value)
        == f"Meld fail: required={x2_required.base} is different self.base='{x1_required.base}'"
    )
