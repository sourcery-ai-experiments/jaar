from src._instrument.python import get_empty_dict_if_none
from src._road.finance import (
    default_penny_if_none,
    default_money_magnitude_if_none,
    allot_scale,
)
from src._road.road import PersonID
from src.agenda.agenda import AgendaUnit
from src.listen.userhub import UserHub
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
    userhub: UserHub = None
    tax_due_ledger: dict[PersonID:float] = None

    def set_other_tax_due(self, x_other_id: PersonID, tax_due: float):
        self.tax_due_ledger[x_other_id] = tax_due

    def tax_due_ledger_is_empty(self) -> bool:
        return len(self.tax_due_ledger) == 0

    def reset_tax_due_ledger(self, debtorledger: dict[PersonID:float]):
        x_amount = self.userhub.econ_money_magnitude
        self.tax_due_ledger = allot_scale(debtorledger, x_amount, self.userhub.penny)

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


def taxdueledger_shop(userhub: UserHub) -> TaxDueLedger:
    x_taxdueledger = TaxDueLedger(userhub)
    x_taxdueledger.tax_due_ledger = get_empty_dict_if_none(None)
    return x_taxdueledger


@dataclass
class RiverBook:
    userhub: UserHub = None
    owner_id: PersonID = None
    book_money_amount: int = None
    _rivergrants: dict[PersonID:float] = None


def riverbook_shop(userhub: UserHub, owner_id: PersonID, book_money_amount: int):
    x_riverbook = RiverBook(userhub, owner_id, book_money_amount)
    x_riverbook._rivergrants = {}
    return x_riverbook


def create_riverbook(
    userhub: UserHub, owner_id: PersonID, x_credorledger: dict, book_money_amount: int
) -> RiverBook:
    x_riverbook = riverbook_shop(userhub, owner_id, book_money_amount)
    x_riverbook._rivergrants = allot_scale(
        ledger=x_credorledger,
        scale_number=x_riverbook.book_money_amount,
        grain_unit=x_riverbook.userhub.penny,
    )
    return x_riverbook


@dataclass
class RiverCycle:
    userhub: UserHub = None
    number: int = None
    credorledgers: dict[PersonID:float] = None
    riverbooks: list[RiverBook] = None
    cycle_money_amount: int = None

    def set_riverbook(self, x_riverbook: RiverBook):
        self.riverbooks[x_riverbook.owner_id] = x_riverbook

    def create_cylceledger(self) -> dict[PersonID:float]:
        return {}


def rivercycle_shop(
    userhub: UserHub,
    number: int,
    credorledgers: dict[PersonID:float] = None,
    riverbooks: list[RiverBook] = None,
    cycle_money_amount: int = None,
):
    return RiverCycle(
        userhub=userhub,
        number=number,
        credorledgers=get_empty_dict_if_none(credorledgers),
        riverbooks=get_empty_dict_if_none(riverbooks),
        cycle_money_amount=default_money_magnitude_if_none(cycle_money_amount),
    )


def create_init_rivercycle(
    leader_userhub: UserHub,
    credorledgers,
) -> RiverCycle:
    money_amount = leader_userhub.econ_money_magnitude
    x_rivercycle = rivercycle_shop(
        leader_userhub, 0, credorledgers, cycle_money_amount=money_amount
    )
    leader_id = leader_userhub.person_id
    x_credorledger = credorledgers.get(leader_id)
    init_riverbook = create_riverbook(
        leader_userhub, leader_id, x_credorledger, book_money_amount=money_amount
    )
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
