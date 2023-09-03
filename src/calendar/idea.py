import dataclasses
from src.calendar.required_assign import (
    AssignedUnit,
    AssignedHeir,
    assigned_unit_shop,
    assigned_heir_shop,
)
from src.calendar.required_idea import (
    AcptFactCore,
    AcptFactHeir,
    acptfactheir_shop,
    RequiredCore,
    RequiredUnit,
    Road,
    AcptFactUnit,
    AcptFactUnit,
    acptfactunit_shop,
    RequiredHeir,
    sufffactunit_shop,
    Road,
    change_road,
    find_replace_road_key_dict,
)
from src.calendar.road import is_sub_road_in_src_road, get_global_root_desc as root_desc
from src.calendar.group import (
    GroupHeir,
    GroupLink,
    GroupName,
    Groupline,
    groupheir_shop,
    GroupUnit,
)
from src.calendar.x_func import (
    get_on_meld_weight_actions,
    get_meld_weight,
    return1ifnone as x_func_return1ifnone,
)
from copy import deepcopy


class InvalidIdeaException(Exception):
    pass


@dataclasses.dataclass
class IdeaBare:
    n: str = None  # name
    weight: int = 1
    b: float = None  # begin
    c: float = None  # close  # where
    a: float = None  # addin
    rr: str = None  # relative_road # not road since it doesn't know root _desc
    mn: int = None  # numor
    md: int = None  # denom
    mr: bool = None  # reest
    sr: str = None  # special_road # not road since it doesn't know root _desc
    nr: str = None  # numeric_road # not road since it doesn't know root _desc


@dataclasses.dataclass
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
    special_road: float = None
    promise: bool = None
    problem_bool: bool = None
    acptfactunit: AcptFactUnit = None
    descendant_promise_count: int = None
    all_member_credit: bool = None
    all_member_debt: bool = None
    grouplink: GroupLink = None
    grouplink_del: GroupName = None
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


@dataclasses.dataclass
class IdeaCore:
    _desc: str = None
    _uid: int = None
    _walk: str = None
    _kids: dict = None  # dict[]
    _weight: int = 1
    _grouplinks: dict[GroupName:GroupLink] = None
    _groupheirs: dict[GroupName:GroupHeir] = None
    _grouplines: dict[GroupName:GroupLink] = None
    _level: int = None
    _requiredunits: dict[Road:RequiredUnit] = None
    _requiredheirs: dict[Road:RequiredHeir] = None
    _assignedunit: AssignedUnit = None
    _assignedheir: AssignedHeir = None
    _calendar_importance: float = None
    _calendar_coin_onset: float = None
    _calendar_coin_cease: float = None
    _kids_total_weight: int = 0
    _begin: float = None
    _close: float = None
    _addin: float = None
    _denom: int = None
    _numor: int = None
    _reest: bool = None
    _special_road: Road = None
    _numeric_road: Road = None
    promise: bool = False
    _problem_bool: bool = False
    _task: bool = None
    _active_status: bool = None
    _ancestor_promise_count: int = None
    _descendant_promise_count: int = None
    _all_member_credit: bool = None
    _all_member_debt: bool = None
    _is_expanded: bool = True
    _active_status: bool = None
    _sibling_total_weight: int = None
    _acptfactheirs: dict[AcptFactHeir] = None
    _acptfactunits: dict[AcptFactUnit] = None
    _on_meld_weight_action: str = "default"
    _active_status_hx: dict[int:bool] = None

    def is_agenda_item(self, base_x: Road = None):
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
        return self._desc

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
        # if a idea is considered a task that means a acptfactheir.open attribute can be increased to
        # a number <= acptfactheir.nighmake that makes the idea no longer a task. This method finds
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

    def set_calendar_importance(
        self,
        coin_onset_x: float,
        parent_calendar_importance: float = None,
        parent_coin_cease: float = None,
    ):
        parent_calendar_importance = x_func_return1ifnone(parent_calendar_importance)
        self.set_kids_total_weight()
        self._calendar_importance = None
        self._calendar_coin_onset = None
        self._calendar_coin_cease = None
        sibling_ratio = self._weight / self._sibling_total_weight
        self._calendar_importance = parent_calendar_importance * sibling_ratio
        self._calendar_coin_onset = coin_onset_x
        self._calendar_coin_cease = (
            self._calendar_coin_onset + self._calendar_importance
        )
        self._calendar_coin_cease = min(self._calendar_coin_cease, parent_coin_cease)
        self.set_groupheirs_calendar_credit_debit()

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

    def get_road(self) -> Road:
        if self._walk in (None, ""):
            return f"{self._desc}"
        else:
            return f"{self._walk},{self._desc}"

    def clear_descendant_promise_count(self):
        self._descendant_promise_count = None

    def set_descendant_promise_count_zero_if_null(self):
        if self._descendant_promise_count is None:
            self._descendant_promise_count = 0

    def clear_all_member_credit_debt(self):
        self._all_member_credit = None
        self._all_member_debt = None

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

    def set_walk(self, parent_road, parent_desc=None):
        if parent_road in ("", None):
            self._walk = "" if parent_desc is None else parent_desc
        elif parent_desc in ("", None):
            self._walk = f"{parent_road}"
        else:
            self._walk = f"{parent_road},{parent_desc}"

    def inherit_groupheirs(self, parent_groupheirs: dict[GroupName:GroupHeir] = None):
        if parent_groupheirs is None:
            parent_groupheirs = {}

        self._groupheirs = {}
        for ib in parent_groupheirs.values():
            groupheir = groupheir_shop(
                name=ib.name,
                creditor_weight=ib.creditor_weight,
                debtor_weight=ib.debtor_weight,
            )
            self._groupheirs[groupheir.name] = groupheir

        self.set_grouplink_empty_if_null()
        for ib in self._grouplinks.values():
            groupheir = groupheir_shop(
                name=ib.name,
                creditor_weight=ib.creditor_weight,
                debtor_weight=ib.debtor_weight,
            )
            self._groupheirs[groupheir.name] = groupheir

    def set_kidless_grouplines(self):
        # get grouplines from self
        for bh in self._groupheirs.values():
            groupline_x = Groupline(
                name=bh.name,
                _calendar_credit=bh._calendar_credit,
                _calendar_debt=bh._calendar_debt,
            )
            self._grouplines[groupline_x.name] = groupline_x

    def set_grouplines(self, child_grouplines: dict[GroupName:Groupline] = None):
        self.set_grouplines_empty_if_null()
        if child_grouplines is None:
            child_grouplines = {}

        # get grouplines from child
        for bl in child_grouplines.values():
            if self._grouplines.get(bl.name) is None:
                self._grouplines[bl.name] = Groupline(
                    name=bl.name,
                    _calendar_credit=0,
                    _calendar_debt=0,
                )

            self._grouplines[bl.name].add_calendar_credit_debt(
                calendar_credit=bl._calendar_credit, calendar_debt=bl._calendar_debt
            )

    def set_kids_total_weight(self):
        self._kids_total_weight = 0
        self.set_kids_empty_if_null()
        for idea_x in self._kids.values():
            self._kids_total_weight += idea_x._weight

    def get_groupheirs_creditor_weight_sum(self):
        self.set_grouplink_empty_if_null()
        self.set_groupheir_empty_if_null()
        return sum(grouplink.creditor_weight for grouplink in self._groupheirs.values())

    def get_groupheirs_debtor_weight_sum(self):
        self.set_grouplink_empty_if_null()
        self.set_groupheir_empty_if_null()
        return sum(grouplink.debtor_weight for grouplink in self._groupheirs.values())

    def set_groupheirs_calendar_credit_debit(self):
        groupheirs_creditor_weight_sum = self.get_groupheirs_creditor_weight_sum()
        groupheirs_debtor_weight_sum = self.get_groupheirs_debtor_weight_sum()
        for groupheir_x in self._groupheirs.values():
            groupheir_x.set_calendar_credit_debt(
                idea_calendar_importance=self._calendar_importance,
                groupheirs_creditor_weight_sum=groupheirs_creditor_weight_sum,
                groupheirs_debtor_weight_sum=groupheirs_debtor_weight_sum,
            )

    def set_kids_empty_if_null(self):
        if self._kids is None:
            self._kids = {}

    def clear_grouplines(self):
        self._grouplines = {}

    def set_idea_desc(self, desc):
        if desc != None:
            self._desc = desc

    def meld_requiredunits(self, other_idea):
        self.set_requiredunits_empty_if_null()
        other_idea.set_requiredunits_empty_if_null()
        for lx in other_idea._requiredunits.values():
            if self._requiredunits.get(lx.base) is None:
                self._requiredunits[lx.base] = lx
            else:
                self._requiredunits.get(lx.base).meld(lx)

    def meld_grouplinks(self, other_idea):
        self.set_grouplink_empty_if_null()
        other_idea.set_grouplink_empty_if_null()
        for bl in other_idea._grouplinks.values():
            if self._grouplinks.get(bl.name) != None:
                self._grouplinks.get(bl.name).meld(
                    other_grouplink=bl,
                    other_on_meld_weight_action=other_idea._on_meld_weight_action,
                    src_on_meld_weight_action=self._on_meld_weight_action,
                )
            else:
                self._grouplinks[bl.name] = bl

    def meld_acptfactunits(self, other_idea):
        self.set_acptfactunits_empty_if_null()
        other_idea.set_acptfactunits_empty_if_null()
        for hc in other_idea._acptfactunits.values():
            if self._acptfactunits.get(hc.base) is None:
                self._acptfactunits[hc.base] = hc
            else:
                self._acptfactunits.get(hc.base).meld(hc)

    def meld(self, other_idea, _idearoot: bool = None):
        if _idearoot and self._desc != other_idea._desc:
            raise InvalidIdeaException(
                f"Meld fail idearoot _desc '{self._desc}' not the same as '{other_idea._desc}'"
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
        self.meld_requiredunits(other_idea=other_idea)
        self.meld_grouplinks(other_idea=other_idea)
        self.meld_acptfactunits(other_idea=other_idea)
        self.meld_attributes_that_will_be_equal(other_idea=other_idea)

    def meld_attributes_that_will_be_equal(self, other_idea):
        xl = [
            ("_uid", self._uid, other_idea._uid),
            ("_begin", self._begin, other_idea._begin),
            ("_close", self._close, other_idea._close),
            ("_addin", self._addin, other_idea._addin),
            ("_denom", self._denom, other_idea._denom),
            ("_numor", self._numor, other_idea._numor),
            ("_reest", self._reest, other_idea._reest),
            ("_special_road", self._special_road, other_idea._special_road),
            ("_numeric_road", self._numeric_road, other_idea._numeric_road),
            ("promise", self.promise, other_idea.promise),
            ("_is_expanded", self._is_expanded, other_idea._is_expanded),
        ]
        while xl != []:
            attrs = xl.pop()
            if attrs[1] != attrs[2]:
                raise InvalidIdeaException(
                    f"Meld fail idea={self._walk},{self._desc} {attrs[0]}:{attrs[1]} with {other_idea._walk},{other_idea._desc} {attrs[0]}:{attrs[2]}"
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
        if idea_attr.special_road != None:
            self._special_road = idea_attr.special_road
        if idea_attr.descendant_promise_count != None:
            self._descendant_promise_count = idea_attr.descendant_promise_count
        if idea_attr.all_member_credit != None:
            self._all_member_credit = idea_attr.all_member_credit
        if idea_attr.all_member_debt != None:
            self._all_member_debt = idea_attr.all_member_debt
        if idea_attr.grouplink != None:
            self.set_grouplink(grouplink=idea_attr.grouplink)
        if idea_attr.grouplink_del != None:
            self.del_grouplink(groupname=idea_attr.grouplink_del)
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
                f"IdeaCore unit '{self._desc}' cannot have on_meld_weight_action '{on_meld_weight_action}'."
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
            requiredunit_x = RequiredUnit(base=base, sufffacts={})
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
                    f"Idea {idea_kid._walk},{idea_kid._desc} cannot have numor,denom,reest if parent does not have begin/close range"
                )

            idea_kid._begin = self._begin * idea_kid._numor / idea_kid._denom
            idea_kid._close = self._close * idea_kid._numor / idea_kid._denom

        self.set_kids_empty_if_null()
        self._kids[idea_kid._desc] = idea_kid
        self._kids = dict(sorted(self._kids.items()))

    def set_grouplink_empty_if_null(self):
        if self._grouplinks is None:
            self._grouplinks = {}

    def set_groupheir_empty_if_null(self):
        if self._groupheirs is None:
            self._groupheirs = {}

    def set_grouplines_empty_if_null(self):
        if self._grouplines is None:
            self._grouplines = {}

    def set_grouplink(self, grouplink: GroupLink):
        self.set_grouplink_empty_if_null()
        self._grouplinks[grouplink.name] = grouplink

    def del_grouplink(self, groupname: GroupName):
        self.set_grouplink_empty_if_null()
        try:
            self._grouplinks.pop(groupname)
        except KeyError as e:
            raise (f"Cannot delete grouplink '{groupname}'.") from e

    def set_required_unit(self, required: RequiredUnit):
        self.set_requiredunits_empty_if_null()
        self._requiredunits[required.base] = required

    def set_requiredunits_empty_if_null(self):
        if self._requiredunits is None:
            self._requiredunits = {}

    def is_heir(self, src: Road, heir: Road) -> bool:
        return src == heir or heir.find(f"{src},") == 0

    def set_requiredheirs_status(self):
        self.set_requiredunits_empty_if_null()
        for lu in self._requiredheirs.values():
            lu.set_status(acptfacts=self._acptfactheirs)

    def set_active_status(
        self,
        tree_traverse_count: int,
        calendar_groups: dict[GroupName:GroupUnit] = None,
        calendar_owner: str = None,
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
            and calendar_groups != None
            and calendar_owner != None
            and self._assignedheir._suffgroups != {}
        ):
            self._assignedheir.set_group_member(calendar_groups, calendar_owner)
            if self._assignedheir._group_member == False:
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
        calendar_idea_dict: dict[Road:],
        requiredheirs: dict[Road:RequiredCore] = None,
    ):
        if requiredheirs is None:
            requiredheirs = self._requiredheirs
        coalesced_requireds = self._coalesce_with_requiredunits(requiredheirs)

        x_dict = {}
        for required in coalesced_requireds.values():
            requiredheir_x = RequiredHeir(
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

            if calendar_idea_dict != None:
                base_idea = calendar_idea_dict.get(required.base)
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

    def get_grouplinks_dict(self):
        grouplinks_dict = {}
        if self._grouplinks != None:
            for group_name, grouplink in self._grouplinks.items():
                grouplinks_dict[group_name] = grouplink.get_dict()
        return grouplinks_dict

    def _get_empty_dict_if_null(self, x_dict: dict) -> dict:
        if x_dict is None:
            x_dict = {}
        return x_dict

    def is_kidless(self):
        return self._kids == {}

    def is_groupheirless(self):
        x_bool = None
        if self._groupheirs in [{}, None]:
            x_bool = True
        elif self._groupheirs != [{}, None]:
            x_bool = False
        return x_bool

    def get_dict(self):
        return {
            "_kids": self.get_kids_dict(),
            "_requiredunits": self.get_requiredunits_dict(),
            "_assignedunit": self.get_assignedunit_dict(),
            "_grouplinks": self.get_grouplinks_dict(),
            "_weight": self._weight,
            "_desc": self._desc,
            "_uid": self._uid,
            "_begin": self._begin,
            "_close": self._close,
            "_addin": self._addin,
            "_numor": self._numor,
            "_denom": self._denom,
            "_reest": self._reest,
            "_special_road": self._special_road,
            "_numeric_road": self._numeric_road,
            "promise": self.promise,
            "_problem_bool": self._problem_bool,
            "_acptfactunits": self.get_acptfactunits_dict(),
            "_is_expanded": self._is_expanded,
            "_on_meld_weight_action": self._on_meld_weight_action,
        }

    def find_replace_road(self, old_road: Road, new_road: Road):
        if is_sub_road_in_src_road(src_road=self._walk, sub_road=old_road):
            self._walk = change_road(self._walk, old_road, new_road)
        if is_sub_road_in_src_road(src_road=self._special_road, sub_road=old_road):
            self._special_road = change_road(self._special_road, old_road, new_road)
        if is_sub_road_in_src_road(src_road=self._numeric_road, sub_road=old_road):
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
        calendar_groups: dict[GroupName:GroupUnit],
    ):
        self.set_assignedunit_empty_if_null()
        self._assignedheir = assigned_heir_shop()
        self._assignedheir.set_suffgroups(
            parent_assignheir=parent_assignheir,
            assignunit=self._assignedunit,
            calendar_groups=calendar_groups,
        )

    def get_assignedunit_dict(self):
        self.set_assignedunit_empty_if_null()
        return self._assignedunit.get_dict()


@dataclasses.dataclass
class IdeaKid(IdeaCore):
    pass


class IdeaRootDescNotEmptyException(Exception):
    pass


@dataclasses.dataclass
class IdeaRoot(IdeaCore):
    def __post_init__(self):
        self.set_idea_desc(desc=root_desc())

    def set_idea_desc(self, desc):
        if desc != root_desc():
            raise IdeaRootDescNotEmptyException(
                f"Cannot set idearoot to string other than '{root_desc()}'"
            )
        else:
            self._desc = root_desc()
