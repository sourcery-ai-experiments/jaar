# command to for converting ui form to python file: pyuic5 ui\Edit_AgendaUI.ui -o ui\Edit_AgendaUI.pyrefresh_all
from ui.Edit_AgendaUI import Ui_Form
from PyQt5.QtCore import pyqtSignal as qsig
from PyQt5.QtWidgets import QWidget as qw
from PyQt5.QtWidgets import QTableWidgetItem as qti
from pyqt_func import num2str, agenda_importance_diplay
from src.agenda.hreg_time import (
    SuffFactUnitHregTime,
    _get_time_hreg_weekday_idea,
    convert1440toHHMM,
)


class Edit_Agenda(qw, Ui_Form):
    intent_changed = qsig(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.close_button.clicked.connect(self.close)
        self.refresh_button.clicked.connect(self.refresh_all)
        self.intent_table.itemClicked.connect(self.select_intent_item)
        self.intent_table.setObjectName("Current Agenda")
        self.intent_table.setRowCount(0)
        self.acptfact_base_update_combo.currentTextChanged.connect(
            self.refreshAgendaTable
        )
        self.cb_acptfactbase_display.stateChanged.connect(self.refresh_all)
        self.acptfact_base_update_init_road = "time,jajatime"
        # self.refresh_all()

    def select_intent_item(self):
        _road = self.intent_table.item(self.intent_table.currentRow(), 1).text()
        _label = self.intent_table.item(self.intent_table.currentRow(), 0).text()
        # base_x = "A,time,jajatime"
        base_x = self.acptfact_base_update_combo.currentText()
        self.agenda_x.set_intent_task_complete(
            task_road=f"{_road},{_label}", base=base_x
        )
        self.refresh_all()

        # yo_id_greater = int(self.intent_table.item(0, 6).text())
        # if yo_id_lesser != None:
        #     self.intent_core.set_greater_weight(
        #         yo_id_lesser=yo_id_lesser, yo_id_greater=yo_id_greater
        #     )
        #     self.refresh_all()
        #     self.intent_changed.emit(True)
        #     self.close()

    def refresh_all(self):
        self.refreshRequiredBaseCombo()
        self.refreshAgendaTable()

    def refreshRequiredBaseCombo(self):
        if self.acptfact_base_update_init_road is None:
            temp_x = self.acptfact_base_update_combo.currentText()

        self.acptfact_base_update_combo.clear()
        required_bases = list(self.agenda_x.get_required_bases())
        required_bases.sort(key=lambda x: x, reverse=False)
        self.acptfact_base_update_combo.addItems(required_bases)
        if self.acptfact_base_update_init_road is None:
            self.acptfact_base_update_combo.setCurrentText(temp_x)

        else:
            self.acptfact_base_update_init_road = (
                f"{self.agenda_x._culture_qid},time,jajatime"
            )
            self.acptfact_base_update_combo.setCurrentText(
                self.acptfact_base_update_init_road
            )
            self.acptfact_base_update_init_road = None

    def refreshAgendaTable(self):
        self.intent_table.clear()
        self.intent_table.setRowCount(0)
        base_x = self.acptfact_base_update_combo.currentText()
        if base_x == "":
            base_x = None

        intent_list = self.agenda_x.get_intent_items(
            intent_enterprise=True, intent_state=False, base=base_x
        )
        intent_list.sort(key=lambda x: x._agenda_importance, reverse=True)

        row = 0
        for intent_item in intent_list:
            if intent_item._task == True:
                self.populate_intent_table_row(
                    row=row, intent_item=intent_item, base=base_x
                )
                row += 1

    def populate_intent_table_row(self, row, intent_item, base):
        a = intent_item
        requiredheir_x = a.get_requiredheir(base=base)
        sufffact_open_x = None
        sufffact_nigh_x = None
        sufffact_divisor_x = None
        agenda_display_x = agenda_importance_diplay(
            agenda_importance=a._agenda_importance
        )

        display_acptfactbase = self.cb_acptfactbase_display.checkState() != 2

        if requiredheir_x != None:
            for sufffact in requiredheir_x.sufffacts.values():
                # if sufffact_task == True:
                sufffact_need_x = sufffact.need
                sufffact_open_x = sufffact.open
                sufffact_nigh_x = sufffact.nigh
                sufffact_divisor_x = sufffact.divisor

        legible_x_text = ""
        if (
            sufffact_open_x != None
            and sufffact_nigh_x != None
            and (
                sufffact_need_x == f"{self.agenda_x._culture_qid},time,jajatime"
                or sufffact_need_x[:21] == f"{self.agenda_x._culture_qid},time,jajatime"
            )
        ):
            legible_x_text = self.agenda_x.get_jajatime_repeating_legible_text(
                open=sufffact_open_x, nigh=sufffact_nigh_x, divisor=sufffact_divisor_x
            )
        elif sufffact_open_x != None and sufffact_nigh_x != None:
            text_x = f"{self.agenda_x._culture_qid},time,jajatime"
            legible_x_text = (
                f"sufffact {sufffact_open_x}-{sufffact_nigh_x} {sufffact_divisor_x=}"
            )
        else:
            legible_x_text = (
                f"sufffact {sufffact_open_x}-{sufffact_nigh_x} {sufffact_divisor_x=}"
            )

        self.intent_table.setRowCount(row + 1)
        self.intent_table.setItem(row, 0, qti(a._label))
        self.intent_table.setItem(row, 1, qti(a._pad))
        self.intent_table.setItem(row, 2, qti(agenda_display_x))
        self.intent_table.setItem(row, 3, qti(num2str(a._weight)))
        self.intent_table.setItem(row, 4, qti(base))
        self.intent_table.setItem(row, 5, qti(num2str(sufffact_open_x)))
        self.intent_table.setItem(row, 6, qti(num2str(sufffact_nigh_x)))
        self.intent_table.setItem(row, 7, qti(num2str(sufffact_divisor_x)))
        self.intent_table.setItem(row, 8, qti(legible_x_text))
        # if a._task in (True, False):
        #     self.intent_table.setItem(row, 7, qti(f"task {a._task}"))
        # else:
        #     self.intent_table.setItem(row, 7, qti("bool not set"))
        self.intent_table.setRowHeight(row, 5)
        self.intent_table.setColumnWidth(0, 300)
        self.intent_table.setColumnWidth(1, 400)
        self.intent_table.setColumnWidth(2, 55)
        self.intent_table.setColumnWidth(3, 55)
        self.intent_table.setColumnWidth(4, 150)
        self.intent_table.setColumnWidth(5, 70)
        self.intent_table.setColumnWidth(6, 70)
        self.intent_table.setColumnWidth(7, 70)
        self.intent_table.setColumnWidth(8, 250)
        self.intent_table.setColumnHidden(0, False)
        self.intent_table.setColumnHidden(1, False)
        self.intent_table.setColumnHidden(2, False)
        self.intent_table.setColumnHidden(3, True)
        self.intent_table.setColumnHidden(4, display_acptfactbase)
        self.intent_table.setColumnHidden(5, display_acptfactbase)
        self.intent_table.setColumnHidden(6, display_acptfactbase)
        self.intent_table.setColumnHidden(7, display_acptfactbase)
        self.intent_table.setColumnHidden(8, not display_acptfactbase)
        self.intent_table.setHorizontalHeaderLabels(
            [
                "_label",
                "road",
                "agenda_importance",
                "weight",
                "acptfact",
                "open",
                "nigh",
                "divisor",
                "time",
            ]
        )
