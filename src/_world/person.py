from src._instrument.python import get_1_if_None, get_dict_from_json, get_0_if_None
from src._road.road import PersonID, default_road_delimiter_if_none, validate_roadnode
from src._road.finance import default_pixel_if_none
from src._world.belieflink import BeliefID, BeliefLink, belieflinks_get_from_dict
from dataclasses import dataclass


class InvalidPersonException(Exception):
    pass


class _pixel_RatioException(Exception):
    pass


@dataclass
class PersonCore:
    person_id: PersonID = None
    _road_delimiter: str = None
    _pixel: float = None

    def set_person_id(self, x_person_id: PersonID):
        self.person_id = validate_roadnode(x_person_id, self._road_delimiter)


@dataclass
class PersonUnit(PersonCore):
    """This represents the relationship from the WorldUnit._owner_id to the PersonUnit.person_id
    PersonUnit.credor_weight represents how much credor_weight the _owner_id gives the person_id
    PersonUnit.debtor_weight represents how much debtor_weight the _owner_id gives the person_id
    """

    credor_weight: int = None
    debtor_weight: int = None
    # calculated fields
    _belieflinks: dict[PersonID:BeliefLink] = None
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
        world_personunit_total_credor_weight: float,
        world_personunit_total_debtor_weight: float,
    ):
        if world_agenda_ratio_cred_sum == 0:
            self._world_agenda_ratio_cred = (
                self.get_credor_weight() / world_personunit_total_credor_weight
            )
        else:
            self._world_agenda_ratio_cred = (
                self._world_agenda_cred / world_agenda_ratio_cred_sum
            )

        if world_agenda_ratio_debt_sum == 0:
            self._world_agenda_ratio_debt = (
                self.get_debtor_weight() / world_personunit_total_debtor_weight
            )
        else:
            self._world_agenda_ratio_debt = (
                self._world_agenda_debt / world_agenda_ratio_debt_sum
            )

    def meld(self, exterior_personunit):
        if self.person_id != exterior_personunit.person_id:
            raise InvalidPersonException(
                f"Meld fail PersonUnit='{self.person_id}' not the equal as PersonUnit='{exterior_personunit.person_id}"
            )

        self.credor_weight += exterior_personunit.credor_weight
        self.debtor_weight += exterior_personunit.debtor_weight
        self._irrational_debtor_weight += exterior_personunit._irrational_debtor_weight
        self._inallocable_debtor_weight += (
            exterior_personunit._inallocable_debtor_weight
        )

    def set_belieflink(self, belieflink: BeliefLink):
        self._belieflinks[belieflink.belief_id] = belieflink

    def get_belieflink(self, belief_id: BeliefID) -> BeliefLink:
        return self._belieflinks.get(belief_id)

    def belieflink_exists(self, belief_id: BeliefID) -> bool:
        return self._belieflinks.get(belief_id) != None

    def delete_belieflink(self, belief_id: BeliefID):
        return self._belieflinks.pop(belief_id)

    def clear_belieflinks(self):
        self._belieflinks = {}

    def get_belieflinks_dict(self) -> dict:
        return {
            x_belieflink.belief_id: {
                "belief_id": x_belieflink.belief_id,
                "credor_weight": x_belieflink.credor_weight,
                "debtor_weight": x_belieflink.debtor_weight,
            }
            for x_belieflink in self._belieflinks.values()
        }

    def get_dict(self, all_attrs: bool = False) -> dict[str:str]:
        x_dict = {
            "person_id": self.person_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
            "_belieflinks": self.get_belieflinks_dict(),
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


# class PersonUnitsshop:
def personunits_get_from_json(personunits_json: str) -> dict[str:PersonUnit]:
    personunits_dict = get_dict_from_json(json_x=personunits_json)
    return personunits_get_from_dict(x_dict=personunits_dict)


def personunits_get_from_dict(
    x_dict: dict, _road_delimiter: str = None
) -> dict[str:PersonUnit]:
    personunits = {}
    for personunit_dict in x_dict.values():
        x_personunit = personunit_get_from_dict(personunit_dict, _road_delimiter)
        personunits[x_personunit.person_id] = x_personunit
    return personunits


def personunit_get_from_dict(personunit_dict: dict, _road_delimiter: str) -> PersonUnit:
    _irrational_debtor_weight = personunit_dict.get("_irrational_debtor_weight", 0)
    _inallocable_debtor_weight = personunit_dict.get("_inallocable_debtor_weight", 0)
    _treasury_due_paid = personunit_dict.get("_treasury_due_paid", 0)
    _treasury_due_diff = personunit_dict.get("_treasury_due_diff", 0)
    _treasury_cred_score = personunit_dict.get("_treasury_cred_score", 0)
    _treasury_voice_rank = personunit_dict.get("_treasury_voice_rank", 0)
    _treasury_voice_hx_lowest_rank = personunit_dict.get(
        "_treasury_voice_hx_lowest_rank", 0
    )
    x_personunit = personunit_shop(
        person_id=personunit_dict["person_id"],
        credor_weight=personunit_dict["credor_weight"],
        debtor_weight=personunit_dict["debtor_weight"],
        _credor_operational=personunit_dict["_credor_operational"],
        _debtor_operational=personunit_dict["_debtor_operational"],
        _road_delimiter=_road_delimiter,
    )
    x_personunit._belieflinks = belieflinks_get_from_dict(
        personunit_dict["_belieflinks"]
    )
    x_personunit.set_treasury_attr(
        _treasury_due_paid=_treasury_due_paid,
        _treasury_due_diff=_treasury_due_diff,
        cred_score=_treasury_cred_score,
        voice_rank=_treasury_voice_rank,
    )
    x_personunit._set_treasury_voice_hx_lowest_rank(_treasury_voice_hx_lowest_rank)
    x_personunit.add_irrational_debtor_weight(get_0_if_None(_irrational_debtor_weight))
    x_personunit.add_inallocable_debtor_weight(
        get_0_if_None(_inallocable_debtor_weight)
    )

    return x_personunit


def personunit_shop(
    person_id: PersonID,
    credor_weight: int = None,
    debtor_weight: int = None,
    _credor_operational: bool = None,
    _debtor_operational: bool = None,
    _road_delimiter: str = None,
    _pixel: float = None,
) -> PersonUnit:
    x_personunit = PersonUnit(
        credor_weight=get_1_if_None(credor_weight),
        debtor_weight=get_1_if_None(debtor_weight),
        _belieflinks={},
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
    x_personunit.set_person_id(x_person_id=person_id)
    return x_personunit


@dataclass
class PersonLink(PersonCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0
    _world_cred: float = None
    _world_debt: float = None
    _world_agenda_cred: float = None
    _world_agenda_debt: float = None

    def get_dict(self) -> dict[str:str]:
        return {
            "person_id": self.person_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def set_world_cred_debt(
        self,
        personlinks_credor_weight_sum: float,
        personlinks_debtor_weight_sum: float,
        belief_world_cred: float,
        belief_world_debt: float,
        belief_world_agenda_cred: float,
        belief_world_agenda_debt: float,
    ):
        belief_world_cred = get_1_if_None(belief_world_cred)
        belief_world_debt = get_1_if_None(belief_world_debt)
        credor_ratio = self.credor_weight / personlinks_credor_weight_sum
        debtor_ratio = self.debtor_weight / personlinks_debtor_weight_sum

        self._world_cred = belief_world_cred * credor_ratio
        self._world_debt = belief_world_debt * debtor_ratio
        self._world_agenda_cred = belief_world_agenda_cred * credor_ratio
        self._world_agenda_debt = belief_world_agenda_debt * debtor_ratio

    def reset_world_cred_debt(self):
        self._world_cred = 0
        self._world_debt = 0
        self._world_agenda_cred = 0
        self._world_agenda_debt = 0

    def meld(self, exterior_personlink):
        if self.person_id != exterior_personlink.person_id:
            raise InvalidPersonException(
                f"Meld fail PersonLink='{self.person_id}' not the equal as PersonLink='{exterior_personlink.person_id}"
            )
        self.credor_weight += exterior_personlink.credor_weight
        self.debtor_weight += exterior_personlink.debtor_weight


def personlinks_get_from_json(personlinks_json: str) -> dict[str:PersonLink]:
    personlinks_dict = get_dict_from_json(json_x=personlinks_json)
    return personlinks_get_from_dict(x_dict=personlinks_dict)


def personlinks_get_from_dict(x_dict: dict) -> dict[str:PersonLink]:
    if x_dict is None:
        x_dict = {}
    personlinks = {}
    for personlinks_dict in x_dict.values():
        x_person = personlink_shop(
            person_id=personlinks_dict["person_id"],
            credor_weight=personlinks_dict["credor_weight"],
            debtor_weight=personlinks_dict["debtor_weight"],
        )
        personlinks[x_person.person_id] = x_person
    return personlinks


def personlink_shop(
    person_id: PersonID,
    credor_weight: float = None,
    debtor_weight: float = None,
    _world_cred: float = None,
    _world_debt: float = None,
    _world_agenda_cred: float = None,
    _world_agenda_debt: float = None,
) -> PersonLink:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return PersonLink(
        person_id=person_id,
        credor_weight=credor_weight,
        debtor_weight=debtor_weight,
        _world_cred=_world_cred,
        _world_debt=_world_debt,
        _world_agenda_cred=_world_agenda_cred,
        _world_agenda_debt=_world_agenda_debt,
    )


@dataclass
class PersonUnitExternalMetrics:
    internal_person_id: PersonID = None
    credor_operational: bool = None
    debtor_operational: bool = None
