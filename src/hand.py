import screenshot
import detect
import distance_time
import touch
import time
import cv2
from subprocess import call
from config import test
import argparse

loop = True


def click_handler(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(x, y)
        call(["python", "src/main.py", "-x", str(x), "-y", str(y)])

        if loop:
            cv2.destroyWindow("Image")
            time.sleep(2)
            load_img()


def load_img():
    imgpath = screenshot.run()
    image = cv2.imread(imgpath, 0)
    cv2.namedWindow("Image")
    cv2.setMouseCallback("Image", click_handler)
    cv2.imshow("Image", image)
    cv2.waitKey(0)


load_img()