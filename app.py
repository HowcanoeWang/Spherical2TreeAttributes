import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QAction, QOpenGLWidget, QVBoxLayout
from PyQt5.QtGui import QIcon, QBrush, QColor
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("Spherical Tree (Beta 0.1)")
        self.resize(600, 800)

        #############
        # UI Design #
        #############

        # Menu Bar UI
        menuBar = self.menuBar()
        menuFile = menuBar.addMenu("File")
        actionNew = menuFile.addAction(QIcon("./img/new.png"), "New")
        actionOpen = menuFile.addAction(QIcon("./img/open.png"), "Open")
        actionSave = menuFile.addAction(QIcon("./img/save.png"), "Save")
        actionSaveAS = menuFile.addAction("Save As")
        actionQuit = menuFile.addAction("Quit")

        # Tool Bar UI
        toolbar = self.addToolBar("File")
        toolbar.addAction(actionNew)
        toolbar.addAction(actionOpen)
        toolbar.addAction(actionSave)

        ####################
        # Connect Function #
        ####################
        actionNew.setShortcut("Ctrl+N")
        actionNew.triggered.connect(self.newProject)
        actionOpen.setShortcut("Ctrl+O")
        actionOpen.triggered.connect(self.openProject)
        actionSave.setShortcut("Ctrl+S")
        actionSave.triggered.connect(self.saveProject)


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