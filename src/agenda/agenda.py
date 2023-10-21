import dataclasses
import json
from datetime import datetime
from src.agenda.party import (
    PersonName,
    PartyTitle,
    PartyUnit,
    PartyLink,
    partyunits_get_from_dict,
    partyunit_shop,
    partylink_shop,
    PartyUnitExternalMetrics,
)
from src.agenda.group import (
    Balancelink,
    GroupBrand,
    GroupUnit,
    balancelinks_get_from_dict,
    get_from_dict as groupunits_get_from_dict,
    groupunit_shop,
    balancelink_shop,
)
from src.agenda.required_idea import (
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
from src.agenda.required_assign import (
    assigned_heir_shop,
    assigned_unit_shop,
    AssignedUnit,
    AssignedHeir,
    assignedunit_get_from_dict,
)
from src.agenda.tree_metrics import TreeMetrics
from src.agenda.x_func import x_get_json
from src.agenda.idea import (
    IdeaCore,
    ideacore_shop,
    IdeaRoot,
    idearoot_shop,
    IdeaAttrHolder,
)
from src.agenda.hreg_time import (
    _get_time_hreg_src_idea,
    get_time_min_from_dt as hreg_get_time_min_from_dt,
    convert1440toReadableTime,
    get_number_with_letter_ending,
    get_jajatime_legible_from_dt,
)
from src.agenda.lemma import Lemmas
from src.agenda.road import (
    get_pad_from_road,
    is_sub_road,
    road_validate,
    change_road,
    get_terminus_node_from_road,
    find_replace_road_key_dict,
    get_ancestor_roads,
    get_default_culture_root_label as root_label,
    get_road_from_nodes,
    get_all_road_nodes,
    get_forefather_roads,
)
from src.agenda.origin import originunit_get_from_dict, originunit_shop, OriginUnit
from copy import deepcopy as copy_deepcopy
from src.agenda.x_func import (
    save_file as x_func_save_file,
    dir_files as x_func_dir_files,
    open_file as x_func_open_file,
    get_meld_weight,
)


class InvalidDealException(Exception):
    pass


class AssignmentPartyException(Exception):
    pass


@dataclasses.dataclass
class DealUnit:
    _healer: PersonName = None
    _weight: float = None
    _partys: dict[PartyTitle:PartyUnit] = None
    _groups: dict[GroupBrand:GroupUnit] = None
    _idearoot: IdeaRoot = None
    _idea_dict: dict[Road:IdeaCore] = None
    _max_tree_traverse: int = None
    _tree_traverse_count: int = None
    _rational: bool = None
    _originunit: OriginUnit = None
    _culture_handle: str = None
    _auto_output_to_public: bool = None

    def set_partys_output_agenda_meld_order(self):
        sort_partys_list = list(self._partys.values())
        sort_partys_list.sort(key=lambda x: x.title.lower(), reverse=False)
        for count_x, x_partyunit in enumerate(sort_partys_list):
            x_partyunit.set_output_agenda_meld_order(count_x)

    def clear_partys_output_agenda_meld_order(self):
        for x_partyunit in self._partys.values():
            x_partyunit.clear_output_agenda_meld_order()

    def set_culture_handle(self, culture_handle: str):
        old_culture_handle = copy_deepcopy(self._culture_handle)
        self._culture_handle = culture_handle
        self.edit_idea_label(
            old_road=old_culture_handle, new_label=self._culture_handle
        )
        self.set_agenda_metrics()

    def set_banking_attr_partyunits(self, river_tallys: dict[str:]):
        for partyunit_x in self._partys.values():
            partyunit_x.clear_banking_data()
            river_tally = river_tallys.get(partyunit_x.title)
            if river_tally != None:
                partyunit_x.set_banking_data(
                    tax_paid=river_tally.tax_total,
                    tax_diff=river_tally.tax_diff,
                    credit_score=river_tally.credit_score,
                    voice_rank=river_tally.voice_rank,
                )

    def import_external_partyunit_metrics(
        self, external_metrics: PartyUnitExternalMetrics
    ):
        party_x = self._partys.get(external_metrics.internal_title)
        party_x._creditor_active = external_metrics.creditor_active
        party_x._debtor_active = external_metrics.debtor_active
        # self.set_partyunit(partyunit=party_x)

    def set_max_tree_traverse(self, int_x: int):
        if int_x < 2:
            raise InvalidDealException(
                f"set_max_tree_traverse: input '{int_x}' must be number that is 2 or greater"
            )
        else:
            self._max_tree_traverse = int_x

    def get_agenda_sprung_from_single_idea(self, road: Road):
        self.set_agenda_metrics()
        idea_x = self.get_idea_kid(road=road)
        new_weight = self._weight * idea_x._agenda_importance
        cx = DealUnit(_healer=self._idearoot._label, _weight=new_weight)

        for road_assc in sorted(list(self._get_relevant_roads({road}))):
            src_yx = self.get_idea_kid(road=road_assc)
            new_yx = copy_deepcopy(src_yx)
            if new_yx._pad != "":
                cx.add_idea(idea_kid=new_yx, pad=new_yx._pad)
            cx.set_agenda_metrics()

        # TODO grab groups
        # TODO grab all group partys
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

    def _are_all_partys_groups_are_in_idea_kid(self, road: Road) -> bool:
        idea_kid = self.get_idea_kid(road=road)
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
        for balanceheir_title in balanceheir_dict:
            groupunit = self._groups.get(balanceheir_title)
            for partylink in groupunit._partys.values():
                balanceheir_partyunits[partylink.title] = self._partys.get(
                    partylink.title
                )

        # check all agenda._partys are in balanceheir_partyunits
        return len(self._partys) == len(balanceheir_partyunits)

    def get_time_min_from_dt(self, dt: datetime) -> float:
        return hreg_get_time_min_from_dt(dt=dt)

    def get_time_c400_from_min(self, min: int) -> int:
        c400_idea = self.get_idea_kid(
            f"{self._culture_handle},time,tech,400 year cycle"
        )
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
            yr4_1461 = self.get_idea_kid(
                f"{self._culture_handle},time,tech,4year with leap"
            )
            yr4_cycles = int(cXXXyr_min / yr4_1461._close)
            cXyr_min = cXXXyr_min % yr4_1461._close
            yr1_idea = yr4_1461.get_kids_in_range(begin=cXyr_min, close=cXyr_min)[0]
        elif c100_4_96y._close - c100_4_96y._begin == 2102400:
            yr4_1460 = self.get_idea_kid(
                f"{self._culture_handle},time,tech,4year wo leap"
            )
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
            yrx = self.get_idea_kid(f"{self._culture_handle},time,tech,365 year")
        elif yr1_idea._close - yr1_idea._begin == 527040:
            yrx = self.get_idea_kid(f"{self._culture_handle},time,tech,366 year")
        mon_x = yrx.get_kids_in_range(begin=yr1_idea_rem_min, close=yr1_idea_rem_min)[0]
        month_rem_min = yr1_idea_rem_min - mon_x._begin
        month_num = int(mon_x._label.split("-")[0])
        day_x = self.get_idea_kid(f"{self._culture_handle},time,tech,day")
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
            # str_x = f"Weekday, monthtitle monthday year"
        elif divisor != None and divisor % 10080 == 0:
            str_x = self._get_jajatime_week_legible_text(open, divisor)
        elif divisor != None and divisor % 1440 == 0:
            if divisor == 1440:
                str_x = f"every day at {convert1440toReadableTime(min1440=open)}"
            else:
                num_days = int(divisor / 1440)
                num_with_letter_ending = get_number_with_letter_ending(num=num_days)
                str_x = f"every {num_with_letter_ending} day at {convert1440toReadableTime(min1440=open)}"
        else:
            str_x = "unknown"

        return str_x

    def _get_jajatime_week_legible_text(self, open: int, divisor: int) -> str:
        open_in_week = open % divisor
        week_road = f"{self._culture_handle},time,tech,week"
        weekday_ideas_dict = self.get_idea_ranged_kids(
            idea_road=week_road, begin=open_in_week
        )
        weekday_idea_node = None
        for idea in weekday_ideas_dict.values():
            weekday_idea_node = idea

        if divisor == 10080:
            return f"every {weekday_idea_node._label} at {convert1440toReadableTime(min1440=open % 1440)}"
        num_with_letter_ending = get_number_with_letter_ending(num=divisor // 10080)
        return f"every {num_with_letter_ending} {weekday_idea_node._label} at {convert1440toReadableTime(min1440=open % 1440)}"

    def get_partys_metrics(self):
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.balancelinks_metrics

    def set_partys_empty_if_null(self):
        if self._partys is None:
            self._partys = {}

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

    def add_to_group_agenda_goal_credit_debt(
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
                group._agenda_goal_credit += balanceline_agenda_credit
                group._agenda_goal_debt += balanceline_agenda_debt

    def add_to_partyunit_agenda_credit_debt(
        self,
        partyunit_title: PartyTitle,
        agenda_credit,
        agenda_debt: float,
        agenda_goal_credit: float,
        agenda_goal_debt: float,
    ):
        for partyunit in self._partys.values():
            if partyunit.title == partyunit_title:
                partyunit.add_agenda_credit_debt(
                    agenda_credit=agenda_credit,
                    agenda_debt=agenda_debt,
                    agenda_goal_credit=agenda_goal_credit,
                    agenda_goal_debt=agenda_goal_debt,
                )

    def set_groupunits_empty_if_null(self):
        if self._groups is None:
            self._groups = {}

    def del_partyunit(self, title: str):
        self._groups.pop(title)
        self._partys.pop(title)

    def add_partyunit(
        self,
        title: str,
        uid: int = None,
        creditor_weight: int = None,
        debtor_weight: int = None,
        depotlink_type: str = None,
    ):
        partyunit = partyunit_shop(
            title=PartyTitle(title),
            uid=uid,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
            depotlink_type=depotlink_type,
        )
        self.set_partyunit(partyunit=partyunit)

    def set_partyunit(self, partyunit: PartyUnit):
        self.set_partys_empty_if_null()
        self.set_groupunits_empty_if_null()
        # future: if party is new check existance of group with party title

        self._partys[partyunit.title] = partyunit

        existing_group = None
        try:
            existing_group = self._groups[partyunit.title]
        except KeyError:
            partylink = partylink_shop(
                title=PartyTitle(partyunit.title), creditor_weight=1, debtor_weight=1
            )
            partylinks = {partylink.title: partylink}
            group_unit = groupunit_shop(
                brand=partyunit.title,
                _single_party=True,
                _partys=partylinks,
                uid=None,
                single_party_id=None,
            )
            self.set_groupunit(groupunit=group_unit)

    def edit_partyunit_title(
        self,
        old_title: str,
        new_title: str,
        allow_party_overwite: bool,
        allow_nonsingle_group_overwrite: bool,
    ):
        old_title_creditor_weight = self._partys.get(old_title).creditor_weight
        if not allow_party_overwite and self._partys.get(new_title) != None:
            raise InvalidDealException(
                f"Party '{old_title}' change to '{new_title}' failed since '{new_title}' exists."
            )
        elif (
            not allow_nonsingle_group_overwrite
            and self._groups.get(new_title) != None
            and self._groups.get(new_title)._single_party == False
        ):
            raise InvalidDealException(
                f"Party '{old_title}' change to '{new_title}' failed since non-single group '{new_title}' exists."
            )
        elif (
            allow_nonsingle_group_overwrite
            and self._groups.get(new_title) != None
            and self._groups.get(new_title)._single_party == False
        ):
            self.del_groupunit(groupbrand=new_title)
        elif self._partys.get(new_title) != None:
            old_title_creditor_weight += self._partys.get(new_title).creditor_weight

        self.add_partyunit(title=new_title, creditor_weight=old_title_creditor_weight)
        groups_affected_list = []
        for group in self._groups.values():
            groups_affected_list.extend(
                group.brand
                for party_x in group._partys.values()
                if party_x.title == old_title
            )
        for group_x in groups_affected_list:
            partylink_creditor_weight = (
                self._groups.get(group_x)._partys.get(old_title).creditor_weight
            )
            partylink_debtor_weight = (
                self._groups.get(group_x)._partys.get(old_title).debtor_weight
            )
            if self._groups.get(group_x)._partys.get(new_title) != None:
                partylink_creditor_weight += (
                    self._groups.get(group_x)._partys.get(new_title).creditor_weight
                )
                partylink_debtor_weight += (
                    self._groups.get(group_x)._partys.get(new_title).debtor_weight
                )

            self._groups.get(group_x).set_partylink(
                partylink=partylink_shop(
                    title=new_title,
                    creditor_weight=partylink_creditor_weight,
                    debtor_weight=partylink_debtor_weight,
                )
            )
            self._groups.get(group_x).del_partylink(title=old_title)

        self.del_partyunit(title=old_title)

    def get_party(self, partytitle: PartyTitle) -> PartyUnit:
        return self._partys.get(partytitle)

    def get_partyunits_title_list(self):
        partytitle_list = list(self._partys.keys())
        partytitle_list.append("")
        partytitle_dict = {
            partytitle.lower(): partytitle for partytitle in partytitle_list
        }
        partytitle_lowercase_ordered_list = sorted(list(partytitle_dict))
        return [
            partytitle_dict[partytitle_l]
            for partytitle_l in partytitle_lowercase_ordered_list
        ]

    def get_partyunits_uid_max(self) -> int:
        uid_max = 1
        for partyunit_x in self._partys.values():
            if partyunit_x.uid != None and partyunit_x.uid > uid_max:
                uid_max = partyunit_x.uid
        return uid_max

    def get_partyunits_uid_dict(self) -> dict[int:int]:
        uid_dict = {}
        for partyunit_x in self._partys.values():
            if uid_dict.get(partyunit_x.uid) is None:
                uid_dict[partyunit_x.uid] = 1
            else:
                uid_dict[partyunit_x.uid] += 1
        return uid_dict

    def set_all_partyunits_uids_unique(self) -> int:
        uid_max = self.get_partyunits_uid_max()
        uid_dict = self.get_partyunits_uid_dict()
        for partyunit_x in self._partys.values():
            if uid_dict.get(partyunit_x.uid) > 0:
                new_uid_max = uid_max + 1
                partyunit_x.uid = new_uid_max
                uid_max = partyunit_x.uid

    def all_partyunits_uids_are_unique(self):
        uid_dict = self.get_partyunits_uid_dict()
        return not any(
            uid_count > 1 or uid is None for uid, uid_count in uid_dict.items()
        )

    def get_partys_depotlink_count(self):
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

    def set_groupunit(self, groupunit: GroupUnit, create_missing_partys: bool = None):
        self.set_groupunits_empty_if_null()
        groupunit._set_partylinks_empty_if_null()
        self._groups[groupunit.brand] = groupunit

        if create_missing_partys:
            self._create_missing_partys(partylinks=groupunit._partys)

    def _create_missing_partys(self, partylinks: dict[PartyTitle:PartyLink]):
        for partylink_x in partylinks.values():
            if self._partys.get(partylink_x.title) is None:
                self.set_partyunit(
                    partyunit=partyunit_shop(
                        title=partylink_x.title,
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
            raise InvalidDealException(
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
            self.set_groupunit(groupunit=groupunit_x)
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
        for idea_x in self.get_idea_list():
            if (
                idea_x._balancelinks.get(new_brand) != None
                and idea_x._balancelinks.get(old_brand) != None
            ):
                old_balancelink = idea_x._balancelinks.get(old_brand)
                old_balancelink.brand = new_brand
                idea_x._balancelinks.get(new_brand).meld(
                    other_balancelink=old_balancelink,
                    other_on_meld_weight_action="sum",
                    src_on_meld_weight_action="sum",
                )

                idea_x.del_balancelink(groupbrand=old_brand)
            elif (
                idea_x._balancelinks.get(new_brand) is None
                and idea_x._balancelinks.get(old_brand) != None
            ):
                old_balancelink = idea_x._balancelinks.get(old_brand)
                new_balancelink = balancelink_shop(
                    brand=new_brand,
                    creditor_weight=old_balancelink.creditor_weight,
                    debtor_weight=old_balancelink.debtor_weight,
                )
                idea_x.set_balancelink(balancelink=new_balancelink)
                idea_x.del_balancelink(groupbrand=old_brand)

    def get_groupunits_brand_list(self):
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
        minutes_acptfact = f"{self._culture_handle},time,jajatime"
        self.set_acptfact(
            base=minutes_acptfact,
            pick=minutes_acptfact,
            open=open_minutes,
            nigh=nigh_minutes,
        )

    def _is_idea_rangeroot(self, idea_road: Road) -> bool:
        anc_roads = get_ancestor_roads(road=idea_road)
        parent_road = self._culture_handle if len(anc_roads) == 1 else anc_roads[1]

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

        # Now get associates (all their descendants and range_source_roads)
        lemma_acptfactunits = {}  # acptfact.base : acptfactUnit
        count_x = 0
        while lemmas_x.is_lemmas_evaluated() == False or count_x > 10000:
            count_x += 1
            if count_x == 9998:
                raise InvalidDealException("lemma loop failed")

            lemma_y = lemmas_x.get_unevaluated_lemma()
            idea_x = lemma_y.idea_x
            acptfact_x = lemma_y.calc_acptfact

            road_x = f"{idea_x._pad},{idea_x._label}"
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
            raise InvalidDealException(
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

        self.set_agenda_metrics()

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
            balancelinks=self._idearoot._balancelinks,
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
            balancelinks=idea_kid._balancelinks,
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
        pad: Road,
        create_missing_ideas_groups: bool = None,
        adoptees: list[str] = None,
        bundling=True,
    ):
        if adoptees != None:
            for adoptee_label in adoptees:
                adoptee_road = f"{pad},{adoptee_label}"
                adoptee_idea = self.get_idea_kid(road=adoptee_road)

        if not create_missing_ideas_groups:
            idea_kid = self._get_filtered_balancelinks_idea(idea_kid)

        pad = road_validate(pad)
        temp_idea = self._idearoot
        pad_nodes = get_all_road_nodes(pad)
        temp_road = pad_nodes.pop(0)

        # idearoot cannot be replaced
        if temp_road == self._culture_handle and pad_nodes == []:
            idea_kid.set_pad(parent_road=Road(self._culture_handle))
        else:
            road_nodes = [temp_road]
            while pad_nodes != []:
                temp_road = pad_nodes.pop(0)
                temp_idea = self._get_or_create_leveln_idea(
                    parent_idea=temp_idea, idea_label=temp_road
                )
                road_nodes.append(temp_road)

            idea_kid.set_pad(parent_road=get_road_from_nodes(road_nodes))

        temp_idea.add_kid(idea_kid)

        if adoptees != None:
            weight_sum = 0
            for adoptee_label in adoptees:
                adoptee_road = f"{pad},{adoptee_label}"
                adoptee_idea = self.get_idea_kid(road=adoptee_road)
                weight_sum += adoptee_idea._weight
                new_adoptee_pad = f"{pad},{idea_kid._label},{adoptee_label}"
                self.add_idea(adoptee_idea, new_adoptee_pad)
                self.edit_idea_attr(road=new_adoptee_pad, weight=adoptee_idea._weight)
                self.del_idea_kid(adoptee_road)

            if bundling:
                self.edit_idea_attr(road=f"{pad},{idea_kid._label}", weight=weight_sum)

        if create_missing_ideas_groups:
            self._create_missing_ideas(road=Road(f"{pad},{idea_kid._label}"))
            self._create_missing_groups_partys(balancelinks=idea_kid._balancelinks)

    def _get_filtered_balancelinks_idea(self, idea: IdeaCore) -> IdeaCore:
        idea.set_balancelink_empty_if_null()
        _balancelinks_to_delete = [
            _balancelink_title
            for _balancelink_title in idea._balancelinks.keys()
            if self._groups.get(_balancelink_title) is None
        ]
        for _balancelink_title in _balancelinks_to_delete:
            idea._balancelinks.pop(_balancelink_title)

        if idea._assignedunit != None:
            _suffgroups_to_delete = [
                _suffgroup_title
                for _suffgroup_title in idea._assignedunit._suffgroups.keys()
                if self._groups.get(_suffgroup_title) is None
            ]
            for _suffgroup_title in _suffgroups_to_delete:
                idea._assignedunit.del_suffgroup(_suffgroup_title)

        return idea

    def _create_missing_groups_partys(self, balancelinks: dict[GroupBrand:Balancelink]):
        for balancelink_x in balancelinks.values():
            if self._groups.get(balancelink_x.brand) is None:
                groupunit_x = groupunit_shop(brand=balancelink_x.brand, _partys={})
                self.set_groupunit(groupunit=groupunit_x)

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

    def _set_ideakid_if_empty(self, road: Road):
        try:
            self.get_idea_kid(road)
        except InvalidDealException:
            base_idea = ideacore_shop(
                _label=get_terminus_node_from_road(road=road),
                _pad=get_pad_from_road(road=road),
            )
            self.add_idea(idea_kid=base_idea, pad=base_idea._pad)

    # def _get_or_create_level1_idea(self, idea_label: str) -> IdeaCore:
    #     return_idea = None
    #     try:
    #         return_idea = self._kids[idea_label]
    #     except Exception:
    #         KeyError
    #         self.add_kid(ideacore_shop(_label=idea_label))
    #         return_idea = self._kids[idea_label]

    #     return return_idea

    def _get_or_create_leveln_idea(self, parent_idea: IdeaCore, idea_label: str):
        return_idea = None
        try:
            return_idea = parent_idea._kids[idea_label]
        except Exception:
            KeyError
            parent_idea.add_kid(ideacore_shop(_label=idea_label))
            return_idea = parent_idea._kids[idea_label]

        return return_idea

    def del_idea_kid(self, road: Road, del_children: bool = True):
        x_road = get_all_road_nodes(road)
        temp_label = x_road.pop(0)
        temps_d = [temp_label]

        if x_road == []:
            raise InvalidDealException("Object cannot delete itself")
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
        d_temp_idea = self.get_idea_kid(road=get_road_from_nodes(road_nodes))
        for kid in d_temp_idea._kids.values():
            self.add_idea(idea_kid=kid, pad=get_road_from_nodes(road_nodes[:-1]))

    def set_healer(self, new_healer):
        self._healer = new_healer

    def edit_idea_label(
        self,
        old_road: Road,
        new_label: str,
    ):
        # check idea exists
        if self.get_idea_kid(road=old_road) is None:
            raise InvalidDealException(f"Idea {old_road=} does not exist")

        pad = get_pad_from_road(road=old_road)
        new_road = Road(f"{new_label}") if pad == "" else Road(f"{pad},{new_label}")
        if old_road != new_road:
            # if root _label is changed
            if pad == "":
                self._idearoot.set_idea_label(
                    new_label, agenda_culture_handle=self._culture_handle
                )
                self._idearoot._pad = pad
            else:
                self._non_root_idea_label_edit(old_road, new_label, pad)
            self._idearoot_find_replace_road(old_road=old_road, new_road=new_road)
            self._set_acptfacts_empty_if_null()
            self._idearoot._acptfactunits = find_replace_road_key_dict(
                dict_x=self._idearoot._acptfactunits,
                old_road=old_road,
                new_road=new_road,
            )

    def _non_root_idea_label_edit(self, old_road, new_label, pad):
        idea_z = self.get_idea_kid(road=old_road)
        idea_z.set_idea_label(new_label)
        idea_z._pad = pad
        idea_parent = self.get_idea_kid(road=get_pad_from_road(old_road))
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
                        ref_road=idea_kid._pad,
                        sub_road=old_road,
                    ):
                        idea_kid._pad = change_road(
                            current_road=idea_kid._pad,
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
            raise InvalidDealException("Root Idea cannot have numor denom reest.")
        parent_road = self._culture_handle if len(anc_roads) == 1 else anc_roads[1]

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
            raise InvalidDealException(
                "Idea has begin-close range parent, cannot have numeric_road"
            )
        elif not parent_has_range and not numeric_range and numor != None:
            raise InvalidDealException(
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
        all_party_credit: bool = None,
        all_party_debt: bool = None,
        balancelink: Balancelink = None,
        balancelink_del: GroupBrand = None,
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
            all_party_credit=all_party_credit,
            all_party_debt=all_party_debt,
            balancelink=balancelink,
            balancelink_del=balancelink_del,
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

        # deleting a balancelink reqquires a tree traverse to correctly set balanceheirs and balancelines
        if balancelink_del != None or balancelink != None:
            self.set_agenda_metrics()

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

    def get_goal_items(
        self, base: Road = None, goal_enterprise: bool = True, goal_state: bool = True
    ) -> list[IdeaCore]:
        return [idea for idea in self.get_idea_list() if idea.is_goal_item(base_x=base)]

    def set_goal_task_complete(self, task_road: Road, base: Road):
        promise_item = self.get_idea_kid(road=task_road)
        promise_item.set_acptfactunit_to_complete(
            base_acptfactunit=self._idearoot._acptfactunits[base]
        )

    def get_partyunit_total_creditor_weight(self):
        return sum(
            partyunit.get_creditor_weight() for partyunit in self._partys.values()
        )

    def get_partyunit_total_debtor_weight(self):
        return sum(partyunit.get_debtor_weight() for partyunit in self._partys.values())

    def _add_to_partyunits_agenda_credit_debt(self, idea_agenda_importance: float):
        sum_partyunit_creditor_weight = self.get_partyunit_total_creditor_weight()
        sum_partyunit_debtor_weight = self.get_partyunit_total_debtor_weight()

        for partyunit_x in self._partys.values():
            au_agenda_credit = (
                idea_agenda_importance * partyunit_x.get_creditor_weight()
            ) / sum_partyunit_creditor_weight

            au_agenda_debt = (
                idea_agenda_importance * partyunit_x.get_debtor_weight()
            ) / sum_partyunit_debtor_weight

            partyunit_x.add_agenda_credit_debt(
                agenda_credit=au_agenda_credit,
                agenda_debt=au_agenda_debt,
                agenda_goal_credit=0,
                agenda_goal_debt=0,
            )

    def _add_to_partyunits_agenda_goal_credit_debt(self, idea_agenda_importance: float):
        sum_partyunit_creditor_weight = self.get_partyunit_total_creditor_weight()
        sum_partyunit_debtor_weight = self.get_partyunit_total_debtor_weight()

        for partyunit_x in self._partys.values():
            au_agenda_goal_credit = (
                idea_agenda_importance * partyunit_x.get_creditor_weight()
            ) / sum_partyunit_creditor_weight

            au_agenda_goal_debt = (
                idea_agenda_importance * partyunit_x.get_debtor_weight()
            ) / sum_partyunit_debtor_weight

            partyunit_x.add_agenda_credit_debt(
                agenda_credit=0,
                agenda_debt=0,
                agenda_goal_credit=au_agenda_goal_credit,
                agenda_goal_debt=au_agenda_goal_debt,
            )

    def _set_partyunits_agenda_goal_importance(self, agenda_goal_importance: float):
        sum_partyunit_creditor_weight = self.get_partyunit_total_creditor_weight()
        sum_partyunit_debtor_weight = self.get_partyunit_total_debtor_weight()

        for partyunit_x in self._partys.values():
            au_agenda_goal_credit = (
                agenda_goal_importance * partyunit_x.get_creditor_weight()
            ) / sum_partyunit_creditor_weight

            au_agenda_goal_debt = (
                agenda_goal_importance * partyunit_x.get_debtor_weight()
            ) / sum_partyunit_debtor_weight

            partyunit_x.add_agenda_goal_credit_debt(
                agenda_goal_credit=au_agenda_goal_credit,
                agenda_goal_debt=au_agenda_goal_debt,
            )

    def _reset_groupunits_agenda_credit_debt(self):
        self.set_groupunits_empty_if_null()
        for balancelink_obj in self._groups.values():
            balancelink_obj.reset_agenda_credit_debt()

    def _set_groupunits_agenda_importance(
        self, balanceheirs: dict[GroupBrand:Balancelink]
    ):
        self.set_groupunits_empty_if_null()
        for balancelink_obj in balanceheirs.values():
            self.add_to_group_agenda_credit_debt(
                groupbrand=balancelink_obj.brand,
                balanceheir_agenda_credit=balancelink_obj._agenda_credit,
                balanceheir_agenda_debt=balancelink_obj._agenda_debt,
            )

    def _distribute_agenda_goal_importance(self):
        for idea in self._idea_dict.values():
            # If there are no balancelines associated with idea
            # distribute agenda_importance via general partyunit
            # credit ratio and debt ratio
            # if idea.is_goal_item() and idea._balancelines == {}:
            if idea.is_goal_item():
                if idea._balancelines == {}:
                    self._add_to_partyunits_agenda_goal_credit_debt(
                        idea._agenda_importance
                    )
                else:
                    for balanceline_x in idea._balancelines.values():
                        self.add_to_group_agenda_goal_credit_debt(
                            groupbrand=balanceline_x.brand,
                            balanceline_agenda_credit=balanceline_x._agenda_credit,
                            balanceline_agenda_debt=balanceline_x._agenda_debt,
                        )

    def _distribute_groups_agenda_importance(self):
        for group_obj in self._groups.values():
            group_obj._set_partylink_agenda_credit_debt()
            for partylink in group_obj._partys.values():
                self.add_to_partyunit_agenda_credit_debt(
                    partyunit_title=partylink.title,
                    agenda_credit=partylink._agenda_credit,
                    agenda_debt=partylink._agenda_debt,
                    agenda_goal_credit=partylink._agenda_goal_credit,
                    agenda_goal_debt=partylink._agenda_goal_debt,
                )

    def _set_agenda_goal_ratio_credit_debt(self):
        agenda_goal_ratio_credit_sum = 0
        agenda_goal_ratio_debt_sum = 0

        for partyunit_x in self._partys.values():
            agenda_goal_ratio_credit_sum += partyunit_x._agenda_goal_credit
            agenda_goal_ratio_debt_sum += partyunit_x._agenda_goal_debt

        for partyunit_x in self._partys.values():
            partyunit_x.set_agenda_goal_ratio_credit_debt(
                agenda_goal_ratio_credit_sum=agenda_goal_ratio_credit_sum,
                agenda_goal_ratio_debt_sum=agenda_goal_ratio_debt_sum,
                agenda_partyunit_total_creditor_weight=self.get_partyunit_total_creditor_weight(),
                agenda_partyunit_total_debtor_weight=self.get_partyunit_total_debtor_weight(),
            )

    def get_party_groups(self, party_title: PartyTitle):
        groups = []
        for group in self._groups.values():
            groups.extend(
                group.brand
                for partylink in group._partys.values()
                if partylink.title == party_title
            )

        return groups

    def _reset_partyunit_agenda_credit_debt(self):
        self.set_partys_empty_if_null()
        for partyunit in self._partys.values():
            partyunit.reset_agenda_credit_debt()

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

    def get_idea_kid(self, road: Road) -> IdeaCore:
        if road is None:
            raise InvalidDealException("get_idea_kid received road=None")
        nodes = get_all_road_nodes(road)
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
                    raise InvalidDealException(
                        f"Temp_idea is None {idea_label=}. No item at '{road}'"
                    )
            except:
                raise InvalidDealException(
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
        child_balancelines = None
        if road is None:
            road = ""

        group_everyone = None
        if len(get_all_road_nodes(road)) <= 1:
            group_everyone = self._idearoot._balanceheirs in [None, {}]
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
                    yu_idea_obj.set_kidless_balancelines()
                    child_balancelines = yu_idea_obj._balancelines
                else:
                    yu_idea_obj.set_balancelines(child_balancelines=child_balancelines)

                if yu_idea_obj._task == True:
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
        self._idearoot._level = 0
        self._idearoot.set_pad(parent_road="")
        self._idearoot.set_requiredheirs(agenda_idea_dict=self._idea_dict)
        self._idearoot.set_assignedheir(
            parent_assignheir=None, agenda_groups=self._groups
        )
        self._idearoot.inherit_balanceheirs()
        self._idearoot.clear_balancelines()
        self._idearoot.set_originunit_empty_if_null()
        self._idearoot.set_acptfactunits_empty_if_null()
        self._idearoot._weight = 1
        self._idearoot._kids_total_weight = 0
        self._idearoot.set_kids_total_weight()
        self._idearoot.set_sibling_total_weight(1)
        self._idearoot.set_agenda_importance(coin_onset_x=0, parent_coin_cease=1)
        self._idearoot.set_balanceheirs_agenda_credit_debit()
        self._idearoot.set_ancestor_promise_count(0, False)
        self._idearoot.clear_descendant_promise_count()
        self._idearoot.clear_all_party_credit_debt()
        self._idearoot.promise = False

        if self._idearoot.is_kidless():
            self._set_ancestor_metrics(road=self._idearoot._pad)
            self._distribute_agenda_importance(idea=self._idearoot)

    def _set_kids_attributes(
        self,
        idea_kid: IdeaCore,
        coin_onset: float,
        parent_coin_cease: float,
        parent_idea: IdeaCore = None,
    ) -> IdeaCore:
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
        idea_kid.set_pad(parent_road=parent_idea._pad, parent_label=parent_idea._label)
        idea_kid.set_acptfactunits_empty_if_null()
        idea_kid.set_acptfactheirs(acptfacts=parent_acptfacts)
        idea_kid.set_requiredheirs(self._idea_dict, parent_requiredheirs)
        idea_kid.set_assignedheir(parent_idea._assignedheir, self._groups)
        idea_kid.inherit_balanceheirs(parent_idea._balanceheirs)
        idea_kid.clear_balancelines()
        idea_kid.set_originunit_empty_if_null()
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
            self._set_ancestor_metrics(road=idea_kid.get_road())
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
    ):
        sibling_ratio = weight / sibling_total_weight
        return parent_agenda_importance * sibling_ratio

    def get_idea_list(self):
        self.set_agenda_metrics()
        return list(self._idea_dict.values())

    def set_agenda_metrics(self):
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

        coin_onset = self._idearoot._agenda_coin_onset
        parent_coin_cease = self._idearoot._agenda_coin_cease

        cache_idea_list = []
        for idea_kid in self._idearoot._kids.values():
            self._set_kids_attributes(
                idea_kid=idea_kid,
                coin_onset=coin_onset,
                parent_coin_cease=parent_coin_cease,
            )
            cache_idea_list.append(idea_kid)
            coin_onset += idea_kid._agenda_importance

        # no function recursion, recursion by iterateing over list that can be added to by iterations
        while cache_idea_list != []:
            parent_idea = cache_idea_list.pop()
            if self._tree_traverse_count == 0:
                self._idea_dict[parent_idea.get_road()] = parent_idea

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

    def _run_after_each_tree_traverse(self):
        any_idea_active_status_changed = False
        for idea in self._idea_dict.values():
            idea.set_active_status_hx_empty_if_null()
            if idea._active_status_hx.get(self._tree_traverse_count) != None:
                any_idea_active_status_changed = True

        if any_idea_active_status_changed == False:
            self._rational = True

    def _run_after_idea_all_tree_traverses(self):
        self._distribute_agenda_goal_importance()
        self._distribute_groups_agenda_importance()
        self._set_agenda_goal_ratio_credit_debt()

    def _run_before_idea_tree_traverse(self):
        self._reset_groupunits_agenda_credit_debt()
        self._reset_groupunits_agenda_credit_debt()
        self._reset_partyunit_agenda_credit_debt()

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

    def get_partys_dict(self):
        x_dict = {}
        if self._partys != None:
            for party_title, party_obj in self._partys.items():
                x_dict[party_title] = party_obj.get_dict()
        return x_dict

    def groupunit_shops_dict(self):
        x_dict = {}
        if self._groups != None:
            for group_title, group_obj in self._groups.items():
                x_dict[group_title] = group_obj.get_dict()
        return x_dict

    def get_dict(self):
        self.set_agenda_metrics()
        return {
            "_kids": self._idearoot.get_kids_dict(),
            "_requiredunits": self._idearoot.get_requiredunits_dict(),
            "_acptfactunits": self.get_acptfactunits_dict(),
            "_partys": self.get_partys_dict(),
            "_groups": self.groupunit_shops_dict(),
            "_balancelinks": self._idearoot.get_balancelinks_dict(),
            "_assignedunit": self._idearoot.get_assignedunit_dict(),
            "_originunit": self._originunit.get_dict(),
            "_weight": self._weight,
            "_healer": self._healer,
            "_culture_handle": self._culture_handle,
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
            "_auto_output_to_public": self._auto_output_to_public,
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
                range_source_road_x = f"{self._culture_handle},{yb.sr}"

            idea_x = ideacore_shop(
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
            road_x = f"{self._culture_handle},{yb.rr}"
            self.add_idea(idea_kid=idea_x, pad=road_x)

            numeric_road_x = None
            if yb.nr != None:
                numeric_road_x = f"{self._culture_handle},{yb.nr}"
                self.edit_idea_attr(
                    road=f"{road_x},{yb.n}", numeric_road=numeric_road_x
                )
            if yb.a != None:
                self.edit_idea_attr(
                    road=f"{road_x},{yb.n}", addin=yb.a, denom=yb.md, numor=yb.mn
                )

        self.set_agenda_metrics()

    def get_agenda4party(
        self, party_title: PartyTitle, acptfacts: dict[Road:AcptFactCore]
    ):
        self.set_agenda_metrics()
        agenda4party = agendaunit_shop(_healer=party_title)
        agenda4party._idearoot._agenda_importance = self._idearoot._agenda_importance
        # get party's partys: partyzone

        # get partyzone groups
        party_groups = self.get_party_groups(party_title=party_title)

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

    # def get_goal_items(
    #     self, goal_enterprise: bool = True, goal_state: bool = True, base: Road = None
    # ) -> list[IdeaCore]:
    #     return list(self.get_goal_items(base=base))

    def set_dominate_promise_idea(self, idea_kid: IdeaCore):
        idea_kid.promise = True
        self.add_idea(
            idea_kid=idea_kid,
            pad=Road(f"{idea_kid._pad}"),
            create_missing_ideas_groups=True,
        )

    def get_idea_list_without_idearoot(self):
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
        party_title = other_agenda._healer
        o_idea_list = other_agenda.get_idea_list_without_idearoot()
        for o_idea in o_idea_list:
            o_road = road_validate(f"{o_idea._pad},{o_idea._label}")
            try:
                main_idea = self.get_idea_kid(o_road)
                main_idea.meld(o_idea, False, party_title, party_weight)
            except Exception:
                self.add_idea(pad=o_idea._pad, idea_kid=o_idea)
                main_idea = self.get_idea_kid(o_road)
                main_idea._originunit.set_originlink(party_title, party_weight)

    def _meld_partys(self, other_agenda):
        self.set_partys_empty_if_null()
        other_agenda.set_partys_empty_if_null()
        for partyunit in other_agenda._partys.values():
            if self._partys.get(partyunit.title) is None:
                self.set_partyunit(partyunit=partyunit)
            else:
                self._partys.get(partyunit.title).meld(partyunit)

    def _meld_groups(self, other_agenda):
        self.set_groupunits_empty_if_null()
        other_agenda.set_groupunits_empty_if_null()
        for brx in other_agenda._groups.values():
            if self._groups.get(brx.brand) is None:
                self.set_groupunit(groupunit=brx)
            else:
                self._groups.get(brx.brand).meld(brx)

    def _meld_acptfacts(self, other_agenda):
        self._set_acptfacts_empty_if_null()
        other_agenda._set_acptfacts_empty_if_null()
        for hx in other_agenda._idearoot._acptfactunits.values():
            if self._idearoot._acptfactunits.get(hx.base) is None:
                self.set_acptfact(
                    base=hx.base, acptfact=hx.acptfact, open=hx.open, nigh=hx.nigh
                )
            else:
                self._idearoot._acptfactunits.get(hx.base).meld(hx)

    def _meld_originlinks(self, party_title: PartyTitle, party_weight: float):
        if party_title != None:
            self._originunit.set_originlink(party_title, party_weight)

    def get_assignment(
        self,
        agenda_x,
        assignor_partys: dict[PartyTitle:PartyUnit],
        assignor_title: PartyTitle,
    ) -> PersonName:
        self.set_agenda_metrics()
        self._set_assignment_partys(agenda_x, assignor_partys, assignor_title)
        self._set_assignment_groups(agenda_x)
        assignor_promises = self._get_assignor_promise_ideas(agenda_x, assignor_title)
        relevant_roads = self._get_relevant_roads(assignor_promises)
        self._set_assignment_ideas(agenda_x, relevant_roads)
        return agenda_x

    def _set_assignment_ideas(self, agenda_x, relevant_roads: dict[Road:str]):
        sorted_relevants = sorted(list(relevant_roads))
        # don't know how to manage root idea attributes...
        if sorted_relevants != []:
            root_road = sorted_relevants.pop(0)

        for relevant_road in sorted_relevants:
            relevant_idea = copy_deepcopy(self.get_idea_kid(relevant_road))
            # if relevant_roads.get(relevant_road) == "descendant":
            #     relevant_idea._requiredunits = {}
            #     relevant_idea._kids = {}
            #     agenda_x.add_idea(idea_kid=relevant_idea, pad=relevant_idea._pad)
            # elif relevant_roads.get(relevant_road) != "descendant":
            relevant_idea._kids = {}
            agenda_x.add_idea(idea_kid=relevant_idea, pad=relevant_idea._pad)

        for afu in self._idearoot._acptfactunits.values():
            if relevant_roads.get(afu.base):
                agenda_x.set_acptfact(
                    base=afu.base, pick=afu.pick, open=afu.open, nigh=afu.nigh
                )

    def _set_assignment_partys(
        self,
        agenda_x,
        assignor_partys: dict[PartyTitle:PartyUnit],
        assignor_title: PartyTitle,
    ):
        agenda_x.set_partys_empty_if_null()
        if self._partys.get(assignor_title) != None:
            # get all partys that are both in self._partys and assignor_known_partys
            partys_set = get_intersection_of_partys(self._partys, assignor_partys)
            for partytitle_x in partys_set:
                agenda_x.set_partyunit(partyunit=self._partys.get(partytitle_x))
        return agenda_x

    def _set_assignment_groups(self, agenda_x):
        revelant_groups = get_partys_relevant_groups(self._groups, agenda_x._partys)
        for group_title, group_partys in revelant_groups.items():
            if agenda_x._groups.get(group_title) is None:
                group_x = groupunit_shop(brand=group_title)
                for party_title in group_partys:
                    group_x.set_partylink(partylink_shop(title=party_title))
                agenda_x.set_groupunit(group_x)

    def _get_assignor_promise_ideas(
        self, agenda_x, assignor_title: GroupBrand
    ) -> dict[Road:int]:
        agenda_x.set_groupunits_empty_if_null()
        assignor_groups = get_party_relevant_groups(agenda_x._groups, assignor_title)
        return {
            idea_road: -1
            for idea_road, idea_x in self._idea_dict.items()
            if (idea_x.assignor_in(assignor_groups) and idea_x.promise)
        }

    def _set_auto_output_to_public(self, bool_x: bool):
        if bool_x is None and self._auto_output_to_public is None:
            self._auto_output_to_public = False
        elif bool_x is not None or not self._auto_output_to_public:
            self._auto_output_to_public = bool_x is not None and bool_x


def agendaunit_shop(
    _healer: PersonName = None,
    _weight: float = None,
    _auto_output_to_public: bool = None,
) -> DealUnit:
    if _weight is None:
        _weight = 1
    if _healer is None:
        _healer = ""
    if _auto_output_to_public is None:
        _auto_output_to_public = False
    x_agenda = DealUnit(
        _healer=_healer, _weight=_weight, _auto_output_to_public=_auto_output_to_public
    )
    x_agenda._culture_handle = root_label()
    x_agenda._idearoot = idearoot_shop(_label=None, _uid=1, _level=0)
    x_agenda.set_max_tree_traverse(3)
    x_agenda._rational = False
    x_agenda._originunit = originunit_shop()
    return x_agenda


def get_from_json(x_agenda_json: str) -> DealUnit:
    return get_from_dict(cx_dict=json.loads(x_agenda_json))


def get_from_dict(cx_dict: dict) -> DealUnit:
    x_agenda = agendaunit_shop()
    x_agenda.set_culture_handle(cx_dict["_culture_handle"])
    x_agenda._idearoot._requiredunits = requireds_get_from_dict(
        requireds_dict=cx_dict["_requiredunits"]
    )
    _assignedunit = "_assignedunit"
    if cx_dict.get(_assignedunit):
        x_agenda._idearoot._assignedunit = assignedunit_get_from_dict(
            assignedunit_dict=cx_dict.get(_assignedunit)
        )
    x_agenda._idearoot._acptfactunits = acptfactunits_get_from_dict(
        x_dict=cx_dict["_acptfactunits"]
    )
    x_agenda._groups = groupunits_get_from_dict(x_dict=cx_dict["_groups"])
    x_agenda._idearoot._balancelinks = balancelinks_get_from_dict(
        x_dict=cx_dict["_balancelinks"]
    )
    try:
        x_agenda._originunit = originunit_get_from_dict(x_dict=cx_dict["_originunit"])
    except Exception:
        x_agenda._originunit = originunit_shop()
    try:
        x_agenda._auto_output_to_public = cx_dict["_auto_output_to_public"]
    except Exception:
        x_agenda._auto_output_to_public = False
    x_agenda._partys = partyunits_get_from_dict(x_dict=cx_dict["_partys"])
    x_agenda._healer = cx_dict["_healer"]
    x_agenda._idearoot.set_idea_label(
        x_agenda._culture_handle, x_agenda._culture_handle
    )
    x_agenda._weight = cx_dict["_weight"]
    x_agenda._max_tree_traverse = cx_dict.get("_max_tree_traverse")
    if cx_dict.get("_max_tree_traverse") is None:
        x_agenda._max_tree_traverse = 20
    x_agenda._idearoot._weight = cx_dict["_weight"]
    x_agenda._idearoot._uid = cx_dict["_uid"]
    x_agenda._idearoot._begin = cx_dict["_begin"]
    x_agenda._idearoot._close = cx_dict["_close"]
    x_agenda._idearoot._numor = cx_dict["_numor"]
    x_agenda._idearoot._denom = cx_dict["_denom"]
    x_agenda._idearoot._reest = cx_dict["_reest"]
    x_agenda._idearoot._range_source_road = cx_dict["_range_source_road"]
    x_agenda._idearoot._numeric_road = cx_dict["_numeric_road"]
    x_agenda._idearoot._is_expanded = cx_dict["_is_expanded"]

    idea_dict_list = []
    for x_dict in cx_dict["_kids"].values():
        x_dict["temp_road"] = x_agenda._healer
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

        idea_obj = ideacore_shop(
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
            _balancelinks=balancelinks_get_from_dict(idea_dict["_balancelinks"]),
            _acptfactunits=acptfactunits_get_from_dict(idea_dict["_acptfactunits"]),
            _is_expanded=idea_dict["_is_expanded"],
            _range_source_road=idea_dict["_range_source_road"],
            _numeric_road=idea_dict["_numeric_road"],
        )
        x_agenda.add_idea(idea_kid=idea_obj, pad=idea_dict["temp_road"])

    x_agenda.set_agenda_metrics()  # clean up tree traverse defined fields
    return x_agenda


def get_dict_of_agenda_from_dict(x_dict: dict[str:dict]) -> dict[str:DealUnit]:
    agendaunits = {}
    for agendaunit_dict in x_dict.values():
        x_agenda = get_from_dict(cx_dict=agendaunit_dict)
        agendaunits[x_agenda._healer] = x_agenda
    return agendaunits


def get_meld_of_agenda_files(primary_agenda: DealUnit, meldees_dir: str) -> DealUnit:
    primary_agenda.set_agenda_metrics()
    for meldee_file_x in x_func_dir_files(dir_path=meldees_dir):
        meldee_x = get_from_json(
            x_agenda_json=x_func_open_file(meldees_dir, meldee_file_x)
        )
        primary_agenda.meld(other_agenda=meldee_x)

    primary_agenda.set_agenda_metrics()
    return primary_agenda


def get_intersection_of_partys(
    partys_x: dict[PartyTitle:PartyUnit], partys_y: dict[PartyTitle:PartyUnit]
) -> dict[PartyTitle:-1]:
    x_set = set(partys_x)
    y_set = set(partys_y)
    intersection_x = x_set.intersection(y_set)
    return {partytitle_x: -1 for partytitle_x in intersection_x}


def get_partys_relevant_groups(
    groups_x: dict[GroupBrand:GroupUnit], partys_x: dict[PartyTitle:PartyUnit]
) -> dict[GroupBrand:{PartyTitle: -1}]:
    relevant_groups = {}
    for partytitle_x in partys_x:
        for group_x in groups_x.values():
            if group_x._partys.get(partytitle_x) != None:
                if relevant_groups.get(group_x.brand) is None:
                    relevant_groups[group_x.brand] = {}
                relevant_groups.get(group_x.brand)[partytitle_x] = -1

    return relevant_groups


def get_party_relevant_groups(
    groups_x: dict[GroupBrand:GroupUnit], partytitle_x: PartyTitle
) -> dict[GroupBrand:-1]:
    return {
        group_x.brand: -1
        for group_x in groups_x.values()
        if group_x._partys.get(partytitle_x) != None
    }
