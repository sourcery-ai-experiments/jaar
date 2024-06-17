# command to for converting ui form to python file: pyuic5 ui\EditOtherUI.ui -o ui\EditOtherUI.py
import sys
from ui.EditOtherUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from ui.EditOther2bd import EditOther2bd
from ui.pyqt_func import agenda_importance_diplay
from src.agenda.agenda import agendaunit_shop
from src.agenda.belief import beliefunit_shop
from src.agenda.other import otherlink_shop


class EditOther(qtw.QTableWidget, Ui_Form):
    other_selected = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.other_table.itemClicked.connect(self.other_select)
        self.other_gui_insert_button.clicked.connect(self.other_gui_insert)
        self.other_update_button.clicked.connect(self.other_update)
        self.other_delete_button.clicked.connect(self.other_delete)
        self.beliefs_in_table.itemClicked.connect(self.beliefs_in_select)
        self.beliefs_out_table.itemClicked.connect(self.beliefs_out_select)
        self.belief_insert_button.clicked.connect(self.belief_insert)
        self.belief_update_button.clicked.connect(self.belief_update)
        self.belief_delete_button.clicked.connect(self.belief_delete)
        self.other_belief_set_button.clicked.connect(self.other_belief_set)
        self.other_belief_del_button.clicked.connect(self.other_belief_del)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)
        self.selected_other_id = None
        self.otherunit_x = None
        self.beliefunit_x = None

    def other_select(self):
        other_id = self.other_table.item(self.other_table.currentRow(), 0).text()
        self.otherunit_x = self.x_agenda._others.get(other_id)
        self.other_id.setText(self.otherunit_x.pid)
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

    def other_belief_set(self):
        self.beliefunit_x.set_otherlink(
            otherlink=otherlink_shop(other_id=self.otherunit_x.pid)
        )
        self.refresh_beliefs()

    def other_belief_del(self):
        if self.beliefunit_x._others.get(self.otherunit_x.pid) != None:
            self.beliefunit_x.del_otherlink(pid=self.otherunit_x.pid)
        self.refresh_beliefs()

    def get_other_belief_count(self, other_id: str):  # OtherID):
        single_belief = ""
        beliefs_count = 0
        belief_otherlinks = []
        for belief in self.x_agenda._beliefs.values():
            for otherlink in belief._others.values():
                if (
                    otherlink.other_id == other_id
                    and belief.belief_id != otherlink.other_id
                ):
                    beliefs_count += 1
                    single_belief = belief.belief_id
                    belief_otherlinks.append((belief, otherlink))

        return beliefs_count, single_belief, belief_otherlinks

    def refresh_other_table(self):
        self.other_table.setObjectName("Others")
        self.other_table.setColumnHidden(0, False)
        self.other_table.setColumnWidth(0, 170)
        self.other_table.setColumnWidth(1, 130)
        self.other_table.setColumnWidth(2, 40)
        self.other_table.setColumnWidth(3, 60)
        self.other_table.setColumnWidth(4, 40)
        self.other_table.setHorizontalHeaderLabels(
            ["Other", "Belief", "Belief Count", "Agenda_Importance", "Weight"]
        )
        self.other_table.setRowCount(0)

        others_list = list(self.x_agenda._others.values())
        others_list.sort(key=lambda x: x.pid, reverse=False)

        for row, other in enumerate(others_list, start=1):
            # beliefs_count = 0
            # for belief in self.x_agenda._beliefs.values():
            #     for otherlink in belief._others.values():
            #         if otherlink.other_id == other.pid:
            #             beliefs_count += 1

            beliefs_count, single_belief, belief_otherlinks = (
                self.get_other_belief_count(other_id=other.pid)
            )

            self.other_table.setRowCount(row)
            self.other_table.setItem(row - 1, 0, qtw.QTableWidgetItem(other.pid))
            qt_agenda_cred = qtw.QTableWidgetItem(
                agenda_importance_diplay(other._agenda_cred)
            )
            qt_agenda_debt = qtw.QTableWidgetItem(
                agenda_importance_diplay(other._agenda_debt)
            )
            self.other_table.setItem(row - 1, 1, qtw.QTableWidgetItem(single_belief))
            self.other_table.setItem(row - 1, 2, qtw.QTableWidgetItem("#"))
            self.other_table.setItem(row - 1, 3, qt_agenda_cred)
            # self.other_table.setItem(row - 1, 3, qt_agenda_debt)
            self.other_table.setItem(
                row - 1, 4, qtw.QTableWidgetItem(f"{other.credor_weight}")
            )
            # self.other_table.setItem(
            #     row - 1, 4, qtw.QTableWidgetItem(f"{other.debtor_weight}")
            # )

    def other_in_belief(self, otherunit, beliefunit):
        return any(
            otherlink.other_id == otherunit.other_id
            for otherlink in beliefunit._others.values()
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
                self.otherunit_x != None
                and self.other_in_belief(
                    otherunit=self.otherunit_x, beliefunit=beliefunit
                )
                and self.otherunit_x.pid != beliefunit.belief_id
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
                self.otherunit_x != None
                and beliefunit._others.get(beliefunit.belief_id) is None
                and (
                    self.other_in_belief(
                        otherunit=self.otherunit_x, beliefunit=beliefunit
                    )
                    is False
                )
            )
            or self.otherunit_x is None
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
            if self.otherunit_x != None
            and (
                beliefunit._others.get(beliefunit.belief_id) != None
                and self.otherunit_x.pid == beliefunit.belief_id
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
        self.refresh_other_table()
        self.other_id.setText("")
        self.refresh_beliefs()
        if self.belief_pid != None:
            self.belief_pid.setText("")

    def refresh_beliefs(self):
        self.refresh_beliefs_in_table()
        self.refresh_beliefs_out_table()
        self.refresh_beliefs_stan_table()

    def other_gui_insert(self):
        self.x_agenda.add_otherunit(other_id=self.other_id.text())
        self.refresh_all()

    def other_delete(self):
        self.x_agenda.del_otherunit(pid=self.other_id.text())
        self.other_id.setText("")
        self.otherunit_x = None
        self.refresh_all()

    def other_update(self):
        self.x_agenda.edit_otherunit_other_id(
            old_other_id=self.other_table.item(self.other_table.currentRow(), 0).text(),
            new_other_id=self.other_id.text(),
            allow_other_overwite=True,
            allow_nonsingle_belief_overwrite=True,
        )
        self.other_id.setText("")
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
