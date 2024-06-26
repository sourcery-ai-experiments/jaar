from src._world.examples.example_worlds import world_v001_with_large_agenda
from src._world.world import worldunit_shop
from src._world.report import (
    get_world_personunits_dataframe,
    get_world_agenda_dataframe,
)


def test_get_world_personunits_dataframe_ReturnsCorrectDataFrame():
    # GIVEN
    luca_world = worldunit_shop()
    luca_world.set_person_credor_pool(500)
    luca_world.set_person_debtor_pool(400)
    todd_text = "Todd"
    todd_credor_weight = 66
    todd_debtor_weight = 77
    luca_world.add_personunit(todd_text, todd_credor_weight, todd_debtor_weight)
    sue_text = "Sue"
    sue_credor_weight = 434
    sue_debtor_weight = 323
    luca_world.add_personunit(sue_text, sue_credor_weight, sue_debtor_weight)

    # WHEN
    x_df = get_world_personunits_dataframe(luca_world)

    # THEN
    personunit_colums = {
        "person_id",
        "credor_weight",
        "debtor_weight",
        "_belieflinks",
        "_world_cred",
        "_world_debt",
        "_world_agenda_cred",
        "_world_agenda_debt",
        "_world_agenda_ratio_cred",
        "_world_agenda_ratio_debt",
        "_credor_operational",
        "_debtor_operational",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_world_meld_order",
        "_treasury_cred_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == personunit_colums
    assert x_df.shape[0] == 2


def test_get_world_personunits_dataframe_ReturnsCorrectEmptyDataFrame():
    # GIVEN
    luca_world = worldunit_shop()

    # WHEN
    x_df = get_world_personunits_dataframe(luca_world)

    # THEN
    personunit_colums = {
        "person_id",
        "credor_weight",
        "debtor_weight",
        "_world_cred",
        "_world_debt",
        "_world_agenda_cred",
        "_world_agenda_debt",
        "_world_agenda_ratio_cred",
        "_world_agenda_ratio_debt",
        "_credor_operational",
        "_debtor_operational",
        "_treasury_due_paid",
        "_treasury_due_diff",
        "_output_world_meld_order",
        "_treasury_cred_score",
        "_treasury_voice_rank",
        "_treasury_voice_hx_lowest_rank",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == personunit_colums
    assert x_df.shape[0] == 0


def test_get_world_agenda_dataframe_ReturnsCorrectDataFrame():
    # GIVEN
    yao_world = world_v001_with_large_agenda()
    week_text = "weekdays"
    week_road = yao_world.make_l1_road(week_text)
    assert len(yao_world.get_agenda_dict()) == 63

    # WHEN
    x_df = get_world_agenda_dataframe(yao_world)
    print(x_df)

    # THEN
    personunit_colums = {
        "owner_id",
        "world_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == personunit_colums
    assert x_df.shape[0] == 63


def test_get_world_agenda_dataframe_ReturnsCorrectEmptyDataFrame():
    # GIVEN
    yao_world = worldunit_shop("Yao")
    assert len(yao_world.get_agenda_dict()) == 0

    # WHEN
    x_df = get_world_agenda_dataframe(yao_world)
    print(x_df)

    # THEN
    personunit_colums = {
        "owner_id",
        "world_importance",
        "_label",
        "_parent_road",
        "_begin",
        "_close",
        "_addin",
        "_denom",
        "_numor",
        "_reest",
    }
    print(f"{set(x_df.columns)=}")

    assert set(x_df.columns) == personunit_colums
