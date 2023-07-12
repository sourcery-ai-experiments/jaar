from dataclasses import dataclass
from lib.agent.required import AcptFactUnit, Road, acptfactunit_shop
from lib.agent.idea import IdeaKid


@dataclass
class Lemma:
    src_acptfact: AcptFactUnit
    calc_acptfact: AcptFactUnit
    idea_x: IdeaKid
    eval_status: bool
    eval_count: int


@dataclass
class Lemmas:
    lemmas: dict[Road:Lemma] = None

    def set_empty_if_null(self):
        if self.lemmas is None:
            self.lemmas = {}

    def _get_loop_range_calc_acptfact_attr(
        self,
        idea_begin: float,
        idea_close: float,
        src_open: float,
        src_nigh: float,
        src_idea_begin: float,
        src_idea_close: float,
    ):
        acptfact_open = None
        acptfact_nigh = None

        # if src_idea and acptfact_idea have same range return same src acptfact range
        if idea_begin == src_idea_begin and idea_close == src_idea_close:
            acptfact_open = src_open
            acptfact_nigh = src_nigh
        else:
            # create both ranges and get calc ranges for both. Return the not null one
            r1_open, r1_nigh = self._get_range_calc_acptfact_attr(
                idea_begin=idea_begin,
                idea_close=idea_close,
                src_open=src_idea_begin,
                src_nigh=src_nigh,
            )
            r2_open, r2_nigh = self._get_range_calc_acptfact_attr(
                idea_begin=idea_begin,
                idea_close=idea_close,
                src_open=src_open,
                src_nigh=src_idea_close,
            )
            # # if both are not null return r1_nigh as acptfact_open and r2_open as acptfact_nigh
            # if r1_open != None and r1_nigh != None and r2_open != None and r2_nigh != None:
            #     acptfact_open = r1_nigh
            #     acptfact_nigh = r2_open
            if r1_open != None and r1_nigh != None:
                acptfact_open = r1_open
                acptfact_nigh = r1_nigh
            elif r2_open != None and r2_nigh != None:
                acptfact_open = r2_open
                acptfact_nigh = r2_nigh

        return acptfact_open, acptfact_nigh

    def _get_range_calc_acptfact_attr(
        self,
        idea_begin,
        idea_close,
        src_open,
        src_nigh,
    ):
        acptfact_open = None
        acptfact_nigh = None
        if src_open <= idea_begin and src_nigh >= idea_close:
            # if parent range contains all idea range
            acptfact_open = idea_begin
            acptfact_nigh = idea_close
        elif src_open >= idea_begin and src_nigh < idea_close:
            # if parent range exists inside idea range
            acptfact_open = src_open
            acptfact_nigh = src_nigh
        elif src_open >= idea_begin and src_open < idea_close and src_nigh > idea_close:
            # if parent range begins inside idea range and ends outside idea range
            acptfact_open = src_open
            acptfact_nigh = idea_close
        elif (
            # if parent range begins outside idea range and ends inside idea range
            src_open <= idea_begin
            and src_nigh > idea_begin
            and src_nigh < idea_close
        ):
            acptfact_open = idea_begin
            acptfact_nigh = src_nigh

        return acptfact_open, acptfact_nigh

    def _get_multipler_calc_acptfact_attr(
        self,
        idea_begin,
        idea_close,
        idea_numor,
        idea_denom,
        src_open,
        src_nigh,
    ):
        return self._get_range_calc_acptfact_attr(
            idea_begin=idea_begin,
            idea_close=idea_close,
            src_open=src_open * idea_numor / idea_denom,
            src_nigh=src_nigh * idea_numor / idea_denom,
        )

    def _get_remainder_calc_acptfact_attr(
        self,
        idea_begin,
        idea_close,
        src_open,
        src_nigh,
    ):
        acptfact_open = None
        acptfact_nigh = None

        if src_nigh - src_open >= idea_close:  # - idea_begin:
            acptfact_open = idea_begin
            acptfact_nigh = idea_close
        else:
            acptfact_open = src_open % idea_close
            acptfact_nigh = src_nigh % idea_close

        return acptfact_open, acptfact_nigh

    def _create_new_acptfact(
        self, idea_x: IdeaKid, src_acptfact: AcptFactUnit, src_idea: IdeaKid
    ) -> AcptFactUnit:
        if idea_x._begin is None or idea_x._close is None:
            raise Exception(f"Idea {idea_x._walk},{idea_x._desc} does not have range")

        idea_begin = idea_x._begin
        idea_close = idea_x._close
        idea_numor = idea_x._numor
        idea_denom = idea_x._denom
        idea_reest = idea_x._reest
        src_open = src_acptfact.open
        src_nigh = src_acptfact.nigh
        src_idea_begin = src_idea._begin
        src_idea_close = src_idea._close
        idea_road = f"{idea_x._walk},{idea_x._desc}"

        acptfact_open = None
        acptfact_nigh = None

        if src_open is None and src_nigh is None:
            acptfact_open = None
            acptfact_nigh = None
        elif (idea_numor is None or idea_denom is None) and src_open > src_nigh:
            acptfact_open, acptfact_nigh = self._get_loop_range_calc_acptfact_attr(
                idea_begin=idea_begin,
                idea_close=idea_close,
                src_open=src_open,
                src_nigh=src_nigh,
                src_idea_begin=src_idea_begin,
                src_idea_close=src_idea_close,
            )

        elif idea_numor is None or idea_denom is None:
            acptfact_open, acptfact_nigh = self._get_range_calc_acptfact_attr(
                idea_begin=idea_begin,
                idea_close=idea_close,
                src_open=src_open,
                src_nigh=src_nigh,
            )
        elif idea_numor != None and idea_denom != None and idea_reest in (False, None):
            acptfact_open, acptfact_nigh = self._get_multipler_calc_acptfact_attr(
                idea_begin=idea_begin,
                idea_close=idea_close,
                idea_numor=idea_numor,
                idea_denom=idea_denom,
                src_open=src_open,
                src_nigh=src_nigh,
            )
        elif idea_numor != None and idea_denom != None and idea_reest == True:
            acptfact_open, acptfact_nigh = self._get_remainder_calc_acptfact_attr(
                idea_begin=idea_begin,
                idea_close=idea_close,
                src_open=src_open,
                src_nigh=src_nigh,
            )

        active_status = False
        if acptfact_open is not None and acptfact_nigh is not None:
            active_status = True

        return acptfactunit_shop(
            base=idea_road,
            pick=idea_road,
            open=acptfact_open,
            nigh=acptfact_nigh,
        )

    def is_lemmas_evaluated(self):
        return sum(lemma.eval_status == True for lemma in self.lemmas.values()) == len(
            self.lemmas
        )

    def get_unevaluated_lemma(self):
        for lemma in self.lemmas.values():
            if lemma.eval_status == False:
                # set to True
                lemma.eval_status = True
                return lemma

    # def _add_lemma_idea(
    def eval(self, idea_x: IdeaKid, src_acptfact: AcptFactUnit, src_idea: IdeaKid):
        new_acptfact = self._create_new_acptfact(
            idea_x=idea_x, src_acptfact=src_acptfact, src_idea=src_idea
        )
        road_x = f"{idea_x._walk},{idea_x._desc}"
        if self.lemmas.get(road_x) is None:
            self.lemmas[road_x] = Lemma(
                src_acptfact=src_acptfact,
                calc_acptfact=new_acptfact,
                idea_x=idea_x,
                eval_status=False,
                eval_count=1,
            )
        else:
            # if new acptfactunit is inactive (acptfact.open == None and acptfact.nigh == None)
            # or current lemma acptfactunit acptfact.open == idea._being and acptfact.acptfact == idea._close
            # do nothing
            pass
            # current_lemma_acptfact = lemma_dict.get(road_x)[1]
            # if (
            #     acptfact_open != None
            #     and acptfact_nigh != None
            #     and (
            #         current_lemma_acptfact.open != acptfact_open
            #         or current_lemma_acptfact.nigh != acptfact_nigh
            #     )
            # ):
            #     prin(f"{current_lemma_acptfact=} {acptfact_open=} {acptfact_nigh=}")

            # if current_lemma_acptfact.base == "src,time,week":
            #     prin(f"{current_lemma_acptfact=} {acptfact_open=} {acptfact_nigh=}")
