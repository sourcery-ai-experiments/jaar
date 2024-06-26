from src._instrument.python import (
    get_json_from_dict,
    get_dict_from_json,
    get_1_if_None,
    get_0_if_None,
    get_False_if_None,
    get_empty_dict_if_none,
)
from src._road.finance import (
    trim_pixel_excess,
    default_pixel_if_none,
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
    PersonID,
    HealerID,
    RealID,
    is_roadunit_convertible_to_path,
)
from src._world.meld import (
    get_meld_weight,
    MeldStrategy,
    get_meld_default,
    validate_meld_strategy,
)
from src._world.person import (
    PersonUnit,
    PersonLink,
    personunits_get_from_dict,
    personunit_shop,
    personlink_shop,
    PersonUnitExternalMetrics,
)
from src._world.belieflink import belieflink_shop
from src._world.beliefunit import (
    BalanceLink,
    BeliefID,
    BeliefUnit,
    get_beliefunits_from_dict,
    beliefunit_shop,
    balancelink_shop,
    get_person_relevant_beliefs,
    get_persons_relevant_beliefs,
    get_intersection_of_persons,
)
from src._world.healer import HealerHold
from src._world.reason_idea import (
    FactCore,
    FactUnit,
    FactUnit,
    ReasonUnit,
    RoadUnit,
    factunit_shop,
)
from src._world.reason_assign import AssignedUnit
from src._world.tree_metrics import TreeMetrics, treemetrics_shop
from src._world.hreg_time import HregTimeIdeaSource as HregIdea
from src._world.lemma import lemmas_shop, Lemmas
from src._world.origin import originunit_get_from_dict, originunit_shop, OriginUnit
from src._world.idea import (
    IdeaUnit,
    ideaunit_shop,
    ideaattrfilter_shop,
    IdeaAttrFilter,
    get_obj_from_idea_dict,
)
from copy import deepcopy as copy_deepcopy
from dataclasses import dataclass
from datetime import datetime


class InvalidWorldException(Exception):
    pass


class InvalidLabelException(Exception):
    pass


class NewDelimiterException(Exception):
    pass


class PersonUnitsCredorDebtorSumException(Exception):
    pass


class PersonMissingException(Exception):
    pass


class Exception_econs_justified(Exception):
    pass


class _pixel_RatioException(Exception):
    pass


class _last_gift_idException(Exception):
    pass


class healerhold_belief_id_Exception(Exception):
    pass


@dataclass
class WorldUnit:
    _real_id: RealID = None
    _owner_id: OwnerID = None
    _last_gift_id: int = None
    _weight: float = None
    _persons: dict[PersonID:PersonUnit] = None
    _beliefs: dict[BeliefID:BeliefUnit] = None
    _idearoot: IdeaUnit = None
    _max_tree_traverse: int = None
    _road_delimiter: str = None
    _pixel: float = None
    _penny: float = None
    _monetary_desc: str = None
    _person_credor_pool: int = None
    _person_debtor_pool: int = None
    _meld_strategy: MeldStrategy = None
    _originunit: OriginUnit = None  # In job worlds this shows source
    # calc_world_metrics Calculated field begin
    _idea_dict: dict[RoadUnit:IdeaUnit] = None
    _econ_dict: dict[RoadUnit:IdeaUnit] = None
    _healers_dict: dict[HealerID : dict[RoadUnit:IdeaUnit]] = None
    _tree_traverse_count: int = None
    _rational: bool = None
    _econs_justified: bool = None
    _econs_buildable: bool = None
    _sum_healerhold_importance: bool = None
    # calc_world_metrics Calculated field end

    def del_last_gift_id(self):
        self._last_gift_id = None

    def set_last_gift_id(self, x_last_gift_id: int):
        if self._last_gift_id != None and x_last_gift_id < self._last_gift_id:
            raise _last_gift_idException(
                f"Cannot set _last_gift_id to {x_last_gift_id} because it is less than {self._last_gift_id}."
            )
        self._last_gift_id = x_last_gift_id

    def set_monetary_desc(self, x_monetary_desc: str):
        self._monetary_desc = x_monetary_desc

    def set_person_pool(self, x_person_pool: int):
        self.set_person_credor_pool(
            new_person_credor_pool=x_person_pool,
            update_persons_credor_weight=True,
            correct_pixel_issues=True,
        )
        self.set_person_debtor_pool(
            new_person_debtor_pool=x_person_pool,
            update_persons_debtor_weight=True,
            correct_pixel_issues=True,
        )

    def set_person_credor_pool(
        self,
        new_person_credor_pool: int,
        update_persons_credor_weight: bool = False,
        correct_pixel_issues: bool = False,
    ):
        if (new_person_credor_pool / self._pixel).is_integer() is False:
            raise _pixel_RatioException(
                f"World '{self._owner_id}' cannot set _person_credor_pool='{new_person_credor_pool}'. It is not divisible by pixel '{self._pixel}'"
            )

        if update_persons_credor_weight:
            old_person_credor_pool = self.get_personunits_credor_weight_sum()
            if old_person_credor_pool != 0:
                x_ratio = new_person_credor_pool / old_person_credor_pool
                for x_person in self._persons.values():
                    new_person_credor_weight = trim_pixel_excess(
                        num=x_person.credor_weight * x_ratio, pixel=x_person._pixel
                    )
                    x_person.set_credor_weight(new_person_credor_weight)

        self._person_credor_pool = new_person_credor_pool
        if correct_pixel_issues:
            self._correct_any_credor_pixel_issues()

    def _correct_any_credor_pixel_issues(self):
        if self.get_personunits_credor_weight_sum() != self._person_credor_pool:
            missing_credor_weight = (
                self._person_credor_pool - self.get_personunits_credor_weight_sum()
            )
            if len(self._persons) > 0:
                personunits = list(self._persons.values())
                # persons_count = len(self._persons)
                # pixel_count = missing_credor_weight / self._pixel
                # if pixel_count <= persons_count:
                for _ in range(0, missing_credor_weight, self._pixel):
                    x_personunit = personunits.pop()
                    x_personunit.set_credor_weight(
                        x_personunit.credor_weight + self._pixel
                    )

    def set_person_debtor_pool(
        self,
        new_person_debtor_pool: int,
        update_persons_debtor_weight: bool = False,
        correct_pixel_issues: bool = False,
    ):
        if (new_person_debtor_pool / self._pixel).is_integer() is False:
            raise _pixel_RatioException(
                f"World '{self._owner_id}' cannot set _person_debtor_pool='{new_person_debtor_pool}'. It is not divisible by pixel '{self._pixel}'"
            )

        if update_persons_debtor_weight:
            old_person_debtor_pool = self.get_personunits_debtor_weight_sum()
            if old_person_debtor_pool != 0:
                x_ratio = new_person_debtor_pool / old_person_debtor_pool
                for x_person in self._persons.values():
                    new_person_debtor_weight = trim_pixel_excess(
                        num=x_person.debtor_weight * x_ratio, pixel=x_person._pixel
                    )
                    x_person.set_debtor_weight(new_person_debtor_weight)
        self._person_debtor_pool = new_person_debtor_pool
        if correct_pixel_issues:
            self._correct_any_debtor_pixel_issues()

    def _correct_any_debtor_pixel_issues(self):
        if self.get_personunits_debtor_weight_sum() != self._person_debtor_pool:
            missing_debtor_weight = (
                self._person_debtor_pool - self.get_personunits_debtor_weight_sum()
            )
            if len(self._persons) > 0:
                personunits = list(self._persons.values())
                # persons_count = len(self._persons)
                # pixel_count = missing_debtor_weight / self._pixel
                # if pixel_count <= persons_count:
                for _ in range(0, missing_debtor_weight, self._pixel):
                    x_personunit = personunits.pop()
                    x_personunit.set_debtor_weight(
                        x_personunit.debtor_weight + self._pixel
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

    def set_persons_output_world_meld_order(self):
        sort_persons_list = list(self._persons.values())
        sort_persons_list.sort(key=lambda x: x.person_id.lower(), reverse=False)
        for count_x, x_personunit in enumerate(sort_persons_list):
            x_personunit.set_output_world_meld_order(count_x)

    def clear_persons_output_world_meld_order(self):
        for x_personunit in self._persons.values():
            x_personunit.clear_output_world_meld_order()

    def set_road_delimiter(self, new_road_delimiter: str):
        self.calc_world_metrics()
        if self._road_delimiter != new_road_delimiter:
            for x_idea_road in self._idea_dict.keys():
                if is_string_in_road(new_road_delimiter, x_idea_road):
                    raise NewDelimiterException(
                        f"Cannot modify delimiter to '{new_road_delimiter}' because it already exists an idea label '{x_idea_road}'"
                    )

            # Grab pointers to every idea
            idea_pointers = {
                x_idea_road: self.get_idea_obj(x_idea_road)
                for x_idea_road in self._idea_dict.keys()
            }

            # modify all road attributes in idea
            # old_road_delimiter = copy_deepcopy(self._road_delimiter)
            self._road_delimiter = default_road_delimiter_if_none(new_road_delimiter)
            for x_idea in idea_pointers.values():
                x_idea.set_road_delimiter(self._road_delimiter)

    def set_real_id(self, real_id: str):
        old_real_id = copy_deepcopy(self._real_id)
        self._real_id = real_id

        self.calc_world_metrics()
        for idea_obj in self._idea_dict.values():
            idea_obj._world_real_id = self._real_id

        self.edit_idea_label(old_road=old_real_id, new_label=self._real_id)
        self.calc_world_metrics()

    def set_personunit_external_metrics(
        self, external_metrics: PersonUnitExternalMetrics
    ):
        person_x = self.get_person(external_metrics.internal_person_id)
        person_x._credor_operational = external_metrics.credor_operational
        person_x._debtor_operational = external_metrics.debtor_operational
        # self.set_personunit(personunit=person_x)

    def set_max_tree_traverse(self, int_x: int):
        if int_x < 2:
            raise InvalidWorldException(
                f"set_max_tree_traverse: input '{int_x}' must be number that is 2 or greater"
            )
        else:
            self._max_tree_traverse = int_x

    def get_world_sprung_from_single_idea(self, road: RoadUnit) -> any:
        self.calc_world_metrics()
        x_idea = self.get_idea_obj(road)
        new_weight = self._weight * x_idea._world_importance
        x_world = worldunit_shop(_owner_id=self._idearoot._label, _weight=new_weight)

        for road_assc in sorted(list(self._get_relevant_roads({road}))):
            src_yx = self.get_idea_obj(road_assc)
            new_yx = copy_deepcopy(src_yx)
            if new_yx._parent_road != "":
                x_world.add_idea(new_yx, parent_road=new_yx._parent_road)
            x_world.calc_world_metrics()

        # TODO grab beliefs
        # TODO grab all belief persons
        # TODO grab facts
        return x_world

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
            x_idea = self.get_idea_obj(road_x)
            for reasonunit_obj in x_idea._reasonunits.values():
                reason_base = reasonunit_obj.base
                self._evaluate_relevancy(
                    to_evaluate_list=to_evaluate_list,
                    to_evaluate_hx_dict=to_evaluate_hx_dict,
                    to_evaluate_road=reason_base,
                    road_type="reasonunit_base",
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
        to_evaluate_list: list[RoadUnit],
        to_evaluate_hx_dict: dict[RoadUnit:int],
        to_evaluate_road: RoadUnit,
        road_type: str,
    ):
        if to_evaluate_hx_dict.get(to_evaluate_road) is None:
            to_evaluate_list.append(to_evaluate_road)
            to_evaluate_hx_dict[to_evaluate_road] = road_type

            if road_type == "reasonunit_base":
                ru_base_idea = self.get_idea_obj(to_evaluate_road)
                for descendant_road in ru_base_idea.get_descendant_roads_from_kids():
                    self._evaluate_relevancy(
                        to_evaluate_list=to_evaluate_list,
                        to_evaluate_hx_dict=to_evaluate_hx_dict,
                        to_evaluate_road=descendant_road,
                        road_type="reasonunit_descendant",
                    )

    def all_ideas_relevant_to_pledge_idea(self, road: RoadUnit) -> bool:
        pledge_idea_assoc_set = set(self._get_relevant_roads({road}))
        all_ideas_set = set(self.get_idea_tree_ordered_road_list())
        return all_ideas_set == all_ideas_set.intersection(pledge_idea_assoc_set)

    def _are_all_persons_beliefs_are_in_idea_kid(self, road: RoadUnit) -> bool:
        idea_kid = self.get_idea_obj(road)
        # get dict of all idea balanceheirs
        balanceheir_list = idea_kid._balanceheirs.keys()
        balanceheir_dict = {
            balanceheir_belief_id: 1 for balanceheir_belief_id in balanceheir_list
        }
        non_single_beliefunits = {
            beliefunit.belief_id: beliefunit
            for beliefunit in self._beliefs.values()
            if beliefunit._person_mirror != True
        }
        # check all non_person_mirror_beliefunits are in balanceheirs
        for non_single_belief in non_single_beliefunits.values():
            if balanceheir_dict.get(non_single_belief.belief_id) is None:
                return False

        # get dict of all personlinks that are in all balanceheirs
        balanceheir_personunits = {}
        for balanceheir_person_id in balanceheir_dict:
            beliefunit = self.get_beliefunit(balanceheir_person_id)
            for personlink in beliefunit._persons.values():
                balanceheir_personunits[personlink.person_id] = self.get_person(
                    personlink.person_id
                )

        # check all world._persons are in balanceheir_personunits
        return len(self._persons) == len(balanceheir_personunits)

    def get_time_min_from_dt(self, dt: datetime) -> float:
        x_hregidea = HregIdea(self._road_delimiter)
        return x_hregidea.get_time_min_from_dt(dt=dt)

    def get_time_c400_from_min(self, min: int) -> int:
        time_road = self.make_l1_road("time")
        tech_road = self.make_road(time_road, "tech")
        c400_road = self.make_road(tech_road, "400 year segment")
        c400_idea = self.get_idea_obj(c400_road)
        c400_min = c400_idea._close
        return int(min / c400_min), c400_idea, min % c400_min

    def get_time_c400yr_from_min(self, min: int):
        # GIVEN int minutes within 400 year range return year and remainder minutes
        c400_count, c400_idea, c400yr_min = self.get_time_c400_from_min(min=min)
        c100_4_96y = c400_idea.get_kids_in_range(begin=c400yr_min, close=c400yr_min)[0]
        cXXXyr_min = c400yr_min - c100_4_96y._begin

        time_road = self.make_l1_road("time")
        tech_road = self.make_road(time_road, "tech")

        # identify which range the time is in
        if c100_4_96y._close - c100_4_96y._begin in (
            50492160,
            52596000,
        ):  # 96 year and 100 year ideas
            yr4_1461_road = self.make_road(tech_road, "4year with leap")
            yr4_1461_idea = self.get_idea_obj(yr4_1461_road)
            yr4_segments = int(cXXXyr_min / yr4_1461_idea._close)
            cXyr_min = cXXXyr_min % yr4_1461_idea._close
            yr1_idea = yr4_1461_idea.get_kids_in_range(begin=cXyr_min, close=cXyr_min)[
                0
            ]
        elif c100_4_96y._close - c100_4_96y._begin == 2102400:
            yr4_1460_road = self.make_road(tech_road, "4year wo leap")
            yr4_1460_idea = self.get_idea_obj(yr4_1460_road)
            yr4_segments = 0
            yr1_idea = yr4_1460_idea.get_kids_in_range(cXXXyr_min, cXXXyr_min)[0]
            cXyr_min = cXXXyr_min % yr4_1460_idea._close

        yr1_rem_min = cXyr_min - yr1_idea._begin
        yr1_idea_begin = int(yr1_idea._label.split("-")[0]) - 1

        c100_4_96y_begin = int(c100_4_96y._label.split("-")[0])
        year_num = c100_4_96y_begin + (4 * yr4_segments) + yr1_idea_begin
        return year_num, yr1_idea, yr1_rem_min

    def get_time_month_from_min(self, min: int):
        time_road = self.make_l1_road("time")
        tech_road = self.make_road(time_road, "tech")

        year_num, yr1_idea, yr1_idea_rem_min = self.get_time_c400yr_from_min(min=min)
        yrx = None
        if yr1_idea._close - yr1_idea._begin == 525600:
            yr365_road = self.make_road(tech_road, "365 year")
            yrx = self.get_idea_obj(yr365_road)
        elif yr1_idea._close - yr1_idea._begin == 527040:
            yr366_road = self.make_road(tech_road, "366 year")
            yrx = self.get_idea_obj(yr366_road)
        mon_x = yrx.get_kids_in_range(begin=yr1_idea_rem_min, close=yr1_idea_rem_min)[0]
        month_rem_min = yr1_idea_rem_min - mon_x._begin
        month_num = int(mon_x._label.split("-")[0])
        day_road = self.make_road(tech_road, "day")
        day_x = self.get_idea_obj(day_road)
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
        x_hregidea = HregIdea(self._road_delimiter)
        return x_hregidea.get_jajatime_legible_from_dt(dt=dt_x)

    def get_jajatime_repeating_legible_text(
        self, open: float = None, nigh: float = None, divisor: float = None
    ) -> str:
        x_hregidea = HregIdea(self._road_delimiter)
        str_x = "test3"
        if divisor is None:
            str_x = self.get_jajatime_legible_one_time_event(jajatime_min=open)
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
        x_hregidea = HregIdea(self._road_delimiter)
        open_in_week = open % divisor
        time_road = self.make_l1_road("time")
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

    def get_persons_metrics(self) -> dict[BeliefID:BalanceLink]:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.balancelinks_metrics

    def add_to_belief_world_cred_debt(
        self,
        belief_id: BeliefID,
        balanceheir_world_cred: float,
        balanceheir_world_debt: float,
    ):
        for belief in self._beliefs.values():
            if belief.belief_id == belief_id:
                belief._world_cred += balanceheir_world_cred
                belief._world_debt += balanceheir_world_debt

    def add_to_belief_world_agenda_cred_debt(
        self,
        belief_id: BeliefID,
        balanceline_world_cred: float,
        balanceline_world_debt: float,
    ):
        for belief in self._beliefs.values():
            if (
                belief.belief_id == belief_id
                and balanceline_world_cred != None
                and balanceline_world_debt != None
            ):
                belief._world_agenda_cred += balanceline_world_cred
                belief._world_agenda_debt += balanceline_world_debt

    def add_to_personunit_world_cred_debt(
        self,
        personunit_person_id: PersonID,
        world_cred,
        world_debt: float,
        world_agenda_cred: float,
        world_agenda_debt: float,
    ):
        for personunit in self._persons.values():
            if personunit.person_id == personunit_person_id:
                personunit.add_world_cred_debt(
                    world_cred=world_cred,
                    world_debt=world_debt,
                    world_agenda_cred=world_agenda_cred,
                    world_agenda_debt=world_agenda_debt,
                )

    def del_personunit(self, person_id: str):
        self._beliefs.pop(person_id)
        self._persons.pop(person_id)

    def add_personunit(
        self, person_id: PersonID, credor_weight: int = None, debtor_weight: int = None
    ):
        personunit = personunit_shop(
            person_id=person_id,
            credor_weight=credor_weight,
            debtor_weight=debtor_weight,
            _road_delimiter=self._road_delimiter,
        )
        self.set_personunit(personunit=personunit)

    def set_personunit(self, personunit: PersonUnit):
        if personunit._road_delimiter != self._road_delimiter:
            personunit._road_delimiter = self._road_delimiter
        if personunit._pixel != self._pixel:
            personunit._pixel = self._pixel
        self._persons[personunit.person_id] = personunit

        try:
            self._beliefs[personunit.person_id]
        except KeyError:
            personlink = personlink_shop(
                person_id=PersonID(personunit.person_id),
                credor_weight=1,
                debtor_weight=1,
            )
            personlinks = {personlink.person_id: personlink}
            belief_unit = beliefunit_shop(
                personunit.person_id,
                _person_mirror=True,
                _persons=personlinks,
                _road_delimiter=self._road_delimiter,
            )
            self.set_beliefunit(y_beliefunit=belief_unit)

    def person_exists(self, person_id: PersonID) -> bool:
        return self.get_person(person_id) != None

    def edit_personunit_person_id(
        self,
        old_person_id: PersonID,
        new_person_id: PersonID,
        allow_person_overwite: bool,
        allow_nonsingle_belief_overwrite: bool,
    ):
        # Handle scenarios: some are unacceptable
        old_person_id_credor_weight = self.get_person(old_person_id).credor_weight
        new_person_id_beliefunit = self.get_beliefunit(new_person_id)
        new_person_id_personunit = self.get_person(new_person_id)
        if not allow_person_overwite and new_person_id_personunit != None:
            raise InvalidWorldException(
                f"Person '{old_person_id}' modify to '{new_person_id}' failed since '{new_person_id}' exists."
            )
        elif (
            not allow_nonsingle_belief_overwrite
            and new_person_id_beliefunit != None
            and new_person_id_beliefunit._person_mirror is False
        ):
            raise InvalidWorldException(
                f"Person '{old_person_id}' modify to '{new_person_id}' failed since non-single belief '{new_person_id}' exists."
            )
        elif (
            allow_nonsingle_belief_overwrite
            and new_person_id_beliefunit != None
            and new_person_id_beliefunit._person_mirror is False
        ):
            self.del_beliefunit(belief_id=new_person_id)
        elif self.person_exists(new_person_id):
            old_person_id_credor_weight += new_person_id_personunit.credor_weight

        # upsert new personunit
        self.add_personunit(
            person_id=new_person_id, credor_weight=old_person_id_credor_weight
        )
        # modify all influenced beliefunits personlinks
        for old_person_belief_id in self.get_person_belief_ids(old_person_id):
            old_person_beliefunit = self.get_beliefunit(old_person_belief_id)
            old_person_beliefunit._shift_personlink(old_person_id, new_person_id)
        self.del_personunit(person_id=old_person_id)

    def edit_personunit(
        self, person_id: PersonID, credor_weight: int = None, debtor_weight: int = None
    ):
        if self._persons.get(person_id) is None:
            raise PersonMissingException(f"PersonUnit '{person_id}' does not exist.")
        x_personunit = self.get_person(person_id)
        if credor_weight != None:
            x_personunit.set_credor_weight(credor_weight)
        if debtor_weight != None:
            x_personunit.set_debtor_weight(debtor_weight)
        self.set_personunit(x_personunit)

    def get_person(self, person_id: PersonID) -> PersonUnit:
        return self._persons.get(person_id)

    def get_personunits_person_id_list(self) -> dict[PersonID]:
        person_id_list = list(self._persons.keys())
        person_id_list.append("")
        person_id_dict = {person_id.lower(): person_id for person_id in person_id_list}
        person_id_lowercase_ordered_list = sorted(list(person_id_dict))
        return [
            person_id_dict[person_id_l]
            for person_id_l in person_id_lowercase_ordered_list
        ]

    def set_beliefunit(
        self,
        y_beliefunit: BeliefUnit,
        create_missing_persons: bool = None,
        replace: bool = True,
        add_personlinks: bool = None,
    ):
        if y_beliefunit._road_delimiter != self._road_delimiter:
            y_beliefunit._road_delimiter = self._road_delimiter
        if replace is None:
            replace = False
        if add_personlinks is None:
            add_personlinks = False
        if (
            self.get_beliefunit(y_beliefunit.belief_id) is None
            or replace
            and not add_personlinks
        ):
            self._beliefs[y_beliefunit.belief_id] = y_beliefunit

        if add_personlinks:
            x_beliefunit = self.get_beliefunit(y_beliefunit.belief_id)
            for x_personlink in y_beliefunit._persons.values():
                x_beliefunit.set_personlink(x_personlink)

        if create_missing_persons:
            self._create_missing_persons(personlinks=y_beliefunit._persons)

    def get_beliefunit(self, x_belief_id: BeliefID) -> BeliefUnit:
        return self._beliefs.get(x_belief_id)

    def _create_missing_persons(self, personlinks: dict[PersonID:PersonLink]):
        for personlink_x in personlinks.values():
            if self.get_person(personlink_x.person_id) is None:
                self.set_personunit(
                    personunit=personunit_shop(
                        person_id=personlink_x.person_id,
                        credor_weight=personlink_x.credor_weight,
                        debtor_weight=personlink_x.debtor_weight,
                    )
                )

    def del_beliefunit(self, belief_id: BeliefID):
        self._beliefs.pop(belief_id)

    def edit_beliefunit_belief_id(
        self,
        old_belief_id: BeliefID,
        new_belief_id: BeliefID,
        allow_belief_overwite: bool,
    ):
        if not allow_belief_overwite and self.get_beliefunit(new_belief_id) != None:
            raise InvalidWorldException(
                f"Belief '{old_belief_id}' modify to '{new_belief_id}' failed since '{new_belief_id}' exists."
            )
        elif self.get_beliefunit(new_belief_id) != None:
            old_beliefunit = self.get_beliefunit(old_belief_id)
            old_beliefunit.set_belief_id(belief_id=new_belief_id)
            self.get_beliefunit(new_belief_id).meld(exterior_belief=old_beliefunit)
            self.del_beliefunit(belief_id=old_belief_id)
        elif self.get_beliefunit(new_belief_id) is None:
            old_beliefunit = self.get_beliefunit(old_belief_id)
            beliefunit_x = beliefunit_shop(
                new_belief_id, old_beliefunit._person_mirror, old_beliefunit._persons
            )
            self.set_beliefunit(y_beliefunit=beliefunit_x)
            self.del_beliefunit(belief_id=old_belief_id)

        self._edit_balancelinks_belief_id(
            old_belief_id=old_belief_id,
            new_belief_id=new_belief_id,
            allow_belief_overwite=allow_belief_overwite,
        )

    def _edit_balancelinks_belief_id(
        self,
        old_belief_id: BeliefID,
        new_belief_id: BeliefID,
        allow_belief_overwite: bool,
    ):
        for x_idea in self.get_idea_dict().values():
            if (
                x_idea._balancelinks.get(new_belief_id) != None
                and x_idea._balancelinks.get(old_belief_id) != None
            ):
                old_balancelink = x_idea._balancelinks.get(old_belief_id)
                old_balancelink.belief_id = new_belief_id
                x_idea._balancelinks.get(new_belief_id).meld(
                    exterior_balancelink=old_balancelink,
                    exterior_meld_strategy="sum",
                    src_meld_strategy="sum",
                )

                x_idea.del_balancelink(belief_id=old_belief_id)
            elif (
                x_idea._balancelinks.get(new_belief_id) is None
                and x_idea._balancelinks.get(old_belief_id) != None
            ):
                old_balancelink = x_idea._balancelinks.get(old_belief_id)
                new_balancelink = balancelink_shop(
                    belief_id=new_belief_id,
                    credor_weight=old_balancelink.credor_weight,
                    debtor_weight=old_balancelink.debtor_weight,
                )
                x_idea.set_balancelink(balancelink=new_balancelink)
                x_idea.del_balancelink(belief_id=old_belief_id)

    def _migrate_beliefunits_to_belieflinks(self):
        for x_personunit in self._persons.values():
            x_personunit.clear_belieflinks()

        for x_beliefunit in self._beliefs.values():
            for x_personlink in x_beliefunit._persons.values():
                x_personunit = self.get_person(x_personlink.person_id)
                x_belieflink = belieflink_shop(
                    x_beliefunit.belief_id,
                    credor_weight=x_personlink.credor_weight,
                    debtor_weight=x_personlink.debtor_weight,
                )
                x_personunit.set_belieflink(x_belieflink)

    def set_time_facts(self, open: datetime = None, nigh: datetime = None) -> None:
        open_minutes = self.get_time_min_from_dt(dt=open) if open != None else None
        nigh_minutes = self.get_time_min_from_dt(dt=nigh) if nigh != None else None
        time_road = self.make_l1_road("time")
        minutes_fact = self.make_road(time_road, "jajatime")
        self.set_fact(
            base=minutes_fact,
            pick=minutes_fact,
            open=open_minutes,
            nigh=nigh_minutes,
        )

    def _is_idea_rangeroot(self, idea_road: RoadUnit) -> bool:
        if self._real_id == idea_road:
            raise InvalidWorldException(
                "its difficult to foresee a scenario where idearoot is rangeroot"
            )
        parent_road = get_parent_road(idea_road)
        parent_idea = self.get_idea_obj(parent_road)
        x_idea = self.get_idea_obj(idea_road)
        return x_idea._numeric_road is None and not parent_idea.is_arithmetic()

    def _get_rangeroot_factunits(self) -> list[FactUnit]:
        return [
            fact
            for fact in self._idearoot._factunits.values()
            if fact.open != None
            and fact.nigh != None
            and self._is_idea_rangeroot(idea_road=fact.base)
        ]

    def _get_rangeroot_1stlevel_associates(
        self, ranged_factunits: list[IdeaUnit]
    ) -> Lemmas:
        x_lemmas = lemmas_shop()
        # lemma_ideas = {}
        for fact in ranged_factunits:
            fact_idea = self.get_idea_obj(fact.base)
            for kid in fact_idea._kids.values():
                x_lemmas.eval(x_idea=kid, src_fact=fact, src_idea=fact_idea)

            if fact_idea._range_source_road != None:
                x_lemmas.eval(
                    x_idea=self.get_idea_obj(fact_idea._range_source_road),
                    src_fact=fact,
                    src_idea=fact_idea,
                )
        return x_lemmas

    def _get_lemma_factunits(self) -> dict[RoadUnit:FactUnit]:
        # get all range-root first level kids and range_source_road
        x_lemmas = self._get_rangeroot_1stlevel_associates(
            self._get_rangeroot_factunits()
        )

        # Now get associates (all their descendants and range_source_roads)
        lemma_factunits = {}  # fact.base : factUnit
        count_x = 0
        while count_x < 10000 and x_lemmas.is_lemmas_evaluated() is False:
            count_x += 1
            if count_x == 9998:
                raise InvalidWorldException("lemma loop failed")

            y_lemma = x_lemmas.get_unevaluated_lemma()
            lemma_idea = y_lemma.x_idea
            fact_x = y_lemma.calc_fact

            road_x = self.make_road(lemma_idea._parent_road, lemma_idea._label)
            lemma_factunits[road_x] = fact_x

            for kid2 in lemma_idea._kids.values():
                x_lemmas.eval(x_idea=kid2, src_fact=fact_x, src_idea=lemma_idea)
            if lemma_idea._range_source_road not in [None, ""]:
                x_lemmas.eval(
                    x_idea=self.get_idea_obj(lemma_idea._range_source_road),
                    src_fact=fact_x,
                    src_idea=lemma_idea,
                )

        return lemma_factunits

    def set_fact(
        self,
        base: RoadUnit,
        pick: RoadUnit = None,
        open: float = None,
        nigh: float = None,
        create_missing_ideas: bool = None,
    ):
        if pick is None:
            pick = base
        if create_missing_ideas:
            self._set_ideakid_if_empty(road=base)
            self._set_ideakid_if_empty(road=pick)

        self._execute_tree_traverse()
        fact_base_idea = self.get_idea_obj(base)
        x_idearoot = self.get_idea_obj(self._real_id)
        x_open = None
        if nigh != None and open is None:
            x_open = x_idearoot._factunits.get(base).open
        else:
            x_open = open
        x_nigh = None
        if open != None and nigh is None:
            x_nigh = x_idearoot._factunits.get(base).nigh
        else:
            x_nigh = nigh
        x_factunit = factunit_shop(base=base, pick=pick, open=x_open, nigh=x_nigh)

        if fact_base_idea.is_arithmetic() is False:
            x_idearoot.set_factunit(x_factunit)

        # if fact's idea no range or is a "range-root" then allow fact to be set
        elif fact_base_idea.is_arithmetic() and self._is_idea_rangeroot(base) is False:
            raise InvalidWorldException(
                f"Non range-root fact:{base} can only be set by range-root fact"
            )

        elif fact_base_idea.is_arithmetic() and self._is_idea_rangeroot(base):
            # WHEN idea is "range-root" identify any reason.bases that are descendants
            # calculate and set those descendant facts
            # example: timeline range (0-, 1.5e9) is range-root
            # example: "timeline,weeks" (spllt 10080) is range-descendant
            # there exists a reason base "timeline,weeks" with premise.need = "timeline,weeks"
            # and (1,2) divisor=2 (every othher week)
            #
            # should not set "timeline,weeks" fact, only "timeline" fact and
            # "timeline,weeks" should be set automatica_lly since there exists a reason
            # that has that base.
            x_idearoot.set_factunit(x_factunit)

            # Find all Fact descendants and any range_source_road connections "Lemmas"
            lemmas_dict = self._get_lemma_factunits()
            missing_facts = self.get_missing_fact_bases().keys()
            x_idearoot._apply_any_range_source_road_connections(
                lemmas_dict, missing_facts
            )

        self.calc_world_metrics()

    def get_fact(self, base: RoadUnit) -> FactUnit:
        return self._idearoot._factunits.get(base)

    def del_fact(self, base: RoadUnit):
        self._idearoot.del_factunit(base)

    def get_idea_dict(self, problem: bool = None) -> dict[RoadUnit:IdeaUnit]:
        self.calc_world_metrics()
        if not problem:
            return self._idea_dict
        if self._econs_justified is False:
            raise Exception_econs_justified(
                f"Cannot return problem set because _econs_justified={self._econs_justified}."
            )

        return {
            x_idea.get_road(): x_idea
            for x_idea in self._idea_dict.values()
            if x_idea._problem_bool
        }

    def get_tree_metrics(self) -> TreeMetrics:
        tree_metrics = treemetrics_shop()
        tree_metrics.evaluate_node(
            level=self._idearoot._level,
            reasons=self._idearoot._reasonunits,
            balancelinks=self._idearoot._balancelinks,
            uid=self._idearoot._uid,
            pledge=self._idearoot.pledge,
            idea_road=self._idearoot.get_road(),
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
            reasons=idea_kid._reasonunits,
            balancelinks=idea_kid._balancelinks,
            uid=idea_kid._uid,
            pledge=idea_kid.pledge,
            idea_road=idea_kid.get_road(),
        )
        x_idea_list.append(idea_kid)

    def get_idea_uid_max(self) -> int:
        tree_metrics = self.get_tree_metrics()
        return tree_metrics.uid_max

    def set_all_idea_uids_unique(self):
        tree_metrics = self.get_tree_metrics()
        idea_uid_max = tree_metrics.uid_max
        idea_uid_dict = tree_metrics.uid_dict

        for x_idea in self.get_idea_dict().values():
            if x_idea._uid is None or idea_uid_dict.get(x_idea._uid) > 1:
                new_idea_uid_max = idea_uid_max + 1
                self.edit_idea_attr(road=x_idea.get_road(), uid=new_idea_uid_max)
                idea_uid_max = new_idea_uid_max

    def get_idea_count(self) -> int:
        return len(self._idea_dict)

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

    def get_missing_fact_bases(self) -> dict[RoadUnit:int]:
        tree_metrics = self.get_tree_metrics()
        reason_bases = tree_metrics.reason_bases
        missing_bases = {}
        for base, base_count in reason_bases.items():
            try:
                self._idearoot._factunits[base]
            except KeyError:
                missing_bases[base] = base_count

        return missing_bases

    def add_l1_idea(
        self,
        idea_kid: IdeaUnit,
        create_missing_ideas: bool = None,
        create_missing_beliefs: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        self.add_idea(
            idea_kid=idea_kid,
            parent_road=self._real_id,
            create_missing_ideas=create_missing_ideas,
            create_missing_beliefs=create_missing_beliefs,
            adoptees=adoptees,
            bundling=bundling,
            create_missing_ancestors=create_missing_ancestors,
        )

    def add_idea(
        self,
        idea_kid: IdeaUnit,
        parent_road: RoadUnit,
        create_missing_beliefs: bool = None,
        create_missing_ideas: bool = None,
        adoptees: list[str] = None,
        bundling: bool = True,
        create_missing_ancestors: bool = True,
    ):
        if RoadNode(idea_kid._label).is_node(self._road_delimiter) is False:
            raise InvalidWorldException(
                f"add_idea failed because '{idea_kid._label}' is not a RoadNode."
            )

        if self._idearoot._label != get_root_node_from_road(
            parent_road, self._road_delimiter
        ):
            raise InvalidWorldException(
                f"add_idea failed because parent_road '{parent_road}' has an invalid root node"
            )

        idea_kid._road_delimiter = self._road_delimiter
        if idea_kid._world_real_id != self._real_id:
            idea_kid._world_real_id = self._real_id
        if not create_missing_beliefs:
            idea_kid = self._get_filtered_balancelinks_idea(idea_kid)
        idea_kid.set_parent_road(parent_road=parent_road)

        # create any missing ideas
        if not create_missing_ancestors and self.idea_exists(parent_road) is False:
            raise InvalidWorldException(
                f"add_idea failed because '{parent_road}' idea does not exist."
            )
        parent_road_idea = self.get_idea_obj(parent_road, create_missing_ancestors)
        if parent_road_idea._root is False:
            parent_road_idea
        parent_road_idea.add_kid(idea_kid)

        kid_road = self.make_road(parent_road, idea_kid._label)
        if adoptees != None:
            weight_sum = 0
            for adoptee_label in adoptees:
                adoptee_road = self.make_road(parent_road, adoptee_label)
                adoptee_idea = self.get_idea_obj(adoptee_road)
                weight_sum += adoptee_idea._weight
                new_adoptee_parent_road = self.make_road(kid_road, adoptee_label)
                self.add_idea(adoptee_idea, new_adoptee_parent_road)
                self.edit_idea_attr(
                    road=new_adoptee_parent_road, weight=adoptee_idea._weight
                )
                self.del_idea_obj(adoptee_road)

            if bundling:
                self.edit_idea_attr(road=kid_road, weight=weight_sum)

        if create_missing_ideas:
            self._create_missing_ideas(road=kid_road)
        if create_missing_beliefs:
            self._create_missing_beliefs_persons(balancelinks=idea_kid._balancelinks)

    def _get_filtered_balancelinks_idea(self, x_idea: IdeaUnit) -> IdeaUnit:
        _balancelinks_to_delete = [
            _balancelink_belief_id
            for _balancelink_belief_id in x_idea._balancelinks.keys()
            if self.get_beliefunit(_balancelink_belief_id) is None
        ]
        for _balancelink_belief_id in _balancelinks_to_delete:
            x_idea._balancelinks.pop(_balancelink_belief_id)

        if x_idea._assignedunit != None:
            _suffbeliefs_to_delete = [
                _suffbelief_belief_id
                for _suffbelief_belief_id in x_idea._assignedunit._suffbeliefs.keys()
                if self.get_beliefunit(_suffbelief_belief_id) is None
            ]
            for _suffbelief_belief_id in _suffbeliefs_to_delete:
                x_idea._assignedunit.del_suffbelief(_suffbelief_belief_id)

        return x_idea

    def _create_missing_beliefs_persons(self, balancelinks: dict[BeliefID:BalanceLink]):
        for balancelink_x in balancelinks.values():
            if self.get_beliefunit(balancelink_x.belief_id) is None:
                beliefunit_x = beliefunit_shop(
                    belief_id=balancelink_x.belief_id, _persons={}
                )
                self.set_beliefunit(y_beliefunit=beliefunit_x)

    def _create_missing_ideas(self, road):
        self.calc_world_metrics()
        posted_idea = self.get_idea_obj(road)

        for reason_x in posted_idea._reasonunits.values():
            self._set_ideakid_if_empty(road=reason_x.base)
            for premise_x in reason_x.premises.values():
                self._set_ideakid_if_empty(road=premise_x.need)
        if posted_idea._range_source_road != None:
            self._set_ideakid_if_empty(road=posted_idea._range_source_road)
        if posted_idea._numeric_road != None:
            self._set_ideakid_if_empty(road=posted_idea._numeric_road)

    def _set_ideakid_if_empty(self, road: RoadUnit):
        if self.idea_exists(road) is False:
            self.add_idea(
                ideaunit_shop(get_terminus_node(road, self._road_delimiter)),
                parent_road=get_parent_road(road),
            )

    def del_idea_obj(self, road: RoadUnit, del_children: bool = True):
        if road == self._idearoot.get_road():
            raise InvalidWorldException("Idearoot cannot be deleted")
        parent_road = get_parent_road(road)
        if self.idea_exists(road):
            if not del_children:
                self._shift_idea_kids(x_road=road)
            parent_idea = self.get_idea_obj(parent_road)
            parent_idea.del_kid(get_terminus_node(road, self._road_delimiter))
        self.calc_world_metrics()

    def _shift_idea_kids(self, x_road: RoadUnit):
        parent_road = get_parent_road(x_road)
        d_temp_idea = self.get_idea_obj(x_road)
        for kid in d_temp_idea._kids.values():
            self.add_idea(kid, parent_road=parent_road)

    def set_owner_id(self, new_owner_id):
        self._owner_id = new_owner_id

    def edit_idea_label(
        self,
        old_road: RoadUnit,
        new_label: RoadNode,
    ):
        if self._road_delimiter in new_label:
            raise InvalidLabelException(
                f"Cannot modify '{old_road}' because new_label {new_label} contains delimiter {self._road_delimiter}"
            )
        if self.idea_exists(old_road) is False:
            raise InvalidWorldException(f"Idea {old_road=} does not exist")

        parent_road = get_parent_road(road=old_road)
        new_road = (
            self.make_road(new_label)
            if parent_road == ""
            else self.make_road(parent_road, new_label)
        )
        if old_road != new_road:
            if parent_road == "":
                self._idearoot.set_idea_label(new_label)
            else:
                self._non_root_idea_label_edit(old_road, new_label, parent_road)
            self._idearoot_find_replace_road(old_road=old_road, new_road=new_road)
            self._idearoot._factunits = find_replace_road_key_dict(
                dict_x=self._idearoot._factunits,
                old_road=old_road,
                new_road=new_road,
            )

    def _non_root_idea_label_edit(
        self, old_road: RoadUnit, new_label: RoadNode, parent_road: RoadUnit
    ):
        x_idea = self.get_idea_obj(old_road)
        x_idea.set_idea_label(new_label)
        x_idea._parent_road = parent_road
        idea_parent = self.get_idea_obj(get_parent_road(old_road))
        idea_parent._kids.pop(get_terminus_node(old_road, self._road_delimiter))
        idea_parent._kids[x_idea._label] = x_idea

    def _idearoot_find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        self._idearoot.find_replace_road(old_road=old_road, new_road=new_road)

        idea_iter_list = [self._idearoot]
        while idea_iter_list != []:
            listed_idea = idea_iter_list.pop()
            # put all idea_children in idea list
            if listed_idea._kids != None:
                for idea_kid in listed_idea._kids.values():
                    idea_iter_list.append(idea_kid)
                    if is_sub_road(
                        ref_road=idea_kid._parent_road,
                        sub_road=old_road,
                    ):
                        idea_kid._parent_road = rebuild_road(
                            subj_road=idea_kid._parent_road,
                            old_road=old_road,
                            new_road=new_road,
                        )
                    idea_kid.find_replace_road(old_road=old_road, new_road=new_road)

    def _set_ideaattrfilter_premise_ranges(self, x_ideaattrfilter: IdeaAttrFilter):
        premise_idea = self.get_idea_obj(x_ideaattrfilter.get_premise_need())
        x_ideaattrfilter.set_premise_range_attributes_influenced_by_premise_idea(
            premise_open=premise_idea._begin,
            premise_nigh=premise_idea._close,
            # premise_numor=premise_idea.anc_numor,
            premise_denom=premise_idea._denom,
            # anc_reest=premise_idea.anc_reest,
        )

    def _set_ideaattrfilter_begin_close(
        self, ideaattrfilter: IdeaAttrFilter, idea_road: RoadUnit
    ) -> set[float, float]:
        x_iaf = ideaattrfilter
        anc_roads = get_ancestor_roads(road=idea_road)
        if (
            x_iaf.addin != None
            or x_iaf.numor != None
            or x_iaf.denom != None
            or x_iaf.reest != None
        ) and len(anc_roads) == 1:
            raise InvalidWorldException("Root Idea cannot have numor denom reest.")
        parent_road = self._real_id if len(anc_roads) == 1 else anc_roads[1]

        parent_has_range = None
        parent_idea = self.get_idea_obj(parent_road)
        parent_begin = parent_idea._begin
        parent_close = parent_idea._close
        parent_has_range = parent_begin is not None and parent_close is not None

        numeric_begin = None
        numeric_close = None
        numeric_range = None
        if x_iaf.numeric_road != None:
            numeric_idea = self.get_idea_obj(x_iaf.numeric_road)
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
            raise InvalidWorldException(
                "Idea has begin-close range parent, cannot have numeric_road"
            )
        elif not parent_has_range and not numeric_range and x_iaf.numor != None:
            raise InvalidWorldException(
                f"Idea cannot edit numor={x_iaf.numor}/denom/reest of '{idea_road}' if parent '{parent_road}' or ideaunit._numeric_road does not have begin/close range"
            )
        ideaattrfilter.begin = x_begin
        ideaattrfilter.close = x_close

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
        self.edit_idea_attr(
            road=road,
            reason_base=reason_base,
            reason_premise=reason_premise,
            reason_premise_open=reason_premise_open,
            reason_premise_nigh=reason_premise_nigh,
            reason_premise_divisor=reason_premise_divisor,
        )

    def edit_idea_attr(
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
        reason_suff_idea_active: str = None,
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
        factunit: FactUnit = None,
        descendant_pledge_count: int = None,
        all_person_cred: bool = None,
        all_person_debt: bool = None,
        balancelink: BalanceLink = None,
        balancelink_del: BeliefID = None,
        is_expanded: bool = None,
        meld_strategy: MeldStrategy = None,
        problem_bool: bool = None,
    ):
        if healerhold != None:
            for x_belief_id in healerhold._belief_ids:
                if self._beliefs.get(x_belief_id) is None:
                    raise healerhold_belief_id_Exception(
                        f"Idea cannot edit healerhold because belief_id '{x_belief_id}' does not exist as belief in World"
                    )

        x_ideaattrfilter = ideaattrfilter_shop(
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
            reason_suff_idea_active=reason_suff_idea_active,
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
            all_person_cred=all_person_cred,
            all_person_debt=all_person_debt,
            balancelink=balancelink,
            balancelink_del=balancelink_del,
            is_expanded=is_expanded,
            pledge=pledge,
            factunit=factunit,
            meld_strategy=meld_strategy,
            problem_bool=problem_bool,
        )
        if x_ideaattrfilter.has_numeric_attrs():
            self._set_ideaattrfilter_begin_close(x_ideaattrfilter, road)
        if x_ideaattrfilter.has_reason_premise():
            self._set_ideaattrfilter_premise_ranges(x_ideaattrfilter)
        x_idea = self.get_idea_obj(road)
        x_idea._set_idea_attr(idea_attr=x_ideaattrfilter)

        # deleting or setting a balancelink reqquires a tree traverse to correctly set balanceheirs and balancelines
        if balancelink_del != None or balancelink != None:
            self.calc_world_metrics()

    def get_agenda_dict(
        self,
        base: RoadUnit = None,
        agenda_enterprise: bool = True,
        agenda_state: bool = True,
    ) -> dict[RoadUnit:IdeaUnit]:
        self.calc_world_metrics()
        return {
            x_idea.get_road(): x_idea
            for x_idea in self._idea_dict.values()
            if x_idea.is_agenda_item(necessary_base=base)
        }

    def get_all_pledges(self) -> dict[RoadUnit:IdeaUnit]:
        self.calc_world_metrics()
        all_ideas = self._idea_dict.values()
        return {x_idea.get_road(): x_idea for x_idea in all_ideas if x_idea.pledge}

    def set_agenda_task_complete(self, task_road: RoadUnit, base: RoadUnit):
        pledge_item = self.get_idea_obj(task_road)
        pledge_item.set_factunit_to_complete(self._idearoot._factunits[base])

    def is_personunits_credor_weight_sum_correct(self) -> bool:
        x_sum = self.get_personunits_credor_weight_sum()
        return (
            x_sum in (0, self._person_credor_pool) or self._person_credor_pool is None
        )

    def is_personunits_debtor_weight_sum_correct(self) -> bool:
        x_sum = self.get_personunits_debtor_weight_sum()
        return self._person_debtor_pool is None or x_sum in (
            self._person_debtor_pool,
            0,
        )

    def get_personunits_credor_weight_sum(self) -> float:
        return sum(
            personunit.get_credor_weight() for personunit in self._persons.values()
        )

    def get_personunits_debtor_weight_sum(self) -> float:
        return sum(
            personunit.get_debtor_weight() for personunit in self._persons.values()
        )

    def _add_to_personunits_world_cred_debt(self, idea_world_importance: float):
        sum_personunit_credor_weight = self.get_personunits_credor_weight_sum()
        sum_personunit_debtor_weight = self.get_personunits_debtor_weight_sum()

        for x_personunit in self._persons.values():
            au_world_cred = (
                idea_world_importance * x_personunit.get_credor_weight()
            ) / sum_personunit_credor_weight

            au_world_debt = (
                idea_world_importance * x_personunit.get_debtor_weight()
            ) / sum_personunit_debtor_weight

            x_personunit.add_world_cred_debt(
                world_cred=au_world_cred,
                world_debt=au_world_debt,
                world_agenda_cred=0,
                world_agenda_debt=0,
            )

    def _add_to_personunits_world_agenda_cred_debt(self, idea_world_importance: float):
        sum_personunit_credor_weight = self.get_personunits_credor_weight_sum()
        sum_personunit_debtor_weight = self.get_personunits_debtor_weight_sum()

        for x_personunit in self._persons.values():
            au_world_agenda_cred = (
                idea_world_importance * x_personunit.get_credor_weight()
            ) / sum_personunit_credor_weight

            au_world_agenda_debt = (
                idea_world_importance * x_personunit.get_debtor_weight()
            ) / sum_personunit_debtor_weight

            x_personunit.add_world_cred_debt(
                world_cred=0,
                world_debt=0,
                world_agenda_cred=au_world_agenda_cred,
                world_agenda_debt=au_world_agenda_debt,
            )

    def _set_personunits_world_agenda_importance(self, world_agenda_importance: float):
        sum_personunit_credor_weight = self.get_personunits_credor_weight_sum()
        sum_personunit_debtor_weight = self.get_personunits_debtor_weight_sum()

        for x_personunit in self._persons.values():
            au_world_agenda_cred = (
                world_agenda_importance * x_personunit.get_credor_weight()
            ) / sum_personunit_credor_weight

            au_world_agenda_debt = (
                world_agenda_importance * x_personunit.get_debtor_weight()
            ) / sum_personunit_debtor_weight

            x_personunit.add_world_agenda_cred_debt(
                world_agenda_cred=au_world_agenda_cred,
                world_agenda_debt=au_world_agenda_debt,
            )

    def _reset_beliefunits_world_cred_debt(self):
        for balancelink_obj in self._beliefs.values():
            balancelink_obj.reset_world_cred_debt()

    def _set_beliefunits_world_importance(
        self, balanceheirs: dict[BeliefID:BalanceLink]
    ):
        for balancelink_obj in balanceheirs.values():
            self.add_to_belief_world_cred_debt(
                belief_id=balancelink_obj.belief_id,
                balanceheir_world_cred=balancelink_obj._world_cred,
                balanceheir_world_debt=balancelink_obj._world_debt,
            )

    def _allot_world_agenda_importance(self):
        for idea in self._idea_dict.values():
            # If there are no balancelines associated with idea
            # allot world_importance via general personunit
            # cred ratio and debt ratio
            # if idea.is_agenda_item() and idea._balancelines == {}:
            if idea.is_agenda_item():
                if idea._balancelines == {}:
                    self._add_to_personunits_world_agenda_cred_debt(
                        idea._world_importance
                    )
                else:
                    for x_balanceline in idea._balancelines.values():
                        self.add_to_belief_world_agenda_cred_debt(
                            belief_id=x_balanceline.belief_id,
                            balanceline_world_cred=x_balanceline._world_cred,
                            balanceline_world_debt=x_balanceline._world_debt,
                        )

    def _allot_beliefs_world_importance(self):
        for belief_obj in self._beliefs.values():
            belief_obj._set_personlink_world_cred_debt()
            for personlink in belief_obj._persons.values():
                self.add_to_personunit_world_cred_debt(
                    personunit_person_id=personlink.person_id,
                    world_cred=personlink._world_cred,
                    world_debt=personlink._world_debt,
                    world_agenda_cred=personlink._world_agenda_cred,
                    world_agenda_debt=personlink._world_agenda_debt,
                )

    def _set_world_agenda_ratio_cred_debt(self):
        world_agenda_ratio_cred_sum = 0
        world_agenda_ratio_debt_sum = 0

        for x_personunit in self._persons.values():
            world_agenda_ratio_cred_sum += x_personunit._world_agenda_cred
            world_agenda_ratio_debt_sum += x_personunit._world_agenda_debt

        for x_personunit in self._persons.values():
            x_personunit.set_world_agenda_ratio_cred_debt(
                world_agenda_ratio_cred_sum=world_agenda_ratio_cred_sum,
                world_agenda_ratio_debt_sum=world_agenda_ratio_debt_sum,
                world_personunit_total_credor_weight=self.get_personunits_credor_weight_sum(),
                world_personunit_total_debtor_weight=self.get_personunits_debtor_weight_sum(),
            )

    def get_person_belief_ids(self, person_id: PersonID) -> list[BeliefID]:
        return [
            x_beliefunit.belief_id
            for x_beliefunit in self._beliefs.values()
            if x_beliefunit.personlink_exists(person_id)
        ]

    def _reset_personunit_world_cred_debt(self):
        for personunit in self._persons.values():
            personunit.reset_world_cred_debt()

    def idea_exists(self, road: RoadUnit) -> bool:
        if road is None:
            return False
        root_road_label = get_root_node_from_road(road, delimiter=self._road_delimiter)
        if root_road_label != self._idearoot._label:
            return False

        nodes = get_all_road_nodes(road, delimiter=self._road_delimiter)
        root_road_label = nodes.pop(0)
        if nodes == []:
            return True

        idea_label = nodes.pop(0)
        x_idea = self._idearoot.get_kid(idea_label)
        if x_idea is None:
            return False
        while nodes != []:
            idea_label = nodes.pop(0)
            x_idea = x_idea.get_kid(idea_label)
            if x_idea is None:
                return False
        return True

    def get_idea_obj(self, road: RoadUnit, if_missing_create: bool = False) -> IdeaUnit:
        if road is None:
            raise InvalidWorldException("get_idea_obj received road=None")
        if self.idea_exists(road) is False and not if_missing_create:
            raise InvalidWorldException(f"get_idea_obj failed. no item at '{road}'")
        roadnodes = get_all_road_nodes(road, delimiter=self._road_delimiter)
        if len(roadnodes) == 1:
            return self._idearoot

        roadnodes.pop(0)
        idea_label = roadnodes.pop(0)
        x_idea = self._idearoot.get_kid(idea_label, if_missing_create)
        while roadnodes != []:
            x_idea = x_idea.get_kid(roadnodes.pop(0), if_missing_create)

        return x_idea

    def get_idea_ranged_kids(
        self, idea_road: str, begin: float = None, close: float = None
    ) -> dict[IdeaUnit]:
        parent_idea = self.get_idea_obj(idea_road)
        if begin is None and close is None:
            begin = parent_idea._begin
            close = parent_idea._close
        elif begin != None and close is None:
            close = begin

        idea_list = parent_idea.get_kids_in_range(begin=begin, close=close)
        return {x_idea._label: x_idea for x_idea in idea_list}

    def _set_ancestors_metrics(self, road: RoadUnit, econ_exceptions: bool = False):
        task_count = 0
        child_balancelines = None
        belief_everyone = None
        ancestor_roads = get_ancestor_roads(road=road)
        econ_justified_by_problem = True
        healerhold_count = 0

        while ancestor_roads != []:
            youngest_road = ancestor_roads.pop(0)
            # _set_non_root_ancestor_metrics(youngest_road, task_count, belief_everyone)
            x_idea_obj = self.get_idea_obj(road=youngest_road)
            x_idea_obj.add_to_descendant_pledge_count(task_count)
            if x_idea_obj.is_kidless():
                x_idea_obj.set_kidless_balancelines()
                child_balancelines = x_idea_obj._balancelines
            else:
                x_idea_obj.set_balancelines(child_balancelines=child_balancelines)

            if x_idea_obj._task:
                task_count += 1

            if (
                belief_everyone != False
                and x_idea_obj._all_person_cred != False
                and x_idea_obj._all_person_debt != False
                and x_idea_obj._balanceheirs != {}
            ) or (
                belief_everyone != False
                and x_idea_obj._all_person_cred is False
                and x_idea_obj._all_person_debt is False
            ):
                belief_everyone = False
            elif belief_everyone != False:
                belief_everyone = True
            x_idea_obj._all_person_cred = belief_everyone
            x_idea_obj._all_person_debt = belief_everyone

            if x_idea_obj._healerhold.any_belief_id_exists():
                econ_justified_by_problem = False
                healerhold_count += 1
                self._sum_healerhold_importance += x_idea_obj._world_importance
            if x_idea_obj._problem_bool:
                econ_justified_by_problem = True

        if econ_justified_by_problem is False or healerhold_count > 1:
            if econ_exceptions:
                raise Exception_econs_justified(
                    f"IdeaUnit '{road}' cannot sponsor ancestor econs."
                )
            self._econs_justified = False

    def _set_root_attributes(self, econ_exceptions: bool):
        x_idearoot = self._idearoot
        x_idearoot._level = 0
        x_idearoot.set_parent_road(parent_road="")
        x_idearoot.set_idearoot_inherit_reasonheirs()
        x_idearoot.set_assignedheir(parent_assignheir=None, world_beliefs=self._beliefs)
        x_idearoot.set_factheirs(facts=self._idearoot._factunits)
        x_idearoot.inherit_balanceheirs()
        x_idearoot.clear_balancelines()
        x_idearoot._weight = 1
        x_idearoot.set_kids_total_weight()
        x_idearoot.set_sibling_total_weight(1)
        x_idearoot.set_active(
            tree_traverse_count=self._tree_traverse_count,
            world_beliefunits=self._beliefs,
            world_owner_id=self._owner_id,
        )
        x_idearoot.set_world_importance(fund_onset_x=0, parent_fund_cease=1)
        x_idearoot.set_balanceheirs_world_cred_debt()
        x_idearoot.set_ancestor_pledge_count(0, False)
        x_idearoot.clear_descendant_pledge_count()
        x_idearoot.clear_all_person_cred_debt()
        x_idearoot.pledge = False

        if x_idearoot.is_kidless():
            self._set_ancestors_metrics(self._idearoot.get_road(), econ_exceptions)
            self._allot_world_importance(idea=self._idearoot)

    def _set_kids_attributes(
        self,
        idea_kid: IdeaUnit,
        fund_onset: float,
        parent_fund_cease: float,
        parent_idea: IdeaUnit,
        econ_exceptions: bool,
    ):
        idea_kid.set_level(parent_level=parent_idea._level)
        idea_kid.set_parent_road(parent_idea.get_road())
        idea_kid.set_factheirs(facts=parent_idea._factheirs)
        idea_kid.set_reasonheirs(self._idea_dict, parent_idea._reasonheirs)
        idea_kid.set_assignedheir(parent_idea._assignedheir, self._beliefs)
        idea_kid.inherit_balanceheirs(parent_idea._balanceheirs)
        idea_kid.clear_balancelines()
        idea_kid.set_active(
            tree_traverse_count=self._tree_traverse_count,
            world_beliefunits=self._beliefs,
            world_owner_id=self._owner_id,
        )
        idea_kid.set_sibling_total_weight(parent_idea._kids_total_weight)
        idea_kid.set_world_importance(
            fund_onset_x=fund_onset,
            parent_world_importance=parent_idea._world_importance,
            parent_fund_cease=parent_fund_cease,
        )
        idea_kid.set_ancestor_pledge_count(
            parent_idea._ancestor_pledge_count, parent_idea.pledge
        )
        idea_kid.clear_descendant_pledge_count()
        idea_kid.clear_all_person_cred_debt()

        if idea_kid.is_kidless():
            # set idea's ancestor metrics using world root as common reference
            self._set_ancestors_metrics(idea_kid.get_road(), econ_exceptions)
            self._allot_world_importance(idea=idea_kid)

    def _allot_world_importance(self, idea: IdeaUnit):
        # TODO manage situations where balanceheir.credor_weight is None for all balanceheirs
        # TODO manage situations where balanceheir.debtor_weight is None for all balanceheirs
        if idea.is_balanceheirless() is False:
            self._set_beliefunits_world_importance(idea._balanceheirs)
        elif idea.is_balanceheirless():
            self._add_to_personunits_world_cred_debt(idea._world_importance)

    def get_world_importance(
        self, parent_world_importance: float, weight: int, sibling_total_weight: int
    ) -> float:
        sibling_ratio = weight / sibling_total_weight
        return parent_world_importance * sibling_ratio

    def _set_tree_traverse_starting_point(self):
        self._rational = False
        self._tree_traverse_count = 0
        self._idea_dict = {self._idearoot.get_road(): self._idearoot}

    def _clear_world_base_metrics(self):
        self._econs_justified = True
        self._econs_buildable = False
        self._sum_healerhold_importance = 0
        self._econ_dict = {}
        self._healers_dict = {}

    def calc_world_metrics(self, econ_exceptions: bool = False):
        self._set_tree_traverse_starting_point()
        max_count = self._max_tree_traverse

        while not self._rational and self._tree_traverse_count < max_count:
            self._clear_world_base_metrics()
            self._execute_tree_traverse(econ_exceptions)
            self._check_if_any_idea_active_status_has_altered()
            self._tree_traverse_count += 1
        self._after_all_tree_traverses_set_cred_debt()
        self._after_all_tree_traverses_set_healerhold_importance()

    def _execute_tree_traverse(self, econ_exceptions: bool = False):
        self._pre_tree_traverse_cred_debt_reset()
        self._set_root_attributes(econ_exceptions)

        fund_onset = self._idearoot._world_fund_onset
        parent_fund_cease = self._idearoot._world_fund_cease

        cache_idea_list = []
        for idea_kid in self._idearoot._kids.values():
            self._set_kids_attributes(
                idea_kid=idea_kid,
                fund_onset=fund_onset,
                parent_fund_cease=parent_fund_cease,
                parent_idea=self._idearoot,
                econ_exceptions=econ_exceptions,
            )
            cache_idea_list.append(idea_kid)
            fund_onset += idea_kid._world_importance

        # no function recursion, recursion by iterateing over list that can be added to by iterations
        while cache_idea_list != []:
            parent_idea = cache_idea_list.pop()
            if self._tree_traverse_count == 0:
                self._idea_dict[parent_idea.get_road()] = parent_idea

            if parent_idea._kids != None:
                fund_onset = parent_idea._world_fund_onset
                parent_fund_cease = parent_idea._world_fund_cease
                for idea_kid in parent_idea._kids.values():
                    self._set_kids_attributes(
                        idea_kid=idea_kid,
                        fund_onset=fund_onset,
                        parent_fund_cease=parent_fund_cease,
                        parent_idea=parent_idea,
                        econ_exceptions=econ_exceptions,
                    )
                    cache_idea_list.append(idea_kid)
                    fund_onset += idea_kid._world_importance

    def _check_if_any_idea_active_status_has_altered(self):
        any_idea_active_status_has_altered = False
        for idea in self._idea_dict.values():
            if idea._active_hx.get(self._tree_traverse_count) != None:
                any_idea_active_status_has_altered = True

        if any_idea_active_status_has_altered is False:
            self._rational = True

    def _after_all_tree_traverses_set_cred_debt(self):
        self._allot_world_agenda_importance()
        self._allot_beliefs_world_importance()
        self._set_world_agenda_ratio_cred_debt()

    def _after_all_tree_traverses_set_healerhold_importance(self):
        self._set_econ_dict()
        self._healers_dict = self._get_healers_dict()
        self._econs_buildable = self._get_buildable_econs()

    def _set_econ_dict(self):
        if self._econs_justified is False:
            self._sum_healerhold_importance = 0
        for x_idea in self._idea_dict.values():
            if self._sum_healerhold_importance == 0:
                x_idea._healerhold_importance = 0
            else:
                x_sum = self._sum_healerhold_importance
                x_idea._healerhold_importance = x_idea._world_importance / x_sum
            if self._econs_justified and x_idea._healerhold.any_belief_id_exists():
                self._econ_dict[x_idea.get_road()] = x_idea

    def _get_healers_dict(self) -> dict[HealerID : dict[RoadUnit:IdeaUnit]]:
        _healers_dict = {}
        for x_econ_road, x_econ_idea in self._econ_dict.items():
            for x_belief_id in x_econ_idea._healerhold._belief_ids:
                x_beliefunit = self.get_beliefunit(x_belief_id)
                for x_person_id in x_beliefunit._persons.keys():
                    if _healers_dict.get(x_person_id) is None:
                        _healers_dict[x_person_id] = {x_econ_road: x_econ_idea}
                    else:
                        healer_dict = _healers_dict.get(x_person_id)
                        healer_dict[x_econ_road] = x_econ_idea
        return _healers_dict

    def _get_buildable_econs(self) -> bool:
        return all(
            is_roadunit_convertible_to_path(econ_road, self._road_delimiter) != False
            for econ_road in self._econ_dict.keys()
        )

    def _pre_tree_traverse_cred_debt_reset(self):
        if self.is_personunits_credor_weight_sum_correct() is False:
            raise PersonUnitsCredorDebtorSumException(
                f"'{self._owner_id}' is_personunits_credor_weight_sum_correct is False. _person_credor_pool={self._person_credor_pool}. personunits_credor_weight_sum={self.get_personunits_credor_weight_sum()}"
            )
        if self.is_personunits_debtor_weight_sum_correct() is False:
            raise PersonUnitsCredorDebtorSumException(
                f"'{self._owner_id}' is_personunits_debtor_weight_sum_correct is False. _person_debtor_pool={self._person_debtor_pool}. personunits_debtor_weight_sum={self.get_personunits_debtor_weight_sum()}"
            )
        self._reset_beliefunits_world_cred_debt()
        self._reset_beliefunits_world_cred_debt()
        self._reset_personunit_world_cred_debt()

    def get_heir_road_list(self, x_road: RoadUnit) -> list[RoadUnit]:
        road_list = self.get_idea_tree_ordered_road_list()
        return [idea_road for idea_road in road_list if is_sub_road(idea_road, x_road)]

    def get_idea_tree_ordered_road_list(
        self, no_range_descendants: bool = False
    ) -> list[RoadUnit]:
        idea_list = list(self.get_idea_dict().values())
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
                    parent_idea = self.get_idea_obj(road=anc_list[1])
                    if parent_idea._begin is None and parent_idea._close is None:
                        list_x.append(road)

        return list_x

    def get_factunits_dict(self) -> dict[str:str]:
        x_dict = {}
        if self._idearoot._factunits != None:
            for fact_road, fact_obj in self._idearoot._factunits.items():
                x_dict[fact_road] = fact_obj.get_dict()
        return x_dict

    def get_persons_dict(self, all_attrs: bool = False) -> dict[str:str]:
        x_dict = {}
        if self._persons != None:
            for person_id, person_obj in self._persons.items():
                x_dict[person_id] = person_obj.get_dict(all_attrs)
        return x_dict

    def get_beliefunits_dict(self) -> dict[str:str]:
        return {
            belief_belief_id: belief_obj.get_dict()
            for belief_belief_id, belief_obj in self._beliefs.items()
            if belief_obj._person_mirror is False
        }

    def get_dict(self) -> dict[str:str]:
        x_dict = {
            "_persons": self.get_persons_dict(),
            "_beliefs": self.get_beliefunits_dict(),
            "_originunit": self._originunit.get_dict(),
            "_weight": self._weight,
            "_pixel": self._pixel,
            "_penny": self._penny,
            "_owner_id": self._owner_id,
            "_real_id": self._real_id,
            "_max_tree_traverse": self._max_tree_traverse,
            "_road_delimiter": self._road_delimiter,
            "_idearoot": self._idearoot.get_dict(),
        }
        if self._person_credor_pool != None:
            x_dict["_person_credor_pool"] = self._person_credor_pool
        if self._person_debtor_pool != None:
            x_dict["_person_debtor_pool"] = self._person_debtor_pool
        if self._meld_strategy != get_meld_default():
            x_dict["_meld_strategy"] = self._meld_strategy
        if self._last_gift_id != None:
            x_dict["_last_gift_id"] = self._last_gift_id

        return x_dict

    def get_json(self) -> str:
        x_dict = self.get_dict()
        return get_json_from_dict(dict_x=x_dict)

    def set_time_hreg_ideas(self, c400_count: int):
        x_hregidea = HregIdea(self._road_delimiter)
        ideabase_list = x_hregidea._get_time_hreg_src_idea(c400_count=c400_count)
        while len(ideabase_list) != 0:
            yb = ideabase_list.pop(0)
            range_source_road_x = None
            if yb.sr != None:
                range_source_road_x = self.make_l1_road(yb.sr)

            x_idea = ideaunit_shop(
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
            self.add_idea(x_idea, parent_road=road_x)

            numeric_road_x = None
            if yb.nr != None:
                numeric_road_x = self.make_l1_road(yb.nr)
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

        self.calc_world_metrics()

    def get_world4person(self, person_id: PersonID, facts: dict[RoadUnit:FactCore]):
        self.calc_world_metrics()
        world4person = worldunit_shop(_owner_id=person_id)
        world4person._idearoot._world_importance = self._idearoot._world_importance
        # get person's persons: personzone

        # get personzone beliefs
        person_beliefs = self.get_person_belief_ids(person_id=person_id)

        # set world4person by traversing the idea tree and selecting associated beliefs
        # set root
        not_included_world_importance = 0
        world4person._idearoot.clear_kids()
        for ykx in self._idearoot._kids.values():
            y4a_included = any(
                belief_ancestor.belief_id in person_beliefs
                for belief_ancestor in ykx._balancelines.values()
            )

            if y4a_included:
                y4a_new = ideaunit_shop(
                    _label=ykx._label,
                    _world_importance=ykx._world_importance,
                    _reasonunits=ykx._reasonunits,
                    _balancelinks=ykx._balancelinks,
                    _begin=ykx._begin,
                    _close=ykx._close,
                    pledge=ykx.pledge,
                    _task=ykx._task,
                )
                world4person._idearoot._kids[ykx._label] = y4a_new
            else:
                not_included_world_importance += ykx._world_importance

        if not_included_world_importance > 0:
            y4a_exterior = ideaunit_shop(
                _label="__world4person__",
                _world_importance=not_included_world_importance,
            )
            world4person._idearoot._kids[y4a_exterior._label] = y4a_exterior

        return world4person

    def set_dominate_pledge_idea(self, idea_kid: IdeaUnit):
        idea_kid.pledge = True
        self.add_idea(
            idea_kid=idea_kid,
            parent_road=self.make_road(idea_kid._parent_road),
            create_missing_beliefs=True,
            create_missing_ideas=True,
        )

    def get_idea_list_without_idearoot(self) -> list[IdeaUnit]:
        self.calc_world_metrics()
        x_list = list(self._idea_dict.values())
        x_list.pop(0)
        return x_list

    def set_meld_strategy(self, x_meld_strategy: MeldStrategy):
        self._meld_strategy = validate_meld_strategy(x_meld_strategy)

    def meld(
        self,
        exterior_world,
        person_weight: float = None,
        ignore_personunits: bool = False,
    ):
        self._meld_beliefs(exterior_world)
        if not ignore_personunits:
            self._meld_persons(exterior_world)
        self._meld_ideas(exterior_world, person_weight)
        self._meld_facts(exterior_world)
        self._weight = get_meld_weight(
            src_weight=self._weight,
            src_meld_strategy="default",
            exterior_weight=exterior_world._weight,
            exterior_meld_strategy="default",
        )
        self._meld_originlinks(exterior_world._owner_id, person_weight)

    def _meld_ideas(self, exterior_world, person_weight: float):
        # meld idearoot
        self._idearoot.meld(exterior_idea=exterior_world._idearoot, _idearoot=True)

        # meld all exterior ideas
        person_id = exterior_world._owner_id
        o_idea_list = exterior_world.get_idea_list_without_idearoot()
        for o_idea in o_idea_list:
            o_road = road_validate(
                self.make_road(o_idea._parent_road, o_idea._label),
                self._road_delimiter,
                self._real_id,
            )
            try:
                main_idea = self.get_idea_obj(o_road)
                main_idea.meld(o_idea, False, person_id, person_weight)
            except Exception:
                self.add_idea(idea_kid=o_idea, parent_road=o_idea._parent_road)
                main_idea = self.get_idea_obj(o_road)
                main_idea._originunit.set_originlink(person_id, person_weight)

    def _meld_persons(self, exterior_world):
        for personunit in exterior_world._persons.values():
            if self.get_person(personunit.person_id) is None:
                self.set_personunit(personunit=personunit)
            else:
                self.get_person(personunit.person_id).meld(personunit)

    def _meld_beliefs(self, exterior_world):
        for brx in exterior_world._beliefs.values():
            if self.get_beliefunit(brx.belief_id) is None:
                self.set_beliefunit(y_beliefunit=brx)
            else:
                self.get_beliefunit(brx.belief_id).meld(brx)

    def _meld_facts(self, exterior_world):
        for hx in exterior_world._idearoot._factunits.values():
            if self._idearoot._factunits.get(hx.base) is None:
                self.set_fact(base=hx.base, pick=hx.fact, open=hx.open, nigh=hx.nigh)
            else:
                self._idearoot._factunits.get(hx.base).meld(hx)

    def _meld_originlinks(self, person_id: PersonID, person_weight: float):
        if person_id != None:
            self._originunit.set_originlink(person_id, person_weight)

    def get_assignment(
        self,
        world_x,
        assignor_persons: dict[PersonID:PersonUnit],
        assignor_person_id: PersonID,
    ) -> any:
        self.calc_world_metrics()
        self._set_assignment_persons(world_x, assignor_persons, assignor_person_id)
        self._set_assignment_beliefs(world_x)
        assignor_pledges = self._get_assignor_pledge_ideas(world_x, assignor_person_id)
        relevant_roads = self._get_relevant_roads(assignor_pledges)
        self._set_assignment_ideas(world_x, relevant_roads)
        return world_x

    def _set_assignment_ideas(self, x_world, relevant_roads: dict[RoadUnit:str]):
        sorted_relevants = sorted(list(relevant_roads))
        # difficult to know how to manage root idea attributes...
        if sorted_relevants != []:
            root_road = sorted_relevants.pop(0)

        for relevant_road in sorted_relevants:
            relevant_idea = copy_deepcopy(self.get_idea_obj(relevant_road))
            relevant_idea.find_replace_road(
                old_road=get_root_node_from_road(relevant_road, self._road_delimiter),
                new_road=x_world._real_id,
            )
            relevant_idea.clear_kids()
            x_world.add_idea(relevant_idea, parent_road=relevant_idea._parent_road)

        for afu in self._idearoot._factunits.values():
            if relevant_roads.get(afu.base) != None:
                x_world.set_fact(
                    base=rebuild_road(afu.base, self._real_id, x_world._real_id),
                    pick=rebuild_road(afu.pick, self._real_id, x_world._real_id),
                    open=afu.open,
                    nigh=afu.nigh,
                )

    def _set_assignment_persons(
        self,
        world_x,
        assignor_persons: dict[PersonID:PersonUnit],
        assignor_person_id: PersonID,
    ):
        if self.person_exists(assignor_person_id):
            # get all persons that are both in self._persons and assignor_known_persons
            persons_set = get_intersection_of_persons(self._persons, assignor_persons)
            for person_id_x in persons_set:
                world_x.set_personunit(personunit=self.get_person(person_id_x))
        return world_x

    def _set_assignment_beliefs(self, world_x):
        revelant_beliefs = get_persons_relevant_beliefs(self._beliefs, world_x._persons)
        for belief_belief_id, belief_persons in revelant_beliefs.items():
            if world_x._beliefs.get(belief_belief_id) is None:
                belief_x = beliefunit_shop(belief_id=belief_belief_id)
                for person_id in belief_persons:
                    belief_x.set_personlink(personlink_shop(person_id=person_id))
                world_x.set_beliefunit(belief_x)

    def _get_assignor_pledge_ideas(
        self, world_x, assignor_person_id: BeliefID
    ) -> dict[RoadUnit:int]:
        assignor_beliefs = get_person_relevant_beliefs(
            world_x._beliefs, assignor_person_id
        )
        return {
            idea_road: -1
            for idea_road, x_idea in self._idea_dict.items()
            if (x_idea.assignor_in(assignor_beliefs) and x_idea.pledge)
        }


def worldunit_shop(
    _owner_id: OwnerID = None,
    _real_id: RealID = None,
    _road_delimiter: str = None,
    _pixel: float = None,
    _penny: float = None,
    _weight: float = None,
    _meld_strategy: MeldStrategy = None,
) -> WorldUnit:
    if _owner_id is None:
        _owner_id = ""
    if _real_id is None:
        _real_id = get_default_real_id_roadnode()
    if _meld_strategy is None:
        _meld_strategy = get_meld_default()

    x_world = WorldUnit(
        _owner_id=_owner_id,
        _weight=get_1_if_None(_weight),
        _real_id=_real_id,
        _persons=get_empty_dict_if_none(None),
        _beliefs=get_empty_dict_if_none(None),
        _idea_dict=get_empty_dict_if_none(None),
        _econ_dict=get_empty_dict_if_none(None),
        _healers_dict=get_empty_dict_if_none(None),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _pixel=default_pixel_if_none(_pixel),
        _penny=default_penny_if_none(_penny),
        _meld_strategy=validate_meld_strategy(_meld_strategy),
        _econs_justified=get_False_if_None(),
        _econs_buildable=get_False_if_None(),
        _sum_healerhold_importance=get_0_if_None(),
    )
    x_world._idearoot = ideaunit_shop(
        _root=True, _uid=1, _level=0, _world_real_id=x_world._real_id
    )
    x_world._idearoot._road_delimiter = x_world._road_delimiter
    x_world.set_max_tree_traverse(3)
    x_world._rational = False
    x_world._originunit = originunit_shop()
    return x_world


def get_from_json(x_world_json: str) -> WorldUnit:
    return get_from_dict(get_dict_from_json(x_world_json))


def get_from_dict(world_dict: dict) -> WorldUnit:
    x_world = worldunit_shop()
    x_world.set_owner_id(get_obj_from_world_dict(world_dict, "_owner_id"))
    x_world._weight = get_obj_from_world_dict(world_dict, "_weight")
    x_world.set_max_tree_traverse(
        get_obj_from_world_dict(world_dict, "_max_tree_traverse")
    )
    x_world.set_real_id(get_obj_from_world_dict(world_dict, "_real_id"))
    x_world._road_delimiter = default_road_delimiter_if_none(
        get_obj_from_world_dict(world_dict, "_road_delimiter")
    )
    x_world._pixel = default_pixel_if_none(
        get_obj_from_world_dict(world_dict, "_pixel")
    )
    x_world._penny = default_penny_if_none(
        get_obj_from_world_dict(world_dict, "_penny")
    )
    x_world._person_credor_pool = get_obj_from_world_dict(
        world_dict, "_person_credor_pool"
    )
    x_world._person_debtor_pool = get_obj_from_world_dict(
        world_dict, "_person_debtor_pool"
    )
    if get_obj_from_world_dict(world_dict, "_meld_strategy") is None:
        x_world._meld_strategy = get_meld_default()
    else:
        x_world._meld_strategy = get_obj_from_world_dict(world_dict, "_meld_strategy")
    x_world._last_gift_id = get_obj_from_world_dict(world_dict, "_last_gift_id")
    for x_personunit in get_obj_from_world_dict(
        world_dict, dict_key="_persons", _road_delimiter=x_world._road_delimiter
    ).values():
        x_world.set_personunit(x_personunit)
    for x_beliefunit in get_obj_from_world_dict(
        world_dict, dict_key="_beliefs", _road_delimiter=x_world._road_delimiter
    ).values():
        x_world.set_beliefunit(x_beliefunit)
    x_world._originunit = get_obj_from_world_dict(world_dict, "_originunit")

    set_idearoot_from_world_dict(x_world, world_dict)
    x_world.calc_world_metrics()  # clean up tree traverse defined fields
    return x_world


def set_idearoot_from_world_dict(x_world: WorldUnit, world_dict: dict):
    idearoot_dict = world_dict.get("_idearoot")
    x_world._idearoot = ideaunit_shop(
        _root=True,
        _label=x_world._real_id,
        _uid=get_obj_from_idea_dict(idearoot_dict, "_uid"),
        _weight=get_obj_from_idea_dict(idearoot_dict, "_weight"),
        _begin=get_obj_from_idea_dict(idearoot_dict, "_begin"),
        _close=get_obj_from_idea_dict(idearoot_dict, "_close"),
        _numor=get_obj_from_idea_dict(idearoot_dict, "_numor"),
        _denom=get_obj_from_idea_dict(idearoot_dict, "_denom"),
        _reest=get_obj_from_idea_dict(idearoot_dict, "_reest"),
        _problem_bool=get_obj_from_idea_dict(idearoot_dict, "_problem_bool"),
        _range_source_road=get_obj_from_idea_dict(idearoot_dict, "_range_source_road"),
        _numeric_road=get_obj_from_idea_dict(idearoot_dict, "_numeric_road"),
        _reasonunits=get_obj_from_idea_dict(idearoot_dict, "_reasonunits"),
        _assignedunit=get_obj_from_idea_dict(idearoot_dict, "_assignedunit"),
        _healerhold=get_obj_from_idea_dict(idearoot_dict, "_healerhold"),
        _factunits=get_obj_from_idea_dict(idearoot_dict, "_factunits"),
        _balancelinks=get_obj_from_idea_dict(idearoot_dict, "_balancelinks"),
        _is_expanded=get_obj_from_idea_dict(idearoot_dict, "_is_expanded"),
        _road_delimiter=get_obj_from_idea_dict(idearoot_dict, "_road_delimiter"),
        _world_real_id=x_world._real_id,
    )
    set_idearoot_kids_from_dict(x_world, idearoot_dict)


def set_idearoot_kids_from_dict(x_world: WorldUnit, idearoot_dict: dict):
    to_evaluate_idea_dicts = []
    parent_road_text = "parent_road"
    # for every kid dict, set parent_road in dict, add to to_evaluate_list
    for x_dict in get_obj_from_idea_dict(idearoot_dict, "_kids").values():
        x_dict[parent_road_text] = x_world._real_id
        to_evaluate_idea_dicts.append(x_dict)

    while to_evaluate_idea_dicts != []:
        idea_dict = to_evaluate_idea_dicts.pop(0)
        # for every kid dict, set parent_road in dict, add to to_evaluate_list
        for kid_dict in get_obj_from_idea_dict(idea_dict, "_kids").values():
            parent_road = get_obj_from_idea_dict(idea_dict, parent_road_text)
            kid_label = get_obj_from_idea_dict(idea_dict, "_label")
            kid_dict[parent_road_text] = x_world.make_road(parent_road, kid_label)
            to_evaluate_idea_dicts.append(kid_dict)

        x_ideakid = ideaunit_shop(
            _label=get_obj_from_idea_dict(idea_dict, "_label"),
            _weight=get_obj_from_idea_dict(idea_dict, "_weight"),
            _uid=get_obj_from_idea_dict(idea_dict, "_uid"),
            _begin=get_obj_from_idea_dict(idea_dict, "_begin"),
            _close=get_obj_from_idea_dict(idea_dict, "_close"),
            _numor=get_obj_from_idea_dict(idea_dict, "_numor"),
            _denom=get_obj_from_idea_dict(idea_dict, "_denom"),
            _reest=get_obj_from_idea_dict(idea_dict, "_reest"),
            pledge=get_obj_from_idea_dict(idea_dict, "pledge"),
            _problem_bool=get_obj_from_idea_dict(idea_dict, "_problem_bool"),
            _reasonunits=get_obj_from_idea_dict(idea_dict, "_reasonunits"),
            _assignedunit=get_obj_from_idea_dict(idea_dict, "_assignedunit"),
            _healerhold=get_obj_from_idea_dict(idea_dict, "_healerhold"),
            _originunit=get_obj_from_idea_dict(idea_dict, "_originunit"),
            _balancelinks=get_obj_from_idea_dict(idea_dict, "_balancelinks"),
            _factunits=get_obj_from_idea_dict(idea_dict, "_factunits"),
            _is_expanded=get_obj_from_idea_dict(idea_dict, "_is_expanded"),
            _range_source_road=get_obj_from_idea_dict(idea_dict, "_range_source_road"),
            _numeric_road=get_obj_from_idea_dict(idea_dict, "_numeric_road"),
            _world_real_id=x_world._real_id,
        )
        x_world.add_idea(x_ideakid, parent_road=idea_dict[parent_road_text])


def get_obj_from_world_dict(
    x_dict: dict[str:], dict_key: str, _road_delimiter: str = None
) -> any:
    if dict_key == "_originunit":
        return (
            originunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else originunit_shop()
        )
    elif dict_key == "_persons":
        return (
            personunits_get_from_dict(x_dict[dict_key], _road_delimiter)
            if x_dict.get(dict_key) != None
            else personunits_get_from_dict(x_dict[dict_key], _road_delimiter)
        )
    elif dict_key == "_beliefs":
        return (
            get_beliefunits_from_dict(x_dict[dict_key], _road_delimiter)
            if x_dict.get(dict_key) != None
            else get_beliefunits_from_dict(x_dict[dict_key], _road_delimiter)
        )
    elif dict_key == "_max_tree_traverse":
        return (
            x_dict[dict_key]
            if x_dict.get(dict_key) != None
            else max_tree_traverse_default()
        )
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None


def get_dict_of_world_from_dict(x_dict: dict[str:dict]) -> dict[str:WorldUnit]:
    worldunits = {}
    for worldunit_dict in x_dict.values():
        x_world = get_from_dict(world_dict=worldunit_dict)
        worldunits[x_world._owner_id] = x_world
    return worldunits
