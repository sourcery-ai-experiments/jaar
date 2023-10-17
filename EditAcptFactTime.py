# command to for converting ui form to python file: pyuic5 ui\EditAcptFactTimeUI.ui -o ui\EditAcptFactTimeUI.py
from ui.EditAcptFactTimeUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from datetime import datetime


class EditAcptFactTime(qtw.QTableWidget, Ui_Form):
    root_changes_submitted = qtc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.curr_year.addItems(self.listYear())
        self.curr_month.addItems(self.listMonth())
        self.curr_monthday.addItems(self.listMonthDay())
        self.curr_hour.addItems(self.listHour())
        self.curr_min.addItems(self.listMin())

        self.prev_year.addItems(self.listYear())
        self.prev_month.addItems(self.listMonth())
        self.prev_monthday.addItems(self.listMonthDay())
        self.prev_hour.addItems(self.listHour())
        self.prev_min.addItems(self.listMin())

        self.american_update.clicked.connect(self.update_acptfact)
        self.refresh_root_values.clicked.connect(self.display_acptfact_time)

        self.show

    def update_acptfact(self):
        # change time acptfact so that the open is the date entered
        open_month = self.prev_month.currentText()
        open_monthday = self.prev_monthday.currentText()
        open_year = self.prev_year.currentText()
        open_hour = self.prev_hour.currentText()
        open_minute = self.prev_min.currentText()

        open_dt_x = datetime(
            year=int(open_year),
            month=int(open_month),
            day=int(open_monthday),
            hour=int(open_hour),
            minute=int(open_minute),
        )

        nigh_month = self.curr_month.currentText()
        nigh_monthday = self.curr_monthday.currentText()
        nigh_year = self.curr_year.currentText()
        nigh_hour = self.curr_hour.currentText()
        nigh_minute = self.curr_min.currentText()

        nigh_dt_x = datetime(
            year=int(nigh_year),
            month=int(nigh_month),
            day=int(nigh_monthday),
            hour=int(nigh_hour),
            minute=int(nigh_minute),
        )

        self.deal_x.set_time_acptfacts(open=open_dt_x, nigh=nigh_dt_x)
        self.root_changes_submitted.emit(True)
        self.close()

    def display_acptfact_time(self):
        # minutes_idea = self.deal_x.get_idea_kid(
        #     road=f"{root_label},time,jajatime"
        # )
        minutes_acptfact = self.deal_x._idearoot._acptfactunits[
            f"{self.deal_x._fix_handle},time,jajatime"
        ]

        dt_open = self.deal_x.get_time_dt_from_min(min=minutes_acptfact.open)
        dt_nigh = self.deal_x.get_time_dt_from_min(min=minutes_acptfact.nigh)

        self.curr_hour.setCurrentIndex(self.curr_hour.findText(str(dt_nigh.hour)))
        self.curr_min.setCurrentIndex(self.curr_min.findText(str(dt_nigh.minute)))
        self.curr_month.setCurrentIndex(self.curr_month.findText(str(dt_nigh.month)))
        self.curr_monthday.setCurrentIndex(
            self.curr_monthday.findText(str(dt_nigh.day))
        )
        self.curr_year.setCurrentIndex(self.curr_year.findText(str(dt_nigh.year)))

        self.prev_hour.setCurrentIndex(self.prev_hour.findText(str(dt_open.hour)))
        self.prev_min.setCurrentIndex(self.prev_min.findText(str(dt_open.minute)))
        self.prev_month.setCurrentIndex(self.prev_month.findText(str(dt_open.month)))
        self.prev_monthday.setCurrentIndex(
            self.prev_monthday.findText(str(dt_open.day))
        )
        self.prev_year.setCurrentIndex(self.prev_year.findText(str(dt_open.year)))

    def listYear(self):
        return ["2023", "2022", "2021", "2000", "2001", "2005"]

    def listMonth(self):
        return [str(int) for int in range(1, 13)]

    def listMonthDay(self):
        return [str(int) for int in range(1, 32)]

    def listHour(self):
        return [str(int) for int in range(24)]

    def listMin(self):
        return [str(int) for int in range(60)]

    # return dictionary with all prev and curr
    def findCurrentRootValues(self):
        root_dt_open = datetime()
        root_dt_nigh = datetime()

        return {
            "curr_hour": root_dt_open.hour,
            "curr_min": root_dt_open.minute,
            "curr_month": root_dt_open.month,
            "curr_monthday": root_dt_open.day,
            "curr_year": root_dt_open.year,
            "prev_hour": root_dt_nigh.hour,
            "prev_min": root_dt_nigh.minute,
            "prev_month": root_dt_nigh.month,
            "prev_monthday": root_dt_nigh.day,
            "prev_year": root_dt_nigh.year,
        }

    def closeRootChanges(self):
        self.root_changes_submitted.emit(True)
        self.close()
