# command to for converting ui form to python file: pyuic5 ui\EditMember2bdUI.ui -o ui\EditMember2bdUI.py
from ui.EditMember2bdUI import Ui_Form
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


class EditMember2bd(qtw.QWidget, Ui_Form):
    """The settings dialog window"""

    refresh_ideaunit_submitted = qtc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.member_id = None
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)

        self.gp_member_yes.clicked.connect(self.gp_member_yes_clicked)
        self.gp_member_no.clicked.connect(self.gp_member_no_clicked)

        self.gp_remove_button.clicked.connect(self.member2group_remove)
        self.gp_add_button.clicked.connect(self.member2group_add)
        self.update_weight_button.clicked.connect(self.member2group_update)

        self.gp_insert_button.clicked.connect(self.gp_insert)
        self.gp_delete_button.clicked.connect(self.gp_delete)
        self.gp_update_button.clicked.connect(self.gp_update)

        # self.EditMember2bd.agent_x = self.agent_x
        # self.EditMember2bd.selected_member_name = self.selected_member_name

    def gp_insert(self):
        gp_name = self.gp_new_edit.text()
        # .gp_insert(gp_name=gp_name)
        # self.gp_new_edit.setText("")
        # self.refreshAll()

    def gp_delete(self):
        currentRowInt = self.gp_member_no.currentRow()
        # if self.gp_member_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     gp_id = int(self.gp_member_no.item(currentRowInt, 2).text())
        #     .gp_delete(gp_id=gp_id)
        # self.refreshAll()

    def gp_update(self):
        currentRowInt = self.gp_member_no.currentRow()
        # if self.gp_member_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     gp_name = self.gp_update_name_edit.text()
        #     gp_id = int(self.gp_member_no.item(currentRowInt, 2).text())
        #     .gp_update(gp_id=gp_id, gp_name=gp_name)
        # self.refreshAll()

    def member2group_update(self):
        currentRowInt = self.gp_member_yes.currentRow()
        # if self.gp_member_yes.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     member_id = self.member_id
        #     gp_id = int(self.gp_member_yes.item(currentRowInt, 4).text())
        #     weight = int(self.member2group_weight_edit.text())
        #     Member2OG.member2group_update(member_id=member_id, gp_id=gp_id, weight=weight)
        #     self.refreshAll()

    def member2group_remove(self):
        currentRowInt = self.gp_member_yes.currentRow()
        # if self.gp_member_yes.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     member_id = self.member_id
        #     gp_id = int(self.gp_member_yes.item(currentRowInt, 4).text())
        #     Member2OG.member2group_delete(member_id=member_id, gp_id=gp_id)
        #     self.refreshAll()

    def member2group_add(self):
        currentRowInt = self.gp_member_no.currentRow()
        # if self.gp_member_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     member_id = self.member_id
        #     gp_id = int(self.gp_member_no.item(currentRowInt, 2).text())
        #     Member2OG.member2group_insert(member_id=member_id, gp_id=gp_id, weight=1)
        # self.refreshAll()

    def refreshAll(self):
        self.refreshMemberYes()
        self.refreshMemberNo()

    def refreshMemberYes(self):
        self.gp_member_yes.setColumnWidth(0, 110)
        self.gp_member_yes.setColumnWidth(1, 50)
        self.gp_member_yes.setColumnWidth(2, 110)
        self.gp_member_yes.setColumnWidth(3, 110)
        self.gp_member_yes.setColumnWidth(4, 30)
        self.gp_member_yes.setColumnHidden(4, True)

    def refreshMemberNo(self):
        member_id = self.member_id
        self.gp_member_no.setColumnWidth(0, 110)
        self.gp_member_no.setColumnWidth(1, 110)
        self.gp_member_no.setColumnWidth(2, 30)
        self.gp_member_no.setColumnHidden(2, True)

    def gp_member_yes_clicked(self):
        self.member2group_weight_edit.setText(
            self.gp_member_yes.item(self.gp_member_yes.currentRow(), 1).text()
        )

    def gp_member_no_clicked(self):
        name = self.gp_member_no.item(self.gp_member_no.currentRow(), 0).text()
        self.gp_update_name_edit.setText(name)
        self.gp_delete_button.setText(f'Delete Member Group " {name} "')
