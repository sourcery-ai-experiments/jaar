# command to for converting ui form to python file: pyuic5 ui\EditGuy2bdUI.ui -o ui\EditGuy2bdUI.py
from ui.EditGuy2bdUI import Ui_Form
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


class EditGuy2bd(qtw.QWidget, Ui_Form):
    """The settings dialog window"""

    refresh_ideaunit_submitted = qtc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.guy_id = None
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)

        self.gp_guy_yes.clicked.connect(self.gp_guy_yes_clicked)
        self.gp_guy_no.clicked.connect(self.gp_guy_no_clicked)

        self.gp_guy2belief_delete_button.clicked.connect(self.guy2belief_delete)
        self.gp_add_button.clicked.connect(self.guy2belief_add)
        self.update_weight_button.clicked.connect(self.guy2belief_update)

        self.gp_insert_button.clicked.connect(self.gp_insert)
        self.gp_delete_button.clicked.connect(self.gp_delete)
        self.gp_update_button.clicked.connect(self.gp_update)

        # self.EditGuy2bd.x_agenda = self.x_agenda
        # self.EditGuy2bd.selected_guy_id = self.selected_guy_id

    def gp_insert(self):
        gp_pid = self.gp_new_edit.text()
        # .gp_insert(gp_pid=gp_pid)
        # self.gp_new_edit.setText("")
        # self.refreshAll()

    def gp_delete(self):
        currentRowInt = self.gp_guy_no.currentRow()
        # if self.gp_guy_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     gp_id = int(self.gp_guy_no.item(currentRowInt, 2).text())
        #     .gp_delete(gp_id=gp_id)
        # self.refreshAll()

    def gp_update(self):
        currentRowInt = self.gp_guy_no.currentRow()
        # if self.gp_guy_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     gp_pid = self.gp_update_pid_edit.text()
        #     gp_id = int(self.gp_guy_no.item(currentRowInt, 2).text())
        #     .gp_update(gp_id=gp_id, gp_pid=gp_pid)
        # self.refreshAll()

    def guy2belief_update(self):
        currentRowInt = self.gp_guy_yes.currentRow()
        # if self.gp_guy_yes.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     guy_id = self.guy_id
        #     gp_id = int(self.gp_guy_yes.item(currentRowInt, 4).text())
        #     weight = int(self.guy2belief_weight_edit.text())
        #     Guy2OG.guy2belief_update(guy_id=guy_id, gp_id=gp_id, weight=weight)
        #     self.refreshAll()

    def guy2belief_delete(self):
        currentRowInt = self.gp_guy_yes.currentRow()
        # if self.gp_guy_yes.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     guy_id = self.guy_id
        #     gp_id = int(self.gp_guy_yes.item(currentRowInt, 4).text())
        #     Guy2OG.guy2belief_delete(guy_id=guy_id, gp_id=gp_id)
        #     self.refreshAll()

    def guy2belief_add(self):
        currentRowInt = self.gp_guy_no.currentRow()
        # if self.gp_guy_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     guy_id = self.guy_id
        #     gp_id = int(self.gp_guy_no.item(currentRowInt, 2).text())
        #     Guy2OG.guy2belief_insert(guy_id=guy_id, gp_id=gp_id, weight=1)
        # self.refreshAll()

    def refreshAll(self):
        self.refreshGuyYes()
        self.refreshGuyNo()

    def refreshGuyYes(self):
        self.gp_guy_yes.setColumnWidth(0, 110)
        self.gp_guy_yes.setColumnWidth(1, 50)
        self.gp_guy_yes.setColumnWidth(2, 110)
        self.gp_guy_yes.setColumnWidth(3, 110)
        self.gp_guy_yes.setColumnWidth(4, 30)
        self.gp_guy_yes.setColumnHidden(4, True)

    def refreshGuyNo(self):
        guy_id = self.guy_id
        self.gp_guy_no.setColumnWidth(0, 110)
        self.gp_guy_no.setColumnWidth(1, 110)
        self.gp_guy_no.setColumnWidth(2, 30)
        self.gp_guy_no.setColumnHidden(2, True)

    def gp_guy_yes_clicked(self):
        self.guy2belief_weight_edit.setText(
            self.gp_guy_yes.item(self.gp_guy_yes.currentRow(), 1).text()
        )

    def gp_guy_no_clicked(self):
        pid = self.gp_guy_no.item(self.gp_guy_no.currentRow(), 0).text()
        self.gp_update_pid_edit.setText(pid)
        self.gp_delete_button.setText(f'Delete Guy Belief " {pid} "')
