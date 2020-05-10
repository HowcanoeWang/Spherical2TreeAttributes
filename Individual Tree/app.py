import sys
import os
import numpy as np
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PIL import Image, ExifTags
#from scipy import ndimage
#from scipy.interpolate import interp1d
#from skimage.exposure import equalize_hist
import imageio
import random

from ba import in_tree_pixel

baf20 = in_tree_pixel(baf=20, img_width=5376)

class MainWindow(QMainWindow):
    keyPressed = pyqtSignal(QEvent)
    vLocked = pyqtSignal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        
        self.coordinate = '(x, y)'

        low = input("Please type the lower camera height in METER, default=1.6\n>>>")
        try:
            e1 = float(low)
        except ValueError:
            print('No valuable float numbers typed, used default 1.6m')
            e1 = 1.6

        high = input("Please type the higher camera height in METER, default=2.6\n>>>")
        try:
            e2 = float(high)
        except ValueError:
            print('No valuable float numbers typed, used default 2.6m')
            e2 = 2.6

        if e1 > e2:
            e1, e2 = e2, e1

        sector_func = input('Use Sector Sampling ? [Y/N]\n>>>')
        sector_intensity = None
        sector_num = None
        if sector_func in ['Y','y', 'yes']:
            intense_loop = True
            while intense_loop:
                intensity_temp = input('[Sector] Please type the intensity '
                                       '(the percentage of sector width, %, 0-100): ')
                try:
                    intensity_temp = float(intensity_temp)
                except ValueError:
                    print(f'[Sector] <{intensity_temp}> is not a valuable float number, please type again.')
                    continue
                if 0 <= intensity_temp and intensity_temp <= 100:
                    sector_intensity = intensity_temp
                    intense_loop = False
                else:
                    print(f'[Sector] <{intensity_temp}> should range from 0 to 100, please type again')
                    continue

            num_loop = True
            while num_loop:
                number_temp = input('[Sector] Please type the number of sector (0-10, int): ')
                try:
                    number_temp = int(number_temp)
                except ValueError:
                    print(f'[Sector] <{number_temp}> is not a valuable integer number, please type again.')
                    continue
                if 0 <= number_temp and number_temp * sector_intensity <= 50:
                    sector_num = number_temp
                    num_loop = False
                else:
                    print(f'[Sector] <{number_temp}>*intensity({sector_intensity}) '
                          f'should range from 0 to 100, please type again')
                    continue

        if sector_intensity is None:
            self.sector_range = None
            print(f'App launch! With low camera {e1}m and high camera {e2}m')
        else:
            self.sector_range = self.getSectorStarts(sector_num, sector_intensity)
            print(f'App launch! With low camera {e1}m and high camera {e2}m, '
                  f'and {sector_num} Sector(s) of {sector_intensity}% width')
        self.e1 = e1
        self.e2 = e2

        self.setWindowTitle('IndividualDemo')
        self.setupUI()
        self.functionConnector()
        
        self.initPlot()
        self.initTree()

        self.addTree = -1  # No add
        
    def setupUI(self):
        self.mainWidget = QWidget()
        
        self.panel1 = ImgPanel(self, self.e1, self.sector_range)
        self.panel2 = ImgPanel(self, self.e2, self.sector_range)
        
        self.line = QFrame()
        self.line.setFrameShape(QFrame.VLine)
        self.line.setFrameShadow(QFrame.Sunken)
        
        self.wl = QHBoxLayout(self.mainWidget)
        
        self.wl.addWidget(self.panel1)
        self.wl.addWidget(self.line)
        self.wl.addWidget(self.panel2)
        
        self.setCentralWidget(self.mainWidget)
    
    def functionConnector(self):
        self.panel1.xScrollChanged.connect(self.panel2.setXScroll)
        self.panel2.xScrollChanged.connect(self.panel1.setXScroll)
        self.panel1.yScrollChanged.connect(self.panel2.setYScroll)
        self.panel2.yScrollChanged.connect(self.panel1.setYScroll)
        
        self.panel1.exifData.connect(self.updatePlot)
        self.panel2.exifData.connect(self.updatePlot)
        
        self.keyPressed.connect(self.panel1.imgShow.changeDirection)
        self.keyPressed.connect(self.panel2.imgShow.changeDirection)
        
        self.panel1.imgShow.emitPoint.connect(self.addTree)
        self.panel2.imgShow.emitPoint.connect(self.addTree)
        
        self.vLocked.connect(self.panel1.imgShow.changeVLock)
        self.vLocked.connect(self.panel2.imgShow.changeVLock)
    
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_L:
            v, okPressed = QInputDialog.getInt(self, "Get integer","Y pixel", 6000, 0, 13000, 1)
            if okPressed:
                self.vLocked.emit(v)
        elif event.key() == Qt.Key_U:
            self.vLocked.emit(-1)
        elif event.key() == Qt.Key_N:   # Add tree easy mode
            self.addTree = 0
            self.initTree()
            self.changeDirection('NE')
            self.showStep(f'[S1:{self.e1}Base]')
        else:
            self.keyPressed.emit(event)
            
    def initPlot(self):
        self.plot = {'GCP16':0, 
             'LatDeg16':0, 'LatMin16':0, 'LatSec16':0.0,
             'LonDeg16':0, 'LonMin16':0, 'LonSec16':0.0,
             'Altitude16':0.0, 'North16':0.0,
             'GCP26':0, 
             'LatDeg26':0, 'LatMin26':0, 'LatSec26':0.0,
             'LonDeg26':0, 'LonMin26':0, 'LonSec26':0.0,
             'Altitude26':0.0, 'North26':0.0}
             
    def updatePlot(self, ht, data_list):
        if ht == self.e1:
            self.plot['GCP16']      = data_list[0]
            self.plot['LatDeg16']   = data_list[1]
            self.plot['LatMin16']   = data_list[2]
            self.plot['LatSec16']   = data_list[3]
            self.plot['LonDeg16']   = data_list[4]
            self.plot['LonDeg16']   = data_list[5]
            self.plot['LonDeg16']   = data_list[6]
            self.plot['Altitude16'] = data_list[7]
            self.plot['North16']    = data_list[8]
        else:
            self.plot['GCP26']      = data_list[0]
            self.plot['LatDeg26']   = data_list[1]
            self.plot['LatMin26']   = data_list[2]
            self.plot['LatSec26']   = data_list[3]
            self.plot['LonDeg26']   = data_list[4]
            self.plot['LonDeg26']   = data_list[5]
            self.plot['LonDeg26']   = data_list[6]
            self.plot['Altitude26'] = data_list[7]
            self.plot['North26']    = data_list[8]
            
        print(self.plot)
             
    def initTree(self):
        self.tree = {'16BX':0, '16BY':0, '16TX':0, '16TY':0,
                     '26BX':0, '26BY':0, '26TX':0, '26TY':0,
                     '16LX':0, '16LY':0, '16RX':0, '16RY':0,
                     '26LX':0, '26LY':0, '26RX':0, '26RY':0,
                     'Dist':0.0, 'DeltaH':0.0, 'HT':0.0, 'DBH':0.0, 'Gamma':0.0, 'Altitude':0.0}
             
    def addTree(self, x, y):
        # 0: Add 16Base
        # 1: Add 26Base => Calculate Dist, DeltaH, Altitude, Gamma, 1.3m, set panel16, panel 26
        # change direction to "W"
        # 2: Add 16Left => change direction to "E"
        # 3: Add 16Right => change direction to "W"
        # 4: Add 26Left => change direction to "E"
        # 5: Add 26Right => calculate DBH
        # 6：Add 16Top
        # 7: Add 26Top => calculate HT, change to -1
        if self.addTree == 0:
            self.tree['16BX'] = x
            self.tree['16BY'] = y
            self.addTree += 1
            self.showStep(f'[S2: {self.e2}Base]')
        elif self.addTree == 1:
            self.tree['26BX'] = x
            self.tree['26BY'] = y
            
            k1 = np.tan(-self.zenithRadians(self.tree['16BY']))
            k2 = np.tan(-self.zenithRadians(self.tree['26BY']))
            ix, iy = self.interactBase(k1, self.e1, k2, self.e2)
            self.tree['Dist'] = -ix
            self.tree['DeltaH'] = iy
            
            self.tree['Altitude'] = (self.plot['Altitude16'] + self.plot['Altitude26']) / 2 + iy
            gamma1 = self.horizonAngle(self.tree['16BX'], self.plot['GCP16'], self.plot['North16'])
            gamma2 = self.horizonAngle(self.tree['26BX'], self.plot['GCP26'], self.plot['North26'])
            self.tree['Gamma'] = (gamma1 + gamma2) / 2
            
            dbh16pos = self.getDBHPosition(self.e1, ix, iy)
            dbh26pos = self.getDBHPosition(self.e2, ix, iy)
            
            self.panel1.imgShow.changeVLock(int(dbh16pos))
            self.panel2.imgShow.changeVLock(int(dbh26pos))
            
            self.changeDirection('NW')
            self.showStep(f'[S3:{self.e1}Left]')
            self.addTree += 1
        elif self.addTree == 2:
            self.tree['16LX'] = x
            self.tree['16LY'] = y
            self.changeDirection('NE')
            self.showStep(f'[S4:{self.e1}Right]')
            self.addTree += 1
        elif self.addTree == 3:
            self.tree['16RX'] = x
            self.tree['16RY'] = y
            self.changeDirection('NW')
            self.showStep(f'[S5:{self.e2}Left]')
            self.addTree += 1
        elif self.addTree == 4:
            self.tree['26LX'] = x
            self.tree['26LY'] = y
            self.changeDirection('NE')
            self.showStep(f'[S6:{self.e2}Right]')
            self.addTree += 1
        elif self.addTree == 5:
            self.tree['26RX'] = x
            self.tree['26RY'] = y
            self.changeDirection('NW')
            
            dbh16 = self.getDBH(self.tree['16LX'], self.tree['16RX'], self.tree['Dist'])
            dbh26 = self.getDBH(self.tree['26LX'], self.tree['26RX'], self.tree['Dist'])
            self.tree['DBH'] = (dbh16 + dbh26) / 2
            
            self.panel1.imgShow.changeVLock(-1)
            self.panel2.imgShow.changeVLock(-1)
            self.showStep(f'[S7:{self.e1}Top]')
            
            self.addTree += 1
        elif self.addTree == 6:
            self.tree['16TX'] = x
            self.tree['16TY'] = y
            self.showStep(f'[S8:{self.e2}Top]')
            self.addTree += 1
        elif self.addTree == 7:
            self.tree['26TX'] = x
            self.tree['26TY'] = y
            
            k1 = np.tan(-self.zenithRadians(self.tree['16TY']))
            k2 = np.tan(-self.zenithRadians(self.tree['26TY']))
            ht1 = - self.tree['Dist'] * k1 + self.e1 - self.tree['DeltaH']
            ht2 = - self.tree['Dist'] * k2 + self.e2 - self.tree['DeltaH']
            
            self.tree['HT'] = (ht1 + ht2) / 2
            self.showStep('[Done&Paste]')
            
            text = f'{self.e1}\t{self.e2}\t'
            for key, value in self.tree.items():
                text += f'{value}\t'
                
            self.cb = QApplication.clipboard()
            self.cb.clear(mode=self.cb.Clipboard)
            self.cb.setText(text[:-1], mode=self.cb.Clipboard)
            
            print(text)
            self.addTree = -1
            QMessageBox.information(self, 'Tree Info',
                                    f'The info of this measured tree is:\n'
                                    f"Distance\t{round(self.tree['Dist'],2)}\n"
                                    f"ΔH      \t{round(self.tree['DeltaH'],2)}\n"
                                    f"HT      \t{round(self.tree['HT'],2)}\n"
                                    f"DBH     \t{round(self.tree['DBH'],2)}\n"
                                    f"North   \t{round(self.tree['Gamma'],2)}\n"
                                    f"Altitude\t{round(self.tree['Altitude'],2)}\n"
                                    f"Please open Excel and Ctrl+V to paste the result\n"
                                    f"Press 'N' to measure a new tree")
        
    def changeDirection(self, direct='NE'):
        self.panel1.imgShow.corner = direct
        self.panel2.imgShow.corner = direct
        self.panel1.imgShow.update()
        self.panel2.imgShow.update()
        
    def showStep(self, string):
        self.panel1.updateProgress(string)
        self.panel2.updateProgress(string)
        
    @staticmethod
    def interactBase(k1, b1, k2, b2):
        x = (b2-b1)/(k1-k2)
        y = k1*x + b1
        return x, y
        
    @staticmethod
    def zenithRadians(ypos):
        return np.radians((1344 - (ypos - 1))/2688*180)
        
    @staticmethod
    def horizonAngle(xpos, gcp, north):
        gamma = (xpos+gcp) / 5376 * 360 - north
        if gamma < 0:
            gamma += 360
        if gamma > 360:
            gamma -= 360
        return gamma
        
    @staticmethod
    def getDBHPosition(e, bx, by):
        angles = -np.degrees(np.arctan((e-1.3-by)/(0-bx)))
        pos = 1344 - angles / 180 * 2688
        return pos
        
    @staticmethod
    def getDBH(lx, rx, dist):
        omiga = np.radians(abs(rx-lx) / 5376 * 360)
        sin_half_omiga = np.sin(omiga / 2)
        dbh = 2 * sin_half_omiga * dist / (1 - sin_half_omiga) * 100
        return dbh

    @staticmethod
    def getSectorStarts(num, width):
        total = 100
        res = set()
        sector_range = []
        for i in range(num):
            temp = random.uniform(0, total - width)
            #print(f'[Sector{i}] -> First guess start point <{temp}> in total {list((idx, idx + width) for idx in res)}')
            #print(f'[Sector{i}] -> Check if overlapped {[(temp >= idx and temp <= idx + width) or (temp + width >= idx and temp + width <= idx + width) for idx in res]}')
            while any((temp >= idx and temp <= idx + width) or (temp + width >= idx and temp + width <= idx + width) for idx in res):
                temp = random.uniform(0, total - width)
                #print(f"[Sector{i}] -> repeat guess start point <{temp}> in total {list((idx, idx + width) for idx in res)}")
            res.add(temp)
        for idx in res:
            sector_range.append((idx, idx + width))

        return sector_range
        
class ImgPanel(QWidget):
    xScrollChanged = pyqtSignal(int)
    yScrollChanged = pyqtSignal(int)
    exifData = pyqtSignal(float, list)
    
    def __init__(self, parent=None, ht=1.6, sector_range=None):
        super().__init__(parent)
        self.refX = 0
        self.refY = 0
        
        self.scrollX = 0
        self.scrollY = 0
        
        self.ht = ht
        self.sector_range = sector_range
        
        self.converter = Converter(self)
        
        self.setupUI(ht)
        self.functionConnector()
        
    def setupUI(self, ht):
        self.layout = QVBoxLayout(self)
        self.infoLayout = QHBoxLayout()
        
        self.htName = QLabel(f"[{ht}m]:")
        self.imgName = QLabel('D:/xxx.Jpg')
        self.infoBtn = QPushButton('Info')
        self.changeImgBtn = QPushButton('OpenImg')
        self.convertBtn = QPushButton('Convert')
        self.saveImgBtn = QPushButton('save')
        
        self.imgShow = ImgShow(self)
        #self.scrollArea = QScrollArea()
        self.scrollArea = Scroller()
        self.scrollArea.setWidget(self.imgShow)
        
        self.hBar = self.scrollArea.horizontalScrollBar()
        self.vBar = self.scrollArea.verticalScrollBar()
        self.scrollX = self.hBar.value()
        self.scrollY = self.vBar.value()
        
        self.infoLayout.addWidget(self.htName)
        self.infoLayout.addWidget(self.imgName)
        self.infoLayout.addStretch(0)
        self.infoLayout.addWidget(self.infoBtn)
        self.infoLayout.addWidget(self.changeImgBtn)
        self.infoLayout.addWidget(self.convertBtn)
        self.infoLayout.addWidget(self.saveImgBtn)
        
        self.layout.addLayout(self.infoLayout)
        self.layout.addWidget(self.scrollArea)
        
    def functionConnector(self):
        self.imgShow.mouseClicked.connect(self.updateRef)
        self.infoBtn.clicked.connect(self.showInfo)
        self.changeImgBtn.clicked.connect(self.loadImg)
        self.convertBtn.clicked.connect(self.convertImg)
        self.saveImgBtn.clicked.connect(self.imgShow.saveImg)
        self.hBar.valueChanged.connect(self.emitX)
        self.vBar.valueChanged.connect(self.emitY)
        self.converter.sigOut.connect(self.updateProgress)
        self.imgShow.saver.sigOut.connect(self.updateProgress)
        
    def emitX(self):
        self.xScrollChanged.emit(self.hBar.value())
    
    def emitY(self):
        self.yScrollChanged.emit(self.vBar.value())
        
    def setXScroll(self, value):
        self.hBar.setValue(min(self.hBar.maximum(),value))
        
    def setYScroll(self, value):
        self.vBar.setValue(min(self.vBar.maximum(),value))
        
    def wheelEvent(self, event):
        if event.modifiers() == Qt.ShiftModifier:
            self.hBar.wheelEvent(event)
        else:
            self.vBar.wheelEvent(event)
            
    def getExifInfo(self):
        self.show_str = ''
        self.clip_str = ''
        # gcp, lat.D, lat.M, lat.S, Lon.D, Lon.M, Lon.S, Altitude, North
        # 0,   1,     2,     3,     4,     5,     6,     7,        8
        self.data_list = [0, 0, 0, 0.0, 0, 0, 0.0, 0.0, None]
        
        if self.imgShow.img_path is not None:
            img = Image.open(self.imgShow.img_path)
            exif_human = {ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS}
            gps_info = exif_human['GPSInfo']
            
            self.data_list[0] = self.refX
            lat_label = gps_info[1] # N
            lat_exif = gps_info[2] # ((45, 1), (56, 1), (4682, 100))
            self.data_list[1] = lat_exif[0][0]
            self.data_list[2] = lat_exif[1][0]
            self.data_list[3] = lat_exif[2][0]/lat_exif[2][1]
            self.show_str += f"{lat_exif[0][0]}°{lat_exif[1][0]}′{self.data_list[3]}″ {lat_label}\n"
            
            lon_label = gps_info[3] # W
            lon_exif = gps_info[4] # ((66, 1), (38, 1), (3938, 100))
            self.data_list[4] = lon_exif[0][0]
            self.data_list[5] = lon_exif[1][0]
            self.data_list[6] = lon_exif[2][0]/lat_exif[2][1]
            self.show_str += f"{lon_exif[0][0]}°{lon_exif[1][0]}′{self.data_list[6]}″ {lon_label}\n"
            
            alt_exif = gps_info[6] # (3512, 100)
            self.data_list[7] = alt_exif[0]/alt_exif[1]
            self.show_str += f"altitude:{self.data_list[7]}\n"
            
            if 17 in gps_info.keys():
                north_angle = gps_info[17] # (1125, 10)
                self.data_list[8] = north_angle[0]/north_angle[1]
                self.show_str += f"north:{self.data_list[8]}°"
            else:
                self.show_str += f"north: missing"
                
            for i in self.data_list:
                self.clip_str += f'{i}\t'
        
        #self.clip_str = f'{self.refX}\t{lat_exif[0][0]}\t{lat_exif[1][0]}\t{lat_exif[2][0]/lat_exif[2][1]}\t{lon_exif[0][0]}\t{lon_exif[1][0]}\t{lon_exif[2][0]/lon_exif[2][1]}\t{alt_exif[0]/alt_exif[1]}'
     
    def showInfo(self):
        self.getExifInfo()
        try:
            QMessageBox.information(self, "GPS Info", self.show_str)
            self.cb = QApplication.clipboard()
            self.cb.clear(mode=self.cb.Clipboard)
            self.cb.setText(self.clip_str[:-1], mode=self.cb.Clipboard)         
        except:
            QMessageBox.information(self, "GPS Info", "Please use raw images!")
        
    def loadImg(self, choose=True):
        if not isinstance(choose, str):
            options = QFileDialog.Options()
            fileName, _ = QFileDialog.getOpenFileName(self, 'QFileDialog.getOpenFileName()', '',
                                                      'Images (*.png *.jpeg *.jpg *.bmp *.gif)', options=options)
            self.convertBtn.setEnabled(True)
        else:
            fileName=choose

        if fileName:
            image = QImage(fileName)
            if image.isNull():
                QMessageBox.information(self, "Image Viewer", "Cannot load %s." % fileName)
                return
                
            self.imgName.setText(fileName[:10]+'...'+fileName[-20:])
            self.imgShow.img_path = fileName
            self.imgShow.addImg = True
            self.imgShow.update()
            if 'converted_imgs/' not in fileName:
                self.getExifInfo()
        
    def convertImg(self):
        if self.imgShow.img_path is not None:
            self.converter.set_param(self.imgShow.img_path, append=self.ht,
                                     zenith=89, equalize=False, gcp=self.refX,
                                     sector_range=self.sector_range)
            self.data_list[0] = self.refX
            self.exifData.emit(self.ht, self.data_list)   
            self.converter.start()
        else:
            print('empty img')
        
    def updateRef(self, X, Y):
        self.refX = X
        self.refY = Y
        
    def updateProgress(self, percent):
        if isinstance(percent, str):
            self.htName.setText(percent)
        else:
            # finished processing
            base = os.path.basename(self.imgShow.img_path)
            file, ext = os.path.splitext(base)
            #self.loadImg(f'converted_imgs/{file}_M{self.refX}{ext}')
            self.loadImg(f'converted_imgs/{file}_D{self.refX}{ext}')
            self.htName.setText(f"|{self.ht}m|:")
            self.convertBtn.setEnabled(False)
        
        
class Scroller(QScrollArea):

    def __init__(self):
        QScrollArea.__init__(self)

    def wheelEvent(self, ev):
        if ev.type() == QEvent.Wheel:
            ev.ignore()
            
class Converter(QThread):
    sigOut = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.img_path = None
        self.mode = 'direct'
        self.append = 1.6
        self.zenith = 85
        self.equalize = False
        self.gcp = 0
        
    def set_param(self, img_path, append=1.6, zenith=85, equalize=False, gcp=0, mode='direct', sector_range=None):
        self.img_path = img_path
        self.append = append
        self.zenith = zenith
        self.equalize = equalize
        self.gcp = gcp
        self.mode = mode
        self.sector_range = sector_range
    
    def run(self):
        '''Document see mercator.py'''
        img = imageio.imread(self.img_path)
        h, w, d = img.shape
        self.sigOut.emit('[10%..]')
        
        if self.mode == 'mercator':
            '''
            if self.equalize:
                img = equalize_hist(img)
                self.sigOut.emit('[20%..]')
                
            h_id = np.arange(h) 
            w_id = np.arange(w)
            self.sigOut.emit('[30%..]')
            
            angle_id = h/2 - h_id - 0.5
            angle = angle_id / angle_id.max() * 90 # degree
            self.sigOut.emit('[40%..]')
            
            select = abs(angle) <= self.zenith
            select_angle = angle[select] 
            self.sigOut.emit('[45%..]')
            
            select_img = img[select, :, :]
            select_h, _, _ = select_img.shape  # (2538, 5376, 3)
            self.sigOut.emit('[50%..]')
            
            mecator_coord = h / 2 * np.log(np.tan(np.deg2rad(45 + select_angle / 2)))
            mecator_coord_zero = mecator_coord.max() - mecator_coord
            self.sigOut.emit('[55%..]')
           
            f = interp1d(mecator_coord_zero, np.arange(select_h), fill_value="extrapolate")
            self.sigOut.emit('[60%..]')
            xnew = np.arange(0, np.ceil(mecator_coord.max())*2, 1)  
            mecator_id = f(xnew)  # related img_h id in raw image (85 degree selected)
            self.sigOut.emit('[65%..]')
            
            # table to refer mecator_id -> zenith angle
            f_angle = interp1d(mecator_coord_zero, select_angle, fill_value="extrapolate")
            mecator_angle = f_angle(xnew)
            self.sigOut.emit('[70%..]')
            
            ww, hh = np.meshgrid(w_id, mecator_id) # shape (8404, 5376)
            self.sigOut.emit('[75%..]')
            
            img_out = np.zeros((*hh.shape, 3))
            for i in range(0 ,3):
                img_out[:,:,i] = ndimage.map_coordinates(select_img[:,:,i], 
                                                         np.array([hh,ww]),output=float,order=1)
                self.sigOut.emit(f'[{70 + 9*(i+1)}%..]')                                                
            
            img_out = np.hstack((img_out[:,self.gcp:, :], img_out[:,0:self.gcp, :]))
            self.sigOut.emit('[98%..]')

            base = os.path.basename(self.img_path)
            file, ext = os.path.splitext(base)
            imageio.imwrite(f'converted_imgs/{file}_M{self.gcp}{ext}', img_out)
            
            self.m2a = mecator_angle'''
            pass
            
        else:
            self.sigOut.emit('[40%..]')
            img_out = np.hstack((img[:,self.gcp:, :], img[:,0:self.gcp, :]))
            # add sector here
            if self.sector_range is not None:
                or1 = [197,90,17]
                or2 = [244,177,131]
                or3 = [247,203,172]
                or4 = [257,229,213]
                for sector in self.sector_range:
                    st, ed = sector
                    st = st * w / 100
                    ed = ed * w / 100
                    img_out[:, int(max(st-3, 0)), :] = or4
                    img_out[:, int(max(st-2, 0)), :] = or3
                    img_out[:, int(max(st-1, 0)), :] = or2
                    img_out[:, int(max(st  , 0)), :] = or1
                    img_out[:, int(min(ed+3, w-1)), :] = or4
                    img_out[:, int(min(ed+2, w-1)), :] = or3
                    img_out[:, int(min(ed+1, w-1)), :] = or2
                    img_out[:, int(min(ed,   w-1)), :] = or1
            self.sigOut.emit('[60%..]')
            base = os.path.basename(self.img_path)
            file, ext = os.path.splitext(base)
            self.sigOut.emit('[80%..]')
            imageio.imwrite(f'converted_imgs/{file}_D{self.gcp}{ext}', img_out)
            self.sigOut.emit('[99%..]')
        
        self.sigOut.emit(True)
        
        
        
class ImgShow(QWidget):
    mouseClicked = pyqtSignal(object, object)
    emitPoint = pyqtSignal(object, object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.x = 0
        self.y = 0
        self.w = self.frameGeometry().width()  # 100
        self.h = self.frameGeometry().height()  # 30
        
        self.corner = 'NE' # North East(default)
        self.vLock = -1
        
        self.img_path = None
        self.addImg = False
        self.isMoving = True
        self.leftPressed = False
        
        self.setMinimumSize(5376, 2000)
        
        self.tempPix = QPixmap(5376, 2000)
        
        self.pix = QPixmap(5376, 2000)
        self.pix.fill(Qt.white)
        
        self.saver = Saver(self)
        
        self.setMouseTracking(True)
        self.setCursor(Qt.BlankCursor)
        
        self.functionConnector()
        
    def functionConnector(self):
        pass
        
    def paintEvent(self, event):
        painter = QPainter(self)
        
        if self.addImg:
            imgPixmap = QPixmap.fromImage(QImage(self.img_path))
            
            imgH = imgPixmap.height()
            imgW = imgPixmap.width()
            
            self.pix = QPixmap(imgW, imgH)
            self.tempPix = QPixmap(imgW, imgH)
            self.resize(imgW, imgH)
            
            p = QPainter(self.pix)
            p.setPen(QColor(255, 255,0))
            p.drawPixmap(0, 0, imgPixmap)
            p.drawLine(0, imgH/2, imgW, imgH/2)
            self.addImg = False
        
        fm = QFontMetrics(QFont('SimSun', 10))
        pw = fm.width(f'{self.x},{self.y}')
        ph = fm.height()
        if self.corner == 'NE':
            text_x, text_y = self.x, self.y
            rect_x, rect_y = self.x-baf20, self.y-20
        elif self.corner == 'NW':
            text_x, text_y = self.x-pw, self.y
            rect_x, rect_y = self.x, self.y-20
        elif self.corner == 'SE':
            text_x, text_y = self.x, self.y+ph
            rect_x, rect_y = self.x-baf20, self.y-20
        else:
            text_x, text_y = self.x-pw, self.y+ph
            rect_x, rect_y = self.x-baf20, self.y-20
            
        if self.isMoving:
            # 把以前的pix复制一遍(相当于清空)
            self.tempPix = self.pix.copy()
            
            qp = QPainter(self.tempPix)
            qp.setPen(QColor(255, 0,0))
            qp.setFont(QFont('SimSun', 10))
            
            qp.drawLine(self.x, 0, self.x, self.h)
            qp.drawLine(0, self.y, self.w, self.y)
            
            qp.drawText(text_x, text_y, f'{self.x},{self.y}')
            
            qp.drawRect(rect_x, rect_y, baf20, 20)
            
            painter.drawPixmap(0, 0, self.tempPix)
        else:
            qp = QPainter(self.pix)
            qp.setPen(QColor(255, 0,0))
            qp.setFont(QFont('SimSun', 10))
            
            qp.drawLine(self.x, self.y-20, self.x, self.y+20)
            qp.drawLine(self.x-20, self.y, self.x+20, self.y)
            qp.drawText(text_x, text_y, f'{self.x},{self.y}')
            
            painter.drawPixmap(0, 0, self.pix)
            
    def saveImg(self):
        if self.img_path is not None:
            self.saver.set_param(self.img_path, self.pix.toImage())
            self.saver.start()
        
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftPressed = True
            self.x = event.x()
            if self.vLock == -1:
                self.y = event.y()
            else:
                self.y = self.vLock
            self.mouseClicked.emit(self.x, self.y)
            
            self.w = self.frameGeometry().width()  # 100
            self.h = self.frameGeometry().height()  # 30
            self.isMoving=False     
            self.update()            
        
    def mouseMoveEvent(self,event):
        if not self.leftPressed:
            self.x = event.x()
            if self.vLock == -1:
                self.y = event.y()
            else:
                self.y = self.vLock
            self.w = self.frameGeometry().width()  # 100
            self.h = self.frameGeometry().height()  # 30
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.leftPressed = False
            self.isMoving=True
            if window.addTree == -1:
                self.copy2Clipboard()
            else:
                self.emitPoint.emit(self.x, self.y)
            
    def changeDirection(self, event):
        if event.key() == Qt.Key_W:
            if 'S' in self.corner:
                self.corner = self.corner.replace('S', 'N')
        elif event.key() == Qt.Key_S:
            if 'N' in self.corner:
                self.corner = self.corner.replace('N', 'S')
        elif event.key() == Qt.Key_A:
            if 'E' in self.corner:
                self.corner = self.corner.replace('E', 'W')
        elif event.key() == Qt.Key_D:
            if 'W' in self.corner:
                self.corner = self.corner.replace('W', 'E')      
        self.update()
        
    def changeVLock(self, value):
        self.vLock = value
        self.update()
            
    def copy2Clipboard(self):
        text = f'{self.x}\t{self.y}'
        self.cb = QApplication.clipboard()
        self.cb.clear(mode=self.cb.Clipboard)
        self.cb.setText(text, mode=self.cb.Clipboard)
        
        
class Saver(QThread):
    sigOut = pyqtSignal(object)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        # https://stackoverflow.com/questions/46945997/creating-qpixmaps-in-a-thread
        # that *QPixmaps* cannot be created outside the main thread. 
        # But it's pretty straightforward to instead use an image loader object, 
        # move it to one or more background threads, in which it loads a QImage, 
        # and then sends that to the main thread for later use
        self.qimage = QImage()
        self.img_path = 'result_imgs/rua.png'
        
    def set_param(self, img_path, qimage):
        self.img_path = img_path
        self.qimage = qimage
    
    def run(self):
        self.sigOut.emit('[20%..]')
        base = os.path.basename(self.img_path)
        self.sigOut.emit('[40%..]')
        file, ext = os.path.splitext(base)
        self.sigOut.emit('[60%..]')
        #self.pix.save(f"result_imgs/{file}_C{ext}", "PNG")
        self.qimage.save(f"result_imgs/{file}_C{ext}", "PNG")
        self.sigOut.emit('[Saved]')
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.showMaximized()
    sys.exit(app.exec_())