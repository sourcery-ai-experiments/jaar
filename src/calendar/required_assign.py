import dataclasses
from src.calendar.group import groupunit_shop, GroupCore, GroupName


@dataclasses.dataclass
class AssignedUnit:
    _suffgroups: dict[GroupName:GroupName]

    def get_dict(self) -> dict[str:str]:
        _suffgroups = {
            group_name: group_name  # sufffact.get_dict()
            for group_name, _suffgroup in self._suffgroups.items()
        }
        return {
            "_suffgroups": _suffgroups,
        }


def assigned_unit_shop(_suffgroups: dict[GroupName:GroupName] = None) -> AssignedUnit:
    if _suffgroups is None:
        _suffgroups = {}

    return AssignedUnit(_suffgroups=_suffgroups)


@dataclasses.dataclass
class AssignedHeir:
    _suffgroups: dict[GroupName:GroupName]
    _group_member_status: bool


def assigned_heir_shop(
    _suffgroups: dict[GroupName:GroupName] = None, _group_member_status: bool = None
) -> AssignedHeir:
    if _suffgroups is None:
        _suffgroups = {}
    if _group_member_status is None:
        _group_member_status = False

    return AssignedHeir(
        _suffgroups=_suffgroups, _group_member_status=_group_member_status
    )

    # def get_key_road(self):
    #     return self.base

    # def set_empty_if_null(self):
    #     if self.sufffacts is None:
    #         self.sufffacts = {}

    # def get_sufffacts_count(self):
    #     self.set_empty_if_null()
    #     return sum(1 for _ in self.sufffacts.values())

    # def set_sufffact(
    #     self,
    #     sufffact: Road,
    #     open: float = None,
    #     nigh: float = None,
    #     divisor: int = None,
    # ):
    #     self.set_empty_if_null()
    #     self.sufffacts[sufffact] = sufffactunit_shop(
    #         need=sufffact,
    #         open=open,
    #         nigh=nigh,
    #         divisor=divisor,
    #     )

    # def del_sufffact(self, sufffact: Road):
    #     try:
    #         self.sufffacts.pop(sufffact)
    #     except KeyError as e:
    #         raise InvalidRequiredException(
    #             f"Required unable to delete sufffact {e}"
    #         ) from e

    # def find_replace_road(self, old_road: Road, new_road: Road):
    #     self.base = change_road(self.base, old_road, new_road)
    #     self.sufffacts = find_replace_road_key_dict(
    #         dict_x=self.sufffacts, old_road=old_road, new_road=new_road
    #     )

    # def meld(self, other_required):
    #     for sufffact_x in other_required.sufffacts.values():
    #         if self.sufffacts.get(sufffact_x.need) is None:
    #             self.sufffacts[sufffact_x.need] = sufffact_x
    #         else:
    #             self.sufffacts.get(sufffact_x.need).meld(sufffact_x)
    #     if other_required.base != self.base:
    #         raise InvalidRequiredException(
    #             f"Meld fail: required={other_required.base} is different {self.base=}"
    #         )
