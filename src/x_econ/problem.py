from dataclasses import dataclass
from src._prime.road import (
    MarketID,
    PersonID,
    ProblemID,
    HealerID,
    default_road_delimiter_if_none,
    validate_roadnode,
)
from src.instrument.python import get_1_if_None, get_empty_dict_if_none


@dataclass
class MarketLink:
    market_id: MarketID
    weight: float
    _relative_weight: float = None
    _person_clout: float = None

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_person_clout(self, person_clout: float):
        self._person_clout = person_clout

    def get_dict(self) -> dict[str:str]:
        return {"market_id": self.market_id, "weight": self.weight}


def marketlink_shop(market_id: MarketID, weight: float = None) -> MarketLink:
    if weight is None:
        weight = 1
    return MarketLink(market_id=market_id, weight=weight)


@dataclass
class HealerLink:
    healer_id: HealerID
    weight: float
    in_tribe: bool
    _marketlinks: dict[MarketID:MarketLink] = None
    _relative_weight: float = None
    _person_clout: float = None

    def set_marketlinks_weight_metrics(self):
        total_marketlinks_weight = sum(
            x_marketlink.weight for x_marketlink in self._marketlinks.values()
        )
        for x_marketlink in self._marketlinks.values():
            x_marketlink.set_relative_weight(
                x_marketlink.weight / total_marketlinks_weight
            )
            x_marketlink.set_person_clout(
                x_marketlink._relative_weight * self._person_clout
            )

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight

    def set_person_clout(self, person_clout: float):
        self._person_clout = person_clout
        self.set_marketlinks_weight_metrics()

    def set_marketlink(self, marketlink: MarketLink):
        self._marketlinks[marketlink.market_id] = marketlink

    def marketlink_exists(self, market_id: MarketID):
        return self._marketlinks.get(market_id) != None

    def get_marketlink(self, market_id: MarketID) -> MarketLink:
        return self._marketlinks.get(market_id)

    def del_marketlink(self, market_id: MarketID):
        self._marketlinks.pop(market_id)

    def get_marketlinks_dict(self) -> dict:
        return {
            marketlink_x.market_id: marketlink_x.get_dict()
            for marketlink_x in self._marketlinks.values()
        }

    def get_dict(self) -> dict[str:str]:
        return {
            "healer_id": self.healer_id,
            "weight": self.weight,
            "_marketlinks": self.get_marketlinks_dict(),
        }


def healerlink_shop(
    healer_id: HealerID, weight: float = None, in_tribe: bool = None
) -> HealerLink:
    if weight is None:
        weight = 1
    return HealerLink(
        healer_id=healer_id, weight=weight, in_tribe=in_tribe, _marketlinks={}
    )


@dataclass
class ProblemUnit:
    problem_id: ProblemID = None
    weight: float = None
    _healerlinks: dict[PersonID:HealerLink] = None
    _relative_weight: float = None
    _person_clout: float = None
    _road_delimiter: str = None

    def set_problem_id(self, x_problem_id: ProblemID):
        self.problem_id = validate_roadnode(x_problem_id, self._road_delimiter)

    def set_healerlinks_weight_metrics(self):
        total_healerlinks_weight = sum(
            x_healerlink.weight for x_healerlink in self._healerlinks.values()
        )

        for x_healerlink in self._healerlinks.values():
            x_healerlink.set_relative_weight(
                x_healerlink.weight / total_healerlinks_weight
            )
            x_healerlink.set_person_clout(
                x_healerlink._relative_weight * self._person_clout
            )

    def set_relative_weight(self, relative_weight: float):
        self._relative_weight = relative_weight
        self.set_person_clout(self._relative_weight)

    def set_person_clout(self, person_clout: float):
        self._person_clout = person_clout
        self.set_healerlinks_weight_metrics()

    def healer_exists(self, healer_id: HealerID) -> bool:
        return self._healerlinks.get(healer_id) != None

    def set_healerlink(self, healerlink: HealerLink):
        self._healerlinks[healerlink.healer_id] = healerlink

    def get_healerlink(self, healer_id: HealerID) -> HealerLink:
        return self._healerlinks.get(healer_id)

    def del_healerlink(self, healer_id: HealerID):
        self._healerlinks.pop(healer_id)

    def marketlink_exists(self, market_id: MarketID):
        return any(
            x_healerlink.marketlink_exists(market_id)
            for x_healerlink in self._healerlinks.values()
        )

    def get_healerlink_objs(self) -> dict[HealerID:HealerLink]:
        return self._healerlinks

    def get_healerlinks_dict(self) -> dict:
        return {
            healerlink_x.healer_id: healerlink_x.get_dict()
            for healerlink_x in self._healerlinks.values()
        }

    def get_dict(self) -> dict[str:str]:
        return {
            "problem_id": self.problem_id,
            "weight": self.weight,
            "_healerlinks": self.get_healerlinks_dict(),
        }


def problemunit_shop(
    problem_id: ProblemID, weight: float = None, _road_delimiter: str = None
) -> ProblemUnit:
    x_problemunit = ProblemUnit(
        weight=get_1_if_None(weight),
        _healerlinks=get_empty_dict_if_none(None),
        _road_delimiter=default_road_delimiter_if_none(_road_delimiter),
    )
    x_problemunit.set_problem_id(problem_id)
    return x_problemunit
