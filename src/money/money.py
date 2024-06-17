from dataclasses import dataclass


@dataclass
class GuyMoneyReport:
    tax_total: float = None
    debtor_rank_num: int = None
    credor_rank_num: int = None
    debtor_rank_percent: float = None
    credor_rank_percent: float = None
    grant_total: float = None
    tax_paid_amount: float = None
    tax_paid_bool: bool = None
    transactions_count: float = None
    transactions_magnitude: float = None
