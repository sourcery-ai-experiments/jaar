# # # command to for converting ui form to python file: pyuic5 ui\econMainUI.ui -o ui\econMainUI.py
# from ui.MainWindowUI import Ui_MainWindow
# from ui.EditMain import EditMainView
# from PyQt5 import QtCore as qtc
# from src.agenda.agenda import (
#     agendaunit_shop,
#     get_from_json as get_agenda_from_json,
# )
# from sys import argv as sys_argv, exit as sys_exit
# from PyQt5.QtWidgets import (
#     QTableWidgetItem as qtw1,
#     QApplication,
#     QMainWindow,
# )
# from src.money.econ import moneyunit_shop
# from src.money.examples.econ_env_kit import (
#     create_example_econs_list,
#     setup_test_example_environment,
#     create_example_econ,
#     delete_dir_example_econ,
#     modification_econ_id_example_econ,
#     temp_reals_dir,
# )
# from src._instrument.file import open_file, dir_files
# from ui.pyqt_func import agenda_importance_diplay


# class MainApp(QApplication):
#     """The main application object"""

#     def __init__(self, argv):
#         super().__init__(argv)

#         self.main_window = MainWindow()
#         self.main_window.show()

#         # create editmain instance
#         self.editmain_view = EditMainView()
#         # create slot for editmain visibility
#         self.main_window.open_editmain.connect(self.editmain_show)

#     def editmain_show(self):
#         if self.main_window.iggnore_agenda_x is None:
#             self.main_window.role = self.main_window.x_FunctionThatBuildsJob.open_role_file()
#             self.editmain_view.agenda_x = self.main_window.role
#         else:
#             self.editmain_view.agenda_x = self.main_window.iggnore_agenda_x
#         self.editmain_view.refresh_all()
#         self.editmain_view.show()


# class MainWindow(QMainWindow, Ui_MainWindow):
#     """The main application window"""

#     open_editmain = qtc.pyqtSignal(bool)

#     def __init__(self):
#         super().__init__()

#         self.setupUi(self)
#         # signals for opening windows
#         self.refresh_all_button.clicked.connect(self.refresh_all)
#         self.econ_insert_button.clicked.connect(self.econ_insert)
#         self.econ_load_button.clicked.connect(self.econ_load_from_file)
#         self.econ_update_button.clicked.connect(self.econ_update_pid)
#         self.econ_delete_button.clicked.connect(self.econ_delete)
#         self.agenda_insert_button.clicked.connect(self.agenda_insert)
#         self.agenda_update_button.clicked.connect(self.agenda_update_pid)
#         self.agenda_delete_button.clicked.connect(self.agenda_delete)
#         self.agendas_table.itemClicked.connect(self.agendas_table_select)
#         self.owner_id_insert_button.clicked.connect(self.owner_id_insert)
#         self.owner_id_update_button.clicked.connect(self.owner_id_update_pid)
#         self.owner_id_delete_button.clicked.connect(self.owner_id_delete)
#         self.owner_ids_table.itemClicked.connect(self.owner_ids_table_select)
#         self.reload_jobs_job_agendas_button.clicked.connect(
#             self.reload_jobs_job_agendas
#         )
#         self.set_job_agenda_button.clicked.connect(self.save_output_agenda_to_jobs)
#         self.set_jobs_and_reload_srcs_button.clicked.connect(
#             self.set_jobs_and_reload_srcs
#         )
#         self.iggnores_table.itemClicked.connect(self.iggnores_table_select)
#         self.open_iggnore_button.clicked.connect(self.open_editmain)
#         self.save_iggnore_button.clicked.connect(self.iggnore_agenda_file_update)
#         self.iggnores_table.setHidden(True)
#         self.show_iggnores_button.clicked.connect(self.show_iggnores_table)
#         self.show_digests_button.clicked.connect(self.show_digests_table)
#         self.role_open_button.clicked.connect(self.open_editmain)
#         self.role_save_button.clicked.connect(self.)

#         self.deiepotlink_insert_button.clicked.connect(self.deiepotlink_insert)
#         self.deiepotlink_update_button.clicked.connect(self.deiepotlink_update)
#         self.deiepotlink_delete_button.clicked.connect(self.deiepotlink_delete)
#         self.deiepotlinks_table.itemClicked.connect(self.deiepotlinks_table_select)

#         self.x_FunctionThatBuildsJob = None
#         self.econ_x = None
#         self.iggnore_agenda_x = None
#         setup_test_example_environment()
#         first_env = "ex5"
#         self.econ_x = moneyunit_shop(econ_id=first_env, econ_dir=temp_reals_dir())
#         self.refresh_econ()
#         self.econ_id_combo_refresh()
#         self.econ_id_combo.setCurrentText(first_env)
#         self._owner_id_load(FunctionThatBuildsJob_id="ernie")

#     def (self):
#         if self.role != None:
#             self.x_FunctionThatBuildsJob._agenda(self.role)
#         self.refresh_owner_id()

#     def reload_jobs_job_agendas(self):
#         if self.econ_x != None:
#             self.econ_x.reload_all_FunctionThatBuildsJobunits_job_agendas()

#     def set_jobs_and_reload_srcs(self):
#         self.save_output_agenda_to_jobs()
#         self.reload_jobs_job_agendas()

#     def save_output_agenda_to_jobs(self):
#         if self.x_FunctionThatBuildsJob != None:
#             self.x_FunctionThatBuildsJob.save_output_agenda_to_jobs()
#         self.refresh_econ()

#     def econ_load_from_file(self):
#         econ_selected = self.econ_id_combo.currentText()
#         self.econ_x = moneyunit_shop(econ_id=econ_selected, econ_dir=temp_reals_dir())
#         self.econ_x.create_treasury_db(in_memory=False)
#         self.econ_id.setText(econ_selected)
#         self.refresh_econ()

#     def agendas_table_select(self):
#         self.agenda_owner_id.setText(
#             self.agendas_table.item(self.agendas_table.currentRow(), 0).text()
#         )
#         if self.owner_ids_table.currentRow() != -1:
#             selected_owner_id = self.owner_ids_table.item(
#                 self.owner_ids_table.currentRow(), 0
#             ).text()
#             selected_agenda = self.agendas_table.item(
#                 self.agendas_table.currentRow(), 0
#             ).text()
#             self.deiepotlink_pid.setText(f"{selected_owner_id} - {selected_agenda}")

#     def owner_ids_table_select(self):
#         x_FunctionThatBuildsJob_id = self.owner_ids_table.item(
#             self.owner_ids_table.currentRow(), 0
#         ).text()
#         self._owner_id_load(FunctionThatBuildsJob_id=x_FunctionThatBuildsJob_id)

#     def _owner_id_load(self, FunctionThatBuildsJob_id: str):
#         self.econ_x.create_FunctionThatBuildsJobunit(FunctionThatBuildsJob_id=FunctionThatBuildsJob_id)
#         self.x_FunctionThatBuildsJob = self.econ_x._FunctionThatBuildsJobunits.get(FunctionThatBuildsJob_id)
#         self.FunctionThatBuildsJob_id.setText(self.x_FunctionThatBuildsJob._FunctionThatBuildsJob_id)
#         self.refresh_owner_id()

#     def deiepotlinks_table_select(self):
#         self.deiepotlink_pid.setText(
#             self.deiepotlinks_table.item(self.deiepotlinks_table.currentRow(), 0).text()
#         )
#         self.deiepotlink_type_combo.setCurrentText(
#             self.deiepotlinks_table.item(self.deiepotlinks_table.currentRow(), 1).text()
#         )
#         self.deiepotlink_weight.setText(
#             self.deiepotlinks_table.item(self.deiepotlinks_table.currentRow(), 2).text()
#         )

#     def iggnores_table_select(self):
#         iggnore_agenda_owner_id = self.iggnores_table.item(
#             self.iggnores_table.currentRow(), 0
#         ).text()
#         # self.iggnore_agenda_x = self.econ_x.(
#         self.iggnore_agenda_x = self.econ_x.get_agenda_from_iggnores_dir(
#             FunctionThatBuildsJob_id=self.x_FunctionThatBuildsJob.pid, _owner_id=iggnore_agenda_owner_id
#         )
#         self.edit_agenda = self.iggnore_agenda_x

#     def iggnore_agenda_file_update(self):
#         self.econ_x.set_iggnore_agenda_file(
#             FunctionThatBuildsJob_id=self.x_FunctionThatBuildsJob.pid, agenda_obj=self.iggnore_agenda_x
#         )
#         self.refresh_owner_id()

#     def show_iggnores_table(self):
#         self.iggnores_table.setHidden(False)
#         self.digests_table.setHidden(True)

#     def show_digests_table(self):
#         self.iggnores_table.setHidden(True)
#         self.digests_table.setHidden(False)

#     def econ_insert(self):
#         create_example_econ(econ_id=self.econ_id.text())
#         self.econ_id_combo_refresh()

#     def econ_update_pid(self):
#         modification_econ_id_example_econ(
#             econ_obj=self.econ_x, new_party_id=self.econ_id.text()
#         )
#         self.econ_id_combo_refresh()

#     def econ_delete(self):
#         delete_dir_example_econ(econ_obj=self.econ_x)
#         self.econ_x = None
#         self.econ_id_combo_refresh()
#         self.refresh_econ()

#     def agenda_insert(self):
#         self.econ_x._file(
#             agenda_x=agendaunit_shop(_owner_id=self.agenda_owner_id.text())
#         )
#         self.refresh_econ()

#     def agenda_update_pid(self):
#         currently_selected = self.agendas_table.item(
#             self.agendas_table.currentRow(), 0
#         ).text()
#         typed_in = self.agenda_owner_id.text()
#         if currently_selected != typed_in:
#             self.econ_x.modification_job_owner_id(
#                 old_label=currently_selected, new_label=typed_in
#             )
#             self.refresh_econ()

#     def agenda_delete(self):
#         self.econ_x.delete_job_file(
#             agenda_x_label=self.agendas_table.item(
#                 self.agendas_table.currentRow(), 0
#             ).text()
#         )
#         self.refresh_econ()

#     def owner_id_insert(self):
#         self.econ_x.create_FunctionThatBuildsJobunit(FunctionThatBuildsJob_id=self.FunctionThatBuildsJob_id.text())
#         self.refresh_owner_ids()

#     def owner_id_update_pid(self):
#         currently_selected = self.owner_ids_table.item(
#             self.owner_ids_table.currentRow(), 0
#         ).text()
#         typed_in = self.FunctionThatBuildsJob_id.text()
#         if currently_selected != typed_in:
#             self.econ_x.modification_FunctionThatBuildsJobunit_FunctionThatBuildsJob_id(
#                 old_label=currently_selected, new_label=typed_in
#             )
#             self.refresh_owner_ids()

#     def owner_id_delete(self):
#         self.econ_x.delete_FunctionThatBuildsJobunit(
#             FunctionThatBuildsJob_id=self.owner_ids_table.item(
#                 self.owner_ids_table.currentRow(), 0
#             ).text()
#         )
#         self.refresh_owner_ids()

#     def deiepotlink_insert(self):
#         agenda_owner_id = self.agendas_table.item(
#             self.agendas_table.currentRow(), 0
#         ).text()
#         if self.x_FunctionThatBuildsJob != None:
#             agenda_json = open_file(
#                 dest_dir=self.x_FunctionThatBuildsJob._jobs_dir,
#                 file_name=f"{agenda_owner_id}.json",
#             )
#             agenda_x = get_agenda_from_json(agenda_json)
#             self.x_FunctionThatBuildsJob.set_depot_agenda(agenda_x=agenda_x)
#             self.econ_x.save_FunctionThatBuildsJobunit_file(FunctionThatBuildsJob_id=self.x_FunctionThatBuildsJob.pid)
#         self.refresh_owner_id()

#     def deiepotlink_update(self):
#         FunctionThatBuildsJob_id_x = self.x_FunctionThatBuildsJob.pid
#         self.econ_x.update_deiepotlink(
#             FunctionThatBuildsJob_id=FunctionThatBuildsJob_id_x,
#             party_id=self.deiepotlink_pid.text(),
#             deiepotlink_type=self.deiepotlink_type_combo.currentText(),
#             credor_weight=self.deiepotlink_weight.text(),
#             debtor_weight=self.deiepotlink_weight.text(),
#         )
#         self.econ_x.save_FunctionThatBuildsJobunit_file(FunctionThatBuildsJob_id=FunctionThatBuildsJob_id_x)
#         self.refresh_owner_id()

#     def deiepotlink_delete(self):
#         FunctionThatBuildsJob_id_x = self.x_FunctionThatBuildsJob.pid
#         self.econ_x.del_deiepotlink(
#             FunctionThatBuildsJob_id=FunctionThatBuildsJob_id_x, agendaunit_owner_id=self.deiepotlink_pid.text()
#         )
#         self.econ_x.save_FunctionThatBuildsJobunit_file(FunctionThatBuildsJob_id=FunctionThatBuildsJob_id_x)
#         self.refresh_owner_id()

#     def get_agenda_owner_id_list(self):
#         return [[file_name] for file_name in dir_files(self.econ_x.get_jobs_dir())]

#     def get_FunctionThatBuildsJob_id_list(self):
#         owner_ids_owner_id_list = []
#         if self.econ_x != None:
#             owner_ids_owner_id_list.extend(
#                 [owner_id_dir]
#                 for owner_id_dir in self.econ_x.get_FunctionThatBuildsJobunit_dir_paths_list()
#             )
#         return owner_ids_owner_id_list

#     def get_deiepotlink_list(self):
#         deiepotlinks_list = []
#         if self.x_FunctionThatBuildsJob != None:
#             cl_dir = self.x_FunctionThatBuildsJob._agendas_depot_dir
#             FunctionThatBuildsJobunit_files = dir_files(cl_dir)
#             # for cl_val in self.x_FunctionThatBuildsJob._deiepotlinks.values():
#             for cl_filename in FunctionThatBuildsJobunit_files:
#                 print(f"{cl_dir=} {cl_filename=}")
#                 agenda_json = open_file(cl_dir, file_name=f"{cl_filename}")
#                 cl_val = get_agenda_from_json(agenda_json)
#                 deiepotlink_row = [cl_val._owner_id, "", ""]
#                 deiepotlinks_list.append(deiepotlink_row)
#         return deiepotlinks_list

#     def get_digests_list(self):
#         x_list = []
#         if self.x_FunctionThatBuildsJob != None:
#             digest_file_list = dir_files(
#                 dir_path=self.x_FunctionThatBuildsJob._agendas_digest_dir,
#                 delete_extensions=True,
#                 include_dirs=False,
#                 include_files=True,
#             )
#             x_list.extend([file] for file in digest_file_list)
#         return x_list

#     def get_iggnores_list(self):
#         x_list = []
#         if self.x_FunctionThatBuildsJob != None:
#             digest_file_list = dir_files(
#                 dir_path=self.x_FunctionThatBuildsJob._agendas_iggnore_dir,
#                 delete_extensions=True,
#                 include_dirs=False,
#                 include_files=True,
#             )
#             x_list.extend([file] for file in digest_file_list)
#         return x_list

#     def get_p_ideas_list(self):
#         x_list = []
#         if self.owner_id_output_agenda != None:
#             idea_list = self.owner_id_output_agenda.get_idea_tree_ordered_road_list()

#             for idea_road in idea_list:
#                 idea_obj = self.owner_id_output_agenda.get_idea_obj(idea_road)

#                 if idea_obj._parent_road.find("time") != 3:
#                     x_list.append(
#                         [
#                             agenda_importance_diplay(idea_obj._agenda_importance),
#                             idea_road,
#                             len(idea_obj._balancelinks),
#                         ]
#                     )

#         return x_list

#     def get_p_partys_list(self):
#         x_list = []
#         if self.owner_id_output_agenda != None:
#             x_list.extend(
#                 [
#                     f"{agenda_importance_diplay(partyunit._agenda_cred)}/{agenda_importance_diplay(partyunit._agenda_debt)}",
#                     partyunit.party_id,
#                     f"{partyunit.credor_weight}/{partyunit.debtor_weight}",
#                 ]
#                 for partyunit in self.owner_id_output_agenda._partys.values()
#             )
#         return x_list

#     def get_p_groups_list(self):
#         x_list = []
#         if self.owner_id_output_agenda != None:
#             x_list.extend(
#                 [
#                     f"{agenda_importance_diplay(groupunit._agenda_debt)}/{agenda_importance_diplay(groupunit._agenda_cred)}",
#                     groupunit.group_id,
#                     len(groupunit._partys),
#                 ]
#                 for groupunit in self.owner_id_output_agenda._groups.values()
#             )
#         return x_list

#     def get_p_beliefs_list(self):
#         x_list = []
#         if self.owner_id_output_agenda != None:
#             for (
#                 beliefunit
#             ) in self.owner_id_output_agenda._idearoot._beliefunits.values():
#                 open_nigh = ""
#                 if beliefunit.open is None and beliefunit.nigh is None:
#                     open_nigh = ""
#                 else:
#                     open_nigh = f"{beliefunit.open}-{beliefunit.nigh}"

#                 x_list.append(
#                     [
#                         beliefunit.base,
#                         beliefunit.pick.replace(beliefunit.base, ""),
#                         open_nigh,
#                     ]
#                 )
#         return x_list

#     def get_p_intent_list(self):
#         x_list = []
#         if self.owner_id_output_agenda != None:
#             intent_list = self.owner_id_output_agenda.get_intent_dict()
#             intent_list.sort(key=lambda x: x._agenda_importance, reverse=True)
#             x_list.extend(
#                 [
#                     agenda_importance_diplay(intent_item._agenda_importance),
#                     intent_item._label,
#                     intent_item._parent_road,
#                 ]
#                 for intent_item in intent_list
#             )
#         return x_list

#     def refresh_all(self):
#         self.refresh_econ()

#     def _sub_refresh_agents_table(self):
#         self.refresh_x(
#             self.owner_ids_table, ["owner_ids Table"], self.get_FunctionThatBuildsJob_id_list()
#         )

#     def _sub_refresh_deiepotlinks_table(self):
#         deiepotlink_types = list(get_deiepotlink_types())
#         deiepotlink_types.insert(0, "")
#         self.deiepotlink_type_combo.clear()
#         self.deiepotlink_type_combo.addItems(deiepotlink_types)
#         self.deiepotlink_type_combo.setCurrentText("")
#         column_header = ""
#         if self.x_FunctionThatBuildsJob is None:
#             column_header = "Agendalinks Table"
#         elif self.x_FunctionThatBuildsJob != None:
#             column_header = f"'{self.x_FunctionThatBuildsJob._FunctionThatBuildsJob_id}' agendas"
#         self.refresh_x(
#             self.deiepotlinks_table,
#             [column_header, "Link Type", "Weight"],
#             self.get_deiepotlink_list(),
#         )

#     def _sub_refresh_digests_table(self):
#         self.refresh_x(self.digests_table, ["digests_table"], self.get_digests_list())

#     def _sub_refresh_iggnores_table(self):
#         iggnores_list = self.get_iggnores_list()
#         if len(iggnores_list) >= 0:
#             column_headers = [
#                 f"iggnores Table ({len(iggnores_list)})",
#             ]
#         self.refresh_x(self.iggnores_table, column_headers, iggnores_list)

#     def _sub_refresh_p_ideas_table(self):
#         p_ideas_list = self.get_p_ideas_list()
#         if len(p_ideas_list) >= 0:
#             column_headers = [
#                 "agenda_importance",
#                 f"Ideas Table ({len(p_ideas_list)})",
#                 "balancelinks",
#             ]
#         else:
#             column_headers = [
#                 "agenda_importance",
#                 "Ideas Table",
#                 "balancelinks",
#             ]

#         self.w_ideas_table.setObjectName("Ideas Table")
#         self.w_ideas_table.setColumnHidden(0, False)
#         self.w_ideas_table.setColumnHidden(1, False)
#         self.w_ideas_table.setColumnHidden(2, False)
#         self.refresh_x(
#             table_x=self.w_ideas_table,
#             column_header=column_headers,
#             populate_list=p_ideas_list,
#             column_width=[50, 300, 50],
#         )

#     def _sub_refresh_p_partys_table(self):
#         p_partys_list = self.get_p_partys_list()
#         column_headers = [
#             "agenda_debt/agenda_cred",
#             f"Partys ({len(p_partys_list)})",
#             "credor_weight/debtor_weight",
#         ]

#         self.refresh_x(
#             table_x=self.w_partys_table,
#             column_header=column_headers,
#             populate_list=p_partys_list,
#             column_width=[50, 300, 50],
#         )

#     def _sub_refresh_p_groups_table(self):
#         p_groups_list = self.get_p_groups_list()
#         column_headers = [
#             "agenda_debt/agenda_cred",
#             f"groups ({len(p_groups_list)})",
#             "Partys",
#         ]

#         self.refresh_x(
#             table_x=self.w_groups_table,
#             column_header=column_headers,
#             populate_list=p_groups_list,
#             column_width=[50, 300, 100],
#         )

#     def _sub_refresh_p_beliefs_table(self):
#         p_beliefs_list = self.get_p_beliefs_list()
#         column_headers = [f"Bases ({len(p_beliefs_list)})", "Beliefs", "Open-Nigh"]

#         self.refresh_x(
#             table_x=self.w_beliefs_table,
#             column_header=column_headers,
#             populate_list=p_beliefs_list,
#             column_width=[200, 100, 200],
#         )

#     def _sub_refresh_p_intent_table(self):
#         p_intent_list = self.get_p_intent_list()
#         column_headers = [
#             "agenda_importance",
#             f"Agenda ({len(p_intent_list)})",
#             "Idea parent_road",
#         ]

#         self.refresh_x(
#             table_x=self.w_intent_table,
#             column_header=column_headers,
#             populate_list=p_intent_list,
#             column_width=[50, 200, 300],
#         )

#     def econ_id_combo_refresh(self):
#         self.econ_id_combo.clear()
#         self.econ_id_combo.addItems(create_example_econs_list())

#     def refresh_owner_ids(self):
#         self.x_FunctionThatBuildsJob = None
#         self._sub_refresh_agents_table()
#         self.refresh_owner_id()

#     def refresh_owner_id(self):
#         self._sub_refresh_deiepotlinks_table()
#         self._sub_refresh_digests_table()
#         self._sub_refresh_iggnores_table()
#         self.owner_id_output_agenda = None
#         if self.x_FunctionThatBuildsJob != None:
#             self.owner_id_output_agenda = self.x_FunctionThatBuildsJob.get_remelded_output_agenda()
#         self._sub_refresh_p_ideas_table()
#         self._sub_refresh_p_partys_table()
#         self._sub_refresh_p_groups_table()
#         self._sub_refresh_p_beliefs_table()
#         self._sub_refresh_p_intent_table()

#     def refresh_econ(self):
#         self.refresh_x(
#             self.agendas_table,
#             ["Econ jobs Agendas"],
#             self.get_agenda_owner_id_list(),
#         )
#         self.refresh_owner_ids()

#     def refresh_x(
#         self,
#         table_x,
#         column_header: list[str],
#         populate_list: list[any],
#         column_width: list[int] = None,
#     ):
#         table_x.setObjectName(column_header[0])
#         if column_width is None:
#             table_x.setColumnWidth(0, 150)
#             table_x.setColumnHidden(0, False)
#         else:
#             table_x.setColumnWidth(0, column_width[0])
#             table_x.setColumnWidth(1, column_width[1])
#             table_x.setColumnWidth(2, column_width[2])

#         table_x.clear()
#         table_x.setHorizontalHeaderLabels(column_header)
#         table_x.verticalHeader().setVisible(False)
#         table_x.setRowCount(0)
#         for row, list_x in enumerate(populate_list):
#             table_x.setRowCount(row + 1)
#             table_x.setRowHeight(row, 9)
#             print(f"{list_x=}")
#             if len(list_x) == 3:
#                 table_x.setHorizontalHeaderLabels(column_header)
#                 table_x.setItem(row, 0, qtw1(str(list_x[0])))
#                 table_x.setItem(row, 1, qtw1(str(list_x[1])))
#                 table_x.setItem(row, 2, qtw1(str(list_x[2])))
#             elif len(list_x) == 1:
#                 table_x.setItem(row, 0, qtw1(list_x[0]))


# if __name__ == "__main__":
#     app = MainApp(sys_argv)
#     sys_exit(app.exec())
