from src.calendar.examples.example_calendars import (
    calendar_v001 as example_calendars_calendar_v001,
)
from src.calendar.member import MemberUnitExternalMetrics


def test_calendar_import_debtor_info_CorrectlyWorks():
    # GIVEN
    calendar_x = example_calendars_calendar_v001()
    jane_text = "Jane Randolph"

    jane_member = calendar_x._members.get(jane_text)
    print(f"Before Member {jane_member.name} {jane_member._debtor_active=} ")
    assert jane_member._debtor_active is None
    assert jane_member._creditor_active is None

    assert sum(
        member_x._creditor_active is None for member_x in calendar_x._members.values()
    ) == len(calendar_x._members)
    assert sum(
        member_x._debtor_active is None for member_x in calendar_x._members.values()
    ) == len(calendar_x._members)

    # WHEN
    jane_debtor_status = True
    jane_creditor_status = True
    jane_metr = MemberUnitExternalMetrics(
        internal_name=jane_text,
        debtor_active=jane_debtor_status,
        creditor_active=jane_creditor_status,
    )
    calendar_x.import_external_memberunit_metrics(jane_metr)

    # THEN
    assert jane_member._debtor_active == jane_debtor_status
    assert jane_member._creditor_active == jane_creditor_status

    assert (
        sum(
            member_x._creditor_active is None
            for member_x in calendar_x._members.values()
        )
        == len(calendar_x._members) - 1
    )
    assert (
        sum(
            member_x._debtor_active is None for member_x in calendar_x._members.values()
        )
        == len(calendar_x._members) - 1
    )
    assert (
        sum(
            member_x._creditor_active != None
            for member_x in calendar_x._members.values()
        )
        == 1
    )
    assert (
        sum(
            member_x._debtor_active != None for member_x in calendar_x._members.values()
        )
        == 1
    )
