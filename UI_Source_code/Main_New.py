"""
Version 0.1
Soft Robot Controller UI
Author: YingGwan
Function: A tool to conveniently adjust airbag pressure
"""
import sys
from PyQt5 import QtCore, QtGui, QtWidgets,Qt
import qdarkstyle
from NEWUI import Ui_MainWindow
from thread1 import Thread1


class CtrlWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(CtrlWindow, self).__init__(parent)
        self.MyUI=Ui_MainWindow();
        self.MyUI.setupUi(self);


        self.setWindowTitle('Soft Robot Controller')
        # pg.setConfigOption('background', '#31363b')
        # pg.setConfigOption('foreground', 'w')

        #Connect to slot functions
        self.MyUI.ConnectButton.clicked.connect(self.connect_buttonClicked)
        self.MyUI.QuitButton.clicked.connect(self.quit_buttonClicked)
        self.MyUI.ClearAllVolt.clicked.connect(self.resetvoltageClicked)
        self.MyUI.ClearBridgeButton.clicked.connect(self.resethalfBridgeClicked)


        self.MyUI.ChannelOpen.clicked.connect(self.SwitchOn)
        self.MyUI.ChannelClose.clicked.connect(self.SwitchOff)

        self.MyUI.Regulator1.clicked.connect(self.Regulator1_Slot)
        self.MyUI.Regulator2.clicked.connect(self.Regulator2_Slot)



#Slot Functions Area
    #Connecting
    def connect_buttonClicked(self):
        t1.link();
        t1.run();

    #Quit
    def quit_buttonClicked(self):
        print("Quit")
        QtWidgets.qApp.quit();

    #Reset all voltage to 0V.
    def resetvoltageClicked(self):
        t1.sendResetCmd();

    #Reset all bridge out to 0V
    def resethalfBridgeClicked(self):
        t1.HalfBridgeLowCmd();

    #Switches on.
    def SwitchOn(self):

        Channel=self.MyUI.lineEdit_2.text()
        # t1.SetHigh(4);
        ChannelNo=int(Channel)
        print(ChannelNo)
        t1.SetHigh(ChannelNo)
        # print(Channel + " ON")

    # Switches off.
    def SwitchOff(self):
        Channel = self.MyUI.lineEdit_2.text()
        # t1.SetHigh(4);
        ChannelNo = int(Channel)
        t1.SetLow(ChannelNo);
        print(Channel+" OFF")

    def Regulator1_Slot(self):
        VoltageStr = self.MyUI.lineEdit_3.text()
        Voltage=float(VoltageStr);
        print("Voltage 1>--->")
        print(Voltage);
        t1.SendVoltage(1, Voltage);
        self.MyUI.lcdNumber.display(VoltageStr)

    def Regulator2_Slot(self):
        VoltageStr = self.MyUI.lineEdit_4.text()
        Voltage=float(VoltageStr);
        print("Voltage 2>--->")
        print(Voltage);
        t1.SendVoltage(2,Voltage);
        self.MyUI.lcdNumber_2.display(VoltageStr)

t1=1;
if __name__ == "__main__":
    t1 = Thread1(); #Get thread 1.
    app = QtWidgets.QApplication(sys.argv)
    #Set UI style
    #app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # app.setStyleSheet('QMainWindow{background-color: dark;border: 1px solid black;}')
    myWin = CtrlWindow()
    myWin.show()


    sys.exit(app.exec_())