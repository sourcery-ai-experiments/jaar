# # command to for converting ui form to python file: pyuic5 ui\MainWindow.ui -o ui\MainWindow.py
import contextlib
from datetime import datetime, timedelta
from ui.MainWindow import Ui_MainWindow
from EditMain import EditMainView
from EditAcptFactTime import EditAcptFactTime
from EditAgenda import EditAgenda
from EditProblem import EditProblem
from src.calendar.calendar import CalendarUnit, get_from_json
from src.calendar.examples.calendar_env import calendar_env
from src.calendar.hreg_time import convert1440toHHMM
from src.calendar.road import get_global_root_label as root_label
from src.pyqt5_kit.pyqt_func import (
    lw_diplay as pyqt_func_lw_diplay,
    str2float as pyqt_func_str2float,
    num2str as pyqt_func_num2str,
)
from src.calendar.x_func import (
    save_file as x_func_save_file,
    open_file as x_func_open_file,
)
from sys import exit as sys_exit

# """Simple test application for dealing with multiple windows"""
import sys

# from PyQt5 import QtWidgets as qtw
from PyQt5.QtWidgets import (
    QTableWidgetItem as qtw1,
    QApplication,
    QFileDialog,
    QMainWindow,
)
from PyQt5 import QtCore as qtc


class MainAppException(Exception):
    pass


class MainApp(QApplication):
    """The main application object"""

    def __init__(self, argv):
        super().__init__(argv)

        file_open_path = argv[1] if len(argv) >= 2 else None
        self.main_window = MainWindow(file_open_path)
        self.main_window.show()

        # create editmain instance
        self.editmain_view = EditMainView()
        # create slot for making editmain visible
        self.main_window.open_editmain.connect(self.editmain_show)

        self.editagenda_view = EditAgenda()
        # create slot for making editmain visible
        self.main_window.open_editagenda.connect(self.editagenda_show)

        self.edittime_view = EditAcptFactTime()
        # create slot for making editmain visible
        self.main_window.open_edittime.connect(self.editacptfact_show)
        self.edittime_view.root_changes_submitted.connect(self.main_window.refresh_all)

        self.editproblem_view = EditProblem()
        self.main_window.open_editproblem.connect(self.editproblem_show)
        self.edittime_view.root_changes_submitted.connect(self.main_window.refresh_all)

    def editmain_show(self):
        self.editmain_view.calendar_x = self.main_window.calendar_x
        self.editmain_view.refresh_all()
        self.editmain_view.show()

    def editproblem_show(self):
        self.editproblem_view.calendar_x = self.main_window.calendar_x
        self.editproblem_view.refresh_all()
        self.editproblem_view.show()

    def editagenda_show(self):
        self.editagenda_view.calendar_x = self.main_window.calendar_x
        self.editagenda_view.refresh_all()
        self.editagenda_view.show()

    def editacptfact_show(self):
        self.edittime_view.calendar_x = self.main_window.calendar_x
        self.edittime_view.display_acptfact_time()
        self.edittime_view.show()


class MainWindow(QMainWindow, Ui_MainWindow):
    """The main application window"""

    open_editmain = qtc.pyqtSignal(bool)
    open_editproblem = qtc.pyqtSignal(bool)
    open_editagenda = qtc.pyqtSignal(bool)
    open_edittime = qtc.pyqtSignal(bool)
    calendar_x_signal = qtc.pyqtSignal(CalendarUnit)

    def __init__(self, file_open_path):
        super().__init__()

        self.setupUi(self)
        # signals for opening windows
        self.save_close_button.clicked.connect(self.save_file_and_quit)
        self.editmain_button.clicked.connect(self.open_editmain)
        self.problem_popup_button.clicked.connect(self.open_editproblem)
        self.editagenda_button.clicked.connect(self.open_editagenda)
        self.acptfact_nigh_now.clicked.connect(self.set_acptfact_time_nigh_now)
        self.acptfact_open_5daysago.clicked.connect(
            self.set_acptfact_time_open_5daysago
        )
        self.acptfact_open_lower_spec1.clicked.connect(
            self.set_acptfact_time_open_midnight
        )
        self.acptfact_open_soft_spec1.clicked.connect(self.set_acptfact_time_open_soft)
        self.root_datetime_view.clicked.connect(self.open_edittime)
        self.agenda_task_complete.clicked.connect(self.set_agenda_item_complete)
        self.cb_update_now_repeat.clicked.connect(self.startTimer)
        self.timer = qtc.QTimer()
        self.timer.timeout.connect(self.showTime)

        self.fm_open.triggered.connect(self.get_file_path)
        self.fm_save.triggered.connect(self.save_file)
        self.save_as.triggered.connect(self.save_as_file)
        self.fm_new.triggered.connect(self.calendar_new)

        # self.acptfacts_table.itemClicked.connect(self.acptfact_base_combo_set)
        self.acptfacts_table.setObjectName("Calendar AcptFacts")
        self.acptfacts_table.setColumnWidth(0, 300)
        self.acptfacts_table.setColumnWidth(1, 300)
        self.acptfacts_table.setColumnWidth(2, 30)
        self.acptfacts_table.setColumnWidth(3, 30)
        self.acptfacts_table.setColumnWidth(4, 30)
        self.acptfacts_table.setColumnWidth(5, 30)
        self.acptfacts_table.setColumnHidden(0, False)
        self.acptfacts_table.setColumnHidden(1, False)
        self.acptfacts_table.setColumnHidden(2, True)
        self.acptfacts_table.setColumnHidden(3, True)
        self.acptfacts_table.setColumnHidden(4, True)
        self.acptfacts_table.setColumnHidden(5, True)
        self.acptfacts_table.horizontalHeaderVisible = True
        self.acptfacts_table.setHorizontalHeaderLabels(
            ["AcptFactBase", "AcptFactSelect", "Base", "AcptFact", "Open", "Nigh"]
        )
        self.acptfacts_table.setRowCount(0)
        self.agenda_states.itemClicked.connect(self.agenda_task_display)
        # self.acptfact_update_combo.activated.connect(self.acptfact_update_heir)

        self.calendar_x_json = None
        # if "delete me this is for dev only":
        self.file_path = None
        if file_open_path is None:
            self.file_path = f"{calendar_env()}/example_calendar2.json"
        else:
            self.file_path = file_open_path
        self.open_file()

        self.refresh_all()
        self.emit_calendar()

    def save_file_and_quit(self):
        self.save_file()
        sys_exit()

    def showTime(self):
        time = qtc.QDateTime.currentDateTime()
        t_x = time.toString("yyyy-MM-dd hh:mm dddd")
        self.label_time_display.setText(t_x)
        self.set_acptfact_time_nigh_now()

    def startTimer(self):
        self.timer.stop()
        if self.cb_update_now_repeat.checkState() == 2:
            curr_time_frame = str(self.update_now_time_frame.currentText())
            curr_time_second = 60
            curr_time_millisecond = curr_time_second * 1000
            self.timer.start(curr_time_millisecond)
        else:
            self.timer.stop()

    def set_agenda_item_complete(self):
        if self.current_task_road is None:
            self.label_last_label.setText("")
        else:
            base_x = "Mycalendar,time,jajatime"
            self.calendar_x.set_agenda_task_complete(
                task_road=self.current_task_road, base=base_x
            )
        self.label_last_label.setText(self.current_task_road)
        self.refresh_all()

    def set_acptfact_time_open_5daysago(self):
        days5ago_x = datetime.now() - timedelta(days=5)
        road_minute = f"{root_label()},time,jajatime"
        # self.root_datetime_curr_l.setText(f"Now: {str(now_x)}")
        self.calendar_x.set_acptfact(
            base=road_minute,
            pick=road_minute,
            open=self.calendar_x.get_time_min_from_dt(dt=days5ago_x),
        )
        self.refresh_all()

    def _set_acptfact_time_open_midnight_attr(self):
        road_minute = f"{root_label()},time,jajatime"
        open_dt = self.calendar_x.get_time_dt_from_min(
            self.calendar_x._idearoot._acptfactunits[road_minute].open
        )
        nigh_dt = self.calendar_x.get_time_dt_from_min(
            self.calendar_x._idearoot._acptfactunits[road_minute].nigh
        )
        open_midnight = datetime(
            year=open_dt.year,
            month=open_dt.month,
            day=open_dt.day,
            hour=0,
            minute=0,
        ) + timedelta(days=1)
        open_minutes = None
        if open_dt < nigh_dt and open_midnight < nigh_dt:
            open_minutes = self.calendar_x.get_time_min_from_dt(open_midnight)
        else:
            open_minutes = self.calendar_x.get_time_min_from_dt(dt=nigh_dt)
        self.calendar_x.set_acptfact(
            base=road_minute,
            pick=road_minute,
            open=open_minutes,
        )

    def set_acptfact_time_open_midnight(self):
        try:
            self._set_acptfact_time_open_midnight_attr()
        except Exception:
            print("calendar does not have jajatime framework")
        self.refresh_all()

    def set_acptfact_time_open_soft(self):
        # now_x = datetime.now()
        # road_minute = f"{root_label()},time,jajatime"
        # self.root_datetime_curr_l.setText(f"Now: {str(now_x)}")
        # self.calendar_x.set_acptfact(
        #     base=road_minute,
        #     pick=road_minute,
        #     open=self.calendar_x.get_time_min_from_dt(dt=now_x),
        # )
        self.refresh_all()

    def set_acptfact_time_nigh_now(self):
        now_x = datetime.now()
        road_minute = f"{root_label()},time,jajatime"
        self.calendar_x.set_acptfact(
            base=road_minute,
            pick=road_minute,
            nigh=self.calendar_x.get_time_min_from_dt(dt=now_x),
        )
        self.refresh_all()

    def emit_calendar(self):
        self.calendar_x_signal.emit(self.calendar_x)

    def get_file_path(self):
        x_file_path, _ = QFileDialog.getOpenFileName()
        if x_file_path:
            self.file_path = x_file_path
            self.open_file()

    def save_as_file(self):
        x_file_path, _ = QFileDialog.getSaveFileName()
        if x_file_path:
            self.file_path = x_file_path
            self._commit_file_save()

    def save_file(self):
        if self.file_path is None:
            self.file_path = f"{calendar_env()}/{self._get_file_name()}"
        self._commit_file_save()

    def _get_file_name(self):
        return f"calendar_{self.calendar_x._owner}.json"

    def _commit_file_save(self):
        calendar_x_json = self.calendar_x.get_json()
        with open(f"{self.file_path}", "w") as f:
            f.write(calendar_x_json)
        self.current_file_path_l.setText(self.file_path)
        # x_func_save_file(
        #     dest_dir=calendar_person_dir,
        #     file_name=f"{root_label()}.json",
        #     file_text=calendar_x.get_json(),
        # )

    def load_file(self):
        x_json = ""
        x_json = x_func_open_file(dest_dir=self.file_path, file_name=None)
        self.current_file_path_l.setText(self.file_path)
        return x_json

    def open_file(self):
        self.calendar_x_json = self.load_file()
        self.calendar_load(cx_json=self.calendar_x_json)

    def calendar_new(self):
        self.calendar_x = CalendarUnit(_owner="new")
        self.calendar_x._set_acptfacts_empty_if_null()
        self.calendar_x.set_members_empty_if_null()
        self.calendar_x.set_groupunits_empty_if_null()
        self.calendar_x.set_time_hreg_ideas(c400_count=7)
        road_minute = f"{root_label()},time,jajatime"
        self.calendar_x.set_acptfact(
            base=road_minute, pick=road_minute, open=1000000, nigh=1000000
        )
        self.refresh_all()

    def refresh_datetime_display(self):
        road_minute = f"{root_label()},time,jajatime"
        jajatime_open = self.calendar_x.get_time_dt_from_min(
            self.calendar_x._idearoot._acptfactunits[road_minute].open
        )
        jajatime_nigh = self.calendar_x.get_time_dt_from_min(
            self.calendar_x._idearoot._acptfactunits[road_minute].nigh
        )
        week_days = ("Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun")
        self.root_datetime_curr_l.setText(
            f"Now:  {str(jajatime_nigh)} {week_days[jajatime_nigh.weekday()]}"
        )
        self.root_datetime_prev_l.setText(
            f"Past: {str(jajatime_open)} {week_days[jajatime_open.weekday()]}"
        )

    def refresh_all(self):
        self.root_datetime_curr_l.setText("")
        self.root_datetime_prev_l.setText("")
        with contextlib.suppress(Exception):
            self.refresh_datetime_display()
        self.calendar_owner.setText(self.calendar_x._owner)
        self.acptfacts_table_load()
        self.agenda_states_load()

    def calendar_load(self, cx_json: str):
        self.calendar_x = get_from_json(cx_json=cx_json)
        self.promise_items = self.calendar_x.get_agenda_items()
        self.refresh_all()

    def get_acptfacts_list(self):
        return self.calendar_x._idearoot._acptfactunits.values()

    def acptfacts_table_load(self):
        self.acptfacts_table.setRowCount(0)

        row = 0
        for acptfact in self.get_acptfacts_list():
            base_text = acptfact.base.replace(f"{self.calendar_x._owner}", "")
            base_text = base_text[1:]
            acptfact_text = acptfact.pick.replace(acptfact.base, "")
            acptfact_text = acptfact_text[1:]
            if acptfact.open is None:
                acptfact_text = f"{acptfact_text}"
            elif base_text == "time,jajatime":
                acptfact_text = f"{self.calendar_x.get_jajatime_legible_one_time_event(acptfact.open)}-{self.calendar_x.get_jajatime_repeating_legible_text(acptfact.nigh)}"
            else:
                acptfact_text = (
                    f"{acptfact_text} Open-Nigh {acptfact.open}-{acptfact.nigh}"
                )

            self._acptfacts_table_set_row_and_2_columns(row, base_text, acptfact_text)
            self.acptfacts_table.setItem(row, 2, qtw1(acptfact.base))
            self.acptfacts_table.setItem(row, 3, qtw1(acptfact.pick))
            self.acptfacts_table.setItem(row, 4, qtw1(pyqt_func_num2str(acptfact.open)))
            self.acptfacts_table.setItem(row, 5, qtw1(pyqt_func_num2str(acptfact.nigh)))
            row += 1

        for base, count in self.calendar_x.get_missing_acptfact_bases().items():
            base_text = base.replace(f"{self.calendar_x._owner}", "")
            base_text = base_text[1:]

            base_lecture_text = f"{base_text} ({count} nodes)"
            self._acptfacts_table_set_row_and_2_columns(row, base_lecture_text, "")
            self.acptfacts_table.setItem(row, 2, qtw1(base))
            self.acptfacts_table.setItem(row, 3, qtw1(""))
            self.acptfacts_table.setItem(row, 4, qtw1(""))
            self.acptfacts_table.setItem(row, 5, qtw1(""))
            row += 1

    def _acptfacts_table_set_row_and_2_columns(self, row, base_text, acptfact_text):
        self.acptfacts_table.setRowCount(row + 1)
        self.acptfacts_table.setItem(row, 0, qtw1(base_text))
        self.acptfacts_table.setItem(row, 1, qtw1(acptfact_text))
        self.acptfacts_table.setColumnWidth(0, 140)
        self.acptfacts_table.setColumnWidth(1, 450)

    def acptfact_update_heir(self, base_road):
        if self.acptfact_update_combo.currentText() == "":
            raise MainAppException("No comboup selection for acptfact update.")
        if (
            self.acptfacts_table.item(self.acptfacts_table.currentRow(), 2).text()
            is None
        ):
            raise MainAppException("No table selection for acptfact update.")
        acptfact_update_combo_text = self.acptfact_update_combo.currentText()
        self.calendar_x._idearoot._acptfactunits[
            base_road
        ].acptfact = acptfact_update_combo_text
        self.base_road = None
        self.refresh_all

    def agenda_states_load(self):
        self.calendar_x.get_tree_metrics()
        agenda_list = self.calendar_x.get_agenda_items()
        agenda_list.sort(key=lambda x: x._calendar_importance, reverse=True)
        self.agenda_states.setSortingEnabled(True)
        self.agenda_states.setRowCount(0)
        self.set_agenda_states_table_properties()

        self.label_agenda_label_data.setText("")
        self.label_agenda_day_data.setText("")
        self.label_agenda_time_data.setText("")
        self.label_agenda_end_data.setText("")

        row = 0
        self.current_task_road = None
        for agenda_item in agenda_list:
            if agenda_item._task == False:
                self.populate_agenda_table_row(row=row, agenda_item=agenda_item)
                row += 1
            elif agenda_item._task == True and self.current_task_road is None:
                self.current_task_road = f"{agenda_item._walk},{agenda_item._label}"
                self.agenda_task_display(agenda_item)

    def populate_agenda_table_row(self, row, agenda_item):
        ax = agenda_item
        self.agenda_states.setRowCount(row + 1)
        self.agenda_states.setItem(row, 0, qtw1(str(ax._uid)))
        self.agenda_states.setItem(row, 1, qtw1(ax._label))

        if ax._requiredunits.get(f"{root_label()},time,jajatime") != None:
            jajatime_required = ax._requiredunits.get(f"{root_label()},time,jajatime")
            sufffact_x = jajatime_required.sufffacts.get(
                f"{root_label()},time,jajatime"
            )
            if sufffact_x != None and sufffact_x.open != 0:
                tw_open = qtw1(
                    self.calendar_x.get_jajatime_repeating_legible_text(
                        open=sufffact_x.open,
                        nigh=sufffact_x.nigh,
                        divisor=sufffact_x.divisor,
                    )
                )
                self.agenda_states.setItem(row, 2, tw_open)
                tw_nigh = qtw1(convert1440toHHMM(min1440=sufffact_x.nigh))
                self.agenda_states.setItem(row, 3, tw_nigh)

        self.agenda_states.setItem(
            row, 4, qtw1(pyqt_func_lw_diplay(ax._calendar_importance))
        )
        self.agenda_states.setItem(row, 5, qtw1(ax._walk))
        self.agenda_states.setItem(row, 6, qtw1(""))

    def set_agenda_states_table_properties(self):
        self.agenda_states.setObjectName("Agenda Being")
        self.agenda_states.setColumnWidth(0, 30)
        self.agenda_states.setColumnWidth(1, 200)
        self.agenda_states.setColumnWidth(2, 120)
        self.agenda_states.setColumnWidth(3, 50)
        self.agenda_states.setColumnWidth(4, 70)
        self.agenda_states.setColumnWidth(5, 500)
        self.agenda_states.setColumnWidth(6, 100)
        self.agenda_states.setColumnHidden(0, True)
        self.agenda_states.setColumnHidden(1, False)
        self.agenda_states.setColumnHidden(2, False)
        self.agenda_states.setColumnHidden(3, True)
        self.agenda_states.setColumnHidden(4, False)
        self.agenda_states.setColumnHidden(5, False)
        self.agenda_states.setColumnHidden(6, True)
        self.agenda_states.setHorizontalHeaderLabels(
            [
                "rank",
                "label",
                "jajatime",
                "jaja_nigh",
                "calendar_importance",
                "idea_road",
                "branch_percent",
            ]
        )

    def agenda_task_display(self, agenda_item):
        self.label_agenda_label_data.setText(agenda_item._label)
        if agenda_item._requiredunits.get(f"{root_label()},time,jajatime") != None:
            jajatime_required = agenda_item._requiredunits.get(
                f"{root_label()},time,jajatime"
            )
            sufffact_x = jajatime_required.sufffacts.get(
                f"{root_label()},time,jajatime,day"
            )
            if sufffact_x != None:
                self.label_agenda_day_data.setText("day_stuff")
                self.label_agenda_time_data.setText(
                    convert1440toHHMM(min1440=sufffact_x.open)
                )
                self.label_agenda_end_data.setText(
                    convert1440toHHMM(min1440=sufffact_x.nigh)
                )
        self.label_agenda_calendar_importance_data.setText(
            str(agenda_item._calendar_importance)
        )
        self.label_agenda_family_data.setText("")
        self.label_agenda_road_data.setText(agenda_item._walk)

    def get_jajaday_open_nigh(self, agenda_item):
        jajatime_required = agenda_item._requiredunits.get(
            f"{root_label()},time,jajatime"
        )
        sufffact_x = jajatime_required.sufffacts.get(
            f"{root_label()},time,jajatime,day"
        )
        if sufffact_x != None:
            open_x = sufffact_x.open
            nigh_x = sufffact_x.nigh
            x_open_minutes = (
                f"0{int(open_x) % 60}" if open_x % 60 < 10 else f"{int(open_x) % 60}"
            )
            open_y = f"{int(open_x/60)}:{x_open_minutes}"
            x_nigh_minutes = (
                f"0{int(nigh_x) % 60}" if nigh_x % 60 < 10 else f"{int(nigh_x) % 60}"
            )
            nigh_y = f"{int(nigh_x/60)}:{x_nigh_minutes}"

        return open_y, nigh_y


if __name__ == "__main__":
    app = MainApp(sys.argv)
    sys.exit(app.exec())
