from src.calendar.member import MemberName, memberlink_shop, memberunit_shop
from src.calendar.group import GroupName, groupunit_shop, grouplink_shop
from src.calendar.examples.example_calendars import (
    calendar_v001 as examples_calendar_v001,
    calendar_v001_with_large_agenda as examples_calendar_v001_with_large_agenda,
)
from src.calendar.calendar import CalendarUnit, get_intersection_of_members
from src.calendar.idea import IdeaKid
from pytest import raises as pytest_raises
from src.system.bank_sqlstr import RiverTmemberUnit


def test_calendar_members_exists():
    # GIVEN / WHEN
    cx = CalendarUnit()

    # THEN
    assert cx._members is None

    # GIVEN
    yahri_member = memberunit_shop(name=MemberName("yahri"))
    members_x = {yahri_member.name: yahri_member}
    cx2 = CalendarUnit()

    # WHEN
    cx2.set_memberunit(memberunit=yahri_member)

    # THEN
    assert cx2._members == members_x


def test_example_has_members():
    # GIVEN / WHEN
    cx = examples_calendar_v001()

    # THEN
    assert cx._members != None
    assert len(cx._members) == 22


def test_calendar_set_member_correctly_sets_members_1():
    # GIVEN
    cx = CalendarUnit(_owner="prom")
    cx.set_calendar_metrics()
    assert len(cx._members) == 0
    assert len(cx._groups) == 0

    # WHEN
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName("rico")))
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName("carmen")))
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName("patrick")))

    # THEN
    assert len(cx._members) == 3
    assert len(cx._groups) == 3
    assert cx._groups["rico"]._single_member == True

    # WHEN
    cx._idearoot.set_grouplink(
        grouplink=grouplink_shop(name=GroupName("rico"), creditor_weight=10)
    )
    cx._idearoot.set_grouplink(
        grouplink=grouplink_shop(name=GroupName("carmen"), creditor_weight=10)
    )
    cx._idearoot.set_grouplink(
        grouplink=grouplink_shop(name=GroupName("patrick"), creditor_weight=10)
    )
    assert len(cx._idearoot._grouplinks) == 3


def test_calendar_set_member_correctly_sets_members_2():
    # GIVEN
    cx = CalendarUnit(_owner="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    assign_text = "assignment"

    # WHEN
    cx.add_memberunit(name=rico_text, uid=61, creditor_weight=13, debtor_weight=8)
    cx.add_memberunit(name=carm_text, uid=5, debtor_weight=5)
    cx.add_memberunit(name=patr_text, creditor_weight=17, depotlink_type=assign_text)

    # THEN
    assert len(cx._members) == 3
    assert len(cx._groups) == 3
    assert cx._groups.get(rico_text)._single_member == True
    assert cx._members.get(patr_text).creditor_weight == 17
    assert cx._members.get(carm_text).debtor_weight == 5
    assert cx._members.get(patr_text).depotlink_type == assign_text


def test_calendar_get_idea_list_CorrectlySetsMemberLinkCalendarCreditAndDebt():
    # GIVEN
    prom_text = "prom"
    cx = CalendarUnit(_owner=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(rico_text)))
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(carm_text)))
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(patr_text)))
    bl_rico = grouplink_shop(name=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = grouplink_shop(name=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = grouplink_shop(name=patr_text, creditor_weight=10, debtor_weight=5)
    cx._idearoot.set_grouplink(grouplink=bl_rico)
    cx._idearoot.set_grouplink(grouplink=bl_carm)
    cx._idearoot.set_grouplink(grouplink=bl_patr)

    rico_groupunit = cx._groups.get(rico_text)
    carm_groupunit = cx._groups.get(carm_text)
    patr_groupunit = cx._groups.get(patr_text)
    rico_memberlink = rico_groupunit._members.get(rico_text)
    carm_memberlink = carm_groupunit._members.get(carm_text)
    patr_memberlink = patr_groupunit._members.get(patr_text)
    rico_memberlink._calendar_credit is None
    rico_memberlink._calendar_debt is None
    carm_memberlink._calendar_credit is None
    carm_memberlink._calendar_debt is None
    patr_memberlink._calendar_credit is None
    patr_memberlink._calendar_debt is None

    # for group in cx._groups.values():
    #     for memberlink in group._members.values():
    #         assert memberlink._calendar_credit is None
    #         assert memberlink._calendar_debt is None

    cx.set_calendar_metrics()

    # for grouplink in cx._groupheirs.values():
    #     print(
    #         f"{cx._calendar_importance=} {grouplink.name=} {grouplink._calendar_credit=} {grouplink._calendar_debt=}"
    #     )

    assert rico_memberlink._calendar_credit == 0.5
    assert rico_memberlink._calendar_debt == 0.8
    assert carm_memberlink._calendar_credit == 0.25
    assert carm_memberlink._calendar_debt == 0.1
    assert patr_memberlink._calendar_credit == 0.25
    assert patr_memberlink._calendar_debt == 0.1

    # memberlink_calendar_credit_sum = 0.0
    # memberlink_calendar_debt_sum = 0.0
    # for group in cx._groups.values():
    #     # print(f"{group.name=} {group._members=}")

    #     for memberlink in group._members.values():
    #         assert memberlink._calendar_credit != None
    #         assert memberlink._calendar_credit in [0.25, 0.5]
    #         assert memberlink._calendar_debt != None
    #         assert memberlink._calendar_debt in [0.8, 0.1]
    #         # print(
    #         #     f"{group.name=} {memberlink._calendar_importance=} {group._calendar_importance=}"
    #         # )
    #         memberlink_calendar_credit_sum += memberlink._calendar_credit
    #         memberlink_calendar_debt_sum += memberlink._calendar_debt

    #         # print(f"{memberlink_calendar_importance_sum=}")
    # assert memberlink_calendar_credit_sum == 1.0
    # assert memberlink_calendar_debt_sum == 1.0

    assert (
        rico_memberlink._calendar_credit
        + carm_memberlink._calendar_credit
        + patr_memberlink._calendar_credit
        == 1.0
    )
    assert (
        rico_memberlink._calendar_debt
        + carm_memberlink._calendar_debt
        + patr_memberlink._calendar_debt
        == 1.0
    )

    # WHEN another action, make sure metrics are as expected
    selena_text = "selena"
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(selena_text)))
    cx._idearoot.set_grouplink(
        grouplink=grouplink_shop(
            name=GroupName(selena_text), creditor_weight=20, debtor_weight=13
        )
    )
    cx.set_calendar_metrics()

    # THEN
    selena_groupunit = cx._groups.get(selena_text)
    selena_memberlink = selena_groupunit._members.get(selena_text)

    assert rico_memberlink._calendar_credit != 0.25
    assert rico_memberlink._calendar_debt != 0.8
    assert carm_memberlink._calendar_credit != 0.25
    assert carm_memberlink._calendar_debt != 0.1
    assert patr_memberlink._calendar_credit != 0.5
    assert patr_memberlink._calendar_debt != 0.1
    assert selena_memberlink._calendar_credit != None
    assert selena_memberlink._calendar_debt != None

    # memberlink_calendar_credit_sum = 0.0
    # memberlink_calendar_debt_sum = 0.0

    # for group in cx._groups.values():
    #     # print(f"{group.name=} {group._members=}")

    #     for memberlink in group._members.values():
    #         assert memberlink._calendar_credit != None
    #         assert memberlink._calendar_credit not in [0.25, 0.5]
    #         assert memberlink._calendar_debt != None
    #         assert memberlink._calendar_debt not in [0.8, 0.1]
    #         # print(
    #         #     f"{group.name=} {memberlink._calendar_importance=} {group._calendar_importance=}"
    #         # )
    #         memberlink_calendar_credit_sum += memberlink._calendar_credit
    #         memberlink_calendar_debt_sum += memberlink._calendar_debt

    #         # print(f"{memberlink_calendar_importance_sum=}")
    # assert memberlink_calendar_credit_sum == 1.0
    # assert memberlink_calendar_debt_sum > 0.9999999
    # assert memberlink_calendar_debt_sum < 1.00000001

    assert (
        rico_memberlink._calendar_credit
        + carm_memberlink._calendar_credit
        + patr_memberlink._calendar_credit
        + selena_memberlink._calendar_credit
        == 1.0
    )
    assert (
        rico_memberlink._calendar_debt
        + carm_memberlink._calendar_debt
        + patr_memberlink._calendar_debt
        + selena_memberlink._calendar_debt
        > 0.9999999
    )
    assert (
        rico_memberlink._calendar_debt
        + carm_memberlink._calendar_debt
        + patr_memberlink._calendar_debt
        + selena_memberlink._calendar_debt
        < 1.0
    )


def test_calendar_get_idea_list_CorrectlySetsMemberUnitCalendarImportance():
    # GIVEN
    prom_text = "prom"
    cx = CalendarUnit(_owner=prom_text)
    swim_text = "swim"
    cx.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(rico_text)))
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(carm_text)))
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(patr_text)))
    bl_rico = grouplink_shop(name=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = grouplink_shop(name=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = grouplink_shop(name=patr_text, creditor_weight=10, debtor_weight=5)
    cx._idearoot._kids[swim_text].set_grouplink(grouplink=bl_rico)
    cx._idearoot._kids[swim_text].set_grouplink(grouplink=bl_carm)
    cx._idearoot._kids[swim_text].set_grouplink(grouplink=bl_patr)

    rico_memberunit = cx._members.get(rico_text)
    carm_memberunit = cx._members.get(carm_text)
    patr_memberunit = cx._members.get(patr_text)

    assert rico_memberunit._calendar_credit is None
    assert rico_memberunit._calendar_debt is None
    assert carm_memberunit._calendar_credit is None
    assert carm_memberunit._calendar_debt is None
    assert patr_memberunit._calendar_credit is None
    assert patr_memberunit._calendar_debt is None

    # WHEN
    cx.set_calendar_metrics()

    # THEN
    memberunit_calendar_credit_sum = 0.0
    memberunit_calendar_debt_sum = 0.0

    assert rico_memberunit._calendar_credit == 0.5
    assert rico_memberunit._calendar_debt == 0.8
    assert carm_memberunit._calendar_credit == 0.25
    assert carm_memberunit._calendar_debt == 0.1
    assert patr_memberunit._calendar_credit == 0.25
    assert patr_memberunit._calendar_debt == 0.1

    assert (
        rico_memberunit._calendar_credit
        + carm_memberunit._calendar_credit
        + patr_memberunit._calendar_credit
        == 1.0
    )
    assert (
        rico_memberunit._calendar_debt
        + carm_memberunit._calendar_debt
        + patr_memberunit._calendar_debt
        == 1.0
    )

    # for memberunit in cx._members.values():
    #     assert memberunit._calendar_credit != None
    #     assert memberunit._calendar_credit in [0.25, 0.5]
    #     assert memberunit._calendar_debt != None
    #     assert memberunit._calendar_debt in [0.8, 0.1]
    #     # print(
    #     #     f"{group.name=} {memberunit._calendar_creditor=} {group._calendar_creditor=}"
    #     # )
    #     print(f"{memberunit.name=} {memberunit._calendar_credit=} {memberunit._calendar_debt=} ")
    #     # print(f"{memberunit_calendar_credit_sum=}")
    #     # print(f"{memberunit_calendar_debt_sum=}")
    #     memberunit_calendar_credit_sum += memberunit._calendar_credit
    #     memberunit_calendar_debt_sum += memberunit._calendar_debt

    # assert memberunit_calendar_credit_sum == 1.0
    # assert memberunit_calendar_debt_sum > 0.9999999
    # assert memberunit_calendar_debt_sum < 1.00000001

    # WHEN another action, make sure metrics are as expected
    selena_text = "selena"
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(selena_text)))
    cx._idearoot.set_grouplink(
        grouplink=grouplink_shop(name=selena_text, creditor_weight=20, debtor_weight=10)
    )
    cx.set_calendar_metrics()

    # THEN
    selena_memberunit = cx._members.get(selena_text)

    assert rico_memberunit._calendar_credit != 0.5
    assert rico_memberunit._calendar_debt != 0.8
    assert carm_memberunit._calendar_credit != 0.25
    assert carm_memberunit._calendar_debt != 0.1
    assert patr_memberunit._calendar_credit != 0.25
    assert patr_memberunit._calendar_debt != 0.1
    assert selena_memberunit._calendar_credit != None
    assert selena_memberunit._calendar_debt != None

    assert (
        rico_memberunit._calendar_credit
        + carm_memberunit._calendar_credit
        + patr_memberunit._calendar_credit
        < 1.0
    )
    assert (
        rico_memberunit._calendar_credit
        + carm_memberunit._calendar_credit
        + patr_memberunit._calendar_credit
        + selena_memberunit._calendar_credit
        == 1.0
    )
    assert (
        rico_memberunit._calendar_debt
        + carm_memberunit._calendar_debt
        + patr_memberunit._calendar_debt
        < 1.0
    )
    assert (
        rico_memberunit._calendar_debt
        + carm_memberunit._calendar_debt
        + patr_memberunit._calendar_debt
        + selena_memberunit._calendar_debt
        == 1.0
    )

    # memberunit_calendar_credit_sum = 0.0
    # memberunit_calendar_debt_sum = 0.0

    # for memberunit in cx._members.values():
    #     assert memberunit._calendar_credit != None
    #     assert memberunit._calendar_credit not in [0.25, 0.5]
    #     assert memberunit._calendar_debt != None
    #     assert memberunit._calendar_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.name=} {memberunit._calendar_creditor=} {group._calendar_creditor=}"
    #     # )
    #     print(f"{memberunit.name=} {memberunit._calendar_credit=} {memberunit._calendar_debt=} ")
    #     # print(f"{memberunit_calendar_credit_sum=}")
    #     # print(f"{memberunit_calendar_debt_sum=}")
    #     memberunit_calendar_credit_sum += memberunit._calendar_credit
    #     memberunit_calendar_debt_sum += memberunit._calendar_debt

    # assert memberunit_calendar_credit_sum == 1.0
    # assert memberunit_calendar_debt_sum > 0.9999999
    # assert memberunit_calendar_debt_sum < 1.00000001


def test_calendar_get_idea_list_CorrectlySetsPartGroupedLWMemberUnitCalendarImportance():
    # GIVEN
    prom_text = "prom"
    cx = CalendarUnit(_owner=prom_text)
    swim_text = "swim"
    cx.add_idea(idea_kid=IdeaKid(_label=swim_text), walk=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(rico_text)))
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(carm_text)))
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(patr_text)))
    bl_rico = grouplink_shop(name=rico_text, creditor_weight=20, debtor_weight=40)
    bl_carm = grouplink_shop(name=carm_text, creditor_weight=10, debtor_weight=5)
    bl_patr = grouplink_shop(name=patr_text, creditor_weight=10, debtor_weight=5)
    cx._idearoot._kids[swim_text].set_grouplink(grouplink=bl_rico)
    cx._idearoot._kids[swim_text].set_grouplink(grouplink=bl_carm)
    cx._idearoot._kids[swim_text].set_grouplink(grouplink=bl_patr)

    # no grouplinks attached to this one
    hunt_text = "hunt"
    cx.add_idea(idea_kid=IdeaKid(_label=hunt_text, _weight=3), walk=prom_text)

    assert cx._idearoot._grouplinks is None

    # WHEN
    cx.set_calendar_metrics()

    # THEN
    rico_groupunit = cx._groups.get(rico_text)
    carm_groupunit = cx._groups.get(carm_text)
    patr_groupunit = cx._groups.get(patr_text)
    assert rico_groupunit._calendar_credit != 0.5
    assert rico_groupunit._calendar_debt != 0.8
    assert carm_groupunit._calendar_credit != 0.25
    assert carm_groupunit._calendar_debt != 0.1
    assert patr_groupunit._calendar_credit != 0.25
    assert patr_groupunit._calendar_debt != 0.1
    assert (
        rico_groupunit._calendar_credit
        + carm_groupunit._calendar_credit
        + patr_groupunit._calendar_credit
        == 0.25
    )
    assert (
        rico_groupunit._calendar_debt
        + carm_groupunit._calendar_debt
        + patr_groupunit._calendar_debt
        == 0.25
    )

    # groupunit_calendar_credit_sum = 0.0
    # groupunit_calendar_debt_sum = 0.0
    # for groupunit in cx._groups.values():
    #     assert groupunit._calendar_credit != None
    #     assert groupunit._calendar_credit not in [0.25, 0.5]
    #     assert groupunit._calendar_debt != None
    #     assert groupunit._calendar_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.name=} {groupunit._calendar_creditor=} {group._calendar_creditor=}"
    #     # )
    #     print(f"{groupunit.name=} {groupunit._calendar_credit=} {groupunit._calendar_debt=} ")
    #     # print(f"{groupunit_calendar_credit_sum=}")
    #     # print(f"{groupunit_calendar_debt_sum=}")
    #     groupunit_calendar_credit_sum += groupunit._calendar_credit
    #     groupunit_calendar_debt_sum += groupunit._calendar_debt
    # assert groupunit_calendar_credit_sum == 0.25
    # assert groupunit_calendar_debt_sum == 0.25

    rico_memberunit = cx._members.get(rico_text)
    carm_memberunit = cx._members.get(carm_text)
    patr_memberunit = cx._members.get(patr_text)

    assert rico_memberunit._calendar_credit == 0.375
    assert rico_memberunit._calendar_debt == 0.45
    assert carm_memberunit._calendar_credit == 0.3125
    assert carm_memberunit._calendar_debt == 0.275
    assert patr_memberunit._calendar_credit == 0.3125
    assert patr_memberunit._calendar_debt == 0.275

    assert (
        rico_memberunit._calendar_credit
        + carm_memberunit._calendar_credit
        + patr_memberunit._calendar_credit
        == 1.0
    )
    assert (
        rico_memberunit._calendar_debt
        + carm_memberunit._calendar_debt
        + patr_memberunit._calendar_debt
        == 1.0
    )

    # memberunit_calendar_credit_sum = 0.0
    # memberunit_calendar_debt_sum = 0.0
    # for memberunit in cx._members.values():
    #     assert memberunit._calendar_credit != None
    #     assert memberunit._calendar_credit not in [0.25, 0.5]
    #     assert memberunit._calendar_debt != None
    #     assert memberunit._calendar_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.name=} {memberunit._calendar_creditor=} {group._calendar_creditor=}"
    #     # )
    #     print(f"{memberunit.name=} {memberunit._calendar_credit=} {memberunit._calendar_debt=} ")
    #     # print(f"{memberunit_calendar_credit_sum=}")
    #     # print(f"{memberunit_calendar_debt_sum=}")
    #     memberunit_calendar_credit_sum += memberunit._calendar_credit
    #     memberunit_calendar_debt_sum += memberunit._calendar_debt
    # assert memberunit_calendar_credit_sum == 1.0
    # assert memberunit_calendar_debt_sum > 0.9999999
    # assert memberunit_calendar_debt_sum < 1.00000001


def test_calendar_get_idea_list_WithAllMembersWeighted():
    # GIVEN
    cx = CalendarUnit(_owner="prom")
    cx.add_idea(idea_kid=IdeaKid(_label="swim"), walk="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.set_memberunit(
        memberunit=memberunit_shop(name=MemberName(rico_text), creditor_weight=8)
    )
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(carm_text)))
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(patr_text)))
    rico_memberunit = cx._members.get(rico_text)
    carm_memberunit = cx._members.get(carm_text)
    patr_memberunit = cx._members.get(patr_text)
    assert rico_memberunit._calendar_credit is None
    assert rico_memberunit._calendar_debt is None
    assert carm_memberunit._calendar_credit is None
    assert carm_memberunit._calendar_debt is None
    assert patr_memberunit._calendar_credit is None
    assert patr_memberunit._calendar_debt is None

    # WHEN
    cx.set_calendar_metrics()

    # THEN
    assert (
        rico_memberunit._calendar_credit
        + carm_memberunit._calendar_credit
        + patr_memberunit._calendar_credit
        == 1.0
    )
    assert (
        rico_memberunit._calendar_debt
        + carm_memberunit._calendar_debt
        + patr_memberunit._calendar_debt
        == 1.0
    )
    # memberunit_calendar_credit_sum = 0.0
    # memberunit_calendar_debt_sum = 0.0
    # for memberunit in cx._members.values():
    #     assert memberunit._calendar_credit != None
    #     assert memberunit._calendar_credit not in [0.25, 0.5]
    #     assert memberunit._calendar_debt != None
    #     assert memberunit._calendar_debt not in [0.8, 0.1]
    #     # print(
    #     #     f"{group.name=} {memberunit._calendar_creditor=} {group._calendar_creditor=}"
    #     # )
    #     print(f"{memberunit.name=} {memberunit._calendar_credit=} {memberunit._calendar_debt=} ")
    #     # print(f"{memberunit_calendar_credit_sum=}")
    #     # print(f"{memberunit_calendar_debt_sum=}")
    #     memberunit_calendar_credit_sum += memberunit._calendar_credit
    #     memberunit_calendar_debt_sum += memberunit._calendar_debt
    # assert memberunit_calendar_credit_sum == 1.0
    # assert memberunit_calendar_debt_sum > 0.9999999
    # assert memberunit_calendar_debt_sum < 1.00000001


def clear_all_memberunits_groupunits_calendar_agenda_credit_debt(cx: CalendarUnit):
    # DELETE calendar_agenda_debt and calendar_agenda_credit
    for groupunit_x in cx._groups.values():
        groupunit_x.reset_calendar_credit_debt()
        # for memberlink_x in groupunit_x._members.values():
        #     print(f"{groupunit_x.name=} {memberlink_x.creditor_weight=}  {memberlink_x._calendar_credit:.6f} {memberlink_x.debtor_weight=} {memberlink_x._calendar_debt:.6f} {memberlink_x.name=} ")

    # DELETE calendar_agenda_debt and calendar_agenda_credit
    for memberunit_x in cx._members.values():
        memberunit_x.reset_calendar_credit_debt()


# sourcery skip: no-loop-in-tests
# sourcery skip: no-conditionals-in-tests
def test_calendar_agenda_credit_debt_IsCorrectlySet():
    # GIVEN
    cx = examples_calendar_v001_with_large_agenda()
    clear_all_memberunits_groupunits_calendar_agenda_credit_debt(cx=cx)

    # TEST calendar_agenda_debt and calendar_agenda_credit are empty
    sum_groupunit_calendar_agenda_credit = 0
    sum_groupunit_calendar_agenda_debt = 0
    sum_memberlink_calendar_agenda_credit = 0
    sum_memberlink_calendar_agenda_debt = 0
    for groupunit_x in cx._groups.values():
        # print(f"{memberunit.name=}")
        sum_groupunit_calendar_agenda_credit += groupunit_x._calendar_agenda_credit
        sum_groupunit_calendar_agenda_debt += groupunit_x._calendar_agenda_debt
        for memberlink_x in groupunit_x._members.values():
            sum_memberlink_calendar_agenda_credit += (
                memberlink_x._calendar_agenda_credit
            )
            sum_memberlink_calendar_agenda_debt += memberlink_x._calendar_agenda_debt

    assert sum_groupunit_calendar_agenda_credit == 0
    assert sum_groupunit_calendar_agenda_debt == 0
    assert sum_memberlink_calendar_agenda_credit == 0
    assert sum_memberlink_calendar_agenda_debt == 0

    # TEST calendar_agenda_debt and calendar_agenda_credit are empty
    sum_memberunit_calendar_agenda_credit = 0
    sum_memberunit_calendar_agenda_debt = 0
    sum_memberunit_calendar_agenda_ratio_credit = 0
    sum_memberunit_calendar_agenda_ratio_debt = 0
    for memberunit in cx._members.values():
        # print(f"{memberunit.name=}")
        sum_memberunit_calendar_agenda_credit += memberunit._calendar_agenda_credit
        sum_memberunit_calendar_agenda_debt += memberunit._calendar_agenda_debt
        sum_memberunit_calendar_agenda_ratio_credit += (
            memberunit._calendar_agenda_ratio_credit
        )
        sum_memberunit_calendar_agenda_ratio_debt += (
            memberunit._calendar_agenda_ratio_debt
        )

    assert sum_memberunit_calendar_agenda_credit == 0
    assert sum_memberunit_calendar_agenda_debt == 0
    assert sum_memberunit_calendar_agenda_ratio_credit == 0
    assert sum_memberunit_calendar_agenda_ratio_debt == 0

    # WHEN
    agenda_list = cx.get_agenda_items()

    # THEN
    assert len(agenda_list) == 68
    sum_calendar_agenda_importance = 0
    agenda_no_grouplines_count = 0
    agenda_yes_grouplines_count = 0
    agenda_no_grouplines_calendar_i_sum = 0
    agenda_yes_grouplines_calendar_i_sum = 0
    for agenda_item in agenda_list:
        sum_calendar_agenda_importance += agenda_item._calendar_importance
        if agenda_item._grouplines == {}:
            agenda_no_grouplines_count += 1
            agenda_no_grouplines_calendar_i_sum += agenda_item._calendar_importance
        else:
            agenda_yes_grouplines_count += 1
            agenda_yes_grouplines_calendar_i_sum += agenda_item._calendar_importance
        # print(f"idea importance: {agenda_item._calendar_importance:.7f} {sum_calendar_agenda_importance:.5f} {agenda_item._label=} ")
        # print(f"{agenda_item.get_road()}")
    print(f"{sum_calendar_agenda_importance=}")
    assert agenda_no_grouplines_count == 20
    assert agenda_yes_grouplines_count == 48
    assert agenda_no_grouplines_calendar_i_sum == 0.00447826215370075
    assert agenda_yes_grouplines_calendar_i_sum == 0.0027152834170378025
    x2 = agenda_no_grouplines_calendar_i_sum + agenda_yes_grouplines_calendar_i_sum
    e10 = 0.0000000001
    assert abs(x2 - sum_calendar_agenda_importance) < e10

    assert sum_calendar_agenda_importance == 0.007193545570738553

    sum_groupunit_calendar_agenda_credit = 0
    sum_groupunit_calendar_agenda_debt = 0
    sum_memberlink_calendar_agenda_credit = 0
    sum_memberlink_calendar_agenda_debt = 0
    memberlink_count = 0
    for groupunit_x in cx._groups.values():
        # print(f"{memberunit.name=}")
        sum_groupunit_calendar_agenda_credit += groupunit_x._calendar_agenda_credit
        sum_groupunit_calendar_agenda_debt += groupunit_x._calendar_agenda_debt
        for memberlink_x in groupunit_x._members.values():
            sum_memberlink_calendar_agenda_credit += (
                memberlink_x._calendar_agenda_credit
            )
            sum_memberlink_calendar_agenda_debt += memberlink_x._calendar_agenda_debt
            memberlink_count += 1

    assert memberlink_count == 81
    x_sum = 0.0027152834170378025
    assert sum_groupunit_calendar_agenda_credit == x_sum
    assert sum_groupunit_calendar_agenda_debt == x_sum
    assert sum_memberlink_calendar_agenda_credit == x_sum
    assert sum_memberlink_calendar_agenda_debt == x_sum
    assert (
        abs(agenda_yes_grouplines_calendar_i_sum - sum_groupunit_calendar_agenda_credit)
        < e10
    )

    sum_memberunit_calendar_agenda_credit = 0
    sum_memberunit_calendar_agenda_debt = 0
    sum_memberunit_calendar_agenda_ratio_credit = 0
    sum_memberunit_calendar_agenda_ratio_debt = 0
    for memberunit in cx._members.values():
        assert memberunit._calendar_credit != None
        assert memberunit._calendar_credit not in [0.25, 0.5]
        assert memberunit._calendar_debt != None
        assert memberunit._calendar_debt not in [
            0.8,
            0.1,
        ]  # print(f"{memberunit.name=}")
        sum_memberunit_calendar_agenda_credit += memberunit._calendar_agenda_credit
        sum_memberunit_calendar_agenda_debt += memberunit._calendar_agenda_debt
        sum_memberunit_calendar_agenda_ratio_credit += (
            memberunit._calendar_agenda_ratio_credit
        )
        sum_memberunit_calendar_agenda_ratio_debt += (
            memberunit._calendar_agenda_ratio_debt
        )

    assert (
        abs(sum_memberunit_calendar_agenda_credit - sum_calendar_agenda_importance)
        < e10
    )
    assert (
        abs(sum_memberunit_calendar_agenda_debt - sum_calendar_agenda_importance) < e10
    )
    assert abs(sum_memberunit_calendar_agenda_ratio_credit - 1) < e10
    assert abs(sum_memberunit_calendar_agenda_ratio_debt - 1) < e10

    # memberunit_calendar_credit_sum = 0.0
    # memberunit_calendar_debt_sum = 0.0

    # assert memberunit_calendar_credit_sum == 1.0
    # assert memberunit_calendar_debt_sum > 0.9999999
    # assert memberunit_calendar_debt_sum < 1.00000001


def test_calendar_agenda_ratio_credit_debt_IsCorrectlySetWhenAgendaIsEmpty():
    # GIVEN
    owner_text = "Noa"
    cx = CalendarUnit(_owner=owner_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    rico_member = memberunit_shop(name=rico_text, creditor_weight=0.5, debtor_weight=2)
    carm_member = memberunit_shop(name=carm_text, creditor_weight=1.5, debtor_weight=3)
    patr_member = memberunit_shop(name=patr_text, creditor_weight=8, debtor_weight=5)
    cx.set_memberunit(memberunit=rico_member)
    cx.set_memberunit(memberunit=carm_member)
    cx.set_memberunit(memberunit=patr_member)
    cx_rico_member = cx._members.get(rico_text)
    cx_carm_member = cx._members.get(carm_text)
    cx_patr_member = cx._members.get(patr_text)

    assert cx_rico_member._calendar_agenda_credit in [0, None]
    assert cx_rico_member._calendar_agenda_debt in [0, None]
    assert cx_carm_member._calendar_agenda_credit in [0, None]
    assert cx_carm_member._calendar_agenda_debt in [0, None]
    assert cx_patr_member._calendar_agenda_credit in [0, None]
    assert cx_patr_member._calendar_agenda_debt in [0, None]
    assert cx_rico_member._calendar_agenda_ratio_credit != 0.05
    assert cx_rico_member._calendar_agenda_ratio_debt != 0.2
    assert cx_carm_member._calendar_agenda_ratio_credit != 0.15
    assert cx_carm_member._calendar_agenda_ratio_debt != 0.3
    assert cx_patr_member._calendar_agenda_ratio_credit != 0.8
    assert cx_patr_member._calendar_agenda_ratio_debt != 0.5

    # WHEN
    cx.set_calendar_metrics()

    # THEN
    assert cx_rico_member._calendar_agenda_credit == 0
    assert cx_rico_member._calendar_agenda_debt == 0
    assert cx_carm_member._calendar_agenda_credit == 0
    assert cx_carm_member._calendar_agenda_debt == 0
    assert cx_patr_member._calendar_agenda_credit == 0
    assert cx_patr_member._calendar_agenda_debt == 0
    assert cx_rico_member._calendar_agenda_ratio_credit == 0.05
    assert cx_rico_member._calendar_agenda_ratio_debt == 0.2
    assert cx_carm_member._calendar_agenda_ratio_credit == 0.15
    assert cx_carm_member._calendar_agenda_ratio_debt == 0.3
    assert cx_patr_member._calendar_agenda_ratio_credit == 0.8
    assert cx_patr_member._calendar_agenda_ratio_debt == 0.5


def test_calendar_get_member_groups_returnsCorrectData():
    cx = CalendarUnit(_owner="prom")
    cx.add_idea(idea_kid=IdeaKid(_label="swim"), walk="prom")
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(rico_text)))
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(carm_text)))
    cx.set_memberunit(memberunit=memberunit_shop(name=MemberName(patr_text)))

    carmen_group_list = cx.get_member_groups(member_name=carm_text)
    assert carmen_group_list == [carm_text]

    swimmers = "swimmers"
    carmen_member_dict = {MemberName(carm_text): memberlink_shop(name=carm_text)}
    swim_group = groupunit_shop(name=swimmers, _members=carmen_member_dict)
    cx._groups[swim_group.name] = swim_group
    carmen_group_list = cx.get_member_groups(member_name=carm_text)
    assert carmen_group_list == [carm_text, swimmers]


def test_calendar_MemberUnit_CorrectlyCreatesNewName():
    # GIVEN
    cx = CalendarUnit(_owner="prom")
    rico_text = "rico"
    cx.add_memberunit(name=rico_text, uid=61, creditor_weight=13)
    cx.add_memberunit(name="carmen", uid=5)
    cx.add_memberunit(name="patrick", creditor_weight=17)
    assert len(cx._members) == 3
    assert cx._members.get(rico_text) != None
    assert cx._members.get(rico_text).creditor_weight == 13
    assert len(cx._groups) == 3
    assert cx._groups.get(rico_text) != None
    assert cx._groups.get(rico_text)._single_member == True

    # WHEN
    beto_text = "beta"
    cx.edit_memberunit_name(
        old_name=rico_text,
        new_name=beto_text,
        allow_member_overwite=False,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert cx._members.get(beto_text) != None
    assert cx._members.get(beto_text).creditor_weight == 13
    assert cx._members.get(rico_text) is None
    assert len(cx._members) == 3
    assert len(cx._groups) == 3
    assert cx._groups.get(rico_text) is None
    assert cx._groups.get(beto_text) != None
    assert cx._groups.get(beto_text)._single_member == True


def test_calendar_MemberUnit_raiseErrorNewNamePreviouslyExists():
    # GIVEN
    sx = CalendarUnit(_owner="prom")
    rico_text = "rico"
    sx.add_memberunit(name=rico_text, uid=61, creditor_weight=13)
    carmen_text = "carmen"
    sx.add_memberunit(name=carmen_text, uid=5)
    sx.add_memberunit(name="patrick", creditor_weight=17)
    assert len(sx._members) == 3
    assert sx._members.get(rico_text) != None
    assert sx._members.get(rico_text).creditor_weight == 13
    assert len(sx._groups) == 3
    assert sx._groups.get(rico_text) != None
    assert sx._groups.get(rico_text)._single_member == True

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sx.edit_memberunit_name(
            old_name=rico_text,
            new_name=carmen_text,
            allow_member_overwite=False,
            allow_nonsingle_group_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Member '{rico_text}' change to '{carmen_text}' failed since '{carmen_text}' exists."
    )


def test_calendar_MemberUnit_CorrectlyChangesGroupUnitMemberLinks():
    # GIVEN
    prom_text = "prom"
    cx = CalendarUnit(_owner=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.add_memberunit(name=rico_text, uid=61, creditor_weight=13)
    cx.add_memberunit(name=carm_text, uid=5)
    cx.add_memberunit(name=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_member_dict = {MemberName(carm_text): memberlink_shop(name=carm_text)}
    swim_group = groupunit_shop(name=swim_text, _members=carmen_member_dict)
    swim_group.set_memberlink(
        memberlink=memberlink_shop(name=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_memberlink(
        memberlink=memberlink_shop(name=rico_text, creditor_weight=7, debtor_weight=30)
    )
    cx.set_groupunit(groupunit=swim_group)

    swim_group = cx._groups.get(swim_text)
    assert len(swim_group._members) == 2
    assert swim_group._members.get(rico_text) != None
    assert swim_group._members.get(rico_text).creditor_weight == 7
    assert swim_group._members.get(rico_text).debtor_weight == 30

    # WHEN
    beto_text = "beta"
    cx.edit_memberunit_name(
        old_name=rico_text,
        new_name=beto_text,
        allow_member_overwite=False,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert swim_group._members.get(beto_text) != None
    assert swim_group._members.get(beto_text).creditor_weight == 7
    assert swim_group._members.get(beto_text).debtor_weight == 30
    assert swim_group._members.get(rico_text) is None
    assert len(swim_group._members) == 2


def test_calendar_MemberUnit_CorrectlyMergesNames():
    # GIVEN
    prom_text = "prom"
    cx = CalendarUnit(_owner=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.add_memberunit(name=rico_text, uid=61, creditor_weight=13)
    cx.add_memberunit(name=carm_text, uid=5, creditor_weight=3)
    cx.add_memberunit(name=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_member_dict = {MemberName(carm_text): memberlink_shop(name=carm_text)}
    swim_group = groupunit_shop(name=swim_text, _members=carmen_member_dict)
    swim_group.set_memberlink(
        memberlink=memberlink_shop(name=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_memberlink(
        memberlink=memberlink_shop(name=rico_text, creditor_weight=7, debtor_weight=30)
    )
    cx.set_groupunit(groupunit=swim_group)

    assert len(cx._members) == 3
    assert cx._members.get(rico_text) != None
    assert cx._members.get(rico_text).creditor_weight == 13
    assert cx._members.get(carm_text) != None
    assert cx._members.get(carm_text).creditor_weight == 3

    # WHEN / THEN
    cx.edit_memberunit_name(
        old_name=rico_text,
        new_name=carm_text,
        allow_member_overwite=True,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert cx._members.get(carm_text) != None
    assert cx._members.get(carm_text).creditor_weight == 16
    assert cx._members.get(rico_text) is None
    assert len(cx._members) == 2


def test_calendar_MemberUnit_CorrectlyMergesGroupUnitMemberLinks():
    # GIVEN
    # GIVEN
    prom_text = "prom"
    cx = CalendarUnit(_owner=prom_text)
    rico_text = "rico"
    carm_text = "carmen"
    patr_text = "patrick"
    cx.add_memberunit(name=rico_text, uid=61, creditor_weight=13)
    cx.add_memberunit(name=carm_text, uid=5)
    cx.add_memberunit(name=patr_text, creditor_weight=17)

    swim_text = "swimmers"
    carmen_member_dict = {MemberName(carm_text): memberlink_shop(name=carm_text)}
    swim_group = groupunit_shop(name=swim_text, _members=carmen_member_dict)
    swim_group.set_memberlink(
        memberlink=memberlink_shop(name=carm_text, creditor_weight=5, debtor_weight=18)
    )
    swim_group.set_memberlink(
        memberlink=memberlink_shop(name=rico_text, creditor_weight=7, debtor_weight=30)
    )
    cx.set_groupunit(groupunit=swim_group)

    swim_group = cx._groups.get(swim_text)
    assert len(swim_group._members) == 2
    assert swim_group._members.get(rico_text) != None
    assert swim_group._members.get(rico_text).creditor_weight == 7
    assert swim_group._members.get(rico_text).debtor_weight == 30
    assert swim_group._members.get(carm_text) != None
    assert swim_group._members.get(carm_text).creditor_weight == 5
    assert swim_group._members.get(carm_text).debtor_weight == 18

    # WHEN
    cx.edit_memberunit_name(
        old_name=rico_text,
        new_name=carm_text,
        allow_member_overwite=True,
        allow_nonsingle_group_overwrite=False,
    )

    # THEN
    assert swim_group._members.get(carm_text) != None
    assert swim_group._members.get(carm_text).creditor_weight == 12
    assert swim_group._members.get(carm_text).debtor_weight == 48
    assert swim_group._members.get(rico_text) is None
    assert len(swim_group._members) == 1


def test_calendar_MemberUnit_raiseErrorNewNameGroupUnitPreviouslyExists():
    # GIVEN
    sx = CalendarUnit(_owner="prom")
    rico_text = "rico"
    sx.add_memberunit(name=rico_text, uid=61, creditor_weight=13)
    anna_text = "anna"
    sx.add_memberunit(name=anna_text, uid=71, creditor_weight=17)
    carmen_text = "carmen"
    carmen_group = groupunit_shop(name=carmen_text)
    carmen_group.set_memberlink(memberlink=memberlink_shop(name=rico_text))
    carmen_group.set_memberlink(memberlink=memberlink_shop(name=anna_text))
    sx.set_groupunit(groupunit=carmen_group)
    assert len(sx._groups) == 3
    assert sx._members.get(carmen_text) is None
    assert sx._groups.get(carmen_text)._single_member == False
    assert len(sx._groups.get(carmen_text)._members) == 2

    # WHEN / THEN
    with pytest_raises(Exception) as excinfo:
        sx.edit_memberunit_name(
            old_name=rico_text,
            new_name=carmen_text,
            allow_member_overwite=False,
            allow_nonsingle_group_overwrite=False,
        )
    assert (
        str(excinfo.value)
        == f"Member '{rico_text}' change to '{carmen_text}' failed since non-single group '{carmen_text}' exists."
    )


def test_calendar_MemberUnit_CorrectlyOverwriteNewNameGroupUnit():
    # GIVEN
    sx = CalendarUnit(_owner="prom")
    rico_text = "rico"
    sx.add_memberunit(name=rico_text, uid=61, creditor_weight=13)
    anna_text = "anna"
    sx.add_memberunit(name=anna_text, uid=71, creditor_weight=17)
    carmen_text = "carmen"
    carmen_group = groupunit_shop(name=carmen_text)
    carmen_group.set_memberlink(
        memberlink=memberlink_shop(name=rico_text, creditor_weight=3)
    )
    carmen_group.set_memberlink(
        memberlink=memberlink_shop(name=anna_text, creditor_weight=5)
    )
    sx.set_groupunit(groupunit=carmen_group)
    assert len(sx._groups) == 3
    assert sx._members.get(rico_text) != None
    assert sx._members.get(carmen_text) is None
    assert sx._groups.get(carmen_text)._single_member == False
    assert len(sx._groups.get(carmen_text)._members) == 2
    assert sx._groups.get(carmen_text)._members.get(anna_text).creditor_weight == 5
    assert sx._groups.get(carmen_text)._members.get(rico_text).creditor_weight == 3

    # WHEN
    sx.edit_memberunit_name(
        old_name=rico_text,
        new_name=carmen_text,
        allow_member_overwite=False,
        allow_nonsingle_group_overwrite=True,
    )

    assert len(sx._groups) == 2
    assert sx._members.get(rico_text) is None
    assert sx._members.get(carmen_text) != None
    assert sx._groups.get(carmen_text)._single_member == True
    assert len(sx._groups.get(carmen_text)._members) == 1
    assert sx._groups.get(carmen_text)._members.get(rico_text) is None
    assert sx._groups.get(carmen_text)._members.get(carmen_text).creditor_weight == 1


def test_calendar_set_all_memberunits_uids_unique_CorrectlySetsEmptyGroupUIDs():
    # GIVEN
    owner_text = "Noa"
    sx = CalendarUnit(_owner=owner_text)
    sx.set_members_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_memberunit(memberunit=memberunit_shop(name=swim_text))
    sx.set_memberunit(memberunit=memberunit_shop(name=walk_text))
    sx.set_memberunit(memberunit=memberunit_shop(name=fly_text))
    assert sx._members[swim_text].uid is None
    assert sx._members[walk_text].uid is None
    assert sx._members[fly_text].uid is None

    # WHEN
    sx.set_all_memberunits_uids_unique()

    # THEN
    assert sx._members[swim_text].uid != None
    assert sx._members[walk_text].uid != None
    assert sx._members[fly_text].uid != None


def test_calendar_set_all_memberunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    owner_text = "Noa"
    sx = CalendarUnit(_owner=owner_text)
    sx.set_members_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_memberunit(memberunit=memberunit_shop(name=swim_text, uid=3))
    sx.set_memberunit(memberunit=memberunit_shop(name=walk_text, uid=3))
    sx.set_memberunit(memberunit=memberunit_shop(name=fly_text))
    assert sx._members[swim_text].uid == 3
    assert sx._members[walk_text].uid == 3
    assert sx._members[fly_text].uid is None

    # WHEN
    sx.set_all_memberunits_uids_unique()

    # THEN
    print(f"{sx._members[swim_text].uid=}")
    print(f"{sx._members[walk_text].uid=}")
    assert sx._members[swim_text].uid != sx._members[walk_text].uid
    assert sx._members[walk_text].uid != 3
    assert sx._members[walk_text].uid != 3
    assert sx._members[fly_text].uid != None


def test_calendar_set_all_memberunits_uids_unique_CorrectlySetsChangesSameGroupUIDs():
    # GIVEN
    owner_text = "Noa"
    sx = CalendarUnit(_owner=owner_text)
    sx.set_members_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_memberunit(memberunit=memberunit_shop(name=swim_text, uid=3))
    sx.set_memberunit(memberunit=memberunit_shop(name=walk_text, uid=3))
    sx.set_memberunit(memberunit=memberunit_shop(name=fly_text))
    assert sx._members[swim_text].uid == 3
    assert sx._members[walk_text].uid == 3
    assert sx._members[fly_text].uid is None

    # WHEN
    sx.set_all_memberunits_uids_unique()

    # THEN
    print(f"{sx._members[swim_text].uid=}")
    print(f"{sx._members[walk_text].uid=}")
    assert sx._members[swim_text].uid != sx._members[walk_text].uid
    assert sx._members[walk_text].uid != 3
    assert sx._members[walk_text].uid != 3
    assert sx._members[fly_text].uid != None


def test_calendar_all_memberunits_uids_are_unique_ReturnsCorrectBoolean():
    # GIVEN
    owner_text = "Noa"
    sx = CalendarUnit(_owner=owner_text)
    sx.set_members_empty_if_null()
    swim_text = "swim"
    walk_text = "walk"
    fly_text = "fly"
    sx.set_memberunit(memberunit=memberunit_shop(name=swim_text, uid=3))
    sx.set_memberunit(memberunit=memberunit_shop(name=walk_text, uid=3))
    sx.set_memberunit(memberunit=memberunit_shop(name=fly_text))
    assert sx._members[swim_text].uid == 3
    assert sx._members[walk_text].uid == 3
    assert sx._members[fly_text].uid is None

    # WHEN1 / THEN
    assert sx.all_memberunits_uids_are_unique() == False

    # WHEN2
    sx.set_memberunit(memberunit=memberunit_shop(name=swim_text, uid=4))

    # THEN
    assert sx.all_memberunits_uids_are_unique() == False

    # WHEN3
    sx.set_memberunit(memberunit=memberunit_shop(name=fly_text, uid=5))

    # THEN
    assert sx.all_memberunits_uids_are_unique()


def test_calendar_get_memberunits_name_list_CorrectlyReturnsListOfMemberUnits():
    # GIVEN
    owner_text = "Noa"
    sx = CalendarUnit(_owner=owner_text)
    sx.set_members_empty_if_null()
    sam_text = "sam"
    will_text = "will"
    fry_text = "fry"
    sx.set_memberunit(memberunit=memberunit_shop(name=sam_text))
    sx.set_memberunit(memberunit=memberunit_shop(name=will_text))
    sx.set_memberunit(memberunit=memberunit_shop(name=fry_text))
    fun_text = "fun people"
    fun_group = groupunit_shop(name=fun_text)
    fun_group.set_memberlink(memberlink=memberlink_shop(name=will_text))
    sx.set_groupunit(groupunit=fun_group)
    assert len(sx._groups) == 4
    assert len(sx._members) == 3

    # WHEN
    memberunit_list_x = sx.get_memberunits_name_list()

    # THEN
    assert len(memberunit_list_x) == 4
    assert memberunit_list_x[0] == ""
    assert memberunit_list_x[1] == fry_text
    assert memberunit_list_x[2] == sam_text
    assert memberunit_list_x[3] == will_text


def test_calendar_set_banking_data_memberunits_CorrectlySetsMemberUnitBankingAttr():
    # GIVEN
    bob_text = "bob"
    ax = CalendarUnit(_owner=bob_text)
    ax.set_members_empty_if_null()
    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "elu"
    ax.set_memberunit(memberunit=memberunit_shop(name=sam_text))
    ax.set_memberunit(memberunit=memberunit_shop(name=wil_text))
    ax.set_memberunit(memberunit=memberunit_shop(name=fry_text))
    assert ax._members.get(sam_text)._bank_tax_paid is None
    assert ax._members.get(sam_text)._bank_tax_diff is None
    assert ax._members.get(wil_text)._bank_tax_paid is None
    assert ax._members.get(wil_text)._bank_tax_diff is None
    assert ax._members.get(fry_text)._bank_tax_paid is None
    assert ax._members.get(fry_text)._bank_tax_diff is None
    elu_memberunit = memberunit_shop(name=elu_text)
    elu_memberunit._bank_tax_paid = 0.003
    elu_memberunit._bank_tax_diff = 0.007
    ax.set_memberunit(memberunit=elu_memberunit)
    assert ax._members.get(elu_text)._bank_tax_paid == 0.003
    assert ax._members.get(elu_text)._bank_tax_diff == 0.007

    river_tmember_sam = RiverTmemberUnit(bob_text, sam_text, 0.209, 0, 0.034)
    river_tmember_wil = RiverTmemberUnit(bob_text, wil_text, 0.501, 0, 0.024)
    river_tmember_fry = RiverTmemberUnit(bob_text, fry_text, 0.111, 0, 0.006)
    river_tmembers = {
        river_tmember_sam.tax_name: river_tmember_sam,
        river_tmember_wil.tax_name: river_tmember_wil,
        river_tmember_fry.tax_name: river_tmember_fry,
    }
    # WHEN
    ax.set_banking_attr_memberunits(river_tmembers=river_tmembers)

    # THEN
    assert ax._members.get(sam_text)._bank_tax_paid == 0.209
    assert ax._members.get(sam_text)._bank_tax_diff == 0.034
    assert ax._members.get(wil_text)._bank_tax_paid == 0.501
    assert ax._members.get(wil_text)._bank_tax_diff == 0.024
    assert ax._members.get(fry_text)._bank_tax_paid == 0.111
    assert ax._members.get(fry_text)._bank_tax_diff == 0.006
    assert ax._members.get(elu_text)._bank_tax_paid is None
    assert ax._members.get(elu_text)._bank_tax_diff is None


def test_get_intersection_of_members_CorrectlyReturnsUnionOfKeysOfTwoDictionarys_scenario1():
    # GIVEN
    bob_text = "bob"
    ax = CalendarUnit(_owner=bob_text)
    ax.set_members_empty_if_null()

    sam_text = "sam"
    wil_text = "wil"
    fry_text = "fry"
    elu_text = "elu"
    ax.set_memberunit(memberunit=memberunit_shop(name=bob_text))
    ax.set_memberunit(memberunit=memberunit_shop(name=sam_text))
    ax.set_memberunit(memberunit=memberunit_shop(name=wil_text))
    ax.set_memberunit(memberunit=memberunit_shop(name=fry_text))

    tx = CalendarUnit()
    tx.set_members_empty_if_null()

    tx.set_memberunit(memberunit=memberunit_shop(name=bob_text))
    tx.set_memberunit(memberunit=memberunit_shop(name=wil_text))
    tx.set_memberunit(memberunit=memberunit_shop(name=fry_text))
    tx.set_memberunit(memberunit=memberunit_shop(name=elu_text))

    # WHEN
    print(f"{len(ax._members)=} {len(tx._members)=}")
    intersection_x = get_intersection_of_members(ax._members, tx._members)

    # THEN
    assert intersection_x == {bob_text: -1, wil_text: -1, fry_text: -1}
