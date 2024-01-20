from src._prime.road import (
    RoadUnit,
    PersonRoad,
    PersonID,
    EconomyRoad,
    PartyID,
    get_single_roadnode,
)
from src.accord.due import DueID, DueUnit, dueunit_shop
from src.accord.delta import DeltaUnit
from src.accord.topic import TopicUnit, TopicLink
from src.tools.python import get_empty_dict_if_none
from dataclasses import dataclass


class AccordMetricsException(Exception):
    pass


class WantSubRoadUnitException(Exception):
    pass


class get_member_attr_Exception(Exception):
    pass


@dataclass
class AccordUnit:
    _author_road: EconomyRoad = None
    _reader_road: EconomyRoad = None
    _author_deltaunits: dict[PartyID:DeltaUnit] = None
    _reader_deltaunits: dict[PartyID:DeltaUnit] = None
    _topicunits: dict[RoadUnit:TopicUnit] = None
    _dueunits: dict[DueID:DueUnit] = None

    def edit_deltaunit_attr(
        self,
        x_party_id: PartyID,
        x_creditor_weight: float = None,
        x_debtor_weight: float = None,
        x_depotlink_type: str = None,
        author: bool = None,
        reader: bool = None,
    ):
        x_deltaunit = self.get_deltaunit(x_party_id, author, reader)
        if x_creditor_weight != None:
            x_deltaunit.creditor_weight = x_creditor_weight
        if x_debtor_weight != None:
            x_deltaunit.debtor_weight = x_debtor_weight
        if x_depotlink_type != None:
            x_deltaunit.depotlink_type = x_depotlink_type

    def set_deltaunit(
        self, x_delta: DeltaUnit, author: bool = False, reader: bool = False
    ):
        if author:
            self._author_deltaunits[x_delta.party_id] = x_delta
        if reader:
            self._reader_deltaunits[x_delta.party_id] = x_delta

    def get_deltaunit(
        self, x_party_id: PartyID, author: bool = False, reader: bool = False
    ) -> DeltaUnit:
        if author:
            return self._author_deltaunits.get(x_party_id)
        if reader:
            return self._reader_deltaunits.get(x_party_id)

    def del_deltaunit(
        self, x_party_id: PartyID, author: bool = False, reader: bool = False
    ):
        if author:
            return self._author_deltaunits.pop(x_party_id)
        if reader:
            return self._reader_deltaunits.pop(x_party_id)

    def deltaunit_exists(self, x_party_id: PartyID) -> bool:
        return (
            self._author_deltaunits.get(x_party_id) != None
            or self._reader_deltaunits.get(x_party_id) != None
        )

    def set_accord_metrics(self):
        due_author_sum = sum(x_due.author_weight for x_due in self._dueunits.values())
        due_reader_sum = sum(x_due.reader_weight for x_due in self._dueunits.values())

        if due_author_sum == 0:
            raise AccordMetricsException(
                "Cannot set accord metrics because due_author_sum == 0."
            )
        if due_reader_sum == 0:
            raise AccordMetricsException(
                "Cannot set accord metrics because due_reader_sum == 0."
            )

        for x_due in self._dueunits.values():
            x_due.edit_attr(
                _relative_author_weight=x_due.author_weight / due_author_sum,
                _relative_reader_weight=x_due.reader_weight / due_reader_sum,
            )

    def edit_dueunit_attr(
        self,
        due_id: DueID,
        author_weight: float = None,
        reader_weight: float = None,
        actor: PersonID = None,
    ):
        x_dueunit = self.get_dueunit(due_id)
        if author_weight != None:
            x_dueunit.edit_attr(author_weight=author_weight)
        if reader_weight != None:
            x_dueunit.edit_attr(reader_weight=reader_weight)
        if actor != None:
            x_dueunit.set_actor(actor)

    def set_dueunit(self, x_dueunit: DueUnit, actor: PersonID = None):
        self._dueunits[x_dueunit.uid] = x_dueunit
        if actor != None:
            self.set_actor(actor, x_dueunit.uid)

    def get_dueunit(self, x_due_id: DueID) -> DueUnit:
        return self._dueunits.get(x_due_id)

    def dueunit_exists(self, x_due_id: DueID) -> bool:
        return self.get_dueunit(x_due_id) != None

    def del_dueunit(self, x_due_id: DueID):
        self._dueunits.pop(x_due_id)

    def add_dueunit(self) -> DueUnit:
        next_due_int = self._get_max_dueunit_uid() + 1
        self.set_dueunit(dueunit_shop(uid=next_due_int))
        return self.get_dueunit(next_due_int)

    def _get_max_dueunit_uid(self) -> DueID:
        max_dueunit_uid = 0
        for x_dueunit in self._dueunits.values():
            max_dueunit_uid = max(x_dueunit.uid, max_dueunit_uid)
        return max_dueunit_uid

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

    def set_actor(self, actor: PersonID, due_uid: DueID):
        if self.dueunit_exists(due_uid):
            x_dueunit = self.get_dueunit(due_uid)
            x_dueunit.set_actor(actor)

    def del_actor(self, actor: PersonID, due_uid: PersonRoad):
        if self.dueunit_exists(due_uid):
            x_dueunit = self.get_dueunit(due_uid)
            x_dueunit.del_actor(actor)

    def get_actor_dueunits(
        self, actor: PersonID, action_filter: bool = None
    ) -> dict[RoadUnit:DueUnit]:
        return {
            x_base: x_dueunit
            for x_base, x_dueunit in self._dueunits.items()
            if x_dueunit.actor_exists(actor)
            and (x_dueunit.has_action() == action_filter or action_filter is None)
        }

    def actor_has_dueunit(self, actor: PersonID, action_filter: bool = None) -> bool:
        return self.get_actor_dueunits(actor, action_filter=action_filter) != {}

    def get_member_attr(self, member: str, attr: str):
        if member not in ("reader", "author"):
            raise get_member_attr_Exception(
                f"get_member_attr cannot receive '{member}' as member parameter."
            )
        if member == "reader":
            return get_single_roadnode(
                roadunit_type="PersonRoad",
                x_roadunit=self._reader_road,
                roadnode_type=attr,
            )
        elif member == "author":
            print(f"huh {attr}")
            return get_single_roadnode(
                roadunit_type="PersonRoad",
                x_roadunit=self._author_road,
                roadnode_type=attr,
            )


def accordunit_shop(
    _author_road: EconomyRoad,
    _reader_road: EconomyRoad,
    _author_deltaunits: dict[PartyID:DeltaUnit] = None,
    _reader_deltaunits: dict[PartyID:DeltaUnit] = None,
    _topicunits: dict[RoadUnit:TopicUnit] = None,
    _dueunits: dict[DueID:DueUnit] = None,
):
    return AccordUnit(
        _author_road=_author_road,
        _reader_road=_reader_road,
        _author_deltaunits=get_empty_dict_if_none(_author_deltaunits),
        _reader_deltaunits=get_empty_dict_if_none(_reader_deltaunits),
        _topicunits=get_empty_dict_if_none(_topicunits),
        _dueunits=get_empty_dict_if_none(_dueunits),
    )
