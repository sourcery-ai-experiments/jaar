from dataclasses import dataclass
from src.agenda.group import GroupUnit, GroupBrand
from src.agenda.party import PartyPID


class InvalidAssignHeirPopulateException(Exception):
    pass


@dataclass
class AssignedUnit:
    _suffgroups: dict[GroupBrand:GroupBrand]

    def get_dict(self) -> dict[str:str]:
        _suffgroups = {
            x_groupbrand: x_groupbrand  # premise.get_dict()
            for x_groupbrand, _suffgroup in self._suffgroups.items()
        }
        return {"_suffgroups": _suffgroups}

    def set_suffgroup(self, brand: GroupBrand):
        self._suffgroups[brand] = -1

    def del_suffgroup(self, brand: GroupBrand):
        self._suffgroups.pop(brand)

    def get_suffgroup(self, brand: GroupBrand) -> GroupBrand:
        return self._suffgroups.get(brand)


def assigned_unit_shop(_suffgroups: dict[GroupBrand:GroupBrand] = None) -> AssignedUnit:
    if _suffgroups is None:
        _suffgroups = {}

    return AssignedUnit(_suffgroups=_suffgroups)


def create_assignedunit(suffgroup: GroupBrand):
    x_assignedunit = assigned_unit_shop()
    x_assignedunit.set_suffgroup(suffgroup)
    return x_assignedunit


@dataclass
class AssignedHeir:
    _suffgroups: dict[GroupBrand:GroupBrand]
    _agent_id_assigned: bool

    def _get_all_partys(
        self,
        agenda_groups: dict[GroupBrand:GroupUnit],
        groupbrand_dict: dict[GroupBrand:],
    ) -> dict[GroupBrand:GroupUnit]:
        dict_x = {}
        for groupbrand_x in groupbrand_dict:
            dict_x |= agenda_groups.get(groupbrand_x)._partys
        return dict_x

    def _get_all_suff_partys(
        self, agenda_groups: dict[GroupBrand:GroupUnit]
    ) -> dict[GroupBrand:GroupUnit]:
        return self._get_all_partys(agenda_groups, self._suffgroups)

    def set_agent_id_assigned(
        self, agenda_groups: dict[GroupBrand:GroupUnit], agenda_agent_id: PartyPID
    ):
        self._agent_id_assigned = False
        if self._suffgroups == {}:
            self._agent_id_assigned = True
        else:
            all_suff_partys_x = self._get_all_suff_partys(agenda_groups)
            if all_suff_partys_x.get(agenda_agent_id) != None:
                self._agent_id_assigned = True

    def set_suffgroups(
        self,
        parent_assignheir,
        assignunit: AssignedUnit,
        agenda_groups: dict[GroupBrand:GroupUnit],
    ):
        dict_x = {}
        if parent_assignheir is None or parent_assignheir._suffgroups == {}:
            for suffgroup in assignunit._suffgroups:
                dict_x[suffgroup] = -1
        elif assignunit._suffgroups == {} or (
            parent_assignheir._suffgroups.keys() == assignunit._suffgroups.keys()
        ):
            for suffgroup in parent_assignheir._suffgroups.keys():
                dict_x[suffgroup] = -1
        else:
            # get all_partys of parent assignedheir groups
            all_parent_assignedheir_partys = self._get_all_partys(
                agenda_groups=agenda_groups,
                groupbrand_dict=parent_assignheir._suffgroups,
            )
            # get all_partys of assignedunit groups
            all_assignedunit_partys = self._get_all_partys(
                agenda_groups=agenda_groups,
                groupbrand_dict=assignunit._suffgroups,
            )
            if not set(all_assignedunit_partys).issubset(
                set(all_parent_assignedheir_partys)
            ):
                # else raise error
                raise InvalidAssignHeirPopulateException(
                    f"parent_assigned_heir does not contain all partys of the idea's assigned_unit\n{set(all_parent_assignedheir_partys)=}\n\n{set(all_assignedunit_partys)=}"
                )

            # set dict_x = to assignedunit groups
            for suffgroup in assignunit._suffgroups.keys():
                dict_x[suffgroup] = -1
        self._suffgroups = dict_x

    def group_in(self, groupbrands: dict[GroupBrand:-1]):
        return self._suffgroups == {} or any(
            self._suffgroups.get(gn_x) != None for gn_x in groupbrands
        )


def assigned_heir_shop(
    _suffgroups: dict[GroupBrand:GroupBrand] = None, _agent_id_assigned: bool = None
) -> AssignedHeir:
    if _suffgroups is None:
        _suffgroups = {}
    if _agent_id_assigned is None:
        _agent_id_assigned = False

    return AssignedHeir(_suffgroups=_suffgroups, _agent_id_assigned=_agent_id_assigned)

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
    assigned_unit_x = assigned_unit_shop()
    for suffgroup_brand in assignedunit_dict.get("_suffgroups"):
        assigned_unit_x.set_suffgroup(brand=suffgroup_brand)

    return assigned_unit_x
