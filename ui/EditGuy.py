# command to for converting ui form to python file: pyuic5 ui\EditGuyUI.ui -o ui\EditGuyUI.py
import sys
from ui.EditGuyUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from ui.EditGuy2bd import EditGuy2bd
from ui.pyqt_func import agenda_importance_diplay
from src.agenda.agenda import agendaunit_shop
from src.agenda.belief import beliefunit_shop
from src.agenda.guy import guylink_shop


class EditGuy(qtw.QTableWidget, Ui_Form):
    guy_selected = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.guy_table.itemClicked.connect(self.guy_select)
        self.guy_gui_insert_button.clicked.connect(self.guy_gui_insert)
        self.guy_update_button.clicked.connect(self.guy_update)
        self.guy_delete_button.clicked.connect(self.guy_delete)
        self.beliefs_in_table.itemClicked.connect(self.beliefs_in_select)
        self.beliefs_out_table.itemClicked.connect(self.beliefs_out_select)
        self.belief_insert_button.clicked.connect(self.belief_insert)
        self.belief_update_button.clicked.connect(self.belief_update)
        self.belief_delete_button.clicked.connect(self.belief_delete)
        self.guy_belief_set_button.clicked.connect(self.guy_belief_set)
        self.guy_belief_del_button.clicked.connect(self.guy_belief_del)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)
        self.selected_guy_id = None
        self.guyunit_x = None
        self.beliefunit_x = None

    def guy_select(self):
        guy_id = self.guy_table.item(self.guy_table.currentRow(), 0).text()
        self.guyunit_x = self.x_agenda._guys.get(guy_id)
        self.guy_id.setText(self.guyunit_x.pid)
        self.refresh_beliefs()

    def beliefs_in_select(self):
        belief_pid = self.beliefs_in_table.item(
            self.beliefs_in_table.currentRow(), 0
        ).text()
        self.beliefunit_x = self.x_agenda._beliefs.get(belief_pid)
        self.belief_pid.setText(self.beliefunit_x.belief_id)

    def beliefs_out_select(self):
        belief_pid = self.beliefs_out_table.item(
            self.beliefs_out_table.currentRow(), 0
        ).text()
        self.beliefunit_x = self.x_agenda._beliefs.get(belief_pid)
        self.belief_pid.setText(self.beliefunit_x.belief_id)

    def guy_belief_set(self):
        self.beliefunit_x.set_guylink(guylink=guylink_shop(guy_id=self.guyunit_x.pid))
        self.refresh_beliefs()

    def guy_belief_del(self):
        if self.beliefunit_x._guys.get(self.guyunit_x.pid) != None:
            self.beliefunit_x.del_guylink(pid=self.guyunit_x.pid)
        self.refresh_beliefs()

    def get_guy_belief_count(self, guy_id: str):  # GuyID):
        single_belief = ""
        beliefs_count = 0
        belief_guylinks = []
        for belief in self.x_agenda._beliefs.values():
            for guylink in belief._guys.values():
                if guylink.guy_id == guy_id and belief.belief_id != guylink.guy_id:
                    beliefs_count += 1
                    single_belief = belief.belief_id
                    belief_guylinks.append((belief, guylink))

        return beliefs_count, single_belief, belief_guylinks

    def refresh_guy_table(self):
        self.guy_table.setObjectName("Guys")
        self.guy_table.setColumnHidden(0, False)
        self.guy_table.setColumnWidth(0, 170)
        self.guy_table.setColumnWidth(1, 130)
        self.guy_table.setColumnWidth(2, 40)
        self.guy_table.setColumnWidth(3, 60)
        self.guy_table.setColumnWidth(4, 40)
        self.guy_table.setHorizontalHeaderLabels(
            ["Guy", "Belief", "Belief Count", "Agenda_Importance", "Weight"]
        )
        self.guy_table.setRowCount(0)

        guys_list = list(self.x_agenda._guys.values())
        guys_list.sort(key=lambda x: x.pid, reverse=False)

        for row, guy in enumerate(guys_list, start=1):
            # beliefs_count = 0
            # for belief in self.x_agenda._beliefs.values():
            #     for guylink in belief._guys.values():
            #         if guylink.guy_id == guy.pid:
            #             beliefs_count += 1

            beliefs_count, single_belief, belief_guylinks = self.get_guy_belief_count(
                guy_id=guy.pid
            )

            self.guy_table.setRowCount(row)
            self.guy_table.setItem(row - 1, 0, qtw.QTableWidgetItem(guy.pid))
            qt_agenda_cred = qtw.QTableWidgetItem(
                agenda_importance_diplay(guy._agenda_cred)
            )
            qt_agenda_debt = qtw.QTableWidgetItem(
                agenda_importance_diplay(guy._agenda_debt)
            )
            self.guy_table.setItem(row - 1, 1, qtw.QTableWidgetItem(single_belief))
            self.guy_table.setItem(row - 1, 2, qtw.QTableWidgetItem("#"))
            self.guy_table.setItem(row - 1, 3, qt_agenda_cred)
            # self.guy_table.setItem(row - 1, 3, qt_agenda_debt)
            self.guy_table.setItem(
                row - 1, 4, qtw.QTableWidgetItem(f"{guy.credor_weight}")
            )
            # self.guy_table.setItem(
            #     row - 1, 4, qtw.QTableWidgetItem(f"{guy.debtor_weight}")
            # )

    def guy_in_belief(self, guyunit, beliefunit):
        return any(
            guylink.guy_id == guyunit.guy_id for guylink in beliefunit._guys.values()
        )

    def refresh_beliefs_in_table(self):
        self.beliefs_in_table.setObjectName("Beliefs Linked")
        self.beliefs_in_table.setColumnHidden(0, False)
        self.beliefs_in_table.setColumnWidth(0, 170)
        self.beliefs_in_table.setColumnWidth(1, 130)
        self.beliefs_in_table.setColumnWidth(2, 40)
        self.beliefs_in_table.setColumnWidth(3, 60)
        self.beliefs_in_table.setColumnWidth(4, 40)
        self.beliefs_in_table.setRowCount(0)

        beliefs_in_list = [
            beliefunit
            for beliefunit in self.x_agenda._beliefs.values()
            if (
                self.guyunit_x != None
                and self.guy_in_belief(guyunit=self.guyunit_x, beliefunit=beliefunit)
                and self.guyunit_x.pid != beliefunit.belief_id
            )
        ]
        beliefs_in_list.sort(key=lambda x: x.belief_id, reverse=False)

        self.beliefs_in_table.setHorizontalHeaderLabels(
            [f"Beliefs ({len(beliefs_in_list)})", "Belief", "Belief Count"]
        )

        for row, beliefunit_x in enumerate(beliefs_in_list, start=1):
            self.beliefs_in_table.setRowCount(row)
            self.beliefs_in_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(beliefunit_x.belief_id)
            )

    def refresh_beliefs_out_table(self):
        self.beliefs_out_table.setObjectName("Beliefs Linked")
        self.beliefs_out_table.setColumnHidden(0, False)
        self.beliefs_out_table.setColumnWidth(0, 170)
        self.beliefs_out_table.setColumnWidth(1, 130)
        self.beliefs_out_table.setColumnWidth(2, 40)
        self.beliefs_out_table.setColumnWidth(3, 60)
        self.beliefs_out_table.setColumnWidth(4, 40)
        self.beliefs_out_table.setRowCount(0)

        beliefs_out_list = [
            beliefunit
            for beliefunit in self.x_agenda._beliefs.values()
            if (
                self.guyunit_x != None
                and beliefunit._guys.get(beliefunit.belief_id) is None
                and (
                    self.guy_in_belief(guyunit=self.guyunit_x, beliefunit=beliefunit)
                    is False
                )
            )
            or self.guyunit_x is None
        ]
        beliefs_out_list.sort(key=lambda x: x.belief_id, reverse=False)
        self.beliefs_out_table.setHorizontalHeaderLabels(
            [f"Beliefs ({len(beliefs_out_list)})", "Belief", "Belief Count"]
        )

        for row, beliefunit_x in enumerate(beliefs_out_list, start=1):
            self.beliefs_out_table.setRowCount(row)
            self.beliefs_out_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(beliefunit_x.belief_id)
            )

    def refresh_beliefs_stan_table(self):
        self.beliefs_stan_table.setObjectName("Beliefs Linked")
        self.beliefs_stan_table.setColumnHidden(0, False)
        self.beliefs_stan_table.setColumnWidth(0, 170)
        self.beliefs_stan_table.setColumnWidth(1, 130)
        self.beliefs_stan_table.setColumnWidth(2, 40)
        self.beliefs_stan_table.setColumnWidth(3, 60)
        self.beliefs_stan_table.setColumnWidth(4, 40)
        self.beliefs_stan_table.setRowCount(0)

        beliefs_stand_list = [
            beliefunit
            for beliefunit in self.x_agenda._beliefs.values()
            if self.guyunit_x != None
            and (
                beliefunit._guys.get(beliefunit.belief_id) != None
                and self.guyunit_x.pid == beliefunit.belief_id
            )
        ]
        beliefs_stand_list.sort(key=lambda x: x.belief_id, reverse=False)
        self.beliefs_stan_table.setHorizontalHeaderLabels(
            [f"Beliefs ({len(beliefs_stand_list)})", "Belief", "Belief Count"]
        )

        for row, beliefunit_x in enumerate(beliefs_stand_list, start=1):
            self.beliefs_stan_table.setRowCount(row)
            self.beliefs_stan_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(beliefunit_x.belief_id)
            )

    def refresh_all(self):
        self.refresh_guy_table()
        self.guy_id.setText("")
        self.refresh_beliefs()
        if self.belief_pid != None:
            self.belief_pid.setText("")

    def refresh_beliefs(self):
        self.refresh_beliefs_in_table()
        self.refresh_beliefs_out_table()
        self.refresh_beliefs_stan_table()

    def guy_gui_insert(self):
        self.x_agenda.add_guyunit(guy_id=self.guy_id.text())
        self.refresh_all()

    def guy_delete(self):
        self.x_agenda.del_guyunit(pid=self.guy_id.text())
        self.guy_id.setText("")
        self.guyunit_x = None
        self.refresh_all()

    def guy_update(self):
        self.x_agenda.edit_guyunit_guy_id(
            old_guy_id=self.guy_table.item(self.guy_table.currentRow(), 0).text(),
            new_guy_id=self.guy_id.text(),
            allow_guy_overwite=True,
            allow_nonsingle_belief_overwrite=True,
        )
        self.guy_id.setText("")
        self.refresh_all()

    def belief_insert(self):
        bu = beliefunit_shop(belief_id=self.belief_pid.text())
        self.x_agenda.set_beliefunit(y_beliefunit=bu)
        self.refresh_beliefs()

    def belief_delete(self):
        self.x_agenda.del_beliefunit(belief_id=self.belief_pid.text())
        self.belief_pid.setText("")
        self.refresh_beliefs()

    def belief_update(self):
        if self.belief_pid != None:
            self.x_agenda.edit_beliefunit_belief_id(
                old_belief_id=self.beliefs_in_table.item(
                    self.beliefs_in_table.currentRow(), 0
                ).text(),
                new_belief_id=self.belief_pid.text(),
                allow_belief_overwite=True,
            )
            self.belief_pid.setText("")
        self.refresh_beliefs()
