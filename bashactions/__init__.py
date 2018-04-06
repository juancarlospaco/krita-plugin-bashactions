#!/usr/bin/env python3
# -*- coding: utf-8 -*-


"""BashActions for Krita."""


import sys
import time

from datetime import datetime
from getpass import getuser
from pathlib import Path
from shutil import which
from time import sleep
from webbrowser import open_new_tab

from PyQt5.QtCore import QProcess, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import (QAbstractItemView, QAbstractScrollArea, QCheckBox,
                             QComboBox, QDialog, QDialogButtonBox, QFileDialog,
                             QFormLayout, QFrame, QHBoxLayout, QLabel,
                             QListWidget, QMessageBox, QPlainTextEdit,
                             QPushButton, QSpinBox, QVBoxLayout, QWidget)

import krita


__version__ = '1.0.0'
__license__ = ' GPLv3+ LGPLv3+ '
__author__ = ' juancarlos '
__email__ = ' juancarlospaco@gmail.com '
__url__ = 'https://github.com/juancarlospaco/krita-plugin-bashactions#krita-plugin-bashactions'
sys.dont_write_bytecode = True


_MSG0 = (
    "Type or paste your Bash commands here, 1 per line (can repeat),\n"
    "FILE1 is your 1 choosed file, FILE2 is your 2 choosed file, and so on.")


class BashActionsDialog(QDialog):

    def __init__(self):
        super().__init__()
        self.mainDialog, self.wid0, self.wid1 = QWidget(), QWidget(), QWidget()
        self.mainDialog.setWindowModality(Qt.NonModal)
        self.mainLayout = QVBoxLayout(self.mainDialog)
        self.box0, self.box1 = QHBoxLayout(self.wid0), QHBoxLayout(self.wid1)
        QLabel(self.mainDialog).setPixmap(
            QIcon.fromTheme("applications-graphics").pixmap(64))
        self.formLayout = QFormLayout()
        self.refreshButton = QPushButton("Refresh")
        self.loadButton = QPushButton("Load")
        self.mode = QComboBox()
        self.mode.addItems(("Full", "Simple"))
        self.widgetDocuments = QListWidget()
        self.widgetDocuments.setSortingEnabled(True)
        self.widgetDocuments.setToolTip("Choose 1 or more files")
        self.widgetDocuments.setSelectionMode(QAbstractItemView.MultiSelection)
        self.widgetDocuments.setSizeAdjustPolicy(
            QAbstractScrollArea.AdjustToContents)
        self.bashscript, self.preview = QPlainTextEdit(), QPlainTextEdit()
        self.bashscript.setPlaceholderText(_MSG0)
        self.bashscript.setToolTip(_MSG0)
        self.bashscript.setPlainText(Path(__file__ + ".txt").read_text())
        self.preview.setPlaceholderText(
            "Read-Only Preview of your Bash Commands before execution.")
        self.preview.setToolTip(
            "This will run exactly as seen here, line-by-line 1 per line.")
        self.preview.setReadOnly(True)
        self.log = QPlainTextEdit()
        self.log.setPlaceholderText(
            "Read-Only Log of your Bash Commands after execution.")
        self.log.setToolTip("Standard output, standard error and extra info.")
        self.log.setReadOnly(True)
        self.chrt = QCheckBox("Low CPU priority")
        self.autoquote = QCheckBox(
            "Auto add quotes if the filename or path has white spaces")
        self.asave = QCheckBox("Auto save")
        self.autoquote.setChecked(True)
        self.asave.setChecked(True)
        self.mini = QCheckBox("Minimize during execution")
        self.qq = QCheckBox("Close after execution")
        self.repeats, self.delay = QSpinBox(), QSpinBox()
        self.backoff, self.timeout = QSpinBox(), QSpinBox()
        self.repeats.setRange(1, 99)
        self.repeats.setPrefix("Repeat ")
        self.repeats.setSuffix(" times")
        self.delay.setRange(0, 99)
        self.delay.setPrefix("Delay ")
        self.delay.setSuffix(" seconds")
        self.backoff.setRange(1, 9)
        self.backoff.setPrefix("Backoff ")
        self.backoff.setSuffix(" seconds")
        self.timeout.setRange(0, 999)
        self.timeout.setValue(999)
        self.timeout.setPrefix("Timeout at ")
        self.timeout.setSuffix(" seconds")
        self.buttonBox = QDialogButtonBox(QDialogButtonBox.Ok |
                                          QDialogButtonBox.Close |
                                          QDialogButtonBox.Help)
        # self.misteryButton = QPushButton("?", self.buttonBox)
        # self.misteryButton.setFlat(True)

        self.refreshButton.clicked.connect(self.loadDocuments)
        self.loadButton.clicked.connect(self.load_script)
        self.buttonBox.accepted.connect(self.confirmButton)
        self.buttonBox.rejected.connect(self.mainDialog.close)
        self.buttonBox.helpRequested.connect(lambda: open_new_tab(__url__))

        self.mode.currentIndexChanged.connect(self.change_mode)
        self.bashscript.textChanged.connect(self.update_preview)

        self.kritaInstance = krita.Krita.instance()
        self.documentsList, self.selected = [], []
        self.process = QProcess(self)
        # self.process.error.connect(
        #     lambda: self.statusBar().showMessage("Info: Process Killed", 5000))

    def change_mode(self, index):
        for item in (self.preview, self.log, self.wid0, self.wid1, self.autoquote):
            if index == 1:
                item.hide()
                self.formLayout.labelForField(item).hide()
                self.mainDialog.resize(400, 400)
            else:
                item.show()
                self.formLayout.labelForField(item).show()
                self.mainDialog.resize(800, 800)

    def load_script(self):
        self.bashscript.setPlainText(str(Path(QFileDialog.getOpenFileName(
            self, "Open 1 Bash Script Template", "Bash_Commands_Template.sh",
            "Bash Script to use as Template (*.sh);;Plain text files (*.txt)"
            )[0]).read_text()))

    def update_preview(self):
        script = str(self.bashscript.toPlainText()).strip()
        self.selected = [a.text() for a in self.widgetDocuments.selectedItems()]
        if not len(script):
            return                             # Nothing to do yet.
        elif not len(self.selected):
            self.preview.setPlainText(script)  # We got script but no files yet.
        else:
            preview_script = script
            for index, selected_file in enumerate(self.selected):
                index, seleted_file = index + 1, str(selected_file)
                need_quote = self.autoquote.isChecked() and " " in seleted_file
                preview_script = preview_script.replace(
                    f"FILE{index}",
                    f'"{seleted_file}"' if need_quote else seleted_file)
            self.preview.setPlainText(preview_script)

    def initialize(self):
        self.loadDocuments()

        self.formLayout.addRow(QLabel("<center><h1>Bash Actions for Krita"))
        self.formLayout.addRow("Mode", self.mode)
        self.formLayout.addRow("Opened image files", self.widgetDocuments)
        self.formLayout.addRow(" ", self.refreshButton)
        self.formLayout.addRow("Commands template", self.bashscript)
        self.formLayout.addRow(" ", self.loadButton)
        self.formLayout.addRow("Preview", self.preview)
        self.formLayout.addRow("Log", self.log)

        self.box1.addWidget(self.repeats)
        self.box1.addWidget(self.delay)
        self.box1.addWidget(self.backoff)
        self.box1.addWidget(self.timeout)
        self.formLayout.addRow("Execution repeats", self.wid1)

        self.box0.addWidget(self.asave)
        self.box0.addWidget(self.chrt)
        self.box0.addWidget(self.mini)
        self.box0.addWidget(self.qq)
        self.formLayout.addRow("Execution details", self.wid0)

        self.formLayout.addRow("Filename correction", self.autoquote)
        self.mainLayout.addLayout(self.formLayout)
        self.mainLayout.addWidget(self.buttonBox)

        self.mainDialog.resize(800, 800)
        self.mainDialog.setWindowTitle("Bash Actions")
        self.mainDialog.show()
        self.mainDialog.activateWindow()
        self.bashscript.setFocus()

    def loadDocuments(self):
        self.widgetDocuments.clear()
        self.documentsList = [
            document for document in self.kritaInstance.documents()
            if document.fileName()]
        for document in self.documentsList:
            self.widgetDocuments.addItem(document.fileName())

    def confirmButton(self):
        start_time, repeat = datetime.now(), int(self.repeats.value())
        end_time = int(time.time() + int(self.timeout.value()))
        delay, backoff = int(self.delay.value()), int(self.backoff.value())
        if self.asave.isChecked():
            Path(__file__ + ".txt").write_text(str(self.bashscript.toPlainText()))
        chrt = which("chrt") if self.chrt.isChecked() else None
        commands = tuple(str(self.preview.toPlainText()).strip().splitlines())
        if not len(commands):
            return QMessageBox.warning(self, __doc__, "Nothing to execute!.")
        if self.mini.isChecked() and self.mainDialog.isVisible():
            self.mainDialog.hide()
        self.log.clear()
        self.log.setPlainText(f"""STARTED: {start_time} by user {getuser()}.
        LINES OF BASH TO EXECUTE: {len(commands)}.\nTIMEOUT: {end_time} Secs.
        SELECTED FILES: {len(self.selected)} files.\nDELAY: {delay} Secs.
        BACKOFF: {backoff} Secs.\nREPEATS: {repeat} Times.\nPRIORITY: {chrt}""")

        while repeat:
            self.log.appendPlainText(f"REPETITION: {repeat} loop.")
            for i, cmd in enumerate(commands):
                cmd = f"""{chrt} -i 0 {cmd.strip()}""" if chrt else cmd.strip()
                self.log.appendPlainText(f"{i} EXECUTING: {cmd}.")
                self.process.start(cmd)
                self.process.waitForFinished(self.timeout.value())
                self.log.appendPlainText(
                    bytes(self.process.readAllStandardError()).decode("utf-8"))
                self.log.appendPlainText(
                    bytes(self.process.readAllStandardOutput()).decode("utf-8"))
            sleep(delay)
            repeat -= 1
            delay *= backoff
            if end_time and time.time() > end_time:
                self.log.appendPlainText(f"TIMEOUT: {time.time()} > {end_time}")
                return
        else:
            self.log.appendPlainText(f"FINISHED: {datetime.now()}.")
            if self.mini.isChecked() and not self.mainDialog.isVisible():
                self.mainDialog.show()
            if self.qq.isChecked():
                self.mainDialog.close()
                self.close()


class BashActions(krita.Extension):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

    def setup(self):
        pass

    def createActions(self, window):
        action = window.createAction(self.__class__.__name__,
                                     self.__class__.__name__)
        action.setToolTip(
            "Execute Bash scripts and commands on selected documents")
        action.triggered.connect(self.initialize)

    def initialize(self):
        self.uidocumenttools = BashActionsDialog()
        self.uidocumenttools.initialize()


if not sys.platform.startswith("win"):
    Scripter.addExtension(BashActions(krita.Krita.instance()))
