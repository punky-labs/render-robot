# -*- coding: utf-8 -*-
# screen/app.py

"""This module provides the Stock Screenr application."""

import sys, os

from PyQt6.QtWidgets import QApplication

import qdarktheme

from .views import Window

def main():
    os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=2"
    # Create the application
    app = QApplication(sys.argv)
    
    qdarktheme.setup_theme()
    # Create and show the main window
    win = Window()
    win.show()
    # Run the event loop
    sys.exit(app.exec())

  