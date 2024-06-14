# command to for converting ui form to python file: pyuic5 ui\EditPartyUI.ui -o ui\EditPartyUI.py
import sys
from ui.EditPartyUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from ui.EditParty2bd import EditParty2bd
from ui.pyqt_func import agenda_importance_diplay
from src.agenda.agenda import agendaunit_shop
from src.agenda.idea import ideaunit_shop
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
        self.ideas_in_table.itemClicked.connect(self.ideas_in_select)
        self.ideas_out_table.itemClicked.connect(self.ideas_out_select)
        self.idea_insert_button.clicked.connect(self.idea_insert)
        self.idea_update_button.clicked.connect(self.idea_update)
        self.idea_delete_button.clicked.connect(self.idea_delete)
        self.party_idea_set_button.clicked.connect(self.party_idea_set)
        self.party_idea_del_button.clicked.connect(self.party_idea_del)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)
        self.selected_party_id = None
        self.partyunit_x = None
        self.ideaunit_x = None

    def party_select(self):
        party_id = self.party_table.item(self.party_table.currentRow(), 0).text()
        self.partyunit_x = self.x_agenda._partys.get(party_id)
        self.party_id.setText(self.partyunit_x.pid)
        self.refresh_ideas()

    def ideas_in_select(self):
        idea_pid = self.ideas_in_table.item(self.ideas_in_table.currentRow(), 0).text()
        self.ideaunit_x = self.x_agenda._ideas.get(idea_pid)
        self.idea_pid.setText(self.ideaunit_x.idea_id)

    def ideas_out_select(self):
        idea_pid = self.ideas_out_table.item(
            self.ideas_out_table.currentRow(), 0
        ).text()
        self.ideaunit_x = self.x_agenda._ideas.get(idea_pid)
        self.idea_pid.setText(self.ideaunit_x.idea_id)

    def party_idea_set(self):
        self.ideaunit_x.set_partylink(
            partylink=partylink_shop(party_id=self.partyunit_x.pid)
        )
        self.refresh_ideas()

    def party_idea_del(self):
        if self.ideaunit_x._partys.get(self.partyunit_x.pid) != None:
            self.ideaunit_x.del_partylink(pid=self.partyunit_x.pid)
        self.refresh_ideas()

    def get_party_idea_count(self, party_id: str):  # PartyID):
        single_idea = ""
        ideas_count = 0
        idea_partylinks = []
        for idea in self.x_agenda._ideas.values():
            for partylink in idea._partys.values():
                if (
                    partylink.party_id == party_id
                    and idea.idea_id != partylink.party_id
                ):
                    ideas_count += 1
                    single_idea = idea.idea_id
                    idea_partylinks.append((idea, partylink))

        return ideas_count, single_idea, idea_partylinks

    def refresh_party_table(self):
        self.party_table.setObjectName("Partys")
        self.party_table.setColumnHidden(0, False)
        self.party_table.setColumnWidth(0, 170)
        self.party_table.setColumnWidth(1, 130)
        self.party_table.setColumnWidth(2, 40)
        self.party_table.setColumnWidth(3, 60)
        self.party_table.setColumnWidth(4, 40)
        self.party_table.setHorizontalHeaderLabels(
            ["Party", "Idea", "Idea Count", "Agenda_Importance", "Weight"]
        )
        self.party_table.setRowCount(0)

        partys_list = list(self.x_agenda._partys.values())
        partys_list.sort(key=lambda x: x.pid, reverse=False)

        for row, party in enumerate(partys_list, start=1):
            # ideas_count = 0
            # for idea in self.x_agenda._ideas.values():
            #     for partylink in idea._partys.values():
            #         if partylink.party_id == party.pid:
            #             ideas_count += 1

            ideas_count, single_idea, idea_partylinks = self.get_party_idea_count(
                party_id=party.pid
            )

            self.party_table.setRowCount(row)
            self.party_table.setItem(row - 1, 0, qtw.QTableWidgetItem(party.pid))
            qt_agenda_cred = qtw.QTableWidgetItem(
                agenda_importance_diplay(party._agenda_cred)
            )
            qt_agenda_debt = qtw.QTableWidgetItem(
                agenda_importance_diplay(party._agenda_debt)
            )
            self.party_table.setItem(row - 1, 1, qtw.QTableWidgetItem(single_idea))
            self.party_table.setItem(row - 1, 2, qtw.QTableWidgetItem("#"))
            self.party_table.setItem(row - 1, 3, qt_agenda_cred)
            # self.party_table.setItem(row - 1, 3, qt_agenda_debt)
            self.party_table.setItem(
                row - 1, 4, qtw.QTableWidgetItem(f"{party.credor_weight}")
            )
            # self.party_table.setItem(
            #     row - 1, 4, qtw.QTableWidgetItem(f"{party.debtor_weight}")
            # )

    def party_in_idea(self, partyunit, ideaunit):
        return any(
            partylink.party_id == partyunit.party_id
            for partylink in ideaunit._partys.values()
        )

    def refresh_ideas_in_table(self):
        self.ideas_in_table.setObjectName("Ideas Linked")
        self.ideas_in_table.setColumnHidden(0, False)
        self.ideas_in_table.setColumnWidth(0, 170)
        self.ideas_in_table.setColumnWidth(1, 130)
        self.ideas_in_table.setColumnWidth(2, 40)
        self.ideas_in_table.setColumnWidth(3, 60)
        self.ideas_in_table.setColumnWidth(4, 40)
        self.ideas_in_table.setRowCount(0)

        ideas_in_list = [
            ideaunit
            for ideaunit in self.x_agenda._ideas.values()
            if (
                self.partyunit_x != None
                and self.party_in_idea(partyunit=self.partyunit_x, ideaunit=ideaunit)
                and self.partyunit_x.pid != ideaunit.idea_id
            )
        ]
        ideas_in_list.sort(key=lambda x: x.idea_id, reverse=False)

        self.ideas_in_table.setHorizontalHeaderLabels(
            [f"Ideas ({len(ideas_in_list)})", "Idea", "Idea Count"]
        )

        for row, ideaunit_x in enumerate(ideas_in_list, start=1):
            self.ideas_in_table.setRowCount(row)
            self.ideas_in_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(ideaunit_x.idea_id)
            )

    def refresh_ideas_out_table(self):
        self.ideas_out_table.setObjectName("Ideas Linked")
        self.ideas_out_table.setColumnHidden(0, False)
        self.ideas_out_table.setColumnWidth(0, 170)
        self.ideas_out_table.setColumnWidth(1, 130)
        self.ideas_out_table.setColumnWidth(2, 40)
        self.ideas_out_table.setColumnWidth(3, 60)
        self.ideas_out_table.setColumnWidth(4, 40)
        self.ideas_out_table.setRowCount(0)

        ideas_out_list = [
            ideaunit
            for ideaunit in self.x_agenda._ideas.values()
            if (
                self.partyunit_x != None
                and ideaunit._partys.get(ideaunit.idea_id) is None
                and (
                    self.party_in_idea(partyunit=self.partyunit_x, ideaunit=ideaunit)
                    is False
                )
            )
            or self.partyunit_x is None
        ]
        ideas_out_list.sort(key=lambda x: x.idea_id, reverse=False)
        self.ideas_out_table.setHorizontalHeaderLabels(
            [f"Ideas ({len(ideas_out_list)})", "Idea", "Idea Count"]
        )

        for row, ideaunit_x in enumerate(ideas_out_list, start=1):
            self.ideas_out_table.setRowCount(row)
            self.ideas_out_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(ideaunit_x.idea_id)
            )

    def refresh_ideas_stan_table(self):
        self.ideas_stan_table.setObjectName("Ideas Linked")
        self.ideas_stan_table.setColumnHidden(0, False)
        self.ideas_stan_table.setColumnWidth(0, 170)
        self.ideas_stan_table.setColumnWidth(1, 130)
        self.ideas_stan_table.setColumnWidth(2, 40)
        self.ideas_stan_table.setColumnWidth(3, 60)
        self.ideas_stan_table.setColumnWidth(4, 40)
        self.ideas_stan_table.setRowCount(0)

        ideas_stand_list = [
            ideaunit
            for ideaunit in self.x_agenda._ideas.values()
            if self.partyunit_x != None
            and (
                ideaunit._partys.get(ideaunit.idea_id) != None
                and self.partyunit_x.pid == ideaunit.idea_id
            )
        ]
        ideas_stand_list.sort(key=lambda x: x.idea_id, reverse=False)
        self.ideas_stan_table.setHorizontalHeaderLabels(
            [f"Ideas ({len(ideas_stand_list)})", "Idea", "Idea Count"]
        )

        for row, ideaunit_x in enumerate(ideas_stand_list, start=1):
            self.ideas_stan_table.setRowCount(row)
            self.ideas_stan_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(ideaunit_x.idea_id)
            )

    def refresh_all(self):
        self.refresh_party_table()
        self.party_id.setText("")
        self.refresh_ideas()
        if self.idea_pid != None:
            self.idea_pid.setText("")

    def refresh_ideas(self):
        self.refresh_ideas_in_table()
        self.refresh_ideas_out_table()
        self.refresh_ideas_stan_table()

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
            allow_nonsingle_idea_overwrite=True,
        )
        self.party_id.setText("")
        self.refresh_all()

    def idea_insert(self):
        bu = ideaunit_shop(idea_id=self.idea_pid.text())
        self.x_agenda.set_ideaunit(y_ideaunit=bu)
        self.refresh_ideas()

    def idea_delete(self):
        self.x_agenda.del_ideaunit(idea_id=self.idea_pid.text())
        self.idea_pid.setText("")
        self.refresh_ideas()

    def idea_update(self):
        if self.idea_pid != None:
            self.x_agenda.edit_ideaunit_idea_id(
                old_idea_id=self.ideas_in_table.item(
                    self.ideas_in_table.currentRow(), 0
                ).text(),
                new_idea_id=self.idea_pid.text(),
                allow_idea_overwite=True,
            )
            self.idea_pid.setText("")
        self.refresh_ideas()
