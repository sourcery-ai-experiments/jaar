from dataclasses import dataclass
from src.agenda.belief import BeliefUnit, BeliefID
from src.agenda.other import OtherID


class InvalidAssignHeirPopulateException(Exception):
    pass


@dataclass
class AssignedUnit:
    _suffbeliefs: dict[BeliefID:BeliefID]

    def get_dict(self) -> dict[str:str]:
        _suffbeliefs = {
            x_belief_id: x_belief_id  # premise.get_dict()
            for x_belief_id, _suffbelief in self._suffbeliefs.items()
        }
        return {"_suffbeliefs": _suffbeliefs}

    def set_suffbelief(self, belief_id: BeliefID):
        self._suffbeliefs[belief_id] = -1

    def suffbelief_exists(self, belief_id: BeliefID):
        return self._suffbeliefs.get(belief_id) != None

    def del_suffbelief(self, belief_id: BeliefID):
        self._suffbeliefs.pop(belief_id)

    def get_suffbelief(self, belief_id: BeliefID) -> BeliefID:
        return self._suffbeliefs.get(belief_id)


def assignedunit_shop(_suffbeliefs: dict[BeliefID:BeliefID] = None) -> AssignedUnit:
    if _suffbeliefs is None:
        _suffbeliefs = {}

    return AssignedUnit(_suffbeliefs=_suffbeliefs)


def create_assignedunit(suffbelief: BeliefID):
    x_assignedunit = assignedunit_shop()
    x_assignedunit.set_suffbelief(suffbelief)
    return x_assignedunit


@dataclass
class AssignedHeir:
    _suffbeliefs: dict[BeliefID:BeliefID]
    _owner_id_assigned: bool

    def _get_all_others(
        self,
        agenda_beliefs: dict[BeliefID:BeliefUnit],
        belief_id_dict: dict[BeliefID:],
    ) -> dict[BeliefID:BeliefUnit]:
        dict_x = {}
        for belief_id_x in belief_id_dict:
            dict_x |= agenda_beliefs.get(belief_id_x)._others
        return dict_x

    def _get_all_suff_others(
        self, agenda_beliefs: dict[BeliefID:BeliefUnit]
    ) -> dict[BeliefID:BeliefUnit]:
        return self._get_all_others(agenda_beliefs, self._suffbeliefs)

    def set_owner_id_assigned(
        self, agenda_beliefs: dict[BeliefID:BeliefUnit], agenda_owner_id: OtherID
    ):
        self._owner_id_assigned = False
        if self._suffbeliefs == {}:
            self._owner_id_assigned = True
        else:
            all_suff_others_x = self._get_all_suff_others(agenda_beliefs)
            if all_suff_others_x.get(agenda_owner_id) != None:
                self._owner_id_assigned = True

    def set_suffbeliefs(
        self,
        parent_assignheir,
        assignunit: AssignedUnit,
        agenda_beliefs: dict[BeliefID:BeliefUnit],
    ):
        dict_x = {}
        if parent_assignheir is None or parent_assignheir._suffbeliefs == {}:
            for suffbelief in assignunit._suffbeliefs:
                dict_x[suffbelief] = -1
        elif assignunit._suffbeliefs == {} or (
            parent_assignheir._suffbeliefs.keys() == assignunit._suffbeliefs.keys()
        ):
            for suffbelief in parent_assignheir._suffbeliefs.keys():
                dict_x[suffbelief] = -1
        else:
            # get all_others of parent assignedheir beliefs
            all_parent_assignedheir_others = self._get_all_others(
                agenda_beliefs=agenda_beliefs,
                belief_id_dict=parent_assignheir._suffbeliefs,
            )
            # get all_others of assignedunit beliefs
            all_assignedunit_others = self._get_all_others(
                agenda_beliefs=agenda_beliefs,
                belief_id_dict=assignunit._suffbeliefs,
            )
            if not set(all_assignedunit_others).issubset(
                set(all_parent_assignedheir_others)
            ):
                # else raise error
                raise InvalidAssignHeirPopulateException(
                    f"parent_assigned_heir does not contain all others of the idea's assignedunit\n{set(all_parent_assignedheir_others)=}\n\n{set(all_assignedunit_others)=}"
                )

            # set dict_x = to assignedunit beliefs
            for suffbelief in assignunit._suffbeliefs.keys():
                dict_x[suffbelief] = -1
        self._suffbeliefs = dict_x

    def belief_in(self, belief_ids: dict[BeliefID:-1]):
        return self._suffbeliefs == {} or any(
            self._suffbeliefs.get(gn_x) != None for gn_x in belief_ids
        )


def assigned_heir_shop(
    _suffbeliefs: dict[BeliefID:BeliefID] = None, _owner_id_assigned: bool = None
) -> AssignedHeir:
    if _suffbeliefs is None:
        _suffbeliefs = {}
    if _owner_id_assigned is None:
        _owner_id_assigned = False

    return AssignedHeir(
        _suffbeliefs=_suffbeliefs, _owner_id_assigned=_owner_id_assigned
    )

    # def meld(self, exterior_reason):
    #     for premise_x in exterior_reason.premises.values():
    #         if self.premises.get(premise_x.need) is None:
    #             self.premises[premise_x.need] = premise_x
    #         else:
    #             self.premises.get(premise_x.need).meld(premise_x)
    #     if exterior_reason.base != self.base:
    #         raise InvalidReasonException(
    #             f"Meld fail: reason={exterior_reason.base} is different {self.base=}"
    #         )


def assignedunit_get_from_dict(assignedunit_dict: dict) -> AssignedUnit:
    assignedunit_x = assignedunit_shop()
    for suffbelief_belief_id in assignedunit_dict.get("_suffbeliefs"):
        assignedunit_x.set_suffbelief(belief_id=suffbelief_belief_id)

    return assignedunit_x
