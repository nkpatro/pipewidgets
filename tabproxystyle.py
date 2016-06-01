from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QProxyStyle, QTabWidget, QStyle

__author__ = 'npatro'


class TabProxyStyle(QProxyStyle):
    def __init__(self, key):
        QProxyStyle.__init__(key)

    def subElementRect(self, element, option, widget):
        rect = QProxyStyle.subElementRect(element, option, widget)
        tabWidget = QTabWidget(widget)

        if not tabWidget:
            if element == QStyle.SE_TabWidgetLeftCorner:
                if not tabWidget.count():
                    rect.setHeight(tabWidget.cornerWidget(Qt.TopLeftCorner).height())
            elif element == QStyle.SE_TabWidgetRightCorner:
                if not tabWidget.count():
                    rect.setHeight(tabWidget.cornerWidget(Qt.TopRightCorner).height())
            if element == QStyle.SE_TabWidgetTabPane:
                if not tabWidget.count():
                    rect.setTop(tabWidget.cornerWidget(Qt.TopLeftCorner).height())

        return rect


def main():
    pass


if __name__ == '__main__':
    main()