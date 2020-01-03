# -*- coding: utf-8 -*-
# @Time    : 2020/1/1 18:29
# @Author  : zhanghao
# @FileName: get_video
# @Software: PyCharm

from location import NewLocation, Location, Position
from constant import *

import cv2
import json
import numpy as np
import time


# 增加 alpha 通道（透明度通道），但需要保存为 PNG 格式
def get_transparent_image(src, alpha):
    b_channel, g_channel, r_channel = cv2.split(src)

    alpha_channel = np.ones(b_channel.shape, dtype=b_channel.dtype) * 255
    # 最小值为0
    alpha_channel[:, :] = alpha

    img_BGRA = cv2.merge((b_channel, g_channel, r_channel, alpha_channel))

    return img_BGRA


# 泊松融合
# style = cv2.NORMAL_CLONE, cv2.MIXED_CLONE
def poisson_integration(background_img, object_image, center, style=cv2.MIXED_CLONE):
    # Create an all white mask
    mask = 255 * np.ones(object_image.shape, object_image.dtype)

    # The location of the center of the src in the dst
    width, height, channels = background_img.shape
    # print(center)
    # Seamlessly clone src into dst and put the results in output
    poisson_image = cv2.seamlessClone(object_image, background_img, mask, center, style)
    return poisson_image


def get_img_obj(location):
    target_image = cv2.imread(location.get_file_name())
    # print(location.get_file_name())
    # cv2.imshow('target', target_image)
    # cv2.waitKey(200)
    return target_image


def create_video():
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    out = cv2.VideoWriter('last_result-mixed.avi', fourcc, 30, (VIDEO_WIDTH, VIDEO_HEIGHT))

    # 读入 new_index.json 文件
    index_json = open('new_index.json', 'r')
    video_index = json.load(index_json)

    background_img = cv2.imread('background.jpg')
    frame_image = background_img
    fps = 0.0
    count = 0

    # 生成每一帧的图片并写入到视频中
    for frame in video_index:
        t1 = time.time()
        # if frame['new_frame_index'] > 50:
        #     break
        frame_image = background_img
        print(frame['new_frame_index'])
        for loc_json in frame['locations']:
            location = NewLocation().json2obj(loc_json=loc_json)
            # print(location.target_id)
            frame_image = poisson_integration(frame_image, get_img_obj(location), location.get_bigger_centeroid())
            count += 1
            # cv2.imshow('frame', frame_image)
            # cv2.waitKey(5)

        out.write(frame_image)
        fps = (fps + (1. / (time.time() - t1))) / 2
        print("fps= %f" % (fps))
        print(count)
    # 释放
    out.release()
    print(count)
    # cv2.imshow('frame_01', frame_image)
    # cv2.imwrite('frame_01_mixed.jpg', frame_image)
    # cv2.waitKey()


create_video()