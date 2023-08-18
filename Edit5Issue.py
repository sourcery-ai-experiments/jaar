# command to for converting ui form to python file: pyuic5 ui\World5IssueUI.ui -o ui\World5IssueUI.py
import sys
from ui.World5IssueUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from src.pyqt5_tools.pyqt_func import lw_diplay
from src.agent.agent import AgentUnit
from src.agent.brand import brandunit_shop
from src.agent.ally import allylink_shop


class Edit5Issue(qtw.QTableWidget, Ui_Form):
    ally_selected = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        # self.brand_update_button.clicked.connect(self.brand_update)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)
        self.selected_ally_name = None
        self.allyunit_x = None
        self.brandunit_x = None

    def refresh_all(self):
        pass
