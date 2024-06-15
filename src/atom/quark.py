from src._instrument.file import open_file, save_file
from src._instrument.python import (
    get_empty_dict_if_none,
    get_json_from_dict,
    get_dict_from_json,
)
from src._instrument.sqlite import create_insert_sqlstr, RowData
from src._road.road import create_road
from src.agenda.reason_idea import factunit_shop
from src.agenda.party import partyunit_shop, partylink_shop
from src.agenda.belief import beliefunit_shop, balancelink_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import AgendaUnit
from dataclasses import dataclass
from os import getcwd as os_getcwd


class CRUD_command(str):
    pass


def quark_update() -> CRUD_command:
    return "UPDATE"


def quark_insert() -> CRUD_command:
    return "INSERT"


def quark_delete() -> CRUD_command:
    return "DELETE"


def quark_hx_table_name() -> str:
    return "quark_hx"


def quark_mstr_table_name() -> str:
    return "quark_mstr"


def get_quark_config_file_name() -> str:
    return "quark_config.json"


def config_file_dir() -> str:
    return f"{os_getcwd()}/src/atom"


def get_quark_config_dict() -> dict:
    return get_dict_from_json(
        open_file(config_file_dir(), get_quark_config_file_name())
    )


def add_to_quark_table_columns(x_dict, quark_category, crud, arg_key, arg_value):
    x_dict[f"{quark_category}_{crud}_{arg_key}"] = arg_value.get("sqlite_datatype")


def get_flattened_quark_table_build() -> dict[str:]:
    required_args_text = "required_args"
    optional_args_text = "optional_args"
    quark_table_columns = {}
    quark_config = get_quark_config_dict()
    for quark_category, category_dict in quark_config.items():
        catergory_insert = category_dict.get(quark_insert())
        catergory_update = category_dict.get(quark_update())
        catergory_delete = category_dict.get(quark_delete())
        if catergory_insert != None:
            required_args = category_dict.get(required_args_text)
            optional_args = category_dict.get(optional_args_text)
            for required_arg, x_value in required_args.items():
                add_to_quark_table_columns(
                    quark_table_columns,
                    quark_category,
                    quark_insert(),
                    required_arg,
                    x_value,
                )
            for optional_arg, x_value in optional_args.items():
                add_to_quark_table_columns(
                    quark_table_columns,
                    quark_category,
                    quark_insert(),
                    optional_arg,
                    x_value,
                )
        if catergory_update != None:
            required_args = category_dict.get(required_args_text)
            optional_args = category_dict.get(optional_args_text)
            for required_arg, x_value in required_args.items():
                add_to_quark_table_columns(
                    quark_table_columns,
                    quark_category,
                    quark_update(),
                    required_arg,
                    x_value,
                )
            for optional_arg, x_value in optional_args.items():
                add_to_quark_table_columns(
                    quark_table_columns,
                    quark_category,
                    quark_update(),
                    optional_arg,
                    x_value,
                )
        if catergory_delete != None:
            required_args = category_dict.get(required_args_text)
            for required_arg, x_value in required_args.items():
                add_to_quark_table_columns(
                    quark_table_columns,
                    quark_category,
                    quark_delete(),
                    required_arg,
                    x_value,
                )
    return quark_table_columns


def get_normalized_agenda_table_build() -> dict[str : dict[str:]]:
    required_args_text = "required_args"
    optional_args_text = "optional_args"
    sqlite_datatype_text = "sqlite_datatype"
    nullable_text = "nullable"
    agenda_tables = {}
    quark_config = get_quark_config_dict()
    for x_category, category_dict in quark_config.items():
        agenda_tables[x_category] = {}
        l1_dict = agenda_tables.get(x_category)
        required_args = category_dict.get(required_args_text)
        optional_args = category_dict.get(optional_args_text)
        if required_args != None:
            for required_arg, x_value in required_args.items():
                l1_dict[required_arg] = {
                    sqlite_datatype_text: x_value.get(sqlite_datatype_text),
                    nullable_text: False,
                }

        if optional_args != None:
            for optional_arg, x_value in optional_args.items():
                l1_dict[optional_arg] = {
                    sqlite_datatype_text: x_value.get(sqlite_datatype_text),
                    nullable_text: True,
                }

    return agenda_tables


def save_quark_config_file(quark_config_dict):
    save_file(
        dest_dir=config_file_dir(),
        file_name=get_quark_config_file_name(),
        file_text=get_json_from_dict(quark_config_dict),
    )


def category_ref() -> set:
    return get_quark_config_dict().keys()


def is_category_ref(category_text: str) -> bool:
    return category_text in category_ref()


def get_quark_order(
    category: str,
    crud_text: str,
    quark_order_text: str,
    expected_quark_order: int = None,
) -> int:
    quark_config_dict = get_quark_config_dict()
    category_dict = quark_config_dict.get(category)
    crud_dict = category_dict.get(crud_text)
    return crud_dict.get(quark_order_text)


def set_mog(
    category: str,
    crud_text: str,
    quark_order_text: str,
    quark_order_int: int,
) -> int:
    quark_config_dict = get_quark_config_dict()
    category_dict = quark_config_dict.get(category)
    crud_dict = category_dict.get(crud_text)
    crud_dict[quark_order_text] = quark_order_int
    save_quark_config_file(quark_config_dict)


class QuarkUnitDescriptionException(Exception):
    pass


@dataclass
class QuarkUnit:
    category: str = None
    crud_text: str = None
    required_args: dict[str:str] = None
    optional_args: dict[str:str] = None
    quark_order: int = None

    def get_insert_sqlstr(self) -> str:
        if self.is_valid() is False:
            raise QuarkUnitDescriptionException(
                f"Cannot get_insert_sqlstr '{self.category}' with is_valid=False."
            )

        x_columns = [
            f"{self.category}_{self.crud_text}_{required_arg}"
            for required_arg in self.required_args.keys()
        ]
        x_columns.extend(
            f"{self.category}_{self.crud_text}_{optional_arg}"
            for optional_arg in self.optional_args.keys()
        )
        x_values = list(self.required_args.values())
        x_values.extend(iter(self.optional_args.values()))
        return create_insert_sqlstr(quark_hx_table_name(), x_columns, x_values)

    def get_description(self) -> str:
        if self.is_valid() is False:
            raise QuarkUnitDescriptionException("quarkunit is not valid")

        description_elements = self._get_crud_dict().get("description_elements")

        x_str = ""
        arg_value = ""
        preceding_text = ""
        proceding_text = ""
        for description_element in description_elements:
            for x_key, x_value in description_element.items():
                if x_key == "arg":
                    arg_value = self.get_value(x_value)
                elif x_key == "preceding text":
                    preceding_text = x_value
                elif x_key == "proceding text":
                    proceding_text = x_value
            if arg_value != None and x_str == "":
                x_str = f"{preceding_text}{arg_value}{proceding_text}"
            elif arg_value != None:
                x_str = f"{x_str} {preceding_text}{arg_value}{proceding_text}"
        return x_str

    def get_all_args_in_list(self):
        x_list = list(self.required_args.values())
        x_list.extend(list(self.optional_args.values()))
        return x_list

    def set_quark_order(self):
        self.quark_order = get_quark_order(
            category=self.category,
            crud_text=self.crud_text,
            quark_order_text="quark_order",
        )

    def set_arg(self, x_key: str, x_value: any):
        for required_arg in self._get_required_args_dict():
            if x_key == required_arg:
                self.set_required_arg(x_key, x_value)
        for optional_arg in self._get_optional_args_dict():
            if x_key == optional_arg:
                self.set_optional_arg(x_key, x_value)

    def set_required_arg(self, x_key: str, x_value: any):
        self.required_args[x_key] = x_value

    def set_optional_arg(self, x_key: str, x_value: any):
        self.optional_args[x_key] = x_value

    def _get_category_dict(self) -> dict:
        return get_quark_config_dict().get(self.category)

    def _get_crud_dict(self) -> dict:
        return self._get_category_dict().get(self.crud_text)

    def _get_required_args_dict(self) -> dict:
        return self._get_category_dict().get("required_args")

    def _get_optional_args_dict(self) -> dict:
        return get_empty_dict_if_none(self._get_category_dict().get("optional_args"))

    def is_required_args_valid(self) -> bool:
        if self.crud_text not in {quark_delete(), quark_insert(), quark_update()}:
            return False
        required_args_dict = self._get_required_args_dict()
        return required_args_dict.keys() == self.required_args.keys()

    def is_optional_args_valid(self) -> bool:
        if self.crud_text not in {quark_delete(), quark_insert(), quark_update()}:
            return False

        optional_args_dict = self._get_optional_args_dict()
        return set(self.optional_args.keys()).issubset(set(optional_args_dict.keys()))

    def is_valid(self) -> bool:
        return self.is_required_args_valid() and self.is_optional_args_valid()

    def get_value(self, arg_key: str) -> any:
        required_value = self.required_args.get(arg_key)
        if required_value is None:
            return self.optional_args.get(arg_key)
        return required_value

    def get_required_args_dict(self) -> dict[str:str]:
        return dict(self.required_args.items())

    def get_optional_args_dict(self) -> dict[str:str]:
        return dict(self.optional_args.items())

    def get_dict(self) -> dict[str:str]:
        required_args_dict = self.get_required_args_dict()
        optional_args_dict = self.get_optional_args_dict()
        # x_dict = {
        #     "category": self.category,
        #     "crud_text": self.crud_text,
        #     "required_args": required_args_dict,
        # }
        # if optional_args_dict != {}:
        #     x_dict["optional_args"] = optional_args_dict
        return {
            "category": self.category,
            "crud_text": self.crud_text,
            "required_args": required_args_dict,
            "optional_args": optional_args_dict,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def quarkunit_shop(
    category: str,
    crud_text: str = None,
    required_args: dict[str:str] = None,
    optional_args: dict[str:str] = None,
) -> QuarkUnit:
    if is_category_ref(category):
        return QuarkUnit(
            category=category,
            crud_text=crud_text,
            required_args=get_empty_dict_if_none(required_args),
            optional_args=get_empty_dict_if_none(optional_args),
        )


def get_from_json(x_str: str) -> QuarkUnit:
    x_dict = get_dict_from_json(x_str)
    x_quark = quarkunit_shop(category=x_dict["category"], crud_text=x_dict["crud_text"])
    for x_key, x_value in x_dict["required_args"].items():
        x_quark.set_required_arg(x_key, x_value)
    for x_key, x_value in x_dict["optional_args"].items():
        x_quark.set_optional_arg(x_key, x_value)
    return x_quark


def _modify_agenda_update_agendaunit(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_arg = "_max_tree_traverse"
    if x_quark.get_value(x_arg) != None:
        x_agenda.set_max_tree_traverse(x_quark.get_value(x_arg))
    x_arg = "_party_credor_pool"
    if x_quark.get_value(x_arg) != None:
        x_agenda.set_party_credor_pool(x_quark.get_value(x_arg))
    x_arg = "_party_debtor_pool"
    if x_quark.get_value(x_arg) != None:
        x_agenda.set_party_debtor_pool(x_quark.get_value(x_arg))
    x_arg = "_meld_strategy"
    if x_quark.get_value(x_arg) != None:
        x_agenda.set_meld_strategy(x_quark.get_value(x_arg))
    x_arg = "_weight"
    if x_quark.get_value(x_arg) != None:
        x_agenda._weight = x_quark.get_value(x_arg)
    x_arg = "_planck"
    if x_quark.get_value(x_arg) != None:
        x_agenda._planck = x_quark.get_value(x_arg)
    x_arg = "_penny"
    if x_quark.get_value(x_arg) != None:
        x_agenda._penny = x_quark.get_value(x_arg)


def _modify_agenda_beliefunit_delete(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    belief_id = x_quark.get_value("belief_id")
    x_agenda.del_beliefunit(belief_id)


def _modify_agenda_beliefunit_update(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_beliefunit = x_agenda.get_beliefunit(x_quark.get_value("belief_id"))


def _modify_agenda_beliefunit_insert(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_beliefunit = beliefunit_shop(belief_id=x_quark.get_value("belief_id"))
    x_agenda.set_beliefunit(
        x_beliefunit, create_missing_partys=False, replace=False, add_partylinks=False
    )


def _modify_agenda_belief_partylink_delete(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_party_id = x_quark.get_value("party_id")
    x_belief_id = x_quark.get_value("belief_id")
    x_agenda.get_beliefunit(x_belief_id).del_partylink(x_party_id)


def _modify_agenda_belief_partylink_update(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_beliefunit = x_agenda.get_beliefunit(x_quark.get_value("belief_id"))
    x_beliefunit.edit_partylink(
        party_id=x_quark.get_value("party_id"),
        credor_weight=x_quark.get_value("credor_weight"),
        debtor_weight=x_quark.get_value("debtor_weight"),
    )


def _modify_agenda_belief_partylink_insert(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_beliefunit = x_agenda.get_beliefunit(x_quark.get_value("belief_id"))
    x_beliefunit.set_partylink(
        partylink_shop(
            party_id=x_quark.get_value("party_id"),
            credor_weight=x_quark.get_value("credor_weight"),
            debtor_weight=x_quark.get_value("debtor_weight"),
        )
    )


def _modify_agenda_ideaunit_delete(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    idea_road = create_road(
        x_quark.get_value("parent_road"),
        x_quark.get_value("label"),
        delimiter=x_agenda._road_delimiter,
    )
    x_agenda.del_idea_obj(idea_road, del_children=x_quark.get_value("del_children"))


def _modify_agenda_ideaunit_update(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    idea_road = create_road(
        x_quark.get_value("parent_road"),
        x_quark.get_value("label"),
        delimiter=x_agenda._road_delimiter,
    )
    x_agenda.edit_idea_attr(
        road=idea_road,
        addin=x_quark.get_value("_addin"),
        begin=x_quark.get_value("_begin"),
        close=x_quark.get_value("_close"),
        denom=x_quark.get_value("_denom"),
        meld_strategy=x_quark.get_value("_meld_strategy"),
        numeric_road=x_quark.get_value("_numeric_road"),
        numor=x_quark.get_value("_numor"),
        range_source_road=x_quark.get_value("_range_source_road"),
        reest=x_quark.get_value("_reest"),
        weight=x_quark.get_value("_weight"),
        pledge=x_quark.get_value("pledge"),
    )


def _modify_agenda_ideaunit_insert(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_agenda.add_idea(
        idea_kid=ideaunit_shop(
            _label=x_quark.get_value("label"),
            _addin=x_quark.get_value("_addin"),
            _begin=x_quark.get_value("_begin"),
            _close=x_quark.get_value("_close"),
            _denom=x_quark.get_value("_denom"),
            _meld_strategy=x_quark.get_value("_meld_strategy"),
            _numeric_road=x_quark.get_value("_numeric_road"),
            _numor=x_quark.get_value("_numor"),
            pledge=x_quark.get_value("pledge"),
        ),
        parent_road=x_quark.get_value("parent_road"),
        create_missing_ideas=False,
        create_missing_beliefs=False,
        create_missing_ancestors=False,
    )


def _modify_agenda_idea_balancelink_delete(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_agenda.edit_idea_attr(
        road=x_quark.get_value("road"),
        balancelink_del=x_quark.get_value("belief_id"),
    )


def _modify_agenda_idea_balancelink_update(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_idea = x_agenda.get_idea_obj(x_quark.get_value("road"))
    x_balancelink = x_idea._balancelinks.get(x_quark.get_value("belief_id"))
    x_credor_weight = x_quark.get_value("credor_weight")
    if x_credor_weight != None and x_balancelink.credor_weight != x_credor_weight:
        x_balancelink.credor_weight = x_credor_weight
    x_debtor_weight = x_quark.get_value("debtor_weight")
    if x_debtor_weight != None and x_balancelink.debtor_weight != x_debtor_weight:
        x_balancelink.debtor_weight = x_debtor_weight
    x_agenda.edit_idea_attr(x_quark.get_value("road"), balancelink=x_balancelink)


def _modify_agenda_idea_balancelink_insert(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_balancelink = balancelink_shop(
        belief_id=x_quark.get_value("belief_id"),
        credor_weight=x_quark.get_value("credor_weight"),
        debtor_weight=x_quark.get_value("debtor_weight"),
    )
    x_agenda.edit_idea_attr(x_quark.get_value("road"), balancelink=x_balancelink)


def _modify_agenda_idea_factunit_delete(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_ideaunit = x_agenda.get_idea_obj(x_quark.get_value("road"))
    x_ideaunit.del_factunit(x_quark.get_value("base"))


def _modify_agenda_idea_factunit_update(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_ideaunit = x_agenda.get_idea_obj(x_quark.get_value("road"))
    x_factunit = x_ideaunit._factunits.get(x_quark.get_value("base"))
    x_factunit.set_attr(
        pick=x_quark.get_value("pick"),
        open=x_quark.get_value("open"),
        nigh=x_quark.get_value("nigh"),
    )
    # x_ideaunit.set_factunit(x_factunit)


def _modify_agenda_idea_factunit_insert(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_agenda.edit_idea_attr(
        road=x_quark.get_value("road"),
        factunit=factunit_shop(
            base=x_quark.get_value("base"),
            pick=x_quark.get_value("pick"),
            open=x_quark.get_value("open"),
            nigh=x_quark.get_value("nigh"),
        ),
    )


def _modify_agenda_idea_reasonunit_delete(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_ideaunit = x_agenda.get_idea_obj(x_quark.get_value("road"))
    x_ideaunit.del_reasonunit_base(x_quark.get_value("base"))


def _modify_agenda_idea_reasonunit_update(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_agenda.edit_idea_attr(
        road=x_quark.get_value("road"),
        reason_base=x_quark.get_value("base"),
        reason_suff_idea_active=x_quark.get_value("suff_idea_active"),
    )


def _modify_agenda_idea_reasonunit_insert(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_agenda.edit_idea_attr(
        road=x_quark.get_value("road"),
        reason_base=x_quark.get_value("base"),
        reason_suff_idea_active=x_quark.get_value("suff_idea_active"),
    )


def _modify_agenda_idea_reason_premiseunit_delete(
    x_agenda: AgendaUnit, x_quark: QuarkUnit
):
    x_agenda.edit_idea_attr(
        road=x_quark.get_value("road"),
        reason_del_premise_base=x_quark.get_value("base"),
        reason_del_premise_need=x_quark.get_value("need"),
    )


def _modify_agenda_idea_reason_premiseunit_update(
    x_agenda: AgendaUnit, x_quark: QuarkUnit
):
    x_agenda.edit_idea_attr(
        road=x_quark.get_value("road"),
        reason_base=x_quark.get_value("base"),
        reason_premise=x_quark.get_value("need"),
        reason_premise_open=x_quark.get_value("open"),
        reason_premise_nigh=x_quark.get_value("nigh"),
        reason_premise_divisor=x_quark.get_value("divisor"),
    )


def _modify_agenda_idea_reason_premiseunit_insert(
    x_agenda: AgendaUnit, x_quark: QuarkUnit
):
    x_ideaunit = x_agenda.get_idea_obj(x_quark.get_value("road"))
    x_ideaunit.set_reason_premise(
        base=x_quark.get_value("base"),
        premise=x_quark.get_value("need"),
        open=x_quark.get_value("open"),
        nigh=x_quark.get_value("nigh"),
        divisor=x_quark.get_value("divisor"),
    )


def _modify_agenda_idea_suffbelief_delete(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_ideaunit = x_agenda.get_idea_obj(x_quark.get_value("road"))
    x_ideaunit._assignedunit.del_suffbelief(belief_id=x_quark.get_value("belief_id"))


def _modify_agenda_idea_suffbelief_insert(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_ideaunit = x_agenda.get_idea_obj(x_quark.get_value("road"))
    x_ideaunit._assignedunit.set_suffbelief(belief_id=x_quark.get_value("belief_id"))


def _modify_agenda_partyunit_delete(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_agenda.del_partyunit(x_quark.get_value("party_id"))


def _modify_agenda_partyunit_update(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_agenda.edit_partyunit(
        party_id=x_quark.get_value("party_id"),
        credor_weight=x_quark.get_value("credor_weight"),
        debtor_weight=x_quark.get_value("debtor_weight"),
    )


def _modify_agenda_partyunit_insert(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    x_agenda.set_partyunit(
        partyunit_shop(
            party_id=x_quark.get_value("party_id"),
            credor_weight=x_quark.get_value("credor_weight"),
            debtor_weight=x_quark.get_value("debtor_weight"),
        )
    )


def _modify_agenda_agendaunit(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    if x_quark.crud_text == quark_update():
        _modify_agenda_update_agendaunit(x_agenda, x_quark)


def _modify_agenda_beliefunit(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    if x_quark.crud_text == quark_delete():
        _modify_agenda_beliefunit_delete(x_agenda, x_quark)
    elif x_quark.crud_text == quark_update():
        _modify_agenda_beliefunit_update(x_agenda, x_quark)
    elif x_quark.crud_text == quark_insert():
        _modify_agenda_beliefunit_insert(x_agenda, x_quark)


def _modify_agenda_belief_partylink(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    if x_quark.crud_text == quark_delete():
        _modify_agenda_belief_partylink_delete(x_agenda, x_quark)
    elif x_quark.crud_text == quark_update():
        _modify_agenda_belief_partylink_update(x_agenda, x_quark)
    elif x_quark.crud_text == quark_insert():
        _modify_agenda_belief_partylink_insert(x_agenda, x_quark)


def _modify_agenda_ideaunit(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    if x_quark.crud_text == quark_delete():
        _modify_agenda_ideaunit_delete(x_agenda, x_quark)
    elif x_quark.crud_text == quark_update():
        _modify_agenda_ideaunit_update(x_agenda, x_quark)
    elif x_quark.crud_text == quark_insert():
        _modify_agenda_ideaunit_insert(x_agenda, x_quark)


def _modify_agenda_idea_balancelink(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    if x_quark.crud_text == quark_delete():
        _modify_agenda_idea_balancelink_delete(x_agenda, x_quark)
    elif x_quark.crud_text == quark_update():
        _modify_agenda_idea_balancelink_update(x_agenda, x_quark)
    elif x_quark.crud_text == quark_insert():
        _modify_agenda_idea_balancelink_insert(x_agenda, x_quark)


def _modify_agenda_idea_factunit(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    if x_quark.crud_text == quark_delete():
        _modify_agenda_idea_factunit_delete(x_agenda, x_quark)
    elif x_quark.crud_text == quark_update():
        _modify_agenda_idea_factunit_update(x_agenda, x_quark)
    elif x_quark.crud_text == quark_insert():
        _modify_agenda_idea_factunit_insert(x_agenda, x_quark)


def _modify_agenda_idea_reasonunit(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    if x_quark.crud_text == quark_delete():
        _modify_agenda_idea_reasonunit_delete(x_agenda, x_quark)
    elif x_quark.crud_text == quark_update():
        _modify_agenda_idea_reasonunit_update(x_agenda, x_quark)
    elif x_quark.crud_text == quark_insert():
        _modify_agenda_idea_reasonunit_insert(x_agenda, x_quark)


def _modify_agenda_idea_reason_premiseunit(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    if x_quark.crud_text == quark_delete():
        _modify_agenda_idea_reason_premiseunit_delete(x_agenda, x_quark)
    elif x_quark.crud_text == quark_update():
        _modify_agenda_idea_reason_premiseunit_update(x_agenda, x_quark)
    elif x_quark.crud_text == quark_insert():
        _modify_agenda_idea_reason_premiseunit_insert(x_agenda, x_quark)


def _modify_agenda_idea_suffbelief(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    if x_quark.crud_text == quark_delete():
        _modify_agenda_idea_suffbelief_delete(x_agenda, x_quark)
    elif x_quark.crud_text == quark_insert():
        _modify_agenda_idea_suffbelief_insert(x_agenda, x_quark)


def _modify_agenda_partyunit(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    if x_quark.crud_text == quark_delete():
        _modify_agenda_partyunit_delete(x_agenda, x_quark)
    elif x_quark.crud_text == quark_update():
        _modify_agenda_partyunit_update(x_agenda, x_quark)
    elif x_quark.crud_text == quark_insert():
        _modify_agenda_partyunit_insert(x_agenda, x_quark)


def modify_agenda_with_quarkunit(x_agenda: AgendaUnit, x_quark: QuarkUnit):
    if x_quark.category == "agendaunit":
        _modify_agenda_agendaunit(x_agenda, x_quark)
    elif x_quark.category == "agenda_beliefunit":
        _modify_agenda_beliefunit(x_agenda, x_quark)
    elif x_quark.category == "agenda_belief_partylink":
        _modify_agenda_belief_partylink(x_agenda, x_quark)
    elif x_quark.category == "agenda_ideaunit":
        _modify_agenda_ideaunit(x_agenda, x_quark)
    elif x_quark.category == "agenda_idea_balancelink":
        _modify_agenda_idea_balancelink(x_agenda, x_quark)
    elif x_quark.category == "agenda_idea_factunit":
        _modify_agenda_idea_factunit(x_agenda, x_quark)
    elif x_quark.category == "agenda_idea_reasonunit":
        _modify_agenda_idea_reasonunit(x_agenda, x_quark)
    elif x_quark.category == "agenda_idea_reason_premiseunit":
        _modify_agenda_idea_reason_premiseunit(x_agenda, x_quark)
    elif x_quark.category == "agenda_idea_suffbelief":
        _modify_agenda_idea_suffbelief(x_agenda, x_quark)
    elif x_quark.category == "agenda_partyunit":
        _modify_agenda_partyunit(x_agenda, x_quark)


def optional_args_different(category: str, x_obj: any, y_obj: any) -> bool:
    if category == "agendaunit":
        return (
            x_obj._weight != y_obj._weight
            or x_obj._max_tree_traverse != y_obj._max_tree_traverse
            or x_obj._meld_strategy != y_obj._meld_strategy
            or x_obj._party_credor_pool != y_obj._party_credor_pool
            or x_obj._party_debtor_pool != y_obj._party_debtor_pool
            or x_obj._planck != y_obj._planck
        )
    elif category in {"agenda_belief_partylink", "agenda_idea_balancelink"}:
        return (x_obj.credor_weight != y_obj.credor_weight) or (
            x_obj.debtor_weight != y_obj.debtor_weight
        )
    elif category == "agenda_ideaunit":
        return (
            x_obj._addin != y_obj._addin
            or x_obj._begin != y_obj._begin
            or x_obj._close != y_obj._close
            or x_obj._denom != y_obj._denom
            or x_obj._meld_strategy != y_obj._meld_strategy
            or x_obj._numeric_road != y_obj._numeric_road
            or x_obj._numor != y_obj._numor
            or x_obj._range_source_road != y_obj._range_source_road
            or x_obj._reest != y_obj._reest
            or x_obj._weight != y_obj._weight
            or x_obj.pledge != y_obj.pledge
        )
    elif category == "agenda_idea_factunit":
        return (
            (x_obj.pick != y_obj.pick)
            or (x_obj.open != y_obj.open)
            or (x_obj.nigh != y_obj.nigh)
        )
    elif category == "agenda_idea_reasonunit":
        return x_obj.suff_idea_active != y_obj.suff_idea_active
    elif category == "agenda_idea_reason_premiseunit":
        return (
            x_obj.open != y_obj.open
            or x_obj.nigh != y_obj.nigh
            or x_obj.divisor != y_obj.divisor
        )
    elif category == "agenda_partyunit":
        return (x_obj.credor_weight != y_obj.credor_weight) or (
            x_obj.debtor_weight != y_obj.debtor_weight
        )


class InvalidQuarkUnitException(Exception):
    pass


def get_category_from_dict(x_row_dict: dict) -> str:
    x_category_ref = category_ref()
    for x_columnname in x_row_dict:
        for x_category in x_category_ref:
            if x_columnname.find(x_category) == 0:
                category_len = len(x_category)
                return x_category, x_columnname[category_len + 1 : category_len + 7]


def get_quarkunit_from_rowdata(x_rowdata: RowData) -> QuarkUnit:
    category_text, crud_text = get_category_from_dict(x_rowdata.row_dict)
    x_quark = quarkunit_shop(category=category_text, crud_text=crud_text)
    front_len = len(category_text) + len(crud_text) + 2
    for x_columnname, x_value in x_rowdata.row_dict.items():
        arg_key = x_columnname[front_len:]
        x_quark.set_arg(x_key=arg_key, x_value=x_value)
    return x_quark
