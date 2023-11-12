# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\EditMainUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1431, 712)
        self.input = QtWidgets.QLineEdit(Form)
        self.input.setGeometry(QtCore.QRect(40, 20, 601, 31))
        self.input.setObjectName("input")
        self.refresh_button = QtWidgets.QPushButton(Form)
        self.refresh_button.setGeometry(QtCore.QRect(670, 20, 161, 31))
        self.refresh_button.setObjectName("refresh_button")
        self.baseideaunit = QtWidgets.QTreeWidget(Form)
        self.baseideaunit.setGeometry(QtCore.QRect(10, 60, 400, 630))
        self.baseideaunit.setObjectName("baseideaunit")
        self.baseideaunit.headerItem().setText(0, "1")
        self.close_button = QtWidgets.QPushButton(Form)
        self.close_button.setGeometry(QtCore.QRect(890, 20, 93, 28))
        self.close_button.setObjectName("close_button")
        self.party_list = QtWidgets.QTableWidget(Form)
        self.party_list.setGeometry(QtCore.QRect(420, 100, 261, 591))
        self.party_list.setObjectName("party_list")
        self.party_list.setColumnCount(0)
        self.party_list.setRowCount(0)
        self.open_groupedit_button = QtWidgets.QPushButton(Form)
        self.open_groupedit_button.setGeometry(QtCore.QRect(430, 60, 161, 31))
        self.open_groupedit_button.setObjectName("open_groupedit_button")
        self.acptfacts_table = QtWidgets.QTableWidget(Form)
        self.acptfacts_table.setGeometry(QtCore.QRect(690, 180, 641, 511))
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
        self.acptfact_pick_update_combo = QtWidgets.QComboBox(Form)
        self.acptfact_pick_update_combo.setGeometry(QtCore.QRect(760, 110, 421, 26))
        self.acptfact_pick_update_combo.setObjectName("acptfact_pick_update_combo")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(700, 140, 71, 20))
        self.label_10.setObjectName("label_10")
        self.acptfact_nigh = QtWidgets.QLineEdit(Form)
        self.acptfact_nigh.setGeometry(QtCore.QRect(1030, 140, 151, 31))
        self.acptfact_nigh.setObjectName("acptfact_nigh")
        self.acptfact_delete_button = QtWidgets.QPushButton(Form)
        self.acptfact_delete_button.setGeometry(QtCore.QRect(1190, 110, 131, 30))
        self.acptfact_delete_button.setObjectName("acptfact_delete_button")
        self.acptfact_open = QtWidgets.QLineEdit(Form)
        self.acptfact_open.setGeometry(QtCore.QRect(760, 140, 161, 31))
        self.acptfact_open.setObjectName("acptfact_open")
        self.display_problem_acptfacts_cb = QtWidgets.QCheckBox(Form)
        self.display_problem_acptfacts_cb.setGeometry(QtCore.QRect(1190, 140, 161, 31))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.display_problem_acptfacts_cb.setFont(font)
        self.display_problem_acptfacts_cb.setObjectName("display_problem_acptfacts_cb")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(690, 110, 61, 20))
        self.label_9.setObjectName("label_9")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(690, 80, 61, 20))
        self.label_6.setObjectName("label_6")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(950, 140, 71, 20))
        self.label_11.setObjectName("label_11")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(770, 60, 141, 20))
        self.label_5.setObjectName("label_5")
        self.acptfact_update_button = QtWidgets.QPushButton(Form)
        self.acptfact_update_button.setGeometry(QtCore.QRect(1190, 80, 131, 30))
        self.acptfact_update_button.setObjectName("acptfact_update_button")
        self.acptfact_base_update_combo = QtWidgets.QComboBox(Form)
        self.acptfact_base_update_combo.setGeometry(QtCore.QRect(760, 80, 421, 26))
        self.acptfact_base_update_combo.setObjectName("acptfact_base_update_combo")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowQID(_translate("Form", "Form"))
        self.refresh_button.setText(_translate("Form", "Refresh All"))
        self.close_button.setText(_translate("Form", "Close"))
        self.open_groupedit_button.setText(_translate("Form", "Open Group Edit"))
        item = self.acptfacts_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "AcptFactBase"))
        item = self.acptfacts_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "AcptFactPick"))
        item = self.acptfacts_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Base"))
        item = self.acptfacts_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Pick"))
        item = self.acptfacts_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Open"))
        item = self.acptfacts_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Close"))
        self.label_10.setText(_translate("Form", "Open"))
        self.acptfact_delete_button.setText(_translate("Form", "Del AcptFact"))
        self.display_problem_acptfacts_cb.setText(
            _translate("Form", "Only Problem AcptFacts")
        )
        self.label_9.setText(_translate("Form", "AcptFact Pick:"))
        self.label_6.setText(_translate("Form", "AcptFact Base:"))
        self.label_11.setText(_translate("Form", "Nigh"))
        self.label_5.setText(_translate("Form", "Change what is acptfact"))
        self.acptfact_update_button.setText(_translate("Form", "Set AcptFact"))
