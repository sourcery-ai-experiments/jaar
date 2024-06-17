from src._road.road import GuyID, default_road_delimiter_if_none, validate_roadnode
from src._road.finance import default_planck_if_none
from dataclasses import dataclass
from src._instrument.python import get_1_if_None, get_dict_from_json, get_0_if_None


class InvalidGuyException(Exception):
    pass


class _planck_RatioException(Exception):
    pass


@dataclass
class GuyCore:
    guy_id: GuyID = None
    _road_delimiter: str = None
    _planck: float = None

    def set_guy_id(self, x_guy_id: GuyID):
        self.guy_id = validate_roadnode(x_guy_id, self._road_delimiter)


@dataclass
class GuyUnit(GuyCore):
    """This represents the relationship from the AgendaUnit._owner_id to the GuyUnit.guy_id
    GuyUnit.credor_weight represents how much credor_weight the _owner_id gives the guy_id
    GuyUnit.debtor_weight represents how much debtor_weight the _owner_id gives the guy_id
    """

    credor_weight: int = None
    debtor_weight: int = None
    # calculated fields
    _irrational_debtor_weight: int = None  # set by listening process
    _inallocable_debtor_weight: int = None  # set by listening process
    # set by Agenda.calc_agenda_metrics()
    _agenda_cred: float = None
    _agenda_debt: float = None
    _agenda_intent_cred: float = None
    _agenda_intent_debt: float = None
    _agenda_intent_ratio_cred: float = None
    _agenda_intent_ratio_debt: float = None
    _credor_operational: bool = None
    _debtor_operational: bool = None
    # set by River process
    _treasury_due_paid: float = None
    _treasury_due_diff: float = None
    _output_agenda_meld_order: int = None
    _treasury_cred_score: float = None
    _treasury_voice_rank: int = None
    _treasury_voice_hx_lowest_rank: int = None

    def set_planck(self, x_planck: float):
        self._planck = x_planck

    def clear_output_agenda_meld_order(self):
        self._output_agenda_meld_order = None

    def set_output_agenda_meld_order(self, _output_agenda_meld_order: int):
        self._output_agenda_meld_order = _output_agenda_meld_order

    def set_credor_debtor_weight(
        self,
        credor_weight: float = None,
        debtor_weight: float = None,
    ):
        if credor_weight != None:
            self.set_credor_weight(credor_weight)
        if debtor_weight != None:
            self.set_debtor_weight(debtor_weight)

    def clear_treasurying_data(self):
        self._treasury_due_paid = None
        self._treasury_due_diff = None
        self._treasury_cred_score = None
        self._treasury_voice_rank = None

    def set_treasury_attr(
        self,
        due_paid: float,
        due_diff: float,
        cred_score: float,
        voice_rank: int,
    ):
        self._treasury_due_paid = due_paid
        self._treasury_due_diff = due_diff
        self._treasury_cred_score = cred_score
        self.set_treasury_voice_rank(voice_rank)

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

    def get_dict(self, all_attrs: bool = False) -> dict[str:str]:
        x_dict = {
            "guy_id": self.guy_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
            "_credor_operational": self._credor_operational,
            "_debtor_operational": self._debtor_operational,
            "_treasury_due_paid": self._treasury_due_paid,
            "_treasury_due_diff": self._treasury_due_diff,
            "_treasury_cred_score": self._treasury_cred_score,
            "_treasury_voice_rank": self._treasury_voice_rank,
            "_treasury_voice_hx_lowest_rank": self._treasury_voice_hx_lowest_rank,
        }
        if self._irrational_debtor_weight not in [None, 0]:
            x_dict["_irrational_debtor_weight"] = self._irrational_debtor_weight
        if self._inallocable_debtor_weight not in [None, 0]:
            x_dict["_inallocable_debtor_weight"] = self._inallocable_debtor_weight

        if all_attrs:
            self._all_attrs_necessary_in_dict(x_dict)
        return x_dict

    def _all_attrs_necessary_in_dict(self, x_dict):
        x_dict["_agenda_cred"] = self._agenda_cred
        x_dict["_agenda_debt"] = self._agenda_debt
        x_dict["_agenda_intent_cred"] = self._agenda_intent_cred
        x_dict["_agenda_intent_debt"] = self._agenda_intent_debt
        x_dict["_agenda_intent_ratio_cred"] = self._agenda_intent_ratio_cred
        x_dict["_agenda_intent_ratio_debt"] = self._agenda_intent_ratio_debt
        x_dict["_output_agenda_meld_order"] = self._output_agenda_meld_order

    def set_credor_weight(self, credor_weight: int):
        if (credor_weight / self._planck).is_integer() is False:
            raise _planck_RatioException(
                f"'{credor_weight}' is not divisible by planck '{self._planck}'"
            )
        self.credor_weight = credor_weight

    def set_debtor_weight(self, debtor_weight: int):
        if (debtor_weight / self._planck).is_integer() is False:
            raise _planck_RatioException(
                f"'{debtor_weight}' is not divisible by planck '{self._planck}'"
            )
        self.debtor_weight = debtor_weight

    def get_credor_weight(self):
        return get_1_if_None(self.credor_weight)

    def get_debtor_weight(self):
        return get_1_if_None(self.debtor_weight)

    def reset_agenda_cred_debt(self):
        self._agenda_cred = 0
        self._agenda_debt = 0
        self._agenda_intent_cred = 0
        self._agenda_intent_debt = 0
        self._agenda_intent_ratio_cred = 0
        self._agenda_intent_ratio_debt = 0

    def add_irrational_debtor_weight(self, x_irrational_debtor_weight: float):
        self._irrational_debtor_weight += x_irrational_debtor_weight

    def add_inallocable_debtor_weight(self, x_inallocable_debtor_weight: float):
        self._inallocable_debtor_weight += x_inallocable_debtor_weight

    def reset_listen_calculated_attrs(self):
        self._irrational_debtor_weight = 0
        self._inallocable_debtor_weight = 0

    def add_agenda_cred_debt(
        self,
        agenda_cred: float,
        agenda_debt,
        agenda_intent_cred: float,
        agenda_intent_debt,
    ):
        self._agenda_cred += agenda_cred
        self._agenda_debt += agenda_debt
        self._agenda_intent_cred += agenda_intent_cred
        self._agenda_intent_debt += agenda_intent_debt

    def set_agenda_intent_ratio_cred_debt(
        self,
        agenda_intent_ratio_cred_sum: float,
        agenda_intent_ratio_debt_sum: float,
        agenda_guyunit_total_credor_weight: float,
        agenda_guyunit_total_debtor_weight: float,
    ):
        if agenda_intent_ratio_cred_sum == 0:
            self._agenda_intent_ratio_cred = (
                self.get_credor_weight() / agenda_guyunit_total_credor_weight
            )
        else:
            self._agenda_intent_ratio_cred = (
                self._agenda_intent_cred / agenda_intent_ratio_cred_sum
            )

        if agenda_intent_ratio_debt_sum == 0:
            self._agenda_intent_ratio_debt = (
                self.get_debtor_weight() / agenda_guyunit_total_debtor_weight
            )
        else:
            self._agenda_intent_ratio_debt = (
                self._agenda_intent_debt / agenda_intent_ratio_debt_sum
            )

    def meld(self, exterior_guyunit):
        if self.guy_id != exterior_guyunit.guy_id:
            raise InvalidGuyException(
                f"Meld fail GuyUnit='{self.guy_id}' not the same as GuyUnit='{exterior_guyunit.guy_id}"
            )

        self.credor_weight += exterior_guyunit.credor_weight
        self.debtor_weight += exterior_guyunit.debtor_weight
        self._irrational_debtor_weight += exterior_guyunit._irrational_debtor_weight
        self._inallocable_debtor_weight += exterior_guyunit._inallocable_debtor_weight


# class GuyUnitsshop:
def guyunits_get_from_json(guyunits_json: str) -> dict[str:GuyUnit]:
    guyunits_dict = get_dict_from_json(json_x=guyunits_json)
    return guyunits_get_from_dict(x_dict=guyunits_dict)


def guyunits_get_from_dict(
    x_dict: dict, _road_delimiter: str = None
) -> dict[str:GuyUnit]:
    guyunits = {}
    for guyunit_dict in x_dict.values():
        x_guyunit = guyunit_get_from_dict(guyunit_dict, _road_delimiter)
        guyunits[x_guyunit.guy_id] = x_guyunit
    return guyunits


def guyunit_get_from_dict(guyunit_dict: dict, _road_delimiter: str) -> GuyUnit:
    _irrational_debtor_weight = guyunit_dict.get("_irrational_debtor_weight", 0)
    _inallocable_debtor_weight = guyunit_dict.get("_inallocable_debtor_weight", 0)
    _treasury_due_paid = guyunit_dict.get("_treasury_due_paid", 0)
    _treasury_due_diff = guyunit_dict.get("_treasury_due_diff", 0)
    _treasury_cred_score = guyunit_dict.get("_treasury_cred_score", 0)
    _treasury_voice_rank = guyunit_dict.get("_treasury_voice_rank", 0)
    _treasury_voice_hx_lowest_rank = guyunit_dict.get(
        "_treasury_voice_hx_lowest_rank", 0
    )

    x_guyunit = guyunit_shop(
        guy_id=guyunit_dict["guy_id"],
        credor_weight=guyunit_dict["credor_weight"],
        debtor_weight=guyunit_dict["debtor_weight"],
        _credor_operational=guyunit_dict["_credor_operational"],
        _debtor_operational=guyunit_dict["_debtor_operational"],
        _road_delimiter=_road_delimiter,
    )
    x_guyunit.set_treasury_attr(
        due_paid=_treasury_due_paid,
        due_diff=_treasury_due_diff,
        cred_score=_treasury_cred_score,
        voice_rank=_treasury_voice_rank,
    )
    x_guyunit._set_treasury_voice_hx_lowest_rank(_treasury_voice_hx_lowest_rank)
    x_guyunit.add_irrational_debtor_weight(get_0_if_None(_irrational_debtor_weight))
    x_guyunit.add_inallocable_debtor_weight(get_0_if_None(_inallocable_debtor_weight))

    return x_guyunit


def guyunit_shop(
    guy_id: GuyID,
    credor_weight: int = None,
    debtor_weight: int = None,
    _credor_operational: bool = None,
    _debtor_operational: bool = None,
    _road_delimiter: str = None,
    _planck: float = None,
) -> GuyUnit:
    x_guyunit = GuyUnit(
        credor_weight=get_1_if_None(credor_weight),
        debtor_weight=get_1_if_None(debtor_weight),
        _irrational_debtor_weight=get_0_if_None(),
        _inallocable_debtor_weight=get_0_if_None(),
        _credor_operational=_credor_operational,
        _debtor_operational=_debtor_operational,
        _agenda_cred=get_0_if_None(),
        _agenda_debt=get_0_if_None(),
        _agenda_intent_cred=get_0_if_None(),
        _agenda_intent_debt=get_0_if_None(),
        _agenda_intent_ratio_cred=get_0_if_None(),
        _agenda_intent_ratio_debt=get_0_if_None(),
        _treasury_due_paid=None,
        _treasury_due_diff=None,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _planck=default_planck_if_none(_planck),
    )
    x_guyunit.set_guy_id(x_guy_id=guy_id)
    return x_guyunit


@dataclass
class GuyLink(GuyCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0
    _agenda_cred: float = None
    _agenda_debt: float = None
    _agenda_intent_cred: float = None
    _agenda_intent_debt: float = None

    def get_dict(self) -> dict[str:str]:
        return {
            "guy_id": self.guy_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def set_agenda_cred_debt(
        self,
        guylinks_credor_weight_sum: float,
        guylinks_debtor_weight_sum: float,
        belief_agenda_cred: float,
        belief_agenda_debt: float,
        belief_agenda_intent_cred: float,
        belief_agenda_intent_debt: float,
    ):
        belief_agenda_cred = get_1_if_None(belief_agenda_cred)
        belief_agenda_debt = get_1_if_None(belief_agenda_debt)
        credor_ratio = self.credor_weight / guylinks_credor_weight_sum
        debtor_ratio = self.debtor_weight / guylinks_debtor_weight_sum

        self._agenda_cred = belief_agenda_cred * credor_ratio
        self._agenda_debt = belief_agenda_debt * debtor_ratio
        self._agenda_intent_cred = belief_agenda_intent_cred * credor_ratio
        self._agenda_intent_debt = belief_agenda_intent_debt * debtor_ratio

    def reset_agenda_cred_debt(self):
        self._agenda_cred = 0
        self._agenda_debt = 0
        self._agenda_intent_cred = 0
        self._agenda_intent_debt = 0

    def meld(self, exterior_guylink):
        if self.guy_id != exterior_guylink.guy_id:
            raise InvalidGuyException(
                f"Meld fail GuyLink='{self.guy_id}' not the same as GuyLink='{exterior_guylink.guy_id}"
            )
        self.credor_weight += exterior_guylink.credor_weight
        self.debtor_weight += exterior_guylink.debtor_weight


# class GuyLinkshop:
def guylinks_get_from_json(guylinks_json: str) -> dict[str:GuyLink]:
    guylinks_dict = get_dict_from_json(json_x=guylinks_json)
    return guylinks_get_from_dict(x_dict=guylinks_dict)


def guylinks_get_from_dict(x_dict: dict) -> dict[str:GuyLink]:
    if x_dict is None:
        x_dict = {}
    guylinks = {}
    for guylinks_dict in x_dict.values():
        x_guy = guylink_shop(
            guy_id=guylinks_dict["guy_id"],
            credor_weight=guylinks_dict["credor_weight"],
            debtor_weight=guylinks_dict["debtor_weight"],
        )
        guylinks[x_guy.guy_id] = x_guy
    return guylinks


def guylink_shop(
    guy_id: GuyID,
    credor_weight: float = None,
    debtor_weight: float = None,
    _agenda_cred: float = None,
    _agenda_debt: float = None,
    _agenda_intent_cred: float = None,
    _agenda_intent_debt: float = None,
) -> GuyLink:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return GuyLink(
        guy_id=guy_id,
        credor_weight=credor_weight,
        debtor_weight=debtor_weight,
        _agenda_cred=_agenda_cred,
        _agenda_debt=_agenda_debt,
        _agenda_intent_cred=_agenda_intent_cred,
        _agenda_intent_debt=_agenda_intent_debt,
    )


@dataclass
class GuyUnitExternalMetrics:
    internal_guy_id: GuyID = None
    credor_operational: bool = None
    debtor_operational: bool = None
