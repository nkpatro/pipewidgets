from PyQt5.QtCore import QRect, Qt, QSize, QEvent
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QMenu

__author__ = 'npatro'


class PanelTopLeftCorner(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.menuRect = QRect(4, 4, 14, 14)
        self.hovered = False
        self.panelMenu = QMenu() if 0 else None

        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover)
        self.installEventFilter(self)

    def minimumSizeHint(self):
        return QSize(22, 22)

    def sizeHint(self):
        return self.minimumSizeHint()

    def paintEvent(self, event):
        painter = QPainter(self)
        palette = self.palette()
        midColor = palette.mid().color()
        highlight = palette.highlight().color()

        # background
        painter.fillRect(self.rect(), midColor.lighter())

        # menu rect
        color = highlight if self.hovered else midColor
        painter.setPen(color)
        painter.setBrush(palette.light())
        painter.drawRect(self.menuRect)
        if color == highlight:
            painter.setBrush(highlight)
            painter.drawRect(self.menuRect.adjusted(2, 2, -2, -2))

    def mouseMoveEvent(self, event):
        self.hovered = self.menuRect.contains(event.pos())
        self.repaint(self.menuRect.adjusted(-1, -1, -1, -1))

    def mousePressEvent(self, event):
        mouseClickPos = event.pos()
        if self.menuRect.contains(mouseClickPos):
            self.panelMenu.exec_(self.mapToGlobal(mouseClickPos))

    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverLeave:
            self.hovered = False
            self.repaint(self.rect())
            return True
        return False

    def createMenu(self, items):
        self.panelMenu = QMenu(self)
        for item in items:
            self.panelMenu.addAction(item)

        self.panelMenu.addSeparator()
        self.panelMenu.addAction('Close Tab')
        self.panelMenu.aboutToHide.connect(lambda: self.menuAboutToHide())

        return self.panelMenu

    def contextMenuEvent(self, event):
        pos = event.pos()
        if self.panelMenu and self.menuRect.contains(pos):
            self.panelMenu.exec_(self.mapToGlobal(pos))
            event.accept()

    def menuAboutToHide(self):
        self.hovered = False
        self.repaint(self.menuRect.adjusted(-1, -1, 1, 1))


def main():
    pass


if __name__ == '__main__':
    main()