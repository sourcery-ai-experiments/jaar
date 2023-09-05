from src.calendar.member import MemberName
from dataclasses import dataclass


@dataclass
class OriginLink:
    name: MemberName
    weight: float


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


def originunit_shop() -> OriginUnit:
    originunit_x = OriginUnit()
    originunit_x._set_originlinks_empty_if_null()
    return originunit_x
