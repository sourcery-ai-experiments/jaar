from dataclasses import dataclass
from src._prime.road import (
    RoadUnit,
    RoadNode,
    PersonRoad,
    is_sub_road,
    default_road_delimiter_if_none,
    create_road,
)
from src.instrument.python import get_empty_dict_if_none


class NoneZeroAffectException(Exception):
    pass


@dataclass
class OpinionUnit:
    road: RoadUnit
    affect: float = None
    love: float = None
    _topic_affect_ratio: float = None
    _topic_love_ratio: float = None

    def set_topic_love_ratio(self, sum_in_tribe: float, sum_out_tribe: float):
        if self.is_in_tribe():
            self._topic_love_ratio = self.love / sum_in_tribe
        elif self.is_out_tribe():
            self._topic_love_ratio = self.love / sum_out_tribe
        elif self.is_no_tribe():
            self._topic_love_ratio = 0

    def set_topic_affect_ratio(self, sum_good_affect: float, sum_bad_affect: float):
        if self.is_good():
            self._topic_affect_ratio = self.affect / sum_good_affect
        elif self.is_bad():
            self._topic_affect_ratio = self.affect / sum_bad_affect

    def set_affect(self, x_affect: float):
        if x_affect in {None, 0}:
            raise NoneZeroAffectException(
                f"set_affect affect parameter {x_affect} must be Non-zero number"
            )
        self.affect = x_affect

    def set_love(self, x_love: float):
        if x_love is None:
            x_love = 0
        self.love = x_love

    def is_good(self):
        return self.affect > 0

    def is_bad(self):
        return self.affect < 0

    def is_in_tribe(self):
        return self.love > 0

    def is_out_tribe(self):
        return self.love < 0

    def is_no_tribe(self):
        return self.love == 0


def opinionunit_shop(
    road: PersonRoad, affect: float = None, love: float = None
) -> OpinionUnit:
    x_opinionunit = OpinionUnit(road=road)
    x_opinionunit.set_affect(affect)
    x_opinionunit.set_love(love)
    return x_opinionunit


@dataclass
class TopicLink:
    base: PersonRoad = None
    action: bool = None
    weight: float = None

    def set_action(self, action_bool: bool):
        self.action = action_bool


def topiclink_shop(
    base: PersonRoad,
    action: bool = None,
    weight: float = None,
) -> TopicLink:
    if weight is None:
        weight = 1
    if action is None:
        action = False
    return TopicLink(base=base, action=action, weight=weight)


class TopicSubRoadUnitException(Exception):
    pass


@dataclass
class TopicUnit:
    base: PersonRoad = None
    opinionunits: dict[PersonRoad:OpinionUnit] = None
    # None: ignore
    # True: base idea._active reason be True,
    # False: base idea._active reason be False
    suff_idea_active: bool = None  # TODO consider removing this attr
    delimiter: str = None
    _calc_is_meaningful: bool = None
    _calc_is_tribal: bool = None
    _calc_is_dialectic: bool = None

    def is_dialectic(self):
        good_in_tribe_road = next(
            (
                x_opinionunit.road
                for x_opinionunit in self.opinionunits.values()
                if x_opinionunit.is_good() and x_opinionunit.is_in_tribe()
            ),
            None,
        )
        good_out_tribe_road = next(
            (
                x_opinionunit.road
                for x_opinionunit in self.opinionunits.values()
                if x_opinionunit.is_good() and x_opinionunit.is_out_tribe()
            ),
            None,
        )
        bad_in_tribe_road = next(
            (
                x_opinionunit.road
                for x_opinionunit in self.opinionunits.values()
                if x_opinionunit.is_bad() and x_opinionunit.is_in_tribe()
            ),
            None,
        )
        bad_out_tribe_road = next(
            (
                x_opinionunit.road
                for x_opinionunit in self.opinionunits.values()
                if x_opinionunit.is_bad() and x_opinionunit.is_out_tribe()
            ),
            None,
        )
        return (
            good_in_tribe_road != None
            and bad_in_tribe_road != None
            and good_out_tribe_road != None
            and bad_out_tribe_road != None
        )

    def is_tribal(self):
        return (
            self.get_1_opinionunit(in_tribe=True) != None
            and self.get_1_opinionunit(out_tribe=True) != None
        )

    def is_meaningful(self):
        return (
            self.get_1_opinionunit(good=True) != None
            and self.get_1_opinionunit(bad=True) != None
        )

    def set_opinionunit(self, x_opinionunit: OpinionUnit, set_metrics: bool = True):
        if is_sub_road(x_opinionunit.road, self.base) == False:
            raise TopicSubRoadUnitException(
                f"TopicUnit cannot set opinionunit '{x_opinionunit.road}' because base road is '{self.base}'."
            )
        self.opinionunits[x_opinionunit.road] = x_opinionunit
        if set_metrics:
            self.set_metrics()

    def del_opinionunit(self, opinion_road: PersonRoad):
        self.opinionunits.pop(opinion_road)

    def get_opinionunit(self, opinion_road: PersonRoad) -> OpinionUnit:
        return self.opinionunits.get(opinion_road)

    def get_opinionunits(
        self,
        good: bool = None,
        bad: bool = None,
        in_tribe: bool = None,
        out_tribe: bool = None,
        x_all: bool = None,
    ) -> dict[PersonRoad:OpinionUnit]:
        if good is None:
            good = False
        if bad is None:
            bad = False
        if in_tribe is None:
            in_tribe = False
        if out_tribe is None:
            out_tribe = False
        if x_all is None:
            x_all = False
        return {
            x_road: x_opinionunit
            for x_road, x_opinionunit in self.opinionunits.items()
            if x_all
            or (x_opinionunit.affect > 0 and good)
            or (x_opinionunit.affect < 0 and bad)
            or (x_opinionunit.love > 0 and in_tribe)
            or (x_opinionunit.love < 0 and out_tribe)
        }

    def get_all_roads(self) -> dict[PersonRoad:int]:
        x_dict = dict(self.get_opinionunits(x_all=True).items())
        x_dict[self.base] = 0
        return x_dict

    def get_1_opinionunit(
        self,
        good: bool = None,
        bad: bool = None,
        in_tribe: bool = None,
        out_tribe: bool = None,
        x_any: bool = None,
    ):
        if good is None:
            good = False
        if bad is None:
            bad = False
        if in_tribe is None:
            in_tribe = False
        if out_tribe is None:
            out_tribe = False
        if x_any is None:
            x_any = False
        return next(
            (
                x_opinionunit.road
                for x_opinionunit in self.opinionunits.values()
                if x_any
                or (x_opinionunit.affect > 0 and good)
                or (x_opinionunit.affect < 0 and bad)
                or (x_opinionunit.love > 0 and in_tribe)
                or (x_opinionunit.love < 0 and out_tribe)
            ),
            None,
        )

    def set_metrics(self):
        good_affect_sum = 0
        bad_affect_sum = 0
        in_tribe_sum = 0
        out_tribe_sum = 0
        for x_opinionunit in self.opinionunits.values():
            if x_opinionunit.is_good():
                good_affect_sum += x_opinionunit.affect
            elif x_opinionunit.is_bad():
                bad_affect_sum += x_opinionunit.affect

            if x_opinionunit.is_in_tribe():
                in_tribe_sum += x_opinionunit.love
            elif x_opinionunit.is_out_tribe():
                out_tribe_sum += x_opinionunit.love

        for x_opinionunit in self.opinionunits.values():
            x_opinionunit.set_topic_affect_ratio(good_affect_sum, bad_affect_sum)
            x_opinionunit.set_topic_love_ratio(in_tribe_sum, out_tribe_sum)

        self._calc_is_meaningful = self.is_meaningful()
        self._calc_is_tribal = self.is_tribal()
        self._calc_is_dialectic = self.is_dialectic()


def topicunit_shop(
    base: PersonRoad,
    action: bool = None,
    opinionunits: dict[PersonRoad:OpinionUnit] = None,
    delimiter: str = None,
):
    if action is None:
        action = False

    return TopicUnit(
        base=base,
        opinionunits=get_empty_dict_if_none(opinionunits),
        delimiter=default_road_delimiter_if_none(delimiter),
        _calc_is_meaningful=False,
        _calc_is_tribal=False,
        _calc_is_dialectic=False,
    )


def create_topicunit(
    base: PersonRoad, good: RoadNode, bad: RoadNode, delimiter: str = None
):
    x_topicunit = topicunit_shop(base=base)
    good_opinionunit = opinionunit_shop(create_road(base, good, delimiter=delimiter), 1)
    bad_opinionunit = opinionunit_shop(create_road(base, bad, delimiter=delimiter), -1)
    x_topicunit.set_opinionunit(good_opinionunit)
    x_topicunit.set_opinionunit(bad_opinionunit)
    if x_topicunit.is_meaningful():
        return x_topicunit
