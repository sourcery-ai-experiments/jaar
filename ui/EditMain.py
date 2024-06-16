# command to for converting ui form to python file: pyuic5 ui\EditMainUI.ui -o ui\EditMainUI.py
from ui.EditMainUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QTableWidgetItem as qtw1
from ui.EditIdeaUnit import EditIdeaUnit
from ui.EditGuy import EditGuy
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
        self.guy_list.itemClicked.connect(self.open_edit_guy)
        self.close_button.clicked.connect(self.close)
        self.open_beliefedit_button.clicked.connect(self.open_edit_guy)

        # self.facts_table.itemClicked.connect(self.fact_base_combo_set)
        self.facts_table.setObjectName("Agenda Facts")
        self.facts_table.setColumnWidth(0, 300)
        self.facts_table.setColumnWidth(1, 300)
        self.facts_table.setColumnWidth(2, 30)
        self.facts_table.setColumnWidth(3, 30)
        self.facts_table.setColumnWidth(4, 30)
        self.facts_table.setColumnWidth(5, 30)
        self.facts_table.setColumnHidden(0, False)
        self.facts_table.setColumnHidden(1, False)
        self.facts_table.setColumnHidden(2, True)
        self.facts_table.setColumnHidden(3, True)
        self.facts_table.setColumnHidden(4, True)
        self.facts_table.setColumnHidden(5, True)
        self.facts_table.horizontalHeaderVisible = True
        self.facts_table.setHorizontalHeaderLabels(
            ["FactBase", "FactSelect", "Base", "Fact", "Open", "Nigh"]
        )
        self.facts_table.setRowCount(0)
        self.facts_table.itemClicked.connect(self.fact_table_select)
        self.fact_base_update_combo.currentTextAtomd.connect(self.fact_pick_combo_load)
        self.fact_update_button.clicked.connect(self.fact_set_action)
        self.fact_delete_button.clicked.connect(self.fact_del_action)

        self.x_agenda = None

    def fact_set_action(self):
        self.x_agenda.set_fact(
            base=self.fact_base_update_combo.currentText(),
            pick=self.fact_pick_update_combo.currentText(),
            open=pyqt_func_str2float(self.fact_open.text()),
            nigh=pyqt_func_str2float(self.fact_nigh.text()),
        )
        self.refresh_all()

    def fact_del_action(self):
        self.x_agenda.del_fact(base=self.fact_base_update_combo.currentText())
        self.refresh_all()

    def get_facts_list(self):
        return self.x_agenda._idearoot._factunits.values()

    def facts_table_load(self):
        self.facts_table.setRowCount(0)

        row = 0
        for fact in self.get_facts_list():
            base_text = fact.base.replace(f"{self.x_agenda._owner_id}", "")
            base_text = base_text[1:]
            fact_text = fact.pick.replace(fact.base, "")
            fact_text = fact_text[1:]
            if fact.open is None:
                fact_text = f"{fact_text}"
            elif base_text == "time,jajatime":
                fact_text = f"{self.x_agenda.get_jajatime_legible_one_time_event(fact.open)}-{self.x_agenda.get_jajatime_repeating_legible_text(fact.nigh)}"
            else:
                fact_text = f"{fact_text} Open-Nigh {fact.open}-{fact.nigh}"

            self._facts_table_set_row_and_2_columns(row, base_text, fact_text)
            self.facts_table.setItem(row, 2, qtw1(fact.base))
            self.facts_table.setItem(row, 3, qtw1(fact.pick))
            self.facts_table.setItem(row, 4, qtw1(pyqt_func_num2str(fact.open)))
            self.facts_table.setItem(row, 5, qtw1(pyqt_func_num2str(fact.nigh)))
            row += 1

        for base, count in self.x_agenda.get_missing_fact_bases().items():
            base_text = base.replace(f"{self.x_agenda._owner_id}", "")
            base_text = base_text[1:]

            base_lecture_text = f"{base_text} ({count} nodes)"
            self._facts_table_set_row_and_2_columns(row, base_lecture_text, "")
            self.facts_table.setItem(row, 2, qtw1(base))
            self.facts_table.setItem(row, 3, qtw1(""))
            self.facts_table.setItem(row, 4, qtw1(""))
            self.facts_table.setItem(row, 5, qtw1(""))
            row += 1
        self.fact_clear_fields()

    def _facts_table_set_row_and_2_columns(self, row, base_text, fact_text):
        self.facts_table.setRowCount(row + 1)
        self.facts_table.setItem(row, 0, qtw1(base_text))
        self.facts_table.setItem(row, 1, qtw1(fact_text))
        self.facts_table.setColumnWidth(0, 140)
        self.facts_table.setColumnWidth(1, 450)

    def fact_clear_fields(self):
        self.fact_base_update_combo.clear()
        self.fact_pick_update_combo.clear()
        self.fact_open.clear()
        self.fact_nigh.clear()

    def fact_table_select(self):
        self.fact_base_update_combo.clear()
        self.fact_base_update_combo.addItems(
            self.x_agenda.get_idea_tree_ordered_road_list()
        )
        self.fact_base_update_combo.setCurrentText(
            self.facts_table.item(self.facts_table.currentRow(), 2).text()
        )

        self.fact_pick_combo_load()
        self.fact_pick_update_combo.setCurrentText(
            self.facts_table.item(self.facts_table.currentRow(), 3).text()
        )

        self.fact_open.clear()
        self.fact_open.setText(
            pyqt_func_num2str(
                self.facts_table.item(self.facts_table.currentRow(), 4).text()
            )
        )

        self.fact_nigh.clear()
        self.fact_nigh.setText(
            pyqt_func_num2str(
                self.facts_table.item(self.facts_table.currentRow(), 5).text()
            )
        )

    def fact_pick_combo_load(self):
        self.fact_pick_update_combo.clear()
        self.fact_pick_update_combo.addItems(
            self.x_agenda.get_heir_road_list(self.fact_base_update_combo.currentText())
        )

    def fact_update_heir(self, base_road):
        if self.fact_update_combo.currentText() == "":
            raise EditMainViewException("No comboup selection for fact update.")
        if self.facts_table.item(self.facts_table.currentRow(), 2).text() is None:
            raise EditMainViewException("No table selection for fact update.")
        fact_update_combo_text = self.fact_update_combo.currentText()
        self.x_agenda._idearoot._factunits[base_road].fact = fact_update_combo_text
        self.base_road = None
        self.refresh_all

    def refresh_all(self):
        if self.x_agenda != None:
            self.refresh_guy_list()
            self.refresh_idea_tree()
            self.facts_table_load()

    def refresh_guy_list(self):
        # guy_list is qtw.QTableWidget()
        self.guy_list.setObjectName("Guy Calculated Weight")
        self.guy_list.setColumnCount(2)
        self.guy_list.setColumnWidth(0, 170)
        self.guy_list.setColumnWidth(1, 70)
        self.guy_list.setHorizontalHeaderLabels(["PID", "LW Force"])
        guys_list = list(self.x_agenda._guys.values())
        guys_list.sort(key=lambda x: x._agenda_cred, reverse=True)

        for row, guy in enumerate(guys_list, start=1):
            beliefs_count = 0
            for belief in self.x_agenda._beliefs.values():
                for guylink in belief._guys.values():
                    if guylink.guy_id == guy.guy_id:
                        beliefs_count += 1

            qt_agenda_cred = qtw.QTableWidgetItem(
                agenda_importance_diplay(guy._agenda_cred)
            )
            qt_belief = qtw.QTableWidgetItem(f"{beliefs_count}")
            self.guy_list.setRowCount(row)
            self.guy_list.setItem(row - 1, 0, qtw.QTableWidgetItem(guy.guy_id))
            self.guy_list.setItem(row - 1, 1, qt_agenda_cred)

    def open_editideaunit(self):
        self.EditIdeaunit = EditIdeaUnit()
        self.EditIdeaunit.x_agenda = self.x_agenda
        self.EditIdeaunit.refresh_tree()
        self.EditIdeaunit.show()

    def open_edit_guy(self):
        self.edit_guy = EditGuy()
        self.edit_guy.x_agenda = self.x_agenda
        self.edit_guy.refresh_all()
        self.edit_guy.show()

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
