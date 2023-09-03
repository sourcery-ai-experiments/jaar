from src.calendar.calendar import CalendarUnit, get_from_json as get_calendar_from_json
from src.calendar.member import memberlink_shop
from src.system.person import (
    PersonUnit,
    personunit_shop,
    get_from_json as get_person_from_json,
)
from src.system.calendarlink import CalendarLink
from dataclasses import dataclass
from src.calendar.x_func import (
    single_dir_create_if_null,
    delete_dir as x_func_delete_dir,
    save_file as x_func_save_file,
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from sqlite3 import connect as sqlite3_connect, Connection
from src.system.bank_sqlstr import (
    get_river_flow_table_delete_sqlstr,
    get_river_flow_table_insert_sqlstr,
    get_river_tmember_table_delete_sqlstr,
    get_river_tmember_table_insert_sqlstr,
    get_river_tmember_dict,
    get_river_bucket_table_insert_sqlstr,
    get_create_table_if_not_exist_sqlstrs,
    get_ledger_table_insert_sqlstr,
    get_calendar_table_insert_sqlstr,
    get_river_ledger_unit,
    LedgerUnit,
    RiverLedgerUnit,
    RiverFlowUnit,
    RiverTmemberUnit,
    IdeaCatalog,
    get_idea_catalog_table_insert_sqlstr,
    get_idea_catalog_dict,
    AcptFactCatalog,
    get_acptfact_catalog_table_insert_sqlstr,
    GroupUnitCatalog,
    get_groupunit_catalog_table_insert_sqlstr,
    get_groupunit_catalog_dict,
)


@dataclass
class SystemUnit:
    name: str
    systems_dir: str
    _personunits: dict[str:PersonUnit] = None
    _bank_db = None

    def set_calendar_attr_defined_by_system(self, calendar_name: str):
        calendar_obj = self.get_calendar_from_calendars_dir(calendar_name)

        for groupunit_x in calendar_obj._groups.values():
            if groupunit_x._memberlinks_set_by_system_road != None:
                groupunit_x.clear_memberlinks()
                ic = get_idea_catalog_dict(
                    self.get_bank_conn(), groupunit_x._memberlinks_set_by_system_road
                )
                for idea_catalog in ic.values():
                    if calendar_name != idea_catalog.calendar_name:
                        memberlink_x = memberlink_shop(name=idea_catalog.calendar_name)
                        groupunit_x.set_memberlink(memberlink_x)
        self.save_calendarunit_obj_to_calendars_dir(calendar_obj)

        # refresh bank metrics
        self.refresh_bank_metrics()

    # figure out who is paying taxes and how much
    def set_river_sphere_for_calendar(
        self, calendar_name: str, max_flows_count: int = None
    ):
        self._clear_all_source_river_data(calendar_name)
        general_bucket = [self._get_root_river_ledger_unit(calendar_name)]

        if max_flows_count is None:
            max_flows_count = 40

        flows_count = 0
        while flows_count < max_flows_count and general_bucket != []:
            parent_calendar_ledger = general_bucket.pop(0)

            parent_range = parent_calendar_ledger.get_range()
            parent_close = parent_calendar_ledger.currency_cease
            curr_onset = parent_calendar_ledger.currency_onset

            ledgers_len = len(parent_calendar_ledger._ledgers.values())
            ledgers_count = 0
            for led_x in parent_calendar_ledger._ledgers.values():
                ledgers_count += 1

                curr_range = parent_range * led_x._calendar_agenda_ratio_credit
                curr_close = curr_onset + curr_range

                # implies last element in dict
                if ledgers_count == ledgers_len and curr_close != parent_close:
                    curr_close = parent_close

                river_flow_x = RiverFlowUnit(
                    currency_calendar_name=calendar_name,
                    src_name=led_x.calendar_name,
                    dst_name=led_x.member_name,
                    currency_start=curr_onset,
                    currency_close=curr_close,
                    flow_num=flows_count,
                    parent_flow_num=parent_calendar_ledger.flow_num,
                    river_tree_level=parent_calendar_ledger.river_tree_level + 1,
                )
                river_ledger_x = self._insert_river_flow_grab_river_ledger(river_flow_x)
                if river_ledger_x != None:
                    general_bucket.append(river_ledger_x)

                flows_count += 1
                if flows_count >= max_flows_count:
                    break

                # change curr_onset for next
                curr_onset += curr_range

        self._set_river_tmembers_buckets(calendar_name)

    def _insert_river_flow_grab_river_ledger(
        self, river_flow_x: RiverFlowUnit
    ) -> RiverLedgerUnit:
        river_ledger_x = None

        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_flow_table_insert_sqlstr(river_flow_x))

            if river_flow_x.flow_returned() == False:
                river_ledger_x = get_river_ledger_unit(bank_conn, river_flow_x)

        return river_ledger_x

    def _clear_all_source_river_data(self, calendar_name: str):
        with self.get_bank_conn() as bank_conn:
            flow_s = get_river_flow_table_delete_sqlstr(calendar_name)
            mstr_s = get_river_tmember_table_delete_sqlstr(calendar_name)
            bank_conn.execute(flow_s)
            bank_conn.execute(mstr_s)

    def _get_root_river_ledger_unit(self, calendar_name: str) -> RiverLedgerUnit:
        default_currency_onset = 0.0
        default_currency_cease = 1.0
        default_root_river_tree_level = 0
        default_root_flow_num = None  # maybe change to 1?
        default_root_parent_flow_num = None
        root_river_flow = RiverFlowUnit(
            currency_calendar_name=calendar_name,
            src_name=None,
            dst_name=calendar_name,
            currency_start=default_currency_onset,
            currency_close=default_currency_cease,
            flow_num=default_root_flow_num,
            parent_flow_num=default_root_parent_flow_num,
            river_tree_level=default_root_river_tree_level,
        )
        with self.get_bank_conn() as bank_conn:
            source_river_ledger = get_river_ledger_unit(bank_conn, root_river_flow)
        return source_river_ledger

    def _set_river_tmembers_buckets(self, calendar_name: str):
        with self.get_bank_conn() as bank_conn:
            bank_conn.execute(get_river_tmember_table_insert_sqlstr(calendar_name))
            bank_conn.execute(get_river_bucket_table_insert_sqlstr(calendar_name))

            sal_river_tmembers = get_river_tmember_dict(bank_conn, calendar_name)
            calendar_x = self.get_calendar_from_calendars_dir(owner=calendar_name)
            calendar_x.set_banking_attr_memberunits(sal_river_tmembers)
            self.save_calendarunit_obj_to_calendars_dir(calendar_x=calendar_x)

    def get_river_tmembers(self, calendar_name: str) -> dict[str:RiverTmemberUnit]:
        with self.get_bank_conn() as bank_conn:
            river_tmembers = get_river_tmember_dict(bank_conn, calendar_name)
        return river_tmembers

    def refresh_bank_metrics(self, in_memory: bool = None):
        if in_memory is None and self._bank_db != None:
            in_memory = True
        self._create_bank_db(in_memory=in_memory, overwrite=True)
        self._bank_populate_calendars_data()

    def _bank_populate_calendars_data(self):
        for file_name in self.get_calendars_dir_file_names_list():
            calendar_json = x_func_open_file(self.get_calendars_dir(), file_name)
            calendarunit_x = get_calendar_from_json(lw_json=calendar_json)
            calendarunit_x.set_calendar_metrics()

            self._bank_insert_calendarunit(calendarunit_x)
            self._bank_insert_memberunit(calendarunit_x)
            self._bank_insert_groupunit(calendarunit_x)
            self._bank_insert_ideaunit(calendarunit_x)
            self._bank_insert_acptfact(calendarunit_x)

    def _bank_insert_calendarunit(self, calendarunit_x: CalendarUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            cur.execute(get_calendar_table_insert_sqlstr(calendar_x=calendarunit_x))

    def _bank_insert_memberunit(self, calendarunit_x: CalendarUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for memberunit_x in calendarunit_x._members.values():
                sqlstr = get_ledger_table_insert_sqlstr(calendarunit_x, memberunit_x)
                cur.execute(sqlstr)

    def _bank_insert_groupunit(self, calendarunit_x: CalendarUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for groupunit_x in calendarunit_x._groups.values():
                groupunit_catalog_x = GroupUnitCatalog(
                    calendar_name=calendarunit_x._owner,
                    groupunit_name=groupunit_x.name,
                    memberlinks_set_by_system_road=groupunit_x._memberlinks_set_by_system_road,
                )
                sqlstr = get_groupunit_catalog_table_insert_sqlstr(groupunit_catalog_x)
                cur.execute(sqlstr)

    def _bank_insert_ideaunit(self, calendarunit_x: CalendarUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for idea_x in calendarunit_x._idea_dict.values():
                idea_catalog_x = IdeaCatalog(calendarunit_x._owner, idea_x.get_road())
                sqlstr = get_idea_catalog_table_insert_sqlstr(idea_catalog_x)
                cur.execute(sqlstr)

    def _bank_insert_acptfact(self, calendarunit_x: CalendarUnit):
        with self.get_bank_conn() as bank_conn:
            cur = bank_conn.cursor()
            for acptfact_x in calendarunit_x._idearoot._acptfactunits.values():
                acptfact_catalog_x = AcptFactCatalog(
                    calendar_name=calendarunit_x._owner,
                    base=acptfact_x.base,
                    pick=acptfact_x.pick,
                )
                sqlstr = get_acptfact_catalog_table_insert_sqlstr(acptfact_catalog_x)
                cur.execute(sqlstr)

    def get_bank_conn(self) -> Connection:
        if self._bank_db is None:
            return sqlite3_connect(self.get_bank_db_path())
        else:
            return self._bank_db

    def _create_bank_db(
        self, in_memory: bool = None, overwrite: bool = None
    ) -> Connection:
        if overwrite:
            self._delete_bank()

        bank_file_new = True
        if in_memory:
            self._bank_db = sqlite3_connect(":memory:")
        else:
            sqlite3_connect(self.get_bank_db_path())

        if bank_file_new:
            with self.get_bank_conn() as bank_conn:
                for sqlstr in get_create_table_if_not_exist_sqlstrs():
                    bank_conn.execute(sqlstr)

    def _delete_bank(self):
        self._bank_db = None
        x_func_delete_dir(dir=self.get_bank_db_path())

    def set_systemunit_name(self, name: str):
        self.name = name

    def get_bank_db_path(self):
        return f"{self.get_object_root_dir()}/bank.db"

    def get_object_root_dir(self):
        return f"{self.systems_dir}/{self.name}"

    def _create_main_file_if_null(self, x_dir):
        system_file_name = "system.json"
        x_func_save_file(
            dest_dir=x_dir,
            file_name=system_file_name,
            file_text="",
        )

    def create_dirs_if_null(self, in_memory_bank: bool = None):
        system_dir = self.get_object_root_dir()
        calendars_dir = self.get_calendars_dir()
        persons_dir = self.get_persons_dir()
        single_dir_create_if_null(x_path=system_dir)
        single_dir_create_if_null(x_path=calendars_dir)
        single_dir_create_if_null(x_path=persons_dir)
        self._create_main_file_if_null(x_dir=system_dir)
        self._create_bank_db(in_memory=in_memory_bank, overwrite=True)

    # PersonUnit management
    def get_persons_dir(self):
        return f"{self.get_object_root_dir()}/persons"

    def get_person_dir_paths_list(self):
        return list(
            x_func_dir_files(
                dir_path=self.get_persons_dir(),
                remove_extensions=False,
                include_dirs=True,
            ).keys()
        )

    def set_personunits_empty_if_null(self):
        if self._personunits is None:
            self._personunits = {}

    def create_new_personunit(self, person_name: str):
        self.set_personunits_empty_if_null()
        px = personunit_shop(name=person_name, env_dir=self.get_object_root_dir())
        px.create_core_dir_and_files()
        self._personunits[px.name] = px

    def get_person_obj_from_system(self, name: str) -> PersonUnit:
        return None if self._personunits.get(name) is None else self._personunits[name]

    def get_person_obj_from_file(self, name: str) -> PersonUnit:
        person_json = x_func_open_file(
            dest_dir=f"{self.get_persons_dir()}/{name}", file_name=f"{name}.json"
        )
        return get_person_from_json(person_json=person_json)

    def load_personunit(self, name: str):
        person_x = self.get_person_obj_from_file(name=name)
        self.set_personunits_empty_if_null()
        self.set_personunit_to_system(person_x)

    def set_personunit_to_system(self, person: PersonUnit):
        self._personunits[person.name] = person
        self.save_person_file(person_name=person.name)

    def save_person_file(self, person_name: str):
        person_x = self.get_person_obj_from_system(name=person_name)
        x_func_save_file(
            dest_dir=person_x._person_dir,
            file_name=person_x.get_person_file_name(),
            file_text=person_x.get_json(),
        )

    def rename_personunit(self, old_name: str, new_name: str):
        person_x = self.get_person_obj_from_system(name=old_name)
        old_person_dir = person_x._person_dir
        person_x.set_person_name(new_name=new_name)
        self.set_personunit_to_system(person=person_x)
        x_func_delete_dir(old_person_dir)
        self.del_person_from_system(person_name=old_name)

    def del_person_from_system(self, person_name):
        self._personunits.pop(person_name)

    def del_person_dir(self, person_name: str):
        x_func_delete_dir(f"{self.get_persons_dir()}/{person_name}")

    # calendars_dir management
    def get_calendars_dir(self):
        return f"{self.get_object_root_dir()}/calendars"

    def get_ignores_dir(self, person_name: str):
        return f"{self.get_persons_dir()}/{person_name}/ignores"

    def get_calendar_from_calendars_dir(self, owner: str) -> CalendarUnit:
        return get_calendar_from_json(
            x_func_open_file(
                dest_dir=self.get_calendars_dir(), file_name=f"{owner}.json"
            )
        )

    def get_calendar_from_ignores_dir(
        self, person_name: str, _owner: str
    ) -> CalendarUnit:
        return get_calendar_from_json(
            x_func_open_file(
                dest_dir=self.get_ignores_dir(person_name=person_name),
                file_name=f"{_owner}.json",
            )
        )

    def set_ignore_calendar_file(self, person_name: str, calendar_obj: CalendarUnit):
        person_x = self.get_person_obj_from_system(name=person_name)
        person_x.set_ignore_calendar_file(
            calendarunit=calendar_obj, src_calendar_owner=calendar_obj._owner
        )

    def rename_calendar_in_calendars_dir(self, old_owner: str, new_owner: str):
        calendar_x = self.get_calendar_from_calendars_dir(owner=old_owner)
        calendar_x.calendar_and_idearoot_desc_edit(new_owner=new_owner)
        self.save_calendarunit_obj_to_calendars_dir(calendar_x=calendar_x)
        self.del_calendarunit_from_calendars_dir(calendar_x_owner=old_owner)

    def del_calendarunit_from_calendars_dir(self, calendar_x_owner: str):
        x_func_delete_dir(f"{self.get_calendars_dir()}/{calendar_x_owner}.json")

    def save_calendarunit_obj_to_calendars_dir(self, calendar_x: CalendarUnit):
        x_func_save_file(
            dest_dir=self.get_calendars_dir(),
            file_name=f"{calendar_x._owner}.json",
            file_text=calendar_x.get_json(),
        )

    def reload_all_persons_src_calendarunits(self):
        for person_x in self._personunits.values():
            person_x.receive_all_src_calendarunit_files()

    def get_calendars_dir_file_names_list(self):
        return list(x_func_dir_files(dir_path=self.get_calendars_dir()).keys())

    def get_calendars_dir_list_of_obj(self):
        calendars_list = []

        for file_name in self.get_calendars_dir_file_names_list():
            calendar_json = x_func_open_file(
                dest_dir=self.get_calendars_dir(), file_name=file_name
            )
            calendars_list.append(get_calendar_from_json(lw_json=calendar_json))

        return calendars_list

    # calendars_dir to person_calendars_dir management
    def _person_receive_src_calendarunit_obj(
        self,
        personunit: PersonUnit,
        calendarunit: CalendarUnit,
        link_type: str = None,
        weight: float = None,
        ignore_calendar: CalendarUnit = None,
    ):
        personunit.receive_src_calendarunit_obj(
            calendar_x=calendarunit, link_type=link_type, calendarlink_weight=weight
        )
        if link_type == "ignore" and ignore_calendar != None:
            personunit.set_ignore_calendar_file(
                calendarunit=ignore_calendar, src_calendar_owner=calendarunit._owner
            )

    def _person_delete_src_calendarunit_obj(
        self, personunit: PersonUnit, calendarunit_owner: str
    ):
        personunit.delete_calendarlink(calendar_owner=calendarunit_owner)

    def create_calendarlink_to_saved_calendar(
        self,
        person_name: str,
        calendar_owner: str,
        link_type: str = None,
        weight: float = None,
        ignore_calendar: CalendarUnit = None,
    ):
        person_x = self.get_person_obj_from_system(name=person_name)
        calendar_x = self.get_calendar_from_calendars_dir(owner=calendar_owner)
        self._person_receive_src_calendarunit_obj(
            personunit=person_x,
            calendarunit=calendar_x,
            link_type=link_type,
            weight=weight,
            ignore_calendar=ignore_calendar,
        )

    def create_calendarlink_to_generated_calendar(
        self,
        person_name: str,
        calendar_owner: str,
        link_type: str = None,
        weight: float = None,
    ):
        person_x = self.get_person_obj_from_system(name=person_name)
        calendar_x = CalendarUnit(_owner=calendar_owner)
        self._person_receive_src_calendarunit_obj(
            personunit=person_x,
            calendarunit=calendar_x,
            link_type=link_type,
            weight=weight,
        )

    def update_calendarlink(self, person_name: str, calendarlink: CalendarLink):
        person_x = self.get_person_obj_from_system(name=person_name)
        calendar_x = self.get_calendar_from_calendars_dir(
            _owner=calendarlink.calendar_owner
        )
        self._person_receive_src_calendarunit_obj(
            personunit=person_x,
            calendarunit=calendar_x,
            link_type=calendarlink.link_type,
            weight=calendarlink.weight,
        )

    def del_calendarlink(self, person_name: str, calendarunit_owner: str):
        person_x = self.get_person_obj_from_system(name=person_name)
        calendar_x = self.get_calendar_from_calendars_dir(owner=calendarunit_owner)
        self._person_delete_src_calendarunit_obj(
            personunit=person_x,
            calendarunit_owner=calendarunit_owner,
        )

    # Person dest_calendar
    def get_person_dest_calendar_from_digest_calendar_files(
        self, person_name: str
    ) -> CalendarUnit:
        person_x = self.get_person_obj_from_system(name=person_name)
        return person_x.get_dest_calendar_from_digest_calendar_files()
