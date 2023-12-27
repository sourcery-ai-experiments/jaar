# command to for converting ui form to python file: pyuic5 ui\EditParty2bdUI.ui -o ui\EditParty2bdUI.py
from ui.EditParty2bdUI import Ui_Form
import sys
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc


class EditParty2bd(qtw.QWidget, Ui_Form):
    """The settings dialog window"""

    refresh_ideaunit_submitted = qtc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)
        self.party_id = None
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)

        self.gp_party_yes.clicked.connect(self.gp_party_yes_clicked)
        self.gp_party_no.clicked.connect(self.gp_party_no_clicked)

        self.gp_remove_button.clicked.connect(self.party2group_remove)
        self.gp_add_button.clicked.connect(self.party2group_add)
        self.update_weight_button.clicked.connect(self.party2group_update)

        self.gp_insert_button.clicked.connect(self.gp_insert)
        self.gp_delete_button.clicked.connect(self.gp_delete)
        self.gp_update_button.clicked.connect(self.gp_update)

        # self.EditParty2bd.agenda_x = self.agenda_x
        # self.EditParty2bd.selected_party_pid = self.selected_party_pid

    def gp_insert(self):
        gp_pid = self.gp_new_edit.text()
        # .gp_insert(gp_pid=gp_pid)
        # self.gp_new_edit.setText("")
        # self.refreshAll()

    def gp_delete(self):
        currentRowInt = self.gp_party_no.currentRow()
        # if self.gp_party_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     gp_id = int(self.gp_party_no.item(currentRowInt, 2).text())
        #     .gp_delete(gp_id=gp_id)
        # self.refreshAll()

    def gp_update(self):
        currentRowInt = self.gp_party_no.currentRow()
        # if self.gp_party_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     gp_pid = self.gp_update_pid_edit.text()
        #     gp_id = int(self.gp_party_no.item(currentRowInt, 2).text())
        #     .gp_update(gp_id=gp_id, gp_pid=gp_pid)
        # self.refreshAll()

    def party2group_update(self):
        currentRowInt = self.gp_party_yes.currentRow()
        # if self.gp_party_yes.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     party_id = self.party_id
        #     gp_id = int(self.gp_party_yes.item(currentRowInt, 4).text())
        #     weight = int(self.party2group_weight_edit.text())
        #     Party2OG.party2group_update(party_id=party_id, gp_id=gp_id, weight=weight)
        #     self.refreshAll()

    def party2group_remove(self):
        currentRowInt = self.gp_party_yes.currentRow()
        # if self.gp_party_yes.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     party_id = self.party_id
        #     gp_id = int(self.gp_party_yes.item(currentRowInt, 4).text())
        #     Party2OG.party2group_delete(party_id=party_id, gp_id=gp_id)
        #     self.refreshAll()

    def party2group_add(self):
        currentRowInt = self.gp_party_no.currentRow()
        # if self.gp_party_no.rowCount() > 0:
        #     currentRowInt = max(currentRowInt, 0)
        #     party_id = self.party_id
        #     gp_id = int(self.gp_party_no.item(currentRowInt, 2).text())
        #     Party2OG.party2group_insert(party_id=party_id, gp_id=gp_id, weight=1)
        # self.refreshAll()

    def refreshAll(self):
        self.refreshPartyYes()
        self.refreshPartyNo()

    def refreshPartyYes(self):
        self.gp_party_yes.setColumnWidth(0, 110)
        self.gp_party_yes.setColumnWidth(1, 50)
        self.gp_party_yes.setColumnWidth(2, 110)
        self.gp_party_yes.setColumnWidth(3, 110)
        self.gp_party_yes.setColumnWidth(4, 30)
        self.gp_party_yes.setColumnHidden(4, True)

    def refreshPartyNo(self):
        party_id = self.party_id
        self.gp_party_no.setColumnWidth(0, 110)
        self.gp_party_no.setColumnWidth(1, 110)
        self.gp_party_no.setColumnWidth(2, 30)
        self.gp_party_no.setColumnHidden(2, True)

    def gp_party_yes_clicked(self):
        self.party2group_weight_edit.setText(
            self.gp_party_yes.item(self.gp_party_yes.currentRow(), 1).text()
        )

    def gp_party_no_clicked(self):
        pid = self.gp_party_no.item(self.gp_party_no.currentRow(), 0).text()
        self.gp_update_pid_edit.setText(pid)
        self.gp_delete_button.setText(f'Delete Party Group " {pid} "')
