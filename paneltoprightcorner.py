from PyQt5.QtCore import Qt, QRect, QSize, QPoint, pyqtSignal, QEvent
from PyQt5.QtGui import QPainter, QPalette, QPen
from PyQt5.QtWidgets import QWidget

__author__ = 'npatro'

class MOUSE_HOVER():
    HOVER_NONE = 0
    HOVER_VSPLIT = 1
    HOVER_HSPLIT = 2
    HOVER_FLOAT = 3
    HOVER_CLOSE = 4


class PanelTopRightCorner(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.vSplitRect = QRect()
        self.hSplitRect = QRect()
        self.floatRect = QRect()
        self.closeRect = QRect()

        self.closeClicked = pyqtSignal()
        self.floatClicked = pyqtSignal()
        self.splitClicked = pyqtSignal()

        self.mouseHoverState = MOUSE_HOVER.HOVER_NONE
        self.mouseClickPos = QPoint()
        self.setMouseTracking(True)
        self.setAttribute(Qt.WA_Hover)
        self.installEventFilter(self)

    def minimumSizeHint(self):
        w = 4
        w += self.vSplitRect.width() + 6
        w += self.hSplitRect.width() + 6
        w += self.floatRect.width() + 6
        w += self.closeRect.width() + 6
        s = QSize(w, 22)
        return s

    def sizeHint(self):
        return self.minimumSizeHint()

    def mouseMoveEvent(self, event):
        p = event.pos()
        r = QRect()

        if self.vSplitRect.contains(p):
            self.mouseHoverState = MOUSE_HOVER.HOVER_VSPLIT
        elif self.hSplitRect.contains(p):
            self.mouseHoverState = MOUSE_HOVER.HOVER_HSPLIT
        elif self.closeRect.contains(p):
            self.mouseHoverState = MOUSE_HOVER.HOVER_CLOSE
        elif self.floatRect.contains(p):
            self.mouseHoverState = MOUSE_HOVER.HOVER_FLOAT
        else:
            self.mouseHoverState = MOUSE_HOVER.HOVER_NONE

        self.repaint(r.adjusted(-1, -1, 1, 1))

    def mousePressEvent(self, event):
        self.mouseClickPos = event.pos()
        if self.closeRect.contains(self.mouseClickPos):
            self.closeClicked.emit()
        elif self.floatRect.contains(self.mouseClickPos):
            self.floatClicked.emit()
        elif self.vSplitRect.contains(self.mouseClickPos):
            self.splitClicked.emit(Qt.Vertical)
        elif self.hSplitRect.contains(self.mouseClickPos):
            self.splitClicked.emit(Qt.Horizontal)
            self.mouseHoverState = MOUSE_HOVER.HOVER_NONE

    def paintEvent(self, event):
        painter = QPainter(self)
        palette = self.palette()
        midColor = palette.mid().color()
        highlight = palette.highlight().color()

        # background
        painter.fillRect(self.rect(), midColor.lighter())

        # float rect
        color = highlight if self.mouseHoverState == MOUSE_HOVER.HOVER_FLOAT else midColor
        painter.setPen(color)
        painter.setBrush(palette.light())
        painter.drawRect(self.floatRect)
        painter.setBrush(highlight if color == highlight else midColor)
        painter.drawRect(self.floatRect.adjusted(4, 2, -2, -4))

        # hsplit rect
        color = highlight if self.mouseHoverState == MOUSE_HOVER.HOVER_HSPLIT else midColor
        painter.setPen(color)
        painter.setBrush(palette.light())
        painter.drawRect(self.hSplitRect)
        painter.setBrush(highlight if color == highlight else midColor)
        painter.drawRect(self.hSplitRect.adjusted(2, 2, -6, -2))

        # float rect
        color = highlight if self.mouseHoverState == MOUSE_HOVER.HOVER_VSPLIT else midColor
        painter.setPen(color)
        painter.setBrush(palette.light())
        painter.drawRect(self.vSplitRect)
        painter.setBrush(highlight if color == highlight else midColor)
        painter.drawRect(self.vSplitRect.adjusted(2, 2, -2, -6))

        # float rect
        color = highlight if self.mouseHoverState == MOUSE_HOVER.HOVER_CLOSE else midColor
        painter.setPen(color)
        painter.setBrush(palette.light())
        painter.drawRect(self.closeRect)
        painter.translate(self.closeRect.topLeft())
        painter.setPen(QPen(color, 1.5))
        painter.drawLine(QPoint(4, 4), QPoint(9, 9))
        painter.drawLine(QPoint(4, 9), QPoint(9, 4))
        painter.resetTransform()

    def resizeEvent(self, event):
        w = self.width()
        self.hSplitRect = QRect(w-72, 4, 12, 12)
        self.vSplitRect = QRect(w-54, 4, 12, 12)
        self.floatRect = QRect(w-36, 4, 12, 12)
        self.closeRect = QRect(w-18, 4, 12, 12)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.HoverLeave:
            self.mouseHoverState = MOUSE_HOVER.HOVER_NONE
            self.repaint(self.rect())
            return True
        return False

def main():
    pass


if __name__ == '__main__':
    main()