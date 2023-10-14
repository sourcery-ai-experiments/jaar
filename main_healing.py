# # command to for converting ui form to python file: pyuic5 ui\HealingMainUI.ui -o ui\HealingMainUI.py
from ui.HealingMainUI import Ui_MainWindow
from Edit5Issue import Edit5Issue
from EditMain import EditMainView
from PyQt5 import QtCore as qtc
from src.contract.contract import (
    ContractUnit,
    get_from_json as get_contract_from_json,
)
from sys import argv as sys_argv, exit as sys_exit
from PyQt5.QtWidgets import (
    QTableWidgetItem as qtw1,
    QApplication,
    QMainWindow,
)
from src.healing.healing import healingunit_shop
from src.healing.examples.healing_env_kit import (
    create_example_healings_list,
    setup_test_example_environment,
    create_example_healing,
    delete_dir_example_healing,
    rename_example_healing,
    get_test_healings_dir,
)

from src.contract.party import get_depotlink_types
from src.contract.x_func import (
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from src.pyqt5_kit.pyqt_func import contract_importance_diplay


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
        if self.main_window.ignore_contract_x is None:
            self.main_window.isol = (
                self.main_window.healer_x._admin.open_isol_contract()
            )
            self.editmain_view.contract_x = self.main_window.isol
        else:
            self.editmain_view.contract_x = self.main_window.ignore_contract_x
        self.editmain_view.refresh_all()
        self.editmain_view.show()

    def edit5issue_show(self):
        if self.main_window.healer_x != None:
            self.edit5issue_view.healer_x = self.main_window.healer_x
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
        self.healing_insert_button.clicked.connect(self.healing_insert)
        self.healing_load_button.clicked.connect(self.healing_load_from_file)
        self.healing_update_button.clicked.connect(self.healing_update_title)
        self.healing_delete_button.clicked.connect(self.healing_delete)
        self.contract_insert_button.clicked.connect(self.contract_insert)
        self.contract_update_button.clicked.connect(self.contract_update_title)
        self.contract_delete_button.clicked.connect(self.contract_delete)
        self.contracts_table.itemClicked.connect(self.contracts_table_select)
        self.healer_insert_button.clicked.connect(self.healer_insert)
        self.healer_update_button.clicked.connect(self.healer_update_title)
        self.healer_delete_button.clicked.connect(self.healer_delete)
        self.healers_table.itemClicked.connect(self.healers_table_select)
        self.reload_all_src_contracts_button.clicked.connect(
            self.reload_all_src_contracts
        )
        self.set_public_contract_button.clicked.connect(
            self.save_output_contract_to_public()
        )
        self.set_public_and_reload_srcs_button.clicked.connect(
            self.set_public_and_reload_srcs
        )
        self.ignores_table.itemClicked.connect(self.ignores_table_select)
        self.open_ignore_button.clicked.connect(self.open_editmain)
        self.save_ignore_button.clicked.connect(self.ignore_contract_file_update)
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

        self.healing_x = None
        self.healer_x = None
        self.ignore_contract_x = None
        setup_test_example_environment()
        first_env = "ex5"
        self.healing_x = healingunit_shop(
            title=first_env, healings_dir=get_test_healings_dir()
        )
        self.refresh_healing()
        self.healing_kind_combo_refresh()
        self.healing_kind_combo.setCurrentText(first_env)
        self._healer_load(healer_title="ernie")

    def save_isol(self):
        if self.isol != None:
            self.healer_x._admin.save_isol_contract(self.isol)
        self.refresh_healer()

    def reload_all_src_contracts(self):
        if self.healing_x != None:
            self.healing_x.reload_all_healers_src_contractunits()

    def set_public_and_reload_srcs(self):
        self.save_output_contract_to_public()
        self.reload_all_src_contracts()

    def save_output_contract_to_public(self):
        if self.healer_x != None:
            self.healer_x.save_output_contract_to_public()
        self.refresh_healing()

    def healing_load_from_file(self):
        healing_selected = self.healing_kind_combo.currentText()
        self.healing_x = healingunit_shop(
            title=healing_selected, healings_dir=get_test_healings_dir()
        )
        self.healing_x.create_dirs_if_null(in_memory_bank=False)
        self.healing_kind.setText(healing_selected)
        self.refresh_healing()

    def contracts_table_select(self):
        self.contract_healer.setText(
            self.contracts_table.item(self.contracts_table.currentRow(), 0).text()
        )
        if self.healers_table.currentRow() != -1:
            selected_healer = self.healers_table.item(
                self.healers_table.currentRow(), 0
            ).text()
            selected_contract = self.contracts_table.item(
                self.contracts_table.currentRow(), 0
            ).text()
            self.depotlink_title.setText(f"{selected_healer} - {selected_contract}")

    def healers_table_select(self):
        healer_x_title = self.healers_table.item(
            self.healers_table.currentRow(), 0
        ).text()
        self._healer_load(healer_title=healer_x_title)

    def _healer_load(self, healer_title: str):
        self.healing_x.create_healerunit_from_public(title=healer_title)
        self.healer_x = self.healing_x._healerunits.get(healer_title)
        self.healer_title.setText(self.healer_x._admin.title)
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
        ignore_contract_healer = self.ignores_table.item(
            self.ignores_table.currentRow(), 0
        ).text()
        # self.ignore_contract_x = self.healing_x.get_public_contract(
        self.ignore_contract_x = self.healing_x.get_contract_from_ignores_dir(
            healer_title=self.healer_x._admin.title, _healer=ignore_contract_healer
        )
        self.edit_contract = self.ignore_contract_x

    def ignore_contract_file_update(self):
        self.healing_x.set_ignore_contract_file(
            healer_title=self.healer_x._admin.title, contract_obj=self.ignore_contract_x
        )
        self.refresh_healer()

    def show_ignores_table(self):
        self.ignores_table.setHidden(False)
        self.digests_table.setHidden(True)

    def show_digests_table(self):
        self.ignores_table.setHidden(True)
        self.digests_table.setHidden(False)

    def healing_insert(self):
        create_example_healing(healing_kind=self.healing_kind.text())
        self.healing_kind_combo_refresh()

    def healing_update_title(self):
        rename_example_healing(
            healing_obj=self.healing_x, new_title=self.healing_kind.text()
        )
        self.healing_kind_combo_refresh()

    def healing_delete(self):
        delete_dir_example_healing(healing_obj=self.healing_x)
        self.healing_x = None
        self.healing_kind_combo_refresh()
        self.refresh_healing()

    def contract_insert(self):
        self.healing_x.save_public_contract(
            contract_x=ContractUnit(_healer=self.contract_healer.text())
        )
        self.refresh_healing()

    def contract_update_title(self):
        currently_selected = self.contracts_table.item(
            self.contracts_table.currentRow(), 0
        ).text()
        typed_in = self.contract_healer.text()
        if currently_selected != typed_in:
            self.healing_x.rename_public_contract(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_healing()

    def contract_delete(self):
        self.healing_x.del_public_contract(
            contract_x_label=self.contracts_table.item(
                self.contracts_table.currentRow(), 0
            ).text()
        )
        self.refresh_healing()

    def healer_insert(self):
        self.healing_x.create_new_healerunit(healer_title=self.healer_title.text())
        self.refresh_healers()

    def healer_update_title(self):
        currently_selected = self.healers_table.item(
            self.healers_table.currentRow(), 0
        ).text()
        typed_in = self.healer_title.text()
        if currently_selected != typed_in:
            self.healing_x.rename_healerunit(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_healers()

    def healer_delete(self):
        self.healing_x.del_healer_dir(
            healer_title=self.healers_table.item(
                self.healers_table.currentRow(), 0
            ).text()
        )
        self.refresh_healers()

    def depotlink_insert(self):
        contract_healer = self.contracts_table.item(
            self.contracts_table.currentRow(), 0
        ).text()
        if self.healer_x != None:
            contract_json = x_func_open_file(
                dest_dir=self.healer_x._admin._contracts_public_dir,
                file_title=f"{contract_healer}.json",
            )
            contract_x = get_contract_from_json(contract_json)
            self.healer_x.set_depot_contract(
                contract_x=contract_x,
                depotlink_type=self.depotlink_type_combo.currentText(),
                depotlink_weight=self.depotlink_weight.text(),
            )
            self.healing_x.save_healer_file(healer_title=self.healer_x._admin.title)
        self.refresh_healer()

    def depotlink_update(self):
        healer_title_x = self.healer_x._admin.title
        self.healing_x.update_depotlink(
            healer_title=healer_title_x,
            partytitle=self.depotlink_title.text(),
            depotlink_type=self.depotlink_type_combo.currentText(),
            creditor_weight=self.depotlink_weight.text(),
            debtor_weight=self.depotlink_weight.text(),
        )
        self.healing_x.save_healer_file(healer_title=healer_title_x)
        self.refresh_healer()

    def depotlink_delete(self):
        healer_title_x = self.healer_x._admin.title
        self.healing_x.del_depotlink(
            healer_title=healer_title_x, contractunit_healer=self.depotlink_title.text()
        )
        self.healing_x.save_healer_file(healer_title=healer_title_x)
        self.refresh_healer()

    def get_contract_healer_list(self):
        contracts_list = []
        for file_title in self.get_public_dir_file_titles_list():
            contract_json = x_func_open_file(
                dest_dir=self.get_public_dir(), file_title=file_title
            )
            contracts_list.append(get_contract_from_json(cx_json=contract_json))
        return contracts_list

    def get_healer_title_list(self):
        healers_healer_list = []
        if self.healing_x != None:
            healers_healer_list.extend(
                [healer_dir]
                for healer_dir in self.healing_x.get_healer_dir_paths_list()
            )
        return healers_healer_list

    def get_depotlink_list(self):
        depotlinks_list = []
        if self.healer_x != None:
            for cl_val in self.healer_x._depotlinks.values():
                depotlink_row = [
                    cl_val.contract_healer,
                    cl_val.depotlink_type,
                    str(cl_val.weight),
                ]
                depotlinks_list.append(depotlink_row)
        return depotlinks_list

    def get_digests_list(self):
        x_list = []
        if self.healer_x != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.healer_x_admin._contracts_digest_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_ignores_list(self):
        x_list = []
        if self.healer_x != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.healer_x._admin._contracts_ignore_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_p_ideas_list(self):
        x_list = []
        if self.healer_output_contract != None:
            idea_list = self.healer_output_contract.get_idea_tree_ordered_road_list()

            for idea_road in idea_list:
                idea_obj = self.healer_output_contract.get_idea_kid(idea_road)

                if idea_obj._walk.find("time") != 3:
                    x_list.append(
                        [
                            contract_importance_diplay(idea_obj._contract_importance),
                            idea_road,
                            len(idea_obj._balancelinks),
                        ]
                    )

        return x_list

    def get_p_partys_list(self):
        x_list = []
        if self.healer_output_contract != None:
            x_list.extend(
                [
                    f"{contract_importance_diplay(partyunit._contract_credit)}/{contract_importance_diplay(partyunit._contract_debt)}",
                    partyunit.title,
                    f"{partyunit.creditor_weight}/{partyunit.debtor_weight}",
                ]
                for partyunit in self.healer_output_contract._partys.values()
            )
        return x_list

    def get_p_groups_list(self):
        x_list = []
        if self.healer_output_contract != None:
            x_list.extend(
                [
                    f"{contract_importance_diplay(groupunit._contract_debt)}/{contract_importance_diplay(groupunit._contract_credit)}",
                    groupunit.brand,
                    len(groupunit._partys),
                ]
                for groupunit in self.healer_output_contract._groups.values()
            )
        return x_list

    def get_p_acptfacts_list(self):
        x_list = []
        if self.healer_output_contract != None:
            for (
                acptfactunit
            ) in self.healer_output_contract._idearoot._acptfactunits.values():
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
        if self.healer_output_contract != None:
            agenda_list = self.healer_output_contract.get_agenda_items()
            agenda_list.sort(key=lambda x: x._contract_importance, reverse=True)
            x_list.extend(
                [
                    contract_importance_diplay(agenda_item._contract_importance),
                    agenda_item._label,
                    agenda_item._walk,
                ]
                for agenda_item in agenda_list
            )
        return x_list

    def refresh_all(self):
        self.refresh_healing()

    def _sub_refresh_healers_table(self):
        self.refresh_x(
            self.healers_table, ["Healers Table"], self.get_healer_title_list()
        )

    def _sub_refresh_depotlinks_table(self):
        depotlink_types = list(get_depotlink_types())
        depotlink_types.insert(0, "")
        self.depotlink_type_combo.clear()
        self.depotlink_type_combo.addItems(depotlink_types)
        self.depotlink_type_combo.setCurrentText("")
        column_header = ""
        if self.healer_x is None:
            column_header = "Contractlinks Table"
        elif self.healer_x != None:
            column_header = f"'{self.healer_x._admin.title}' Contractlinks"
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
                "contract_importance",
                f"Ideas Table ({len(p_ideas_list)})",
                "balancelinks",
            ]
        else:
            column_headers = [
                "contract_importance",
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
            "contract_debt/contract_credit",
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
            "contract_debt/contract_credit",
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
            "contract_importance",
            f"Agenda ({len(p_agenda_list)})",
            "Idea Walk",
        ]

        self.refresh_x(
            table_x=self.w_agenda_table,
            column_header=column_headers,
            populate_list=p_agenda_list,
            column_width=[50, 200, 300],
        )

    def healing_kind_combo_refresh(self):
        self.healing_kind_combo.clear()
        self.healing_kind_combo.addItems(create_example_healings_list())

    def refresh_healers(self):
        self.healer_x = None
        self._sub_refresh_healers_table()
        self.refresh_healer()

    def refresh_healer(self):
        self._sub_refresh_depotlinks_table()
        self._sub_refresh_digests_table()
        self._sub_refresh_ignores_table()
        self.healer_output_contract = None
        if self.healer_x != None:
            self.healer_output_contract = (
                self.healer_x._admin.get_remelded_output_contract()
            )
        self._sub_refresh_p_ideas_table()
        self._sub_refresh_p_partys_table()
        self._sub_refresh_p_groups_table()
        self._sub_refresh_p_acptfacts_table()
        self._sub_refresh_p_agenda_table()

    def refresh_healing(self):
        self.refresh_x(
            self.contracts_table, ["Contracts Table"], self.get_contract_healer_list()
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
