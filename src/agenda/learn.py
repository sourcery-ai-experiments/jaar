from src._prime.road import PersonRoad
from src.agenda.reason_idea import beliefunit_shop
from src.agenda.party import partyunit_shop, partylink_shop
from src.agenda.group import groupunit_shop, balancelink_shop
from src.agenda.idea import ideaunit_shop
from src.agenda.agenda import AgendaUnit
from src.agenda.examples.agenda_env import get_src_agenda_dir
from src.tools.python import (
    get_empty_dict_if_none,
    x_get_json,
    x_get_dict,
    place_obj_in_dict,
    get_nested_value,
    get_all_nondictionary_objs,
)
from src.tools.file import open_file, save_file
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


def grain_update() -> str:
    return "UPDATE"


def grain_insert() -> str:
    return "INSERT"


def grain_delete() -> str:
    return "DELETE"


def get_grain_config_file_name() -> str:
    return "learn_grain_config.json"


def get_grain_config_dict() -> dict:
    return x_get_dict(open_file(get_src_agenda_dir(), get_grain_config_file_name()))


def save_grain_config_file(grain_config_dict):
    save_file(
        dest_dir=get_src_agenda_dir(),
        file_name=get_grain_config_file_name(),
        file_text=x_get_json(grain_config_dict),
    )


def category_ref() -> set:
    return get_grain_config_dict().keys()


def is_category_ref(category_text: str) -> bool:
    return category_text in category_ref()


def get_mog(
    category: str,
    crud_text: str,
    grain_order_text: str,
    expected_grain_order: int = None,
) -> int:
    grain_config_dict = get_grain_config_dict()
    category_dict = grain_config_dict.get(category)
    crud_dict = category_dict.get(crud_text)
    return crud_dict.get(grain_order_text)


def set_mog(
    category: str,
    crud_text: str,
    grain_order_text: str,
    grain_order_int: int,
) -> int:
    grain_config_dict = get_grain_config_dict()
    category_dict = grain_config_dict.get(category)
    crud_dict = category_dict.get(crud_text)
    crud_dict[grain_order_text] = grain_order_int
    save_grain_config_file(grain_config_dict)


@dataclass
class GrainUnit:
    category: str = None
    crud_text: str = None
    locator: dict[str:str] = None
    required_args: dict[str:str] = None
    optional_args: dict[str:str] = None
    grain_order: int = None

    def set_grain_order(self):
        self.grain_order = get_mog(
            category=self.category,
            crud_text=self.crud_text,
            grain_order_text="grain_order",
        )

    def set_locator(self, x_key: str, x_value: any):
        self.locator[x_key] = x_value

    def get_locator(self, x_key: str) -> any:
        return self.locator.get(x_key)

    def is_locator_valid(self) -> bool:
        category_dict = get_grain_config_dict().get(self.category)
        locator_dict = get_empty_dict_if_none(category_dict.get("locator"))
        return locator_dict.keys() == self.locator.keys()

    def set_required_arg(self, x_key: str, x_value: any):
        self.required_args[x_key] = x_value

    def set_optional_arg(self, x_key: str, x_value: any):
        self.optional_args[x_key] = x_value

    def _get_category_dict(self):
        return get_grain_config_dict().get(self.category)

    def _get_required_args_dict(self) -> dict:
        crud_dict = self._get_category_dict().get(self.crud_text)
        return crud_dict.get("required_args")

    def _get_optional_args_dict(self) -> dict:
        crud_dict = self._get_category_dict().get(self.crud_text)
        return crud_dict.get("optional_args")

    def is_required_args_valid(self) -> bool:
        if self.crud_text not in {grain_delete(), grain_insert(), grain_update()}:
            return False
        required_args_dict = get_empty_dict_if_none(self._get_required_args_dict())
        return required_args_dict.keys() == self.required_args.keys()

    def is_optional_args_valid(self) -> bool:
        if self.crud_text not in {grain_delete(), grain_insert(), grain_update()}:
            return False

        optional_args_dict = get_empty_dict_if_none(self._get_optional_args_dict())
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


def grainunit_shop(
    category: str,
    crud_text: str = None,
    locator: dict[str:str] = None,
    required_args: dict[str:str] = None,
    optional_args: dict[str:str] = None,
) -> GrainUnit:
    if is_category_ref(category):
        return GrainUnit(
            category=category,
            crud_text=crud_text,
            locator=get_empty_dict_if_none(locator),
            required_args=get_empty_dict_if_none(required_args),
            optional_args=get_empty_dict_if_none(optional_args),
        )


def change_agenda_with_grainunit(x_agenda: AgendaUnit, x_grainunit: GrainUnit):
    # sourcery skip: extract-method
    xs = x_grainunit
    if xs.category == "_max_tree_traverse":
        x_agenda.set_max_tree_traverse(xs.get_value(xs.category))
    elif xs.category == "_party_creditor_pool":
        x_agenda.set_party_creditor_pool(xs.get_value(xs.category))
    elif xs.category == "_party_debtor_pool":
        x_agenda.set_party_debtor_pool(xs.get_value(xs.category))
    elif xs.category == "_meld_strategy":
        x_agenda.set_meld_strategy(xs.get_value(xs.category))
    elif xs.category == "AgendaUnit_weight":
        x_agenda._weight = xs.get_value(xs.category)
    elif xs.category == "groupunit" and xs.crud_text == grain_delete():
        group_id = xs.get_locator("group_id")
        x_agenda.del_groupunit(group_id)
    elif xs.category == "groupunit" and xs.crud_text == grain_update():
        x_groupunit = x_agenda.get_groupunit(xs.get_value("group_id"))
        x_groupunit._partylinks_set_by_economy_road = xs.get_value(
            "_partylinks_set_by_economy_road"
        )
    elif xs.category == "groupunit" and xs.crud_text == grain_insert():
        x_agenda.set_groupunit(
            groupunit_shop(
                group_id=xs.get_locator("group_id"),
                _partylinks_set_by_economy_road=xs.get_locator(
                    "_partylinks_set_by_economy_road"
                ),
            ),
            create_missing_partys=False,
            replace=False,
            add_partylinks=False,
        )
    elif xs.category == "groupunit_partylink" and xs.crud_text == grain_delete():
        x_agenda.get_groupunit(xs.get_locator("group_id")).del_partylink(
            xs.get_locator("party_id")
        )
    elif xs.category == "groupunit_partylink" and xs.crud_text == grain_update():
        x_groupunit = x_agenda.get_groupunit(xs.get_value("group_id"))
        x_groupunit.edit_partylink(
            party_id=xs.get_value("party_id"),
            creditor_weight=xs.get_value("creditor_weight"),
            debtor_weight=xs.get_value("debtor_weight"),
        )
    elif xs.category == "groupunit_partylink" and xs.crud_text == grain_insert():
        x_groupunit = x_agenda.get_groupunit(xs.get_locator("group_id"))
        x_groupunit.set_partylink(
            partylink_shop(
                party_id=xs.get_locator("party_id"),
                creditor_weight=xs.get_value("creditor_weight"),
                debtor_weight=xs.get_value("debtor_weight"),
            )
        )
    elif xs.category == "idea" and xs.crud_text == grain_delete():
        x_agenda.del_idea_kid(
            road=xs.get_locator("road"), del_children=xs.get_value("del_children")
        )
    elif xs.category == "idea" and xs.crud_text == grain_update():
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
    elif xs.category == "idea" and xs.crud_text == grain_insert():
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
    elif xs.category == "idea_balancelink" and xs.crud_text == grain_delete():
        x_agenda.edit_idea_attr(
            road=xs.get_locator("road"), balancelink_del=xs.get_value("group_id")
        )
    elif xs.category == "idea_balancelink" and xs.crud_text == grain_update():
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
    elif xs.category == "idea_balancelink" and xs.crud_text == grain_insert():
        x_balancelink = balancelink_shop(
            group_id=xs.get_value("group_id"),
            creditor_weight=xs.get_value("creditor_weight"),
            debtor_weight=xs.get_value("debtor_weight"),
        )
        x_agenda.edit_idea_attr(xs.get_value("road"), balancelink=x_balancelink)
    elif xs.category == "idea_beliefunit" and xs.crud_text == grain_delete():
        x_ideaunit = x_agenda.get_idea_obj(xs.get_value("road"))
        x_ideaunit.del_beliefunit(xs.get_value("base"))
    elif xs.category == "idea_beliefunit" and xs.crud_text == grain_update():
        x_ideaunit = x_agenda.get_idea_obj(xs.get_value("road"))
        x_beliefunit = x_ideaunit._beliefunits.get(xs.get_value("base"))
        x_beliefunit.set_attr(
            pick=xs.get_value("pick"),
            open=xs.get_value("open"),
            nigh=xs.get_value("nigh"),
        )
        # x_ideaunit.set_beliefunit(x_beliefunit)
    elif xs.category == "idea_beliefunit" and xs.crud_text == grain_insert():
        x_agenda.edit_idea_attr(
            road=xs.get_value("road"),
            beliefunit=beliefunit_shop(
                base=xs.get_value("base"),
                pick=xs.get_value("pick"),
                open=xs.get_value("open"),
                nigh=xs.get_value("nigh"),
            ),
        )
    elif xs.category == "idea_reasonunit" and xs.crud_text == grain_delete():
        x_ideaunit = x_agenda.get_idea_obj(xs.get_value("road"))
        x_ideaunit.del_reasonunit_base(xs.get_value("base"))
    elif xs.category == "idea_reasonunit" and xs.crud_text == grain_update():
        x_agenda.edit_idea_attr(
            road=xs.get_value("road"),
            reason_base=xs.get_value("base"),
            reason_suff_idea_active=xs.get_value("suff_idea_active"),
        )
    elif xs.category == "idea_reasonunit" and xs.crud_text == grain_insert():
        x_agenda.edit_idea_attr(
            road=xs.get_value("road"),
            reason_base=xs.get_value("base"),
            reason_suff_idea_active=xs.get_value("suff_idea_active"),
        )
    elif (
        xs.category == "idea_reasonunit_premiseunit" and xs.crud_text == grain_delete()
    ):
        x_agenda.edit_idea_attr(
            road=xs.get_value("road"),
            reason_del_premise_base=xs.get_value("base"),
            reason_del_premise_need=xs.get_value("need"),
        )
    elif (
        xs.category == "idea_reasonunit_premiseunit" and xs.crud_text == grain_update()
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
        xs.category == "idea_reasonunit_premiseunit" and xs.crud_text == grain_insert()
    ):
        x_ideaunit = x_agenda.get_idea_obj(xs.get_value("road"))
        x_ideaunit.set_reason_premise(
            base=xs.get_value("base"),
            premise=xs.get_value("need"),
            open=xs.get_value("open"),
            nigh=xs.get_value("nigh"),
            divisor=xs.get_value("divisor"),
        )
    elif xs.category == "idea_suffgroup" and xs.crud_text == grain_delete():
        x_ideaunit = x_agenda.get_idea_obj(xs.get_value("road"))
        x_ideaunit._assignedunit.del_suffgroup(group_id=xs.get_value("group_id"))
    elif xs.category == "idea_suffgroup" and xs.crud_text == grain_insert():
        x_ideaunit = x_agenda.get_idea_obj(xs.get_value("road"))
        x_ideaunit._assignedunit.set_suffgroup(group_id=xs.get_value("group_id"))
    elif xs.category == "partyunit" and xs.crud_text == grain_delete():
        x_agenda.del_partyunit(xs.get_locator("party_id"))
    elif xs.category == "partyunit" and xs.crud_text == grain_update():
        x_agenda.edit_partyunit(
            party_id=xs.get_value("party_id"),
            creditor_weight=xs.get_value("creditor_weight"),
            debtor_weight=xs.get_value("debtor_weight"),
            depotlink_type=xs.get_value("depotlink_type"),
        )
    elif xs.category == "partyunit" and xs.crud_text == grain_insert():
        x_agenda.set_partyunit(
            partyunit_shop(
                party_id=xs.get_value("party_id"),
                creditor_weight=xs.get_value("creditor_weight"),
                debtor_weight=xs.get_value("debtor_weight"),
                depotlink_type=xs.get_value("depotlink_type"),
            )
        )


@dataclass
class LearnUnit:
    agenda_road: PersonRoad = None
    grainunits: dict[str : dict[str:any]] = None

    def get_grain_order_grainunit_dict(self) -> dict[int:GrainUnit]:
        return get_all_nondictionary_objs(self.grainunits)

    def get_after_agenda(self, before_agenda: AgendaUnit):
        after_agenda = copy_deepcopy(before_agenda)
        grainunits_by_order = self.get_grain_order_grainunit_dict()

        for x_grain_order_int in sorted(grainunits_by_order.keys()):
            grainunits_list = grainunits_by_order.get(x_grain_order_int)
            for x_grainunit in grainunits_list:
                change_agenda_with_grainunit(after_agenda, x_grainunit)
        return after_agenda

    def set_grainunit(self, x_grainunit: GrainUnit):
        if x_grainunit.is_valid():
            x_grainunit.set_grain_order()
            x_keylist = [
                x_grainunit.crud_text,
                x_grainunit.category,
                *list(x_grainunit.locator.values()),
            ]
            place_obj_in_dict(self.grainunits, x_keylist, x_grainunit)

    def add_grainunit(
        self,
        category: str,
        crud_text: str,
        locator: str = None,
        required_args: str = None,
        optional_args: str = None,
    ):
        x_grainunit = grainunit_shop(
            category=category,
            crud_text=crud_text,
            locator=locator,
            required_args=required_args,
            optional_args=optional_args,
        )
        self.set_grainunit(x_grainunit)

    def get_grainunit(
        self, crud_text: str, category: str, locator_values: list[str]
    ) -> GrainUnit:
        x_keylist = [crud_text, category, *locator_values]
        return get_nested_value(self.grainunits, x_keylist)


def learnunit_shop(
    agenda_road: PersonRoad,
    grainunits: dict[str:str] = None,
):
    return LearnUnit(
        agenda_road=agenda_road, grainunits=get_empty_dict_if_none(grainunits)
    )
