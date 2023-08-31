from dataclasses import dataclass
from src.calendar.x_func import x_get_dict, return1ifnone as x_func_return1ifnone


class InvalidMemberException(Exception):
    pass


class MemberName(str):
    pass


@dataclass
class MemberRing:
    name: MemberName

    def get_dict(self):
        return {"name": self.name}


@dataclass
class MemberCore:
    name: MemberName


# class MemberRingsshop:
def memberrings_get_from_json(memberrings_json: str) -> dict[str:MemberRing]:
    memberrings_dict = x_get_dict(json_x=memberrings_json)
    return memberrings_get_from_dict(x_dict=memberrings_dict)


def memberrings_get_from_dict(x_dict: dict) -> dict[str:MemberRing]:
    memberrings = {}
    if x_dict != None:
        for memberrings_dict in x_dict.values():
            x_memberring = memberrings_get_memberring(
                name=memberrings_dict["name"],
            )
            memberrings[x_memberring.name] = x_memberring
    return memberrings


def memberrings_get_memberring(name: MemberName) -> MemberRing:
    return MemberRing(name=name)


@dataclass
class MemberUnit(MemberCore):
    uid: int = None
    creditor_weight: int = None
    debtor_weight: int = None
    _calendar_credit: float = None
    _calendar_debt: float = None
    _calendar_agenda_credit: float = None
    _calendar_agenda_debt: float = None
    _calendar_agenda_ratio_credit: float = None
    _calendar_agenda_ratio_debt: float = None
    _creditor_active: bool = None
    _debtor_active: bool = None
    _memberrings: dict[MemberName:MemberRing] = None
    _bank_tax_paid: float = None
    _bank_tax_diff: float = None

    def clear_banking_data(self):
        self._bank_tax_paid = None
        self._bank_tax_diff = None

    def set_banking_data(self, tax_paid: float, tax_diff: float):
        self._bank_tax_paid = tax_paid
        self._bank_tax_diff = tax_diff
        # if tax_diff is None or self._calendar_agenda_ratio_credit is None:
        #     self._bank_tax_diff = tax_diff
        # elif (
        #     round(self._bank_tax_paid - self._calendar_agenda_ratio_credit, 15) == tax_diff
        # ):
        #     self._bank_tax_diff = tax_diff
        # else:
        #     raise Exception(
        #         f"MemberUnit.set_banking_data fail: tax_paid={tax_paid} + tax_diff={tax_diff} not equal to _calendar_agenda_ratio_credit={self._calendar_agenda_ratio_credit}"
        #     )

    def get_dict(self):
        return {
            "name": self.name,
            "uid": self.uid,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
            "_creditor_active": self._creditor_active,
            "_debtor_active": self._debtor_active,
            "_memberrings": self.get_memberrings_dict(),
            "_bank_tax_paid": self._bank_tax_paid,
            "_bank_tax_diff": self._bank_tax_diff,
        }

    def get_memberrings_dict(self):
        x_dict = {}
        if self._memberrings != None:
            for memberring in self._memberrings.values():
                x_dict[memberring.name] = memberring.get_dict()
        return x_dict

    def get_creditor_weight(self):
        return x_func_return1ifnone(self.creditor_weight)

    def get_debtor_weight(self):
        return x_func_return1ifnone(self.debtor_weight)

    def set_empty_calendar_credit_debt_to_zero(self):
        if self._calendar_credit is None:
            self._calendar_credit = 0
        if self._calendar_debt is None:
            self._calendar_debt = 0
        if self._calendar_agenda_credit is None:
            self._calendar_agenda_credit = 0
        if self._calendar_agenda_debt is None:
            self._calendar_agenda_debt = 0
        if self._calendar_agenda_ratio_credit is None:
            self._calendar_agenda_ratio_credit = 0
        if self._calendar_agenda_ratio_debt is None:
            self._calendar_agenda_ratio_debt = 0

    def reset_calendar_credit_debt(self):
        self._calendar_credit = 0
        self._calendar_debt = 0
        self._calendar_agenda_credit = 0
        self._calendar_agenda_debt = 0
        self._calendar_agenda_ratio_credit = 0
        self._calendar_agenda_ratio_debt = 0

    def add_calendar_credit_debt(
        self,
        calendar_credit: float,
        calendar_debt,
        calendar_agenda_credit: float,
        calendar_agenda_debt,
    ):
        self.set_empty_calendar_credit_debt_to_zero()
        self._calendar_credit += calendar_credit
        self._calendar_debt += calendar_debt
        self._calendar_agenda_credit += calendar_agenda_credit
        self._calendar_agenda_debt += calendar_agenda_debt

    def set_calendar_agenda_ratio_credit_debt(
        self,
        calendar_agenda_ratio_credit_sum: float,
        calendar_agenda_ratio_debt_sum: float,
        calendar_memberunit_total_creditor_weight: float,
        calendar_memberunit_total_debtor_weight: float,
    ):
        if calendar_agenda_ratio_credit_sum == 0:
            self._calendar_agenda_ratio_credit = (
                self.get_creditor_weight() / calendar_memberunit_total_creditor_weight
            )
        else:
            self._calendar_agenda_ratio_credit = (
                self._calendar_agenda_credit / calendar_agenda_ratio_credit_sum
            )

        if calendar_agenda_ratio_debt_sum == 0:
            self._calendar_agenda_ratio_debt = (
                self.get_debtor_weight() / calendar_memberunit_total_debtor_weight
            )
        else:
            self._calendar_agenda_ratio_debt = (
                self._calendar_agenda_debt / calendar_agenda_ratio_debt_sum
            )

    def meld(self, other_memberunit):
        if self.name != other_memberunit.name:
            raise InvalidMemberException(
                f"Meld fail MemberUnit='{self.name}' not the same as MemberUnit='{other_memberunit.name}"
            )

        self.creditor_weight += other_memberunit.creditor_weight
        self.debtor_weight += other_memberunit.debtor_weight


# class MemberUnitsshop:
def memberunits_get_from_json(memberunits_json: str) -> dict[str:MemberUnit]:
    memberunits_dict = x_get_dict(json_x=memberunits_json)
    return memberunits_get_from_dict(x_dict=memberunits_dict)


def memberunits_get_from_dict(x_dict: dict) -> dict[str:MemberUnit]:
    memberunits = {}
    for memberunits_dict in x_dict.values():
        try:
            memberrings = memberunits_dict["_memberrings"]
        except KeyError:
            memberrings = {}

        try:
            _bank_tax_paid = memberunits_dict["_bank_tax_paid"]
        except KeyError:
            _bank_tax_paid = None

        try:
            _bank_tax_diff = memberunits_dict["_bank_tax_diff"]
        except KeyError:
            _bank_tax_diff = None

        x_memberunit = memberunit_shop(
            name=memberunits_dict["name"],
            uid=memberunits_dict["uid"],
            creditor_weight=memberunits_dict["creditor_weight"],
            debtor_weight=memberunits_dict["debtor_weight"],
            _creditor_active=memberunits_dict["_creditor_active"],
            _debtor_active=memberunits_dict["_debtor_active"],
            _memberrings=memberrings_get_from_dict(x_dict=memberrings),
            _bank_tax_paid=_bank_tax_paid,
            _bank_tax_diff=_bank_tax_diff,
        )
        memberunits[x_memberunit.name] = x_memberunit
    return memberunits


def memberunit_shop(
    name: MemberName,
    uid: int = None,
    creditor_weight: int = None,
    debtor_weight: int = None,
    _creditor_active: bool = None,
    _debtor_active: bool = None,
    _memberrings: dict[MemberName:MemberRing] = None,
    _calendar_credit: float = None,
    _calendar_debt: float = None,
    _calendar_agenda_credit: float = None,
    _calendar_agenda_debt: float = None,
    _calendar_agenda_ratio_credit: float = None,
    _calendar_agenda_ratio_debt: float = None,
    _bank_tax_paid: float = None,
    _bank_tax_diff: float = None,
) -> MemberUnit:
    final_memberrings = {} if _memberrings is None else _memberrings

    return MemberUnit(
        name=name,
        uid=uid,
        creditor_weight=x_func_return1ifnone(creditor_weight),
        debtor_weight=x_func_return1ifnone(debtor_weight),
        _creditor_active=_creditor_active,
        _debtor_active=_debtor_active,
        _calendar_credit=_calendar_credit,
        _calendar_debt=_calendar_debt,
        _calendar_agenda_credit=_calendar_agenda_credit,
        _calendar_agenda_debt=_calendar_agenda_debt,
        _calendar_agenda_ratio_credit=_calendar_agenda_ratio_credit,
        _calendar_agenda_ratio_debt=_calendar_agenda_ratio_debt,
        _memberrings=final_memberrings,
        _bank_tax_paid=_bank_tax_paid,
        _bank_tax_diff=_bank_tax_diff,
    )


@dataclass
class MemberLink(MemberCore):
    creditor_weight: float = 1.0
    debtor_weight: float = 1.0
    _calendar_credit: float = None
    _calendar_debt: float = None
    _calendar_agenda_credit: float = None
    _calendar_agenda_debt: float = None

    def get_dict(self):
        return {
            "name": self.name,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def set_calendar_credit_debt(
        self,
        memberlinks_creditor_weight_sum: float,
        memberlinks_debtor_weight_sum: float,
        group_calendar_credit: float,
        group_calendar_debt: float,
        group_calendar_agenda_credit: float,
        group_calendar_agenda_debt: float,
    ):
        group_calendar_credit = x_func_return1ifnone(group_calendar_credit)
        group_calendar_debt = x_func_return1ifnone(group_calendar_debt)
        creditor_ratio = self.creditor_weight / memberlinks_creditor_weight_sum
        debtor_ratio = self.debtor_weight / memberlinks_debtor_weight_sum

        self._calendar_credit = group_calendar_credit * creditor_ratio
        self._calendar_debt = group_calendar_debt * debtor_ratio
        self._calendar_agenda_credit = group_calendar_agenda_credit * creditor_ratio
        self._calendar_agenda_debt = group_calendar_agenda_debt * debtor_ratio

    def reset_calendar_credit_debt(self):
        self._calendar_credit = 0
        self._calendar_debt = 0
        self._calendar_agenda_credit = 0
        self._calendar_agenda_debt = 0

    def meld(self, other_memberlink):
        if self.name != other_memberlink.name:
            raise InvalidMemberException(
                f"Meld fail MemberLink='{self.name}' not the same as MemberLink='{other_memberlink.name}"
            )
        self.creditor_weight += other_memberlink.creditor_weight
        self.debtor_weight += other_memberlink.debtor_weight


# class MemberLinkshop:
def memberlinks_get_from_json(memberlinks_json: str) -> dict[str:MemberLink]:
    memberlinks_dict = x_get_dict(json_x=memberlinks_json)
    return memberlinks_get_from_dict(x_dict=memberlinks_dict)


def memberlinks_get_from_dict(x_dict: dict) -> dict[str:MemberLink]:
    memberlinks = {}
    for memberlinks_dict in x_dict.values():
        x_member = memberlink_shop(
            name=memberlinks_dict["name"],
            creditor_weight=memberlinks_dict["creditor_weight"],
            debtor_weight=memberlinks_dict["debtor_weight"],
        )
        memberlinks[x_member.name] = x_member
    return memberlinks


def memberlink_shop(
    name: MemberName,
    creditor_weight: float = None,
    debtor_weight: float = None,
    _calendar_credit: float = None,
    _calendar_debt: float = None,
    _calendar_agenda_credit: float = None,
    _calendar_agenda_debt: float = None,
) -> MemberLink:
    creditor_weight = x_func_return1ifnone(creditor_weight)
    debtor_weight = x_func_return1ifnone(debtor_weight)
    return MemberLink(
        name=name,
        creditor_weight=creditor_weight,
        debtor_weight=debtor_weight,
        _calendar_credit=_calendar_credit,
        _calendar_debt=_calendar_debt,
        _calendar_agenda_credit=_calendar_agenda_credit,
        _calendar_agenda_debt=_calendar_agenda_debt,
    )


@dataclass
class MemberUnitExternalMetrics:
    internal_name: MemberName = None
    creditor_active: bool = None
    debtor_active: bool = None
