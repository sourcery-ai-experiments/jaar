from src._road.road import PersonRoad, RoadUnit
from src.agenda.reason_idea import beliefunit_shop, BeliefUnit, PremiseUnit, ReasonUnit
from src.agenda.party import (
    partyunit_shop,
    partylink_shop,
    PartyUnit,
    PartyLink,
    PartyID,
)
from src.agenda.group import (
    groupunit_shop,
    balancelink_shop,
    GroupUnit,
    GroupID,
    BalanceLink,
)
from src.agenda.idea import ideaunit_shop, IdeaUnit
from src.agenda.agenda import AgendaUnit
from src.agenda.examples.agenda_env import get_codespace_agenda_dir
from src.instrument.python import (
    get_empty_dict_if_none,
    x_get_json,
    x_get_dict,
    place_obj_in_dict,
    get_nested_value,
    get_all_nondictionary_objs,
)
from src.instrument.sqlite import create_insert_sqlstr, RowData
from src.instrument.file import open_file, save_file
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


def atom_update() -> str:
    return "UPDATE"


def atom_insert() -> str:
    return "INSERT"


def atom_delete() -> str:
    return "DELETE"


def atom_hx_table_name() -> str:
    return "atom_hx"


def atom_curr_table_name() -> str:
    return "atom_curr"


def get_atom_config_file_name() -> str:
    return "atom_config.json"


def get_atom_config_dict() -> dict:
    return x_get_dict(
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
            required_args = catergory_insert.get(required_args_text)
            optional_args = catergory_insert.get(optional_args_text)
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
            required_args = catergory_update.get(required_args_text)
            optional_args = catergory_update.get(optional_args_text)
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
            required_args = catergory_delete.get(required_args_text)
            optional_args = catergory_delete.get(optional_args_text)
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
        file_text=x_get_json(atom_config_dict),
    )


def category_ref() -> set:
    return get_atom_config_dict().keys()


def is_category_ref(category_text: str) -> bool:
    return category_text in category_ref()


def get_mog(
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
    locator: dict[str:str] = None
    required_args: dict[str:str] = None
    optional_args: dict[str:str] = None
    atom_order: int = None
    _crud_cache: str = None

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
        self.atom_order = get_mog(
            category=self.category,
            crud_text=self.crud_text,
            atom_order_text="atom_order",
        )

    def set_locator(self, x_key: str, x_value: any):
        self.locator[x_key] = x_value

    def get_locator(self, x_key: str) -> any:
        return self.locator.get(x_key)

    def is_locator_valid(self) -> bool:
        return self._get_locator_args_dict().keys() == self.locator.keys()

    def _get_locator_args_dict(self) -> dict:
        return get_empty_dict_if_none(self._get_category_dict().get("locator"))

    def set_arg(self, x_key: str, x_value: any):
        for required_arg in self._get_required_args_dict():
            if x_key == required_arg:
                self.set_required_arg(x_key, x_value)
        for optional_arg in self._get_optional_args_dict():
            if x_key == optional_arg:
                self.set_optional_arg(x_key, x_value)
        for locator_arg in self._get_locator_args_dict():
            if x_key == locator_arg:
                self.set_locator(x_key, x_value)

    def set_required_arg(self, x_key: str, x_value: any):
        self.required_args[x_key] = x_value

    def set_optional_arg(self, x_key: str, x_value: any):
        self.optional_args[x_key] = x_value

    def _get_category_dict(self) -> dict:
        if self._crud_cache is None:
            self._crud_cache = get_atom_config_dict()
        return self._crud_cache.get(self.category)

    def _get_crud_dict(self) -> dict:
        return self._get_category_dict().get(self.crud_text)

    def _get_required_args_dict(self) -> dict:
        return self._get_crud_dict().get("required_args")

    def _get_optional_args_dict(self) -> dict:
        crud_dict = self._get_category_dict().get(self.crud_text)
        return get_empty_dict_if_none(crud_dict.get("optional_args"))

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
        return (
            self.is_locator_valid()
            and self.is_required_args_valid()
            and self.is_optional_args_valid()
        )

    def get_value(self, arg_key: str) -> any:
        required_value = self.required_args.get(arg_key)
        if required_value is None:
            return self.optional_args.get(arg_key)
        return required_value


def agendaatom_shop(
    category: str,
    crud_text: str = None,
    locator: dict[str:str] = None,
    required_args: dict[str:str] = None,
    optional_args: dict[str:str] = None,
) -> AgendaAtom:
    if is_category_ref(category):
        return AgendaAtom(
            category=category,
            crud_text=crud_text,
            locator=get_empty_dict_if_none(locator),
            required_args=get_empty_dict_if_none(required_args),
            optional_args=get_empty_dict_if_none(optional_args),
        )


def change_agenda_with_agendaatom(x_agenda: AgendaUnit, x_agendaatom: AgendaAtom):
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
    elif xs.category == "agenda_groupunit" and xs.crud_text == atom_delete():
        group_id = xs.get_locator("group_id")
        x_agenda.del_groupunit(group_id)
    elif xs.category == "agenda_groupunit" and xs.crud_text == atom_update():
        x_groupunit = x_agenda.get_groupunit(xs.get_value("group_id"))
        x_groupunit._treasury_partylinks = xs.get_value("_treasury_partylinks")
    elif xs.category == "agenda_groupunit" and xs.crud_text == atom_insert():
        x_agenda.set_groupunit(
            groupunit_shop(
                group_id=xs.get_locator("group_id"),
                _treasury_partylinks=xs.get_locator("_treasury_partylinks"),
            ),
            create_missing_partys=False,
            replace=False,
            add_partylinks=False,
        )
    elif xs.category == "agenda_group_partylink" and xs.crud_text == atom_delete():
        x_agenda.get_groupunit(xs.get_locator("group_id")).del_partylink(
            xs.get_locator("party_id")
        )
    elif xs.category == "agenda_group_partylink" and xs.crud_text == atom_update():
        x_groupunit = x_agenda.get_groupunit(xs.get_value("group_id"))
        x_groupunit.edit_partylink(
            party_id=xs.get_value("party_id"),
            creditor_weight=xs.get_value("creditor_weight"),
            debtor_weight=xs.get_value("debtor_weight"),
        )
    elif xs.category == "agenda_group_partylink" and xs.crud_text == atom_insert():
        x_groupunit = x_agenda.get_groupunit(xs.get_locator("group_id"))
        x_groupunit.set_partylink(
            partylink_shop(
                party_id=xs.get_locator("party_id"),
                creditor_weight=xs.get_value("creditor_weight"),
                debtor_weight=xs.get_value("debtor_weight"),
            )
        )
    elif xs.category == "agenda_ideaunit" and xs.crud_text == atom_delete():
        x_agenda.del_idea_obj(
            road=xs.get_locator("road"), del_children=xs.get_value("del_children")
        )
    elif xs.category == "agenda_ideaunit" and xs.crud_text == atom_update():
        x_agenda.edit_idea_attr(
            road=xs.get_value("road"),
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
            promise=xs.get_value("promise"),
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
                promise=xs.get_value("promise"),
            ),
            parent_road=xs.get_value("parent_road"),
            create_missing_ideas_groups=False,
            create_missing_ancestors=False,
        )
    elif xs.category == "agenda_idea_balancelink" and xs.crud_text == atom_delete():
        x_agenda.edit_idea_attr(
            road=xs.get_locator("road"), balancelink_del=xs.get_value("group_id")
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
        x_agenda.del_partyunit(xs.get_locator("party_id"))
    elif xs.category == "agenda_partyunit" and xs.crud_text == atom_update():
        x_agenda.edit_partyunit(
            party_id=xs.get_value("party_id"),
            creditor_weight=xs.get_value("creditor_weight"),
            debtor_weight=xs.get_value("debtor_weight"),
            depotlink_type=xs.get_value("depotlink_type"),
        )
    elif xs.category == "agenda_partyunit" and xs.crud_text == atom_insert():
        x_agenda.set_partyunit(
            partyunit_shop(
                party_id=xs.get_value("party_id"),
                creditor_weight=xs.get_value("creditor_weight"),
                debtor_weight=xs.get_value("debtor_weight"),
                depotlink_type=xs.get_value("depotlink_type"),
            )
        )


def optional_args_different(category: str, x_obj: any, y_obj: any) -> bool:
    if category == "agendaunit":
        return (
            x_obj._weight != y_obj._weight
            or x_obj._auto_output_job_to_forum != y_obj._auto_output_job_to_forum
            or x_obj._max_tree_traverse != y_obj._max_tree_traverse
            or x_obj._meld_strategy != y_obj._meld_strategy
            or x_obj._party_creditor_pool != y_obj._party_creditor_pool
            or x_obj._party_debtor_pool != y_obj._party_debtor_pool
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
            or x_obj.promise != y_obj.promise
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
        return (
            (x_obj.creditor_weight != y_obj.creditor_weight)
            or (x_obj.debtor_weight != y_obj.debtor_weight)
            or (x_obj.depotlink_type != y_obj.depotlink_type)
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


@dataclass
class BookUnit:
    agendaatoms: dict[str : dict[str:any]] = None

    def get_atom_order_agendaatom_dict(self) -> dict[int:AgendaAtom]:
        return get_all_nondictionary_objs(self.agendaatoms)

    def get_after_agenda(self, before_agenda: AgendaUnit):
        after_agenda = copy_deepcopy(before_agenda)
        agendaatoms_by_order = self.get_atom_order_agendaatom_dict()

        for x_atom_order_int in sorted(agendaatoms_by_order.keys()):
            agendaatoms_list = agendaatoms_by_order.get(x_atom_order_int)
            for x_agendaatom in agendaatoms_list:
                change_agenda_with_agendaatom(after_agenda, x_agendaatom)
        return after_agenda

    def set_agendaatom(self, x_agendaatom: AgendaAtom):
        if x_agendaatom.is_valid() == False:
            raise InvalidAgendaAtomException(
                f"""'{x_agendaatom.category}' {x_agendaatom.crud_text} AgendaAtom is invalid
                {x_agendaatom.is_locator_valid()=}
                {x_agendaatom.is_required_args_valid()=}
                {x_agendaatom.is_optional_args_valid()=}"""
            )

        x_agendaatom.set_atom_order()
        x_keylist = [
            x_agendaatom.crud_text,
            x_agendaatom.category,
            *list(x_agendaatom.locator.values()),
        ]
        place_obj_in_dict(self.agendaatoms, x_keylist, x_agendaatom)

    def add_agendaatom(
        self,
        category: str,
        crud_text: str,
        locator: str = None,
        required_args: str = None,
        optional_args: str = None,
    ):
        x_agendaatom = agendaatom_shop(
            category=category,
            crud_text=crud_text,
            locator=locator,
            required_args=required_args,
            optional_args=optional_args,
        )
        self.set_agendaatom(x_agendaatom)

    def get_agendaatom(
        self, crud_text: str, category: str, locator_values: list[str]
    ) -> AgendaAtom:
        x_keylist = [crud_text, category, *locator_values]
        return get_nested_value(self.agendaatoms, x_keylist)

    def add_all_agendaatoms(self, before_agenda: AgendaUnit, after_agenda: AgendaUnit):
        before_agenda.set_agenda_metrics()
        after_agenda.set_agenda_metrics()
        self.add_agendaatoms_agendaunit_simple_attrs(before_agenda, after_agenda)
        self.add_agendaatom_partyunits(before_agenda, after_agenda)
        self.add_agendaatom_groupunits(before_agenda, after_agenda)
        self.add_agendaatoms_ideas(before_agenda, after_agenda)

    def add_agendaatoms_agendaunit_simple_attrs(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        if optional_args_different("agendaunit", before_agenda, after_agenda):
            x_agendaatom = agendaatom_shop("agendaunit", atom_update())
            x_agendaatom.set_optional_arg("_weight", after_agenda._weight)
            x_agendaatom.set_optional_arg(
                "_max_tree_traverse", after_agenda._max_tree_traverse
            )
            x_agendaatom.set_optional_arg(
                "_party_creditor_pool", after_agenda._party_creditor_pool
            )
            x_agendaatom.set_optional_arg(
                "_party_debtor_pool", after_agenda._party_debtor_pool
            )
            x_agendaatom.set_optional_arg(
                "_auto_output_job_to_forum", after_agenda._auto_output_job_to_forum
            )
            x_agendaatom.set_optional_arg("_meld_strategy", after_agenda._meld_strategy)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_partyunits(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        before_party_ids = set(before_agenda._partys.keys())
        after_party_ids = set(after_agenda._partys.keys())

        self.add_agendaatom_partyunit_inserts(
            after_agenda=after_agenda,
            insert_party_ids=after_party_ids.difference(before_party_ids),
        )
        self.add_agendaatom_partyunit_deletes(
            delete_party_ids=before_party_ids.difference(after_party_ids)
        )
        self.add_agendaatom_partyunit_updates(
            before_agenda=before_agenda,
            after_agenda=after_agenda,
            update_party_ids=before_party_ids.intersection(after_party_ids),
        )

    def add_agendaatom_partyunit_inserts(
        self, after_agenda: AgendaUnit, insert_party_ids: set
    ):
        for insert_party_id in insert_party_ids:
            x_partyunit = after_agenda.get_party(insert_party_id)
            x_agendaatom = agendaatom_shop("agenda_partyunit", atom_insert())
            x_agendaatom.set_locator("party_id", x_partyunit.party_id)
            x_agendaatom.set_required_arg("party_id", x_partyunit.party_id)
            if x_partyunit.creditor_weight != None:
                x_agendaatom.set_optional_arg(
                    "creditor_weight", x_partyunit.creditor_weight
                )
            if x_partyunit.debtor_weight != None:
                x_agendaatom.set_optional_arg(
                    "debtor_weight", x_partyunit.debtor_weight
                )
            if x_partyunit.depotlink_type != None:
                x_agendaatom.set_optional_arg(
                    "depotlink_type", x_partyunit.depotlink_type
                )
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_partyunit_updates(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit, update_party_ids: set
    ):
        for party_id in update_party_ids:
            after_partyunit = after_agenda.get_party(party_id)
            before_partyunit = before_agenda.get_party(party_id)
            if optional_args_different(
                "agenda_partyunit", after_partyunit, before_partyunit
            ):
                x_agendaatom = agendaatom_shop("agenda_partyunit", atom_update())
                x_agendaatom.set_locator("party_id", after_partyunit.party_id)
                x_agendaatom.set_required_arg("party_id", after_partyunit.party_id)
                if before_partyunit.creditor_weight != after_partyunit.creditor_weight:
                    x_agendaatom.set_optional_arg(
                        "creditor_weight", after_partyunit.creditor_weight
                    )
                if before_partyunit.debtor_weight != after_partyunit.debtor_weight:
                    x_agendaatom.set_optional_arg(
                        "debtor_weight", after_partyunit.debtor_weight
                    )
                if before_partyunit.depotlink_type != after_partyunit.depotlink_type:
                    x_agendaatom.set_optional_arg(
                        "depotlink_type", after_partyunit.depotlink_type
                    )
                self.set_agendaatom(x_agendaatom)

    def add_agendaatom_partyunit_deletes(self, delete_party_ids: set):
        for delete_party_id in delete_party_ids:
            x_agendaatom = agendaatom_shop("agenda_partyunit", atom_delete())
            x_agendaatom.set_locator("party_id", delete_party_id)
            x_agendaatom.set_required_arg("party_id", delete_party_id)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_groupunits(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        before_group_ids = {
            before_group_id
            for before_group_id in before_agenda._groups.keys()
            if before_agenda.get_groupunit(before_group_id)._party_mirror == False
        }
        after_group_ids = {
            after_group_id
            for after_group_id in after_agenda._groups.keys()
            if after_agenda.get_groupunit(after_group_id)._party_mirror == False
        }

        self.add_agendaatom_groupunit_inserts(
            after_agenda=after_agenda,
            insert_group_ids=after_group_ids.difference(before_group_ids),
        )

        self.add_agendaatom_groupunit_deletes(
            before_agenda=before_agenda,
            delete_group_ids=before_group_ids.difference(after_group_ids),
        )

        self.add_agendaatom_groupunit_updates(
            before_agenda=before_agenda,
            after_agenda=after_agenda,
            update_group_ids=before_group_ids.intersection(after_group_ids),
        )

    def add_agendaatom_groupunit_inserts(
        self, after_agenda: AgendaUnit, insert_group_ids: set
    ):
        for insert_group_id in insert_group_ids:
            insert_groupunit = after_agenda.get_groupunit(insert_group_id)
            x_agendaatom = agendaatom_shop("agenda_groupunit", atom_insert())
            x_agendaatom.set_locator("group_id", insert_groupunit.group_id)
            x_agendaatom.set_required_arg("group_id", insert_groupunit.group_id)
            if insert_groupunit._treasury_partylinks != None:
                x_agendaatom.set_optional_arg(
                    "_treasury_partylinks",
                    insert_groupunit._treasury_partylinks,
                )
            self.set_agendaatom(x_agendaatom)
            self.add_agendaatom_partylinks_inserts(
                after_groupunit=insert_groupunit,
                insert_partylink_party_ids=set(insert_groupunit._partys.keys()),
            )

    def add_agendaatom_groupunit_updates(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit, update_group_ids: set
    ):
        for group_id in update_group_ids:
            after_groupunit = after_agenda.get_groupunit(group_id)
            before_groupunit = before_agenda.get_groupunit(group_id)
            if optional_args_different(
                "agenda_groupunit", before_groupunit, after_groupunit
            ):
                x_agendaatom = agendaatom_shop("agenda_groupunit", atom_update())
                x_agendaatom.set_locator("group_id", after_groupunit.group_id)
                x_agendaatom.set_required_arg("group_id", after_groupunit.group_id)
                x_agendaatom.set_optional_arg(
                    "_treasury_partylinks",
                    after_groupunit._treasury_partylinks,
                )
                self.set_agendaatom(x_agendaatom)

            self.add_agendaatom_groupunit_update_partylinks(
                after_groupunit=after_groupunit, before_groupunit=before_groupunit
            )

    def add_agendaatom_groupunit_update_partylinks(
        self, after_groupunit: GroupUnit, before_groupunit: GroupUnit
    ):
        after_party_ids = set(after_groupunit._partys.keys())
        before_party_ids = set(before_groupunit._partys.keys())

        self.add_agendaatom_partylinks_inserts(
            after_groupunit=after_groupunit,
            insert_partylink_party_ids=after_party_ids.difference(before_party_ids),
        )

        self.add_agendaatom_partylinks_delete(
            before_group_id=before_groupunit.group_id,
            before_party_ids=before_party_ids.difference(after_party_ids),
        )

        update_party_ids = before_party_ids.intersection(after_party_ids)
        for update_party_id in update_party_ids:
            before_partylink = before_groupunit.get_partylink(update_party_id)
            after_partylink = after_groupunit.get_partylink(update_party_id)
            if optional_args_different(
                "agenda_group_partylink", before_partylink, after_partylink
            ):
                self.add_agendaatom_partylink_update(
                    group_id=after_groupunit.group_id,
                    before_partylink=before_partylink,
                    after_partylink=after_partylink,
                )

    def add_agendaatom_groupunit_deletes(
        self, before_agenda: AgendaUnit, delete_group_ids: set
    ):
        for delete_group_id in delete_group_ids:
            x_agendaatom = agendaatom_shop("agenda_groupunit", atom_delete())
            x_agendaatom.set_locator("group_id", delete_group_id)
            x_agendaatom.set_required_arg("group_id", delete_group_id)
            self.set_agendaatom(x_agendaatom)

            delete_groupunit = before_agenda.get_groupunit(delete_group_id)
            self.add_agendaatom_partylinks_delete(
                delete_group_id, set(delete_groupunit._partys.keys())
            )

    def add_agendaatom_partylinks_inserts(
        self,
        after_groupunit: GroupUnit,
        insert_partylink_party_ids: list[PartyID],
    ):
        after_group_id = after_groupunit.group_id
        for insert_party_id in insert_partylink_party_ids:
            after_partylink = after_groupunit.get_partylink(insert_party_id)
            x_agendaatom = agendaatom_shop("agenda_group_partylink", atom_insert())
            x_agendaatom.set_locator("group_id", after_group_id)
            x_agendaatom.set_locator("party_id", after_partylink.party_id)
            x_agendaatom.set_required_arg("group_id", after_group_id)
            x_agendaatom.set_required_arg("party_id", after_partylink.party_id)
            if after_partylink.creditor_weight != None:
                x_agendaatom.set_optional_arg(
                    "creditor_weight", after_partylink.creditor_weight
                )
            if after_partylink.debtor_weight != None:
                x_agendaatom.set_optional_arg(
                    "debtor_weight", after_partylink.debtor_weight
                )
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_partylink_update(
        self,
        group_id: GroupID,
        before_partylink: PartyLink,
        after_partylink: PartyLink,
    ):
        x_agendaatom = agendaatom_shop("agenda_group_partylink", atom_update())
        x_agendaatom.set_locator("group_id", group_id)
        x_agendaatom.set_locator("party_id", after_partylink.party_id)
        x_agendaatom.set_required_arg("group_id", group_id)
        x_agendaatom.set_required_arg("party_id", after_partylink.party_id)
        if after_partylink.creditor_weight != before_partylink.creditor_weight:
            x_agendaatom.set_optional_arg(
                "creditor_weight", after_partylink.creditor_weight
            )
        if after_partylink.debtor_weight != before_partylink.debtor_weight:
            x_agendaatom.set_optional_arg(
                "debtor_weight", after_partylink.debtor_weight
            )
        self.set_agendaatom(x_agendaatom)

    def add_agendaatom_partylinks_delete(
        self, before_group_id: GroupID, before_party_ids: PartyID
    ):
        for delete_party_id in before_party_ids:
            x_agendaatom = agendaatom_shop("agenda_group_partylink", atom_delete())
            x_agendaatom.set_locator("group_id", before_group_id)
            x_agendaatom.set_locator("party_id", delete_party_id)
            x_agendaatom.set_required_arg("group_id", before_group_id)
            x_agendaatom.set_required_arg("party_id", delete_party_id)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatoms_ideas(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit
    ):
        before_idea_roads = set(before_agenda._idea_dict.keys())
        after_idea_roads = set(after_agenda._idea_dict.keys())

        self.add_agendaatom_idea_inserts(
            after_agenda=after_agenda,
            insert_idea_roads=after_idea_roads.difference(before_idea_roads),
        )
        self.add_agendaatom_idea_deletes(
            before_agenda=before_agenda,
            delete_idea_roads=before_idea_roads.difference(after_idea_roads),
        )
        self.add_agendaatom_idea_updates(
            before_agenda=before_agenda,
            after_agenda=after_agenda,
            update_roads=before_idea_roads.intersection(after_idea_roads),
        )

    def add_agendaatom_idea_inserts(
        self, after_agenda: AgendaUnit, insert_idea_roads: set
    ):
        for insert_idea_road in insert_idea_roads:
            insert_ideaunit = after_agenda.get_idea_obj(insert_idea_road)
            x_agendaatom = agendaatom_shop("agenda_ideaunit", atom_insert())
            x_agendaatom.set_locator("road", insert_ideaunit.get_road())
            x_agendaatom.set_required_arg("label", insert_ideaunit._label)
            x_agendaatom.set_required_arg("parent_road", insert_ideaunit._parent_road)
            x_agendaatom.set_optional_arg("_addin", insert_ideaunit._addin)
            x_agendaatom.set_optional_arg("_begin", insert_ideaunit._begin)
            x_agendaatom.set_optional_arg("_close", insert_ideaunit._close)
            x_agendaatom.set_optional_arg("_denom", insert_ideaunit._denom)
            x_agendaatom.set_optional_arg(
                "_meld_strategy", insert_ideaunit._meld_strategy
            )
            x_agendaatom.set_optional_arg(
                "_numeric_road", insert_ideaunit._numeric_road
            )
            x_agendaatom.set_optional_arg("_numor", insert_ideaunit._numor)
            x_agendaatom.set_optional_arg(
                "_range_source_road", insert_ideaunit._range_source_road
            )
            x_agendaatom.set_optional_arg("_reest", insert_ideaunit._reest)
            x_agendaatom.set_optional_arg("_weight", insert_ideaunit._weight)
            x_agendaatom.set_optional_arg("promise", insert_ideaunit.promise)
            self.set_agendaatom(x_agendaatom)

            self.add_agendaatom_idea_beliefunit_inserts(
                ideaunit=insert_ideaunit,
                insert_beliefunit_bases=set(insert_ideaunit._beliefunits.keys()),
            )
            self.add_agendaatom_idea_balancelink_inserts(
                after_ideaunit=insert_ideaunit,
                insert_balancelink_group_ids=set(insert_ideaunit._balancelinks.keys()),
            )
            self.add_agendaatom_idea_reasonunit_inserts(
                after_ideaunit=insert_ideaunit,
                insert_reasonunit_bases=set(insert_ideaunit._reasonunits.keys()),
            )
            self.add_agendaatom_idea_suffgroup_insert(
                idea_road=insert_idea_road,
                insert_suffgroup_group_ids=insert_ideaunit._assignedunit._suffgroups.keys(),
            )

    def add_agendaatom_idea_updates(
        self, before_agenda: AgendaUnit, after_agenda: AgendaUnit, update_roads: set
    ):
        for idea_road in update_roads:
            after_ideaunit = after_agenda.get_idea_obj(idea_road)
            before_ideaunit = before_agenda.get_idea_obj(idea_road)
            if optional_args_different(
                "agenda_ideaunit", before_ideaunit, after_ideaunit
            ):
                x_agendaatom = agendaatom_shop("agenda_ideaunit", atom_update())
                x_agendaatom.set_locator("road", after_ideaunit.get_road())
                x_agendaatom.set_required_arg("road", after_ideaunit.get_road())
                if before_ideaunit._addin != after_ideaunit._addin:
                    x_agendaatom.set_optional_arg("_addin", after_ideaunit._addin)
                if before_ideaunit._begin != after_ideaunit._begin:
                    x_agendaatom.set_optional_arg("_begin", after_ideaunit._begin)
                if before_ideaunit._close != after_ideaunit._close:
                    x_agendaatom.set_optional_arg("_close", after_ideaunit._close)
                if before_ideaunit._denom != after_ideaunit._denom:
                    x_agendaatom.set_optional_arg("_denom", after_ideaunit._denom)
                if before_ideaunit._meld_strategy != after_ideaunit._meld_strategy:
                    x_agendaatom.set_optional_arg(
                        "_meld_strategy", after_ideaunit._meld_strategy
                    )
                if before_ideaunit._numeric_road != after_ideaunit._numeric_road:
                    x_agendaatom.set_optional_arg(
                        "_numeric_road", after_ideaunit._numeric_road
                    )
                if before_ideaunit._numor != after_ideaunit._numor:
                    x_agendaatom.set_optional_arg("_numor", after_ideaunit._numor)
                if (
                    before_ideaunit._range_source_road
                    != after_ideaunit._range_source_road
                ):
                    x_agendaatom.set_optional_arg(
                        "_range_source_road", after_ideaunit._range_source_road
                    )
                if before_ideaunit._reest != after_ideaunit._reest:
                    x_agendaatom.set_optional_arg("_reest", after_ideaunit._reest)
                if before_ideaunit._weight != after_ideaunit._weight:
                    x_agendaatom.set_optional_arg("_weight", after_ideaunit._weight)
                if before_ideaunit.promise != after_ideaunit.promise:
                    x_agendaatom.set_optional_arg("promise", after_ideaunit.promise)
                self.set_agendaatom(x_agendaatom)

            # insert / update / delete beliefunits
            before_beliefunit_bases = set(before_ideaunit._beliefunits.keys())
            after_beliefunit_bases = set(after_ideaunit._beliefunits.keys())
            self.add_agendaatom_idea_beliefunit_inserts(
                ideaunit=after_ideaunit,
                insert_beliefunit_bases=after_beliefunit_bases.difference(
                    before_beliefunit_bases
                ),
            )
            self.add_agendaatom_idea_beliefunit_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_beliefunit_bases=before_beliefunit_bases.intersection(
                    after_beliefunit_bases
                ),
            )
            self.add_agendaatom_idea_beliefunit_deletes(
                idea_road=idea_road,
                delete_beliefunit_bases=before_beliefunit_bases.difference(
                    after_beliefunit_bases
                ),
            )

            # insert / update / delete balanceunits
            before_balancelinks_group_ids = set(before_ideaunit._balancelinks.keys())
            after_balancelinks_group_ids = set(after_ideaunit._balancelinks.keys())
            self.add_agendaatom_idea_balancelink_inserts(
                after_ideaunit=after_ideaunit,
                insert_balancelink_group_ids=after_balancelinks_group_ids.difference(
                    before_balancelinks_group_ids
                ),
            )
            self.add_agendaatom_idea_balancelink_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_balancelink_group_ids=before_balancelinks_group_ids.intersection(
                    after_balancelinks_group_ids
                ),
            )
            self.add_agendaatom_idea_balancelink_deletes(
                idea_road=idea_road,
                delete_balancelink_group_ids=before_balancelinks_group_ids.difference(
                    after_balancelinks_group_ids
                ),
            )

            # insert / update / delete reasonunits
            before_reasonunit_bases = set(before_ideaunit._reasonunits.keys())
            after_reasonunit_bases = set(after_ideaunit._reasonunits.keys())
            self.add_agendaatom_idea_reasonunit_inserts(
                after_ideaunit=after_ideaunit,
                insert_reasonunit_bases=after_reasonunit_bases.difference(
                    before_reasonunit_bases
                ),
            )
            self.add_agendaatom_idea_reasonunit_updates(
                before_ideaunit=before_ideaunit,
                after_ideaunit=after_ideaunit,
                update_reasonunit_bases=before_reasonunit_bases.intersection(
                    after_reasonunit_bases
                ),
            )
            self.add_agendaatom_idea_reasonunit_deletes(
                before_ideaunit=before_ideaunit,
                delete_reasonunit_bases=before_reasonunit_bases.difference(
                    after_reasonunit_bases
                ),
            )
            # insert / update / delete reasonunits_permises
            # update reasonunits_permises insert_premise
            # update reasonunits_permises update_premise
            # update reasonunits_permises delete_premise

            # insert / update / delete suffgroups
            before_suffgroups_group_ids = set(
                before_ideaunit._assignedunit._suffgroups.keys()
            )
            after_suffgroups_group_ids = set(
                after_ideaunit._assignedunit._suffgroups.keys()
            )
            self.add_agendaatom_idea_suffgroup_insert(
                idea_road=idea_road,
                insert_suffgroup_group_ids=after_suffgroups_group_ids.difference(
                    before_suffgroups_group_ids
                ),
            )
            self.add_agendaatom_idea_suffgroup_deletes(
                idea_road=idea_road,
                delete_suffgroup_group_ids=before_suffgroups_group_ids.difference(
                    after_suffgroups_group_ids
                ),
            )

    def add_agendaatom_idea_deletes(
        self, before_agenda: AgendaUnit, delete_idea_roads: set
    ):
        for delete_idea_road in delete_idea_roads:
            x_agendaatom = agendaatom_shop("agenda_ideaunit", atom_delete())
            x_agendaatom.set_locator("road", delete_idea_road)
            x_agendaatom.set_required_arg("road", delete_idea_road)
            self.set_agendaatom(x_agendaatom)

            delete_ideaunit = before_agenda.get_idea_obj(delete_idea_road)
            self.add_agendaatom_idea_beliefunit_deletes(
                idea_road=delete_idea_road,
                delete_beliefunit_bases=set(delete_ideaunit._beliefunits.keys()),
            )
            self.add_agendaatom_idea_balancelink_deletes(
                idea_road=delete_idea_road,
                delete_balancelink_group_ids=set(delete_ideaunit._balancelinks.keys()),
            )
            self.add_agendaatom_idea_reasonunit_deletes(
                before_ideaunit=delete_ideaunit,
                delete_reasonunit_bases=set(delete_ideaunit._reasonunits.keys()),
            )
            self.add_agendaatom_idea_suffgroup_deletes(
                idea_road=delete_idea_road,
                delete_suffgroup_group_ids=set(
                    delete_ideaunit._assignedunit._suffgroups.keys()
                ),
            )

    def add_agendaatom_idea_reasonunit_inserts(
        self, after_ideaunit: IdeaUnit, insert_reasonunit_bases: set
    ):
        for insert_reasonunit_base in insert_reasonunit_bases:
            after_reasonunit = after_ideaunit.get_reasonunit(insert_reasonunit_base)
            x_agendaatom = agendaatom_shop("agenda_idea_reasonunit", atom_insert())
            x_agendaatom.set_locator("road", after_ideaunit.get_road())
            x_agendaatom.set_locator("base", after_reasonunit.base)
            x_agendaatom.set_required_arg("road", after_ideaunit.get_road())
            x_agendaatom.set_required_arg("base", after_reasonunit.base)
            if after_reasonunit.suff_idea_active != None:
                x_agendaatom.set_optional_arg(
                    "suff_idea_active", after_reasonunit.suff_idea_active
                )
            self.set_agendaatom(x_agendaatom)

            self.add_agendaatom_idea_reason_premiseunit_inserts(
                idea_road=after_ideaunit.get_road(),
                after_reasonunit=after_reasonunit,
                insert_premise_needs=set(after_reasonunit.premises.keys()),
            )

    def add_agendaatom_idea_reasonunit_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_reasonunit_bases: set,
    ):
        for update_reasonunit_base in update_reasonunit_bases:
            before_reasonunit = before_ideaunit.get_reasonunit(update_reasonunit_base)
            after_reasonunit = after_ideaunit.get_reasonunit(update_reasonunit_base)
            if optional_args_different(
                "agenda_idea_reasonunit", before_reasonunit, after_reasonunit
            ):
                x_agendaatom = agendaatom_shop("agenda_idea_reasonunit", atom_update())
                x_agendaatom.set_locator("road", before_ideaunit.get_road())
                x_agendaatom.set_locator("base", after_reasonunit.base)
                x_agendaatom.set_required_arg("road", before_ideaunit.get_road())
                x_agendaatom.set_required_arg("base", after_reasonunit.base)
                if (
                    before_reasonunit.suff_idea_active
                    != after_reasonunit.suff_idea_active
                ):
                    x_agendaatom.set_optional_arg(
                        "suff_idea_active", after_reasonunit.suff_idea_active
                    )
                self.set_agendaatom(x_agendaatom)

            before_premise_needs = set(before_reasonunit.premises.keys())
            after_premise_needs = set(after_reasonunit.premises.keys())
            self.add_agendaatom_idea_reason_premiseunit_inserts(
                idea_road=before_ideaunit.get_road(),
                after_reasonunit=after_reasonunit,
                insert_premise_needs=after_premise_needs.difference(
                    before_premise_needs
                ),
            )
            self.add_agendaatom_idea_reason_premiseunit_updates(
                idea_road=before_ideaunit.get_road(),
                before_reasonunit=before_reasonunit,
                after_reasonunit=after_reasonunit,
                update_premise_needs=after_premise_needs.intersection(
                    before_premise_needs
                ),
            )
            self.add_agendaatom_idea_reason_premiseunit_deletes(
                idea_road=before_ideaunit.get_road(),
                reasonunit_base=update_reasonunit_base,
                delete_premise_needs=before_premise_needs.difference(
                    after_premise_needs
                ),
            )

    def add_agendaatom_idea_reasonunit_deletes(
        self, before_ideaunit: IdeaUnit, delete_reasonunit_bases: set
    ):
        for delete_reasonunit_base in delete_reasonunit_bases:
            x_agendaatom = agendaatom_shop("agenda_idea_reasonunit", atom_delete())
            x_agendaatom.set_locator("road", before_ideaunit.get_road())
            x_agendaatom.set_locator("base", delete_reasonunit_base)
            x_agendaatom.set_required_arg("road", before_ideaunit.get_road())
            x_agendaatom.set_required_arg("base", delete_reasonunit_base)
            self.set_agendaatom(x_agendaatom)

            before_reasonunit = before_ideaunit.get_reasonunit(delete_reasonunit_base)
            self.add_agendaatom_idea_reason_premiseunit_deletes(
                idea_road=before_ideaunit.get_road(),
                reasonunit_base=delete_reasonunit_base,
                delete_premise_needs=set(before_reasonunit.premises.keys()),
            )

    def add_agendaatom_idea_reason_premiseunit_inserts(
        self,
        idea_road: RoadUnit,
        after_reasonunit: ReasonUnit,
        insert_premise_needs: set,
    ):
        for insert_premise_need in insert_premise_needs:
            after_premiseunit = after_reasonunit.get_premise(insert_premise_need)
            x_agendaatom = agendaatom_shop(
                "agenda_idea_reason_premiseunit", atom_insert()
            )
            x_agendaatom.set_locator("road", idea_road)
            x_agendaatom.set_locator("base", after_reasonunit.base)
            x_agendaatom.set_locator("need", after_premiseunit.need)
            x_agendaatom.set_required_arg("road", idea_road)
            x_agendaatom.set_required_arg("base", after_reasonunit.base)
            x_agendaatom.set_required_arg("need", after_premiseunit.need)
            if after_premiseunit.open != None:
                x_agendaatom.set_optional_arg("open", after_premiseunit.open)
            if after_premiseunit.nigh != None:
                x_agendaatom.set_optional_arg("nigh", after_premiseunit.nigh)
            if after_premiseunit.divisor != None:
                x_agendaatom.set_optional_arg("divisor", after_premiseunit.divisor)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_reason_premiseunit_updates(
        self,
        idea_road: RoadUnit,
        before_reasonunit: ReasonUnit,
        after_reasonunit: ReasonUnit,
        update_premise_needs: set,
    ):
        for update_premise_need in update_premise_needs:
            before_premiseunit = before_reasonunit.get_premise(update_premise_need)
            after_premiseunit = after_reasonunit.get_premise(update_premise_need)
            if optional_args_different(
                "agenda_idea_reason_premiseunit", before_premiseunit, after_premiseunit
            ):
                x_agendaatom = agendaatom_shop(
                    "agenda_idea_reason_premiseunit", atom_update()
                )
                x_agendaatom.set_locator("road", idea_road)
                x_agendaatom.set_locator("base", before_reasonunit.base)
                x_agendaatom.set_locator("need", after_premiseunit.need)
                x_agendaatom.set_required_arg("road", idea_road)
                x_agendaatom.set_required_arg("base", before_reasonunit.base)
                x_agendaatom.set_required_arg("need", after_premiseunit.need)
                if after_premiseunit.open != before_premiseunit.open:
                    x_agendaatom.set_optional_arg("open", after_premiseunit.open)
                if after_premiseunit.nigh != before_premiseunit.nigh:
                    x_agendaatom.set_optional_arg("nigh", after_premiseunit.nigh)
                if after_premiseunit.divisor != before_premiseunit.divisor:
                    x_agendaatom.set_optional_arg("divisor", after_premiseunit.divisor)
                self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_reason_premiseunit_deletes(
        self,
        idea_road: RoadUnit,
        reasonunit_base: RoadUnit,
        delete_premise_needs: set,
    ):
        for delete_premise_need in delete_premise_needs:
            x_agendaatom = agendaatom_shop(
                "agenda_idea_reason_premiseunit", atom_delete()
            )
            x_agendaatom.set_locator("road", idea_road)
            x_agendaatom.set_locator("base", reasonunit_base)
            x_agendaatom.set_locator("need", delete_premise_need)
            x_agendaatom.set_required_arg("road", idea_road)
            x_agendaatom.set_required_arg("base", reasonunit_base)
            x_agendaatom.set_required_arg("need", delete_premise_needs)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_suffgroup_insert(
        self, idea_road: RoadUnit, insert_suffgroup_group_ids: set
    ):
        for insert_suffgroup_group_id in insert_suffgroup_group_ids:
            x_agendaatom = agendaatom_shop("agenda_idea_suffgroup", atom_insert())
            x_agendaatom.set_locator("road", idea_road)
            x_agendaatom.set_locator("group_id", insert_suffgroup_group_id)
            x_agendaatom.set_required_arg("road", idea_road)
            x_agendaatom.set_required_arg("group_id", insert_suffgroup_group_id)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_suffgroup_deletes(
        self, idea_road: RoadUnit, delete_suffgroup_group_ids: set
    ):
        for delete_suffgroup_group_id in delete_suffgroup_group_ids:
            x_agendaatom = agendaatom_shop("agenda_idea_suffgroup", atom_delete())
            x_agendaatom.set_locator("road", idea_road)
            x_agendaatom.set_locator("group_id", delete_suffgroup_group_id)
            x_agendaatom.set_required_arg("road", idea_road)
            x_agendaatom.set_required_arg("group_id", delete_suffgroup_group_id)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_balancelink_inserts(
        self, after_ideaunit: IdeaUnit, insert_balancelink_group_ids: set
    ):
        for after_balancelink_group_id in insert_balancelink_group_ids:
            after_balancelink = after_ideaunit._balancelinks.get(
                after_balancelink_group_id
            )
            x_agendaatom = agendaatom_shop("agenda_idea_balancelink", atom_insert())
            x_agendaatom.set_locator("road", after_ideaunit.get_road())
            x_agendaatom.set_locator("group_id", after_balancelink.group_id)
            x_agendaatom.set_required_arg("road", after_ideaunit.get_road())
            x_agendaatom.set_required_arg("group_id", after_balancelink.group_id)
            x_agendaatom.set_optional_arg(
                "creditor_weight", after_balancelink.creditor_weight
            )
            x_agendaatom.set_optional_arg(
                "debtor_weight", after_balancelink.debtor_weight
            )
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_balancelink_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_balancelink_group_ids: set,
    ):
        for update_balancelink_group_id in update_balancelink_group_ids:
            before_balancelink = before_ideaunit._balancelinks.get(
                update_balancelink_group_id
            )
            after_balancelink = after_ideaunit._balancelinks.get(
                update_balancelink_group_id
            )
            if optional_args_different(
                "agenda_idea_balancelink", before_balancelink, after_balancelink
            ):
                x_agendaatom = agendaatom_shop("agenda_idea_balancelink", atom_update())
                x_agendaatom.set_locator("road", before_ideaunit.get_road())
                x_agendaatom.set_locator("group_id", after_balancelink.group_id)
                x_agendaatom.set_required_arg("road", before_ideaunit.get_road())
                x_agendaatom.set_required_arg("group_id", after_balancelink.group_id)
                if (
                    before_balancelink.creditor_weight
                    != after_balancelink.creditor_weight
                ):
                    x_agendaatom.set_optional_arg(
                        "creditor_weight", after_balancelink.creditor_weight
                    )
                if before_balancelink.debtor_weight != after_balancelink.debtor_weight:
                    x_agendaatom.set_optional_arg(
                        "debtor_weight", after_balancelink.debtor_weight
                    )
                self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_balancelink_deletes(
        self, idea_road: RoadUnit, delete_balancelink_group_ids: set
    ):
        for delete_balancelink_group_id in delete_balancelink_group_ids:
            x_agendaatom = agendaatom_shop("agenda_idea_balancelink", atom_delete())
            x_agendaatom.set_locator("road", idea_road)
            x_agendaatom.set_locator("group_id", delete_balancelink_group_id)
            x_agendaatom.set_required_arg("road", idea_road)
            x_agendaatom.set_required_arg("group_id", delete_balancelink_group_id)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_beliefunit_inserts(
        self, ideaunit: IdeaUnit, insert_beliefunit_bases: set
    ):
        for insert_beliefunit_base in insert_beliefunit_bases:
            insert_beliefunit = ideaunit._beliefunits.get(insert_beliefunit_base)
            x_agendaatom = agendaatom_shop("agenda_idea_beliefunit", atom_insert())
            x_agendaatom.set_locator("road", ideaunit.get_road())
            x_agendaatom.set_locator("base", insert_beliefunit.base)
            x_agendaatom.set_required_arg("road", ideaunit.get_road())
            x_agendaatom.set_required_arg("base", insert_beliefunit.base)
            if insert_beliefunit.pick != None:
                x_agendaatom.set_optional_arg("pick", insert_beliefunit.pick)
            if insert_beliefunit.open != None:
                x_agendaatom.set_optional_arg("open", insert_beliefunit.open)
            if insert_beliefunit.nigh != None:
                x_agendaatom.set_optional_arg("nigh", insert_beliefunit.nigh)
            self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_beliefunit_updates(
        self,
        before_ideaunit: IdeaUnit,
        after_ideaunit: IdeaUnit,
        update_beliefunit_bases: set,
    ):
        for update_beliefunit_base in update_beliefunit_bases:
            before_beliefunit = before_ideaunit._beliefunits.get(update_beliefunit_base)
            after_beliefunit = after_ideaunit._beliefunits.get(update_beliefunit_base)
            if optional_args_different(
                "agenda_idea_beliefunit", before_beliefunit, after_beliefunit
            ):
                x_agendaatom = agendaatom_shop("agenda_idea_beliefunit", atom_update())
                x_agendaatom.set_locator("road", before_ideaunit.get_road())
                x_agendaatom.set_locator("base", after_beliefunit.base)
                x_agendaatom.set_required_arg("road", before_ideaunit.get_road())
                x_agendaatom.set_required_arg("base", after_beliefunit.base)
                if before_beliefunit.pick != after_beliefunit.pick:
                    x_agendaatom.set_optional_arg("pick", after_beliefunit.pick)
                if before_beliefunit.open != after_beliefunit.open:
                    x_agendaatom.set_optional_arg("open", after_beliefunit.open)
                if before_beliefunit.nigh != after_beliefunit.nigh:
                    x_agendaatom.set_optional_arg("nigh", after_beliefunit.nigh)
                self.set_agendaatom(x_agendaatom)

    def add_agendaatom_idea_beliefunit_deletes(
        self, idea_road: RoadUnit, delete_beliefunit_bases: BeliefUnit
    ):
        for delete_beliefunit_base in delete_beliefunit_bases:
            x_agendaatom = agendaatom_shop("agenda_idea_beliefunit", atom_delete())
            x_agendaatom.set_locator("road", idea_road)
            x_agendaatom.set_locator("base", delete_beliefunit_base)
            x_agendaatom.set_required_arg("road", idea_road)
            x_agendaatom.set_required_arg("base", delete_beliefunit_base)
            self.set_agendaatom(x_agendaatom)


def bookunit_shop(agendaatoms: dict[str:str] = None):
    return BookUnit(agendaatoms=get_empty_dict_if_none(agendaatoms))
