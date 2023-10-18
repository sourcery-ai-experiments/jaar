# # command to for converting ui form to python file: pyuic5 ui\projectMainUI.ui -o ui\projectMainUI.py
from ui.projectMainUI import Ui_MainWindow
from Edit5Issue import Edit5Issue
from EditMain import EditMainView
from PyQt5 import QtCore as qtc
from src.deal.deal import (
    DealUnit,
    get_from_json as get_deal_from_json,
)
from sys import argv as sys_argv, exit as sys_exit
from PyQt5.QtWidgets import (
    QTableWidgetItem as qtw1,
    QApplication,
    QMainWindow,
)
from src.project.project import projectunit_shop
from src.project.examples.project_env_kit import (
    create_example_projects_list,
    setup_test_example_environment,
    create_example_project,
    delete_dir_example_project,
    rename_example_project,
    get_test_projects_dir,
)

from src.deal.party import get_depotlink_types
from src.deal.x_func import (
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from pyqt_func import deal_importance_diplay


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
        if self.main_window.ignore_deal_x is None:
            self.main_window.seed = self.main_window.x_kitchen._admin.open_seed_deal()
            self.editmain_view.deal_x = self.main_window.seed
        else:
            self.editmain_view.deal_x = self.main_window.ignore_deal_x
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
        self.project_insert_button.clicked.connect(self.project_insert)
        self.project_load_button.clicked.connect(self.project_load_from_file)
        self.project_update_button.clicked.connect(self.project_update_title)
        self.project_delete_button.clicked.connect(self.project_delete)
        self.deal_insert_button.clicked.connect(self.deal_insert)
        self.deal_update_button.clicked.connect(self.deal_update_title)
        self.deal_delete_button.clicked.connect(self.deal_delete)
        self.deals_table.itemClicked.connect(self.deals_table_select)
        self.healer_insert_button.clicked.connect(self.healer_insert)
        self.healer_update_button.clicked.connect(self.healer_update_title)
        self.healer_delete_button.clicked.connect(self.healer_delete)
        self.healers_table.itemClicked.connect(self.healers_table_select)
        self.reload_all_src_deals_button.clicked.connect(self.reload_all_src_deals)
        self.set_public_deal_button.clicked.connect(self.save_output_deal_to_public())
        self.set_public_and_reload_srcs_button.clicked.connect(
            self.set_public_and_reload_srcs
        )
        self.ignores_table.itemClicked.connect(self.ignores_table_select)
        self.open_ignore_button.clicked.connect(self.open_editmain)
        self.save_ignore_button.clicked.connect(self.ignore_deal_file_update)
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

        self.project_x = None
        self.x_kitchen = None
        self.ignore_deal_x = None
        setup_test_example_environment()
        first_env = "ex5"
        self.project_x = projectunit_shop(
            title=first_env, projects_dir=get_test_projects_dir()
        )
        self.refresh_project()
        self.project_handle_combo_refresh()
        self.project_handle_combo.setCurrentText(first_env)
        self._healer_load(kitchen_title="ernie")

    def save_seed(self):
        if self.seed != None:
            self.x_kitchen._admin.save_seed_deal(self.seed)
        self.refresh_healer()

    def reload_all_src_deals(self):
        if self.project_x != None:
            self.project_x.reload_all_kitchenunits_src_dealunits()

    def set_public_and_reload_srcs(self):
        self.save_output_deal_to_public()
        self.reload_all_src_deals()

    def save_output_deal_to_public(self):
        if self.x_kitchen != None:
            self.x_kitchen.save_output_deal_to_public()
        self.refresh_project()

    def project_load_from_file(self):
        project_selected = self.project_handle_combo.currentText()
        self.project_x = projectunit_shop(
            title=project_selected, projects_dir=get_test_projects_dir()
        )
        self.project_x.create_dirs_if_null(in_memory_bank=False)
        self.project_handle.setText(project_selected)
        self.refresh_project()

    def deals_table_select(self):
        self.deal_healer.setText(
            self.deals_table.item(self.deals_table.currentRow(), 0).text()
        )
        if self.healers_table.currentRow() != -1:
            selected_healer = self.healers_table.item(
                self.healers_table.currentRow(), 0
            ).text()
            selected_deal = self.deals_table.item(
                self.deals_table.currentRow(), 0
            ).text()
            self.depotlink_title.setText(f"{selected_healer} - {selected_deal}")

    def healers_table_select(self):
        x_kitchen_title = self.healers_table.item(
            self.healers_table.currentRow(), 0
        ).text()
        self._healer_load(kitchen_title=x_kitchen_title)

    def _healer_load(self, kitchen_title: str):
        self.project_x.create_kitchenunit_from_public(title=kitchen_title)
        self.x_kitchen = self.project_x._kitchenunits.get(kitchen_title)
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
        ignore_deal_healer = self.ignores_table.item(
            self.ignores_table.currentRow(), 0
        ).text()
        # self.ignore_deal_x = self.project_x.get_public_deal(
        self.ignore_deal_x = self.project_x.get_deal_from_ignores_dir(
            kitchen_title=self.x_kitchen._admin.title, _healer=ignore_deal_healer
        )
        self.edit_deal = self.ignore_deal_x

    def ignore_deal_file_update(self):
        self.project_x.set_ignore_deal_file(
            kitchen_title=self.x_kitchen._admin.title, deal_obj=self.ignore_deal_x
        )
        self.refresh_healer()

    def show_ignores_table(self):
        self.ignores_table.setHidden(False)
        self.digests_table.setHidden(True)

    def show_digests_table(self):
        self.ignores_table.setHidden(True)
        self.digests_table.setHidden(False)

    def project_insert(self):
        create_example_project(project_handle=self.project_handle.text())
        self.project_handle_combo_refresh()

    def project_update_title(self):
        rename_example_project(
            project_obj=self.project_x, new_title=self.project_handle.text()
        )
        self.project_handle_combo_refresh()

    def project_delete(self):
        delete_dir_example_project(project_obj=self.project_x)
        self.project_x = None
        self.project_handle_combo_refresh()
        self.refresh_project()

    def deal_insert(self):
        self.project_x.save_public_deal(
            deal_x=DealUnit(_healer=self.deal_healer.text())
        )
        self.refresh_project()

    def deal_update_title(self):
        currently_selected = self.deals_table.item(
            self.deals_table.currentRow(), 0
        ).text()
        typed_in = self.deal_healer.text()
        if currently_selected != typed_in:
            self.project_x.rename_public_deal(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_project()

    def deal_delete(self):
        self.project_x.del_public_deal(
            deal_x_label=self.deals_table.item(self.deals_table.currentRow(), 0).text()
        )
        self.refresh_project()

    def healer_insert(self):
        self.project_x.create_new_kitchenunit(kitchen_title=self.kitchen_title.text())
        self.refresh_healers()

    def healer_update_title(self):
        currently_selected = self.healers_table.item(
            self.healers_table.currentRow(), 0
        ).text()
        typed_in = self.kitchen_title.text()
        if currently_selected != typed_in:
            self.project_x.rename_kitchenunit(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_healers()

    def healer_delete(self):
        self.project_x.del_kitchenunit_dir(
            kitchen_title=self.healers_table.item(
                self.healers_table.currentRow(), 0
            ).text()
        )
        self.refresh_healers()

    def depotlink_insert(self):
        deal_healer = self.deals_table.item(self.deals_table.currentRow(), 0).text()
        if self.x_kitchen != None:
            deal_json = x_func_open_file(
                dest_dir=self.x_kitchen._admin._deals_public_dir,
                file_title=f"{deal_healer}.json",
            )
            deal_x = get_deal_from_json(deal_json)
            self.x_kitchen.set_depot_deal(
                deal_x=deal_x,
                depotlink_type=self.depotlink_type_combo.currentText(),
                depotlink_weight=self.depotlink_weight.text(),
            )
            self.project_x.save_kitchenunit_file(
                kitchen_title=self.x_kitchen._admin.title
            )
        self.refresh_healer()

    def depotlink_update(self):
        kitchen_title_x = self.x_kitchen._admin.title
        self.project_x.update_depotlink(
            kitchen_title=kitchen_title_x,
            partytitle=self.depotlink_title.text(),
            depotlink_type=self.depotlink_type_combo.currentText(),
            creditor_weight=self.depotlink_weight.text(),
            debtor_weight=self.depotlink_weight.text(),
        )
        self.project_x.save_kitchenunit_file(kitchen_title=kitchen_title_x)
        self.refresh_healer()

    def depotlink_delete(self):
        kitchen_title_x = self.x_kitchen._admin.title
        self.project_x.del_depotlink(
            kitchen_title=kitchen_title_x, dealunit_healer=self.depotlink_title.text()
        )
        self.project_x.save_kitchenunit_file(kitchen_title=kitchen_title_x)
        self.refresh_healer()

    def get_deal_healer_list(self):
        deals_list = []
        for file_title in self.get_public_dir_file_titles_list():
            deal_json = x_func_open_file(
                dest_dir=self.get_public_dir(), file_title=file_title
            )
            deals_list.append(get_deal_from_json(x_deal_json=deal_json))
        return deals_list

    def get_kitchen_title_list(self):
        healers_healer_list = []
        if self.project_x != None:
            healers_healer_list.extend(
                [healer_dir]
                for healer_dir in self.project_x.get_kitchenunit_dir_paths_list()
            )
        return healers_healer_list

    def get_depotlink_list(self):
        depotlinks_list = []
        if self.x_kitchen != None:
            for cl_val in self.x_kitchen._depotlinks.values():
                depotlink_row = [
                    cl_val.deal_healer,
                    cl_val.depotlink_type,
                    str(cl_val.weight),
                ]
                depotlinks_list.append(depotlink_row)
        return depotlinks_list

    def get_digests_list(self):
        x_list = []
        if self.x_kitchen != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.x_kitchen_admin._deals_digest_dir,
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
                dir_path=self.x_kitchen._admin._deals_ignore_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_p_ideas_list(self):
        x_list = []
        if self.healer_output_deal != None:
            idea_list = self.healer_output_deal.get_idea_tree_ordered_road_list()

            for idea_road in idea_list:
                idea_obj = self.healer_output_deal.get_idea_kid(idea_road)

                if idea_obj._pad.find("time") != 3:
                    x_list.append(
                        [
                            deal_importance_diplay(idea_obj._deal_importance),
                            idea_road,
                            len(idea_obj._balancelinks),
                        ]
                    )

        return x_list

    def get_p_partys_list(self):
        x_list = []
        if self.healer_output_deal != None:
            x_list.extend(
                [
                    f"{deal_importance_diplay(partyunit._deal_credit)}/{deal_importance_diplay(partyunit._deal_debt)}",
                    partyunit.title,
                    f"{partyunit.creditor_weight}/{partyunit.debtor_weight}",
                ]
                for partyunit in self.healer_output_deal._partys.values()
            )
        return x_list

    def get_p_groups_list(self):
        x_list = []
        if self.healer_output_deal != None:
            x_list.extend(
                [
                    f"{deal_importance_diplay(groupunit._deal_debt)}/{deal_importance_diplay(groupunit._deal_credit)}",
                    groupunit.brand,
                    len(groupunit._partys),
                ]
                for groupunit in self.healer_output_deal._groups.values()
            )
        return x_list

    def get_p_acptfacts_list(self):
        x_list = []
        if self.healer_output_deal != None:
            for (
                acptfactunit
            ) in self.healer_output_deal._idearoot._acptfactunits.values():
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
        if self.healer_output_deal != None:
            agenda_list = self.healer_output_deal.get_agenda_items()
            agenda_list.sort(key=lambda x: x._deal_importance, reverse=True)
            x_list.extend(
                [
                    deal_importance_diplay(agenda_item._deal_importance),
                    agenda_item._label,
                    agenda_item._pad,
                ]
                for agenda_item in agenda_list
            )
        return x_list

    def refresh_all(self):
        self.refresh_project()

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
            column_header = "Deallinks Table"
        elif self.x_kitchen != None:
            column_header = f"'{self.x_kitchen._admin.title}' Deallinks"
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
                "deal_importance",
                f"Ideas Table ({len(p_ideas_list)})",
                "balancelinks",
            ]
        else:
            column_headers = [
                "deal_importance",
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
            "deal_debt/deal_credit",
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
            "deal_debt/deal_credit",
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

    def _sub_refresh_p_agenda_table(self):
        p_agenda_list = self.get_p_agenda_list()
        column_headers = [
            "deal_importance",
            f"Agenda ({len(p_agenda_list)})",
            "Idea Walk",
        ]

        self.refresh_x(
            table_x=self.w_agenda_table,
            column_header=column_headers,
            populate_list=p_agenda_list,
            column_width=[50, 200, 300],
        )

    def project_handle_combo_refresh(self):
        self.project_handle_combo.clear()
        self.project_handle_combo.addItems(create_example_projects_list())

    def refresh_healers(self):
        self.x_kitchen = None
        self._sub_refresh_healers_table()
        self.refresh_healer()

    def refresh_healer(self):
        self._sub_refresh_depotlinks_table()
        self._sub_refresh_digests_table()
        self._sub_refresh_ignores_table()
        self.healer_output_deal = None
        if self.x_kitchen != None:
            self.healer_output_deal = self.x_kitchen._admin.get_remelded_output_deal()
        self._sub_refresh_p_ideas_table()
        self._sub_refresh_p_partys_table()
        self._sub_refresh_p_groups_table()
        self._sub_refresh_p_acptfacts_table()
        self._sub_refresh_p_agenda_table()

    def refresh_project(self):
        self.refresh_x(self.deals_table, ["Deals Table"], self.get_deal_healer_list())
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
