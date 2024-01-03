from dataclasses import dataclass
from src.agenda.required_assign import (
    AssignedUnit,
    AssignedHeir,
    assigned_unit_shop,
    assigned_heir_shop,
    assignedunit_get_from_dict,
)
from src.agenda.required_idea import (
    AcptFactCore,
    AcptFactHeir,
    acptfactheir_shop,
    RequiredCore,
    RequiredUnit,
    requiredunit_shop,
    RoadUnit,
    AcptFactUnit,
    AcptFactUnit,
    acptfactunit_shop,
    RequiredHeir,
    requiredheir_shop,
    sufffactunit_shop,
    RoadUnit,
    change_road,
    find_replace_road_key_dict,
    requireds_get_from_dict,
    acptfactunits_get_from_dict,
)
from src.agenda.road import (
    RoadUnit,
    RoadNode,
    is_sub_road,
    get_default_economy_root_roadnode as root_label,
    create_road as road_create_road,
    default_road_delimiter_if_none,
    replace_road_delimiter,
    EconomyID,
)
from src.agenda.group import (
    BalanceHeir,
    BalanceLink,
    balancelinks_get_from_dict,
    GroupBrand,
    BalanceLine,
    balanceline_shop,
    balanceheir_shop,
    GroupUnit,
)
from src.agenda.origin import OriginUnit, originunit_get_from_dict
from src.agenda.party import PartyPID
from src.agenda.origin import originunit_shop
from src.agenda.x_func import (
    get_on_meld_weight_actions,
    get_meld_weight,
    return1ifnone as x_func_return1ifnone,
)
from src.agenda.y_func import get_empty_dict_if_none
from copy import deepcopy


class InvalidIdeaException(Exception):
    pass


class IdeaGetDescendantsException(Exception):
    pass


@dataclass
class IdeaAttrFilter:
    weight: int = None
    uid: int = None
    required: RequiredUnit = None
    required_base: RoadUnit = None
    required_sufffact: RoadUnit = None
    required_sufffact_open: float = None
    required_sufffact_nigh: float = None
    required_sufffact_divisor: int = None
    required_del_sufffact_base: RoadUnit = None
    required_del_sufffact_need: RoadUnit = None
    required_suff_idea_active_status: str = None
    assignedunit: AssignedUnit = None
    begin: float = None
    close: float = None
    addin: float = None
    numor: float = None
    denom: float = None
    reest: bool = None
    numeric_road: RoadUnit = None
    range_source_road: float = None
    promise: bool = None
    problem_bool: bool = None
    acptfactunit: AcptFactUnit = None
    descendant_promise_count: int = None
    all_party_credit: bool = None
    all_party_debt: bool = None
    balancelink: BalanceLink = None
    balancelink_del: GroupBrand = None
    is_expanded: bool = None
    on_meld_weight_action: str = None

    def get_sufffact_need(self):
        return self.required_sufffact

    def set_sufffact_range_attributes_influenced_by_sufffact_idea(
        self,
        sufffact_open,
        sufffact_nigh,
        # sufffact_numor,
        sufffact_denom,
        # sufffact_reest,
    ):
        if self.required_sufffact != None:
            if self.required_sufffact_open is None:
                self.required_sufffact_open = sufffact_open
            if self.required_sufffact_nigh is None:
                self.required_sufffact_nigh = sufffact_nigh
            # if self.required_sufffact_numor is None:
            #     numor_x = sufffact_numor
            if self.required_sufffact_divisor is None:
                self.required_sufffact_divisor = sufffact_denom
            # if self.required_sufffact_reest is None:
            #     self.required_sufffact_reest = sufffact_reest

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

    def has_required_sufffact(self):
        return self.required_sufffact != None


def ideaattrfilter_shop(
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
) -> IdeaAttrFilter:
    x_ideaattrfilter = IdeaAttrFilter(
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
        promise=promise,
        problem_bool=problem_bool,
        acptfactunit=acptfactunit,
        descendant_promise_count=descendant_promise_count,
        all_party_credit=all_party_credit,
        all_party_debt=all_party_debt,
        balancelink=balancelink,
        balancelink_del=balancelink_del,
        is_expanded=is_expanded,
        on_meld_weight_action=on_meld_weight_action,
    )
    if x_ideaattrfilter.has_ratio_attrs():
        x_ideaattrfilter.set_ratio_attr_defaults_if_none()
    return x_ideaattrfilter


@dataclass
class IdeaUnit:
    _label: RoadNode = None
    _uid: int = None  # Calculated field?
    _parent_road: RoadUnit = None
    _kids: dict = None
    _weight: int = None
    _balancelinks: dict[GroupBrand:BalanceLink] = None
    _balanceheirs: dict[GroupBrand:BalanceHeir] = None  # Calculated field
    _balancelines: dict[GroupBrand:BalanceLine] = None  # Calculated field
    _requiredunits: dict[RoadUnit:RequiredUnit] = None
    _requiredheirs: dict[RoadUnit:RequiredHeir] = None  # Calculated field
    _assignedunit: AssignedUnit = None
    _assignedheir: AssignedHeir = None  # Calculated field
    _acptfactunits: dict[AcptFactUnit] = None
    _acptfactheirs: dict[AcptFactHeir] = None  # Calculated field
    _begin: float = None
    _close: float = None
    _addin: float = None
    _denom: int = None
    _numor: int = None
    _reest: bool = None
    _range_source_road: RoadUnit = None
    _numeric_road: RoadUnit = None
    promise: bool = None
    _problem_bool: bool = None
    _originunit: OriginUnit = None
    _on_meld_weight_action: str = None
    _root: bool = None
    _agenda_economy_id: EconomyID = None
    # Calculated fields
    _level: int = None
    _kids_total_weight: int = None
    _agenda_importance: float = None
    _agenda_coin_onset: float = None
    _agenda_coin_cease: float = None
    _task: bool = None
    _active_status: bool = None
    _ancestor_promise_count: int = None
    _descendant_promise_count: int = None
    _all_party_credit: bool = None
    _all_party_debt: bool = None
    _is_expanded: bool = None
    _sibling_total_weight: int = None
    _active_status_hx: dict[int:bool] = None
    _road_delimiter: str = None

    def is_intent_item(self, necessary_base: RoadUnit = None) -> bool:
        # bool_x = False
        return (
            self.promise
            and self._active_status
            and self.base_requiredunit_exists(necessary_base)
        )

    def base_requiredunit_exists(self, necessary_base: RoadUnit = None) -> bool:
        return necessary_base is None or any(
            required.base == necessary_base for required in self._requiredunits.values()
        )

    def record_active_status_hx(
        self,
        tree_traverse_count: int,
        prev_active_status: bool,
        curr_active_status: bool,
    ):
        if tree_traverse_count == 0:
            self._active_status_hx = {0: curr_active_status}
        elif prev_active_status != curr_active_status:
            self._active_status_hx[tree_traverse_count] = curr_active_status

    def set_acptfactheirs(self, acptfacts: dict[RoadUnit:AcptFactCore]):
        acptfacts = get_empty_dict_if_none(x_dict=acptfacts)
        self._acptfactheirs = {}
        for h in acptfacts.values():
            x_acptfact = acptfactheir_shop(
                base=h.base, pick=h.pick, open=h.open, nigh=h.nigh
            )
            self.delete_acptfactunit_if_past(acptfactheir=x_acptfact)
            x_acptfact = self.apply_acptfactunit_transformations(
                acptfactheir=x_acptfact
            )
            self._acptfactheirs[x_acptfact.base] = x_acptfact

    def apply_acptfactunit_transformations(
        self, acptfactheir: AcptFactHeir
    ) -> AcptFactHeir:
        for acptfactunit in self._acptfactunits.values():
            if acptfactunit.base == acptfactheir.base:
                acptfactheir.transform(acptfactunit=acptfactunit)
        return acptfactheir

    def delete_acptfactunit_if_past(self, acptfactheir: AcptFactHeir):
        delete_acptfactunit = False
        for acptfactunit in self._acptfactunits.values():
            if (
                acptfactunit.base == acptfactheir.base
                and acptfactunit.nigh != None
                and acptfactheir.open != None
            ) and acptfactunit.nigh < acptfactheir.open:
                delete_acptfactunit = True

        if delete_acptfactunit:
            del self._acptfactunits[acptfactunit.base]

    def set_acptfactunit(self, acptfactunit: AcptFactUnit):
        self._acptfactunits[acptfactunit.base] = acptfactunit

    def get_acptfactunits_dict(self) -> dict[RoadUnit:AcptFactUnit]:
        return {hc.base: hc.get_dict() for hc in self._acptfactunits.values()}

    def set_acptfactunit_to_complete(self, base_acptfactunit: AcptFactUnit):
        # if a idea is considered a task then a acptfactheir.open attribute can be increased to
        # a number <= acptfactheir.nigh so the idea no longer is a task. This method finds
        # the minimal acptfactheir.open to change idea._task == False. idea_core._acptfactheir cannot be straight up manpulated
        # so idea._acptfactunit reqquires being changed.
        # self.set_acptfactunits(base=acptfact, acptfact=base, open=sufffact_nigh, nigh=acptfact_nigh)
        self._acptfactunits[base_acptfactunit.base] = acptfactunit_shop(
            base=base_acptfactunit.base,
            pick=base_acptfactunit.base,
            open=base_acptfactunit.nigh,
            nigh=base_acptfactunit.nigh,
        )

    def del_acptfactunit(self, base: RoadUnit):
        self._acptfactunits.pop(base)

    def _apply_any_range_source_road_connections(
        self,
        lemmas_dict: dict[RoadUnit:AcptFactUnit],
        missing_acptfacts: list[AcptFactUnit],
    ):
        for current_acptfact in self._acptfactunits.values():
            for lemma_acptfact in lemmas_dict.values():
                if lemma_acptfact.base == current_acptfact.base:
                    self.set_acptfactunit(lemma_acptfact)

        for missing_acptfact in missing_acptfacts:
            for lemma_acptfact in lemmas_dict.values():
                if lemma_acptfact.base == missing_acptfact:
                    self.set_acptfactunit(lemma_acptfact)

    def set_agenda_importance(
        self,
        coin_onset_x: float,
        parent_agenda_importance: float = None,
        parent_coin_cease: float = None,
    ):
        parent_agenda_importance = x_func_return1ifnone(parent_agenda_importance)
        self.set_kids_total_weight()
        self._agenda_importance = None
        self._agenda_coin_onset = None
        self._agenda_coin_cease = None
        sibling_ratio = self._weight / self._sibling_total_weight
        self._agenda_importance = parent_agenda_importance * sibling_ratio
        self._agenda_coin_onset = coin_onset_x
        self._agenda_coin_cease = self._agenda_coin_onset + self._agenda_importance
        self._agenda_coin_cease = min(self._agenda_coin_cease, parent_coin_cease)
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
        self, parent_balanceheirs: dict[GroupBrand:BalanceHeir] = None
    ):
        if parent_balanceheirs is None:
            parent_balanceheirs = {}

        self._balanceheirs = {}
        for ib in parent_balanceheirs.values():
            balanceheir = balanceheir_shop(
                brand=ib.brand,
                creditor_weight=ib.creditor_weight,
                debtor_weight=ib.debtor_weight,
            )
            self._balanceheirs[balanceheir.brand] = balanceheir

        for ib in self._balancelinks.values():
            balanceheir = balanceheir_shop(
                brand=ib.brand,
                creditor_weight=ib.creditor_weight,
                debtor_weight=ib.debtor_weight,
            )
            self._balanceheirs[balanceheir.brand] = balanceheir

    def set_kidless_balancelines(self):
        # get balancelines from self
        for bh in self._balanceheirs.values():
            x_balanceline = balanceline_shop(
                brand=bh.brand,
                _agenda_credit=bh._agenda_credit,
                _agenda_debt=bh._agenda_debt,
            )
            self._balancelines[x_balanceline.brand] = x_balanceline

    def set_balancelines(self, child_balancelines: dict[GroupBrand:BalanceLine] = None):
        if child_balancelines is None:
            child_balancelines = {}

        # get balancelines from child
        for bl in child_balancelines.values():
            if self._balancelines.get(bl.brand) is None:
                self._balancelines[bl.brand] = balanceline_shop(
                    brand=bl.brand,
                    _agenda_credit=0,
                    _agenda_debt=0,
                )

            self._balancelines[bl.brand].add_agenda_credit_debt(
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
            and _label != self._agenda_economy_id
            and self._agenda_economy_id != None
        ):
            raise Idea_root_LabelNotEmptyException(
                f"Cannot set idearoot to string other than '{self._agenda_economy_id}'"
            )
        elif self._root and self._agenda_economy_id is None:
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

        new_requiredunits = {}
        for requiredunit_road, requiredunit_obj in self._requiredunits.items():
            new_requiredunit_road = replace_road_delimiter(
                road=requiredunit_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )
            requiredunit_obj.set_delimiter(self._road_delimiter)
            new_requiredunits[new_requiredunit_road] = requiredunit_obj
        self._requiredunits = new_requiredunits

        new_acptfactunits = {}
        for acptfactunit_road, acptfactunit_obj in self._acptfactunits.items():
            new_base_road = replace_road_delimiter(
                road=acptfactunit_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )
            acptfactunit_obj.base = new_base_road
            new_pick_road = replace_road_delimiter(
                road=acptfactunit_obj.pick,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_delimiter,
            )
            acptfactunit_obj.set_attr(pick=new_pick_road)
            new_acptfactunits[new_base_road] = acptfactunit_obj
        self._acptfactunits = new_acptfactunits

    def _meld_requiredunits(self, other_idea):
        for lx in other_idea._requiredunits.values():
            if self._requiredunits.get(lx.base) is None:
                self._requiredunits[lx.base] = lx
            else:
                self._requiredunits.get(lx.base).meld(lx)

    def _meld_balancelinks(self, other_idea):
        for bl in other_idea._balancelinks.values():
            if self._balancelinks.get(bl.brand) != None:
                self._balancelinks.get(bl.brand).meld(
                    other_balancelink=bl,
                    other_on_meld_weight_action=other_idea._on_meld_weight_action,
                    src_on_meld_weight_action=self._on_meld_weight_action,
                )
            else:
                self._balancelinks[bl.brand] = bl

    def _meld_acptfactunits(self, other_idea):
        for hc in other_idea._acptfactunits.values():
            if self._acptfactunits.get(hc.base) is None:
                self._acptfactunits[hc.base] = hc
            else:
                self._acptfactunits.get(hc.base).meld(hc)

    def meld(
        self,
        other_idea,
        _idearoot: bool = None,
        party_pid: PartyPID = None,
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
                src_on_meld_weight_action=self._on_meld_weight_action,
                other_weight=other_idea._weight,
                other_on_meld_weight_action=other_idea._on_meld_weight_action,
            )
        self._meld_requiredunits(other_idea=other_idea)
        self._meld_balancelinks(other_idea=other_idea)
        self._meld_acptfactunits(other_idea=other_idea)
        self._meld_attributes_that_will_be_equal(other_idea=other_idea)
        self._meld_originlinks(party_pid, party_weight)

    def _meld_originlinks(self, party_pid: PartyPID, party_weight: float):
        if party_pid != None:
            self._originunit.set_originlink(pid=party_pid, weight=party_weight)

    def set_originunit_empty_if_null(self):
        if self._originunit is None:
            self._originunit = originunit_shop()

    def get_originunit_dict(self) -> dict[str:str]:
        return self._originunit.get_dict()

    def _meld_attributes_that_will_be_equal(self, other_idea):
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
        if idea_attr.required != None:
            self.set_required_unit(required=idea_attr.required)
        if idea_attr.required_base != None and idea_attr.required_sufffact != None:
            self.set_required_sufffact(
                base=idea_attr.required_base,
                sufffact=idea_attr.required_sufffact,
                open=idea_attr.required_sufffact_open,
                nigh=idea_attr.required_sufffact_nigh,
                divisor=idea_attr.required_sufffact_divisor,
            )
        if (
            idea_attr.required_base != None
            and idea_attr.required_suff_idea_active_status != None
        ):
            self.set_required_suff_idea_active_status(
                base=idea_attr.required_base,
                suff_idea_active_status=idea_attr.required_suff_idea_active_status,
            )
        if idea_attr.assignedunit != None:
            self._assignedunit = idea_attr.assignedunit
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
            self.del_balancelink(groupbrand=idea_attr.balancelink_del)
        if idea_attr.is_expanded != None:
            self._is_expanded = idea_attr.is_expanded
        if idea_attr.promise != None:
            self.promise = idea_attr.promise
        if idea_attr.problem_bool != None:
            self._problem_bool = idea_attr.problem_bool
        if idea_attr.on_meld_weight_action != None:
            self._check_get_on_meld_weight_actions(idea_attr.on_meld_weight_action)
            self._on_meld_weight_action = idea_attr.on_meld_weight_action
        if idea_attr.acptfactunit != None:
            self.set_acptfactunit(idea_attr.acptfactunit)

        self._del_requiredunit_all_cases(
            base=idea_attr.required_del_sufffact_base,
            sufffact=idea_attr.required_del_sufffact_need,
        )
        self._set_addin_to_zero_if_any_transformations_exist()

    def _check_get_on_meld_weight_actions(self, on_meld_weight_action: str):
        if on_meld_weight_action not in (list(get_on_meld_weight_actions())):
            raise InvalidIdeaException(
                f"IdeaUnit unit '{self._label}' cannot have on_meld_weight_action '{on_meld_weight_action}'."
            )

    def _set_addin_to_zero_if_any_transformations_exist(self):
        if (
            self._begin != None
            and self._close != None
            and (self._numor != None or self._denom != None)
            and self._addin is None
        ):
            self._addin = 0

    def _del_requiredunit_all_cases(self, base: RoadUnit, sufffact: RoadUnit):
        if base != None and sufffact != None:
            self.del_requiredunit_sufffact(base=base, sufffact=sufffact)
            if len(self._requiredunits[base].sufffacts) == 0:
                self.del_requiredunit_base(base=base)

    def set_required_suff_idea_active_status(
        self, base: RoadUnit, suff_idea_active_status: str
    ):
        x_requiredunit = self._get_or_create_requiredunit(base=base)
        if suff_idea_active_status == False:
            x_requiredunit.suff_idea_active_status = False
        elif suff_idea_active_status == "Set to Ignore":
            x_requiredunit.suff_idea_active_status = None
        elif suff_idea_active_status:
            x_requiredunit.suff_idea_active_status = True

    def _get_or_create_requiredunit(self, base: RoadUnit) -> RequiredUnit:
        x_requiredunit = None
        try:
            x_requiredunit = self._requiredunits[base]
        except Exception:
            x_requiredunit = requiredunit_shop(base, delimiter=self._road_delimiter)
            self._requiredunits[base] = x_requiredunit
        return x_requiredunit

    def set_required_sufffact(
        self,
        base: RoadUnit,
        sufffact: RoadUnit,
        open: float,
        nigh: float,
        divisor: int,
    ):
        x_requiredunit = self._get_or_create_requiredunit(base=base)
        x_requiredunit.set_sufffact(
            sufffact=sufffact, open=open, nigh=nigh, divisor=divisor
        )

    def del_requiredunit_base(self, base: RoadUnit):
        try:
            self._requiredunits.pop(base)
        except KeyError as e:
            raise InvalidIdeaException(f"No RequiredUnit at '{base}'") from e

    def del_requiredunit_sufffact(self, base: RoadUnit, sufffact: RoadUnit):
        required_unit = self._requiredunits[base]
        required_unit.del_sufffact(sufffact=sufffact)

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
        self._balancelinks[balancelink.brand] = balancelink

    def del_balancelink(self, groupbrand: GroupBrand):
        try:
            self._balancelinks.pop(groupbrand)
        except KeyError as e:
            raise (f"Cannot delete balancelink '{groupbrand}'.") from e

    def set_required_unit(self, required: RequiredUnit):
        required.delimiter = self._road_delimiter
        self._requiredunits[required.base] = required

    def set_requiredheirs_status(self):
        self.clear_requiredheirs_status()
        for x_requiredheir in self._requiredheirs.values():
            x_requiredheir.set_status(acptfacts=self._acptfactheirs)

    def set_active_status(
        self,
        tree_traverse_count: int,
        agenda_groupunits: dict[GroupBrand:GroupUnit] = None,
        agenda_healer: PartyPID = None,
    ):
        prev_to_now_active_status = deepcopy(self._active_status)
        self._active_status = self._create_active_status(
            agenda_groupunits=agenda_groupunits, agenda_healer=agenda_healer
        )
        self._set_idea_task()
        self.record_active_status_hx(
            tree_traverse_count=tree_traverse_count,
            prev_active_status=prev_to_now_active_status,
            curr_active_status=self._active_status,
        )

    def _set_idea_task(self):
        self._task = False
        if (
            self.promise
            and self._active_status
            and (self._requiredheirs == {} or self._is_any_requiredheir_task_true())
        ):
            self._task = True

    def _is_any_requiredheir_task_true(self) -> bool:
        return any(
            x_requiredheir._task for x_requiredheir in self._requiredheirs.values()
        )

    def _create_active_status(
        self, agenda_groupunits: dict[GroupBrand:GroupUnit], agenda_healer: PartyPID
    ) -> bool:
        self.set_requiredheirs_status()
        x_bool = self._are_all_requiredheir_active_status_true()
        if (
            x_bool
            and agenda_groupunits != {}
            and agenda_healer != None
            and self._assignedheir._suffgroups != {}
        ):
            self._assignedheir.set_healer_assigned(agenda_groupunits, agenda_healer)
            if self._assignedheir._healer_assigned == False:
                x_bool = False
        return x_bool

    def _are_all_requiredheir_active_status_true(self) -> bool:
        return all(
            x_requiredheir._status != False
            for x_requiredheir in self._requiredheirs.values()
        )

    def clear_requiredheirs_status(self):
        for required in self._requiredheirs.values():
            required.clear_status()

    def _coalesce_with_requiredunits(self, requiredheirs: dict[RoadUnit:RequiredHeir]):
        requiredheirs_new = get_empty_dict_if_none(x_dict=deepcopy(requiredheirs))
        requiredheirs_new.update(self._requiredunits)
        return requiredheirs_new

    def set_requiredheirs(
        self,
        agenda_idea_dict: dict[RoadUnit:],
        requiredheirs: dict[RoadUnit:RequiredCore] = None,
    ):
        if requiredheirs is None:
            requiredheirs = self._requiredheirs
        coalesced_requireds = self._coalesce_with_requiredunits(requiredheirs)

        self._requiredheirs = {}
        for old_requiredheir in coalesced_requireds.values():
            new_requiredheir = requiredheir_shop(
                base=old_requiredheir.base,
                suff_idea_active_status=old_requiredheir.suff_idea_active_status,
            )
            new_requiredheir.inherit_from_requiredheir(old_requiredheir)

            # if agenda_idea_dict != None:
            base_idea = agenda_idea_dict.get(old_requiredheir.base)
            if base_idea != None:
                new_requiredheir.set_curr_idea_active_status(
                    bool_x=base_idea._active_status
                )

            self._requiredheirs[new_requiredheir.base] = new_requiredheir

    def set_idearoot_inherit_requiredheirs(self):
        self._requiredheirs = {}
        for curr_requiredunit in self._requiredunits.values():
            new_requiredheir = requiredheir_shop(curr_requiredunit.base)
            new_requiredheir.inherit_from_requiredheir(curr_requiredunit)
            self._requiredheirs[new_requiredheir.base] = new_requiredheir

    def get_requiredheir(self, base: RoadUnit) -> RequiredHeir:
        return self._requiredheirs.get(base)

    def get_requiredunits_dict(self):
        return {
            base: required.get_dict() for base, required in self._requiredunits.items()
        }

    def get_kids_dict(self):
        return {c_road: kid.get_dict() for c_road, kid in self._kids.items()}

    def get_balancelinks_dict(self):
        return {
            group_pid: balancelink.get_dict()
            for group_pid, balancelink in self._balancelinks.items()
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

    def get_dict(self):
        x_dict = {"_weight": self._weight}

        if self._label != None:
            x_dict["_label"] = self._label
        if self._uid != None:
            x_dict["_uid"] = self._uid
        if self._kids not in [{}, None]:
            x_dict["_kids"] = self.get_kids_dict()
        if self._requiredunits not in [{}, None]:
            x_dict["_requiredunits"] = self.get_requiredunits_dict()
        if self._assignedunit not in [None, assigned_unit_shop()]:
            x_dict["_assignedunit"] = self.get_assignedunit_dict()
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
        if self._acptfactunits not in [{}, None]:
            x_dict["_acptfactunits"] = self.get_acptfactunits_dict()
        if self._is_expanded == False:
            x_dict["_is_expanded"] = self._is_expanded
        if self._on_meld_weight_action != "default":
            x_dict["_on_meld_weight_action"] = self._on_meld_weight_action

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

        self._requiredunits == find_replace_road_key_dict(
            dict_x=self._requiredunits, old_road=old_road, new_road=new_road
        )

        self._acptfactunits == find_replace_road_key_dict(
            dict_x=self._acptfactunits, old_road=old_road, new_road=new_road
        )

    def set_assignedunit_empty_if_null(self):
        if self._assignedunit is None:
            self._assignedunit = assigned_unit_shop()

    def set_assignedheir(
        self,
        parent_assignheir: AssignedHeir,
        agenda_groups: dict[GroupBrand:GroupUnit],
    ):
        self._assignedheir = assigned_heir_shop()
        self._assignedheir.set_suffgroups(
            parent_assignheir=parent_assignheir,
            assignunit=self._assignedunit,
            agenda_groups=agenda_groups,
        )

    def get_assignedunit_dict(self):
        return self._assignedunit.get_dict()

    def assignor_in(self, groupbrands: dict[GroupBrand:-1]):
        return self._assignedheir.group_in(groupbrands)


def ideaunit_shop(
    _label: RoadNode = None,
    _uid: int = None,  # Calculated field?
    _parent_road: RoadUnit = None,
    _kids: dict = None,
    _weight: int = 1,
    _balancelinks: dict[GroupBrand:BalanceLink] = None,
    _balanceheirs: dict[GroupBrand:BalanceHeir] = None,  # Calculated field
    _balancelines: dict[GroupBrand:BalanceLink] = None,  # Calculated field
    _requiredunits: dict[RoadUnit:RequiredUnit] = None,
    _requiredheirs: dict[RoadUnit:RequiredHeir] = None,  # Calculated field
    _assignedunit: AssignedUnit = None,
    _assignedheir: AssignedHeir = None,  # Calculated field
    _acptfactunits: dict[AcptFactUnit] = None,
    _acptfactheirs: dict[AcptFactHeir] = None,  # Calculated field
    _begin: float = None,
    _close: float = None,
    _addin: float = None,
    _denom: int = None,
    _numor: int = None,
    _reest: bool = None,
    _range_source_road: RoadUnit = None,
    _numeric_road: RoadUnit = None,
    promise: bool = None,
    _problem_bool: bool = None,
    _originunit: OriginUnit = None,
    _on_meld_weight_action: str = None,
    _root: bool = None,
    _agenda_economy_id: EconomyID = None,
    # Calculated fields
    _level: int = None,
    _kids_total_weight: int = None,
    _agenda_importance: float = None,
    _agenda_coin_onset: float = None,
    _agenda_coin_cease: float = None,
    _task: bool = None,
    _active_status: bool = None,
    _ancestor_promise_count: int = None,
    _descendant_promise_count: int = None,
    _all_party_credit: bool = None,
    _all_party_debt: bool = None,
    _is_expanded: bool = True,
    _sibling_total_weight: int = None,
    _active_status_hx: dict[int:bool] = None,
    _road_delimiter: str = None,
) -> IdeaUnit:
    if promise is None:
        promise = False
    if _problem_bool is None:
        _problem_bool = False
    if _on_meld_weight_action is None:
        _on_meld_weight_action = "default"
    if _kids_total_weight is None:
        _kids_total_weight = 0
    if _root is None:
        _root = False
    if _agenda_economy_id is None:
        _agenda_economy_id = root_label()

    x_ideakid = IdeaUnit(
        _label=None,
        _uid=_uid,
        _parent_road=_parent_road,
        _kids=get_empty_dict_if_none(_kids),
        _weight=_weight,
        _balancelinks=get_empty_dict_if_none(_balancelinks),
        _balanceheirs=get_empty_dict_if_none(_balanceheirs),
        _balancelines=get_empty_dict_if_none(_balancelines),
        _requiredunits=get_empty_dict_if_none(_requiredunits),
        _requiredheirs=get_empty_dict_if_none(_requiredheirs),
        _assignedunit=_assignedunit,
        _assignedheir=_assignedheir,
        _acptfactunits=get_empty_dict_if_none(_acptfactunits),
        _acptfactheirs=get_empty_dict_if_none(_acptfactheirs),
        _begin=_begin,
        _close=_close,
        _addin=_addin,
        _denom=_denom,
        _numor=_numor,
        _reest=_reest,
        _range_source_road=_range_source_road,
        _numeric_road=_numeric_road,
        promise=promise,
        _problem_bool=_problem_bool,
        _originunit=_originunit,
        _on_meld_weight_action=_on_meld_weight_action,
        _root=_root,
        _agenda_economy_id=_agenda_economy_id,
        # Calculated fields
        _level=_level,
        _kids_total_weight=_kids_total_weight,
        _agenda_importance=_agenda_importance,
        _agenda_coin_onset=_agenda_coin_onset,
        _agenda_coin_cease=_agenda_coin_cease,
        _task=_task,
        _active_status=_active_status,
        _ancestor_promise_count=_ancestor_promise_count,
        _descendant_promise_count=_descendant_promise_count,
        _all_party_credit=_all_party_credit,
        _all_party_debt=_all_party_debt,
        _is_expanded=_is_expanded,
        _sibling_total_weight=_sibling_total_weight,
        _active_status_hx=get_empty_dict_if_none(_active_status_hx),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    if x_ideakid._root:
        x_ideakid.set_idea_label(_label=_agenda_economy_id)
    else:
        x_ideakid.set_idea_label(_label=_label)
    x_ideakid.set_assignedunit_empty_if_null()
    x_ideakid.set_originunit_empty_if_null()
    return x_ideakid


class Idea_root_LabelNotEmptyException(Exception):
    pass


def get_obj_from_idea_dict(x_dict: dict[str:], dict_key: str) -> any:
    if dict_key == "_requiredunits":
        return (
            requireds_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else None
        )
    elif dict_key == "_assignedunit":
        return (
            assignedunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else assigned_unit_shop()
        )
    elif dict_key == "_originunit":
        return (
            originunit_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else originunit_shop()
        )
    elif dict_key == "_acptfactunits":
        return (
            acptfactunits_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else acptfactunits_get_from_dict({})
        )
    elif dict_key == "_balancelinks":
        return (
            balancelinks_get_from_dict(x_dict[dict_key])
            if x_dict.get(dict_key) != None
            else balancelinks_get_from_dict({})
        )
    elif dict_key in {"_kids"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else {}
    elif dict_key in {"promise"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else False
    elif dict_key in {"_is_expanded"}:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else True
    # elif dict_key == "_on_meld_weight_action":
    #     return x_dict[dict_key] if x_dict.get(dict_key) != None else "default"
    else:
        return x_dict[dict_key] if x_dict.get(dict_key) != None else None
