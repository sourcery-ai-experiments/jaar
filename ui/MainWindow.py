# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1693, 914)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.editmain_button = QtWidgets.QPushButton(self.centralwidget)
        self.editmain_button.setGeometry(QtCore.QRect(390, 270, 201, 30))
        self.editmain_button.setObjectName("editmain_button")
        self.acptfact_open_lower_spec1 = QtWidgets.QPushButton(self.centralwidget)
        self.acptfact_open_lower_spec1.setGeometry(QtCore.QRect(200, 190, 181, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.acptfact_open_lower_spec1.setFont(font)
        self.acptfact_open_lower_spec1.setObjectName("acptfact_open_lower_spec1")
        self.acptfact_nigh_now = QtWidgets.QPushButton(self.centralwidget)
        self.acptfact_nigh_now.setGeometry(QtCore.QRect(30, 170, 281, 21))
        self.acptfact_nigh_now.setObjectName("acptfact_nigh_now")
        self.agenda_task_complete = QtWidgets.QPushButton(self.centralwidget)
        self.agenda_task_complete.setGeometry(QtCore.QRect(30, 270, 221, 30))
        self.agenda_task_complete.setObjectName("agenda_task_complete")
        self.root_datetime_prev_label = QtWidgets.QLabel(self.centralwidget)
        self.root_datetime_prev_label.setGeometry(QtCore.QRect(30, 50, 971, 51))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.root_datetime_prev_label.setFont(font)
        self.root_datetime_prev_label.setObjectName("root_datetime_prev_label")
        self.root_datetime_curr_label = QtWidgets.QLabel(self.centralwidget)
        self.root_datetime_curr_label.setGeometry(QtCore.QRect(30, 120, 981, 51))
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(36)
        font.setBold(True)
        font.setWeight(75)
        self.root_datetime_curr_label.setFont(font)
        self.root_datetime_curr_label.setObjectName("root_datetime_curr_label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(30, 100, 141, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(30, 30, 181, 16))
        self.label_3.setObjectName("label_3")
        self.label_agenda_desc_header = QtWidgets.QLabel(self.centralwidget)
        self.label_agenda_desc_header.setGeometry(QtCore.QRect(30, 340, 141, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_agenda_desc_header.setFont(font)
        self.label_agenda_desc_header.setObjectName("label_agenda_desc_header")
        self.root_datetime_view = QtWidgets.QPushButton(self.centralwidget)
        self.root_datetime_view.setGeometry(QtCore.QRect(590, 170, 151, 41))
        self.root_datetime_view.setObjectName("root_datetime_view")
        self.lobby_button = QtWidgets.QPushButton(self.centralwidget)
        self.lobby_button.setGeometry(QtCore.QRect(380, 810, 201, 24))
        self.lobby_button.setObjectName("lobby_button")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(130, 840, 331, 16))
        self.label_7.setObjectName("label_7")
        self.cb_update_now_repeat = QtWidgets.QCheckBox(self.centralwidget)
        self.cb_update_now_repeat.setGeometry(QtCore.QRect(30, 220, 371, 41))
        font = QtGui.QFont()
        font.setPointSize(18)
        self.cb_update_now_repeat.setFont(font)
        self.cb_update_now_repeat.setObjectName("cb_update_now_repeat")
        self.label_time_display = QtWidgets.QLabel(self.centralwidget)
        self.label_time_display.setGeometry(QtCore.QRect(30, 210, 261, 16))
        self.label_time_display.setObjectName("label_time_display")
        self.editagenda_button = QtWidgets.QPushButton(self.centralwidget)
        self.editagenda_button.setGeometry(QtCore.QRect(250, 270, 141, 30))
        self.editagenda_button.setObjectName("editagenda_button")
        self.acptfacts_table = QtWidgets.QTableWidget(self.centralwidget)
        self.acptfacts_table.setGeometry(QtCore.QRect(1270, 390, 391, 461))
        self.acptfacts_table.setObjectName("acptfacts_table")
        self.acptfacts_table.setColumnCount(6)
        self.acptfacts_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.acptfacts_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.acptfacts_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.acptfacts_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.acptfacts_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.acptfacts_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.acptfacts_table.setHorizontalHeaderItem(5, item)
        self.calendar_label = QtWidgets.QLabel(self.centralwidget)
        self.calendar_label.setGeometry(QtCore.QRect(30, 10, 91, 16))
        self.calendar_label.setObjectName("calendar_label")
        self.lw_desc_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.lw_desc_update_button.setGeometry(QtCore.QRect(310, 10, 101, 21))
        self.lw_desc_update_button.setObjectName("lw_desc_update_button")
        self.calendar_owner = QtWidgets.QLineEdit(self.centralwidget)
        self.calendar_owner.setGeometry(QtCore.QRect(100, 10, 201, 22))
        self.calendar_owner.setObjectName("calendar_owner")
        self.label_agenda_day_header = QtWidgets.QLabel(self.centralwidget)
        self.label_agenda_day_header.setGeometry(QtCore.QRect(30, 500, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_agenda_day_header.setFont(font)
        self.label_agenda_day_header.setObjectName("label_agenda_day_header")
        self.label_agenda_time_header = QtWidgets.QLabel(self.centralwidget)
        self.label_agenda_time_header.setGeometry(QtCore.QRect(30, 560, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_agenda_time_header.setFont(font)
        self.label_agenda_time_header.setObjectName("label_agenda_time_header")
        self.label_agenda_end_header = QtWidgets.QLabel(self.centralwidget)
        self.label_agenda_end_header.setGeometry(QtCore.QRect(30, 610, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label_agenda_end_header.setFont(font)
        self.label_agenda_end_header.setObjectName("label_agenda_end_header")
        self.label_agenda_calendar_importance_header1 = QtWidgets.QLabel(
            self.centralwidget
        )
        self.label_agenda_calendar_importance_header1.setGeometry(
            QtCore.QRect(30, 640, 91, 31)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_agenda_calendar_importance_header1.setFont(font)
        self.label_agenda_calendar_importance_header1.setObjectName(
            "label_agenda_calendar_importance_header1"
        )
        self.label_agenda_family_header1 = QtWidgets.QLabel(self.centralwidget)
        self.label_agenda_family_header1.setGeometry(QtCore.QRect(30, 700, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_agenda_family_header1.setFont(font)
        self.label_agenda_family_header1.setObjectName("label_agenda_family_header1")
        self.label_agenda_road_header = QtWidgets.QLabel(self.centralwidget)
        self.label_agenda_road_header.setGeometry(QtCore.QRect(30, 320, 71, 41))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_agenda_road_header.setFont(font)
        self.label_agenda_road_header.setObjectName("label_agenda_road_header")
        self.label_agenda_desc_data = QtWidgets.QLabel(self.centralwidget)
        self.label_agenda_desc_data.setGeometry(QtCore.QRect(150, 340, 861, 71))
        font = QtGui.QFont()
        font.setPointSize(36)
        self.label_agenda_desc_data.setFont(font)
        self.label_agenda_desc_data.setText("")
        self.label_agenda_desc_data.setWordWrap(True)
        self.label_agenda_desc_data.setObjectName("label_agenda_desc_data")
        self.label_agenda_family_header2 = QtWidgets.QLabel(self.centralwidget)
        self.label_agenda_family_header2.setGeometry(QtCore.QRect(30, 720, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.label_agenda_family_header2.setFont(font)
        self.label_agenda_family_header2.setObjectName("label_agenda_family_header2")
        self.label_agenda_calendar_importance_header2 = QtWidgets.QLabel(
            self.centralwidget
        )
        self.label_agenda_calendar_importance_header2.setGeometry(
            QtCore.QRect(30, 660, 101, 31)
        )
        font = QtGui.QFont()
        font.setPointSize(11)
        self.label_agenda_calendar_importance_header2.setFont(font)
        self.label_agenda_calendar_importance_header2.setObjectName(
            "label_agenda_calendar_importance_header2"
        )
        self.label_agenda_road_data = QtWidgets.QLabel(self.centralwidget)
        self.label_agenda_road_data.setGeometry(QtCore.QRect(80, 330, 561, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_agenda_road_data.setFont(font)
        self.label_agenda_road_data.setObjectName("label_agenda_road_data")
        self.label_agenda_family_data = QtWidgets.QLabel(self.centralwidget)
        self.label_agenda_family_data.setGeometry(QtCore.QRect(130, 710, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_agenda_family_data.setFont(font)
        self.label_agenda_family_data.setObjectName("label_agenda_family_data")
        self.label_agenda_calendar_importance_data = QtWidgets.QLabel(
            self.centralwidget
        )
        self.label_agenda_calendar_importance_data.setGeometry(
            QtCore.QRect(130, 650, 221, 41)
        )
        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)
        font.setWeight(75)
        self.label_agenda_calendar_importance_data.setFont(font)
        self.label_agenda_calendar_importance_data.setObjectName(
            "label_agenda_calendar_importance_data"
        )
        self.label_agenda_end_data = QtWidgets.QLabel(self.centralwidget)
        self.label_agenda_end_data.setGeometry(QtCore.QRect(130, 610, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_agenda_end_data.setFont(font)
        self.label_agenda_end_data.setObjectName("label_agenda_end_data")
        self.label_agenda_time_data = QtWidgets.QLabel(self.centralwidget)
        self.label_agenda_time_data.setGeometry(QtCore.QRect(130, 560, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_agenda_time_data.setFont(font)
        self.label_agenda_time_data.setObjectName("label_agenda_time_data")
        self.label_agenda_day_data = QtWidgets.QLabel(self.centralwidget)
        self.label_agenda_day_data.setGeometry(QtCore.QRect(130, 500, 221, 31))
        font = QtGui.QFont()
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.label_agenda_day_data.setFont(font)
        self.label_agenda_day_data.setObjectName("label_agenda_day_data")
        self.update_now_time_frame = QtWidgets.QComboBox(self.centralwidget)
        self.update_now_time_frame.setGeometry(QtCore.QRect(280, 230, 261, 31))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.update_now_time_frame.setFont(font)
        self.update_now_time_frame.setObjectName("update_now_time_frame")
        self.acptfact_open_soft_spec1 = QtWidgets.QPushButton(self.centralwidget)
        self.acptfact_open_soft_spec1.setGeometry(QtCore.QRect(380, 190, 211, 21))
        self.acptfact_open_soft_spec1.setObjectName("acptfact_open_soft_spec1")
        self.agenda_states = QtWidgets.QTableWidget(self.centralwidget)
        self.agenda_states.setGeometry(QtCore.QRect(1020, 30, 641, 351))
        self.agenda_states.setSizeAdjustPolicy(
            QtWidgets.QAbstractScrollArea.AdjustToContents
        )
        self.agenda_states.setObjectName("agenda_states")
        self.agenda_states.setColumnCount(8)
        self.agenda_states.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_states.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_states.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_states.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_states.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_states.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_states.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_states.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_states.setHorizontalHeaderItem(7, item)
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(430, 840, 331, 20))
        self.label_8.setObjectName("label_8")
        self.acptfact_open_5daysago = QtWidgets.QPushButton(self.centralwidget)
        self.acptfact_open_5daysago.setGeometry(QtCore.QRect(30, 190, 171, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.acptfact_open_5daysago.setFont(font)
        self.acptfact_open_5daysago.setObjectName("acptfact_open_5daysago")
        self.label_last_desc = QtWidgets.QLabel(self.centralwidget)
        self.label_last_desc.setGeometry(QtCore.QRect(120, 300, 891, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        font.setBold(True)
        font.setWeight(75)
        self.label_last_desc.setFont(font)
        self.label_last_desc.setText("")
        self.label_last_desc.setObjectName("label_last_desc")
        self.label_last_burb = QtWidgets.QLabel(self.centralwidget)
        self.label_last_burb.setGeometry(QtCore.QRect(30, 300, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label_last_burb.setFont(font)
        self.label_last_burb.setObjectName("label_last_burb")
        self.problem_popup_button = QtWidgets.QPushButton(self.centralwidget)
        self.problem_popup_button.setGeometry(QtCore.QRect(750, 170, 151, 41))
        self.problem_popup_button.setObjectName("problem_popup_button")
        self.current_file_path_label = QtWidgets.QLabel(self.centralwidget)
        self.current_file_path_label.setGeometry(QtCore.QRect(540, 10, 471, 20))
        self.current_file_path_label.setText("")
        self.current_file_path_label.setObjectName("current_file_path_label")
        self.save_close_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_close_button.setGeometry(QtCore.QRect(420, 10, 111, 21))
        self.save_close_button.setObjectName("save_close_button")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1693, 21))
        self.menubar.setObjectName("menubar")
        self.file_menu = QtWidgets.QMenu(self.menubar)
        self.file_menu.setObjectName("file_menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.fm_open = QtWidgets.QAction(MainWindow)
        self.fm_open.setCheckable(False)
        self.fm_open.setObjectName("fm_open")
        self.fm_save = QtWidgets.QAction(MainWindow)
        self.fm_save.setObjectName("fm_save")
        self.save_as = QtWidgets.QAction(MainWindow)
        self.save_as.setObjectName("save_as")
        self.fm_new = QtWidgets.QAction(MainWindow)
        self.fm_new.setObjectName("fm_new")
        self.file_menu.addAction(self.fm_new)
        self.file_menu.addAction(self.fm_open)
        self.file_menu.addAction(self.fm_save)
        self.file_menu.addAction(self.save_as)
        self.menubar.addAction(self.file_menu.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.editmain_button.setText(
            _translate("MainWindow", "Calendars /  Member /  dimension")
        )
        self.acptfact_open_lower_spec1.setText(
            _translate("MainWindow", "set minutes next midnight")
        )
        self.acptfact_nigh_now.setText(_translate("MainWindow", "Update nigh to Now"))
        self.agenda_task_complete.setText(_translate("MainWindow", "Complete Promise"))
        self.root_datetime_prev_label.setText(_translate("MainWindow", "Past:"))
        self.root_datetime_curr_label.setText(_translate("MainWindow", "Now:"))
        self.label_2.setText(_translate("MainWindow", "What is your present?"))
        self.label_3.setText(
            _translate("MainWindow", "When is the past you have not let go?")
        )
        self.label_agenda_desc_header.setText(_translate("MainWindow", "Description"))
        self.root_datetime_view.setText(_translate("MainWindow", "Manumember change"))
        self.lobby_button.setText(_translate("MainWindow", "Lobby Someone"))
        self.label_7.setText(
            _translate("MainWindow", "Who you are right now. What's missing...")
        )
        self.cb_update_now_repeat.setText(_translate("MainWindow", "Update now per"))
        self.label_time_display.setText(_translate("MainWindow", "Current Time:"))
        self.editagenda_button.setText(_translate("MainWindow", "view current agenda"))
        item = self.acptfacts_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "AcptFactBase"))
        item = self.acptfacts_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "AcptFactPick"))
        item = self.acptfacts_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Base"))
        item = self.acptfacts_table.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Pick"))
        item = self.acptfacts_table.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Open"))
        item = self.acptfacts_table.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "Close"))
        self.calendar_label.setText(_translate("MainWindow", "CALENDAR: "))
        self.lw_desc_update_button.setText(_translate("MainWindow", "Update"))
        self.label_agenda_day_header.setText(_translate("MainWindow", "Day:"))
        self.label_agenda_time_header.setText(_translate("MainWindow", "Time:"))
        self.label_agenda_end_header.setText(_translate("MainWindow", "End:"))
        self.label_agenda_calendar_importance_header1.setText(
            _translate("MainWindow", "root_relative")
        )
        self.label_agenda_family_header1.setText(_translate("MainWindow", "Agenda"))
        self.label_agenda_road_header.setText(_translate("MainWindow", "Road:"))
        self.label_agenda_family_header2.setText(_translate("MainWindow", "Family:"))
        self.label_agenda_calendar_importance_header2.setText(
            _translate("MainWindow", "weight:")
        )
        self.label_agenda_road_data.setText(_translate("MainWindow", "Idea_id:"))
        self.label_agenda_family_data.setText(_translate("MainWindow", "Agenda"))
        self.label_agenda_calendar_importance_data.setText(
            _translate("MainWindow", "weight:")
        )
        self.label_agenda_end_data.setText(_translate("MainWindow", "End:"))
        self.label_agenda_time_data.setText(_translate("MainWindow", "Time:"))
        self.label_agenda_day_data.setText(_translate("MainWindow", "Day:"))
        self.acptfact_open_soft_spec1.setText(
            _translate("MainWindow", '"Soft" moving up the past')
        )
        item = self.agenda_states.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "rank"))
        item = self.agenda_states.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "description"))
        item = self.agenda_states.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "calendar_importance"))
        item = self.agenda_states.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "idea_road"))
        item = self.agenda_states.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "branch_percent"))
        item = self.agenda_states.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "jaja_open"))
        item = self.agenda_states.horizontalHeaderItem(6)
        item.setText(_translate("MainWindow", "jaja_nigh"))
        item = self.agenda_states.horizontalHeaderItem(7)
        item.setText(_translate("MainWindow", "special_road"))
        self.label_8.setText(
            _translate("MainWindow", "Things you promised to be right now")
        )
        self.acptfact_open_5daysago.setText(
            _translate("MainWindow", "Set open 5 days ago")
        )
        self.label_last_burb.setText(_translate("MainWindow", "Last Complete:"))
        self.problem_popup_button.setText(_translate("MainWindow", "Problem Creation"))
        self.save_close_button.setText(_translate("MainWindow", "Save And Close"))
        self.menubar.setAccessibleName(_translate("MainWindow", "File"))
        self.menubar.setAccessibleDescription(
            _translate("MainWindow", "General Operations")
        )
        self.file_menu.setTitle(_translate("MainWindow", "File"))
        self.fm_open.setText(_translate("MainWindow", "Open"))
        self.fm_save.setText(_translate("MainWindow", "Save"))
        self.save_as.setText(_translate("MainWindow", "Save as..."))
        self.fm_new.setText(_translate("MainWindow", "New"))
