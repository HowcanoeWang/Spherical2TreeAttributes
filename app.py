import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from PIL import Image


class MainWindow(QMainWindow):
    '''
    MainFrame
    |-- MenuBar
    |-- ProjectPanel
    |-- TabPanel
         |-- IndividualTab
         |-- BasalAreaTab
         |-- PlantFractionTab
    '''

    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)

        self.setWindowTitle("Spherical2TreeAttributes (Beta 0.1)")
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        screen = QDesktopWidget().screenGeometry()
        self.resize(screen.width(), screen.height())
        self.move(0,0)
        self.setWindowIcon(QIcon('./img/logo.png'))

        self.setupUI()
        self.functionConnector()

        #self.glWidget = GLWidget()

    def setupUI(self):
        # Menu Bar UI
        self.menuBar = MenuBar()

        # Project Panel UI
        self.projectPanel = ProjectPanel()

        # Tabs UI
        self.tabs = QTabWidget()

        self.indTab = IndividualTreePanel()
        self.baTab = BasalAreaPanel()
        self.pfTab = PlantFractionPanel()

        self.tabs.addTab(self.indTab, 'Individual DBH|HT')
        self.tabs.addTab(self.baTab, 'Basal Area')
        self.tabs.addTab(self.pfTab, 'Plant Fraction')

        #self.tabs.setTabPosition(QTabWidget.West)
        #self.tabs.setStyleSheet("QTabBar::tab {width: 50px}")

        self.tabs.setStyleSheet("QTabBar::tab {height: 50px}")

        # Pack these UIs together
        self.mainWidget = QWidget()

        wl = QHBoxLayout(self.mainWidget)

        layout = QVBoxLayout()
        layout.addWidget(self.menuBar, stretch=1)
        layout.addLayout(self.projectPanel, stretch=7)

        wl.addLayout(layout, stretch=1)
        wl.addWidget(self.tabs, stretch=3)

        self.setCentralWidget(self.mainWidget)

    def functionConnector(self):
        self.menuBar.actionNew.clicked.connect(self.newProject)
        self.menuBar.actionOpen.clicked.connect(self.openProject)
        self.menuBar.actionSave.clicked.connect(self.saveProject)
        self.menuBar.actionQuit.clicked.connect(self.quitSoftware)

    def newProject(self):
        self.updateStatus("add new project")

    def openProject(self):
        self.updateStatus("open project")

    def saveProject(self):
        self.updateStatus("save project")

    def quitSoftware(self):
        qApp = QApplication.instance()
        qApp.quit()

    def updateStatus(self, string):
        if len(string) >= 50:
            self.projectPanel.statusBar.setText(string[:50] + '...')
        else:
            self.projectPanel.statusBar.setText(string)


class MenuBar(QTabWidget):

    def __init__(self, parent=None):
        super(QTabWidget, self).__init__(parent)

        self.btnStyle='''
        QPushButton {
            background-color:white; 
            border: none;
            padding: 5px;
            } 
        QPushButton:hover {
            border:1px solid;
            }
        '''
        self.setupUI()

    def setupUI(self):
        self.fileTab = QWidget()
        self.plotTab = QWidget()
        self.helpTab = QWidget()

        self.addTab(self.fileTab, 'File')
        self.addTab(self.plotTab, 'Plot')
        self.addTab(self.helpTab, 'Help')

        self.setStyleSheet("QTabBar::tab { height: 50px}")

        # File Tab
        self.fileLayout = QGridLayout()

        self.actionNew = QPushButton("&New")
        self.actionNew.setIcon(QIcon("./img/new.png"))
        self.actionNew.setShortcut("Ctrl+N")
        self.actionNew.setStyleSheet(self.btnStyle)

        self.actionOpen = QPushButton("&Open")
        self.actionOpen.setIcon(QIcon("./img/open.png"))
        self.actionOpen.setShortcut("Ctrl+O")
        self.actionOpen.setStyleSheet(self.btnStyle)

        self.actionSave = QPushButton("&Save")
        self.actionSave.setEnabled(False)
        self.actionSave.setIcon(QIcon("./img/save.png"))
        self.actionSave.setShortcut("Ctrl+S")
        self.actionSave.setStyleSheet(self.btnStyle)

        self.actionSaveAs = QPushButton("Save As")
        self.actionSaveAs.setEnabled(False)
        self.actionSaveAs.setIcon(QIcon("./img/save.png"))
        self.actionSaveAs.setShortcut("Ctrl+Alt+S")
        self.actionSaveAs.setStyleSheet(self.btnStyle)

        self.actionExport = QPushButton("Export")
        self.actionExport.setEnabled(False)
        self.actionExport.setIcon(QIcon("./img/export.png"))
        self.actionExport.setStyleSheet(self.btnStyle)

        self.actionQuit = QPushButton("Quit")
        self.actionQuit.setEnabled(True)
        self.actionQuit.setIcon(QIcon("./img/quit.png"))
        self.actionQuit.setStyleSheet(self.btnStyle)

        self.fileLayout.addWidget(self.actionNew, 0, 0, alignment=Qt.AlignLeft)
        self.fileLayout.addWidget(self.actionOpen, 1, 0, alignment=Qt.AlignLeft)
        self.fileLayout.addWidget(self.actionSave, 0, 1, alignment=Qt.AlignLeft)
        self.fileLayout.addWidget(self.actionSaveAs, 1,1, alignment=Qt.AlignLeft)
        self.fileLayout.addWidget(self.actionExport, 0, 2, alignment=Qt.AlignLeft)
        self.fileLayout.addWidget(self.actionQuit, 1, 2, alignment=Qt.AlignLeft)
        #self.fileLayout.addStretch(0)

        self.fileTab.setLayout(self.fileLayout)

        # Plot Tab
        self.plotLayout = QGridLayout()

        self.actionAdd = QPushButton("Single")
        self.actionAdd.setIcon(QIcon("./img/add.png"))
        self.actionAdd.setStyleSheet(self.btnStyle)

        self.actionBatchAdd = QPushButton("Batch")
        self.actionBatchAdd.setIcon(QIcon("./img/add.png"))
        self.actionBatchAdd.setStyleSheet(self.btnStyle)

        #self.labelAdd = QLabel('Add')
        #self.labelAdd.setAlignment(Qt.AlignHCenter)

        self.actionEditName = QPushButton("Name")
        self.actionEditName.setIcon(QIcon("./img/edit.png"))
        self.actionEditName.setStyleSheet(self.btnStyle)

        self.actionEditEle = QPushButton("Elevation")
        self.actionEditEle.setIcon(QIcon("./img/edit.png"))
        self.actionEditEle.setStyleSheet(self.btnStyle)

        self.actionEditImg = QPushButton("Image")
        self.actionEditImg.setIcon(QIcon("./img/edit.png"))
        self.actionEditImg.setStyleSheet(self.btnStyle)

        #self.labelEdit = QLabel('Edit')
        #self.labelEdit.setAlignment(Qt.AlignHCenter)

        self.actionDel = QPushButton("Delete")
        self.actionDel.setIcon(QIcon("./img/delete.png"))
        self.actionDel.setStyleSheet(self.btnStyle)

        self.plotLayout.addWidget(self.actionAdd, 0, 0, alignment=Qt.AlignLeft)
        self.plotLayout.addWidget(self.actionBatchAdd, 1, 0, alignment=Qt.AlignLeft)
        #self.plotLayout.addWidget(self.labelAdd, 3, 0)
        self.plotLayout.addWidget(self.actionEditName, 0, 1, alignment=Qt.AlignLeft)
        self.plotLayout.addWidget(self.actionEditEle, 1, 1, alignment=Qt.AlignLeft)
        self.plotLayout.addWidget(self.actionEditImg, 0, 2, alignment=Qt.AlignLeft)
        #self.plotLayout.addWidget(self.labelEdit, 3, 1)

        self.plotLayout.addWidget(self.actionDel, 1, 2, alignment=Qt.AlignLeft)

        self.plotTab.setLayout(self.plotLayout)

        # Help Tab
        self.helpLayout = QGridLayout()

        self.actionApp = QPushButton("User Manual")
        self.actionApp.setIcon(QIcon("./img/file.png"))
        self.actionApp.setStyleSheet(self.btnStyle)

        self.actionAuthor = QPushButton("About Author")
        self.actionAuthor.setIcon(QIcon("./img/file.png"))
        self.actionAuthor.setStyleSheet(self.btnStyle)

        self.actionLab = QPushButton("About Lab")
        self.actionLab.setIcon(QIcon("./img/file.png"))
        self.actionLab.setStyleSheet(self.btnStyle)

        self.helpLayout.addWidget(self.actionApp, 0, 0, alignment=Qt.AlignLeft)
        self.helpLayout.addWidget(self.actionAuthor, 0, 1, alignment=Qt.AlignLeft)
        self.helpLayout.addWidget(self.actionLab, 0, 2, alignment=Qt.AlignLeft)
        #self.helpLayout.addStretch(0)

        self.helpTab.setLayout(self.helpLayout)

class ProjectPanel(QVBoxLayout):
    '''
    ProjectPanel
    |-- ImageInfo(QTreeWidget)
    |-- PlotInfo(QTableWidget)
    |-- ControlGroups(HorizontalLayout)
        |-- AddPlot
        |-- DelPlot
        |-- EditPlot
    '''

    def __init__(self, parent=None):
        super(QVBoxLayout, self).__init__(parent)
        self.setupUI()

    def setupUI(self):
        # Image Info Panel
        self.projectTree = QTreeWidget()
        self.projectTree.setColumnCount(2)
        self.projectTree.setHeaderLabels(['Plot', 'Elevation', 'Image File Path'])

        plot1 = QTreeWidgetItem(self.projectTree)
        plot1.setText(0, 'Plot1')

        img1 = QTreeWidgetItem(plot1)
        img1.setText(0, 'Upper')
        img1.setText(1, '2.6m')
        img1.setText(2, 'D:/Test/test2.jpg')
        img1.setIcon(0, QIcon('./img/img.png'))

        img2 = QTreeWidgetItem(plot1)
        img2.setText(0, 'Lower')
        img2.setText(1, '1.6m')
        img2.setText(2, 'D:/Test/test1.jpg')
        img2.setIcon(0, QIcon('./img/img.png'))
        
        #for i in range(0,3):
        #    self.projectTree.resizeColumnToContents(i) 
        self.projectTree.header().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.projectTree.header().setStretchLastSection(True)
        self.projectTree.expandAll()
        
        # Plot Info Panel
        self.projectTableView = QTableView()
        
        self.projectModel = QStandardItemModel(0, 5)
        self.projectModel.setHorizontalHeaderLabels(['Plot', 'meanDBH', 'meanHT', 'standBA', 'PF'])
        
        self.projectTableView.setModel(self.projectModel)
        self.projectTableView.resizeColumnsToContents()
        self.projectTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        # Control Panel
        # self.projectButtonLayout = QHBoxLayout()
        # self.addPlot = QPushButton('Add')
        # self.delPlot = QPushButton('Del')
        # self.editPlot = QPushButton('Edit')
        # self.projectButtonLayout.addWidget(self.addPlot)
        # self.projectButtonLayout.addWidget(self.delPlot)
        # self.projectButtonLayout.addWidget(self.editPlot)
        
        self.statusBar = QLabel('[AI]: Hello World!')

        self.addWidget(QLabel('Plot Management'))
        self.addWidget(self.projectTree, stretch=2)
        #self.addLayout(self.projectButtonLayout)
        self.addWidget(QLabel('Plot Overview'))
        self.addWidget(self.projectTableView, stretch=1)
        self.addWidget(self.statusBar)
        
        
class IndividualTreePanel(QWidget):
    '''
    IndividualTreePanel
    |-- OpenGLContainer（VerticalLayout）
        |-- UpperHorizontalLayout
        |   |-- VerticalBar（Zenith Angle）
        |   |-- OpenGLPanel（VerticalLayout）
        |   |    |-- UpperGL
        |   |    |-- LowerGL
        |   |-- VerticalBar（Zoom in/out）
        |   |-- HorzontalBar
        |-- VertialLayout
             |-- TreeInfoTable
             |-- ButtonHorizontalLayout
                  |-- AddBtn
                  |-- DelBtn
    '''

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)

        self.setupUI()
        self.functionConnector()

    def setupUI(self):
        self.layout = QHBoxLayout(self)
        
        ### OpenGLCtrl
        self.openglCtrlLayout = QVBoxLayout()
        
        self.xSlider = QSlider(Qt.Horizontal)
        self.xSlider.setMinimum(0)
        self.xSlider.setMaximum(360)
        self.xSlider.setSingleStep(10)
        self.xSlider.setValue(180)
        self.xSlider.setTickPosition(QSlider.TicksBelow)
        self.xSlider.setTickInterval(10)
        
        self.ySlider = QSlider(Qt.Vertical)
        self.ySlider.setMinimum(-90)
        self.ySlider.setMaximum(90)
        self.ySlider.setSingleStep(5)
        self.ySlider.setValue(0)
        self.ySlider.setTickPosition(QSlider.TicksLeft)
        self.ySlider.setTickInterval(5)
        
        self.zoomSlider = QSlider(Qt.Vertical)
        self.zoomSlider.setMinimum(100)
        self.zoomSlider.setMaximum(500)
        self.zoomSlider.setSingleStep(10)
        self.zoomSlider.setValue(100)
        self.zoomSlider.setTickPosition(QSlider.TicksRight)
        self.zoomSlider.setTickInterval(10)

        self.glUp = GLWidget()
        self.glUp.setEnabled(True)
        #self.glDown = QOpenGLWidget()
        self.glDown = GLWidget()
        self.glDown.setEnabled(True)

        self.upperImgName = QLabel('Upper Image (2.6m): [D:/test/test2.jpg]')
        self.lowerImgName = QLabel('Lower Image (1.6m): [D:/test/test1.jpg]')
        self.line = QFrame()
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        
        self.openglLayout = QVBoxLayout()
        self.openglLayout.addWidget(self.upperImgName, stretch=1)
        self.openglLayout.addWidget(self.glUp, stretch=20)
        self.openglLayout.addWidget(self.line)
        self.openglLayout.addWidget(self.lowerImgName, stretch=1)
        self.openglLayout.addWidget(self.glDown, stretch=20)
        
        self.openglLR = QHBoxLayout()
        
        self.ySliderLabels = QVBoxLayout()
        self.ySliderLabels.addWidget(QLabel('90°'), 1, Qt.AlignTop)
        self.ySliderLabels.addWidget(QLabel('Zenith\nAngle'), 10, Qt.AlignVCenter)
        self.ySliderLabels.addWidget(QLabel('-90°'), 1, Qt.AlignBottom)
        
        self.zoomSliderLabels = QVBoxLayout()
        self.zoomSliderLabels.addWidget(QLabel('500%'), 1, Qt.AlignTop)
        self.zoomSliderLabels.addWidget(QLabel('Zoom\nRatio'), 10, Qt.AlignVCenter)
        self.zoomSliderLabels.addWidget(QLabel('100%'), 1, Qt.AlignBottom)
        
        self.openglLR.addLayout(self.ySliderLabels,2)
        self.openglLR.addWidget(self.ySlider,1)
        self.openglLR.addLayout(self.openglLayout,40)
        self.openglLR.addWidget(self.zoomSlider,1)
        self.openglLR.addLayout(self.zoomSliderLabels, 2)
        
        self.openglCtrlLayout.addLayout(self.openglLR)
        self.openglCtrlLayout.addWidget(self.xSlider)
        
        self.xSliderLabels = QHBoxLayout()
        self.xSliderLabels.addWidget(QLabel('0°'), 1, Qt.AlignLeft)
        self.xSliderLabels.addWidget(QLabel('Azimuth Angle'), 10, Qt.AlignCenter)
        self.xSliderLabels.addWidget(QLabel('360°'), 1, Qt.AlignRight)
        
        self.openglCtrlLayout.addLayout(self.xSliderLabels)

        ## Results Layouts
        self.individualTreeInfoLayout = QVBoxLayout()
        ### IndividualModel
        self.individualModel = QStandardItemModel(0, 4)
        self.individualModel.setHorizontalHeaderLabels(['Distance', '△H', 'DBH', 'HT'])
        
        self.individualTableView = QTableView()
        self.individualTableView.setModel(self.individualModel)
        self.individualTableView.resizeColumnsToContents()
        self.individualTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        ### DiameterMdoel
        self.diameterModel = QStandardItemModel(0,2)
        self.diameterModel.setHorizontalHeaderLabels(['No.', 'Diameter', 'at height'])

        self.diameterTableView = QTableView()
        self.diameterTableView.setModel(self.diameterModel)
        self.diameterTableView.resizeColumnsToContents()
        self.diameterTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.individualTreeInfoLayout.addWidget(QLabel('Individual Tree Panel'))
        self.individualTreeInfoLayout.addWidget(self.individualTableView, stretch=2)
        self.individualTreeInfoLayout.addWidget(QLabel('Diameter Panel'))
        self.individualTreeInfoLayout.addWidget(self.diameterTableView, stretch=1)

        self.layout.addLayout(self.openglCtrlLayout, stretch=2)
        self.layout.addLayout(self.individualTreeInfoLayout, stretch=1)

    def functionConnector(self):
        self.xSlider.valueChanged.connect(self.glUp.setXRotation)
        self.xSlider.valueChanged.connect(self.glDown.setXRotation)
        self.glUp.xRotationChanged.connect(self.xSlider.setValue)
        self.glDown.xRotationChanged.connect(self.xSlider.setValue)

        self.ySlider.valueChanged.connect(self.glUp.setYRotation)
        self.ySlider.valueChanged.connect(self.glDown.setYRotation)
        self.glUp.yRotationChanged.connect(self.ySlider.setValue)
        self.glDown.yRotationChanged.connect(self.ySlider.setValue)

        #self.zSlider.valueChanged.connect(self.glUp.setZRotation)
        #self.zSlider.valueChanged.connect(self.glDown.setZRotation)
        #self.glUp.zRotationChanged.connect(self.zSlider.setValue)
        #self.glDown.zRotationChanged.connect(self.zSlider.setValue)

    def setXRotation(self):
        print('setXroataion')

    def setYRotation(self):
        print('setYroataion')

    def setZRotation(self):
        print('setZroataion')


class GLWidget(QOpenGLWidget):
    xRotationChanged = pyqtSignal(int)
    yRotationChanged = pyqtSignal(int)
    zRotationChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(QOpenGLWidget, self).__init__(parent)

        self.object = 0
        self.xRot = 0
        self.yRot = 0
        self.zRot = 0

    def getOpenglInfo(self):
        info = f"Renderer: {glGetString(GL_RENDERER)}. Version:{glGetString(GL_VERSION)}"
        return info

    def setXRotation(self, angle):
        window.updateStatus(f'XRoate:{angle}')
        '''
        angle = self.normalizeAngle(angle)
        if angle != self.xRot:
            self.xRot = angle
            self.xRotationChanged.emit(angle)
            self.update()
        '''

    def setYRotation(self, angle):
        window.updateStatus(f'YRoate:{angle}')
        '''
        angle = self.normalizeAngle(angle)
        if angle != self.yRot:
            self.yRot = angle
            self.yRotationChanged.emit(angle)
            self.update()
        '''

    def setZRotation(self, angle):
        window.updateStatus(f'ZRoate:{angle}')
        '''
        angle = self.normalizeAngle(angle)
        if angle != self.zRot:
            self.zRot = angle
            self.zRotationChanged.emit(angle)
            self.update()
        '''

    def mousePressEvent(self, event):
        self.lastPos = event.pos()
        window.updateStatus(f'LastPosition:{self.lastPos}')

    def mouseMoveEvent(self, event):
        dx = event.x() - self.lastPos.x()
        dy = event.y() - self.lastPos.y()
        '''
        if event.buttons() & Qt.LeftButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setYRotation(self.yRot + 8 * dx)
        elif event.buttons() & Qt.RightButton:
            self.setXRotation(self.xRot + 8 * dy)
            self.setZRotation(self.zRot + 8 * dx)
        '''
        self.lastPos = event.pos()
        window.updateStatus(f'dx:{dx}, dy:{dy}')

    def initializeGL(self):
        window.updateStatus(self.getOpenglInfo())
        

class BasalAreaPanel(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        
        baLayout = QHBoxLayout()
        baLayout.addWidget(QLabel('Under Construction'))
        self.setLayout(baLayout)
        
        
class PlantFractionPanel(QWidget):

    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        
        pfLayout = QHBoxLayout()
        pfLayout.addWidget(QLabel('Under Construction'))
        self.setLayout(pfLayout)
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setStyleSheet("QMainWindow {background: rgba(255,255,255,230);}");
    window.showMaximized()
    sys.exit(app.exec_())