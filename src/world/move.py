from src._prime.road import PersonRoad
from src.agenda.agenda import AgendaUnit, agendaunit_shop
from src.world.examples.world_env_kit import get_src_world_dir
from src.tools.python import get_empty_dict_if_none, x_get_json, x_get_dict
from src.tools.file import open_file
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


def stir_update() -> str:
    return "UPDATE"


def stir_insert() -> str:
    return "INSERT"


def stir_delete() -> str:
    return "DELETE"


def get_stir_config_dict() -> dict:
    return x_get_dict(open_file(get_src_world_dir(), "stir_config.json"))


def attribute_ref() -> set:
    return get_stir_config_dict().keys()


def is_attribute_ref(attribute_text: str) -> bool:
    return attribute_text in attribute_ref()


@dataclass
class StirUnit:
    attribute_name: str = None
    crud_command: str = None
    locator: dict[str:str] = None
    required_args: dict[str:str] = None
    optional_args: dict[str:str] = None

    def is_locator_valid(self) -> bool:
        attribute_dict = get_stir_config_dict().get(self.attribute_name)
        locator_dict = get_empty_dict_if_none(attribute_dict.get("locator"))
        return locator_dict.keys() == self.locator.keys()

    def add_required_arg(self, x_key: str, x_value: any):
        self.required_args[x_key] = x_value

    def _get_required_args_dict(self) -> dict:
        attribute_dict = get_stir_config_dict().get(self.attribute_name)
        crud_dict = attribute_dict.get(self.crud_command)
        return crud_dict.get("required_args")

    def is_args_valid(self) -> bool:
        if self.crud_command not in {stir_delete(), stir_insert(), stir_update()}:
            return False
        required_args_dict = get_empty_dict_if_none(self._get_required_args_dict())
        return required_args_dict.keys() == self.required_args.keys()

    def is_valid(self) -> bool:
        return self.is_locator_valid() and self.is_args_valid()

    def get_value(self, arg: str) -> any:
        return self.required_args.get(arg)


def stirunit_shop(
    attribute_name: str,
    crud_command: str = None,
    locator: dict[str:str] = None,
    required_args: dict[str:str] = None,
    optional_args: dict[str:str] = None,
) -> StirUnit:
    if is_attribute_ref(attribute_name):
        return StirUnit(
            attribute_name=attribute_name,
            crud_command=crud_command,
            locator=get_empty_dict_if_none(locator),
            required_args=get_empty_dict_if_none(required_args),
            optional_args=get_empty_dict_if_none(optional_args),
        )


@dataclass
class MoveUnit:
    agenda_road: PersonRoad = None
    delete_stirs: dict[str:StirUnit] = None
    insert_stirs: dict[str:StirUnit] = None
    update_stirs: dict[str:StirUnit] = None

    def get_after_agenda(self, before_agenda: AgendaUnit):
        after_agenda = copy_deepcopy(before_agenda)
        agenda_weight_text = "AgendaUnit._weight"
        agenda_max_tree_traverse = "_max_tree_traverse"
        agenda_party_creditor_pool = "_party_creditor_pool"
        agenda_party_debtor_pool = "_party_debtor_pool"
        agenda_meld_strategy = "_meld_strategy"

        x_stirunit = self.update_stirs.get(agenda_weight_text)
        if x_stirunit != None:
            after_agenda._weight = x_stirunit.get_value(agenda_weight_text)
        x_stirunit = self.update_stirs.get(agenda_max_tree_traverse)
        if x_stirunit != None:
            after_agenda.set_max_tree_traverse(
                x_stirunit.get_value(agenda_max_tree_traverse)
            )
        x_stirunit = self.update_stirs.get(agenda_party_creditor_pool)
        if x_stirunit != None:
            after_agenda.set_party_creditor_pool(
                x_stirunit.get_value(agenda_party_creditor_pool)
            )
        x_stirunit = self.update_stirs.get(agenda_party_debtor_pool)
        if x_stirunit != None:
            after_agenda.set_party_debtor_pool(
                x_stirunit.get_value(agenda_party_debtor_pool)
            )
        x_stirunit = self.update_stirs.get(agenda_meld_strategy)
        if x_stirunit != None:
            after_agenda.set_meld_strategy(x_stirunit.get_value(agenda_meld_strategy))
        return after_agenda

    def set_stirunit(self, x_stirunit: StirUnit):
        if x_stirunit.is_valid():
            if x_stirunit.crud_command == stir_update():
                self.update_stirs[x_stirunit.attribute_name] = x_stirunit
            elif x_stirunit.crud_command == stir_insert():
                self.insert_stirs[x_stirunit.attribute_name] = x_stirunit
            elif x_stirunit.crud_command == stir_delete():
                self.delete_stirs[x_stirunit.attribute_name] = x_stirunit

    def add_stirunit(
        self,
        attribute_name: str,
        stir_crud: str,
        locator: str = None,
        required_args: str = None,
        optional_args: str = None,
    ):
        x_stirunit = stirunit_shop(
            attribute_name=attribute_name,
            crud_command=stir_crud,
            locator=locator,
            required_args=required_args,
            optional_args=optional_args,
        )
        self.set_stirunit(x_stirunit)


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
