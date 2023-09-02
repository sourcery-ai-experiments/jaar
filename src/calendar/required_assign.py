import dataclasses
from src.calendar.group import groupunit_shop, GroupUnit, GroupName
from src.calendar.member import MemberName


class InvalidAssignHeirPopulateException(Exception):
    pass


@dataclasses.dataclass
class AssignedUnit:
    _suffgroups: dict[GroupName:GroupName]

    def get_dict(self) -> dict[str:str]:
        _suffgroups = {
            group_name: group_name  # sufffact.get_dict()
            for group_name, _suffgroup in self._suffgroups.items()
        }
        return {
            "_suffgroups": _suffgroups,
        }

    def set_suffgroup(self, name: GroupName):
        self._suffgroups[name] = -1

    def del_suffgroup(self, name: GroupName):
        self._suffgroups.pop(name)


def assigned_unit_shop(_suffgroups: dict[GroupName:GroupName] = None) -> AssignedUnit:
    if _suffgroups is None:
        _suffgroups = {}

    return AssignedUnit(_suffgroups=_suffgroups)


@dataclasses.dataclass
class AssignedHeir:
    _suffgroups: dict[GroupName:GroupName]
    _group_member: bool

    def _get_all_members(
        self,
        calendar_groups: dict[GroupName:GroupUnit],
        groupname_dict: dict[GroupName:],
    ):
        dict_x = {}
        for groupname_x in groupname_dict:
            dict_x |= calendar_groups.get(groupname_x)._members
        return dict_x

    def _get_all_suff_members(self, calendar_groups: dict[GroupName:GroupUnit]):
        return self._get_all_members(calendar_groups, self._suffgroups)

    def set_group_member(
        self, calendar_groups: dict[GroupName:GroupUnit], calendar_owner: MemberName
    ):
        self._group_member = False
        if self._suffgroups == {}:
            self._group_member = True
        else:
            all_suff_members_x = self._get_all_suff_members(calendar_groups)
            if all_suff_members_x.get(calendar_owner) != None:
                self._group_member = True

    def set_suffgroups(
        self,
        parent_assignheir,
        assignunit: AssignedUnit,
        calendar_groups: dict[GroupName:GroupUnit],
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
            # collect all_members of parent assignedheir groups
            all_parent_assignedheir_members = self._get_all_members(
                calendar_groups=calendar_groups,
                groupname_dict=parent_assignheir._suffgroups,
            )
            # collect all_members of assignedunit groups
            all_assignedunit_members = self._get_all_members(
                calendar_groups=calendar_groups,
                groupname_dict=assignunit._suffgroups,
            )
            # if all_assignedunit_members is subset of all_parent_assignedheir_members
            if set(all_assignedunit_members).issubset(
                set(all_parent_assignedheir_members)
            ):
                # set dict_x = to assignedunit groups
                for suffgroup in assignunit._suffgroups.keys():
                    dict_x[suffgroup] = -1
            else:
                # else raise error
                raise InvalidAssignHeirPopulateException(
                    f"parent_assigned_heir does not contain all members of the idea's assigned_unit\n{set(all_parent_assignedheir_members)=}\n\n{set(all_assignedunit_members)=}"
                )

        self._suffgroups = dict_x


def assigned_heir_shop(
    _suffgroups: dict[GroupName:GroupName] = None, _group_member: bool = None
) -> AssignedHeir:
    if _suffgroups is None:
        _suffgroups = {}
    if _group_member is None:
        _group_member = False

    return AssignedHeir(_suffgroups=_suffgroups, _group_member=_group_member)

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
    for suffgroup_name in assignedunit_dict.get("_suffgroups"):
        assigned_unit_x.set_suffgroup(name=suffgroup_name)

    return assigned_unit_x
