from dataclasses import dataclass
from src.agenda.x_func import x_get_dict, return1ifnone as x_func_return1ifnone


class InvalidPartyException(Exception):
    pass


class InvalidDepotLinkException(Exception):
    pass


class PersonName(str):  # Created to help track the concept
    pass


class PartyHandle(PersonName):  # Created to help track the concept
    pass


@dataclass
class PartyRing:
    handle: PartyHandle

    def get_dict(self):
        return {"handle": self.handle}


@dataclass
class PartyCore:
    handle: PartyHandle


# class PartyRingsshop:
def partyrings_get_from_json(partyrings_json: str) -> dict[str:PartyRing]:
    partyrings_dict = x_get_dict(json_x=partyrings_json)
    return partyrings_get_from_dict(x_dict=partyrings_dict)


def partyrings_get_from_dict(x_dict: dict) -> dict[str:PartyRing]:
    partyrings = {}
    if x_dict != None:
        for partyrings_dict in x_dict.values():
            x_partyring = partyrings_get_partyring(
                handle=partyrings_dict["handle"],
            )
            partyrings[x_partyring.handle] = x_partyring
    return partyrings


def partyrings_get_partyring(handle: PartyHandle) -> PartyRing:
    return PartyRing(handle=handle)


@dataclass
class PartyUnit(PartyCore):
    uid: int = None
    creditor_weight: int = None
    debtor_weight: int = None
    depotlink_type: str = None
    _agenda_credit: float = None
    _agenda_debt: float = None
    _agenda_intent_credit: float = None
    _agenda_intent_debt: float = None
    _agenda_intent_ratio_credit: float = None
    _agenda_intent_ratio_debt: float = None
    _creditor_active: bool = None
    _debtor_active: bool = None
    _partyrings: dict[PartyHandle:PartyRing] = None
    _bank_tax_paid: float = None
    _bank_tax_diff: float = None
    _output_agenda_meld_order: int = None
    _bank_credit_score: float = None
    _bank_voice_rank: int = None
    _bank_voice_hx_lowest_rank: int = None

    def clear_output_agenda_meld_order(self):
        self._output_agenda_meld_order = None

    def set_output_agenda_meld_order(self, _output_agenda_meld_order: int):
        self._output_agenda_meld_order = _output_agenda_meld_order

    def set_depotlink_type(
        self,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        if depotlink_type not in (list(get_depotlink_types())):
            raise InvalidDepotLinkException(
                f"PartyUnit '{self.handle}' cannot have type '{depotlink_type}'."
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
        self._bank_credit_score = None
        self._bank_voice_rank = None

    def set_banking_data(
        self,
        tax_paid: float,
        tax_diff: float,
        credit_score: float,
        voice_rank: int,
    ):
        self._bank_tax_paid = tax_paid
        self._bank_tax_diff = tax_diff
        self._bank_credit_score = credit_score
        self.set_bank_voice_rank(voice_rank)

        # if tax_diff is None or self._agenda_intent_ratio_credit is None:
        #     self._bank_tax_diff = tax_diff
        # elif (
        #     round(self._bank_tax_paid - self._agenda_intent_ratio_credit, 15) == tax_diff
        # ):
        #     self._bank_tax_diff = tax_diff
        # else:
        #     raise Exception(
        #         f"PartyUnit.set_banking_data fail: tax_paid={tax_paid} + tax_diff={tax_diff} not equal to _agenda_intent_ratio_credit={self._agenda_intent_ratio_credit}"
        #     )

    def set_bank_voice_rank(self, voice_rank: int):
        self._bank_voice_rank = voice_rank
        self._set_bank_voice_hx_lowest_rank()

    def _set_bank_voice_hx_lowest_rank(self, bank_voice_hx_lowest_rank: float = None):
        if (
            bank_voice_hx_lowest_rank != None
            and self._bank_voice_hx_lowest_rank != None
        ):
            self._bank_voice_hx_lowest_rank = bank_voice_hx_lowest_rank

        if self._bank_voice_hx_lowest_rank is None or (
            self._bank_voice_hx_lowest_rank > self._bank_voice_rank
        ):
            self._bank_voice_hx_lowest_rank = self._bank_voice_rank

    def get_dict(self):
        return {
            "handle": self.handle,
            "uid": self.uid,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
            "_creditor_active": self._creditor_active,
            "_debtor_active": self._debtor_active,
            "_partyrings": self.get_partyrings_dict(),
            "_bank_tax_paid": self._bank_tax_paid,
            "_bank_tax_diff": self._bank_tax_diff,
            "_bank_credit_score": self._bank_credit_score,
            "_bank_voice_rank": self._bank_voice_rank,
            "_bank_voice_hx_lowest_rank": self._bank_voice_hx_lowest_rank,
            "depotlink_type": self.depotlink_type,
        }

    def get_partyrings_dict(self):
        x_dict = {}
        if self._partyrings != None:
            for partyring in self._partyrings.values():
                x_dict[partyring.handle] = partyring.get_dict()
        return x_dict

    def get_creditor_weight(self):
        return x_func_return1ifnone(self.creditor_weight)

    def get_debtor_weight(self):
        return x_func_return1ifnone(self.debtor_weight)

    def set_empty_agenda_credit_debt_to_zero(self):
        if self._agenda_credit is None:
            self._agenda_credit = 0
        if self._agenda_debt is None:
            self._agenda_debt = 0
        if self._agenda_intent_credit is None:
            self._agenda_intent_credit = 0
        if self._agenda_intent_debt is None:
            self._agenda_intent_debt = 0
        if self._agenda_intent_ratio_credit is None:
            self._agenda_intent_ratio_credit = 0
        if self._agenda_intent_ratio_debt is None:
            self._agenda_intent_ratio_debt = 0

    def reset_agenda_credit_debt(self):
        self._agenda_credit = 0
        self._agenda_debt = 0
        self._agenda_intent_credit = 0
        self._agenda_intent_debt = 0
        self._agenda_intent_ratio_credit = 0
        self._agenda_intent_ratio_debt = 0

    def add_agenda_credit_debt(
        self,
        agenda_credit: float,
        agenda_debt,
        agenda_intent_credit: float,
        agenda_intent_debt,
    ):
        self.set_empty_agenda_credit_debt_to_zero()
        self._agenda_credit += agenda_credit
        self._agenda_debt += agenda_debt
        self._agenda_intent_credit += agenda_intent_credit
        self._agenda_intent_debt += agenda_intent_debt

    def set_agenda_intent_ratio_credit_debt(
        self,
        agenda_intent_ratio_credit_sum: float,
        agenda_intent_ratio_debt_sum: float,
        agenda_partyunit_total_creditor_weight: float,
        agenda_partyunit_total_debtor_weight: float,
    ):
        if agenda_intent_ratio_credit_sum == 0:
            self._agenda_intent_ratio_credit = (
                self.get_creditor_weight() / agenda_partyunit_total_creditor_weight
            )
        else:
            self._agenda_intent_ratio_credit = (
                self._agenda_intent_credit / agenda_intent_ratio_credit_sum
            )

        if agenda_intent_ratio_debt_sum == 0:
            self._agenda_intent_ratio_debt = (
                self.get_debtor_weight() / agenda_partyunit_total_debtor_weight
            )
        else:
            self._agenda_intent_ratio_debt = (
                self._agenda_intent_debt / agenda_intent_ratio_debt_sum
            )

    def meld(self, other_partyunit):
        if self.handle != other_partyunit.handle:
            raise InvalidPartyException(
                f"Meld fail PartyUnit='{self.handle}' not the same as PartyUnit='{other_partyunit.handle}"
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
            _bank_credit_score = partyunits_dict["_bank_credit_score"]
        except KeyError:
            _bank_credit_score = None

        try:
            _bank_voice_rank = partyunits_dict["_bank_voice_rank"]
        except KeyError:
            _bank_voice_rank = None

        try:
            _bank_voice_hx_lowest_rank = partyunits_dict["_bank_voice_hx_lowest_rank"]
        except KeyError:
            _bank_voice_hx_lowest_rank = None

        try:
            depotlink_type = partyunits_dict["depotlink_type"]
        except KeyError:
            depotlink_type = None

        x_partyunit = partyunit_shop(
            handle=partyunits_dict["handle"],
            uid=partyunits_dict["uid"],
            creditor_weight=partyunits_dict["creditor_weight"],
            debtor_weight=partyunits_dict["debtor_weight"],
            _creditor_active=partyunits_dict["_creditor_active"],
            _debtor_active=partyunits_dict["_debtor_active"],
            _partyrings=partyrings_get_from_dict(x_dict=partyrings),
            depotlink_type=depotlink_type,
        )
        x_partyunit.set_banking_data(
            tax_paid=_bank_tax_paid,
            tax_diff=_bank_tax_diff,
            credit_score=_bank_credit_score,
            voice_rank=_bank_voice_rank,
        )
        x_partyunit._set_bank_voice_hx_lowest_rank(_bank_voice_hx_lowest_rank)
        partyunits[x_partyunit.handle] = x_partyunit
    return partyunits


def partyunit_shop(
    handle: PartyHandle,
    uid: int = None,
    creditor_weight: int = None,
    debtor_weight: int = None,
    _creditor_active: bool = None,
    _debtor_active: bool = None,
    _partyrings: dict[PartyHandle:PartyRing] = None,
    _agenda_credit: float = None,
    _agenda_debt: float = None,
    _agenda_intent_credit: float = None,
    _agenda_intent_debt: float = None,
    _agenda_intent_ratio_credit: float = None,
    _agenda_intent_ratio_debt: float = None,
    _bank_tax_paid: float = None,
    _bank_tax_diff: float = None,
    depotlink_type: str = None,
) -> PartyUnit:
    final_partyrings = {} if _partyrings is None else _partyrings

    partyunit_x = PartyUnit(
        handle=handle,
        uid=uid,
        creditor_weight=x_func_return1ifnone(creditor_weight),
        debtor_weight=x_func_return1ifnone(debtor_weight),
        _creditor_active=_creditor_active,
        _debtor_active=_debtor_active,
        _agenda_credit=_agenda_credit,
        _agenda_debt=_agenda_debt,
        _agenda_intent_credit=_agenda_intent_credit,
        _agenda_intent_debt=_agenda_intent_debt,
        _agenda_intent_ratio_credit=_agenda_intent_ratio_credit,
        _agenda_intent_ratio_debt=_agenda_intent_ratio_debt,
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
    _agenda_credit: float = None
    _agenda_debt: float = None
    _agenda_intent_credit: float = None
    _agenda_intent_debt: float = None

    def get_dict(self):
        return {
            "handle": self.handle,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def set_agenda_credit_debt(
        self,
        partylinks_creditor_weight_sum: float,
        partylinks_debtor_weight_sum: float,
        group_agenda_credit: float,
        group_agenda_debt: float,
        group_agenda_intent_credit: float,
        group_agenda_intent_debt: float,
    ):
        group_agenda_credit = x_func_return1ifnone(group_agenda_credit)
        group_agenda_debt = x_func_return1ifnone(group_agenda_debt)
        creditor_ratio = self.creditor_weight / partylinks_creditor_weight_sum
        debtor_ratio = self.debtor_weight / partylinks_debtor_weight_sum

        self._agenda_credit = group_agenda_credit * creditor_ratio
        self._agenda_debt = group_agenda_debt * debtor_ratio
        self._agenda_intent_credit = group_agenda_intent_credit * creditor_ratio
        self._agenda_intent_debt = group_agenda_intent_debt * debtor_ratio

    def reset_agenda_credit_debt(self):
        self._agenda_credit = 0
        self._agenda_debt = 0
        self._agenda_intent_credit = 0
        self._agenda_intent_debt = 0

    def meld(self, other_partylink):
        if self.handle != other_partylink.handle:
            raise InvalidPartyException(
                f"Meld fail PartyLink='{self.handle}' not the same as PartyLink='{other_partylink.handle}"
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
            handle=partylinks_dict["handle"],
            creditor_weight=partylinks_dict["creditor_weight"],
            debtor_weight=partylinks_dict["debtor_weight"],
        )
        partylinks[x_party.handle] = x_party
    return partylinks


def partylink_shop(
    handle: PartyHandle,
    creditor_weight: float = None,
    debtor_weight: float = None,
    _agenda_credit: float = None,
    _agenda_debt: float = None,
    _agenda_intent_credit: float = None,
    _agenda_intent_debt: float = None,
) -> PartyLink:
    creditor_weight = x_func_return1ifnone(creditor_weight)
    debtor_weight = x_func_return1ifnone(debtor_weight)
    return PartyLink(
        handle=handle,
        creditor_weight=creditor_weight,
        debtor_weight=debtor_weight,
        _agenda_credit=_agenda_credit,
        _agenda_debt=_agenda_debt,
        _agenda_intent_credit=_agenda_intent_credit,
        _agenda_intent_debt=_agenda_intent_debt,
    )


@dataclass
class PartyUnitExternalMetrics:
    internal_handle: PartyHandle = None
    creditor_active: bool = None
    debtor_active: bool = None


def get_depotlink_types() -> dict[str:None]:
    return {"blind_trust": None, "ignore": None, "assignment": None}
