import dataclasses
from src.deal.party import (
    PartyTitle,
    PartyUnit,
    PartyLink,
    partylinks_get_from_dict,
)
from src.deal.x_func import (
    x_get_dict,
    get_meld_weight,
    return1ifnone as x_func_return1ifnone,
)
from src.deal.road import Road


class InvalidGroupException(Exception):
    pass


class GroupBrand(str):
    pass


@dataclasses.dataclass
class GroupCore:
    brand: GroupBrand


@dataclasses.dataclass
class GroupUnit(GroupCore):
    uid: int = None
    single_party_id: int = None
    _single_party: bool = None
    _partys: dict[PartyTitle:PartyLink] = None
    _deal_credit: float = None
    _deal_debt: float = None
    _deal_agenda_credit: float = None
    _deal_agenda_debt: float = None
    _partylinks_set_by_cure_road: Road = None

    def set_brand(self, brand: GroupBrand = None):
        if brand != None:
            self.brand = brand

    def set_attr(self, _partylinks_set_by_cure_road: Road):
        if _partylinks_set_by_cure_road != None:
            self._partylinks_set_by_cure_road = _partylinks_set_by_cure_road

    def get_dict(self):
        return {
            "brand": self.brand,
            "uid": self.uid,
            "single_party_id": self.single_party_id,
            "_single_party": self._single_party,
            "_partys": self.get_partys_dict(),
            "_partylinks_set_by_cure_road": self._partylinks_set_by_cure_road,
        }

    def set_empty_deal_credit_debt_to_zero(self):
        if self._deal_credit is None:
            self._deal_credit = 0
        if self._deal_debt is None:
            self._deal_debt = 0
        if self._deal_agenda_credit is None:
            self._deal_agenda_credit = 0
        if self._deal_agenda_debt is None:
            self._deal_agenda_debt = 0

    def reset_deal_credit_debt(self):
        self._deal_credit = 0
        self._deal_debt = 0
        self._deal_agenda_credit = 0
        self._deal_agenda_debt = 0
        self._set_partylinks_empty_if_null()
        for partylink in self._partys.values():
            partylink.reset_deal_credit_debt()

    def _set_partylink_deal_credit_debt(self):
        partylinks_creditor_weight_sum = sum(
            partylink.creditor_weight for partylink in self._partys.values()
        )
        partylinks_debtor_weight_sum = sum(
            partylink.debtor_weight for partylink in self._partys.values()
        )

        for partylink in self._partys.values():
            partylink.set_deal_credit_debt(
                partylinks_creditor_weight_sum=partylinks_creditor_weight_sum,
                partylinks_debtor_weight_sum=partylinks_debtor_weight_sum,
                group_deal_credit=self._deal_credit,
                group_deal_debt=self._deal_debt,
                group_deal_agenda_credit=self._deal_agenda_credit,
                group_deal_agenda_debt=self._deal_agenda_debt,
            )

    def clear_partylinks(self):
        self._partys = {}

    def _set_partylinks_empty_if_null(self):
        if self._partys is None:
            self._partys = {}

    def get_partys_dict(self):
        self._set_partylinks_empty_if_null()

        partys_x_dict = {}
        for party in self._partys.values():
            party_dict = party.get_dict()
            partys_x_dict[party_dict["title"]] = party_dict

        return partys_x_dict

    def set_partylink(self, partylink: PartyLink):
        self._set_partylinks_empty_if_null()
        self._partys[partylink.title] = partylink

    def del_partylink(self, title):
        self._partys.pop(title)

    def meld(self, other_group):
        self._meld_attributes_that_will_be_equal(other_group=other_group)
        self.meld_partylinks(other_group=other_group)

    def meld_partylinks(self, other_group):
        self._set_partylinks_empty_if_null()
        for oba in other_group._partys.values():
            if self._partys.get(oba.title) is None:
                self._partys[oba.title] = oba
            else:
                self._partys[oba.title].meld(oba)

    def _meld_attributes_that_will_be_equal(self, other_group):
        xl = [
            ("brand", self.brand, other_group.brand),
            ("uid", self.uid, other_group.uid),
        ]
        while xl != []:
            attrs = xl.pop()
            if attrs[1] != attrs[2]:
                raise InvalidGroupException(
                    f"Meld fail GroupUnit {self.brand} .{attrs[0]}='{attrs[1]}' not the same as .{attrs[0]}='{attrs[2]}"
                )

        # if self.brand != other_group.brand:
        #     raise InvalidGroupException(
        #             f"Meld fail idea={self._pad},{self._label} {attrs[0]}:{attrs[1]} with {other_idea._pad},{other_idea._label} {attrs[0]}:{attrs[2]}"
        #     )


# class GroupUnitsshop:
def get_from_json(groupunits_json: str):
    groupunits_dict = x_get_dict(json_x=groupunits_json)
    return get_from_dict(x_dict=groupunits_dict)


def get_from_dict(x_dict: dict):
    groupunits = {}

    for groupunits_dict in x_dict.values():
        try:
            ex_partylinks_set_by_cure_road = groupunits_dict[
                "_partylinks_set_by_cure_road"
            ]
        except KeyError:
            ex_partylinks_set_by_cure_road = None

        x_group = groupunit_shop(
            brand=groupunits_dict["brand"],
            uid=groupunits_dict["uid"],
            _single_party=groupunits_dict["_single_party"],
            single_party_id=groupunits_dict["single_party_id"],
            _partys=partylinks_get_from_dict(x_dict=groupunits_dict["_partys"]),
            _partylinks_set_by_cure_road=ex_partylinks_set_by_cure_road,
        )
        groupunits[x_group.brand] = x_group
    return groupunits


def groupunit_shop(
    brand: GroupBrand,
    uid: int = None,
    single_party_id: int = None,
    _single_party: bool = None,
    _partys: dict[PartyTitle:PartyLink] = None,
    _deal_credit: float = None,
    _deal_debt: float = None,
    _deal_agenda_credit: float = None,
    _deal_agenda_debt: float = None,
    _partylinks_set_by_cure_road: Road = None,
) -> GroupUnit:
    if _single_party and _partylinks_set_by_cure_road != None:
        raise InvalidGroupException(
            f"_partylinks_set_by_cure_road cannot be '{_partylinks_set_by_cure_road}' for a single_party GroupUnit. It must have no value."
        )

    if _partys is None:
        _partys = {}
    if _single_party is None:
        _single_party = False
    return GroupUnit(
        brand=brand,
        uid=uid,
        single_party_id=single_party_id,
        _single_party=_single_party,
        _partys=_partys,
        _deal_credit=_deal_credit,
        _deal_debt=_deal_debt,
        _deal_agenda_credit=_deal_agenda_credit,
        _deal_agenda_debt=_deal_agenda_debt,
        _partylinks_set_by_cure_road=_partylinks_set_by_cure_road,
    )


@dataclasses.dataclass
class Balancelink(GroupCore):
    creditor_weight: float = 1.0
    debtor_weight: float = 1.0

    def get_dict(self):
        return {
            "brand": self.brand,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def meld(
        self,
        other_balancelink,
        other_on_meld_weight_action: str,
        src_on_meld_weight_action: str,
    ):
        self.creditor_weight = get_meld_weight(
            src_weight=self.creditor_weight,
            src_on_meld_weight_action=src_on_meld_weight_action,
            other_weight=other_balancelink.creditor_weight,
            other_on_meld_weight_action=other_on_meld_weight_action,
        )
        self.debtor_weight = get_meld_weight(
            src_weight=self.debtor_weight,
            src_on_meld_weight_action=src_on_meld_weight_action,
            other_weight=other_balancelink.debtor_weight,
            other_on_meld_weight_action=other_on_meld_weight_action,
        )


# class Balancelinksshop:
def balancelinks_get_from_json(balancelinks_json: str) -> dict[GroupBrand, Balancelink]:
    balancelinks_dict = x_get_dict(json_x=balancelinks_json)
    return balancelinks_get_from_dict(x_dict=balancelinks_dict)


def balancelinks_get_from_dict(x_dict: dict) -> dict[GroupBrand, Balancelink]:
    balancelinks = {}
    for balancelinks_dict in x_dict.values():
        x_group = balancelink_shop(
            brand=balancelinks_dict["brand"],
            creditor_weight=balancelinks_dict["creditor_weight"],
            debtor_weight=balancelinks_dict["debtor_weight"],
        )
        balancelinks[x_group.brand] = x_group
    return balancelinks


def balancelink_shop(
    brand: GroupBrand, creditor_weight: float = None, debtor_weight: float = None
) -> Balancelink:
    creditor_weight = x_func_return1ifnone(creditor_weight)
    debtor_weight = x_func_return1ifnone(debtor_weight)
    return Balancelink(
        brand=brand, creditor_weight=creditor_weight, debtor_weight=debtor_weight
    )


@dataclasses.dataclass
class BalanceHeir(GroupCore):
    creditor_weight: float = 1.0
    debtor_weight: float = 1.0
    _deal_credit: float = None
    _deal_debt: float = None

    def set_deal_credit_debt(
        self,
        idea_deal_importance,
        balanceheirs_creditor_weight_sum: float,
        balanceheirs_debtor_weight_sum: float,
    ):
        self._deal_credit = idea_deal_importance * (
            self.creditor_weight / balanceheirs_creditor_weight_sum
        )
        self._deal_debt = idea_deal_importance * (
            self.debtor_weight / balanceheirs_debtor_weight_sum
        )


def balanceheir_shop(
    brand: GroupBrand,
    creditor_weight: float = None,
    debtor_weight: float = None,
    _deal_credit: float = None,
    _deal_debt: float = None,
) -> BalanceHeir:
    creditor_weight = x_func_return1ifnone(creditor_weight)
    debtor_weight = x_func_return1ifnone(debtor_weight)
    return BalanceHeir(
        brand=brand,
        creditor_weight=creditor_weight,
        debtor_weight=debtor_weight,
        _deal_credit=_deal_credit,
        _deal_debt=_deal_debt,
    )


@dataclasses.dataclass
class Balanceline(GroupCore):
    _deal_credit: float
    _deal_debt: float

    def add_deal_credit_debt(self, deal_credit: float, deal_debt: float):
        self.set_deal_credit_debt_zero_if_null()
        self._deal_credit += deal_credit
        self._deal_debt += deal_debt

    def set_deal_credit_debt_zero_if_null(self):
        if self._deal_credit is None:
            self._deal_credit = 0
        if self._deal_debt is None:
            self._deal_debt = 0


class GroupMetrics:
    pass
