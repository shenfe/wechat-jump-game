import argparse
from subprocess import call
import imutils
import cv2
import os
import sys


def run():
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=False, help="path to the input image")
    args = vars(ap.parse_args())

    path1 = "/mnt/sdcard/output.png"

    output_path = "data/screenshot"
    output_files = os.listdir(output_path)
    print(output_files)
    path2 = output_path + "/" + str(len(output_files)) + ".png"
    if args["image"]:
        path2 = args["image"]

    path2 = os.path.normpath(path2)

    call(["adb", "shell", "screencap", "-p", path1])
    call(["adb", "pull", path1, path2])
    call(["adb", "shell", "rm", path1])

    image = cv2.imread(path2)
    resized = imutils.resize(image, width=300)

    gray = cv2.cvtColor(resized, cv2.COLOR_BGR2GRAY)

    cv2.imwrite(path2, gray)

    # cv2.imshow("Image", gray)
    # cv2.waitKey(0)

    # if sys.platform.startswith('darwin'):
    #     os.subprocess.call(('open', path2))
    # elif os.name == 'nt':
    #     os.startfile(path2)
    # elif os.name == 'posix':
    #     os.subprocess.call(('xdg-open', path2))

    return path2
