from dataclasses import dataclass
from src._prime.road import (
    RoadUnit,
    RoadNode,
    PersonRoad,
    PersonID,
    is_sub_road,
    default_road_delimiter_if_none,
    create_road,
)
from src.tools.python import get_empty_dict_if_none


class NoneZeroAffectException(Exception):
    pass


@dataclass
class FactUnit:
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


def factunit_shop(
    road: PersonRoad, affect: float = None, love: float = None
) -> FactUnit:
    x_factunit = FactUnit(road=road)
    x_factunit.set_affect(affect)
    x_factunit.set_love(love)
    return x_factunit


class TopicSubRoadUnitException(Exception):
    pass


@dataclass
class TopicUnit:
    base: PersonRoad = None
    action: bool = None
    actors: dict[PersonID:PersonID] = None
    factunits: dict[PersonRoad:FactUnit] = None
    delimiter: str = None
    _calc_is_meaningful: bool = None
    _calc_is_tribal: bool = None
    _calc_is_dialectic: bool = None

    def set_action(self, action_bool: bool):
        self.action = action_bool

    def is_dialectic(self):
        good_in_tribe_road = next(
            (
                x_factunit.road
                for x_factunit in self.factunits.values()
                if x_factunit.is_good() and x_factunit.is_in_tribe()
            ),
            None,
        )
        good_out_tribe_road = next(
            (
                x_factunit.road
                for x_factunit in self.factunits.values()
                if x_factunit.is_good() and x_factunit.is_out_tribe()
            ),
            None,
        )
        bad_in_tribe_road = next(
            (
                x_factunit.road
                for x_factunit in self.factunits.values()
                if x_factunit.is_bad() and x_factunit.is_in_tribe()
            ),
            None,
        )
        bad_out_tribe_road = next(
            (
                x_factunit.road
                for x_factunit in self.factunits.values()
                if x_factunit.is_bad() and x_factunit.is_out_tribe()
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
            self.get_1_factunit(in_tribe=True) != None
            and self.get_1_factunit(out_tribe=True) != None
        )

    def is_meaningful(self):
        return (
            self.get_1_factunit(good=True) != None
            and self.get_1_factunit(bad=True) != None
        )

    def set_factunit(self, x_factunit: FactUnit, set_metrics: bool = True):
        if is_sub_road(x_factunit.road, self.base) == False:
            raise TopicSubRoadUnitException(
                f"TopicUnit cannot set factunit '{x_factunit.road}' because base road is '{self.base}'."
            )
        self.factunits[x_factunit.road] = x_factunit
        if set_metrics:
            self.set_metrics()

    def del_factunit(self, fact_road: PersonRoad):
        self.factunits.pop(fact_road)

    def get_factunit(self, fact_road: PersonRoad) -> FactUnit:
        return self.factunits.get(fact_road)

    def get_factunits(
        self,
        good: bool = None,
        bad: bool = None,
        in_tribe: bool = None,
        out_tribe: bool = None,
        x_all: bool = None,
    ) -> dict[PersonRoad:FactUnit]:
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
            x_road: x_factunit
            for x_road, x_factunit in self.factunits.items()
            if x_all
            or (x_factunit.affect > 0 and good)
            or (x_factunit.affect < 0 and bad)
            or (x_factunit.love > 0 and in_tribe)
            or (x_factunit.love < 0 and out_tribe)
        }

    def get_all_roads(self) -> dict[PersonRoad:int]:
        x_dict = dict(self.get_factunits(x_all=True).items())
        x_dict[self.base] = 0
        return x_dict

    def get_1_factunit(
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
                x_factunit.road
                for x_factunit in self.factunits.values()
                if x_any
                or (x_factunit.affect > 0 and good)
                or (x_factunit.affect < 0 and bad)
                or (x_factunit.love > 0 and in_tribe)
                or (x_factunit.love < 0 and out_tribe)
            ),
            None,
        )

    def set_actor(self, x_actor: PersonID):
        self.actors[x_actor] = x_actor

    def del_actor(self, actor: PersonRoad):
        self.actors.pop(actor)

    def get_actor(self, x_actor: PersonID) -> PersonID:
        return self.actors.get(x_actor)

    def actor_exists(self, x_actor: PersonID) -> bool:
        return self.actors.get(x_actor) != None

    def set_metrics(self):
        good_affect_sum = 0
        bad_affect_sum = 0
        in_tribe_sum = 0
        out_tribe_sum = 0
        for x_factunit in self.factunits.values():
            if x_factunit.is_good():
                good_affect_sum += x_factunit.affect
            elif x_factunit.is_bad():
                bad_affect_sum += x_factunit.affect

            if x_factunit.is_in_tribe():
                in_tribe_sum += x_factunit.love
            elif x_factunit.is_out_tribe():
                out_tribe_sum += x_factunit.love

        for x_factunit in self.factunits.values():
            x_factunit.set_topic_affect_ratio(good_affect_sum, bad_affect_sum)
            x_factunit.set_topic_love_ratio(in_tribe_sum, out_tribe_sum)

        self._calc_is_meaningful = self.is_meaningful()
        self._calc_is_tribal = self.is_tribal()
        self._calc_is_dialectic = self.is_dialectic()


def topicunit_shop(
    base: PersonRoad,
    action: bool = None,
    factunits: dict[PersonRoad:FactUnit] = None,
    delimiter: str = None,
):
    if action is None:
        action = False

    return TopicUnit(
        base=base,
        action=action,
        factunits=get_empty_dict_if_none(factunits),
        delimiter=default_road_delimiter_if_none(delimiter),
        actors=get_empty_dict_if_none(None),
        _calc_is_meaningful=False,
        _calc_is_tribal=False,
        _calc_is_dialectic=False,
    )


def create_topicunit(
    base: PersonRoad, good: RoadNode, bad: RoadNode, delimiter: str = None
):
    x_topicunit = topicunit_shop(base=base)
    good_factunit = factunit_shop(create_road(base, good, delimiter=delimiter), 1)
    bad_factunit = factunit_shop(create_road(base, bad, delimiter=delimiter), -1)
    x_topicunit.set_factunit(good_factunit)
    x_topicunit.set_factunit(bad_factunit)
    if x_topicunit.is_meaningful():
        return x_topicunit
