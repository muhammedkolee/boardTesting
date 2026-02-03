import sys
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import (QApplication, QWidget, QGridLayout, QVBoxLayout, QHBoxLayout, QPushButton, QComboBox, QLabel, QMessageBox, QTextEdit, QSlider, QLineEdit, QGroupBox, QCheckBox)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QFont

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.serialConnect = None

        # Default values of Pins and others
        self.pin22 = False
        self.pin23 = False
        self.pin24 = False
        self.pin25 = False
        self.pin26 = False
        self.pin27 = False
        self.pin28 = False
        self.pin29 = False
        self.loadcellActive = False
        self.RFID = False
        self.continuousData = True
        self.tempActive = True
        
        # Data holders
        self.lastLoadcellValue = "---"
        self.lastHeartbeat = "---"
        self.lastTemperature = "---"
        self.lastRFID = "---"
        
        self.init_ui()

        # Every 10 milliseconds, check card's response.
        self.readTimer = QTimer()
        self.readTimer.timeout.connect(self.readSerialData)
        self.readTimer.start(10)

    def init_ui(self):
        # Main Layout
        mainLayout = QHBoxLayout()

        # Control Layout
        controlLayout = QVBoxLayout()
        
        # Connection Layout
        connectionSettings = QGroupBox("Bağlantı Ayarları")
        connectionLayout = QVBoxLayout()
        self.portCombo = QComboBox()
        self.scanPorts()
        self.connectButton = QPushButton("Bağlantıyı Kur")
        self.scanPortsButton = QPushButton("Portları Tara")
        self.connectButton.clicked.connect(self.manageConnections)
        self.scanPortsButton.clicked.connect(self.scanPorts)
        connectionLayout.addWidget(self.portCombo)
        connectionLayout.addWidget(self.connectButton)
        connectionLayout.addWidget(self.scanPortsButton )
        connectionSettings.setLayout(connectionLayout)
        controlLayout.addWidget(connectionSettings)

        # GPIO Pins Controls
        pinControls = QGroupBox("Pin Kontrol (Mosfet 22-29)")
        pinLayout = QGridLayout()

        # Create pin buttons
        self.pinButton22 = QPushButton("PIN 22")
        self.pinButton23 = QPushButton("PIN 23")
        self.pinButton24 = QPushButton("PIN 24")
        self.pinButton25 = QPushButton("PIN 25")
        self.pinButton26 = QPushButton("PIN 26")
        self.pinButton27 = QPushButton("PIN 27")
        self.pinButton28 = QPushButton("PIN 28")
        self.pinButton29 = QPushButton("PIN 29")

        # When click pin buttons
        self.pinButton22.clicked.connect(self.togglePin22)
        self.pinButton23.clicked.connect(self.togglePin23)
        self.pinButton24.clicked.connect(self.togglePin24)
        self.pinButton25.clicked.connect(self.togglePin25)
        self.pinButton26.clicked.connect(self.togglePin26)
        self.pinButton27.clicked.connect(self.togglePin27)
        self.pinButton28.clicked.connect(self.togglePin28)
        self.pinButton29.clicked.connect(self.togglePin29)

        # Style for pin buttons
        for button in [self.pinButton22, self.pinButton23, self.pinButton24, self.pinButton25, self.pinButton26, self.pinButton27, self.pinButton28, self.pinButton29]:
            button.setStyleSheet("background-color: red; color: white;")
        
        # Fullset Button
        self.FullsetButton = QPushButton("Fullset")
        self.FullsetButton.clicked.connect(self.runFullset)
        self.FullsetButton.setStyleSheet("background-color: blue; color: white;")
        
        # Layout for pins
        pinLayout.addWidget(self.pinButton22, 0, 0)
        pinLayout.addWidget(self.pinButton23, 0, 1)
        pinLayout.addWidget(self.pinButton24, 0, 2)
        pinLayout.addWidget(self.pinButton25, 1, 0)
        pinLayout.addWidget(self.pinButton26, 1, 1)
        pinLayout.addWidget(self.pinButton27, 1, 2)
        pinLayout.addWidget(self.pinButton28, 2, 0)
        pinLayout.addWidget(self.pinButton29, 2, 1)
        pinLayout.addWidget(self.FullsetButton, 2, 2)
        pinControls.setLayout(pinLayout)
        controlLayout.addWidget(pinControls)

        # Loadcell Controls
        loadcellControls = QGroupBox("Loadcell İşlemleri")
        loadcellLayout = QVBoxLayout()
        
        self.loadcellButton = QPushButton("Loadcell Aktif Et")
        self.loadcellButton.clicked.connect(self.toggleLoadcell)
        
        self.loadcellTareButton = QPushButton("Dara Al (Tare)")
        self.loadcellTareButton.clicked.connect(lambda: self.sendCommand("CMD SET LOADCELL_TARE 0"))

        hLayout = QHBoxLayout()
        self.calibrateWeight = QLineEdit("2800")
        self.runCalibrateButton = QPushButton("Kalibrasyon Başlat")
        self.runCalibrateButton.clicked.connect(self.runCalibrateS1)
        hLayout.addWidget(QLabel("Ağırlık (gr):"))
        hLayout.addWidget(self.calibrateWeight)
        hLayout.addWidget(self.runCalibrateButton)

        loadcellLayout.addWidget(self.loadcellButton)
        loadcellLayout.addWidget(self.loadcellTareButton)
        loadcellLayout.addLayout(hLayout)
        loadcellControls.setLayout(loadcellLayout)
        controlLayout.addWidget(loadcellControls)

        # Fan ve Diğer Sensörler
        otherSensors = QGroupBox("Fan ve Modüller")
        otherLayout = QVBoxLayout()
        
        # Fan Slider
        self.fanSlider = QSlider(Qt.Horizontal)
        self.fanSlider.setRange(0, 100)
        self.fanSlider.valueChanged.connect(self.changeFanSpeed)
        self.fanLabel = QLabel("Fan Hızı: %0")
        
        self.HeartbeatCheckBox = QCheckBox("Heartbeat Aktif")
        self.HeartbeatCheckBox.stateChanged.connect(lambda s: self.updateHeartbeat(s))
        
        self.RFIDButton = QPushButton("RFID Aktif Et")
        self.RFIDButton.clicked.connect(self.activeRFID)
        
        # Continuous Data Button
        self.continuousDataButton = QPushButton("Sürekli Veri: KAPALI")
        self.continuousDataButton.setStyleSheet("background-color: gray; color: white;")
        self.continuousDataButton.clicked.connect(self.toggleContinuousData)
        
        # Temperature Sensor Button
        self.tempButton = QPushButton("Sıcaklık Sensörü: KAPALI")
        self.tempButton.setStyleSheet("background-color: gray; color: white;")
        self.tempButton.clicked.connect(self.toggleTemperature)
        
        self.bootButton = QPushButton("USB BOOT (Güncelleme)")
        self.bootButton.setStyleSheet("background-color: red; color: white;")
        self.bootButton.clicked.connect(lambda: self.sendCommand("CMD SET USB_BOOT 1"))

        otherLayout.addWidget(self.fanLabel)
        otherLayout.addWidget(self.fanSlider)
        otherLayout.addWidget(self.HeartbeatCheckBox)
        otherLayout.addWidget(self.RFIDButton)
        otherLayout.addWidget(self.continuousDataButton)
        otherLayout.addWidget(self.tempButton)
        otherLayout.addWidget(self.bootButton)
        otherSensors.setLayout(otherLayout)
        controlLayout.addWidget(otherSensors)

        controlLayout.addStretch()

        # Data Display Layout
        dataDisplayLayout = QVBoxLayout()
        dataDisplayLayout.addWidget(QLabel("CANLI VERİ GÖSTERİMİ"))
        
        # Loadcell Display
        self.loadcellFrame = self.createDataFrame("LOADCELL", "---")
        dataDisplayLayout.addWidget(self.loadcellFrame)
        
        # Heartbeat Display
        self.heartbeatFrame = self.createDataFrame("HEARTBEAT", "---")
        dataDisplayLayout.addWidget(self.heartbeatFrame)
        
        # Temperature Display
        self.temperatureFrame = self.createDataFrame("SICAKLIK", "---")
        dataDisplayLayout.addWidget(self.temperatureFrame)
        
        # RFID Display
        self.rfidFrame = self.createDataFrame("RFID", "---")
        dataDisplayLayout.addWidget(self.rfidFrame)
        
        dataDisplayLayout.addStretch()

        # Log Layout
        logLayout = QVBoxLayout()
        logLayout.addWidget(QLabel("Terminal / Gelen Veri Log:"))
        self.logScreen = QTextEdit()
        self.logScreen.setReadOnly(True)
        self.logScreen.setStyleSheet("background-color: black; color: white;")
        logLayout.addWidget(self.logScreen)
        
        # Clear Button
        clearButton = QPushButton("Logu Temizle")
        clearButton.clicked.connect(lambda: self.logScreen.clear())
        logLayout.addWidget(clearButton)

        # Merge Layouts
        mainLayout.addLayout(controlLayout, 1)
        mainLayout.addLayout(dataDisplayLayout, 1)
        mainLayout.addLayout(logLayout, 2)
        
        self.setLayout(mainLayout)
        self.setWindowTitle('Kart Test Uygulaması')
        self.resize(1200, 700)

    def createDataFrame(self, title, initial_value):
        frame = QGroupBox(title)
        layout = QVBoxLayout()
        
        valueLabel = QLabel(initial_value)
        valueLabel.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(18)
        font.setBold(True)
        valueLabel.setFont(font)
        valueLabel.setStyleSheet("color: blue;")
        
        layout.addWidget(valueLabel)
        frame.setLayout(layout)
        layout.addWidget(valueLabel)
        frame.setLayout(layout)
        frame.setStyleSheet("QGroupBox { border: 2px solid #ccc; border-radius: 5px; margin-top: 10px; }"
                           "QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }")
        
        
        # Store reference to label for updating
        if title == "LOADCELL":
            self.loadcellValueLabel = valueLabel
        elif title == "HEARTBEAT":
            self.heartbeatValueLabel = valueLabel
        elif title == "SICAKLIK":
            self.temperatureValueLabel = valueLabel
        elif title == "RFID":
            self.rfidValueLabel = valueLabel
            
        return frame

    def updateDataDisplay(self, data_type, value):
        if data_type == "LOADCELL":
            self.loadcellValueLabel.setText(f"{value} gr")
            self.lastLoadcellValue = value
        elif data_type == "HEARTBEAT":
            self.heartbeatValueLabel.setText(value)
            self.lastHeartbeat = value
        elif data_type == "TEMPERATURE":
            self.temperatureValueLabel.setText(f"{value} °C")
            self.lastTemperature = value
        elif data_type == "RFID":
            self.rfidValueLabel.setText(value)
            self.lastRFID = value

    def toggleContinuousData(self):
        if self.continuousData:
            self.sendCommand("CMD SET SEND_DATA_CONTINUOUSLY 0")
            self.continuousDataButton.setText("Sürekli Veri: KAPALI")
            self.continuousDataButton.setStyleSheet("background-color: #555; color: white;")
            self.continuousData = False
        else:
            self.sendCommand("CMD SET SEND_DATA_CONTINUOUSLY 1")
            self.continuousDataButton.setText("Sürekli Veri: AÇIK")
            self.continuousDataButton.setStyleSheet("background-color: green; color: white;")
            self.continuousData = True

    def toggleTemperature(self):
        if self.tempActive:
            self.sendCommand("CMD SET TEMP_ACTIVE 0")
            self.tempButton.setText("Sıcaklık Sensörü: KAPALI")
            self.tempButton.setStyleSheet("background-color: #555; color: white;")
            self.tempActive = False
        else:
            self.sendCommand("CMD SET TEMP_ACTIVE 1")
            self.tempButton.setText("Sıcaklık Sensörü: AÇIK")
            self.tempButton.setStyleSheet("background-color: green; color: white;")
            self.tempActive = True

    # Pin Functions
    def togglePin22(self):
        if self.pin22:
            self.sendCommand("CMD SET 22 0")
            self.pinButton22.setStyleSheet("background-color: red; color: white;")
            self.pin22 = False
        else:
            self.sendCommand("CMD SET 22 1")
            self.pinButton22.setStyleSheet("background-color: green;")
            self.pin22 = True
            QTimer.singleShot(5000, self.resPin22)
    
    def resPin22(self):
        self.pinButton22.setStyleSheet("background-color: red; color: white;")
        self.pin22 = False

    def togglePin23(self):
        if self.pin23:
            self.sendCommand("CMD SET 23 0")
            self.pinButton23.setStyleSheet("background-color: red; color: white;")
            self.pin23 = False
        else:
            self.sendCommand("CMD SET 23 1")
            self.pinButton23.setStyleSheet("background-color: green;")
            self.pin23 = True
            QTimer.singleShot(5000, lambda: self.pinButton23.setStyleSheet("background-color: red; color: white;"))

    def resPin23(self):
        self.pinButton23.setStyleSheet("background-color: red; color: white;")
        self.pin23 = False

    def togglePin24(self):
        if self.pin24:
            self.sendCommand("CMD SET 24 0")
            self.pinButton24.setStyleSheet("background-color: red; color: white;")            
            self.pin24 = False
        else:
            self.sendCommand("CMD SET 24 1")
            self.pinButton24.setStyleSheet("background-color: green;")
            self.pin24 = True
            QTimer.singleShot(5000, lambda: self.pinButton24.setStyleSheet("background-color: red; color: white;"))

    def resPin24(self):
        self.pinButton24.setStyleSheet("background-color: red; color: white;")
        self.pin24 = False

    def togglePin25(self):
        if self.pin25:
            self.sendCommand("CMD SET 25 0")
            self.pinButton25.setStyleSheet("background-color: red; color: white;")
            self.pin25 = False
        else:
            self.sendCommand("CMD SET 25 1")
            self.pinButton25.setStyleSheet("background-color: green;")
            self.pin25 = True
            QTimer.singleShot(5000, lambda: self.pinButton25.setStyleSheet("background-color: red; color: white;"))

    def resPin25(self):
        self.pinButton25.setStyleSheet("background-color: red; color: white;")
        self.pin25 = False

    def togglePin26(self):
        if self.pin26:
            self.sendCommand("CMD SET 26 0")
            self.pinButton26.setStyleSheet("background-color: red; color: white;")
            self.pin26 = False
        else:
            self.sendCommand("CMD SET 26 1")
            self.pinButton26.setStyleSheet("background-color: green;")
            self.pin26 = True

    def togglePin27(self):
        if self.pin27:
            self.sendCommand("CMD SET 27 0")
            self.pinButton27.setStyleSheet("background-color: red; color: white;")
            self.pin27 = False
        else:
            self.sendCommand("CMD SET 27 1")
            self.pinButton27.setStyleSheet("background-color: green;")
            self.pin27 = True

    def togglePin28(self):
        if self.pin28:
            self.sendCommand("CMD SET 28 0")
            self.pinButton28.setStyleSheet("background-color: red; color: white;")
            self.pin28 = False
        else:
            self.sendCommand("CMD SET 28 1")
            self.pinButton28.setStyleSheet("background-color: green;")
            self.pin28 = True

    def togglePin29(self):
        if self.pin29:
            self.sendCommand("CMD SET 29 0")
            self.pinButton29.setStyleSheet("background-color: red; color: white;")
            self.pin29 = False
        else:
            self.sendCommand("CMD SET 29 1")
            self.pinButton29.setStyleSheet("background-color: green;")
            self.pin29 = True

    def runFullset(self):
        self.sendCommand("CMD FULLSET 255 30 FE")
        for btn in [self.pinButton22, self.pinButton23, self.pinButton24, self.pinButton25,
                    self.pinButton26, self.pinButton27, self.pinButton28, self.pinButton29]:
            btn.setStyleSheet("background-color: green;")
        self.pin22 = self.pin23 = self.pin24 = self.pin25 = self.pin26 = self.pin27 = self.pin28 = self.pin29 = True
        self.fanSlider.setValue(30)

        QTimer.singleShot(5000, lambda: self.pinButton22.setStyleSheet("background-color: red; color: white;"))
        QTimer.singleShot(5000, lambda: self.pinButton23.setStyleSheet("background-color: red; color: white;"))
        QTimer.singleShot(5000, lambda: self.pinButton24.setStyleSheet("background-color: red; color: white;"))
        QTimer.singleShot(5000, lambda: self.pinButton25.setStyleSheet("background-color: red; color: white;"))

    def scanPorts(self):
        self.portCombo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.portCombo.addItem(port.device)

    def manageConnections(self):
        if self.serialConnect is None or not self.serialConnect.is_open:
            try:
                self.serialConnect = serial.Serial(self.portCombo.currentText(), 115200, timeout=0.1)
                self.connectButton.setText("Bağlantıyı Kes")
                self.connectButton.setStyleSheet("background-color: green; color: white;")
                self.writeLog("✓ Sistem: Bağlantı kuruldu.")
                
                # When connected, send once commands
                QTimer.singleShot(5, self.sendInitialCommands)
                
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Bağlantı hatası: {e}")
        else:
            self.serialConnect.close()
            self.connectButton.setText("Bağlantıyı Kur")
            self.connectButton.setStyleSheet("")
            self.writeLog("Sistem: Bağlantı kesildi.")

            self.loadcellButton.setText("Loadcell Aktif Et")
            self.loadcellButton.setStyleSheet("")
            self.loadcellValueLabel.setText("---")
            self.loadcellActive = False

            self.RFIDButton.setText("RFID Aktif Et")
            self.RFIDButton.setStyleSheet("")
            self.RFID = False

            self.pinButton22.setStyleSheet("background-color: red; color: white;")
            self.pinButton23.setStyleSheet("background-color: red; color: white;")
            self.pinButton24.setStyleSheet("background-color: red; color: white;")
            self.pinButton25.setStyleSheet("background-color: red; color: white;")
            self.pinButton26.setStyleSheet("background-color: red; color: white;")
            self.pinButton27.setStyleSheet("background-color: red; color: white;")
            self.pinButton28.setStyleSheet("background-color: red; color: white;")
            self.pinButton29.setStyleSheet("background-color: red; color: white;")    

    def sendInitialCommands(self):      
        # Turn all pins off
        self.sendCommand("CMD SET 22 0")
        self.sendCommand("CMD SET 23 0")
        self.sendCommand("CMD SET 24 0")
        self.sendCommand("CMD SET 25 0")
        self.sendCommand("CMD SET 26 0")
        self.sendCommand("CMD SET 27 0")
        self.sendCommand("CMD SET 28 0")
        self.sendCommand("CMD SET 29 0")

        # Turn sensors off
        self.sendCommand("CMD SET LOADCELL_ACTIVE 0")
        self.sendCommand("CMD SET LOADCELL_PUBLISH_ENABLED 0")
        self.sendCommand("CMD SET RFID_ACTIVE 0")
        
        # Activate temp. sensor and continuously data
        self.sendCommand("CMD SET TEMP_ACTIVE 1")
        self.sendCommand("CMD SET SEND_DATA_CONTINUOUSLY 1")
        
        # Update UI
        self.tempActive = True
        self.tempButton.setText("Sıcaklık Sensörü: AÇIK")
        self.tempButton.setStyleSheet("background-color: green; color: white;")
        
        self.continuousData = True
        self.continuousDataButton.setText("Sürekli Veri: AÇIK")
        self.continuousDataButton.setStyleSheet("background-color: green; color: white;")

        self.pinButton22.setStyleSheet("background-color: red; color: white;")
        self.pinButton23.setStyleSheet("background-color: red; color: white;")
        self.pinButton24.setStyleSheet("background-color: red; color: white;")
        self.pinButton25.setStyleSheet("background-color: red; color: white;")
        self.pinButton26.setStyleSheet("background-color: red; color: white;")
        self.pinButton27.setStyleSheet("background-color: red; color: white;")
        self.pinButton28.setStyleSheet("background-color: red; color: white;")
        self.pinButton29.setStyleSheet("background-color: red; color: white;")
        
        self.loadcellValueLabel.setText("---")
        self.rfidValueLabel.setText("---")
        self.heartbeatValueLabel.setText("---")

        self.writeLog("Başlangıç komutları gönderildi.")


    def sendCommand(self, komut):
        if self.serialConnect and self.serialConnect.is_open:
            try:
                self.serialConnect.write((komut + '\n').encode('utf-8'))
                self.writeLog(f"→ {komut}")
            except Exception as e:
                self.writeLog(f"Hata: Komut gönderilemedi! {e}")
        else:
            self.writeLog("Uyarı: Önce portu açmalısınız!")

    def writeLog(self, mesaj):
        self.logScreen.append(mesaj)
        self.logScreen.moveCursor(self.logScreen.textCursor().End)

    def changeFanSpeed(self):
        fanValue = self.fanSlider.value()
        self.fanLabel.setText(f"Fan Hızı: %{fanValue}")
        self.sendCommand(f"CMD SET FAN {fanValue}")

    def toggleLoadcell(self):
        if self.loadcellActive:
            self.sendCommand("CMD SET LOADCELL_ACTIVE 0")
            self.sendCommand("CMD SET LOADCELL_PUBLISH_ENABLED 0")
            self.loadcellButton.setText("Loadcell Aktif Et")
            self.loadcellButton.setStyleSheet("")
            self.loadcellValueLabel.setText("---")
            self.loadcellActive = False
        else:
            self.sendCommand("CMD SET LOADCELL_ACTIVE 1")
            self.sendCommand("CMD SET LOADCELL_PUBLISH_ENABLED 1")
            self.loadcellButton.setText("Loadcell Kapat")
            self.loadcellButton.setStyleSheet("background-color: green; color: white;")
            self.loadcellActive = True

    def runCalibrateS1(self):
        self.sendCommand(f"CMD SET LOADCELL_DO_CALIBRATION {self.calibrateWeight.text()}")
        self.message1 = QMessageBox(self)
        self.message1.setIcon(QMessageBox.Information)
        self.message1.setWindowTitle("Kalibrasyon")
        self.message1.setText("Loadcell üzerindeki bütün cisimleri kaldırın!")
        self.message1.setStandardButtons(QMessageBox.NoButton)

        QTimer.singleShot(2500, self.runCalibrateS2)
        self.message1.show()

    def runCalibrateS2(self):
        self.message1.done(0) 

        self.message2 = QMessageBox(self)    
        self.message2.setIcon(QMessageBox.Warning)
        self.message2.setWindowTitle("Kalibrasyon")
        self.message2.setText(f"10 saniye içerisinde Loadcell üzerine {self.calibrateWeight.text()} gram ağırlığında cisim yerleştirin!")
        self.message2.setStandardButtons(QMessageBox.NoButton)

        QTimer.singleShot(11000, lambda: self.message2.done(0))
        self.message2.show()

    def activeRFID(self):
        if self.RFID:
            self.RFIDButton.setText("RFID Aktif Et")
            self.RFIDButton.setStyleSheet("")
            self.sendCommand("CMD SET RFID_ACTIVE 0")
            self.rfidValueLabel.setText("---")
            self.RFID = False
        else:
            self.RFIDButton.setText("RFID Kapat")
            self.RFIDButton.setStyleSheet("background-color: green; color: white;")
            self.sendCommand("CMD SET RFID_ACTIVE 1")
            self.RFID = True

    def updateHeartbeat(self, s):
        if s == 2:
            self.sendCommand("CMD SET HEARTBEAT 1")
        else:
            self.sendCommand(f"CMD SET HEARTBEAT 0")
            QTimer.singleShot(1000, lambda: self.updateDataDisplay("HEARTBEAT", "---"))
            


    def readSerialData(self):
        if self.serialConnect and self.serialConnect.is_open:
            if self.serialConnect.in_waiting > 0:
                try:
                    line = self.serialConnect.readline().decode('utf-8').strip()
                    if line:
                        # Terminal'e her veriyi yaz
                        self.writeLog(f"← KART: {line}")

                        # VERİ PARSE ETME - Format: DATA,LC,3731.80,RF,Nan
                        if line.startswith("DATA,"):
                            try:
                                parts = line.split(",")
                                # parts[0] = "DATA"
                                # parts[1] = "LC", parts[2] = "3731.80"
                                # parts[3] = "RF", parts[4] = "Nan"
                                # İndeksleri çiftler halinde işle
                                i = 1
                                while i < len(parts) - 1:
                                    key = parts[i]
                                    value = parts[i + 1]
                                    
                                    if key == "LC":  # LoadCell
                                        self.updateDataDisplay("LOADCELL", value)
                                    elif key == "RF":  # RFID
                                        self.updateDataDisplay("RFID", value)
                                    elif key == "HB":  # Heartbeat
                                        self.updateDataDisplay("HEARTBEAT", value)
                                    elif key == "TMP" or key == "TP" or key == "TEMP":  # Temperature
                                        self.updateDataDisplay("TEMPERATURE", value)
                                    
                                    i += 2
                            except Exception as e:
                                self.writeLog(f"Parse hatası: {e}")
                        
                        # HEARTBEAT format: "HEARTBEAT 7132419"
                        elif line.startswith("HEARTBEAT "):
                            try:
                                value = line.split()[1]  # "HEARTBEAT" sonrası değer
                                self.updateDataDisplay("HEARTBEAT", value)
                            except:
                                pass
                        
                        # TEMPERATURE formats: "TEMP 25.5" or "TEMPERATURE 25.5"
                        elif line.startswith("TEMP ") or line.startswith("TEMPERATURE "):
                            try:
                                value = line.split()[1]
                                self.updateDataDisplay("TEMPERATURE", value)
                            except:
                                pass
                        
                        # Diğer formatlar için destek
                        elif "LOADCELL:" in line or "WEIGHT:" in line:
                            try:
                                value = line.split(":")[-1].strip().split()[0]
                                self.updateDataDisplay("LOADCELL", value)
                            except:
                                pass
                        
                        elif "HEARTBEAT:" in line or "HB:" in line:
                            try:
                                value = line.split(":")[-1].strip()
                                self.updateDataDisplay("HEARTBEAT", value)
                            except:
                                pass
                        
                        elif "TEMP:" in line or "TEMPERATURE:" in line:
                            try:
                                value = line.split(":")[-1].strip().split()[0]
                                self.updateDataDisplay("TEMPERATURE", value)
                            except:
                                pass
                        
                        elif "RFID:" in line or "CARD:" in line:
                            try:
                                value = line.split(":")[-1].strip()
                                self.updateDataDisplay("RFID", value)
                            except:
                                pass

                        # ÖZEL DURUM KONTROLÜ
                        if "OK LOADCELL_DO_CALIBRATION" in line:
                            self.response = QMessageBox(self)
                            self.response.setIcon(QMessageBox.Information)
                            self.response.setWindowTitle("Kalibrasyon Değeri")
                            self.response.setText(f"Belirlenen kalibrasyon değeri: {line[26:34]}")
                            self.response.setDefaultButton(QMessageBox.Ok)
                            self.response.show()
                            
                except Exception as e:
                    pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    pencere = Window()
    pencere.show()
    sys.exit(app.exec_())