# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\dev\reddibrush\ui\cultureMainUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1557, 792)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.cultures_table = QtWidgets.QTableWidget(self.centralwidget)
        self.cultures_table.setGeometry(QtCore.QRect(10, 190, 151, 501))
        self.cultures_table.setObjectName("cultures_table")
        self.cultures_table.setColumnCount(2)
        self.cultures_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.cultures_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.cultures_table.setHorizontalHeaderItem(1, item)
        self.healers_table = QtWidgets.QTableWidget(self.centralwidget)
        self.healers_table.setGeometry(QtCore.QRect(350, 190, 171, 501))
        self.healers_table.setObjectName("healers_table")
        self.healers_table.setColumnCount(2)
        self.healers_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.healers_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.healers_table.setHorizontalHeaderItem(1, item)
        self.agendas_table = QtWidgets.QTableWidget(self.centralwidget)
        self.agendas_table.setGeometry(QtCore.QRect(170, 190, 171, 501))
        self.agendas_table.setObjectName("agendas_table")
        self.agendas_table.setColumnCount(2)
        self.agendas_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.agendas_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.agendas_table.setHorizontalHeaderItem(1, item)
        self.depotlinks_table = QtWidgets.QTableWidget(self.centralwidget)
        self.depotlinks_table.setGeometry(QtCore.QRect(530, 190, 171, 501))
        self.depotlinks_table.setObjectName("depotlinks_table")
        self.depotlinks_table.setColumnCount(2)
        self.depotlinks_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.depotlinks_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.depotlinks_table.setHorizontalHeaderItem(1, item)
        self.culture_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.culture_delete_button.setGeometry(QtCore.QRect(80, 110, 81, 28))
        self.culture_delete_button.setObjectName("culture_delete_button")
        self.culture_insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.culture_insert_button.setGeometry(QtCore.QRect(20, 50, 141, 31))
        self.culture_insert_button.setObjectName("culture_insert_button")
        self.culture_handle = QtWidgets.QLineEdit(self.centralwidget)
        self.culture_handle.setGeometry(QtCore.QRect(20, 20, 141, 22))
        self.culture_handle.setObjectName("culture_handle")
        self.culture_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.culture_update_button.setGeometry(QtCore.QRect(20, 80, 141, 31))
        self.culture_update_button.setObjectName("culture_update_button")
        self.agenda_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.agenda_update_button.setGeometry(QtCore.QRect(180, 80, 141, 31))
        self.agenda_update_button.setObjectName("agenda_update_button")
        self.agenda_insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.agenda_insert_button.setGeometry(QtCore.QRect(180, 50, 141, 31))
        self.agenda_insert_button.setObjectName("agenda_insert_button")
        self.agenda_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.agenda_delete_button.setGeometry(QtCore.QRect(240, 110, 81, 28))
        self.agenda_delete_button.setObjectName("agenda_delete_button")
        self.agenda_healer = QtWidgets.QLineEdit(self.centralwidget)
        self.agenda_healer.setGeometry(QtCore.QRect(180, 20, 141, 22))
        self.agenda_healer.setObjectName("agenda_healer")
        self.healer_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.healer_update_button.setGeometry(QtCore.QRect(350, 80, 141, 31))
        self.healer_update_button.setObjectName("healer_update_button")
        self.healer_insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.healer_insert_button.setGeometry(QtCore.QRect(350, 50, 141, 31))
        self.healer_insert_button.setObjectName("healer_insert_button")
        self.healer_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.healer_delete_button.setGeometry(QtCore.QRect(410, 110, 81, 28))
        self.healer_delete_button.setObjectName("healer_delete_button")
        self.kitchen_title = QtWidgets.QLineEdit(self.centralwidget)
        self.kitchen_title.setGeometry(QtCore.QRect(350, 20, 141, 22))
        self.kitchen_title.setObjectName("kitchen_title")
        self.depotlink_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.depotlink_delete_button.setGeometry(QtCore.QRect(580, 110, 91, 28))
        self.depotlink_delete_button.setObjectName("depotlink_delete_button")
        self.depotlink_title = QtWidgets.QLineEdit(self.centralwidget)
        self.depotlink_title.setGeometry(QtCore.QRect(530, 20, 141, 22))
        self.depotlink_title.setObjectName("depotlink_title")
        self.depotlink_insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.depotlink_insert_button.setGeometry(QtCore.QRect(530, 50, 141, 31))
        self.depotlink_insert_button.setObjectName("depotlink_insert_button")
        self.depotlink_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.depotlink_update_button.setGeometry(QtCore.QRect(530, 80, 141, 31))
        self.depotlink_update_button.setObjectName("depotlink_update_button")
        self.refresh_all_button = QtWidgets.QPushButton(self.centralwidget)
        self.refresh_all_button.setGeometry(QtCore.QRect(10, 700, 141, 31))
        self.refresh_all_button.setObjectName("refresh_all_button")
        self.agenda_edit_button = QtWidgets.QPushButton(self.centralwidget)
        self.agenda_edit_button.setGeometry(QtCore.QRect(170, 160, 91, 31))
        self.agenda_edit_button.setObjectName("agenda_edit_button")
        self.healer_edit_button = QtWidgets.QPushButton(self.centralwidget)
        self.healer_edit_button.setGeometry(QtCore.QRect(350, 160, 91, 31))
        self.healer_edit_button.setObjectName("healer_edit_button")
        self.depotlink_edit_button = QtWidgets.QPushButton(self.centralwidget)
        self.depotlink_edit_button.setGeometry(QtCore.QRect(530, 160, 91, 31))
        self.depotlink_edit_button.setObjectName("depotlink_edit_button")
        self.eluc_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.eluc_update_button.setGeometry(QtCore.QRect(710, 80, 141, 31))
        self.eluc_update_button.setObjectName("eluc_update_button")
        self.eluc_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.eluc_delete_button.setGeometry(QtCore.QRect(760, 110, 91, 28))
        self.eluc_delete_button.setObjectName("eluc_delete_button")
        self.eluc_title = QtWidgets.QLineEdit(self.centralwidget)
        self.eluc_title.setGeometry(QtCore.QRect(710, 20, 141, 22))
        self.eluc_title.setObjectName("eluc_title")
        self.eluc_edit_button = QtWidgets.QPushButton(self.centralwidget)
        self.eluc_edit_button.setGeometry(QtCore.QRect(710, 160, 91, 31))
        self.eluc_edit_button.setObjectName("eluc_edit_button")
        self.elucs_table = QtWidgets.QTableWidget(self.centralwidget)
        self.elucs_table.setGeometry(QtCore.QRect(710, 190, 171, 501))
        self.elucs_table.setObjectName("elucs_table")
        self.elucs_table.setColumnCount(2)
        self.elucs_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.elucs_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.elucs_table.setHorizontalHeaderItem(1, item)
        self.eluc_insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.eluc_insert_button.setGeometry(QtCore.QRect(710, 50, 141, 31))
        self.eluc_insert_button.setObjectName("eluc_insert_button")
        self.w_goal_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_goal_table.setGeometry(QtCore.QRect(1320, 260, 171, 431))
        self.w_goal_table.setObjectName("w_goal_table")
        self.w_goal_table.setColumnCount(2)
        self.w_goal_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_goal_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_goal_table.setHorizontalHeaderItem(1, item)
        self.w_partys_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_partys_table.setGeometry(QtCore.QRect(1140, 10, 171, 241))
        self.w_partys_table.setObjectName("w_partys_table")
        self.w_partys_table.setColumnCount(2)
        self.w_partys_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_partys_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_partys_table.setHorizontalHeaderItem(1, item)
        self.w_groups_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_groups_table.setGeometry(QtCore.QRect(1140, 260, 171, 431))
        self.w_groups_table.setObjectName("w_groups_table")
        self.w_groups_table.setColumnCount(2)
        self.w_groups_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_groups_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_groups_table.setHorizontalHeaderItem(1, item)
        self.w_ideas_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_ideas_table.setGeometry(QtCore.QRect(900, 10, 231, 681))
        self.w_ideas_table.setObjectName("w_ideas_table")
        self.w_ideas_table.setColumnCount(3)
        self.w_ideas_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_ideas_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_ideas_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_ideas_table.setHorizontalHeaderItem(2, item)
        self.w_acptfacts_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_acptfacts_table.setGeometry(QtCore.QRect(1320, 10, 171, 241))
        self.w_acptfacts_table.setObjectName("w_acptfacts_table")
        self.w_acptfacts_table.setColumnCount(2)
        self.w_acptfacts_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_acptfacts_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_acptfacts_table.setHorizontalHeaderItem(1, item)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1557, 21))
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
        item = self.cultures_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "cultures"))
        item = self.healers_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Healers"))
        item = self.agendas_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "culture Stories"))
        item = self.depotlinks_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Agendalinks"))
        self.culture_delete_button.setText(_translate("MainWindow", "delete culture"))
        self.culture_insert_button.setText(_translate("MainWindow", "Add new culture"))
        self.culture_update_button.setText(
            _translate("MainWindow", "Change culture Title")
        )
        self.agenda_update_button.setText(
            _translate("MainWindow", "Change Agenda Title")
        )
        self.agenda_insert_button.setText(_translate("MainWindow", "Add new Agenda"))
        self.agenda_delete_button.setText(_translate("MainWindow", "delete Agenda"))
        self.healer_update_button.setText(
            _translate("MainWindow", "Change Healer Title")
        )
        self.healer_insert_button.setText(_translate("MainWindow", "Add new Healer"))
        self.healer_delete_button.setText(_translate("MainWindow", "delete Healer"))
        self.depotlink_delete_button.setText(_translate("MainWindow", "delete Agenda"))
        self.depotlink_insert_button.setText(_translate("MainWindow", "Add new Agenda"))
        self.depotlink_update_button.setText(
            _translate("MainWindow", "Change Agenda Title")
        )
        self.refresh_all_button.setText(_translate("MainWindow", "Refresh Tables"))
        self.agenda_edit_button.setText(_translate("MainWindow", "Edit Agenda"))
        self.healer_edit_button.setText(_translate("MainWindow", "Edit Healer"))
        self.depotlink_edit_button.setText(_translate("MainWindow", "Edit Agenda"))
        self.eluc_update_button.setText(_translate("MainWindow", "Change Agenda Title"))
        self.eluc_delete_button.setText(_translate("MainWindow", "delete Agenda"))
        self.eluc_edit_button.setText(_translate("MainWindow", "Edit Agenda"))
        item = self.elucs_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Elucs"))
        self.eluc_insert_button.setText(_translate("MainWindow", "Add new Agenda"))
        item = self.w_goal_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Healers Agenda"))
        item = self.w_partys_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Healers Partys"))
        item = self.w_groups_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Healers Groups"))
        item = self.w_ideas_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Healer Ideas"))
        item = self.w_ideas_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Idea pad"))
        item = self.w_acptfacts_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Healers AcptFacts"))
        self.menubar.setAccessibleName(_translate("MainWindow", "File"))
        self.menubar.setAccessibleDescription(
            _translate("MainWindow", "General Operations")
        )
        self.file_menu.setTitle(_translate("MainWindow", "File"))
        self.fm_open.setText(_translate("MainWindow", "Open"))
        self.fm_save.setText(_translate("MainWindow", "Save"))
        self.save_as.setText(_translate("MainWindow", "Save as..."))
        self.fm_new.setText(_translate("MainWindow", "New"))
