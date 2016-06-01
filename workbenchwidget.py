from PyQt5.QtWidgets import QWidget, QGridLayout

from applicationwidget import ApplicationWidget
from contextwidget import ContextWidget
from movieplayer import MoviePlayer
from notesview import NotesView
from taskbrowser import TaskBrowser

__author__ = 'npatro'


class WorkbenchWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        self.mainLayout = QGridLayout()
        self.mainLayout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.mainLayout)

        self.moviePlayer = MoviePlayer(self)
        self.notesView = NotesView(self)
        self.taskBrowser = TaskBrowser(self)
        self.applicationWidget = ApplicationWidget(self)
        self.contextWidget = ContextWidget(self)

        panelWidgets = dict()
        panelWidgets['Movie Player'] = self.moviePlayer
        panelWidgets['Notes'] = self.notesView
        panelWidgets['Task'] = self.taskBrowser
        panelWidgets['Applications'] = self.applicationWidget
        panelWidgets['Context'] = self.contextWidget

        for wid in panelWidgets.values():
            wid.hide()

    @staticmethod
    def panelNames():
        return ['Asset',
                'Application',
                'Context',
                'Info',
                'Localization',
                'Movie Preview',
                'Notes',
                'Pipeline',
                'Task',
                'Workbook Summary']


def main():
    pass


if __name__ == '__main__':
    main()