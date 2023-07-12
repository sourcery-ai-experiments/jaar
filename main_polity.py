# # command to for converting ui form to python file: pyuic5 ui\PolityMainUI.ui -o ui\PolityMainUI.py
from ui.PolityMainUI import Ui_MainWindow
from Edit5Issue import Edit5Issue
from EditMain import EditMainView
from PyQt5 import QtCore as qtc
from lib.agent.agent import AgentUnit
from sys import argv as sys_argv, exit as sys_exit
from PyQt5.QtWidgets import (
    QTableWidgetItem as qtw1,
    QApplication,
    QMainWindow,
)
from lib.polity.polity import PolityUnit
from lib.polity.test_polity.env_tools import (
    create_test_politys_list,
    setup_test_example_environment,
    create_test_polity,
    delete_dir_test_polity,
    rename_test_polity,
    get_test_politys_dir,
)
from lib.polity.agentlink import get_agentlink_types, agentlink_shop
from lib.agent.x_func import (
    open_file as x_func_open_file,
    dir_files as x_func_dir_files,
)
from lib.pyqt5_tools.pyqt_func import lw_diplay


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
        if self.main_window.ignore_agent_x != None:
            self.editmain_view.agent_x = self.main_window.ignore_agent_x
        else:
            self.main_window.starting_digest = (
                self.main_window.person_x.get_starting_digest_agent()
            )
            self.editmain_view.agent_x = self.main_window.starting_digest
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
        self.polity_insert_button.clicked.connect(self.polity_insert)
        self.polity_load_button.clicked.connect(self.polity_load_from_file)
        self.polity_update_button.clicked.connect(self.polity_update_name)
        self.polity_delete_button.clicked.connect(self.polity_delete)
        self.agent_insert_button.clicked.connect(self.agent_insert)
        self.agent_update_button.clicked.connect(self.agent_update_name)
        self.agent_delete_button.clicked.connect(self.agent_delete)
        self.agents_table.itemClicked.connect(self.agents_table_select)
        self.person_insert_button.clicked.connect(self.person_insert)
        self.person_update_button.clicked.connect(self.person_update_name)
        self.person_delete_button.clicked.connect(self.person_delete)
        self.persons_table.itemClicked.connect(self.persons_table_select)
        self.reload_all_src_agents_button.clicked.connect(self.reload_all_src_agents)
        self.set_public_agent_button.clicked.connect(
            self.set_dest_agent_to_public_agent
        )
        self.set_public_and_reload_srcs_button.clicked.connect(
            self.set_public_and_reload_srcs
        )
        self.ignores_table.itemClicked.connect(self.ignores_table_select)
        self.open_ignore_button.clicked.connect(self.open_editmain)
        self.save_ignore_button.clicked.connect(self.ignore_agent_file_update)
        self.ignores_table.setHidden(True)
        self.show_ignores_button.clicked.connect(self.show_ignores_table)
        self.show_digests_button.clicked.connect(self.show_digests_table)
        self.starting_digest_open_button.clicked.connect(self.open_editmain)
        self.starting_digest_save_button.clicked.connect(self.save_starting_digest)

        self.agentlink_insert_button.clicked.connect(self.agentlink_insert)
        self.agentlink_update_button.clicked.connect(self.agentlink_update)
        self.agentlink_delete_button.clicked.connect(self.agentlink_delete)
        self.agentlinks_table.itemClicked.connect(self.agentlinks_table_select)
        self.five_issue_button.clicked.connect(self.open_edit5issue)

        self.polity_x = None
        self.person_x = None
        self.ignore_agent_x = None
        setup_test_example_environment()
        first_env = "ex5"
        self.polity_x = PolityUnit(name=first_env, politys_dir=get_test_politys_dir())
        self.refresh_polity()
        self.polity_name_combo_refresh()
        self.polity_name_combo.setCurrentText(first_env)
        self._person_load(person_name="ernie")

    def save_starting_digest(self):
        if self.starting_digest != None:
            self.person_x.set_starting_digest_agent(self.starting_digest)
        self.refresh_person()

    def reload_all_src_agents(self):
        if self.polity_x != None:
            self.polity_x.reload_all_persons_src_agentunits()

    def set_public_and_reload_srcs(self):
        self.set_dest_agent_to_public_agent()
        self.reload_all_src_agents()

    def set_dest_agent_to_public_agent(self):
        if self.person_x != None:
            self.person_x.set_dest_agent_to_public_agent()
        self.refresh_polity()

    def polity_load_from_file(self):
        polity_selected = self.polity_name_combo.currentText()
        self.polity_x = PolityUnit(
            name=polity_selected, politys_dir=get_test_politys_dir()
        )
        self.polity_x.create_dirs_if_null(in_memory_bank=False)
        self.polity_name.setText(polity_selected)
        self.refresh_polity()

    def agents_table_select(self):
        self.agent_name.setText(
            self.agents_table.item(self.agents_table.currentRow(), 0).text()
        )
        if self.persons_table.currentRow() != -1:
            selected_person = self.persons_table.item(
                self.persons_table.currentRow(), 0
            ).text()
            selected_agent = self.agents_table.item(
                self.agents_table.currentRow(), 0
            ).text()
            self.agentlink_name.setText(f"{selected_person} - {selected_agent}")

    def persons_table_select(self):
        person_x_name = self.persons_table.item(
            self.persons_table.currentRow(), 0
        ).text()
        self._person_load(person_name=person_x_name)

    def _person_load(self, person_name: str):
        self.polity_x.load_personunit(name=person_name)
        self.person_x = self.polity_x._personunits.get(person_name)
        self.person_name.setText(self.person_x.name)
        self.refresh_person()

    def agentlinks_table_select(self):
        self.agentlink_name.setText(
            self.agentlinks_table.item(self.agentlinks_table.currentRow(), 0).text()
        )
        self.link_type_combo.setCurrentText(
            self.agentlinks_table.item(self.agentlinks_table.currentRow(), 1).text()
        )
        self.agentlink_weight.setText(
            self.agentlinks_table.item(self.agentlinks_table.currentRow(), 2).text()
        )

    def ignores_table_select(self):
        ignore_agent_desc = self.ignores_table.item(
            self.ignores_table.currentRow(), 0
        ).text()
        # self.ignore_agent_x = self.polity_x.get_agent_from_agents_dir(
        self.ignore_agent_x = self.polity_x.get_agent_from_ignores_dir(
            person_name=self.person_x.name, _desc=ignore_agent_desc
        )
        self.edit_agent = self.ignore_agent_x

    def ignore_agent_file_update(self):
        self.polity_x.set_ignore_agent_file(
            person_name=self.person_x.name, agent_obj=self.ignore_agent_x
        )
        self.refresh_person()

    def show_ignores_table(self):
        self.ignores_table.setHidden(False)
        self.digests_table.setHidden(True)

    def show_digests_table(self):
        self.ignores_table.setHidden(True)
        self.digests_table.setHidden(False)

    def polity_insert(self):
        create_test_polity(polity_name=self.polity_name.text())
        self.polity_name_combo_refresh()

    def polity_update_name(self):
        rename_test_polity(polity_obj=self.polity_x, new_name=self.polity_name.text())
        self.polity_name_combo_refresh()

    def polity_delete(self):
        delete_dir_test_polity(polity_obj=self.polity_x)
        self.polity_x = None
        self.polity_name_combo_refresh()
        self.refresh_polity()

    def agent_insert(self):
        self.polity_x.save_agentunit_obj_to_agents_dir(
            agent_x=AgentUnit(_desc=self.agent_name.text())
        )
        self.refresh_polity()

    def agent_update_name(self):
        currently_selected = self.agents_table.item(
            self.agents_table.currentRow(), 0
        ).text()
        typed_in = self.agent_name.text()
        if currently_selected != typed_in:
            self.polity_x.rename_agent_in_agents_dir(
                old_desc=currently_selected, new_desc=typed_in
            )
            self.refresh_polity()

    def agent_delete(self):
        self.polity_x.del_agentunit_from_agents_dir(
            agent_x_desc=self.agents_table.item(
                self.agents_table.currentRow(), 0
            ).text()
        )
        self.refresh_polity()

    def person_insert(self):
        self.polity_x.create_new_personunit(person_name=self.person_name.text())
        self.refresh_persons()

    def person_update_name(self):
        currently_selected = self.persons_table.item(
            self.persons_table.currentRow(), 0
        ).text()
        typed_in = self.person_name.text()
        if currently_selected != typed_in:
            self.polity_x.rename_personunit(
                old_desc=currently_selected, new_desc=typed_in
            )
            self.refresh_persons()

    def person_delete(self):
        self.polity_x.del_person_dir(
            person_name=self.persons_table.item(
                self.persons_table.currentRow(), 0
            ).text()
        )
        self.refresh_persons()

    def agentlink_insert(self):
        agent_desc = self.agents_table.item(self.agents_table.currentRow(), 0).text()
        if self.person_x != None:
            agent_json = x_func_open_file(
                dest_dir=self.person_x._public_agents_dir,
                file_name=f"{agent_desc}.json",
            )
            self.person_x.receive_src_agentunit_file(
                agent_json=agent_json,
                link_type=self.link_type_combo.currentText(),
                weight=self.agentlink_weight.text(),
            )
            self.polity_x.save_person_file(person_name=self.person_x.name)
        self.refresh_person()

    def agentlink_update(self):
        person_name_x = self.person_x.name
        new_agentlink = agentlink_shop(
            agent_desc=self.agentlink_name.text(),
            link_type=self.link_type_combo.currentText(),
            weight=self.agentlink_weight.text(),
        )

        self.polity_x.update_agentlink(
            person_name=person_name_x,
            agentlink=new_agentlink,
        )
        self.polity_x.save_person_file(person_name=person_name_x)
        self.refresh_person()

    def agentlink_delete(self):
        person_name_x = self.person_x.name
        self.polity_x.del_agentlink(
            person_name=person_name_x, agentunit_desc=self.agentlink_name.text()
        )
        self.polity_x.save_person_file(person_name=person_name_x)
        self.refresh_person()

    def get_agent_desc_list(self):
        agents_desc_list = []
        if self.polity_x != None:
            for agent in self.polity_x.get_agents_dir_list_of_obj():
                agents_desc_list.append([agent._desc])
        return agents_desc_list

    def get_person_desc_list(self):
        persons_desc_list = []
        if self.polity_x != None:
            for person_dir in self.polity_x.get_person_dir_paths_list():
                persons_desc_list.append([person_dir])
        return persons_desc_list

    def get_agentlink_list(self):
        agentlinks_list = []
        if self.person_x != None:
            for cl_val in self.person_x._src_agentlinks.values():
                agentlink_row = [
                    cl_val.agent_desc,
                    cl_val.link_type,
                    str(cl_val.weight),
                ]
                agentlinks_list.append(agentlink_row)
        return agentlinks_list

    def get_digests_list(self):
        x_list = []
        if self.person_x != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.person_x._digest_agents_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            for file in digest_file_list:
                x_list.append([file])

        return x_list

    def get_ignores_list(self):
        x_list = []
        if self.person_x != None:
            digest_file_list = x_func_dir_files(
                dir_path=self.person_x._ignore_agents_dir,
                remove_extensions=True,
                include_dirs=False,
                include_files=True,
            )
            for file in digest_file_list:
                x_list.append([file])

        return x_list

    def get_p_ideas_list(self):
        x_list = []
        if self.person_dest_agent != None:
            idea_list = self.person_dest_agent.get_idea_tree_ordered_road_list()

            for idea_road in idea_list:
                idea_obj = self.person_dest_agent.get_idea_kid(idea_road)

                if idea_obj._walk.find("time") != 3:
                    x_list.append(
                        [
                            lw_diplay(idea_obj._agent_importance),
                            idea_road,
                            len(idea_obj._brandlinks),
                        ]
                    )

        return x_list

    def get_p_allys_list(self):
        x_list = []
        if self.person_dest_agent != None:
            for allyunit in self.person_dest_agent._allys.values():
                x_list.append(
                    [
                        lw_diplay(allyunit._agent_importance),
                        allyunit.name,
                        allyunit.weight,
                    ]
                )

        return x_list

    def get_p_brands_list(self):
        x_list = []
        if self.person_dest_agent != None:
            for brandunit in self.person_dest_agent._brands.values():
                x_list.append(
                    [
                        lw_diplay(brandunit._agent_importance),
                        brandunit.name,
                        len(brandunit._allys),
                    ]
                )

        return x_list

    def get_p_acptfacts_list(self):
        x_list = []
        if self.person_dest_agent != None:
            for (
                acptfactunit
            ) in self.person_dest_agent._idearoot._acptfactunits.values():
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
        if self.person_dest_agent != None:
            agenda_list = self.person_dest_agent.get_agenda_items()
            agenda_list.sort(key=lambda x: x._agent_importance, reverse=True)
            for agenda_item in agenda_list:
                x_list.append(
                    [
                        lw_diplay(agenda_item._agent_importance),
                        agenda_item._desc,
                        agenda_item._walk,
                    ]
                )
        return x_list

    def refresh_all(self):
        self.refresh_polity()

    def _sub_refresh_persons_table(self):
        self.refresh_x(
            self.persons_table, ["Persons Table"], self.get_person_desc_list()
        )

    def _sub_refresh_agentlinks_table(self):
        agentlink_types = list(get_agentlink_types())
        agentlink_types.insert(0, "")
        self.link_type_combo.clear()
        self.link_type_combo.addItems(agentlink_types)
        self.link_type_combo.setCurrentText("")
        column_header = ""
        if self.person_x is None:
            column_header = f"Agentlinks Table"
        elif self.person_x != None:
            column_header = f"'{self.person_x.name}' Agentlinks"
        self.refresh_x(
            self.agentlinks_table,
            [column_header, "Link Type", "Weight"],
            self.get_agentlink_list(),
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
                "agent_importance",
                f"Ideas Table ({len(p_ideas_list)})",
                "brandlinks",
            ]
        else:
            column_headers = [
                "agent_importance",
                "Ideas Table",
                "brandlinks",
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

    def _sub_refresh_p_allys_table(self):
        p_allys_list = self.get_p_allys_list()
        column_headers = [
            "agent_importance",
            f"Allys ({len(p_allys_list)})",
            "Weight",
        ]

        self.refresh_x(
            table_x=self.w_allys_table,
            column_header=column_headers,
            populate_list=p_allys_list,
            column_width=[50, 300, 50],
        )

    def _sub_refresh_p_brands_table(self):
        p_brands_list = self.get_p_brands_list()
        column_headers = [
            "agent_importance",
            f"brands ({len(p_brands_list)})",
            "Allys",
        ]

        self.refresh_x(
            table_x=self.w_brands_table,
            column_header=column_headers,
            populate_list=p_brands_list,
            column_width=[50, 300, 100],
        )

    def _sub_refresh_p_acptfacts_table(self):
        p_acptfacts_list = self.get_p_acptfacts_list()
        column_headers = [
            f"Bases ({len(p_acptfacts_list)})",
            f"AcptFacts",
            "Open-Nigh",
        ]

        self.refresh_x(
            table_x=self.w_acptfacts_table,
            column_header=column_headers,
            populate_list=p_acptfacts_list,
            column_width=[200, 100, 200],
        )

    def _sub_refresh_p_agenda_table(self):
        p_agenda_list = self.get_p_agenda_list()
        column_headers = [
            f"agent_importance",
            f"Agenda ({len(p_agenda_list)})",
            "Idea Walk",
        ]

        self.refresh_x(
            table_x=self.w_agenda_table,
            column_header=column_headers,
            populate_list=p_agenda_list,
            column_width=[50, 200, 300],
        )

    def polity_name_combo_refresh(self):
        self.polity_name_combo.clear()
        self.polity_name_combo.addItems(create_test_politys_list())

    def refresh_persons(self):
        self.person_x = None
        self._sub_refresh_persons_table()
        self.refresh_person()

    def refresh_person(self):
        self._sub_refresh_agentlinks_table()
        self._sub_refresh_digests_table()
        self._sub_refresh_ignores_table()
        self.person_dest_agent = None
        if self.person_x != None:
            self.person_dest_agent = (
                self.person_x.get_dest_agent_from_digest_agent_files()
            )
        self._sub_refresh_p_ideas_table()
        self._sub_refresh_p_allys_table()
        self._sub_refresh_p_brands_table()
        self._sub_refresh_p_acptfacts_table()
        self._sub_refresh_p_agenda_table()

    def refresh_polity(self):
        self.refresh_x(self.agents_table, ["Agents Table"], self.get_agent_desc_list())
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
