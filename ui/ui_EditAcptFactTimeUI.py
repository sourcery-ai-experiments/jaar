# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\dev\reddibrush\ui\EditFactTimeUI.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(663, 702)
        self.curr_year = QtWidgets.QComboBox(Form)
        self.curr_year.setGeometry(QtCore.QRect(20, 100, 73, 22))
        self.curr_year.setObjectName("curr_year")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(20, 60, 381, 16))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(20, 80, 55, 16))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(110, 80, 55, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(250, 80, 55, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(330, 80, 55, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(410, 80, 55, 16))
        self.label_6.setObjectName("label_6")
        self.curr_american_update = QtWidgets.QPushButton(Form)
        self.curr_american_update.setGeometry(QtCore.QRect(100, 140, 381, 41))
        self.curr_american_update.setObjectName("curr_american_update")
        self.curr_month = QtWidgets.QComboBox(Form)
        self.curr_month.setGeometry(QtCore.QRect(100, 100, 141, 22))
        self.curr_month.setObjectName("curr_month")
        self.curr_monthday = QtWidgets.QComboBox(Form)
        self.curr_monthday.setGeometry(QtCore.QRect(250, 100, 73, 22))
        self.curr_monthday.setObjectName("curr_monthday")
        self.curr_hour = QtWidgets.QComboBox(Form)
        self.curr_hour.setGeometry(QtCore.QRect(330, 100, 73, 22))
        self.curr_hour.setObjectName("curr_hour")
        self.curr_min = QtWidgets.QComboBox(Form)
        self.curr_min.setGeometry(QtCore.QRect(410, 100, 73, 22))
        self.curr_min.setObjectName("curr_min")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(10, 220, 381, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(20, 240, 81, 16))
        self.label_8.setObjectName("label_8")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 210, 501, 121))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.curr_local_update = QtWidgets.QPushButton(self.frame)
        self.curr_local_update.setGeometry(QtCore.QRect(100, 80, 381, 41))
        self.curr_local_update.setObjectName("curr_local_update")
        self.label_9 = QtWidgets.QLabel(self.frame)
        self.label_9.setGeometry(QtCore.QRect(150, 30, 121, 16))
        self.label_9.setObjectName("label_9")
        self.curr_day_id = QtWidgets.QComboBox(self.frame)
        self.curr_day_id.setGeometry(QtCore.QRect(20, 50, 101, 22))
        self.curr_day_id.setObjectName("curr_day_id")
        self.curr_daymin_id = QtWidgets.QComboBox(self.frame)
        self.curr_daymin_id.setGeometry(QtCore.QRect(150, 50, 81, 22))
        self.curr_daymin_id.setObjectName("curr_daymin_id")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setGeometry(QtCore.QRect(10, 50, 501, 121))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(20, 550, 391, 16))
        self.label_10.setObjectName("label_10")
        self.frame_3 = QtWidgets.QFrame(Form)
        self.frame_3.setGeometry(QtCore.QRect(10, 540, 501, 121))
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.prev_local_update = QtWidgets.QPushButton(self.frame_3)
        self.prev_local_update.setGeometry(QtCore.QRect(100, 80, 371, 41))
        self.prev_local_update.setObjectName("prev_local_update")
        self.label_13 = QtWidgets.QLabel(self.frame_3)
        self.label_13.setGeometry(QtCore.QRect(140, 30, 111, 16))
        self.label_13.setObjectName("label_13")
        self.prev_daymin_id = QtWidgets.QComboBox(self.frame_3)
        self.prev_daymin_id.setGeometry(QtCore.QRect(140, 50, 81, 22))
        self.prev_daymin_id.setObjectName("prev_daymin_id")
        self.prev_day_id = QtWidgets.QComboBox(self.frame_3)
        self.prev_day_id.setGeometry(QtCore.QRect(10, 50, 101, 22))
        self.prev_day_id.setObjectName("prev_day_id")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(250, 410, 55, 16))
        self.label_11.setObjectName("label_11")
        self.prev_monthday = QtWidgets.QComboBox(Form)
        self.prev_monthday.setGeometry(QtCore.QRect(250, 430, 73, 22))
        self.prev_monthday.setObjectName("prev_monthday")
        self.prev_american_update = QtWidgets.QPushButton(Form)
        self.prev_american_update.setGeometry(QtCore.QRect(110, 470, 371, 41))
        self.prev_american_update.setObjectName("prev_american_update")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(30, 570, 71, 16))
        self.label_12.setObjectName("label_12")
        self.prev_hour = QtWidgets.QComboBox(Form)
        self.prev_hour.setGeometry(QtCore.QRect(330, 430, 73, 22))
        self.prev_hour.setObjectName("prev_hour")
        self.label_14 = QtWidgets.QLabel(Form)
        self.label_14.setGeometry(QtCore.QRect(20, 390, 391, 16))
        self.label_14.setObjectName("label_14")
        self.prev_year = QtWidgets.QComboBox(Form)
        self.prev_year.setGeometry(QtCore.QRect(20, 430, 73, 22))
        self.prev_year.setObjectName("prev_year")
        self.label_15 = QtWidgets.QLabel(Form)
        self.label_15.setGeometry(QtCore.QRect(20, 410, 55, 16))
        self.label_15.setObjectName("label_15")
        self.label_16 = QtWidgets.QLabel(Form)
        self.label_16.setGeometry(QtCore.QRect(330, 410, 55, 16))
        self.label_16.setObjectName("label_16")
        self.label_17 = QtWidgets.QLabel(Form)
        self.label_17.setGeometry(QtCore.QRect(110, 410, 55, 16))
        self.label_17.setObjectName("label_17")
        self.prev_month = QtWidgets.QComboBox(Form)
        self.prev_month.setGeometry(QtCore.QRect(100, 430, 141, 22))
        self.prev_month.setObjectName("prev_month")
        self.prev_min = QtWidgets.QComboBox(Form)
        self.prev_min.setGeometry(QtCore.QRect(410, 430, 73, 22))
        self.prev_min.setObjectName("prev_min")
        self.label_18 = QtWidgets.QLabel(Form)
        self.label_18.setGeometry(QtCore.QRect(410, 410, 55, 16))
        self.label_18.setObjectName("label_18")
        self.refresh_root_values = QtWidgets.QPushButton(Form)
        self.refresh_root_values.setGeometry(QtCore.QRect(342, 10, 141, 28))
        font = QtGui.QFont()
        font.setBold(False)
        font.setItalic(True)
        font.setWeight(50)
        self.refresh_root_values.setFont(font)
        self.refresh_root_values.setObjectName("refresh_root_values")
        self.frame_2.raise_()
        self.frame.raise_()
        self.frame_3.raise_()
        self.curr_year.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.label_3.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.label_6.raise_()
        self.curr_american_update.raise_()
        self.curr_month.raise_()
        self.curr_monthday.raise_()
        self.curr_hour.raise_()
        self.curr_min.raise_()
        self.label_7.raise_()
        self.label_8.raise_()
        self.label_10.raise_()
        self.label_11.raise_()
        self.prev_monthday.raise_()
        self.prev_american_update.raise_()
        self.label_12.raise_()
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
        Form.setWindowTitle(_translate("Form", "Form"))
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
        self.curr_american_update.setText(
            _translate("Form", "Use American Dates to change Current Date")
        )
        self.label_7.setText(
            _translate(
                "Form", "Reset Current Date for entire ideaunit (My Day Listing)"
            )
        )
        self.label_8.setText(_translate("Form", "Day ID"))
        self.curr_local_update.setText(
            _translate("Form", "Use Local Structure Dates to change Current Date")
        )
        self.label_9.setText(_translate("Form", "Day_Min ID"))
        self.label_10.setText(
            _translate(
                "Form", "Reset Previous Date for entire ideaunit (My Day Listing)"
            )
        )
        self.prev_local_update.setText(
            _translate("Form", "Use Local Structure Dates to change Previous Date")
        )
        self.label_13.setText(_translate("Form", "Day_Min ID"))
        self.label_11.setText(_translate("Form", "Day"))
        self.prev_american_update.setText(
            _translate("Form", "Use American Dates to change Previous Date")
        )
        self.label_12.setText(_translate("Form", "Day ID"))
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
