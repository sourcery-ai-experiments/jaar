from src.atom.quark import quarkunit_shop, quark_update
from src.atom.nuc import nucunit_shop, create_legible_list
from src._truth.truth import truthunit_shop


def test_create_legible_list_ReturnsObjGivenEmptyNuc():
    # GIVEN / WHEN
    x_nucunit = nucunit_shop()
    sue_truth = truthunit_shop("Sue")

    # THEN
    assert create_legible_list(x_nucunit, sue_truth) == []


def test_create_legible_list_ReturnsObjGivenTruthUpdate_weight():
    # GIVEN
    category = "truthunit"
    weight_text = "_weight"
    weight_int = 55
    weight_quarkunit = quarkunit_shop(category, quark_update())
    weight_quarkunit.set_arg(weight_text, weight_int)
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(weight_quarkunit)
    sue_truth = truthunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_truth)

    # THEN
    x_str = f"{sue_truth._owner_id}'s truth weight was transited to {weight_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenTruthUpdate_monetary_desc():
    # GIVEN
    category = "truthunit"
    _monetary_desc_text = "_monetary_desc"
    sue_monetary_desc = "dragon funds"
    _monetary_desc_quarkunit = quarkunit_shop(category, quark_update())
    _monetary_desc_quarkunit.set_arg(_monetary_desc_text, sue_monetary_desc)
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(_monetary_desc_quarkunit)
    sue_truth = truthunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_truth)

    # THEN
    x_str = f"{sue_truth._owner_id}'s monetary_desc is now called '{sue_monetary_desc}'"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenTruthUpdate_other_credor_pool():
    # GIVEN
    category = "truthunit"
    other_credor_pool_text = "_other_credor_pool"
    other_credor_pool_int = 71
    other_credor_pool_quarkunit = quarkunit_shop(category, quark_update())
    other_credor_pool_quarkunit.set_arg(other_credor_pool_text, other_credor_pool_int)

    print(f"{other_credor_pool_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(other_credor_pool_quarkunit)
    sue_truth = truthunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_truth.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_truth)

    # THEN
    x_str = f"{sue_monetary_desc} credor pool is now {other_credor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenTruthUpdate_other_credor_pool_With_monetary_desc_None():
    # GIVEN
    category = "truthunit"
    other_credor_pool_text = "_other_credor_pool"
    other_credor_pool_int = 71
    other_credor_pool_quarkunit = quarkunit_shop(category, quark_update())
    other_credor_pool_quarkunit.set_arg(other_credor_pool_text, other_credor_pool_int)

    print(f"{other_credor_pool_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(other_credor_pool_quarkunit)
    sue_truth = truthunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_truth)

    # THEN
    x_str = f"{sue_truth._owner_id}'s monetary_desc credor pool is now {other_credor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenTruthUpdate_other_debtor_pool():
    # GIVEN
    category = "truthunit"
    other_debtor_pool_text = "_other_debtor_pool"
    other_debtor_pool_int = 78
    other_debtor_pool_quarkunit = quarkunit_shop(category, quark_update())
    other_debtor_pool_quarkunit.set_arg(other_debtor_pool_text, other_debtor_pool_int)

    print(f"{other_debtor_pool_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(other_debtor_pool_quarkunit)
    sue_truth = truthunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_truth.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_truth)

    # THEN
    x_str = f"{sue_monetary_desc} debtor pool is now {other_debtor_pool_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenTruthUpdate_other_credor_pool_Equal_other_debtor_pool():
    # GIVEN
    x_nucunit = nucunit_shop()
    category = "truthunit"
    other_credor_pool_text = "_other_credor_pool"
    other_debtor_pool_text = "_other_debtor_pool"
    other_pool_int = 83
    truthunit_quarkunit = quarkunit_shop(category, quark_update())
    truthunit_quarkunit.set_arg(other_credor_pool_text, other_pool_int)
    truthunit_quarkunit.set_arg(other_debtor_pool_text, other_pool_int)
    x_nucunit.set_quarkunit(truthunit_quarkunit)
    sue_truth = truthunit_shop("Sue")
    sue_monetary_desc = "dragon funds"
    sue_truth.set_monetary_desc(sue_monetary_desc)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_truth)

    # THEN
    x_str = f"{sue_monetary_desc} total pool is now {other_pool_int}"
    assert len(legible_list) == 1
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenTruthUpdate_max_tree_traverse():
    # GIVEN
    category = "truthunit"
    max_tree_traverse_text = "_max_tree_traverse"
    max_tree_traverse_int = 71
    max_tree_traverse_quarkunit = quarkunit_shop(category, quark_update())
    max_tree_traverse_quarkunit.set_arg(max_tree_traverse_text, max_tree_traverse_int)

    print(f"{max_tree_traverse_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(max_tree_traverse_quarkunit)
    sue_truth = truthunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_truth)

    # THEN
    x_str = f"{sue_truth._owner_id}'s maximum number of Truth output evaluations transited to {max_tree_traverse_int}"
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObjGivenTruthUpdate_meld_strategy():
    # GIVEN
    category = "truthunit"
    meld_strategy_text = "_meld_strategy"
    meld_strategy_value = "override"
    meld_strategy_quarkunit = quarkunit_shop(category, quark_update())
    meld_strategy_quarkunit.set_arg(meld_strategy_text, meld_strategy_value)

    print(f"{meld_strategy_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(meld_strategy_quarkunit)
    sue_truth = truthunit_shop("Sue")

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_truth)

    # THEN
    x_str = (
        f"{sue_truth._owner_id}'s Meld strategy transited to '{meld_strategy_value}'"
    )
    assert legible_list[0] == x_str
