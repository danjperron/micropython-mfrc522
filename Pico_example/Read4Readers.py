from mfrc522 import MFRC522
import utime


def uidToString(uid):
    mystring = ""
    for i in uid:
        mystring = "%02X" % i + mystring
    return mystring
    

class myRFIDReader(MFRC522):
    def __init__(self,cs=6):
        super().__init__(spi_id=0,sck=2,miso=4,mosi=3,cs=cs,rst=0)
        self.key = None
        self.keyIn = False
        self.keyValidCount=0;

    def Read(self):
        status, TagType = self.request(super().REQIDL)
        if status == self.OK:
            status, uid = self.SelectTagSN()
            if status == self.OK:
                self.keyIn=True
                self.keyValidCount=2
                if self.key != uid:
                   self.key = uid
                   if uid is None:
                      return False
                   return True
        else:
            if self.keyIn:
                if self.keyValidCount>0:
                   self.keyValidCount= self.keyValidCount - 1
                else:
                   self.keyIn=False
                   self.key=None
        return False
              
              
reader1 = myRFIDReader(cs=1)
reader2 = myRFIDReader(cs=6)
reader3 = myRFIDReader(cs=7)
reader4 = myRFIDReader(cs=8)

#because of reset to same pins we need to re-init reader
reader1.init()
reader2.init()
reader3.init()
reader4.init()

print("")
print("Please place card on any reader")
print("")


try:
    while True:
        if reader1.Read():
           print("Reader1 : %s" %uidToString(reader1.key))
        if reader2.Read():
           print("Reader2 : %s" %uidToString(reader2.key))
        if reader3.Read():
           print("Reader3 : %s" %uidToString(reader3.key))
        if reader4.Read():
           print("Reader4 : %s" %uidToString(reader4.key))
        
except KeyboardInterrupt:
    pass