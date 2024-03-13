from src.agenda.atom import agendaatom_shop, atom_update, atom_insert, atom_delete
from src.agenda.book import bookunit_shop, create_legible_list
from src.agenda.agenda import agendaunit_shop


def test_create_legible_list_ReturnsObj_partyunit_INSERT():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    _addin_text = "_addin"
    _begin_text = "_begin"
    _close_text = "_close"
    _denom_text = "_denom"
    _meld_strategy_text = "_meld_strategy"
    _numeric_road_text = "_numeric_road"
    _numor_text = "_numor"
    _problem_bool_text = "_problem_bool"
    _range_source_road_text = "_range_source_road"
    _reest_text = "_reest"
    _weight_text = "_weight"
    promise_text = "promise"
    label_value = "clean fridge"
    parent_road_value = sue_agenda.make_l1_road("casa")
    _addin_value = 7
    _begin_value = 13
    _close_value = 17
    _denom_value = 23
    _meld_strategy_value = "example_text1"
    _numeric_road_value = sue_agenda.make_l1_road("sports")
    _numor_value = 29
    _problem_bool_value = False
    _range_source_road_value = sue_agenda.make_l1_road("greenways")
    _reest_value = 37
    _weight_value = 43
    promise_value = False
    clean_agendaatom = agendaatom_shop(category, atom_insert())
    clean_agendaatom.set_arg(label_text, label_value)
    clean_agendaatom.set_arg(parent_road_text, parent_road_value)
    clean_agendaatom.set_arg(_addin_text, _addin_value)
    clean_agendaatom.set_arg(_begin_text, _begin_value)
    clean_agendaatom.set_arg(_close_text, _close_value)
    clean_agendaatom.set_arg(_denom_text, _denom_value)
    clean_agendaatom.set_arg(_meld_strategy_text, _meld_strategy_value)
    clean_agendaatom.set_arg(_numeric_road_text, _numeric_road_value)
    clean_agendaatom.set_arg(_numor_text, _numor_value)
    clean_agendaatom.set_arg(_problem_bool_text, _problem_bool_value)
    clean_agendaatom.set_arg(_range_source_road_text, _range_source_road_value)
    clean_agendaatom.set_arg(_reest_text, _reest_value)
    clean_agendaatom.set_arg(_weight_text, _weight_value)
    clean_agendaatom.set_arg(promise_text, promise_value)
    # rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(clean_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"Created Idea '{label_value}' with parent_road {parent_road_value}. _addin={_addin_value}._begin={_begin_value}._close={_close_value}._denom={_denom_value}._meld_strategy={_meld_strategy_value}._numeric_road={_numeric_road_value}._numor={_numor_value}._problem_bool={_problem_bool_value}._range_source_road={_range_source_road_value}._reest={_reest_value}._weight={_weight_value}.promise={promise_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partyunit_UPDATE():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    _addin_text = "_addin"
    _begin_text = "_begin"
    _close_text = "_close"
    _denom_text = "_denom"
    _meld_strategy_text = "_meld_strategy"
    _numeric_road_text = "_numeric_road"
    _numor_text = "_numor"
    _problem_bool_text = "_problem_bool"
    _range_source_road_text = "_range_source_road"
    _reest_text = "_reest"
    _weight_text = "_weight"
    promise_text = "promise"
    label_value = "clean fridge"
    parent_road_value = sue_agenda.make_l1_road("casa")
    _addin_value = 7
    _begin_value = 13
    _close_value = 17
    _denom_value = 23
    _meld_strategy_value = "example_text1"
    _numeric_road_value = sue_agenda.make_l1_road("sports")
    _numor_value = 29
    _problem_bool_value = False
    _range_source_road_value = sue_agenda.make_l1_road("greenways")
    _reest_value = 37
    _weight_value = 43
    promise_value = False
    clean_agendaatom = agendaatom_shop(category, atom_update())
    clean_agendaatom.set_arg(label_text, label_value)
    clean_agendaatom.set_arg(parent_road_text, parent_road_value)
    clean_agendaatom.set_arg(_addin_text, _addin_value)
    clean_agendaatom.set_arg(_begin_text, _begin_value)
    clean_agendaatom.set_arg(_close_text, _close_value)
    clean_agendaatom.set_arg(_denom_text, _denom_value)
    clean_agendaatom.set_arg(_meld_strategy_text, _meld_strategy_value)
    clean_agendaatom.set_arg(_numeric_road_text, _numeric_road_value)
    clean_agendaatom.set_arg(_numor_text, _numor_value)
    clean_agendaatom.set_arg(_problem_bool_text, _problem_bool_value)
    clean_agendaatom.set_arg(_range_source_road_text, _range_source_road_value)
    clean_agendaatom.set_arg(_reest_text, _reest_value)
    clean_agendaatom.set_arg(_weight_text, _weight_value)
    clean_agendaatom.set_arg(promise_text, promise_value)
    # rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(clean_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"Idea '{label_value}' with parent_road {parent_road_value} changed these attributes: _addin={_addin_value}._begin={_begin_value}._close={_close_value}._denom={_denom_value}._meld_strategy={_meld_strategy_value}._numeric_road={_numeric_road_value}._numor={_numor_value}._problem_bool={_problem_bool_value}._range_source_road={_range_source_road_value}._reest={_reest_value}._weight={_weight_value}.promise={promise_value}."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


def test_create_legible_list_ReturnsObj_partyunit_DELETE():
    # GIVEN
    sue_agenda = agendaunit_shop("Sue")
    category = "agenda_ideaunit"
    label_text = "label"
    parent_road_text = "parent_road"
    label_value = "clean fridge"
    parent_road_value = sue_agenda.make_l1_road("casa")
    clean_agendaatom = agendaatom_shop(category, atom_delete())
    clean_agendaatom.set_arg(label_text, label_value)
    clean_agendaatom.set_arg(parent_road_text, parent_road_value)
    # rico_agendaatom._crud_cache = None
    # print(f"{rico_agendaatom=}")
    x_bookunit = bookunit_shop()
    x_bookunit.set_agendaatom(clean_agendaatom)

    # WHEN
    legible_list = create_legible_list(x_bookunit, sue_agenda)

    # THEN
    x_str = f"Idea '{label_value}' with parent_road {parent_road_value} was deleted."
    print(f"{x_str=}")
    assert legible_list[0] == x_str


# def test_create_legible_list_ReturnsObj_partyunit_INSERT_money_desc_IsNone():
#     # GIVEN
#     category = "agenda_partyunit"
#     party_id_text = "party_id"
#     creditor_weight_text = "creditor_weight"
#     debtor_weight_text = "debtor_weight"
#     creditor_weight_value = 81
#     debtor_weight_value = 43
#     rico_text = "Rico"
#     rico_agendaatom = agendaatom_shop(category, atom_insert())
#     rico_agendaatom.set_arg(party_id_text, rico_text)
#     rico_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
#     rico_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
#     rico_agendaatom._crud_cache = None
#     # print(f"{rico_agendaatom=}")
#     x_bookunit = bookunit_shop()
#     x_bookunit.set_agendaatom(rico_agendaatom)
#     sue_agenda = agendaunit_shop("Sue")

#     # WHEN
#     legible_list = create_legible_list(x_bookunit, sue_agenda)

#     # THEN
#     x_str = f"{rico_text} was added with {creditor_weight_value} money credit and {debtor_weight_value} money debt"
#     print(f"{x_str=}")
#     assert legible_list[0] == x_str


# def test_create_legible_list_ReturnsObj_partyunit_UPDATE_creditor_weight_debtor_weight():
#     # GIVEN
#     category = "agenda_partyunit"
#     party_id_text = "party_id"
#     creditor_weight_text = "creditor_weight"
#     debtor_weight_text = "debtor_weight"
#     creditor_weight_value = 81
#     debtor_weight_value = 43
#     rico_text = "Rico"
#     rico_agendaatom = agendaatom_shop(category, atom_update())
#     rico_agendaatom.set_arg(party_id_text, rico_text)
#     rico_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
#     rico_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
#     rico_agendaatom._crud_cache = None
#     # print(f"{rico_agendaatom=}")
#     x_bookunit = bookunit_shop()
#     x_bookunit.set_agendaatom(rico_agendaatom)
#     sue_agenda = agendaunit_shop("Sue")
#     sue_money_desc = "dragon coins"
#     sue_agenda.set_money_desc(sue_money_desc)

#     # WHEN
#     legible_list = create_legible_list(x_bookunit, sue_agenda)

#     # THEN
#     x_str = f"{rico_text} now has {creditor_weight_value} {sue_agenda._money_desc} credit and {debtor_weight_value} {sue_agenda._money_desc} debt."
#     print(f"{x_str=}")
#     assert legible_list[0] == x_str


# def test_create_legible_list_ReturnsObj_partyunit_UPDATE_creditor_weight():
#     # GIVEN
#     category = "agenda_partyunit"
#     party_id_text = "party_id"
#     creditor_weight_text = "creditor_weight"
#     creditor_weight_value = 81
#     rico_text = "Rico"
#     rico_agendaatom = agendaatom_shop(category, atom_update())
#     rico_agendaatom.set_arg(party_id_text, rico_text)
#     rico_agendaatom.set_arg(creditor_weight_text, creditor_weight_value)
#     rico_agendaatom._crud_cache = None
#     # print(f"{rico_agendaatom=}")
#     x_bookunit = bookunit_shop()
#     x_bookunit.set_agendaatom(rico_agendaatom)
#     sue_agenda = agendaunit_shop("Sue")
#     sue_money_desc = "dragon coins"
#     sue_agenda.set_money_desc(sue_money_desc)

#     # WHEN
#     legible_list = create_legible_list(x_bookunit, sue_agenda)

#     # THEN
#     x_str = (
#         f"{rico_text} now has {creditor_weight_value} {sue_agenda._money_desc} credit."
#     )
#     print(f"{x_str=}")
#     assert legible_list[0] == x_str


# def test_create_legible_list_ReturnsObj_partyunit_UPDATE_debtor_weight():
#     # GIVEN
#     category = "agenda_partyunit"
#     party_id_text = "party_id"
#     debtor_weight_text = "debtor_weight"
#     debtor_weight_value = 43
#     rico_text = "Rico"
#     rico_agendaatom = agendaatom_shop(category, atom_update())
#     rico_agendaatom.set_arg(party_id_text, rico_text)
#     rico_agendaatom.set_arg(debtor_weight_text, debtor_weight_value)
#     rico_agendaatom._crud_cache = None
#     # print(f"{rico_agendaatom=}")
#     x_bookunit = bookunit_shop()
#     x_bookunit.set_agendaatom(rico_agendaatom)
#     sue_agenda = agendaunit_shop("Sue")
#     sue_money_desc = "dragon coins"
#     sue_agenda.set_money_desc(sue_money_desc)

#     # WHEN
#     legible_list = create_legible_list(x_bookunit, sue_agenda)

#     # THEN
#     x_str = f"{rico_text} now has {debtor_weight_value} {sue_agenda._money_desc} debt."
#     print(f"{x_str=}")
#     assert legible_list[0] == x_str


# def test_create_legible_list_ReturnsObj_partyunit_DELETE():
#     # GIVEN
#     category = "agenda_partyunit"
#     party_id_text = "party_id"
#     rico_text = "Rico"
#     rico_agendaatom = agendaatom_shop(category, atom_delete())
#     rico_agendaatom.set_arg(party_id_text, rico_text)
#     rico_agendaatom._crud_cache = None
#     # print(f"{rico_agendaatom=}")
#     x_bookunit = bookunit_shop()
#     x_bookunit.set_agendaatom(rico_agendaatom)
#     sue_agenda = agendaunit_shop("Sue")
#     sue_money_desc = "dragon coins"
#     sue_agenda.set_money_desc(sue_money_desc)

#     # WHEN
#     legible_list = create_legible_list(x_bookunit, sue_agenda)

#     # THEN
#     x_str = f"{rico_text} was removed from {sue_agenda._money_desc} partys."
#     print(f"{x_str=}")
#     assert legible_list[0] == x_str
