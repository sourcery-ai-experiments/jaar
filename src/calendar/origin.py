from contextlib import suppress as contextlib_suppress
from src.calendar.member import MemberName
from dataclasses import dataclass


@dataclass
class OriginLink:
    name: MemberName
    weight: float

    def get_dict(self):
        return {
            "name": self.name,
            "weight": self.weight,
        }


def originlink_shop(name: MemberName, weight: float = None) -> OriginLink:
    if weight is None:
        weight = 1
    return OriginLink(name=name, weight=weight)


@dataclass
class OriginUnit:
    _links: dict[MemberName:OriginLink] = None

    def _set_originlinks_empty_if_null(self):
        if self._links is None:
            self._links = {}

    def set_originlink(self, name: MemberName, weight: float):
        self._set_originlinks_empty_if_null()
        self._links[name] = originlink_shop(name=name, weight=weight)

    def del_originlink(self, name: MemberName):
        self._set_originlinks_empty_if_null()
        self._links.pop(name)

    def get_dict(self):
        return {"_links": self.get_originlinks_dict()}

    def get_originlinks_dict(self):
        x_dict = {}
        if self._links != None:
            for originlink_x in self._links.values():
                x_dict[originlink_x.name] = originlink_x.get_dict()
        return x_dict


def originunit_shop() -> OriginUnit:
    originunit_x = OriginUnit()
    originunit_x._set_originlinks_empty_if_null()
    return originunit_x


def originunit_get_from_dict(x_dict: dict) -> OriginUnit:
    originunit_x = originlink_shop()
    with contextlib_suppress(KeyError):
        originlinks_dict = x_dict["_links"]
        for originlink_dict in originlinks_dict.values():
            originunit_x.set_originlink(
                name=originlink_dict["name"], weight=originlink_dict["weight"]
            )
    return originunit_x
