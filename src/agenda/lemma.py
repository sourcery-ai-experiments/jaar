from src._instrument.python import get_empty_dict_if_none
from src.agenda.reason_oath import BeliefUnit, RoadUnit, beliefunit_shop
from src.agenda.oath import OathUnit
from dataclasses import dataclass


class InvalidLemmaException(Exception):
    pass


@dataclass
class Lemma:
    src_belief: BeliefUnit
    calc_belief: BeliefUnit
    x_oath: OathUnit
    eval_status: bool
    eval_count: int


@dataclass
class Lemmas:
    lemmas: dict[RoadUnit:Lemma] = None

    def _get_loop_range_calc_belief_attr(
        self,
        oath_begin: float,
        oath_close: float,
        src_open: float,
        src_nigh: float,
        src_oath_begin: float,
        src_oath_close: float,
    ) -> RoadUnit:
        belief_open = None
        belief_nigh = None

        # if src_oath and belief_oath have same range return same src belief range
        if oath_begin == src_oath_begin and oath_close == src_oath_close:
            belief_open = src_open
            belief_nigh = src_nigh
        else:
            # create both ranges and get calc ranges for both. Return the not null one
            r1_open, r1_nigh = self._get_range_calc_belief_attr(
                oath_begin=oath_begin,
                oath_close=oath_close,
                src_open=src_oath_begin,
                src_nigh=src_nigh,
            )
            r2_open, r2_nigh = self._get_range_calc_belief_attr(
                oath_begin=oath_begin,
                oath_close=oath_close,
                src_open=src_open,
                src_nigh=src_oath_close,
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
        oath_begin,
        oath_close,
        src_open,
        src_nigh,
    ) -> set[float, float]:
        belief_open = None
        belief_nigh = None
        if src_open <= oath_begin and src_nigh >= oath_close:
            # if parent range contains all oath range
            belief_open = oath_begin
            belief_nigh = oath_close
        elif src_open >= oath_begin and src_nigh < oath_close:
            # if parent range exists inside oath range
            belief_open = src_open
            belief_nigh = src_nigh
        elif src_open >= oath_begin and src_open < oath_close and src_nigh > oath_close:
            # if parent range begins inside oath range and ends outside oath range
            belief_open = src_open
            belief_nigh = oath_close
        elif src_open <= oath_begin and src_nigh > oath_begin:
            belief_open = oath_begin
            belief_nigh = src_nigh
        # if src_open <= oath_begin and src_nigh >= oath_close:
        #     # if parent range contains all oath range
        #     belief_open = oath_begin
        #     belief_nigh = oath_close
        # elif src_open >= oath_begin and src_nigh < oath_close:
        #     # if parent range exists inside oath range
        #     belief_open = src_open
        #     belief_nigh = src_nigh
        # elif src_open >= oath_begin and src_open < oath_close and src_nigh > oath_close:
        #     # if parent range begins inside oath range and ends outside oath range
        #     belief_open = src_open
        #     belief_nigh = oath_close
        # elif (
        #     # if parent range begins outside oath range and ends inside oath range
        #     src_open <= oath_begin
        #     and src_nigh > oath_begin
        #     and src_nigh < oath_close
        # ):
        #     belief_open = oath_begin
        #     belief_nigh = src_nigh

        return belief_open, belief_nigh

    def _get_multipler_calc_belief_attr(
        self,
        oath_begin,
        oath_close,
        oath_numor,
        oath_denom,
        src_open,
        src_nigh,
    ) -> set[float, float]:
        return self._get_range_calc_belief_attr(
            oath_begin=oath_begin,
            oath_close=oath_close,
            src_open=src_open * oath_numor / oath_denom,
            src_nigh=src_nigh * oath_numor / oath_denom,
        )

    def _get_remainder_calc_belief_attr(
        self,
        oath_begin,
        oath_close,
        src_open,
        src_nigh,
    ):
        belief_open = None
        belief_nigh = None

        if src_nigh - src_open >= oath_close:  # - oath_begin:
            belief_open = oath_begin
            belief_nigh = oath_close
        else:
            belief_open = src_open % oath_close
            belief_nigh = src_nigh % oath_close

        return belief_open, belief_nigh

    def _create_new_belief(
        self, x_oath: OathUnit, src_belief: BeliefUnit, src_oath: OathUnit
    ) -> BeliefUnit:
        if x_oath._begin is None or x_oath._close is None:
            raise InvalidLemmaException(f"Oath {x_oath.get_road()} does not have range")

        oath_begin = x_oath._begin
        oath_close = x_oath._close
        oath_numor = x_oath._numor
        oath_denom = x_oath._denom
        oath_reest = x_oath._reest
        src_open = src_belief.open
        src_nigh = src_belief.nigh
        src_oath_begin = src_oath._begin
        src_oath_close = src_oath._close
        oath_road = x_oath.get_road()

        belief_open = None
        belief_nigh = None

        if src_open is None and src_nigh is None:
            belief_open = None
            belief_nigh = None
        elif (oath_numor is None or oath_denom is None) and src_open > src_nigh:
            belief_open, belief_nigh = self._get_loop_range_calc_belief_attr(
                oath_begin=oath_begin,
                oath_close=oath_close,
                src_open=src_open,
                src_nigh=src_nigh,
                src_oath_begin=src_oath_begin,
                src_oath_close=src_oath_close,
            )

        elif oath_numor is None or oath_denom is None:
            belief_open, belief_nigh = self._get_range_calc_belief_attr(
                oath_begin=oath_begin,
                oath_close=oath_close,
                src_open=src_open,
                src_nigh=src_nigh,
            )
        elif oath_numor != None and oath_denom != None and oath_reest in (False, None):
            belief_open, belief_nigh = self._get_multipler_calc_belief_attr(
                oath_begin=oath_begin,
                oath_close=oath_close,
                oath_numor=oath_numor,
                oath_denom=oath_denom,
                src_open=src_open,
                src_nigh=src_nigh,
            )
        elif oath_numor != None and oath_denom != None and oath_reest == True:
            belief_open, belief_nigh = self._get_remainder_calc_belief_attr(
                oath_begin=oath_begin,
                oath_close=oath_close,
                src_open=src_open,
                src_nigh=src_nigh,
            )

        active = belief_open is not None and belief_nigh is not None
        return beliefunit_shop(
            base=oath_road,
            pick=oath_road,
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

    # def _add_lemma_oath(
    def eval(self, x_oath: OathUnit, src_belief: BeliefUnit, src_oath: OathUnit):
        new_belief = self._create_new_belief(
            x_oath=x_oath, src_belief=src_belief, src_oath=src_oath
        )
        road_x = x_oath.get_road()
        if self.lemmas.get(road_x) is None:
            self.lemmas[road_x] = Lemma(
                src_belief=src_belief,
                calc_belief=new_belief,
                x_oath=x_oath,
                eval_status=False,
                eval_count=1,
            )


def lemmas_shop(lemmas: dict[RoadUnit:Lemma] = None, delimiter: str = None) -> Lemmas:
    return Lemmas(lemmas=get_empty_dict_if_none(lemmas))
