import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QOpenGLWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("Spherical2TreeAttributes (Beta 0.1)")
        self.resize(600, 800)
        self.setWindowIcon(QIcon('./img/logo.png'))

        self.setupUI()
        self.functionConnector()

    def setupUI(self):
        # Menu Bar UI
        self.menu = self.menuBar()
        self.menuFile = self.menu.addMenu("File")
        self.actionNew = self.menuFile.addAction(QIcon("./img/new.png"), "New")
        self.actionOpen = self.menuFile.addAction(QIcon("./img/open.png"), "Open")
        self.actionSave = self.menuFile.addAction(QIcon("./img/save.png"), "Save")
        self.actionSaveAS = self.menuFile.addAction("Save As")
        self.actionQuit = self.menuFile.addAction("Quit")

        # Tool Bar UI
        self.toolbar = self.addToolBar("File")
        self.toolbar.addAction(self.actionNew)
        self.toolbar.addAction(self.actionOpen)
        self.toolbar.addAction(self.actionSave)

    def functionConnector(self):
        self.actionNew.setShortcut("Ctrl+N")
        self.actionNew.triggered.connect(self.newProject)
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.triggered.connect(self.openProject)
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.triggered.connect(self.saveProject)

    def newProject(self):
        print("add new project")

    def openProject(self):
        print("open project")

    def saveProject(self):
        print("save project")



if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())