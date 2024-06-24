from src._instrument.file import save_file
from src._instrument.python import (
    get_empty_dict_if_none,
    get_positive_int,
    get_0_if_None,
    place_obj_in_dict,
)
from src._road.jaar_config import get_json_filename
from src._road.finance import allot_scale
from src._road.road import OtherID, OwnerID
from src.money.rivercycle import (
    RiverGrade,
    rivergrade_shop,
    create_init_rivercycle,
    create_next_rivercycle,
)
from src.listen.userhub import UserHub
from dataclasses import dataclass


@dataclass
class RiverRun:
    userhub: UserHub = None
    number: int = None
    econ_credorledgers: dict[OwnerID : dict[OtherID:float]] = None
    tax_dues: dict[OtherID:float] = None
    cycle_max: int = None
    # calculated fields
    _grants: dict[OtherID:float] = None
    _tax_yields: dict[OtherID:float] = None
    _tax_got_prev: float = None
    _tax_got_curr: float = None
    _cycle_count: int = None
    _cycle_payees_prev: set = None
    _cycle_payees_curr: set = None
    _debtor_count: int = None
    _credor_count: int = None
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

    def levy_tax_dues(self, cycleledger: tuple[dict[OtherID:float], float]):
        delete_from_cycleledger = []
        tax_got_total = 0
        for payee, payee_amount in cycleledger.items():
            if self.other_has_tax_due(payee):
                excess_payer_money, tax_got = self.levy_tax_due(payee, payee_amount)
                tax_got_total += tax_got
                if excess_payer_money == 0:
                    delete_from_cycleledger.append(payee)
                else:
                    cycleledger[payee] = excess_payer_money

        for payee_to_delete in delete_from_cycleledger:
            cycleledger.pop(payee_to_delete)
        return cycleledger, tax_got_total

    def set_other_tax_due(self, x_other_id: OtherID, tax_due: float):
        self.tax_dues[x_other_id] = tax_due

    def tax_dues_unpaid(self) -> bool:
        return len(self.tax_dues) != 0

    def set_tax_dues(self, debtorledger: dict[OtherID:float]):
        x_amount = self.userhub.econ_money_magnitude
        self.tax_dues = allot_scale(debtorledger, x_amount, self.userhub.penny)

    def other_has_tax_due(self, x_other_id: OtherID) -> bool:
        return self.tax_dues.get(x_other_id) != None

    def get_other_tax_due(self, x_other_id: OtherID) -> float:
        x_tax_due = self.tax_dues.get(x_other_id)
        return 0 if x_tax_due is None else x_tax_due

    def delete_tax_due(self, x_other_id: OtherID):
        self.tax_dues.pop(x_other_id)

    def levy_tax_due(self, x_other_id: OtherID, payer_money: float) -> float:
        if self.other_has_tax_due(x_other_id) == False:
            return payer_money, 0
        x_tax_due = self.get_other_tax_due(x_other_id)
        if x_tax_due > payer_money:
            left_over_pay = x_tax_due - payer_money
            self.set_other_tax_due(x_other_id, left_over_pay)
            self.add_other_tax_yield(x_other_id, payer_money)
            return 0, payer_money
        else:
            self.delete_tax_due(x_other_id)
            self.add_other_tax_yield(x_other_id, x_tax_due)
            return payer_money - x_tax_due, x_tax_due

    def get_ledger_dict(self) -> dict[OtherID:float]:
        return self.tax_dues

    def set_other_tax_yield(self, x_other_id: OtherID, tax_yield: float):
        self._tax_yields[x_other_id] = tax_yield

    def tax_yields_is_empty(self) -> bool:
        return len(self._tax_yields) == 0

    def reset_tax_yields(self):
        self._tax_yields = {}

    def other_has_tax_yield(self, x_other_id: OtherID) -> bool:
        return self._tax_yields.get(x_other_id) != None

    def get_other_tax_yield(self, x_other_id: OtherID) -> float:
        x_tax_yield = self._tax_yields.get(x_other_id)
        return 0 if x_tax_yield is None else x_tax_yield

    def delete_tax_yield(self, x_other_id: OtherID):
        self._tax_yields.pop(x_other_id)

    def add_other_tax_yield(self, x_other_id: OtherID, x_tax_yield: float):
        if self.other_has_tax_yield(x_other_id):
            x_tax_yield = self.get_other_tax_yield(x_other_id) + x_tax_yield
        self.set_other_tax_yield(x_other_id, x_tax_yield)

    def get_rivergrade(self, other_id: OtherID) -> RiverGrade:
        return self._rivergrades.get(other_id)

    def _rivergrades_is_empty(self) -> bool:
        return self._rivergrades == {}

    def rivergrade_exists(self, other_id: OtherID) -> bool:
        return self._rivergrades.get(other_id) != None

    def _get_other_grant(self, other_id: OtherID) -> float:
        return get_0_if_None(self._grants.get(other_id))

    def set_initial_rivergrade(self, other_id: OtherID):
        x_rivergrade = rivergrade_shop(self.userhub, other_id, self.number)
        x_rivergrade.debtor_count = self._debtor_count
        x_rivergrade.credor_count = self._credor_count
        x_rivergrade.grant_amount = self._get_other_grant(other_id)
        self._rivergrades[other_id] = x_rivergrade

    def set_all_initial_rivergrades(self):
        self._rivergrades = {}
        all_other_ids = self.get_all_econ_credorledger_other_ids()
        for other_id in all_other_ids:
            self.set_initial_rivergrade(other_id)

    def _set_post_loop_rivergrade_attrs(self):
        for x_other_id, other_rivergrade in self._rivergrades.items():
            tax_due_remaining = self.get_other_tax_due(x_other_id)
            tax_due_paid = self.get_other_tax_yield(x_other_id)
            other_rivergrade.set_tax_bill_amount(tax_due_paid + tax_due_remaining)
            other_rivergrade.set_tax_paid_amount(tax_due_paid)

    def calc_metrics(self):
        self._set_debtor_count_credor_count()
        self._set_grants()
        self.set_all_initial_rivergrades()

        self._cycle_count = 0
        x_rivercyle = create_init_rivercycle(self.userhub, self.econ_credorledgers)
        x_cyclelegder = x_rivercyle.create_cylceledger()
        self._cycle_payees_curr = set(x_cyclelegder.keys())
        x_cyclelegder, tax_got_curr = self.levy_tax_dues(x_cyclelegder)
        self._set_tax_got_attrs(tax_got_curr)

        while self.cycle_max > self._cycle_count and self.cycles_vary():
            x_rivercyle = create_next_rivercycle(x_rivercyle, x_cyclelegder)
            x_cyclelegder, tax_got_curr = self.levy_tax_dues(x_cyclelegder)

            self._set_tax_got_attrs(tax_got_curr)
            print(f"{self._tax_got_curr=} {self._tax_got_prev=}")
            self._cycle_payees_prev = self._cycle_payees_curr
            self._cycle_payees_curr = set(x_cyclelegder.keys())
            self._cycle_count += 1

        self._set_post_loop_rivergrade_attrs()

    def _set_debtor_count_credor_count(self):
        tax_dues_others = set(self.tax_dues.keys())
        tax_yields_others = set(self._tax_yields.keys())
        self._debtor_count = len(tax_dues_others.union(tax_yields_others))
        self._credor_count = len(self.econ_credorledgers.get(self.userhub.person_id))

    def _set_grants(self):
        grant_credorledger = self.econ_credorledgers.get(self.userhub.person_id)
        self._grants = allot_scale(
            ledger=grant_credorledger,
            scale_number=self.userhub.econ_money_magnitude,
            grain_unit=self.userhub.penny,
        )

    def _save_rivergrade_file(self, other_id: OtherID):
        rivergrade = self.get_rivergrade(other_id)
        grade_path = self.userhub.grade_path(other_id)
        grade_filename = get_json_filename(other_id)
        save_file(grade_path, grade_filename, rivergrade.get_json())

    def save_rivergrade_files(self):
        for rivergrade_other in self._rivergrades.keys():
            self._save_rivergrade_file(rivergrade_other)

    def _cycle_payees_vary(self) -> bool:
        return self._cycle_payees_prev != self._cycle_payees_curr

    def _set_tax_got_attrs(self, x_tax_got_curr: float):
        self._tax_got_prev = self._tax_got_curr
        self._tax_got_curr = x_tax_got_curr

    def _tax_gotten(self) -> bool:
        return max(self._tax_got_prev, self._tax_got_curr) > 0

    def cycles_vary(self) -> bool:
        return self._tax_gotten() or self._cycle_payees_vary()


def riverrun_shop(
    userhub: UserHub,
    number: int = None,
    econ_credorledgers: dict[OwnerID : dict[OtherID:float]] = None,
    tax_dues: dict[OtherID:float] = None,
    cycle_max: int = None,
):
    x_riverun = RiverRun(
        userhub=userhub,
        number=get_0_if_None(number),
        econ_credorledgers=get_empty_dict_if_none(econ_credorledgers),
        tax_dues=get_empty_dict_if_none(tax_dues),
        _rivergrades={},
        _grants={},
        _tax_yields={},
    )
    x_riverun._cycle_count = 0
    x_riverun._cycle_payees_prev = set()
    x_riverun._cycle_payees_curr = set()
    x_riverun._tax_got_prev = 0
    x_riverun._tax_got_curr = 0
    if cycle_max is None:
        cycle_max = 10
    x_riverun.set_cycle_max(cycle_max)
    return x_riverun
