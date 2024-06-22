from src._instrument.python import (
    get_empty_dict_if_none,
    get_positive_int,
    get_0_if_None,
    place_obj_in_dict,
)
from src._road.finance import allot_scale
from src._road.road import OtherID, OwnerID
from src.agenda.agenda import AgendaUnit
from src.listen.userhub import UserHub
from dataclasses import dataclass


def get_credorledger(x_agenda: AgendaUnit) -> dict[OtherID:float]:
    return {
        otherunit.other_id: otherunit.credor_weight
        for otherunit in x_agenda._others.values()
    }


def get_debtorledger(x_agenda: AgendaUnit) -> dict[OtherID:float]:
    return {
        otherunit.other_id: otherunit.debtor_weight
        for otherunit in x_agenda._others.values()
    }


@dataclass
class RiverBook:
    userhub: UserHub = None
    owner_id: OwnerID = None
    _rivergrants: dict[OtherID:float] = None


def riverbook_shop(userhub: UserHub, owner_id: OwnerID):
    x_riverbook = RiverBook(userhub, owner_id)
    x_riverbook._rivergrants = {}
    return x_riverbook


def create_riverbook(
    userhub: UserHub,
    owner_id: OwnerID,
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
    econ_credorledgers: dict[OwnerID : dict[OtherID:float]] = None
    riverbooks: dict[OtherID:RiverBook] = None

    def _set_complete_riverbook(self, x_riverbook: RiverBook):
        self.riverbooks[x_riverbook.owner_id] = x_riverbook

    def set_riverbook(self, book_other_id: OtherID, book_money_amount: float):
        owner_credorledger = self.econ_credorledgers.get(book_other_id)
        if owner_credorledger != None:
            x_riverbook = create_riverbook(
                userhub=self.userhub,
                owner_id=book_other_id,
                econ_credorledger=owner_credorledger,
                book_money_amount=book_money_amount,
            )
            self._set_complete_riverbook(x_riverbook)

    def create_cylceledger(self) -> dict[OtherID:float]:
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
    econ_credorledgers: dict[OwnerID : dict[OtherID:float]] = None,
):
    return RiverCycle(
        userhub=userhub,
        number=number,
        econ_credorledgers=get_empty_dict_if_none(econ_credorledgers),
        riverbooks=get_empty_dict_if_none(None),
    )


def create_init_rivercycle(
    leader_userhub: UserHub,
    econ_credorledgers: dict[OwnerID : dict[OtherID:float]],
) -> RiverCycle:
    x_rivercycle = rivercycle_shop(leader_userhub, 0, econ_credorledgers)
    init_amount = leader_userhub.econ_money_magnitude
    x_rivercycle.set_riverbook(leader_userhub.person_id, init_amount)
    return x_rivercycle


def get_init_rivercycle_cycleledger(
    leader_userhub: UserHub,
    econ_credorledgers: dict[OwnerID : dict[OtherID:float]],
) -> dict[OtherID:float]:
    init_rivercycle = create_init_rivercycle(leader_userhub, econ_credorledgers)
    return init_rivercycle.create_cylceledger()


def create_next_rivercycle(
    prev_rivercycle: RiverCycle, prev_cycle_cycleledger_post_tax: dict[OtherID:float]
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
class RiverGrade:
    userhub: UserHub = None
    other_id: OtherID = None
    number: int = None
    tax_due_amount: float = None
    grant_amount: float = None
    debtor_rank_num: float = None
    credor_rank_num: float = None
    tax_paid_amount: float = None
    tax_paid_bool: float = None
    tax_paid_rank_num: float = None
    tax_paid_rank_percent: float = None
    debtor_count: float = None
    credor_count: float = None
    debtor_rank_percent: float = None
    credor_rank_percent: float = None
    transactions_count: float = None
    transactions_magnitude: float = None


def rivergrade_shop(userhub: UserHub, other_id: OtherID, number: float = None):
    return RiverGrade(userhub=userhub, other_id=other_id, number=get_0_if_None(number))


@dataclass
class RiverRun:
    userhub: UserHub = None
    number: int = None
    econ_credorledgers: dict[OwnerID : dict[OtherID:float]] = None
    taxledger: dict[OtherID:float] = None
    cycle_max: int = None
    # calculated fields
    cycle_count: int = None
    _rivergrades: dict[OtherID:RiverGrade] = None

    def set_cycle_max(self, x_cycle_max: int):
        self.cycle_max = get_positive_int(x_cycle_max)

    def set_econ_credorledger(
        self, owner_id: OwnerID, other_id: OtherID, other_credor_weight: float
    ):
        place_obj_in_dict(
            x_dict=self.econ_credorledgers,
            x_keylist=[owner_id, other_id],
            x_obj=other_credor_weight,
        )

    def delete_econ_credorledgers_owner(self, owner_id: OwnerID):
        self.econ_credorledgers.pop(owner_id)

    def get_all_econ_credorledger_other_ids(self):
        x_set = set()
        for owner_id, owner_dict in self.econ_credorledgers.items():
            if owner_id not in x_set:
                x_set.add(owner_id)
            for other_id in owner_dict.keys():
                if other_id not in x_set:
                    x_set.add(other_id)
        return x_set

    def levy_tax_dues(self, cycleledger: dict[OtherID:float]):
        delete_from_cycleledger = []
        for payee, payee_amount in cycleledger.items():
            if self.other_has_tax_due(payee):
                excess_payer_money = self.levy_tax_due(payee, payee_amount)
                if excess_payer_money == 0:
                    delete_from_cycleledger.append(payee)
                else:
                    cycleledger[payee] = excess_payer_money

        for payee_to_delete in delete_from_cycleledger:
            cycleledger.pop(payee_to_delete)

    def set_other_tax_due(self, x_other_id: OtherID, tax_due: float):
        self.taxledger[x_other_id] = tax_due

    def taxledger_is_empty(self) -> bool:
        return len(self.taxledger) == 0

    def reset_taxledger(self, debtorledger: dict[OtherID:float]):
        x_amount = self.userhub.econ_money_magnitude
        self.taxledger = allot_scale(debtorledger, x_amount, self.userhub.penny)

    def other_has_tax_due(self, x_other_id: OtherID) -> bool:
        return self.taxledger.get(x_other_id) != None

    def get_other_tax_due(self, x_other_id: OtherID) -> float:
        x_tax_due = self.taxledger.get(x_other_id)
        return 0 if x_tax_due is None else x_tax_due

    def delete_tax_due(self, x_other_id: OtherID):
        self.taxledger.pop(x_other_id)

    def levy_tax_due(self, x_other_id: OtherID, payer_money: float) -> float:
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

    def get_ledger_dict(self) -> dict[OtherID:float]:
        return self.taxledger

    def set_initial_rivergrade(self, other_id: OtherID):
        self._rivergrades[other_id] = rivergrade_shop(
            self.userhub, other_id, self.number
        )

    def get_rivergrade(self, other_id: OtherID) -> RiverGrade:
        return self._rivergrades.get(other_id)

    def _rivergrades_is_empty(self) -> bool:
        return self._rivergrades == {}

    def rivergrade_exists(self, other_id: OtherID) -> bool:
        return self._rivergrades.get(other_id) != None

    def reset_initial_rivergrades(self):
        self._rivergrades = {}
        all_other_ids = self.get_all_econ_credorledger_other_ids()
        for other_id in all_other_ids:
            self.set_initial_rivergrade(other_id)

    def calc_metrics(self):
        self.cycle_count = 0
        self.reset_initial_rivergrades()

        init_rivercylce = create_init_rivercycle(self.userhub, self.econ_credorledgers)

        self.cycle_count = 1


def riverrun_shop(
    userhub: UserHub,
    number: int = None,
    econ_credorledgers: dict[OwnerID : dict[OtherID:float]] = None,
    taxledger: dict[OtherID:float] = None,
    cycle_max: int = None,
):
    x_riverun = RiverRun(
        userhub=userhub,
        number=get_0_if_None(number),
        econ_credorledgers=get_empty_dict_if_none(econ_credorledgers),
        taxledger=get_empty_dict_if_none(taxledger),
        _rivergrades={},
    )
    x_riverun.cycle_count = 0
    if cycle_max is None:
        cycle_max = 10
    x_riverun.set_cycle_max(cycle_max)
    return x_riverun
