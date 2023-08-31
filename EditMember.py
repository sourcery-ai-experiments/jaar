# command to for converting ui form to python file: pyuic5 ui\EditMemberUI.ui -o ui\EditMemberUI.py
import sys
from ui.EditMemberUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from EditMember2bd import EditMember2bd
from src.pyqt5_kit.pyqt_func import lw_diplay
from src.calendar.calendar import CalendarUnit
from src.calendar.group import groupunit_shop
from src.calendar.member import memberlink_shop


class EditMember(qtw.QTableWidget, Ui_Form):
    member_selected = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.member_table.itemClicked.connect(self.member_select)
        self.member_insert_button.clicked.connect(self.member_insert)
        self.member_update_button.clicked.connect(self.member_update)
        self.member_delete_button.clicked.connect(self.member_delete)
        self.groups_in_table.itemClicked.connect(self.groups_in_select)
        self.groups_out_table.itemClicked.connect(self.groups_out_select)
        self.group_insert_button.clicked.connect(self.group_insert)
        self.group_update_button.clicked.connect(self.group_update)
        self.group_delete_button.clicked.connect(self.group_delete)
        self.member_group_set_button.clicked.connect(self.member_group_set)
        self.member_group_del_button.clicked.connect(self.member_group_del)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)
        self.selected_member_name = None
        self.memberunit_x = None
        self.groupunit_x = None

    def member_select(self):
        member_name = self.member_table.item(self.member_table.currentRow(), 0).text()
        self.memberunit_x = self.calendar_x._members.get(member_name)
        self.member_name.setText(self.memberunit_x.name)
        self.refresh_groups()

    def groups_in_select(self):
        group_name = self.groups_in_table.item(
            self.groups_in_table.currentRow(), 0
        ).text()
        self.groupunit_x = self.calendar_x._groups.get(group_name)
        self.group_name.setText(self.groupunit_x.name)

    def groups_out_select(self):
        group_name = self.groups_out_table.item(
            self.groups_out_table.currentRow(), 0
        ).text()
        self.groupunit_x = self.calendar_x._groups.get(group_name)
        self.group_name.setText(self.groupunit_x.name)

    def member_group_set(self):
        self.groupunit_x.set_memberlink(
            memberlink=memberlink_shop(name=self.memberunit_x.name)
        )
        self.refresh_groups()

    def member_group_del(self):
        if self.groupunit_x._members.get(self.memberunit_x.name) != None:
            self.groupunit_x.del_memberlink(name=self.memberunit_x.name)
        self.refresh_groups()

    def get_member_group_count(self, member_name: str):  # MemberName):
        single_group = ""
        groups_count = 0
        group_memberlinks = []
        for group in self.calendar_x._groups.values():
            for memberlink in group._members.values():
                if memberlink.name == member_name and group.name != memberlink.name:
                    groups_count += 1
                    single_group = group.name
                    group_memberlinks.append((group, memberlink))

        return groups_count, single_group, group_memberlinks

    def refresh_member_table(self):
        self.member_table.setObjectName("Members")
        self.member_table.setColumnHidden(0, False)
        self.member_table.setColumnWidth(0, 170)
        self.member_table.setColumnWidth(1, 130)
        self.member_table.setColumnWidth(2, 40)
        self.member_table.setColumnWidth(3, 60)
        self.member_table.setColumnWidth(4, 40)
        self.member_table.setHorizontalHeaderLabels(
            ["Member", "Group", "Group Count", "CALENDAR_Importance", "Weight"]
        )
        self.member_table.setRowCount(0)

        members_list = list(self.calendar_x._members.values())
        members_list.sort(key=lambda x: x.name, reverse=False)

        for row, member in enumerate(members_list, start=1):
            # groups_count = 0
            # for group in self.calendar_x._groups.values():
            #     for memberlink in group._members.values():
            #         if memberlink.name == member.name:
            #             groups_count += 1

            groups_count, single_group, group_memberlinks = self.get_member_group_count(
                member_name=member.name
            )

            self.member_table.setRowCount(row)
            self.member_table.setItem(row - 1, 0, qtw.QTableWidgetItem(member.name))
            qt_calendar_credit = qtw.QTableWidgetItem(
                lw_diplay(member._calendar_credit)
            )
            qt_calendar_debt = qtw.QTableWidgetItem(lw_diplay(member._calendar_debt))
            self.member_table.setItem(row - 1, 1, qtw.QTableWidgetItem(single_group))
            self.member_table.setItem(row - 1, 2, qtw.QTableWidgetItem("#"))
            self.member_table.setItem(row - 1, 3, qt_calendar_credit)
            # self.member_table.setItem(row - 1, 3, qt_calendar_debt)
            self.member_table.setItem(
                row - 1, 4, qtw.QTableWidgetItem(f"{member.creditor_weight}")
            )
            # self.member_table.setItem(
            #     row - 1, 4, qtw.QTableWidgetItem(f"{member.debtor_weight}")
            # )

    def member_in_group(self, memberunit, groupunit):
        return any(
            memberlink.name == memberunit.name
            for memberlink in groupunit._members.values()
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
            for groupunit in self.calendar_x._groups.values()
            if (
                self.memberunit_x != None
                and self.member_in_group(
                    memberunit=self.memberunit_x, groupunit=groupunit
                )
                and self.memberunit_x.name != groupunit.name
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
            for groupunit in self.calendar_x._groups.values()
            if (
                self.memberunit_x != None
                and groupunit._members.get(groupunit.name) is None
                and (
                    self.member_in_group(
                        memberunit=self.memberunit_x, groupunit=groupunit
                    )
                    == False
                )
            )
            or self.memberunit_x is None
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
            for groupunit in self.calendar_x._groups.values()
            if self.memberunit_x != None
            and (
                groupunit._members.get(groupunit.name) != None
                and self.memberunit_x.name == groupunit.name
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
        self.refresh_member_table()
        self.member_name.setText("")
        self.refresh_groups()
        if self.group_name != None:
            self.group_name.setText("")

    def refresh_groups(self):
        self.refresh_groups_in_table()
        self.refresh_groups_out_table()
        self.refresh_groups_stan_table()

    def member_insert(self):
        self.calendar_x.add_memberunit(name=self.member_name.text())
        self.refresh_all()

    def member_delete(self):
        self.calendar_x.del_memberunit(name=self.member_name.text())
        self.member_name.setText("")
        self.memberunit_x = None
        self.refresh_all()

    def member_update(self):
        self.calendar_x.edit_memberunit_name(
            old_name=self.member_table.item(self.member_table.currentRow(), 0).text(),
            new_name=self.member_name.text(),
            allow_member_overwite=True,
            allow_nonsingle_group_overwrite=True,
        )
        self.member_name.setText("")
        self.refresh_all()

    def group_insert(self):
        bu = groupunit_shop(name=self.group_name.text())
        self.calendar_x.set_groupunit(groupunit=bu)
        self.refresh_groups()

    def group_delete(self):
        self.calendar_x.del_groupunit(groupname=self.group_name.text())
        self.group_name.setText("")
        self.refresh_groups()

    def group_update(self):
        if self.group_name != None:
            self.calendar_x.edit_groupunit_name(
                old_name=self.groups_in_table.item(
                    self.groups_in_table.currentRow(), 0
                ).text(),
                new_name=self.group_name.text(),
                allow_group_overwite=True,
            )
            self.group_name.setText("")
        self.refresh_groups()
