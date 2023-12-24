from contextlib import suppress as contextlib_suppress
from src.agenda.party import PartyPID
from src.agenda.y_func import get_empty_dict_if_none
from dataclasses import dataclass


@dataclass
class OriginLink:
    pid: PartyPID
    weight: float

    def get_dict(self):
        return {
            "pid": self.pid,
            "weight": self.weight,
        }


def originlink_shop(pid: PartyPID, weight: float = None) -> OriginLink:
    if weight is None:
        weight = 1
    return OriginLink(pid=pid, weight=weight)


@dataclass
class OriginUnit:
    _links: dict[PartyPID:OriginLink] = None

    def set_originlink(self, pid: PartyPID, weight: float):
        self._links[pid] = originlink_shop(pid=pid, weight=weight)

    def del_originlink(self, pid: PartyPID):
        self._links.pop(pid)

    def get_dict(self):
        return {"_links": self.get_originlinks_dict()}

    def get_originlinks_dict(self):
        x_dict = {}
        if self._links != None:
            for originlink_x in self._links.values():
                x_dict[originlink_x.pid] = originlink_x.get_dict()
        return x_dict


def originunit_shop(_links: dict[PartyPID:OriginLink] = None) -> OriginUnit:
    return OriginUnit(_links=get_empty_dict_if_none(_links))


def originunit_get_from_dict(x_dict: dict) -> OriginUnit:
    originunit_x = originunit_shop()
    with contextlib_suppress(KeyError):
        originlinks_dict = x_dict["_links"]
        for originlink_dict in originlinks_dict.values():
            originunit_x.set_originlink(
                pid=originlink_dict["pid"], weight=originlink_dict["weight"]
            )
    return originunit_x
