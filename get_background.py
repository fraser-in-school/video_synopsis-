# -*- coding: utf-8 -*-
# @Time    : 2020/1/1 18:29
# @Author  : zhanghao
# @FileName: get_background.py
# @Software: PyCharm

# a file used to create background image

import cv2
from constant import *

capture = cv2.VideoCapture(VIDEO_PATH)
mog = cv2.createBackgroundSubtractorMOG2()
se = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))

while True:
    ret, image = capture.read()
    if ret is True:
        fgmask = mog.apply(image)
        ret, binary = cv2.threshold(fgmask, 220, 255, cv2.THRESH_BINARY)
        binary = cv2.morphologyEx(binary, cv2.MORPH_OPEN, se)
        back_image = mog.getBackgroundImage()
        cv2.imshow("back_image", back_image)
        # Press Q to stop!
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite('./temp_file/background.jpg', back_image)
            break
    else:
        break

cv2.destroyAllWindows()
