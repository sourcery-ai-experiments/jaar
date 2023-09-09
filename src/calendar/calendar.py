import dataclasses
import json
from datetime import datetime
from src.calendar.member import (
    MemberName,
    MemberUnit,
    MemberLink,
    memberunits_get_from_dict,
    memberunit_shop,
    memberlink_shop,
    MemberUnitExternalMetrics,
)
from src.calendar.group import (
    GroupLink,
    GroupName,
    GroupUnit,
    grouplinks_get_from_dict,
    get_from_dict as groupunits_get_from_dict,
    groupunit_shop,
    grouplink_shop,
)
from src.calendar.required_idea import (
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
from src.calendar.required_assign import (
    assigned_heir_shop,
    assigned_unit_shop,
    AssignedUnit,
    AssignedHeir,
    assignedunit_get_from_dict,
)
from src.calendar.tree_metrics import TreeMetrics
from src.calendar.x_func import x_get_json
from src.calendar.idea import IdeaCore, IdeaKid, IdeaRoot, IdeaAttrHolder
from src.calendar.hreg_time import (
    _get_time_hreg_src_idea,
    get_time_min_from_dt as hreg_get_time_min_from_dt,
    convert1440toReadableTime,
    get_number_with_postfix,
    get_jajatime_legible_from_dt,
)
from src.calendar.lemma import Lemmas
from src.calendar.road import (
    get_walk_from_road,
    is_sub_road,
    road_validate,
    change_road,
    get_terminus_node_from_road,
    find_replace_road_key_dict,
    get_ancestor_roads,
    get_global_root_label as root_label,
    get_road_from_nodes,
    get_all_road_nodes,
    get_forefather_roads,
)
from src.calendar.origin import originunit_get_from_dict, originunit_shop, OriginUnit
from copy import deepcopy as copy_deepcopy
from src.calendar.x_func import (
    save_file as x_func_save_file,
    dir_files as x_func_dir_files,
    open_file as x_func_open_file,
    get_meld_weight,
)


class InvalidCalendarException(Exception):
    pass


class AssignmentMemberException(Exception):
    pass


class CalendarOwner(str):
    pass


@dataclasses.dataclass
class CalendarUnit:
    _owner: CalendarOwner = None
    _weight: float = None
    _members: dict[MemberName:MemberUnit] = None
    _groups: dict[GroupName:GroupUnit] = None
    _idearoot: IdeaRoot = None
    _idea_dict: dict[Road:IdeaCore] = None
    _max_tree_traverse: int = 3
    _tree_traverse_count: int = None
    _rational: bool = False
    _originunit: OriginUnit = None

    def __init__(self, _weight: float = None, _owner=None) -> None:
        if _weight is None:
            _weight = 1
        self._weight = _weight
        if _owner is None:
            _owner = ""
        self._idearoot = IdeaRoot(_label=root_label(), _uid=1, _level=0)
        self._owner = _owner
        self._originunit = originunit_shop()

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
            raise InvalidCalendarException(
                f"set_max_tree_traverse: input '{int_x}' must be number that is 2 or greater"
            )
        else:
            self._max_tree_traverse = int_x

    def get_bond_status(self) -> bool:
        self.set_calendar_metrics()
        tree_metrics_x = self.get_tree_metrics()
        if tree_metrics_x.bond_promise_count != 1:
            return False

        promise_idea_road = tree_metrics_x.an_promise_idea_road
        if (
            self._are_all_members_groups_are_in_idea_kid(road=promise_idea_road)
            == False
        ):
            return False

        return self.all_ideas_relevant_to_promise_idea(road=promise_idea_road) != False

    def export_all_bonds(self, dir: str):
        self.set_all_idea_uids_unique()
        self.set_calendar_metrics()
        # dict_x = {}
        for yx in self.get_idea_list():
            if yx.promise:
                cx = self.get_calendar_sprung_from_single_idea(yx.get_road())
                file_name = f"{yx._uid}.json"
                x_func_save_file(
                    dest_dir=dir,
                    file_name=file_name,
                    file_text=cx.get_json(),
                    replace=True,
                )
        return {}

    def get_calendar_sprung_from_single_idea(self, road: Road):
        self.set_calendar_metrics()
        idea_x = self.get_idea_kid(road=road)
        new_weight = self._weight * idea_x._calendar_importance
        cx = CalendarUnit(_owner=self._idearoot._label, _weight=new_weight)

        for road_assc in sorted(list(self._get_relevant_roads({road}))):
            src_yx = self.get_idea_kid(road=road_assc)
            new_yx = copy_deepcopy(src_yx)
            if new_yx._walk != "":
                cx.add_idea(idea_kid=new_yx, walk=new_yx._walk)
            cx.set_calendar_metrics()

        # TODO grab groups
        # TODO grab all group members
        # TODO grab acptfacts
        return cx

    def _get_relevant_roads(self, roads: dict[Road:]) -> dict[Road:str]:
        to_evaluate_list = []
        to_evaluate_hx_dict = {}
        for road_x in roads:
            to_evaluate_list.append(road_x)
            to_evaluate_hx_dict[road_x] = "given"
        evaluated_roads = {}

        # tree_metrics = self.get_tree_metrics()
        # while roads_to_evaluate != [] and count_x <= tree_metrics.node_count:
        # changed because count_x might be wrong way to measure
        # nice to avoid infinite loops from programming errors though...
        while to_evaluate_list != []:
            road_x = to_evaluate_list.pop()

            idea_x = self.get_idea_kid(road=road_x)
            for requiredunit_obj in idea_x._requiredunits.values():
                required_base = requiredunit_obj.base
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=required_base,
                    road_type="requiredunit_base",
                )

            if idea_x._numeric_road != None:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=idea_x._numeric_road,
                    road_type="numeric_road",
                )

            if idea_x._range_source_road != None:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=idea_x._range_source_road,
                    road_type="range_source_road",
                )

            forefather_roads = get_forefather_roads(road_x)
            for forefather_road in forefather_roads:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=forefather_road,
                    road_type="forefather",
                )

            evaluated_roads[road_x] = -1
        return evaluated_roads

    def _evaluate_relevancy(
        self,
        to_evaluate_list: [Road],
        to_evaluate_hx_dict: dict[Road:int],
        to_evaluate_road: Road,
        road_type: str,
    ):
        if to_evaluate_hx_dict.get(to_evaluate_road) is None:
            to_evaluate_list.append(to_evaluate_road)
            to_evaluate_hx_dict[to_evaluate_road] = road_type

            if road_type == "requiredunit_base":
                ru_base_idea = self.get_idea_kid(to_evaluate_road)
                for descendant_road in ru_base_idea.get_descendant_roads():
                    self._evaluate_relevancy(
                        to_evaluate_list=to_evaluate_list,
                        to_evaluate_hx_dict=to_evaluate_hx_dict,
                        to_evaluate_road=descendant_road,
                        road_type="requiredunit_descendant",
                    )

    def all_ideas_relevant_to_promise_idea(self, road: Road) -> bool:
        promise_idea_assoc_set = set(self._get_relevant_roads({road}))
        all_ideas_set = set(self.get_idea_tree_ordered_road_list())
        return all_ideas_set == all_ideas_set.intersection(promise_idea_assoc_set)

    def _are_all_members_groups_are_in_idea_kid(self, road: Road) -> bool:
        idea_kid = self.get_idea_kid(road=road)
        # get dict of all idea groupheirs
        groupheir_list = idea_kid._groupheirs.keys()
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

        # check all calendar._members are in groupheir_memberunits
        return len(self._members) == len(groupheir_memberunits)

    def get_time_min_from_dt(self, dt: datetime) -> float:
        return hreg_get_time_min_from_dt(dt=dt)

    def get_time_c400_from_min(self, min: int) -> int:
        c400_idea = self.get_idea_kid(f"{root_label()},time,tech,400 year cycle")
        c400_min = c400_idea._close
        return int(min / c400_min), c400_idea, min % c400_min

    def get_time_c400yr_from_min(self, min: int):
        # given int minutes within 400 year range return year and remainder minutes
        c400_count, c400_idea, c400yr_min = self.get_time_c400_from_min(min=min)
        c100_4_96y = c400_idea.get_kids_in_range(begin=c400yr_min, close=c400yr_min)[0]
        cXXXyr_min = c400yr_min - c100_4_96y._begin

        # identify which range the time is in
        if c100_4_96y._close - c100_4_96y._begin in (
            50492160,
            52596000,
        ):  # 96 year and 100 year spans
            yr4_1461 = self.get_idea_kid(f"{root_label()},time,tech,4year with leap")
            yr4_cycles = int(cXXXyr_min / yr4_1461._close)
            cXyr_min = cXXXyr_min % yr4_1461._close
            yr1_idea = yr4_1461.get_kids_in_range(begin=cXyr_min, close=cXyr_min)[0]
        elif c100_4_96y._close - c100_4_96y._begin == 2102400:
            yr4_1460 = self.get_idea_kid(f"{root_label()},time,tech,4year wo leap")
            yr4_cycles = 0
            yr1_idea = yr4_1460.get_kids_in_range(begin=cXXXyr_min, close=cXXXyr_min)[0]
            cXyr_min = cXXXyr_min % yr4_1460._close

        yr1_rem_min = cXyr_min - yr1_idea._begin
        yr1_idea_begin = int(yr1_idea._label.split("-")[0]) - 1

        c100_4_96y_begin = int(c100_4_96y._label.split("-")[0])
        year_num = c100_4_96y_begin + (4 * yr4_cycles) + yr1_idea_begin
        return year_num, yr1_idea, yr1_rem_min

    def get_time_month_from_min(self, min: int):
        year_num, yr1_idea, yr1_idea_rem_min = self.get_time_c400yr_from_min(min=min)
        yrx = None
        if yr1_idea._close - yr1_idea._begin == 525600:
            yrx = self.get_idea_kid(f"{root_label()},time,tech,365 year")
        elif yr1_idea._close - yr1_idea._begin == 527040:
            yrx = self.get_idea_kid(f"{root_label()},time,tech,366 year")
        mon_x = yrx.get_kids_in_range(begin=yr1_idea_rem_min, close=yr1_idea_rem_min)[0]
        month_rem_min = yr1_idea_rem_min - mon_x._begin
        month_num = int(mon_x._label.split("-")[0])
        day_x = self.get_idea_kid(f"{root_label()},time,tech,day")
        day_num = int(month_rem_min / day_x._close)
        day_rem_min = month_rem_min % day_x._close
        return month_num, day_num, day_rem_min, day_x

    def get_time_hour_from_min(self, min: int):
        month_num, day_num, day_rem_min, day_x = self.get_time_month_from_min(min=min)
        hr_x = day_x.get_kids_in_range(begin=day_rem_min, close=day_rem_min)[0]
        hr_rem_min = day_rem_min - hr_x._begin
        hr_num = int(hr_x._label.split("-")[0])
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

    def get_jajatime_legible_one_time_event(self, jajatime_min: int) -> str:
        dt_x = self.get_time_dt_from_min(min=jajatime_min)
        return get_jajatime_legible_from_dt(dt=dt_x)

    def get_jajatime_repeating_legible_text(
        self, open: float = None, nigh: float = None, divisor: float = None
    ) -> str:
        str_x = "test3"
        if divisor is None:
            str_x = self.get_jajatime_legible_one_time_event(jajatime_min=open)
            # str_x = f"Weekday, monthname monthday year"
        elif divisor != None and divisor % 10080 == 0:
            str_x = self._get_jajatime_week_legible_text(open, divisor)
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

    def _get_jajatime_week_legible_text(self, open: int, divisor: int) -> str:
        open_in_week = open % divisor
        week_road = f"{root_label()},time,tech,week"
        weekday_ideas_dict = self.get_idea_ranged_kids(
            idea_road=week_road, begin=open_in_week
        )
        weekday_idea_node = None
        for idea in weekday_ideas_dict.values():
            weekday_idea_node = idea

        if divisor == 10080:
            return f"every {weekday_idea_node._label} at {convert1440toReadableTime(min1440=open % 1440)}"
        num_with_postfix = get_number_with_postfix(num=divisor // 10080)
        return f"every {num_with_postfix} {weekday_idea_node._label} at {convert1440toReadableTime(min1440=open % 1440)}"

    def get_members_metrics(self):
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.grouplinks_metrics

    def set_members_empty_if_null(self):
        if self._members is None:
            self._members = {}

    def add_to_group_calendar_credit_debt(
        self,
        groupname: GroupName,
        groupheir_calendar_credit: float,
        groupheir_calendar_debt: float,
    ):
        for group in self._groups.values():
            if group.name == groupname:
                group.set_empty_calendar_credit_debt_to_zero()
                group._calendar_credit += groupheir_calendar_credit
                group._calendar_debt += groupheir_calendar_debt

    def add_to_group_calendar_agenda_credit_debt(
        self,
        groupname: GroupName,
        groupline_calendar_credit: float,
        groupline_calendar_debt: float,
    ):
        for group in self._groups.values():
            if (
                group.name == groupname
                and groupline_calendar_credit != None
                and groupline_calendar_debt != None
            ):
                group.set_empty_calendar_credit_debt_to_zero()
                group._calendar_agenda_credit += groupline_calendar_credit
                group._calendar_agenda_debt += groupline_calendar_debt

    def add_to_memberunit_calendar_credit_debt(
        self,
        memberunit_name: MemberName,
        calendar_credit,
        calendar_debt: float,
        calendar_agenda_credit: float,
        calendar_agenda_debt: float,
    ):
        for memberunit in self._members.values():
            if memberunit.name == memberunit_name:
                memberunit.add_calendar_credit_debt(
                    calendar_credit=calendar_credit,
                    calendar_debt=calendar_debt,
                    calendar_agenda_credit=calendar_agenda_credit,
                    calendar_agenda_debt=calendar_agenda_debt,
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
        # future: if member is new check existance of group with member name

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
            raise InvalidCalendarException(
                f"Member '{old_name}' change to '{new_name}' failed since '{new_name}' exists."
            )
        elif (
            not allow_nonsingle_group_overwrite
            and self._groups.get(new_name) != None
            and self._groups.get(new_name)._single_member == False
        ):
            raise InvalidCalendarException(
                f"Member '{old_name}' change to '{new_name}' failed since non-single group '{new_name}' exists."
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
            raise InvalidCalendarException(
                f"Group '{old_name}' change to '{new_name}' failed since '{new_name}' exists."
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
        for idea_x in self.get_idea_list():
            if (
                idea_x._grouplinks.get(new_name) != None
                and idea_x._grouplinks.get(old_name) != None
            ):
                old_grouplink = idea_x._grouplinks.get(old_name)
                old_grouplink.name = new_name
                idea_x._grouplinks.get(new_name).meld(
                    other_grouplink=old_grouplink,
                    other_on_meld_weight_action="sum",
                    src_on_meld_weight_action="sum",
                )

                idea_x.del_grouplink(groupname=old_name)
            elif (
                idea_x._grouplinks.get(new_name) is None
                and idea_x._grouplinks.get(old_name) != None
            ):
                old_grouplink = idea_x._grouplinks.get(old_name)
                new_grouplink = grouplink_shop(
                    name=new_name,
                    creditor_weight=old_grouplink.creditor_weight,
                    debtor_weight=old_grouplink.debtor_weight,
                )
                idea_x.set_grouplink(grouplink=new_grouplink)
                idea_x.del_grouplink(groupname=old_name)

    def get_groupunits_name_list(self):
        groupname_list = list(self._groups.keys())
        groupname_list.append("")
        groupname_dict = {groupname.lower(): groupname for groupname in groupname_list}
        groupname_lowercase_ordered_list = sorted(list(groupname_dict))
        return [groupname_dict[group_l] for group_l in groupname_lowercase_ordered_list]

    def set_time_acptfacts(self, open: datetime = None, nigh: datetime = None) -> None:
        open_minutes = self.get_time_min_from_dt(dt=open) if open != None else None
        nigh_minutes = self.get_time_min_from_dt(dt=nigh) if nigh != None else None
        minutes_acptfact = f"{root_label()},time,jajatime"
        self.set_acptfact(
            base=minutes_acptfact,
            pick=minutes_acptfact,
            open=open_minutes,
            nigh=nigh_minutes,
        )

    def _is_idea_rangeroot(self, idea_road: Road) -> bool:
        anc_roads = get_ancestor_roads(road=idea_road)
        parent_road = root_label() if len(anc_roads) == 1 else anc_roads[1]

        # figure out if parent is range
        parent_range = None
        if len(get_all_road_nodes(parent_road)) == 1:
            parent_range = False
        else:
            parent_idea = self.get_idea_kid(road=parent_road)
            parent_range = parent_idea._begin != None and parent_idea._close != None

        # figure out if numeric source exists
        idea_x = self.get_idea_kid(road=idea_road)
        numeric_source_road = None
        numeric_source_road = idea_x._numeric_road != None

        return not numeric_source_road and not parent_range

    def _get_rangeroot_acptfactunits(self):
        return [
            acptfact
            for acptfact in self._idearoot._acptfactunits.values()
            if acptfact.open != None
            and acptfact.nigh != None
            and self._is_idea_rangeroot(idea_road=acptfact.base)
        ]

    def _get_rangeroot_1stlevel_associates(
        self, ranged_acptfactunits: list[IdeaCore]
    ) -> Lemmas:
        lemmas_x = Lemmas()
        lemmas_x.set_empty_if_null()
        # lemma_ideas = {}
        for acptfact in ranged_acptfactunits:
            acptfact_idea = self.get_idea_kid(road=acptfact.base)
            for kid in acptfact_idea._kids.values():
                lemmas_x.eval(idea_x=kid, src_acptfact=acptfact, src_idea=acptfact_idea)

            if acptfact_idea._range_source_road != None:
                lemmas_x.eval(
                    idea_x=self.get_idea_kid(road=acptfact_idea._range_source_road),
                    src_acptfact=acptfact,
                    src_idea=acptfact_idea,
                )
        return lemmas_x

    def _get_lemma_acptfactunits(self) -> dict:
        # get all range-root first level kids and range_source_road
        lemmas_x = self._get_rangeroot_1stlevel_associates(
            self._get_rangeroot_acptfactunits()
        )

        # Now collect associates (all their descendants and range_source_roads)
        lemma_acptfactunits = {}  # acptfact.base : acptfactUnit
        count_x = 0
        while lemmas_x.is_lemmas_evaluated() == False or count_x > 10000:
            count_x += 1
            if count_x == 9998:
                raise InvalidCalendarException("lemma loop failed")

            lemma_y = lemmas_x.get_unevaluated_lemma()
            idea_x = lemma_y.idea_x
            acptfact_x = lemma_y.calc_acptfact

            road_x = f"{idea_x._walk},{idea_x._label}"
            lemma_acptfactunits[road_x] = acptfact_x

            for kid2 in idea_x._kids.values():
                lemmas_x.eval(idea_x=kid2, src_acptfact=acptfact_x, src_idea=idea_x)
            if idea_x._range_source_road not in [None, ""]:
                lemmas_x.eval(
                    idea_x=self.get_idea_kid(road=idea_x._range_source_road),
                    src_acptfact=acptfact_x,
                    src_idea=idea_x,
                )

        return lemma_acptfactunits

    def set_acptfact(
        self,
        base: Road,
        pick: Road,
        open: float = None,
        nigh: float = None,
        create_missing_ideas: bool = None,
    ):  # sourcery skip: low-code-quality
        if create_missing_ideas:
            self._set_ideakid_if_empty(road=base)
            self._set_ideakid_if_empty(road=pick)

        self._set_acptfacts_empty_if_null()
        self._execute_tree_traverse()
        acptfact_idea = self.get_idea_kid(road=base)

        if acptfact_idea._begin is None and acptfact_idea._close is None:
            self._edit_set_idearoot_acptfactunits(
                base=base, pick=pick, open=open, nigh=nigh
            )

        # if acptfact's idea no range or is a "range-root" then allow acptfact to be set by user
        elif (
            acptfact_idea._begin != None
            and acptfact_idea._close != None
            and self._is_idea_rangeroot(idea_road=base) == False
        ):
            raise InvalidCalendarException(
                f"Non range-root acptfact:{base} can only be set by range-root acptfact"
            )

        elif (
            acptfact_idea._begin != None
            and acptfact_idea._close != None
            and self._is_idea_rangeroot(idea_road=base) == True
        ):
            # when idea is "range-root" identify any required.bases that are descendants
            # calculate and set those descendant acptfacts
            # example: timeline range (0-, 1.5e9) is range-root
            # example: "timeline,weeks" (spllt 10080) is range-descendant
            # there exists a required base "timeline,weeks" with sufffact.need = "timeline,weeks"
            # and (1,2) divisor=2 (every other week)
            #
            # user should not set "timeline,weeks" acptfact, only "timeline" acptfact and
            # "timeline,weeks" should be set automatica_lly since there exists a required
            # that has that base.
            self._edit_set_idearoot_acptfactunits(
                base=base, pick=pick, open=open, nigh=nigh
            )

            # Find all AcptFact descendants and any range_source_road connections "Lemmas"
            lemmas_dict = self._get_lemma_acptfactunits()
            for current_acptfact in self._idearoot._acptfactunits.values():
                for lemma_acptfact in lemmas_dict.values():
                    if lemma_acptfact.base == current_acptfact.base:
                        self._edit_set_idearoot_acptfactunits(
                            base=lemma_acptfact.base,
                            pick=lemma_acptfact.pick,
                            open=lemma_acptfact.open,
                            nigh=lemma_acptfact.nigh,
                        )
                        self._idearoot._acptfactunits[
                            lemma_acptfact.base
                        ] = lemma_acptfact

            for missing_acptfact in self.get_missing_acptfact_bases().keys():
                for lemma_acptfact in lemmas_dict.values():
                    if lemma_acptfact.base == missing_acptfact:
                        self._idearoot._acptfactunits[
                            lemma_acptfact.base
                        ] = lemma_acptfact

        self.set_calendar_metrics()

    def _edit_set_idearoot_acptfactunits(
        self, pick: Road, base: Road, open: float, nigh: float
    ):
        acptfactunit = acptfactunit_shop(base=base, pick=pick, open=open, nigh=nigh)
        try:
            acptfact_obj = self._idearoot._acptfactunits[base]
            if pick != None:
                acptfact_obj.set_attr(pick=pick)
            if open != None:
                acptfact_obj.set_attr(open=open)
            if nigh != None:
                acptfact_obj.set_attr(nigh=nigh)
        except KeyError as e:
            self._idearoot._acptfactunits[acptfactunit.base] = acptfactunit

    def get_acptfactunits_base_and_acptfact_list(self):
        acptfact_list = list(self._idearoot._acptfactunits.values())
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
        self._idearoot._acptfactunits.pop(base)

    def get_tree_metrics(self) -> TreeMetrics:
        tree_metrics = TreeMetrics()
        tree_metrics.evaluate_node(
            level=self._idearoot._level,
            requireds=self._idearoot._requiredunits,
            grouplinks=self._idearoot._grouplinks,
            uid=self._idearoot._uid,
            promise=self._idearoot.promise,
            idea_road=self._idearoot.get_road(),
        )

        idea_list = [self._idearoot]
        while idea_list != []:
            idea_x = idea_list.pop()
            if idea_x._kids != None:
                for idea_kid in idea_x._kids.values():
                    self._eval_tree_metrics(idea_x, idea_kid, tree_metrics, idea_list)
        return tree_metrics

    def _eval_tree_metrics(self, idea_x, idea_kid, tree_metrics, idea_list):
        idea_kid._level = idea_x._level + 1
        tree_metrics.evaluate_node(
            level=idea_kid._level,
            requireds=idea_kid._requiredunits,
            grouplinks=idea_kid._grouplinks,
            uid=idea_kid._uid,
            promise=idea_kid.promise,
            idea_road=idea_kid.get_road(),
        )
        idea_list.append(idea_kid)

    def get_idea_uid_max(self) -> int:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.uid_max

    def set_all_idea_uids_unique(self):
        tree_metrics = self.get_tree_metrics()
        idea_uid_max = tree_metrics.uid_max
        idea_uid_dict = tree_metrics.uid_dict

        for idea_x in self.get_idea_list():
            if idea_x._uid is None or idea_uid_dict.get(idea_x._uid) > 1:
                new_idea_uid_max = idea_uid_max + 1
                self.edit_idea_attr(road=idea_x.get_road(), uid=new_idea_uid_max)
                idea_uid_max = new_idea_uid_max

    def get_node_count(self):
        # tree_metrics = self.get_tree_metrics()
        # return tree_metrics.node_count
        return len(self._idea_dict)

    def get_level_count(self, level):
        tree_metrics = self.get_tree_metrics()
        level_count = None
        try:
            level_count = tree_metrics.level_count[level]
        except KeyError:
            level_count = 0
        return level_count

    def get_required_bases(self) -> dict[Road:int]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.required_bases

    def get_missing_acptfact_bases(self):
        tree_metrics = self.get_tree_metrics()
        required_bases = tree_metrics.required_bases
        missing_bases = {}
        if self._idearoot._acptfactunits is None:
            missing_bases = required_bases
        elif self._idearoot._acptfactunits != None:
            for base, base_count in required_bases.items():
                try:
                    level_count = self._idearoot._acptfactunits[base]
                except KeyError:
                    missing_bases[base] = base_count

        return missing_bases

    def add_idea(
        self,
        idea_kid: IdeaCore,
        walk: Road,
        create_missing_ideas_groups: bool = None,
    ):
        walk = road_validate(walk)
        temp_idea = self._idearoot
        walk_nodes = get_all_road_nodes(walk)
        temp_road = walk_nodes.pop(0)

        # idearoot cannot be replaced
        if temp_road == root_label() and walk_nodes == []:
            idea_kid.set_walk(parent_road=Road(root_label()))
        else:
            road_nodes = [temp_road]
            while walk_nodes != []:
                temp_road = walk_nodes.pop(0)
                temp_idea = self._get_or_create_leveln_idea(
                    parent_idea=temp_idea, idea_label=temp_road
                )
                road_nodes.append(temp_road)

            idea_kid.set_walk(parent_road=get_road_from_nodes(road_nodes))

        temp_idea.add_kid(idea_kid)

        if create_missing_ideas_groups:
            self._create_missing_ideas(road=Road(f"{walk},{idea_kid._label}"))
            self._create_missing_groups_members(grouplinks=idea_kid._grouplinks)

    def _create_missing_groups_members(self, grouplinks: dict[GroupName:GroupLink]):
        for grouplink_x in grouplinks.values():
            if self._groups.get(grouplink_x.name) is None:
                groupunit_x = groupunit_shop(name=grouplink_x.name, _members={})
                self.set_groupunit(groupunit=groupunit_x)

    def _create_missing_ideas(self, road):
        self.set_calendar_metrics()
        posted_idea = self.get_idea_kid(road)

        for required_x in posted_idea._requiredunits.values():
            self._set_ideakid_if_empty(road=required_x.base)
            for sufffact_x in required_x.sufffacts.values():
                self._set_ideakid_if_empty(road=sufffact_x.need)
        if posted_idea._range_source_road != None:
            self._set_ideakid_if_empty(road=posted_idea._range_source_road)
        if posted_idea._numeric_road != None:
            self._set_ideakid_if_empty(road=posted_idea._numeric_road)

    def _set_ideakid_if_empty(self, road: Road):
        try:
            self.get_idea_kid(road)
        except InvalidCalendarException:
            base_idea = IdeaKid(
                _label=get_terminus_node_from_road(road=road),
                _walk=get_walk_from_road(road=road),
            )
            self.add_idea(idea_kid=base_idea, walk=base_idea._walk)

    # def _get_or_create_level1_idea(self, idea_label: str) -> IdeaKid:
    #     return_idea = None
    #     try:
    #         return_idea = self._kids[idea_label]
    #     except Exception:
    #         KeyError
    #         self.add_kid(IdeaKid(_label=idea_label))
    #         return_idea = self._kids[idea_label]

    #     return return_idea

    def _get_or_create_leveln_idea(self, parent_idea: IdeaCore, idea_label: str):
        return_idea = None
        try:
            return_idea = parent_idea._kids[idea_label]
        except Exception:
            KeyError
            parent_idea.add_kid(IdeaKid(_label=idea_label))
            return_idea = parent_idea._kids[idea_label]

        return return_idea

    def del_idea_kid(self, road: Road, del_children: bool = True):
        x_road = get_all_road_nodes(road)
        temp_label = x_road.pop(0)
        temps_d = [temp_label]

        if x_road == []:
            raise InvalidCalendarException("Object cannot delete itself")
        temp_label = x_road.pop(0)
        temps_d.append(temp_label)

        if x_road == []:
            if not del_children:
                d_temp_idea = self.get_idea_kid(road=get_road_from_nodes(temps_d))
                for kid in d_temp_idea._kids.values():
                    self.add_idea(idea_kid=kid, walk=get_road_from_nodes(temps_d[:-1]))
            self._idearoot._kids.pop(temp_label)
        elif x_road != []:
            i_temp_idea = self._idearoot._kids[temp_label]
            while x_road != []:
                temp_label = x_road.pop(0)
                parent_temp_idea = i_temp_idea
                i_temp_idea = i_temp_idea._kids[temp_label]

            parent_temp_idea._kids.pop(temp_label)
        self.set_calendar_metrics()

    def set_owner(self, new_owner):
        self._owner = new_owner

    def edit_idea_label(
        self,
        old_road: Road,
        new_label: str,
    ):
        # confirm idea exists
        if self.get_idea_kid(road=old_road) is None:
            raise InvalidCalendarException(f"Idea {old_road=} does not exist")

        walk = get_walk_from_road(road=old_road)
        new_road = Road(f"{new_label}") if walk == "" else Road(f"{walk},{new_label}")
        if old_road != new_road:
            # if root _label is changed
            if walk == "":
                self._idearoot.set_idea_label(new_label)
                self._idearoot._walk = walk
            else:
                self._non_root_idea_label_edit(old_road, new_label, walk)
            self._idearoot_find_replace_road(old_road=old_road, new_road=new_road)
            self._set_acptfacts_empty_if_null()
            self._idearoot._acptfactunits = find_replace_road_key_dict(
                dict_x=self._idearoot._acptfactunits,
                old_road=old_road,
                new_road=new_road,
            )

    def _non_root_idea_label_edit(self, old_road, new_label, walk):
        idea_z = self.get_idea_kid(road=old_road)
        idea_z.set_idea_label(new_label)
        idea_z._walk = walk
        idea_parent = self.get_idea_kid(road=get_walk_from_road(old_road))
        idea_parent._kids.pop(get_terminus_node_from_road(old_road))
        idea_parent._kids[idea_z._label] = idea_z

    def _idearoot_find_replace_road(self, old_road, new_road):
        self._idearoot.find_replace_road(old_road=old_road, new_road=new_road)

        idea_iter_list = [self._idearoot]
        while idea_iter_list != []:
            listed_idea = idea_iter_list.pop()
            # put all idea_children in idea list
            if listed_idea._kids != None:
                for idea_kid in listed_idea._kids.values():
                    idea_iter_list.append(idea_kid)
                    if is_sub_road(
                        ref_road=idea_kid._walk,
                        sub_road=old_road,
                    ):
                        idea_kid._walk = change_road(
                            current_road=idea_kid._walk,
                            old_road=old_road,
                            new_road=new_road,
                        )
                    idea_kid.find_replace_road(old_road=old_road, new_road=new_road)

    def get_begin_close_if_denom_or_numeric_road(
        self,
        begin: float,
        close: float,
        addin: float,
        numor: float,
        denom: float,
        reest: bool,
        idea_road: Road,
        numeric_road: Road,
    ):
        anc_roads = get_ancestor_roads(road=idea_road)
        if (addin != None or numor != None or denom != None or reest != None) and len(
            anc_roads
        ) == 1:
            raise InvalidCalendarException("Root Idea cannot have numor denom reest.")
        parent_road = root_label() if len(anc_roads) == 1 else anc_roads[1]

        parent_has_range = None
        parent_idea_x = self.get_idea_kid(road=parent_road)
        parent_begin = parent_idea_x._begin
        parent_close = parent_idea_x._close
        parent_has_range = parent_begin is not None and parent_close is not None

        numeric_begin = None
        numeric_close = None
        numeric_range = None
        if numeric_road != None:
            numeric_idea_x = self.get_idea_kid(road=numeric_road)
            numeric_begin = numeric_idea_x._begin
            numeric_close = numeric_idea_x._close
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
            raise InvalidCalendarException(
                "Idea has begin-close range parent, cannot have numeric_road"
            )
        elif not parent_has_range and not numeric_range and numor != None:
            raise InvalidCalendarException(
                f"Idea cannot edit {numor=}/denom/reest of '{idea_road}' if parent '{parent_road}' or ideacore._numeric_road does not have begin/close range"
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

    def edit_idea_attr(
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
        required_suff_idea_active_status: str = None,
        assignedunit: AssignedUnit = None,
        begin: float = None,
        close: float = None,
        addin: float = None,
        numor: float = None,
        denom: float = None,
        reest: bool = None,
        numeric_road: Road = None,
        range_source_road: float = None,
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
                idea_road=road,
                numeric_road=numeric_road,
            )

        idea_attr = IdeaAttrHolder(
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
            required_suff_idea_active_status=required_suff_idea_active_status,
            assignedunit=assignedunit,
            begin=begin,
            close=close,
            addin=addin,
            numor=numor,
            denom=denom,
            reest=reest,
            numeric_road=numeric_road,
            range_source_road=range_source_road,
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
        if idea_attr.required_sufffact != None:
            suffact_idea = self.get_idea_kid(road=required_sufffact)
            idea_attr.set_sufffact_range_attributes_influenced_by_sufffact_idea(
                sufffact_open=suffact_idea._begin,
                sufffact_nigh=suffact_idea._close,
                # suffact_numor=suffact_idea.anc_numor,
                sufffact_denom=suffact_idea._denom,
                # anc_reest=suffact_idea.anc_reest,
            )
        temp_idea = self.get_idea_kid(road=road)
        temp_idea._set_idea_attr(idea_attr=idea_attr)
        if f"{type(temp_idea)}".find("'.idea.IdeaRoot'>") <= 0:
            temp_idea._set_ideakid_attr(acptfactunit=acptfactunit)

        # deleting a grouplink reqquires a tree traverse to correctly set groupheirs and grouplines
        if grouplink_del != None or grouplink != None:
            self.set_calendar_metrics()

    def del_idea_required_sufffact(
        self, road: Road, required_base: Road, required_sufffact: Road
    ):
        self.edit_idea_attr(
            road=road,
            required_del_sufffact_base=required_base,
            required_del_sufffact_need=required_sufffact,
        )

    def _set_acptfacts_empty_if_null(self):
        self._idearoot.set_acptfactunits_empty_if_null()

    def get_agenda_items(
        self, base: Road = None, agenda_todo: bool = True, agenda_state: bool = True
    ) -> list[IdeaCore]:
        return [
            idea for idea in self.get_idea_list() if idea.is_agenda_item(base_x=base)
        ]

    def set_agenda_task_complete(self, task_road: Road, base: Road):
        promise_item = self.get_idea_kid(road=task_road)
        promise_item.set_acptfactunit_to_complete(
            base_acptfactunit=self._idearoot._acptfactunits[base]
        )

    def get_memberunit_total_creditor_weight(self):
        return sum(
            memberunit.get_creditor_weight() for memberunit in self._members.values()
        )

    def get_memberunit_total_debtor_weight(self):
        return sum(
            memberunit.get_debtor_weight() for memberunit in self._members.values()
        )

    def _add_to_memberunits_calendar_credit_debt(self, idea_calendar_importance: float):
        sum_memberunit_creditor_weight = self.get_memberunit_total_creditor_weight()
        sum_memberunit_debtor_weight = self.get_memberunit_total_debtor_weight()

        for memberunit_x in self._members.values():
            au_calendar_credit = (
                idea_calendar_importance * memberunit_x.get_creditor_weight()
            ) / sum_memberunit_creditor_weight

            au_calendar_debt = (
                idea_calendar_importance * memberunit_x.get_debtor_weight()
            ) / sum_memberunit_debtor_weight

            memberunit_x.add_calendar_credit_debt(
                calendar_credit=au_calendar_credit,
                calendar_debt=au_calendar_debt,
                calendar_agenda_credit=0,
                calendar_agenda_debt=0,
            )

    def _add_to_memberunits_calendar_agenda_credit_debt(
        self, idea_calendar_importance: float
    ):
        sum_memberunit_creditor_weight = self.get_memberunit_total_creditor_weight()
        sum_memberunit_debtor_weight = self.get_memberunit_total_debtor_weight()

        for memberunit_x in self._members.values():
            au_calendar_agenda_credit = (
                idea_calendar_importance * memberunit_x.get_creditor_weight()
            ) / sum_memberunit_creditor_weight

            au_calendar_agenda_debt = (
                idea_calendar_importance * memberunit_x.get_debtor_weight()
            ) / sum_memberunit_debtor_weight

            memberunit_x.add_calendar_credit_debt(
                calendar_credit=0,
                calendar_debt=0,
                calendar_agenda_credit=au_calendar_agenda_credit,
                calendar_agenda_debt=au_calendar_agenda_debt,
            )

    def _set_memberunits_calendar_agenda_importance(
        self, calendar_agenda_importance: float
    ):
        sum_memberunit_creditor_weight = self.get_memberunit_total_creditor_weight()
        sum_memberunit_debtor_weight = self.get_memberunit_total_debtor_weight()

        for memberunit_x in self._members.values():
            au_calendar_agenda_credit = (
                calendar_agenda_importance * memberunit_x.get_creditor_weight()
            ) / sum_memberunit_creditor_weight

            au_calendar_agenda_debt = (
                calendar_agenda_importance * memberunit_x.get_debtor_weight()
            ) / sum_memberunit_debtor_weight

            memberunit_x.add_calendar_agenda_credit_debt(
                calendar_agenda_credit=au_calendar_agenda_credit,
                calendar_agenda_debt=au_calendar_agenda_debt,
            )

    def _reset_groupunits_calendar_credit_debt(self):
        self.set_groupunits_empty_if_null()
        for grouplink_obj in self._groups.values():
            grouplink_obj.reset_calendar_credit_debt()

    def _set_groupunits_calendar_importance(
        self, groupheirs: dict[GroupName:GroupLink]
    ):
        self.set_groupunits_empty_if_null()
        for grouplink_obj in groupheirs.values():
            self.add_to_group_calendar_credit_debt(
                groupname=grouplink_obj.name,
                groupheir_calendar_credit=grouplink_obj._calendar_credit,
                groupheir_calendar_debt=grouplink_obj._calendar_debt,
            )

    def _distribute_calendar_agenda_importance(self):
        for idea in self._idea_dict.values():
            # If there are no grouplines associated with idea
            # distribute calendar_importance via general memberunit
            # credit ratio and debt ratio
            # if idea.is_agenda_item() and idea._grouplines == {}:
            if idea.is_agenda_item():
                if idea._grouplines == {}:
                    self._add_to_memberunits_calendar_agenda_credit_debt(
                        idea._calendar_importance
                    )
                else:
                    for groupline_x in idea._grouplines.values():
                        self.add_to_group_calendar_agenda_credit_debt(
                            groupname=groupline_x.name,
                            groupline_calendar_credit=groupline_x._calendar_credit,
                            groupline_calendar_debt=groupline_x._calendar_debt,
                        )

    def _distribute_groups_calendar_importance(self):
        for group_obj in self._groups.values():
            group_obj._set_memberlink_calendar_credit_debt()
            for memberlink in group_obj._members.values():
                self.add_to_memberunit_calendar_credit_debt(
                    memberunit_name=memberlink.name,
                    calendar_credit=memberlink._calendar_credit,
                    calendar_debt=memberlink._calendar_debt,
                    calendar_agenda_credit=memberlink._calendar_agenda_credit,
                    calendar_agenda_debt=memberlink._calendar_agenda_debt,
                )

    def _set_calendar_agenda_ratio_credit_debt(self):
        calendar_agenda_ratio_credit_sum = 0
        calendar_agenda_ratio_debt_sum = 0

        for memberunit_x in self._members.values():
            calendar_agenda_ratio_credit_sum += memberunit_x._calendar_agenda_credit
            calendar_agenda_ratio_debt_sum += memberunit_x._calendar_agenda_debt

        for memberunit_x in self._members.values():
            memberunit_x.set_calendar_agenda_ratio_credit_debt(
                calendar_agenda_ratio_credit_sum=calendar_agenda_ratio_credit_sum,
                calendar_agenda_ratio_debt_sum=calendar_agenda_ratio_debt_sum,
                calendar_memberunit_total_creditor_weight=self.get_memberunit_total_creditor_weight(),
                calendar_memberunit_total_debtor_weight=self.get_memberunit_total_debtor_weight(),
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

    def _reset_memberunit_calendar_credit_debt(self):
        self.set_members_empty_if_null()
        for memberunit in self._members.values():
            memberunit.reset_calendar_credit_debt()

    def _idearoot_inherit_requiredheirs(self):
        self._idearoot.set_requiredunits_empty_if_null()
        x_dict = {}
        for required in self._idearoot._requiredunits.values():
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
        self._idearoot._requiredheirs = x_dict

    def get_idea_kid(self, road: Road) -> IdeaKid:
        if road is None:
            raise InvalidCalendarException("get_idea_kid received road=None")
        nodes = get_all_road_nodes(road)
        src = nodes.pop(0)
        temp_idea = None

        if nodes == [] and src == self._idearoot._label:
            temp_idea = self._idearoot
            # raise InvalidCalendarException(f"Cannot return root '{root_label()}'")
        else:
            idea_label = src if nodes == [] else nodes.pop(0)
            try:
                temp_idea = self._idearoot._kids.get(idea_label)

                while nodes != []:
                    idea_label = nodes.pop(0)
                    temp_idea = temp_idea._kids[idea_label]
                if temp_idea is None:
                    raise InvalidCalendarException(
                        f"Temp_idea is None {idea_label=}. No item at '{road}'"
                    )
            except:
                raise InvalidCalendarException(
                    f"Getting {idea_label=} failed no item at '{road}'"
                )

        return temp_idea

    def get_idea_ranged_kids(
        self, idea_road: str, begin: float = None, close: float = None
    ) -> dict[IdeaCore]:
        parent_idea = self.get_idea_kid(road=idea_road)
        if begin is None and close is None:
            begin = parent_idea._begin
            close = parent_idea._close
        elif begin != None and close is None:
            close = begin

        idea_list = parent_idea.get_kids_in_range(begin=begin, close=close)
        return {idea_x._label: idea_x for idea_x in idea_list}

    def _set_ancestor_metrics(self, road: Road):
        # sourcery skip: low-code-quality
        da_count = 0
        child_grouplines = None
        if road is None:
            road = ""

        group_everyone = None
        if len(get_all_road_nodes(road)) <= 1:
            group_everyone = self._idearoot._groupheirs in [None, {}]
        else:
            ancestor_roads = get_ancestor_roads(road=road)
            # remove root road
            ancestor_roads.pop(len(ancestor_roads) - 1)

            while ancestor_roads != []:
                # youngest_untouched_idea
                yu_idea_obj = self.get_idea_kid(road=ancestor_roads.pop(0))
                yu_idea_obj.set_descendant_promise_count_zero_if_null()
                yu_idea_obj._descendant_promise_count += da_count
                if yu_idea_obj.is_kidless():
                    yu_idea_obj.set_kidless_grouplines()
                    child_grouplines = yu_idea_obj._grouplines
                else:
                    yu_idea_obj.set_grouplines(child_grouplines=child_grouplines)

                if yu_idea_obj._task == True:
                    da_count += 1

                if (
                    group_everyone != False
                    and yu_idea_obj._all_member_credit != False
                    and yu_idea_obj._all_member_debt != False
                    and yu_idea_obj._groupheirs != {}
                    or group_everyone != False
                    and yu_idea_obj._all_member_credit == False
                    and yu_idea_obj._all_member_debt == False
                ):
                    group_everyone = False
                elif group_everyone != False:
                    group_everyone = True
                yu_idea_obj._all_member_credit = group_everyone
                yu_idea_obj._all_member_debt = group_everyone

            if (
                group_everyone != False
                and self._idearoot._all_member_credit != False
                and self._idearoot._all_member_debt != False
                and self._idearoot._groupheirs != {}
                or group_everyone != False
                and self._idearoot._all_member_credit == False
                and self._idearoot._all_member_debt == False
            ):
                group_everyone = False
            elif group_everyone != False and yu_idea_obj._groupheirs == {}:
                group_everyone = True

        self._idearoot._all_member_credit = group_everyone
        self._idearoot._all_member_debt = group_everyone

        if self._idearoot.is_kidless():
            self._idearoot.set_kidless_grouplines()
        else:
            self._idearoot.set_grouplines(child_grouplines=child_grouplines)
        self._idearoot.set_descendant_promise_count_zero_if_null()
        self._idearoot._descendant_promise_count += da_count

    def _set_root_attributes(self):
        self._idearoot._level = 0
        self._idearoot.set_walk(parent_road="")
        self._idearoot.set_requiredheirs(calendar_idea_dict=self._idea_dict)
        self._idearoot.set_assignedheir(
            parent_assignheir=None, calendar_groups=self._groups
        )
        self._idearoot.inherit_groupheirs()
        self._idearoot.clear_grouplines()
        self._idearoot.set_originunit_empty_if_null()
        self._idearoot.set_acptfactunits_empty_if_null()
        self._idearoot._weight = 1
        self._idearoot._kids_total_weight = 0
        self._idearoot.set_kids_total_weight()
        self._idearoot.set_sibling_total_weight(1)
        self._idearoot.set_calendar_importance(coin_onset_x=0, parent_coin_cease=1)
        self._idearoot.set_groupheirs_calendar_credit_debit()
        self._idearoot.set_ancestor_promise_count(0, False)
        self._idearoot.clear_descendant_promise_count()
        self._idearoot.clear_all_member_credit_debt()
        self._idearoot.promise = False

        if self._idearoot.is_kidless():
            self._set_ancestor_metrics(road=self._idearoot._walk)
            self._distribute_calendar_importance(idea=self._idearoot)

    def _set_kids_attributes(
        self,
        idea_kid: IdeaKid,
        coin_onset: float,
        parent_coin_cease: float,
        parent_idea: IdeaKid = None,
    ) -> IdeaKid:
        parent_acptfacts = None
        parent_requiredheirs = None

        if parent_idea is None:
            parent_idea = self._idearoot
            parent_acptfacts = self._idearoot._acptfactunits
            parent_requiredheirs = self._idearoot_inherit_requiredheirs()
        else:
            parent_acptfacts = parent_idea._acptfactheirs
            parent_requiredheirs = parent_idea._requiredheirs

        idea_kid.set_level(parent_level=parent_idea._level)
        idea_kid.set_walk(
            parent_road=parent_idea._walk, parent_label=parent_idea._label
        )
        idea_kid.set_acptfactunits_empty_if_null()
        idea_kid.set_acptfactheirs(acptfacts=parent_acptfacts)
        idea_kid.set_requiredheirs(self._idea_dict, parent_requiredheirs)
        idea_kid.set_assignedheir(parent_idea._assignedheir, self._groups)
        idea_kid.inherit_groupheirs(parent_idea._groupheirs)
        idea_kid.clear_grouplines()
        idea_kid.set_originunit_empty_if_null()
        idea_kid.set_active_status(
            tree_traverse_count=self._tree_traverse_count,
            calendar_groups=self._groups,
            calendar_owner=self._owner,
        )
        idea_kid.set_sibling_total_weight(parent_idea._kids_total_weight)
        idea_kid.set_calendar_importance(
            coin_onset_x=coin_onset,
            parent_calendar_importance=parent_idea._calendar_importance,
            parent_coin_cease=parent_coin_cease,
        )
        idea_kid.set_ancestor_promise_count(
            parent_idea._ancestor_promise_count, parent_idea.promise
        )
        idea_kid.clear_descendant_promise_count()
        idea_kid.clear_all_member_credit_debt()

        if idea_kid.is_kidless():
            # set idea's ancestor metrics using calendar root as common reference
            self._set_ancestor_metrics(road=idea_kid.get_road())
            self._distribute_calendar_importance(idea=idea_kid)

    def _distribute_calendar_importance(self, idea: IdeaCore):
        # TODO manage situations where groupheir.creditor_weight is None for all groupheirs
        # TODO manage situations where groupheir.debtor_weight is None for all groupheirs
        if idea.is_groupheirless() == False:
            self._set_groupunits_calendar_importance(idea._groupheirs)
        elif idea.is_groupheirless():
            self._add_to_memberunits_calendar_credit_debt(idea._calendar_importance)

    def get_calendar_importance(
        self, parent_calendar_importance: float, weight: int, sibling_total_weight: int
    ):
        sibling_ratio = weight / sibling_total_weight
        return parent_calendar_importance * sibling_ratio

    def get_idea_list(self):
        self.set_calendar_metrics()
        return list(self._idea_dict.values())

    def set_calendar_metrics(self):
        self._set_acptfacts_empty_if_null()

        self._rational = False
        self._tree_traverse_count = 0
        self._idea_dict = {self._idearoot.get_road(): self._idearoot}

        while (
            not self._rational and self._tree_traverse_count < self._max_tree_traverse
        ):
            self._execute_tree_traverse()
            self._run_after_each_tree_traverse()
            self._tree_traverse_count += 1
        self._run_after_idea_all_tree_traverses()

    def _execute_tree_traverse(self):
        self._run_before_idea_tree_traverse()
        self._set_root_attributes()

        coin_onset = self._idearoot._calendar_coin_onset
        parent_coin_cease = self._idearoot._calendar_coin_cease

        cache_idea_list = []
        for idea_kid in self._idearoot._kids.values():
            self._set_kids_attributes(
                idea_kid=idea_kid,
                coin_onset=coin_onset,
                parent_coin_cease=parent_coin_cease,
            )
            cache_idea_list.append(idea_kid)
            coin_onset += idea_kid._calendar_importance

        # no function recursion, recursion by iterateing over list that can be added to by iterations
        while cache_idea_list != []:
            parent_idea = cache_idea_list.pop()
            if self._tree_traverse_count == 0:
                self._idea_dict[parent_idea.get_road()] = parent_idea

            if parent_idea._kids != None:
                coin_onset = parent_idea._calendar_coin_onset
                parent_coin_cease = parent_idea._calendar_coin_cease
                for idea_kid in parent_idea._kids.values():
                    self._set_kids_attributes(
                        idea_kid=idea_kid,
                        coin_onset=coin_onset,
                        parent_coin_cease=parent_coin_cease,
                        parent_idea=parent_idea,
                    )
                    cache_idea_list.append(idea_kid)
                    coin_onset += idea_kid._calendar_importance

    def _run_after_each_tree_traverse(self):
        any_idea_active_status_changed = False
        for idea in self._idea_dict.values():
            idea.set_active_status_hx_empty_if_null()
            if idea._active_status_hx.get(self._tree_traverse_count) != None:
                any_idea_active_status_changed = True

        if any_idea_active_status_changed == False:
            self._rational = True

    def _run_after_idea_all_tree_traverses(self):
        self._distribute_calendar_agenda_importance()
        self._distribute_groups_calendar_importance()
        self._set_calendar_agenda_ratio_credit_debt()

    def _run_before_idea_tree_traverse(self):
        self._reset_groupunits_calendar_credit_debt()
        self._reset_groupunits_calendar_credit_debt()
        self._reset_memberunit_calendar_credit_debt()

    def get_heir_road_list(self, road_x: Road):
        # create list of all idea roads (road+desc)
        return [
            road
            for road in self.get_idea_tree_ordered_road_list()
            if road.find(road_x) == 0
        ]

    def get_idea_tree_ordered_road_list(self, no_range_descendants: bool = False):
        idea_list = self.get_idea_list()
        node_dict = {idea.get_road().lower(): idea.get_road() for idea in idea_list}
        node_lowercase_ordered_list = sorted(list(node_dict))
        node_orginalcase_ordered_list = [
            node_dict[node_l] for node_l in node_lowercase_ordered_list
        ]

        list_x = []
        for road in node_orginalcase_ordered_list:
            if not no_range_descendants:
                list_x.append(road)
            else:
                anc_list = get_ancestor_roads(road=road)
                if len(anc_list) == 1:
                    list_x.append(road)
                elif len(anc_list) == 2:
                    if self._idearoot._begin is None and self._idearoot._close is None:
                        list_x.append(road)
                else:
                    parent_idea = self.get_idea_kid(road=anc_list[1])
                    if parent_idea._begin is None and parent_idea._close is None:
                        list_x.append(road)

        return list_x

    def get_acptfactunits_dict(self):
        x_dict = {}
        if self._idearoot._acptfactunits != None:
            for acptfact_road, acptfact_obj in self._idearoot._acptfactunits.items():
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
        self.set_calendar_metrics()
        return {
            "_kids": self._idearoot.get_kids_dict(),
            "_requiredunits": self._idearoot.get_requiredunits_dict(),
            "_acptfactunits": self.get_acptfactunits_dict(),
            "_members": self.get_members_dict(),
            "_groups": self.groupunit_shops_dict(),
            "_grouplinks": self._idearoot.get_grouplinks_dict(),
            "_assignedunit": self._idearoot.get_assignedunit_dict(),
            "_originunit": self._originunit.get_dict(),
            "_weight": self._weight,
            "_owner": self._owner,
            "_uid": self._idearoot._uid,
            "_begin": self._idearoot._begin,
            "_close": self._idearoot._close,
            "_addin": self._idearoot._addin,
            "_numor": self._idearoot._numor,
            "_denom": self._idearoot._denom,
            "_reest": self._idearoot._reest,
            "_problem_bool": self._idearoot._problem_bool,
            "_is_expanded": self._idearoot._is_expanded,
            "_range_source_road": self._idearoot._range_source_road,
            "_numeric_road": self._idearoot._numeric_road,
            "_on_meld_weight_action": self._idearoot._on_meld_weight_action,
            "_max_tree_traverse": self._max_tree_traverse,
        }

    def get_json(self):
        x_dict = self.get_dict()
        return x_get_json(dict_x=x_dict)

    def set_time_hreg_ideas(self, c400_count):
        ideabase_list = _get_time_hreg_src_idea(c400_count=c400_count)
        while len(ideabase_list) != 0:
            yb = ideabase_list.pop(0)
            range_source_road_x = None
            if yb.sr != None:
                range_source_road_x = f"{root_label()},{yb.sr}"

            idea_x = IdeaKid(
                _label=yb.n,
                _begin=yb.b,
                _close=yb.c,
                _weight=yb.weight,
                _is_expanded=False,
                _addin=yb.a,
                _numor=yb.mn,
                _denom=yb.md,
                _reest=yb.mr,
                _range_source_road=range_source_road_x,
            )
            road_x = f"{root_label()},{yb.rr}"
            self.add_idea(idea_kid=idea_x, walk=road_x)

            numeric_road_x = None
            if yb.nr != None:
                numeric_road_x = f"{root_label()},{yb.nr}"
                self.edit_idea_attr(
                    road=f"{road_x},{yb.n}", numeric_road=numeric_road_x
                )
            if yb.a != None:
                self.edit_idea_attr(
                    road=f"{road_x},{yb.n}", addin=yb.a, denom=yb.md, numor=yb.mn
                )

        self.set_calendar_metrics()

    def get_calendar4member(
        self, member_name: MemberName, acptfacts: dict[Road:AcptFactCore]
    ):
        self.set_calendar_metrics()
        calendar4member = CalendarUnit(_owner=member_name)
        calendar4member._idearoot._calendar_importance = (
            self._idearoot._calendar_importance
        )
        # get member's members: memberzone

        # get memberzone groups
        member_groups = self.get_member_groups(member_name=member_name)

        # set calendar4member by traversing the idea tree and selecting associated groups
        # set root
        not_included_calendar_importance = 0
        calendar4member._idearoot._kids = {}
        for ykx in self._idearoot._kids.values():
            y4a_included = any(
                group_ancestor.name in member_groups
                for group_ancestor in ykx._grouplines.values()
            )

            if y4a_included:
                y4a_new = IdeaKid(
                    _label=ykx._label,
                    _calendar_importance=ykx._calendar_importance,
                    _requiredunits=ykx._requiredunits,
                    _grouplinks=ykx._grouplinks,
                    _begin=ykx._begin,
                    _close=ykx._close,
                    promise=ykx.promise,
                    _task=ykx._task,
                )
                calendar4member._idearoot._kids[ykx._label] = y4a_new
            else:
                not_included_calendar_importance += ykx._calendar_importance

        if not_included_calendar_importance > 0:
            y4a_other = IdeaKid(
                _label="__other__",
                _calendar_importance=not_included_calendar_importance,
            )
            calendar4member._idearoot._kids[y4a_other._label] = y4a_other

        return calendar4member

    # def get_agenda_items(
    #     self, agenda_todo: bool = True, agenda_state: bool = True, base: Road = None
    # ) -> list[IdeaCore]:
    #     return list(self.get_agenda_items(base=base))

    def set_dominate_promise_idea(self, idea_kid: IdeaKid):
        idea_kid.promise = True
        self.add_idea(
            idea_kid=idea_kid,
            walk=Road(f"{idea_kid._walk}"),
            create_missing_ideas_groups=True,
        )

    def get_idea_list_without_idearoot(self):
        x_list = self.get_idea_list()
        x_list.pop(0)
        return x_list

    def meld(self, other_calendar, member_weight: float = None):
        self._meld_groups(other_calendar)
        self._meld_members(other_calendar)
        self._meld_ideas(other_calendar, member_weight)
        self._meld_acptfacts(other_calendar)
        self._weight = get_meld_weight(
            src_weight=self._weight,
            src_on_meld_weight_action="default",
            other_weight=other_calendar._weight,
            other_on_meld_weight_action="default",
        )
        self._meld_originlinks(other_calendar._owner, member_weight)

    def _meld_ideas(self, other_calendar, member_weight: float):
        # meld idearoot
        self._idearoot.meld(other_idea=other_calendar._idearoot, _idearoot=True)

        # meld all other ideas
        member_name = other_calendar._owner
        o_idea_list = other_calendar.get_idea_list_without_idearoot()
        for o_idea in o_idea_list:
            o_road = road_validate(f"{o_idea._walk},{o_idea._label}")
            try:
                main_idea = self.get_idea_kid(o_road)
                main_idea.meld(o_idea, False, member_name, member_weight)
            except Exception:
                self.add_idea(walk=o_idea._walk, idea_kid=o_idea)
                main_idea = self.get_idea_kid(o_road)
                main_idea._originunit.set_originlink(member_name, member_weight)

    def _meld_members(self, other_calendar):
        self.set_members_empty_if_null()
        other_calendar.set_members_empty_if_null()
        for memberunit in other_calendar._members.values():
            if self._members.get(memberunit.name) is None:
                self.set_memberunit(memberunit=memberunit)
            else:
                self._members.get(memberunit.name).meld(memberunit)

    def _meld_groups(self, other_calendar):
        self.set_groupunits_empty_if_null()
        other_calendar.set_groupunits_empty_if_null()
        for brx in other_calendar._groups.values():
            if self._groups.get(brx.name) is None:
                self.set_groupunit(groupunit=brx)
            else:
                self._groups.get(brx.name).meld(brx)

    def _meld_acptfacts(self, other_calendar):
        self._set_acptfacts_empty_if_null()
        other_calendar._set_acptfacts_empty_if_null()
        for hx in other_calendar._idearoot._acptfactunits.values():
            if self._idearoot._acptfactunits.get(hx.base) is None:
                self.set_acptfact(
                    base=hx.base, acptfact=hx.acptfact, open=hx.open, nigh=hx.nigh
                )
            else:
                self._idearoot._acptfactunits.get(hx.base).meld(hx)

    def _meld_originlinks(self, member_name: MemberName, member_weight: float):
        if member_name != None:
            self._originunit.set_originlink(member_name, member_weight)

    def get_assignment(
        self,
        calendar_x,
        assignor_members: dict[MemberName:MemberUnit],
        assignor_name: MemberName,
    ) -> CalendarOwner:
        self.set_calendar_metrics()
        self._set_assignment_members(calendar_x, assignor_members, assignor_name)
        self._set_assignment_groups(calendar_x)
        assignor_promises = self._get_assignor_promise_ideas(calendar_x, assignor_name)
        relevant_roads = self._get_relevant_roads(assignor_promises)
        self._set_assignment_ideas(calendar_x, relevant_roads)
        return calendar_x

    def _set_assignment_ideas(self, calendar_x, relevant_roads: dict[Road:str]):
        sorted_relevants = sorted(list(relevant_roads))
        # don't know how to handle root idea attributes...
        if sorted_relevants != []:
            root_road = sorted_relevants.pop(0)

        for relevant_road in sorted_relevants:
            relevant_idea = copy_deepcopy(self.get_idea_kid(relevant_road))
            # if relevant_roads.get(relevant_road) == "descendant":
            #     relevant_idea._requiredunits = {}
            #     relevant_idea._kids = {}
            #     calendar_x.add_idea(idea_kid=relevant_idea, walk=relevant_idea._walk)
            # elif relevant_roads.get(relevant_road) != "descendant":
            relevant_idea._kids = {}
            calendar_x.add_idea(idea_kid=relevant_idea, walk=relevant_idea._walk)

    def _set_assignment_members(
        self,
        calendar_x,
        assignor_members: dict[MemberName:MemberUnit],
        assignor_name: MemberName,
    ):
        calendar_x.set_members_empty_if_null()
        if self._members.get(assignor_name) != None:
            # get all members that are both in self._members and assignor_known_members
            members_set = get_intersection_of_members(self._members, assignor_members)
            for membername_x in members_set:
                calendar_x.set_memberunit(memberunit=self._members.get(membername_x))
        return calendar_x

    def _set_assignment_groups(self, calendar_x):
        revelant_groups = get_members_relevant_groups(self._groups, calendar_x._members)
        for group_name, group_members in revelant_groups.items():
            if calendar_x._groups.get(group_name) is None:
                group_x = groupunit_shop(name=group_name)
                for member_name in group_members:
                    group_x.set_memberlink(memberlink_shop(name=member_name))
                calendar_x.set_groupunit(group_x)

    def _get_assignor_promise_ideas(
        self, calendar_x, assignor_name: GroupName
    ) -> dict[Road:int]:
        calendar_x.set_groupunits_empty_if_null()
        assignor_groups = get_member_relevant_groups(calendar_x._groups, assignor_name)
        return {
            idea_road: -1
            for idea_road, idea_x in self._idea_dict.items()
            if (idea_x.assignor_in(assignor_groups) and idea_x.promise)
        }


def get_from_json(cx_json: str) -> CalendarUnit:
    return get_from_dict(cx_dict=json.loads(cx_json))


def get_from_dict(cx_dict: dict) -> CalendarUnit:
    c_x = CalendarUnit()
    c_x._idearoot._requiredunits = requireds_get_from_dict(
        requireds_dict=cx_dict["_requiredunits"]
    )
    _assignedunit = "_assignedunit"
    if cx_dict.get(_assignedunit):
        c_x._idearoot._assignedunit = assignedunit_get_from_dict(
            assignedunit_dict=cx_dict.get(_assignedunit)
        )
    c_x._idearoot._acptfactunits = acptfactunits_get_from_dict(
        x_dict=cx_dict["_acptfactunits"]
    )
    c_x._groups = groupunits_get_from_dict(x_dict=cx_dict["_groups"])
    c_x._idearoot._grouplinks = grouplinks_get_from_dict(x_dict=cx_dict["_grouplinks"])
    try:
        c_x._originunit = originunit_get_from_dict(x_dict=cx_dict["_originunit"])
    except Exception:
        c_x._originunit = originunit_shop()
    c_x._members = memberunits_get_from_dict(x_dict=cx_dict["_members"])
    c_x._owner = cx_dict["_owner"]
    c_x._idearoot.set_idea_label(root_label())
    c_x._weight = cx_dict["_weight"]
    c_x._max_tree_traverse = cx_dict.get("_max_tree_traverse")
    if cx_dict.get("_max_tree_traverse") is None:
        c_x._max_tree_traverse = 20
    c_x._idearoot._weight = cx_dict["_weight"]
    c_x._idearoot._uid = cx_dict["_uid"]
    c_x._idearoot._begin = cx_dict["_begin"]
    c_x._idearoot._close = cx_dict["_close"]
    c_x._idearoot._numor = cx_dict["_numor"]
    c_x._idearoot._denom = cx_dict["_denom"]
    c_x._idearoot._reest = cx_dict["_reest"]
    c_x._idearoot._range_source_road = cx_dict["_range_source_road"]
    c_x._idearoot._numeric_road = cx_dict["_numeric_road"]
    c_x._idearoot._is_expanded = cx_dict["_is_expanded"]

    idea_dict_list = []
    for x_dict in cx_dict["_kids"].values():
        x_dict["temp_road"] = c_x._owner
        idea_dict_list.append(x_dict)

    while idea_dict_list != []:
        idea_dict = idea_dict_list.pop(0)
        for x_dict in idea_dict["_kids"].values():
            temp_road = idea_dict["temp_road"]
            temp_label = idea_dict["_label"]
            x_dict["temp_road"] = f"{temp_road},{temp_label}"
            idea_dict_list.append(x_dict)

        idea_assignedunit = assigned_unit_shop()
        if idea_dict.get(_assignedunit):
            idea_assignedunit = assignedunit_get_from_dict(
                assignedunit_dict=idea_dict.get(_assignedunit)
            )
        originunit_from_dict = None
        try:
            originunit_from_dict = originunit_get_from_dict(idea_dict["_originunit"])
        except Exception:
            originunit_from_dict = originunit_shop()

        idea_obj = IdeaKid(
            _label=idea_dict["_label"],
            _weight=idea_dict["_weight"],
            _uid=idea_dict["_uid"],
            _begin=idea_dict["_begin"],
            _close=idea_dict["_close"],
            _numor=idea_dict["_numor"],
            _denom=idea_dict["_denom"],
            _reest=idea_dict["_reest"],
            promise=idea_dict["promise"],
            _requiredunits=requireds_get_from_dict(
                requireds_dict=idea_dict["_requiredunits"]
            ),
            _assignedunit=idea_assignedunit,
            _originunit=originunit_from_dict,
            _grouplinks=grouplinks_get_from_dict(idea_dict["_grouplinks"]),
            _acptfactunits=acptfactunits_get_from_dict(idea_dict["_acptfactunits"]),
            _is_expanded=idea_dict["_is_expanded"],
            _range_source_road=idea_dict["_range_source_road"],
            _numeric_road=idea_dict["_numeric_road"],
        )
        c_x.add_idea(idea_kid=idea_obj, walk=idea_dict["temp_road"])

    c_x.set_calendar_metrics()  # clean up tree traverse defined fields
    return c_x


def get_dict_of_calendar_from_dict(x_dict: dict[str:dict]) -> dict[str:CalendarUnit]:
    calendarunits = {}
    for calendarunit_dict in x_dict.values():
        x_calendar = get_from_dict(cx_dict=calendarunit_dict)
        calendarunits[x_calendar._owner] = x_calendar
    return calendarunits


def get_meld_of_calendar_files(
    cx_primary: CalendarUnit, meldees_dir: str
) -> CalendarUnit:
    cx_primary.set_calendar_metrics()
    for bond_file_x in x_func_dir_files(dir_path=meldees_dir):
        bond_x = get_from_json(cx_json=x_func_open_file(meldees_dir, bond_file_x))
        cx_primary.meld(other_calendar=bond_x)

    cx_primary.set_calendar_metrics()
    return cx_primary


def get_intersection_of_members(
    members_x: dict[MemberName:MemberUnit], members_y: dict[MemberName:MemberUnit]
) -> dict[MemberName:-1]:
    x_set = set(members_x)
    y_set = set(members_y)
    intersection_x = x_set.intersection(y_set)
    return {membername_x: -1 for membername_x in intersection_x}


def get_members_relevant_groups(
    groups_x: dict[GroupName:GroupUnit], members_x: dict[MemberName:MemberUnit]
) -> dict[GroupName:{MemberName: -1}]:
    relevant_groups = {}
    for membername_x in members_x:
        for group_x in groups_x.values():
            if group_x._members.get(membername_x) != None:
                if relevant_groups.get(group_x.name) is None:
                    relevant_groups[group_x.name] = {}
                relevant_groups.get(group_x.name)[membername_x] = -1

    return relevant_groups


def get_member_relevant_groups(
    groups_x: dict[GroupName:GroupUnit], membername_x: MemberName
) -> dict[GroupName:-1]:
    return {
        group_x.name: -1
        for group_x in groups_x.values()
        if group_x._members.get(membername_x) != None
    }
