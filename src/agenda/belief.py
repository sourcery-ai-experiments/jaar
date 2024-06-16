from dataclasses import dataclass
from src._instrument.python import (
    get_empty_dict_if_none,
    get_1_if_None,
    get_dict_from_json,
    get_0_if_None,
)
from src._road.road import (
    GuyID,
    RoadUnit,
    default_road_delimiter_if_none,
    validate_roadnode,
)
from src.agenda.guy import (
    GuyLink,
    guylinks_get_from_dict,
    guylink_shop,
    GuyUnit,
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
    _guy_mirror: bool = None  # set by AgendaUnit.set_guyunit()
    _guys: dict[GuyID:GuyLink] = None  # set by AgendaUnit.set_guyunit()
    _road_delimiter: str = None  # calculated by AgendaUnit.set_beliefunit
    # calculated by AgendaUnit.calc_agenda_metrics()
    _agenda_cred: float = None
    _agenda_debt: float = None
    _agenda_intent_cred: float = None
    _agenda_intent_debt: float = None

    def set_belief_id(self, belief_id: BeliefID = None):
        if belief_id != None:
            if self._guy_mirror:
                self.belief_id = validate_roadnode(belief_id, self._road_delimiter)
            else:
                self.belief_id = validate_roadnode(
                    belief_id, self._road_delimiter, not_roadnode_required=True
                )

    def get_dict(self) -> dict[str:str]:
        x_dict = {"belief_id": self.belief_id}
        if self._guy_mirror:
            x_dict["_guy_mirror"] = self._guy_mirror
        if self._guys not in [{}, None]:
            x_dict["_guys"] = self.get_guys_dict()

        return x_dict

    def reset_agenda_cred_debt(self):
        self._agenda_cred = 0
        self._agenda_debt = 0
        self._agenda_intent_cred = 0
        self._agenda_intent_debt = 0
        for guylink in self._guys.values():
            guylink.reset_agenda_cred_debt()

    def _set_guylink_agenda_cred_debt(self):
        guylinks_credor_weight_sum = sum(
            guylink.credor_weight for guylink in self._guys.values()
        )
        guylinks_debtor_weight_sum = sum(
            guylink.debtor_weight for guylink in self._guys.values()
        )

        for guylink in self._guys.values():
            guylink.set_agenda_cred_debt(
                guylinks_credor_weight_sum=guylinks_credor_weight_sum,
                guylinks_debtor_weight_sum=guylinks_debtor_weight_sum,
                belief_agenda_cred=self._agenda_cred,
                belief_agenda_debt=self._agenda_debt,
                belief_agenda_intent_cred=self._agenda_intent_cred,
                belief_agenda_intent_debt=self._agenda_intent_debt,
            )

    def clear_guylinks(self):
        self._guys = {}

    def get_guys_dict(self) -> dict[str:str]:
        guys_x_dict = {}
        for guy in self._guys.values():
            guy_dict = guy.get_dict()
            guys_x_dict[guy_dict["guy_id"]] = guy_dict
        return guys_x_dict

    def set_guylink(self, guylink: GuyLink):
        self._guys[guylink.guy_id] = guylink

    def edit_guylink(
        self, guy_id: GuyID, credor_weight: int = None, debtor_weight: int = None
    ):
        x_guylink = self.get_guylink(guy_id)
        if credor_weight != None:
            x_guylink.credor_weight = credor_weight
        if debtor_weight != None:
            x_guylink.debtor_weight = debtor_weight

    def get_guylink(self, guy_id: GuyID) -> GuyLink:
        return self._guys.get(guy_id)

    def guylink_exists(self, guylink_guy_id: GuyID) -> bool:
        return self.get_guylink(guylink_guy_id) != None

    def del_guylink(self, guy_id):
        self._guys.pop(guy_id)

    def _shift_guylink(self, to_delete_guy_id: GuyID, to_absorb_guy_id: GuyID):
        old_belief_guylink = self.get_guylink(to_delete_guy_id)
        new_guylink_credor_weight = old_belief_guylink.credor_weight
        new_guylink_debtor_weight = old_belief_guylink.debtor_weight

        new_guylink = self.get_guylink(to_absorb_guy_id)
        if new_guylink != None:
            new_guylink_credor_weight += new_guylink.credor_weight
            new_guylink_debtor_weight += new_guylink.debtor_weight

        self.set_guylink(
            guylink=guylink_shop(
                guy_id=to_absorb_guy_id,
                credor_weight=new_guylink_credor_weight,
                debtor_weight=new_guylink_debtor_weight,
            )
        )
        self.del_guylink(guy_id=to_delete_guy_id)

    def meld(self, other_belief):
        self._meld_attributes_that_must_be_equal(other_belief=other_belief)
        self.meld_guylinks(other_belief=other_belief)

    def meld_guylinks(self, other_belief):
        for oba in other_belief._guys.values():
            if self._guys.get(oba.guy_id) is None:
                self._guys[oba.guy_id] = oba
            else:
                self._guys[oba.guy_id].meld(oba)

    def _meld_attributes_that_must_be_equal(self, other_belief):
        xl = [("belief_id", self.belief_id, other_belief.belief_id)]
        while xl != []:
            attrs = xl.pop()
            if attrs[1] != attrs[2]:
                raise InvalidBeliefException(
                    f"Meld fail BeliefUnit {self.belief_id} .{attrs[0]}='{attrs[1]}' not the same as .{attrs[0]}='{attrs[2]}"
                )

        # if self.belief_id != other_belief.belief_id:
        #     raise InvalidBeliefException(
        #             f"Meld fail idea={self.get_road()} {attrs[0]}:{attrs[1]} with {other_idea.get_road()} {attrs[0]}:{attrs[2]}"
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
        _guy_mirror=get_obj_from_beliefunit_dict(beliefunit_dict, "_guy_mirror"),
        _guys=get_obj_from_beliefunit_dict(beliefunit_dict, "_guys"),
        _road_delimiter=_road_delimiter,
    )


def get_obj_from_beliefunit_dict(x_dict: dict[str:], dict_key: str) -> any:
    if dict_key == "_guys":
        return guylinks_get_from_dict(x_dict.get(dict_key))
    elif dict_key in {"_guy_mirror"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else False
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None


def beliefunit_shop(
    belief_id: BeliefID,
    _guy_mirror: bool = None,
    _guys: dict[GuyID:GuyLink] = None,
    _road_delimiter: str = None,
) -> BeliefUnit:
    if _guy_mirror is None:
        _guy_mirror = False
    x_beliefunit = BeliefUnit(
        _guy_mirror=_guy_mirror,
        _guys=get_empty_dict_if_none(_guys),
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
        other_balancelink,
        other_meld_strategy: str,
        src_meld_strategy: str,
    ):
        self.credor_weight = get_meld_weight(
            src_weight=self.credor_weight,
            src_meld_strategy=src_meld_strategy,
            other_weight=other_balancelink.credor_weight,
            other_meld_strategy=other_meld_strategy,
        )
        self.debtor_weight = get_meld_weight(
            src_weight=self.debtor_weight,
            src_meld_strategy=src_meld_strategy,
            other_weight=other_balancelink.debtor_weight,
            other_meld_strategy=other_meld_strategy,
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


def get_intersection_of_guys(
    guys_x: dict[GuyID:GuyUnit], guys_y: dict[GuyID:GuyUnit]
) -> dict[GuyID:-1]:
    x_set = set(guys_x)
    y_set = set(guys_y)
    intersection_x = x_set.intersection(y_set)
    return {guy_id_x: -1 for guy_id_x in intersection_x}


def get_guys_relevant_beliefs(
    beliefs_x: dict[BeliefID:BeliefUnit], guys_x: dict[GuyID:GuyUnit]
) -> dict[BeliefID:{GuyID: -1}]:
    relevant_beliefs = {}
    for guy_id_x in guys_x:
        for belief_x in beliefs_x.values():
            if belief_x._guys.get(guy_id_x) != None:
                if relevant_beliefs.get(belief_x.belief_id) is None:
                    relevant_beliefs[belief_x.belief_id] = {}
                relevant_beliefs.get(belief_x.belief_id)[guy_id_x] = -1

    return relevant_beliefs


def get_guy_relevant_beliefs(
    beliefs_x: dict[BeliefID:BeliefUnit], guy_id_x: GuyID
) -> dict[BeliefID:-1]:
    return {
        belief_x.belief_id: -1
        for belief_x in beliefs_x.values()
        if belief_x._guys.get(guy_id_x) != None
    }
