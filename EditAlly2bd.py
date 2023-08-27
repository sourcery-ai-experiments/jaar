# command to for converting ui form to python file: pyuic5 ui\EditAlly2bdUI.ui -o ui\EditAlly2bdUI.py
from ui.EditAlly2bdUI import Ui_Form
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


class EditAlly2bd(qtw.QWidget, Ui_Form):
    """The settings dialog window"""

    refresh_ideaunit_submitted = qtc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.ally_id = None
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)

        self.gp_member_yes.clicked.connect(self.gp_member_yes_clicked)
        self.gp_member_no.clicked.connect(self.gp_member_no_clicked)

        self.gp_remove_button.clicked.connect(self.ally2group_remove)
        self.gp_add_button.clicked.connect(self.ally2group_add)
        self.update_weight_button.clicked.connect(self.ally2group_update)

        self.gp_insert_button.clicked.connect(self.gp_insert)
        self.gp_delete_button.clicked.connect(self.gp_delete)
        self.gp_update_button.clicked.connect(self.gp_update)

        # self.EditAlly2bd.agent_x = self.agent_x
        # self.EditAlly2bd.selected_ally_name = self.selected_ally_name

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

    def ally2group_update(self):
        currentRowInt = self.gp_member_yes.currentRow()
        # if self.gp_member_yes.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     ally_id = self.ally_id
        #     gp_id = int(self.gp_member_yes.item(currentRowInt, 4).text())
        #     weight = int(self.ally2group_weight_edit.text())
        #     Ally2OG.ally2group_update(ally_id=ally_id, gp_id=gp_id, weight=weight)
        #     self.refreshAll()

    def ally2group_remove(self):
        currentRowInt = self.gp_member_yes.currentRow()
        # if self.gp_member_yes.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     ally_id = self.ally_id
        #     gp_id = int(self.gp_member_yes.item(currentRowInt, 4).text())
        #     Ally2OG.ally2group_delete(ally_id=ally_id, gp_id=gp_id)
        #     self.refreshAll()

    def ally2group_add(self):
        currentRowInt = self.gp_member_no.currentRow()
        # if self.gp_member_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     ally_id = self.ally_id
        #     gp_id = int(self.gp_member_no.item(currentRowInt, 2).text())
        #     Ally2OG.ally2group_insert(ally_id=ally_id, gp_id=gp_id, weight=1)
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
        ally_id = self.ally_id
        self.gp_member_no.setColumnWidth(0, 110)
        self.gp_member_no.setColumnWidth(1, 110)
        self.gp_member_no.setColumnWidth(2, 30)
        self.gp_member_no.setColumnHidden(2, True)

    def gp_member_yes_clicked(self):
        self.ally2group_weight_edit.setText(
            self.gp_member_yes.item(self.gp_member_yes.currentRow(), 1).text()
        )

    def gp_member_no_clicked(self):
        name = self.gp_member_no.item(self.gp_member_no.currentRow(), 0).text()
        self.gp_update_name_edit.setText(name)
        self.gp_delete_button.setText(f'Delete Ally Group " {name} "')
