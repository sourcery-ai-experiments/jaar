import dataclasses
import json
from datetime import datetime
from src.agent.member import (
    MemberName,
    MemberUnit,
    MemberLink,
    memberunits_get_from_dict,
    memberunit_shop,
    memberlink_shop,
    MemberUnitExternalMetrics,
)
from src.agent.group import (
    GroupLink,
    GroupName,
    GroupUnit,
    grouplinks_get_from_dict,
    get_from_dict as groupunits_get_from_dict,
    groupunit_shop,
    grouplink_shop,
)
from src.agent.required import (
    AcptFactCore,
    AcptFactUnit,
    AcptFactUnit,
    RequiredHeir,
    RequiredUnit,
    Road,
    acptfactunits_get_from_dict,
    acptfactunit_shop,
    acptfactunits_get_from_dict,
    requireds_get_from_dict,
    sufffactunit_shop,
)
from src.agent.tree_metrics import TreeMetrics
from src.agent.x_func import x_get_json
from src.agent.tool import ToolCore, ToolKid, ToolRoot, ToolAttrHolder
from src.agent.hreg_time import (
    _get_time_hreg_src_tool,
    get_time_min_from_dt as hreg_get_time_min_from_dt,
    convert1440toReadableTime,
    get_number_with_postfix,
    get_jajatime_readable_from_dt,
)
from src.agent.lemma import Lemmas
from src.agent.road import (
    get_walk_from_road,
    is_sub_road_in_src_road,
    road_validate,
    change_road,
    get_terminus_node_from_road,
    find_replace_road_key_dict,
    get_ancestor_roads,
)
from copy import deepcopy as copy_deepcopy
from src.agent.x_func import (
    save_file as x_func_save_file,
    dir_files as x_func_dir_files,
    open_file as x_func_open_file,
    get_meld_weight,
)


class InvalidAgentException(Exception):
    pass


@dataclasses.dataclass
class AgentUnit:
    _desc: str = None
    _weight: float = None
    _members: dict[MemberName:MemberUnit] = None
    _groups: dict[GroupName:GroupUnit] = None
    _toolroot: ToolRoot = None
    _tool_dict: dict[Road:ToolCore] = None
    _max_tree_traverse: int = 3
    _tree_traverse_count: int = None
    _rational: bool = False

    def __init__(self, _weight: float = None, _desc=None) -> None:
        if _weight is None:
            _weight = 1
        self._weight = _weight
        if _desc is None:
            _desc = ""
        self._toolroot = ToolRoot(_desc=_desc, _uid=1)
        self._desc = _desc

    def set_banking_attr_memberunits(self, river_tmembers: dict):
        for memberunit_x in self._members.values():
            memberunit_x.clear_banking_data()
            river_tmember = river_tmembers.get(memberunit_x.name)
            if river_tmember != None:
                memberunit_x.set_banking_data(
                    river_tmember.tax_total, river_tmember.tax_diff
                )

    def import_external_memberunit_metrics(
        self, external_metrics: MemberUnitExternalMetrics
    ):
        member_x = self._members.get(external_metrics.internal_name)
        member_x._creditor_active = external_metrics.creditor_active
        member_x._debtor_active = external_metrics.debtor_active
        # self.set_memberunit(memberunit=member_x)

    def set_max_tree_traverse(self, int_x: int):
        if int_x < 2:
            raise InvalidAgentException(
                f"set_max_tree_traverse: input '{int_x}' must be number that is 2 or greater"
            )
        else:
            self._max_tree_traverse = int_x

    def get_bond_status(self) -> bool:
        self.set_agent_metrics()
        tree_metrics_x = self.get_tree_metrics()
        if tree_metrics_x.bond_promise_count != 1:
            return False

        promise_tool_road = tree_metrics_x.an_promise_tool_road
        if (
            self._are_all_members_groups_are_in_tool_kid(road=promise_tool_road)
            == False
        ):
            return False

        return self.all_tools_relevant_to_promise_tool(road=promise_tool_road) != False

    def export_all_bonds(self, dir: str):
        self.set_all_tool_uids_unique()
        self.set_agent_metrics()
        # dict_x = {}
        for yx in self.get_tool_list():
            if yx.promise:
                cx = self.get_agent_sprung_from_single_tool(yx.get_road())
                file_name = f"{yx._uid}.json"
                x_func_save_file(
                    dest_dir=dir,
                    file_name=file_name,
                    file_text=cx.get_json(),
                    replace=True,
                )
        return {}

    def get_agent_sprung_from_single_tool(self, road: Road):
        self.set_agent_metrics()
        tool_x = self.get_tool_kid(road=road)
        new_weight = self._weight * tool_x._agent_importance
        cx = AgentUnit(_desc=self._toolroot._desc, _weight=new_weight)

        for road_assc in sorted(list(self._get_all_tool_assoc_roads(road))):
            src_yx = self.get_tool_kid(road=road_assc)
            new_yx = copy_deepcopy(src_yx)
            if new_yx._walk != "":
                cx.add_tool(tool_kid=new_yx, walk=new_yx._walk)
            cx.set_agent_metrics()

        # TODO grab groups
        # TODO grab all group members
        # TODO grab acptfacts
        return cx

    def _get_all_tool_assoc_roads(self, road: Road) -> set[Road]:
        tool_ancestor_list = get_ancestor_roads(road=road)
        tool_x = self.get_tool_kid(road=road)
        requiredunit_base_road_list = []

        for requiredunit_obj in tool_x._requiredunits.values():
            required_base = requiredunit_obj.base
            requiredunit_base_road_list.extend(get_ancestor_roads(required_base))
            requiredunit_base_road_list.extend(self.get_heir_road_list(required_base))

        tool_assoc_list = [road]
        tool_assoc_list.extend(tool_ancestor_list)
        tool_assoc_list.extend(requiredunit_base_road_list)
        return set(tool_assoc_list)

    def all_tools_relevant_to_promise_tool(self, road: Road) -> bool:
        promise_tool_assoc_set = set(self._get_all_tool_assoc_roads(road=road))
        all_tools_set = set(self.get_tool_tree_ordered_road_list())
        return all_tools_set == all_tools_set.intersection(promise_tool_assoc_set)

    def _are_all_members_groups_are_in_tool_kid(self, road: Road) -> bool:
        tool_kid = self.get_tool_kid(road=road)
        # get dict of all tool groupheirs
        groupheir_list = tool_kid._groupheirs.keys()
        groupheir_dict = {groupheir_name: 1 for groupheir_name in groupheir_list}
        non_single_groupunits = {
            groupunit.name: groupunit
            for groupunit in self._groups.values()
            if groupunit._single_member != True
        }
        # check all non_single_member_groupunits are in groupheirs
        for non_single_group in non_single_groupunits.values():
            if groupheir_dict.get(non_single_group.name) is None:
                return False

        # get dict of all memberlinks that are in all groupheirs
        groupheir_memberunits = {}
        for groupheir_name in groupheir_dict:
            groupunit = self._groups.get(groupheir_name)
            for memberlink in groupunit._members.values():
                groupheir_memberunits[memberlink.name] = self._members.get(
                    memberlink.name
                )

        # check all agent._members are in groupheir_memberunits
        return len(self._members) == len(groupheir_memberunits)

    def get_time_min_from_dt(self, dt: datetime) -> float:
        return hreg_get_time_min_from_dt(dt=dt)

    def get_time_c400_from_min(self, min: int) -> int:
        c400_tool = self.get_tool_kid(f"{self._desc},time,tech,400 year cycle")
        c400_min = c400_tool._close
        return int(min / c400_min), c400_tool, min % c400_min

    def get_time_c400yr_from_min(self, min: int):
        # given int minutes within 400 year range return year and remainder minutes
        c400_count, c400_tool, c400yr_min = self.get_time_c400_from_min(min=min)
        c100_4_96y = c400_tool.get_kids_in_range(begin=c400yr_min, close=c400yr_min)[0]
        cXXXyr_min = c400yr_min - c100_4_96y._begin

        # identify which range the time is in
        if c100_4_96y._close - c100_4_96y._begin in (
            50492160,
            52596000,
        ):  # 96 year and 100 year spans
            yr4_1461 = self.get_tool_kid(f"{self._desc},time,tech,4year with leap")
            yr4_cycles = int(cXXXyr_min / yr4_1461._close)
            cXyr_min = cXXXyr_min % yr4_1461._close
            yr1_tool = yr4_1461.get_kids_in_range(begin=cXyr_min, close=cXyr_min)[0]
        elif c100_4_96y._close - c100_4_96y._begin == 2102400:
            yr4_1460 = self.get_tool_kid(f"{self._desc},time,tech,4year wo leap")
            yr4_cycles = 0
            yr1_tool = yr4_1460.get_kids_in_range(begin=cXXXyr_min, close=cXXXyr_min)[0]
            cXyr_min = cXXXyr_min % yr4_1460._close

        yr1_rem_min = cXyr_min - yr1_tool._begin
        yr1_tool_begin = int(yr1_tool._desc.split("-")[0]) - 1

        c100_4_96y_begin = int(c100_4_96y._desc.split("-")[0])
        year_num = c100_4_96y_begin + (4 * yr4_cycles) + yr1_tool_begin
        return year_num, yr1_tool, yr1_rem_min

    def get_time_month_from_min(self, min: int):
        year_num, yr1_tool, yr1_tool_rem_min = self.get_time_c400yr_from_min(min=min)
        yrx = None
        if yr1_tool._close - yr1_tool._begin == 525600:
            yrx = self.get_tool_kid(f"{self._desc},time,tech,365 year")
        elif yr1_tool._close - yr1_tool._begin == 527040:
            yrx = self.get_tool_kid(f"{self._desc},time,tech,366 year")
        mon_x = yrx.get_kids_in_range(begin=yr1_tool_rem_min, close=yr1_tool_rem_min)[0]
        month_rem_min = yr1_tool_rem_min - mon_x._begin
        month_num = int(mon_x._desc.split("-")[0])
        day_x = self.get_tool_kid(f"{self._desc},time,tech,day")
        day_num = int(month_rem_min / day_x._close)
        day_rem_min = month_rem_min % day_x._close
        return month_num, day_num, day_rem_min, day_x

    def get_time_hour_from_min(self, min: int):
        month_num, day_num, day_rem_min, day_x = self.get_time_month_from_min(min=min)
        hr_x = day_x.get_kids_in_range(begin=day_rem_min, close=day_rem_min)[0]
        hr_rem_min = day_rem_min - hr_x._begin
        hr_num = int(hr_x._desc.split("-")[0])
        min_num = int(hr_rem_min % (hr_x._close - hr_x._begin))
        return hr_num, min_num, hr_x

    def get_time_dt_from_min(self, min: int) -> datetime:
        year_x = (
            400 * self.get_time_c400_from_min(min=min)[0]
        ) + self.get_time_c400yr_from_min(min=min)[0]
        month_num = self.get_time_month_from_min(min=min)[0]
        day_num = self.get_time_month_from_min(min=min)[1] + 1
        hr_num, min_num, hr_x = self.get_time_hour_from_min(min=min)
        return datetime(
            year=year_x, month=month_num, day=day_num, hour=hr_num, minute=min_num
        )

    def get_jajatime_readable_one_time_event(self, jajatime_min: int) -> str:
        dt_x = self.get_time_dt_from_min(min=jajatime_min)
        return get_jajatime_readable_from_dt(dt=dt_x)

    def get_jajatime_repeating_readable_text(
        self, open: float = None, nigh: float = None, divisor: float = None
    ) -> str:
        str_x = "test3"
        if divisor is None:
            str_x = self.get_jajatime_readable_one_time_event(jajatime_min=open)
            # str_x = f"Weekday, monthname monthday year"
        elif divisor != None and divisor % 10080 == 0:
            str_x = self._get_jajatime_week_readable_text(open, divisor)
        elif divisor != None and divisor % 1440 == 0:
            if divisor == 1440:
                str_x = f"every day at {convert1440toReadableTime(min1440=open)}"
            else:
                num_days = int(divisor / 1440)
                num_with_postfix = get_number_with_postfix(num=num_days)
                str_x = f"every {num_with_postfix} day at {convert1440toReadableTime(min1440=open)}"
        else:
            str_x = "unkonwn"

        return str_x

    def _get_jajatime_week_readable_text(self, open: int, divisor: int) -> str:
        open_in_week = open % divisor
        week_road = f"{self._desc},time,tech,week"
        weekday_tools_dict = self.get_tool_ranged_kids(
            tool_road=week_road, begin=open_in_week
        )
        weekday_tool_node = None
        for tool in weekday_tools_dict.values():
            weekday_tool_node = tool

        if divisor == 10080:
            return f"every {weekday_tool_node._desc} at {convert1440toReadableTime(min1440=open % 1440)}"
        num_with_postfix = get_number_with_postfix(num=divisor // 10080)
        return f"every {num_with_postfix} {weekday_tool_node._desc} at {convert1440toReadableTime(min1440=open % 1440)}"

    def get_members_metrics(self):
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.grouplinks_metrics

    def set_members_empty_if_null(self):
        if self._members is None:
            self._members = {}

    def add_to_group_agent_credit_debt(
        self,
        groupname: GroupName,
        groupheir_agent_credit: float,
        groupheir_agent_debt: float,
    ):
        for group in self._groups.values():
            if group.name == groupname:
                group.set_empty_agent_credit_debt_to_zero()
                group._agent_credit += groupheir_agent_credit
                group._agent_debt += groupheir_agent_debt

    def add_to_group_agent_agenda_credit_debt(
        self,
        groupname: GroupName,
        groupline_agent_credit: float,
        groupline_agent_debt: float,
    ):
        for group in self._groups.values():
            if (
                group.name == groupname
                and groupline_agent_credit != None
                and groupline_agent_debt != None
            ):
                group.set_empty_agent_credit_debt_to_zero()
                group._agent_agenda_credit += groupline_agent_credit
                group._agent_agenda_debt += groupline_agent_debt

    def add_to_memberunit_agent_credit_debt(
        self,
        memberunit_name: MemberName,
        agent_credit,
        agent_debt: float,
        agent_agenda_credit: float,
        agent_agenda_debt: float,
    ):
        for memberunit in self._members.values():
            if memberunit.name == memberunit_name:
                memberunit.add_agent_credit_debt(
                    agent_credit=agent_credit,
                    agent_debt=agent_debt,
                    agent_agenda_credit=agent_agenda_credit,
                    agent_agenda_debt=agent_agenda_debt,
                )

    def set_groupunits_empty_if_null(self):
        if self._groups is None:
            self._groups = {}

    def del_memberunit(self, name: str):
        self._groups.pop(name)
        self._members.pop(name)

    def add_memberunit(
        self,
        name: str,
        uid: int = None,
        creditor_weight: int = None,
        debtor_weight: int = None,
    ):
        memberunit = memberunit_shop(
            name=MemberName(name),
            uid=uid,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )
        self.set_memberunit(memberunit=memberunit)

    def set_memberunit(self, memberunit: MemberUnit):
        self.set_members_empty_if_null()
        self.set_groupunits_empty_if_null()
        # future: if member is new check group does not already have that name

        self._members[memberunit.name] = memberunit

        existing_group = None
        try:
            existing_group = self._groups[memberunit.name]
        except KeyError:
            memberlink = memberlink_shop(
                name=MemberName(memberunit.name), creditor_weight=1, debtor_weight=1
            )
            memberlinks = {memberlink.name: memberlink}
            group_unit = groupunit_shop(
                name=memberunit.name,
                _single_member=True,
                _members=memberlinks,
                uid=None,
                single_member_id=None,
            )
            self.set_groupunit(groupunit=group_unit)

    def edit_memberunit_name(
        self,
        old_name: str,
        new_name: str,
        allow_member_overwite: bool,
        allow_nonsingle_group_overwrite: bool,
    ):
        old_name_creditor_weight = self._members.get(old_name).creditor_weight
        if not allow_member_overwite and self._members.get(new_name) != None:
            raise InvalidAgentException(
                f"Member '{old_name}' change to '{new_name}' failed since it already exists."
            )
        elif (
            not allow_nonsingle_group_overwrite
            and self._groups.get(new_name) != None
            and self._groups.get(new_name)._single_member == False
        ):
            raise InvalidAgentException(
                f"Member '{old_name}' change to '{new_name}' failed since non-single group '{new_name}' already exists."
            )
        elif (
            allow_nonsingle_group_overwrite
            and self._groups.get(new_name) != None
            and self._groups.get(new_name)._single_member == False
        ):
            self.del_groupunit(groupname=new_name)
        elif self._members.get(new_name) != None:
            old_name_creditor_weight += self._members.get(new_name).creditor_weight

        self.add_memberunit(name=new_name, creditor_weight=old_name_creditor_weight)
        groups_affected_list = []
        for group in self._groups.values():
            groups_affected_list.extend(
                group.name
                for member_x in group._members.values()
                if member_x.name == old_name
            )
        for group_x in groups_affected_list:
            memberlink_creditor_weight = (
                self._groups.get(group_x)._members.get(old_name).creditor_weight
            )
            memberlink_debtor_weight = (
                self._groups.get(group_x)._members.get(old_name).debtor_weight
            )
            if self._groups.get(group_x)._members.get(new_name) != None:
                memberlink_creditor_weight += (
                    self._groups.get(group_x)._members.get(new_name).creditor_weight
                )
                memberlink_debtor_weight += (
                    self._groups.get(group_x)._members.get(new_name).debtor_weight
                )

            self._groups.get(group_x).set_memberlink(
                memberlink=memberlink_shop(
                    name=new_name,
                    creditor_weight=memberlink_creditor_weight,
                    debtor_weight=memberlink_debtor_weight,
                )
            )
            self._groups.get(group_x).del_memberlink(name=old_name)

        self.del_memberunit(name=old_name)

    def get_memberunits_name_list(self):
        membername_list = list(self._members.keys())
        membername_list.append("")
        membername_dict = {
            membername.lower(): membername for membername in membername_list
        }
        membername_lowercase_ordered_list = sorted(list(membername_dict))
        return [
            membername_dict[membername_l]
            for membername_l in membername_lowercase_ordered_list
        ]

    def get_memberunits_uid_max(self) -> int:
        uid_max = 1
        for memberunit_x in self._members.values():
            if memberunit_x.uid != None and memberunit_x.uid > uid_max:
                uid_max = memberunit_x.uid
        return uid_max

    def get_memberunits_uid_dict(self) -> dict[int:int]:
        uid_dict = {}
        for memberunit_x in self._members.values():
            if uid_dict.get(memberunit_x.uid) is None:
                uid_dict[memberunit_x.uid] = 1
            else:
                uid_dict[memberunit_x.uid] += 1
        return uid_dict

    def set_all_memberunits_uids_unique(self) -> int:
        uid_max = self.get_memberunits_uid_max()
        uid_dict = self.get_memberunits_uid_dict()
        for memberunit_x in self._members.values():
            if uid_dict.get(memberunit_x.uid) > 0:
                new_uid_max = uid_max + 1
                memberunit_x.uid = new_uid_max
                uid_max = memberunit_x.uid

    def all_memberunits_uids_are_unique(self):
        uid_dict = self.get_memberunits_uid_dict()
        return not any(
            uid_count > 1 or uid is None for uid, uid_count in uid_dict.items()
        )

    def get_groupunits_uid_max(self) -> int:
        uid_max = 1
        for groupunit_x in self._groups.values():
            if groupunit_x.uid != None and groupunit_x.uid > uid_max:
                uid_max = groupunit_x.uid
        return uid_max

    def get_groupunits_uid_dict(self) -> dict[int:int]:
        uid_dict = {}
        for groupunit_x in self._groups.values():
            if uid_dict.get(groupunit_x.uid) is None:
                uid_dict[groupunit_x.uid] = 1
            else:
                uid_dict[groupunit_x.uid] += 1
        return uid_dict

    def set_all_groupunits_uids_unique(self) -> int:
        uid_max = self.get_groupunits_uid_max()
        uid_dict = self.get_groupunits_uid_dict()
        for groupunit_x in self._groups.values():
            if uid_dict.get(groupunit_x.uid) > 0:
                new_uid_max = uid_max + 1
                groupunit_x.uid = new_uid_max
                uid_max = groupunit_x.uid

    def all_groupunits_uids_are_unique(self):
        uid_dict = self.get_groupunits_uid_dict()
        return not any(
            uid_count > 1 or uid is None for uid, uid_count in uid_dict.items()
        )

    def set_groupunit(self, groupunit: GroupUnit, create_missing_members: bool = None):
        self.set_groupunits_empty_if_null()
        groupunit._set_memberlinks_empty_if_null()
        self._groups[groupunit.name] = groupunit

        if create_missing_members:
            self._create_missing_members(memberlinks=groupunit._members)

    def _create_missing_members(self, memberlinks: dict[MemberName:MemberLink]):
        for memberlink_x in memberlinks.values():
            if self._members.get(memberlink_x.name) is None:
                self.set_memberunit(
                    memberunit=memberunit_shop(
                        name=memberlink_x.name,
                        creditor_weight=memberlink_x.creditor_weight,
                        debtor_weight=memberlink_x.debtor_weight,
                    )
                )

    def del_groupunit(self, groupname: GroupName):
        self._groups.pop(groupname)

    def edit_groupunit_name(
        self, old_name: GroupName, new_name: GroupName, allow_group_overwite: bool
    ):
        if not allow_group_overwite and self._groups.get(new_name) != None:
            raise InvalidAgentException(
                f"Group '{old_name}' change to '{new_name}' failed since it already exists."
            )
        elif self._groups.get(new_name) != None:
            old_groupunit = self._groups.get(old_name)
            old_groupunit.set_name(name=new_name)
            self._groups.get(new_name).meld(other_group=old_groupunit)
            self.del_groupunit(groupname=old_name)
        elif self._groups.get(new_name) is None:
            old_groupunit = self._groups.get(old_name)
            groupunit_x = groupunit_shop(
                name=new_name,
                uid=old_groupunit.uid,
                _members=old_groupunit._members,
                single_member_id=old_groupunit.single_member_id,
                _single_member=old_groupunit._single_member,
            )
            self.set_groupunit(groupunit=groupunit_x)
            self.del_groupunit(groupname=old_name)

        self._edit_grouplinks_name(
            old_name=old_name,
            new_name=new_name,
            allow_group_overwite=allow_group_overwite,
        )

    def _edit_grouplinks_name(
        self,
        old_name: GroupName,
        new_name: GroupName,
        allow_group_overwite: bool,
    ):
        for tool_x in self.get_tool_list():
            if (
                tool_x._grouplinks.get(new_name) != None
                and tool_x._grouplinks.get(old_name) != None
            ):
                old_grouplink = tool_x._grouplinks.get(old_name)
                old_grouplink.name = new_name
                tool_x._grouplinks.get(new_name).meld(
                    other_grouplink=old_grouplink,
                    other_on_meld_weight_action="sum",
                    src_on_meld_weight_action="sum",
                )

                tool_x.del_grouplink(groupname=old_name)
            elif (
                tool_x._grouplinks.get(new_name) is None
                and tool_x._grouplinks.get(old_name) != None
            ):
                old_grouplink = tool_x._grouplinks.get(old_name)
                new_grouplink = grouplink_shop(
                    name=new_name,
                    creditor_weight=old_grouplink.creditor_weight,
                    debtor_weight=old_grouplink.debtor_weight,
                )
                tool_x.set_grouplink(grouplink=new_grouplink)
                tool_x.del_grouplink(groupname=old_name)

    def get_groupunits_name_list(self):
        groupname_list = list(self._groups.keys())
        groupname_list.append("")
        groupname_dict = {groupname.lower(): groupname for groupname in groupname_list}
        groupname_lowercase_ordered_list = sorted(list(groupname_dict))
        return [groupname_dict[group_l] for group_l in groupname_lowercase_ordered_list]

    def set_time_acptfacts(self, open: datetime = None, nigh: datetime = None) -> None:
        open_minutes = self.get_time_min_from_dt(dt=open) if open != None else None
        nigh_minutes = self.get_time_min_from_dt(dt=nigh) if nigh != None else None
        minutes_acptfact = f"{self._desc},time,jajatime"
        self.set_acptfact(
            base=minutes_acptfact,
            pick=minutes_acptfact,
            open=open_minutes,
            nigh=nigh_minutes,
        )

    def _is_tool_rangeroot(self, tool_road: Road):
        anc_roads = get_ancestor_roads(road=tool_road)
        parent_road = self._desc if len(anc_roads) == 1 else anc_roads[1]

        # figure out if parent is range
        parent_range = None
        if len(parent_road.split(",")) == 1:
            parent_range = False
        else:
            parent_tool = self.get_tool_kid(road=parent_road)
            parent_range = parent_tool._begin != None and parent_tool._close != None

        # figure out if numeric source exists
        tool_x = self.get_tool_kid(road=tool_road)
        numeric_src_road = None
        numeric_src_road = tool_x._numeric_road != None

        return not numeric_src_road and not parent_range

    def _get_rangeroot_acptfactunits(self):
        return [
            acptfact
            for acptfact in self._toolroot._acptfactunits.values()
            if acptfact.open != None
            and acptfact.nigh != None
            and self._is_tool_rangeroot(tool_road=acptfact.base)
        ]

    def _get_rangeroot_1stlevel_associates(self, ranged_acptfactunits: list[ToolCore]):
        lemmas_x = Lemmas()
        lemmas_x.set_empty_if_null()
        # lemma_tools = {}
        for acptfact in ranged_acptfactunits:
            acptfact_tool = self.get_tool_kid(road=acptfact.base)
            for kid in acptfact_tool._kids.values():
                lemmas_x.eval(tool_x=kid, src_acptfact=acptfact, src_tool=acptfact_tool)

            if acptfact_tool._special_road != None:
                lemmas_x.eval(
                    tool_x=self.get_tool_kid(road=acptfact_tool._special_road),
                    src_acptfact=acptfact,
                    src_tool=acptfact_tool,
                )
        return lemmas_x

    def _get_lemma_acptfactunits(self) -> dict:
        # get all range-root first level kids and special_road
        lemmas_x = self._get_rangeroot_1stlevel_associates(
            self._get_rangeroot_acptfactunits()
        )

        # Now collect associates (all their descendents and special_roads)
        lemma_acptfactunits = {}  # acptfact.base : acptfactUnit
        count_x = 0
        while lemmas_x.is_lemmas_evaluated() == False or count_x > 10000:
            count_x += 1
            if count_x == 9998:
                raise InvalidAgentException("lemma loop failed")

            lemma_y = lemmas_x.get_unevaluated_lemma()
            tool_x = lemma_y.tool_x
            acptfact_x = lemma_y.calc_acptfact

            road_x = f"{tool_x._walk},{tool_x._desc}"
            lemma_acptfactunits[road_x] = acptfact_x

            for kid2 in tool_x._kids.values():
                lemmas_x.eval(tool_x=kid2, src_acptfact=acptfact_x, src_tool=tool_x)
            if tool_x._special_road not in [None, ""]:
                lemmas_x.eval(
                    tool_x=self.get_tool_kid(road=tool_x._special_road),
                    src_acptfact=acptfact_x,
                    src_tool=tool_x,
                )

        return lemma_acptfactunits

    def set_acptfact(
        self,
        base: Road,
        pick: Road,
        open: float = None,
        nigh: float = None,
        create_missing_tools: bool = None,
    ):  # sourcery skip: low-code-quality
        if create_missing_tools:
            self._set_toolkid_if_empty(road=base)
            self._set_toolkid_if_empty(road=pick)

        self._set_acptfacts_empty_if_null()
        self._execute_tree_traverse()
        acptfact_tool = self.get_tool_kid(road=base)

        if acptfact_tool._begin is None and acptfact_tool._close is None:
            self._edit_set_toolroot_acptfactunits(
                base=base, pick=pick, open=open, nigh=nigh
            )

        # if acptfact's tool no range or is a "range-root" then allow acptfact to be set by user
        elif (
            acptfact_tool._begin != None
            and acptfact_tool._close != None
            and self._is_tool_rangeroot(tool_road=base) == False
        ):
            raise InvalidAgentException(
                f"Non range-root acptfact:{base} can only be set by range-root acptfact"
            )

        elif (
            acptfact_tool._begin != None
            and acptfact_tool._close != None
            and self._is_tool_rangeroot(tool_road=base) == True
        ):
            # when tool is "range-root" identify any required.bases that are descendents
            # calculate and set those descendent acptfacts
            # example: timeline range (0-, 1.5e9) is range-root
            # example: "timeline,weeks" (spllt 10080) is range-descendent
            # there exists a required base "timeline,weeks" with sufffact.need = "timeline,weeks"
            # and (1,2) divisor=2 (every other week)
            #
            # user should not set "timeline,weeks" acptfact, only "timeline" acptfact and
            # "timeline,weeks" should be set automatica_lly since there exists a required
            # that has that base.
            self._edit_set_toolroot_acptfactunits(
                base=base, pick=pick, open=open, nigh=nigh
            )

            # Find all AcptFact descendents and any special_road connections "Lemmas"
            lemmas_dict = self._get_lemma_acptfactunits()
            for current_acptfact in self._toolroot._acptfactunits.values():
                for lemma_acptfact in lemmas_dict.values():
                    if lemma_acptfact.base == current_acptfact.base:
                        self._edit_set_toolroot_acptfactunits(
                            base=lemma_acptfact.base,
                            pick=lemma_acptfact.pick,
                            open=lemma_acptfact.open,
                            nigh=lemma_acptfact.nigh,
                        )
                        self._toolroot._acptfactunits[
                            lemma_acptfact.base
                        ] = lemma_acptfact

            for missing_acptfact in self.get_missing_acptfact_bases().keys():
                for lemma_acptfact in lemmas_dict.values():
                    if lemma_acptfact.base == missing_acptfact:
                        self._toolroot._acptfactunits[
                            lemma_acptfact.base
                        ] = lemma_acptfact

        self.set_agent_metrics()

    def _edit_set_toolroot_acptfactunits(
        self, pick: Road, base: Road, open: float, nigh: float
    ):
        acptfactunit = acptfactunit_shop(base=base, pick=pick, open=open, nigh=nigh)
        try:
            acptfact_obj = self._toolroot._acptfactunits[base]
            if pick != None:
                acptfact_obj.set_attr(pick=pick)
            if open != None:
                acptfact_obj.set_attr(open=open)
            if nigh != None:
                acptfact_obj.set_attr(nigh=nigh)
        except KeyError as e:
            self._toolroot._acptfactunits[acptfactunit.base] = acptfactunit

    def get_acptfactunits_base_and_acptfact_list(self):
        acptfact_list = list(self._toolroot._acptfactunits.values())
        node_dict = {
            acptfact_x.base.lower(): acptfact_x for acptfact_x in acptfact_list
        }
        node_lowercase_ordered_list = sorted(list(node_dict))
        node_orginalcase_ordered_list = [
            node_dict[node_l] for node_l in node_lowercase_ordered_list
        ]

        list_x = [["", ""]]
        list_x.extend(
            [acptfact_x.base, acptfact_x.pick]
            for acptfact_x in node_orginalcase_ordered_list
        )
        return list_x

    def del_acptfact(self, base: Road):
        self._set_acptfacts_empty_if_null()
        self._toolroot._acptfactunits.pop(base)

    def get_tree_metrics(self) -> TreeMetrics:
        tree_metrics = TreeMetrics()
        self._toolroot._level = 0
        tree_metrics.evaluate_node(
            level=self._toolroot._level,
            requireds=self._toolroot._requiredunits,
            grouplinks=self._toolroot._grouplinks,
            uid=self._toolroot._uid,
            promise=self._toolroot.promise,
            tool_road=self._toolroot.get_road(),
        )

        tool_list = [self._toolroot]
        while tool_list != []:
            tool_x = tool_list.pop()
            if tool_x._kids != None:
                for tool_kid in tool_x._kids.values():
                    self._eval_tree_metrics(tool_x, tool_kid, tree_metrics, tool_list)
        return tree_metrics

    def _eval_tree_metrics(self, tool_x, tool_kid, tree_metrics, tool_list):
        tool_kid._level = tool_x._level + 1
        tree_metrics.evaluate_node(
            level=tool_kid._level,
            requireds=tool_kid._requiredunits,
            grouplinks=tool_kid._grouplinks,
            uid=tool_kid._uid,
            promise=tool_kid.promise,
            tool_road=tool_kid.get_road(),
        )
        tool_list.append(tool_kid)

    def get_tool_uid_max(self) -> int:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.uid_max

    def set_all_tool_uids_unique(self):
        tree_metrics = self.get_tree_metrics()
        tool_uid_max = tree_metrics.uid_max
        tool_uid_dict = tree_metrics.uid_dict

        for tool_x in self.get_tool_list():
            if tool_x._uid is None or tool_uid_dict.get(tool_x._uid) > 1:
                new_tool_uid_max = tool_uid_max + 1
                self.edit_tool_attr(road=tool_x.get_road(), uid=new_tool_uid_max)
                tool_uid_max = new_tool_uid_max

    def get_node_count(self):
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.nodeCount

    def get_level_count(self, level):
        tree_metrics = self.get_tree_metrics()
        levelCount = None
        try:
            levelCount = tree_metrics.levelCount[level]
        except KeyError:
            levelCount = 0
        return levelCount

    def get_required_bases(self) -> dict[Road:int]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.required_bases

    def get_missing_acptfact_bases(self):
        tree_metrics = self.get_tree_metrics()
        required_bases = tree_metrics.required_bases
        missing_bases = {}
        if self._toolroot._acptfactunits is None:
            missing_bases = required_bases
        elif self._toolroot._acptfactunits != None:
            for base, base_count in required_bases.items():
                try:
                    levelCount = self._toolroot._acptfactunits[base]
                except KeyError:
                    missing_bases[base] = base_count

        return missing_bases

    def add_tool(
        self,
        tool_kid: ToolCore,
        walk: Road,
        create_missing_tools_groups: bool = None,
    ):
        temp_tool = self._toolroot
        _road = walk.split(",")
        temp_road = _road.pop(0)

        # toolroot cannot be replaced
        if temp_road == self._desc and _road == []:
            tool_kid.set_road(parent_road=Road(self._desc))
        else:
            parent_road = [temp_road]
            while _road != []:
                temp_road = _road.pop(0)
                temp_tool = self._get_or_create_leveln_tool(
                    parent_tool=temp_tool, tool_desc=temp_road
                )
                parent_road.append(temp_road)

            tool_kid.set_road(parent_road=",".join(parent_road))

        temp_tool.add_kid(tool_kid)

        if create_missing_tools_groups:
            self._create_missing_tools(road=Road(f"{walk},{tool_kid._desc}"))
            self._create_missing_groups_members(grouplinks=tool_kid._grouplinks)

    def _create_missing_groups_members(self, grouplinks: dict[GroupName:GroupLink]):
        for grouplink_x in grouplinks.values():
            if self._groups.get(grouplink_x.name) is None:
                groupunit_x = groupunit_shop(name=grouplink_x.name, _members={})
                self.set_groupunit(groupunit=groupunit_x)

    def _create_missing_tools(self, road):
        self.set_agent_metrics()
        posted_tool = self.get_tool_kid(road)

        for required_x in posted_tool._requiredunits.values():
            self._set_toolkid_if_empty(road=required_x.base)
            for sufffact_x in required_x.sufffacts.values():
                self._set_toolkid_if_empty(road=sufffact_x.need)
        if posted_tool._special_road != None:
            self._set_toolkid_if_empty(road=posted_tool._special_road)
        if posted_tool._numeric_road != None:
            self._set_toolkid_if_empty(road=posted_tool._numeric_road)

    def _set_toolkid_if_empty(self, road: Road):
        try:
            self.get_tool_kid(road)
        except InvalidAgentException:
            base_tool = ToolKid(
                _desc=get_terminus_node_from_road(road=road),
                _walk=get_walk_from_road(road=road),
            )
            self.add_tool(tool_kid=base_tool, walk=base_tool._walk)

    # def _get_or_create_level1_tool(self, tool_desc: str) -> ToolKid:
    #     return_tool = None
    #     try:
    #         return_tool = self._kids[tool_desc]
    #     except Exception:
    #         KeyError
    #         self.add_kid(ToolKid(_desc=tool_desc))
    #         return_tool = self._kids[tool_desc]

    #     return return_tool

    def _get_or_create_leveln_tool(self, parent_tool: ToolCore, tool_desc: str):
        return_tool = None
        try:
            return_tool = parent_tool._kids[tool_desc]
        except Exception:
            KeyError
            parent_tool.add_kid(ToolKid(_desc=tool_desc))
            return_tool = parent_tool._kids[tool_desc]

        return return_tool

    def del_tool_kid(self, road: Road, del_children: bool = True):
        x_road = road.split(",")
        temp_desc = x_road.pop(0)
        temps_d = [temp_desc]

        if x_road == []:
            raise InvalidAgentException("Object cannot delete itself")
        temp_desc = x_road.pop(0)
        temps_d.append(temp_desc)

        if x_road == []:
            if not del_children:
                d_temp_tool = self.get_tool_kid(road=",".join(temps_d))
                for kid in d_temp_tool._kids.values():
                    self.add_tool(tool_kid=kid, walk=",".join(temps_d[:-1]))
            self._toolroot._kids.pop(temp_desc)
        elif x_road != []:
            i_temp_tool = self._toolroot._kids[temp_desc]
            while x_road != []:
                temp_desc = x_road.pop(0)
                parent_temp_tool = i_temp_tool
                i_temp_tool = i_temp_tool._kids[temp_desc]

            parent_temp_tool._kids.pop(temp_desc)
        self.set_agent_metrics()

    def agent_and_toolroot_desc_edit(self, new_desc):
        self._desc = new_desc
        self.edit_tool_desc(old_road=self._toolroot._desc, new_desc=new_desc)

    def edit_tool_desc(
        self,
        old_road: Road,
        new_desc: str,
    ):
        # confirm tool exists
        if self.get_tool_kid(road=old_road) is None:
            raise InvalidAgentException(f"Tool {old_road=} does not exist")

        walk = get_walk_from_road(road=old_road)
        new_road = road_validate(Road(f"{walk},{new_desc}"))

        if old_road != new_road:
            # if root _desc is changed
            if walk == "":
                self._toolroot._desc = new_desc
                self._toolroot._walk = walk
            else:
                self._non_root_tool_desc_edit(old_road, new_desc, walk)
            self._toolroot_find_replace_road(old_road=old_road, new_road=new_road)
            self._set_acptfacts_empty_if_null()
            self._toolroot._acptfactunits = find_replace_road_key_dict(
                dict_x=self._toolroot._acptfactunits,
                old_road=old_road,
                new_road=new_road,
            )

    def _non_root_tool_desc_edit(self, old_road, new_desc, walk):
        tool_z = self.get_tool_kid(road=old_road)
        tool_z._desc = new_desc
        tool_z._walk = walk
        tool_parent = self.get_tool_kid(road=get_walk_from_road(old_road))
        tool_parent._kids.pop(get_terminus_node_from_road(old_road))
        tool_parent._kids[tool_z._desc] = tool_z

    def _toolroot_find_replace_road(self, old_road, new_road):
        self._toolroot.find_replace_road(old_road=old_road, new_road=new_road)

        tool_iter_list = [self._toolroot]
        while tool_iter_list != []:
            listed_tool = tool_iter_list.pop()
            # put all tool_children in tool list
            if listed_tool._kids != None:
                for tool_kid in listed_tool._kids.values():
                    tool_iter_list.append(tool_kid)
                    if is_sub_road_in_src_road(
                        src_road=tool_kid._walk,
                        sub_road=old_road,
                    ):
                        tool_kid._walk = change_road(
                            current_road=tool_kid._walk,
                            old_road=old_road,
                            new_road=new_road,
                        )
                    tool_kid.find_replace_road(old_road=old_road, new_road=new_road)

    def get_begin_close_if_denom_or_numeric_road(
        self,
        begin: float,
        close: float,
        addin: float,
        numor: float,
        denom: float,
        reest: bool,
        tool_road: Road,
        numeric_road: Road,
    ):
        anc_roads = get_ancestor_roads(road=tool_road)
        if (addin != None or numor != None or denom != None or reest != None) and len(
            anc_roads
        ) == 1:
            raise InvalidAgentException("Root Tool cannot have numor denom reest.")
        parent_road = self._desc if len(anc_roads) == 1 else anc_roads[1]

        parent_has_range = None
        parent_tool_x = self.get_tool_kid(road=parent_road)
        parent_begin = parent_tool_x._begin
        parent_close = parent_tool_x._close
        parent_has_range = parent_begin is not None and parent_close is not None

        numeric_begin = None
        numeric_close = None
        numeric_range = None
        if numeric_road != None:
            numeric_tool_x = self.get_tool_kid(road=numeric_road)
            numeric_begin = numeric_tool_x._begin
            numeric_close = numeric_tool_x._close
            numeric_range = numeric_begin != None and numeric_close != None

        if parent_has_range and addin not in [None, 0]:
            parent_begin = parent_begin + addin
            parent_close = parent_close + addin

        begin, close = self._transform_begin_close(
            reest=reest,
            begin=begin,
            close=close,
            numor=numor,
            denom=denom,
            parent_has_range=parent_has_range,
            parent_begin=parent_begin,
            parent_close=parent_close,
            numeric_range=numeric_range,
            numeric_begin=numeric_begin,
            numeric_close=numeric_close,
        )

        if parent_has_range and numeric_range:
            raise InvalidAgentException(
                "Tool has begin-close range parent, cannot have numeric_road"
            )
        elif not parent_has_range and not numeric_range and numor != None:
            raise InvalidAgentException(
                f"Tool cannot edit {numor=}/denom/reest of '{tool_road}' if parent '{parent_road}' or toolcore._numeric_road does not have begin/close range"
            )
        return begin, close

    def _transform_begin_close(
        self,
        reest,
        begin,
        close,
        numor,
        denom,
        parent_has_range,
        parent_begin,
        parent_close,
        numeric_range,
        numeric_begin,
        numeric_close,
    ):
        if not reest and parent_has_range and numor != None:
            begin = parent_begin * numor / denom
            close = parent_close * numor / denom
        elif not reest and parent_has_range and numor is None:
            begin = parent_begin
            close = parent_close
        elif not reest and numeric_range and numor != None:
            begin = numeric_begin * numor / denom
            close = numeric_close * numor / denom
        elif not reest and numeric_range and numor is None:
            begin = numeric_begin
            close = numeric_close
        elif reest and parent_has_range and numor != None:
            begin = parent_begin * numor % denom
            close = parent_close * numor % denom
        elif reest and parent_has_range and numor is None:
            begin = 0
            close = parent_close - parent_begin
        elif reest and numeric_range and numor != None:
            begin = numeric_begin * numor % denom
            close = numeric_close * numor % denom
        elif reest and numeric_range and numor is None:
            begin = 0
            close = parent_close - parent_begin
        else:
            begin = begin
            close = close

        return begin, close

    def edit_tool_attr(
        self,
        road: Road,
        weight: int = None,
        uid: int = None,
        required: RequiredUnit = None,
        required_base: Road = None,
        required_sufffact: Road = None,
        required_sufffact_open: float = None,
        required_sufffact_nigh: float = None,
        required_sufffact_divisor: int = None,
        required_del_sufffact_base: Road = None,
        required_del_sufffact_need: Road = None,
        required_suff_tool_active_status: str = None,
        begin: float = None,
        close: float = None,
        addin: float = None,
        numor: float = None,
        denom: float = None,
        reest: bool = None,
        numeric_road: Road = None,
        special_road: float = None,
        promise: bool = None,
        problem_bool: bool = None,
        acptfactunit: AcptFactUnit = None,
        descendant_promise_count: int = None,
        all_member_credit: bool = None,
        all_member_debt: bool = None,
        grouplink: GroupLink = None,
        grouplink_del: GroupName = None,
        is_expanded: bool = None,
        on_meld_weight_action: str = None,
    ):  # sourcery skip: low-code-quality
        if denom != None or numor != None or reest or addin != None:
            if addin is None:
                addin = 0
            if denom is None:
                denom = 1
            if numor is None:
                numor = 1
            if reest is None:
                reest = False

        if (
            begin != None
            or close != None
            or numor != None
            or numeric_road != None
            or addin != None
        ):
            begin, close = self.get_begin_close_if_denom_or_numeric_road(
                begin=begin,
                close=close,
                addin=addin,
                numor=numor,
                denom=denom,
                reest=reest,
                tool_road=road,
                numeric_road=numeric_road,
            )

        tool_attr = ToolAttrHolder(
            weight=weight,
            uid=uid,
            required=required,
            required_base=required_base,
            required_sufffact=required_sufffact,
            required_sufffact_open=required_sufffact_open,
            required_sufffact_nigh=required_sufffact_nigh,
            required_sufffact_divisor=required_sufffact_divisor,
            required_del_sufffact_base=required_del_sufffact_base,
            required_del_sufffact_need=required_del_sufffact_need,
            required_suff_tool_active_status=required_suff_tool_active_status,
            begin=begin,
            close=close,
            addin=addin,
            numor=numor,
            denom=denom,
            reest=reest,
            numeric_road=numeric_road,
            special_road=special_road,
            descendant_promise_count=descendant_promise_count,
            all_member_credit=all_member_credit,
            all_member_debt=all_member_debt,
            grouplink=grouplink,
            grouplink_del=grouplink_del,
            is_expanded=is_expanded,
            promise=promise,
            problem_bool=problem_bool,
            on_meld_weight_action=on_meld_weight_action,
        )
        if tool_attr.required_sufffact != None:
            suffact_tool = self.get_tool_kid(road=required_sufffact)
            tool_attr.set_sufffact_range_attributes_influenced_by_sufffact_tool(
                sufffact_open=suffact_tool._begin,
                sufffact_nigh=suffact_tool._close,
                # suffact_numor=suffact_tool.anc_numor,
                sufffact_denom=suffact_tool._denom,
                # anc_reest=suffact_tool.anc_reest,
            )
        temp_tool = self.get_tool_kid(road=road)
        temp_tool._set_tool_attr(tool_attr=tool_attr)
        if f"{type(temp_tool)}".find("'.tool.ToolRoot'>") <= 0:
            temp_tool._set_toolkid_attr(acptfactunit=acptfactunit)

        # deleting a grouplink reqquires a tree traverse to correctly set groupheirs and grouplines
        if grouplink_del != None or grouplink != None:
            self.set_agent_metrics()

    def del_tool_required_sufffact(
        self, road: Road, required_base: Road, required_sufffact: Road
    ):
        self.edit_tool_attr(
            road=road,
            required_del_sufffact_base=required_base,
            required_del_sufffact_need=required_sufffact,
        )

    def _set_acptfacts_empty_if_null(self):
        self._toolroot.set_acptfactunits_empty_if_null()

    def get_agenda_items(
        self, base: Road = None, agenda_todo: bool = True, agenda_state: bool = True
    ) -> list[ToolCore]:
        return [
            tool for tool in self.get_tool_list() if tool.is_agenda_item(base_x=base)
        ]

    def set_agenda_task_complete(self, task_road: Road, base: Road):
        promise_item = self.get_tool_kid(road=task_road)
        promise_item.set_acptfactunit_to_complete(
            base_acptfactunit=self._toolroot._acptfactunits[base]
        )

    def get_memberunit_total_creditor_weight(self):
        return sum(
            memberunit.get_creditor_weight() for memberunit in self._members.values()
        )

    def get_memberunit_total_debtor_weight(self):
        return sum(
            memberunit.get_debtor_weight() for memberunit in self._members.values()
        )

    def _add_to_memberunits_agent_credit_debt(self, tool_agent_importance: float):
        sum_memberunit_creditor_weight = self.get_memberunit_total_creditor_weight()
        sum_memberunit_debtor_weight = self.get_memberunit_total_debtor_weight()

        for memberunit_x in self._members.values():
            au_agent_credit = (
                tool_agent_importance * memberunit_x.get_creditor_weight()
            ) / sum_memberunit_creditor_weight

            au_agent_debt = (
                tool_agent_importance * memberunit_x.get_debtor_weight()
            ) / sum_memberunit_debtor_weight

            memberunit_x.add_agent_credit_debt(
                agent_credit=au_agent_credit,
                agent_debt=au_agent_debt,
                agent_agenda_credit=0,
                agent_agenda_debt=0,
            )

    def _add_to_memberunits_agent_agenda_credit_debt(
        self, tool_agent_importance: float
    ):
        sum_memberunit_creditor_weight = self.get_memberunit_total_creditor_weight()
        sum_memberunit_debtor_weight = self.get_memberunit_total_debtor_weight()

        for memberunit_x in self._members.values():
            au_agent_agenda_credit = (
                tool_agent_importance * memberunit_x.get_creditor_weight()
            ) / sum_memberunit_creditor_weight

            au_agent_agenda_debt = (
                tool_agent_importance * memberunit_x.get_debtor_weight()
            ) / sum_memberunit_debtor_weight

            memberunit_x.add_agent_credit_debt(
                agent_credit=0,
                agent_debt=0,
                agent_agenda_credit=au_agent_agenda_credit,
                agent_agenda_debt=au_agent_agenda_debt,
            )

    def _set_memberunits_agent_agenda_importance(self, agent_agenda_importance: float):
        sum_memberunit_creditor_weight = self.get_memberunit_total_creditor_weight()
        sum_memberunit_debtor_weight = self.get_memberunit_total_debtor_weight()

        for memberunit_x in self._members.values():
            au_agent_agenda_credit = (
                agent_agenda_importance * memberunit_x.get_creditor_weight()
            ) / sum_memberunit_creditor_weight

            au_agent_agenda_debt = (
                agent_agenda_importance * memberunit_x.get_debtor_weight()
            ) / sum_memberunit_debtor_weight

            memberunit_x.add_agent_agenda_credit_debt(
                agent_agenda_credit=au_agent_agenda_credit,
                agent_agenda_debt=au_agent_agenda_debt,
            )

    def _reset_groupunits_agent_credit_debt(self):
        self.set_groupunits_empty_if_null()
        for grouplink_obj in self._groups.values():
            grouplink_obj.reset_agent_credit_debt()

    def _set_groupunits_agent_importance(self, groupheirs: dict[GroupName:GroupLink]):
        self.set_groupunits_empty_if_null()
        for grouplink_obj in groupheirs.values():
            self.add_to_group_agent_credit_debt(
                groupname=grouplink_obj.name,
                groupheir_agent_credit=grouplink_obj._agent_credit,
                groupheir_agent_debt=grouplink_obj._agent_debt,
            )

    def _distribute_agent_agenda_importance(self):
        for tool in self._tool_dict.values():
            # If there are no grouplines associated with tool
            # distribute agent_importance via general memberunit
            # credit ratio and debt ratio
            # if tool.is_agenda_item() and tool._grouplines == {}:
            if tool.is_agenda_item():
                if tool._grouplines == {}:
                    self._add_to_memberunits_agent_agenda_credit_debt(
                        tool._agent_importance
                    )
                else:
                    for groupline_x in tool._grouplines.values():
                        self.add_to_group_agent_agenda_credit_debt(
                            groupname=groupline_x.name,
                            groupline_agent_credit=groupline_x._agent_credit,
                            groupline_agent_debt=groupline_x._agent_debt,
                        )

    def _distribute_groups_agent_importance(self):
        for group_obj in self._groups.values():
            group_obj._set_memberlink_agent_credit_debt()
            for memberlink in group_obj._members.values():
                self.add_to_memberunit_agent_credit_debt(
                    memberunit_name=memberlink.name,
                    agent_credit=memberlink._agent_credit,
                    agent_debt=memberlink._agent_debt,
                    agent_agenda_credit=memberlink._agent_agenda_credit,
                    agent_agenda_debt=memberlink._agent_agenda_debt,
                )

    def _set_agent_agenda_ratio_credit_debt(self):
        agent_agenda_ratio_credit_sum = 0
        agent_agenda_ratio_debt_sum = 0

        for memberunit_x in self._members.values():
            agent_agenda_ratio_credit_sum += memberunit_x._agent_agenda_credit
            agent_agenda_ratio_debt_sum += memberunit_x._agent_agenda_debt

        for memberunit_x in self._members.values():
            memberunit_x.set_agent_agenda_ratio_credit_debt(
                agent_agenda_ratio_credit_sum=agent_agenda_ratio_credit_sum,
                agent_agenda_ratio_debt_sum=agent_agenda_ratio_debt_sum,
                agent_memberunit_total_creditor_weight=self.get_memberunit_total_creditor_weight(),
                agent_memberunit_total_debtor_weight=self.get_memberunit_total_debtor_weight(),
            )

    def get_member_groups(self, member_name: MemberName):
        groups = []
        for group in self._groups.values():
            groups.extend(
                group.name
                for memberlink in group._members.values()
                if memberlink.name == member_name
            )

        return groups

    def _reset_memberunit_agent_credit_debt(self):
        self.set_members_empty_if_null()
        for memberunit in self._members.values():
            memberunit.reset_agent_credit_debt()

    def _toolroot_inherit_requiredheirs(self):
        self._toolroot.set_requiredunits_empty_if_null()
        x_dict = {}
        for required in self._toolroot._requiredunits.values():
            x_required = RequiredHeir(base=required.base, sufffacts=None)
            x_sufffacts = {}
            for w in required.sufffacts.values():
                sufffact_x = sufffactunit_shop(
                    need=w.need,
                    open=w.open,
                    nigh=w.nigh,
                    divisor=w.divisor,
                )
                x_sufffacts[sufffact_x.need] = sufffact_x
            x_required.sufffacts = x_sufffacts
            x_dict[x_required.base] = x_required
        self._toolroot._requiredheirs = x_dict

    def get_tool_kid(self, road: Road) -> ToolKid:
        if road is None:
            raise InvalidAgentException("get_tool_kid received road=None")
        nodes = road.split(",")
        src = nodes.pop(0)
        temp_tool = None

        if nodes == [] and src == self._toolroot._desc:
            temp_tool = self._toolroot
            # raise InvalidAgentException(f"Cannot return root '{src}'")
        else:
            tool_desc = src if nodes == [] else nodes.pop(0)
            try:
                temp_tool = self._toolroot._kids.get(tool_desc)

                while nodes != []:
                    tool_desc = nodes.pop(0)
                    temp_tool = temp_tool._kids[tool_desc]
                if temp_tool is None:
                    raise InvalidAgentException(
                        f"Temp_tool is None {tool_desc=}. No item at '{road}'"
                    )
            except:
                raise InvalidAgentException(
                    f"Getting {tool_desc=} failed no item at '{road}'"
                )

        return temp_tool

    def get_tool_ranged_kids(
        self, tool_road: str, begin: float = None, close: float = None
    ) -> dict[ToolCore]:
        parent_tool = self.get_tool_kid(road=tool_road)
        if begin is None and close is None:
            begin = parent_tool._begin
            close = parent_tool._close
        elif begin != None and close is None:
            close = begin

        tool_list = parent_tool.get_kids_in_range(begin=begin, close=close)
        return {tool_x._desc: tool_x for tool_x in tool_list}

    def _set_ancestor_metrics(self, road: Road):
        # sourcery skip: low-code-quality
        da_count = 0
        child_grouplines = None
        if road is None:
            road = ""

        group_everyone = None
        if len(road.split(",")) <= 1:
            group_everyone = self._toolroot._groupheirs in [None, {}]
        else:
            ancestor_roads = get_ancestor_roads(road=road)
            # remove root road
            ancestor_roads.pop(len(ancestor_roads) - 1)

            while ancestor_roads != []:
                # youngest_untouched_tool
                yu_tool_obj = self.get_tool_kid(road=ancestor_roads.pop(0))
                yu_tool_obj.set_descendant_promise_count_zero_if_null()
                yu_tool_obj._descendant_promise_count += da_count
                if yu_tool_obj.is_kidless():
                    yu_tool_obj.set_kidless_grouplines()
                    child_grouplines = yu_tool_obj._grouplines
                else:
                    yu_tool_obj.set_grouplines(child_grouplines=child_grouplines)

                if yu_tool_obj._task == True:
                    da_count += 1

                if (
                    group_everyone != False
                    and yu_tool_obj._all_member_credit != False
                    and yu_tool_obj._all_member_debt != False
                    and yu_tool_obj._groupheirs != {}
                    or group_everyone != False
                    and yu_tool_obj._all_member_credit == False
                    and yu_tool_obj._all_member_debt == False
                ):
                    group_everyone = False
                elif group_everyone != False:
                    group_everyone = True
                yu_tool_obj._all_member_credit = group_everyone
                yu_tool_obj._all_member_debt = group_everyone

            if (
                group_everyone != False
                and self._toolroot._all_member_credit != False
                and self._toolroot._all_member_debt != False
                and self._toolroot._groupheirs != {}
                or group_everyone != False
                and self._toolroot._all_member_credit == False
                and self._toolroot._all_member_debt == False
            ):
                group_everyone = False
            elif group_everyone != False and yu_tool_obj._groupheirs == {}:
                group_everyone = True

        self._toolroot._all_member_credit = group_everyone
        self._toolroot._all_member_debt = group_everyone

        if self._toolroot.is_kidless():
            self._toolroot.set_kidless_grouplines()
        else:
            self._toolroot.set_grouplines(child_grouplines=child_grouplines)
        self._toolroot.set_descendant_promise_count_zero_if_null()
        self._toolroot._descendant_promise_count += da_count

    def _set_root_attributes(self):
        self._toolroot._level = 0
        self._toolroot.set_road(parent_road="")
        self._toolroot.set_requiredheirs(
            requiredheirs=self._toolroot._requiredunits, agent_tool_dict=self._tool_dict
        )
        self._toolroot.inherit_groupheirs()
        self._toolroot.clear_grouplines()
        self._toolroot.set_acptfactunits_empty_if_null()
        self._toolroot._weight = 1
        self._toolroot._kids_total_weight = 0
        self._toolroot.set_kids_total_weight()
        self._toolroot.set_sibling_total_weight(1)
        self._toolroot.set_agent_importance(coin_onset_x=0, parent_coin_cease=1)
        self._toolroot.set_groupheirs_agent_credit_debit()
        self._toolroot.set_ancestor_promise_count(0, False)
        self._toolroot.clear_descendant_promise_count()
        self._toolroot.clear_all_member_credit_debt()
        self._toolroot.promise = False

        if self._toolroot.is_kidless():
            self._set_ancestor_metrics(road=self._toolroot._walk)
            self._distribute_agent_importance(tool=self._toolroot)

    def _set_kids_attributes(
        self,
        tool_kid: ToolKid,
        coin_onset: float,
        parent_coin_cease: float,
        parent_tool: ToolKid = None,
    ) -> ToolKid:
        parent_acptfacts = None
        parent_requiredheirs = None

        if parent_tool is None:
            parent_tool = self._toolroot
            parent_acptfacts = self._toolroot._acptfactunits
            parent_requiredheirs = self._toolroot_inherit_requiredheirs()
        else:
            parent_acptfacts = parent_tool._acptfactheirs
            parent_requiredheirs = parent_tool._requiredheirs

        tool_kid.set_level(parent_level=parent_tool._level)
        tool_kid.set_road(parent_road=parent_tool._walk, parent_desc=parent_tool._desc)
        tool_kid.set_acptfactunits_empty_if_null()
        tool_kid.set_acptfactheirs(acptfacts=parent_acptfacts)
        tool_kid.set_requiredheirs(parent_requiredheirs, self._tool_dict)
        tool_kid.inherit_groupheirs(parent_groupheirs=parent_tool._groupheirs)
        tool_kid.clear_grouplines()
        tool_kid.set_active_status(tree_traverse_count=self._tree_traverse_count)
        tool_kid.set_sibling_total_weight(parent_tool._kids_total_weight)
        # tool_kid.set_agent_importance(
        #     parent_agent_importance=parent_tool._agent_importance,
        #     coin_onset_x=coin_onset_x,
        #     parent_coin_cease=parent_tool._agent_coin_cease,
        # )
        tool_kid.set_agent_importance(
            coin_onset_x=coin_onset,
            parent_agent_importance=parent_tool._agent_importance,
            parent_coin_cease=parent_coin_cease,
        )
        tool_kid.set_ancestor_promise_count(
            parent_tool._ancestor_promise_count, parent_tool.promise
        )
        tool_kid.clear_descendant_promise_count()
        tool_kid.clear_all_member_credit_debt()

        if tool_kid.is_kidless():
            # set tool's ancestor metrics using agent root as common reference
            self._set_ancestor_metrics(road=tool_kid.get_road())
            self._distribute_agent_importance(tool=tool_kid)

    def _distribute_agent_importance(self, tool: ToolCore):
        # TODO manage situations where groupheir.creditor_weight is None for all groupheirs
        # TODO manage situations where groupheir.debtor_weight is None for all groupheirs
        if tool.is_groupheirless() == False:
            self._set_groupunits_agent_importance(groupheirs=tool._groupheirs)
        elif tool.is_groupheirless():
            self._add_to_memberunits_agent_credit_debt(
                tool_agent_importance=tool._agent_importance
            )

    def get_agent_importance(
        self, parent_agent_importance: float, weight: int, sibling_total_weight: int
    ):
        sibling_ratio = weight / sibling_total_weight
        return parent_agent_importance * sibling_ratio

    def get_tool_list(self):
        self.set_agent_metrics()
        return list(self._tool_dict.values())

    def set_agent_metrics(self):
        self._set_acptfacts_empty_if_null()

        self._rational = False
        self._tree_traverse_count = 0
        self._tool_dict = {self._toolroot.get_road(): self._toolroot}

        while (
            not self._rational and self._tree_traverse_count < self._max_tree_traverse
        ):
            self._execute_tree_traverse()
            self._run_after_each_tree_traverse()
            self._tree_traverse_count += 1
        self._run_after_tool_all_tree_traverses()

    def _execute_tree_traverse(self):
        self._run_before_tool_tree_traverse()
        self._set_root_attributes()

        coin_onset = self._toolroot._agent_coin_onset
        parent_coin_cease = self._toolroot._agent_coin_cease

        cache_tool_list = []
        for tool_kid in self._toolroot._kids.values():
            self._set_kids_attributes(
                tool_kid=tool_kid,
                coin_onset=coin_onset,
                parent_coin_cease=parent_coin_cease,
            )
            cache_tool_list.append(tool_kid)
            coin_onset += tool_kid._agent_importance

        # no function recursion, recursion by iterateing over list that can be added to by iterations
        while cache_tool_list != []:
            parent_tool = cache_tool_list.pop()
            if self._tree_traverse_count == 0:
                self._tool_dict[parent_tool.get_road()] = parent_tool

            if parent_tool._kids != None:
                coin_onset = parent_tool._agent_coin_onset
                parent_coin_cease = parent_tool._agent_coin_cease
                for tool_kid in parent_tool._kids.values():
                    self._set_kids_attributes(
                        tool_kid=tool_kid,
                        coin_onset=coin_onset,
                        parent_coin_cease=parent_coin_cease,
                        parent_tool=parent_tool,
                    )
                    cache_tool_list.append(tool_kid)
                    coin_onset += tool_kid._agent_importance

    def _run_after_each_tree_traverse(self):
        any_tool_active_status_changed = False
        for tool in self._tool_dict.values():
            tool.set_active_status_hx_empty_if_null()
            if tool._active_status_hx.get(self._tree_traverse_count) != None:
                any_tool_active_status_changed = True

        if any_tool_active_status_changed == False:
            self._rational = True

    def _run_after_tool_all_tree_traverses(self):
        self._distribute_agent_agenda_importance()
        self._distribute_groups_agent_importance()
        self._set_agent_agenda_ratio_credit_debt()

    def _run_before_tool_tree_traverse(self):
        self._reset_groupunits_agent_credit_debt()
        self._reset_groupunits_agent_credit_debt()
        self._reset_memberunit_agent_credit_debt()

    def get_heir_road_list(self, src_road: Road):
        # create list of all tool roads (road+desc)
        return [
            road
            for road in self.get_tool_tree_ordered_road_list()
            if road.find(src_road) == 0
        ]

    def get_tool_tree_ordered_road_list(self, no_range_descendents: bool = False):
        tool_list = self.get_tool_list()
        node_dict = {tool.get_road().lower(): tool.get_road() for tool in tool_list}
        node_lowercase_ordered_list = sorted(list(node_dict))
        node_orginalcase_ordered_list = [
            node_dict[node_l] for node_l in node_lowercase_ordered_list
        ]

        list_x = []
        for road in node_orginalcase_ordered_list:
            if not no_range_descendents:
                list_x.append(road)
            else:
                anc_list = get_ancestor_roads(road=road)
                if len(anc_list) == 1:
                    list_x.append(road)
                elif len(anc_list) == 2:
                    if self._toolroot._begin is None and self._toolroot._close is None:
                        list_x.append(road)
                else:
                    parent_tool = self.get_tool_kid(road=anc_list[1])
                    if parent_tool._begin is None and parent_tool._close is None:
                        list_x.append(road)

        return list_x

    def get_acptfactunits_dict(self):
        x_dict = {}
        if self._toolroot._acptfactunits != None:
            for acptfact_road, acptfact_obj in self._toolroot._acptfactunits.items():
                x_dict[acptfact_road] = acptfact_obj.get_dict()
        return x_dict

    def get_members_dict(self):
        x_dict = {}
        if self._members != None:
            for member_name, member_obj in self._members.items():
                x_dict[member_name] = member_obj.get_dict()
        return x_dict

    def groupunit_shops_dict(self):
        x_dict = {}
        if self._groups != None:
            for group_name, group_obj in self._groups.items():
                x_dict[group_name] = group_obj.get_dict()
        return x_dict

    def get_dict(self):
        self.set_agent_metrics()
        return {
            "_kids": self._toolroot.get_kids_dict(),
            "_requiredunits": self._toolroot.get_requiredunits_dict(),
            "_acptfactunits": self.get_acptfactunits_dict(),
            "_members": self.get_members_dict(),
            "_groups": self.groupunit_shops_dict(),
            "_grouplinks": self._toolroot.get_grouplinks_dict(),
            "_weight": self._weight,
            "_desc": self._desc,
            "_uid": self._toolroot._uid,
            "_begin": self._toolroot._begin,
            "_close": self._toolroot._close,
            "_addin": self._toolroot._addin,
            "_numor": self._toolroot._numor,
            "_denom": self._toolroot._denom,
            "_reest": self._toolroot._reest,
            "_problem_bool": self._toolroot._problem_bool,
            "_is_expanded": self._toolroot._is_expanded,
            "_special_road": self._toolroot._special_road,
            "_numeric_road": self._toolroot._numeric_road,
            "_on_meld_weight_action": self._toolroot._on_meld_weight_action,
            "_max_tree_traverse": self._max_tree_traverse,
        }

    def get_json(self):
        x_dict = self.get_dict()
        return x_get_json(dict_x=x_dict)

    def set_time_hreg_tools(self, c400_count):
        toolbase_list = _get_time_hreg_src_tool(c400_count=c400_count)
        while len(toolbase_list) != 0:
            yb = toolbase_list.pop(0)
            special_road_x = None
            if yb.sr != None:
                special_road_x = f"{self._desc},{yb.sr}"

            tool_x = ToolKid(
                _desc=yb.n,
                _begin=yb.b,
                _close=yb.c,
                _weight=yb.weight,
                _is_expanded=False,
                _addin=yb.a,
                _numor=yb.mn,
                _denom=yb.md,
                _reest=yb.mr,
                _special_road=special_road_x,
            )
            road_x = f"{self._desc},{yb.rr}"
            self.add_tool(tool_kid=tool_x, walk=road_x)

            numeric_road_x = None
            if yb.nr != None:
                numeric_road_x = f"{self._desc},{yb.nr}"
                self.edit_tool_attr(
                    road=f"{road_x},{yb.n}", numeric_road=numeric_road_x
                )
            if yb.a != None:
                self.edit_tool_attr(
                    road=f"{road_x},{yb.n}", addin=yb.a, denom=yb.md, numor=yb.mn
                )

        self.set_agent_metrics()

    def get_agent4member(
        self, member_name: MemberName, acptfacts: dict[Road:AcptFactCore]
    ):
        self.set_agent_metrics()
        agent4member = AgentUnit(_desc=member_name)
        agent4member._toolroot._agent_importance = self._toolroot._agent_importance
        # get member's members: memberzone

        # get memberzone groups
        member_groups = self.get_member_groups(member_name=member_name)

        # set agent4member by traversing the tool tree and selecting associated groups
        # set root
        not_included_agent_importance = 0
        agent4member._toolroot._kids = {}
        for ykx in self._toolroot._kids.values():
            y4a_included = any(
                group_ancestor.name in member_groups
                for group_ancestor in ykx._grouplines.values()
            )

            if y4a_included:
                y4a_new = ToolKid(
                    _desc=ykx._desc,
                    _agent_importance=ykx._agent_importance,
                    _requiredunits=ykx._requiredunits,
                    _grouplinks=ykx._grouplinks,
                    _begin=ykx._begin,
                    _close=ykx._close,
                    promise=ykx.promise,
                    _task=ykx._task,
                )
                agent4member._toolroot._kids[ykx._desc] = y4a_new
            else:
                not_included_agent_importance += ykx._agent_importance

        if not_included_agent_importance > 0:
            y4a_other = ToolKid(
                _desc="__other__",
                _agent_importance=not_included_agent_importance,
            )
            agent4member._toolroot._kids[y4a_other._desc] = y4a_other

        return agent4member

    # def get_agenda_items(
    #     self, agenda_todo: bool = True, agenda_state: bool = True, base: Road = None
    # ) -> list[ToolCore]:
    #     return list(self.get_agenda_items(base=base))

    def set_dominate_promise_tool(self, tool_kid: ToolKid):
        tool_kid.promise = True
        self.add_tool(
            tool_kid=tool_kid,
            walk=Road(f"{tool_kid._walk}"),
            create_missing_tools_groups=True,
        )

    def get_tool_list_without_toolroot(self):
        x_list = self.get_tool_list()
        x_list.pop(0)
        return x_list

    def make_meldable(self, starting_digest_agent):
        self.edit_tool_desc(
            old_road=Road(f"{self._toolroot._desc}"),
            new_desc=starting_digest_agent._toolroot._desc,
        )

    def meld(self, other_agent):
        self.meld_groups(other_agent=other_agent)
        self.meld_members(other_agent=other_agent)
        self.meld_toolroot(other_agent=other_agent)
        self.meld_acptfacts(other_agent=other_agent)
        self._weight = get_meld_weight(
            src_weight=self._weight,
            src_on_meld_weight_action="default",
            other_weight=other_agent._weight,
            other_on_meld_weight_action="default",
        )

    def meld_toolroot(self, other_agent):
        self._toolroot.meld(other_tool=other_agent._toolroot, _toolroot=True)
        o_tool_list = other_agent.get_tool_list_without_toolroot()
        for oyx in o_tool_list:
            o_road = road_validate(f"{oyx._walk},{oyx._desc}")
            try:
                main_tool = self.get_tool_kid(o_road)
                main_tool.meld(other_tool=oyx)
            except Exception:
                self.add_tool(walk=oyx._walk, tool_kid=oyx)

    def meld_members(self, other_agent):
        self.set_members_empty_if_null()
        other_agent.set_members_empty_if_null()
        for memberunit in other_agent._members.values():
            if self._members.get(memberunit.name) is None:
                self.set_memberunit(memberunit=memberunit)
            else:
                self._members.get(memberunit.name).meld(memberunit)

    def meld_groups(self, other_agent):
        self.set_groupunits_empty_if_null()
        other_agent.set_groupunits_empty_if_null()
        for brx in other_agent._groups.values():
            if self._groups.get(brx.name) is None:
                self.set_groupunit(groupunit=brx)
            else:
                self._groups.get(brx.name).meld(brx)

    def meld_acptfacts(self, other_agent):
        self._set_acptfacts_empty_if_null()
        other_agent._set_acptfacts_empty_if_null()
        for hx in other_agent._toolroot._acptfactunits.values():
            if self._toolroot._acptfactunits.get(hx.base) is None:
                self.set_acptfact(
                    base=hx.base, acptfact=hx.acptfact, open=hx.open, nigh=hx.nigh
                )
            else:
                self._toolroot._acptfactunits.get(hx.base).meld(hx)


# class Agentshop:
def get_from_json(lw_json: str) -> AgentUnit:
    return get_from_dict(lw_dict=json.loads(lw_json))


def get_from_dict(lw_dict: dict) -> AgentUnit:
    c_x = AgentUnit()
    c_x._toolroot._requiredunits = requireds_get_from_dict(
        requireds_dict=lw_dict["_requiredunits"]
    )
    c_x._toolroot._acptfactunits = acptfactunits_get_from_dict(
        x_dict=lw_dict["_acptfactunits"]
    )
    c_x._groups = groupunits_get_from_dict(x_dict=lw_dict["_groups"])
    c_x._toolroot._grouplinks = grouplinks_get_from_dict(x_dict=lw_dict["_grouplinks"])
    c_x._members = memberunits_get_from_dict(x_dict=lw_dict["_members"])
    c_x._desc = lw_dict["_desc"]
    c_x._toolroot._desc = lw_dict["_desc"]
    c_x._weight = lw_dict["_weight"]
    c_x._max_tree_traverse = lw_dict.get("_max_tree_traverse")
    if lw_dict.get("_max_tree_traverse") is None:
        c_x._max_tree_traverse = 20
    c_x._toolroot._weight = lw_dict["_weight"]
    c_x._toolroot._uid = lw_dict["_uid"]
    c_x._toolroot._begin = lw_dict["_begin"]
    c_x._toolroot._close = lw_dict["_close"]
    c_x._toolroot._numor = lw_dict["_numor"]
    c_x._toolroot._denom = lw_dict["_denom"]
    c_x._toolroot._reest = lw_dict["_reest"]
    c_x._toolroot._special_road = lw_dict["_special_road"]
    c_x._toolroot._numeric_road = lw_dict["_numeric_road"]
    c_x._toolroot._is_expanded = lw_dict["_is_expanded"]

    tool_dict_list = []
    for x_dict in lw_dict["_kids"].values():
        x_dict["temp_road"] = c_x._desc
        tool_dict_list.append(x_dict)

    while tool_dict_list != []:
        tool_dict = tool_dict_list.pop(0)
        for x_dict in tool_dict["_kids"].values():
            temp_road = tool_dict["temp_road"]
            temp_desc = tool_dict["_desc"]
            x_dict["temp_road"] = f"{temp_road},{temp_desc}"
            tool_dict_list.append(x_dict)

        tool_obj = ToolKid(
            _desc=tool_dict["_desc"],
            _weight=tool_dict["_weight"],
            _uid=tool_dict["_uid"],
            _begin=tool_dict["_begin"],
            _close=tool_dict["_close"],
            _numor=tool_dict["_numor"],
            _denom=tool_dict["_denom"],
            _reest=tool_dict["_reest"],
            promise=tool_dict["promise"],
            _requiredunits=requireds_get_from_dict(
                requireds_dict=tool_dict["_requiredunits"]
            ),
            _grouplinks=grouplinks_get_from_dict(tool_dict["_grouplinks"]),
            _acptfactunits=acptfactunits_get_from_dict(tool_dict["_acptfactunits"]),
            _is_expanded=tool_dict["_is_expanded"],
            _special_road=tool_dict["_special_road"],
            _numeric_road=tool_dict["_numeric_road"],
        )
        c_x.add_tool(tool_kid=tool_obj, walk=tool_dict["temp_road"])

    c_x.set_agent_metrics()  # clean up tree traverse defined fields
    return c_x


def get_dict_of_agent_from_dict(x_dict: dict) -> dict[str:AgentUnit]:
    agentunits = {}
    for agentunit_dict in x_dict.values():
        x_agent = get_from_dict(lw_dict=agentunit_dict)
        agentunits[x_agent._desc] = x_agent
    return agentunits


def get_meld_of_agent_files(agentunit: AgentUnit, dir: str) -> AgentUnit:
    agentunit.set_agent_metrics()
    for bond_file_x in x_func_dir_files(dir_path=dir):
        bond_x = get_from_json(
            lw_json=x_func_open_file(dest_dir=dir, file_name=bond_file_x)
        )
        bond_x.make_meldable(starting_digest_agent=agentunit)
        agentunit.meld(other_agent=bond_x)

    agentunit.set_agent_metrics()
    return agentunit
