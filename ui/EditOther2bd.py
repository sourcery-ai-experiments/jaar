# command to for converting ui form to python file: pyuic5 ui\EditOther2bdUI.ui -o ui\EditOther2bdUI.py
from ui.EditOther2bdUI import Ui_Form
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


class EditOther2bd(qtw.QWidget, Ui_Form):
    """The settings dialog window"""

    refresh_ideaunit_submitted = qtc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.other_id = None
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)

        self.gp_other_yes.clicked.connect(self.gp_other_yes_clicked)
        self.gp_other_no.clicked.connect(self.gp_other_no_clicked)

        self.gp_other2belief_delete_button.clicked.connect(self.other2belief_delete)
        self.gp_add_button.clicked.connect(self.other2belief_add)
        self.update_weight_button.clicked.connect(self.other2belief_update)

        self.gp_insert_button.clicked.connect(self.gp_insert)
        self.gp_delete_button.clicked.connect(self.gp_delete)
        self.gp_update_button.clicked.connect(self.gp_update)

        # self.EditOther2bd.x_agenda = self.x_agenda
        # self.EditOther2bd.selected_other_id = self.selected_other_id

    def gp_insert(self):
        gp_pid = self.gp_new_edit.text()
        # .gp_insert(gp_pid=gp_pid)
        # self.gp_new_edit.setText("")
        # self.refreshAll()

    def gp_delete(self):
        currentRowInt = self.gp_other_no.currentRow()
        # if self.gp_other_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     gp_id = int(self.gp_other_no.item(currentRowInt, 2).text())
        #     .gp_delete(gp_id=gp_id)
        # self.refreshAll()

    def gp_update(self):
        currentRowInt = self.gp_other_no.currentRow()
        # if self.gp_other_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     gp_pid = self.gp_update_pid_edit.text()
        #     gp_id = int(self.gp_other_no.item(currentRowInt, 2).text())
        #     .gp_update(gp_id=gp_id, gp_pid=gp_pid)
        # self.refreshAll()

    def other2belief_update(self):
        currentRowInt = self.gp_other_yes.currentRow()
        # if self.gp_other_yes.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     other_id = self.other_id
        #     gp_id = int(self.gp_other_yes.item(currentRowInt, 4).text())
        #     weight = int(self.other2belief_weight_edit.text())
        #     Other2OG.other2belief_update(other_id=other_id, gp_id=gp_id, weight=weight)
        #     self.refreshAll()

    def other2belief_delete(self):
        currentRowInt = self.gp_other_yes.currentRow()
        # if self.gp_other_yes.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     other_id = self.other_id
        #     gp_id = int(self.gp_other_yes.item(currentRowInt, 4).text())
        #     Other2OG.other2belief_delete(other_id=other_id, gp_id=gp_id)
        #     self.refreshAll()

    def other2belief_add(self):
        currentRowInt = self.gp_other_no.currentRow()
        # if self.gp_other_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     other_id = self.other_id
        #     gp_id = int(self.gp_other_no.item(currentRowInt, 2).text())
        #     Other2OG.other2belief_insert(other_id=other_id, gp_id=gp_id, weight=1)
        # self.refreshAll()

    def refreshAll(self):
        self.refreshOtherYes()
        self.refreshOtherNo()

    def refreshOtherYes(self):
        self.gp_other_yes.setColumnWidth(0, 110)
        self.gp_other_yes.setColumnWidth(1, 50)
        self.gp_other_yes.setColumnWidth(2, 110)
        self.gp_other_yes.setColumnWidth(3, 110)
        self.gp_other_yes.setColumnWidth(4, 30)
        self.gp_other_yes.setColumnHidden(4, True)

    def refreshOtherNo(self):
        other_id = self.other_id
        self.gp_other_no.setColumnWidth(0, 110)
        self.gp_other_no.setColumnWidth(1, 110)
        self.gp_other_no.setColumnWidth(2, 30)
        self.gp_other_no.setColumnHidden(2, True)

    def gp_other_yes_clicked(self):
        self.other2belief_weight_edit.setText(
            self.gp_other_yes.item(self.gp_other_yes.currentRow(), 1).text()
        )

    def gp_other_no_clicked(self):
        pid = self.gp_other_no.item(self.gp_other_no.currentRow(), 0).text()
        self.gp_update_pid_edit.setText(pid)
        self.gp_delete_button.setText(f'Delete Other Belief " {pid} "')
