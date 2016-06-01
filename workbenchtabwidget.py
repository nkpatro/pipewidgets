from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTabWidget, QToolBar, QPushButton, QTabBar

from workbenchwidget import WorkbenchWidget

__author__ = 'npatro'


class WorkbenchTabWidget(QTabWidget):
    def __init__(self, parent):
        # QTabWidget.__init__(parent)
        super(QTabWidget, self).__init__(parent)

        # self.setParent(parent)
        self.setMovable(True)

        toolBar = QToolBar()
        locatorAct = toolBar.addAction('Locate')
        locatorAct.triggered.connect(lambda: self.openLoctor())
        reloadAct = toolBar.addAction('Reload')
        reloadAct.triggered.connect(lambda: self.reloadPage())

        self.setCornerWidget(toolBar, Qt.TopRightCorner)

        self.tabBar().setStyleSheet('QTabBar::tab { min-width: 8ex; padding: 2px; margin-right: 4px; }')

    def newPage(self):
        wb = WorkbenchWidget(self)
        index = self.addTab(wb, 'Test')

        btnClose = QPushButton(self)
        btnClose.setText('close')
        btnClose.setStyleSheet('margin-right: 4px')

        btnClose.clicked.connect(lambda: self.closePage())

        self.tabBar().setTabButton(index, QTabBar.RightSide, btnClose)

        self.setCurrentIndex(index)
        return wb

    def closePage(self):
        print 'close page requested'

    def openLoctor(self):
        print 'haha'

    def reloadPage(self):
        print 'hehe'

    # def createViewByName(self, name):
    #     if name == 'Asset':
    #         # return self.createResourcesView()
    #         pass
    #     else:
    #         return self.pa
    #
    #
    #
    # def createResourcesView(self):
    #     resourceView = ResourceBrowser()


def main():
    pass


if __name__ == '__main__':
    main()