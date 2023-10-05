# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\EditPartyUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1199, 771)
        self.party_insert_button = QtWidgets.QPushButton(Form)
        self.party_insert_button.setGeometry(QtCore.QRect(170, 40, 61, 31))
        self.party_insert_button.setObjectName("party_insert_button")
        self.party_update_button = QtWidgets.QPushButton(Form)
        self.party_update_button.setGeometry(QtCore.QRect(170, 70, 61, 28))
        self.party_update_button.setObjectName("party_update_button")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(10, 80, 61, 21))
        self.label_3.setWordWrap(True)
        self.label_3.setObjectName("label_3")
        self.party_delete_button = QtWidgets.QPushButton(Form)
        self.party_delete_button.setGeometry(QtCore.QRect(10, 100, 151, 28))
        self.party_delete_button.setObjectName("party_delete_button")
        self.party_table = QtWidgets.QTableWidget(Form)
        self.party_table.setGeometry(QtCore.QRect(10, 130, 511, 621))
        self.party_table.setObjectName("party_table")
        self.party_table.setColumnCount(5)
        self.party_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.party_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.party_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.party_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.party_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.party_table.setHorizontalHeaderItem(4, item)
        self.close_button = QtWidgets.QPushButton(Form)
        self.close_button.setGeometry(QtCore.QRect(1090, 10, 93, 28))
        self.close_button.setObjectName("close_button")
        self.quit_button = QtWidgets.QPushButton(Form)
        self.quit_button.setGeometry(QtCore.QRect(1090, 40, 93, 28))
        self.quit_button.setObjectName("quit_button")
        self.party_name = QtWidgets.QLineEdit(Form)
        self.party_name.setGeometry(QtCore.QRect(10, 40, 151, 31))
        self.party_name.setObjectName("party_name")
        self.groups_in_table = QtWidgets.QTableWidget(Form)
        self.groups_in_table.setGeometry(QtCore.QRect(530, 130, 381, 511))
        self.groups_in_table.setObjectName("groups_in_table")
        self.groups_in_table.setColumnCount(5)
        self.groups_in_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.groups_in_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_in_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_in_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_in_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_in_table.setHorizontalHeaderItem(4, item)
        self.groups_out_table = QtWidgets.QTableWidget(Form)
        self.groups_out_table.setGeometry(QtCore.QRect(920, 130, 261, 621))
        self.groups_out_table.setObjectName("groups_out_table")
        self.groups_out_table.setColumnCount(5)
        self.groups_out_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.groups_out_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_out_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_out_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_out_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_out_table.setHorizontalHeaderItem(4, item)
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(20, 10, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_4.setFont(font)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(760, 10, 161, 21))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.label_5.setFont(font)
        self.label_5.setWordWrap(True)
        self.label_5.setObjectName("label_5")
        self.group_update_button = QtWidgets.QPushButton(Form)
        self.group_update_button.setGeometry(QtCore.QRect(880, 70, 91, 28))
        self.group_update_button.setObjectName("group_update_button")
        self.group_delete_button = QtWidgets.QPushButton(Form)
        self.group_delete_button.setGeometry(QtCore.QRect(720, 100, 151, 28))
        self.group_delete_button.setObjectName("group_delete_button")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(730, 70, 161, 21))
        self.label_6.setWordWrap(True)
        self.label_6.setObjectName("label_6")
        self.group_insert_button = QtWidgets.QPushButton(Form)
        self.group_insert_button.setGeometry(QtCore.QRect(880, 40, 91, 31))
        self.group_insert_button.setObjectName("group_insert_button")
        self.group_name = QtWidgets.QLineEdit(Form)
        self.group_name.setGeometry(QtCore.QRect(720, 40, 151, 31))
        self.group_name.setObjectName("group_name")
        self.party_group_set_button = QtWidgets.QPushButton(Form)
        self.party_group_set_button.setGeometry(QtCore.QRect(1060, 100, 121, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.party_group_set_button.setFont(font)
        self.party_group_set_button.setObjectName("party_group_set_button")
        self.party_group_del_button = QtWidgets.QPushButton(Form)
        self.party_group_del_button.setGeometry(QtCore.QRect(530, 100, 161, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.party_group_del_button.setFont(font)
        self.party_group_del_button.setObjectName("party_group_del_button")
        self.groups_stan_table = QtWidgets.QTableWidget(Form)
        self.groups_stan_table.setGeometry(QtCore.QRect(530, 650, 381, 101))
        self.groups_stan_table.setObjectName("groups_stan_table")
        self.groups_stan_table.setColumnCount(5)
        self.groups_stan_table.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.groups_stan_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_stan_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_stan_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_stan_table.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.groups_stan_table.setHorizontalHeaderItem(4, item)
        self.party_weight = QtWidgets.QLineEdit(Form)
        self.party_weight.setGeometry(QtCore.QRect(70, 70, 91, 31))
        self.party_weight.setObjectName("party_weight")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTag(_translate("Form", "Form"))
        self.party_insert_button.setText(_translate("Form", "Add Party"))
        self.party_update_button.setText(_translate("Form", "Update"))
        self.label_3.setText(_translate("Form", "Weight:"))
        self.party_delete_button.setText(_translate("Form", "delete Party"))
        item = self.party_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.party_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.party_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "3"))
        item = self.party_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "4"))
        item = self.party_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "5"))
        self.close_button.setText(_translate("Form", "Close"))
        self.quit_button.setText(_translate("Form", "Quit App"))
        item = self.groups_in_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.groups_in_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.groups_in_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "3"))
        item = self.groups_in_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "4"))
        item = self.groups_in_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "5"))
        item = self.groups_out_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.groups_out_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.groups_out_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "3"))
        item = self.groups_out_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "4"))
        item = self.groups_out_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "5"))
        self.label_4.setText(_translate("Form", "Partys"))
        self.label_5.setText(_translate("Form", "Groups"))
        self.group_update_button.setText(_translate("Form", "Update Group"))
        self.group_delete_button.setText(_translate("Form", "delete Group"))
        self.label_6.setText(_translate("Form", "Change Name to:"))
        self.group_insert_button.setText(_translate("Form", "Add Group"))
        self.party_group_set_button.setText(_translate("Form", "add group to party"))
        self.party_group_del_button.setText(
            _translate("Form", "remove group from party")
        )
        item = self.groups_stan_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "1"))
        item = self.groups_stan_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "2"))
        item = self.groups_stan_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "3"))
        item = self.groups_stan_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "4"))
        item = self.groups_stan_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "5"))
