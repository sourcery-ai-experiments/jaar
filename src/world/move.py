from src._prime.road import PersonRoad
from src.agenda.agenda import AgendaUnit, agendaunit_shop
from src.tools.python import get_empty_dict_if_none
from dataclasses import dataclass
from copy import deepcopy as copy_deepcopy


@dataclass
class MoveUnit:
    agenda_road: PersonRoad = None
    stirs: dict[str:str] = None

    def get_after_agenda(self, before_agenda: AgendaUnit):
        crud_text = "crud"
        update_text = "UPDATE"
        after_agenda = copy_deepcopy(before_agenda)
        agenda_weight_text = "AgendaUnit._weight"
        agenda_max_tree_traverse = "_max_tree_traverse"
        agenda_party_creditor_pool = "_party_creditor_pool"
        agenda_party_debtor_pool = "_party_debtor_pool"
        agenda_meld_strategy = "_meld_strategy"

        x_stir = self.stirs.get(agenda_weight_text)
        if x_stir != None and x_stir.get(crud_text) == update_text:
            after_agenda._weight = x_stir.get(agenda_weight_text)
        x_stir = self.stirs.get(agenda_max_tree_traverse)
        if x_stir != None and x_stir.get(crud_text) == update_text:
            after_agenda.set_max_tree_traverse(x_stir.get(agenda_max_tree_traverse))
        x_stir = self.stirs.get(agenda_party_creditor_pool)
        if x_stir != None and x_stir.get(crud_text) == update_text:
            after_agenda.set_party_creditor_pool(x_stir.get(agenda_party_creditor_pool))
        x_stir = self.stirs.get(agenda_party_debtor_pool)
        if x_stir != None and x_stir.get(crud_text) == update_text:
            after_agenda.set_party_debtor_pool(x_stir.get(agenda_party_debtor_pool))
        x_stir = self.stirs.get(agenda_meld_strategy)
        if x_stir != None and x_stir.get(crud_text) == update_text:
            after_agenda.set_meld_strategy(x_stir.get(agenda_meld_strategy))
        return after_agenda

    def set_stir(
        self, attr_name: str, crud: str, record_locator: str = None, arg1: str = None
    ):
        crud_text = "crud"
        create_text = "CREATE"
        update_text = "UPDATE"
        delete_text = "DELETE"
        print(f"{attr_name=}")
        if crud == update_text and attr_name in {
            "AgendaUnit._weight",
            "_max_tree_traverse",
            "_party_creditor_pool",
            "_party_debtor_pool",
            "_meld_strategy",
        }:
            self.stirs[attr_name] = {crud_text: update_text, attr_name: arg1}
        # elif attr_name == "AgendaUnit._party_creditor_pool":
        #     self.stirs = {attr_name: {crud_text: update_text, "_party_creditor_pool": arg1}}
        # elif attr_name == "AgendaUnit._party_debtor_pool":
        #     self.stirs = {attr_name: {crud_text: update_text, "_party_debtor_pool": arg1}}
        # elif attr_name == "AgendaUnit._auto_output_to_forum":
        #     self.stirs = {attr_name: {crud_text: update_text, "_auto_output_to_forum": arg1}}
        # elif attr_name == "AgendaUnit._meld_strategy":
        #     self.stirs = {attr_name: {crud_text: update_text, "_meld_strategy": arg1}}


def moveunit_shop(agenda_road: PersonRoad, stirs: dict[str:str] = None):
    return MoveUnit(agenda_road=agenda_road, stirs=get_empty_dict_if_none(stirs))
