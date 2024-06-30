from src._instrument.python import get_1_if_None, get_dict_from_json, get_0_if_None
from src._road.road import CharID, default_road_delimiter_if_none, validate_roadnode
from src._road.finance import default_pixel_if_none
from src._world.beliefhold import BeliefID, BeliefHold, beliefholds_get_from_dict
from dataclasses import dataclass


class InvalidCharException(Exception):
    pass


class _pixel_RatioException(Exception):
    pass


@dataclass
class CharCore:
    char_id: CharID = None
    _road_delimiter: str = None
    _pixel: float = None

    def set_char_id(self, x_char_id: CharID):
        self.char_id = validate_roadnode(x_char_id, self._road_delimiter)


@dataclass
class CharUnit(CharCore):
    """This represents the relationship from the WorldUnit._owner_id to the CharUnit.char_id
    CharUnit.credor_weight represents how much credor_weight the _owner_id gives the char_id
    CharUnit.debtor_weight represents how much debtor_weight the _owner_id gives the char_id
    """

    credor_weight: int = None
    debtor_weight: int = None
    # special attribute: static in world json, in memory it is deleted after loading and recalculated during saving.
    _beliefholds: dict[CharID:BeliefHold] = None
    # calculated fields
    _irrational_debtor_weight: int = None  # set by listening process
    _inallocable_debtor_weight: int = None  # set by listening process
    # set by World.calc_world_metrics()
    _world_cred: float = None
    _world_debt: float = None
    _world_agenda_cred: float = None
    _world_agenda_debt: float = None
    _world_agenda_ratio_cred: float = None
    _world_agenda_ratio_debt: float = None
    _credor_operational: bool = None
    _debtor_operational: bool = None
    # set by River process
    _treasury_due_paid: float = None
    _treasury_due_diff: float = None
    _output_world_meld_order: int = None
    _treasury_cred_score: float = None
    _treasury_voice_rank: int = None
    _treasury_voice_hx_lowest_rank: int = None

    def set_pixel(self, x_pixel: float):
        self._pixel = x_pixel

    def clear_output_world_meld_order(self):
        self._output_world_meld_order = None

    def set_output_world_meld_order(self, _output_world_meld_order: int):
        self._output_world_meld_order = _output_world_meld_order

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
        _treasury_due_paid: float,
        _treasury_due_diff: float,
        cred_score: float,
        voice_rank: int,
    ):
        self._treasury_due_paid = _treasury_due_paid
        self._treasury_due_diff = _treasury_due_diff
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

    def set_credor_weight(self, credor_weight: int):
        if (credor_weight / self._pixel).is_integer() is False:
            raise _pixel_RatioException(
                f"'{credor_weight}' is not divisible by pixel '{self._pixel}'"
            )
        self.credor_weight = credor_weight

    def set_debtor_weight(self, debtor_weight: int):
        if (debtor_weight / self._pixel).is_integer() is False:
            raise _pixel_RatioException(
                f"'{debtor_weight}' is not divisible by pixel '{self._pixel}'"
            )
        self.debtor_weight = debtor_weight

    def get_credor_weight(self):
        return get_1_if_None(self.credor_weight)

    def get_debtor_weight(self):
        return get_1_if_None(self.debtor_weight)

    def reset_world_cred_debt(self):
        self._world_cred = 0
        self._world_debt = 0
        self._world_agenda_cred = 0
        self._world_agenda_debt = 0
        self._world_agenda_ratio_cred = 0
        self._world_agenda_ratio_debt = 0

    def add_irrational_debtor_weight(self, x_irrational_debtor_weight: float):
        self._irrational_debtor_weight += x_irrational_debtor_weight

    def add_inallocable_debtor_weight(self, x_inallocable_debtor_weight: float):
        self._inallocable_debtor_weight += x_inallocable_debtor_weight

    def reset_listen_calculated_attrs(self):
        self._irrational_debtor_weight = 0
        self._inallocable_debtor_weight = 0

    def add_world_cred_debt(
        self,
        world_cred: float,
        world_debt,
        world_agenda_cred: float,
        world_agenda_debt,
    ):
        self._world_cred += world_cred
        self._world_debt += world_debt
        self._world_agenda_cred += world_agenda_cred
        self._world_agenda_debt += world_agenda_debt

    def set_world_agenda_ratio_cred_debt(
        self,
        world_agenda_ratio_cred_sum: float,
        world_agenda_ratio_debt_sum: float,
        world_charunit_total_credor_weight: float,
        world_charunit_total_debtor_weight: float,
    ):
        if world_agenda_ratio_cred_sum == 0:
            self._world_agenda_ratio_cred = (
                self.get_credor_weight() / world_charunit_total_credor_weight
            )
        else:
            self._world_agenda_ratio_cred = (
                self._world_agenda_cred / world_agenda_ratio_cred_sum
            )

        if world_agenda_ratio_debt_sum == 0:
            self._world_agenda_ratio_debt = (
                self.get_debtor_weight() / world_charunit_total_debtor_weight
            )
        else:
            self._world_agenda_ratio_debt = (
                self._world_agenda_debt / world_agenda_ratio_debt_sum
            )

    def meld(self, exterior_charunit):
        if self.char_id != exterior_charunit.char_id:
            raise InvalidCharException(
                f"Meld fail CharUnit='{self.char_id}' not the equal as CharUnit='{exterior_charunit.char_id}"
            )

        self.credor_weight += exterior_charunit.credor_weight
        self.debtor_weight += exterior_charunit.debtor_weight
        self._irrational_debtor_weight += exterior_charunit._irrational_debtor_weight
        self._inallocable_debtor_weight += exterior_charunit._inallocable_debtor_weight

    def set_beliefhold(self, beliefhold: BeliefHold):
        self._beliefholds[beliefhold.belief_id] = beliefhold

    def get_beliefhold(self, belief_id: BeliefID) -> BeliefHold:
        return self._beliefholds.get(belief_id)

    def beliefhold_exists(self, belief_id: BeliefID) -> bool:
        return self._beliefholds.get(belief_id) != None

    def delete_beliefhold(self, belief_id: BeliefID):
        return self._beliefholds.pop(belief_id)

    def clear_beliefholds(self):
        self._beliefholds = {}

    def get_beliefholds_dict(self) -> dict:
        return {
            x_beliefhold.belief_id: {
                "belief_id": x_beliefhold.belief_id,
                "credor_weight": x_beliefhold.credor_weight,
                "debtor_weight": x_beliefhold.debtor_weight,
            }
            for x_beliefhold in self._beliefholds.values()
        }

    def get_dict(self, all_attrs: bool = False) -> dict[str:str]:
        x_dict = {
            "char_id": self.char_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
            "_beliefholds": self.get_beliefholds_dict(),
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
        x_dict["_world_cred"] = self._world_cred
        x_dict["_world_debt"] = self._world_debt
        x_dict["_world_agenda_cred"] = self._world_agenda_cred
        x_dict["_world_agenda_debt"] = self._world_agenda_debt
        x_dict["_world_agenda_ratio_cred"] = self._world_agenda_ratio_cred
        x_dict["_world_agenda_ratio_debt"] = self._world_agenda_ratio_debt
        x_dict["_output_world_meld_order"] = self._output_world_meld_order


# class CharUnitsshop:
def charunits_get_from_json(charunits_json: str) -> dict[str:CharUnit]:
    charunits_dict = get_dict_from_json(json_x=charunits_json)
    return charunits_get_from_dict(x_dict=charunits_dict)


def charunits_get_from_dict(
    x_dict: dict, _road_delimiter: str = None
) -> dict[str:CharUnit]:
    charunits = {}
    for charunit_dict in x_dict.values():
        x_charunit = charunit_get_from_dict(charunit_dict, _road_delimiter)
        charunits[x_charunit.char_id] = x_charunit
    return charunits


def charunit_get_from_dict(charunit_dict: dict, _road_delimiter: str) -> CharUnit:
    _irrational_debtor_weight = charunit_dict.get("_irrational_debtor_weight", 0)
    _inallocable_debtor_weight = charunit_dict.get("_inallocable_debtor_weight", 0)
    _treasury_due_paid = charunit_dict.get("_treasury_due_paid", 0)
    _treasury_due_diff = charunit_dict.get("_treasury_due_diff", 0)
    _treasury_cred_score = charunit_dict.get("_treasury_cred_score", 0)
    _treasury_voice_rank = charunit_dict.get("_treasury_voice_rank", 0)
    _treasury_voice_hx_lowest_rank = charunit_dict.get(
        "_treasury_voice_hx_lowest_rank", 0
    )
    x_charunit = charunit_shop(
        char_id=charunit_dict["char_id"],
        credor_weight=charunit_dict["credor_weight"],
        debtor_weight=charunit_dict["debtor_weight"],
        _credor_operational=charunit_dict["_credor_operational"],
        _debtor_operational=charunit_dict["_debtor_operational"],
        _road_delimiter=_road_delimiter,
    )
    x_charunit._beliefholds = beliefholds_get_from_dict(charunit_dict["_beliefholds"])
    x_charunit.set_treasury_attr(
        _treasury_due_paid=_treasury_due_paid,
        _treasury_due_diff=_treasury_due_diff,
        cred_score=_treasury_cred_score,
        voice_rank=_treasury_voice_rank,
    )
    x_charunit._set_treasury_voice_hx_lowest_rank(_treasury_voice_hx_lowest_rank)
    x_charunit.add_irrational_debtor_weight(get_0_if_None(_irrational_debtor_weight))
    x_charunit.add_inallocable_debtor_weight(get_0_if_None(_inallocable_debtor_weight))

    return x_charunit


def charunit_shop(
    char_id: CharID,
    credor_weight: int = None,
    debtor_weight: int = None,
    _credor_operational: bool = None,
    _debtor_operational: bool = None,
    _road_delimiter: str = None,
    _pixel: float = None,
) -> CharUnit:
    x_charunit = CharUnit(
        credor_weight=get_1_if_None(credor_weight),
        debtor_weight=get_1_if_None(debtor_weight),
        _beliefholds={},
        _irrational_debtor_weight=get_0_if_None(),
        _inallocable_debtor_weight=get_0_if_None(),
        _credor_operational=_credor_operational,
        _debtor_operational=_debtor_operational,
        _world_cred=get_0_if_None(),
        _world_debt=get_0_if_None(),
        _world_agenda_cred=get_0_if_None(),
        _world_agenda_debt=get_0_if_None(),
        _world_agenda_ratio_cred=get_0_if_None(),
        _world_agenda_ratio_debt=get_0_if_None(),
        _treasury_due_paid=None,
        _treasury_due_diff=None,
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _pixel=default_pixel_if_none(_pixel),
    )
    x_charunit.set_char_id(x_char_id=char_id)
    return x_charunit


@dataclass
class CharLink(CharCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0
    _world_cred: float = None
    _world_debt: float = None
    _world_agenda_cred: float = None
    _world_agenda_debt: float = None

    def get_dict(self) -> dict[str:str]:
        return {
            "char_id": self.char_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def set_world_cred_debt(
        self,
        charlinks_credor_weight_sum: float,
        charlinks_debtor_weight_sum: float,
        belief_world_cred: float,
        belief_world_debt: float,
        belief_world_agenda_cred: float,
        belief_world_agenda_debt: float,
    ):
        belief_world_cred = get_1_if_None(belief_world_cred)
        belief_world_debt = get_1_if_None(belief_world_debt)
        credor_ratio = self.credor_weight / charlinks_credor_weight_sum
        debtor_ratio = self.debtor_weight / charlinks_debtor_weight_sum

        self._world_cred = belief_world_cred * credor_ratio
        self._world_debt = belief_world_debt * debtor_ratio
        self._world_agenda_cred = belief_world_agenda_cred * credor_ratio
        self._world_agenda_debt = belief_world_agenda_debt * debtor_ratio

    def reset_world_cred_debt(self):
        self._world_cred = 0
        self._world_debt = 0
        self._world_agenda_cred = 0
        self._world_agenda_debt = 0

    def meld(self, exterior_charlink):
        if self.char_id != exterior_charlink.char_id:
            raise InvalidCharException(
                f"Meld fail CharLink='{self.char_id}' not the equal as CharLink='{exterior_charlink.char_id}"
            )
        self.credor_weight += exterior_charlink.credor_weight
        self.debtor_weight += exterior_charlink.debtor_weight


def charlinks_get_from_json(charlinks_json: str) -> dict[str:CharLink]:
    charlinks_dict = get_dict_from_json(json_x=charlinks_json)
    return charlinks_get_from_dict(x_dict=charlinks_dict)


def charlinks_get_from_dict(x_dict: dict) -> dict[str:CharLink]:
    if x_dict is None:
        x_dict = {}
    charlinks = {}
    for charlinks_dict in x_dict.values():
        x_char = charlink_shop(
            char_id=charlinks_dict["char_id"],
            credor_weight=charlinks_dict["credor_weight"],
            debtor_weight=charlinks_dict["debtor_weight"],
        )
        charlinks[x_char.char_id] = x_char
    return charlinks


def charlink_shop(
    char_id: CharID,
    credor_weight: float = None,
    debtor_weight: float = None,
    _world_cred: float = None,
    _world_debt: float = None,
    _world_agenda_cred: float = None,
    _world_agenda_debt: float = None,
) -> CharLink:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return CharLink(
        char_id=char_id,
        credor_weight=credor_weight,
        debtor_weight=debtor_weight,
        _world_cred=_world_cred,
        _world_debt=_world_debt,
        _world_agenda_cred=_world_agenda_cred,
        _world_agenda_debt=_world_agenda_debt,
    )


@dataclass
class CharUnitExternalMetrics:
    internal_char_id: CharID = None
    credor_operational: bool = None
    debtor_operational: bool = None
