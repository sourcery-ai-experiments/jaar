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


class InvalidPersonException(Exception):
    pass


@dataclass
class PersonUnit:
    name: str
    _env_dir: str = None
    _person_dir: str = None
    _public_calendars_dir: str = None
    _person_calendars_dir: str = None
    _ignore_calendars_dir: str = None
    _bond_calendars_dir: str = None
    _digest_calendars_dir: str = None
    _person_file_path: str = None
    _src_calendarlinks: dict[str:CalendarUnit] = None
    _dest_calendar: CalendarUnit = None
    _auto_dest_calendar_to_public_calendar: bool = None

    # dir methods
    def _set_env_dir(self, env_dir: str):
        self._env_dir = env_dir
        self._set_person_dir()
        self._set_calendars_dir()

    def _set_calendars_dir(self):
        self._public_calendars_dir = f"{self._env_dir}/calendars"

    def _set_person_dir(self):
        self._person_dir = f"{self._env_dir}/persons/{self.name}"
        self._set_person_calendars_dir()
        self._set_digest_calendars_dir()
        self._set_ignore_calendars_dir()
        self._set_bond_calendars_dir()
        self._set_person_file_path()

    def _set_person_calendars_dir(self):
        self._person_calendars_dir = f"{self._person_dir}/calendars"

    def get_starting_digest_calendar_file_name(self):
        return "starting_digest_calendar.json"

    def _set_digest_calendars_dir(self):
        self._digest_calendars_dir = f"{self._person_dir}/digests"

    def _set_ignore_calendars_dir(self):
        self._ignore_calendars_dir = f"{self._person_dir}/ignores"

    def _set_bond_calendars_dir(self):
        self._bond_calendars_dir = f"{self._person_dir}/bonds"

    def _set_person_file_path(self) -> str:
        self._person_file_path = f"{self._person_dir}/{self.get_person_file_name()}"

    def get_person_file_name(self) -> str:
        return f"{self.name}.json"

    def create_core_dir_and_files(self):
        single_dir_create_if_null(x_path=self._person_dir)
        single_dir_create_if_null(x_path=self._public_calendars_dir)
        single_dir_create_if_null(x_path=self._person_calendars_dir)
        single_dir_create_if_null(x_path=self._digest_calendars_dir)
        single_dir_create_if_null(x_path=self._ignore_calendars_dir)
        single_dir_create_if_null(x_path=self._bond_calendars_dir)
        x_func_save_file(
            dest_dir=self._person_dir,
            file_name=self.get_person_file_name(),
            file_text=self.get_json(),
            replace=False,
        )

    def set_person_name(self, new_name: str):
        old_name = self.name
        old_person_dir = self._person_dir
        self.name = new_name
        self._set_person_dir()
        old_person_dir_file_path = f"{self._person_dir}/{old_name}.json"

        rename_dir(src=old_person_dir, dst=self._person_dir)
        rename_dir(src=old_person_dir_file_path, dst=self._person_file_path)

    def receive_src_calendarunit_obj(
        self,
        calendar_x: CalendarUnit,
        link_type: str = None,
        calendarlink_weight: float = None,
    ):
        x_func_save_file(
            dest_dir=self._person_calendars_dir,
            file_name=f"{calendar_x._owner}.json",
            file_text=calendar_x.get_json(),
        )
        self._set_src_calendarlinks(
            calendar_owner=calendar_x._owner,
            link_type=link_type,
            weight=calendarlink_weight,
        )

    def receive_src_calendarunit_file(
        self, calendar_json: str, link_type: str = None, weight: float = None
    ):
        calendar_x = calendarunit_get_from_json(lw_json=calendar_json)
        self.receive_src_calendarunit_obj(
            calendar_x=calendar_x, link_type=link_type, calendarlink_weight=weight
        )

    def receive_all_src_calendarunit_files(self):
        for calendarlink_obj in self._src_calendarlinks.values():
            file_name_x = f"{calendarlink_obj.calendar_owner}.json"
            calendar_json = x_func_open_file(self._public_calendars_dir, file_name_x)
            self.receive_src_calendarunit_file(
                calendar_json=calendar_json,
                link_type=calendarlink_obj.link_type,
                weight=calendarlink_obj.weight,
            )

    def _set_src_calendarlinks(
        self, calendar_owner: str, link_type: str = None, weight: float = None
    ):
        self._set_src_calendarlinks_empty_if_null()
        cx_file_name = f"{calendar_owner}.json"
        cx_file_path = f"{self._person_calendars_dir}/{cx_file_name}"
        if not os_path.exists(cx_file_path):
            raise InvalidPersonException(
                f"Person {self.name} cannot find calendar {calendar_owner}"
            )

        # if not calendarlink_x.link_type in list(get_calendarlink_types().keys()):
        #     raise Exception(f"{calendarlink_x.link_type=} not allowed.")
        calendarlink_x = calendarlink_shop(
            calendar_owner=calendar_owner, link_type=link_type, weight=weight
        )

        # if self._src_calendarlinks.get(calendar_owner) is None:
        #     self._src_calendarlinks[calendar_owner] = calendarlink_x
        # elif self._src_calendarlinks.get(calendar_owner) != None:
        #     self._src_calendarlinks[calendar_owner] = calendarlink_x
        self._src_calendarlinks[calendar_owner] = calendarlink_x

        if calendarlink_x.link_type == "blind_trust":
            cx_json = x_func_open_file(self._person_calendars_dir, cx_file_name)
            cx_obj = calendarunit_get_from_json(lw_json=cx_json)
            self._save_digest_calendar_file(
                calendarunit=cx_obj, src_calendar_owner=cx_obj._owner
            )
        elif calendarlink_x.link_type == "ignore":
            new_cx_obj = CalendarUnit(_owner=calendar_owner)
            self.set_ignore_calendar_file(new_cx_obj, new_cx_obj._owner)

    def _set_src_calendarlinks_empty_if_null(self):
        if self._src_calendarlinks is None:
            self._src_calendarlinks = {}

    def delete_calendarlink(self, calendar_owner: str):
        self._src_calendarlinks.pop(calendar_owner)
        x_func_delete_dir(dir=f"{self._person_calendars_dir}/{calendar_owner}.json")
        x_func_delete_dir(dir=f"{self._digest_calendars_dir}/{calendar_owner}.json")

    def _set_auto_dest_calendar_to_public_calendar(
        self, _auto_dest_calendar_to_public_calendar: bool
    ):
        self._auto_dest_calendar_to_public_calendar = (
            _auto_dest_calendar_to_public_calendar
        )

    def _set_emtpy_dest_calendar(self):
        self._dest_calendar = CalendarUnit(_owner="")

    def get_dest_calendar_from_digest_calendar_files(self) -> CalendarUnit:
        return get_meld_of_calendar_files(
            calendarunit=self.get_starting_digest_calendar(),
            dir=self._digest_calendars_dir,
        )

    def set_dest_calendar_to_public_calendar(self):
        dest_calendar = self.get_dest_calendar_from_digest_calendar_files()
        self._save_public_calendar_file(calendarunit=dest_calendar)

    def get_ignore_calendar_from_ignore_calendar_files(
        self, _desc: str
    ) -> CalendarUnit:
        file_name_x = f"{_desc}.json"
        calendar_json = x_func_open_file(self._ignore_calendars_dir, file_name_x)
        calendar_obj = calendarunit_get_from_json(lw_json=calendar_json)
        calendar_obj.set_calendar_metrics()
        return calendar_obj

    def set_ignore_calendar_file(
        self, calendarunit: CalendarUnit, src_calendar_owner: str
    ):
        self._save_ignore_calendar_file(calendarunit, src_calendar_owner)
        cx_file_name = f"{src_calendar_owner}.json"
        cx_2_json = x_func_open_file(self._ignore_calendars_dir, cx_file_name)
        cx_2_obj = calendarunit_get_from_json(lw_json=cx_2_json)
        self._save_digest_calendar_file(
            calendarunit=cx_2_obj, src_calendar_owner=src_calendar_owner
        )

    def _save_ignore_calendar_file(
        self, calendarunit: CalendarUnit, src_calendar_owner: str
    ):
        file_name = f"{src_calendar_owner}.json"
        x_func_save_file(
            dest_dir=self._ignore_calendars_dir,
            file_name=file_name,
            file_text=calendarunit.get_json(),
            replace=True,
        )

    def _save_digest_calendar_file(
        self, calendarunit: CalendarUnit, src_calendar_owner: str
    ):
        file_name = f"{src_calendar_owner}.json"
        x_func_save_file(
            dest_dir=self._digest_calendars_dir,
            file_name=file_name,
            file_text=calendarunit.get_json(),
            replace=True,
        )

        if self._auto_dest_calendar_to_public_calendar:
            self.set_dest_calendar_to_public_calendar()

    def _save_public_calendar_file(self, calendarunit: CalendarUnit):
        file_name = f"{calendarunit._owner}.json"
        x_func_save_file(
            dest_dir=self._public_calendars_dir,
            file_name=file_name,
            file_text=calendarunit.get_json(),
            replace=True,
        )

    def get_starting_digest_calendar(self) -> CalendarUnit:
        cx = None
        try:
            ct = x_func_open_file(self._person_dir, "starting_digest_calendar.json")
            cx = calendarunit_get_from_json(lw_json=ct)
            empty_cx = self._get_empty_starting_digest_calendar()
            cx.calendar_and_idearoot_desc_edit(new_desc=empty_cx._owner)
            cx.set_calendar_metrics()
        except Exception:
            cx = self._get_empty_starting_digest_calendar()
            cx.set_calendar_metrics()
        return cx

    def _get_empty_starting_digest_calendar(self):
        return CalendarUnit(_owner=self.name, _weight=0)

    def set_starting_digest_calendar(self, calendarunit: CalendarUnit):
        x_func_save_file(
            dest_dir=self._person_dir,
            file_name="starting_digest_calendar.json",
            file_text=calendarunit.get_json(),
            replace=True,
        )

    def del_starting_digest_calendar_file(self):
        file_path = (
            f"{self._person_dir}/{self.get_starting_digest_calendar_file_name()}"
        )
        x_func_delete_dir(dir=file_path)

    def get_dict(self):
        return {
            "name": self.name,
            "_env_dir": self._env_dir,
            "_person_dir": self._person_dir,
            "_public_calendars_dir": self._public_calendars_dir,
            "_digest_calendars_dir": self._digest_calendars_dir,
            "_src_calendarlinks": self.get_calendar_from_calendars_dirlinks_dict(),
            "_dest_calendar": self._dest_calendar.get_dict(),
            "_auto_dest_calendar_to_public_calendar": self._auto_dest_calendar_to_public_calendar,
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
    name: str, env_dir: str, _auto_dest_calendar_to_public_calendar: bool = None
) -> PersonUnit:
    person_x = PersonUnit(name=name)
    person_x._set_env_dir(env_dir=env_dir)
    person_x._set_auto_dest_calendar_to_public_calendar(
        _auto_dest_calendar_to_public_calendar
    )
    person_x._set_src_calendarlinks_empty_if_null()
    person_x._set_emtpy_dest_calendar()
    return person_x


def get_from_json(person_json: str) -> PersonUnit:
    return get_from_dict(person_dict=json_loads(person_json))


def get_from_dict(person_dict: dict) -> PersonUnit:
    wx = personunit_shop(
        name=person_dict["name"],
        env_dir=person_dict["_env_dir"],
        _auto_dest_calendar_to_public_calendar=person_dict[
            "_auto_dest_calendar_to_public_calendar"
        ],
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
