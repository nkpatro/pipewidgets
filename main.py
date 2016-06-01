import sys
from PyQt5.QtWidgets import QApplication

from workbenchwindow import WorkbenchWindow

__author__ = 'npatro'


def main():
    app = QApplication(sys.argv)
    wb = WorkbenchWindow()
    wb.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()