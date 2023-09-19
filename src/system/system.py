from src.calendar.calendar import CalendarUnit, get_from_json as get_calendar_from_json
from src.calendar.member import memberlink_shop, MemberName
from src.system.author import AuthorUnit, authorunit_shop
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
    _authorunits: dict[str:AuthorUnit] = None
    _bank_db = None

    def set_calendar_bank_attrs(self, calendar_name: str):
        calendar_obj = self.get_public_calendar(calendar_name)

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
        self.save_public_calendar(calendar_obj)

        # refresh bank metrics
        self.refresh_bank_metrics()

    # banking
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
            calendar_x = self.get_public_calendar(owner=calendar_name)
            calendar_x.set_banking_attr_memberunits(sal_river_tmembers)
            self.save_public_calendar(calendar_x=calendar_x)

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
        for file_name in self.get_public_dir_file_names_list():
            calendar_json = x_func_open_file(self.get_public_dir(), file_name)
            calendarunit_x = get_calendar_from_json(cx_json=calendar_json)
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
        calendars_dir = self.get_public_dir()
        authors_dir = self.get_authors_dir()
        single_dir_create_if_null(x_path=system_dir)
        single_dir_create_if_null(x_path=calendars_dir)
        single_dir_create_if_null(x_path=authors_dir)
        self._create_main_file_if_null(x_dir=system_dir)
        self._create_bank_db(in_memory=in_memory_bank, overwrite=True)

    # AuthorUnit management
    def get_authors_dir(self):
        return f"{self.get_object_root_dir()}/authors"

    def get_author_dir_paths_list(self):
        return list(
            x_func_dir_files(
                dir_path=self.get_authors_dir(),
                remove_extensions=False,
                include_dirs=True,
            ).keys()
        )

    def set_authorunits_empty_if_null(self):
        if self._authorunits is None:
            self._authorunits = {}

    def create_new_authorunit(self, author_name: str):
        self.set_authorunits_empty_if_null()
        ux = authorunit_shop(name=author_name, env_dir=self.get_object_root_dir())
        ux.create_core_dir_and_files()
        self._authorunits[ux._admin._author_name] = ux

    def get_author_obj(self, name: str) -> AuthorUnit:
        return None if self._authorunits.get(name) is None else self._authorunits[name]

    def create_authorunit_from_public(self, name: str):
        cx = self.get_public_calendar(owner=name)
        author_x = authorunit_shop(name=cx._owner, env_dir=self.get_object_root_dir())
        self.set_authorunits_empty_if_null()
        self.set_authorunit_to_system(author_x)

    def set_authorunit_to_system(self, author: AuthorUnit):
        self._authorunits[author._admin._author_name] = author
        self.save_author_file(author_name=author._admin._author_name)

    def save_author_file(self, author_name: str):
        author_x = self.get_author_obj(name=author_name)
        author_x._admin.save_isol_calendar(author_x.get_isol())

    def rename_authorunit(self, old_name: str, new_name: str):
        author_x = self.get_author_obj(name=old_name)
        old_author_dir = author_x._admin._author_dir
        author_x._admin.set_author_name(new_name=new_name)
        self.set_authorunit_to_system(author=author_x)
        x_func_delete_dir(old_author_dir)
        self.del_author_from_system(author_name=old_name)

    def del_author_from_system(self, author_name):
        self._authorunits.pop(author_name)

    def del_author_dir(self, author_name: str):
        x_func_delete_dir(f"{self.get_authors_dir()}/{author_name}")

    # public dir management
    def get_public_dir(self):
        return f"{self.get_object_root_dir()}/calendars"

    def get_ignores_dir(self, author_name: str):
        per_x = self.get_author_obj(author_name)
        return per_x._admin._calendars_ignore_dir

    def get_public_calendar(self, owner: str) -> CalendarUnit:
        return get_calendar_from_json(
            x_func_open_file(dest_dir=self.get_public_dir(), file_name=f"{owner}.json")
        )

    def get_calendar_from_ignores_dir(
        self, author_name: str, _owner: str
    ) -> CalendarUnit:
        return get_calendar_from_json(
            x_func_open_file(
                dest_dir=self.get_ignores_dir(author_name=author_name),
                file_name=f"{_owner}.json",
            )
        )

    def set_ignore_calendar_file(self, author_name: str, calendar_obj: CalendarUnit):
        author_x = self.get_author_obj(name=author_name)
        author_x.set_ignore_calendar_file(
            calendarunit=calendar_obj, src_calendar_owner=calendar_obj._owner
        )

    def rename_public_calendar(self, old_owner: str, new_owner: str):
        calendar_x = self.get_public_calendar(owner=old_owner)
        calendar_x.set_owner(new_owner=new_owner)
        self.save_public_calendar(calendar_x=calendar_x)
        self.del_public_calendar(calendar_x_owner=old_owner)

    def del_public_calendar(self, calendar_x_owner: str):
        x_func_delete_dir(f"{self.get_public_dir()}/{calendar_x_owner}.json")

    def save_public_calendar(self, calendar_x: CalendarUnit):
        x_func_save_file(
            dest_dir=self.get_public_dir(),
            file_name=f"{calendar_x._owner}.json",
            file_text=calendar_x.get_json(),
        )

    def reload_all_authors_src_calendarunits(self):
        for author_x in self._authorunits.values():
            author_x.refresh_depot_calendars()

    def get_public_dir_file_names_list(self):
        return list(x_func_dir_files(dir_path=self.get_public_dir()).keys())

    # calendars_dir to author_calendars_dir management
    def _author_set_depot_calendar(
        self,
        authorunit: AuthorUnit,
        calendarunit: CalendarUnit,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_calendar: CalendarUnit = None,
    ):
        authorunit.set_depot_calendar(
            calendar_x=calendarunit,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )
        if depotlink_type == "ignore" and ignore_calendar != None:
            authorunit.set_ignore_calendar_file(
                calendarunit=ignore_calendar, src_calendar_owner=calendarunit._owner
            )

    def set_author_depotlink(
        self,
        author_name: str,
        calendar_owner: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
        ignore_calendar: CalendarUnit = None,
    ):
        author_x = self.get_author_obj(name=author_name)
        calendar_x = self.get_public_calendar(owner=calendar_owner)
        self._author_set_depot_calendar(
            authorunit=author_x,
            calendarunit=calendar_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
            ignore_calendar=ignore_calendar,
        )

    def create_depotlink_to_generated_calendar(
        self,
        author_name: str,
        calendar_owner: str,
        depotlink_type: str,
        creditor_weight: float = None,
        debtor_weight: float = None,
    ):
        author_x = self.get_author_obj(name=author_name)
        calendar_x = CalendarUnit(_owner=calendar_owner)
        self._author_set_depot_calendar(
            authorunit=author_x,
            calendarunit=calendar_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def update_depotlink(
        self,
        author_name: str,
        membername: MemberName,
        depotlink_type: str,
        creditor_weight: str,
        debtor_weight: str,
    ):
        author_x = self.get_author_obj(name=author_name)
        calendar_x = self.get_public_calendar(_owner=membername)
        self._author_set_depot_calendar(
            authorunit=author_x,
            calendarunit=calendar_x,
            depotlink_type=depotlink_type,
            creditor_weight=creditor_weight,
            debtor_weight=debtor_weight,
        )

    def del_depotlink(self, author_name: str, calendarunit_owner: str):
        author_x = self.get_author_obj(name=author_name)
        author_x.del_depot_calendar(calendar_owner=calendarunit_owner)

    # Author output_calendar
    def get_output_calendar(self, author_name: str) -> CalendarUnit:
        author_x = self.get_author_obj(name=author_name)
        return author_x._admin.get_remelded_output_calendar()


def systemunit_shop(
    name: str,
    systems_dir: str,
    _authorunits: dict[str:AuthorUnit] = None,
    in_memory_bank: bool = None,
):
    if in_memory_bank is None:
        in_memory_bank = True
    system_x = SystemUnit(name=name, systems_dir=systems_dir, _authorunits=_authorunits)
    system_x.create_dirs_if_null(in_memory_bank=in_memory_bank)
    return system_x
