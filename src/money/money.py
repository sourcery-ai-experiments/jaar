from src._road.road import OtherID
from src.listen.userhub import UserHub
from dataclasses import dataclass


@dataclass
class OtherMoneyReport:
    other_id: OtherID = None
    grant_count: int = None
    grant_amount: float = None
    grant_rank_num: int = None
    grant_rank_percent: float = None
    tax_due_count: int = None
    tax_due_amount: float = None
    tax_due_rank_num: int = None
    tax_due_rank_percent: float = None
    tax_paid_amount: float = None
    tax_paid_bool: bool = None
    tax_paid_rank_num: int = None
    tax_paid_rank_percent: float = None
    transactions_count: int = None
    transactions_magnitude: float = None
    transactions_rank_num: int = None
    transactions_rank_percent: float = None


@dataclass
class MoneyUnit:
    userhub: UserHub
