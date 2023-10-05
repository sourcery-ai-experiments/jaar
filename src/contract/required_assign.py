import dataclasses
from src.contract.group import groupunit_shop, GroupUnit, GroupBrand
from src.contract.party import PartyTitle


class InvalidAssignHeirPopulateException(Exception):
    pass


@dataclasses.dataclass
class AssignedUnit:
    _suffgroups: dict[GroupBrand:GroupBrand]

    def get_dict(self) -> dict[str:str]:
        _suffgroups = {
            group_title: group_title  # sufffact.get_dict()
            for group_title, _suffgroup in self._suffgroups.items()
        }
        return {"_suffgroups": _suffgroups}

    def set_suffgroup(self, title: GroupBrand):
        self._suffgroups[title] = -1

    def del_suffgroup(self, title: GroupBrand):
        self._suffgroups.pop(title)


def assigned_unit_shop(_suffgroups: dict[GroupBrand:GroupBrand] = None) -> AssignedUnit:
    if _suffgroups is None:
        _suffgroups = {}

    return AssignedUnit(_suffgroups=_suffgroups)


@dataclasses.dataclass
class AssignedHeir:
    _suffgroups: dict[GroupBrand:GroupBrand]
    _group_party: bool

    def _get_all_partys(
        self,
        contract_groups: dict[GroupBrand:GroupUnit],
        groupbrand_dict: dict[GroupBrand:],
    ):
        dict_x = {}
        for groupbrand_x in groupbrand_dict:
            dict_x |= contract_groups.get(groupbrand_x)._partys
        return dict_x

    def _get_all_suff_partys(self, contract_groups: dict[GroupBrand:GroupUnit]):
        return self._get_all_partys(contract_groups, self._suffgroups)

    def set_group_party(
        self, contract_groups: dict[GroupBrand:GroupUnit], contract_owner: PartyTitle
    ):
        self._group_party = False
        if self._suffgroups == {}:
            self._group_party = True
        else:
            all_suff_partys_x = self._get_all_suff_partys(contract_groups)
            if all_suff_partys_x.get(contract_owner) != None:
                self._group_party = True

    def set_suffgroups(
        self,
        parent_assignheir,
        assignunit: AssignedUnit,
        contract_groups: dict[GroupBrand:GroupUnit],
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
            # collect all_partys of parent assignedheir groups
            all_parent_assignedheir_partys = self._get_all_partys(
                contract_groups=contract_groups,
                groupbrand_dict=parent_assignheir._suffgroups,
            )
            # collect all_partys of assignedunit groups
            all_assignedunit_partys = self._get_all_partys(
                contract_groups=contract_groups,
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
    _suffgroups: dict[GroupBrand:GroupBrand] = None, _group_party: bool = None
) -> AssignedHeir:
    if _suffgroups is None:
        _suffgroups = {}
    if _group_party is None:
        _group_party = False

    return AssignedHeir(_suffgroups=_suffgroups, _group_party=_group_party)

    # def meld(self, other_required):
    #     for sufffact_x in other_required.sufffacts.values():
    #         if self.sufffacts.get(sufffact_x.need) is None:
    #             self.sufffacts[sufffact_x.need] = sufffact_x
    #         else:
    #             self.sufffacts.get(sufffact_x.need).meld(sufffact_x)
    #     if other_required.base != self.base:
    #         raise InvalidRequiredException(
    #             f"Meld fail: required={other_required.base} is different {self.base=}"
    #         )


def assignedunit_get_from_dict(assignedunit_dict: dict) -> AssignedUnit:
    assigned_unit_x = assigned_unit_shop()
    for suffgroup_title in assignedunit_dict.get("_suffgroups"):
        assigned_unit_x.set_suffgroup(title=suffgroup_title)

    return assigned_unit_x
