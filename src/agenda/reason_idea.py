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
class FactCore:
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

    def meld(self, other_factcore, same_reason: bool = False):
        if same_reason and other_factcore.base != self.base:
            raise InvalidReasonException(
                f"Meld fail: base={other_factcore.base} is different {self.base=}"
            )
        elif same_reason and other_factcore.pick != self.pick:
            raise InvalidReasonException(
                f"Meld fail: pick={other_factcore.pick} is different {self.pick=}"
            )
        elif same_reason and other_factcore.open != self.open:
            raise InvalidReasonException(
                f"Meld fail: base={other_factcore.base} open={other_factcore.open} is different {self.open=}"
            )
        elif same_reason and other_factcore.nigh != self.nigh:
            raise InvalidReasonException(
                f"Meld fail: base={other_factcore.base} nigh={other_factcore.nigh} is different {self.nigh=}"
            )
        else:
            self.base = other_factcore.base
            self.pick = other_factcore.pick
            self.open = other_factcore.open
            self.nigh = other_factcore.nigh
        return self


@dataclass
class FactUnit(FactCore):
    pass


# class FactUnitsshop:
def factunits_get_from_dict(x_dict: dict):
    facts = {}
    for fact_dict in x_dict.values():
        x_base = fact_dict["base"]
        x_pick = fact_dict["pick"]

        try:
            x_open = fact_dict["open"]
        except KeyError:
            x_open = None
        try:
            x_nigh = fact_dict["nigh"]
        except KeyError:
            x_nigh = None

        x_fact = factunit_shop(
            base=x_base,
            pick=x_pick,
            open=x_open,
            nigh=x_nigh,
        )

        facts[x_fact.base] = x_fact
    return facts


def factunit_shop(
    base: RoadUnit = None, pick: RoadUnit = None, open: float = None, nigh: float = None
) -> FactUnit:
    return FactUnit(base=base, pick=pick, open=open, nigh=nigh)


@dataclass
class FactHeir(FactCore):
    def transform(self, factunit: FactUnit):
        if (
            (self.open != None and factunit.open != None and self.nigh != None)
            and self.open <= factunit.open
            and self.nigh >= factunit.open
        ):
            self.open = factunit.open

    def is_range(self):
        return self.open != None and self.nigh != None


def factheir_shop(
    base: RoadUnit = None, pick: RoadUnit = None, open: float = None, nigh: float = None
) -> FactHeir:
    return FactHeir(base=base, pick=pick, open=open, nigh=nigh)


@dataclass
class PremiseStatusFinder:
    fact_open: float
    fact_nigh: float
    premise_open: float
    premise_nigh: float
    premise_divisor: int
    _active_status: bool = None
    _task_status: bool = None
    _in_range_count: int = None

    def __post_init__(self):
        self._active_status = False
        self._task_status = False

        self._fact_range_len = None
        if self.fact_nigh >= self.fact_open:
            self._fact_range_len = self.fact_nigh - self.fact_open

        # create transformed premise_open and premise_nigh that can be compared to facts
        open_multipler = int(self.fact_open / self.premise_divisor)
        nigh_multipler = int(self.fact_nigh / self.premise_divisor)
        self.premise_open_trans = (
            self.premise_divisor * open_multipler
        ) + self.premise_open
        self.premise_nigh_trans = (
            self.premise_divisor * nigh_multipler
        ) + self.premise_nigh

        if (
            self.premise_nigh_trans_in_fact_range()
            or self.premise_open_trans_equal_fact_open()
            # or self.fact_range_len_is_greater_than_divisor()
            or self.premise_x_range_inside_fact_range()
            or self.fact_range_inside_premise_x_range()
            or self.premise_open_trans_in_fact_range()
        ):
            self._active_status = True

            if self.fact_nigh_mod_div_outside_need_range():
                self._task_status = True

        # no features use this
        self._in_range_count = None

    def fact_range_len_is_greater_than_divisor(self) -> bool:
        return self._fact_range_len >= self.premise_divisor

    def get_fact_open_mod_div(self):
        return self.fact_open % self.premise_divisor

    def get_fact_nigh_mod_div(self):
        return self.fact_nigh % self.premise_divisor

    def fact_nigh_mod_div_outside_need_range(self) -> bool:
        return (
            self.get_fact_nigh_mod_div() < self.premise_open
            or self.get_fact_nigh_mod_div() >= self.premise_nigh
        )

    def premise_nigh_trans_in_fact_range(self) -> bool:
        return (
            self.premise_open_trans < self.fact_open
            and self.premise_nigh_trans >= self.fact_open
            and self.premise_nigh_trans < self.fact_nigh
        )

    def premise_open_trans_equal_fact_open(self) -> bool:
        return self.premise_open_trans == self.fact_open

    def premise_x_range_inside_fact_range(self) -> bool:
        return (
            self.premise_open_trans > self.fact_open
            and self.premise_nigh_trans < self.fact_nigh
        )

    def fact_range_inside_premise_x_range(self) -> bool:
        return (
            self.premise_open_trans <= self.fact_open
            and self.premise_nigh_trans > self.fact_nigh
        )

    def premise_open_trans_in_fact_range(self) -> bool:
        return (
            self.premise_open_trans > self.fact_open
            and self.premise_open_trans < self.fact_nigh
            and self.premise_nigh_trans > self.fact_nigh
        )


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

    def is_in_lineage(self, fact_pick: RoadUnit):
        return is_heir_road(
            src=self.need, heir=fact_pick, delimiter=self.delimiter
        ) or is_heir_road(src=fact_pick, heir=self.need, delimiter=self.delimiter)

    def set_status(self, factheir: FactHeir):
        self._status = self._get_active_status(factheir=factheir)
        self._task = self._get_task_status(factheir=factheir)

    def _get_active_status(self, factheir: FactHeir):
        x_status = None
        # status might be true if premise is in lineage of fact
        if factheir is None:
            x_status = False
        elif self.is_in_lineage(fact_pick=factheir.pick) == True:
            if self._is_range_or_segregate() == False:
                x_status = True
            elif self._is_range_or_segregate() and factheir.is_range() == False:
                x_status = False
            elif self._is_range_or_segregate() and factheir.is_range() == True:
                x_status = self._get_range_segregate_status(factheir=factheir)
        elif self.is_in_lineage(fact_pick=factheir.pick) == False:
            x_status = False

        return x_status

    def _is_range_or_segregate(self):
        return self._is_range() or self._is_segregate()

    def _is_segregate(self):
        return self.divisor != None and self.open != None and self.nigh != None

    def _is_range(self):
        return self.divisor is None and self.open != None and self.nigh != None

    def _get_task_status(self, factheir: FactHeir) -> bool:
        x_task = None
        if self._status and self._is_range():
            x_task = factheir.nigh > self.nigh
        elif self._status and self._is_segregate():
            segr_obj = PremiseStatusFinder(
                fact_open=factheir.open,
                fact_nigh=factheir.nigh,
                premise_open=self.open,
                premise_nigh=self.nigh,
                premise_divisor=self.divisor,
            )
            x_task = segr_obj._task_status
        elif self._status in [True, False]:
            x_task = False

        return x_task

    def _get_range_segregate_status(self, factheir: FactHeir) -> bool:
        x_status = None
        if self._is_range():
            x_status = self._get_range_status(factheir=factheir)
        elif self._is_segregate():
            x_status = self._get_segregate_status(factheir=factheir)

        return x_status

    def _get_segregate_status(self, factheir: FactHeir) -> bool:
        segr_obj = PremiseStatusFinder(
            fact_open=factheir.open,
            fact_nigh=factheir.nigh,
            premise_open=self.open,
            premise_nigh=self.nigh,
            premise_divisor=self.divisor,
        )
        return segr_obj._active_status

    def _get_range_status(self, factheir: FactHeir) -> bool:
        return (
            (self.open <= factheir.open and self.nigh > factheir.open)
            or (self.open <= factheir.nigh and self.nigh > factheir.nigh)
            or (self.open >= factheir.open and self.nigh < factheir.nigh)
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

    def _set_premise_status(self, factheir: FactHeir):
        for premise in self.premises.values():
            premise.set_status(factheir=factheir)

    def _get_base_fact(self, facts: dict[RoadUnit:FactHeir]):
        x_fact = None
        if facts is None:
            facts = {}

        for fact in facts.values():
            if self.base == fact.base:
                x_fact = fact

        return x_fact

    def set_curr_idea_active_status(self, bool_x: bool):
        self._curr_idea_active_status = bool_x

    def set_status(self, facts: dict[RoadUnit:FactHeir]):
        self.clear_status()
        fact = self._get_base_fact(facts=facts)
        self._set_premise_status(factheir=fact)

        # if a single one is true return true (OR operator)
        is_single_premise_true = False
        is_single_task_true = False
        for premise in self.premises.values():
            if premise._status == True:
                is_single_premise_true = True
                if premise._task == True:
                    is_single_task_true = True

        self._status = bool(
            is_single_premise_true
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
