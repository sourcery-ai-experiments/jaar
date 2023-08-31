import dataclasses
from src.calendar.member import (
    MemberName,
    MemberUnit,
    MemberLink,
    memberlinks_get_from_dict,
)
from src.calendar.x_func import (
    x_get_dict,
    get_meld_weight,
    return1ifnone as x_func_return1ifnone,
)
from src.calendar.road import Road


class InvalidGroupException(Exception):
    pass


class GroupName(str):
    pass


@dataclasses.dataclass
class GroupCore:
    name: GroupName


@dataclasses.dataclass
class GroupUnit(GroupCore):
    uid: int = None
    single_member_id: int = None
    _single_member: bool = None
    _members: dict[MemberName:MemberLink] = None
    _calendar_credit: float = None
    _calendar_debt: float = None
    _calendar_agenda_credit: float = None
    _calendar_agenda_debt: float = None
    _memberlinks_set_by_system_road: Road = None

    def set_name(self, name: GroupName = None):
        if name != None:
            self.name = name

    def set_attr(self, _memberlinks_set_by_system_road: Road):
        if _memberlinks_set_by_system_road != None:
            self._memberlinks_set_by_system_road = _memberlinks_set_by_system_road

    def get_dict(self):
        return {
            "name": self.name,
            "uid": self.uid,
            "single_member_id": self.single_member_id,
            "_single_member": self._single_member,
            "_members": self.get_members_dict(),
            "_memberlinks_set_by_system_road": self._memberlinks_set_by_system_road,
        }

    def set_empty_calendar_credit_debt_to_zero(self):
        if self._calendar_credit is None:
            self._calendar_credit = 0
        if self._calendar_debt is None:
            self._calendar_debt = 0
        if self._calendar_agenda_credit is None:
            self._calendar_agenda_credit = 0
        if self._calendar_agenda_debt is None:
            self._calendar_agenda_debt = 0

    def reset_calendar_credit_debt(self):
        self._calendar_credit = 0
        self._calendar_debt = 0
        self._calendar_agenda_credit = 0
        self._calendar_agenda_debt = 0
        self._set_memberlinks_empty_if_null()
        for memberlink in self._members.values():
            memberlink.reset_calendar_credit_debt()

    def _set_memberlink_calendar_credit_debt(self):
        memberlinks_creditor_weight_sum = sum(
            memberlink.creditor_weight for memberlink in self._members.values()
        )
        memberlinks_debtor_weight_sum = sum(
            memberlink.debtor_weight for memberlink in self._members.values()
        )

        for memberlink in self._members.values():
            memberlink.set_calendar_credit_debt(
                memberlinks_creditor_weight_sum=memberlinks_creditor_weight_sum,
                memberlinks_debtor_weight_sum=memberlinks_debtor_weight_sum,
                group_calendar_credit=self._calendar_credit,
                group_calendar_debt=self._calendar_debt,
                group_calendar_agenda_credit=self._calendar_agenda_credit,
                group_calendar_agenda_debt=self._calendar_agenda_debt,
            )

    def clear_memberlinks(self):
        self._members = {}

    def _set_memberlinks_empty_if_null(self):
        if self._members is None:
            self._members = {}

    def get_members_dict(self):
        self._set_memberlinks_empty_if_null()

        x_members_dict = {}
        for member in self._members.values():
            member_dict = member.get_dict()
            x_members_dict[member_dict["name"]] = member_dict

        return x_members_dict

    def set_memberlink(self, memberlink: MemberLink):
        self._set_memberlinks_empty_if_null()
        self._members[memberlink.name] = memberlink

    def del_memberlink(self, name):
        self._members.pop(name)

    def meld(self, other_group):
        self.meld_attributes_that_will_be_equal(other_group=other_group)
        self.meld_memberlinks(other_group=other_group)

    def meld_memberlinks(self, other_group):
        self._set_memberlinks_empty_if_null()
        for oba in other_group._members.values():
            if self._members.get(oba.name) is None:
                self._members[oba.name] = oba
            else:
                self._members[oba.name].meld(oba)

    def meld_attributes_that_will_be_equal(self, other_group):
        xl = [
            ("name", self.name, other_group.name),
            ("uid", self.uid, other_group.uid),
        ]
        while xl != []:
            attrs = xl.pop()
            if attrs[1] != attrs[2]:
                raise InvalidGroupException(
                    f"Meld fail GroupUnit {self.name} .{attrs[0]}='{attrs[1]}' not the same as .{attrs[0]}='{attrs[2]}"
                )

        # if self.name != other_group.name:
        #     raise InvalidGroupException(
        #             f"Meld fail idea={self._walk},{self._desc} {attrs[0]}:{attrs[1]} with {other_idea._walk},{other_idea._desc} {attrs[0]}:{attrs[2]}"
        #     )


# class GroupUnitsshop:
def get_from_json(groupunits_json: str):
    groupunits_dict = x_get_dict(json_x=groupunits_json)
    return get_from_dict(x_dict=groupunits_dict)


def get_from_dict(x_dict: dict):
    groupunits = {}
    for groupunits_dict in x_dict.values():
        try:
            ex_memberlinks_set_by_system_road = groupunits_dict[
                "_memberlinks_set_by_system_road"
            ]
        except KeyError:
            ex_memberlinks_set_by_system_road = None

        x_group = groupunit_shop(
            name=groupunits_dict["name"],
            uid=groupunits_dict["uid"],
            _single_member=groupunits_dict["_single_member"],
            single_member_id=groupunits_dict["single_member_id"],
            _members=memberlinks_get_from_dict(x_dict=groupunits_dict["_members"]),
            _memberlinks_set_by_system_road=ex_memberlinks_set_by_system_road,
        )
        groupunits[x_group.name] = x_group
    return groupunits


def groupunit_shop(
    name: GroupName,
    uid: int = None,
    single_member_id: int = None,
    _single_member: bool = None,
    _members: dict[MemberName:MemberUnit] = None,
    _calendar_credit: float = None,
    _calendar_debt: float = None,
    _calendar_agenda_credit: float = None,
    _calendar_agenda_debt: float = None,
    _memberlinks_set_by_system_road: Road = None,
) -> GroupUnit:
    if _single_member and _memberlinks_set_by_system_road != None:
        raise InvalidGroupException(
            f"_memberlinks_set_by_system_road cannot be '{_memberlinks_set_by_system_road}' for a single_member GroupUnit. It must have no value."
        )

    if _members is None:
        _members = {}
    if _single_member is None:
        _single_member = False
    return GroupUnit(
        name=name,
        uid=uid,
        single_member_id=single_member_id,
        _single_member=_single_member,
        _members=_members,
        _calendar_credit=_calendar_credit,
        _calendar_debt=_calendar_debt,
        _calendar_agenda_credit=_calendar_agenda_credit,
        _calendar_agenda_debt=_calendar_agenda_debt,
        _memberlinks_set_by_system_road=_memberlinks_set_by_system_road,
    )


@dataclasses.dataclass
class GroupLink(GroupCore):
    creditor_weight: float = 1.0
    debtor_weight: float = 1.0

    def get_dict(self):
        return {
            "name": self.name,
            "creditor_weight": self.creditor_weight,
            "debtor_weight": self.debtor_weight,
        }

    def meld(
        self,
        other_grouplink,
        other_on_meld_weight_action: str,
        src_on_meld_weight_action: str,
    ):
        self.creditor_weight = get_meld_weight(
            src_weight=self.creditor_weight,
            src_on_meld_weight_action=src_on_meld_weight_action,
            other_weight=other_grouplink.creditor_weight,
            other_on_meld_weight_action=other_on_meld_weight_action,
        )
        self.debtor_weight = get_meld_weight(
            src_weight=self.debtor_weight,
            src_on_meld_weight_action=src_on_meld_weight_action,
            other_weight=other_grouplink.debtor_weight,
            other_on_meld_weight_action=other_on_meld_weight_action,
        )


# class GroupLinksshop:
def grouplinks_get_from_json(grouplinks_json: str) -> dict[GroupName, GroupLink]:
    grouplinks_dict = x_get_dict(json_x=grouplinks_json)
    return grouplinks_get_from_dict(x_dict=grouplinks_dict)


def grouplinks_get_from_dict(x_dict: dict) -> dict[GroupName, GroupLink]:
    grouplinks = {}
    for grouplinks_dict in x_dict.values():
        x_group = grouplink_shop(
            name=grouplinks_dict["name"],
            creditor_weight=grouplinks_dict["creditor_weight"],
            debtor_weight=grouplinks_dict["debtor_weight"],
        )
        grouplinks[x_group.name] = x_group
    return grouplinks


def grouplink_shop(
    name: GroupName, creditor_weight: float = None, debtor_weight: float = None
) -> GroupLink:
    creditor_weight = x_func_return1ifnone(creditor_weight)
    debtor_weight = x_func_return1ifnone(debtor_weight)
    return GroupLink(
        name=name, creditor_weight=creditor_weight, debtor_weight=debtor_weight
    )


@dataclasses.dataclass
class GroupHeir(GroupCore):
    creditor_weight: float = 1.0
    debtor_weight: float = 1.0
    _calendar_credit: float = None
    _calendar_debt: float = None

    def set_calendar_credit_debt(
        self,
        idea_calendar_importance,
        groupheirs_creditor_weight_sum: float,
        groupheirs_debtor_weight_sum: float,
    ):
        self._calendar_credit = idea_calendar_importance * (
            self.creditor_weight / groupheirs_creditor_weight_sum
        )
        self._calendar_debt = idea_calendar_importance * (
            self.debtor_weight / groupheirs_debtor_weight_sum
        )


def groupheir_shop(
    name: GroupName,
    creditor_weight: float = None,
    debtor_weight: float = None,
    _calendar_credit: float = None,
    _calendar_debt: float = None,
) -> GroupHeir:
    creditor_weight = x_func_return1ifnone(creditor_weight)
    debtor_weight = x_func_return1ifnone(debtor_weight)
    return GroupHeir(
        name=name,
        creditor_weight=creditor_weight,
        debtor_weight=debtor_weight,
        _calendar_credit=_calendar_credit,
        _calendar_debt=_calendar_debt,
    )


@dataclasses.dataclass
class Groupline(GroupCore):
    _calendar_credit: float
    _calendar_debt: float

    def add_calendar_credit_debt(self, calendar_credit: float, calendar_debt: float):
        self.set_calendar_credit_debt_zero_if_null()
        self._calendar_credit += calendar_credit
        self._calendar_debt += calendar_debt

    def set_calendar_credit_debt_zero_if_null(self):
        if self._calendar_credit is None:
            self._calendar_credit = 0
        if self._calendar_debt is None:
            self._calendar_debt = 0


class GroupMetrics:
    pass
