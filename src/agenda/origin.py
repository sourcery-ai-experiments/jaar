from contextlib import suppress as contextlib_suppress
from src.agenda.party import PartyID
from src.tools.python import get_empty_dict_if_none
from dataclasses import dataclass


@dataclass
class OriginLink:
    party_id: PartyID
    weight: float

    def get_dict(self) -> dict[str:str]:
        return {
            "party_id": self.party_id,
            "weight": self.weight,
        }


def originlink_shop(party_id: PartyID, weight: float = None) -> OriginLink:
    if weight is None:
        weight = 1
    return OriginLink(party_id=party_id, weight=weight)


@dataclass
class OriginUnit:
    _links: dict[PartyID:OriginLink] = None

    def set_originlink(self, party_id: PartyID, weight: float):
        self._links[party_id] = originlink_shop(party_id=party_id, weight=weight)

    def del_originlink(self, party_id: PartyID):
        self._links.pop(party_id)

    def get_dict(self) -> dict[str:str]:
        return {"_links": self.get_originlinks_dict()}

    def get_originlinks_dict(self):
        x_dict = {}
        if self._links != None:
            for originlink_x in self._links.values():
                x_dict[originlink_x.party_id] = originlink_x.get_dict()
        return x_dict


def originunit_shop(_links: dict[PartyID:OriginLink] = None) -> OriginUnit:
    return OriginUnit(_links=get_empty_dict_if_none(_links))


def originunit_get_from_dict(x_dict: dict) -> OriginUnit:
    originunit_x = originunit_shop()
    with contextlib_suppress(KeyError):
        originlinks_dict = x_dict["_links"]
        for originlink_dict in originlinks_dict.values():
            originunit_x.set_originlink(
                party_id=originlink_dict["party_id"], weight=originlink_dict["weight"]
            )
    return originunit_x
