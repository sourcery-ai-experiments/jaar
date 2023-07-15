from dataclasses import dataclass
from lib.agent.x_func import x_get_dict, return1ifnone as x_func_return1ifnone


class InvalidAllyException(Exception):
    pass


class AllyName(str):
    pass


@dataclass
class AllyRing:
    name: AllyName

    def get_dict(self):
        return {"name": self.name}


@dataclass
class AllyCore:
    name: AllyName


# class AllyRingsshop:
def allyrings_get_from_json(allyrings_json: str) -> dict[str:AllyRing]:
    allyrings_dict = x_get_dict(json_x=allyrings_json)
    return allyrings_get_from_dict(x_dict=allyrings_dict)


def allyrings_get_from_dict(x_dict: dict) -> dict[str:AllyRing]:
    allyrings = {}
    if x_dict != None:
        for allyrings_dict in x_dict.values():
            x_allyring = allyrings_get_allyring(
                name=allyrings_dict["name"],
            )
            allyrings[x_allyring.name] = x_allyring
    return allyrings


def allyrings_get_allyring(name: AllyName) -> AllyRing:
    return AllyRing(name=name)


@dataclass
class AllyUnit(AllyCore):
    uid: int = None
    creditor_weight: int = None
    debtor_weight: int = None
    external_name: str = None
    _agent_credit: float = None
    _agent_debt: float = None
    _agent_agenda_credit: float = None
    _agent_agenda_debt: float = None
    _agent_agenda_ratio_credit: float = None
    _agent_agenda_ratio_debt: float = None
    _creditor_active: bool = None
    _debtor_active: bool = None
    _allyrings: dict[AllyName:AllyRing] = None
    _bank_tax_paid: float = None
    _bank_tax_diff: float = None

    def __post_init__(self):
        if self.external_name is None:
            self.external_name = str(self.name)

    def clear_banking_data(self):
        self._bank_tax_paid = None
        self._bank_tax_diff = None

    def set_banking_data(self, tax_paid: float, tax_diff: float):
        self._bank_tax_paid = tax_paid
        self._bank_tax_diff = tax_diff
        # if tax_diff is None or self._agent_agenda_ratio_credit is None:
        #     self._bank_tax_diff = tax_diff
        # elif (
        #     round(self._bank_tax_paid - self._agent_agenda_ratio_credit, 15) == tax_diff
        # ):
        #     self._bank_tax_diff = tax_diff
        # else:
        #     raise Exception(
        #         f"AllyUnit.set_banking_data fail: tax_paid={tax_paid} + tax_diff={tax_diff} not equal to _agent_agenda_ratio_credit={self._agent_agenda_ratio_credit}"
        #     )

    def get_dict(self):
        return {
            "name": self.name,
            "uid": self.uid,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
            "_creditor_active": self._creditor_active,
            "_debtor_active": self._debtor_active,
            "_allyrings": self.get_allyrings_dict(),
            "external_name": self.external_name,
            "_bank_tax_paid": self._bank_tax_paid,
            "_bank_tax_diff": self._bank_tax_diff,
        }

    def get_allyrings_dict(self):
        x_dict = {}
        if self._allyrings != None:
            for allyring in self._allyrings.values():
                x_dict[allyring.name] = allyring.get_dict()
        return x_dict

    def get_creditor_weight(self):
        return x_func_return1ifnone(self.creditor_weight)

    def get_debtor_weight(self):
        return x_func_return1ifnone(self.debtor_weight)

    def set_empty_agent_credit_debt_to_zero(self):
        if self._agent_credit is None:
            self._agent_credit = 0
        if self._agent_debt is None:
            self._agent_debt = 0
        if self._agent_agenda_credit is None:
            self._agent_agenda_credit = 0
        if self._agent_agenda_debt is None:
            self._agent_agenda_debt = 0
        if self._agent_agenda_ratio_credit is None:
            self._agent_agenda_ratio_credit = 0
        if self._agent_agenda_ratio_debt is None:
            self._agent_agenda_ratio_debt = 0

    def reset_agent_credit_debt(self):
        self._agent_credit = 0
        self._agent_debt = 0
        self._agent_agenda_credit = 0
        self._agent_agenda_debt = 0
        self._agent_agenda_ratio_credit = 0
        self._agent_agenda_ratio_debt = 0

    def add_agent_credit_debt(
        self,
        agent_credit: float,
        agent_debt,
        agent_agenda_credit: float,
        agent_agenda_debt,
    ):
        self.set_empty_agent_credit_debt_to_zero()
        self._agent_credit += agent_credit
        self._agent_debt += agent_debt
        self._agent_agenda_credit += agent_agenda_credit
        self._agent_agenda_debt += agent_agenda_debt

    def set_agent_agenda_ratio_credit_debt(
        self,
        agent_agenda_ratio_credit_sum: float,
        agent_agenda_ratio_debt_sum: float,
        agent_allyunit_total_creditor_weight: float,
        agent_allyunit_total_debtor_weight: float,
    ):
        if agent_agenda_ratio_credit_sum == 0:
            self._agent_agenda_ratio_credit = (
                self.get_creditor_weight() / agent_allyunit_total_creditor_weight
            )
        else:
            self._agent_agenda_ratio_credit = (
                self._agent_agenda_credit / agent_agenda_ratio_credit_sum
            )

        if agent_agenda_ratio_debt_sum == 0:
            self._agent_agenda_ratio_debt = (
                self.get_debtor_weight() / agent_allyunit_total_debtor_weight
            )
        else:
            self._agent_agenda_ratio_debt = (
                self._agent_agenda_debt / agent_agenda_ratio_debt_sum
            )

    def meld(self, other_allyunit):
        if self.name != other_allyunit.name:
            raise InvalidAllyException(
                f"Meld fail AllyUnit='{self.name}' not the same as AllyUnit='{other_allyunit.name}"
            )

        self.creditor_weight += other_allyunit.creditor_weight
        self.debtor_weight += other_allyunit.debtor_weight


# class AllyUnitsshop:
def allyunits_get_from_json(allyunits_json: str) -> dict[str:AllyUnit]:
    allyunits_dict = x_get_dict(json_x=allyunits_json)
    return allyunits_get_from_dict(x_dict=allyunits_dict)


def allyunits_get_from_dict(x_dict: dict) -> dict[str:AllyUnit]:
    allyunits = {}
    for allyunits_dict in x_dict.values():
        try:
            allyrings = allyunits_dict["_allyrings"]
        except KeyError:
            allyrings = {}

        try:
            external_name = allyunits_dict["external_name"]
        except KeyError:
            external_name = {}

        try:
            _bank_tax_paid = allyunits_dict["_bank_tax_paid"]
        except KeyError:
            _bank_tax_paid = None

        try:
            _bank_tax_diff = allyunits_dict["_bank_tax_diff"]
        except KeyError:
            _bank_tax_diff = None

        x_allyunit = allyunit_shop(
            name=allyunits_dict["name"],
            uid=allyunits_dict["uid"],
            creditor_weight=allyunits_dict["creditor_weight"],
            debtor_weight=allyunits_dict["debtor_weight"],
            _creditor_active=allyunits_dict["_creditor_active"],
            _debtor_active=allyunits_dict["_debtor_active"],
            _allyrings=allyrings_get_from_dict(x_dict=allyrings),
            external_name=external_name,
            _bank_tax_paid=_bank_tax_paid,
            _bank_tax_diff=_bank_tax_diff,
        )
        allyunits[x_allyunit.name] = x_allyunit
    return allyunits


def allyunit_shop(
    name: AllyName,
    uid: int = None,
    creditor_weight: int = None,
    debtor_weight: int = None,
    _creditor_active: bool = None,
    _debtor_active: bool = None,
    _allyrings: dict[AllyName:AllyRing] = None,
    _agent_credit: float = None,
    _agent_debt: float = None,
    _agent_agenda_credit: float = None,
    _agent_agenda_debt: float = None,
    _agent_agenda_ratio_credit: float = None,
    _agent_agenda_ratio_debt: float = None,
    external_name: str = None,
    _bank_tax_paid: float = None,
    _bank_tax_diff: float = None,
) -> AllyUnit:
    final_allyrings = {} if _allyrings is None else _allyrings

    return AllyUnit(
        name=name,
        uid=uid,
        creditor_weight=x_func_return1ifnone(creditor_weight),
        debtor_weight=x_func_return1ifnone(debtor_weight),
        _creditor_active=_creditor_active,
        _debtor_active=_debtor_active,
        _agent_credit=_agent_credit,
        _agent_debt=_agent_debt,
        _agent_agenda_credit=_agent_agenda_credit,
        _agent_agenda_debt=_agent_agenda_debt,
        _agent_agenda_ratio_credit=_agent_agenda_ratio_credit,
        _agent_agenda_ratio_debt=_agent_agenda_ratio_debt,
        _allyrings=final_allyrings,
        external_name=external_name,
        _bank_tax_paid=_bank_tax_paid,
        _bank_tax_diff=_bank_tax_diff,
    )


@dataclass
class AllyLink(AllyCore):
    creditor_weight: float = 1.0
    debtor_weight: float = 1.0
    _agent_credit: float = None
    _agent_debt: float = None
    _agent_agenda_credit: float = None
    _agent_agenda_debt: float = None

    def get_dict(self):
        return {
            "name": self.name,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def set_agent_credit_debt(
        self,
        allylinks_creditor_weight_sum: float,
        allylinks_debtor_weight_sum: float,
        brand_agent_credit: float,
        brand_agent_debt: float,
        brand_agent_agenda_credit: float,
        brand_agent_agenda_debt: float,
    ):
        brand_agent_credit = x_func_return1ifnone(brand_agent_credit)
        brand_agent_debt = x_func_return1ifnone(brand_agent_debt)
        creditor_ratio = self.creditor_weight / allylinks_creditor_weight_sum
        debtor_ratio = self.debtor_weight / allylinks_debtor_weight_sum

        self._agent_credit = brand_agent_credit * creditor_ratio
        self._agent_debt = brand_agent_debt * debtor_ratio
        self._agent_agenda_credit = brand_agent_agenda_credit * creditor_ratio
        self._agent_agenda_debt = brand_agent_agenda_debt * debtor_ratio

    def reset_agent_credit_debt(self):
        self._agent_credit = 0
        self._agent_debt = 0
        self._agent_agenda_credit = 0
        self._agent_agenda_debt = 0

    def meld(self, other_allylink):
        if self.name != other_allylink.name:
            raise InvalidAllyException(
                f"Meld fail AllyLink='{self.name}' not the same as AllyLink='{other_allylink.name}"
            )
        self.creditor_weight += other_allylink.creditor_weight
        self.debtor_weight += other_allylink.debtor_weight


# class AllyLinkshop:
def allylinks_get_from_json(allylinks_json: str) -> dict[str:AllyLink]:
    allylinks_dict = x_get_dict(json_x=allylinks_json)
    return allylinks_get_from_dict(x_dict=allylinks_dict)


def allylinks_get_from_dict(x_dict: dict) -> dict[str:AllyLink]:
    allylinks = {}
    for allylinks_dict in x_dict.values():
        x_ally = allylink_shop(
            name=allylinks_dict["name"],
            creditor_weight=allylinks_dict["creditor_weight"],
            debtor_weight=allylinks_dict["debtor_weight"],
        )
        allylinks[x_ally.name] = x_ally
    return allylinks


def allylink_shop(
    name: AllyName,
    creditor_weight: float = None,
    debtor_weight: float = None,
    _agent_credit: float = None,
    _agent_debt: float = None,
    _agent_agenda_credit: float = None,
    _agent_agenda_debt: float = None,
) -> AllyLink:
    creditor_weight = x_func_return1ifnone(creditor_weight)
    debtor_weight = x_func_return1ifnone(debtor_weight)
    return AllyLink(
        name=name,
        creditor_weight=creditor_weight,
        debtor_weight=debtor_weight,
        _agent_credit=_agent_credit,
        _agent_debt=_agent_debt,
        _agent_agenda_credit=_agent_agenda_credit,
        _agent_agenda_debt=_agent_agenda_debt,
    )


@dataclass
class AllyUnitExternalMetrics:
    external_name: str = None
    internal_name: AllyName = None
    creditor_active: bool = None
    debtor_active: bool = None
