from dataclasses import dataclass
from src._world.beliefunit import BeliefUnit, BeliefID
from src._world.char import CharID


class InvalidAssignedHeirPopulateException(Exception):
    pass


@dataclass
class AssignedUnit:
    _heldbeliefs: dict[BeliefID:BeliefID]

    def get_dict(self) -> dict[str:str]:
        _heldbeliefs = {
            x_belief_id: x_belief_id  # premise.get_dict()
            for x_belief_id, _heldbelief in self._heldbeliefs.items()
        }
        return {"_heldbeliefs": _heldbeliefs}

    def set_heldbelief(self, belief_id: BeliefID):
        self._heldbeliefs[belief_id] = -1

    def heldbelief_exists(self, belief_id: BeliefID):
        return self._heldbeliefs.get(belief_id) != None

    def del_heldbelief(self, belief_id: BeliefID):
        self._heldbeliefs.pop(belief_id)

    def get_heldbelief(self, belief_id: BeliefID) -> BeliefID:
        return self._heldbeliefs.get(belief_id)


def cultureunit_shop(_heldbeliefs: dict[BeliefID:BeliefID] = None) -> AssignedUnit:
    if _heldbeliefs is None:
        _heldbeliefs = {}

    return AssignedUnit(_heldbeliefs=_heldbeliefs)


def create_cultureunit(heldbelief: BeliefID):
    x_cultureunit = cultureunit_shop()
    x_cultureunit.set_heldbelief(heldbelief)
    return x_cultureunit


@dataclass
class AssignedHeir:
    _heldbeliefs: dict[BeliefID:BeliefID]
    _owner_id_culture: bool

    def _get_all_chars(
        self,
        world_beliefs: dict[BeliefID:BeliefUnit],
        belief_id_dict: dict[BeliefID:],
    ) -> dict[BeliefID:BeliefUnit]:
        dict_x = {}
        for belief_id_x in belief_id_dict:
            dict_x |= world_beliefs.get(belief_id_x)._chars
        return dict_x

    def _get_all_suff_chars(
        self, world_beliefs: dict[BeliefID:BeliefUnit]
    ) -> dict[BeliefID:BeliefUnit]:
        return self._get_all_chars(world_beliefs, self._heldbeliefs)

    def set_owner_id_culture(
        self, world_beliefs: dict[BeliefID:BeliefUnit], world_owner_id: CharID
    ):
        self._owner_id_culture = False
        if self._heldbeliefs == {}:
            self._owner_id_culture = True
        else:
            all_suff_chars_x = self._get_all_suff_chars(world_beliefs)
            if all_suff_chars_x.get(world_owner_id) != None:
                self._owner_id_culture = True

    def set_heldbeliefs(
        self,
        parent_cultureheir,
        cultureunit: AssignedUnit,
        world_beliefs: dict[BeliefID:BeliefUnit],
    ):
        dict_x = {}
        if parent_cultureheir is None or parent_cultureheir._heldbeliefs == {}:
            for heldbelief in cultureunit._heldbeliefs:
                dict_x[heldbelief] = -1
        elif cultureunit._heldbeliefs == {} or (
            parent_cultureheir._heldbeliefs.keys() == cultureunit._heldbeliefs.keys()
        ):
            for heldbelief in parent_cultureheir._heldbeliefs.keys():
                dict_x[heldbelief] = -1
        else:
            # get all_chars of parent cultureheir beliefs
            all_parent_cultureheir_chars = self._get_all_chars(
                world_beliefs=world_beliefs,
                belief_id_dict=parent_cultureheir._heldbeliefs,
            )
            # get all_chars of cultureunit beliefs
            all_cultureunit_chars = self._get_all_chars(
                world_beliefs=world_beliefs,
                belief_id_dict=cultureunit._heldbeliefs,
            )
            if not set(all_cultureunit_chars).issubset(
                set(all_parent_cultureheir_chars)
            ):
                # else raise error
                raise InvalidAssignedHeirPopulateException(
                    f"parent_culture_heir does not contain all chars of the idea's cultureunit\n{set(all_parent_cultureheir_chars)=}\n\n{set(all_cultureunit_chars)=}"
                )

            # set dict_x = to cultureunit beliefs
            for heldbelief in cultureunit._heldbeliefs.keys():
                dict_x[heldbelief] = -1
        self._heldbeliefs = dict_x

    def belief_in(self, belief_ids: dict[BeliefID:-1]):
        return self._heldbeliefs == {} or any(
            self._heldbeliefs.get(gn_x) != None for gn_x in belief_ids
        )


def cultureheir_shop(
    _heldbeliefs: dict[BeliefID:BeliefID] = None, _owner_id_culture: bool = None
) -> AssignedHeir:
    if _heldbeliefs is None:
        _heldbeliefs = {}
    if _owner_id_culture is None:
        _owner_id_culture = False

    return AssignedHeir(_heldbeliefs=_heldbeliefs, _owner_id_culture=_owner_id_culture)

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


def cultureunit_get_from_dict(cultureunit_dict: dict) -> AssignedUnit:
    cultureunit_x = cultureunit_shop()
    for heldbelief_belief_id in cultureunit_dict.get("_heldbeliefs"):
        cultureunit_x.set_heldbelief(belief_id=heldbelief_belief_id)

    return cultureunit_x
