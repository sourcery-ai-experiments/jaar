# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\EditParty2bdUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1162, 829)
        self.gp_add_button = QtWidgets.QPushButton(Form)
        self.gp_add_button.setGeometry(QtCore.QRect(500, 330, 121, 61))
        self.gp_add_button.setObjectName("gp_add_button")
        self.gp_remove_button = QtWidgets.QPushButton(Form)
        self.gp_remove_button.setGeometry(QtCore.QRect(500, 200, 111, 61))
        self.gp_remove_button.setObjectName("gp_remove_button")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 45, 281, 41))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(640, 50, 281, 41))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.source_party = QtWidgets.QLabel(Form)
        self.source_party.setGeometry(QtCore.QRect(20, 30, 561, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.source_party.setFont(font)
        self.source_party.setObjectName("source_party")
        self.gp_party_yes = QtWidgets.QTableWidget(Form)
        self.gp_party_yes.setGeometry(QtCore.QRect(10, 90, 481, 581))
        self.gp_party_yes.setObjectName("gp_party_yes")
        self.gp_party_yes.setColumnCount(5)
        self.gp_party_yes.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.gp_party_yes.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.gp_party_yes.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.gp_party_yes.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.gp_party_yes.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.gp_party_yes.setHorizontalHeaderItem(4, item)
        self.gp_party_no = QtWidgets.QTableWidget(Form)
        self.gp_party_no.setGeometry(QtCore.QRect(630, 90, 521, 581))
        self.gp_party_no.setObjectName("gp_party_no")
        self.gp_party_no.setColumnCount(3)
        self.gp_party_no.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.gp_party_no.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.gp_party_no.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.gp_party_no.setHorizontalHeaderItem(2, item)
        self.close_button = QtWidgets.QPushButton(Form)
        self.close_button.setGeometry(QtCore.QRect(720, 10, 93, 28))
        self.close_button.setObjectName("close_button")
        self.quit_button = QtWidgets.QPushButton(Form)
        self.quit_button.setGeometry(QtCore.QRect(830, 10, 93, 28))
        self.quit_button.setObjectName("quit_button")
        self.party2group_weight_edit = QtWidgets.QLineEdit(Form)
        self.party2group_weight_edit.setGeometry(QtCore.QRect(240, 690, 113, 21))
        self.party2group_weight_edit.setObjectName("party2group_weight_edit")
        self.update_weight_button = QtWidgets.QPushButton(Form)
        self.update_weight_button.setGeometry(QtCore.QRect(10, 690, 221, 28))
        self.update_weight_button.setObjectName("update_weight_button")
        self.gp_insert_button = QtWidgets.QPushButton(Form)
        self.gp_insert_button.setGeometry(QtCore.QRect(990, 680, 151, 28))
        self.gp_insert_button.setObjectName("gp_insert_button")
        self.gp_new_edit = QtWidgets.QLineEdit(Form)
        self.gp_new_edit.setGeometry(QtCore.QRect(870, 680, 113, 22))
        self.gp_new_edit.setObjectName("gp_new_edit")
        self.gp_delete_button = QtWidgets.QPushButton(Form)
        self.gp_delete_button.setGeometry(QtCore.QRect(840, 750, 301, 28))
        self.gp_delete_button.setObjectName("gp_delete_button")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(710, 680, 151, 16))
        self.label_3.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(660, 710, 201, 20))
        self.label_4.setAlignment(
            QtCore.Qt.AlignRight | QtCore.Qt.AlignTrailing | QtCore.Qt.AlignVCenter
        )
        self.label_4.setObjectName("label_4")
        self.gp_update_name_edit = QtWidgets.QLineEdit(Form)
        self.gp_update_name_edit.setGeometry(QtCore.QRect(870, 710, 113, 22))
        self.gp_update_name_edit.setObjectName("gp_update_name_edit")
        self.gp_update_button = QtWidgets.QPushButton(Form)
        self.gp_update_button.setGeometry(QtCore.QRect(990, 710, 151, 28))
        self.gp_update_button.setObjectName("gp_update_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTag(_translate("Form", "Form"))
        self.gp_add_button.setText(_translate("Form", "Add Group"))
        self.gp_remove_button.setText(_translate("Form", "Remove Group"))
        self.label.setText(_translate("Form", "Party is party of these Groups"))
        self.label_2.setText(_translate("Form", "Party is not party of these Groups"))
        self.source_party.setText(_translate("Form", "Party (ID): "))
        item = self.gp_party_yes.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Group"))
        item = self.gp_party_yes.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Weight"))
        item = self.gp_party_yes.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Relative_weight"))
        item = self.gp_party_yes.horizontalHeaderItem(3)
        item.setText(_translate("Form", "PartyCount"))
        item = self.gp_party_yes.horizontalHeaderItem(4)
        item.setText(_translate("Form", "ID"))
        item = self.gp_party_no.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Group"))
        item = self.gp_party_no.horizontalHeaderItem(1)
        item.setText(_translate("Form", "PartyCount"))
        item = self.gp_party_no.horizontalHeaderItem(2)
        item.setText(_translate("Form", "ID"))
        self.close_button.setText(_translate("Form", "Close"))
        self.quit_button.setText(_translate("Form", "Quit App"))
        self.update_weight_button.setText(
            _translate("Form", "Update Party's Weight in Group to:")
        )
        self.gp_insert_button.setText(_translate("Form", "Create Group"))
        self.gp_delete_button.setText(_translate("Form", "Delete Group"))
        self.label_3.setText(_translate("Form", "New Group Name:"))
        self.label_4.setText(_translate("Form", "Change Group Name:"))
        self.gp_update_button.setText(_translate("Form", "Update Group"))
