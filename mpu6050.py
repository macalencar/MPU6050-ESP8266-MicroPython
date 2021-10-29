import machine
import struct

class accel():
    def __init__(self, i2c, addr=0x68):
        self.iic = i2c
        self.addr = addr
        self.iic.writeto(self.addr, bytearray([107, 0]))

    def get_raw_values(self):
        a = self.iic.readfrom_mem(self.addr, 0x3B, 14)
        return a


    def get_values(self):
        raw_ints = self.get_raw_values()
        acx, acy,acz,tmp, gyx,gyy,gyz = struct.unpack('>hhhhhhh',raw_ints)
        
        vals = {}
        vals["AcX"] = acx
        vals["AcY"] = acy
        vals["AcZ"] = acz
        vals["Tmp"] = tmp / 340.00 + 36.53
        vals["GyX"] = gyx
        vals["GyY"] = gyy
        vals["GyZ"] = gyz
        return vals  # returned in range of Int16
        # -32768 to 32767

    def sleep(self):
        self.iic.start()
        self.iic.writeto_mem(self.addr, 0x6B, b'\x40')
        self.iic.stop()
        
    def wakeup(self):
        from time import sleep
        self.iic.writeto_mem(self.addr, 0x6B, b'\x80')
        sleep(0.05)
        self.iic.writeto_mem(self.addr, 0x68, b'\x07')
        sleep(0.05)
        self.iic.writeto_mem(self.addr, 0x68, b'\x00')
        sleep(0.05)
        self.iic.writeto_mem(self.addr, 0x6B, b'\x00')

    def val_test(self):  # ONLY FOR TESTING! Also, fast reading sometimes crashes IIC
        from time import sleep
        while 1:
            print(self.get_values())
            sleep(0.05)
