# command to for converting ui form to python file: pyuic5 ui\EditPartyUI.ui -o ui\EditPartyUI.py
import sys
from ui.EditPartyUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from EditParty2bd import EditParty2bd
from pyqt_func import agenda_importance_diplay
from src.agenda.agenda import agendaunit_shop
from src.agenda.group import groupunit_shop
from src.agenda.party import partylink_shop


class EditParty(qtw.QTableWidget, Ui_Form):
    party_selected = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.party_table.itemClicked.connect(self.party_select)
        self.party_insert_button.clicked.connect(self.party_insert)
        self.party_update_button.clicked.connect(self.party_update)
        self.party_delete_button.clicked.connect(self.party_delete)
        self.groups_in_table.itemClicked.connect(self.groups_in_select)
        self.groups_out_table.itemClicked.connect(self.groups_out_select)
        self.group_insert_button.clicked.connect(self.group_insert)
        self.group_update_button.clicked.connect(self.group_update)
        self.group_delete_button.clicked.connect(self.group_delete)
        self.party_group_set_button.clicked.connect(self.party_group_set)
        self.party_group_del_button.clicked.connect(self.party_group_del)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)
        self.selected_party_title = None
        self.partyunit_x = None
        self.groupunit_x = None

    def party_select(self):
        party_title = self.party_table.item(self.party_table.currentRow(), 0).text()
        self.partyunit_x = self.agenda_x._partys.get(party_title)
        self.party_title.setText(self.partyunit_x.title)
        self.refresh_groups()

    def groups_in_select(self):
        group_title = self.groups_in_table.item(
            self.groups_in_table.currentRow(), 0
        ).text()
        self.groupunit_x = self.agenda_x._groups.get(group_title)
        self.group_title.setText(self.groupunit_x.brand)

    def groups_out_select(self):
        group_title = self.groups_out_table.item(
            self.groups_out_table.currentRow(), 0
        ).text()
        self.groupunit_x = self.agenda_x._groups.get(group_title)
        self.group_title.setText(self.groupunit_x.brand)

    def party_group_set(self):
        self.groupunit_x.set_partylink(
            partylink=partylink_shop(title=self.partyunit_x.title)
        )
        self.refresh_groups()

    def party_group_del(self):
        if self.groupunit_x._partys.get(self.partyunit_x.title) != None:
            self.groupunit_x.del_partylink(title=self.partyunit_x.title)
        self.refresh_groups()

    def get_party_group_count(self, party_title: str):  # PartyTitle):
        single_group = ""
        groups_count = 0
        group_partylinks = []
        for group in self.agenda_x._groups.values():
            for partylink in group._partys.values():
                if partylink.title == party_title and group.brand != partylink.title:
                    groups_count += 1
                    single_group = group.brand
                    group_partylinks.append((group, partylink))

        return groups_count, single_group, group_partylinks

    def refresh_party_table(self):
        self.party_table.setObjectName("Partys")
        self.party_table.setColumnHidden(0, False)
        self.party_table.setColumnWidth(0, 170)
        self.party_table.setColumnWidth(1, 130)
        self.party_table.setColumnWidth(2, 40)
        self.party_table.setColumnWidth(3, 60)
        self.party_table.setColumnWidth(4, 40)
        self.party_table.setHorizontalHeaderLabels(
            ["Party", "Group", "Group Count", "DEAL_Importance", "Weight"]
        )
        self.party_table.setRowCount(0)

        partys_list = list(self.agenda_x._partys.values())
        partys_list.sort(key=lambda x: x.title, reverse=False)

        for row, party in enumerate(partys_list, start=1):
            # groups_count = 0
            # for group in self.agenda_x._groups.values():
            #     for partylink in group._partys.values():
            #         if partylink.title == party.title:
            #             groups_count += 1

            groups_count, single_group, group_partylinks = self.get_party_group_count(
                party_title=party.title
            )

            self.party_table.setRowCount(row)
            self.party_table.setItem(row - 1, 0, qtw.QTableWidgetItem(party.title))
            qt_agenda_credit = qtw.QTableWidgetItem(
                agenda_importance_diplay(party._agenda_credit)
            )
            qt_agenda_debt = qtw.QTableWidgetItem(
                agenda_importance_diplay(party._agenda_debt)
            )
            self.party_table.setItem(row - 1, 1, qtw.QTableWidgetItem(single_group))
            self.party_table.setItem(row - 1, 2, qtw.QTableWidgetItem("#"))
            self.party_table.setItem(row - 1, 3, qt_agenda_credit)
            # self.party_table.setItem(row - 1, 3, qt_agenda_debt)
            self.party_table.setItem(
                row - 1, 4, qtw.QTableWidgetItem(f"{party.creditor_weight}")
            )
            # self.party_table.setItem(
            #     row - 1, 4, qtw.QTableWidgetItem(f"{party.debtor_weight}")
            # )

    def party_in_group(self, partyunit, groupunit):
        return any(
            partylink.title == partyunit.title
            for partylink in groupunit._partys.values()
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
            for groupunit in self.agenda_x._groups.values()
            if (
                self.partyunit_x != None
                and self.party_in_group(partyunit=self.partyunit_x, groupunit=groupunit)
                and self.partyunit_x.title != groupunit.brand
            )
        ]
        groups_in_list.sort(key=lambda x: x.title, reverse=False)

        self.groups_in_table.setHorizontalHeaderLabels(
            [f"Groups ({len(groups_in_list)})", "Group", "Group Count"]
        )

        for row, groupunit_x in enumerate(groups_in_list, start=1):
            self.groups_in_table.setRowCount(row)
            self.groups_in_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(groupunit_x.brand)
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
            for groupunit in self.agenda_x._groups.values()
            if (
                self.partyunit_x != None
                and groupunit._partys.get(groupunit.brand) is None
                and (
                    self.party_in_group(partyunit=self.partyunit_x, groupunit=groupunit)
                    == False
                )
            )
            or self.partyunit_x is None
        ]
        groups_out_list.sort(key=lambda x: x.title, reverse=False)
        self.groups_out_table.setHorizontalHeaderLabels(
            [f"Groups ({len(groups_out_list)})", "Group", "Group Count"]
        )

        for row, groupunit_x in enumerate(groups_out_list, start=1):
            self.groups_out_table.setRowCount(row)
            self.groups_out_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(groupunit_x.brand)
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
            for groupunit in self.agenda_x._groups.values()
            if self.partyunit_x != None
            and (
                groupunit._partys.get(groupunit.brand) != None
                and self.partyunit_x.title == groupunit.brand
            )
        ]
        groups_stand_list.sort(key=lambda x: x.title, reverse=False)
        self.groups_stan_table.setHorizontalHeaderLabels(
            [f"Groups ({len(groups_stand_list)})", "Group", "Group Count"]
        )

        for row, groupunit_x in enumerate(groups_stand_list, start=1):
            self.groups_stan_table.setRowCount(row)
            self.groups_stan_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(groupunit_x.brand)
            )

    def refresh_all(self):
        self.refresh_party_table()
        self.party_title.setText("")
        self.refresh_groups()
        if self.group_title != None:
            self.group_title.setText("")

    def refresh_groups(self):
        self.refresh_groups_in_table()
        self.refresh_groups_out_table()
        self.refresh_groups_stan_table()

    def party_insert(self):
        self.agenda_x.add_partyunit(title=self.party_title.text())
        self.refresh_all()

    def party_delete(self):
        self.agenda_x.del_partyunit(title=self.party_title.text())
        self.party_title.setText("")
        self.partyunit_x = None
        self.refresh_all()

    def party_update(self):
        self.agenda_x.edit_partyunit_title(
            old_title=self.party_table.item(self.party_table.currentRow(), 0).text(),
            new_title=self.party_title.text(),
            allow_party_overwite=True,
            allow_nonsingle_group_overwrite=True,
        )
        self.party_title.setText("")
        self.refresh_all()

    def group_insert(self):
        bu = groupunit_shop(brand=self.group_title.text())
        self.agenda_x.set_groupunit(groupunit=bu)
        self.refresh_groups()

    def group_delete(self):
        self.agenda_x.del_groupunit(groupbrand=self.group_title.text())
        self.group_title.setText("")
        self.refresh_groups()

    def group_update(self):
        if self.group_title != None:
            self.agenda_x.edit_groupunit_brand(
                old_title=self.groups_in_table.item(
                    self.groups_in_table.currentRow(), 0
                ).text(),
                new_title=self.group_title.text(),
                allow_group_overwite=True,
            )
            self.group_title.setText("")
        self.refresh_groups()
