from dataclasses import dataclass
from src._prime.road import (
    RoadUnit,
    RoadNode,
    PersonRoad,
    is_sub_road,
    default_road_delimiter_if_none,
    create_road,
)
from src.tools.python import get_empty_dict_if_none


class NoneZeroAffectException(Exception):
    pass


@dataclass
class OpinionUnit:
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


def opinionunit_shop(
    road: PersonRoad, affect: float = None, love: float = None
) -> OpinionUnit:
    x_opinionunit = OpinionUnit(road=road)
    x_opinionunit.set_affect(affect)
    x_opinionunit.set_love(love)
    return x_opinionunit


class BeliefSubRoadUnitException(Exception):
    pass


@dataclass
class BeliefUnit:
    base: PersonRoad = None
    opinionunits: dict[PersonRoad:OpinionUnit] = None
    delimiter: str = None

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

    def is_moral(self):
        return (
            self.get_1_opinionunit(good=True) != None
            and self.get_1_opinionunit(bad=True) != None
        )

    def set_opinionunit(self, x_opinionunit: OpinionUnit):
        if is_sub_road(x_opinionunit.road, self.base) == False:
            raise BeliefSubRoadUnitException(
                f"BeliefUnit cannot set opinionunit '{x_opinionunit.road}' because base road is '{self.base}'."
            )
        self.opinionunits[x_opinionunit.road] = x_opinionunit

    def del_opinionunit(self, opinionunit: PersonRoad):
        self.opinionunits.pop(opinionunit)

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


def beliefunit_shop(
    base: PersonRoad,
    opinionunits: dict[PersonRoad:float] = None,
    delimiter: str = None,
):
    return BeliefUnit(
        base=base,
        opinionunits=get_empty_dict_if_none(opinionunits),
        delimiter=default_road_delimiter_if_none(delimiter),
    )


def create_beliefunit(
    base: PersonRoad, good: RoadNode, bad: RoadNode, delimiter: str = None
):
    x_beliefunit = beliefunit_shop(base=base)
    good_opinionunit = opinionunit_shop(create_road(base, good, delimiter=delimiter), 1)
    bad_opinionunit = opinionunit_shop(create_road(base, bad, delimiter=delimiter), -1)
    x_beliefunit.set_opinionunit(good_opinionunit)
    x_beliefunit.set_opinionunit(bad_opinionunit)
    if x_beliefunit.is_moral():
        return x_beliefunit
