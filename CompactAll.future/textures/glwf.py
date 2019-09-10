from OpenGL.GL import *
from OpenGL.GLU import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtOpenGL import *
import sys

class MainWindow(QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.widget = GLWidget(self)
        #self.statusbar = QStatusBar()
        #self.statusbar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        #self.statusbar.showMessage("Click anywhere on the QGLWidget to see a pixel's RGBA value!")
        layout = QVBoxLayout()
        layout.addWidget(self.widget)
        #layout.addWidget(self.statusbar)
        layout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(layout)

class GLWidget(QGLWidget):

    def __init__(self, parent):
        QGLWidget.__init__(self, parent)
        self.setMinimumSize(640, 480)
        #LMB = left mouse button
        #True: fires mouseMoveEvents even when not holding down LMB
        #False: only fire mouseMoveEvents when holding down LMB
        self.setMouseTracking(False)

    def initializeGL(self):
        glClearColor(0, 0, 0, 1)
        glClearDepth(1.0)
        glEnable(GL_DEPTH_TEST)

    def resizeGL(self, width, height):
        #glViewport is needed for proper resizing of QGLWidget
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glOrtho(0, width, 0, height, -1, 1)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

    def paintGL(self):
        #Renders a triangle... obvious (and deprecated!) stuff
        w, h = self.width(), self.height()
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glBegin(GL_TRIANGLES)
        glColor3f(1, 0, 0)
        glVertex3f(0, 0, 0)
        glColor3f(0, 1, 0)
        glVertex3f(w/2.0, h, 0)
        glColor3f(0, 0, 1)
        glVertex3f(w, 0, 0)
        glEnd()

    def mousePressEvent(self, event):
        x, y = event.x(), event.y()
        w, h = self.width(), self.height()
        #required to call this to force PyQt to read from the correct, updated buffer 
        #see issue noted by @BjkOcean in comments!!!
        glReadBuffer(GL_FRONT)
        data = self.grabFrameBuffer()#builtin function that calls glReadPixels internally
        data.save("test.png")
        rgba = QColor(data.pixel(x, y)).getRgb()#gets the appropriate pixel data as an RGBA tuple
        message = "You selected pixel ({0}, {1}) with an RGBA value of {2}.".format(x, y, rgba)
        statusbar = self.parent().statusbar#goes to the parent widget (main window QWidget) and gets its statusbar widget
        statusbar.showMessage(message)

    def mouseMoveEvent(self, event):
        pass

    def mouseReleaseEvent(self, event):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Color Picker Demo")
    window.show()
    app.exec_()