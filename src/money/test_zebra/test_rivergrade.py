from src.money.examples.example_credorledgers import example_yao_userhub
from src.money.rivercycle import RiverGrade, rivergrade_shop


def test_RiverGrade_Exists():
    # GIVEN / WHEN
    x_rivergrade = RiverGrade()

    # THEN
    #: Leader Duty get_other._debtor_weight (SELECT tax_due_amount FROM other WHERE other_id = bob_text)
    assert x_rivergrade.userhub is None
    assert x_rivergrade.other_id is None
    assert x_rivergrade.number is None
    #: Leader Duty get_other._debtor_weight (SELECT tax_due_amount FROM other WHERE other_id = bob_text)
    assert x_rivergrade.tax_due_amount is None
    #: Leader Duty get_other._credor_weight (SELECT grant_amount FROM other WHERE other_id = bob_text)
    assert x_rivergrade.grant_amount is None
    #: SELECT COUNT(*) FROM other WHERE tax_due_amount > (SELECT tax_due_amount FROM other WHERE other_id = bob_text)
    assert x_rivergrade.debtor_rank_num is None
    #: SELECT COUNT(*) FROM other WHERE grant_amount > (SELECT tax_due_amount FROM other WHERE other_id = bob_text)
    assert x_rivergrade.credor_rank_num is None
    #: SELECT amount_paid FROM tax_ledger WHERE other_id = bob_text
    assert x_rivergrade.tax_paid_amount is None
    #: bool (if tax_due_amount == tax_paid_amount)
    assert x_rivergrade.tax_paid_bool is None
    #: SELECT COUNT(*) FROM other WHERE tax_paid_amount > (SELECT tax_paid_amount FROM other WHERE other_id = bob_text)
    assert x_rivergrade.tax_paid_rank_num is None
    #: tax_paid_rank_num / (SELECT COUNT(*) FROM other WHERE tax_paid_amount>0)
    assert x_rivergrade.tax_paid_rank_percent is None
    #: SELECT COUNT(*) FROM other WHERE tax_due_amount > 0
    assert x_rivergrade.debtor_count is None
    #: SELECT COUNT(*) FROM other WHERE grant_amount > 0
    assert x_rivergrade.credor_count is None
    #: debtor_rank_num / SELECT COUNT(*) FROM other WHERE tax_due_amount > 0
    assert x_rivergrade.debtor_rank_percent is None
    #: credor_rank_num / SELECT COUNT(*) FROM other WHERE grant_amount > 0
    assert x_rivergrade.credor_rank_percent is None
    # SELECT COUNT(*) FROM transactions WHERE dst_other_id = bob_text
    assert x_rivergrade.transactions_count is None
    # SELECT SUM(money_amount) FROM transactions WHERE dst_other_id = bob_text
    assert x_rivergrade.transactions_magnitude is None


def test_rivergrade_shop_ReturnsCorrectObjWithArg():
    # GIVEN
    bob_text = "Bob"
    yao_userhub = example_yao_userhub()
    ten_int = 10
    x_debtor_count = 7
    x_credor_count = 9

    # WHEN
    x_rivergrade = rivergrade_shop(
        yao_userhub, bob_text, ten_int, x_debtor_count, x_credor_count
    )

    # THEN
    # create RiverGrade and
    assert x_rivergrade.userhub == yao_userhub
    assert x_rivergrade.other_id == bob_text
    assert x_rivergrade.number == ten_int
    assert x_rivergrade.tax_due_amount is None
    assert x_rivergrade.grant_amount is None
    assert x_rivergrade.debtor_rank_num is None
    assert x_rivergrade.credor_rank_num is None
    assert x_rivergrade.tax_paid_amount is None
    assert x_rivergrade.tax_paid_bool is None
    assert x_rivergrade.tax_paid_rank_num is None
    assert x_rivergrade.tax_paid_rank_percent is None
    assert x_rivergrade.debtor_count == x_debtor_count
    assert x_rivergrade.credor_count == x_credor_count
    assert x_rivergrade.debtor_rank_percent is None
    assert x_rivergrade.credor_rank_percent is None
    assert x_rivergrade.transactions_count is None
    assert x_rivergrade.transactions_magnitude is None


def test_rivergrade_shop_ReturnsCorrectObjWithoutArgs():
    # GIVEN
    bob_text = "Bob"
    yao_userhub = example_yao_userhub()

    # WHEN
    x_rivergrade = rivergrade_shop(yao_userhub, bob_text)

    # THEN
    # create RiverGrade and
    assert x_rivergrade.userhub == yao_userhub
    assert x_rivergrade.number == 0
    assert x_rivergrade.tax_due_amount is None
    assert x_rivergrade.grant_amount is None
    assert x_rivergrade.debtor_rank_num is None
    assert x_rivergrade.credor_rank_num is None
    assert x_rivergrade.tax_paid_amount is None
    assert x_rivergrade.tax_paid_bool is None
    assert x_rivergrade.tax_paid_rank_num is None
    assert x_rivergrade.tax_paid_rank_percent is None
    assert x_rivergrade.debtor_count is None
    assert x_rivergrade.credor_count is None
    assert x_rivergrade.debtor_rank_percent is None
    assert x_rivergrade.credor_rank_percent is None
    assert x_rivergrade.transactions_count is None
    assert x_rivergrade.transactions_magnitude is None


def test_RiverGrade_Exists():
    # GIVEN
    x_rivergrade = RiverGrade()
    assert x_rivergrade.tax_due_amount is None
    assert x_rivergrade.tax_paid_amount is None
    assert x_rivergrade.tax_paid_bool is None

    # WHEN
    x_tax_due_amount = 88
    x_rivergrade.set_tax_due_amount(x_tax_due_amount)
    # THEN
    assert x_rivergrade.tax_due_amount == x_tax_due_amount
    assert x_rivergrade.tax_paid_amount is None
    assert x_rivergrade.tax_paid_bool == False

    # WHEN
    x_tax_paid_amount = 77
    x_rivergrade.set_tax_paid_amount(x_tax_paid_amount)
    # THEN
    assert x_rivergrade.tax_due_amount == x_tax_due_amount
    assert x_rivergrade.tax_paid_amount == x_tax_paid_amount
    assert x_rivergrade.tax_paid_bool == False

    # WHEN
    x_rivergrade.set_tax_paid_amount(x_tax_due_amount)
    # THEN
    assert x_rivergrade.tax_due_amount == x_rivergrade.tax_paid_amount
    assert x_rivergrade.tax_paid_bool == True
