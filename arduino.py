from serial import Serial
from serial import SerialException

class Arduino(Serial):
    def poll(self, pin=3):
        self.write("POLL " + str(pin))
        return self.readline()[:-2]
