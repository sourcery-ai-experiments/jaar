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

    def add_locator(self, x_key: str, x_value: any):
        self.locator[x_key] = x_value

    def get_locator(self, x_key: str) -> any:
        return self.locator.get(x_key)

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

    def get_value(self, arg_key: str) -> any:
        return self.required_args.get(arg_key)


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
        agendaunit_simple_attrs = {
            "AgendaUnit._weight",
            "_max_tree_traverse",
            "_party_creditor_pool",
            "_party_debtor_pool",
            "_meld_strategy",
        }

        for x_stir in self.delete_stirs.values():
            if x_stir.attribute_name == "partyunit":
                party_id = x_stir.get_locator("party_id")
                after_agenda.del_partyunit(party_id)

        for simple_attr in agendaunit_simple_attrs:
            x_stir = self.get_stir(stir_update(), simple_attr)
            if x_stir != None:
                if simple_attr == "AgendaUnit._weight":
                    after_agenda._weight = x_stir.get_value(simple_attr)
                elif simple_attr == "_max_tree_traverse":
                    after_agenda.set_max_tree_traverse(x_stir.get_value(simple_attr))
                elif simple_attr == "_party_creditor_pool":
                    after_agenda.set_party_creditor_pool(x_stir.get_value(simple_attr))
                elif simple_attr == "_party_debtor_pool":
                    after_agenda.set_party_debtor_pool(x_stir.get_value(simple_attr))
                elif simple_attr == "_meld_strategy":
                    after_agenda.set_meld_strategy(x_stir.get_value(simple_attr))

        # for x_stir in self.update_stirs.values():
        #     if x_stir.attribute_name == "partyunit":
        #         #first get current partyunit
        #         #update current partyunit
        #         # save current partyunit?

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

    def get_stir(self, crud_command: str, attribute_name: str) -> StirUnit:
        if crud_command == stir_update():
            return self.update_stirs.get(attribute_name)
        elif crud_command == stir_delete():
            return self.delete_stirs.get(attribute_name)
        elif crud_command == stir_insert():
            return self.insert_stirs.get(attribute_name)


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
