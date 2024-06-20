from src._instrument.python import get_empty_dict_if_none
from src._road.finance import (
    default_penny_if_none,
    default_money_magnitude_if_none,
    allot_scale,
)
from src._road.road import PersonID
from src.agenda.agenda import AgendaUnit
from dataclasses import dataclass


def get_credorledger(x_agenda: AgendaUnit) -> dict[PersonID:float]:
    return {
        otherunit.other_id: otherunit.credor_weight
        for otherunit in x_agenda._others.values()
    }


def get_debtorledger(x_agenda: AgendaUnit) -> dict[PersonID:float]:
    return {
        otherunit.other_id: otherunit.debtor_weight
        for otherunit in x_agenda._others.values()
    }


@dataclass
class TaxDueLedger:
    healer_id: PersonID = None
    tax_due_ledger: dict[PersonID:float] = None
    money_amount: float = None
    penny: float = None

    def set_other_tax_due(self, x_other_id: PersonID, tax_due: float):
        self.tax_due_ledger[x_other_id] = tax_due

    def tax_due_ledger_is_empty(self) -> bool:
        return len(self.tax_due_ledger) == 0

    def reset_tax_due_ledger(self, debtorledger: dict[PersonID:float]):
        self.tax_due_ledger = allot_scale(debtorledger, self.money_amount, self.penny)

    def other_has_tax_due(self, x_other_id: PersonID) -> bool:
        return self.tax_due_ledger.get(x_other_id) != None

    def get_other_tax_due(self, x_other_id: PersonID) -> float:
        x_tax_due = self.tax_due_ledger.get(x_other_id)
        return 0 if x_tax_due is None else x_tax_due

    def delete_tax_due(self, x_other_id: PersonID):
        self.tax_due_ledger.pop(x_other_id)

    def pay_any_tax_due(self, x_other_id: PersonID, payer_money: float) -> float:
        if self.other_has_tax_due(x_other_id) == False:
            return payer_money
        x_tax_due = self.get_other_tax_due(x_other_id)
        if x_tax_due > payer_money:
            left_over_pay = x_tax_due - payer_money
            self.set_other_tax_due(x_other_id, left_over_pay)
        else:
            self.delete_tax_due(x_other_id)
            return payer_money - x_tax_due


def taxdueledger_shop(
    healer_id: PersonID, money_amount: float = None, penny: float = None
) -> TaxDueLedger:
    x_taxdueledger = TaxDueLedger(healer_id)
    x_taxdueledger.tax_due_ledger = get_empty_dict_if_none(None)
    x_taxdueledger.money_amount = default_money_magnitude_if_none(money_amount)
    x_taxdueledger.penny = default_penny_if_none(penny)
    return x_taxdueledger


@dataclass
class RiverBook:
    _owner_id: PersonID = None
    _money_amount: int = None
    _rivergrants: dict[PersonID:float] = None
    penny: float = None


def riverbook_shop(owner_id: PersonID, money_amount: int, penny: float):
    x_riverbook = RiverBook(owner_id, penny=default_penny_if_none(penny))
    x_riverbook._money_amount = money_amount
    x_riverbook._rivergrants = {}
    return x_riverbook


def create_riverbook(
    owner_id: PersonID, x_credorledger: dict, money_amount: int, penny: float = None
) -> RiverBook:
    x_riverbook = riverbook_shop(owner_id, money_amount, penny)
    x_riverbook._rivergrants = allot_scale(
        x_credorledger, x_riverbook._money_amount, x_riverbook.penny
    )
    return x_riverbook


@dataclass
class RiverCycle:
    number: int = None
    credorledgers: dict[PersonID:float] = None
    riverbooks: list[RiverBook] = None
    money_amount: int = None
    penny: float = None

    def set_riverbook(self, x_riverbook: RiverBook):
        self.riverbooks[x_riverbook._owner_id] = x_riverbook

    def create_cylceledger(self) -> dict[PersonID:float]:
        return {}


def rivercycle_shop(
    number: int,
    credorledgers: dict[PersonID:float] = None,
    riverbooks: list[RiverBook] = None,
    money_amount: int = None,
    penny=None,
):
    return RiverCycle(
        number=number,
        credorledgers=get_empty_dict_if_none(credorledgers),
        riverbooks=get_empty_dict_if_none(riverbooks),
        money_amount=default_money_magnitude_if_none(money_amount),
        penny=default_penny_if_none(penny),
    )


def create_init_rivercycle(
    leader_id: PersonID, credorledgers, money_amount: int = None, penny: float = None
) -> RiverCycle:
    money_amount = default_money_magnitude_if_none(money_amount)
    x_rivercycle = rivercycle_shop(
        0, credorledgers, money_amount=money_amount, penny=penny
    )
    x_credorledger = credorledgers.get(leader_id)
    init_riverbook = create_riverbook(leader_id, x_credorledger, money_amount, penny)
    x_rivercycle.set_riverbook(init_riverbook)
    return x_rivercycle


@dataclass
class RiverRun:
    number: int = None
    due_taxes: dict[PersonID:float] = None
    cycle_curr: RiverCycle = None
    cyclc_next: RiverCycle = None
    cycle_count: int = None
    cycle_max: int = None
    money_amount: int = None
    penny: int = None
