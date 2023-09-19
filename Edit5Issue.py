# command to for converting ui form to python file: pyuic5 ui\System5IssueUI.ui -o ui\System5IssueUI.py
import sys
from ui.System5IssueUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from src.pyqt5_kit.pyqt_func import calendar_importance_diplay
from src.calendar.calendar import CalendarUnit
from src.calendar.group import groupunit_shop
from src.calendar.member import memberlink_shop


class Edit5Issue(qtw.QTableWidget, Ui_Form):
    member_selected = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        # self.group_update_button.clicked.connect(self.group_update)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)
        self.selected_member_name = None
        self.memberunit_x = None
        self.groupunit_x = None

    def refresh_all(self):
        pass
