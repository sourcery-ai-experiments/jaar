from dataclasses import dataclass
from src._instrument.python import (
    get_empty_dict_if_none,
    get_1_if_None,
    get_dict_from_json,
    get_0_if_None,
)
from src._road.road import (
    OtherID,
    RoadUnit,
    default_road_delimiter_if_none,
    validate_roadnode,
)
from src.agenda.other import (
    OtherLink,
    otherlinks_get_from_dict,
    otherlink_shop,
    OtherUnit,
)
from src.agenda.meld import get_meld_weight


class InvalidBeliefException(Exception):
    pass


class BeliefID(str):  # Created to help track the concept
    pass


@dataclass
class BeliefCore:
    belief_id: BeliefID = None


@dataclass
class BeliefUnit(BeliefCore):
    _other_mirror: bool = None  # set by AgendaUnit.set_otherunit()
    _others: dict[OtherID:OtherLink] = None  # set by AgendaUnit.set_otherunit()
    _road_delimiter: str = None  # calculated by AgendaUnit.set_beliefunit
    # calculated by AgendaUnit.calc_agenda_metrics()
    _agenda_cred: float = None
    _agenda_debt: float = None
    _agenda_intent_cred: float = None
    _agenda_intent_debt: float = None

    def set_belief_id(self, belief_id: BeliefID = None):
        if belief_id != None:
            if self._other_mirror:
                self.belief_id = validate_roadnode(belief_id, self._road_delimiter)
            else:
                self.belief_id = validate_roadnode(
                    belief_id, self._road_delimiter, not_roadnode_required=True
                )

    def get_dict(self) -> dict[str:str]:
        x_dict = {"belief_id": self.belief_id}
        if self._other_mirror:
            x_dict["_other_mirror"] = self._other_mirror
        if self._others not in [{}, None]:
            x_dict["_others"] = self.get_others_dict()

        return x_dict

    def reset_agenda_cred_debt(self):
        self._agenda_cred = 0
        self._agenda_debt = 0
        self._agenda_intent_cred = 0
        self._agenda_intent_debt = 0
        for otherlink in self._others.values():
            otherlink.reset_agenda_cred_debt()

    def _set_otherlink_agenda_cred_debt(self):
        otherlinks_credor_weight_sum = sum(
            otherlink.credor_weight for otherlink in self._others.values()
        )
        otherlinks_debtor_weight_sum = sum(
            otherlink.debtor_weight for otherlink in self._others.values()
        )

        for otherlink in self._others.values():
            otherlink.set_agenda_cred_debt(
                otherlinks_credor_weight_sum=otherlinks_credor_weight_sum,
                otherlinks_debtor_weight_sum=otherlinks_debtor_weight_sum,
                belief_agenda_cred=self._agenda_cred,
                belief_agenda_debt=self._agenda_debt,
                belief_agenda_intent_cred=self._agenda_intent_cred,
                belief_agenda_intent_debt=self._agenda_intent_debt,
            )

    def clear_otherlinks(self):
        self._others = {}

    def get_others_dict(self) -> dict[str:str]:
        others_x_dict = {}
        for other in self._others.values():
            other_dict = other.get_dict()
            others_x_dict[other_dict["other_id"]] = other_dict
        return others_x_dict

    def set_otherlink(self, otherlink: OtherLink):
        self._others[otherlink.other_id] = otherlink

    def edit_otherlink(
        self, other_id: OtherID, credor_weight: int = None, debtor_weight: int = None
    ):
        x_otherlink = self.get_otherlink(other_id)
        if credor_weight != None:
            x_otherlink.credor_weight = credor_weight
        if debtor_weight != None:
            x_otherlink.debtor_weight = debtor_weight

    def get_otherlink(self, other_id: OtherID) -> OtherLink:
        return self._others.get(other_id)

    def otherlink_exists(self, otherlink_other_id: OtherID) -> bool:
        return self.get_otherlink(otherlink_other_id) != None

    def del_otherlink(self, other_id):
        self._others.pop(other_id)

    def _shift_otherlink(
        self, to_delete_other_id: OtherID, to_absorb_other_id: OtherID
    ):
        old_belief_otherlink = self.get_otherlink(to_delete_other_id)
        new_otherlink_credor_weight = old_belief_otherlink.credor_weight
        new_otherlink_debtor_weight = old_belief_otherlink.debtor_weight

        new_otherlink = self.get_otherlink(to_absorb_other_id)
        if new_otherlink != None:
            new_otherlink_credor_weight += new_otherlink.credor_weight
            new_otherlink_debtor_weight += new_otherlink.debtor_weight

        self.set_otherlink(
            otherlink=otherlink_shop(
                other_id=to_absorb_other_id,
                credor_weight=new_otherlink_credor_weight,
                debtor_weight=new_otherlink_debtor_weight,
            )
        )
        self.del_otherlink(other_id=to_delete_other_id)

    def meld(self, exterior_belief):
        self._meld_attributes_that_must_be_equal(exterior_belief=exterior_belief)
        self.meld_otherlinks(exterior_belief=exterior_belief)

    def meld_otherlinks(self, exterior_belief):
        for oba in exterior_belief._others.values():
            if self._others.get(oba.other_id) is None:
                self._others[oba.other_id] = oba
            else:
                self._others[oba.other_id].meld(oba)

    def _meld_attributes_that_must_be_equal(self, exterior_belief):
        xl = [("belief_id", self.belief_id, exterior_belief.belief_id)]
        while xl != []:
            attrs = xl.pop()
            if attrs[1] != attrs[2]:
                raise InvalidBeliefException(
                    f"Meld fail BeliefUnit {self.belief_id} .{attrs[0]}='{attrs[1]}' not the equal as .{attrs[0]}='{attrs[2]}"
                )

        # if self.belief_id != exterior_belief.belief_id:
        #     raise InvalidBeliefException(
        #             f"Meld fail idea={self.get_road()} {attrs[0]}:{attrs[1]} with {exterior_idea.get_road()} {attrs[0]}:{attrs[2]}"
        #     )


# class BeliefUnitsshop:
def get_from_json(beliefunits_json: str) -> dict[BeliefID:BeliefUnit]:
    beliefunits_dict = get_dict_from_json(json_x=beliefunits_json)
    return get_beliefunits_from_dict(x_dict=beliefunits_dict)


def get_beliefunits_from_dict(
    x_dict: dict, _road_delimiter: str = None
) -> dict[BeliefID:BeliefUnit]:
    beliefunits = {}
    for beliefunit_dict in x_dict.values():
        x_belief = get_beliefunit_from_dict(beliefunit_dict, _road_delimiter)
        beliefunits[x_belief.belief_id] = x_belief
    return beliefunits


def get_beliefunit_from_dict(
    beliefunit_dict: dict, _road_delimiter: str = None
) -> BeliefUnit:
    return beliefunit_shop(
        belief_id=beliefunit_dict["belief_id"],
        _other_mirror=get_obj_from_beliefunit_dict(beliefunit_dict, "_other_mirror"),
        _others=get_obj_from_beliefunit_dict(beliefunit_dict, "_others"),
        _road_delimiter=_road_delimiter,
    )


def get_obj_from_beliefunit_dict(x_dict: dict[str:], dict_key: str) -> any:
    if dict_key == "_others":
        return otherlinks_get_from_dict(x_dict.get(dict_key))
    elif dict_key in {"_other_mirror"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else False
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None


def beliefunit_shop(
    belief_id: BeliefID,
    _other_mirror: bool = None,
    _others: dict[OtherID:OtherLink] = None,
    _road_delimiter: str = None,
) -> BeliefUnit:
    if _other_mirror is None:
        _other_mirror = False
    x_beliefunit = BeliefUnit(
        _other_mirror=_other_mirror,
        _others=get_empty_dict_if_none(_others),
        _agenda_cred=get_0_if_None(),
        _agenda_debt=get_0_if_None(),
        _agenda_intent_cred=get_0_if_None(),
        _agenda_intent_debt=get_0_if_None(),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    x_beliefunit.set_belief_id(belief_id=belief_id)
    return x_beliefunit


@dataclass
class BalanceLink(BeliefCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0

    def get_dict(self) -> dict[str:str]:
        return {
            "belief_id": self.belief_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def meld(
        self,
        exterior_balancelink,
        exterior_meld_strategy: str,
        src_meld_strategy: str,
    ):
        self.credor_weight = get_meld_weight(
            src_weight=self.credor_weight,
            src_meld_strategy=src_meld_strategy,
            exterior_weight=exterior_balancelink.credor_weight,
            exterior_meld_strategy=exterior_meld_strategy,
        )
        self.debtor_weight = get_meld_weight(
            src_weight=self.debtor_weight,
            src_meld_strategy=src_meld_strategy,
            exterior_weight=exterior_balancelink.debtor_weight,
            exterior_meld_strategy=exterior_meld_strategy,
        )


# class BalanceLinksshop:
def balancelinks_get_from_json(balancelinks_json: str) -> dict[BeliefID, BalanceLink]:
    balancelinks_dict = get_dict_from_json(json_x=balancelinks_json)
    return balancelinks_get_from_dict(x_dict=balancelinks_dict)


def balancelinks_get_from_dict(x_dict: dict) -> dict[BeliefID, BalanceLink]:
    balancelinks = {}
    for balancelinks_dict in x_dict.values():
        x_belief = balancelink_shop(
            belief_id=balancelinks_dict["belief_id"],
            credor_weight=balancelinks_dict["credor_weight"],
            debtor_weight=balancelinks_dict["debtor_weight"],
        )
        balancelinks[x_belief.belief_id] = x_belief
    return balancelinks


def balancelink_shop(
    belief_id: BeliefID, credor_weight: float = None, debtor_weight: float = None
) -> BalanceLink:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return BalanceLink(
        belief_id=belief_id, credor_weight=credor_weight, debtor_weight=debtor_weight
    )


@dataclass
class BalanceHeir(BeliefCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0
    _agenda_cred: float = None
    _agenda_debt: float = None

    def set_agenda_cred_debt(
        self,
        idea_agenda_importance,
        balanceheirs_credor_weight_sum: float,
        balanceheirs_debtor_weight_sum: float,
    ):
        self._agenda_cred = idea_agenda_importance * (
            self.credor_weight / balanceheirs_credor_weight_sum
        )
        self._agenda_debt = idea_agenda_importance * (
            self.debtor_weight / balanceheirs_debtor_weight_sum
        )


def balanceheir_shop(
    belief_id: BeliefID,
    credor_weight: float = None,
    debtor_weight: float = None,
    _agenda_cred: float = None,
    _agenda_debt: float = None,
) -> BalanceHeir:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return BalanceHeir(
        belief_id=belief_id,
        credor_weight=credor_weight,
        debtor_weight=debtor_weight,
        _agenda_cred=_agenda_cred,
        _agenda_debt=_agenda_debt,
    )


@dataclass
class BalanceLine(BeliefCore):
    _agenda_cred: float = None
    _agenda_debt: float = None

    def add_agenda_cred_debt(self, agenda_cred: float, agenda_debt: float):
        self.set_agenda_cred_debt_zero_if_null()
        self._agenda_cred += agenda_cred
        self._agenda_debt += agenda_debt

    def set_agenda_cred_debt_zero_if_null(self):
        if self._agenda_cred is None:
            self._agenda_cred = 0
        if self._agenda_debt is None:
            self._agenda_debt = 0


def balanceline_shop(belief_id: BeliefID, _agenda_cred: float, _agenda_debt: float):
    return BalanceLine(
        belief_id=belief_id, _agenda_cred=_agenda_cred, _agenda_debt=_agenda_debt
    )


def get_intersection_of_others(
    others_x: dict[OtherID:OtherUnit], others_y: dict[OtherID:OtherUnit]
) -> dict[OtherID:-1]:
    x_set = set(others_x)
    y_set = set(others_y)
    intersection_x = x_set.intersection(y_set)
    return {other_id_x: -1 for other_id_x in intersection_x}


def get_others_relevant_beliefs(
    beliefs_x: dict[BeliefID:BeliefUnit], others_x: dict[OtherID:OtherUnit]
) -> dict[BeliefID:{OtherID: -1}]:
    relevant_beliefs = {}
    for other_id_x in others_x:
        for belief_x in beliefs_x.values():
            if belief_x._others.get(other_id_x) != None:
                if relevant_beliefs.get(belief_x.belief_id) is None:
                    relevant_beliefs[belief_x.belief_id] = {}
                relevant_beliefs.get(belief_x.belief_id)[other_id_x] = -1

    return relevant_beliefs


def get_other_relevant_beliefs(
    beliefs_x: dict[BeliefID:BeliefUnit], other_id_x: OtherID
) -> dict[BeliefID:-1]:
    return {
        belief_x.belief_id: -1
        for belief_x in beliefs_x.values()
        if belief_x._others.get(other_id_x) != None
    }
