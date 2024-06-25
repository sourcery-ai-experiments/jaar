from src._instrument.python import (
    get_empty_dict_if_none,
    get_0_if_None,
    get_json_from_dict,
)
from src._road.finance import allot_scale
from src._road.road import PersonID, OwnerID
from src._world.world import WorldUnit
from src.listen.userhub import UserHub
from dataclasses import dataclass


def get_credorledger(x_world: WorldUnit) -> dict[PersonID:float]:
    return {
        personunit.person_id: personunit.credor_weight
        for personunit in x_world._persons.values()
        if personunit.credor_weight > 0
    }


def get_debtorledger(x_world: WorldUnit) -> dict[PersonID:float]:
    return {
        personunit.person_id: personunit.debtor_weight
        for personunit in x_world._persons.values()
        if personunit.debtor_weight > 0
    }


@dataclass
class RiverBook:
    userhub: UserHub = None
    owner_id: OwnerID = None
    _rivergrants: dict[PersonID:float] = None


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
    econ_credorledgers: dict[OwnerID : dict[PersonID:float]] = None
    riverbooks: dict[PersonID:RiverBook] = None

    def _set_complete_riverbook(self, x_riverbook: RiverBook):
        self.riverbooks[x_riverbook.owner_id] = x_riverbook

    def set_riverbook(self, book_person_id: PersonID, book_money_amount: float):
        owner_credorledger = self.econ_credorledgers.get(book_person_id)
        if owner_credorledger != None:
            x_riverbook = create_riverbook(
                userhub=self.userhub,
                owner_id=book_person_id,
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
    econ_credorledgers: dict[OwnerID : dict[PersonID:float]] = None,
):
    return RiverCycle(
        userhub=userhub,
        number=number,
        econ_credorledgers=get_empty_dict_if_none(econ_credorledgers),
        riverbooks=get_empty_dict_if_none(None),
    )


def create_init_rivercycle(
    leader_userhub: UserHub,
    econ_credorledgers: dict[OwnerID : dict[PersonID:float]],
) -> RiverCycle:
    x_rivercycle = rivercycle_shop(leader_userhub, 0, econ_credorledgers)
    init_amount = leader_userhub.econ_money_magnitude
    x_rivercycle.set_riverbook(leader_userhub.owner_id, init_amount)
    return x_rivercycle


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
class RiverGrade:
    userhub: UserHub = None
    person_id: PersonID = None
    number: int = None
    tax_bill_amount: float = None
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
    rewards_count: float = None
    rewards_magnitude: float = None

    def set_tax_bill_amount(self, x_tax_bill_amount: float):
        self.tax_bill_amount = x_tax_bill_amount
        self.set_tax_paid_bool()

    def set_tax_paid_amount(self, x_tax_paid_amount: float):
        self.tax_paid_amount = x_tax_paid_amount
        self.set_tax_paid_bool()

    def set_tax_paid_bool(self):
        self.tax_paid_bool = (
            self.tax_bill_amount != None
            and self.tax_bill_amount == self.tax_paid_amount
        )

    def get_dict(self) -> dict:
        return {
            "real_id": self.userhub.real_id,
            "healer_id": self.userhub.owner_id,
            "econ_road": self.userhub.econ_road,
            "tax_bill_amount": self.tax_bill_amount,
            "grant_amount": self.grant_amount,
            "debtor_rank_num": self.debtor_rank_num,
            "credor_rank_num": self.credor_rank_num,
            "tax_paid_amount": self.tax_paid_amount,
            "tax_paid_bool": self.tax_paid_bool,
            "tax_paid_rank_num": self.tax_paid_rank_num,
            "tax_paid_rank_percent": self.tax_paid_rank_percent,
            "debtor_count": self.debtor_count,
            "credor_count": self.credor_count,
            "debtor_rank_percent": self.debtor_rank_percent,
            "credor_rank_percent": self.credor_rank_percent,
            "rewards_count": self.rewards_count,
            "rewards_magnitude": self.rewards_magnitude,
        }

    def get_json(self) -> str:
        return get_json_from_dict(self.get_dict())


def rivergrade_shop(
    userhub: UserHub,
    person_id: PersonID,
    number: float = None,
    debtor_count: int = None,
    credor_count: int = None,
):
    return RiverGrade(
        userhub=userhub,
        person_id=person_id,
        number=get_0_if_None(number),
        debtor_count=debtor_count,
        credor_count=credor_count,
    )
