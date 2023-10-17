# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\CureMainUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1557, 750)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.digests_table = QtWidgets.QTableWidget(self.centralwidget)
        self.digests_table.setGeometry(QtCore.QRect(530, 190, 61, 501))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.digests_table.setFont(font)
        self.digests_table.setObjectName("digests_table")
        self.digests_table.setColumnCount(2)
        self.digests_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.digests_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.digests_table.setHorizontalHeaderItem(1, item)
        self.healers_table = QtWidgets.QTableWidget(self.centralwidget)
        self.healers_table.setGeometry(QtCore.QRect(190, 190, 141, 430))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.healers_table.setFont(font)
        self.healers_table.setObjectName("healers_table")
        self.healers_table.setColumnCount(2)
        self.healers_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.healers_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.healers_table.setHorizontalHeaderItem(1, item)
        self.pacts_table = QtWidgets.QTableWidget(self.centralwidget)
        self.pacts_table.setGeometry(QtCore.QRect(10, 310, 171, 381))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pacts_table.setFont(font)
        self.pacts_table.setObjectName("pacts_table")
        self.pacts_table.setColumnCount(2)
        self.pacts_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.pacts_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.pacts_table.setHorizontalHeaderItem(1, item)
        self.depotlinks_table = QtWidgets.QTableWidget(self.centralwidget)
        self.depotlinks_table.setGeometry(QtCore.QRect(340, 190, 191, 501))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlinks_table.setFont(font)
        self.depotlinks_table.setObjectName("depotlinks_table")
        self.depotlinks_table.setColumnCount(4)
        self.depotlinks_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.depotlinks_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.depotlinks_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.depotlinks_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.depotlinks_table.setHorizontalHeaderItem(3, item)
        self.cure_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.cure_delete_button.setGeometry(QtCore.QRect(170, 20, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cure_delete_button.setFont(font)
        self.cure_delete_button.setObjectName("cure_delete_button")
        self.cure_insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.cure_insert_button.setGeometry(QtCore.QRect(20, 50, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cure_insert_button.setFont(font)
        self.cure_insert_button.setObjectName("cure_insert_button")
        self.cure_handle = QtWidgets.QLineEdit(self.centralwidget)
        self.cure_handle.setGeometry(QtCore.QRect(20, 20, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cure_handle.setFont(font)
        self.cure_handle.setObjectName("cure_handle")
        self.cure_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.cure_update_button.setGeometry(QtCore.QRect(20, 80, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cure_update_button.setFont(font)
        self.cure_update_button.setObjectName("cure_update_button")
        self.pact_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.pact_update_button.setGeometry(QtCore.QRect(10, 240, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pact_update_button.setFont(font)
        self.pact_update_button.setObjectName("pact_update_button")
        self.pact_insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.pact_insert_button.setGeometry(QtCore.QRect(10, 210, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pact_insert_button.setFont(font)
        self.pact_insert_button.setObjectName("pact_insert_button")
        self.pact_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.pact_delete_button.setGeometry(QtCore.QRect(80, 270, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pact_delete_button.setFont(font)
        self.pact_delete_button.setObjectName("pact_delete_button")
        self.pact_healer = QtWidgets.QLineEdit(self.centralwidget)
        self.pact_healer.setGeometry(QtCore.QRect(10, 180, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pact_healer.setFont(font)
        self.pact_healer.setObjectName("pact_healer")
        self.healer_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.healer_update_button.setGeometry(QtCore.QRect(190, 130, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.healer_update_button.setFont(font)
        self.healer_update_button.setObjectName("healer_update_button")
        self.healer_insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.healer_insert_button.setGeometry(QtCore.QRect(190, 100, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.healer_insert_button.setFont(font)
        self.healer_insert_button.setObjectName("healer_insert_button")
        self.healer_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.healer_delete_button.setGeometry(QtCore.QRect(240, 40, 91, 28))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.healer_delete_button.setFont(font)
        self.healer_delete_button.setObjectName("healer_delete_button")
        self.healer_title = QtWidgets.QLineEdit(self.centralwidget)
        self.healer_title.setGeometry(QtCore.QRect(190, 70, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.healer_title.setFont(font)
        self.healer_title.setObjectName("healer_title")
        self.depotlink_delete_button = QtWidgets.QPushButton(self.centralwidget)
        self.depotlink_delete_button.setGeometry(QtCore.QRect(480, 20, 101, 28))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_delete_button.setFont(font)
        self.depotlink_delete_button.setObjectName("depotlink_delete_button")
        self.depotlink_title = QtWidgets.QLineEdit(self.centralwidget)
        self.depotlink_title.setGeometry(QtCore.QRect(340, 20, 141, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_title.setFont(font)
        self.depotlink_title.setObjectName("depotlink_title")
        self.depotlink_insert_button = QtWidgets.QPushButton(self.centralwidget)
        self.depotlink_insert_button.setGeometry(QtCore.QRect(376, 50, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_insert_button.setFont(font)
        self.depotlink_insert_button.setObjectName("depotlink_insert_button")
        self.depotlink_update_button = QtWidgets.QPushButton(self.centralwidget)
        self.depotlink_update_button.setGeometry(QtCore.QRect(376, 80, 141, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_update_button.setFont(font)
        self.depotlink_update_button.setObjectName("depotlink_update_button")
        self.refresh_all_button = QtWidgets.QPushButton(self.centralwidget)
        self.refresh_all_button.setGeometry(QtCore.QRect(530, 90, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.refresh_all_button.setFont(font)
        self.refresh_all_button.setObjectName("refresh_all_button")
        self.pact_edit_button = QtWidgets.QPushButton(self.centralwidget)
        self.pact_edit_button.setGeometry(QtCore.QRect(10, 270, 71, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.pact_edit_button.setFont(font)
        self.pact_edit_button.setObjectName("pact_edit_button")
        self.healer_edit_button = QtWidgets.QPushButton(self.centralwidget)
        self.healer_edit_button.setGeometry(QtCore.QRect(190, 160, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.healer_edit_button.setFont(font)
        self.healer_edit_button.setObjectName("healer_edit_button")
        self.depotlink_edit_button = QtWidgets.QPushButton(self.centralwidget)
        self.depotlink_edit_button.setGeometry(QtCore.QRect(340, 160, 91, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_edit_button.setFont(font)
        self.depotlink_edit_button.setObjectName("depotlink_edit_button")
        self.w_agenda_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_agenda_table.setGeometry(QtCore.QRect(1180, 260, 371, 431))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.w_agenda_table.setFont(font)
        self.w_agenda_table.setObjectName("w_agenda_table")
        self.w_agenda_table.setColumnCount(3)
        self.w_agenda_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_agenda_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_agenda_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_agenda_table.setHorizontalHeaderItem(2, item)
        self.w_partys_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_partys_table.setGeometry(QtCore.QRect(1000, 10, 171, 241))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.w_partys_table.setFont(font)
        self.w_partys_table.setObjectName("w_partys_table")
        self.w_partys_table.setColumnCount(3)
        self.w_partys_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_partys_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_partys_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_partys_table.setHorizontalHeaderItem(2, item)
        self.w_groups_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_groups_table.setGeometry(QtCore.QRect(1000, 260, 171, 431))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.w_groups_table.setFont(font)
        self.w_groups_table.setObjectName("w_groups_table")
        self.w_groups_table.setColumnCount(3)
        self.w_groups_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_groups_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_groups_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_groups_table.setHorizontalHeaderItem(2, item)
        self.w_ideas_table = QtWidgets.QTableWidget(self.centralwidget)
        self.w_ideas_table.setGeometry(QtCore.QRect(600, 10, 391, 681))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.w_ideas_table.setFont(font)
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
        self.w_acptfacts_table.setGeometry(QtCore.QRect(1180, 10, 371, 241))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.w_acptfacts_table.setFont(font)
        self.w_acptfacts_table.setObjectName("w_acptfacts_table")
        self.w_acptfacts_table.setColumnCount(3)
        self.w_acptfacts_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.w_acptfacts_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_acptfacts_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.w_acptfacts_table.setHorizontalHeaderItem(2, item)
        self.cure_handle_combo = QtWidgets.QComboBox(self.centralwidget)
        self.cure_handle_combo.setGeometry(QtCore.QRect(20, 110, 141, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cure_handle_combo.setFont(font)
        self.cure_handle_combo.setObjectName("cure_handle_combo")
        self.cure_copy_button = QtWidgets.QPushButton(self.centralwidget)
        self.cure_copy_button.setGeometry(QtCore.QRect(100, 80, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cure_copy_button.setFont(font)
        self.cure_copy_button.setObjectName("cure_copy_button")
        self.depotlink_type_combo = QtWidgets.QComboBox(self.centralwidget)
        self.depotlink_type_combo.setGeometry(QtCore.QRect(376, 110, 141, 26))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_type_combo.setFont(font)
        self.depotlink_type_combo.setObjectName("depotlink_type_combo")
        self.cure_load_button = QtWidgets.QPushButton(self.centralwidget)
        self.cure_load_button.setGeometry(QtCore.QRect(100, 140, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.cure_load_button.setFont(font)
        self.cure_load_button.setObjectName("cure_load_button")
        self.depotlink_weight = QtWidgets.QLineEdit(self.centralwidget)
        self.depotlink_weight.setGeometry(QtCore.QRect(460, 140, 61, 22))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.depotlink_weight.setFont(font)
        self.depotlink_weight.setObjectName("depotlink_weight")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(340, 140, 111, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.ignores_table = QtWidgets.QTableWidget(self.centralwidget)
        self.ignores_table.setGeometry(QtCore.QRect(530, 190, 61, 501))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.ignores_table.setFont(font)
        self.ignores_table.setObjectName("ignores_table")
        self.ignores_table.setColumnCount(2)
        self.ignores_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.ignores_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.ignores_table.setHorizontalHeaderItem(1, item)
        self.show_digests_button = QtWidgets.QPushButton(self.centralwidget)
        self.show_digests_button.setGeometry(QtCore.QRect(530, 120, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.show_digests_button.setFont(font)
        self.show_digests_button.setObjectName("show_digests_button")
        self.show_ignores_button = QtWidgets.QPushButton(self.centralwidget)
        self.show_ignores_button.setGeometry(QtCore.QRect(530, 140, 41, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.show_ignores_button.setFont(font)
        self.show_ignores_button.setObjectName("show_ignores_button")
        self.open_ignore_button = QtWidgets.QPushButton(self.centralwidget)
        self.open_ignore_button.setGeometry(QtCore.QRect(570, 140, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.open_ignore_button.setFont(font)
        self.open_ignore_button.setObjectName("open_ignore_button")
        self.save_ignore_button = QtWidgets.QPushButton(self.centralwidget)
        self.save_ignore_button.setGeometry(QtCore.QRect(570, 160, 31, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.save_ignore_button.setFont(font)
        self.save_ignore_button.setObjectName("save_ignore_button")
        self.set_public_pact_button = QtWidgets.QPushButton(self.centralwidget)
        self.set_public_pact_button.setGeometry(QtCore.QRect(190, 640, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.set_public_pact_button.setFont(font)
        self.set_public_pact_button.setObjectName("set_public_pact_button")
        self.reload_all_src_pacts_button = QtWidgets.QPushButton(self.centralwidget)
        self.reload_all_src_pacts_button.setGeometry(QtCore.QRect(190, 620, 141, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.reload_all_src_pacts_button.setFont(font)
        self.reload_all_src_pacts_button.setObjectName("reload_all_src_pacts_button")
        self.set_public_and_reload_srcs_button = QtWidgets.QPushButton(
            self.centralwidget
        )
        self.set_public_and_reload_srcs_button.setGeometry(
            QtCore.QRect(190, 660, 141, 21)
        )
        font = QtGui.QFont()
        font.setPointSize(8)
        self.set_public_and_reload_srcs_button.setFont(font)
        self.set_public_and_reload_srcs_button.setObjectName(
            "set_public_and_reload_srcs_button"
        )
        self.isol_open_button = QtWidgets.QPushButton(self.centralwidget)
        self.isol_open_button.setGeometry(QtCore.QRect(530, 50, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.isol_open_button.setFont(font)
        self.isol_open_button.setObjectName("isol_open_button")
        self.isol_save_button = QtWidgets.QPushButton(self.centralwidget)
        self.isol_save_button.setGeometry(QtCore.QRect(530, 70, 51, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.isol_save_button.setFont(font)
        self.isol_save_button.setObjectName("isol_save_button")
        self.five_issue_button = QtWidgets.QPushButton(self.centralwidget)
        self.five_issue_button.setGeometry(QtCore.QRect(450, 160, 61, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.five_issue_button.setFont(font)
        self.five_issue_button.setObjectName("five_issue_button")
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
        item = self.digests_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Digest"))
        item = self.healers_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Healers"))
        item = self.pacts_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "CURE Stories"))
        item = self.depotlinks_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Contractlinks"))
        item = self.depotlinks_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Weight"))
        item = self.depotlinks_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Type"))
        self.cure_delete_button.setText(_translate("MainWindow", "delete "))
        self.cure_insert_button.setText(_translate("MainWindow", "Add new Cure"))
        self.cure_update_button.setText(_translate("MainWindow", "Change Title"))
        self.pact_update_button.setText(
            _translate("MainWindow", "Change Contract Title")
        )
        self.pact_insert_button.setText(_translate("MainWindow", "Add new Contract"))
        self.pact_delete_button.setText(_translate("MainWindow", "Delete"))
        self.healer_update_button.setText(
            _translate("MainWindow", "Change Healer Title")
        )
        self.healer_insert_button.setText(_translate("MainWindow", "Add new Healer"))
        self.healer_delete_button.setText(_translate("MainWindow", "delete Healer"))
        self.depotlink_delete_button.setText(
            _translate("MainWindow", "delete ContractLink")
        )
        self.depotlink_insert_button.setText(
            _translate("MainWindow", "Add new ContractLink")
        )
        self.depotlink_update_button.setText(
            _translate("MainWindow", "Update ContractLink")
        )
        self.refresh_all_button.setText(_translate("MainWindow", "refresh"))
        self.pact_edit_button.setText(_translate("MainWindow", "Edit "))
        self.healer_edit_button.setText(_translate("MainWindow", "Edit Healer"))
        self.depotlink_edit_button.setText(
            _translate("MainWindow", "Edit ContractLink")
        )
        item = self.w_agenda_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Healers Agenda"))
        item = self.w_agenda_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.w_partys_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Healers Partys"))
        item = self.w_partys_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.w_groups_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Healers Groups"))
        item = self.w_groups_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "New Column"))
        item = self.w_ideas_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Healer Ideas"))
        item = self.w_ideas_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Idea pad"))
        item = self.w_acptfacts_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "AcptFacts Base"))
        item = self.w_acptfacts_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "AcptFacts AcptFact"))
        self.cure_copy_button.setText(_translate("MainWindow", "Copy"))
        self.cure_load_button.setText(_translate("MainWindow", "load"))
        self.label.setText(_translate("MainWindow", "Contractlink Weight:"))
        item = self.ignores_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Ignore"))
        self.show_digests_button.setText(_translate("MainWindow", "digest"))
        self.show_ignores_button.setText(_translate("MainWindow", "ignore"))
        self.open_ignore_button.setText(_translate("MainWindow", "o"))
        self.save_ignore_button.setText(_translate("MainWindow", "s"))
        self.set_public_pact_button.setText(
            _translate("MainWindow", "output_pact to public_dir")
        )
        self.reload_all_src_pacts_button.setText(
            _translate("MainWindow", "refresh_all_src_pacts")
        )
        self.set_public_and_reload_srcs_button.setText(
            _translate("MainWindow", "dest2public and refresh")
        )
        self.isol_open_button.setText(_translate("MainWindow", "isol"))
        self.isol_save_button.setText(_translate("MainWindow", "save"))
        self.five_issue_button.setText(_translate("MainWindow", "5 issue"))
        self.menubar.setAccessibleName(_translate("MainWindow", "File"))
        self.menubar.setAccessibleDescription(
            _translate("MainWindow", "General Operations")
        )
        self.file_menu.setTitle(_translate("MainWindow", "File"))
        self.fm_open.setText(_translate("MainWindow", "Open"))
        self.fm_save.setText(_translate("MainWindow", "Save"))
        self.save_as.setText(_translate("MainWindow", "Save as..."))
        self.fm_new.setText(_translate("MainWindow", "New"))
