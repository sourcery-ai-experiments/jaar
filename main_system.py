# # command to for converting ui form to python file: pyuic5 ui\SystemMainUI.ui -o ui\SystemMainUI.py
from ui.SystemMainUI import Ui_MainWindow
from Edit5Issue import Edit5Issue
from EditMain import EditMainView
from PyQt5 import QtCore as qtc
from src.calendar.calendar import (
    CalendarUnit,
    get_from_json as calendarunit_get_from_json,
)
from sys import argv as sys_argv, exit as sys_exit
from PyQt5.QtWidgets import (
    QTableWidgetItem as qtw1,
    QApplication,
    QMainWindow,
)
from src.system.system import SystemUnit
from src.system.examples.system_env_kit import (
    create_example_systems_list,
    setup_test_example_environment,
    create_example_system,
    delete_dir_example_system,
    rename_example_system,
    get_test_systems_dir,
)

from src.calendar.member import get_depotlink_types
from src.calendar.x_func import (
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from src.pyqt5_kit.pyqt_func import lw_diplay


class MainApp(QApplication):
    """The main application object"""

    def __init__(self, argv):
        super().__init__(argv)

        self.main_window = MainWindow()
        self.main_window.show()

        # create editmain instance
        self.editmain_view = EditMainView()
        # create slot for making editmain visible
        self.main_window.open_editmain.connect(self.editmain_show)

        # create instance
        self.edit5issue_view = Edit5Issue()
        # create slot for making visible
        self.main_window.open_edit5issue.connect(self.edit5issue_show)

    def editmain_show(self):
        if self.main_window.ignore_calendar_x is None:
            self.main_window.isol = (
                self.main_window.person_x._admin.open_isol_calendar()
            )
            self.editmain_view.calendar_x = self.main_window.isol
        else:
            self.editmain_view.calendar_x = self.main_window.ignore_calendar_x
        self.editmain_view.refresh_all()
        self.editmain_view.show()

    def edit5issue_show(self):
        if self.main_window.person_x != None:
            self.edit5issue_view.person_x = self.main_window.person_x
            self.edit5issue_view.refresh_all()
            self.edit5issue_view.show()


class MainWindow(QMainWindow, Ui_MainWindow):
    """The main application window"""

    open_editmain = qtc.pyqtSignal(bool)
    open_edit5issue = qtc.pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        # signals for opening windows
        self.refresh_all_button.clicked.connect(self.refresh_all)
        self.system_insert_button.clicked.connect(self.system_insert)
        self.system_load_button.clicked.connect(self.system_load_from_file)
        self.system_update_button.clicked.connect(self.system_update_name)
        self.system_delete_button.clicked.connect(self.system_delete)
        self.calendar_insert_button.clicked.connect(self.calendar_insert)
        self.calendar_update_button.clicked.connect(self.calendar_update_name)
        self.calendar_delete_button.clicked.connect(self.calendar_delete)
        self.calendars_table.itemClicked.connect(self.calendars_table_select)
        self.person_insert_button.clicked.connect(self.person_insert)
        self.person_update_button.clicked.connect(self.person_update_name)
        self.person_delete_button.clicked.connect(self.person_delete)
        self.persons_table.itemClicked.connect(self.persons_table_select)
        self.reload_all_src_calendars_button.clicked.connect(
            self.reload_all_src_calendars
        )
        self.set_public_calendar_button.clicked.connect(
            self.save_output_calendar_to_public()
        )
        self.set_public_and_reload_srcs_button.clicked.connect(
            self.set_public_and_reload_srcs
        )
        self.ignores_table.itemClicked.connect(self.ignores_table_select)
        self.open_ignore_button.clicked.connect(self.open_editmain)
        self.save_ignore_button.clicked.connect(self.ignore_calendar_file_update)
        self.ignores_table.setHidden(True)
        self.show_ignores_button.clicked.connect(self.show_ignores_table)
        self.show_digests_button.clicked.connect(self.show_digests_table)
        self.isol_open_button.clicked.connect(self.open_editmain)
        self.isol_save_button.clicked.connect(self.save_isol)

        self.depotlink_insert_button.clicked.connect(self.depotlink_insert)
        self.depotlink_update_button.clicked.connect(self.depotlink_update)
        self.depotlink_delete_button.clicked.connect(self.depotlink_delete)
        self.depotlinks_table.itemClicked.connect(self.depotlinks_table_select)
        self.five_issue_button.clicked.connect(self.open_edit5issue)

        self.system_x = None
        self.person_x = None
        self.ignore_calendar_x = None
        setup_test_example_environment()
        first_env = "ex5"
        self.system_x = SystemUnit(name=first_env, systems_dir=get_test_systems_dir())
        self.refresh_system()
        self.system_name_combo_refresh()
        self.system_name_combo.setCurrentText(first_env)
        self._person_load(person_name="ernie")

    def save_isol(self):
        if self.isol != None:
            self.person_x._admin.save_isol_calendar(self.isol)
        self.refresh_person()

    def reload_all_src_calendars(self):
        if self.system_x != None:
            self.system_x.reload_all_persons_src_calendarunits()

    def set_public_and_reload_srcs(self):
        self.save_output_calendar_to_public()
        self.reload_all_src_calendars()

    def save_output_calendar_to_public(self):
        if self.person_x != None:
            self.person_x.save_output_calendar_to_public()
        self.refresh_system()

    def system_load_from_file(self):
        system_selected = self.system_name_combo.currentText()
        self.system_x = SystemUnit(
            name=system_selected, systems_dir=get_test_systems_dir()
        )
        self.system_x.create_dirs_if_null(in_memory_bank=False)
        self.system_name.setText(system_selected)
        self.refresh_system()

    def calendars_table_select(self):
        self.calendar_name.setText(
            self.calendars_table.item(self.calendars_table.currentRow(), 0).text()
        )
        if self.persons_table.currentRow() != -1:
            selected_person = self.persons_table.item(
                self.persons_table.currentRow(), 0
            ).text()
            selected_calendar = self.calendars_table.item(
                self.calendars_table.currentRow(), 0
            ).text()
            self.depotlink_name.setText(f"{selected_person} - {selected_calendar}")

    def persons_table_select(self):
        person_x_name = self.persons_table.item(
            self.persons_table.currentRow(), 0
        ).text()
        self._person_load(person_name=person_x_name)

    def _person_load(self, person_name: str):
        self.system_x.load_personunit(name=person_name)
        self.person_x = self.system_x._personunits.get(person_name)
        self.person_name.setText(self.person_x._admin.name)
        self.refresh_person()

    def depotlinks_table_select(self):
        self.depotlink_name.setText(
            self.depotlinks_table.item(self.depotlinks_table.currentRow(), 0).text()
        )
        self.depotlink_type_combo.setCurrentText(
            self.depotlinks_table.item(self.depotlinks_table.currentRow(), 1).text()
        )
        self.depotlink_weight.setText(
            self.depotlinks_table.item(self.depotlinks_table.currentRow(), 2).text()
        )

    def ignores_table_select(self):
        ignore_calendar_owner = self.ignores_table.item(
            self.ignores_table.currentRow(), 0
        ).text()
        # self.ignore_calendar_x = self.system_x.get_public_calendar(
        self.ignore_calendar_x = self.system_x.get_calendar_from_ignores_dir(
            person_name=self.person_x._admin.name, _owner=ignore_calendar_owner
        )
        self.edit_calendar = self.ignore_calendar_x

    def ignore_calendar_file_update(self):
        self.system_x.set_ignore_calendar_file(
            person_name=self.person_x._admin.name, calendar_obj=self.ignore_calendar_x
        )
        self.refresh_person()

    def show_ignores_table(self):
        self.ignores_table.setHidden(False)
        self.digests_table.setHidden(True)

    def show_digests_table(self):
        self.ignores_table.setHidden(True)
        self.digests_table.setHidden(False)

    def system_insert(self):
        create_example_system(system_name=self.system_name.text())
        self.system_name_combo_refresh()

    def system_update_name(self):
        rename_example_system(
            system_obj=self.system_x, new_name=self.system_name.text()
        )
        self.system_name_combo_refresh()

    def system_delete(self):
        delete_dir_example_system(system_obj=self.system_x)
        self.system_x = None
        self.system_name_combo_refresh()
        self.refresh_system()

    def calendar_insert(self):
        self.system_x.save_public_calendarunit(
            calendar_x=CalendarUnit(_owner=self.calendar_name.text())
        )
        self.refresh_system()

    def calendar_update_name(self):
        currently_selected = self.calendars_table.item(
            self.calendars_table.currentRow(), 0
        ).text()
        typed_in = self.calendar_name.text()
        if currently_selected != typed_in:
            self.system_x.rename_calendar_in_calendars_dir(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_system()

    def calendar_delete(self):
        self.system_x.del_calendarunit_from_calendars_dir(
            calendar_x_label=self.calendars_table.item(
                self.calendars_table.currentRow(), 0
            ).text()
        )
        self.refresh_system()

    def person_insert(self):
        self.system_x.create_new_personunit(person_name=self.person_name.text())
        self.refresh_persons()

    def person_update_name(self):
        currently_selected = self.persons_table.item(
            self.persons_table.currentRow(), 0
        ).text()
        typed_in = self.person_name.text()
        if currently_selected != typed_in:
            self.system_x.rename_personunit(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_persons()

    def person_delete(self):
        self.system_x.del_person_dir(
            person_name=self.persons_table.item(
                self.persons_table.currentRow(), 0
            ).text()
        )
        self.refresh_persons()

    def depotlink_insert(self):
        calendar_owner = self.calendars_table.item(
            self.calendars_table.currentRow(), 0
        ).text()
        if self.person_x != None:
            calendar_json = x_func_open_file(
                dest_dir=self.person_x._admin._calendars_public_dir,
                file_name=f"{calendar_owner}.json",
            )
            calendar_x = calendarunit_get_from_json(calendar_json)
            self.person_x.set_depot_calendar(
                calendar_x=calendar_x,
                depotlink_type=self.depotlink_type_combo.currentText(),
                depotlink_weight=self.depotlink_weight.text(),
            )
            self.system_x.save_person_file(person_name=self.person_x._admin.name)
        self.refresh_person()

    def depotlink_update(self):
        person_name_x = self.person_x._admin.name
        self.system_x.update_depotlink(
            person_name=person_name_x,
            membername=self.depotlink_name.text(),
            depotlink_type=self.depotlink_type_combo.currentText(),
            creditor_weight=self.depotlink_weight.text(),
            debtor_weight=self.depotlink_weight.text(),
        )
        self.system_x.save_person_file(person_name=person_name_x)
        self.refresh_person()

    def depotlink_delete(self):
        person_name_x = self.person_x._admin.name
        self.system_x.del_depotlink(
            person_name=person_name_x, calendarunit_owner=self.depotlink_name.text()
        )
        self.system_x.save_person_file(person_name=person_name_x)
        self.refresh_person()

    def get_calendar_owner_list(self):
        calendars_owner_list = []
        if self.system_x != None:
            calendars_owner_list.extend(
                [calendar._owner]
                for calendar in self.system_x.get_calendars_dir_list_of_obj()
            )
        return calendars_owner_list

    def get_person_name_list(self):
        persons_owner_list = []
        if self.system_x != None:
            persons_owner_list.extend(
                [person_dir] for person_dir in self.system_x.get_person_dir_paths_list()
            )
        return persons_owner_list

    def get_depotlink_list(self):
        depotlinks_list = []
        if self.person_x != None:
            for cl_val in self.person_x._depotlinks.values():
                depotlink_row = [
                    cl_val.calendar_owner,
                    cl_val.depotlink_type,
                    str(cl_val.weight),
                ]
                depotlinks_list.append(depotlink_row)
        return depotlinks_list

    def get_digests_list(self):
        x_list = []
        if self.person_x != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.person_x_admin._calendars_digest_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_ignores_list(self):
        x_list = []
        if self.person_x != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.person_x._admin._calendars_ignore_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_p_ideas_list(self):
        x_list = []
        if self.person_output_calendar != None:
            idea_list = self.person_output_calendar.get_idea_tree_ordered_road_list()

            for idea_road in idea_list:
                idea_obj = self.person_output_calendar.get_idea_kid(idea_road)

                if idea_obj._walk.find("time") != 3:
                    x_list.append(
                        [
                            lw_diplay(idea_obj._calendar_importance),
                            idea_road,
                            len(idea_obj._grouplinks),
                        ]
                    )

        return x_list

    def get_p_members_list(self):
        x_list = []
        if self.person_output_calendar != None:
            x_list.extend(
                [
                    f"{lw_diplay(memberunit._calendar_credit)}/{lw_diplay(memberunit._calendar_debt)}",
                    memberunit.name,
                    f"{memberunit.creditor_weight}/{memberunit.debtor_weight}",
                ]
                for memberunit in self.person_output_calendar._members.values()
            )
        return x_list

    def get_p_groups_list(self):
        x_list = []
        if self.person_output_calendar != None:
            x_list.extend(
                [
                    f"{lw_diplay(groupunit._calendar_debt)}/{lw_diplay(groupunit._calendar_credit)}",
                    groupunit.name,
                    len(groupunit._members),
                ]
                for groupunit in self.person_output_calendar._groups.values()
            )
        return x_list

    def get_p_acptfacts_list(self):
        x_list = []
        if self.person_output_calendar != None:
            for (
                acptfactunit
            ) in self.person_output_calendar._idearoot._acptfactunits.values():
                open_nigh = ""
                if acptfactunit.open is None and acptfactunit.nigh is None:
                    open_nigh = ""
                else:
                    open_nigh = f"{acptfactunit.open}-{acptfactunit.nigh}"

                x_list.append(
                    [
                        acptfactunit.base,
                        acptfactunit.pick.replace(acptfactunit.base, ""),
                        open_nigh,
                    ]
                )
        return x_list

    def get_p_agenda_list(self):
        x_list = []
        if self.person_output_calendar != None:
            agenda_list = self.person_output_calendar.get_agenda_items()
            agenda_list.sort(key=lambda x: x._calendar_importance, reverse=True)
            x_list.extend(
                [
                    lw_diplay(agenda_item._calendar_importance),
                    agenda_item._label,
                    agenda_item._walk,
                ]
                for agenda_item in agenda_list
            )
        return x_list

    def refresh_all(self):
        self.refresh_system()

    def _sub_refresh_persons_table(self):
        self.refresh_x(
            self.persons_table, ["Persons Table"], self.get_person_name_list()
        )

    def _sub_refresh_depotlinks_table(self):
        depotlink_types = list(get_depotlink_types())
        depotlink_types.insert(0, "")
        self.depotlink_type_combo.clear()
        self.depotlink_type_combo.addItems(depotlink_types)
        self.depotlink_type_combo.setCurrentText("")
        column_header = ""
        if self.person_x is None:
            column_header = "Calendarlinks Table"
        elif self.person_x != None:
            column_header = f"'{self.person_x._admin.name}' Calendarlinks"
        self.refresh_x(
            self.depotlinks_table,
            [column_header, "Link Type", "Weight"],
            self.get_depotlink_list(),
        )

    def _sub_refresh_digests_table(self):
        self.refresh_x(self.digests_table, ["digests_table"], self.get_digests_list())

    def _sub_refresh_ignores_table(self):
        ignores_list = self.get_ignores_list()
        if len(ignores_list) >= 0:
            column_headers = [
                f"Ignores Table ({len(ignores_list)})",
            ]
        self.refresh_x(self.ignores_table, column_headers, ignores_list)

    def _sub_refresh_p_ideas_table(self):
        p_ideas_list = self.get_p_ideas_list()
        if len(p_ideas_list) >= 0:
            column_headers = [
                "calendar_importance",
                f"Ideas Table ({len(p_ideas_list)})",
                "grouplinks",
            ]
        else:
            column_headers = [
                "calendar_importance",
                "Ideas Table",
                "grouplinks",
            ]

        self.w_ideas_table.setObjectName("Ideas Table")
        self.w_ideas_table.setColumnHidden(0, False)
        self.w_ideas_table.setColumnHidden(1, False)
        self.w_ideas_table.setColumnHidden(2, False)
        self.refresh_x(
            table_x=self.w_ideas_table,
            column_header=column_headers,
            populate_list=p_ideas_list,
            column_width=[50, 300, 50],
        )

    def _sub_refresh_p_members_table(self):
        p_members_list = self.get_p_members_list()
        column_headers = [
            "calendar_debt/calendar_credit",
            f"Members ({len(p_members_list)})",
            "creditor_weight/debtor_weight",
        ]

        self.refresh_x(
            table_x=self.w_members_table,
            column_header=column_headers,
            populate_list=p_members_list,
            column_width=[50, 300, 50],
        )

    def _sub_refresh_p_groups_table(self):
        p_groups_list = self.get_p_groups_list()
        column_headers = [
            "calendar_debt/calendar_credit",
            f"groups ({len(p_groups_list)})",
            "Members",
        ]

        self.refresh_x(
            table_x=self.w_groups_table,
            column_header=column_headers,
            populate_list=p_groups_list,
            column_width=[50, 300, 100],
        )

    def _sub_refresh_p_acptfacts_table(self):
        p_acptfacts_list = self.get_p_acptfacts_list()
        column_headers = [f"Bases ({len(p_acptfacts_list)})", "AcptFacts", "Open-Nigh"]

        self.refresh_x(
            table_x=self.w_acptfacts_table,
            column_header=column_headers,
            populate_list=p_acptfacts_list,
            column_width=[200, 100, 200],
        )

    def _sub_refresh_p_agenda_table(self):
        p_agenda_list = self.get_p_agenda_list()
        column_headers = [
            "calendar_importance",
            f"Agenda ({len(p_agenda_list)})",
            "Idea Walk",
        ]

        self.refresh_x(
            table_x=self.w_agenda_table,
            column_header=column_headers,
            populate_list=p_agenda_list,
            column_width=[50, 200, 300],
        )

    def system_name_combo_refresh(self):
        self.system_name_combo.clear()
        self.system_name_combo.addItems(create_example_systems_list())

    def refresh_persons(self):
        self.person_x = None
        self._sub_refresh_persons_table()
        self.refresh_person()

    def refresh_person(self):
        self._sub_refresh_depotlinks_table()
        self._sub_refresh_digests_table()
        self._sub_refresh_ignores_table()
        self.person_output_calendar = None
        if self.person_x != None:
            self.person_output_calendar = self.person_x.get_refreshed_output_calendar()
        self._sub_refresh_p_ideas_table()
        self._sub_refresh_p_members_table()
        self._sub_refresh_p_groups_table()
        self._sub_refresh_p_acptfacts_table()
        self._sub_refresh_p_agenda_table()

    def refresh_system(self):
        self.refresh_x(
            self.calendars_table, ["Calendars Table"], self.get_calendar_owner_list()
        )
        self.refresh_persons()

    def refresh_x(
        self,
        table_x,
        column_header: list[str],
        populate_list: list[any],
        column_width: list[int] = None,
    ):
        table_x.setObjectName(column_header[0])
        if column_width is None:
            table_x.setColumnWidth(0, 150)
            table_x.setColumnHidden(0, False)
        else:
            table_x.setColumnWidth(0, column_width[0])
            table_x.setColumnWidth(1, column_width[1])
            table_x.setColumnWidth(2, column_width[2])

        table_x.clear()
        table_x.setHorizontalHeaderLabels(column_header)
        table_x.verticalHeader().setVisible(False)
        table_x.setRowCount(0)
        for row, list_x in enumerate(populate_list):
            table_x.setRowCount(row + 1)
            table_x.setRowHeight(row, 9)
            if len(list_x) == 3:
                table_x.setHorizontalHeaderLabels(column_header)
                table_x.setItem(row, 0, qtw1(str(list_x[0])))
                table_x.setItem(row, 1, qtw1(str(list_x[1])))
                table_x.setItem(row, 2, qtw1(str(list_x[2])))
            elif len(list_x) == 1:
                table_x.setItem(row, 0, qtw1(list_x[0]))


if __name__ == "__main__":
    app = MainApp(sys_argv)
    sys_exit(app.exec())
