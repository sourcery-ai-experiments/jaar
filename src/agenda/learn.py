from src._prime.road import PersonRoad, RoadUnit
from src.agenda.reason_idea import beliefunit_shop, BeliefUnit, PremiseUnit
from src.agenda.party import partyunit_shop, partylink_shop, PartyUnit, PartyLink
from src.agenda.group import (
    groupunit_shop,
    balancelink_shop,
    GroupUnit,
    GroupID,
    BalanceLink,
)
from src.agenda.idea import ideaunit_shop, IdeaUnit
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
        x_groupunit._treasury_partylinks = xs.get_value("_treasury_partylinks")
    elif xs.category == "groupunit" and xs.crud_text == grain_insert():
        x_agenda.set_groupunit(
            groupunit_shop(
                group_id=xs.get_locator("group_id"),
                _treasury_partylinks=xs.get_locator("_treasury_partylinks"),
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
        x_agenda.del_idea_obj(
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


class InvalidGrainUnitException(Exception):
    pass


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
        if x_grainunit.is_valid() == False:
            raise InvalidGrainUnitException(
                f"""'{x_grainunit.category}' {x_grainunit.crud_text} GrainUnit is invalid
{x_grainunit.is_locator_valid()=}
{x_grainunit.is_required_args_valid()=}
{x_grainunit.is_optional_args_valid()=}"""
            )

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


def create_learnunit(
    before_agenda: AgendaUnit, after_agenda: AgendaUnit, agenda_road: PersonRoad = None
) -> LearnUnit:
    before_agenda = copy_deepcopy(before_agenda)
    x_learnunit = learnunit_shop(agenda_road=agenda_road)

    # Given before_agenda, after_agenda
    # Go to every element of before_agenda, check if it exists in after_agenda
    # If the element is missing in after_agenda: create delete grainunit
    # If the element is changed in after_agenda: create update grainunit (optional args in config)
    # Go to every element in after_agenda, check if it exists in before_agenda
    # If the element does not exist, create insert grainunit

    # Use python's ability to compare custom class objects. Don't start at a smallest detail.
    # Given before_agenda, after_agenda

    before_agenda.set_agenda_metrics()
    after_agenda.set_agenda_metrics()

    add_grainunits_partyunit_insert(x_learnunit, before_agenda, after_agenda)
    add_grainunits_groupunit_insert(x_learnunit, before_agenda, after_agenda)
    add_grainunits_groupunit_partylink_insert(x_learnunit, before_agenda, after_agenda)
    add_grainunits_partyunit_delete(x_learnunit, before_agenda, after_agenda)
    add_grainunits_partyunit_update(x_learnunit, before_agenda, after_agenda)
    add_grainunits_AgendaUnit_simple_update(x_learnunit, before_agenda, after_agenda)
    add_grainunits_groupunit_partylink_delete(x_learnunit, before_agenda, after_agenda)
    add_grainunits_groupunit_partylink_update(x_learnunit, before_agenda, after_agenda)
    add_grainunits_groupunit_delete(x_learnunit, before_agenda, after_agenda)
    add_grainunits_groupunit_update(x_learnunit, before_agenda, after_agenda)
    add_grainunits_idea_reasonunit_premiseunit_insert(
        x_learnunit, before_agenda, after_agenda
    )
    add_grainunits_idea_reasonunit_premiseunit_delete(
        x_learnunit, before_agenda, after_agenda
    )
    # add_grainunits_idea_reasonunit_premiseunit_update(x_learnunit, before_agenda, after_agenda)
    # add_grainunits_idea_reasonunit_insert(x_learnunit, before_agenda, after_agenda)
    # add_grainunits_idea_reasonunit_delete(x_learnunit, before_agenda, after_agenda)
    # add_grainunits_idea_reasonunit_update(x_learnunit, before_agenda, after_agenda)
    add_grainunits_idea_beliefunit_insert(x_learnunit, before_agenda, after_agenda)
    add_grainunits_idea_beliefunit_delete(x_learnunit, before_agenda, after_agenda)
    add_grainunits_idea_beliefunit_update(x_learnunit, before_agenda, after_agenda)
    # add_grainunits_idea_suffgroup_insert(x_learnunit, before_agenda, after_agenda)
    # add_grainunits_idea_suffgroup_delete(x_learnunit, before_agenda, after_agenda)
    add_grainunits_idea_balancelink_insert(x_learnunit, before_agenda, after_agenda)
    add_grainunits_idea_balancelink_delete(x_learnunit, before_agenda, after_agenda)
    add_grainunits_idea_balancelink_update(x_learnunit, before_agenda, after_agenda)
    add_grainunits_idea_insert(x_learnunit, before_agenda, after_agenda)
    add_grainunits_idea_delete(x_learnunit, before_agenda, after_agenda)
    add_grainunits_idea_update(x_learnunit, before_agenda, after_agenda)
    # add_grainunits_idea_update(x_learnunit, before_agenda, after_agenda)

    # create deepcopy of before_agenda, call it learning_agenda
    # if learning_agenda != after_agenda: check something if different find grainunits.
    #   Apply grainunits to learning_agenda
    # if learning_agenda != after_agenda again: check something else if different
    # all the way down the line for all 15 elements

    return x_learnunit


def add_grainunits_AgendaUnit_simple_update(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    if before_agenda._weight != after_agenda._weight:
        x_grainunit = grainunit_shop("AgendaUnit_weight", grain_update())
        x_grainunit.set_required_arg("AgendaUnit_weight", after_agenda._weight)
        x_learnunit.set_grainunit(x_grainunit)
    if before_agenda._max_tree_traverse != after_agenda._max_tree_traverse:
        x_grainunit = grainunit_shop("_max_tree_traverse", grain_update())
        x_grainunit.set_required_arg(
            "_max_tree_traverse", after_agenda._max_tree_traverse
        )
        x_learnunit.set_grainunit(x_grainunit)
    if before_agenda._party_creditor_pool != after_agenda._party_creditor_pool:
        x_grainunit = grainunit_shop("_party_creditor_pool", grain_update())
        x_grainunit.set_required_arg(
            "_party_creditor_pool", after_agenda._party_creditor_pool
        )
        x_learnunit.set_grainunit(x_grainunit)
    if before_agenda._party_debtor_pool != after_agenda._party_debtor_pool:
        x_grainunit = grainunit_shop("_party_debtor_pool", grain_update())
        x_grainunit.set_required_arg(
            "_party_debtor_pool", after_agenda._party_debtor_pool
        )
        x_learnunit.set_grainunit(x_grainunit)
    if before_agenda._auto_output_to_forum != after_agenda._auto_output_to_forum:
        x_grainunit = grainunit_shop("_auto_output_to_forum", grain_update())
        x_grainunit.set_required_arg(
            "_auto_output_to_forum", after_agenda._auto_output_to_forum
        )
        x_learnunit.set_grainunit(x_grainunit)
    if before_agenda._meld_strategy != after_agenda._meld_strategy:
        x_grainunit = grainunit_shop("_meld_strategy", grain_update())
        x_grainunit.set_required_arg("_meld_strategy", after_agenda._meld_strategy)
        x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_groupunit_partylink_update(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    if before_agenda.get_groupunits_dict() != after_agenda.get_groupunits_dict():
        for after_groupunit in after_agenda._groups.values():
            for after_partylink in after_groupunit._partys.values():
                before_group = before_agenda.get_groupunit(after_groupunit.group_id)
                if before_group != None:
                    before_partylink = before_group.get_partylink(
                        after_partylink.party_id
                    )
                    if before_partylink.get_dict() != after_partylink.get_dict():
                        add_grainunit_groupunit_partylink_update(
                            x_learnunit, before_group, before_partylink, after_partylink
                        )


def add_grainunit_groupunit_partylink_update(
    x_learnunit: LearnUnit,
    before_groupunit: GroupUnit,
    before_partylink: PartyLink,
    after_partylink: PartyLink,
):
    after_grainunit = grainunit_shop("groupunit_partylink", grain_update())
    after_grainunit.set_locator("group_id", before_groupunit.group_id)
    after_grainunit.set_locator("party_id", after_partylink.party_id)
    after_grainunit.set_required_arg("group_id", before_groupunit.group_id)
    after_grainunit.set_required_arg("party_id", after_partylink.party_id)
    if after_partylink.creditor_weight != before_partylink.creditor_weight:
        after_grainunit.set_optional_arg(
            "creditor_weight", after_partylink.creditor_weight
        )
    if after_partylink.debtor_weight != before_partylink.debtor_weight:
        after_grainunit.set_optional_arg("debtor_weight", after_partylink.debtor_weight)
    x_learnunit.set_grainunit(after_grainunit)


def add_grainunits_groupunit_partylink_delete(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    if before_agenda.get_groupunits_dict() != after_agenda.get_groupunits_dict():
        for before_groupunit in before_agenda._groups.values():
            for before_partylink in before_groupunit._partys.values():
                after_group = after_agenda.get_groupunit(before_groupunit.group_id)
                if (
                    after_group is None
                    or after_group.get_partylink(before_partylink.party_id) is None
                ):
                    add_grainunit_groupunit_partylink_delete(
                        x_learnunit, before_groupunit, before_partylink
                    )


def add_grainunit_groupunit_partylink_delete(
    x_learnunit: LearnUnit, before_groupunit: GroupUnit, before_partylink: PartyLink
):
    after_grainunit = grainunit_shop("groupunit_partylink", grain_delete())
    after_grainunit.set_locator("group_id", before_groupunit.group_id)
    after_grainunit.set_locator("party_id", before_partylink.party_id)
    after_grainunit.set_required_arg("group_id", before_groupunit.group_id)
    after_grainunit.set_required_arg("party_id", before_partylink.party_id)
    x_learnunit.set_grainunit(after_grainunit)


def add_grainunits_groupunit_partylink_insert(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    if before_agenda.get_groupunits_dict() != after_agenda.get_groupunits_dict():
        for after_groupunit in after_agenda._groups.values():
            for after_partylink in after_groupunit._partys.values():
                before_group = before_agenda.get_groupunit(after_groupunit.group_id)
                if (
                    before_group is None
                    or before_group.get_partylink(after_partylink.party_id) is None
                ) and after_groupunit._party_mirror == False:
                    add_grainunit_groupunit_partylink_insert(
                        x_learnunit, after_groupunit, after_partylink
                    )


def add_grainunit_groupunit_partylink_insert(
    x_learnunit: LearnUnit, after_groupunit: GroupUnit, after_partylink: PartyLink
):
    after_grainunit = grainunit_shop("groupunit_partylink", grain_insert())
    after_grainunit.set_locator("group_id", after_groupunit.group_id)
    after_grainunit.set_locator("party_id", after_partylink.party_id)
    after_grainunit.set_required_arg("group_id", after_groupunit.group_id)
    after_grainunit.set_required_arg("party_id", after_partylink.party_id)
    if after_partylink.creditor_weight != None:
        after_grainunit.set_optional_arg(
            "creditor_weight", after_partylink.creditor_weight
        )
    if after_partylink.debtor_weight != None:
        after_grainunit.set_optional_arg("debtor_weight", after_partylink.debtor_weight)
    x_learnunit.set_grainunit(after_grainunit)


def add_grainunits_groupunit_insert(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    if before_agenda.get_groupunits_dict() != after_agenda.get_groupunits_dict():
        for after_groupunit in after_agenda._groups.values():
            if (
                before_agenda.get_groupunit(after_groupunit.group_id) is None
                and after_groupunit._party_mirror == False
            ):
                add_grainunit_groupunit_insert(x_learnunit, after_groupunit)


def add_grainunit_groupunit_insert(x_learnunit: LearnUnit, after_groupunit: GroupUnit):
    after_grainunit = grainunit_shop("groupunit", grain_insert())
    after_grainunit.set_locator("group_id", after_groupunit.group_id)
    after_grainunit.set_required_arg("group_id", after_groupunit.group_id)
    if after_groupunit._treasury_partylinks != None:
        after_grainunit.set_optional_arg(
            "_treasury_partylinks",
            after_groupunit._treasury_partylinks,
        )
    x_learnunit.set_grainunit(after_grainunit)


def add_grainunits_groupunit_update(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    if before_agenda.get_groupunits_dict() != after_agenda.get_groupunits_dict():
        for after_groupunit in after_agenda._groups.values():
            before_groupunit = before_agenda.get_groupunit(after_groupunit.group_id)
            if (
                before_groupunit != None
                and before_groupunit._treasury_partylinks
                != after_groupunit._treasury_partylinks
            ):
                add_grainunit_groupunit_update(
                    x_learnunit, before_groupunit, after_groupunit
                )


def add_grainunit_groupunit_update(
    x_learnunit: LearnUnit, before_groupunit: GroupUnit, after_groupunit: GroupUnit
):
    after_grainunit = grainunit_shop("groupunit", grain_update())
    after_grainunit.set_locator("group_id", after_groupunit.group_id)
    after_grainunit.set_required_arg("group_id", after_groupunit.group_id)
    if after_groupunit._treasury_partylinks != before_groupunit._treasury_partylinks:
        after_grainunit.set_optional_arg(
            "_treasury_partylinks",
            after_groupunit._treasury_partylinks,
        )
    x_learnunit.set_grainunit(after_grainunit)


def add_grainunits_groupunit_delete(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    if before_agenda._groups != after_agenda._groups:
        for before_groupunit in before_agenda._groups.values():
            if (
                after_agenda.get_groupunit(before_groupunit.group_id) is None
                and before_groupunit._party_mirror == False
            ):
                add_grainunit_groupunit_delete(x_learnunit, before_groupunit)


def add_grainunit_groupunit_delete(x_learnunit: LearnUnit, before_groupunit: GroupUnit):
    after_grainunit = grainunit_shop("groupunit", grain_delete())
    after_grainunit.set_locator("group_id", before_groupunit.group_id)
    after_grainunit.set_required_arg("group_id", before_groupunit.group_id)
    x_learnunit.set_grainunit(after_grainunit)


def add_grainunits_idea_reasonunit_premiseunit_insert(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    for after_ideaunit in after_agenda._idea_dict.values():
        if before_agenda.idea_exists(after_ideaunit.get_road()):
            before_ideaunit = before_agenda.get_idea_obj(after_ideaunit.get_road())
            for after_reasonunit in after_ideaunit._reasonunits.values():
                before_reasonunit = before_ideaunit.get_reasonunit(
                    after_reasonunit.base
                )
                if before_reasonunit != None:
                    for after_premiseunit in after_reasonunit.premises.values():
                        before_premiseunit = before_reasonunit.get_premise(
                            after_premiseunit.need
                        )
                        if before_premiseunit is None:
                            add_grainunit_idea_reasonunit_premiseunit_insert(
                                x_learnunit,
                                after_ideaunit.get_road(),
                                after_reasonunit.base,
                                after_premiseunit,
                            )


def add_grainunit_idea_reasonunit_premiseunit_insert(
    x_learnunit: LearnUnit,
    idea_road: RoadUnit,
    reason_base: RoadUnit,
    after_premiseunit: PremiseUnit,
):
    x_grainunit = grainunit_shop("idea_reasonunit_premiseunit", grain_insert())
    x_grainunit.set_locator("road", idea_road)
    x_grainunit.set_locator("base", reason_base)
    x_grainunit.set_locator("need", after_premiseunit.need)
    x_grainunit.set_required_arg("road", idea_road)
    x_grainunit.set_required_arg("base", reason_base)
    x_grainunit.set_required_arg("need", after_premiseunit.need)
    if after_premiseunit.open != None:
        x_grainunit.set_optional_arg("open", after_premiseunit.open)
    if after_premiseunit.nigh != None:
        x_grainunit.set_optional_arg("nigh", after_premiseunit.nigh)
    if after_premiseunit.divisor != None:
        x_grainunit.set_optional_arg("divisor", after_premiseunit.divisor)
    x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_idea_reasonunit_premiseunit_delete(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    for before_ideaunit in before_agenda._idea_dict.values():
        if after_agenda.idea_exists(before_ideaunit.get_road()):
            after_ideaunit = after_agenda.get_idea_obj(before_ideaunit.get_road())
            for before_reasonunit in before_ideaunit._reasonunits.values():
                after_reasonunit = after_ideaunit.get_reasonunit(before_reasonunit.base)
                if after_reasonunit != None:
                    for before_premiseunit in before_reasonunit.premises.values():
                        after_premiseunit = after_reasonunit.get_premise(
                            before_premiseunit.need
                        )
                        if after_premiseunit is None:
                            add_grainunit_idea_reasonunit_premiseunit_delete(
                                x_learnunit,
                                before_ideaunit.get_road(),
                                before_reasonunit.base,
                                before_premiseunit,
                            )


def add_grainunit_idea_reasonunit_premiseunit_delete(
    x_learnunit: LearnUnit,
    idea_road: RoadUnit,
    reason_base: RoadUnit,
    before_premiseunit: PremiseUnit,
):
    x_grainunit = grainunit_shop("idea_reasonunit_premiseunit", grain_delete())
    x_grainunit.set_locator("road", idea_road)
    x_grainunit.set_locator("base", reason_base)
    x_grainunit.set_locator("need", before_premiseunit.need)
    x_grainunit.set_required_arg("road", idea_road)
    x_grainunit.set_required_arg("base", reason_base)
    x_grainunit.set_required_arg("need", before_premiseunit.need)
    x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_idea_reasonunit(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    pass


def add_grainunits_idea_suffgroup(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    pass


def add_grainunits_idea_balancelink_insert(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    after_idea_list = list(after_agenda._idea_dict.values())
    for after_ideaunit in after_idea_list:
        if before_agenda.idea_exists(after_ideaunit.get_road()):
            before_ideaunit = before_agenda.get_idea_obj(after_ideaunit.get_road())
            if (
                before_ideaunit is None
                or before_ideaunit.get_balancelinks_dict()
                != after_ideaunit.get_balancelinks_dict()
            ):
                for after_balancelink in after_ideaunit._balancelinks.values():
                    if (
                        before_ideaunit._balancelinks.get(after_balancelink.group_id)
                        is None
                    ):
                        add_grainunit_idea_balancelink_insert(
                            x_learnunit, after_ideaunit.get_road(), after_balancelink
                        )


def add_grainunit_idea_balancelink_insert(
    x_learnunit: LearnUnit, idea_road: RoadUnit, after_balancelink: BalanceLink
):
    x_grainunit = grainunit_shop("idea_balancelink", grain_insert())
    x_grainunit.set_locator("road", idea_road)
    x_grainunit.set_locator("group_id", after_balancelink.group_id)
    x_grainunit.set_required_arg("road", idea_road)
    x_grainunit.set_required_arg("group_id", after_balancelink.group_id)
    x_grainunit.set_optional_arg("creditor_weight", after_balancelink.creditor_weight)
    x_grainunit.set_optional_arg("debtor_weight", after_balancelink.debtor_weight)
    x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_idea_balancelink_delete(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    before_idea_list = list(before_agenda._idea_dict.values())
    for before_ideaunit in before_idea_list:
        if after_agenda.idea_exists(before_ideaunit.get_road()):
            after_ideaunit = after_agenda.get_idea_obj(before_ideaunit.get_road())
            if (
                after_ideaunit != None
                and after_ideaunit.get_balancelinks_dict()
                != before_ideaunit.get_balancelinks_dict()
            ):
                for before_group_id in before_ideaunit._balancelinks.keys():
                    if after_ideaunit._balancelinks.get(before_group_id) is None:
                        add_grainunit_idea_balancelink_delete(
                            x_learnunit, before_ideaunit.get_road(), before_group_id
                        )


def add_grainunit_idea_balancelink_delete(
    x_learnunit: LearnUnit, before_idea_road: RoadUnit, before_group_id: GroupID
):
    x_grainunit = grainunit_shop("idea_balancelink", grain_delete())
    x_grainunit.set_locator("road", before_idea_road)
    x_grainunit.set_locator("group_id", before_group_id)
    x_grainunit.set_required_arg("road", before_idea_road)
    x_grainunit.set_required_arg("group_id", before_group_id)
    x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_idea_balancelink_update(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    before_idea_list = list(before_agenda._idea_dict.values())
    for before_ideaunit in before_idea_list:
        if after_agenda.idea_exists(before_ideaunit.get_road()):
            after_ideaunit = after_agenda.get_idea_obj(before_ideaunit.get_road())
            if (
                after_ideaunit != None
                and after_ideaunit.get_balancelinks_dict()
                != before_ideaunit.get_balancelinks_dict()
            ):
                for before_group_id in before_ideaunit._balancelinks.keys():
                    after_balancelink = after_ideaunit._balancelinks.get(
                        before_group_id
                    )
                    before_balancelink = before_ideaunit._balancelinks.get(
                        before_group_id
                    )
                    if (
                        after_balancelink != None
                        and before_balancelink.get_dict()
                        != after_balancelink.get_dict()
                    ):
                        add_grainunit_idea_balancelink_update(
                            x_learnunit=x_learnunit,
                            idea_road=before_ideaunit.get_road(),
                            before_balancelink=before_balancelink,
                            after_balancelink=after_balancelink,
                        )


def add_grainunit_idea_balancelink_update(
    x_learnunit: LearnUnit,
    idea_road: RoadUnit,
    before_balancelink: BalanceLink,
    after_balancelink: BalanceLink,
):
    x_grainunit = grainunit_shop("idea_balancelink", grain_update())
    x_grainunit.set_locator("road", idea_road)
    x_grainunit.set_locator("group_id", after_balancelink.group_id)
    x_grainunit.set_required_arg("road", idea_road)
    x_grainunit.set_required_arg("group_id", after_balancelink.group_id)
    if before_balancelink.creditor_weight != after_balancelink.creditor_weight:
        x_grainunit.set_optional_arg(
            "creditor_weight", after_balancelink.creditor_weight
        )
    if before_balancelink.debtor_weight != after_balancelink.debtor_weight:
        x_grainunit.set_optional_arg("debtor_weight", after_balancelink.debtor_weight)
    x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_idea_beliefunit_update(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    before_idea_list = list(before_agenda._idea_dict.values())
    for before_ideaunit in before_idea_list:
        if after_agenda.idea_exists(before_ideaunit.get_road()):
            after_ideaunit = after_agenda.get_idea_obj(before_ideaunit.get_road())
            if (
                after_ideaunit != None
                and after_ideaunit.get_beliefunits_dict()
                != before_ideaunit.get_beliefunits_dict()
            ):
                for before_base in before_ideaunit._beliefunits.keys():
                    after_beliefunit = after_ideaunit._beliefunits.get(before_base)
                    before_beliefunit = before_ideaunit._beliefunits.get(before_base)
                    if (
                        after_beliefunit != None
                        and before_beliefunit.get_dict() != after_beliefunit.get_dict()
                    ):
                        add_grainunit_idea_beliefunit_update(
                            x_learnunit=x_learnunit,
                            idea_road=before_ideaunit.get_road(),
                            before_beliefunit=before_beliefunit,
                            after_beliefunit=after_beliefunit,
                        )


def add_grainunit_idea_beliefunit_update(
    x_learnunit: LearnUnit,
    idea_road: RoadUnit,
    before_beliefunit: BeliefUnit,
    after_beliefunit: BeliefUnit,
):
    x_grainunit = grainunit_shop("idea_beliefunit", grain_update())
    x_grainunit.set_locator("road", idea_road)
    x_grainunit.set_locator("base", after_beliefunit.base)
    x_grainunit.set_required_arg("road", idea_road)
    x_grainunit.set_required_arg("base", after_beliefunit.base)
    if before_beliefunit.pick != after_beliefunit.pick:
        x_grainunit.set_optional_arg("pick", after_beliefunit.pick)
    if before_beliefunit.open != after_beliefunit.open:
        x_grainunit.set_optional_arg("open", after_beliefunit.open)
    if before_beliefunit.nigh != after_beliefunit.nigh:
        x_grainunit.set_optional_arg("nigh", after_beliefunit.nigh)
    x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_idea_beliefunit_insert(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    after_idea_list = list(after_agenda._idea_dict.values())
    for after_ideaunit in after_idea_list:
        if before_agenda.idea_exists(after_ideaunit.get_road()):
            before_ideaunit = before_agenda.get_idea_obj(after_ideaunit.get_road())
            if (
                before_ideaunit != None
                and before_ideaunit.get_beliefunits_dict()
                != after_ideaunit.get_beliefunits_dict()
            ):
                for after_base in after_ideaunit._beliefunits.keys():
                    if before_ideaunit._beliefunits.get(after_base) is None:
                        add_grainunit_idea_beliefunit_insert(
                            x_learnunit=x_learnunit,
                            idea_road=after_ideaunit.get_road(),
                            after_beliefunit=after_ideaunit._beliefunits.get(
                                after_base
                            ),
                        )


def add_grainunit_idea_beliefunit_insert(
    x_learnunit: LearnUnit, idea_road: RoadUnit, after_beliefunit: BeliefUnit
):
    x_grainunit = grainunit_shop("idea_beliefunit", grain_insert())
    x_grainunit.set_locator("road", idea_road)
    x_grainunit.set_locator("base", after_beliefunit.base)
    x_grainunit.set_required_arg("road", idea_road)
    x_grainunit.set_required_arg("base", after_beliefunit.base)
    if after_beliefunit.pick != None:
        x_grainunit.set_optional_arg("pick", after_beliefunit.pick)
    if after_beliefunit.open != None:
        x_grainunit.set_optional_arg("open", after_beliefunit.open)
    if after_beliefunit.nigh != None:
        x_grainunit.set_optional_arg("nigh", after_beliefunit.nigh)
    x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_idea_beliefunit_delete(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    before_idea_list = list(before_agenda._idea_dict.values())
    for before_ideaunit in before_idea_list:
        if after_agenda.idea_exists(before_ideaunit.get_road()):
            after_ideaunit = after_agenda.get_idea_obj(before_ideaunit.get_road())
            if (
                after_ideaunit != None
                and after_ideaunit.get_beliefunits_dict()
                != before_ideaunit.get_beliefunits_dict()
            ):
                for before_base in before_ideaunit._beliefunits.keys():
                    if after_ideaunit._beliefunits.get(before_base) is None:
                        add_grainunit_idea_beliefunit_delete(
                            x_learnunit=x_learnunit,
                            idea_road=before_ideaunit.get_road(),
                            before_beliefunit=before_ideaunit._beliefunits.get(
                                before_base
                            ),
                        )


def add_grainunit_idea_beliefunit_delete(
    x_learnunit: LearnUnit, idea_road: RoadUnit, before_beliefunit: BeliefUnit
):
    x_grainunit = grainunit_shop("idea_beliefunit", grain_delete())
    x_grainunit.set_locator("road", idea_road)
    x_grainunit.set_locator("base", before_beliefunit.base)
    x_grainunit.set_required_arg("road", idea_road)
    x_grainunit.set_required_arg("base", before_beliefunit.base)
    x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_idea_update(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    after_idea_list = list(after_agenda._idea_dict.values())
    for after_ideaunit in after_idea_list:
        if before_agenda.idea_exists(after_ideaunit.get_road()):
            before_ideaunit = before_agenda.get_idea_obj(after_ideaunit.get_road())
            if before_ideaunit != None and (
                before_ideaunit._addin != after_ideaunit._addin
                or before_ideaunit._begin != after_ideaunit._begin
                or before_ideaunit._close != after_ideaunit._close
                or before_ideaunit._denom != after_ideaunit._denom
                or before_ideaunit._meld_strategy != after_ideaunit._meld_strategy
                or before_ideaunit._numeric_road != after_ideaunit._numeric_road
                or before_ideaunit._numor != after_ideaunit._numor
                or before_ideaunit._range_source_road
                != after_ideaunit._range_source_road
                or before_ideaunit._reest != after_ideaunit._reest
                or before_ideaunit._weight != after_ideaunit._weight
                or before_ideaunit.promise != after_ideaunit.promise
            ):
                add_grainunit_idea_update(x_learnunit, before_ideaunit, after_ideaunit)


def add_grainunit_idea_update(x_learnunit, before_ideaunit, after_ideaunit):
    x_grainunit = grainunit_shop("idea", grain_update())
    x_grainunit.set_locator("road", after_ideaunit.get_road())
    x_grainunit.set_required_arg("road", after_ideaunit.get_road())
    if before_ideaunit._addin != after_ideaunit._addin:
        x_grainunit.set_optional_arg("_addin", after_ideaunit._addin)
    if before_ideaunit._begin != after_ideaunit._begin:
        x_grainunit.set_optional_arg("_begin", after_ideaunit._begin)
    if before_ideaunit._close != after_ideaunit._close:
        x_grainunit.set_optional_arg("_close", after_ideaunit._close)
    if before_ideaunit._denom != after_ideaunit._denom:
        x_grainunit.set_optional_arg("_denom", after_ideaunit._denom)
    if before_ideaunit._meld_strategy != after_ideaunit._meld_strategy:
        x_grainunit.set_optional_arg("_meld_strategy", after_ideaunit._meld_strategy)
    if before_ideaunit._numeric_road != after_ideaunit._numeric_road:
        x_grainunit.set_optional_arg("_numeric_road", after_ideaunit._numeric_road)
    if before_ideaunit._numor != after_ideaunit._numor:
        x_grainunit.set_optional_arg("_numor", after_ideaunit._numor)
    if before_ideaunit._range_source_road != after_ideaunit._range_source_road:
        x_grainunit.set_optional_arg(
            "_range_source_road", after_ideaunit._range_source_road
        )
    if before_ideaunit._reest != after_ideaunit._reest:
        x_grainunit.set_optional_arg("_reest", after_ideaunit._reest)
    if before_ideaunit._weight != after_ideaunit._weight:
        x_grainunit.set_optional_arg("_weight", after_ideaunit._weight)
    if before_ideaunit.promise != after_ideaunit.promise:
        x_grainunit.set_optional_arg("promise", after_ideaunit.promise)
    x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_idea_insert(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    after_idea_list = list(after_agenda._idea_dict.keys())
    after_idea_list.sort(reverse=True)
    for x_idea_road in after_idea_list:
        if before_agenda.idea_exists(x_idea_road) == False:
            after_ideaunit = after_agenda.get_idea_obj(x_idea_road)
            add_grainunit_idea_insert(x_learnunit, after_ideaunit)


def add_grainunit_idea_insert(x_learnunit, after_ideaunit: IdeaUnit):
    x_grainunit = grainunit_shop("idea", grain_insert())
    x_grainunit.set_locator("road", after_ideaunit.get_road())
    x_grainunit.set_required_arg("label", after_ideaunit._label)
    x_grainunit.set_required_arg("parent_road", after_ideaunit._parent_road)
    x_grainunit.set_optional_arg("_addin", after_ideaunit._addin)
    x_grainunit.set_optional_arg("_begin", after_ideaunit._begin)
    x_grainunit.set_optional_arg("_close", after_ideaunit._close)
    x_grainunit.set_optional_arg("_denom", after_ideaunit._denom)
    x_grainunit.set_optional_arg("_meld_strategy", after_ideaunit._meld_strategy)
    x_grainunit.set_optional_arg("_numeric_road", after_ideaunit._numeric_road)
    x_grainunit.set_optional_arg("_numor", after_ideaunit._numor)
    x_grainunit.set_optional_arg(
        "_range_source_road", after_ideaunit._range_source_road
    )
    x_grainunit.set_optional_arg("_reest", after_ideaunit._reest)
    x_grainunit.set_optional_arg("_weight", after_ideaunit._weight)
    x_grainunit.set_optional_arg("promise", after_ideaunit.promise)
    x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_idea_delete(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    before_idea_list = list(before_agenda._idea_dict.keys())
    before_idea_list.sort(reverse=True)
    for x_idea_road in before_idea_list:
        if after_agenda.idea_exists(x_idea_road) == False:
            add_grainunit_idea_delete(x_learnunit, before_idea_road=x_idea_road)


def add_grainunit_idea_delete(x_learnunit, before_idea_road: RoadUnit):
    x_grainunit = grainunit_shop("idea", grain_delete())
    x_grainunit.set_locator("road", before_idea_road)
    x_grainunit.set_required_arg("road", before_idea_road)
    x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_partyunit_update(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    if before_agenda.get_partys_dict() != after_agenda.get_partys_dict():
        for after_partyunit in after_agenda._partys.values():
            before_partyunit = before_agenda.get_party(after_partyunit.party_id)
            if before_partyunit not in [None, after_partyunit]:
                add_grainunit_partyunit_update(
                    x_learnunit, before_partyunit, after_partyunit
                )


def add_grainunit_partyunit_update(
    x_learnunit: LearnUnit, before_partyunit: PartyUnit, after_partyunit: PartyUnit
):
    x_grainunit = grainunit_shop("partyunit", grain_update())
    x_grainunit.set_locator("party_id", after_partyunit.party_id)
    x_grainunit.set_required_arg("party_id", after_partyunit.party_id)
    if before_partyunit.creditor_weight != after_partyunit.creditor_weight:
        x_grainunit.set_optional_arg("creditor_weight", after_partyunit.creditor_weight)
    if before_partyunit.debtor_weight != after_partyunit.debtor_weight:
        x_grainunit.set_optional_arg("debtor_weight", after_partyunit.debtor_weight)
    if before_partyunit.depotlink_type != after_partyunit.depotlink_type:
        x_grainunit.set_optional_arg("depotlink_type", after_partyunit.depotlink_type)
    x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_partyunit_delete(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    if before_agenda.get_partys_dict() != after_agenda.get_partys_dict():
        for before_partyunit in before_agenda._partys.values():
            if after_agenda.get_party(before_partyunit.party_id) is None:
                add_grainunit_partyunit_delete(x_learnunit, before_partyunit)


def add_grainunit_partyunit_delete(x_learnunit: LearnUnit, x_partyunit: PartyUnit):
    x_grainunit = grainunit_shop("partyunit", grain_delete())
    x_grainunit.set_locator("party_id", x_partyunit.party_id)
    x_grainunit.set_required_arg("party_id", x_partyunit.party_id)
    x_learnunit.set_grainunit(x_grainunit)


def add_grainunits_partyunit_insert(
    x_learnunit: LearnUnit, before_agenda: AgendaUnit, after_agenda: AgendaUnit
):
    if before_agenda.get_partys_dict() != after_agenda.get_partys_dict():
        for after_partyunit in after_agenda._partys.values():
            if before_agenda.get_party(after_partyunit.party_id) is None:
                add_grainunit_partyunit_insert(x_learnunit, after_partyunit)


def add_grainunit_partyunit_insert(x_learnunit: LearnUnit, x_partyunit: PartyUnit):
    x_grainunit = grainunit_shop("partyunit", grain_insert())
    x_grainunit.set_locator("party_id", x_partyunit.party_id)
    x_grainunit.set_required_arg("party_id", x_partyunit.party_id)
    if x_partyunit.creditor_weight != None:
        x_grainunit.set_optional_arg("creditor_weight", x_partyunit.creditor_weight)
    if x_partyunit.debtor_weight != None:
        x_grainunit.set_optional_arg("debtor_weight", x_partyunit.debtor_weight)
    if x_partyunit.depotlink_type != None:
        x_grainunit.set_optional_arg("depotlink_type", x_partyunit.depotlink_type)
    x_learnunit.set_grainunit(x_grainunit)
