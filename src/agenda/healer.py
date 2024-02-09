from src.agenda.group import GroupID
from src.instrument.python import get_empty_set_if_none
from dataclasses import dataclass


@dataclass
class HealerHold:
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
        return {"_group_ids": list(self._group_ids)}


def healerhold_shop(_group_ids: set[GroupID] = None) -> HealerHold:
    return HealerHold(_group_ids=get_empty_set_if_none(_group_ids))
