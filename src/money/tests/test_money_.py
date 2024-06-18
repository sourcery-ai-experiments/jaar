# from src.agenda.examples.example_agendas import agenda_v001_with_large_intent
# from src.agenda.agenda import agendaunit_shop
from src._instrument.file import save_file
from src._road.jaar_config import get_test_reals_dir as env_dir
from src._instrument.python import get_dict_from_json, get_json_from_dict
from src.money.money import OtherMoneyReport, MoneyUnit
from src.money.examples.money_env import (
    env_dir_setup_cleanup,
    get_bob_othermoneyreport,
    get_sue_texas_userhub,
)


def test_OtherMoneyReport_exists():
    # GIVEN / WHEN
    x_othermoneyreport = OtherMoneyReport()

    # THEN
    assert x_othermoneyreport.other_id is None
    assert x_othermoneyreport.grant_count is None
    assert x_othermoneyreport.grant_amount is None
    assert x_othermoneyreport.grant_rank_num is None
    assert x_othermoneyreport.grant_rank_percent is None
    assert x_othermoneyreport.tax_due_count is None
    assert x_othermoneyreport.tax_due_amount is None
    assert x_othermoneyreport.tax_due_rank_num is None
    assert x_othermoneyreport.tax_due_rank_percent is None
    assert x_othermoneyreport.tax_paid_amount is None
    assert x_othermoneyreport.tax_paid_bool is None
    assert x_othermoneyreport.tax_paid_rank_num is None
    assert x_othermoneyreport.tax_paid_rank_percent is None
    assert x_othermoneyreport.transactions_count is None
    assert x_othermoneyreport.transactions_magnitude is None
    assert x_othermoneyreport.transactions_rank_num is None
    assert x_othermoneyreport.transactions_rank_percent is None


def test_OtherMoneyReport_DoesNotChangeInputs():
    # GIVEN
    bob_other_id = "Bob"
    bob_grant_count = 333
    bob_grant_amount = 333111
    bob_grant_rank_num = 22
    bob_grant_rank_percent = 0.668
    bob_tax_due_count = 444
    bob_tax_due_amount = 444111
    bob_tax_due_rank_num = 55
    bob_tax_due_rank_percent = 0.1111
    bob_tax_paid_amount = 77777
    bob_tax_paid_bool = True
    bob_tax_paid_rank_num = 111
    bob_tax_paid_rank_percent = 0.22222
    bob_transactions_count = 888888
    bob_transactions_magnitude = 9696
    bob_transactions_rank_num = 100
    bob_transactions_rank_percent = 0.99

    # WHEN
    bob_othermoneyreport = OtherMoneyReport(
        other_id=bob_other_id,
        grant_count=bob_grant_count,
        grant_amount=bob_grant_amount,
        grant_rank_num=bob_grant_rank_num,
        grant_rank_percent=bob_grant_rank_percent,
        tax_due_count=bob_tax_due_count,
        tax_due_amount=bob_tax_due_amount,
        tax_due_rank_num=bob_tax_due_rank_num,
        tax_due_rank_percent=bob_tax_due_rank_percent,
        tax_paid_amount=bob_tax_paid_amount,
        tax_paid_bool=bob_tax_paid_bool,
        tax_paid_rank_num=bob_tax_paid_rank_num,
        tax_paid_rank_percent=bob_tax_paid_rank_percent,
        transactions_count=bob_transactions_count,
        transactions_magnitude=bob_transactions_magnitude,
        transactions_rank_num=bob_transactions_rank_num,
        transactions_rank_percent=bob_transactions_rank_percent,
    )

    # THEN
    assert bob_othermoneyreport.other_id == bob_other_id
    assert bob_othermoneyreport.grant_count == bob_grant_count
    assert bob_othermoneyreport.grant_amount == bob_grant_amount
    assert bob_othermoneyreport.grant_rank_num == bob_grant_rank_num
    assert bob_othermoneyreport.grant_rank_percent == bob_grant_rank_percent
    assert bob_othermoneyreport.tax_due_count == bob_tax_due_count
    assert bob_othermoneyreport.tax_due_amount == bob_tax_due_amount
    assert bob_othermoneyreport.tax_due_rank_num == bob_tax_due_rank_num
    assert bob_othermoneyreport.tax_due_rank_percent == bob_tax_due_rank_percent
    assert bob_othermoneyreport.tax_paid_amount == bob_tax_paid_amount
    assert bob_othermoneyreport.tax_paid_bool == bob_tax_paid_bool
    assert bob_othermoneyreport.tax_paid_rank_num == bob_tax_paid_rank_num
    assert bob_othermoneyreport.tax_paid_rank_percent == bob_tax_paid_rank_percent
    assert bob_othermoneyreport.transactions_count == bob_transactions_count
    assert bob_othermoneyreport.transactions_magnitude == bob_transactions_magnitude
    assert bob_othermoneyreport.transactions_rank_num == bob_transactions_rank_num
    assert (
        bob_othermoneyreport.transactions_rank_percent == bob_transactions_rank_percent
    )


def test_MoneyUnit_exists():
    # GIVEN
    texas_userhub = get_sue_texas_userhub()

    # WHEN
    x_money = MoneyUnit(userhub=texas_userhub)

    # THEN
    assert x_money.userhub == texas_userhub


# def test_MoneyUnit_save_other_report_CreatesFile():
#     # GIVEN


#     # WHEN
#     yao_moneyunit.save_other_report(get_bob_othermoneyreport())

#     # THEN
#     save_file(env_dir(), "bob.json", get_json_from_dict(dict(yao_moneyunit)) )

#     bob_ get_dict_from_json

# def test_MoneyUnit_save_other_report_CorrectlyCreatesFile():
#     # GIVEN
#     yao_moneyunit = MoneyUnit(yao_text)

#     # WHEN
#     yao_moneyunit.save_other_report(get_bob_othermoneyreport())

#     # THEN
#     save_file(env_dir(), "bob.json", get_json_from_dict(dict(yao_moneyunit)) )

#     bob_ get_dict_from_json


# def test_report_csv_file_HasCorrectColumns(env_dir_setup_cleanup):
#     # GIVEN

#     # grant_count: SELECT COUNT(*) FROM other WHERE grant_amount > 0
#     # grant_amount: Leader Duty get_other._credor_weight (SELECT grant_amount FROM other WHERE other_id = bob_text)
#     # grant_rank_num: SELECT COUNT(*) FROM other WHERE grant_amount > (SELECT tax_due_amount FROM other WHERE other_id = bob_text)
#     # grant_rank_percent: credor_rank_num / SELECT COUNT(*) FROM other WHERE grant_amount > 0
#     # tax_due_count: SELECT COUNT(*) FROM other WHERE tax_due_amount > 0
#     # tax_due_amount: Leader Duty get_other._debtor_weight (SELECT tax_due_amount FROM other WHERE other_id = bob_text)
#     # tax_due_rank_num: SELECT COUNT(*) FROM other WHERE tax_due_amount > (SELECT tax_due_amount FROM other WHERE other_id = bob_text)
#     # tax_due_rank_percent: debtor_rank_num / SELECT COUNT(*) FROM other WHERE tax_due_amount > 0
#     # tax_paid_bool: bool (if tax_due_amount == tax_paid_amount)
#     # tax_paid_amount: SELECT amount_paid FROM tax_ledger WHERE other_id = bob_text
#     # tax_paid_rank_num: SELECT COUNT(*) FROM other WHERE tax_paid_amount > (SELECT tax_paid_amount FROM other WHERE other_id = bob_text)
#     # tax_paid_rank_percent: tax_paid_rank_num / (SELECT COUNT(*) FROM other WHERE tax_paid_amount>0)
#     # transactions_cycle_count: SELECT COUNT(*) FROM transactions
#     # transactions_person_count: SELECT COUNT(*) FROM transactions WHERE dst_other_id = bob_text
#     # transactions_magnitude: SELECT SUM(money_amount) FROM transactions WHERE dst_other_id = bob_text
#     # transactions_rank_num: SELECT COUNT(*) FROM other WHERE tax_paid_amount > (SELECT tax_paid_amount FROM other WHERE other_id = bob_text)
#     # transactions_rank_percent: tax_paid_rank_num / transactions_cycle_count

#     assert 1 == 2


# def test_get_agenda_otherunits_dataframe_ReturnsCorrectDataFrame():
#     # GIVEN
#     bob_othermoneyreport = get_bob_othermoneyreport()

#     # WHEN
#     x_df = get_othermoneyreport_dataframe(bob_othermoneyreport)

#     # THEN
#     otherunit_colums = {
#         "other_id",
#         "credor_weight",
#         "debtor_weight",
#         "_agenda_cred",
#         "_agenda_debt",
#         "_agenda_intent_cred",
#         "_agenda_intent_debt",
#         "_agenda_intent_ratio_cred",
#         "_agenda_intent_ratio_debt",
#         "_credor_operational",
#         "_debtor_operational",
#         "_treasury_due_paid",
#         "_treasury_due_diff",
#         "_output_agenda_meld_order",
#         "_treasury_cred_score",
#         "_treasury_voice_rank",
#         "_treasury_voice_hx_lowest_rank",
#     }
#     print(f"{set(x_df.columns)=}")

#     assert set(x_df.columns) == otherunit_colums
#     assert x_df.shape[0] == 2


# # during the currency river process
# # init RiverCycle with init RiverBlock grants money to credors
# # Every RiverCycle after that creates all the riverblocks, dstributes the money
# # to the next RiverCycle.
# # Money leaves the system by paying taxes
# # Stop RiverCycling #1 If all money leaves the system by paying taxes
# # Stop RiverCycling #2 if two rivercycles in a row don't pay more taxes AND have the same others (no new others added between Cycles)
# # Stop RiverCycling #3 if cycles_run = rivercyclinglimit


# # def test_get_agenda_otherunits_dataframe_ReturnsCorrectDataFrame():
# #     # GIVEN
# #     luca_agenda = agendaunit_shop()
# #     luca_agenda.set_other_credor_pool(500)
# #     luca_agenda.set_other_debtor_pool(400)
# #     todd_text = "Todd"
# #     todd_credor_weight = 66
# #     todd_debtor_weight = 77
# #     luca_agenda.add_otherunit(todd_text, todd_credor_weight, todd_debtor_weight)
# #     sue_text = "Sue"
# #     sue_credor_weight = 434
# #     sue_debtor_weight = 323
# #     luca_agenda.add_otherunit(sue_text, sue_credor_weight, sue_debtor_weight)

# #     # WHEN
# #     x_df = get_agenda_otherunits_dataframe(luca_agenda)

# #     # THEN
# #     otherunit_colums = {
# #         "other_id",
# #         "credor_weight",
# #         "debtor_weight",
# #         "_agenda_cred",
# #         "_agenda_debt",
# #         "_agenda_intent_cred",
# #         "_agenda_intent_debt",
# #         "_agenda_intent_ratio_cred",
# #         "_agenda_intent_ratio_debt",
# #         "_credor_operational",
# #         "_debtor_operational",
# #         "_treasury_due_paid",
# #         "_treasury_due_diff",
# #         "_output_agenda_meld_order",
# #         "_treasury_cred_score",
# #         "_treasury_voice_rank",
# #         "_treasury_voice_hx_lowest_rank",
# #     }
# #     print(f"{set(x_df.columns)=}")

# #     assert set(x_df.columns) == otherunit_colums
# #     assert x_df.shape[0] == 2


# # def test_get_agenda_otherunits_dataframe_ReturnsCorrectEmptyDataFrame():
# #     # GIVEN
# #     luca_agenda = agendaunit_shop()

# #     # WHEN
# #     x_df = get_agenda_otherunits_dataframe(luca_agenda)

# #     # THEN
# #     otherunit_colums = {
# #         "other_id",
# #         "credor_weight",
# #         "debtor_weight",
# #         "_agenda_cred",
# #         "_agenda_debt",
# #         "_agenda_intent_cred",
# #         "_agenda_intent_debt",
# #         "_agenda_intent_ratio_cred",
# #         "_agenda_intent_ratio_debt",
# #         "_credor_operational",
# #         "_debtor_operational",
# #         "_treasury_due_paid",
# #         "_treasury_due_diff",
# #         "_output_agenda_meld_order",
# #         "_treasury_cred_score",
# #         "_treasury_voice_rank",
# #         "_treasury_voice_hx_lowest_rank",
# #     }
# #     print(f"{set(x_df.columns)=}")

# #     assert set(x_df.columns) == otherunit_colums
# #     assert x_df.shape[0] == 0


# # def test_get_agenda_intent_dataframe_ReturnsCorrectDataFrame():
# #     # GIVEN
# #     yao_agenda = agenda_v001_with_large_intent()
# #     week_text = "weekdays"
# #     week_road = yao_agenda.make_l1_road(week_text)
# #     assert len(yao_agenda.get_intent_dict()) == 63

# #     # WHEN
# #     x_df = get_agenda_intent_dataframe(yao_agenda)
# #     print(x_df)

# #     # THEN
# #     otherunit_colums = {
# #         "owner_id",
# #         "agenda_importance",
# #         "_label",
# #         "_parent_road",
# #         "_begin",
# #         "_close",
# #         "_addin",
# #         "_denom",
# #         "_numor",
# #         "_reest",
# #     }
# #     print(f"{set(x_df.columns)=}")

# #     assert set(x_df.columns) == otherunit_colums
# #     assert x_df.shape[0] == 63


# # def test_get_agenda_intent_dataframe_ReturnsCorrectEmptyDataFrame():
# #     # GIVEN
# #     yao_agenda = agendaunit_shop("Yao")
# #     assert len(yao_agenda.get_intent_dict()) == 0

# #     # WHEN
# #     x_df = get_agenda_intent_dataframe(yao_agenda)
# #     print(x_df)

# #     # THEN
# #     otherunit_colums = {
# #         "owner_id",
# #         "agenda_importance",
# #         "_label",
# #         "_parent_road",
# #         "_begin",
# #         "_close",
# #         "_addin",
# #         "_denom",
# #         "_numor",
# #         "_reest",
# #     }
# #     print(f"{set(x_df.columns)=}")

# #     assert set(x_df.columns) == otherunit_colums
