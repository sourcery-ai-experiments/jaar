# command to for converting ui form to python file: pyuic5 ui\EditMainUI.ui -o ui\EditMainUI.py
from ui.EditMainUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QTableWidgetItem as qtw1
from ui.EditIdeaUnit import EditIdeaUnit
from ui.EditParty import EditParty
from ui.pyqt_func import (
    agenda_importance_diplay,
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
        self.party_list.itemClicked.connect(self.open_edit_party)
        self.close_button.clicked.connect(self.close)
        self.open_groupedit_button.clicked.connect(self.open_edit_party)

        # self.beliefs_table.itemClicked.connect(self.belief_base_combo_set)
        self.beliefs_table.setObjectName("Agenda Beliefs")
        self.beliefs_table.setColumnWidth(0, 300)
        self.beliefs_table.setColumnWidth(1, 300)
        self.beliefs_table.setColumnWidth(2, 30)
        self.beliefs_table.setColumnWidth(3, 30)
        self.beliefs_table.setColumnWidth(4, 30)
        self.beliefs_table.setColumnWidth(5, 30)
        self.beliefs_table.setColumnHidden(0, False)
        self.beliefs_table.setColumnHidden(1, False)
        self.beliefs_table.setColumnHidden(2, True)
        self.beliefs_table.setColumnHidden(3, True)
        self.beliefs_table.setColumnHidden(4, True)
        self.beliefs_table.setColumnHidden(5, True)
        self.beliefs_table.horizontalHeaderVisible = True
        self.beliefs_table.setHorizontalHeaderLabels(
            ["BeliefBase", "BeliefSelect", "Base", "Belief", "Open", "Nigh"]
        )
        self.beliefs_table.setRowCount(0)
        self.beliefs_table.itemClicked.connect(self.belief_table_select)
        self.belief_base_update_combo.currentTextAtomd.connect(
            self.belief_pick_combo_load
        )
        self.belief_update_button.clicked.connect(self.belief_set_action)
        self.belief_delete_button.clicked.connect(self.belief_del_action)

        self.x_agenda = None

    def belief_set_action(self):
        self.x_agenda.set_belief(
            base=self.belief_base_update_combo.currentText(),
            pick=self.belief_pick_update_combo.currentText(),
            open=pyqt_func_str2float(self.belief_open.text()),
            nigh=pyqt_func_str2float(self.belief_nigh.text()),
        )
        self.refresh_all()

    def belief_del_action(self):
        self.x_agenda.del_belief(base=self.belief_base_update_combo.currentText())
        self.refresh_all()

    def get_beliefs_list(self):
        return self.x_agenda._idearoot._beliefunits.values()

    def beliefs_table_load(self):
        self.beliefs_table.setRowCount(0)

        row = 0
        for belief in self.get_beliefs_list():
            base_text = belief.base.replace(f"{self.x_agenda._owner_id}", "")
            base_text = base_text[1:]
            belief_text = belief.pick.replace(belief.base, "")
            belief_text = belief_text[1:]
            if belief.open is None:
                belief_text = f"{belief_text}"
            elif base_text == "time,jajatime":
                belief_text = f"{self.x_agenda.get_jajatime_legible_one_time_event(belief.open)}-{self.x_agenda.get_jajatime_repeating_legible_text(belief.nigh)}"
            else:
                belief_text = f"{belief_text} Open-Nigh {belief.open}-{belief.nigh}"

            self._beliefs_table_set_row_and_2_columns(row, base_text, belief_text)
            self.beliefs_table.setItem(row, 2, qtw1(belief.base))
            self.beliefs_table.setItem(row, 3, qtw1(belief.pick))
            self.beliefs_table.setItem(row, 4, qtw1(pyqt_func_num2str(belief.open)))
            self.beliefs_table.setItem(row, 5, qtw1(pyqt_func_num2str(belief.nigh)))
            row += 1

        for base, count in self.x_agenda.get_missing_belief_bases().items():
            base_text = base.replace(f"{self.x_agenda._owner_id}", "")
            base_text = base_text[1:]

            base_lecture_text = f"{base_text} ({count} nodes)"
            self._beliefs_table_set_row_and_2_columns(row, base_lecture_text, "")
            self.beliefs_table.setItem(row, 2, qtw1(base))
            self.beliefs_table.setItem(row, 3, qtw1(""))
            self.beliefs_table.setItem(row, 4, qtw1(""))
            self.beliefs_table.setItem(row, 5, qtw1(""))
            row += 1
        self.belief_clear_fields()

    def _beliefs_table_set_row_and_2_columns(self, row, base_text, belief_text):
        self.beliefs_table.setRowCount(row + 1)
        self.beliefs_table.setItem(row, 0, qtw1(base_text))
        self.beliefs_table.setItem(row, 1, qtw1(belief_text))
        self.beliefs_table.setColumnWidth(0, 140)
        self.beliefs_table.setColumnWidth(1, 450)

    def belief_clear_fields(self):
        self.belief_base_update_combo.clear()
        self.belief_pick_update_combo.clear()
        self.belief_open.clear()
        self.belief_nigh.clear()

    def belief_table_select(self):
        self.belief_base_update_combo.clear()
        self.belief_base_update_combo.addItems(
            self.x_agenda.get_idea_tree_ordered_road_list()
        )
        self.belief_base_update_combo.setCurrentText(
            self.beliefs_table.item(self.beliefs_table.currentRow(), 2).text()
        )

        self.belief_pick_combo_load()
        self.belief_pick_update_combo.setCurrentText(
            self.beliefs_table.item(self.beliefs_table.currentRow(), 3).text()
        )

        self.belief_open.clear()
        self.belief_open.setText(
            pyqt_func_num2str(
                self.beliefs_table.item(self.beliefs_table.currentRow(), 4).text()
            )
        )

        self.belief_nigh.clear()
        self.belief_nigh.setText(
            pyqt_func_num2str(
                self.beliefs_table.item(self.beliefs_table.currentRow(), 5).text()
            )
        )

    def belief_pick_combo_load(self):
        self.belief_pick_update_combo.clear()
        self.belief_pick_update_combo.addItems(
            self.x_agenda.get_heir_road_list(
                self.belief_base_update_combo.currentText()
            )
        )

    def belief_update_heir(self, base_road):
        if self.belief_update_combo.currentText() == "":
            raise EditMainViewException("No comboup selection for belief update.")
        if self.beliefs_table.item(self.beliefs_table.currentRow(), 2).text() is None:
            raise EditMainViewException("No table selection for belief update.")
        belief_update_combo_text = self.belief_update_combo.currentText()
        self.x_agenda._idearoot._beliefunits[base_road].belief = (
            belief_update_combo_text
        )
        self.base_road = None
        self.refresh_all

    def refresh_all(self):
        if self.x_agenda != None:
            self.refresh_party_list()
            self.refresh_idea_tree()
            self.beliefs_table_load()

    def refresh_party_list(self):
        # party_list is qtw.QTableWidget()
        self.party_list.setObjectName("Party Calculated Weight")
        self.party_list.setColumnCount(2)
        self.party_list.setColumnWidth(0, 170)
        self.party_list.setColumnWidth(1, 70)
        self.party_list.setHorizontalHeaderLabels(["PID", "LW Force"])
        partys_list = list(self.x_agenda._partys.values())
        partys_list.sort(key=lambda x: x._agenda_credit, reverse=True)

        for row, party in enumerate(partys_list, start=1):
            groups_count = 0
            for group in self.x_agenda._groups.values():
                for partylink in group._partys.values():
                    if partylink.party_id == party.party_id:
                        groups_count += 1

            qt_agenda_credit = qtw.QTableWidgetItem(
                agenda_importance_diplay(party._agenda_credit)
            )
            qt_group = qtw.QTableWidgetItem(f"{groups_count}")
            self.party_list.setRowCount(row)
            self.party_list.setItem(row - 1, 0, qtw.QTableWidgetItem(party.party_id))
            self.party_list.setItem(row - 1, 1, qt_agenda_credit)

    def open_editideaunit(self):
        self.EditIdeaunit = EditIdeaUnit()
        self.EditIdeaunit.x_agenda = self.x_agenda
        self.EditIdeaunit.refresh_tree()
        self.EditIdeaunit.show()

    def open_edit_party(self):
        self.edit_party = EditParty()
        self.edit_party.x_agenda = self.x_agenda
        self.edit_party.refresh_all()
        self.edit_party.show()

    def refresh_idea_tree(self):
        tree_root = get_pyqttree(idearoot=self.x_agenda._idearoot)
        self.baseideaunit.clear()
        self.baseideaunit.insertTopLevelItems(0, [tree_root])

        # expand to depth set by agenda
        def yo_tree_setExpanded(root):
            child_count = root.childCount()
            for i in range(child_count):
                item = root.child(i)
                item.setExpanded(item.data(2, 20))
                yo_tree_setExpanded(item)

        root = self.baseideaunit.invisibleRootItem()
        yo_tree_setExpanded(root)
