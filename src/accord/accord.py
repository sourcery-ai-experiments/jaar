from src._prime.road import (
    RoadUnit,
    PersonRoad,
    PersonID,
)
from src.accord.arrear import ArrearID, ArrearUnit, arrearunit_shop
from src.accord.topic import TopicUnit, TopicLink
from src.tools.python import get_empty_dict_if_none
from dataclasses import dataclass


class WantSubRoadUnitException(Exception):
    pass


@dataclass
class AccordUnit:
    _author: PersonID = None
    _reader: PersonID = None
    _topicunits: dict[PersonRoad:TopicUnit] = None
    _arrearunits: dict[ArrearID:ArrearUnit] = None

    def set_accord_metrics(self):
        arrear_sum = sum(x_arrear.weight for x_arrear in self._arrearunits.values())

        for x_arrear in self._arrearunits.values():
            x_arrear.edit_attr(_relative_accord_weight=x_arrear.weight / arrear_sum)

    def edit_arrearunit_attr(
        self, arrear_id: ArrearID, weight: float = None, actor: PersonID = None
    ):
        x_arrearunit = self.get_arrearunit(arrear_id)
        if weight != None:
            x_arrearunit.edit_attr(weight=weight)
        if actor != None:
            x_arrearunit.set_actor(actor)

    def set_arrearunit(self, x_arrearunit: ArrearUnit, actor: PersonID = None):
        self._arrearunits[x_arrearunit.uid] = x_arrearunit
        if actor != None:
            self.set_actor(actor, x_arrearunit.uid)

    def get_arrearunit(self, x_arrear_id: ArrearID) -> ArrearUnit:
        return self._arrearunits.get(x_arrear_id)

    def arrearunit_exists(self, x_arrear_id: ArrearID) -> bool:
        return self.get_arrearunit(x_arrear_id) != None

    def del_arrearunit(self, x_arrear_id: ArrearID):
        self._arrearunits.pop(x_arrear_id)

    def add_arrearunit(self) -> ArrearUnit:
        next_arrear_int = self._get_max_arrearunit_uid() + 1
        self.set_arrearunit(arrearunit_shop(uid=next_arrear_int))
        return self.get_arrearunit(next_arrear_int)

    def _get_max_arrearunit_uid(self) -> ArrearID:
        max_arrearunit_uid = 0
        for x_arrearunit in self._arrearunits.values():
            max_arrearunit_uid = max(x_arrearunit.uid, max_arrearunit_uid)
        return max_arrearunit_uid

    def is_meaningful(self) -> bool:
        return next(
            (
                False
                for x_topicunit in self._topicunits.values()
                if x_topicunit.is_meaningful() == False
            ),
            self._topicunits != {},
        )

    def set_topicunit(self, x_topicunit: TopicUnit):
        self._topicunits[x_topicunit.base] = x_topicunit

    def topicunit_exists(self, topicbase: PersonRoad) -> bool:
        return self._topicunits.get(topicbase) != None

    def get_topicunit(self, personroad: PersonRoad) -> TopicUnit:
        return self._topicunits.get(personroad)

    def del_topicunit(self, personroad: PersonRoad):
        self._topicunits.pop(personroad)

    def set_actor(self, actor: PersonID, arrear_uid: ArrearID):
        if self.arrearunit_exists(arrear_uid):
            x_arrearunit = self.get_arrearunit(arrear_uid)
            x_arrearunit.set_actor(actor)

    def del_actor(self, actor: PersonID, arrear_uid: PersonRoad):
        if self.arrearunit_exists(arrear_uid):
            x_arrearunit = self.get_arrearunit(arrear_uid)
            x_arrearunit.del_actor(actor)

    def get_actor_arrearunits(
        self, actor: PersonID, action_filter: bool = None
    ) -> dict[RoadUnit:ArrearUnit]:
        return {
            x_base: x_arrearunit
            for x_base, x_arrearunit in self._arrearunits.items()
            if x_arrearunit.actor_exists(actor)
            and (x_arrearunit.has_action() == action_filter or action_filter is None)
        }

    def actor_has_arrearunit(self, actor: PersonID, action_filter: bool = None) -> bool:
        return self.get_actor_arrearunits(actor, action_filter=action_filter) != {}


def accordunit_shop(_author: PersonID, _reader: PersonID):
    return AccordUnit(
        _author=_author,
        _reader=_reader,
        _topicunits=get_empty_dict_if_none(None),
        _arrearunits=get_empty_dict_if_none(None),
    )
