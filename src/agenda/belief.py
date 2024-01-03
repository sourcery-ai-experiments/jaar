from dataclasses import dataclass
from src.agenda.road import (
    PersonRoad,
    RoadNode,
    is_sub_road,
    default_road_delimiter_if_none,
    create_road,
)
from src.agenda.y_func import get_empty_dict_if_none


class NoneZeroAffectException(Exception):
    pass


@dataclass
class IdeaView:
    road: PersonRoad
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


def ideaview_shop(
    road: PersonRoad, affect: float = None, love: float = None
) -> IdeaView:
    x_ideaview = IdeaView(road=road)
    x_ideaview.set_affect(affect)
    x_ideaview.set_love(love)
    return x_ideaview


class BeliefSubRoadUnitException(Exception):
    pass


@dataclass
class BeliefUnit:
    base: PersonRoad = None
    ideaviews: dict[PersonRoad:IdeaView] = None
    delimiter: str = None

    def is_dialectic(self):
        good_in_tribe_road = next(
            (
                x_ideaview.road
                for x_ideaview in self.ideaviews.values()
                if x_ideaview.is_good() and x_ideaview.is_in_tribe()
            ),
            None,
        )
        good_out_tribe_road = next(
            (
                x_ideaview.road
                for x_ideaview in self.ideaviews.values()
                if x_ideaview.is_good() and x_ideaview.is_out_tribe()
            ),
            None,
        )
        bad_in_tribe_road = next(
            (
                x_ideaview.road
                for x_ideaview in self.ideaviews.values()
                if x_ideaview.is_bad() and x_ideaview.is_in_tribe()
            ),
            None,
        )
        bad_out_tribe_road = next(
            (
                x_ideaview.road
                for x_ideaview in self.ideaviews.values()
                if x_ideaview.is_bad() and x_ideaview.is_out_tribe()
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
            self.get_1_ideaview(in_tribe=True) != None
            and self.get_1_ideaview(out_tribe=True) != None
        )

    def is_moral(self):
        return (
            self.get_1_ideaview(good=True) != None
            and self.get_1_ideaview(bad=True) != None
        )

    def set_ideaview(self, x_ideaview: IdeaView):
        if is_sub_road(x_ideaview.road, self.base) == False:
            raise BeliefSubRoadUnitException(
                f"BeliefUnit cannot set ideaview '{x_ideaview.road}' because base road is '{self.base}'."
            )
        self.ideaviews[x_ideaview.road] = x_ideaview

    def del_ideaview(self, ideaview: PersonRoad):
        self.ideaviews.pop(ideaview)

    def get_ideaviews(
        self,
        good: bool = None,
        bad: bool = None,
        in_tribe: bool = None,
        out_tribe: bool = None,
        x_all: bool = None,
    ) -> dict[PersonRoad:IdeaView]:
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
            x_road: x_ideaview
            for x_road, x_ideaview in self.ideaviews.items()
            if x_all
            or (x_ideaview.affect > 0 and good)
            or (x_ideaview.affect < 0 and bad)
            or (x_ideaview.love > 0 and in_tribe)
            or (x_ideaview.love < 0 and out_tribe)
        }

    def get_all_roads(self) -> dict[PersonRoad:int]:
        x_dict = dict(self.get_ideaviews(x_all=True).items())
        x_dict[self.base] = 0
        return x_dict

    def get_1_ideaview(
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
                x_ideaview.road
                for x_ideaview in self.ideaviews.values()
                if x_any
                or (x_ideaview.affect > 0 and good)
                or (x_ideaview.affect < 0 and bad)
                or (x_ideaview.love > 0 and in_tribe)
                or (x_ideaview.love < 0 and out_tribe)
            ),
            None,
        )


def beliefunit_shop(
    base: PersonRoad,
    ideaviews: dict[PersonRoad:float] = None,
    delimiter: str = None,
):
    return BeliefUnit(
        base=base,
        ideaviews=get_empty_dict_if_none(ideaviews),
        delimiter=default_road_delimiter_if_none(delimiter),
    )


def create_beliefunit(
    base: PersonRoad, good: RoadNode, bad: RoadNode, delimiter: str = None
):
    x_beliefunit = beliefunit_shop(base=base)
    good_ideaview = ideaview_shop(create_road(base, good, delimiter=delimiter), 1)
    bad_ideaview = ideaview_shop(create_road(base, bad, delimiter=delimiter), -1)
    x_beliefunit.set_ideaview(good_ideaview)
    x_beliefunit.set_ideaview(bad_ideaview)
    if x_beliefunit.is_moral():
        return x_beliefunit
