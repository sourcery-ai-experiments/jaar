from src._instrument.python import get_empty_set_if_none
from src.agenda.idea import IdeaID
from dataclasses import dataclass


@dataclass
class HealerHold:
    _idea_ids: set[IdeaID]

    def set_idea_id(self, x_idea_id: IdeaID):
        self._idea_ids.add(x_idea_id)

    def idea_id_exists(self, x_idea_id: IdeaID) -> bool:
        return x_idea_id in self._idea_ids

    def any_idea_id_exists(self) -> bool:
        return len(self._idea_ids) > 0

    def del_idea_id(self, x_idea_id: IdeaID):
        self._idea_ids.remove(x_idea_id)

    def get_dict(self):
        return {"healerhold_idea_ids": list(self._idea_ids)}


def healerhold_shop(_idea_ids: set[IdeaID] = None) -> HealerHold:
    return HealerHold(_idea_ids=get_empty_set_if_none(_idea_ids))


def healerhold_get_from_dict(x_dict: dict[str:set]) -> HealerHold:
    x_healerhold = healerhold_shop()
    if x_dict.get("healerhold_idea_ids") != None:
        for x_idea_id in x_dict.get("healerhold_idea_ids"):
            x_healerhold.set_idea_id(x_idea_id=x_idea_id)
    return x_healerhold
