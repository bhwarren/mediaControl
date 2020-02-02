

from SerialDevice import SerialDevice
import sys
import subprocess
import traceback

def setVolume(percent=25):
    percent = max(0, min(100, int(percent))) #limit percent from 0-100

    os = sys.platform
    if os == "win32":
        winVolume = str(int(percent/2)) # windows does things in 2% increments 🙄
        subprocess.call(["powershell.exe", "Function Set-Speaker($Volume){$wshShell = new-object -com wscript.shell;1..50 | % {$wshShell.SendKeys([char]174)};1..$Volume | % {$wshShell.SendKeys([char]175)}} ; Set-Speaker("+winVolume+")"], shell=True)
    elif os == "darwin":
        subprocess.call("osascript -e 'set volume output volume "+str(percent)+"'", shell=True)
    elif os == "linux":
        val = float(int(percent))
        proc = subprocess.Popen('/usr/bin/amixer sset Master ' + str(val) + '%', shell=True, stdout=subprocess.PIPE)
        proc.wait()


def cb(event):
    try:
        print(event)
        if(event.startswith("set_volume_")):
            percent = event.split("_")[-1]
            setVolume(percent)
    except:
        traceback.print_exc()


pidVid = (32799, 9114)
mediaDevice = SerialDevice(cb, pidVid)