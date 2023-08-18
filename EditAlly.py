# command to for converting ui form to python file: pyuic5 ui\EditAllyUI.ui -o ui\EditAllyUI.py
import sys
from ui.EditAllyUI import Ui_Form
from PyQt5 import QtWidgets as qtw
from PyQt5 import QtCore as qtc
from EditAlly2bd import EditAlly2bd
from src.pyqt5_tools.pyqt_func import lw_diplay
from src.agent.agent import AgentUnit
from src.agent.brand import brandunit_shop
from src.agent.ally import allylink_shop


class EditAlly(qtw.QTableWidget, Ui_Form):
    ally_selected = qtc.pyqtSignal(int)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setupUi(self)

        self.ally_table.itemClicked.connect(self.ally_select)
        self.ally_insert_button.clicked.connect(self.ally_insert)
        self.ally_update_button.clicked.connect(self.ally_update)
        self.ally_delete_button.clicked.connect(self.ally_delete)
        self.brands_in_table.itemClicked.connect(self.brands_in_select)
        self.brands_out_table.itemClicked.connect(self.brands_out_select)
        self.brand_insert_button.clicked.connect(self.brand_insert)
        self.brand_update_button.clicked.connect(self.brand_update)
        self.brand_delete_button.clicked.connect(self.brand_delete)
        self.ally_brand_set_button.clicked.connect(self.ally_brand_set)
        self.ally_brand_del_button.clicked.connect(self.ally_brand_del)
        self.close_button.clicked.connect(self.close)
        self.quit_button.clicked.connect(sys.exit)
        self.selected_ally_name = None
        self.allyunit_x = None
        self.brandunit_x = None

    def ally_select(self):
        ally_name = self.ally_table.item(self.ally_table.currentRow(), 0).text()
        self.allyunit_x = self.agent_x._allys.get(ally_name)
        self.ally_name.setText(self.allyunit_x.name)
        self.refresh_brands()

    def brands_in_select(self):
        brand_name = self.brands_in_table.item(
            self.brands_in_table.currentRow(), 0
        ).text()
        self.brandunit_x = self.agent_x._brands.get(brand_name)
        self.brand_name.setText(self.brandunit_x.name)

    def brands_out_select(self):
        brand_name = self.brands_out_table.item(
            self.brands_out_table.currentRow(), 0
        ).text()
        self.brandunit_x = self.agent_x._brands.get(brand_name)
        self.brand_name.setText(self.brandunit_x.name)

    def ally_brand_set(self):
        self.brandunit_x.set_allylink(allylink=allylink_shop(name=self.allyunit_x.name))
        self.refresh_brands()

    def ally_brand_del(self):
        if self.brandunit_x._allys.get(self.allyunit_x.name) != None:
            self.brandunit_x.del_allylink(name=self.allyunit_x.name)
        self.refresh_brands()

    def get_ally_brand_count(self, ally_name: str):  # AllyName):
        single_brand = ""
        brands_count = 0
        brand_allylinks = []
        for brand in self.agent_x._brands.values():
            for allylink in brand._allys.values():
                if allylink.name == ally_name and brand.name != allylink.name:
                    brands_count += 1
                    single_brand = brand.name
                    brand_allylinks.append((brand, allylink))

        return brands_count, single_brand, brand_allylinks

    def refresh_ally_table(self):
        self.ally_table.setObjectName("Allys")
        self.ally_table.setColumnHidden(0, False)
        self.ally_table.setColumnWidth(0, 170)
        self.ally_table.setColumnWidth(1, 130)
        self.ally_table.setColumnWidth(2, 40)
        self.ally_table.setColumnWidth(3, 60)
        self.ally_table.setColumnWidth(4, 40)
        self.ally_table.setHorizontalHeaderLabels(
            ["Ally", "Brand", "Brand Count", "AGENT_Importance", "Weight"]
        )
        self.ally_table.setRowCount(0)

        allys_list = list(self.agent_x._allys.values())
        allys_list.sort(key=lambda x: x.name, reverse=False)

        for row, ally in enumerate(allys_list, start=1):
            # brands_count = 0
            # for brand in self.agent_x._brands.values():
            #     for allylink in brand._allys.values():
            #         if allylink.name == ally.name:
            #             brands_count += 1

            brands_count, single_brand, brand_allylinks = self.get_ally_brand_count(
                ally_name=ally.name
            )

            self.ally_table.setRowCount(row)
            self.ally_table.setItem(row - 1, 0, qtw.QTableWidgetItem(ally.name))
            qt_agent_credit = qtw.QTableWidgetItem(lw_diplay(ally._agent_credit))
            qt_agent_debt = qtw.QTableWidgetItem(lw_diplay(ally._agent_debt))
            self.ally_table.setItem(row - 1, 1, qtw.QTableWidgetItem(single_brand))
            self.ally_table.setItem(row - 1, 2, qtw.QTableWidgetItem("#"))
            self.ally_table.setItem(row - 1, 3, qt_agent_credit)
            # self.ally_table.setItem(row - 1, 3, qt_agent_debt)
            self.ally_table.setItem(
                row - 1, 4, qtw.QTableWidgetItem(f"{ally.creditor_weight}")
            )
            # self.ally_table.setItem(
            #     row - 1, 4, qtw.QTableWidgetItem(f"{ally.debtor_weight}")
            # )

    def ally_in_brand(self, allyunit, brandunit):
        return any(
            allylink.name == allyunit.name for allylink in brandunit._allys.values()
        )

    def refresh_brands_in_table(self):
        self.brands_in_table.setObjectName("Brands Linked")
        self.brands_in_table.setColumnHidden(0, False)
        self.brands_in_table.setColumnWidth(0, 170)
        self.brands_in_table.setColumnWidth(1, 130)
        self.brands_in_table.setColumnWidth(2, 40)
        self.brands_in_table.setColumnWidth(3, 60)
        self.brands_in_table.setColumnWidth(4, 40)
        self.brands_in_table.setRowCount(0)

        brands_in_list = [
            brandunit
            for brandunit in self.agent_x._brands.values()
            if (
                self.allyunit_x != None
                and self.ally_in_brand(allyunit=self.allyunit_x, brandunit=brandunit)
                and self.allyunit_x.name != brandunit.name
            )
        ]
        brands_in_list.sort(key=lambda x: x.name, reverse=False)

        self.brands_in_table.setHorizontalHeaderLabels(
            [f"Brands ({len(brands_in_list)})", "Brand", "Brand Count"]
        )

        for row, brandunit_x in enumerate(brands_in_list, start=1):
            self.brands_in_table.setRowCount(row)
            self.brands_in_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(brandunit_x.name)
            )

    def refresh_brands_out_table(self):
        self.brands_out_table.setObjectName("Brands Linked")
        self.brands_out_table.setColumnHidden(0, False)
        self.brands_out_table.setColumnWidth(0, 170)
        self.brands_out_table.setColumnWidth(1, 130)
        self.brands_out_table.setColumnWidth(2, 40)
        self.brands_out_table.setColumnWidth(3, 60)
        self.brands_out_table.setColumnWidth(4, 40)
        self.brands_out_table.setRowCount(0)

        brands_out_list = [
            brandunit
            for brandunit in self.agent_x._brands.values()
            if (
                self.allyunit_x != None
                and brandunit._allys.get(brandunit.name) is None
                and (
                    self.ally_in_brand(allyunit=self.allyunit_x, brandunit=brandunit)
                    == False
                )
            )
            or self.allyunit_x is None
        ]
        brands_out_list.sort(key=lambda x: x.name, reverse=False)
        self.brands_out_table.setHorizontalHeaderLabels(
            [f"Brands ({len(brands_out_list)})", "Brand", "Brand Count"]
        )

        for row, brandunit_x in enumerate(brands_out_list, start=1):
            self.brands_out_table.setRowCount(row)
            self.brands_out_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(brandunit_x.name)
            )

    def refresh_brands_stan_table(self):
        self.brands_stan_table.setObjectName("Brands Linked")
        self.brands_stan_table.setColumnHidden(0, False)
        self.brands_stan_table.setColumnWidth(0, 170)
        self.brands_stan_table.setColumnWidth(1, 130)
        self.brands_stan_table.setColumnWidth(2, 40)
        self.brands_stan_table.setColumnWidth(3, 60)
        self.brands_stan_table.setColumnWidth(4, 40)
        self.brands_stan_table.setRowCount(0)

        brands_stand_list = [
            brandunit
            for brandunit in self.agent_x._brands.values()
            if self.allyunit_x != None
            and (
                brandunit._allys.get(brandunit.name) != None
                and self.allyunit_x.name == brandunit.name
            )
        ]
        brands_stand_list.sort(key=lambda x: x.name, reverse=False)
        self.brands_stan_table.setHorizontalHeaderLabels(
            [f"Brands ({len(brands_stand_list)})", "Brand", "Brand Count"]
        )

        for row, brandunit_x in enumerate(brands_stand_list, start=1):
            self.brands_stan_table.setRowCount(row)
            self.brands_stan_table.setItem(
                row - 1, 0, qtw.QTableWidgetItem(brandunit_x.name)
            )

    def refresh_all(self):
        self.refresh_ally_table()
        self.ally_name.setText("")
        self.refresh_brands()
        if self.brand_name != None:
            self.brand_name.setText("")

    def refresh_brands(self):
        self.refresh_brands_in_table()
        self.refresh_brands_out_table()
        self.refresh_brands_stan_table()

    def ally_insert(self):
        self.agent_x.add_allyunit(name=self.ally_name.text())
        self.refresh_all()

    def ally_delete(self):
        self.agent_x.del_allyunit(name=self.ally_name.text())
        self.ally_name.setText("")
        self.allyunit_x = None
        self.refresh_all()

    def ally_update(self):
        self.agent_x.edit_allyunit_name(
            old_name=self.ally_table.item(self.ally_table.currentRow(), 0).text(),
            new_name=self.ally_name.text(),
            allow_ally_overwite=True,
            allow_nonsingle_brand_overwrite=True,
        )
        self.ally_name.setText("")
        self.refresh_all()

    def brand_insert(self):
        bu = brandunit_shop(name=self.brand_name.text())
        self.agent_x.set_brandunit(brandunit=bu)
        self.refresh_brands()

    def brand_delete(self):
        self.agent_x.del_brandunit(brandname=self.brand_name.text())
        self.brand_name.setText("")
        self.refresh_brands()

    def brand_update(self):
        if self.brand_name != None:
            self.agent_x.edit_brandunit_name(
                old_name=self.brands_in_table.item(
                    self.brands_in_table.currentRow(), 0
                ).text(),
                new_name=self.brand_name.text(),
                allow_brand_overwite=True,
            )
            self.brand_name.setText("")
        self.refresh_brands()
