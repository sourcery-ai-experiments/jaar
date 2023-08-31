from src.calendar.required import SuffFactStatusFinder
from pytest import raises as pytest_raises


def test_sufffactstatusfinder_acptfact_nigh_outside_sufffact_range_correctlyReturnsValue():
    # GIVEN / WHEN
    segr_obj = SuffFactStatusFinder(
        acptfact_open=20000,
        acptfact_nigh=29000,
        sufffact_open=1305.0,
        sufffact_nigh=1305.0,
        sufffact_divisor=1440,
    )
    print(f"----\n  {segr_obj.acptfact_open=}  {segr_obj.acptfact_nigh=}")
    print(
        f"  {segr_obj.sufffact_open=}  {segr_obj.sufffact_nigh=}  {segr_obj.sufffact_divisor=}"
    )
    print(
        f"  {segr_obj.acptfact_open=}  {segr_obj.acptfact_nigh=} \tdifference:{segr_obj.acptfact_nigh-segr_obj.acptfact_open}"
    )
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

    # THEN
    # assert segr_obj._acptfact_range_len == 9000
    assert segr_obj.get_acptfact_nigh_mod_div() == 200
    assert segr_obj._task_status


def test_sufffactstatusfinder_correctlyReturnsTaskStatusTrueWhenAcptFactRangeGreaterTacptfactivisor():
    # GIVEN / WHEN
    segr_obj = SuffFactStatusFinder(
        acptfact_open=20000,
        acptfact_nigh=29000,
        sufffact_open=1305.0,
        sufffact_nigh=1305.0,
        sufffact_divisor=1440,
    )
    print(f"----\n  {segr_obj.acptfact_open=}  {segr_obj.acptfact_nigh=}")
    print(
        f"  {segr_obj.sufffact_open=}  {segr_obj.sufffact_nigh=}  {segr_obj.sufffact_divisor=}"
    )
    print(
        f"  {segr_obj.acptfact_open=}  {segr_obj.acptfact_nigh=} \tdifference:{segr_obj.acptfact_nigh-segr_obj.acptfact_open}"
    )
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

    # THEN
    assert segr_obj._acptfact_range_len == 9000
    assert segr_obj._active_status
    assert segr_obj._task_status


def test_sufffactstatusfinder_correctlyReturnsActiveStatus_Scenario01():
    # GIVEN / WHEN
    segr_obj = SuffFactStatusFinder(
        acptfact_open=1300,
        acptfact_nigh=1400,
        sufffact_open=1305.0,
        sufffact_nigh=1305.0,
        sufffact_divisor=1440,
    )
    print(f"----\n  {segr_obj.acptfact_open=}  {segr_obj.acptfact_nigh=}")
    print(
        f"  {segr_obj.sufffact_open=}  {segr_obj.sufffact_nigh=}  {segr_obj.sufffact_divisor=}"
    )
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

    # THEN
    assert segr_obj._active_status
    assert segr_obj._task_status


def test_sufffactstatusfinder_correctlyReturnsActiveStatus_Scenario02():
    # GIVEN / WHEN
    segr_obj = SuffFactStatusFinder(
        acptfact_open=1300,
        acptfact_nigh=1300,
        sufffact_open=1305.0,
        sufffact_nigh=1305.0,
        sufffact_divisor=1440,
    )
    print(f"----\n  {segr_obj.acptfact_open=}  {segr_obj.acptfact_nigh=}")
    print(
        f"  {segr_obj.sufffact_open=}  {segr_obj.sufffact_nigh=}  {segr_obj.sufffact_divisor=}"
    )
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

    # THEN
    assert segr_obj._active_status == False
    assert segr_obj._task_status == False


# def test_sufffactstatusfinder_correctlyReturnsActiveStatus_Scenario03():
#     # GIVEN / WHEN
#     segr_obj = SuffFactStatusFinder(
#         acptfact_open=1063998720,
#         acptfact_nigh=1064130373,
#         sufffact_open=1305.0,
#         sufffact_nigh=1305.0,
#         sufffact_divisor=1440,
#     )
#     print(f"----\n  {segr_obj.acptfact_open=}  {segr_obj.acptfact_nigh=}")
#     print(f"  {segr_obj.sufffact_open=}  {segr_obj.sufffact_nigh=}  {segr_obj.sufffact_divisor=}")
#     print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

#     # THEN
#     assert segr_obj._active_status
#     assert segr_obj._task_status
