import cv2
import math
import os
import argparse
import screenshot
from config import test


template_path = 'data/chess.png'



def point0(large_image):
    # Refer: https://stackoverflow.com/questions/7853628/how-do-i-find-an-image-contained-within-an-image

    small_image = cv2.imread(template_path, 0)

    result = cv2.matchTemplate(large_image, small_image, cv2.TM_SQDIFF_NORMED)

    # Want the minimum squared difference
    mn, _, mnloc, _ = cv2.minMaxLoc(result)

    # Draw the rectangle:
    # Extract the coordinates of our best match
    mpx, mpy = mnloc

    # Step 2: Get the size of the template. This is the same size as the match.
    trows, tcols = small_image.shape[:2]

    # Step 3: Draw the rectangle on large_image
    p1 = (mpx, mpy)
    p2 = (mpx + tcols, mpy + trows)
    p = (mpx + 10, mpy + 53)
    cv2.rectangle(large_image, p1, p2, (0, 0, 255), 1)
    cv2.rectangle(large_image, p, p, (0, 0, 255), 2)

    # # Display the original image with the rectangle around the match.
    # cv2.imshow('output', large_image)
    #
    # # The image is only displayed if we call this
    # cv2.waitKey(0)

    return p1, p2, p


def point1(image, p0):
    imgpath2 = screenshot.run()
    c1, c2, c0 = p0
    image2 = cv2.imread(imgpath2, 0)
    height, width = image.shape
    for i in range(150, height):
        flag = False
        color = image[i, 0]
        # print("this line color: ", color)
        start = 0
        for j in range(1, width):
            if (c1[1] - 5) <= i <= (c2[1] + 5) and (c1[0] - 3) <= j <= (c2[0] + 3):
                continue
            if image[i, j] != color and image[i, j] == image2[i, j] and not flag:
                flag = True
                start = j
                continue
            if image[i, j] == color and flag:
                end = j
                mid = int((start + end - 1) / 2)
                # cv2.rectangle(image, (mid, i), (mid, i), (0, 0, 255), 2)
                # cv2.imshow('output', image)
                # cv2.waitKey(0)
                return mid, i


def _next_point(d, p):
    d = d % 8
    if d == 0: return p[0] - 1, p[1]
    if d == 1: return p[0] - 1, p[1] - 1
    if d == 2: return p[0], p[1] - 1
    if d == 3: return p[0] + 1, p[1] - 1
    if d == 4: return p[0] + 1, p[1]
    if d == 5: return p[0] + 1, p[1] + 1
    if d == 6: return p[0], p[1] + 1
    return p[0] - 1, p[1] + 1


def point2(image, p1):
    j, i = p1
    while True:
        if image[i, j - 1] == image[i, j] \
                and image[i, j + 1] == image[i, j]:
            break
        else:
            i += 1
    print("top point: ", i, j)
    ii = i
    jj = j
    bottom_y = i
    bottom_x = j
    cur_color = image[ii, jj]
    print("find color: ", cur_color)

    d = 2  # 0: up, 1: up-left, 2: left, ..., 7: right-up
    last_d = d
    p = (ii, jj)
    while 2 <= d <= 6:
        if math.fabs(d - last_d) == 4:
            d += 1
            continue
        q = _next_point(d, p)
        if image[q[0], q[1]] != cur_color:
            d += 1
            continue
        last_d = d
        if q[0] > bottom_y:
            bottom_y = q[0]
            bottom_x = q[1]
        # print("find next p: ", q, cur_color)
        p = q
        d = 2

    d = 6
    last_d = d
    p = (ii, jj)
    while 2 <= d <= 6:
        if math.fabs(d - last_d) == 4:
            d -= 1
            continue
        q = _next_point(d, p)
        if image[q[0], q[1]] != cur_color:
            d -= 1
            continue
        last_d = d
        if q[0] > bottom_y:
            bottom_y = q[0]
            bottom_x = q[1]
        p = q
        d = 6

    print("bottom point: ", bottom_y, bottom_x)
    return bottom_x, bottom_y


def region(image, template_index=-1):
    arr = []
    if template_index >= 0:
        i = template_index
        image1 = cv2.imread(os.path.normpath('data/template/' + str(i) + '.png'), 0)
        result = cv2.matchTemplate(image, image1, cv2.TM_SQDIFF_NORMED)
        result1 = cv2.minMaxLoc(result)
        min_val, max_val, min_loc, max_loc = result1
        height, width = image1.shape
        result2 = ((min_val + max_val) / 2, min_loc[0], min_loc[1], width, height, i)
        if test: print(i, result2)
        return result2
    else:
        for i in range(len(os.listdir('data/template'))):
            image1 = cv2.imread(os.path.normpath('data/template/' + str(i) + '.png'), 0)
            result = cv2.matchTemplate(image, image1, cv2.TM_SQDIFF_NORMED)
            result1 = cv2.minMaxLoc(result)
            min_val, max_val, min_loc, max_loc = result1
            if min_loc[1] < 100:
                continue
            height, width = image1.shape
            result2 = ((min_val + max_val) / 2, min_loc[0], min_loc[1], width, height, i)
            if test: print(i, result2)
            arr.append(result2)
        arr.sort(key=lambda x: x[2])
        if test:
            for item in arr:
                print(item)
        arr1 = arr[1:]
        j = 0
        for i in range(len(arr1)):
            if math.fabs(arr1[i][2] - arr[i][2]) > 10:
                break
            if (arr1[i][0] < arr[j][0] and arr[j][2] - 5 < arr1[i][2] < arr[j][2] + 5) \
                    or (arr1[i][0] < arr[j][0] + 0.02 and arr1[i][3] > arr[j][3] + 20) \
                    or (math.fabs(arr1[i][2] - arr[j][2]) <= 10 and arr1[i][4] * 2 <= arr[j][4]):
                j = i + 1
                continue

        if test: print(arr[j][5])
        return arr[j]


def run(imgpath, template_index=-1, sx=-1, sy=-1):
    image = cv2.imread(imgpath, 0)
    p0 = point0(image)

    p1 = (sx, sy)
    if not (sx > 0 and sy > 0):
        r = region(image, template_index)
        p1 = point1(image, p0)
        p2 = point2(image, p1)
        print(p1, p2)
        if (math.fabs(p1[0] - p2[0]) < 3) and (20 <= p2[1] - p1[1] <= 75):
            p1 = ((p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2)
            print(1)
        elif (math.fabs(p1[0] - (r[1] + r[3] / 2)) < 5) \
                and (math.fabs(p1[1] - (r[2] + r[4])) < 50):
            p1 = (r[1] + r[3] / 2, r[2] + r[4])
            print(2)
        else:
            p1 = (p1[0], p1[1] + 10)
            print(3)

    w = p1[0] - p0[2][0]
    h = p0[2][1] - p1[1]
    d = math.sqrt(w * w + h * h)
    re = dict(p0=p0, p1=p1, w=w, h=h, d=d)
    if test: print(re)
    return re
