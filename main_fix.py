# # command to for converting ui form to python file: pyuic5 ui\cultureMainUI.ui -o ui\cultureMainUI.py
from ui.CultureMainUI import Ui_MainWindow
from Edit5Issue import Edit5Issue
from EditMain import EditMainView
from PyQt5 import QtCore as qtc
from src.agenda.agenda import (
    AgendaUnit,
    get_from_json as get_agenda_from_json,
)
from sys import argv as sys_argv, exit as sys_exit
from PyQt5.QtWidgets import (
    QTableWidgetItem as qtw1,
    QApplication,
    QMainWindow,
)
from src.culture.culture import cultureunit_shop
from src.culture.examples.culture_env_kit import (
    create_example_cultures_list,
    setup_test_example_environment,
    create_example_culture,
    delete_dir_example_culture,
    rename_example_culture,
    get_test_cultures_dir,
)

from src.agenda.party import get_depotlink_types
from src.agenda.x_func import (
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from pyqt_func import agenda_importance_diplay


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
        if self.main_window.ignore_agenda_x is None:
            self.main_window.seed = self.main_window.x_kitchen._admin.open_seed_agenda()
            self.editmain_view.agenda_x = self.main_window.seed
        else:
            self.editmain_view.agenda_x = self.main_window.ignore_agenda_x
        self.editmain_view.refresh_all()
        self.editmain_view.show()

    def edit5issue_show(self):
        if self.main_window.x_kitchen != None:
            self.edit5issue_view.x_kitchen = self.main_window.x_kitchen
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
        self.culture_insert_button.clicked.connect(self.culture_insert)
        self.culture_load_button.clicked.connect(self.culture_load_from_file)
        self.culture_update_button.clicked.connect(self.culture_update_title)
        self.culture_delete_button.clicked.connect(self.culture_delete)
        self.agenda_insert_button.clicked.connect(self.agenda_insert)
        self.agenda_update_button.clicked.connect(self.agenda_update_title)
        self.agenda_delete_button.clicked.connect(self.agenda_delete)
        self.agendas_table.itemClicked.connect(self.agendas_table_select)
        self.healer_insert_button.clicked.connect(self.healer_insert)
        self.healer_update_button.clicked.connect(self.healer_update_title)
        self.healer_delete_button.clicked.connect(self.healer_delete)
        self.healers_table.itemClicked.connect(self.healers_table_select)
        self.reload_all_src_agendas_button.clicked.connect(self.reload_all_src_agendas)
        self.set_public_agenda_button.clicked.connect(
            self.save_output_agenda_to_public()
        )
        self.set_public_and_reload_srcs_button.clicked.connect(
            self.set_public_and_reload_srcs
        )
        self.ignores_table.itemClicked.connect(self.ignores_table_select)
        self.open_ignore_button.clicked.connect(self.open_editmain)
        self.save_ignore_button.clicked.connect(self.ignore_agenda_file_update)
        self.ignores_table.setHidden(True)
        self.show_ignores_button.clicked.connect(self.show_ignores_table)
        self.show_digests_button.clicked.connect(self.show_digests_table)
        self.seed_open_button.clicked.connect(self.open_editmain)
        self.seed_save_button.clicked.connect(self.save_seed)

        self.depotlink_insert_button.clicked.connect(self.depotlink_insert)
        self.depotlink_update_button.clicked.connect(self.depotlink_update)
        self.depotlink_delete_button.clicked.connect(self.depotlink_delete)
        self.depotlinks_table.itemClicked.connect(self.depotlinks_table_select)
        self.five_issue_button.clicked.connect(self.open_edit5issue)

        self.culture_x = None
        self.x_kitchen = None
        self.ignore_agenda_x = None
        setup_test_example_environment()
        first_env = "ex5"
        self.culture_x = cultureunit_shop(
            title=first_env, cultures_dir=get_test_cultures_dir()
        )
        self.refresh_culture()
        self.culture_handle_combo_refresh()
        self.culture_handle_combo.setCurrentText(first_env)
        self._healer_load(kitchen_title="ernie")

    def save_seed(self):
        if self.seed != None:
            self.x_kitchen._admin.save_seed_agenda(self.seed)
        self.refresh_healer()

    def reload_all_src_agendas(self):
        if self.culture_x != None:
            self.culture_x.reload_all_kitchenunits_src_agendaunits()

    def set_public_and_reload_srcs(self):
        self.save_output_agenda_to_public()
        self.reload_all_src_agendas()

    def save_output_agenda_to_public(self):
        if self.x_kitchen != None:
            self.x_kitchen.save_output_agenda_to_public()
        self.refresh_culture()

    def culture_load_from_file(self):
        culture_selected = self.culture_handle_combo.currentText()
        self.culture_x = cultureunit_shop(
            title=culture_selected, cultures_dir=get_test_cultures_dir()
        )
        self.culture_x.create_dirs_if_null(in_memory_bank=False)
        self.culture_handle.setText(culture_selected)
        self.refresh_culture()

    def agendas_table_select(self):
        self.agenda_healer.setText(
            self.agendas_table.item(self.agendas_table.currentRow(), 0).text()
        )
        if self.healers_table.currentRow() != -1:
            selected_healer = self.healers_table.item(
                self.healers_table.currentRow(), 0
            ).text()
            selected_agenda = self.agendas_table.item(
                self.agendas_table.currentRow(), 0
            ).text()
            self.depotlink_title.setText(f"{selected_healer} - {selected_agenda}")

    def healers_table_select(self):
        x_kitchen_title = self.healers_table.item(
            self.healers_table.currentRow(), 0
        ).text()
        self._healer_load(kitchen_title=x_kitchen_title)

    def _healer_load(self, kitchen_title: str):
        self.culture_x.create_new_kitchenunit(title=kitchen_title)
        self.x_kitchen = self.culture_x._kitchenunits.get(kitchen_title)
        self.kitchen_title.setText(self.x_kitchen._admin.title)
        self.refresh_healer()

    def depotlinks_table_select(self):
        self.depotlink_title.setText(
            self.depotlinks_table.item(self.depotlinks_table.currentRow(), 0).text()
        )
        self.depotlink_type_combo.setCurrentText(
            self.depotlinks_table.item(self.depotlinks_table.currentRow(), 1).text()
        )
        self.depotlink_weight.setText(
            self.depotlinks_table.item(self.depotlinks_table.currentRow(), 2).text()
        )

    def ignores_table_select(self):
        ignore_agenda_healer = self.ignores_table.item(
            self.ignores_table.currentRow(), 0
        ).text()
        # self.ignore_agenda_x = self.culture_x.get_public_agenda(
        self.ignore_agenda_x = self.culture_x.get_agenda_from_ignores_dir(
            kitchen_title=self.x_kitchen._admin.title, _healer=ignore_agenda_healer
        )
        self.edit_agenda = self.ignore_agenda_x

    def ignore_agenda_file_update(self):
        self.culture_x.set_ignore_agenda_file(
            kitchen_title=self.x_kitchen._admin.title, agenda_obj=self.ignore_agenda_x
        )
        self.refresh_healer()

    def show_ignores_table(self):
        self.ignores_table.setHidden(False)
        self.digests_table.setHidden(True)

    def show_digests_table(self):
        self.ignores_table.setHidden(True)
        self.digests_table.setHidden(False)

    def culture_insert(self):
        create_example_culture(culture_handle=self.culture_handle.text())
        self.culture_handle_combo_refresh()

    def culture_update_title(self):
        rename_example_culture(
            culture_obj=self.culture_x, new_title=self.culture_handle.text()
        )
        self.culture_handle_combo_refresh()

    def culture_delete(self):
        delete_dir_example_culture(culture_obj=self.culture_x)
        self.culture_x = None
        self.culture_handle_combo_refresh()
        self.refresh_culture()

    def agenda_insert(self):
        self.culture_x.save_public_agenda(
            agenda_x=AgendaUnit(_healer=self.agenda_healer.text())
        )
        self.refresh_culture()

    def agenda_update_title(self):
        currently_selected = self.agendas_table.item(
            self.agendas_table.currentRow(), 0
        ).text()
        typed_in = self.agenda_healer.text()
        if currently_selected != typed_in:
            self.culture_x.rename_public_agenda(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_culture()

    def agenda_delete(self):
        self.culture_x.del_public_agenda(
            agenda_x_label=self.agendas_table.item(
                self.agendas_table.currentRow(), 0
            ).text()
        )
        self.refresh_culture()

    def healer_insert(self):
        self.culture_x.create_new_kitchenunit(kitchen_title=self.kitchen_title.text())
        self.refresh_healers()

    def healer_update_title(self):
        currently_selected = self.healers_table.item(
            self.healers_table.currentRow(), 0
        ).text()
        typed_in = self.kitchen_title.text()
        if currently_selected != typed_in:
            self.culture_x.rename_kitchenunit(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_healers()

    def healer_delete(self):
        self.culture_x.del_kitchenunit_dir(
            kitchen_title=self.healers_table.item(
                self.healers_table.currentRow(), 0
            ).text()
        )
        self.refresh_healers()

    def depotlink_insert(self):
        agenda_healer = self.agendas_table.item(
            self.agendas_table.currentRow(), 0
        ).text()
        if self.x_kitchen != None:
            agenda_json = x_func_open_file(
                dest_dir=self.x_kitchen._admin._agendas_public_dir,
                file_title=f"{agenda_healer}.json",
            )
            agenda_x = get_agenda_from_json(agenda_json)
            self.x_kitchen.set_depot_agenda(
                agenda_x=agenda_x,
                depotlink_type=self.depotlink_type_combo.currentText(),
                depotlink_weight=self.depotlink_weight.text(),
            )
            self.culture_x.save_kitchenunit_file(
                kitchen_title=self.x_kitchen._admin.title
            )
        self.refresh_healer()

    def depotlink_update(self):
        kitchen_title_x = self.x_kitchen._admin.title
        self.culture_x.update_depotlink(
            kitchen_title=kitchen_title_x,
            partytitle=self.depotlink_title.text(),
            depotlink_type=self.depotlink_type_combo.currentText(),
            creditor_weight=self.depotlink_weight.text(),
            debtor_weight=self.depotlink_weight.text(),
        )
        self.culture_x.save_kitchenunit_file(kitchen_title=kitchen_title_x)
        self.refresh_healer()

    def depotlink_delete(self):
        kitchen_title_x = self.x_kitchen._admin.title
        self.culture_x.del_depotlink(
            kitchen_title=kitchen_title_x, agendaunit_healer=self.depotlink_title.text()
        )
        self.culture_x.save_kitchenunit_file(kitchen_title=kitchen_title_x)
        self.refresh_healer()

    def get_agenda_healer_list(self):
        agendas_list = []
        for file_title in self.get_public_dir_file_titles_list():
            agenda_json = x_func_open_file(
                dest_dir=self.get_public_dir(), file_title=file_title
            )
            agendas_list.append(get_agenda_from_json(x_agenda_json=agenda_json))
        return agendas_list

    def get_kitchen_title_list(self):
        healers_healer_list = []
        if self.culture_x != None:
            healers_healer_list.extend(
                [healer_dir]
                for healer_dir in self.culture_x.get_kitchenunit_dir_paths_list()
            )
        return healers_healer_list

    def get_depotlink_list(self):
        depotlinks_list = []
        if self.x_kitchen != None:
            for cl_val in self.x_kitchen._depotlinks.values():
                depotlink_row = [
                    cl_val.agenda_healer,
                    cl_val.depotlink_type,
                    str(cl_val.weight),
                ]
                depotlinks_list.append(depotlink_row)
        return depotlinks_list

    def get_digests_list(self):
        x_list = []
        if self.x_kitchen != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.x_kitchen_admin._agendas_digest_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_ignores_list(self):
        x_list = []
        if self.x_kitchen != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.x_kitchen._admin._agendas_ignore_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_p_ideas_list(self):
        x_list = []
        if self.healer_output_agenda != None:
            idea_list = self.healer_output_agenda.get_idea_tree_ordered_road_list()

            for idea_road in idea_list:
                idea_obj = self.healer_output_agenda.get_idea_kid(idea_road)

                if idea_obj._pad.find("time") != 3:
                    x_list.append(
                        [
                            agenda_importance_diplay(idea_obj._agenda_importance),
                            idea_road,
                            len(idea_obj._balancelinks),
                        ]
                    )

        return x_list

    def get_p_partys_list(self):
        x_list = []
        if self.healer_output_agenda != None:
            x_list.extend(
                [
                    f"{agenda_importance_diplay(partyunit._agenda_credit)}/{agenda_importance_diplay(partyunit._agenda_debt)}",
                    partyunit.title,
                    f"{partyunit.creditor_weight}/{partyunit.debtor_weight}",
                ]
                for partyunit in self.healer_output_agenda._partys.values()
            )
        return x_list

    def get_p_groups_list(self):
        x_list = []
        if self.healer_output_agenda != None:
            x_list.extend(
                [
                    f"{agenda_importance_diplay(groupunit._agenda_debt)}/{agenda_importance_diplay(groupunit._agenda_credit)}",
                    groupunit.brand,
                    len(groupunit._partys),
                ]
                for groupunit in self.healer_output_agenda._groups.values()
            )
        return x_list

    def get_p_acptfacts_list(self):
        x_list = []
        if self.healer_output_agenda != None:
            for (
                acptfactunit
            ) in self.healer_output_agenda._idearoot._acptfactunits.values():
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

    def get_p_goal_list(self):
        x_list = []
        if self.healer_output_agenda != None:
            goal_list = self.healer_output_agenda.get_goal_items()
            goal_list.sort(key=lambda x: x._agenda_importance, reverse=True)
            x_list.extend(
                [
                    agenda_importance_diplay(goal_item._agenda_importance),
                    goal_item._label,
                    goal_item._pad,
                ]
                for goal_item in goal_list
            )
        return x_list

    def refresh_all(self):
        self.refresh_culture()

    def _sub_refresh_healers_table(self):
        self.refresh_x(
            self.healers_table, ["Healers Table"], self.get_kitchen_title_list()
        )

    def _sub_refresh_depotlinks_table(self):
        depotlink_types = list(get_depotlink_types())
        depotlink_types.insert(0, "")
        self.depotlink_type_combo.clear()
        self.depotlink_type_combo.addItems(depotlink_types)
        self.depotlink_type_combo.setCurrentText("")
        column_header = ""
        if self.x_kitchen is None:
            column_header = "Agendalinks Table"
        elif self.x_kitchen != None:
            column_header = f"'{self.x_kitchen._admin.title}' Agendas"
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
                "agenda_importance",
                f"Ideas Table ({len(p_ideas_list)})",
                "balancelinks",
            ]
        else:
            column_headers = [
                "agenda_importance",
                "Ideas Table",
                "balancelinks",
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

    def _sub_refresh_p_partys_table(self):
        p_partys_list = self.get_p_partys_list()
        column_headers = [
            "agenda_debt/agenda_credit",
            f"Partys ({len(p_partys_list)})",
            "creditor_weight/debtor_weight",
        ]

        self.refresh_x(
            table_x=self.w_partys_table,
            column_header=column_headers,
            populate_list=p_partys_list,
            column_width=[50, 300, 50],
        )

    def _sub_refresh_p_groups_table(self):
        p_groups_list = self.get_p_groups_list()
        column_headers = [
            "agenda_debt/agenda_credit",
            f"groups ({len(p_groups_list)})",
            "Partys",
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

    def _sub_refresh_p_goal_table(self):
        p_goal_list = self.get_p_goal_list()
        column_headers = [
            "agenda_importance",
            f"Agenda ({len(p_goal_list)})",
            "Idea Walk",
        ]

        self.refresh_x(
            table_x=self.w_goal_table,
            column_header=column_headers,
            populate_list=p_goal_list,
            column_width=[50, 200, 300],
        )

    def culture_handle_combo_refresh(self):
        self.culture_handle_combo.clear()
        self.culture_handle_combo.addItems(create_example_cultures_list())

    def refresh_healers(self):
        self.x_kitchen = None
        self._sub_refresh_healers_table()
        self.refresh_healer()

    def refresh_healer(self):
        self._sub_refresh_depotlinks_table()
        self._sub_refresh_digests_table()
        self._sub_refresh_ignores_table()
        self.healer_output_agenda = None
        if self.x_kitchen != None:
            self.healer_output_agenda = (
                self.x_kitchen._admin.get_remelded_output_agenda()
            )
        self._sub_refresh_p_ideas_table()
        self._sub_refresh_p_partys_table()
        self._sub_refresh_p_groups_table()
        self._sub_refresh_p_acptfacts_table()
        self._sub_refresh_p_goal_table()

    def refresh_culture(self):
        self.refresh_x(
            self.agendas_table, ["Agendas Table"], self.get_agenda_healer_list()
        )
        self.refresh_healers()

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


if __title__ == "__main__":
    app = MainApp(sys_argv)
    sys_exit(app.exec())
