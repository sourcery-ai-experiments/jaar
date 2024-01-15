from dataclasses import dataclass
from src._prime.road import (
    RoadUnit,
    change_road,
    find_replace_road_key_dict,
    replace_road_delimiter,
    is_heir_road,
    default_road_delimiter_if_none,
)
from src.tools.python import get_empty_dict_if_none
from copy import deepcopy as copy_deepcopy


class InvalidReasonException(Exception):
    pass


@dataclass
class BeliefCore:
    base: RoadUnit
    pick: RoadUnit
    open: float = None
    nigh: float = None

    def get_dict(self):
        x_dict = {
            "base": self.base,
            "pick": self.pick,
        }
        if self.open != None:
            x_dict["open"] = self.open
        if self.nigh != None:
            x_dict["nigh"] = self.nigh
        return x_dict

    def set_range_null(self):
        self.open = None
        self.nigh = None

    def set_attr(self, pick: RoadUnit = None, open: float = None, nigh: float = None):
        if pick != None:
            self.pick = pick
        if open != None:
            self.open = open
        if nigh != None:
            self.nigh = nigh

    def find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        self.base = change_road(self.base, old_road, new_road)
        self.pick = change_road(self.pick, old_road, new_road)

    def get_obj_key(self):
        return self.base

    def meld(self, other_beliefcore, same_reason: bool = False):
        if same_reason and other_beliefcore.base != self.base:
            raise InvalidReasonException(
                f"Meld fail: base={other_beliefcore.base} is different {self.base=}"
            )
        elif same_reason and other_beliefcore.pick != self.pick:
            raise InvalidReasonException(
                f"Meld fail: pick={other_beliefcore.pick} is different {self.pick=}"
            )
        elif same_reason and other_beliefcore.open != self.open:
            raise InvalidReasonException(
                f"Meld fail: base={other_beliefcore.base} open={other_beliefcore.open} is different {self.open=}"
            )
        elif same_reason and other_beliefcore.nigh != self.nigh:
            raise InvalidReasonException(
                f"Meld fail: base={other_beliefcore.base} nigh={other_beliefcore.nigh} is different {self.nigh=}"
            )
        else:
            self.base = other_beliefcore.base
            self.pick = other_beliefcore.pick
            self.open = other_beliefcore.open
            self.nigh = other_beliefcore.nigh
        return self


@dataclass
class BeliefUnit(BeliefCore):
    pass


# class BeliefUnitsshop:
def beliefunits_get_from_dict(x_dict: dict):
    beliefs = {}
    for belief_dict in x_dict.values():
        x_base = belief_dict["base"]
        x_pick = belief_dict["pick"]

        try:
            x_open = belief_dict["open"]
        except KeyError:
            x_open = None
        try:
            x_nigh = belief_dict["nigh"]
        except KeyError:
            x_nigh = None

        x_belief = beliefunit_shop(
            base=x_base,
            pick=x_pick,
            open=x_open,
            nigh=x_nigh,
        )

        beliefs[x_belief.base] = x_belief
    return beliefs


def beliefunit_shop(
    base: RoadUnit = None, pick: RoadUnit = None, open: float = None, nigh: float = None
) -> BeliefUnit:
    return BeliefUnit(base=base, pick=pick, open=open, nigh=nigh)


@dataclass
class BeliefHeir(BeliefCore):
    def transform(self, beliefunit: BeliefUnit):
        if (
            (self.open != None and beliefunit.open != None and self.nigh != None)
            and self.open <= beliefunit.open
            and self.nigh >= beliefunit.open
        ):
            self.open = beliefunit.open

    def is_range(self):
        return self.open != None and self.nigh != None


def beliefheir_shop(
    base: RoadUnit = None, pick: RoadUnit = None, open: float = None, nigh: float = None
) -> BeliefHeir:
    return BeliefHeir(base=base, pick=pick, open=open, nigh=nigh)


class PremiseStatusFinderException(Exception):
    pass


@dataclass
class PremiseStatusFinder:
    premise_open: float  # always within 0 and divisor, can be more than premise_nigh
    premise_nigh: float  # always within 0 and divisor, can be less than premise_open
    premise_divisor: float  # always greater than zero
    belief_open_full: float  # always less than belief nigh
    belief_nigh_full: float  # always less than belief nigh

    def check_attr(self):
        if None in (
            self.premise_open,
            self.premise_nigh,
            self.premise_divisor,
            self.belief_open_full,
            self.belief_nigh_full,
        ):
            raise PremiseStatusFinderException("No parameter can be None")

        if self.belief_open_full > self.belief_nigh_full:
            raise PremiseStatusFinderException(
                f"{self.belief_open_full=} cannot be greater that {self.belief_nigh_full=}"
            )

        if self.premise_divisor <= 0:
            raise PremiseStatusFinderException(
                f"{self.premise_divisor=} cannot be less/equal to zero"
            )

        if self.premise_open < 0 or self.premise_open > self.premise_divisor:
            raise PremiseStatusFinderException(
                f"{self.premise_open=} cannot be less than zero or greater than {self.premise_divisor=}"
            )

        if self.premise_nigh < 0 or self.premise_nigh > self.premise_divisor:
            raise PremiseStatusFinderException(
                f"{self.premise_nigh=} cannot be less than zero or greater than {self.premise_divisor=}"
            )

    def bo(self) -> float:
        return self.belief_open_full % self.premise_divisor

    def bn(self) -> float:
        return self.belief_nigh_full % self.premise_divisor

    def po(self) -> float:
        return self.premise_open

    def pn(self) -> float:
        return self.premise_nigh

    def pd(self) -> float:
        return self.premise_divisor

    def get_active_status(self) -> bool:
        if self.belief_nigh_full - self.belief_open_full > self.premise_divisor:
            return True
        # Case B1
        elif get_range_less_than_divisor_active_status(
            bo=self.bo(), bn=self.bn(), po=self.po(), pn=self.pn()
        ):
            return True

        return False

    def get_task_status(self):
        return bool(
            (
                self.get_active_status()
                and get_collasped_beliefrange_active_status(
                    self.premise_open,
                    self.premise_nigh,
                    self.premise_divisor,
                    self.belief_nigh_full,
                )
                == False
            )
        )


def get_range_less_than_divisor_active_status(bo, bn, po, pn):
    # x_bool = False
    # if bo <= bn and po <= pn:
    #     if (
    #         (bo >= po and bo < pn)
    #         or (bn > po and bn < pn)
    #         or (bo < po and bn > pn)
    #         or (bo == po)
    #     ):
    #         x_bool = True
    # elif bo > bn and po <= pn:
    #     if (bn > po) or (bo < pn) or (bo == po):
    #         x_bool = True
    # elif bo <= bn and po > pn:
    #     if (bo < pn) or (bn > po) or (bo == po):
    #         x_bool = True
    # elif bo > bn and po > pn:
    #     if (bn <= pn) or (bn > pn):
    #         x_bool = True
    # return x_bool
    x_bool = False
    if bo <= bn and po <= pn:
        if (
            (bo >= po and bo < pn)
            or (bn > po and bn < pn)
            or (bo < po and bn > pn)
            or (bo == po)
        ):
            x_bool = True
    elif bo > bn and po <= pn:
        if (bn > po) or (bo < pn) or (bo == po):
            x_bool = True
    elif bo <= bn:
        if (bo < pn) or (bn > po) or (bo == po):
            x_bool = True
    else:
        x_bool = True
    return x_bool


def get_collasped_beliefrange_active_status(
    premise_open: float,
    premise_nigh: float,
    premise_divisor: float,
    belief_nigh_full: float,
) -> bool:
    x_pbsd = premisestatusfinder_shop(
        premise_open=premise_open,
        premise_nigh=premise_nigh,
        premise_divisor=premise_divisor,
        belief_open_full=belief_nigh_full,
        belief_nigh_full=belief_nigh_full,
    )
    return x_pbsd.get_active_status()


def premisestatusfinder_shop(
    premise_open: float,
    premise_nigh: float,
    premise_divisor: float,
    belief_open_full: float,
    belief_nigh_full: float,
):
    x_premisestatusfinder = PremiseStatusFinder(
        premise_open, premise_nigh, premise_divisor, belief_open_full, belief_nigh_full
    )
    x_premisestatusfinder.check_attr()
    return x_premisestatusfinder


@dataclass
class PremiseUnit:
    need: RoadUnit
    open: float = None
    nigh: float = None
    divisor: int = None
    _status: bool = None
    _task: bool = None
    delimiter: str = None

    def get_obj_key(self):
        return self.need

    def get_dict(self):
        x_dict = {"need": self.need}
        if self.open != None:
            x_dict["open"] = self.open
        if self.nigh != None:
            x_dict["nigh"] = self.nigh

        if self.divisor != None:
            x_dict["divisor"] = self.divisor

        return x_dict

    def clear_status(self):
        self._status = None

    def set_delimiter(self, new_delimiter: str):
        old_delimiter = copy_deepcopy(self.delimiter)
        self.delimiter = new_delimiter
        self.need = replace_road_delimiter(
            road=self.need, old_delimiter=old_delimiter, new_delimiter=self.delimiter
        )

    def is_in_lineage(self, belief_pick: RoadUnit):
        return is_heir_road(
            src=self.need, heir=belief_pick, delimiter=self.delimiter
        ) or is_heir_road(src=belief_pick, heir=self.need, delimiter=self.delimiter)

    def set_status(self, x_beliefheir: BeliefHeir):
        self._status = self._get_active_status(beliefheir=x_beliefheir)
        self._task = self._get_task_status(beliefheir=x_beliefheir)

    def _get_active_status(self, beliefheir: BeliefHeir):
        x_status = None
        # status might be true if premise is in lineage of belief
        if beliefheir is None:
            x_status = False
        elif self.is_in_lineage(belief_pick=beliefheir.pick) == True:
            if self._is_range_or_segregate() == False:
                x_status = True
            elif self._is_range_or_segregate() and beliefheir.is_range() == False:
                x_status = False
            elif self._is_range_or_segregate() and beliefheir.is_range():
                x_status = self._get_range_segregate_status(beliefheir=beliefheir)
        elif self.is_in_lineage(belief_pick=beliefheir.pick) == False:
            x_status = False

        return x_status

    def _is_range_or_segregate(self):
        return self._is_range() or self._is_segregate()

    def _is_segregate(self):
        return self.divisor != None and self.open != None and self.nigh != None

    def _is_range(self):
        return self.divisor is None and self.open != None and self.nigh != None

    def _get_task_status(self, beliefheir: BeliefHeir) -> bool:
        x_task = None
        if self._status and self._is_range():
            x_task = beliefheir.nigh > self.nigh
        elif self._status and self._is_segregate():
            segr_obj = premisestatusfinder_shop(
                premise_open=self.open,
                premise_nigh=self.nigh,
                premise_divisor=self.divisor,
                belief_open_full=beliefheir.open,
                belief_nigh_full=beliefheir.nigh,
            )
            x_task = segr_obj.get_task_status()
        elif self._status in [True, False]:
            x_task = False

        return x_task

    def _get_range_segregate_status(self, beliefheir: BeliefHeir) -> bool:
        x_status = None
        if self._is_range():
            x_status = self._get_range_status(beliefheir=beliefheir)
        elif self._is_segregate():
            x_status = self._get_segregate_status(beliefheir=beliefheir)

        return x_status

    def _get_segregate_status(self, beliefheir: BeliefHeir) -> bool:
        segr_obj = premisestatusfinder_shop(
            premise_open=self.open,
            premise_nigh=self.nigh,
            premise_divisor=self.divisor,
            belief_open_full=beliefheir.open,
            belief_nigh_full=beliefheir.nigh,
        )
        return segr_obj.get_active_status()

    def _get_range_status(self, beliefheir: BeliefHeir) -> bool:
        return (
            (self.open <= beliefheir.open and self.nigh > beliefheir.open)
            or (self.open <= beliefheir.nigh and self.nigh > beliefheir.nigh)
            or (self.open >= beliefheir.open and self.nigh < beliefheir.nigh)
        )

    def find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        self.need = change_road(self.need, old_road, new_road)

    def meld(self, other_premise):
        if other_premise.need != self.need:
            raise InvalidReasonException(
                f"Meld fail: need={other_premise.need} is different {self.need=}"
            )
        elif other_premise.open != self.open:
            raise InvalidReasonException(
                f"Meld fail: need={other_premise.need} open={other_premise.open} is different {self.open=}"
            )
        elif other_premise.nigh != self.nigh:
            raise InvalidReasonException(
                f"Meld fail: need={other_premise.need} nigh={other_premise.nigh} is different {self.nigh=}"
            )
        elif other_premise.divisor != self.divisor:
            raise InvalidReasonException(
                f"Meld fail: need={other_premise.need} divisor={other_premise.divisor} is different {self.divisor=}"
            )

        return self


# class premisesshop:
def premiseunit_shop(
    need: RoadUnit,
    open: float = None,
    nigh: float = None,
    divisor: float = None,
    delimiter: str = None,
) -> PremiseUnit:
    return PremiseUnit(
        need=need,
        open=open,
        nigh=nigh,
        divisor=divisor,
        delimiter=default_road_delimiter_if_none(delimiter),
    )


def premises_get_from_dict(x_dict: dict) -> dict[str:PremiseUnit]:
    premises = {}
    for premise_dict in x_dict.values():
        try:
            x_open = premise_dict["open"]
        except KeyError:
            x_open = None
        try:
            x_nigh = premise_dict["nigh"]
        except KeyError:
            x_nigh = None
        try:
            x_divisor = premise_dict["divisor"]
        except KeyError:
            x_divisor = None

        premise_x = premiseunit_shop(
            need=premise_dict["need"],
            open=x_open,
            nigh=x_nigh,
            divisor=x_divisor,
        )
        premises[premise_x.need] = premise_x
    return premises


@dataclass
class ReasonCore:
    base: RoadUnit
    premises: dict[RoadUnit:PremiseUnit]
    # None: ignore,
    # True: base idea._active_status reason be True,
    # False: base idea._active_status reason be False
    suff_idea_active_status: bool = None
    delimiter: str = None

    def set_delimiter(self, new_delimiter: str):
        old_delimiter = copy_deepcopy(self.delimiter)
        self.delimiter = new_delimiter
        self.base = replace_road_delimiter(self.base, old_delimiter, new_delimiter)

        new_premises = {}
        for premise_road, premise_obj in self.premises.items():
            new_premise_road = replace_road_delimiter(
                road=premise_road,
                old_delimiter=old_delimiter,
                new_delimiter=self.delimiter,
            )
            premise_obj.set_delimiter(self.delimiter)
            new_premises[new_premise_road] = premise_obj
        self.premises = new_premises

    def get_obj_key(self):
        return self.base

    def get_premises_count(self):
        return sum(1 for _ in self.premises.values())

    def set_premise(
        self,
        premise: RoadUnit,
        open: float = None,
        nigh: float = None,
        divisor: int = None,
    ):
        self.premises[premise] = premiseunit_shop(
            need=premise,
            open=open,
            nigh=nigh,
            divisor=divisor,
            delimiter=self.delimiter,
        )

    def get_premise(self, premise: RoadUnit) -> PremiseUnit:
        return self.premises.get(premise)

    def del_premise(self, premise: RoadUnit):
        try:
            self.premises.pop(premise)
        except KeyError as e:
            raise InvalidReasonException(f"Reason unable to delete premise {e}") from e

    def find_replace_road(self, old_road: RoadUnit, new_road: RoadUnit):
        self.base = change_road(self.base, old_road, new_road)
        self.premises = find_replace_road_key_dict(
            dict_x=self.premises, old_road=old_road, new_road=new_road
        )

    def meld(self, other_reason):
        for premise_x in other_reason.premises.values():
            if self.premises.get(premise_x.need) is None:
                self.premises[premise_x.need] = premise_x
            else:
                self.premises.get(premise_x.need).meld(premise_x)
        if other_reason.base != self.base:
            raise InvalidReasonException(
                f"Meld fail: reason={other_reason.base} is different {self.base=}"
            )

        # TODO get rid of this return self
        return self


def reasoncore_shop(
    base: RoadUnit,
    premises: dict[RoadUnit:PremiseUnit] = None,
    suff_idea_active_status: bool = None,
    delimiter: str = None,
):
    return ReasonCore(
        base=base,
        premises=get_empty_dict_if_none(premises),
        suff_idea_active_status=suff_idea_active_status,
        delimiter=default_road_delimiter_if_none(delimiter),
    )


@dataclass
class ReasonUnit(ReasonCore):
    def get_dict(self):
        premises_dict = {
            premise_road: premise.get_dict()
            for premise_road, premise in self.premises.items()
        }
        return {
            "base": self.base,
            "premises": premises_dict,
        }


def reasonunit_shop(
    base: RoadUnit,
    premises: dict[RoadUnit:PremiseUnit] = None,
    suff_idea_active_status: bool = None,
    delimiter: str = None,
):
    return ReasonUnit(
        base=base,
        premises=get_empty_dict_if_none(premises),
        suff_idea_active_status=suff_idea_active_status,
        delimiter=default_road_delimiter_if_none(delimiter),
    )


@dataclass
class ReasonHeir(ReasonCore):
    _status: bool = None
    _task: bool = None
    _curr_idea_active_status: bool = None

    def inherit_from_reasonheir(self, x_reasonunit: ReasonUnit):
        x_premises = {}
        for w in x_reasonunit.premises.values():
            premise_x = premiseunit_shop(
                need=w.need,
                open=w.open,
                nigh=w.nigh,
                divisor=w.divisor,
            )
            x_premises[premise_x.need] = premise_x
        self.premises = x_premises

    def clear_status(self):
        self._status = None
        for premise in self.premises.values():
            premise.clear_status()

    def _set_premise_status(self, beliefheir: BeliefHeir):
        for premise in self.premises.values():
            premise.set_status(x_beliefheir=beliefheir)

    def _get_base_belief(self, beliefs: dict[RoadUnit:BeliefHeir]) -> BeliefHeir:
        x_belief = None
        if beliefs is None:
            beliefs = {}

        for belief in beliefs.values():
            if self.base == belief.base:
                x_belief = belief

        return x_belief

    def set_curr_idea_active_status(self, bool_x: bool):
        self._curr_idea_active_status = bool_x

    def set_status(self, beliefs: dict[RoadUnit:BeliefHeir]):
        self.clear_status()
        belief = self._get_base_belief(beliefs=beliefs)
        self._set_premise_status(beliefheir=belief)

        # if a single one is true return true (OR operator)
        is_a_single_premise_true = False
        is_single_task_true = False
        for premise in self.premises.values():
            if premise._status == True:
                is_a_single_premise_true = True
                if premise._task == True:
                    is_single_task_true = True

        # reasonheir object status is set by either
        self._status = bool(
            is_a_single_premise_true
            or (
                self._curr_idea_active_status != None
                and self._curr_idea_active_status == self.suff_idea_active_status
            )
        )
        self._task = True if is_single_task_true else None
        if self._status and self._task is None:
            self._task = False


def reasonheir_shop(
    base: RoadUnit,
    premises: dict[RoadUnit:PremiseUnit] = None,
    suff_idea_active_status: bool = None,
    _status: bool = None,
    _task: bool = None,
    _curr_idea_active_status: bool = None,
    delimiter: str = None,
):
    return ReasonHeir(
        base=base,
        premises=get_empty_dict_if_none(premises),
        suff_idea_active_status=suff_idea_active_status,
        _status=_status,
        _task=_task,
        _curr_idea_active_status=_curr_idea_active_status,
        delimiter=default_road_delimiter_if_none(delimiter),
    )


# class Reasonsshop:
def reasons_get_from_dict(reasons_dict: dict) -> dict[ReasonUnit]:
    reasons = {}
    for reason_dict in reasons_dict.values():
        x_reason = reasonunit_shop(
            base=reason_dict["base"],
            premises=premises_get_from_dict(x_dict=reason_dict["premises"]),
        )
        reasons[x_reason.base] = x_reason
    return reasons
