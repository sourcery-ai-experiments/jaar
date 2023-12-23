# # command to for converting ui form to python file: pyuic5 ui\economyMainUI.ui -o ui\economyMainUI.py
from ui.EconomyMainUI import Ui_MainWindow
from Edit5Issue import Edit5Issue
from EditMain import EditMainView
from PyQt5 import QtCore as qtc
from src.agenda.agenda import (
    agendaunit_shop,
    get_from_json as get_agenda_from_json,
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
    change_economy_id_example_economy,
    get_test_economys_dir,
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
            self.main_window.contract = self.main_window.x_enact.open_contract_agenda()
            self.editmain_view.agenda_x = self.main_window.contract
        else:
            self.editmain_view.agenda_x = self.main_window.ignore_agenda_x
        self.editmain_view.refresh_all()
        self.editmain_view.show()

    def edit5issue_show(self):
        if self.main_window.x_enact != None:
            self.edit5issue_view.x_enact = self.main_window.x_enact
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
        self.economy_update_button.clicked.connect(self.economy_update_pid)
        self.economy_delete_button.clicked.connect(self.economy_delete)
        self.agenda_insert_button.clicked.connect(self.agenda_insert)
        self.agenda_update_button.clicked.connect(self.agenda_update_pid)
        self.agenda_delete_button.clicked.connect(self.agenda_delete)
        self.agendas_table.itemClicked.connect(self.agendas_table_select)
        self.healer_insert_button.clicked.connect(self.healer_insert)
        self.healer_update_button.clicked.connect(self.healer_update_pid)
        self.healer_delete_button.clicked.connect(self.healer_delete)
        self.healers_table.itemClicked.connect(self.healers_table_select)
        self.reload_all_src_agendas_button.clicked.connect(self.reload_all_src_agendas)
        self.set_public_agenda_button.clicked.connect(self.save_output_agenda_to_public)
        self.set_public_and_reload_srcs_button.clicked.connect(
            self.set_public_and_reload_srcs
        )
        self.ignores_table.itemClicked.connect(self.ignores_table_select)
        self.open_ignore_button.clicked.connect(self.open_editmain)
        self.save_ignore_button.clicked.connect(self.ignore_agenda_file_update)
        self.ignores_table.setHidden(True)
        self.show_ignores_button.clicked.connect(self.show_ignores_table)
        self.show_digests_button.clicked.connect(self.show_digests_table)
        self.contract_open_button.clicked.connect(self.open_editmain)
        self.contract_save_button.clicked.connect(self.save_contract)

        self.depotlink_insert_button.clicked.connect(self.depotlink_insert)
        self.depotlink_update_button.clicked.connect(self.depotlink_update)
        self.depotlink_delete_button.clicked.connect(self.depotlink_delete)
        self.depotlinks_table.itemClicked.connect(self.depotlinks_table_select)
        self.five_issue_button.clicked.connect(self.open_edit5issue)

        self.x_enact = None
        self.economy_x = None
        self.ignore_agenda_x = None
        setup_test_example_environment()
        first_env = "ex5"
        self.economy_x = economyunit_shop(
            economy_id=first_env, economys_dir=get_test_economys_dir()
        )
        self.refresh_economy()
        self.economy_id_combo_refresh()
        self.economy_id_combo.setCurrentText(first_env)
        self._healer_load(enact_cid="ernie")

    def save_contract(self):
        if self.contract != None:
            self.x_enact.save_contract_agenda(self.contract)
        self.refresh_healer()

    def reload_all_src_agendas(self):
        if self.economy_x != None:
            self.economy_x.reload_all_enactunits_src_agendaunits()

    def set_public_and_reload_srcs(self):
        self.save_output_agenda_to_public()
        self.reload_all_src_agendas()

    def save_output_agenda_to_public(self):
        if self.x_enact != None:
            self.x_enact.save_output_agenda_to_public()
        self.refresh_economy()

    def economy_load_from_file(self):
        economy_selected = self.economy_id_combo.currentText()
        self.economy_x = economyunit_shop(
            economy_id=economy_selected, economys_dir=get_test_economys_dir()
        )
        self.economy_x.create_dirs_if_null(in_memory_treasury=False)
        self.economy_id.setText(economy_selected)
        self.refresh_economy()

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
            self.depotlink_pid.setText(f"{selected_healer} - {selected_agenda}")

    def healers_table_select(self):
        x_enact_cid = self.healers_table.item(self.healers_table.currentRow(), 0).text()
        self._healer_load(enact_cid=x_enact_cid)

    def _healer_load(self, enact_cid: str):
        self.economy_x.create_new_enactunit(enact_cid=enact_cid)
        self.x_enact = self.economy_x._enactunits.get(enact_cid)
        self.enact_cid.setText(self.x_enact._enact_cid)
        self.refresh_healer()

    def depotlinks_table_select(self):
        self.depotlink_pid.setText(
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
        # self.ignore_agenda_x = self.economy_x.get_public_agenda(
        self.ignore_agenda_x = self.economy_x.get_agenda_from_ignores_dir(
            enact_cid=self.x_enact.pid, _healer=ignore_agenda_healer
        )
        self.edit_agenda = self.ignore_agenda_x

    def ignore_agenda_file_update(self):
        self.economy_x.set_ignore_agenda_file(
            enact_cid=self.x_enact.pid, agenda_obj=self.ignore_agenda_x
        )
        self.refresh_healer()

    def show_ignores_table(self):
        self.ignores_table.setHidden(False)
        self.digests_table.setHidden(True)

    def show_digests_table(self):
        self.ignores_table.setHidden(True)
        self.digests_table.setHidden(False)

    def economy_insert(self):
        create_example_economy(economy_id=self.economy_id.text())
        self.economy_id_combo_refresh()

    def economy_update_pid(self):
        change_economy_id_example_economy(
            economy_obj=self.economy_x, new_pid=self.economy_id.text()
        )
        self.economy_id_combo_refresh()

    def economy_delete(self):
        delete_dir_example_economy(economy_obj=self.economy_x)
        self.economy_x = None
        self.economy_id_combo_refresh()
        self.refresh_economy()

    def agenda_insert(self):
        self.economy_x.save_public_agenda(
            agenda_x=agendaunit_shop(_healer=self.agenda_healer.text())
        )
        self.refresh_economy()

    def agenda_update_pid(self):
        currently_selected = self.agendas_table.item(
            self.agendas_table.currentRow(), 0
        ).text()
        typed_in = self.agenda_healer.text()
        if currently_selected != typed_in:
            self.economy_x.change_public_agenda_healer(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_economy()

    def agenda_delete(self):
        self.economy_x.del_public_agenda(
            agenda_x_label=self.agendas_table.item(
                self.agendas_table.currentRow(), 0
            ).text()
        )
        self.refresh_economy()

    def healer_insert(self):
        self.economy_x.create_new_enactunit(enact_cid=self.enact_cid.text())
        self.refresh_healers()

    def healer_update_pid(self):
        currently_selected = self.healers_table.item(
            self.healers_table.currentRow(), 0
        ).text()
        typed_in = self.enact_cid.text()
        if currently_selected != typed_in:
            self.economy_x.change_enactunit_cid(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_healers()

    def healer_delete(self):
        self.economy_x.del_enactunit_dir(
            enact_cid=self.healers_table.item(self.healers_table.currentRow(), 0).text()
        )
        self.refresh_healers()

    def depotlink_insert(self):
        agenda_healer = self.agendas_table.item(
            self.agendas_table.currentRow(), 0
        ).text()
        if self.x_enact != None:
            agenda_json = x_func_open_file(
                dest_dir=self.x_enact._agendas_public_dir,
                file_name=f"{agenda_healer}.json",
            )
            agenda_x = get_agenda_from_json(agenda_json)
            self.x_enact.set_depot_agenda(
                agenda_x=agenda_x,
                depotlink_type=self.depotlink_type_combo.currentText(),
                depotlink_weight=self.depotlink_weight.text(),
            )
            self.economy_x.save_enactunit_file(enact_cid=self.x_enact.pid)
        self.refresh_healer()

    def depotlink_update(self):
        enact_cid_x = self.x_enact.pid
        self.economy_x.update_depotlink(
            enact_cid=enact_cid_x,
            partypid=self.depotlink_pid.text(),
            depotlink_type=self.depotlink_type_combo.currentText(),
            creditor_weight=self.depotlink_weight.text(),
            debtor_weight=self.depotlink_weight.text(),
        )
        self.economy_x.save_enactunit_file(enact_cid=enact_cid_x)
        self.refresh_healer()

    def depotlink_delete(self):
        enact_cid_x = self.x_enact.pid
        self.economy_x.del_depotlink(
            enact_cid=enact_cid_x, agendaunit_healer=self.depotlink_pid.text()
        )
        self.economy_x.save_enactunit_file(enact_cid=enact_cid_x)
        self.refresh_healer()

    def get_agenda_healer_list(self):
        agendas_list = []
        for file_name in x_func_dir_files(self.economy_x.get_public_dir()):
            # agenda_json = x_func_open_file(
            #     dest_dir=self.economy_x.get_public_dir(), file_name=file_name
            # )
            # x_agenda = get_agenda_from_json(x_agenda_json=agenda_json)
            agendas_list.append([file_name])
        return agendas_list

    def get_enact_cid_list(self):
        healers_healer_list = []
        if self.economy_x != None:
            healers_healer_list.extend(
                [healer_dir]
                for healer_dir in self.economy_x.get_enactunit_dir_paths_list()
            )
        return healers_healer_list

    def get_depotlink_list(self):
        depotlinks_list = []
        if self.x_enact != None:
            cl_dir = self.x_enact._agendas_depot_dir
            enactunit_files = x_func_dir_files(cl_dir)
            # for cl_val in self.x_enact._depotlinks.values():
            for cl_filename in enactunit_files:
                print(f"{cl_dir=} {cl_filename=}")
                agenda_json = x_func_open_file(cl_dir, file_name=f"{cl_filename}")
                cl_val = get_agenda_from_json(agenda_json)
                depotlink_row = [
                    cl_val._healer,
                    "",
                    "",
                ]
                depotlinks_list.append(depotlink_row)
        return depotlinks_list

    def get_digests_list(self):
        x_list = []
        if self.x_enact != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.x_enact._agendas_digest_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_ignores_list(self):
        x_list = []
        if self.x_enact != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.x_enact._agendas_ignore_dir,
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
                    partyunit.pid,
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

    def get_p_intent_list(self):
        x_list = []
        if self.healer_output_agenda != None:
            intent_list = self.healer_output_agenda.get_intent_items()
            intent_list.sort(key=lambda x: x._agenda_importance, reverse=True)
            x_list.extend(
                [
                    agenda_importance_diplay(intent_item._agenda_importance),
                    intent_item._label,
                    intent_item._pad,
                ]
                for intent_item in intent_list
            )
        return x_list

    def refresh_all(self):
        self.refresh_economy()

    def _sub_refresh_healers_table(self):
        self.refresh_x(self.healers_table, ["Healers Table"], self.get_enact_cid_list())

    def _sub_refresh_depotlinks_table(self):
        depotlink_types = list(get_depotlink_types())
        depotlink_types.insert(0, "")
        self.depotlink_type_combo.clear()
        self.depotlink_type_combo.addItems(depotlink_types)
        self.depotlink_type_combo.setCurrentText("")
        column_header = ""
        if self.x_enact is None:
            column_header = "Agendalinks Table"
        elif self.x_enact != None:
            column_header = f"'{self.x_enact._enact_cid}' agendas"
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

    def _sub_refresh_p_intent_table(self):
        p_intent_list = self.get_p_intent_list()
        column_headers = [
            "agenda_importance",
            f"Agenda ({len(p_intent_list)})",
            "Idea Pad",
        ]

        self.refresh_x(
            table_x=self.w_intent_table,
            column_header=column_headers,
            populate_list=p_intent_list,
            column_width=[50, 200, 300],
        )

    def economy_id_combo_refresh(self):
        self.economy_id_combo.clear()
        self.economy_id_combo.addItems(create_example_economys_list())

    def refresh_healers(self):
        self.x_enact = None
        self._sub_refresh_healers_table()
        self.refresh_healer()

    def refresh_healer(self):
        self._sub_refresh_depotlinks_table()
        self._sub_refresh_digests_table()
        self._sub_refresh_ignores_table()
        self.healer_output_agenda = None
        if self.x_enact != None:
            self.healer_output_agenda = self.x_enact.get_remelded_output_agenda()
        self._sub_refresh_p_ideas_table()
        self._sub_refresh_p_partys_table()
        self._sub_refresh_p_groups_table()
        self._sub_refresh_p_acptfacts_table()
        self._sub_refresh_p_intent_table()

    def refresh_economy(self):
        self.refresh_x(
            self.agendas_table,
            ["Economy Public Agendas"],
            self.get_agenda_healer_list(),
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
            print(f"{list_x=}")
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
