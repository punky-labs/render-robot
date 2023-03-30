# -*- coding: utf-8 -*-
# rprename/views.py

"""This module provides the Views for main window."""

from PyQt6.QtCore import QThread, Qt
from PyQt6.QtWidgets import QFileDialog, QMainWindow, QTableWidgetItem, QDialog, QLabel
from PyQt6.QtGui import QStandardItemModel, QIcon, QPixmap
from pathlib import Path

import os

from .ui.window import Ui_MainWindow
from render_robot.render import Render
import render_robot.process as process

CSV_FILTERS = ";;".join(
    (
        "CSV Files (*.csv)",
        "Text Files (*.txt)",
        "All File Formats (*.*)"
    )
)

AEF_FILTERS = ";;".join(
    (
        "Adobe After Effects Project (*.aep;*.aet;*.mogrt;*.aegraphic)",
        "All File Formats (*.*)"
    )
)

APP_NAME = "Robot Render"

class Window(QMainWindow, Ui_MainWindow):


    def __init__(self):
        super().__init__()
        self._setupUI()
        self._connectSignalsSlots()
        self._local = True
        self._valid = False
        icon_path = os.path.dirname(os.path.realpath(__file__)) + '/robot.png'
        self.setWindowIcon(QIcon(icon_path))
        self.setWindowTitle(APP_NAME)

        pixmap = QPixmap(icon_path)
        self.logo_label.setPixmap(pixmap)
        self.logo_label.setScaledContents(True)
        #self.resize(pixmap.width(), pixmap.height())

    def _setupUI(self):
        self.setupUi(self)
        render_prefix_items = ["0", "00" ,"000","0000"]
        self.prefix_numb.addItems(render_prefix_items)
        ext_items = [".mp4", ".mov" ,".png",".exr"]
        self.ext_box.addItems(ext_items)
        self._var_path_group = [
            self.var_path,
            self.var_path_button,
            self.local_label,
            ]
        self._var_url_group = [
            self.csv_url,
            self.url_label,
            self.load_online_button
            ]
        self._name_prefix_group = [
            self.comp_prefix,
            self.prefix_numb,
            self.ext_box,
            self.label_6
            ]
        self._name_csv_group = [
            self.csv_prefix,
            self.label_11
        ]
        self._om_group = [
            self.label_13,
            self.output_module
        ]

    def _connectSignalsSlots(self):
        self.ae_path_button.clicked.connect(self._ae_path_selected)
        self.proj_path_button.clicked.connect(self._proj_path_selected)
        self.set_path_button.clicked.connect(self._proj_set_selected)
        self.out_path_button.clicked.connect(self._out_path_selected)
        self.var_path_button.clicked.connect(self._var_path_selected)
        self.var_path.textChanged.connect(self._loaded_csv_local)
        self.load_online_button.clicked.connect(self._loaded_csv_remote)
        self.render_button.clicked.connect(self._render_selected)
        self.radioSource_1.toggled.connect(self._radio_toggled)
        self.radioSource_2.toggled.connect(self._radio_toggled)
        self.name_radio_1.toggled.connect(self._name_toggled)
        self.name_radio_2.toggled.connect(self._name_toggled)
        self.om_check.clicked.connect(self.om_checked)
        self.actionHelp.triggered.connect(self.help)
        self.actionAbout.triggered.connect(self.about)


    def _ae_path_selected(self):
        if self.ae_path.text():
            initDir = self.ae_path.text()
        else:
            initDir = str(Path.home())
        dirname = QFileDialog.getExistingDirectory(
            self, "Select After Effects application folder", initDir,
            )
        if dirname:
            path = Path(dirname)
            self.ae_path.setText(str(path))

    def _proj_path_selected(self):
        if self.proj_path.text():
            initDir = self.proj_path.text()
        else:
            initDir = str(Path.home())
        files, filter = QFileDialog.getOpenFileNames(
            self, "Select After Effects project", initDir, AEF_FILTERS
            )
        if len(files) > 0:
            self.proj_path.setText(files[0])
            self.setWindowTitle(APP_NAME + " - "+ str(files[0]))

    def _proj_set_selected(self):
        if self.set_path.text():
            initDir = self.set_path.text()
        else:
            initDir = str(Path.home())
        files, _ = QFileDialog.getOpenFileNames(
            self, "Select project settings", initDir, CSV_FILTERS
            )
        if len(files) > 0:
            self.set_path.setText(files[0])

    def _out_path_selected(self):
        if self.out_path.text():
            initDir = self.out_path.text()
        else:
            initDir = str(Path.home())
        dirname = QFileDialog.getExistingDirectory(
            self, "Select output folder", initDir,
            )
        if dirname:
            path = Path(dirname)
            self.out_path.setText(str(path))


    def _var_path_selected(self):
        if self.var_path.text():
            initDir = self.var_path.text()
        else:
            initDir = str(Path.home())
        files, _ = QFileDialog.getOpenFileNames(
            self, "Choose source file", initDir, CSV_FILTERS
            )
        if len(files) > 0:
            self.var_path.setText(files[0])

    def _render_selected(self):

        if self.proj_path.text == '':
            self.statusUpdate("Please select an After Effects project")
            return
        if self.set_path.text == '':
            self.statusUpdate("Please select a projects settings file")
            return
        """
        if self.comp_name.text == '':
            self.statusUpdate("Please enter a composition name")
            return
        """
        if self._local:
            self._var_loc = self.var_path.text()
            if self.var_path.text() == '' or not self._valid:
                self.statusUpdate("Please select a valid source file")
                return
        else:
            self._var_loc = self.csv_url.text()
            if self.csv_url.text() == '' or not self._valid:
                self.statusUpdate("Please select a valid source file")
                return
        
        
        if self.name_radio_1.isChecked():
            if self.comp_prefix.text() == '':
                self.comp_prefix.setText(self.comp_name.text())
            self.prefix = self.comp_prefix.text()
            self.numpad = self.prefix_numb.currentText()
            self.csv_name = False
        else:
            self.prefix = self.csv_prefix.currentIndex()
            self.numpad = '0'
            self.csv_name = True

        if self.om_check.isChecked() and self.output_module.currentIndex():
            self.om = self.output_module.currentIndex()
        else:
            self.om = False
        
        self._thread = QThread()
        self._render = Render(self.ae_path.text(), 
                              proj_path = self.proj_path.text(), 
                              out_path = self.out_path.text(), 
                              comp_prefix = self.prefix,
                              var_path = self._var_loc, 
                              set_file = self.set_path.text(),
                              comp_name = self.comp_csv.currentIndex(),
                              csv_name = self.csv_name,
                              output_module = self.om,
                              file_ext = self.ext_box.currentText(),
                              num_pad = self.numpad
        )
        self._render.moveToThread(self._thread)
        # Filter
        if self._local:
            self._thread.started.connect(self._render.localCSV)
        else:
            self._thread.started.connect(self._render.streamCSV)
        self._render.progressed.connect(self._updateProgressBar)
        self._render.rendered_file.connect(self._updateProgressList)
        self._render.status_update.connect(self.statusUpdate)
        # Clean up
        self._render.finished.connect(self._thread.quit)
        self._render.finished.connect(self._render.deleteLater)
        self._thread.finished.connect(self._thread.deleteLater)
        # Run the thread
        self._thread.start()

    def _updateProgressBar(self, progressPercent):
        self.render_progress.setValue(progressPercent)

    def _updateProgressList(self, file):
        self.render_list.addItem(file)

    def toggle_group(self, group, state):
        for item in group:
            item.setEnabled(state)

    def _radio_toggled(self):
        self.toggle_group(self._var_path_group, self.radioSource_1.isChecked())
        self.toggle_group(self._var_url_group, self.radioSource_2.isChecked())
        self._local = False

    def _name_toggled(self):
        self.toggle_group(self._name_prefix_group, self.name_radio_1.isChecked())
        self.toggle_group(self._name_csv_group, self.name_radio_2.isChecked())

    def om_checked(self):
        self.toggle_group(self._om_group, self.om_check.isChecked())


    def statusUpdate(self, string):
        self.statusbar = self.statusBar()
        self.statusbar.showMessage(string, 4000)

    def _loaded_csv_local(self):
        self._valid = False
        if self.var_path.text() != '':
            self.statusUpdate("Loading file")
            headers = process.get_headers_local(self.var_path.text())
            if headers:
                self._headers = headers
                self.update_headers()
                self.statusUpdate("Loaded file")
                self._valid = True
            else:
                self.statusUpdate("Error reading file")

    def _loaded_csv_remote(self):
        self._valid = False
        if self.csv_url.text() != '':
            self.statusUpdate("Getting remote data")
            headers = process.get_headers_remote(self.csv_url.text())
            if headers:
                self._headers = headers
                self.update_headers()
                self.statusUpdate("Loaded remote data")
                self._valid = True
            else:
                self.statusUpdate("Error retrieving data")
                
        else:
            self.statusUpdate("Please enter a valid URL")

    def update_headers(self):
        name_prefix_items = self._headers
        self.csv_prefix.clear()
        self.csv_prefix.addItems(name_prefix_items)
        self.comp_csv.clear()
        self.comp_csv.addItems(name_prefix_items)
        self.output_module.clear()
        self.output_module.addItems(name_prefix_items)

    def help(self):
        print("Help!!!!!")

    def about(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("aboot")
        icon_path = os.path.dirname(os.path.realpath(__file__)) + '/robot.png'
        pixmap = QPixmap(icon_path)
        logo_label = QLabel('', dlg)
        logo_label.setPixmap(pixmap)
        logo_label.setScaledContents(True)
        logo_label.setMaximumSize(360,360)
        dlg.setMinimumSize(360, 360)
        
        dlg.exec()


