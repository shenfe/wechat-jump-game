import argparse
import os
import cv2
from detect import region


ap = argparse.ArgumentParser()
ap.add_argument("-t", "--template", required=False, default=-1, help="index of the template", type=int)
args = vars(ap.parse_args())
ti = args["template"]

count = len(os.listdir('data/screenshot'))
for i in range(count - 1, count):
    image = cv2.imread(os.path.normpath('data/screenshot/' + str(i) + '.png'), 0)
    r = region(image, ti)
    cv2.rectangle(image, (r[1], r[2]), (r[1] + r[3], r[2] + r[4]), (0, 0, 255), 2)
    cv2.imshow('output', image)
    cv2.waitKey(0)
