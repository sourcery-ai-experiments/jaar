# command to for converting ui form to python file: pyuic5 ui\EditAllyUI.ui -o ui\EditAllyUI.py
import sys
from ui.EditAllyUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from EditAlly2bd import EditAlly2bd
from src.pyqt5_tools.pyqt_func import lw_diplay
from src.agent.agent import AgentUnit
from src.agent.group import groupunit_shop
from src.agent.ally import allylink_shop


class EditAlly(qtw.QTableWidget, Ui_Form):
    ally_selected = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.ally_table.itemClicked.connect(self.ally_select)
        self.ally_insert_button.clicked.connect(self.ally_insert)
        self.ally_update_button.clicked.connect(self.ally_update)
        self.ally_delete_button.clicked.connect(self.ally_delete)
        self.groups_in_table.itemClicked.connect(self.groups_in_select)
        self.groups_out_table.itemClicked.connect(self.groups_out_select)
        self.group_insert_button.clicked.connect(self.group_insert)
        self.group_update_button.clicked.connect(self.group_update)
        self.group_delete_button.clicked.connect(self.group_delete)
        self.ally_group_set_button.clicked.connect(self.ally_group_set)
        self.ally_group_del_button.clicked.connect(self.ally_group_del)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)
        self.selected_ally_name = None
        self.allyunit_x = None
        self.groupunit_x = None

    def ally_select(self):
        ally_name = self.ally_table.item(self.ally_table.currentRow(), 0).text()
        self.allyunit_x = self.agent_x._allys.get(ally_name)
        self.ally_name.setText(self.allyunit_x.name)
        self.refresh_groups()

    def groups_in_select(self):
        group_name = self.groups_in_table.item(
            self.groups_in_table.currentRow(), 0
        ).text()
        self.groupunit_x = self.agent_x._groups.get(group_name)
        self.group_name.setText(self.groupunit_x.name)

    def groups_out_select(self):
        group_name = self.groups_out_table.item(
            self.groups_out_table.currentRow(), 0
        ).text()
        self.groupunit_x = self.agent_x._groups.get(group_name)
        self.group_name.setText(self.groupunit_x.name)

    def ally_group_set(self):
        self.groupunit_x.set_allylink(allylink=allylink_shop(name=self.allyunit_x.name))
        self.refresh_groups()

    def ally_group_del(self):
        if self.groupunit_x._allys.get(self.allyunit_x.name) != None:
            self.groupunit_x.del_allylink(name=self.allyunit_x.name)
        self.refresh_groups()

    def get_ally_group_count(self, ally_name: str):  # AllyName):
        single_group = ""
        groups_count = 0
        group_allylinks = []
        for group in self.agent_x._groups.values():
            for allylink in group._allys.values():
                if allylink.name == ally_name and group.name != allylink.name:
                    groups_count += 1
                    single_group = group.name
                    group_allylinks.append((group, allylink))

        return groups_count, single_group, group_allylinks

    def refresh_ally_table(self):
        self.ally_table.setObjectName("Allys")
        self.ally_table.setColumnHidden(0, False)
        self.ally_table.setColumnWidth(0, 170)
        self.ally_table.setColumnWidth(1, 130)
        self.ally_table.setColumnWidth(2, 40)
        self.ally_table.setColumnWidth(3, 60)
        self.ally_table.setColumnWidth(4, 40)
        self.ally_table.setHorizontalHeaderLabels(
            ["Ally", "Group", "Group Count", "AGENT_Importance", "Weight"]
        )
        self.ally_table.setRowCount(0)

        allys_list = list(self.agent_x._allys.values())
        allys_list.sort(key=lambda x: x.name, reverse=False)

        for row, ally in enumerate(allys_list, start=1):
            # groups_count = 0
            # for group in self.agent_x._groups.values():
            #     for allylink in group._allys.values():
            #         if allylink.name == ally.name:
            #             groups_count += 1

            groups_count, single_group, group_allylinks = self.get_ally_group_count(
                ally_name=ally.name
            )

            self.ally_table.setRowCount(row)
            self.ally_table.setItem(row - 1, 0, qtw.QTableWidgetItem(ally.name))
            qt_agent_credit = qtw.QTableWidgetItem(lw_diplay(ally._agent_credit))
            qt_agent_debt = qtw.QTableWidgetItem(lw_diplay(ally._agent_debt))
            self.ally_table.setItem(row - 1, 1, qtw.QTableWidgetItem(single_group))
            self.ally_table.setItem(row - 1, 2, qtw.QTableWidgetItem("#"))
            self.ally_table.setItem(row - 1, 3, qt_agent_credit)
            # self.ally_table.setItem(row - 1, 3, qt_agent_debt)
            self.ally_table.setItem(
                row - 1, 4, qtw.QTableWidgetItem(f"{ally.creditor_weight}")
            )
            # self.ally_table.setItem(
            #     row - 1, 4, qtw.QTableWidgetItem(f"{ally.debtor_weight}")
            # )

    def ally_in_group(self, allyunit, groupunit):
        return any(
            allylink.name == allyunit.name for allylink in groupunit._allys.values()
        )

    def refresh_groups_in_table(self):
        self.groups_in_table.setObjectName("Groups Linked")
        self.groups_in_table.setColumnHidden(0, False)
        self.groups_in_table.setColumnWidth(0, 170)
        self.groups_in_table.setColumnWidth(1, 130)
        self.groups_in_table.setColumnWidth(2, 40)
        self.groups_in_table.setColumnWidth(3, 60)
        self.groups_in_table.setColumnWidth(4, 40)
        self.groups_in_table.setRowCount(0)

        groups_in_list = [
            groupunit
            for groupunit in self.agent_x._groups.values()
            if (
                self.allyunit_x != None
                and self.ally_in_group(allyunit=self.allyunit_x, groupunit=groupunit)
                and self.allyunit_x.name != groupunit.name
            )
        ]
        groups_in_list.sort(key=lambda x: x.name, reverse=False)

        self.groups_in_table.setHorizontalHeaderLabels(
            [f"Groups ({len(groups_in_list)})", "Group", "Group Count"]
        )

        for row, groupunit_x in enumerate(groups_in_list, start=1):
            self.groups_in_table.setRowCount(row)
            self.groups_in_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(groupunit_x.name)
            )

    def refresh_groups_out_table(self):
        self.groups_out_table.setObjectName("Groups Linked")
        self.groups_out_table.setColumnHidden(0, False)
        self.groups_out_table.setColumnWidth(0, 170)
        self.groups_out_table.setColumnWidth(1, 130)
        self.groups_out_table.setColumnWidth(2, 40)
        self.groups_out_table.setColumnWidth(3, 60)
        self.groups_out_table.setColumnWidth(4, 40)
        self.groups_out_table.setRowCount(0)

        groups_out_list = [
            groupunit
            for groupunit in self.agent_x._groups.values()
            if (
                self.allyunit_x != None
                and groupunit._allys.get(groupunit.name) is None
                and (
                    self.ally_in_group(allyunit=self.allyunit_x, groupunit=groupunit)
                    == False
                )
            )
            or self.allyunit_x is None
        ]
        groups_out_list.sort(key=lambda x: x.name, reverse=False)
        self.groups_out_table.setHorizontalHeaderLabels(
            [f"Groups ({len(groups_out_list)})", "Group", "Group Count"]
        )

        for row, groupunit_x in enumerate(groups_out_list, start=1):
            self.groups_out_table.setRowCount(row)
            self.groups_out_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(groupunit_x.name)
            )

    def refresh_groups_stan_table(self):
        self.groups_stan_table.setObjectName("Groups Linked")
        self.groups_stan_table.setColumnHidden(0, False)
        self.groups_stan_table.setColumnWidth(0, 170)
        self.groups_stan_table.setColumnWidth(1, 130)
        self.groups_stan_table.setColumnWidth(2, 40)
        self.groups_stan_table.setColumnWidth(3, 60)
        self.groups_stan_table.setColumnWidth(4, 40)
        self.groups_stan_table.setRowCount(0)

        groups_stand_list = [
            groupunit
            for groupunit in self.agent_x._groups.values()
            if self.allyunit_x != None
            and (
                groupunit._allys.get(groupunit.name) != None
                and self.allyunit_x.name == groupunit.name
            )
        ]
        groups_stand_list.sort(key=lambda x: x.name, reverse=False)
        self.groups_stan_table.setHorizontalHeaderLabels(
            [f"Groups ({len(groups_stand_list)})", "Group", "Group Count"]
        )

        for row, groupunit_x in enumerate(groups_stand_list, start=1):
            self.groups_stan_table.setRowCount(row)
            self.groups_stan_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(groupunit_x.name)
            )

    def refresh_all(self):
        self.refresh_ally_table()
        self.ally_name.setText("")
        self.refresh_groups()
        if self.group_name != None:
            self.group_name.setText("")

    def refresh_groups(self):
        self.refresh_groups_in_table()
        self.refresh_groups_out_table()
        self.refresh_groups_stan_table()

    def ally_insert(self):
        self.agent_x.add_allyunit(name=self.ally_name.text())
        self.refresh_all()

    def ally_delete(self):
        self.agent_x.del_allyunit(name=self.ally_name.text())
        self.ally_name.setText("")
        self.allyunit_x = None
        self.refresh_all()

    def ally_update(self):
        self.agent_x.edit_allyunit_name(
            old_name=self.ally_table.item(self.ally_table.currentRow(), 0).text(),
            new_name=self.ally_name.text(),
            allow_ally_overwite=True,
            allow_nonsingle_group_overwrite=True,
        )
        self.ally_name.setText("")
        self.refresh_all()

    def group_insert(self):
        bu = groupunit_shop(name=self.group_name.text())
        self.agent_x.set_groupunit(groupunit=bu)
        self.refresh_groups()

    def group_delete(self):
        self.agent_x.del_groupunit(groupname=self.group_name.text())
        self.group_name.setText("")
        self.refresh_groups()

    def group_update(self):
        if self.group_name != None:
            self.agent_x.edit_groupunit_name(
                old_name=self.groups_in_table.item(
                    self.groups_in_table.currentRow(), 0
                ).text(),
                new_name=self.group_name.text(),
                allow_group_overwite=True,
            )
            self.group_name.setText("")
        self.refresh_groups()
