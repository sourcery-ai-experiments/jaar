from dataclasses import dataclass
from src.oath.x_func import x_get_dict, return1ifnone as x_func_return1ifnone


class InvalidPartyException(Exception):
    pass


class InvalidDepotLinkException(Exception):
    pass


class PartyTitle(str):
    pass


@dataclass
class PartyRing:
    title: PartyTitle

    def get_dict(self):
        return {"title": self.title}


@dataclass
class PartyCore:
    title: PartyTitle


# class PartyRingsshop:
def partyrings_get_from_json(partyrings_json: str) -> dict[str:PartyRing]:
    partyrings_dict = x_get_dict(json_x=partyrings_json)
    return partyrings_get_from_dict(x_dict=partyrings_dict)


def partyrings_get_from_dict(x_dict: dict) -> dict[str:PartyRing]:
    partyrings = {}
    if x_dict != None:
        for partyrings_dict in x_dict.values():
            x_partyring = partyrings_get_partyring(
                title=partyrings_dict["title"],
            )
            partyrings[x_partyring.title] = x_partyring
    return partyrings


def partyrings_get_partyring(title: PartyTitle) -> PartyRing:
    return PartyRing(title=title)


@dataclass
class PartyUnit(PartyCore):
    uid: int = None
    creditor_weight: int = None
    debtor_weight: int = None
    depotlink_type: str = None
    _oath_credit: float = None
    _oath_debt: float = None
    _oath_agenda_credit: float = None
    _oath_agenda_debt: float = None
    _oath_agenda_ratio_credit: float = None
    _oath_agenda_ratio_debt: float = None
    _creditor_active: bool = None
    _debtor_active: bool = None
    _partyrings: dict[PartyTitle:PartyRing] = None
    _bank_tax_paid: float = None
    _bank_tax_diff: float = None

    def set_depotlink_type(
        self,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        if depotlink_type not in (list(get_depotlink_types())):
            raise InvalidDepotLinkException(
                f"PartyUnit '{self.title}' cannot have type '{depotlink_type}'."
            )
        self.depotlink_type = depotlink_type
        if creditor_weight != None:
            self.creditor_weight = creditor_weight
        if debtor_weight != None:
            self.debtor_weight = debtor_weight

    def del_depotlink_type(self):
        self.depotlink_type = None

    def clear_banking_data(self):
        self._bank_tax_paid = None
        self._bank_tax_diff = None

    def set_banking_data(self, tax_paid: float, tax_diff: float):
        self._bank_tax_paid = tax_paid
        self._bank_tax_diff = tax_diff
        # if tax_diff is None or self._oath_agenda_ratio_credit is None:
        #     self._bank_tax_diff = tax_diff
        # elif (
        #     round(self._bank_tax_paid - self._oath_agenda_ratio_credit, 15) == tax_diff
        # ):
        #     self._bank_tax_diff = tax_diff
        # else:
        #     raise Exception(
        #         f"PartyUnit.set_banking_data fail: tax_paid={tax_paid} + tax_diff={tax_diff} not equal to _oath_agenda_ratio_credit={self._oath_agenda_ratio_credit}"
        #     )

    def get_dict(self):
        return {
            "title": self.title,
            "uid": self.uid,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
            "_creditor_active": self._creditor_active,
            "_debtor_active": self._debtor_active,
            "_partyrings": self.get_partyrings_dict(),
            "_bank_tax_paid": self._bank_tax_paid,
            "_bank_tax_diff": self._bank_tax_diff,
            "depotlink_type": self.depotlink_type,
        }

    def get_partyrings_dict(self):
        x_dict = {}
        if self._partyrings != None:
            for partyring in self._partyrings.values():
                x_dict[partyring.title] = partyring.get_dict()
        return x_dict

    def get_creditor_weight(self):
        return x_func_return1ifnone(self.creditor_weight)

    def get_debtor_weight(self):
        return x_func_return1ifnone(self.debtor_weight)

    def set_empty_oath_credit_debt_to_zero(self):
        if self._oath_credit is None:
            self._oath_credit = 0
        if self._oath_debt is None:
            self._oath_debt = 0
        if self._oath_agenda_credit is None:
            self._oath_agenda_credit = 0
        if self._oath_agenda_debt is None:
            self._oath_agenda_debt = 0
        if self._oath_agenda_ratio_credit is None:
            self._oath_agenda_ratio_credit = 0
        if self._oath_agenda_ratio_debt is None:
            self._oath_agenda_ratio_debt = 0

    def reset_oath_credit_debt(self):
        self._oath_credit = 0
        self._oath_debt = 0
        self._oath_agenda_credit = 0
        self._oath_agenda_debt = 0
        self._oath_agenda_ratio_credit = 0
        self._oath_agenda_ratio_debt = 0

    def add_oath_credit_debt(
        self,
        oath_credit: float,
        oath_debt,
        oath_agenda_credit: float,
        oath_agenda_debt,
    ):
        self.set_empty_oath_credit_debt_to_zero()
        self._oath_credit += oath_credit
        self._oath_debt += oath_debt
        self._oath_agenda_credit += oath_agenda_credit
        self._oath_agenda_debt += oath_agenda_debt

    def set_oath_agenda_ratio_credit_debt(
        self,
        oath_agenda_ratio_credit_sum: float,
        oath_agenda_ratio_debt_sum: float,
        oath_partyunit_total_creditor_weight: float,
        oath_partyunit_total_debtor_weight: float,
    ):
        if oath_agenda_ratio_credit_sum == 0:
            self._oath_agenda_ratio_credit = (
                self.get_creditor_weight() / oath_partyunit_total_creditor_weight
            )
        else:
            self._oath_agenda_ratio_credit = (
                self._oath_agenda_credit / oath_agenda_ratio_credit_sum
            )

        if oath_agenda_ratio_debt_sum == 0:
            self._oath_agenda_ratio_debt = (
                self.get_debtor_weight() / oath_partyunit_total_debtor_weight
            )
        else:
            self._oath_agenda_ratio_debt = (
                self._oath_agenda_debt / oath_agenda_ratio_debt_sum
            )

    def meld(self, other_partyunit):
        if self.title != other_partyunit.title:
            raise InvalidPartyException(
                f"Meld fail PartyUnit='{self.title}' not the same as PartyUnit='{other_partyunit.title}"
            )

        self.creditor_weight += other_partyunit.creditor_weight
        self.debtor_weight += other_partyunit.debtor_weight


# class PartyUnitsshop:
def partyunits_get_from_json(partyunits_json: str) -> dict[str:PartyUnit]:
    partyunits_dict = x_get_dict(json_x=partyunits_json)
    return partyunits_get_from_dict(x_dict=partyunits_dict)


def partyunits_get_from_dict(x_dict: dict) -> dict[str:PartyUnit]:
    partyunits = {}
    for partyunits_dict in x_dict.values():
        try:
            partyrings = partyunits_dict["_partyrings"]
        except KeyError:
            partyrings = {}

        try:
            _bank_tax_paid = partyunits_dict["_bank_tax_paid"]
        except KeyError:
            _bank_tax_paid = None

        try:
            _bank_tax_diff = partyunits_dict["_bank_tax_diff"]
        except KeyError:
            _bank_tax_diff = None

        try:
            depotlink_type = partyunits_dict["depotlink_type"]
        except KeyError:
            depotlink_type = None

        x_partyunit = partyunit_shop(
            title=partyunits_dict["title"],
            uid=partyunits_dict["uid"],
            creditor_weight=partyunits_dict["creditor_weight"],
            debtor_weight=partyunits_dict["debtor_weight"],
            _creditor_active=partyunits_dict["_creditor_active"],
            _debtor_active=partyunits_dict["_debtor_active"],
            _partyrings=partyrings_get_from_dict(x_dict=partyrings),
            _bank_tax_paid=_bank_tax_paid,
            _bank_tax_diff=_bank_tax_diff,
            depotlink_type=depotlink_type,
        )
        partyunits[x_partyunit.title] = x_partyunit
    return partyunits


def partyunit_shop(
    title: PartyTitle,
    uid: int = None,
    creditor_weight: int = None,
    debtor_weight: int = None,
    _creditor_active: bool = None,
    _debtor_active: bool = None,
    _partyrings: dict[PartyTitle:PartyRing] = None,
    _oath_credit: float = None,
    _oath_debt: float = None,
    _oath_agenda_credit: float = None,
    _oath_agenda_debt: float = None,
    _oath_agenda_ratio_credit: float = None,
    _oath_agenda_ratio_debt: float = None,
    _bank_tax_paid: float = None,
    _bank_tax_diff: float = None,
    depotlink_type: str = None,
) -> PartyUnit:
    final_partyrings = {} if _partyrings is None else _partyrings

    partyunit_x = PartyUnit(
        title=title,
        uid=uid,
        creditor_weight=x_func_return1ifnone(creditor_weight),
        debtor_weight=x_func_return1ifnone(debtor_weight),
        _creditor_active=_creditor_active,
        _debtor_active=_debtor_active,
        _oath_credit=_oath_credit,
        _oath_debt=_oath_debt,
        _oath_agenda_credit=_oath_agenda_credit,
        _oath_agenda_debt=_oath_agenda_debt,
        _oath_agenda_ratio_credit=_oath_agenda_ratio_credit,
        _oath_agenda_ratio_debt=_oath_agenda_ratio_debt,
        _partyrings=final_partyrings,
        _bank_tax_paid=_bank_tax_paid,
        _bank_tax_diff=_bank_tax_diff,
    )
    if depotlink_type != None:
        partyunit_x.set_depotlink_type(depotlink_type=depotlink_type)
    return partyunit_x


@dataclass
class PartyLink(PartyCore):
    creditor_weight: float = 1.0
    debtor_weight: float = 1.0
    _oath_credit: float = None
    _oath_debt: float = None
    _oath_agenda_credit: float = None
    _oath_agenda_debt: float = None

    def get_dict(self):
        return {
            "title": self.title,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def set_oath_credit_debt(
        self,
        partylinks_creditor_weight_sum: float,
        partylinks_debtor_weight_sum: float,
        group_oath_credit: float,
        group_oath_debt: float,
        group_oath_agenda_credit: float,
        group_oath_agenda_debt: float,
    ):
        group_oath_credit = x_func_return1ifnone(group_oath_credit)
        group_oath_debt = x_func_return1ifnone(group_oath_debt)
        creditor_ratio = self.creditor_weight / partylinks_creditor_weight_sum
        debtor_ratio = self.debtor_weight / partylinks_debtor_weight_sum

        self._oath_credit = group_oath_credit * creditor_ratio
        self._oath_debt = group_oath_debt * debtor_ratio
        self._oath_agenda_credit = group_oath_agenda_credit * creditor_ratio
        self._oath_agenda_debt = group_oath_agenda_debt * debtor_ratio

    def reset_oath_credit_debt(self):
        self._oath_credit = 0
        self._oath_debt = 0
        self._oath_agenda_credit = 0
        self._oath_agenda_debt = 0

    def meld(self, other_partylink):
        if self.title != other_partylink.title:
            raise InvalidPartyException(
                f"Meld fail PartyLink='{self.title}' not the same as PartyLink='{other_partylink.title}"
            )
        self.creditor_weight += other_partylink.creditor_weight
        self.debtor_weight += other_partylink.debtor_weight


# class PartyLinkshop:
def partylinks_get_from_json(partylinks_json: str) -> dict[str:PartyLink]:
    partylinks_dict = x_get_dict(json_x=partylinks_json)
    return partylinks_get_from_dict(x_dict=partylinks_dict)


def partylinks_get_from_dict(x_dict: dict) -> dict[str:PartyLink]:
    partylinks = {}
    for partylinks_dict in x_dict.values():
        x_party = partylink_shop(
            title=partylinks_dict["title"],
            creditor_weight=partylinks_dict["creditor_weight"],
            debtor_weight=partylinks_dict["debtor_weight"],
        )
        partylinks[x_party.title] = x_party
    return partylinks


def partylink_shop(
    title: PartyTitle,
    creditor_weight: float = None,
    debtor_weight: float = None,
    _oath_credit: float = None,
    _oath_debt: float = None,
    _oath_agenda_credit: float = None,
    _oath_agenda_debt: float = None,
) -> PartyLink:
    creditor_weight = x_func_return1ifnone(creditor_weight)
    debtor_weight = x_func_return1ifnone(debtor_weight)
    return PartyLink(
        title=title,
        creditor_weight=creditor_weight,
        debtor_weight=debtor_weight,
        _oath_credit=_oath_credit,
        _oath_debt=_oath_debt,
        _oath_agenda_credit=_oath_agenda_credit,
        _oath_agenda_debt=_oath_agenda_debt,
    )


@dataclass
class PartyUnitExternalMetrics:
    internal_title: PartyTitle = None
    creditor_active: bool = None
    debtor_active: bool = None


def get_depotlink_types() -> dict[str:None]:
    return {"blind_trust": None, "ignore": None, "assignment": None}
