import asyncio
import serial
import serial.tools.list_ports
import re
import traceback as tb

# a class that looks for a specific serial port and listens for events
# and executes the supplied callback on any event
class SerialDevice:
    def __init__(self, callback, pidVidTuple):
        self.callback = callback
        self.isConnected = False
        self.loop = asyncio.get_event_loop()
        self.serialDevice = None
        self.pid = str(pidVidTuple[0])
        self.vid = str(pidVidTuple[1])
        self.start()
    
    def setEventProcessor(self, callback):
        self.callback = callback

    # find the serial device and open it, listening for events
    def start(self):
        self.loop.run_until_complete(self.setupSerial())
    
    # close the serial connection and stop listening for events
    def stop(self):
        self.isRunning = False
        if self.serialDevice:
            self.serialDevice.close()
        self.loop.stop()

    # return the serial device with the given pid & vid
    def getSerialDevice(self):
        ports=serial.tools.list_ports.comports(include_links=False)
        for p in ports:
            if(str(p.pid) == self.pid and str(p.vid) == self.vid):
                return serial.Serial(p.device)
        return None

    # read serial lines, and async call the callback
    def listenForEvents(self, serial):
        while(serial.isOpen()):
            event = serial.readline().decode('utf-8').strip()
            self.loop.run_in_executor(None, self.callback, event)

    # forever run, waiting for serial connections
    async def setupSerial(self):
        self.isRunning = True
        print("searching for devices...")
        while self.isRunning:
            try:
                self.serialDevice = self.getSerialDevice()
                print("initialized on device "+self.serialDevice.port)
                print("waiting for events...")
                self.isConnected = True
                await self.listenForEvents(self.serialDevice)
            except Exception as e:
                self.isConnected = False
                await asyncio.sleep(5)