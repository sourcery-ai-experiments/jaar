# command to for converting ui form to python file: pyuic5 ui\EditProblemUI.ui -o ui\EditProblemUI.py
from ui.EditProblemUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtGui as qtg
from PyQt5 import QtCore as qtc
from PyQt5.QtWidgets import QTableWidgetItem as qti
from EditIdeaUnit import EditIdeaUnit
from EditMember import EditMember
from src.pyqt5_kit.pyqt_func import lw_diplay, get_pyqttree, num2str
from src.agent.group import groupunit_shop, grouplink_shop
from src.agent.idea import IdeaKid
from src.agent.road import Road, get_walk_from_road, get_terminus_node_from_road
from sys import exit as sys_exit

# self.problem_name_text
# self.problem_name_combo

# self.problem_context_text
# self.problem_context_combo

# self.group1_name_combo self.group1_weight_text
# self.group2_name_combo self.group2_weight_text
# self.group3_name_combo self.group3_weight_text

# self.action1_combo
# self.action2_combo
# self.action3_combo
# self.action1_text
# self.action2_text
# self.action3_text

# self.agenda_display
# self.add_group_text
# self.add_group_button
# load_problem_button
# refresh_button


class EditProblem(qtw.QWidget, Ui_Form):
    """The settings dialog window"""

    refresh_ideaunit_submitted = qtc.pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys_exit)
        self.refresh_button.clicked.connect(self.refresh_all)
        self.baseideaunit.itemClicked.connect(self.open_editideaunit)
        self.add_group_button.clicked.connect(self.add_group)
        self.load_problem_button.clicked.connect(self.load_problem)

        self.problem_name_combo.currentTextChanged.connect(
            self.select_problem_name_combo
        )
        self.problem_context_combo.currentTextChanged.connect(
            self.select_problem_context_combo
        )
        self.action1_combo.currentTextChanged.connect(self.select_action1_combo)
        self.action2_combo.currentTextChanged.connect(self.select_action2_combo)
        self.action3_combo.currentTextChanged.connect(self.select_action3_combo)

        self.agenda_table.itemClicked.connect(self.select_agenda_item)
        self.agenda_table.setObjectName("Current Agenda")
        self.agenda_table.setRowCount(0)

        self.agent_x = None

    def select_problem_name_combo(self):
        self.problem_name_text.setText(self.problem_name_combo.currentText())

    def select_problem_context_combo(self):
        self.problem_context_text.setText(self.problem_context_combo.currentText())

    def select_action1_combo(self):
        self.action1_text.setText(self.action1_combo.currentText())

    def select_action2_combo(self):
        self.action2_text.setText(self.action2_combo.currentText())

    def select_action3_combo(self):
        self.action3_text.setText(self.action3_combo.currentText())

    def create_grouplinks_list(self):
        grouplinks_x_list = []
        if self.group1_name_combo.currentText() != "":
            weight1 = 1
            if self.group1_weight_text.text() != "":
                weight1 = float(self.group1_weight_text.text())
            grouplinks_x_list.append(
                grouplink_shop(
                    name=self.group1_name_combo.currentText(), weight=weight1
                )
            )
        if self.group2_name_combo.currentText() != "":
            weight2 = 1
            if self.group2_weight_text.text() != "":
                weight2 = float(self.group2_weight_text.text())

            grouplinks_x_list.append(
                grouplink_shop(
                    name=self.group2_name_combo.currentText(), weight=weight2
                )
            )
        if self.group3_name_combo.currentText() != "":
            weight3 = 1
            if self.group3_weight_text.text() != "":
                weight3 = float(self.group3_weight_text.text())
            grouplinks_x_list.append(
                grouplink_shop(
                    name=self.group3_name_combo.currentText(), weight=weight3
                )
            )
        return grouplinks_x_list

    def load_problem(self):
        self.set_problem_dominate_action_idea(road=self.problem_name_text.text())
        self.set_problem_dominate_action_idea(road=self.action1_text.text())
        self.set_problem_dominate_action_idea(road=self.action2_text.text())
        self.set_problem_dominate_action_idea(road=self.action3_text.text())
        self.refresh_all()

    def set_problem_dominate_action_idea(self, road):
        if road != "":
            prob_walk = get_walk_from_road(road)
            prob_desc = get_terminus_node_from_road(road)
            prob_idea = IdeaKid(_desc=prob_desc, _walk=prob_walk)
            for grouplink_x in self.create_grouplinks_list():
                prob_idea.set_grouplink(grouplink_x)
            self.agent_x.set_dominate_promise_idea(idea_kid=prob_idea)

    def add_group(self):
        if self.add_group_text not in (None, ""):
            self.agent_x.set_groupunit(groupunit_shop(name=self.add_group_text.text()))
        self.refresh_all()

    def refresh_all(self):
        self.problem_name_text.setText("")
        self.problem_context_text.setText("")
        self.group1_weight_text.setText("")
        self.group2_weight_text.setText("")
        self.group3_weight_text.setText("")
        self.action1_text.setText("")
        self.action2_text.setText("")
        self.action3_text.setText("")
        self.add_group_text.setText("")

        if self.agent_x != None:
            self.refresh_agenda_list()
            self.refresh_idea_tree()

            idea_road_list = self.agent_x.get_idea_tree_ordered_road_list()
            idea_road_list.insert(0, "")

            self.problem_name_combo.clear()
            self.problem_name_combo.addItems(idea_road_list)
            self.problem_context_combo.clear()
            self.problem_context_combo.addItems(idea_road_list)
            self.group1_name_combo.clear()
            self.group2_name_combo.clear()
            self.group3_name_combo.clear()
            self.group1_name_combo.addItems(self.agent_x.get_groupunits_name_list())
            self.group2_name_combo.addItems(self.agent_x.get_groupunits_name_list())
            self.group3_name_combo.addItems(self.agent_x.get_groupunits_name_list())
            self.action1_combo.clear()
            self.action2_combo.clear()
            self.action3_combo.clear()
            self.action1_combo.addItems(idea_road_list)
            self.action2_combo.addItems(idea_road_list)
            self.action3_combo.addItems(idea_road_list)

    def select_agenda_item(self):
        pass

    def refresh_agenda_list(self):
        self.agenda_table.clear()
        self.agenda_table.setRowCount(0)
        self.set_agenda_table_gui_attr()
        # base_x = self.acptfact_base_update_combo.currentText()
        # base_x = ""
        # if base_x == "":
        #     base_x = None
        base_x = None

        agenda_list = self.agent_x.get_agenda_items(
            agenda_todo=True, agenda_state=True, base=base_x
        )
        agenda_list.sort(key=lambda x: x._agent_importance, reverse=True)

        row = 0
        for agenda_item in agenda_list:
            if agenda_item._task == True:
                self.populate_agenda_table_row(
                    row=row, agenda_item=agenda_item, base=base_x
                )
                row += 1

    def populate_agenda_table_row(self, row, agenda_item, base):
        a = agenda_item
        requiredheir_x = a.get_requiredheir(base=base)
        sufffact_open_x = None
        sufffact_nigh_x = None
        sufffact_divisor_x = None
        lw_display_x = lw_diplay(agent_importance=a._agent_importance)

        if requiredheir_x != None:
            for sufffact in requiredheir_x.sufffacts.values():
                if sufffact._task == True:
                    sufffact_open_x = sufffact.open
                    sufffact_nigh_x = sufffact.nigh
                    sufffact_divisor_x = sufffact.divisor

        self.agenda_table.setRowCount(row + 1)
        self.agenda_table.setItem(row, 0, qti(a._desc))
        self.agenda_table.setItem(row, 1, qti(a._walk))
        self.agenda_table.setItem(row, 2, qti(lw_display_x))
        self.agenda_table.setItem(row, 3, qti(num2str(a._weight)))
        self.agenda_table.setItem(row, 4, qti(base))
        self.agenda_table.setItem(row, 5, qti(num2str(sufffact_open_x)))
        self.agenda_table.setItem(row, 6, qti(num2str(sufffact_nigh_x)))
        self.agenda_table.setItem(row, 7, qti(num2str(sufffact_divisor_x)))
        # if a._task in (True, False):
        #     self.agenda_table.setItem(row, 7, qti(f"task {a._task}"))
        # else:
        #     self.agenda_table.setItem(row, 7, qti("bool not set"))
        self.agenda_table.setRowHeight(row, 5)

    def set_agenda_table_gui_attr(self):
        self.agenda_table.setColumnWidth(0, 300)
        self.agenda_table.setColumnWidth(1, 400)
        self.agenda_table.setColumnWidth(2, 55)
        self.agenda_table.setColumnWidth(3, 55)
        self.agenda_table.setColumnWidth(4, 150)
        self.agenda_table.setColumnWidth(5, 70)
        self.agenda_table.setColumnWidth(6, 70)
        self.agenda_table.setColumnWidth(7, 70)
        self.agenda_table.setColumnHidden(0, False)
        self.agenda_table.setColumnHidden(1, False)
        self.agenda_table.setColumnHidden(2, False)
        self.agenda_table.setColumnHidden(3, True)
        self.agenda_table.setColumnHidden(4, False)
        self.agenda_table.setColumnHidden(5, False)
        self.agenda_table.setColumnHidden(6, False)
        self.agenda_table.setColumnHidden(7, False)
        self.agenda_table.setHorizontalHeaderLabels(
            [
                "_desc",
                "road",
                "agent_importance",
                "weight",
                "acptfact",
                "open",
                "nigh",
                "divisor",
            ]
        )

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
