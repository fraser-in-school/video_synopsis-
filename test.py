# -*- coding: utf-8 -*-
# @Time    : 2020/1/1 18:29
# @Author  : zhanghao
# @FileName: test.py
# @Software: PyCharm

# a file used to test some code, just like a temp file
# 注意修改路径！
import cv2
import numpy as np

# Read images : src image will be cloned into dst
img = cv2.imread("background.jpg")
obj = cv2.imread("./targets_image/target_4/0-0-540-34-637.jpg")

# Create an all white mask
mask = 255 * np.ones(obj.shape, obj.dtype)

# The location of the center of the src in the dst
width, height, channels = img.shape
center = (20, 588)

# Seamlessly clone src into dst and put the results in output
normal_clone = cv2.seamlessClone(obj, img, mask, center, cv2.NORMAL_CLONE)
mixed_clone = cv2.seamlessClone(obj, img, mask, center, cv2.MIXED_CLONE)

# Write results
cv2.imshow("images/opencv-normal-clone-example.jpg", normal_clone)
cv2.waitKey()
cv2.imshow("images/opencv-mixed-clone-example.jpg", mixed_clone)
cv2.waitKey()