from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QMenu

from workbenchtabwidget import WorkbenchTabWidget

__author__ = 'npatro'


class WorkbenchWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self)

        self.mainMenu = QMenu(' Window ')
        layMenu1 = self.mainMenu.addAction('Default Layout')
        layMenu1.triggered.connect(lambda: self.loadLayoutPreset())
        self.mainMenu.addSeparator()
        layMenu2 = self.mainMenu.addAction('Import Layout')
        layMenu2.triggered.connect(lambda: self.importLayoutPreset())
        layMenu3 = self.mainMenu.addAction('Save Layout')
        layMenu3.triggered.connect(lambda: self.saveLayoutPreset())

        self.menuBar().addMenu(self.mainMenu)
        self.mainMenu.setLayoutDirection(Qt.LeftToRight)
        self.menuBar().setLayoutDirection(Qt.RightToLeft)

        self.tabWidget = WorkbenchTabWidget(self)
        self.setCentralWidget(self.tabWidget)

        self.tabWidget.newPage()

    def loadLayoutPreset(self):
        print 'loadLayoutPreset'

    def importLayoutPreset(self):
        print 'importLayoutPreset'

    def saveLayoutPreset(self):
        print 'saveLayoutPreset'


def main():
    pass


if __name__ == '__main__':
    main()