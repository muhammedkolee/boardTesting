import sys
from PySide6.QtWidgets import QApplication, QMainWindow, QMessageBox
from PySide6.QtCore import QTimer
from PySide6.QtGui import QTextCursor
import serial
import serial.tools.list_ports
from beeboard import Ui_MainWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.serialConnect = None

        # Default values
        self.loadcellActive = self.RFID = False
        self.continuousData = self.tempActive = True
        self.pinButtons = {} 

        #2 Create and setup UI
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.showMaximized()

        # Scan ports for boards
        self.scanPorts()

        # Connect buttons to functions
        self.ui.connectButton.clicked.connect(self.manageConnections)
        self.ui.scanPortsButton.clicked.connect(self.scanPorts)
        self.ui.fullsetButton.clicked.connect(self.runFullset)
        self.ui.loadcellButton.clicked.connect(self.toggleLoadcell)
        self.ui.runCalibrateButton.clicked.connect(self.runCalibrateS1)
        self.ui.fanSlider.setRange(0, 100)
        self.ui.fanSlider.valueChanged.connect(self.changeFanSpeed)
        self.ui.label_2.setText("Fan Hızı: %0")

        self.ui.heartbeatCheckBox.clicked.connect(self.updateHeartbeat)
        self.ui.RFIDButton.clicked.connect(self.activeRFID)
        self.ui.continuousCheckBox.clicked.connect(self.toggleContinuousData)
        self.ui.temperatureCheckBox.clicked.connect(self.toggleTemperature)
        self.ui.bootButton.clicked.connect(lambda: self.sendCommand("CMD SET USB_BOOT 1"))
        self.ui.clearButton.clicked.connect(self.ui.logScreen.clear)
        self.ui.loadcellTareButton.clicked.connect(self.runTare)

        self.ui.testButton.clicked.connect(self.runTest)

        # Dynamic Pin Names
        for pin in range(22, 30):
            button_name = f"pin{pin}Button"
            self.btn = getattr(self.ui, button_name)
            
            self.pinButtons[pin] = self.btn
            
            self.btn.clicked.connect(lambda checked=False, p=pin: self.togglePin(p))

        # Timer to read terminal
        self.readTimer = QTimer()
        self.readTimer.timeout.connect(self.readSerialData)
        self.readTimer.start(10)

    # Read data from board
    def readSerialData(self):
        if self.serialConnect and self.serialConnect.is_open:
            if self.serialConnect.in_waiting > 0:
                try:
                    line = self.serialConnect.readline().decode('utf-8').strip()
                    if not line: return
                    self.writeLog(f"<= {line}")

                    if line.startswith("DATA,"):
                        parts = line.split(",")
                        for i in range(1, len(parts)-1, 2):
                            key, val = parts[i], parts[i+1]
                            if key == "LC": self.ui.loadcellValueLabel.setText(f"{val} gr")
                            elif key == "RF": self.ui.RFIDValueLabel.setText(val)
                            elif key == "HB": self.ui.heartbeatValueLabel.setText(val)
                            elif key in ["TMP", "TP", "TEMP"]: self.ui.temperatureValueLabel.setText(f"{val} °C")
                    
                    elif line.startswith("HEARTBEAT "): self.ui.heartbeatValueLabel.setText(line.split()[1])
                    elif line.startswith("TEMP "): self.ui.temperatureValueLabel.setText(f"{line.split()[1]} °C")
                except: pass

    # Connections Function for ports
    def manageConnections(self):
        if self.serialConnect is None or not self.serialConnect.is_open:
            try:
                self.serialConnect = serial.Serial(self.ui.portCombo.currentText(), 115200, timeout=0.1)
                self.ui.connectButton.setText("Bağlantıyı Kes")
                QTimer.singleShot(50, self.sendInitialCommands)
            except Exception as e:
                QMessageBox.critical(self, "Hata", f"Bağlantı hatası: {e}")
        else:
            self.serialConnect.close()
            self.serialConnect = None
            self.ui.connectButton.setText("Bağlantıyı Kur")
            self.ui.connectButton.setStyleSheet("")
            self.writeLog("Sistem: Bağlantı kesildi.")

    # To write terminal
    def writeLog(self, message):
        self.ui.logScreen.append(message)
        self.ui.logScreen.moveCursor(QTextCursor.MoveOperation.End)

    # Inital Commands
    def sendInitialCommands(self):
        for pin in range(22, 30): self.sendCommand(f"CMD SET {pin} 0")
        self.sendCommand("CMD SET LOADCELL_ACTIVE 0")
        self.sendCommand("CMD SET RFID_ACTIVE 0")
        self.sendCommand("CMD SET TEMP_ACTIVE 1")
        self.sendCommand("CMD SET SEND_DATA_CONTINUOUSLY 1")
        self.sendCommand("CMD SET HEARTBEAT 0")

        self.ui.continuousCheckBox.setChecked(True)
        self.ui.temperatureCheckBox.setChecked(True)

        self.writeLog("Başlangıç ayarları yüklendi.")

    # Send command to board
    def sendCommand(self, komut):
        if self.serialConnect and self.serialConnect.is_open:
            try:
                self.serialConnect.write((komut + '\n').encode('utf-8'))
                self.writeLog(f"=> {komut}")
            except Exception as e:
                self.writeLog(f"Hata: {e}")
        else:
            self.writeLog("Uyarı: Port kapalı!")

    # Scan ports with serial library
    def scanPorts(self):
        self.ui.portCombo.clear()
        ports = serial.tools.list_ports.comports()
        for port in ports:
            self.ui.portCombo.addItem(port.device)

    # When clicked fullset button
    def runFullset(self):
        self.sendCommand("CMD FULLSET 255 30 FE")

        self.ui.fanSlider.setValue(30)
        self.ui.label_2.setText("Fan Hızı: %30")

        for p in range(22, 30):
            button = self.pinButtons.get(p)
            if button:
                setattr(self, f"pin{p}", True)
                button.setChecked(True)

        for p in [22, 23, 24, 25]:
            QTimer.singleShot(5000, lambda p=p: self.resetPinUI(p))

    # To get loadcell value
    def toggleLoadcell(self):
        self.loadcellActive = not self.loadcellActive
        val = 1 if self.loadcellActive else 0
        self.sendCommand(f"CMD SET LOADCELL_ACTIVE {val}")
        self.sendCommand(f"CMD SET LOADCELL_PUBLISH_ENABLED {val}")

    # Loadcell calibrate step one
    def runCalibrateS1(self):
        self.msg1 = QMessageBox(self)
        self.sendCommand(f"CMD SET LOADCELL_DO_CALIBRATION {self.ui.calibrateWeight.text()}")
        self.msg1.setWindowTitle("Boşaltma İşlemi")
        self.msg1.setText("Loadcell üzerini boşaltın!")
        self.msg1.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.msg1.show()
        QTimer.singleShot(2500, self.runCalibrateS2)

    # Loadcell calibrate step two
    def runCalibrateS2(self):
        if hasattr(self, "msg1"):
            self.msg1.accept()
        self.msg2 = QMessageBox(self)
        self.msg2.setWindowTitle("Kalibre İşlemi")
        self.msg2.setText(f"Lütfen loadcell üzerine {self.ui.calibrateWeight.text()} gram ağırlığında cisim koyun!")
        self.msg2.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.msg2.show()
        QTimer.singleShot(12000, self.finishCalibrate)

    # Loadcell calibrate last step
    def finishCalibrate(self):
        if hasattr(self, "msg2"):
            self.msg2.accept()
        
        log_text = self.ui.logScreen.toPlainText().strip().split('\n')
        cal_value = "Bilinmiyor"
        
        for line in reversed(log_text):
            if "OK LOADCELL_DO_CALIBRATION" in line:
                parts = line.split()
                if len(parts) >= 4:
                    cal_value = parts[3]
                break
        
        QMessageBox.information(self, "Tamamlandı", f"Kalibrasyon işlemi tamamlandı.\nYeni Kalibrasyon Katsayısı: {cal_value}")
        

    # When did drag slider
    def changeFanSpeed(self):
        val = self.ui.fanSlider.value()
        self.ui.label_2.setText(f"Fan Hızı: %{val}")
        self.sendCommand(f"CMD SET FAN {val}")

    # Activate or deactivate heartbeat
    def updateHeartbeat(self):
        val = 1 if self.ui.heartbeatCheckBox.isChecked() else 0
        self.sendCommand(f"CMD SET HEARTBEAT {val}")

    # Activate or deactivate RFID
    def activeRFID(self):
        self.RFID = not self.RFID
        self.sendCommand(f"CMD SET RFID_ACTIVE {1 if self.RFID else 0}")

    # Activate or deactivate continuous data
    def toggleContinuousData(self):
        self.continuousData = not self.continuousData
        self.sendCommand(f"CMD SET SEND_DATA_CONTINUOUSLY {1 if self.continuousData else 0}")

    # Activate or deactivate temperature value
    def toggleTemperature(self):
        self.tempActive = not self.tempActive
        self.sendCommand(f"CMD SET TEMP_ACTIVE {1 if self.tempActive else 0}")

    # Turn on or Turn off pins
    def togglePin(self, pin):
        pin_state_name = f"pin{pin}" 
        
        currentState = getattr(self, pin_state_name, False)
        newState = not currentState
        
        setattr(self, pin_state_name, newState)
        
        self.sendCommand(f"CMD SET {pin} {1 if newState else 0}")
        
        if pin in [22, 23, 24, 25] and newState:
            QTimer.singleShot(5000, lambda: self.resetPinUI(pin))

    # Reset pin UI (for Pin 22, 23, 24 and 25)
    def resetPinUI(self, pin):
        setattr(self, f"pin{pin}", False)
        
        button = self.pinButtons.get(pin)
        
        if button:
            button.setChecked(False)         

    # To take tare
    def runTare(self):
        self.sendCommand("CMD SET LOADCELL_TARE 0")
        self.message1 = QMessageBox(self)
        self.message1.setWindowTitle("Dara Alma İşlemi")
        self.message1.setText("Dara alınıyor...")
        self.message1.setStandardButtons(QMessageBox.StandardButton.NoButton)
        self.message1.show()
        QTimer.singleShot(2500, self.finishTare)

    # Finish tare function
    def finishTare(self):
        if hasattr(self, "message1"):
            self.message1.accept()

        QMessageBox.information(self, "Tamamlandı", "Dara alma işlemi tamamlandı. Devam etmek için OK butonuna basın.")

    def runTest(self):
        # Testi başlatmak için önce uyarıyı gösterir
        self.showWarning()

    def runTest(self):
        # Test değişkenlerini yerel olarak sıfırla
        self.testResults = {} 
        self.showWarning()

    def showWarning(self):
        reply = QMessageBox.information(self, "UYARI", 
            "Test bitene kadar komut göndermeyiniz.\nTest bittiğinde sonucunu ekranda göreceksiniz!")
        if reply == QMessageBox.StandardButton.Ok:
            self.testS1_Loadcell()

    def testS1_Loadcell(self):
        self.sendCommand("CMD SET SEND_DATA_CONTINUOUSLY 1")
        self.sendCommand("CMD SET LOADCELL_ACTIVE 1")
        QTimer.singleShot(1000, self.checkS1_And_StartS2)

    def checkS1_And_StartS2(self):
        # Kontrol et ve veriyi kaydet
        val = self.ui.loadcellValueLabel.text()
        self.testResults['LOADCELL'] = "GEÇTİ" if val != "---" else "KALDI"
        self.sendCommand("CMD SET LOADCELL_ACTIVE 0")
        
        # RFID Testine geç
        self.sendCommand("CMD SET RFID_ACTIVE 1")
        QTimer.singleShot(1000, self.checkS2_And_StartS3)

    def checkS2_And_StartS3(self):
        val = self.ui.RFIDValueLabel.text()
        self.testResults['RFID'] = "GEÇTİ" if val != "---" else "KALDI"
        self.sendCommand("CMD SET RFID_ACTIVE 0")
        
        # Sıcaklık Testine geç
        self.sendCommand("CMD SET TEMP_ACTIVE 1")
        QTimer.singleShot(1000, self.checkS3_And_StartS4)

    def checkS3_And_StartS4(self):
        val = self.ui.temperatureValueLabel.text()
        self.testResults['SICAKLIK'] = "GEÇTİ" if val != "---" else "KALDI"
        
        # Heartbeat Testine geç
        self.sendCommand("CMD SET HEARTBEAT 1")
        QTimer.singleShot(1000, self.checkS4_And_StartS5)

    def checkS4_And_StartS5(self):
        self.sendCommand("CMD SET HEARTBEAT 0")
        val = self.ui.heartbeatValueLabel.text()
        self.testResults['HEARTBEAT'] = "GEÇTİ" if val != "---" else "KALDI"
        
        # Pin Testlerini başlat
        self.currentTestPin = 22
        self.startPinTest()

    def startPinTest(self):
        if self.currentTestPin <= 29:
            self.sendCommand(f"CMD SET {self.currentTestPin} 1")
            msg = QMessageBox(self)
            msg.setWindowTitle("Pin Kontrol")
            msg.setText(f"Pin {self.currentTestPin} çalışıyor mu?")
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            
            res = "OK" if msg.exec() == QMessageBox.Yes else "HATA"
            self.testResults[f'Pin {self.currentTestPin}'] = res
            
            self.sendCommand(f"CMD SET {self.currentTestPin} 0")
            self.currentTestPin += 1
            self.startPinTest()
        else:
            self.finalizeTest()

    def finalizeTest(self):
        self.sendCommand("CMD SET LOADCELL_TARE 0")
        self.writeLog("Sistem: Dara alınıyor, lütfen 3 saniye bekleyin...")
        
        QTimer.singleShot(3000, self.showFinalTestReport)

    def showFinalTestReport(self):
        log_content = self.ui.logScreen.toPlainText()
        self.testResults['HEARTBEAT'] = "GEÇTİ" if "<= WARN LOOP_TIME" in log_content else "KALDI"
        
        report = "TEST SONUÇLARI\n\n"
        
        for key in ['LOADCELL', 'RFID', 'SICAKLIK', 'HEARTBEAT', 'TARE']:
            if key in self.testResults:
                report += f"{key}: {self.testResults[key]}\n"
        
        report += "\nPİN KONTROLLERİ\n"
        
        # Pin Sonuçları
        for pin in range(22, 30):
            pinKey = f'Pin {pin}'
            if pinKey in self.testResults:
                report += f"{pinKey}: {self.testResults[pinKey]}\n"
        
        # 4. Final Mesajını Göster
        QMessageBox.information(self, "Test Tamamlandı", report)

# Run application
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())