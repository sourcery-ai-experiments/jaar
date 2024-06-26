from dataclasses import dataclass
from src._instrument.python import (
    get_empty_dict_if_none,
    get_1_if_None,
    get_dict_from_json,
    get_0_if_None,
)
from src._road.road import (
    PersonID,
    RoadUnit,
    default_road_delimiter_if_none,
    validate_roadnode,
)
from src._world.person import (
    PersonLink,
    personlinks_get_from_dict,
    personlink_shop,
    PersonUnit,
)
from src._world.meld import get_meld_weight


class InvalidBeliefException(Exception):
    pass


class BeliefID(str):  # Created to help track the concept
    pass


@dataclass
class BeliefCore:
    belief_id: BeliefID = None


@dataclass
class BeliefUnit(BeliefCore):
    _person_mirror: bool = None  # set by WorldUnit.set_personunit()
    _persons: dict[PersonID:PersonLink] = None  # set by WorldUnit.set_personunit()
    _road_delimiter: str = None  # calculated by WorldUnit.set_beliefunit
    # calculated by WorldUnit.calc_world_metrics()
    _world_cred: float = None
    _world_debt: float = None
    _world_agenda_cred: float = None
    _world_agenda_debt: float = None

    def set_belief_id(self, belief_id: BeliefID = None):
        if belief_id != None:
            if self._person_mirror:
                self.belief_id = validate_roadnode(belief_id, self._road_delimiter)
            else:
                self.belief_id = validate_roadnode(
                    belief_id, self._road_delimiter, not_roadnode_required=True
                )

    def get_dict(self) -> dict[str:str]:
        x_dict = {"belief_id": self.belief_id}
        if self._person_mirror:
            x_dict["_person_mirror"] = self._person_mirror
        if self._persons not in [{}, None]:
            x_dict["_persons"] = self.get_persons_dict()

        return x_dict

    def reset_world_cred_debt(self):
        self._world_cred = 0
        self._world_debt = 0
        self._world_agenda_cred = 0
        self._world_agenda_debt = 0
        for personlink in self._persons.values():
            personlink.reset_world_cred_debt()

    def _set_personlink_world_cred_debt(self):
        personlinks_credor_weight_sum = sum(
            personlink.credor_weight for personlink in self._persons.values()
        )
        personlinks_debtor_weight_sum = sum(
            personlink.debtor_weight for personlink in self._persons.values()
        )

        for personlink in self._persons.values():
            personlink.set_world_cred_debt(
                personlinks_credor_weight_sum=personlinks_credor_weight_sum,
                personlinks_debtor_weight_sum=personlinks_debtor_weight_sum,
                belief_world_cred=self._world_cred,
                belief_world_debt=self._world_debt,
                belief_world_agenda_cred=self._world_agenda_cred,
                belief_world_agenda_debt=self._world_agenda_debt,
            )

    def clear_personlinks(self):
        self._persons = {}

    def get_persons_dict(self) -> dict[str:str]:
        persons_x_dict = {}
        for person in self._persons.values():
            person_dict = person.get_dict()
            persons_x_dict[person_dict["person_id"]] = person_dict
        return persons_x_dict

    def set_personlink(self, personlink: PersonLink):
        self._persons[personlink.person_id] = personlink

    def edit_personlink(
        self, person_id: PersonID, credor_weight: int = None, debtor_weight: int = None
    ):
        x_personlink = self.get_personlink(person_id)
        if credor_weight != None:
            x_personlink.credor_weight = credor_weight
        if debtor_weight != None:
            x_personlink.debtor_weight = debtor_weight

    def get_personlink(self, person_id: PersonID) -> PersonLink:
        return self._persons.get(person_id)

    def personlink_exists(self, personlink_person_id: PersonID) -> bool:
        return self.get_personlink(personlink_person_id) != None

    def del_personlink(self, person_id):
        self._persons.pop(person_id)

    def _shift_personlink(
        self, to_delete_person_id: PersonID, to_absorb_person_id: PersonID
    ):
        old_belief_personlink = self.get_personlink(to_delete_person_id)
        new_personlink_credor_weight = old_belief_personlink.credor_weight
        new_personlink_debtor_weight = old_belief_personlink.debtor_weight

        new_personlink = self.get_personlink(to_absorb_person_id)
        if new_personlink != None:
            new_personlink_credor_weight += new_personlink.credor_weight
            new_personlink_debtor_weight += new_personlink.debtor_weight

        self.set_personlink(
            personlink=personlink_shop(
                person_id=to_absorb_person_id,
                credor_weight=new_personlink_credor_weight,
                debtor_weight=new_personlink_debtor_weight,
            )
        )
        self.del_personlink(person_id=to_delete_person_id)

    def meld(self, exterior_belief):
        self._meld_attributes_that_must_be_equal(exterior_belief=exterior_belief)
        self.meld_personlinks(exterior_belief=exterior_belief)

    def meld_personlinks(self, exterior_belief):
        for oba in exterior_belief._persons.values():
            if self._persons.get(oba.person_id) is None:
                self._persons[oba.person_id] = oba
            else:
                self._persons[oba.person_id].meld(oba)

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
        _person_mirror=get_obj_from_beliefunit_dict(beliefunit_dict, "_person_mirror"),
        _persons=get_obj_from_beliefunit_dict(beliefunit_dict, "_persons"),
        _road_delimiter=_road_delimiter,
    )


def get_obj_from_beliefunit_dict(x_dict: dict[str:], dict_key: str) -> any:
    if dict_key == "_persons":
        return personlinks_get_from_dict(x_dict.get(dict_key))
    elif dict_key in {"_person_mirror"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else False
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None


def beliefunit_shop(
    belief_id: BeliefID,
    _person_mirror: bool = None,
    _persons: dict[PersonID:PersonLink] = None,
    _road_delimiter: str = None,
) -> BeliefUnit:
    if _person_mirror is None:
        _person_mirror = False
    x_beliefunit = BeliefUnit(
        _person_mirror=_person_mirror,
        _persons=get_empty_dict_if_none(_persons),
        _world_cred=get_0_if_None(),
        _world_debt=get_0_if_None(),
        _world_agenda_cred=get_0_if_None(),
        _world_agenda_debt=get_0_if_None(),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    x_beliefunit.set_belief_id(belief_id=belief_id)
    return x_beliefunit


@dataclass
class BeliefLink(BeliefCore):
    credor_weight: float = 1.0
    debtor_weight: float = 1.0

    def get_dict(self) -> dict[str:str]:
        return {
            "belief_id": self.belief_id,
            "credor_weight": self.credor_weight,
            "debtor_weight": self.debtor_weight,
        }


def belieflink_shop(
    belief_id: BeliefID, credor_weight: float = None, debtor_weight: float = None
) -> BeliefLink:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return BeliefLink(
        belief_id=belief_id, credor_weight=credor_weight, debtor_weight=debtor_weight
    )


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
    _world_cred: float = None
    _world_debt: float = None

    def set_world_cred_debt(
        self,
        idea_world_importance,
        balanceheirs_credor_weight_sum: float,
        balanceheirs_debtor_weight_sum: float,
    ):
        self._world_cred = idea_world_importance * (
            self.credor_weight / balanceheirs_credor_weight_sum
        )
        self._world_debt = idea_world_importance * (
            self.debtor_weight / balanceheirs_debtor_weight_sum
        )


def balanceheir_shop(
    belief_id: BeliefID,
    credor_weight: float = None,
    debtor_weight: float = None,
    _world_cred: float = None,
    _world_debt: float = None,
) -> BalanceHeir:
    credor_weight = get_1_if_None(credor_weight)
    debtor_weight = get_1_if_None(debtor_weight)
    return BalanceHeir(
        belief_id=belief_id,
        credor_weight=credor_weight,
        debtor_weight=debtor_weight,
        _world_cred=_world_cred,
        _world_debt=_world_debt,
    )


@dataclass
class BalanceLine(BeliefCore):
    _world_cred: float = None
    _world_debt: float = None

    def add_world_cred_debt(self, world_cred: float, world_debt: float):
        self.set_world_cred_debt_zero_if_null()
        self._world_cred += world_cred
        self._world_debt += world_debt

    def set_world_cred_debt_zero_if_null(self):
        if self._world_cred is None:
            self._world_cred = 0
        if self._world_debt is None:
            self._world_debt = 0


def balanceline_shop(belief_id: BeliefID, _world_cred: float, _world_debt: float):
    return BalanceLine(
        belief_id=belief_id, _world_cred=_world_cred, _world_debt=_world_debt
    )


def get_intersection_of_persons(
    persons_x: dict[PersonID:PersonUnit], persons_y: dict[PersonID:PersonUnit]
) -> dict[PersonID:-1]:
    x_set = set(persons_x)
    y_set = set(persons_y)
    intersection_x = x_set.intersection(y_set)
    return {person_id_x: -1 for person_id_x in intersection_x}


def get_persons_relevant_beliefs(
    beliefs_x: dict[BeliefID:BeliefUnit], persons_x: dict[PersonID:PersonUnit]
) -> dict[BeliefID:{PersonID: -1}]:
    relevant_beliefs = {}
    for person_id_x in persons_x:
        for belief_x in beliefs_x.values():
            if belief_x._persons.get(person_id_x) != None:
                if relevant_beliefs.get(belief_x.belief_id) is None:
                    relevant_beliefs[belief_x.belief_id] = {}
                relevant_beliefs.get(belief_x.belief_id)[person_id_x] = -1

    return relevant_beliefs


def get_person_relevant_beliefs(
    beliefs_x: dict[BeliefID:BeliefUnit], person_id_x: PersonID
) -> dict[BeliefID:-1]:
    return {
        belief_x.belief_id: -1
        for belief_x in beliefs_x.values()
        if belief_x._persons.get(person_id_x) != None
    }
