from contextlib import suppress as contextlib_suppress
from src.agenda.party import PartyID
from src.tools.python import get_empty_dict_if_none
from dataclasses import dataclass


@dataclass
class OriginLink:
    pid: PartyID
    weight: float

    def get_dict(self) -> dict[str:str]:
        return {
            "pid": self.pid,
            "weight": self.weight,
        }


def originlink_shop(pid: PartyID, weight: float = None) -> OriginLink:
    if weight is None:
        weight = 1
    return OriginLink(pid=pid, weight=weight)


@dataclass
class OriginUnit:
    _links: dict[PartyID:OriginLink] = None

    def set_originlink(self, pid: PartyID, weight: float):
        self._links[pid] = originlink_shop(pid=pid, weight=weight)

    def del_originlink(self, pid: PartyID):
        self._links.pop(pid)

    def get_dict(self) -> dict[str:str]:
        return {"_links": self.get_originlinks_dict()}

    def get_originlinks_dict(self):
        x_dict = {}
        if self._links != None:
            for originlink_x in self._links.values():
                x_dict[originlink_x.pid] = originlink_x.get_dict()
        return x_dict


def originunit_shop(_links: dict[PartyID:OriginLink] = None) -> OriginUnit:
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
