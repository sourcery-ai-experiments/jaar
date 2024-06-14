# command to for converting ui form to python file: pyuic5 ui\EditFactUnitUI.ui -o ui\EditFactUnitUI.py
import sys
from src.agenda.fact import factunit_shop, factattrfilter_shop
from ui.EditFactUnitUI import Ui_Form
from PyQt5 import QtWidgets as qtw, QtCore
from PyQt5.QtWidgets import QTableWidgetItem as qtw1, QTableWidget as qtw0
from src._road.road import create_road
from src.agenda.hreg_time import PremiseUnitHregTime
from src.agenda.idea import BalanceLink, IdeaID
from src.agenda.reason_fact import RoadUnit
from src.agenda.hreg_time import HregTimeFactSource  # get_24hr, get_60min
from ui.pyqt_func import (
    num2str,
    bool_val,
    str2float,
    get_pyqttree,
    emptystr,
    agenda_importance_diplay,
    emptystring_returns_none,
)


class PyQtUIException(Exception):
    pass


class EditFactUnit(qtw0, Ui_Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.refresh_button.clicked.connect(self.refresh_tree)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)

        self.basefactunit.itemClicked.connect(self.yo_tree_item_selected)
        self.basefactunit.itemActivated.connect(self.yo_tree_item_expanded)
        self.submit_node_update.clicked.connect(self.fact_update)
        self.submit_node_delete.clicked.connect(self.fact_delete)
        self.submit_child_insert.clicked.connect(self.fact_insert)
        self.submit_pledge_insert.clicked.connect(self.fact_pledge_insert)

        self.cb_rootadmiration.stateAtomd.connect(self.refresh_tree)
        self.cb_yo_id.stateAtomd.connect(self.refresh_tree)
        self.cb_yo_intent.stateAtomd.connect(self.refresh_tree)
        self.cb_yo_action.stateAtomd.connect(self.refresh_tree)
        self.cb_yo_complete.stateAtomd.connect(self.refresh_tree)
        self.cb_yo_beliefunit_time.stateAtomd.connect(self.refresh_tree)
        self.cb_yo_beliefunit_count.stateAtomd.connect(self.refresh_tree)
        self.cb_yo_beliefheir_count.stateAtomd.connect(self.refresh_tree)
        self.cb_reasonheir_count.stateAtomd.connect(self.refresh_tree)
        self.cb_reason_count.stateAtomd.connect(self.refresh_tree)
        self.cb_reason_view.stateAtomd.connect(self.refresh_tree)
        self.cb_beliefheir_view.stateAtomd.connect(self.refresh_tree)
        self.cb_yo2bd_count.stateAtomd.connect(self.refresh_tree)
        self.combo_dim_root.currentTextAtomd.connect(self.refresh_tree)

        self.fact2idea_table.itemClicked.connect(self.fact2idea_table_select)
        self.fact2idea_delete_button.clicked.connect(self.fact2idea_delete)
        self.fact2idea_insert_button.clicked.connect(self.fact2idea_update)
        self.reason_table.itemClicked.connect(self.reason_table_select)
        self.reason_base_combo.currentTextAtomd.connect(self.reason_premise_combo_load)
        self.reason_premise_combo.currentTextAtomd.connect(
            self.reason_premise_xxxx_combo_load
        )
        self.reason_premise_open_combo.currentTextAtomd.connect(
            self.reason_premise_open_combo_select
        )
        self.reason_premise_nigh_combo.currentTextAtomd.connect(
            self.reason_premise_nigh_combo_select
        )
        self.reason_premise_divisor_combo.currentTextAtomd.connect(
            self.reason_premise_divisor_combo_select
        )
        self.button_reason_upsert.clicked.connect(self.reason_upsert)
        self.button_reason_delete.clicked.connect(self.reason_delete)
        self.button_premiseunit_hreg_update_days.clicked.connect(
            self.premiseunit_hreg_update_days
        )
        self.button_premiseunit_hreg_update_weeks.clicked.connect(
            self.premiseunit_hreg_update_weeks
        )
        self.button_hreg_base.clicked.connect(self.set_base_to_hregtime)
        self.create_hreg_button.clicked.connect(self.add_hreg_to_agenda)
        self.button_view_reasonheirs.clicked.connect(self.toogle_reasonheir_tables)
        self.reasonheir_table_hidden = True

        self.yo_tree_item_setHidden(setHiddenBool=True)
        self.show
        self.x_fact = None

    def toogle_reasonheir_tables(self):
        self.reasonheir_table_hidden = self.reasonheir_table_hidden is False
        self.reasonheir_table.setHidden(self.reasonheir_table_hidden)

    def set_base_to_hregtime(self):
        self.reason_base_combo.setCurrentText(f"{self.x_agenda._real_id},time,jajatime")

    def add_hreg_to_agenda(self):
        self.x_agenda.set_time_hreg_facts(c400_count=7)
        self.refresh_tree()

    def yo_tree_item_setHidden(self, setHiddenBool):
        if type(setHiddenBool) is not bool:
            raise PyQtUIException("input varible is not boolen")

        self.label_parent_id.setHidden(setHiddenBool)
        self.button_hreg_instance.setHidden(setHiddenBool)
        self.button_hreg_1hour.setHidden(setHiddenBool)
        self.button_hreg_all_day.setHidden(setHiddenBool)
        self.cb_yo_insert_allChildren.setHidden(setHiddenBool)
        self.label_1.setHidden(setHiddenBool)
        self.label_4.setHidden(setHiddenBool)
        self.label_10.setHidden(setHiddenBool)
        self.label_11.setHidden(setHiddenBool)
        self.label_12.setHidden(setHiddenBool)
        self.label_14.setHidden(setHiddenBool)
        self.label_18.setHidden(setHiddenBool)
        self.label_19.setHidden(setHiddenBool)
        self.label_20.setHidden(setHiddenBool)
        self.label_21.setHidden(setHiddenBool)
        self.label_22.setHidden(setHiddenBool)
        self.label_23.setHidden(setHiddenBool)
        self.label_24.setHidden(setHiddenBool)
        self.prom_l_02.setHidden(setHiddenBool)
        self.prom_l_03.setHidden(setHiddenBool)
        self.yo_action_cb.setHidden(setHiddenBool)
        self.yo_deescription.setHidden(setHiddenBool)
        self.yo_parent_road.setHidden(setHiddenBool)
        self.yo_weight.setHidden(setHiddenBool)
        self.yo_begin.setHidden(setHiddenBool)
        self.yo_addin.setHidden(setHiddenBool)
        self.yo_numor.setHidden(setHiddenBool)
        self.yo_denom.setHidden(setHiddenBool)
        self.yo_reest.setHidden(setHiddenBool)
        self.yo_range_source_road.setHidden(setHiddenBool)
        self.yo_numeric_road.setHidden(setHiddenBool)
        self.yo_close.setHidden(setHiddenBool)
        self.yo_task_status.setHidden(setHiddenBool)
        self.yo_active.setHidden(setHiddenBool)
        self.hreg_open_hr.setHidden(setHiddenBool)
        self.hreg_open_min.setHidden(setHiddenBool)
        self.hreg_length_hr.setHidden(setHiddenBool)
        self.hreg_length_min.setHidden(setHiddenBool)
        self.submit_child_insert.setHidden(setHiddenBool)
        self.fact2idea_table.setHidden(setHiddenBool)
        self.fact2idea_table.clear()
        self.fact2idea_table.setRowCount(1)
        self.fact2idea_insert_combo.setHidden(setHiddenBool)
        self.fact2idea_delete_button.setHidden(setHiddenBool)
        self.fact2idea_insert_button.setHidden(setHiddenBool)
        self.reasonheir_table.setHidden(True)
        self.reason_table.setHidden(setHiddenBool)
        self.reason_base_combo.setHidden(setHiddenBool)
        self.reason_premise_combo.setHidden(setHiddenBool)
        self.reason_premise_open_combo.setHidden(setHiddenBool)
        self.reason_premise_nigh_combo.setHidden(setHiddenBool)
        self.reason_premise_divisor_combo.setHidden(setHiddenBool)
        self.reason_premise_open.setHidden(setHiddenBool)
        self.reason_premise_nigh.setHidden(setHiddenBool)
        self.reason_premise_divisor.setHidden(setHiddenBool)
        self.label_9.setHidden(setHiddenBool)
        self.label_15.setHidden(setHiddenBool)
        self.label_16.setHidden(setHiddenBool)
        self.label_17.setHidden(setHiddenBool)
        self.button_reason_upsert.setHidden(setHiddenBool)
        self.button_premiseunit_hreg_update_days.setHidden(setHiddenBool)
        self.button_premiseunit_hreg_update_weeks.setHidden(setHiddenBool)
        self.button_reason_delete.setHidden(setHiddenBool)
        self.button_hreg_base.setHidden(setHiddenBool)
        self.submit_child_insert.setHidden(setHiddenBool)
        self.submit_node_update.setHidden(setHiddenBool)
        self.submit_node_delete.setHidden(setHiddenBool)
        hregfact = HregTimeFactSource(",")
        self.hreg_open_hr.clear()
        self.hreg_open_hr.addItems(hregfact.get_24hr())
        self.hreg_open_hr.setCurrentText("")
        self.hreg_open_min.clear()
        self.hreg_open_min.addItems(hregfact.get_60min())
        self.hreg_open_min.setCurrentText("")
        self.hreg_length_hr.clear()
        self.hreg_length_hr.addItems(hregfact.get_24hr())
        self.hreg_length_hr.setCurrentText("")
        self.hreg_length_min.clear()
        self.hreg_length_min.addItems(hregfact.get_60min())
        self.hreg_length_min.setCurrentText("")
        self.hreg_weekday.clear()
        self.hreg_weekday.addItems(
            [
                "",
                "Sunday",
                "Monday",
                "Tuesday",
                "Wednesday",
                "Thursday",
                "Friday",
                "Saturday",
            ]
        )
        self.hreg_weeks_repeat.setText("")
        self.hreg_weeks_remainder.setText("")
        self.label_parent_id.setText("Current Node ID : ")
        self.prom_l_02.setText("")
        self.yo_action_cb.setChecked(False)
        self.yo_deescription.setText("")
        self.fact_label_on_populate = ""
        self.yo_weight.setText("")
        # self.reason_base_combo.setText("")
        # self.reason_premise_combo.setText("")
        self.reason_premise_open.setText("")
        self.reason_premise_nigh.setText("")
        self.reason_premise_divisor.setText("")

        self.reason_table.setRowCount(0)
        self.reason_base_combo.clear()
        self.reason_premise_combo.clear()
        self.reason_premise_open_combo.clear()
        self.reason_premise_nigh_combo.clear()
        self.reason_premise_divisor_combo.clear()
        self.fact2idea_insert_combo.clear()

        if setHiddenBool is False:
            self.x_fact_populate()

    def x_fact_populate(self):
        self.label_parent_id.setText(f"Current Node road : {self.x_fact._parent_road}")
        self.yo_deescription.setText(self.x_fact._label)
        # self.fact_label_on_populate = self.x_fact._label
        self.yo_parent_road.setText(self.x_fact._parent_road)
        self.yo_weight.setText(num2str(self.x_fact._weight))
        self.yo_begin.setText(num2str(self.x_fact._begin))
        self.yo_range_source_road.clear()
        self.yo_numeric_road.clear()
        if f"{type(self.x_fact)}" != "<class 'lw.agenda.AgendaUnit'>":
            self.populate_fact_kid_actions()
        self.yo_close.setText(num2str(self.x_fact._close))
        self.yo_action_cb.setChecked(self.x_fact.pledge)
        self.yo_task_status.setText(str(self.x_fact._task))
        self.yo_active.setText(str(self.x_fact._active))
        self.submit_child_insert.setText(f"Add child {self.x_fact._label:8}")
        self.reason_table_load()
        self.reasonheir_table_load()
        self.reason_base_combo_load()
        self.fact2idea_table_load()
        self.fact2idea_insert_combo_load()
        if self.combo_dim_root.currentText() == "":
            self.combo_dim_root.addItems(list(self.x_agenda.get_reason_bases()))

    def populate_fact_kid_actions(self):
        self.yo_addin.setText(num2str(self.x_fact._addin))
        self.yo_numor.setText(num2str(self.x_fact._numor))
        self.yo_denom.setText(num2str(self.x_fact._denom))
        self.yo_reest.setChecked(bool_val(self.x_fact._reest))
        fact_road_list = self.x_agenda.get_fact_tree_ordered_road_list()
        fact_road_list.append("")
        self.yo_range_source_road.addItems(fact_road_list)
        self.yo_range_source_road.setCurrentText(self.x_fact._range_source_road)
        self.yo_numeric_road.addItems(fact_road_list)
        self.yo_numeric_road.setCurrentText(self.x_fact._numeric_road)

    def yo_tree_item_selected(self):
        fact_label = self.basefactunit.currentItem().data(2, 10)
        fact_parent_road = self.basefactunit.currentItem().data(2, 11)
        if fact_parent_road not in ("", None):
            self.x_fact = self.x_agenda.get_fact_obj(
                road=create_road(fact_parent_road, fact_label)
            )
        else:
            self.x_fact = self.x_agenda._factroot
        self.yo_tree_item_setHidden(setHiddenBool=False)

    def yo_tree_item_expanded(self):
        root = self.basefactunit.invisibleRootItem()
        self.fact_tree_set_is_expanded(root)

    def reason_base_combo_load(self):
        # create list of all fact roads (road+_label)
        self.reason_base_combo.clear()
        self.reason_base_combo.addItems([""])
        self.reason_base_combo.addItems(self.x_agenda.get_fact_tree_ordered_road_list())

    def reason_premise_combo_load(self):
        self.reason_premise_combo.clear()
        self.reason_premise_combo.addItems([""])
        self.reason_premise_combo.addItems(
            self.x_agenda.get_heir_road_list(self.reason_base_combo.currentText())
        )

    def reason_premise_xxxx_combo_load(self):
        filtered_list = []
        if self.reason_premise_combo.currentText() not in [
            self.x_agenda._owner_id,
            "",
        ]:
            premise_fact = self.x_agenda.get_fact_obj(
                road=self.reason_premise_combo.currentText()
            )
            if premise_fact._range_source_road != None:
                filtered_list = self.x_agenda.get_heir_road_list(
                    premise_fact._range_source_road
                )
        self.reason_premise_open_combo.clear()
        self.reason_premise_nigh_combo.clear()
        self.reason_premise_divisor_combo.clear()
        self.reason_premise_open_combo.addItems(filtered_list)
        self.reason_premise_nigh_combo.addItems(filtered_list)
        self.reason_premise_divisor_combo.addItems(filtered_list)
        self.set_premise_open_combo()
        self.set_premise_nigh_combo()
        self.set_premise_divisor_combo()

    def reason_premise_open_combo_select(self):
        self.reason_premise_open.setText("")
        self.reason_premise_nigh.setText("")
        self.reason_premise_divisor.setText("")

        if self.reason_premise_open_combo.currentText() not in [
            self.x_agenda._owner_id,
            "",
        ]:
            self.reason_premise_open_combo_sel_actions()

    def reason_premise_open_combo_sel_actions(self):
        open_fact_x = self.x_agenda.get_fact_obj(
            road=self.reason_premise_open_combo.currentText()
        )
        if open_fact_x._begin != None:
            self.reason_premise_open.setText(str(open_fact_x._begin))
        if open_fact_x._close != None:
            self.reason_premise_nigh.setText(str(open_fact_x._close))
        if open_fact_x._addin != None:
            self.reason_premise_divisor.setText(str(open_fact_x._addin))
        if open_fact_x._numor != None:
            self.reason_premise_divisor.setText(str(open_fact_x._numor))
        if open_fact_x._denom != None:
            self.reason_premise_divisor.setText(str(open_fact_x._denom))
        if open_fact_x._reest != None:
            self.reason_premise_divisor.setText(str(open_fact_x._reest))

    def numeric_road_combo_select(self):
        if self.reason_premise_open_combo.currentText() not in [
            self.x_agenda._owner_id,
            "",
        ]:
            open_fact_x = self.x_agenda.get_fact_obj(
                road=self.reason_premise_open_combo.currentText()
            )
            # nigh_fact_x = self.x_agenda.get_fact_obj(
            #     road=self.reason_premise_nigh_combo.currentText()
            # )
            # divisor_fact_x = self.x_agenda.get_fact_obj(
            #     road=self.reason_premise_divisor_combo.currentText()
            # )
            # if open_fact_x._begin != None:
            #     self.reason_premise_open.setText(str(open_fact_x._begin))
            # if open_fact_x._close != None:
            #     self.reason_premise_nigh.setText(str(open_fact_x._close))

    def set_premise_open_combo(self):
        if (
            self.reason_premise_open_combo.currentText()
            not in [
                self.x_agenda._owner_id,
                "",
            ]
            and self.reason_premise_open.toPlainText() != ""
        ):
            open_fact_x = self.x_agenda.get_fact_obj(
                road=self.reason_premise_open_combo.currentText()
            )
            open_int = str2float(self.reason_premise_open.toPlainText())
            open_kids = open_fact_x.get_kids_in_range(begin=open_int, close=open_int)
            if len(open_kids) == 1:
                fact_x = open_kids[0]
                self.reason_premise_open_combo.setCurrentText(
                    f"{fact_x._parent_road},{fact_x._label}"
                )

    def set_premise_nigh_combo(self):
        if (
            self.reason_premise_nigh_combo.currentText()
            not in [
                self.x_agenda._owner_id,
                "",
            ]
            and self.reason_premise_nigh.toPlainText() != ""
        ):
            nigh_fact_x = self.x_agenda.get_fact_obj(
                road=self.reason_premise_nigh_combo.currentText()
            )
            nigh_int = int(self.reason_premise_nigh.toPlainText())
            nigh_kids = nigh_fact_x.get_kids_in_range(begin=nigh_int, close=nigh_int)
            if len(nigh_kids) == 1:
                fact_x = nigh_kids[0]
                self.reason_premise_nigh_combo.setCurrentText(
                    f"{fact_x._parent_road},{fact_x._label}"
                )

    def set_premise_divisor_combo(self):
        if (
            self.reason_premise_divisor_combo.currentText()
            not in [
                self.x_agenda._owner_id,
                "",
            ]
            and self.reason_premise_divisor.toPlainText() != ""
        ):
            divisor_fact_x = self.x_agenda.get_fact_obj(
                road=self.reason_premise_divisor_combo.currentText()
            )
            divisor_int = int(self.reason_premise_divisor.toPlainText())
            divisor_kids = divisor_fact_x.get_kids_in_range(
                begin=divisor_int, close=divisor_int
            )
            if len(divisor_kids) == 1:
                fact_x = divisor_kids[0]
                self.reason_premise_divisor_combo.setCurrentText(
                    f"{fact_x._parent_road},{fact_x._label}"
                )

    def reason_premise_nigh_combo_select(self):
        self.reason_premise_nigh.setText("")
        if self.reason_premise_nigh_combo.currentText() not in [
            self.x_agenda._owner_id,
            "",
        ]:
            nigh_fact_x = self.x_agenda.get_fact_obj(
                road=self.reason_premise_nigh_combo.currentText()
            )
            if nigh_fact_x._close != None:
                self.reason_premise_nigh.setText(str(nigh_fact_x._close))

    def reason_premise_divisor_combo_select(self):
        self.reason_premise_divisor.setText("")
        if self.reason_premise_divisor_combo.currentText() not in [
            self.x_agenda._owner_id,
            "",
        ]:
            divisor_fact_x = self.x_agenda.get_fact_obj(
                road=self.reason_premise_divisor_combo.currentText()
            )
            if divisor_fact_x._denom != None:
                self.reason_premise_divisor.setText(str(divisor_fact_x._denom))

    def reason_table_load(self):
        self.reason_table.clear()
        row = 0
        for reason in self.x_fact._reasonunits.values():
            reasonheir = self.x_fact._reasonheirs.get(reason.base)
            for premise in reason.premises.values():
                reason_text = reason.base.replace(f"{self.x_agenda._owner_id}", "")
                reason_text = reason_text[1:]
                premise_text = premise.need.replace(reason.base, "")
                premise_text = premise_text[1:]
                premise_open = premise.open
                premise_nigh = premise.nigh
                if reason_text == "time,jajatime":
                    premise_open = self.x_agenda.get_jajatime_repeating_legible_text(
                        open=premise.open,
                        nigh=premise.nigh,
                        divisor=premise.divisor,
                    )
                    premise_nigh = ""
                    premise_text = f"{premise_open}"

                elif premise.divisor != None:
                    premise_text = f"{premise_text}  Open-Nigh {premise_open}-{premise.nigh} Divisor {premise.divisor}"
                elif premise.open != None:
                    premise_text = (
                        f"{premise_text}  Open-Nigh {premise.open}-{premise.nigh}"
                    )
                else:
                    premise_text = f"{premise_text}"

                self.reason_table.setRowCount(row + 1)
                self.reason_table.setItem(row, 0, qtw1(reason_text))
                self.reason_table.setItem(row, 1, qtw1(premise_text))
                self.reason_table.setItem(row, 2, qtw1(reason.base))
                self.reason_table.setItem(row, 3, qtw1(premise.need))
                self.reason_table.setItem(row, 4, qtw1(num2str(premise.open)))
                self.reason_table.setItem(row, 5, qtw1(num2str(premise.nigh)))
                self.reason_table.setItem(row, 6, qtw1(num2str(premise.divisor)))
                self.reason_table.setItem(row, 7, qtw1(f"{reasonheir._task}"))
                self.reason_table.setItem(row, 8, qtw1(f"{reasonheir._status}"))
                self.reason_table.setItem(row, 9, qtw1(str(premise._status)))
                self.reason_table.setItem(row, 10, qtw1(str(premise._task)))
                row += 1

        self.reason_table.horizontalHeaderVisible = False
        self.reason_table.verticalHeaderVisible = False
        self.reason_table.setColumnWidth(0, 300)
        self.reason_table.setColumnWidth(1, 400)
        self.reason_table.setColumnWidth(2, 30)
        self.reason_table.setColumnWidth(3, 30)
        self.reason_table.setColumnWidth(4, 30)
        self.reason_table.setColumnWidth(5, 30)
        self.reason_table.setColumnWidth(6, 60)
        self.reason_table.setColumnWidth(7, 60)
        self.reason_table.setColumnWidth(8, 60)
        self.reason_table.setColumnWidth(9, 60)
        self.reason_table.setColumnWidth(10, 60)
        self.reason_table.setColumnHidden(0, False)
        self.reason_table.setColumnHidden(1, False)
        self.reason_table.setColumnHidden(2, True)
        self.reason_table.setColumnHidden(3, True)
        self.reason_table.setColumnHidden(4, True)
        self.reason_table.setColumnHidden(5, True)
        self.reason_table.setColumnHidden(6, False)
        self.reason_table.setColumnHidden(7, False)
        self.reason_table.setColumnHidden(8, False)
        self.reason_table.setColumnHidden(9, False)
        self.reason_table.setColumnHidden(10, False)
        self.reason_table.setHorizontalHeaderLabels(
            [
                "Reason",
                "Premise",
                "Base",
                "Need",
                "Open",
                "Nigh",
                "Divisor",
                "LimTask",
                "LimStatus",
                "Premise active",
                "Premise task_status",
            ]
        )

    def reasonheir_table_load(self):
        self.reasonheir_table.clear()
        row = 0
        for reasonheir in self.x_fact._reasonheirs.values():
            for premise in reasonheir.premises.values():
                reasonheir_text = reasonheir.base.replace(
                    f"{self.x_agenda._owner_id}", ""
                )
                reasonheir_text = reasonheir_text[1:]
                premise_text = premise.need.replace(reasonheir.base, "")
                premise_text = premise_text[1:]
                premise_open = premise.open
                premise_nigh = premise.nigh
                if reasonheir_text == "time,jajatime":
                    premise_open = self.x_agenda.get_jajatime_repeating_legible_text(
                        open=premise.open,
                        nigh=premise.nigh,
                        divisor=premise.divisor,
                    )
                    premise_nigh = ""
                    premise_text = f"{premise_open}"

                elif premise.divisor != None:
                    premise_text = f"{premise_text}  Open-Nigh {premise_open}-{premise.nigh} Divisor {premise.divisor}"
                elif premise.open != None:
                    premise_text = (
                        f"{premise_text}  Open-Nigh {premise.open}-{premise.nigh}"
                    )
                else:
                    premise_text = f"{premise_text}"

                premise_text += f"{type(reasonheir)}"

                self.reasonheir_table.setRowCount(row + 1)
                self.reasonheir_table.setItem(row, 0, qtw1(reasonheir_text))
                self.reasonheir_table.setItem(row, 1, qtw1(premise_text))
                self.reasonheir_table.setItem(row, 2, qtw1(reasonheir.base))
                self.reasonheir_table.setItem(row, 3, qtw1(premise.need))
                self.reasonheir_table.setItem(row, 4, qtw1(num2str(premise.open)))
                self.reasonheir_table.setItem(row, 5, qtw1(num2str(premise.nigh)))
                self.reasonheir_table.setItem(row, 6, qtw1(num2str(premise.divisor)))
                self.reasonheir_table.setItem(row, 7, qtw1(f"{reasonheir._task}"))
                self.reasonheir_table.setItem(row, 8, qtw1(f"{reasonheir._status}"))
                self.reasonheir_table.setItem(row, 9, qtw1(str(premise._status)))
                self.reasonheir_table.setItem(row, 10, qtw1(str(premise._task)))
                row += 1

        self.reasonheir_table.horizontalHeaderVisible = False
        self.reasonheir_table.verticalHeaderVisible = False
        self.reasonheir_table.setColumnWidth(0, 300)
        self.reasonheir_table.setColumnWidth(1, 400)
        self.reasonheir_table.setColumnWidth(2, 30)
        self.reasonheir_table.setColumnWidth(3, 30)
        self.reasonheir_table.setColumnWidth(4, 30)
        self.reasonheir_table.setColumnWidth(5, 30)
        self.reasonheir_table.setColumnWidth(6, 60)
        self.reasonheir_table.setColumnWidth(7, 60)
        self.reasonheir_table.setColumnWidth(8, 60)
        self.reasonheir_table.setColumnWidth(9, 60)
        self.reasonheir_table.setColumnWidth(10, 60)
        self.reasonheir_table.setColumnHidden(0, False)
        self.reasonheir_table.setColumnHidden(1, False)
        self.reasonheir_table.setColumnHidden(2, True)
        self.reasonheir_table.setColumnHidden(3, True)
        self.reasonheir_table.setColumnHidden(4, True)
        self.reasonheir_table.setColumnHidden(5, True)
        self.reasonheir_table.setColumnHidden(6, False)
        self.reasonheir_table.setColumnHidden(7, False)
        self.reasonheir_table.setColumnHidden(8, False)
        self.reasonheir_table.setColumnHidden(9, False)
        self.reasonheir_table.setColumnHidden(10, False)
        self.reasonheir_table.setHorizontalHeaderLabels(
            [
                "Reasonheir",
                "Premise",
                "Base",
                "Need",
                "Open",
                "Nigh",
                "Divisor",
                "LimTask",
                "LimStatus",
                "Premise active",
                "Premise task_status",
            ]
        )

    def premiseunit_hreg_update_weeks(self):
        self.hreg_days_repeat.setText("")
        self.hreg_days_remainder.setText("")

        if self.hreg_length_hr.currentText() == "":
            self.hreg_length_hr.setCurrentText("0")
        if self.hreg_length_min.currentText() == "":
            self.hreg_length_min.setCurrentText("0")
        if self.hreg_open_hr.currentText() == "":
            self.hreg_open_hr.setCurrentText("0")
        if self.hreg_open_min.currentText() == "":
            self.hreg_open_min.setCurrentText("0")
        if self.hreg_weekday.currentText() == "":
            self.hreg_weekday.setCurrentText("Saturday")
        if self.hreg_weeks_repeat.toPlainText() == "":
            self.hreg_weeks_repeat.setText("1")
        if self.hreg_weeks_remainder.toPlainText() == "":
            self.hreg_weeks_remainder.setText("0")

        hu = PremiseUnitHregTime()
        event_minutes = (int(self.hreg_length_hr.currentText()) * 60) + int(
            self.hreg_length_min.currentText()
        )
        hu.set_weekly_event(
            every_x_weeks=int(self.hreg_weeks_repeat.toPlainText()),
            remainder_weeks=int(self.hreg_weeks_remainder.toPlainText()),
            weekday=self.hreg_weekday.currentText(),
            start_hr=int(self.hreg_open_hr.currentText()),
            start_minute=int(self.hreg_open_min.currentText()),
            event_minutes=event_minutes,
        )
        self.reason_premise_open.setText(str(hu.jajatime_open))
        self.reason_premise_nigh.setText(str(hu.jajatime_nigh))
        self.reason_premise_divisor.setText(str(hu.jajatime_divisor))

    def premiseunit_hreg_update_days(self):
        self.hreg_weekday.setCurrentText("")
        self.hreg_weeks_repeat.setText("")
        self.hreg_weeks_remainder.setText("")

        if self.hreg_length_hr.currentText() == "":
            self.hreg_length_hr.setCurrentText("0")
        if self.hreg_length_min.currentText() == "":
            self.hreg_length_min.setCurrentText("0")
        if self.hreg_open_hr.currentText() == "":
            self.hreg_open_hr.setCurrentText("0")
        if self.hreg_open_min.currentText() == "":
            self.hreg_open_min.setCurrentText("0")
        if self.hreg_days_repeat.toPlainText() == "":
            self.hreg_days_repeat.setText("1")
        if self.hreg_days_remainder.toPlainText() == "":
            self.hreg_days_remainder.setText("0")

        hu = PremiseUnitHregTime()
        event_minutes = (int(self.hreg_length_hr.currentText()) * 60) + int(
            self.hreg_length_min.currentText()
        )
        hu.set_days_event(
            every_x_days=float(self.hreg_days_repeat.toPlainText()),
            remainder_days=float(self.hreg_days_remainder.toPlainText()),
            start_hr=int(self.hreg_open_hr.currentText()),
            start_minute=int(self.hreg_open_min.currentText()),
            event_minutes=event_minutes,
        )
        self.reason_premise_open.setText(str(hu.jajatime_open))
        self.reason_premise_nigh.setText(str(hu.jajatime_nigh))
        self.reason_premise_divisor.setText(str(hu.jajatime_divisor))

    def reason_upsert(self):
        if (
            self.reason_base_combo.currentText() != ""
            and self.reason_premise_combo.currentText() != ""
        ):
            base_x = self.reason_base_combo.currentText()
            premise_x = self.reason_premise_combo.currentText()
            open_x = str2float(self.reason_premise_open.toPlainText())
            nigh_x = str2float(self.reason_premise_nigh.toPlainText())
            divisor_x = str2float(self.reason_premise_divisor.toPlainText())
            fact_label = self.basefactunit.currentItem().data(2, 10)
            fact_parent_road = self.basefactunit.currentItem().data(2, 11)
            self.x_agenda.edit_fact_attr(
                road=f"{fact_parent_road},{fact_label}",
                reason_base=base_x,
                reason_premise=premise_x,
                reason_premise_open=open_x,
                reason_premise_nigh=nigh_x,
                reason_premise_divisor=divisor_x,
            )

            # self.x_fact.set_reason_premise(
            #     base=base_x,
            #     need=premise_x,
            #     open=open_x,
            #     nigh=nigh_x,
            #     divisor=divisor_x,
            # )
            self.x_agenda.calc_agenda_metrics()
            self.reason_table_load()

    def reason_delete(self):
        if (
            self.reason_base_combo.currentText() != ""
            and self.reason_premise_combo.currentText() != ""
        ):
            self.x_fact.del_reasonunit_premise(
                base=self.reason_base_combo.currentText(),
                need=self.reason_premise_combo.currentText(),
            )
            self.reason_table_load()

    def fact2idea_table_select(self):
        self.fact2idea_delete_button.setText(
            f"""Delete {self.fact2idea_table.item(self.fact2idea_table.currentRow(), 1).text()}"""
        )

    def fact2idea_table_load(self):
        # fact2idea_table is qtw.QTableWidget()
        self.fact2idea_table.clear()
        self.fact2idea_table.sortItems(1, QtCore.Qt.AscendingOrder)
        self.fact2idea_table.horizontalHeaderVisible = False
        self.fact2idea_table.verticalHeaderVisible = False
        self.fact2idea_table.setColumnWidth(0, 150)
        self.fact2idea_table.setColumnHidden(1, True)
        self.fact2idea_table.setColumnWidth(1, 50)
        self.fact2idea_table.setColumnWidth(2, 70)
        self.fact2idea_table.setHorizontalHeaderLabels(
            ["Idea display", "idea_pid", "LW Force"]
        )
        # print(f"{self.x_fact._balancelinks=}")
        # print(f"{self.x_fact._balanceheirs=}")
        balancelinks_list = list(self.x_fact._balancelinks.values())
        balancelinks_list.sort(key=lambda x: x.idea_id, reverse=False)
        balanceheirs_list = list(self.x_fact._balanceheirs.values())
        balanceheirs_list.sort(key=lambda x: x.idea_id, reverse=False)
        # print(f"{balancelinks_list=}")
        # print(f"{balanceheirs_list=}")

        for row, balanceheir in enumerate(balanceheirs_list, start=1):
            self.fact2idea_table.setRowCount(row)
            x_text = f"  Heir: {balanceheir.idea_id}"
            for balancelink in balancelinks_list:
                if balancelink.idea_id == balanceheir.idea_id:
                    x_text = f"{balanceheir.idea_id}"
            self.fact2idea_table.setItem(row - 1, 0, qtw1(x_text))
            self.fact2idea_table.setItem(row - 1, 1, qtw1(balanceheir.idea_id))
            self.fact2idea_table.setItem(
                row - 1,
                2,
                qtw1(agenda_importance_diplay(balanceheir._agenda_cred)),
            )

        self.fact2idea_table.sortItems(1, QtCore.Qt.AscendingOrder)

    def fact2idea_insert_combo_load(self):
        # ideaunits_list = list(self.x_agenda._ideaunits.values())
        ideaunits_pids_list = []
        for ideaunit in self.x_agenda._ideas.values():
            idea_previously_selected = any(
                ideaunit.idea_id == balancelink.idea_id
                for balancelink in self.x_fact._balancelinks.values()
            )
            if not idea_previously_selected:
                ideaunits_pids_list.append(ideaunit.idea_id)
        ideaunits_pids_list.sort(key=lambda x: x.lower(), reverse=False)

        self.fact2idea_insert_combo.clear()
        self.fact2idea_insert_combo.addItems(ideaunits_pids_list)

    def fact2idea_update(self):
        bd_pid_new = self.fact2idea_insert_combo.currentText()
        if bd_pid_new == "":
            raise PyQtUIException("bd_pid is empty, fact2bd cannot be updated")
        balancelink_new = BalanceLink(idea_id=IdeaID(bd_pid_new), weight=1)
        self.x_agenda.edit_fact_attr(
            road=f"{self.x_fact._parent_road},{self.x_fact._label}",
            balancelink=balancelink_new,
        )
        self.fact2idea_insert_combo_load()
        self.fact2idea_table_load()

    def fact2idea_delete(self):
        delete_idea_pid = ""
        if self.fact2idea_table.currentRow() != None:
            delete_idea_pid = self.fact2idea_table.item(
                self.fact2idea_table.currentRow(), 1
            ).text()
            self.x_agenda.edit_fact_attr(
                road=f"{self.x_fact._parent_road},{self.x_fact._label}",
                balancelink_del=delete_idea_pid,
            )
            self.fact2idea_insert_combo_load()
            self.fact2idea_table_load()

    def fact_delete(self):
        self.x_agenda.del_fact_obj(
            road=f"{self.x_fact._parent_road},{self.x_fact._label}"
        )
        self.basefactunit.clear()
        self.refresh_tree(disable_is_expanded=True)

    def fact_edit_nonroad_data(self, fact_road):
        self.x_agenda.edit_fact_attr(
            road=fact_road,
            weight=float(self.yo_weight.toPlainText()),
            begin=str2float(self.yo_begin.toPlainText()),
            close=str2float(self.yo_close.toPlainText()),
            addin=str2float(self.yo_addin.toPlainText()),
            numor=str2float(self.yo_numor.toPlainText()),
            denom=str2float(self.yo_denom.toPlainText()),
            reest=self.yo_reest.checkState() == 2,
            range_source_road=emptystr(self.yo_range_source_road.currentText()),
            numeric_road=emptystr(self.yo_numeric_road.currentText()),
            pledge=(self.yo_action_cb.checkState() == 2),
            reason_base=None,
            reason_premise=None,
            reason_premise_open=None,
            reason_premise_nigh=None,
            reason_premise_divisor=None,
            reason_del_premise_base=None,
            reason_del_premise_need=None,
            uid=None,
            reason=None,
            descendant_pledge_count=None,
            all_party_cred=None,
            all_party_debt=None,
            balancelink=None,
            is_expanded=None,
        )

    def fact_edit_road(self, fact_road):
        self.x_agenda.edit_fact_label(
            old_road=fact_road,
            new_label=self.yo_deescription.toPlainText(),
        )

        # update hierarchical data
        self.refresh_tree(disable_is_expanded=True)
        self.yo_tree_item_setHidden(setHiddenBool=True)

    def fact_update(self):
        fact_road = None
        if self.x_fact._parent_road not in (None, ""):
            fact_road = f"{self.x_fact._parent_road},{self.x_fact._label}"
        else:
            fact_road = f"{self.x_fact._label}"
        self.fact_edit_nonroad_data(fact_road=fact_road)
        # if (
        #     self.fact_label_on_populate != self.yo_deescription.toPlainText()
        #     and self.fact_label_on_populate != ""
        #     and self.fact_label_on_populate != None
        # ):
        #     self.fact_edit_road()
        if self.x_fact._label != self.yo_deescription.toPlainText():
            self.fact_edit_road(fact_road=fact_road)

    def fact_pledge_insert(self):
        new_parent_road = f"{self.x_fact._label}"
        if self.x_fact._parent_road not in ("", None):
            new_parent_road = f"{self.x_fact._parent_road},{self.x_fact._label}"
        new_road = f"{new_parent_road},{self.yo_deescription.toPlainText()}"
        self.fact_insert()

        # add done/not_done children
        not_done_text = "not done"
        self.x_agenda.add_fact(factunit_shop(not_done_text), new_road)
        done_text = "done"
        self.x_agenda.add_fact(factunit_shop(done_text), new_road)
        # set reason to "not done"
        self.x_agenda.edit_fact_attr(
            road=new_road,
            reason_base=new_road,
            reason_premise=f"{new_road},{not_done_text}",
        )
        self.x_agenda.set_belief(
            base=new_road,
            pick=f"{new_road},{not_done_text}",
        )
        self.refresh_tree()

    def fact_insert(self):
        new_fact = factunit_shop(self.yo_deescription.toPlainText())
        fact_attr_x = factattrfilter_shop(
            weight=float(self.yo_weight.toPlainText()),
            begin=str2float(self.yo_begin.toPlainText()),
            close=str2float(self.yo_close.toPlainText()),
            addin=str2float(self.yo_addin.toPlainText()),
            numor=str2float(self.yo_numor.toPlainText()),
            denom=str2float(self.yo_denom.toPlainText()),
            reest=self.yo_reest.checkState() == 2,
            range_source_road=emptystring_returns_none(
                self.yo_range_source_road.currentText()
            ),
            numeric_road=emptystring_returns_none(self.yo_numeric_road.currentText()),
            pledge=(self.yo_action_cb.checkState() == 2),
            uid=None,
            reason=None,
            reason_base=None,
            reason_premise=None,
            reason_premise_open=None,
            reason_premise_nigh=None,
            reason_premise_divisor=None,
            reason_del_premise_base=None,
            reason_del_premise_need=None,
            descendant_pledge_count=None,
            all_party_cred=None,
            all_party_debt=None,
            balancelink=None,
            balancelink_del=None,
            is_expanded=None,
            meld_strategy=None,
        )
        new_fact._set_fact_attr(fact_attr=fact_attr_x)
        new_parent_road = f"{self.x_fact._label}"
        if self.x_fact._parent_road not in ("", None):
            new_parent_road = f"{self.x_fact._parent_road},{self.x_fact._label}"
        self.x_agenda.add_fact(new_fact, new_parent_road)
        self.refresh_tree()

    def refresh_tree(self, disable_is_expanded: bool = False):
        root_percent_flag = self.cb_rootadmiration.checkState() == 2
        yo_id_flag = self.cb_yo_id.checkState() == 2
        yo_intent_flag = self.cb_yo_intent.checkState() == 2
        yo_action_flag = self.cb_yo_action.checkState() == 2
        yo2bd_count_flag = self.cb_yo2bd_count.checkState() == 2
        # yo2bd_spec1_flag = self.yo2bd_spec1_flag.checkState() == 2
        yo_complete_flag = self.cb_yo_complete.checkState() == 2
        yo_beliefunit_time_flag = self.cb_yo_beliefunit_time.checkState() == 2
        yo_beliefunit_count_flag = self.cb_yo_beliefunit_count.checkState() == 2
        yo_beliefheir_count_flag = self.cb_yo_beliefheir_count.checkState() == 2
        reasonheir_count_flag = self.cb_reasonheir_count.checkState() == 2
        reason_count_flag = self.cb_reason_count.checkState() == 2
        reason_view_flag = self.cb_reason_view.checkState() == 2
        reason_view_base = self.combo_dim_root.currentText()
        beliefheir_view_flag = self.cb_beliefheir_view.checkState() == 2

        # root = self.basefactunit.invisibleRootItem()
        # self.yo_tree_isExpanded(node=root, level=1)
        root = self.basefactunit.invisibleRootItem()
        if not disable_is_expanded:
            self.fact_tree_set_is_expanded(root)

        tree_root = get_pyqttree(
            factroot=self.x_agenda._factroot,
            yo_intent_flag=yo_intent_flag,
            yo_action_flag=yo_action_flag,
            yo_beliefunit_time_flag=yo_beliefunit_time_flag,
            yo_beliefunit_count_flag=yo_beliefunit_count_flag,
            yo_beliefheir_count_flag=yo_beliefheir_count_flag,
            yo_complete_flag=yo_complete_flag,
            yo2bd_count_flag=yo2bd_count_flag,
            reasonheir_count_flag=reasonheir_count_flag,
            reason_count_flag=reason_count_flag,
            reason_view_flag=reason_view_flag,
            reason_view_person_id=reason_view_base,
            beliefheir_view_flag=beliefheir_view_flag,
            root_percent_flag=root_percent_flag,
            source_agenda=self.x_agenda,
        )

        self.basefactunit.clear()
        self.basefactunit.insertTopLevelItems(0, [tree_root])

        root = self.basefactunit.invisibleRootItem()
        self.pyqt_tree_setExpanded(root)
        # self.yo_tree_item_setHidden(setHiddenBool=True)

    # expand to depth set by agenda
    def pyqt_tree_setExpanded(self, root):
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            item.setExpanded(item.data(2, 20))
            self.pyqt_tree_setExpanded(item)

    def fact_tree_set_is_expanded(self, root):
        child_count = root.childCount()
        for i in range(child_count):
            item = root.child(i)
            label_x = item.data(2, 10)
            road_x = item.data(2, 11)
            is_expanded = item.isExpanded()
            # print(f"{road_x},{label_x}")
            _road = f"{label_x}" if road_x in ("", None) else f"{road_x},{label_x}"
            # print(f"road={road_x},{label_x}")
            # print(f"{_road=}")

            self.x_agenda.edit_fact_attr(road=_road, is_expanded=is_expanded)
            self.fact_tree_set_is_expanded(item)

    def reason_table_select(self):
        self.reason_base_combo_load()
        self.reason_base_combo.setCurrentText(
            self.reason_table.item(self.reason_table.currentRow(), 2).text()
        )
        self.reason_premise_combo.setCurrentText(
            self.reason_table.item(self.reason_table.currentRow(), 3).text()
        )
        self.reason_premise_open.setText(
            self.reason_table.item(self.reason_table.currentRow(), 4).text()
        )
        self.reason_premise_nigh.setText(
            self.reason_table.item(self.reason_table.currentRow(), 5).text()
        )
        self.reason_premise_divisor.setText(
            self.reason_table.item(self.reason_table.currentRow(), 6).text()
        )

        if self.reason_premise_divisor.toPlainText() != "":
            if float(self.reason_premise_divisor.toPlainText()) % 10080 == 0:
                self.set_weeks_repeat_premiseunit_hregtime()
            elif float(self.reason_premise_divisor.toPlainText()) % 1440 == 0:
                self.set_days_repeat_premiseunit_hregtime()

    def set_days_repeat_premiseunit_hregtime(self):
        days_minutes = float(self.reason_premise_open.toPlainText())
        day_minutes = days_minutes % 1440
        days_repeat = float(self.reason_premise_divisor.toPlainText()) / 1440
        self.hreg_days_repeat.setText(str(int(days_repeat)))

        days_remainder = (days_minutes - day_minutes) / 1440
        self.hreg_days_remainder.setText(str(int(days_remainder)))

        event_minute = day_minutes % 60
        self.hreg_open_min.setCurrentText(str(int(event_minute)))

        event_hour = (day_minutes - event_minute) / 60
        self.hreg_open_hr.setCurrentText(str(int(event_hour)))

    def set_weeks_repeat_premiseunit_hregtime(self):
        self.hreg_weeks_repeat.setText(
            str(int(float(self.reason_premise_divisor.toPlainText()) / 1440))
        )

        week_extra_min = float(self.reason_premise_open.toPlainText()) % 10080
        week_remainder = (
            float(self.reason_premise_open.toPlainText()) - week_extra_min
        ) / 10080
        self.hreg_weeks_remainder.setText(str(int(week_remainder)))

        day_minutes_extra = week_extra_min % 1440
        days_extra = (week_extra_min - day_minutes_extra) / 1440
        if days_extra == 0:
            self.hreg_weekday.setCurrentText("Saturday")
        elif days_extra == 1:
            self.hreg_weekday.setCurrentText("Sunday")
        elif days_extra == 2:
            self.hreg_weekday.setCurrentText("Monday")
        elif days_extra == 3:
            self.hreg_weekday.setCurrentText("Tuesday")
        elif days_extra == 4:
            self.hreg_weekday.setCurrentText("Wednesday")
        elif days_extra == 5:
            self.hreg_weekday.setCurrentText("Thursday")
        elif days_extra == 6:
            self.hreg_weekday.setCurrentText("Friday")

        event_minute = day_minutes_extra % 60

        self.hreg_open_min.setCurrentText(str(int(event_minute)))
        event_hour = (day_minutes_extra - event_minute) / 60
        self.hreg_open_hr.setCurrentText(str(int(event_hour)))

        days_extra = week_extra_min - 0

    def set_weeks_repeat_premiseunit_hregtime(self):
        self.hreg_weeks_repeat.setText(
            str(int(float(self.reason_premise_divisor.toPlainText()) / 10080))
        )

        week_extra_min = float(self.reason_premise_open.toPlainText()) % 10080
        week_remainder = (
            float(self.reason_premise_open.toPlainText()) - week_extra_min
        ) / 10080
        self.hreg_weeks_remainder.setText(str(int(week_remainder)))

        day_minutes_extra = week_extra_min % 1440
        days_extra = (week_extra_min - day_minutes_extra) / 1440
        if days_extra == 0:
            self.hreg_weekday.setCurrentText("Saturday")
        elif days_extra == 1:
            self.hreg_weekday.setCurrentText("Sunday")
        elif days_extra == 2:
            self.hreg_weekday.setCurrentText("Monday")
        elif days_extra == 3:
            self.hreg_weekday.setCurrentText("Tuesday")
        elif days_extra == 4:
            self.hreg_weekday.setCurrentText("Wednesday")
        elif days_extra == 5:
            self.hreg_weekday.setCurrentText("Thursday")
        elif days_extra == 6:
            self.hreg_weekday.setCurrentText("Friday")

        event_minute = day_minutes_extra % 60

        self.hreg_open_min.setCurrentText(str(int(event_minute)))
        event_hour = (day_minutes_extra - event_minute) / 60
        self.hreg_open_hr.setCurrentText(str(int(event_hour)))

        days_extra = week_extra_min - 0
