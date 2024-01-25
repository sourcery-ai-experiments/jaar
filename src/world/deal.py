from src._prime.road import (
    RoadUnit,
    PersonRoad,
    PersonID,
    EconomyRoad,
    PartyID,
    get_single_roadnode,
)
from src.world.vow import VowID, VowUnit, vowunit_shop
from src.world.partyedit import PartyEditUnit
from src.world.topic import TopicUnit
from src.tools.python import get_empty_dict_if_none
from dataclasses import dataclass


class DealMetricsException(Exception):
    pass


class WantSubRoadUnitException(Exception):
    pass


class get_member_attr_Exception(Exception):
    pass


@dataclass
class DealUnit:
    _author_road: EconomyRoad = None
    _reader_road: EconomyRoad = None
    _members_partyeditunits: dict[PersonID : dict[PartyID:PartyEditUnit]] = None
    _topicunits: dict[RoadUnit:TopicUnit] = None
    _vowunits: dict[VowID:VowUnit] = None

    def edit_partyeditunit_attr(
        self,
        member: PersonID,
        x_party_id: PartyID,
        x_creditor_change: float = None,
        x_debtor_change: float = None,
        x_depotlink_type: str = None,
    ):
        x_partyeditunit = self.get_partyeditunit(member, x_party_id)
        if x_creditor_change != None:
            x_partyeditunit.creditor_change = x_creditor_change
        if x_debtor_change != None:
            x_partyeditunit.debtor_change = x_debtor_change
        if x_depotlink_type != None:
            x_partyeditunit.depotlink_type = x_depotlink_type

    def set_partyeditunit(self, member: PersonID, x_partyeditunit: PartyEditUnit):
        x_partyeditunit.set_deal_member(member)
        member_partyeditunits = self._get_member_partyeditunits(member)
        member_partyeditunits[x_partyeditunit.party_id] = x_partyeditunit

    def _get_member_partyeditunits(
        self, member: PersonID
    ) -> dict[PartyID:PartyEditUnit]:
        return self._members_partyeditunits.get(member)

    def get_partyeditunit(self, member: PersonID, x_party_id: PartyID) -> PartyEditUnit:
        member_partyeditunits = self._get_member_partyeditunits(member)
        return member_partyeditunits.get(x_party_id)

    def del_partyeditunit(self, member: PersonID, x_party_id: PartyID):
        member_partyeditunits = self._get_member_partyeditunits(member)
        return member_partyeditunits.pop(x_party_id)

    def partyeditunit_exists(self, x_party_id: PartyID) -> bool:
        return any(
            x_member_partyeditunits.get(x_party_id) != None
            for x_member_partyeditunits in self._members_partyeditunits.values()
        )

    def set_deal_metrics(self):
        vow_author_sum = sum(x_vow.author_weight for x_vow in self._vowunits.values())
        vow_reader_sum = sum(x_vow.reader_weight for x_vow in self._vowunits.values())

        if vow_author_sum == 0:
            raise DealMetricsException(
                "Cannot set deal metrics because vow_author_sum == 0."
            )
        if vow_reader_sum == 0:
            raise DealMetricsException(
                "Cannot set deal metrics because vow_reader_sum == 0."
            )

        for x_vow in self._vowunits.values():
            x_vow.edit_attr(
                _relative_author_weight=x_vow.author_weight / vow_author_sum,
                _relative_reader_weight=x_vow.reader_weight / vow_reader_sum,
            )

    def edit_vowunit_attr(
        self,
        vow_id: VowID,
        author_weight: float = None,
        reader_weight: float = None,
        actor: PersonID = None,
    ):
        x_vowunit = self.get_vowunit(vow_id)
        if author_weight != None:
            x_vowunit.edit_attr(author_weight=author_weight)
        if reader_weight != None:
            x_vowunit.edit_attr(reader_weight=reader_weight)
        if actor != None:
            x_vowunit.set_actor(actor)

    def set_vowunit(self, x_vowunit: VowUnit, actor: PersonID = None):
        self._vowunits[x_vowunit.uid] = x_vowunit
        if actor != None:
            self.set_actor(actor, x_vowunit.uid)

    def get_vowunit(self, x_vow_id: VowID) -> VowUnit:
        return self._vowunits.get(x_vow_id)

    def vowunit_exists(self, x_vow_id: VowID) -> bool:
        return self.get_vowunit(x_vow_id) != None

    def del_vowunit(self, x_vow_id: VowID):
        self._vowunits.pop(x_vow_id)

    def add_vowunit(self) -> VowUnit:
        next_vow_int = self._get_max_vowunit_uid() + 1
        self.set_vowunit(vowunit_shop(uid=next_vow_int))
        return self.get_vowunit(next_vow_int)

    def _get_max_vowunit_uid(self) -> VowID:
        max_vowunit_uid = 0
        for x_vowunit in self._vowunits.values():
            max_vowunit_uid = max(x_vowunit.uid, max_vowunit_uid)
        return max_vowunit_uid

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

    def set_actor(self, actor: PersonID, vow_uid: VowID):
        if self.vowunit_exists(vow_uid):
            x_vowunit = self.get_vowunit(vow_uid)
            x_vowunit.set_actor(actor)

    def del_actor(self, actor: PersonID, vow_uid: PersonRoad):
        if self.vowunit_exists(vow_uid):
            x_vowunit = self.get_vowunit(vow_uid)
            x_vowunit.del_actor(actor)

    def get_actor_vowunits(
        self, actor: PersonID, action_filter: bool = None
    ) -> dict[RoadUnit:VowUnit]:
        return {
            x_base: x_vowunit
            for x_base, x_vowunit in self._vowunits.items()
            if x_vowunit.actor_exists(actor)
            and (x_vowunit.has_action() == action_filter or action_filter is None)
        }

    def actor_has_vowunit(self, actor: PersonID, action_filter: bool = None) -> bool:
        return self.get_actor_vowunits(actor, action_filter=action_filter) != {}

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


def dealunit_shop(
    _author_road: EconomyRoad,
    _reader_road: EconomyRoad,
    _members_partyeditunits: dict[PersonID : dict[PartyID:PartyEditUnit]] = None,
    _topicunits: dict[RoadUnit:TopicUnit] = None,
    _vowunits: dict[VowID:VowUnit] = None,
):
    author_person_id = get_single_roadnode("PersonRoad", _author_road, "PersonID")
    reader_person_id = get_single_roadnode("PersonRoad", _reader_road, "PersonID")
    _members_partyeditunits = get_empty_dict_if_none(_members_partyeditunits)
    if _members_partyeditunits.get(author_person_id) is None:
        _members_partyeditunits[author_person_id] = {}
    if _members_partyeditunits.get(reader_person_id) is None:
        _members_partyeditunits[reader_person_id] = {}
    return DealUnit(
        _author_road=_author_road,
        _reader_road=_reader_road,
        _members_partyeditunits=_members_partyeditunits,
        _topicunits=get_empty_dict_if_none(_topicunits),
        _vowunits=get_empty_dict_if_none(_vowunits),
    )
