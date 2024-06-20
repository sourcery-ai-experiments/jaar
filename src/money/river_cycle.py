from src._instrument.python import get_empty_dict_if_none
from src._road.finance import default_penny_if_none, default_money_magnitude_if_none
from src._road.road import PersonID
from src.money.scale_distribution import allot_scale
from dataclasses import dataclass


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
