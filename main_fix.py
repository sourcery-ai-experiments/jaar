# # command to for converting ui form to python file: pyuic5 ui\econMainUI.ui -o ui\econMainUI.py
from ui.MainWindowUI import Ui_MainWindow
from ui.EditMain import EditMainView
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
from src.econ.econ import econunit_shop
from src.econ.examples.econ_env_kit import (
    create_example_econs_list,
    setup_test_example_environment,
    create_example_econ,
    delete_dir_example_econ,
    change_econ_id_example_econ,
    get_test_econ_dir,
)

from src.agenda.party import get_depotlink_types
from src.instrument.file import open_file, dir_files
from ui.pyqt_func import agenda_importance_diplay


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

    def editmain_show(self):
        if self.main_window.ignore_agenda_x is None:
            self.main_window.plan = self.main_window.x_clerk.open_plan_file()
            self.editmain_view.agenda_x = self.main_window.plan
        else:
            self.editmain_view.agenda_x = self.main_window.ignore_agenda_x
        self.editmain_view.refresh_all()
        self.editmain_view.show()


class MainWindow(QMainWindow, Ui_MainWindow):
    """The main application window"""

    open_editmain = qtc.pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.setupUi(self)
        # signals for opening windows
        self.refresh_all_button.clicked.connect(self.refresh_all)
        self.econ_insert_button.clicked.connect(self.econ_insert)
        self.econ_load_button.clicked.connect(self.econ_load_from_file)
        self.econ_update_button.clicked.connect(self.econ_update_pid)
        self.econ_delete_button.clicked.connect(self.econ_delete)
        self.agenda_insert_button.clicked.connect(self.agenda_insert)
        self.agenda_update_button.clicked.connect(self.agenda_update_pid)
        self.agenda_delete_button.clicked.connect(self.agenda_delete)
        self.agendas_table.itemClicked.connect(self.agendas_table_select)
        self.worker_id_insert_button.clicked.connect(self.worker_id_insert)
        self.worker_id_update_button.clicked.connect(self.worker_id_update_pid)
        self.worker_id_delete_button.clicked.connect(self.worker_id_delete)
        self.worker_ids_table.itemClicked.connect(self.worker_ids_table_select)
        self.reload_forum_agendas_button.clicked.connect(self.reload_forum_agendas)
        self.set_forum_agenda_button.clicked.connect(self.save_output_agenda_to_forum)
        self.set_forum_and_reload_srcs_button.clicked.connect(
            self.set_forum_and_reload_srcs
        )
        self.ignores_table.itemClicked.connect(self.ignores_table_select)
        self.open_ignore_button.clicked.connect(self.open_editmain)
        self.save_ignore_button.clicked.connect(self.ignore_agenda_file_update)
        self.ignores_table.setHidden(True)
        self.show_ignores_button.clicked.connect(self.show_ignores_table)
        self.show_digests_button.clicked.connect(self.show_digests_table)
        self.plan_open_button.clicked.connect(self.open_editmain)
        self.plan_save_button.clicked.connect(self.save_plan)

        self.depotlink_insert_button.clicked.connect(self.depotlink_insert)
        self.depotlink_update_button.clicked.connect(self.depotlink_update)
        self.depotlink_delete_button.clicked.connect(self.depotlink_delete)
        self.depotlinks_table.itemClicked.connect(self.depotlinks_table_select)

        self.x_clerk = None
        self.econ_x = None
        self.ignore_agenda_x = None
        setup_test_example_environment()
        first_env = "ex5"
        self.econ_x = econunit_shop(econ_id=first_env, econ_dir=get_test_econ_dir())
        self.refresh_econ()
        self.econ_id_combo_refresh()
        self.econ_id_combo.setCurrentText(first_env)
        self._worker_id_load(clerk_id="ernie")

    def save_plan(self):
        if self.plan != None:
            self.x_clerk.save_plan_agenda(self.plan)
        self.refresh_worker_id()

    def reload_forum_agendas(self):
        if self.econ_x != None:
            self.econ_x.reload_all_clerkunits_forum_agendaunits()

    def set_forum_and_reload_srcs(self):
        self.save_output_agenda_to_forum()
        self.reload_forum_agendas()

    def save_output_agenda_to_forum(self):
        if self.x_clerk != None:
            self.x_clerk.save_output_agenda_to_forum()
        self.refresh_econ()

    def econ_load_from_file(self):
        econ_selected = self.econ_id_combo.currentText()
        self.econ_x = econunit_shop(econ_id=econ_selected, econ_dir=get_test_econ_dir())
        self.econ_x.set_econ_dirs(in_memory_treasury=False)
        self.econ_id.setText(econ_selected)
        self.refresh_econ()

    def agendas_table_select(self):
        self.agenda_worker_id.setText(
            self.agendas_table.item(self.agendas_table.currentRow(), 0).text()
        )
        if self.worker_ids_table.currentRow() != -1:
            selected_worker_id = self.worker_ids_table.item(
                self.worker_ids_table.currentRow(), 0
            ).text()
            selected_agenda = self.agendas_table.item(
                self.agendas_table.currentRow(), 0
            ).text()
            self.depotlink_pid.setText(f"{selected_worker_id} - {selected_agenda}")

    def worker_ids_table_select(self):
        x_clerk_id = self.worker_ids_table.item(
            self.worker_ids_table.currentRow(), 0
        ).text()
        self._worker_id_load(clerk_id=x_clerk_id)

    def _worker_id_load(self, clerk_id: str):
        self.econ_x.create_new_clerkunit(clerk_id=clerk_id)
        self.x_clerk = self.econ_x._clerkunits.get(clerk_id)
        self.clerk_id.setText(self.x_clerk._clerk_id)
        self.refresh_worker_id()

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
        ignore_agenda_worker_id = self.ignores_table.item(
            self.ignores_table.currentRow(), 0
        ).text()
        # self.ignore_agenda_x = self.econ_x.get_forum_agenda(
        self.ignore_agenda_x = self.econ_x.get_agenda_from_ignores_dir(
            clerk_id=self.x_clerk.pid, _worker_id=ignore_agenda_worker_id
        )
        self.edit_agenda = self.ignore_agenda_x

    def ignore_agenda_file_update(self):
        self.econ_x.set_ignore_agenda_file(
            clerk_id=self.x_clerk.pid, agenda_obj=self.ignore_agenda_x
        )
        self.refresh_worker_id()

    def show_ignores_table(self):
        self.ignores_table.setHidden(False)
        self.digests_table.setHidden(True)

    def show_digests_table(self):
        self.ignores_table.setHidden(True)
        self.digests_table.setHidden(False)

    def econ_insert(self):
        create_example_econ(econ_id=self.econ_id.text())
        self.econ_id_combo_refresh()

    def econ_update_pid(self):
        change_econ_id_example_econ(
            econ_obj=self.econ_x, new_party_id=self.econ_id.text()
        )
        self.econ_id_combo_refresh()

    def econ_delete(self):
        delete_dir_example_econ(econ_obj=self.econ_x)
        self.econ_x = None
        self.econ_id_combo_refresh()
        self.refresh_econ()

    def agenda_insert(self):
        self.econ_x.save_forum_agenda(
            agenda_x=agendaunit_shop(_worker_id=self.agenda_worker_id.text())
        )
        self.refresh_econ()

    def agenda_update_pid(self):
        currently_selected = self.agendas_table.item(
            self.agendas_table.currentRow(), 0
        ).text()
        typed_in = self.agenda_worker_id.text()
        if currently_selected != typed_in:
            self.econ_x.change_forum_worker_id(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_econ()

    def agenda_delete(self):
        self.econ_x.del_forum_agenda(
            agenda_x_label=self.agendas_table.item(
                self.agendas_table.currentRow(), 0
            ).text()
        )
        self.refresh_econ()

    def worker_id_insert(self):
        self.econ_x.create_new_clerkunit(clerk_id=self.clerk_id.text())
        self.refresh_worker_ids()

    def worker_id_update_pid(self):
        currently_selected = self.worker_ids_table.item(
            self.worker_ids_table.currentRow(), 0
        ).text()
        typed_in = self.clerk_id.text()
        if currently_selected != typed_in:
            self.econ_x.change_clerkunit_clerk_id(
                old_label=currently_selected, new_label=typed_in
            )
            self.refresh_worker_ids()

    def worker_id_delete(self):
        self.econ_x.del_clerkunit_dir(
            clerk_id=self.worker_ids_table.item(
                self.worker_ids_table.currentRow(), 0
            ).text()
        )
        self.refresh_worker_ids()

    def depotlink_insert(self):
        agenda_worker_id = self.agendas_table.item(
            self.agendas_table.currentRow(), 0
        ).text()
        if self.x_clerk != None:
            agenda_json = open_file(
                dest_dir=self.x_clerk._forum_dir,
                file_name=f"{agenda_worker_id}.json",
            )
            agenda_x = get_agenda_from_json(agenda_json)
            self.x_clerk.set_depot_agenda(
                agenda_x=agenda_x,
                depotlink_type=self.depotlink_type_combo.currentText(),
                depotlink_weight=self.depotlink_weight.text(),
            )
            self.econ_x.save_clerkunit_file(clerk_id=self.x_clerk.pid)
        self.refresh_worker_id()

    def depotlink_update(self):
        clerk_id_x = self.x_clerk.pid
        self.econ_x.update_depotlink(
            clerk_id=clerk_id_x,
            party_id=self.depotlink_pid.text(),
            depotlink_type=self.depotlink_type_combo.currentText(),
            creditor_weight=self.depotlink_weight.text(),
            debtor_weight=self.depotlink_weight.text(),
        )
        self.econ_x.save_clerkunit_file(clerk_id=clerk_id_x)
        self.refresh_worker_id()

    def depotlink_delete(self):
        clerk_id_x = self.x_clerk.pid
        self.econ_x.del_depotlink(
            clerk_id=clerk_id_x, agendaunit_worker_id=self.depotlink_pid.text()
        )
        self.econ_x.save_clerkunit_file(clerk_id=clerk_id_x)
        self.refresh_worker_id()

    def get_agenda_worker_id_list(self):
        return [[file_name] for file_name in dir_files(self.econ_x.get_forum_dir())]

    def get_clerk_id_list(self):
        worker_ids_worker_id_list = []
        if self.econ_x != None:
            worker_ids_worker_id_list.extend(
                [worker_id_dir]
                for worker_id_dir in self.econ_x.get_clerkunit_dir_paths_list()
            )
        return worker_ids_worker_id_list

    def get_depotlink_list(self):
        depotlinks_list = []
        if self.x_clerk != None:
            cl_dir = self.x_clerk._agendas_depot_dir
            clerkunit_files = dir_files(cl_dir)
            # for cl_val in self.x_clerk._depotlinks.values():
            for cl_filename in clerkunit_files:
                print(f"{cl_dir=} {cl_filename=}")
                agenda_json = open_file(cl_dir, file_name=f"{cl_filename}")
                cl_val = get_agenda_from_json(agenda_json)
                depotlink_row = [cl_val._worker_id, "", ""]
                depotlinks_list.append(depotlink_row)
        return depotlinks_list

    def get_digests_list(self):
        x_list = []
        if self.x_clerk != None:
            digest_file_list = dir_files(
                dir_path=self.x_clerk._agendas_digest_dir,
                delete_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_ignores_list(self):
        x_list = []
        if self.x_clerk != None:
            digest_file_list = dir_files(
                dir_path=self.x_clerk._agendas_ignore_dir,
                delete_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            x_list.extend([file] for file in digest_file_list)
        return x_list

    def get_p_ideas_list(self):
        x_list = []
        if self.worker_id_output_agenda != None:
            idea_list = self.worker_id_output_agenda.get_idea_tree_ordered_road_list()

            for idea_road in idea_list:
                idea_obj = self.worker_id_output_agenda.get_idea_obj(idea_road)

                if idea_obj._parent_road.find("time") != 3:
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
        if self.worker_id_output_agenda != None:
            x_list.extend(
                [
                    f"{agenda_importance_diplay(partyunit._agenda_credit)}/{agenda_importance_diplay(partyunit._agenda_debt)}",
                    partyunit.party_id,
                    f"{partyunit.creditor_weight}/{partyunit.debtor_weight}",
                ]
                for partyunit in self.worker_id_output_agenda._partys.values()
            )
        return x_list

    def get_p_groups_list(self):
        x_list = []
        if self.worker_id_output_agenda != None:
            x_list.extend(
                [
                    f"{agenda_importance_diplay(groupunit._agenda_debt)}/{agenda_importance_diplay(groupunit._agenda_credit)}",
                    groupunit.group_id,
                    len(groupunit._partys),
                ]
                for groupunit in self.worker_id_output_agenda._groups.values()
            )
        return x_list

    def get_p_beliefs_list(self):
        x_list = []
        if self.worker_id_output_agenda != None:
            for (
                beliefunit
            ) in self.worker_id_output_agenda._idearoot._beliefunits.values():
                open_nigh = ""
                if beliefunit.open is None and beliefunit.nigh is None:
                    open_nigh = ""
                else:
                    open_nigh = f"{beliefunit.open}-{beliefunit.nigh}"

                x_list.append(
                    [
                        beliefunit.base,
                        beliefunit.pick.replace(beliefunit.base, ""),
                        open_nigh,
                    ]
                )
        return x_list

    def get_p_intent_list(self):
        x_list = []
        if self.worker_id_output_agenda != None:
            intent_list = self.worker_id_output_agenda.get_intent_dict()
            intent_list.sort(key=lambda x: x._agenda_importance, reverse=True)
            x_list.extend(
                [
                    agenda_importance_diplay(intent_item._agenda_importance),
                    intent_item._label,
                    intent_item._parent_road,
                ]
                for intent_item in intent_list
            )
        return x_list

    def refresh_all(self):
        self.refresh_econ()

    def _sub_refresh_agents_table(self):
        self.refresh_x(
            self.worker_ids_table, ["worker_ids Table"], self.get_clerk_id_list()
        )

    def _sub_refresh_depotlinks_table(self):
        depotlink_types = list(get_depotlink_types())
        depotlink_types.insert(0, "")
        self.depotlink_type_combo.clear()
        self.depotlink_type_combo.addItems(depotlink_types)
        self.depotlink_type_combo.setCurrentText("")
        column_header = ""
        if self.x_clerk is None:
            column_header = "Agendalinks Table"
        elif self.x_clerk != None:
            column_header = f"'{self.x_clerk._clerk_id}' agendas"
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

    def _sub_refresh_p_beliefs_table(self):
        p_beliefs_list = self.get_p_beliefs_list()
        column_headers = [f"Bases ({len(p_beliefs_list)})", "Beliefs", "Open-Nigh"]

        self.refresh_x(
            table_x=self.w_beliefs_table,
            column_header=column_headers,
            populate_list=p_beliefs_list,
            column_width=[200, 100, 200],
        )

    def _sub_refresh_p_intent_table(self):
        p_intent_list = self.get_p_intent_list()
        column_headers = [
            "agenda_importance",
            f"Agenda ({len(p_intent_list)})",
            "Idea parent_road",
        ]

        self.refresh_x(
            table_x=self.w_intent_table,
            column_header=column_headers,
            populate_list=p_intent_list,
            column_width=[50, 200, 300],
        )

    def econ_id_combo_refresh(self):
        self.econ_id_combo.clear()
        self.econ_id_combo.addItems(create_example_econs_list())

    def refresh_worker_ids(self):
        self.x_clerk = None
        self._sub_refresh_agents_table()
        self.refresh_worker_id()

    def refresh_worker_id(self):
        self._sub_refresh_depotlinks_table()
        self._sub_refresh_digests_table()
        self._sub_refresh_ignores_table()
        self.worker_id_output_agenda = None
        if self.x_clerk != None:
            self.worker_id_output_agenda = self.x_clerk.get_remelded_output_agenda()
        self._sub_refresh_p_ideas_table()
        self._sub_refresh_p_partys_table()
        self._sub_refresh_p_groups_table()
        self._sub_refresh_p_beliefs_table()
        self._sub_refresh_p_intent_table()

    def refresh_econ(self):
        self.refresh_x(
            self.agendas_table,
            ["Econ Forum Agendas"],
            self.get_agenda_worker_id_list(),
        )
        self.refresh_worker_ids()

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
