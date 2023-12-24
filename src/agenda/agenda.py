from dataclasses import dataclass
from json import loads as json_loads
from datetime import datetime
from src.agenda.party import (
    PersonID,
    PartyPID,
    PartyUnit,
    PartyLink,
    partyunits_get_from_dict,
    partyunit_shop,
    partylink_shop,
    PartyUnitExternalMetrics,
)
from src.agenda.group import (
    BalanceLink,
    GroupBrand,
    GroupUnit,
    GroupMetrics,
    get_from_dict as groupunits_get_from_dict,
    groupunit_shop,
    balancelink_shop,
)
from src.agenda.required_idea import (
    AcptFactCore,
    AcptFactUnit,
    AcptFactUnit,
    requiredheir_shop,
    RequiredUnit,
    RoadUnit,
    acptfactunit_shop,
    sufffactunit_shop,
)
from src.agenda.required_assign import AssignedUnit
from src.agenda.tree_metrics import TreeMetrics

from src.agenda.x_func import x_get_json
from src.agenda.idea import (
    IdeaCore,
    ideacore_shop,
    IdeaRoot,
    idearoot_shop,
    ideaattrfilter_shop,
    IdeaAttrFilter,
    get_obj_from_idea_dict,
)
from src.agenda.hreg_time import HregTimeIdeaSource as HregIdea
from src.agenda.lemma import lemmas_shop, Lemmas
from src.agenda.road import (
    get_pad_from_road,
    is_sub_road,
    road_validate,
    change_road,
    get_terminus_node_from_road,
    find_replace_road_key_dict,
    get_ancestor_roads,
    get_default_economy_root_label,
    get_all_road_nodes,
    get_forefather_roads,
    get_road,
    get_node_delimiter,
    RoadNode,
    RoadUnit,
    is_string_in_road,
)
from src.agenda.origin import originunit_get_from_dict, originunit_shop, OriginUnit
from copy import deepcopy as copy_deepcopy
from src.agenda.x_func import (
    dir_files as x_func_dir_files,
    open_file as x_func_open_file,
    get_meld_weight,
)


class InvalidAgendaException(Exception):
    pass


class InvalidLabelException(Exception):
    pass


class AssignmentPartyException(Exception):
    pass


class NewDelimiterException(Exception):
    pass


class EconomyID(str):  # Created to help track the concept
    pass


@dataclass
class AgendaUnit:
    _healer: PersonID = None
    _weight: float = None
    _partys: dict[PartyPID:PartyUnit] = None
    _groups: dict[GroupBrand:GroupUnit] = None
    _idearoot: IdeaRoot = None
    _idea_dict: dict[RoadUnit:IdeaCore] = None
    _max_tree_traverse: int = None
    _tree_traverse_count: int = None
    _rational: bool = None
    _originunit: OriginUnit = None
    _economy_id: str = None
    _auto_output_to_public: bool = None
    _road_node_delimiter: str = None

    def make_road(
        self,
        road_begin: RoadUnit = None,
        terminus_node: RoadNode = None,
        road_nodes: list[RoadNode] = None,
    ) -> RoadUnit:
        x_road = get_road(
            road_begin=road_begin,
            terminus_node=terminus_node,
            road_nodes=road_nodes,
            delimiter=self._road_node_delimiter,
        )
        x_road = road_validate(x_road, self._road_node_delimiter, self._economy_id)
        return x_road

    def make_l1_road(self, l1_node: RoadNode):
        return self.make_road(self._economy_id, l1_node)

    def set_partys_output_agenda_meld_order(self):
        sort_partys_list = list(self._partys.values())
        sort_partys_list.sort(key=lambda x: x.pid.lower(), reverse=False)
        for count_x, x_partyunit in enumerate(sort_partys_list):
            x_partyunit.set_output_agenda_meld_order(count_x)

    def clear_partys_output_agenda_meld_order(self):
        for x_partyunit in self._partys.values():
            x_partyunit.clear_output_agenda_meld_order()

    def set_road_node_delimiter(self, new_road_node_delimiter: str):
        self.set_agenda_metrics()
        if self._road_node_delimiter != new_road_node_delimiter:
            for x_idea_road in self._idea_dict.keys():
                if is_string_in_road(new_road_node_delimiter, x_idea_road):
                    raise NewDelimiterException(
                        f"Cannot change delimiter to '{new_road_node_delimiter}' because it already exists an idea label '{x_idea_road}'"
                    )

            # Grab pointers to every idea
            idea_pointers = {
                x_idea_road: self.get_idea_kid(x_idea_road)
                for x_idea_road in self._idea_dict.keys()
            }

            # change all road attributes in idea
            # old_road_node_delimiter = copy_deepcopy(self._road_node_delimiter)
            self._road_node_delimiter = get_node_delimiter(new_road_node_delimiter)
            for x_idea in idea_pointers.values():
                x_idea.set_road_node_delimiter(self._road_node_delimiter)

    def set_economy_id(self, economy_id: str):
        old_economy_id = copy_deepcopy(self._economy_id)
        self._economy_id = economy_id
        self.edit_idea_label(old_road=old_economy_id, new_label=self._economy_id)
        self.set_agenda_metrics()

    def set_partyunit_external_metrics(
        self, external_metrics: PartyUnitExternalMetrics
    ):
        party_x = self._partys.get(external_metrics.internal_pid)
        party_x._creditor_active = external_metrics.creditor_active
        party_x._debtor_active = external_metrics.debtor_active
        # self.set_partyunit(partyunit=party_x)

    def set_max_tree_traverse(self, int_x: int):
        if int_x < 2:
            raise InvalidAgendaException(
                f"set_max_tree_traverse: input '{int_x}' must be number that is 2 or greater"
            )
        else:
            self._max_tree_traverse = int_x

    def get_agenda_sprung_from_single_idea(self, road: RoadUnit) -> any:
        self.set_agenda_metrics()
        x_idea = self.get_idea_kid(road)
        new_weight = self._weight * x_idea._agenda_importance
        x_agenda = agendaunit_shop(_healer=self._idearoot._label, _weight=new_weight)

        for road_assc in sorted(list(self._get_relevant_roads({road}))):
            src_yx = self.get_idea_kid(road_assc)
            new_yx = copy_deepcopy(src_yx)
            if new_yx._pad != "":
                x_agenda.add_idea(new_yx, pad=new_yx._pad)
            x_agenda.set_agenda_metrics()

        # TODO grab groups
        # TODO grab all group partys
        # TODO grab acptfacts
        return x_agenda

    def _get_relevant_roads(self, roads: dict[RoadUnit:]) -> dict[RoadUnit:str]:
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
            x_idea = self.get_idea_kid(road_x)
            for requiredunit_obj in x_idea._requiredunits.values():
                required_base = requiredunit_obj.base
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=required_base,
                    road_type="requiredunit_base",
                )

            if x_idea._numeric_road != None:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=x_idea._numeric_road,
                    road_type="numeric_road",
                )

            if x_idea._range_source_road != None:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=x_idea._range_source_road,
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
        to_evaluate_list: [RoadUnit],
        to_evaluate_hx_dict: dict[RoadUnit:int],
        to_evaluate_road: RoadUnit,
        road_type: str,
    ):
        if to_evaluate_hx_dict.get(to_evaluate_road) is None:
            to_evaluate_list.append(to_evaluate_road)
            to_evaluate_hx_dict[to_evaluate_road] = road_type

            if road_type == "requiredunit_base":
                ru_base_idea = self.get_idea_kid(to_evaluate_road)
                for descendant_road in ru_base_idea.get_descendant_roads_from_kids():
                    self._evaluate_relevancy(
                        to_evaluate_list=to_evaluate_list,
                        to_evaluate_hx_dict=to_evaluate_hx_dict,
                        to_evaluate_road=descendant_road,
                        road_type="requiredunit_descendant",
                    )

    def all_ideas_relevant_to_promise_idea(self, road: RoadUnit) -> bool:
        promise_idea_assoc_set = set(self._get_relevant_roads({road}))
        all_ideas_set = set(self.get_idea_tree_ordered_road_list())
        return all_ideas_set == all_ideas_set.intersection(promise_idea_assoc_set)

    def _are_all_partys_groups_are_in_idea_kid(self, road: RoadUnit) -> bool:
        idea_kid = self.get_idea_kid(road)
        # get dict of all idea balanceheirs
        balanceheir_list = idea_kid._balanceheirs.keys()
        balanceheir_dict = {
            balanceheir_brand: 1 for balanceheir_brand in balanceheir_list
        }
        non_single_groupunits = {
            groupunit.brand: groupunit
            for groupunit in self._groups.values()
            if groupunit._single_party != True
        }
        # check all non_single_party_groupunits are in balanceheirs
        for non_single_group in non_single_groupunits.values():
            if balanceheir_dict.get(non_single_group.brand) is None:
                return False

        # get dict of all partylinks that are in all balanceheirs
        balanceheir_partyunits = {}
        for balanceheir_pid in balanceheir_dict:
            groupunit = self._groups.get(balanceheir_pid)
            for partylink in groupunit._partys.values():
                balanceheir_partyunits[partylink.pid] = self._partys.get(partylink.pid)

        # check all agenda._partys are in balanceheir_partyunits
        return len(self._partys) == len(balanceheir_partyunits)

    def get_time_min_from_dt(self, dt: datetime) -> float:
        x_hregidea = HregIdea(self._road_node_delimiter)
        return x_hregidea.get_time_min_from_dt(dt=dt)

    def get_time_c400_from_min(self, min: int) -> int:
        time_road = self.make_road(self._economy_id, "time")
        tech_road = self.make_road(time_road, "tech")
        c400_road = self.make_road(tech_road, "400 year cycle")
        c400_idea = self.get_idea_kid(c400_road)
        c400_min = c400_idea._close
        return int(min / c400_min), c400_idea, min % c400_min

    def get_time_c400yr_from_min(self, min: int):
        # GIVEN int minutes within 400 year range return year and remainder minutes
        c400_count, c400_idea, c400yr_min = self.get_time_c400_from_min(min=min)
        c100_4_96y = c400_idea.get_kids_in_range(begin=c400yr_min, close=c400yr_min)[0]
        cXXXyr_min = c400yr_min - c100_4_96y._begin

        time_road = self.make_road(self._economy_id, "time")
        tech_road = self.make_road(time_road, "tech")

        # identify which range the time is in
        if c100_4_96y._close - c100_4_96y._begin in (
            50492160,
            52596000,
        ):  # 96 year and 100 year ideas
            yr4_1461_road = self.make_road(tech_road, "4year with leap")
            yr4_1461_idea = self.get_idea_kid(yr4_1461_road)
            yr4_cycles = int(cXXXyr_min / yr4_1461_idea._close)
            cXyr_min = cXXXyr_min % yr4_1461_idea._close
            yr1_idea = yr4_1461_idea.get_kids_in_range(begin=cXyr_min, close=cXyr_min)[
                0
            ]
        elif c100_4_96y._close - c100_4_96y._begin == 2102400:
            yr4_1460_road = self.make_road(tech_road, "4year wo leap")
            yr4_1460_idea = self.get_idea_kid(yr4_1460_road)
            yr4_cycles = 0
            yr1_idea = yr4_1460_idea.get_kids_in_range(cXXXyr_min, cXXXyr_min)[0]
            cXyr_min = cXXXyr_min % yr4_1460_idea._close

        yr1_rem_min = cXyr_min - yr1_idea._begin
        yr1_idea_begin = int(yr1_idea._label.split("-")[0]) - 1

        c100_4_96y_begin = int(c100_4_96y._label.split("-")[0])
        year_num = c100_4_96y_begin + (4 * yr4_cycles) + yr1_idea_begin
        return year_num, yr1_idea, yr1_rem_min

    def get_time_month_from_min(self, min: int):
        time_road = self.make_road(self._economy_id, "time")
        tech_road = self.make_road(time_road, "tech")

        year_num, yr1_idea, yr1_idea_rem_min = self.get_time_c400yr_from_min(min=min)
        yrx = None
        if yr1_idea._close - yr1_idea._begin == 525600:
            yr365_road = self.make_road(tech_road, "365 year")
            yrx = self.get_idea_kid(yr365_road)
        elif yr1_idea._close - yr1_idea._begin == 527040:
            yr366_road = self.make_road(tech_road, "366 year")
            yrx = self.get_idea_kid(yr366_road)
        mon_x = yrx.get_kids_in_range(begin=yr1_idea_rem_min, close=yr1_idea_rem_min)[0]
        month_rem_min = yr1_idea_rem_min - mon_x._begin
        month_num = int(mon_x._label.split("-")[0])
        day_road = self.make_road(tech_road, "day")
        day_x = self.get_idea_kid(day_road)
        day_num = int(month_rem_min / day_x._close)
        day_rem_min = month_rem_min % day_x._close
        return month_num, day_num, day_rem_min, day_x

    def get_time_hour_from_min(self, min: int) -> (int, int, list[int]):
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
        x_hregidea = HregIdea(self._road_node_delimiter)
        return x_hregidea.get_jajatime_legible_from_dt(dt=dt_x)

    def get_jajatime_repeating_legible_text(
        self, open: float = None, nigh: float = None, divisor: float = None
    ) -> str:
        x_hregidea = HregIdea(self._road_node_delimiter)
        str_x = "test3"
        if divisor is None:
            str_x = self.get_jajatime_legible_one_time_event(jajatime_min=open)
            # str_x = f"Weekday, monthpid monthday year"
        elif divisor != None and divisor % 10080 == 0:
            str_x = self._get_jajatime_week_legible_text(open, divisor)
        elif divisor != None and divisor % 1440 == 0:
            if divisor == 1440:
                str_x = (
                    f"every day at {x_hregidea.convert1440toReadableTime(min1440=open)}"
                )
            else:
                num_days = int(divisor / 1440)
                num_with_letter_ending = x_hregidea.get_number_with_letter_ending(
                    num=num_days
                )
                str_x = f"every {num_with_letter_ending} day at {x_hregidea.convert1440toReadableTime(min1440=open)}"
        else:
            str_x = "unknown"

        return str_x

    def _get_jajatime_week_legible_text(self, open: int, divisor: int) -> str:
        x_hregidea = HregIdea(self._road_node_delimiter)
        open_in_week = open % divisor
        time_road = self.make_road(self._economy_id, "time")
        tech_road = self.make_road(time_road, "tech")
        week_road = self.make_road(tech_road, "week")
        weekday_ideas_dict = self.get_idea_ranged_kids(
            idea_road=week_road, begin=open_in_week
        )
        weekday_idea_node = None
        for idea in weekday_ideas_dict.values():
            weekday_idea_node = idea

        if divisor == 10080:
            return f"every {weekday_idea_node._label} at {x_hregidea.convert1440toReadableTime(min1440=open % 1440)}"
        num_with_letter_ending = x_hregidea.get_number_with_letter_ending(
            num=divisor // 10080
        )
        return f"every {num_with_letter_ending} {weekday_idea_node._label} at {x_hregidea.convert1440toReadableTime(min1440=open % 1440)}"

    def get_partys_metrics(self) -> dict[GroupBrand:GroupMetrics]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.balancelinks_metrics

    def add_to_group_agenda_credit_debt(
        self,
        groupbrand: GroupBrand,
        balanceheir_agenda_credit: float,
        balanceheir_agenda_debt: float,
    ):
        for group in self._groups.values():
            if group.brand == groupbrand:
                group.set_empty_agenda_credit_debt_to_zero()
                group._agenda_credit += balanceheir_agenda_credit
                group._agenda_debt += balanceheir_agenda_debt

    def add_to_group_agenda_intent_credit_debt(
        self,
        groupbrand: GroupBrand,
        balanceline_agenda_credit: float,
        balanceline_agenda_debt: float,
    ):
        for group in self._groups.values():
            if (
                group.brand == groupbrand
                and balanceline_agenda_credit != None
                and balanceline_agenda_debt != None
            ):
                group.set_empty_agenda_credit_debt_to_zero()
                group._agenda_intent_credit += balanceline_agenda_credit
                group._agenda_intent_debt += balanceline_agenda_debt

    def add_to_partyunit_agenda_credit_debt(
        self,
        partyunit_pid: PartyPID,
        agenda_credit,
        agenda_debt: float,
        agenda_intent_credit: float,
        agenda_intent_debt: float,
    ):
        for partyunit in self._partys.values():
            if partyunit.pid == partyunit_pid:
                partyunit.add_agenda_credit_debt(
                    agenda_credit=agenda_credit,
                    agenda_debt=agenda_debt,
                    agenda_intent_credit=agenda_intent_credit,
                    agenda_intent_debt=agenda_intent_debt,
                )

    def del_partyunit(self, pid: str):
        self._groups.pop(pid)
        self._partys.pop(pid)

    def add_partyunit(
        self,
        pid: str,
        uid: int = None,
        creditor_weight: int = None,
        debtor_weight: int = None,
        depotlink_type: str = None,
    ):
        partyunit = partyunit_shop(
            pid=PartyPID(pid),
            uid=uid,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
            depotlink_type=depotlink_type,
        )
        self.set_partyunit(partyunit=partyunit)

    def set_partyunit(self, partyunit: PartyUnit):
        # future: if party is new check existance of group with party pid
        self._partys[partyunit.pid] = partyunit

        existing_group = None
        try:
            existing_group = self._groups[partyunit.pid]
        except KeyError:
            partylink = partylink_shop(
                pid=PartyPID(partyunit.pid), creditor_weight=1, debtor_weight=1
            )
            partylinks = {partylink.pid: partylink}
            group_unit = groupunit_shop(
                brand=partyunit.pid,
                _single_party=True,
                _partys=partylinks,
                uid=None,
                single_party_id=None,
            )
            self.set_groupunit(y_groupunit=group_unit)

    def edit_partyunit_pid(
        self,
        old_pid: str,
        new_pid: str,
        allow_party_overwite: bool,
        allow_nonsingle_group_overwrite: bool,
    ):
        # Handle scenarios: some are unacceptable
        old_pid_creditor_weight = self.get_party(old_pid).creditor_weight
        new_pid_groupunit = self.get_groupunit(new_pid)
        new_pid_partyunit = self.get_party(new_pid)
        if not allow_party_overwite and new_pid_partyunit != None:
            raise InvalidAgendaException(
                f"Party '{old_pid}' change to '{new_pid}' failed since '{new_pid}' exists."
            )
        elif (
            not allow_nonsingle_group_overwrite
            and new_pid_groupunit != None
            and new_pid_groupunit._single_party == False
        ):
            raise InvalidAgendaException(
                f"Party '{old_pid}' change to '{new_pid}' failed since non-single group '{new_pid}' exists."
            )
        elif (
            allow_nonsingle_group_overwrite
            and new_pid_groupunit != None
            and new_pid_groupunit._single_party == False
        ):
            self.del_groupunit(groupbrand=new_pid)
        elif self._partys.get(new_pid) != None:
            old_pid_creditor_weight += new_pid_partyunit.creditor_weight

        # upsert new partyunit
        self.add_partyunit(pid=new_pid, creditor_weight=old_pid_creditor_weight)
        # change all influenced groupunits partylinks
        for old_party_groupbrand in self.get_party_groupbrands(old_pid):
            old_party_groupunit = self.get_groupunit(old_party_groupbrand)
            old_party_groupunit._move_partylink(old_pid, new_pid)
        self.del_partyunit(pid=old_pid)

    def get_party(self, partypid: PartyPID) -> PartyUnit:
        return self._partys.get(partypid)

    def get_partyunits_pid_list(self) -> dict[PartyPID]:
        partypid_list = list(self._partys.keys())
        partypid_list.append("")
        partypid_dict = {partypid.lower(): partypid for partypid in partypid_list}
        partypid_lowercase_ordered_list = sorted(list(partypid_dict))
        return [
            partypid_dict[partypid_l] for partypid_l in partypid_lowercase_ordered_list
        ]

    def get_partyunits_uid_max(self) -> int:
        uid_max = 1
        for x_partyunit in self._partys.values():
            if x_partyunit.uid != None and x_partyunit.uid > uid_max:
                uid_max = x_partyunit.uid
        return uid_max

    def get_partyunits_uid_dict(self) -> dict[int:int]:
        uid_dict = {}
        for x_partyunit in self._partys.values():
            if uid_dict.get(x_partyunit.uid) is None:
                uid_dict[x_partyunit.uid] = 1
            else:
                uid_dict[x_partyunit.uid] += 1
        return uid_dict

    def set_all_partyunits_uids_unique(self) -> int:
        uid_max = self.get_partyunits_uid_max()
        uid_dict = self.get_partyunits_uid_dict()
        for x_partyunit in self._partys.values():
            if uid_dict.get(x_partyunit.uid) > 0:
                new_uid_max = uid_max + 1
                x_partyunit.uid = new_uid_max
                uid_max = x_partyunit.uid

    def all_partyunits_uids_are_unique(self) -> bool:
        uid_dict = self.get_partyunits_uid_dict()
        return not any(
            uid_count > 1 or uid is None for uid, uid_count in uid_dict.items()
        )

    def get_partys_depotlink_count(self) -> int:
        return sum(party_x.depotlink_type != None for party_x in self._partys.values())

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

    def set_groupunit(
        self,
        y_groupunit: GroupUnit,
        create_missing_partys: bool = None,
        replace: bool = True,
        add_partylinks: bool = None,
    ):
        if replace is None:
            replace = False
        if add_partylinks is None:
            add_partylinks = False
        if (
            self.get_groupunit(y_groupunit.brand) is None
            or replace
            and not add_partylinks
        ):
            self._groups[y_groupunit.brand] = y_groupunit

        if add_partylinks:
            x_groupunit = self.get_groupunit(y_groupunit.brand)
            for x_partylink in y_groupunit._partys.values():
                x_groupunit.set_partylink(x_partylink)

        if create_missing_partys:
            self._create_missing_partys(partylinks=y_groupunit._partys)

    def get_groupunit(self, x_groupbrand: GroupBrand) -> GroupUnit:
        return self._groups.get(x_groupbrand)

    def _create_missing_partys(self, partylinks: dict[PartyPID:PartyLink]):
        for partylink_x in partylinks.values():
            if self._partys.get(partylink_x.pid) is None:
                self.set_partyunit(
                    partyunit=partyunit_shop(
                        pid=partylink_x.pid,
                        creditor_weight=partylink_x.creditor_weight,
                        debtor_weight=partylink_x.debtor_weight,
                    )
                )

    def del_groupunit(self, groupbrand: GroupBrand):
        self._groups.pop(groupbrand)

    def edit_groupunit_brand(
        self, old_brand: GroupBrand, new_brand: GroupBrand, allow_group_overwite: bool
    ):
        if not allow_group_overwite and self._groups.get(new_brand) != None:
            raise InvalidAgendaException(
                f"Group '{old_brand}' change to '{new_brand}' failed since '{new_brand}' exists."
            )
        elif self._groups.get(new_brand) != None:
            old_groupunit = self._groups.get(old_brand)
            old_groupunit.set_brand(brand=new_brand)
            self._groups.get(new_brand).meld(other_group=old_groupunit)
            self.del_groupunit(groupbrand=old_brand)
        elif self._groups.get(new_brand) is None:
            old_groupunit = self._groups.get(old_brand)
            groupunit_x = groupunit_shop(
                brand=new_brand,
                uid=old_groupunit.uid,
                _partys=old_groupunit._partys,
                single_party_id=old_groupunit.single_party_id,
                _single_party=old_groupunit._single_party,
            )
            self.set_groupunit(y_groupunit=groupunit_x)
            self.del_groupunit(groupbrand=old_brand)

        self._edit_balancelinks_brand(
            old_brand=old_brand,
            new_brand=new_brand,
            allow_group_overwite=allow_group_overwite,
        )

    def _edit_balancelinks_brand(
        self,
        old_brand: GroupBrand,
        new_brand: GroupBrand,
        allow_group_overwite: bool,
    ):
        for x_idea in self.get_idea_list():
            if (
                x_idea._balancelinks.get(new_brand) != None
                and x_idea._balancelinks.get(old_brand) != None
            ):
                old_balancelink = x_idea._balancelinks.get(old_brand)
                old_balancelink.brand = new_brand
                x_idea._balancelinks.get(new_brand).meld(
                    other_balancelink=old_balancelink,
                    other_on_meld_weight_action="sum",
                    src_on_meld_weight_action="sum",
                )

                x_idea.del_balancelink(groupbrand=old_brand)
            elif (
                x_idea._balancelinks.get(new_brand) is None
                and x_idea._balancelinks.get(old_brand) != None
            ):
                old_balancelink = x_idea._balancelinks.get(old_brand)
                new_balancelink = balancelink_shop(
                    brand=new_brand,
                    creditor_weight=old_balancelink.creditor_weight,
                    debtor_weight=old_balancelink.debtor_weight,
                )
                x_idea.set_balancelink(balancelink=new_balancelink)
                x_idea.del_balancelink(groupbrand=old_brand)

    def get_groupunits_brand_list(self) -> list[GroupBrand]:
        groupbrand_list = list(self._groups.keys())
        groupbrand_list.append("")
        groupbrand_dict = {
            groupbrand.lower(): groupbrand for groupbrand in groupbrand_list
        }
        groupbrand_lowercase_ordered_list = sorted(list(groupbrand_dict))
        return [
            groupbrand_dict[group_l] for group_l in groupbrand_lowercase_ordered_list
        ]

    def set_time_acptfacts(self, open: datetime = None, nigh: datetime = None) -> None:
        open_minutes = self.get_time_min_from_dt(dt=open) if open != None else None
        nigh_minutes = self.get_time_min_from_dt(dt=nigh) if nigh != None else None
        time_road = self.make_road(self._economy_id, "time")
        minutes_acptfact = self.make_road(time_road, "jajatime")
        self.set_acptfact(
            base=minutes_acptfact,
            pick=minutes_acptfact,
            open=open_minutes,
            nigh=nigh_minutes,
        )

    def _is_idea_rangeroot(self, idea_road: RoadUnit) -> bool:
        anc_roads = get_ancestor_roads(road=idea_road)
        parent_road = self._economy_id if len(anc_roads) == 1 else anc_roads[1]

        # figure out if parent is range
        parent_range = None
        if len(get_all_road_nodes(parent_road)) == 1:
            parent_range = False
        else:
            parent_idea = self.get_idea_kid(parent_road)
            parent_range = parent_idea._begin != None and parent_idea._close != None

        # figure out if numeric source exists
        x_idea = self.get_idea_kid(idea_road)
        numeric_source_road = None
        numeric_source_road = x_idea._numeric_road != None

        return not numeric_source_road and not parent_range

    def _get_rangeroot_acptfactunits(self) -> list[AcptFactUnit]:
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
        x_lemmas = lemmas_shop()
        # lemma_ideas = {}
        for acptfact in ranged_acptfactunits:
            acptfact_idea = self.get_idea_kid(acptfact.base)
            for kid in acptfact_idea._kids.values():
                x_lemmas.eval(x_idea=kid, src_acptfact=acptfact, src_idea=acptfact_idea)

            if acptfact_idea._range_source_road != None:
                x_lemmas.eval(
                    x_idea=self.get_idea_kid(acptfact_idea._range_source_road),
                    src_acptfact=acptfact,
                    src_idea=acptfact_idea,
                )
        return x_lemmas

    def _get_lemma_acptfactunits(self) -> dict:
        # get all range-root first level kids and range_source_road
        x_lemmas = self._get_rangeroot_1stlevel_associates(
            self._get_rangeroot_acptfactunits()
        )

        # Now get associates (all their descendants and range_source_roads)
        lemma_acptfactunits = {}  # acptfact.base : acptfactUnit
        count_x = 0
        while x_lemmas.is_lemmas_evaluated() == False or count_x > 10000:
            count_x += 1
            if count_x == 9998:
                raise InvalidAgendaException("lemma loop failed")

            lemma_y = x_lemmas.get_unevaluated_lemma()
            lemma_idea = lemma_y.x_idea
            acptfact_x = lemma_y.calc_acptfact

            road_x = self.make_road(lemma_idea._pad, lemma_idea._label)
            lemma_acptfactunits[road_x] = acptfact_x

            for kid2 in lemma_idea._kids.values():
                x_lemmas.eval(x_idea=kid2, src_acptfact=acptfact_x, src_idea=lemma_idea)
            if lemma_idea._range_source_road not in [None, ""]:
                x_lemmas.eval(
                    x_idea=self.get_idea_kid(lemma_idea._range_source_road),
                    src_acptfact=acptfact_x,
                    src_idea=lemma_idea,
                )

        return lemma_acptfactunits

    def set_acptfact(
        self,
        base: RoadUnit,
        pick: RoadUnit,
        open: float = None,
        nigh: float = None,
        create_missing_ideas: bool = None,
    ):  # sourcery skip: low-code-quality
        if create_missing_ideas:
            self._set_ideakid_if_empty(road=base)
            self._set_ideakid_if_empty(road=pick)

        self._execute_tree_traverse()
        acptfact_base_idea = self.get_idea_kid(base)
        x_acptfactunit = acptfactunit_shop(base=base, pick=pick, open=open, nigh=nigh)
        x_idearoot = self.get_idea_kid(self._economy_id)

        if acptfact_base_idea._begin is None and acptfact_base_idea._close is None:
            x_idearoot.set_acptfactunit(x_acptfactunit)

        # if acptfact's idea no range or is a "range-root" then allow acptfact to be set by user
        elif (
            acptfact_base_idea._begin != None
            and acptfact_base_idea._close != None
            and self._is_idea_rangeroot(idea_road=base) == False
        ):
            raise InvalidAgendaException(
                f"Non range-root acptfact:{base} can only be set by range-root acptfact"
            )

        elif (
            acptfact_base_idea._begin != None
            and acptfact_base_idea._close != None
            and self._is_idea_rangeroot(idea_road=base)
        ):
            # WHEN idea is "range-root" identify any required.bases that are descendants
            # calculate and set those descendant acptfacts
            # example: timeline range (0-, 1.5e9) is range-root
            # example: "timeline,weeks" (spllt 10080) is range-descendant
            # there exists a required base "timeline,weeks" with sufffact.need = "timeline,weeks"
            # and (1,2) divisor=2 (every other week)
            #
            # user should not set "timeline,weeks" acptfact, only "timeline" acptfact and
            # "timeline,weeks" should be set automatica_lly since there exists a required
            # that has that base.
            x_idearoot.set_acptfactunit(x_acptfactunit)

            # Find all AcptFact descendants and any range_source_road connections "Lemmas"
            lemmas_dict = self._get_lemma_acptfactunits()
            for current_acptfact in x_idearoot._acptfactunits.values():
                for lemma_acptfact in lemmas_dict.values():
                    if lemma_acptfact.base == current_acptfact.base:
                        x_idearoot.set_acptfactunit(
                            acptfactunit_shop(
                                base=lemma_acptfact.base,
                                pick=lemma_acptfact.pick,
                                open=lemma_acptfact.open,
                                nigh=lemma_acptfact.nigh,
                            )
                        )
                        x_idearoot._acptfactunits[lemma_acptfact.base] = lemma_acptfact

            for missing_acptfact in self.get_missing_acptfact_bases().keys():
                for lemma_acptfact in lemmas_dict.values():
                    if lemma_acptfact.base == missing_acptfact:
                        x_idearoot._acptfactunits[lemma_acptfact.base] = lemma_acptfact

        self.set_agenda_metrics()

    def get_acptfactunits_base_and_acptfact_list(self) -> list:
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

    def del_acptfact(self, base: RoadUnit):
        self._idearoot.del_acptfactunit(base)

    def get_tree_metrics(self) -> TreeMetrics:
        tree_metrics = TreeMetrics()
        tree_metrics.evaluate_node(
            level=self._idearoot._level,
            requireds=self._idearoot._requiredunits,
            balancelinks=self._idearoot._balancelinks,
            uid=self._idearoot._uid,
            promise=self._idearoot.promise,
            idea_road=self._idearoot.get_idea_road(),
        )

        x_idea_list = [self._idearoot]
        while x_idea_list != []:
            parent_idea = x_idea_list.pop()
            for idea_kid in parent_idea._kids.values():
                self._eval_tree_metrics(
                    parent_idea, idea_kid, tree_metrics, x_idea_list
                )
        return tree_metrics

    def _eval_tree_metrics(self, parent_idea, idea_kid, tree_metrics, x_idea_list):
        idea_kid._level = parent_idea._level + 1
        tree_metrics.evaluate_node(
            level=idea_kid._level,
            requireds=idea_kid._requiredunits,
            balancelinks=idea_kid._balancelinks,
            uid=idea_kid._uid,
            promise=idea_kid.promise,
            idea_road=idea_kid.get_idea_road(),
        )
        x_idea_list.append(idea_kid)

    def get_idea_uid_max(self) -> int:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.uid_max

    def set_all_idea_uids_unique(self):
        tree_metrics = self.get_tree_metrics()
        idea_uid_max = tree_metrics.uid_max
        idea_uid_dict = tree_metrics.uid_dict

        for x_idea in self.get_idea_list():
            if x_idea._uid is None or idea_uid_dict.get(x_idea._uid) > 1:
                new_idea_uid_max = idea_uid_max + 1
                self.edit_idea_attr(road=x_idea.get_idea_road(), uid=new_idea_uid_max)
                idea_uid_max = new_idea_uid_max

    def get_node_count(self) -> int:
        # tree_metrics = self.get_tree_metrics()
        # return tree_metrics.node_count
        return len(self._idea_dict)

    def get_level_count(self, level) -> int:
        tree_metrics = self.get_tree_metrics()
        level_count = None
        try:
            level_count = tree_metrics.level_count[level]
        except KeyError:
            level_count = 0
        return level_count

    def get_required_bases(self) -> dict[RoadUnit:int]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.required_bases

    def get_missing_acptfact_bases(self) -> dict[RoadUnit:int]:
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
        pad: RoadUnit,
        create_missing_ideas_groups: bool = None,
        adoptees: list[str] = None,
        bundling=True,
    ):
        idea_kid._road_node_delimiter = self._road_node_delimiter

        if not create_missing_ideas_groups:
            idea_kid = self._get_filtered_balancelinks_idea(idea_kid)

        pad = road_validate(pad, self._road_node_delimiter, self._economy_id)
        temp_idea = self._idearoot
        pad_nodes = get_all_road_nodes(pad, delimiter=self._road_node_delimiter)
        temp_road = pad_nodes.pop(0)

        # idearoot cannot be replaced
        if temp_road == self._economy_id and pad_nodes == []:
            idea_kid.set_pad(parent_road=self._economy_id)
        else:
            road_nodes = [temp_road]
            while pad_nodes != []:
                temp_road = pad_nodes.pop(0)
                temp_idea = self._get_or_create_leveln_idea(
                    parent_idea=temp_idea, idea_label=temp_road
                )
                temp_idea._road_node_delimiter = self._road_node_delimiter
                road_nodes.append(temp_road)
            idea_kid.set_pad(parent_road=self.make_road(road_nodes=road_nodes))
        idea_kid._road_node_delimiter = self._road_node_delimiter
        temp_idea.add_kid(idea_kid)

        kid_road = self.make_road(pad, idea_kid._label)

        if adoptees != None:
            weight_sum = 0
            for adoptee_label in adoptees:
                adoptee_road = self.make_road(pad, adoptee_label)
                adoptee_idea = self.get_idea_kid(adoptee_road)
                weight_sum += adoptee_idea._weight
                new_adoptee_pad = self.make_road(kid_road, adoptee_label)
                self.add_idea(adoptee_idea, new_adoptee_pad)
                self.edit_idea_attr(road=new_adoptee_pad, weight=adoptee_idea._weight)
                self.del_idea_kid(adoptee_road)

            if bundling:
                self.edit_idea_attr(road=kid_road, weight=weight_sum)

        if create_missing_ideas_groups:
            self._create_missing_ideas(road=kid_road)
            self._create_missing_groups_partys(balancelinks=idea_kid._balancelinks)

    def _get_filtered_balancelinks_idea(self, idea: IdeaCore) -> IdeaCore:
        _balancelinks_to_delete = [
            _balancelink_pid
            for _balancelink_pid in idea._balancelinks.keys()
            if self._groups.get(_balancelink_pid) is None
        ]
        for _balancelink_pid in _balancelinks_to_delete:
            idea._balancelinks.pop(_balancelink_pid)

        if idea._assignedunit != None:
            _suffgroups_to_delete = [
                _suffgroup_pid
                for _suffgroup_pid in idea._assignedunit._suffgroups.keys()
                if self._groups.get(_suffgroup_pid) is None
            ]
            for _suffgroup_pid in _suffgroups_to_delete:
                idea._assignedunit.del_suffgroup(_suffgroup_pid)

        return idea

    def _create_missing_groups_partys(self, balancelinks: dict[GroupBrand:BalanceLink]):
        for balancelink_x in balancelinks.values():
            if self._groups.get(balancelink_x.brand) is None:
                groupunit_x = groupunit_shop(brand=balancelink_x.brand, _partys={})
                self.set_groupunit(y_groupunit=groupunit_x)

    def _create_missing_ideas(self, road):
        self.set_agenda_metrics()
        posted_idea = self.get_idea_kid(road)

        for required_x in posted_idea._requiredunits.values():
            self._set_ideakid_if_empty(road=required_x.base)
            for sufffact_x in required_x.sufffacts.values():
                self._set_ideakid_if_empty(road=sufffact_x.need)
        if posted_idea._range_source_road != None:
            self._set_ideakid_if_empty(road=posted_idea._range_source_road)
        if posted_idea._numeric_road != None:
            self._set_ideakid_if_empty(road=posted_idea._numeric_road)

    def _set_ideakid_if_empty(self, road: RoadUnit):
        try:
            self.get_idea_kid(road)
        except InvalidAgendaException:
            base_idea = ideacore_shop(
                _label=get_terminus_node_from_road(road=road),
                _pad=get_pad_from_road(road=road),
            )
            self.add_idea(base_idea, pad=base_idea._pad)

    def _get_or_create_leveln_idea(
        self, parent_idea: IdeaCore, idea_label: str
    ) -> IdeaCore:
        return_idea = None
        try:
            return_idea = parent_idea._kids[idea_label]
        except Exception:
            KeyError
            parent_idea.add_kid(ideacore_shop(idea_label))
            return_idea = parent_idea._kids[idea_label]

        return return_idea

    def del_idea_kid(self, road: RoadUnit, del_children: bool = True):
        x_road = get_all_road_nodes(road)
        temp_label = x_road.pop(0)
        temps_d = [temp_label]

        if x_road == []:
            raise InvalidAgendaException("Object cannot delete itself")
        temp_label = x_road.pop(0)
        temps_d.append(temp_label)

        if x_road == []:
            if not del_children:
                self._move_idea_kids(road_nodes=temps_d)
            self._idearoot._kids.pop(temp_label)
        elif x_road != []:
            i_temp_idea = self._idearoot._kids[temp_label]
            while x_road != []:
                temp_label = x_road.pop(0)
                parent_temp_idea = i_temp_idea
                i_temp_idea = i_temp_idea._kids[temp_label]

            if not del_children:
                self.set_agenda_metrics()
                self._move_idea_kids(road_nodes=get_all_road_nodes(road))
            parent_temp_idea._kids.pop(temp_label)
        self.set_agenda_metrics()

    def _move_idea_kids(self, road_nodes: list):
        d_temp_idea = self.get_idea_kid(self.make_road(road_nodes=road_nodes))
        for kid in d_temp_idea._kids.values():
            self.add_idea(kid, pad=self.make_road(road_nodes=road_nodes[:-1]))

    def set_healer(self, new_healer):
        self._healer = new_healer

    def edit_idea_label(
        self,
        old_road: RoadUnit,
        new_label: str,
    ):
        if self._road_node_delimiter in new_label:
            raise InvalidLabelException(
                f"Cannot change '{old_road}' because new_label {new_label} contains delimiter {self._road_node_delimiter}"
            )

        # check idea exists
        if self.get_idea_kid(old_road) is None:
            raise InvalidAgendaException(f"Idea {old_road=} does not exist")

        pad = get_pad_from_road(road=old_road)
        new_road = (
            self.make_road(new_label) if pad == "" else self.make_road(pad, new_label)
        )
        if old_road != new_road:
            # if root _label is changed
            if pad == "":
                self._idearoot.set_idea_label(
                    new_label, agenda_economy_id=self._economy_id
                )
                self._idearoot._pad = pad
            else:
                self._non_root_idea_label_edit(old_road, new_label, pad)
            self._idearoot_find_replace_road(old_road=old_road, new_road=new_road)
            self._idearoot._acptfactunits = find_replace_road_key_dict(
                dict_x=self._idearoot._acptfactunits,
                old_road=old_road,
                new_road=new_road,
            )

    def _non_root_idea_label_edit(self, old_road, new_label, pad):
        x_idea = self.get_idea_kid(old_road)
        x_idea.set_idea_label(new_label)
        x_idea._pad = pad
        idea_parent = self.get_idea_kid(get_pad_from_road(old_road))
        idea_parent._kids.pop(get_terminus_node_from_road(old_road))
        idea_parent._kids[x_idea._label] = x_idea

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
                        ref_road=idea_kid._pad,
                        sub_road=old_road,
                    ):
                        idea_kid._pad = change_road(
                            current_road=idea_kid._pad,
                            old_road=old_road,
                            new_road=new_road,
                        )
                    idea_kid.find_replace_road(old_road=old_road, new_road=new_road)

    def _set_ideaattrfilter_sufffact_ranges(self, x_ideaattrfilter: IdeaAttrFilter):
        suffact_idea = self.get_idea_kid(x_ideaattrfilter.get_sufffact_need())
        x_ideaattrfilter.set_sufffact_range_attributes_influenced_by_sufffact_idea(
            sufffact_open=suffact_idea._begin,
            sufffact_nigh=suffact_idea._close,
            # suffact_numor=suffact_idea.anc_numor,
            sufffact_denom=suffact_idea._denom,
            # anc_reest=suffact_idea.anc_reest,
        )

    def _set_ideaattrfilter_begin_close(
        self, ideaattrfilter: IdeaAttrFilter, idea_road: RoadUnit
    ) -> (float, float):
        x_iaf = ideaattrfilter
        anc_roads = get_ancestor_roads(road=idea_road)
        if (
            x_iaf.addin != None
            or x_iaf.numor != None
            or x_iaf.denom != None
            or x_iaf.reest != None
        ) and len(anc_roads) == 1:
            raise InvalidAgendaException("Root Idea cannot have numor denom reest.")
        parent_road = self._economy_id if len(anc_roads) == 1 else anc_roads[1]

        parent_has_range = None
        parent_idea = self.get_idea_kid(parent_road)
        parent_begin = parent_idea._begin
        parent_close = parent_idea._close
        parent_has_range = parent_begin is not None and parent_close is not None

        numeric_begin = None
        numeric_close = None
        numeric_range = None
        if x_iaf.numeric_road != None:
            numeric_idea = self.get_idea_kid(x_iaf.numeric_road)
            numeric_begin = numeric_idea._begin
            numeric_close = numeric_idea._close
            numeric_range = numeric_begin != None and numeric_close != None

        if parent_has_range and x_iaf.addin not in [None, 0]:
            parent_begin = parent_begin + x_iaf.addin
            parent_close = parent_close + x_iaf.addin

        x_begin, x_close = self._transform_begin_close(
            reest=x_iaf.reest,
            begin=x_iaf.begin,
            close=x_iaf.close,
            numor=x_iaf.numor,
            denom=x_iaf.denom,
            parent_has_range=parent_has_range,
            parent_begin=parent_begin,
            parent_close=parent_close,
            numeric_range=numeric_range,
            numeric_begin=numeric_begin,
            numeric_close=numeric_close,
        )

        if parent_has_range and numeric_range:
            raise InvalidAgendaException(
                "Idea has begin-close range parent, cannot have numeric_road"
            )
        elif not parent_has_range and not numeric_range and x_iaf.numor != None:
            raise InvalidAgendaException(
                f"Idea cannot edit numor={x_iaf.numor}/denom/reest of '{idea_road}' if parent '{parent_road}' or ideacore._numeric_road does not have begin/close range"
            )
        ideaattrfilter.begin = x_begin
        ideaattrfilter.close = x_close

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
        road: RoadUnit,
        weight: int = None,
        uid: int = None,
        required: RequiredUnit = None,
        required_base: RoadUnit = None,
        required_sufffact: RoadUnit = None,
        required_sufffact_open: float = None,
        required_sufffact_nigh: float = None,
        required_sufffact_divisor: int = None,
        required_del_sufffact_base: RoadUnit = None,
        required_del_sufffact_need: RoadUnit = None,
        required_suff_idea_active_status: str = None,
        assignedunit: AssignedUnit = None,
        begin: float = None,
        close: float = None,
        addin: float = None,
        numor: float = None,
        denom: float = None,
        reest: bool = None,
        numeric_road: RoadUnit = None,
        range_source_road: float = None,
        promise: bool = None,
        problem_bool: bool = None,
        acptfactunit: AcptFactUnit = None,
        descendant_promise_count: int = None,
        all_party_credit: bool = None,
        all_party_debt: bool = None,
        balancelink: BalanceLink = None,
        balancelink_del: GroupBrand = None,
        is_expanded: bool = None,
        on_meld_weight_action: str = None,
    ):
        x_ideaattrfilter = ideaattrfilter_shop(
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
            all_party_credit=all_party_credit,
            all_party_debt=all_party_debt,
            balancelink=balancelink,
            balancelink_del=balancelink_del,
            is_expanded=is_expanded,
            promise=promise,
            problem_bool=problem_bool,
            acptfactunit=acptfactunit,
            on_meld_weight_action=on_meld_weight_action,
        )
        if x_ideaattrfilter.has_numeric_attrs():
            self._set_ideaattrfilter_begin_close(x_ideaattrfilter, road)
        if x_ideaattrfilter.has_required_sufffact():
            self._set_ideaattrfilter_sufffact_ranges(x_ideaattrfilter)
        x_idea = self.get_idea_kid(road)
        x_idea._set_idea_attr(idea_attr=x_ideaattrfilter)

        # deleting or setting a balancelink reqquires a tree traverse to correctly set balanceheirs and balancelines
        if balancelink_del != None or balancelink != None:
            self.set_agenda_metrics()

    def del_idea_required_sufffact(
        self, road: RoadUnit, required_base: RoadUnit, required_sufffact: RoadUnit
    ):
        self.edit_idea_attr(
            road=road,
            required_del_sufffact_base=required_base,
            required_del_sufffact_need=required_sufffact,
        )

    def get_intent_items(
        self,
        base: RoadUnit = None,
        intent_enterprise: bool = True,
        intent_state: bool = True,
    ) -> list[IdeaCore]:
        return [
            idea
            for idea in self.get_idea_list()
            if idea.is_intent_item(necessary_base=base)
        ]

    def set_intent_task_complete(self, task_road: RoadUnit, base: RoadUnit):
        promise_item = self.get_idea_kid(task_road)
        promise_item.set_acptfactunit_to_complete(
            base_acptfactunit=self._idearoot._acptfactunits[base]
        )

    def get_partyunit_total_creditor_weight(self) -> float:
        return sum(
            partyunit.get_creditor_weight() for partyunit in self._partys.values()
        )

    def get_partyunit_total_debtor_weight(self) -> float:
        return sum(partyunit.get_debtor_weight() for partyunit in self._partys.values())

    def _add_to_partyunits_agenda_credit_debt(self, idea_agenda_importance: float):
        sum_partyunit_creditor_weight = self.get_partyunit_total_creditor_weight()
        sum_partyunit_debtor_weight = self.get_partyunit_total_debtor_weight()

        for x_partyunit in self._partys.values():
            au_agenda_credit = (
                idea_agenda_importance * x_partyunit.get_creditor_weight()
            ) / sum_partyunit_creditor_weight

            au_agenda_debt = (
                idea_agenda_importance * x_partyunit.get_debtor_weight()
            ) / sum_partyunit_debtor_weight

            x_partyunit.add_agenda_credit_debt(
                agenda_credit=au_agenda_credit,
                agenda_debt=au_agenda_debt,
                agenda_intent_credit=0,
                agenda_intent_debt=0,
            )

    def _add_to_partyunits_agenda_intent_credit_debt(
        self, idea_agenda_importance: float
    ):
        sum_partyunit_creditor_weight = self.get_partyunit_total_creditor_weight()
        sum_partyunit_debtor_weight = self.get_partyunit_total_debtor_weight()

        for x_partyunit in self._partys.values():
            au_agenda_intent_credit = (
                idea_agenda_importance * x_partyunit.get_creditor_weight()
            ) / sum_partyunit_creditor_weight

            au_agenda_intent_debt = (
                idea_agenda_importance * x_partyunit.get_debtor_weight()
            ) / sum_partyunit_debtor_weight

            x_partyunit.add_agenda_credit_debt(
                agenda_credit=0,
                agenda_debt=0,
                agenda_intent_credit=au_agenda_intent_credit,
                agenda_intent_debt=au_agenda_intent_debt,
            )

    def _set_partyunits_agenda_intent_importance(self, agenda_intent_importance: float):
        sum_partyunit_creditor_weight = self.get_partyunit_total_creditor_weight()
        sum_partyunit_debtor_weight = self.get_partyunit_total_debtor_weight()

        for x_partyunit in self._partys.values():
            au_agenda_intent_credit = (
                agenda_intent_importance * x_partyunit.get_creditor_weight()
            ) / sum_partyunit_creditor_weight

            au_agenda_intent_debt = (
                agenda_intent_importance * x_partyunit.get_debtor_weight()
            ) / sum_partyunit_debtor_weight

            x_partyunit.add_agenda_intent_credit_debt(
                agenda_intent_credit=au_agenda_intent_credit,
                agenda_intent_debt=au_agenda_intent_debt,
            )

    def _reset_groupunits_agenda_credit_debt(self):
        for balancelink_obj in self._groups.values():
            balancelink_obj.reset_agenda_credit_debt()

    def _set_groupunits_agenda_importance(
        self, balanceheirs: dict[GroupBrand:BalanceLink]
    ):
        for balancelink_obj in balanceheirs.values():
            self.add_to_group_agenda_credit_debt(
                groupbrand=balancelink_obj.brand,
                balanceheir_agenda_credit=balancelink_obj._agenda_credit,
                balanceheir_agenda_debt=balancelink_obj._agenda_debt,
            )

    def _distribute_agenda_intent_importance(self):
        for idea in self._idea_dict.values():
            # If there are no balancelines associated with idea
            # distribute agenda_importance via general partyunit
            # credit ratio and debt ratio
            # if idea.is_intent_item() and idea._balancelines == {}:
            if idea.is_intent_item():
                if idea._balancelines == {}:
                    self._add_to_partyunits_agenda_intent_credit_debt(
                        idea._agenda_importance
                    )
                else:
                    for x_balanceline in idea._balancelines.values():
                        self.add_to_group_agenda_intent_credit_debt(
                            groupbrand=x_balanceline.brand,
                            balanceline_agenda_credit=x_balanceline._agenda_credit,
                            balanceline_agenda_debt=x_balanceline._agenda_debt,
                        )

    def _distribute_groups_agenda_importance(self):
        for group_obj in self._groups.values():
            group_obj._set_partylink_agenda_credit_debt()
            for partylink in group_obj._partys.values():
                self.add_to_partyunit_agenda_credit_debt(
                    partyunit_pid=partylink.pid,
                    agenda_credit=partylink._agenda_credit,
                    agenda_debt=partylink._agenda_debt,
                    agenda_intent_credit=partylink._agenda_intent_credit,
                    agenda_intent_debt=partylink._agenda_intent_debt,
                )

    def _set_agenda_intent_ratio_credit_debt(self):
        agenda_intent_ratio_credit_sum = 0
        agenda_intent_ratio_debt_sum = 0

        for x_partyunit in self._partys.values():
            agenda_intent_ratio_credit_sum += x_partyunit._agenda_intent_credit
            agenda_intent_ratio_debt_sum += x_partyunit._agenda_intent_debt

        for x_partyunit in self._partys.values():
            x_partyunit.set_agenda_intent_ratio_credit_debt(
                agenda_intent_ratio_credit_sum=agenda_intent_ratio_credit_sum,
                agenda_intent_ratio_debt_sum=agenda_intent_ratio_debt_sum,
                agenda_partyunit_total_creditor_weight=self.get_partyunit_total_creditor_weight(),
                agenda_partyunit_total_debtor_weight=self.get_partyunit_total_debtor_weight(),
            )

    def get_party_groupbrands(self, party_pid: PartyPID) -> list[GroupBrand]:
        return [
            x_groupunit.brand
            for x_groupunit in self._groups.values()
            if x_groupunit.has_partylink(party_pid)
        ]

    def _reset_partyunit_agenda_credit_debt(self):
        for partyunit in self._partys.values():
            partyunit.reset_agenda_credit_debt()

    def get_idea_kid(self, road: RoadUnit) -> IdeaCore:
        if road is None:
            raise InvalidAgendaException("get_idea_kid received road=None")
        nodes = get_all_road_nodes(road, delimiter=self._road_node_delimiter)
        src = nodes.pop(0)
        temp_idea = None

        if nodes == [] and src == self._idearoot._label:
            temp_idea = self._idearoot
        else:
            idea_label = src if nodes == [] else nodes.pop(0)
            try:
                temp_idea = self._idearoot._kids.get(idea_label)

                while nodes != []:
                    idea_label = nodes.pop(0)
                    temp_idea = temp_idea._kids[idea_label]
                if temp_idea is None:
                    raise InvalidAgendaException(
                        f"Temp_idea is None {idea_label=}. No item at '{road}'"
                    )
            except:
                raise InvalidAgendaException(
                    f"Getting {idea_label=} failed no item at '{road}'"
                )

        return temp_idea

    def get_idea_ranged_kids(
        self, idea_road: str, begin: float = None, close: float = None
    ) -> dict[IdeaCore]:
        parent_idea = self.get_idea_kid(idea_road)
        if begin is None and close is None:
            begin = parent_idea._begin
            close = parent_idea._close
        elif begin != None and close is None:
            close = begin

        idea_list = parent_idea.get_kids_in_range(begin=begin, close=close)
        return {x_idea._label: x_idea for x_idea in idea_list}

    def _set_ancestor_metrics(self, road: RoadUnit):
        # sourcery skip: low-code-quality
        da_count = 0
        child_balancelines = None
        if road is None:
            road = ""

        group_everyone = None
        if len(get_all_road_nodes(road)) <= 1:
            group_everyone = self._idearoot._balanceheirs == {}
        else:
            ancestor_roads = get_ancestor_roads(road=road)
            # remove root road
            ancestor_roads.pop(len(ancestor_roads) - 1)

            while ancestor_roads != []:
                # youngest_unprocessed_idea
                yu_idea_obj = self.get_idea_kid(road=ancestor_roads.pop(0))
                yu_idea_obj.set_descendant_promise_count_zero_if_null()
                yu_idea_obj._descendant_promise_count += da_count
                if yu_idea_obj.is_kidless():
                    yu_idea_obj.set_kidless_balancelines()
                    child_balancelines = yu_idea_obj._balancelines
                else:
                    yu_idea_obj.set_balancelines(child_balancelines=child_balancelines)

                if yu_idea_obj._task:
                    da_count += 1

                if (
                    group_everyone != False
                    and yu_idea_obj._all_party_credit != False
                    and yu_idea_obj._all_party_debt != False
                    and yu_idea_obj._balanceheirs != {}
                    or group_everyone != False
                    and yu_idea_obj._all_party_credit == False
                    and yu_idea_obj._all_party_debt == False
                ):
                    group_everyone = False
                elif group_everyone != False:
                    group_everyone = True
                yu_idea_obj._all_party_credit = group_everyone
                yu_idea_obj._all_party_debt = group_everyone

            if (
                group_everyone != False
                and self._idearoot._all_party_credit != False
                and self._idearoot._all_party_debt != False
                and self._idearoot._balanceheirs != {}
                or group_everyone != False
                and self._idearoot._all_party_credit == False
                and self._idearoot._all_party_debt == False
            ):
                group_everyone = False
            elif group_everyone != False and yu_idea_obj._balanceheirs == {}:
                group_everyone = True

        self._idearoot._all_party_credit = group_everyone
        self._idearoot._all_party_debt = group_everyone

        if self._idearoot.is_kidless():
            self._idearoot.set_kidless_balancelines()
        else:
            self._idearoot.set_balancelines(child_balancelines=child_balancelines)
        self._idearoot.set_descendant_promise_count_zero_if_null()
        self._idearoot._descendant_promise_count += da_count

    def _set_root_attributes(self):
        x_idearoot = self._idearoot
        x_idearoot._level = 0
        x_idearoot.set_pad(parent_road="")
        x_idearoot.set_idearoot_inherit_requiredheirs()
        x_idearoot.set_assignedheir(parent_assignheir=None, agenda_groups=self._groups)
        x_idearoot.set_acptfactheirs(acptfacts=self._idearoot._acptfactunits)
        x_idearoot.inherit_balanceheirs()
        x_idearoot.clear_balancelines()
        x_idearoot._weight = 1
        x_idearoot._kids_total_weight = 0
        x_idearoot.set_kids_total_weight()
        x_idearoot.set_sibling_total_weight(1)
        # x_idearoot.set_active_status(
        #     tree_traverse_count=self._tree_traverse_count,
        #     agenda_groups=self._groups,
        #     agenda_healer=self._healer,
        # )
        x_idearoot.set_agenda_importance(coin_onset_x=0, parent_coin_cease=1)
        x_idearoot.set_balanceheirs_agenda_credit_debt()
        x_idearoot.set_ancestor_promise_count(0, False)
        x_idearoot.clear_descendant_promise_count()
        x_idearoot.clear_all_party_credit_debt()
        x_idearoot.promise = False

        if x_idearoot.is_kidless():
            self._set_ancestor_metrics(road=self._idearoot._pad)
            self._distribute_agenda_importance(idea=self._idearoot)

    def _set_kids_attributes(
        self,
        idea_kid: IdeaCore,
        coin_onset: float,
        parent_coin_cease: float,
        parent_idea: IdeaCore,
    ):
        idea_kid.set_level(parent_level=parent_idea._level)
        idea_kid.set_pad(parent_idea._pad, parent_idea._label)
        idea_kid.set_acptfactheirs(acptfacts=parent_idea._acptfactheirs)
        idea_kid.set_requiredheirs(self._idea_dict, parent_idea._requiredheirs)
        idea_kid.set_assignedheir(parent_idea._assignedheir, self._groups)
        idea_kid.inherit_balanceheirs(parent_idea._balanceheirs)
        idea_kid.clear_balancelines()
        idea_kid.set_active_status(
            tree_traverse_count=self._tree_traverse_count,
            agenda_groups=self._groups,
            agenda_healer=self._healer,
        )
        idea_kid.set_sibling_total_weight(parent_idea._kids_total_weight)
        idea_kid.set_agenda_importance(
            coin_onset_x=coin_onset,
            parent_agenda_importance=parent_idea._agenda_importance,
            parent_coin_cease=parent_coin_cease,
        )
        idea_kid.set_ancestor_promise_count(
            parent_idea._ancestor_promise_count, parent_idea.promise
        )
        idea_kid.clear_descendant_promise_count()
        idea_kid.clear_all_party_credit_debt()

        if idea_kid.is_kidless():
            # set idea's ancestor metrics using agenda root as common reference
            self._set_ancestor_metrics(road=idea_kid.get_idea_road())
            self._distribute_agenda_importance(idea=idea_kid)

    def _distribute_agenda_importance(self, idea: IdeaCore):
        # TODO manage situations where balanceheir.creditor_weight is None for all balanceheirs
        # TODO manage situations where balanceheir.debtor_weight is None for all balanceheirs
        if idea.is_balanceheirless() == False:
            self._set_groupunits_agenda_importance(idea._balanceheirs)
        elif idea.is_balanceheirless():
            self._add_to_partyunits_agenda_credit_debt(idea._agenda_importance)

    def get_agenda_importance(
        self, parent_agenda_importance: float, weight: int, sibling_total_weight: int
    ) -> float:
        sibling_ratio = weight / sibling_total_weight
        return parent_agenda_importance * sibling_ratio

    def get_idea_list(self) -> list[IdeaCore]:
        self.set_agenda_metrics()
        return list(self._idea_dict.values())

    def set_agenda_metrics(self):
        self._rational = False
        self._tree_traverse_count = 0
        self._idea_dict = {self._idearoot.get_idea_road(): self._idearoot}

        while (
            not self._rational and self._tree_traverse_count < self._max_tree_traverse
        ):
            self._execute_tree_traverse()
            self._check_if_any_idea_active_status_has_changed()
            self._tree_traverse_count += 1
        self._after_all_tree_traverses_set_credit_debt()

    def _execute_tree_traverse(self):
        self._pre_tree_traverse_credit_debt_reset()
        self._set_root_attributes()

        coin_onset = self._idearoot._agenda_coin_onset
        parent_coin_cease = self._idearoot._agenda_coin_cease

        cache_idea_list = []
        for idea_kid in self._idearoot._kids.values():
            self._set_kids_attributes(
                idea_kid=idea_kid,
                coin_onset=coin_onset,
                parent_coin_cease=parent_coin_cease,
                parent_idea=self._idearoot,
            )
            cache_idea_list.append(idea_kid)
            coin_onset += idea_kid._agenda_importance

        # no function recursion, recursion by iterateing over list that can be added to by iterations
        while cache_idea_list != []:
            parent_idea = cache_idea_list.pop()
            if self._tree_traverse_count == 0:
                self._idea_dict[parent_idea.get_idea_road()] = parent_idea

            if parent_idea._kids != None:
                coin_onset = parent_idea._agenda_coin_onset
                parent_coin_cease = parent_idea._agenda_coin_cease
                for idea_kid in parent_idea._kids.values():
                    self._set_kids_attributes(
                        idea_kid=idea_kid,
                        coin_onset=coin_onset,
                        parent_coin_cease=parent_coin_cease,
                        parent_idea=parent_idea,
                    )
                    cache_idea_list.append(idea_kid)
                    coin_onset += idea_kid._agenda_importance

    def _check_if_any_idea_active_status_has_changed(self):
        any_idea_active_status_changed = False
        for idea in self._idea_dict.values():
            if idea._active_status_hx.get(self._tree_traverse_count) != None:
                any_idea_active_status_changed = True

        if any_idea_active_status_changed == False:
            self._rational = True

    def _after_all_tree_traverses_set_credit_debt(self):
        self._distribute_agenda_intent_importance()
        self._distribute_groups_agenda_importance()
        self._set_agenda_intent_ratio_credit_debt()

    def _pre_tree_traverse_credit_debt_reset(self):
        self._reset_groupunits_agenda_credit_debt()
        self._reset_groupunits_agenda_credit_debt()
        self._reset_partyunit_agenda_credit_debt()

    def get_heir_road_list(self, road_x: RoadUnit) -> list[RoadUnit]:
        # create list of all idea roads (road+desc)
        return [
            road
            for road in self.get_idea_tree_ordered_road_list()
            if road.find(road_x) == 0
        ]

    def get_idea_tree_ordered_road_list(
        self, no_range_descendants: bool = False
    ) -> list[RoadUnit]:
        idea_list = self.get_idea_list()
        node_dict = {
            idea.get_idea_road().lower(): idea.get_idea_road() for idea in idea_list
        }
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

    def get_acptfactunits_dict(self) -> dict[str:str]:
        x_dict = {}
        if self._idearoot._acptfactunits != None:
            for acptfact_road, acptfact_obj in self._idearoot._acptfactunits.items():
                x_dict[acptfact_road] = acptfact_obj.get_dict()
        return x_dict

    def get_partys_dict(self) -> dict[str:str]:
        x_dict = {}
        if self._partys != None:
            for party_pid, party_obj in self._partys.items():
                x_dict[party_pid] = party_obj.get_dict()
        return x_dict

    def get_groupunits_from_dict(self) -> dict[str:str]:
        x_dict = {}
        if self._groups != None:
            for group_pid, group_obj in self._groups.items():
                x_dict[group_pid] = group_obj.get_dict()
        return x_dict

    def get_dict(self) -> dict[str:str]:
        self.set_agenda_metrics()
        return {
            "_partys": self.get_partys_dict(),
            "_groups": self.get_groupunits_from_dict(),
            "_originunit": self._originunit.get_dict(),
            "_weight": self._weight,
            "_healer": self._healer,
            "_economy_id": self._economy_id,
            "_max_tree_traverse": self._max_tree_traverse,
            "_auto_output_to_public": self._auto_output_to_public,
            "_road_node_delimiter": self._road_node_delimiter,
            "_idearoot": self._idearoot.get_dict(),
        }

    def get_json(self) -> str:
        x_dict = self.get_dict()
        return x_get_json(dict_x=x_dict)

    def set_time_hreg_ideas(self, c400_count):
        x_hregidea = HregIdea(self._road_node_delimiter)
        ideabase_list = x_hregidea._get_time_hreg_src_idea(c400_count=c400_count)
        while len(ideabase_list) != 0:
            yb = ideabase_list.pop(0)
            range_source_road_x = None
            if yb.sr != None:
                range_source_road_x = self.make_road(self._economy_id, yb.sr)

            x_idea = ideacore_shop(
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
            road_x = self.make_road(self._economy_id, yb.rr)
            self.add_idea(x_idea, pad=road_x)

            numeric_road_x = None
            if yb.nr != None:
                numeric_road_x = self.make_road(self._economy_id, yb.nr)
                self.edit_idea_attr(
                    road=self.make_road(road_x, yb.n), numeric_road=numeric_road_x
                )
            if yb.a != None:
                self.edit_idea_attr(
                    road=self.make_road(road_x, yb.n),
                    addin=yb.a,
                    denom=yb.md,
                    numor=yb.mn,
                )

        self.set_agenda_metrics()

    def get_agenda4party(
        self, party_pid: PartyPID, acptfacts: dict[RoadUnit:AcptFactCore]
    ):
        self.set_agenda_metrics()
        agenda4party = agendaunit_shop(_healer=party_pid)
        agenda4party._idearoot._agenda_importance = self._idearoot._agenda_importance
        # get party's partys: partyzone

        # get partyzone groups
        party_groups = self.get_party_groupbrands(party_pid=party_pid)

        # set agenda4party by traversing the idea tree and selecting associated groups
        # set root
        not_included_agenda_importance = 0
        agenda4party._idearoot._kids = {}
        for ykx in self._idearoot._kids.values():
            y4a_included = any(
                group_ancestor.brand in party_groups
                for group_ancestor in ykx._balancelines.values()
            )

            if y4a_included:
                y4a_new = ideacore_shop(
                    _label=ykx._label,
                    _agenda_importance=ykx._agenda_importance,
                    _requiredunits=ykx._requiredunits,
                    _balancelinks=ykx._balancelinks,
                    _begin=ykx._begin,
                    _close=ykx._close,
                    promise=ykx.promise,
                    _task=ykx._task,
                )
                agenda4party._idearoot._kids[ykx._label] = y4a_new
            else:
                not_included_agenda_importance += ykx._agenda_importance

        if not_included_agenda_importance > 0:
            y4a_other = ideacore_shop(
                _label="__other__",
                _agenda_importance=not_included_agenda_importance,
            )
            agenda4party._idearoot._kids[y4a_other._label] = y4a_other

        return agenda4party

    def set_dominate_promise_idea(self, idea_kid: IdeaCore):
        idea_kid.promise = True
        self.add_idea(
            idea_kid=idea_kid,
            pad=self.make_road(idea_kid._pad),
            create_missing_ideas_groups=True,
        )

    def get_idea_list_without_idearoot(self) -> list[IdeaCore]:
        x_list = self.get_idea_list()
        x_list.pop(0)
        return x_list

    def meld(self, other_agenda, party_weight: float = None):
        self._meld_groups(other_agenda)
        self._meld_partys(other_agenda)
        self._meld_ideas(other_agenda, party_weight)
        self._meld_acptfacts(other_agenda)
        self._weight = get_meld_weight(
            src_weight=self._weight,
            src_on_meld_weight_action="default",
            other_weight=other_agenda._weight,
            other_on_meld_weight_action="default",
        )
        self._meld_originlinks(other_agenda._healer, party_weight)

    def _meld_ideas(self, other_agenda, party_weight: float):
        # meld idearoot
        self._idearoot.meld(other_idea=other_agenda._idearoot, _idearoot=True)

        # meld all other ideas
        party_pid = other_agenda._healer
        o_idea_list = other_agenda.get_idea_list_without_idearoot()
        for o_idea in o_idea_list:
            o_road = road_validate(
                self.make_road(o_idea._pad, o_idea._label),
                self._road_node_delimiter,
                self._economy_id,
            )
            try:
                main_idea = self.get_idea_kid(o_road)
                main_idea.meld(o_idea, False, party_pid, party_weight)
            except Exception:
                self.add_idea(idea_kid=o_idea, pad=o_idea._pad)
                main_idea = self.get_idea_kid(o_road)
                main_idea._originunit.set_originlink(party_pid, party_weight)

    def _meld_partys(self, other_agenda):
        for partyunit in other_agenda._partys.values():
            if self._partys.get(partyunit.pid) is None:
                self.set_partyunit(partyunit=partyunit)
            else:
                self._partys.get(partyunit.pid).meld(partyunit)

    def _meld_groups(self, other_agenda):
        for brx in other_agenda._groups.values():
            if self._groups.get(brx.brand) is None:
                self.set_groupunit(y_groupunit=brx)
            else:
                self._groups.get(brx.brand).meld(brx)

    def _meld_acptfacts(self, other_agenda):
        for hx in other_agenda._idearoot._acptfactunits.values():
            if self._idearoot._acptfactunits.get(hx.base) is None:
                self.set_acptfact(
                    base=hx.base, acptfact=hx.acptfact, open=hx.open, nigh=hx.nigh
                )
            else:
                self._idearoot._acptfactunits.get(hx.base).meld(hx)

    def _meld_originlinks(self, party_pid: PartyPID, party_weight: float):
        if party_pid != None:
            self._originunit.set_originlink(party_pid, party_weight)

    def get_assignment(
        self,
        agenda_x,
        assignor_partys: dict[PartyPID:PartyUnit],
        assignor_pid: PartyPID,
    ):
        self.set_agenda_metrics()
        self._set_assignment_partys(agenda_x, assignor_partys, assignor_pid)
        self._set_assignment_groups(agenda_x)
        assignor_promises = self._get_assignor_promise_ideas(agenda_x, assignor_pid)
        relevant_roads = self._get_relevant_roads(assignor_promises)
        self._set_assignment_ideas(agenda_x, relevant_roads)
        return agenda_x

    def _set_assignment_ideas(self, agenda_x, relevant_roads: dict[RoadUnit:str]):
        sorted_relevants = sorted(list(relevant_roads))
        # don't know how to manage root idea attributes...
        if sorted_relevants != []:
            root_road = sorted_relevants.pop(0)

        for relevant_road in sorted_relevants:
            relevant_idea = copy_deepcopy(self.get_idea_kid(relevant_road))
            # if relevant_roads.get(relevant_road) == "descendant":
            #     relevant_idea._requiredunits = {}
            #     relevant_idea._kids = {}
            #     agenda_x.add_idea(relevant_idea, pad=relevant_idea._pad)
            # elif relevant_roads.get(relevant_road) != "descendant":
            relevant_idea._kids = {}
            agenda_x.add_idea(relevant_idea, pad=relevant_idea._pad)

        for afu in self._idearoot._acptfactunits.values():
            if relevant_roads.get(afu.base):
                agenda_x.set_acptfact(
                    base=afu.base, pick=afu.pick, open=afu.open, nigh=afu.nigh
                )

    def _set_assignment_partys(
        self,
        agenda_x,
        assignor_partys: dict[PartyPID:PartyUnit],
        assignor_pid: PartyPID,
    ):
        if self._partys.get(assignor_pid) != None:
            # get all partys that are both in self._partys and assignor_known_partys
            partys_set = get_intersection_of_partys(self._partys, assignor_partys)
            for partypid_x in partys_set:
                agenda_x.set_partyunit(partyunit=self._partys.get(partypid_x))
        return agenda_x

    def _set_assignment_groups(self, agenda_x):
        revelant_groups = get_partys_relevant_groups(self._groups, agenda_x._partys)
        for group_pid, group_partys in revelant_groups.items():
            if agenda_x._groups.get(group_pid) is None:
                group_x = groupunit_shop(brand=group_pid)
                for party_pid in group_partys:
                    group_x.set_partylink(partylink_shop(pid=party_pid))
                agenda_x.set_groupunit(group_x)

    def _get_assignor_promise_ideas(
        self, agenda_x, assignor_pid: GroupBrand
    ) -> dict[RoadUnit:int]:
        assignor_groups = get_party_relevant_groups(agenda_x._groups, assignor_pid)
        return {
            idea_road: -1
            for idea_road, x_idea in self._idea_dict.items()
            if (x_idea.assignor_in(assignor_groups) and x_idea.promise)
        }

    def _set_auto_output_to_public(self, bool_x: bool):
        if bool_x is None and self._auto_output_to_public is None:
            self._auto_output_to_public = False
        elif bool_x is not None or not self._auto_output_to_public:
            self._auto_output_to_public = bool_x is not None and bool_x


def agendaunit_shop(
    _healer: PersonID = None,
    _economy_id: EconomyID = None,
    _weight: float = None,
    _auto_output_to_public: bool = None,
    _road_node_delimiter: str = None,
) -> AgendaUnit:
    if _weight is None:
        _weight = 1
    if _healer is None:
        _healer = ""
    if _auto_output_to_public is None:
        _auto_output_to_public = False
    if _economy_id is None:
        _economy_id = get_default_economy_root_label()

    x_agenda = AgendaUnit(
        _healer=_healer,
        _weight=_weight,
        _auto_output_to_public=_auto_output_to_public,
        _economy_id=_economy_id,
        _partys={},
        _groups={},
        _idea_dict={},
        _road_node_delimiter=get_node_delimiter(_road_node_delimiter),
    )
    x_agenda._idearoot = idearoot_shop(
        _label=x_agenda._economy_id,
        _uid=1,
        _level=0,
    )
    x_agenda._idearoot._road_node_delimiter = x_agenda._road_node_delimiter
    x_agenda.set_max_tree_traverse(3)
    x_agenda._rational = False
    x_agenda._originunit = originunit_shop()
    return x_agenda


def get_from_json(x_agenda_json: str) -> AgendaUnit:
    return get_from_dict(agenda_dict=json_loads(x_agenda_json))


def get_from_dict(agenda_dict: dict) -> AgendaUnit:
    x_agenda = agendaunit_shop()
    x_agenda.set_healer(get_obj_from_agenda_dict(agenda_dict, "_healer"))
    x_agenda._weight = get_obj_from_agenda_dict(agenda_dict, "_weight")
    x_agenda._auto_output_to_public = get_obj_from_agenda_dict(
        agenda_dict, "_auto_output_to_public"
    )
    x_agenda.set_max_tree_traverse(
        get_obj_from_agenda_dict(agenda_dict, "_max_tree_traverse")
    )
    x_agenda.set_economy_id(get_obj_from_agenda_dict(agenda_dict, "_economy_id"))
    x_agenda._road_node_delimiter = get_node_delimiter(
        get_obj_from_agenda_dict(agenda_dict, "_road_node_delimiter")
    )
    x_agenda._partys = get_obj_from_agenda_dict(agenda_dict, "_partys")
    x_agenda._groups = get_obj_from_agenda_dict(agenda_dict, "_groups")
    x_agenda._originunit = get_obj_from_agenda_dict(agenda_dict, "_originunit")

    set_idearoot_from_agenda_dict(x_agenda, agenda_dict)
    x_agenda.set_agenda_metrics()  # clean up tree traverse defined fields
    return x_agenda


def set_idearoot_from_agenda_dict(x_agenda: AgendaUnit, agenda_dict: dict):
    idearoot_dict = agenda_dict.get("_idearoot")
    x_agenda._idearoot = idearoot_shop(
        _label=x_agenda._economy_id,
        _uid=get_obj_from_idea_dict(idearoot_dict, "_uid"),
        _weight=get_obj_from_idea_dict(idearoot_dict, "_weight"),
        _begin=get_obj_from_idea_dict(idearoot_dict, "_begin"),
        _close=get_obj_from_idea_dict(idearoot_dict, "_close"),
        _numor=get_obj_from_idea_dict(idearoot_dict, "_numor"),
        _denom=get_obj_from_idea_dict(idearoot_dict, "_denom"),
        _reest=get_obj_from_idea_dict(idearoot_dict, "_reest"),
        _range_source_road=get_obj_from_idea_dict(idearoot_dict, "_range_source_road"),
        _numeric_road=get_obj_from_idea_dict(idearoot_dict, "_numeric_road"),
        _requiredunits=get_obj_from_idea_dict(idearoot_dict, "_requiredunits"),
        _assignedunit=get_obj_from_idea_dict(idearoot_dict, "_assignedunit"),
        _acptfactunits=get_obj_from_idea_dict(idearoot_dict, "_acptfactunits"),
        _balancelinks=get_obj_from_idea_dict(idearoot_dict, "_balancelinks"),
        _is_expanded=get_obj_from_idea_dict(idearoot_dict, "_is_expanded"),
        _road_node_delimiter=get_obj_from_idea_dict(
            idearoot_dict, "_road_node_delimiter"
        ),
    )
    set_idearoot_kids_from_dict(x_agenda, idearoot_dict)


def set_idearoot_kids_from_dict(x_agenda: AgendaUnit, idearoot_dict: dict):
    to_evaluate_idea_dicts = []
    pad_text = "pad"
    # for every kid dict, set pad in dict, add to to_evaluate_list
    for x_dict in get_obj_from_idea_dict(idearoot_dict, "_kids").values():
        x_dict[pad_text] = x_agenda._healer
        to_evaluate_idea_dicts.append(x_dict)

    while to_evaluate_idea_dicts != []:
        idea_dict = to_evaluate_idea_dicts.pop(0)
        # for every kid dict, set pad in dict, add to to_evaluate_list
        for kid_dict in get_obj_from_idea_dict(idea_dict, "_kids").values():
            pad_road = get_obj_from_idea_dict(idea_dict, pad_text)
            kid_label = get_obj_from_idea_dict(idea_dict, "_label")
            kid_dict[pad_text] = get_road(
                pad_road, kid_label, delimiter=x_agenda._road_node_delimiter
            )
            to_evaluate_idea_dicts.append(kid_dict)

        x_ideakid = ideacore_shop(
            _label=get_obj_from_idea_dict(idea_dict, "_label"),
            _weight=get_obj_from_idea_dict(idea_dict, "_weight"),
            _uid=get_obj_from_idea_dict(idea_dict, "_uid"),
            _begin=get_obj_from_idea_dict(idea_dict, "_begin"),
            _close=get_obj_from_idea_dict(idea_dict, "_close"),
            _numor=get_obj_from_idea_dict(idea_dict, "_numor"),
            _denom=get_obj_from_idea_dict(idea_dict, "_denom"),
            _reest=get_obj_from_idea_dict(idea_dict, "_reest"),
            promise=get_obj_from_idea_dict(idea_dict, "promise"),
            _requiredunits=get_obj_from_idea_dict(idea_dict, "_requiredunits"),
            _assignedunit=get_obj_from_idea_dict(idea_dict, "_assignedunit"),
            _originunit=get_obj_from_idea_dict(idea_dict, "_originunit"),
            _balancelinks=get_obj_from_idea_dict(idea_dict, "_balancelinks"),
            _acptfactunits=get_obj_from_idea_dict(idea_dict, "_acptfactunits"),
            _is_expanded=get_obj_from_idea_dict(idea_dict, "_is_expanded"),
            _range_source_road=get_obj_from_idea_dict(idea_dict, "_range_source_road"),
            _numeric_road=get_obj_from_idea_dict(idea_dict, "_numeric_road"),
        )
        # add idea with created pad
        x_agenda.add_idea(x_ideakid, pad=idea_dict[pad_text])


def get_obj_from_agenda_dict(x_dict: dict[str:], dict_key: str) -> any:
    if dict_key == "_originunit":
        return (
            originunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else originunit_shop()
        )
    elif dict_key == "_partys":
        return (
            partyunits_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else partyunits_get_from_dict(x_dict[dict_key])
        )
    elif dict_key == "_groups":
        return (
            groupunits_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else groupunits_get_from_dict(x_dict[dict_key])
        )
    elif dict_key == "_max_tree_traverse":
        return x_dict[dict_key] if x_dict.get(dict_key) != None else 20
    elif dict_key == "_auto_output_to_public":
        return x_dict[dict_key] if x_dict.get(dict_key) != None else False
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None


def get_dict_of_agenda_from_dict(x_dict: dict[str:dict]) -> dict[str:AgendaUnit]:
    agendaunits = {}
    for agendaunit_dict in x_dict.values():
        x_agenda = get_from_dict(agenda_dict=agendaunit_dict)
        agendaunits[x_agenda._healer] = x_agenda
    return agendaunits


@dataclass
class MeldeeOrderUnit:
    healer: PersonID
    voice_rank: int
    voice_hx_lowest_rank: int
    file_name: str


def get_meldeeorderunit(
    primary_agenda: AgendaUnit, meldee_file_name: str
) -> MeldeeOrderUnit:
    file_src_healer = meldee_file_name.replace(".json", "")
    primary_meldee_partyunit = primary_agenda.get_party(file_src_healer)

    default_voice_rank = 0
    default_voice_hx_lowest_rank = 0
    if primary_meldee_partyunit is None:
        primary_voice_rank_for_meldee = default_voice_rank
        primary_voice_hx_lowest_rank_for_meldee = default_voice_hx_lowest_rank
    else:
        primary_voice_rank_for_meldee = primary_meldee_partyunit._treasury_voice_rank
        primary_voice_hx_lowest_rank_for_meldee = (
            primary_meldee_partyunit._treasury_voice_hx_lowest_rank
        )
        if primary_voice_rank_for_meldee is None:
            primary_voice_rank_for_meldee = default_voice_rank
            primary_voice_hx_lowest_rank_for_meldee = default_voice_hx_lowest_rank

    return MeldeeOrderUnit(
        healer=file_src_healer,
        voice_rank=primary_voice_rank_for_meldee,
        voice_hx_lowest_rank=primary_voice_hx_lowest_rank_for_meldee,
        file_name=meldee_file_name,
    )


def get_file_names_in_voice_rank_order(primary_agenda, meldees_dir) -> list[str]:
    agenda_voice_ranks = {}
    for meldee_file_name in x_func_dir_files(dir_path=meldees_dir):
        meldee_orderunit = get_meldeeorderunit(primary_agenda, meldee_file_name)
        agenda_voice_ranks[meldee_orderunit.healer] = meldee_orderunit
    agendas_voice_rank_ordered_list = list(agenda_voice_ranks.values())
    agendas_voice_rank_ordered_list.sort(
        key=lambda x: (x.voice_rank * -1, x.voice_hx_lowest_rank * -1, x.healer)
    )
    return [
        x_meldeeorderunit.file_name
        for x_meldeeorderunit in agendas_voice_rank_ordered_list
    ]


def get_meld_of_agenda_files(
    primary_agenda: AgendaUnit, meldees_dir: str
) -> AgendaUnit:
    for x_filename in get_file_names_in_voice_rank_order(primary_agenda, meldees_dir):
        primary_agenda.meld(get_from_json(x_func_open_file(meldees_dir, x_filename)))
    primary_agenda.set_agenda_metrics()
    return primary_agenda


def get_intersection_of_partys(
    partys_x: dict[PartyPID:PartyUnit], partys_y: dict[PartyPID:PartyUnit]
) -> dict[PartyPID:-1]:
    x_set = set(partys_x)
    y_set = set(partys_y)
    intersection_x = x_set.intersection(y_set)
    return {partypid_x: -1 for partypid_x in intersection_x}


def get_partys_relevant_groups(
    groups_x: dict[GroupBrand:GroupUnit], partys_x: dict[PartyPID:PartyUnit]
) -> dict[GroupBrand:{PartyPID: -1}]:
    relevant_groups = {}
    for partypid_x in partys_x:
        for group_x in groups_x.values():
            if group_x._partys.get(partypid_x) != None:
                if relevant_groups.get(group_x.brand) is None:
                    relevant_groups[group_x.brand] = {}
                relevant_groups.get(group_x.brand)[partypid_x] = -1

    return relevant_groups


def get_party_relevant_groups(
    groups_x: dict[GroupBrand:GroupUnit], partypid_x: PartyPID
) -> dict[GroupBrand:-1]:
    return {
        group_x.brand: -1
        for group_x in groups_x.values()
        if group_x._partys.get(partypid_x) != None
    }
