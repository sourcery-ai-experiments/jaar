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
    Road,
    AcptFactUnit,
    AcptFactUnit,
    acptfactunit_shop,
    RequiredHeir,
    requiredheir_shop,
    sufffactunit_shop,
    Road,
    change_road,
    find_replace_road_key_dict,
    requireds_get_from_dict,
    acptfactunits_get_from_dict,
)
from src.agenda.road import (
    Road,
    RaodNode,
    is_sub_road,
    get_default_culture_root_label as root_label,
    get_road as road_get_road,
    get_node_delimiter,
    replace_road_node_delimiter,
)
from src.agenda.group import (
    BalanceHeir,
    BalanceLink,
    balancelinks_get_from_dict,
    GroupBrand,
    BalanceLine,
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
from copy import deepcopy


class InvalidIdeaException(Exception):
    pass


class IdeaGetDescendantsException(Exception):
    pass


@dataclass
class IdeaBare:
    n: str = None  # pid
    weight: int = 1
    b: float = None  # begin
    c: float = None  # close  # where
    a: float = None  # addin
    rr: str = None  # relative_road # not road since it doesn't know root _label
    mn: int = None  # numor
    md: int = None  # denom
    mr: bool = None  # reest
    sr: str = None  # range_source_road # not road since it doesn't know root _label
    nr: str = None  # numeric_road # not road since it doesn't know root _label


@dataclass
class IdeaAttrHolder:
    weight: int = None
    uid: int = None
    required: RequiredUnit = None
    required_base: Road = None
    required_sufffact: Road = None
    required_sufffact_open: float = None
    required_sufffact_nigh: float = None
    required_sufffact_divisor: int = None
    required_del_sufffact_base: Road = None
    required_del_sufffact_need: Road = None
    required_suff_idea_active_status: str = None
    assignedunit: AssignedUnit = None
    begin: float = None
    close: float = None
    addin: float = None
    numor: float = None
    denom: float = None
    reest: bool = None
    numeric_road: Road = None
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


@dataclass
class IdeaCore:
    _label: str = None
    _uid: int = None  # Calculated field?
    _pad: str = None
    _kids: dict = None
    _weight: int = None
    _balancelinks: dict[GroupBrand:BalanceLink] = None
    _balanceheirs: dict[GroupBrand:BalanceHeir] = None  # Calculated field
    _balancelines: dict[GroupBrand:BalanceLink] = None  # Calculated field
    _requiredunits: dict[Road:RequiredUnit] = None
    _requiredheirs: dict[Road:RequiredHeir] = None  # Calculated field
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
    _range_source_road: Road = None
    _numeric_road: Road = None
    promise: bool = None
    _problem_bool: bool = None
    _originunit: OriginUnit = None
    _on_meld_weight_action: str = None
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
    _road_node_delimiter: str = None

    def is_intent_item(self, base_x: Road = None):
        # bool_x = False
        return (
            self.promise == True
            and self._active_status == True
            and (
                base_x is None
                or any(
                    required.base == base_x for required in self._requiredunits.values()
                )
            )
        )

    def set_active_status_hx_empty_if_null(self):
        if self._active_status_hx is None:
            self._active_status_hx = {}

    def record_active_status_hx(
        self,
        tree_traverse_count: int,
        prev_active_status: bool,
        curr_active_status: bool,
    ):
        if tree_traverse_count == 0:
            self._active_status_hx = {0: curr_active_status}
        else:
            self.set_active_status_hx_empty_if_null()
            if prev_active_status != curr_active_status:
                self._active_status_hx[tree_traverse_count] = curr_active_status

    def get_key_road(self):
        return self._label

    def set_acptfactheirs(self, acptfacts: dict[Road:AcptFactCore]):
        acptfacts = self._get_empty_dict_if_null(x_dict=acptfacts)
        self.set_acptfactheirs_empty_if_null()
        x_dict = {}
        for h in acptfacts.values():
            x_acptfact = acptfactheir_shop(
                base=h.base, pick=h.pick, open=h.open, nigh=h.nigh
            )
            self.delete_acptfactunit_if_past(acptfactheir=x_acptfact)
            x_acptfact = self.apply_acptfactunit_transformations(
                acptfactheir=x_acptfact
            )
            x_dict[x_acptfact.base] = x_acptfact

        self._acptfactheirs = x_dict

    def set_acptfactheirs_empty_if_null(self):
        if self._acptfactheirs is None:
            self._acptfactheirs == {}

    def apply_acptfactunit_transformations(
        self, acptfactheir: AcptFactHeir
    ) -> AcptFactHeir:
        for acptfactunit in self._acptfactunits.values():
            if acptfactunit.base == acptfactheir.base:
                acptfactheir.transform(acptfactunit=acptfactunit)
        return acptfactheir

    def delete_acptfactunit_if_past(self, acptfactheir: AcptFactHeir):
        self.set_acptfactunits_empty_if_null()
        delete_acptfactunit = False
        for acptfactunit in self._acptfactunits.values():
            if (
                acptfactunit.base == acptfactheir.base
                and acptfactunit.nigh != None
                and acptfactheir.open != None
            ) and acptfactunit.nigh < acptfactheir.open:
                delete_acptfactunit = True

        if delete_acptfactunit == True:
            del self._acptfactunits[acptfactunit.base]

        return acptfactheir

    def set_acptfactunits_empty_if_null(self):
        if self._acptfactunits is None:
            self._acptfactunits = {}

    def set_acptfactunit(self, acptfactunit: AcptFactUnit):
        self.set_acptfactunits_empty_if_null()
        self._acptfactunits[acptfactunit.base] = acptfactunit

    def _set_ideakid_attr(
        self,
        acptfactunit: AcptFactUnit = None,
        acptfactunit_base: Road = None,
        acptfactunit_sufffact: Road = None,
        acptfactunit_open: float = None,
        acptfactunit_nigh: float = None,
    ):
        if acptfactunit != None:
            self.set_acptfactunit(acptfactunit=acptfactunit)
        if acptfactunit_base != None and acptfactunit_sufffact != None:
            self.set_acptfactunit(
                base=acptfactunit_base,
                need=acptfactunit_sufffact,
                open=acptfactunit_open,
                nigh=acptfactunit_nigh,
            )

    def get_acptfactunits_dict(self):
        acptfactunits_dict = {}
        if self._acptfactunits != None:
            for hc in self._acptfactunits.values():
                acptfactunits_dict[hc.base] = hc.get_dict()
        return acptfactunits_dict

    def set_acptfactunit_to_complete(self, base_acptfactunit: AcptFactUnit):
        # if a idea is considered a task then a acptfactheir.open attribute can be increased to
        # a number <= acptfactheir.nigh so the idea no longer is a task. This method finds
        # the minimal acptfactheir.open to change idea._task == False. idea_core._acptfactheir cannot be straight up manpulated
        # so idea._acptfactunit reqquires being changed.
        # self.set_acptfactunits(base=acptfact, acptfact=base, open=sufffact_nigh, nigh=acptfact_nigh)
        acptfact_curb_x = acptfactunit_shop(
            base=base_acptfactunit.base,
            pick=base_acptfactunit.base,
            open=base_acptfactunit.nigh,
            nigh=base_acptfactunit.nigh,
        )
        self._acptfactunits[base_acptfactunit.base] = acptfact_curb_x

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
            idea_x
            for idea_x in self._kids.values()
            if (
                (begin >= idea_x._begin and begin < idea_x._close)
                or (close > idea_x._begin and close < idea_x._close)
                or (begin <= idea_x._begin and close >= idea_x._close)
            )
        ]

    def create_road(
        self,
        road_begin: Road = None,
        terminus_node: RaodNode = None,
        road_nodes: list[RaodNode] = None,
    ):
        return road_get_road(
            road_begin=road_begin,
            terminus_node=terminus_node,
            road_nodes=road_nodes,
            delimiter=self._road_node_delimiter,
        )

    def get_idea_road(self) -> Road:
        if self._pad in (None, ""):
            return self.create_road(self._label)
        else:
            return self.create_road(self._pad, self._label)

    def clear_descendant_promise_count(self):
        self._descendant_promise_count = None

    def set_descendant_promise_count_zero_if_null(self):
        if self._descendant_promise_count is None:
            self._descendant_promise_count = 0

    def get_descendant_roads(self) -> dict[Road:int]:
        self.set_kids_empty_if_null()
        descendant_roads = {}
        to_evaluate_ideas = list(self._kids.values())
        count_x = 0
        max_count = 1000
        while to_evaluate_ideas != [] and count_x < max_count:
            idea_x = to_evaluate_ideas.pop()
            idea_x.set_kids_empty_if_null()
            descendant_roads[idea_x.get_idea_road()] = -1
            to_evaluate_ideas.extend(idea_x._kids.values())
            count_x += 1

        if count_x == max_count:
            raise IdeaGetDescendantsException(
                f"Idea '{self.get_idea_road()}' either has an infinite loop or more than {max_count} descendants."
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

    def set_pad(self, parent_road, parent_label=None):
        if parent_road == "" and parent_label is None:
            self._pad = ""
        elif parent_road == "" and parent_label != None:
            self._pad = parent_label
        elif parent_road != "" and parent_label in ("", None):
            self._pad = self.create_road(parent_road)
        else:
            self._pad = self.create_road(parent_road, parent_label)

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

        self.set_balancelink_empty_if_null()
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
            balanceline_x = BalanceLine(
                brand=bh.brand,
                _agenda_credit=bh._agenda_credit,
                _agenda_debt=bh._agenda_debt,
            )
            self._balancelines[balanceline_x.brand] = balanceline_x

    def set_balancelines(self, child_balancelines: dict[GroupBrand:BalanceLine] = None):
        self.set_balancelines_empty_if_null()
        if child_balancelines is None:
            child_balancelines = {}

        # get balancelines from child
        for bl in child_balancelines.values():
            if self._balancelines.get(bl.brand) is None:
                self._balancelines[bl.brand] = BalanceLine(
                    brand=bl.brand,
                    _agenda_credit=0,
                    _agenda_debt=0,
                )

            self._balancelines[bl.brand].add_agenda_credit_debt(
                agenda_credit=bl._agenda_credit, agenda_debt=bl._agenda_debt
            )

    def set_kids_total_weight(self):
        self._kids_total_weight = 0
        self.set_kids_empty_if_null()
        for idea_x in self._kids.values():
            self._kids_total_weight += idea_x._weight

    def get_balanceheirs_creditor_weight_sum(self):
        self.set_balancelink_empty_if_null()
        self.set_balanceheir_empty_if_null()
        return sum(
            balancelink.creditor_weight for balancelink in self._balanceheirs.values()
        )

    def get_balanceheirs_debtor_weight_sum(self):
        self.set_balancelink_empty_if_null()
        self.set_balanceheir_empty_if_null()
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

    def set_kids_empty_if_null(self):
        if self._kids is None:
            self._kids = {}

    def clear_balancelines(self):
        self._balancelines = {}

    def set_idea_label(self, _label):
        if _label != None:
            self._label = _label

    def set_road_node_delimiter(self, new_road_node_delimiter: str):
        old_delimiter = deepcopy(self._road_node_delimiter)
        self._road_node_delimiter = get_node_delimiter(new_road_node_delimiter)
        self._pad = replace_road_node_delimiter(
            road=self._pad,
            old_delimiter=old_delimiter,
            new_delimiter=self._road_node_delimiter,
        )
        if self._numeric_road != None:
            self._numeric_road = replace_road_node_delimiter(
                road=self._numeric_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_node_delimiter,
            )
        if self._range_source_road != None:
            self._range_source_road = replace_road_node_delimiter(
                road=self._range_source_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_node_delimiter,
            )

        new_requiredunits = {}
        for requiredunit_road, requiredunit_obj in self._requiredunits.items():
            new_requiredunit_road = replace_road_node_delimiter(
                road=requiredunit_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_node_delimiter,
            )
            requiredunit_obj.set_delimiter(self._road_node_delimiter)
            new_requiredunits[new_requiredunit_road] = requiredunit_obj
        self._requiredunits = new_requiredunits

        new_acptfactunits = {}
        for acptfactunit_road, acptfactunit_obj in self._acptfactunits.items():
            new_base_road = replace_road_node_delimiter(
                road=acptfactunit_road,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_node_delimiter,
            )
            acptfactunit_obj.base = new_base_road
            new_pick_road = replace_road_node_delimiter(
                road=acptfactunit_obj.pick,
                old_delimiter=old_delimiter,
                new_delimiter=self._road_node_delimiter,
            )
            acptfactunit_obj.set_attr(pick=new_pick_road)
            new_acptfactunits[new_base_road] = acptfactunit_obj
        self._acptfactunits = new_acptfactunits

    def _meld_requiredunits(self, other_idea):
        self.set_requiredunits_empty_if_null()
        other_idea.set_requiredunits_empty_if_null()
        for lx in other_idea._requiredunits.values():
            if self._requiredunits.get(lx.base) is None:
                self._requiredunits[lx.base] = lx
            else:
                self._requiredunits.get(lx.base).meld(lx)

    def _meld_balancelinks(self, other_idea):
        self.set_balancelink_empty_if_null()
        other_idea.set_balancelink_empty_if_null()
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
        self.set_acptfactunits_empty_if_null()
        other_idea.set_acptfactunits_empty_if_null()
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
            self.set_originunit_empty_if_null()
            self._originunit.set_originlink(pid=party_pid, weight=party_weight)

    def set_originunit_empty_if_null(self):
        if self._originunit is None:
            self._originunit = originunit_shop()

    def get_originunit_dict(self):
        self.set_originunit_empty_if_null()
        return self._originunit.get_dict()

    def _meld_attributes_that_will_be_equal(self, other_idea):
        xl = [
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
        while xl != []:
            attrs = xl.pop()
            if attrs[1] != attrs[2]:
                raise InvalidIdeaException(
                    f"Meld fail idea={self.get_idea_road()} {attrs[0]}:{attrs[1]} with {other_idea.get_idea_road()} {attrs[0]}:{attrs[2]}"
                )

    def _set_idea_attr(self, idea_attr: IdeaAttrHolder):
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

        self._del_requiredunit_all_cases(
            base=idea_attr.required_del_sufffact_base,
            sufffact=idea_attr.required_del_sufffact_need,
        )
        self._set_addin_to_zero_if_any_transformations_exist()

    def _check_get_on_meld_weight_actions(self, on_meld_weight_action: str):
        if on_meld_weight_action not in (list(get_on_meld_weight_actions())):
            raise InvalidIdeaException(
                f"IdeaCore unit '{self._label}' cannot have on_meld_weight_action '{on_meld_weight_action}'."
            )

    def _set_addin_to_zero_if_any_transformations_exist(self):
        if (
            self._begin != None
            and self._close != None
            and (self._numor != None or self._denom != None)
            and self._addin is None
        ):
            self._addin = 0

    def _del_requiredunit_all_cases(self, base: Road, sufffact: Road):
        if base != None and sufffact != None:
            self.del_requiredunit_sufffact(base=base, sufffact=sufffact)
            if len(self._requiredunits[base].sufffacts) == 0:
                self.del_requiredunit_base(base=base)

    def set_required_suff_idea_active_status(
        self, base: Road, suff_idea_active_status: str
    ):
        requiredunit_x = self._get_or_create_requiredunit(base=base)
        if suff_idea_active_status == False:
            requiredunit_x.suff_idea_active_status = False
        elif suff_idea_active_status == "Set to Ignore":
            requiredunit_x.suff_idea_active_status = None
        elif suff_idea_active_status == True:
            requiredunit_x.suff_idea_active_status = True

    def _get_or_create_requiredunit(self, base: Road):
        self.set_requiredunits_empty_if_null()
        requiredunit_x = None
        try:
            requiredunit_x = self._requiredunits[base]
        except Exception:
            requiredunit_x = requiredunit_shop(
                base, delimiter=self._road_node_delimiter
            )
            self._requiredunits[base] = requiredunit_x
        return requiredunit_x

    def set_required_sufffact(
        self,
        base: Road,
        sufffact: Road,
        open: float,
        nigh: float,
        divisor: int,
    ):
        requiredunit_x = self._get_or_create_requiredunit(base=base)
        requiredunit_x.set_sufffact(
            sufffact=sufffact, open=open, nigh=nigh, divisor=divisor
        )

    def del_requiredunit_base(self, base: Road):
        try:
            self._requiredunits.pop(base)
        except KeyError as e:
            raise InvalidIdeaException(f"No RequiredUnit at '{base}'") from e

    def del_requiredunit_sufffact(self, base: Road, sufffact: Road):
        required_unit = self._requiredunits[base]
        required_unit.del_sufffact(sufffact=sufffact)

    def add_kid(self, idea_kid):
        if idea_kid._numor != None:
            # if idea_kid._denom != None:
            # if idea_kid._reest != None:
            if self._begin is None or self._close is None:
                raise InvalidIdeaException(
                    f"Idea {idea_kid.get_idea_road()} cannot have numor,denom,reest if parent does not have begin/close range"
                )

            idea_kid._begin = self._begin * idea_kid._numor / idea_kid._denom
            idea_kid._close = self._close * idea_kid._numor / idea_kid._denom

        self.set_kids_empty_if_null()
        self._kids[idea_kid._label] = idea_kid
        self._kids = dict(sorted(self._kids.items()))

    def set_balancelink_empty_if_null(self):
        if self._balancelinks is None:
            self._balancelinks = {}

    def set_balanceheir_empty_if_null(self):
        if self._balanceheirs is None:
            self._balanceheirs = {}

    def set_balancelines_empty_if_null(self):
        if self._balancelines is None:
            self._balancelines = {}

    def set_balancelink(self, balancelink: BalanceLink):
        self.set_balancelink_empty_if_null()
        self._balancelinks[balancelink.brand] = balancelink

    def del_balancelink(self, groupbrand: GroupBrand):
        self.set_balancelink_empty_if_null()
        try:
            self._balancelinks.pop(groupbrand)
        except KeyError as e:
            raise (f"Cannot delete balancelink '{groupbrand}'.") from e

    def set_required_unit(self, required: RequiredUnit):
        self.set_requiredunits_empty_if_null()
        required.delimiter = self._road_node_delimiter
        self._requiredunits[required.base] = required

    def set_requiredunits_empty_if_null(self):
        if self._requiredunits is None:
            self._requiredunits = {}

    def set_requiredheirs_status(self):
        self.set_requiredunits_empty_if_null()
        for lu in self._requiredheirs.values():
            lu.set_status(acptfacts=self._acptfactheirs)

    def set_active_status(
        self,
        tree_traverse_count: int,
        agenda_groups: dict[GroupBrand:GroupUnit] = None,
        agenda_healer: str = None,
    ):
        self.set_acptfactheirs_empty_if_null()
        self.clear_requiredheirs_status()
        prev_to_now_active_status = bool(self._active_status)
        self._active_status = True
        self._task = False
        self.set_requiredheirs_status()

        for requiredheir in self._requiredheirs.values():
            # one required.status is false, idea.active_status is false
            if requiredheir._status == False:
                self._active_status = False
            # one required.task is true, idea._task is True
            if requiredheir._task == True:
                self._task = True

        if self._active_status == False:
            self._task = None
        elif (
            self.promise == True
            and self._active_status == True
            and self._requiredheirs == {}
        ):
            self._task = True

        if (
            self._active_status
            and agenda_groups != None
            and agenda_healer != None
            and self._assignedheir._suffgroups != {}
        ):
            self._assignedheir.set_group_party(agenda_groups, agenda_healer)
            if self._assignedheir._group_party == False:
                self._active_status = False

        self.record_active_status_hx(
            tree_traverse_count=tree_traverse_count,
            prev_active_status=prev_to_now_active_status,
            curr_active_status=self._active_status,
        )

    def clear_requiredheirs_status(self):
        self.set_requiredheirs_empty_if_null()
        for required in self._requiredheirs.values():
            required.clear_status()

    def _coalesce_with_requiredunits(self, requiredheirs: dict[Road:RequiredHeir]):
        self.set_requiredunits_empty_if_null()
        self.set_requiredheirs_empty_if_null()

        requiredheirs_new = self._get_empty_dict_if_null(x_dict=deepcopy(requiredheirs))
        requiredheirs_new.update(self._requiredunits)
        return requiredheirs_new

    def set_requiredheirs(
        self,
        agenda_idea_dict: dict[Road:],
        requiredheirs: dict[Road:RequiredCore] = None,
    ):
        if requiredheirs is None:
            requiredheirs = self._requiredheirs
        coalesced_requireds = self._coalesce_with_requiredunits(requiredheirs)

        x_dict = {}
        for required in coalesced_requireds.values():
            requiredheir_x = requiredheir_shop(
                base=required.base,
                sufffacts=None,
                suff_idea_active_status=required.suff_idea_active_status,
            )
            sufffacts_x = {}
            for w in required.sufffacts.values():
                sufffact_x = sufffactunit_shop(
                    need=w.need,
                    open=w.open,
                    nigh=w.nigh,
                    divisor=w.divisor,
                )
                sufffacts_x[sufffact_x.need] = sufffact_x
            requiredheir_x.sufffacts = sufffacts_x

            if agenda_idea_dict != None:
                base_idea = agenda_idea_dict.get(required.base)
                if base_idea != None:
                    requiredheir_x.set_curr_idea_active_status(
                        bool_x=base_idea._active_status
                    )

            x_dict[requiredheir_x.base] = requiredheir_x
        self._requiredheirs = x_dict

    def set_requiredheirs_empty_if_null(self):
        if self._requiredheirs is None:
            self._requiredheirs = {}

    def get_requiredheir(self, base: Road):
        self.set_requiredheirs_empty_if_null()
        return self._requiredheirs.get(base)

    def get_requiredunits_dict(self):
        x_dict = {}
        if self._requiredunits != None:
            for base, required in self._requiredunits.items():
                x_dict[base] = required.get_dict()
        return x_dict

    def get_kids_dict(self):
        x_dict = {}
        if self._kids != None:
            for c_road, kid in self._kids.items():
                x_dict[c_road] = kid.get_dict()
        return x_dict

    def get_balancelinks_dict(self):
        balancelinks_dict = {}
        if self._balancelinks != None:
            for group_pid, balancelink in self._balancelinks.items():
                balancelinks_dict[group_pid] = balancelink.get_dict()
        return balancelinks_dict

    def _get_empty_dict_if_null(self, x_dict: dict) -> dict:
        if x_dict is None:
            x_dict = {}
        return x_dict

    def is_kidless(self):
        return self._kids == {}

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

    def find_replace_road(self, old_road: Road, new_road: Road):
        if is_sub_road(ref_road=self._pad, sub_road=old_road):
            self._pad = change_road(self._pad, old_road, new_road)
        if is_sub_road(ref_road=self._range_source_road, sub_road=old_road):
            self._range_source_road = change_road(
                self._range_source_road, old_road, new_road
            )
        if is_sub_road(ref_road=self._numeric_road, sub_road=old_road):
            self._numeric_road = change_road(self._numeric_road, old_road, new_road)

        self.set_requiredunits_empty_if_null()
        self._requiredunits == find_replace_road_key_dict(
            dict_x=self._requiredunits, old_road=old_road, new_road=new_road
        )

        self.set_acptfactunits_empty_if_null()
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
        self.set_assignedunit_empty_if_null()
        self._assignedheir = assigned_heir_shop()
        self._assignedheir.set_suffgroups(
            parent_assignheir=parent_assignheir,
            assignunit=self._assignedunit,
            agenda_groups=agenda_groups,
        )

    def get_assignedunit_dict(self):
        self.set_assignedunit_empty_if_null()
        return self._assignedunit.get_dict()

    def assignor_in(self, groupbrands: dict[GroupBrand:-1]):
        return self._assignedheir.group_in(groupbrands)


@dataclass
class IdeaKid(IdeaCore):
    pass


def ideacore_shop(
    _label: str = None,
    _uid: int = None,  # Calculated field?
    _pad: str = None,
    _kids: dict = None,
    _weight: int = 1,
    _balancelinks: dict[GroupBrand:BalanceLink] = None,
    _balanceheirs: dict[GroupBrand:BalanceHeir] = None,  # Calculated field
    _balancelines: dict[GroupBrand:BalanceLink] = None,  # Calculated field
    _requiredunits: dict[Road:RequiredUnit] = None,
    _requiredheirs: dict[Road:RequiredHeir] = None,  # Calculated field
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
    _range_source_road: Road = None,
    _numeric_road: Road = None,
    promise: bool = None,
    _problem_bool: bool = None,
    _originunit: OriginUnit = None,
    _on_meld_weight_action: str = None,
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
    _road_node_delimiter: str = None,
) -> IdeaCore:
    if promise is None:
        promise = False
    if _problem_bool is None:
        _problem_bool = False
    if _on_meld_weight_action is None:
        _on_meld_weight_action = "default"
    if _kids_total_weight is None:
        _kids_total_weight = 0

    return IdeaKid(
        _label=_label,
        _uid=_uid,
        _pad=_pad,
        _kids=_kids,
        _weight=_weight,
        _balancelinks=_balancelinks,
        _balanceheirs=_balanceheirs,
        _balancelines=_balancelines,
        _requiredunits=_requiredunits,
        _requiredheirs=_requiredheirs,
        _assignedunit=_assignedunit,
        _assignedheir=_assignedheir,
        _acptfactunits=_acptfactunits,
        _acptfactheirs=_acptfactheirs,
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
        _active_status_hx=_active_status_hx,
        _road_node_delimiter=get_node_delimiter(_road_node_delimiter),
    )


class IdeaRootLabelNotEmptyException(Exception):
    pass


@dataclass
class IdeaRoot(IdeaCore):
    def set_idea_label(self, _label: str, agenda_culture_qid: str = None):
        if _label != root_label() and agenda_culture_qid is None:
            raise IdeaRootLabelNotEmptyException(
                f"Cannot set idearoot to string other than '{root_label()}'"
            )
        elif _label != agenda_culture_qid != None:
            raise IdeaRootLabelNotEmptyException(
                f"Cannot set idearoot to string other than '{agenda_culture_qid}'"
            )
        elif _label != root_label() and agenda_culture_qid == _label:
            self._label = _label
        else:
            self._label = root_label()


def idearoot_shop(
    _label: str = None,
    _uid: int = None,  # Calculated field?
    _pad: str = None,
    _kids: dict = None,
    _weight: int = 1,
    _balancelinks: dict[GroupBrand:BalanceLink] = None,
    _balanceheirs: dict[GroupBrand:BalanceHeir] = None,  # Calculated field
    _balancelines: dict[GroupBrand:BalanceLink] = None,  # Calculated field
    _requiredunits: dict[Road:RequiredUnit] = None,
    _requiredheirs: dict[Road:RequiredHeir] = None,  # Calculated field
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
    _range_source_road: Road = None,
    _numeric_road: Road = None,
    promise: bool = None,
    _problem_bool: bool = None,
    _originunit: OriginUnit = None,
    _on_meld_weight_action: str = None,
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
) -> IdeaCore:
    if promise is None:
        promise = False
    if _problem_bool is None:
        _problem_bool = False
    if _on_meld_weight_action is None:
        _on_meld_weight_action = "default"
    if _kids_total_weight is None:
        _kids_total_weight = 0

    x_idearoot = IdeaRoot(
        _label=_label,
        _uid=_uid,
        _pad=_pad,
        _kids=_kids,
        _weight=_weight,
        _balancelinks=_balancelinks,
        _balanceheirs=_balanceheirs,
        _balancelines=_balancelines,
        _requiredunits=_requiredunits,
        _requiredheirs=_requiredheirs,
        _assignedunit=_assignedunit,
        _assignedheir=_assignedheir,
        _acptfactunits=_acptfactunits,
        _acptfactheirs=_acptfactheirs,
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
        _active_status_hx=_active_status_hx,
    )
    if x_idearoot._label is None:
        x_idearoot.set_idea_label(_label=root_label())
    return x_idearoot


def get_obj_from_idea_dict(x_dict: dict[str:], field_name: str) -> any:
    if field_name == "_requiredunits":
        return (
            requireds_get_from_dict(x_dict[field_name])
            if x_dict.get(field_name) != None
            else None
        )
    elif field_name == "_assignedunit":
        return (
            assignedunit_get_from_dict(x_dict[field_name])
            if x_dict.get(field_name) != None
            else assigned_unit_shop()
        )
    elif field_name == "_originunit":
        return (
            originunit_get_from_dict(x_dict[field_name])
            if x_dict.get(field_name) != None
            else originunit_shop()
        )
    elif field_name == "_acptfactunits":
        return (
            acptfactunits_get_from_dict(x_dict[field_name])
            if x_dict.get(field_name) != None
            else acptfactunits_get_from_dict({})
        )
    elif field_name == "_balancelinks":
        return (
            balancelinks_get_from_dict(x_dict[field_name])
            if x_dict.get(field_name) != None
            else balancelinks_get_from_dict({})
        )
    elif field_name in {"_kids"}:
        return x_dict[field_name] if x_dict.get(field_name) != None else {}
    elif field_name in {"promise"}:
        return x_dict[field_name] if x_dict.get(field_name) != None else False
    elif field_name in {"_is_expanded"}:
        return x_dict[field_name] if x_dict.get(field_name) != None else True
    # elif field_name == "_on_meld_weight_action":
    #     return x_dict[field_name] if x_dict.get(field_name) != None else "default"
    else:
        return x_dict[field_name] if x_dict.get(field_name) != None else None
