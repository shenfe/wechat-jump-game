import screenshot
import detect
import distance_time
import touch
import time

loop = True

while loop:
    # loop = False
    time.sleep(2)
    imgpath = screenshot.run()
    result = detect.run(imgpath)
    t = distance_time.compute(result['d'])
    touch.run(t)
