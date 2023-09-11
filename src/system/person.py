from src.calendar.member import get_depotlink_types, memberunit_shop
from src.calendar.calendar import (
    get_from_json as calendarunit_get_from_json,
    get_dict_of_calendar_from_dict,
    get_meld_of_calendar_files,
    CalendarOwner,
)
from src.calendar.idea import IdeaRoot
from src.calendar.member import MemberName
from src.calendar.calendar import (
    CalendarUnit,
    get_from_json as calendarunit_get_from_json,
)
from src.calendar.x_func import (
    x_get_json,
    single_dir_create_if_null,
    rename_dir,
    save_file as x_func_save_file,
    dir_files as x_func_dir_files,
    open_file as x_func_open_file,
    delete_dir as x_func_delete_dir,
)
from dataclasses import dataclass
from os import path as os_path
from json import loads as json_loads


class InvalidPersonException(Exception):
    pass


@dataclass
class PersonAdmin:
    _person_name: str
    _env_dir: str
    _person_dir: str = None
    _persons_dir: str = None
    _person_file_name: str = None
    _person_file_path: str = None
    _calendar_output_file_name: str = None
    _calendar_output_file_path: str = None
    _calendars_public_dir: str = None
    _calendars_depot_dir: str = None
    _calendars_ignore_dir: str = None
    _calendars_bond_dir: str = None
    _calendars_digest_dir: str = None
    _isol_calendar_file_name: str = None
    _auto_output_to_public: bool = None

    def set_dirs(self):
        env_persons_dir_name = "persons"
        calendars_str = "calendars"
        self._persons_dir = f"{self._env_dir}/{env_persons_dir_name}"
        self._person_dir = f"{self._persons_dir}/{self._person_name}"
        self._person_file_name = f"{self._person_name}.json"
        self._person_file_path = f"{self._person_dir}/{self._person_file_name}"
        self._calendar_output_file_name = "output_calendar.json"
        self._calendar_output_file_path = (
            f"{self._person_dir}/{self._calendar_output_file_name}"
        )
        self._calendars_public_dir = f"{self._env_dir}/{calendars_str}"
        self._calendars_depot_dir = f"{self._person_dir}/{calendars_str}"
        self._calendars_ignore_dir = f"{self._person_dir}/ignores"
        self._calendars_bond_dir = f"{self._person_dir}/bonds"
        self._calendars_digest_dir = f"{self._person_dir}/digests"
        self._isol_calendar_file_name = "isol_calendar.json"
        self._auto_output_to_public = self._set_auto_output_to_public(
            self._auto_output_to_public
        )

    def _set_auto_output_to_public(self, bool_x: bool):
        return bool_x is not None and bool_x

    def set_person_name(self, new_name: str):
        old_name = self._person_name
        old_person_dir = self._person_dir
        self._person_name = new_name
        self.set_dirs()
        old_person_dir_file_path = f"{self._person_dir}/{old_name}.json"

        rename_dir(src=old_person_dir, dst=self._person_dir)
        rename_dir(src=old_person_dir_file_path, dst=self._person_file_path)

    def create_core_dir_and_files(self, file_text: str):
        single_dir_create_if_null(x_path=self._person_dir)
        single_dir_create_if_null(x_path=self._calendars_public_dir)
        single_dir_create_if_null(x_path=self._calendars_depot_dir)
        single_dir_create_if_null(x_path=self._calendars_digest_dir)
        single_dir_create_if_null(x_path=self._calendars_ignore_dir)
        single_dir_create_if_null(x_path=self._calendars_bond_dir)
        x_func_save_file(
            dest_dir=self._person_dir,
            file_name=self._person_file_name,
            file_text=file_text,
            replace=False,
        )

    def _save_calendar_to_path(
        self, calendar_x: CalendarUnit, dest_dir: str, file_name: str = None
    ):
        if file_name is None:
            file_name = f"{calendar_x._owner}.json"
        x_func_save_file(
            dest_dir=dest_dir,
            file_name=file_name,
            file_text=calendar_x.get_json(),
            replace=True,
        )

    def save_calendar_to_public(self, calendar_x: CalendarUnit):
        dest_dir = self._calendars_public_dir
        self._save_calendar_to_path(calendar_x, dest_dir)

    def save_ignore_calendar(self, calendar_x: CalendarUnit, src_calendar_owner: str):
        dest_dir = self._calendars_ignore_dir
        file_name = None
        if src_calendar_owner != None:
            file_name = f"{src_calendar_owner}.json"
        else:
            file_name = f"{calendar_x._owner}.json"
        self._save_calendar_to_path(calendar_x, dest_dir, file_name)

    def save_calendar_to_digest(
        self, calendar_x: CalendarUnit, src_calendar_owner: str = None
    ):
        dest_dir = self._calendars_digest_dir
        file_name = None
        if src_calendar_owner != None:
            file_name = f"{src_calendar_owner}.json"
        else:
            file_name = f"{calendar_x._owner}.json"
        self._save_calendar_to_path(calendar_x, dest_dir, file_name)

    def save_isol_calendar(self, calendar_x: CalendarUnit):
        calendar_x.set_owner(self._person_name)
        self._save_calendar_to_path(
            calendar_x, self._person_dir, self._isol_calendar_file_name
        )

    def save_calendar_to_depot(self, calendar_x: CalendarUnit):
        dest_dir = self._calendars_depot_dir
        self._save_calendar_to_path(calendar_x, dest_dir)
        if self._auto_output_to_public:
            self.save_calendar_to_public(calendar_x)

    def save_output_calendar(self) -> CalendarUnit:
        isol_calendar_x = self.open_isol_calendar()
        isol_calendar_x.meld(isol_calendar_x, member_weight=1)
        calendar_x = get_meld_of_calendar_files(
            cx_primary=isol_calendar_x,
            meldees_dir=self._calendars_digest_dir,
        )
        dest_dir = self._person_dir
        file_name = self._calendar_output_file_name
        self._save_calendar_to_path(calendar_x, dest_dir, file_name)

    def open_public_calendar(self, owner: CalendarOwner) -> str:
        file_name_x = f"{owner}.json"
        return x_func_open_file(self._calendars_public_dir, file_name_x)

    def open_depot_calendar(self, owner: CalendarOwner) -> str:
        file_name_x = f"{owner}.json"
        cx_json = x_func_open_file(self._calendars_depot_dir, file_name_x)
        return calendarunit_get_from_json(cx_json=cx_json)

    def open_ignore_calendar(self, owner: CalendarOwner) -> CalendarUnit:
        ignore_file_name = f"{owner}.json"
        calendar_json = x_func_open_file(self._calendars_ignore_dir, ignore_file_name)
        calendar_obj = calendarunit_get_from_json(cx_json=calendar_json)
        calendar_obj.set_calendar_metrics()
        return calendar_obj

    def open_isol_calendar(self) -> CalendarUnit:
        cx = None
        try:
            ct = x_func_open_file(self._person_dir, self._isol_calendar_file_name)
            cx = calendarunit_get_from_json(cx_json=ct)
        except Exception:
            self.save_isol_calendar(self._get_empty_isol_calendar())
            ct = x_func_open_file(self._person_dir, self._isol_calendar_file_name)
            cx = calendarunit_get_from_json(cx_json=ct)
        cx.set_calendar_metrics()
        return cx

    def open_output_calendar(self) -> CalendarUnit:
        cx_json = x_func_open_file(self._person_dir, self._calendar_output_file_name)
        cx_obj = calendarunit_get_from_json(cx_json)
        cx_obj.set_calendar_metrics()
        return cx_obj

    def _get_empty_isol_calendar(self):
        return CalendarUnit(_owner=self._person_name, _weight=0)

    def erase_depot_calendar(self, owner):
        x_func_delete_dir(f"{self._calendars_depot_dir}/{owner}.json")

    def erase_digest_calendar(self, owner):
        x_func_delete_dir(f"{self._calendars_digest_dir}/{owner}.json")

    def erase_isol_calendar_file(self):
        x_func_delete_dir(dir=f"{self._person_dir}/{self._isol_calendar_file_name}")

    def check_file_exists(self, dir_type: str, owner: str):
        cx_file_name = f"{owner}.json"
        if dir_type == "depot":
            cx_file_path = f"{self._calendars_depot_dir}/{cx_file_name}"
        if not os_path.exists(cx_file_path):
            raise InvalidPersonException(
                f"Person {self._person_name} cannot find calendar {owner} in {cx_file_path}"
            )

    def get_dict(self):
        return {
            "name": self._person_name,
            "_auto_output_to_public": self._auto_output_to_public,
        }


def personadmin_shop(
    _person_name: str, _env_dir: str, _auto_output_to_public: bool = None
) -> PersonAdmin:
    px = PersonAdmin(
        _person_name=_person_name,
        _env_dir=_env_dir,
        _auto_output_to_public=_auto_output_to_public,
    )
    px.set_dirs()
    return px


@dataclass
class PersonUnit:
    _admin: PersonAdmin = None
    _isol: CalendarUnit = None

    def reset_depot_calendars(self):
        for member_x in self._isol._members.values():
            member_calendar = calendarunit_get_from_json(
                cx_json=self._admin.open_public_calendar(member_x.name)
            )
            self.set_depot_calendar(
                calendar_x=member_calendar,
                depotlink_type=member_x.depotlink_type,
                creditor_weight=member_x.creditor_weight,
                debtor_weight=member_x.debtor_weight,
            )

    def set_depot_calendar(
        self,
        calendar_x: CalendarUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        self.set_isol_calendar_if_empty()
        self._admin.save_calendar_to_depot(calendar_x)
        self._set_depotlink(
            calendar_x._owner, depotlink_type, creditor_weight, debtor_weight
        )

    def _set_depotlinks_empty_if_null(self):
        self.set_isol_calendar_if_empty()
        self._isol.set_members_empty_if_null()

    def _set_depotlink(
        self,
        owner: str,
        link_type: str = None,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        self._admin.check_file_exists("depot", owner)
        member_x = self._isol.get_member(owner)
        if member_x is None:
            self._isol.set_memberunit(
                memberunit_shop(
                    name=owner,
                    depotlink_type=link_type,
                    creditor_weight=creditor_weight,
                    debtor_weight=debtor_weight,
                )
            )
        else:
            member_x.set_depotlink_type(
                depotlink_type=link_type,
                creditor_weight=creditor_weight,
                debtor_weight=debtor_weight,
            )

        if link_type == "blind_trust":
            cx_obj = self._admin.open_depot_calendar(owner=owner)
            self._admin.save_calendar_to_digest(cx_obj)
        elif link_type == "ignore":
            new_cx_obj = CalendarUnit(_owner=owner)
            self.set_ignore_calendar_file(new_cx_obj, new_cx_obj._owner)

    def del_depot_calendar(self, calendar_owner: str):
        self._del_depotlink(membername=calendar_owner)
        self._admin.erase_depot_calendar(calendar_owner)
        self._admin.erase_digest_calendar(calendar_owner)

    def _del_depotlink(self, membername: MemberName):
        self._isol.get_member(membername).del_depotlink_type()

    def get_isol_calendar(self):
        if self._isol is None:
            self._isol = self._admin.open_isol_calendar()
        return self._isol

    def set_isol_calendar(self, calendar_x: CalendarUnit = None):
        if calendar_x != None:
            self._isol = calendar_x
        self._admin.save_isol_calendar(self._isol)
        self._isol = None

    def set_isol_calendar_if_empty(self):
        # if self._isol is None:
        self.get_isol_calendar()

    def get_refreshed_output_calendar(self) -> CalendarUnit:
        self._admin.save_output_calendar()
        return self._admin.open_output_calendar()

    def set_ignore_calendar_file(
        self, calendarunit: CalendarUnit, src_calendar_owner: str
    ):
        self._admin.save_ignore_calendar(calendarunit, src_calendar_owner)
        self._admin.save_calendar_to_digest(calendarunit, src_calendar_owner)

    # housekeeping
    def get_dict(self):
        return self._admin.get_dict()

    def get_json(self):
        return x_get_json(dict_x=self.get_dict())

    def set_env_dir(
        self, env_dir: str, person_name: str, _auto_output_to_public: bool = None
    ):
        self._admin = personadmin_shop(
            _person_name=person_name,
            _env_dir=env_dir,
            _auto_output_to_public=_auto_output_to_public,
        )

    def create_core_dir_and_files(self):
        self._admin.create_core_dir_and_files(self.get_json())


def personunit_shop(
    name: str, env_dir: str, _auto_output_to_public: bool = None
) -> PersonUnit:
    person_x = PersonUnit()
    person_x.set_env_dir(env_dir, name, _auto_output_to_public)
    return person_x


def get_from_json(person_json: str, env_dir: str) -> PersonUnit:
    return get_from_dict(person_dict=json_loads(person_json), env_dir=env_dir)


def get_from_dict(person_dict: dict, env_dir: str) -> PersonUnit:
    return personunit_shop(
        name=person_dict["name"],
        env_dir=env_dir,
        _auto_output_to_public=person_dict["_auto_output_to_public"],
    )
