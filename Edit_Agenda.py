# command to for converting ui form to python file: pyuic5 ui\Edit_AgendaUI.ui -o ui\Edit_AgendaUI.pyrefresh_all
from ui.Edit_AgendaUI import Ui_Form
from PyQt5.QtCore import pyqtSignal as qsig
from PyQt5.QtWidgets import QWidget as qw
from PyQt5.QtWidgets import QTableWidgetItem as qti
from src.pyqt5_kit.pyqt_func import num2str, contract_importance_diplay
from src.contract.hreg_time import (
    SuffFactUnitHregTime,
    _get_time_hreg_weekday_idea,
    convert1440toHHMM,
)


class Edit_Agenda(qw, Ui_Form):
    agenda_changed = qsig(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.close_button.clicked.connect(self.close)
        self.refresh_button.clicked.connect(self.refresh_all)
        self.agenda_table.itemClicked.connect(self.select_agenda_item)
        self.agenda_table.setObjectName("Current Agenda")
        self.agenda_table.setRowCount(0)
        self.acptfact_base_update_combo.currentTextChanged.connect(
            self.refreshAgendaTable
        )
        self.cb_acptfactbase_display.stateChanged.connect(self.refresh_all)
        self.acptfact_base_update_init_road = "time,jajatime"
        # self.refresh_all()

    def select_agenda_item(self):
        _road = self.agenda_table.item(self.agenda_table.currentRow(), 1).text()
        _label = self.agenda_table.item(self.agenda_table.currentRow(), 0).text()
        # base_x = "Mycontract,time,jajatime"
        base_x = self.acptfact_base_update_combo.currentText()
        self.contract_x.set_agenda_task_complete(
            task_road=f"{_road},{_label}", base=base_x
        )
        self.refresh_all()

        # yo_id_greater = int(self.agenda_table.item(0, 6).text())
        # if yo_id_lesser != None:
        #     self.agenda_core.set_greater_weight(
        #         yo_id_lesser=yo_id_lesser, yo_id_greater=yo_id_greater
        #     )
        #     self.refresh_all()
        #     self.agenda_changed.emit(True)
        #     self.close()

    def refresh_all(self):
        self.refreshRequiredBaseCombo()
        self.refreshAgendaTable()

    def refreshRequiredBaseCombo(self):
        if self.acptfact_base_update_init_road is None:
            temp_x = self.acptfact_base_update_combo.currentText()

        self.acptfact_base_update_combo.clear()
        required_bases = list(self.contract_x.get_required_bases())
        required_bases.sort(key=lambda x: x, reverse=False)
        self.acptfact_base_update_combo.addItems(required_bases)
        if self.acptfact_base_update_init_road is None:
            self.acptfact_base_update_combo.setCurrentText(temp_x)

        else:
            self.acptfact_base_update_init_road = (
                f"{self.contract_x._heal_kind},time,jajatime"
            )
            self.acptfact_base_update_combo.setCurrentText(
                self.acptfact_base_update_init_road
            )
            self.acptfact_base_update_init_road = None

    def refreshAgendaTable(self):
        self.agenda_table.clear()
        self.agenda_table.setRowCount(0)
        base_x = self.acptfact_base_update_combo.currentText()
        if base_x == "":
            base_x = None

        agenda_list = self.contract_x.get_agenda_items(
            agenda_todo=True, agenda_state=False, base=base_x
        )
        agenda_list.sort(key=lambda x: x._contract_importance, reverse=True)

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
        lw_display_x = contract_importance_diplay(
            contract_importance=a._contract_importance
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
                sufffact_need_x == f"{self.contract_x._heal_kind},time,jajatime"
                or sufffact_need_x[:21] == f"{self.contract_x._heal_kind},time,jajatime"
            )
        ):
            legible_x_text = self.contract_x.get_jajatime_repeating_legible_text(
                open=sufffact_open_x, nigh=sufffact_nigh_x, divisor=sufffact_divisor_x
            )
        elif sufffact_open_x != None and sufffact_nigh_x != None:
            text_x = f"{self.contract_x._heal_kind},time,jajatime"
            legible_x_text = (
                f"sufffact {sufffact_open_x}-{sufffact_nigh_x} {sufffact_divisor_x=}"
            )
        else:
            legible_x_text = (
                f"sufffact {sufffact_open_x}-{sufffact_nigh_x} {sufffact_divisor_x=}"
            )

        self.agenda_table.setRowCount(row + 1)
        self.agenda_table.setItem(row, 0, qti(a._label))
        self.agenda_table.setItem(row, 1, qti(a._walk))
        self.agenda_table.setItem(row, 2, qti(lw_display_x))
        self.agenda_table.setItem(row, 3, qti(num2str(a._weight)))
        self.agenda_table.setItem(row, 4, qti(base))
        self.agenda_table.setItem(row, 5, qti(num2str(sufffact_open_x)))
        self.agenda_table.setItem(row, 6, qti(num2str(sufffact_nigh_x)))
        self.agenda_table.setItem(row, 7, qti(num2str(sufffact_divisor_x)))
        self.agenda_table.setItem(row, 8, qti(legible_x_text))
        # if a._task in (True, False):
        #     self.agenda_table.setItem(row, 7, qti(f"task {a._task}"))
        # else:
        #     self.agenda_table.setItem(row, 7, qti("bool not set"))
        self.agenda_table.setRowHeight(row, 5)
        self.agenda_table.setColumnWidth(0, 300)
        self.agenda_table.setColumnWidth(1, 400)
        self.agenda_table.setColumnWidth(2, 55)
        self.agenda_table.setColumnWidth(3, 55)
        self.agenda_table.setColumnWidth(4, 150)
        self.agenda_table.setColumnWidth(5, 70)
        self.agenda_table.setColumnWidth(6, 70)
        self.agenda_table.setColumnWidth(7, 70)
        self.agenda_table.setColumnWidth(8, 250)
        self.agenda_table.setColumnHidden(0, False)
        self.agenda_table.setColumnHidden(1, False)
        self.agenda_table.setColumnHidden(2, False)
        self.agenda_table.setColumnHidden(3, True)
        self.agenda_table.setColumnHidden(4, display_acptfactbase)
        self.agenda_table.setColumnHidden(5, display_acptfactbase)
        self.agenda_table.setColumnHidden(6, display_acptfactbase)
        self.agenda_table.setColumnHidden(7, display_acptfactbase)
        self.agenda_table.setColumnHidden(8, not display_acptfactbase)
        self.agenda_table.setHorizontalHeaderLabels(
            [
                "_label",
                "road",
                "contract_importance",
                "weight",
                "acptfact",
                "open",
                "nigh",
                "divisor",
                "time",
            ]
        )
