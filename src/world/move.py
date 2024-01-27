from src._prime.road import PersonRoad
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
    return "stir_config.json"


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
    stratification_text: str,
    expected_stratification: int = None,
) -> int:
    stir_config_dict = get_stir_config_dict()
    category_dict = stir_config_dict.get(category)
    crud_dict = category_dict.get(crud_text)
    return crud_dict.get(stratification_text)


def set_mog(
    category: str,
    crud_text: str,
    stratification_text: str,
    stratification_int: int,
) -> int:
    stir_config_dict = get_stir_config_dict()
    category_dict = stir_config_dict.get(category)
    crud_dict = category_dict.get(crud_text)
    crud_dict[stratification_text] = stratification_int
    save_stir_config_file(stir_config_dict)


@dataclass
class StirUnit:
    category: str = None
    crud_text: str = None
    locator: dict[str:str] = None
    required_args: dict[str:str] = None
    optional_args: dict[str:str] = None
    stratification: int = None

    def set_stratification(self):
        self.stratification = get_mog(
            category=self.category,
            crud_text=self.crud_text,
            stratification_text="stratification",
        )

    def add_locator(self, x_key: str, x_value: any):
        self.locator[x_key] = x_value

    def get_locator(self, x_key: str) -> any:
        return self.locator.get(x_key)

    def is_locator_valid(self) -> bool:
        category_dict = get_stir_config_dict().get(self.category)
        locator_dict = get_empty_dict_if_none(category_dict.get("locator"))
        return locator_dict.keys() == self.locator.keys()

    def add_required_arg(self, x_key: str, x_value: any):
        self.required_args[x_key] = x_value

    def _get_required_args_dict(self) -> dict:
        category_dict = get_stir_config_dict().get(self.category)
        crud_dict = category_dict.get(self.crud_text)
        return crud_dict.get("required_args")

    def is_args_valid(self) -> bool:
        if self.crud_text not in {stir_delete(), stir_insert(), stir_update()}:
            return False
        required_args_dict = get_empty_dict_if_none(self._get_required_args_dict())
        return required_args_dict.keys() == self.required_args.keys()

    def is_valid(self) -> bool:
        return self.is_locator_valid() and self.is_args_valid()

    def get_value(self, arg_key: str) -> any:
        return self.required_args.get(arg_key)


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
    if x_stirunit.category == "partyunit" and x_stirunit.crud_text == stir_delete():
        party_id = x_stirunit.get_locator("party_id")
        x_agenda.del_partyunit(party_id)
    elif x_stirunit.category == "partyunit" and x_stirunit.crud_text == stir_update():
        pass
    elif x_stirunit.category == "partyunit" and x_stirunit.crud_text == stir_insert():
        pass

    elif x_stirunit.category == "AgendaUnit_weight":
        x_agenda._weight = x_stirunit.get_value(x_stirunit.category)
    elif x_stirunit.category == "_max_tree_traverse":
        x_agenda.set_max_tree_traverse(x_stirunit.get_value(x_stirunit.category))
    elif x_stirunit.category == "_party_creditor_pool":
        x_agenda.set_party_creditor_pool(x_stirunit.get_value(x_stirunit.category))
    elif x_stirunit.category == "_party_debtor_pool":
        x_agenda.set_party_debtor_pool(x_stirunit.get_value(x_stirunit.category))
    elif x_stirunit.category == "_meld_strategy":
        x_agenda.set_meld_strategy(x_stirunit.get_value(x_stirunit.category))


@dataclass
class MoveUnit:
    agenda_road: PersonRoad = None
    delete_stirs: dict[str:StirUnit] = None
    insert_stirs: dict[str:StirUnit] = None
    update_stirs: dict[str:StirUnit] = None

    def get_stratification_stirunit_dict(self) -> dict[int:StirUnit]:
        x_dict = {}
        for xs in self.delete_stirs.values():
            add_dict_if_missing(x_dict, x_key=xs.stratification)
            x_dict[xs.stratification][xs.category] = xs
        for xs in self.insert_stirs.values():
            add_dict_if_missing(x_dict, x_key=xs.stratification)
            x_dict[xs.stratification][xs.category] = xs
        for xs in self.update_stirs.values():
            add_dict_if_missing(x_dict, x_key=xs.stratification)
            x_dict[xs.stratification][xs.category] = xs
        return x_dict

    def get_after_agenda(self, before_agenda: AgendaUnit):
        after_agenda = copy_deepcopy(before_agenda)
        stirunits = self.get_stratification_stirunit_dict()

        for stratification in sorted(stirunits.keys()):
            stra_stirunits = stirunits.get(stratification)
            for x_stir in stra_stirunits.values():
                change_agenda_with_stirunit(after_agenda, x_stirunit=x_stir)
        return after_agenda

    def set_stirunit(self, x_stirunit: StirUnit):
        if x_stirunit.is_valid():
            x_stirunit.set_stratification()
            if x_stirunit.crud_text == stir_update():
                self.update_stirs[x_stirunit.category] = x_stirunit
            elif x_stirunit.crud_text == stir_insert():
                self.insert_stirs[x_stirunit.category] = x_stirunit
            elif x_stirunit.crud_text == stir_delete():
                self.delete_stirs[x_stirunit.category] = x_stirunit

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

    def get_stir(self, crud_text: str, category: str) -> StirUnit:
        if crud_text == stir_update():
            return self.update_stirs.get(category)
        elif crud_text == stir_delete():
            return self.delete_stirs.get(category)
        elif crud_text == stir_insert():
            return self.insert_stirs.get(category)


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
