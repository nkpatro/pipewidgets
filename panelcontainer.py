from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QGridLayout, QSplitter

from panelwidget import PanelWidget
from workbenchwidget import WorkbenchWidget

__author__ = 'npatro'


class PanelContainer(QWidget):
    def __init__(self, panelWin):
        super(QWidget, self).__init__()

        self.panelWindow = panelWin
        self.panelCount = 0

        self.mainLayout = QGridLayout(self)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

        self.splitter = QSplitter(self)
        self.containerParent = 0

        self.mainLayout.addWidget(self.splitter, 0, 0)

    def splitter(self):
        return self.splitter

    def addPanel(self, panel=None):
        if panel:
            panel.setParent(self)
            panel.setContainer(self)
            self.splitter.addWidget(panel)
            self.panelCount += 1
            self.updatePanelSignals(panel)
        else:
            panel = self.createPanel()
            self.splitter.addWidget(panel)
            return panel

    def addPanelSplit(self, panel, direction):
        panel = PanelWidget(self) if 0 else panel

        # Store original size
        origSize = panel.size()

        # reparent the panel
        panel.setParent(self)
        panel.setContainer(self)

        # set orientation and add the panel
        self.splitter.setOrientation(direction)
        self.splitter.addWidget(panel)

        # add another panel for split
        panel = self.createPanel()
        self.splitter.addWidget(panel)

        sizes = list()
        origSize *= 0.5
        if direction == Qt.Horizontal:
            sizes.append(origSize.width())
            sizes.append(origSize.width())
        else:
            sizes.append(origSize.height())
            sizes.append(origSize.height())

        self.splitter.setSizes(sizes)
        self.panelCount += 1

    def addContainer(self, child):
        child = PanelContainer(self) if 0 else child
        self.splitter.addWidget(child)
        child.setParentContainer(self)

    def insertContainer(self, child, index):
        child = PanelContainer(self) if 0 else child
        self.splitter.insertWidget(index, child)
        child.setParentContainer(self)

    def setParentContainer(self, parent):
        self.containerParent = parent

    def parentContainer(self):
        return self.containerParent

    def childContainers(self):
        # childContainers = list()
        # for index in range(0, self.splitter.count()):
        #     container = self.splitter.widget(index)
        #     if container:
        #         childContainers.append(container)
        return self.sortedChildren()

    def panels(self):
        # panels = list()
        # for index in range(0, self.splitter.count()):
        #     panel = self.splitter.widget(index)
        #     if panel:
        #         panels.append(panel)
        return self.sortedChildren()

    def sortedChildren(self):
        return (self.splitter.widget(index) for index in range(self.splitter.count()))

    def numberOfPanels(self):
        return self.panelCount

    def createPanel(self):
        panel = PanelWidget(self)
        panel.createMenu(WorkbenchWidget.panelNames())
        self.connectPanelSignals(panel)
        self.panelCount += 1
        return panel

    def connectPanelSignals(self, panel):
        panel = PanelWidget(self) if 0 else panel
        panel.panelSplit.connect(lambda: self.panelWindow.splitPanel())
        panel.panelFloat.connect(lambda : self.panelWindow.floatPanel())
        panel.panelClosed.connect(lambda : self.panelWindow.closePanel())
        panel.panelMenuTriggered.connect(lambda : self.panelWindow.closePanel())
        panel.tabClosed.connect(lambda : self.panelWindow.closePanel())

    def updatePanelSignals(self, panel):
        panel = PanelWidget(self) if 0 else panel
        panel.panelSplit.disconnect()
        panel.panelFloat.disconnect()
        panel.panelClosed.disconnect()
        panel.panelMenuTriggered.disconnect()
        panel.tabClosed.disconnect()




def main():
    pass


if __name__ == '__main__':
    main()