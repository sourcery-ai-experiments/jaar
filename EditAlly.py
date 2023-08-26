# command to for converting ui form to python file: pyuic5 ui\EditAllyUI.ui -o ui\EditAllyUI.py
import sys
from ui.EditAllyUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from EditAlly2bd import EditAlly2bd
from src.pyqt5_tools.pyqt_func import lw_diplay
from src.agent.agent import AgentUnit
from src.agent.tribe import tribeunit_shop
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
        self.tribes_in_table.itemClicked.connect(self.tribes_in_select)
        self.tribes_out_table.itemClicked.connect(self.tribes_out_select)
        self.tribe_insert_button.clicked.connect(self.tribe_insert)
        self.tribe_update_button.clicked.connect(self.tribe_update)
        self.tribe_delete_button.clicked.connect(self.tribe_delete)
        self.ally_tribe_set_button.clicked.connect(self.ally_tribe_set)
        self.ally_tribe_del_button.clicked.connect(self.ally_tribe_del)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)
        self.selected_ally_name = None
        self.allyunit_x = None
        self.tribeunit_x = None

    def ally_select(self):
        ally_name = self.ally_table.item(self.ally_table.currentRow(), 0).text()
        self.allyunit_x = self.agent_x._allys.get(ally_name)
        self.ally_name.setText(self.allyunit_x.name)
        self.refresh_tribes()

    def tribes_in_select(self):
        tribe_name = self.tribes_in_table.item(
            self.tribes_in_table.currentRow(), 0
        ).text()
        self.tribeunit_x = self.agent_x._tribes.get(tribe_name)
        self.tribe_name.setText(self.tribeunit_x.name)

    def tribes_out_select(self):
        tribe_name = self.tribes_out_table.item(
            self.tribes_out_table.currentRow(), 0
        ).text()
        self.tribeunit_x = self.agent_x._tribes.get(tribe_name)
        self.tribe_name.setText(self.tribeunit_x.name)

    def ally_tribe_set(self):
        self.tribeunit_x.set_allylink(allylink=allylink_shop(name=self.allyunit_x.name))
        self.refresh_tribes()

    def ally_tribe_del(self):
        if self.tribeunit_x._allys.get(self.allyunit_x.name) != None:
            self.tribeunit_x.del_allylink(name=self.allyunit_x.name)
        self.refresh_tribes()

    def get_ally_tribe_count(self, ally_name: str):  # AllyName):
        single_tribe = ""
        tribes_count = 0
        tribe_allylinks = []
        for tribe in self.agent_x._tribes.values():
            for allylink in tribe._allys.values():
                if allylink.name == ally_name and tribe.name != allylink.name:
                    tribes_count += 1
                    single_tribe = tribe.name
                    tribe_allylinks.append((tribe, allylink))

        return tribes_count, single_tribe, tribe_allylinks

    def refresh_ally_table(self):
        self.ally_table.setObjectName("Allys")
        self.ally_table.setColumnHidden(0, False)
        self.ally_table.setColumnWidth(0, 170)
        self.ally_table.setColumnWidth(1, 130)
        self.ally_table.setColumnWidth(2, 40)
        self.ally_table.setColumnWidth(3, 60)
        self.ally_table.setColumnWidth(4, 40)
        self.ally_table.setHorizontalHeaderLabels(
            ["Ally", "Tribe", "Tribe Count", "AGENT_Importance", "Weight"]
        )
        self.ally_table.setRowCount(0)

        allys_list = list(self.agent_x._allys.values())
        allys_list.sort(key=lambda x: x.name, reverse=False)

        for row, ally in enumerate(allys_list, start=1):
            # tribes_count = 0
            # for tribe in self.agent_x._tribes.values():
            #     for allylink in tribe._allys.values():
            #         if allylink.name == ally.name:
            #             tribes_count += 1

            tribes_count, single_tribe, tribe_allylinks = self.get_ally_tribe_count(
                ally_name=ally.name
            )

            self.ally_table.setRowCount(row)
            self.ally_table.setItem(row - 1, 0, qtw.QTableWidgetItem(ally.name))
            qt_agent_credit = qtw.QTableWidgetItem(lw_diplay(ally._agent_credit))
            qt_agent_debt = qtw.QTableWidgetItem(lw_diplay(ally._agent_debt))
            self.ally_table.setItem(row - 1, 1, qtw.QTableWidgetItem(single_tribe))
            self.ally_table.setItem(row - 1, 2, qtw.QTableWidgetItem("#"))
            self.ally_table.setItem(row - 1, 3, qt_agent_credit)
            # self.ally_table.setItem(row - 1, 3, qt_agent_debt)
            self.ally_table.setItem(
                row - 1, 4, qtw.QTableWidgetItem(f"{ally.creditor_weight}")
            )
            # self.ally_table.setItem(
            #     row - 1, 4, qtw.QTableWidgetItem(f"{ally.debtor_weight}")
            # )

    def ally_in_tribe(self, allyunit, tribeunit):
        return any(
            allylink.name == allyunit.name for allylink in tribeunit._allys.values()
        )

    def refresh_tribes_in_table(self):
        self.tribes_in_table.setObjectName("Tribes Linked")
        self.tribes_in_table.setColumnHidden(0, False)
        self.tribes_in_table.setColumnWidth(0, 170)
        self.tribes_in_table.setColumnWidth(1, 130)
        self.tribes_in_table.setColumnWidth(2, 40)
        self.tribes_in_table.setColumnWidth(3, 60)
        self.tribes_in_table.setColumnWidth(4, 40)
        self.tribes_in_table.setRowCount(0)

        tribes_in_list = [
            tribeunit
            for tribeunit in self.agent_x._tribes.values()
            if (
                self.allyunit_x != None
                and self.ally_in_tribe(allyunit=self.allyunit_x, tribeunit=tribeunit)
                and self.allyunit_x.name != tribeunit.name
            )
        ]
        tribes_in_list.sort(key=lambda x: x.name, reverse=False)

        self.tribes_in_table.setHorizontalHeaderLabels(
            [f"Tribes ({len(tribes_in_list)})", "Tribe", "Tribe Count"]
        )

        for row, tribeunit_x in enumerate(tribes_in_list, start=1):
            self.tribes_in_table.setRowCount(row)
            self.tribes_in_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(tribeunit_x.name)
            )

    def refresh_tribes_out_table(self):
        self.tribes_out_table.setObjectName("Tribes Linked")
        self.tribes_out_table.setColumnHidden(0, False)
        self.tribes_out_table.setColumnWidth(0, 170)
        self.tribes_out_table.setColumnWidth(1, 130)
        self.tribes_out_table.setColumnWidth(2, 40)
        self.tribes_out_table.setColumnWidth(3, 60)
        self.tribes_out_table.setColumnWidth(4, 40)
        self.tribes_out_table.setRowCount(0)

        tribes_out_list = [
            tribeunit
            for tribeunit in self.agent_x._tribes.values()
            if (
                self.allyunit_x != None
                and tribeunit._allys.get(tribeunit.name) is None
                and (
                    self.ally_in_tribe(allyunit=self.allyunit_x, tribeunit=tribeunit)
                    == False
                )
            )
            or self.allyunit_x is None
        ]
        tribes_out_list.sort(key=lambda x: x.name, reverse=False)
        self.tribes_out_table.setHorizontalHeaderLabels(
            [f"Tribes ({len(tribes_out_list)})", "Tribe", "Tribe Count"]
        )

        for row, tribeunit_x in enumerate(tribes_out_list, start=1):
            self.tribes_out_table.setRowCount(row)
            self.tribes_out_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(tribeunit_x.name)
            )

    def refresh_tribes_stan_table(self):
        self.tribes_stan_table.setObjectName("Tribes Linked")
        self.tribes_stan_table.setColumnHidden(0, False)
        self.tribes_stan_table.setColumnWidth(0, 170)
        self.tribes_stan_table.setColumnWidth(1, 130)
        self.tribes_stan_table.setColumnWidth(2, 40)
        self.tribes_stan_table.setColumnWidth(3, 60)
        self.tribes_stan_table.setColumnWidth(4, 40)
        self.tribes_stan_table.setRowCount(0)

        tribes_stand_list = [
            tribeunit
            for tribeunit in self.agent_x._tribes.values()
            if self.allyunit_x != None
            and (
                tribeunit._allys.get(tribeunit.name) != None
                and self.allyunit_x.name == tribeunit.name
            )
        ]
        tribes_stand_list.sort(key=lambda x: x.name, reverse=False)
        self.tribes_stan_table.setHorizontalHeaderLabels(
            [f"Tribes ({len(tribes_stand_list)})", "Tribe", "Tribe Count"]
        )

        for row, tribeunit_x in enumerate(tribes_stand_list, start=1):
            self.tribes_stan_table.setRowCount(row)
            self.tribes_stan_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(tribeunit_x.name)
            )

    def refresh_all(self):
        self.refresh_ally_table()
        self.ally_name.setText("")
        self.refresh_tribes()
        if self.tribe_name != None:
            self.tribe_name.setText("")

    def refresh_tribes(self):
        self.refresh_tribes_in_table()
        self.refresh_tribes_out_table()
        self.refresh_tribes_stan_table()

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
            allow_nonsingle_tribe_overwrite=True,
        )
        self.ally_name.setText("")
        self.refresh_all()

    def tribe_insert(self):
        bu = tribeunit_shop(name=self.tribe_name.text())
        self.agent_x.set_tribeunit(tribeunit=bu)
        self.refresh_tribes()

    def tribe_delete(self):
        self.agent_x.del_tribeunit(tribename=self.tribe_name.text())
        self.tribe_name.setText("")
        self.refresh_tribes()

    def tribe_update(self):
        if self.tribe_name != None:
            self.agent_x.edit_tribeunit_name(
                old_name=self.tribes_in_table.item(
                    self.tribes_in_table.currentRow(), 0
                ).text(),
                new_name=self.tribe_name.text(),
                allow_tribe_overwite=True,
            )
            self.tribe_name.setText("")
        self.refresh_tribes()
