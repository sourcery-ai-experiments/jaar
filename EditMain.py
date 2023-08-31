# command to for converting ui form to python file: pyuic5 ui\EditMainUI.ui -o ui\EditMainUI.py
from ui.EditMainUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QTableWidgetItem as qtw1
from EditIdeaUnit import EditIdeaUnit
from EditMember import EditMember
from src.pyqt5_kit.pyqt_func import (
    lw_diplay,
    get_pyqttree,
    str2float as pyqt_func_str2float,
    num2str as pyqt_func_num2str,
)


class EditMainViewException(Exception):
    pass


class EditMainView(qtw.QWidget, Ui_Form):
    """The settings dialog window"""

    refresh_ideaunit_submitted = qtc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.refresh_button.clicked.connect(self.refresh_all)
        self.baseideaunit.itemClicked.connect(self.open_editideaunit)
        self.member_list.itemClicked.connect(self.open_edit_member)
        self.close_button.clicked.connect(self.close)
        self.open_groupedit_button.clicked.connect(self.open_edit_member)

        # self.acptfacts_table.itemClicked.connect(self.acptfact_base_combo_set)
        self.acptfacts_table.setObjectName("Agent AcptFacts")
        self.acptfacts_table.setColumnWidth(0, 300)
        self.acptfacts_table.setColumnWidth(1, 300)
        self.acptfacts_table.setColumnWidth(2, 30)
        self.acptfacts_table.setColumnWidth(3, 30)
        self.acptfacts_table.setColumnWidth(4, 30)
        self.acptfacts_table.setColumnWidth(5, 30)
        self.acptfacts_table.setColumnHidden(0, False)
        self.acptfacts_table.setColumnHidden(1, False)
        self.acptfacts_table.setColumnHidden(2, True)
        self.acptfacts_table.setColumnHidden(3, True)
        self.acptfacts_table.setColumnHidden(4, True)
        self.acptfacts_table.setColumnHidden(5, True)
        self.acptfacts_table.horizontalHeaderVisible = True
        self.acptfacts_table.setHorizontalHeaderLabels(
            ["AcptFactBase", "AcptFactSelect", "Base", "AcptFact", "Open", "Nigh"]
        )
        self.acptfacts_table.setRowCount(0)
        self.acptfacts_table.itemClicked.connect(self.acptfact_table_select)
        self.acptfact_base_update_combo.currentTextChanged.connect(
            self.acptfact_pick_combo_load
        )
        self.acptfact_update_button.clicked.connect(self.acptfact_set_action)
        self.acptfact_delete_button.clicked.connect(self.acptfact_del_action)

        self.agent_x = None

    def acptfact_set_action(self):
        self.agent_x.set_acptfact(
            base=self.acptfact_base_update_combo.currentText(),
            pick=self.acptfact_pick_update_combo.currentText(),
            open=pyqt_func_str2float(self.acptfact_open.text()),
            nigh=pyqt_func_str2float(self.acptfact_nigh.text()),
        )
        self.refresh_all()

    def acptfact_del_action(self):
        self.agent_x.del_acptfact(base=self.acptfact_base_update_combo.currentText())
        self.refresh_all()

    def get_acptfacts_list(self):
        x_list = []
        if self.display_problem_acptfacts_cb.checkState() == 2:
            x_list.extend(
                acptfact
                for acptfact in self.agent_x._idearoot._acptfactunits.values()
                if (
                    self.agent_x.get_idea_kid(road=acptfact.base)._problem_bool
                    or self.agent_x.get_idea_kid(road=acptfact.pick)._problem_bool
                )
            )
        else:
            x_list = self.agent_x._idearoot._acptfactunits.values()
        return x_list

    def acptfacts_table_load(self):
        self.acptfacts_table.setRowCount(0)

        row = 0
        for acptfact in self.get_acptfacts_list():
            base_text = acptfact.base.replace(f"{self.agent_x._desc}", "")
            base_text = base_text[1:]
            acptfact_text = acptfact.pick.replace(acptfact.base, "")
            acptfact_text = acptfact_text[1:]
            if acptfact.open is None:
                acptfact_text = f"{acptfact_text}"
            elif base_text == "time,jajatime":
                acptfact_text = f"{self.agent_x.get_jajatime_readable_one_time_event(acptfact.open)}-{self.agent_x.get_jajatime_repeating_readable_text(acptfact.nigh)}"
            else:
                acptfact_text = (
                    f"{acptfact_text} Open-Nigh {acptfact.open}-{acptfact.nigh}"
                )

            self._acptfacts_table_set_row_and_2_columns(row, base_text, acptfact_text)
            self.acptfacts_table.setItem(row, 2, qtw1(acptfact.base))
            self.acptfacts_table.setItem(row, 3, qtw1(acptfact.pick))
            self.acptfacts_table.setItem(row, 4, qtw1(pyqt_func_num2str(acptfact.open)))
            self.acptfacts_table.setItem(row, 5, qtw1(pyqt_func_num2str(acptfact.nigh)))
            row += 1

        for base, count in self.agent_x.get_missing_acptfact_bases().items():
            base_text = base.replace(f"{self.agent_x._desc}", "")
            base_text = base_text[1:]

            base_explain_text = f"{base_text} ({count} nodes)"
            self._acptfacts_table_set_row_and_2_columns(row, base_explain_text, "")
            self.acptfacts_table.setItem(row, 2, qtw1(base))
            self.acptfacts_table.setItem(row, 3, qtw1(""))
            self.acptfacts_table.setItem(row, 4, qtw1(""))
            self.acptfacts_table.setItem(row, 5, qtw1(""))
            row += 1
        self.acptfact_clear_fields()

    def _acptfacts_table_set_row_and_2_columns(self, row, base_text, acptfact_text):
        self.acptfacts_table.setRowCount(row + 1)
        self.acptfacts_table.setItem(row, 0, qtw1(base_text))
        self.acptfacts_table.setItem(row, 1, qtw1(acptfact_text))
        self.acptfacts_table.setColumnWidth(0, 140)
        self.acptfacts_table.setColumnWidth(1, 450)

    def acptfact_clear_fields(self):
        self.acptfact_base_update_combo.clear()
        self.acptfact_pick_update_combo.clear()
        self.acptfact_open.clear()
        self.acptfact_nigh.clear()

    def acptfact_table_select(self):
        self.acptfact_base_update_combo.clear()
        self.acptfact_base_update_combo.addItems(
            self.agent_x.get_idea_tree_ordered_road_list()
        )
        self.acptfact_base_update_combo.setCurrentText(
            self.acptfacts_table.item(self.acptfacts_table.currentRow(), 2).text()
        )

        self.acptfact_pick_combo_load()
        self.acptfact_pick_update_combo.setCurrentText(
            self.acptfacts_table.item(self.acptfacts_table.currentRow(), 3).text()
        )

        self.acptfact_open.clear()
        self.acptfact_open.setText(
            pyqt_func_num2str(
                self.acptfacts_table.item(self.acptfacts_table.currentRow(), 4).text()
            )
        )

        self.acptfact_nigh.clear()
        self.acptfact_nigh.setText(
            pyqt_func_num2str(
                self.acptfacts_table.item(self.acptfacts_table.currentRow(), 5).text()
            )
        )

    def acptfact_pick_combo_load(self):
        self.acptfact_pick_update_combo.clear()
        self.acptfact_pick_update_combo.addItems(
            self.agent_x.get_heir_road_list(
                src_road=self.acptfact_base_update_combo.currentText()
            )
        )

    def acptfact_update_heir(self, base_road):
        if self.acptfact_update_combo.currentText() == "":
            raise EditMainViewException("No comboup selection for acptfact update.")
        if (
            self.acptfacts_table.item(self.acptfacts_table.currentRow(), 2).text()
            is None
        ):
            raise EditMainViewException("No table selection for acptfact update.")
        acptfact_update_combo_text = self.acptfact_update_combo.currentText()
        self.agent_x._idearoot._acptfactunits[
            base_road
        ].acptfact = acptfact_update_combo_text
        self.base_road = None
        self.refresh_all

    def refresh_all(self):
        if self.agent_x != None:
            self.refresh_member_list()
            self.refresh_idea_tree()
            self.acptfacts_table_load()

    def refresh_member_list(self):
        # member_list is qtw.QTableWidget()
        self.member_list.setObjectName("Member Calculated Weight")
        self.member_list.setColumnCount(2)
        self.member_list.setColumnWidth(0, 170)
        self.member_list.setColumnWidth(1, 70)
        self.member_list.setHorizontalHeaderLabels(["Name", "LW Force"])
        members_list = list(self.agent_x._members.values())
        members_list.sort(key=lambda x: x._agent_credit, reverse=True)

        for row, member in enumerate(members_list, start=1):
            groups_count = 0
            for group in self.agent_x._groups.values():
                for memberlink in group._members.values():
                    if memberlink.name == member.name:
                        groups_count += 1

            qt_agent_credit = qtw.QTableWidgetItem(lw_diplay(member._agent_credit))
            qt_group = qtw.QTableWidgetItem(f"{groups_count}")
            self.member_list.setRowCount(row)
            self.member_list.setItem(row - 1, 0, qtw.QTableWidgetItem(member.name))
            self.member_list.setItem(row - 1, 1, qt_agent_credit)

    def open_editideaunit(self):
        self.EditIdeaunit = EditIdeaUnit()
        self.EditIdeaunit.agent_x = self.agent_x
        self.EditIdeaunit.refresh_tree()
        self.EditIdeaunit.show()

    def open_edit_member(self):
        self.edit_member = EditMember()
        self.edit_member.agent_x = self.agent_x
        self.edit_member.refresh_all()
        self.edit_member.show()

    def refresh_idea_tree(self):
        tree_root = get_pyqttree(idearoot=self.agent_x._idearoot)
        self.baseideaunit.clear()
        self.baseideaunit.insertTopLevelItems(0, [tree_root])

        # expand to depth set by agent
        def yo_tree_setExpanded(root):
            child_count = root.childCount()
            for i in range(child_count):
                item = root.child(i)
                item.setExpanded(item.data(2, 20))
                yo_tree_setExpanded(item)

        root = self.baseideaunit.invisibleRootItem()
        yo_tree_setExpanded(root)
