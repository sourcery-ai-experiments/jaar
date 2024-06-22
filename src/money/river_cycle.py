from src._instrument.python import get_empty_dict_if_none
from src._road.finance import allot_scale
from src._road.road import PersonID, OtherID
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
class TaxUnit:
    userhub: UserHub = None
    taxledger: dict[PersonID:float] = None

    def set_other_tax_due(self, x_other_id: PersonID, tax_due: float):
        self.taxledger[x_other_id] = tax_due

    def taxledger_is_empty(self) -> bool:
        return len(self.taxledger) == 0

    def reset_taxledger(self, debtorledger: dict[PersonID:float]):
        x_amount = self.userhub.econ_money_magnitude
        self.taxledger = allot_scale(debtorledger, x_amount, self.userhub.penny)

    def other_has_tax_due(self, x_other_id: PersonID) -> bool:
        return self.taxledger.get(x_other_id) != None

    def get_other_tax_due(self, x_other_id: PersonID) -> float:
        x_tax_due = self.taxledger.get(x_other_id)
        return 0 if x_tax_due is None else x_tax_due

    def delete_tax_due(self, x_other_id: PersonID):
        self.taxledger.pop(x_other_id)

    def levy_tax_due(self, x_other_id: PersonID, payer_money: float) -> float:
        if self.other_has_tax_due(x_other_id) == False:
            return payer_money
        x_tax_due = self.get_other_tax_due(x_other_id)
        if x_tax_due > payer_money:
            left_over_pay = x_tax_due - payer_money
            self.set_other_tax_due(x_other_id, left_over_pay)
            return 0
        else:
            self.delete_tax_due(x_other_id)
            return payer_money - x_tax_due

    def get_ledger_dict(self) -> dict[PersonID:float]:
        return self.taxledger


def taxunit_shop(userhub: UserHub) -> TaxUnit:
    x_taxunit = TaxUnit(userhub)
    x_taxunit.taxledger = get_empty_dict_if_none(None)
    return x_taxunit


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
    taxunit: TaxUnit = None
    cycle_count: int = None
    cycle_max: int = None

    def levy_tax_dues(self, cycleledger: dict[OtherID:float]):
        delete_from_cycleledger = []
        for payee, payee_amount in cycleledger.items():
            if self.taxunit.other_has_tax_due(payee):
                excess_payer_money = self.taxunit.levy_tax_due(payee, payee_amount)
                if excess_payer_money == 0:
                    delete_from_cycleledger.append(payee)
                else:
                    cycleledger[payee] = excess_payer_money

        for payee_to_delete in delete_from_cycleledger:
            cycleledger.pop(payee_to_delete)


def riverrun_shop(
    userhub: UserHub,
    number: int = None,
    econ_credorledgers: dict[PersonID : dict[PersonID:float]] = None,
    taxunit: TaxUnit = None,
    cycle_max: int = None,
):
    x_riverun = RiverRun(
        userhub=userhub,
        number=number,
        econ_credorledgers=econ_credorledgers,
        taxunit=taxunit,
        cycle_max=cycle_max,
    )
    x_riverun.cycle_count = 0
    return x_riverun
