from dataclasses import dataclass
from src.agent.required import AcptFactUnit, Road, acptfactunit_shop
from src.agent.tool import ToolKid


class InvalidLemmaException(Exception):
    pass


@dataclass
class Lemma:
    src_acptfact: AcptFactUnit
    calc_acptfact: AcptFactUnit
    tool_x: ToolKid
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
        tool_begin: float,
        tool_close: float,
        src_open: float,
        src_nigh: float,
        src_tool_begin: float,
        src_tool_close: float,
    ):
        acptfact_open = None
        acptfact_nigh = None

        # if src_tool and acptfact_tool have same range return same src acptfact range
        if tool_begin == src_tool_begin and tool_close == src_tool_close:
            acptfact_open = src_open
            acptfact_nigh = src_nigh
        else:
            # create both ranges and get calc ranges for both. Return the not null one
            r1_open, r1_nigh = self._get_range_calc_acptfact_attr(
                tool_begin=tool_begin,
                tool_close=tool_close,
                src_open=src_tool_begin,
                src_nigh=src_nigh,
            )
            r2_open, r2_nigh = self._get_range_calc_acptfact_attr(
                tool_begin=tool_begin,
                tool_close=tool_close,
                src_open=src_open,
                src_nigh=src_tool_close,
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
        tool_begin,
        tool_close,
        src_open,
        src_nigh,
    ):  # sourcery skip: remove-redundant-if
        acptfact_open = None
        acptfact_nigh = None
        if src_open <= tool_begin and src_nigh >= tool_close:
            # if parent range contains all tool range
            acptfact_open = tool_begin
            acptfact_nigh = tool_close
        elif src_open >= tool_begin and src_nigh < tool_close:
            # if parent range exists inside tool range
            acptfact_open = src_open
            acptfact_nigh = src_nigh
        elif src_open >= tool_begin and src_open < tool_close and src_nigh > tool_close:
            # if parent range begins inside tool range and ends outside tool range
            acptfact_open = src_open
            acptfact_nigh = tool_close
        elif (
            # if parent range begins outside tool range and ends inside tool range
            src_open <= tool_begin
            and src_nigh > tool_begin
            and src_nigh < tool_close
        ):
            acptfact_open = tool_begin
            acptfact_nigh = src_nigh

        return acptfact_open, acptfact_nigh

    def _get_multipler_calc_acptfact_attr(
        self,
        tool_begin,
        tool_close,
        tool_numor,
        tool_denom,
        src_open,
        src_nigh,
    ):
        return self._get_range_calc_acptfact_attr(
            tool_begin=tool_begin,
            tool_close=tool_close,
            src_open=src_open * tool_numor / tool_denom,
            src_nigh=src_nigh * tool_numor / tool_denom,
        )

    def _get_remainder_calc_acptfact_attr(
        self,
        tool_begin,
        tool_close,
        src_open,
        src_nigh,
    ):
        acptfact_open = None
        acptfact_nigh = None

        if src_nigh - src_open >= tool_close:  # - tool_begin:
            acptfact_open = tool_begin
            acptfact_nigh = tool_close
        else:
            acptfact_open = src_open % tool_close
            acptfact_nigh = src_nigh % tool_close

        return acptfact_open, acptfact_nigh

    def _create_new_acptfact(
        self, tool_x: ToolKid, src_acptfact: AcptFactUnit, src_tool: ToolKid
    ) -> AcptFactUnit:
        if tool_x._begin is None or tool_x._close is None:
            raise InvalidLemmaException(
                f"Tool {tool_x._walk},{tool_x._desc} does not have range"
            )

        tool_begin = tool_x._begin
        tool_close = tool_x._close
        tool_numor = tool_x._numor
        tool_denom = tool_x._denom
        tool_reest = tool_x._reest
        src_open = src_acptfact.open
        src_nigh = src_acptfact.nigh
        src_tool_begin = src_tool._begin
        src_tool_close = src_tool._close
        tool_road = f"{tool_x._walk},{tool_x._desc}"

        acptfact_open = None
        acptfact_nigh = None

        if src_open is None and src_nigh is None:
            acptfact_open = None
            acptfact_nigh = None
        elif (tool_numor is None or tool_denom is None) and src_open > src_nigh:
            acptfact_open, acptfact_nigh = self._get_loop_range_calc_acptfact_attr(
                tool_begin=tool_begin,
                tool_close=tool_close,
                src_open=src_open,
                src_nigh=src_nigh,
                src_tool_begin=src_tool_begin,
                src_tool_close=src_tool_close,
            )

        elif tool_numor is None or tool_denom is None:
            acptfact_open, acptfact_nigh = self._get_range_calc_acptfact_attr(
                tool_begin=tool_begin,
                tool_close=tool_close,
                src_open=src_open,
                src_nigh=src_nigh,
            )
        elif tool_numor != None and tool_denom != None and tool_reest in (False, None):
            acptfact_open, acptfact_nigh = self._get_multipler_calc_acptfact_attr(
                tool_begin=tool_begin,
                tool_close=tool_close,
                tool_numor=tool_numor,
                tool_denom=tool_denom,
                src_open=src_open,
                src_nigh=src_nigh,
            )
        elif tool_numor != None and tool_denom != None and tool_reest == True:
            acptfact_open, acptfact_nigh = self._get_remainder_calc_acptfact_attr(
                tool_begin=tool_begin,
                tool_close=tool_close,
                src_open=src_open,
                src_nigh=src_nigh,
            )

        active_status = acptfact_open is not None and acptfact_nigh is not None
        return acptfactunit_shop(
            base=tool_road,
            pick=tool_road,
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

    # def _add_lemma_tool(
    def eval(self, tool_x: ToolKid, src_acptfact: AcptFactUnit, src_tool: ToolKid):
        new_acptfact = self._create_new_acptfact(
            tool_x=tool_x, src_acptfact=src_acptfact, src_tool=src_tool
        )
        road_x = f"{tool_x._walk},{tool_x._desc}"
        if self.lemmas.get(road_x) is None:
            self.lemmas[road_x] = Lemma(
                src_acptfact=src_acptfact,
                calc_acptfact=new_acptfact,
                tool_x=tool_x,
                eval_status=False,
                eval_count=1,
            )
        # else:
        #     # if new acptfactunit is inactive (acptfact.open == None and acptfact.nigh == None)
        #     # or current lemma acptfactunit acptfact.open == tool._being and acptfact.acptfact == tool._close
        #     # do nothing
        #     pass
        #     # current_lemma_acptfact = lemma_dict.get(road_x)[1]
        #     # if (
        #     #     acptfact_open != None
        #     #     and acptfact_nigh != None
        #     #     and (
        #     #         current_lemma_acptfact.open != acptfact_open
        #     #         or current_lemma_acptfact.nigh != acptfact_nigh
        #     #     )
        #     # ):
        #     #     prin(f"{current_lemma_acptfact=} {acptfact_open=} {acptfact_nigh=}")

        #     # if current_lemma_acptfact.base == "src,time,week":
        #     #     prin(f"{current_lemma_acptfact=} {acptfact_open=} {acptfact_nigh=}")
