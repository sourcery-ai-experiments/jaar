# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui\EditAcptFactTimeUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(534, 253)
        self.curr_year = QtWidgets.QComboBox(Form)
        self.curr_year.setGeometry(QtCore.QRect(30, 150, 73, 22))
        self.curr_year.setObjectName("curr_year")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(30, 110, 381, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 130, 55, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(120, 130, 55, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(260, 130, 55, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(340, 130, 55, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(420, 130, 55, 16))
        self.label_6.setObjectName("label_6")
        self.curr_month = QtWidgets.QComboBox(Form)
        self.curr_month.setGeometry(QtCore.QRect(110, 150, 141, 22))
        self.curr_month.setObjectName("curr_month")
        self.curr_monthday = QtWidgets.QComboBox(Form)
        self.curr_monthday.setGeometry(QtCore.QRect(260, 150, 73, 22))
        self.curr_monthday.setObjectName("curr_monthday")
        self.curr_hour = QtWidgets.QComboBox(Form)
        self.curr_hour.setGeometry(QtCore.QRect(340, 150, 73, 22))
        self.curr_hour.setObjectName("curr_hour")
        self.curr_min = QtWidgets.QComboBox(Form)
        self.curr_min.setGeometry(QtCore.QRect(420, 150, 73, 22))
        self.curr_min.setObjectName("curr_min")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(20, 100, 501, 141))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.american_update = QtWidgets.QPushButton(self.frame_2)
        self.american_update.setGeometry(QtCore.QRect(190, 100, 101, 31))
        self.american_update.setObjectName("american_update")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(260, 40, 55, 16))
        self.label_11.setObjectName("label_11")
        self.prev_monthday = QtWidgets.QComboBox(Form)
        self.prev_monthday.setGeometry(QtCore.QRect(260, 60, 73, 22))
        self.prev_monthday.setObjectName("prev_monthday")
        self.prev_hour = QtWidgets.QComboBox(Form)
        self.prev_hour.setGeometry(QtCore.QRect(340, 60, 73, 22))
        self.prev_hour.setObjectName("prev_hour")
        self.label_14 = QtWidgets.QLabel(Form)
        self.label_14.setGeometry(QtCore.QRect(30, 20, 391, 16))
        self.label_14.setObjectName("label_14")
        self.prev_year = QtWidgets.QComboBox(Form)
        self.prev_year.setGeometry(QtCore.QRect(30, 60, 73, 22))
        self.prev_year.setObjectName("prev_year")
        self.label_15 = QtWidgets.QLabel(Form)
        self.label_15.setGeometry(QtCore.QRect(30, 40, 55, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(Form)
        self.label_16.setGeometry(QtCore.QRect(340, 40, 55, 16))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(Form)
        self.label_17.setGeometry(QtCore.QRect(120, 40, 55, 16))
        self.label_17.setObjectName("label_17")
        self.prev_month = QtWidgets.QComboBox(Form)
        self.prev_month.setGeometry(QtCore.QRect(110, 60, 141, 22))
        self.prev_month.setObjectName("prev_month")
        self.prev_min = QtWidgets.QComboBox(Form)
        self.prev_min.setGeometry(QtCore.QRect(420, 60, 73, 22))
        self.prev_min.setObjectName("prev_min")
        self.label_18 = QtWidgets.QLabel(Form)
        self.label_18.setGeometry(QtCore.QRect(420, 40, 55, 16))
        self.label_18.setObjectName("label_18")
        self.refresh_root_values = QtWidgets.QPushButton(Form)
        self.refresh_root_values.setGeometry(QtCore.QRect(420, 10, 81, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.refresh_root_values.setFont(font)
        self.refresh_root_values.setObjectName("refresh_root_values")
        self.frame_2.raise_()
        self.curr_year.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.curr_month.raise_()
        self.curr_monthday.raise_()
        self.curr_hour.raise_()
        self.curr_min.raise_()
        self.label_11.raise_()
        self.prev_monthday.raise_()
        self.prev_hour.raise_()
        self.label_14.raise_()
        self.prev_year.raise_()
        self.label_15.raise_()
        self.label_16.raise_()
        self.label_17.raise_()
        self.prev_month.raise_()
        self.prev_min.raise_()
        self.label_18.raise_()
        self.refresh_root_values.raise_()

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowQID(_translate("Form", "Form"))
        self.label.setText(
            _translate(
                "Form", "Reset Current Date for entire ideaunit (American standard)"
            )
        )
        self.label_2.setText(_translate("Form", "Year"))
        self.label_3.setText(_translate("Form", "Month"))
        self.label_4.setText(_translate("Form", "Day"))
        self.label_5.setText(_translate("Form", "Hour"))
        self.label_6.setText(_translate("Form", "Min"))
        self.american_update.setText(_translate("Form", "OK"))
        self.label_11.setText(_translate("Form", "Day"))
        self.label_14.setText(
            _translate(
                "Form", "Reset Previous Date for entire ideaunit (American standard)"
            )
        )
        self.label_15.setText(_translate("Form", "Year"))
        self.label_16.setText(_translate("Form", "Hour"))
        self.label_17.setText(_translate("Form", "Month"))
        self.label_18.setText(_translate("Form", "Min"))
        self.refresh_root_values.setText(_translate("Form", "Refresh"))
