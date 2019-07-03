import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from qt import GLWidget


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
        self.resize(600, 800)
        self.setWindowIcon(QIcon('./img/logo.png'))

        self.setupUI()
        self.functionConnector()
        
        self.glWidget = GLWidget()

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
        
        self.tabs.setTabPosition(QTabWidget.West)
        self.tabs.setStyleSheet("QTabBar::tab {width: 50px}")

        # Pack these UIs together
        self.mainWidget = QWidget()
        layout = QVBoxLayout(self.mainWidget)
        wl = QHBoxLayout()
        wl.addLayout(self.projectPanel, stretch=1)
        wl.addWidget(self.tabs, stretch=3)
        
        layout.addWidget(self.menuBar, stretch=1)
        layout.addLayout(wl, stretch=19)

        self.setCentralWidget(self.mainWidget)

    def functionConnector(self):
        self.menuBar.actionNew.clicked.connect(self.newProject)
        self.menuBar.actionOpen.clicked.connect(self.openProject)
        self.menuBar.actionSave.clicked.connect(self.saveProject)

    def newProject(self):
        print("add new project")

    def openProject(self):
        print("open project")

    def saveProject(self):
        print("save project")
        

class MenuBar(QTabWidget):

    def __init__(self, parent=None):
        super(QTabWidget, self).__init__(parent)
        
        self.btnStyle='''
        QPushButton {
            background-color:white; 
            border:0px;
            } 
        QPushButton:hover {
            background-color: rgb(216,234,249); 
            }
        QPushButton:pressed {
            background-color: rgba(255,255,255,200);
        }
        '''
        self.setupUI()
        
    def setupUI(self):
        self.fileTab = QWidget()
        self.helpTab = QWidget()
        
        self.addTab(self.fileTab, 'File')
        self.addTab(self.helpTab, 'Help')
        
        self.setStyleSheet("QTabBar::tab { height: 50px}")
        
        # File Tab
        self.fileLayout = QHBoxLayout()
        
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
        
        self.fileLayout.addWidget(self.actionNew)
        self.fileLayout.addWidget(self.actionOpen)
        self.fileLayout.addWidget(self.actionSave)
        self.fileLayout.addWidget(self.actionSaveAs)
        self.fileLayout.addWidget(self.actionExport)
        self.fileLayout.addStretch(0)
        
        self.fileTab.setLayout(self.fileLayout)
        
        # Help Tab
        self.helpLayout = QHBoxLayout()
        
        self.actionApp = QPushButton("User Manual")
        self.actionApp.setIcon(QIcon("./img/file.png"))
        self.actionApp.setStyleSheet(self.btnStyle)
        
        self.actionAuthor = QPushButton("About Author")
        self.actionAuthor.setIcon(QIcon("./img/file.png"))
        self.actionAuthor.setStyleSheet(self.btnStyle)
        
        self.actionLab = QPushButton("About Lab")
        self.actionLab.setIcon(QIcon("./img/file.png"))
        self.actionLab.setStyleSheet(self.btnStyle)
        
        self.helpLayout.addWidget(self.actionApp)
        self.helpLayout.addWidget(self.actionAuthor)
        self.helpLayout.addWidget(self.actionLab)
        self.helpLayout.addStretch(0)
        
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
        img1.setText(0, 'Lower')
        img1.setText(1, '1.6m')
        img1.setText(2, 'D:/Test/test1.jpg')
        img1.setIcon(0, QIcon('./img/img.png'))

        img2 = QTreeWidgetItem(plot1)
        img2.setText(0, 'Upper')
        img2.setText(1, '2.6m')
        img2.setText(2, 'D:/Test/test2.jpg')
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
        self.projectButtonLayout = QHBoxLayout()
        self.addPlot = QPushButton('Add')
        self.delPlot = QPushButton('Del')
        self.editPlot = QPushButton('Edit')
        self.projectButtonLayout.addWidget(self.addPlot)
        self.projectButtonLayout.addWidget(self.delPlot)
        self.projectButtonLayout.addWidget(self.editPlot)
        
        self.progressBar = QProgressBar()
        
        self.addWidget(self.projectTree)
        self.addWidget(self.projectTableView)
        self.addLayout(self.projectButtonLayout)
        self.addWidget(self.progressBar)
        
        
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

        self.glUp = QOpenGLWidget()
        self.glUp.setEnabled(False)
        #self.glDown = QOpenGLWidget()
        self.glDown = GLWidget()
        self.glDown.setEnabled(True)
        
        self.openglLayout = QVBoxLayout()
        self.openglLayout.addWidget(self.glUp)
        self.openglLayout.addWidget(self.glDown)
        
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
        
        ### IndividualModel
        self.IndividualModel = QStandardItemModel(0, 4)
        self.IndividualModel.setHorizontalHeaderLabels(['Distance', '△H', 'DBH', 'HT'])
        
        self.IndividualTableView = QTableView()
        self.IndividualTableView.setModel(self.IndividualModel)
        self.IndividualTableView.resizeColumnsToContents()
        self.IndividualTableView.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        
        self.layout.addLayout(self.openglCtrlLayout, stretch=2)
        self.layout.addWidget(self.IndividualTableView, stretch=1)

        
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