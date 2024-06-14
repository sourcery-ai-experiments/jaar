from src._instrument.python import get_empty_dict_if_none
from src.agenda.reason_fact import BeliefUnit, RoadUnit, beliefunit_shop
from src.agenda.fact import FactUnit
from dataclasses import dataclass


class InvalidLemmaException(Exception):
    pass


@dataclass
class Lemma:
    src_belief: BeliefUnit
    calc_belief: BeliefUnit
    x_fact: FactUnit
    eval_status: bool
    eval_count: int


@dataclass
class Lemmas:
    lemmas: dict[RoadUnit:Lemma] = None

    def _get_loop_range_calc_belief_attr(
        self,
        fact_begin: float,
        fact_close: float,
        src_open: float,
        src_nigh: float,
        src_fact_begin: float,
        src_fact_close: float,
    ) -> RoadUnit:
        belief_open = None
        belief_nigh = None

        # if src_fact and belief_fact have same range return same src belief range
        if fact_begin == src_fact_begin and fact_close == src_fact_close:
            belief_open = src_open
            belief_nigh = src_nigh
        else:
            # create both ranges and get calc ranges for both. Return the not null one
            r1_open, r1_nigh = self._get_range_calc_belief_attr(
                fact_begin=fact_begin,
                fact_close=fact_close,
                src_open=src_fact_begin,
                src_nigh=src_nigh,
            )
            r2_open, r2_nigh = self._get_range_calc_belief_attr(
                fact_begin=fact_begin,
                fact_close=fact_close,
                src_open=src_open,
                src_nigh=src_fact_close,
            )
            # # if both are not null return r1_nigh as belief_open and r2_open as belief_nigh
            # if r1_open != None and r1_nigh != None and r2_open != None and r2_nigh != None:
            #     belief_open = r1_nigh
            #     belief_nigh = r2_open
            if r1_open != None and r1_nigh != None:
                belief_open = r1_open
                belief_nigh = r1_nigh
            elif r2_open != None and r2_nigh != None:
                belief_open = r2_open
                belief_nigh = r2_nigh

        return belief_open, belief_nigh

    def _get_range_calc_belief_attr(
        self,
        fact_begin,
        fact_close,
        src_open,
        src_nigh,
    ) -> set[float, float]:
        belief_open = None
        belief_nigh = None
        if src_open <= fact_begin and src_nigh >= fact_close:
            # if parent range contains all fact range
            belief_open = fact_begin
            belief_nigh = fact_close
        elif src_open >= fact_begin and src_nigh < fact_close:
            # if parent range exists inside fact range
            belief_open = src_open
            belief_nigh = src_nigh
        elif src_open >= fact_begin and src_open < fact_close and src_nigh > fact_close:
            # if parent range begins inside fact range and ends outside fact range
            belief_open = src_open
            belief_nigh = fact_close
        elif src_open <= fact_begin and src_nigh > fact_begin:
            belief_open = fact_begin
            belief_nigh = src_nigh
        # if src_open <= fact_begin and src_nigh >= fact_close:
        #     # if parent range contains all fact range
        #     belief_open = fact_begin
        #     belief_nigh = fact_close
        # elif src_open >= fact_begin and src_nigh < fact_close:
        #     # if parent range exists inside fact range
        #     belief_open = src_open
        #     belief_nigh = src_nigh
        # elif src_open >= fact_begin and src_open < fact_close and src_nigh > fact_close:
        #     # if parent range begins inside fact range and ends outside fact range
        #     belief_open = src_open
        #     belief_nigh = fact_close
        # elif (
        #     # if parent range begins outside fact range and ends inside fact range
        #     src_open <= fact_begin
        #     and src_nigh > fact_begin
        #     and src_nigh < fact_close
        # ):
        #     belief_open = fact_begin
        #     belief_nigh = src_nigh

        return belief_open, belief_nigh

    def _get_multipler_calc_belief_attr(
        self,
        fact_begin,
        fact_close,
        fact_numor,
        fact_denom,
        src_open,
        src_nigh,
    ) -> set[float, float]:
        return self._get_range_calc_belief_attr(
            fact_begin=fact_begin,
            fact_close=fact_close,
            src_open=src_open * fact_numor / fact_denom,
            src_nigh=src_nigh * fact_numor / fact_denom,
        )

    def _get_remainder_calc_belief_attr(
        self,
        fact_begin,
        fact_close,
        src_open,
        src_nigh,
    ):
        belief_open = None
        belief_nigh = None

        if src_nigh - src_open >= fact_close:  # - fact_begin:
            belief_open = fact_begin
            belief_nigh = fact_close
        else:
            belief_open = src_open % fact_close
            belief_nigh = src_nigh % fact_close

        return belief_open, belief_nigh

    def _create_new_belief(
        self, x_fact: FactUnit, src_belief: BeliefUnit, src_fact: FactUnit
    ) -> BeliefUnit:
        if x_fact._begin is None or x_fact._close is None:
            raise InvalidLemmaException(f"Fact {x_fact.get_road()} does not have range")

        fact_begin = x_fact._begin
        fact_close = x_fact._close
        fact_numor = x_fact._numor
        fact_denom = x_fact._denom
        fact_reest = x_fact._reest
        src_open = src_belief.open
        src_nigh = src_belief.nigh
        src_fact_begin = src_fact._begin
        src_fact_close = src_fact._close
        fact_road = x_fact.get_road()

        belief_open = None
        belief_nigh = None

        if src_open is None and src_nigh is None:
            belief_open = None
            belief_nigh = None
        elif (fact_numor is None or fact_denom is None) and src_open > src_nigh:
            belief_open, belief_nigh = self._get_loop_range_calc_belief_attr(
                fact_begin=fact_begin,
                fact_close=fact_close,
                src_open=src_open,
                src_nigh=src_nigh,
                src_fact_begin=src_fact_begin,
                src_fact_close=src_fact_close,
            )

        elif fact_numor is None or fact_denom is None:
            belief_open, belief_nigh = self._get_range_calc_belief_attr(
                fact_begin=fact_begin,
                fact_close=fact_close,
                src_open=src_open,
                src_nigh=src_nigh,
            )
        elif fact_numor != None and fact_denom != None and fact_reest in (False, None):
            belief_open, belief_nigh = self._get_multipler_calc_belief_attr(
                fact_begin=fact_begin,
                fact_close=fact_close,
                fact_numor=fact_numor,
                fact_denom=fact_denom,
                src_open=src_open,
                src_nigh=src_nigh,
            )
        elif fact_numor != None and fact_denom != None and fact_reest == True:
            belief_open, belief_nigh = self._get_remainder_calc_belief_attr(
                fact_begin=fact_begin,
                fact_close=fact_close,
                src_open=src_open,
                src_nigh=src_nigh,
            )

        active = belief_open is not None and belief_nigh is not None
        return beliefunit_shop(
            base=fact_road,
            pick=fact_road,
            open=belief_open,
            nigh=belief_nigh,
        )

    def is_lemmas_evaluated(self) -> bool:
        return sum(lemma.eval_status == True for lemma in self.lemmas.values()) == len(
            self.lemmas
        )

    def get_unevaluated_lemma(self) -> Lemma:
        for lemma in self.lemmas.values():
            if lemma.eval_status is False:
                # set to True
                lemma.eval_status = True
                return lemma

    # def _add_lemma_fact(
    def eval(self, x_fact: FactUnit, src_belief: BeliefUnit, src_fact: FactUnit):
        new_belief = self._create_new_belief(
            x_fact=x_fact, src_belief=src_belief, src_fact=src_fact
        )
        road_x = x_fact.get_road()
        if self.lemmas.get(road_x) is None:
            self.lemmas[road_x] = Lemma(
                src_belief=src_belief,
                calc_belief=new_belief,
                x_fact=x_fact,
                eval_status=False,
                eval_count=1,
            )


def lemmas_shop(lemmas: dict[RoadUnit:Lemma] = None, delimiter: str = None) -> Lemmas:
    return Lemmas(lemmas=get_empty_dict_if_none(lemmas))
