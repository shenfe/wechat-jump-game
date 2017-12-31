import cv2
import math
import screenshot
import os


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
                cv2.rectangle(image, (mid, i), (mid, i), (0, 0, 255), 2)
                # cv2.imshow('output', image)
                # cv2.waitKey(0)
                return mid, i


def region(image):
    arr = []
    for i in range(len(os.listdir('data/template'))):
        image1 = cv2.imread(os.path.normpath('data/template/' + str(i) + '.png'), 0)
        result = cv2.matchTemplate(image, image1, cv2.TM_SQDIFF_NORMED)
        result1 = cv2.minMaxLoc(result)
        min_val, max_val, min_loc, max_loc = result1
        if min_loc[1] < 100:
            continue
        height, width = image1.shape
        result2 = ((min_val + max_val) / 2, min_loc[0], min_loc[1], width, height, i)
        # print(i, result2)
        arr.append(result2)
    arr.sort(key=lambda x: x[2])
    # for item in arr:
    #     print(item)
    arr1 = arr[1:]
    j = 0
    for i in range(len(arr1)):
        if arr1[i][2] - arr[i][2] > 10:
            break
        if (arr1[i][0] < arr[j][0] and arr[j][2] - 5 < arr1[i][2] < arr[j][2] + 5) \
                or (arr1[i][0] < arr[j][0] + 0.02 and arr1[i][3] > arr[j][3] + 20):
            j = i + 1
            continue
    # print(arr[j][5])
    return arr[j]


# # Test
# for i in range(0, 10):
#     image = cv2.imread(os.path.normpath('data/screenshot/' + str(i) + '.png'), 0)
#     r = region(image)
#     cv2.rectangle(image, (r[1], r[2]), (r[1] + r[3], r[2] + r[4]), (0, 0, 255), 2)
#     cv2.imshow('output', image)
#     cv2.waitKey(0)


def run(imgpath):
    image = cv2.imread(imgpath, 0)
    p0 = point0(image)
    r = region(image)
    p1 = point1(image, p0)
    if math.fabs(p1[0] - (r[1] + r[3] / 2)) < 5:
        p1 = (r[1] + r[3] / 2, r[2] + r[4])
    w = p1[0] - p0[2][0]
    h = p0[2][1] - p1[1]
    d = math.sqrt(w * w + h * h)
    re = dict(p0=p0, p1=p1, w=w, h=h, d=d)
    # print(re)
    return re
