# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'beeboard.ui'
##
## Created by: Qt User Interface Compiler version 6.10.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QCheckBox, QComboBox, QGroupBox,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSlider, QStatusBar,
    QTextEdit, QVBoxLayout, QWidget, QAbstractButton)

import os
import sys

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

class PySwitch(QAbstractButton):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCheckable(True)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed) # Genişliği yazıya göre esnettik
        self.setMinimumHeight(26)
        self.setMinimumWidth(80) # Yazı için biraz yer açtık
        
        self._on_color = QColor("#008000")
        self._off_color = QColor("#cccccc")

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # Geometri ayarları
        switch_width = 50
        switch_height = 26
        
        # 1. Arka Planı Çiz (Sadece switch kısmı)
        color = self._on_color if self.isChecked() else self._off_color
        painter.setBrush(color)
        painter.setPen(Qt.NoPen)
        painter.drawRoundedRect(0, 0, switch_width, switch_height, switch_height/2, switch_height/2)
        
        # 2. Hareketli Daireyi Çiz
        painter.setBrush(QColor("white"))
        x_pos = (switch_width - switch_height + 3) if self.isChecked() else 3
        painter.drawEllipse(x_pos, 3, switch_height-6, switch_height-6)

        # 3. YAZIYI ÇİZ (Eğer metin varsa)
        if self.text():
            painter.setPen(QColor("white")) # Yazı rengi
            # Metni switch'in 10 piksel sağından başlatarak ortala
            text_rect = QRect(switch_width + 10, 0, self.width() - switch_width - 10, self.height())
            painter.drawText(text_rect, Qt.AlignVCenter | Qt.AlignLeft, self.text())

    def sizeHint(self):
        # Layout'un widget için ne kadar yer ayıracağını belirler
        return QPoint(120, 26)

    def mouseReleaseEvent(self, e):
        super().mouseReleaseEvent(e)
        self.update()

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1676, 752)
        MainWindow.setAutoFillBackground(False)
        MainWindow.setStyleSheet(u"")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setEnabled(True)
        self.label.setGeometry(QRect(230, 0, 1301, 671))
        self.label.setStyleSheet(u"")
        self.label.setPixmap(QPixmap(resource_path("board.png")))
        self.label.setScaledContents(True)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label.setIndent(-1)
        self.pin22Button = PySwitch(self.centralwidget)
        self.pin22Button.setObjectName(u"pin22Button")
        self.pin22Button.setGeometry(QRect(1040, 30, 21, 20))
        self.pin22Button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pin22Button.setStyleSheet(u"color: black;")
        self.pin23Button = PySwitch(self.centralwidget)
        self.pin23Button.setObjectName(u"pin23Button")
        self.pin23Button.setGeometry(QRect(1151, 30, 21, 20))
        self.pin23Button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pin23Button.setStyleSheet(u"color: black;")
        self.pin24Button = PySwitch(self.centralwidget)
        self.pin24Button.setObjectName(u"pin24Button")
        self.pin24Button.setGeometry(QRect(1270, 30, 21, 20))
        self.pin24Button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pin24Button.setStyleSheet(u"color: black;")
        self.pin25Button = PySwitch(self.centralwidget)
        self.pin25Button.setObjectName(u"pin25Button")
        self.pin25Button.setGeometry(QRect(1381, 30, 21, 20))
        self.pin25Button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pin25Button.setStyleSheet(u"color: black;")
        self.RFIDButton = PySwitch(self.centralwidget)
        self.RFIDButton.setObjectName(u"RFIDButton")
        self.RFIDButton.setGeometry(QRect(1479, 290, 21, 20))
        self.RFIDButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.RFIDButton.setStyleSheet(u"color: black;")
        self.pin26Button = PySwitch(self.centralwidget)
        self.pin26Button.setObjectName(u"pin26Button")
        self.pin26Button.setGeometry(QRect(1383, 610, 21, 20))
        self.pin26Button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pin26Button.setStyleSheet(u"color: black;")
        self.pin27Button = PySwitch(self.centralwidget)
        self.pin27Button.setObjectName(u"pin27Button")
        self.pin27Button.setGeometry(QRect(1270, 610, 21, 20))
        self.pin27Button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pin27Button.setStyleSheet(u"color: black;")
        self.pin28Button = PySwitch(self.centralwidget)
        self.pin28Button.setObjectName(u"pin28Button")
        self.pin28Button.setGeometry(QRect(1150, 610, 21, 20))
        self.pin28Button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pin28Button.setStyleSheet(u"color: black;")
        self.pin29Button = PySwitch(self.centralwidget)
        self.pin29Button.setObjectName(u"pin29Button")
        self.pin29Button.setGeometry(QRect(1040, 610, 21, 20))
        self.pin29Button.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.pin29Button.setStyleSheet(u"color: black;")
        self.loadcellButton = PySwitch(self.centralwidget)
        self.loadcellButton.setObjectName(u"loadcellButton")
        self.loadcellButton.setGeometry(QRect(485, 610, 21, 20))
        self.loadcellButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.loadcellButton.setStyleSheet(u"color: black;")
        self.connectionSettings = QGroupBox(self.centralwidget)
        self.connectionSettings.setObjectName(u"connectionSettings")
        self.connectionSettings.setGeometry(QRect(0, 0, 231, 131))
        self.verticalLayoutWidget = QWidget(self.connectionSettings)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(9, 19, 211, 111))
        self.controlLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.controlLayout.setObjectName(u"controlLayout")
        self.controlLayout.setContentsMargins(0, 0, 0, 0)
        self.portCombo = QComboBox(self.verticalLayoutWidget)
        self.portCombo.setObjectName(u"portCombo")
        self.portCombo.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.portCombo.sizePolicy().hasHeightForWidth())
        self.portCombo.setSizePolicy(sizePolicy)
        self.portCombo.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.controlLayout.addWidget(self.portCombo)

        self.connectButton = QPushButton(self.verticalLayoutWidget)
        self.connectButton.setObjectName(u"connectButton")
        self.connectButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.controlLayout.addWidget(self.connectButton)

        self.scanPortsButton = QPushButton(self.verticalLayoutWidget)
        self.scanPortsButton.setObjectName(u"scanPortsButton")
        self.scanPortsButton.setMinimumSize(QSize(0, 0))
        self.scanPortsButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.controlLayout.addWidget(self.scanPortsButton)

        self.pinControls = QGroupBox(self.centralwidget)
        self.pinControls.setObjectName(u"pinControls")
        self.pinControls.setGeometry(QRect(0, 140, 231, 91))
        self.fullsetButton = QPushButton(self.pinControls)
        self.fullsetButton.setObjectName(u"fullsetButton")
        self.fullsetButton.setGeometry(QRect(10, 30, 211, 41))
        self.fullsetButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.fullsetButton.setStyleSheet(u"background-color: blue; font: bold")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(0, 240, 231, 111))
        self.verticalLayoutWidget_2 = QWidget(self.groupBox)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 30, 211, 81))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.loadcellTareButton = QPushButton(self.verticalLayoutWidget_2)
        self.loadcellTareButton.setObjectName(u"loadcellTareButton")
        self.loadcellTareButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.verticalLayout.addWidget(self.loadcellTareButton)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.calibrateLabel = QLabel(self.verticalLayoutWidget_2)
        self.calibrateLabel.setObjectName(u"calibrateLabel")

        self.horizontalLayout.addWidget(self.calibrateLabel)

        self.calibrateWeight = QLineEdit(self.verticalLayoutWidget_2)
        self.calibrateWeight.setObjectName(u"calibrateWeight")
        self.calibrateWeight.setCursor(QCursor(Qt.CursorShape.IBeamCursor))
        self.calibrateWeight.setInputMethodHints(Qt.InputMethodHint.ImhDigitsOnly)
        self.calibrateWeight.setDragEnabled(False)

        self.horizontalLayout.addWidget(self.calibrateWeight)

        self.runCalibrateButton = QPushButton(self.verticalLayoutWidget_2)
        self.runCalibrateButton.setObjectName(u"runCalibrateButton")
        self.runCalibrateButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.horizontalLayout.addWidget(self.runCalibrateButton)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.groupBox_2 = QGroupBox(self.centralwidget)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(-1, 349, 231, 321))
        self.groupBox_3 = QGroupBox(self.groupBox_2)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(0, 20, 229, 61))
        self.verticalLayoutWidget_4 = QWidget(self.groupBox_3)
        self.verticalLayoutWidget_4.setObjectName(u"verticalLayoutWidget_4")
        self.verticalLayoutWidget_4.setGeometry(QRect(10, 0, 211, 51))
        self.verticalLayout_3 = QVBoxLayout(self.verticalLayoutWidget_4)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.verticalLayoutWidget_4)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setIndent(0)

        self.verticalLayout_3.addWidget(self.label_2)

        self.fanSlider = QSlider(self.verticalLayoutWidget_4)
        self.fanSlider.setObjectName(u"fanSlider")
        sizePolicy.setHeightForWidth(self.fanSlider.sizePolicy().hasHeightForWidth())
        self.fanSlider.setSizePolicy(sizePolicy)
        self.fanSlider.setAutoFillBackground(True)
        self.fanSlider.setSliderPosition(0)
        self.fanSlider.setOrientation(Qt.Orientation.Horizontal)

        self.verticalLayout_3.addWidget(self.fanSlider)

        self.groupBox_4 = QGroupBox(self.groupBox_2)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.groupBox_4.setGeometry(QRect(0, 80, 229, 111))
        self.verticalLayoutWidget_5 = QWidget(self.groupBox_4)
        self.verticalLayoutWidget_5.setObjectName(u"verticalLayoutWidget_5")
        self.verticalLayoutWidget_5.setGeometry(QRect(10, 10, 211, 91))
        self.verticalLayout_4 = QVBoxLayout(self.verticalLayoutWidget_5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.heartbeatCheckBox = PySwitch(self.verticalLayoutWidget_5)
        self.heartbeatCheckBox.setObjectName(u"heartbeatCheckBox")
        self.heartbeatCheckBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.heartbeatCheckBox.setStyleSheet(u"color: white;")

        self.verticalLayout_4.addWidget(self.heartbeatCheckBox)

        self.continuousCheckBox = PySwitch(self.verticalLayoutWidget_5)
        self.continuousCheckBox.setObjectName(u"continuousCheckBox")
        self.continuousCheckBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.continuousCheckBox.setStyleSheet(u"color: white;")

        self.verticalLayout_4.addWidget(self.continuousCheckBox)

        self.temperatureCheckBox = PySwitch(self.verticalLayoutWidget_5)
        self.temperatureCheckBox.setObjectName(u"temperatureCheckBox")
        self.temperatureCheckBox.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.temperatureCheckBox.setStyleSheet(u"color: white;")

        self.verticalLayout_4.addWidget(self.temperatureCheckBox)

        self.bootButton = QPushButton(self.groupBox_2)
        self.bootButton.setObjectName(u"bootButton")
        self.bootButton.setGeometry(QRect(10, 270, 211, 41))
        self.bootButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.bootButton.setStyleSheet(u"background-color: red;\n"
"color: black; font: bold;")
        self.bootButton.setAutoDefault(False)
        self.bootButton.setFlat(False)
        self.testGroupBox = QGroupBox(self.groupBox_2)
        self.testGroupBox.setObjectName(u"testGroupBox")
        self.testGroupBox.setGeometry(QRect(-1, 189, 231, 81))
        self.testButton = QPushButton(self.testGroupBox)
        self.testButton.setObjectName(u"testButton")
        self.testButton.setGeometry(QRect(20, 20, 191, 51))
        self.testButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.testButton.setStyleSheet(u"background-color: green")
        self.logScreen = QTextEdit(self.centralwidget)
        self.logScreen.setObjectName(u"logScreen")
        self.logScreen.setGeometry(QRect(1010, 150, 371, 331))
        self.logScreen.setAutoFillBackground(False)
        self.logScreen.setStyleSheet(u"background-color: black; color #00FF00; font-family: Consolas;")
        self.logScreen.setReadOnly(True)
        self.pin22Label = QLabel(self.centralwidget)
        self.pin22Label.setObjectName(u"pin22Label")
        self.pin22Label.setGeometry(QRect(1024, 70, 71, 41))
        self.pin22Label.setStyleSheet(u"color: black; font: bold;")
        self.pin22Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin23Label = QLabel(self.centralwidget)
        self.pin23Label.setObjectName(u"pin23Label")
        self.pin23Label.setGeometry(QRect(1139, 70, 71, 41))
        self.pin23Label.setStyleSheet(u"color: black; font: bold;")
        self.pin23Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin24Label = QLabel(self.centralwidget)
        self.pin24Label.setObjectName(u"pin24Label")
        self.pin24Label.setGeometry(QRect(1254, 70, 71, 41))
        self.pin24Label.setStyleSheet(u"color: black; font: bold;")
        self.pin24Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin25Label = QLabel(self.centralwidget)
        self.pin25Label.setObjectName(u"pin25Label")
        self.pin25Label.setGeometry(QRect(1370, 70, 71, 41))
        self.pin25Label.setStyleSheet(u"color: black; font: bold;")
        self.pin25Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.RFIDLabel = QLabel(self.centralwidget)
        self.RFIDLabel.setObjectName(u"RFIDLabel")
        self.RFIDLabel.setGeometry(QRect(1460, 320, 71, 41))
        self.RFIDLabel.setStyleSheet(u"color: black; font: bold;")
        self.RFIDLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin26Label = QLabel(self.centralwidget)
        self.pin26Label.setObjectName(u"pin26Label")
        self.pin26Label.setGeometry(QRect(1370, 550, 71, 41))
        self.pin26Label.setStyleSheet(u"color: black; font: bold;")
        self.pin26Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin27Label = QLabel(self.centralwidget)
        self.pin27Label.setObjectName(u"pin27Label")
        self.pin27Label.setGeometry(QRect(1254, 550, 71, 41))
        self.pin27Label.setStyleSheet(u"color: black; font: bold;")
        self.pin27Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin28Label = QLabel(self.centralwidget)
        self.pin28Label.setObjectName(u"pin28Label")
        self.pin28Label.setGeometry(QRect(1139, 550, 71, 41))
        self.pin28Label.setStyleSheet(u"color: black; font: bold;")
        self.pin28Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.pin29Label = QLabel(self.centralwidget)
        self.pin29Label.setObjectName(u"pin29Label")
        self.pin29Label.setGeometry(QRect(1024, 550, 71, 41))
        self.pin29Label.setStyleSheet(u"color: black; font: bold;")
        self.pin29Label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loadcellLabel = QLabel(self.centralwidget)
        self.loadcellLabel.setObjectName(u"loadcellLabel")
        self.loadcellLabel.setGeometry(QRect(468, 560, 71, 31))
        self.loadcellLabel.setStyleSheet(u"color: black; font: bold;")
        self.loadcellLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.groupBox_5 = QGroupBox(self.centralwidget)
        self.groupBox_5.setObjectName(u"groupBox_5")
        self.groupBox_5.setGeometry(QRect(310, 180, 291, 291))
        self.groupBox_5.setAutoFillBackground(False)
        self.groupBox_5.setStyleSheet(u"QGroupBox {\n"
"border: 2px solid gray;\n"
"border-color: black;\n"
"font-size: 14px;\n"
"border-radius: 15px;\n"
"}\n"
"QGroupBox::title {\n"
"border-top-left-radius: 5px;\n"
"border-top-right-radius: 5px;\n"
"padding: 2px 5px;\n"
"background-color: gray;\n"
"color: rgb(255, 255, 255);\n"
"}")
        self.verticalLayoutWidget_3 = QWidget(self.groupBox_5)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(9, 39, 271, 231))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.groupBox_6 = QGroupBox(self.verticalLayoutWidget_3)
        self.groupBox_6.setObjectName(u"groupBox_6")
        self.horizontalLayoutWidget = QWidget(self.groupBox_6)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 0, 251, 51))
        self.horizontalLayout_2 = QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.loadcellValueLabel = QLabel(self.horizontalLayoutWidget)
        self.loadcellValueLabel.setObjectName(u"loadcellValueLabel")
        self.loadcellValueLabel.setStyleSheet(u"color: blue; font-weight: bold; font-size: 24px")
        self.loadcellValueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.loadcellValueLabel.setWordWrap(False)

        self.horizontalLayout_2.addWidget(self.loadcellValueLabel)


        self.verticalLayout_2.addWidget(self.groupBox_6)

        self.groupBox_7 = QGroupBox(self.verticalLayoutWidget_3)
        self.groupBox_7.setObjectName(u"groupBox_7")
        self.horizontalLayoutWidget_2 = QWidget(self.groupBox_7)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 0, 251, 51))
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.heartbeatValueLabel = QLabel(self.horizontalLayoutWidget_2)
        self.heartbeatValueLabel.setObjectName(u"heartbeatValueLabel")
        self.heartbeatValueLabel.setStyleSheet(u"color: blue; font-weight: bold; font-size: 24px")
        self.heartbeatValueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.heartbeatValueLabel.setWordWrap(False)

        self.horizontalLayout_4.addWidget(self.heartbeatValueLabel)


        self.verticalLayout_2.addWidget(self.groupBox_7)

        self.groupBox_8 = QGroupBox(self.verticalLayoutWidget_3)
        self.groupBox_8.setObjectName(u"groupBox_8")
        self.horizontalLayoutWidget_3 = QWidget(self.groupBox_8)
        self.horizontalLayoutWidget_3.setObjectName(u"horizontalLayoutWidget_3")
        self.horizontalLayoutWidget_3.setGeometry(QRect(10, 0, 251, 51))
        self.horizontalLayout_5 = QHBoxLayout(self.horizontalLayoutWidget_3)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.temperatureValueLabel = QLabel(self.horizontalLayoutWidget_3)
        self.temperatureValueLabel.setObjectName(u"temperatureValueLabel")
        self.temperatureValueLabel.setStyleSheet(u"color: blue; font-weight: bold; font-size: 24px")
        self.temperatureValueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.temperatureValueLabel.setWordWrap(False)

        self.horizontalLayout_5.addWidget(self.temperatureValueLabel)


        self.verticalLayout_2.addWidget(self.groupBox_8)

        self.groupBox_9 = QGroupBox(self.verticalLayoutWidget_3)
        self.groupBox_9.setObjectName(u"groupBox_9")
        self.horizontalLayoutWidget_4 = QWidget(self.groupBox_9)
        self.horizontalLayoutWidget_4.setObjectName(u"horizontalLayoutWidget_4")
        self.horizontalLayoutWidget_4.setGeometry(QRect(10, 0, 251, 51))
        self.horizontalLayout_6 = QHBoxLayout(self.horizontalLayoutWidget_4)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.RFIDValueLabel = QLabel(self.horizontalLayoutWidget_4)
        self.RFIDValueLabel.setObjectName(u"RFIDValueLabel")
        self.RFIDValueLabel.setStyleSheet(u"color: blue; font-weight: bold; font-size: 24px")
        self.RFIDValueLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.RFIDValueLabel.setWordWrap(False)

        self.horizontalLayout_6.addWidget(self.RFIDValueLabel)


        self.verticalLayout_2.addWidget(self.groupBox_9)

        self.clearButton = QPushButton(self.centralwidget)
        self.clearButton.setObjectName(u"clearButton")
        self.clearButton.setGeometry(QRect(1010, 480, 371, 26))
        self.clearButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.clearButton.setStyleSheet(u"background-color: red")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.bootButton.setDefault(False)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText("")
        self.pin22Button.setText("")
        self.pin23Button.setText("")
        self.pin24Button.setText("")
        self.pin25Button.setText("")
        self.RFIDButton.setText("")
        self.pin26Button.setText("")
        self.pin27Button.setText("")
        self.pin28Button.setText("")
        self.pin29Button.setText("")
        self.loadcellButton.setText("")
        self.connectionSettings.setTitle(QCoreApplication.translate("MainWindow", u"Ba\u011flant\u0131 Ayarlar\u0131", None))
        self.connectButton.setText(QCoreApplication.translate("MainWindow", u"Ba\u011flant\u0131y\u0131 Kur", None))
        self.scanPortsButton.setText(QCoreApplication.translate("MainWindow", u"Portlar\u0131 Tara", None))
        self.pinControls.setTitle(QCoreApplication.translate("MainWindow", u"Pin Kontrol", None))
        self.fullsetButton.setText(QCoreApplication.translate("MainWindow", u"Fullset", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Loadcell \u0130\u015flemleri", None))
        self.loadcellTareButton.setText(QCoreApplication.translate("MainWindow", u"Dara Al (Tare)", None))
        self.calibrateLabel.setText(QCoreApplication.translate("MainWindow", u"gr :", None))
        self.calibrateWeight.setInputMask("")
        self.calibrateWeight.setText(QCoreApplication.translate("MainWindow", u"2800", None))
        self.calibrateWeight.setPlaceholderText("")
        self.runCalibrateButton.setText(QCoreApplication.translate("MainWindow", u"Kalibrasyon Ba\u015flat", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MainWindow", u"Fan ve Di\u011fer Mod\u00fcller", None))
        self.groupBox_3.setTitle("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Fan H\u0131z\u0131:", None))
        self.groupBox_4.setTitle("")
        self.heartbeatCheckBox.setText(QCoreApplication.translate("MainWindow", u"Heartbeat Aktif", None))
        self.continuousCheckBox.setText(QCoreApplication.translate("MainWindow", u"S\u00fcrekli Veri Aktif", None))
        self.temperatureCheckBox.setText(QCoreApplication.translate("MainWindow", u"S\u0131cakl\u0131k Sens\u00f6r\u00fc Aktif", None))
        self.bootButton.setText(QCoreApplication.translate("MainWindow", u"USB BOOT (G\u00fcncelleme)", None))
        self.testGroupBox.setTitle(QCoreApplication.translate("MainWindow", u"Test", None))
        self.testButton.setText(QCoreApplication.translate("MainWindow", u"Testi Ba\u015flat", None))
        self.logScreen.setPlaceholderText(QCoreApplication.translate("MainWindow", u"Karttan gelen veriler burada yazacak", None))
        self.pin22Label.setText(QCoreApplication.translate("MainWindow", u"Pin 22\n"
"Sick F", None))
        self.pin23Label.setText(QCoreApplication.translate("MainWindow", u"Pin 23\n"
"Sick D", None))
        self.pin24Label.setText(QCoreApplication.translate("MainWindow", u"Pin 24\n"
"Sick C", None))
        self.pin25Label.setText(QCoreApplication.translate("MainWindow", u"Pin 25\n"
"Sick Reset", None))
        self.RFIDLabel.setText(QCoreApplication.translate("MainWindow", u"RFID", None))
        self.pin26Label.setText(QCoreApplication.translate("MainWindow", u"Pin 26\n"
"Buzzer", None))
        self.pin27Label.setText(QCoreApplication.translate("MainWindow", u"Pin 27\n"
"LED Red", None))
        self.pin28Label.setText(QCoreApplication.translate("MainWindow", u"Pin 28\n"
"LED Blue", None))
        self.pin29Label.setText(QCoreApplication.translate("MainWindow", u"Pin 29\n"
"LED Green", None))
        self.loadcellLabel.setText(QCoreApplication.translate("MainWindow", u"Loadcell", None))
        self.groupBox_5.setTitle(QCoreApplication.translate("MainWindow", u"Canl\u0131 Veri", None))
        self.groupBox_6.setTitle(QCoreApplication.translate("MainWindow", u"LOADCELL", None))
        self.loadcellValueLabel.setText(QCoreApplication.translate("MainWindow", u"---", None))
        self.groupBox_7.setTitle(QCoreApplication.translate("MainWindow", u"HEARTBEAT", None))
        self.heartbeatValueLabel.setText(QCoreApplication.translate("MainWindow", u"---", None))
        self.groupBox_8.setTitle(QCoreApplication.translate("MainWindow", u"SICAKLIK", None))
        self.temperatureValueLabel.setText(QCoreApplication.translate("MainWindow", u"---", None))
        self.groupBox_9.setTitle(QCoreApplication.translate("MainWindow", u"RFID", None))
        self.RFIDValueLabel.setText(QCoreApplication.translate("MainWindow", u"---", None))
        self.clearButton.setText(QCoreApplication.translate("MainWindow", u"Terminali Temizle", None))
    # retranslateUi

