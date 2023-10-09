# # command to for converting ui form to python file: pyuic5 ui\EconomyMainUI.ui -o ui\EconomyMainUI.py
from ui.EconomyMainUI import Ui_MainWindow
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
from src.economy.economy import economyunit_shop
from src.economy.examples.economy_env_kit import (
    create_example_economys_list,
    setup_test_example_environment,
    create_example_economy,
    delete_dir_example_economy,
    rename_example_economy,
    get_test_economys_dir,
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
            self.main_window.isol = self.main_window.owner_x._admin.open_isol_contract()
            self.editmain_view.contract_x = self.main_window.isol
        else:
            self.editmain_view.contract_x = self.main_window.ignore_contract_x
        self.editmain_view.refresh_all()
        self.editmain_view.show()

    def edit5issue_show(self):
        if self.main_window.owner_x != None:
            self.edit5issue_view.owner_x = self.main_window.owner_x
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
        self.economy_insert_button.clicked.connect(self.economy_insert)
        self.economy_load_button.clicked.connect(self.economy_load_from_file)
        self.economy_update_button.clicked.connect(self.economy_update_title)
        self.economy_delete_button.clicked.connect(self.economy_delete)
        self.contract_insert_button.clicked.connect(self.contract_insert)
        self.contract_update_button.clicked.connect(self.contract_update_title)
        self.contract_delete_button.clicked.connect(self.contract_delete)
        self.contracts_table.itemClicked.connect(self.contracts_table_select)
        self.owner_insert_button.clicked.connect(self.owner_insert)
        self.owner_update_button.clicked.connect(self.owner_update_title)
        self.owner_delete_button.clicked.connect(self.owner_delete)
        self.owners_table.itemClicked.connect(self.owners_table_select)
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

        self.economy_x = None
        self.owner_x = None
        self.ignore_contract_x = None
        setup_test_example_environment()
        first_env = "ex5"
        self.economy_x = economyunit_shop(
            title=first_env, economys_dir=get_test_economys_dir()
        )
        self.refresh_economy()
        self.economy_tag_combo_refresh()
        self.economy_tag_combo.setCurrentText(first_env)
        self._owner_load(owner_title="ernie")

    def save_isol(self):
        if self.isol != None:
            self.owner_x._admin.save_isol_contract(self.isol)
        self.refresh_owner()

    def reload_all_src_contracts(self):
        if self.economy_x != None:
            self.economy_x.reload_all_owners_src_contractunits()

    def set_public_and_reload_srcs(self):
        self.save_output_contract_to_public()
        self.reload_all_src_contracts()

    def save_output_contract_to_public(self):
        if self.owner_x != None:
            self.owner_x.save_output_contract_to_public()
        self.refresh_economy()

    def economy_load_from_file(self):
        economy_selected = self.economy_tag_combo.currentText()
        self.economy_x = economyunit_shop(
            title=economy_selected, economys_dir=get_test_economys_dir()
        )
        self.economy_x.create_dirs_if_null(in_memory_bank=False)
        self.economy_tag.setText(economy_selected)
        self.refresh_economy()

    def contracts_table_select(self):
        self.contract_owner.setText(
            self.contracts_table.item(self.contracts_table.currentRow(), 0).text()
        )
        if self.owners_table.currentRow() != -1:
            selected_owner = self.owners_table.item(
                self.owners_table.currentRow(), 0
            ).text()
            selected_contract = self.contracts_table.item(
                self.contracts_table.currentRow(), 0
            ).text()
            self.depotlink_title.setText(f"{selected_owner} - {selected_contract}")

    def owners_table_select(self):
        owner_x_title = self.owners_table.item(self.owners_table.currentRow(), 0).text()
        self._owner_load(owner_title=owner_x_title)

    def _owner_load(self, owner_title: str):
        self.economy_x.create_ownerunit_from_public(title=owner_title)
        self.owner_x = self.economy_x._ownerunits.get(owner_title)
        self.owner_title.setText(self.owner_x._admin.title)
        self.refresh_owner()

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
        ignore_contract_owner = self.ignores_table.item(
            self.ignores_table.currentRow(), 0
        ).text()
        # self.ignore_contract_x = self.economy_x.get_public_contract(
        self.ignore_contract_x = self.economy_x.get_contract_from_ignores_dir(
            owner_title=self.owner_x._admin.title, _owner=ignore_contract_owner
        )
        self.edit_contract = self.ignore_contract_x

    def ignore_contract_file_update(self):
        self.economy_x.set_ignore_contract_file(
            owner_title=self.owner_x._admin.title, contract_obj=self.ignore_contract_x
        )
        self.refresh_owner()

    def show_ignores_table(self):
        self.ignores_table.setHidden(False)
        self.digests_table.setHidden(True)

    def show_digests_table(self):
        self.ignores_table.setHidden(True)
        self.digests_table.setHidden(False)

    def economy_insert(self):
        create_example_economy(economy_tag=self.economy_tag.text())
        self.economy_tag_combo_refresh()

    def economy_update_title(self):
        rename_example_economy(
            economy_obj=self.economy_x, new_title=self.economy_tag.text()
        )
        self.economy_tag_combo_refresh()

    def economy_delete(self):
        delete_dir_example_economy(economy_obj=self.economy_x)
        self.economy_x = None
        self.economy_tag_combo_refresh()
        self.refresh_economy()

    def contract_insert(self):
        self.economy_x.save_public_contract(
            contract_x=ContractUnit(_owner=self.contract_owner.text())
        )
        self.refresh_economy()

    def contract_update_title(self):
        currently_selected = self.contracts_table.item(
            self.contracts_table.currentRow(), 0
        ).text()
        typed_in = self.contract_owner.text()
        if currently_selected != typed_in:
            self.economy_x.rename_public_contract(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_economy()

    def contract_delete(self):
        self.economy_x.del_public_contract(
            contract_x_label=self.contracts_table.item(
                self.contracts_table.currentRow(), 0
            ).text()
        )
        self.refresh_economy()

    def owner_insert(self):
        self.economy_x.create_new_ownerunit(owner_title=self.owner_title.text())
        self.refresh_owners()

    def owner_update_title(self):
        currently_selected = self.owners_table.item(
            self.owners_table.currentRow(), 0
        ).text()
        typed_in = self.owner_title.text()
        if currently_selected != typed_in:
            self.economy_x.rename_ownerunit(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_owners()

    def owner_delete(self):
        self.economy_x.del_owner_dir(
            owner_title=self.owners_table.item(self.owners_table.currentRow(), 0).text()
        )
        self.refresh_owners()

    def depotlink_insert(self):
        contract_owner = self.contracts_table.item(
            self.contracts_table.currentRow(), 0
        ).text()
        if self.owner_x != None:
            contract_json = x_func_open_file(
                dest_dir=self.owner_x._admin._contracts_public_dir,
                file_title=f"{contract_owner}.json",
            )
            contract_x = get_contract_from_json(contract_json)
            self.owner_x.set_depot_contract(
                contract_x=contract_x,
                depotlink_type=self.depotlink_type_combo.currentText(),
                depotlink_weight=self.depotlink_weight.text(),
            )
            self.economy_x.save_owner_file(owner_title=self.owner_x._admin.title)
        self.refresh_owner()

    def depotlink_update(self):
        owner_title_x = self.owner_x._admin.title
        self.economy_x.update_depotlink(
            owner_title=owner_title_x,
            partytitle=self.depotlink_title.text(),
            depotlink_type=self.depotlink_type_combo.currentText(),
            creditor_weight=self.depotlink_weight.text(),
            debtor_weight=self.depotlink_weight.text(),
        )
        self.economy_x.save_owner_file(owner_title=owner_title_x)
        self.refresh_owner()

    def depotlink_delete(self):
        owner_title_x = self.owner_x._admin.title
        self.economy_x.del_depotlink(
            owner_title=owner_title_x, contractunit_owner=self.depotlink_title.text()
        )
        self.economy_x.save_owner_file(owner_title=owner_title_x)
        self.refresh_owner()

    def get_contract_owner_list(self):
        contracts_list = []
        for file_title in self.get_public_dir_file_titles_list():
            contract_json = x_func_open_file(
                dest_dir=self.get_public_dir(), file_title=file_title
            )
            contracts_list.append(get_contract_from_json(cx_json=contract_json))
        return contracts_list

    def get_owner_title_list(self):
        owners_owner_list = []
        if self.economy_x != None:
            owners_owner_list.extend(
                [owner_dir] for owner_dir in self.economy_x.get_owner_dir_paths_list()
            )
        return owners_owner_list

    def get_depotlink_list(self):
        depotlinks_list = []
        if self.owner_x != None:
            for cl_val in self.owner_x._depotlinks.values():
                depotlink_row = [
                    cl_val.contract_owner,
                    cl_val.depotlink_type,
                    str(cl_val.weight),
                ]
                depotlinks_list.append(depotlink_row)
        return depotlinks_list

    def get_digests_list(self):
        x_list = []
        if self.owner_x != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.owner_x_admin._contracts_digest_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_ignores_list(self):
        x_list = []
        if self.owner_x != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.owner_x._admin._contracts_ignore_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_p_ideas_list(self):
        x_list = []
        if self.owner_output_contract != None:
            idea_list = self.owner_output_contract.get_idea_tree_ordered_road_list()

            for idea_road in idea_list:
                idea_obj = self.owner_output_contract.get_idea_kid(idea_road)

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
        if self.owner_output_contract != None:
            x_list.extend(
                [
                    f"{contract_importance_diplay(partyunit._contract_credit)}/{contract_importance_diplay(partyunit._contract_debt)}",
                    partyunit.title,
                    f"{partyunit.creditor_weight}/{partyunit.debtor_weight}",
                ]
                for partyunit in self.owner_output_contract._partys.values()
            )
        return x_list

    def get_p_groups_list(self):
        x_list = []
        if self.owner_output_contract != None:
            x_list.extend(
                [
                    f"{contract_importance_diplay(groupunit._contract_debt)}/{contract_importance_diplay(groupunit._contract_credit)}",
                    groupunit.brand,
                    len(groupunit._partys),
                ]
                for groupunit in self.owner_output_contract._groups.values()
            )
        return x_list

    def get_p_acptfacts_list(self):
        x_list = []
        if self.owner_output_contract != None:
            for (
                acptfactunit
            ) in self.owner_output_contract._idearoot._acptfactunits.values():
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
        if self.owner_output_contract != None:
            agenda_list = self.owner_output_contract.get_agenda_items()
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
        self.refresh_economy()

    def _sub_refresh_owners_table(self):
        self.refresh_x(self.owners_table, ["Owners Table"], self.get_owner_title_list())

    def _sub_refresh_depotlinks_table(self):
        depotlink_types = list(get_depotlink_types())
        depotlink_types.insert(0, "")
        self.depotlink_type_combo.clear()
        self.depotlink_type_combo.addItems(depotlink_types)
        self.depotlink_type_combo.setCurrentText("")
        column_header = ""
        if self.owner_x is None:
            column_header = "Contractlinks Table"
        elif self.owner_x != None:
            column_header = f"'{self.owner_x._admin.title}' Contractlinks"
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

    def economy_tag_combo_refresh(self):
        self.economy_tag_combo.clear()
        self.economy_tag_combo.addItems(create_example_economys_list())

    def refresh_owners(self):
        self.owner_x = None
        self._sub_refresh_owners_table()
        self.refresh_owner()

    def refresh_owner(self):
        self._sub_refresh_depotlinks_table()
        self._sub_refresh_digests_table()
        self._sub_refresh_ignores_table()
        self.owner_output_contract = None
        if self.owner_x != None:
            self.owner_output_contract = (
                self.owner_x._admin.get_remelded_output_contract()
            )
        self._sub_refresh_p_ideas_table()
        self._sub_refresh_p_partys_table()
        self._sub_refresh_p_groups_table()
        self._sub_refresh_p_acptfacts_table()
        self._sub_refresh_p_agenda_table()

    def refresh_economy(self):
        self.refresh_x(
            self.contracts_table, ["Contracts Table"], self.get_contract_owner_list()
        )
        self.refresh_owners()

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
