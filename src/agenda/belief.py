from dataclasses import dataclass
from src._instrument.python import (
    get_empty_dict_if_none,
    get_1_if_None,
    get_dict_from_json,
    get_0_if_None,
)
from src._road.road import (
    PartyID,
    RoadUnit,
    default_road_delimiter_if_none,
    validate_roadnode,
)
from src.agenda.party import (
    PartyLink,
    partylinks_get_from_dict,
    partylink_shop,
    PartyUnit,
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
    _party_mirror: bool = None  # set by AgendaUnit.set_partyunit()
    _partys: dict[PartyID:PartyLink] = None  # set by AgendaUnit.set_partyunit()
    _road_delimiter: str = None  # calculated by AgendaUnit.set_beliefunit
    # calculated by AgendaUnit.calc_agenda_metrics()
    _agenda_cred: float = None
    _agenda_debt: float = None
    _agenda_intent_cred: float = None
    _agenda_intent_debt: float = None

    def set_belief_id(self, belief_id: BeliefID = None):
        if belief_id != None:
            if self._party_mirror:
                self.belief_id = validate_roadnode(belief_id, self._road_delimiter)
            else:
                self.belief_id = validate_roadnode(
                    belief_id, self._road_delimiter, not_roadnode_required=True
                )

    def get_dict(self) -> dict[str:str]:
        x_dict = {"belief_id": self.belief_id}
        if self._party_mirror:
            x_dict["_party_mirror"] = self._party_mirror
        if self._partys not in [{}, None]:
            x_dict["_partys"] = self.get_partys_dict()

        return x_dict

    def reset_agenda_cred_debt(self):
        self._agenda_cred = 0
        self._agenda_debt = 0
        self._agenda_intent_cred = 0
        self._agenda_intent_debt = 0
        for partylink in self._partys.values():
            partylink.reset_agenda_cred_debt()

    def _set_partylink_agenda_cred_debt(self):
        partylinks_credor_weight_sum = sum(
            partylink.credor_weight for partylink in self._partys.values()
        )
        partylinks_debtor_weight_sum = sum(
            partylink.debtor_weight for partylink in self._partys.values()
        )

        for partylink in self._partys.values():
            partylink.set_agenda_cred_debt(
                partylinks_credor_weight_sum=partylinks_credor_weight_sum,
                partylinks_debtor_weight_sum=partylinks_debtor_weight_sum,
                belief_agenda_cred=self._agenda_cred,
                belief_agenda_debt=self._agenda_debt,
                belief_agenda_intent_cred=self._agenda_intent_cred,
                belief_agenda_intent_debt=self._agenda_intent_debt,
            )

    def clear_partylinks(self):
        self._partys = {}

    def get_partys_dict(self) -> dict[str:str]:
        partys_x_dict = {}
        for party in self._partys.values():
            party_dict = party.get_dict()
            partys_x_dict[party_dict["party_id"]] = party_dict
        return partys_x_dict

    def set_partylink(self, partylink: PartyLink):
        self._partys[partylink.party_id] = partylink

    def edit_partylink(
        self, party_id: PartyID, credor_weight: int = None, debtor_weight: int = None
    ):
        x_partylink = self.get_partylink(party_id)
        if credor_weight != None:
            x_partylink.credor_weight = credor_weight
        if debtor_weight != None:
            x_partylink.debtor_weight = debtor_weight

    def get_partylink(self, party_id: PartyID) -> PartyLink:
        return self._partys.get(party_id)

    def partylink_exists(self, partylink_party_id: PartyID) -> bool:
        return self.get_partylink(partylink_party_id) != None

    def del_partylink(self, party_id):
        self._partys.pop(party_id)

    def _shift_partylink(
        self, to_delete_party_id: PartyID, to_absorb_party_id: PartyID
    ):
        old_belief_partylink = self.get_partylink(to_delete_party_id)
        new_partylink_credor_weight = old_belief_partylink.credor_weight
        new_partylink_debtor_weight = old_belief_partylink.debtor_weight

        new_partylink = self.get_partylink(to_absorb_party_id)
        if new_partylink != None:
            new_partylink_credor_weight += new_partylink.credor_weight
            new_partylink_debtor_weight += new_partylink.debtor_weight

        self.set_partylink(
            partylink=partylink_shop(
                party_id=to_absorb_party_id,
                credor_weight=new_partylink_credor_weight,
                debtor_weight=new_partylink_debtor_weight,
            )
        )
        self.del_partylink(party_id=to_delete_party_id)

    def meld(self, other_belief):
        self._meld_attributes_that_must_be_equal(other_belief=other_belief)
        self.meld_partylinks(other_belief=other_belief)

    def meld_partylinks(self, other_belief):
        for oba in other_belief._partys.values():
            if self._partys.get(oba.party_id) is None:
                self._partys[oba.party_id] = oba
            else:
                self._partys[oba.party_id].meld(oba)

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
        _party_mirror=get_obj_from_beliefunit_dict(beliefunit_dict, "_party_mirror"),
        _partys=get_obj_from_beliefunit_dict(beliefunit_dict, "_partys"),
        _road_delimiter=_road_delimiter,
    )


def get_obj_from_beliefunit_dict(x_dict: dict[str:], dict_key: str) -> any:
    if dict_key == "_partys":
        return partylinks_get_from_dict(x_dict.get(dict_key))
    elif dict_key in {"_party_mirror"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else False
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None


def beliefunit_shop(
    belief_id: BeliefID,
    _party_mirror: bool = None,
    _partys: dict[PartyID:PartyLink] = None,
    _road_delimiter: str = None,
) -> BeliefUnit:
    if _party_mirror is None:
        _party_mirror = False
    x_beliefunit = BeliefUnit(
        _party_mirror=_party_mirror,
        _partys=get_empty_dict_if_none(_partys),
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


def get_intersection_of_partys(
    partys_x: dict[PartyID:PartyUnit], partys_y: dict[PartyID:PartyUnit]
) -> dict[PartyID:-1]:
    x_set = set(partys_x)
    y_set = set(partys_y)
    intersection_x = x_set.intersection(y_set)
    return {party_id_x: -1 for party_id_x in intersection_x}


def get_partys_relevant_beliefs(
    beliefs_x: dict[BeliefID:BeliefUnit], partys_x: dict[PartyID:PartyUnit]
) -> dict[BeliefID:{PartyID: -1}]:
    relevant_beliefs = {}
    for party_id_x in partys_x:
        for belief_x in beliefs_x.values():
            if belief_x._partys.get(party_id_x) != None:
                if relevant_beliefs.get(belief_x.belief_id) is None:
                    relevant_beliefs[belief_x.belief_id] = {}
                relevant_beliefs.get(belief_x.belief_id)[party_id_x] = -1

    return relevant_beliefs


def get_party_relevant_beliefs(
    beliefs_x: dict[BeliefID:BeliefUnit], party_id_x: PartyID
) -> dict[BeliefID:-1]:
    return {
        belief_x.belief_id: -1
        for belief_x in beliefs_x.values()
        if belief_x._partys.get(party_id_x) != None
    }
