# command to for converting ui form to python file: pyuic5 ui\EditAlly2bdUI.ui -o ui\EditAlly2bdUI.py
from ui.EditAlly2bdUI import Ui_Form

import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QApplication, QTreeWidget, QTreeWidgetItem
import EditIdeaUnit, EditAlly
from PyQt5.QtSql import QSqlQuery, QSqlQueryModel


class EditAlly2bd(qtw.QWidget, Ui_Form):
    """The settings dialog window"""

    refresh_ideaunit_submitted = qtc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.ally_id = None
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)

        self.bd_member_yes.clicked.connect(self.bd_member_yes_clicked)
        self.bd_member_no.clicked.connect(self.bd_member_no_clicked)

        self.bd_remove_button.clicked.connect(self.ally2tribe_remove)
        self.bd_add_button.clicked.connect(self.ally2tribe_add)
        self.update_weight_button.clicked.connect(self.ally2tribe_update)

        self.bd_insert_button.clicked.connect(self.bd_insert)
        self.bd_delete_button.clicked.connect(self.bd_delete)
        self.bd_update_button.clicked.connect(self.bd_update)

        # self.EditAlly2bd.agent_x = self.agent_x
        # self.EditAlly2bd.selected_ally_name = self.selected_ally_name

    def bd_insert(self):
        bd_name = self.bd_new_edit.text()
        # .bd_insert(bd_name=bd_name)
        # self.bd_new_edit.setText("")
        # self.refreshAll()

    def bd_delete(self):
        currentRowInt = self.bd_member_no.currentRow()
        # if self.bd_member_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     bd_id = int(self.bd_member_no.item(currentRowInt, 2).text())
        #     .bd_delete(bd_id=bd_id)
        # self.refreshAll()

    def bd_update(self):
        currentRowInt = self.bd_member_no.currentRow()
        # if self.bd_member_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     bd_name = self.bd_update_name_edit.text()
        #     bd_id = int(self.bd_member_no.item(currentRowInt, 2).text())
        #     .bd_update(bd_id=bd_id, bd_name=bd_name)
        # self.refreshAll()

    def ally2tribe_update(self):
        currentRowInt = self.bd_member_yes.currentRow()
        # if self.bd_member_yes.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     ally_id = self.ally_id
        #     bd_id = int(self.bd_member_yes.item(currentRowInt, 4).text())
        #     weight = int(self.ally2tribe_weight_edit.text())
        #     Ally2OG.ally2tribe_update(ally_id=ally_id, bd_id=bd_id, weight=weight)
        #     self.refreshAll()

    def ally2tribe_remove(self):
        currentRowInt = self.bd_member_yes.currentRow()
        # if self.bd_member_yes.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     ally_id = self.ally_id
        #     bd_id = int(self.bd_member_yes.item(currentRowInt, 4).text())
        #     Ally2OG.ally2tribe_delete(ally_id=ally_id, bd_id=bd_id)
        #     self.refreshAll()

    def ally2tribe_add(self):
        currentRowInt = self.bd_member_no.currentRow()
        # if self.bd_member_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     ally_id = self.ally_id
        #     bd_id = int(self.bd_member_no.item(currentRowInt, 2).text())
        #     Ally2OG.ally2tribe_insert(ally_id=ally_id, bd_id=bd_id, weight=1)
        # self.refreshAll()

    def refreshAll(self):
        self.refreshMemberYes()
        self.refreshMemberNo()

    def refreshMemberYes(self):
        self.bd_member_yes.setColumnWidth(0, 110)
        self.bd_member_yes.setColumnWidth(1, 50)
        self.bd_member_yes.setColumnWidth(2, 110)
        self.bd_member_yes.setColumnWidth(3, 110)
        self.bd_member_yes.setColumnWidth(4, 30)
        self.bd_member_yes.setColumnHidden(4, True)

    def refreshMemberNo(self):
        ally_id = self.ally_id
        self.bd_member_no.setColumnWidth(0, 110)
        self.bd_member_no.setColumnWidth(1, 110)
        self.bd_member_no.setColumnWidth(2, 30)
        self.bd_member_no.setColumnHidden(2, True)

    def bd_member_yes_clicked(self):
        self.ally2tribe_weight_edit.setText(
            self.bd_member_yes.item(self.bd_member_yes.currentRow(), 1).text()
        )

    def bd_member_no_clicked(self):
        name = self.bd_member_no.item(self.bd_member_no.currentRow(), 0).text()
        self.bd_update_name_edit.setText(name)
        self.bd_delete_button.setText(f'Delete Ally Tribe " {name} "')
