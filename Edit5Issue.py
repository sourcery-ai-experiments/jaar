# command to for converting ui form to python file: pyuic5 ui\Cure5IssueUI.ui -o ui\Cure5IssueUI.py
import sys
from ui.Cure5IssueUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from pyqt_func import deal_importance_diplay
from src.deal.deal import DealUnit
from src.deal.group import groupunit_shop
from src.deal.party import partylink_shop


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
