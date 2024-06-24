from contextlib import suppress as contextlib_suppress
from src._truth.other import OtherID
from src._instrument.python import get_empty_dict_if_none
from dataclasses import dataclass


@dataclass
class OriginLink:
    other_id: OtherID
    weight: float

    def get_dict(self) -> dict[str:str]:
        return {
            "other_id": self.other_id,
            "weight": self.weight,
        }


def originlink_shop(other_id: OtherID, weight: float = None) -> OriginLink:
    if weight is None:
        weight = 1
    return OriginLink(other_id=other_id, weight=weight)


@dataclass
class OriginUnit:
    _links: dict[OtherID:OriginLink] = None

    def set_originlink(self, other_id: OtherID, weight: float):
        self._links[other_id] = originlink_shop(other_id=other_id, weight=weight)

    def del_originlink(self, other_id: OtherID):
        self._links.pop(other_id)

    def get_dict(self) -> dict[str:str]:
        return {"_links": self.get_originlinks_dict()}

    def get_originlinks_dict(self):
        x_dict = {}
        if self._links != None:
            for originlink_x in self._links.values():
                x_dict[originlink_x.other_id] = originlink_x.get_dict()
        return x_dict


def originunit_shop(_links: dict[OtherID:OriginLink] = None) -> OriginUnit:
    return OriginUnit(_links=get_empty_dict_if_none(_links))


def originunit_get_from_dict(x_dict: dict) -> OriginUnit:
    originunit_x = originunit_shop()
    with contextlib_suppress(KeyError):
        originlinks_dict = x_dict["_links"]
        for originlink_dict in originlinks_dict.values():
            originunit_x.set_originlink(
                other_id=originlink_dict["other_id"], weight=originlink_dict["weight"]
            )
    return originunit_x
