from src.agenda.group import GroupID
from src.instrument.python import get_empty_set_if_none
from dataclasses import dataclass


@dataclass
class HealerUnit:
    _group_ids: set[GroupID]

    def set_group_id(self, x_group_id: GroupID):
        self._group_ids.add(x_group_id)

    def group_id_exists(self, x_group_id: GroupID) -> bool:
        return x_group_id in self._group_ids

    def any_group_id_exists(self) -> bool:
        return len(self._group_ids) > 0

    def del_group_id(self, x_group_id: GroupID):
        self._group_ids.remove(x_group_id)

    def get_dict(self):
        return {"healerunit_group_ids": list(self._group_ids)}


def healerunit_shop(_group_ids: set[GroupID] = None) -> HealerUnit:
    return HealerUnit(_group_ids=get_empty_set_if_none(_group_ids))


def healerunit_get_from_dict(x_dict: dict[str:set]) -> HealerUnit:
    x_healerunit = healerunit_shop()
    if x_dict.get("healerunit_group_ids") != None:
        for x_group_id in x_dict.get("healerunit_group_ids"):
            x_healerunit.set_group_id(x_group_id=x_group_id)
    return x_healerunit
