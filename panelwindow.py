from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMenu, QAction

from panelcontainer import PanelContainer
from panelwidget import PanelWidget
from workbenchwidget import WorkbenchWidget

__author__ = 'npatro'


class PanelWindow(QMainWindow):
    def __init__(self, parent, panel=None):
        QMainWindow.__init__(self)

        self.workbenchWidget = WorkbenchWidget(self) if 0 else parent
        self.resized = pyqtSignal(object)

        center = QWidget()
        self.mainLayout = QVBoxLayout(center)
        self.setCentralWidget(center)

        self.contextMenu = QMenu(self)
        panelBin = self.contextMenu.addAction('Create Panel Bin')
        panelBin.triggered.connect(lambda: self.createPanelContainer())

        if panel:
            container = PanelContainer(self)
            container.addPanel(panel)
            self.mainLayout.addWidget(container)

        self.mainLayout.setStretch(0, 10)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        center.setLayout(self.mainLayout)
        self.mainLayout.setContentsMargins(0, 0, 0, 0)

    def contextMenuEvent(self, event):
        if self.centralWidget().children().count() < 2:
            pos = event.pos()
            self.contextMenu.exec_(self.mapToGlobal(pos))
            event.accept()

    def closeEvent(self, event):
        panels = self.findChildren()
        for panel in panels:
            panel.closeAllTabs()

        QMainWindow.closeEvent(event)
        self.deleteLater()

    def resizeEvent(self, event):
        self.resized.emit(event)
        QMainWindow.resizeEvent(event)

    def createPanelContainer(self):
        container = PanelContainer(self)
        container.addPanel()
        self.mainLayout.insertWidget(0, container)

    def splitPanel(self, panel, direction):
        panel = PanelWidget(self) if 0 else panel
        container = PanelContainer(self) if 0 else panel.container
        splitParent = container.splitter()
        index = splitParent.indexOf(panel)

        # set orientation on initial split
        if splitParent.count() == 1:
            splitParent.setOrientation(direction)

        # store initial panel size
        sizes = splitParent.sizes()
        if splitParent.orientation() == direction:
            # if the direction match,insert new panel into current splitParent
            panel = container.createPanel()
            splitParent.insertWidget(index + 1, panel)

            # current panel shares half the space with the new panel
            half = sizes.at(index) / 2
            sizes[index] = half
            sizes.insert(index, half)
            splitParent.setSizes(sizes)
        else:
            newContainer = PanelContainer(self)
            newContainer.setParentContainer(container)
            newContainer.addPanelSplit(panel, direction)

            splitParent.insertWidget(index, newContainer)
            container.updatePanelCount(-1)

            splitParent.setSizes(sizes)

    def floatPanel(self, panel):
        panel = PanelWidget(self) if 0 else panel

        pSize = panel.size()
        container = panel.container
        pos = container.mapToGlobal(panel.pos())

        panel.setParent(0)
        container.updatePanelCount(-1)
        self.deleteContainer(container)

        # create a window with panel
        window = PanelWindow(self.workbench(), panel)
        window.setWindowFlags(window.windowFlags() | Qt.Tool)
        window.setGeometry(pos.x(), pos.y(), pSize.width(), pSize.height())
        window.show()

    def closePanel(self, panel):
        panel = PanelWidget(self) if 0 else panel
        container = panel.container
        panel.close()
        container.updatePanelCount(-1)
        self.deleteContainer(container)

    def deleteContainer(self, container):
        container = PanelContainer(self) if 0 else container

        if container.numberOfPanels():
            return

        parentContainer = container.parentContainer()
        childContainers = container.childContainers()
        if childContainers.count():
            if parentContainer:
                index = parentContainer.splitter().indexOf(container)
                for cc in childContainers:
                    parentContainer.insertContainer(cc, index)
            else:
                if container.parentWidget() == self.centralWidget():
                    return

        container.setParent(0)
        container.deleteLater()

        if parentContainer and parentContainer.isEmpty():
            self.deleteContainer(parentContainer)

    def panelMenuTriggered(self, panel, action):
        panel = PanelWidget(self) if 0 else panel
        action = QAction() if 0 else action
        name = action.text()
        panel.addWidget(self.workbenchWidget.createViewByName(name), name)




def main():
    pass


if __name__ == '__main__':
    main()