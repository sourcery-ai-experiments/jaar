# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\EditAlly2bdUI.ui'
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
        self.bd_add_button = QtWidgets.QPushButton(Form)
        self.bd_add_button.setGeometry(QtCore.QRect(500, 330, 121, 61))
        self.bd_add_button.setObjectName("bd_add_button")
        self.bd_remove_button = QtWidgets.QPushButton(Form)
        self.bd_remove_button.setGeometry(QtCore.QRect(500, 200, 111, 61))
        self.bd_remove_button.setObjectName("bd_remove_button")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(10, 45, 281, 41))
        self.label.setWordWrap(True)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(640, 50, 281, 41))
        self.label_2.setWordWrap(True)
        self.label_2.setObjectName("label_2")
        self.source_ally = QtWidgets.QLabel(Form)
        self.source_ally.setGeometry(QtCore.QRect(20, 30, 561, 20))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.source_ally.setFont(font)
        self.source_ally.setObjectName("source_ally")
        self.bd_member_yes = QtWidgets.QTableWidget(Form)
        self.bd_member_yes.setGeometry(QtCore.QRect(10, 90, 481, 581))
        self.bd_member_yes.setObjectName("bd_member_yes")
        self.bd_member_yes.setColumnCount(5)
        self.bd_member_yes.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.bd_member_yes.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.bd_member_yes.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.bd_member_yes.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.bd_member_yes.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.bd_member_yes.setHorizontalHeaderItem(4, item)
        self.bd_member_no = QtWidgets.QTableWidget(Form)
        self.bd_member_no.setGeometry(QtCore.QRect(630, 90, 521, 581))
        self.bd_member_no.setObjectName("bd_member_no")
        self.bd_member_no.setColumnCount(3)
        self.bd_member_no.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.bd_member_no.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.bd_member_no.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.bd_member_no.setHorizontalHeaderItem(2, item)
        self.close_button = QtWidgets.QPushButton(Form)
        self.close_button.setGeometry(QtCore.QRect(720, 10, 93, 28))
        self.close_button.setObjectName("close_button")
        self.quit_button = QtWidgets.QPushButton(Form)
        self.quit_button.setGeometry(QtCore.QRect(830, 10, 93, 28))
        self.quit_button.setObjectName("quit_button")
        self.ally2brand_weight_edit = QtWidgets.QLineEdit(Form)
        self.ally2brand_weight_edit.setGeometry(QtCore.QRect(240, 690, 113, 21))
        self.ally2brand_weight_edit.setObjectName("ally2brand_weight_edit")
        self.update_weight_button = QtWidgets.QPushButton(Form)
        self.update_weight_button.setGeometry(QtCore.QRect(10, 690, 221, 28))
        self.update_weight_button.setObjectName("update_weight_button")
        self.bd_insert_button = QtWidgets.QPushButton(Form)
        self.bd_insert_button.setGeometry(QtCore.QRect(990, 680, 151, 28))
        self.bd_insert_button.setObjectName("bd_insert_button")
        self.bd_new_edit = QtWidgets.QLineEdit(Form)
        self.bd_new_edit.setGeometry(QtCore.QRect(870, 680, 113, 22))
        self.bd_new_edit.setObjectName("bd_new_edit")
        self.bd_delete_button = QtWidgets.QPushButton(Form)
        self.bd_delete_button.setGeometry(QtCore.QRect(840, 750, 301, 28))
        self.bd_delete_button.setObjectName("bd_delete_button")
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
        self.bd_update_name_edit = QtWidgets.QLineEdit(Form)
        self.bd_update_name_edit.setGeometry(QtCore.QRect(870, 710, 113, 22))
        self.bd_update_name_edit.setObjectName("bd_update_name_edit")
        self.bd_update_button = QtWidgets.QPushButton(Form)
        self.bd_update_button.setGeometry(QtCore.QRect(990, 710, 151, 28))
        self.bd_update_button.setObjectName("bd_update_button")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.bd_add_button.setText(_translate("Form", "Add Brand"))
        self.bd_remove_button.setText(_translate("Form", "Remove Brand"))
        self.label.setText(_translate("Form", "Ally is member of these Brands"))
        self.label_2.setText(_translate("Form", "Ally is not member of these Brands"))
        self.source_ally.setText(_translate("Form", "Ally (ID): "))
        item = self.bd_member_yes.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Brand"))
        item = self.bd_member_yes.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Weight"))
        item = self.bd_member_yes.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Relative_weight"))
        item = self.bd_member_yes.horizontalHeaderItem(3)
        item.setText(_translate("Form", "MemberCount"))
        item = self.bd_member_yes.horizontalHeaderItem(4)
        item.setText(_translate("Form", "ID"))
        item = self.bd_member_no.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Brand"))
        item = self.bd_member_no.horizontalHeaderItem(1)
        item.setText(_translate("Form", "MemberCount"))
        item = self.bd_member_no.horizontalHeaderItem(2)
        item.setText(_translate("Form", "ID"))
        self.close_button.setText(_translate("Form", "Close"))
        self.quit_button.setText(_translate("Form", "Quit App"))
        self.update_weight_button.setText(
            _translate("Form", "Update Ally's Weight in Group to:")
        )
        self.bd_insert_button.setText(_translate("Form", "Create Brand"))
        self.bd_delete_button.setText(_translate("Form", "Delete Brand"))
        self.label_3.setText(_translate("Form", "New Brand Name:"))
        self.label_4.setText(_translate("Form", "Change Brand Name:"))
        self.bd_update_button.setText(_translate("Form", "Update Brand"))
