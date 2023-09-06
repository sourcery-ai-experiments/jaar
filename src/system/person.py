from src.system.calendarlink import (
    calendarlink_shop,
    get_calendar_from_calendars_dirlink_from_dict,
    CalendarLink,
    get_calendarlink_types,
)
from src.calendar.calendar import (
    get_from_json as calendarunit_get_from_json,
    get_dict_of_calendar_from_dict,
    get_meld_of_calendar_files,
)
from src.calendar.idea import IdeaRoot
from src.calendar.road import Road
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


@dataclass
class PersonAdmin:
    _person_name: str
    _env_dir: str
    _person_dir: str = None
    _persons_dir: str = None
    _person_file_name: str = None
    _person_file_path: str = None
    _calendars_public_dir: str = None
    _calendars_depot_dir: str = None
    _calendars_ignore_dir: str = None
    _calendars_bond_dir: str = None
    _calendars_digest_dir: str = None
    _isol_calendar_file_name: str = None

    def set_dirs(self):
        env_persons_dir_name = "persons"
        calendars_str = "calendars"
        self._persons_dir = f"{self._env_dir}/{env_persons_dir_name}"
        self._person_dir = f"{self._persons_dir}/{self._person_name}"
        self._person_file_name = f"{self._person_name}.json"
        self._person_file_path = f"{self._person_dir}/{self._person_file_name}"
        self._calendars_public_dir = f"{self._env_dir}/{calendars_str}"
        self._calendars_depot_dir = f"{self._person_dir}/{calendars_str}"
        self._calendars_ignore_dir = f"{self._person_dir}/ignores"
        self._calendars_bond_dir = f"{self._person_dir}/bonds"
        self._calendars_digest_dir = f"{self._person_dir}/digests"
        self._isol_calendar_file_name = "isol_digest_calendar.json"

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

    def save_calendar_to_depot(self, calendar_x: CalendarUnit):
        x_func_save_file(
            dest_dir=self._calendars_depot_dir,
            file_name=f"{calendar_x._owner}.json",
            file_text=calendar_x.get_json(),
        )

    def save_calendar_to_public(self, calendar_x: CalendarUnit):
        x_func_save_file(
            dest_dir=self._calendars_public_dir,
            file_name=f"{calendar_x._owner}.json",
            file_text=calendar_x.get_json(),
            replace=True,
        )

    def get_public_calendar(self, owner: str) -> CalendarUnit:
        file_name_x = f"{owner}.json"
        return x_func_open_file(self._calendars_public_dir, file_name_x)

    def get_depot_calendar(self, owner: str) -> CalendarUnit:
        file_name_x = f"{owner}.json"
        cx_json = x_func_open_file(self._calendars_depot_dir, file_name_x)
        return calendarunit_get_from_json(cx_json=cx_json)

    def init_ignore_calendar(self, _label: str) -> CalendarUnit:
        ignore_file_name = f"{_label}.json"
        calendar_json = x_func_open_file(self._calendars_ignore_dir, ignore_file_name)
        calendar_obj = calendarunit_get_from_json(cx_json=calendar_json)
        calendar_obj.set_calendar_metrics()
        return calendar_obj

    def save_calendar_to_ignore_dir(
        self, calendar_x: CalendarUnit, src_calendar_owner: str
    ):
        file_name = f"{src_calendar_owner}.json"
        x_func_save_file(
            dest_dir=self._calendars_ignore_dir,
            file_name=file_name,
            file_text=calendar_x.get_json(),
            replace=True,
        )

    def save_calendar_to_digest(
        self, calendar_x: CalendarUnit, src_calendar_owner: str = None
    ):
        if src_calendar_owner is None:
            src_calendar_owner = calendar_x._owner
        file_name = f"{src_calendar_owner}.json"
        x_func_save_file(
            dest_dir=self._calendars_digest_dir,
            file_name=file_name,
            file_text=calendar_x.get_json(),
            replace=True,
        )

    def init_isol_calendar(self) -> CalendarUnit:
        return x_func_open_file(self._person_dir, self._isol_calendar_file_name)

    def del_isol_digest_calendar_file(self):
        x_func_delete_dir(dir=f"{self._person_dir}/{self._isol_calendar_file_name}")

    def get_isol_digest_calendar(self) -> CalendarUnit:
        cx = None
        try:
            ct = self.init_isol_calendar()
            cx = calendarunit_get_from_json(cx_json=ct)
        except Exception:
            cx = self._get_empty_isol_digest_calendar()
        cx.set_calendar_metrics()
        return cx

    def set_isol_digest_calendar(self, calendar_x: CalendarUnit):
        calendar_x.set_owner(self._person_name)
        x_func_save_file(
            dest_dir=self._person_dir,
            file_name=self._isol_calendar_file_name,
            file_text=calendar_x.get_json(),
            replace=True,
        )

    def _get_empty_isol_digest_calendar(self):
        return CalendarUnit(_owner=self._person_name, _weight=0)

    def delete_depot_calendar(self, owner):
        x_func_delete_dir(f"{self._calendars_depot_dir}/{owner}.json")

    def delete_digest_calendar(self, owner):
        x_func_delete_dir(f"{self._calendars_digest_dir}/{owner}.json")

    def check_file_exists(self, dir_type: str, owner: str):
        cx_file_name = f"{owner}.json"
        cx_file_path = f"{self._calendars_depot_dir}/{cx_file_name}"
        if not os_path.exists(cx_file_path):
            raise InvalidPersonException(
                f"Person {self._person_name} cannot find calendar {owner} in {cx_file_path}"
            )


class InvalidPersonException(Exception):
    pass


@dataclass
class PersonUnit:
    _admin: PersonAdmin = None
    _src_calendarlinks: dict[str:CalendarUnit] = None
    _output_calendar: CalendarUnit = None
    _auto_output_calendar_to_public: bool = None

    # dir methods
    def _set_env_dir(self, env_dir: str, person_name: str):
        self._admin = PersonAdmin(_person_name=person_name, _env_dir=env_dir)
        self._admin.set_dirs()

    def create_core_dir_and_files(self):
        self._admin.create_core_dir_and_files(self.get_json())

    def receive_src_calendarunit_obj(
        self,
        calendar_x: CalendarUnit,
        link_type: str = None,
        calendarlink_weight: float = None,
    ):
        self._admin.save_calendar_to_depot(calendar_x)
        self.set_src_calendarlinks(calendar_x._owner, link_type, calendarlink_weight)
        if self._auto_output_calendar_to_public:
            self.save_output_calendar_to_public_dir()

    def receive_src_calendarunit_file(
        self, calendar_json: str, link_type: str = None, weight: float = None
    ):
        calendar_x = calendarunit_get_from_json(cx_json=calendar_json)
        self.receive_src_calendarunit_obj(calendar_x, link_type, weight)

    def receive_all_src_calendarunit_files(self):
        for calendarlink_obj in self._src_calendarlinks.values():
            cx_json = self._admin.get_public_calendar(calendarlink_obj.calendar_owner)
            self.receive_src_calendarunit_file(
                calendar_json=cx_json,
                link_type=calendarlink_obj.link_type,
                weight=calendarlink_obj.weight,
            )

    def set_src_calendarlinks(
        self, owner: str, link_type: str = None, weight: float = None
    ):
        self.set_src_calendarlinks_empty_if_null()
        self._admin.check_file_exists("depot", owner)

        calendarlink_x = calendarlink_shop(owner, link_type, weight)
        self._src_calendarlinks[owner] = calendarlink_x

        if calendarlink_x.link_type == "blind_trust":
            cx_obj = self._admin.get_depot_calendar(owner=owner)
            self._admin.save_calendar_to_digest(cx_obj)
        elif calendarlink_x.link_type == "ignore":
            new_cx_obj = CalendarUnit(_owner=owner)
            self.set_ignore_calendar_file(new_cx_obj, new_cx_obj._owner)

    def set_src_calendarlinks_empty_if_null(self):
        if self._src_calendarlinks is None:
            self._src_calendarlinks = {}

    def delete_calendarlink(self, calendar_owner: str):
        self._src_calendarlinks.pop(calendar_owner)
        self._admin.delete_depot_calendar(calendar_owner)
        self._admin.delete_digest_calendar(calendar_owner)

    def _set_auto_output_calendar_to_public(self, bool_x: bool):
        self._auto_output_calendar_to_public = bool_x

    def _set_emtpy_output_calendar(self):
        self._output_calendar = CalendarUnit(_owner=self._admin._person_name)

    def get_output_from_digest_calendar_files(self) -> CalendarUnit:
        return get_meld_of_calendar_files(
            cx_primary=self._admin.get_isol_digest_calendar(),
            meldees_dir=self._admin._calendars_digest_dir,
        )

    def save_output_calendar_to_public_dir(self):
        self._admin.save_calendar_to_public(
            self.get_output_from_digest_calendar_files()
        )

    def get_ignore_calendar_from_ignore_calendar_files(
        self, _label: str
    ) -> CalendarUnit:
        return self._admin.init_ignore_calendar(_label)

    def set_ignore_calendar_file(
        self, calendarunit: CalendarUnit, src_calendar_owner: str
    ):
        self._admin.save_calendar_to_ignore_dir(calendarunit, src_calendar_owner)
        self._admin.save_calendar_to_digest(calendarunit, src_calendar_owner)

    def get_dict(self):
        return {
            "name": self._admin._person_name,
            "_src_calendarlinks": self.get_calendar_from_calendars_dirlinks_dict(),
            "_auto_output_calendar_to_public": self._auto_output_calendar_to_public,
        }

    def get_calendar_from_calendars_dirlinks_dict(self) -> dict[str:dict]:
        src_calendarlinks_dict = {}
        for calendarlink_x in self._src_calendarlinks.values():
            single_x_dict = calendarlink_x.get_dict()
            src_calendarlinks_dict[single_x_dict["calendar_owner"]] = single_x_dict
        return src_calendarlinks_dict

    def get_json(self):
        x_dict = self.get_dict()
        return x_get_json(dict_x=x_dict)


def personunit_shop(
    name: str, env_dir: str, _auto_output_calendar_to_public: bool = None
) -> PersonUnit:
    person_x = PersonUnit()
    person_x._set_env_dir(env_dir=env_dir, person_name=name)
    person_x._set_auto_output_calendar_to_public(_auto_output_calendar_to_public)
    person_x.set_src_calendarlinks_empty_if_null()
    person_x._set_emtpy_output_calendar()
    return person_x


def get_from_json(person_json: str, env_dir: str) -> PersonUnit:
    return get_from_dict(person_dict=json_loads(person_json), env_dir=env_dir)


def get_from_dict(person_dict: dict, env_dir: str) -> PersonUnit:
    wx = personunit_shop(
        name=person_dict["name"],
        env_dir=env_dir,
        _auto_output_calendar_to_public=person_dict["_auto_output_calendar_to_public"],
    )
    wx._src_calendarlinks = get_calendar_from_calendars_dirlinks_from_dict(
        person_dict["_src_calendarlinks"]
    )
    return wx


def get_calendar_from_calendars_dirlinks_from_dict(
    x_dict: dict,
) -> dict[str:CalendarLink]:
    _src_calendarlinks = {}

    for calendarlink_dict in x_dict.values():
        calendarlink_obj = get_calendar_from_calendars_dirlink_from_dict(
            x_dict=calendarlink_dict
        )
        _src_calendarlinks[calendarlink_obj.calendar_owner] = calendarlink_obj
    return _src_calendarlinks
