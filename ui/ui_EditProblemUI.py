# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\dev\reddibrush\ui\EditProblemUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1880, 712)
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(90, 140, 301, 21))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.close_button = QtWidgets.QPushButton(Form)
        self.close_button.setGeometry(QtCore.QRect(1740, 20, 93, 28))
        self.close_button.setObjectName("close_button")
        self.quit_button = QtWidgets.QPushButton(Form)
        self.quit_button.setGeometry(QtCore.QRect(1640, 20, 93, 28))
        self.quit_button.setObjectName("quit_button")
        self.problem_context_text = QtWidgets.QLineEdit(Form)
        self.problem_context_text.setGeometry(QtCore.QRect(80, 200, 391, 31))
        self.problem_context_text.setObjectName("problem_context_text")
        self.agenda_table = QtWidgets.QTableWidget(Form)
        self.agenda_table.setGeometry(QtCore.QRect(750, 50, 651, 631))
        self.agenda_table.setObjectName("agenda_table")
        self.agenda_table.setColumnCount(8)
        self.agenda_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_table.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_table.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_table.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.agenda_table.setHorizontalHeaderItem(7, item)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(90, 40, 301, 21))
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.problem_name_text = QtWidgets.QLineEdit(Form)
        self.problem_name_text.setGeometry(QtCore.QRect(80, 100, 391, 31))
        self.problem_name_text.setObjectName("problem_name_text")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(90, 260, 301, 21))
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.problem_context_combo = QtWidgets.QComboBox(Form)
        self.problem_context_combo.setGeometry(QtCore.QRect(80, 161, 391, 31))
        self.problem_context_combo.setObjectName("problem_context_combo")
        self.problem_name_combo = QtWidgets.QComboBox(Form)
        self.problem_name_combo.setGeometry(QtCore.QRect(80, 60, 391, 31))
        self.problem_name_combo.setObjectName("problem_name_combo")
        self.add_brand_button = QtWidgets.QPushButton(Form)
        self.add_brand_button.setGeometry(QtCore.QRect(500, 310, 161, 28))
        self.add_brand_button.setObjectName("add_brand_button")
        self.brand1_name_combo = QtWidgets.QComboBox(Form)
        self.brand1_name_combo.setGeometry(QtCore.QRect(80, 281, 291, 31))
        self.brand1_name_combo.setObjectName("brand1_name_combo")
        self.add_brand_text = QtWidgets.QLineEdit(Form)
        self.add_brand_text.setGeometry(QtCore.QRect(500, 280, 161, 31))
        self.add_brand_text.setObjectName("add_brand_text")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(50, 290, 31, 21))
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(50, 320, 51, 31))
        self.label_7.setWordWrap(True)
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(50, 360, 51, 31))
        self.label_8.setWordWrap(True)
        self.label_8.setObjectName("label_8")
        self.brand2_name_combo = QtWidgets.QComboBox(Form)
        self.brand2_name_combo.setGeometry(QtCore.QRect(80, 320, 291, 31))
        self.brand2_name_combo.setObjectName("brand2_name_combo")
        self.brand3_name_combo = QtWidgets.QComboBox(Form)
        self.brand3_name_combo.setGeometry(QtCore.QRect(80, 360, 291, 31))
        self.brand3_name_combo.setObjectName("brand3_name_combo")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(500, 350, 171, 41))
        self.label_9.setWordWrap(True)
        self.label_9.setObjectName("label_9")
        self.brand1_weight_text = QtWidgets.QLineEdit(Form)
        self.brand1_weight_text.setGeometry(QtCore.QRect(380, 280, 91, 31))
        self.brand1_weight_text.setObjectName("brand1_weight_text")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(400, 260, 81, 21))
        self.label_10.setWordWrap(True)
        self.label_10.setObjectName("label_10")
        self.brand2_weight_text = QtWidgets.QLineEdit(Form)
        self.brand2_weight_text.setGeometry(QtCore.QRect(380, 320, 91, 31))
        self.brand2_weight_text.setObjectName("brand2_weight_text")
        self.brand3_weight_text = QtWidgets.QLineEdit(Form)
        self.brand3_weight_text.setGeometry(QtCore.QRect(380, 360, 91, 31))
        self.brand3_weight_text.setObjectName("brand3_weight_text")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(90, 420, 301, 21))
        self.label_11.setWordWrap(True)
        self.label_11.setObjectName("label_11")
        self.action1_combo = QtWidgets.QComboBox(Form)
        self.action1_combo.setGeometry(QtCore.QRect(80, 440, 391, 31))
        self.action1_combo.setObjectName("action1_combo")
        self.action1_text = QtWidgets.QLineEdit(Form)
        self.action1_text.setGeometry(QtCore.QRect(80, 480, 391, 31))
        self.action1_text.setObjectName("action1_text")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(50, 590, 51, 31))
        self.label_12.setWordWrap(True)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(Form)
        self.label_13.setGeometry(QtCore.QRect(50, 520, 51, 31))
        self.label_13.setWordWrap(True)
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(Form)
        self.label_14.setGeometry(QtCore.QRect(50, 450, 31, 21))
        self.label_14.setWordWrap(True)
        self.label_14.setObjectName("label_14")
        self.action2_combo = QtWidgets.QComboBox(Form)
        self.action2_combo.setGeometry(QtCore.QRect(80, 521, 391, 31))
        self.action2_combo.setObjectName("action2_combo")
        self.action2_text = QtWidgets.QLineEdit(Form)
        self.action2_text.setGeometry(QtCore.QRect(80, 560, 391, 31))
        self.action2_text.setObjectName("action2_text")
        self.action3_combo = QtWidgets.QComboBox(Form)
        self.action3_combo.setGeometry(QtCore.QRect(80, 601, 391, 31))
        self.action3_combo.setObjectName("action3_combo")
        self.action3_text = QtWidgets.QLineEdit(Form)
        self.action3_text.setGeometry(QtCore.QRect(80, 640, 391, 31))
        self.action3_text.setObjectName("action3_text")
        self.baseideaunit = QtWidgets.QTreeWidget(Form)
        self.baseideaunit.setGeometry(QtCore.QRect(1420, 50, 411, 631))
        self.baseideaunit.setIndentation(15)
        self.baseideaunit.setObjectName("baseideaunit")
        self.refresh_button = QtWidgets.QPushButton(Form)
        self.refresh_button.setGeometry(QtCore.QRect(1220, 10, 171, 31))
        self.refresh_button.setObjectName("refresh_button")
        self.load_problem_button = QtWidgets.QPushButton(Form)
        self.load_problem_button.setGeometry(QtCore.QRect(490, 600, 171, 31))
        self.load_problem_button.setObjectName("load_problem_button")
        self.view_problems_cb = QtWidgets.QCheckBox(Form)
        self.view_problems_cb.setGeometry(QtCore.QRect(1420, 10, 211, 41))
        font = QtGui.QFont()
        font.setPointSize(10)
        self.view_problems_cb.setFont(font)
        self.view_problems_cb.setObjectName("view_problems_cb")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_3.setText(_translate("Form", "What is the Problem's context"))
        self.close_button.setText(_translate("Form", "Close"))
        self.quit_button.setText(_translate("Form", "Quit App"))
        item = self.agenda_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "0"))
        item = self.agenda_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "1"))
        item = self.agenda_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "2"))
        item = self.agenda_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "3"))
        item = self.agenda_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "4"))
        item = self.agenda_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "5"))
        item = self.agenda_table.horizontalHeaderItem(6)
        item.setText(_translate("Form", "6"))
        item = self.agenda_table.horizontalHeaderItem(7)
        item.setText(_translate("Form", "7"))
        self.label_4.setText(_translate("Form", "What is the Problem"))
        self.label_5.setText(_translate("Form", "Which group is this for?"))
        self.add_brand_button.setText(_translate("Form", "add Brand/Group"))
        self.label_6.setText(_translate("Form", "1."))
        self.label_7.setText(_translate("Form", "2."))
        self.label_8.setText(_translate("Form", "3."))
        self.label_9.setText(
            _translate("Form", "Add people to groups in oter interface")
        )
        self.label_10.setText(_translate("Form", "weight"))
        self.label_11.setText(
            _translate("Form", "What's a thing you're going to do about it")
        )
        self.label_12.setText(_translate("Form", "3."))
        self.label_13.setText(_translate("Form", "2."))
        self.label_14.setText(_translate("Form", "1."))
        self.baseideaunit.headerItem().setText(0, _translate("Form", "ideaunit"))
        self.refresh_button.setText(_translate("Form", "Refresh All"))
        self.load_problem_button.setText(_translate("Form", "Load Problem"))
        self.view_problems_cb.setText(_translate("Form", "view only problems"))
