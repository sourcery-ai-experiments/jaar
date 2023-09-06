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

    def init_isol_calendar(self) -> CalendarUnit:
        return x_func_open_file(self._person_dir, self._isol_calendar_file_name)

    def init_ignore_calendar(self, _label: str) -> CalendarUnit:
        ignore_file_name = f"{_label}.json"
        calendar_json = x_func_open_file(self._calendars_ignore_dir, ignore_file_name)
        calendar_obj = calendarunit_get_from_json(cx_json=calendar_json)
        calendar_obj.set_calendar_metrics()
        return calendar_obj

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

    def set_person_name(self, new_name: str):
        self._admin.set_person_name(new_name=new_name)

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
            file_name_x = f"{calendarlink_obj.calendar_owner}.json"
            calendar_json = x_func_open_file(
                self._admin._calendars_public_dir, file_name_x
            )
            self.receive_src_calendarunit_file(
                calendar_json=calendar_json,
                link_type=calendarlink_obj.link_type,
                weight=calendarlink_obj.weight,
            )

    def set_src_calendarlinks(
        self, calendar_owner: str, link_type: str = None, weight: float = None
    ):
        self.set_src_calendarlinks_empty_if_null()
        cx_file_name = f"{calendar_owner}.json"
        cx_file_path = f"{self._admin._calendars_depot_dir}/{cx_file_name}"
        if not os_path.exists(cx_file_path):
            raise InvalidPersonException(
                f"Person {self._admin._person_name} cannot find calendar {calendar_owner} in {cx_file_path}"
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
            cx_json = x_func_open_file(self._admin._calendars_depot_dir, cx_file_name)
            cx_obj = calendarunit_get_from_json(cx_json=cx_json)
            self._admin.save_calendar_to_digest(cx_obj)
        elif calendarlink_x.link_type == "ignore":
            new_cx_obj = CalendarUnit(_owner=calendar_owner)
            self.set_ignore_calendar_file(new_cx_obj, new_cx_obj._owner)

    def set_src_calendarlinks_empty_if_null(self):
        if self._src_calendarlinks is None:
            self._src_calendarlinks = {}

    def delete_calendarlink(self, calendar_owner: str):
        self._src_calendarlinks.pop(calendar_owner)
        x_func_delete_dir(
            dir=f"{self._admin._calendars_depot_dir}/{calendar_owner}.json"
        )
        x_func_delete_dir(
            dir=f"{self._admin._calendars_digest_dir}/{calendar_owner}.json"
        )

    def _set_auto_output_calendar_to_public(self, bool_x: bool):
        self._auto_output_calendar_to_public = bool_x

    def _set_emtpy_output_calendar(self):
        self._output_calendar = CalendarUnit(_owner="")

    def get_output_from_digest_calendar_files(self) -> CalendarUnit:
        return get_meld_of_calendar_files(
            cx_primary=self.get_isol_digest_calendar(),
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
        self._save_ignore_calendar_file(calendarunit, src_calendar_owner)
        cx_file_name = f"{src_calendar_owner}.json"
        cx_2_json = x_func_open_file(self._admin._calendars_ignore_dir, cx_file_name)
        cx_2_obj = calendarunit_get_from_json(cx_json=cx_2_json)
        self._admin.save_calendar_to_digest(cx_2_obj, src_calendar_owner)

    def _save_ignore_calendar_file(
        self, calendarunit: CalendarUnit, src_calendar_owner: str
    ):
        file_name = f"{src_calendar_owner}.json"
        x_func_save_file(
            dest_dir=self._admin._calendars_ignore_dir,
            file_name=file_name,
            file_text=calendarunit.get_json(),
            replace=True,
        )

        if self._auto_output_calendar_to_public:
            self.save_output_calendar_to_public_dir()

    def get_isol_digest_calendar(self) -> CalendarUnit:
        cx = None
        try:
            ct = self._admin.init_isol_calendar()
            cx = calendarunit_get_from_json(cx_json=ct)
            empty_cx = self._get_empty_isol_digest_calendar()
            cx.calendar_owner_edit(new_owner=empty_cx._owner)
            cx.set_calendar_metrics()
        except Exception:
            cx = self._get_empty_isol_digest_calendar()
            cx.set_calendar_metrics()
        return cx

    def _get_empty_isol_digest_calendar(self):
        return CalendarUnit(_owner=self._admin._person_name, _weight=0)

    def set_isol_digest_calendar(self, calendarunit: CalendarUnit):
        x_func_save_file(
            dest_dir=self._admin._person_dir,
            file_name=self._admin._isol_calendar_file_name,
            file_text=calendarunit.get_json(),
            replace=True,
        )

    def del_isol_digest_calendar_file(self):
        file_path = f"{self._admin._person_dir}/{self._admin._isol_calendar_file_name}"
        x_func_delete_dir(dir=file_path)

    def get_dict(self):
        return {
            "name": self._admin._person_name,
            "_env_dir": self._admin._env_dir,
            "_person_dir": self._admin._person_dir,
            "_public_calendars_dir": self._admin._calendars_public_dir,
            "_digest_calendars_dir": self._admin._calendars_digest_dir,
            "_src_calendarlinks": self.get_calendar_from_calendars_dirlinks_dict(),
            "_output_calendar": self._output_calendar.get_dict(),
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


def get_from_json(person_json: str) -> PersonUnit:
    return get_from_dict(person_dict=json_loads(person_json))


def get_from_dict(person_dict: dict) -> PersonUnit:
    wx = personunit_shop(
        name=person_dict["name"],
        env_dir=person_dict["_env_dir"],
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
