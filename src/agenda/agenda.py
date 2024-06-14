from src._instrument.python import (
    get_json_from_dict,
    get_dict_from_json,
    get_1_if_None,
    get_0_if_None,
    get_False_if_None,
    get_empty_dict_if_none,
)
from src._road.finance import (
    trim_planck_excess,
    default_planck_if_none,
    default_penny_if_none,
)
from src._road.jaar_config import max_tree_traverse_default
from src._road.road import (
    get_parent_road,
    is_sub_road,
    road_validate,
    rebuild_road,
    get_terminus_node,
    get_root_node_from_road,
    find_replace_road_key_dict,
    get_ancestor_roads,
    get_default_real_id_roadnode,
    get_all_road_nodes,
    get_forefather_roads,
    create_road,
    default_road_delimiter_if_none,
    RoadNode,
    RoadUnit,
    is_string_in_road,
    OwnerID,
    PartyID,
    HealerID,
    RealID,
    is_roadunit_convertible_to_path,
)
from src.agenda.meld import (
    get_meld_weight,
    MeldStrategy,
    get_meld_default,
    validate_meld_strategy,
)
from src.agenda.party import (
    PartyUnit,
    PartyLink,
    partyunits_get_from_dict,
    partyunit_shop,
    partylink_shop,
    PartyUnitExternalMetrics,
)
from src.agenda.idea import (
    BalanceLink,
    IdeaID,
    IdeaUnit,
    get_ideaunits_from_dict,
    ideaunit_shop,
    balancelink_shop,
    get_party_relevant_ideas,
    get_partys_relevant_ideas,
    get_intersection_of_partys,
)
from src.agenda.healer import HealerHold
from src.agenda.reason_fact import (
    BeliefCore,
    BeliefUnit,
    BeliefUnit,
    ReasonUnit,
    RoadUnit,
    beliefunit_shop,
)
from src.agenda.reason_assign import AssignedUnit
from src.agenda.tree_metrics import TreeMetrics, treemetrics_shop
from src.agenda.hreg_time import HregTimeFactSource as HregFact
from src.agenda.lemma import lemmas_shop, Lemmas
from src.agenda.origin import originunit_get_from_dict, originunit_shop, OriginUnit
from src.agenda.fact import (
    FactUnit,
    factunit_shop,
    factattrfilter_shop,
    FactAttrFilter,
    get_obj_from_fact_dict,
)
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from datetime import datetime


class InvalidAgendaException(Exception):
    pass


class InvalidLabelException(Exception):
    pass


class NewDelimiterException(Exception):
    pass


class PartyUnitsCredorDebtorSumException(Exception):
    pass


class PartyMissingException(Exception):
    pass


class Exception_econs_justified(Exception):
    pass


class _planck_RatioException(Exception):
    pass


class _last_atom_idException(Exception):
    pass


class healerhold_idea_id_Exception(Exception):
    pass


@dataclass
class AgendaUnit:
    _real_id: RealID = None
    _owner_id: OwnerID = None
    _last_atom_id: int = None
    _weight: float = None
    _partys: dict[PartyID:PartyUnit] = None
    _ideas: dict[IdeaID:IdeaUnit] = None
    _factroot: FactUnit = None
    _max_tree_traverse: int = None
    _road_delimiter: str = None
    _planck: float = None
    _penny: float = None
    _monetary_desc: str = None
    _party_credor_pool: int = None
    _party_debtor_pool: int = None
    _meld_strategy: MeldStrategy = None
    _originunit: OriginUnit = None  # In job agendas this shows source
    # calc_agenda_metrics Calculated field begin
    _fact_dict: dict[RoadUnit:FactUnit] = None
    _econ_dict: dict[RoadUnit:FactUnit] = None
    _healers_dict: dict[HealerID : dict[RoadUnit:FactUnit]] = None
    _tree_traverse_count: int = None
    _rational: bool = None
    _econs_justified: bool = None
    _econs_buildable: bool = None
    _sum_healerhold_importance: bool = None
    # calc_agenda_metrics Calculated field end

    def del_last_atom_id(self):
        self._last_atom_id = None

    def set_last_atom_id(self, x_last_atom_id: int):
        if self._last_atom_id != None and x_last_atom_id < self._last_atom_id:
            raise _last_atom_idException(
                f"Cannot set _last_atom_id to {x_last_atom_id} because it is less than {self._last_atom_id}."
            )
        self._last_atom_id = x_last_atom_id

    def set_monetary_desc(self, x_monetary_desc: str):
        self._monetary_desc = x_monetary_desc

    def set_party_pool(self, x_party_pool: int):
        self.set_party_credor_pool(
            new_party_credor_pool=x_party_pool,
            update_partys_credor_weight=True,
            correct_planck_issues=True,
        )
        self.set_party_debtor_pool(
            new_party_debtor_pool=x_party_pool,
            update_partys_debtor_weight=True,
            correct_planck_issues=True,
        )

    def set_party_credor_pool(
        self,
        new_party_credor_pool: int,
        update_partys_credor_weight: bool = False,
        correct_planck_issues: bool = False,
    ):
        if (new_party_credor_pool / self._planck).is_integer() is False:
            raise _planck_RatioException(
                f"Agenda '{self._owner_id}' cannot set _party_credor_pool='{new_party_credor_pool}'. It is not divisible by planck '{self._planck}'"
            )

        if update_partys_credor_weight:
            old_party_credor_pool = self.get_partyunits_credor_weight_sum()
            if old_party_credor_pool != 0:
                x_ratio = new_party_credor_pool / old_party_credor_pool
                for x_party in self._partys.values():
                    new_party_credor_weight = trim_planck_excess(
                        num=x_party.credor_weight * x_ratio, planck=x_party._planck
                    )
                    x_party.set_credor_weight(new_party_credor_weight)

        self._party_credor_pool = new_party_credor_pool
        if correct_planck_issues:
            self._correct_any_credor_planck_issues()

    def _correct_any_credor_planck_issues(self):
        if self.get_partyunits_credor_weight_sum() != self._party_credor_pool:
            missing_credor_weight = (
                self._party_credor_pool - self.get_partyunits_credor_weight_sum()
            )
            if len(self._partys) > 0:
                partyunits = list(self._partys.values())
                # partys_count = len(self._partys)
                # planck_count = missing_credor_weight / self._planck
                # if planck_count <= partys_count:
                for _ in range(0, missing_credor_weight, self._planck):
                    x_partyunit = partyunits.pop()
                    x_partyunit.set_credor_weight(
                        x_partyunit.credor_weight + self._planck
                    )

    def set_party_debtor_pool(
        self,
        new_party_debtor_pool: int,
        update_partys_debtor_weight: bool = False,
        correct_planck_issues: bool = False,
    ):
        if (new_party_debtor_pool / self._planck).is_integer() is False:
            raise _planck_RatioException(
                f"Agenda '{self._owner_id}' cannot set _party_debtor_pool='{new_party_debtor_pool}'. It is not divisible by planck '{self._planck}'"
            )

        if update_partys_debtor_weight:
            old_party_debtor_pool = self.get_partyunits_debtor_weight_sum()
            if old_party_debtor_pool != 0:
                x_ratio = new_party_debtor_pool / old_party_debtor_pool
                for x_party in self._partys.values():
                    new_party_debtor_weight = trim_planck_excess(
                        num=x_party.debtor_weight * x_ratio, planck=x_party._planck
                    )
                    x_party.set_debtor_weight(new_party_debtor_weight)
        self._party_debtor_pool = new_party_debtor_pool
        if correct_planck_issues:
            self._correct_any_debtor_planck_issues()

    def _correct_any_debtor_planck_issues(self):
        if self.get_partyunits_debtor_weight_sum() != self._party_debtor_pool:
            missing_debtor_weight = (
                self._party_debtor_pool - self.get_partyunits_debtor_weight_sum()
            )
            if len(self._partys) > 0:
                partyunits = list(self._partys.values())
                # partys_count = len(self._partys)
                # planck_count = missing_debtor_weight / self._planck
                # if planck_count <= partys_count:
                for _ in range(0, missing_debtor_weight, self._planck):
                    x_partyunit = partyunits.pop()
                    x_partyunit.set_debtor_weight(
                        x_partyunit.debtor_weight + self._planck
                    )

    def make_road(
        self,
        parent_road: RoadUnit = None,
        terminus_node: RoadNode = None,
    ) -> RoadUnit:
        x_road = create_road(
            parent_road=parent_road,
            terminus_node=terminus_node,
            delimiter=self._road_delimiter,
        )
        return road_validate(x_road, self._road_delimiter, self._real_id)

    def make_l1_road(self, l1_node: RoadNode):
        return self.make_road(self._real_id, l1_node)

    def set_partys_output_agenda_meld_order(self):
        sort_partys_list = list(self._partys.values())
        sort_partys_list.sort(key=lambda x: x.party_id.lower(), reverse=False)
        for count_x, x_partyunit in enumerate(sort_partys_list):
            x_partyunit.set_output_agenda_meld_order(count_x)

    def clear_partys_output_agenda_meld_order(self):
        for x_partyunit in self._partys.values():
            x_partyunit.clear_output_agenda_meld_order()

    def set_road_delimiter(self, new_road_delimiter: str):
        self.calc_agenda_metrics()
        if self._road_delimiter != new_road_delimiter:
            for x_fact_road in self._fact_dict.keys():
                if is_string_in_road(new_road_delimiter, x_fact_road):
                    raise NewDelimiterException(
                        f"Cannot modify delimiter to '{new_road_delimiter}' because it already exists an fact label '{x_fact_road}'"
                    )

            # Grab pointers to every fact
            fact_pointers = {
                x_fact_road: self.get_fact_obj(x_fact_road)
                for x_fact_road in self._fact_dict.keys()
            }

            # modify all road attributes in fact
            # old_road_delimiter = copy_deepcopy(self._road_delimiter)
            self._road_delimiter = default_road_delimiter_if_none(new_road_delimiter)
            for x_fact in fact_pointers.values():
                x_fact.set_road_delimiter(self._road_delimiter)

    def set_real_id(self, real_id: str):
        old_real_id = copy_deepcopy(self._real_id)
        self._real_id = real_id

        self.calc_agenda_metrics()
        for fact_obj in self._fact_dict.values():
            fact_obj._agenda_real_id = self._real_id

        self.edit_fact_label(old_road=old_real_id, new_label=self._real_id)
        self.calc_agenda_metrics()

    def set_partyunit_external_metrics(
        self, external_metrics: PartyUnitExternalMetrics
    ):
        party_x = self.get_party(external_metrics.internal_party_id)
        party_x._credor_operational = external_metrics.credor_operational
        party_x._debtor_operational = external_metrics.debtor_operational
        # self.set_partyunit(partyunit=party_x)

    def set_max_tree_traverse(self, int_x: int):
        if int_x < 2:
            raise InvalidAgendaException(
                f"set_max_tree_traverse: input '{int_x}' must be number that is 2 or greater"
            )
        else:
            self._max_tree_traverse = int_x

    def get_agenda_sprung_from_single_fact(self, road: RoadUnit) -> any:
        self.calc_agenda_metrics()
        x_fact = self.get_fact_obj(road)
        new_weight = self._weight * x_fact._agenda_importance
        x_agenda = agendaunit_shop(_owner_id=self._factroot._label, _weight=new_weight)

        for road_assc in sorted(list(self._get_relevant_roads({road}))):
            src_yx = self.get_fact_obj(road_assc)
            new_yx = copy_deepcopy(src_yx)
            if new_yx._parent_road != "":
                x_agenda.add_fact(new_yx, parent_road=new_yx._parent_road)
            x_agenda.calc_agenda_metrics()

        # TODO grab ideas
        # TODO grab all idea partys
        # TODO grab beliefs
        return x_agenda

    def _get_relevant_roads(self, roads: dict[RoadUnit:]) -> dict[RoadUnit:str]:
        to_evaluate_list = []
        to_evaluate_hx_dict = {}
        for road_x in roads:
            to_evaluate_list.append(road_x)
            to_evaluate_hx_dict[road_x] = "to_evaluate"
        evaluated_roads = {}

        # tree_metrics = self.get_tree_metrics()
        # while roads_to_evaluate != [] and count_x <= tree_metrics.node_count:
        # transited because count_x might be wrong thing to measure
        # nice to avoid infinite loops from programming errors though...
        while to_evaluate_list != []:
            road_x = to_evaluate_list.pop()
            x_fact = self.get_fact_obj(road_x)
            for reasonunit_obj in x_fact._reasonunits.values():
                reason_base = reasonunit_obj.base
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=reason_base,
                    road_type="reasonunit_base",
                )

            if x_fact._numeric_road != None:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=x_fact._numeric_road,
                    road_type="numeric_road",
                )

            if x_fact._range_source_road != None:
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=x_fact._range_source_road,
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
        to_evaluate_list: list[RoadUnit],
        to_evaluate_hx_dict: dict[RoadUnit:int],
        to_evaluate_road: RoadUnit,
        road_type: str,
    ):
        if to_evaluate_hx_dict.get(to_evaluate_road) is None:
            to_evaluate_list.append(to_evaluate_road)
            to_evaluate_hx_dict[to_evaluate_road] = road_type

            if road_type == "reasonunit_base":
                ru_base_fact = self.get_fact_obj(to_evaluate_road)
                for descendant_road in ru_base_fact.get_descendant_roads_from_kids():
                    self._evaluate_relevancy(
                        to_evaluate_list=to_evaluate_list,
                        to_evaluate_hx_dict=to_evaluate_hx_dict,
                        to_evaluate_road=descendant_road,
                        road_type="reasonunit_descendant",
                    )

    def all_facts_relevant_to_pledge_fact(self, road: RoadUnit) -> bool:
        pledge_fact_assoc_set = set(self._get_relevant_roads({road}))
        all_facts_set = set(self.get_fact_tree_ordered_road_list())
        return all_facts_set == all_facts_set.intersection(pledge_fact_assoc_set)

    def _are_all_partys_ideas_are_in_fact_kid(self, road: RoadUnit) -> bool:
        fact_kid = self.get_fact_obj(road)
        # get dict of all fact balanceheirs
        balanceheir_list = fact_kid._balanceheirs.keys()
        balanceheir_dict = {
            balanceheir_idea_id: 1 for balanceheir_idea_id in balanceheir_list
        }
        non_single_ideaunits = {
            ideaunit.idea_id: ideaunit
            for ideaunit in self._ideas.values()
            if ideaunit._party_mirror != True
        }
        # check all non_party_mirror_ideaunits are in balanceheirs
        for non_single_idea in non_single_ideaunits.values():
            if balanceheir_dict.get(non_single_idea.idea_id) is None:
                return False

        # get dict of all partylinks that are in all balanceheirs
        balanceheir_partyunits = {}
        for balanceheir_party_id in balanceheir_dict:
            ideaunit = self.get_ideaunit(balanceheir_party_id)
            for partylink in ideaunit._partys.values():
                balanceheir_partyunits[partylink.party_id] = self.get_party(
                    partylink.party_id
                )

        # check all agenda._partys are in balanceheir_partyunits
        return len(self._partys) == len(balanceheir_partyunits)

    def get_time_min_from_dt(self, dt: datetime) -> float:
        x_hregfact = HregFact(self._road_delimiter)
        return x_hregfact.get_time_min_from_dt(dt=dt)

    def get_time_c400_from_min(self, min: int) -> int:
        time_road = self.make_l1_road("time")
        tech_road = self.make_road(time_road, "tech")
        c400_road = self.make_road(tech_road, "400 year segment")
        c400_fact = self.get_fact_obj(c400_road)
        c400_min = c400_fact._close
        return int(min / c400_min), c400_fact, min % c400_min

    def get_time_c400yr_from_min(self, min: int):
        # GIVEN int minutes within 400 year range return year and remainder minutes
        c400_count, c400_fact, c400yr_min = self.get_time_c400_from_min(min=min)
        c100_4_96y = c400_fact.get_kids_in_range(begin=c400yr_min, close=c400yr_min)[0]
        cXXXyr_min = c400yr_min - c100_4_96y._begin

        time_road = self.make_l1_road("time")
        tech_road = self.make_road(time_road, "tech")

        # identify which range the time is in
        if c100_4_96y._close - c100_4_96y._begin in (
            50492160,
            52596000,
        ):  # 96 year and 100 year facts
            yr4_1461_road = self.make_road(tech_road, "4year with leap")
            yr4_1461_fact = self.get_fact_obj(yr4_1461_road)
            yr4_segments = int(cXXXyr_min / yr4_1461_fact._close)
            cXyr_min = cXXXyr_min % yr4_1461_fact._close
            yr1_fact = yr4_1461_fact.get_kids_in_range(begin=cXyr_min, close=cXyr_min)[
                0
            ]
        elif c100_4_96y._close - c100_4_96y._begin == 2102400:
            yr4_1460_road = self.make_road(tech_road, "4year wo leap")
            yr4_1460_fact = self.get_fact_obj(yr4_1460_road)
            yr4_segments = 0
            yr1_fact = yr4_1460_fact.get_kids_in_range(cXXXyr_min, cXXXyr_min)[0]
            cXyr_min = cXXXyr_min % yr4_1460_fact._close

        yr1_rem_min = cXyr_min - yr1_fact._begin
        yr1_fact_begin = int(yr1_fact._label.split("-")[0]) - 1

        c100_4_96y_begin = int(c100_4_96y._label.split("-")[0])
        year_num = c100_4_96y_begin + (4 * yr4_segments) + yr1_fact_begin
        return year_num, yr1_fact, yr1_rem_min

    def get_time_month_from_min(self, min: int):
        time_road = self.make_l1_road("time")
        tech_road = self.make_road(time_road, "tech")

        year_num, yr1_fact, yr1_fact_rem_min = self.get_time_c400yr_from_min(min=min)
        yrx = None
        if yr1_fact._close - yr1_fact._begin == 525600:
            yr365_road = self.make_road(tech_road, "365 year")
            yrx = self.get_fact_obj(yr365_road)
        elif yr1_fact._close - yr1_fact._begin == 527040:
            yr366_road = self.make_road(tech_road, "366 year")
            yrx = self.get_fact_obj(yr366_road)
        mon_x = yrx.get_kids_in_range(begin=yr1_fact_rem_min, close=yr1_fact_rem_min)[0]
        month_rem_min = yr1_fact_rem_min - mon_x._begin
        month_num = int(mon_x._label.split("-")[0])
        day_road = self.make_road(tech_road, "day")
        day_x = self.get_fact_obj(day_road)
        day_num = int(month_rem_min / day_x._close)
        day_rem_min = month_rem_min % day_x._close
        return month_num, day_num, day_rem_min, day_x

    def get_time_hour_from_min(self, min: int) -> set[int, int, list[int]]:
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
        x_hregfact = HregFact(self._road_delimiter)
        return x_hregfact.get_jajatime_legible_from_dt(dt=dt_x)

    def get_jajatime_repeating_legible_text(
        self, open: float = None, nigh: float = None, divisor: float = None
    ) -> str:
        x_hregfact = HregFact(self._road_delimiter)
        str_x = "test3"
        if divisor is None:
            str_x = self.get_jajatime_legible_one_time_event(jajatime_min=open)
        elif divisor != None and divisor % 10080 == 0:
            str_x = self._get_jajatime_week_legible_text(open, divisor)
        elif divisor != None and divisor % 1440 == 0:
            if divisor == 1440:
                str_x = (
                    f"every day at {x_hregfact.convert1440toReadableTime(min1440=open)}"
                )
            else:
                num_days = int(divisor / 1440)
                num_with_letter_ending = x_hregfact.get_number_with_letter_ending(
                    num=num_days
                )
                str_x = f"every {num_with_letter_ending} day at {x_hregfact.convert1440toReadableTime(min1440=open)}"
        else:
            str_x = "unknown"
        return str_x

    def _get_jajatime_week_legible_text(self, open: int, divisor: int) -> str:
        x_hregfact = HregFact(self._road_delimiter)
        open_in_week = open % divisor
        time_road = self.make_l1_road("time")
        tech_road = self.make_road(time_road, "tech")
        week_road = self.make_road(tech_road, "week")
        weekday_facts_dict = self.get_fact_ranged_kids(
            fact_road=week_road, begin=open_in_week
        )
        weekday_fact_node = None
        for fact in weekday_facts_dict.values():
            weekday_fact_node = fact

        if divisor == 10080:
            return f"every {weekday_fact_node._label} at {x_hregfact.convert1440toReadableTime(min1440=open % 1440)}"
        num_with_letter_ending = x_hregfact.get_number_with_letter_ending(
            num=divisor // 10080
        )
        return f"every {num_with_letter_ending} {weekday_fact_node._label} at {x_hregfact.convert1440toReadableTime(min1440=open % 1440)}"

    def get_partys_metrics(self) -> dict[IdeaID:BalanceLink]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.balancelinks_metrics

    def add_to_idea_agenda_cred_debt(
        self,
        idea_id: IdeaID,
        balanceheir_agenda_cred: float,
        balanceheir_agenda_debt: float,
    ):
        for idea in self._ideas.values():
            if idea.idea_id == idea_id:
                idea._agenda_cred += balanceheir_agenda_cred
                idea._agenda_debt += balanceheir_agenda_debt

    def add_to_idea_agenda_intent_cred_debt(
        self,
        idea_id: IdeaID,
        balanceline_agenda_cred: float,
        balanceline_agenda_debt: float,
    ):
        for idea in self._ideas.values():
            if (
                idea.idea_id == idea_id
                and balanceline_agenda_cred != None
                and balanceline_agenda_debt != None
            ):
                idea._agenda_intent_cred += balanceline_agenda_cred
                idea._agenda_intent_debt += balanceline_agenda_debt

    def add_to_partyunit_agenda_cred_debt(
        self,
        partyunit_party_id: PartyID,
        agenda_cred,
        agenda_debt: float,
        agenda_intent_cred: float,
        agenda_intent_debt: float,
    ):
        for partyunit in self._partys.values():
            if partyunit.party_id == partyunit_party_id:
                partyunit.add_agenda_cred_debt(
                    agenda_cred=agenda_cred,
                    agenda_debt=agenda_debt,
                    agenda_intent_cred=agenda_intent_cred,
                    agenda_intent_debt=agenda_intent_debt,
                )

    def del_partyunit(self, party_id: str):
        self._ideas.pop(party_id)
        self._partys.pop(party_id)

    def add_partyunit(
        self, party_id: PartyID, credor_weight: int = None, debtor_weight: int = None
    ):
        partyunit = partyunit_shop(
            party_id=party_id,
            credor_weight=credor_weight,
            debtor_weight=debtor_weight,
            _road_delimiter=self._road_delimiter,
        )
        self.set_partyunit(partyunit=partyunit)

    def set_partyunit(self, partyunit: PartyUnit):
        if partyunit._road_delimiter != self._road_delimiter:
            partyunit._road_delimiter = self._road_delimiter
        if partyunit._planck != self._planck:
            partyunit._planck = self._planck
        self._partys[partyunit.party_id] = partyunit

        try:
            self._ideas[partyunit.party_id]
        except KeyError:
            partylink = partylink_shop(
                party_id=PartyID(partyunit.party_id), credor_weight=1, debtor_weight=1
            )
            partylinks = {partylink.party_id: partylink}
            idea_unit = ideaunit_shop(
                partyunit.party_id,
                _party_mirror=True,
                _partys=partylinks,
                _road_delimiter=self._road_delimiter,
            )
            self.set_ideaunit(y_ideaunit=idea_unit)

    def party_exists(self, party_id: PartyID) -> bool:
        return self.get_party(party_id) != None

    def edit_partyunit_party_id(
        self,
        old_party_id: PartyID,
        new_party_id: PartyID,
        allow_party_overwite: bool,
        allow_nonsingle_idea_overwrite: bool,
    ):
        # Handle scenarios: some are unacceptable
        old_party_id_credor_weight = self.get_party(old_party_id).credor_weight
        new_party_id_ideaunit = self.get_ideaunit(new_party_id)
        new_party_id_partyunit = self.get_party(new_party_id)
        if not allow_party_overwite and new_party_id_partyunit != None:
            raise InvalidAgendaException(
                f"Party '{old_party_id}' modify to '{new_party_id}' failed since '{new_party_id}' exists."
            )
        elif (
            not allow_nonsingle_idea_overwrite
            and new_party_id_ideaunit != None
            and new_party_id_ideaunit._party_mirror is False
        ):
            raise InvalidAgendaException(
                f"Party '{old_party_id}' modify to '{new_party_id}' failed since non-single idea '{new_party_id}' exists."
            )
        elif (
            allow_nonsingle_idea_overwrite
            and new_party_id_ideaunit != None
            and new_party_id_ideaunit._party_mirror is False
        ):
            self.del_ideaunit(idea_id=new_party_id)
        elif self.party_exists(new_party_id):
            old_party_id_credor_weight += new_party_id_partyunit.credor_weight

        # upsert new partyunit
        self.add_partyunit(
            party_id=new_party_id, credor_weight=old_party_id_credor_weight
        )
        # modify all influenced ideaunits partylinks
        for old_party_idea_id in self.get_party_idea_ids(old_party_id):
            old_party_ideaunit = self.get_ideaunit(old_party_idea_id)
            old_party_ideaunit._shift_partylink(old_party_id, new_party_id)
        self.del_partyunit(party_id=old_party_id)

    def edit_partyunit(
        self, party_id: PartyID, credor_weight: int = None, debtor_weight: int = None
    ):
        if self._partys.get(party_id) is None:
            raise PartyMissingException(f"PartyUnit '{party_id}' does not exist.")
        x_partyunit = self.get_party(party_id)
        if credor_weight != None:
            x_partyunit.set_credor_weight(credor_weight)
        if debtor_weight != None:
            x_partyunit.set_debtor_weight(debtor_weight)
        self.set_partyunit(x_partyunit)

    def get_party(self, party_id: PartyID) -> PartyUnit:
        return self._partys.get(party_id)

    def get_partyunits_party_id_list(self) -> dict[PartyID]:
        party_id_list = list(self._partys.keys())
        party_id_list.append("")
        party_id_dict = {party_id.lower(): party_id for party_id in party_id_list}
        party_id_lowercase_ordered_list = sorted(list(party_id_dict))
        return [
            party_id_dict[party_id_l] for party_id_l in party_id_lowercase_ordered_list
        ]

    def set_ideaunit(
        self,
        y_ideaunit: IdeaUnit,
        create_missing_partys: bool = None,
        replace: bool = True,
        add_partylinks: bool = None,
    ):
        if y_ideaunit._road_delimiter != self._road_delimiter:
            y_ideaunit._road_delimiter = self._road_delimiter
        if replace is None:
            replace = False
        if add_partylinks is None:
            add_partylinks = False
        if (
            self.get_ideaunit(y_ideaunit.idea_id) is None
            or replace
            and not add_partylinks
        ):
            self._ideas[y_ideaunit.idea_id] = y_ideaunit

        if add_partylinks:
            x_ideaunit = self.get_ideaunit(y_ideaunit.idea_id)
            for x_partylink in y_ideaunit._partys.values():
                x_ideaunit.set_partylink(x_partylink)

        if create_missing_partys:
            self._create_missing_partys(partylinks=y_ideaunit._partys)

    def get_ideaunit(self, x_idea_id: IdeaID) -> IdeaUnit:
        return self._ideas.get(x_idea_id)

    def _create_missing_partys(self, partylinks: dict[PartyID:PartyLink]):
        for partylink_x in partylinks.values():
            if self.get_party(partylink_x.party_id) is None:
                self.set_partyunit(
                    partyunit=partyunit_shop(
                        party_id=partylink_x.party_id,
                        credor_weight=partylink_x.credor_weight,
                        debtor_weight=partylink_x.debtor_weight,
                    )
                )

    def del_ideaunit(self, idea_id: IdeaID):
        self._ideas.pop(idea_id)

    def edit_ideaunit_idea_id(
        self, old_idea_id: IdeaID, new_idea_id: IdeaID, allow_idea_overwite: bool
    ):
        if not allow_idea_overwite and self.get_ideaunit(new_idea_id) != None:
            raise InvalidAgendaException(
                f"Idea '{old_idea_id}' modify to '{new_idea_id}' failed since '{new_idea_id}' exists."
            )
        elif self.get_ideaunit(new_idea_id) != None:
            old_ideaunit = self.get_ideaunit(old_idea_id)
            old_ideaunit.set_idea_id(idea_id=new_idea_id)
            self.get_ideaunit(new_idea_id).meld(other_idea=old_ideaunit)
            self.del_ideaunit(idea_id=old_idea_id)
        elif self.get_ideaunit(new_idea_id) is None:
            old_ideaunit = self.get_ideaunit(old_idea_id)
            ideaunit_x = ideaunit_shop(
                new_idea_id, old_ideaunit._party_mirror, old_ideaunit._partys
            )
            self.set_ideaunit(y_ideaunit=ideaunit_x)
            self.del_ideaunit(idea_id=old_idea_id)

        self._edit_balancelinks_idea_id(
            old_idea_id=old_idea_id,
            new_idea_id=new_idea_id,
            allow_idea_overwite=allow_idea_overwite,
        )

    def _edit_balancelinks_idea_id(
        self,
        old_idea_id: IdeaID,
        new_idea_id: IdeaID,
        allow_idea_overwite: bool,
    ):
        for x_fact in self.get_fact_dict().values():
            if (
                x_fact._balancelinks.get(new_idea_id) != None
                and x_fact._balancelinks.get(old_idea_id) != None
            ):
                old_balancelink = x_fact._balancelinks.get(old_idea_id)
                old_balancelink.idea_id = new_idea_id
                x_fact._balancelinks.get(new_idea_id).meld(
                    other_balancelink=old_balancelink,
                    other_meld_strategy="sum",
                    src_meld_strategy="sum",
                )

                x_fact.del_balancelink(idea_id=old_idea_id)
            elif (
                x_fact._balancelinks.get(new_idea_id) is None
                and x_fact._balancelinks.get(old_idea_id) != None
            ):
                old_balancelink = x_fact._balancelinks.get(old_idea_id)
                new_balancelink = balancelink_shop(
                    idea_id=new_idea_id,
                    credor_weight=old_balancelink.credor_weight,
                    debtor_weight=old_balancelink.debtor_weight,
                )
                x_fact.set_balancelink(balancelink=new_balancelink)
                x_fact.del_balancelink(idea_id=old_idea_id)

    def set_time_beliefs(self, open: datetime = None, nigh: datetime = None) -> None:
        open_minutes = self.get_time_min_from_dt(dt=open) if open != None else None
        nigh_minutes = self.get_time_min_from_dt(dt=nigh) if nigh != None else None
        time_road = self.make_l1_road("time")
        minutes_belief = self.make_road(time_road, "jajatime")
        self.set_belief(
            base=minutes_belief,
            pick=minutes_belief,
            open=open_minutes,
            nigh=nigh_minutes,
        )

    def _is_fact_rangeroot(self, fact_road: RoadUnit) -> bool:
        if self._real_id == fact_road:
            raise InvalidAgendaException(
                "its difficult to foresee a scenario where factroot is rangeroot"
            )
        parent_road = get_parent_road(fact_road)
        parent_fact = self.get_fact_obj(parent_road)
        x_fact = self.get_fact_obj(fact_road)
        return x_fact._numeric_road is None and not parent_fact.is_arithmetic()

    def _get_rangeroot_beliefunits(self) -> list[BeliefUnit]:
        return [
            belief
            for belief in self._factroot._beliefunits.values()
            if belief.open != None
            and belief.nigh != None
            and self._is_fact_rangeroot(fact_road=belief.base)
        ]

    def _get_rangeroot_1stlevel_associates(
        self, ranged_beliefunits: list[FactUnit]
    ) -> Lemmas:
        x_lemmas = lemmas_shop()
        # lemma_facts = {}
        for belief in ranged_beliefunits:
            belief_fact = self.get_fact_obj(belief.base)
            for kid in belief_fact._kids.values():
                x_lemmas.eval(x_fact=kid, src_belief=belief, src_fact=belief_fact)

            if belief_fact._range_source_road != None:
                x_lemmas.eval(
                    x_fact=self.get_fact_obj(belief_fact._range_source_road),
                    src_belief=belief,
                    src_fact=belief_fact,
                )
        return x_lemmas

    def _get_lemma_beliefunits(self) -> dict[RoadUnit:BeliefUnit]:
        # get all range-root first level kids and range_source_road
        x_lemmas = self._get_rangeroot_1stlevel_associates(
            self._get_rangeroot_beliefunits()
        )

        # Now get associates (all their descendants and range_source_roads)
        lemma_beliefunits = {}  # belief.base : beliefUnit
        count_x = 0
        while count_x < 10000 and x_lemmas.is_lemmas_evaluated() is False:
            count_x += 1
            if count_x == 9998:
                raise InvalidAgendaException("lemma loop failed")

            y_lemma = x_lemmas.get_unevaluated_lemma()
            lemma_fact = y_lemma.x_fact
            belief_x = y_lemma.calc_belief

            road_x = self.make_road(lemma_fact._parent_road, lemma_fact._label)
            lemma_beliefunits[road_x] = belief_x

            for kid2 in lemma_fact._kids.values():
                x_lemmas.eval(x_fact=kid2, src_belief=belief_x, src_fact=lemma_fact)
            if lemma_fact._range_source_road not in [None, ""]:
                x_lemmas.eval(
                    x_fact=self.get_fact_obj(lemma_fact._range_source_road),
                    src_belief=belief_x,
                    src_fact=lemma_fact,
                )

        return lemma_beliefunits

    def set_belief(
        self,
        base: RoadUnit,
        pick: RoadUnit = None,
        open: float = None,
        nigh: float = None,
        create_missing_facts: bool = None,
    ):
        if pick is None:
            pick = base
        if create_missing_facts:
            self._set_factkid_if_empty(road=base)
            self._set_factkid_if_empty(road=pick)

        self._execute_tree_traverse()
        belief_base_fact = self.get_fact_obj(base)
        x_factroot = self.get_fact_obj(self._real_id)
        x_open = None
        if nigh != None and open is None:
            x_open = x_factroot._beliefunits.get(base).open
        else:
            x_open = open
        x_nigh = None
        if open != None and nigh is None:
            x_nigh = x_factroot._beliefunits.get(base).nigh
        else:
            x_nigh = nigh
        x_beliefunit = beliefunit_shop(base=base, pick=pick, open=x_open, nigh=x_nigh)

        if belief_base_fact.is_arithmetic() is False:
            x_factroot.set_beliefunit(x_beliefunit)

        # if belief's fact no range or is a "range-root" then allow belief to be set
        elif (
            belief_base_fact.is_arithmetic() and self._is_fact_rangeroot(base) is False
        ):
            raise InvalidAgendaException(
                f"Non range-root belief:{base} can only be set by range-root belief"
            )

        elif belief_base_fact.is_arithmetic() and self._is_fact_rangeroot(base):
            # WHEN fact is "range-root" identify any reason.bases that are descendants
            # calculate and set those descendant beliefs
            # example: timeline range (0-, 1.5e9) is range-root
            # example: "timeline,weeks" (spllt 10080) is range-descendant
            # there exists a reason base "timeline,weeks" with premise.need = "timeline,weeks"
            # and (1,2) divisor=2 (every other week)
            #
            # should not set "timeline,weeks" belief, only "timeline" belief and
            # "timeline,weeks" should be set automatica_lly since there exists a reason
            # that has that base.
            x_factroot.set_beliefunit(x_beliefunit)

            # Find all Belief descendants and any range_source_road connections "Lemmas"
            lemmas_dict = self._get_lemma_beliefunits()
            missing_beliefs = self.get_missing_belief_bases().keys()
            x_factroot._apply_any_range_source_road_connections(
                lemmas_dict, missing_beliefs
            )

        self.calc_agenda_metrics()

    def get_belief(self, base: RoadUnit) -> BeliefUnit:
        return self._factroot._beliefunits.get(base)

    def del_belief(self, base: RoadUnit):
        self._factroot.del_beliefunit(base)

    def get_fact_dict(self, problem: bool = None) -> dict[RoadUnit:FactUnit]:
        self.calc_agenda_metrics()
        if not problem:
            return self._fact_dict
        if self._econs_justified is False:
            raise Exception_econs_justified(
                f"Cannot return problem set because _econs_justified={self._econs_justified}."
            )

        return {
            x_fact.get_road(): x_fact
            for x_fact in self._fact_dict.values()
            if x_fact._problem_bool
        }

    def get_tree_metrics(self) -> TreeMetrics:
        tree_metrics = treemetrics_shop()
        tree_metrics.evaluate_node(
            level=self._factroot._level,
            reasons=self._factroot._reasonunits,
            balancelinks=self._factroot._balancelinks,
            uid=self._factroot._uid,
            pledge=self._factroot.pledge,
            fact_road=self._factroot.get_road(),
        )

        x_fact_list = [self._factroot]
        while x_fact_list != []:
            parent_fact = x_fact_list.pop()
            for fact_kid in parent_fact._kids.values():
                self._eval_tree_metrics(
                    parent_fact, fact_kid, tree_metrics, x_fact_list
                )
        return tree_metrics

    def _eval_tree_metrics(self, parent_fact, fact_kid, tree_metrics, x_fact_list):
        fact_kid._level = parent_fact._level + 1
        tree_metrics.evaluate_node(
            level=fact_kid._level,
            reasons=fact_kid._reasonunits,
            balancelinks=fact_kid._balancelinks,
            uid=fact_kid._uid,
            pledge=fact_kid.pledge,
            fact_road=fact_kid.get_road(),
        )
        x_fact_list.append(fact_kid)

    def get_fact_uid_max(self) -> int:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.uid_max

    def set_all_fact_uids_unique(self):
        tree_metrics = self.get_tree_metrics()
        fact_uid_max = tree_metrics.uid_max
        fact_uid_dict = tree_metrics.uid_dict

        for x_fact in self.get_fact_dict().values():
            if x_fact._uid is None or fact_uid_dict.get(x_fact._uid) > 1:
                new_fact_uid_max = fact_uid_max + 1
                self.edit_fact_attr(road=x_fact.get_road(), uid=new_fact_uid_max)
                fact_uid_max = new_fact_uid_max

    def get_fact_count(self) -> int:
        return len(self._fact_dict)

    def get_level_count(self, level) -> int:
        tree_metrics = self.get_tree_metrics()
        level_count = None
        try:
            level_count = tree_metrics.level_count[level]
        except KeyError:
            level_count = 0
        return level_count

    def get_reason_bases(self) -> dict[RoadUnit:int]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.reason_bases

    def get_missing_belief_bases(self) -> dict[RoadUnit:int]:
        tree_metrics = self.get_tree_metrics()
        reason_bases = tree_metrics.reason_bases
        missing_bases = {}
        for base, base_count in reason_bases.items():
            try:
                self._factroot._beliefunits[base]
            except KeyError:
                missing_bases[base] = base_count

        return missing_bases

    def add_l1_fact(
        self,
        fact_kid: FactUnit,
        create_missing_facts: bool = None,
        create_missing_ideas: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        self.add_fact(
            fact_kid=fact_kid,
            parent_road=self._real_id,
            create_missing_facts=create_missing_facts,
            create_missing_ideas=create_missing_ideas,
            adoptees=adoptees,
            bundling=bundling,
            create_missing_ancestors=create_missing_ancestors,
        )

    def add_fact(
        self,
        fact_kid: FactUnit,
        parent_road: RoadUnit,
        create_missing_ideas: bool = None,
        create_missing_facts: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        if RoadNode(fact_kid._label).is_node(self._road_delimiter) is False:
            raise InvalidAgendaException(
                f"add_fact failed because '{fact_kid._label}' is not a RoadNode."
            )

        if self._factroot._label != get_root_node_from_road(
            parent_road, self._road_delimiter
        ):
            raise InvalidAgendaException(
                f"add_fact failed because parent_road '{parent_road}' has an invalid root node"
            )

        fact_kid._road_delimiter = self._road_delimiter
        if fact_kid._agenda_real_id != self._real_id:
            fact_kid._agenda_real_id = self._real_id
        if not create_missing_ideas:
            fact_kid = self._get_filtered_balancelinks_fact(fact_kid)
        fact_kid.set_parent_road(parent_road=parent_road)

        # create any missing facts
        if not create_missing_ancestors and self.fact_exists(parent_road) is False:
            raise InvalidAgendaException(
                f"add_fact failed because '{parent_road}' fact does not exist."
            )
        parent_road_fact = self.get_fact_obj(parent_road, create_missing_ancestors)
        if parent_road_fact._root is False:
            parent_road_fact
        parent_road_fact.add_kid(fact_kid)

        kid_road = self.make_road(parent_road, fact_kid._label)
        if adoptees != None:
            weight_sum = 0
            for adoptee_label in adoptees:
                adoptee_road = self.make_road(parent_road, adoptee_label)
                adoptee_fact = self.get_fact_obj(adoptee_road)
                weight_sum += adoptee_fact._weight
                new_adoptee_parent_road = self.make_road(kid_road, adoptee_label)
                self.add_fact(adoptee_fact, new_adoptee_parent_road)
                self.edit_fact_attr(
                    road=new_adoptee_parent_road, weight=adoptee_fact._weight
                )
                self.del_fact_obj(adoptee_road)

            if bundling:
                self.edit_fact_attr(road=kid_road, weight=weight_sum)

        if create_missing_facts:
            self._create_missing_facts(road=kid_road)
        if create_missing_ideas:
            self._create_missing_ideas_partys(balancelinks=fact_kid._balancelinks)

    def _get_filtered_balancelinks_fact(self, x_fact: FactUnit) -> FactUnit:
        _balancelinks_to_delete = [
            _balancelink_idea_id
            for _balancelink_idea_id in x_fact._balancelinks.keys()
            if self.get_ideaunit(_balancelink_idea_id) is None
        ]
        for _balancelink_idea_id in _balancelinks_to_delete:
            x_fact._balancelinks.pop(_balancelink_idea_id)

        if x_fact._assignedunit != None:
            _suffideas_to_delete = [
                _suffidea_idea_id
                for _suffidea_idea_id in x_fact._assignedunit._suffideas.keys()
                if self.get_ideaunit(_suffidea_idea_id) is None
            ]
            for _suffidea_idea_id in _suffideas_to_delete:
                x_fact._assignedunit.del_suffidea(_suffidea_idea_id)

        return x_fact

    def _create_missing_ideas_partys(self, balancelinks: dict[IdeaID:BalanceLink]):
        for balancelink_x in balancelinks.values():
            if self.get_ideaunit(balancelink_x.idea_id) is None:
                ideaunit_x = ideaunit_shop(idea_id=balancelink_x.idea_id, _partys={})
                self.set_ideaunit(y_ideaunit=ideaunit_x)

    def _create_missing_facts(self, road):
        self.calc_agenda_metrics()
        posted_fact = self.get_fact_obj(road)

        for reason_x in posted_fact._reasonunits.values():
            self._set_factkid_if_empty(road=reason_x.base)
            for premise_x in reason_x.premises.values():
                self._set_factkid_if_empty(road=premise_x.need)
        if posted_fact._range_source_road != None:
            self._set_factkid_if_empty(road=posted_fact._range_source_road)
        if posted_fact._numeric_road != None:
            self._set_factkid_if_empty(road=posted_fact._numeric_road)

    def _set_factkid_if_empty(self, road: RoadUnit):
        if self.fact_exists(road) is False:
            self.add_fact(
                factunit_shop(get_terminus_node(road, self._road_delimiter)),
                parent_road=get_parent_road(road),
            )

    def del_fact_obj(self, road: RoadUnit, del_children: bool = True):
        if road == self._factroot.get_road():
            raise InvalidAgendaException("Factroot cannot be deleted")
        parent_road = get_parent_road(road)
        if self.fact_exists(road):
            if not del_children:
                self._shift_fact_kids(x_road=road)
            parent_fact = self.get_fact_obj(parent_road)
            parent_fact.del_kid(get_terminus_node(road, self._road_delimiter))
        self.calc_agenda_metrics()

    def _shift_fact_kids(self, x_road: RoadUnit):
        parent_road = get_parent_road(x_road)
        d_temp_fact = self.get_fact_obj(x_road)
        for kid in d_temp_fact._kids.values():
            self.add_fact(kid, parent_road=parent_road)

    def set_owner_id(self, new_owner_id):
        self._owner_id = new_owner_id

    def edit_fact_label(
        self,
        old_road: RoadUnit,
        new_label: RoadNode,
    ):
        if self._road_delimiter in new_label:
            raise InvalidLabelException(
                f"Cannot modify '{old_road}' because new_label {new_label} contains delimiter {self._road_delimiter}"
            )
        if self.fact_exists(old_road) is False:
            raise InvalidAgendaException(f"Fact {old_road=} does not exist")

        parent_road = get_parent_road(road=old_road)
        new_road = (
            self.make_road(new_label)
            if parent_road == ""
            else self.make_road(parent_road, new_label)
        )
        if old_road != new_road:
            if parent_road == "":
                self._factroot.set_fact_label(new_label)
            else:
                self._non_root_fact_label_edit(old_road, new_label, parent_road)
            self._factroot_find_replace_road(old_road=old_road, new_road=new_road)
            self._factroot._beliefunits = find_replace_road_key_dict(
                dict_x=self._factroot._beliefunits,
                old_road=old_road,
                new_road=new_road,
            )

    def _non_root_fact_label_edit(
        self, old_road: RoadUnit, new_label: RoadNode, parent_road: RoadUnit
    ):
        x_fact = self.get_fact_obj(old_road)
        x_fact.set_fact_label(new_label)
        x_fact._parent_road = parent_road
        fact_parent = self.get_fact_obj(get_parent_road(old_road))
        fact_parent._kids.pop(get_terminus_node(old_road, self._road_delimiter))
        fact_parent._kids[x_fact._label] = x_fact

    def _factroot_find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        self._factroot.find_replace_road(old_road=old_road, new_road=new_road)

        fact_iter_list = [self._factroot]
        while fact_iter_list != []:
            listed_fact = fact_iter_list.pop()
            # put all fact_children in fact list
            if listed_fact._kids != None:
                for fact_kid in listed_fact._kids.values():
                    fact_iter_list.append(fact_kid)
                    if is_sub_road(
                        ref_road=fact_kid._parent_road,
                        sub_road=old_road,
                    ):
                        fact_kid._parent_road = rebuild_road(
                            subj_road=fact_kid._parent_road,
                            old_road=old_road,
                            new_road=new_road,
                        )
                    fact_kid.find_replace_road(old_road=old_road, new_road=new_road)

    def _set_factattrfilter_premise_ranges(self, x_factattrfilter: FactAttrFilter):
        premise_fact = self.get_fact_obj(x_factattrfilter.get_premise_need())
        x_factattrfilter.set_premise_range_attributes_influenced_by_premise_fact(
            premise_open=premise_fact._begin,
            premise_nigh=premise_fact._close,
            # premise_numor=premise_fact.anc_numor,
            premise_denom=premise_fact._denom,
            # anc_reest=premise_fact.anc_reest,
        )

    def _set_factattrfilter_begin_close(
        self, factattrfilter: FactAttrFilter, fact_road: RoadUnit
    ) -> set[float, float]:
        x_iaf = factattrfilter
        anc_roads = get_ancestor_roads(road=fact_road)
        if (
            x_iaf.addin != None
            or x_iaf.numor != None
            or x_iaf.denom != None
            or x_iaf.reest != None
        ) and len(anc_roads) == 1:
            raise InvalidAgendaException("Root Fact cannot have numor denom reest.")
        parent_road = self._real_id if len(anc_roads) == 1 else anc_roads[1]

        parent_has_range = None
        parent_fact = self.get_fact_obj(parent_road)
        parent_begin = parent_fact._begin
        parent_close = parent_fact._close
        parent_has_range = parent_begin is not None and parent_close is not None

        numeric_begin = None
        numeric_close = None
        numeric_range = None
        if x_iaf.numeric_road != None:
            numeric_fact = self.get_fact_obj(x_iaf.numeric_road)
            numeric_begin = numeric_fact._begin
            numeric_close = numeric_fact._close
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
                "Fact has begin-close range parent, cannot have numeric_road"
            )
        elif not parent_has_range and not numeric_range and x_iaf.numor != None:
            raise InvalidAgendaException(
                f"Fact cannot edit numor={x_iaf.numor}/denom/reest of '{fact_road}' if parent '{parent_road}' or factunit._numeric_road does not have begin/close range"
            )
        factattrfilter.begin = x_begin
        factattrfilter.close = x_close

    def _transform_begin_close(
        self,
        reest,
        begin: float,
        close: float,
        numor: float,
        denom: float,
        parent_has_range: float,
        parent_begin: float,
        parent_close: float,
        numeric_range: float,
        numeric_begin: float,
        numeric_close: float,
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

    def edit_reason(
        self,
        road: RoadUnit,
        reason_base: RoadUnit = None,
        reason_premise: RoadUnit = None,
        reason_premise_open: float = None,
        reason_premise_nigh: float = None,
        reason_premise_divisor: int = None,
    ):
        self.edit_fact_attr(
            road=road,
            reason_base=reason_base,
            reason_premise=reason_premise,
            reason_premise_open=reason_premise_open,
            reason_premise_nigh=reason_premise_nigh,
            reason_premise_divisor=reason_premise_divisor,
        )

    def edit_fact_attr(
        self,
        road: RoadUnit,
        weight: int = None,
        uid: int = None,
        reason: ReasonUnit = None,
        reason_base: RoadUnit = None,
        reason_premise: RoadUnit = None,
        reason_premise_open: float = None,
        reason_premise_nigh: float = None,
        reason_premise_divisor: int = None,
        reason_del_premise_base: RoadUnit = None,
        reason_del_premise_need: RoadUnit = None,
        reason_suff_fact_active: str = None,
        assignedunit: AssignedUnit = None,
        healerhold: HealerHold = None,
        begin: float = None,
        close: float = None,
        addin: float = None,
        numor: float = None,
        denom: float = None,
        reest: bool = None,
        numeric_road: RoadUnit = None,
        range_source_road: float = None,
        pledge: bool = None,
        beliefunit: BeliefUnit = None,
        descendant_pledge_count: int = None,
        all_party_cred: bool = None,
        all_party_debt: bool = None,
        balancelink: BalanceLink = None,
        balancelink_del: IdeaID = None,
        is_expanded: bool = None,
        meld_strategy: MeldStrategy = None,
        problem_bool: bool = None,
    ):
        if healerhold != None:
            for x_idea_id in healerhold._idea_ids:
                if self._ideas.get(x_idea_id) is None:
                    raise healerhold_idea_id_Exception(
                        f"Fact cannot edit healerhold because idea_id '{x_idea_id}' does not exist as idea in Agenda"
                    )

        x_factattrfilter = factattrfilter_shop(
            weight=weight,
            uid=uid,
            reason=reason,
            reason_base=reason_base,
            reason_premise=reason_premise,
            reason_premise_open=reason_premise_open,
            reason_premise_nigh=reason_premise_nigh,
            reason_premise_divisor=reason_premise_divisor,
            reason_del_premise_base=reason_del_premise_base,
            reason_del_premise_need=reason_del_premise_need,
            reason_suff_fact_active=reason_suff_fact_active,
            assignedunit=assignedunit,
            healerhold=healerhold,
            begin=begin,
            close=close,
            addin=addin,
            numor=numor,
            denom=denom,
            reest=reest,
            numeric_road=numeric_road,
            range_source_road=range_source_road,
            descendant_pledge_count=descendant_pledge_count,
            all_party_cred=all_party_cred,
            all_party_debt=all_party_debt,
            balancelink=balancelink,
            balancelink_del=balancelink_del,
            is_expanded=is_expanded,
            pledge=pledge,
            beliefunit=beliefunit,
            meld_strategy=meld_strategy,
            problem_bool=problem_bool,
        )
        if x_factattrfilter.has_numeric_attrs():
            self._set_factattrfilter_begin_close(x_factattrfilter, road)
        if x_factattrfilter.has_reason_premise():
            self._set_factattrfilter_premise_ranges(x_factattrfilter)
        x_fact = self.get_fact_obj(road)
        x_fact._set_fact_attr(fact_attr=x_factattrfilter)

        # deleting or setting a balancelink reqquires a tree traverse to correctly set balanceheirs and balancelines
        if balancelink_del != None or balancelink != None:
            self.calc_agenda_metrics()

    def get_intent_dict(
        self,
        base: RoadUnit = None,
        intent_enterprise: bool = True,
        intent_state: bool = True,
    ) -> dict[RoadUnit:FactUnit]:
        self.calc_agenda_metrics()
        return {
            x_fact.get_road(): x_fact
            for x_fact in self._fact_dict.values()
            if x_fact.is_intent_item(necessary_base=base)
        }

    def get_all_pledges(self) -> dict[RoadUnit:FactUnit]:
        self.calc_agenda_metrics()
        all_facts = self._fact_dict.values()
        return {x_fact.get_road(): x_fact for x_fact in all_facts if x_fact.pledge}

    def set_intent_task_complete(self, task_road: RoadUnit, base: RoadUnit):
        pledge_item = self.get_fact_obj(task_road)
        pledge_item.set_beliefunit_to_complete(self._factroot._beliefunits[base])

    def is_partyunits_credor_weight_sum_correct(self) -> bool:
        x_sum = self.get_partyunits_credor_weight_sum()
        return x_sum in (0, self._party_credor_pool) or self._party_credor_pool is None

    def is_partyunits_debtor_weight_sum_correct(self) -> bool:
        x_sum = self.get_partyunits_debtor_weight_sum()
        return self._party_debtor_pool is None or x_sum in (self._party_debtor_pool, 0)

    def get_partyunits_credor_weight_sum(self) -> float:
        return sum(partyunit.get_credor_weight() for partyunit in self._partys.values())

    def get_partyunits_debtor_weight_sum(self) -> float:
        return sum(partyunit.get_debtor_weight() for partyunit in self._partys.values())

    def _add_to_partyunits_agenda_cred_debt(self, fact_agenda_importance: float):
        sum_partyunit_credor_weight = self.get_partyunits_credor_weight_sum()
        sum_partyunit_debtor_weight = self.get_partyunits_debtor_weight_sum()

        for x_partyunit in self._partys.values():
            au_agenda_cred = (
                fact_agenda_importance * x_partyunit.get_credor_weight()
            ) / sum_partyunit_credor_weight

            au_agenda_debt = (
                fact_agenda_importance * x_partyunit.get_debtor_weight()
            ) / sum_partyunit_debtor_weight

            x_partyunit.add_agenda_cred_debt(
                agenda_cred=au_agenda_cred,
                agenda_debt=au_agenda_debt,
                agenda_intent_cred=0,
                agenda_intent_debt=0,
            )

    def _add_to_partyunits_agenda_intent_cred_debt(self, fact_agenda_importance: float):
        sum_partyunit_credor_weight = self.get_partyunits_credor_weight_sum()
        sum_partyunit_debtor_weight = self.get_partyunits_debtor_weight_sum()

        for x_partyunit in self._partys.values():
            au_agenda_intent_cred = (
                fact_agenda_importance * x_partyunit.get_credor_weight()
            ) / sum_partyunit_credor_weight

            au_agenda_intent_debt = (
                fact_agenda_importance * x_partyunit.get_debtor_weight()
            ) / sum_partyunit_debtor_weight

            x_partyunit.add_agenda_cred_debt(
                agenda_cred=0,
                agenda_debt=0,
                agenda_intent_cred=au_agenda_intent_cred,
                agenda_intent_debt=au_agenda_intent_debt,
            )

    def _set_partyunits_agenda_intent_importance(self, agenda_intent_importance: float):
        sum_partyunit_credor_weight = self.get_partyunits_credor_weight_sum()
        sum_partyunit_debtor_weight = self.get_partyunits_debtor_weight_sum()

        for x_partyunit in self._partys.values():
            au_agenda_intent_cred = (
                agenda_intent_importance * x_partyunit.get_credor_weight()
            ) / sum_partyunit_credor_weight

            au_agenda_intent_debt = (
                agenda_intent_importance * x_partyunit.get_debtor_weight()
            ) / sum_partyunit_debtor_weight

            x_partyunit.add_agenda_intent_cred_debt(
                agenda_intent_cred=au_agenda_intent_cred,
                agenda_intent_debt=au_agenda_intent_debt,
            )

    def _reset_ideaunits_agenda_cred_debt(self):
        for balancelink_obj in self._ideas.values():
            balancelink_obj.reset_agenda_cred_debt()

    def _set_ideaunits_agenda_importance(self, balanceheirs: dict[IdeaID:BalanceLink]):
        for balancelink_obj in balanceheirs.values():
            self.add_to_idea_agenda_cred_debt(
                idea_id=balancelink_obj.idea_id,
                balanceheir_agenda_cred=balancelink_obj._agenda_cred,
                balanceheir_agenda_debt=balancelink_obj._agenda_debt,
            )

    def _allot_agenda_intent_importance(self):
        for fact in self._fact_dict.values():
            # If there are no balancelines associated with fact
            # allot agenda_importance via general partyunit
            # cred ratio and debt ratio
            # if fact.is_intent_item() and fact._balancelines == {}:
            if fact.is_intent_item():
                if fact._balancelines == {}:
                    self._add_to_partyunits_agenda_intent_cred_debt(
                        fact._agenda_importance
                    )
                else:
                    for x_balanceline in fact._balancelines.values():
                        self.add_to_idea_agenda_intent_cred_debt(
                            idea_id=x_balanceline.idea_id,
                            balanceline_agenda_cred=x_balanceline._agenda_cred,
                            balanceline_agenda_debt=x_balanceline._agenda_debt,
                        )

    def _allot_ideas_agenda_importance(self):
        for idea_obj in self._ideas.values():
            idea_obj._set_partylink_agenda_cred_debt()
            for partylink in idea_obj._partys.values():
                self.add_to_partyunit_agenda_cred_debt(
                    partyunit_party_id=partylink.party_id,
                    agenda_cred=partylink._agenda_cred,
                    agenda_debt=partylink._agenda_debt,
                    agenda_intent_cred=partylink._agenda_intent_cred,
                    agenda_intent_debt=partylink._agenda_intent_debt,
                )

    def _set_agenda_intent_ratio_cred_debt(self):
        agenda_intent_ratio_cred_sum = 0
        agenda_intent_ratio_debt_sum = 0

        for x_partyunit in self._partys.values():
            agenda_intent_ratio_cred_sum += x_partyunit._agenda_intent_cred
            agenda_intent_ratio_debt_sum += x_partyunit._agenda_intent_debt

        for x_partyunit in self._partys.values():
            x_partyunit.set_agenda_intent_ratio_cred_debt(
                agenda_intent_ratio_cred_sum=agenda_intent_ratio_cred_sum,
                agenda_intent_ratio_debt_sum=agenda_intent_ratio_debt_sum,
                agenda_partyunit_total_credor_weight=self.get_partyunits_credor_weight_sum(),
                agenda_partyunit_total_debtor_weight=self.get_partyunits_debtor_weight_sum(),
            )

    def get_party_idea_ids(self, party_id: PartyID) -> list[IdeaID]:
        return [
            x_ideaunit.idea_id
            for x_ideaunit in self._ideas.values()
            if x_ideaunit.partylink_exists(party_id)
        ]

    def _reset_partyunit_agenda_cred_debt(self):
        for partyunit in self._partys.values():
            partyunit.reset_agenda_cred_debt()

    def fact_exists(self, road: RoadUnit) -> bool:
        if road is None:
            return False
        root_road_label = get_root_node_from_road(road, delimiter=self._road_delimiter)
        if root_road_label != self._factroot._label:
            return False

        nodes = get_all_road_nodes(road, delimiter=self._road_delimiter)
        root_road_label = nodes.pop(0)
        if nodes == []:
            return True

        fact_label = nodes.pop(0)
        x_fact = self._factroot.get_kid(fact_label)
        if x_fact is None:
            return False
        while nodes != []:
            fact_label = nodes.pop(0)
            x_fact = x_fact.get_kid(fact_label)
            if x_fact is None:
                return False
        return True

    def get_fact_obj(self, road: RoadUnit, if_missing_create: bool = False) -> FactUnit:
        if road is None:
            raise InvalidAgendaException("get_fact_obj received road=None")
        if self.fact_exists(road) is False and not if_missing_create:
            raise InvalidAgendaException(f"get_fact_obj failed. no item at '{road}'")
        roadnodes = get_all_road_nodes(road, delimiter=self._road_delimiter)
        if len(roadnodes) == 1:
            return self._factroot

        roadnodes.pop(0)
        fact_label = roadnodes.pop(0)
        x_fact = self._factroot.get_kid(fact_label, if_missing_create)
        while roadnodes != []:
            x_fact = x_fact.get_kid(roadnodes.pop(0), if_missing_create)

        return x_fact

    def get_fact_ranged_kids(
        self, fact_road: str, begin: float = None, close: float = None
    ) -> dict[FactUnit]:
        parent_fact = self.get_fact_obj(fact_road)
        if begin is None and close is None:
            begin = parent_fact._begin
            close = parent_fact._close
        elif begin != None and close is None:
            close = begin

        fact_list = parent_fact.get_kids_in_range(begin=begin, close=close)
        return {x_fact._label: x_fact for x_fact in fact_list}

    def _set_ancestors_metrics(self, road: RoadUnit, econ_exceptions: bool = False):
        task_count = 0
        child_balancelines = None
        idea_everyone = None
        ancestor_roads = get_ancestor_roads(road=road)
        econ_justified_by_problem = True
        healerhold_count = 0

        while ancestor_roads != []:
            youngest_road = ancestor_roads.pop(0)
            # _set_non_root_ancestor_metrics(youngest_road, task_count, idea_everyone)
            x_fact_obj = self.get_fact_obj(road=youngest_road)
            x_fact_obj.add_to_descendant_pledge_count(task_count)
            if x_fact_obj.is_kidless():
                x_fact_obj.set_kidless_balancelines()
                child_balancelines = x_fact_obj._balancelines
            else:
                x_fact_obj.set_balancelines(child_balancelines=child_balancelines)

            if x_fact_obj._task:
                task_count += 1

            if (
                idea_everyone != False
                and x_fact_obj._all_party_cred != False
                and x_fact_obj._all_party_debt != False
                and x_fact_obj._balanceheirs != {}
            ) or (
                idea_everyone != False
                and x_fact_obj._all_party_cred is False
                and x_fact_obj._all_party_debt is False
            ):
                idea_everyone = False
            elif idea_everyone != False:
                idea_everyone = True
            x_fact_obj._all_party_cred = idea_everyone
            x_fact_obj._all_party_debt = idea_everyone

            if x_fact_obj._healerhold.any_idea_id_exists():
                econ_justified_by_problem = False
                healerhold_count += 1
                self._sum_healerhold_importance += x_fact_obj._agenda_importance
            if x_fact_obj._problem_bool:
                econ_justified_by_problem = True

        if econ_justified_by_problem is False or healerhold_count > 1:
            if econ_exceptions:
                raise Exception_econs_justified(
                    f"FactUnit '{road}' cannot sponsor ancestor econs."
                )
            self._econs_justified = False

    def _set_root_attributes(self, econ_exceptions: bool):
        x_factroot = self._factroot
        x_factroot._level = 0
        x_factroot.set_parent_road(parent_road="")
        x_factroot.set_factroot_inherit_reasonheirs()
        x_factroot.set_assignedheir(parent_assignheir=None, agenda_ideas=self._ideas)
        x_factroot.set_beliefheirs(beliefs=self._factroot._beliefunits)
        x_factroot.inherit_balanceheirs()
        x_factroot.clear_balancelines()
        x_factroot._weight = 1
        x_factroot.set_kids_total_weight()
        x_factroot.set_sibling_total_weight(1)
        x_factroot.set_active(
            tree_traverse_count=self._tree_traverse_count,
            agenda_ideaunits=self._ideas,
            agenda_owner_id=self._owner_id,
        )
        x_factroot.set_agenda_importance(fund_onset_x=0, parent_fund_cease=1)
        x_factroot.set_balanceheirs_agenda_cred_debt()
        x_factroot.set_ancestor_pledge_count(0, False)
        x_factroot.clear_descendant_pledge_count()
        x_factroot.clear_all_party_cred_debt()
        x_factroot.pledge = False

        if x_factroot.is_kidless():
            self._set_ancestors_metrics(self._factroot.get_road(), econ_exceptions)
            self._allot_agenda_importance(fact=self._factroot)

    def _set_kids_attributes(
        self,
        fact_kid: FactUnit,
        fund_onset: float,
        parent_fund_cease: float,
        parent_fact: FactUnit,
        econ_exceptions: bool,
    ):
        fact_kid.set_level(parent_level=parent_fact._level)
        fact_kid.set_parent_road(parent_fact.get_road())
        fact_kid.set_beliefheirs(beliefs=parent_fact._beliefheirs)
        fact_kid.set_reasonheirs(self._fact_dict, parent_fact._reasonheirs)
        fact_kid.set_assignedheir(parent_fact._assignedheir, self._ideas)
        fact_kid.inherit_balanceheirs(parent_fact._balanceheirs)
        fact_kid.clear_balancelines()
        fact_kid.set_active(
            tree_traverse_count=self._tree_traverse_count,
            agenda_ideaunits=self._ideas,
            agenda_owner_id=self._owner_id,
        )
        fact_kid.set_sibling_total_weight(parent_fact._kids_total_weight)
        fact_kid.set_agenda_importance(
            fund_onset_x=fund_onset,
            parent_agenda_importance=parent_fact._agenda_importance,
            parent_fund_cease=parent_fund_cease,
        )
        fact_kid.set_ancestor_pledge_count(
            parent_fact._ancestor_pledge_count, parent_fact.pledge
        )
        fact_kid.clear_descendant_pledge_count()
        fact_kid.clear_all_party_cred_debt()

        if fact_kid.is_kidless():
            # set fact's ancestor metrics using agenda root as common reference
            self._set_ancestors_metrics(fact_kid.get_road(), econ_exceptions)
            self._allot_agenda_importance(fact=fact_kid)

    def _allot_agenda_importance(self, fact: FactUnit):
        # TODO manage situations where balanceheir.credor_weight is None for all balanceheirs
        # TODO manage situations where balanceheir.debtor_weight is None for all balanceheirs
        if fact.is_balanceheirless() is False:
            self._set_ideaunits_agenda_importance(fact._balanceheirs)
        elif fact.is_balanceheirless():
            self._add_to_partyunits_agenda_cred_debt(fact._agenda_importance)

    def get_agenda_importance(
        self, parent_agenda_importance: float, weight: int, sibling_total_weight: int
    ) -> float:
        sibling_ratio = weight / sibling_total_weight
        return parent_agenda_importance * sibling_ratio

    def _set_tree_traverse_starting_point(self):
        self._rational = False
        self._tree_traverse_count = 0
        self._fact_dict = {self._factroot.get_road(): self._factroot}

    def _clear_agenda_base_metrics(self):
        self._econs_justified = True
        self._econs_buildable = False
        self._sum_healerhold_importance = 0
        self._econ_dict = {}
        self._healers_dict = {}

    def calc_agenda_metrics(self, econ_exceptions: bool = False):
        self._set_tree_traverse_starting_point()
        max_count = self._max_tree_traverse

        while not self._rational and self._tree_traverse_count < max_count:
            self._clear_agenda_base_metrics()
            self._execute_tree_traverse(econ_exceptions)
            self._check_if_any_fact_active_status_has_altered()
            self._tree_traverse_count += 1
        self._after_all_tree_traverses_set_cred_debt()
        self._after_all_tree_traverses_set_healerhold_importance()

    def _execute_tree_traverse(self, econ_exceptions: bool = False):
        self._pre_tree_traverse_cred_debt_reset()
        self._set_root_attributes(econ_exceptions)

        fund_onset = self._factroot._agenda_fund_onset
        parent_fund_cease = self._factroot._agenda_fund_cease

        cache_fact_list = []
        for fact_kid in self._factroot._kids.values():
            self._set_kids_attributes(
                fact_kid=fact_kid,
                fund_onset=fund_onset,
                parent_fund_cease=parent_fund_cease,
                parent_fact=self._factroot,
                econ_exceptions=econ_exceptions,
            )
            cache_fact_list.append(fact_kid)
            fund_onset += fact_kid._agenda_importance

        # no function recursion, recursion by iterateing over list that can be added to by iterations
        while cache_fact_list != []:
            parent_fact = cache_fact_list.pop()
            if self._tree_traverse_count == 0:
                self._fact_dict[parent_fact.get_road()] = parent_fact

            if parent_fact._kids != None:
                fund_onset = parent_fact._agenda_fund_onset
                parent_fund_cease = parent_fact._agenda_fund_cease
                for fact_kid in parent_fact._kids.values():
                    self._set_kids_attributes(
                        fact_kid=fact_kid,
                        fund_onset=fund_onset,
                        parent_fund_cease=parent_fund_cease,
                        parent_fact=parent_fact,
                        econ_exceptions=econ_exceptions,
                    )
                    cache_fact_list.append(fact_kid)
                    fund_onset += fact_kid._agenda_importance

    def _check_if_any_fact_active_status_has_altered(self):
        any_fact_active_status_has_altered = False
        for fact in self._fact_dict.values():
            if fact._active_hx.get(self._tree_traverse_count) != None:
                any_fact_active_status_has_altered = True

        if any_fact_active_status_has_altered is False:
            self._rational = True

    def _after_all_tree_traverses_set_cred_debt(self):
        self._allot_agenda_intent_importance()
        self._allot_ideas_agenda_importance()
        self._set_agenda_intent_ratio_cred_debt()

    def _after_all_tree_traverses_set_healerhold_importance(self):
        self._set_econ_dict()
        self._healers_dict = self._get_healers_dict()
        self._econs_buildable = self._get_buildable_econs()

    def _set_econ_dict(self):
        if self._econs_justified is False:
            self._sum_healerhold_importance = 0
        for x_fact in self._fact_dict.values():
            if self._sum_healerhold_importance == 0:
                x_fact._healerhold_importance = 0
            else:
                x_sum = self._sum_healerhold_importance
                x_fact._healerhold_importance = x_fact._agenda_importance / x_sum
            if self._econs_justified and x_fact._healerhold.any_idea_id_exists():
                self._econ_dict[x_fact.get_road()] = x_fact

    def _get_healers_dict(self) -> dict[HealerID : dict[RoadUnit:FactUnit]]:
        _healers_dict = {}
        for x_econ_road, x_econ_fact in self._econ_dict.items():
            for x_idea_id in x_econ_fact._healerhold._idea_ids:
                x_ideaunit = self.get_ideaunit(x_idea_id)
                for x_party_id in x_ideaunit._partys.keys():
                    if _healers_dict.get(x_party_id) is None:
                        _healers_dict[x_party_id] = {x_econ_road: x_econ_fact}
                    else:
                        healer_dict = _healers_dict.get(x_party_id)
                        healer_dict[x_econ_road] = x_econ_fact
        return _healers_dict

    def _get_buildable_econs(self) -> bool:
        return all(
            is_roadunit_convertible_to_path(econ_road, self._road_delimiter) != False
            for econ_road in self._econ_dict.keys()
        )

    def _pre_tree_traverse_cred_debt_reset(self):
        if self.is_partyunits_credor_weight_sum_correct() is False:
            raise PartyUnitsCredorDebtorSumException(
                f"'{self._owner_id}' is_partyunits_credor_weight_sum_correct is False. _party_credor_pool={self._party_credor_pool}. partyunits_credor_weight_sum={self.get_partyunits_credor_weight_sum()}"
            )
        if self.is_partyunits_debtor_weight_sum_correct() is False:
            raise PartyUnitsCredorDebtorSumException(
                f"'{self._owner_id}' is_partyunits_debtor_weight_sum_correct is False. _party_debtor_pool={self._party_debtor_pool}. partyunits_debtor_weight_sum={self.get_partyunits_debtor_weight_sum()}"
            )
        self._reset_ideaunits_agenda_cred_debt()
        self._reset_ideaunits_agenda_cred_debt()
        self._reset_partyunit_agenda_cred_debt()

    def get_heir_road_list(self, x_road: RoadUnit) -> list[RoadUnit]:
        road_list = self.get_fact_tree_ordered_road_list()
        return [fact_road for fact_road in road_list if is_sub_road(fact_road, x_road)]

    def get_fact_tree_ordered_road_list(
        self, no_range_descendants: bool = False
    ) -> list[RoadUnit]:
        fact_list = list(self.get_fact_dict().values())
        node_dict = {fact.get_road().lower(): fact.get_road() for fact in fact_list}
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
                    if self._factroot._begin is None and self._factroot._close is None:
                        list_x.append(road)
                else:
                    parent_fact = self.get_fact_obj(road=anc_list[1])
                    if parent_fact._begin is None and parent_fact._close is None:
                        list_x.append(road)

        return list_x

    def get_beliefunits_dict(self) -> dict[str:str]:
        x_dict = {}
        if self._factroot._beliefunits != None:
            for belief_road, belief_obj in self._factroot._beliefunits.items():
                x_dict[belief_road] = belief_obj.get_dict()
        return x_dict

    def get_partys_dict(self, all_attrs: bool = False) -> dict[str:str]:
        x_dict = {}
        if self._partys != None:
            for party_id, party_obj in self._partys.items():
                x_dict[party_id] = party_obj.get_dict(all_attrs)
        return x_dict

    def get_ideaunits_dict(self) -> dict[str:str]:
        return {
            idea_idea_id: idea_obj.get_dict()
            for idea_idea_id, idea_obj in self._ideas.items()
            if idea_obj._party_mirror is False
        }

    def get_dict(self) -> dict[str:str]:
        x_dict = {
            "_partys": self.get_partys_dict(),
            "_ideas": self.get_ideaunits_dict(),
            "_originunit": self._originunit.get_dict(),
            "_weight": self._weight,
            "_planck": self._planck,
            "_penny": self._penny,
            "_owner_id": self._owner_id,
            "_real_id": self._real_id,
            "_max_tree_traverse": self._max_tree_traverse,
            "_road_delimiter": self._road_delimiter,
            "_factroot": self._factroot.get_dict(),
        }
        if self._party_credor_pool != None:
            x_dict["_party_credor_pool"] = self._party_credor_pool
        if self._party_debtor_pool != None:
            x_dict["_party_debtor_pool"] = self._party_debtor_pool
        if self._meld_strategy != get_meld_default():
            x_dict["_meld_strategy"] = self._meld_strategy
        if self._last_atom_id != None:
            x_dict["_last_atom_id"] = self._last_atom_id

        return x_dict

    def get_json(self) -> str:
        x_dict = self.get_dict()
        return get_json_from_dict(dict_x=x_dict)

    def set_time_hreg_facts(self, c400_count: int):
        x_hregfact = HregFact(self._road_delimiter)
        factbase_list = x_hregfact._get_time_hreg_src_fact(c400_count=c400_count)
        while len(factbase_list) != 0:
            yb = factbase_list.pop(0)
            range_source_road_x = None
            if yb.sr != None:
                range_source_road_x = self.make_l1_road(yb.sr)

            x_fact = factunit_shop(
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
            road_x = self.make_l1_road(yb.rr)
            self.add_fact(x_fact, parent_road=road_x)

            numeric_road_x = None
            if yb.nr != None:
                numeric_road_x = self.make_l1_road(yb.nr)
                self.edit_fact_attr(
                    road=self.make_road(road_x, yb.n), numeric_road=numeric_road_x
                )
            if yb.a != None:
                self.edit_fact_attr(
                    road=self.make_road(road_x, yb.n),
                    addin=yb.a,
                    denom=yb.md,
                    numor=yb.mn,
                )

        self.calc_agenda_metrics()

    def get_agenda4party(self, party_id: PartyID, beliefs: dict[RoadUnit:BeliefCore]):
        self.calc_agenda_metrics()
        agenda4party = agendaunit_shop(_owner_id=party_id)
        agenda4party._factroot._agenda_importance = self._factroot._agenda_importance
        # get party's partys: partyzone

        # get partyzone ideas
        party_ideas = self.get_party_idea_ids(party_id=party_id)

        # set agenda4party by traversing the fact tree and selecting associated ideas
        # set root
        not_included_agenda_importance = 0
        agenda4party._factroot.clear_kids()
        for ykx in self._factroot._kids.values():
            y4a_included = any(
                idea_ancestor.idea_id in party_ideas
                for idea_ancestor in ykx._balancelines.values()
            )

            if y4a_included:
                y4a_new = factunit_shop(
                    _label=ykx._label,
                    _agenda_importance=ykx._agenda_importance,
                    _reasonunits=ykx._reasonunits,
                    _balancelinks=ykx._balancelinks,
                    _begin=ykx._begin,
                    _close=ykx._close,
                    pledge=ykx.pledge,
                    _task=ykx._task,
                )
                agenda4party._factroot._kids[ykx._label] = y4a_new
            else:
                not_included_agenda_importance += ykx._agenda_importance

        if not_included_agenda_importance > 0:
            y4a_other = factunit_shop(
                _label="__other__",
                _agenda_importance=not_included_agenda_importance,
            )
            agenda4party._factroot._kids[y4a_other._label] = y4a_other

        return agenda4party

    def set_dominate_pledge_fact(self, fact_kid: FactUnit):
        fact_kid.pledge = True
        self.add_fact(
            fact_kid=fact_kid,
            parent_road=self.make_road(fact_kid._parent_road),
            create_missing_ideas=True,
            create_missing_facts=True,
        )

    def get_fact_list_without_factroot(self) -> list[FactUnit]:
        self.calc_agenda_metrics()
        x_list = list(self._fact_dict.values())
        x_list.pop(0)
        return x_list

    def set_meld_strategy(self, x_meld_strategy: MeldStrategy):
        self._meld_strategy = validate_meld_strategy(x_meld_strategy)

    def meld(
        self, other_agenda, party_weight: float = None, ignore_partyunits: bool = False
    ):
        self._meld_ideas(other_agenda)
        if not ignore_partyunits:
            self._meld_partys(other_agenda)
        self._meld_facts(other_agenda, party_weight)
        self._meld_beliefs(other_agenda)
        self._weight = get_meld_weight(
            src_weight=self._weight,
            src_meld_strategy="default",
            other_weight=other_agenda._weight,
            other_meld_strategy="default",
        )
        self._meld_originlinks(other_agenda._owner_id, party_weight)

    def _meld_facts(self, other_agenda, party_weight: float):
        # meld factroot
        self._factroot.meld(other_fact=other_agenda._factroot, _factroot=True)

        # meld all other facts
        party_id = other_agenda._owner_id
        o_fact_list = other_agenda.get_fact_list_without_factroot()
        for o_fact in o_fact_list:
            o_road = road_validate(
                self.make_road(o_fact._parent_road, o_fact._label),
                self._road_delimiter,
                self._real_id,
            )
            try:
                main_fact = self.get_fact_obj(o_road)
                main_fact.meld(o_fact, False, party_id, party_weight)
            except Exception:
                self.add_fact(fact_kid=o_fact, parent_road=o_fact._parent_road)
                main_fact = self.get_fact_obj(o_road)
                main_fact._originunit.set_originlink(party_id, party_weight)

    def _meld_partys(self, other_agenda):
        for partyunit in other_agenda._partys.values():
            if self.get_party(partyunit.party_id) is None:
                self.set_partyunit(partyunit=partyunit)
            else:
                self.get_party(partyunit.party_id).meld(partyunit)

    def _meld_ideas(self, other_agenda):
        for brx in other_agenda._ideas.values():
            if self.get_ideaunit(brx.idea_id) is None:
                self.set_ideaunit(y_ideaunit=brx)
            else:
                self.get_ideaunit(brx.idea_id).meld(brx)

    def _meld_beliefs(self, other_agenda):
        for hx in other_agenda._factroot._beliefunits.values():
            if self._factroot._beliefunits.get(hx.base) is None:
                self.set_belief(
                    base=hx.base, pick=hx.belief, open=hx.open, nigh=hx.nigh
                )
            else:
                self._factroot._beliefunits.get(hx.base).meld(hx)

    def _meld_originlinks(self, party_id: PartyID, party_weight: float):
        if party_id != None:
            self._originunit.set_originlink(party_id, party_weight)

    def get_assignment(
        self,
        agenda_x,
        assignor_partys: dict[PartyID:PartyUnit],
        assignor_party_id: PartyID,
    ) -> any:
        self.calc_agenda_metrics()
        self._set_assignment_partys(agenda_x, assignor_partys, assignor_party_id)
        self._set_assignment_ideas(agenda_x)
        assignor_pledges = self._get_assignor_pledge_facts(agenda_x, assignor_party_id)
        relevant_roads = self._get_relevant_roads(assignor_pledges)
        self._set_assignment_facts(agenda_x, relevant_roads)
        return agenda_x

    def _set_assignment_facts(self, x_agenda, relevant_roads: dict[RoadUnit:str]):
        sorted_relevants = sorted(list(relevant_roads))
        # difficult to know how to manage root fact attributes...
        if sorted_relevants != []:
            root_road = sorted_relevants.pop(0)

        for relevant_road in sorted_relevants:
            relevant_fact = copy_deepcopy(self.get_fact_obj(relevant_road))
            relevant_fact.find_replace_road(
                old_road=get_root_node_from_road(relevant_road, self._road_delimiter),
                new_road=x_agenda._real_id,
            )
            relevant_fact.clear_kids()
            x_agenda.add_fact(relevant_fact, parent_road=relevant_fact._parent_road)

        for afu in self._factroot._beliefunits.values():
            if relevant_roads.get(afu.base) != None:
                x_agenda.set_belief(
                    base=rebuild_road(afu.base, self._real_id, x_agenda._real_id),
                    pick=rebuild_road(afu.pick, self._real_id, x_agenda._real_id),
                    open=afu.open,
                    nigh=afu.nigh,
                )

    def _set_assignment_partys(
        self,
        agenda_x,
        assignor_partys: dict[PartyID:PartyUnit],
        assignor_party_id: PartyID,
    ):
        if self.party_exists(assignor_party_id):
            # get all partys that are both in self._partys and assignor_known_partys
            partys_set = get_intersection_of_partys(self._partys, assignor_partys)
            for party_id_x in partys_set:
                agenda_x.set_partyunit(partyunit=self.get_party(party_id_x))
        return agenda_x

    def _set_assignment_ideas(self, agenda_x):
        revelant_ideas = get_partys_relevant_ideas(self._ideas, agenda_x._partys)
        for idea_idea_id, idea_partys in revelant_ideas.items():
            if agenda_x._ideas.get(idea_idea_id) is None:
                idea_x = ideaunit_shop(idea_id=idea_idea_id)
                for party_id in idea_partys:
                    idea_x.set_partylink(partylink_shop(party_id=party_id))
                agenda_x.set_ideaunit(idea_x)

    def _get_assignor_pledge_facts(
        self, agenda_x, assignor_party_id: IdeaID
    ) -> dict[RoadUnit:int]:
        assignor_ideas = get_party_relevant_ideas(agenda_x._ideas, assignor_party_id)
        return {
            fact_road: -1
            for fact_road, x_fact in self._fact_dict.items()
            if (x_fact.assignor_in(assignor_ideas) and x_fact.pledge)
        }


def agendaunit_shop(
    _owner_id: OwnerID = None,
    _real_id: RealID = None,
    _road_delimiter: str = None,
    _planck: float = None,
    _penny: float = None,
    _weight: float = None,
    _meld_strategy: MeldStrategy = None,
) -> AgendaUnit:
    if _owner_id is None:
        _owner_id = ""
    if _real_id is None:
        _real_id = get_default_real_id_roadnode()
    if _meld_strategy is None:
        _meld_strategy = get_meld_default()

    x_agenda = AgendaUnit(
        _owner_id=_owner_id,
        _weight=get_1_if_None(_weight),
        _real_id=_real_id,
        _partys=get_empty_dict_if_none(None),
        _ideas=get_empty_dict_if_none(None),
        _fact_dict=get_empty_dict_if_none(None),
        _econ_dict=get_empty_dict_if_none(None),
        _healers_dict=get_empty_dict_if_none(None),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _planck=default_planck_if_none(_planck),
        _penny=default_penny_if_none(_penny),
        _meld_strategy=validate_meld_strategy(_meld_strategy),
        _econs_justified=get_False_if_None(),
        _econs_buildable=get_False_if_None(),
        _sum_healerhold_importance=get_0_if_None(),
    )
    x_agenda._factroot = factunit_shop(
        _root=True, _uid=1, _level=0, _agenda_real_id=x_agenda._real_id
    )
    x_agenda._factroot._road_delimiter = x_agenda._road_delimiter
    x_agenda.set_max_tree_traverse(3)
    x_agenda._rational = False
    x_agenda._originunit = originunit_shop()
    return x_agenda


def get_from_json(x_agenda_json: str) -> AgendaUnit:
    return get_from_dict(get_dict_from_json(x_agenda_json))


def get_from_dict(agenda_dict: dict) -> AgendaUnit:
    x_agenda = agendaunit_shop()
    x_agenda.set_owner_id(get_obj_from_agenda_dict(agenda_dict, "_owner_id"))
    x_agenda._weight = get_obj_from_agenda_dict(agenda_dict, "_weight")
    x_agenda.set_max_tree_traverse(
        get_obj_from_agenda_dict(agenda_dict, "_max_tree_traverse")
    )
    x_agenda.set_real_id(get_obj_from_agenda_dict(agenda_dict, "_real_id"))
    x_agenda._road_delimiter = default_road_delimiter_if_none(
        get_obj_from_agenda_dict(agenda_dict, "_road_delimiter")
    )
    x_agenda._planck = default_planck_if_none(
        get_obj_from_agenda_dict(agenda_dict, "_planck")
    )
    x_agenda._penny = default_penny_if_none(
        get_obj_from_agenda_dict(agenda_dict, "_penny")
    )
    x_agenda._party_credor_pool = get_obj_from_agenda_dict(
        agenda_dict, "_party_credor_pool"
    )
    x_agenda._party_debtor_pool = get_obj_from_agenda_dict(
        agenda_dict, "_party_debtor_pool"
    )
    if get_obj_from_agenda_dict(agenda_dict, "_meld_strategy") is None:
        x_agenda._meld_strategy = get_meld_default()
    else:
        x_agenda._meld_strategy = get_obj_from_agenda_dict(
            agenda_dict, "_meld_strategy"
        )
    x_agenda._last_atom_id = get_obj_from_agenda_dict(agenda_dict, "_last_atom_id")
    for x_partyunit in get_obj_from_agenda_dict(
        agenda_dict, dict_key="_partys", _road_delimiter=x_agenda._road_delimiter
    ).values():
        x_agenda.set_partyunit(x_partyunit)
    for x_ideaunit in get_obj_from_agenda_dict(
        agenda_dict, dict_key="_ideas", _road_delimiter=x_agenda._road_delimiter
    ).values():
        x_agenda.set_ideaunit(x_ideaunit)
    x_agenda._originunit = get_obj_from_agenda_dict(agenda_dict, "_originunit")

    set_factroot_from_agenda_dict(x_agenda, agenda_dict)
    x_agenda.calc_agenda_metrics()  # clean up tree traverse defined fields
    return x_agenda


def set_factroot_from_agenda_dict(x_agenda: AgendaUnit, agenda_dict: dict):
    factroot_dict = agenda_dict.get("_factroot")
    x_agenda._factroot = factunit_shop(
        _root=True,
        _label=x_agenda._real_id,
        _uid=get_obj_from_fact_dict(factroot_dict, "_uid"),
        _weight=get_obj_from_fact_dict(factroot_dict, "_weight"),
        _begin=get_obj_from_fact_dict(factroot_dict, "_begin"),
        _close=get_obj_from_fact_dict(factroot_dict, "_close"),
        _numor=get_obj_from_fact_dict(factroot_dict, "_numor"),
        _denom=get_obj_from_fact_dict(factroot_dict, "_denom"),
        _reest=get_obj_from_fact_dict(factroot_dict, "_reest"),
        _problem_bool=get_obj_from_fact_dict(factroot_dict, "_problem_bool"),
        _range_source_road=get_obj_from_fact_dict(factroot_dict, "_range_source_road"),
        _numeric_road=get_obj_from_fact_dict(factroot_dict, "_numeric_road"),
        _reasonunits=get_obj_from_fact_dict(factroot_dict, "_reasonunits"),
        _assignedunit=get_obj_from_fact_dict(factroot_dict, "_assignedunit"),
        _healerhold=get_obj_from_fact_dict(factroot_dict, "_healerhold"),
        _beliefunits=get_obj_from_fact_dict(factroot_dict, "_beliefunits"),
        _balancelinks=get_obj_from_fact_dict(factroot_dict, "_balancelinks"),
        _is_expanded=get_obj_from_fact_dict(factroot_dict, "_is_expanded"),
        _road_delimiter=get_obj_from_fact_dict(factroot_dict, "_road_delimiter"),
        _agenda_real_id=x_agenda._real_id,
    )
    set_factroot_kids_from_dict(x_agenda, factroot_dict)


def set_factroot_kids_from_dict(x_agenda: AgendaUnit, factroot_dict: dict):
    to_evaluate_fact_dicts = []
    parent_road_text = "parent_road"
    # for every kid dict, set parent_road in dict, add to to_evaluate_list
    for x_dict in get_obj_from_fact_dict(factroot_dict, "_kids").values():
        x_dict[parent_road_text] = x_agenda._real_id
        to_evaluate_fact_dicts.append(x_dict)

    while to_evaluate_fact_dicts != []:
        fact_dict = to_evaluate_fact_dicts.pop(0)
        # for every kid dict, set parent_road in dict, add to to_evaluate_list
        for kid_dict in get_obj_from_fact_dict(fact_dict, "_kids").values():
            parent_road = get_obj_from_fact_dict(fact_dict, parent_road_text)
            kid_label = get_obj_from_fact_dict(fact_dict, "_label")
            kid_dict[parent_road_text] = x_agenda.make_road(parent_road, kid_label)
            to_evaluate_fact_dicts.append(kid_dict)

        x_factkid = factunit_shop(
            _label=get_obj_from_fact_dict(fact_dict, "_label"),
            _weight=get_obj_from_fact_dict(fact_dict, "_weight"),
            _uid=get_obj_from_fact_dict(fact_dict, "_uid"),
            _begin=get_obj_from_fact_dict(fact_dict, "_begin"),
            _close=get_obj_from_fact_dict(fact_dict, "_close"),
            _numor=get_obj_from_fact_dict(fact_dict, "_numor"),
            _denom=get_obj_from_fact_dict(fact_dict, "_denom"),
            _reest=get_obj_from_fact_dict(fact_dict, "_reest"),
            pledge=get_obj_from_fact_dict(fact_dict, "pledge"),
            _problem_bool=get_obj_from_fact_dict(fact_dict, "_problem_bool"),
            _reasonunits=get_obj_from_fact_dict(fact_dict, "_reasonunits"),
            _assignedunit=get_obj_from_fact_dict(fact_dict, "_assignedunit"),
            _healerhold=get_obj_from_fact_dict(fact_dict, "_healerhold"),
            _originunit=get_obj_from_fact_dict(fact_dict, "_originunit"),
            _balancelinks=get_obj_from_fact_dict(fact_dict, "_balancelinks"),
            _beliefunits=get_obj_from_fact_dict(fact_dict, "_beliefunits"),
            _is_expanded=get_obj_from_fact_dict(fact_dict, "_is_expanded"),
            _range_source_road=get_obj_from_fact_dict(fact_dict, "_range_source_road"),
            _numeric_road=get_obj_from_fact_dict(fact_dict, "_numeric_road"),
            _agenda_real_id=x_agenda._real_id,
        )
        x_agenda.add_fact(x_factkid, parent_road=fact_dict[parent_road_text])


def get_obj_from_agenda_dict(
    x_dict: dict[str:], dict_key: str, _road_delimiter: str = None
) -> any:
    if dict_key == "_originunit":
        return (
            originunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else originunit_shop()
        )
    elif dict_key == "_partys":
        return (
            partyunits_get_from_dict(x_dict[dict_key], _road_delimiter)
            if x_dict.get(dict_key) != None
            else partyunits_get_from_dict(x_dict[dict_key], _road_delimiter)
        )
    elif dict_key == "_ideas":
        return (
            get_ideaunits_from_dict(x_dict[dict_key], _road_delimiter)
            if x_dict.get(dict_key) != None
            else get_ideaunits_from_dict(x_dict[dict_key], _road_delimiter)
        )
    elif dict_key == "_max_tree_traverse":
        return (
            x_dict[dict_key]
            if x_dict.get(dict_key) != None
            else max_tree_traverse_default()
        )
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None


def get_dict_of_agenda_from_dict(x_dict: dict[str:dict]) -> dict[str:AgendaUnit]:
    agendaunits = {}
    for agendaunit_dict in x_dict.values():
        x_agenda = get_from_dict(agenda_dict=agendaunit_dict)
        agendaunits[x_agenda._owner_id] = x_agenda
    return agendaunits
