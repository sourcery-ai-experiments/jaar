from src.atom.quark import quarkunit_shop, quark_update, quark_insert, quark_delete
from src.atom.nuc import nucunit_shop, create_legible_list
from src._truth.truth import truthunit_shop


def test_create_legible_list_ReturnsObj_idea_balancelink_INSERT():
    # GIVEN
    sue_truth = truthunit_shop("Sue")
    category = "truth_idea_balancelink"
    road_text = "road"
    casa_road = sue_truth.make_l1_road("casa")
    road_value = sue_truth.make_road(casa_road, "clean fridge")
    belief_id_text = "belief_id"
    belief_id_value = f"{sue_truth._road_delimiter}Swimmers"
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    credor_weight_value = 81
    debtor_weight_value = 43
    swim_quarkunit = quarkunit_shop(category, quark_insert())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(belief_id_text, belief_id_value)
    swim_quarkunit.set_arg(credor_weight_text, credor_weight_value)
    swim_quarkunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_truth)

    # THEN
    x_str = f"Balancelink created for belief {belief_id_value} for idea '{road_value}' with credor_weight={credor_weight_value} and debtor_weight={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_balancelink_UPDATE_credor_weight_debtor_weight():
    # GIVEN
    sue_truth = truthunit_shop("Sue")

    category = "truth_idea_balancelink"
    belief_id_text = "belief_id"
    belief_id_value = f"{sue_truth._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_truth.make_l1_road("casa")
    road_value = sue_truth.make_road(casa_road, "clean fridge")
    credor_weight_text = "credor_weight"
    debtor_weight_text = "debtor_weight"
    credor_weight_value = 81
    debtor_weight_value = 43
    swim_quarkunit = quarkunit_shop(category, quark_update())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(belief_id_text, belief_id_value)
    swim_quarkunit.set_arg(credor_weight_text, credor_weight_value)
    swim_quarkunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_truth)

    # THEN
    x_str = f"Balancelink has been transited for belief {belief_id_value} for idea '{road_value}'. Now credor_weight={credor_weight_value} and debtor_weight={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_balancelink_UPDATE_credor_weight():
    # GIVEN
    sue_truth = truthunit_shop("Sue")
    category = "truth_idea_balancelink"
    belief_id_text = "belief_id"
    belief_id_value = f"{sue_truth._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_truth.make_l1_road("casa")
    road_value = sue_truth.make_road(casa_road, "clean fridge")
    credor_weight_text = "credor_weight"
    credor_weight_value = 81
    swim_quarkunit = quarkunit_shop(category, quark_update())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(belief_id_text, belief_id_value)
    swim_quarkunit.set_arg(credor_weight_text, credor_weight_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_truth)

    # THEN
    x_str = f"Balancelink has been transited for belief {belief_id_value} for idea '{road_value}'. Now credor_weight={credor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_balancelink_UPDATE_debtor_weight():
    # GIVEN
    sue_truth = truthunit_shop("Sue")
    category = "truth_idea_balancelink"
    belief_id_text = "belief_id"
    belief_id_value = f"{sue_truth._road_delimiter}Swimmers"
    road_text = "road"
    casa_road = sue_truth.make_l1_road("casa")
    road_value = sue_truth.make_road(casa_road, "clean fridge")
    debtor_weight_text = "debtor_weight"
    debtor_weight_value = 81
    swim_quarkunit = quarkunit_shop(category, quark_update())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(belief_id_text, belief_id_value)
    swim_quarkunit.set_arg(debtor_weight_text, debtor_weight_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_truth)

    # THEN
    x_str = f"Balancelink has been transited for belief {belief_id_value} for idea '{road_value}'. Now debtor_weight={debtor_weight_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_idea_balancelink_DELETE():
    # GIVEN
    sue_truth = truthunit_shop("Sue")
    category = "truth_idea_balancelink"
    road_text = "road"
    casa_road = sue_truth.make_l1_road("casa")
    road_value = sue_truth.make_road(casa_road, "clean fridge")
    belief_id_text = "belief_id"
    belief_id_value = f"{sue_truth._road_delimiter}Swimmers"
    swim_quarkunit = quarkunit_shop(category, quark_delete())
    swim_quarkunit.set_arg(road_text, road_value)
    swim_quarkunit.set_arg(belief_id_text, belief_id_value)
    # print(f"{swim_quarkunit=}")
    x_nucunit = nucunit_shop()
    x_nucunit.set_quarkunit(swim_quarkunit)

    # WHEN
    legible_list = create_legible_list(x_nucunit, sue_truth)

    # THEN
    x_str = f"Balancelink for belief {belief_id_value}, idea '{road_value}' has been deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str
