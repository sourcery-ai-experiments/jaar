from dataclasses import dataclass
from src.agenda.road import (
    RoadUnit,
    RoadNode,
    is_sub_road,
    default_road_delimiter_if_none,
    create_road,
)
from src.agenda.y_func import get_empty_dict_if_none


class NoneZeroAffectException(Exception):
    pass


@dataclass
class IdeaLink:
    road: RoadUnit
    affect: float = None
    love: float = None

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


def idealink_shop(road: RoadUnit, affect: float = None, love: float = None) -> IdeaLink:
    x_idealink = IdeaLink(road=road)
    x_idealink.set_affect(affect)
    x_idealink.set_love(love)
    return x_idealink


class BeliefSubRoadUnitException(Exception):
    pass


@dataclass
class BeliefUnit:
    base: RoadUnit = None
    idealinks: dict[RoadUnit:IdeaLink] = None
    delimiter: str = None

    def is_dialectic(self):
        good_in_tribe_road = next(
            (
                x_idealink.road
                for x_idealink in self.idealinks.values()
                if x_idealink.is_good() and x_idealink.is_in_tribe()
            ),
            None,
        )
        good_out_tribe_road = next(
            (
                x_idealink.road
                for x_idealink in self.idealinks.values()
                if x_idealink.is_good() and x_idealink.is_out_tribe()
            ),
            None,
        )
        bad_in_tribe_road = next(
            (
                x_idealink.road
                for x_idealink in self.idealinks.values()
                if x_idealink.is_bad() and x_idealink.is_in_tribe()
            ),
            None,
        )
        bad_out_tribe_road = next(
            (
                x_idealink.road
                for x_idealink in self.idealinks.values()
                if x_idealink.is_bad() and x_idealink.is_out_tribe()
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
            self.get_1_idealink(in_tribe=True) != None
            and self.get_1_idealink(out_tribe=True) != None
        )

    def is_moral(self):
        return (
            self.get_1_idealink(good=True) != None
            and self.get_1_idealink(bad=True) != None
        )

    def set_idealink(self, x_idealink: IdeaLink):
        if is_sub_road(x_idealink.road, self.base) == False:
            raise BeliefSubRoadUnitException(
                f"BeliefUnit cannot set idealink '{x_idealink.road}' because base road is '{self.base}'."
            )
        self.idealinks[x_idealink.road] = x_idealink

    def del_idealink(self, idealink: RoadUnit):
        self.idealinks.pop(idealink)

    def get_idealinks(
        self,
        good: bool = None,
        bad: bool = None,
        in_tribe: bool = None,
        out_tribe: bool = None,
        x_all: bool = None,
    ) -> dict[RoadUnit:IdeaLink]:
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
            x_road: x_idealink
            for x_road, x_idealink in self.idealinks.items()
            if x_all
            or (x_idealink.affect > 0 and good)
            or (x_idealink.affect < 0 and bad)
            or (x_idealink.love > 0 and in_tribe)
            or (x_idealink.love < 0 and out_tribe)
        }

    def get_all_roads(self) -> dict[RoadUnit:int]:
        x_dict = dict(self.get_idealinks(x_all=True).items())
        x_dict[self.base] = 0
        return x_dict

    def get_1_idealink(
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
                x_idealink.road
                for x_idealink in self.idealinks.values()
                if x_any
                or (x_idealink.affect > 0 and good)
                or (x_idealink.affect < 0 and bad)
                or (x_idealink.love > 0 and in_tribe)
                or (x_idealink.love < 0 and out_tribe)
            ),
            None,
        )


def beliefunit_shop(
    base: RoadUnit, idealinks: dict[RoadUnit:float] = None, delimiter: str = None
):
    return BeliefUnit(
        base=base,
        idealinks=get_empty_dict_if_none(idealinks),
        delimiter=default_road_delimiter_if_none(delimiter),
    )


def create_beliefunit(
    base: RoadUnit, good: RoadNode, bad: RoadNode, delimiter: str = None
):
    x_beliefunit = beliefunit_shop(base=base)
    good_idealink = idealink_shop(create_road(base, good, delimiter=delimiter), 1)
    bad_idealink = idealink_shop(create_road(base, bad, delimiter=delimiter), -1)
    x_beliefunit.set_idealink(good_idealink)
    x_beliefunit.set_idealink(bad_idealink)
    if x_beliefunit.is_moral():
        return x_beliefunit
