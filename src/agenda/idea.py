from dataclasses import dataclass
from src._road.road import (
    RoadUnit,
    RoadNode,
    is_sub_road,
    get_default_world_id_roadnode as root_label,
    create_road as road_create_road,
    default_road_delimiter_if_none,
    replace_road_delimiter,
    WorldID,
)
from src.agenda.meld import get_meld_default
from src.agenda.healer import HealerHold, healerhold_shop, healerhold_get_from_dict
from src.agenda.reason_assign import (
    AssignedUnit,
    AssignedHeir,
    assignedunit_shop,
    assigned_heir_shop,
    assignedunit_get_from_dict,
)
from src.agenda.reason_idea import (
    BeliefCore,
    BeliefHeir,
    beliefheir_shop,
    ReasonCore,
    ReasonUnit,
    reasonunit_shop,
    RoadUnit,
    BeliefUnit,
    beliefunit_shop,
    ReasonHeir,
    reasonheir_shop,
    RoadUnit,
    change_road,
    find_replace_road_key_dict,
    reasons_get_from_dict,
    beliefunits_get_from_dict,
)
from src.agenda.group import (
    BalanceHeir,
    BalanceLink,
    balancelinks_get_from_dict,
    GroupID,
    BalanceLine,
    balanceline_shop,
    balanceheir_shop,
    GroupUnit,
)
from src.agenda.origin import OriginUnit, originunit_get_from_dict
from src.agenda.party import PartyID
from src.agenda.origin import originunit_shop
from src.instrument.python import (
    get_empty_dict_if_none,
    get_1_if_None,
    get_0_if_None,
    get_False_if_None,
)
from src.agenda.meld import get_meld_weight, validate_meld_strategy
from copy import deepcopy


class InvalidIdeaException(Exception):
    pass


class IdeaGetDescendantsException(Exception):
    pass


@dataclass
class IdeaAttrFilter:
    weight: int = None
    uid: int = None
    reason: ReasonUnit = None
    reason_base: RoadUnit = None
    reason_premise: RoadUnit = None
    reason_premise_open: float = None
    reason_premise_nigh: float = None
    reason_premise_divisor: int = None
    reason_del_premise_base: RoadUnit = None
    reason_del_premise_need: RoadUnit = None
    reason_suff_idea_active: str = None
    assignedunit: AssignedUnit = None
    healerhold: HealerHold = None
    begin: float = None
    close: float = None
    addin: float = None
    numor: float = None
    denom: float = None
    reest: bool = None
    numeric_road: RoadUnit = None
    range_source_road: float = None
    promise: bool = None
    beliefunit: BeliefUnit = None
    descendant_promise_count: int = None
    all_party_credit: bool = None
    all_party_debt: bool = None
    balancelink: BalanceLink = None
    balancelink_del: GroupID = None
    is_expanded: bool = None
    meld_strategy: str = None
    problem_bool: bool = None

    def get_premise_need(self):
        return self.reason_premise

    def set_premise_range_attributes_influenced_by_premise_idea(
        self,
        premise_open,
        premise_nigh,
        # premise_numor,
        premise_denom,
        # premise_reest,
    ):
        if self.reason_premise != None:
            if self.reason_premise_open is None:
                self.reason_premise_open = premise_open
            if self.reason_premise_nigh is None:
                self.reason_premise_nigh = premise_nigh
            # if self.reason_premise_numor is None:
            #     numor_x = premise_numor
            if self.reason_premise_divisor is None:
                self.reason_premise_divisor = premise_denom
            # if self.reason_premise_reest is None:
            #     self.reason_premise_reest = premise_reest

    def has_numeric_attrs(self):
        return (
            self.begin != None
            or self.close != None
            or self.numor != None
            or self.numeric_road != None
            or self.addin != None
        )

    def has_ratio_attrs(self):
        return (
            self.denom != None or self.numor != None or self.reest or self.addin != None
        )

    def set_ratio_attr_defaults_if_none(self):
        if self.addin is None:
            self.addin = 0
        if self.denom is None:
            self.denom = 1
        if self.numor is None:
            self.numor = 1
        if self.reest is None:
            self.reest = False

    def has_reason_premise(self):
        return self.reason_premise != None


def ideaattrfilter_shop(
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
    promise: bool = None,
    beliefunit: BeliefUnit = None,
    descendant_promise_count: int = None,
    all_party_credit: bool = None,
    all_party_debt: bool = None,
    balancelink: BalanceLink = None,
    balancelink_del: GroupID = None,
    is_expanded: bool = None,
    meld_strategy: str = None,
    problem_bool: bool = None,
) -> IdeaAttrFilter:
    x_ideaattrfilter = IdeaAttrFilter(
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
        promise=promise,
        beliefunit=beliefunit,
        descendant_promise_count=descendant_promise_count,
        all_party_credit=all_party_credit,
        all_party_debt=all_party_debt,
        balancelink=balancelink,
        balancelink_del=balancelink_del,
        is_expanded=is_expanded,
        meld_strategy=meld_strategy,
        problem_bool=problem_bool,
    )
    if x_ideaattrfilter.has_ratio_attrs():
        x_ideaattrfilter.set_ratio_attr_defaults_if_none()
    return x_ideaattrfilter


@dataclass
class IdeaUnit:
    _label: RoadNode = None
    _weight: int = None
    _parent_road: RoadUnit = None
    _root: bool = None
    _kids: dict = None
    _agenda_world_id: WorldID = None
    _uid: int = None  # Calculated field?
    _balancelinks: dict[GroupID:BalanceLink] = None
    _balanceheirs: dict[GroupID:BalanceHeir] = None  # Calculated field
    _balancelines: dict[GroupID:BalanceLine] = None  # Calculated field
    _reasonunits: dict[RoadUnit:ReasonUnit] = None
    _reasonheirs: dict[RoadUnit:ReasonHeir] = None  # Calculated field
    _assignedunit: AssignedUnit = None
    _assignedheir: AssignedHeir = None  # Calculated field
    _beliefunits: dict[RoadUnit:BeliefUnit] = None
    _beliefheirs: dict[RoadUnit:BeliefHeir] = None  # Calculated field
    _healerhold: HealerHold = None
    _begin: float = None
    _close: float = None
    _addin: float = None
    _denom: int = None
    _numor: int = None
    _reest: bool = None
    _range_source_road: RoadUnit = None
    _numeric_road: RoadUnit = None
    promise: bool = None
    _originunit: OriginUnit = None
    _meld_strategy: str = None
    _problem_bool: bool = None
    # Calculated fields
    _level: int = None
    _kids_total_weight: int = None
    _agenda_importance: float = None
    _agenda_fund_onset: float = None
    _agenda_fund_cease: float = None
    _task: bool = None
    _active: bool = None
    _ancestor_promise_count: int = None
    _descendant_promise_count: int = None
    _all_party_credit: bool = None
    _all_party_debt: bool = None
    _is_expanded: bool = None
    _sibling_total_weight: int = None
    _active_hx: dict[int:bool] = None
    _road_delimiter: str = None
    _healerhold_importance: float = None

    def is_intent_item(self, necessary_base: RoadUnit = None) -> bool:
        # bool_x = False
        return (
            self.promise
            and self._active
            and self.base_reasonunit_exists(necessary_base)
        )

    def base_reasonunit_exists(self, necessary_base: RoadUnit = None) -> bool:
        return necessary_base is None or any(
            reason.base == necessary_base for reason in self._reasonunits.values()
        )

    def record_active_hx(
        self,
        tree_traverse_count: int,
        prev_active: bool,
        curr_active: bool,
    ):
        if tree_traverse_count == 0:
            self._active_hx = {0: curr_active}
        elif prev_active != curr_active:
            self._active_hx[tree_traverse_count] = curr_active

    def set_beliefheirs(self, beliefs: dict[RoadUnit:BeliefCore]):
        beliefs = get_empty_dict_if_none(x_dict=beliefs)
        self._beliefheirs = {}
        for h in beliefs.values():
            x_belief = beliefheir_shop(
                base=h.base, pick=h.pick, open=h.open, nigh=h.nigh
            )
            self.delete_beliefunit_if_past(beliefheir=x_belief)
            x_belief = self.apply_beliefunit_transformations(beliefheir=x_belief)
            self._beliefheirs[x_belief.base] = x_belief

    def apply_beliefunit_transformations(self, beliefheir: BeliefHeir) -> BeliefHeir:
        for beliefunit in self._beliefunits.values():
            if beliefunit.base == beliefheir.base:
                beliefheir.transform(beliefunit=beliefunit)
        return beliefheir

    def delete_beliefunit_if_past(self, beliefheir: BeliefHeir):
        delete_beliefunit = False
        for beliefunit in self._beliefunits.values():
            if (
                beliefunit.base == beliefheir.base
                and beliefunit.nigh != None
                and beliefheir.open != None
            ) and beliefunit.nigh < beliefheir.open:
                delete_beliefunit = True

        if delete_beliefunit:
            del self._beliefunits[beliefunit.base]

    def set_beliefunit(self, beliefunit: BeliefUnit):
        self._beliefunits[beliefunit.base] = beliefunit

    def get_beliefunits_dict(self) -> dict[RoadUnit:BeliefUnit]:
        return {hc.base: hc.get_dict() for hc in self._beliefunits.values()}

    def set_beliefunit_to_complete(self, base_beliefunit: BeliefUnit):
        # if a idea is considered a task then a beliefheir.open attribute can be increased to
        # a number <= beliefheir.nigh so the idea no longer is a task. This method finds
        # the minimal beliefheir.open to change idea._task == False. idea_core._beliefheir cannot be straight up manpulated
        # so it is mandatory that idea._beliefunit is changed.
        # self.set_beliefunits(base=belief, belief=base, open=premise_nigh, nigh=belief_nigh)
        self._beliefunits[base_beliefunit.base] = beliefunit_shop(
            base=base_beliefunit.base,
            pick=base_beliefunit.base,
            open=base_beliefunit.nigh,
            nigh=base_beliefunit.nigh,
        )

    def del_beliefunit(self, base: RoadUnit):
        self._beliefunits.pop(base)

    def _apply_any_range_source_road_connections(
        self,
        lemmas_dict: dict[RoadUnit:BeliefUnit],
        missing_beliefs: list[BeliefUnit],
    ):
        for current_belief in self._beliefunits.values():
            for lemma_belief in lemmas_dict.values():
                if lemma_belief.base == current_belief.base:
                    self.set_beliefunit(lemma_belief)

        for missing_belief in missing_beliefs:
            for lemma_belief in lemmas_dict.values():
                if lemma_belief.base == missing_belief:
                    self.set_beliefunit(lemma_belief)

    def set_agenda_importance(
        self,
        fund_onset_x: float,
        parent_agenda_importance: float = None,
        parent_fund_cease: float = None,
    ):
        parent_agenda_importance = get_1_if_None(parent_agenda_importance)
        self.set_kids_total_weight()
        self._agenda_importance = None
        self._agenda_fund_onset = None
        self._agenda_fund_cease = None
        sibling_ratio = self._weight / self._sibling_total_weight
        self._agenda_importance = parent_agenda_importance * sibling_ratio
        self._agenda_fund_onset = fund_onset_x
        self._agenda_fund_cease = self._agenda_fund_onset + self._agenda_importance
        self._agenda_fund_cease = min(self._agenda_fund_cease, parent_fund_cease)
        self.set_balanceheirs_agenda_credit_debt()

    def get_kids_in_range(self, begin: float, close: float) -> list:
        return [
            x_idea
            for x_idea in self._kids.values()
            if (
                (begin >= x_idea._begin and begin < x_idea._close)
                or (close > x_idea._begin and close < x_idea._close)
                or (begin <= x_idea._begin and close >= x_idea._close)
            )
        ]

    def get_obj_key(self) -> RoadNode:
        return self._label

    def get_road(self) -> RoadUnit:
        if self._parent_road in (None, ""):
            return road_create_road(self._label, delimiter=self._road_delimiter)
        else:
            return road_create_road(
                self._parent_road, self._label, delimiter=self._road_delimiter
            )

    def clear_descendant_promise_count(self):
        self._descendant_promise_count = None

    def set_descendant_promise_count_zero_if_null(self):
        if self._descendant_promise_count is None:
            self._descendant_promise_count = 0

    def add_to_descendant_promise_count(self, x_int: int):
        self.set_descendant_promise_count_zero_if_null()
        self._descendant_promise_count += x_int

    def get_descendant_roads_from_kids(self) -> dict[RoadUnit:int]:
        descendant_roads = {}
        to_evaluate_ideas = list(self._kids.values())
        count_x = 0
        max_count = 1000
        while to_evaluate_ideas != [] and count_x < max_count:
            x_idea = to_evaluate_ideas.pop()
            descendant_roads[x_idea.get_road()] = -1
            to_evaluate_ideas.extend(x_idea._kids.values())
            count_x += 1

        if count_x == max_count:
            raise IdeaGetDescendantsException(
                f"Idea '{self.get_road()}' either has an infinite loop or more than {max_count} descendants."
            )

        return descendant_roads

    def clear_all_party_credit_debt(self):
        self._all_party_credit = None
        self._all_party_debt = None

    def set_ancestor_promise_count(
        self, parent_ancestor_promise_count: int, parent_promise: bool
    ):
        x_int = 0
        x_int = 1 if parent_promise else 0
        self._ancestor_promise_count = parent_ancestor_promise_count + x_int

    def set_sibling_total_weight(self, parent_kids_total_weight):
        self._sibling_total_weight = parent_kids_total_weight

    def set_level(self, parent_level):
        self._level = parent_level + 1

    def set_parent_road(self, parent_road):
        self._parent_road = parent_road

    def inherit_balanceheirs(
        self, parent_balanceheirs: dict[GroupID:BalanceHeir] = None
    ):
        if parent_balanceheirs is None:
            parent_balanceheirs = {}

        self._balanceheirs = {}
        for ib in parent_balanceheirs.values():
            balanceheir = balanceheir_shop(
                group_id=ib.group_id,
                creditor_weight=ib.creditor_weight,
                debtor_weight=ib.debtor_weight,
            )
            self._balanceheirs[balanceheir.group_id] = balanceheir

        for ib in self._balancelinks.values():
            balanceheir = balanceheir_shop(
                group_id=ib.group_id,
                creditor_weight=ib.creditor_weight,
                debtor_weight=ib.debtor_weight,
            )
            self._balanceheirs[balanceheir.group_id] = balanceheir

    def set_kidless_balancelines(self):
        # get balancelines from self
        for bh in self._balanceheirs.values():
            x_balanceline = balanceline_shop(
                group_id=bh.group_id,
                _agenda_credit=bh._agenda_credit,
                _agenda_debt=bh._agenda_debt,
            )
            self._balancelines[x_balanceline.group_id] = x_balanceline

    def set_balancelines(self, child_balancelines: dict[GroupID:BalanceLine] = None):
        if child_balancelines is None:
            child_balancelines = {}

        # get balancelines from child
        for bl in child_balancelines.values():
            if self._balancelines.get(bl.group_id) is None:
                self._balancelines[bl.group_id] = balanceline_shop(
                    group_id=bl.group_id,
                    _agenda_credit=0,
                    _agenda_debt=0,
                )

            self._balancelines[bl.group_id].add_agenda_credit_debt(
                agenda_credit=bl._agenda_credit, agenda_debt=bl._agenda_debt
            )

    def set_kids_total_weight(self):
        self._kids_total_weight = 0
        for x_idea in self._kids.values():
            self._kids_total_weight += x_idea._weight

    def get_balanceheirs_creditor_weight_sum(self) -> float:
        return sum(
            balancelink.creditor_weight for balancelink in self._balanceheirs.values()
        )

    def get_balanceheirs_debtor_weight_sum(self) -> float:
        return sum(
            balancelink.debtor_weight for balancelink in self._balanceheirs.values()
        )

    def set_balanceheirs_agenda_credit_debt(self):
        balanceheirs_creditor_weight_sum = self.get_balanceheirs_creditor_weight_sum()
        balanceheirs_debtor_weight_sum = self.get_balanceheirs_debtor_weight_sum()
        for balanceheir_x in self._balanceheirs.values():
            balanceheir_x.set_agenda_credit_debt(
                idea_agenda_importance=self._agenda_importance,
                balanceheirs_creditor_weight_sum=balanceheirs_creditor_weight_sum,
                balanceheirs_debtor_weight_sum=balanceheirs_debtor_weight_sum,
            )

    def clear_balancelines(self):
        self._balancelines = {}

    def set_idea_label(self, _label: str):
        if (
            self._root
            and _label != None
            and _label != self._agenda_world_id
            and self._agenda_world_id != None
        ):
            raise Idea_root_LabelNotEmptyException(
                f"Cannot set idearoot to string other than '{self._agenda_world_id}'"
            )
        elif self._root and self._agenda_world_id is None:
            self._label = root_label()
        # elif _label != None:
        else:
            self._label = _label

    def set_road_delimiter(self, new_road_delimiter: str):
        old_delimiter = deepcopy(self._road_delimiter)
        if old_delimiter is None:
            old_delimiter = default_road_delimiter_if_none()
        self._road_delimiter = default_road_delimiter_if_none(new_road_delimiter)
        if old_delimiter != self._road_delimiter:
            self._find_replace_road_delimiter(old_delimiter)

    def _find_replace_road_delimiter(self, old_delimiter):
        self._parent_road = replace_road_delimiter(
            road=self._parent_road,
            old_delimiter=old_delimiter,
            new_delimiter=self._road_delimiter,
        )
        if self._numeric_road != None:
            self._numeric_road = replace_road_delimiter(
                road=self._numeric_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )
        if self._range_source_road != None:
            self._range_source_road = replace_road_delimiter(
                road=self._range_source_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )

        new_reasonunits = {}
        for reasonunit_road, reasonunit_obj in self._reasonunits.items():
            new_reasonunit_road = replace_road_delimiter(
                road=reasonunit_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )
            reasonunit_obj.set_delimiter(self._road_delimiter)
            new_reasonunits[new_reasonunit_road] = reasonunit_obj
        self._reasonunits = new_reasonunits

        new_beliefunits = {}
        for beliefunit_road, beliefunit_obj in self._beliefunits.items():
            new_base_road = replace_road_delimiter(
                road=beliefunit_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )
            beliefunit_obj.base = new_base_road
            new_pick_road = replace_road_delimiter(
                road=beliefunit_obj.pick,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )
            beliefunit_obj.set_attr(pick=new_pick_road)
            new_beliefunits[new_base_road] = beliefunit_obj
        self._beliefunits = new_beliefunits

    def _meld_reasonunits(self, other_idea):
        for lx in other_idea._reasonunits.values():
            if self._reasonunits.get(lx.base) is None:
                self._reasonunits[lx.base] = lx
            else:
                self._reasonunits.get(lx.base).meld(lx)

    def _meld_balancelinks(self, other_idea):
        for bl in other_idea._balancelinks.values():
            if self._balancelinks.get(bl.group_id) != None:
                self._balancelinks.get(bl.group_id).meld(
                    other_balancelink=bl,
                    other_meld_strategy=other_idea._meld_strategy,
                    src_meld_strategy=self._meld_strategy,
                )
            else:
                self._balancelinks[bl.group_id] = bl

    def _meld_beliefunits(self, other_idea):
        for hc in other_idea._beliefunits.values():
            if self._beliefunits.get(hc.base) is None:
                self._beliefunits[hc.base] = hc
            else:
                self._beliefunits.get(hc.base).meld(hc)

    def meld(
        self,
        other_idea,
        _idearoot: bool = None,
        party_id: PartyID = None,
        party_weight: float = None,
    ):
        if _idearoot and self._label != other_idea._label:
            raise InvalidIdeaException(
                f"Meld fail idearoot _label '{self._label}' not the same as '{other_idea._label}'"
            )
        if _idearoot:
            self._weight = 1
        else:
            self._weight = get_meld_weight(
                src_weight=self._weight,
                src_meld_strategy=self._meld_strategy,
                other_weight=other_idea._weight,
                other_meld_strategy=other_idea._meld_strategy,
            )
        self._meld_reasonunits(other_idea=other_idea)
        self._meld_balancelinks(other_idea=other_idea)
        self._meld_beliefunits(other_idea=other_idea)
        if other_idea._meld_strategy != "override":
            self._meld_attributes_that_must_be_equal(other_idea=other_idea)
        else:
            self._meld_attributes_overide(other_idea=other_idea)
        self._meld_originlinks(party_id, party_weight)

    def _meld_originlinks(self, party_id: PartyID, party_weight: float):
        if party_id != None:
            self._originunit.set_originlink(party_id=party_id, weight=party_weight)

    def set_originunit_empty_if_null(self):
        if self._originunit is None:
            self._originunit = originunit_shop()

    def get_originunit_dict(self) -> dict[str:str]:
        return self._originunit.get_dict()

    def _meld_attributes_overide(self, other_idea):
        self._uid = other_idea._uid
        self._begin = other_idea._begin
        self._close = other_idea._close
        self._addin = other_idea._addin
        self._denom = other_idea._denom
        self._numor = other_idea._numor
        self._reest = other_idea._reest
        self._range_source_road = other_idea._range_source_road
        self._numeric_road = other_idea._numeric_road
        self.promise = other_idea.promise
        self._is_expanded = other_idea._is_expanded

    def _meld_attributes_that_must_be_equal(self, other_idea):
        to_be_equal_attributes = [
            ("_uid", self._uid, other_idea._uid),
            ("_begin", self._begin, other_idea._begin),
            ("_close", self._close, other_idea._close),
            ("_addin", self._addin, other_idea._addin),
            ("_denom", self._denom, other_idea._denom),
            ("_numor", self._numor, other_idea._numor),
            ("_reest", self._reest, other_idea._reest),
            (
                "_range_source_road",
                self._range_source_road,
                other_idea._range_source_road,
            ),
            ("_numeric_road", self._numeric_road, other_idea._numeric_road),
            ("promise", self.promise, other_idea.promise),
            ("_is_expanded", self._is_expanded, other_idea._is_expanded),
        ]
        while to_be_equal_attributes != []:
            attrs = to_be_equal_attributes.pop()
            if attrs[1] != attrs[2]:
                raise InvalidIdeaException(
                    f"Meld fail idea={self.get_road()} {attrs[0]}:{attrs[1]} with {other_idea.get_road()} {attrs[0]}:{attrs[2]}"
                )

    def _set_idea_attr(self, idea_attr: IdeaAttrFilter):
        if idea_attr.weight != None:
            self._weight = idea_attr.weight
        if idea_attr.uid != None:
            self._uid = idea_attr.uid
        if idea_attr.reason != None:
            self.set_reasonunit(reason=idea_attr.reason)
        if idea_attr.reason_base != None and idea_attr.reason_premise != None:
            self.set_reason_premise(
                base=idea_attr.reason_base,
                premise=idea_attr.reason_premise,
                open=idea_attr.reason_premise_open,
                nigh=idea_attr.reason_premise_nigh,
                divisor=idea_attr.reason_premise_divisor,
            )
        if idea_attr.reason_base != None and idea_attr.reason_suff_idea_active != None:
            self.set_reason_suff_idea_active(
                base=idea_attr.reason_base,
                suff_idea_active=idea_attr.reason_suff_idea_active,
            )
        if idea_attr.assignedunit != None:
            self._assignedunit = idea_attr.assignedunit
        if idea_attr.healerhold != None:
            self._healerhold = idea_attr.healerhold
        if idea_attr.begin != None:
            self._begin = idea_attr.begin
        if idea_attr.close != None:
            self._close = idea_attr.close
        if idea_attr.addin != None:
            self._addin = idea_attr.addin
        if idea_attr.numor != None:
            self._numor = idea_attr.numor
        if idea_attr.denom != None:
            self._denom = idea_attr.denom
        if idea_attr.reest != None:
            self._reest = idea_attr.reest
        if idea_attr.numeric_road != None:
            self._numeric_road = idea_attr.numeric_road
        if idea_attr.range_source_road != None:
            self._range_source_road = idea_attr.range_source_road
        if idea_attr.descendant_promise_count != None:
            self._descendant_promise_count = idea_attr.descendant_promise_count
        if idea_attr.all_party_credit != None:
            self._all_party_credit = idea_attr.all_party_credit
        if idea_attr.all_party_debt != None:
            self._all_party_debt = idea_attr.all_party_debt
        if idea_attr.balancelink != None:
            self.set_balancelink(balancelink=idea_attr.balancelink)
        if idea_attr.balancelink_del != None:
            self.del_balancelink(group_id=idea_attr.balancelink_del)
        if idea_attr.is_expanded != None:
            self._is_expanded = idea_attr.is_expanded
        if idea_attr.promise != None:
            self.promise = idea_attr.promise
        if idea_attr.meld_strategy != None:
            self._meld_strategy = validate_meld_strategy(idea_attr.meld_strategy)
        if idea_attr.beliefunit != None:
            self.set_beliefunit(idea_attr.beliefunit)
        if idea_attr.problem_bool != None:
            self._problem_bool = idea_attr.problem_bool

        self._del_reasonunit_all_cases(
            base=idea_attr.reason_del_premise_base,
            premise=idea_attr.reason_del_premise_need,
        )
        self._set_addin_to_zero_if_any_transformations_exist()

    def _set_addin_to_zero_if_any_transformations_exist(self):
        if (
            self._begin != None
            and self._close != None
            and (self._numor != None or self._denom != None)
            and self._addin is None
        ):
            self._addin = 0

    def _del_reasonunit_all_cases(self, base: RoadUnit, premise: RoadUnit):
        if base != None and premise != None:
            self.del_reasonunit_premise(base=base, premise=premise)
            if len(self._reasonunits[base].premises) == 0:
                self.del_reasonunit_base(base=base)

    def set_reason_suff_idea_active(self, base: RoadUnit, suff_idea_active: str):
        x_reasonunit = self._get_or_create_reasonunit(base=base)
        if suff_idea_active == False:
            x_reasonunit.suff_idea_active = False
        elif suff_idea_active == "Set to Ignore":
            x_reasonunit.suff_idea_active = None
        elif suff_idea_active:
            x_reasonunit.suff_idea_active = True

    def _get_or_create_reasonunit(self, base: RoadUnit) -> ReasonUnit:
        x_reasonunit = None
        try:
            x_reasonunit = self._reasonunits[base]
        except Exception:
            x_reasonunit = reasonunit_shop(base, delimiter=self._road_delimiter)
            self._reasonunits[base] = x_reasonunit
        return x_reasonunit

    def set_reason_premise(
        self,
        base: RoadUnit,
        premise: RoadUnit,
        open: float,
        nigh: float,
        divisor: int,
    ):
        x_reasonunit = self._get_or_create_reasonunit(base=base)
        x_reasonunit.set_premise(premise=premise, open=open, nigh=nigh, divisor=divisor)

    def del_reasonunit_base(self, base: RoadUnit):
        try:
            self._reasonunits.pop(base)
        except KeyError as e:
            raise InvalidIdeaException(f"No ReasonUnit at '{base}'") from e

    def del_reasonunit_premise(self, base: RoadUnit, premise: RoadUnit):
        reason_unit = self._reasonunits[base]
        reason_unit.del_premise(premise=premise)

    def add_kid(self, idea_kid):
        if idea_kid._numor != None:
            # if idea_kid._denom != None:
            # if idea_kid._reest != None:
            if self._begin is None or self._close is None:
                raise InvalidIdeaException(
                    f"Idea {idea_kid.get_road()} cannot have numor,denom,reest if parent does not have begin/close range"
                )

            idea_kid._begin = self._begin * idea_kid._numor / idea_kid._denom
            idea_kid._close = self._close * idea_kid._numor / idea_kid._denom

        self._kids[idea_kid._label] = idea_kid
        self._kids = dict(sorted(self._kids.items()))

    def get_kid(self, idea_kid_label: RoadNode, if_missing_create=False):
        if if_missing_create == False:
            return self._kids.get(idea_kid_label)
        try:
            return self._kids[idea_kid_label]
        except Exception:
            KeyError
            self.add_kid(ideaunit_shop(idea_kid_label))
            return_idea = self._kids.get(idea_kid_label)
        return return_idea

    def del_kid(self, idea_kid_label: RoadNode):
        self._kids.pop(idea_kid_label)

    def clear_kids(self):
        self._kids = {}

    def set_balancelink(self, balancelink: BalanceLink):
        self._balancelinks[balancelink.group_id] = balancelink

    def del_balancelink(self, group_id: GroupID):
        try:
            self._balancelinks.pop(group_id)
        except KeyError as e:
            raise (f"Cannot delete balancelink '{group_id}'.") from e

    def set_reasonunit(self, reason: ReasonUnit):
        reason.delimiter = self._road_delimiter
        self._reasonunits[reason.base] = reason

    def get_reasonunit(self, base: RoadUnit) -> ReasonUnit:
        return self._reasonunits.get(base)

    def set_reasonheirs_status(self):
        self.clear_reasonheirs_status()
        for x_reasonheir in self._reasonheirs.values():
            x_reasonheir.set_status(beliefs=self._beliefheirs)

    def set_active(
        self,
        tree_traverse_count: int,
        agenda_groupunits: dict[GroupID:GroupUnit] = None,
        agenda_owner_id: PartyID = None,
    ):
        prev_to_now_active = deepcopy(self._active)
        self._active = self._create_active(
            agenda_groupunits=agenda_groupunits, agenda_owner_id=agenda_owner_id
        )
        self._set_idea_task()
        self.record_active_hx(
            tree_traverse_count=tree_traverse_count,
            prev_active=prev_to_now_active,
            curr_active=self._active,
        )

    def _set_idea_task(self):
        self._task = False
        if (
            self.promise
            and self._active
            and (self._reasonheirs == {} or self._is_any_reasonheir_task_true())
        ):
            self._task = True

    def _is_any_reasonheir_task_true(self) -> bool:
        return any(x_reasonheir._task for x_reasonheir in self._reasonheirs.values())

    def _create_active(
        self, agenda_groupunits: dict[GroupID:GroupUnit], agenda_owner_id: PartyID
    ) -> bool:
        self.set_reasonheirs_status()
        x_bool = self._are_all_reasonheir_active_true()
        if (
            x_bool
            and agenda_groupunits != {}
            and agenda_owner_id != None
            and self._assignedheir._suffgroups != {}
        ):
            self._assignedheir.set_owner_id_assigned(agenda_groupunits, agenda_owner_id)
            if self._assignedheir._owner_id_assigned == False:
                x_bool = False
        return x_bool

    def _are_all_reasonheir_active_true(self) -> bool:
        return all(
            x_reasonheir._status != False for x_reasonheir in self._reasonheirs.values()
        )

    def clear_reasonheirs_status(self):
        for reason in self._reasonheirs.values():
            reason.clear_status()

    def _coalesce_with_reasonunits(self, reasonheirs: dict[RoadUnit:ReasonHeir]):
        reasonheirs_new = get_empty_dict_if_none(x_dict=deepcopy(reasonheirs))
        reasonheirs_new.update(self._reasonunits)
        return reasonheirs_new

    def set_reasonheirs(
        self,
        agenda_idea_dict: dict[RoadUnit:],
        reasonheirs: dict[RoadUnit:ReasonCore] = None,
    ):
        if reasonheirs is None:
            reasonheirs = self._reasonheirs
        coalesced_reasons = self._coalesce_with_reasonunits(reasonheirs)

        self._reasonheirs = {}
        for old_reasonheir in coalesced_reasons.values():
            new_reasonheir = reasonheir_shop(
                base=old_reasonheir.base,
                suff_idea_active=old_reasonheir.suff_idea_active,
            )
            new_reasonheir.inherit_from_reasonheir(old_reasonheir)

            # if agenda_idea_dict != None:
            base_idea = agenda_idea_dict.get(old_reasonheir.base)
            if base_idea != None:
                new_reasonheir.set_curr_idea_active(bool_x=base_idea._active)

            self._reasonheirs[new_reasonheir.base] = new_reasonheir

    def set_idearoot_inherit_reasonheirs(self):
        self._reasonheirs = {}
        for curr_reasonunit in self._reasonunits.values():
            new_reasonheir = reasonheir_shop(curr_reasonunit.base)
            new_reasonheir.inherit_from_reasonheir(curr_reasonunit)
            self._reasonheirs[new_reasonheir.base] = new_reasonheir

    def get_reasonheir(self, base: RoadUnit) -> ReasonHeir:
        return self._reasonheirs.get(base)

    def get_reasonunits_dict(self):
        return {base: reason.get_dict() for base, reason in self._reasonunits.items()}

    def get_kids_dict(self):
        return {c_road: kid.get_dict() for c_road, kid in self._kids.items()}

    def get_balancelinks_dict(self):
        return {
            x_group_id: balancelink.get_dict()
            for x_group_id, balancelink in self._balancelinks.items()
        }

    def is_kidless(self):
        return self._kids == {}

    def is_arithmetic(self):
        return self._begin != None and self._close != None

    def is_balanceheirless(self):
        x_bool = None
        if self._balanceheirs in [{}, None]:
            x_bool = True
        elif self._balanceheirs != [{}, None]:
            x_bool = False
        return x_bool

    def get_dict(self) -> dict[str:str]:
        x_dict = {"_weight": self._weight}

        if self._label != None:
            x_dict["_label"] = self._label
        if self._uid != None:
            x_dict["_uid"] = self._uid
        if self._kids not in [{}, None]:
            x_dict["_kids"] = self.get_kids_dict()
        if self._reasonunits not in [{}, None]:
            x_dict["_reasonunits"] = self.get_reasonunits_dict()
        if self._assignedunit not in [None, assignedunit_shop()]:
            x_dict["_assignedunit"] = self.get_assignedunit_dict()
        if self._healerhold not in [None, healerhold_shop()]:
            x_dict["_healerhold"] = self._healerhold.get_dict()
        if self._balancelinks not in [{}, None]:
            x_dict["_balancelinks"] = self.get_balancelinks_dict()
        if self._originunit not in [None, originunit_shop()]:
            x_dict["_originunit"] = self.get_originunit_dict()
        if self._begin != None:
            x_dict["_begin"] = self._begin
        if self._close != None:
            x_dict["_close"] = self._close
        if self._addin != None:
            x_dict["_addin"] = self._addin
        if self._numor != None:
            x_dict["_numor"] = self._numor
        if self._denom != None:
            x_dict["_denom"] = self._denom
        if self._reest != None:
            x_dict["_reest"] = self._reest
        if self._range_source_road != None:
            x_dict["_range_source_road"] = self._range_source_road
        if self._numeric_road != None:
            x_dict["_numeric_road"] = self._numeric_road
        if self.promise:
            x_dict["promise"] = self.promise
        if self._problem_bool:
            x_dict["_problem_bool"] = self._problem_bool
        if self._beliefunits not in [{}, None]:
            x_dict["_beliefunits"] = self.get_beliefunits_dict()
        if self._is_expanded == False:
            x_dict["_is_expanded"] = self._is_expanded
        if self._meld_strategy != "default":
            x_dict["_meld_strategy"] = self._meld_strategy

        return x_dict

    def find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        if is_sub_road(ref_road=self._parent_road, sub_road=old_road):
            self._parent_road = change_road(self._parent_road, old_road, new_road)
        if is_sub_road(ref_road=self._range_source_road, sub_road=old_road):
            self._range_source_road = change_road(
                self._range_source_road, old_road, new_road
            )
        if is_sub_road(ref_road=self._numeric_road, sub_road=old_road):
            self._numeric_road = change_road(self._numeric_road, old_road, new_road)

        self._reasonunits == find_replace_road_key_dict(
            dict_x=self._reasonunits, old_road=old_road, new_road=new_road
        )

        self._beliefunits == find_replace_road_key_dict(
            dict_x=self._beliefunits, old_road=old_road, new_road=new_road
        )

    def set_assignedunit_empty_if_null(self):
        if self._assignedunit is None:
            self._assignedunit = assignedunit_shop()

    def set_assignedheir(
        self,
        parent_assignheir: AssignedHeir,
        agenda_groups: dict[GroupID:GroupUnit],
    ):
        self._assignedheir = assigned_heir_shop()
        self._assignedheir.set_suffgroups(
            parent_assignheir=parent_assignheir,
            assignunit=self._assignedunit,
            agenda_groups=agenda_groups,
        )

    def get_assignedunit_dict(self):
        return self._assignedunit.get_dict()

    def assignor_in(self, group_ids: dict[GroupID:-1]):
        return self._assignedheir.group_in(group_ids)


def ideaunit_shop(
    _label: RoadNode = None,
    _uid: int = None,  # Calculated field?
    _parent_road: RoadUnit = None,
    _kids: dict = None,
    _weight: int = 1,
    _balancelinks: dict[GroupID:BalanceLink] = None,
    _balanceheirs: dict[GroupID:BalanceHeir] = None,  # Calculated field
    _balancelines: dict[GroupID:BalanceLink] = None,  # Calculated field
    _reasonunits: dict[RoadUnit:ReasonUnit] = None,
    _reasonheirs: dict[RoadUnit:ReasonHeir] = None,  # Calculated field
    _assignedunit: AssignedUnit = None,
    _assignedheir: AssignedHeir = None,  # Calculated field
    _beliefunits: dict[BeliefUnit] = None,
    _beliefheirs: dict[BeliefHeir] = None,  # Calculated field
    _healerhold: HealerHold = None,
    _begin: float = None,
    _close: float = None,
    _addin: float = None,
    _denom: int = None,
    _numor: int = None,
    _reest: bool = None,
    _range_source_road: RoadUnit = None,
    _numeric_road: RoadUnit = None,
    promise: bool = None,
    _originunit: OriginUnit = None,
    _meld_strategy: str = None,
    _root: bool = None,
    _agenda_world_id: WorldID = None,
    _problem_bool: bool = None,
    # Calculated fields
    _level: int = None,
    _kids_total_weight: int = None,
    _agenda_importance: float = None,
    _agenda_fund_onset: float = None,
    _agenda_fund_cease: float = None,
    _task: bool = None,
    _active: bool = None,
    _ancestor_promise_count: int = None,
    _descendant_promise_count: int = None,
    _all_party_credit: bool = None,
    _all_party_debt: bool = None,
    _is_expanded: bool = True,
    _sibling_total_weight: int = None,
    _active_hx: dict[int:bool] = None,
    _road_delimiter: str = None,
    _healerhold_importance: float = None,
) -> IdeaUnit:
    if _meld_strategy is None:
        _meld_strategy = get_meld_default()
    if _agenda_world_id is None:
        _agenda_world_id = root_label()
    if _healerhold is None:
        _healerhold = healerhold_shop()

    x_ideakid = IdeaUnit(
        _label=None,
        _uid=_uid,
        _parent_road=_parent_road,
        _kids=get_empty_dict_if_none(_kids),
        _weight=_weight,
        _balancelinks=get_empty_dict_if_none(_balancelinks),
        _balanceheirs=get_empty_dict_if_none(_balanceheirs),
        _balancelines=get_empty_dict_if_none(_balancelines),
        _reasonunits=get_empty_dict_if_none(_reasonunits),
        _reasonheirs=get_empty_dict_if_none(_reasonheirs),
        _assignedunit=_assignedunit,
        _assignedheir=_assignedheir,
        _beliefunits=get_empty_dict_if_none(_beliefunits),
        _beliefheirs=get_empty_dict_if_none(_beliefheirs),
        _healerhold=_healerhold,
        _begin=_begin,
        _close=_close,
        _addin=_addin,
        _denom=_denom,
        _numor=_numor,
        _reest=_reest,
        _range_source_road=_range_source_road,
        _numeric_road=_numeric_road,
        promise=get_False_if_None(promise),
        _problem_bool=get_False_if_None(_problem_bool),
        _originunit=_originunit,
        _meld_strategy=_meld_strategy,
        _root=get_False_if_None(_root),
        _agenda_world_id=_agenda_world_id,
        # Calculated fields
        _level=_level,
        _kids_total_weight=get_0_if_None(_kids_total_weight),
        _agenda_importance=_agenda_importance,
        _agenda_fund_onset=_agenda_fund_onset,
        _agenda_fund_cease=_agenda_fund_cease,
        _task=_task,
        _active=_active,
        _ancestor_promise_count=_ancestor_promise_count,
        _descendant_promise_count=_descendant_promise_count,
        _all_party_credit=_all_party_credit,
        _all_party_debt=_all_party_debt,
        _is_expanded=_is_expanded,
        _sibling_total_weight=_sibling_total_weight,
        _active_hx=get_empty_dict_if_none(_active_hx),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
        _healerhold_importance=get_0_if_None(_healerhold_importance),
    )
    if x_ideakid._root:
        x_ideakid.set_idea_label(_label=_agenda_world_id)
    else:
        x_ideakid.set_idea_label(_label=_label)
    x_ideakid.set_assignedunit_empty_if_null()
    x_ideakid.set_originunit_empty_if_null()
    return x_ideakid


class Idea_root_LabelNotEmptyException(Exception):
    pass


def get_obj_from_idea_dict(x_dict: dict[str:], dict_key: str) -> any:
    if dict_key == "_reasonunits":
        return (
            reasons_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else None
        )
    elif dict_key == "_assignedunit":
        return (
            assignedunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else assignedunit_shop()
        )
    elif dict_key == "_healerhold":
        return (
            healerhold_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else healerhold_shop()
        )
    elif dict_key == "_originunit":
        return (
            originunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else originunit_shop()
        )
    elif dict_key == "_beliefunits":
        return (
            beliefunits_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else beliefunits_get_from_dict({})
        )
    elif dict_key == "_balancelinks":
        return (
            balancelinks_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else balancelinks_get_from_dict({})
        )
    elif dict_key in {"_kids"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else {}
    elif dict_key in {"promise", "_problem_bool"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else False
    elif dict_key in {"_is_expanded"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else True
    # elif dict_key == "_meld_strategy":
    #     return x_dict[dict_key] if x_dict.get(dict_key) != None else "default"
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None
