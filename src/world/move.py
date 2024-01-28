from src._prime.road import PersonRoad
from src.agenda.party import partyunit_shop, partylink_shop
from src.agenda.group import groupunit_shop
from src.agenda.agenda import AgendaUnit, agendaunit_shop
from src.world.examples.world_env_kit import get_src_world_dir
from src.tools.python import (
    get_empty_dict_if_none,
    x_get_json,
    x_get_dict,
    add_dict_if_missing,
)
from src.tools.file import open_file, save_file
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


def stir_update() -> str:
    return "UPDATE"


def stir_insert() -> str:
    return "INSERT"


def stir_delete() -> str:
    return "DELETE"


def get_stir_config_file_name() -> str:
    return "stir_categorys.json"


def get_stir_config_dict() -> dict:
    return x_get_dict(open_file(get_src_world_dir(), get_stir_config_file_name()))


def save_stir_config_file(stir_config_dict):
    save_file(
        dest_dir=get_src_world_dir(),
        file_name=get_stir_config_file_name(),
        file_text=x_get_json(stir_config_dict),
    )


def category_ref() -> set:
    return get_stir_config_dict().keys()


def is_category_ref(category_text: str) -> bool:
    return category_text in category_ref()


def get_mog(
    category: str,
    crud_text: str,
    stir_order_text: str,
    expected_stir_order: int = None,
) -> int:
    stir_config_dict = get_stir_config_dict()
    category_dict = stir_config_dict.get(category)
    crud_dict = category_dict.get(crud_text)
    return crud_dict.get(stir_order_text)


def set_mog(
    category: str,
    crud_text: str,
    stir_order_text: str,
    stir_order_int: int,
) -> int:
    stir_config_dict = get_stir_config_dict()
    category_dict = stir_config_dict.get(category)
    crud_dict = category_dict.get(crud_text)
    crud_dict[stir_order_text] = stir_order_int
    save_stir_config_file(stir_config_dict)


@dataclass
class StirUnit:
    category: str = None
    crud_text: str = None
    locator: dict[str:str] = None
    required_args: dict[str:str] = None
    optional_args: dict[str:str] = None
    stir_order: int = None

    def set_stir_order(self):
        self.stir_order = get_mog(
            category=self.category,
            crud_text=self.crud_text,
            stir_order_text="stir_order",
        )

    def set_locator(self, x_key: str, x_value: any):
        self.locator[x_key] = x_value

    def get_locator(self, x_key: str) -> any:
        return self.locator.get(x_key)

    def get_locator_key(self) -> str:
        x_text = f"{self.category}"
        for locator_key in sorted(self.locator.keys()):
            x_text = f"{x_text} {self.locator.get(locator_key)}"
        return x_text.lstrip().rstrip()

    def is_locator_valid(self) -> bool:
        category_dict = get_stir_config_dict().get(self.category)
        locator_dict = get_empty_dict_if_none(category_dict.get("locator"))
        return locator_dict.keys() == self.locator.keys()

    def set_required_arg(self, x_key: str, x_value: any):
        self.required_args[x_key] = x_value

    def set_optional_arg(self, x_key: str, x_value: any):
        self.optional_args[x_key] = x_value

    def _get_category_dict(self):
        return get_stir_config_dict().get(self.category)

    def _get_required_args_dict(self) -> dict:
        crud_dict = self._get_category_dict().get(self.crud_text)
        return crud_dict.get("required_args")

    def _get_optional_args_dict(self) -> dict:
        crud_dict = self._get_category_dict().get(self.crud_text)
        return crud_dict.get("optional_args")

    def is_required_args_valid(self) -> bool:
        if self.crud_text not in {stir_delete(), stir_insert(), stir_update()}:
            return False
        required_args_dict = get_empty_dict_if_none(self._get_required_args_dict())
        return required_args_dict.keys() == self.required_args.keys()

    def is_optional_args_valid(self) -> bool:
        if self.crud_text not in {stir_delete(), stir_insert(), stir_update()}:
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
        print(f"{required_value} {self.required_args=} {arg_key=}")
        if required_value is None:
            return self.optional_args.get(arg_key)
        return required_value


def stirunit_shop(
    category: str,
    crud_text: str = None,
    locator: dict[str:str] = None,
    required_args: dict[str:str] = None,
    optional_args: dict[str:str] = None,
) -> StirUnit:
    if is_category_ref(category):
        return StirUnit(
            category=category,
            crud_text=crud_text,
            locator=get_empty_dict_if_none(locator),
            required_args=get_empty_dict_if_none(required_args),
            optional_args=get_empty_dict_if_none(optional_args),
        )


def change_agenda_with_stirunit(x_agenda: AgendaUnit, x_stirunit: StirUnit):
    xs = x_stirunit
    if xs.category == "partyunit" and xs.crud_text == stir_delete():
        party_id = xs.get_locator("party_id")
        x_agenda.del_partyunit(party_id)
    elif xs.category == "partyunit" and xs.crud_text == stir_update():
        x_agenda.edit_partyunit(
            party_id=xs.get_value("party_id"),
            creditor_weight=xs.get_value("creditor_weight"),
            debtor_weight=xs.get_value("debtor_weight"),
            depotlink_type=xs.get_value("depotlink_type"),
        )
    elif xs.category == "partyunit" and xs.crud_text == stir_insert():
        x_agenda.set_partyunit(
            partyunit_shop(
                party_id=xs.get_value("party_id"),
                creditor_weight=xs.get_value("creditor_weight"),
                debtor_weight=xs.get_value("debtor_weight"),
                depotlink_type=xs.get_value("depotlink_type"),
            )
        )
    elif xs.category == "groupunit_partylink" and xs.crud_text == stir_delete():
        group_id = xs.get_locator("group_id")
        party_id = xs.get_locator("party_id")
        x_agenda.get_groupunit(group_id).del_partylink(party_id)
    elif xs.category == "groupunit_partylink" and xs.crud_text == stir_update():
        x_groupunit = x_agenda.get_groupunit(xs.get_value("group_id"))
        x_groupunit.edit_partylink(
            party_id=xs.get_value("party_id"),
            creditor_weight=xs.get_value("creditor_weight"),
            debtor_weight=xs.get_value("debtor_weight"),
        )
    elif xs.category == "groupunit_partylink" and xs.crud_text == stir_insert():
        x_groupunit = x_agenda.get_groupunit(xs.get_locator("group_id"))
        x_groupunit.set_partylink(
            partylink_shop(
                party_id=xs.get_locator("party_id"),
                creditor_weight=xs.get_value("creditor_weight"),
                debtor_weight=xs.get_value("debtor_weight"),
            )
        )
    elif xs.category == "groupunit" and xs.crud_text == stir_delete():
        group_id = xs.get_locator("group_id")
        x_agenda.del_groupunit(group_id)
    elif xs.category == "groupunit" and xs.crud_text == stir_update():
        if xs.get_value("_partylinks_set_by_economy_road") != None:
            x_groupunit = x_agenda.get_groupunit(xs.get_value("group_id"))
            x_groupunit._partylinks_set_by_economy_road = xs.get_value(
                "_partylinks_set_by_economy_road"
            )
    elif xs.category == "groupunit" and xs.crud_text == stir_insert():
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
    elif xs.category == "idea" and xs.crud_text == stir_delete():
        idea_road = xs.get_locator("road")
        del_children = xs.get_value("del_children")
        x_agenda.del_idea_kid(idea_road, del_children=del_children)
    elif xs.category == "idea" and xs.crud_text == stir_update():
        pass
    elif xs.category == "idea" and xs.crud_text == stir_insert():
        pass
    elif xs.category == "idea_balancelink" and xs.crud_text == stir_delete():
        idea_road = xs.get_locator("road")
        group_id = xs.get_value("group_id")
        x_agenda.edit_idea_attr(idea_road, balancelink_del=group_id)
    elif xs.category == "idea_balancelink" and xs.crud_text == stir_update():
        pass
    elif xs.category == "idea_balancelink" and xs.crud_text == stir_insert():
        pass

    elif xs.category == "AgendaUnit_weight":
        x_agenda._weight = xs.get_value(xs.category)
    elif xs.category == "_max_tree_traverse":
        x_agenda.set_max_tree_traverse(xs.get_value(xs.category))
    elif xs.category == "_party_creditor_pool":
        x_agenda.set_party_creditor_pool(xs.get_value(xs.category))
    elif xs.category == "_party_debtor_pool":
        x_agenda.set_party_debtor_pool(xs.get_value(xs.category))
    elif xs.category == "_meld_strategy":
        x_agenda.set_meld_strategy(xs.get_value(xs.category))


@dataclass
class MoveUnit:
    agenda_road: PersonRoad = None
    delete_stirs: dict[str:StirUnit] = None
    insert_stirs: dict[str:StirUnit] = None
    update_stirs: dict[str:StirUnit] = None

    def get_stir_order_stirunit_dict(self) -> dict[int:StirUnit]:
        x_dict = {}
        for xs in self.delete_stirs.values():
            add_dict_if_missing(x_dict, x_key1=xs.stir_order)
            x_dict[xs.stir_order][xs.get_locator_key()] = xs
        for xs in self.insert_stirs.values():
            add_dict_if_missing(x_dict, x_key1=xs.stir_order)
            x_dict[xs.stir_order][xs.get_locator_key()] = xs
        for xs in self.update_stirs.values():
            add_dict_if_missing(x_dict, x_key1=xs.stir_order)
            x_dict[xs.stir_order][xs.get_locator_key()] = xs
        return x_dict

    def get_after_agenda(self, before_agenda: AgendaUnit):
        after_agenda = copy_deepcopy(before_agenda)
        stirunits = self.get_stir_order_stirunit_dict()

        for stir_order in sorted(stirunits.keys()):
            stra_stirunits = stirunits.get(stir_order)
            for x_stir in stra_stirunits.values():
                change_agenda_with_stirunit(after_agenda, x_stirunit=x_stir)
        return after_agenda

    def set_stirunit(self, x_stirunit: StirUnit):
        if x_stirunit.is_valid():
            x_stirunit.set_stir_order()
            if x_stirunit.crud_text == stir_update():
                self.update_stirs[x_stirunit.get_locator_key()] = x_stirunit
            elif x_stirunit.crud_text == stir_insert():
                self.insert_stirs[x_stirunit.get_locator_key()] = x_stirunit
            elif x_stirunit.crud_text == stir_delete():
                self.delete_stirs[x_stirunit.get_locator_key()] = x_stirunit

    def add_stirunit(
        self,
        category: str,
        crud_text: str,
        locator: str = None,
        required_args: str = None,
        optional_args: str = None,
    ):
        x_stirunit = stirunit_shop(
            category=category,
            crud_text=crud_text,
            locator=locator,
            required_args=required_args,
            optional_args=optional_args,
        )
        self.set_stirunit(x_stirunit)

    def get_stir(self, crud_text: str, locator_key: str) -> StirUnit:
        if crud_text == stir_update():
            return self.update_stirs.get(locator_key)
        elif crud_text == stir_delete():
            return self.delete_stirs.get(locator_key)
        elif crud_text == stir_insert():
            return self.insert_stirs.get(locator_key)


def moveunit_shop(
    agenda_road: PersonRoad,
    delete_stirs: dict[str:str] = None,
    insert_stirs: dict[str:str] = None,
    update_stirs: dict[str:str] = None,
):
    return MoveUnit(
        agenda_road=agenda_road,
        delete_stirs=get_empty_dict_if_none(delete_stirs),
        insert_stirs=get_empty_dict_if_none(insert_stirs),
        update_stirs=get_empty_dict_if_none(update_stirs),
    )
