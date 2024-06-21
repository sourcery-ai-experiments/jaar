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
    _rivergrants: dict[PersonID:float] = None


def riverbook_shop(userhub: UserHub, owner_id: PersonID):
    x_riverbook = RiverBook(userhub, owner_id)
    x_riverbook._rivergrants = {}
    return x_riverbook


def create_riverbook(
    userhub: UserHub,
    owner_id: PersonID,
    econ_credorledger: dict,
    book_money_amount: int,
) -> RiverBook:
    x_riverbook = riverbook_shop(userhub, owner_id)
    x_riverbook._rivergrants = allot_scale(
        ledger=econ_credorledger,
        scale_number=book_money_amount,
        grain_unit=x_riverbook.userhub.penny,
    )
    return x_riverbook


@dataclass
class RiverCycle:
    userhub: UserHub = None
    number: int = None
    econ_credorledgers: dict[PersonID : dict[PersonID:float]] = None
    riverbooks: dict[PersonID:RiverBook] = None

    def _set_complete_riverbook(self, x_riverbook: RiverBook):
        self.riverbooks[x_riverbook.owner_id] = x_riverbook

    def set_riverbook(self, book_owner_id: PersonID, book_money_amount: float):
        owner_credorledger = self.econ_credorledgers.get(book_owner_id)
        if owner_credorledger != None:
            x_riverbook = create_riverbook(
                userhub=self.userhub,
                owner_id=book_owner_id,
                econ_credorledger=owner_credorledger,
                book_money_amount=book_money_amount,
            )
            self._set_complete_riverbook(x_riverbook)

    def create_cylceledger(self) -> dict[PersonID:float]:
        x_dict = {}
        for x_riverbook in self.riverbooks.values():
            for payee, pay_amount in x_riverbook._rivergrants.items():
                if x_dict.get(payee) is None:
                    x_dict[payee] = pay_amount
                else:
                    x_dict[payee] = x_dict[payee] + pay_amount
        return x_dict


def rivercycle_shop(
    userhub: UserHub,
    number: int,
    econ_credorledgers: dict[PersonID : dict[PersonID:float]] = None,
):
    return RiverCycle(
        userhub=userhub,
        number=number,
        econ_credorledgers=get_empty_dict_if_none(econ_credorledgers),
        riverbooks=get_empty_dict_if_none(None),
    )


def create_init_rivercycle(
    leader_userhub: UserHub,
    econ_credorledgers: dict[PersonID : dict[PersonID:float]],
) -> RiverCycle:
    x_rivercycle = rivercycle_shop(leader_userhub, 0, econ_credorledgers)
    init_amount = leader_userhub.econ_money_magnitude
    x_rivercycle.set_riverbook(leader_userhub.person_id, init_amount)
    return x_rivercycle


def get_init_rivercycle_cycleledger(
    leader_userhub: UserHub,
    econ_credorledgers: dict[PersonID : dict[PersonID:float]],
) -> dict[PersonID:float]:
    init_rivercycle = create_init_rivercycle(leader_userhub, econ_credorledgers)
    return init_rivercycle.create_cylceledger()


def create_next_rivercycle(
    prev_rivercycle: RiverCycle, prev_cycle_cycleledger_post_tax: dict[PersonID:float]
) -> RiverCycle:
    next_rivercycle = rivercycle_shop(
        userhub=prev_rivercycle.userhub,
        number=prev_rivercycle.number + 1,
        econ_credorledgers=prev_rivercycle.econ_credorledgers,
    )
    for payer_id, paying_amount in prev_cycle_cycleledger_post_tax.items():
        next_rivercycle.set_riverbook(payer_id, paying_amount)
    return next_rivercycle


@dataclass
class RiverRun:
    userhub: UserHub = None
    number: int = None
    econ_credorledgers: dict[PersonID : dict[PersonID:float]] = None
    due_taxes: dict[PersonID:float] = None
    cycle_count: int = None
    cycle_max: int = None


def riverrun_shop(
    userhub: UserHub,
    number: int = None,
    econ_credorledgers: dict[PersonID : dict[PersonID:float]] = None,
    due_taxes: dict[PersonID:float] = None,
    cycle_max: int = None,
):
    x_riverun = RiverRun(
        userhub=userhub,
        number=number,
        econ_credorledgers=econ_credorledgers,
        due_taxes=due_taxes,
        cycle_max=cycle_max,
    )
    x_riverun.cycle_count = 0
    return x_riverun
