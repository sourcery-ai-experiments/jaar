from src._road.road import create_road
from src.agenda.reason_idea import beliefunit_shop
from src.agenda.agenda import AgendaUnit
from src.agenda.idea import ideaunit_shop
from src.agenda.party import partyunit_shop, partylink_shop
from src.agenda.group import groupunit_shop, balancelink_shop
from src.agenda.examples.agenda_env import get_codespace_agenda_dir
from src._instrument.python import (
    get_empty_dict_if_none,
    get_json_from_dict,
    get_dict_from_json,
)
from src._instrument.sqlite import create_insert_sqlstr, RowData
from src._instrument.file import open_file, save_file
from dataclasses import dataclass


class CRUD_command(str):
    pass


def atom_update() -> CRUD_command:
    return "UPDATE"


def atom_insert() -> CRUD_command:
    return "INSERT"


def atom_delete() -> CRUD_command:
    return "DELETE"


def atom_hx_table_name() -> str:
    return "atom_hx"


def atom_mstr_table_name() -> str:
    return "atom_mstr"


def get_atom_config_file_name() -> str:
    return "atom_config.json"


def get_atom_config_dict() -> dict:
    return get_dict_from_json(
        open_file(get_codespace_agenda_dir(), get_atom_config_file_name())
    )


def add_to_atom_table_columns(x_dict, atom_category, crud, arg_key, arg_value):
    x_dict[f"{atom_category}_{crud}_{arg_key}"] = arg_value.get("sqlite_datatype")


def get_atom_columns_build() -> dict[str:]:
    required_args_text = "required_args"
    optional_args_text = "optional_args"
    atom_table_columns = {}
    atom_config = get_atom_config_dict()
    for atom_category, category_dict in atom_config.items():
        catergory_insert = category_dict.get(atom_insert())
        catergory_update = category_dict.get(atom_update())
        catergory_delete = category_dict.get(atom_delete())
        if catergory_insert != None:
            required_args = category_dict.get(required_args_text)
            optional_args = category_dict.get(optional_args_text)
            for required_arg, x_value in required_args.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_insert(),
                    required_arg,
                    x_value,
                )
            for optional_arg, x_value in optional_args.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_insert(),
                    optional_arg,
                    x_value,
                )
        if catergory_update != None:
            required_args = category_dict.get(required_args_text)
            optional_args = category_dict.get(optional_args_text)
            for required_arg, x_value in required_args.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_update(),
                    required_arg,
                    x_value,
                )
            for optional_arg, x_value in optional_args.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_update(),
                    optional_arg,
                    x_value,
                )
        if catergory_delete != None:
            required_args = category_dict.get(required_args_text)
            optional_args = category_dict.get(optional_args_text)
            for required_arg, x_value in required_args.items():
                add_to_atom_table_columns(
                    atom_table_columns,
                    atom_category,
                    atom_delete(),
                    required_arg,
                    x_value,
                )
    return atom_table_columns


def save_atom_config_file(atom_config_dict):
    save_file(
        dest_dir=get_codespace_agenda_dir(),
        file_name=get_atom_config_file_name(),
        file_text=get_json_from_dict(atom_config_dict),
    )


def category_ref() -> set:
    return get_atom_config_dict().keys()


def is_category_ref(category_text: str) -> bool:
    return category_text in category_ref()


def get_atom_order(
    category: str,
    crud_text: str,
    atom_order_text: str,
    expected_atom_order: int = None,
) -> int:
    atom_config_dict = get_atom_config_dict()
    category_dict = atom_config_dict.get(category)
    crud_dict = category_dict.get(crud_text)
    return crud_dict.get(atom_order_text)


def set_mog(
    category: str,
    crud_text: str,
    atom_order_text: str,
    atom_order_int: int,
) -> int:
    atom_config_dict = get_atom_config_dict()
    category_dict = atom_config_dict.get(category)
    crud_dict = category_dict.get(crud_text)
    crud_dict[atom_order_text] = atom_order_int
    save_atom_config_file(atom_config_dict)


class AgendaAtomDescriptionException(Exception):
    pass


@dataclass
class AgendaAtom:
    category: str = None
    crud_text: str = None
    required_args: dict[str:str] = None
    optional_args: dict[str:str] = None
    atom_order: int = None

    def get_insert_sqlstr(self) -> str:
        if self.is_valid() == False:
            raise AgendaAtomDescriptionException(
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
        return create_insert_sqlstr(atom_hx_table_name(), x_columns, x_values)

    def get_description(self) -> str:
        if self.is_valid() == False:
            raise AgendaAtomDescriptionException("agendaatom is not valid")

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

    def set_atom_order(self):
        self.atom_order = get_atom_order(
            category=self.category,
            crud_text=self.crud_text,
            atom_order_text="atom_order",
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
        return get_atom_config_dict().get(self.category)

    def _get_crud_dict(self) -> dict:
        return self._get_category_dict().get(self.crud_text)

    def _get_required_args_dict(self) -> dict:
        return self._get_category_dict().get("required_args")

    def _get_optional_args_dict(self) -> dict:
        return get_empty_dict_if_none(self._get_category_dict().get("optional_args"))

    def is_required_args_valid(self) -> bool:
        if self.crud_text not in {atom_delete(), atom_insert(), atom_update()}:
            return False
        required_args_dict = self._get_required_args_dict()
        return required_args_dict.keys() == self.required_args.keys()

    def is_optional_args_valid(self) -> bool:
        if self.crud_text not in {atom_delete(), atom_insert(), atom_update()}:
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


def agendaatom_shop(
    category: str,
    crud_text: str = None,
    required_args: dict[str:str] = None,
    optional_args: dict[str:str] = None,
) -> AgendaAtom:
    if is_category_ref(category):
        return AgendaAtom(
            category=category,
            crud_text=crud_text,
            required_args=get_empty_dict_if_none(required_args),
            optional_args=get_empty_dict_if_none(optional_args),
        )


def get_from_json(x_str: str) -> AgendaAtom:
    x_dict = get_dict_from_json(x_str)
    x_agendaatom = agendaatom_shop(
        category=x_dict["category"], crud_text=x_dict["crud_text"]
    )
    for x_key, x_value in x_dict["required_args"].items():
        x_agendaatom.set_required_arg(x_key, x_value)
    for x_key, x_value in x_dict["optional_args"].items():
        x_agendaatom.set_optional_arg(x_key, x_value)
    return x_agendaatom


def modify_agenda_with_agendaatom(x_agenda: AgendaUnit, x_agendaatom: AgendaAtom):
    # sourcery skip: extract-method
    xs = x_agendaatom
    if xs.category == "agendaunit" and xs.crud_text == atom_update():
        x_arg = "_max_tree_traverse"
        if xs.get_value(x_arg) != None:
            x_agenda.set_max_tree_traverse(xs.get_value(x_arg))
        x_arg = "_party_creditor_pool"
        if xs.get_value(x_arg) != None:
            x_agenda.set_party_creditor_pool(xs.get_value(x_arg))
        x_arg = "_party_debtor_pool"
        if xs.get_value(x_arg) != None:
            x_agenda.set_party_debtor_pool(xs.get_value(x_arg))
        x_arg = "_meld_strategy"
        if xs.get_value(x_arg) != None:
            x_agenda.set_meld_strategy(xs.get_value(x_arg))
        x_arg = "_weight"
        if xs.get_value(x_arg) != None:
            x_agenda._weight = xs.get_value(x_arg)
        x_arg = "_planck"
        if xs.get_value(x_arg) != None:
            x_agenda._planck = xs.get_value(x_arg)
    elif xs.category == "agenda_groupunit" and xs.crud_text == atom_delete():
        group_id = xs.get_value("group_id")
        x_agenda.del_groupunit(group_id)
    elif xs.category == "agenda_groupunit" and xs.crud_text == atom_update():
        x_groupunit = x_agenda.get_groupunit(xs.get_value("group_id"))
        x_groupunit._treasury_partylinks = xs.get_value("_treasury_partylinks")
    elif xs.category == "agenda_groupunit" and xs.crud_text == atom_insert():
        x_agenda.set_groupunit(
            groupunit_shop(
                group_id=xs.get_value("group_id"),
                _treasury_partylinks=xs.get_value("_treasury_partylinks"),
            ),
            create_missing_partys=False,
            replace=False,
            add_partylinks=False,
        )
    elif xs.category == "agenda_group_partylink" and xs.crud_text == atom_delete():
        x_agenda.get_groupunit(xs.get_value("group_id")).del_partylink(
            xs.get_value("party_id")
        )
    elif xs.category == "agenda_group_partylink" and xs.crud_text == atom_update():
        x_groupunit = x_agenda.get_groupunit(xs.get_value("group_id"))
        x_groupunit.edit_partylink(
            party_id=xs.get_value("party_id"),
            creditor_weight=xs.get_value("creditor_weight"),
            debtor_weight=xs.get_value("debtor_weight"),
        )
    elif xs.category == "agenda_group_partylink" and xs.crud_text == atom_insert():
        x_groupunit = x_agenda.get_groupunit(xs.get_value("group_id"))
        x_groupunit.set_partylink(
            partylink_shop(
                party_id=xs.get_value("party_id"),
                creditor_weight=xs.get_value("creditor_weight"),
                debtor_weight=xs.get_value("debtor_weight"),
            )
        )
    elif xs.category == "agenda_ideaunit" and xs.crud_text == atom_delete():
        idea_road = create_road(
            xs.get_value("parent_road"),
            xs.get_value("label"),
            delimiter=x_agenda._road_delimiter,
        )
        x_agenda.del_idea_obj(road=idea_road, del_children=xs.get_value("del_children"))
    elif xs.category == "agenda_ideaunit" and xs.crud_text == atom_update():
        idea_road = create_road(
            xs.get_value("parent_road"),
            xs.get_value("label"),
            delimiter=x_agenda._road_delimiter,
        )
        x_agenda.edit_idea_attr(
            road=idea_road,
            addin=xs.get_value("_addin"),
            begin=xs.get_value("_begin"),
            close=xs.get_value("_close"),
            denom=xs.get_value("_denom"),
            meld_strategy=xs.get_value("_meld_strategy"),
            numeric_road=xs.get_value("_numeric_road"),
            numor=xs.get_value("_numor"),
            range_source_road=xs.get_value("_range_source_road"),
            reest=xs.get_value("_reest"),
            weight=xs.get_value("_weight"),
            pledge=xs.get_value("pledge"),
        )
    elif xs.category == "agenda_ideaunit" and xs.crud_text == atom_insert():
        x_agenda.add_idea(
            idea_kid=ideaunit_shop(
                _label=xs.get_value("label"),
                _addin=xs.get_value("_addin"),
                _begin=xs.get_value("_begin"),
                _close=xs.get_value("_close"),
                _denom=xs.get_value("_denom"),
                _meld_strategy=xs.get_value("_meld_strategy"),
                _numeric_road=xs.get_value("_numeric_road"),
                _numor=xs.get_value("_numor"),
                pledge=xs.get_value("pledge"),
            ),
            parent_road=xs.get_value("parent_road"),
            create_missing_ideas=False,
            create_missing_groups=False,
            create_missing_ancestors=False,
        )
    elif xs.category == "agenda_idea_balancelink" and xs.crud_text == atom_delete():
        x_agenda.edit_idea_attr(
            road=xs.get_value("road"), balancelink_del=xs.get_value("group_id")
        )
    elif xs.category == "agenda_idea_balancelink" and xs.crud_text == atom_update():
        x_idea = x_agenda.get_idea_obj(xs.get_value("road"))
        x_balancelink = x_idea._balancelinks.get(xs.get_value("group_id"))
        x_creditor_weight = xs.get_value("creditor_weight")
        if (
            x_creditor_weight != None
            and x_balancelink.creditor_weight != x_creditor_weight
        ):
            x_balancelink.creditor_weight = x_creditor_weight
        x_debtor_weight = xs.get_value("debtor_weight")
        if x_debtor_weight != None and x_balancelink.debtor_weight != x_debtor_weight:
            x_balancelink.debtor_weight = x_debtor_weight
        x_agenda.edit_idea_attr(xs.get_value("road"), balancelink=x_balancelink)
    elif xs.category == "agenda_idea_balancelink" and xs.crud_text == atom_insert():
        x_balancelink = balancelink_shop(
            group_id=xs.get_value("group_id"),
            creditor_weight=xs.get_value("creditor_weight"),
            debtor_weight=xs.get_value("debtor_weight"),
        )
        x_agenda.edit_idea_attr(xs.get_value("road"), balancelink=x_balancelink)
    elif xs.category == "agenda_idea_beliefunit" and xs.crud_text == atom_delete():
        x_ideaunit = x_agenda.get_idea_obj(xs.get_value("road"))
        x_ideaunit.del_beliefunit(xs.get_value("base"))
    elif xs.category == "agenda_idea_beliefunit" and xs.crud_text == atom_update():
        x_ideaunit = x_agenda.get_idea_obj(xs.get_value("road"))
        x_beliefunit = x_ideaunit._beliefunits.get(xs.get_value("base"))
        x_beliefunit.set_attr(
            pick=xs.get_value("pick"),
            open=xs.get_value("open"),
            nigh=xs.get_value("nigh"),
        )
        # x_ideaunit.set_beliefunit(x_beliefunit)
    elif xs.category == "agenda_idea_beliefunit" and xs.crud_text == atom_insert():
        x_agenda.edit_idea_attr(
            road=xs.get_value("road"),
            beliefunit=beliefunit_shop(
                base=xs.get_value("base"),
                pick=xs.get_value("pick"),
                open=xs.get_value("open"),
                nigh=xs.get_value("nigh"),
            ),
        )
    elif xs.category == "agenda_idea_reasonunit" and xs.crud_text == atom_delete():
        x_ideaunit = x_agenda.get_idea_obj(xs.get_value("road"))
        x_ideaunit.del_reasonunit_base(xs.get_value("base"))
    elif xs.category == "agenda_idea_reasonunit" and xs.crud_text == atom_update():
        x_agenda.edit_idea_attr(
            road=xs.get_value("road"),
            reason_base=xs.get_value("base"),
            reason_suff_idea_active=xs.get_value("suff_idea_active"),
        )
    elif xs.category == "agenda_idea_reasonunit" and xs.crud_text == atom_insert():
        x_agenda.edit_idea_attr(
            road=xs.get_value("road"),
            reason_base=xs.get_value("base"),
            reason_suff_idea_active=xs.get_value("suff_idea_active"),
        )
    elif (
        xs.category == "agenda_idea_reason_premiseunit"
        and xs.crud_text == atom_delete()
    ):
        x_agenda.edit_idea_attr(
            road=xs.get_value("road"),
            reason_del_premise_base=xs.get_value("base"),
            reason_del_premise_need=xs.get_value("need"),
        )
    elif (
        xs.category == "agenda_idea_reason_premiseunit"
        and xs.crud_text == atom_update()
    ):
        x_agenda.edit_idea_attr(
            road=xs.get_value("road"),
            reason_base=xs.get_value("base"),
            reason_premise=xs.get_value("need"),
            reason_premise_open=xs.get_value("open"),
            reason_premise_nigh=xs.get_value("nigh"),
            reason_premise_divisor=xs.get_value("divisor"),
        )
    elif (
        xs.category == "agenda_idea_reason_premiseunit"
        and xs.crud_text == atom_insert()
    ):
        x_ideaunit = x_agenda.get_idea_obj(xs.get_value("road"))
        x_ideaunit.set_reason_premise(
            base=xs.get_value("base"),
            premise=xs.get_value("need"),
            open=xs.get_value("open"),
            nigh=xs.get_value("nigh"),
            divisor=xs.get_value("divisor"),
        )
    elif xs.category == "agenda_idea_suffgroup" and xs.crud_text == atom_delete():
        x_ideaunit = x_agenda.get_idea_obj(xs.get_value("road"))
        x_ideaunit._assignedunit.del_suffgroup(group_id=xs.get_value("group_id"))
    elif xs.category == "agenda_idea_suffgroup" and xs.crud_text == atom_insert():
        x_ideaunit = x_agenda.get_idea_obj(xs.get_value("road"))
        x_ideaunit._assignedunit.set_suffgroup(group_id=xs.get_value("group_id"))
    elif xs.category == "agenda_partyunit" and xs.crud_text == atom_delete():
        x_agenda.del_partyunit(xs.get_value("party_id"))
    elif xs.category == "agenda_partyunit" and xs.crud_text == atom_update():
        x_agenda.edit_partyunit(
            party_id=xs.get_value("party_id"),
            creditor_weight=xs.get_value("creditor_weight"),
            debtor_weight=xs.get_value("debtor_weight"),
        )
    elif xs.category == "agenda_partyunit" and xs.crud_text == atom_insert():
        x_agenda.set_partyunit(
            partyunit_shop(
                party_id=xs.get_value("party_id"),
                creditor_weight=xs.get_value("creditor_weight"),
                debtor_weight=xs.get_value("debtor_weight"),
            )
        )


def optional_args_different(category: str, x_obj: any, y_obj: any) -> bool:
    if category == "agendaunit":
        return (
            x_obj._weight != y_obj._weight
            or x_obj._max_tree_traverse != y_obj._max_tree_traverse
            or x_obj._meld_strategy != y_obj._meld_strategy
            or x_obj._party_creditor_pool != y_obj._party_creditor_pool
            or x_obj._party_debtor_pool != y_obj._party_debtor_pool
            or x_obj._planck != y_obj._planck
        )
    elif category == "agenda_groupunit":
        return x_obj._treasury_partylinks != y_obj._treasury_partylinks
    elif category in {"agenda_group_partylink", "agenda_idea_balancelink"}:
        return (x_obj.creditor_weight != y_obj.creditor_weight) or (
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
    elif category == "agenda_idea_beliefunit":
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
        return (x_obj.creditor_weight != y_obj.creditor_weight) or (
            x_obj.debtor_weight != y_obj.debtor_weight
        )


class InvalidAgendaAtomException(Exception):
    pass


def get_category_from_dict(x_row_dict: dict) -> str:
    x_category_ref = category_ref()
    for x_columnname in x_row_dict:
        for x_category in x_category_ref:
            if x_columnname.find(x_category) == 0:
                category_len = len(x_category)
                return x_category, x_columnname[category_len + 1 : category_len + 7]


def get_agendaatom_from_rowdata(x_rowdata: RowData) -> AgendaAtom:
    category_text, crud_text = get_category_from_dict(x_rowdata.row_dict)
    x_agendaatom = agendaatom_shop(category=category_text, crud_text=crud_text)
    front_len = len(category_text) + len(crud_text) + 2
    for x_columnname, x_value in x_rowdata.row_dict.items():
        arg_key = x_columnname[front_len:]
        x_agendaatom.set_arg(x_key=arg_key, x_value=x_value)
    return x_agendaatom
