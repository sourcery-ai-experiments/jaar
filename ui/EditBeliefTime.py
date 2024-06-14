# command to for converting ui form to python file: pyuic5 ui\EditBeliefTimeUI.ui -o ui\EditBeliefTimeUI.py
from ui.EditBeliefTimeUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from datetime import datetime


class EditBeliefTime(qtw.QTableWidget, Ui_Form):
    root_modify_submitted = qtc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.now_year.addItems(self.listYear())
        self.now_month.addItems(self.listMonth())
        self.now_monthday.addItems(self.listMonthDay())
        self.now_hour.addItems(self.listHour())
        self.now_min.addItems(self.listMin())

        self.prev_year.addItems(self.listYear())
        self.prev_month.addItems(self.listMonth())
        self.prev_monthday.addItems(self.listMonthDay())
        self.prev_hour.addItems(self.listHour())
        self.prev_min.addItems(self.listMin())

        self.american_update.clicked.connect(self.update_belief)
        self.refresh_root_values.clicked.connect(self.display_belief_time)

        self.show

    def update_belief(self):
        # modify time belief so that the open is the date entered
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

        nigh_month = self.now_month.currentText()
        nigh_monthday = self.now_monthday.currentText()
        nigh_year = self.now_year.currentText()
        nigh_hour = self.now_hour.currentText()
        nigh_minute = self.now_min.currentText()

        nigh_dt_x = datetime(
            year=int(nigh_year),
            month=int(nigh_month),
            day=int(nigh_monthday),
            hour=int(nigh_hour),
            minute=int(nigh_minute),
        )

        self.agenda_x.set_time_beliefs(open=open_dt_x, nigh=nigh_dt_x)
        self.root_modify_submitted.emit(True)
        self.close()

    def display_belief_time(self):
        # minutes_fact = self.agenda_x.get_fact_obj(
        #     road=f"{root_label},time,jajatime"
        # )
        minutes_belief = self.agenda_x._factroot._beliefunits[
            f"{self.agenda_x._econ_id},time,jajatime"
        ]

        dt_open = self.agenda_x.get_time_dt_from_min(min=minutes_belief.open)
        dt_nigh = self.agenda_x.get_time_dt_from_min(min=minutes_belief.nigh)

        self.now_hour.setCurrentIndex(self.now_hour.findText(str(dt_nigh.hour)))
        self.now_min.setCurrentIndex(self.now_min.findText(str(dt_nigh.minute)))
        self.now_month.setCurrentIndex(self.now_month.findText(str(dt_nigh.month)))
        self.now_monthday.setCurrentIndex(self.now_monthday.findText(str(dt_nigh.day)))
        self.now_year.setCurrentIndex(self.now_year.findText(str(dt_nigh.year)))

        self.prev_hour.setCurrentIndex(self.prev_hour.findText(str(dt_open.hour)))
        self.prev_min.setCurrentIndex(self.prev_min.findText(str(dt_open.minute)))
        self.prev_month.setCurrentIndex(self.prev_month.findText(str(dt_open.month)))
        self.prev_monthday.setCurrentIndex(
            self.prev_monthday.findText(str(dt_open.day))
        )
        self.prev_year.setCurrentIndex(self.prev_year.findText(str(dt_open.year)))

    def listYear(self):
        return ["2024", "2023", "2022", "2021", "2000", "2001", "2005"]

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
            "now_hour": root_dt_open.hour,
            "now_min": root_dt_open.minute,
            "now_month": root_dt_open.month,
            "now_monthday": root_dt_open.day,
            "now_year": root_dt_open.year,
            "prev_hour": root_dt_nigh.hour,
            "prev_min": root_dt_nigh.minute,
            "prev_month": root_dt_nigh.month,
            "prev_monthday": root_dt_nigh.day,
            "prev_year": root_dt_nigh.year,
        }
