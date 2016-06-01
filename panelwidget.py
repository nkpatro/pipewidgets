from functools import partial

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QPainter, QBrush
from PyQt5.QtWidgets import QWidget, QGridLayout, QAction

from paneltab import PanelTab
from paneltopleftcorner import PanelTopLeftCorner
from paneltoprightcorner import PanelTopRightCorner
from tabproxystyle import TabProxyStyle

__author__ = 'npatro'

class PanelWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.container = parent
        self.tabWidget = PanelTab(self)

        self.panelSplit = pyqtSignal(object)
        self.panelFloat = pyqtSignal()
        self.panelClosed = pyqtSignal()
        self.tabClosed = pyqtSignal(QWidget, QString)
        self.panelMenuTriggered = pyqtSignal(PanelWidget, QAction)

        self.topLeftCorner = PanelTopLeftCorner(self)
        self.tabWidget.setCornerWidget(self.topLeftCorner, Qt.TopLeftCorner)
        self.topRightCorner = PanelTopRightCorner(self)
        self.tabWidget.setCornerWidget(self.topRightCorner, Qt.TopRightCorner)

        self.tabProxyStyle = TabProxyStyle('fusion')
        self.tabWidget.setStyle(self.tabProxyStyle)

        self.topRightCorner.floatClicked.connect(lambda: self.floatRequested())
        self.topRightCorner.closeClicked.connect(lambda: self.closeRequested())
        self.topRightCorner.splitClicked.connect(partial(self.splitRequested, Qt.PrimaryOrientation))

        mainLayout = QGridLayout(self)
        mainLayout.addWidget(self.tabWidget)
        mainLayout.setContentsMargins(2, 2, 2, 2)

        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.setAttribute(Qt.WA_Hover)
        self.installEventFilter(self)

    def createMenu(self, items):
        menu = self.topLeftCorner.createMenu(items)
        menu.triggered.connect(lambda: self.menuTriggered())

    def paintEvent(self, event):
        painter = QPainter(self)
        palette = self.palette()
        midColor = palette.mid().color()
        darkBrush = QBrush(midColor)

        painter.setBrush(darkBrush)
        painter.fillRect(self.rect(), midColor.lighter())

    def splitRequested(self, orientation):
        self.panelSplit.emit(orientation)

    def floatRequested(self):
        self.panelFloat.emit()

    def closeRequested(self):
        self.closeAllTabs()
        self.panelClosed.emit()

    def setContainer(self, container):
        self.container = container

    def menuTriggered(self, action):
        if action.text() == 'Close Tab':
            self.closeTab()
            return
        self.panelMenuTriggered.emit(self, action)

    def addWidget(self, widget, name):
        if widget:
            self.tabWidget.addTab(widget, name)
            self.tabWidget.setCurrentWidget(widget)

    def closeTab(self):
        index = self.tabWidget.currentIndex()
        if index == -1:
            return
        label = self.tabWidget.tabText(index)
        wid = self.tabWidget.currentWidget()
        self.tabWidget.removeTab(index)
        self.tabClosed.emit(wid, label)

    def closeAllTabs(self):
        while self.tabWidget.count():
            self.closeTab()

    def tabNames(self):
        names = list()
        tabCount =self.tabWidget.count()
        for index in range(0, tabCount):
            names.append(self.tabWidget.tabText(index))

        return names

    def currentTabIndex(self):
        return self.tabWidget.currentIndex()

    def selectTab(self, val):
        if not val == -1:
            self.tabWidget.setCurrentIndex(val)


def main():
    pass


if __name__ == '__main__':
    main()