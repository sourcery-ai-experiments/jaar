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
    tribal: float = None

    def set_affect(self, x_affect: float):
        if x_affect in {None, 0}:
            raise NoneZeroAffectException(
                f"set_affect affect parameter {x_affect} must be Non-zero number"
            )
        self.affect = x_affect

    def set_tribal(self, x_tribal: float):
        if x_tribal is None:
            x_tribal = 0
        self.tribal = x_tribal


def prongunit_shop(
    road: RoadUnit, affect: float = None, tribal: float = None
) -> ProngUnit:
    x_prongunit = ProngUnit(road=road)
    x_prongunit.set_affect(affect)
    x_prongunit.set_tribal(tribal)
    return x_prongunit


class ForkSubRoadUnitException(Exception):
    pass


@dataclass
class ForkUnit:
    base: RoadUnit = None
    prongs: dict[RoadUnit:ProngUnit] = None
    delimiter: str = None

    def is_dialectic(self):
        return len(self.get_good_prongs()) > 0 and len(self.get_bad_prongs()) > 0

    def set_prong(self, x_prongunit: ProngUnit):
        if is_sub_road(x_prongunit.road, self.base) == False:
            raise ForkSubRoadUnitException(
                f"ForkUnit cannot set prong '{x_prongunit.road}' because base road is '{self.base}'."
            )
        self.prongs[x_prongunit.road] = x_prongunit

    def del_prong(self, prong: RoadUnit):
        self.prongs.pop(prong)

    def get_good_prongs(self) -> dict[RoadUnit:int]:
        return {
            x_road: x_prongunnit
            for x_road, x_prongunnit in self.get_prongs().items()
            if x_prongunnit.affect > 0
        }

    def get_bad_prongs(self) -> dict[RoadUnit:int]:
        return {
            x_road: x_prongunnit
            for x_road, x_prongunnit in self.get_prongs().items()
            if x_prongunnit.affect < 0
        }

    def get_prongs(self) -> dict[RoadUnit:int]:
        return self.prongs

    def get_all_roads(self) -> dict[RoadUnit:int]:
        x_dict = dict(self.get_prongs().items())
        x_dict[self.base] = 0
        return x_dict

    def get_1_good(self):
        return list(self.get_good_prongs())[0]

    def get_1_bad(self):
        return list(self.get_bad_prongs())[0]


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
    if x_forkunit.is_dialectic():
        return x_forkunit
