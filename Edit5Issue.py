# command to for converting ui form to python file: pyuic5 ui\Heal5IssueUI.ui -o ui\Heal5IssueUI.py
import sys
from ui.Heal5IssueUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from src.pyqt5_kit.pyqt_func import contract_importance_diplay
from src.contract.contract import ContractUnit
from src.contract.group import groupunit_shop
from src.contract.party import partylink_shop


class Edit5Issue(qtw.QTableWidget, Ui_Form):
    party_selected = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        # self.group_update_button.clicked.connect(self.group_update)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)
        self.selected_party_title = None
        self.partyunit_x = None
        self.groupunit_x = None

    def refresh_all(self):
        pass
