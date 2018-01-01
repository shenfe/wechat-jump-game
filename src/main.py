import screenshot
import detect
import distance_time
import touch
import time
from config import test
import argparse

loop = True

def run():
    global loop

    ap = argparse.ArgumentParser()
    ap.add_argument("-t", "--template", required=False, default=-1, help="index of the template", type=int)
    ap.add_argument("-x", "--sx", required=False, default=-1, help="x of the location", type=int)
    ap.add_argument("-y", "--sy", required=False, default=-1, help="y of the location", type=int)
    args = ap.parse_args()
    ti = args.template
    sx = args.sx
    sy = args.sy
    print(args)

    while loop:
        loop = not test
        if loop:
            time.sleep(2)
        imgpath = screenshot.run()

        result = detect.run(imgpath, ti, sx, sy)

        t = distance_time.compute(result['d'])
        print('t: ', t)
        touch.run(t)

run()