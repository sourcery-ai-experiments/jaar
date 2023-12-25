from dataclasses import dataclass
from src.agenda.road import (
    RoadUnit,
    RoadNode,
    is_sub_road,
    get_node_delimiter,
    get_road,
)
from src.agenda.y_func import get_empty_dict_if_none


class NoneZeroAffectException(Exception):
    pass


@dataclass
class ProngUnit:
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


def prongunit_shop(
    road: RoadUnit, affect: float = None, love: float = None
) -> ProngUnit:
    x_prongunit = ProngUnit(road=road)
    x_prongunit.set_affect(affect)
    x_prongunit.set_love(love)
    return x_prongunit


class ForkSubRoadUnitException(Exception):
    pass


@dataclass
class ForkUnit:
    base: RoadUnit = None
    prongs: dict[RoadUnit:ProngUnit] = None
    delimiter: str = None

    def is_dialectic(self):
        good_in_tribe_road = next(
            (
                x_prongunit.road
                for x_prongunit in self.prongs.values()
                if x_prongunit.is_good() and x_prongunit.is_in_tribe()
            ),
            None,
        )
        good_out_tribe_road = next(
            (
                x_prongunit.road
                for x_prongunit in self.prongs.values()
                if x_prongunit.is_good() and x_prongunit.is_out_tribe()
            ),
            None,
        )
        bad_in_tribe_road = next(
            (
                x_prongunit.road
                for x_prongunit in self.prongs.values()
                if x_prongunit.is_bad() and x_prongunit.is_in_tribe()
            ),
            None,
        )
        bad_out_tribe_road = next(
            (
                x_prongunit.road
                for x_prongunit in self.prongs.values()
                if x_prongunit.is_bad() and x_prongunit.is_out_tribe()
            ),
            None,
        )
        print(f"{good_in_tribe_road=}")
        print(f"{bad_in_tribe_road=}")
        print(f"{good_out_tribe_road=}")
        print(f"{bad_out_tribe_road=}")
        return (
            good_in_tribe_road != None
            and bad_in_tribe_road != None
            and good_out_tribe_road != None
            and bad_out_tribe_road != None
        )

    def is_tribal(self):
        return (
            self.get_1_prong(in_tribe=True) != None
            and self.get_1_prong(out_tribe=True) != None
        )

    def is_moral(self):
        return (
            self.get_1_prong(good=True) != None and self.get_1_prong(bad=True) != None
        )

    def set_prong(self, x_prongunit: ProngUnit):
        if is_sub_road(x_prongunit.road, self.base) == False:
            raise ForkSubRoadUnitException(
                f"ForkUnit cannot set prong '{x_prongunit.road}' because base road is '{self.base}'."
            )
        self.prongs[x_prongunit.road] = x_prongunit

    def del_prong(self, prong: RoadUnit):
        self.prongs.pop(prong)

    def get_prongs(
        self,
        good: bool = None,
        bad: bool = None,
        in_tribe: bool = None,
        out_tribe: bool = None,
        x_all: bool = None,
    ) -> dict[RoadUnit:ProngUnit]:
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
            x_road: x_prongunit
            for x_road, x_prongunit in self.prongs.items()
            if x_all
            or (x_prongunit.affect > 0 and good)
            or (x_prongunit.affect < 0 and bad)
            or (x_prongunit.love > 0 and in_tribe)
            or (x_prongunit.love < 0 and out_tribe)
        }

    def get_all_roads(self) -> dict[RoadUnit:int]:
        x_dict = dict(self.get_prongs(x_all=True).items())
        x_dict[self.base] = 0
        return x_dict

    def get_1_prong(
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
                x_prongunit.road
                for x_prongunit in self.prongs.values()
                if x_any
                or (x_prongunit.affect > 0 and good)
                or (x_prongunit.affect < 0 and bad)
                or (x_prongunit.love > 0 and in_tribe)
                or (x_prongunit.love < 0 and out_tribe)
            ),
            None,
        )


def forkunit_shop(
    base: RoadUnit, prongs: dict[RoadUnit:float] = None, delimiter: str = None
):
    return ForkUnit(
        base=base,
        prongs=get_empty_dict_if_none(prongs),
        delimiter=get_node_delimiter(delimiter),
    )


def create_forkunit(
    base: RoadUnit, good: RoadNode, bad: RoadNode, delimiter: str = None
):
    x_forkunit = forkunit_shop(base=base)
    good_prongunit = prongunit_shop(get_road(base, good, delimiter=delimiter), 1)
    bad_prongunit = prongunit_shop(get_road(base, bad, delimiter=delimiter), -1)
    x_forkunit.set_prong(good_prongunit)
    x_forkunit.set_prong(bad_prongunit)
    if x_forkunit.is_moral():
        return x_forkunit
