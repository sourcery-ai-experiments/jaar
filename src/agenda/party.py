from src._prime.road import PartyID
from dataclasses import dataclass
from src.tools.python import return1ifnone, x_get_dict


class InvalidPartyException(Exception):
    pass


class InvalidDepotLinkException(Exception):
    pass


class PartyTitle(str):
    pass


@dataclass
class PartyRing:
    pid: PartyID

    def get_dict(self):
        return {"pid": self.pid}


@dataclass
class PartyCore:
    pid: PartyID


# class PartyRingsshop:
def partyrings_get_from_json(partyrings_json: str) -> dict[str:PartyRing]:
    partyrings_dict = x_get_dict(json_x=partyrings_json)
    return partyrings_get_from_dict(x_dict=partyrings_dict)


def partyrings_get_from_dict(x_dict: dict) -> dict[str:PartyRing]:
    partyrings = {}
    if x_dict != None:
        for partyrings_dict in x_dict.values():
            x_partyring = partyrings_get_partyring(
                pid=partyrings_dict["pid"],
            )
            partyrings[x_partyring.pid] = x_partyring
    return partyrings


def partyrings_get_partyring(pid: PartyID) -> PartyRing:
    return PartyRing(pid=pid)


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
    _partyrings: dict[PartyID:PartyRing] = None
    _treasury_tax_paid: float = None
    _treasury_tax_diff: float = None
    _output_agenda_meld_order: int = None
    _treasury_credit_score: float = None
    _treasury_voice_rank: int = None
    _treasury_voice_hx_lowest_rank: int = None
    _title: PartyTitle = None

    def set_title(self, title: PartyTitle):
        self._title = title

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
                f"PartyUnit '{self.pid}' cannot have type '{depotlink_type}'."
            )
        self.depotlink_type = depotlink_type
        if creditor_weight != None:
            self.creditor_weight = creditor_weight
        if debtor_weight != None:
            self.debtor_weight = debtor_weight

    def del_depotlink_type(self):
        self.depotlink_type = None

    def clear_treasurying_data(self):
        self._treasury_tax_paid = None
        self._treasury_tax_diff = None
        self._treasury_credit_score = None
        self._treasury_voice_rank = None

    def set_treasurying_data(
        self,
        tax_paid: float,
        tax_diff: float,
        credit_score: float,
        voice_rank: int,
    ):
        self._treasury_tax_paid = tax_paid
        self._treasury_tax_diff = tax_diff
        self._treasury_credit_score = credit_score
        self.set_treasury_voice_rank(voice_rank)

        # if tax_diff is None or self._agenda_intent_ratio_credit is None:
        #     self._treasury_tax_diff = tax_diff
        # elif (
        #     round(self._treasury_tax_paid - self._agenda_intent_ratio_credit, 15) == tax_diff
        # ):
        #     self._treasury_tax_diff = tax_diff
        # else:
        #     raise Exception(
        #         f"PartyUnit.set_treasurying_data fail: tax_paid={tax_paid} + tax_diff={tax_diff} not equal to _agenda_intent_ratio_credit={self._agenda_intent_ratio_credit}"
        #     )

    def set_treasury_voice_rank(self, voice_rank: int):
        self._treasury_voice_rank = voice_rank
        self._set_treasury_voice_hx_lowest_rank()

    def _set_treasury_voice_hx_lowest_rank(
        self, treasury_voice_hx_lowest_rank: float = None
    ):
        if (
            treasury_voice_hx_lowest_rank != None
            and self._treasury_voice_hx_lowest_rank != None
        ):
            self._treasury_voice_hx_lowest_rank = treasury_voice_hx_lowest_rank

        if self._treasury_voice_hx_lowest_rank is None or (
            self._treasury_voice_hx_lowest_rank > self._treasury_voice_rank
        ):
            self._treasury_voice_hx_lowest_rank = self._treasury_voice_rank

    def get_dict(self):
        return {
            "pid": self.pid,
            "uid": self.uid,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
            "_creditor_active": self._creditor_active,
            "_debtor_active": self._debtor_active,
            "_partyrings": self.get_partyrings_dict(),
            "_treasury_tax_paid": self._treasury_tax_paid,
            "_treasury_tax_diff": self._treasury_tax_diff,
            "_treasury_credit_score": self._treasury_credit_score,
            "_treasury_voice_rank": self._treasury_voice_rank,
            "_treasury_voice_hx_lowest_rank": self._treasury_voice_hx_lowest_rank,
            "depotlink_type": self.depotlink_type,
            "_title": self._title,
        }

    def get_partyrings_dict(self):
        x_dict = {}
        if self._partyrings != None:
            for partyring in self._partyrings.values():
                x_dict[partyring.pid] = partyring.get_dict()
        return x_dict

    def get_creditor_weight(self):
        return return1ifnone(self.creditor_weight)

    def get_debtor_weight(self):
        return return1ifnone(self.debtor_weight)

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
        if self.pid != other_partyunit.pid:
            raise InvalidPartyException(
                f"Meld fail PartyUnit='{self.pid}' not the same as PartyUnit='{other_partyunit.pid}"
            )

        self.creditor_weight += other_partyunit.creditor_weight
        self.debtor_weight += other_partyunit.debtor_weight
        self._title = other_partyunit._title


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
            _treasury_tax_paid = partyunits_dict["_treasury_tax_paid"]
        except KeyError:
            _treasury_tax_paid = None

        try:
            _treasury_tax_diff = partyunits_dict["_treasury_tax_diff"]
        except KeyError:
            _treasury_tax_diff = None

        try:
            _treasury_credit_score = partyunits_dict["_treasury_credit_score"]
        except KeyError:
            _treasury_credit_score = None

        try:
            _treasury_voice_rank = partyunits_dict["_treasury_voice_rank"]
        except KeyError:
            _treasury_voice_rank = None

        try:
            _treasury_voice_hx_lowest_rank = partyunits_dict[
                "_treasury_voice_hx_lowest_rank"
            ]
        except KeyError:
            _treasury_voice_hx_lowest_rank = None

        try:
            depotlink_type = partyunits_dict["depotlink_type"]
        except KeyError:
            depotlink_type = None

        try:
            _title = partyunits_dict["_title"]
        except KeyError:
            _title = None

        x_partyunit = partyunit_shop(
            pid=partyunits_dict["pid"],
            uid=partyunits_dict["uid"],
            creditor_weight=partyunits_dict["creditor_weight"],
            debtor_weight=partyunits_dict["debtor_weight"],
            _creditor_active=partyunits_dict["_creditor_active"],
            _debtor_active=partyunits_dict["_debtor_active"],
            _partyrings=partyrings_get_from_dict(x_dict=partyrings),
            depotlink_type=depotlink_type,
            _title=_title,
        )
        x_partyunit.set_treasurying_data(
            tax_paid=_treasury_tax_paid,
            tax_diff=_treasury_tax_diff,
            credit_score=_treasury_credit_score,
            voice_rank=_treasury_voice_rank,
        )
        x_partyunit._set_treasury_voice_hx_lowest_rank(_treasury_voice_hx_lowest_rank)
        partyunits[x_partyunit.pid] = x_partyunit
    return partyunits


def partyunit_shop(
    pid: PartyID,
    uid: int = None,
    creditor_weight: int = None,
    debtor_weight: int = None,
    _creditor_active: bool = None,
    _debtor_active: bool = None,
    _partyrings: dict[PartyID:PartyRing] = None,
    _agenda_credit: float = None,
    _agenda_debt: float = None,
    _agenda_intent_credit: float = None,
    _agenda_intent_debt: float = None,
    _agenda_intent_ratio_credit: float = None,
    _agenda_intent_ratio_debt: float = None,
    _treasury_tax_paid: float = None,
    _treasury_tax_diff: float = None,
    depotlink_type: str = None,
    _title: PartyTitle = None,
) -> PartyUnit:
    final_partyrings = {} if _partyrings is None else _partyrings

    x_partyunit = PartyUnit(
        pid=pid,
        uid=uid,
        creditor_weight=return1ifnone(creditor_weight),
        debtor_weight=return1ifnone(debtor_weight),
        _creditor_active=_creditor_active,
        _debtor_active=_debtor_active,
        _agenda_credit=_agenda_credit,
        _agenda_debt=_agenda_debt,
        _agenda_intent_credit=_agenda_intent_credit,
        _agenda_intent_debt=_agenda_intent_debt,
        _agenda_intent_ratio_credit=_agenda_intent_ratio_credit,
        _agenda_intent_ratio_debt=_agenda_intent_ratio_debt,
        _partyrings=final_partyrings,
        _treasury_tax_paid=_treasury_tax_paid,
        _treasury_tax_diff=_treasury_tax_diff,
    )
    if depotlink_type != None:
        x_partyunit.set_depotlink_type(depotlink_type=depotlink_type)
    if _title != None:
        x_partyunit.set_title(_title)
    return x_partyunit


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
            "pid": self.pid,
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
        group_agenda_credit = return1ifnone(group_agenda_credit)
        group_agenda_debt = return1ifnone(group_agenda_debt)
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
        if self.pid != other_partylink.pid:
            raise InvalidPartyException(
                f"Meld fail PartyLink='{self.pid}' not the same as PartyLink='{other_partylink.pid}"
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
            pid=partylinks_dict["pid"],
            creditor_weight=partylinks_dict["creditor_weight"],
            debtor_weight=partylinks_dict["debtor_weight"],
        )
        partylinks[x_party.pid] = x_party
    return partylinks


def partylink_shop(
    pid: PartyID,
    creditor_weight: float = None,
    debtor_weight: float = None,
    _agenda_credit: float = None,
    _agenda_debt: float = None,
    _agenda_intent_credit: float = None,
    _agenda_intent_debt: float = None,
) -> PartyLink:
    creditor_weight = return1ifnone(creditor_weight)
    debtor_weight = return1ifnone(debtor_weight)
    return PartyLink(
        pid=pid,
        creditor_weight=creditor_weight,
        debtor_weight=debtor_weight,
        _agenda_credit=_agenda_credit,
        _agenda_debt=_agenda_debt,
        _agenda_intent_credit=_agenda_intent_credit,
        _agenda_intent_debt=_agenda_intent_debt,
    )


@dataclass
class PartyUnitExternalMetrics:
    internal_pid: PartyID = None
    creditor_active: bool = None
    debtor_active: bool = None


def get_depotlink_types() -> dict[str:None]:
    return {"blind_trust": None, "ignore": None, "assignment": None}
