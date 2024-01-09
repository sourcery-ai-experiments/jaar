from src.agenda.reason_idea import PremiseStatusFinder
from pytest import raises as pytest_raises


def test_premisestatusfinder_fact_nigh_outside_premise_range_correctlyReturnsValue():
    # GIVEN / WHEN
    segr_obj = PremiseStatusFinder(
        fact_open=20000,
        fact_nigh=29000,
        premise_open=1305.0,
        premise_nigh=1305.0,
        premise_divisor=1440,
    )
    print(f"----\n  {segr_obj.fact_open=}  {segr_obj.fact_nigh=}")
    print(
        f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    )
    print(
        f"  {segr_obj.fact_open=}  {segr_obj.fact_nigh=} \tdifference:{segr_obj.fact_nigh-segr_obj.fact_open}"
    )
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

    # THEN
    # assert segr_obj._fact_range_len == 9000
    assert segr_obj.get_fact_nigh_mod_div() == 200
    assert segr_obj._task_status


def test_premisestatusfinder_correctlyReturnsTaskStatusTrueWhenFactRangeGreaterTfactivisor():
    # GIVEN / WHEN
    segr_obj = PremiseStatusFinder(
        fact_open=20000,
        fact_nigh=29000,
        premise_open=1305.0,
        premise_nigh=1305.0,
        premise_divisor=1440,
    )
    print(f"----\n  {segr_obj.fact_open=}  {segr_obj.fact_nigh=}")
    print(
        f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    )
    print(
        f"  {segr_obj.fact_open=}  {segr_obj.fact_nigh=} \tdifference:{segr_obj.fact_nigh-segr_obj.fact_open}"
    )
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

    # THEN
    assert segr_obj._fact_range_len == 9000
    assert segr_obj._active_status
    assert segr_obj._task_status


def test_premisestatusfinder_correctlyReturnsActiveStatus_Scenario01():
    # GIVEN / WHEN
    segr_obj = PremiseStatusFinder(
        fact_open=1300,
        fact_nigh=1400,
        premise_open=1305.0,
        premise_nigh=1305.0,
        premise_divisor=1440,
    )
    print(f"----\n  {segr_obj.fact_open=}  {segr_obj.fact_nigh=}")
    print(
        f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    )
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

    # THEN
    assert segr_obj._active_status
    assert segr_obj._task_status


def test_premisestatusfinder_correctlyReturnsActiveStatus_Scenario02():
    # GIVEN / WHEN
    segr_obj = PremiseStatusFinder(
        fact_open=1300,
        fact_nigh=1300,
        premise_open=1305.0,
        premise_nigh=1305.0,
        premise_divisor=1440,
    )
    print(f"----\n  {segr_obj.fact_open=}  {segr_obj.fact_nigh=}")
    print(
        f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}"
    )
    print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

    # THEN
    assert segr_obj._active_status == False
    assert segr_obj._task_status == False


# def test_premisestatusfinder_correctlyReturnsActiveStatus_Scenario03():
#     # GIVEN / WHEN
#     segr_obj = PremiseStatusFinder(
#         fact_open=1063998720,
#         fact_nigh=1064130373,
#         premise_open=1305.0,
#         premise_nigh=1305.0,
#         premise_divisor=1440,
#     )
#     print(f"----\n  {segr_obj.fact_open=}  {segr_obj.fact_nigh=}")
#     print(f"  {segr_obj.premise_open=}  {segr_obj.premise_nigh=}  {segr_obj.premise_divisor=}")
#     print(f"  {segr_obj._active_status=}  {segr_obj._task_status=}")

#     # THEN
#     assert segr_obj._active_status
#     assert segr_obj._task_status
