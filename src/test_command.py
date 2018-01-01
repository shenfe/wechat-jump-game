from subprocess import call
import os

os.system('adb shell screencap -p | sed "s/\r\r$//g" > ' + os.path.normpath("data/test.png"))
