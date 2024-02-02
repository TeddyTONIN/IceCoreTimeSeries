# Copyright are given to LSCE and CentraleSupélec

import sys
from PyQt5.QtWidgets import QApplication
from home import Home

def main():
    """Launch the software"""
    app = QApplication.instance()
    if not app:
        app = QApplication(sys.argv)
    home_window = Home()
    home_window.show() 
    app.exec()
    

if __name__ == '__main__':
    main()