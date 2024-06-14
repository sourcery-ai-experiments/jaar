# command to for converting ui form to python file: pyuic5 ui\EditPartyUI.ui -o ui\EditPartyUI.py
import sys
from ui.EditPartyUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from ui.EditParty2bd import EditParty2bd
from ui.pyqt_func import agenda_importance_diplay
from src.agenda.agenda import agendaunit_shop
from src.agenda.belief import beliefunit_shop
from src.agenda.party import partylink_shop


class EditParty(qtw.QTableWidget, Ui_Form):
    party_selected = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.party_table.itemClicked.connect(self.party_select)
        self.party_gui_insert_button.clicked.connect(self.party_gui_insert)
        self.party_update_button.clicked.connect(self.party_update)
        self.party_delete_button.clicked.connect(self.party_delete)
        self.beliefs_in_table.itemClicked.connect(self.beliefs_in_select)
        self.beliefs_out_table.itemClicked.connect(self.beliefs_out_select)
        self.belief_insert_button.clicked.connect(self.belief_insert)
        self.belief_update_button.clicked.connect(self.belief_update)
        self.belief_delete_button.clicked.connect(self.belief_delete)
        self.party_belief_set_button.clicked.connect(self.party_belief_set)
        self.party_belief_del_button.clicked.connect(self.party_belief_del)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)
        self.selected_party_id = None
        self.partyunit_x = None
        self.beliefunit_x = None

    def party_select(self):
        party_id = self.party_table.item(self.party_table.currentRow(), 0).text()
        self.partyunit_x = self.x_agenda._partys.get(party_id)
        self.party_id.setText(self.partyunit_x.pid)
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

    def party_belief_set(self):
        self.beliefunit_x.set_partylink(
            partylink=partylink_shop(party_id=self.partyunit_x.pid)
        )
        self.refresh_beliefs()

    def party_belief_del(self):
        if self.beliefunit_x._partys.get(self.partyunit_x.pid) != None:
            self.beliefunit_x.del_partylink(pid=self.partyunit_x.pid)
        self.refresh_beliefs()

    def get_party_belief_count(self, party_id: str):  # PartyID):
        single_belief = ""
        beliefs_count = 0
        belief_partylinks = []
        for belief in self.x_agenda._beliefs.values():
            for partylink in belief._partys.values():
                if (
                    partylink.party_id == party_id
                    and belief.belief_id != partylink.party_id
                ):
                    beliefs_count += 1
                    single_belief = belief.belief_id
                    belief_partylinks.append((belief, partylink))

        return beliefs_count, single_belief, belief_partylinks

    def refresh_party_table(self):
        self.party_table.setObjectName("Partys")
        self.party_table.setColumnHidden(0, False)
        self.party_table.setColumnWidth(0, 170)
        self.party_table.setColumnWidth(1, 130)
        self.party_table.setColumnWidth(2, 40)
        self.party_table.setColumnWidth(3, 60)
        self.party_table.setColumnWidth(4, 40)
        self.party_table.setHorizontalHeaderLabels(
            ["Party", "Belief", "Belief Count", "Agenda_Importance", "Weight"]
        )
        self.party_table.setRowCount(0)

        partys_list = list(self.x_agenda._partys.values())
        partys_list.sort(key=lambda x: x.pid, reverse=False)

        for row, party in enumerate(partys_list, start=1):
            # beliefs_count = 0
            # for belief in self.x_agenda._beliefs.values():
            #     for partylink in belief._partys.values():
            #         if partylink.party_id == party.pid:
            #             beliefs_count += 1

            beliefs_count, single_belief, belief_partylinks = (
                self.get_party_belief_count(party_id=party.pid)
            )

            self.party_table.setRowCount(row)
            self.party_table.setItem(row - 1, 0, qtw.QTableWidgetItem(party.pid))
            qt_agenda_cred = qtw.QTableWidgetItem(
                agenda_importance_diplay(party._agenda_cred)
            )
            qt_agenda_debt = qtw.QTableWidgetItem(
                agenda_importance_diplay(party._agenda_debt)
            )
            self.party_table.setItem(row - 1, 1, qtw.QTableWidgetItem(single_belief))
            self.party_table.setItem(row - 1, 2, qtw.QTableWidgetItem("#"))
            self.party_table.setItem(row - 1, 3, qt_agenda_cred)
            # self.party_table.setItem(row - 1, 3, qt_agenda_debt)
            self.party_table.setItem(
                row - 1, 4, qtw.QTableWidgetItem(f"{party.credor_weight}")
            )
            # self.party_table.setItem(
            #     row - 1, 4, qtw.QTableWidgetItem(f"{party.debtor_weight}")
            # )

    def party_in_belief(self, partyunit, beliefunit):
        return any(
            partylink.party_id == partyunit.party_id
            for partylink in beliefunit._partys.values()
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
                self.partyunit_x != None
                and self.party_in_belief(
                    partyunit=self.partyunit_x, beliefunit=beliefunit
                )
                and self.partyunit_x.pid != beliefunit.belief_id
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
                self.partyunit_x != None
                and beliefunit._partys.get(beliefunit.belief_id) is None
                and (
                    self.party_in_belief(
                        partyunit=self.partyunit_x, beliefunit=beliefunit
                    )
                    is False
                )
            )
            or self.partyunit_x is None
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
            if self.partyunit_x != None
            and (
                beliefunit._partys.get(beliefunit.belief_id) != None
                and self.partyunit_x.pid == beliefunit.belief_id
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
        self.refresh_party_table()
        self.party_id.setText("")
        self.refresh_beliefs()
        if self.belief_pid != None:
            self.belief_pid.setText("")

    def refresh_beliefs(self):
        self.refresh_beliefs_in_table()
        self.refresh_beliefs_out_table()
        self.refresh_beliefs_stan_table()

    def party_gui_insert(self):
        self.x_agenda.add_partyunit(party_id=self.party_id.text())
        self.refresh_all()

    def party_delete(self):
        self.x_agenda.del_partyunit(pid=self.party_id.text())
        self.party_id.setText("")
        self.partyunit_x = None
        self.refresh_all()

    def party_update(self):
        self.x_agenda.edit_partyunit_party_id(
            old_party_id=self.party_table.item(self.party_table.currentRow(), 0).text(),
            new_party_id=self.party_id.text(),
            allow_party_overwite=True,
            allow_nonsingle_belief_overwrite=True,
        )
        self.party_id.setText("")
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
