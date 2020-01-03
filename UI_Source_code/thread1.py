#This contains class used for serial communication
from PyQt5 import QtCore, QtGui, QtWidgets
from deviceComScript import MySerial

import serial
import serial.tools.list_ports


class Thread1(QtCore.QThread):
    sinOut1 = QtCore.pyqtSignal(str)
    flag ="None"
    def link(self):
        self.serial = MySerial(
            port=None,
            baudrate=115200,  # Serial baudrate：115200bps
            # Following settings are not used.
            # bytesize=EIGHTBITS, # Eight data bits
            # parity=PARITY_NONE, # No parity bit.
            # stopbits=STOPBITS_ONE, # One stop bit.
            timeout=1,  # read timeout
            xonxoff=False,
            rtscts=False,
            write_timeout=0.5,  # write timeout
            dsrdtr=False,
            inter_byte_timeout=None,
            exclusive=None)
        if self.serial.is_open is True:  # Check if it is opened.
            self.serial.close()
            print("The serial port has been closed. Try to reconnect!")
        # Get serial list.
        self.plist = list(serial.tools.list_ports.comports())

        if len(self.plist) <= 0:  # 无串口
            self.sinOut1.emit("no port")
            print("no port")
            self.flag = "end"

        else:
            # Connect to first serial port.
            print("connecting.")
            plist_0 = list(self.plist[0])
            serialName = plist_0[0]
            self.serial.port = serialName
            self.serial.open()
            self.sinOut1.emit(serialName)
            self.serial.reset_input_buffer()
            print("Already connected.")
            self.flag = "start";

    def run(self):
        print("Try to communicate")
        try:
            if self.flag is "start":
                self.serial.write(b"AT\r\n")
                answer = self.serial.read_until()
                print(answer)
                if answer[-4:] == b"OK\r\n":
                    self.sinOut1.emit("Success")
                    print("Success")
                else:
                    if answer[-3:]==b"":
                        print("empty command")
                    else:
                        self.serial.reset_input_buffer()  # Clear input buffer
                        self.sinOut1.emit("Error")
                        print("Error response")
        except serial.SerialException as e:  # Serial operations go wrong.
            self.sinOut1.emit(str(e))
            print(str(e))

    def sendResetCmd(self):
        try:
            if self.flag is "start":
                self.serial.write(b"AT+RESET\r\n")
                answer = self.serial.read_until()
                if answer[-4:] == b"OK\r\n":
                    self.sinOut1.emit("Success")
                    print("All reset to 0V")
                else:
                    if answer[-3:] == b"":
                        print("empty command")
                    else:
                        self.serial.reset_input_buffer()
                        self.sinOut1.emit("Error")
                        print("Error response")
        except serial.SerialException as e:
            self.sinOut1.emit(str(e))
            print(str(e))

    def HalfBridgeLowCmd(self):
        try:
            if self.flag is "start":
                self.serial.write(b"AT+RESETR\r\n")
                answer = self.serial.read_until()
                if answer[-4:] == b"OK\r\n":
                    self.sinOut1.emit("Success")
                    print("All half-bridges reset to 0V")
                else:
                    if answer[-3:] == b"":
                        print("empty command")
                    else:
                        self.serial.reset_input_buffer()
                        self.sinOut1.emit("Error")
                        print("Error response")
        except serial.SerialException as e:
            self.sinOut1.emit(str(e))
            print(str(e))

    def SetDAC1Voltage(self):
        try:
            if self.flag is "start":
                self.serial.write(b"AT+RESET\r\n")

                answer = self.serial.read_until()

                if answer[-4:] == b"OK\r\n":
                    self.sinOut1.emit("Success")
                    print("All reset to 0V")
                else:
                    if answer[-3:] == b"":
                        print("empty command")
                    else:
                        self.serial.reset_input_buffer()
                        self.sinOut1.emit("Error")
                        print("Error response")
        except serial.SerialException as e:
            self.sinOut1.emit(str(e))
            print(str(e))

    #Pull up Port No to become 24V
    def SetHigh(self,No):
        #Up to 6 ports
        try:
            if self.flag is "start":

                if No<10:
                    a = "AT+RON=0"
                else:
                    a = "AT+RON="

                c = "\r\n"
                b = repr(No)

                cmd=a+b+c;

                self.serial.write(cmd.encode("utf-8"))#gbk  utf-8
                answer = self.serial.read_until()
                if answer[-4:] == b"OK\r\n":
                    self.sinOut1.emit("Success")
                    print("Port %d Pull up to 24V"%No)
                    print("Success")
                else:
                    if answer[-3:] == b"":
                        print("empty command")
                    else:
                        self.serial.reset_input_buffer()
                        self.sinOut1.emit("Error")
                        print("Error response")
        except serial.SerialException as e:
            self.sinOut1.emit(str(e))
            print(str(e))

    #Pull down Port No to become 0V
    def SetLow(self,No):
        #Up to 6 ports
        try:
            if self.flag is "start":

                if No<10:
                    a = "AT+ROFF=0"
                else:
                    a = "AT+ROFF="

                c = "\r\n"
                b = repr(No)

                cmd=a+b+c;
                print(cmd)
                self.serial.write(cmd.encode("utf-8"))#gbk  utf-8
                answer = self.serial.read_until()
                if answer[-4:] == b"OK\r\n":
                    self.sinOut1.emit("Success")
                    print("Port %d Pull down to 0V"%No)
                else:
                    if answer[-3:] == b"":
                        print("empty command")
                    else:
                        self.serial.reset_input_buffer()
                        self.sinOut1.emit("Error")
                        print("Error response")
        except serial.SerialException as e:
            self.sinOut1.emit(str(e))
            print(str(e))



    def SendVoltage(self,Port,Volt):
        """
        #Up to 2 ports
        #Input : Volt ∈ [0,10]
        #Output: Cmd  ∈ [0,4095]
        #Transition:
            Cmd=4095/10.0*Volt
            Out=hex((int)Cmd)
        """
        try:
            if self.flag is "start":

                if Port==1:
                    a = "AT+DAC1="
                else:
                    a = "AT+DAC2="

                c = "\r\n"

                Cmd = 4095.0 / 10.0 * Volt
                Cmd=int(Cmd)
                Out = hex(Cmd)
                OutPut=Out[2:]

                cmd=a+OutPut+c;
                print(cmd)
                self.serial.write(cmd.encode("utf-8"))#gbk  utf-8
                answer = self.serial.read_until()
                if answer[-4:] == b"OK\r\n":
                    self.sinOut1.emit("Success")
                    print("Regulator %d Pulled to %lf V"%(Port,Volt))
                else:
                    if answer[-3:] == b"":
                        print("empty command")
                    else:
                        self.serial.reset_input_buffer()
                        self.sinOut1.emit("Error")
                        print("Error response")
        except serial.SerialException as e:
            self.sinOut1.emit(str(e))
            print(str(e))