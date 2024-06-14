from dataclasses import dataclass
from src.agenda.idea import IdeaUnit, IdeaID
from src.agenda.party import PartyID


class InvalidAssignHeirPopulateException(Exception):
    pass


@dataclass
class AssignedUnit:
    _suffideas: dict[IdeaID:IdeaID]

    def get_dict(self) -> dict[str:str]:
        _suffideas = {
            x_idea_id: x_idea_id  # premise.get_dict()
            for x_idea_id, _suffidea in self._suffideas.items()
        }
        return {"_suffideas": _suffideas}

    def set_suffidea(self, idea_id: IdeaID):
        self._suffideas[idea_id] = -1

    def suffidea_exists(self, idea_id: IdeaID):
        return self._suffideas.get(idea_id) != None

    def del_suffidea(self, idea_id: IdeaID):
        self._suffideas.pop(idea_id)

    def get_suffidea(self, idea_id: IdeaID) -> IdeaID:
        return self._suffideas.get(idea_id)


def assignedunit_shop(_suffideas: dict[IdeaID:IdeaID] = None) -> AssignedUnit:
    if _suffideas is None:
        _suffideas = {}

    return AssignedUnit(_suffideas=_suffideas)


def create_assignedunit(suffidea: IdeaID):
    x_assignedunit = assignedunit_shop()
    x_assignedunit.set_suffidea(suffidea)
    return x_assignedunit


@dataclass
class AssignedHeir:
    _suffideas: dict[IdeaID:IdeaID]
    _owner_id_assigned: bool

    def _get_all_partys(
        self,
        agenda_ideas: dict[IdeaID:IdeaUnit],
        idea_id_dict: dict[IdeaID:],
    ) -> dict[IdeaID:IdeaUnit]:
        dict_x = {}
        for idea_id_x in idea_id_dict:
            dict_x |= agenda_ideas.get(idea_id_x)._partys
        return dict_x

    def _get_all_suff_partys(
        self, agenda_ideas: dict[IdeaID:IdeaUnit]
    ) -> dict[IdeaID:IdeaUnit]:
        return self._get_all_partys(agenda_ideas, self._suffideas)

    def set_owner_id_assigned(
        self, agenda_ideas: dict[IdeaID:IdeaUnit], agenda_owner_id: PartyID
    ):
        self._owner_id_assigned = False
        if self._suffideas == {}:
            self._owner_id_assigned = True
        else:
            all_suff_partys_x = self._get_all_suff_partys(agenda_ideas)
            if all_suff_partys_x.get(agenda_owner_id) != None:
                self._owner_id_assigned = True

    def set_suffideas(
        self,
        parent_assignheir,
        assignunit: AssignedUnit,
        agenda_ideas: dict[IdeaID:IdeaUnit],
    ):
        dict_x = {}
        if parent_assignheir is None or parent_assignheir._suffideas == {}:
            for suffidea in assignunit._suffideas:
                dict_x[suffidea] = -1
        elif assignunit._suffideas == {} or (
            parent_assignheir._suffideas.keys() == assignunit._suffideas.keys()
        ):
            for suffidea in parent_assignheir._suffideas.keys():
                dict_x[suffidea] = -1
        else:
            # get all_partys of parent assignedheir ideas
            all_parent_assignedheir_partys = self._get_all_partys(
                agenda_ideas=agenda_ideas,
                idea_id_dict=parent_assignheir._suffideas,
            )
            # get all_partys of assignedunit ideas
            all_assignedunit_partys = self._get_all_partys(
                agenda_ideas=agenda_ideas,
                idea_id_dict=assignunit._suffideas,
            )
            if not set(all_assignedunit_partys).issubset(
                set(all_parent_assignedheir_partys)
            ):
                # else raise error
                raise InvalidAssignHeirPopulateException(
                    f"parent_assigned_heir does not contain all partys of the fact's assignedunit\n{set(all_parent_assignedheir_partys)=}\n\n{set(all_assignedunit_partys)=}"
                )

            # set dict_x = to assignedunit ideas
            for suffidea in assignunit._suffideas.keys():
                dict_x[suffidea] = -1
        self._suffideas = dict_x

    def idea_in(self, idea_ids: dict[IdeaID:-1]):
        return self._suffideas == {} or any(
            self._suffideas.get(gn_x) != None for gn_x in idea_ids
        )


def assigned_heir_shop(
    _suffideas: dict[IdeaID:IdeaID] = None, _owner_id_assigned: bool = None
) -> AssignedHeir:
    if _suffideas is None:
        _suffideas = {}
    if _owner_id_assigned is None:
        _owner_id_assigned = False

    return AssignedHeir(_suffideas=_suffideas, _owner_id_assigned=_owner_id_assigned)

    # def meld(self, other_reason):
    #     for premise_x in other_reason.premises.values():
    #         if self.premises.get(premise_x.need) is None:
    #             self.premises[premise_x.need] = premise_x
    #         else:
    #             self.premises.get(premise_x.need).meld(premise_x)
    #     if other_reason.base != self.base:
    #         raise InvalidReasonException(
    #             f"Meld fail: reason={other_reason.base} is different {self.base=}"
    #         )


def assignedunit_get_from_dict(assignedunit_dict: dict) -> AssignedUnit:
    assignedunit_x = assignedunit_shop()
    for suffidea_idea_id in assignedunit_dict.get("_suffideas"):
        assignedunit_x.set_suffidea(idea_id=suffidea_idea_id)

    return assignedunit_x
